#!/usr/bin/env bash
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
hb(){ orca orchestration send --from term_12f0d3c0-a102-4007-be44-98a3992acd74 --type heartbeat --subject alive --task-id task_66219252a0bf --dispatch-id ctx_bd9d9609e808 --phase "$1" >/dev/null 2>&1; }
( while true; do sleep 270; hb "running reviewers"; done ) & HB=$!
for P in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
 for R in "t4-1 claude-haiku-5-5" "t3-1 claude-haiku-5-5" "t4-2 grok-4.7" "t2b-1 gpt-6.1-terra"; do
  set -- $R
  bash $EVAL/tools/run-reviewer.sh $EVAL $P $1 $2 combos/r2-terra
  echo "DONE $P $1 $(date -u +%H:%M:%S)"
 done
done
kill $HB; echo ALL_DONE
