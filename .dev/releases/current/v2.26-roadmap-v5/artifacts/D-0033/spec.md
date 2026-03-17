# D-0033: Atomic State Writes and Coercion

## Summary

Atomic writes for `.roadmap-state.json` were already implemented via `write_state()` using `.tmp` + `os.replace()`. This task hardened coercion in `_save_state()` and added `_increment_remediation_attempts()`.

## Existing Atomic Write Pattern (write_state)

```python
def write_state(state: dict, path: Path) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    os.replace(str(tmp), str(path))
```

No partial-write risk. NFR-022 compliant.

## Added Coercion in _save_state()

```python
existing_attempts_raw = existing.get("remediation_attempts", 0) if existing else 0
try:
    existing_attempts = int(existing_attempts_raw)
except (ValueError, TypeError):
    _log.warning("remediation_attempts=%r is not a valid int; treating as 0", ...)
    existing_attempts = 0
```

## Added _increment_remediation_attempts()

Atomically reads, coerces to int (NFR-017), increments, writes back.
Non-numeric values → WARNING + treat as 0.

## Test Results

`uv run pytest tests/sprint/test_executor.py -v -k "state"` — **11 passed**
- String "2" coerced to 2 before increment → result 3 ✓
- Non-numeric → 0 with WARNING → result 1 ✓
- Atomic write uses .tmp + os.replace() ✓
