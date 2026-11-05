#!/usr/bin/env bash
# /sc:implement Q7 for a compliant task. Usage (repo root):
#   qdone.sh <task-number> <ac-list> <evidence-list> <lint> <typecheck> <test> <files>
# Appends the complete line, then deletes the Q0 pin and the task's r<k>-<j> refs (sweep refs are kept).
set -euo pipefail
n=$1; id="T$n"
S=TASK-WF-removeTheAnyIssu-20261102-053741
P=.dev/tasks/to-do/$S
line="$id: complete verdict=compliant ac=$2 evidence=$3 extras=lint:$4,typecheck:$5,test:$6 files=$7"
echo "$line" | grep -qE '^T([0-9A-Za-z.-]+): (complete|blocked) verdict=(compliant|missing|extra|misunderstood|cannot-verify) ac=([^ ]+) evidence=(.+) extras=lint:(pass|fail|skip),typecheck:(pass|fail|skip),test:(pass|fail|skip|unrelated-red) files=(.+)$' \
  || { echo "BAD LINE: $line"; exit 1; }
echo "$line" >> "$P/progress.md"
git update-ref -d "refs/superclaude/implement/$S/$id" 2>/dev/null || true
git for-each-ref --format='%(refname)' "refs/superclaude/implement/$S/retry/$id/" | while read -r r; do git update-ref -d "$r"; done
tail -1 "$P/progress.md"
