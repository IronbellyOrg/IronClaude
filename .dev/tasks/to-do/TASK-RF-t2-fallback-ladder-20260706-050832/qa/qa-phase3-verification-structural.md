# QA Report — Report Validation (Step 3.G7 Structural Verification)

**Topic:** TASK-RF-t2-fallback-ladder — Phase 3 fix-cycle re-verification
**Date:** 2026-07-06
**Phase:** report-validation (fix-cycle re-verify, structural)
**Fix authorization:** false (report-only)

## Overall Verdict: PASS

All 6 IMPORTANT/MINOR actionability findings (P3-ACT-001..006) are addressed with real-controller-driven assertions. No `src/` file was modified beyond the pre-existing Phase 3 source set; `contract.py` is byte-unchanged. Both required test suites are green (10/10 fallback, 15/15 integration).

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | P3-ACT-001 ensemble ENGAGE/SKIP via real `run_tier2_ensemble` | PASS | `test_ensemble_fallback_engage.py`: Test A (enabled) asserts `t2_fallback is not None`, `engaged True`, `certified_with_fallback True`, `tier_reached==2`, `reviewer_count==2`, PASS/exit 0. Test B (disabled) asserts `t2_fallback` absent/None, `tier_reached==1`, `reviewer_count==1`, DEGRADED/exit 11/`degraded-tier1`. Gate at `ensemble.py:296`. |
| 2 | P3-ACT-002 exact `primary_failures_preserved` | PASS | `== ["primary:00","primary:02"]` (exact list, not truthy). |
| 3 | P3-ACT-003 incident indices align §8 | PASS | Survivor `deepseek-primary` at index 1; failures at index 0/2 → `primary:00`/`primary:02`. |
| 4 | P3-ACT-004 real `_stamp_worker_paths` | PASS | `ensemble.py:308 stamp=_stamp_worker_paths` wired inside `run_tier2_ensemble`; engage test drives it. |
| 5 | P3-ACT-005 real stub arm + openai_compat raises `TransportEnvError` | PASS | Engage test exercises the real `resolve_t1_fallback_factory("stub")` arm; unit asserts `pytest.raises(TransportEnvError)` on the `_T1_PROXY_BINDING is None`-gated openai_compat arm. |
| 6 | P3-ACT-006 incident engaged/count/exhausted | PASS | `engaged is True`, `fallback_attempt_count == 1`, `exhausted is False`. |
| 7 | No `src/` modified by fix cycle; `contract.py` empty | PASS | `git diff --stat -- src/` shows only the four pre-existing Phase 3 files; `contract.py` diff empty. |
| 8 | Test suites green | PASS | 10 passed (fallback trio) + 15 passed (integration). |

## Summary
- Checks passed: 8 / 8
- Critical issues: 0

## Issues Found

None. (Adversarial probes on src-tampering, trivial-pass tests, and §8 index drift all cleared.)

## Observations

- P3-COMP-MINOR-1/2/3 and P3-SEAM-INFO-1 were authorized no-fix carry-forwards; correctly untouched.

## Recommendation

Step 3.G7 passes. Phase 3 fix cycle is verified — proceed. No fix cycle re-run needed.
