#!/usr/bin/env bash
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
for p in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
  for r in t3-1:glm-5.3 t2b-1:muse-wonder-1.0 t2-1:gpt-6.1-terra t4-1:gpt-6-luna; do
    echo "$p ${r%%:*} ${r#*:}"
  done
done | xargs -P2 -L1 bash -c 'bash '"$EVAL"'/tools/run-reviewer.sh '"$EVAL"' "$0" "$1" "$2" combos/n5-terra; echo "done $0 $1 rc=$?"'
echo ALL_DONE
