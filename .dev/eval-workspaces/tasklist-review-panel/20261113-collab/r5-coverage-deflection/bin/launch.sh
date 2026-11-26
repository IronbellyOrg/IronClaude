#!/usr/bin/env bash
# One panel on all requested packages: preflight, run, merge, anonymise, judge, results row (DESIGN 5).
# usage: launch.sh <panel> <row> [--pkgs <pkg>[,<pkg>...]]; env PANEL_COLLAB (default 1), PANEL_KIT, SPIKE4=1, NOFALLBACK=1
# exit: 0 complete, 1 partial/quarantined, 2 preflight refused, 3 F6 not runnable on this panel
set -u -o pipefail
PANEL=$1; ROW=$2; shift 2
R5=$(cd "$(dirname "$0")/.." && pwd); CFG=${R5_CONFIG:-$R5/config}; OUTR=${R5_OUT:-$R5}
REPO=$(git -C "$R5" rev-parse --show-toplevel)
PKGS=(TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415)
[ "${1:-}" = --pkgs ] && IFS=, read -r -a PKGS <<<"$2"
export PANEL_COLLAB=${PANEL_COLLAB:-1}; export PANEL_KIT=${PANEL_KIT:-0}; [ "$PANEL_COLLAB" = 1 ] && export PANEL_KIT=1
RD=$OUTR/runs/$ROW; LJ=$RD/launch.json
py() { (cd "$REPO" && PYTHONPATH="$R5/lib" uv run --no-sync python -m "$@"); }
refuse() { # <exit> <reason>
  echo "refused ($1): $2" >&2
  if [ -d "$RD" ] && [ ! -f "$LJ" ] || [ "${CREATED:-0}" = 1 ]; then
    jq -n --arg r "$2" --argjson e "$1" --arg row "$ROW" --arg panel "$PANEL" '{row:$row,panel:$panel,preflight:"refused",exit:$e,reason:$r}' > "$LJ"
  fi
  exit "$1"
}
case "$ROW" in */*|.*|'') echo "refused: bad row name" >&2; exit 2;; esac
[ -e "$RD" ] && { echo "refused (2): row folder $RD already exists" >&2; exit 2; }
mkdir -p "$RD"; CREATED=1
# 1. NOFALLBACK
[ "${NOFALLBACK:-}" = 1 ] || refuse 2 "NOFALLBACK=1 is not set"
# 2. models
PJ=$(jq -c --arg p "$PANEL" '.[$p]' "$CFG/panels.json"); [ "$PJ" != null ] || refuse 2 "unknown panel $PANEL"
for m in $(jq -r '.reviewers[].model' <<<"$PJ"); do
  case "$(tr 'A-Z' 'a-z' <<<"$m")" in *glm*|*qwen*|*opus*) refuse 2 "model $m is forbidden";; esac
  case " muse-ember-1.0 gpt-6-luna claude-haiku-5-5 claude-sonnet-5-5 grok-4.7 " in *" $m "*) ;; *) refuse 2 "model $m not in the allow-list";; esac
done
# 3. pins
PC=$(bash "$R5/bin/pins-check.sh" 2>&1); PCRC=$?  # rc 3 = values sums only: checked per panel in steps 5 and 6
[ $PCRC = 0 ] || [ $PCRC = 3 ] || refuse 2 "pins-check failed: $(grep FAIL <<<"$PC" | tr '\n' ';')"
# 4. sandboxes
SBX=$(bash "$R5/bin/sandbox-build.sh" "${PKGS[@]}" 2>&1) || refuse 2 "sandbox check failed: $(tr '\n' ';' <<<"$SBX")"
# 5./6. values. Owner decision 2026-11-14: PANEL_SLACK_S=<s> raises the cap to 1.35 B + s and reads values-slack<s>/ instead of values/
SLACK=${PANEL_SLACK_S:-0}
[[ $SLACK =~ ^(0|[1-9][0-9]*)$ ]] || refuse 2 "PANEL_SLACK_S must be a whole number of seconds (0, 30, ...), got '$SLACK'"
VDIR=values; [ "$SLACK" != 0 ] && VDIR=values-slack$SLACK
# Owner-authorised time-cap exception (2026-11-14, OVERRIDE.md): TIME_CAP_EXCEPTION=1 forces k = 1 where the measured k is 0 and widens the guards.
TCX=${TIME_CAP_EXCEPTION:-0}; PLANS='{}'
[[ $TCX =~ ^[01]$ ]] || refuse 2 "TIME_CAP_EXCEPTION must be 0 or 1 (forced k of 1), got '$TCX'"
if [ "$TCX" = 1 ]; then
  [ "$PANEL_COLLAB" = 1 ] || refuse 2 "TIME_CAP_EXCEPTION=1 applies to the collaboration arm only (PANEL_COLLAB=1); a baseline row must obey the cap"
  [ "$SLACK" = 0 ] || refuse 2 "TIME_CAP_EXCEPTION=1 and PANEL_SLACK_S are exclusive"
fi
if [ "$SLACK" != 0 ] && [ "${SPIKE4:-}" != 1 ]; then
  for p in "${PKGS[@]}"; do
    [ -f "$CFG/$VDIR/$PANEL/$p.json" ] && [ -f "$CFG/$VDIR/$PANEL/SHA256SUMS" ] ||
      refuse 2 "PANEL_SLACK_S=$SLACK but the slack values for panel $PANEL, package $p are missing ($CFG/$VDIR/$PANEL/); compute them from the Spike 4 rows: PANEL_SLACK_S=$SLACK uv run python -m r5.timing spike4 --panel $PANEL --rows <a1 rows> --kit-rows <a2 rows>"
  done
fi
if [ "$PANEL_COLLAB" = 1 ]; then
  [ "${SPIKE4:-}" = 1 ] && refuse 2 "SPIKE4=1 is for A1/A2 measurement rows only"
  anyk=0
  for p in "${PKGS[@]}"; do
    V=$CFG/$VDIR/$PANEL/$p.json
    [ -f "$V" ] || refuse 3 "F6 not runnable on $PANEL: no values file for $p (run Spike 4)"
    W=$(awk -v f="$p.json" '$2==f{print $1}' "$CFG/$VDIR/$PANEL/SHA256SUMS" 2>/dev/null)
    [ -n "$W" ] && [ "$W" = "$(sha256sum "$V" | cut -d' ' -f1)" ] || refuse 3 "F6 not runnable on $PANEL: values sum mismatch for $p (R-30)"
    if [ "$TCX" = 1 ]; then  # same checks on the numbers the exception will run with (k forced to 1, cap 2.7 B)
      PLAN=$(py r5.timing exception "$V") || refuse 3 "F6 not runnable on $PANEL: time-cap exception plan failed for $p"
      PLANS=$(jq -c --arg p "$p" --argjson plan "$PLAN" '.[$p]=$plan' <<<"$PLANS")
      BOK=$(jq .budget_ok <<<"$PLAN"); KK=$(jq .k_run <<<"$PLAN"); LIM=$(jq .slowdown_limit <<<"$PLAN")
    else
      BOK=$(jq .budget_ok "$V"); KK=$(jq .k "$V"); LIM=$(jq .slowdown_limit "$V")
    fi
    [ "$BOK" = true ] || refuse 3 "F6 not runnable on $PANEL: budget_ok false for $p (slowdown $(jq .slowdown_s "$V") > limit $LIM)"
    [ "$KK" -ge 1 ] && anyk=1
  done
  [ $anyk = 1 ] || refuse 3 "F6 not runnable on $PANEL: k = 0 on every package (T_report_p90: $(for p in "${PKGS[@]}"; do jq -r '"\(.pkg[8:20])=\(.T_report_p90_s)s"' "$CFG/$VDIR/$PANEL/$p.json"; done | tr '\n' ' '))"
elif [ "${SPIKE4:-}" != 1 ]; then
  for p in "${PKGS[@]}"; do
    V=$CFG/$VDIR/$PANEL/$p.json
    [ -f "$V" ] || refuse 2 "no values file for $p; PANEL_COLLAB=0 without values needs SPIKE4=1"
    W=$(awk -v f="$p.json" '$2==f{print $1}' "$CFG/$VDIR/$PANEL/SHA256SUMS" 2>/dev/null)
    [ -n "$W" ] && [ "$W" = "$(sha256sum "$V" | cut -d' ' -f1)" ] || refuse 3 "values sum mismatch for $p (R-30)"
  done
fi
# 7. versions
jq -n --arg row "$ROW" --arg panel "$PANEL" --arg cv "$(claude --version 2>&1 | head -1)" --arg sv "$(superclaude --version 2>&1 | head -1)" \
  --arg pkgs "$(IFS=,; echo "${PKGS[*]}")" --argjson collab "$PANEL_COLLAB" --argjson kit "$PANEL_KIT" --arg s4 "${SPIKE4:-0}" \
  --argjson tcx "$TCX" --argjson plans "$PLANS" \
  --argjson models "$(jq -c '.reviewers|map({(.rid):.model})|add' <<<"$PJ")" --argjson t "$(date +%s%3N)" \
  '{row:$row,panel:$panel,preflight:"ok",claude_version:$cv,superclaude_version:$sv,pkgs:($pkgs|split(",")),models:$models,
    time_cap_exception:($tcx==1),time_cap_plan:$plans,
    env:{PANEL_COLLAB:$collab,PANEL_KIT:$kit,NOFALLBACK:1,SPIKE4:($s4=="1"),TIME_CAP_EXCEPTION:$tcx},t_start_ms:$t}' > "$LJ"

for p in "${PKGS[@]}"; do  # packages one after another (D11)
  bash "$R5/bin/run-panel.sh" "$ROW" "$PANEL" "$p" || echo "run-panel $p rc=$?" >&2
  bash "$R5/bin/merge.sh" "$ROW" "$p" || echo "merge $p rc=$?" >&2
  py r5.collab "$RD/$p"; py r5.alarms package "$RD/$p" --ref "$OUTR/results/arm-summary-A1-$PANEL.json" > /dev/null
done
for p in "${PKGS[@]}"; do  # judges one after another (D11)
  [ "$(jq -r '.merge // ""' "$RD/$p/pkg-status.json" 2>/dev/null)" = ok ] || continue
  TL=$(bash "$R5/bin/anon.sh" "$ROW" "$p") || { echo "anon $p failed: not judged" >&2; continue; }
  read -r TOKEN L <<<"$TL"
  bash "$R5/bin/judge.sh" "$TOKEN" "$p" "$L" "$ROW" || echo "judge $p failed" >&2
done
RES=$(py r5.results "$ROW")
ST=$(jq -r .status <<<"$RES")
jq --argjson t "$(date +%s%3N)" --arg s "$ST" '.t_end_ms=$t|.status=$s' "$LJ" > "$LJ.tmp" && mv "$LJ.tmp" "$LJ"
echo "$RES"
[ "$ST" = complete ] && exit 0 || exit 1
