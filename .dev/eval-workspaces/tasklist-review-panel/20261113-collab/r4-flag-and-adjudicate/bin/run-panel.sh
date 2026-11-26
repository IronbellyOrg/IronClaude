#!/usr/bin/env bash
# run-panel.sh: the one launch script (design 5.1).
#   PANEL_COLLAB=0|1 NOFALLBACK=1 run-panel.sh --panel EL2|SL2|HL2 --row <row-id> --values <values file>
#       [--packages "<ids>"] [--seed <int>] [--block <id>] [--no-judge]
#   run-panel.sh --print-session-count   (prints "<all> <ember>" for the concurrency check; used by tests)
# Reads PANEL_COLLAB (default 1), NOFALLBACK, R4_SBR and R4_OUT.
set -u -o pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
REPO=${R4_REPO:-$(cd "$HERE/../../../../.." && pwd)}
EVAL="$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
SBR=${R4_SBR:-/tmp/evalsb-collab-r4}
OUT=${R4_OUT:-$HERE}
PY=(uv run --frozen --project "$REPO" python)
now_ms() { date +%s%3N; }
count_sessions() {
  local a e
  a=$(pgrep -fc '(^|/)claude -p( |$)' || true)
  e=$(pgrep -fc '(^|/)claude -p --model muse-ember-1.0( |$)' || true)
  echo "${a:-0} ${e:-0}"
}
[ "${1:-}" = --print-session-count ] && { count_sessions; exit 0; }

PANEL="" ROW="" VALUES="" PKGS="" SEED="" BLOCK="" NOJUDGE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --panel) PANEL=${2-}; shift 2 ;; --row) ROW=${2-}; shift 2 ;; --values) VALUES=${2-}; shift 2 ;;
    --packages) PKGS=${2-}; shift 2 ;; --seed) SEED=${2-}; shift 2 ;; --block) BLOCK=${2-}; shift 2 ;;
    --no-judge) NOJUDGE=1; shift ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
COLLAB=${PANEL_COLLAB:-1}
# Owner-authorised time-cap exception (OVERRIDE.md, 2026-11-14), default off. TIME_CAP_EXCEPTION=1 forces k = 1 on a package
# whose measured k is 0 and widens the hang guard and finish time (lib/values.py tce_entry); every such row is stamped.
TCE=${TIME_CAP_EXCEPTION:-0}
SLACK=${PANEL_SLACK_S:-0}  # seconds added to the 35% cap (cap = 1.35 B + SLACK); 0 = the old cap
mkdir -p "$OUT/runs" "$OUT/results"
RD="$OUT/runs/$ROW"

refuse() {
  jq -nc --arg row "$ROW" --arg t "$(date -u +%FT%TZ)" --arg r "$1" '{row:$row,time:$t,reason:$r}' >> "$OUT/runs/refusals.jsonl"
  echo "refused: $1" >&2
  exit 2
}

# ---- 0. preflight: refuse before any work, never touching runs/<row>/
[ -n "$ROW" ] || refuse "no --row"
[[ "$ROW" =~ ^[A-Za-z0-9._-]+$ ]] || refuse "bad row id"
[ "${NOFALLBACK:-}" = 1 ] || refuse "NOFALLBACK is not 1"
case "$COLLAB" in 0|1) ;; *) refuse "PANEL_COLLAB is not 0 or 1" ;; esac
case "$TCE" in 0|1) ;; *) refuse "TIME_CAP_EXCEPTION is not 0 or 1" ;; esac
[[ "$SLACK" =~ ^(0|[1-9][0-9]*(\.[0-9]+)?)$ ]] || refuse "PANEL_SLACK_S is not a plain non-negative number of seconds: $SLACK"
[ "$TCE" = 0 ] || [ "$COLLAB" = 1 ] || refuse "TIME_CAP_EXCEPTION=1 needs PANEL_COLLAB=1"
PDEF=$(jq -c --arg p "$PANEL" '.panels[$p] // empty' "$HERE/frozen/panels.json")
[ -n "$PDEF" ] || refuse "unknown panel '$PANEL'"
[ -e "$RD" ] && refuse "row directory exists: runs/$ROW"
(cd "$HERE/frozen" && sha256sum -c --quiet pins.sha256 >/dev/null 2>&1) || refuse "pins check failed (frozen/pins.sha256)"
if [ "$SLACK" != 0 ]; then  # owner decision 2026-11-14: cap = 1.35 B + PANEL_SLACK_S; the slack values live in values-slack<S>/
  [ -n "$VALUES" ] || VALUES="$OUT/values-slack$SLACK/$PANEL.json"
  [ -f "$VALUES" ] && [ -f "$VALUES.sha256" ] || refuse "PANEL_SLACK_S=$SLACK but the slack values file for $PANEL is missing ($VALUES or its .sha256); build it with PANEL_SLACK_S=$SLACK values.py build/srun/slowdown"
