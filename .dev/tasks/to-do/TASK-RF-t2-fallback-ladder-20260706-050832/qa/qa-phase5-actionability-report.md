# QA Report — Step 5.G1 Real-Dispatch Actionability Lens

**Topic:** Phase 5 real-dispatch resolver-binding tests (T2 fallback ladder)
**Date:** 2026-07-07
**Phase:** task-qualitative (real-dispatch actionability lens, report-only)
**Fix cycle:** N/A
**Fix authorization:** false (report-only; no source/test/task modified)

---

## Overall Verdict: FAIL

Any issue = FAIL. Three actionability defects found (1 IMPORTANT, 2 MINOR). The
five verify items are **substantively satisfied** — the binding is real, the
missing-env test is deterministic, the tests are network-free, concrete, and the
stale None-premise test is gone — but the real-dispatch suite has coverage/sharpness
gaps that let real regressions slip through green.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | F1 slot-NAME binding on ENABLED openai_compat arm, injected env, distinct model/position | AX-4 | PASS (with caveat, see D-2) | `test_...real_binding_is_slot_name_keyed` (L239-258) injects `env={T1ProxyUrl,T1ProxyKey,T1Model01:"qwen-t1",T1Model02:"deepseek-t1"}`, asserts `factory("T1Model01").model=="qwen-t1"` and `factory("T1Model02").model=="deepseek-t1"`. Traced through `resolve_t1_fallback_factory` L248-286 → `read_env_for_pool` (openai_compat.py L160-211, index-ordered dense pool) → `make_fallback_slot_factory` (fallback.py L251-272, `slot_to_model[ladder[i]]=pool[i]`). Two DISTINCT values returned → "never pool[0] twice" holds. Uses injected env, never os.environ, never `.send()`. |
| 2 | Missing-env test is env-DETERMINISTIC (`env={}`, no os.environ dependence) | none | PASS | `test_...missing_env_degrades` (L225-236) passes `env={}` explicitly. `read_env_for_pool` L186 `env if env is not None else os.environ` → `{}` used, os.environ never touched. Raises `TransportEnvError` deterministically. Flakiness risk (binding now non-None) is closed. |
| 3 | Network-free (transport constructed, never `.send()`-ed; no live socket) | none | PASS (hygiene caveat D-3) | `grep` shows no `.send(` in test file; only `.model` read. `OpenAICompatTransport.__init__` (openai_compat.py L280-303) builds `httpx.Client()` lazily — no socket opened until first request. Strictly network-free. |
| 4 | Concrete, not tautological (fails if `model_prefix` ignored / binding reverts to T2 pool) | AX-4 | PASS (partial, see D-2) | If binding reverted to T2 pool or `model_prefix` ignored, `read_env_for_pool` scans `T2Model0N` → absent in the T1-only env → raises `TransportEnvError` → test errors. That mutation IS caught. The positional-vs-name-lookup mutation is NOT (D-2). |
| 5 | Stale `_T1_PROXY_BINDING is None`-premise test updated, not left asserting superseded premise | none | PASS | Full file read: no test asserts `_T1_PROXY_BINDING is None` or "gated factory raises regardless of env". The former gated-premise test is now `test_...missing_env_degrades` (L225), docstring "Phase 5 (real binding enabled)". `_T1_PROXY_BINDING` is enabled (ensemble.py L193-198). No superseded premise remains. |

