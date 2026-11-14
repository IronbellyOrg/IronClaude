#!/usr/bin/env bash
# Spike 4: n A1 runs (PANEL_COLLAB=0, hang guard 3000 s via config/spike4-values.json) of one panel on the three
# packages, then values.py reduce per package -> config/values/<panel>/<pkg>.json, then re-pin manifest.json (R-30).
# Rows are stamped planning so summarize_arm.py never counts them. No merge, anonymise or judge.
#   flock /tmp/collab-gateway.lock bash spikes/spike4-values.sh <EL2|SL2|HL2> [n=4]
set -u -o pipefail
. "$(dirname "$0")/_spike.sh"
PANEL=$1; N=${2:-4}
OUTD=$SPIKES/out/spike4/$PANEL; mkdir -p "$OUTD"
for p in $(jq -r '.packages[]' "$PANELS"); do bash "$R2_HOME/bin/build-sandbox.sh" "$p" >/dev/null || exit 1; done
for i in $(seq 1 "$N"); do
  ROW=spike4-$(tr A-Z a-z <<<"$PANEL")-r$i; RUNID=$(rand_hex)
  mkdir -p "$OUT/runs/$ROW"; : > "$OUT/runs/$ROW/planning"; echo "$RUNID" > "$OUT/runs/$ROW/runid"
  echo "$PANEL" > "$OUT/runs/$ROW/panel"; echo 0 > "$OUT/runs/$ROW/panel_collab"
  for p in $(jq -r '.packages[]' "$PANELS"); do
    [ -e "$OUT/runs/$ROW/$p/DONE" ] && continue
    bash "$R2_HOME/bin/run-package.sh" --row "$ROW" --runid "$RUNID" --pkg "$p" --panel "$PANEL" \
      --values "$R2_HOME/config/spike4-values.json" --collab 0 >> "$OUTD/run.log" 2>&1 || echo "INVALID $ROW $p" >> "$OUTD/run.log"
  done
done
V=PASS
for p in $(jq -r '.packages[]' "$PANELS"); do
  DIRS=$(for i in $(seq 1 "$N"); do d=$OUT/runs/spike4-$(tr A-Z a-z <<<"$PANEL")-r$i/$p; [ -e "$d/DONE" ] && [ ! -e "$d/INVALID" ] && echo "$d"; done)
  if [ -z "$DIRS" ] || ! $PY "$R2_HOME/py/values.py" reduce --runs $DIRS --panels "$PANELS" --pkg "$p" \
       --out "$R2_HOME/config/values/$PANEL/$p.json" > "$OUTD/$p.json"; then V=FAIL; fi
done
[ "$V" = PASS ] && $PY "$R2_HOME/py/values.py" pin --r2 "$R2_HOME" --repo "$REPO" --eval "$EVAL" --out "$MANIFEST" > /dev/null
record "Spike4[$PANEL]" "$V" "$OUTD" "n=$N values in config/values/$PANEL/"
[ "$V" = PASS ]
