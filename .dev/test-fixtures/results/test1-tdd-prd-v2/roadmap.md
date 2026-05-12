---
spec_source: "test-tdd-user-auth.md"
prd_source: "test-prd-user-auth.md"
complexity_score: 0.55
adversarial: true
base_variant: "B (Haiku Architect)"
variant_scores: "A:71 B:79"
convergence_score: 0.72
timeline: "6 weeks"
---

# User Authentication Service — Merged Project Roadmap

## Executive Summary

The User Authentication Service delivers secure, self-service identity management through registration, login, JWT token management, profile retrieval, and password reset. Built on a stateless REST architecture with PostgreSQL persistence, Redis token storage, and SendGrid transactional email, this service is the prerequisite for the entire Q2–Q3 2026 personalization roadmap (~$2.4M projected annual revenue) and a SOC2 Type II compliance gate in Q3 2026.

This roadmap merges the operational completeness of the Haiku Architect variant (consolidated wiring documentation, critical path analysis, FTE staffing, cost estimates, per-NFR measurement methods) with the phasing discipline of the Opus Architect variant (progressive delivery, reduced Phase 1 blast radius, explicit open questions tracking, post-GA stabilization). The adversarial debate converged on a **6-week timeline** as the optimal compromise between Opus's 9-week conservatism and Haiku's 4-week aggression.

**Key architectural decisions:**

- Stateless `AuthService` facade orchestrating `PasswordHasher`, `TokenManager`, `UserRepo` via constructor dependency injection
- RS256 JWT access tokens (15-min TTL) + opaque Redis-stored refresh tokens (7-day TTL)
- bcrypt cost factor 12 via `PasswordHasher` abstraction (future-proofs for argon2id migration)
- Feature-flag-gated rollout (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) with automatic rollback criteria
- Dual security gate: end-of-Phase-1 checkpoint + pre-GA penetration testing

**Scope:** 5 functional requirements (FR-AUTH-001 through FR-AUTH-005), 8 non-functional requirements, 7 API endpoints (including logout per GAP-002 and admin audit query per GAP-003), 9 components (5 backend, 4 frontend), 3-phase rollout with post-GA stabilization.

**Critical gaps requiring resolution before implementation:**

| Gap ID | Gap | Resolution |
|--------|-----|-----------|
| GAP-001 | Audit log retention conflict (TDD 90-day vs PRD 12-month) | 12-month per PRD/SOC2 — overrides TDD |
| GAP-002 | Logout endpoint missing from TDD | Add POST `/auth/logout` — in-scope per PRD AUTH-E1 |
| GAP-003 | Admin audit log query API missing | Add GET `/admin/auth/audit-logs` — persona Jordan requirement |
| GAP-004 | GDPR consent field missing from `UserProfile` | Add `consent_given` + `consent_timestamp` fields |
| GAP-005 | Password reset endpoint schemas incomplete | Finalize request/response schemas before implementation |

**Persona coverage:** Alex (end user) — core login/register/reset flows in Phases 1–2; Sam (API consumer) — programmatic token management in Phase 1 (implementation) and Phase 2 (production exercise); Jordan (platform admin) — audit log query API in Phase 2, compliance validation tools.

---

## Phased Implementation Plan

### Phase 1: Core Authentication — Internal Alpha (Weeks 1–2)

**Objective:** Deliver registration, login, logout, and token infrastructure to staging. Implement all backend components and frontend pages. Conduct security checkpoint review. Gate production exposure behind feature flags.

**PRD Alignment:** Epics AUTH-E1 (login, registration, logout) and AUTH-E2 (token issuance — implementation only, production exercise deferred to Phase 2). Personas Alex (core flows) and Sam (token contract).

**Scope change from base variant (Haiku):** Password reset (FR-AUTH-005) moved to Phase 2 per Opus's progressive delivery argument — reduces Phase 1 blast radius. Token refresh is implemented and tested in staging but gated in production via `AUTH_TOKEN_REFRESH=OFF`.

#### 1.1 Infrastructure Provisioning (Day 1)

1. Provision PostgreSQL 15+ with `UserProfile` table schema including:
   - All fields per data model (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles)
   - GDPR consent fields (`consent_given` boolean, `consent_timestamp` ISO 8601) — resolves GAP-004
   - Audit log table with **12-month retention policy** — resolves GAP-001
   - Password hash column (bcrypt, not part of `UserProfile` interface)
2. Provision Redis 7+ cluster for refresh token storage (1 GB initial, HPA at 70%)
3. Configure feature flag infrastructure for `AUTH_NEW_LOGIN` (OFF) and `AUTH_TOKEN_REFRESH` (OFF)
4. Generate RS256 2048-bit RSA key pair for `JwtService`; mount as Kubernetes secrets
5. Set up Docker Compose for local dev (PostgreSQL + Redis containers)

**Dependencies:** INFRA-DB-001 (database provisioning), SEC-POLICY-001 (key management policy)

#### 1.2 Backend Core Components (Days 1–4)

| Task | Component | Requirement | Detail |
|------|-----------|-------------|--------|
| Implement `PasswordHasher` | `PasswordHasher` | NFR-SEC-001 | bcrypt with cost factor 12. Abstract interface for future algorithm migration. Unit tests: hash/verify operations, timing invariance. |
| Implement `JwtService` | `JwtService` | NFR-SEC-002 | RS256 sign/verify with 2048-bit RSA. 5-second clock skew tolerance. Configuration validation test. |
| Implement `TokenManager` | `TokenManager` | FR-AUTH-003 | Token issuance (access 15-min + refresh 7-day). Refresh token hashed before Redis storage. Revocation support. |
| Implement `UserRepo` | `UserRepo` | FR-AUTH-002 | CRUD operations against PostgreSQL. Email uniqueness enforcement. Lowercase normalization. |
| Implement `AuthService` facade | `AuthService` | FR-AUTH-001, FR-AUTH-002 | Orchestrates login, registration, logout, and token flows. Delegates to `PasswordHasher`, `TokenManager`, `UserRepo`. |
| Implement logout | `AuthService` | GAP-002 | POST `/auth/logout` — revoke refresh token in Redis, clear HttpOnly cookie. |

