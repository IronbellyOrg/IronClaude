#!/usr/bin/env bash
# PreToolUse(Edit-class) freshness gate per design §3.3.
# Decision: allow (exit 0) | block (stderr + exit 2). NEVER exit 1 (NFR-10).
# Fail-open per NFR-3: state missing/corrupt → log to stderr, exit 0.

set -u

STATE_DIR="$HOME/.claude/state"
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$STATE_DIR/tool-call-counter" "$LOG_DIR" 2>/dev/null || true

READS_FILE="$STATE_DIR/reads.jsonl"
CHANGES_FILE="$STATE_DIR/changes.jsonl"
TELEMETRY="$LOG_DIR/freshness-hook.jsonl"
FRESH_HORIZON=1800   # 30 min per DQ-3

INPUT="$(cat 2>/dev/null || true)"
SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // "unknown"' 2>/dev/null || echo "unknown")
CWD=$(printf '%s' "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
[ -z "${CWD:-}" ] && CWD="$PWD"

# 2. Extract target_path
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
REL_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.relative_path // empty' 2>/dev/null)
TARGET=""
if [ -n "$FILE_PATH" ]; then
    TARGET="$FILE_PATH"
elif [ -n "$REL_PATH" ]; then
    case "$REL_PATH" in
        /*) TARGET="$REL_PATH" ;;
        *)  TARGET="$CWD/$REL_PATH" ;;
    esac
else
    # Cannot enforce on this tool variant — fail open.
    echo "freshness-pre-edit: no file_path/relative_path in tool_input for $TOOL_NAME; allowing." >&2
    exit 0
fi

NOW_ISO=$(date -Iseconds 2>/dev/null || date "+%Y-%m-%dT%H:%M:%S")
NOW_UNIX=$(date +%s 2>/dev/null || echo 0)

# 3. Increment tool-call-counter atomically; emit new value to per-process tempfile
# so the outer scope reads THIS invocation's idx, not a later-race value.
TCC_FILE="$STATE_DIR/tool-call-counter/$SESSION_ID.txt"
TCC_TMP=$(mktemp 2>/dev/null || echo "/tmp/tcc-$$-$RANDOM.txt")
TC_IDX=1
(
    if command -v flock >/dev/null 2>&1; then
        exec 9>"$TCC_FILE.lock"
        flock 9 2>/dev/null || exit 0
    fi
    prev=0
    [ -f "$TCC_FILE" ] && prev=$(cat "$TCC_FILE" 2>/dev/null || echo 0)
    case "$prev" in ''|*[!0-9]*) prev=0 ;; esac
    new=$((prev + 1))
    echo "$new" > "$TCC_FILE" 2>/dev/null || true
    echo "$new" > "$TCC_TMP" 2>/dev/null || true
) 2>/dev/null || true
[ -f "$TCC_TMP" ] && TC_IDX=$(cat "$TCC_TMP" 2>/dev/null || echo 1)
rm -f "$TCC_TMP" 2>/dev/null || true

# 4. Look up most recent Read of TARGET for this session
LAST_READ_TS_UNIX=0
if [ -f "$READS_FILE" ]; then
    LAST_READ_TS_UNIX=$(jq -r --arg p "$TARGET" --arg s "$SESSION_ID" \
        'select(.path == $p and .session_id == $s) | .ts_unix' "$READS_FILE" 2>/dev/null \
        | sort -n | tail -1)
    [ -z "$LAST_READ_TS_UNIX" ] && LAST_READ_TS_UNIX=0
fi

DECISION="allow"
REASON="recent_read"
READ_AGE="null"

if [ "$LAST_READ_TS_UNIX" -le 0 ] 2>/dev/null; then
    DECISION="block"
    REASON="no_prior_read"
else
    # 5. Δ
    DELTA=$((NOW_UNIX - LAST_READ_TS_UNIX))
    READ_AGE="$DELTA"
    if [ "$DELTA" -gt "$FRESH_HORIZON" ]; then
        DECISION="block"
        REASON="read_too_old"
    else
        # 7. external_change check
        if [ -f "$CHANGES_FILE" ]; then
            CHANGED_AFTER=$(jq -r --arg p "$TARGET" --argjson t "$LAST_READ_TS_UNIX" \
                'select(.path == $p and .ts_unix > $t) | .path' "$CHANGES_FILE" 2>/dev/null | head -1)
            if [ -n "$CHANGED_AFTER" ]; then
                DECISION="block"
                REASON="external_change"
            fi
        fi
    fi
fi

# 9. Telemetry
EXT_SEEN=false
[ "$REASON" = "external_change" ] && EXT_SEEN=true
{
    jq -nc \
        --arg ts "$NOW_ISO" --arg tool "$TOOL_NAME" --arg path "$TARGET" \
        --arg sid "$SESSION_ID" --argjson idx "$TC_IDX" \
        --arg age "$READ_AGE" --argjson ext "$EXT_SEEN" \
        --arg dec "$DECISION" --arg rsn "$REASON" \
        '{ts:$ts, event:"PreToolUse", tool:$tool, path:$path, session_id:$sid, tool_call_idx:$idx, recent_read_age_sec:($age|if . == "null" then null else (tonumber? // null) end), external_change_seen:$ext, decision:$dec, reason:$rsn}' \
        2>/dev/null
} >> "$TELEMETRY" 2>/dev/null || true

# 10. Block or allow
if [ "$DECISION" = "block" ]; then
    case "$REASON" in
        no_prior_read)
            echo "You have not Read \`$TARGET\` in this session. Read it before editing." >&2 ;;
        read_too_old)
            echo "You last Read \`$TARGET\` ${READ_AGE}s ago, beyond the 30-minute freshness horizon. Re-Read before editing." >&2 ;;
        external_change)
            echo "\`$TARGET\` was modified after your last Read (mtime change detected). Re-Read before editing." >&2 ;;
        *)
            echo "Re-Read \`$TARGET\` before editing (freshness gate: $REASON)." >&2 ;;
    esac
    exit 2
fi

exit 0
