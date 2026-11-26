#!/usr/bin/env bash
# Owner order 2026-11-14: wait for run-replicates.sh to finish, then rerun the three packages whose reviewer sessions hung (exit 124, 0 tokens).
# Replaces run-reruns.sh, which was a no-op: R1's results.py refuses a row already in results.jsonl, and R2 skips a package that has a DONE marker.
# Nothing is deleted: old rows, files and package folders are moved aside with an .incomplete-<stamp> name.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
C=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
R1=$C/r1-move-radar; R2=$C/r2-idle-shift-sweeper; L=$C/counted-logs; mkdir -p "$L"
S=$(date -u +%Y%m%dT%H%M%SZ)
export NOFALLBACK=1 R1 R2 L S
cd "$REPO" || exit 2
echo "WAIT $(date -u +%T)"; while pgrep -f 'bash run-replicates.sh' >/dev/null || pgrep -f 'run-counted.sh' >/dev/null; do sleep 30; done; echo "GO $(date -u +%T)"
# R1: take the two hung rows out of results.jsonl (kept in a side file), and move aside the hung package folder so the launcher reruns it
for row in hl2-c0-r4 sl2-c0-r4; do
  jq -c --arg r "$row" 'select(.row==$r)' "$R1/results/results.jsonl" >> "$R1/results/results.jsonl.removed-$S"
  jq -c --arg r "$row" 'select(.row!=$r)' "$R1/results/results.jsonl" > "$R1/results/results.jsonl.new-$S" && mv "$R1/results/results.jsonl.new-$S" "$R1/results/results.jsonl"
  [ -e "$R1/results/$row.json" ] && mv "$R1/results/$row.json" "$R1/results/$row.json.incomplete-$S"
done
# R2: move the hung designSpec package aside so DONE no longer makes the launcher skip it
D=$R2/runs/f4-hl2-exc-r1/TASK-WF-designSpec-20261107-075614
[ -e "$D" ] && mv "$D" "$D.incomplete-$S"
job() {
  case "$1" in
    r1-hl2-base) env PANEL_COLLAB=0 bash $R1/tools/launch.sh hl2 4 ;;
    r1-sl2-base) env PANEL_COLLAB=0 bash $R1/tools/launch.sh sl2 4 ;;
    r2-hl2-collab) env TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash $R2/bin/launch-panel.sh --panel HL2 --row f4-hl2-exc-r1 ;;
  esac
}
run() { local id=$1; echo "START $id $(date -u +%T)"; job "$id" > "$L/rerun2-$id.log" 2>&1; echo "END $id rc=$? $(date -u +%T)"; }
export -f job run
printf '%s\n' r1-hl2-base r1-sl2-base r2-hl2-collab | xargs -P 2 -I{} bash -c 'run {}'
echo ALLDONE
