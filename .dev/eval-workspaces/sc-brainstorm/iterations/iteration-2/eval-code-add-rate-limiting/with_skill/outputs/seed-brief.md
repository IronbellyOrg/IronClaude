---
topic: "add rate limiting to public API endpoints"
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-05-25T00:00:00Z
---

# Seed Brief: add-rate-limiting-public-api

## Socratic Dialogue Record

The following 10 questions (code-domain STANDARD tier: Clarify + Validate batches) were posed and answered to ground the topic.

### Clarify batch

**Q1. What's the entry point — a specific file/function, or a feature you want to introduce?**
A: A new feature. We have a FastAPI-based gateway (`src/api/gateway/app.py`) that fronts ~20 public endpoints. There is no rate-limiting today — we want to introduce it as a middleware layer plus per-endpoint overrides.

**Q2. What's the scope: single-module change, cross-module refactor, or new subsystem?**
A: New subsystem. The middleware itself is one module, but it needs a Redis-backed counter store, a configuration surface (per-endpoint and per-API-key limits), client-facing response headers, and observability hooks. Cross-cutting but contained.

**Q3. What's the failure mode you're trying to prevent / behavior you're trying to add?**
A: Two failure modes: (a) abusive clients (scraping, credential stuffing, accidental loops) overwhelming downstream services; (b) noisy-neighbor effects where one heavy API key starves capacity for others. Behavior to add: per-API-key sliding-window limits, with anonymous-IP fallback when no key is present.

**Q4. Any non-negotiable constraints from existing code (API stability, backward compat, performance SLO)?**
A: Yes. (i) p99 latency budget for the gateway is 50ms — middleware must add ≤2ms p99. (ii) Existing 200/4xx response shapes must not change. (iii) Limits must be configurable without redeploy. (iv) Must not break existing webhook receivers which are async/long-running.

**Q5. What does "done" look like — a passing test? a deployed feature? a code review?**
A: All three, in this order. Unit + integration tests green; a one-week canary at 5% traffic with telemetry showing no SLO regression; full rollout with documented runbook. Done = full rollout and on-call training.

### Validate batch

**Q6. Are there existing implementations in the codebase that this should align with or replace?**
A: No prior rate-limiting code. But there is an existing API-key authn middleware (`src/api/gateway/middleware/auth.py`) that we should sit immediately downstream of — auth resolves the principal first, then rate limit applies. There is also a Redis client pool (`src/api/shared/redis.py`) that we should reuse.

**Q7. Who consumes this — internal callers, external API users, or both?**
A: Both, but limits differ. External (paying customers): tiered by plan (free=60 req/min, pro=600 req/min, enterprise=6000 req/min, with burst allowance). Internal service-to-service calls bypass via a signed bypass header. Anonymous traffic gets a strict IP-based limit (30 req/min).

**Q8. What's the test surface — unit, integration, e2e, or all three?**
A: All three. Unit: window-counter math, header generation, config parsing. Integration: middleware + Redis (with miniredis or a real container). E2E: end-to-end at the gateway with synthetic load proving both enforcement and that bypass works.

**Q9. Is there a deadline or other forcing function?**
A: Soft deadline: next quarter (Q3). The forcing function is that we onboarded a large enterprise customer whose contract requires "documented abuse prevention" — security review needs evidence. Also two recent incidents where misbehaving customer scripts caused brief degradation.

**Q10. What's the rollback plan if this change misbehaves in prod?**
A: Three layers. (i) Feature flag in config to disable enforcement (log-only mode). (ii) Per-endpoint kill switch. (iii) Full middleware bypass via env var (boot-time). Roll forward preferred over rollback because the middleware is additive.

## Problem Statement

The public API gateway has no rate-limiting, exposing the system to abusive clients and noisy-neighbor effects, and blocking onboarding of an enterprise customer whose contract requires documented abuse controls. Two recent minor incidents traced to runaway customer scripts confirm the gap. The solution must add per-principal sliding-window limits with tiered plans, anonymous-IP fallback, and client-facing rate-limit headers, while preserving the existing 50ms p99 SLO and not breaking long-running webhook receivers.

