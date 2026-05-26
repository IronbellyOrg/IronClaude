---
spec_type: requirements
domain: code
strategy: systematic
adversarial_status: pass
convergence_score: 0.81
proposal_count: 3
source_proposals: [proposal-1-architect, proposal-2-refactorer, proposal-3-performance]
source_seed: ../seed-brief.md
debate_transcript: ./adversarial/debate-transcript.md
agents: "opus:architect:'prioritize cache-coherency model, invalidation correctness, and long-term extensibility',sonnet:refactorer:'focus on minimal blast radius, reusing existing primitives, and incremental migration',haiku:performance:'focus on latency budget, hit-rate, stampede, and load characteristics'"
---

# Merged Requirements: API Layer Caching

## Problem Statement

The API service has no shared caching layer for hot reference-data reads. Catalog/pricing/feature-flag GET endpoints drive 60-80% of read latency at p99 and ~70% of the API's upstream spend (~$8k/month and growing); peak traffic approaches the catalog upstream's rate limit. The solution is a Redis-backed request/response cache, opt-in per route, applied only to GETs classified as reference data, with strong-consistency write paths and targeted invalidation on writes that affect cached data. Cache hits must satisfy a 5ms p99 budget; Redis unavailability must degrade gracefully to upstream calls (slower but correct). The forcing functions are upstream spend trajectory and two enterprise latency complaints.

## Constraints

- **C1** — p99 cache-hit latency ≤ 5ms; p99.9 ≤ 12ms. *(seed brief Q4; firm)*
- **C2** — No changes to response schemas or to non-cached request paths' behavior. *(seed brief Q4)*
- **C3** — Strong consistency for write endpoints. Writes are never cached; writes trigger targeted invalidation of any cached entries they affect. *(seed brief Q4; debate Tension 2)*
- **C4** — Reuse existing async Redis pool (`src/api/shared/redis.py`). No new infra dependency. *(seed brief Q6; enrichment)*
- **C5** — Default off per route. Caching enabled only on routes with an explicit `cache:` config block. *(seed brief Q10)*
- **C6** — Graceful degradation: if Redis is unavailable, route falls through to upstream; cache outcome telemetry records `degraded`. *(seed brief Q4, Q10)*
- **C7** — Soft deadline: end of next sprint cycle (~4 weeks). *(seed brief Q9)*

## Functional Requirements

