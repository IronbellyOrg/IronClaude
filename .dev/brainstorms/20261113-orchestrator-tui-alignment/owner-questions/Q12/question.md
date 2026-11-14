# Q12: should the observer get a routing row

## Question (verbatim from the spec row)

merged-requirements.md section 3, row Q12: "A routing row for the observer?"

ADJ Part 7 wording (alignment-findings-adjudicated.md:782): "Should the observer get a routing row in `HOW-WE-WORK.md` (and its plugin mirror and the sc-recommend table)?"

## Spec's recommended answer

"Yes, one row, own small PR after #539 merges" (merged-requirements.md:539). ADJ adds: "(the two table tests need edits: INV-029)" (alignment-findings-adjudicated.md:782). Origin: V5 D8 (variant-5-original.md:256-259): "the routing row only, in its own small PR. A command is not needed: it is a CLI the user starts in a terminal."

## Default if unanswered

"PLAN INFERENCE: OB-07 does not start" (merged-requirements.md:539). PLAN INFERENCE means the spec derived it; no debate file states it.

## What it gates

- OB-07, "Routing row for `superclaude observe`" (merged-requirements.md:255): a small PR that adds the observer to the routing guide `HOW-WE-WORK.md`, its byte-for-byte plugin mirror and the sc-recommend table, with named test edits and a "person only" line. Wave W3 (the wave that opens after PR #539, the sweep PR, merges).
- Graph: "SW-05, K-ROUTE, Q12 -> OB-07" (merged-requirements.md:807). SW-05 is the merge of PR #539; K-ROUTE is the shared routing files (merged-requirements.md:622). OB-07 is a sink: nothing waits on it (merged-requirements.md:779).

## Facts the question depends on

1. The observer `superclaude observe` (issue #409) is built and merged (PRs #503, #514; ADJ glossary line 77); its code is in `src/superclaude/cli/observe/`.
2. The routing guide on this branch and on `origin/master` does not mention `superclaude observe` (grep of `src/superclaude/core/HOW-WE-WORK.md` and `git show origin/master:...`, run 2026-11-14: no hit for "observe" except unrelated words). `docs/`, `src/superclaude/core` and `src/superclaude/commands` have no "superclaude observe" text either (same grep).
3. INV-029 (an invariant-probe finding, MEDIUM, invariant-probe.md:36): "A CLI-only `superclaude observe` row fits neither block without a test edit." The routing-table block needs 8 cells and resolvable steps (`tests/core/test_how_we_work_routing_table.py:193-205`, re-read); the other-commands block takes the first backticked slash token of each row and asserts `members == _OTHER_COMMANDS` (`:297-298`, re-read), so a row with no slash command breaks it. PR #539 already edits the same test, `tests/recommend/test_routing_refresh.py:33` and both guide copies.
4. INV-013 (LOW, invariant-probe.md:20): only a coordinator or a person should run `superclaude observe`; the never-as-worker list names slash commands only, and an unscoped worker listing from an unbound terminal returned rows across all Runs. Action: one "person only" sentence in the routing row and the contract note.
5. The "Orca coordination" section of the guide (`HOW-WE-WORK.md:398` onward, re-read) is a bullet list, not a machine-read table; the two table tests above do not read it. PR #539 added the `/sc:sweep` bullet there.
6. Project rule: after editing `HOW-WE-WORK.md` it must be copied byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (project CLAUDE.md, "Key Documentation Files").
7. Every PR goes to the fork through `/sc:pr-submit --monitor 3` (project CLAUDE.md; merged-requirements.md:768, edge 121).
8. V5 D8 options: a routing row and a sc-recommend line; a `/sc:observe` command; nothing (variant-5-original.md:256-259).
