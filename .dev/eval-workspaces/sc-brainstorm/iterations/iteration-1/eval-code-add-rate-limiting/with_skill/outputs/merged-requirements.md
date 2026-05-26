---
spec_type: requirements
domain: code
adversarial_status: pass
convergence_score: 0.78
source_proposals: 2
debate_transcript: adversarial/debate-transcript.md
created: 2026-05-25T00:00:00Z
---

# Merged Requirements — Rate Limiting for Public API Endpoints

## Problem Statement

Public API endpoints currently have no per-caller rate limiting, exposing the service to cost-driven abuse, accidental client retry storms, and noisy-neighbor capacity exhaustion. We need a uniform, observable, low-overhead rate-limiting layer applied at the HTTP middleware boundary, with per-IP and per-API-key policies, structured 429 responses, and a safe canary rollout path that allows tuning against real production traffic before enforcement.

## Functional Requirements

1. **FR-1 Middleware boundary enforcement** — A single HTTP middleware applies rate-limit checks before request reaches handler code. The middleware extracts `api_key` (if authenticated) or client IP (resolved trustfully from the existing proxy chain) as the scope key.
2. **FR-2 Token-bucket algorithm (v1)** — Initial release ships exactly one algorithm: token-bucket with configurable `capacity` (burst) and `refill_rate` (sustained RPS). Algorithm is not pluggable in v1; a protocol/abstraction is added only when a second algorithm is genuinely needed.
3. **FR-3 Per-endpoint policy via config** — Rate-limit policies are declared in YAML under `rate_limit.endpoints` with a `rate_limit.default` fallback. Policy shape: `{capacity, refill_rate_per_sec}`. No code change required to introduce a new policy.
4. **FR-4 Three-state feature flag** — `RATE_LIMIT_MODE` env var with values `off`, `shadow`, `enforce`. `off` short-circuits middleware. `shadow` performs full policy decision and emits metrics with `decision=would_deny` but always passes requests. `enforce` returns 429 on deny.
5. **FR-5 429 response contract** — On deny, return HTTP 429 with `Retry-After` header (seconds, RFC 6585) and a JSON body containing `error.code = "rate_limited"`, `error.retry_after_seconds`, and a structured policy identifier (no leaking of internal counter state).
6. **FR-6 Storage backends** — Redis backend (default, production) using a single Lua script for atomic decrement-and-check; in-memory backend (dev/test, single-replica deployments) implementing the same interface. Backend chosen by env config with explicit, documented fallback rules.

## Non-Functional Requirements

1. **NFR-1 Latency budget** — Middleware adds ≤ 2ms p99 overhead under 1000 RPS sustained against Redis backend (measured in load test, not estimated).
2. **NFR-2 Metrics observability** — Emit Prometheus counters `rate_limit_allowed_total`, `rate_limit_denied_total`, `rate_limit_storage_errors_total` and histogram `rate_limit_decide_duration_seconds`, all with stable labels `{policy, scope, decision, backend}`. Metric names and label set are part of the operator contract — breaking changes require a deprecation cycle.
3. **NFR-3 Module layout that admits future growth without speculative scaffolding** — Land code under `src/superclaude/ratelimit/` (new package) but with a single `middleware.py` module at v1. The package boundary is the seam; the file split happens when the second consumer (or second algorithm) lands.
4. **NFR-4 Storage failure behavior** — Storage errors are fail-OPEN by default (request is allowed, `rate_limit_storage_errors_total` increments, structured log emitted). Fail-closed mode available via config flag for security-sensitive endpoints; the choice is explicit and documented in the runbook.

## Acceptance Criteria

1. **AC-1** Integration test: an over-limit request returns HTTP 429 with `Retry-After` header present and ≥ 1 second; the next allowed request occurs at or after the indicated time.
2. **AC-2** Integration test: the same key under `shadow` mode never returns 429, but `rate_limit_denied_total{decision="would_deny"}` increments at the expected rate.
3. **AC-3** Load test: 1000 RPS sustained for 60s against an endpoint with limit configured at 800 RPS shows ~200 RPS deny rate, p99 middleware overhead ≤ 2ms, and Redis CPU < 30% on a single small instance.
4. **AC-4** Runbook entry exists with: (a) emergency disable via env var, (b) procedure to raise a specific endpoint's limit, (c) procedure to swap backend to in-memory in a degraded-Redis incident.
5. **AC-5** One production endpoint runs in `enforce` mode for 7 consecutive days with zero p99 latency regression versus the pre-rollout baseline.

## Open Questions

1. **OQ-1** Public API surface does not exist in this repo today (confirmed via codebase scan). Is this brainstorm targeting (a) a future API layer to be added here, or (b) a sibling consumer service? The answer changes where the middleware lives and who reviews the PR.
2. **OQ-2** Per-customer billing-tier policy (free/paid/enterprise) is explicitly deferred to v2. Confirm with product that v1 single-default-policy-per-endpoint is acceptable.
3. **OQ-3** Trusted-proxy-hop count for X-Forwarded-For parsing: do we have an authoritative list of our edge proxies, or should we read from existing auth-middleware config?

## Risks

- **R-1 Algorithm regret**: Token-bucket may prove inappropriate for some endpoint traffic shapes (e.g., strictly periodic batch jobs). Mitigation: shadow mode tuning before enforce, and the package-level layout lets us add a second algorithm without API churn.
- **R-2 Lua script ops surface**: Managed Redis providers sometimes restrict Lua. Mitigation: keep the script tiny (<20 lines); include a MULTI/EXEC fallback path in v1; load via `SCRIPT LOAD` on startup with a health check.
- **R-3 Fail-open default surprises security review**: Some endpoints (e.g., auth/login) need fail-closed. Mitigation: per-endpoint config override, documented runbook decision tree, and a security-review checkpoint before any endpoint flips to enforce.
- **R-4 Greenfield risk**: No existing rate-limit code in the repo means no implicit alignment constraints — but also no existing test harness for this concern. Mitigation: invest in the `tests/ratelimit/` package early (load test fixture, Redis-in-Docker for integration).
