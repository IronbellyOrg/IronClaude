#!/bin/bash
# Extra observation: command-word recognition of orca vs orca-ide (reuses the sandbox store left by run-guard-observation.sh).
set -u -o pipefail
SB=/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/05-guard-run-sandbox
GUARD=/home/coder/.cache/ic-snap-20261120/master/src/superclaude/hooks/scripts/launch-level-guard.sh
pb() { jq -nc --arg s "$1" --arg c "$2" '{hook_event_name:"PreToolUse",session_id:$s,tool_name:"Bash",tool_input:{command:$c}}'; }
for c in 'orca terminal send --text hi' 'orca-ide terminal send --text hi' 'orca-ide orchestration send --to run:run_1 --body hi' '/usr/local/bin/orca terminal send --text hi'; do
  printf '%s' "$(pb worker-w "$c")" | env -i HOME="$SB/home" PATH=/usr/bin:/bin "$GUARD" >"$SB/out/extra.stdout" 2>"$SB/out/extra.stderr"; rc=$?
  printf 'EXTRA | %s | exit=%s | blocked=[%s]\n' "$c" "$rc" "$(sed -n 's/^\(Blocked: .*\)$/\1/p' "$SB/out/extra.stderr" | head -n1 | cut -c1-70)"
done
