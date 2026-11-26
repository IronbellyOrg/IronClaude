#!/usr/bin/env bash
# usage: run-schedule.sh SCHEDULE.tsv [--max-panels N] [--values FILE]   (DESIGN 9.5, REQ-29, REQ-32)
# Runs the rows of a schedule written by bin/make-schedule.py through bin/run-panel.sh, block by block in file order.
# Each row is one `run-panel.sh --arm A --panel P --doc D --replicate R --block B --seed S --run-id <run>`; the run
# folder is RUN_ROOT/<run>, where RUN_ROOT is RL_RUNS_ROOT (default RL/runs; under RL or /tmp). A run folder that
# already holds a run.json is skipped: a counted run is never repeated, so a stopped schedule is resumed by running it again.
#   --max-panels N   panels at once, 1 to 3 (default 1). A panel is 3 reviewer sessions, so the default keeps at most
#                    3 alive and 3 panels reach 9. The gateway is untested above about 10 sessions across all builds, so
#                    raise N only while the sibling's schedule is idle (DESIGN 9.5, 13.1 item 10).
#   --values FILE    a values file instead of config/values.json (a test hook, accepted only under /tmp/)
# The spike record: the script refuses to start (exit 2, E_NO_SPIKE) unless the values file holds `spike.runs` of at
# least 5 and a numeric `spike.c_luna` above 0 (REQ-32, bin/run-spike.sh timing writes it). Every RL run is then given
# the cap lens_row_cap(b_min, c_luna) through `--b-min` and `--c-luna` of run-panel.sh, with b_min the smallest b of
# the row's panel in the values file (DR-4): c_luna 2.41 gives 12 rows at b = 100, 2.50 gives 11.
# Environment: NOFALLBACK=1 is required (DD-8); the fake claude is first on PATH in every test of this build.
# Written files: RUN_ROOT/schedule-run.json (the summary) and RUN_ROOT/schedule-run.log (the output of every run-panel.sh call).
# Exit: 0 every row ran or was skipped (a row refused with no_budget, exit 3 of run-panel.sh, is listed in the summary
# under no_budget: the schedule excludes RL on that panel, DESIGN 8 row 4); 1 some run-panel.sh call failed (the rest
# still ran); 2 refused before any run started (no spike record, bad argument, unreadable schedule, NOFALLBACK not 1).
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=rl-env.sh
source "$HERE/rl-env.sh"
# shellcheck source=common.sh
source "$HERE/common.sh"

usage() {
  sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
[ $# -ge 1 ] && [ "${1#--}" = "$1" ] || usage
SCHED=$1
shift
JOBS=1 VALUES=
while [ $# -gt 0 ]; do
  [ $# -ge 2 ] || usage
  case "$1" in
    --max-panels) JOBS=$2 ;;
    --values) VALUES=$2 ;;
    *) usage ;;
  esac
  shift 2
done
sw_assert_nofallback || exit 2
[ -f "$SCHED" ] || { echo "E_ARG: no schedule file $SCHED" >&2; exit 2; }
[[ $JOBS =~ ^[1-3]$ ]] || { echo "E_JOBS: --max-panels is 1, 2 or 3 (at most 3 panels = 9 reviewer sessions at once)" >&2; exit 2; }
if [ -n "$VALUES" ]; then
  case "$(realpath -m -- "$VALUES")/" in /tmp/?*) ;; *) echo "E_OVERRIDE: $VALUES is outside /tmp/" >&2; exit 2 ;; esac
fi
if [ "$(sed -n '2p' "$SCHED")" != $'stage\tblock\tarm\tpanel\tdoc\treplicate\tseed\tset\trun' ]; then
  echo "E_ARG: $SCHED is not a schedule file of bin/make-schedule.py" >&2
  exit 2
fi
ROOT=${RL_RUNS_ROOT:-$SW/runs}
sw_assert_writable "$ROOT" || exit 2

