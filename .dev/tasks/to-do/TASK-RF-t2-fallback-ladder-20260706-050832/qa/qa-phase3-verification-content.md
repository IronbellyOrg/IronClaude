# QA Report — Step 3.G7 Content Verification (Phase 3 fix cycle)

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-06
**Phase:** task-qualitative / fix-cycle content verification
**Fix authorization:** false (report only)

## Overall Verdict: PASS

All five verification requirements are satisfied by evidence in the actual source. The new ensemble-level gate test genuinely proves the enable/skip gate, the PASS is real (not fixture-forced), the exact-id assertion matches the realigned §8 arrangement, the tests are network-free and non-tautological, and no test conflates `t2_fallback` with the verdict.

`uv run pytest tests/cli/reflect/test_ensemble_fallback_engage.py tests/cli/reflect/test_ensemble_fallback_stub.py -q` → 5 passed.

## Items Reviewed

| # | Requirement | Result | Evidence |
|---|-------------|--------|----------|
| 1 | Gate test proves enable/skip; ENGAGE fails if controller skipped, SKIP fails if controller ran; separate output dirs | PASS | Gate is `if config.tier2_fallback_enabled:` (`ensemble.py:296`); `run_fallback_ladder` never reads the flag, so the engage test drives real `run_tier2_ensemble`. If controller skipped: `reviewer_count=1`, `t2_fallback` absent → engage asserts fail. If controller ran under SKIP: `tier_reached=2`, `t2_fallback` present → skip asserts fail. Contracts isolated via `tmp_path/"on"` vs `tmp_path/"off"`. |
| 2 | ENGAGE PASS is real (distinct-vendor stub fallback → certify), not fixture-forced | PASS | Survivor `qwen-stub-00` (vendor qwen) + fallback `gemini-t1fallback-stub` (vendor google) → mcd full, vendor multi, convergence 0.86 → PASS. If fallback shared the vendor → single-vendor DEGRADE. Load-bearing on vendor distinctness. |
| 3 | Exact `primary_failures_preserved` matches realigned §8 | PASS | Failures idx0 proxy_error + idx2 parse_error → `["primary:00","primary:02"]`; asserted exactly. Survivor at index 1 matches §8. |
| 4 | Network-free and non-tautological | PASS | In-process `StubTransport`/`_FailingTransport`; `adversarial_score_fn=_const_score` avoids launching `ClaudeProcess`. Every asserted signal computed from the real controller + real `build_reflect_contract`/`derive_verdict`. |
| 5 | No test falsely implies `t2_fallback` gates the verdict | PASS | Verdict derives from `tier_reached`/diversity/convergence via `derive_verdict`; `t2_fallback` asserted separately as additive bookkeeping. |

## Summary
- Checks passed: 5 / 5
- Critical issues: 0

## Issues Found

None. (Adversarially probed all five; each fix is operationally meaningful, not a rubber stamp.)

## Notes

- The `on`/`off` subdirs are belt-and-suspenders (separate pytest `tmp_path` already isolates). Redundant but correct.
- The ENGAGE PASS is load-bearing on vendor distinctness (cannot silently pass on a same-vendor fallback) — exactly the property P3-ACT-001 demanded.
- The gated openai_compat unit correctly exercises the real `_T1_PROXY_BINDING is None` gate → `TransportEnvError`.

## QA Complete
