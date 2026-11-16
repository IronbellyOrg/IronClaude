#!/usr/bin/env bash
# usage: judge-batch.sh [--go] [--dry | --audit-only] [--seed N] [--par N] [--runs-dir DIR] [--scoring-dir DIR]
#                       (--runs RUN... | <stage>)
# Anonymise the merged report of every run, run one blind judge per run and a second judge on a seeded 15% sample
# (round(0.15 n) runs, the same for a fixed seed), then audit every judge output (DESIGN 9.7, REQ-43, row 22).
# `<stage>` selects every folder runs/<stage>-* that holds merged/merged-1.md (the schedule names its runs that way).
# Built locally to the sibling's written contract.
#
# THIS SCRIPT STARTS THE BLIND JUDGE through judge-one.sh, so it refuses (exit 4) unless NOFALLBACK=1 and --go are
# given. Two modes never start a judge and need no --go: --dry (writes scoring/labels.tsv and the anonymised reports,
# prints the plan) and --audit-only (audits the judge folders that exist).
#
# scoring/labels.tsv holds label, run, doc, role (first | second); it is the only map from a label to a run.
# The audit flags: no_judge_json, judge_unparseable, api_error, no_score, score_unparseable, stale_score,
# rows_total_mismatch, rows_blocking_mismatch. A flagged score.json is renamed score.json.invalid and the judge is run
# once more for that label; the audit is then repeated and written to scoring/judge_audit.json.
# Exit codes: 0 every item good; 1 an item is still bad; 2 usage; 3 anonymisation failed; 4 refused.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=rl-env.sh
source "$HERE/rl-env.sh"
# shellcheck source=common.sh
source "$HERE/common.sh"

GO=0 DRY=0 AUDIT_ONLY=0 SEED=20261115 PAR=4
RUNS_DIR=$SW/runs SCORING=$SW/scoring
RUNS=() STAGE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --go) GO=1 ;;
    --dry) DRY=1 ;;
    --audit-only) AUDIT_ONLY=1 ;;
    --seed) SEED=${2:-}; shift ;;
    --par) PAR=${2:-}; shift ;;
    --runs-dir) RUNS_DIR=${2:-}; shift ;;
    --scoring-dir) SCORING=${2:-}; shift ;;
    --runs) shift; while [ $# -gt 0 ] && [[ $1 != --* ]]; do RUNS+=("$1"); shift; done; continue ;;
    --*) echo "E_USAGE: unknown option $1" >&2; exit 2 ;;
    *) STAGE=$1 ;;
  esac
  shift
done
[[ $SEED =~ ^[0-9]+$ && $PAR =~ ^[1-9][0-9]*$ ]] || { echo "E_USAGE: --seed and --par are positive numbers" >&2; exit 2; }
sw_assert_writable "$SCORING" || exit 2

if [ "$AUDIT_ONLY" = 1 ]; then
  sw_py "$SW/analysis/judge_audit.py" audit --scoring-dir "$SCORING" --out "$SCORING/judge_audit.json"
  exit $?
fi

if [ "$DRY" = 0 ] && { [ "$GO" = 0 ] || ! sw_assert_nofallback; }; then
  echo "E_REFUSED: judge-batch.sh starts the blind Opus judge; it needs NOFALLBACK=1 and --go (or use --dry / --audit-only)" >&2
  exit 4
fi

if [ -n "$STAGE" ]; then
  for d in "$RUNS_DIR/$STAGE"-*/; do
    [ -f "${d}merged/merged-1.md" ] && RUNS+=("$(basename "$d")")
  done
fi
[ ${#RUNS[@]} -gt 0 ] || { echo "E_USAGE: no runs (give --runs RUN... or a stage with merged reports)" >&2; exit 2; }

mkdir -p "$SCORING"
PLAN=$(sw_py "$SW/analysis/judge_audit.py" plan --runs-dir "$RUNS_DIR" --scoring-dir "$SCORING" --seed "$SEED" "${RUNS[@]}") || exit 2
JOBS=()
while IFS=$'\t' read -r label run doc role; do
  [ -n "$label" ] || continue
  bash "$HERE/anon.sh" "$RUNS_DIR/$run" "$label" "$SCORING/$label/merged-anon.md" "$SEED" || exit 3
  JOBS+=("$label $doc")
  echo "PLAN $label $role"
done <<<"$PLAN"
if [ "$DRY" = 1 ]; then
  echo "DRY ${#RUNS[@]} runs, $(( ${#JOBS[@]} - ${#RUNS[@]} )) second judgings; no judge started"
  exit 0
fi

judge_all() { printf '%s\n' "$@" | JUDGE_SCORING_DIR=$SCORING xargs -P "$PAR" -L 1 bash "$HERE/judge-one.sh" --go; }
judge_all "${JOBS[@]}" || true
sw_py "$SW/analysis/judge_audit.py" audit --scoring-dir "$SCORING" --invalidate --out "$SCORING/judge_audit.json" || {
  echo "re-judging the flagged items once"
  AGAIN=()
  for j in "${JOBS[@]}"; do
    [ -f "$SCORING/${j%% *}/score.json" ] || AGAIN+=("$j")
  done
  [ ${#AGAIN[@]} -eq 0 ] || judge_all "${AGAIN[@]}" || true
}
sw_py "$SW/analysis/judge_audit.py" audit --scoring-dir "$SCORING" --out "$SCORING/judge_audit.json"
