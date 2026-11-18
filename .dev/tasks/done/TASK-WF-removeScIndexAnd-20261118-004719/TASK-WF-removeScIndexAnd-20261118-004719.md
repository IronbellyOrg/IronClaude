---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeScIndexAnd-20261118-004719
version: "1"
priority: Medium
created_date: "2026-11-18"
---

# Remove /sc:index and /sc:index-repo (6.0.0, PR 9)

Source: ./source.md
Goal: `/sc:index` and `/sc:index-repo` are gone from the command files, every mirror, the docs, the routing guide (both copies), the worker contract and the routing tests; no tracked file outside the historical records and `.dev/` working records names them; the full test suite has 0 new failures and its pass count drops only by the tests of the removed commands; `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync` and `git diff --check` stay green.

## Constraints

- Source of truth is `src/superclaude/`. After editing it run `make sync-dev` for the mirrors under the project `.claude` folder; those mirrors are gitignored and are never staged (the only tracked `.claude` file is `.claude/settings.json`).
- Do not edit historical records: `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries. Do not add a `CHANGELOG.md` entry (the release PR does that). `.dev/` working records (research, experiments, finished tasks) are not edited.
- What stays: the `repo-index` agent (`src/superclaude/agents/repo-index.md` and its mirrors; agents are issue 572), codegraph and `/sc:graph`, the generated `PROJECT_INDEX.md` and `PROJECT_INDEX.json` files at the repo root, `src/superclaude/execution/reflection.py` (reads `PROJECT_INDEX.md` when present, needs no command), the frozen command record in `tests/recommend/fixtures/routing_refresh_cases.json` (its `commands` list names `index` and `index-repo`, as it still names build, improve, save and load), and swarm with everything under "Kept for now" in issue 571.
- Smallest edit that keeps each sentence true: name `/sc:graph` or codegraph only where it really does the job, otherwise drop the clause. Do not renumber or reword unrelated text.
- The line-by-line list of references is `.dev/cleanup/index/dependency-map.md`; line numbers there were measured at 956f49642 and move as earlier tasks edit a file, so locate each reference by its text.
- Shared files (`PROJECT_INDEX.*`, `docs/developer-guide/technical-architecture.md`, the routing guide) are also touched by other PRs of the wave. Keep every removal that is already on `origin/integration` if a rebase is needed.
- No count statement outside the ones named in the tasks below is changed (for example "45 slash commands" in `docs/developer-guide/technical-architecture.md` was already stale and is left for the release PR).

## Phase 1: Delete the commands and their mirrors

## Task 1: Delete the six tracked command files and the stale dev mirror copies

Delete these tracked files: `src/superclaude/commands/index.md`, `src/superclaude/commands/index-repo.md`, `plugins/superclaude/commands/index.md`, `plugins/superclaude/commands/index-repo.md`, `commands/sc-index.md`, `commands/sc-index-repo.md`. `make sync-dev` copies but does not delete, so also remove the two gitignored dev mirror copies (`index.md` and `index-repo.md`) from the project `.claude` commands folder, then run `make sync-dev`. Nothing under `src/superclaude/skills/`, `agents/`, `hooks/` or `cli/` names these commands (checked in the dependency map, section Scope rules), so no other file needs to change for the deletion itself.

Acceptance criteria:
- `git ls-files | grep -E '(^|/)(index|index-repo)\.md$|sc-index'` lists none of the six paths (other tracked files named `INDEX.md` or `index-template.md` elsewhere are unrelated and stay).
- The project `.claude` commands folder has no `index.md` or `index-repo.md` after `make sync-dev`, and `git status --short` shows no path under `.claude/` other than possibly `.claude/settings.json` (never staged).
- `make verify-sync` reports all components in sync.

## Phase 2: Update the shipped guide, contract and legacy text

## Task 2: Remove the index rows and steps from the routing guide source

Depends on: Task 1

In `src/superclaude/core/HOW-WE-WORK.md`: delete the whole table row that begins `| Coordinated project-wide documentation and navigation |` (it names only `/sc:index`); delete the two rows `| \`/sc:index\` |` and `| \`/sc:index-repo\` |` of the Other-commands block (the block between the `other-commands:v1` and `/other-commands` markers); in the `document-built` row of the routing table remove "coordinated project docs" from the intent cell, remove step `1b. coordinated project documentation: \`/sc:index <target>\` with requested type/format` and renumber step `1c` to `1b`. The level-table block is untouched, so `src/superclaude/core/CLAUDE.md` does not change.

Acceptance criteria:
- `git grep -nE 'sc:index|index-repo' src/superclaude/core/HOW-WE-WORK.md` prints nothing.
- The `document-built` row steps read `1a. focused output ...`, `1b. template-led output: one of /tech-reference, /operational-guide, /readme ...`, then `2. stop at the requested documentation`.
- `tests/core/test_claude_md_routing_block.py` still passes (the level-table copy in `src/superclaude/core/CLAUDE.md` is unchanged and byte-equal).

## Task 3: Copy the routing guide to the sc-recommend reference

Depends on: Task 2

