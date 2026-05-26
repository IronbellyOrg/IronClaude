---
proposal_id: 3
persona: performance
model: haiku
lens: latency budget, hit-rate, stampede, load characteristics
---

# Proposal 3 — Performance: Stampede Protection, Latency Budget, and the Failure Modes Everyone's Skipping

## Position

The architect and refactorer are arguing about how much *structure* the cache should have. I want to talk about what happens **the first time a popular cached key expires under 1000 req/s.** Without stampede protection, that's an instant upstream storm — exactly the failure the cache exists to prevent. Either v1 ships with it, or v1 is missing the load-bearing piece that justifies the project.

## Failure modes I expect to find

1. **Cache stampede on hot-key expiry.** Popular catalog item TTL expires; 1000 concurrent requests miss simultaneously; all 1000 call upstream. Upstream rate-limit hit, every response slow, every customer affected. *Test this*. SETNX + 300ms wait window is the standard mitigation; ~30 lines.

2. **Latency budget overrun in p99.9.** The 5ms p99 budget for cache-hit is achievable on average but the long tail (Redis spike + connection-pool contention + serialization overhead) blows past it. Need to budget p99.9 ≤12ms and measure on canary; per-route opt-out if a specific route can't hit budget.

3. **Hit-rate degradation under cache-warming asymmetry.** New deployment → all caches cold → every request misses → upstream storm during deploy. *Mitigation*: warm the cache at boot for known-hot keys, or accept a "cache-warming canary" pattern where deploys roll slowly enough to warm naturally.

4. **Cache size unbounded → OOM eviction surprise.** Without per-class memory limits in Redis, the largest cache class consumes more than its share and LRU evicts from other classes unexpectedly. Per-class namespacing with explicit memory ceilings is mandatory.

5. **Invalidation correctness under concurrent write/read.** Reader pulls value V1 → writer updates to V2 → writer triggers invalidate(K) → reader's cached V1 was already read (consistent) BUT a *next* reader between the write commit and invalidation event sees V1 again. Test: write + immediate read race; verify staleness window is bounded by invalidation propagation time.

6. **Degraded-Redis tail latency.** Redis "available but slow" is worse than "unavailable" — middleware waits for a slow response on every key before timing out. Need an aggressive Redis client timeout (≤3ms) with circuit-breaker semantics — too many timeouts → flip to degraded mode for N seconds.

7. **Body serialization overhead.** Large responses (catalog list responses can be 50KB+) serialize/deserialize through Redis on every hit. JSON-vs-orjson choice matters; measure.

8. **Observability blind spots without per-outcome counters.** "Hit rate is 70%" hides a 5% stampede-waited rate, a 2% degraded rate, and a 3% bypass rate. Outcome counter labels must include all five outcomes (hit, miss, bypass, degraded, stampede_waited) or we can't debug.

## Stampede protection (FR5) — the load-bearing v1 feature

This is the difference between caching as a *latency improvement* and caching as a *resilience improvement*. Without it, the cache is fragile under exactly the conditions where it's most valuable (high traffic on a hot key). With it, the cache absorbs traffic spikes; without it, the cache amplifies them at expiry boundaries.

Implementation sketch (using existing `src/api/shared/locks.py` SETNX primitive):

```
async def get_or_populate(key, ttl, fetch_fn):
    cached = await redis.get(key)
    if cached: return cached
    lock_key = f"lock:{key}"
    acquired = await redis.set(lock_key, "1", nx=True, ex=2)  # 2s lock TTL
    if acquired:
        try:
            value = await fetch_fn()
            await redis.setex(key, ttl, value)
            return value
        finally:
            await redis.delete(lock_key)
    else:
        # Wait up to 300ms for the first caller to populate
        for _ in range(30):
            await asyncio.sleep(0.01)
            cached = await redis.get(key)
            if cached: return cached
        # Lock contention timeout — proceed without coalescing
        return await fetch_fn()
```

~30 lines, testable with N=1000 concurrent first-callers (must produce ≤2 upstream calls).

## Test plan (concrete, non-negotiable)

- **Unit (≥25)**: key derivation (all field combinations), TTL math, lock-acquire/release semantics, invalidation-event payloads, fail-open semantics.
- **Integration (≥12)**: middleware + real Redis. Cover Redis unavailability (fall-through), concurrent write/read with invalidation (staleness window bounded), stampede coalescing (≤2 upstream calls for N=1000 first-callers), pricing-LRU-migration parity.
- **E2E load (≥3)**: sustained 5-minute load (hit-rate + latency budget); stampede scenario; chaos Redis-kill.

## Acceptance criteria additions

- Stampede load test: 1000 concurrent first-callers → ≤2 upstream calls.
- p99.9 latency ≤12ms (in addition to p99 ≤5ms).
- Per-class memory ceiling enforced and observable.
- Outcome counter has all five labels (hit, miss, bypass, degraded, stampede_waited).

## What I'd push back on

The refactorer's "inline invalidation, 3 known write routes" is fine *today* but the architect is right that an event bus is the better long-term shape — and the cost of moving to one *later* is higher than building it now if we already accept that we'll have 5+ write routes within 6 months. I'd let the refactorer win on inline for v1 and require a v1.1 ticket to convert.

The architect's "5-component package" is over-engineered for v1, but the underlying concerns (structured keys, invalidation discipline, inspectability) are real. Pick the cheap wins (structured key shape, outcome counters, per-class memory) and defer the expensive ones (event bus, CacheInspector endpoint).

## Cost

Stampede protection: ~30 lines + ~5 test cases = 0.5 day. Per-class memory ceilings: config-level, ~0.5 day. Outcome counter labels + dashboards: ~1 day. Total addition vs refactorer's baseline: ~2 days.

## Position summary

Ship the refactorer's thin middleware *with* stampede protection, per-class memory ceilings, full-label outcome counters, and aggressive Redis client timeout. The architect's structured-key + invalidation-discipline points are correct in posture — adopt the cheap versions (structured key format, mandatory invalidation handlers in PR checklist) and defer the expensive ones (event bus, CacheInspector) with a v1.1 ticket.
