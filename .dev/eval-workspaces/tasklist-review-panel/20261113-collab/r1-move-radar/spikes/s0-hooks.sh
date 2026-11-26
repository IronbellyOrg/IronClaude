#!/usr/bin/env bash
# s0-hooks.sh <model> [--root R1] [--sb SB] [--projects DIR]   (Gate 0, S0; DESIGN.md 6.3, Adaptation A-7)
# One probe session (3 Bash calls, one subagent, a final report) in SB/<DS>/repo with a --settings JSON holding two PostToolUse
# handlers: probe-hook.sh log (returns an additionalContext, snapshots the transcript) and probe-hook.sh sleep (past its 1 s timeout).
# Writes spikes/s0/<model>.json = {"model","pass","checks":{...},"hook_ms_p95","hooks_lists":{...},"session_id",...}.
# pass = hook stdin carries tool_name, tool_input and transcript_path on every call AND the subagent question is settled (its calls
# reach the hook WITH agent_id, or do not reach it; reaching without agent_id fails; not observed fails) AND a snapshot was written
# and hashed AND the session survived the over-timeout hook AND the additionalContext reached the session transcript.
# Deletes only the session file whose id it recorded (R-46).
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
SB=/tmp/evalsb-collab-r1; PROJ=$HOME/.claude/projects
MODEL=${1:?usage: s0-hooks.sh <model> [--root R1] [--sb SB] [--projects DIR]}; shift
while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; --projects) PROJ=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
export NOFALLBACK=1
DS=TASK-WF-designSpec-20261107-075614
CWD=$SB/$DS/repo; [ -d "$CWD" ] || { echo "FAIL build the sandbox first: sandbox.sh $DS" >&2; exit 1; }
OUT=$R1/spikes/s0; W=$SB/s0/$MODEL; rm -rf "$W"; mkdir -p "$OUT" "$W"
HOOK=$R1/spikes/probe-hook.sh
SETTINGS=$(jq -n -c --arg a "bash $HOOK $W log" --arg b "bash $HOOK $W sleep" \
  '{hooks:{PostToolUse:[{matcher:"*",hooks:[{type:"command",command:$a,timeout:5},{type:"command",command:$b,timeout:1}]}]}}')
PROMPT='This is a hook probe, not a review. Do exactly this, in order. 1) With the Bash tool run `ls`. 2) With the Bash tool run `pwd`. 3) With the Bash tool run `echo probe`. 4) Use the Agent tool (also called Task) once to start a subagent whose only job is to run `ls /tmp` with its Bash tool and report the first line. 5) Finish with one line that starts with SAW: followed by every PROBE-CONTEXT-<number> token that appeared in the tool results or system messages you were shown, separated by spaces, or SAW: none.'
S=$(date +%s%3N)
( cd "$CWD" && timeout --kill-after=5 420 claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions \
    --disallowedTools Edit Write NotebookEdit --settings "$SETTINGS" <<<"$PROMPT" ) > "$W/out.json" 2> "$W/err.txt"
