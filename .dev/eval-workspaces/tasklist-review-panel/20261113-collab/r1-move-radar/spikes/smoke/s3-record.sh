#!/usr/bin/env bash
# s3-record.sh [--root R1] [--out FILE]   (Gate 0, S3; DESIGN.md 6.3 and 6.4)
# Decides the seven smoke conditions of 6.4 for BOTH one-package smoke rows (el2-c1-r0 and el2-c0-r0, package DS) with smokecheck.sh and
# writes spikes/s3.json = {"pass":bool,"checked_utc",...} that gate0-check.sh reads. Refuses (exit 1, writes nothing) when either row
# is missing, so S3 stays "missing" until the real collab-1 smoke has run: PANEL_COLLAB=1 bash tools/launch.sh el2 0 <DS>.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); R1=$(dirname "$(dirname "$HERE")"); OUT=""
while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --out) OUT=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
[ -n "$OUT" ] || OUT=$R1/spikes/s3.json
DS=TASK-WF-designSpec-20261107-075614
for row in el2-c1-r0 el2-c0-r0; do
  [ -f "$R1/runs/$row/$DS/status" ] || { echo "S3 missing: no smoke row $row under $R1/runs" >&2; exit 1; }
done
C1=$(bash "$HERE/smokecheck.sh" "$R1" el2-c1-r0 1); C0=$(bash "$HERE/smokecheck.sh" "$R1" el2-c0-r0 0)
PASS=true; for o in "$C1" "$C0"; do grep -qP '^[1-7]\tfalse\t' <<<"$o" && PASS=false; [ "$(grep -cP '^[1-7]\ttrue\t' <<<"$o")" = 7 ] || PASS=false; done
jq -n -c --argjson pass $PASS --arg t "$(date -u +%FT%TZ)" --arg c1 "$C1" --arg c0 "$C0" '{pass:$pass, checked_utc:$t, collab1:$c1, collab0:$c0}' > "$OUT"
jq -c '{pass,checked_utc}' "$OUT"
