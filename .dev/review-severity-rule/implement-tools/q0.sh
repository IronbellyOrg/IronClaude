#!/usr/bin/env bash
# /sc:implement Q0 for one task of the managed package. Usage (repo root): q0.sh <task-number>
# Snapshots HEAD + worktree (tracked + untracked, non-ignored) into a tree without touching the user index,
# pins it, writes q0-head, then appends the start line. Prints the start sha.
set -euo pipefail
id="T$1"
S=TASK-WF-removeTheAnyIssu-20261102-053741
P=.dev/tasks/to-do/$S
if grep -q "^$id: start sha=" "$P/progress.md"; then
  grep "^$id: start sha=" "$P/progress.md" | tail -1 | sed 's/.*sha=//'; exit 0
fi
idx=$(mktemp)
GIT_INDEX_FILE="$idx" git read-tree HEAD
GIT_INDEX_FILE="$idx" git add -A
start=$(GIT_INDEX_FILE="$idx" git write-tree)
rm -f "$idx"
git update-ref "refs/superclaude/implement/$S/$id" "$start"
mkdir -p "$P/artifacts/retries/$id"
git rev-parse HEAD > "$P/artifacts/retries/$id/q0-head"
echo "$id: start sha=$start" >> "$P/progress.md"
echo "$start"
