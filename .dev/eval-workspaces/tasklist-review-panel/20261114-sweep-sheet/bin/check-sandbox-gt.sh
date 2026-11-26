#!/usr/bin/env bash
# check-sandbox-gt.sh [--sb DIR] [--runs DIR]   (REQ-34, DESIGN AO-6; read-only)
# A recursive grep for ground truth over every sandbox repository (DIR/<doc>/repo and DIR/<doc>/repo-raw) and every sheet of
# every run (RUNS/*/*/prepass/sheets): a file whose name starts with `ground-truth`, and any text that holds a field name of
# a ground-truth item or of a judge score (plan_quote, blocking_in_implement, gt_covered_any, gt_covered_blocking).
# It prints one line per hit and nothing when the places are clean. Run it before the first arm and after the last.
#   --sb DIR     the sandbox root (default SW_SB_ROOT or /tmp/evalsb-sweep)
#   --runs DIR   the run folders (default <SW>/runs); the sheets are RUNS/<stage>/<run>/prepass/sheets and, for a folder of runs
#                directly under RUNS, RUNS/<run>/prepass/sheets
# Exit: 0 clean (and no output); 1 a hit (printed); 2 no sandbox under the root, so nothing could be checked (a clean result
# over nothing would prove nothing).
set -u -o pipefail
source "$(dirname "$0")/common.sh"

usage() {
  sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
SBROOT=$SB RUNS=$SW/runs
while [ $# -gt 0 ]; do
  [ $# -ge 2 ] || usage
  case "$1" in
    --sb) SBROOT=$2 ;;
    --runs) RUNS=$2 ;;
    *) usage ;;
  esac
  shift 2
done

PLACES=()
for d in "$SBROOT"/*/repo "$SBROOT"/*/repo-raw; do
  [ -d "$d" ] && PLACES+=("$d")
done
[ ${#PLACES[@]} -gt 0 ] || { echo "E_NO_SANDBOX: no <doc>/repo under $SBROOT; build it with bin/build-sandbox.sh" >&2; exit 2; }
for d in "$RUNS"/*/*/prepass/sheets "$RUNS"/*/prepass/sheets; do
  [ -d "$d" ] && PLACES+=("$d")
done

HITS=0
FIELDS='plan_quote|blocking_in_implement|gt_covered_any|gt_covered_blocking'
for place in "${PLACES[@]}"; do
  while IFS= read -r f; do
    echo "$f: a file named like ground truth"
    HITS=1
  done < <(find "$place" -path '*/.git' -prune -o \( -iname 'ground-truth*' -o -iname 'ground_truth*' \) -print 2>/dev/null)
  while IFS= read -r line; do
    echo "$line"
    HITS=1
  done < <(grep -rEIn --exclude-dir=.git -e "$FIELDS" -- "$place" 2>/dev/null | cut -c1-200)
done
[ "$HITS" = 0 ] || exit 1
exit 0
