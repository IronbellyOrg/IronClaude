#!/usr/bin/env bash
# Spike 4 (DESIGN 6.3; R-30): A1 and A2 measurement launches for one panel, then `r5.timing spike4` writes the values files.
# usage: spike4.sh <panel>
# env: A1_RUNS (default 4), A2_RUNS (default 2), PKGS (comma list, default all three), ROW_PREFIX (default s4),
#      NOFALLBACK=1, R5_CONFIG (where the values files are written; default R5/config). Each launch holds the gateway lock.
set -u -o pipefail
PANEL=$1
R5=$(cd "$(dirname "$0")/.." && pwd); REPO=$(git -C "$R5" rev-parse --show-toplevel); NOTES=$R5/spikes/NOTES.md
[ "${NOFALLBACK:-}" = 1 ] || { echo "NOFALLBACK=1 required" >&2; exit 2; }
P=${ROW_PREFIX:-s4}; A1=${A1_RUNS:-4}; A2=${A2_RUNS:-2}
mkdir -p /tmp/collab-r5  # launch logs go here; /tmp can be cleared between sessions
PK=(); [ -n "${PKGS:-}" ] && PK=(--pkgs "$PKGS")
A1ROWS=(); A2ROWS=(); LOG=""
for i in $(seq 1 "$A1"); do
  row=$P-a1-$PANEL-r$i; A1ROWS+=("$row")
  SPIKE4=1 PANEL_COLLAB=0 PANEL_KIT=0 flock /tmp/collab-gateway.lock bash "$R5/bin/launch.sh" "$PANEL" "$row" "${PK[@]}" > "/tmp/collab-r5/$row.out" 2>&1
  LOG+="- $row: launch exit $?"$'\n'
done
for i in $(seq 1 "$A2"); do
  row=$P-a2-$PANEL-r$i; A2ROWS+=("$row")
  SPIKE4=1 PANEL_COLLAB=0 PANEL_KIT=1 flock /tmp/collab-gateway.lock bash "$R5/bin/launch.sh" "$PANEL" "$row" "${PK[@]}" > "/tmp/collab-r5/$row.out" 2>&1
  LOG+="- $row: launch exit $?"$'\n'
done
VALS=$(cd "$REPO" && PYTHONPATH="$R5/lib" uv run --no-sync python -m r5.timing spike4 --panel "$PANEL" \
  --rows "$(IFS=,; echo "${A1ROWS[*]}")" --kit-rows "$(IFS=,; echo "${A2ROWS[*]}")" 2>&1); RC=$?
ST=PASS; [ $RC = 0 ] || ST=FAIL
{ echo; echo "## Spike 4 $PANEL (prefix $P, A1 x$A1, A2 x$A2, packages ${PKGS:-all}): $ST ($(date -u +%Y-%m-%dT%H:%M:%SZ))"; echo
  echo "Command: \`ROW_PREFIX=$P A1_RUNS=$A1 A2_RUNS=$A2 PKGS=${PKGS:-} bash spikes/spike4.sh $PANEL\` (NOFALLBACK=1). Values written under \`${R5_CONFIG:-$R5/config}/values/$PANEL/\`."; echo
  printf '%s' "$LOG"; echo '```'; echo "$VALS"; echo '```'; } >> "$NOTES"
echo "$VALS"
exit $RC