fi
[ -f "$VALUES" ] && [ -f "$VALUES.sha256" ] || refuse "values file or its .sha256 missing"
VSHA=$(sha256sum "$VALUES" | cut -d' ' -f1)
[ "$VSHA" = "$(cut -d' ' -f1 "$VALUES.sha256")" ] || refuse "values sha256 differs from $VALUES.sha256"
[ "$(jq -r .panel "$VALUES")" = "$PANEL" ] || refuse "values file is for another panel"
jq -e --argjson s "$SLACK" '(.slack_s // 0) == $s' "$VALUES" >/dev/null || refuse "values file slack_s ($(jq -r '.slack_s // 0' "$VALUES")) differs from PANEL_SLACK_S=$SLACK"
if [ "$TCE" = 1 ]; then  # the exception is defined on a measured B_A1 and needs delivery on
  case "$(jq -r '.kind // ""' "$VALUES")" in planning|srun) refuse "TIME_CAP_EXCEPTION=1 needs measured values, not kind $(jq -r .kind "$VALUES")" ;; esac
fi
declare -A TCEJ
FLAGGER=$(jq -r .flagger.rid <<<"$PDEF"); FMODEL=$(jq -r .flagger.model <<<"$PDEF")
mapfile -t ADJ < <(jq -r '.adjudicators[].rid' <<<"$PDEF")
PEERS="${ADJ[0]},${ADJ[1]}"
while IFS=$'\t' read -r rid model; do
  jq -e --arg m "$model" '.allowed_models | index([$m])' "$HERE/frozen/panels.json" >/dev/null || refuse "model not allowed: $model"
  echo "$model" | grep -qiE 'glm|qwen|opus' && refuse "forbidden model: $model"
done < <(jq -r '(.flagger, .adjudicators[]) | [.rid, .model] | @tsv' <<<"$PDEF")
[ "$FMODEL" = gpt-6-luna ] && refuse "flagger model is gpt-6-luna"
ALLPKGS=$(jq -r '.[].id' "$HERE/frozen/packages.json")
[ -n "$PKGS" ] || PKGS=$ALLPKGS
for p in $PKGS; do
  grep -qxF -- "$p" <<<"$ALLPKGS" || refuse "unknown package $p"
  jq -e --arg p "$p" '.packages[$p]' "$VALUES" >/dev/null || refuse "values file lacks $p"
  [ -f "$SBR/sb/$p/built.json" ] || refuse "sandbox missing for $p (run build-sandbox.sh)"
  [ "$(sha256sum "$SBR/cand/$p/candidate.md" 2>/dev/null | cut -d' ' -f1)" = "$(jq -r --arg p "$p" '.packages[]|select(.package==$p)|.candidate_sha256' "$OUT/manifest.json" 2>/dev/null)" ] \
    || refuse "candidate copy for $p does not match manifest.json"
  if [ "$TCE" = 1 ]; then
    [ "$(jq -r --arg p "$p" '.packages[$p].deliver' "$VALUES")" = true ] || refuse "TIME_CAP_EXCEPTION=1 needs deliver true for $p"
    TCEJ[$p]=$("${PY[@]}" "$HERE/lib/values.py" tce --values "$VALUES" --pkg "$p") || refuse "values.py tce failed for $p"
  fi
done
if [ "$COLLAB" = 1 ] && [ "$TCE" = 0 ]; then
  anyk=0; for p in $PKGS; do [ "$(jq -r --arg p "$p" '.packages[$p].k' "$VALUES")" -ge 1 ] && anyk=1; done
  [ "$anyk" = 1 ] || refuse "F7 not runnable on $PANEL: k = 0 on every package (values $VSHA)"
fi

