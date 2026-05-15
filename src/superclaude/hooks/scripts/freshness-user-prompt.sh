#!/usr/bin/env bash
# UserPromptSubmit hook per design §3.2.
# Per-turn envelope with conditional items + truncation (token-budget-check §3).
# Fail-open per NFR-3: always emit at least baseline envelope.

set -u

STATE_DIR="$HOME/.claude/state"
LOG_DIR="$HOME/.claude/logs"
AUGGIE_LOG="$LOG_DIR/auggie-first.jsonl"
AUGGIE_THRESHOLD_S=10800
AUGGIE_WARN_MAX_LEN=300
mkdir -p "$STATE_DIR/turns" "$STATE_DIR/last-prompt-ts" "$STATE_DIR/bg-agents" \
         "$STATE_DIR/tool-call-counter" "$STATE_DIR/auggie-first-pending" \
         "$STATE_DIR/auggie-no-warn" "$LOG_DIR" 2>/dev/null || true
if [ -n "${AUGGIE_FIRST_THRESHOLD:-}" ]; then
    case "$AUGGIE_FIRST_THRESHOLD" in (*[!0-9]*|"") ;; (*) AUGGIE_THRESHOLD_S="$AUGGIE_FIRST_THRESHOLD" ;; esac
fi

INPUT="$(cat 2>/dev/null || true)"
SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
CWD=$(printf '%s' "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
[ -z "${CWD:-}" ] && CWD="$PWD"
PERM_MODE=$(printf '%s' "$INPUT" | jq -r '.permission_mode // "default"' 2>/dev/null || echo "default")

NOW_ISO=$(date -Iseconds 2>/dev/null || date "+%Y-%m-%dT%H:%M:%S")
NOW_UNIX=$(date +%s 2>/dev/null || echo 0)

# 1. Turn counter (flocked)
TURN_FILE="$STATE_DIR/turns/$SESSION_ID.txt"
TURN=1
(
    if command -v flock >/dev/null 2>&1; then
        exec 9>"$TURN_FILE.lock"
        flock 9 2>/dev/null || exit 0
    fi
    if [ -f "$TURN_FILE" ]; then
        prev=$(cat "$TURN_FILE" 2>/dev/null || echo 0)
        TURN_CALC=$((prev + 1))
    else
        TURN_CALC=1
    fi
    echo "$TURN_CALC" > "$TURN_FILE" 2>/dev/null || true
) 2>/dev/null || true
[ -f "$TURN_FILE" ] && TURN=$(cat "$TURN_FILE" 2>/dev/null || echo 1)

# 2. Δ since last prompt
LP_FILE="$STATE_DIR/last-prompt-ts/$SESSION_ID.txt"
DELTA_SEC=""
if [ -f "$LP_FILE" ]; then
    last_ts=$(cat "$LP_FILE" 2>/dev/null || true)
    if [ -n "$last_ts" ]; then
        last_unix=$(date -d "$last_ts" +%s 2>/dev/null || echo 0)
        if [ "$last_unix" -gt 0 ] && [ "$NOW_UNIX" -gt 0 ]; then
            DELTA_SEC=$((NOW_UNIX - last_unix))
        fi
    fi
fi
echo "$NOW_ISO" > "$LP_FILE" 2>/dev/null || true

# 3. Bg-agents count
BG_FILE="$STATE_DIR/bg-agents/$SESSION_ID.txt"
BG_COUNT=0
[ -f "$BG_FILE" ] && BG_COUNT=$(cat "$BG_FILE" 2>/dev/null || echo 0)

# 4. Git dirty probe
GIT_INFO=""
if (cd "$CWD" 2>/dev/null && git rev-parse --git-dir >/dev/null 2>&1); then
    branch=$(cd "$CWD" && git branch --show-current 2>/dev/null || true)
    porcelain_output=$(cd "$CWD" && git status --porcelain 2>/dev/null || true)
    modified=$(printf '%s\n' "$porcelain_output" | grep -E -c '^.M| M|^M ' 2>/dev/null)
    [ -z "$modified" ] && modified=0
    untracked=$(printf '%s\n' "$porcelain_output" | grep -c '^??' 2>/dev/null)
    [ -z "$untracked" ] && untracked=0
    total=$(printf '%s\n' "$porcelain_output" | grep -v '^$' | wc -l | tr -d ' ')
    [ -z "$total" ] && total=0
    if [ "$total" -gt 0 ] && [ -n "$branch" ]; then
        GIT_INFO="git=$branch dirty=${modified}M/${untracked}U"
    fi
fi

# 5. Consume changes.jsonl: collect distinct paths, then truncate (flocked)
CHANGES_FILE="$STATE_DIR/changes.jsonl"
CHANGED_PATHS=""
CHANGED_COUNT=0
if [ -f "$CHANGES_FILE" ]; then
    (
        if command -v flock >/dev/null 2>&1; then
            exec 8>"$CHANGES_FILE.lock"
            flock 8 2>/dev/null || exit 0
        fi
        CHANGED_PATHS_LOCAL=$(jq -r '.path // empty' "$CHANGES_FILE" 2>/dev/null | awk 'NF && !seen[$0]++' | head -200)
        printf '%s' "$CHANGED_PATHS_LOCAL" > "$CHANGES_FILE.tmp" 2>/dev/null
        : > "$CHANGES_FILE" 2>/dev/null || true
    ) 2>/dev/null || true
    CHANGED_PATHS=$(cat "$CHANGES_FILE.tmp" 2>/dev/null || true)
    rm -f "$CHANGES_FILE.tmp" 2>/dev/null || true
    CHANGED_COUNT=$(printf '%s\n' "$CHANGED_PATHS" | grep -v '^$' | wc -l | tr -d ' ')
    [ -z "$CHANGED_COUNT" ] && CHANGED_COUNT=0
fi

# 6. Conditional items
ITEMS=""
if [ -n "$DELTA_SEC" ] && [ "$DELTA_SEC" -ge 300 ] 2>/dev/null; then
    if [ "$DELTA_SEC" -ge 3600 ]; then
        h=$((DELTA_SEC / 3600))
        m=$(((DELTA_SEC % 3600) / 60))
        s=$((DELTA_SEC % 60))
        DELTA_FMT=$(printf '%02d:%02d:%02d' "$h" "$m" "$s")
    else
        m=$((DELTA_SEC / 60))
        s=$((DELTA_SEC % 60))
        DELTA_FMT=$(printf '%02d:%02d' "$m" "$s")
    fi
    ITEMS+="Δ=$DELTA_FMT "
fi
if [ "$PERM_MODE" != "default" ]; then
    ITEMS+="mode=$PERM_MODE "
fi
if [ -n "$GIT_INFO" ]; then
    ITEMS+="$GIT_INFO "
fi
if [ "$BG_COUNT" -gt 0 ] 2>/dev/null; then
    ITEMS+="bg=$BG_COUNT "
fi

# 6.5. Auggie-first flag (auggie-first-hook-proposal-v2.1.md)
# Q1: fire on sticky OR Δ≥AUGGIE_THRESHOLD_S. Q2: jq -e on .mcpServers.
# Q3: indexed → full nag; unindexed → one-time warn. Q5: matcher mcp__auggie__.* clears sticky.
# Q6: highest priority, never truncated. Q7: AUGGIE_FIRST_DISABLE=1 short-circuits.
AUGGIE_FLAG=""
AUGGIE_WARN=""

if [ "${AUGGIE_FIRST_DISABLE:-0}" != "1" ] \
   && [ "$SESSION_ID" != "unknown" ] && [ -n "$SESSION_ID" ]; then

    CWD_NORM="${CWD%/}"
    [ -z "$CWD_NORM" ] && CWD_NORM="/"
    PROJECT_KEY=$(printf '%s' "$CWD_NORM" | sed 's|/|-|g' 2>/dev/null || true)
    PROJECT_KEY="${PROJECT_KEY#-}"
    [ -z "$PROJECT_KEY" ] && PROJECT_KEY="root"

    STICKY_FILE="$STATE_DIR/auggie-first-pending/$SESSION_ID.txt"

    CROSSED=false
    CROSS_CAUSE=""
    if [ -f "$STICKY_FILE" ]; then
        CROSSED=true; CROSS_CAUSE="sticky"
    elif [ -n "$DELTA_SEC" ] && [ "$DELTA_SEC" -ge "$AUGGIE_THRESHOLD_S" ] 2>/dev/null; then
        CROSSED=true; CROSS_CAUSE="threshold"
    fi

    if [ "$CROSSED" = true ]; then
        AUGGIE_REG=false
        if [ -r "$HOME/.claude.json" ] && command -v jq >/dev/null 2>&1; then
            if jq -e '.mcpServers // {} | has("auggie")' "$HOME/.claude.json" >/dev/null 2>&1; then
                AUGGIE_REG=true
            fi
        fi

        if [ "$AUGGIE_REG" = true ]; then
            INDEXED_LIST="$HOME/.claude/auggie-projects.txt"
            IS_INDEXED=false
            if [ -r "$INDEXED_LIST" ] && [ -n "$CWD_NORM" ]; then
                if awk -v target="$CWD_NORM" '{ sub(/\/+$/,""); if ($0==target) { found=1; exit } } END { exit !found }' \
                       "$INDEXED_LIST" 2>/dev/null; then
                    IS_INDEXED=true
                fi
            fi

            DISMISS_FILE="$STATE_DIR/auggie-no-warn/$PROJECT_KEY"

            if [ "$IS_INDEXED" = true ]; then
                [ ! -f "$STICKY_FILE" ] && echo "$NOW_ISO" > "$STICKY_FILE" 2>/dev/null || true
                AUGGIE_FLAG="auggie_first_required=1"
                printf '{"ts":"%s","session_id":"%s","event":"nag_emitted","cause":"%s","cwd":"%s","delta_sec":%s}\n' \
                    "$NOW_ISO" "$SESSION_ID" "$CROSS_CAUSE" "$CWD_NORM" "${DELTA_SEC:-0}" \
                    >> "$AUGGIE_LOG" 2>/dev/null || true
            elif [ ! -e "$DISMISS_FILE" ]; then
                : > "$DISMISS_FILE" 2>/dev/null || true
                rm -f "$STICKY_FILE" 2>/dev/null || true
                AUGGIE_WARN="auggie_project_not_indexed=1 (call mcp__auggie__codebase-retrieval to index $CWD_NORM, or add to $INDEXED_LIST; rm $DISMISS_FILE to re-arm warning)"
                if [ ${#AUGGIE_WARN} -gt "$AUGGIE_WARN_MAX_LEN" ]; then
                    AUGGIE_WARN="auggie_project_not_indexed=1 (see $DISMISS_FILE for dismiss state)"
                fi
                printf '{"ts":"%s","session_id":"%s","event":"warn_emitted","cause":"%s","cwd":"%s","delta_sec":%s}\n' \
                    "$NOW_ISO" "$SESSION_ID" "$CROSS_CAUSE" "$CWD_NORM" "${DELTA_SEC:-0}" \
                    >> "$AUGGIE_LOG" 2>/dev/null || true
            fi
        fi
    fi
fi

# 7. RESUMED flag
RESUMED_FLAG=""
if [ -n "$DELTA_SEC" ] && [ "$DELTA_SEC" -ge 3600 ] 2>/dev/null; then
    RESUMED_FLAG="RESUMED_AFTER_LONG_PAUSE; rich refresh fired in SessionStart"
fi

# 8. Build envelope with truncation cascade
# Reads globals: CHANGED_FIELD, RESUMED_LINE, AUGGIE_FLAG, AUGGIE_WARN, NOW_ISO, TURN, ITEMS.
build_envelope() {
    {
        echo "<session-context>"
        printf '  ts=%s turn=%d' "$NOW_ISO" "$TURN"
        if [ -n "$ITEMS" ]; then
            printf ' %s' "${ITEMS% }"
        fi
        echo
        # Q6: auggie line printed first — highest priority, never truncated.
        if [ -n "$AUGGIE_FLAG" ]; then
            echo "  $AUGGIE_FLAG"
        elif [ -n "$AUGGIE_WARN" ]; then
            echo "  $AUGGIE_WARN"
        fi
        if [ -n "$CHANGED_FIELD" ]; then
            echo "  changed_since_last_turn=$CHANGED_FIELD"
        fi
        if [ -n "$RESUMED_LINE" ]; then
            echo "  $RESUMED_LINE"
        fi
        echo "</session-context>"
    }
}

CHANGED_FIELD=""
if [ "$CHANGED_COUNT" -gt 0 ]; then
    CHANGED_FIELD=$(printf '%s\n' "$CHANGED_PATHS" | grep -v '^$' | paste -sd ',' -)
fi
RESUMED_LINE="$RESUMED_FLAG"
ENVELOPE=$(build_envelope)
TRUNCATED=false
FIRST_THREE=""
DROPPED=0

# Truncate changed_since_last_turn first
if [ ${#ENVELOPE} -gt 9000 ] && [ "$CHANGED_COUNT" -gt 3 ]; then
    FIRST_THREE=$(printf '%s\n' "$CHANGED_PATHS" | grep -v '^$' | head -3 | paste -sd ',' -)
    DROPPED=$((CHANGED_COUNT - 3))
    CHANGED_FIELD="${FIRST_THREE},...(${DROPPED} more)"
    ENVELOPE=$(build_envelope)
    TRUNCATED=true
fi
# Drop RESUMED if still over
if [ ${#ENVELOPE} -gt 9000 ] && [ -n "$RESUMED_LINE" ]; then
    RESUMED_LINE=""
    ENVELOPE=$(build_envelope)
    TRUNCATED=true
fi

# 9. Truncation telemetry
if [ "$TRUNCATED" = true ]; then
    printf '{"ts":"%s","event":"UserPromptSubmit","session_id":"%s","turn":%d,"truncated":true,"changed_count":%d}\n' \
        "$NOW_ISO" "$SESSION_ID" "$TURN" "$CHANGED_COUNT" \
        >> "$LOG_DIR/freshness-hook.jsonl" 2>/dev/null || true
fi

# 10. Emit additionalContext JSON
jq -nc --arg ctx "$ENVELOPE" '{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": $ctx
  }
}' 2>/dev/null || printf '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"<session-context>ts=%s turn=%d</session-context>"}}\n' "$NOW_ISO" "$TURN"

exit 0
