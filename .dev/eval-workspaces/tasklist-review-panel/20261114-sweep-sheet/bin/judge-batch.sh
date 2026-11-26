#!/usr/bin/env bash
# judge-batch.sh STAGE --gt-dir DIR [--runs DIR] [--scoring DIR] [--cand-root DIR] [--seed N] [--jobs N]   (DESIGN 11.3, 14.3, REQ-43)
# One blind judge per finished run of a stage, an audit of every judge output, and a second judge on a seeded 15% sample.
#   --runs DIR       the run folders of the stage; default SW/runs/STAGE. A run is judged when it holds run.json and merged/merged-1.md
#   --scoring DIR    where the judge folders are made; default SW/scoring/STAGE. A judge folder is named by its random label, so
#                    the path the judge reads in its brief carries no run, arm or reviewer name
#   --gt-dir DIR     holds one ground-truth file per document, DIR/<doc>.json (required; the batch only passes the path on)
#   --cand-root DIR  holds <doc>/candidate.md; default SB/cand (DESIGN 2.2, step S0)
#   --seed N         seeds the second-judge sample (default 20261115); the sample holds round(0.15 n) of the n judged runs
#   --jobs N         judges running at once (default 3)
# Steps: 1 anonymise each merged report (bin/anon.sh) and write RUN/scoring/label-key.json; 2 run bin/judge-one.sh for every
# run that has no score file yet; 3 judge the sample again under a new label (key field `second`); 4 audit every judge folder
# (scaffold/judge.py). A score file that fails the audit is renamed score.json.invalid-<problem> (DESIGN 10 row 20) and the
# batch exits 1: run it again to re-judge those runs. Every step is idempotent. Output under the scoring folder:
#   judge-batch.log (one line per judge), judge-audit.json, judge-batch.json (the summary)
# The judge model is named only in bin/judge-one.sh. Tests run this against the fake claude only.
set -u -o pipefail
source "$(dirname "$0")/common.sh"

usage() {
  sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
STAGE=${1:-}
[ -n "$STAGE" ] || usage
shift
[[ $STAGE =~ ^[A-Za-z0-9._-]+$ ]] || { echo "E_ARG: bad stage name $STAGE" >&2; exit 2; }
RUNS=$SW/runs/$STAGE SCORING=$SW/scoring/$STAGE CANDROOT=$SB/cand GTDIR= SEED=20261115 JOBS=3
while [ $# -gt 0 ]; do
  [ $# -ge 2 ] || usage
  case "$1" in
    --runs) RUNS=$2 ;;
    --scoring) SCORING=$2 ;;
    --cand-root) CANDROOT=$2 ;;
    --gt-dir) GTDIR=$2 ;;
    --seed) SEED=$2 ;;
    --jobs) JOBS=$2 ;;
    *) usage ;;
  esac
  shift 2
done
[ -d "$GTDIR" ] || { echo "E_ARG: --gt-dir is required and must be a folder" >&2; exit 2; }
[ -d "$RUNS" ] || { echo "E_ARG: no run folder $RUNS" >&2; exit 2; }
[[ $SEED =~ ^[0-9]+$ ]] || { echo "E_ARG: --seed is not a number" >&2; exit 2; }
[[ $JOBS =~ ^[1-9][0-9]*$ ]] || { echo "E_ARG: --jobs is not a positive number" >&2; exit 2; }
sw_assert_writable "$SCORING" || exit 2
mkdir -p "$SCORING" || exit 2
LOG=$SCORING/judge-batch.log

