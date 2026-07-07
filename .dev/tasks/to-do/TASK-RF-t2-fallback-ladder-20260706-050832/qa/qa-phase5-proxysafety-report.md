# QA Report — Phase 5 Proxy-Safety / Evidence Lens (Step 5.G1)

**Topic:** T1 fallback-ladder real-dispatch enablement — proxy-safety audit
**Date:** 2026-07-07
**Phase:** report-validation (proxy-safety/evidence lens, report-only)

## Overall Verdict: PASS (all 5 stated criteria hold); 3 MINOR observations, none a credential-value leak

The adversarial hypothesis — that Phase 5 leaked a proxy key/url VALUE or added a proxy probe — is not supported. All five criteria pass under zero-trust verification.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | NO proxy key/url VALUE in source/committed artifacts; fake test values confined to the test file | PASS | Value-pattern grep over `reflect/` returned only NAME-config lines + unrelated path false-positives. `unit-test-key`/`t1-proxy:4000` appear ONLY in `test_ensemble_fallback_stub.py`. In QA reports the tokens appear only as forbidden-string-list search targets. |
| 2 | `_T1_PROXY_BINDING` = four NAME/config keys only, no resolved credential | PASS | dict = `{model_prefix:"T1Model0", proxy_url_env:"T1ProxyUrl", proxy_key_env:"T1ProxyKey", max_slots:T1_MODEL_MAX_SLOTS}`. Env-var NAME strings + an int ceiling. No URL, no key. |
| 3 | Proxy creds live only inside the `build_transport` closure; never returned/logged/surfaced | PASS (caveat P5-PS-01) | `pool_config` (`.base_url`/`.api_key`) is a local in `_lazy_openai_factory`, referenced only inside `_build_transport`. Never returned/logged/placed in the contract. |
| 4 | No `:4000/v1` or proxy-API probe added; env check is NAMES-only grep | PASS | Probe-pattern grep over `reflect/` → zero hits. The env confirmation is `grep -oE '^(export )?(T1ProxyUrl|...)' ~/.aienv` — NAME extraction only. Decision artifacts attest NAMES-only. |
| 5 | Resolver-binding test injects fake env; network-free | PASS | `missing_env_degrades` passes `env={}` (deterministic, never os.environ); `real_binding` passes a fake env and asserts F1 binding; `OpenAICompatTransport` constructed but never `.send()`-ed. |

## Summary
- Checks passed: 5 / 5
- Credential-VALUE leaks (key or url) in source/committed artifacts: 0
- Hardening observations (MINOR, none a value-leak): 3

## Issues Found

| # | Severity | Location | Issue | Fix decision |
|---|----------|----------|-------|-------------|
| P5-PS-01 | MINOR (OUT-OF-SCOPE) | `swarm/transports/openai_compat.py` `send()` `httpx.RequestError` arm | On a REAL T1 fallback network failure, `body=str(exc)` is stashed on `WorkerResult.body` and materialized to a raw artifact; httpx `RequestError` strings can embed the request URL (base_url). The api_key does NOT leak (lives in the Bearer header, not rendered by `str(exc)`). Shared PRE-EXISTING T2 transport behavior, NOT introduced by this task; Phase 5 only newly routes T1 through it. Out of the task's changed surface (the task extended `read_env_for_pool`, not `send()`). | Follow-up (not this task): scrub the request URL from `str(exc)` before persisting to `body`, or redact host in the raw-artifact writer. Runtime-only, uncommitted, URL-not-key. |
| P5-PS-02 | MINOR | `test_contract_fallback_metadata.py` no-proxy-leak guard | The guard dumps the contract to YAML and scans a 13-token forbidden list — correct for the `t2_fallback` metadata dump, but does not cover on-disk per-worker `raw.md` bodies (where P5-PS-01's URL could land). | Optional hardening: a sibling assertion scanning materialized worker artifacts. The actual leak vector (P5-PS-01) is out-of-scope; the guard's contract coverage is correct for what THIS task added. |
| P5-PS-03 | MINOR (informational — NOT a leak) | `openai_compat.py` `TransportEnvError.__str__` | For an incomplete T1 pool, the `.missing` tuple is correct (T1 NAMES) but the inherited message text is T2-worded. Zero credential-safety impact — identical to the Phase 4 F2/F3 finding already ACCEPTED (folded into `fallback_config_missing`, never operator-surfaced). | ACCEPT (same rationale as Phase 4 F2/F3). |

## Recommendations

1. Green light on proxy-safety — no proxy secret leaked into source/committed artifacts, no `:4000/v1`/proxy-API probe added. The credential-scoping design (lazy env read inside the closure, creds confined to `_build_transport`, NAMES-only binding + errors) is sound.
2. Follow-ups (out-of-scope / non-blocking): P5-PS-01 (scrub request URL from `str(exc)` in the shared transport), P5-PS-02 (widen the no-leak guard to worker bodies). Neither is a gate-blocker for this task.

## QA Complete
