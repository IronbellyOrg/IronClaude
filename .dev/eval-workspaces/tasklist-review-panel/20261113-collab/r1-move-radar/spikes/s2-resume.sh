#!/usr/bin/env bash
# s2-resume.sh <model> [--root R1] [--sb SB] [--projects DIR]   (Gate 0, S2; DESIGN.md 6.3, Adaptation A-7)
# A short `claude -p` (session persistence on) that is told a code word, then `claude -p --resume <session_id>` with
# --output-format stream-json --verbose (exactly the H2 re-ask form of run-reviewer.sh) that is asked for it. Writes spikes/s2/<model>.json.
# pass = the resume reply contains the code word (the same session answered), the `result` event of the stream is parsed by the
# `jq -s` filter of the H2 re-ask, and the first attempt used the right model. Records the resume start time (planning value 6 s).
# Deletes only the session files whose ids it recorded (R-46).
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
SB=/tmp/evalsb-collab-r1; PROJ=$HOME/.claude/projects
MODEL=${1:?usage: s2-resume.sh <model> [--root R1] [--sb SB] [--projects DIR]}; shift
while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; --projects) PROJ=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
export NOFALLBACK=1
DS=TASK-WF-designSpec-20261107-075614
CWD=$SB/$DS/repo; [ -d "$CWD" ] || { echo "FAIL build the sandbox first: sandbox.sh $DS" >&2; exit 1; }
OUT=$R1/spikes/s2; W=$SB/s2/$MODEL; rm -rf "$W"; mkdir -p "$OUT" "$W"
WORD=ORCHID-$RANDOM
S1=$(date +%s%3N)
( cd "$CWD" && timeout --kill-after=5 240 claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions \
    --disallowedTools Edit Write NotebookEdit <<<"Remember the code word $WORD. Reply with the single word OK." ) > "$W/first.json" 2> "$W/first.err"
RC1=$?; WALL1=$(( $(date +%s%3N) - S1 ))
SID=$(jq -r '[.[]|select(.type=="result")|.session_id]|.[0] // ""' "$W/first.json" 2>/dev/null)
OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$W/first.json" 2>/dev/null)
RES=""; RC2=null; FIRST_EVENT_MS=null; WALL2=null; PARSED=false; RSID=""
if [ -n "$SID" ]; then
  S2=$(date +%s%3N)
  ( cd "$CWD" && timeout --kill-after=5 240 claude -p --resume "$SID" --model "$MODEL" --output-format stream-json --verbose \
      --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"What was the code word? Reply with only the code word." ) \
      2> "$W/resume.err" | while IFS= read -r line; do printf '%s\n' "$line"; [ -f "$W/.first" ] || { echo $(( $(date +%s%3N) - S2 )) > "$W/.first"; }; done > "$W/resume.json"
  RC2=${PIPESTATUS[0]}; WALL2=$(( $(date +%s%3N) - S2 )); FIRST_EVENT_MS=$(cat "$W/.first" 2>/dev/null || echo null)
  RES=$(jq -s -r '[.[]|select(.type=="result")|.result][0] // ""' "$W/resume.json" 2>/dev/null) && PARSED=true
  RSID=$(jq -s -r '[.[]|select(.type=="result")|.session_id][0] // ""' "$W/resume.json" 2>/dev/null)
fi
SAME=false; grep -q "$WORD" <<<"$RES" && SAME=true
MODEL_OK=false; lo=$(tr 'A-Z' 'a-z' <<<"$OBS"); le=$(tr 'A-Z' 'a-z' <<<"$MODEL"); { [ "$lo" = "$le" ] || [ "$lo" = "$le-build" ]; } && MODEL_OK=true
PASS=false; $SAME && $PARSED && $MODEL_OK && PASS=true
jq -n -c --arg m "$MODEL" --argjson pass $PASS --argjson same $SAME --argjson parsed $PARSED --argjson modelok $MODEL_OK --arg obs "$OBS" \
  --arg sid "$SID" --arg rsid "$RSID" --arg word "$WORD" --arg res "$RES" --argjson w1 $WALL1 --argjson w2 "$WALL2" --argjson fe "$FIRST_EVENT_MS" \
  --argjson rc1 $RC1 --argjson rc2 "$RC2" \
  '{model:$m, pass:$pass, observed_model:$obs, model_ok:$modelok, first_session_id:$sid, resume_session_id:$rsid, code_word:$word,
    resume_reply:$res, answered_in_same_session:$same, result_event_parsed_by_jq_s:$parsed, first_wall_ms:$w1, resume_wall_ms:$w2,
    resume_first_event_ms:$fe, exit_first:$rc1, exit_resume:$rc2}' > "$OUT/$MODEL.json"
# R-46: delete only the session files this spike recorded
ENC=$(printf '%s' "$CWD" | sed 's/[^A-Za-z0-9]/-/g')
for ID in $SID $RSID; do case $ID in ''|*/*|*..*) ;; *) F=$PROJ/$ENC/$ID.jsonl; [ -f "$F" ] && [ ! -L "$F" ] && rm -f -- "$F";; esac; done
jq -c . "$OUT/$MODEL.json"
