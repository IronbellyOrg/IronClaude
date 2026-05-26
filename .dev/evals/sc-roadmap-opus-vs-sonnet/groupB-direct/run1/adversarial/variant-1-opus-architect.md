---
id: "AUTH-ROADMAP-V1"
title: "User Authentication Service - Roadmap"
source: "merged-prd-tdd-user-auth.md"
target_release: "v1.0 (2026-06-09)"
variant: "opus:architect"
---

# User Authentication Service — Roadmap

## Executive Summary

The User Authentication Service is the foundational identity substrate on which the platform's entire Q2-Q3 2026 personalization roadmap and SOC2 Type II compliance posture depend. This roadmap sequences the construction of a JWT-based, stateless authentication system organized around `AuthService` as the orchestrating facade, with `TokenManager`, `JwtService`, `PasswordHasher`, and the `UserProfile`/`AuthToken` data models forming the core component graph. The architecture deliberately separates credential validation (bcrypt cost-12 hashing via `PasswordHasher`), token lifecycle management (15-minute access / 7-day refresh via `TokenManager` + Redis), and persistence (`UserProfile` in PostgreSQL 15) so that each cross-cutting concern — security hardening, observability, scalability — can be tested and evolved independently.

From an architectural standpoint, the dominant risk is not any single feature but the *integration surface* between four asynchronous subsystems: PostgreSQL for durable user records, Redis for revocable refresh-token state, the email delivery provider (SendGrid) for password reset, and the RS256-signing key infrastructure for `JwtService`. The roadmap therefore front-loads infrastructure provisioning and contract definition (M1) before any user-visible flow is built, and explicitly carves out a hardening milestone (M4) to absorb the security, observability, and resilience work that always slips when squeezed into feature sprints. The frontend integration (`LoginPage`, `RegisterPage`, `AuthProvider`) is sequenced to begin only once the backend contracts are stable, with `AuthProvider`'s silent-refresh behavior treated as a first-class architectural concern rather than UI polish.

Critically, the v1.0 design must avoid trapping the team into a corner that the explicit non-goals (OAuth, MFA, RBAC) will eventually demand. The `AuthService` interface and `AuthToken` schema are sequenced to ship with extension seams — payload claims, scope fields, role arrays — that allow MFA (v1.1) and OAuth (v2.0) to land as additive changes rather than breaking rewrites. Target GA is 2026-06-09, leaving ~11 weeks from start of M1 to a hardened, audited, observed v1.0.

## Strategic Objectives

1. **Ship a SOC2-auditable identity layer by 2026-06-09** — Every authentication event (login, registration, refresh, reset, lockout) is persisted to the audit log with user ID, IP, timestamp, and outcome, with 90-day retention in PostgreSQL and 12-month archive per the PRD compliance table. Measurable outcome: 100% of `AuthService` public methods emit structured audit records validated against SOC2 control mapping in M4.

2. **Meet the p95 < 200ms latency budget under 500-concurrent-request load** — NFR-PERF-001 and NFR-PERF-002 require that `AuthService.login()`, `TokenManager.refresh()`, and `/auth/me` all stay under 200ms at the 95th percentile while sustaining 500 concurrent logins. Measurable outcome: k6 load harness in M3 produces a green report attached to the M4 exit gate.

3. **Eliminate plaintext credential surface area end-to-end** — Passwords pass from `RegisterPage`/`LoginPage` through TLS 1.3 into `PasswordHasher` (bcrypt cost 12) without ever appearing in logs, error messages, exception traces, or APM payloads. Refresh tokens are stored hashed in Redis by `TokenManager`. Measurable outcome: automated log-scrubber test in M4 plus the M5 penetration-test report.

4. **Preserve extensibility for MFA (v1.1) and OAuth (v2.0)** — `AuthService` method signatures, the `AuthToken` payload schema, and the `UserProfile` roles array are designed so that adding a TOTP step or an external identity provider requires only additive changes, not breaking API revisions. Measurable outcome: ADR documenting the MFA and OAuth extension points, signed off by the architect approver in M2.

