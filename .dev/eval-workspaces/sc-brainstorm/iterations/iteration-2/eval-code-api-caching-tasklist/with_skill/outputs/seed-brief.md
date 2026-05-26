---
topic: "add caching to the API layer"
domain: code
strategy: systematic
depth: standard
proposal_count: 3
handoff_target: tasklist
created: 2026-05-25T00:00:00Z
---

# Seed Brief: api-layer-caching

## Socratic Dialogue Record

The following 10 questions (code-domain STANDARD tier: Clarify + Validate batches) were posed and answered to ground the topic.

### Clarify batch

**Q1. What's the entry point — a specific file/function, or a feature you want to introduce?**
A: New cross-cutting layer. The API service (`src/api/server.py`, FastAPI) currently has no caching beyond per-instance LRU on a few hot pure functions. We want to introduce a proper caching layer at the request/response boundary, with selective application per route.

**Q2. What's the scope: single-module change, cross-module refactor, or new subsystem?**
A: New cross-cutting middleware + a small subsystem. The cache adapter (Redis-backed) needs to be reusable for non-HTTP callers (background jobs reading the same upstream data), so it sits in a shared module.

**Q3. What's the failure mode you're trying to prevent / behavior you're trying to add?**
A: Two related problems. (a) Hot upstream-data reads (catalog, pricing, feature flags) are causing 60-80% of read latency at p99 and ~70% of upstream-API spend. (b) The upstream catalog API has a rate limit we're approaching during traffic spikes. Caching solves both — cheaper, faster, and fewer upstream calls.

**Q4. Any non-negotiable constraints from existing code (API stability, backward compat, performance SLO)?**
A: (i) No change to response schemas. (ii) Strong consistency required for write paths — caching applies only to GET endpoints classified as "reference data" (catalog, pricing, flags). (iii) p99 latency budget on cache hit ≤ 5ms total (cache lookup + response build). (iv) Cache must degrade gracefully — if Redis is unavailable, fall back to upstream (slow but correct).

**Q5. What does "done" look like — a passing test? a deployed feature? a code review?**
A: All three, plus a one-week production canary at 10% traffic showing the hit-rate and latency improvements. Done = canary clean + full rollout + runbook published.

### Validate batch

**Q6. Are there existing implementations in the codebase that this should align with or replace?**
A: There is per-instance `functools.lru_cache` on three pure functions in `src/api/services/pricing.py`. We should replace those with the new shared cache (cluster-wide visibility) but preserve their semantics. There is also a shared Redis client at `src/api/shared/redis.py` (already used for sessions + idempotency keys) that we will reuse.

**Q7. Who consumes this — internal callers, external API users, or both?**
A: Both. External API users (paying customers) hit the public read endpoints; internal services hit the same endpoints via service-to-service. Cache rules apply uniformly to both; no need to differentiate cache namespaces by caller class.

**Q8. What's the test surface — unit, integration, e2e, or all three?**
A: All three. Unit: cache-key derivation, TTL math, invalidation-event handling. Integration: middleware + Redis (Testcontainer). E2E: load test demonstrating hit-rate target and latency budget. Plus chaos: kill Redis mid-test, assert graceful degradation.

**Q9. Is there a deadline or other forcing function?**
A: Soft deadline: 4 weeks (end of next sprint cycle). The forcing function is upstream API spend (~$8k/month and growing) and the latency complaint trend from two enterprise customers.

**Q10. What's the rollback plan if this change misbehaves in prod?**
A: Three layers. (i) Per-route opt-in: cache must be explicitly enabled on a route by config; the default is off. (ii) Feature flag to globally disable caching middleware (it short-circuits to passthrough). (iii) Per-route TTL=0 forces no caching but keeps the middleware active for telemetry. Roll forward preferred.

## Problem Statement

