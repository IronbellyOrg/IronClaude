---
id: "AUTH-ROADMAP-V1-MERGED"
title: "User Authentication Service - Roadmap (Adversarially Merged)"
source: "merged-prd-tdd-user-auth.md"
target_release: "v1.0 (2026-06-09)"
variant: "merged: opus:architect (base) + sonnet:analyzer (format tables) + R2.5 probe additions"
pipeline: "/sc:adversarial --depth standard"
convergence: 0.806
status: "partial (7 HIGH UNADDRESSED invariants addressed via Changes #8-#14)"
---

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (opus:architect) -->
<!-- Incorporations from: Variant 2 (sonnet:analyzer) -->
<!-- R2.5 invariant probe additions: INV-001, INV-002, INV-004, INV-005, INV-007, INV-011, INV-013 -->
<!-- Merge date: 2026-05-22T17:10:00+00:00 -->

# User Authentication Service — Roadmap

## Executive Summary

<!-- Source: Base (V1 opus:architect, original) -->

The User Authentication Service is the foundational identity substrate on which the platform's entire Q2-Q3 2026 personalization roadmap and SOC2 Type II compliance posture depend. This roadmap sequences the construction of a JWT-based, stateless authentication system organized around `AuthService` as the orchestrating facade, with `TokenManager`, `JwtService`, `PasswordHasher`, and the `UserProfile`/`AuthToken` data models forming the core component graph. The architecture deliberately separates credential validation (bcrypt cost-12 hashing via `PasswordHasher`), token lifecycle management (15-minute access / 7-day refresh via `TokenManager` + Redis), and persistence (`UserProfile` in PostgreSQL 15) so that each cross-cutting concern — security hardening, observability, scalability — can be tested and evolved independently.

From an architectural standpoint, the dominant risk is not any single feature but the *integration surface* between four asynchronous subsystems: PostgreSQL for durable user records, Redis for revocable refresh-token state, the email delivery provider (SendGrid) for password reset, and the RS256-signing key infrastructure for `JwtService`. The roadmap therefore front-loads infrastructure provisioning and contract definition (M1) before any user-visible flow is built, and explicitly carves out a hardening milestone (M4) to absorb the security, observability, and resilience work that always slips when squeezed into feature sprints. The frontend integration (`LoginPage`, `RegisterPage`, `AuthProvider`) is sequenced to begin only once the backend contracts are stable, with `AuthProvider`'s silent-refresh behavior treated as a first-class architectural concern rather than UI polish.

Critically, the v1.0 design must avoid trapping the team into a corner that the explicit non-goals (OAuth, MFA, RBAC) will eventually demand. The `AuthService` interface and `AuthToken` schema are sequenced to ship with extension seams — payload claims, scope fields, role arrays — that allow MFA (v1.1) and OAuth (v2.0) to land as additive changes rather than breaking rewrites. Target GA is 2026-06-09, leaving ~11 weeks from start of M1 to a hardened, audited, observed v1.0.

## Success Metrics

<!-- Source: Variant 2 (sonnet:analyzer), §Success Metrics — merged per Change #1 -->

| Metric | Target | Baseline | Measurement Method | Source |
|--------|--------|----------|--------------------|--------|
| Login response time (p95) | < 200ms | N/A (greenfield) | APM on `AuthService.login()` | NFR-PERF-001 |
| Concurrent login capacity | 500 RPS | N/A | k6 load test | NFR-PERF-002 |
| Service availability | 99.9% / 30d rolling | N/A | Health-check uptime monitor | NFR-REL-001 |
| Token refresh latency (p95) | < 100ms | N/A | APM on `TokenManager.refresh()` | TDD §4.1 |
| Password hash time | < 500ms | N/A | Benchmark `PasswordHasher.hash()` at bcrypt cost 12 | NFR-SEC-001, TDD §4.1 |
| `JwtService` sign/verify | < 5ms | N/A | Unit benchmark | TDD §17 |
| Registration conversion | > 60% | N/A | Funnel landing → confirmed account | PRD §Success Metrics |
| Failed login rate | < 5% of attempts | N/A | Auth event log analysis | PRD §Success Metrics |
| Password reset completion | > 80% | N/A | Funnel: reset requested → new password set | PRD §Success Metrics |
| Avg session duration | > 30 minutes | N/A | Token refresh event analytics | PRD §Success Metrics |
| Unit test coverage | ≥ 80% | 0% | Jest coverage report on `AuthService`/`TokenManager`/`JwtService`/`PasswordHasher` | TDD §15.1, §24.1 |
| DAU (authenticated) | > 1000 within 30d of GA | 0 | `AuthToken` issuance counts | TDD §4.2 |

### Why These Metrics — Strategic Objectives

<!-- Source: Base (V1 opus:architect, modified) — repositioned under Success Metrics table as rationale per Change #1 -->

1. **Ship a SOC2-auditable identity layer by 2026-06-09** — Every authentication event (login, registration, refresh, reset, lockout) is persisted to the audit log with user ID, IP, timestamp, and outcome, with 90-day retention in PostgreSQL and 12-month archive per the PRD compliance table. Measurable outcome: 100% of `AuthService` public methods emit structured audit records validated against SOC2 control mapping in M4.

2. **Meet the p95 < 200ms latency budget under 500-concurrent-request load** — NFR-PERF-001 and NFR-PERF-002 require that `AuthService.login()`, `TokenManager.refresh()`, and `/auth/me` all stay under 200ms at the 95th percentile while sustaining 500 concurrent logins. Measurable outcome: k6 load harness in M3 produces a green report attached to the M4 exit gate.

3. **Eliminate plaintext credential surface area end-to-end** — Passwords pass from `RegisterPage`/`LoginPage` through TLS 1.3 into `PasswordHasher` (bcrypt cost 12) without ever appearing in logs, error messages, exception traces, or APM payloads. Refresh tokens are stored hashed in Redis by `TokenManager`. Measurable outcome: automated log-scrubber test in M4 plus the M5 penetration-test report.

4. **Preserve extensibility for MFA (v1.1) and OAuth (v2.0)** — `AuthService` method signatures, the `AuthToken` payload schema, and the `UserProfile` roles array are designed so that adding a TOTP step or an external identity provider requires only additive changes, not breaking API revisions. Measurable outcome: ADR documenting the MFA and OAuth extension points, signed off by the architect approver in M2.

5. **Deliver a frontend that survives token expiry transparently** — The `AuthProvider` performs silent refresh before access-token expiry, recovers from 401 responses, and degrades gracefully when Redis is unavailable. Measurable outcome: Playwright E2E suite in M3 covers expiry, refresh, and revocation flows with zero user-visible re-login prompts inside the 7-day window.

6. **Establish operational readiness before GA** — Runbooks, dashboards, alerts (login failure rate > 20% over 5min, p95 > 500ms, Redis connection failures), and an on-call rotation are in place at least one week before 2026-06-09. Measurable outcome: M5 operational-readiness review checklist signed by the engineering manager.

## Milestones

<!-- Source: Base (V1 opus:architect, original) -->

