# Phase 5 Dispatch Verdict

**Date:** 2026-07-07
**Step 5.1 outcome:** CONFIRMED — real T1-proxy fallback dispatch AUTHORIZED and ENABLED.

## Decision chain

1. **Step 5.1 (needs_human_decision HALT):** read-only NAMES-only env check confirmed `T1ProxyUrl`, `T1ProxyKey`, `T1Model01`, `T1Model02` all present in `~/.aienv` (no value read/printed, no `:4000/v1` probe). Operator explicitly RE-CONFIRMED "Enable real dispatch now" interactively this session. Binding recorded in `t1-proxy-binding-decision.md`; Open Questions HUMAN-DECISION entry updated with the execution-time confirmation.
2. **Step 5.2 (enable):** set `_T1_PROXY_BINDING = {"model_prefix": "T1Model0", "proxy_url_env": "T1ProxyUrl", "proxy_key_env": "T1ProxyKey", "max_slots": T1_MODEL_MAX_SLOTS}` in `ensemble.py` (imported `T1_MODEL_MAX_SLOTS` from `swarm.config`). Only env-var NAME strings — never a proxy key/url VALUE. Supersedes the design §7.3 T2-reuse default.
3. **Step 5.3 (resolver-binding test):** in `tests/cli/reflect/test_ensemble_fallback_stub.py` — updated the stale None-gated test (renamed / made env-deterministic with `env={}`) and added `test_resolve_t1_fallback_factory_openai_compat_real_binding_is_slot_name_keyed` proving F1 slot-NAME binding on the enabled arm with an injected env (`T1Model01→pool[0]`, `T1Model02→pool[1]`), plus the missing-env degrade. Network-free.
4. **Step 5.4:** scoped Phase 5 run 54/54 passed; scoped ruff clean.

## Effect on production behavior

On a live `superclaude reflect run --depth deep` with the default `--transport openai_compat` and `--tier2-fallback` (default ON), a single transient primary Tier-2 reviewer failure now dispatches a real T1 reviewer (from the dedicated T1 proxy pool) to top up the quorum, instead of collapsing to Tier-1 / exit-11. If the T1 env is incomplete at dispatch, the run degrades gracefully to `terminal_reason: fallback_config_missing` (lazy read inside the controller's catch) rather than crashing.

## Safety properties preserved

- No proxy key/url VALUE written into any source or artifact (verified: no value literals in `ensemble.py`).
- `contract.py` verdict map unchanged; `t2_fallback` remains additive telemetry; a genuine unrepairable failure still degrades to exit 11.
- The `--no-tier2-fallback` flag and the `--transport stub` OFF-default keep a credit-free / deterministic lane.
