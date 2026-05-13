#!/usr/bin/env bash
# After running a test, run this to inspect telemetry and confirm expected
# decision/reason rows landed in ~/.claude/logs/freshness-hook.jsonl.
#
# Usage:
#   verify-telemetry.sh                     # show summary
#   verify-telemetry.sh /path/to/file       # rows mentioning that file
#   verify-telemetry.sh --reason=read_too_old  # filter by reason

set -u

LOG="$HOME/.claude/logs/freshness-hook.jsonl"

if [ ! -f "$LOG" ]; then
    echo "ERROR: $LOG not found — no telemetry yet. Run a Claude Code session first." >&2
    exit 1
fi

ROWS=$(wc -l < "$LOG")
echo "Telemetry rows: $ROWS"
echo

if [ "$#" -eq 0 ]; then
    echo "=== Distribution by decision ==="
    jq -r '.decision // "?"' "$LOG" | sort | uniq -c
    echo
    echo "=== Distribution by reason ==="
    jq -r '.reason // "?"' "$LOG" | sort | uniq -c
    echo
    echo "=== Last 5 rows (most recent) ==="
    tail -5 "$LOG" | jq -c '{ts,decision,reason,path,tool,recent_read_age_sec}'
    exit 0
fi

case "$1" in
    --reason=*)
        WANT="${1#--reason=}"
        jq -c --arg r "$WANT" 'select(.reason == $r) | {ts,decision,reason,path,tool,recent_read_age_sec}' "$LOG"
        ;;
    *)
        # Treat $1 as a path substring
        jq -c --arg p "$1" 'select(.path | contains($p)) | {ts,decision,reason,path,tool,recent_read_age_sec}' "$LOG"
        ;;
esac
