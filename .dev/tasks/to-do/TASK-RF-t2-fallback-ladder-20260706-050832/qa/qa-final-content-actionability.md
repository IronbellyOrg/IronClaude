# QA Report — Test Actionability Lens (Step 6.G5)

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Phase:** task-qualitative (test-actionability), report-only
**Date:** 2026-07-07

## Overall Verdict: FAIL

FAIL on the "any issue regardless of severity" gate. NOT a correctness failure of what is tested — every required load-bearing assertion is present, genuinely load-bearing, and the suite is green (2548 passed, 28 skipped, 0 failed). FAIL is driven by 1 IMPORTANT coverage gap (F4 tested only at the pure-planner layer) + 2 MINOR hygiene defects.

## Load-bearing assertion audit

| Required signal | Present? | Evidence |
|---|---|---|
| F1 `T1Model02→pool[1]` (not pool[0] twice) | PASS | `test_fallback_plan.py` + `test_fallback_slot_factory.py` |
| F1 reversed-ladder positional test | PASS | `test_ensemble_fallback_stub.py` `..._binding_is_positional_not_name` |
| F2 stable non-empty `final_path` | PASS | stub test asserts truthy + `.endswith(".final.md")` after stamp→normalize |
| F4 no dispatch on `wall_clock_ok=False` | PARTIAL (Finding 1) | Proven only at pure planner; controller never tested with a past deadline |
| F6 first-match `degraded-tier1` | PASS | `test_verdict_mapping.py` + verified against `contract.py:271` (T6) preceding `:288` (T10) |
| config-missing FOLD via `run_fallback_ladder` | PASS | parametrized D1 drives the REAL controller |
| Extended files did NOT clobber regression bodies | PASS | `git diff --numstat`: all 4 modified files 0 deletions |
| Network-free | PASS | injected stubs / StubTransport / env dicts; ClaudeProcess only in assert_not_called guards |
| `pytest -k "reflect or swarm"` green | PASS | 2548 passed, 28 skipped, 1 xpassed, 0 failed |

## Issues Found

| # | Severity | Location | Issue | Fix decision |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `test_ensemble_fallback_stub.py` (all `run_fallback_ladder` calls pass `deadline_monotonic=None`) | F4's controller-level enforcement is untested. The impure seam (`_wall_clock_ok(deadline, time.monotonic())` → `plan_next_attempt(wall_clock_ok=...)` → dispatch-skip) is never exercised. A regression dropping `wall_clock_ok=wall_ok` or a sign error in `_wall_clock_ok` would pass every test. | FIX: add a controller-level test injecting a PAST `deadline_monotonic` into `run_fallback_ladder` with the §8 incident shape and a spy `dispatch`; assert the spy is NEVER called AND `terminal_reason == "fallback_wall_clock_exhausted"`. |
| 2 | MINOR | `tests/cli/reflect/fixtures/pass_with_t2_fallback.yaml` | Orphaned fixture (referenced by zero tests). | FIX: wire into a `test_verdict_mapping.py` verdict-unchanged assertion (dedup with conformance #1 / enums G1). |
| 3 | MINOR | `tests/swarm/test_openai_compat.py` (`test_resolve_factory_t1_branch_binds_per_slot_models`, `..._pool_too_small_raises`) | httpx-client-leak: these construct live `OpenAICompatTransport` without closing (each opens an `httpx.Client`), inconsistent with the `_closing_factory` hygiene added on the reflect side (D3). | FIX: close constructed transports in a `try/finally` in the two swarm factory tests. |

## Recommendation

Three additive test-quality fixes; none indicates a defect in the implementation under test (the F4 controller logic, the fold, and F6 precedence are all correct in `fallback.py`/`contract.py` — simply under-exercised or accompanied by a dead artifact). Fold all three into the final fix cycle. Finding 1 (F4 controller test) is the priority — the one genuine runtime seam currently unguarded.
