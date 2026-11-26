#!/usr/bin/env bash
# S3 = the one-package smoke test (DESIGN 6.4): EL2, SL2 and HL2, each with PANEL_COLLAB=1 and 0, on the control
# package with planning values (rows stamped planning, never counted), then the AC-2..AC-10 checks (s3_check.py).
#   flock /tmp/collab-gateway.lock bash spikes/s3-smoke.sh [EL2 SL2 HL2]
set -u -o pipefail
. "$(dirname "$0")/_spike.sh"
OUTD=$SPIKES/out/s3; mkdir -p "$OUTD"
PKG=TASK-WF-design-20261108-041415
STAMP=$OUTD/stamp; [ -f "$STAMP" ] || touch "$STAMP"   # AC-2: nothing under src/ or EVAL may be newer than this
PANELS_TO_RUN=${*:-EL2 SL2 HL2}
for P in $PANELS_TO_RUN; do
  p=$(tr A-Z a-z <<<"$P")
  for C in 1 0; do
    ROW=smoke-$p-$([ $C = 1 ] && echo collab || echo iso)
    ( cd "$REPO" && NOFALLBACK=1 PANEL_COLLAB=$C bash "$R2_HOME/bin/launch-panel.sh" --panel "$P" --row "$ROW" \
        --packages "$PKG" --planning-values ) > "$OUTD/$ROW.log" 2>&1
    echo "$?" > "$OUTD/$ROW.rc"
    echo "$ROW exit $(cat "$OUTD/$ROW.rc")"
  done
done
$PY "$SPIKES/s3_check.py" --stamp "$STAMP" --out "$OUTD/check.json" --panels $PANELS_TO_RUN
V=$(jq -r 'if .all_pass then "PASS" else "FAIL" end' "$OUTD/check.json")
record S3 "$V" "$OUTD/check.json" "$(jq -r '[.acs|to_entries[]|"\(.key)=\(.value.pass)"]|join(" ")' "$OUTD/check.json")"
[ "$V" = PASS ]
