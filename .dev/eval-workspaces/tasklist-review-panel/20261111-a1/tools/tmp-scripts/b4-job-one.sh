#!/usr/bin/env bash
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
p="$1"; rid="$2"; model="$3"; C="$4"
[ -e "/tmp/cancel-$C" ] && { echo "SKIP-CANCELLED $(date -u +%T) $C/$p/$rid"; exit 0; }
echo "START $(date -u +%T) $C/$p/$rid=$model"
bash "$EVAL/tools/run-reviewer.sh" "$EVAL" "$p" "$rid" "$model" "combos/$C"
echo "END $(date -u +%T) $C/$p/$rid $(jq -c '[.observed_model,.model_ok,.findings_block]' "$EVAL/$p/reviews/combos/$C/$rid.meta.json" 2>/dev/null)"
