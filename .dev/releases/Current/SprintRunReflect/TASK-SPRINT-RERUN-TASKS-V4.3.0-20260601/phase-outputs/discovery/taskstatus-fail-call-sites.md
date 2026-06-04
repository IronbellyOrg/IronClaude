# TaskStatus.FAIL Call Sites Inventory — Phase 1 Step 1.4

**Task:** TASK-SPRINT-RERUN-TASKS-V4.3.0-20260601
**Step:** 1.4 — Inventory existing TaskStatus.FAIL call sites (Resolution 1 preparation)
**Date:** 2026-06-02
**Worktree:** /config/workspace/IronClaude/.claude/worktrees/SprintReRun (branch SprintReRun)

## Purpose

Per `research/06-gate-resolutions.md` Resolution 1 (AUTHORITATIVE OVERRIDE of `research/03-integration-points.md` IP-3 and `research/05-template-examples.md` §4.3), the TDD line 119 mandates the rename `TaskStatus.FAIL` → `TaskStatus.FAIL_TERMINAL` keeping serialized string `"fail"`. This file is the source of truth for Step 1.5's atomic rename — every site listed here MUST be updated.

## Search Patterns

Pattern: `TaskStatus\.FAIL\b` (word boundary excludes `FAIL_TERMINAL` and `FAIL_RECOVERABLE`)

Globs covered:
- `src/superclaude/cli/sprint/**/*.py`
- `tests/**/*.py`
- Remainder of `src/superclaude/**/*.py`

Pre-rename sanity check: `grep -rn "TaskStatus\.FAIL_TERMINAL\|TaskStatus\.FAIL_RECOVERABLE" src/ tests/` returned ZERO matches — no partial application exists.

## Inventory — src/superclaude/cli/sprint/ (12 occurrences across 3 files)

| File | Line | Context Snippet | Notes |
|---|---|---|---|
| src/superclaude/cli/sprint/models.py | 53 | `return self in (TaskStatus.FAIL, TaskStatus.INCOMPLETE)` | SPECIAL — `is_failure` property body, widens per Resolution 2 to `(TaskStatus.FAIL_TERMINAL, TaskStatus.FAIL_RECOVERABLE, TaskStatus.INCOMPLETE)` |
| src/superclaude/cli/sprint/preflight.py | 178 | `TaskStatus.PASS if classification == "pass" else TaskStatus.FAIL` | Rename to `TaskStatus.FAIL_TERMINAL` |
| src/superclaude/cli/sprint/preflight.py | 184 | `task_status = TaskStatus.FAIL` | Rename to `TaskStatus.FAIL_TERMINAL` |
| src/superclaude/cli/sprint/preflight.py | 205 | `tasks_failed = sum(1 for tr in task_results if tr.status == TaskStatus.FAIL)` | Rename to `TaskStatus.FAIL_TERMINAL` |
| src/superclaude/cli/sprint/executor.py | 324 | `report.tasks_failed = sum(1 for r in task_results if r.status == TaskStatus.FAIL)` | Rename to `TaskStatus.FAIL_TERMINAL` |
| src/superclaude/cli/sprint/executor.py | 570 | `task_result.status = TaskStatus.FAIL` | Rename to `TaskStatus.FAIL_TERMINAL` |
| src/superclaude/cli/sprint/executor.py | 774 | `synth_status = TaskStatus.FAIL` | Rename to `TaskStatus.FAIL_TERMINAL` |
| src/superclaude/cli/sprint/executor.py | 797 | `if updated_result.status == TaskStatus.FAIL and synth_status != TaskStatus.FAIL:` | Rename BOTH instances to `TaskStatus.FAIL_TERMINAL` (two occurrences on one line) |
| src/superclaude/cli/sprint/executor.py | 894 | `# (set GateOutcome.FAIL / TaskStatus.FAIL) as an intentional v3.1` | COMMENT — rename for accuracy |
| src/superclaude/cli/sprint/executor.py | 910 | `task_result.status = TaskStatus.FAIL` | Rename to `TaskStatus.FAIL_TERMINAL` |
| src/superclaude/cli/sprint/executor.py | 922 | `task_result.status = TaskStatus.FAIL` | Rename to `TaskStatus.FAIL_TERMINAL` |
| src/superclaude/cli/sprint/executor.py | 1020 | `status = TaskStatus.FAIL` | Rename to `TaskStatus.FAIL_TERMINAL` (within `_classify_from_result_file` per Phase 4 IP-9) |

