#!/usr/bin/env bash
# radar-hook.sh <BOARD> <RUN> <RID> <ROLE> <T0_MS> <FINISH_MS> <GUARD_MS> <K> <CP1> <CP2> <ORDER> <PKG> <CLOCK_FILE>
# The PostToolUse hook of F3 (DESIGN.md section 2.4): telemetry, checkpoint logic, seal, injection, finish signal.
# Frozen per-package inputs are read from BOARD/ctx/ (written by launch.sh): catalogue.json, index.json and
# panel.json = {"searcher":rid,"readers":[rid,rid],"srcpath":".../cand/<pkg>/source.md"}.
# Prints nothing or one {"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":..}}; always exits 0.
BOARD=${1:-}; RUN=${2:-}; RID=${3:-}; ROLE=${4:-}; T0_MS=${5:-0}; FINISH_MS=${6:-0}; GUARD_MS=${7:-0}
K=${8:-0}; CP1=${9:-0}; CP2=${10:-0}; ORDER=${11:-}; PKG=${12:-}; CLOCK_FILE=${13:-}
TOOLS=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
MET=$BOARD/metrics/$RID.jsonl
start_ms=$(date +%s%3N)
now_ms() { if [ -n "$CLOCK_FILE" ]; then tr -dc '0-9' < "$CLOCK_FILE"; else date +%s%3N; fi; }
logm() { printf '%s\n' "$1" >> "$MET"; }

