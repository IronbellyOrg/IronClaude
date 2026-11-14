#!/usr/bin/env bash
# Owner orders 2026-11-14: "let them all run, we can make exceptions to the 35% rule" and "run the baseline arms too".
# Counted rows: for every design and panel, one collaboration row (time-cap exception on) and one isolated baseline row with the same harness,
# each over the three packages, judged blind by Opus. Design 5 runs on el2 and hl2 only (owner order). Two sequential lanes (owner limit: 2 parallel).
# Each design keeps its own concurrency gate; no shared lock. Resumable: a step with a marker in counted-logs/done/ is skipped. NOFALLBACK=1.
# Design 2 on el2 runs as built (sweeper starts after ember): the design's own smoke row showed all facts arriving late; this is recorded, not changed.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
C=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
R1=$C/r1-move-radar; R2=$C/r2-idle-shift-sweeper; R3=$C/r3-axis-flip-challenge; R4=$C/r4-flag-and-adjudicate; R5=$C/r5-coverage-deflection
L=$C/counted-logs; mkdir -p "$L/done"
export NOFALLBACK=1
cd "$REPO" || exit 2

step() { # step <id> <command...>
  local id=$1; shift
  [ -e "$L/done/$id" ] && { echo "SKIP $id"; return 0; }
  echo "START $id $(date -u +%T)"
  ( "$@" ) >"$L/$id.log" 2>&1; local rc=$?
  echo "END $id rc=$rc $(date -u +%T)"
  [ $rc = 0 ] && touch "$L/done/$id"
  return 0   # a failed row is logged and the lane continues
}

d1() { local P=$1
  step r1-$P-collab env TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash $R1/tools/launch.sh $P 1
  step r1-$P-base   env PANEL_COLLAB=0 bash $R1/tools/launch.sh $P 4; }
d2() { local P=$1 PU=${1^^}
  step r2-$P-collab env TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash $R2/bin/launch-panel.sh --panel $PU --row f4-$P-exc-r1
  step r2-$P-base   env TIME_CAP_EXCEPTION=1 PANEL_COLLAB=0 bash $R2/bin/launch-panel.sh --panel $PU --row a1-$P-exc-r1; }
d3() { local P=$1
  step r3-$P-collab bash -c "cd $R3 && env TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash bin/launch-panel.sh $P"
  step r3-$P-base   bash -c "cd $R3 && env PANEL_COLLAB=0 bash bin/launch-panel.sh $P"; }
d4() { local P=$1 PU=${1^^}
  step r4-$P-collab env TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash $R4/bin/run-panel.sh --panel $PU --row tce-f7-$P-r01 --values $R4/values/$PU.json --block tce-b01
  step r4-$P-base   env PANEL_COLLAB=0 bash $R4/bin/run-panel.sh --panel $PU --row a1-$P-r01 --values $R4/values/$PU.json --block tce-b01; }
d5() { local P=$1  # baseline first: its summary is the reference the collaboration row's alarms read
  step r5-$P-base   env PANEL_COLLAB=0 PANEL_KIT=0 bash $R5/bin/launch.sh $P a1x-$P-r01
  step r5-$P-collab env PANEL_COLLAB=1 TIME_CAP_EXCEPTION=1 bash $R5/bin/launch.sh $P f6x-$P-r01; }

laneA() { for P in el2 hl2 sl2; do d4 $P; [ "$P" != sl2 ] && d5 $P; d3 $P; echo "LANE A $P DONE $(date -u +%T)"; done; echo "LANE A ALLDONE"; }
laneB() { for P in el2 hl2 sl2; do d1 $P; d2 $P; echo "LANE B $P DONE $(date -u +%T)"; done; echo "LANE B ALLDONE"; }

echo "START $(date -u +%T)"
laneA > "$L/laneA.log" 2>&1 &
laneB > "$L/laneB.log" 2>&1 &
wait
echo "ALLDONE $(date -u +%T)"
