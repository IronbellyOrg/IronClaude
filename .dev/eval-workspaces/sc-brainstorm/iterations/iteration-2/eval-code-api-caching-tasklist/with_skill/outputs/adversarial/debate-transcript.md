---
debate_round: 1
proposals: [proposal-1-architect, proposal-2-refactorer, proposal-3-performance]
convergence_score: 0.81
---

# Adversarial Debate Transcript

Three proposals against `seed-brief.md`. Convergence score 0.81 reflects strong agreement on the *what* (middleware + per-route config + Redis adapter + opt-in + observability) and a productive disagreement on the *shape* (subsystem vs thin middleware) that resolved cleanly along cost/timing lines.

## Tension 1 — Subsystem vs thin middleware (Architect vs Refactorer)

**Architect's position**: Five-component package under `src/api/cache/`. Structured CacheKey, CacheAdapter, InvalidationDispatcher (event bus), RequestCacheMiddleware, CacheInspector endpoint.

**Refactorer's pushback**: Single middleware file, inline invalidation, private key-derivation function, no inspector endpoint. Three known write paths don't justify an event bus.

**Resolution**: **Refactorer wins on shape, architect wins on discipline.** Single module (`src/api/middleware/request_cache.py`) + separate invalidation module + structured cache-key format (FR2 — architect's `CacheKey` fields, refactorer's "it's a private function" implementation). InvalidationDispatcher exists as a thin coordination point (FR4) but is implemented as a registry of inline handlers, not an async event bus. CacheInspector endpoint deferred to v1.1 (architect's concession). This adopts the architect's structural posture without paying the full subsystem cost.

## Tension 2 — Invalidation strategy (Architect vs Refactorer; Performance arbitrates)

**Architect's position**: Event-bus invalidation. Write handlers publish events; cache adapter subscribes. Future-proof for 20+ write routes.

**Refactorer's position**: Inline `await cache.delete(key)` calls from the 3 known write routes. No infrastructure required.

**Performance's tiebreak**: Either works for v1 *if* invalidation correctness is tested under concurrent write/read (failure mode 5). The event bus does not improve correctness — only ergonomics for future writers. Adopt the cheaper option.

**Resolution**: **Inline invalidation for v1 (refactorer), with a registry shim (FR4) that makes the future event-bus refactor mechanical.** PR checklist mandates that any new write route on cached data adds its invalidation handler at the source. Integration test verifies each known write route triggers expected invalidation (AC2). Risk R1 (stale data) explicitly cited.

## Tension 3 — Cache-key shape (Architect vs Refactorer)

**Architect's position**: Structured `CacheKey` value object with `route_id`, `api_version`, `user_tier`, `params_hash`.

**Refactorer's position**: Documented string format from a private function. Same fields, less ceremony.

**Performance's contribution**: Either works. The *content* of the key must include `user_tier_or_anon` to prevent cross-tier collisions (R4) — anonymous-vs-authenticated pricing must produce distinct keys. Also raised: should body hash be in the key? Affected endpoints today: 1.

**Resolution**: **Adopt the architect's field list, the refactorer's implementation.** FR2 specifies the format. Body-in-key deferred to OQ1 — the one affected GET-with-body endpoint opts out of caching until reviewed.

## Tension 4 — Stampede protection: v1 or v1.1? (Architect deferred initially; Performance + Refactorer pushed)

**Architect's initial position**: Stampede protection is important but could be v1.1 if shipping pressure is intense.

**Performance's pushback**: This is the load-bearing v1 feature. Without it, the cache *amplifies* traffic spikes at TTL boundaries — exactly the opposite of the intended effect. The first time a popular catalog key expires under load, you've made the problem worse. Failure mode 1.

**Refactorer's reply**: ~30 lines using the existing SETNX primitive in `src/api/shared/locks.py`. The marginal cost is low; the marginal value is high. v1.

**Resolution**: **Performance + Refactorer win.** FR5 is v1. Test in AC3 (1000 concurrent first-callers → ≤2 upstream calls). Architect concedes; this was their original position softened under shipping pressure, and the team agreed shipping pressure shouldn't override the load-bearing piece.

## Tension 5 — Background-job access to the same cache (open question from seed brief)

**Architect's position**: Same cache adapter, exposed as a programmatic read-only API for non-HTTP callers.

**Refactorer's position**: Defer to v1.1 — HTTP is the v1 surface; background jobs are a v1.1 add.

**Performance's contribution**: If background jobs hit the same upstream APIs, they cause cache stampedes by warming separately. Better to share the cache and let HTTP traffic benefit from warmed entries.

**Resolution**: **Architect + Performance win.** FR7 in v1. Read-only programmatic API for `src/jobs/catalog_refresher.py` and `src/jobs/pricing_warmer.py`. No invalidation rights from background jobs (keeps the surface narrow).

## Tension 6 — Observability granularity (Performance pushes for full-label counters)

**Performance's position**: Outcome counter must include all five labels (hit, miss, bypass, degraded, stampede_waited). "Hit rate is 70%" hides too much without the breakdown.

**Architect's reply**: Agreed. Counter labels are cheap; lack of granularity is the actual cost.

**Refactorer's reply**: Agreed. Adds ~5 lines to the middleware.

**Resolution**: **Unanimous.** FR9 specifies the five-label outcome counter. AC4 verifies the `degraded` outcome on chaos test.

## Tension 7 — CacheInspector debug endpoint (architect)

**Architect's position**: Admin-only endpoint to inspect a single cache key's status (TTL remaining, last-write time, source-route).

**Refactorer's position**: v1.1 — debugging works via `request_id` + Redis CLI today. Not load-bearing.

**Performance's position**: Useful for operating the cache but not load-bearing for shipping. v1.1.

**Resolution**: **Deferred to v1.1.** Architect concedes; the structured-key + outcome-counter combination provides enough on-call debugging surface for v1.

## Remaining disagreements (logged for transparency)

- **OQ1 — Body-in-cache-key**: Carried forward; one affected endpoint opts out for v1.
- **OQ3 — X-Cache response headers**: Architect favors expose (debug aid for customers); Performance favors internal-only (information leakage potential). Carried forward as open question.

## Convergence rationale

Three proposals, seven tensions, all but two resolved with clear positions. Strong consensus on the *correctness* concerns (stampede protection, invalidation discipline, structured-key fields). Productive disagreement on *shape* (subsystem vs middleware) resolved by adopting refactorer's shape with architect's discipline. Convergence score **0.81** — strong PASS. Open questions are bounded and defensible.
