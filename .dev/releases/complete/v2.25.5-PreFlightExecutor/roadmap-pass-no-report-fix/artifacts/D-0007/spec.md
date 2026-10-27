# D-0007 — Call Site in `execute_sprint()`

## Task: T03.01

## Deliverable

Call site for `_write_preliminary_result()` inserted in `execute_sprint()` in
`src/superclaude/cli/sprint/executor.py`, guarded by `if exit_code == 0:`,
placed after `finished_at` capture and signal/shutdown check, before
`_determine_phase_status()`.

## Location

- **File**: `src/superclaude/cli/sprint/executor.py`
- **Lines inserted**: 695–707 (after signal check at line 690–693, before `_determine_phase_status` at line 709)

## Inserted Code

```python
                # Write a preliminary result sentinel so _determine_phase_status()
                # always finds a result file for exit_code=0 phases that wrote no report.
                # Guard: only for successful exits; non-zero paths must not reach this.
                if exit_code == 0:
                    _wrote_preliminary = _write_preliminary_result(
                        config, phase, started_at.timestamp()
                    )
                    debug_log(
                        _dbg,
                        "preliminary_result_write",
                        path=f"{'executor-preliminary (option_d)' if _wrote_preliminary else 'agent-written/option_a_or_noop'}",
                    )
```

## Ordered-Triple Invariant

| Call | Line | Note |
|---|---|---|
| `_write_preliminary_result(...)` | 699 | Inside `if exit_code == 0:` guard |
| `_determine_phase_status(...)` | 709 | Unconditional |
| `_write_executor_result_file(...)` | 722 | Unconditional |

699 < 709 < 722 — strict sequential ordering. No conditional branches between
the three calls that could reorder them.

## Acceptance Criteria Status

| Criterion | Status |
|---|---|
| Call site exists in `execute_sprint()` guarded by `if exit_code == 0:` | PASS |
| Ordered-triple invariant: preliminary < determine_status < executor_result | PASS |
| DEBUG log emits `executor-preliminary (option_d)` or `agent-written/option_a_or_noop` | PASS |
| Non-zero exit paths do not reach `_write_preliminary_result()` (FR-005) | PASS |
