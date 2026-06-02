#!/usr/bin/env bash
# FileChanged tracker per design §3.5. async:true.
# Records external modifications ONLY for paths some session has Read (last 24h).
# Fail-open per NFR-3.
#
# ⚠️  NOT REGISTERED IN v1. The T05.01 probe revealed that Claude Code's
# FileChanged matcher accepts only |-separated literal filenames (not regex,
# not "watch all"), so the design's matcher ".*" never fired. The FileChanged
# entry has been removed from src/superclaude/hooks/hooks.json. This script
# remains on disk (and still gets copied to ~/.claude/hooks/) for v1.5
# re-implementation. To reactivate, register it in settings.json with a
# meaningful matcher (specific filenames) and verify the watch list is
# populated either statically or via hookSpecificOutput.watchPaths from
# another hook event.
#
# Confirmed stdin schema from the probe (when it eventually fires):
#   file_path: absolute path to the changed file
#   event:     "change" | "add" | "unlink"
# The .path // .file_path fallback below handles either naming.

set -u

STATE_DIR="$HOME/.claude/state"
mkdir -p "$STATE_DIR" 2>/dev/null || true
READS_FILE="$STATE_DIR/reads.jsonl"
CHANGES_FILE="$STATE_DIR/changes.jsonl"

INPUT="$(cat 2>/dev/null || true)"
CHANGED_PATH=$(printf '%s' "$INPUT" | jq -r '.path // .file_path // .filePath // empty' 2>/dev/null)
[ -z "$CHANGED_PATH" ] && exit 0
CHANGE_TYPE=$(printf '%s' "$INPUT" | jq -r '.change_type // .changeType // .event // "modified"' 2>/dev/null || echo "modified")

# 2. Only care if some session Read this path (within 24h)
[ -f "$READS_FILE" ] || exit 0
NOW_UNIX=$(date +%s 2>/dev/null || echo 0)
CUTOFF=$((NOW_UNIX - 86400))
# Line-resilient lookup (see freshness-pre-edit.sh): one corrupt/torn line
# must not abort the stream. grep -F prefilters; fromjson? drops bad lines.
SEEN=$(grep -F "$CHANGED_PATH" "$READS_FILE" 2>/dev/null \
    | jq -rR --arg p "$CHANGED_PATH" --argjson c "$CUTOFF" \
        'fromjson? // empty | select(.path == $p and .ts_unix >= $c) | .path' 2>/dev/null | head -1)
[ -z "$SEEN" ] && exit 0

NOW_ISO=$(date -Iseconds 2>/dev/null || date "+%Y-%m-%dT%H:%M:%S")

# 3. Append to changes.jsonl (flocked)
(
    if command -v flock >/dev/null 2>&1; then
        exec 8>"$CHANGES_FILE.lock"
        flock -w 1 8 2>/dev/null || true
    fi
    jq -nc --arg ts "$NOW_ISO" --argjson tu "$NOW_UNIX" --arg path "$CHANGED_PATH" \
        --arg ct "$CHANGE_TYPE" \
        '{ts:$ts, ts_unix:$tu, path:$path, change_type:$ct}' \
        2>/dev/null >> "$CHANGES_FILE" || true
) 2>/dev/null || true

exit 0