main() {
  set -eu -o pipefail
  local in now n tele ix cat panel sealed inj eligible item move text slot hint line env valid
  in=$(head -c 1048576)
  printf '%s' "$in" | jq -e 'type == "object"' >/dev/null      # not JSON -> error -> hook_error
  now=$(now_ms); [ -n "$now" ]
  mkdir -p "$BOARD/tele" "$BOARD/state" "$BOARD/metrics"
  exec 9>>"$BOARD/state/$RID.lock"; flock -w 4 9
  # 3. subagent call: log only, never counted or classified
  if [ "$(printf '%s' "$in" | jq -r '.agent_id // empty')" != "" ]; then
    tele=$(printf '%s' "$in" | jq -c --argjson t "$now" --arg rid "$RID" \
      '{n: null, t: $t, rid: $rid, sub: true, tool: .tool_name, input: (.tool_input // {} | walk(if type == "string" then .[:2000] else . end))}')
    printf '%s\n' "$tele" >> "$BOARD/tele/$RID.jsonl"; return 0
  fi
  # 4. count and telemetry (one O_APPEND write)
  n=$(( $(cat "$BOARD/state/$RID.count" 2>/dev/null || echo 0) + 1 )); echo "$n" > "$BOARD/state/$RID.count"
  N=$n
  tele=$(printf '%s' "$in" | jq -c --argjson n "$n" --argjson t "$now" --arg rid "$RID" \
    '{n: $n, t: $t, rid: $rid, sub: false, tool: .tool_name, input: (.tool_input // {} | walk(if type == "string" then .[:2000] else . end))}')
  printf '%s\n' "$tele" >> "$BOARD/tele/$RID.jsonl"
  sealed=$(cat "$BOARD/state/$RID.sealed" 2>/dev/null || true)
  [ "$sealed" = failed ] && return 0                              # a failed seal: nothing more is delivered
  cat=$BOARD/ctx/catalogue.json
  # 5. finish signal; after FINISH_MS nothing else is ever injected
  if [ "$now" -ge "$FINISH_MS" ]; then
    [ -e "$BOARD/state/$RID.finish" ] && return 0
    : > "$BOARD/state/$RID.finish"
    logm "{\"ev\":\"finish\",\"t\":$now,\"n\":$n}"
    jq -c '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: .finish_text}}' "$cat"
    return 0
  fi
  # 6. checkpoint test
  eligible=$( [ "$K" -ge 1 ] && echo "$CP1"; [ "$K" -ge 2 ] && echo "$CP2"; true )
  grep -qx -- "$n" <<< "$eligible" || return 0      # here-strings, not pipes: grep -q must not SIGPIPE a writer
  inj=$(grep -c '"ev":"inject"' "$MET" 2>/dev/null || true)
  [ "${inj:-0}" -ge "$K" ] && return 0
  if [ "$now" -ge "$GUARD_MS" ]; then logm "{\"ev\":\"skip\",\"reason\":\"guard\",\"n\":$n}"; return 0; fi
  # 7. seal (fail closed)
  if [ -z "$sealed" ]; then
    local tp; tp=$(printf '%s' "$in" | jq -r '.transcript_path // empty')
    mkdir -p "$BOARD/snap"
    if [ -n "$tp" ] && cp "$tp" "$BOARD/snap/$RID.jsonl" 2>/dev/null \
       && (cd "$BOARD/snap" && sha256sum "$RID.jsonl" > "$RID.sha256"); then
      logm "{\"ev\":\"seal\",\"t\":$now,\"sha256\":\"$(cut -d' ' -f1 "$BOARD/snap/$RID.sha256")\"}"
      echo ok > "$BOARD/state/$RID.sealed"
    else
      echo failed > "$BOARD/state/$RID.sealed"
      logm "{\"ev\":\"snapshot_missing\",\"t\":$now}"
      return 0
    fi
  fi
  # 8. choose the item (section 2.5)
  ix=$BOARD/ctx/index.json; panel=$BOARD/ctx/panel.json
  local srcpath; srcpath=$(jq -r .srcpath "$panel")
  classify() { jq -R -c --slurpfile ix "$ix" --arg srcpath "$srcpath" -f "$TOOLS/radar-classify.jq" "$@" | jq -r '.sig[]'; }
  local injected; injected=$(jq -R -r 'fromjson? // empty | select(type == "object" and .ev == "inject") | .move // "SRC"' "$MET" 2>/dev/null || true)
  item=""
  local own=""; [ "$n" = "$CP1" ] && own=$(classify "$BOARD/tele/$RID.jsonl")
  if [ "$n" = "$CP1" ] && ! grep -qx SRC_OPENED <<< "$own"; then
    item=SRC
  else
    local covered=""
    [ "$ROLE" = searcher ] && covered=$(cat "$BOARD"/tele/*.jsonl | classify | sort -u)
    for move in ${ORDER//,/ }; do
      grep -qx -- "$move" <<< "$injected" && continue
      [ "$ROLE" = searcher ] && grep -qx -- "$move" <<< "$covered" && continue
      item=$move; break
    done
  fi
  if [ -z "$item" ]; then logm "{\"ev\":\"skip\",\"reason\":\"no_gap\",\"n\":$n}"; return 0; fi
  # 9. task hint (metrics only, never in the message)
  hint=$(printf '%s' "$in" | jq -c --slurpfile ix "$ix" '(.tool_input // {} | tostring) as $s
      | [$ix[0].task_of_path | to_entries[] | select(.key as $k | $s | contains($k)) | .value[]] | unique')
  # 10. line, validation, delivery
  local id; id=$(printf 'm-%s-%02d' "$RID" "$n")
  if [ "$item" = SRC ]; then
    move=null; slot=src; text=$(jq -r .src_text "$cat")
    line=$(jq -n -c --arg id "$id" --arg run "$RUN" --arg to "$RID" --argjson t "$now" '{v:"panel-msg/1",id:$id,run:$run,from:"radar",to:$to,t:$t,kind:"move"}')
  else
    move="\"$item\""
    if [ "$ROLE" = searcher ]; then slot=search; else slot=static; fi
    text=$(jq -r --arg m "$item" --arg role "$ROLE" '.moves[$m] + (if $role == "searcher" and (.observable | index($m)) != null then .observable_suffix else "" end)' "$cat")
    line=$(jq -n -c --arg id "$id" --arg run "$RUN" --arg to "$RID" --argjson t "$now" --arg m "$item" '{v:"panel-msg/1",id:$id,run:$run,from:"radar",to:$to,t:$t,kind:"move",move:$m}')
  fi
  env=$(jq -n -c --arg line "$line" --arg text "$text" '{line:$line,text:$text}')
  valid=$(printf '%s\n' "$env" | bash "$TOOLS/msg-validate.sh" "$cat" "$(jq -r .searcher "$panel")" "$(jq -r '.readers|join(",")' "$panel")" 2>/dev/null) \
    || { logm "{\"ev\":\"hook_error\",\"t\":$now,\"msg\":\"validator rejected $id\"}"; return 0; }
  mkdir -p "$BOARD/msgs"
  printf '%s\n' "$valid" >> "$BOARD/msgs/radar.jsonl"
  logm "$(jq -n -c --arg id "$id" --argjson t "$now" --argjson n "$n" --argjson move "$move" --arg slot "$slot" \
      --argjson hint "$hint" --arg text "$text" --arg sha "$(printf '%s' "$text" | sha256sum | cut -d' ' -f1)" \
      '{ev:"inject",id:$id,t:$t,n:$n,move:$move,slot_type:$slot,task_hint:$hint,text:$text,text_sha256:$sha}')"
  jq -n -c --arg text "$text" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $text}}'
}

N=null
mkdir -p "$BOARD/metrics" 2>/dev/null
out=$(main); rc=$?
if [ $rc -eq 0 ]; then
  [ -n "$out" ] && printf '%s\n' "$out"
else
  printf '{"ev":"hook_error","t":%s,"msg":"rc=%s"}\n' "$(date +%s%3N)" "$rc" >> "$MET" 2>/dev/null
fi
[ -f "$BOARD/state/$RID.count" ] && N=$(cat "$BOARD/state/$RID.count" 2>/dev/null)
printf '{"ev":"t","n":%s,"ms":%s}\n' "${N:-null}" "$(( $(date +%s%3N) - start_ms ))" >> "$MET" 2>/dev/null
exit 0
