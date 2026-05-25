---
proposal_id: 2
persona: refactorer
model: sonnet
lens: minimum-viable, reuse existing primitives, incremental migration
---

# Proposal 2 — Refactorer: Adopt a Thin Cache Layer, Migrate Pricing First, Iterate

## Position

The architect's coherency-subsystem framing is right *in spirit* but premature *in shape*. The codebase already has a Redis client, a SETNX lock primitive, a per-route config pattern, and a per-instance LRU that's a perfect migration testbed. The job is to **adapt what we have, migrate the smallest seam first, and add complexity only as the test surface demands it.** A 5-component package is debt — 5 places for the next engineer to misunderstand. Build one module, prove it on pricing, then expand.

## What to build (v1)

A single file: `src/api/middleware/request_cache.py`. ~200 lines including tests.

```
class RequestCacheMiddleware:
    - __init__(redis_pool, route_config_loader)
    - async __call__(request, call_next):
        - if route not in cache-enabled config: passthrough
        - key = _derive_key(request)
        - cached = await self.redis.get(key)
        - if cached: return _build_response(cached, headers={"x-cache": "hit"})
        - response = await call_next(request)
        - if response.status_code in (200, 304):
            - await self.redis.setex(key, ttl, _serialize(response))
        - return response
```

That's the v1. Two additional small modules:

- `src/api/middleware/cache_invalidation.py` — ~80 lines. Inline invalidation calls from the three known write routes. No event bus; explicit calls. If we add more write routes that need invalidation, we add explicit calls.
- `src/api/services/pricing.py` — refactor the three LRU-decorated functions to call the cache adapter directly. Function signatures unchanged.

## Why this shape

**The blast radius of new code is real.** A 5-component package introduces 5 places for misunderstanding. A single middleware + two helpers is auditable in one PR. The architect's "structured CacheKey + InvalidationDispatcher + CacheInspector" pattern is what the code *will look like in 6 months* if it earns it, but shipping it in week one trades real engineering time against speculative needs.

**Inline invalidation > event bus for 3 known write paths.** Event buses are the right answer when (a) you don't know all the writers, (b) the writers shouldn't have to know about subscribers, or (c) you need async fan-out. None of those apply here. Three write routes, all known, all owned by the same team. Inline `await cache.delete(...)` after the write commit is one line per site, no infrastructure.

**Pricing migration is the right first seam.** Three functions, known-correct semantics, hit-rate already measured (~85%). Migration to Redis preserves the interface; only the storage layer changes. Verifying it produces the same outputs is a few lines of differential test. This proves the cache adapter before we point it at messier code.

## On the architect's "CacheInspector"

Disagree on day-one inclusion. We have `request_id` propagation and Prometheus counters; debugging stale data starts with the counters (which key class had a high `outcome=hit` rate when the customer reported staleness?) and proceeds via Redis CLI for the specific key. A dedicated admin endpoint is nice but is a v1.1 — not a load-bearing piece of v1.

## On the architect's "structured CacheKey"

Mostly agree on shape, disagree on framing. The key needs route + version + tier + params-hash — that's table stakes, not a "value object". I'll write it as a private function (`_derive_key`) returning a string in a documented format. Same fields, less ceremony.

## On stampede protection (performance reviewer's concern)

Right call. Use the existing `src/api/shared/locks.py` SETNX primitive. ~20 additional lines. Goes into v1.

## Migration sequence

1. Ship the thin middleware + per-route config + inline invalidation on the three known write routes.
2. Migrate `pricing.py`'s LRU → adapter. Differential test asserts behavior preserved.
3. Enable cache on one catalog endpoint behind a feature flag. 10% canary. Observe.
4. Enable cache on flag-reads. Observe.
5. Iterate based on what we actually saw, not what we guessed.

## What I'd push back on

The architect is solving for a future where we have 20 write paths invalidating 50 cache key prefixes across 8 cache classes. We have 3 write paths invalidating 3 cache classes. Build for what's in front of us. If/when we get to 20 write paths, refactor the inline calls into an event bus *with the benefit of real evidence about the actual coupling shape*.

## Cost

~3 engineering days for the middleware + invalidation + pricing migration. Another ~2 for tests + integration verification. ~5 days total inside a 4-week deadline leaves room for canary observation and adjustment.

## Concessions

- Stampede protection is in v1, agreed with performance reviewer.
- TTL defaults per data class (catalog/pricing/flags), agreed.
- Observability counter with `outcome` label is non-negotiable v1, agreed.

## What I'd defer

- CacheInspector endpoint → v1.1.
- Cross-region replication strategy → separate brainstorm.
- Body-in-key handling → opt out the one affected endpoint, defer.
