#!/usr/bin/env bash
# package.sh <rundir> <pkg>: one panel on one package (section 4).
# exit 0 package valid; 3 package invalid (reason in pkg.json).
set -u -o pipefail
source "$(dirname "$0")/common.sh"
RUNDIR=$1; PKG=$2
PD=$RUNDIR/$PKG
r3_assert_writable "$PD" || exit 3
mkdir -p "$PD/reviews" "$PD/board" "$PD/merged"
RUN=$RUNDIR/run.json
RUN_ID=$(jq -r .run_id "$RUN"); PANEL=$(jq -r .panel "$RUN"); COLLAB=$(jq -r .collab "$RUN")
SMOKE=$(jq -r '.smoke // false' "$RUN"); SPIKE4=$(jq -r '.spike4 // false' "$RUN")
PANELS=$R3/config/panels.json
mapfile -t RIDS < <(jq -r --arg p "$PANEL" '.[$p] | ([.searcher] + .readers)[] | .rid' "$PANELS")
declare -A MODEL
for r in "${RIDS[@]}"; do MODEL[$r]=$(jq -r --arg p "$PANEL" --arg r "$r" '.[$p] | ([.searcher] + .readers)[] | select(.rid==$r) | .model' "$PANELS"); done

# 1. values
VFLAGS=(); [ "$SMOKE" = true ] && VFLAGS+=(--smoke); [ "$SPIKE4" = true ] && VFLAGS+=(--spike4)
TCE_N=$(jq -r '.tce_forced_n // 0' "$RUN")  # owner-authorised time-cap exception (OVERRIDE.md); 0 = off
[ "$TCE_N" != 0 ] && VFLAGS+=(--tce "$TCE_N")
VALS=$(r3_py values-show --panel "$PANEL" "${VFLAGS[@]}") || { echo "values refused" >&2; exit 3; }
B_F=$(jq -r --arg k "$PKG" '.values.packages[$k].B_f' <<<"$VALS")
TCE=$(jq -c --arg k "$PKG" '.tce[$k] // null' <<<"$VALS")
mkdir -p "$SB/$PKG/active"; touch "$SB/$PKG/active/$RUN_ID"

# 2. admission (13.3)
EMBER_HERE=0; for r in "${RIDS[@]}"; do [ "${MODEL[$r]}" = muse-ember-1.0 ] && EMBER_HERE=$((EMBER_HERE+1)); done
r3_admit "$SB/admit.lock" "$EMBER_HERE"
T0=$(r3_now)
if [ "$SPIKE4" = true ]; then HANG_AT=$(r3_calc "$T0 + 3000"); else HANG_AT=$(r3_calc "$T0 + 1.5 * $B_F"); fi
SLACK=$(jq -r '.values.slack_s // 0' <<<"$VALS")  # PANEL_SLACK_S, checked against the values file by values-show
P2_DEADLINE=$(r3_calc "$T0 + 1.30 * $B_F + $SLACK")
if [ "$TCE" != null ]; then  # widened kill timers: hang guard max(1.5 B_f, 3.0 B_A1); phase-2 deadline after it
  HANG_AT=$(r3_calc "$T0 + $(jq -r .hang_offset_s <<<"$TCE")")
  P2_DEADLINE=$(r3_calc "$T0 + $(jq -r .p2_deadline_offset_s <<<"$TCE")")
fi
CAND_SB=$SB/cand/$PKG/candidate.md; SRC_SB=$SB/cand/$PKG/source.md
jq -n --arg run "$RUN_ID" --arg pkg "$PKG" --arg panel "$PANEL" --argjson collab "$COLLAB" --argjson T0 "$T0" --argjson B "$B_F" \
  --argjson p2 "$P2_DEADLINE" --argjson hang "$HANG_AT" --arg cand "$CAND_SB" --arg src "$SRC_SB" \
  --arg csha "$(sha256sum "$CAND_SB" | cut -d' ' -f1)" --arg ssha "$(sha256sum "$SRC_SB" | cut -d' ' -f1)" \
  --arg cev "$EVAL/$PKG/candidate.md" --arg sbp "$SB/$PKG" --arg tree "$(git -C "$SB/$PKG/repo" rev-parse 'HEAD^{tree}')" \
  --argjson vals "$VALS" --argjson tce "$TCE" \
  '{run_id:$run,pkg:$pkg,panel:$panel,collab:$collab,T0:$T0,B_f:$B,P2_DEADLINE:$p2,HANG_AT:$hang,cand_sb:$cand,src_sb:$src,
    cand_eval:$cev,cand_sha256:$csha,src_sha256:$ssha,sb_pkg:$sbp,sandbox_tree:$tree,turn_p90:$vals.values.turn_p90,
    values_sha256:$vals.sha256,values_status:$vals.values.status,values:{pkg:$vals.values.packages[$pkg]},p1_sha256:{},valid:null}
   | if $tce then .tce=$tce | .values.pkg.panel_finish_offset_s=$tce.finish_offset_s else . end' > "$PD/pkg.json"
