---
topic: "add rate limiting to public API endpoints"
domain: code
strategy: systematic
depth: quick
proposals_target: 2
handoff_target: none
created: 2026-05-25T00:00:00Z
---

# Seed Brief: add-rate-limiting-public-api

## Socratic Dialogue (Clarify batch, quick depth)

**Q1: What's the entry point — a specific file/function, or a feature you want to introduce?**
A: A new cross-cutting feature applied at the HTTP layer of all public-facing API endpoints. No single file; a middleware/handler that the router applies uniformly. Internal/service-to-service endpoints are out of scope for v1.

**Q2: What's the scope: single-module change, cross-module refactor, or new subsystem?**
A: New subsystem (rate-limit policy + storage + middleware + admin/observability hooks). Touches the HTTP router, a new policy module, a new storage backend (Redis or in-memory), and metrics/log emitters. No data model changes required for first-party resources.

**Q3: What's the failure mode you're trying to prevent / behavior you're trying to add?**
A: Prevent abusive clients from exhausting capacity (cost protection + neighbor protection). Add: per-IP and per-API-key request quotas, with 429 + Retry-After responses and structured metrics so on-call can attribute traffic. Secondary: detect and shed obvious bot/credential-stuffing patterns.

**Q4: Any non-negotiable constraints from existing code (API stability, backward compat, performance SLO)?**
A: Must not regress p99 latency by more than ~2ms at the middleware layer. Must be drop-in for the existing router (no breaking handler signatures). Must work in dev with no external dependency (in-memory fallback). Must emit existing structured-log schema (no parallel log formats).

**Q5: What does "done" look like — a passing test? a deployed feature? a code review?**
A: Done = (a) feature flag-gated middleware deployed to staging with metrics dashboard, (b) test suite covers: under-limit pass, over-limit 429, Retry-After header correctness, key-vs-IP precedence, storage backend swap; (c) runbook entry for emergency disable; (d) one canary endpoint flips to enforced mode in production.

## Problem Statement

Public API endpoints currently have no per-caller rate limiting, exposing the service to cost-driven abuse, accidental client retry storms, and noisy-neighbor capacity exhaustion. We need a uniform, observable, low-overhead rate-limiting layer applied at the HTTP middleware boundary, with per-IP and per-API-key policies, structured 429 responses, and an emergency disable path.

## Known Context

- Service uses an HTTP router with existing middleware chain (auth, logging, tracing already wired in).
- No existing rate-limit code paths or policy abstractions in the repo (verified via codebase scan — see Enrichment Context below).
- Redis is already a runtime dependency for session/cache work; suitable as default counter backend.
- Structured logging + metrics emission (Prometheus-style) are conventions across handlers.
- Auth middleware already attaches `api_key_id` and resolves client IP from `X-Forwarded-For` chain.

## Constraints

- p99 middleware overhead ≤ 2ms.
- No breaking changes to handler signatures or router setup API.
- Must operate without Redis (in-memory fallback) in dev/test.
- Must respect existing logging schema and Prometheus metric naming conventions.
- Feature-flag gated for staged rollout (off → shadow-count → enforce).
- 429 responses must include `Retry-After` per RFC 6585.

## Success Criteria

- Per-IP and per-API-key quotas enforced at HTTP boundary with token-bucket or fixed-window semantics.
- 429 response with `Retry-After` header observable in integration tests.
- Metrics exposed: `rate_limit_allowed_total`, `rate_limit_denied_total`, `rate_limit_storage_errors_total` (labels: policy, scope).
- Test coverage: unit (policy decisions), integration (middleware + storage), e2e (one canary endpoint).
- Runbook entry for emergency global-disable via feature flag.
- One production endpoint enforcing limits behind canary flag with zero p99 regression.

## Open Questions

- Token-bucket vs fixed-window vs sliding-log: which algorithm best matches our traffic shape and storage cost?
- Where does policy live — config file, env-var defaults, or admin API for runtime adjustment?
- Per-API-key quotas: do we honor a per-customer tier (free/paid/enterprise) at v1 or punt to v2?
- Storage failure mode: fail-open (allow request) or fail-closed (return 503)? What's the on-call expectation?
- IP extraction trust boundary: how do we authoritatively resolve client IP behind multiple proxy hops without spoofing risk?
- (From enrichment) Public API surface does not exist in this repo today — is this targeting a future surface in this repo, or a sibling consumer service? Where would the middleware module live?

## Enrichment Context

**Source**: codebase scan (quality_tier: `fallback_2` — native Glob/Grep). Full report: `enrichment/codebase-context.md`.

- **No existing rate-limit code** in `src/`. All `.md` matches are docs unrelated to this repo's implementation. Greenfield feature here.
- **No HTTP server present**: `src/superclaude/cli/` is a Click-based CLI (audit, eval, pipeline, prd, roadmap, sprint). No FastAPI/Flask. The "public API endpoints" referenced in the topic do not exist in this codebase today — treat as forward-looking design or as targeting a different service. Surfaced as an Open Question above.
- **Adjacent infra**: `audit/profiler.py` already implements budget/token accounting patterns that could inform a rate-limit budget abstraction. Test layout is per-subsystem (`tests/<subsystem>/`).
- **Implication for proposals**: design space is unusually open (no align-with-existing constraints); proposals should explicitly state where the new module lives and what new runtime dependencies (Redis) they introduce.
