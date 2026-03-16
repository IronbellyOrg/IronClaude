# D-0013 Evidence — Classifier Lookup Validation and Exception Handling

**Task:** T02.03
**Deliverable:** `run_classifier()` wrapper with KeyError propagation and exception catching
**Status:** COMPLETE

## Implementation
```python
def run_classifier(name: str, exit_code: int, stdout: str, stderr: str) -> str:
    fn = CLASSIFIERS[name]  # KeyError propagates to caller on unknown name
    try:
        return fn(exit_code, stdout, stderr)
    except Exception as exc:
        logger.warning("Classifier %s raised %s: %s", name, type(exc).__name__, exc)
        return "error"
```

## Behavior
- `CLASSIFIERS["nonexistent"]` raises `KeyError` (dict default, not suppressed)
- `run_classifier("nonexistent", ...)` also raises `KeyError` (dict lookup propagates)
- Classifier that raises any `Exception` → WARNING logged, `"error"` returned
- `"error"` classification maps to `TaskStatus.FAIL` at executor level (T03.01)

## Acceptance Criteria Checklist
- [x] `CLASSIFIERS["nonexistent_classifier"]` raises `KeyError`
- [x] `run_classifier()` catches classifier exceptions, returns `"error"`
- [x] Exception logged at WARNING with classifier name and message
- [x] `"error"` maps to `TaskStatus.FAIL` (by design, verified in T03.01)
