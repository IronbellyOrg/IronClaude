---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeThePrdComm-20261117-200005
version: "1"
priority: Medium
created_date: "2026-11-17"
---

# Remove the prd command-line pipeline (6.0.0, PR 1)

Source: ./source.md
Goal: `superclaude prd` no longer exists and `superclaude --help` does not list it, while the interactive `prd` skill still installs and no live file outside the historical records names the removed pipeline.

## Constraints

- The full reference table with line numbers is `.dev/cleanup/prd-cli/dependency-map.md`; every task below comes from it (sections A and B).
- Edit only under `src/superclaude/`, `tests/`, `docs/`, the two root `PROJECT_INDEX` files and the two `.dev/review-severity-rule/*.yaml` byte copies. The distributable source of truth is `src/superclaude/`; run `make sync-dev` for the mirrors and do not stage mirror output.
- Keep the interactive skill (`src/superclaude/skills/prd/`, `/prd`), the PRD templates and everything that treats a PRD as an input document (`roadmap`, `tasklist`, `tdd`, `--prd-file`).
- Do not edit historical records: `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries, and tracked `.dev/` working records other than the two yaml byte copies named in Task 5. Add no `CHANGELOG.md` entry.
- The three tests that fail at baseline (`tests/cli/eval/test_signal_handling.py::test_executor_without_cancel_logs_skipped`, `tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files`, `tests/swarm/test_imm3_parallel.py::test_imm3_sequential_baseline_speedup`) are not caused by this work and are not to be fixed here.

## Phase 1: Remove the command and its tests

## Task 1: Delete the prd package and its registration

Delete the directory `src/superclaude/cli/prd/` (15 files: `__init__.py`, `_artifact_patterns.py`, `commands.py`, `config.py`, `diagnostics.py`, `executor.py`, `filtering.py`, `gates.py`, `inventory.py`, `logging_.py`, `models.py`, `monitor.py`, `process.py`, `prompts.py`, `tui.py`). In `src/superclaude/cli/main.py` delete lines 539-541: the `from superclaude.cli.prd.commands import prd_group` line and `main.add_command(prd_group, name="prd")`, with the blank line that separates them from the neighbouring registrations kept tidy. `main.py:539-541` is the only import of the package in `src/`.

Acceptance criteria:
- `src/superclaude/cli/prd/` does not exist and `src/superclaude/skills/prd/` is unchanged.
- `uv run superclaude --help` does not list `prd`, and `uv run superclaude prd` exits non-zero with a "No such command" message.
- `git grep -n -E 'superclaude\.cli\.prd|prd_group' -- src` prints nothing.

## Task 2: Delete the prd command-line tests

Depends on: Task 1

Delete the directory `tests/cli/prd/` (17 files: `__init__.py` and `test_cli_smoke.py`, `test_config.py`, `test_e2e.py`, `test_executor.py`, `test_filtering.py`, `test_gates.py`, `test_integration.py`, `test_inventory.py`, `test_models.py`, `test_path_resolution.py`, `test_prompt_builders_dual_mode.py`, `test_prompts.py`, `test_research_notes_roundtrip.py`, `test_resolve_step_content.py`, `test_resume_skip.py`, `test_spec_flag.py`). These held 229 passing tests at baseline and no skips.

Acceptance criteria:
- `tests/cli/prd/` does not exist.
- `uv run pytest tests/cli --collect-only -q` collects no test id that starts with `tests/cli/prd/`.

## Phase 2: Keep the remaining tests valid

## Task 3: Drop prd from the top-level command roster test

Depends on: Task 1

In `tests/cli/test_cli_registration.py`, remove the `"prd",` entry (line 41) from `EXPECTED_TOP_LEVEL_COMMANDS`. `test_pre_existing_command_help_still_invokable` runs `<name> --help` for every entry, so the entry would fail once the command is gone.

Acceptance criteria:
- `uv run pytest tests/cli/test_cli_registration.py -q` passes.
- The frozen set still lists the other fourteen commands (`cleanup-audit`, `cli-portify`, `doctor`, `eval`, `init-lite`, `install`, `install-skill`, `mcp`, `recommend`, `roadmap`, `sprint`, `tasklist`, `update`, `version`).

## Task 4: Point the replay-executor test at a function that stays

Depends on: Task 1

In `tests/troubleshoot/backtest/test_replay_executor.py`, `test_backtest_resolve_callable_module_level_function` (around lines 79-92) imports `superclaude.cli.prd.gates` and resolves `_check_parallel_instructions`. Change it to `from superclaude.cli.pipeline import gates` and resolve `gate_passed` (module-level in `src/superclaude/cli/pipeline/gates.py`, parameters `output_file`, `criteria`, `envelope`, `repo_root`). Update the `qualname` assertion to `gate_passed` and the final signature assertion to check that `output_file` is a parameter; keep the assertions that the callable is not class-bound, has no owning class and has an `inspect.Signature`, and fix the nearby comment that says "one positional content param". Leave `test_backtest_e1.py`, `test_backtest_e2.py`, `test_backtest_e4.py` and the `replay_executor.py` docstrings as they are: their `superclaude.cli.prd` imports sit inside snippet strings run in a subprocess against an old checked-out commit, not against this tree.

Acceptance criteria:
- `uv run pytest tests/troubleshoot/backtest -q` passes with the same number of passed tests as before the edit (no test removed there).
- `git grep -n 'superclaude.cli.prd' -- tests/troubleshoot/backtest/test_replay_executor.py` prints nothing.

## Task 5: Remove the three severity-rule rows that point at removed files

Depends on: Task 1

Rows C-152 (file `src/superclaude/cli/prd/models.py`, line 203) in `tests/skills/fixtures/review_severity_cap_edits.yaml` (about lines 1256-1263; rows C-153 and later stay in group `prd-core`, so keep the `# --- prd-core` banner), and rows S-107 and S-108 (file `src/superclaude/cli/prd/prompts.py`) in `tests/skills/fixtures/review_severity_sweep_edits.yaml` (about lines 880-895), assert text inside the deleted package; `tests/skills/test_review_severity_rule.py` reads each row's file, so they would fail. Delete those three rows. In the header comment of the cap file (line 21) change `prd-core (cli/prd/models.py, rules/core/ib_agent_core.md)` to `prd-core (rules/core/ib_agent_core.md)`. Apply the identical edits to the two tracked byte copies `.dev/review-severity-rule/cap-edits.yaml` and `.dev/review-severity-rule/sweep-edits.yaml`, because `test_ej_fixtures_are_byte_copies_of_the_plan_tables` compares them byte for byte.

