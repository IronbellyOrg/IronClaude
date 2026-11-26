eeb3226713ddfe56ec1b0ab41b1b3b0439d77286
Review one task for spec compliance.

Task brief: T8 (source: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/DESIGN.md sections 1.3 and 6.3; task grouping in .dev/implement/collab-r1-move-radar/tasks.md). Covers DESIGN.md section 1.3 rows spikes/s0-hooks.sh, spikes/s2-resume.sh, spikes/reqs3-actrate.sh (plus the helper spikes/probe-hook.sh they use) and the Gate 0 spikes S0, S2 and REQ-S3 of section 6.3 on all four reviewer models (muse-ember-1.0, gpt-6-luna, claude-sonnet-5-5, claude-haiku-5-5; Adaptation A-7).
T8.AC1: Spikes run under the gateway lock; records written; gate0.json decided mechanically. Notes: the design defines no gateway lock; the executor read "gateway lock" as the orchestrator's cap of at most 3 concurrent model sessions, NOFALLBACK=1, models from the allowed list only. Records written by the executor: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s0/<model>.json, .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s2/<model>.json, .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/reqs3/<model>.json, .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/reqs3.json, and .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/gate0.json (written by the existing .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/gate0-check.sh, run after the spikes). Section 6.3 pass conditions: S0 = hook stdin has tool_name, tool_input and transcript_path for every model; a subagent probe shows whether subagent tool calls reach the hook and carry agent_id (reaching without agent_id fails S0); the snapshot is written and hashed; a hook that exceeds its timeout does not kill the session; the hooks keys of the user and sandbox settings are listed and none is a PostToolUse additionalContext producer. S2 = resume answers in the same session for all four models; the result event is parsed by the jq -s filter; the resume start time is recorded. REQ-S3 = recorded, not gated: act rate and finish act rate per model in spikes/reqs3.json (3 sessions per model with the real A1 brief on DS; the hook injects "run ls /tmp/panel-probe" at call 3 and finish_text at call 8). Spike 4 and S3 are not part of T8.
Global constraints: Orchestrator constraints (global): create and edit files only under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/ (plus .dev/implement/collab-r1-move-radar/ and scratch under /tmp/evalsb-collab-r1/ and /tmp/collab-r1/); do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder or any other redesign's folder; do not stage, commit or push; python only through uv; models allowed muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7, Opus only as the blind judge, never Qwen or glm; NOFALLBACK=1; no full panel runs; at most 3 reviewer or judge sessions at once.
Start sha: eeb3226713ddfe56ec1b0ab41b1b3b0439d77286
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/probe-hook.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/probe-hook.sh
new file mode 100755
index 000000000..d032ce0fb
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/probe-hook.sh
@@ -0,0 +1,30 @@
+#!/usr/bin/env bash
+# probe-hook.sh <logdir> <mode> [<catalogue.json>]   (Gate 0 probe hook; DESIGN.md 6.3 S0 and REQ-S3; not the radar hook)
+#   log    save stdin as stdin.<n>.json, snapshot the transcript (snap.<n>.jsonl + sha256 in snap.sha), time this call in t.log,
+#          print additionalContext "PROBE-CONTEXT-<n>"
+#   sleep  sleep 5 s (run with a 1 s hook timeout: shows that a hook past its timeout does not kill the session)
+#   reqs3  count calls in count; log {n,tool,cmd} to tele.jsonl; call 3 prints "run `ls /tmp/panel-probe`", call 8 prints finish_text
+# Always exits 0. bash, jq, flock and coreutils only.
+set -u -o pipefail
+D=${1:?logdir}; MODE=${2:?mode}; CAT=${3:-}
+mkdir -p "$D"
+ms() { date +%s%3N; }
+T0=$(ms); IN=$(head -c 1048576)
+emit() { jq -n -c --arg t "$1" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$t}}'; }
+case $MODE in
+  sleep) echo "$(ms)" >> "$D/sleep.started"; sleep 5;;
+  log)
+    n=$( { flock 9; c=$(( $(cat "$D/count" 2>/dev/null || echo 0) + 1 )); echo "$c" > "$D/count"; echo "$c"; } 9> "$D/count.lock" )
+    printf '%s' "$IN" > "$D/stdin.$n.json"
+    tp=$(printf '%s' "$IN" | jq -r '.transcript_path // empty')
+    if [ -n "$tp" ] && [ -s "$tp" ] && cp "$tp" "$D/snap.$n.jsonl"; then echo "$n $(sha256sum "$D/snap.$n.jsonl" | cut -d' ' -f1)" >> "$D/snap.sha"; fi
+    emit "PROBE-CONTEXT-$n"
+    echo "$(( $(ms) - T0 ))" >> "$D/t.log";;
+  reqs3)
+    sub=$(printf '%s' "$IN" | jq -r '.agent_id // empty')
+    n=null; [ -n "$sub" ] || n=$( { flock 9; c=$(( $(cat "$D/count" 2>/dev/null || echo 0) + 1 )); echo "$c" > "$D/count"; echo "$c"; } 9> "$D/count.lock" )
+    printf '%s' "$IN" | jq -c --argjson n "$n" --argjson t "$T0" '{n:$n,t:$t,tool:.tool_name,sub:(.agent_id != null),cmd:(.tool_input.command // .tool_input.file_path // .tool_input.pattern // "")}' >> "$D/tele.jsonl"
+    if [ -z "$sub" ] && [ "$n" = 3 ]; then emit 'Run `ls /tmp/panel-probe` with the Bash tool now, then continue your review.'; echo "$n $T0 item" >> "$D/inject.log"
+    elif [ -z "$sub" ] && [ "$n" = 8 ]; then emit "$(jq -r .finish_text "$CAT")"; echo "$n $T0 finish" >> "$D/inject.log"; fi;;
+esac
+exit 0
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/reqs3-actrate.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/reqs3-actrate.sh
new file mode 100755
index 000000000..591d3fa4f
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/reqs3-actrate.sh
@@ -0,0 +1,54 @@
+#!/usr/bin/env bash
+# reqs3-actrate.sh <model> [--root R1] [--sb SB] [--projects DIR] [--n 3]   (Gate 0, REQ-S3; DESIGN.md 6.3; recorded, not gated)
+# Three concurrent sessions per model with the real A1 brief (config/brief.txt) on the DS candidate. The probe hook (probe-hook.sh reqs3)
+# injects "run `ls /tmp/panel-probe`" after main-chain tool call 3 and finish_text after call 8. Per session:
+#   item act = the very next main-chain call (call 4) is a Bash command that runs `ls /tmp/panel-probe`;
+#   item act_within = any later call does;  finish act = at most 1 further main-chain call after the finish text.
+# Rates are computed over the sessions that reached the injection. Writes spikes/reqs3/<model>.json and rebuilds spikes/reqs3.json
+# (one object per model). These replace the planning act rates 0.5-0.8 of Redesign 1 (f) (R-47). Deletes only its own session files (R-46).
+set -u -o pipefail
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
+SB=/tmp/evalsb-collab-r1; PROJ=$HOME/.claude/projects; N=3
+MODEL=${1:?usage: reqs3-actrate.sh <model> [--root R1] [--sb SB] [--projects DIR] [--n 3]}; shift
+while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; --projects) PROJ=$2; shift 2;; --n) N=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
+export NOFALLBACK=1
+DS=TASK-WF-designSpec-20261107-075614
+CWD=$SB/$DS/repo; [ -d "$CWD" ] || { echo "FAIL build the sandbox first: sandbox.sh $DS" >&2; exit 1; }
+CAND=$SB/cand/$DS/candidate.md; SRC=$SB/cand/$DS/source.md
+OUT=$R1/spikes/reqs3; W=$SB/reqs3/$MODEL; rm -rf "$W"; mkdir -p "$OUT" "$W" /tmp/panel-probe
+BRIEF=$(cat "$R1/config/brief.txt")
+BRIEF=${BRIEF//@@CAND@@/$CAND}; BRIEF=${BRIEF//@@SRC@@/$SRC}
+BRIEF=${BRIEF//@@SHA@@/$(sha256sum "$CAND" | cut -d' ' -f1)}; BRIEF=${BRIEF//@@SRCSHA@@/$(sha256sum "$SRC" | cut -d' ' -f1)}
+for ((i = 1; i <= N; i++)); do
+  D=$W/s$i; mkdir -p "$D"
+  SETTINGS=$(jq -n -c --arg a "bash $R1/spikes/probe-hook.sh $D reqs3 $R1/config/catalogue.json" \
+    '{hooks:{PostToolUse:[{matcher:"*",hooks:[{type:"command",command:$a,timeout:5}]}]}}')
+  ( S=$(date +%s%3N); cd "$CWD" && timeout --kill-after=5 600 claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions \
+      --disallowedTools Edit Write NotebookEdit --settings "$SETTINGS" <<<"$BRIEF" > "$D/out.json" 2> "$D/err.txt"; echo "$? $(( $(date +%s%3N) - S ))" > "$D/rc" ) &
+done
+wait
+SESS='[]'
+for ((i = 1; i <= N; i++)); do
+  D=$W/s$i; read -r RC WALL < "$D/rc" 2>/dev/null || { RC=-1; WALL=0; }
+  SID=$(jq -r '[.[]|select(.type=="result")|.session_id]|.[0] // ""' "$D/out.json" 2>/dev/null)
+  OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$D/out.json" 2>/dev/null)
+  MAIN=$(jq -s '[.[]|select(.sub==false)]|length' "$D/tele.jsonl" 2>/dev/null || echo 0)
+  ITEM=$(grep -c ' item$' "$D/inject.log" 2>/dev/null); FIN=$(grep -c ' finish$' "$D/inject.log" 2>/dev/null)
+  ACT=$(jq -s '[.[]|select(.n==4 and .tool=="Bash" and (.cmd|test("ls /tmp/panel-probe")))]|length' "$D/tele.jsonl" 2>/dev/null || echo 0)
+  ACTW=$(jq -s '[.[]|select(.n != null and .n>4 and .tool=="Bash" and (.cmd|test("ls /tmp/panel-probe")))]|length' "$D/tele.jsonl" 2>/dev/null || echo 0)
+  AFTER=$(jq -s '[.[]|select(.n != null and .n>8)]|length' "$D/tele.jsonl" 2>/dev/null || echo 0)
+  SESS=$(jq -c --arg sid "$SID" --arg obs "$OBS" --argjson rc "$RC" --argjson wall "$WALL" --argjson main "$MAIN" --argjson item "${ITEM:-0}" \
+    --argjson fin "${FIN:-0}" --argjson act "${ACT:-0}" --argjson actw "${ACTW:-0}" --argjson after "${AFTER:-0}" \
+    '. + [{session_id:$sid, observed_model:$obs, exit:$rc, wall_ms:$wall, main_calls:$main, item_injected:($item>0), item_acted_next_call:($act>0),
+           item_acted_later:($actw>0), finish_injected:($fin>0), further_calls_after_finish:$after, finish_acted:($fin>0 and $after<=1)}]' <<<"$SESS")
+done
+jq -n -c --arg m "$MODEL" --argjson s "$SESS" '
+  ($s|map(select(.item_injected))) as $i | ($s|map(select(.finish_injected))) as $f |
+  {model:$m, sessions:$s, n_sessions:($s|length), item_reached:($i|length), item_act_rate:(if ($i|length)==0 then null else ($i|map(select(.item_acted_next_call))|length)/($i|length) end),
+   item_act_rate_within_session:(if ($i|length)==0 then null else ($i|map(select(.item_acted_next_call or .item_acted_later))|length)/($i|length) end),
+   finish_reached:($f|length), finish_act_rate:(if ($f|length)==0 then null else ($f|map(select(.finish_acted))|length)/($f|length) end)}' > "$OUT/$MODEL.json"
+jq -s 'map({(.model):.})|add' "$OUT"/*.json > "$R1/spikes/reqs3.json"
+ENC=$(printf '%s' "$CWD" | sed 's/[^A-Za-z0-9]/-/g')
+for ID in $(jq -r '.sessions[].session_id' "$OUT/$MODEL.json"); do case $ID in ''|*/*|*..*) ;; *) F=$PROJ/$ENC/$ID.jsonl; [ -f "$F" ] && [ ! -L "$F" ] && rm -f -- "$F";; esac; done
+jq -c 'del(.sessions)' "$OUT/$MODEL.json"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s0-hooks.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s0-hooks.sh
new file mode 100755
index 000000000..e6e27b9fc
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s0-hooks.sh
@@ -0,0 +1,66 @@
+#!/usr/bin/env bash
+# s0-hooks.sh <model> [--root R1] [--sb SB] [--projects DIR]   (Gate 0, S0; DESIGN.md 6.3, Adaptation A-7)
+# One probe session (3 Bash calls, one subagent, a final report) in SB/<DS>/repo with a --settings JSON holding two PostToolUse
+# handlers: probe-hook.sh log (returns an additionalContext, snapshots the transcript) and probe-hook.sh sleep (past its 1 s timeout).
+# Writes spikes/s0/<model>.json = {"model","pass","checks":{...},"hook_ms_p95","hooks_lists":{...},"session_id",...}.
+# pass = hook stdin carries tool_name, tool_input and transcript_path on every call AND the subagent question is settled (its calls
+# reach the hook WITH agent_id, or do not reach it; reaching without agent_id fails; not observed fails) AND a snapshot was written
+# and hashed AND the session survived the over-timeout hook AND the additionalContext reached the session transcript.
+# Deletes only the session file whose id it recorded (R-46).
+set -u -o pipefail
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
+SB=/tmp/evalsb-collab-r1; PROJ=$HOME/.claude/projects
+MODEL=${1:?usage: s0-hooks.sh <model> [--root R1] [--sb SB] [--projects DIR]}; shift
+while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; --projects) PROJ=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
+export NOFALLBACK=1
+DS=TASK-WF-designSpec-20261107-075614
+CWD=$SB/$DS/repo; [ -d "$CWD" ] || { echo "FAIL build the sandbox first: sandbox.sh $DS" >&2; exit 1; }
+OUT=$R1/spikes/s0; W=$SB/s0/$MODEL; rm -rf "$W"; mkdir -p "$OUT" "$W"
+HOOK=$R1/spikes/probe-hook.sh
+SETTINGS=$(jq -n -c --arg a "bash $HOOK $W log" --arg b "bash $HOOK $W sleep" \
+  '{hooks:{PostToolUse:[{matcher:"*",hooks:[{type:"command",command:$a,timeout:5},{type:"command",command:$b,timeout:1}]}]}}')
+PROMPT='This is a hook probe, not a review. Do exactly this, in order. 1) With the Bash tool run `ls`. 2) With the Bash tool run `pwd`. 3) With the Bash tool run `echo probe`. 4) Use the Agent tool (also called Task) once to start a subagent whose only job is to run `ls /tmp` with its Bash tool and report the first line. 5) Finish with one line that starts with SAW: followed by every PROBE-CONTEXT-<number> token that appeared in the tool results or system messages you were shown, separated by spaces, or SAW: none.'
+S=$(date +%s%3N)
+( cd "$CWD" && timeout --kill-after=5 420 claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions \
+    --disallowedTools Edit Write NotebookEdit --settings "$SETTINGS" <<<"$PROMPT" ) > "$W/out.json" 2> "$W/err.txt"
+RC=$?; WALL=$(( $(date +%s%3N) - S ))
+RES=$(jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$W/out.json" 2>/dev/null)
+SID=$(jq -r '[.[]|select(.type=="result")|.session_id]|.[0] // ""' "$W/out.json" 2>/dev/null)
+OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$W/out.json" 2>/dev/null)
+NSTDIN=$(ls "$W"/stdin.*.json 2>/dev/null | wc -l)
+FIELDS=false; [ "$NSTDIN" -gt 0 ] && jq -s -e 'all(.[]; has("tool_name") and has("tool_input") and has("transcript_path"))' "$W"/stdin.*.json >/dev/null 2>&1 && FIELDS=true
+NSUB=$(jq -s '[.[]|select(.agent_id != null)]|length' "$W"/stdin.*.json 2>/dev/null || echo 0)
+NAGENT=$(jq -s '[.[]|select(.agent_id == null and (.tool_name=="Agent" or .tool_name=="Task"))]|length' "$W"/stdin.*.json 2>/dev/null || echo 0)
+NLS_SUB=$(jq -s '[.[]|select(.tool_name=="Bash" and ((.tool_input.command // "")|test("ls /tmp")) and .agent_id != null)]|length' "$W"/stdin.*.json 2>/dev/null || echo 0)
+NLS_MAIN=$(jq -s '[.[]|select(.tool_name=="Bash" and ((.tool_input.command // "")|test("ls /tmp")) and .agent_id == null)]|length' "$W"/stdin.*.json 2>/dev/null || echo 0)
+if [ "$NLS_SUB" -gt 0 ]; then SUBST=reaches_with_agent_id
+elif [ "$NLS_MAIN" -gt 0 ]; then SUBST=reaches_without_agent_id
+elif [ "$NAGENT" -gt 0 ]; then SUBST=does_not_reach
+else SUBST=not_observed; fi
+SNAP=false; [ -s "$W/snap.sha" ] && SNAP=true
+LASTSNAP=$(ls "$W"/snap.*.jsonl 2>/dev/null | sort -t. -k2 -n | tail -1)
+CTX=false; [ -n "$LASTSNAP" ] && grep -q 'PROBE-CONTEXT-' "$LASTSNAP" && CTX=true
+SAW=false; grep -q 'SAW:.*PROBE-CONTEXT' <<<"$RES" && SAW=true
+SLEEPS=$( [ -f "$W/sleep.started" ] && wc -l < "$W/sleep.started" || echo 0 )
+SURV=false; [ "$(jq -r '[.[]|select(.type=="result")|.subtype]|.[0] // ""' "$W/out.json" 2>/dev/null)" = success ] && [ "$SLEEPS" -gt 0 ] && SURV=true
+P95=$(jq -s 'sort|if length==0 then null else .[((length*0.95|ceil)-1)] end' "$W/t.log" 2>/dev/null || echo null)
+# hooks other than ours: keys of the user and sandbox settings, and PostToolUse additionalContext seen from anything but our probe
+UH=$(jq -c '.hooks|keys' "$HOME/.claude/settings.json" 2>/dev/null || echo null)
+SH=$(jq -c '.hooks|keys' "$CWD/.claude/settings.json" 2>/dev/null || echo null)
+OTHER_CTX=0; [ -n "$LASTSNAP" ] && OTHER_CTX=$(jq -s '[.[]|select(.type=="attachment" and .attachment.type=="hook_additional_context" and .attachment.hookEvent=="PostToolUse" and (tostring|test("PROBE-CONTEXT")|not))]|length' "$LASTSNAP" 2>/dev/null || echo 0)
+MODEL_OK=false; lo=$(tr 'A-Z' 'a-z' <<<"$OBS"); le=$(tr 'A-Z' 'a-z' <<<"$MODEL"); { [ "$lo" = "$le" ] || [ "$lo" = "$le-build" ]; } && MODEL_OK=true
+PASS=false; $FIELDS && $SNAP && $SURV && $CTX && $MODEL_OK && { [ "$SUBST" = reaches_with_agent_id ] || [ "$SUBST" = does_not_reach ]; } && PASS=true
+jq -n -c --arg m "$MODEL" --argjson pass $PASS --argjson fields $FIELDS --argjson snap $SNAP --argjson surv $SURV --argjson ctx $CTX --argjson saw $SAW \
+  --argjson modelok $MODEL_OK --arg subst "$SUBST" --argjson nsub "$NSUB" --argjson nstdin "$NSTDIN" --argjson sleeps "$SLEEPS" --argjson p95 "${P95:-null}" \
+  --arg obs "$OBS" --arg sid "$SID" --argjson rc $RC --argjson wall "$WALL" --arg res "$RES" --argjson uh "${UH:-null}" --argjson sh "${SH:-null}" \
+  --argjson other "$OTHER_CTX" \
+  '{model:$m, pass:$pass, observed_model:$obs, model_ok:$modelok, session_id:$sid, exit:$rc, wall_ms:$wall,
+    checks:{stdin_fields_ok:$fields, hook_calls:$nstdin, subagent_status:$subst, subagent_hook_calls_with_agent_id:$nsub, snapshot_hashed:$snap,
+            survived_over_timeout_hook:$surv, sleeper_started:$sleeps, context_in_transcript:$ctx, model_repeated_context:$saw,
+            other_hook_additional_context_entries:$other},
+    hook_ms_p95:$p95, hooks_lists:{user_settings:$uh, sandbox_settings:$sh}, final_text:$res}' > "$OUT/$MODEL.json"
+# R-46: delete only this probe's own session file
+ENC=$(printf '%s' "$CWD" | sed 's/[^A-Za-z0-9]/-/g')
+case $SID in ''|*/*|*..*) ;; *) F=$PROJ/$ENC/$SID.jsonl; [ -f "$F" ] && [ ! -L "$F" ] && rm -f -- "$F";; esac
+jq -c '{model,pass,checks,hook_ms_p95}' "$OUT/$MODEL.json"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s2-resume.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s2-resume.sh
new file mode 100755
index 000000000..9122f774c
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s2-resume.sh
@@ -0,0 +1,47 @@
+#!/usr/bin/env bash
+# s2-resume.sh <model> [--root R1] [--sb SB] [--projects DIR]   (Gate 0, S2; DESIGN.md 6.3, Adaptation A-7)
+# A short `claude -p` (session persistence on) that is told a code word, then `claude -p --resume <session_id>` with
+# --output-format stream-json --verbose (exactly the H2 re-ask form of run-reviewer.sh) that is asked for it. Writes spikes/s2/<model>.json.
+# pass = the resume reply contains the code word (the same session answered), the `result` event of the stream is parsed by the
+# `jq -s` filter of the H2 re-ask, and the first attempt used the right model. Records the resume start time (planning value 6 s).
+# Deletes only the session files whose ids it recorded (R-46).
+set -u -o pipefail
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
+SB=/tmp/evalsb-collab-r1; PROJ=$HOME/.claude/projects
+MODEL=${1:?usage: s2-resume.sh <model> [--root R1] [--sb SB] [--projects DIR]}; shift
+while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; --projects) PROJ=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
+export NOFALLBACK=1
+DS=TASK-WF-designSpec-20261107-075614
+CWD=$SB/$DS/repo; [ -d "$CWD" ] || { echo "FAIL build the sandbox first: sandbox.sh $DS" >&2; exit 1; }
+OUT=$R1/spikes/s2; W=$SB/s2/$MODEL; rm -rf "$W"; mkdir -p "$OUT" "$W"
+WORD=ORCHID-$RANDOM
+S1=$(date +%s%3N)
+( cd "$CWD" && timeout --kill-after=5 240 claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions \
+    --disallowedTools Edit Write NotebookEdit <<<"Remember the code word $WORD. Reply with the single word OK." ) > "$W/first.json" 2> "$W/first.err"
+RC1=$?; WALL1=$(( $(date +%s%3N) - S1 ))
+SID=$(jq -r '[.[]|select(.type=="result")|.session_id]|.[0] // ""' "$W/first.json" 2>/dev/null)
+OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$W/first.json" 2>/dev/null)
+RES=""; RC2=null; FIRST_EVENT_MS=null; WALL2=null; PARSED=false; RSID=""
+if [ -n "$SID" ]; then
+  S2=$(date +%s%3N)
+  ( cd "$CWD" && timeout --kill-after=5 240 claude -p --resume "$SID" --model "$MODEL" --output-format stream-json --verbose \
+      --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"What was the code word? Reply with only the code word." ) \
+      2> "$W/resume.err" | while IFS= read -r line; do printf '%s\n' "$line"; [ -f "$W/.first" ] || { echo $(( $(date +%s%3N) - S2 )) > "$W/.first"; }; done > "$W/resume.json"
+  RC2=${PIPESTATUS[0]}; WALL2=$(( $(date +%s%3N) - S2 )); FIRST_EVENT_MS=$(cat "$W/.first" 2>/dev/null || echo null)
+  RES=$(jq -s -r '[.[]|select(.type=="result")|.result][0] // ""' "$W/resume.json" 2>/dev/null) && PARSED=true
+  RSID=$(jq -s -r '[.[]|select(.type=="result")|.session_id][0] // ""' "$W/resume.json" 2>/dev/null)
+fi
+SAME=false; grep -q "$WORD" <<<"$RES" && SAME=true
+MODEL_OK=false; lo=$(tr 'A-Z' 'a-z' <<<"$OBS"); le=$(tr 'A-Z' 'a-z' <<<"$MODEL"); { [ "$lo" = "$le" ] || [ "$lo" = "$le-build" ]; } && MODEL_OK=true
+PASS=false; $SAME && $PARSED && $MODEL_OK && PASS=true
+jq -n -c --arg m "$MODEL" --argjson pass $PASS --argjson same $SAME --argjson parsed $PARSED --argjson modelok $MODEL_OK --arg obs "$OBS" \
+  --arg sid "$SID" --arg rsid "$RSID" --arg word "$WORD" --arg res "$RES" --argjson w1 $WALL1 --argjson w2 "$WALL2" --argjson fe "$FIRST_EVENT_MS" \
+  --argjson rc1 $RC1 --argjson rc2 "$RC2" \
+  '{model:$m, pass:$pass, observed_model:$obs, model_ok:$modelok, first_session_id:$sid, resume_session_id:$rsid, code_word:$word,
+    resume_reply:$res, answered_in_same_session:$same, result_event_parsed_by_jq_s:$parsed, first_wall_ms:$w1, resume_wall_ms:$w2,
+    resume_first_event_ms:$fe, exit_first:$rc1, exit_resume:$rc2}' > "$OUT/$MODEL.json"
+# R-46: delete only the session files this spike recorded
+ENC=$(printf '%s' "$CWD" | sed 's/[^A-Za-z0-9]/-/g')
+for ID in $SID $RSID; do case $ID in ''|*/*|*..*) ;; *) F=$PROJ/$ENC/$ID.jsonl; [ -f "$F" ] && [ ! -L "$F" ] && rm -f -- "$F";; esac; done
+jq -c . "$OUT/$MODEL.json"

Codegraph context: index_state: fresh; checked_at: 2026-11-13T22:17:42Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel. call codegraph only when index_state: fresh, never to widen scope. Q2b dependents: none outside the diff (shell, markdown and untracked test files are not indexed; Grep floor used).
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): Evidence the reviewer may read (records, not part of the diff): .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s0/*.json, .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s2/*.json, .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/reqs3/*.json, .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/reqs3.json, .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/gate0.json; per-session working files under /tmp/evalsb-collab-r1/s0, /tmp/evalsb-collab-r1/s2, /tmp/evalsb-collab-r1/reqs3 (raw hook stdin, snapshots, tele). Executor's summary (an implementer claim, verify it): S0 pass 4/4 (subagent calls reach the hook with agent_id; sleeper hook cancelled by its 1 s timeout, session survived), S2 pass 4/4, REQ-S3 recorded 4/4, gate0.json: G-BASE pass, G-PINS pass, S0 pass, S2 pass, REQ-S3 recorded, S3 missing, Spike 4 missing.


Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.