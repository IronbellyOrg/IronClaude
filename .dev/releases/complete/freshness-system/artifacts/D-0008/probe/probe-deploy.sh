#!/usr/bin/env bash
# Deploy a probe handler that captures FileChanged stdin shape.
# Backs up the production handler first; run probe-revert.sh to restore.

set -euo pipefail

REAL="$HOME/.claude/hooks/freshness-file-changed.sh"
BACKUP="$HOME/.claude/hooks/freshness-file-changed.sh.real"
LOGDIR="$HOME/.claude/logs"

if [ ! -f "$REAL" ]; then
    echo "ERROR: $REAL not found — run 'superclaude install --force' first." >&2
    exit 1
fi

mkdir -p "$LOGDIR"

# Backup real handler ONCE (don't overwrite if backup already exists).
if [ ! -f "$BACKUP" ]; then
    cp "$REAL" "$BACKUP"
    chmod +x "$BACKUP"
fi

# Install probe
cat > "$REAL" <<'PROBE'
#!/usr/bin/env bash
# PROBE: capture FileChanged stdin to ~/.claude/logs/file-changed-probe-<ts>.json
TS=$(date +%s%N)
cat - > "$HOME/.claude/logs/file-changed-probe-${TS}.json"
exit 0
PROBE
chmod +x "$REAL"

echo "✓ Probe deployed at $REAL"
echo "✓ Real handler backed up to $BACKUP"
echo ""
echo "Next: in a FRESH Claude Code session, edit a file Claude has Read."
echo "Probe output will land at: $LOGDIR/file-changed-probe-*.json"
echo ""
echo "When done, run probe-revert.sh to restore the real handler."
