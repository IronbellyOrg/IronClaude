#!/usr/bin/env bash
# sha-checked wrapper around the unchanged EVAL judge-one.sh (D-7). judge.sh <opaque> <pkg> <label>
# exit 5: judge-one.sh sha256 differs from the manifest (nothing judged); 6: the judge dir would land outside OUT/scoring.
set -u -o pipefail
. "$(dirname "$0")/lib/common.sh"
OPAQUE=$1 PKG=$2 L=$3
J=$EVAL/tools/tmp-scripts/judge-one.sh
PIN=$(jq -r '.sha256["judge-one.sh"] // empty' "$MANIFEST")
[ -n "$PIN" ] && [ "$(sha256sum "$J" | cut -d' ' -f1)" = "$PIN" ] || { echo "judge-one.sh sha256 mismatch" >&2; exit 5; }
COMBOS=$EVAL/arms/scoring/combos
[ -d "$COMBOS" ] || { echo "missing $COMBOS" >&2; exit 6; }
C=$(realpath -m --relative-to="$COMBOS" "$OUT/scoring/$OPAQUE")
DREAL=$(realpath -m "$COMBOS/$C/$PKG/$L")
case "$DREAL" in "$(realpath -m "$OUT/scoring")"/*) ;; *) echo "judge dir $DREAL outside $OUT/scoring" >&2; exit 6;; esac
bash "$J" "$C" "$PKG" "$L"
