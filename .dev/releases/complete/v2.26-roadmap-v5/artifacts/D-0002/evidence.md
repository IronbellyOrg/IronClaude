# D-0002: OQ-E/OQ-F Resolution — fidelity.py Signature Inspection

**Task:** T01.02
**Date:** 2026-03-16
**Status:** RESOLVED

---

## File Location

**File:** `src/superclaude/cli/roadmap/fidelity.py`

Module docstring: "Fidelity deviation data model -- 7-column deviation report schema."

Key characteristic: "This module has zero imports from pipeline or gate enforcement code."

---

## OQ-E Resolution — `_extract_fidelity_deviations()` Signature

**Search result:** Function `_extract_fidelity_deviations()` is **NOT FOUND** in `fidelity.py`.

**fidelity.py actual contents (complete symbol list):**
- `class Severity(Enum)` — deviation severity classification (HIGH, MEDIUM, LOW)
- `@dataclass class FidelityDeviation` — 7-field dataclass representing one deviation row
  - Fields: `id: str`, `severity: Severity`, `deviation: str`, `upstream_quote: str`, `downstream_quote: str`, `impact: str`, `recommended_correction: str`
  - Method: `__post_init__()` — validates all field constraints

**Disposition:** `_extract_fidelity_deviations()` does **not exist** → requires creation.

**Planned signature for v2.26 implementation:**
```python
def _extract_fidelity_deviations(content: str) -> list[FidelityDeviation]:
    """Parse fidelity report markdown content into FidelityDeviation objects."""
```

---

## OQ-F Resolution — `_extract_deviation_classes()` Signature

**Search result:** Function `_extract_deviation_classes()` is **NOT FOUND** in `fidelity.py`.

**Disposition:** `_extract_deviation_classes()` does **not exist** → requires creation.

**Planned signature for v2.26 implementation:**
```python
def _extract_deviation_classes(deviations: list[FidelityDeviation]) -> dict[str, list[FidelityDeviation]]:
    """Group FidelityDeviation objects by severity class."""
```

---

## fidelity.py Disposition

**Status:** `fidelity.py` requires **modification** for v2.26.

**Scope:** Add two new extraction helper functions:
1. `_extract_fidelity_deviations(content: str) -> list[FidelityDeviation]`
2. `_extract_deviation_classes(deviations: list[FidelityDeviation]) -> dict[str, list[FidelityDeviation]]`

The existing `Severity` enum and `FidelityDeviation` dataclass are **already correct** and do **not** require modification.

---

## Phase 2 Files Modified Impact

- `src/superclaude/cli/roadmap/fidelity.py` — ADD two extraction helper functions
- No modification to `pipeline/models.py` or `pipeline/executor.py` (constraint preserved)
- New functions are pure: `str → list[FidelityDeviation]` and `list → dict` with no side effects

---

## Summary Table

| OQ | Function | Status | Action |
|----|----------|--------|--------|
| OQ-E | `_extract_fidelity_deviations()` | Not found — requires creation | Add to fidelity.py in Phase 2 |
| OQ-F | `_extract_deviation_classes()` | Not found — requires creation | Add to fidelity.py in Phase 2 |
