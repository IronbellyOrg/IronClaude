#!/usr/bin/env bash
# Build the task brief file: usage brief.sh T12 "<AC text or 'title'>"   -> prints path of $D/work/T12/brief.txt
# AC1 defaults to the item title (QUALIFY rule 4). Pass a second argument to override AC text.
set -u
R=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
D=$R/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
F=$R/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
id=$1; ac=${2:-}
start_line=$(awk -F'\t' -v t="$id" '$1==t{print $3}' "$D/item-map.tsv")
lab=$(awk -F'\t' -v t="$id" '$1==t{print $2}' "$D/item-map.tsv")
# end = line before the next checkbox item, phase heading, or END PHASE comment
end_line=$(awk -v s="$start_line" 'NR>s && (/^- \[[ x]\] \*\*[0-9]+\.[0-9]+ / || /^## / || /^<!-- END PHASE/){print NR-1; exit}' "$F")
mkdir -p "$D/work/$id"
title=$(sed -n "${start_line}p" "$F" | sed -E 's/^- \[[ x]\] \*\*[0-9]+\.[0-9]+ — (.*)\*\*$/\1/')
[ -n "$ac" ] || ac="the item title \"$title\" (no AC block; the title is the AC)"
{
  echo "$id = item $lab of the source file $F (lines $start_line-$end_line). Item text:"
  sed -n "${start_line},${end_line}p" "$F" | sed -e 's/^- \[x\] /- [ ] /' | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}'
  echo "AC ids: $id.AC1 = $ac. The item's own Verification and Completion gate lines are context for what \"done\" means. Ticking the item's checkbox is done by the orchestrator after the verdict and is not part of the diff under review."
} > "$D/work/$id/brief.txt"
echo "$D/work/$id/brief.txt"
