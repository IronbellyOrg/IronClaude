#!/usr/bin/env bash
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
while read -r p r m; do echo "$p $r $m"; done < /tmp/n5s-jobs.txt | xargs -P 2 -L 1 bash -c 'bash /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1 "$0" "$1" "$2" combos/n5-sonnet; echo DONE $0 $1'
echo ALL_DONE
