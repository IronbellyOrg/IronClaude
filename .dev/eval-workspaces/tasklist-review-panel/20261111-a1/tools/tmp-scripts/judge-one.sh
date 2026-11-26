#!/bin/bash
# Worker for one judge line: C P L (tab-separated args).
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
C="$1"; P="$2"; L="$3"
D="$EVAL/arms/scoring/combos/$C/$P/$L"
[ -f "$D/score.json" ] && { echo "SKIP $C/$P/$L"; exit 0; }
GT="$EVAL/$P/ground-truth.json"
CAND="$EVAL/$P/candidate.md"
F="$D/merged-anon.md"
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