**Wiring Task 1.2.1: `AuthService` Facade Dispatch**

- **Mechanism:** Constructor dependency injection
- **Wired Components:** `PasswordHasher`, `TokenManager`, `UserRepo` injected into `AuthService`
- **Cross-Reference:** FR-AUTH-001 (login), FR-AUTH-002 (registration), FR-AUTH-003 (token issuance)
- **Consumers:** All API endpoint handlers (Phases 1–3)

**Wiring Task 1.2.2: Password Hashing Strategy Registry**

- **Mechanism:** `PasswordHasher` abstraction with pluggable strategy
- **Wired Components:** bcryptjs implementation (cost 12); future argon2id slot reserved
- **Cross-Reference:** FR-AUTH-001, FR-AUTH-002, FR-AUTH-005
- **Implementation Detail:** Default bcryptjs. Migration to argon2id requires no API changes.

**Wiring Task 1.2.3: Token Dispatch Table**

- **Mechanism:** `TokenManager` internal routing for token type handling
- **Wired Components:** Access token flow → `JwtService.sign()`, refresh token flow → Redis storage with TTL
- **Cross-Reference:** FR-AUTH-003 (token issuance and refresh)

**Wiring Task 1.2.4: Account Lockout Strategy**

- **Mechanism:** Failed attempt counter in Redis with 15-minute TTL per IP/email
- **Wired Components:** `AuthService.login()` increments counter; 6th attempt within 15 minutes triggers 423 Locked
- **Cross-Reference:** FR-AUTH-001 AC #4

#### 1.3 API Endpoints — Core (Days 2–5)

| Endpoint | Requirement | Key Behaviors |
|----------|-------------|---------------|
| POST `/auth/login` | FR-AUTH-001 | Valid creds → 200 + `AuthToken`. Invalid → 401 (no enumeration). Lockout after 5 failures in 15 min → 423. Rate limit: 10 req/min per IP. |
| POST `/auth/register` | FR-AUTH-002 | Valid → 201 + `UserProfile`. Duplicate email → 409. Weak password → 400. GDPR consent required in request body (GAP-004). |
| POST `/auth/refresh` | FR-AUTH-003 | Valid refresh token → 200 + new `AuthToken` pair. Old refresh token revoked. Expired → 401. Rate limit: 30 req/min per user. Gated behind `AUTH_TOKEN_REFRESH` flag. |
| GET `/auth/me` | FR-AUTH-004 | Valid accessToken → 200 + `UserProfile`. Invalid/expired → 401. Rate limit: 60 req/min per user. |
| POST `/auth/logout` | GAP-002 | Revoke refresh token in Redis. Clear HttpOnly cookie. Return 200. |

#### 1.4 Audit Logging Foundation (Days 2–3)

1. Implement structured audit log writer (user_id, event_type, timestamp, ip_address, outcome, details JSON)
2. Configure **12-month retention** per NFR-COMP-002 (GAP-001 resolution)
3. Log all auth events: login success/failure, registration, token refresh, logout, lockout
4. Wire OpenTelemetry spans: `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`

**Wiring Task 1.4.1: Audit Log Callback Chain**

- **Mechanism:** Synchronous post-operation callback in `AuthService`
- **Wired Components:** Each auth flow endpoint triggers audit log write
- **Cross-Reference:** NFR-COMP-002, GAP-003 (query API in Phase 2)
- **Implementation Detail:** One callback per auth operation. Logging does not block response. Schema: user_id, event_type, timestamp, ip_address, outcome, details (JSON). 12-month retention.

#### 1.5 Frontend Implementation (Days 1–5, parallel with backend)

| Task | Component | Detail |
|------|-----------|--------|
| Implement `LoginPage` | `LoginPage` | Email/password form. Calls POST `/auth/login`. Inline validation. Generic error on failure (no enumeration). CAPTCHA after 3 failures (R-002 mitigation). |
| Implement `RegisterPage` | `RegisterPage` | Email/password/displayName form. Client-side password policy validation. GDPR consent checkbox (GAP-004). Calls POST `/auth/register`. |
| Implement `AuthProvider` | `AuthProvider` | Context provider managing `AuthToken` state. accessToken in memory only (R-001 mitigation). HttpOnly cookie for refreshToken. 401 interceptor with silent refresh handler. |
| Implement `ProfilePage` | `ProfilePage` | Displays user profile from GET `/auth/me`. |
| Route protection | Router config | `/login` → `LoginPage`, `/register` → `RegisterPage`, `/profile` → `ProfilePage` (protected). |

**Wiring Task 1.5.1: Silent Token Refresh Middleware Chain**

- **Mechanism:** HTTP client interceptor in `AuthProvider`
- **Wired Components:** Detects 401 → calls POST `/auth/refresh` → retries original request → updates context
- **Cross-Reference:** FR-AUTH-003, JTBD-2 (session persistence)
- **Implementation Detail:** Idempotent retry. Expired refresh token triggers logout redirect.

**Wiring Task 1.5.2: Feature Flag Registry**

- **Mechanism:** Feature flag service (LaunchDarkly or in-house)
- **Wired Components:** `AUTH_NEW_LOGIN` gates login/register traffic routing; `AUTH_TOKEN_REFRESH` gates refresh endpoint availability
- **Cross-Reference:** Rollout phasing (Phase 1 Alpha → Phase 2 Beta → Phase 3 GA)
- **Implementation Detail:** Flags loaded from environment or polling store. Changes do not require restart. Default OFF for both.

#### 1.6 API Gateway and Rate Limiting (Day 4)