5. **Deliver a frontend that survives token expiry transparently** — The `AuthProvider` performs silent refresh before access-token expiry, recovers from 401 responses, and degrades gracefully when Redis is unavailable. Measurable outcome: Playwright E2E suite in M3 covers expiry, refresh, and revocation flows with zero user-visible re-login prompts inside the 7-day window.

6. **Establish operational readiness before GA** — Runbooks, dashboards, alerts (login failure rate > 20% over 5min, p95 > 500ms, Redis connection failures), and an on-call rotation are in place at least one week before 2026-06-09. Measurable outcome: M5 operational-readiness review checklist signed by the engineering manager.

## Milestones

| Milestone | Target Date | Scope | Exit Criteria | Architectural Focus |
|-----------|-------------|-------|---------------|---------------------|
| M1: Foundations | 2026-04-03 | Infra provisioning, contracts, ADRs | Postgres+Redis up, OpenAPI schema frozen, key infra in place | Component boundaries, dependency graph |
| M2: Core Auth Backend | 2026-04-24 | `AuthService` + `PasswordHasher` + `JwtService` + register/login | FR-AUTH-001, FR-AUTH-002 green; integration tests pass | Service decomposition, contract stability |
| M3: Token Lifecycle + Frontend | 2026-05-15 | `TokenManager` refresh, `AuthProvider`, `LoginPage`/`RegisterPage` | FR-AUTH-003, FR-AUTH-004 green; silent refresh works end-to-end | Stateless session integrity, UI/state seam |
| M4: Hardening + Reset Flow | 2026-05-29 | FR-AUTH-005, rate limiting, audit logs, observability | NFR-PERF-001/002, NFR-SEC-001/002 verified; SOC2 mapping done | Security, performance, observability |
| M5: GA Readiness | 2026-06-09 | Pen-test remediation, runbooks, dashboards, rollout | All release gates pass; on-call ready; rollback rehearsed | Operational excellence, contingency |

### M1: Foundations — 2026-04-03

**Scope**: Stand up infrastructure dependencies, freeze API contracts, ratify architectural decisions, and produce the dependency graph that subsequent milestones execute against. This is a deliberately backend-heavy milestone — no user-facing code ships here.

**Deliverables**:

- **D1.1** — Provision PostgreSQL 15 with a dedicated `auth` schema, including `users` and `audit_log` tables; configure pg-pool connection pooling sized for 500 concurrent connections (owner: platform team; dependency: infra capacity review).
- **D1.2** — Provision Redis 7 cluster for `TokenManager` refresh-token storage; verify TCP/RESP connectivity from the `AuthService` runtime environment; document failover behavior (owner: platform team; dependency: D1.1 not required, can parallelize).
- **D1.3** — Generate, store, and rotate the 2048-bit RSA key pair used by `JwtService` for RS256 signing; document quarterly rotation procedure (owner: security; dependency: secret-management system).
- **D1.4** — Freeze the OpenAPI 3.1 spec for `/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`, `/auth/reset-request`, `/auth/reset-confirm`, including the standardized error envelope `{ error: { code, message, status } }` (owner: backend lead; dependency: PRD/TDD review).
- **D1.5** — Author ADRs covering: (a) JWT vs. server-side sessions, (b) bcrypt cost-12 vs. argon2id, (c) refresh-token storage in Redis with hashed values, (d) MFA/OAuth extension seams in `AuthService` and `AuthToken` (owner: architect; dependency: D1.4).
- **D1.6** — Configure SendGrid (or equivalent) transactional email account with sandbox + production keys for the password-reset flow; verify deliverability to test domains (owner: backend; dependency: PRD constraint — email infra "available before development begins").

**Exit Criteria**:

- `psql` and `redis-cli` smoke tests pass from the application runtime.
- OpenAPI spec validates against Spectral lint rules with zero errors.
- Signed ADRs merged to `docs/` and referenced from the TDD.
- RSA key pair accessible via secret manager; key ID published to backend team.

**Architectural Risks**:

