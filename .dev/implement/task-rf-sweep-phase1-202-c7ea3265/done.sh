#!/usr/bin/env bash
# Complete one task: usage done.sh T12 "<ev-list>" "<file-list>" ["lint:skip,typecheck:skip,test:skip"]
# Appends the compliant complete line, ticks the item's checkbox in the source, deletes the Q0 pin.
set -u
R=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
D=$R/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
SLUG=task-rf-sweep-phase1-202-c7ea3265
F=$R/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
id=$1; ev=$2; files=$3; extras=${4:-lint:skip,typecheck:skip,test:skip}
cd "$R" || exit 1
line="$id: complete verdict=compliant ac=$id.AC1 evidence=$ev extras=$extras files=$files"
re='^T([0-9A-Za-z.-]+): (complete|blocked) verdict=(compliant|missing|extra|misunderstood|cannot-verify) ac=([^ ]+) evidence=(.+) extras=lint:(pass|fail|skip),typecheck:(pass|fail|skip),test:(pass|fail|skip|unrelated-red) files=(.+)$'
[[ $line =~ $re ]] || { echo "LEDGER LINE FAILS REGEX: $line"; exit 2; }
printf '%s\n' "$line" >> "$D/progress.md"
lab=$(awk -v t="$id" -F'\t' '$1==t{print $2}' "$D/item-map.tsv")
esc=${lab//./\\.}
sed -i "s/^- \[ \] \*\*$esc /- [x] **$lab /" "$F"
git update-ref -d "refs/superclaude/implement/$SLUG/$id" 2>/dev/null
# also drop the reviewed-tree refs r<k>-<j> of this task (retry/ folder is kept)
for r in $(git for-each-ref --format='%(refname)' "refs/superclaude/implement/$SLUG/retry/$id/"); do git update-ref -d "$r"; done
tail -1 "$D/progress.md"
grep -c "^- \[x\] \*\*$esc " "$F"