Acceptance criteria:
- `cmp tests/skills/fixtures/review_severity_cap_edits.yaml .dev/review-severity-rule/cap-edits.yaml` and the matching `cmp` for the sweep pair print nothing.
- Both fixtures still parse with `yaml.safe_load`; the cap file has 160 rows and the sweep file has 137.
- `git grep -n 'cli/prd' -- tests/skills/fixtures .dev/review-severity-rule/cap-edits.yaml .dev/review-severity-rule/sweep-edits.yaml` prints nothing.

## Task 6: Update the row counts the severity-rule test pins

Depends on: Task 5

In `tests/skills/test_review_severity_rule.py` change `assert len(rows) == 161` (line 281, `test_e_every_cap_edits_row_holds`) to 160 and `assert len(rows) == 139` (line 288, `test_j_every_sweep_edits_row_holds`) to 137.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_rule.py -q` passes, including `test_e_every_cap_edits_row_holds`, `test_j_every_sweep_edits_row_holds` and `test_ej_fixtures_are_byte_copies_of_the_plan_tables`.

## Task 7: Reword the reflect smoke-test docstring

Depends on: Task 2

In `tests/cli/reflect/test_cli_smoke.py`, the module docstring (line 3) says it "Mirrors `tests/cli/prd/test_cli_smoke.py`". Remove that sentence fragment and keep the rest (dry-run and print-command paths never construct `ClaudeProcess`, FR-12, asserted via `assert_not_called`).

Acceptance criteria:
- `git grep -n 'tests/cli/prd' -- tests/cli/reflect/test_cli_smoke.py` prints nothing and the docstring remains one valid sentence-complete paragraph.
- `uv run pytest tests/cli/reflect/test_cli_smoke.py -q` passes.

## Phase 3: Clean source primitives that name the pipeline

## Task 8: Remove the prd-output branch from the workspace-write hook

Depends on: Task 1

In `src/superclaude/hooks/scripts/reject-workspace-writes.sh` delete the FU-003 block (lines 39-62: the comment starting `# FU-003 defense-in-depth`, the `REL=` assignment, and the `if [[ "$REL" =~ ^(prd-[^/]+)... ]]` branch with its message, which names `superclaude prd run` and `src/superclaude/cli/prd/config.py`). Keep the skill-creator workspace branch above it and the final `exit 0`. Then run `make sync-dev` so the project mirror picks the script up (mirror files are gitignored and are not staged).

