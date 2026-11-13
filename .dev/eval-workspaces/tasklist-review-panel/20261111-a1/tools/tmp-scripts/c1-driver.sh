#!/usr/bin/env bash
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
for p in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
  echo "$p t4-1 claude-haiku-5-5"; echo "$p t4-2 gpt-6-luna"
done | xargs -P 2 -L 1 bash -c 'bash '$EVAL'/tools/run-reviewer.sh '$EVAL' "$0" "$1" "$2" combos/c1-haiku-luna'
echo C1_DRIVER_DONE
