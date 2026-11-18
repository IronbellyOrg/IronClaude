---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeTheRoadmap-20261118-003614
version: "1"
priority: High
created_date: "2026-11-18"
---

# Remove the roadmap, tasklist and sprint family (IronClaude 6.0.0, PR 11)

Source: ./source.md
Goal: `superclaude roadmap`, `superclaude tasklist` and `superclaude sprint`, the commands `/sc:roadmap`, `/sc:validate-roadmap` and `/sc:tasklist`, and the skills `sc-roadmap-protocol`, `sc-validate-roadmap-protocol` and `sc-tasklist-protocol` are gone from source, mirrors, install lists, tests and docs, while every kept item still installs and its tests pass.

## Constraints

- Source of truth is `src/superclaude/`. Run `make sync-dev` for the `.claude/` mirrors. Never stage `.claude/` except `.claude/settings.json`. Stage `.dev/tasks` (it is always staged).
- Dependency map with every path:line: `.dev/cleanup/roadmap-family/dependency-map.md`. Baseline counts: `.dev/issues/v6-roadmap-family/BASELINE.md` (26702 passed, 178 skipped, 1 load-only failure).
- What STAYS: the plain `roadmap` skill (`src/superclaude/skills/roadmap/`, including its own `.roadmap-state.json` use and `src/superclaude/templates/documents/roadmap_template.md`), the skills `task`, `task-builder`, `tdd`, `prd`, `readme`, `tech-reference`, `tech-research`, `operational-guide`, `/sc:workflow`, `/sc:implement`, `/sc:task`, `/sc:tdd`, `cli/pipeline`, reflect, swarm, `cli/audit`, the eval harness, ccsession, observe, sweep and issue_watch.
- Do not edit historical records: `.dev/` (except this package and `.dev/issues`, `.dev/cleanup`), `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, `docs/memory/`, past `CHANGELOG.md` entries, past `KNOWLEDGE.md` entries. Do not add a `CHANGELOG.md` entry.
- If a kept source module (not a test) turns out to import a removed package, stop and report the import line; do not rewrite kept modules to make the removal fit.
- Installed primitives never name a `src/superclaude/...` path; when rewording, use installed paths.
- No subagents: every skill step runs inline.

## Phase 1: Remove the runners, commands, skills and their code

## Task 1: Delete the three runner packages, `compression.py` and the registrations

Delete the directories `src/superclaude/cli/roadmap/`, `src/superclaude/cli/tasklist/` and `src/superclaude/cli/sprint/`, and the files `src/superclaude/compression.py` and `scripts/compress.py`. In `src/superclaude/cli/main.py` remove the three deferred imports and the three `main.add_command(...)` calls for `sprint_group`, `roadmap_group` and `tasklist_group` (lines 525-535 at the time of writing), including the comment block above them if it only explains those three.

Dependents (from the dependency map section 1): `cli/main.py` is the only kept source module that imports the three packages; `compression.py` is imported only by `cli/roadmap/executor.py` and `scripts/compress.py`; `cli/sprint/aienv.py` imports `swarm.config` and goes with sprint.

Acceptance criteria:
- `grep -rn "superclaude.cli.sprint\|superclaude.cli.roadmap\|superclaude.cli.tasklist\|superclaude.compression" src/` finds no import statement.
- `uv run superclaude --help` lists no `roadmap`, `tasklist` or `sprint` command, and still lists `eval`, `swarm`, `recommend`, `reflect`, `sweep`, `observe` and the install commands.
- `uv run python -c "import superclaude.cli.main"` succeeds.

## Task 2: Delete the three commands, three skills and their templates and eval suite

Depends on: Task 1

Delete `src/superclaude/commands/roadmap.md`, `src/superclaude/commands/validate-roadmap.md`, `src/superclaude/commands/tasklist.md`; the skill folders `src/superclaude/skills/sc-roadmap-protocol/`, `src/superclaude/skills/sc-validate-roadmap-protocol/`, `src/superclaude/skills/sc-tasklist-protocol/`; the template files `src/superclaude/examples/roadmap_template.md`, `roadmap_template.compressed.md`, `tasklist_index_template.md`, `tasklist_phase_template.md`; the plugin template folder `plugins/superclaude/templates/roadmaps/` (6 files); and the eval suite `src/superclaude/cli/eval/suites/tasklist_deterministic_shape.yaml`. Keep `src/superclaude/templates/documents/roadmap_template.md` (the plain `roadmap` skill reads it) and the plain skill `src/superclaude/skills/roadmap/`.

Acceptance criteria:
- None of those paths exists in `git ls-files`.
- `src/superclaude/skills/roadmap/SKILL.md` and `src/superclaude/templates/documents/roadmap_template.md` are unchanged by this task.
- If `plugins/superclaude/templates/` becomes empty, the folder is removed and `scripts/build_superclaude_plugin.py` does not fail on the missing folder (checked by reading the script for `templates`).

## Task 3: Delete the scripts that only drive the removed pipelines

Depends on: Task 1

Delete `scripts/eval_1.py`, `scripts/eval_2.py`, `scripts/eval_3.py` (drive `superclaude roadmap run` and import `cli.roadmap`), `scripts/eval_runner.py` and `tests/unit/test_eval_runner_master_checkout.py` (the runner only runs `tests/roadmap/test_eval_*.py` and those three scripts), `scripts/fidelity-check-setup.sh`, `scripts/run-fidelity-batch.sh`, `scripts/run-fidelity-batch-refactored.sh` (call `superclaude roadmap run`), `scripts/rerun-incomplete-phases.sh` (calls `superclaude sprint run`), and `scripts/smoke-test-v2.sh` (greps `cli/sprint` and `cli/roadmap` source). Remove their rows from `scripts/README.md`. In `scripts/dependency_baseline.txt` reword the comment at line 71 that cites `src/superclaude/cli/roadmap/tool_writer.py`.

Acceptance criteria:
- None of the deleted scripts exists; no kept file names them (`git grep` for each basename outside the historical records is empty).
- `scripts/README.md` lists only scripts that exist.
- `make verify-deps` still passes (the dependency allow-list is unchanged except for the comment).

## Phase 2: Remove their tests and trim kept tests

## Task 4: Delete the test folders and files that cover only removed code

Depends on: Task 3

Delete the folders `tests/roadmap/`, `tests/sprint/`, `tests/tasklist/`, `tests/sc-roadmap/`, `tests/v3.3/`, `tests/troubleshoot/fixtures/procedures/tasklist/`; the files `tests/test_sc_roadmap_refactor.sh`, `tests/integration/test_sprint_wiring.py`, `tests/integration/test_wiring_e2e_shadow.py`, `tests/cli/test_tdd_extract_prompt.py`, `tests/cli/eval/test_isolation_layers_probe.py`, `tests/cli/eval/test_phase_report_probe.py`. Before deleting `tests/v3.3/` and `tests/troubleshoot/fixtures/procedures/tasklist/`, confirm with `git grep` and codegraph that no kept test or source reads them, and keep any file that a kept test still uses.

Acceptance criteria:
- `pytest --collect-only -q` reports no collection error.
- The summed test count removed is recorded in `.dev/issues/v6-roadmap-family/` for the before/after comparison.

## Task 5: Trim the kept test files that import or read removed code

Depends on: Task 4

Remove only the cases and imports that depend on removed code, in each kept file: `tests/pipeline/test_full_flow.py` (imports from `cli.sprint.models` and `cli.sprint.executor` at lines 39 and 345-360 and 472, with the test sections that use them), `tests/pipeline/test_trailing_gate.py` (the `SprintGatePolicy` cases around lines 558-607), `tests/pipeline/test_process.py` (the case at line 243), `tests/cli/eval/test_home_isolation_extend.py` (the cases `test_isolation_layers_probe_still_passes_after_extension` and `test_home_isolation_env_does_not_collide_with_isolation_layers_keys`), `tests/swarm/test_module_shape.py` (drop the sprint-parity half: keep the swarm-only file and package checks, remove the checks that read `src/superclaude/cli/sprint/`), `tests/unit/test_cli_install.py` (the `cli.roadmap.templates` import at line 35, the expected-file lists naming `sc-roadmap-protocol`, `sc-tasklist-protocol`, `sc-validate-roadmap-protocol` and the four example templates, and the cases that assume `sc-roadmap-protocol` exists at lines 706 and 766), `tests/unit/test_cli_doctor.py` (the fixture at lines 50-52 that writes a `roadmap` command and `sc-roadmap-protocol` skill: use another kept command and skill), `tests/cli/eval/test_single_command.py` (comment at line 35), `tests/troubleshoot/backtest/git_replay.py` (comment at line 3), `tests/cli/reflect/test_no_nesting_guard.py` (reword the guard text at lines 39 and 128 to the generic rule; keep the guard).

Acceptance criteria:
- Each edited file passes `uv run pytest <file>` and `ruff check` / `ruff format --check`.
- No kept test file contains `superclaude.cli.sprint`, `superclaude.cli.roadmap` or `superclaude.cli.tasklist` as an import.
- The list of trimmed cases and their count goes into `.dev/issues/v6-roadmap-family/` so the pass-count drop is explained.

## Phase 3: Fix the kept source, commands, skills and routing

## Task 6: Reword the comments in kept source modules that name the removed packages

Depends on: Task 1

Reword (comments and docstrings only, no code change) in: `src/superclaude/cli/pipeline/` (the NFR-007 note and `cli/roadmap/...` pointers in `combined_m2_pass.py`, `conflict_detector.py`, `conflict_review.py`, `contract_extractor.py`, `dataflow_graph.py`, `dataflow_pass.py`, `diagnostic_chain.py`, `executor.py`, `fmea_classifier.py`, `fmea_domains.py`, `fmea_promotion.py`, `gates.py`, `guard_analyzer.py`, `guard_pass.py`, `guard_resolution.py`, `invariant_pass.py`, `invariants.py`, `models.py`, `mutation_inventory.py`, `process.py`, `state_detector.py`, `trailing_gate.py`, `verification_emitter.py`), `src/superclaude/cli/reflect/config.py`, `models.py`, `runner.py`, `src/superclaude/cli/swarm/__init__.py`, `config.py`, `models.py`, `tmux.py`, `transports/__init__.py` (swarm stays; drop the "mirrors cli/sprint" claim), `src/superclaude/cli/eval/isolation.py`, `eval/reporter.py`, `src/superclaude/cli/install_skills.py` (use another example than `sc-roadmap-protocol`), `src/superclaude/cli/recommend/commands.py`, `recommend/models.py`, `recommend/cache.py`, and `src/superclaude/contracts/__init__.py` (remove or reword the `cli/roadmap/...` citations and the `"sc:roadmap"` threshold entry only if no kept code or test reads it; read the file and its callers first).

Acceptance criteria:
- `git diff` for these files shows only comment, docstring or constant-table changes; `uv run pytest tests/pipeline tests/cli/reflect tests/swarm tests/recommend tests/contracts` passes.
- `grep -rn "cli.sprint\|cli.roadmap\|cli.tasklist\|cli/sprint\|cli/roadmap\|cli/tasklist" src/superclaude --include=*.py` finds nothing.

## Task 7: Update kept commands, skills, agents and templates that name the removed items

Depends on: Task 2

Edit the removed-item mentions in: `src/superclaude/skills/sc-crash-recovery/SKILL.md` (lines 116-118), `refs/pipelines.md` (the roadmap, tasklist and sprint pipeline sections and their resume commands), `refs/report-template.md` (resume commands at lines 84-109), `refs/investigators.md` (lines 19 and 35; keep the `.roadmap-state.json` scan, the plain `roadmap` skill still writes it); `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (the sprint-failure recovery hint at line 525); `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (consumer rows at lines 998-1001 and the sprint mentions at 1430-1446 and 1520); `src/superclaude/commands/workflow.md` and `src/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md` (the `/sc:tasklist` and `/sc:roadmap` rows and the "run `superclaude roadmap`" text), `plugins/superclaude/commands/workflow.md`, `plugins/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md`; `src/superclaude/commands/brainstorm.md`, `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` and `refs/handoff-routing.md` (the `--handoff tasklist` choice and the `sc-tasklist-protocol` invocation; keep `none`, `design` and `task`), `plugins/superclaude/commands/brainstorm.md`; `src/superclaude/commands/spec-panel.md` and `plugins/superclaude/commands/spec-panel.md` (the downstream-roadmap frontmatter lines 38 and 40 and the table rows at 405-406); `src/superclaude/commands/release-split.md`, `src/superclaude/skills/sc-release-split-protocol/SKILL.md` and `refs/adversarial-integration.md`; `src/superclaude/commands/adversarial.md` and `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` (the `/sc:roadmap` integration rows); `src/superclaude/skills/sc-implement-protocol/SKILL.md` line 210 and `plugins/superclaude/skills/sc-implement-protocol/SKILL.md`; `src/superclaude/skills/sc-issue-protocol/refs/chains.md` line 24; `src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md` and its plugin copy; `src/superclaude/agents/rf-qa.md` and `src/superclaude/skills/task-builder/SKILL.md` (the "imported from sc:tasklist check N" provenance text; keep the checks themselves); `src/superclaude/examples/tdd_template.md`, `src/superclaude/examples/release-spec-template.md`, `src/superclaude/templates/documents/release-spec-template.md` (the "computed by sc:roadmap" and "For sc:roadmap / For sc:tasklist" text); `src/superclaude/core/RULES.md` line 64 and `plugins/superclaude/core/RULES.md` (the `superclaude sprint run --help` example: use a kept CLI).

Acceptance criteria:
- No file in this list still contains `/sc:roadmap`, `sc:roadmap`, `/sc:tasklist`, `sc:tasklist`, `sc-tasklist-protocol`, `sc-roadmap-protocol`, `/sc:validate-roadmap`, `superclaude sprint`, `superclaude roadmap` or `superclaude tasklist`, except where a kept check names a historical provenance that the edit rewords.
- The plain `roadmap` skill (`/roadmap`) is still described correctly wherever a row mentioned both.
- `uv run pytest tests/skills tests/commands tests/agents` passes after Task 8 updates the pinned tests.

## Task 8: Update the routing guide, worker contract, core guide and the tests that pin them

Depends on: Task 7

Edit `src/superclaude/core/HOW-WE-WORK.md` (lines 256-258, 296, 381-383: remove the release-pipeline roadmap, Sprint tasklist bundle and roadmap-fidelity rows and the `/sc:roadmap` text in the `/roadmap` row) and copy it byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; re-run the level-table copy into `src/superclaude/core/CLAUDE.md` and reword line 38 (`docs/generated/` as a roadmap pipeline directory); in `src/superclaude/core/WORKER-CONTRACT.md` line 330 remove `tasklist` from the list of 12 commands and fix the count and any list of command names the guard test reads. Update the tests that pin counts and rows: `tests/core/test_how_we_work_routing_table.py` (lines 301, 706, 713, 725), `tests/recommend/fixtures/routing_refresh_cases.json` (cases at lines 233 and 268-325) and `tests/recommend/test_routing_refresh.py` (line 620), `tests/commands/test_workflow_command.py` (lines 231-238), `tests/hooks/test_launch_level_guard.py` (line 937 parameter list), `tests/skills/test_codegraph_adoption.py` (lines 18 and 27), `tests/skills/test_primitive_dual_surface_lookup.py` (lines 19-20), `tests/skills/test_task_builder_merge.py` (the `sc-tasklist-protocol` checks at lines 28-31 and 548-590 and the provenance text at 131-142), `tests/skills/test_worker_contract.py` (line 760 list), `tests/skills/fixtures/review_severity_sweep_edits.yaml` (the `tasklist` entries at lines 29 and 961-1049), `tests/review/test_reflect_consumer_inventory.py` and `scripts/reflect_consumer_inventory.py` (the consumer rows for `sc-roadmap-protocol`, `sc-tasklist-protocol` and `cli/sprint/executor.py`). Read each pinned count (commands, skills, routing rows, unattended commands) from its test before editing and set it to the new real value, not a guess.

Acceptance criteria:
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- `uv run pytest tests/core tests/recommend tests/commands tests/hooks tests/skills tests/review tests/unit` passes with every pinned count equal to the real count.
- Each removed routing row has no remaining test fixture asking for it.

## Phase 4: Docs, index and root files

## Task 9: Delete the docs for the removed items and fix the kept docs

Depends on: Task 2

Delete `docs/analysis-sc-tasklist.md`, `docs/sprint-budget-architecture.md`, `docs/sprint-cli-deep-dive.md`, `docs/developer-guide/sprint-tui-reference.md`, `docs/guides/roadmap-cli-tools-release-guide.md`, `docs/guides/sprint-cli-tools-release-guide.md` and the folder `docs/generated/sprint-cli/`. Edit the kept docs named in the dependency map section 4 and 5: `docs/user-guide/commands.md` (table rows at 42, 43, 73 and the three command sections at 548-577, 667-712, 714-745 and the brainstorm line 828), `docs/user-guide/flags.md` (sprint rows 239-245; check lines 89 and 121 before editing), `docs/user-guide/brainstorm.md`, `docs/user-guide/codegraph.md`, `docs/user-guide/session-management.md`, `docs/developer-guide/session-memory.md`, `docs/developer-guide/review-severity-rule.md`, `docs/developer-guide/technical-architecture.md` (line 315), `docs/developer-guide/testing-debugging.md` (line 348), `docs/generated/contributor-knowledge-base/` (the four files), `docs/getting-started/upgrading.md` (line 263), `docs/guides/RELEASE-GUIDE-INSTRUCTIONS.md`, `docs/guides/prd-skill-release-guide.md`, `docs/guides/tdd-skill-release-guide.md`, `docs/guides/reflect-cli-tools-guide.md` (line 444), `docs/guides/suites-guide.md` (suite 7 row and section), `docs/onboarding/ironclaude-onboarding.html` (line 564), `docs/reference/deviation-report-format.md`, `docs/reference/diagnostic-reference.md`, `docs/reference/model-aliases.md` (lines 61-62), `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (lines 1321 and 2042 if they name `tasklist` as a command; lines that only count commands are corrected to the real count). Add an upgrade note to `docs/getting-started/upgrading.md` stating that the three CLI groups, three commands and three skills are removed in 6.0.0.

