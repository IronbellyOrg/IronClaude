#!/usr/bin/env bash
# probe-hook.sh <logdir> <mode> [<catalogue.json>]   (Gate 0 probe hook; DESIGN.md 6.3 S0 and REQ-S3; not the radar hook)
#   log    save stdin as stdin.<n>.json, snapshot the transcript (snap.<n>.jsonl + sha256 in snap.sha), time this call in t.log,
#          print additionalContext "PROBE-CONTEXT-<n>"
#   sleep  sleep 5 s (run with a 1 s hook timeout: shows that a hook past its timeout does not kill the session)
#   reqs3  count calls in count; log {n,tool,cmd} to tele.jsonl; call 3 prints "run `ls /tmp/panel-probe`", call 8 prints finish_text
# Always exits 0. bash, jq, flock and coreutils only.
set -u -o pipefail
D=${1:?logdir}; MODE=${2:?mode}; CAT=${3:-}
mkdir -p "$D"
ms() { date +%s%3N; }
T0=$(ms); IN=$(head -c 1048576)
emit() { jq -n -c --arg t "$1" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$t}}'; }
case $MODE in
  sleep) echo "$(ms)" >> "$D/sleep.started"; sleep 5;;
  log)
    n=$( { flock 9; c=$(( $(cat "$D/count" 2>/dev/null || echo 0) + 1 )); echo "$c" > "$D/count"; echo "$c"; } 9> "$D/count.lock" )
    printf '%s' "$IN" > "$D/stdin.$n.json"
    tp=$(printf '%s' "$IN" | jq -r '.transcript_path // empty')
    if [ -n "$tp" ] && [ -s "$tp" ] && cp "$tp" "$D/snap.$n.jsonl"; then echo "$n $(sha256sum "$D/snap.$n.jsonl" | cut -d' ' -f1)" >> "$D/snap.sha"; fi
    emit "PROBE-CONTEXT-$n"
    echo "$(( $(ms) - T0 ))" >> "$D/t.log";;
  reqs3)
    sub=$(printf '%s' "$IN" | jq -r '.agent_id // empty')
    n=null; [ -n "$sub" ] || n=$( { flock 9; c=$(( $(cat "$D/count" 2>/dev/null || echo 0) + 1 )); echo "$c" > "$D/count"; echo "$c"; } 9> "$D/count.lock" )
    printf '%s' "$IN" | jq -c --argjson n "$n" --argjson t "$T0" '{n:$n,t:$t,tool:.tool_name,sub:(.agent_id != null),cmd:(.tool_input.command // .tool_input.file_path // .tool_input.pattern // "")}' >> "$D/tele.jsonl"
    if [ -z "$sub" ] && [ "$n" = 3 ]; then emit 'Run `ls /tmp/panel-probe` with the Bash tool now, then continue your review.'; echo "$n $T0 item" >> "$D/inject.log"
    elif [ -z "$sub" ] && [ "$n" = 8 ]; then emit "$(jq -r .finish_text "$CAT")"; echo "$n $T0 finish" >> "$D/inject.log"; fi;;
esac
exit 0
