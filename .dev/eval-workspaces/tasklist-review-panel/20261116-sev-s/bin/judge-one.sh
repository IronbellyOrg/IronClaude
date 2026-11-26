#!/usr/bin/env bash
# usage: judge-one.sh --go <label> <doc id>
# The blind judge for one anonymised merged report (DESIGN 9.7, REQ-05, REQ-43). Built locally to the sibling's written
# contract: a copy of the original judge script with the paths as variables and the BRIEF text (original lines 12-23)
# byte for byte; a test compares its sha256. THIS SCRIPT STARTS THE BLIND OPUS JUDGE. The build never runs it:
# it refuses (exit 4) unless NOFALLBACK=1 and the explicit argument --go are both present. It is the only file under
# bin/, rl/ and scaffold/ that names the judge model (K2).
#
# Reads  $D/merged-anon.md (written by anon.sh), the candidate and the ground truth of the package <doc id>
#        ($JUDGE_PKG_ROOT/<doc id>/{candidate.md,ground-truth.json}; JUDGE_PKG_ROOT defaults to EVAL, hold-out documents
#        use RL/holdout-gt). Reading the ground truth is what scoring is; no other script of this design does it.
# Writes $D/judge.json, $D/judge.err and (by the judge) $D/score.json, with D = scoring/<label>.
# The combo field of score.json carries the label, never a run id or an arm, so the judge cannot see the arm.
# Exit codes: 0 judged or skipped (score.json exists); 1 the judge call failed; 2 usage; 4 refused.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=rl-env.sh
source "$HERE/rl-env.sh"
# shellcheck source=common.sh
source "$HERE/common.sh"

[ "${1:-}" = "--go" ] || { echo "E_REFUSED: judge-one.sh starts the blind Opus judge; pass --go as the first argument" >&2; exit 4; }
sw_assert_nofallback || exit 4
shift
[ $# -eq 2 ] || { echo "usage: judge-one.sh --go <label> <doc id>" >&2; exit 2; }
L="$1"; P="$2"; C="$L"
[[ $L =~ ^[A-Za-z0-9._-]+$ && $P =~ ^[A-Za-z0-9._-]+$ ]] || { echo "E_USAGE: bad label or doc id" >&2; exit 2; }
EVAL=${JUDGE_PKG_ROOT:-$EVAL}
D="${JUDGE_SCORING_DIR:-$SW/scoring}/$L"
sw_assert_writable "$D" || exit 2
[ -f "$D/score.json" ] && { echo "SKIP $C/$P/$L"; exit 0; }
GT="$EVAL/$P/ground-truth.json"
CAND="$EVAL/$P/candidate.md"
F="$D/merged-anon.md"
for f in "$GT" "$CAND" "$F"; do [ -f "$f" ] || { echo "E_USAGE: missing $f" >&2; exit 2; }; done
GTN=$(jq -r '.items|length' "$GT")
BRIEF="You are a blind scoring judge for an evaluation of review panels. Score ONE merged review report against ground truth. Do not read anything outside the files named here.
Files:
- Ground truth: $GT (items GT1..GT$GTN, each with id, class, blocking_in_implement, description, plan_quote)
- Candidate plan under review: $CAND
- Merged review report (anonymized): $F
Task:
1. Read all three files fully.
2. For each ground truth item GTn: does ANY finding in the merged report (Ledger rows / Blocking findings / Other findings) describe the same underlying defect? Covered only if the claim is substantively about the same wrong outcome (match anchors/quotes against candidate.md; wording differences fine, different defects not). Record covered at any severity and covered by a BLOCKING ledger row (blocking yes).
3. For each blocking ledger row: does it correspond to at least one ground truth item? A blocking row with no GT correspondence is a wrong blocker. Count them.
4. Write JSON to $D/score.json with schema: {\"label\":\"$L\",\"combo\":\"$C\",\"package\":\"$P\",\"gt_total\":$GTN,\"gt_covered_any\":[...],\"gt_covered_blocking\":[...],\"ledger_rows_total\":N,\"ledger_rows_blocking\":N,\"blocking_rows_gt_matched\":N,\"wrong_blockers\":N,\"notes\":\"2-3 sentences citing lids and GT ids\"}
5. Reply one line: score.json written, gt_covered_any count, wrong_blockers count.
Rules: never invent ground truth; be strict about same defect; if the report is unreadable write score.json with zeros and say why."
RC=0
timeout 900 claude -p --model claude-opus-5-5 --output-format json --no-session-persistence \
  --permission-mode bypassPermissions \
  < <(printf '%s' "$BRIEF") > "$D/judge.json" 2> "$D/judge.err" || RC=$?
if [ $RC -ne 0 ] || ! jq -e . "$D/judge.json" >/dev/null 2>&1; then
  echo "FAIL $C/$P/$L rc=$RC"; exit 1
fi
echo "OK $C/$P/$L"
