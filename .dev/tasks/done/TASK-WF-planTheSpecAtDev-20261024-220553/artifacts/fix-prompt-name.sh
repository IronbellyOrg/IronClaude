#!/bin/bash
# Rename the stale saved-prompt name `prompt-<k>.md` to `prompt-<k>-<j>.md`
# in the four files FINAL flagged. Usage: fix-prompt-name.sh [--dry-run]
set -u -o pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1
FILES=(
  src/superclaude/skills/sc-implement-protocol/refs/qa.md
  src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
  plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
  plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
)
OLD='prompt-<k>.md'
NEW='prompt-<k>-<j>.md'
rc=0
for f in "${FILES[@]}"; do
  n=$(grep -cF "$OLD" "$f")
  if [ "$n" -ne 1 ]; then echo "FAIL $f: expected 1 hit, found $n"; rc=1; continue; fi
  if [ "${1:-}" = "--dry-run" ]; then
    sed "s/prompt-<k>\.md/prompt-<k>-<j>.md/" "$f" | diff "$f" - ; echo "DRY $f: 1 line would change"
  else
    sed -i "s/prompt-<k>\.md/prompt-<k>-<j>.md/" "$f"
    left=$(grep -cF "$OLD" "$f"); echo "DONE $f: remaining old=$left"
    [ "$left" -eq 0 ] || rc=1
  fi
done
exit $rc
