#!/usr/bin/env bash
# Reviewer launcher (DESIGN 2.2): RR's launch, extraction and retry loop, plus H1 brief, sandbox cwd, hang guard,
# per-receiver --settings on attempt 1 only, isolated attempt 2, H2 normalise and one re-ask. No fallback ladder.
# run-reviewer2.sh --pkgdir <runs/row/pkg> --sb <SBR/sb/runid/pkg> --pkg <pkg> --rid <rid> --model <m>
#                  --deadline-ms <T0+hang> [--settings <file>] [--turn-p90 <s>] [--print-cmd]
set -u -o pipefail
. "$(dirname "$0")/lib/common.sh"
shopt -u patsub_replacement 2>/dev/null || true
PKGDIR="" SB="" PKG="" RID="" MODEL="" DEADLINE="" SETTINGS="" TURN=6.4 PRINT=0
while [ $# -gt 0 ]; do case "$1" in
  --pkgdir) PKGDIR=$2; shift 2;; --sb) SB=$2; shift 2;; --pkg) PKG=$2; shift 2;; --rid) RID=$2; shift 2;;
  --model) MODEL=$2; shift 2;; --deadline-ms) DEADLINE=$2; shift 2;; --settings) SETTINGS=$2; shift 2;;
  --turn-p90) TURN=$2; shift 2;; --print-cmd) PRINT=1; shift;; *) echo "unknown arg $1" >&2; exit 2;; esac; done
OUT=$PKGDIR/reviews; mkdir -p "$OUT"
CAND_SB=$SB/cand/candidate.md; SRC_SB=$SB/cand/source.md
SHA=$(sha256sum "$CAND_SB" | cut -d' ' -f1); SRC_SHA=$(sha256sum "$SRC_SB" | cut -d' ' -f1)
T=$(cat "$R2_HOME/config/brief-a1.tmpl")
T=${T//\{CAND\}/$CAND_SB}; T=${T//\{SHA\}/$SHA}; T=${T//\{SRC\}/$SRC_SB}; T=${T//\{SRC_SHA\}/$SRC_SHA}
BRIEF=$T
rem_s() { awk -v d="$DEADLINE" -v n="$(now_ms)" 'BEGIN{r=(d-n)/1000; if (r<0) r=0; printf "%.3f", r}'; }
rem_ms() { echo $(( DEADLINE - $(now_ms) )); }
argv_for() { # $1 = attempt; fills ARGV
  ARGV=(timeout "$(rem_s)" claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit)
  if [ "$1" = 1 ] && [ -n "$SETTINGS" ]; then ARGV+=(--settings "$SETTINGS"); fi
}
if [ $PRINT = 1 ]; then
  argv_for 1
  printf '%s\0' cd "$SB/repo" '&&' "${ARGV[@]}" '<<<' "$BRIEF" | jq -cRs 'split("\u0000")[:-1]'
  exit 0
fi

MODEL_OK=false; BLOCK_OK=false; APIERR=false
run_attempt() { # RR:46-60 with sandbox cwd, deadline timeout, session id and timing added
  local attempt=$1 S E RC OBS TOK TOKALL SID LOWOBS LOWEXP HANG=false SET=false ISO=false
  argv_for "$attempt"
  S=$(now_ms)
  ( cd "$SB/repo" && "${ARGV[@]}" <<<"$BRIEF" ) >"$OUT/$RID.attempt$attempt.json" 2>"$OUT/$RID.attempt$attempt.err"
  RC=$?; E=$(now_ms)
  [ "$attempt" = 1 ] && : > "$OUT/$RID.attempt1.exit"
  [ $RC = 124 ] && HANG=true
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$OUT/$RID.attempt$attempt.json" > "$OUT/$RID.attempt$attempt.md" 2>/dev/null
  OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$OUT/$RID.attempt$attempt.json" 2>/dev/null)
  TOK=$(jq '[.[]|select(.type=="result")|.usage.output_tokens]|.[0] // 0' "$OUT/$RID.attempt$attempt.json" 2>/dev/null)
  TOKALL=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$OUT/$RID.attempt$attempt.json" 2>/dev/null)
  SID=$(jq -r '[.[]|select(.type=="result")|.session_id][0] // ""' "$OUT/$RID.attempt$attempt.json" 2>/dev/null)
  APIERR=false; grep -q 'API Error' "$OUT/$RID.attempt$attempt.md" 2>/dev/null && APIERR=true
  LOWOBS=$(echo "$OBS" | tr 'A-Z' 'a-z'); LOWEXP=$(echo "$MODEL" | tr 'A-Z' 'a-z')
  MODEL_OK=false; [ -n "$OBS" ] && [ "$OBS" != "<synthetic>" ] && { [ "$LOWOBS" = "$LOWEXP" ] || [ "$LOWOBS" = "$LOWEXP-build" ]; } && MODEL_OK=true
  BLOCK_OK=false; grep -q '^```findings-v1' "$OUT/$RID.attempt$attempt.md" && BLOCK_OK=true
  { [ "$attempt" = 1 ] && [ -n "$SETTINGS" ]; } && SET=true
  [ "$attempt" = 2 ] && ISO=true
  jq -n --arg rid "$RID" --arg exp "$MODEL" --arg obs "$OBS" --argjson mok $MODEL_OK --argjson bok $BLOCK_OK \
    --argjson att "$attempt" --argjson w $(( (E - S) / 1000 )) --argjson tok "${TOK:-0}" --argjson tokall "${TOKALL:-0}" \
    --argjson rc $RC --arg sid "$SID" --argjson s "$S" --argjson e "$E" --argjson hang $HANG --argjson set $SET \
    --argjson iso $ISO --argjson apierr $APIERR \
    '{reviewer_id:$rid,expected_model:$exp,observed_model:$obs,model_ok:$mok,findings_block:$bok,attempt:$att,wall_s:$w,
      output_tokens_main:$tok,output_tokens_all:$tokall,exit:$rc,session_id:$sid,start_ms:$s,end_ms:$e,hang_kill:$hang,
      settings:$set,retry_isolated:$iso,api_error:$apierr}' > "$OUT/$RID.attempt$attempt.meta.json"
  $MODEL_OK && $BLOCK_OK && ! $APIERR
}
attempt=0; SKIP2=false
while [ $attempt -lt 2 ]; do
  if [ $attempt = 1 ] && [ "$(rem_ms)" -lt 10000 ]; then SKIP2=true; break; fi   # R-44: no attempt 2 with under 10 s left
  attempt=$((attempt + 1))
  if run_attempt $attempt; then break; fi
