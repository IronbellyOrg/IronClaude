# Pipeline Execution Summary — Baseline Full E2E

**Date:** 2026-04-03
**Overall Result:** HALTED-AT-STEP (spec-fidelity)

## Step Sequence

| Step | Status | Attempt | Duration |
|------|--------|---------|----------|
| extract | PASS | 1 | 80s |
| generate-opus-architect | PASS | 1 | 115s |
| generate-haiku-architect | PASS | 1 | 232s |
| diff | PASS | 1 | 88s |
| debate | PASS | 1 | 97s |
| score | PASS | 1 | 74s |
| merge | PASS | 1 | 156s |
| anti-instinct | PASS | 1 | 0s |
| test-strategy | PASS | 1 | 101s |
| spec-fidelity | FAIL | 2 | 156s |
| wiring-verification | PASS | 1 (trailing) | 0s |
| remediate | SKIPPED | — | — |
| certify | SKIPPED | — | — |

## Halt Details
- **Halted at:** spec-fidelity (attempt 2/2)
- **Reason:** high_severity_count must be 0 for spec-fidelity gate to pass
- **Resume needed:** No (merge passed on first attempt)

## Key Observations
- Anti-instinct **PASSED** this run (unlike prior baseline run where it failed on fingerprint_coverage < 0.7)
- This allowed test-strategy and spec-fidelity to execute (they were SKIPPED in prior run)
- Pipeline produced **11 content artifacts** (vs 9 in prior run)
- spec-fidelity generated output (9,101 bytes) but failed the gate on high_severity_count
- Total elapsed: ~18 minutes

## Artifact Count
- Content .md files produced: 11 (expected 9-11 depending on anti-instinct gate)
- All 11 files verified on disk with non-zero sizes