Copy `src/superclaude/core/HOW-WE-WORK.md` byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (project rule: the two copies are identical; the dependency map lists the same four reference lines there).

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` reports no difference.
- `git grep -nE 'sc:index|index-repo' plugins/superclaude/skills/sc-recommend` prints nothing.

## Task 4: Remove the two commands from the worker contract

Depends on: Task 1

In `src/superclaude/core/WORKER-CONTRACT.md`: in the bullet that starts `Put --unattended and exactly one report directory on every Command: line`, change "the 15 commands converted in P1 (adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow, analyze, business-panel, design, document, explain, index, test)" to "the 13 commands converted in P1" with `index-repo` and `index` removed from the list; in the paragraph that starts `Flags the brief must pass, for the 12 commands` change 12 to 11, change the sentence "`/sc:index-repo` and `/sc:init-lite` have no directory flag of their own, so they take `--report-dir`" to name `/sc:init-lite` alone ("has no directory flag of its own, so it takes `--report-dir`"), and change "so it has 15 rows" to 14; delete the table row `| \`/sc:index-repo\` | \`--report-dir <dir>\` |`. The P2 sentence ("12 commands converted in P2") is already correct and stays.

Acceptance criteria:
- `git grep -nE 'sc:index|index-repo|\bindex\b' src/superclaude/core/WORKER-CONTRACT.md` prints nothing that refers to the removed commands.
- The brief flag table has 14 data rows (11 ready commands plus the 3 P2 rows `/sc:auggie-review`, `/sc:cli-eval`, `/sc:spec-panel`).
- `tests/skills/test_worker_contract.py` phrase pins on the contract text still pass after Task 12.

## Task 5: Remove the two commands from the legacy root commands folder text

Depends on: Task 1

In `commands/sc-README.md` delete the bullet `- **index-repo.md** - Repository indexing for context optimization`. In `commands/sc-help.md` delete the table row that names `/sc:sc:index` ("Generate comprehensive project documentation and knowledge base with intelligent organization").

Acceptance criteria:
- `git grep -nE 'sc:sc:index|sc:index|index-repo' commands/` prints nothing.
- The surrounding bullet list in `commands/sc-README.md` and table in `commands/sc-help.md` stay well formed (no blank row, no dangling separator).

## Phase 3: Update the docs

## Task 6: Remove the two commands from the user guide

Depends on: Task 1

In `docs/user-guide/commands.md`: delete the two table rows for `/sc:index-repo` (with its `#scindex-repo---repository-indexing` link) and `/sc:index`; delete the whole `### \`/sc:index\` - Project Documentation` section (up to the next `###` heading, `/sc:init-lite`); delete the whole `### \`/sc:index-repo\` - Repository Indexing` section (up to the next `###` heading, `/sc:spec-panel`). In `docs/user-guide/flags.md` delete the `### Index Command Flags (\`/sc:index\`)` section (heading, table and trailing blank line). Check that no other link or anchor in `docs/` points at the deleted sections.

Acceptance criteria:
- `git grep -nE 'sc:index|index-repo|scindex' docs/user-guide` prints nothing.
- `docs/user-guide/commands.md` and `docs/user-guide/flags.md` have no doubled blank lines or empty section left at the removal points, and `git diff --check` is clean.

## Task 7: Remove the two commands from the generated contributor knowledge base lists

Depends on: Task 1

In `docs/generated/contributor-knowledge-base/architecture-guide.md` delete the bullets `- \`index.md\`` and `- \`index-repo.md\``; in `docs/generated/contributor-knowledge-base/components-guide.md` delete the same two bullets. Leave `docs/generated/contributor-knowledge-base/repository-overview.md` unchanged (its `PROJECT_INDEX.md` mention names a repository file that stays).

Acceptance criteria:
- `git grep -nE '`index(-repo)?\.md`' docs/generated/contributor-knowledge-base` prints nothing.
- The neighbouring command lists in both files still list every other command file.

## Task 8: Update the removed commands and the converted-command counts in the architecture reference

Depends on: Task 4

In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`: in the "Four layouts" item (d) list remove `index, index-repo` and change "20 commands" to 18; update the count statements to the values measured in the checkout after this PR: 25 of 38 command files carry `## Unattended mode` (13 in phase P1, 12 in P2; the folder then has 39 `.md` files including `README.md`), `UNATTENDED_EXPECT` has 25 keys, "25 converted commands" wherever the text says 28 converted commands, and the "P1 and P2 converted 31 commands; N remain" sentence says 25 remain. Measured before this PR: 27 of 40 command files carry the section, so the existing "28 of 41" text was already one behind after the cli-portify removal; the new numbers are measured, not decremented. The lines are around `:81`, `:196`, `:290`, `:317`, `:710`, `:745`, `:1315`, `:1319`, `:1321`, `:1958`, `:2197`, `:2230` (locate by text). Recount with `ls src/superclaude/commands/*.md | grep -v README | wc -l` and `grep -l '^## Unattended mode' src/superclaude/commands/*.md | wc -l` after Task 1 and use those numbers.