- **FR1** — Implement a `RequestCacheMiddleware` (FastAPI) that, on enabled routes, computes a cache key, queries Redis, returns cached response on hit, otherwise proxies to the handler and writes the response to cache on success (2xx only). Lives at `src/api/middleware/request_cache.py`. *(seed brief Q1; debate Tension 1 consensus)*
- **FR2** — Cache key shape: `cache:{route_id}:{api_version}:{user_tier_or_anon}:{normalized_params_hash}`. `route_id` is the FastAPI route name; `api_version` from the request; `user_tier` derived from the auth result (or `anon`); `normalized_params_hash` is a stable SHA-256 of sorted query + path params. *(seed brief OQ "cache-key shape"; debate Tension 3)*
- **FR3** — TTL configuration: per-route, with class defaults — `catalog: 120s`, `pricing: 30s`, `flags: 15s`. Configurable override per route in `config/api.yaml`. *(seed brief OQ "TTL defaults"; performance proposal §latency-vs-staleness)*
- **FR4** — Invalidation: writes that affect cached data emit a structured invalidation event consumed by an `InvalidationDispatcher` (`src/api/middleware/cache_invalidation.py`). Affected sites: `POST/PATCH /catalog/items/*` (invalidates the item's entry + the parent list entry), `POST /pricing/rules` (invalidates affected pricing entries), `POST /flags/*` (invalidates the flag entry). *(seed brief Q6; debate Tension 2)*
- **FR5** — Stampede protection: on cache miss, requests for the same key within a 200ms window coalesce via a Redis SETNX-based lock. The first request fetches and populates; subsequent requests wait (up to 300ms) and read the cached result. *(performance proposal §stampede; debate Tension 4)*
- **FR6** — Migrate existing per-instance LRU on `src/api/services/pricing.py` to use the shared cache adapter. Preserve function-level semantics (same input → same output). LRU is removed after migration verified. *(seed brief Q6; refactorer proposal §migration)*
- **FR7** — Background-job lookups (non-HTTP callers of the same upstream data) consume the same cache adapter via a programmatic API. Read-only access from background jobs; no invalidation rights. *(seed brief OQ; debate Tension 5)*
- **FR8** — Per-route config block in `config/api.yaml`:
  ```yaml
  routes:
    GET_catalog_items:
      cache:
        enabled: true
        ttl_seconds: 120
        class: catalog
        stampede_protection: true
  ```
  *(refactorer proposal §config)*
- **FR9** — Observability: emit `api_cache_outcome_total{route, outcome}` Prometheus counter (`outcome` ∈ {hit, miss, bypass, degraded, stampede_waited}) and `api_cache_lookup_seconds{route}` histogram. *(performance proposal §observability; debate Tension 6)*

## Non-Functional Requirements

- **NFR1** — p99 cache-hit latency ≤ 5ms end-to-end; p99.9 ≤ 12ms; measured on canary. *(C1)*
- **NFR2** — Cache hit-rate ≥ 70% sustained on enabled routes during canary. *(seed brief success criteria)*
- **NFR3** — Zero stale-data incidents during canary. Invalidation must be correct under concurrent write/read (verified by integration test). *(seed brief success criteria; debate Tension 2)*
- **NFR4** — Graceful degradation: Redis kill in pre-prod load test results in 100% request success (slower) and zero error responses. Degraded path latency must not exceed pre-cache baseline by >5%. *(C6; performance proposal §degradation)*
- **NFR5** — Memory ceiling: per-instance cache memory footprint negligible (Redis-only). Redis memory ceiling: cached payloads bounded by per-class limit (`catalog: 200MB`, `pricing: 50MB`, `flags: 5MB`) with LRU eviction within each namespace. *(architect proposal §coherency; performance proposal §capacity)*

## Acceptance Criteria

- **AC1** — Unit suite: ≥25 cases covering key derivation (all field combinations), TTL math (incl. boundary conditions), invalidation-event payload validation, fail-open path semantics. All green. *(performance proposal §test plan)*
- **AC2** — Integration suite: ≥12 cases with real Redis (Testcontainer). Cover Redis unavailability → fall-through, concurrent write/read with invalidation, stampede coalescing (verified by spawning N=20 concurrent first-callers), pricing-LRU-migration parity (same input/output as before). All green. *(performance proposal §test plan; refactorer proposal §migration)*
- **AC3** — E2E load test: sustained 5-minute load on a representative reference-data endpoint shows hit-rate ≥70% and p99 cache-hit latency ≤5ms. Stampede scenario (1000 concurrent requests for a single uncached key) shows ≤2 upstream calls. *(NFR1, NFR2, FR5)*
- **AC4** — Chaos test: kill Redis mid-load → 100% requests succeed; outcome counter shows `degraded`; latency does not exceed pre-cache baseline by >5%. *(NFR4)*
- **AC5** — Canary: 1-week at 10% traffic on enabled routes shows ≥50% p99 latency reduction on hit and ≥40% upstream-spend reduction on cached routes. Zero stale-data tickets. *(seed brief success criteria)*
- **AC6** — Runbook published at `docs/runbooks/api-caching.md` covering: cache-stampede investigation, "customer reports stale data" debug path, Redis degraded behavior, manual invalidation procedure. On-call trained. *(seed brief Q5)*

## Risks

- **R1** (severity: HIGH) — **Stale data after a missed invalidation.** A write that should invalidate a cache entry but doesn't (because the invalidation handler is missing or buggy) produces customer-visible stale data — exactly the failure the strong-consistency constraint exists to prevent. *Mitigation*: Invalidation handlers are mandatory on the affected write routes (PR checklist); integration test asserts each affected write route produces the expected invalidation event; TTL acts as an upper bound on staleness even if invalidation fails.
- **R2** (severity: HIGH) — **Latency budget overrun on cache hit.** 5ms p99 budget assumes Redis lookup ≤2ms + response build ≤2ms + headroom. Tail-latency Redis spikes can blow it. *Mitigation*: pipelined lookup for compound keys; measured in canary on a representative endpoint before full rollout; budget is per-route — a single slow route can be opted-out without affecting others.
- **R3** (severity: MEDIUM) — **Stampede on a popular uncached key.** First request after eviction triggers an upstream storm if N=many concurrent requests arrive. *Mitigation*: FR5 stampede protection (SETNX lock + 300ms wait window); load test verifies ≤2 upstream calls for 1000 concurrent first-callers.
- **R4** (severity: MEDIUM) — **Cache-key collisions.** A bug in the key normalization produces keys that conflate distinct requests; users see each other's data. Catastrophic if it happens. *Mitigation*: key includes `user_tier_or_anon`; integration test verifies anon vs authenticated returns distinct keys; per-tier pricing test verifies tier isolation; security review on the key function.
- **R5** (severity: LOW) — **Memory growth from unbounded cache.** Without per-class memory limits, the cache could grow until eviction kicks in unpredictably. *Mitigation*: NFR5 per-class limits with LRU eviction in each namespace.

## Open Questions

- **OQ1** — Should we include the request body hash in the cache key for GET endpoints that accept body params (rare, but exist)? Current proposal: no body in key; affected endpoints (one currently) opt out of caching until reviewed.
- **OQ2** — Cross-region cache strategy: today Redis is single-region; if we add a second region next quarter, do we run independent caches (eventual consistency between regions) or replicate? Deferred to a follow-up brainstorm.
- **OQ3** — Should we expose a tenant-visible "cache headers" surface (`X-Cache: hit`, `X-Cache-TTL-Remaining: ...`) for debuggability, or keep it internal? Architect favors expose; performance favors internal-only.

## Out of Scope (explicit)

- Caching of write endpoints (POST/PATCH/DELETE) — these remain pass-through.
- CDN-level caching (Cloudflare/Fastly tier) — separate decision, separate system.
- In-process LRU as a tier (L1 in front of Redis L2) — considered and deferred; the latency budget is met without it for v1.
- Multi-region cache replication — see OQ2.

## Provenance

| Requirement | Origin |
|---|---|
| FR1 (middleware) | All three proposals agreed on the shape |
| FR2 (cache-key) | Debate Tension 3 — architect proposed structured key, refactorer wanted simpler hash, performance verified collision risk; merged shape adopted |
| FR3 (TTL config) | Performance proposal §latency-vs-staleness; refactorer proposal §config |
| FR4 (invalidation) | Seed brief Q6; debate Tension 2 (architect wanted event bus, refactorer wanted inline, hybrid adopted) |
| FR5 (stampede) | Performance proposal §stampede; debate Tension 4 (architect deferred v1, performance + refactorer insisted on v1) |
| FR6 (LRU migration) | Refactorer proposal §migration |
| FR7 (background-job access) | Seed brief OQ; debate Tension 5 |
| FR8 (config block) | Refactorer proposal §config |
| FR9 (observability) | Performance proposal §observability |
| NFR1-NFR2 | Seed brief Q4, success criteria |
| NFR3 (zero stale) | Seed brief success criteria; debate Tension 2 |
| NFR4 (graceful degrade) | Seed brief Q4; performance proposal §degradation |
| NFR5 (memory ceiling) | Architect proposal §coherency; performance proposal §capacity |
| AC1-AC6 | Aggregated, performance proposal led the test plan |
| R1 (stale data) | Debate Tension 2 — primary risk identified by all three |
| R2 (latency overrun) | Performance proposal §risk |
| R3 (stampede) | Performance proposal §stampede; FR5 mitigation |
| R4 (key collision) | Debate Tension 3 — architect raised; security framing |
| R5 (memory) | Architect proposal §coherency |
| OQ1 (body in key) | Debate Tension 3 carry-forward |
| OQ2 (cross-region) | Architect proposal §future; deferred |
| OQ3 (X-Cache headers) | Architect vs performance disagreement; deferred |
