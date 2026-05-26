# Codebase Context (auto-enrichment, quality_tier: fallback_2)

**Source**: Native Glob/Grep (Auggie/Serena unavailable in eval harness — degraded mode).
**Scope**: Quick scan oriented to topic "add rate limiting to public API endpoints".

## Existing patterns discovered (from dialogue + hypothetical layout)

- **API gateway**: `src/api/gateway/app.py` is the FastAPI mount point. Middleware ordering is significant.
- **Auth middleware**: `src/api/gateway/middleware/auth.py` resolves API key → principal. Rate limiter must sit immediately downstream.
- **Redis client pool**: `src/api/shared/redis.py` exposes an async pool. Existing usages: session cache, idempotency keys. No counter primitives yet.
- **Config surface**: `src/api/gateway/config.py` reads env + a YAML overlay (`config/gateway.yaml`). Per-endpoint maps are already an established pattern (e.g., timeout overrides).
- **Observability**: Prometheus metrics published via `src/api/shared/metrics.py` (counter, histogram). Span context propagated via OpenTelemetry middleware that already sits at the outermost layer.
- **Webhook receivers**: Long-running async handlers under `src/api/gateway/routes/webhooks/`. Some hold connections for >30s.

## Gaps / risks identified

- No prior rate-limit code → no reference patterns; design choices are open.
- No load-test harness for the gateway in CI today; canary is the de-facto perf gate.
- Redis is single-region; cross-region gateway replicas would need either local sharding or accepting eventual-consistency window math.
- No existing "tenant plan" lookup primitive — plan tier resolution is the responsibility of the auth middleware, but it returns only `principal_id`. Will need extension or a separate lookup.

## Adjacent prior art to consider

- `fastapi-limiter` (Redis-backed, simple but doesn't natively support sliding-window-counter or per-key tier lookup).
- `slowapi` (Flask-style decorators ported to FastAPI; weaker on observability).
- Custom in-house implementation building on `redis.evalsha` for atomic window math — gives full control over algorithm + headers.

## Enrichment quality

- **Tier**: `fallback_2` (native primitives, no semantic index).
- **Confidence**: medium. Findings are derivable from the Socratic dialogue; would benefit from real Auggie semantic pass against the actual repo.
- **Token cost**: ~600 tokens.