Acceptance criteria:
- `git grep -nE 'index-repo|\bindex, ' docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` prints nothing that names the removed commands.
- Every count statement above matches the recount commands run after Task 1 (38 command files without `README.md`, 25 with the section), and the arithmetic holds: sections plus the 8 barred names plus the 5 files with no section equals the command-file count.

## Phase 4: Update the tests

## Task 9: Update the routing-table test

Depends on: Task 2

In `tests/core/test_how_we_work_routing_table.py`: remove `"sc:index"` and `"sc:index-repo"` from `_OTHER_COMMANDS`; in the `document-built` assertion of `test_previews_documentation_and_suite_runs_disclose_actual_writes` (the set that holds `sc:document`, `sc:index`, `tech-reference`, `operational-guide`, `readme`) remove `"sc:index"`; in `test_other_operations_preserve_requested_authority_and_owned_state` remove the three assertions that pin `mode=quick or mode=update`, `PROJECT_INDEX.md and PROJECT_INDEX.json` and `Coordinated project docs/API/structure/README`, and update the docstring if it names a retired case.

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py -q` passes.
- `git grep -nE 'sc:index|index-repo|PROJECT_INDEX' tests/core` prints nothing.

## Task 10: Retire routing case S24 and update the routing-refresh test

Depends on: Task 2

In `tests/recommend/fixtures/routing_refresh_cases.json` delete the whole case object with `"id": "S24"` (request "Produce a compact repo map in quick mode.", with its repeat and variants); keep the `commands` records `index-repo` and `index` (frozen record). In `tests/recommend/test_routing_refresh.py`: add `"index"` and `"index-repo"` to `_POST_REFRESH_REMOVALS` (and extend its comment: removed in 6.0.0, the frozen record still lists them as active); change the case-id list in `test_fixture_schema_and_completeness` to skip 24 as well (`n not in (5, 7, 24, 25, 27)`, comment `# S05, S07, S24, S25, S27 retired`) and update the module docstring list of retired cases; delete the three lines in `test_flag_value_check_rejects_undeclared_enumerated_value` that read `index-repo.md` and check `mode=quick`/`mode=full` (the explain and tasklist checks keep the test meaningful); in `test_route_check_rejects_other_route_for_a_routed_command` replace the stand-in command `sc:index` with a command that stays and is named by a routing row step (for example `sc:document`), with the request text adjusted to match. The `formatting_only` list near the end of the commands test is derived from the frozen record and stays as it is.

Acceptance criteria:
- `uv run pytest tests/recommend -q` passes.
- `git grep -nE 'sc:index|S24' tests/recommend` prints nothing except the frozen `commands` records for `index` and `index-repo`.

## Task 11: Remove index-repo from the codegraph adoption test lists

Depends on: Task 1

In `tests/skills/test_codegraph_adoption.py` remove `"index-repo.md"` from `_ISSUE_504_COMMANDS` and from `_OWN_CHECK_COMMANDS` (the `analyze.md` and `document.md` entries stay).

Acceptance criteria:
- `uv run pytest tests/skills/test_codegraph_adoption.py -q` passes, and its parametrised case count drops by exactly the two removed `index-repo.md` cases.
- `git grep -n 'index-repo' tests/skills/test_codegraph_adoption.py` prints nothing.

## Task 12: Update the worker-contract test sets and counts

Depends on: Task 4

In `tests/skills/test_worker_contract.py`: remove `"index-repo"` and `"index"` from `P1_COMMANDS`, and the `"index-repo"` and `"index"` entries from `UNATTENDED_EXPECT`; change the comment "The fifteen commands" to "The thirteen commands"; in `_check_p1_set` (callers: `test_p1_command_set_is_complete`, `test_p1_set_check_fails_on_a_missing_extra_or_repeated_command`) change both counts and the message from 15 to 13; in `_check_p2_set` (callers: `test_p2_command_set_is_complete`, `test_p2_set_check_fails_when_a_command_file_is_missing`, `test_p2_set_check_fails_on_a_missing_extra_or_repeated_command`) change the `UNATTENDED_EXPECT` size check from 27 to 25 (message too); delete `test_index_repo_output_format_states_where_the_files_land`. Then run the file and fix any other count or name it pins for the two commands (search the file for `index` and for the numbers 15 and 27).

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -q` passes.
- `git grep -nE '"index(-repo)?"|index-repo\.md' tests/skills/test_worker_contract.py` prints nothing.

## Task 13: Remove the two commands from the installer test samples

Depends on: Task 1

In `tests/unit/test_cli_install.py`: remove `index-repo.md index.md` from the two sample listings (the one around line 116, the larger `commands` listing, and the one around line 400, the smaller `commands` listing); in `TestInstallCommands.test_list_available_commands` replace `assert "index-repo" in commands` with an assertion for a command that stays (`"agent"`); in `test_install_commands_to_temp_dir` replace the check for `index-repo.md` with `agent.md`; in `test_all_expected_commands_available` replace `"index-repo"` in `expected` with `"workflow"` (all of these commands exist in `src/superclaude/commands/`).

Acceptance criteria:
- `uv run pytest tests/unit/test_cli_install.py -q` passes.
- `git grep -nE 'index-repo|index\.md' tests/unit/test_cli_install.py` prints nothing.
