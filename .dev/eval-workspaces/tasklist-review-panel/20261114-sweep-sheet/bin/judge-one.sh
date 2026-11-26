#!/bin/bash
# Worker for one blind judge run (DESIGN 11.3, REQ-43): a copy of JJ (EVAL/tools/tmp-scripts/judge-one.sh) with the paths turned
# into variables. Usage: judge-one.sh D GT CAND [P [C]]
#   D     the judge folder, named by its random label; it holds merged-anon.md (bin/anon.sh) and receives score.json,
#         judge.json, judge.err and judge.started (the audit compares score.json with it)
#   GT    the ground-truth file of the document (a path given by the caller; this script never builds one)
#   CAND  the candidate plan under review
#   P     the document id written into score.json ("package"); default "document"
#   C     the opaque value written into score.json ("combo"); default "blind". It must never name the arm: the judge
#         reads it in the brief below.
# The BRIEF text is byte-identical to JJ lines 12-23 (a test compares the sha256). The judge model is named here and
# nowhere else in bin/, sweep/ and scaffold/ (K2).
set -u
source "$(dirname "$0")/common.sh"
D=${1:?usage: judge-one.sh D GT CAND [P [C]]}
GT=${2:?usage: judge-one.sh D GT CAND [P [C]]}
CAND=${3:?usage: judge-one.sh D GT CAND [P [C]]}
P=${4:-document}
C=${5:-blind}
L=$(basename "$D")
sw_assert_writable "$D" || exit 2
# EVAL (the study folder) is read only: a judge folder inside it is refused.
case "$(realpath -m -- "$D")/" in "$EVAL"/*) echo "E_NOT_WRITABLE: $D is inside the study folder" >&2; exit 2 ;; esac
F="$D/merged-anon.md"
[ -f "$F" ] || { echo "FAIL $C/$P/$L: $F is missing" >&2; exit 2; }
[ -f "$GT" ] || { echo "FAIL $C/$P/$L: the ground-truth file is missing" >&2; exit 2; }
[ -f "$CAND" ] || { echo "FAIL $C/$P/$L: the candidate is missing" >&2; exit 2; }
[ -f "$D/score.json" ] && { echo "SKIP $C/$P/$L"; exit 0; }
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
: > "$D/judge.started"
timeout 900 claude -p --model claude-opus-5-5 --output-format json --no-session-persistence \
  --permission-mode bypassPermissions \
  < <(printf '%s' "$BRIEF") > "$D/judge.json" 2> "$D/judge.err" || RC=$?
if [ $RC -ne 0 ] || ! jq -e . "$D/judge.json" >/dev/null 2>&1; then
  echo "FAIL $C/$P/$L rc=$RC"; exit 1
fi
echo "OK $C/$P/$L"
