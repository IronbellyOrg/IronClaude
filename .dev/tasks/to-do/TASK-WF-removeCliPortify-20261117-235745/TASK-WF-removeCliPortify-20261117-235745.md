---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeCliPortify-20261117-235745
version: "1"
priority: Medium
created_date: "2026-11-17"
---

# Remove cli-portify (IronClaude 6.0.0, PR 4 of issue 571)

Source: ./source.md
Goal: cli-portify (the `superclaude cli-portify` command group, `/sc:cli-portify` and the `sc-cli-portify-protocol` skill) is gone from the installed surface and from every kept file, while every kept module still imports and passes its tests.

## Constraints

- The line-by-line list of references is `.dev/cleanup/cli-portify/dependency-map.md`; each task below names its files from that map and from `git grep -i portify`.
- Source of truth is `src/superclaude/`; mirrors come from `make sync-dev`. Never stage the gitignored mirror folders of `.claude/` (only `.claude/settings.json` is tracked).
- Keep `src/superclaude/cli/pipeline`, `reflect`, swarm, `src/superclaude/cli/audit`, the eval harness and `/sc:implement`. No kept module imports `cli_portify` (checked with codegraph and `git grep`); if one is found, stop and tell the orchestrator.
- Do not edit historical records: `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries, and `.dev/` work records. Do not add a `CHANGELOG.md` entry.
- The routing guide exists in two copies (`src/superclaude/core/HOW-WE-WORK.md` and `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`) and they must stay byte-identical.
- Use `uv run` for every Python command.

## Phase 1: Delete the removed surface

## Task 1: Delete the cli_portify package, its tests and its registration

Delete the directory `src/superclaude/cli/cli_portify/` (including `steps/`) and the directory `tests/cli_portify/` (including `integration/` and `fixtures/`). In `src/superclaude/cli/main.py` remove the import at line 537 (`from superclaude.cli.cli_portify.commands import cli_portify_group`, with its `noqa` comment) and `main.add_command(cli_portify_group)` at line 539. `main.py` is the only importer of the package in `src/`; the other callers codegraph lists are in the deleted `tests/cli_portify/test_cli.py`.

Acceptance criteria:
- `uv run superclaude --help` does not list `cli-portify` and `uv run python -c "import superclaude.cli.main"` succeeds.
- `git grep -n cli_portify -- src/superclaude --  ':!src/superclaude/skills/sc-cli-portify-protocol'` prints no Python import of the package.

## Task 2: Delete the /sc:cli-portify command, the sc-cli-portify-protocol skill and the classifier key

Delete `src/superclaude/commands/cli-portify.md` and the directory `src/superclaude/skills/sc-cli-portify-protocol/` (`SKILL.md`, `__init__.py`, `decisions.yaml`, `refs/analysis-protocol.md`, `refs/code-templates.md`, `refs/pipeline-spec.md`). Run `make sync-dev`, then delete the stale untracked mirror copies of that command and that skill from the gitignored `.claude` mirror folders by hand (sync-dev copies but never deletes). In `src/superclaude/cli/recommend/prompts.py` remove the `"cli-portify"` entry at line 38 from `CLASSIFICATION_KEYS` and its description line at line 68 from `CLASSIFIER_PROMPT`.

Acceptance criteria:
- Neither `src/superclaude/commands/cli-portify.md` nor `src/superclaude/skills/sc-cli-portify-protocol/` exists, and `uv run python -c "from superclaude.cli.recommend.prompts import CLASSIFICATION_KEYS; assert 'cli-portify' not in CLASSIFICATION_KEYS"` succeeds.
- `make verify-sync` stays green.

## Task 3: Delete the portify guide and the staleness checker

Delete `docs/guides/cli-portify-and-pipeline-runner-guide.md` (the whole guide is about portify and nothing links to it) and `scripts/check-ref-staleness.py` (it only compares the portify skill refs with `src/superclaude/cli/pipeline/models.py` and `gates.py`; nothing calls it).

Acceptance criteria:
- `git grep -n "check-ref-staleness\|cli-portify-and-pipeline-runner-guide" -- . ':!.dev'` prints nothing.

## Phase 2: Routing guide, worker contract and templates

## Task 4: Remove the portify rows from the routing guide, both copies

Depends on: Task 2

In `src/superclaude/core/HOW-WE-WORK.md` delete the routing row 'Workflow-to-CLI specification' (line 254) and the `cli-portification-spec` row (line 380), and in the bullet 'Portification and optional referrals' (line 267) drop the portify sentence and keep the referral sentences that stay true (rename the bullet to 'Optional referrals'). Copy the file byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (same lines 254, 267, 380). `src/superclaude/core/CLAUDE.md` names no portify; leave it unless a level-table copy changes.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` reports no difference and neither file contains `portif`.

