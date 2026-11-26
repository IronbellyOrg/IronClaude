#!/bin/bash
# usage: run_case.sh NAME SID PUSHARGS...   (SID "-" = no launch record)
S=/tmp/l2-refusal-test; H=$S/home; HK=$H/.claude/hooks/launch-job-identity.sh
name=$1; sid=$2; shift 2
cmd="git push origin $*"
echo "=== $name"; date -u +%FT%TZ
echo "launch record: $(if [ "$sid" = - ]; then echo none; else echo "sessions/$sid = $(cat $H/.claude/state/launch-level/sessions/$sid)"; fi)"
echo "command: cd $S/work && $cmd"
if [ "$sid" = - ]; then wrapped="cd $S/work && $cmd"
else
  # the same rewrite the guard's identity hook makes for a governed Bash call
  json=$(jq -nc --arg s "$sid" --arg c "cd $S/work && $cmd" '{hook_event_name:"PreToolUse",tool_name:"Bash",session_id:$s,tool_use_id:"toolu_l2test",tool_input:{command:$c}}')
  wrapped=$(printf '%s' "$json" | HOME=$H bash $HK hook | jq -r '.hookSpecificOutput.updatedInput.command')
  echo "wrapped command (from identity hook): $wrapped"
fi
HOME=$H bash -c "$wrapped" >$S/out.txt 2>$S/err.txt; rc=$?
echo "exit code: $rc"; echo "--- stdout"; cat $S/out.txt; echo "--- stderr (git push output, after the hook's own text)"; cat $S/err.txt
echo "--- remote refs now:"; git -C $S/remote.git for-each-ref --format='%(refname)' | sed 's/^/  /'; echo "  (end)"
