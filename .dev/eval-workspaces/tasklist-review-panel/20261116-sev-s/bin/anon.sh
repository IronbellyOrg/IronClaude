#!/usr/bin/env bash
# usage: anon.sh <run dir> <label> <out file> [seed]
# Anonymise the merged report of one run for the blind judge (DESIGN 9.7, REQ-43). Built locally to the sibling's
# written contract: the label is random-looking, reviewer ids become R1..Rn (numbered by a shuffle seeded by seed and
# label), every absolute path and the run id are redacted (merged-1.md prints each reviewer's report path, which holds
# the run id), and the arm marker (`ledger-v1`, the keys class, probe and src, the arm names) is removed. The result is
# checked again and the script exits 3 if anything still leaks. No model, no network, no ground truth.
# Exit codes: 0 written; 2 usage; 3 the anonymised report still leaks or the run has no merged report.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=rl-env.sh
source "$HERE/rl-env.sh"
# shellcheck source=common.sh
source "$HERE/common.sh"

if [ $# -lt 3 ] || [ $# -gt 4 ]; then
  echo "usage: anon.sh <run dir> <label> <out file> [seed]" >&2
  exit 2
fi
RUN=$1 LABEL=$2 OUT=$3 SEED=${4:-0}
[[ $LABEL =~ ^[A-Za-z0-9._-]+$ && $SEED =~ ^[0-9]+$ ]] || { echo "E_USAGE: bad label or seed" >&2; exit 2; }
sw_assert_writable "$OUT" || exit 2
sw_py "$SW/analysis/judge_audit.py" anon --run "$RUN" --label "$LABEL" --seed "$SEED" --out "$OUT"
