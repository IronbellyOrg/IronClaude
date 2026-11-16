#!/usr/bin/env bash
# Confirming run: replicates 4 to 9 (owner order 2026-11-16, "run 6 more"); same driver as run2.sh with schedule-9reps.tsv and up to 25 passes (owner order 2026-11-16). Pass 1 (run.sh) finished 9 of 27 runs: after the first run on each of two
# packages the reviewers had left .venv/ and uv.lock in the sandbox, and bin/run-panel.sh refuses a dirty sandbox (exit 2, E_SANDBOX_DIRTY).
# This is the known gap listed in POST-BUILD-LOG-20261115.md item 6 (bin/run-schedule.sh has no rebuild between runs; bin/run-spike.sh has).
# Fix without editing the RL code: before every pass of bin/run-schedule.sh, rebuild any dirty sandbox under /tmp/evalsb-recipe with RL's own
# build-sandbox.sh (same guard as run-spike.sh), then run the schedule again; finished runs are skipped. One panel at a time, so a rebuild never
# races a run. Passes stop when no run fails or after 12 passes. Consequence for the record: runs finish in a different order than the
# block-randomised schedule (a refused run waits for a later pass), so load drift is not cancelled by blocks; the summary says so.
set -u -o pipefail
RLD=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
LOCK=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-collab-process/with-slot.sh
cd "$RLD" || exit 2
export NOFALLBACK=1 SW_SB_ROOT=/tmp/evalsb-recipe
OUT=$RLD/results/derivation-3x
DOCS="TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415"

fresh_sandboxes() {
  local doc sbx
  for doc in $DOCS; do
    sbx=$SW_SB_ROOT/$doc
    if [ -d "$sbx/repo/.git" ] && [ -n "$(git -C "$sbx/repo" status --porcelain --ignored)" ]; then
      case "$(realpath -m -- "$sbx")/" in /tmp/evalsb-recipe/?*) ;; *) echo "E_SANDBOX: refusing to rebuild $sbx" >&2; return 2 ;; esac
      rm -rf -- "$sbx" && bash bin/build-sandbox.sh "$doc" > /dev/null || return 2
      echo "rebuilt $doc"
    fi
  done
}

echo "START pass loop $(date -u +%T)"
for pass in $(seq 1 25); do
  fresh_sandboxes || { echo "E_REBUILD"; break; }
  echo "PASS $pass $(date -u +%T)"
  bash "$LOCK" rl-derivation-schedule bash bin/run-schedule.sh "$OUT/schedule-9reps.tsv" --max-panels 1 > "$OUT/schedule-run9-pass$pass.out" 2>&1
  rc=$?
  tail -1 "$OUT/schedule-run9-pass$pass.out" | cut -c1-200
  [ "$rc" = 0 ] && { echo "all runs done after pass $pass"; break; }
  [ "$rc" = 1 ] || { echo "schedule exit $rc, stopping"; break; }
done
echo "START judge $(date -u +%T)"
bash "$LOCK" rl-derivation-judge bash bin/judge-batch.sh --go --par 2 staged1 > "$OUT/judge-run3.out" 2>&1
echo "END judge rc=$? $(date -u +%T)"
echo ALLDONE
