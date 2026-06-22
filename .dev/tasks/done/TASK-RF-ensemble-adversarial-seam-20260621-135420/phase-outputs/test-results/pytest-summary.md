# Pytest Summary — reflect + swarm suites (Step 3.3)

**Date:** 2026-06-22
**Command:** `uv run pytest tests/cli/reflect tests/swarm -q`
**Raw output:** `phase-outputs/test-results/pytest-full-output.txt`

## Overall Result

**PASSED** — exit code 0.

| Metric   | Count |
|----------|-------|
| Passed   | 2353  |
| Failed   | 0     |
| Skipped  | 26    |
| xpassed  | 1     |

## Key-test confirmations (targeted `-v` re-run, 5 passed in 0.16s)

| Test | Status | Significance |
|------|--------|--------------|
| `test_i12_seam_regression_does_not_pass` | **PASSED** | NEW headline R6 acceptance — seam regression routes HALTED/exit-10/reason=regression, NOT PASS |
| `test_i1_positive_witness_real_fanout` | **PASSED** | I1 clean-path PASS still green (clean Tier-2 run still PASSes) |
| `test_u11_build_reflect_contract_threads_regression_fields` | **PASSED** | NEW unit companion — widened builder threads deviation/regression kwargs + clean defaults |
| `test_u10_adversarial_contract_parse_real_shape` | **PASSED** | `parse_adversarial_contract`/`extract_convergence_score` signatures UNCHANGED (wrapped not replaced) |
| `test_u6_verdict_map_and_derive_ordering_are_unchanged` | **PASSED** | FR-RH2.7 frozen-ordering guard intact |

## Red-then-green note

`test_i12_seam_regression_does_not_pass` is red-then-green by construction: against the pre-R6 code `build_reflect_contract` hard-coded `regression_present: False`, so the contract routed `Verdict.PASS` and the test's `result.verdict is Verdict.HALTED` / `contract["regression_present"] is True` assertions FAIL. After the seam widening the injected `AdversarialResult(regression_present=True)` threads through to the contract and `derive_verdict` routes HALTED.

## Failures

None. No failure table required.
