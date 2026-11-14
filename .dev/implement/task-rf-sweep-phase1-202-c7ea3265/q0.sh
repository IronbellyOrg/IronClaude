#!/usr/bin/env bash
# Q0 snapshot for one task id (usage: q0.sh T12). Writes q0-head, pins the tree, appends the start line once.
set -u
R=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
D=$R/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
SLUG=task-rf-sweep-phase1-202-c7ea3265
id=$1
cd "$R" || exit 1
if grep -qE "^$id: start sha=" "$D/progress.md"; then
  grep -E "^$id: start sha=" "$D/progress.md" | tail -1
  exit 0
fi
mkdir -p "$D/retries/$id"
idx=$(mktemp)
start=""
if GIT_INDEX_FILE="$idx" git read-tree HEAD && GIT_INDEX_FILE="$idx" git add -A && start=$(GIT_INDEX_FILE="$idx" git write-tree); then
  rm -f "$idx"
  git update-ref "refs/superclaude/implement/$SLUG/$id" "$start"
  git rev-parse HEAD > "$D/retries/$id/q0-head"
else
  rm -f "$idx"
  start=$(git rev-parse HEAD 2>/dev/null) || start=nogit
fi
printf '%s: start sha=%s\n' "$id" "$start" >> "$D/progress.md"
tail -1 "$D/progress.md"
