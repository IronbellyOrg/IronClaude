#!/usr/bin/env bash
# Print the comma-joined touched files of task N (start tree vs current worktree tree). Usage: capfiles.sh <n>
set -euo pipefail
S=TASK-WF-removeTheAnyIssu-20261102-053741
start=$(grep "^T$1: start sha=" ".dev/tasks/to-do/$S/progress.md" | tail -1 | sed 's/.*sha=//')
idx=$(mktemp); GIT_INDEX_FILE="$idx" git read-tree HEAD; GIT_INDEX_FILE="$idx" git add -A
tree=$(GIT_INDEX_FILE="$idx" git write-tree); rm -f "$idx"
git diff --name-only "$start" "$tree" -- src plugins tests CHANGELOG.md | paste -sd, -
