#!/usr/bin/env bash
# Q2 diff for a task against its Q0 snapshot tree, tracked or untracked alike.
# usage: mkdiff.sh T12 path [path...]  -> writes work/T12/diff.txt and prints its path and size
# Per path: unified diff of `git show <start>:path` (or empty if absent in the snapshot) against the working file.
# Paths that are directories are expanded with find -type f. Large new files are summarized with a head, see MAXNEW.
set -u
R=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
D=$R/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
MAXNEW=${MAXNEW:-400}
id=$1; shift
cd "$R" || exit 1
start=$(grep -E "^$id: start sha=" "$D/progress.md" | tail -1 | sed 's/.*sha=//')
# BASE_TREE=<tree> OUTNAME=<file> give a delta diff from a pinned reviewed tree instead of the start snapshot
start=${BASE_TREE:-$start}
mkdir -p "$D/work/$id"
out=$D/work/$id/${OUTNAME:-diff.txt}
: > "$out"
tmp=$(mktemp)
for p in "$@"; do
  if [ -d "$p" ]; then files=$(find "$p" -type f | sort); else files=$p; fi
  for f in $files; do
    if git cat-file -e "$start:$f" 2>/dev/null; then
      git show "$start:$f" > "$tmp"
      if [ -e "$f" ]; then diff -u --label "a/$f" --label "b/$f" "$tmp" "$f" >> "$out"; else echo "deleted: $f" >> "$out"; fi
    elif [ -e "$f" ]; then
      n=$(wc -l < "$f")
      echo "--- /dev/null" >> "$out"; echo "+++ b/$f   (new file, $n lines)" >> "$out"
      if [ "$n" -le "$MAXNEW" ]; then sed 's/^/+/' "$f" >> "$out"; else sed -n "1,${MAXNEW}p" "$f" | sed 's/^/+/' >> "$out"; echo "... (new file continues; read $f from disk for lines $((MAXNEW+1))-$n)" >> "$out"; fi
    else
      echo "missing: $f" >> "$out"
    fi
  done
done
rm -f "$tmp"
echo "$out $(wc -c < "$out") bytes"