Acceptance criteria:
- No kept doc outside the historical records names a removed command, skill or CLI group (search in Task 11).
- Relative links in edited docs still resolve (no link points at a deleted file): `git grep` for each deleted doc basename finds no link.
- `docs/user-guide/commands.md` command count and any "N commands" sentence match `ls src/superclaude/commands/*.md`.

## Task 10: Fix the root files, index, ignore rules and project config

Depends on: Task 3

Edit `CLAUDE.md` (the Pipelines block at lines 168-170; the internal-temporary-checkout exception list: four cases, drop `scripts/eval_runner.py`), `README.md` (lines 114-117), `PROJECT_INDEX.md` (lines 36, 68, 97) and `PROJECT_INDEX.json` (lines 46 and 94), `.gitignore` (remove the sprint-runner rules for `/.sprint-exitcode`, `.dev/sprint-state/` and the per-task output dump rule; keep the e2e-reflect harness rule if a kept harness writes there), and `pyproject.toml` line 127 (the `diagnostic` pytest marker: check with `git grep "mark.diagnostic"` whether a kept test uses it; remove the marker only if none does). Do not touch `CHANGELOG.md`.

Acceptance criteria:
- `git grep -n "superclaude sprint\|superclaude roadmap\|superclaude tasklist" -- CLAUDE.md README.md PROJECT_INDEX.md PROJECT_INDEX.json` is empty.
- `uv run pytest --strict-markers --collect-only -q` still collects without an unknown-marker error.

