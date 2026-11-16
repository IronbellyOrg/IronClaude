#!/usr/bin/env bash
# Owner order 2026-11-16: after stage 1 ends, move the invalid run aside (never delete) and rerun it once, alone, with the same seed and block.
set -u -o pipefail
cd "$(dirname "$0")/.." || exit 2
while pgrep -f 'run-schedule.sh runs-holdout' >/dev/null; do sleep 15; done
INV=stage1-z0-HX-3-r1
[ -e runs-holdout/$INV/run.json ] || { echo "nothing to rerun"; exit 0; }
mv runs-holdout/$INV runs-holdout/$INV.invalid-claude-update-20261116
echo "moved aside $INV $(date -u +%T)"
RL_RUNS_ROOT=$PWD/runs-holdout NOFALLBACK=1 bash ../20261114-collab-process/with-slot.sh rl-holdout-rerun bash bin/run-schedule.sh runs-holdout/schedule-stage1.tsv
echo "RERUN DONE $(date -u +%T) rc=$?"
