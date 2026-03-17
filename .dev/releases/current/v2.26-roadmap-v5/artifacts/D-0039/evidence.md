# D-0039 -- T05.03: Ambiguous Continuation Causes STRICT Gate Failure

## Summary

`ambiguous_count > 0` causes `_no_ambiguous_deviations()` to return False. DEVIATION_ANALYSIS_GATE (STRICT) enforces ambiguity control. Ambiguous deviations cannot silently pass through the pipeline.

## Test Evidence

**Test file:** `tests/sprint/test_phase5_negative_validation.py::TestAmbiguousContinuation`

**Validation command:** `uv run pytest tests/sprint/ -v -k "ambiguous"`

**Result:** 9 passed, 0 failed

### Tests executed:

| Test | Assertion | Result |
|------|-----------|--------|
| `test_no_ambiguous_deviations_zero_passes` | ambiguous_deviations=0 -> True | PASS |
| `test_ambiguous_count_nonzero_causes_gate_function_failure` | ambiguous_deviations=1 -> False | PASS |
| `test_ambiguous_count_two_causes_gate_function_failure` | ambiguous_deviations=2 -> False | PASS |
| `test_ambiguous_missing_field_is_fail_closed` | Missing field -> fail-closed (False) | PASS |
| `test_ambiguous_no_frontmatter_is_fail_closed` | No frontmatter -> fail-closed (False) | PASS |
| `test_ambiguous_non_integer_is_fail_closed` | Non-integer value -> fail-closed (False) | PASS |
| `test_deviation_analysis_gate_is_strict` | DEVIATION_ANALYSIS_GATE.enforcement_tier == "STRICT" | PASS |
| `test_deviation_analysis_gate_requires_ambiguous_count_field` | "ambiguous_count" in required_frontmatter_fields | PASS |
| `test_ambiguous_deviation_cannot_silently_pass` | DEVIATION_ANALYSIS_GATE is STRICT, ambiguous_count tracked | PASS |

## Implementation

- **Function**: `_no_ambiguous_deviations()` in `gates.py`
- **Gate**: DEVIATION_ANALYSIS_GATE (enforcement_tier="STRICT")
- **Field**: `ambiguous_deviations` (checked by function) and `ambiguous_count` (required frontmatter field in gate)
- **Fail-closed**: Missing frontmatter, missing field, non-integer, or count > 0 all return False

## Acceptance Criteria Verification

- [x] `ambiguous_count > 0` causes `_no_ambiguous_deviations()` to return False
- [x] DEVIATION_ANALYSIS_GATE (STRICT) fails when ambiguous items detected
- [x] Ambiguous deviations cannot silently pass through pipeline (fail-closed)
- [x] `uv run pytest tests/sprint/ -v -k "ambiguous"` exits 0
