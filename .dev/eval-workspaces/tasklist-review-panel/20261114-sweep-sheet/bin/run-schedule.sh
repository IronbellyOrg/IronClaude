#!/usr/bin/env bash
# run-schedule.sh SCHEDULE.tsv [--runs-root DIR] [--values FILE] [--packages FILE] [--jobs N]   (DESIGN 11.6, REQ-32, REQ-29)
# Runs the rows of a schedule written by bin/make-schedule.py through bin/run-panel.sh, at most 3 panels at once (so at most
# 9 reviewer sessions and 3 ember sessions), block by block in file order. Each run is `bin/run-panel.sh --arm A --panel P
# --doc D --run <root>/<run> --seed S --replicate R --block B --concurrent N`, where N is the number of panels running when
# that one started (`concurrent_panels_at_start` in its run.json). A run folder that already holds a run.json is skipped: a
# counted run is never repeated, so a stopped schedule is resumed by running it again.
#   --runs-root DIR   the run folders go here (default SW/runs/stage<stage> of each row); under SW or /tmp (K1)
#   --values FILE     a values file instead of config/values.json (a test hook, accepted only under /tmp/)
#   --packages FILE   passed to run-panel.sh (a test hook, accepted only under /tmp/)
#   --jobs N          panels at once, 1 to 3 (default 3)
# The spike record: the script refuses to start (exit 2, E_NO_SPIKE) unless the values file holds `spike.runs` of at least 5
# and a numeric `spike.c_luna` (REQ-32). When c_luna is above the break-even seconds per item at b = 100 (2.75 s) every run
# uses the fallback caps: each luna takes 6 items, the search reviewer 12. The caps are written to a copy of config/panels.json
# (<root>/panels-in-use.json) that the runs read through SW_PANELS; config/panels.json itself is never changed.
# Environment: NOFALLBACK=1 is required (DD-8). Written files: <root>/schedule-run.json (the summary) and
# <root>/schedule-run.log (the output of every run-panel.sh call), where <root> is --runs-root or SW/runs.
# Exit: 0 every row ran or was skipped; 1 some run-panel.sh call exited non-zero (the rest still ran); 2 refused before any
# run started (no spike record, bad argument, unreadable schedule).
set -u -o pipefail
source "$(dirname "$0")/common.sh"

usage() {
  sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
SCHED=${1:-}
[ -n "$SCHED" ] && [ "${SCHED#--}" = "$SCHED" ] || usage
shift
ROOT= VALUES= PKFILE= JOBS=3
while [ $# -gt 0 ]; do
  [ $# -ge 2 ] || usage
  case "$1" in
    --runs-root) ROOT=$2 ;;
    --values) VALUES=$2 ;;
    --packages) PKFILE=$2 ;;
    --jobs) JOBS=$2 ;;
    *) usage ;;
  esac
  shift 2
done
[ -f "$SCHED" ] || { echo "E_ARG: no schedule file $SCHED" >&2; exit 2; }
[[ $JOBS =~ ^[1-3]$ ]] || { echo "E_JOBS: --jobs is 1, 2 or 3 (at most 3 panels at once)" >&2; exit 2; }
for f in "$VALUES" "$PKFILE"; do
  [ -z "$f" ] && continue
  case "$(realpath -m -- "$f")/" in /tmp/?*) ;; *) echo "E_OVERRIDE: $f is outside /tmp/" >&2; exit 2 ;; esac
done
sw_assert_nofallback || exit 2
if [ "$(sed -n '2p' "$SCHED")" != $'stage\tblock\tarm\tpanel\tdoc\treplicate\tseed\tset\trun' ]; then
  echo "E_ARG: $SCHED is not a schedule file of bin/make-schedule.py" >&2
  exit 2
fi
BASE=${ROOT:-$SW/runs}
sw_assert_writable "$BASE" || exit 2

