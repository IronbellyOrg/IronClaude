---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeScReviewTr-20261117-210253
version: "1"
priority: Medium
created_date: "2026-11-17"
---

# Remove /sc:review-translation and the sc-review-translation-protocol skill (6.0.0, PR 10)

Source: ./source.md
Goal: `/sc:review-translation` and the `sc-review-translation-protocol` skill are gone from commands, skills, mirrors, docs, the routing guide and the routing tests, with every count that depended on them corrected, and nothing outside the historical records and `.dev/tasks` names them.

## Constraints

- Source of truth is `src/superclaude/`. Local mirrors under `.claude/` are gitignored sync output: delete them by hand, never stage them.
- Leave alone: `.dev/**` records (including the `TASK-RESEARCH-recommend-refresh-*` package), `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, `CHANGELOG.md`, and the frozen 47-command record line in `tests/recommend/fixtures/routing_refresh_cases.json` (the line whose `name` is `review-translation`).
- Counts in `docs/developer-guide/technical-architecture.md`, `docs/getting-started/upgrading.md`, `PROJECT_INDEX.*` and the dated 2026-11-12 snapshot counts in `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` were already out of date before this change and stay as they are.
- The fork `ironbelly/IronClaudeV5` is read-only here: it holds both files with identical contents (blobs a2a5f8e0f and c5a26e491), checked before this plan.
- `swarm` and everything in "Kept for now" stays. No CHANGELOG entry.

## Phase 1: Remove the command, the skill and their unit test

## Task 1: Delete the command, the skill and their local mirrors

Delete `src/superclaude/commands/review-translation.md` and the whole folder `src/superclaude/skills/sc-review-translation-protocol/` (it holds only `SKILL.md`; no `refs/`). Also delete the gitignored local mirrors `.claude/commands/sc/review-translation.md` and `.claude/skills/sc-review-translation-protocol/` by hand, because `make sync-dev` copies but never prunes. No tracked copy exists under `plugins/superclaude/`, the root `commands/`, `skills/` or `agents/`; confirm with `git ls-files`.

Acceptance criteria:
- `git ls-files | grep -i review-translation` lists only paths under `.dev/tasks/` (old records) and nothing under `src/`, `plugins/`, `commands/`, `skills/` or `agents/`.
- `.claude/commands/sc/review-translation.md` and `.claude/skills/sc-review-translation-protocol` do not exist, and `git status` shows no staged `.claude/` path.
- `make verify-sync` reports all components in sync.

## Task 2: Delete the command's unit test file

Delete `tests/unit/test_review_translation.py` (565 lines, 44 test functions). It imports only `re` and `pytest` and exercises no production code, so nothing else depends on it.

Acceptance criteria:
- The file is gone, and `uv run pytest tests/unit -q` collects no error from a missing import.
- The pass count of the full suite drops by exactly the number of tests that file collected (record that number in the PR body).

## Phase 2: Remove the routing guide and worker contract text

## Task 3: Remove the two routing rows from the guide and refresh the plugin copy

Depends on: Task 1

In `src/superclaude/core/HOW-WE-WORK.md` delete the "Localization review" outcome row (line 252) and the `localization-review` routing row (line 383). Then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (the plugin copy has the same two rows at the same lines). The level table is untouched, so `src/superclaude/core/CLAUDE.md` needs no change.

Acceptance criteria:
- `git grep -n -i -E 'review-translation|localization-review|Localization review' -- src/superclaude/core plugins` prints nothing.
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- Dependents `tests/core/test_how_we_work_routing_table.py` and `tests/recommend/test_routing_refresh.py` read this file; they are updated in Tasks 6 and 7.

## Task 4: Remove the command from the worker contract

Depends on: Task 1

In `src/superclaude/core/WORKER-CONTRACT.md`: at line 330 change "the 15 commands converted in P2" to 14 and drop `review-translation` from the parenthesised list; at line 334 change "the five P2 commands with a required brief flag (`/sc:auggie-review`, `/sc:cli-eval`, `/sc:cli-portify`, `/sc:review-translation`, `/sc:spec-panel`)" to the four that remain and "so it has 17 rows" to 16; delete the table row `| /sc:review-translation | ... |` at line 350. Leave the "12 commands that are ready" count unchanged (review-translation was one of the five P2 rows, not of the 12).

Acceptance criteria:
- `git grep -n -i review-translation -- src/superclaude/core/WORKER-CONTRACT.md` prints nothing.
- The brief-flag table has 16 data rows, matching the sentence above it.
- `tests/skills/test_worker_contract.py` (updated in Task 5) passes against the edited contract.

## Phase 3: Update the tests that named the command

## Task 5: Update the worker contract test

Depends on: Task 4

In `tests/skills/test_worker_contract.py`: remove `"review-translation"` from `P2_COMMANDS` (line 504) and from `P2_NEW_BRIEF_ROWS` (line 1006); remove the `UNATTENDED_EXPECT["review-translation"]` entry (lines 679 to 690); remove the two `review-translation` tuples in `P2_GATES` (around lines 1813 to 1824); in `_check_p2_set` (line 1667) change the P2 size 15 to 14 (both asserts and the message) and the `UNATTENDED_EXPECT` size 31 to 30 (assert and message). Dependents of `P2_COMMANDS` in the same file (`_check_p1_set`, `_check_p2_brief`, `_P2_SET_DEFECTS`, the set-completeness tests) follow from the tuple and need no separate edit.

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -q` passes with no failure, and its pass count drops only by the parametrized cases of the removed command.
- `git grep -n review-translation -- tests/skills` prints nothing.

