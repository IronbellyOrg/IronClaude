#!/usr/bin/env bash
# Owner order 2026-11-14: "run each spike/smoke first"; design 5 excluded from sonnet (sl2) panels.
# Runs the Spike 4 measurement chain (and the remaining real smoke for design 1) for all five designs on three panels,
# in TWO sequential lanes (owner limit: 2 parallel). Lane A: designs 5 and 4. Lane B: designs 1, 2 and 3.
# Order inside each lane: all of el2, then hl2, then sl2. Resumable: a step with a marker in spike4-logs/done/ is skipped.
# NOFALLBACK=1 everywhere. Each design keeps its own concurrency gate; the lanes use no shared lock, so at most 2 panel launches run at once.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
C=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
R1=$C/r1-move-radar; R2=$C/r2-idle-shift-sweeper; R3=$C/r3-axis-flip-challenge; R4=$C/r4-flag-and-adjudicate; R5=$C/r5-coverage-deflection
L=$C/spike4-logs; mkdir -p "$L/done"
export NOFALLBACK=1
cd "$REPO" || exit 2

step() { # step <id> <command...>: logs to $L/<id>.log, marks done on rc 0
  local id=$1; shift
  [ -e "$L/done/$id" ] && { echo "SKIP $id"; return 0; }
  echo "START $id $(date -u +%T)"
  ( "$@" ) >"$L/$id.log" 2>&1; local rc=$?
  echo "END $id rc=$rc $(date -u +%T)"
  [ $rc = 0 ] && touch "$L/done/$id"
  return $rc
}

d1() { local P=$1  # design 1 Move Radar
  step r1-gate0-pre-$P bash $R1/spikes/gate0-check.sh
  step r1-s4-$P bash $R1/spikes/spike4.sh $P || return 1
  if [ "$P" = el2 ]; then
    step r1-gate0a bash $R1/spikes/gate0-check.sh
    step r1-smoke-c1 env PANEL_COLLAB=1 bash $R1/tools/launch.sh el2 0 TASK-WF-designSpec-20261107-075614 || return 1
    step r1-s3 bash $R1/spikes/smoke/s3-record.sh
    step r1-gate0b bash $R1/spikes/gate0-check.sh
  fi; }
d2() { local P=$1; step r2-s4-$P bash $R2/spikes/spike4-values.sh "${P^^}"; }
d3() { local P=$1
  step r3-s4-$P bash -c '
    cd '"$R3"'; ids=()
    for i in 1 2 3; do
      out=$(env R3_SPIKE4=1 PANEL_COLLAB=0 bash bin/launch-panel.sh '"$P"' --tag spike4-$i 2>&1); echo "$out"
      rid=$(echo "$out" | grep -o "run_id=[^ ]*" | tail -1 | cut -d= -f2); [ -n "$rid" ] || { echo "no run_id for spike4-$i"; exit 1; }
      ids+=("$rid")
    done
    source lib/common.sh; r3_py values-freeze --panel '"$P"' --runs "${ids[@]}"'; }
d4() { local P=$1 PU=${1^^}
  step r4-s4-$P bash -c '
    R4='"$R4"'; REPO='"$REPO"'; PU='"$PU"'; P='"$P"'
    a1=(); for i in 1 2 3 4; do
      PANEL_COLLAB=0 bash $R4/bin/run-panel.sh --panel $PU --row s4-a1-$P-$i --values $R4/values/planning-$PU.json --no-judge --block s4 || echo "a1 row $i rc=$?"
      a1+=($R4/runs/s4-a1-$P-$i); done
    uv run --frozen --project $REPO python $R4/lib/values.py build --panel $PU --runs "${a1[@]}" || exit 1
    uv run --frozen --project $REPO python $R4/lib/values.py srun --panel $PU || exit 1
    sr=(); for i in 1 2; do
      PANEL_COLLAB=1 bash $R4/bin/run-panel.sh --panel $PU --row s4-sr-$P-$i --values $R4/values/$PU-srun.json --no-judge --block s4 || echo "srun row $i rc=$?"
      sr+=($R4/runs/s4-sr-$P-$i); done
    uv run --frozen --project $REPO python $R4/lib/values.py slowdown --panel $PU --a1 "${a1[@]}" --srun "${sr[@]}"'; }
d5() { local P=$1; step r5-s4-$P bash $R5/spikes/spike4.sh $P; }  # design 5 never runs on sl2 (owner order)

laneA() { for P in el2 hl2 sl2; do [ "$P" != sl2 ] && d5 $P; d4 $P; echo "LANE A $P DONE $(date -u +%T)"; done; echo "LANE A ALLDONE"; }
laneB() { for P in el2 hl2 sl2; do d1 $P; d2 $P; d3 $P; echo "LANE B $P DONE $(date -u +%T)"; done; echo "LANE B ALLDONE"; }

echo "START $(date -u +%T)"
if [ "${RERUN_R4_HL2_SL2:-}" = 1 ]; then  # rerun of design 4's haiku and sonnet spikes after the /proc uuid fault (2026-11-14): one per lane
  { d4 hl2; echo "LANE A R4 hl2 DONE"; } > "$L/laneA-r4rerun.log" 2>&1 &
  { d4 sl2; echo "LANE B R4 sl2 DONE"; } > "$L/laneB-r4rerun.log" 2>&1 &
else
laneA > "$L/laneA.log" 2>&1 &
laneB > "$L/laneB.log" 2>&1 &
fi
wait
echo "ALLDONE $(date -u +%T)"
