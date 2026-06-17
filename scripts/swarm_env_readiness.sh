#!/usr/bin/env bash
# OPS-002 / T09.02 (roadmap R-151) — MultiModelSwarm environment readiness preflight.
#
# Companion to docs/swarm/env-readiness.md. Asserts every prerequisite in that
# doc's §1 checklist BEFORE the first `superclaude swarm run` on a fresh,
# non-Anthropic T2 proxy host:
#
#   1. Python  >= 3.10        (required — fail)
#   2. UV present             (required — fail)
#   3. httpx importable       (required — fail)
#   4. Click importable       (required — fail)
#   5. Rich  importable       (required — fail)
#   6. tmux present           (optional — WARN only, never fail)
#   7. T2 proxy env vars      (required — fail): T2ProxyUrl, T2ProxyKey,
#                              and >= 1 of T2Model01..T2Model09.
#
# Exits NON-ZERO if any REQUIRED check fails, mirroring the INV-007 env-missing
# failure path (docs/swarm/env-readiness.md §3): the missing T2 contract is
# enumerated verbatim so the operator can fix it in one pass. tmux absence is a
# warning only — the default inline pipeline runs without it.
#
# This surface speaks ONLY to the OpenAI-compatible T2 proxy. No Anthropic /
# native host-vendor credential is read, required, or accepted.
set -euo pipefail

# --- presentation helpers (portable; no color dependency) --------------------
PASS='[ OK ]'
FAIL='[FAIL]'
WARN='[WARN]'

failures=0
warnings=0

ok()   { printf '%s %s\n' "$PASS" "$1"; }
bad()  { printf '%s %s\n' "$FAIL" "$1"; failures=$((failures + 1)); }
warn() { printf '%s %s\n' "$WARN" "$1"; warnings=$((warnings + 1)); }

# T2 model slot bound — matches T2_MODEL_MAX_SLOTS = 9 (config.py / doc §2).
T2_MODEL_MAX_SLOTS=9
T2_MODEL_ENV_PREFIX='T2Model0'

printf '== MultiModelSwarm environment readiness ==\n'
printf '   (OPS-002 preflight — see docs/swarm/env-readiness.md)\n\n'

# --- 1. Python >= 3.10 -------------------------------------------------------
python_bin=''
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1; then
    python_bin="$cand"
    break
  fi
done

if [ -z "$python_bin" ]; then
  bad "Python: no python3/python interpreter found on PATH (need >= 3.10)."
else
  py_version="$("$python_bin" -c 'import sys; print("%d.%d" % sys.version_info[:2])' 2>/dev/null || echo '?')"
  if "$python_bin" -c 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3, 10) else 1)' >/dev/null 2>&1; then
    ok "Python $py_version (>= 3.10) via '$python_bin'."
  else
    bad "Python $py_version is too old; need >= 3.10. Install a newer interpreter."
  fi
fi

# --- 2. UV present -----------------------------------------------------------
if command -v uv >/dev/null 2>&1; then
  uv_version="$(uv --version 2>/dev/null || echo 'unknown')"
  ok "UV present ($uv_version)."
else
  bad "UV not found on PATH. Install UV — every Python op runs via 'uv run …'. See https://docs.astral.sh/uv/."
fi

# --- 3-5. Required Python deps (httpx / Click / Rich) ------------------------
# Prefer `uv run` (the project's standard invocation); fall back to the bare
# interpreter if UV is absent so the dep diagnostics are still actionable.
check_dep() {
  module="$1"
  label="$2"
  if command -v uv >/dev/null 2>&1; then
    if uv run python -c "import $module" >/dev/null 2>&1; then
      ok "$label importable ('uv run python -c \"import $module\"')."
      return
    fi
  fi
  if [ -n "$python_bin" ] && "$python_bin" -c "import $module" >/dev/null 2>&1; then
    ok "$label importable (via '$python_bin')."
    return
  fi
  bad "$label not importable. Install project deps (e.g. 'make dev' / 'uv pip install $module')."
}

check_dep httpx httpx
check_dep click Click
check_dep rich Rich

# --- 6. tmux (optional — WARN only) ------------------------------------------
if command -v tmux >/dev/null 2>&1; then
  ok "tmux present (enables 'swarm run --detached')."
else
  warn "tmux not found — OPTIONAL. The default inline 'swarm run' works without it; only '--detached' requires tmux."
fi

# --- 7. T2 proxy env contract -----------------------------------------------
# Mirrors read_env()/TransportEnvError: collect every missing mandatory name in
# one pass (T2ProxyUrl, T2ProxyKey, and >= 1 T2Model01..T2Model09 slot).
missing=''
add_missing() {
  if [ -z "$missing" ]; then
    missing="$1"
  else
    missing="$missing, $1"
  fi
}

# Whitespace-only values are treated as absent (doc §2 slot semantics).
url_val="$(printf '%s' "${T2ProxyUrl-}" | tr -d '[:space:]')"
key_val="$(printf '%s' "${T2ProxyKey-}" | tr -d '[:space:]')"

if [ -z "$url_val" ]; then
  add_missing T2ProxyUrl
fi
if [ -z "$key_val" ]; then
  add_missing T2ProxyKey
fi

# Probe T2Model01..T2Model0<MAX>; count any non-whitespace-only slot.
resolved_slots=0
slot=1
while [ "$slot" -le "$T2_MODEL_MAX_SLOTS" ]; do
  var_name="${T2_MODEL_ENV_PREFIX}${slot}"
  # Indirect expansion (portable in bash).
  slot_raw="${!var_name-}"
  slot_val="$(printf '%s' "$slot_raw" | tr -d '[:space:]')"
  if [ -n "$slot_val" ]; then
    resolved_slots=$((resolved_slots + 1))
  fi
  slot=$((slot + 1))
done

if [ "$resolved_slots" -eq 0 ]; then
  add_missing "${T2_MODEL_ENV_PREFIX}1..${T2_MODEL_ENV_PREFIX}${T2_MODEL_MAX_SLOTS}"
fi

if [ -z "$missing" ]; then
  ok "T2 proxy env contract complete (T2ProxyUrl, T2ProxyKey, $resolved_slots model slot(s))."
else
  bad "T2 proxy env contract incomplete; missing: ${missing}. Set T2ProxyUrl, T2ProxyKey, and at least one ${T2_MODEL_ENV_PREFIX}1..${T2_MODEL_MAX_SLOTS} slot."
fi

# --- summary + exit ----------------------------------------------------------
printf '\n-- summary --\n'
printf '   warnings: %d   failures: %d\n' "$warnings" "$failures"

if [ "$failures" -gt 0 ]; then
  printf '%s environment NOT ready — resolve the %d failure(s) above before running the swarm.\n' "$FAIL" "$failures"
  exit 1
fi

printf '%s environment ready for swarm run.\n' "$PASS"
if [ "$warnings" -gt 0 ]; then
  printf '   (%d optional warning(s) — non-blocking.)\n' "$warnings"
fi
exit 0