# ---- 1. row start
[ "$TCE" = 1 ] && echo "TIME_CAP_EXCEPTION=1: owner-authorised exception to the +35% cap; this row is stamped time_cap_exception and is not comparable with cap-obeying rows" >&2
mkdir -p "$RD"
[ -n "$SEED" ] || SEED=$(od -An -N4 -tu4 /dev/urandom | tr -d ' ')
ARM=A1; [ "$COLLAB" = 1 ] && ARM=F7
START_ISO=$(date -u +%FT%TZ); START_MS=$(now_ms)
jq -n --arg row "$ROW" --arg panel "$PANEL" --argjson pdef "$PDEF" --argjson c "$COLLAB" --arg arm "$ARM" --arg v "$(realpath "$VALUES")" \
  --arg vsha "$VSHA" --argjson seed "$SEED" --arg block "$BLOCK" --arg st "$START_ISO" --argjson sms "$START_MS" --arg sbr "$SBR" --arg out "$OUT" \
  --argjson tce "$TCE" --argjson slack "$SLACK" \
  '{row:$row,panel:$panel,models:([$pdef.flagger]+$pdef.adjudicators|map({(.rid):.model})|add),panel_collab:$c,arm:$arm,nofallback:"1",
    time_cap_exception:($tce==1),slack_s:$slack,values:$v,values_sha256:$vsha,pins_ok:true,seed:$seed,block:$block,started:$st,start:$sms,sbr:$sbr,out:$out,status:"running"}' > "$RD/run.json"
runjson() { jq "$@" "$RD/run.json" > "$RD/run.json.tmp" && mv "$RD/run.json.tmp" "$RD/run.json"; }

