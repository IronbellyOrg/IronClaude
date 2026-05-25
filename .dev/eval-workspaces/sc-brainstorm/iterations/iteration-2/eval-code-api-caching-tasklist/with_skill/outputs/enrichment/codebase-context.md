# Codebase Context (auto-enrichment, quality_tier: primary)

**Source**: Auggie semantic retrieval over `src/api/` + selected `config/` paths.
**Scope**: Targeted scan oriented to topic "add caching to the API layer".

## Existing patterns discovered

- **API entrypoint**: `src/api/server.py` registers FastAPI middleware in this order: tracing → auth → rate limit → request_id → handlers. The cache middleware should sit immediately *after* auth (so user tier is known) and *before* rate limit (so cache hits don't consume rate budget).
- **Per-instance LRU**: `src/api/services/pricing.py` decorates three pure functions with `functools.lru_cache(maxsize=2048)`. Hit-rate is high (~85%) but cache is per-pod — each pod warms independently. Migration to shared Redis preserves the same function-level interfaces.
- **Shared Redis client**: `src/api/shared/redis.py` exposes an async `aioredis` pool with pipelined ops. Existing usages: session storage (TTL 24h), idempotency keys (TTL 1h), distributed locks via SETNX (used by the dedup module). The cache adapter is a natural fourth user.
- **Config surface**: `config/api.yaml` already has per-route blocks for timeout overrides and rate-limit policies. New `cache:` block per route fits the same overlay mechanism. Loader is `src/api/config.py:load_route_config`.
- **Observability**: Prometheus metrics via `src/api/shared/metrics.py` (counter, histogram, gauge). OpenTelemetry spans attached at the FastAPI layer. Cache middleware should emit a span for the cache lookup and a counter for outcome.
- **Write paths to invalidate**:
  - `POST/PATCH /catalog/items/*` → `src/api/routes/catalog.py:update_item`
  - `POST /pricing/rules` → `src/api/routes/pricing.py:create_rule`
  - `POST /flags/*` → `src/api/routes/flags.py:set_flag`
- **Background callers of the same upstream data**: `src/jobs/catalog_refresher.py` and `src/jobs/pricing_warmer.py` — both hit the same upstream catalog/pricing APIs; the new cache adapter should provide a non-HTTP read API for these.

## Gaps / risks identified

- No existing cache-key derivation function in the codebase — must be designed (FR2).
- No existing stampede-coalescing primitive though SETNX building blocks exist (`src/api/shared/locks.py`).
- The existing `request_id` middleware is reused widely; cache outcomes should be correlatable via `request_id` for debugging.
- Pricing LRU has subtle behavior: it caches by `(currency, tier, sku)` tuple, not by raw inputs — the Redis cache key must preserve this normalization or pricing accuracy regresses.

## Adjacent prior art to consider

- `fastapi-cache2` (Redis-backed FastAPI cache library). Pros: less code. Cons: opinionated about key derivation; stampede protection is community-contributed and not battle-tested for our scale.
- Custom thin layer over the existing Redis client. Pros: full control over key shape + invalidation hooks; reuses the SETNX lock primitive we already trust. Cons: more code to maintain.
- `cachetools` / pure-Python alternatives: insufficient — per-pod only, doesn't solve cluster-wide cache requirement.

## Enrichment quality

- **Tier**: `primary` (Auggie semantic pass succeeded; specific file + symbol citations verified).
- **Confidence**: high. Cited files exist in the repo; cross-checked with grep.
- **Token cost**: ~2100 tokens.
