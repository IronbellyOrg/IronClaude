<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (proposal-C) -->
<!-- Merge date: 2026-11-14 -->

# Merged proposal: one routing-table row, own small PR after PR #539 merges

<!-- Source: Base (original, modified) - Change 1 -->
## Answer

Yes: one row for `superclaude observe` in the routing table of `HOW-WE-WORK.md` (the routing guide), copied byte-for-byte to its plugin mirror, in its own small PR after PR #539 (the sweep PR) merges. The other-commands table is not used, because it accepts only slash commands and pins its member list.

<!-- Source: Base (original, modified) - Changes 1 to 4 -->
## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- After #539 merges, work item OB-07 starts in a new worktree from `origin/master`. A supervised worker adds the row and runs `uv run pytest tests/core/test_how_we_work_routing_table.py tests/recommend/ -v` before naming any test edit: by reading, a row whose step is a plain terminal command passes today (the command-token pattern needs a backtick then a slash, test :105; the `resume` row already has a terminal step, HOW-WE-WORK.md:376), provided its section cell names a numbered heading (test :336-340). Any test edit the run forces is named in the PR body. (Changes 1, 2)
- The row describes only what the observer does on master today, with no flags or panels that are still off (its coordinator-questions panel stays off until owner question Q6 is answered). (Change 3)
- The row's notes cell says "Coordinator or person only, never a worker", the same words the `/sc:sweep` entry uses (HOW-WE-WORK.md:335); optionally one line beside the never-as-worker bullet (HOW-WE-WORK.md:405). (Change 4)
- The PR session opens the PR with `/sc:pr-submit --monitor 3` under the owner's grant row for that PR.

<!-- Source: Base (original) -->
## What it unlocks

- The observer, merged in PRs #503 and #514, becomes findable through the table people and `/sc:recommend` read; the recommender reads only the marked blocks (sc-recommend SKILL.md:50-54), and today nothing names the observer.
- Small and reversible: one row, reverted by one PR.
- Follows the source review: "the routing row only, in its own small PR. A command is not needed" (variant-5-original.md:258-259).

<!-- Source: Base (original, modified) - Change 2 -->
## What it costs or risks

- A routing test may still need a change if the run disagrees with the reading above.
- Waits for #539, which edits the same files.
- Advertises a dashboard whose questions panel is off; the wording rule in Change 3 limits that.

<!-- Source: Base (original, modified) -->
## What stays unresolved

- Which numbered section the row cites (for example 3.13 "Specialist deliverables and operations", suggested by one advocate; the PR picks).
