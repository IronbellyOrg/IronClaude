---
spec_type: requirements
domain: code
strategy: systematic
adversarial_status: pass
convergence_score: 0.78
proposal_count: 3
source_seed: ../seed-brief.md
agents: "opus:architect:'prioritize maintainability and extension scaffolding for code domain',sonnet:refactorer:'focus on technical debt, simplification, and minimal-risk transformation paths',haiku:qa:'focus on test surface, edge cases, regression risk, and acceptance criteria'"
---

# Merged Requirements: Public API Rate Limiting

## Problem Statement

The public API gateway (`src/api/gateway/app.py`, ~20 endpoints) has no rate-limiting today. This exposes downstream services to abusive clients (scraping, credential stuffing, runaway scripts) and produces noisy-neighbor effects where one heavy API consumer starves capacity for others. Two production incidents in the last 90 days were traced to misbehaving customer scripts. A recently-onboarded enterprise customer has a contractual requirement for "documented abuse prevention" — security review is blocked without it. The solution must enforce per-principal sliding-window limits with plan-tier differentiation and an anonymous-IP fallback, surface standard client-facing headers, preserve the gateway's 50ms p99 latency SLO (≤2ms middleware overhead), and not disrupt long-running webhook receivers.

## Constraints

- **C1** — p99 latency overhead from the rate-limit middleware ≤ 2ms; p99.9 ≤ 5ms. *(seed brief Q4; firm)*
- **C2** — No changes to 2xx/4xx response body shapes for non-rate-limited requests. *(seed brief Q4)*
- **C3** — Limits and per-endpoint overrides must be runtime-configurable without a code deploy (config-reload acceptable; full code redeploy not). *(seed brief Q4; debate Tension 5)*
- **C4** — Must reuse the existing async Redis pool at `src/api/shared/redis.py`. No new infra dependency. *(seed brief Q6, enrichment)*
- **C5** — Middleware must sit immediately downstream of `src/api/gateway/middleware/auth.py` (principal must be resolved before limit evaluation). *(seed brief Q6, enrichment)*
- **C6** — Must support log-only (shadow) mode AND per-endpoint kill switch for safe rollout. *(seed brief Q10)*
- **C7** — Webhook receiver endpoints under `src/api/gateway/routes/webhooks/` must be exempt from default limits (long-running async handlers). *(seed brief Q4, debate Tension 1)*
- **C8** — Soft deadline: end of Q3. *(seed brief Q9)*

## Functional Requirements

