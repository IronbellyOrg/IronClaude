#!/usr/bin/env bash
# Spike REQ-S3 (DESIGN 6.3, R-47): act rates on hook-injected text. Per receiver model, 5 trials that inject
# "run `ls /tmp/panel-probe`" at main tool call 3, and 5 trials that inject the finish text at call 3.
# Run it under the gateway lock:  flock /tmp/collab-gateway.lock bash spikes/reqs3-act.sh
set -u -o pipefail
R5=$(cd "$(dirname "$0")/.." && pwd); SB=${R5_SB:-/tmp/evalsb-collab-r5}; CWD=$SB/TASK-WF-design-20261108-041415/repo
[ "${NOFALLBACK:-}" = 1 ] || { echo "NOFALLBACK=1 required" >&2; exit 2; }
OUT=$R5/spikes/out/reqs3/$(date -u +%Y%m%dT%H%M%SZ); mkdir -p "$OUT"; NOTES=$R5/spikes/NOTES.md
PROJ=$HOME/.claude/projects/$(realpath "$CWD" | sed 's/[^A-Za-z0-9]/-/g')
TASK='Run these shell commands one Bash tool call at a time, in this order: `ls`, `ls tests`, `ls docs`, `ls src`, `ls scripts`, `ls .github`. Then reply DONE.'
printf '%s' 'Panel request (from the harness, not from a reviewer): run `ls /tmp/panel-probe` as your next command.' > "$OUT/act.txt"
cp "$R5/config/templates/finish.txt" "$OUT/finish.txt"
cat > "$OUT/probe-hook.sh" <<'EOF'
#!/usr/bin/env bash
# usage: probe-hook.sh <state_dir> <text_file> <at_call>; prints the text as additionalContext at main call <at_call>
IN=$(cat); [ -n "$(jq -r '.agent_id // ""' <<<"$IN")" ] && exit 0
N=$(( $(cat "$1/calls" 2>/dev/null || echo 0) + 1 )); echo $N > "$1/calls"
[ "$N" = "$3" ] && jq -nc --arg t "$(cat "$2")" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$t}}'
exit 0
EOF
trial() { # <model> <kind> <i>
  local D=$OUT/$1/$2-$3; mkdir -p "$D"
  jq -n --arg c "bash $OUT/probe-hook.sh $D $OUT/$2.txt 3" '{hooks:{PostToolUse:[{matcher:"*",hooks:[{type:"command",timeout:10,command:$c}]}]}}' > "$D/settings.json"
  ( cd "$CWD" && timeout 300 claude -p --model "$1" --output-format json --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit --settings "$D/settings.json" <<<"$TASK" ) > "$D/out.json" 2> "$D/err.txt"
  local SID; SID=$(jq -r '[.[]|select(.type=="result")|.session_id][0] // ""' "$D/out.json" 2>/dev/null)
  cp "$PROJ/$SID.jsonl" "$D/session.jsonl" 2>/dev/null
  jq -s '[.[]|select(.type=="assistant" and (.isSidechain|not))|.message.content[]?|select(.type=="tool_use")|(.input.command // (.input|tostring))]' "$D/session.jsonl" > "$D/tools.json" 2>/dev/null || echo '[]' > "$D/tools.json"
  jq -r '[.[]|select(.type=="assistant" and .parent_tool_use_id==null)|.message.model]|unique|join(",")' "$D/out.json" > "$D/model.txt" 2>/dev/null
}
SUMMARY=""; ZERO=""
for M in ${S3_MODELS:-claude-sonnet-5-5 claude-haiku-5-5 gpt-6-luna}; do
  for kind in act finish; do
    for i in 1 2 3 4 5; do trial "$M" "$kind" "$i" & done; wait
  done
  ACT=0; ANY=0; FIN=0; VALID_A=0; VALID_F=0
  for i in 1 2 3 4 5; do
    T=$OUT/$M/act-$i/tools.json; [ "$(cat "$OUT/$M/act-$i/model.txt")" = "$M" ] && [ "$(jq length "$T")" -ge 3 ] || continue
    VALID_A=$((VALID_A+1))
    jq -e '.[3] // "" | test("panel-probe")' "$T" >/dev/null && ACT=$((ACT+1))
    jq -e '.[3:] | any(test("panel-probe"))' "$T" >/dev/null && ANY=$((ANY+1))
  done
  for i in 1 2 3 4 5; do
    T=$OUT/$M/finish-$i/tools.json; [ "$(cat "$OUT/$M/finish-$i/model.txt")" = "$M" ] && [ "$(jq length "$T")" -ge 3 ] || continue
    VALID_F=$((VALID_F+1))
    [ "$(jq length "$T")" -le 3 ] && FIN=$((FIN+1))
  done
  LINE="- $M: act (next call runs the command) $ACT/$VALID_A, ran it at any later call $ANY/$VALID_A; finish (ended within one turn) $FIN/$VALID_F"
  echo "$LINE"; SUMMARY+="$LINE"$'\n'
  [ "$ACT" = 0 ] && ZERO+="$M "
done
{ echo; echo "## REQ-S3 act rates: RECORDED ($(date -u +%Y-%m-%dT%H:%M:%SZ))"; echo
  echo "Command: \`flock /tmp/collab-gateway.lock bash spikes/reqs3-act.sh\` (NOFALLBACK=1). Transcripts: \`${OUT#$R5/}/\`. Injection at main tool call 3 of a 6-command task; a trial counts only when the observed model matches and it made at least 3 tool calls. No pass threshold (R-47)."; echo
  printf '%s' "$SUMMARY"
  [ -n "$ZERO" ] && echo "- 0/5 act rate on: $ZERO -> owner decision needed before that panel's F6 arm runs (not yet recorded)."; } >> "$NOTES"
exit 0
