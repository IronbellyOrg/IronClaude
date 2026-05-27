---
schema_version: brainstorm-variant/2.0
variant: 1
agent: architect:opus
focus: endpoint cache architecture and policy boundaries
case_id: 8
---

# Proposal Variant 1 — Policy-First API Endpoint Cache (architect:opus)

## Position
Add caching via an explicit endpoint cache-policy registry, not ad-hoc decorators. The registry is the source of truth for eligibility, key dimensions, TTL, invalidation, rollout state, and observability.

## Functional Requirements
- FR1. Endpoint cache-policy registry: every cached endpoint declares eligibility, TTL, key dimensions, invalidation source, rollout flag.
- FR2. Cache only idempotent reads by default; mutations, auth/session, and sensitive endpoints excluded unless explicitly approved.
- FR3. Keys derived from: route, normalized path params, normalized query params, API version, tenant id, auth/role dimensions, content-negotiation headers, feature-flag state when output-affecting.
- FR4. TTL expiration for all cached endpoints; event-driven invalidation when mutations affect cached reads.
- FR5. Global, per-endpoint, per-tenant disable switches.
- FR6. Preserve existing API contracts, status codes, headers, error semantics.

## Non-Functional Requirements
- NFR1. p95 latency reduction ≥ 30% for approved read endpoints in pilot cohort.
- NFR2. Origin load reduction ≥ 20% for cached endpoints in steady state.
- NFR3. Cache lookup failures degrade to origin reads.
- NFR4. Observability by endpoint, tenant cohort, and cache-policy version.

## Security & Correctness
- SEC1. Keys include tenant + authorization dimensions unless policy proves response is globally identical.
- SEC2. Sensitive responses require explicit opt-in review.
- SEC3. Manual purge auditable: actor, time, scope, reason.

## Rollout
- R1. Shadow-metric phase for candidate endpoints.
- R2. Read-through enabled for lowest-risk endpoints first.
- R3. Expansion gated on hit-rate, latency, freshness, and fallback metric thresholds.

## Risks
- Cross-tenant leakage if keys omit auth dimensions.
- Stale reads when invalidation is incomplete.
- Stampede on simultaneous TTL expiry of hot keys.

## Acceptance Criteria
- Three endpoint classes have reviewed cache policies enabled in pilot.
- Disable switches function globally, per endpoint, per tenant.
- Cache keys covered by tests for tenant, auth, query, and version dimensions.