## Inventory — tests/ (31 occurrences across 11 files)

| File | Line | Context Snippet | Notes |
|---|---|---|---|
| tests/integration/test_sprint_wiring.py | 179 | `assert returned.status == TaskStatus.FAIL` | Rename |
| tests/sprint/test_anti_instinct_sprint.py | 239 | `assert result.status == TaskStatus.FAIL  # full mode FAILS the task` | Rename |
| tests/sprint/test_anti_instinct_sprint.py | 283 | `assert result.status == TaskStatus.FAIL` | Rename |
| tests/sprint/test_anti_instinct_sprint.py | 389 | `assert result.status == TaskStatus.FAIL` | Rename |
| tests/sprint/test_context_injection.py | 89 | `r = _result(task_id="T01.01", exit_code=1, status=TaskStatus.FAIL)` | Rename |
| tests/sprint/test_context_injection.py | 165 | `_result(task_id="T01.02", status=TaskStatus.FAIL),` | Rename |
| tests/sprint/test_context_injection.py | 278 | `status=TaskStatus.FAIL,` | Rename |
| tests/sprint/test_wiring_budget_scenarios.py | 205 | `assert returned.status == TaskStatus.FAIL` | Rename |
| tests/sprint/test_backward_compat_regression.py | 535 | `assert TaskStatus.FAIL.value == "fail"` | SPECIAL — wire-format back-compat test; rename to `TaskStatus.FAIL_TERMINAL.value == "fail"` (serialized value MUST remain `"fail"`) |
| tests/sprint/test_models.py | 1016 | `status=TaskStatus.FAIL,` | Rename |
| tests/sprint/test_preflight.py | 881 | `status=TaskStatus.FAIL,` | Rename |
| tests/sprint/test_executor.py | 712 | `assert results[0].status == TaskStatus.FAIL` | Rename |
| tests/sprint/test_executor.py | 835 | `self._make_task_result("T02.02", TaskStatus.FAIL, 5),` | Rename |
| tests/sprint/test_executor.py | 845 | `self._make_task_result("T02.01", TaskStatus.FAIL, 3),` | Rename |
| tests/sprint/test_executor.py | 888 | `self._make_task_result("T02.01", TaskStatus.FAIL, 5),` | Rename |
| tests/sprint/test_executor.py | 898 | `self._make_task_result("T02.02", TaskStatus.FAIL, 5),` | Rename |
| tests/sprint/test_executor.py | 939 | `self._make_task_result("T03.02", TaskStatus.FAIL, 3),` | Rename |
| tests/sprint/test_executor.py | 967 | `self._make_task_result("T03.02", TaskStatus.FAIL, 3),` | Rename |
| tests/sprint/test_executor.py | 984 | `self._make_task_result("T03.03", TaskStatus.FAIL, 2),` | Rename |
| tests/sprint/test_executor.py | 1139 | `assert results[2].status == TaskStatus.FAIL` | Rename |
| tests/sprint/test_e2e_trailing.py | 472 | `TaskStatus.FAIL,` | Rename |
| tests/sprint/test_e2e_trailing.py | 563 | `status=TaskStatus.FAIL,` | Rename |
| tests/v3.3/test_gate_rollout_modes.py | 334 | `assert result.status == TaskStatus.FAIL` | Rename |
| tests/v3.3/test_gate_rollout_modes.py | 367 | `evidence="full mode: empty output → gate FAIL → TaskStatus.FAIL, metrics recorded",` | STRING LITERAL — rename for doc accuracy |
| tests/v3.3/test_gate_rollout_modes.py | 616 | `assert result.status == TaskStatus.FAIL` | Rename |
| tests/v3.3/test_gate_rollout_modes.py | 818 | `assert result.status == TaskStatus.FAIL` | Rename |
| tests/v3.3/test_wiring_points_e2e.py | 950 | `status=TaskStatus.FAIL,` | Rename |
| tests/v3.3/test_wiring_points_e2e.py | 2002 | `assert results_b[0].status == TaskStatus.FAIL, (` | Rename |
| tests/v3.3/test_wiring_points_e2e.py | 2022 | `"scenario_b_status": TaskStatus.FAIL.value,` | Rename (`.value` still returns `"fail"` after rename) |
| tests/pipeline/test_full_flow.py | 435 | `assert result.status == SprintTaskStatus.FAIL  # full mode fails task` | ALIASED — `from .models import TaskStatus as SprintTaskStatus`; rename to `SprintTaskStatus.FAIL_TERMINAL` |
| tests/pipeline/test_full_flow.py | 463 | `assert result.status == SprintTaskStatus.FAIL` | Rename to `SprintTaskStatus.FAIL_TERMINAL` |

