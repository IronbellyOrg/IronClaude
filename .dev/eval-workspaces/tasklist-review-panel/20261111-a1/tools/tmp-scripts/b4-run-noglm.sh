#!/usr/bin/env bash
# Batch 4 continuation WITHOUT glm (owner decision 2026-11-12 14:40 UTC: drop all glm runs for speed).
# Rows affected: n4-sonnet-src and n5-sonnet-src lose their glm reviewer (t3-1) -> 3-reviewer rows;
# n5-muse-glm-luna-src becomes muse+luna only (renamed n5-muse-luna-src). All other remaining rows have no glm.
# Already complete (not re-run here): sol-alone-src(3), n2-sonnet-src(12), n4-sonnet-src muse(1 of 4 done).
set -u
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
RR="$EVAL/tools/run-reviewer.sh"
DS=TASK-WF-designSpec-20261107-075614
AL=TASK-WF-makeTheAliasOnly-20261105-051649
DE=TASK-WF-design-20261108-041415

run() { echo "START $(date -u +%T) $4/$1/$2=$3"; bash "$RR" "$EVAL" "$1" "$2" "$3" "combos/$4"; echo "END $(date -u +%T) $4/$1/$2 $(jq -c '[.observed_model,.model_ok,.findings_block]' "$EVAL/$1/reviews/combos/$4/$2.meta.json" 2>/dev/null)"; }

# n4-sonnet-src WITHOUT glm: muse (already done for designSpec; skip if final exists), haiku, sonnet
have() { [ -f "$EVAL/$1/reviews/combos/$2/$3.md" ] && [ -f "$EVAL/$1/reviews/combos/$2/$3.meta.json" ]; }
for p in $DS $AL $DE; do
  have "$p" n4-sonnet-src t2b-1 || run "$p" t2b-1 muse-wonder-1.0 n4-sonnet-src
  run "$p" t4-1 claude-haiku-5-5 n4-sonnet-src
  run "$p" t1b-1 claude-sonnet-5-5 n4-sonnet-src
done
# n5-sonnet-src WITHOUT glm: muse, luna, sonnet
for p in $DS $AL $DE; do
  run "$p" t2b-1 muse-wonder-1.0 n5-sonnet-src
  run "$p" t4-1 gpt-6-luna n5-sonnet-src
  run "$p" t1b-1 claude-sonnet-5-5 n5-sonnet-src
done
# r2-sonnet-src (no glm): haiku x2, grok, sonnet
for p in $DS $AL $DE; do
  run "$p" t4-1 claude-haiku-5-5 r2-sonnet-src
  run "$p" t3-1 claude-haiku-5-5 r2-sonnet-src
  run "$p" t4-2 grok-4.7 r2-sonnet-src
  run "$p" t1b-1 claude-sonnet-5-5 r2-sonnet-src
done
# r1-haiku-luna2-src (no glm)
for p in $DS $AL $DE; do
  run "$p" t4-1 claude-haiku-5-5 r1-haiku-luna2-src
  run "$p" t4-2 gpt-6-luna r1-haiku-luna2-src
  run "$p" t3-1 gpt-6-luna r1-haiku-luna2-src
done
# n2-muse-haiku-grok-src (no glm)
for p in $DS $AL $DE; do
  run "$p" t2b-1 muse-wonder-1.0 n2-muse-haiku-grok-src
  run "$p" t4-1 claude-haiku-5-5 n2-muse-haiku-grok-src
  run "$p" t4-2 grok-4.7 n2-muse-haiku-grok-src
done
# n5-muse-luna-src (glm dropped from n5-muse-glm-luna)
for p in $DS $AL $DE; do
  run "$p" t2b-1 muse-wonder-1.0 n5-muse-luna-src
  run "$p" t4-1 gpt-6-luna n5-muse-luna-src
done
echo ALLDONE_NOGLM
