#!/usr/bin/env bash
# usage: revstart.sh Tn <pairs-file>  (pairs-file: python file defining PAIRS=[(new,old),...]) 
# Build a Q0 start tree from HEAD + working tree, with the design file reverted for edits already made. Records start line once.
set -u
R=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
D=$R/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
SLUG=task-rf-sweep-phase1-202-c7ea3265
id=$1; pairs=$2; M=docs/designs/orchestrator-mode.md
cd $R
grep -qE "^$id: start sha=" $D/progress.md && { echo exists; exit 0; }
tmp=$(mktemp)
uv run python - "$pairs" "$M" "$tmp" <<'PY'
import sys, runpy
ns = runpy.run_path(sys.argv[1]); text = open(sys.argv[2], encoding="utf-8").read()
for new, old in ns["PAIRS"]:
    assert text.count(new) == 1, ("not unique or missing", new[:60])
    text = text.replace(new, old)
open(sys.argv[3], "w", encoding="utf-8").write(text)
PY
[ $? -eq 0 ] || { echo "revert failed"; exit 1; }
blob=$(git hash-object -w $tmp)
idx=$(mktemp)
GIT_INDEX_FILE="$idx" git read-tree HEAD && GIT_INDEX_FILE="$idx" git add -A && GIT_INDEX_FILE="$idx" git update-index --add --cacheinfo 100644,$blob,$M && start=$(GIT_INDEX_FILE="$idx" git write-tree)
rm -f "$idx" "$tmp"
git update-ref "refs/superclaude/implement/$SLUG/$id" "$start"
mkdir -p $D/retries/$id; git rev-parse HEAD > $D/retries/$id/q0-head
printf '%s: start sha=%s\n' "$id" "$start" >> $D/progress.md
tail -1 $D/progress.md
