#!/usr/bin/env bash
# Two luna-bearing rows WITHOUT muse, run in parallel with b4 (serial inside each row, one reviewer at a time).
# r3-luna2-grok-src: luna x2 + grok (best non-muse luna row to re-test; original 2/14, luna 0 findings on designSpec)
# c3-luna-grok-src:  luna + grok (cheapest luna row; original 1/14, luna empty everywhere)
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
RR="$EVAL/tools/run-reviewer.sh"
DS=TASK-WF-designSpec-20261107-075614
AL=TASK-WF-makeTheAliasOnly-20261105-051649
DE=TASK-WF-design-20261108-041415

run() { echo "START $(date -u +%T) $4/$1/$2=$3"; bash "$RR" "$EVAL" "$1" "$2" "$3" "combos/$4"; echo "END $(date -u +%T) $4/$1/$2 $(jq -c '[.observed_model,.model_ok,.findings_block]' "$EVAL/$1/reviews/combos/$4/$2.meta.json" 2>/dev/null)"; }

# Row A: r3-luna2-grok-src (t4-1 luna, t3-1 luna, t4-2 grok) - parallel to b4
(
  for p in $DS $AL $DE; do
    run "$p" t4-1 gpt-6-luna r3-luna2-grok-src
    run "$p" t3-1 gpt-6-luna r3-luna2-grok-src
    run "$p" t4-2 grok-4.7 r3-luna2-grok-src
  done
  echo R3_SRC_DONE
) > /tmp/b4-r3.log 2>&1 &

# Row B: c3-luna-grok-src (t4-1 luna, t4-2 grok)
(
  for p in $DS $AL $DE; do
    run "$p" t4-1 gpt-6-luna c3-luna-grok-src
    run "$p" t4-2 grok-4.7 c3-luna-grok-src
  done
  echo C3_SRC_DONE
) > /tmp/b4-c3.log 2>&1 &

wait
echo LUNA_NO_MUSE_DONE
