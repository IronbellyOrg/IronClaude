# QA Report — Task Qualitative (Step 5.G2 Content Verification)

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-07
**Phase:** task-qualitative / fix-cycle content verification (report-only)

## Overall Verdict: PASS

All three test-only fixes (D-1/D-2/D-3) are operationally meaningful and would each go RED under the regression they target. All three accepted/out-of-scope decisions (P5-PS-01, P5-PS-03, P5-HALT-5) are defensible against the actual change surface and control flow. No new test is tautological.

## Detailed Findings

### 1. D-1 config-missing fold test — GENUINE
Drives the REAL `run_fallback_ladder` with parametrized raising factories. The factory fires inside `_dispatch_one_fallback` (`fallback.py:372`) BEFORE dispatch; the empty dispatch queue (`_make_dispatch([])`) is a real guard proving factory-before-dispatch order (a reversed order would raise `IndexError`, not in the `except` tuple, and error the test). Because `fallback_available` is unconditionally True, the planner's own `fallback_config_missing` branch is unreachable — the ONLY reachable source of the asserted `terminal_reason == "fallback_config_missing"` is the `except (TransportEnvError, ModelPoolTooSmallError)` fold (`fallback.py:471-474`). Removing that clause makes the test error (RED). Confirmed genuine.

### 2. D-2 reversed-ladder test — TRULY ISOLATES POSITIONAL BINDING
`read_env_for_pool` reads the pool by prefix-index (`T1Model01` then `T1Model02`), independent of ladder. `make_fallback_slot_factory` binds `slot_to_model[ladder[i]] = pool[i]` (position). With reversed `ladder=("T1Model02","T1Model01")`: `T1Model02→pool[0]=qwen-t1`, `T1Model01→pool[1]=deepseek-t1`. A `slot_name→env[slot_name]` name-lookup would bind the opposite and fail both asserts. Confirmed isolating.

### 3. D-3 close treatment — CORRECT, NO F1 MASK
`_closing_factory` closes every constructed transport (the real-binding factory owns an `httpx.Client`, `_owns_client=True`; `close()` actually closes it). `.model` is a read-only property independent of client state and asserted before `finally`. A failing assert still triggers `finally`. The honesty note (httpx 0.28.1 `Client` has no `__del__` so `-W error::ResourceWarning` is green either way) is accurate — the `.close()` is durable hygiene, not green-washing.

### 4. Accepted / out-of-scope decisions — ALL DEFENSIBLE
- **P5-PS-01 (OUT-OF-SCOPE):** the `openai_compat.py` diff touches ONLY `read_env_for_pool` + `__all__` + the thin `read_env` wrapper; `send()`'s `RequestError` URL-embedding arm and the `Bearer` header are NOT in any hunk. The rationale ("task extended `read_env_for_pool`, not `send()`") matches the actual change set. No credential VALUE leaks. The OUT-OF-SCOPE tag is the lens's own, not a waiver.
- **P5-PS-03 (accept):** T2-worded `TransportEnvError` carries env-var NAMES, folds into `fallback_config_missing`, never operator-surfaced — identical to the accepted Phase 4 F2/F3. Zero credential impact.
- **P5-HALT-5 (accept):** the `if _T1_PROXY_BINDING is None` branch is dead now the binding is a non-None literal; the real safety net is the LAZY env read (proven by `test_..._missing_env_degrades` with `env={}` still raising `TransportEnvError`). Genuine defensive belt-and-suspenders.

### 5. Tautology check — NONE FOUND
Both new tests drive real code paths with a concrete kill-mutant. Neither asserts against a copied fixture value or a placeholder.

## Summary
- Checks passed: 5 / 5
- Critical issues: 0

## Issues Found

None.

## QA Complete
