#!/usr/bin/env bash
# PostToolUse(Read) tracker per design §3.4. async:true — non-blocking.
# Fail-open per NFR-3: append fails → exit 0; gap heals on next gate eval.

set -u

STATE_DIR="$HOME/.claude/state"
mkdir -p "$STATE_DIR/tool-call-counter" 2>/dev/null || true
READS_FILE="$STATE_DIR/reads.jsonl"

INPUT="$(cat 2>/dev/null || true)"
SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
[ -z "$FILE_PATH" ] && exit 0

# 2. Skip failed reads. tool_response shape varies; treat presence of an error
# indicator (success:false, error key, or is_error:true) as failure.
RESP_FAILED=$(printf '%s' "$INPUT" | jq -r '
    .tool_response as $r
    | if ($r | type) == "object" then
        ( $r.success == false or ($r.error != null) or ($r.is_error == true) )
      else false end' 2>/dev/null || echo "false")
[ "$RESP_FAILED" = "true" ] && exit 0

NOW_ISO=$(date -Iseconds 2>/dev/null || date "+%Y-%m-%dT%H:%M:%S")
NOW_UNIX=$(date +%s 2>/dev/null || echo 0)

# 3-4. Atomic: increment tool-call-counter + append reads row with that idx.
# Both operations inside one lock (counter lock file is per-session) to guarantee
# unique tool_call_idx per session even under heavy parallel post-read calls.
TCC_FILE="$STATE_DIR/tool-call-counter/$SESSION_ID.txt"
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
    # Atomic append: build the COMPLETE record first, then write it with a
    # single printf that includes the trailing newline. Streaming jq's output
    # straight to `>> file` can leave a torn record (a partial line with no
    # newline) if the write is interrupted mid-stream under ENOSPC — and the
    # next append then fuses onto it, producing an unparseable line that
    # poisons every reader. Building the line first means a jq failure writes
    # NOTHING (not a partial), and the lone printf never emits a record
    # without its terminator.
    line=$(jq -nc --arg ts "$NOW_ISO" --argjson tu "$NOW_UNIX" --arg sid "$SESSION_ID" \
        --arg path "$FILE_PATH" --argjson idx "$new" \
        '{ts:$ts, ts_unix:$tu, session_id:$sid, path:$path, tool_call_idx:$idx}' 2>/dev/null)
    [ -n "$line" ] && printf '%s\n' "$line" >> "$READS_FILE" 2>/dev/null || true
) 2>/dev/null || true

exit 0
