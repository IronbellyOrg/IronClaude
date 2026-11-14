#!/usr/bin/env bash
# s2-resume.sh <model>: spike S2, resume part (design 6.3; deviation D-5). Real model calls:
# run it under the shared gateway lock:  flock /tmp/collab-gateway.lock spikes/s2-resume.sh <model>
set -u -o pipefail
MODEL=$1
HERE=$(cd "$(dirname "$0")/.." && pwd)
SB="${R4_SBR:-/tmp/evalsb-collab-r4}/sb/TASK-WF-designSpec-20261107-075614/repo"
OUTD="$HERE/spikes/out"; mkdir -p "$OUTD"
W=/tmp/collab-r4/s2-$MODEL-$(date +%s); mkdir -p "$W"
[ "${NOFALLBACK:-}" = 1 ] || { echo "NOFALLBACK=1 required" >&2; exit 2; }
jq -e --arg m "$MODEL" '.allowed_models|index([$m])' "$HERE/frozen/panels.json" >/dev/null || { echo "model not allowed" >&2; exit 2; }
SID=$(cat /proc/sys/kernel/random/uuid)
( cd "$SB" && timeout 300 claude -p --model "$MODEL" --output-format json --session-id "$SID" --permission-mode bypassPermissions \
    --disallowedTools Edit Write NotebookEdit <<<"Reply with the single word ALPHA and nothing else." ) > "$W/first.json" 2> "$W/first.err"
RC1=$?
TR=$(find "$HOME/.claude/projects" -maxdepth 2 -name "$SID.jsonl" | head -1)
( cd "$SB" && timeout 300 claude -p --resume "$SID" --model "$MODEL" --output-format stream-json --verbose --permission-mode bypassPermissions \
    --disallowedTools Edit Write NotebookEdit <<<"Reply with the word BETA, then repeat the single word you replied with before." ) > "$W/resume.jsonl" 2> "$W/resume.err"
RC2=$?
R1=$(jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$W/first.json" 2>/dev/null)
R2=$(jq -r 'select(.type=="result")|.result // ""' "$W/resume.jsonl" 2>/dev/null | tail -1)
O1=$(jq -r '[.[]|select(.type=="assistant" and .parent_tool_use_id==null)|.message.model]|unique|join(",")' "$W/first.json" 2>/dev/null)
O2=$(jq -r 'select(.type=="assistant" and .parent_tool_use_id==null)|.message.model' "$W/resume.jsonl" 2>/dev/null | sort -u | paste -sd, -)
SID2=$(jq -r 'select(.type=="result")|.session_id // ""' "$W/resume.jsonl" 2>/dev/null | tail -1)
jq -n --arg m "$MODEL" --arg sid "$SID" --arg tr "$TR" --arg r1 "$R1" --arg r2 "$R2" --arg o1 "$O1" --arg o2 "$O2" --arg sid2 "$SID2" \
  --argjson rc1 $RC1 --argjson rc2 $RC2 --arg w "$W" '
  {model:$m, session_id:$sid, rc_first:$rc1, rc_resume:$rc2, transcript_file:$tr, transcript_written:($tr!=""),
   first_reply:$r1, resume_reply:$r2, observed_first:$o1, observed_resume:$o2, resume_session_id:$sid2, work_dir:$w,
   both_words:(($r2|test("BETA"))and($r2|test("ALPHA"))),
   model_ok:(($o1|ascii_downcase)==($m|ascii_downcase) and ($o2|ascii_downcase)==($m|ascii_downcase)),
   pass:(($tr!="") and ($r2|test("BETA")) and ($r2|test("ALPHA")) and ($o2|ascii_downcase)==($m|ascii_downcase))}' > "$OUTD/s2-$MODEL.json"
jq -c '{model,pass,transcript_written,both_words,model_ok}' "$OUTD/s2-$MODEL.json"
