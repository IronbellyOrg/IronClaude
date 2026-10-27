# D-0010: Finding.deviation_class Field — spec.md

**Task:** T02.01
**Roadmap Items:** R-017, R-018, R-019, R-020
**Date:** 2026-03-16
**Status:** COMPLETE

---

## Changes Made

**File:** `src/superclaude/cli/roadmap/models.py`

### 1. Added `VALID_DEVIATION_CLASSES` frozenset (line ~16)

```python
VALID_DEVIATION_CLASSES = frozenset(
    {"SLIP", "INTENTIONAL", "AMBIGUOUS", "PRE_APPROVED", "UNCLASSIFIED"}
)
```

- Exactly 5 values as specified.

### 2. Added `deviation_class` field to `Finding` dataclass

```python
deviation_class: str = "UNCLASSIFIED"
```

- Default value `"UNCLASSIFIED"` ensures backward compatibility: all existing `Finding(...)` constructors continue to work without modification.

### 3. Updated `__post_init__` validation

```python
if self.deviation_class not in VALID_DEVIATION_CLASSES:
    raise ValueError(
        f"Invalid Finding deviation_class {self.deviation_class!r}. "
        f"Must be one of: {', '.join(sorted(VALID_DEVIATION_CLASSES))}"
    )
```

---

## Acceptance Criteria Verification

| Criterion | Result |
|-----------|--------|
| `Finding("test", ..., deviation_class="SLIP")` constructs successfully | PASS |
| `Finding("test", ..., deviation_class="INVALID")` raises `ValueError` | PASS |
| `Finding("test", ...)` defaults to `"UNCLASSIFIED"` | PASS |
| `VALID_DEVIATION_CLASSES` contains exactly 5 values | PASS |

## Test Runs

- `uv run pytest tests/roadmap/test_models.py tests/sprint/test_models.py -v` → 132 passed
- All existing `Finding` constructors remain backward-compatible (no positional arguments changed, default value added at tail of field list)
