#!/bin/bash
# session-start hook for the ccsession skill.
#
# Fires on SessionStart (matcher: startup|resume). Reads session_id from the
# JSON payload on stdin and:
#   1. Writes CLAUDE_SESSION_ID into $CLAUDE_ENV_FILE so Bash tool calls
#      can see it (used by /ccsession-tag's fast path).
#   2. If $CLAUDE_TOPIC is set by the ccsession wrapper, writes the
#      session_id to the workspace's topic file so future
#      `ccsession <topic>` resumes it.
#
# Register this hook in ~/.claude/settings.json — install.sh prints the
# JSON snippet to add.

set -e

PAYLOAD=$(cat)

SESSION_ID=$(printf '%s' "$PAYLOAD" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null || echo "")
CWD=$(printf '%s' "$PAYLOAD" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('cwd',''))" 2>/dev/null || echo "")

[ -z "$SESSION_ID" ] && exit 0
[ -z "$CWD" ] && CWD=$(pwd)

# 1. Persist session_id into the env file so Bash tool calls can read
#    $CLAUDE_SESSION_ID. A non-writable env file must NOT abort the hook
#    (set -e would otherwise exit non-zero on the failed append), so the
#    write is made failure-tolerant.
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo "CLAUDE_SESSION_ID=$SESSION_ID" >> "$CLAUDE_ENV_FILE" 2>/dev/null || true
fi

# 2. If the parent shell labeled this session via the ccsession wrapper,
#    persist the label → session_id mapping under this workspace.
#    Defense-in-depth: $CLAUDE_TOPIC is interpolated into a file path, so
#    reject any value that could escape the topics/ dir before using it.
case "$CLAUDE_TOPIC" in
  */* | *..* | . | *[!A-Za-z0-9._-]*) CLAUDE_TOPIC="" ;;
esac
if [ -n "$CLAUDE_TOPIC" ]; then
  WS_SLUG=$(echo "$CWD" | sed 's|/|-|g')
  TOPIC_DIR="$HOME/.claude/projects/$WS_SLUG/topics"
  # All writes are failure-tolerant so a non-writable target can never abort
  # the hook under set -e — it must always reach `exit 0`.
  mkdir -p "$TOPIC_DIR" 2>/dev/null || true
  echo "$SESSION_ID" > "$TOPIC_DIR/$CLAUDE_TOPIC.txt" 2>/dev/null || true
  echo "$CWD" > "$TOPIC_DIR/.cwd" 2>/dev/null || true
fi

exit 0
