# D-0037 -- T05.01: Bogus Intentional Claims Rejected (Anti-Laundering)

## Summary

INTENTIONAL_IMPROVEMENT annotation without valid D-XX + round citation is rejected and promoted to HIGH severity in spec-fidelity output. Silent approval of bogus claims is impossible (fail-closed).

## Test Evidence

**Test file:** `tests/sprint/test_phase5_negative_validation.py::TestBogusIntentionalClaims`

**Validation command:** `uv run pytest tests/sprint/ -v -k "bogus_intentional or anti_laundering"`

**Result:** 5 passed, 0 failed

### Tests executed:

| Test | Assertion | Result |
|------|-----------|--------|
| `test_bogus_intentional_claim_promotes_to_high_severity` | Bogus INTENTIONAL_IMPROVEMENT (no D-XX) -> high_severity_count=1 -> `_high_severity_count_zero` returns False | PASS |
| `test_anti_laundering_enforcement_blocks_spec_fidelity_gate` | SPEC_FIDELITY_GATE fails when bogus annotation produces HIGH finding | PASS |
| `test_anti_laundering_d_xx_present_but_no_round_still_high` | D-XX present but missing round citation -> still HIGH severity | PASS |
| `test_bogus_intentional_silent_approval_is_impossible` | Missing high_severity_count -> fail-closed (returns False) | PASS |
| `test_anti_laundering_zero_high_severity_allows_gate_pass` | Valid annotation (no HIGH findings) -> gate passes | PASS |

## Anti-Laundering Rule Enforcement

- **Mechanism**: `_high_severity_count_zero()` in `SPEC_FIDELITY_GATE` semantic checks
- **Rule**: Invalid INTENTIONAL_IMPROVEMENT/PREFERENCE annotation (missing D-XX + round) -> report as HIGH severity
- **Enforcement**: `high_severity_count > 0` blocks SPEC_FIDELITY_GATE (STRICT tier)
- **Fail-closed**: missing `high_severity_count` field also returns False

## Acceptance Criteria Verification

- [x] Test fixture with bogus INTENTIONAL_IMPROVEMENT (no D-XX citation) causes HIGH severity in spec-fidelity output
- [x] Invalid annotation rejection is logged with the specific missing citation (documented in prompt)
- [x] Silent approval of bogus claims is impossible (fail-closed)
- [x] Test fixture with D-XX present but missing round citation also causes HIGH severity
- [x] `uv run pytest tests/sprint/ -v -k "bogus_intentional or anti_laundering"` exits 0
