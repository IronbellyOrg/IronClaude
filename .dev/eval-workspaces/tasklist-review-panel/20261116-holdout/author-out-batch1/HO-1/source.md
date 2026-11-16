# Worker contract follow-ups from the PR #411 review (separate PR)

Repository: the Orca worktree `/home/coder/workspaces/worktrees/IronClaude/WorkerContractFollowups`, branch `ironbelly/WorkerContractFollowups`, based on `origin/master` at cb8f2f81 (PR #411 merged). All paths below are relative to that worktree.

## Why

PR #411's two review rounds fixed the unattended worker contract `artifacts` lists for init-lite, cleanup-audit, workflow and build, and its troubleshoot reports recorded three follow-ups that were left out of that PR's scope. This plan closes those three. Reports: PR #411 round-2 diagnosis (follow-up tasks section), copied facts below.

## Follow-up 1: state the gitignored-path rule once in the shared contract

- Today the rule "leave out of `artifacts` the paths git ignores (and paths outside the repository), because WC-9 stages every listed path and git refuses them" is written per command: `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:52` (YAML comment), `src/superclaude/commands/workflow.md:72` (Contract bullet), `src/superclaude/commands/build.md:104` (Contract bullet).
- WC-4 in `src/superclaude/core/WORKER-CONTRACT.md` (around lines 31-37) defines `artifacts` as "every other file written" and WC-9 (around line 41) stages `report_path`, `artifacts` and `.dev/tasks` with `git add -- <paths>`. The shared document exists so the shared rules are written once (its opening lines).
- Change: add one sentence to WC-4 in WORKER-CONTRACT.md saying `artifacts` leaves out paths git ignores and paths outside the repository, because WC-9 stages every listed path, and the report names where those files were written. Then shorten the per-command copies to a pointer to that WC-4 rule (keep each command's own list of which ignored files it writes, e.g. workflow's `.dev/reflect/runs.jsonl` and `.superclaude/memory/`, build's `build/`, `dist/`, `*.egg-info/`).
- Constraints: `tests/skills/test_worker_contract.py` pins the WC-4 phrase "`artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed" (around line 107) and must keep passing; `test_unattended_artifacts_list_only_files_the_run_wrote` currently asserts the workflow clause contains "runs.jsonl" and "left out", and the build clause contains "git check-ignore" and "left out" with no write-verb match: update those assertions to the new wording and add one assertion that WC-4 carries the rule. Avoid the literal phrase `git add` in new command-section text (the write-verb classification test flags unclassified hits). `workflow.md` and the whole `sc-workflow-protocol` folder must be byte-copied to `plugins/superclaude/` (parity tests in `tests/commands/test_workflow_command.py`, `tests/skills/test_task_workspace_smoke.py`, `tests/commands/test_routing_plugin_parity.py`). WORKER-CONTRACT.md is a core file installed to `~/.claude/`; check whether any test or mirror pins its text beyond line 107 (for example a plugin or spec copy) and keep them consistent.

## Follow-up 2: `/sc:test` has no `artifacts` rule

- `src/superclaude/commands/test.md` Unattended section, Contract bullet (around line 103), names `report_path` but says nothing about `artifacts`, although `--coverage` writes coverage output (`htmlcov/`, `.coverage`, `coverage.xml`, and `.pytest_cache/`), which this repository's `.gitignore` ignores (around lines 37, 40, 44, 48).
- Change: add an `artifacts` clause: every other file the run wrote, leaving out ignored paths per the WC-4 rule from follow-up 1 (so coverage output in an ignored location is named in the test report, not listed); `[]` when nothing else was written.
- Test: add the test section to `test_unattended_artifacts_list_only_files_the_run_wrote` (or a sibling test) so the clause is pinned. Keep the existing pins for test.md in `UNATTENDED_EXPECT` (test_worker_contract.py:349-353: flags `--watch`, `--output`; phrases `test-report.md`, `verdict`, `destructive`).

## Follow-up 3: init-lite `worker_status` when the scaffold step fails

- `src/superclaude/skills/sc-init-lite-protocol/SKILL.md:61` and `src/superclaude/commands/init-lite.md:92` say the run is `succeeded` "when the audit finished", else `failed`. Since PR #411, `superclaude init-lite` can write the report, print a `Scaffold:` line for the first scaffold file, then fail on the second write and exit non-zero (`src/superclaude/cli/init_lite.py`, `_write_scaffold`; regression test `tests/cli/test_init_lite.py::test_scaffold_partial_failure_prints_written_file`). Under the current wording that run is `succeeded`, so a WC-9 commit grant (commit only on `succeeded`, WORKER-CONTRACT.md around line 40) would stage a partial scaffold.
- Decision (default chosen; change it if the owner disagrees): the worker status follows the tool's exit code. `succeeded` when `superclaude init-lite` exited 0 (the audit finished and every requested scaffold write succeeded); otherwise `failed`, with the tool's error in `reason`; `artifacts` still lists the `Scaffold:` lines printed before the failure.
- Change both lines (SKILL.md:61 and init-lite.md:92) consistently; keep their test pins (`the one write besides the report`, `Safety Invariants 2 and 3`, `--dry-run`, `Scaffold:`, `[]`, no "when `--scaffold` is set", no "on a failed run").
- Test: assert both texts tie `succeeded` to the tool's exit status (for example the phrase "exited 0").

## Out of scope

- The two flaky master tests (ccsession shim-port collision, roadmap thread-ident reuse) diagnosed during PR #411: separate work.
- Other commands' sections beyond workflow, build and test.

## Verification for the whole change

`uv run pytest tests/skills/test_worker_contract.py tests/commands/test_workflow_command.py tests/skills/test_task_workspace_smoke.py tests/commands/test_routing_plugin_parity.py tests/cli/test_init_lite.py tests/cli/test_how_we_work_install.py`, then `make lint`, `uv run ruff format --check src/ tests/`, `make sync-dev` and `make verify-sync`. Never stage `.claude/`. Stage `.dev/tasks` (do not commit unless asked).
