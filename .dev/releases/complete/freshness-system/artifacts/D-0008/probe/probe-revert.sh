#!/usr/bin/env bash
# Restore the production freshness-file-changed.sh after probing.

set -euo pipefail

REAL="$HOME/.claude/hooks/freshness-file-changed.sh"
BACKUP="$HOME/.claude/hooks/freshness-file-changed.sh.real"

if [ ! -f "$BACKUP" ]; then
    echo "ERROR: backup $BACKUP not found — nothing to revert from." >&2
    echo "Re-install with 'superclaude install --force' to restore the real handler." >&2
    exit 1
fi

mv "$BACKUP" "$REAL"
chmod +x "$REAL"
echo "✓ Restored real freshness-file-changed.sh from backup."

# Show captured probe rows
LOGDIR="$HOME/.claude/logs"
PROBES=$(ls -1 "$LOGDIR"/file-changed-probe-*.json 2>/dev/null | wc -l)
if [ "$PROBES" -gt 0 ]; then
    echo ""
    echo "Captured $PROBES probe row(s) at $LOGDIR/file-changed-probe-*.json"
    echo "Example contents (first probe):"
    head -c 500 "$(ls -1t $LOGDIR/file-changed-probe-*.json | head -1)" 2>/dev/null
    echo ""
    echo ""
    echo "Field names captured (jq keys):"
    jq -r 'keys[]' "$(ls -1t $LOGDIR/file-changed-probe-*.json | head -1)" 2>/dev/null || echo "(probe payload wasn't valid JSON — inspect manually)"
fi
