#!/bin/bash
# PreToolUse hook of the claim session: refuse a Write/Edit to an ob-442/ file and a shell command that writes one.
in=$(cat 2>/dev/null) || exit 0
case "$(printf '%s' "$in" | jq -r '.tool_name // ""')" in
  Write|Edit|NotebookEdit) p=$(printf '%s' "$in" | jq -r '.tool_input.file_path // .tool_input.notebook_path // ""')
    case "$p" in *ob-442/*|*settings.local.json*) echo "ob-442 guard: the claim session must not create files for the disposable issues or edit a worktree's settings.local.json" >&2; exit 2 ;; esac ;;
  Bash) c=$(printf '%s' "$in" | jq -r '.tool_input.command // ""')
    if printf '%s' "$c" | grep -qE '(>|tee|touch|mkdir|cp|mv|printf|echo|sed|jq)[^|;&]*(ob-442/|settings\.local\.json)'; then echo "ob-442 guard: the claim session must not create files for the disposable issues or edit a worktree's settings.local.json" >&2; exit 2; fi ;;
esac
exit 0