# ---- 2. packages, one after another
j=0; STATUS=done
for PKG in $PKGS; do
  PD="$RD/$PKG"; mkdir -p "$PD"/{reviews,tags,scoring}
  V=$(jq -c --arg p "$PKG" '.packages[$p]' "$VALUES")
  [ "$TCE" = 1 ] && V=$(jq -c --argjson t "${TCEJ[$PKG]}" '. + $t' <<<"$V")  # effective k, finish offset, hang guard
  K=$(jq -r .k <<<"$V"); DELIVER=$(jq -r 'if .deliver then 1 else 0 end' <<<"$V")
  R=$(( (SEED >> (2 * j)) & 1 )); C=$(( (SEED >> (2 * j + 1)) & 1 )); j=$((j + 1))
  PCOLLAB=$COLLAB; K0=false
  [ "$COLLAB" = 1 ] && [ "$K" -lt 1 ] && { PCOLLAB=0; K0=true; }
  CAND="$SBR/cand/$PKG/candidate.md"
  BD=""; HELPER=""
  # concurrency (REQ 4: at most 10 sessions, at most 4 ember), host-wide
  exec 7>"$SBR/launch.lock"; waited=0
  while :; do
    flock 7
    read -r NALL NEMB < <(count_sessions)
    if [ "$NALL" -le 7 ] && { [ "$PANEL" != EL2 ] || [ "$NEMB" -le 3 ]; }; then break; fi
    flock -u 7
    [ "$waited" -ge 1800 ] && { STATUS=concurrency_refused; break 2; }
    sleep 30; waited=$((waited + 30))
  done
  # T0, deadlines
  T0=$(now_ms)
  F=$(( T0 + $(jq -r '(.finish_offset_s*1000|round)' <<<"$V") ))
  H=$(( T0 + $(jq -r '(.hang_s*1000|round)' <<<"$V") ))
  SETTINGS="{}"
  if [ "$PCOLLAB" = 1 ]; then
    BD="$SBR/board/$ROW/$PKG"; mkdir -p "$BD"/{msgs,state,snap,metrics,settings,bin}
    for rid in "$FLAGGER" "${ADJ[@]}"; do
      role=adjudicator; [ "$rid" = "$FLAGGER" ] && role=flagger
      CMD="$HERE/bin/r4-hook --board $BD --rid $rid --role $role --flagger $FLAGGER --t0-ms $T0 --finish-ms $F --k $K --deliver $DELIVER --c $C"
      jq -n --arg cmd "$CMD" '{hooks:{PostToolUse:[{hooks:[{type:"command",command:$cmd,timeout:5}]}]}}' > "$BD/settings/$rid.json"
      SETTINGS=$(jq -c --arg r "$rid" --arg f "$BD/settings/$rid.json" '. + {($r):$f}' <<<"$SETTINGS")
    done
    HELPER="$BD/bin/card"
    printf '#!/usr/bin/env bash\nexec %q --board %q --rid %q --run %q --cand-flat %q --cap %d --t0-ms %d --finish-ms %d --r %d --peers %q "$@"\n' \
      "$HERE/bin/panel-post" "$BD" "$FLAGGER" "$ROW/$PKG" "$SBR/cand/$PKG/candidate.flat" $((2 * K)) "$T0" "$F" "$R" "$PEERS" > "$HELPER"
    chmod +x "$HELPER"
  fi
  jq -n --arg row "$ROW" --arg pkg "$PKG" --arg panel "$PANEL" --arg arm "$ARM" --argjson collab "$PCOLLAB" --argjson k "$K" \
    --argjson k0 $K0 --argjson del "$DELIVER" --argjson r "$R" --argjson c "$C" --argjson t0 "$T0" --argjson f "$F" --argjson h "$H" \
    --argjson v "$V" --arg vsha "$VSHA" --arg sb "$SBR/sb/$PKG/repo" --arg cand "$CAND" --arg src "$SBR/cand/$PKG/source.md" \
    --arg cflat "$SBR/cand/$PKG/candidate.flat" --arg csha "$(sha256sum "$CAND" | cut -d' ' -f1)" --argjson set "$SETTINGS" \
    --arg helper "$HELPER" --arg board "$BD" --argjson pdef "$PDEF" --argjson tce "$TCE" \
    '{row:$row,pkg:$pkg,panel:$panel,arm:$arm,collab:$collab,k:$k,k0_isolated:$k0,deliver:$del,
      time_cap_exception:($tce==1),k_measured:($v.k_measured // $v.k),k_forced:($v.k_forced // false),
      finish_offset_s:$v.finish_offset_s,hang_s:$v.hang_s,r:$r,c:$c,t0_ms:$t0,finish_ms:$f,hang_ms:$h,
      B_A1:$v.B_A1,turn_p90:$v.turn_p90,T_report_p90:$v.T_report_p90,cp_role:$pdef.cp_role,values_sha256:$vsha,sandbox:$sb,cand:$cand,src:$src,
      cand_flat:$cflat,cand_sha:$csha,settings:$set,helper:(if $helper=="" then null else $helper end),board:(if $board=="" then null else $board end),
      flagger:$pdef.flagger.rid,peers:[$pdef.adjudicators[].rid],
      reviewers:([$pdef.flagger+{role:"flagger"}]+($pdef.adjudicators|map(.+{role:"adjudicator"})))}' > "$PD/panel.json"
  # start the three reviewers together
  pids=()
  bash "$HERE/bin/reviewer.sh" "$PD" "$FLAGGER" "$FMODEL" flagger "$PCOLLAB" & pids+=($!)
  for a in "${ADJ[@]}"; do
    m=$(jq -r --arg r "$a" '.adjudicators[]|select(.rid==$r)|.model' <<<"$PDEF")
    bash "$HERE/bin/reviewer.sh" "$PD" "$a" "$m" adjudicator "$PCOLLAB" & pids+=($!)
  done
  flock -u 7; exec 7>&-
  wait "${pids[@]}"
  # board copy (R-26)
  [ -n "$BD" ] && cp -a "$BD" "$PD/board"
  # merge (R-04)
  PST=ok
  if jq -s -e 'any(.[]; .model_mismatch == true)' "$PD"/reviews/{"$FLAGGER","${ADJ[0]}","${ADJ[1]}"}.meta.json >/dev/null 2>&1; then
    PST=invalid_model
  else
    REV=$(jq -c --argjson pdef "$PDEF" '. as $p | [$pdef.flagger] + $pdef.adjudicators | map({reviewer_id:.rid,model:.model,alias:$p.ALIAS[.rid],
      tier:$p.TIER[.rid],strategy:"fixed",stand_in:false,fallback_depth:0,fallbacks:[],launch:null,seed:null,slot_id:(.rid|split("-")[0])})' "$HERE/frozen/panels.json")
    jq -c --argjson rev "$REV" '.reviewers=$rev' "$EVAL/$PKG/resolution-live7.json" > "$PD/resolution.json"
    ARGS=(); for rid in "$FLAGGER" "${ADJ[@]}"; do ARGS+=(--report "$rid=$PD/reviews/$rid.final.md"); done
    uv run --frozen --project "$REPO" superclaude review merge --ledger "$PD/ledger.json" --doc "$CAND" --round 1 "${ARGS[@]}" \
      --resolution "$PD/resolution.json" --out "$PD/merged-1.md" > "$PD/merge-stdout.txt" 2>&1 \
      || { PST=merge_refused; head -1 "$PD/merge-stdout.txt" > "$PD/merge-refused.txt"; }
  fi
  echo "$PST" > "$PD/status"
  "${PY[@]}" "$HERE/lib/collab.py" "$PD" 2> "$PD/collab.err" || echo "collab.py failed" >&2
