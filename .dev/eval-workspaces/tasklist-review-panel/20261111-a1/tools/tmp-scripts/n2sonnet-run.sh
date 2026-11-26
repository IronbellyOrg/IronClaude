#!/usr/bin/env bash
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
mkdir -p $EVAL/combos/n2-sonnet
for p in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
 for r in "t1b-1 claude-sonnet-5-5" "t2b-1 muse-wonder-1.0" "t4-1 claude-haiku-5-5" "t4-2 grok-4.7"; do echo "$p $r"; done
done | xargs -P 2 -L 1 bash -c 'bash '$EVAL'/tools/run-reviewer.sh '$EVAL' "$0" "$1" "$2" combos/n2-sonnet; echo "done $0 $1 rc=$?"' 
echo ALLDONE
