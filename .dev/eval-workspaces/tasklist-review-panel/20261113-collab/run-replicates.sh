#!/usr/bin/env bash
# Owner approval 2026-11-14 ("approve replicates"): 5 more collaboration rows and 5 more baseline rows for design 1 (Move Radar) and
# design 4 (Flag-and-Adjudicate) on the ember panel (el2), all three packages each, judged blind. Same commands as run-counted.sh.
# Starts only after run-counted.sh has ended, so the owner's limit of 2 parallel lanes holds. Lane A = design 4, lane B = design 1.
# Rows: design 1 collab el2-c1x-r2..r6, baseline el2-c0-r5..r9 (r0..r4 already exist); design 4 collab tce-f7-el2-r02..r06, baseline a1-el2-r02..r06.
# Resumable: a step with a marker in replicate-logs/done/ is skipped. A failed row is logged and the lane continues. NOFALLBACK=1.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
C=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
R1=$C/r1-move-radar; R4=$C/r4-flag-and-adjudicate
L=$C/replicate-logs; mkdir -p "$L/done"
export NOFALLBACK=1
cd "$REPO" || exit 2

while pgrep -f 'bash run-counted.sh' >/dev/null; do sleep 60; done
echo "START $(date -u +%T)"

step() {
  local id=$1; shift
  [ -e "$L/done/$id" ] && { echo "SKIP $id"; return 0; }
  echo "START $id $(date -u +%T)"
  ( "$@" ) >"$L/$id.log" 2>&1; local rc=$?
  echo "END $id rc=$rc $(date -u +%T)"
  [ $rc = 0 ] && touch "$L/done/$id"
  return 0
}

laneA() { for n in 02 03 04 05 06; do
  step r4-el2-collab-r$n env TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash $R4/bin/run-panel.sh --panel EL2 --row tce-f7-el2-r$n --values $R4/values/EL2.json --block tce-b$n
  step r4-el2-base-r$n   env PANEL_COLLAB=0 bash $R4/bin/run-panel.sh --panel EL2 --row a1-el2-r$n --values $R4/values/EL2.json --block tce-b$n
  done; echo "LANE A ALLDONE"; }
laneB() { for n in 2 3 4 5 6; do
  step r1-el2-collab-r$n env TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash $R1/tools/launch.sh el2 $n
  step r1-el2-base-r$((n+3)) env PANEL_COLLAB=0 bash $R1/tools/launch.sh el2 $((n+3))
  done; echo "LANE B ALLDONE"; }

laneA > "$L/laneA.log" 2>&1 &
laneB > "$L/laneB.log" 2>&1 &
wait
echo "ALLDONE $(date -u +%T)"
