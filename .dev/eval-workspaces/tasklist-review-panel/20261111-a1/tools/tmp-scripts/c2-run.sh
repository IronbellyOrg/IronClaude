#!/usr/bin/env bash
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
printf '%s\n' \
 "TASK-WF-designSpec-20261107-075614 t4-1 claude-haiku-5-5" \
 "TASK-WF-designSpec-20261107-075614 t4-2 grok-4.7" \
 "TASK-WF-makeTheAliasOnly-20261105-051649 t4-1 claude-haiku-5-5" \
 "TASK-WF-makeTheAliasOnly-20261105-051649 t4-2 grok-4.7" \
 "TASK-WF-design-20261108-041415 t4-1 claude-haiku-5-5" \
 "TASK-WF-design-20261108-041415 t4-2 grok-4.7" |
 xargs -P2 -L1 bash -c 'bash '"$EVAL"'/tools/run-reviewer.sh '"$EVAL"' $0 $1 $2 combos/c2-haiku-grok'
echo ALL_DONE
