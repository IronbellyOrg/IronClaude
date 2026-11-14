#!/usr/bin/env bash
# One panel on one package (DESIGN 2.2 timeline).
# run-package.sh --row <row> --runid <hex> --pkg <pkg> --panel <EL2|SL2|HL2> --values <file> --collab <0|1> [--sweeper-model <m>]
# The switch comes in as --collab from launch-panel.sh; this script never reads PANEL_COLLAB.
set -u -o pipefail
. "$(dirname "$0")/lib/common.sh"
ROW="" RUNID="" PKG="" PANEL="" VALUES="" COLLAB="" SWM=""
while [ $# -gt 0 ]; do case "$1" in
  --row) ROW=$2;; --runid) RUNID=$2;; --pkg) PKG=$2;; --panel) PANEL=$2;; --values) VALUES=$2;;
  --collab) COLLAB=$2;; --sweeper-model) SWM=$2;; *) echo "unknown arg $1" >&2; exit 2;; esac; shift 2; done
case "$COLLAB" in 0|1) ;; *) echo "--collab must be 0 or 1" >&2; exit 2;; esac
PKGDIR=$OUT/runs/$ROW/$PKG; SB=$SBR/sb/$RUNID/$PKG; B=$SBR/board/$RUNID/$PKG; SET=$SBR/board/$RUNID/settings/$PKG
mkdir -p "$PKGDIR/reviews" "$PKGDIR/sweeper"
cp "$VALUES" "$PKGDIR/values.json"
V() { jq -r ".$1" "$PKGDIR/values.json"; }
[ -n "$SWM" ] || SWM=$(jq -r --arg p "$PANEL" '.[$p].sweeper.model' "$PANELS")

# 1. per-run sandbox (D-6)
make_sandbox "$SB" "$PKG" || { echo "sandbox build failed" >&2; exit 1; }
echo "$SB/repo" > "$PKGDIR/sandbox"
jq -n --arg c "$(sha256sum "$SB/cand/candidate.md" | cut -d' ' -f1)" --arg s "$(sha256sum "$SB/cand/source.md" | cut -d' ' -f1)" \
  --arg sb "$SB" --arg panel "$PANEL" --argjson collab "$COLLAB" --arg vsha "$(sha256sum "$VALUES" | cut -d' ' -f1)" \
  '{candidate_sha256:$c,source_sha256:$s,sandbox:$sb,panel:$panel,panel_collab:$collab,values_sha256:$vsha}' > "$PKGDIR/inputs.json"

