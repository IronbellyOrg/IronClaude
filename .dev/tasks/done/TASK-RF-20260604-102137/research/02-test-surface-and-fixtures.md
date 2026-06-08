# Test Surface and Fixtures Research

Topic: Test & Verification
Status: Complete
Date: 2026-06-04

## 1. Rerun test surface: current coverage and fixtures

Searched `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py`, `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks_failure_modes.py`, and `/config/workspace/IronClaude/tests/sprint/test_handoff_record.py` for `_rerun_targets_passed`, `rerun_succeeded`, `phase-N-result`, `phase_result_json`, `is_validated_success`, `HandoffRecord`, and `pass_recovered`.

Findings:

- No existing test directly imports or calls `_rerun_targets_passed`; the import block in `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py` includes public rerun helpers but not `_rerun_targets_passed` (`/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py:40-51`).
- No test file currently references the local `rerun_succeeded` variable by name. The source uses it in `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1370-1374` to gate merge-back after `_rerun_targets_passed(...)`.
- Existing rerun orchestration tests exercise `_rerun_targets_passed` indirectly by stubbing `execute_sprint` to write a `phase-7-result.json` whose target status is `"pass"`, then asserting merge-back behavior. The clearest fixture is `_execute_sprint_writes_pass` in `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py:398-418`.
- Failure-mode tests include the best reusable phase-result JSON builder, `_phase_result_payload`, in `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks_failure_modes.py:91-130`. It constructs each result as:

```python
{
    "task": {
        "task_id": tid,
        "title": f"Task {tid}",
        "description": "",
        "dependencies": [],
        "command": "",
        "classifier": "",
    },
    "status": status,
    "turns_consumed": 5,
    "exit_code": 0 if status == "pass" else 1,
    "started_at": "2026-06-01T00:00:00+00:00",
    "finished_at": "2026-06-01T00:01:00+00:00",
    "output_bytes": 100,
    "gate_outcome": "pass" if status == "pass" else "fail",
    "reimbursement_amount": 0,
    "output_path": "",
}
```

and wraps those entries as:

```python
{
    "phase": _PHASE,
    "task_results": task_results,
    "recovery_history": recovery_history or [],
}
```

- The user-specified minimal dict shape is compatible with production `_rerun_targets_passed`, because the function only reads `task_results[*].task.task_id` and `task_results[*].status` (`/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1171-1177`). A test fixture can therefore use the smaller payload:

```python
{
    "phase": 7,
    "status": "pass_recovered",
    "task_results": [
        {"task": {"task_id": "T07.11"}, "status": "pass_recovered"}
    ],
}
```

## 2. Best existing test to mirror

Best mirror for the RED→GREEN regression is `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py` under `class TestRunOrchestration`, because that file already imports rerun helper functions from `superclaude.cli.sprint.rerun_tasks`, uses module-level helper setup, and directly covers rerun merge-back behavior.

Verbatim excerpt to mirror for the higher-level path (`/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py:398-418`):

```python
def _execute_sprint_writes_pass(target: str):
    """Return a fake execute_sprint that writes a PASS rerun result + produced
    transcript into the sub-config's bundle results dir."""

    def _fake(sub_config: SprintConfig):
        sub_results = sub_config.results_dir
        sub_results.mkdir(parents=True, exist_ok=True)
        rerun_result = {
            "task_results": [_task_result(target, TaskStatus.PASS, turns=1).to_dict()],
            "recovery_history": [],
        }
        (sub_results / "phase-7-result.json").write_text(
            json.dumps(rerun_result), encoding="utf-8"
        )
        # Produced transcript the merge-back copies to the canonical path.
        (sub_results / f"phase-7-task-{target}-output.txt").write_text(
            "rerun (passing) transcript\n", encoding="utf-8"
        )
        return None

    return _fake
```

Related merge-back assertions already present:

- `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py:421-457` asserts `run_rerun_tasks(...)` returns `0` and renames the original transcript to `*.failed-<ts>`.
- `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py:459-493` asserts a successful rerun emits one `phase_rerun_complete` event.

A direct unit-style predicate test is simpler and more surgical than copying the whole orchestration test, because the bug is isolated to `_rerun_targets_passed`'s predicate.

## 3. Clean RED→GREEN test shape for `_rerun_targets_passed`

Import path and call signature:

```python
from superclaude.cli.sprint.rerun_tasks import _rerun_targets_passed

_rerun_targets_passed(phase_result_json: Path, targets: list[str]) -> bool
```

The function is module-level and therefore importable despite the underscore prefix. Current source signature is in `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1165`; the current buggy predicate is `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1177`:

```python
return bool(targets) and all(status_by_id.get(t) == "pass" for t in targets)
```

Recommended location: `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py`, adding `_rerun_targets_passed` to the existing import block at `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py:40-51`, then adding a focused class near `TestRunOrchestration` or just before it.

Recommended method name:

```python
class TestRerunTargetsPassed:
    def test_pass_recovered_target_counts_as_passed(self, tmp_path: Path):
        """R-F rerun merge gate: PASS_RECOVERED is a successful target result."""
```

Recommended fixture construction and assertion:

```python
result_path = tmp_path / "phase-7-result.json"
result_path.write_text(
    json.dumps(
        {
            "phase": 7,
            "status": "pass_recovered",
            "task_results": [
                {
                    "task": {"task_id": "T07.11"},
                    "status": "pass_recovered",
                }
            ],
        }
    ),
    encoding="utf-8",
)

assert _rerun_targets_passed(result_path, ["T07.11"]) is True
```

Why this is RED→GREEN:

