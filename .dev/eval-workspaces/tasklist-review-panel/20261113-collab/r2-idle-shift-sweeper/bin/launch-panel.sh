#!/usr/bin/env bash
# THE launch script (DESIGN 5.1): one panel on the three packages, merge, anonymise, judge, audits, results row.
# NOFALLBACK=1 [PANEL_COLLAB=1|0] [SWEEPER_MODEL=<model>] bash launch-panel.sh --panel EL2|SL2|HL2 --row <row>
#   [--packages "<pkg> ..."] [--planning-values] [--no-judge]
set -u -o pipefail
. "$(dirname "$0")/lib/common.sh"
PANEL="" ROW="" PKGS="" PLANNING=0 NOJUDGE=0
while [ $# -gt 0 ]; do case "$1" in
  --panel) PANEL=$2; shift 2;; --row) ROW=$2; shift 2;; --packages) PKGS=$2; shift 2;;
  --planning-values) PLANNING=1; shift;; --no-judge) NOJUDGE=1; shift;; *) echo "unknown arg $1" >&2; exit 2;; esac; done
# the switch is read here, once, and passed to every child as an argument
COLLAB=${PANEL_COLLAB-1}
pf() { echo "PREFLIGHT: $1" >&2; exit 2; }

# ---- step 0: preflight (refuse before any model call)
[ "${NOFALLBACK:-}" = 1 ] || pf "NOFALLBACK=1 is required"
case "$COLLAB" in 0|1) ;; *) pf "PANEL_COLLAB must be 0 or 1";; esac
[[ $ROW =~ ^[a-z0-9][a-z0-9-]{0,40}$ ]] || pf "bad --row '$ROW'"
jq -e --arg p "$PANEL" 'has($p) and ($p|IN("EL2","SL2","HL2"))' "$PANELS" >/dev/null || pf "bad --panel '$PANEL'"
[ -n "$PKGS" ] || PKGS=$(jq -r '.packages|join(" ")' "$PANELS")
SWM=${SWEEPER_MODEL:-$(jq -r --arg p "$PANEL" '.[$p].sweeper.model' "$PANELS")}
for m in $(jq -r --arg p "$PANEL" '.[$p].reviewers[].model' "$PANELS") "$SWM"; do
  jq -e --arg m "$m" '.allowed_models|index($m)' "$PANELS" >/dev/null || pf "model '$m' is not allowed"
done
for t in jq flock superclaude uv; do command -v "$t" >/dev/null || pf "$t not on PATH"; done
pin() { jq -r --arg k "$1" '.sha256[$k] // empty' "$MANIFEST"; }
chk() { [ "$(sha256sum "$2" 2>/dev/null | cut -d' ' -f1)" = "$(pin "$1")" ] || pf "sha256 of $2 differs from manifest ($1)"; }
chk judge-one.sh "$EVAL/tools/tmp-scripts/judge-one.sh"
chk catalogue.json "$CATALOGUE"
chk brief_a1 "$R2_HOME/config/brief-a1.tmpl"
chk sweeper_brief "$R2_HOME/config/sweeper-brief.tmpl"
for p in $PKGS; do
  jq -e --arg p "$p" '.packages|index($p)' "$PANELS" >/dev/null || pf "unknown package $p"
  if [ $PLANNING = 0 ]; then
    vf=$R2_HOME/config/values/$PANEL/$p.json
    [ -f "$vf" ] || pf "values file $vf missing (run Spike 4, or pass --planning-values for a smoke row)"
    chk "values/$PANEL/$p.json" "$vf"
  fi
done
mkdir -p "$SBR" "$OUT/runs" "$OUT/results/keys" "$OUT/scoring"
for p in $PKGS; do
  [ -f "$SBR/base/$p.tar" ] || bash "$R2_HOME/bin/build-sandbox.sh" "$p" >/dev/null || pf "build-sandbox failed for $p"
done
exec 8>>"$SBR/slot.1"
if ! flock -n 8; then exec 8>>"$SBR/slot.2"; flock -n 8 || pf "both concurrency slots are held"; fi

