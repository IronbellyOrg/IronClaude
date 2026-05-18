# All Fixes Consolidated Summary

**Date:** 2026-05-18
**Task:** TASK-RF-20260518-015659 — Sprint Runner Deterministic Fixes

## C3 — Timeout Formula Reconciliation
- **Production change:** `src/superclaude/cli/sprint/executor.py:86` changed `max_turns * 60` → `max_turns * 120 + 300` (matches canonical at L1106 and `sprint/process.py:115`). Located in `SprintGatePolicy.build_remediation_step` which has zero production callers per Researcher 3 IP-7.
- **New test class:** `tests/sprint/test_executor.py::TestTimeoutFormulaConsistency` (2 tests) — asserts the literal canonical formula values across `max_turns ∈ {1, 50, 100, 500}`.
- **Gate verdict:** G1 PASS cycle 1 — see `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/reviews/c3-qa-report.md` and `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/plans/c3-verdict.md`
- **pytest:** 2/2 PASS — see `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-3-c3-summary.md`

## C4 — phase_start JSONL Emission in Per-Task Branch
- **Production change:** `src/superclaude/cli/sprint/executor.py` — inserted `logger.write_phase_start(phase, started_at)` in the per-task branch immediately after `started_at = datetime.now(timezone.utc)` (between L1264 and L1266 in the discovery line numbering; lines shifted +1 after insertion). The per-phase fallback at L1328 (which already had this call) was NOT modified.
- **New test:** `tests/sprint/test_regression_gaps.py::TestSprintLoggerPhaseStart::test_phase_start_emitted_for_per_task_branch` — uses mocked `_parse_phase_tasks`/`execute_phase_tasks`/`run_post_phase_wiring_hook` to fire the per-task branch, asserts (a) phase_start present in JSONL, (b) fields present (phase, phase_name, phase_file, timestamp), (c) phase==1, (d) phase_start precedes phase_complete. Also added `TaskEntry` to module imports.
- **Gate verdict:** G2 PASS cycle 1 — see `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/reviews/c4-qa-report.md` and `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/plans/c4-verdict.md`
- **pytest:** 4/4 PASS (1 new + 3 existing in class) — see `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-4-c4-summary.md`

## C1 — Watchdog Split + startup_stall_timeout Field
- **Production changes (4 files):**
  1. `src/superclaude/cli/sprint/models.py` — new dataclass field `startup_stall_timeout: int = 300  # 0 = disabled; fires when no events received yet (process never began streaming)` between `stall_timeout` (kept `0`) and `stall_action` (kept `"warn"`).
  2. `src/superclaude/cli/sprint/config.py` — `load_sprint_config` signature + constructor pass-through.
  3. `src/superclaude/cli/sprint/commands.py` — new `@click.option("--startup-stall-timeout", ...)` decorator + `run()` parameter + `load_sprint_config(...)` pass-through.
  4. `src/superclaude/cli/sprint/executor.py:1365-1404` — split single watchdog branch into TWO mutually-exclusive branches: (a) startup-stall guard (`events_received == 0`, `[WATCHDOG] Startup-stall detected`), (b) mid-stall guard (`events_received > 0`, `[WATCHDOG] Mid-stall detected`). Single-fire `_stall_acted` reset clause preserved.
- **New tests (5 total):**
  - 3 config defaults in `tests/sprint/test_config.py::TestStartupStallTimeoutDefaults`
  - 2 watchdog integration in `tests/sprint/test_watchdog.py::TestStartupStallWatchdog` (uses `MagicMock()` for `stdin` workaround for pre-existing commit-4799719 issue)
- **Gate verdict:** G3 PASS cycle 1 — see `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/reviews/c1-qa-report.md` and `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/plans/c1-verdict.md`
- **pytest:** 5/5 PASS — see `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-5-c1-summary.md`

## C2 — Per-Task Output-File Collision Elimination
- **Production changes (2 files):**
  1. `src/superclaude/cli/sprint/models.py:473-478` — additive helpers `task_output_file(self, phase, task)` and `task_error_file(self, phase, task)` inserted between `error_file` and `result_file`. Path format: `phase-{N}-task-{task.task_id}-{output,errors}.txt`. Forward-ref `"TaskEntry"` annotation. Existing `output_file`/`error_file` byte-unchanged (Q2 invariant).
  2. `src/superclaude/cli/sprint/executor.py:1086-1115` — 3 line changes inside `_run_task_subprocess`: output_file kwarg, error_file kwarg, post-subprocess size read all swapped to `task_output_file`/`task_error_file`. C3 timeout (`max_turns * 120 + 300` at L1106) preserved.
- **New tests (5 total):**
  - 3 helper unit tests in `tests/sprint/test_models.py::TestTaskOutputFileHelpers`
  - 1 collision integration test in `tests/pipeline/test_process.py::TestClaudeProcessOutputFileCollision` using `sys.executable -c "echo stdin"` stand-in. LOAD-BEARING on C2 — asserts `out_a != out_b` up front before subprocesses run.
  - 1 mock-capture test in `tests/sprint/test_executor.py::test_run_task_subprocess_uses_task_output_file` — asserts the kwarg replacements AND C3 timeout consistency.
- **Gate verdict:** G4 PASS cycle 1 (11/15 checks per agent's 15-item run) — see `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/reviews/c2-qa-report.md` and `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/plans/c2-verdict.md`
- **pytest:** 5/5 PASS — see `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-6-c2-summary.md`

## Phase 7 — make lint
**Result:** PASSED for changed files (10 files, 0 errors via `uv run ruff check`); 241 pre-existing repo-wide errors documented out-of-scope (mostly in `.dev/releases/complete/...` frozen artifacts and unrelated CLI modules).
See `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-7-make-lint-summary.md`.

## Phase 7 — sprint+pipeline pytest
**Result:** 1350/1408 PASSED; 57 pre-existing `.stdin AttributeError` failures (from commit 4799719, 2026-04-20); 1 skipped. **13/13 NEW tests added by this task all PASS.**
See `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-7-sprint-pipeline-pytest-summary.md` and `.../plans/phase-7-pytest-verdict.md`.

## Phase 7 — make test (full suite)
**Result:** 5644/5813 PASSED; 63 failures (57 pre-existing stdin + 4 caused by the in-flight sprint Phase 6 concurrently editing task-builder SKILL.md and rf-* agents + 2 wiring tests unrelated to sprint runner) + 1 collection error. **0 failures attributable to C1-C4.**
See `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-7-make-test-summary.md` and `.../plans/phase-7-make-test-verdict.md`.

## Overall
- All 4 fix clusters (C3, C4, C1, C2) implemented and passing.
- All 4 phase-gate QA verdicts PASS cycle 1 (G1, G2, G3, G4).
- 13 new tests, 13/13 PASS.
- 0 regressions caused by this task; all observed failures pre-existing or external (concurrent sprint Phase 6).
- C5 (--no-session-persistence), C6 (axis-fan-out), C7 (per-task watchdog coverage) documented as Follow-Up Items per BUILD_REQUEST.

Ready for G5 qualitative gate.