## Known Context

- Gateway entrypoint: `src/api/gateway/app.py` (FastAPI). ~20 public endpoints.
- Existing API-key auth middleware at `src/api/gateway/middleware/auth.py` — rate limiter must sit downstream of it (principal-aware).
- Shared Redis client at `src/api/shared/redis.py` available for counter storage.
- Plan tiers: free=60/min, pro=600/min, enterprise=6000/min, anonymous=30/min (IP).
- Internal service-to-service traffic bypasses via signed bypass header.
- p99 latency budget for gateway: 50ms; rate-limit middleware must add ≤2ms p99.
- Two recent abuse incidents in last 90 days; enterprise contract requires documented abuse controls.
- Webhook receivers are long-running/async — middleware must not break them.

## Constraints

- p99 latency overhead ≤ 2ms (firm).
- Must not change existing 2xx/4xx response body shapes for non-rate-limited requests.
- Must be runtime-configurable without redeploy (limits + per-endpoint overrides).
- Must reuse existing Redis pool; must not introduce a new infra dependency (e.g., separate token-bucket service).
- Must sit immediately downstream of the API-key auth middleware (principal must be resolved first).
- Must provide a log-only mode and per-endpoint kill switch for safe rollout.
- Soft deadline: end of Q3 (this quarter).

## Success Criteria

- All three plan tiers enforced correctly under synthetic load with <0.1% false-positive rate (verified by e2e test).
- Sliding-window algorithm verified deterministic via unit tests across boundary conditions (window wrap, clock skew ≤ 1s, Redis transient errors).
- p99 latency overhead ≤ 2ms measured during canary, ≤ 5ms p99.9.
- Standard client-facing headers emitted on every response: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After` (on 429).
- 429 response includes machine-parseable JSON body with reason code and reset timestamp.
- One-week canary at 5% traffic shows no SLO regression and no false-block tickets.
- Runbook published; on-call trained; documented in security review packet for enterprise customer.

## Open Questions

- Sliding-window algorithm choice: fixed window vs. sliding-window-counter vs. token bucket? Trade-off between memory/Redis cost and burst tolerance not yet decided.
- Should we expose a tenant-self-service "current usage" endpoint, or wait for a v2?
- How to handle distributed clock skew across gateway replicas — best-effort or strict?
- What's the policy for retries-on-429: do we encourage clients to back off via `Retry-After` only, or also recommend a jittered retry library?
- Burst allowance shape: do enterprise plans get a 2x burst over 10s, or a separate burst budget?
- Threat model breadth: do we need to defend against distributed/botnet abuse (where a single principal isn't the right key)?

## Enrichment Context

Codebase enrichment ran in degraded mode (`fallback_2`, native Glob/Grep). Full output at `enrichment/codebase-context.md`. Key signals folded into the brief:

- FastAPI middleware ordering matters — rate limiter goes immediately downstream of `middleware/auth.py`.
- Reuse `src/api/shared/redis.py` (async pool); existing usage patterns are session cache + idempotency keys (no counter primitives yet).
- Config pattern for per-endpoint overrides exists in `config/gateway.yaml`; rate-limit config should reuse the same overlay mechanism.
- Observability stack (Prometheus + OpenTelemetry) already wraps the gateway — emit a counter for `rate_limit_decision{outcome,plan,endpoint}` and a histogram for middleware latency.
- Auth middleware currently returns only `principal_id`; will need extension (or sidecar lookup) to provide `plan_tier`.
- Prior art: `fastapi-limiter`, `slowapi`, or custom `redis.evalsha` sliding-window. Build vs adopt is an open design call.

Confidence on enrichment: medium. A real Auggie semantic pass would tighten the file/symbol claims.
