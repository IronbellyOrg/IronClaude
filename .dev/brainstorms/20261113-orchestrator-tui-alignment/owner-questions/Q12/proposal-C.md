# Proposal C: one routing row, own small PR after PR #539 merges

## Answer

Yes: one routing row for `superclaude observe` in `HOW-WE-WORK.md` (the routing guide), copied to its plugin mirror and matched in the sc-recommend table, in its own small PR after PR #539 (the sweep PR) merges, with the needed routing-test edits named in the PR.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- After #539 merges, work item OB-07 starts in a new worktree from `origin/master`. The PR decides which table carries the row: the routing table needs 8 cells and resolvable steps, and the other-commands table rejects a row with no slash command and pins its member list (INV-029, an invariant-probe finding; `tests/core/test_how_we_work_routing_table.py:193-205`, `:297-298`). Every test edit is named in the PR body, including `tests/recommend/test_routing_refresh.py:33`.
- The row says "person only" (INV-013, an invariant-probe finding that only a coordinator or person should run the observer).
- A supervised worker makes and tests the change; the PR session opens the PR with `/sc:pr-submit --monitor 3` under the owner's grant row for that PR.

## What it unlocks

- The observer, built and merged in PRs #503 and #514, becomes findable through the same table people and `/sc:recommend` already use; today no guide or command file names it (grep, 2026-11-14).
- Small and reversible: one row plus test edits, reverted by one PR.
- Follows the source review's recommendation: "the routing row only, in its own small PR. A command is not needed" (variant-5-original.md:258-259).

## What it costs or risks

- At least one routing test must change, because neither table accepts a CLI-only entry as written (INV-029); a test edit to fit one row is a small precedent for non-slash entries.
- Waits for #539, which edits the same four files; until then nothing moves.
- Advertises a dashboard whose coordinator-questions panel is still off on master (owner question Q6).

## What stays unresolved

- Which of the two tables carries the row (decided inside the PR).
