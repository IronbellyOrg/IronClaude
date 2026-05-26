---
agent: sonnet:refactorer
proposal_id: 2
persona: refactorer
model: sonnet
domain: code
depth: quick
---

# Proposal 2 — Refactorer Stance: Smallest Viable Middleware, Earn Complexity

## Stance Summary

Ship the smallest middleware that passes acceptance, in a single module, with one algorithm and one backend, and earn additional complexity only when a real second use-case (or a real bug) demands it. Premature abstraction is the dominant failure mode of "policy framework"-style rate limiters — they accumulate config surface area faster than features and leave the team owning a half-built DSL.

## Minimal Architecture

### Single Module: `src/superclaude/middleware/rate_limit.py`

One file. Three things in it:

1. A small `Limiter` class wrapping a backend. One method: `check(key: str, limit: int, window_seconds: int) -> tuple[bool, int]` returning `(allowed, retry_after_seconds)`.
2. An async middleware function `rate_limit_middleware(request, call_next)` that extracts the scope key (api_key if authed, else IP), looks up the per-endpoint limit from a dict in config, calls `Limiter.check`, emits two metrics counters, and either returns 429 with `Retry-After` or calls through.
3. A backend pair: `RedisLimiter` (default) and `InMemoryLimiter` (dev/test). Both implement the same two methods. Chosen at startup based on a single env var.

### Algorithm: Fixed Window

Counter per `(scope_key, endpoint, window_start_epoch)` with TTL = window. One Redis `INCR` + one `EXPIRE` on miss. Done. Burst tolerance handled by tuning window size; if a customer reports "spike at window boundary," we revisit.

Rationale: token-bucket and sliding-window are real algorithms with real merit, but the v1 question is "do we have any rate limiting at all?" — not "do we have the optimal one?" Fixed window is the cheapest to reason about, the cheapest to debug, and the cheapest to back out of.

### Config Surface

```yaml
rate_limit:
  enabled: true
  default: { limit: 1000, window_seconds: 60 }
  endpoints:
    "POST /api/v1/expensive": { limit: 10, window_seconds: 60 }
```

One config block. No algorithm selection knob (we have one algorithm). No per-tier override (deferred). No hot-reload (process restart is acceptable for v1; rate limit config changes are not p0 emergencies — feature flag IS).

### Feature Flag

Single boolean `RATE_LIMIT_ENABLED`. Off = middleware returns instantly. On = enforce. Shadow mode is a luxury we add ONLY if telemetry from staging shows uncertainty about limits — and at that point it's a 30-line diff.

## Migration / Rollout

1. Land middleware behind `RATE_LIMIT_ENABLED=false`.
2. Enable in staging, observe metrics for 1 week.
3. Enable on ONE canary endpoint in production with a conservative limit (10x historical p95).
4. Expand endpoint-by-endpoint over 2-3 weeks.

No new package, no new config system, no new abstractions. ~200 lines of code total.

## Acceptance Criteria

- All seed-brief success criteria met (429 + Retry-After, metrics, test coverage, runbook).
- Middleware overhead ≤ 2ms p99 (single Redis round-trip; achievable).
- Code review fits on one screen per file.
- Zero new top-level packages.

## What I'm Deliberately NOT Building

- Pluggable algorithm framework. (Add when we need the second algorithm.)
- Pluggable backend protocol. (Two concrete classes with shared interface; convert to protocol the day we add a third.)
- Hot-reload. (YAGNI for v1.)
- Per-customer-tier policy. (Out of scope; the architect's `PolicyRegistry` agrees on this.)
- Shadow mode as a first-class state. (Single-bool flag covers off/on; shadow is a debugging tactic, not a feature.)

## Risks

- "We'll regret not making it pluggable" — possible, but pluggable scaffolding without a second consumer is dead weight. Refactor when the second consumer arrives; the diff will be smaller than building speculative seams now.
- Fixed window has boundary-spike behavior. Mitigation: pick window=60s so any burst is at most 2x for ~1s; document it; revisit if monitoring shows it matters.
