#!/usr/bin/env bash
# PostToolUse: clear auggie-first sticky after any mcp__auggie__* tool call.
# auggie-first-hook-proposal-v2.1.md §6 — synchronous (no async:true) per spec-panel Wh-8.
# Fail-open per NFR-3.
set -u

[ "${AUGGIE_FIRST_DISABLE:-0}" = "1" ] && exit 0

STATE_DIR="$HOME/.claude/state"
LOG_DIR="$HOME/.claude/logs"
AUGGIE_LOG="$LOG_DIR/auggie-first.jsonl"
INPUT="$(cat 2>/dev/null || true)"

SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || true)

# Sentinel guard: never operate on the "unknown" bucket (collision risk per Wh-1/Wh-6).
[ "$SESSION_ID" = "unknown" ] && exit 0
[ -z "$SESSION_ID" ] && exit 0

case "$TOOL_NAME" in
    mcp__auggie__*)
        STICKY="$STATE_DIR/auggie-first-pending/$SESSION_ID.txt"
        if [ -f "$STICKY" ]; then
            rm -f "$STICKY" 2>/dev/null || true
            NOW_ISO=$(date -Iseconds 2>/dev/null || date "+%Y-%m-%dT%H:%M:%S")
            printf '{"ts":"%s","session_id":"%s","event":"sticky_cleared","tool":"%s"}\n' \
                "$NOW_ISO" "$SESSION_ID" "$TOOL_NAME" >> "$AUGGIE_LOG" 2>/dev/null || true
        fi
        ;;
esac
exit 0
