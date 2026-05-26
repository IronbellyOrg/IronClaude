---
proposal_id: 2
persona: refactorer
model: sonnet
lens: minimum-viable, paying off existing debt, smallest blast radius
---

# Proposal 2 — Refactorer: Adopt `fastapi-limiter`, Wrap It Thinly, Ship in a Week

## Position

The architect's "subsystem with seams" answer is what you build when you don't trust yourself to ship a v2. Trust the team. The seed brief lists one concrete forcing function (enterprise contract evidence) and two production incidents — both addressable by **the smallest thing that actually enforces a limit**. Everything else (algorithm pluggability, secondary keys, hot reload via SIGHUP) is speculative work justified by hypothetical future requirements. Build the minimum, run it in canary, learn what's actually wrong, then refactor *on real evidence*.

## What to build

A single module: `src/api/gateway/middleware/rate_limit.py`. ~150 lines including tests.

1. **Adopt `fastapi-limiter`** (Redis-backed, ~1.5K stars, BSD-3, active maintenance). It provides sliding-window via Redis Lua scripts, integrates as FastAPI middleware, and supports per-route dependency injection.
2. **Wrap it** with a 30-line shim that:
   - Reads plan tier from the request (auth middleware will set it on `request.state.plan_tier`).
   - Looks up the limit from a small dict: `{free: (60, 60), pro: (600, 60), enterprise: (6000, 60), anonymous: (30, 60)}` — `(limit, window_seconds)`.
   - Calls `fastapi-limiter` with the resolved limit + a key built from `(plan_tier, principal_id_or_ip)`.
   - On 429, emits the standard `X-RateLimit-*` headers + a JSON body. (The library doesn't do header shaping the way we want; the shim handles it.)
3. **Config**: limits live in `config/gateway.yaml` under a single `rate_limits:` key. No hot reload — config is read at boot. If we need hot reload later, that's a v2 problem; in practice, ops will push a new config and roll the pods, which already takes ~3 minutes.
4. **Bypass**: signed bypass header check — 5 lines, before the limiter check.

## Why this shape

**The blast radius of new code is the dominant risk.** Every new file is a place for a bug. Every new abstraction is a place for the next engineer to misunderstand the seam and break a different thing. A 150-line module sitting downstream of a battle-tested library is auditable in one PR; a 5-component subsystem is auditable in five.

**The architect's "pluggable algorithm" seam is unjustified.** Webhook receivers being long-running is a real concern, but the fix is not "build an algorithm registry"; the fix is to **exempt webhook endpoints from rate limiting entirely** via the per-endpoint kill switch we already need for safety. One config key, zero algorithm work. If we discover in 3 months that we actually do need a token bucket for some endpoint, we add it then, with the benefit of real data on what shape the algorithm needs to take.

**The architect's "future self-service usage endpoint" is hypothetical.** If a customer asks for it, the answer is `GET /v1/me/rate-limit-status` which calls the same library function the limiter uses. ~20 lines added later. No need for a `Decision` object now.

## Client-facing contract

Same standard headers the architect proposes — that's table stakes, not a differentiator:
- `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` on every response.
- `Retry-After` + structured JSON body on 429.

These ship as part of the 30-line shim. Total cost: ~30 lines.

## Tier handling

The plan tier dict lives in code, not config, for v1. **This is a deliberate choice**: tiers change on a quarterly basis (when product changes pricing), not weekly. A code change with a tested deploy is safer than a config change that nobody reviews. When the tiers do change, the diff is one line.

## Threat model — be honest about scope

The brief asks about botnet defense. **Out of scope.** Botnet defense is a different product (WAF, bot management) and conflating it with API rate limiting will produce a worse version of both. State this explicitly in the security review packet so the customer knows where the line is.

## Cost

~2 engineering days including tests and the runbook. Ships well inside the Q3 deadline with weeks to spare for the canary.

## What I'd push back on

The architect is solving for a future I can't predict and probably won't come. The QA reviewer will want more edge cases tested than I've listed — accept that and pad the test surface, but don't let it turn into "build everything before shipping anything". The 150-line module + adopted library + small config is the version that ships, gets feedback, and lets us iterate. The 5-component subsystem is the version that's still being designed when Q3 ends.
