# Test-Site Inventory — Step 2.2

**Date:** 2026-06-05
**Worktree root:** `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-rerun-pass-recovered`
**Seed evidence:** `research/02-test-surface-and-fixtures.md:99-151`, `research/04-gate-resolutions.md:25-36`

| Test Site | Worktree File | Existing Test/Import Context | New Case Required | RED Reason | GREEN Criterion | Command |
|-----------|---------------|------------------------------|-------------------|------------|-----------------|---------|
| T1 (CRITICAL — S1) | `tests/sprint/test_rerun_tasks.py` | `_rerun_targets_passed` is **NOT** in the `from superclaude.cli.sprint.rerun_tasks import (...)` block (lines 40-51). No `TestRerunTargetsPassed` class exists yet. | Add `_rerun_targets_passed` to the import block; add `class TestRerunTargetsPassed:` with `test_pass_recovered_target_counts_as_passed` writing a `phase-7-result.json` fixture and asserting `_rerun_targets_passed(result_path, ["T07.11"]) is True`. | Old literal `status_by_id.get(t) == "pass"` (`rerun_tasks.py:1216`) returns `False` for `"pass_recovered"`. | New `is_success` coercion returns `True` for `"pass_recovered"`. | `uv run pytest tests/sprint/test_rerun_tasks.py::TestRerunTargetsPassed::test_pass_recovered_target_counts_as_passed -q` |
| T2 (HIGH — S2) | `tests/sprint/test_resume_contract.py` | `is_validated_success` imported (line 8). Target parametrized test `test_is_validated_success_only_for_pass_plus_gate_success` at line 55 uses a `cases` list of `(TaskStatus, GateOutcome, expected)` tuples + `_record(task_id, status, gate)` helper (line 40). | Append `(TaskStatus.PASS_RECOVERED, GateOutcome.PASS, True)` to the `cases` list. | Old `record.status != TaskStatus.PASS.value` (`handoff.py:34`) returns `False` for `"pass_recovered"`+good gate. | New coercion + `.is_success` returns `True`; existing failing-gate cases still return `False` (gate requirement preserved). | `uv run pytest tests/sprint/test_resume_contract.py::test_is_validated_success_only_for_pass_plus_gate_success -q` |
| T3 (LOW — S3) | (none) | `_print_investigation_summary` display-only. | **No dedicated test.** Covered by full `tests/sprint/` suite for import/runtime compatibility (research/02 + task Key constraints). | n/a | Full sprint suite green. | `uv run pytest tests/sprint/ -q` |

## ✅ CARRIED CORRECTION F1 [MEDIUM] — CRITICAL RED-fixture shape (authoritative)

The task's **inline** Step 4.1 fixture `{"task": {"task_id": "T07.11"}, "status": "pass_recovered"}` is **WRONG** — `_rerun_targets_passed` parses `data.get("task_results", [])` (`rerun_tasks.py:1211`), so an entry not wrapped in `task_results` is never read, `status_by_id` stays empty, and the GREEN assertion `... is True` **fails even after the correct source fix** (RED → still-RED).

**Use the wrapped shape from `research/02-test-surface-and-fixtures.md:36-39`:**

```json
{
  "status": "pass_recovered",
  "task_results": [
    {"task": {"task_id": "T07.11"}, "status": "pass_recovered"}
  ]
}
```

The top-level `"status"` key is harmless; the load-bearing element is the `"task_results"` list wrapper. The T1 test MUST construct the fixture this way.

## Import/convention notes for Phase 4

- T1: extend the existing `from superclaude.cli.sprint.rerun_tasks import (...)` tuple alphabetically; follow the file's existing `class Test*` + `tmp_path` fixture style (e.g. `TestExtractPhaseSubset` at line 98).
- T2: do not restructure the parametrized test — only append one tuple to the `cases` list to preserve the gate-success coverage already present.