## Phase 5: Sync, search and prove

## Task 11: Sync the mirrors and prove no removed item remains

Depends on: Task 5, Task 6, Task 8, Task 9, Task 10

Run `make sync-dev` (it removes mirror files that no longer exist in `src/`; if it leaves stale files under `.claude/`, delete them by literal path), then `make verify-sync`. Run the leftover search for the removed names over tracked files, excluding the historical records, and fix every hit that is not the plain `roadmap` skill's own `.roadmap-state.json` use. Run `make lint`, `uv run ruff format --check src/ tests/`, `git diff --check`, the full test command of the `test` job (`pytest -v --tb=short -n auto --ignore=tests/cli/test_verify_sync_hooks.py`) and `pytest tests/cli/test_verify_sync_hooks.py`; compare with the baseline. Then in a throwaway `HOME` (`mktemp -d /tmp/throwaway-home.XXXX`) run `superclaude install` and `superclaude doctor`, check `~/.claude/commands/sc/` has no `roadmap.md`, `validate-roadmap.md` or `tasklist.md` and `~/.claude/skills/` has none of the three skills but has `roadmap`, `task`, `task-builder`, `tdd`, `prd`; remove the throwaway home by its literal path.

Acceptance criteria:
- `make verify-sync`, `make lint`, `ruff format --check` and `git diff --check` exit 0.
- Full test run: 0 failures that are not in the baseline; passed count equals baseline passed minus the removed and trimmed tests recorded in Tasks 4 and 5.
- The leftover search (patterns saved in `.dev/issues/v6-roadmap-family/leftover-search.md` with its result) is empty outside the historical records.
- `superclaude install` and `superclaude doctor` exit 0 in the throwaway home, and the installed lists match the check above.
