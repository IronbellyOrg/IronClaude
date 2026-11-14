#!/usr/bin/env bash
# Check one TIME_CAP_EXCEPTION=1 collaboration row (DESIGN 6.4 items 1-4, 6, 7; item 5 is A1-only and is not part of this row)
# plus the exception's own stamps (OVERRIDE.md), and append the result to spikes/NOTES.md.
# usage: smoke-check-tcx.sh <f6 row> <launch exit> [pkg]
set -u -o pipefail
ROW=$1; RF=$2; PKG=${3:-TASK-WF-design-20261108-041415}
R5=$(cd "$(dirname "$0")/.." && pwd); OUTR=${R5_OUT:-$R5}; NOTES=$R5/spikes/NOTES.md; CFG=${R5_CONFIG:-$R5/config}
D=$OUTR/runs/$ROW/$PKG; RES=$OUTR/results/$ROW.json
L=""; ALL=PASS
item() { local ok=$1; shift; [ "$ok" = PASS ] || ALL=FAIL; L+="$ok $*"$'\n'; }
b() { if eval "$1"; then echo PASS; else echo FAIL; fi; }
ST=$(jq -r .status "$RES" 2>/dev/null)
item "$(b "[ $RF = 0 ] && [ \"$ST\" = complete ]")" "1 launch exit=$RF; results status=$ST"
M2=PASS; DET=""
for m in "$D"/reviews/*.meta.json; do
  case "$m" in *attempt*) continue;; esac
  rid=$(basename "$m" .meta.json); want=$(jq -r --arg r "$rid" '.models[$r]' "$D/run.json")
  ok=$(jq -r .model_ok "$m"); obs=$(jq -r .observed_model "$m")
  { [ "$ok" = true ] && [ "$obs" = "$want" ]; } || M2=FAIL; DET+="$rid=$obs "
done
item $M2 "2 final model_ok and observed model equals requested: $DET"
DL=$(cat "$D"/reviews/*.timing.json | jq -s 'map(.dropped_lines)|add')
NB=$(jq -s 'map(.block_ok|length)|min' "$D/merge-stdout.txt" 2>/dev/null)
item "$(b "[ \"$DL\" = 0 ] && [ \"$NB\" = 3 ]")" "3 dropped_lines total=$DL; reviewer ids in the merge=$NB"
CD=$(jq '[.cards[]?|select(.status=="delivered")]|length' "$D/collab.json")
SMALL=$(jq '[.reviewers[]|select(.role=="receiver")|.snapshot_missing]|add' "$D/collab.json"); HE=$(jq '[.reviewers[]|select(.role=="receiver")|.hook_error]|add' "$D/collab.json")
C4=PASS; D4=""
for rid in $(jq -r '[.cards[]?|select(.status=="delivered")|.to]|unique[]' "$D/collab.json"); do
  SEAL=$(cat "$D/board/snap/$rid.t" 2>/dev/null || echo 0)
  SESS=$(ls "$D/reviews/$rid".attempt1.session.jsonl 2>/dev/null)
  TXT_T=$(jq -r 'select(tostring|test("Panel request \\(from the harness"))|.timestamp' "$SESS" 2>/dev/null | head -1)
  TXT_MS=$( [ -n "$TXT_T" ] && date -d "$TXT_T" +%s%3N || echo 0)
  SNAPOK=false; [ -s "$D/board/snap/$rid.sha256" ] && [ "$(cut -d' ' -f1 "$D/board/snap/$rid.sha256")" = "$(sha256sum "$D/board/snap/$rid.jsonl" | cut -d' ' -f1)" ] && SNAPOK=true
  VAL=$(cd "$(git -C "$R5" rev-parse --show-toplevel)" && PYTHONPATH="$R5/lib" uv run --no-sync python -m r5.panelmsg "${R5_SB:-/tmp/evalsb-collab-r5}/cand/$PKG/candidate.md" \
        "$(jq .k "$D/run.json")" "$(jq -r '.receivers|join(",")' "$D/run.json")" "$ROW/$PKG" < "$D/board/msgs/watcher.jsonl" >/dev/null 2>&1 && echo ok || echo bad)
  { [ "$TXT_MS" -ge "$SEAL" ] && [ "$SEAL" -gt 0 ] && [ $VAL = ok ] && $SNAPOK; } || C4=FAIL
  D4+="[$rid seal_t=$SEAL card_text_in_transcript_at=$TXT_MS validator=$VAL snapshot_sha_ok=$SNAPOK] "
done
[ "$CD" -ge 1 ] && [ "$SMALL" = 0 ] && [ "$HE" = 0 ] || C4=FAIL
item $C4 "4 cards_delivered=$CD snapshot_missing=$SMALL hook_error=$HE $D4"
K=$(jq .k "$D/run.json"); FIN=$(jq .finish_ms "$D/run.json")
KEYS=$(jq -r '[.[]|select(.v=="panel-msg/1")]|length' <(jq -s . "$D/board/msgs/watcher.jsonl") 2>/dev/null)
AFTER=$(jq -s --argjson f "$FIN" '[.[]|select(.t>=$f)]|length' "$D/board/msgs/watcher.jsonl")
ITEMS_OK=$(jq -s --argjson k "$K" 'all(.[]; (.items|length)<=$k and (keys|sort)==["from","id","items","kind","run","t","to","v"])' "$D/board/msgs/watcher.jsonl")
DAFTER=$(jq -s --argjson f "$FIN" '[.[]|select(.status=="delivered" and .t>=$f)]|length' "$D"/board/delivered/*.jsonl)
item "$(b "[ \"$AFTER\" = 0 ] && [ \"$ITEMS_OK\" = true ] && [ \"$DAFTER\" = 0 ]")" "AC-9 cards=$KEYS keys_and_items_ok=$ITEMS_OK posted_at_or_after_finish=$AFTER delivered_at_or_after_finish=$DAFTER (k=$K)"
TOK=$(jq -c --arg r "$ROW" 'select(.row==$r and .pkg=="'"$PKG"'")' "$OUTR/results/scoring-keys.jsonl" | tail -1)
tok=$(jq -r .token <<<"$TOK"); lab=$(jq -r .label <<<"$TOK"); an=$(jq -r .status <<<"$TOK")
sc=$OUTR/scoring/$tok/$PKG/$lab/score.json; au=$(jq -r .status "$D/audit.json")
item "$(b "jq -e . \"$sc\" >/dev/null 2>&1 && [ \"$an\" = ok ] && [ \"$au\" = pass ]")" "6 anon=$an score=$( [ -f "$sc" ] && echo parsed || echo missing) audit=$au"
EL=$(jq .elapsed_s "$D/collab.json"); B=$(jq .B_f_s "$D/run.json"); HK=$(jq '[.reviewers[].hang_kill]|any' "$D/collab.json")
HANGS=$(( $(jq .hang_ms "$D/run.json") - $(jq .T0 "$D/run.json") ))
item "$(b "awk -v e=$EL -v h=$HANGS 'BEGIN{exit !(e*1000 <= h)}' && [ $HK = false ]")" "7 (exception form) elapsed_s=$EL B_A1=$B hang_guard_s=$(awk -v h=$HANGS 'BEGIN{print h/1000}') ratio=$(jq .elapsed_over_baseline "$D/collab.json") hang_kill=$HK slo=$(jq -r .slo "$D/collab.json")"
VS=$(jq -r .values_sha256 "$D/run.json"); VB=$(jq .B_f_s "$CFG/values/$(jq -r .panel "$D/run.json")/$PKG.json")
S1=$(jq .time_cap_exception "$D/run.json"); S2=$(jq .time_cap_exception "$D/collab.json"); S3=$(jq .time_cap_exception "$RES"); KF=$(jq .k_forced "$D/run.json")
S4=$(jq -r --arg p "$PKG" '.time_cap[$p]|has("messages_delivered")' "$RES")
item "$(b "[ $S1 = true ] && [ $S2 = true ] && [ $S3 = true ] && [ $KF = true ] && [ $K = 1 ] && [ \"$B\" = \"$VB\" ] && [ $S4 = true ]")" "8 stamps time_cap_exception=true in run/collab/results; k_measured=$(jq .k_measured "$D/run.json") k_forced=true k=$K; B_A1=$B equals values file $VB; values_sha256=$VS; messages_delivered=$(jq -c .messages_delivered "$D/collab.json")"
printf '%s' "$L"
{ echo; echo "## Smoke test, TIME_CAP_EXCEPTION=1 (DESIGN 6.4 items 1-4, 6, 7 + stamps): $ALL ($(date -u +%Y-%m-%dT%H:%M:%SZ))"; echo
  echo "Row \`$ROW\` on \`$PKG\`; checked by \`spikes/smoke-check-tcx.sh\`."; echo; printf '%s' "$L" | sed 's/^/- /'; } >> "$NOTES"
[ $ALL = PASS ]