## Task 5: Remove cli-portify from the worker contract

In `src/superclaude/core/WORKER-CONTRACT.md` drop `cli-portify` from the list of converted commands at line 330 and change '13 commands' to '12 commands'; in line 334 change 'four P2 commands with a required brief flag' (listing `/sc:auggie-review`, `/sc:cli-eval`, `/sc:cli-portify`, `/sc:spec-panel`) to three commands without `/sc:cli-portify` and 'it has 16 rows' to 15 rows; delete the table row at line 343. Any other count the file gives for this set must follow (read lines 325 to 350 and fix each).

Acceptance criteria:
- `src/superclaude/core/WORKER-CONTRACT.md` contains no `portif` and its counts agree with its table (15 rows).

## Task 6: Reword the release-spec template note in both template copies

In `src/superclaude/templates/documents/release-spec-template.md` (line 244) and `src/superclaude/examples/release-spec-template.md` (line 248) replace 'Auto-populated by `sc:cli-portify` Phase 3c embedded brainstorm pass. For manually created specs, use `/sc:brainstorm` to identify gaps.' with 'Use `/sc:brainstorm` to identify gaps.' Run `make sync-dev` to refresh the template mirror.

Acceptance criteria:
- Both files contain no `portif` and differ from each other only as they did before.

## Phase 3: Documentation

## Task 7: Remove cli-portify from the user guide and the architecture overview

In `docs/user-guide/commands.md` delete the table row at line 60 and the whole section `### /sc:cli-portify - Workflow to CLI Pipeline Port` (lines 216 to 231, up to and including its closing `---`). In `docs/developer-guide/technical-architecture.md` line 315 remove `cli-portify` from the list of `superclaude` CLI commands (fix the 'and' wording of the list).

Acceptance criteria:
- Neither file contains `portif`, and the commands.md table and section separators stay well formed.

## Task 8: Remove the portify rows from the review-severity rule, its fixture and its test pin

In `docs/developer-guide/review-severity-rule.md` delete the B4 row (line 48), the `/sc:cli-portify` table row (line 70) and the `--max-convergence` bullet (line 104). In `tests/skills/fixtures/review_severity_cap_edits.yaml` delete the 20 rows with group `portify` (ids C-132 to C-151, lines 1093 to 1203) and the `portify` group text and cli_portify mentions in the header comment (lines 20 and 21, and line 4 if it names cli-portify). Apply the identical edit to the byte-twin `.dev/review-severity-rule/cap-edits.yaml` (the test `test_ej_fixtures_are_byte_copies_of_the_plan_tables` compares the two; this is a plan table pinned by a test, not a narrative record). In `tests/skills/test_review_severity_rule.py` change `assert len(rows) == 160` (line 281) to 140.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_rule.py -q` passes.
- The fixture and `.dev/review-severity-rule/cap-edits.yaml` are byte-identical and contain no `portif`.

## Task 9: Replace the /sc:cli-portify example in the maintainer rule

In `CLAUDE.md` line 97 and in `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` line 114 the rule that allows `src/superclaude/...` paths names `/sc:cli-portify` as the example of a command that works on this repo's own source by design. Remove that example, keeping the rest of each sentence correct (the clause then reads 'commands that operate on this repo's own source by design').

Acceptance criteria:
- Neither file contains `portif` and both sentences still read as complete English.

## Task 10: Remove cli-portify from the supervised-orchestration technical reference

In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` edit lines 1315, 1318, 1840 and 1989: drop cli-portify from each list of converted commands and fix every count or sentence that depended on it (read each line first; keep wording that describes other commands).

