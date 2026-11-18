---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeScSaveAndL-20261117-210605
version: "1"
priority: Medium
created_date: "2026-11-17"
---

# Remove /sc:save and /sc:load (6.0.0, PR 6)

Source: ./source.md
Goal: `/sc:save` and `/sc:load` no longer exist in the commands, their mirrors, the docs, the routing guide or the routing tests, while the `sc-crash-recovery` skill and the `<project>/.superclaude/memory/` folder convention stay.

## Constraints

- The edit list is `.dev/cleanup/save-load/dependency-map.md` (sections A and B); section C lists what must not change.
- Source of truth is `src/superclaude/`. Run `make sync-dev` for the mirrors and never stage `.claude/` (except `.claude/settings.json`).
- Do not edit historical records: `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries and tracked `.dev/` working records. Do not add a `CHANGELOG.md` entry.
- Keep the `sc-crash-recovery` skill, `ccsession-tag/install.sh` (its `PLAN-context-save-load.md` clean-up line is an old file name, not the command) and the frozen command-disposition rows in `tests/recommend/fixtures/routing_refresh_cases.json`.
- Only remove or reword lines that tell a reader to run `/sc:save` or `/sc:load`. If a kept skill or command cannot work without them, stop and report; do not invent a replacement.
- The two files `HOW-WE-WORK.md` copies and the two `RULES.md` copies must stay byte-identical to their source.

## Phase 1: Delete the commands

## Task 1: Delete the six command files and the stale dev copies

Delete `src/superclaude/commands/save.md`, `src/superclaude/commands/load.md`, `plugins/superclaude/commands/save.md`, `plugins/superclaude/commands/load.md`, `commands/sc-save.md` and `commands/sc-load.md` (dependency map section A). Then run `make sync-dev` and remove the two stale copies of these commands from the gitignored `.claude` mirror by hand, because `make sync-dev` copies but never prunes.

Acceptance criteria:
- None of the six tracked files exists, and `git status` shows only those six as deleted for this task.
- `make verify-sync` reports all components in sync.
- `superclaude install` no longer has a `save.md` or `load.md` to copy (checked by the install test in Task 6 and the throwaway-HOME install in the final gate).

## Phase 2: Fix the routing guide, rules and kept skills

## Task 2: Remove the two commands from the routing guide and its plugin copy

Depends on: Task 1

In `src/superclaude/core/HOW-WE-WORK.md` delete the paragraph at line 238 that starts "`/sc:save` and `/sc:load` store and load project memory" (keep the sentences after it about other command-owned continuations, reworded to start on their own), delete the `/sc:load` row (line 331) and the `/sc:save` row (line 333) of the Other commands table, and remove "`/sc:save` and `/sc:load` are memory, not executor resume;" from the resume row (line 375). Copy the result byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` shows no difference.
- `tests/core/test_how_we_work_routing_table.py` and `tests/commands/test_routing_plugin_parity.py` pass after Task 5.
- `git grep -n -E 'sc:save|sc:load'` finds nothing in either guide copy.

## Task 3: Remove the session lifecycle lines from the rules and the example from the worker contract

Depends on: Task 1

In `src/superclaude/core/RULES.md` delete the "Session Lifecycle" and "Session Pattern" lines (49-50) and keep "Checkpoint Triggers"; apply the identical edit to `plugins/superclaude/core/RULES.md`. In `src/superclaude/core/WORKER-CONTRACT.md` line 204 replace the example `Command: /sc:load ...`, then the converted command, with `Command: /sc:design ...`, then `Command: /sc:workflow ...`.

Acceptance criteria:
- The two `RULES.md` files are byte-identical to each other and name neither command.
- `WORKER-CONTRACT.md` names neither command, and `tests/skills/test_worker_contract.py` still passes after Task 6.

## Task 4: Remove the mentions from the sc-crash-recovery and sc-roadmap-protocol skills

Depends on: Task 1

In `src/superclaude/skills/sc-crash-recovery/SKILL.md` delete the bullet at line 157 ("It does not replace `/sc:load` ..."). In `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` delete each "Trigger `sc:save` with ..." clause in the exit criteria at lines 190, 215, 272, 297 and 316, delete completion step 3 at line 326 (renumber the next step), and reword line 420 so it says sc:roadmap persists session state at each wave boundary to `<output_dir>/.session-memory.md`, without naming `sc:save`.