# Finished runs, and a check of every input before any judge starts.
ELIG=() UNMERGED=()
for R in "$RUNS"/*/; do
  R=${R%/}
  [ -f "$R/run.json" ] || continue
  if [ -f "$R/merged/merged-1.md" ]; then ELIG+=("$R"); else UNMERGED+=("$(basename "$R")"); fi
done
[ ${#ELIG[@]} -gt 0 ] || { echo "E_ARG: no run with merged/merged-1.md under $RUNS" >&2; exit 2; }
doc_of() { jq -r '.doc // empty' "$1/run.json"; }
for R in "${ELIG[@]}"; do
  doc=$(doc_of "$R")
  [ -n "$doc" ] || { echo "E_ARG: $R/run.json has no doc" >&2; exit 2; }
  [ -f "$GTDIR/$doc.json" ] || { echo "E_ARG: no ground-truth file for $doc under $GTDIR" >&2; exit 2; }
  [ -f "$CANDROOT/$doc/candidate.md" ] || { echo "E_ARG: no candidate for $doc under $CANDROOT" >&2; exit 2; }
done

# 1. Anonymise. The key keeps the label, the judge folder and, later, the second judge's.
key_of() { echo "$1/scoring/label-key.json"; }
for R in "${ELIG[@]}"; do
  K=$(key_of "$R")
  [ -f "$K" ] && continue
  sw_assert_writable "$R/scoring" || exit 2
  mkdir -p "$R/scoring" || exit 2
  L=$(bash "$SW/bin/anon.sh" "$R/merged/merged-1.md" "$SCORING") || { echo "E_ANON: $R" >&2; exit 2; }
  jq -n --arg l "$L" --arg d "$SCORING/$L" --arg r "$(basename "$R")" --arg doc "$(doc_of "$R")" \
    '{label:$l, dir:$d, run:$r, doc:$doc, second:null}' >"$K"
done

# 2. Judge. Judges run $JOBS at a time; a failure is left to the audit.
judge_dir() { # judge_dir DIR DOC
  bash "$SW/bin/judge-one.sh" "$1" "$GTDIR/$2.json" "$CANDROOT/$2/candidate.md" "$2" blind >>"$LOG" 2>&1
}
pool_wait() { while [ "$(jobs -rp | wc -l)" -ge "$JOBS" ]; do wait -n || true; done; }
for R in "${ELIG[@]}"; do
  pool_wait
  judge_dir "$(jq -r .dir "$(key_of "$R")")" "$(doc_of "$R")" &
done
wait

# 3. Second judge on a seeded sample of round(0.15 n) runs: a new label, so it never sees the first judge's score.
IDS=()
for R in "${ELIG[@]}"; do IDS+=("$(basename "$R")"); done
mapfile -t SAMPLE < <(sw_py "$SW/scaffold/judge.py" sample "$SEED" "${IDS[@]}")
for id in ${SAMPLE[@]+"${SAMPLE[@]}"}; do
  R=$RUNS/$id
  K=$(key_of "$R")
  if [ "$(jq -r '.second // empty' "$K")" = "" ]; then
    L2=$(bash "$SW/bin/anon.sh" "$R/merged/merged-1.md" "$SCORING") || { echo "E_ANON: $R" >&2; exit 2; }
    jq --arg l "$L2" --arg d "$SCORING/$L2" '.second={label:$l, dir:$d}' "$K" >"$K.tmp" && mv "$K.tmp" "$K"
  fi
  pool_wait
  judge_dir "$(jq -r .second.dir "$K")" "$(doc_of "$R")" &
done
wait

# 4. Audit every judge folder; invalidate a bad score file.
DIRS=()
for R in "${ELIG[@]}"; do
  K=$(key_of "$R")
  DIRS+=("$(jq -r .dir "$K")")
  [ "$(jq -r '.second // empty' "$K")" = "" ] || DIRS+=("$(jq -r .second.dir "$K")")
done
sw_py "$SW/scaffold/judge.py" audit "${DIRS[@]}" >"$SCORING/judge-audit.json"
BAD=$(jq -r .bad "$SCORING/judge-audit.json")
while IFS=$'\t' read -r dir problem; do
  [ -f "$dir/score.json" ] || continue
  mv -n "$dir/score.json" "$dir/score.json.invalid-$problem"
  echo "INVALIDATED $dir/score.json ($problem)" >>"$LOG"
done < <(jq -r '.items[] | [.dir, .problems[0]] | @tsv' "$SCORING/judge-audit.json")

jq -n --arg stage "$STAGE" --argjson seed "$SEED" --argjson n "${#ELIG[@]}" --argjson bad "$BAD" \
  --argjson second "$(printf '%s\n' ${SAMPLE[@]+"${SAMPLE[@]}"} | jq -R 'select(length>0)' | jq -sc .)" \
  --argjson unmerged "$(printf '%s\n' ${UNMERGED[@]+"${UNMERGED[@]}"} | jq -R 'select(length>0)' | jq -sc .)" \
  '{stage:$stage, seed:$seed, runs_judged:$n, second_sample:$second, unmerged_runs:$unmerged, audit_bad:$bad}' \
  >"$SCORING/judge-batch.json"
echo "BATCH stage=$STAGE runs=${#ELIG[@]} second=${#SAMPLE[@]} bad=$BAD"
if [ "$BAD" -ne 0 ]; then
  echo "BATCH_BAD: see $SCORING/judge-audit.json; run this command again to re-judge the invalidated runs" >&2
  exit 1
fi
