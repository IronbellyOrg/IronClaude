#!/usr/bin/env bash
# reqs3-actrate.sh <model> [--root R1] [--sb SB] [--projects DIR] [--n 3]   (Gate 0, REQ-S3; DESIGN.md 6.3; recorded, not gated)
# Three concurrent sessions per model with the real A1 brief (config/brief.txt) on the DS candidate. The probe hook (probe-hook.sh reqs3)
# injects "run `ls /tmp/panel-probe`" after main-chain tool call 3 and finish_text after call 8. Per session:
#   item act = the very next main-chain call (call 4) is a Bash command that runs `ls /tmp/panel-probe`;
#   item act_within = any later call does;  finish act = at most 1 further main-chain call after the finish text.
# Rates are computed over the sessions that reached the injection. Writes spikes/reqs3/<model>.json and rebuilds spikes/reqs3.json
# (one object per model). These replace the planning act rates 0.5-0.8 of Redesign 1 (f) (R-47). Deletes only its own session files (R-46).
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
SB=/tmp/evalsb-collab-r1; PROJ=$HOME/.claude/projects; N=3
MODEL=${1:?usage: reqs3-actrate.sh <model> [--root R1] [--sb SB] [--projects DIR] [--n 3]}; shift
RECOMPUTE=0
while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; --projects) PROJ=$2; shift 2;; --n) N=$2; shift 2;; --recompute) RECOMPUTE=1; shift;; *) echo "bad arg $1" >&2; exit 2;; esac; done
export NOFALLBACK=1
PROBE_RE='(^|[;&|] *)ls( +-[A-Za-z]+)* +/tmp/panel-probe'  # ls, ls -l, ls -la ... of the probe directory
DS=TASK-WF-designSpec-20261107-075614
CWD=$SB/$DS/repo; [ -d "$CWD" ] || { echo "FAIL build the sandbox first: sandbox.sh $DS" >&2; exit 1; }
CAND=$SB/cand/$DS/candidate.md; SRC=$SB/cand/$DS/source.md
OUT=$R1/spikes/reqs3; W=$SB/reqs3/$MODEL; [ $RECOMPUTE = 1 ] || rm -rf "$W"; mkdir -p "$OUT" "$W" /tmp/panel-probe  # --recompute: rebuild the record from the saved working files, no new session
BRIEF=$(cat "$R1/config/brief.txt")
BRIEF=${BRIEF//@@CAND@@/$CAND}; BRIEF=${BRIEF//@@SRC@@/$SRC}
BRIEF=${BRIEF//@@SHA@@/$(sha256sum "$CAND" | cut -d' ' -f1)}; BRIEF=${BRIEF//@@SRCSHA@@/$(sha256sum "$SRC" | cut -d' ' -f1)}
for ((i = 1; i <= N && RECOMPUTE == 0; i++)); do
  D=$W/s$i; mkdir -p "$D"
  SETTINGS=$(jq -n -c --arg a "bash $R1/spikes/probe-hook.sh $D reqs3 $R1/config/catalogue.json" \
    '{hooks:{PostToolUse:[{matcher:"*",hooks:[{type:"command",command:$a,timeout:5}]}]}}')
  ( S=$(date +%s%3N); cd "$CWD" && timeout --kill-after=5 600 claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions \
      --disallowedTools Edit Write NotebookEdit --settings "$SETTINGS" <<<"$BRIEF" > "$D/out.json" 2> "$D/err.txt"; echo "$? $(( $(date +%s%3N) - S ))" > "$D/rc" ) &
done
wait
SESS='[]'
for ((i = 1; i <= N; i++)); do
  D=$W/s$i; read -r RC WALL < "$D/rc" 2>/dev/null || { RC=-1; WALL=0; }
  SID=$(jq -r '[.[]|select(.type=="result")|.session_id]|.[0] // ""' "$D/out.json" 2>/dev/null)
  OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$D/out.json" 2>/dev/null)
  MAIN=$(jq -s '[.[]|select(.sub==false)]|length' "$D/tele.jsonl" 2>/dev/null || echo 0)
  ITEM=$(grep -c ' item$' "$D/inject.log" 2>/dev/null); FIN=$(grep -c ' finish$' "$D/inject.log" 2>/dev/null)
  ACT=$(jq -s --arg re "$PROBE_RE" '[.[]|select(.n==4 and .tool=="Bash" and (.cmd|test($re)))]|length' "$D/tele.jsonl" 2>/dev/null || echo 0)
  ACTW=$(jq -s --arg re "$PROBE_RE" '[.[]|select(.n != null and .n>4 and .tool=="Bash" and (.cmd|test($re)))]|length' "$D/tele.jsonl" 2>/dev/null || echo 0)
  AFTER=$(jq -s '[.[]|select(.n != null and .n>8)]|length' "$D/tele.jsonl" 2>/dev/null || echo 0)
  SESS=$(jq -c --arg sid "$SID" --arg obs "$OBS" --argjson rc "$RC" --argjson wall "$WALL" --argjson main "$MAIN" --argjson item "${ITEM:-0}" \
    --argjson fin "${FIN:-0}" --argjson act "${ACT:-0}" --argjson actw "${ACTW:-0}" --argjson after "${AFTER:-0}" \
    '. + [{session_id:$sid, observed_model:$obs, exit:$rc, wall_ms:$wall, main_calls:$main, item_injected:($item>0), item_acted_next_call:($act>0),
           item_acted_later:($actw>0), finish_injected:($fin>0), further_calls_after_finish:$after, finish_acted:($fin>0 and $after<=1),
           session_ended_at_finish_call:($fin>0 and $after==0)}]' <<<"$SESS")  # limit: a session that simply ends at call 8 also counts as acted
done
jq -n -c --arg m "$MODEL" --argjson s "$SESS" '
  ($s|map(select(.item_injected))) as $i | ($s|map(select(.finish_injected))) as $f |
  {model:$m, sessions:$s, n_sessions:($s|length), item_reached:($i|length), item_act_rate:(if ($i|length)==0 then null else ($i|map(select(.item_acted_next_call))|length)/($i|length) end),
   item_act_rate_within_session:(if ($i|length)==0 then null else ($i|map(select(.item_acted_next_call or .item_acted_later))|length)/($i|length) end),
   finish_reached:($f|length), finish_act_rate:(if ($f|length)==0 then null else ($f|map(select(.finish_acted))|length)/($f|length) end)}' > "$OUT/$MODEL.json"
jq -s 'map({(.model):.})|add' "$OUT"/*.json > "$R1/spikes/reqs3.json"
ENC=$(printf '%s' "$CWD" | sed 's/[^A-Za-z0-9]/-/g')
for ID in $(jq -r '.sessions[].session_id' "$OUT/$MODEL.json"); do case $ID in ''|*/*|*..*) ;; *) F=$PROJ/$ENC/$ID.jsonl; [ -f "$F" ] && [ ! -L "$F" ] && rm -f -- "$F";; esac; done
jq -c 'del(.sessions)' "$OUT/$MODEL.json"
