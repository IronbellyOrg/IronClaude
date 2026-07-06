# Contract-Gate Test Summary (Step 2.5)

**Generated:** 2026-06-11 11:23
**Command:** `uv run pytest tests/pr_submit/test_detection_contract.py -v --no-header`
**Raw output:** `phase-outputs/test-results/contract-gate-raw.txt`

| Metric | Value |
|--------|------:|
| Overall result | **PASSED** |
| Tests collected | 6 |
| Passed | 6 |
| Failed | 0 |

## Per-test results

| Test ID | Function | Result |
|---------|----------|--------|
| T-201 | `test_t201_empty_reviews_polling` | PASSED |
| T-202 | `test_t202_augment_clean` | PASSED |
| T-203 | `test_t203_augment_findings` | PASSED |
| **T-210** (locked:false → HALT) | `test_t210_locked_false_halts` | **PASSED** |
| T-211 | `test_t211_different_bot_not_detected` | PASSED |
| T-212 | `test_t212_interleaved_only_augment_parsed` | PASSED |

## Failures

None.

**Verdict:** PASSED — all 6 detection-contract tests pass. The load-bearing **T-210**
gate (the shipped `detection-contract.md` is `locked: false`, so `DetectionContract.load()`
raises `DetectionContractLocked`; an absent or explicitly-unlocked contract also HALTs)
is explicitly proven. Counts match the raw output exactly; no fabricated results.
