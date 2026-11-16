#!/usr/bin/env bash
# usage: run-spike.sh {timing|compliance} --go --doc DOC [--panel primary] [--runs N] [--baseline-runs N] [--values FILE]
#                     (DESIGN 12.4, REQ-17, REQ-32)
# The two spikes that come before every arm. They start models, so each mode refuses to run without an explicit --go
# (the owner's go-ahead): without it the script prints that it needs models and exits 2 having started nothing. This build
# never runs either mode; the tests only run the refusal. One panel at a time, through bin/run-panel.sh. The sandbox of
# DOC must exist (bin/build-sandbox.sh DOC). NOFALLBACK=1 is required (DD-8).
#
#   timing      N RL runs (--runs, default 5) and N Z0 runs (--baseline-runs, default 5) of the primary panel on DOC, block
#               k holding RL run k and Z0 run k (the same day). From the wall seconds of luna 1 (the first luna of the lens
#               table) it computes
#                 c_luna = (median(luna 1 in the RL runs) - median(luna 1 in the Z0 runs) - 4) / mean rows luna 1 wrote
#               and writes the record `spike` = {runs, baseline_runs, c_luna, median_rl_s, median_z0_s, mean_rows, ...}
#               into the values file (config/values.json, or --values). The RL runs use the planning cap of 14 rows.
#               Run folders: RUN_ROOT/spike-timing/timing-{rl,z0}-<k>. bin/run-schedule.sh refuses without this record.
#   compliance  N RL panel runs (--runs, default 5; 15 reviewer runs) on DOC, then
#               `analysis/analyze.py compliance --runs RUN_ROOT/spike-compliance`: the ledger_missing rate, recipe_missing,
#               quote validity, format errors and none_found per class. Exit 0 when ledger_missing is at most 10% (go),
#               1 when it is not. Run folders: RUN_ROOT/spike-compliance/compliance-<k>; the numbers go to compliance.json.
#
# RUN_ROOT is RL_RUNS_ROOT (default RL/runs; under RL or /tmp). --values is a test hook (accepted only under /tmp/).
# Exit: 0 done (and go); 1 compliance no-go, a run failed, or the timing record could not be computed; 2 refused (no
# --go, bad argument, NOFALLBACK not 1).
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=rl-env.sh
source "$HERE/rl-env.sh"
# shellcheck source=common.sh
source "$HERE/common.sh"

help() { sed -n '2,/^set -u/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; }
usage() {
  sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
case "${1:-}" in -h | --help) help; exit 0 ;; esac
MODE=${1:-}
case "$MODE" in timing | compliance) shift ;; *) usage ;; esac
GO=0 PANEL=primary DOC= RUNS=5 BASE_RUNS=5 VALUES=
while [ $# -gt 0 ]; do
  case "$1" in
    -h | --help) help; exit 0 ;;
    --go) GO=1; shift; continue ;;
  esac
  [ $# -ge 2 ] || usage
  case "$1" in
    --panel) PANEL=$2 ;;
    --doc) DOC=$2 ;;
    --runs) RUNS=$2 ;;
    --baseline-runs) BASE_RUNS=$2 ;;
    --values) VALUES=$2 ;;
    *) usage ;;
  esac
  shift 2
done
if [ "$GO" != 1 ]; then
  echo "run-spike.sh $MODE needs models (the spike starts real reviewer sessions); it started nothing." >&2
  echo "Run it again with --go only with the owner's go-ahead. See --help." >&2
  exit 2
fi
[ "$PANEL" = primary ] || { echo "E_ARG: --panel is primary (the spikes measure luna, which the primary panel holds)" >&2; exit 2; }
[[ $DOC =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || { echo "E_DOC: bad document id: $DOC" >&2; exit 2; }
for v in RUNS BASE_RUNS; do [[ ${!v} =~ ^[1-9][0-9]*$ ]] || { echo "E_ARG: $v is not a positive number" >&2; exit 2; }; done
if [ -n "$VALUES" ]; then
  case "$(realpath -m -- "$VALUES")/" in /tmp/?*) ;; *) echo "E_OVERRIDE: $VALUES is outside /tmp/" >&2; exit 2 ;; esac
