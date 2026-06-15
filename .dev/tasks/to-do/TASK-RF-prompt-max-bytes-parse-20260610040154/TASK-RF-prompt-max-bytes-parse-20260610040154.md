---
id: "TASK-RF-prompt-max-bytes-parse-20260610040154"
title: "Defensive parsing of SUPERCLAUDE_PROMPT_MAX_BYTES so a bad env value can never hard-fail module import"
description: "Add a `_parse_prompt_max_bytes(raw, default)` helper to `src/superclaude/cli/pipeline/process.py` and replace the import-time bare `int(os.environ.get(...))` assignment with a call to it, so a misconfigured SUPERCLAUDE_PROMPT_MAX_BYTES env var degrades to the default (with a logged warning) instead of raising ValueError and cascading an ImportError to every dependent module. Add unit tests covering the env-parse paths. Resolves PR #156 review comment r3385368388 (augmentcode bot, severity medium)."
version: ""
status: "🟢 Done"
type: "🐛 BugFix"
priority: "🔼 High"
created_date: "2026-06-10"
updated_date: "2026-06-10"
assigned_to: "rf-task-executor"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_doc: ""
parent_task: ""
depends_on: []
spec_path: ""
reflect_pre:
  verdict: ""
  coverage_pct: null
  depth: ""
  tcs: 0
  run_id: ""
  report: ""
  reviewed_at: ""
reflect_post: "verdict=pass; mode=post(UC-2); executor-disjoint; deviations=none(only authorized formatter whitespace on in-scope files); reviewed=2026-06-10"
related_docs:
- path: ".dev/troubleshoot/bug-prompt-max-bytes-import-hardfail-20260610035732/REPORT.md"
  description: "Troubleshoot report identifying the import-time hard-fail defect and the proven fix"
- path: ".dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/research-notes.md"
  description: "Consolidated research evidence: verified file paths, line numbers, in-scope imports, test seam, conventions"
related_prd: ""
related_tdd: ""
tags:
- "bugfix"
- "pipeline"
- "process"
- "defensive-parsing"
- "pr-156"
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
start_date: "2026-06-10"
completion_date: "2026-06-10"
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
---

# Defensive parsing of SUPERCLAUDE_PROMPT_MAX_BYTES

## Task Overview

The module `src/superclaude/cli/pipeline/process.py` currently computes its prompt-size sanity guard at import time with a bare conversion:

```python
PROMPT_MAX_BYTES: int = int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024))
```

Because this runs at module-import time, any non-integer override (`"16MB"`, `""`, `"0x10"`) raises `ValueError` during import of `superclaude.cli.pipeline.process`, which cascades an `ImportError` to every dependent module and prevents the CLI from loading at all. The documented intent is a "sanity guard … env-overridable for operators," so a bad override MUST degrade gracefully (fall back to the default, emit a logged warning), not brick the module.

This task adds a small defensive helper `_parse_prompt_max_bytes(raw, default)` and replaces the bare assignment with a call to it. The helper returns the default on `None`, on non-integer input (caught `TypeError`/`ValueError`), and on non-positive values — logging a warning in the latter two cases. It uses only symbols already in scope (`_log`, `Optional`, `os`) — no new imports. The task then adds unit tests for every env-parse path and runs the targeted + regression suites.

This work resolves PR #156 review comment r3385368388 (augmentcode bot, severity medium). All changes are confined to `src/` and `tests/`; there is NO `.claude/` involvement. The work MUST be applied on branch `fix/pipeline-stdin-large-prompts` (PR #156 head) in an isolated git worktree and MUST NOT disturb the current `fix/prd-parallel-gate-advisory` working tree.

## Key Objectives

The following objectives MUST be achieved by this task:

1. **Add the defensive helper:** Insert `_parse_prompt_max_bytes(raw, default=16*1024*1024) -> int` into `process.py`, placed AFTER the `_log` assignment and BEFORE the `PROMPT_MAX_BYTES` module-level assignment, using only symbols already imported.
2. **Swap the assignment:** Replace the bare `int(os.environ.get(...))` with `PROMPT_MAX_BYTES: int = _parse_prompt_max_bytes(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES"))`, keeping `PROMPT_MAX_BYTES` typed `int` so the downstream `ClaudeProcess.start()` consumer needs no change.
3. **Add unit tests:** Add a test class to `tests/pipeline/test_process_stdin.py` covering non-integer → default (with caplog warning), non-positive (`"0"`, `"-1"`) → default, valid int string → parsed value, and absent var → default.
4. **Validate:** Confirm the module imports cleanly with a bad env var set, run the targeted test file and the regression suites GREEN, and confirm `ruff` lint + format pass on the two modified files.
5. **Pass a final lite QA gate** (3 agents) and complete the POST reflect gate before marking the task Done.

## Prerequisites & Dependencies