RD=$OUT/runs/$ROW
log() { mkdir -p "$RD"; echo "STEP $1 $2 $3 $(utc)" >> "$RD/launch.log"; }
if [ -d "$RD" ] && [ -f "$RD/runid" ]; then
  [ "$(cat "$RD/panel")" = "$PANEL" ] || pf "resume: panel differs from the first launch"
  [ "$(cat "$RD/panel_collab")" = "$COLLAB" ] || pf "resume: PANEL_COLLAB differs from the first launch"
  [ "$(cat "$RD/sweeper_model")" = "$SWM" ] || pf "resume: sweeper model differs from the first launch"
  [ "$([ -e "$RD/planning" ] && echo 1 || echo 0)" = $PLANNING ] || pf "resume: --planning-values differs from the first launch"
  RUNID=$(cat "$RD/runid"); OPAQUE=$(cat "$RD/opaque")
else
  # ---- step 1: first launch only
  mkdir -p "$RD"
  RUNID=$(od -An -N4 -tx1 /dev/urandom | tr -d ' \n'); OPAQUE=$(od -An -N6 -tx1 /dev/urandom | tr -d ' \n')
  echo "$RUNID" > "$RD/runid"; echo "$OPAQUE" > "$RD/opaque"; echo "$PANEL" > "$RD/panel"
  echo "$COLLAB" > "$RD/panel_collab"; echo "$SWM" > "$RD/sweeper_model"; utc > "$RD/started_at"
  [ $PLANNING = 1 ] && : > "$RD/planning"
  jq -n --arg row "$ROW" --arg runid "$RUNID" --arg arm "$([ "$COLLAB" = 1 ] && echo F4 || echo A1)" \
    '{row:$row,runid:$runid,arm:$arm}' > "$OUT/results/keys/$OPAQUE.json"
fi
log 1 - OK

values_for() {
  if [ $PLANNING = 1 ]; then
    jq --arg p "$1" --arg panel "$PANEL" '.[$panel] + {pkg:$p, source:"planning"}' "$R2_HOME/config/planning-values.json" > "$RD/values-$1.json"
    echo "$RD/values-$1.json"
  else echo "$R2_HOME/config/values/$PANEL/$1.json"; fi
}
quarantine() { local s; s=$(date -u +%Y%m%dT%H%M%SZ); for d in "$@"; do [ -e "$d" ] && mv "$d" "$d.incomplete-$s"; done; return 0; }

# ---- step 2: run each package
for p in $PKGS; do
  PD=$RD/$p
  if [ -e "$PD/DONE" ]; then log 2 "$p" "OK skipped-done"; continue; fi
  quarantine "$PD" "$SBR/sb/$RUNID/$p" "$SBR/board/$RUNID/$p" "$SBR/board/$RUNID/settings/$p"
  if bash "$R2_HOME/bin/run-package.sh" --row "$ROW" --runid "$RUNID" --pkg "$p" --panel "$PANEL" \
       --values "$(values_for "$p")" --collab "$COLLAB" --sweeper-model "$SWM"; then log 2 "$p" OK
  else log 2 "$p" "FAIL invalid"; fi
done

# ---- step 3: merge (merge-b11.sh:17-34 arguments)
for p in $PKGS; do
  PD=$RD/$p
  [ -e "$PD/DONE" ] && [ ! -e "$PD/INVALID" ] || { log 3 "$p" "FAIL invalid-package"; continue; }
  [ -e "$PD/merged-1.md" ] && { log 3 "$p" "OK skipped-merged"; continue; }
  REV=$(jq -c --arg p "$PANEL" '. as $c | [.[$p].reviewers[] | {reviewer_id:.rid, model:.model, alias:$c.merge.alias[.rid],
      tier:$c.merge.tier[.rid], strategy:"fixed", stand_in:false, fallback_depth:0, fallbacks:[], launch:null, seed:null,
      slot_id:(.rid|split("-")[0])}]' "$PANELS")
  jq -c --argjson rev "$REV" '.reviewers=$rev' "$EVAL/$p/resolution-live7.json" > "$PD/resolution.json"
  ARGS=()
  for rid in $(jq -r --arg p "$PANEL" '.[$p].reviewers[].rid' "$PANELS"); do ARGS+=(--report "$rid=$PD/reviews/$rid.final.md"); done
  if superclaude review merge --ledger "$PD/ledger.json" --doc "$EVAL/$p/candidate.md" --round 1 "${ARGS[@]}" \
       --resolution "$PD/resolution.json" --out "$PD/merged-1.md" > "$PD/merge-stdout.txt" 2>&1 && [ -s "$PD/merged-1.md" ]; then
    LR=$(jq '.rows|length' "$PD/ledger.json" 2>/dev/null || echo 0)
    jq --argjson n "$LR" '.ledger_rows=$n' "$PD/collab.json" > "$PD/collab.json.tmp" && mv "$PD/collab.json.tmp" "$PD/collab.json"
    log 3 "$p" OK
  else
    rm -f "$PD/merged-1.md"; echo "merge refused" >> "$PD/INVALID"; log 3 "$p" "FAIL merge-refused"
  fi