| Milestone | Target Date | Scope | Exit Criteria | Architectural Focus |
|-----------|-------------|-------|---------------|---------------------|
| M1: Foundations | 2026-04-03 | Infra provisioning, contracts, ADRs | Postgres+Redis up, OpenAPI schema frozen, key infra in place | Component boundaries, dependency graph |
| M2: Core Auth Backend | 2026-04-24 | `AuthService` + `PasswordHasher` + `JwtService` + register/login | FR-AUTH-001, FR-AUTH-002 green; integration tests pass | Service decomposition, contract stability |
| M3: Token Lifecycle + Frontend | 2026-05-15 | `TokenManager` refresh, `AuthProvider`, `LoginPage`/`RegisterPage` | FR-AUTH-003, FR-AUTH-004 green; silent refresh works end-to-end | Stateless session integrity, UI/state seam |
| M4: Hardening + Reset Flow | 2026-05-29 | FR-AUTH-005, rate limiting, audit logs, observability | NFR-PERF-001/002, NFR-SEC-001/002 verified; SOC2 mapping done | Security, performance, observability |
| M5: GA Readiness | 2026-06-09 | Pen-test remediation, runbooks, dashboards, rollout | All release gates pass; on-call ready; rollback rehearsed | Operational excellence, contingency |

### M1: Foundations — 2026-04-03

<!-- Source: Base (V1 opus:architect, modified) — D1.1 reconciled with pg max-connections per Change #13; D1.7 frontend-team capacity added per Change #8; D1.8 PgBouncer added per Change #13 -->

**Scope**: Stand up infrastructure dependencies, freeze API contracts, ratify architectural decisions, and produce the dependency graph that subsequent milestones execute against. This is a deliberately backend-heavy milestone — no user-facing code ships here.

**Deliverables**:

- **D1.1** — Provision PostgreSQL 15 with a dedicated `auth` schema, including `users` and `audit_log` tables; configure pg-pool connection pooling sized per source spec line 1212 ("200 max" with HPA awareness; scale to 200 only when wait > 50ms), with explicit awareness that horizontal pod replication multiplies clients per pod against this cap (owner: platform team; dependency: infra capacity review). <!-- Source: R2.5 invariant probe INV-011 — modified per Change #13 -->
- **D1.2** — Provision Redis 7 cluster for `TokenManager` refresh-token storage; verify TCP/RESP connectivity from the `AuthService` runtime environment; document failover behavior (owner: platform team; dependency: D1.1 not required, can parallelize).
- **D1.3** — Generate, store, and rotate the 2048-bit RSA key pair used by `JwtService` for RS256 signing; document quarterly rotation procedure (owner: security; dependency: secret-management system).
- **D1.4** — Freeze the OpenAPI 3.1 spec for `/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`, `/auth/reset-request`, `/auth/reset-confirm`, including the standardized error envelope `{ error: { code, message, status } }` (owner: backend lead; dependency: PRD/TDD review).
- **D1.5** — Author ADRs covering: (a) JWT vs. server-side sessions, (b) bcrypt cost-12 vs. argon2id, (c) refresh-token storage in Redis with hashed values, (d) MFA/OAuth extension seams in `AuthService` and `AuthToken`, (e) named SOC2 compliance reviewer for M4 sign-off (per Change #9) (owner: architect; dependency: D1.4). <!-- Source: R2.5 invariant probe INV-002 — modified per Change #9 -->
- **D1.6** — Configure SendGrid (or equivalent) transactional email account with sandbox + production keys for the password-reset flow; verify deliverability to test domains (owner: backend; dependency: PRD constraint — email infra "available before development begins").
- **D1.7** — Frontend-team representative committed to M3 workstream with named POC and capacity allocation by M1 exit; confirms ≥1.0 FTE coverage for D3.4/D3.5/D3.6 across mid-M2 through M3 (owner: engineering manager + frontend-team lead; dependency: organizational confirmation). <!-- Source: R2.5 invariant probe INV-001 — added per Change #8 -->
- **D1.8** — Deploy PgBouncer (or read replica) connection pooler alongside PostgreSQL to absorb horizontal-scaling client multiplication; configure transaction-mode pooling to multiplex auth-service pod connections against the 200-max PG cap; document fallback to per-pod connection limits if PgBouncer config errors emerge (owner: platform team; dependency: D1.1). <!-- Source: R2.5 invariant probe INV-011 — added per Change #13 -->

**Exit Criteria**:

- `psql` and `redis-cli` smoke tests pass from the application runtime.
- OpenAPI spec validates against Spectral lint rules with zero errors.
- Signed ADRs merged to `docs/` and referenced from the TDD.
- RSA key pair accessible via secret manager; key ID published to backend team.
- Frontend-team POC named and committed in writing (D1.7).
- PgBouncer connectivity smoke test passes from auth-service pods (D1.8).

**Architectural Risks**:

- Redis as a hard dependency for refresh-token revocation: if Redis is unavailable, `TokenManager` must reject refresh requests rather than fall back to stateless validation (which would defeat revocation). The TDD already specifies this; M1 ratifies it in the ADR.
- Key rotation strategy for `JwtService` must avoid invalidating in-flight refresh tokens. ADR D1.5 must include a `kid` (key ID) header strategy with overlapping key validity windows.
- PostgreSQL 200-max connection cap is a hard ceiling under horizontal pod scaling; PgBouncer (D1.8) is required infrastructure, not optional. <!-- Source: R2.5 invariant probe INV-011 — added per Change #13 -->

**Dependencies**: Upstream — none (entry milestone). Downstream — every other milestone is blocked on D1.1, D1.2, D1.3, D1.4, and D1.8.

### M2: Core Auth Backend — 2026-04-24

<!-- Source: Base (V1 opus:architect, original) -->

**Scope**: Build the `AuthService` orchestration layer, `PasswordHasher`, `JwtService`, and the `UserProfile`/`AuthToken` data models. Land FR-AUTH-001 (login) and FR-AUTH-002 (registration) end-to-end at the API level. No frontend work yet; backend is consumed via curl/Postman and integration tests only.

**Deliverables**:

- **D2.1** — Implement `AuthService` as the facade pattern, with `login()`, `register()`, `getProfile()` method signatures designed to accept an optional `authContext` parameter (future MFA challenge data, OAuth provider tokens) — extension seam per Objective 4 (owner: backend lead; dependency: D1.4, D1.5).
- **D2.2** — Implement `PasswordHasher` wrapping bcrypt with cost factor 12; expose `hash()` and `verify()` methods; unit-test that the bcrypt cost parameter is asserted (NFR-SEC-001) and that hash time stays under 500ms on the target runtime (owner: backend; dependency: D2.1).
- **D2.3** — Implement `JwtService` signing access tokens with RS256/2048-bit RSA, payload containing `sub` (user id), `roles`, `iat`, `exp`, `kid`; build clock-skew tolerance of 5 seconds into the verification path (TDD §12 edge case); unit-test against NFR-SEC-002 (owner: backend; dependency: D1.3).
- **D2.4** — Implement `UserProfile` repository over PostgreSQL with email normalization to lowercase, unique constraint, UUID v4 primary key, and the field set specified in TDD §7.1; handle concurrent registration via the unique-constraint race (TDD §12) returning 409 (owner: backend; dependency: D1.1).
- **D2.5** — Wire `POST /auth/register` and `POST /auth/login` endpoints behind the API gateway; enforce password policy (≥8 chars, uppercase, number) returning 400 with field-level error codes; ensure invalid credentials return generic 401 (no user enumeration) per FR-AUTH-001 AC 3 (owner: backend; dependency: D2.1, D2.2, D2.3, D2.4).
- **D2.6** — Integration test suite using Supertest + testcontainers covering registration happy path, duplicate-email 409, weak-password 400, valid login 200, invalid login 401, and the concurrent-registration race (owner: QA + backend; dependency: D2.5).

**Exit Criteria**:

- FR-AUTH-001 and FR-AUTH-002 acceptance criteria pass end-to-end against a live PostgreSQL.
- Integration test coverage for `AuthService`, `PasswordHasher`, and `JwtService` ≥ 80% (per TDD §15.1).
- No `password` or `accessToken` string appears in any captured log line during the integration run (automated grep gate).
- Architect-signed ADR review for the MFA/OAuth extension seams (Objective 4).

**Architectural Risks**:

- `PasswordHasher` cost factor 12 may push hash time above the 500ms target on under-provisioned runtimes; M2 must benchmark on production-equivalent hardware, not developer laptops.
- The concurrent-registration race (two requests with the same email arriving milliseconds apart) is mitigated by the database unique constraint, but the error returned must be the same 409 in both ordering cases — verify with explicit integration test.
- Generic 401 for both "unknown email" and "wrong password" is a security requirement, but it must not leak through timing differences. Constant-time comparison and a dummy bcrypt verify for unknown emails are required (TDD §13 implies this; ADR should make it explicit).

**Dependencies**: Upstream — M1 (D1.1, D1.2, D1.3, D1.4, D1.5). Downstream — M3 (token lifecycle), M4 (audit logging hooks).

### M3: Token Lifecycle + Frontend — 2026-05-15

<!-- Source: Base (V1 opus:architect, modified) — D3.2 atomic-rotation test added per Change #11 -->

**Scope**: Implement `TokenManager`'s full refresh-token lifecycle with Redis-backed revocation, build the `AuthProvider` context with silent refresh, and ship `LoginPage`/`RegisterPage` UI. Deliver FR-AUTH-003 (token issuance/refresh) and FR-AUTH-004 (profile retrieval) end-to-end.

**Deliverables**:

- **D3.1** — Implement `TokenManager` with `issue()`, `refresh()`, `revoke()`, `revokeAll()` methods; store refresh tokens as hashed values in Redis with 7-day TTL keyed by `{userId}:{tokenHash}` to support `revokeAll` on password reset (owner: backend; dependency: M2 complete).
- **D3.2** — Implement `POST /auth/refresh` endpoint that validates the refresh token, rotates it (issues a new pair, revokes the old), and returns the new `AuthToken`; handle expired-vs-revoked distinction with separate error codes for observability (owner: backend; dependency: D3.1).
- **D3.3** — Implement `GET /auth/me` returning the authenticated `UserProfile` including `lastLoginAt` updated on successful login; verify the Bearer token via `JwtService` middleware (owner: backend; dependency: M2 + D3.1).
- **D3.4** — Build `AuthProvider` React context: stores `AuthToken` in memory + httpOnly cookie (or secure storage strategy per ADR), schedules silent refresh 60s before access-token expiry, intercepts 401 responses and triggers a single refresh attempt before redirecting to `LoginPage` (owner: frontend; dependency: D3.2, D3.3).
- **D3.5** — Build `LoginPage` (route `/login`) with email + password fields, client-side validation, generic error display on 401, redirect on success via `AuthProvider.onSuccess`; build `RegisterPage` (route `/register`) with email + password + displayName, client-side password-strength check before submission (owner: frontend; dependency: D3.4).
- **D3.6** — Playwright E2E test suite covering: successful login, failed login, successful registration, duplicate-email registration, token refresh during active navigation, refresh-token expiry after simulated 7-day idle, concurrent login from two tabs (TDD §11 user flow) (owner: QA; dependency: D3.5).

**Exit Criteria**:

- FR-AUTH-003 and FR-AUTH-004 acceptance criteria pass end-to-end through the UI.
- Silent refresh demonstrably works: a 30-minute Playwright session shows zero user-visible re-login prompts despite multiple access-token expirations.
- `AuthProvider` correctly handles the Redis-unavailable case by surfacing a clear error rather than serving stale tokens (TDD §12 edge case).
- E2E coverage report attached to the milestone gate.
- **D3.2 atomic rotation verified by integration test simulating concurrent refresh requests; LUA script or MULTI/EXEC transaction confirmed by code review.** <!-- Source: R2.5 invariant probe INV-005 — added per Change #11 -->

**Architectural Risks**:

- `AuthProvider` token storage strategy is contested: in-memory only loses sessions on page refresh; localStorage exposes to XSS; httpOnly cookies require CSRF mitigation. The ADR from M1 (D1.5) must resolve this before M3 starts, or it becomes a critical-path blocker.
- Refresh-token rotation must be atomic in Redis (LUA script or transaction) — a non-atomic rotation creates a window where both old and new tokens are valid, enabling replay if the old token is captured. **This atomicity is now gated by D3.2 integration test (per Change #11).** <!-- Source: R2.5 invariant probe INV-005 — modified per Change #11 -->
- Clock skew between client and server in `AuthProvider`'s silent-refresh scheduling must align with the 5-second tolerance in `JwtService` (D2.3); otherwise users on devices with skewed clocks see spurious 401s.

**Dependencies**: Upstream — M2 (full backend). Downstream — M4 (rate limiting wraps these endpoints, audit logs hook in here).

### M4: Hardening + Reset Flow — 2026-05-29

<!-- Source: Base (V1 opus:architect, modified) — D4.4 dual-counter lockout added per Change #10; D4.5 compliance-reviewer sign-off added per Change #9; pen-test exit gate added per Change #12 -->

**Scope**: Land the password reset flow (FR-AUTH-005), wire in rate limiting, account lockout, comprehensive audit logging, Prometheus metrics, OpenTelemetry tracing, and run load tests to verify the performance NFRs. This is the milestone where cross-cutting concerns become first-class deliverables. **M4 exit additionally gates external penetration testing (D5.1 per Change #12).**

**Deliverables**:

- **D4.1** — Implement `POST /auth/reset-request` and `POST /auth/reset-confirm` endpoints; reset tokens are single-use, 1-hour TTL, stored hashed in Redis; on confirm, `TokenManager.revokeAll()` is invoked for the user so all existing sessions are invalidated per FR-AUTH-005 AC 4 (owner: backend; dependency: M3 complete).
- **D4.2** — Integrate SendGrid for password-reset emails; respond with identical success messaging regardless of whether the email is registered (no enumeration per PRD edge case table) (owner: backend; dependency: D1.6, D4.1).
- **D4.3** — Implement rate limiting at the API Gateway: 10 req/min/IP for `/auth/login`, 5 req/min/IP for `/auth/register`, 60 req/min/user for `/auth/me`, 30 req/min/user for `/auth/refresh` per TDD §8.1; return 429 (owner: platform; dependency: M3).
- **D4.4** — Implement account lockout with **dual-key counter design**: (a) **email+IP composite** counter — 5 failed logins within 15 minutes locks the (email, IP) tuple, mitigating distributed-DoS attacks against a single account; (b) **per-email aggregate** counter — 50 failed logins within 15 minutes across all IPs locks the email itself, mitigating IP-rotating attacks per FR-AUTH-001 AC4. Both counters return 423 Locked, emit a security event, and notify an admin alert channel. Aggregate threshold is tunable via config; if false-positive rate > 1%, fall back to composite-only (owner: backend; dependency: D4.3). <!-- Source: R2.5 invariant probe INV-004 — modified per Change #10 -->
- **D4.5** — Wire the `audit_log` table (from D1.1) into every `AuthService` method: login success/failure, registration, refresh, reset-request, reset-confirm, lockout. Each row captures userId (nullable for failed-unknown-email cases), eventType, timestamp, IP, outcome. **SOC2 control-mapping reviewer named in M1 D1.5 ADR; sign-off calendar hold confirmed by M3 exit so the reviewer's M4 slot is locked in ahead of Q3 2026 audit-prep contention** (owner: backend + security; dependency: D4.1, D4.4). <!-- Source: R2.5 invariant probe INV-002 — modified per Change #9 -->
- **D4.6** — Expose Prometheus metrics `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total` per TDD §14; wire OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService` (owner: backend + observability; dependency: D4.5).
- **D4.7** — Build k6 load harness: 500 concurrent login requests sustained for 5 minutes; assert p95 < 200ms (NFR-PERF-001) and zero errors (NFR-PERF-002); produce a published report (owner: QA; dependency: D4.6).
- **D4.8** — Log scrubber gate: automated test that pipes 1000 randomized auth requests through the system and greps captured logs for any `password`, `accessToken`, or `refreshToken` value substring; zero matches required (Objective 3) (owner: security; dependency: D4.5).

**Exit Criteria**:

- FR-AUTH-005 acceptance criteria pass end-to-end (reset email arrives in < 60s; link expires after 1 hour; password update invalidates all sessions).
- NFR-PERF-001 (p95 < 200ms) and NFR-PERF-002 (500 concurrent) verified by k6 report.
- NFR-SEC-001 (bcrypt cost 12) and NFR-SEC-002 (RS256 / 2048-bit) verified by automated tests.
- SOC2 audit-log control mapping reviewed and signed by named compliance reviewer.
- Log scrubber gate green (zero credential leaks).
- All Prometheus metrics scraped by the staging Prometheus instance and visible in a draft Grafana dashboard.
- **External penetration test (D5.1) report delivered; this is both the M4 exit gate and the M5 entry artifact (per Change #12).** <!-- Source: R2.5 invariant probe INV-007 — added per Change #12 -->

**Architectural Risks**:

- Bcrypt cost 12 under 500 concurrent load can saturate CPU and breach the p95 latency budget. M4 must measure this explicitly; if breached, the contingency is to scale horizontally rather than reduce cost factor (security non-negotiable). Horizontal scaling multiplies client connections against the PostgreSQL 200-max cap — PgBouncer (D1.8) absorbs this multiplication.
- Account lockout (D4.4) is itself a DoS vector — an attacker can lock arbitrary users by submitting bad passwords. Mitigation: dual-key counter design (email+IP composite for DoS prevention + per-email aggregate for IP-rotation attack defense, per Change #10). ADR documents this; M4 tests both counters explicitly. <!-- Source: R2.5 invariant probe INV-004 — modified per Change #10 -->
- Audit logging at 500 concurrent rps generates ~500 row inserts/sec into PostgreSQL; M4 must verify the `audit_log` table doesn't become the latency bottleneck — consider batching or a separate write path if measurements show it.
- SendGrid delivery latency can exceed the 60-second target if their API is degraded; the password-reset flow must enqueue and acknowledge before delivery confirmation, with retries on transient SendGrid errors.

**Dependencies**: Upstream — M3 (token lifecycle), M2 (audit log table). Downstream — M5 (pen-test remediation, ops readiness). External pen-test (D5.1) executes during M4 exit window so its findings drive M5 work (per Change #12).

### M5: GA Readiness — 2026-06-09

<!-- Source: Base (V1 opus:architect, modified) — pen-test resequenced to M4→M5 boundary per Change #12; rollback contract changed to forward-only per Change #14; TDD §19.4 thresholds quoted verbatim per Change #7 -->

**Scope**: Pen-test remediation, finalization of runbooks and dashboards, rollout plan execution with a controlled traffic ramp, and the GA cutover. **The external penetration test (D5.1) now sits on the M4→M5 boundary (per Change #12): it is the M4 exit gate AND the M5 entry artifact. M5's 11-day window is therefore allocated to remediation (D5.2, 7 days), parallel runbooks/dashboards (D5.3-D5.5, 5 days), rollout (D5.6, 4 days), and readiness review (D5.7, 1 day) — no buffer compression.**

**Deliverables**:

- **D5.1** — External penetration test scoped to all `/auth/*` endpoints, password reset flow, account lockout (both composite and aggregate counters), token revocation, atomic refresh-token rotation, and `AuthProvider` token storage; severity-classified report. **Executes at the M4→M5 boundary as the M4 exit gate AND the M5 entry artifact** (owner: external pen-test vendor; dependency: M4 substantially complete). <!-- Source: R2.5 invariant probe INV-007 — modified per Change #12 -->
- **D5.2** — Remediate all critical and high findings from D5.1 within a **7-day remediation window** (was 2 days in V1; expanded per Change #12 resequence); medium findings tracked but not blocking (owner: backend + security; dependency: D5.1). <!-- Source: R2.5 invariant probe INV-007 — modified per Change #12 -->
- **D5.3** — Publish runbooks: "login failure rate alert response", "Redis unavailability", "key rotation procedure", "account unlock for admin (Jordan persona)", "audit log export for SOC2 review", "forward-only rollback after revokeAll events" (owner: SRE + backend; dependency: M4 metrics + alerts).
- **D5.4** — Finalize Grafana dashboards covering login rate, error rate by code, p95/p99 latency per endpoint, refresh-token churn, lockout count (both composite and aggregate), audit-log volume; tie each panel to a runbook link (owner: observability + SRE; dependency: D4.6).
- **D5.5** — Configure production alerts: login failure rate > 20% over 5 min, p95 > 500ms over 10 min, `TokenManager` Redis connection failure, password-hash latency > 1s (early bcrypt-saturation warning), audit-log write failure (owner: SRE; dependency: D5.4).
- **D5.6** — Execute controlled rollout: 1% traffic → 10% → 50% → 100%, gated 24 hours per stage, with a documented **forward-only rollback procedure** (per Change #14) that reverts the API gateway routing rule and preserves user data. Rollout window is 4 days within M5 (owner: SRE + product; dependency: D5.5).
- **D5.7** — Operational-readiness review meeting; sign-off checklist (oncall rotation, runbooks live, dashboards visible, alerts active, rollback rehearsed, dual-key lockout tested); engineering manager signature (owner: engineering manager; dependency: D5.3-D5.6).

**Exit Criteria**:

- Zero open critical or high findings from D5.1.
- 100% traffic on the new service for 48 hours with no incident-grade alerts.
- All five FRs and all NFRs verified in production telemetry.
- Operational-readiness checklist signed.
- Public release notes shipped.

**Architectural Risks**:

- A pen-test finding at the M4→M5 boundary could push GA past 2026-06-09. **The 7-day remediation window in D5.2 (per Change #12) replaces V1's original 2-day buffer**; if a critical finding requires more than 7 days of work, GA is delayed rather than shipped with a known critical vulnerability. Per TDD §19.4, transparent comms to product. <!-- Source: R2.5 invariant probe INV-007 — modified per Change #12 -->
- **Rollback contract is forward-only after revokeAll events** (per Change #14): Rollback after a revokeAll event (password reset, security incident) is forward-only; affected users re-login on the legacy or new service. Pre-revokeAll tokens are flushed in both services upon rollback to prevent stale-token validation drift. This replaces V1's original "honor refresh tokens" language, which directly contradicted `TokenManager.revokeAll()` semantics. Coordination with the legacy service for token-flush API is required; documented in the D5.3 rollback runbook. <!-- Source: R2.5 invariant probe INV-013 — modified per Change #14 -->
- **Verbatim TDD §19.4 rollback trigger thresholds**: Rollback is triggered immediately and automatically if any of the following fire during Beta or GA: **"p95 > 1000ms for > 5 min; error rate > 5% for > 2 min; Redis connection failures > 10/min"** (TDD §19.4). Any `UserProfile` data corruption also triggers rollback. <!-- Source: Variant 2 (sonnet:analyzer), §Performance & Reliability Gates closing paragraph — merged per Change #7 -->

**Dependencies**: Upstream — M4 (hardening complete), D5.1 (pen-test at M4→M5 boundary). Downstream — none (terminal milestone), but feeds the v1.1 MFA planning cycle.

## Sprint-Level Breakdown

<!-- Source: Variant 2 (sonnet:analyzer), §Sprint-Level Breakdown — merged per Change #2; owner cells reconciled with V1's 5-workstream model -->

| Sprint | Window | Milestones | Owner Workstreams | Primary Deliverables |
|--------|--------|------------|-------------------|----------------------|
| S1 | 2026-03-17 → 2026-03-31 | M1 (part 1) | Backend Core; Operational Readiness | D1.1 PostgreSQL schema + pool; D1.2 Redis cluster; D1.3 RSA key pair |
| S2 | 2026-04-01 → 2026-04-14 | M1 (part 2) → M2 start | Backend Core; Security & Compliance | D1.4 OpenAPI freeze; D1.5 ADRs (incl. SOC2 reviewer name); D1.6 SendGrid; D1.7 frontend-team commitment; D1.8 PgBouncer |
| S3 | 2026-04-15 → 2026-04-28 | M2 | Backend Core; Security & Compliance | D2.1-D2.6 `AuthService` + `PasswordHasher` + `JwtService` + `UserProfile` + login/register + integration tests |
| S4 | 2026-04-29 → 2026-05-15 | M3 | Backend Core; Frontend Integration; Observability & SRE | D3.1-D3.3 `TokenManager` + `/auth/refresh` + `/auth/me`; D3.4-D3.6 `AuthProvider` + `LoginPage`/`RegisterPage` + Playwright E2E |
| S5 | 2026-05-16 → 2026-05-29 | M4 | Backend Core; Security & Compliance; Observability & SRE | D4.1-D4.8 reset flow + dual-key lockout + rate limit + audit log + metrics + k6 + log scrubber; D5.1 pen-test (M4→M5 boundary) |
| S6 | 2026-05-30 → 2026-06-09 | M5 | Operational Readiness; Backend Core; Security & Compliance; Observability & SRE | D5.2 remediation (7d); D5.3-D5.5 runbooks/dashboards/alerts; D5.6 rollout (1%→10%→50%→100%); D5.7 readiness review |

Note: V2's "S1-S6" sprint structure is preserved but reconciled with V1's M1-M5 milestone calendar. V1's M1 exit (2026-04-03) sits inside S2; V1's M4 absorbs V2's reset and frontend work into the V1 hardening milestone. Each sprint may have multiple owning workstreams from the 5-workstream model below.

## Workstreams

<!-- Source: Base (V1 opus:architect, original) -->

The roadmap executes across five parallel workstreams that share milestone gates but progress independently between gates:

- **Backend Core** — Owns `AuthService`, `PasswordHasher`, `JwtService`, `TokenManager`, the `UserProfile` repository, and the REST endpoints. This is the critical-path workstream; M1 through M4 are dominated by its deliverables. Skills: TypeScript, PostgreSQL, Redis, JWT internals. Lead: auth-team tech lead (test-lead per TDD).
- **Frontend Integration** — Owns `LoginPage`, `RegisterPage`, `AuthProvider`, and the routing integration into protected routes. Engagement begins mid-M2 with API contract review and ramps in M3. Skills: React, context API, secure token storage. Lead: frontend-team representative (named in D1.7 per Change #8). <!-- Source: R2.5 invariant probe INV-001 — modified per Change #8 -->
- **Security & Compliance** — Owns the password policy enforcement, audit-log schema and SOC2 control mapping, RS256 key management, pen-test coordination, and the log-scrubber gate. Active across all milestones; peaks in M4 and M5. Skills: SOC2 controls, bcrypt/JWT cryptanalysis, NIST SP 800-63B. Lead: sec-reviewer per TDD; SOC2 compliance reviewer named in D1.5 ADR (per Change #9).
- **Observability & SRE** — Owns Prometheus metric exposition, OpenTelemetry trace instrumentation, Grafana dashboards, alert configuration, and runbooks. Engagement begins in M2 with metric/trace point definition; peaks in M4 and M5. Skills: Prometheus, OpenTelemetry, Grafana, alerting design. Lead: platform-team observability owner.
- **Operational Readiness** — Owns rollout strategy, oncall rotation, rollback procedures (forward-only contract per Change #14), capacity planning, and the GA gate. Active in M1 (capacity planning for PostgreSQL pool with PgBouncer, Redis cluster) and M5 (rollout execution). Lead: engineering manager.

## Cross-Cutting Concerns

<!-- Source: Base (V1 opus:architect, original) -->

**Observability**: Every `AuthService` public method emits a structured log line (JSON, no PII in the message body), a Prometheus counter, and an OpenTelemetry span. The span graph for a login request must show `AuthService.login` → `PasswordHasher.verify` → `TokenManager.issue` → `JwtService.sign` with each child span's latency, enabling root-cause attribution when p95 budgets are breached. Metric cardinality is bounded: no userId labels on Prometheus metrics (per high-cardinality avoidance), but audit logs carry userId for forensic queries.

**Security**: Defense-in-depth is non-negotiable. (1) TLS 1.3 at the gateway. (2) `PasswordHasher` with bcrypt cost 12, constant-time verify, dummy-verify for unknown-email cases. (3) `JwtService` with RS256/2048-bit RSA, `kid` header for rotation, 5-second clock-skew tolerance. (4) `TokenManager` storing only refresh-token hashes in Redis, atomic rotation (D3.2 integration-test gated per Change #11). (5) Rate limiting at the gateway with per-IP and per-user dimensions. (6) Account lockout with dual-key counters: email+IP composite + per-email aggregate (per Change #10). (7) Log scrubber gate preventing credential leaks. (8) CORS restricted to known frontend origins. (9) Pen-test at M4→M5 boundary (per Change #12). (10) Quarterly RSA key rotation procedure.

**Performance Budgets**: NFR-PERF-001 (p95 < 200ms for all auth endpoints) and NFR-PERF-002 (500 concurrent). Sub-budgets: `PasswordHasher.hash` < 500ms (TDD success metric), `TokenManager.refresh` p95 < 100ms (TDD success metric), `JwtService.sign/verify` < 5ms. Bcrypt cost 12 is the dominant latency contributor and is held constant for security; throughput scales via horizontal pod replication, with PgBouncer (D1.8) absorbing the resulting PostgreSQL client multiplication against the 200-max cap. M4 verifies the budgets with k6.

**Data Integrity**: Database migrations for the `users` and `audit_log` tables use forward-only migrations with `IF NOT EXISTS` semantics; rollback is achieved by feature-flag disable rather than schema reversal once data exists. Concurrent registration race resolved by the unique constraint on `email`. Email normalization to lowercase is enforced at the `AuthService` layer to avoid case-mismatch bypasses. Redis is treated as authoritative for refresh-token state but its loss does not lose user identity (only forces re-login) — graceful-degradation contract is documented in the M1 ADR.

## Validation Strategy

<!-- Source: Variant 2 (sonnet:analyzer), §Validation Strategy — merged per Change #4 -->

Validation follows the test pyramid in TDD §15.1: 80% unit / 15% integration / 5% E2E. Every FR-AUTH-NNN has at least one unit test and one integration test; high-traffic flows additionally have E2E coverage.

| FR | Unit Validation | Integration Validation | E2E Validation |
|----|-----------------|------------------------|----------------|
| FR-AUTH-001 (login) | `AuthService.login()` happy + invalid-credentials + lockout (both composite and aggregate counters per Change #10) (TDD §15.2) | `POST /auth/login` against PostgreSQL with bcrypt-hashed seed user | Playwright login flow via `LoginPage` |
| FR-AUTH-002 (register) | `AuthService.register()` validation: duplicate email, weak password | Registration persists `UserProfile` to PostgreSQL (TDD §15.2) | Playwright register → first login |
| FR-AUTH-003 (tokens) | `TokenManager.refresh()` rotation; `JwtService.sign()`/`verify()` | Expired refresh token rejected by Redis TTL; **atomic rotation under concurrent refresh per Change #11** (TDD §15.2) | `AuthProvider` silent refresh in Playwright |
| FR-AUTH-004 (profile) | `AuthService.getMe()` returns full `UserProfile` shape | `GET /auth/me` with Bearer returns 200 + all fields | `ProfilePage` renders post-login |
| FR-AUTH-005 (reset) | Reset-token single-use + 1h expiry logic | Full request → confirm flow against staging SendGrid; revokeAll invalidates prior refresh tokens | Playwright full reset journey |

NFR validation is gated at M4 exit (load tests) and M5 entry (pen-test, per Change #12):

- NFR-PERF-001 (p95 < 200ms): k6 load test in staging at M4 exit (D4.7)
- NFR-PERF-002 (500 concurrent): k6 sustained-load test at M4 exit (D4.7)
- NFR-REL-001 (99.9% uptime): measured over 7 days post-GA via health-check monitor
- NFR-SEC-001 (bcrypt cost 12): unit test asserts `PasswordHasher` cost parameter (TDD §15.2)
- NFR-SEC-002 (RS256 / 2048-bit): configuration validation test in CI

## Risk Register

<!-- Source: Base (V1 opus:architect, original) -->

| Risk | Likelihood | Impact | Mitigation | Contingency |
|------|-----------|--------|------------|-------------|
| Bcrypt cost 12 breaches p95 < 200ms under 500-concurrent load | Medium | High | Benchmark on production-equivalent hardware in M2; horizontal scaling plan ready by M4; PgBouncer (D1.8) absorbs client multiplication | Add stateless pre-check (rate-limit + dummy bcrypt) at gateway; scale horizontally; never reduce cost factor |
| Redis unavailability invalidates all refresh sessions | Low | High | Multi-AZ Redis cluster (D1.2); rejection of refresh on Redis fail (TDD §12) is the documented fallback | Force re-login storm acceptable; advance-notice banner; cache last-known-good keys in `JwtService` so access tokens still validate |
| Critical pen-test finding at M4→M5 boundary | Medium | Critical | 7-day remediation window in D5.2 (per Change #12); pen-test scheduled at M4 exit so M5 has full remediation runway | Delay GA rather than ship known-critical vulnerability; transparent comms to product |
| Account lockout exploited as DoS against legitimate users | Medium | Medium | Dual-key counter design (per Change #10): composite for DoS prevention + aggregate for IP-rotation defense; admin unlock runbook (D5.3) | Aggregate threshold tunable via config; revert to composite-only if false-positive rate > 1% |
| IP-rotating attacker bypasses email+IP composite lockout | Medium | High | Per-email aggregate counter (50/15min) catches IP-rotating attacks per FR-AUTH-001 AC4 (per Change #10) | Reduce aggregate threshold; CAPTCHA at lower thresholds; manual security review |
| SendGrid degraded delivery breaks password reset (PRD risk row 4) | Low | Medium | Delivery monitoring + retry; alert in D5.5 | Fallback to support-ticket path per PRD; queue reset requests for later delivery |
| Clock skew causes spurious 401s for users on misconfigured devices | Medium | Low | 5-second tolerance in `JwtService` (TDD §12); silent refresh in `AuthProvider` re-issues on 401 | Increase tolerance to 30s if telemetry shows widespread skew impact |
| SOC2 audit-log gap discovered post-launch | Low | Critical | M4 mapping reviewed by named compliance reviewer (D4.5, per Change #9); 12-month retention configured | Backfill audit log from application logs if telemetry was preserved; document gap |
| `AuthProvider` token storage choice exposes XSS attack surface | Medium | High | ADR in M1 (D1.5) resolves storage strategy before M3; httpOnly cookie + CSRF token is the default position | Switch to in-memory + silent-refresh-on-load if XSS surface materializes |
| Concurrent registration race produces inconsistent state | Low | Medium | Database unique constraint on email; integration test in D2.6 covers the race | Manual cleanup script for any pre-constraint legacy data (none expected on greenfield deploy) |
| MFA/OAuth extension assumptions break in v1.1/v2.0 design | Medium | Medium | Architect signs off on extension seams in M2 (Objective 4); ADR documents the seams | Acceptable to break the API at v2.0 boundary if absolutely needed; versioned URL prefix (`/v1/auth/*`) makes this clean |
| Frontend team unavailable when M3 starts | Medium | High | D1.7 organizational commitment by M1 exit (per Change #8); named POC in writing | Re-source from contractor pool or compress D3.4-D3.5 with pre-built Playwright suites |
| PostgreSQL 200-max connection cap breached by horizontal scaling | Medium | High | PgBouncer (D1.8) absorbs pod-multiplication; pool sized per source spec line 1212 (per Change #13) | Fallback to per-pod connection limits; switch PgBouncer to session-mode if proxy-mode shows bugs |
| Non-atomic refresh-token rotation creates replay window | Medium | High | D3.2 integration test verifies atomic rotation under concurrent requests (per Change #11); LUA or MULTI/EXEC mandated | Fall back to `WATCH/MULTI/EXEC` if LUA proves debug-hostile; document and gate |
| Rollback contract contradicts revokeAll semantics | Was Medium | Critical | Forward-only rollback contract (per Change #14) — pre-revokeAll tokens flushed in both services | Manual support flow for affected users; documented in D5.3 runbook |

## Dependency Graph

<!-- Source: Base (V1 opus:architect, modified) — D5.1 resequenced to M4→M5 boundary per Change #12; D1.7/D1.8 added per Changes #8/#13 -->

The critical path runs: D1.1/D1.2/D1.3/D1.4/D1.7/D1.8 (M1) → D2.1/D2.2/D2.3/D2.4 (M2) → D3.1/D3.2 (M3 backend) → D3.4/D3.5 (M3 frontend) → D4.1/D4.5/D4.6 (M4 hardening) → D5.1 (M4→M5 boundary pen-test) → D5.2 (M5 remediation) → D5.6/D5.7 (M5 rollout).

Key sequencing constraints:

- D1.3 (RSA keys) blocks D2.3 (`JwtService`) absolutely — no JWT signing without keys.
- D1.1 (Postgres + tables) blocks D2.4 (`UserProfile` repository) and D4.5 (audit logging).
- D1.2 (Redis) blocks D3.1 (`TokenManager`), which blocks D3.2 (`/auth/refresh`), which blocks D3.4 (`AuthProvider` silent refresh).
- **D1.7 (frontend-team capacity commitment) must close before M2 exit so D3.4/D3.5 have named ownership (per Change #8).** <!-- Source: R2.5 invariant probe INV-001 — added per Change #8 -->
- **D1.8 (PgBouncer) blocks the M4 k6 load test (D4.7) — without PgBouncer, the 500-concurrent test will saturate PostgreSQL's 200-max connection cap (per Change #13).** <!-- Source: R2.5 invariant probe INV-011 — added per Change #13 -->
- D2.6 (integration tests) is a gate for M2 exit and blocks all M3 work.
- **D3.2 atomic-rotation integration test (per Change #11) gates M3 exit.** <!-- Source: R2.5 invariant probe INV-005 — added per Change #11 -->
- D4.5 (audit logging wired, with named SOC2 reviewer per Change #9) blocks the SOC2 control mapping sign-off in M4.
- D4.7 (k6 load test) blocks the NFR-PERF verification at M4 exit.
- **D5.1 (pen-test) sits on the M4→M5 boundary: it is both the M4 exit gate and the M5 entry artifact (per Change #12).** <!-- Source: R2.5 invariant probe INV-007 — modified per Change #12 -->
- D5.1 blocks D5.2 (7-day remediation), which blocks D5.6 (rollout).

Parallelizable: Frontend D3.4/D3.5 can begin once the OpenAPI spec is frozen (D1.4) using mocked endpoints, joining the backend at M3 integration. Observability D4.6 instrumentation can be developed against the M2 codebase. SOC2 control mapping (part of D4.5) can be drafted from the TDD before D4.5 implementation lands. D5.3-D5.5 (runbooks, dashboards, alerts) execute in parallel with D5.2 (remediation) during M5.

## Performance & Reliability Gates

<!-- Source: Variant 2 (sonnet:analyzer), §Performance & Reliability Gates — merged per Change #3; V1's final GA criteria preserved as M5-exit row -->

Hard gates blocking promotion from one phase to the next:

| Gate | Threshold | Phase Boundary | Source |
|------|-----------|----------------|--------|
| Connectivity smoke tests | `psql` + `redis-cli` + PgBouncer pass | M1 exit | V1 D1.1/D1.2/D1.8 |
| OpenAPI spec | Spectral-clean (0 errors) | M1 exit | V1 D1.4 |
| ADRs signed and merged | All 4 ADRs + SOC2 reviewer name | M1 exit | V1 D1.5 |
| Frontend-team POC committed | Named in writing, ≥1.0 FTE allocated | M1 exit | Change #8 (INV-001) |
| FR-AUTH-001 + FR-AUTH-002 acceptance | All AC pass against live PostgreSQL | M2 exit | V1 §M2 exit |
| Unit test coverage | ≥ 80% on `AuthService`/`PasswordHasher`/`JwtService` | M2 exit | NFR-SEC-001, TDD §24.1 |
| Architect sign-off on MFA/OAuth seam ADR | Signed | M2 exit | V1 Objective 4 |
| bcrypt cost factor | == 12 (asserted by unit test) | M2 exit | NFR-SEC-001 |
| JWT signing algorithm | == RS256 + 2048-bit RSA | M2 exit | NFR-SEC-002 |
| FR-AUTH-003 + FR-AUTH-004 acceptance | UI end-to-end pass | M3 exit | V1 §M3 exit |
| Silent refresh | Zero re-login prompts in 30-min Playwright session | M3 exit | V1 Objective 5 |
| Atomic refresh-token rotation | D3.2 integration test green | M3 exit | Change #11 (INV-005) |
| `AuthProvider` storage ADR | Resolved | M3 exit | V1 §M3 risks |
| FR-AUTH-005 acceptance | Reset email < 60s; link expires after 1h; revokeAll | M4 exit | V1 §M4 exit |
| Login p95 latency | < 200ms (k6) | M4 exit | NFR-PERF-001 |
| Concurrent login capacity | 500 RPS sustained (k6) | M4 exit | NFR-PERF-002 |
| Log scrubber gate | Zero credential matches in 1000-request grep | M4 exit | V1 D4.8 |
| SOC2 audit-log control mapping | Signed by named compliance reviewer | M4 exit | Change #9 (INV-002) |
| Dual-key lockout | Both composite and aggregate counters tested | M4 exit | Change #10 (INV-004) |
| Prometheus metrics in staging Grafana | All 4 counters visible | M4 exit | V1 D4.6 |
| External penetration test | Report delivered, scoped to all auth surfaces | M4→M5 boundary | Change #12 (INV-007) |
| Critical/high pen-test findings | Zero open | M5 exit | V1 §M5 exit |
| Runbooks published | All 6 runbooks live (incl. forward-only rollback) | M5 exit | Change #14 (INV-013) |
| Alerts active | All 5 alerts live | M5 exit | V1 D5.5 |
| Rollback rehearsed | Forward-only rollback drill complete | M5 exit | Change #14 (INV-013) |
| Engineering-manager readiness signature | Signed | M5 exit | V1 D5.7 |
| Error rate during rollout | < 0.1% | Each rollout stage (1%/10%/50%/100%) | TDD §19.1 |
| Redis connection failures during rollout | 0 over 2-week observation | Each rollout stage | TDD §19.1 |
| Uptime post-GA | 99.9% over first 7 days | GA exit | NFR-REL-001 |
| Rollback trigger thresholds | Not breached (TDD §19.4) | Every rollout stage | TDD §19.4 |
| **Final GA criteria (cluster row for M5 exit)** | (1) All five FRs verified in production; (2) all NFRs (NFR-PERF-001, NFR-PERF-002, NFR-REL-001, NFR-SEC-001, NFR-SEC-002) verified; (3) 100% traffic ramped 48h without incident-grade alert; (4) SOC2 control mapping signed; (5) on-call live + runbooks linked from alerts; (6) forward-only rollback rehearsed within prior 7 days; (7) public release notes shipped | GA cutover 2026-06-09 | V1 §Final GA criteria (preserved as cluster row per Change #3) |

Rollback is triggered immediately and automatically if any of the following fire during Beta or GA (TDD §19.4): **"p95 > 1000ms for > 5 min; error rate > 5% for > 2 min; Redis connection failures > 10/min"**; any `UserProfile` data corruption also triggers rollback.

## Out-of-Scope (explicit)

<!-- Source: Variant 2 (sonnet:analyzer), §Out-of-Scope — merged per Change #5 -->

v1.0 explicitly excludes the following per TDD §3.2 and PRD §Scope Definition. These appear in this section solely to prevent scope creep — they are not roadmap items:

| Capability | Deferred To | Rationale |
|------------|-------------|-----------|
| OAuth / OIDC / social login (Google, GitHub) | v1.1 (NG-001) | Requires third-party integration infrastructure |
| Multi-factor authentication (SMS/TOTP) | v1.2 (NG-002) | Separate feature; requires SMS/TOTP vendor selection |
| Role-based access control enforcement | v2.0 (NG-003) | Authorization is a distinct PRD; `roles` field exists but is not enforced by `AuthService` |
| API-key authentication for service-to-service | v1.1 (OQ-001) | Open question pending v1.1 scope discussion |
| "Remember me" extended session duration | TBD (PRD OQ-4) | Open question, owner: Product |
| Account lockout policy beyond 5/15min composite + 50/15min aggregate | v1.1 candidate (PRD OQ-3) | Owner: Security; current dual-key design per Change #10 |

Anything not on the in-scope list is out-of-scope by construction. New asks during the build must be triaged to a future release and added to the deferred-list, not absorbed into v1.0.

## Open Questions

<!-- Source: Base (V1 opus:architect, modified) — V2's Owner + Target Resolution Date columns added per Change #6; V1's 8 OQs and recommended positions preserved; new INV-001 OQ appended per Change #8 -->

The PRD and TDD leave the following architectural decisions unresolved; each must be answered before its dependent deliverable begins. V2's table format (Owner + Target Resolution Date) is applied; V1's "Recommended position" prose is preserved beneath each row.

| ID | Question | Owner | Target Resolution | Source |
|----|----------|-------|-------------------|--------|
| OQ-1 | `AuthProvider` token storage strategy | architect | 2026-04-03 (M1 D1.5 ADR) | TDD §22 |
| OQ-2 | Maximum concurrent refresh tokens per user | Product + auth-team | 2026-04-24 (M2 exit) | PRD OQ-2 |
| OQ-3 | Account lockout policy details (composite + aggregate thresholds) | Security | 2026-05-15 (before D4.4) | PRD OQ-3, Change #10 |
| OQ-4 | Synchronous vs. asynchronous password-reset email | Engineering | 2026-04-22 (before M3 reset work) | PRD OQ-1 |
| OQ-5 | "Remember me" extended session duration | Product | 2026-05-06 (deferred to v1.1) | PRD OQ-4 |
| OQ-6 | Rate-limit identity for `/auth/login` (IP vs. composite) | Security + Platform | 2026-04-24 (before D4.3) | V1 OQ-6 |
| OQ-7 | Key rotation overlap window for `JwtService` | Security + architect | 2026-04-03 (M1 D1.5 ADR) | V1 OQ-7 |
| OQ-8 | Audit-log partitioning and 12-month archive path | backend + Platform | 2026-05-29 (M4 exit) | V1 OQ-8 |
| OQ-9 | Frontend-team capacity confirmation: named POC + FTE allocation | engineering manager + frontend-team lead | 2026-04-03 (M1 D1.7) | Change #8 (INV-001) |

**Recommended positions** (preserved from V1, applied per row):

1. **OQ-1 (`AuthProvider` token storage)** — Default position: httpOnly cookie + CSRF token; alternatives: in-memory only with silent refresh on page load, encrypted localStorage. Must be answered in the M1 ADR (D1.5) before M3 D3.4 begins.

2. **OQ-2 (max concurrent refresh tokens)** — If unlimited, multi-device is trivially supported per PRD edge case row 6; if capped, oldest-token-eviction policy needed. Recommended position: unlimited within the 7-day TTL window, but emit a metric on per-user count to detect anomalies.

3. **OQ-3 (lockout policy details)** — PRD edge case row 3 specifies 5 attempts; this roadmap proposes a 15-minute sliding window with **dual-key counters per Change #10**: email+IP composite (5/15min) + per-email aggregate (50/15min). Final policy must be signed by security before D4.4.

4. **OQ-4 (sync vs. async reset email)** — Affects whether `/auth/reset-request` returns after SMTP enqueue or after delivery confirmation. Recommended position: asynchronous enqueue with 200 response, separate delivery-success metric; PRD 60-second SLO measures end-to-end, not API response time.

5. **OQ-5 ("Remember me")** — Out of scope for v1.0; document as a v1.1 candidate alongside MFA. The 7-day refresh window already covers the common case.

6. **OQ-6 (rate-limit identity)** — IP-based rate limiting is specified (10 req/min per IP) but corporate NAT can put many users behind one IP. Recommended position: keep IP-based for v1.0, add a per-email cap as secondary dimension, plan a CAPTCHA fallback for v1.1.

7. **OQ-7 (key rotation overlap)** — The M1 ADR must specify how long an old `kid` remains valid after rotation (proposal: 24 hours, equal to access-token max age × 96), and the runbook (D5.3) must document the rotation procedure.

8. **OQ-8 (audit-log volume and retention)** — At 500 concurrent rps the audit log accrues meaningfully over 90 days; M4 must size the PostgreSQL `audit_log` table partitioning strategy and document the 12-month archive path required by the PRD compliance row.

9. **OQ-9 (frontend-team capacity)** — Frontend-team representative must be named with FTE allocation by M1 exit (D1.7 per Change #8). Recommended position: ≥1.0 FTE dedicated coverage for D3.4/D3.5/D3.6 across mid-M2 through M3; escalate to contractor pool if internal capacity gap emerges. <!-- Source: R2.5 invariant probe INV-001 — added per Change #8 -->

These open questions are deliberately listed at the roadmap level (rather than buried in milestones) because each touches multiple deliverables and warrants explicit cross-team resolution before its blocking deliverable enters implementation. Open questions that miss their target resolution date escalate to the engineering manager for explicit defer-or-decide; none may remain open at M5 entry.