### Parent Task & Dependencies
- **Parent Task:** None (standalone PR #156 review remediation)
- **Blocking Dependencies:** None
- **This task blocks:** Merge of PR #156 (the review comment must be resolved before merge)

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

**Required Previous Stage Outputs:**
- **Troubleshoot Report:** `.dev/troubleshoot/bug-prompt-max-bytes-import-hardfail-20260610035732/REPORT.md` - The report identifying the import-time hard-fail and the proven fix shape.
- **Research Notes:** `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/research-notes.md` - Verified file paths, line numbers, in-scope imports (`_log`, `Optional`, `os`, `logging`), the `TestPromptMaxBytesGuard` test seam, and project conventions.

## Execution Context

### References
- BUILD_REQUEST GOAL (verbatim): Make `PROMPT_MAX_BYTES` parsing in `src/superclaude/cli/pipeline/process.py` defensive so a misconfigured `SUPERCLAUDE_PROMPT_MAX_BYTES` env var can never hard-fail module import. Add a `_parse_prompt_max_bytes(raw, default)` helper and replace the bare `int(os.environ.get(...))` assignment with a call to it; add tests for the env-parse paths.
- BUILD_REQUEST WHY (summary): The current import-time `int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16*1024*1024))` raises `ValueError` on a non-integer override during import of `superclaude.cli.pipeline.process`, cascading `ImportError` to every dependent module — a config typo becomes a total import outage. A bad override must degrade gracefully, not brick the module.
- [Troubleshoot REPORT](.dev/troubleshoot/bug-prompt-max-bytes-import-hardfail-20260610035732/REPORT.md): Root-cause report and the proven fix.
- [Research Notes](.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/research-notes.md): Verified evidence — file paths, line numbers, in-scope imports, test seam, conventions.

### Source Areas
- `src/superclaude/cli/pipeline/process.py`: The module under fix. Contains the module logger `_log = logging.getLogger("superclaude.pipeline.process")` (~line 21), the defective `PROMPT_MAX_BYTES` env-parse assignment (~lines 27-29), and the existing imports `from typing import Callable, Optional` plus `os`/`logging`. Downstream consumer `ClaudeProcess.start()` reads `PROMPT_MAX_BYTES` and expects an `int`.
- `tests/pipeline/test_process_stdin.py`: The test module to extend. Contains `class TestPromptMaxBytesGuard` (~line 123 onward) which patches the constant but does NOT exercise env-var parsing. Uses pytest classes, `tmp_path`/`monkeypatch`/`caplog` fixtures, UV-run pytest.

### Key Constraints
- QA intensity: **lite** — final QA gate uses exactly 3 agents (1 structural + 1 content + 1 domain), max 1 fix cycle, 1 verification agent.
- `PROMPT_MAX_BYTES` MUST remain a typed `int` — NO call-site changes to `ClaudeProcess.start()`.
- `_log` (module logger) and `Optional` (from `typing`) are ALREADY imported — NO new imports may be added.
- The helper MUST be defined AFTER `_log` is assigned and BEFORE the `PROMPT_MAX_BYTES` module-level assignment.
- Scope is `src/` + `tests/` ONLY — NO `.claude/` involvement, NO `git add` of any `.claude/` path.
- Execute on branch `fix/pipeline-stdin-large-prompts` (PR #156 head) in an isolated git worktree; do NOT disturb the current `fix/prd-parallel-gate-advisory` working tree.
- Python operations use UV only (`uv run pytest ...`) — never `python -m` or bare `pytest`.

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:
- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user.

## Detailed Task Instructions

### Phase 1: Preparation and Worktree Setup

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

**Step 1.1:** Update task status

- [x] Update status to "🟠 Doing" and start_date to current date in frontmatter of this file, then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.` Once done, mark this item as complete.

**Step 1.2:** Create an isolated worktree on the PR #156 head branch

- [x] Establish an isolated working environment for this fix so the current `fix/prd-parallel-gate-advisory` working tree is NOT disturbed, because the changes MUST land on the PR #156 head branch `fix/pipeline-stdin-large-prompts` and that branch is not currently checked out. Use the Bash tool to run `git fetch origin fix/pipeline-stdin-large-prompts` to ensure the branch tip is local, then create a dedicated worktree by running `git worktree add ../IronClaude-pr156 fix/pipeline-stdin-large-prompts` (if a worktree already exists for that branch, instead run `git worktree list`, reuse the existing `fix/pipeline-stdin-large-prompts` worktree path, and run `git pull --ff-only` inside it to bring it up to date with origin). All subsequent file reads, edits, and test runs in this task MUST operate on the files inside this worktree (the `src/superclaude/cli/pipeline/process.py` and `tests/pipeline/test_process_stdin.py` copies on the `fix/pipeline-stdin-large-prompts` branch), NOT the files in the current `fix/prd-parallel-gate-advisory` checkout, ensuring no edits leak into the wrong branch and that `git status` in the original working tree remains untouched by this task's source edits. Record the absolute worktree path in the ### Phase 1 Findings section of the ## Task Log / Notes for use by later steps. If unable to complete due to git errors, an existing conflicting worktree, or the branch not existing on origin, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 2: Implementation (process.py)

**Step 2.1:** Add the `_parse_prompt_max_bytes` defensive helper

- [x] Read the file `process.py` at `src/superclaude/cli/pipeline/process.py` (inside the `fix/pipeline-stdin-large-prompts` worktree from Step 1.2) to locate the module logger assignment `_log = logging.getLogger("superclaude.pipeline.process")` (around line 21) and the existing module-level `PROMPT_MAX_BYTES: int = int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024))` assignment (around lines 27-29), and to confirm that `Optional` is already imported via `from typing import Callable, Optional` and that `os` and `logging` are already imported at the module top — this confirmation is required because the helper signature uses `Optional[str]` and the body uses `_log.warning(...)`, and NO new imports may be added. Then edit `process.py` to insert the following helper definition AFTER the `_log = logging.getLogger(...)` line and BEFORE the `PROMPT_MAX_BYTES` module-level assignment (the helper MUST reference the already-in-scope `_log` and `Optional`, and MUST NOT add any import):

  ```python
  def _parse_prompt_max_bytes(
      raw: Optional[str], default: int = 16 * 1024 * 1024
  ) -> int:
      """Parse SUPERCLAUDE_PROMPT_MAX_BYTES defensively.

      A misconfigured env var must never hard-fail module import. Invalid or
      non-positive values fall back to the default with a logged warning.
      """
      if raw is None:
          return default
      try:
          value = int(raw)
      except (TypeError, ValueError):
          _log.warning(
              "Invalid SUPERCLAUDE_PROMPT_MAX_BYTES=%r (not an integer); "
              "falling back to default %d bytes.",
              raw,
              default,
          )
          return default
      if value <= 0:
          _log.warning(
              "SUPERCLAUDE_PROMPT_MAX_BYTES=%d is non-positive; "
              "falling back to default %d bytes.",
              value,
              default,
          )
          return default
      return value
  ```

  Insert this helper verbatim (matching the project's dense, explanatory docstring register), ensuring the helper is placed at module scope between `_log` and the `PROMPT_MAX_BYTES` assignment, the indentation matches the surrounding module-level code, no new import statements are introduced, and the rest of the file is left unchanged. If unable to complete due to the anchor lines not being found at the expected location, file access issues, or an unexpected import layout, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.2:** Swap the bare `int(...)` assignment for a call to the helper

- [x] Read the file `process.py` at `src/superclaude/cli/pipeline/process.py` (inside the `fix/pipeline-stdin-large-prompts` worktree) to locate the existing defective assignment `PROMPT_MAX_BYTES: int = int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024))` (around lines 27-29), because this import-time bare `int()` is exactly what raises `ValueError` on a bad override and must be replaced now that the helper from Step 2.1 exists. Then edit `process.py` to replace that single assignment with:

  ```python
  PROMPT_MAX_BYTES: int = _parse_prompt_max_bytes(
      os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES")
  )
  ```

  ensuring `PROMPT_MAX_BYTES` remains annotated as `int` (so the downstream `ClaudeProcess.start()` consumer that reads it for the pre-spawn size guard requires NO change), the default 16 MiB value now lives solely in the helper's `default` parameter (do NOT also pass a redundant default at the call site), any adjacent explanatory comment (e.g., the `# Default 16 MiB; ...` block) is preserved or updated to remain accurate, and no other code in the file is altered. If unable to complete due to the assignment not being found at the expected location or file access issues, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 3: Unit Tests (test_process_stdin.py)

