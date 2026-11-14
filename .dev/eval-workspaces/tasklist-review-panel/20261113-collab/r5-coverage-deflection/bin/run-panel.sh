#!/usr/bin/env bash
# One panel on one package (DESIGN 2.1, 2.7): T0, watcher, reviewers, tags, collab.json, alarms, audit.
# usage: run-panel.sh <row> <panel> <pkg>; env PANEL_COLLAB, PANEL_KIT, SPIKE4=1, NOFALLBACK=1; tests: R5_OUT, R5_SB, R5_CONFIG
set -u -o pipefail
ROW=$1; PANEL=$2; PKG=$3
R5=$(cd "$(dirname "$0")/.." && pwd); CFG=${R5_CONFIG:-$R5/config}; OUTR=${R5_OUT:-$R5}; SB=${R5_SB:-/tmp/evalsb-collab-r5}
REPO=$(git -C "$R5" rev-parse --show-toplevel)
py() { (cd "$REPO" && PYTHONPATH="$R5/lib" uv run --no-sync python -m "$@"); }
nowms() { date +%s%3N; }
COLLAB=${PANEL_COLLAB:-0}; KIT=${PANEL_KIT:-0}; [ "$COLLAB" = 1 ] && KIT=1
export PANEL_COLLAB=$COLLAB PANEL_KIT=$KIT
ARM=A1; [ "$KIT" = 1 ] && ARM=A2; [ "$COLLAB" = 1 ] && ARM=F6; ARM="$ARM-$PANEL"
D=$OUTR/runs/$ROW/$PKG; mkdir -p "$D/reviews"
PJ=$(jq -c --arg p "$PANEL" '.[$p]' "$CFG/panels.json"); [ "$PJ" != null ] || { echo "unknown panel $PANEL" >&2; exit 2; }
MINC=$(jq .min_calls <<<"$PJ")
SLACK=${PANEL_SLACK_S:-0}  # owner decision 2026-11-14: cap is 1.35 B + PANEL_SLACK_S (whole seconds); values live in values-slack<S>/
[[ $SLACK =~ ^(0|[1-9][0-9]*)$ ]] || { echo "PANEL_SLACK_S must be a whole number of seconds, got '$SLACK'" >&2; exit 2; }
VDIR=values; [ "$SLACK" != 0 ] && VDIR=values-slack$SLACK
# Owner-authorised time-cap exception (2026-11-14, OVERRIDE.md): TIME_CAP_EXCEPTION=1 forces k = 1 where the measured k is 0 and widens the guards.
TCX=${TIME_CAP_EXCEPTION:-0}
[[ $TCX =~ ^[01]$ ]] || { echo "TIME_CAP_EXCEPTION must be 0 or 1, got '$TCX'" >&2; exit 2; }
if [ "$TCX" = 1 ]; then
  [ "$COLLAB" = 1 ] || { echo "TIME_CAP_EXCEPTION=1 applies to the collaboration arm only (PANEL_COLLAB=1)" >&2; exit 2; }
  [ "$SLACK" = 0 ] || { echo "TIME_CAP_EXCEPTION=1 and PANEL_SLACK_S are exclusive" >&2; exit 2; }
  [ "${SPIKE4:-}" != 1 ] || { echo "TIME_CAP_EXCEPTION=1 cannot be combined with SPIKE4=1" >&2; exit 2; }
fi
KMEAS=0; KFORCED=false; TCAP=null

if [ "${SPIKE4:-}" = 1 ]; then
  VAL=planning; VSHA=null
  B=$(jq --arg p "$PKG" '.planning_B_s[$p]' <<<"$PJ")
  OFF=$(py r5.timing offsets "$B" "$(jq .receiver_turn_planning_s <<<"$PJ")" "$(jq .receiver_report_planning_s <<<"$PJ")")
  K=0; FOFF=$(jq .finish_offset_s <<<"$OFF"); HOFF=3000
else
  VAL=$CFG/$VDIR/$PANEL/$PKG.json
  [ -f "$VAL" ] || { echo "no values file $VAL" >&2; exit 3; }
  WANT=$(awk -v f="$PKG.json" '$2==f{print $1}' "$CFG/$VDIR/$PANEL/SHA256SUMS" 2>/dev/null)
  VSHA=$(sha256sum "$VAL" | cut -d' ' -f1)
  [ -n "$WANT" ] && [ "$WANT" = "$VSHA" ] || { echo "values sum mismatch for $VAL (R-30)" >&2; exit 3; }
  [ "$(jq '.slack_s // 0' "$VAL")" = "$SLACK" ] || { echo "values file $VAL was computed with slack_s=$(jq '.slack_s // 0' "$VAL"), PANEL_SLACK_S=$SLACK" >&2; exit 3; }
  VSHA="\"$VSHA\""
  B=$(jq .B_f_s "$VAL"); K=$(jq .k "$VAL"); FOFF=$(jq .finish_offset_s "$VAL"); HOFF=$(jq .hang_offset_s "$VAL")
  KMEAS=$K
  if [ "$TCX" = 1 ]; then  # the frozen values file stays as it is (sum checked above); the runner reads an effective copy with the widened numbers
    PLAN=$(py r5.timing exception "$VAL") || { echo "time-cap exception plan failed for $VAL" >&2; exit 3; }
    K=$(jq .k_run <<<"$PLAN"); FOFF=$(jq .finish_offset_s <<<"$PLAN"); HOFF=$(jq .hang_offset_s <<<"$PLAN")
    TCAP=$(jq .time_cap_s <<<"$PLAN"); KFORCED=$(jq .k_forced <<<"$PLAN")
    jq --argjson p "$PLAN" '. + {k:$p.k_run, finish_offset_s:$p.finish_offset_s, hang_offset_s:$p.hang_offset_s, time_cap_exception:true, k_measured:.k}' "$VAL" > "$D/values-effective.json"
    VAL=$D/values-effective.json
  fi
