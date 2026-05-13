#!/usr/bin/env bash
# SubagentStop counter (decrement, floored at 0) per design §3.6. async:true. Fail-open.

set -u

STATE_DIR="$HOME/.claude/state"
mkdir -p "$STATE_DIR/bg-agents" 2>/dev/null || true

INPUT="$(cat 2>/dev/null || true)"
SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
BG_FILE="$STATE_DIR/bg-agents/$SESSION_ID.txt"

(
    if command -v flock >/dev/null 2>&1; then
        exec 9>"$BG_FILE.lock"
        # Block until lock acquired (critical section is microseconds; no deadlock risk).
        # Skip update entirely if flock errors — fail-open per NFR-3.
        flock 9 2>/dev/null || exit 0
    fi
    cur=0
    [ -f "$BG_FILE" ] && cur=$(cat "$BG_FILE" 2>/dev/null || echo 0)
    case "$cur" in ''|*[!0-9]*) cur=0 ;; esac
    if [ "$cur" -gt 0 ]; then
        echo $((cur - 1)) > "$BG_FILE" 2>/dev/null || true
    else
        echo "0" > "$BG_FILE" 2>/dev/null || true
    fi
) 2>/dev/null || true

exit 0
