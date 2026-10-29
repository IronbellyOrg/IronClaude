#!/bin/bash
# session-name hook for the ccsession skill: keeps ccsession's name list in
# step with the session's name in Claude Code, so a name given either way
# (`ccsession <name>` or /rename <name>) is listed and resumes with
# `ccsession <name>`.
#
# Registered for UserPromptSubmit and SessionEnd; session-start.sh passes its
# SessionStart payload here too. Claude Code runs no hook when /rename changes
# a name, so the change is picked up by the next of these:
#   - SessionStart: a session ccsession launched takes its label
#     ($CLAUDE_TOPIC); any other session its current name (session_title).
#   - UserPromptSubmit: the session's current name (session_title).
#   - SessionEnd: the newest name in the transcript (the payload has none), so
#     a /rename just before quitting is kept.
# A session without a name changes nothing: Claude Code reports only names a
# person gave, never its automatic ones. In an Orca tab whose title ccsession
# owns, a new name is shown on the tab too (ccsession --sync-name does it).
# Always exits 0: a naming problem must never block a prompt.

PAYLOAD=$(cat)

# One field per NUL-ended line: session id, folder, event, name, end reason.
read_payload='
import json, sys

MARK = b"\"type\":\"custom-title\""
TAIL = 8 << 20  # a /rename just before quitting is at the very end


def newest_name(path):
    try:
        with open(path, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - TAIL))
            data = f.read()
    except (OSError, TypeError):
        return ""
    at = data.rfind(MARK)
    if at < 0:
        return ""
    start = data.rfind(b"\n", 0, at) + 1
    end = data.find(b"\n", at)
    try:
        return json.loads(data[start : end if end >= 0 else len(data)]).get(
            "customTitle"
        ) or ""
    except (ValueError, AttributeError):
        return ""


try:
    p = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
event = p.get("hook_event_name") or ""
name = p.get("session_title")
if event == "SessionEnd":
    name = newest_name(p.get("transcript_path"))
fields = [p.get("session_id"), p.get("cwd"), event, name, p.get("reason")]
fields = [f if isinstance(f, str) else "" for f in fields]
sys.stdout.write("".join(f.replace("\0", "") + "\0" for f in fields))
'
{
  IFS= read -r -d '' SESSION_ID
  IFS= read -r -d '' CWD
  IFS= read -r -d '' EVENT
  IFS= read -r -d '' NAME
  IFS= read -r -d '' REASON
} < <(printf '%s' "$PAYLOAD" | python3 -c "$read_payload" 2>/dev/null)

[ -n "${SESSION_ID:-}" ] || exit 0
[ -n "${CWD:-}" ] || CWD=$(pwd)
# session-start.sh says which event it passes on (its payload may not).
[ -n "${EVENT:-}" ] || EVENT="${CCSESSION_HOOK_EVENT:-}"

proc() {
  # Sets PROC_PPID and PROC_COMM (name without path or login "-") for a process:
  # from /proc on Linux, with no new process; else from one `ps` listing.
  local line p pp c
  PROC_PPID="" PROC_COMM=""
  if [ -r "/proc/$1/stat" ] && IFS= read -r line < "/proc/$1/stat" 2>/dev/null; then
    # The name in stat is in brackets and may hold spaces; fields follow ") ".
    read -r _ PROC_PPID _ <<< "${line##*) }"
    IFS= read -r PROC_COMM < "/proc/$1/comm" 2>/dev/null || PROC_COMM=""
  else
    [ -n "${PS_TABLE+set}" ] || PS_TABLE=$(ps -A -o pid= -o ppid= -o comm= 2>/dev/null)
    while read -r p pp c; do
      [ "$p" = "$1" ] && { PROC_PPID=$pp; PROC_COMM=$c; break; }
    done <<< "$PS_TABLE"
  fi
  PROC_COMM=${PROC_COMM##*/}
  PROC_COMM=${PROC_COMM#-}
  [ -n "$PROC_PPID" ]
}

is_shell_name() {
  case "$1" in
    sh | bash | dash | zsh | ksh | mksh) return 0 ;;
  esac
  return 1
}

firing_claude() {
  # The Claude Code that runs this hook: it starts a hook through sh, so it is
  # the nearest ancestor that is not a shell. session-start.sh, which passes
  # SessionStart on, gives its own parent (CCSESSION_HOOK_PARENT): Claude Code
  # runs it under the script's name, which is no shell name. Prints its id, and
  # its parent's id when that parent is a shell (a CLAUDE_BIN wrapper script
  # that runs claude), else 0. Exit 2: processes could not be read.
  local pid=$PPID n=0
  case "${CCSESSION_HOOK_PARENT:-}" in
    '' | *[!0-9]*) : ;;
    *) pid=$CCSESSION_HOOK_PARENT ;;
  esac
  proc "$pid" || return 2
  while [ "$n" -lt 8 ] && [ "${pid:-0}" -gt 1 ]; do
    if is_shell_name "$PROC_COMM"; then
      pid=$PROC_PPID
      proc "$pid" || return 1
    else
      local claude=$pid parent=$PROC_PPID
      proc "$parent" && is_shell_name "$PROC_COMM" || parent=0
      printf '%s %s\n' "$claude" "$parent"
      return 0
    fi
    n=$((n + 1))
  done
  return 1
}