| Task | Deliverable | Acceptance |
|------|-------------|-----------|
| Configure rate limiting | Per-endpoint limits (login: 10/min/IP, register: 5/min/IP, refresh: 30/min/user, me: 60/min/user, logout: 60/min/user) | Staging test: limits enforced, 429 returned |
| Configure CORS | Allow frontend origin; disallow cross-origin token access | Staging test: CORS headers present, preflight passes |

#### 1.7 Monitoring and Observability (Days 3–4, parallel)

| Artifact | Details |
|----------|---------|
| Prometheus metrics | `auth_login_total`, `auth_login_duration_seconds`, `auth_registration_total`, `auth_token_refresh_total` |
| OpenTelemetry traces | Spans from API entry through `PasswordHasher` → `TokenManager` → `JwtService` |
| Structured logging | All auth events logged, searchable by user_id and event_type |
| Grafana dashboards | Login latency p95, error rate, concurrent requests, Redis memory usage |

#### 1.8 Security Checkpoint Review (Days 8–9)

Per debate convergence: early security checkpoint catches crypto implementation bugs when they are cheapest to fix.

1. Security code review of `PasswordHasher`, `JwtService`, `TokenManager` implementations
2. Validate bcrypt cost factor 12 timing invariance
3. Verify HttpOnly cookie configuration for refreshToken
4. Review `JwtService` clock skew handling
5. Validate no plaintext passwords in logs or database
6. **Finding remediation window:** Days 9–10 if issues found

#### 1.9 Manual Testing and Bug Fix (Days 8–10)

| Test Scenario | Success Criteria |
|---------------|------------------|
| Registration (valid data) | Account created, user logged in, redirected to dashboard |
| Registration (duplicate email) | 409 error, user NOT created, helpful message |
| Registration (weak password) | 400 error, inline validation feedback |
| Registration (no GDPR consent) | 400 error, consent required |
| Login (valid credentials) | 200 OK, `AuthToken` returned, token stored via `AuthProvider` |
| Login (invalid credentials) | 401 error, no user enumeration |
| Login (5 failed attempts) | Account locked, 423 response |
| Token refresh (valid) | 200 OK, new `AuthToken` pair, old token revoked |
| Token refresh (expired) | 401 error, user prompted to re-login |
| Profile retrieval (authenticated) | GET `/auth/me` returns full `UserProfile` |
| Profile retrieval (unauthenticated) | 401 error |
| Session persistence (page refresh) | `AuthProvider` silently refreshes; no re-login prompt |
| Logout | Refresh token revoked, cookie cleared, redirect to landing |
| Audit logging (login success) | Audit log entry with user_id, timestamp, IP, outcome |

#### Phase 1 Exit Criteria