The API service has no shared caching layer for hot reference-data reads. Catalog/pricing/feature-flag endpoints drive 60-80% of read latency at p99 and ~70% of upstream-API spend (~$8k/month), and traffic spikes approach the upstream catalog API's rate limit. The proposed solution is a Redis-backed request/response cache applied selectively to GET endpoints classified as "reference data," with a 5ms p99 cache-hit budget, graceful degradation if Redis is unavailable, and an explicit opt-in per route. Write-path consistency must remain strong (no caching of writes; targeted invalidation on relevant writes).

## Known Context

- API service entrypoint: `src/api/server.py` (FastAPI).
- Per-instance LRU on three pricing functions in `src/api/services/pricing.py` — to be replaced.
- Shared Redis client at `src/api/shared/redis.py` (async pool; used today for sessions + idempotency keys).
- Catalog API upstream has a rate limit (~500 req/s sustained) that we approach during spikes.
- Upstream spend ~$8k/month, growing.
- Reference-data endpoints currently dominate read latency (60-80% p99 share).
- Latency budget on cache hit: ≤ 5ms p99 total.
- Per-route opt-in design preferred; default-off.
- Soft deadline: 4 weeks.

## Constraints

- p99 cache-hit latency ≤ 5ms.
- No response-schema changes.
- Strong consistency for write endpoints (no write-path caching).
- Must reuse existing Redis pool; no new infra dependency.
- Default off per route; explicit opt-in via config.
- Must include a fail-open path (Redis unavailable → upstream).
- Targeted invalidation on writes that affect cached data (e.g., a catalog item update invalidates that item's cache entry).
- Soft deadline: end of next sprint cycle (~4 weeks).

## Success Criteria

- Reference-data endpoint p99 latency reduced by ≥50% on hit (and ≥10% overall, given hit-rate).
- Upstream API spend reduced by ≥40% on the cached routes.
- Cache hit-rate ≥ 70% sustained on enabled routes (1-week canary).
- Zero stale-data incidents during canary (verified via invalidation correctness tests).
- Graceful degradation: Redis kill in pre-prod load test → 100% requests succeed (slower, no errors).
- Runbook published; on-call trained.

## Open Questions

- Cache-key shape: include API version? Include user-tier (for tier-specific pricing)? Initial preference is include both, but worth a dedicated design pass.
- Invalidation strategy: write-through delete vs TTL-only vs hybrid? Trade-off between staleness and complexity.
- TTL defaults per data class — what's the right default for catalog (rare writes, tolerable staleness ~60s) vs pricing (writes more often, staleness ~10s) vs flags (writes via admin tool, staleness ~5s acceptable for flag flips)?
- Should the same cache layer serve background-job lookups, or just HTTP requests for v1?
- Observability: cache-hit-rate histogram per route vs per endpoint-class — finest reasonable granularity that's still cheap?
- Stampede protection (request coalescing on cache miss): include in v1 or defer?

## Enrichment Context

Codebase enrichment ran (`codebase` track, quality_tier: primary via Auggie). Full output at `enrichment/codebase-context.md`. Key signals folded into the brief:

- Existing per-instance LRU in `pricing.py` is the cleanest seam for the first migration target — same code paths, but elevate cache to Redis.
- Redis client at `src/api/shared/redis.py` already supports pipelined operations; cache adapter will piggyback.
- Config pattern in `config/api.yaml` already has per-route blocks (timeout overrides exist) — cache config slots into the same overlay structure.
- Observability stack already emits per-route latency histograms; add `cache_outcome` label (hit/miss/bypass/degraded) at minimum.
- Write paths that need invalidation: `POST/PATCH /catalog/items/*`, `POST /pricing/rules`, `POST /flags/*`. Targeted invalidation handlers added at these sites.
- Stampede protection: existing `request_id` infra plus a Redis SETNX-based lock primitive provides building blocks; not yet wired for this purpose.

Confidence on enrichment: high (Auggie semantic pass landed cleanly; specific file/symbol citations are concrete).
