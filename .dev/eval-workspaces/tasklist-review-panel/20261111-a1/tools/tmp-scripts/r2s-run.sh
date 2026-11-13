#!/usr/bin/env bash
# runs the 12 reviewer runs strictly one at a time
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
for p in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
 for r in t4-1:claude-haiku-5-5 t3-1:claude-haiku-5-5 t4-2:grok-4.7 t1b-1:claude-sonnet-5-5; do
  echo "START $p ${r%%:*} $(date +%T)"
  bash $EVAL/tools/run-reviewer.sh $EVAL $p ${r%%:*} ${r#*:} combos/r2-sonnet
  echo "END $p ${r%%:*} $(date +%T)"
 done
done
echo ALLDONE
