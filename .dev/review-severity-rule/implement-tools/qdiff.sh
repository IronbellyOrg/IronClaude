#!/usr/bin/env bash
# /sc:implement Q2 diff. Usage (repo root): qdiff.sh <task-number> <k> <j>
# Pins the reviewed tree as r<k>-<j>, writes the diff of every changed path under src/ plugins/ tests/ CHANGELOG.md
# (tracked changes vs the start tree, plus new untracked files in full) to artifacts/diffs/T<id>-r<k>-<j>.diff,
# and prints: reviewed-tree sha, diff path, touched files.
set -euo pipefail
id="T$1"; k=$2; j=$3
S=TASK-WF-removeTheAnyIssu-20261102-053741
P=.dev/tasks/to-do/$S
start=$(grep "^$id: start sha=" "$P/progress.md" | tail -1 | sed 's/.*sha=//')
idx=$(mktemp)
GIT_INDEX_FILE="$idx" git read-tree HEAD
GIT_INDEX_FILE="$idx" git add -A
tree=$(GIT_INDEX_FILE="$idx" git write-tree)
rm -f "$idx"
git update-ref "refs/superclaude/implement/$S/retry/$id/r$k-$j" "$tree"
out="$P/artifacts/diffs/$id-r$k-$j.diff"
git diff "$start" "$tree" -- src plugins tests CHANGELOG.md > "$out"
echo "tree=$tree"
echo "diff=$out ($(wc -l < "$out") lines)"
echo "files=$(git diff --name-only "$start" "$tree" -- src plugins tests CHANGELOG.md | paste -sd, -)"
