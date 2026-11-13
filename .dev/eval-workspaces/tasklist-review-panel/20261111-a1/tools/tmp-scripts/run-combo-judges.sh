#!/bin/bash
# Run all 39 blind combo judges via claude -p (Opus), 4 at a time.
# Each judge reads GT + candidate + one anonymized merged report, writes score.json.
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
LIST=/tmp/combo-judges.tsv
OUTDIR="$EVAL/arms/scoring/combos"
run_judge() {
  local C="$1" P="$2" L="$3" F="$4"
  local D="$OUTDIR/$C/$P/$L"
  [ -f "$D/score.json" ] && { echo "SKIP $C/$P/$L"; return 0; }
  local GT="$EVAL/$P/ground-truth.json"
  local CAND="$EVAL/$P/candidate.md"
  local GTN=$(jq -r '.items|length' "$GT")
  local BRIEF
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
  local RC=0
  timeout 900 claude -p --model claude-opus-5-5 --output-format json --no-session-persistence \
    --permission-mode bypassPermissions \
    < <(printf '%s' "$BRIEF") > "$D/judge.json" 2> "$D/judge.err" || RC=$?
  if [ $RC -ne 0 ] || ! jq -e . "$D/judge.json" >/dev/null 2>&1; then
    echo "FAIL $C/$P/$L rc=$RC"
    return 1
  fi
  echo "OK $C/$P/$L"
}
export -f run_judge 2>/dev/null || true
# serial-4: run with xargs -P4
awk -F'\t' '{print $1"\t"$2"\t"$3"\t"$4}' "$LIST" | xargs -P 4 -I{} bash -c 'IFS=$'"'"'\t'"'"' read -r C P L F <<< "{}"; run_judge "$C" "$P" "$L" "$F"' _
echo ALL_DONE
