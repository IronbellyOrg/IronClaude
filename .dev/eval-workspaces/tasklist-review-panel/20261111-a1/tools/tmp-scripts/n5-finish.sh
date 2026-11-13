#!/usr/bin/env bash
# Controlled serial completion of the 5 missing/corrupted n5 reviewer runs.
# No parallelism, no workers, no driver. One run-reviewer.sh at a time.
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
DS=TASK-WF-designSpec-20261107-075614
DE=TASK-WF-design-20261108-041415
RR="$EVAL/tools/run-reviewer.sh"

run() { # pkg rid model combo
  echo "START $(date -u +%T) $4/$1/$2=$3"
  bash "$RR" "$EVAL" "$1" "$2" "$3" "combos/$4"
  echo "END $(date -u +%T) $4/$1/$2 $(jq -c '[.observed_model,.model_ok,.findings_block]' "$EVAL/$1/reviews/combos/$4/$2.meta.json" 2>/dev/null)"
}

run "$DE" t3-1 glm-5.3 n5-terra
run "$DS" t3-1 glm-5.3 n5-sol
run "$DE" t3-1 glm-5.3 n5-sol
run "$DE" t4-1 gpt-6-luna n5-sol
run "$DE" t2-1 gpt-6.1-sol n5-sol
echo ALLDONE
