#!/usr/bin/env bash
# Spike SW-1: the real sweeper alone (no reviewers), ember, the three packages.
# PASS: >= 1 fact accepted by the validator on >= 2 of 3 packages, and sweeper model_ok on all 3. Rejection reasons recorded.
#   flock /tmp/collab-gateway.lock bash spikes/sw1-sweeper.sh
set -u -o pipefail
. "$(dirname "$0")/_spike.sh"
OUTD=$SPIKES/out/sw1; mkdir -p "$OUTD"
K=${SW1_K:-2}; ID=sw1-$(rand_hex)
for PKG in $(jq -r '.packages[]' "$PANELS"); do
  bash "$R2_HOME/bin/build-sandbox.sh" "$PKG" >/dev/null || { record SW-1 FAIL "$OUTD" "build-sandbox $PKG"; exit 1; }
  SB=$SBR/sb/$ID/$PKG; B=$SBR/board/$ID/$PKG; D=$OUTD/$PKG; mkdir -p "$D"
  make_sandbox "$SB" "$PKG"; board_init "$B" "$SB"
  T0=$(now_ms); board_conf "$B" "$SB" "$ID/$PKG" "$T0" $((T0 + 600000)) $((2 * K)) "$SBR/board/$ID/settings/$PKG"
  ( bash "$R2_HOME/bin/run-sweeper.sh" --pkgdir "$D" --sb "$SB" --board "$B" --model muse-ember-1.0 --kill-ms $((T0 + 300000)) \
      --k "$K" --settings "$SBR/board/$ID/settings/$PKG/sw-1.json" > "$D/launcher.log" 2>&1 ) &
done
wait
OK=0; MOKN=0; N=0
for PKG in $(jq -r '.packages[]' "$PANELS"); do
  D=$OUTD/$PKG; B=$SBR/board/$ID/$PKG; cp -a "$B" "$D/board"; N=$((N + 1))
  ACC=$(grep -c . "$B/msgs/board.jsonl" || true); ACC=${ACC:-0}
  REJ=$(jq -sc 'map(.reason)|group_by(.)|map({(.[0]):length})|add // {}' "$B/msgs/rejected.jsonl")
  MOK=$(jq -r .model_ok "$D/sweeper/sw-1.meta.json")
  [ "$ACC" -ge 1 ] && OK=$((OK + 1)); [ "$MOK" = true ] && MOKN=$((MOKN + 1))
  BYFROM=$(jq -sc 'group_by(.from)|map({(.[0].from):length})|add // {}' "$B/msgs/board.jsonl")
  record "SW-1[$PKG]" "$([ "$ACC" -ge 1 ] && [ "$MOK" = true ] && echo PASS || echo FAIL)" "$D" "accepted=$ACC by_from=$BYFROM rejected=$REJ model_ok=$MOK"
done
V=FAIL; [ $OK -ge 2 ] && [ $MOKN = $N ] && V=PASS
record SW-1 "$V" "$OUTD" "packages_with_fact=$OK/$N model_ok=$MOKN/$N"
[ "$V" = PASS ]
