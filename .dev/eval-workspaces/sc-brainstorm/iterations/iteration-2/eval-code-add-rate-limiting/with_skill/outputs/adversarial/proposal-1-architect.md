---
proposal_id: 1
persona: architect
model: opus
lens: long-term system fit, extensibility, future-proofing
---

# Proposal 1 — Architect: Build a Rate-Limit Subsystem, Not a Middleware

## Position

The right unit of work here is a **rate-limit subsystem**, not a single middleware. Treating this as "drop in fastapi-limiter and ship" optimizes for now and trades away every adjacent need: tiered plans, observability hooks, future cross-region replication, the inevitable "give me a self-service usage endpoint" ticket, and the equally inevitable "we need a different algorithm for the streaming endpoint" request. Build the subsystem with seams in the right places, and the middleware becomes a thin shell that calls into it.

## Architecture

Five components, all under `src/api/gateway/ratelimit/`:

1. **`RateLimitPolicy`** — declarative config object: `{principal_match, endpoint_match, algorithm, limit, window, burst}`. Loaded from `config/gateway.yaml` with hot-reload via SIGHUP.
2. **`AlgorithmRegistry`** — pluggable algorithm interface (`evaluate(key, now) → Decision`). Ship two implementations day one: `SlidingWindowCounter` (the default, Redis-Lua-backed for atomicity) and `TokenBucket` (for endpoints with bursty-but-bounded traffic, like webhook delivery).
3. **`CounterStore`** — adapter over `src/api/shared/redis.py` exposing `incr_window`, `peek_window`, `reset`. Hides Redis from the algorithm code so we can swap to a different backing store (Memcached, in-process LRU for dev) without touching algorithms.
4. **`Decision`** — value object: `{allowed: bool, limit, remaining, reset_at, retry_after, plan_tier, reason_code}`. This is what flows back through the middleware to the response builder.
5. **`RateLimitMiddleware`** — 30-line FastAPI middleware. Resolves principal (already done by upstream auth middleware), picks policy, evaluates, sets headers, optionally short-circuits with 429.

## Why this shape

**Extensibility is not speculative; the requirements already imply it.** The seed brief surfaces tiered plans, anonymous IP fallback, bypass for internal traffic, per-endpoint overrides, and an open question about a self-service usage endpoint. Each of those is a feature *on the subsystem*, not a feature *on a monolithic middleware*. The `Decision` object exists so the future usage endpoint can read it cheaply; the `AlgorithmRegistry` exists so the webhook team isn't blocked when they ask for a different algorithm; the `CounterStore` abstraction lets us run a dev profile without Redis, which removes friction from local tests.

**Pluggable algorithms day one — not later.** This is the riskiest assumption to bake in: that one algorithm fits all endpoints. Webhook receivers (long-running, low-frequency) want different behavior than CRUD endpoints (short, frequent). Building the registry now costs ~1 day of engineering and avoids a v2 migration.

## Client-facing contract (explicit)

Standard headers on every gateway response, allowed or denied:
- `X-RateLimit-Limit: <int>` — the policy ceiling for this window
- `X-RateLimit-Remaining: <int>` — capacity left in this window
- `X-RateLimit-Reset: <unix-seconds>` — when capacity replenishes
- `X-RateLimit-Policy: "<algo>;w=<seconds>"` — RFC 9331 draft-style hint
- On 429 only: `Retry-After: <seconds>` and a structured JSON body `{error: "rate_limited", reason_code, plan_tier, reset_at, retry_after}`

Document these in the public API reference and the security review packet — this is what the enterprise customer needs to see.

## Tiered limits + extensibility for billing

Plan tier flows from auth middleware → `PolicyResolver` → `RateLimitPolicy`. Storing tier *on the policy resolution path* (not hardcoded in the limiter) means the future "introduce a new tier" or "give this one customer a custom limit" lands as a config change, not a code change. This is exactly what enterprise procurement teams will demand within 6 months.

## Threat-model breadth

The principal-keyed limit handles the obvious abuser, but it does not handle distributed abuse (botnets, credential stuffing across many keys). The subsystem should be designed so that **secondary keys** (IP, ASN, fingerprint) can be added as additional policy axes later — the `Decision` object's `key` field is composite for this reason. Don't ship the secondary axis yet; ship the seam.

## Cost

Higher than the minimum-viable path. ~5-7 engineering days vs ~2 for the "drop in a library" approach. The return is that the next 6 months of foreseeable requirements land as ~1-day config or config+policy diffs instead of ~1-week refactors.

## What I'd push back on

Anyone who proposes shipping with a single hardcoded algorithm to "keep it simple" is optimizing for the first week and ignoring the next 6 months. The simplest version that meets the explicit acceptance criteria is not the simplest version that meets the *real* requirement, which includes everything the dialogue flagged as an open question.