- [ ] FR-AUTH-001 acceptance criteria 1–4 pass (login, invalid creds, no enumeration, lockout)
- [ ] FR-AUTH-002 acceptance criteria 1–4 pass (registration, duplicate, weak password, bcrypt)
- [ ] FR-AUTH-003 token issuance and refresh pass in staging (gated in production)
- [ ] FR-AUTH-004 profile retrieval pass
- [ ] Logout endpoint functional (GAP-002 resolved)
- [ ] GDPR consent captured at registration (GAP-004 resolved)
- [ ] Password reset schemas finalized (GAP-005 resolved — implementation in Phase 2)
- [ ] NFR-SEC-001 validated (bcrypt cost 12 unit test + security review)
- [ ] NFR-SEC-002 validated (RS256 config test + security review)
- [ ] NFR-COMP-001 validated (GDPR consent field stored with timestamp)
- [ ] NFR-COMP-002 foundation: audit log operational with 12-month retention configured
- [ ] Unit test coverage ≥ 80% on all backend components
- [ ] Integration tests pass: registration → DB, login → token, refresh → rotation, logout → revocation
- [ ] Security checkpoint complete with findings remediated
- [ ] Feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` both OFF by default
- [ ] Zero P0/P1 bugs in staging

---

### Phase 2: Password Reset, Compliance, and Beta (Weeks 3–4)

**Objective:** Implement password reset flow. Deploy admin audit log query API. Deploy to production at 10% traffic. Validate NFRs under production load. Complete compliance pre-audit preparation.

**PRD Alignment:** Completes AUTH-E2 (token refresh exercised in production), AUTH-E3 (password reset, admin audit logs). Migration Phase 1 (Internal Alpha) and Phase 2 (Beta 10%). Persona Jordan's audit needs addressed.

**Scope change from base variant (Haiku):** Password reset moved here from Phase 1 — built on stable `AuthService` foundation with adequate testing time (debate compromise). Admin audit query API retained in Phase 2 per Haiku's compliance-forward phasing.

#### 2.1 Password Reset Implementation (Days 1–3)

| Endpoint | Requirement | Key Behaviors |
|----------|-------------|---------------|
| POST `/auth/reset-request` | FR-AUTH-005 | Email in body. Sends reset token via SendGrid. Same response regardless of registration (no enumeration). Token: 1-hour TTL, single-use. |
| POST `/auth/reset-confirm` | FR-AUTH-005 | Token + new password in body. Validates token, updates password hash via `PasswordHasher`. Invalidates all refresh tokens. |

- Email delivery: async (queue-based) for resilience — recommended resolution for OQ-PRD-001
- Implement email delivery monitoring and alerting (R-007 mitigation)
- Implement fallback support channel documentation for email delivery failures
- Audit log: record password reset request and confirmation events

**Wiring Task 2.1.1: SendGrid Email Service Integration**

- **Mechanism:** External API client via async queue
- **Wired Components:** `AuthService.resetRequest()` → email queue → SendGrid API
- **Cross-Reference:** FR-AUTH-005, OQ-PRD-001
- **Implementation Detail:** Queue-based for resilience. Delivery monitoring via SendGrid webhooks.

#### 2.2 Admin Audit Log Query API (Days 2–3) — GAP-003 Resolution

| Endpoint | Requirement | Key Behaviors |
|----------|-------------|---------------|
| GET `/admin/auth/audit-logs` | GAP-003 / PRD AUTH-E3 | Queryable by date range, user_id, event type. Protected by admin role authorization. Rate limit: 10 req/min. |

- Validates NFR-COMP-002 (SOC2 audit logging) end-to-end
- Addresses persona Jordan's primary need: "view authentication event logs for incident investigation and auditors"
- Query performance target: < 1 second for typical auditor query

#### 2.3 Compliance and Audit Readiness (Days 3–5)

| Task | Owner | Acceptance |
|------|-------|-----------|
| Audit log verification | security-team | Spot-check 100 entries: all fields present, 12-month retention confirmed |
| GDPR consent tracking | legal-team | Consent field present on registration, timestamp recorded (GAP-004 validation) |
| SOC2 control validation | security-team | Audit log queryable via admin API, retention policy enforced, sample report generated |
| Admin audit query validation | compliance-team | Jordan persona can query by date range, user_id, event type with < 1s response |

#### 2.4 Production Deployment and Internal Alpha (Days 3–5)

1. Deploy `AuthService` and all dependencies to production with `AUTH_NEW_LOGIN=OFF`
2. auth-team and QA manually test all endpoints against production PostgreSQL and Redis
3. Run integration test suite against production infrastructure
4. Validate observability stack: metrics, dashboards, alerts, traces operational in production

#### 2.5 Beta 10% Traffic Shift (Days 5–14)

1. Enable `AUTH_NEW_LOGIN` for 10% of production traffic (user ID hash for consistent routing)
2. Monitor continuously:
   - p95 latency < 200ms (NFR-PERF-001)
   - Error rate < 0.1%
   - Redis connection health
   - Registration conversion funnel (target > 60%)
   - Password reset completion funnel (target > 80%)

**Alert Thresholds:**

| Metric | Alert Threshold | Action |
|--------|-----------------|--------|
| `auth_login_duration_seconds` p95 | > 500ms | Page on-call, investigate |
| `auth_login_total` error rate | > 5% for 2 minutes | Page on-call |
| Redis connection failures | > 10/minute | Page on-call, check cluster |
| PostgreSQL pool exhaustion | > 80% utilized | Page on-call, check for leaks |
| Brute-force detected (rate limit > 1000x) | True | Page security-team, WAF blocking |

**Automatic Rollback Triggers:**

- p95 latency > 1000ms for > 5 minutes
- Error rate > 5% for > 2 minutes
- Redis connection failures > 10/minute
- Any `UserProfile` data corruption

**Rollback Procedure:**
1. Disable `AUTH_NEW_LOGIN` → 100% traffic to legacy auth
2. Verify legacy login operational via smoke tests
3. Investigate root cause in logs/traces
4. If data corruption: restore PostgreSQL and Redis from pre-deployment backup
5. Post-mortem within 48 hours

#### 2.6 Load Testing and Performance Validation (Days 6–10, parallel with beta monitoring)

| Test | Load | Success Criteria | Tool |
|------|------|------------------|------|
| Concurrent login | 500 concurrent | p95 < 200ms; error rate < 0.1% | k6 |
| Sustained traffic | 100 req/sec for 10 min | p95 < 200ms; no pool exhaustion | k6 |
| Token refresh under load | 200 concurrent | p95 < 100ms; TTL respected | k6 |
| DB connection limits | 500 concurrent login + profile | No connection timeouts | k6 + Postgres monitoring |
| Password reset flow | 50 concurrent | Email queued within 2s; reset completes | k6 |

#### 2.7 Performance Tuning (Days 10–14, if needed)

| Bottleneck | Mitigation |
|-----------|-----------|
| `PasswordHasher` slow (bcrypt cost 12 > 500ms) | Reduce cost to 11; profile CPU; validate timing invariance |
| `TokenManager` Redis latency | Increase replica count; enable read-from-replica |
| `UserRepo` query latency | Add database index on email; profile query plans |

#### Phase 2 Exit Criteria

- [ ] FR-AUTH-005 acceptance criteria 1–4 pass (reset request, confirm, expiry, single-use)
- [ ] GAP-003 resolved: admin audit log query API operational and validated by compliance team
- [ ] NFR-PERF-001 validated in production (p95 < 200ms on all endpoints)
- [ ] NFR-PERF-002 validated (500 concurrent login load test passes)
- [ ] NFR-COMP-002 validated end-to-end (audit logs queryable, 12-month retention verified)
- [ ] 7-day beta monitoring window: 99.9% uptime, error rate < 0.1%
- [ ] Zero data corruption incidents
- [ ] E2E test passes: register → login → profile → refresh → logout → password reset
- [ ] Compliance pre-audit preparation complete: sample reports generated

---

### Phase 3: GA Rollout and Stabilization (Weeks 5–6)

**Objective:** Ramp to 100% production traffic. Execute pre-GA penetration testing. Remove feature flags. Deprecate legacy auth. Establish on-call rotation. Validate all success metrics.

**PRD Alignment:** Migration Phase 3 (GA 100%). Completes all PRD scope. Post-GA stabilization per Opus's recommendation.

#### 3.1 Pre-GA Security Gate (Days 1–3)

Per debate convergence: consolidated pre-GA security gate complements the Phase 1 checkpoint.

1. **Penetration testing** by external firm (R-005 mitigation)
   - Focus areas: XSS token theft (R-001), brute force (R-002), user enumeration, password reset token security
2. Security review of any code changed since Phase 1 checkpoint (token refresh production flow, password reset, admin API)
3. Validate NIST SP 800-63B password policy compliance
4. Verify NFR-COMP-003 (data minimization): only email, hashed password, displayName collected
5. Confirm HttpOnly cookie configuration across all supported browsers
6. **Finding remediation:** Days 3–4 if critical/high findings

#### 3.2 Traffic Ramp to GA (Days 3–5)

| Task | Details | Acceptance |
|------|---------|-----------|
| Increase `AUTH_NEW_LOGIN` to 50% | Gradual ramp, monitor error rate and latency | Stable for 8 hours |
| Increase `AUTH_NEW_LOGIN` to 100% | All traffic to `AuthService` | Smoke test passes, zero errors for 1 hour |
| Enable `AUTH_TOKEN_REFRESH` | Refresh tokens fully functional for all users | POST `/auth/refresh` success rate > 99% |

#### 3.3 Legacy Auth Deprecation (Days 5–7)

| Task | Details |
|------|---------|
| Announce deprecation | Public communication: legacy endpoint deprecated after 30 days |
| Redirect legacy traffic | Legacy `/v0/auth/login` returns 301 → `/v1/auth/login` |
| Remove legacy code | Delete legacy `AuthService` and related components; code review approved |

#### 3.4 Feature Flag Cleanup

| Flag | Cleanup Schedule |
|------|-----------------|
| `AUTH_NEW_LOGIN` | Remove at GA (Day 5) |
| `AUTH_TOKEN_REFRESH` | Remove at GA + 2 weeks |

#### 3.5 Runbook Validation and On-Call Setup (Days 5–7)

| Task | Details | Acceptance |
|------|---------|-----------|
| Validate runbooks | Dry-run: `AuthService` down, token refresh failures, Redis down | All runbooks executable, completion time < 15 min |
| On-call handoff | 24/7 on-call rotation for first 2 weeks post-GA | auth-team confirmed, escalation paths clear |
| Capacity planning | Verify pod count, pool sizes, Redis memory handle peak projections | Scaling triggers defined and tested |

#### 3.6 Success Metrics Baseline (Days 6–7)

| Metric | Baseline Action | Target |
|--------|----------------|--------|
| Daily active authenticated users | Establish Day 1 baseline | > 1000 within 30 days |
| Registration conversion rate | Establish baseline | > 60% within 30 days |
| Login response time (p95) | Record from Phase 2 | < 200ms sustained |
| Service availability | Record from Phase 2 | 99.9% rolling 30-day |
| Failed login rate | Record from Phase 2 | < 5% |
| Password reset completion | Establish baseline | > 80% within 14 days |
| Average session duration | Establish baseline | > 30 minutes within 7 days |

#### 3.7 Documentation and Knowledge Transfer (Days 5–10)

| Deliverable | Audience |
|-------------|----------|
| Operations runbook | On-call engineers |
| API documentation (OpenAPI spec) | Developers, API consumers (persona Sam) |
| Troubleshooting guide | Support team, auth-team |
| Architecture decision record (ADR) | Future maintainers |

#### 3.8 Post-GA Stabilization (Week 6)

Per Opus's recommendation: explicit stabilization period prevents premature handoff.

1. 24/7 on-call rotation active for auth-team
2. Continuous metric validation against success criteria
3. Remove `AUTH_TOKEN_REFRESH` flag at GA + 2 weeks
4. Post-mortem if any P0/P1 incidents occurred
5. Validate 99.9% uptime over 7 consecutive days (NFR-REL-001)
6. Finalize all dashboards and alerting thresholds based on production data

#### Phase 3 Exit Criteria

- [ ] Penetration test complete with no critical or high findings unresolved
- [ ] 100% traffic on new `AuthService` for 7+ days
- [ ] Legacy auth fully deprecated and code removed
- [ ] Feature flags cleaned up (`AUTH_NEW_LOGIN` removed; `AUTH_TOKEN_REFRESH` removal scheduled)
- [ ] 99.9% uptime over 7 consecutive days
- [ ] On-call rotation established and acknowledged
- [ ] 48-hour post-GA window: zero P0 incidents
- [ ] All runbooks validated
- [ ] Success metrics baselines established
- [ ] Documentation published: runbooks, API docs, troubleshooting guide, ADR

---

## Integration Points and Wiring Summary

### Dispatch Tables and Registries

| Artifact | Components | Phase | Validation |
|----------|-----------|-------|-----------|
| Password Hashing Strategy | `PasswordHasher` (bcryptjs cost 12) + future argon2id slot | 1 | Unit test: hash/verify operations |
| Token Dispatch | `TokenManager` routes to JWT (access) vs Redis (refresh) | 1 | Integration test: both paths exercise |
| Feature Flag Registry | `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH` + traffic router | 1 | Staging test: traffic splits correctly |
| Rate Limiting Rules | Per-endpoint limits at API Gateway | 1 | Load test: limits enforced, 429 returned |
| Account Lockout Strategy | Failed attempt counter with 15-min Redis TTL | 1 | Unit test: counter increments, lockout at 5 |
| Audit Log Callback Chain | Post-operation callbacks writing structured events | 1 | Integration test: all auth events logged |
| Silent Refresh Middleware | HTTP interceptor → 401 → refresh → retry | 1 | Component test: chain executes end-to-end |
| Error Response Dispatch | Error codes mapped to HTTP status (401, 409, 423, 429) | 1 | API test: all endpoints return correct codes |
| CORS Middleware | Allowed origins configuration | 1 | Staging test: headers present, preflight passes |
| SendGrid Email Integration | `AuthService.resetRequest()` → queue → SendGrid API | 2 | Integration test: email queued and delivered |

### Dependency Injection Configuration

| Component | Injected Dependencies | Configuration Source |
|-----------|----------------------|----------------------|
| `AuthService` | `PasswordHasher`, `TokenManager`, `UserRepo` | Constructor injection |
| `TokenManager` | `JwtService`, Redis client | Constructor injection |
| `UserRepo` | PostgreSQL connection pool | Constructor injection |
| `JwtService` | RS256 private/public key pair | Environment + secret store |
| `PasswordHasher` | bcryptjs cost factor (12) | Configuration file or environment |
| `AuthProvider` (frontend) | API base URL, token storage mechanism | Context props |

### Feature Flag Integration Matrix

| Flag | Service Boundary | Check Location | ON Behavior | OFF Behavior | Phases Active |
|------|-----------------|----------------|-------------|--------------|---------------|
| `AUTH_NEW_LOGIN` | Router → `AuthService` vs legacy | API Gateway | Route to new service | Route to legacy | 1 (OFF), 2 (10%), 3 (100% → removed) |
| `AUTH_TOKEN_REFRESH` | `TokenManager` refresh endpoint | TokenManager init | Expose POST `/auth/refresh` | 404 | 1 (OFF), 2 (OFF in prod), 3 (ON → removed) |

### Callback Chain: Audit Logging

1. User calls auth endpoint (login, register, refresh, logout, reset)
2. `AuthService` executes the operation
3. On completion (success or failure), `AuditLogger.log()` callback fires synchronously
4. Log entry written to PostgreSQL: `{ user_id, event_type, timestamp, ip_address, outcome, details }`
5. Retention policy: 12 months (PRD requirement, overrides TDD 90-day)
6. Phase 2: admin query API exposes these logs to persona Jordan

---

## Risk Assessment and Mitigation

### Technical Risks

| ID | Risk | Prob. | Impact | Phase | Mitigation | Contingency |
|----|------|-------|--------|-------|------------|-------------|
| R-001 | Token theft via XSS → session hijacking | Medium | High | 1 | accessToken in memory only; HttpOnly cookie for refreshToken; 15-min access TTL; CSP headers | Immediate revocation via `TokenManager`; force password reset for affected accounts |
| R-002 | Brute-force login attacks | High | Medium | 1 | Rate limit 10 req/min/IP; lockout after 5 failures in 15 min; bcrypt cost 12; CAPTCHA after 3 failures | WAF IP blocking; SMS alert for admin on lockout spike |
| R-003 | Data loss during legacy auth migration | Low | High | 3 | Parallel run during Phases 1–2; idempotent upserts; full DB backup before each phase | Rollback to legacy; restore from pre-migration backup within 30 minutes |
| R-005 | Security breach from implementation flaws | Low | Critical | 1, 3 | Phase 1 security checkpoint + Phase 3 penetration testing (dual-gate) | Incident response; emergency patch; forced password reset; public disclosure within 48 hours |

### Business and Product Risks

| ID | Risk | Prob. | Impact | Phase | Mitigation |
|----|------|-------|--------|-------|------------|
| R-004 | Low registration adoption (poor UX) | Medium | High | 2–3 | Usability testing before beta; A/B test registration form; iterate based on funnel data. Extend beta by 1 week if conversion < 40%. |
| R-006 | Compliance failure (incomplete audit logging) | Medium | High | 1–2 | Define 12-month retention early (Phase 1); validate with admin query API in Phase 2; SOC2 pre-audit review in Phase 2 |
| R-007 | Email delivery failures blocking password reset | Low | Medium | 2 | SendGrid delivery monitoring + alerting; fallback support channel; weekly test of reset flow |

### Architectural Risks

| Risk | Prob. | Impact | Mitigation |
|------|-------|--------|------------|
| Redis single point of failure | Medium | High | Redis cluster with replication; graceful degradation (users re-login if unavailable) |
| RSA key compromise | Low | Critical | Keys in Kubernetes secrets with RBAC; quarterly rotation; revocation procedure documented |

### Risk Mitigation Roadmap

**Immediate (Phase 1):**
- R-001: CSP headers + memory-only accessToken + HttpOnly cookies
- R-002: Rate limiting + account lockout wired
- R-003: DB backup automation set up and tested
- R-005: Security checkpoint review of crypto components
- R-006: Audit log schema finalized, 12-month retention configured

**Pre-Beta (End of Phase 1):**
- R-002: CAPTCHA integration tested
- R-004: Usability testing of `RegisterPage` with 10 users
- R-005: Penetration testing engagement scoped

**Pre-GA (Phases 2–3):**
- R-004: A/B testing results analyzed; conversion rate decision gate
- R-005: Pentest findings remediated; security sign-off obtained
- R-006: SOC2 pre-audit review completed
- R-007: SendGrid alerting configured; fallback documentation published

---

## Resource Requirements and Dependencies

### Team Composition

| Role | Count | Allocation | Phase Coverage | Key Responsibilities |
|------|-------|-----------|----------------|---------------------|
| Backend Engineer (auth-team) | 2 | 100% | Phases 1–3 | `AuthService`, `TokenManager`, `PasswordHasher`, `JwtService`, `UserRepo`, API endpoints, password reset |
| Frontend Engineer | 1 | 100% (P1–2), 50% (P3) | Phases 1–3 | `LoginPage`, `RegisterPage`, `AuthProvider`, `ProfilePage`, protected routes |
| DevOps Engineer | 1 | 50% | Phases 1–3 | Infrastructure, feature flags, deployment, monitoring, on-call setup |
| QA Engineer | 1 | 100% | Phases 1–3 | Manual testing, load testing (k6), E2E automation, runbook validation |
| Security Engineer | 0.5 | 50% | Phases 1, 3 | Phase 1 checkpoint review, Phase 3 pentest coordination, audit log validation |
| Product Manager | 0.25 | 25% | Phases 1–3 | Metrics definition, business value tracking, UX iteration decisions |
| Compliance Officer | 0.25 | 25% | Phases 1–2 | Audit logging verification, SOC2 alignment, GDPR consent tracking |

**Peak Staffing:** 6 FTE during Phase 1 (full implementation); 5 FTE during Phase 2 (beta + password reset); 3 FTE during Phase 3 (GA + stabilization).

### Infrastructure Dependencies

| Dependency | Version | Purpose | Impact if Unavailable | Procurement Timeline |
|-----------|---------|---------|----------------------|----------------------|
| PostgreSQL | 15+ | `UserProfile` persistence, audit log | Service non-functional | Pre-Phase 1 (INFRA-DB-001) |
| Redis | 7+ | Refresh token storage, lockout counter | Token refresh disabled; lockout bypassed | Pre-Phase 1 |
| Node.js LTS | 20 | `AuthService` runtime | Service cannot run | Pre-Phase 1 |
| SendGrid API | — | Password reset emails | FR-AUTH-005 blocked | Pre-Phase 2 (API key provisioned) |
| Feature flag service | — | Traffic routing and gating | Hardcoded flags fallback | Pre-Phase 1 |
| RSA key pair (2048-bit) | — | JWT signing | Token issuance impossible | Pre-Phase 1 (SEC-POLICY-001) |
| Frontend routing framework | — | Client-side routing + token auth | Auth pages cannot render | Pre-Phase 1 |

### Third-Party Cost Estimates

| Service | Provider | Purpose | Estimated Cost | SLA |
|---------|----------|---------|---------------|-----|
| Email delivery | SendGrid | Password reset | ~$100/month at scale | 99.9% |
| Feature flags | LaunchDarkly (or in-house) | Traffic routing | $0 (in-house) or $200+/month | — |
| Error tracking | Sentry (optional) | Error monitoring | $100+/month | — |
| APM | DataDog/New Relic (optional) | Performance monitoring | $200+/month | — |

### Library Dependencies

| Library | Version | Component | Phase |
|---------|---------|-----------|-------|
| bcryptjs | Latest stable | `PasswordHasher` | 1 |
| jsonwebtoken | Latest stable | `JwtService` | 1 |

### Document Dependencies

| Document | Type | Required Resolution |
|----------|------|---------------------|
| AUTH-PRD-001 | Upstream requirements | Active (this roadmap) |
| INFRA-DB-001 | Database provisioning | Must be complete before Phase 1 |
| SEC-POLICY-001 | Security policy | Must be available for key management |
| COMPLIANCE-001 | SOC2/GDPR requirements | Pending review — needed for Phase 2 compliance validation |

---

## Success Criteria and Validation Approach

### Technical Validation

#### NFR-PERF-001: API Response Time (< 200ms p95)

**Measurement Method:** APM instrumentation on `AuthService.login()`, `TokenManager.refresh()`, `UserRepo.getById()`. Trace all HTTP requests end-to-end. Capture p50, p95, p99.

| Phase | Target | Validation | Tool |
|-------|--------|-----------|------|
| Alpha (Staging) | < 200ms p95 | Manual load test, 100 concurrent | APM dashboard |
| Beta (10% prod) | < 200ms p95 sustained | k6: 500 concurrent logins, sustained 10 min | APM + k6 |
| GA | < 200ms p95 sustained | Ongoing monitoring; alert if > 500ms for 5 min | APM dashboard |

**Success Definition:** p95 latency < 200ms throughout Phase 2 beta monitoring window under production load.

#### NFR-PERF-002: Concurrent Authentication (500 concurrent logins)

**Measurement Method:** k6 load test: 500 concurrent login requests, sustained for 10 minutes. Measure: success rate, latency distribution, error rate, DB pool utilization.

**Success Definition:** 0% error rate, p95 < 200ms, no connection pool exhaustion.

#### NFR-REL-001: Service Availability (99.9% uptime)

**Measurement Method:** GET `/auth/health` endpoint (checks `AuthService`, PostgreSQL, Redis). Prometheus scrapes every 30 seconds.

| Phase | Target | Window |
|-------|--------|--------|
| Beta | 99.9% | 7-day |
| GA | 99.9% | 30-day rolling |

**Success Definition:** 99.9% uptime for 7 consecutive days during Phase 2 beta and sustained post-GA.

#### NFR-SEC-001: Password Hashing (bcrypt cost factor 12)

**Measurement Method:** Unit test verifies bcrypt cost parameter in resulting hash. Benchmark: hash time < 500ms.

#### NFR-SEC-002: Token Signing (RS256 with 2048-bit RSA)

**Measurement Method:** Unit test verifies JWT header `alg = "RS256"`. Configuration test verifies key size ≥ 2048 bits.

#### NFR-COMP-001: GDPR Consent at Registration

**Measurement Method:** Integration test asserts `consent_given` and `consent_timestamp` stored on registration. Registration form requires consent checkbox.

#### NFR-COMP-002: SOC2 Audit Logging (12-month retention)

**Measurement Method:** Audit log table with required columns. Admin query API (Phase 2) returns events queryable by user_id, date range, event type. Retention policy deletes records > 12 months. Query performance < 1 second.

**Success Definition:** SOC2 pre-audit review in Phase 2 confirms compliance.

#### NFR-COMP-003: GDPR Data Minimization

**Measurement Method:** Schema review confirms only email, hashed password, displayName collected. Compliance team approval.

### Business Validation

| Metric | Target | Measurement | Timeline |
|--------|--------|-------------|----------|
| Registration conversion rate | > 60% | Funnel: landing → register → confirmed account | GA + 30 days |
| Daily active authenticated users | > 1000 | Unique users with ≥ 1 auth event per day | GA + 30 days |
| Average session duration | > 30 minutes | Token refresh event analytics | GA + 7 days |
| Failed login rate | < 5% | Auth event log analysis | GA + 14 days |
| Password reset completion | > 80% | Funnel: reset requested → new password set | GA + 14 days |

**Phased targets (relaxed during beta):**

| Metric | Beta Target | GA Target |
|--------|-------------|-----------|
| Registration conversion | > 40% | > 60% |
| Failed login rate | < 10% | < 5% |
| Session duration | > 20 min | > 30 min |
| Reset completion | > 70% | > 80% |

### Test Coverage Targets

| Level | Target | Phase |
|-------|--------|-------|
| Unit | ≥ 80% on all backend components | 1 |
| Integration | All API endpoints with DB + Redis | 1–2 |
| E2E | Full journey: register → login → profile → refresh → logout → reset | 2 |
| Load | 500 concurrent logins (k6) | 2 |
| Security | Phase 1 checkpoint + Phase 3 pentest with zero unresolved critical/high | 1, 3 |

---

## Timeline Summary

| Phase | Duration | Weeks | Key Deliverables | Milestone |
|-------|----------|-------|------------------|-----------|
| **Phase 1: Core Auth + Alpha** | 2 weeks | 1–2 | Login, registration, logout, token infrastructure, profile, `AuthService` facade, all backend components, frontend pages, `AuthProvider`, audit logging, GDPR consent, security checkpoint | M1 |
| **Phase 2: Reset + Beta** | 2 weeks | 3–4 | Password reset (2 endpoints), admin audit query API, compliance validation, production deployment, beta 10% traffic, load testing, 7-day stability monitoring | M2 |
| **Phase 3: GA + Stabilization** | 2 weeks | 5–6 | Pre-GA penetration testing, traffic ramp to 100%, legacy deprecation, feature flag cleanup, runbook validation, on-call rotation, success metrics baseline, post-GA stabilization | M3 |

**Total: 6 weeks to GA (including 1-week post-GA stabilization)**

### Critical Path

```
INFRA-DB-001 + Redis provisioning (pre-Phase 1)
  → PasswordHasher + JwtService + UserRepo (parallel, Days 1–2)
    → TokenManager (depends on JwtService + Redis, Days 2–3)
      → AuthService facade (depends on all services, Days 3–4)
        → API endpoints + frontend (parallel, Days 3–5)
          → Security checkpoint (Days 8–9)
            → Manual testing + bug fix (Days 8–10)
              → Phase 1 exit gate (end of Week 2)
                → Password reset + admin API (Week 3, Days 1–3)
                  → Production deploy + beta 10% (Week 3, Days 3–14)
                    → 7-day stability window (Week 4)
                      → Phase 2 exit gate (end of Week 4)
                        → Pentest + traffic ramp (Week 5)
                          → GA 100% + stabilization (Week 6)
