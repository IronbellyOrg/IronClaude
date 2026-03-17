# D-0040 -- T05.04: False Certification Blocked (SC-5)

## Summary

`certified: false` causes CERTIFY_GATE failure. Pipeline does not advance past certification. SC-5 verified with explicit true/false/missing/malformed unit tests for `_certified_is_true()`.

**Implementation fix applied**: `_certified_is_true` semantic check added to CERTIFY_GATE (T02.06 gap resolved in T05.04).

## Test Evidence

**Test file:** `tests/sprint/test_phase5_negative_validation.py::TestFalseCertification`

**Validation command:** `uv run pytest tests/sprint/ -v -k "certif"`

**Result:** 10 passed, 0 failed

### SC-5 Four Variant Tests:

| Test | Input | `_certified_is_true()` result | SC-5 case |
|------|-------|-------------------------------|-----------|
| `test_certified_true_passes` | `certified: true` | True | Case 1 (true) |
| `test_certified_false_fails` | `certified: false` | False | Case 2 (false) |
| `test_certified_missing_fails` | (field absent) | False | Case 3 (missing) |
| `test_certified_malformed_fails` | `certified: yes`, `1`, `` | False | Case 4 (malformed) |

### Gate Integration Tests:

| Test | Assertion | Result |
|------|-----------|--------|
| `test_certify_gate_is_strict` | CERTIFY_GATE.enforcement_tier == "STRICT" | PASS |
| `test_certify_gate_requires_certified_field` | "certified" in required_frontmatter_fields | PASS |
| `test_false_certification_blocks_certify_gate` | gate_passed() returns (False, reason) for certified:false | PASS |
| `test_true_certification_passes_certify_gate` | gate_passed() returns (True, None) for certified:true | PASS |

## Implementation Change

Added `certified_is_true` semantic check to `CERTIFY_GATE` in `gates.py`:

```python
SemanticCheck(
    name="certified_is_true",
    check_fn=_certified_is_true,
    failure_message="certified must be true for certify gate to pass (anti-false-certification)",
),
```

Updated `tests/roadmap/test_certify_gates.py` to expect 3 semantic checks (was 2).

## Acceptance Criteria Verification

- [x] `_certified_is_true()` returns True only for `certified: true`
- [x] `_certified_is_true()` returns False for false/missing/malformed (all 3 variants tested)
- [x] CERTIFY_GATE fails when `certified: false`, blocking pipeline advancement
- [x] SC-5 verified with all 4 input variants tested
- [x] `uv run pytest tests/sprint/ -v -k "certif"` exits 0
