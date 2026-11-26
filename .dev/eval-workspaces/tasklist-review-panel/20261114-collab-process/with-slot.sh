#!/usr/bin/env bash
# One slot of two for every claude launch of both sessions (PROCESS.md M2). Usage: with-slot.sh <label> <command> [args...]
# Waits up to SLOT_WAIT_S (default 7200) for slot.1 or slot.2 under /tmp/panel-slots, holds it while the command runs, then releases.
# The holder label and start time are written into the slot file so `with-slot.sh --status` shows who holds what.
# A session that started before the lock existed counts as one slot but is not enforced; its owner says so in PROCESS.md.
set -u -o pipefail
D=${PANEL_SLOTS_DIR:-/tmp/panel-slots}; mkdir -p "$D"
if [ "${1:-}" = --status ]; then
  for n in 1 2; do
    if flock -n "$D/slot.$n" true 2>/dev/null; then echo "slot.$n free"; else echo "slot.$n held: $(cat "$D/slot.$n.holder" 2>/dev/null)"; fi
  done; exit 0
fi
[ $# -ge 2 ] || { echo "usage: with-slot.sh <label> <command> [args...]  |  --status" >&2; exit 2; }
LABEL=$1; shift
WAIT=${SLOT_WAIT_S:-7200}; END=$(( $(date +%s) + WAIT ))
while :; do
  for n in 1 2; do
    exec 9>"$D/slot.$n"
    if flock -n 9; then
      echo "$LABEL pid=$$ since=$(date -u +%FT%TZ)" > "$D/slot.$n.holder"
      "$@"; rc=$?
      rm -f "$D/slot.$n.holder"; exit $rc
    fi
    exec 9>&-
  done
  [ "$(date +%s)" -lt "$END" ] || { echo "with-slot: no slot within ${WAIT}s" >&2; exit 75; }
  sleep 5
done