RC=$?; WALL=$(( $(date +%s%3N) - S ))
RES=$(jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$W/out.json" 2>/dev/null)
SID=$(jq -r '[.[]|select(.type=="result")|.session_id]|.[0] // ""' "$W/out.json" 2>/dev/null)
OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$W/out.json" 2>/dev/null)
NSTDIN=$(ls "$W"/stdin.*.json 2>/dev/null | wc -l)
FIELDS=false; [ "$NSTDIN" -gt 0 ] && jq -s -e 'all(.[]; has("tool_name") and has("tool_input") and has("transcript_path"))' "$W"/stdin.*.json >/dev/null 2>&1 && FIELDS=true
NSUB=$(jq -s '[.[]|select(.agent_id != null)]|length' "$W"/stdin.*.json 2>/dev/null || echo 0)
NAGENT=$(jq -s '[.[]|select(.agent_id == null and (.tool_name=="Agent" or .tool_name=="Task"))]|length' "$W"/stdin.*.json 2>/dev/null || echo 0)
NLS_SUB=$(jq -s '[.[]|select(.tool_name=="Bash" and ((.tool_input.command // "")|test("ls /tmp")) and .agent_id != null)]|length' "$W"/stdin.*.json 2>/dev/null || echo 0)
NLS_MAIN=$(jq -s '[.[]|select(.tool_name=="Bash" and ((.tool_input.command // "")|test("ls /tmp")) and .agent_id == null)]|length' "$W"/stdin.*.json 2>/dev/null || echo 0)
if [ "$NLS_SUB" -gt 0 ]; then SUBST=reaches_with_agent_id
elif [ "$NLS_MAIN" -gt 0 ]; then SUBST=reaches_without_agent_id
elif [ "$NAGENT" -gt 0 ]; then SUBST=does_not_reach
else SUBST=not_observed; fi
SNAP=false; [ -s "$W/snap.sha" ] && SNAP=true
LASTSNAP=$(ls "$W"/snap.*.jsonl 2>/dev/null | sort -t. -k2 -n | tail -1)
CTX=false; [ -n "$LASTSNAP" ] && grep -q 'PROBE-CONTEXT-' "$LASTSNAP" && CTX=true
SAW=false; grep -q 'SAW:.*PROBE-CONTEXT' <<<"$RES" && SAW=true
SLEEPS=$( [ -f "$W/sleep.started" ] && wc -l < "$W/sleep.started" || echo 0 )
SURV=false; [ "$(jq -r '[.[]|select(.type=="result")|.subtype]|.[0] // ""' "$W/out.json" 2>/dev/null)" = success ] && [ "$SLEEPS" -gt 0 ] && SURV=true
P95=$(jq -s 'sort|if length==0 then null else .[((length*0.95|ceil)-1)] end' "$W/t.log" 2>/dev/null || echo null)
# hooks other than ours: keys of the user and sandbox settings, and PostToolUse additionalContext seen from anything but our probe
UH=$(jq -c '.hooks|keys' "$HOME/.claude/settings.json" 2>/dev/null || echo null)
SH=$(jq -c '.hooks|keys' "$CWD/.claude/settings.json" 2>/dev/null || echo null)
OTHER_CTX=0; [ -n "$LASTSNAP" ] && OTHER_CTX=$(jq -s '[.[]|select(.type=="attachment" and .attachment.type=="hook_additional_context" and .attachment.hookEvent=="PostToolUse" and (tostring|test("PROBE-CONTEXT")|not))]|length' "$LASTSNAP" 2>/dev/null || echo 0)
MODEL_OK=false; lo=$(tr 'A-Z' 'a-z' <<<"$OBS"); le=$(tr 'A-Z' 'a-z' <<<"$MODEL"); { [ "$lo" = "$le" ] || [ "$lo" = "$le-build" ]; } && MODEL_OK=true
PASS=false; $FIELDS && $SNAP && $SURV && $CTX && $MODEL_OK && { [ "$SUBST" = reaches_with_agent_id ] || [ "$SUBST" = does_not_reach ]; } && PASS=true
jq -n -c --arg m "$MODEL" --argjson pass $PASS --argjson fields $FIELDS --argjson snap $SNAP --argjson surv $SURV --argjson ctx $CTX --argjson saw $SAW \
  --argjson modelok $MODEL_OK --arg subst "$SUBST" --argjson nsub "$NSUB" --argjson nstdin "$NSTDIN" --argjson sleeps "$SLEEPS" --argjson p95 "${P95:-null}" \
  --arg obs "$OBS" --arg sid "$SID" --argjson rc $RC --argjson wall "$WALL" --arg res "$RES" --argjson uh "${UH:-null}" --argjson sh "${SH:-null}" \
  --argjson other "$OTHER_CTX" \
  '{model:$m, pass:$pass, observed_model:$obs, model_ok:$modelok, session_id:$sid, exit:$rc, wall_ms:$wall,
    checks:{stdin_fields_ok:$fields, hook_calls:$nstdin, subagent_status:$subst, subagent_hook_calls_with_agent_id:$nsub, snapshot_hashed:$snap,
            survived_over_timeout_hook:$surv, sleeper_started:$sleeps, context_in_transcript:$ctx, model_repeated_context:$saw,
            other_hook_additional_context_entries:$other},
    hook_ms_p95:$p95, hooks_lists:{user_settings:$uh, sandbox_settings:$sh}, final_text:$res}' > "$OUT/$MODEL.json"
# R-46: delete only this probe's own session file
ENC=$(printf '%s' "$CWD" | sed 's/[^A-Za-z0-9]/-/g')
case $SID in ''|*/*|*..*) ;; *) F=$PROJ/$ENC/$SID.jsonl; [ -f "$F" ] && [ ! -L "$F" ] && rm -f -- "$F";; esac
jq -c '{model,pass,checks,hook_ms_p95}' "$OUT/$MODEL.json"