- Redis as a hard dependency for refresh-token revocation: if Redis is unavailable, `TokenManager` must reject refresh requests rather than fall back to stateless validation (which would defeat revocation). The TDD already specifies this; M1 ratifies it in the ADR.
- Key rotation strategy for `JwtService` must avoid invalidating in-flight refresh tokens. ADR D1.5 must include a `kid` (key ID) header strategy with overlapping key validity windows.

**Dependencies**: Upstream — none (entry milestone). Downstream — every other milestone is blocked on D1.1, D1.2, D1.3, and D1.4.

### M2: Core Auth Backend — 2026-04-24

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

**Architectural Risks**:

- `AuthProvider` token storage strategy is contested: in-memory only loses sessions on page refresh; localStorage exposes to XSS; httpOnly cookies require CSRF mitigation. The ADR from M1 (D1.5) must resolve this before M3 starts, or it becomes a critical-path blocker.
- Refresh-token rotation must be atomic in Redis (LUA script or transaction) — a non-atomic rotation creates a window where both old and new tokens are valid, enabling replay if the old token is captured.
- Clock skew between client and server in `AuthProvider`'s silent-refresh scheduling must align with the 5-second tolerance in `JwtService` (D2.3); otherwise users on devices with skewed clocks see spurious 401s.

**Dependencies**: Upstream — M2 (full backend). Downstream — M4 (rate limiting wraps these endpoints, audit logs hook in here).

### M4: Hardening + Reset Flow — 2026-05-29

**Scope**: Land the password reset flow (FR-AUTH-005), wire in rate limiting, account lockout, comprehensive audit logging, Prometheus metrics, OpenTelemetry tracing, and run load tests to verify the performance NFRs. This is the milestone where cross-cutting concerns become first-class deliverables.

**Deliverables**:

- **D4.1** — Implement `POST /auth/reset-request` and `POST /auth/reset-confirm` endpoints; reset tokens are single-use, 1-hour TTL, stored hashed in Redis; on confirm, `TokenManager.revokeAll()` is invoked for the user so all existing sessions are invalidated per FR-AUTH-005 AC 4 (owner: backend; dependency: M3 complete).
- **D4.2** — Integrate SendGrid for password-reset emails; respond with identical success messaging regardless of whether the email is registered (no enumeration per PRD edge case table) (owner: backend; dependency: D1.6, D4.1).
- **D4.3** — Implement rate limiting at the API Gateway: 10 req/min/IP for `/auth/login`, 5 req/min/IP for `/auth/register`, 60 req/min/user for `/auth/me`, 30 req/min/user for `/auth/refresh` per TDD §8.1; return 429 (owner: platform; dependency: M3).
- **D4.4** — Implement account lockout: 5 failed logins within 15 minutes locks the account, returns 423 Locked, emits a security event, and notifies an admin alert channel per PRD edge case row 3 (owner: backend; dependency: D4.3).
- **D4.5** — Wire the `audit_log` table (from D1.1) into every `AuthService` method: login success/failure, registration, refresh, reset-request, reset-confirm, lockout. Each row captures userId (nullable for failed-unknown-email cases), eventType, timestamp, IP, outcome. Verify SOC2 control mapping document is complete (owner: backend + security; dependency: D4.1, D4.4).
- **D4.6** — Expose Prometheus metrics `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total` per TDD §14; wire OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService` (owner: backend + observability; dependency: D4.5).
- **D4.7** — Build k6 load harness: 500 concurrent login requests sustained for 5 minutes; assert p95 < 200ms (NFR-PERF-001) and zero errors (NFR-PERF-002); produce a published report (owner: QA; dependency: D4.6).
- **D4.8** — Log scrubber gate: automated test that pipes 1000 randomized auth requests through the system and greps captured logs for any `password`, `accessToken`, or `refreshToken` value substring; zero matches required (Objective 3) (owner: security; dependency: D4.5).

**Exit Criteria**:

- FR-AUTH-005 acceptance criteria pass end-to-end (reset email arrives in < 60s; link expires after 1 hour; password update invalidates all sessions).
- NFR-PERF-001 (p95 < 200ms) and NFR-PERF-002 (500 concurrent) verified by k6 report.
- NFR-SEC-001 (bcrypt cost 12) and NFR-SEC-002 (RS256 / 2048-bit) verified by automated tests.
- SOC2 audit-log control mapping reviewed and signed by compliance contact.
- Log scrubber gate green (zero credential leaks).
- All Prometheus metrics scraped by the staging Prometheus instance and visible in a draft Grafana dashboard.

**Architectural Risks**:

- Bcrypt cost 12 under 500 concurrent load can saturate CPU and breach the p95 latency budget. M4 must measure this explicitly; if breached, the contingency is to scale horizontally rather than reduce cost factor (security non-negotiable).
- Account lockout (D4.4) is itself a DoS vector — an attacker can lock arbitrary users by submitting bad passwords. Mitigation: lockout key includes IP + email so distributed attempts don't trivially lock a victim. ADR should document this; M4 should test it.
- Audit logging at 500 concurrent rps generates ~500 row inserts/sec into PostgreSQL; M4 must verify the `audit_log` table doesn't become the latency bottleneck — consider batching or a separate write path if measurements show it.
- SendGrid delivery latency can exceed the 60-second target if their API is degraded; the password-reset flow must enqueue and acknowledge before delivery confirmation, with retries on transient SendGrid errors.

**Dependencies**: Upstream — M3 (token lifecycle), M2 (audit log table). Downstream — M5 (pen-test, ops readiness).

### M5: GA Readiness — 2026-06-09

**Scope**: Penetration testing, remediation of any findings, finalization of runbooks and dashboards, rollout plan execution with a controlled traffic ramp, and the GA cutover.

**Deliverables**:

- **D5.1** — External penetration test scoped to all `/auth/*` endpoints, password reset flow, account lockout, token revocation, and `AuthProvider` token storage; severity-classified report (owner: external pen-test vendor; dependency: M4 complete).
- **D5.2** — Remediate all critical and high findings from D5.1 within the milestone window; medium findings tracked but not blocking (owner: backend + security; dependency: D5.1).
- **D5.3** — Publish runbooks: "login failure rate alert response", "Redis unavailability", "key rotation procedure", "account unlock for admin (Jordan persona)", "audit log export for SOC2 review" (owner: SRE + backend; dependency: M4 metrics + alerts).
- **D5.4** — Finalize Grafana dashboards covering login rate, error rate by code, p95/p99 latency per endpoint, refresh-token churn, lockout count, audit-log volume; tie each panel to a runbook link (owner: observability + SRE; dependency: D4.6).
- **D5.5** — Configure production alerts: login failure rate > 20% over 5 min, p95 > 500ms over 10 min, `TokenManager` Redis connection failure, password-hash latency > 1s (early bcrypt-saturation warning), audit-log write failure (owner: SRE; dependency: D5.4).
- **D5.6** — Execute controlled rollout: 1% traffic → 10% → 50% → 100%, gated 24 hours per stage, with a documented rollback procedure that reverts the API gateway routing rule and preserves user data (owner: SRE + product; dependency: D5.5).
- **D5.7** — Operational-readiness review meeting; sign-off checklist (oncall rotation, runbooks live, dashboards visible, alerts active, rollback rehearsed); engineering manager signature (owner: engineering manager; dependency: D5.3-D5.6).

**Exit Criteria**:

- Zero open critical or high findings from D5.1.
- 100% traffic on the new service for 48 hours with no incident-grade alerts.
- All five FRs and all NFRs verified in production telemetry.
- Operational-readiness checklist signed.
- Public release notes shipped.

**Architectural Risks**:

- A pen-test finding in the final week could push GA past 2026-06-09. Contingency: maintain a 2-day buffer between D5.2 and D5.7; if a critical finding arrives in the buffer, GA is delayed rather than shipped with a known critical vulnerability.
- Rollback during the controlled rollout must not orphan refresh tokens issued during the 1%/10%/50% stages. The rollback procedure must include either honoring those tokens via the old service (if compatible) or forcing affected users to re-login with a clear message.

**Dependencies**: Upstream — M4 (hardening complete). Downstream — none (terminal milestone), but feeds the v1.1 MFA planning cycle.

## Workstreams

The roadmap executes across five parallel workstreams that share milestone gates but progress independently between gates:

- **Backend Core** — Owns `AuthService`, `PasswordHasher`, `JwtService`, `TokenManager`, the `UserProfile` repository, and the REST endpoints. This is the critical-path workstream; M1 through M4 are dominated by its deliverables. Skills: TypeScript, PostgreSQL, Redis, JWT internals. Lead: auth-team tech lead (test-lead per TDD).
- **Frontend Integration** — Owns `LoginPage`, `RegisterPage`, `AuthProvider`, and the routing integration into protected routes. Engagement begins mid-M2 with API contract review and ramps in M3. Skills: React, context API, secure token storage. Lead: frontend-team representative.
- **Security & Compliance** — Owns the password policy enforcement, audit-log schema and SOC2 control mapping, RS256 key management, pen-test coordination, and the log-scrubber gate. Active across all milestones; peaks in M4 and M5. Skills: SOC2 controls, bcrypt/JWT cryptanalysis, NIST SP 800-63B. Lead: sec-reviewer per TDD.
- **Observability & SRE** — Owns Prometheus metric exposition, OpenTelemetry trace instrumentation, Grafana dashboards, alert configuration, and runbooks. Engagement begins in M2 with metric/trace point definition; peaks in M4 and M5. Skills: Prometheus, OpenTelemetry, Grafana, alerting design. Lead: platform-team observability owner.
- **Operational Readiness** — Owns rollout strategy, oncall rotation, rollback procedures, capacity planning, and the GA gate. Active in M1 (capacity planning for PostgreSQL pool, Redis cluster) and M5 (rollout execution). Lead: engineering manager.

## Cross-Cutting Concerns

**Observability**: Every `AuthService` public method emits a structured log line (JSON, no PII in the message body), a Prometheus counter, and an OpenTelemetry span. The span graph for a login request must show `AuthService.login` → `PasswordHasher.verify` → `TokenManager.issue` → `JwtService.sign` with each child span's latency, enabling root-cause attribution when p95 budgets are breached. Metric cardinality is bounded: no userId labels on Prometheus metrics (per high-cardinality avoidance), but audit logs carry userId for forensic queries.

**Security**: Defense-in-depth is non-negotiable. (1) TLS 1.3 at the gateway. (2) `PasswordHasher` with bcrypt cost 12, constant-time verify, dummy-verify for unknown-email cases. (3) `JwtService` with RS256/2048-bit RSA, `kid` header for rotation, 5-second clock-skew tolerance. (4) `TokenManager` storing only refresh-token hashes in Redis, atomic rotation. (5) Rate limiting at the gateway with per-IP and per-user dimensions. (6) Account lockout keyed on email+IP composite. (7) Log scrubber gate preventing credential leaks. (8) CORS restricted to known frontend origins. (9) Pen-test in M5. (10) Quarterly RSA key rotation procedure.

**Performance Budgets**: NFR-PERF-001 (p95 < 200ms for all auth endpoints) and NFR-PERF-002 (500 concurrent). Sub-budgets: `PasswordHasher.hash` < 500ms (TDD success metric), `TokenManager.refresh` p95 < 100ms (TDD success metric), `JwtService.sign/verify` < 5ms. Bcrypt cost 12 is the dominant latency contributor and is held constant for security; throughput scales via horizontal pod replication. M4 verifies the budgets with k6.

**Data Integrity**: Database migrations for the `users` and `audit_log` tables use forward-only migrations with `IF NOT EXISTS` semantics; rollback is achieved by feature-flag disable rather than schema reversal once data exists. Concurrent registration race resolved by the unique constraint on `email`. Email normalization to lowercase is enforced at the `AuthService` layer to avoid case-mismatch bypasses. Redis is treated as authoritative for refresh-token state but its loss does not lose user identity (only forces re-login) — graceful-degradation contract is documented in the M1 ADR.

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Contingency |
|------|-----------|--------|------------|-------------|
| Bcrypt cost 12 breaches p95 < 200ms under 500-concurrent load | Medium | High | Benchmark on production-equivalent hardware in M2; horizontal scaling plan ready by M4 | Add stateless pre-check (rate-limit + dummy bcrypt) at gateway; scale horizontally; never reduce cost factor |
| Redis unavailability invalidates all refresh sessions | Low | High | Multi-AZ Redis cluster (D1.2); rejection of refresh on Redis fail (TDD §12) is the documented fallback | Force re-login storm acceptable; advance-notice banner; cache last-known-good keys in `JwtService` so access tokens still validate |
| Critical pen-test finding within 5 days of GA | Medium | Critical | 2-day buffer in M5; pen-test scheduled with 2-week remediation window | Delay GA rather than ship known-critical vulnerability; transparent comms to product |
| Account lockout exploited as DoS against legitimate users | Medium | Medium | Lockout key is email+IP composite, not email alone; admin unlock runbook (D5.3) | Rate-limit lockout-triggering requests separately; surface admin notification per PRD edge case row 3 |
| SendGrid degraded delivery breaks password reset (PRD risk row 4) | Low | Medium | Delivery monitoring + retry; alert in D5.5 | Fallback to support-ticket path per PRD; queue reset requests for later delivery |
| Clock skew causes spurious 401s for users on misconfigured devices | Medium | Low | 5-second tolerance in `JwtService` (TDD §12); silent refresh in `AuthProvider` re-issues on 401 | Increase tolerance to 30s if telemetry shows widespread skew impact |
| SOC2 audit-log gap discovered post-launch | Low | Critical | M4 mapping reviewed by compliance contact (D4.5); 12-month retention configured | Backfill audit log from application logs if telemetry was preserved; document gap |
| `AuthProvider` token storage choice exposes XSS attack surface | Medium | High | ADR in M1 (D1.5) resolves storage strategy before M3; httpOnly cookie + CSRF token is the default position | Switch to in-memory + silent-refresh-on-load if XSS surface materializes |
| Concurrent registration race produces inconsistent state | Low | Medium | Database unique constraint on email; integration test in D2.6 covers the race | Manual cleanup script for any pre-constraint legacy data (none expected on greenfield deploy) |
| MFA/OAuth extension assumptions break in v1.1/v2.0 design | Medium | Medium | Architect signs off on extension seams in M2 (Objective 4); ADR documents the seams | Acceptable to break the API at v2.0 boundary if absolutely needed; versioned URL prefix (`/v1/auth/*`) makes this clean |

## Dependency Graph

The critical path runs: D1.1/D1.2/D1.3/D1.4 (M1) → D2.1/D2.2/D2.3/D2.4 (M2) → D3.1/D3.2 (M3 backend) → D3.4/D3.5 (M3 frontend) → D4.1/D4.5/D4.6 (M4 hardening) → D5.1/D5.2 (M5 pen-test) → D5.6/D5.7 (M5 rollout).

Key sequencing constraints:

- D1.3 (RSA keys) blocks D2.3 (`JwtService`) absolutely — no JWT signing without keys.
- D1.1 (Postgres + tables) blocks D2.4 (`UserProfile` repository) and D4.5 (audit logging).
- D1.2 (Redis) blocks D3.1 (`TokenManager`), which blocks D3.2 (`/auth/refresh`), which blocks D3.4 (`AuthProvider` silent refresh).
- D2.6 (integration tests) is a gate for M2 exit and blocks all M3 work.
- D4.5 (audit logging wired) blocks the SOC2 control mapping sign-off in M4.
- D4.7 (k6 load test) blocks the NFR-PERF verification at M4 exit.
- D5.1 (pen-test) blocks D5.2 (remediation), which blocks D5.6 (rollout).

Parallelizable: Frontend D3.4/D3.5 can begin once the OpenAPI spec is frozen (D1.4) using mocked endpoints, joining the backend at M3 integration. Observability D4.6 instrumentation can be developed against the M2 codebase. SOC2 control mapping (part of D4.5) can be drafted from the TDD before D4.5 implementation lands.

## Acceptance & Release Gates

**Per-milestone gates** (each must pass for the next milestone to begin):

- **M1 gate**: D1.1 + D1.2 + D1.3 connectivity smoke tests pass; OpenAPI Spectral-clean; signed ADRs merged.
- **M2 gate**: FR-AUTH-001 + FR-AUTH-002 acceptance criteria pass; integration coverage ≥ 80% on `AuthService`, `PasswordHasher`, `JwtService`; log-scrubber pre-check passes; architect sign-off on MFA/OAuth seam ADR.
- **M3 gate**: FR-AUTH-003 + FR-AUTH-004 acceptance criteria pass end-to-end through the UI; Playwright E2E suite green; silent-refresh demonstrably zero re-login prompts in 30-minute test; `AuthProvider` storage ADR resolved.
- **M4 gate**: FR-AUTH-005 acceptance criteria pass; NFR-PERF-001 + NFR-PERF-002 verified by k6; NFR-SEC-001 + NFR-SEC-002 verified by automated tests; SOC2 audit-log mapping signed; log-scrubber gate green; Prometheus metrics visible in staging Grafana.
- **M5 gate**: zero critical/high pen-test findings open; runbooks published; alerts active; rollback rehearsed; engineering manager signs operational-readiness checklist.

**Final GA criteria (2026-06-09)**:

1. All five FRs (FR-AUTH-001 through FR-AUTH-005) verified end-to-end in production.
2. All NFRs (NFR-PERF-001, NFR-PERF-002, NFR-REL-001, NFR-SEC-001, NFR-SEC-002) verified by automated test or pen-test evidence.
3. 100% traffic ramped for 48 hours without an incident-grade alert.
4. SOC2 audit-log control mapping signed by compliance.
5. Oncall rotation live; runbooks linked from every alert.
6. Rollback procedure rehearsed within the prior 7 days.
7. Public release notes shipped to the docs site.

## Open Questions

The PRD and TDD leave the following architectural decisions unresolved; each must be answered before its dependent deliverable begins:

1. **`AuthProvider` token storage strategy** (TDD §22 implicit; PRD constraint on no MFA does not resolve this) — must be answered in the M1 ADR (D1.5) before M3 D3.4 begins. Default position: httpOnly cookie + CSRF token; alternatives: in-memory only with silent refresh on page load, encrypted localStorage.

2. **Maximum concurrent refresh tokens per user** (PRD open question 2) — affects `TokenManager` storage shape and revocation semantics. If unlimited, multi-device is trivially supported per PRD edge case row 6; if capped, oldest-token-eviction policy needed. Recommended position: unlimited within the 7-day TTL window, but emit a metric on per-user count to detect anomalies.

3. **Account lockout policy details** (PRD open question 3) — PRD edge case row 3 specifies 5 attempts; this roadmap proposes a 15-minute sliding window keyed on email+IP composite, with admin notification. Final policy must be signed by security before D4.4.

4. **Synchronous vs. asynchronous password-reset email** (PRD open question 1) — affects whether `/auth/reset-request` returns after SMTP enqueue or after delivery confirmation. Recommended position: asynchronous enqueue with 200 response, separate delivery-success metric; PRD 60-second SLO measures end-to-end, not API response time.

5. **"Remember me" extended session duration** (PRD open question 4) — out of scope for v1.0; document as a v1.1 candidate alongside MFA. The 7-day refresh window already covers the common case.

6. **Rate-limit identity for `/auth/login`** — IP-based rate limiting is specified (10 req/min per IP) but corporate NAT can put many users behind one IP. Recommended position: keep IP-based for v1.0, add a per-email cap as secondary dimension, plan a CAPTCHA fallback for v1.1.

7. **Key rotation overlap window for `JwtService`** — the M1 ADR must specify how long an old `kid` remains valid after rotation (proposal: 24 hours, equal to access-token max age × 96), and the runbook (D5.3) must document the rotation procedure.

8. **Audit-log volume and retention storage** — at 500 concurrent rps the audit log accrues meaningfully over 90 days; M4 must size the PostgreSQL `audit_log` table partitioning strategy and document the 12-month archive path required by the PRD compliance row.

These open questions are deliberately listed at the roadmap level (rather than buried in milestones) because each touches multiple deliverables and warrants explicit cross-team resolution before its blocking deliverable enters implementation.
