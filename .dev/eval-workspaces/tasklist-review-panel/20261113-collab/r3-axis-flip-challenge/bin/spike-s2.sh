#!/usr/bin/env bash
# spike-s2.sh <model>: Gate 0 spike S2 (resume and stream-json). Records under R3/spikes/s2/<model>/.
set -u -o pipefail
source "$(dirname "$0")/../lib/common.sh"
MODEL=$1; r3_assert_model "$MODEL" || exit 1; r3_assert_nofallback || exit 1
PKG=${2:-TASK-WF-design-20261108-041415}
O=$R3/spikes/s2/$MODEL; r3_assert_writable "$O" || exit 1; mkdir -p "$O"
bash "$R3/bin/build-sandbox.sh" "$PKG" >/dev/null || exit 1
CWD=$SB/$PKG/repo; CAND=$SB/cand/$PKG/candidate.md
D=(--permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit)
P1="Read $CAND and reply with its first heading line only."
t0=$(r3_now)
( cd "$CWD" && timeout --kill-after=5 300 claude -p --model "$MODEL" --output-format json "${D[@]}" <<<"$P1" ) > "$O/fresh.json" 2> "$O/fresh.err"
t1=$(r3_now)
SID=$(jq -r '[.[]|select(.type=="result")|.session_id][0] // ""' "$O/fresh.json")
OBS1=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$O/fresh.json")
( cd "$CWD" && timeout --kill-after=5 300 claude -p --model "$MODEL" --resume "$SID" --output-format stream-json --verbose "${D[@]}" <<<"Now reply with the word RESUMED and the heading again." ) > "$O/resume.stream.jsonl" 2> "$O/resume.err"
RRC=$?; t2=$(r3_now)
FIRST_A=$(jq -s 'map(select(.type=="assistant"))|length' "$O/resume.stream.jsonl")
RSID=$(jq -sr '[.[]|select(.type=="system")|.session_id][0] // ""' "$O/resume.stream.jsonl")
OBS2=$(jq -sr '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$O/resume.stream.jsonl")
# killed mid-answer: a long task, killed after S2_KILL_S (default 25) s
( cd "$CWD" && timeout --kill-after=3 "${S2_KILL_S:-25}" claude -p --model "$MODEL" --resume "$SID" --output-format stream-json --verbose "${D[@]}" <<<"${S2_KILL_PROMPT:-Write, as you go, one line per Task heading in the candidate with a three-sentence summary of each task, then list every file path the candidate names with one sentence each; take your time and be thorough.}" ) > "$O/killed.stream.jsonl" 2> "$O/killed.err"
KRC=$?
KA=$(jq -s 'map(select(.type=="assistant"))|length' "$O/killed.stream.jsonl" 2>/dev/null || echo 0)
KT=$(jq -s 'map(select(.type=="assistant")|.message.content[]?|select(.type=="text"))|length' "$O/killed.stream.jsonl" 2>/dev/null || echo 0)
TF=$(find "$CLAUDE_PROJECTS" -maxdepth 2 -name "$SID.jsonl" | head -1)
TS=$( [ -n "$TF" ] && jq -s 'map(select(.type=="assistant" or .type=="user"))|all(has("timestamp"))' "$TF" || echo null)
[ -n "$TF" ] && cp "$TF" "$O/transcript.jsonl"
lc() { echo "$1" | tr A-Z a-z; }
jq -n --arg m "$MODEL" --arg sid "$SID" --arg rsid "$RSID" --arg o1 "$OBS1" --arg o2 "$OBS2" --argjson rrc $RRC --argjson krc $KRC \
  --argjson fa "$FIRST_A" --argjson ka "$KA" --argjson kt "$KT" --argjson ts "$TS" \
  --argjson fresh_s "$(r3_calc "$t1 - $t0")" --argjson resume_s "$(r3_calc "$t2 - $t1")" \
  --argjson mok1 "$([ "$(lc "$OBS1")" = "$(lc "$MODEL")" ] && echo true || echo false)" \
  --argjson mok2 "$([ "$(lc "$OBS2")" = "$(lc "$MODEL")" ] && echo true || echo false)" \
  '{model:$m,fresh_session:$sid,fresh_model_ok:$mok1,fresh_s:$fresh_s,resume_rc:$rrc,resume_session:$rsid,same_session:($sid==$rsid and $sid!=""),
    resume_model_ok:$mok2,resume_s:$resume_s,resume_assistant_events:$fa,killed_rc:$krc,killed_assistant_events:$ka,killed_text_events:$kt,
    transcript_timestamps:$ts,
    killed_mid_answer:($krc==124 or $krc==137),
    kill_text_ok:(($krc==124 or $krc==137) and $kt>=1),
    resume_pass:($rrc==0 and $sid==$rsid and $sid!="" and $mok2 and ($ts==true)),
    pass:($rrc==0 and $sid==$rsid and $sid!="" and $mok2 and ($ts==true) and ($m!="gpt-6-luna" or (($krc==124 or $krc==137) and $kt>=1)))}' | tee "$O/result.json"