fi
T0=$(nowms)
FIN=$(awk -v t="$T0" -v o="$FOFF" 'BEGIN{printf "%d", t + 1000*o}')
HANG=$(awk -v t="$T0" -v o="$HOFF" 'BEGIN{printf "%d", t + 1000*o}')
H=$(printf '%s' "$ROW/$PKG/deal" | sha256sum); DEAL=$(( 0x${H:0:1} >> 3 ))
RECV=$(jq -c '[.reviewers[]|select(.role=="receiver")|.rid]' <<<"$PJ"); SCOUTS=$(jq -c '[.reviewers[]|select(.role=="scout")|.rid]' <<<"$PJ")
K0ISO=false; [ "$COLLAB" = 1 ] && [ "$K" -le 0 ] && K0ISO=true
jq -n --arg row "$ROW" --arg arm "$ARM" --arg panel "$PANEL" --arg pkg "$PKG" --argjson t0 "$T0" --argjson fin "$FIN" --argjson hang "$HANG" \
  --argjson k "$K" --argjson deal "$DEAL" --argjson vsha "$VSHA" --argjson B "$B" --argjson recv "$RECV" --argjson scouts "$SCOUTS" \
  --argjson collab "$COLLAB" --argjson kit "$KIT" --argjson k0 $K0ISO --arg spike4 "${SPIKE4:-0}" --argjson pj "$PJ" --argjson slack "$SLACK" \
  --argjson tcx "$([ "$TCX" = 1 ] && echo true || echo false)" --argjson kmeas "$KMEAS" --argjson kforced "$KFORCED" --argjson tcap "$TCAP" \
  '{row:$row,arm:$arm,panel:$panel,pkg:$pkg,T0:$t0,finish_ms:$fin,hang_ms:$hang,k:$k,deal_r:$deal,values_sha256:$vsha,B_f_s:$B,slack_s:$slack,
    time_cap_exception:$tcx,k_measured:$kmeas,k_forced:$kforced,time_cap_s:$tcap,
    receivers:$recv,scouts:$scouts,models:($pj.reviewers|map({(.rid):.model})|add),min_calls:$pj.min_calls,
    switches:{PANEL_COLLAB:$collab,PANEL_KIT:$kit,NOFALLBACK:1,SPIKE4:($spike4=="1")},k0_isolated:$k0}' > "$D/run.json"

WPID=""
if [ "$COLLAB" = 1 ] && [ "$K" -gt 0 ]; then
  BD=$D/board; mkdir -p "$BD"/{msgs,delivered,state,snap,metrics,settings}; : > "$BD/msgs/watcher.jsonl"
  for rid in $(jq -r '.[]' <<<"$RECV"); do
    jq -n --arg c "bash $R5/bin/hook-posttool.sh $BD $rid $T0 $FIN $MINC $K $R5" \
      '{hooks:{PostToolUse:[{matcher:"*",hooks:[{type:"command",timeout:10,command:$c}]}]}}' > "$BD/settings/$rid.json"
  done
  py r5.watcher --run-dir "$D" --candidate "$SB/cand/$PKG/candidate.md" --panel "$PANEL" --k "$K" --finish-ms "$FIN" \
    --row "$ROW" --pkg "$PKG" --deal-r "$DEAL" ${R5_POLL_S:+--poll "$R5_POLL_S"} >> "$BD/watcher.out" 2>&1 &
  WPID=$!
fi
PIDS=()
while read -r rid model role; do
  S=""; [ -n "$WPID" ] && [ "$role" = receiver ] && S=$D/board/settings/$rid.json
  bash "$R5/bin/run-reviewer-r5.sh" "$D/reviews" "$PKG" "$rid" "$model" "$role" "$T0" "$VAL" $S > "$D/reviews/$rid.runner.log" 2>&1 &
  PIDS+=($!)
done < <(jq -r '.reviewers[]|"\(.rid) \(.model) \(.role)"' <<<"$PJ")
for p in "${PIDS[@]}"; do wait "$p"; done
if [ -n "$WPID" ]; then kill "$WPID" 2>/dev/null; wait "$WPID" 2>/dev/null; fi
py r5.tagger "$D" "$SB/cand/$PKG/candidate.md" > /dev/null
py r5.collab "$D"
py r5.alarms package "$D" --ref "$OUTR/results/arm-summary-A1-$PANEL.json" > /dev/null
py r5.audit package "$D" > /dev/null
exit 0
