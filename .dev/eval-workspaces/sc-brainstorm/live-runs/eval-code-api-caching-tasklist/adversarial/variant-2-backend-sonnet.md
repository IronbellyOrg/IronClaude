---
schema_version: brainstorm-variant/2.0
variant: 2
agent: backend:sonnet
focus: implementation mechanics, invalidation, resilience
case_id: 8
---

# Proposal Variant 2 — Read-Through Cache With Invalidation Hooks (backend:sonnet)

## Position
Implement endpoint caching as backend read-through middleware with endpoint-specific policy metadata and resource invalidation hooks. Prioritise safe operational behaviour: origin fallback, stampede protection, metrics, controlled rollout.

## Functional Requirements
- FR1. Read-through cache behaviour for approved GET / list / detail endpoints.
- FR2. Per-endpoint cache policy object: TTL, key builder, invalidation topics, stale-if-error eligibility, rollout flag.
- FR3. Normalised cache keys — semantically equivalent query strings map to the same entry.
- FR4. Mutation-driven invalidation; unsupported invalidation paths force short TTLs or no caching.
- FR5. Stampede prevention via single-flight request coalescing or per-key locking on hot keys.
- FR6. Stale-if-error only for endpoints explicitly marked safe for bounded-stale data.
- FR7. Manual purge APIs at endpoint, resource, tenant, and global scope.

## Non-Functional Requirements
- NFR1. Cache hit path adds ≤ 10 ms p95 overhead beyond cache-backend latency.
- NFR2. Cache miss path adds ≤ 15 ms p95 overhead over current origin behaviour.
- NFR3. Cache-backend outage must not take down the API; bypass + alert.
- NFR4. Metrics: hit ratio, miss ratio, origin fallback count, stale-served count, invalidation count, purge count, backend errors.

## Testing Requirements
- T1. Unit tests for key normalisation and dimension coverage.
- T2. Integration tests for mutation-driven invalidation.
- T3. Load tests proving latency and origin-load improvements under representative traffic.
- T4. Fault-injection tests: cache outage, high miss rate, stampede behaviour, invalidation failure.

## Rollout Requirements
- R1. Ship disabled by default.
- R2. Shadow mode to compute would-hit rates without serving cached responses.
- R3. Read-through enabled for one endpoint class + limited tenant cohort.
- R4. Expand via feature flags after metrics meet thresholds for seven consecutive days.

## Open Questions
- Which cache backend is available and what are its reliability characteristics?
- Is there an existing domain event stream for invalidation?
- Which endpoints have bounded staleness tolerance?
