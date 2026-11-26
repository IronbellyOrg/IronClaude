#!/usr/bin/env bash
# Spike S2 (DESIGN 6.3): `claude -p --resume <session_id>` with stream-json for every panel model (H2 re-ask path).
# Run it under the gateway lock:  flock /tmp/collab-gateway.lock bash spikes/s2-resume.sh
set -u -o pipefail
R5=$(cd "$(dirname "$0")/.." && pwd); SB=${R5_SB:-/tmp/evalsb-collab-r5}; CWD=$SB/TASK-WF-design-20261108-041415/repo
[ "${NOFALLBACK:-}" = 1 ] || { echo "NOFALLBACK=1 required" >&2; exit 2; }
OUT=$R5/spikes/out/s2/$(date -u +%Y%m%dT%H%M%SZ); mkdir -p "$OUT"; NOTES=$R5/spikes/NOTES.md
overall=PASS; SUMMARY=""
for M in ${S2_MODELS:-claude-sonnet-5-5 claude-haiku-5-5 gpt-6-luna muse-ember-1.0}; do
  W=WORD$RANDOM$RANDOM; D=$OUT/$M; mkdir -p "$D"
  ( cd "$CWD" && timeout 300 claude -p --model "$M" --output-format json --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit \
      <<<"Remember this code word: $W. Reply with OK only." ) > "$D/first.json" 2> "$D/first.err"
  SID=$(jq -r '[.[]|select(.type=="result")|.session_id][0] // ""' "$D/first.json")
  O1=$(jq -r '[.[]|select(.type=="assistant" and .parent_tool_use_id==null)|.message.model]|unique|join(",")' "$D/first.json")
  S=$(date +%s%3N)
  ( cd "$CWD" && timeout 300 claude -p --resume "$SID" --model "$M" --output-format stream-json --verbose --permission-mode bypassPermissions \
      --disallowedTools Edit Write NotebookEdit <<<"What was the code word? Reply with the code word only." ) > "$D/resume.jsonl" 2> "$D/resume.err"
  E=$(date +%s%3N)
  ANS=$(jq -rs '[.[]|select(.type=="result")|.result][0] // ""' "$D/resume.jsonl")
  O2=$(jq -rs '[.[]|select(.type=="assistant" and .parent_tool_use_id==null)|.message.model]|unique|join(",")' "$D/resume.jsonl")
  FIRST_MS=$(jq -rs '[.[]|select(.type=="result")|.duration_ms][0] // null' "$D/resume.jsonl")
  OK=PASS; { grep -q "$W" <<<"$ANS" && [ "$O1" = "$M" ] && [ "$O2" = "$M" ]; } || { OK=FAIL; overall=FAIL; }
  LINE="- $M: $OK (first_model=$O1 resume_model=$O2 answer_has_word=$(grep -q "$W" <<<"$ANS" && echo yes || echo no) resume_wall_s=$(awk -v a=$S -v b=$E 'BEGIN{printf "%.1f",(b-a)/1000}') resume_duration_ms=$FIRST_MS)"
  echo "$LINE"; SUMMARY+="$LINE"$'\n'
done
{ echo; echo "## S2 resume: $overall ($(date -u +%Y-%m-%dT%H:%M:%SZ))"; echo
  echo "Command: \`flock /tmp/collab-gateway.lock bash spikes/s2-resume.sh\` (NOFALLBACK=1). Transcripts: \`${OUT#$R5/}/\`. Planning start cost was 6 s (MR:270); resume_wall_s is the whole resumed call."; echo
  printf '%s' "$SUMMARY"; } >> "$NOTES"
[ $overall = PASS ]
