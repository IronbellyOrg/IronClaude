# Research: ensemble → swarm T1 pool/creds acquisition seam (GAP-2 gap-fill)

**Topic type:** Integration Points (gap-fill)
**Scope:** `src/superclaude/cli/reflect/ensemble.py` `resolve_t2_transport_factory` + `run_tier2_ensemble`; `src/superclaude/cli/swarm/commands.py` `_resolve_run_transport_factory`
**Status:** Complete
**Date:** 2026-07-06
**Reason:** A.8 gap-detection GAP-2 (IMPORTANT): no research file grounded HOW the ensemble obtains the T1 pool + proxy creds. Closes it, and corrects a design §2.1 pseudocode inaccuracy.

---

## The finding: proxy creds are read from ENV *internally*, never surfaced to the ensemble

Verified by symbol read (2026-07-06):

- **`ensemble.py:139-167` `resolve_t2_transport_factory(transport, *, reviewers, models=None, env=None)`** — the ONLY thing `run_tier2_ensemble` calls to get its per-slot factory (ensemble.py:201-205). For `openai_compat` it delegates to `_resolve_run_transport_factory(transport, models, env, workers_requested=reviewers)`.
- **`swarm/commands.py:612-707` `_resolve_run_transport_factory`** — for `openai_compat` it calls `read_env(env)` **internally** (commands.py:680), gets `TransportConfig(base_url, api_key, models)`, builds `OpenAICompatTransport(base_url=config.base_url, api_key=config.api_key, model=...)` per slot (commands.py:695-699), and **caches per model**. The `base_url`/`api_key` never leave this function — they are bound into the transport closure.

**Consequence (corrects design §2.1):** `run_tier2_ensemble` receives only a `ReflectConfig` + an optional `env` mapping (ensemble.py:171-178). It has **no `SwarmConfig`, no `t1_models`, no `base_url`/`api_key`** in scope (confirmed: `grep swarm_config`/`t1_models` in ensemble.py → zero matches). Therefore the design §2.1 pseudocode

```python
make_fallback_slot_factory(pool=swarm_config.t1_models, base_url=..., api_key=...)
```

is NOT constructable at the seam as written — there is no `swarm_config` there.

## Grounded resolution: a sibling env-reading resolver (mirror the T2 path)

The correct pattern mirrors `resolve_t2_transport_factory` exactly — resolve the T1
factory from `env` INTERNALLY, so no `SwarmConfig` needs to reach the ensemble:

```python
# NEW in ensemble.py, sibling to resolve_t2_transport_factory (ensemble.py:139)
def resolve_t1_fallback_factory(
    transport: str,
    *,
    ladder: tuple[str, ...],          # config.tier2_fallback_ladder
    env: Mapping[str, str] | None = None,
) -> FallbackTransportFactory:        # (slot_name: str) -> Transport
    """Slot-NAME-keyed factory for the T1 fallback pool. openai_compat reads the
    T1 env contract internally (read_env_for_pool with the T1Proxy*/T1Model0
    names — research/06 reconciliation), binding ladder[i] -> pool[i]. Raises
    TransportEnvError/ModelPoolTooSmallError eagerly; the controller catches into
    terminal_reason: fallback_config_missing. stub -> a stub factory (or, per
    design §7.2, fallback is disabled for stub upstream in resolve_config)."""
```

Implementation options (design §7.3 already flagged "parameterize, don't fork"):
- **Preferred:** parameterize `_resolve_run_transport_factory` (swarm/commands.py) on `(model_prefix, proxy_url_env, proxy_key_env, max_slots)` and have it call `read_env_for_pool` instead of the hard-coded `read_env`; `resolve_t1_fallback_factory` calls it with the T1 names and then wraps the returned positional `(slot_index)->Transport` into a slot-NAME map via `make_fallback_slot_factory` (F1) — OR, cleaner, `_resolve_run_transport_factory` grows a `slot_names` param so it can key by name directly.
- The ensemble already has `env` (passed to `run_tier2_ensemble(..., env=env)`); forward it to `resolve_t1_fallback_factory(config.transport, ladder=config.tier2_fallback_ladder, env=env)` and hand the result to `run_fallback_ladder(transport_for_fallback_slot=...)`.

**Net:** the T1 pool + creds are acquired from `env` inside the resolver, EXACTLY like T2 — no `SwarmConfig` plumbing into the ensemble. This closes GAP-2 and removes the design §2.1 misdirection (the design body is being corrected to match).

## Builder action

1. Add `resolve_t1_fallback_factory` to `ensemble.py` (sibling of `resolve_t2_transport_factory`).
2. Parameterize `_resolve_run_transport_factory` (swarm/commands.py) on pool/prefix/proxy-env-names + optional `slot_names`, calling `read_env_for_pool` (F3).
3. Wire it in `run_tier2_ensemble` at the controller seam; `run_fallback_ladder` consumes the slot-NAME factory (F1).
4. Test: `resolve_t1_fallback_factory("stub", ...)` returns a working stub factory; `"openai_compat"` with a monkeypatched env dict binds `T1Model01`→ladder[0], `T1Model02`→ladder[1]; missing T1 env → `TransportEnvError` caught into `fallback_config_missing`. Network-free via `httpx.MockTransport` or a stub.

This makes the T1 acquisition path a mirror of the proven T2 path, not a new plumbing channel.