done

# ---- step 4: anonymise
label_of() { for l in Q R S T U V; do [ -f "$OUT/scoring/$OPAQUE/$1/$l/merged-anon.md" ] && echo "$l"; done | tail -n1; }
for p in $PKGS; do
  PD=$RD/$p
  [ -e "$PD/merged-1.md" ] || continue
  if [ -n "$(label_of "$p")" ] && [ -f "$OUT/scoring/$OPAQUE/$p/label-key.json" ]; then log 4 "$p" "OK skipped-labelled"; continue; fi
  if L=$(bash "$R2_HOME/bin/anon.sh" --merged "$PD/merged-1.md" --out-dir "$OUT/scoring/$OPAQUE/$p" --row "$ROW" --runid "$RUNID" 2>"$PD/anon.err"); then
    log 4 "$p" "OK $L"
  else
    rc=$?; for l in Q R S T U V; do [ -f "$OUT/scoring/$OPAQUE/$p/$l/merged-anon.md" ] && mv "$OUT/scoring/$OPAQUE/$p/$l" "$OUT/scoring/$OPAQUE/$p/$l.anon-leak-$(date -u +%Y%m%dT%H%M%SZ)"; done
    echo "anonymiser exit $rc" >> "$PD/INVALID"; log 4 "$p" "FAIL anon-exit-$rc"
  fi
done

# ---- step 5: judge, the packages in parallel, one retry, never a guessed score
if [ $NOJUDGE = 0 ]; then
  declare -A JP
  for p in $PKGS; do
    L=$(jq -r '.label // empty' "$OUT/scoring/$OPAQUE/$p/label-key.json" 2>/dev/null)
    [ -n "$L" ] && [ -f "$OUT/scoring/$OPAQUE/$p/$L/merged-anon.md" ] || continue
    [ -f "$OUT/scoring/$OPAQUE/$p/$L/score.json" ] && { log 5 "$p" "OK skipped-scored"; continue; }
    ( bash "$R2_HOME/bin/judge.sh" "$OPAQUE" "$p" "$L" || { [ $? = 5 ] && exit 5; bash "$R2_HOME/bin/judge.sh" "$OPAQUE" "$p" "$L"; } ) \
      > "$RD/$p/judge.log" 2>&1 &
    JP[$p]=$!
  done
  for p in "${!JP[@]}"; do
    if wait "${JP[$p]}"; then log 5 "$p" OK; else log 5 "$p" "FAIL judge"; fi
  done
fi

# ---- step 6: audits (contamination incl. ground-truth substrings, read-only)
for p in $PKGS; do
  PD=$RD/$p
  [ -e "$PD/inputs.json" ] || continue
  if $PY "$R2_HOME/py/audits.py" run --pkgdir "$PD" --gt "$EVAL/$p/ground-truth.json" > "$PD/audit-stdout.txt"; then log 6 "$p" OK
  else log 6 "$p" "FAIL audit"; fi
  AOK=$(jq '.ok' "$PD/audit.json")
  [ -f "$PD/collab.json" ] && jq --argjson a "$AOK" '.audit_ok=$a' "$PD/collab.json" > "$PD/collab.json.tmp" && mv "$PD/collab.json.tmp" "$PD/collab.json"
done

# ---- step 7: results row
utc > "$RD/finished_at"
$PY "$R2_HOME/py/results_row.py" --row "$ROW" --opaque "$OPAQUE" --out "$OUT/results/$ROW.json" > /dev/null && log 7 - OK || log 7 - FAIL

# ---- step 8: exit status
INV=$(jq -r '.invalid|length' "$OUT/results/$ROW.json" 2>/dev/null || echo 1)
if [ $NOJUDGE = 1 ]; then INV=$(jq -r '[.invalid[]|select(test("unscored")|not)]|length' "$OUT/results/$ROW.json" 2>/dev/null || echo 1); fi
NPK=$(wc -w <<<"$PKGS")
DONE_N=$(jq -r '[.per_package[]|select(.valid and .audit_ok)]|length' "$OUT/results/$ROW.json" 2>/dev/null || echo 0)
echo "row $ROW: results $OUT/results/$ROW.json invalid=$INV valid_packages=$DONE_N/$NPK"
[ "$INV" = 0 ] && [ "$DONE_N" = "$NPK" ]