## Inventory — Remainder of src/superclaude/ (0 occurrences)

Grep against `src/superclaude/` excluding `cli/sprint/` returned ZERO matches. No TaskStatus.FAIL references exist outside the sprint module.

## Summary

- **Total occurrences:** 43 (12 in sprint module + 31 in tests + 0 elsewhere)
- **Total files affected:** 14 (3 sprint source + 11 test files)
- **Special cases:**
  - `models.py:53` — `is_failure` property widens per Resolution 2 (not just rename)
  - `models.py` enum member definition site (around line 45 per researcher 2 §3.3) — atomic rename `FAIL = "fail"` → `FAIL_TERMINAL = "fail"` (the rename target itself, not in this grep because pattern is `TaskStatus.FAIL\b` not the bare definition)
  - `executor.py:894` — comment string, rename for accuracy
  - `executor.py:797` — TWO occurrences on one line, both rename
  - `test_backward_compat_regression.py:535` — wire-format value test; `.value` MUST remain `"fail"` after rename (validates the back-compat contract)
  - `test_full_flow.py:435,463` — uses `SprintTaskStatus` alias; rename accordingly
  - `test_gate_rollout_modes.py:367` — string literal in `evidence=` keyword; rename for doc accuracy

## Source Commands

1. `grep -rn "TaskStatus\.FAIL\b" src/superclaude/cli/sprint/` → 12 matches
2. `grep -rn "TaskStatus\.FAIL\b" tests/` → 31 matches (includes `SprintTaskStatus.FAIL` due to substring match on suffix)
3. `grep -rn "TaskStatus\.FAIL\b" src/superclaude/ --include="*.py" | grep -v "src/superclaude/cli/sprint/"` → 0 matches
4. `grep -rn "TaskStatus\.FAIL_TERMINAL\|TaskStatus\.FAIL_RECOVERABLE\|SprintTaskStatus\.FAIL_TERMINAL\|SprintTaskStatus\.FAIL_RECOVERABLE" src/ tests/` → 0 matches (no partial application)

## Conclusion

All 43 call sites enumerated with file paths and line numbers. Step 1.5 atomic rename will:
1. Edit `models.py` — rename enum member `FAIL = "fail"` → `FAIL_TERMINAL = "fail"`, add `FAIL_RECOVERABLE = "fail_recoverable"`, widen `is_failure` body at line 53.
2. Edit each of the 13 other files using per-file Edits with `replace_all: true` on the pattern `TaskStatus.FAIL` → `TaskStatus.FAIL_TERMINAL` (per-file scope to avoid cross-file ambiguity).
3. For `test_full_flow.py` — additional Edit replacing `SprintTaskStatus.FAIL` → `SprintTaskStatus.FAIL_TERMINAL`.
4. Verify with `grep -rn "TaskStatus\.FAIL\b" src/superclaude/cli/sprint/ tests/` returning ZERO matches post-edit.
