#!/usr/bin/env bash
# t2_dispatch.sh — sc-bare-review Wave C, ONE reviewer.
#
# Dispatches a single bare-review request to the OpenAI-compatible proxy and writes the
# model's review markdown to <raw-out> plus a <meta-out> sidecar. Self-contained by
# design: the orchestrator invokes this N times in a SINGLE message (N parallel Bash
# tool calls — AC-1.5 / IMM-3), and a failure here NEVER aborts sibling reviewers
# (AC-1.7) because each runs in its own process.
#
# Usage:
#   t2_dispatch.sh --model <id> --prompt-dir <dir> \
#     --raw-out <path> --meta-out <path> --timeout <sec> --temperature <float>
#
# Env (required): T2ProxyUrl, T2ProxyKey.
# Always exits 0 after writing meta.json — reviewer status lives in the sidecar, not the
# exit code, so the orchestrator can read every reviewer's outcome uniformly.
#
# Spec: merged-requirements.md §3.3 Wave C, §7.4, §8 (5xx retry-once / 4xx no-retry).

set -uo pipefail

MODEL="" ; PROMPT_DIR="" ; RAW_OUT="" ; META_OUT="" ; TIMEOUT=180 ; TEMPERATURE="0.2"
while [ $# -gt 0 ]; do
  case "$1" in
    --model)       MODEL="${2:-}"; shift 2 ;;
    --prompt-dir)  PROMPT_DIR="${2:-}"; shift 2 ;;
    --raw-out)     RAW_OUT="${2:-}"; shift 2 ;;
    --meta-out)    META_OUT="${2:-}"; shift 2 ;;
    --timeout)     TIMEOUT="${2:-180}"; shift 2 ;;
    --temperature) TEMPERATURE="${2:-0.2}"; shift 2 ;;
    *) printf 't2_dispatch: unknown argument: %s\n' "$1" >&2; exit 2 ;;
  esac
done

now_ms() { local n; n="$(date +%s%N 2>/dev/null)"; case "$n" in (*[!0-9]*|'') echo $(( $(date +%s) * 1000 )) ;; (*) echo $(( n / 1000000 )) ;; esac; }

write_meta() { # status http_code elapsed_ms attempts
  jq -n --arg status "$1" --argjson http "${2:-0}" --argjson ms "${3:-0}" \
        --argjson attempts "${4:-1}" --arg model "$MODEL" \
        '{status:$status, http_code:$http, elapsed_ms:$ms, attempts:$attempts, model_id:$model}' \
        > "$META_OUT"
}

[ -n "$MODEL" ] && [ -n "$PROMPT_DIR" ] && [ -n "$RAW_OUT" ] && [ -n "$META_OUT" ] || {
  printf 't2_dispatch: --model, --prompt-dir, --raw-out, --meta-out are required\n' >&2; exit 2; }
: > "$RAW_OUT"
[ -n "${T2ProxyUrl:-}" ] && [ -n "${T2ProxyKey:-}" ] || { write_meta proxy_error 0 0 0; exit 0; }

# Build request body (target content is JSON-escaped here via --arg — never shell-interpolated).
BODY_TMP="$(mktemp)"; RESP_TMP="$(mktemp)"
trap 'rm -f "$BODY_TMP" "$RESP_TMP"' EXIT
jq -n --arg model "$MODEL" \
      --arg sys "$(cat "$PROMPT_DIR/system.txt")" \
      --arg usr "$(cat "$PROMPT_DIR/user.txt")" \
      --argjson temp "$TEMPERATURE" \
      '{model:$model, messages:[{role:"system",content:$sys},{role:"user",content:$usr}], temperature:$temp}' \
      > "$BODY_TMP"

dispatch() { # echoes "http_code", body in $RESP_TMP; returns curl rc
  local rc=0 code
  code="$(curl -s -o "$RESP_TMP" -w '%{http_code}' \
            --max-time "$TIMEOUT" \
            -H "Authorization: Bearer ${T2ProxyKey}" \
            -H "Content-Type: application/json" \
            --data-binary @"$BODY_TMP" \
            "${T2ProxyUrl%/}/chat/completions")" || rc=$?
  echo "${code:-000}"
  return $rc
}

START="$(now_ms)"; ATTEMPTS=1; RC=0
HTTP="$(dispatch)" || RC=$?

# Timeout (curl 28). No retry; the per-reviewer hard cap already elapsed.
if [ "$RC" -eq 28 ]; then
  write_meta timeout 0 "$(( $(now_ms) - START ))" "$ATTEMPTS"; exit 0
fi

# 5xx → retry once after 2s. 4xx → no retry (§8).
if [ "$HTTP" -ge 500 ] 2>/dev/null; then
  sleep 2; ATTEMPTS=2; RC=0
  HTTP="$(dispatch)" || RC=$?
  if [ "$RC" -eq 28 ]; then write_meta timeout 0 "$(( $(now_ms) - START ))" "$ATTEMPTS"; exit 0; fi
fi

ELAPSED="$(( $(now_ms) - START ))"

if [ "$RC" -ne 0 ] || [ "$HTTP" -lt 200 ] 2>/dev/null || [ "$HTTP" -ge 300 ] 2>/dev/null; then
  # Non-2xx (incl. 4xx/5xx-after-retry) or transport error → proxy_error. Keep body for triage.
  cp "$RESP_TMP" "$RAW_OUT" 2>/dev/null || true
  write_meta proxy_error "$HTTP" "$ELAPSED" "$ATTEMPTS"; exit 0
fi

# 2xx: extract assistant content (§3.3 C.2). On extraction failure, retain the raw body
# and flag parse_error so the normalizer (Wave D) can attempt its §7.4 fallback.
CONTENT="$(jq -r '.choices[0].message.content // empty' "$RESP_TMP" 2>/dev/null)"
if [ -z "$CONTENT" ]; then
  cp "$RESP_TMP" "$RAW_OUT" 2>/dev/null || true
  write_meta parse_error "$HTTP" "$ELAPSED" "$ATTEMPTS"; exit 0
fi

printf '%s\n' "$CONTENT" > "$RAW_OUT"
write_meta success "$HTTP" "$ELAPSED" "$ATTEMPTS"
exit 0
