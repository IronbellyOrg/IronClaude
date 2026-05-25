---
proposal_id: 1
persona: architect
model: opus
lens: coherency model, invalidation correctness, long-term extensibility
---

# Proposal 1 — Architect: Build the Cache as a Coherency Subsystem, Not a Middleware

## Position

Caching looks like a middleware problem until the first stale-data incident. Then it's a coherency problem. Build for the coherency model from day one — explicit invalidation events, structured cache keys, an inspectable cache surface — and the middleware is a thin shell. Build it as "stuff a hash and a TTL into Redis," and the second time a customer sees a stale price on a deal that already changed, you'll be retrofitting the coherency model under production pressure.

## Architecture

Five components, all under `src/api/cache/` (new package):

1. **`CacheKey`** — value object: `{route_id, api_version, user_tier, params_hash}`. Structured, not opaque. Inspectable in logs without leaking data. Comparable across processes.
2. **`CacheAdapter`** — async interface over Redis with `get`, `set`, `delete`, `delete_prefix`. Hides Redis primitives from middleware.
3. **`InvalidationDispatcher`** — event bus. Write handlers publish typed invalidation events (`CatalogItemUpdated`, `PricingRuleChanged`, `FlagSet`); subscribers map events to `CacheAdapter.delete_prefix(...)` calls. New write routes register handlers explicitly.
4. **`RequestCacheMiddleware`** — 40-line FastAPI middleware. On enabled routes: compute key → adapter.get → return cached or proxy + adapter.set. Emits `cache_outcome` counter.
5. **`CacheInspector`** — debug-only HTTP endpoint (admin-only) to introspect a single cache key's status (TTL remaining, last-write time, source-route). Critical for debugging stale-data tickets.

## Why this shape

**Invalidation correctness is the load-bearing concern.** A cache that returns stale data is worse than no cache — customers prefer "slow but right" over "fast but wrong" by a wide margin. The event-bus shape forces every write handler to opt into invalidation explicitly. Without the bus, the next person who adds a write route on a cached resource forgets to invalidate, and the next stale-data ticket has no upstream "you forgot to wire this up" trail.

**Structured keys make debugging tractable.** When a customer reports stale data, the on-call engineer needs to answer "which key was served, when was it written, what was the TTL?" A structured `CacheKey` + the `CacheInspector` endpoint makes that a 30-second answer. An opaque hash makes it a 2-hour archaeology.

**The pricing-LRU migration is a graceful seam.** The existing LRU has known-correct semantics; the migration replaces the storage layer (per-pod → Redis) without changing the function-level interface. This is a low-risk first migration target that proves the adapter before riskier work (catalog, flags).

## Coherency contract

- **Read-after-write within a single request**: a write handler that completes successfully invalidates affected entries *before* the response returns. A subsequent read in the same conversation sees the new state.
- **Eventual consistency across replicas**: invalidation event propagation is bounded — the cache entry is gone within ~50ms of the write commit. The TTL acts as an upper bound on staleness if invalidation fails entirely.
- **No write-path caching ever**: explicit. POST/PATCH/DELETE never touch the cache for read; writes only trigger invalidation.
- **Cache responses are never stale by intent**: TTL is a *bound*, not a *target*. Architectural posture: prefer cache miss over stale hit when in doubt.

## What I'd push back on

The "just add a middleware that wraps Redis" framing optimizes for week one and trades away every adjacent need. Stampede protection (which the performance reviewer will raise) is one example — without the adapter pattern, stampede protection has to be re-implemented at every callsite. The CacheInspector endpoint is another — without structured keys, it's not implementable. And the invalidation event bus is the third — without it, the next stale-data incident leaves the team chasing ghost dependencies.

The refactorer's "thin layer" position is right on cost (this is more code than necessary for week one) but wrong on debt (every shortcut here lands as a SEV in months 6-12).

## Cost

~6-8 engineering days vs ~3 for a thin middleware. The premium pays back the first time we have to debug a stale-data ticket without spending 2 hours in Redis CLI.

## Concession to refactorer

The CacheInspector endpoint can be deferred to v1.1 if shipping pressure is intense — the structured-key + invalidation-event work cannot. Inspection is a debugging accelerant; the other two are correctness load-bearing.

## Concession to performance

Stampede protection (FR5) should be in v1, not v1.1. Performance is right that an untracked stampede on a popular uncached key is a SEV waiting to happen. The SETNX + wait pattern is ~30 lines and fits cleanly into the adapter.
