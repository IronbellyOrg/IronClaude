#!/usr/bin/env bash
# run-spike.sh {timing|compliance} --panel {ember|haiku|sonnet} --doc DOC [--runs N] [--baseline-runs N] [--item-count N]
#                                   [--runs-root DIR] [--values FILE] [--packages FILE]   (DESIGN 14.2, REQ-17, REQ-32)
# The two spikes that come before every arm. They start models, so in real use they need the owner's go-ahead; the tests run
# them against the fake claude only. Runs go one after the other through bin/run-panel.sh (one panel at a time).
#   timing      N SS runs (--runs, default 5) and N Z0 runs (--baseline-runs, default 5) of the panel on one document, block k
#               holding SS run k and Z0 run k (the same day). From the luna reviewers' wall seconds it computes
#                 c_luna = (median(luna seconds in the SS runs) - median(luna seconds in the Z0 runs) - 3) / item_count
#               (item_count default 8) and writes the record `spike` = {runs, baseline_runs, item_count, c_luna, median_ss_s,
#               median_z0_s, doc, panel, date} into the values file (config/values.json, or --values). Output: <root>/spike-timing/.
#   compliance  N SS runs (default 5) and then `analysis/analyze.py compliance` over them: the ledger_missing rate, the quote
#               validity and the format errors. Exit 0 when ledger_missing is at most 10% (go), 1 when it is not.
#               Output: <root>/spike-compliance/ (compliance.json beside the run folders).
# Options: --runs-root DIR (default SW/runs; under SW or /tmp), --values FILE and --packages FILE (test hooks, /tmp only).
# Environment: NOFALLBACK=1 is required (DD-8). Exit: 0 done (and go); 1 compliance no-go or a run failed; 2 refused.
set -u -o pipefail
source "$(dirname "$0")/common.sh"

usage() {
  sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
MODE=${1:-}
case "$MODE" in timing | compliance) shift ;; *) usage ;; esac
PANEL= DOC= RUNS=5 BASE_RUNS=5 ITEMS=8 ROOT= VALUES= PKFILE=
while [ $# -gt 0 ]; do
  [ $# -ge 2 ] || usage
  case "$1" in
    --panel) PANEL=$2 ;;
    --doc) DOC=$2 ;;
    --runs) RUNS=$2 ;;
    --baseline-runs) BASE_RUNS=$2 ;;
    --item-count) ITEMS=$2 ;;
    --runs-root) ROOT=$2 ;;
    --values) VALUES=$2 ;;
    --packages) PKFILE=$2 ;;
    *) usage ;;
  esac
  shift 2
done
case "$PANEL" in ember) PANEL=primary ;; primary | haiku | sonnet) ;; *) echo "E_ARG: --panel is ember, haiku or sonnet" >&2; exit 2 ;; esac
[[ $DOC =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || { echo "E_DOC: bad document id: $DOC" >&2; exit 2; }
for v in RUNS BASE_RUNS ITEMS; do [[ ${!v} =~ ^[1-9][0-9]*$ ]] || { echo "E_ARG: $v is not a positive number" >&2; exit 2; }; done
for f in "$VALUES" "$PKFILE"; do
  [ -z "$f" ] && continue
  case "$(realpath -m -- "$f")/" in /tmp/?*) ;; *) echo "E_OVERRIDE: $f is outside /tmp/" >&2; exit 2 ;; esac
done
sw_assert_nofallback || exit 2
BASE=${ROOT:-$SW/runs}
sw_assert_writable "$BASE" || exit 2
VALS=${VALUES:-$SW/config/values.json}
[ -f "$VALS" ] || { echo "E_ARG: no values file $VALS" >&2; exit 2; }

panel_run() { # panel_run ARM DIR K: one run of the spike, block K
  local args=(--arm "$1" --panel "$PANEL" --doc "$DOC" --run "$2" --seed 1 --replicate "$3" --block "$3" --concurrent 1)
  [ -n "$VALUES" ] && args+=(--values "$VALUES")
  [ -n "$PKFILE" ] && args+=(--packages "$PKFILE")
  bash "$SW/bin/run-panel.sh" "${args[@]}"
}
median() { jq -s 'sort | if length == 0 then null elif length % 2 == 1 then .[length / 2 | floor] else (.[length / 2 - 1] + .[length / 2]) / 2 end'; }
luna_seconds() { # luna_seconds RUNDIR...: the wall seconds of every luna reviewer of the runs
  local d
  for d in "$@"; do
    for f in "$d"/reviews/*.meta.json; do
      [ -f "$f" ] || continue
      case $f in *.attempt*.meta.json) continue ;; esac # <rid>.meta.json is the copy of <rid>.attempt1.meta.json: count once
      jq -r 'select(.expected_model == "gpt-6-luna") | .wall_s' "$f"
    done
  done
}

FAILED=0
if [ "$MODE" = timing ]; then
  OUT=$BASE/spike-timing
  mkdir -p "$OUT" || exit 2
  N=$((RUNS > BASE_RUNS ? RUNS : BASE_RUNS))
  for k in $(seq 1 "$N"); do
    [ "$k" -gt "$RUNS" ] || panel_run SS "$OUT/ss-$k" "$k" || FAILED=1
    [ "$k" -gt "$BASE_RUNS" ] || panel_run Z0 "$OUT/z0-$k" "$k" || FAILED=1
  done
  SS_DIRS=() Z0_DIRS=()
  for k in $(seq 1 "$RUNS"); do [ -f "$OUT/ss-$k/run.json" ] && SS_DIRS+=("$OUT/ss-$k"); done
  for k in $(seq 1 "$BASE_RUNS"); do [ -f "$OUT/z0-$k/run.json" ] && Z0_DIRS+=("$OUT/z0-$k"); done
  MS=$(luna_seconds ${SS_DIRS[@]+"${SS_DIRS[@]}"} | median)
  MZ=$(luna_seconds ${Z0_DIRS[@]+"${Z0_DIRS[@]}"} | median)
  if [ "$MS" = null ] || [ "$MZ" = null ] || [ -z "$MS" ] || [ -z "$MZ" ]; then
    echo "E_SPIKE_DATA: no luna reviewer finished in the SS runs or in the Z0 runs; no record written" >&2
    exit 1
  fi
  REC=$(jq -n --argjson runs "${#SS_DIRS[@]}" --argjson base "${#Z0_DIRS[@]}" --argjson n "$ITEMS" --argjson ms "$MS" --argjson mz "$MZ" \
    --arg doc "$DOC" --arg panel "$PANEL" --arg date "$(date -u +%Y-%m-%d)" \
    '{runs:$runs, baseline_runs:$base, item_count:$n, c_luna:((($ms - $mz - 3) / $n) * 1000 | round / 1000),
      median_ss_s:$ms, median_z0_s:$mz, doc:$doc, panel:$panel, date:$date}')
  jq --argjson rec "$REC" '.spike = $rec' "$VALS" >"$VALS.tmp.$$" && mv -- "$VALS.tmp.$$" "$VALS" || { rm -f -- "$VALS.tmp.$$"; exit 1; }
  echo "SPIKE timing: $REC"
  [ "$FAILED" = 0 ] || exit 1
  exit 0
fi

# compliance
OUT=$BASE/spike-compliance
mkdir -p "$OUT" || exit 2
for k in $(seq 1 "$RUNS"); do
  panel_run SS "$OUT/ss-$k" "$k" || FAILED=1
done
sw_py "$SW/analysis/analyze.py" compliance --runs "$OUT" --out "$OUT/compliance.json" || exit 1
[ "$FAILED" = 0 ] || exit 1
exit 0
