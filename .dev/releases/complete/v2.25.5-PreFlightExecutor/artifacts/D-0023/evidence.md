# D-0023 Evidence — T04.01: Integrate execute_preflight_phases() into execute_sprint()

## Summary

`execute_preflight_phases(config)` is called exactly once in `execute_sprint()` in
`src/superclaude/cli/sprint/executor.py`, before the main phase loop.

## Insertion Point

**File**: `src/superclaude/cli/sprint/executor.py`
**Line**: ~532 (after orphan cleanup, before `try: for phase in config.active_phases`)

```python
# Execute all python-mode phases via preflight executor before the main loop.
# Removing this single call reverts to all-Claude behavior (R-051 rollback property).
# Lazy import breaks the preflight → executor → preflight circular import cycle.
from .preflight import execute_preflight_phases  # noqa: PLC0415
preflight_results = execute_preflight_phases(config)
```

## Circular Import Resolution

A top-level import created a circular dependency:
- `executor.py` → `preflight.py` (to call `execute_preflight_phases`)
- `preflight.py` → `executor.py` (to import `AggregatedPhaseReport`)

**Resolution**: Lazy (local) import of `execute_preflight_phases` inside `execute_sprint()`.
Python resolves the cycle because `executor.py` is fully initialized before `preflight.py`
needs it (the lazy import only runs at call time, not at module load time).

## Skip Condition (T04.02)

```python
# Python-mode phases were already executed by preflight; skip here.
if phase.execution_mode == "python":
    continue
```

## Rollback Property (R-051)

Removing the `from .preflight import execute_preflight_phases` + `preflight_results = execute_preflight_phases(config)` lines (2 lines) plus the `if phase.execution_mode == "python": continue` block reverts to all-Claude behavior.

## Verification

- `uv run pytest tests/sprint/ -v --tb=short` → **696 passed, 0 failed**
- Existing 46 preflight tests all pass after the change
