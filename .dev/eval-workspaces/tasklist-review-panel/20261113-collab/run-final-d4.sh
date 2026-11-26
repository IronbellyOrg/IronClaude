#!/usr/bin/env bash
# Owner approval 2026-11-14 ("approve the final batch"), part 1: 6 more design 4 (Flag-and-Adjudicate) collaboration rows and 6 more baseline
# rows on the ember panel (el2), rows r07..r12, same commands as run-replicates.sh. One lane; the control lane (original launcher) is a
# separate script (run-final-control.sh) so the owner's limit of 2 parallel lanes holds. Resumable via replicate-logs/done/. NOFALLBACK=1.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
C=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab
R4=$C/r4-flag-and-adjudicate
L=$C/replicate-logs; mkdir -p "$L/done"
export NOFALLBACK=1
cd "$REPO" || exit 2
step() {
  local id=$1; shift
  [ -e "$L/done/$id" ] && { echo "SKIP $id"; return 0; }
  echo "START $id $(date -u +%T)"
  ( "$@" ) >"$L/$id.log" 2>&1; local rc=$?
  echo "END $id rc=$rc $(date -u +%T)"
  [ $rc = 0 ] && touch "$L/done/$id"
  return 0
}
echo "START $(date -u +%T)"
for n in 07 08 09 10 11 12; do
  step r4-el2-collab-r$n env TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash $R4/bin/run-panel.sh --panel EL2 --row tce-f7-el2-r$n --values $R4/values/EL2.json --block tce-b$n
  step r4-el2-base-r$n   env PANEL_COLLAB=0 bash $R4/bin/run-panel.sh --panel EL2 --row a1-el2-r$n --values $R4/values/EL2.json --block tce-b$n
done
echo "ALLDONE $(date -u +%T)"