r3_event "$PD" "-" T0 --argjson B_f "$B_F"

# 3. phase 1 for all three reviewers at T0
declare -A PIDS
for r in "${RIDS[@]}"; do
  bash "$R3/lib/reviewer.sh" phase1 "$PD" "$r" "${MODEL[$r]}" >"$PD/reviews/$r.phase1.log" 2>&1 &
  PIDS[$r]=$!
done
for _ in $(seq 1 50); do
  [ "$(pgrep -c -f '^timeout .* claude -p --model ' || true)" -ge 3 ] && break
  alive=0; for p in "${PIDS[@]}"; do kill -0 "$p" 2>/dev/null && alive=1; done
  [ $alive = 0 ] && break  # all three phase-1 jobs already ended (fast fakes): nothing left to wait for
  sleep 0.1
done
flock -u 8; exec 8>&-

state() { cat "$PD/reviews/$1.p1.state" 2>/dev/null; }
settled() { [ -n "$(state "$1")" ]; }

# 4. scheduler (collab only)
declare -A DONE WAITLOG
P2PIDS=()
if [ "$COLLAB" = 1 ]; then
  SEARCHER=$(jq -r --arg p "$PANEL" '.[$p].searcher.rid' "$PANELS")
  mapfile -t READERS < <(jq -r --arg p "$PANEL" '.[$p].readers[].rid' "$PANELS")
  BOXCAP=$(jq -r --arg p "$PANEL" '.[$p].box_cap_s // "null"' "$PANELS")
  sources_of() { if [ "$1" = "$SEARCHER" ]; then echo "${READERS[@]}"; else echo "$SEARCHER"; fi; }
  cap_of() { jq -r --arg p "$PANEL" --arg r "$1" '.[$p] | ([.searcher] + .readers)[] | select(.rid==$r) | .cap' "$PANELS"; }
  n_now() { # 6.5 with start cost 6, relative times
    local turn; turn=$(jq -r --arg m "${MODEL[$1]}" '.turn_p90[$m]' "$PD/pkg.json")
    local tf=0 te=0; [ "$TCE" != null ] && { tf=$(jq -r .forced_n <<<"$TCE"); te=$(jq -r .p2_deadline_offset_s <<<"$TCE"); }
    awk -v B="$B_F" -v S="$SLACK" -v rel="$(r3_calc "$(r3_now) - $T0")" -v cap="$(cap_of "$1")" -v bc="$BOXCAP" -v t="$turn" -v tf="$tf" -v te="$te" 'BEGIN{
      box = 1.30*B + S - rel; if (bc != "null" && bc+S < box) box = bc+S;
      x = (box - 6) / (2*t) + 1e-9; n = (x >= 0) ? int(x) : -1; if (n > cap) n = cap; if (n < 0) n = 0;
      if (n == 0 && tf > 0) { f = (tf > cap) ? cap : tf; if (f > 0 && te - rel - 6 >= 2*f*t) n = f }  # time-cap exception floor
      print n }'
  }
  while :; do
    all=1
    for r in "${RIDS[@]}"; do
      [ -n "${DONE[$r]:-}" ] && continue
      st=$(state "$r")
      if [ -z "$st" ]; then all=0; continue; fi
      if [ "$st" != sealed ]; then DONE[$r]=1; continue; fi
      if [ "$(jq -r '.retry_isolated' "$PD/reviews/$r.meta.json")" = true ]; then
        r3_event "$PD" "$r" no_launch --arg reason retry_isolated; DONE[$r]=1; continue
      fi
      if [ "$(n_now "$r")" = 0 ]; then r3_event "$PD" "$r" no_launch --arg reason deadline; DONE[$r]=1; continue; fi
      ok=1; for s in $(sources_of "$r"); do settled "$s" || ok=0; done
      if [ $ok = 1 ]; then
        out=$(r3_py digest --pkgdir "$PD" --rid "$r" --t-launch "$(r3_now)" --start-cost 6); drc=$?
        if [ $drc = 0 ]; then
          r3_event "$PD" "$r" launch --arg digest "$out"
          bash "$R3/lib/reviewer.sh" phase2 "$PD" "$r" "${MODEL[$r]}" >"$PD/reviews/$r.phase2.log" 2>&1 &
          P2PIDS+=($!)
        else
          r3_event "$PD" "$r" no_launch --arg reason no_slots --arg digest "$out"
        fi
        DONE[$r]=1
      else
        all=0
        [ -z "${WAITLOG[$r]:-}" ] && { r3_event "$PD" "$r" waiting_for --arg sources "$(sources_of "$r")"; WAITLOG[$r]=1; }
      fi
    done
    [ $all = 1 ] && break
    sleep 1
  done