- **FR1** — Enforce per-API-key sliding-window-counter rate limiting with these defaults: `free=60 req/min`, `pro=600 req/min`, `enterprise=6000 req/min`. *(seed brief Q7)*
- **FR2** — Apply an anonymous-IP fallback at `30 req/min` when no API key is present. IP resolution **MUST** come from the trusted upstream proxy chain only; raw `X-Forwarded-For` from client traffic is ignored. *(seed brief Q7; debate Tension 3 / QA failure mode 6)*
- **FR3** — Internal service-to-service traffic bypasses the limiter when a signed bypass header is present and verifies. Bypass-key rotation must accept both old and new keys during a rotation window. Unknown bypass keys are rejected and audited. *(seed brief Q7; debate Tension 3 / QA failure mode 4)*
- **FR4** — Emit the following headers on **every** gateway response (allowed or denied): `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (Unix seconds), `X-RateLimit-Policy` (e.g. `"sliding-window;w=60"`). On 429, additionally emit `Retry-After`. *(debate Tension 3; addresses iter-1 grader gap on client headers)*
- **FR5** — On 429, return a machine-parseable JSON body: `{error: "rate_limited", reason_code, plan_tier, reset_at, retry_after}`. *(seed brief success criteria; debate consensus)*
- **FR6** — Configuration surface: tier *definitions* live in code (`src/api/gateway/ratelimit/tiers.py`); per-tier *limits* and per-endpoint *overrides* live in `config/gateway.yaml`. Boot-time config read is required; hot-reload via SIGHUP is deferred to v1.1. *(debate Tension 5)*
- **FR7** — Per-endpoint policy controls (in `config/gateway.yaml`): `enabled` (default true), `log_only` (default false), `fail_mode: open|closed` (default `closed` for write endpoints, `open` for read endpoints), `algorithm` (default `sliding-window`; reserved for future). *(debate Tension 3, C6)*
- **FR8** — Telemetry: emit `rate_limit_decision_total{endpoint, plan_tier, outcome}` Prometheus counter and `rate_limit_evaluation_duration_seconds{endpoint}` histogram via `src/api/shared/metrics.py`. *(debate Tension 3 / QA failure mode 8; enrichment)*

## Non-Functional Requirements

- **NFR1** — Middleware overhead: p99 ≤ 2ms, p99.9 ≤ 5ms, measured during canary on production traffic shape. *(C1)*
- **NFR2** — Counter accuracy: no client exceeds 1.0× its plan limit averaged over any rolling 60-second slice, including across window boundaries. False-positive rate (legitimate request blocked) < 0.1% under synthetic load. *(seed brief success criteria; debate Tension 3 / QA failure mode 3)*
- **NFR3** — `X-RateLimit-Reset` consistency: across all gateway replicas, the reported reset timestamp for the same `(principal, endpoint, window)` must agree within 1 second. *(debate Tension 3 / QA failure mode 2)*
- **NFR4** — 429 backpressure: at sustained 1000 req/s rejection rate from a single principal, gateway CPU stays under 80% per replica. *(debate Tension 3 / QA failure mode 7)*
- **NFR5** — Documentation: public API reference is updated with the rate-limit headers, the 429 JSON schema, and the per-tier defaults. A "documented abuse prevention" packet (≤4 pages) is produced for the enterprise security review. *(seed brief Q9)*

## Acceptance Criteria

- **AC1** — Unit test suite: ≥30 cases covering window math (including the window-boundary doubling proof at the 59-60s boundary), header generation for each outcome, config parsing including malformed cases, bypass-key rotation handling. All green. *(QA proposal §test plan)*
- **AC2** — Integration test suite: ≥10 cases with real Redis (Testcontainer). Cover Redis-unavailable behavior under each `fail_mode`, plan-tier change mid-request-stream applied at next window boundary, concurrent requests across two replicas hitting the same window. All green. *(QA proposal §test plan)*
- **AC3** — E2E load tests: 3 scenarios — (i) sustained 2× free-tier rate from one principal for 5 minutes, observed enforcement within ±2% of limit; (ii) burst at window-boundary from 100 principals, no client exceeds limit over any rolling 60s; (iii) webhook-exempt endpoint under load, zero false-429s. *(QA proposal §test plan)*
- **AC4** — Chaos: kill Redis mid-test → per-endpoint `fail_mode` policy is honored (verified). Bypass-key rotation during sustained internal load → zero false-rejects. *(QA proposal §test plan)*
- **AC5** — Canary: 1-week deploy at 5% traffic with `log_only: false` shows no SLO regression (NFR1) and zero customer-filed false-block tickets routed to support. *(seed brief success criteria)*
- **AC6** — Runbook published at `docs/runbooks/rate-limiting.md` covering: "customer says they were rate-limited and shouldn't have been" debug procedure with concrete metric/log queries; "Redis degraded" failover procedure; "emergency bypass for a single customer" procedure. On-call training completed. *(QA proposal §acceptance; seed brief Q5)*

## Risks

- **R1** (severity: HIGH) — **Latency budget overrun.** Sliding-window math + Redis round-trip risks blowing the 2ms p99 target on hot endpoints. *Mitigation*: measure in canary on a representative endpoint *before* full rollout; if exceeded, fall back to per-replica local approximation + periodic Redis sync (acceptable accuracy degradation documented in the ADR).
- **R2** (severity: HIGH) — **Fail-mode misconfiguration.** A read endpoint mistakenly set to `fail_mode: closed` could 429 all traffic during a Redis blip. *Mitigation*: per-endpoint policy is reviewed at PR time; integration test asserts default `fail_mode` matches a curated list; canary monitors `rate_limit_decision_total{outcome="fail_closed_redis_error"}` and pages on threshold.
- **R3** (severity: MEDIUM) — **Plan-tier lookup hot path cost.** Auth middleware currently returns only `principal_id`; resolving `plan_tier` adds either a DB read or a cache lookup on every request. *Mitigation*: extend the auth middleware's existing principal cache to include `plan_tier`; treat tier as part of the auth result rather than a separate lookup. ~1 day extra in auth middleware.
- **R4** (severity: MEDIUM) — **Bypass-key compromise.** If the signed bypass key leaks, an attacker bypasses all limits. *Mitigation*: short-lived keys (24h) with rotation tooling; failed-verification audit log; alert on a single source IP attempting many bypass-failed requests.
- **R5** (severity: LOW) — **Distributed/botnet abuse not addressed.** A determined attacker can rotate across many free-tier keys or anonymous IPs. *Mitigation*: explicitly documented as out of scope for this work, deferred to a future WAF/bot-management product evaluation (see Open Questions).

## Open Questions

- **OQ1** — Burst allowance shape. Default: 1.5× tier limit over a 10-second window, per-tier configurable. To be ratified by product/customer-success before launch.
- **OQ2** — Distributed/botnet abuse: when (not if) we see it, do we extend this subsystem with secondary keys (IP/ASN/fingerprint), or invest in a separate WAF/bot product? Decision deferred; the principal key field is structured to allow future composition.
- **OQ3** — Self-service "current rate-limit usage" endpoint for tenants. Likely a v1.1 add (~20 lines reusing the same Redis lookup) once we have customer signal on demand.

## Out of Scope (explicit)

- Botnet / distributed abuse defense.
- WAF-style payload inspection.
- Quota / monthly billing limits (this is *rate* limiting, not *quota* — different problem, different system).
- Cross-region replication of counters (single-region Redis; cross-region pods accept the eventual-consistency window).

## Provenance

| Requirement | Origin |
|---|---|
| FR1 (tiered per-key limits) | Seed brief Q7 (Validate batch); ratified by all 3 proposals |
| FR2 (anonymous IP + trusted proxy) | Seed brief Q7; QA proposal failure mode 6 (X-Forwarded-For spoofing) |
| FR3 (bypass + rotation) | Seed brief Q7; QA proposal failure mode 4 (rotation correctness) |
| FR4 (client-facing headers) | Architect proposal §Client-facing contract; refactorer agreed; addresses iter-1 grader gap |
| FR5 (429 JSON body) | Seed brief success criteria; consensus across all 3 proposals |
| FR6 (config split: code + YAML) | Debate Tension 5 — compromise between architect (full YAML) and refactorer (code) |
| FR7 (per-endpoint policy) | QA proposal failure mode 1 (Redis unavailability); architect concession in debate Tension 3 |
| FR8 (telemetry) | QA proposal failure mode 8; architect proposal §Architecture; refactorer agreed |
| NFR1 (latency) | Seed brief Q4 (firm constraint) |
| NFR2 (window-boundary accuracy) | QA proposal failure mode 3 (window-boundary doubling) |
| NFR3 (reset consistency) | QA proposal failure mode 2 (clock skew across replicas) |
| NFR4 (rejection backpressure) | QA proposal failure mode 7 |
| AC1-AC4 (tests + chaos) | QA proposal §test plan, adopted wholesale per debate Tension 3 resolution |
| AC5 (canary) | Seed brief Q5, success criteria |
| AC6 (runbook + training) | QA proposal §acceptance + seed brief Q5 |
| R1 (latency overrun) | Architect proposal §Cost; QA tests force early detection |
| R2 (fail-mode misconfig) | QA proposal failure mode 1 escalation |
| R3 (tier-lookup cost) | Enrichment finding (auth middleware returns only principal_id) |
| R4 (bypass compromise) | QA proposal failure mode 4 |
| R5 + Out-of-scope botnet | Debate Tension 4 — refactorer + QA vs architect, refactorer/QA won |
| OQ1 (burst shape) | Seed brief open question carried forward; no proposal had definitive answer |
| OQ2 (secondary keys) | Architect proposal §Threat-model breadth, deferred per debate Tension 4 |
| OQ3 (usage endpoint) | Architect proposal §Architecture; refactorer's "add when asked" position adopted |
