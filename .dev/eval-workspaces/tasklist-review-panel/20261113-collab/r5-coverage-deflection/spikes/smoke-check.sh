#!/usr/bin/env bash
# Check the 7 items of the one-package smoke test (DESIGN 6.4) and append the result to spikes/NOTES.md.
# usage: smoke-check.sh <f6 row> <a1 row> <f6 launch exit> <a1 launch exit> [pkg]
set -u -o pipefail
F6=$1; A1=$2; RF=$3; RA=$4; PKG=${5:-TASK-WF-design-20261108-041415}
R5=$(cd "$(dirname "$0")/.." && pwd); OUTR=${R5_OUT:-$R5}; NOTES=$R5/spikes/NOTES.md
DF=$OUTR/runs/$F6/$PKG; DA=$OUTR/runs/$A1/$PKG
res() { jq -r "$2" "$OUTR/results/$1.json" 2>/dev/null; }
L=""; ALL=PASS
item() { local ok=$1; shift; [ "$ok" = PASS ] || ALL=FAIL; L+="$ok $*"$'\n'; }
b() { if eval "$1"; then echo PASS; else echo FAIL; fi; }
item "$(b "[ $RF = 0 ] && [ $RA = 0 ] && [ \"\$(res $F6 .status)\" = complete ] && [ \"\$(res $A1 .status)\" = complete ]")" \
  "1 exits f6=$RF a1=$RA; status f6=$(res "$F6" .status) a1=$(res "$A1" .status)"
M2=PASS; DET=""
for D in "$DF" "$DA"; do for m in "$D"/reviews/*.meta.json; do
  case "$m" in *attempt*) continue;; esac
  rid=$(basename "$m" .meta.json); want=$(jq -r --arg r "$rid" '.models[$r]' "$D/run.json")
  ok=$(jq -r '.model_ok' "$m"); obs=$(jq -r '.observed_model' "$m")
  { [ "$ok" = true ] && [ "$obs" = "$want" ]; } || M2=FAIL; DET+="$rid=$obs "
done; done
item $M2 "2 final model_ok and observed models: $DET"
DL=$(cat "$DF"/reviews/*.timing.json "$DA"/reviews/*.timing.json | jq -s 'map(.dropped_lines)|add')
NB=$(jq -s 'map(.block_ok|length)|min' "$DF/merge-stdout.txt" "$DA/merge-stdout.txt" 2>/dev/null)
item "$(b "[ \"$DL\" = 0 ] && [ \"$NB\" = 3 ]")" "3 dropped_lines total=$DL; reviewer ids in each merge=$NB"
R=$(jq -r '.receivers[0]' "$DF/run.json")
CD=$(jq '[.cards[]?|select(.status=="delivered")]|length' "$DF/collab.json")
SM=$(jq --arg r "$R" '.reviewers[$r].snapshot_missing' "$DF/collab.json"); HE=$(jq --arg r "$R" '.reviewers[$r].hook_error' "$DF/collab.json")
SEAL=$(cat "$DF/board/snap/$R.t" 2>/dev/null || echo 0)
SESS=$(ls "$DF/reviews/$R".attempt1.session.jsonl 2>/dev/null)
TXT_T=$(jq -r 'select(tostring|test("Panel request \\(from the harness"))|.timestamp' "$SESS" 2>/dev/null | head -1)
TXT_MS=$( [ -n "$TXT_T" ] && date -d "$TXT_T" +%s%3N || echo 0)
VAL=$(cd "$(git -C "$R5" rev-parse --show-toplevel)" && PYTHONPATH="$R5/lib" uv run --no-sync python -m r5.panelmsg "${R5_SB:-/tmp/evalsb-collab-r5}/cand/$PKG/candidate.md" \
      "$(jq .k "$DF/run.json")" "$R" "$F6/$PKG" < "$DF/board/msgs/watcher.jsonl" >/dev/null 2>&1 && echo ok || echo bad)
SNAPOK=false; [ -s "$DF/board/snap/$R.sha256" ] && [ "$(cut -d' ' -f1 "$DF/board/snap/$R.sha256")" = "$(sha256sum "$DF/board/snap/$R.jsonl" | cut -d' ' -f1)" ] && SNAPOK=true
item "$(b "[ \"$CD\" -ge 1 ] && [ \"$SM\" = 0 ] && [ \"$HE\" = 0 ] && [ \"$TXT_MS\" -ge \"$SEAL\" ] && [ \"$SEAL\" -gt 0 ] && [ $VAL = ok ] && $SNAPOK")" \
  "4 f6 cards_delivered=$CD snapshot_missing=$SM hook_error=$HE card_text_in_transcript_at=$TXT_MS seal_t=$SEAL validator=$VAL snapshot_sha_ok=$SNAPOK"
SETS=$(jq -s '[.[]|.settings]|any' "$DA"/reviews/*.attempt*.meta.json)
F6NULL=$(jq '[.cards,.requests_posted,.requests_delivered,.requests_acted]|all(.==null)' "$DA/collab.json" 2>/dev/null)
item "$(b "[ ! -d \"$DA/board\" ] && [ \"$SETS\" = false ] && [ \"$F6NULL\" = true ]")" "5 a1 board_dir=$([ -d "$DA/board" ] && echo yes || echo no) settings_used=$SETS f6_fields_null=$F6NULL"
I6=PASS; D6=""
for row in "$F6" "$A1"; do
  k=$(jq -c --arg r "$row" 'select(.row==$r)' "$OUTR/results/scoring-keys.jsonl" | tail -1)
  tok=$(jq -r .token <<<"$k"); lab=$(jq -r .label <<<"$k"); st=$(jq -r .status <<<"$k")
  sc=$OUTR/scoring/$tok/$PKG/$lab/score.json; jq -e . "$sc" >/dev/null 2>&1 || I6=FAIL
  au=$(jq -r .status "$OUTR/runs/$row/$PKG/audit.json"); [ "$st" = ok ] && [ "$au" = pass ] || I6=FAIL
  D6+="$row: anon=$st score=$( [ -f "$sc" ] && echo parsed || echo missing) audit=$au; "
done
item $I6 "6 $D6"
EL=$(jq .elapsed_s "$DF/collab.json"); B=$(jq .B_f_s "$DF/run.json"); HK=$(jq '[.reviewers[].hang_kill]|any' "$DF/collab.json")
item "$(b "awk -v e=$EL -v b=$B 'BEGIN{exit !(e <= 1.5*b)}' && [ $HK = false ]")" "7 f6 elapsed_s=$EL B_f=$B hang_kill=$HK"
printf '%s' "$L"
{ echo; echo "## Smoke test (DESIGN 6.4): $ALL ($(date -u +%Y-%m-%dT%H:%M:%SZ))"; echo
  echo "Rows \`$F6\` and \`$A1\` on \`$PKG\`; checked by \`spikes/smoke-check.sh\`."; echo; printf '%s' "$L" | sed 's/^/- /'; } >> "$NOTES"
[ $ALL = PASS ]