fi
sw_assert_nofallback || exit 2
BASE=${RL_RUNS_ROOT:-$SW/runs}
sw_assert_writable "$BASE" || exit 2
VALS=${VALUES:-$SW/config/values.json}
[ -f "$VALS" ] || { echo "E_ARG: no values file $VALS" >&2; exit 2; }

fresh_sandbox() { # one panel at a time here, so a sandbox a reviewer left dirty (e.g. `uv run` writes uv.lock) can be rebuilt between runs
  local sbx="$SW_SB_ROOT/$DOC"
  if [ -d "$sbx/repo/.git" ] && [ -n "$(git -C "$sbx/repo" status --porcelain --ignored)" ]; then
    echo "sandbox of $DOC was left dirty by the previous run ($(git -C "$sbx/repo" status --porcelain --ignored | head -3 | tr '\n' ' ')); rebuilding it" >&2
    case "$(realpath -m -- "$sbx")/" in /tmp/evalsb-recipe/?*) ;; *) echo "E_SANDBOX: refusing to rebuild $sbx" >&2; return 2 ;; esac
    rm -rf -- "$sbx" && bash "$HERE/build-sandbox.sh" "$DOC" > /dev/null
  fi
}

panel_run() { # panel_run SUBDIR ARM RUN-ID K: one run of the spike, block K, into BASE/SUBDIR/RUN-ID
  fresh_sandbox || return 2
  RL_RUNS_ROOT=$BASE/$1 bash "$HERE/run-panel.sh" --arm "$2" --panel "$PANEL" --doc "$DOC" --replicate "$4" --block "$4" \
    --seed 1 --run-id "$3"
}

FAILED=0
if [ "$MODE" = timing ]; then
  OUT=$BASE/spike-timing
  mkdir -p "$OUT" || exit 2
  LUNA=$(jq -r '[.panels.primary.roles[] | select(.model == "gpt-6-luna") | .rid][0] // empty' "$SW/config/lenses.json")
  [ -n "$LUNA" ] || { echo "E_ARG: no luna reviewer in the primary panel of config/lenses.json" >&2; exit 2; }
  N=$((RUNS > BASE_RUNS ? RUNS : BASE_RUNS))
  RL_DIRS=() Z0_DIRS=()
  for k in $(seq 1 "$N"); do
    if [ "$k" -le "$RUNS" ]; then
      panel_run spike-timing RL "timing-rl-$k" "$k" || FAILED=1
      [ -f "$OUT/timing-rl-$k/run.json" ] && RL_DIRS+=(--rl-run "$OUT/timing-rl-$k")
    fi
    if [ "$k" -le "$BASE_RUNS" ]; then
      panel_run spike-timing Z0 "timing-z0-$k" "$k" || FAILED=1
      [ -f "$OUT/timing-z0-$k/run.json" ] && Z0_DIRS+=(--z0-run "$OUT/timing-z0-$k")
    fi
  done
  sw_py "$HERE/../rl/spike.py" timing --values "$VALS" --rid "$LUNA" --doc "$DOC" --panel "$PANEL" \
    ${RL_DIRS[@]+"${RL_DIRS[@]}"} ${Z0_DIRS[@]+"${Z0_DIRS[@]}"} || exit 1
  [ "$FAILED" = 0 ] || exit 1
  exit 0
fi

OUT=$BASE/spike-compliance
mkdir -p "$OUT" || exit 2
for k in $(seq 1 "$RUNS"); do
  panel_run spike-compliance RL "compliance-$k" "$k" || FAILED=1
done
sw_py "$HERE/../analysis/analyze.py" compliance --runs "$OUT" --out "$OUT/compliance.json" || exit 1
[ "$FAILED" = 0 ] || exit 1
exit 0