```

### Slack and Risk Analysis

| Phase | Critical Path Days | Slack | Risk Scenario | Time Impact |
|-------|-------------------|-------|---------------|-------------|
| Phase 1 | 10 days | 0.5 days (monitoring setup) | `PasswordHasher` bugs | +1–2 days |
| Phase 2 | 14 days | 0 days (7-day window absolute) | p95 > 500ms under load | +2–3 days tuning |
| Phase 3 | 10 days | 2 days (stabilization buffer) | Pentest critical finding | +2–3 days remediation |

**Conservative estimate:** 6 weeks best-case; 7–8 weeks if P1 bugs, load test failures, or pentest findings require remediation.

---

## Open Questions Requiring Resolution

| ID | Question | Impact | Recommended Resolution | Blocking Phase |
|----|----------|--------|----------------------|----------------|
| OQ-001 | API key auth for service-to-service? | Scope expansion | Defer to v1.1; not blocking core auth | None |
| OQ-002 | Max `UserProfile` roles array length? | Schema constraint | Set to 20; enforce at `UserRepo` layer | Phase 1 |
| OQ-PRD-001 | Sync vs async password reset emails? | Architecture | Async (queue-based) for resilience | Phase 2 |
| OQ-PRD-002 | Max refresh tokens per user? | Redis storage | Set to 10; revoke oldest on overflow | Phase 1 |
| OQ-PRD-003 | "Remember me" extended sessions? | UX | Defer to v1.1; 7-day refresh is sufficient for v1.0 | None |

---

## Gap Resolution Summary

| Gap ID | Gap | Severity | Resolution | Phase | Status |
|--------|-----|----------|-----------|-------|--------|
| GAP-001 | Audit log retention: TDD 90-day vs PRD 12-month | High | Override TDD → 12-month per PRD/SOC2 | Phase 1 (configure), Phase 2 (validate) | Resolved in roadmap |
| GAP-002 | Logout endpoint missing from TDD | Medium | Add POST `/auth/logout` | Phase 1 | Resolved in roadmap |
| GAP-003 | Admin audit log query API missing | Medium | Add GET `/admin/auth/audit-logs` | Phase 2 | Resolved in roadmap |
| GAP-004 | GDPR consent field missing | Medium | Add `consent_given` + `consent_timestamp` to schema and registration | Phase 1 | Resolved in roadmap |
| GAP-005 | Password reset schemas incomplete | Medium | Finalize schemas before implementation | Phase 1 (schema), Phase 2 (implement) | Resolved in roadmap |

---

## API Endpoint Inventory

| # | Method | Path | Auth | Rate Limit | Phase |
|---|--------|------|------|------------|-------|
| 1 | POST | `/auth/login` | No | 10 req/min per IP | 1 |
| 2 | POST | `/auth/register` | No | 5 req/min per IP | 1 |
| 3 | POST | `/auth/refresh` | No (refresh token body) | 30 req/min per user | 1 (impl), 2 (beta) |
| 4 | GET | `/auth/me` | Yes (Bearer) | 60 req/min per user | 1 |
| 5 | POST | `/auth/logout` | Yes (Bearer) | 60 req/min per user | 1 (GAP-002) |
| 6 | POST | `/auth/reset-request` | No | 2 req/min per email | 2 |
| 7 | POST | `/auth/reset-confirm` | No | 5 req/min per token | 2 |
| 8 | GET | `/admin/auth/audit-logs` | Yes (Admin) | 10 req/min | 2 (GAP-003) |
