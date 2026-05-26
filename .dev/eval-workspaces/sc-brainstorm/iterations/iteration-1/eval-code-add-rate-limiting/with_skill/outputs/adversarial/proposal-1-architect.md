---
agent: opus:architect
proposal_id: 1
persona: architect
model: opus
domain: code
depth: quick
---

# Proposal 1 — Architect Stance: Policy-First, Pluggable Rate Limiter Subsystem

## Stance Summary

Build rate limiting as a first-class subsystem with a clean policy abstraction, pluggable storage, and explicit extension scaffolding. The cost of doing it cleanly now is small and the cost of retrofitting clean seams later is large — especially once a second consumer (internal-RPC, websocket, billing-gated tier) inevitably arrives.

## Architecture

### Module Layout (new package: `src/superclaude/ratelimit/`)

- `policy.py` — `RateLimitPolicy` dataclass (algorithm, scope, limit, window, burst), `PolicyRegistry` for named policies and per-endpoint overrides.
- `algorithms/` — `token_bucket.py`, `fixed_window.py`, `sliding_window.py`. Each implements a single `decide(key, policy, now) -> Decision` method returning `(allowed, remaining, retry_after_ms)`. Decision is a frozen dataclass for cheap dispatch.
- `storage/` — `backend.py` defines `RateLimitBackend` protocol (`incr_with_ttl`, `get_count`, `reset`). Concrete backends: `redis_backend.py`, `inmemory_backend.py` (dev/test; thread-safe LRU with sweeper). `backend_factory.py` chooses based on env config with explicit fallback rules.
- `middleware.py` — single `RateLimitMiddleware(router_app, registry, backend)` callable. Pulls IP + api_key from request context (already set by auth middleware), composes a `key`, calls `policy.decide`, sets standard headers, emits metrics, and either passes through or returns 429.
- `metrics.py` — Prometheus counters/histograms with stable label set `{policy, scope, decision, backend}`. Histogram for `decide_duration_seconds` (perf SLI).
- `config.py` — Pydantic-validated config from YAML + env override, with hot-reload via SIGHUP for policy changes (storage stays stable).

### Algorithm Choice (v1)

**Token bucket** for default policy. Rationale: smooth handling of bursts (capacity = burst, refill = sustained rate) matches real API traffic shape better than fixed-window; cheaper than sliding-window-log in Redis (one INCR + EXPIRE per request vs. ZADD + ZREMRANGEBYSCORE). Sliding-window-counter ships as the second algorithm for policies that need stricter "no spikes" semantics.

### Storage

**Redis as default, in-memory fallback explicit and supported.** Redis ops use Lua script for atomic check-and-decrement; falls back to MULTI/EXEC pipeline if Lua is disabled (managed Redis quirk). In-memory backend is feature-complete for dev/test and a documented option for single-instance deployments, behind a "single-replica only" warning.

### Feature Flag Rollout

Three states, controlled by a single env var `RATE_LIMIT_MODE`:
1. `off` — middleware mounted but short-circuits before policy lookup (zero hot-path cost).
2. `shadow` — full policy decision, metrics emitted with `decision=would_deny`, but request always passes.
3. `enforce` — return 429 on deny.

Shadow mode is the canary tool: lets us tune limits against real traffic without user-visible impact.

## Acceptance Criteria

- `RateLimitPolicy` definable in YAML; new policy needs zero code change.
- New algorithm pluggable by implementing `Algorithm` protocol (+ test vector contribution).
- New storage backend pluggable by implementing `RateLimitBackend` protocol.
- Middleware p99 overhead ≤ 2ms under load (1000 RPS sustained, redis backend).
- Three feature-flag states observable in metrics dashboard before flip to `enforce`.

## Non-Goals (v1)

- Per-customer-tier billing logic (separate concern; v2 hook via `PolicyRegistry.resolve(api_key) -> Policy`).
- Distributed quota coordination across regions (rely on per-region Redis; cross-region drift is acceptable for v1).

## Risks

- Over-abstraction risk: 3 algorithms day-1 is one too many. Mitigation: ship token-bucket + skeleton for the second; gate sliding-window behind a config flag until needed.
- Redis Lua script management is a real ops surface. Mitigation: keep the script tiny (< 20 lines) and version-tag it; load via SCRIPT LOAD on startup with a fallback path.