## Task 6: Update the routing table test

Depends on: Task 3

In `tests/core/test_how_we_work_routing_table.py`: remove `"localization-review"` from `_EXPECTED_IDS` (line 86) and add to the comment above the set that `localization-review` left in 6.0.0 with `/sc:review-translation`; remove `"sc:review-translation"` from the not-in-other-commands set (line 305); remove the S07 tuple (lines 672 to 683); in the test whose docstring reads "T15-T17/S07/S29" (line 836) drop S07 from the docstring and delete the `locale = rows["localization-review"]` assertions (lines 850 to 855).

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_routing_table.py -q` passes.
- `git grep -n -i -E 'review-translation|localization-review|S07' -- tests/core` prints nothing.

## Task 7: Retire routing case S07 in the recommend fixture and its test

Depends on: Task 3

In `tests/recommend/fixtures/routing_refresh_cases.json`: delete the case with `"id": "S07"` (about lines 175 to 195, the case that targets `sc:review-translation`) and the two fixture inputs `source-strings` and `locale-files` (lines 32 and 33; only S07 used them). Keep the frozen command record line with `"name": "review-translation"` unchanged. In `tests/recommend/test_routing_refresh.py`: extend the module docstring (line 3) to say S07 is retired too; change `_POST_REFRESH_REMOVALS` (line 35) to `{"spawn", "review-translation"}` and update its comment; change the case-id assertion (line 139) to skip both 7 and 27.

Acceptance criteria:
- `uv run pytest tests/recommend -q` passes, and the parametrized per-case tests lose exactly the S07 cases.
- The fixture is still valid JSON and `git grep -n 'sc:review-translation' -- tests/recommend` prints nothing.

## Task 8: Update the install test expectations

Depends on: Task 1

In `tests/unit/test_cli_install.py` remove `review-translation.md` from the expected command list (line 118) and `sc-review-translation-protocol/SKILL.md` from the expected skill list (line 288), keeping the surrounding word wrapping and the other names.

Acceptance criteria:
- `uv run pytest tests/unit/test_cli_install.py -q` passes.
- `git grep -n -i review-translation -- tests/unit` prints nothing.

## Phase 4: Update the documentation

## Task 9: Remove the command from the user guide

Depends on: Task 1

In `docs/user-guide/commands.md` delete the table row at line 95 and the whole `### /sc:review-translation - Localization Quality Review` section (lines 587 to 615), including its closing `---` rule so the neighbouring sections keep exactly one separator.

Acceptance criteria:
- `git grep -n -i -E 'review-translation|tone-matrix' -- docs/user-guide` prints nothing.
- The sections before and after the deleted one are still separated by one `---` line and the file passes `make lint`.

## Task 10: Fix the developer guide and the supervised-orchestration reference

Depends on: Task 4

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` line 976 change "All 31 converted commands ... (16 from phase 1, 15 from phase 2) ... exactly those 31 entries" to 30, 14 and 30. In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`: at line 1315 drop `review-translation` from the 22-command list and change 22 to 21; at line 1840 change "five P2 commands (auggie-review, cli-eval, cli-portify, review-translation, spec-panel ...)" to four without the name, "exactly 15 P2 names" to 14, `len(expect) == 31` to 30, and any row-count words in the same sentence to match (the other rows and row line numbers are quoted from the 2026-11-12 snapshot and stay); at line 1989 change "its five P2 rows (...)" to four without the name. Leave every other snapshot count in that file.

Acceptance criteria:
- `git grep -n -i review-translation -- docs/developer-guide docs/architecture` prints nothing.
- Line 976 of the developer guide reads 30 converted commands, 16 from phase 1 and 14 from phase 2.

## Task 11: Remove the command from the generated contributor knowledge base

Depends on: Task 1

In `docs/generated/contributor-knowledge-base/architecture-guide.md` delete the line `- \`sc-review-translation-protocol/\`` (line 261). In `components-guide.md` delete the line `- review-translation protocol` (line 188). In `visual-architecture-summary.md`: drop the table-of-contents entry (line 28) and retitle it and the section heading (line 446) to "Audit and recommendation orchestration family" with the matching anchor `#audit-and-recommendation-orchestration-family`; in the first mermaid block delete node `C7[/sc:review-translation]` and `S7[sc:review-translation-protocol]` and the edge `C7 --> S7`, renumbering `C8`, `C9`, `S8`, `S9` to `C7`, `C8`, `S7`, `S8` and their edges; in the family section change "These flows are all skill-backed (... the other two by `-protocol` skills)" to "the other by a `-protocol` skill", delete the `/sc:review-translation` bullet (line 452) and the whole `subgraph Translation[Localization review flow]` block (lines 473 to 480); at line 606 remove `review-translation, ` from the family list.

Acceptance criteria:
- `git grep -n -i -E 'review-translation|Localization review' -- docs/generated` prints nothing.
- Every anchor link in `visual-architecture-summary.md`'s table of contents still resolves to an existing heading, and each mermaid block keeps balanced `subgraph`/`end` pairs.
