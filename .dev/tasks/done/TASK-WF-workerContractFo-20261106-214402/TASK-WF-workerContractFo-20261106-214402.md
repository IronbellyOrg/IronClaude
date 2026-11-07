---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-workerContractFo-20261106-214402
version: "2"
priority: Medium
created_date: "2026-11-06"
---

# Worker contract follow-ups from the PR #411 review

Source: ./source.md
Goal: The gitignored-path exclusion for the unattended worker contract `artifacts` field is stated once in WC-4 and referenced by workflow, build and test; `/sc:test` gains an `artifacts` rule; init-lite's `worker_status` follows the tool's exit code, so a partial scaffold is never `succeeded`.

## Revision note (version 2)

Version 1 was reviewed by `/sc:reflect --mode pre` (report: `.dev/reflect/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/REPORT.md`, findings M-1 to M-11 and RF-1 to RF-3). The owner revised the plan with those findings before execution. One owner decision (2026-11-06, finding M-3) changes the brief's wording: source.md:13 asks WC-4 to say "the report names where those files were written", but workflow's report is the plan file, which never names its ignored files and may not be edited after review. Decision: WC-4 states only the exclusion and its reason; build and test each keep one short local sentence that their report names where the left-out files were written (source.md:19 requires this for test); workflow has no such sentence.

## Constraints

- Work only in this worktree's branch `ironbelly/WorkerContractFollowups` (based on `origin/master` cb8f2f81).
- Keep every existing test pin in `tests/skills/test_worker_contract.py`: the WC-4 phrase "`artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed"; the `UNATTENDED_EXPECT` flags and phrases for init-lite, build, test and workflow; the `Scaffold:`, `[]`, `--dry-run` and "as each file is written" / "as it is written" pins of the init-lite `artifacts` clause, and its bans on "when `--scaffold` is set", "failed tool run" and "on a failed run".
- No new text in `src/superclaude/commands/` or `src/superclaude/skills/` may contain the literal phrase `git add` (the write-verb classification test scans both); `git check-ignore` is allowed.
- New pointer text in installed files names the installed contract `~/.claude/WORKER-CONTRACT.md` where the file does not already point at it, and contains no `src/superclaude/` path.
- `src/superclaude/commands/workflow.md` and every file under `src/superclaude/skills/sc-workflow-protocol/` must stay byte-identical to their copies under `plugins/superclaude/` (parity tests in `tests/commands/test_workflow_command.py`, `tests/skills/test_task_workspace_smoke.py`, `tests/commands/test_routing_plugin_parity.py`). The plugin copies of `build.md` and `test.md` have no Unattended section and stay unchanged; init-lite has no plugin copy.
- Copies of WC-4 text (decided in review, finding M-4): the live copies are `src/superclaude/core/WORKER-CONTRACT.md`, the pins in `tests/skills/test_worker_contract.py`, and the developer-guide summary `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (around line 1002), which Task 1 updates. The planning spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (header: "Planning only") and its `specs/history/` snapshots stay unchanged, as do frozen records under `.dev/tasks/done/`, `.dev/orca-command-refactor/decisions/` and `.dev/reflect/`.
- Edit `src/superclaude/` (and the developer guide) only; run `make sync-dev` after edits; never stage `.claude/`. `.dev/tasks` is staged with `git add .dev/tasks`.
- Out of scope: the two flaky master tests (ccsession shim-port collision, roadmap thread-ident reuse), any other command's Unattended section (index-repo's fixed list is covered by the new WC-4 sentence without an edit), and `report_path` under an ignored path.

## Phase 1: Shared rule in the worker contract

## Task 1: Add the gitignored-path exclusion to WC-4 in WORKER-CONTRACT.md

In `src/superclaude/core/WORKER-CONTRACT.md`, WC-4 (the `- **WC-4.` bullet at line 31 and its sub-bullets up to the `- **WC-8.` bullet), add a new sub-bullet directly after the worker-fields sub-bullet (line 32) reading exactly: "`artifacts` leaves out paths git ignores and paths outside the repository, because WC-9 stages every listed path and git refuses them. This applies to every command's `artifacts` list, including a fixed list in the command's own section." Do not change the pinned phrase on line 32. Do not add a report-naming duty to WC-4 (owner decision, Revision note). In `tests/skills/test_worker_contract.py`, add the phrase "`artifacts` leaves out paths git ignores and paths outside the repository" to `RULE_PHRASES["WC-4"]` (so `test_rule_check_fails_when_rule_removed` covers it), and add one assertion that the WC-4 span alone (the text from "- **WC-4." up to "\n- **WC-8.") contains "git ignores", "outside the repository" and "every command's `artifacts` list". In the developer guide (`docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, the "WC-4, the worker contract." bullet around line 1002), add one sentence with the same rule: `artifacts` leaves out paths git ignores and paths outside the repository, because WC-9 stages every listed path and git refuses them.