fi

# 5. wait for every background process
wait

# 6. combine
INVALID=""; SLO=false
for r in "${RIDS[@]}"; do
  st=$(state "$r")
  case $st in
    sealed) r3_py combine --pkgdir "$PD" --rid "$r" 2>>"$PD/reviews/$r.combine.err" || INVALID="${INVALID:+$INVALID; }E_COMBINE $r";;
    hang_kill) INVALID="${INVALID:+$INVALID; }hang_kill $r"; SLO=true;;
    *) INVALID="${INVALID:+$INVALID; }phase1 failed $r";;
  esac
done

# 7. merge (R-04)
REV=$(for r in "${RIDS[@]}"; do jq -nc --arg r "$r" --arg m "${MODEL[$r]}" '{reviewer_id:$r,model:$m,alias:null,tier:null,strategy:"fixed",stand_in:false,fallback_depth:0,fallbacks:[],launch:null,seed:null,slot_id:($r|split("-")[0])}'; done | jq -sc .)
jq -c --argjson rev "$REV" '.reviewers=$rev' "$EVAL/$PKG/resolution-live7.json" > "$PD/merged/resolution.json"
cmp -s "$EVAL/$PKG/candidate.md" "$CAND_SB" || INVALID="${INVALID:+$INVALID; }candidate copy differs"
merge() { # <outdir> <suffix of report file>
  local out=$1 suf=$2 args=() r
  mkdir -p "$out"; [ "$out" = "$PD/merged" ] || cp "$PD/merged/resolution.json" "$out/resolution.json"
  for r in "${RIDS[@]}"; do [ -f "$PD/reviews/$r$suf" ] && args+=(--report "$r=$(realpath "$PD/reviews/$r$suf")"); done
  [ ${#args[@]} -gt 0 ] || { echo "no reports" > "$out/merge-stdout.txt"; return 1; }
  uv run --frozen --project "$REPO" superclaude review merge --ledger "$out/ledger.json" --doc "$EVAL/$PKG/candidate.md" \
    --round 1 "${args[@]}" --resolution "$out/resolution.json" --out "$out/merged-1.md" > "$out/merge-stdout.txt" 2>&1
}
merge "$PD/merged" .md || INVALID="${INVALID:+$INVALID; }merge refused: $(tail -1 "$PD/merged/merge-stdout.txt")"
# 8. sealed merge (collab only)
[ "$COLLAB" = 1 ] && { merge "$PD/merged-sealed" .p1norm.md || r3_event "$PD" "-" sealed_merge_failed; }

# 9. transcripts, metrics, audit
r3_py capture-sessions --pkgdir "$PD" >/dev/null 2>"$PD/reviews/capture.err"
r3_py metrics --pkgdir "$PD" || INVALID="${INVALID:+$INVALID; }metrics failed"
r3_py audit --pkgdir "$PD"; ARC=$?
# 10. release the sandbox marker
rm -f "$SB/$PKG/active/$RUN_ID"
VALID=true; [ -n "$INVALID" ] && VALID=false
jq --argjson v $VALID --arg why "$INVALID" --argjson slo $SLO --argjson arc $ARC \
  '.valid=$v | .invalid_reason=(if $why=="" then null else $why end) | .slo_breach=$slo | .audit_violation=($arc==8)' "$PD/pkg.json" > "$PD/pkg.json.tmp" && mv "$PD/pkg.json.tmp" "$PD/pkg.json"
r3_py metrics --pkgdir "$PD" >/dev/null 2>&1
r3_event "$PD" "-" package_done --argjson valid $VALID
$VALID && exit 0 || exit 3
