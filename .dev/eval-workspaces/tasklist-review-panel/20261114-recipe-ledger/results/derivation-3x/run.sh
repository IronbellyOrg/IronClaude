#!/usr/bin/env bash
# Owner order 2026-11-16 ("run the recipe ledger experiment 3 times and summarize results").
# 3 replicates of arms Z0 (the plain panel, harness fixes and brief edits), K (plain words) and RL (recipes and ledger) on the primary panel
# (muse-ember-1.0 + 2 x gpt-6-luna) over the three STUDY packages (derivation check; the requirements say study packages are never evidence for
# adoption). 27 panel runs, one at a time (timing is only valid without parallel panels), then blind judging by Opus (judge only), 2 at a time.
# Each stage is wrapped in the shared slot lock as one slot. NOFALLBACK=1. Resumable: run.sh again skips finished runs and judged labels.
# Not done by this run: freeze tag, hold-out documents, shared control, parity test (void: the sibling redesign is stopped).
set -u -o pipefail
RLD=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
LOCK=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-collab-process/with-slot.sh
cd "$RLD" || exit 2
export NOFALLBACK=1 SW_SB_ROOT=/tmp/evalsb-recipe
OUT=$RLD/results/derivation-3x
echo "START schedule $(date -u +%T)"
bash "$LOCK" rl-derivation-schedule bash bin/run-schedule.sh "$OUT/schedule.tsv" --max-panels 1 > "$OUT/schedule-run.out" 2>&1
echo "END schedule rc=$? $(date -u +%T)"
echo "START judge $(date -u +%T)"
bash "$LOCK" rl-derivation-judge bash bin/judge-batch.sh --go --par 2 staged1 > "$OUT/judge-run.out" 2>&1
echo "END judge rc=$? $(date -u +%T)"
echo ALLDONE
