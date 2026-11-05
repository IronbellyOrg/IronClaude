#!/bin/bash
# session-start hook for the ccsession skill.
#
# Fires on SessionStart (matcher: startup|resume). Reads session_id from the
# JSON payload on stdin and:
#   1. Writes CLAUDE_SESSION_ID into $CLAUDE_ENV_FILE so Bash tool calls
#      can see it.
#   2. Passes the payload to session-name.sh beside it, which saves the
#      session's name in the repo's name list: the label the ccsession wrapper
#      launched it with ($CLAUDE_TOPIC), else its Claude Code name, so future
#      `ccsession <name>` resumes it.
#
# Register this hook in ~/.claude/settings.json — install.sh prints the
# JSON snippet to add.

set -e

PAYLOAD=$(cat)

SESSION_ID=$(printf '%s' "$PAYLOAD" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null || echo "")

[ -z "$SESSION_ID" ] && exit 0

# 1. Persist session_id into the env file so Bash tool calls can read
#    $CLAUDE_SESSION_ID. A non-writable env file must NOT abort the hook
#    (set -e would otherwise exit non-zero on the failed append), so the
#    write is made failure-tolerant.
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo "CLAUDE_SESSION_ID=$SESSION_ID" >> "$CLAUDE_ENV_FILE" 2>/dev/null || true
fi

# 2. Save the session's name, using session-name.sh next to the real file of
#    this hook (following a symlinked hook). It never fails the hook.
_self="$0"
while [ -L "$_self" ]; do
  _link="$(readlink "$_self")"
  case "$_link" in
    /*) _self="$_link" ;;
    *) _self="$(dirname "$_self")/$_link" ;;
  esac
done
# Its own parent tells session-name.sh which Claude Code runs the hook.
printf '%s' "$PAYLOAD" | CCSESSION_HOOK_EVENT=SessionStart CCSESSION_HOOK_PARENT=$PPID \
  bash "$(dirname "$_self")/session-name.sh" 2>/dev/null || true

exit 0
