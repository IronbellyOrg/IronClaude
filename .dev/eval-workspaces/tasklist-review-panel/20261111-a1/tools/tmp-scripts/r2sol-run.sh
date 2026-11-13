#!/usr/bin/env bash
xargs -P2 -L1 bash -c 'bash /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1 $0 $1 $2 combos/r2-sol; echo done $0 $1' < /tmp/r2sol-jobs.txt
echo ALLDONE