Acceptance criteria:
- Neither skill names `sc:save` or `/sc:load`.
- `sc-crash-recovery` still has its `SKILL.md`, `refs/` and `scripts/` untouched apart from that one bullet, and still installs.
- The roadmap skill's own `.session-memory.md` save points, session schema and resume protocol are unchanged.

## Phase 3: Fix the tests

## Task 5: Update the routing tests

Depends on: Task 2

In `tests/core/test_how_we_work_routing_table.py` remove `"sc:save"` and `"sc:load"` from `_OTHER_COMMANDS` (lines 38-39). In `tests/recommend/fixtures/routing_refresh_cases.json` delete case S25 (the save case, with its load repeat). In `tests/recommend/test_routing_refresh.py` make the case id list skip 25 as well as 27, add `save` and `load` to `_POST_REFRESH_REMOVALS`, and say in the module docstring that S25 is retired. Leave the frozen command-disposition rows and the `formatting_only` list alone.

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/recommend tests/commands/test_routing_plugin_parity.py` passes.
- The fixture's `save` and `load` command rows are still present, and the shipped-command comparison still holds through `_POST_REFRESH_REMOVALS`.

## Task 6: Update the worker-contract and install tests

Depends on: Task 1

In `tests/skills/test_worker_contract.py` delete `test_load_usage_line_declares_checkpoint_and_load_is_not_converted` (lines 1429-1434), remove `"load"` from `NOT_CONVERTED_IN_P1` (line 1448) and change the synthetic temp file at lines 1602-1607 from `load.md` to `pm.md` with `["pm"]`. In `tests/unit/test_cli_install.py` remove `load.md` and `save.md` from both expected command lists (lines 116, 118 and 404).

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py tests/unit/test_cli_install.py` passes.
- The only removed tests are the one deleted function and the `load` case of `test_unconverted_command_has_no_unattended_section`.

## Phase 4: Fix the docs

## Task 7: Rewrite the user guides

Depends on: Task 1

In `docs/user-guide/commands.md` delete the `/sc:load` and `/sc:save` table rows (lines 110-111) and both sections (`### /sc:load` at about line 411 and `### /sc:save` at about line 654). In `docs/user-guide/session-management.md` delete the two command sections, every `/sc:save` and `/sc:load` example and instruction, and the end-of-fallback text of "Upgrading from Serena memory" (keep the `cp` recipe), and say memory is written by `/sc:pm` and the PM agent; keep the resume section and the context-envelope section. In `README.md` line 100 say the memory folder is read and written by `/sc:pm` and the PM agent. In `docs/user-guide/codegraph.md` delete the `/sc:load` bullet (line 123) and drop `load.md` from the Source line (125). In `docs/user-guide/memory-system.md` line 18 replace "that `/sc:save` writes and `/sc:load` reads" with wording about the PM agent.

Acceptance criteria:
- None of the five files names `/sc:save` or `/sc:load`.
- Links inside `session-management.md` and `commands.md` still resolve (no anchor to a deleted section).

## Task 8: Rewrite the developer and reference docs

Depends on: Task 1

In `docs/developer-guide/session-memory.md` remove the save and load rows, the `/sc:save` and `/sc:load` subsections and the "Legacy fallback" section, renumber the contents list, point the layout and write-rule sources to `src/superclaude/agents/pm-agent.md`, and reword "Why files", "Stores this is not" and "Changing the store" so they name neither command. In `docs/developer-guide/README.md` reword lines 56 and 82. In `docs/getting-started/upgrading.md` rewrite Step 5 (lines 241-248) to say `/sc:pm` and the PM agent keep the memory, that 6.0.0 removed `/sc:save`, `/sc:load` and the `.serena` fallback, and keep the copy recipe. In `docs/onboarding/ironclaude-onboarding.html` remove the two mentions (lines 534 and 574). In `docs/reference/pm-agent-autonomous-reflection.md` line 195 replace "written by `/sc:save`" with "written by the PM agent". In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` update lines 1321 and 2203: five command files with no section (`implement`, `post-release`, `roadmap`, `validate-roadmap`, `validate-tests`), 44 command files, and remove the `save` and `/sc:load` statements.

Acceptance criteria:
- None of the six files names `/sc:save` or `/sc:load`, and `git grep -n -E 'sc:save|sc:load|sc-save|sc-load'` finds nothing outside the historical records.
- `git diff --check` is clean and `uv run ruff check .` and `uv run ruff format --check src/ tests/` stay green.
