# D-0010 — Preflight Phase Isolation Evidence

## Task: T03.04

## Deliverable

Verification that python/skip preflight phases are handled by
`execute_preflight_phases()` and never reach the new `_write_preliminary_result()`
code.

## Isolation Mechanism

In `execute_sprint()`, before the main loop body (lines 531–544):

```python
# Python-mode phases were already executed by preflight; skip here.
if phase.execution_mode == "python":
    continue

# Skip-mode phases: record SKIPPED with no subprocess launched.
if phase.execution_mode == "skip":
    ...
    continue
```

Both `python` and `skip` phases `continue` immediately — they never enter
the subprocess launch block, never set `exit_code`, and never reach the
`if exit_code == 0:` guard at line 698.

## Preflight Execution Path

1. `execute_preflight_phases(config)` is called at line ~534 (before main loop)
2. It handles all `execution_mode == "python"` phases independently
3. Results are merged back into `sprint_result` after the main loop

The new `_write_preliminary_result()` code lives inside:
```
for phase in config.active_phases:
    if phase.execution_mode == "python": continue   # ← python exits here
    if phase.execution_mode == "skip":   continue   # ← skip exits here
    ...
    # subprocess block (only claude-mode phases reach here)
    ...
    if exit_code == 0:
        _write_preliminary_result(...)              # ← never reached by preflight
```

## Preflight Status Verification

`execute_preflight_phases()` returns `PhaseResult` objects with
`PhaseStatus.PREFLIGHT_PASS` (or `PREFLIGHT_FAIL`) status. These are set by
the preflight executor, not by `_determine_phase_status()`, and are merged
after the main loop. The new call site has no effect on preflight results.

## Acceptance Criteria Status

| Criterion | Status |
|---|---|
| Python/skip phases confirmed handled by `execute_preflight_phases()` only | PASS |
| These phases never enter the main Claude loop where `_write_preliminary_result()` is called | PASS |
| Preflight phases still yield `PREFLIGHT_PASS` status (architecture invariant) | PASS |
