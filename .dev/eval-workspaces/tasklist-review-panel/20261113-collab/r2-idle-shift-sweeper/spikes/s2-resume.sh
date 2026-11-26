#!/usr/bin/env bash
# Spike S2: --resume <sid> with stream-json --verbose for the four reviewer models after a normal run without
# --no-session-persistence. PASS: the resumed reply comes from the same model and the stream file has lines.
#   flock /tmp/collab-gateway.lock bash spikes/s2-resume.sh
set -u -o pipefail
. "$(dirname "$0")/_spike.sh"
OUTD=$SPIKES/out/s2; mkdir -p "$OUTD"
ALL=PASS
for MODEL in muse-ember-1.0 gpt-6-luna claude-sonnet-5-5 claude-haiku-5-5; do
  D=$OUTD/$MODEL; W=/tmp/collab-r2/s2-$(rand_hex); mkdir -p "$D" "$W"
  ( cd "$W" && timeout 300 claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions \
      --disallowedTools Edit Write NotebookEdit <<<"Reply with exactly the word alpha." ) > "$D/first.json" 2> "$D/first.err"
  SID=$(jq -r '[.[]|select(.type=="result")|.session_id][0] // ""' "$D/first.json")
  S=$(now_ms)
  ( cd "$W" && timeout 300 claude -p --resume "$SID" --model "$MODEL" --output-format stream-json --verbose \
      --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"Reply with exactly the word beta." ) 2> "$D/resume.err" \
    | while IFS= read -r line; do printf '%s\n' "$line" >> "$D/resume.jsonl"; [ -f "$D/first_line_ms" ] || now_ms > "$D/first_line_ms"; done
  E=$(now_ms)
  OBS1=$(model_of "$D/first.json")
  OBS2=$(jq -rs '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$D/resume.jsonl" 2>/dev/null)
  RES=$(jq -rs '[.[]|select(.type=="result")|.result][0] // ""' "$D/resume.jsonl" 2>/dev/null)
  LINES=$(wc -l < "$D/resume.jsonl" 2>/dev/null || echo 0)
  FIRST=$(( $(cat "$D/first_line_ms" 2>/dev/null || echo "$S") - S ))
  V=PASS; WHY=()
  [ -n "$SID" ] || { V=FAIL; WHY+=("no-session-id"); }
  model_ok "$OBS1" "$MODEL" || { V=FAIL; WHY+=("first-model=$OBS1"); }
  model_ok "$OBS2" "$MODEL" || { V=FAIL; WHY+=("resume-model=$OBS2"); }
  [ "$LINES" -gt 0 ] || { V=FAIL; WHY+=("no-stream-lines"); }
  jq -n --arg m "$MODEL" --arg sid "$SID" --arg o1 "$OBS1" --arg o2 "$OBS2" --arg res "$RES" --argjson lines "$LINES" \
    --argjson first "$FIRST" --argjson wall $((E - S)) --arg v "$V" \
    '{model:$m,session_id:$sid,first_model:$o1,resume_model:$o2,resume_result:$res,stream_lines:$lines,
      resume_first_line_ms:$first,resume_wall_ms:$wall,verdict:$v}' > "$D/s2.json"
  record "S2[$MODEL]" "$V" "$D/s2.json" "resume_model=$OBS2 stream_lines=$LINES first_line_ms=$FIRST wall_ms=$((E - S)) result='${RES:0:20}' ${WHY[*]:-}"
  [ "$V" = PASS ] || ALL=FAIL
done
record S2 "$ALL" "$OUTD" "four models"
[ "$ALL" = PASS ]