## Summary
- Checks passed: 5 / 5 (all five verify items substantively satisfied)
- Checks failed: 0 verify items — but 3 actionability defects surface under the adversarial lens
- Critical issues: 0
- Important issues: 1 (D-1)
- Minor issues: 2 (D-2, D-3)
- Issues fixed in-place: 0 (report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| D-1 | IMPORTANT | `test_ensemble_fallback_stub.py` L225-236 (`test_...missing_env_degrades`) + fallback.py L471-474 | The test NAME says `..._degrades` and its docstring (L229-230) claims the `TransportEnvError` is "folded into `terminal_reason: fallback_config_missing`", but the body asserts ONLY `pytest.raises(TransportEnvError)`. **No test in this file drives a raising openai_compat factory through `run_fallback_ladder`.** Both ladder tests (L118, L174) use `_trivial_factory` (returns `object()`, never raises). `grep` confirms `fallback_config_missing` appears only in the docstring (L230), never in an assertion. A regression that broke the `except (TransportEnvError, ModelPoolTooSmallError)` fold at fallback.py L471-474 (e.g., narrowing the caught tuple, or mis-setting `terminal_reason`) would let all 5 tests stay green while the "degrades" behavior the name promises is silently lost. | Add a test that calls `run_fallback_ladder(..., transport_for_fallback_slot=<factory raising TransportEnvError>, dispatch=..., ...)` on a primary set with an eligible failure, and asserts `outcome.metadata["terminal_reason"] == "fallback_config_missing"` and `outcome.metadata["exhausted"] is False`. That closes the name-vs-assertion gap and pins the fold seam. |
| D-2 | MINOR | `test_ensemble_fallback_stub.py` L247-258 (`test_...real_binding_is_slot_name_keyed`) | The test cannot ISOLATE the F1 mechanism it names ("slot NAME → distinct pool model **by ladder position**", task L127 `ladder[i]→pool[i]`). Because the ladder slot names `("T1Model01","T1Model02")` are byte-identical to the pool env-var KEY names, the expected outputs are the same under two different implementations: (a) the real positional binding `ladder[i]→pool[i]`, and (b) a hypothetical direct name-lookup `slot_name → env[slot_name]`. A name-keyed misimplementation of `make_fallback_slot_factory` would PASS this test. (Low real-world risk: production ladder is fixed to `T1Model0N` and the pool is index-ordered from the same keys, so name and position always coincide — hence MINOR, not IMPORTANT — but the test's stated positional claim is under-proven.) | Add a divergence fixture where name-order ≠ position-order: e.g. `ladder=("T1Model02","T1Model01")` with the same env, and assert `factory("T1Model02").model=="qwen-t1"` (pool[0]) — this fails under direct name-lookup, proving positional binding. Or assert directly on `make_fallback_slot_factory` with a pool whose ordering diverges from the slot names. |
| D-3 | MINOR | `test_ensemble_fallback_stub.py` L257-258 | The real-binding test constructs live `OpenAICompatTransport` instances with NO injected `client` (openai_compat.py L303 → owns a real `httpx.Client()`), builds TWO of them (qwen-t1, deepseek-t1), and never `.close()`s either. `grep` confirms no `client=`, `MockTransport`, or `.close()` in the file. Result: 2 leaked httpx clients / `ResourceWarning` per run, and the test exercises a network-capable client where the transport explicitly supports injecting `httpx.MockTransport` (docstring L263-268) to stay hermetic. Not a correctness bug (no socket opens without a request) but a hygiene/leak defect that scales with repeated runs. | Assert the binding via `make_fallback_slot_factory` with a `build_transport` stub (avoid constructing a live transport at all), OR inject `client=httpx.Client(transport=httpx.MockTransport(...))` and close it (context manager / `try/finally`). Then the model-identity assertion stays but no live client leaks. |

## Actions Taken
None — report-only (`fix_authorization: false`). No source, test, or task file modified. Only this report written.

## Adversarial notes (env-dependence / flakiness sweep — the stated hypothesis)
The spawn hypothesis ("assume shallow/tautological/env-dependent/flaky") was tested and **largely rejected**:
- **Not env-dependent:** the two resolver tests inject `env` explicitly (L234, L253); the missing-env test passes `env={}` so it never reads `os.environ` (item 2). The ladder tests inject `dispatch`/`stamp`/`normalize`/factory and `deadline_monotonic=None`, so `_wall_clock_ok` (fallback.py L296-299) short-circuits to always-ok — no `time.monotonic()` race.
- **Not flaky:** deterministic pool ordering (`read_env_for_pool` dense index scan), no network, no clock dependence.
- **Not tautological:** assertions are real behavior checks (distinct `.model` values; `pytest.raises`), not identity restatements.
- **Residual shallowness is real** and is captured as D-1 (untested fold), D-2 (under-isolated positional claim), D-3 (leaked live client). The stub-arm test (L213-222) intentionally binds ONE shared stub to all slots — it does NOT prove slot distinctness, so distinctness rests entirely on the openai_compat test, sharpening the importance of D-2.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` block was supplied in the spawn prompt; standalone
behavior applies. All findings below rest on my own tool engagement, not on any inherited PASS.

## Self-Audit
**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was provided; every item was verified independently.

**(b) Independent semantic checks (≥1 required, INV-019):**
- F1 positional-binding semantics — traced `resolve_t1_fallback_factory` (ensemble.py L248-286) → `read_env_for_pool` (openai_compat.py L160-211) → `make_fallback_slot_factory` (fallback.py L251-272) and reasoned about the name==key-name collision (D-2); tool evidence: Read of all three, plus `grep` of the test file.
- Fold-path coverage — verified via `grep -n "fallback_config_missing|TransportEnvError|_trivial_factory|raises"` that the `TransportEnvError → fallback_config_missing` fold (fallback.py L471-474) is asserted nowhere in the file (D-1).
- Client-leak hygiene — verified via `grep` that no `client=`/`MockTransport`/`.close()` exists, cross-referenced against `OpenAICompatTransport.__init__` L302-303 owning a real `httpx.Client` (D-3).

## Self-Audit answers (mandatory)
1. **Factual claims independently verified against source:** 12+ — pool ordering, dense-scan, `env is not None` branch, `make_fallback_slot_factory` mapping, `_T1_PROXY_BINDING` enabled state, ladder defaults, T1_MODEL_MAX_SLOTS=9, httpx.Client construction, the except-fold, all 5 test bodies, and the task's F1 statement (task L127).
2. **Files read:** `tests/cli/reflect/test_ensemble_fallback_stub.py`, `src/superclaude/cli/reflect/fallback.py`, `src/superclaude/cli/reflect/ensemble.py`, `src/superclaude/cli/swarm/transports/openai_compat.py`, plus grep of `swarm/config.py`, `reflect/config.py`, `reflect/models.py`, and the task file.
3. **Why trust the finding:** I ran the suite (5 passed, 0.18s) AND read every seam the tests traverse, then constructed concrete mutation scenarios (broken fold at fallback.py L471-474; name-lookup misimplementation of `make_fallback_slot_factory`) and confirmed each would stay green — evidence of real coverage gaps, not a rubber-stamp.
4. **Web research:** none performed; no external lookup required (all claims are local-code-bound). Tavily not invoked.

## Confidence
Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 4 | Grep: 5 | Glob: 0 | Bash: 6 (incl. 1 pytest run)

## Recommendations
- Address D-1 before merge (IMPORTANT): add the `run_fallback_ladder` fold test so `terminal_reason == "fallback_config_missing"` is pinned; the current suite would not catch a broken except clause.
- Address D-2 + D-3 (MINOR) to harden the real-dispatch proof: add a name≠position divergence fixture, and stop leaking live httpx clients (assert via `make_fallback_slot_factory` + `build_transport` stub, or inject+close a `MockTransport`).
- All three are resolvable without changing production code — they are test-quality gaps, not implementation defects. The binding itself (F1) is correctly implemented.

## QA Complete
