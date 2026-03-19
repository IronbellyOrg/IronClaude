# D-0030: remediation_attempts Counter in .roadmap-state.json

## Summary

Added `remediation_attempts` field to `.roadmap-state.json` schema with default value 0 and full backward compatibility for existing state files.

## Changes in executor.py

- `_save_state()`: reads `existing.get("remediation_attempts", 0)` with int coercion and WARNING on failure; includes field in every state write
- New `_increment_remediation_attempts(state_file)`: atomically reads, coerces, increments, and writes counter
- `write_state()` + `os.replace()`: already atomic; field persists across save/load cycles

## Schema

```json
{
  "schema_version": 1,
  "remediation_attempts": 0,
  ...
}
```

## Backward Compatibility

- Old state files without `remediation_attempts` default to 0 via `existing.get("remediation_attempts", 0)`
- No migration required; read-on-save strategy

## Test Results

`uv run pytest tests/sprint/test_executor.py -v -k "state"` — **11 passed**
- New file has remediation_attempts: 0
- Old file without field reads as 0
- Persists across save/load cycles
- String coercion ("2" → 2)
- Non-numeric coercion ("not-a-number" → 0 with WARNING)
- Atomic write verified via os.replace mock