# Is this the session ccsession launched? A claude started inside it (a
# pipeline's `claude -p`) inherits its environment, label and Orca tab, and
# must take over neither. ccsession replaces itself with Claude Code, so the
# Claude Code it launched has ccsession's process id, the first part of
# CCSESSION_LAUNCH_ID (or, for a CLAUDE_BIN wrapper script that does not exec,
# that script, its parent, has). Every session of that Claude Code is the
# launched one, /clear and resume included; a nested claude is another
# process, started by a shell or by Claude Code, and never is. Where no
# process can be read at all (no /proc and no usable ps), ownership cannot be
# checked and the hook acts for the launch, as ccsession did before.
OWNER=1
if [ -n "${CCSESSION_LAUNCH_ID:-}" ]; then
  OWNER=0
  launch_pid=${CCSESSION_LAUNCH_ID%%.*}
  case "$launch_pid" in
    '' | *[!0-9]*) : ;;
    *)
      _found=$(firing_claude)
      case $? in
        0)
          read -r _pid _ppid <<< "$_found"
          if [ "$_pid" = "$launch_pid" ] || [ "$_ppid" = "$launch_pid" ]; then
            OWNER=1
          fi
          ;;
        2) OWNER=1 ;;
      esac
      ;;
  esac
fi
# The launched session takes its label, in the folder ccsession launched it
# in; a nested claude keeps its own name, if it has one.
if [ "$EVENT" = SessionStart ] && [ "$OWNER" = 1 ] && [ -n "${CLAUDE_TOPIC:-}" ] &&
  { [ -z "${CCSESSION_TOPIC_CWD:-}" ] ||
    [ "$(cd "$CWD" 2>/dev/null && pwd -P)" = "$CCSESSION_TOPIC_CWD" ]; }; then
  NAME="$CLAUDE_TOPIC"
fi
# Only the launched session shows its name on the Orca tab.
[ "$OWNER" = 1 ] || unset ORCA_TERMINAL_HANDLE

# The ccsession beside this hook (following a symlinked hook), else the
# installed one. Only a ccsession that knows --sync-name is asked.
_self="$0"
while [ -L "$_self" ]; do
  _link="$(readlink "$_self")"
  case "$_link" in
    /*) _self="$_link" ;;
    *) _self="$(dirname "$_self")/$_link" ;;
  esac
done
for _ccs in "$(dirname "$_self")/../ccsession" \
  "$HOME/.claude/skills/ccsession-tag/ccsession"; do
  [ -x "$_ccs" ] && grep -q -- '--sync-name)' "$_ccs" 2>/dev/null || continue
  if [ -n "${NAME:-}" ]; then
    # Older names of the session are looked for only when the name changes,
    # and at the start and end of a session; not on every prompt.
    _check=--check-others
    [ "$EVENT" = UserPromptSubmit ] && _check=""
    (cd "$CWD" 2>/dev/null && "$_ccs" --sync-name "$SESSION_ID" "$NAME" $_check) \
      >/dev/null 2>&1 || true
  fi
  # Leaving Claude Code (not /clear): take a tab title ccsession set back off,
  # so the tab no longer shows a session that has ended.
  if [ "$EVENT" = SessionEnd ] && [ "${REASON:-}" != clear ] && [ "$OWNER" = 1 ]; then
    "$_ccs" --orca-tab-clear >/dev/null 2>&1 || true
  fi
  break
done

exit 0