Acceptance criteria:
- WC-4 in `src/superclaude/core/WORKER-CONTRACT.md` holds the new sub-bullet with the exact text above, inside the WC-4 span; the line-32 pin is unchanged; no new WC-4 text contains the literal `git add`.
- The new `RULE_PHRASES["WC-4"]` entry and the WC-4-span assertion exist; the span assertion fails if the sentence is moved into WC-9 (check by reasoning over the slice bounds, or with the existing `_patched_copy` helper).
- The developer-guide WC-4 bullet carries the rule.
- `uv run pytest tests/skills/test_worker_contract.py -q` passes.

## Phase 2: Command sections point at the shared rule

## Task 2: Shorten the workflow copies of the rule to a WC-4 pointer

Depends on: Task 1

In `src/superclaude/commands/workflow.md` (Unattended mode, Contract bullet, line 72), replace "are left out because WC-9 stages every `artifacts` path and git refuses ignored paths" with "are left out (WC-4)". In `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md` (the `artifacts:` YAML line 52), replace the comment tail "are left out (WC-9 stages every listed path, and git refuses ignored paths)" with "are left out (WC-4 in ~/.claude/WORKER-CONTRACT.md)". Keep everything else on both lines (package `return-contract.yaml`, `source.md` when written, reflect's run-directory files, the deviation-patterns file, "pre-creation", `[]` before a package exists). Add no line with a backticked `artifacts` or a leading `artifacts:` above line 52 of return-contract.md, so the test helper `_artifacts_clause` keeps reading line 52. Byte-copy both files to `plugins/superclaude/commands/workflow.md` and `plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`. In `test_unattended_artifacts_list_only_files_the_run_wrote` (`tests/skills/test_worker_contract.py`), make the workflow assertions require "runs.jsonl", "left out" and "WC-4" in both the command clause and the ref line.

Acceptance criteria:
- Both workflow texts name the ignored files they leave out and point at WC-4; neither contains "git refuses", "stages every" or the literal `git add`; return-contract.md names `~/.claude/WORKER-CONTRACT.md` and no `src/superclaude/` path.
- The plugin copies are byte-identical (`uv run pytest tests/commands/test_workflow_command.py tests/skills/test_task_workspace_smoke.py tests/commands/test_routing_plugin_parity.py -q` passes).
- `uv run pytest tests/skills/test_worker_contract.py -q` passes with the updated workflow assertions.

## Task 3: Shorten the build copy of the rule to a WC-4 pointer

Depends on: Task 1

In `src/superclaude/commands/build.md` (Unattended mode, Contract bullet, line 104), rewrite the `artifacts` clause to: "`artifacts` lists the build output files the build tool reports; paths git ignores are left out (WC-4; in a git repository, check each with `git check-ignore`; typically `build/`, `dist/` and `*.egg-info/`), and the build report names where they were written." The restated reason ("because WC-9 stages every listed path and git refuses them") and "paths outside the repository" go (WC-4 carries both). Keep "build-report.md" and `--output` in the bullet and "no gate" in the Gates bullet. In `test_unattended_artifacts_list_only_files_the_run_wrote`, make the build assertions require "git check-ignore", the exact phrase "paths git ignores are left out" and "WC-4", with no write-verb match.

Acceptance criteria:
- `src/superclaude/commands/build.md` names the check, the typical ignored paths and the local report sentence, points at WC-4 for the reason, and contains neither "git refuses" nor the literal `git add`.
- `uv run pytest tests/skills/test_worker_contract.py -q` passes, including the build `UNATTENDED_EXPECT` pins (`--output`, "build-report.md", "no gate") and the updated build assertions.

## Phase 3: Test command artifacts rule

## Task 4: Add an `artifacts` rule to the /sc:test Unattended section

Depends on: Task 1

In `src/superclaude/commands/test.md` (Unattended mode, Contract bullet, line 103), add after the `report_path` sentence: "`artifacts` lists every other file the run wrote; paths git ignores are left out (WC-4; typically coverage output such as `htmlcov/`, `.coverage`, `coverage.xml` and `.pytest_cache/`), and the test report names where they were written; it is `[]` when nothing else listable was written." This must be the first backticked `artifacts` in the test Unattended section (no earlier bullet mentions it). Keep the existing pins (`--watch`, `--output`, "test-report.md", "verdict", "destructive"). In `tests/skills/test_worker_contract.py`, add "left out" to `UNATTENDED_EXPECT["test"]["phrases"]` (so the token-removal test covers it), and in `test_unattended_artifacts_list_only_files_the_run_wrote` assert that the test section's `artifacts` clause contains the exact phrase "paths git ignores are left out", "WC-4" and "`[]`", and has no write-verb match.

Acceptance criteria:
- The `src/superclaude/commands/test.md` Contract bullet has the `artifacts` clause above: ignored coverage output is left out with a WC-4 pointer, the report names where it went, and `[]` applies when nothing else listable was written.
- A clause that lists `htmlcov/` while naming WC-4 and `[]` but lacking "paths git ignores are left out" would fail the new assertion.
- `uv run pytest tests/skills/test_worker_contract.py -q` passes, including the new pins and the existing test.md `UNATTENDED_EXPECT` row.

## Phase 4: init-lite worker status

## Task 5: Tie init-lite's `worker_status` to the tool's exit code

In `src/superclaude/skills/sc-init-lite-protocol/SKILL.md` (Section 3 step 6, line 61), replace "`worker_status` (`succeeded` when the audit finished, else `failed`)" with "`worker_status` (`succeeded` when `superclaude init-lite` exited 0, meaning the audit finished and every requested scaffold write succeeded; otherwise `failed`, with the tool's error in `reason`; the tool's exit code is the only basis for `succeeded`)". In `src/superclaude/commands/init-lite.md` (Unattended mode, Contract bullet, line 92), replace the last sentence "The run is succeeded when the audit finished, and failed otherwise." with "The run is `succeeded` when `superclaude init-lite` exited 0 (the audit finished and every requested scaffold write succeeded), and `failed` otherwise, with the tool's error in `reason`; `artifacts` still lists the `Scaffold:` lines printed before a failure." This follows the decision in ./source.md (Follow-up 3): a WC-9 commit grant commits only on `succeeded`, so a partial scaffold must not be `succeeded`. The init-lite.md status sentence sits inside the `artifacts` clause the tests read, so it must contain neither "failed tool run" nor "on a failed run". Keep the pins "the one write besides the report", "Safety Invariants 2 and 3", `--dry-run`, `Scaffold:`, `[]`, "as it is written". In `tests/skills/test_worker_contract.py`, assert that the SKILL.md line carrying `worker_status` and the init-lite.md Contract line each contain the exact phrase "`succeeded` when `superclaude init-lite` exited 0" and do not contain "when the audit finished".

Acceptance criteria:
- Both init-lite texts carry the exact phrase "`succeeded` when `superclaude init-lite` exited 0", tie `failed` to any other exit with the error in `reason`, keep `artifacts` listing the printed `Scaffold:` lines, and no longer contain "when the audit finished".
- `uv run pytest tests/skills/test_worker_contract.py tests/cli/test_init_lite.py -q` passes, including the new assertions and the existing init-lite pins.
- `uv run pytest tests/skills/test_worker_contract.py tests/commands/test_workflow_command.py tests/skills/test_task_workspace_smoke.py tests/commands/test_routing_plugin_parity.py tests/cli/test_init_lite.py tests/cli/test_how_we_work_install.py -q`, `make lint`, `uv run ruff format --check src/ tests/` and `make verify-sync` (after `make sync-dev`) all pass, with output saved to `./artifacts/t5-checks.txt` (the package's own `artifacts/` folder).