Acceptance criteria:
- The file contains no `portif` and no count in those four lines disagrees with Task 5.

## Task 11: Remove cli-portify from the generated guides and the project index

Delete the line or sentence naming it in `docs/generated/contributor-knowledge-base/architecture-guide.md` (line 256), `docs/generated/contributor-knowledge-base/components-guide.md` (line 184), `docs/generated/sprint-cli/04-gates-validation.md` (line 198) and `docs/generated/sprint-cli/07-skills-commands.md` (line 181, the `cli_portify/resolution.py` entry and its body up to the next entry). In `PROJECT_INDEX.md` remove `cli-portify` (line 36) and `cli_portify/` (lines 68 and 97) from the lists; in `PROJECT_INDEX.json` remove `"cli-portify"` (line 46) and `"cli_portify"` (line 94).

Acceptance criteria:
- None of the six files contains `portif`, and `PROJECT_INDEX.json` still parses with `uv run python -c "import json; json.load(open('PROJECT_INDEX.json'))"`.

## Phase 4: Tests that stay

## Task 12: Retire the portify routing cases

Depends on: Task 4

In `tests/core/test_how_we_work_routing_table.py` remove the id `cli-portification-spec` from `_EXPECTED_IDS`, `"sc:cli-portify"` from the set at line 299, the `S11` case tuple at lines 681 to about 695, and the three portify assertions at lines 879 to 881 (keep the rest of that test). In `tests/recommend/fixtures/routing_refresh_cases.json` delete case `S11` (lines 220 to 242); keep the frozen command row `cli-portify` at line 678 (earlier removals kept their frozen rows). In `tests/recommend/test_routing_refresh.py` update the docstring and the id list so `S11` is retired (as `S05` was) and add `"cli-portify"` to `_POST_REFRESH_REMOVALS`; check the `T` checks and contract-gap `C04` entries of the fixture for any use that depended on `S11`.

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/recommend -q` passes.

## Task 13: Remove cli-portify from the worker-contract tests

Depends on: Task 5

In `tests/skills/test_worker_contract.py` remove `"cli-portify"` from `P2_COMMANDS` (line 499), delete its `UNATTENDED_EXPECT` entry (lines 669 to 683), remove it from `P2_NEW_BRIEF_ROWS` (line 970) and delete its `P2_GATES` row (the tuple at about line 1771). Change the pins in `_check_p2_set` to 12 commands for P2 and 27 for `UNATTENDED_EXPECT`, and any 'four' or '16 rows' pin to three and 15 (search the file for these numbers).

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -q` passes.

## Task 14: Update the registration, install and classifier tests

Depends on: Task 2

In `tests/cli/test_cli_registration.py` remove `"cli-portify"` from `EXPECTED_TOP_LEVEL_COMMANDS` (line 33). In `tests/unit/test_cli_install.py` remove `cli-portify.md` from the commands list (line 115) and the five `sc-cli-portify-protocol/...` entries from the skills list (lines 228 to 232), and reword the docstring at line 801 so it no longer cites `cli-portify/resolution.py`. In `tests/skills/test_sc_recommend_routing_contract.py` remove `"cli-portify"` from the expected `CLASSIFICATION_KEYS` tuple (line 280).

Acceptance criteria:
- `uv run pytest tests/cli/test_cli_registration.py tests/unit/test_cli_install.py tests/skills/test_sc_recommend_routing_contract.py -q` passes.

## Task 15: Drop the PortifyProcess tests from the pipeline stdin test file

Depends on: Task 1

In `tests/pipeline/test_process_stdin.py` remove the import of `PortifyProcess` (line 19), the class `TestPortifyAnchor` (lines 41 to 117 including its section comment), any helper or import that becomes unused (`patch`, `_stdin_echo_argv`, check each with a search), and the word PortifyProcess from the module docstring. The `ClaudeProcess` tests stay.

Acceptance criteria:
- `uv run pytest tests/pipeline/test_process_stdin.py -q` passes and `uv run ruff check tests/pipeline/test_process_stdin.py` reports nothing.