done
[ "$STATUS" = concurrency_refused ] && echo "refused remaining packages: concurrency limit for 30 minutes" >&2

# ---- 3. audit, after every reviewer of the row has exited
runjson --arg e "$(now_ms)" '.reviewers_end=($e|tonumber)'
"${PY[@]}" "$HERE/lib/audit.py" "$RD" 2> "$RD/audit.err" || echo "audit.py failed" >&2
VIOL=$(jq -c '.violations // []' "$RD/audit.json" 2>/dev/null || echo '["audit.py failed"]')
if [ "$VIOL" != "[]" ]; then
  printf 'QUARANTINED %s\nviolations: %s\n' "$(date -u +%FT%TZ)" "$VIOL" > "$RD/QUARANTINED"
  for b in "$RD"/*/board; do [ -d "$b" ] && cp "$RD/QUARANTINED" "$b/QUARANTINED"; done
fi

if [ "$NOJUDGE" = 0 ]; then
  for PKG in $PKGS; do
    PD="$RD/$PKG"; [ -f "$PD/status" ] || continue
    [ "$(cat "$PD/status")" = ok ] || continue
    # ---- 4. anonymise
    if ! bash "$HERE/bin/anon.sh" "$PD/merged-1.md" "$PD/scoring/merged-anon.md" 2> "$PD/scoring/anon.err"; then
      echo anon_failed > "$PD/status"; continue
    fi
    # ---- 5. judge
    bash "$HERE/bin/judge.sh" "$PD" "$PD/scoring/merged-anon.md" > "$PD/scoring/judge.out" 2>&1 || cat "$PD/scoring/judge-status" > "$PD/status"
  done
  # ---- 6. results
  "${PY[@]}" "$HERE/lib/results.py" "$RD" --out "$OUT/results/$ROW.json" 2> "$RD/results.err" || echo "results.py failed" >&2
fi

# ---- 7. end
END_ISO=$(date -u +%FT%TZ)
for PKG in $PKGS; do s=$(cat "$RD/$PKG/status" 2>/dev/null || echo not_run); [ "$s" != ok ] && [ "$STATUS" = done ] && STATUS="$PKG:$s"; done
[ "$NOJUDGE" = 0 ] && [ ! -f "$OUT/results/$ROW.json" ] && [ "$STATUS" = done ] && STATUS=results_failed
runjson --arg e "$END_ISO" --arg s "$STATUS" --argjson em "$(now_ms)" '.finished=$e | .end=$em | .status=$s'
jq -nc --arg row "$ROW" --arg panel "$PANEL" --arg arm "$ARM" --arg block "$BLOCK" --argjson s "$START_MS" --argjson e "$(now_ms)" \
  --argjson tce "$TCE" '{row:$row,panel:$panel,arm:$arm,block:$block,start:$s,end:$e} + (if $tce == 1 then {time_cap_exception:true} else {} end)' >> "$OUT/runs/schedule.jsonl"
[ -f "$OUT/results/$ROW.json" ] && jq -r '"\(.row): found \(.found_14)/14, real blocking \(.real_blocking_8)/8, control \(.control_found_2)/2, elapsed \(.elapsed_s|tostring), cards \([.collab[]?.cards_sent]|add)/\([.collab[]?.cards_delivered]|add)"' "$OUT/results/$ROW.json"
[ "$STATUS" = done ] && [ "$NOJUDGE" = 0 ] && exit 0
[ "$STATUS" = done ] && [ "$NOJUDGE" = 1 ] && exit 0
exit 1