K=$(V k); FIN_S=$(V panel_finish_at_s); KILL_S=$(V sweeper_kill_s); HANG_S=$(V hang_s)
TURN_RECV=$(V turn_p90_recv); TURN_CRIT=$(V turn_p90_crit); CRIT=$(jq -r --arg p "$PANEL" '.[$p].critical_role' "$PANELS")
DEAL_R=$(( 16#$(printf '%s' "$RUNID/$PKG/deal" | sha256sum | cut -c1-2) % 2 ))
echo "$DEAL_R" > "$PKGDIR/deal_r"
ms_of() { awk -v t0="$1" -v s="$2" 'BEGIN{printf "%d", t0 + s * 1000}'; }

[ "$COLLAB" = 1 ] && board_init "$B" "$SB"

# 2. T0
T0=$(now_ms); echo "$T0" > "$PKGDIR/t0"
FIN_MS=$(ms_of "$T0" "$FIN_S"); KILL_MS=$(ms_of "$T0" "$KILL_S"); DEADLINE=$(ms_of "$T0" "$HANG_S")

[ "$COLLAB" = 1 ] && board_conf "$B" "$SB" "$RUNID/$PKG" "$T0" "$FIN_MS" $((2 * K)) "$SET"

# 3. reviewers, all at once
declare -A PID
while IFS=$'\t' read -r rid model role ri; do
  args=(--pkgdir "$PKGDIR" --sb "$SB" --pkg "$PKG" --rid "$rid" --model "$model" --deadline-ms "$DEADLINE")
  if [ "$role" = receiver ]; then t=$TURN_RECV; elif [ "$model" = "$CRIT" ]; then t=$TURN_CRIT
  else t=$(jq -r --arg m "$model" '.planning_turn_p90[$m] // 6.4' "$PANELS"); fi
  args+=(--turn-p90 "$t")
  if [ "$COLLAB" = 1 ] && [ "$role" = receiver ]; then
    bash "$R2_HOME/bin/make-settings.sh" receiver --board "$B" --rid "$rid" --recv-index "$ri" --t0-ms "$T0" \
      --finish-ms "$FIN_MS" --k "$K" --deal-r "$DEAL_R" --out "$SET/$rid.json"
    args+=(--settings "$SET/$rid.json")
  fi
  bash "$R2_HOME/bin/run-reviewer2.sh" "${args[@]}" > "$PKGDIR/reviews/$rid.launcher.log" 2>&1 &
  PID[$rid]=$!
done < <(jq -r --arg p "$PANEL" '.[$p].reviewers[]|[.rid,.model,.role,(.recv_index // "")]|@tsv' "$PANELS")

# 4. sweeper
sweeper() {
  local start
  start=$(jq -r --arg p "$PANEL" '.[$p].sweeper.start' "$PANELS")
  if [[ $start == after:* ]]; then
    local after=${start#after:}
    while [ ! -e "$PKGDIR/reviews/$after.attempt1.exit" ]; do
      kill -0 "${PID[$after]}" 2>/dev/null || [ -e "$PKGDIR/reviews/$after.attempt1.exit" ] || break
      sleep 0.5
    done
    # the non-receiver's own Reads join the harvest filter before the sweeper starts
    jq -r '.[]|select(.type=="assistant")|.message.content[]?|select(.type=="tool_use" and .name=="Read")|.input.file_path' \
      "$PKGDIR/reviews/$after.attempt1.json" 2>/dev/null | sed "s|^$SB/repo/||" >> "$B/state/opened.txt" || true
  fi
  jq -n --argjson t "$(now_ms)" '{sweeper_start_t:$t}' > "$PKGDIR/sweeper/start.json"
  bash "$R2_HOME/bin/run-sweeper.sh" --pkgdir "$PKGDIR" --sb "$SB" --board "$B" --model "$SWM" --kill-ms "$KILL_MS" \
    --k "$K" --settings "$SET/sw-1.json" > "$PKGDIR/sweeper/launcher.log" 2>&1
}
SWPID=""
if [ "$COLLAB" = 1 ]; then sweeper & SWPID=$!; fi

# 5. wait
INVALID=()
for rid in "${!PID[@]}"; do wait "${PID[$rid]}" || INVALID+=("reviewer $rid invalid (model or findings block)"); done
[ -n "$SWPID" ] && wait "$SWPID"
if [ "$COLLAB" = 1 ] && [ "$(jq -r .model_ok "$PKGDIR/sweeper/sw-1.meta.json" 2>/dev/null)" = false ]; then
  INVALID+=("sweeper model_ok false (observed $(jq -r .observed_model "$PKGDIR/sweeper/sw-1.meta.json"))")
fi
END=$(jq -s '[.[].end_ms // 0]|max' "$PKGDIR"/reviews/*.meta.json "$PKGDIR"/sweeper/sw-1.meta.json 2>/dev/null)
[ -n "$END" ] && [ "$END" != null ] && [ "$END" != 0 ] || END=$(now_ms)
awk -v e="$END" -v t="$T0" 'BEGIN{printf "%.3f\n", (e-t)/1000}' > "$PKGDIR/elapsed_s"

# 6. board copy, tags, audits, metrics
[ "$COLLAB" = 1 ] && cp -a "$B" "$PKGDIR/board"
while IFS=$'\t' read -r rid role; do
  targs=(--report "$PKGDIR/reviews/$rid.norm.md" --rid "$rid" --out "$PKGDIR/reviews/$rid.final.md")
  [ "$COLLAB" = 1 ] && targs+=(--board-dir "$PKGDIR/board")
  [ "$role" = receiver ] || targs+=(--nonreceiver)
  [ "$(jq -r .attempt "$PKGDIR/reviews/$rid.meta.json" 2>/dev/null)" = 2 ] && targs+=(--isolated)
  $PY "$R2_HOME/py/tagger.py" "${targs[@]}" > /dev/null || INVALID+=("tagger failed for $rid")
done < <(jq -r --arg p "$PANEL" '.[$p].reviewers[]|[.rid,.role]|@tsv' "$PANELS")
$PY "$R2_HOME/py/audits.py" run --pkgdir "$PKGDIR" > /dev/null || true
$PY "$R2_HOME/py/collab_metrics.py" --pkgdir "$PKGDIR" --panel "$PANEL" --values "$PKGDIR/values.json" \
  --arm "$([ "$COLLAB" = 1 ] && echo F4 || echo A1)" --row "$ROW" --pkg "$PKG" > /dev/null || INVALID+=("collab_metrics failed")
if [ ${#INVALID[@]} -gt 0 ]; then printf '%s\n' "${INVALID[@]}" > "$PKGDIR/INVALID"; fi
date -u +%Y-%m-%dT%H:%M:%SZ > "$PKGDIR/DONE"
[ ${#INVALID[@]} -eq 0 ]