Acceptance criteria:
- `bash -n src/superclaude/hooks/scripts/reject-workspace-writes.sh` succeeds; the script ends with `exit 0`.
- Feeding it a JSON `tool_input.file_path` that is a skill-creator sibling-workspace path (a `<skill>-workspace/` folder inside a project's skills folder) on stdin exits 2 with the redirect message, and feeding it `{"tool_input":{"file_path":"/x/prd-demo/a.md"}}` exits 0.
- `make verify-sync` passes after `make sync-dev`; `uv run pytest tests/cli/test_install_hooks.py -q` passes.

## Task 9: Reword the eval orchestrator docstring

Depends on: Task 1

In `src/superclaude/cli/eval/orchestrator.py` the module docstring (lines 10-12) says the scheduler "mirrors the shape used by `src/superclaude/cli/prd/executor.py:774-802` so a reader switching between the PRD pipeline and the eval harness sees the same scheduling skeleton". Replace it with a statement that needs no removed file: the scheduler is `concurrent.futures.ThreadPoolExecutor` plus `as_completed` (the AC6 pattern the design spec pins). Do not change any code in the file.

Acceptance criteria:
- `git grep -n -E 'cli/prd|PRD pipeline' -- src/superclaude/cli/eval/orchestrator.py` prints nothing.
- `uv run pytest tests/cli/eval -q` has no new failures against the baseline (the baseline failure `test_executor_without_cancel_logs_skipped` is unrelated).

## Task 10: Make the reuse-auditor example name no removed pipeline

Depends on: Task 1

In `src/superclaude/agents/reuse-auditor.md` line 22 the motivating case reads "`prd`'s `_bind_specs` re-implementing the roadmap `_inject_*` post-LLM artifact-injection idiom". Reword it so it names no removed pipeline, for example "a pipeline's `_bind_specs` helper re-implementing ...", and keep the rest of the sentence. Leave lines 85 and 97 unchanged (they name only the function as a worked-example label). Run `make sync-dev` afterwards.

Acceptance criteria:
- Line 22 of the agent no longer contains the word `prd`; the rest of the file is byte-identical.
- `make verify-sync` passes.

## Phase 4: Update docs and indexes

## Task 11: Remove the headless CLI section from the prd skill release guide

Depends on: Task 1

In `docs/guides/prd-skill-release-guide.md` delete the subsection "### `superclaude prd` (headless CLI)" (heading at line 135 through its last bullet, line 147, "Run `superclaude prd run --help` ..."), together with its code block, leaving one blank line before the `---` rule that opens section 3. Do not touch the rest of the guide, which is about the skill.

Acceptance criteria:
- `git grep -n 'superclaude prd' -- docs/guides/prd-skill-release-guide.md` prints nothing.
- The text before the removed section ends with the skill examples block and the file still has its "3) The 7-Phase Multi-Agent Pipeline" heading.

## Task 12: Update the review-severity developer guide

Depends on: Task 5

In `docs/developer-guide/review-severity-rule.md` delete the table row `| prd CLI | Research and synthesis fix cycles default to 2 | src/superclaude/cli/prd/models.py:203-204 |` (line 69). In the row at line 94 change "161 cap-edit or 139 sweep-edit rows" to "160 cap-edit or 137 sweep-edit rows". Leave the `prd, tdd, ... skills` row at line 68 (it is about the skills).

Acceptance criteria:
- `git grep -n -E 'prd CLI|cli/prd' -- docs/developer-guide/review-severity-rule.md` prints nothing.
- The file contains "160 cap-edit or 137 sweep-edit rows" and the table above it still renders (every row keeps three cells).

## Task 13: Remove prd from the technical-architecture pipeline list

Depends on: Task 1

In `docs/developer-guide/technical-architecture.md` line 315 (the "What Runs Code" bullet), remove `prd`, from the list "`sprint`, `roadmap`, `tasklist`, `eval`, `swarm`, `reflect`, `prd`, `cli-portify` and `cleanup-audit`" so it reads "`sprint`, `roadmap`, `tasklist`, `eval`, `swarm`, `reflect`, `cli-portify` and `cleanup-audit`". Change nothing else in the bullet.

Acceptance criteria:
- `git grep -n -w 'prd' -- docs/developer-guide/technical-architecture.md` prints nothing on line 315.

## Task 14: Remove prd from the project index files

Depends on: Task 1

In `PROJECT_INDEX.json` remove `"prd"` from the CLI `groups` list (line 46) and from the `cli` `subpackages` list (line 94); leave the skills list on line 110, which names the skill. In `PROJECT_INDEX.md` remove `` `prd` `` from the Groups line (line 36); leave line 75, which names the skill.

Acceptance criteria:
- `python -c "import json; json.load(open('PROJECT_INDEX.json'))"` run through `uv run` succeeds.
- `git grep -n '"prd"' -- PROJECT_INDEX.json` prints one line only (the skills list) and `git grep -n -F '`prd`, `eval`' -- PROJECT_INDEX.md` prints nothing.
