#!/usr/bin/env bash
# SubagentStart counter + Bash inspection policy injection. Synchronous, fail-open.

set -u

STATE_DIR="$HOME/.claude/state"
POLICY_FILE="$HOME/.claude/BASH_INSPECTION_POLICY.md"
mkdir -p "$STATE_DIR/bg-agents" 2>/dev/null || true

INPUT="$(cat 2>/dev/null || true)"
SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
case "$SESSION_ID" in
    ""|*[!A-Za-z0-9._-]*) SESSION_ID="unknown" ;;
esac
BG_FILE="$STATE_DIR/bg-agents/$SESSION_ID.txt"

(
    if command -v flock >/dev/null 2>&1; then
        exec 9>"$BG_FILE.lock"
        # The hook is synchronous so lock contention must not delay agent startup.
        flock -w 0.2 9 2>/dev/null || exit 0
    fi
    cur=0
    [ -f "$BG_FILE" ] && cur=$(cat "$BG_FILE" 2>/dev/null || echo 0)
    case "$cur" in ''|*[!0-9]*) cur=0 ;; esac
    echo $((cur + 1)) > "$BG_FILE" 2>/dev/null || true
) 2>/dev/null || true

# additionalContext must be valid hook JSON. Missing dependencies fail open.
if command -v jq >/dev/null 2>&1 && [ -r "$POLICY_FILE" ]; then
    jq -nc --rawfile policy "$POLICY_FILE" \
        '{hookSpecificOutput:{hookEventName:"SubagentStart",additionalContext:$policy}}' \
        2>/dev/null || true
fi

exit 0
