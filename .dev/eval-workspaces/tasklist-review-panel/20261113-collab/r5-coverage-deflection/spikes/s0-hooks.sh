#!/usr/bin/env bash
# Spike S0 (DESIGN 6.3): hook delivery on each receiver model with the real hook and a pre-seeded card.
# Run it under the gateway lock:  flock /tmp/collab-gateway.lock bash spikes/s0-hooks.sh
# min_calls is 2 here (not 6) so that a 4-call task reaches delivery.
set -u -o pipefail
R5=$(cd "$(dirname "$0")/.." && pwd); SB=${R5_SB:-/tmp/evalsb-collab-r5}; PKG=TASK-WF-design-20261108-041415; CWD=$SB/$PKG/repo
[ "${NOFALLBACK:-}" = 1 ] || { echo "NOFALLBACK=1 required" >&2; exit 2; }
OUT=$R5/spikes/out/s0/$(date -u +%Y%m%dT%H%M%SZ); mkdir -p "$OUT"
NOTES=$R5/spikes/NOTES.md; PROJ=$HOME/.claude/projects/$(realpath "$CWD" | sed 's/[^A-Za-z0-9]/-/g')
TASK='Run the shell command `ls` four times, one Bash tool call each, then reply DONE.'
{ echo "user hooks (~/.claude/settings.json):"; jq -r '.hooks|to_entries[]|"  \(.key): \(.value|map(.hooks[].command|split("\n")[0][0:90])|join(" | "))"' ~/.claude/settings.json
  echo "project settings in sandbox: $(ls "$CWD"/.claude/settings*.json 2>/dev/null | tr '\n' ' ')"; } > "$OUT/hooks-active.txt"
overall=PASS; SUMMARY=""
for M in ${S0_MODELS:-claude-sonnet-5-5 claude-haiku-5-5 gpt-6-luna}; do
  D=$OUT/$M; B=$D/board; mkdir -p "$B"/{msgs,delivered,state,snap,metrics}
  T0=$(date +%s%3N); FIN=$((T0 + 600000))
  echo "{\"v\":\"panel-msg/1\",\"id\":\"c-s0-1\",\"run\":\"s0/$PKG\",\"from\":\"watcher\",\"to\":\"s0\",\"t\":$T0,\"kind\":\"coverage\",\"items\":[\"T9\"]}" > "$B/msgs/watcher.jsonl"
  jq -n --arg c "bash $R5/bin/hook-posttool.sh $B s0 $T0 $FIN 2 2 $R5" '{hooks:{PostToolUse:[{matcher:"*",hooks:[{type:"command",timeout:10,command:$c}]}]}}' > "$D/settings.json"
  S=$(date +%s%3N)
  ( cd "$CWD" && timeout 300 claude -p --model "$M" --output-format json --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit --settings "$D/settings.json" <<<"$TASK" ) > "$D/out.json" 2> "$D/err.txt"
  RC=$?; W=$(( $(date +%s%3N) - S ))
  SID=$(jq -r '[.[]|select(.type=="result")|.session_id][0] // ""' "$D/out.json" 2>/dev/null)
  OBS=$(jq -r '[.[]|select(.type=="assistant" and .parent_tool_use_id==null)|.message.model]|unique|join(",")' "$D/out.json" 2>/dev/null)
  cp "$PROJ/$SID.jsonl" "$D/session.jsonl" 2>/dev/null
  TOOLS=$(jq -s '[.[]|select(.type=="assistant" and (.isSidechain|not))|.message.content[]?|select(.type=="tool_use")]|length' "$D/session.jsonl" 2>/dev/null || echo -1)
  CALLS=$(jq -s '[.[]|select(.event=="call")]|length' "$B/metrics/s0.jsonl" 2>/dev/null || echo 0)
  SUBAG=$(jq -s '[.[]|select(.event=="subagent_call")]|length' "$B/metrics/s0.jsonl" 2>/dev/null || echo 0)
  P95=$(jq -s '[.[]|select(.event=="call")|.ms]|sort|if length==0 then null else .[((length*0.95)|ceil)-1] end' "$B/metrics/s0.jsonl" 2>/dev/null)
  DELIV=$(jq -s '[.[]|select(.status=="delivered")]|length' "$B/delivered/s0.jsonl" 2>/dev/null || echo 0)
  INTRANS=$(grep -c 'Panel request (from the harness' "$D/session.jsonl" 2>/dev/null || echo 0)
  SNAPOK=false; [ -s "$B/snap/s0.sha256" ] && [ "$(cut -d' ' -f1 "$B/snap/s0.sha256")" = "$(sha256sum "$B/snap/s0.jsonl" | cut -d' ' -f1)" ] && SNAPOK=true
  OK=PASS
  { [ "$RC" = 0 ] && [ "$OBS" = "$M" ] && [ "$TOOLS" -ge 1 ] && [ "$CALLS" = "$TOOLS" ] && [ "$DELIV" = 1 ] && [ "$INTRANS" -ge 1 ] && $SNAPOK; } || { OK=FAIL; overall=FAIL; }
  LINE="- $M: $OK (rc=$RC observed=$OBS main_tool_calls=$TOOLS hook_calls=$CALLS subagent_calls=$SUBAG delivered=$DELIV card_text_in_transcript=$INTRANS snapshot_sha_ok=$SNAPOK hook_ms_p95=$P95 wall_ms=$W)"
  echo "$LINE"; SUMMARY+="$LINE"$'\n'
done
echo "sandbox git status lines after S0: $(git -C "$CWD" status --porcelain | wc -l)" | tee -a "$OUT/hooks-active.txt"
{ echo; echo "## S0 hooks: $overall ($(date -u +%Y-%m-%dT%H:%M:%SZ))"; echo
  echo "Command: \`flock /tmp/collab-gateway.lock bash spikes/s0-hooks.sh\` (NOFALLBACK=1). Transcripts: \`${OUT#$R5/}/\`."; echo
  printf '%s' "$SUMMARY"; echo "- user/project hooks active in the sandbox: \`${OUT#$R5/}/hooks-active.txt\`"; } >> "$NOTES"
[ $overall = PASS ]