**Step 3.1:** Add an env-parse test class exercising the helper directly

- [x] Read the file `test_process_stdin.py` at `tests/pipeline/test_process_stdin.py` (inside the `fix/pipeline-stdin-large-prompts` worktree) to study the existing `class TestPromptMaxBytesGuard` (around line 123 onward) and adopt its conventions — pytest classes grouping related tests, fixture-based style using `monkeypatch`/`caplog`, no inline `python -c`, and the import path `superclaude.cli.pipeline.process` — because the new tests must match the established style and import the helper added in Step 2.1. Then edit `test_process_stdin.py` to add a new test class `TestPromptMaxBytesEnvParse` that imports and exercises `_parse_prompt_max_bytes` from `superclaude.cli.pipeline.process` directly (calling the helper with explicit `raw` arguments rather than mutating the process environment), covering exactly these env-parse paths as separate test methods: (a) a non-integer string such as `"16MB"` returns the default AND emits a warning — assert the fallback value equals the default `16 * 1024 * 1024` and assert via `caplog` (at `logging.WARNING`) that a warning mentioning `SUPERCLAUDE_PROMPT_MAX_BYTES` was logged; (b) an empty string `""` returns the default with a warning (same caplog assertion); (c) a non-positive value `"0"` returns the default AND emits the non-positive warning; (d) a non-positive value `"-1"` returns the default AND emits the non-positive warning; (e) a valid integer string such as `"2048"` returns the parsed `int` value `2048` with NO warning; (f) `raw=None` (absent var) returns the default with NO warning. Use `caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process")` (or the project's established caplog pattern) so warning assertions are scoped to the module logger, ensuring every assertion checks a concrete value (no `assert True`), the default constant is referenced as `16 * 1024 * 1024` (not a hardcoded magic number divergent from the helper), no test fabricates behavior the helper does not implement, and the new class integrates cleanly alongside `TestPromptMaxBytesGuard` without modifying the existing class. If unable to complete due to import errors, the helper not being importable, or file access issues, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.2:** Run the targeted test file and confirm GREEN

- [x] Run the targeted test file to verify the new env-parse tests AND the existing guard tests all pass, because this is the direct evidence that the helper behaves correctly across every env-parse path. Use the Bash tool to execute `uv run pytest tests/pipeline/test_process_stdin.py -v` from inside the `fix/pipeline-stdin-large-prompts` worktree (UV only — never `python -m` or bare `pytest`), ensuring the run reports 0 failures and 0 errors and that both `TestPromptMaxBytesEnvParse` and the pre-existing `TestPromptMaxBytesGuard` test methods are collected and pass. Capture the summary line (passed/failed counts) to the ### Phase 3 Findings section of the ## Task Log / Notes. If any test fails, read the failure output to identify the root cause, fix the test or the Step 2.1 helper / Step 2.2 assignment as appropriate, then re-run until GREEN. If unable to reach a GREEN run after reasonable attempts, log the specific failures using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.3:** Confirm the module imports cleanly with a bad env var set

- [x] Verify the core defect is actually fixed by confirming the module imports cleanly even when the env var is misconfigured, because the whole purpose of this change is that a bad override must not raise at import time. Use the Bash tool from inside the `fix/pipeline-stdin-large-prompts` worktree to run `SUPERCLAUDE_PROMPT_MAX_BYTES=16MB uv run python -c "import superclaude.cli.pipeline.process as p; print(p.PROMPT_MAX_BYTES)"` and confirm it exits 0 and prints the default value `16777216` (i.e., `16 * 1024 * 1024`) rather than raising `ValueError`/`ImportError`, then repeat with `SUPERCLAUDE_PROMPT_MAX_BYTES=0` confirming it also prints `16777216`, and with `SUPERCLAUDE_PROMPT_MAX_BYTES=2048` confirming it prints `2048`. Capture the three printed values to the ### Phase 3 Findings section of the ## Task Log / Notes, ensuring no invocation raises an exception. If any invocation raises or prints an unexpected value, log the specific output using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.4:** Run the regression suites and confirm GREEN

- [x] Run the broader regression suites to confirm the change introduces no regressions in the pipeline or cli_portify test areas, because the modified module is imported widely and the size-guard consumer must remain intact. Use the Bash tool from inside the `fix/pipeline-stdin-large-prompts` worktree to execute `uv run pytest tests/pipeline/ tests/cli_portify/` (UV only), ensuring the run reports 0 failures and 0 errors across both directories. Capture the summary line (passed/failed counts) to the ### Phase 3 Findings section of the ## Task Log / Notes. If any test fails, read the failure output to identify whether the failure is caused by this change or is a pre-existing unrelated failure, fix any failure caused by this change, then re-run. If unrelated pre-existing failures are found, note them explicitly. If unable to reach a GREEN run for changes caused by this task, log the specific failures using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 4: Lint & Format Validation

**Step 4.1:** Run ruff lint and format on the modified files

- [x] Validate code style on the two modified files because the project requires `ruff` lint and format to pass before changes are committed. Use the Bash tool from inside the `fix/pipeline-stdin-large-prompts` worktree to run `ruff` scoped to ONLY the two modified files: `uv run ruff format src/superclaude/cli/pipeline/process.py tests/pipeline/test_process_stdin.py` then `uv run ruff check src/superclaude/cli/pipeline/process.py tests/pipeline/test_process_stdin.py`, ensuring both commands report clean for those two files. Do NOT run repo-wide `make lint` / `make format` at this gate — the freshly-checked-out PR-branch worktree may carry pre-existing `ruff` violations in unrelated files that are OUT OF SCOPE for this task and MUST NOT block this gate or be fixed here. Only the two target files must be lint- and format-clean; if `ruff format` reformats anything beyond the two target files, do NOT stage those. After formatting, re-run `uv run pytest tests/pipeline/test_process_stdin.py -v` to confirm formatting did not break anything, capturing the lint/format outcome to the ### Phase 4 Findings section of the ## Task Log / Notes. If lint or format reports errors, fix them in the two modified files and re-run until clean. If unable to reach a clean lint/format state, log the specific errors using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 5: Final QA Gate (lite — 3 agents, M3 lite sequence)

This is the single final QA validation gate (FINAL_ONLY) at **lite** intensity per I22: 3 report-only lens agents (1 combined structural + 1 combined content + 1 domain), one serialized consolidation, one serialized fix agent, one verification agent, and a conditional proceed with a maximum of 1 fix cycle. The two target files under review are `src/superclaude/cli/pipeline/process.py` and `tests/pipeline/test_process_stdin.py` (inside the `fix/pipeline-stdin-large-prompts` worktree). Adversarial framing uses N=5 (the change is <500 lines).

**Step 5.1 (Aggregation — M3 Step 1)**

- [x] Build the QA input inventory for the final gate by recording the two changed files and the exact diff under review, because the lens agents need a precise, shared description of what to verify. Use the Bash tool from inside the `fix/pipeline-stdin-large-prompts` worktree to run `git --no-pager diff` (capturing the working-tree changes to `process.py` and `test_process_stdin.py`), then write a summary inventory to `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/final-output-inventory.md` listing each modified file with its path and a one-line description of the change (helper addition + assignment swap in `process.py`; `TestPromptMaxBytesEnvParse` class in `test_process_stdin.py`), and noting the worktree path so QA agents read the correct copies. Ensure the inventory accurately reflects both deliverables. If unable to complete, log the blocker in the ### Phase 5 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 5.2 (Structural Lens — combined, report-only)**

- [x] Spawn ONE rf-qa agent with `fix_authorization: false` to review the two changed files through a **combined structural lens** (template/code-conformance + internal-consistency + evidence-quality merged, per I22 lite). Provide the agent the inventory at `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/final-output-inventory.md` and have it read `src/superclaude/cli/pipeline/process.py` and `tests/pipeline/test_process_stdin.py` (in the `fix/pipeline-stdin-large-prompts` worktree). The agent MUST check: the helper `_parse_prompt_max_bytes` is placed AFTER `_log` and BEFORE the `PROMPT_MAX_BYTES` assignment; NO new imports were added (`Optional`, `os`, `logging`, `_log` all pre-existing); `PROMPT_MAX_BYTES` is still annotated `int`; the call site passes no redundant default; the helper handles `None`, non-integer (`TypeError`/`ValueError`), and non-positive paths with the correct warning calls; the test class imports the helper from the real module path and asserts concrete values; and no placeholder/TODO remains. Use adversarial framing: "Assume these changes have at least 5 structural errors. Find them." The agent writes its report with a PASS/FAIL verdict to `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/qa-structural-combined-report.md`. If unable to spawn the agent, log the blocker in the ### Phase 5 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 5.3 (Content Lens — combined, report-only)**

- [x] Spawn ONE rf-qa-qualitative agent with `fix_authorization: false` to review the two changed files through a **combined content lens** (actionability + numbers/metrics + crossref-chain merged, per I22 lite). Provide the agent the inventory and have it read both changed files (in the `fix/pipeline-stdin-large-prompts` worktree). The agent MUST check: the test class covers ALL required env-parse paths from the BUILD_REQUEST (non-integer→default+warning, empty string→default+warning, `"0"`→default+warning, `"-1"`→default+warning, valid string→parsed value with no warning, absent/`None`→default with no warning) with no path silently dropped; the caplog warning assertions actually scope to the `superclaude.pipeline.process` logger; the default value `16 * 1024 * 1024` is consistent between the helper and the tests; and the warning messages are coherent and reference `SUPERCLAUDE_PROMPT_MAX_BYTES`. Use adversarial framing: "Assume these changes have at least 5 content/coverage errors. Find them." The agent writes its report with a PASS/FAIL verdict to `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/qa-content-combined-report.md`. If unable to spawn the agent, log the blocker in the ### Phase 5 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 5.4 (Domain Lens — Python import-safety, report-only)**

- [x] Spawn ONE rf-qa agent with `fix_authorization: false` for the highest-value **domain lens: Python module-import safety** (the core defect class). Provide the agent the inventory and have it read `src/superclaude/cli/pipeline/process.py` (in the `fix/pipeline-stdin-large-prompts` worktree) plus the Phase 3 Findings (Step 3.3 import-safety evidence) in the ## Task Log / Notes of this task file. The agent MUST verify: there is NO remaining import-time call path that can raise on a bad env value (the `int()` conversion is now inside the helper's `try` and the only module-level call is `_parse_prompt_max_bytes(os.environ.get(...))`); the helper never propagates `ValueError`/`TypeError`; non-positive values cannot slip through as a valid size; and the change does NOT alter the contract that `ClaudeProcess.start()` reads `PROMPT_MAX_BYTES` as an `int`. Use adversarial framing: "Assume there is still at least 1 import-time failure path. Find it." The agent writes its report with a PASS/FAIL verdict to `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/qa-domain-import-safety-report.md`. If unable to spawn the agent, log the blocker in the ### Phase 5 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 5.5 (Findings Consolidation — M3 Step 5)**

- [x] Read all three lens reports from Steps 5.2-5.4 by using Glob to find `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/qa-structural-combined-report.md`, `.../qa-content-combined-report.md`, and `.../qa-domain-import-safety-report.md`. Extract all findings and produce a single consolidated findings file at `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/qa-consolidated-findings.md` listing each issue deduplicated (same issue found by multiple lenses listed once with all originating lenses noted), with severity (CRITICAL/IMPORTANT/MINOR) and originating lens, ensuring no findings are omitted. If all three reports show PASS with zero findings, write "No findings — all lenses passed" to the consolidated file and proceed. If unable to read the reports, log the blocker in the ### Phase 5 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 5.6 (Fix Agent — M3 Step 6, serialized per I20)**

- [x] Read the consolidated findings file at `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/qa-consolidated-findings.md`. If it says "No findings," skip this step and mark complete. If findings exist, spawn ONE rf-qa agent with `fix_authorization: true` and the consolidated findings file as input; this single agent applies ALL fixes to `src/superclaude/cli/pipeline/process.py` and/or `tests/pipeline/test_process_stdin.py` (in the `fix/pipeline-stdin-large-prompts` worktree) and writes a fix log to `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/qa-fix-log.md` documenting each finding addressed and the specific edit made, ensuring only ONE agent modifies files (no parallel fixes per I20) and that after fixing it re-runs `uv run pytest tests/pipeline/test_process_stdin.py -v` to confirm tests still pass. If unable to spawn the agent, log the blocker in the ### Phase 5 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 5.7 (Verification — M3 Step 7, lite: 1 agent)**

- [x] Read the fix log at `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/qa-fix-log.md`. If no fixes were needed (Step 5.6 was skipped), skip this step and mark complete. If fixes were applied, spawn ONE rf-qa verification agent (lite intensity, combined structural + content check) with `fix_authorization: false` to confirm: (a) all findings from the consolidated findings file were addressed, (b) fixes were applied correctly with no garbled text or lost content, (c) no new issues were introduced, and (d) `uv run pytest tests/pipeline/test_process_stdin.py -v` still passes. The agent writes its verdict to `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/qa-verification-report.md` using adversarial framing. If unable to spawn the agent, log the blocker in the ### Phase 5 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 5.8 (Conditional Proceed — M3 Step 8, lite: max 1 fix cycle)**

- [x] Read the verification report at `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/qa/qa-verification-report.md` (or, if Steps 5.6-5.7 were skipped because there were no findings, treat the gate as PASS). If the verdict is PASS, proceed to Phase 6. If the verdict is FAIL and no fix cycle has yet been run, repeat Steps 5.5-5.7 ONCE (re-consolidate new + remaining findings, fix, verify) — this is the lite maximum of 1 fix cycle. If the verdict is still FAIL after that single fix cycle, do NOT loop further: record the unresolved issues as Open Questions in the ### Phase 5 Findings section of the ## Task Log / Notes (per I22 lite: unresolved issues become Open Questions and the task proceeds), then mark this item complete. Once done, mark this item as complete.

### Phase 6: Commit & Push to Update PR #156

**Step 6.1:** Stage only the two source/test files (NEVER `.claude/`)

- [x] Stage exactly the two changed files for commit, because the scope of this task is strictly `src/` + `tests/` and staging any `.claude/` path is forbidden. Use the Bash tool from inside the `fix/pipeline-stdin-large-prompts` worktree to run `git status` first to confirm the only intended changes are to `src/superclaude/cli/pipeline/process.py` and `tests/pipeline/test_process_stdin.py`, then run `git add src/superclaude/cli/pipeline/process.py tests/pipeline/test_process_stdin.py`. YOU MUST NOT run `git add .`, `git add -A`, or `git add -f` on any path, and YOU MUST NOT stage any `.claude/` file. After staging, run `git status` again and confirm only the two intended files are staged, ensuring nothing under `.claude/` and no unrelated files are included. If any `.claude/` path or unrelated file appears staged, unstage it with `git restore --staged <path>` before proceeding. If unable to complete due to git errors, log the blocker in the ### Phase 6 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 6.2:** Commit with a descriptive message

- [x] Commit the staged changes with a conventional-commit message describing the fix, because PR #156 needs this remediation recorded against its head branch. Use the Bash tool from inside the `fix/pipeline-stdin-large-prompts` worktree to run a commit with message body `fix(pipeline): parse SUPERCLAUDE_PROMPT_MAX_BYTES defensively to avoid import-time hard-fail` and a body explaining that a misconfigured env var previously raised ValueError at module import (cascading ImportError) and now degrades to the default with a logged warning, resolving PR #156 review comment r3385368388. The commit message MUST end with the line `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`. Ensure the commit succeeds and captures only the two staged files. If a pre-commit `verify-sync` hook runs and fails for reasons unrelated to this change, log that in the ### Phase 6 Findings section of the ## Task Log / Notes. If unable to complete the commit, log the blocker in the ### Phase 6 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step 6.3:** Push to origin to update PR #156

- [x] Push the commit to the fork remote so PR #156 is updated, because the fix is not visible on the PR until pushed. Use the Bash tool from inside the `fix/pipeline-stdin-large-prompts` worktree to FIRST run `git remote -v` and confirm `origin` is `IronbellyOrg/IronClaude` (NEVER push to `upstream` / `SuperClaude-Org`), then run `git push origin fix/pipeline-stdin-large-prompts`. Ensure the push targets `origin` and the `fix/pipeline-stdin-large-prompts` branch only, and confirm from the push output that it updated the existing remote branch (the PR #156 head). After pushing, record the resulting commit SHA in the ### Phase 6 Findings section of the ## Task Log / Notes. If the push is rejected (e.g., the remote branch advanced), run `git fetch origin fix/pipeline-stdin-large-prompts` and `git rebase origin/fix/pipeline-stdin-large-prompts`, re-run the targeted tests, then push again. If unable to complete the push, log the blocker in the ### Phase 6 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

### Phase 7: POST Reflect Gate

**Step 7.1:** Run the POST reflect gate over the completed work

- [x] Run the POST reflect gate (standard depth) to audit this completed task against its driving intent, because the BUILD_REQUEST specifies POST_REFLECT_GATE: ENABLED with DEPTH: standard and no separate spec (SPEC_PATH: NONE), so the audit reads this task file and its outputs rather than an external spec. Invoke the reflect protocol in UC-2 (post-execution) standard mode against this task file `.dev/tasks/to-do/TASK-RF-prompt-max-bytes-parse-20260610040154/TASK-RF-prompt-max-bytes-parse-20260610040154.md` and the two modified files in the `fix/pipeline-stdin-large-prompts` worktree, having it classify any divergence under the 4-category deviation taxonomy (Authorized expansion / Necessary deviation / Drift / Regression) and confirm: the exact fix from the BUILD_REQUEST was encoded faithfully (helper placement, no new imports, typed `int`, no call-site change), all required env-parse test paths exist, and the validation/regression/lint steps passed. Record the reflect verdict (pass/fail), the deviation classifications, and the report path into the `reflect_post` frontmatter field of this task file and into the ### Phase 7 Findings section of the ## Task Log / Notes. If the reflect gate reports a Regression or Drift that is fixable, fix it in the worktree and re-run the targeted tests; if it reports an unfixable concern, record it as an Open Question. If unable to run the reflect gate, log the blocker in the ### Phase 7 Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

## Post-Completion Actions

- [x] Verify all checklist items are marked complete by scanning this task file for any remaining `- [ ]` items (excluding the Post-Completion Actions themselves and any embedded code-block examples), ensuring none remain unchecked. If unchecked items are found, determine whether they were intentionally skipped (with a blocker logged in the Task Log) or accidentally missed, and log any discrepancies in ### Follow-Up Items Identified below, then mark this item complete. Once done, mark this item as complete.

- [x] Verify all blocker entries in the Task Log have resolution notes by reading the Phase Findings and Follow-Up sections of this task file, ensuring every logged blocker includes a resolution status (Resolved or Unresolved with explanation). If any blocker entries lack resolution notes, add the missing resolution status, then mark this item complete. Once done, mark this item as complete.

- [x] Verify the two task outputs exist on disk and contain the changes by using Glob/Read to confirm `src/superclaude/cli/pipeline/process.py` contains the `_parse_prompt_max_bytes` helper and the helper-based `PROMPT_MAX_BYTES` assignment, and `tests/pipeline/test_process_stdin.py` contains the `TestPromptMaxBytesEnvParse` class (both in the `fix/pipeline-stdin-large-prompts` worktree), ensuring no expected deliverable is missing. If either file lacks the expected change, check the Task Log for a documented blocker; if missing without reason, log the gap in ### Follow-Up Items Identified below, then mark this item complete. Once done, mark this item as complete.

- [x] Confirm the test suites pass cleanly as a final check by confirming the Phase 3 results (Steps 3.2 and 3.4) reported 0 failures, or, if any subsequent edits were made in Phase 5/6/7, re-run `uv run pytest tests/pipeline/test_process_stdin.py -v` and `uv run pytest tests/pipeline/ tests/cli_portify/` from the `fix/pipeline-stdin-large-prompts` worktree to confirm the final codebase state is GREEN. Note "Tests verified in Phase 3" in the Task Log if no subsequent changes were made, ensuring the final state is clean. If a re-run fails, log the failure in ### Follow-Up Items Identified below, then mark this item complete. Once done, mark this item as complete.

- [x] Create a ### Task Summary section at the top of the ## Task Log / Notes section at the bottom of this task file using the templated format provided there, documenting: work completed (the helper added to `process.py`, the assignment swap, the `TestPromptMaxBytesEnvParse` class added to `test_process_stdin.py`), the commit SHA pushed to PR #156, challenges encountered, any deviations from the planned process with rationale, the lite QA gate verdict, the POST reflect verdict, and any blockers logged with resolution status. Once the summary is complete, mark this item as complete. Once done, mark this item as complete.

- [x] Update `completion_date` and `updated_date` to today's date and update task status to "🟢 Done" in the frontmatter, then add an entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.` Once done, mark this item as complete.

## Task Log / Notes 📋

### Task Summary

**Completion Date:** 2026-06-10

**Work Completed:**
- Helper added to process.py: `_parse_prompt_max_bytes(raw, default=16*1024*1024) -> int` inserted after `_log` (L24); returns default on `None`, catches `(TypeError, ValueError)` from `int(raw)`→warn+default, guards `value <= 0`→warn+default. No new imports.
- Assignment swap in process.py: bare `int(os.environ.get(...))` replaced by `PROMPT_MAX_BYTES: int = _parse_prompt_max_bytes(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES"))` (L56) — still typed `int`, no call-site change.
- Test class added to test_process_stdin.py: `TestPromptMaxBytesEnvParse` (6 methods, L413) covering non-integer/empty/"0"/"-1"/valid/None; helper added to module import.
- Commit pushed to PR #156: `445dab7a28a165e6b65aa3614adeadeb64035a79` (origin/fix/pipeline-stdin-large-prompts).

**Challenges Encountered:**
- `ruff` absent from the fresh worktree venv: Resolved by running it via `uv run --with ruff`.

**Deviations from Process:**
- ruff-format whitespace on the two in-scope files (Phase 4): Authorized expansion — Step 4.1 mandated `ruff format` on exactly these files; behavior unchanged. Classified by the POST reflect gate as the only divergence, non-blocking.

**QA Gate (lite):** PASS - 0 fix cycles (3 lens agents all PASS, zero findings).

**POST Reflect Verdict:** pass (UC-2, executor-disjoint) - 100% adherence, no Drift/Regression. Verdict in `reflect_post` frontmatter; rationale in Phase 7 Findings.

**Blockers Logged:**
- None.

**Follow-Up Required:** No. (Once PR #156 CI is green, the augmentcode review thread r3385368388 can be resolved.)

### Execution Log

<!-- TEMPLATE FOR EXECUTION LOG ENTRIES:
**[YYYY-MM-DD HH:MM]** - [Action taken]: [Brief description of what was done and outcome]
-->

**[2026-06-10 04:41]** - Task started: Updated status to "🟠 Doing" and start_date.

**[2026-06-10 05:00]** - Task completed: Updated status to "🟢 Done" and completion_date.

### Phase 1 - Preparation and Worktree Setup Findings

<!-- TEMPLATE FOR PHASE FINDINGS:
**[YYYY-MM-DD HH:MM]** - [Step X.Y]: [Finding or blocker description]
- **Status:** [Completed | Blocked]
- **Details:** [Specific information about what was found, created, or what blocked completion]
- **Blocker Reason (if blocked):** [Specific reason why this could not be completed]
- **Files Affected:** [List of files read, created, or modified]
-->

**[2026-06-10 04:42]** - Step 1.2: Isolated worktree created.
- **Status:** Completed
- **Details:** `git worktree add ../IronClaude-pr156 fix/pipeline-stdin-large-prompts` succeeded; branch tip `3a2db5f0`. The current `fix/prd-parallel-gate-advisory` working tree is untouched.
- **Worktree path (absolute):** `/config/workspace/IronClaude-pr156`
- **Files Affected:** none yet (worktree setup only)

### Phase 2 - Implementation Findings

**[2026-06-10 04:43]** - Steps 2.1 + 2.2: Implementation complete.
- **Status:** Completed
- **Details:** Inserted `_parse_prompt_max_bytes(raw, default)` helper after `_log` (L21) and before the `# Default 16 MiB` comment block; no new imports (`Optional`/`os`/`logging`/`_log` all pre-existing). Replaced the bare `int(os.environ.get(...))` assignment with `PROMPT_MAX_BYTES: int = _parse_prompt_max_bytes(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES"))` — still annotated `int`, no redundant default at call site, comment block preserved.
- **Files Affected:** `src/superclaude/cli/pipeline/process.py` (worktree)

### Phase 3 - Unit Tests Findings

**[2026-06-10 04:45]** - Steps 3.1-3.4: Tests added and all green.
- **Status:** Completed
- **Details:**
  - 3.1: Added `TestPromptMaxBytesEnvParse` (6 methods) + `_parse_prompt_max_bytes` to the module import.
  - 3.2: `uv run pytest tests/pipeline/test_process_stdin.py -v` → **19 passed** (13 pre-existing + 6 new).
  - 3.3: import-safety repro — `SUPERCLAUDE_PROMPT_MAX_BYTES=16MB`→`16777216`, `=0`→`16777216`, `=2048`→`2048`; **no exception** on any invocation (defect confirmed fixed).
  - 3.4: `uv run pytest tests/pipeline/ tests/cli_portify/` → **1302 passed, 1 skipped, 0 failed**. The 2 warnings are pre-existing in `invariant_pass.py:107` (unrelated to this change).
- **Files Affected:** `tests/pipeline/test_process_stdin.py` (worktree)

### Phase 4 - Lint & Format Findings

**[2026-06-10 04:48]** - Step 4.1: ruff format + check clean (scoped to two files).
- **Status:** Completed
- **Details:** `ruff` was absent from the fresh worktree venv; ran via `uv run --with ruff`. `ruff format` reformatted both files (collapsed the helper signature to one line; minor import-block spacing) and `ruff check --fix` applied 1 import-organization fix. Re-verified: "2 files already formatted" + "All checks passed!". Targeted tests re-run after format → 19 passed. Scoped to the two target files only; no repo-wide lint run (per the out-of-scope clause).
- **Files Affected:** `src/superclaude/cli/pipeline/process.py`, `tests/pipeline/test_process_stdin.py` (worktree)

### Phase 5 - Final QA Gate Findings

_QA gate verdicts, fix cycle counts, and unresolved issues (Open Questions) are recorded here._

**[2026-06-10 04:55]** - Phase 5 lite QA gate: **PASS**, 0 fix cycles.
- **Status:** Completed
- **Details:** 3 report-only lens agents all PASS — structural (rf-qa, 7/7), content (rf-qa-qualitative, 6/6), domain import-safety (rf-qa, 5/5). Zero findings → Steps 5.6 (fix) and 5.7 (verification) skipped per the "No findings" branch. Consolidated at `qa/qa-consolidated-findings.md`. Adversarial rigor: content lens mutation-tested the warning assertions; domain lens ran 24-input exhaustive + 8-value live-import trace.
- **Open Questions:** None.

### Phase 6 - Commit & Push Findings

**[2026-06-10 04:57]** - Steps 6.1-6.3: Committed and pushed to PR #156.
- **Status:** Completed
- **Details:** Staged ONLY `src/superclaude/cli/pipeline/process.py` + `tests/pipeline/test_process_stdin.py` (no `.claude/`, no `git add -A/-f`). Committed as `445dab7a` (2 files, +124/-18; message ends with the Co-Authored-By trailer). Confirmed `origin` = `IronbellyOrg/IronClaude` before pushing; `git push origin fix/pipeline-stdin-large-prompts` → `3a2db5f0..445dab7a`. No pre-commit hook failure.
- **Commit SHA:** `445dab7a28a165e6b65aa3614adeadeb64035a79`
- **Files Affected:** committed `process.py` + `test_process_stdin.py`

### Phase 7 - POST Reflect Gate Findings

**[2026-06-10 04:59]** - Step 7.1: POST reflect gate (UC-2, standard) — **PASS**.
- **Status:** Completed
- **Details:** Executor-disjoint audit (self-review agent that did NOT execute the work) independently re-verified the committed diff `445dab7a` against the BUILD_REQUEST intent. 100% adherence: faithful fix encoding (helper placement, no new imports, typed `int`, no call-site change), all 6 env-parse test paths present, validation evidence reproduced (19 targeted, import-safety repro, ruff clean), no scope creep (only the 2 in-scope files, no `.claude/`), commit message + trailer correct.
- **Deviation taxonomy:** None classifiable as Drift or Regression. Sole divergence = ruff-format whitespace on the two in-scope files → **Authorized expansion** (Step 4.1 mandated `ruff format` on exactly these files). No remediation required.
- **Verdict recorded to:** `reflect_post` frontmatter.

### Follow-Up Items Identified

<!-- TEMPLATE FOR FOLLOW-UP ITEMS:
- **[Priority: High/Medium/Low]** [Description of follow-up needed] - Identified in Step [X.Y]
-->

### Deviations from Process

<!-- TEMPLATE FOR DEVIATIONS:
**[YYYY-MM-DD HH:MM]** - Deviation from [Step X.Y]:
- **Expected:** [What the process specified]
- **Actual:** [What was done instead]
- **Rationale:** [Why this deviation was necessary]
-->