# The spike record comes first: nothing starts without it (REQ-32).
VALS=${VALUES:-$SW/config/values.json}
SPIKE=$(sw_py "$SW/sweep/cli.py" clock spike --values "$VALS") || { echo "E_ARG: cannot read the values file $VALS" >&2; exit 2; }
if [ "$(jq -r .ok <<<"$SPIKE")" != true ]; then
  echo "E_NO_SPIKE: $VALS has no spike record of 5 runs with a c_luna (bin/run-spike.sh timing); no arm starts without it (REQ-32)" >&2
  exit 2
fi
FALLBACK=$(jq -r .fallback <<<"$SPIKE")
mkdir -p "$BASE" || exit 2
PANELS_IN_USE=$BASE/panels-in-use.json
sw_py "$SW/sweep/cli.py" clock spike --values "$VALS" --panels-out "$PANELS_IN_USE" >/dev/null || exit 2
export SW_PANELS=$PANELS_IN_USE
sw_assert_override SW_PANELS || exit 2

LOG=$BASE/schedule-run.log
RCDIR=$(mktemp -d /tmp/run-schedule.XXXXXXXX) || exit 2
trap 'rm -rf -- "$RCDIR"' EXIT
STARTED=() SKIPPED=() MAXC=0

launch() { # launch ROW-FIELDS...: one run-panel.sh call in the background; its exit code goes to $RCDIR/<run>
  local stage=$1 block=$2 arm=$3 panel=$4 doc=$5 rep=$6 seed=$7 run=$8 conc=$9 dir
  dir=${ROOT:-$SW/runs/stage$stage}/$run
  local args=(--arm "$arm" --panel "$panel" --doc "$doc" --run "$dir" --seed "$seed" --replicate "$rep" --block "$block" --concurrent "$conc")
  [ -n "$VALUES" ] && args+=(--values "$VALUES")
  [ -n "$PKFILE" ] && args+=(--packages "$PKFILE")
  (
    bash "$SW/bin/run-panel.sh" "${args[@]}" >>"$LOG" 2>&1
    echo $? >"$RCDIR/$run"
  ) &
}

while IFS=$'\t' read -r stage block arm panel doc rep seed _set run; do
  [ -n "$run" ] || continue
  dir=${ROOT:-$SW/runs/stage$stage}/$run
  if [ -e "$dir/run.json" ]; then
    SKIPPED+=("$run")
    echo "SKIP $run (run.json exists)" >>"$LOG"
    continue
  fi
  while [ "$(jobs -rp | wc -l)" -ge "$JOBS" ]; do wait -n || true; done
  conc=$(($(jobs -rp | wc -l) + 1))
  [ "$conc" -le "$MAXC" ] || MAXC=$conc
  echo "START $run concurrent=$conc" >>"$LOG"
  launch "$stage" "$block" "$arm" "$panel" "$doc" "$rep" "$seed" "$run" "$conc"
  STARTED+=("$run")
done < <(tail -n +3 "$SCHED")
wait

FAILED=()
for run in ${STARTED[@]+"${STARTED[@]}"}; do
  rc=$(cat "$RCDIR/$run" 2>/dev/null || echo missing)
  [ "$rc" = 0 ] || FAILED+=("$run:$rc")
done
tojson() { printf '%s\n' "$@" | jq -R 'select(length>0)' | jq -sc .; }
jq -n --arg sched "$SCHED" --argjson started "$(tojson ${STARTED[@]+"${STARTED[@]}"})" \
  --argjson skipped "$(tojson ${SKIPPED[@]+"${SKIPPED[@]}"})" --argjson failed "$(tojson ${FAILED[@]+"${FAILED[@]}"})" \
  --argjson fb "$FALLBACK" --argjson maxc "$MAXC" --argjson jobs "$JOBS" --argjson spike "$SPIKE" \
  '{schedule:$sched, started:$started, skipped:$skipped, failed:$failed, max_concurrent:$maxc, jobs:$jobs,
    spike_fallback:$fb, spike:$spike}' >"$BASE/schedule-run.json"
echo "SCHEDULE started=${#STARTED[@]} skipped=${#SKIPPED[@]} failed=${#FAILED[@]} max_concurrent=$MAXC fallback=$FALLBACK"
[ ${#FAILED[@]} -eq 0 ] || exit 1
exit 0