done
cp "$OUT/$RID.attempt$attempt.md" "$OUT/$RID.md"; cp "$OUT/$RID.attempt$attempt.meta.json" "$OUT/$RID.meta.json"

# H2 (R-02): normalise, validate with the real parser, one re-ask under the same hang deadline
H2() { $PY "$R2_HOME/py/h2_normalize.py" --report "$OUT/$RID.md" --out "$OUT/$RID.norm.md" --json "$OUT/$RID.h2.json" >/dev/null; }
H2
SID=$(jq -r .session_id "$OUT/$RID.meta.json")
REASK_S=0; REASK_TOK=0; REASK=false; REASK_OK=null; REASK_HANG=false; REASK_SKIP=false; REASK_END=0
if [ "$(jq -r .needs_reask "$OUT/$RID.h2.json")" = true ] && $MODEL_OK && [ -n "$SID" ]; then
  NEED=$(awk -v t="$TURN" 'BEGIN{printf "%d", (6 + t) * 1000}')
  if [ "$(rem_ms)" -ge "$NEED" ]; then
    REASK=true
    ERRS=$(jq -r '.errors[]|"line \(.line): \(.msg)"' "$OUT/$RID.h2.json")
    PROMPT="Your findings block has these problems: $ERRS. Reply with the complete report again, with the same findings, changing only what these errors require."
    RS=$(now_ms)
    ( cd "$SB/repo" && timeout "$(rem_s)" claude -p --resume "$SID" --model "$MODEL" --output-format stream-json --verbose --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"$PROMPT" ) >"$OUT/$RID.reask.jsonl" 2>"$OUT/$RID.reask.err"
    RRC=$?; REASK_END=$(now_ms); REASK_S=$(awk -v a="$RS" -v b="$REASK_END" 'BEGIN{printf "%.3f", (b-a)/1000}')
    [ $RRC = 124 ] && REASK_HANG=true
    ROBS=$(jq -rs '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$OUT/$RID.reask.jsonl" 2>/dev/null)
    REASK_TOK=$(jq -s '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$OUT/$RID.reask.jsonl" 2>/dev/null || echo 0)
    RTEXT=$(jq -rs '[.[]|select(.type=="result")|.result][0] // ""' "$OUT/$RID.reask.jsonl" 2>/dev/null)
    LROBS=$(echo "$ROBS" | tr 'A-Z' 'a-z'); LEXP=$(echo "$MODEL" | tr 'A-Z' 'a-z')
    REASK_OK=false
    [ -n "$ROBS" ] && { [ "$LROBS" = "$LEXP" ] || [ "$LROBS" = "$LEXP-build" ]; } && REASK_OK=true
    if $REASK_OK && [ -n "$RTEXT" ]; then
      cp "$OUT/$RID.md" "$OUT/$RID.pre-reask.md"; printf '%s\n' "$RTEXT" > "$OUT/$RID.md"; H2
    fi
  else
    REASK_SKIP=true
  fi
fi
DROPPED=$(jq '[.errors[]|select(.line > 0)]|length' "$OUT/$RID.h2.json")
BFOUND=$(jq -r .block_found "$OUT/$RID.h2.json")
jq --argjson reask $REASK --argjson rs "$REASK_S" --argjson rtok "${REASK_TOK:-0}" --argjson rok "$REASK_OK" \
   --argjson rhang $REASK_HANG --argjson rskip $REASK_SKIP --argjson rend "$REASK_END" --argjson dropped "$DROPPED" \
   --argjson skip2 $SKIP2 --argjson attempts "$attempt" --argjson bfound "$BFOUND" --slurpfile h2 "$OUT/$RID.h2.json" '
  . + {reask:$reask, reask_s:$rs, reask_output_tokens:$rtok, reask_model_ok:$rok, reask_skipped_deadline:$rskip,
       dropped_lines:$dropped, retry_skipped_deadline:$skip2, attempts:$attempts, block_found:$bfound,
       h2_truncated:$h2[0].truncated, end_ms:([.end_ms, $rend]|max), hang_kill:(.hang_kill or $rhang)}
  | .slo_breach = .hang_kill' "$OUT/$RID.meta.json" > "$OUT/$RID.meta.json.tmp" && mv "$OUT/$RID.meta.json.tmp" "$OUT/$RID.meta.json"
jq -s --argjson rs "$REASK_S" --argjson rtok "${REASK_TOK:-0}" \
  '{attempts:length,total_wall_s:(map(.wall_s)|add),total_output_tokens_all:((map(.output_tokens_all)|add) + $rtok),
    reask_s:$rs,reask_output_tokens:$rtok,retry_s:((.[1:]|map(.wall_s)|add) // 0)}' "$OUT/$RID".attempt*.meta.json > "$OUT/$RID.cost.json"
$MODEL_OK && [ "$BFOUND" = true ]
