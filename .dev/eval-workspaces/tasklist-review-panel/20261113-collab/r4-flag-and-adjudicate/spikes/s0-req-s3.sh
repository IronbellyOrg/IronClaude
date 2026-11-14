#!/usr/bin/env bash
# s0-req-s3.sh <model> [sessions=5]: spikes S0 and REQ-S3 for one model (design 6.3). Real model calls:
# run it under the shared gateway lock:  flock /tmp/collab-gateway.lock spikes/s0-req-s3.sh <model>
# Session 1 also carries the S0-only checks (failing tool call, subagent). Writes spikes/out/s0-<model>.json
# and merges the act rates into spikes/out/act-rates.json.
set -u -o pipefail
MODEL=$1; NS=${2:-5}
HERE=$(cd "$(dirname "$0")/.." && pwd)
SBR=${R4_SBR:-/tmp/evalsb-collab-r4}
SB="$SBR/sb/TASK-WF-designSpec-20261107-075614/repo"
OUTD="$HERE/spikes/out"; mkdir -p "$OUTD"
WORK=/tmp/collab-r4/s0-$MODEL-$(date +%s); mkdir -p "$WORK"
[ "${NOFALLBACK:-}" = 1 ] || { echo "NOFALLBACK=1 required" >&2; exit 2; }
jq -e --arg m "$MODEL" '.allowed_models|index([$m])' "$HERE/frozen/panels.json" >/dev/null || { echo "model not allowed" >&2; exit 2; }
[ -d "$SB" ] || { echo "sandbox missing: run bin/build-sandbox.sh" >&2; exit 2; }
STEPS='Do the following steps one at a time, exactly one tool call per step, in this order:
1. Run `ls`.
2. Run `head -5 README.md`.
3. Run `pwd`.
4. Run `ls docs | head -5`.
5. Run `ls /nonexistent-panel-probe-dir` (it fails; that is expected).
6. Run `date`.
7. Run `git log --oneline -1`.
8. Run `wc -l README.md`.'
RESULTS="[]"
for s in $(seq 1 "$NS"); do
  L="$WORK/sess$s"; mkdir -p "$L"
  jq -n --arg c "$HERE/spikes/probe-hook --log $L" '{hooks:{PostToolUse:[{hooks:[{type:"command",command:$c,timeout:10}]}]}}' > "$L/settings.json"
  BRIEF="$STEPS"
  [ "$s" = 1 ] && BRIEF="$BRIEF
