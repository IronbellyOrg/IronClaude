#!/usr/bin/env bash
# Owner order 2026-11-14 ("go ahead with the fixes and reruns"): rerun the packages whose reviewer sessions hung with no output (exit 124, 0 tokens).
# Starts only after run-counted.sh has finished (so at most 2 panel launches run at once), then runs these three resumes two at a time.
# Each launcher resumes per package: the valid packages are kept, the invalid one is moved aside (never deleted) and rerun.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
C=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
R1=$C/r1-move-radar; R2=$C/r2-idle-shift-sweeper; L=$C/counted-logs; mkdir -p "$L"
export NOFALLBACK=1 R1 R2 L
cd "$REPO" || exit 2
echo "WAIT $(date -u +%T)"; while pgrep -f 'run-counted.sh' >/dev/null; do sleep 30; done; echo "GO $(date -u +%T)"
job() {
  case "$1" in
    r1-hl2-base) mv "$R1/results/hl2-c0-r4.json" "$R1/results/hl2-c0-r4.json.incomplete-20261114"; env PANEL_COLLAB=0 bash $R1/tools/launch.sh hl2 4 ;;
    r1-sl2-base) mv "$R1/results/sl2-c0-r4.json" "$R1/results/sl2-c0-r4.json.incomplete-20261114"; env PANEL_COLLAB=0 bash $R1/tools/launch.sh sl2 4 ;;
    r2-hl2-collab) env TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash $R2/bin/launch-panel.sh --panel HL2 --row f4-hl2-exc-r1 ;;
  esac
}
run() { local id=$1; echo "START $id $(date -u +%T)"; job "$id" > "$L/rerun-$id.log" 2>&1; echo "END $id rc=$? $(date -u +%T)"; }
export -f job run
printf '%s\n' r1-hl2-base r1-sl2-base r2-hl2-collab | xargs -P 2 -I{} bash -c 'run {}'
echo ALLDONE
