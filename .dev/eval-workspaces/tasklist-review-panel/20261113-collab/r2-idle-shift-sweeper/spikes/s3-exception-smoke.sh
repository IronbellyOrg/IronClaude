#!/usr/bin/env bash
# One real smoke row with the owner-authorised time-cap exception ON (OVERRIDE.md): EL2 collaboration arm, control package,
# frozen config/values-exception/ values (no planning values), judged. Then the 6.4-style checks (s3_exception_check.py).
#   flock /tmp/collab-gateway.lock bash spikes/s3-exception-smoke.sh [panel=EL2] [row=smoke-el2-exc-collab]
set -u -o pipefail
. "$(dirname "$0")/_spike.sh"
P=${1:-EL2}; ROW=${2:-smoke-$(tr A-Z a-z <<<"$P")-exc-collab}
OUTD=$SPIKES/out/s3-exception; mkdir -p "$OUTD"
PKG=TASK-WF-design-20261108-041415
STAMP=$OUTD/stamp; [ -f "$STAMP" ] || touch "$STAMP"   # nothing under src/ or EVAL may be newer than this afterwards
( cd "$REPO" && NOFALLBACK=1 PANEL_COLLAB=1 TIME_CAP_EXCEPTION=1 bash "$R2_HOME/bin/launch-panel.sh" --panel "$P" --row "$ROW" \
    --packages "$PKG" ) > "$OUTD/$ROW.log" 2>&1
echo "$?" > "$OUTD/$ROW.rc"
echo "$ROW exit $(cat "$OUTD/$ROW.rc")"
$PY "$SPIKES/s3_exception_check.py" --stamp "$STAMP" --row "$ROW" --out "$OUTD/check-$ROW.json"
V=$(jq -r 'if .all_pass then "PASS" else "FAIL" end' "$OUTD/check-$ROW.json")
record "S3-EXC" "$V" "$OUTD/check-$ROW.json" "$(jq -r '[.acs|to_entries[]|"\(.key)=\(.value.pass)"]|join(" ")' "$OUTD/check-$ROW.json")"
[ "$V" = PASS ]
