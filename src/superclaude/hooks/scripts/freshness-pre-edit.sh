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
    # NFR-3 fail-open: a Write/Edit to a path that does not yet exist is a
    # create, not an edit. The freshness gate is meaningless when there is
    # no prior state to be stale relative to. Resolves F10 from
    # .dev/releases/complete/freshness-system/checkpoints/CP-P05-T05.01.md.
    if [ ! -e "$TARGET" ]; then
        DECISION="allow"
        REASON="create_allowed"
    else
        DECISION="block"
        REASON="no_prior_read"
    fi
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
    AVOIDANCE_WARN="DO NOT pivot to mdformat / prettier / sed -i / awk-with-redirect / a Python helper / any other tool that bypasses the Edit pathway. Strategy pivots that escape freshness checks are an avoidance anti-pattern — they introduce uncontrolled diffs, lose the surgical-Edit property, and defeat the safety reason this hook exists (stale citations + wrong line numbers). Re-reading is bounded: one Read call, ~2K tokens, ~1 second. Just Read."
    case "$REASON" in
        no_prior_read)
            echo "FRESHNESS BLOCK: You have not Read \`$TARGET\` in this session. Required action: Read the file (one tool call), then retry your Edit." >&2
            echo "$AVOIDANCE_WARN" >&2 ;;
        read_too_old)
            echo "FRESHNESS BLOCK: You last Read \`$TARGET\` ${READ_AGE}s ago, beyond the 30-minute freshness horizon. Required action: Re-Read the file (one tool call), then retry your Edit." >&2
            echo "$AVOIDANCE_WARN" >&2 ;;
        external_change)
            echo "FRESHNESS BLOCK: \`$TARGET\` was modified after your last Read (mtime change detected). Required action: Re-Read the file (one tool call), then retry your Edit." >&2
            echo "DO NOT pivot to mdformat / prettier / sed -i / a Python helper. The file changed on disk — anything other than Re-Read will edit stale content." >&2 ;;
        *)
            echo "FRESHNESS BLOCK on \`$TARGET\` (gate: $REASON). Required action: Re-Read, then retry your Edit. DO NOT pivot to bulk-reformat tools (mdformat / prettier / sed -i / scripts) to escape this hook." >&2 ;;
    esac
    exit 2
fi

exit 0