9. Use the Task tool to start one subagent whose only job is to run \`echo sub-ok\`."
  BRIEF="$BRIEF
Then reply DONE."
  SID=$(cat /proc/sys/kernel/random/uuid)
  ( cd "$SB" && timeout 600 claude -p --model "$MODEL" --output-format json --session-id "$SID" --permission-mode bypassPermissions \
      --disallowedTools Edit Write NotebookEdit --settings "$L/settings.json" <<<"$BRIEF" ) > "$L/out.json" 2> "$L/err.txt" &
  P=$!
  # while it runs: the launcher's concurrency count and the real process argv (does the wrapper add --settings?)
  sleep 8
  "$HERE/bin/run-panel.sh" --print-session-count > "$L/count.txt"
  pgrep -af "session-id $SID" > "$L/ps.txt" || true
  wait $P; RC=$?
  TR=$(find "$HOME/.claude/projects" -maxdepth 2 -name "$SID.jsonl" | head -1)
  [ -n "$TR" ] && cp "$TR" "$L/transcript.jsonl"
  OBS=$(jq -r '[.[]|select(.type=="assistant" and .parent_tool_use_id==null)|.message.model]|unique|join(",")' "$L/out.json" 2>/dev/null)
  if [ ! -s "$L/inputs.jsonl" ]; then  # the session never made a hooked tool call (e.g. the claude binary was missing)
    RESULTS=$(jq -c --argjson s "$s" --argjson rc "$RC" --arg e "$(head -c 300 "$L/err.txt")" '. + [{session:$s,rc:$rc,usable:false,error:$e}]' <<<"$RESULTS")
    continue
  fi
  # act rate: the main-thread tool call right after call 3 (the injection) is `ls /tmp/panel-probe`
  ACT=$(jq -s '[.[]|select(.agent_id==null)] as $m | ($m|map(select(.n==4))|.[0].tool_input.command // "") | test("ls\\s+/tmp/panel-probe")' "$L/inputs.jsonl")
  # finish act: no main-thread tool call after the finish text injected at call 6. A failing call fires no
  # PostToolUse (S0 finding), so "calls <= 7" would wrongly count a session that ran every remaining step.
  MAXN=$(jq -s '[.[]|select(.agent_id==null)|.n]|max // 0' "$L/inputs.jsonl")
  FIN=false; [ "$MAXN" -le 6 ] && FIN=true
  S0=$(jq -n --arg tr "$L/transcript.jsonl" --slurpfile in <(cat "$L/inputs.jsonl" 2>/dev/null || true) --arg snap "$(cat "$L/snap.status" 2>/dev/null)" \
    --arg count "$(cat "$L/count.txt")" --arg ps "$(cat "$L/ps.txt")" --arg obs "$OBS" --argjson rc "$RC" --argjson act "$ACT" --argjson fin $FIN '
    ($in|map(select(.agent_id==null))) as $m |
    {session:'"$s"', usable:true, rc:$rc, observed_model:$obs, hook_inputs:($in|length), main_calls:($m|length),
     transcript_path_readable:([$m[]|.transcript_readable]|all), snapshot_at_call2:$snap,
     hook_ms_p95:([$m[].hook_ms]|sort|if length>0 then .[((length*95+99)/100|floor)-1] else null end),
     failing_call_fired:([$in[]|select((.tool_input.command//"")|test("nonexistent-panel-probe"))]|length>0),
     subagent_calls:([$in[]|select(.agent_id!=null)]|length),
     session_count_during_run:$count, real_process_argv:$ps,
     settings_flags_in_argv:($ps|[scan("--settings")]|length), act:$act, finish_act:$fin}')
  if [ -f "$L/transcript.jsonl" ]; then
    S0=$(jq -c --slurpfile t "$L/transcript.jsonl" '. + {
      transcript_entries_with_timestamp:([$t[]|select(.timestamp)]|length),
      assistant_messages_split:([$t[]|select(.type=="assistant")|.message.id]|group_by(.)|map(select(length>1))|length),
      tool_result_inside_split_message:([$t[]|select(.timestamp)] as $a
        | [$a|to_entries[]|select(.value.type=="assistant")|{i:.key,id:.value.message.id}] | group_by(.id) | map(select(length>1))
        | map((map(.i)|min) as $lo | (map(.i)|max) as $hi | [$a[$lo:$hi][]|select(.type=="user")]|length>0) | any),
      hook_related_entries:([$t[]|select(tostring|test("hook";"i"))|.type]|unique)}' <<<"$S0")
  fi
  RESULTS=$(jq -c --argjson r "$S0" '. + [$r]' <<<"$RESULTS")
done
HOOKS_IN_SB=$(jq -c '.hooks|keys' "$SB/.claude/settings.json" 2>/dev/null || echo null)
jq -n --arg m "$MODEL" --argjson r "$RESULTS" --argjson sbh "$HOOKS_IN_SB" --arg w "$WORK" '[$r[]|select(.usable)] as $u |
  {model:$m, work_dir:$w, sandbox_project_hook_events:$sbh, sessions:$r, usable_sessions:($u|length),
   pass:(($u|length)>0 and ($u|map(.main_calls>=6 and .transcript_path_readable and .snapshot_at_call2=="ok")|all)),
   act_rate:(if ($u|length)>0 then ($u|map(select(.act))|length)/($u|length) else null end),
   finish_act_rate:(if ($u|length)>0 then ($u|map(select(.finish_act))|length)/($u|length) else null end)}' > "$OUTD/s0-$MODEL.json"
AR="$OUTD/act-rates.json"; [ -f "$AR" ] || echo '{}' > "$AR"
jq --arg m "$MODEL" --slurpfile s "$OUTD/s0-$MODEL.json" '. + {($m):{sessions:$s[0].usable_sessions,act_rate:$s[0].act_rate,finish_act_rate:$s[0].finish_act_rate}}' "$AR" > "$AR.tmp" && mv "$AR.tmp" "$AR"
jq -c '{model,pass,act_rate,finish_act_rate}' "$OUTD/s0-$MODEL.json"
