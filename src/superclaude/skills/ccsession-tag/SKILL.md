---
name: ccsession-tag
description: "Tag the current Claude session with a label so it can be resumed by name via 'ccsession <name>' from the shell"
---

# /ccsession-tag — Label this session for later resume

The user invokes this command with a label as the argument, e.g.
`/ccsession-tag brownfield`.

## What to do

1. Extract the label from the user's invocation (the single argument after the
   command name, whitespace trimmed). If empty, ask the user for one and stop.

2. Run this bash command, with `<LABEL>` replaced by the user's label:

   ```bash
   LABEL="<LABEL>"

   WS_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
   WS_SLUG=$(echo "$WS_DIR" | sed 's|/|-|g')
   PROJECT_DIR="$HOME/.claude/projects/$WS_SLUG"
   TOPIC_DIR="$PROJECT_DIR/topics"

   # Resolve current session ID: prefer the env var set by the session-start
   # hook; otherwise fall back to "newest .jsonl in this workspace's project
   # dir". The fallback works for any session, including ones that started
   # before the hook was installed — running this command writes to the active
   # session's transcript, so its mtime is freshest at lookup time.
   SESSION_ID="${CLAUDE_SESSION_ID:-}"
   if [ -z "$SESSION_ID" ]; then
     NEWEST_JSONL=$(ls -t "$PROJECT_DIR"/*.jsonl 2>/dev/null | head -1)
     if [ -z "$NEWEST_JSONL" ]; then
       echo "ERROR: no session JSONLs found under $PROJECT_DIR" >&2
       exit 1
     fi
     SESSION_ID=$(basename "$NEWEST_JSONL" .jsonl)
   fi

   mkdir -p "$TOPIC_DIR"
   echo "$SESSION_ID" > "$TOPIC_DIR/$LABEL.txt"
   # Cache the real workspace path so listing logic can show it accurately
   # even when the dir name contains dashes (slug encoding is lossy).
   echo "$WS_DIR" > "$TOPIC_DIR/.cwd"

   echo "Tagged session ${SESSION_ID:0:8} as '$LABEL' in $(basename "$WS_DIR")"
   echo "Resume next time with: ccsession $LABEL"
   ```

3. Relay the bash output to the user verbatim. If it exits non-zero, surface
   the error.

## Notes

- Re-tagging is allowed; running again with a different label overwrites the
  pointer. The underlying transcript is untouched.
- Labels are per-workspace. Two workspaces can each have their own
  `brownfield` without collision.
- This command writes only two tiny files under
  `~/.claude/projects/<workspace-slug>/topics/` — a `<label>.txt` containing
  the session UUID, and a `.cwd` containing the real workspace path.
- The shell-side counterpart is `ccsession` — see this skill's README for
  install instructions.
