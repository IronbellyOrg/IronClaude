#!/usr/bin/env bash
# Spike S0: do --settings PostToolUse hooks fire in `claude -p` for muse-ember-1.0 and gpt-6-luna; is the hook-side
# snapshot written and hashed before the first delivery; does the delivered text reach the transcript; hook timing;
# which project hooks of the base sandbox are active (recorded, not judged).
#   flock /tmp/collab-gateway.lock bash spikes/s0-hooks.sh
set -u -o pipefail
. "$(dirname "$0")/_spike.sh"
PKG=TASK-WF-design-20261108-041415
OUTD=$SPIKES/out/s0; mkdir -p "$OUTD"
bash "$R2_HOME/bin/build-sandbox.sh" "$PKG" >/dev/null || { record S0 FAIL "$OUTD" "build-sandbox failed"; exit 1; }
ALL=PASS
for MODEL in muse-ember-1.0 gpt-6-luna; do
  ID=s0-$(rand_hex); SB=$SBR/sb/$ID/$PKG; B=$SBR/board/$ID/$PKG; D=$OUTD/$MODEL; mkdir -p "$D"
  make_sandbox "$SB" "$PKG"; board_init "$B" "$SB"
  T0=$(now_ms); board_conf "$B" "$SB" "$ID/$PKG" "$T0" $((T0 + 900000)) 8 "$SBR/board/$ID/settings"
  UT=$(ls "$SB/repo/tests" | grep -E '^test_.*\.py$' | while read -r f; do grep -qxF "tests/$f" "$B/named.txt" || echo "tests/$f"; done | head -4)
  i=0; for t in $UT; do "$B/bin/panel-post" --move M1 --cmd "grep -rln review tests/" --item "$t" >> "$D/seed.txt"; i=$((i+1)); done
  bash "$R2_HOME/bin/make-settings.sh" receiver --board "$B" --rid t4-1 --recv-index 0 --t0-ms "$T0" --finish-ms $((T0 + 900000)) \
    --k 2 --deal-r 0 --out "$D/settings.json"
  ( cd "$SB/repo" && timeout 400 claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions \
      --disallowedTools Edit Write NotebookEdit --settings "$D/settings.json" <<<"$COMMANDS_PROMPT" ) > "$D/out.json" 2> "$D/err.txt"
  echo $? > "$D/rc"
  cp -a "$B" "$D/board"
  OBS=$(model_of "$D/out.json"); SID=$(jq -r '[.[]|select(.type=="result")|.session_id][0] // ""' "$D/out.json")
  TOOLS=$(jq '[.[]|select(.type=="assistant")|.message.content[]?|select(.type=="tool_use")]|length' "$D/out.json")
  CALLS=$(grep -c '"ev":"call"' "$B/metrics/t4-1.jsonl" 2>/dev/null || echo 0)
  ORDER=$(jq -r 'select(.ev=="seal" or .ev=="deliver")|.ev' "$B/metrics/t4-1.jsonl" 2>/dev/null | tr '\n' ' ')
  SNAPOK=false; [ -f "$B/snap/t4-1.jsonl" ] && [ "$(sha256sum "$B/snap/t4-1.jsonl" | cut -d' ' -f1)" = "$(cat "$B/snap/t4-1.sha256")" ] && SNAPOK=true
  TR=$HOME/.claude/projects/$(echo "$SB/repo" | sed 's/[^A-Za-z0-9]/-/g')/$SID.jsonl
  [ -f "$TR" ] && cp "$TR" "$D/transcript.jsonl"
  INTR=false; grep -q 'Search result to check yourself' "$D/transcript.jsonl" 2>/dev/null && INTR=true
  MS=$(jq -s '[.[]|select(.ev=="call")|.ms]|sort' "$B/metrics/t4-1.jsonl" 2>/dev/null)
  P95=$(jq -n --argjson a "${MS:-[]}" 'if ($a|length)==0 then null else $a[((($a|length)*0.95|ceil)-1)] end')
  MAXMS=$(jq -n --argjson a "${MS:-[]}" '$a|max')
  PROJ=$(jq -c '.hooks // {} | to_entries | map({event:.key, commands:[.value[].hooks[]?.command]})' "$SB/repo/.claude/settings.json" 2>/dev/null || echo '"no .claude/settings.json"')
  V=PASS; WHY=()
  model_ok "$OBS" "$MODEL" || { V=FAIL; WHY+=("model=$OBS"); }
  [ "$TOOLS" -gt 0 ] && [ "$CALLS" = "$TOOLS" ] || { V=FAIL; WHY+=("calls=$CALLS tool_use=$TOOLS"); }
  [[ $ORDER == seal\ deliver* ]] || { V=FAIL; WHY+=("order='$ORDER'"); }
  $SNAPOK || { V=FAIL; WHY+=("snapshot"); }
  $INTR || { V=FAIL; WHY+=("delivered-text-not-in-transcript"); }
  [ "${MAXMS:-null}" != null ] && [ "$MAXMS" -lt 5000 ] || { V=FAIL; WHY+=("max_ms=$MAXMS"); }
  [ "${P95:-null}" != null ] && [ "$P95" -le 500 ] || { V=FAIL; WHY+=("p95=$P95"); }
  jq -n --arg m "$MODEL" --arg obs "$OBS" --argjson tools "$TOOLS" --argjson calls "$CALLS" --arg order "$ORDER" \
    --argjson snap $SNAPOK --argjson intr $INTR --argjson p95 "${P95:-null}" --argjson max "${MAXMS:-null}" \
    --argjson proj "$PROJ" --arg v "$V" --arg why "${WHY[*]:-}" --arg sb "$SB" \
    '{model:$m,observed:$obs,tool_use:$tools,hook_calls:$calls,seal_deliver_order:$order,snapshot_ok:$snap,
      delivered_text_in_transcript:$intr,hook_ms_p95:$p95,hook_ms_max:$max,project_hooks:$proj,verdict:$v,why:$why,sandbox:$sb}' > "$D/s0.json"
  record "S0[$MODEL]" "$V" "$D/s0.json" "tool_use=$TOOLS hook_calls=$CALLS order='$ORDER' p95_ms=$P95 max_ms=$MAXMS delivered_in_transcript=$INTR ${WHY[*]:-}"
  [ "$V" = PASS ] || ALL=FAIL
done
record S0 "$ALL" "$OUTD" "both models"
[ "$ALL" = PASS ]