# The spike record comes first: nothing starts and nothing is written without it (REQ-32).
VALS=${VALUES:-$SW/config/values.json}
[ -f "$VALS" ] || { echo "E_ARG: no values file $VALS" >&2; exit 2; }
CLUNA=$(jq -r 'if (.spike | type) == "object" and (.spike.runs | type) == "number" and .spike.runs >= 5
  and (.spike.c_luna | type) == "number" and .spike.c_luna > 0 then .spike.c_luna else empty end' "$VALS" 2>/dev/null)
if [ -z "$CLUNA" ]; then
  echo "E_NO_SPIKE: $VALS has no spike record of 5 runs with a c_luna (bin/run-spike.sh timing); no arm starts without it (REQ-32)" >&2
  exit 2
fi
mkdir -p "$ROOT" || exit 2
LOG=$ROOT/schedule-run.log
RCDIR=$(mktemp -d /tmp/rl-run-schedule.XXXXXXXX) || exit 2
trap 'rm -rf -- "$RCDIR"' EXIT
STARTED=() SKIPPED=() MAXC=0

fresh_sandbox() { # fresh_sandbox DOC: with one panel at a time, rebuild a sandbox that holds leftovers (uv.lock, .venv) of the previous run
  local doc=$1 sbx
  [ "$JOBS" = 1 ] || return 0
  sbx="${SW_SB_ROOT:-/tmp/evalsb-recipe}/$doc"
  [ -d "$sbx/repo/.git" ] || return 0
  [ -n "$(git -C "$sbx/repo" status --porcelain --ignored)" ] || return 0
  case "$(realpath -m -- "$sbx")/" in /tmp/evalsb-recipe/?*) ;; *) echo "E_SANDBOX: refusing to rebuild $sbx" >&2; return 2 ;; esac
  echo "REBUILD sandbox $doc (leftovers: $(git -C "$sbx/repo" status --porcelain --ignored | head -3 | tr '\n' ' '))" >>"$LOG"
  rm -rf -- "$sbx" && bash "$HERE/build-sandbox.sh" "$doc" >>"$LOG" 2>&1
}

launch() { # launch STAGE BLOCK ARM PANEL DOC REP SEED RUN: one run-panel.sh call in the background; its exit code goes to $RCDIR/<run>
  local arm=$3 panel=$4 bmin args
  fresh_sandbox "$5" || { echo 2 >"$RCDIR/$8"; return 0; }
  args=(--arm "$arm" --panel "$panel" --doc "$5" --replicate "$6" --block "$2" --seed "$7" --run-id "$8")
  if [ "$arm" = RL ]; then
    bmin=$(jq -r --arg p "$panel" '[.b[$p][]] | min // empty' "$VALS")
    args+=(--b-min "$bmin" --c-luna "$CLUNA")
  fi
  (
    bash "$HERE/run-panel.sh" "${args[@]}" >>"$LOG" 2>&1
    echo $? >"$RCDIR/$8"
  ) &
}

while IFS=$'\t' read -r stage block arm panel doc rep seed _set run; do
  [ -n "$run" ] || continue
  if [ -e "$ROOT/$run/run.json" ]; then
    SKIPPED+=("$run")
    echo "SKIP $run (run.json exists)" >>"$LOG"
    continue
  fi
  while [ "$(jobs -rp | wc -l)" -ge "$JOBS" ]; do wait -n || true; done
  conc=$(($(jobs -rp | wc -l) + 1))
  [ "$conc" -le "$MAXC" ] || MAXC=$conc
  echo "START $run concurrent=$conc" >>"$LOG"
  launch "$stage" "$block" "$arm" "$panel" "$doc" "$rep" "$seed" "$run"
  STARTED+=("$run")
done < <(tail -n +3 "$SCHED")
wait

FAILED=() NOBUDGET=()
for run in ${STARTED[@]+"${STARTED[@]}"}; do
  rc=$(cat "$RCDIR/$run" 2>/dev/null || echo missing)
  case $rc in
    0) ;;
    3) NOBUDGET+=("$run") ;;
    *) FAILED+=("$run:$rc") ;;
  esac
done
tojson() { printf '%s\n' "$@" | jq -R 'select(length>0)' | jq -sc .; }
jq -n --arg sched "$SCHED" --argjson started "$(tojson ${STARTED[@]+"${STARTED[@]}"})" \
  --argjson skipped "$(tojson ${SKIPPED[@]+"${SKIPPED[@]}"})" --argjson failed "$(tojson ${FAILED[@]+"${FAILED[@]}"})" \
  --argjson nobudget "$(tojson ${NOBUDGET[@]+"${NOBUDGET[@]}"})" --argjson maxc "$MAXC" --argjson jobs "$JOBS" \
  --argjson c_luna "$CLUNA" \
  '{schedule:$sched, started:$started, skipped:$skipped, failed:$failed, no_budget:$nobudget, max_concurrent:$maxc,
    max_panels:$jobs, c_luna:$c_luna}' >"$ROOT/schedule-run.json"
echo "SCHEDULE started=${#STARTED[@]} skipped=${#SKIPPED[@]} failed=${#FAILED[@]} no_budget=${#NOBUDGET[@]} max_concurrent=$MAXC c_luna=$CLUNA"
[ ${#FAILED[@]} -eq 0 ] || exit 1
exit 0
