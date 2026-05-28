# Pytest Comparison — Phase 5

**Timestamp:** 2026-05-25 04:10
**Comparison:** Baseline → After Phase 5 naming/noqa fixes

## Full-Run Status

Per Phase 4 finding, the full-suite pytest is now segfault-flaky due to environmental PyYAML/pty interaction (NOT introduced by lint cleanup). Comparison uses touched-files-only methodology.

## Targeted Regression on Touched Test Files

Files modified in Phase 5:
- `tests/audit/test_invariant_preservation_NFR_6_through_10.py`
- `tests/audit/test_nfr_conv_9_zero_trust.py`
- `tests/audit/test_monotonicity_halt_F_5_5_5.py`
- `tests/audit/test_sequencing_PR06_before_PR04.py`

| Metric | Value |
|--------|-------|
| Passed | 100 |
| Failed | 3 (all pre-existing in baseline — see below) |
| Total | 103 |
| Duration | 37.75s |

## Pre-Existing Failures (Cross-Check Against Baseline)

The 3 failed tests appear identically in `pytest-baseline-pre-fix.txt`:
- `tests/audit/test_nfr_conv_9_zero_trust.py::TestPassFailBulletsByteIdentical::test_source_and_mirror_byte_identical`
- `tests/audit/test_sequencing_PR06_before_PR04.py::TestK007MitigationDocumented::test_rf_qa_src_and_mirror_byte_identical`
- `tests/audit/test_sequencing_PR06_before_PR04.py::TestCanonicalRfQaUntouched::test_mirror_rf_qa_byte_identical_post_fixture`

These are pre-existing test failures unrelated to ruff cleanup (they appear to be byte-identity tests against canonical files that may have drifted independently).

## Verdict

**PASS** — Phase 5 noqa additions for N801/N999 do not introduce new test failures. All 3 failures pre-exist in baseline and are explicitly tracked as part of the 88-failure baseline preservation target.