- RED now: `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:1177` compares each target status to literal `"pass"`, so `"pass_recovered"` returns `False`.
- GREEN after fix: convert status strings through `TaskStatus(...)` and use `.is_success`, or otherwise include `TaskStatus.PASS_RECOVERED.value` as successful. `TaskStatus.is_success` already returns `True` for both `PASS` and `PASS_RECOVERED` (`/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:46-58`).

Higher-level alternative:

- Add `_execute_sprint_writes_pass_recovered(target: str)` mirroring `_execute_sprint_writes_pass` (`/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py:398-418`) but using `TaskStatus.PASS_RECOVERED` and `exit_code=1` via `_task_result` if needed, then run `run_rerun_tasks(...)` like `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py:421-457` and assert exit `0` plus transcript rename or `phase_rerun_complete` event.
- This proves merge-back proceeds end-to-end, but it is more expensive and may be less direct because `run_rerun_tasks` has unrelated locking/SHA/merge side effects. For the requested regression, the direct predicate test is the cleanest first test.

## 4. Handoff `is_validated_success` surface

`/config/workspace/IronClaude/tests/sprint/test_handoff_record.py` currently tests HandoffRecord serialization and derivation only; it does not import or test `is_validated_success` (`/config/workspace/IronClaude/tests/sprint/test_handoff_record.py:7-13`, `/config/workspace/IronClaude/tests/sprint/test_handoff_record.py:48-106`).

Existing HandoffRecord fixture shape is `_record()` in `/config/workspace/IronClaude/tests/sprint/test_handoff_record.py:31-45`:

```python
def _record() -> HandoffRecord:
    return HandoffRecord(
        schema_version=1,
        task_id="T01.02",
        phase=1,
        status="pass",
        gate_outcome="pass",
        turns_consumed=7,
        exit_code=0,
        output_path="/r/phase-1-task-T01.02-output.txt",
        started_at="2026-06-03T10:00:00+00:00",
        finished_at="2026-06-03T10:01:00+00:00",
        produced_artifacts=["/r/phase-1-task-T01.02-output.txt"],
        consumed_upstreams=["T01.01"],
    )
```

If the source fix touches handoff resume semantics, add a second focused test in `/config/workspace/IronClaude/tests/sprint/test_handoff_record.py`:

```python
from superclaude.cli.sprint.handoff import is_validated_success


def test_is_validated_success_accepts_pass_recovered_with_pass_gate() -> None:
    """H5 resume skip: PASS_RECOVERED with a passing gate is validated success."""
    rec = _record()
    rec.status = "pass_recovered"
    rec.gate_outcome = "pass"

    assert is_validated_success(rec) is True
```

Why this is RED→GREEN if `handoff.py` is in scope:

- RED now: `/config/workspace/IronClaude/src/superclaude/cli/sprint/handoff.py:34-35` returns `False` unless `record.status == TaskStatus.PASS.value`.
- GREEN after fix: parse `record.status` as `TaskStatus(record.status)` and require `.is_success`, then retain the existing successful-gate check in `/config/workspace/IronClaude/src/superclaude/cli/sprint/handoff.py:36-40`.

This handoff test is optional relative to the immediate rerun merge-back bug unless the implementation updates `handoff.py.is_validated_success`.

## 5. Test conventions and run command

Observed conventions:

- `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py` uses module-level helper functions, one `TestXxx` class per concept, and `tmp_path` throughout; the module docstring explicitly states this convention at `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py:17-20`.
- `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks_failure_modes.py` marks integration classes with `@pytest.mark.integration`, uses `CliRunner`, and stubs side effects with `unittest.mock.patch` (`/config/workspace/IronClaude/tests/sprint/test_rerun_tasks_failure_modes.py:23-33`, `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks_failure_modes.py:249-251`).
- `test_handoff_record.py` uses top-level function tests rather than classes (`/config/workspace/IronClaude/tests/sprint/test_handoff_record.py:48-106`).
- Method names follow `test_<behavior>`; docstrings are common for behavior/spec context in rerun tests, especially for integration and regression cases.
- JSON files are written with `Path.write_text(..., encoding="utf-8")`; fixture JSON often uses `json.dumps(...)`, sometimes with `indent=2` and trailing newline in failure-mode tests (`/config/workspace/IronClaude/tests/sprint/test_rerun_tasks_failure_modes.py:158-160`, `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py:409-411`).

Recommended suite command:

```bash
uv run pytest tests/sprint/ -q
```

## 6. Final recommendation

Primary RED→GREEN test:

- Target module: `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py`
- Target class: new `TestRerunTargetsPassed`
- Method: `test_pass_recovered_target_counts_as_passed`
- Import: add `_rerun_targets_passed` to `from superclaude.cli.sprint.rerun_tasks import (...)`
- Fixture: write `tmp_path / "phase-7-result.json"` with a target `T07.11` whose serialized status is `"pass_recovered"`
- Assertion: `assert _rerun_targets_passed(result_path, ["T07.11"]) is True`

Optional companion if handoff is fixed:

- Target module: `/config/workspace/IronClaude/tests/sprint/test_handoff_record.py`
- Method: `test_is_validated_success_accepts_pass_recovered_with_pass_gate`
- Import: `from superclaude.cli.sprint.handoff import is_validated_success`
- Fixture: mutate `_record()` to `status = "pass_recovered"`, `gate_outcome = "pass"`
- Assertion: `assert is_validated_success(rec) is True`

Summary: the direct `_rerun_targets_passed` test is the smallest evidence-based regression: it fails exactly because the current predicate is `== "pass"` and passes once the predicate recognizes `TaskStatus.PASS_RECOVERED.is_success`.
