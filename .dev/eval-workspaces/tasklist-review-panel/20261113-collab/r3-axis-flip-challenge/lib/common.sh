#!/usr/bin/env bash
# Sourced by every shell file of the R3 harness (section 2.1).
R3=${R3:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)}
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
EVAL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
SB=${R3_SB_ROOT:-/tmp/evalsb-collab-r3}
RUNS_ROOT=${R3_RUNS_ROOT:-$R3/runs}
SCORING_ROOT=${R3_SCORING_ROOT:-$R3/scoring}
RESULTS_ROOT=${R3_RESULTS_ROOT:-$R3/results}
CLAUDE_PROJECTS=${R3_CLAUDE_PROJECTS:-$HOME/.claude/projects}
export PYTHONDONTWRITEBYTECODE=1
export SUPERCLAUDE_CODEGRAPH_AUTOINIT=0
ALLOWED_MODELS="muse-ember-1.0 gpt-6-luna claude-haiku-5-5 claude-sonnet-5-5 grok-4.7"

r3_now() { date +%s.%3N; }

# Refuse any output path outside R3, SB or a /tmp test override root (K1).
r3_assert_writable() {
  local p rp root
  p=$1
  rp=$(realpath -m -- "$p") || return 1
  for v in R3_RUNS_ROOT R3_SB_ROOT R3_SCORING_ROOT R3_RESULTS_ROOT R3_VALUES_FILE R3_CLAUDE_PROJECTS; do
    root=${!v:-}
    [ -z "$root" ] && continue
    root=$(realpath -m -- "$root")
    case "$root/" in /tmp/*) ;; *) echo "E_OVERRIDE: $v=$root is outside /tmp/" >&2; return 1;; esac
    case "$rp/" in "$root"/*) return 0;; esac
  done
  for root in "$(realpath -m -- "$R3")" "$(realpath -m -- "$SB")"; do
    case "$rp/" in "$root"/*) return 0;; esac
  done
  echo "E_NOT_WRITABLE: $p (resolves to $rp)" >&2
  return 1
}

r3_assert_model() {
  local m=$1
  [ -n "$m" ] || { echo "E_MODEL: empty model id" >&2; return 1; }
  case " $ALLOWED_MODELS " in *" $m "*) return 0;; esac
  echo "E_MODEL: $m is not an allowed reviewer model" >&2
  return 1
}

r3_assert_nofallback() {
  [ "${NOFALLBACK:-}" = "1" ] || { echo "E_NOFALLBACK: NOFALLBACK=1 is required" >&2; return 1; }
}

r3_py() { uv run --frozen --project "$REPO" python "$R3/r3lib/cli.py" "$@"; }

# r3_event <pkgdir> <rid> <ev> [jq-args...]: append one JSON line to board/events.jsonl under flock.
r3_event() {
  local pd=$1 rid=$2 ev=$3; shift 3
  mkdir -p "$pd/board"
  local line
  line=$(jq -nc --argjson t "$(r3_now)" --arg rid "$rid" --arg ev "$ev" "$@" '{t:$t,rid:$rid,ev:$ev} + ($ARGS.named|del(.t,.rid,.ev))')
  ( flock 9; printf '%s\n' "$line" >> "$pd/board/events.jsonl" ) 9>>"$pd/board/events.lock"
}

# float arithmetic helper
r3_calc() { awk "BEGIN{printf \"%.3f\", $*}"; }

# Admission (13.3). r3_admission_ok <ember reviewers in this panel>: 0 when total+3<=10 and ember+here<=4.
r3_admission_ok() {
  local tot emb
  tot=$(pgrep -fc '^timeout .* claude -p --model ' || true); emb=$(pgrep -fc '^timeout .* claude -p --model muse-ember-1.0 ' || true)
  ADMIT_TOTAL=${tot:-0}; ADMIT_EMBER=${emb:-0}
  [ $((ADMIT_TOTAL + 3)) -le 10 ] && [ $((ADMIT_EMBER + $1)) -le 4 ]
}
# r3_admit <lockfile> <ember here> [max tries]: takes the lock on fd 8 and returns holding it once admitted.
# With max tries reached it returns 1 with the lock released.
r3_admit() {
  local lock=$1 here=$2 max=${3:-0} n=0
  exec 8>>"$lock"
  while :; do
    flock 8
    r3_admission_ok "$here" && return 0
    flock -u 8
    n=$((n+1)); [ "$max" -gt 0 ] && [ $n -ge "$max" ] && return 1
    sleep 5
  done
}
