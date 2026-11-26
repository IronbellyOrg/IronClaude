#!/usr/bin/env bash
# PostToolUse(Bash) Run-ledger appender: records a new Orca Run in the Run ledger at once.
#
# When a Bash tool call ran `orca orchestration run-create` or `orca orchestration
# worker-start` (also as `orca-ide`, the command named by ORCA_CLI_COMMAND, or an absolute
# path to one of them), this takes the Run id and calls `superclaude sweep ledger --add <id>`,
# so the coordinator's `/sc:sweep` sees the Run before the next scheduled rebuild.
# Id sources: `run-create` prints the new Run in its result (`result.run.id`); the first
# `run_[0-9a-f]{12}` in the Bash result text is used. `worker-start` takes the value of
# the command's own `--run`, else the first such id in the result text.
#
# Decision contract (same family as require-orca-worktree-agent.sh): this hook never
# blocks. It always exits 0 and prints nothing. Fail open: jq or superclaude missing,
# input not valid JSON, tool is not Bash, no command, no id, or `--add` failing. When a
# matching command gives no id, or `--add` fails, one line is appended to
# ${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/run-ledger-hook.log; the next
# ledger rebuild catches the Run through its 24 h "new" rule.
#
# Registration is NOT done here or by `superclaude install`: Coder issue 545 registers
# it under hooks.PostToolUse with matcher "Bash" (see docs/user-guide/run-ledger.md).
#
# shortcut: the command is matched with a simple pattern, not a full shell tokenizer, a
# quoted mention can add a harmless extra id

set -u

command -v jq >/dev/null 2>&1 || exit 0
command -v superclaude >/dev/null 2>&1 || exit 0

input=$(cat) || exit 0
[ "$(printf '%s' "$input" | jq -r '.tool_name // empty' 2>/dev/null)" = "Bash" ] || exit 0
command_text=$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null) || exit 0
[ -n "$command_text" ] || exit 0

# The Orca CLI is `orca-ide` by default in the sweep, `orca` on some hosts, or the command named
# by ORCA_CLI_COMMAND; it may also be called by an absolute path.
orca_names='orca|orca-ide'
cli_name=${ORCA_CLI_COMMAND:-}
cli_name=${cli_name##*/}
[[ $cli_name =~ ^[A-Za-z0-9._-]+$ ]] && orca_names="$orca_names|${cli_name//./\\.}"
# The path may be quoted (it can then hold spaces): "/opt/My Tools/orca-ide" or '/a b/orca'.
path_prefix='("[^"]*/|'"'"'[^'"'"']*/|[^[:space:];&|()"'"'"']*/)?'
verb_pattern="(^|[[:space:];&|(])${path_prefix}[\"']?($orca_names)[\"']?[[:space:]]+orchestration[[:space:]]+(run-create|worker-start)([[:space:]]|\$)"
[[ $command_text =~ $verb_pattern ]] || exit 0
verb=${BASH_REMATCH[4]}

id_pattern='run_[0-9a-f]{12}'
id=""
if [ "$verb" = "worker-start" ]; then
  run_flag_pattern='--run[[:space:]=]+(run_[0-9a-f]{12})([^0-9a-f]|$)'
  [[ $command_text =~ $run_flag_pattern ]] && id=${BASH_REMATCH[1]}
fi
if [ -z "$id" ]; then
  # tool_response is a string or an object; look at its whole text either way.
  response=$(printf '%s' "$input" | jq -r '.tool_response // empty | if type == "string" then . else tojson end' 2>/dev/null) || response=""
  id=$(printf '%s' "$response" | grep -oE "$id_pattern" | head -n 1)
fi

log() {
  local dir="${XDG_STATE_HOME:-$HOME/.local/state}/superclaude"
  mkdir -p "$dir" 2>/dev/null || return 0
  printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" >>"$dir/run-ledger-hook.log" 2>/dev/null || true
}

if [ -z "$id" ]; then
  log "$verb: no Run id found in the result; the next ledger rebuild will pick the Run up"
  exit 0
fi
superclaude sweep ledger --add "$id" >/dev/null 2>&1 || log "$verb: superclaude sweep ledger --add $id failed"
exit 0
