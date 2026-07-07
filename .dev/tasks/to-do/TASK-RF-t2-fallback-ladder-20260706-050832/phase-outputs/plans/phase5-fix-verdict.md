# Phase 5 Fix Verdict — Step 5.G2 (I20, serialized test-only fixes)

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-07
**File modified (ONLY):** `tests/cli/reflect/test_ensemble_fallback_stub.py`

## Overall: PASS — all three actionability findings applied and verified

Executor-owned record fixes (P5-HALT-1/2/3/4 provenance + Phase 5 log entry; P5-PS-01 follow-up) were applied separately before this fix agent ran. This agent handled the three test-only actionability fixes.

## What changed

- **Imports added:** `Iterator`, `contextmanager`, `ModelPoolTooSmallError`.
- **New helpers:** `_raising_transport_env_factory` / `_raising_pool_too_small_factory` (raise on call), `_closing_factory` (`@contextmanager` closing every transport a factory returns — D3 no-leak).
- **P5-ACT-D1 (IMPORTANT):** new `test_raising_fallback_factory_folds_into_config_missing`, parametrized over both raising factories. Drives the REAL `run_fallback_ladder` with a raising factory + empty dispatch queue (factory raises inside `_dispatch_one_fallback` before dispatch). Asserts `terminal_reason == "fallback_config_missing"`, `certified_with_fallback is False`, contributing set stays `["deepseek-primary"]`. Would FAIL if the `except (TransportEnvError, ModelPoolTooSmallError)` fold at `fallback.py` broke.
- **P5-ACT-D2 (MINOR):** new `test_resolve_t1_fallback_factory_openai_compat_binding_is_positional_not_name` with a REVERSED ladder (`("T1Model02","T1Model01")`), asserting `T1Model02→pool[0]=qwen-t1`, `T1Model01→pool[1]=deepseek-t1`. A name-lookup misimplementation fails this. Transports closed via `_closing_factory`.
- **P5-ACT-D3 (MINOR):** both real-binding tests now call the factory through `_closing_factory`, closing every constructed `OpenAICompatTransport`'s `httpx.Client`. F1 `.model` assertions preserved.

## Commands run

| Command | Result |
|---|---|
| `uv run pytest .../test_ensemble_fallback_stub.py .../test_ensemble_fallback_engage.py -q` | 10 passed (stub 8 + engage 2) |
| `uv run pytest .../test_ensemble_fallback_stub.py -W error::ResourceWarning -q` | 8 passed, no ResourceWarning |
| `uv run ruff check` / `--format --check` on the changed file | clean / already formatted |
| `git diff --stat -- src/` | only pre-existing Phase 1-5 files; zero edits by the fix agent |

Test count 5 → 8 in the stub file (D1 ×2 parametrized + D2 ×1); no existing test weakened.

## Honesty note (from the fix agent)

In the pinned httpx 0.28.1, `httpx.Client` has no `__del__` and emits no ResourceWarning on GC, so the `-W error::ResourceWarning` gate is green either way. The `.close()` treatment is still the correct durable resource-hygiene fix (covers future httpx versions / any test that later sends a request).

## Constraints honored

- No `src/` touched; `_T1_PROXY_BINDING` real-dispatch literal intact; `contract.py` / `swarm/models.py` unchanged. UV only. Nothing staged/committed.
