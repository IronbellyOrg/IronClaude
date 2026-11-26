#!/usr/bin/env bash
# Call the unchanged EVAL judge-one.sh in place for one row-package (DESIGN 5.4, decision D9).
# usage: judge.sh <token> <pkg> <label> [row]; exit = judge-one.sh exit (2 = judge sum mismatch, nothing run)
set -u -o pipefail
TOKEN=$1; PKG=$2; L=$3; ROW=${4:-}
R5=$(cd "$(dirname "$0")/.." && pwd); CFG=${R5_CONFIG:-$R5/config}; OUTR=${R5_OUT:-$R5}
EVAL=${R5_EVAL:-$(cd "$R5/../../20261111-a1" && pwd)}
PINS=${R5_PINS:-$CFG/pins.json}
J=$EVAL/tools/tmp-scripts/judge-one.sh
WANT=$(jq -r '.judge_one_sha256' "$PINS"); HAVE=$(sha256sum "$J" | cut -d' ' -f1)
[ "$WANT" = "$HAVE" ] || { echo "refused: judge-one.sh sha256 $HAVE != pinned $WANT" >&2; exit 2; }
C=$(realpath -m --relative-to="$EVAL/arms/scoring/combos" "$OUTR/scoring/$TOKEN")
D=$OUTR/scoring/$TOKEN/$PKG/$L
[ "$(realpath -m "$EVAL/arms/scoring/combos/$C")" = "$(realpath -m "$OUTR/scoring/$TOKEN")" ] || { echo "refused: combo path does not resolve to $D" >&2; exit 2; }
if [ "${DRY_RUN:-}" = 1 ]; then echo "COMBO: $C"; exit 0; fi
bash "$J" "$C" "$PKG" "$L"; RC=$?
ST=ok
if [ $RC -ne 0 ] || ! jq -e 'has("gt_covered_any") and has("gt_covered_blocking") and has("wrong_blockers") and has("ledger_rows_total") and has("ledger_rows_blocking") and has("blocking_rows_gt_matched") and has("gt_total")' "$D/score.json" >/dev/null 2>&1; then
  ST=judge_failed; [ $RC -eq 0 ] && RC=1
fi
APIERR=false; grep -q 'API Error' "$D/judge.json" 2>/dev/null && APIERR=true
if [ -n "$ROW" ]; then
  f=$OUTR/runs/$ROW/$PKG/pkg-status.json; [ -f "$f" ] || echo '{}' > "$f"
  jq --arg s "$ST" --argjson a $APIERR '.judge=$s|.judge_api_error=$a' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
fi
echo "$ST api_error=$APIERR"
exit $RC