## Task 16: Rename the portify fixture in the wiring-audit test

In `tests/audit/test_wiring_integration.py` rename the fixture `cli_portify_fixture` (definition at line 29 and every use at lines 81 to 132) to `noop_step_runner_fixture`, and reword the module docstring and the fixture docstring (lines 1 to 12 and 30) so they describe the `step_runner: Optional[Callable] = None` no-op pattern without naming cli-portify or `PortifyExecutor`. The test still exercises `analyze_unwired_callables` and `run_wiring_analysis` in `src/superclaude/cli/audit/wiring_gate.py`.

Acceptance criteria:
- `uv run pytest tests/audit/test_wiring_integration.py -q` passes and the file contains no `portif`.

## Task 17: Rename the portify regression cases in the roadmap tests

In `tests/roadmap/test_fingerprint.py` (lines 9, 93, 108, 305 to 326), `tests/roadmap/test_integration_contracts.py` (lines 7, 98, 114, 281 to 360), `tests/roadmap/test_obligation_scanner.py` (lines 8, 84, 334 to 350) and `tests/roadmap/test_anti_instinct_integration.py` (lines 8, 127 to 133) rename `CLI_PORTIFY_SPEC`, `CLI_PORTIFY_BAD_ROADMAP`, `CLI_PORTIFY_REGRESSION`, the classes `TestCliPortifyRegression` and the method `test_t5_cli_portify_regression_still_blocks` to dispatch-table names (`DISPATCH_TABLE_SPEC`, `DISPATCH_TABLE_BAD_ROADMAP`, `DISPATCH_TABLE_REGRESSION`, `TestDispatchTableRegression`, `test_t5_dispatch_table_regression_still_blocks`) and reword the comments that say 'cli-portify regression' to 'dispatch-table regression'. In `tests/roadmap/test_parser_consistency.py` lines 216 to 218 delete the assertion on `cli_portify/utils.py` and reword the comment so it names only the audit parser. In `tests/roadmap/fixtures/recurrence/retry_contract/retry_loop_no_terminal_case.md` (line 17) and `retry_loop_no_terminal_case.expected.json` (line 6) replace `v2.24-cli-portify` with `v2.24` if no test pins the exact text (search for the fixture name first; if one does, change both sides together). In `KNOWLEDGE.md` line 185 change `TestCliPortifyRegression.*` to `TestDispatchTableRegression.*`. These roadmap tests stay until the roadmap removal PR; only names and text change.

Acceptance criteria:
- `uv run pytest tests/roadmap -q` passes with the same pass count as before the rename for these files.
- The files in this task contain no `portif`.

## Phase 5: Scripts and final sweep

## Task 18: Remove the portify releases from the fidelity batch scripts and sweep for leftovers

In `scripts/run-fidelity-batch.sh` delete the entries at lines 33 and 34 (`v2.24-cli-portify-cli-v4` and `v2.24.1-cli-portify-cli-v5`) and fix the comment that gives the release count and batch count (10 releases in 5 batches becomes 8 in 4). In `scripts/run-fidelity-batch-refactored.sh` delete the same two releases (lines 30 to 31, the two `"$SETUP"` lines at 62 and 76, and the report entries at 134 to 135), renumber the batch comments and waits that follow, and keep the script syntactically valid.

Acceptance criteria:
- `bash -n scripts/run-fidelity-batch.sh` and `bash -n scripts/run-fidelity-batch-refactored.sh` succeed.
- `git grep -il portify -- . ':!docs/releases' ':!docs/testing/v5.0.0' ':!docs/designs' ':!.dev' ':!CHANGELOG.md'` lists only the frozen records named in the Constraints and the retired-name entries in `tests/recommend/test_routing_refresh.py` and `tests/recommend/fixtures/routing_refresh_cases.json`.
- `uv run superclaude --help` does not list `cli-portify`, and `uv run pytest -n auto --ignore=tests/cli/test_verify_sync_hooks.py` shows 0 new failures against the baseline in `.dev/issues/v6-cli-portify/`.
