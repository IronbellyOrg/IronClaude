#!/usr/bin/env bash
# usage: probe-hook.sh <state_dir> <text_file> <at_call>; prints the text as additionalContext at main call <at_call>
IN=$(cat); [ -n "$(jq -r '.agent_id // ""' <<<"$IN")" ] && exit 0
N=$(( $(cat "$1/calls" 2>/dev/null || echo 0) + 1 )); echo $N > "$1/calls"
[ "$N" = "$3" ] && jq -nc --arg t "$(cat "$2")" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$t}}'
exit 0
