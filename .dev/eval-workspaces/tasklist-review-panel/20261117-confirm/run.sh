#!/usr/bin/env bash
# Confirming test of wonsol (owner order 2026-11-17); pre-registration PREREG.md (frozen, hash in FROZEN.txt).
# 50 panel runs: arm B = ember panel (panel "primary"), arm W = wonsol (panel "sonnet" in lenses-wonsol.json), plain Z0, 5 new plans x 5 replicates,
# one interleaved schedule, one panel at a time under the slot lock, killed runs moved aside and re-run once, then blind Opus judging.
set -u -o pipefail
RLD=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
CF=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261117-confirm
LOCK=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-collab-process/with-slot.sh
cd "$RLD" || exit 2
export NOFALLBACK=1 SW_SB_ROOT=/tmp/evalsb-recipe/confirm JUDGE_PKG_ROOT=$CF/confirm-gt
export RL_LENSES=$RLD/results/stronger-panel/lenses/lenses-wonsol.json RL_RUNS_ROOT=$RLD/runs-confirm
ROOT=$RL_RUNS_ROOT SCORING=$RLD/scoring-confirm SCHED=$CF/schedule/schedule.tsv OUT=$CF/logs
mkdir -p "$ROOT" "$SCORING" "$OUT"
echo "START $(date -u +%T) cli=$(claude --version 2>/dev/null | head -1)"
for pass in 1 2 3 4 5 6; do
  bash "$LOCK" cf-schedule bash bin/run-schedule.sh "$SCHED" --max-panels 1 > "$OUT/schedule-pass$pass.out" 2>&1
  rc=$?; echo "PASS $pass rc=$rc $(date -u +%T) $(tail -1 "$OUT/schedule-pass$pass.out" | cut -c1-160)"
  [ "$rc" = 0 ] && break
  [ "$rc" = 1 ] || { echo "schedule exit $rc, stopping"; break; }
done
inv=${ROOT}-invalid; mkdir -p "$inv"; n=0
for d in "$ROOT"/stagecf-*; do
  [ -f "$d/run.json" ] || continue
  if jq -e '[.reviewers[] | select(.absent_reason != null and .absent_reason != "invalid")] | length > 0' "$d/run.json" >/dev/null; then
    echo "invalid run $(basename "$d")"; mv "$d" "$inv/$(basename "$d").original-$(date -u +%H%M)"; n=$((n+1))
  fi
done
echo "$n invalid run(s) moved aside"
[ "$n" -gt 0 ] && { bash "$LOCK" cf-rerun bash bin/run-schedule.sh "$SCHED" --max-panels 1 > "$OUT/rerun.out" 2>&1; echo "rerun rc=$? $(tail -1 "$OUT/rerun.out" | cut -c1-160)"; }
bash "$LOCK" cf-judge bash bin/judge-batch.sh --go --par 2 --runs-dir "$ROOT" --scoring-dir "$SCORING" stagecf > "$OUT/judge.out" 2>&1
echo "judged rc=$? $(date -u +%T)"
echo ALLDONE-CONFIRM
