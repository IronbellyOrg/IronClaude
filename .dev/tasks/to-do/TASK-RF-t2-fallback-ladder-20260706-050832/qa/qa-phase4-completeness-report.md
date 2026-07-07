# Phase 4 Completeness Verification — Step 4.G2 Completeness Lens

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-07
**Lens:** Completeness (report-only)

## Verdict: PASS

All 6 verify items satisfied with direct-evidence grounding. The adversarial "≥5 missing" hypothesis is not supported — zero missing *required* elements. Found 1 MEDIUM + 2 LOW + 2 INFO, none blocking.

## Per-Item Verification

| # | Verify item | Result | Evidence |
|---|---|---|---|
| 1 | `T1_MODEL_ENV_PREFIX` + `T1_MODEL_MAX_SLOTS` in `__all__`; `t1_models` frozen defaulted field; `_collect_models` called TWICE | PASS | config.py: `__all__` +T1 constants; `t1_models: tuple[str,...] = ()` (frozen); `_collect_models(prefix, max_slots)` called for T2 and T1 in `from_env`. |
| 2 | `read_env_for_pool` parameterized; `read_env(env=None)` thin wrapper preserving signature | PASS | `read_env_for_pool(*, model_prefix, max_slots, proxy_url_env, proxy_key_env, env=None)`; `read_env` delegates bound to T2 constants; both in `__all__`. |
| 3 | `_resolve_run_transport_factory` parameterized (defaults None→T2), calls `read_env_for_pool` | PASS (see F1) | New kwargs; `read_env_for_pool(model_prefix=model_prefix or T2_..., …)`; D2 guard preserved. |
| 4 | `resolve_t1_fallback_factory` openai_compat arm wired (slot-NAME, F1) but binding-gated | PASS | `_T1_PROXY_BINDING = None`; stub arm; gated arm raises `TransportEnvError`; lazy ungated arm reads `read_env_for_pool` + `make_fallback_slot_factory`. |
| 5 | Both swarm tests EXTEND (not clobber) T2 bodies; new T1/F3 tests exist | PASS | `git diff` pure additions: test_config.py +57/−0 (5 T1), test_openai_compat.py +80/−0 (4 F3). 46 passed. |
| 6 | `git diff -- swarm/models.py` empty | PASS | Empty diff; `WorkerStatus`/`WorkerResult` unchanged. |

## Findings (all non-blocking)

### F1 — MEDIUM — `_resolve_run_transport_factory` T1-parameter branch is vestigial and untested
Check 3 is literally satisfied (params exist, default None→T2, calls `read_env_for_pool`), and the T2-default path is regression-tested. But no test passes non-default T1 values to `_resolve_run_transport_factory`, and no production caller passes them: the actual T1 fallback path (`ensemble.resolve_t1_fallback_factory`) bypasses this resolver, acquiring the pool via `read_env_for_pool` + `make_fallback_slot_factory` directly (which raises the `ModelPoolTooSmallError` *type* itself). Net: the parameterization meets the requirement's letter but its new branch is currently unexercised. **Recommendation:** add a unit test asserting `_resolve_run_transport_factory("openai_compat", model_prefix="T1Model0", proxy_url_env="T1ProxyUrl", proxy_key_env="T1ProxyKey", env=…)` reads the T1 pool, OR document the params as future-use.

### F2 — LOW — `TransportEnvError` message string is T2-hardcoded on the generalized reader
When `read_env_for_pool` reads a T1 pool and raises, the structured `.missing` tuple is correct (T1 names) but the human-readable `str()` still names T2. Bounded: folded into `terminal_reason: fallback_config_missing` (text not operator-surfaced). Cosmetic. **Recommendation:** interpolate the actual env names, or accept given the folding.

### F3 — LOW — `ModelPoolTooSmallError` message string is T2-hardcoded, and IS reachable on the T1 path
`make_fallback_slot_factory` raises this exact type when the T1 pool is smaller than the ladder position. A real T1 pool-too-small would emit a message naming "T2Model0N". Bounded by the same `fallback_config_missing` folding. Cosmetic. **Recommendation:** parameterize the slot label, or accept.

### F4 — INFO — no T1 counterpart to `missing_t2_env_vars()`
config.py remains T2-only. Not required by design (optional sibling). Deliberate omission, no action.

### F5 — INFO (PASS-strengthener) — gated arm's fixed 3-tuple + lazy real arm are correct
The gated arm raises a fixed `TransportEnvError(("T1ProxyUrl","T1ProxyKey","T1Model01"))` for the `_T1_PROXY_BINDING=None` sentinel state (covered by tests). The real (ungated) arm defers the env read lazily into the returned factory so an incomplete env raises on the factory CALL inside the controller's catch, not eagerly — matching the phase-4 latent-bug note. No gap.

## Contradictions

None. Implementation, design (post-reflect), research/02, research/07 mutually consistent.

## Recommendations (priority)

1. F1 (MEDIUM): add a direct unit test for the T1-args branch, or annotate the params as future-use.
2. F2/F3 (LOW): interpolate the actual env-var names into the messages, or explicitly accept given the folding.
3. F4/F5 (INFO): no action.

**Gate outcome:** PASS — Phase 4 swarm-side deliverables complete and correctly gated. Carry F1 forward.
