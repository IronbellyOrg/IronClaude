---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.65
adversarial: true
base_variant: "A (Opus-Architect)"
variant_scores: "A:79 B:74"
convergence_score: 0.62
debate_rounds: 2
generated: "2026-04-03"
generator: "adversarial-merge"
total_phases: 5
total_task_rows: 60
risk_count: 7
open_questions: 10
---

# User Authentication Service — Merged Project Roadmap

## Executive Summary

This roadmap defines a five-phase implementation plan for the User Authentication Service, delivering secure email/password authentication, JWT-based session management, self-service password reset, logout capability, and compliance-ready audit logging. The system serves three personas — Alex (end user), Jordan (platform admin), and Sam (API consumer) — and must meet SOC2 Type II and GDPR compliance requirements before the Q3 2026 audit deadline.

**Business Impact:** Authentication unblocks approximately $2.4M in projected annual revenue from personalization-dependent features planned for Q2–Q3 2026. Not shipping in Q2 means a full-quarter delay to the personalization roadmap and potential SOC2 audit failure in Q3.

**Complexity:** MEDIUM (0.65) — 9 components across 5 domains (backend, security, frontend, testing, devops), 7 API endpoints (including logout), 2 data models, and a 3-phase migration with feature flags.

**Critical path:** Data layer (Phase 1) → Backend services with security hardening (Phase 2) → API surface, frontend, and logout (Phase 3) → Testing and compliance validation (Phase 4) → Migration rollout (Phase 5).

**Key architectural decisions:**

- Stateless JWT with refresh tokens (server-side sessions rejected)
- RS256 signing with quarterly key rotation
- bcrypt cost factor 12 via PasswordHasher abstraction
- Refresh tokens hashed in Redis (not plaintext)
- GDPR consent field proactively added to UserProfile schema (OQ-9 resolved)
- Audit log retention resolved via stakeholder gate before Phase 1 (OQ-6 gated, not assumed)

**Open risks requiring resolution before Phase 1:**

- Audit log retention policy (OQ-6) — must be resolved with compliance team; PRD specifies 12 months but implementation implications are non-trivial and require stakeholder sign-off
- Logout endpoint scoping (OQ-7) — PRD requires it; included in Phase 3 with explicit acceptance criteria

---

## Phase 1: Data Layer and Infrastructure

**Objective:** Establish persistent storage, caching infrastructure, and data models. All subsequent phases depend on this foundation.

**Personas & Value:** Enables platform to track users in log data. Compliance team can begin validating audit logging infrastructure.

**Duration:** 1 week

**Entry criteria:** PostgreSQL 15+ and Redis 7+ provisioned. Node.js 20 LTS runtime available. RSA key pair generated for JWT signing. **OQ-6 (audit log retention) resolved by stakeholder decision.**

**Exit criteria:** Database migrations applied. Connection pooling verified. Redis connectivity confirmed. Schema validated against compliance requirements. Audit log retention policy implemented per stakeholder decision.

| # | ID | Task | Description | Depends On | Acceptance Criteria |
|---|-----|------|-------------|------------|---------------------|
| 1 | DM-001 | Implement UserProfile schema | Create PostgreSQL table with id (UUID v4), email (unique, indexed, lowercase-normalized), displayName, createdAt, updatedAt, lastLoginAt, roles (default ["user"]), passwordHash, consentTimestamp (NFR-COMP-001). | — | Migration runs idempotently. All columns match spec. consentTimestamp field present for GDPR (NOT NULL on new registrations). |
| 2 | DM-002 | Implement AuthToken data structures | Define AuthToken interface (accessToken, refreshToken, expiresIn=900, tokenType="Bearer"). Configure Redis 7 for refresh token storage with 7-day TTL. | — | TypeScript interfaces compile. Redis accepts/retrieves hashed tokens with correct TTL. |
| 3 | NFR-COMP-001 | Add GDPR consent recording | Add consentTimestamp field to UserProfile schema. Ensure registration flow records consent with ISO 8601 timestamp. | DM-001 | Field exists in schema. NOT NULL constraint enforced on new registrations. |
| 4 | NFR-COMP-004 | Validate data minimization | Verify UserProfile collects only email, hashed password, displayName, and consent timestamp. No additional PII columns. | DM-001 | Schema review confirms no extraneous PII fields. |
| 5 | OPS-005 | Configure PostgreSQL connection pooling | Set up pg-pool with 100 initial pool size. Configure connection wait time monitoring (alert threshold: 50ms). | DM-001 | Pool accepts 100 concurrent connections. Monitoring metric emits. |
| 6 | OPS-006 | Configure Redis memory and connectivity | Provision 1 GB Redis instance. Configure memory utilization alerting at 70%. Verify hash storage for refresh tokens. | DM-002 | Redis responds to PING. Memory monitoring active. Hash set/get operations verified. |
| 7 | NFR-COMP-002 | Create audit log table | Create PostgreSQL audit_log table with user_id, event_type, timestamp, ip_address, outcome, and metadata columns. Retention policy per OQ-6 stakeholder decision. Configure partition-based retention policy. | DM-001, OQ-6 resolution | Table created. Partition pruning configured per resolved retention period. Insert/query operations verified. |

### Integration Points — Phase 1

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|----------------|------|-------------------|--------------|-------------|
| PostgreSQL connection pool (pg-pool) | Connection pool | UserRepo (COMP-005), audit log writer | Phase 1 | Phase 2 (COMP-005), Phase 4 (TEST-004) |
| Redis connection | Cache/store | TokenManager (COMP-002) | Phase 1 | Phase 2 (COMP-002), Phase 4 (TEST-005) |
| UserProfile migration | DB schema | DM-001 + NFR-COMP-001 | Phase 1 | Phase 2 (COMP-005), Phase 3 (API-002) |
| Audit log schema | DB schema | NFR-COMP-002 | Phase 1 | Phase 2 (audit log writer), Phase 4 (compliance validation) |

---

## Phase 2: Backend Services and Security

**Objective:** Implement all backend service components with security hardening. This phase builds the core business logic that the API layer exposes.

**Personas & Value:** Alex gains the backend foundation for frictionless registration and login. Sam gains token refresh capability at the service layer. Jordan's audit trail begins emitting events.

**Duration:** 2 weeks

**Entry criteria:** Phase 1 complete. All data stores operational. RSA key pair mounted as secrets.

**Exit criteria:** All 5 backend components pass unit tests. Security constraints (bcrypt cost 12, RS256, token hashing) verified. Audit logging emits for all auth events.

| # | ID | Task | Description | Depends On | Acceptance Criteria |
|---|-----|------|-------------|------------|---------------------|
| 8 | COMP-004 | Implement PasswordHasher | bcrypt abstraction with configurable cost factor (default 12). hash() and verify() methods. Designed for future algorithm migration (Argon2id). | — | hash() produces bcrypt output with cost 12. verify() correctly validates. Raw passwords never logged. |
| 9 | NFR-SEC-001 | Validate bcrypt cost factor | Unit test asserting PasswordHasher uses bcrypt cost factor 12. Verify hash timing < 500ms. | COMP-004 | Test passes. Benchmark confirms < 500ms per hash. |
| 10 | NFR-COMP-003 | Validate NIST password storage compliance | Verify one-way adaptive hashing. Confirm raw passwords never persisted or logged anywhere in the pipeline. | COMP-004 | Security review checklist signed off. grep confirms no password plaintext in logs. |
| 11 | COMP-003 | Implement JwtService | RS256 signing/verification with 2048-bit RSA keys. 5-second clock skew tolerance. Key rotation support (quarterly). | — | Tokens sign and verify correctly. Clock skew within tolerance accepted. Expired tokens rejected. |
| 12 | NFR-SEC-002 | Validate RS256 token signing | Configuration validation test confirming RS256 algorithm and 2048-bit key length. | COMP-003 | Test passes. No weaker algorithms accepted. |
| 13 | COMP-002 | Implement TokenManager | Issue access tokens (15-min TTL) and refresh tokens (7-day TTL). Store refresh tokens as hashed values in Redis. Support revocation. Rotation on refresh (old token revoked, new pair issued). | COMP-003, DM-002, OPS-006 | issueTokens() returns valid AuthToken. refresh() rotates tokens. revoke() invalidates token in Redis. |
| 14 | COMP-005 | Implement UserRepo | Data access layer for UserProfile CRUD in PostgreSQL. Uses pg-pool. Methods: findByEmail(), findById(), create(), updateLastLogin(), updatePassword(). | DM-001, OPS-005 | All CRUD operations verified against PostgreSQL. Connection pooling active. Email uniqueness enforced at DB level. |
| 15 | COMP-001 | Implement AuthService | Orchestrator facade: login(), register(), getProfile(), requestPasswordReset(), confirmPasswordReset(), logout(). Coordinates PasswordHasher, TokenManager, UserRepo. Account lockout after 5 failed attempts within 15 minutes. | COMP-002, COMP-004, COMP-005 | All orchestration flows execute correctly. Lockout triggers at threshold. No user enumeration on login failure. |
| 16 | FR-AUTH-001 | Wire login flow | AuthService.login() validates credentials via PasswordHasher.verify(), issues tokens via TokenManager.issueTokens(). Returns AuthToken on success, 401 on failure. | COMP-001 | Valid credentials → 200 + AuthToken. Invalid → 401. Non-existent email → 401 (no enumeration). Locked account → 423. |
| 17 | FR-AUTH-002 | Wire registration flow | AuthService.register() validates email uniqueness, enforces password policy (≥8 chars, uppercase, number), hashes via PasswordHasher, creates UserProfile with consentTimestamp, persists via UserRepo. | COMP-001, NFR-COMP-001 | Valid registration → 201 + UserProfile. Duplicate email → 409. Weak password → 400. Consent timestamp recorded. |
| 18 | FR-AUTH-003 | Wire token refresh flow | TokenManager.refresh() validates refresh token against Redis, revokes old token, issues new AuthToken pair via JwtService. | COMP-002 | Valid refresh → new AuthToken pair. Expired → 401. Revoked → 401. Old token no longer valid after refresh. |
| 19 | FR-AUTH-004 | Wire profile retrieval | AuthService.getProfile() returns UserProfile for authenticated user via UserRepo.findById(). | COMP-001 | Valid token → UserProfile with all fields. Invalid token → 401. |
| 20 | FR-AUTH-005 | Wire password reset flow | Two-step flow: requestPasswordReset() generates token, sends email via SendGrid. confirmPasswordReset() validates token (1-hour TTL, single-use), updates hash via PasswordHasher. | COMP-001, COMP-004 | Reset request → email sent (or silent success for unknown email). Valid token → password updated. Expired/used token → 400. |
| 21 | NFR-COMP-002-impl | Implement audit log emission | All auth events (login success/failure, registration, token refresh, password reset request/confirm, account lockout, logout) logged with user_id, timestamp, IP, and outcome to audit_log table. | NFR-COMP-002, COMP-001 | All event types emit audit records. Records include required fields. Retention per OQ-6 decision confirmed. |

### Integration Points — Phase 2

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|----------------|------|-------------------|--------------|-------------|
| AuthService dispatch | Orchestrator/facade | PasswordHasher (COMP-004), TokenManager (COMP-002), UserRepo (COMP-005) | Phase 2 (COMP-001) | Phase 3 (all API endpoints) |
| TokenManager → JwtService wiring | Composition | JwtService (COMP-003) nested in TokenManager (COMP-002) | Phase 2 (COMP-002) | Phase 3 (API-001, API-004, API-007), Phase 3 (COMP-009 silent refresh) |
| TokenManager → Redis wiring | Store binding | Redis hash storage for refresh tokens | Phase 1 (OPS-006), Phase 2 (COMP-002) | Phase 4 (TEST-003, TEST-005) |
| Audit log writer | Event emitter | AuthService → audit_log table | Phase 2 (NFR-COMP-002-impl) | Phase 4 (compliance validation), Phase 5 (OPS-003 on-call) |
| Account lockout mechanism | Rate limiter (in-service) | AuthService tracks failed attempts per email | Phase 2 (FR-AUTH-001) | Phase 3 (API-001 returns 423), Phase 4 (TEST-002 edge case) |

---

## Phase 3: API Surface, Frontend, and Integration

**Objective:** Expose backend services through versioned REST API endpoints including logout. Build frontend components with AuthProvider context. Wire end-to-end flows.

**Personas & Value:** Alex completes signup in < 60 seconds and can log out on shared devices. Sam gains programmatic token management with clear error codes. Jordan's audit trail covers logout events. Platform achieves measurable registration conversion.

**Duration:** 2 weeks

**Entry criteria:** Phase 2 complete. All backend services pass unit tests. SendGrid API credentials available.

**Exit criteria:** All 7 API endpoints respond correctly (including logout). Frontend components render and interact with API. AuthProvider handles token lifecycle including logout. Feature flags (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH) operational.

| # | ID | Task | Description | Depends On | Acceptance Criteria |
|---|-----|------|-------------|------------|---------------------|
| 22 | API-001 | Implement POST /auth/login | Rate limit: 10 req/min per IP. Request: {email, password}. Response: AuthToken (200), 401 (invalid), 423 (locked), 429 (rate limit). Error format: {error: {code, message, status}}. | FR-AUTH-001 | All response codes verified. Rate limiting enforced. Error codes match spec (AUTH_INVALID_CREDENTIALS). |
| 23 | API-002 | Implement POST /auth/register | Rate limit: 5 req/min per IP. Request: {email, password, displayName}. Response: UserProfile (201), 400 (validation), 409 (conflict). Records GDPR consent. | FR-AUTH-002 | Registration creates user. Validation errors return 400. Duplicate email returns 409. consentTimestamp persisted. |
| 24 | API-003 | Implement GET /auth/me | Rate limit: 60 req/min per user. Requires Bearer token. Response: UserProfile (200), 401 (unauthorized). | FR-AUTH-004 | Authenticated request returns full UserProfile. Missing/expired token returns 401. |
| 25 | API-004 | Implement POST /auth/refresh | Rate limit: 30 req/min per user. Request: {refreshToken}. Response: AuthToken (200), 401 (expired/revoked). | FR-AUTH-003 | Valid refresh token → new AuthToken pair. Expired → 401. Revoked → 401. |
| 26 | API-005 | Implement POST /auth/reset-request | Request: {email}. Returns success regardless of email registration (prevents enumeration). Triggers SendGrid email with 1-hour TTL token. | FR-AUTH-005 | Email sent for registered users. Silent success for unknown emails. Token generated with 1-hour expiry. |
| 27 | API-006 | Implement POST /auth/reset-confirm | Request: {token, newPassword}. Validates token (1-hour TTL, single-use), updates password hash. | FR-AUTH-005 | Valid token → password updated. Expired token → 400. Used token → 400. New password passes policy validation. |
| 28 | API-007 | Implement POST /auth/logout | Single-device logout. Revokes current refresh token in Redis via TokenManager.revoke(). Returns 200 on success, 401 if unauthenticated. Emits logout audit event. | COMP-001, COMP-002 | Authenticated request → refresh token revoked, 200 returned. Subsequent refresh with revoked token → 401. Audit log entry emitted. Unauthenticated request → 401. |
| 29 | — | Implement API versioning | Mount all endpoints under /v1/auth/*. Configure URL prefix routing. Document breaking change policy. | API-001 through API-007 | All endpoints accessible at /v1/auth/*. Non-versioned paths return 404. |
| 30 | — | Implement API error format | Consistent JSON error structure: {error: {code, message, status}} across all endpoints. | API-001 through API-007 | All error responses conform to format. Error codes documented. |
| 31 | — | Configure API Gateway rate limiting | IP-based rate limiting for public endpoints (login: 10/min, register: 5/min). User-based for authenticated endpoints (me: 60/min, refresh: 30/min, logout: 30/min). | API-001 through API-007 | Rate limits enforced. 429 returned with Retry-After header. |
| 32 | COMP-009 | Implement AuthProvider | React context provider managing AuthToken state. Silent refresh via TokenManager. Exposes UserProfile and auth methods (login, register, logout, refresh). Intercepts 401 responses, triggers token refresh, redirects unauthenticated users to LoginPage. Clears tokens on tab close (R-001 mitigation). logout() calls API-007, clears AuthToken state, redirects to /login. | API-001, API-003, API-004, API-007 | Context provides auth state to child components. Silent refresh works before token expiry. 401 interception triggers refresh. Tab close clears accessToken from memory. logout() revokes token and redirects. |
| 33 | COMP-006 | Implement LoginPage | Route /login. Email/password form. Submits to API-001 via AuthProvider. Stores AuthToken. Redirects on success. Generic error messages (no user enumeration). CAPTCHA after 3 failed attempts (R-002 contingency). | COMP-009, API-001 | Form renders. Valid credentials → redirect. Invalid → generic error. 3 failures → CAPTCHA shown. |
| 34 | COMP-007 | Implement RegisterPage | Route /register. Email, password, displayName fields. Client-side password policy validation (≥8 chars, uppercase, number). GDPR consent checkbox (NFR-COMP-001). Submits to API-002 via AuthProvider. < 60 seconds to complete (Alex persona constraint). | COMP-009, API-002 | Form renders with inline validation. Weak password blocked client-side. Consent required. Successful registration → logged in. |
| 35 | COMP-008 | Implement ProfilePage | Route /profile. Protected route (requires auth). Displays UserProfile via API-003: id, email, displayName, createdAt, updatedAt, lastLoginAt, roles. | COMP-009, API-003 | Page renders for authenticated users. All UserProfile fields displayed. Unauthenticated users redirected to /login. |
| 36 | MIG-004 | Implement AUTH_NEW_LOGIN feature flag | Gates access to new LoginPage and AuthService login endpoint. Default: OFF. | COMP-006, API-001 | Flag toggles between legacy and new login. OFF = legacy. ON = new system. |
| 37 | MIG-005 | Implement AUTH_TOKEN_REFRESH feature flag | Enables refresh token flow in TokenManager. When OFF, only access tokens issued. Default: OFF. | COMP-002, API-004 | Flag OFF → no refresh tokens issued. Flag ON → full token refresh flow active. |
| 38 | NFR-PERF-001 | Add APM instrumentation | Instrument all AuthService methods with OpenTelemetry spans. Emit auth_login_duration_seconds histogram, auth_login_total counter, auth_token_refresh_total counter, auth_registration_total counter, auth_logout_total counter. | COMP-001, API-001 through API-007 | All metrics emit. Spans trace AuthService → PasswordHasher → TokenManager → JwtService. Prometheus scrape endpoint active. |

### Integration Points — Phase 3

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|----------------|------|-------------------|--------------|-------------|
| API Gateway rate limiter | Middleware chain | IP-based (API-001, API-002, API-005, API-006), user-based (API-003, API-004, API-007) | Phase 3 | Phase 4 (load testing), Phase 5 (OPS-001 diagnosis) |
| AuthProvider context | React context/DI | LoginPage (COMP-006), RegisterPage (COMP-007), ProfilePage (COMP-008) | Phase 3 (COMP-009) | Phase 4 (TEST-006 E2E) |
| Feature flag registry | Feature flag system | AUTH_NEW_LOGIN (MIG-004), AUTH_TOKEN_REFRESH (MIG-005) | Phase 3 | Phase 5 (MIG-001, MIG-002, MIG-003 rollout) |
| Router → Page wiring | Frontend routing | /login → COMP-006, /register → COMP-007, /profile → COMP-008 (protected) | Phase 3 | Phase 4 (TEST-006) |
| Prometheus metrics registry | Observability | auth_login_total, auth_login_duration_seconds, auth_token_refresh_total, auth_registration_total, auth_logout_total | Phase 3 (NFR-PERF-001) | Phase 5 (OPS-001, OPS-002 runbooks, alerting) |

---

## Phase 4: Testing, Security Review, and Compliance Validation

**Objective:** Execute full test pyramid (unit, integration, E2E). Conduct security review and penetration testing. Validate compliance requirements (SOC2, GDPR, NIST). All testing runs against a frozen codebase.

**Personas & Value:** Jordan's compliance requirements validated against SOC2 controls. All personas' flows verified end-to-end before any real user exposure.

**Duration:** 2 weeks

**Entry criteria:** Phase 3 complete. All components integrated. Feature flags operational. Staging environment provisioned. Codebase frozen (no feature work during Phase 4).

**Exit criteria:** 80% unit test coverage. All integration tests pass with real databases. E2E flows pass in staging. Security review signed off. Compliance checklist complete. All success criteria measurable.

| # | ID | Task | Description | Depends On | Acceptance Criteria |
|---|-----|------|-------------|------------|---------------------|
| 39 | TEST-001 | Unit: Login with valid credentials | Jest/ts-jest. AuthService.login() → PasswordHasher.verify() → TokenManager.issueTokens() → returns AuthToken. Mocks: PasswordHasher.verify()=true, TokenManager.issueTokens()=mock pair. | FR-AUTH-001 | Test passes. AuthToken contains accessToken and refreshToken. |
| 40 | TEST-002 | Unit: Login with invalid credentials | Jest/ts-jest. AuthService.login() returns 401 when PasswordHasher.verify()=false. No token issued. | FR-AUTH-001 | Test passes. 401 returned. No AuthToken in response. |
| 41 | TEST-003 | Unit: Token refresh with valid refresh token | Jest/ts-jest. TokenManager.refresh() validates token, revokes old, issues new pair. Mock: Redis returns valid record. | FR-AUTH-003 | Test passes. New AuthToken pair returned. Old token marked revoked. |
| 42 | TEST-004 | Integration: Registration persists UserProfile | Supertest + testcontainers. Full flow: API request → PasswordHasher → PostgreSQL insert. Real database. | FR-AUTH-002 | Test passes. UserProfile in database matches request. 201 response. bcrypt hash stored (not plaintext). |
| 43 | TEST-005 | Integration: Expired refresh token rejected | Supertest + testcontainers. TokenManager + Redis. TTL expiration invalidates token. | FR-AUTH-003 | Test passes. Expired token → 401. |
| 44 | TEST-006 | E2E: Register, login, and logout flow | Playwright. RegisterPage → LoginPage → ProfilePage → Logout → LoginPage. Full user journey through AuthProvider including logout. | FR-AUTH-001, FR-AUTH-002, API-007 | Test passes. Registration succeeds. Login succeeds. ProfilePage shows correct data. Logout clears session and redirects to /login. Subsequent /profile access redirects to /login. |
| 45 | NFR-PERF-002 | Load test: 500 concurrent logins | k6 load test against staging (isolated from real traffic). 500 concurrent login requests. Verify p95 < 200ms. Monitor Redis and PostgreSQL under load. | API-001, OPS-004 | p95 latency < 200ms. No 5xx errors. Redis and PostgreSQL stable. |
| 46 | NFR-REL-001 | Configure availability monitoring | Health check endpoint for AuthService. Uptime monitoring over 30-day rolling windows. Target: 99.9%. | API-001 | Health endpoint responds. Monitoring dashboard active. Alerting configured for downtime. |
| 47 | — | Security review and penetration testing | Dedicated security review of: token storage (R-001), brute force protection (R-002), password hashing (NFR-SEC-001), input validation, CORS, TLS, logout token revocation. Penetration test on all API endpoints. | All Phase 2–3 components | Security review report with no P0/P1 findings. Pen test report with all findings remediated. |
| 48 | — | Compliance validation checklist | Verify: GDPR consent recording (NFR-COMP-001), SOC2 audit logging with correct retention (NFR-COMP-002), NIST password storage (NFR-COMP-003), data minimization (NFR-COMP-004). | NFR-COMP-001 through NFR-COMP-004 | All compliance items checked and documented. Audit log retention confirmed per OQ-6 decision. |
| 49 | — | Success criteria instrumentation | Verify all 10 success criteria are measurable: login p95 (APM), registration rate (funnel), refresh latency (APM), availability (health check), hash time (benchmark), conversion (analytics), DAU (token counts), session duration (refresh analytics), failed login rate (audit logs), password reset completion (funnel). | NFR-PERF-001 | All 10 metrics have active measurement. Dashboards show baseline readings. |

---

## Phase 5: Migration Rollout and Operational Readiness

**Objective:** Execute 3-phase migration (alpha → beta → GA). Establish operational runbooks, alerting, and on-call procedures. Remove feature flags post-GA. Schedule retrospective.

**Personas & Value:** Alex and Sam experience production authentication. Jordan has runbooks and alerts for incident response. Platform achieves 99.9% uptime SLA. Compliance team gains confidence for Q3 2026 SOC2 audit.

**Duration:** 4 weeks (1 + 2 + 1)

**Entry criteria:** Phase 4 complete. All tests pass. Security review signed off. Compliance validated. Staging environment validated.

**Exit criteria:** GA achieved with 99.9% uptime over first 7 days. All monitoring dashboards green. Runbooks validated. On-call rotation active. Feature flags removed. Post-GA retrospective scheduled.

| # | ID | Task | Description | Depends On | Acceptance Criteria |
|---|-----|------|-------------|------------|---------------------|
| 50 | MIG-001 | Phase 1 — Internal Alpha (1 week) | Deploy AuthService to staging. auth-team and QA test all endpoints including logout. LoginPage and RegisterPage behind AUTH_NEW_LOGIN flag. | All Phase 4 | All FR pass manual testing. Zero P0/P1 bugs. |
| 51 | MIG-002 | Phase 2 — Beta 10% (2 weeks) | Enable AUTH_NEW_LOGIN for 10% of traffic. Monitor latency, error rates, Redis usage. AuthProvider handles token refresh and logout under real load. | MIG-001 | p95 < 200ms. Error rate < 0.1%. No Redis connection failures. |
| 52 | MIG-003 | Phase 3 — GA 100% (1 week) | Remove AUTH_NEW_LOGIN flag. All traffic through new AuthService. Legacy endpoints deprecated. Enable AUTH_TOKEN_REFRESH. | MIG-002 | 99.9% uptime over first 7 days. All dashboards green. |
| 53 | MIG-006 | Validate rollback procedure | Test rollback triggers: p95 > 1000ms for 5min, error rate > 5% for 2min, Redis failures > 10/min, data corruption. Verify legacy auth resumes within 5 minutes. | MIG-001 | Rollback tested in staging. Legacy auth resumes. Smoke tests pass. |
| 54 | OPS-001 | Publish AuthService Down runbook | Document symptoms (5xx on /auth/*), diagnosis (pod health, PostgreSQL, Redis), resolution (restart, failover, re-login), escalation (auth-team → platform-team). | MIG-003 | Runbook reviewed by auth-team. Linked from on-call dashboard. |
| 55 | OPS-002 | Publish Token Refresh Failures runbook | Document symptoms (unexpected logouts, redirect loops), diagnosis (Redis, JwtService keys, feature flag), resolution (scale Redis, re-mount secrets), escalation path. | MIG-003 | Runbook reviewed. Linked from on-call dashboard. |
| 56 | OPS-003 | Establish on-call rotation | auth-team 24/7 on-call for first 2 weeks post-GA. P1 acknowledgment within 15 minutes. Escalation: on-call → test-lead → eng-manager → platform-team. | MIG-003 | Rotation scheduled. PagerDuty/equivalent configured. All team members briefed on runbooks. |
| 57 | OPS-004 | Configure HPA for AuthService pods | 3 replicas baseline. HPA scales to 10 replicas on CPU > 70%. Validate scaling under load. | MIG-001 | HPA triggers correctly. Scale-up completes within 2 minutes. Scale-down after load subsides. |
| 58 | — | Configure alerting rules | Login failure rate > 20% over 5min. p95 latency > 500ms. Redis connection failures. TokenManager error counter spikes. | NFR-PERF-001, OPS-001, OPS-002 | All alerts fire in staging test. PagerDuty integration verified. |
| 59 | — | Post-GA feature flag cleanup | Remove AUTH_NEW_LOGIN (MIG-004) after GA. Remove AUTH_TOKEN_REFRESH (MIG-005) after GA + 2 weeks. Clean up flag evaluation code. | MIG-003 | No feature flag references in codebase. All code paths use new auth exclusively. |
| 60 | — | Schedule post-GA retrospective | Schedule retrospective for 2 weeks post-GA. Agenda: Phase 1–5 execution review, estimate accuracy, risk materialization, process improvements. | MIG-003 | Calendar invite sent. All team leads confirmed. Retrospective agenda distributed. |

### Post-GA Monitoring Cadence

| Cadence | Activity | Owner |
|---------|----------|-------|
| Daily | SLO dashboard review: login latency, availability, error rates, registration conversion | ops-team |
| Weekly | Metrics review: user growth, session duration, reset completion rate, failed login trends | product-team + ops-team |
| Monthly | Post-incident reviews: incident frequency, MTTR, customer impact | auth-team |
| Quarterly | Compliance audit: log retention, consent tracking, NIST compliance | compliance-team |

---

## Risk Assessment and Mitigation

| ID | Risk | Severity | Probability | Phase Addressed | Mitigation | Contingency |
|----|------|----------|-------------|-----------------|------------|-------------|
| R-001 | Token theft via XSS | HIGH | Medium | Phase 3 (COMP-009) | accessToken in memory only. HttpOnly cookies for refreshToken. 15-minute expiry. Clear tokens on tab close. Logout via API-007. | Immediate revocation via TokenManager. Force password reset. |
| R-002 | Brute-force attacks on login | MEDIUM | High | Phase 3 (API Gateway) | Rate limiting 10 req/min/IP. Account lockout after 5 attempts. bcrypt cost 12. | WAF IP blocking. CAPTCHA after 3 failures on LoginPage. |
| R-003 | Data loss during legacy migration | HIGH | Low | Phase 5 (MIG-001–003) | Parallel operation in Phases 1–2. Idempotent upserts. Full backup before each phase. | Rollback to legacy auth (MIG-006). Restore from backup. |
| R-004 | Low registration adoption | HIGH | Medium | Phase 3 (COMP-007) | Usability testing before launch. < 60 seconds completion target. Inline validation. | Iterate based on funnel analytics post-GA. |
| R-005 | Security breach from flaws | CRITICAL | Low | Phase 4 (security review) | Dedicated security review. Penetration testing before production. | Incident response per runbook. Token revocation. Force password resets. |
| R-006 | Compliance failure from audit gaps | HIGH | Medium | Phase 1 (NFR-COMP-002), Phase 4 | Resolve OQ-6 before Phase 1 via stakeholder gate. Validate against SOC2 in Phase 4. | Extend retention retroactively if gap discovered. |
| R-007 | Email delivery failures | MEDIUM | Low | Phase 3 (API-005) | SendGrid delivery monitoring and alerting. | Fallback support channel for manual password resets. |

---

## Resource Requirements and Dependencies

### Team Allocation (Indicative FTE)

These FTE estimates are indicative for planning purposes and should be adjusted based on actual team capacity and availability.

| Team | Phase 1 (1 wk) | Phase 2 (2 wk) | Phase 3 (2 wk) | Phase 4 (2 wk) | Phase 5 (4 wk) |
|------|-----------------|-----------------|-----------------|-----------------|-----------------|
| auth-team (5 FTE) | Lead | Lead | Lead (backend) | Lead | Lead |
| platform-team (2 FTE) | Infrastructure setup | Support | API Gateway config | Load testing | On-call backup |
| frontend-team (3 FTE) | — | — | Lead (frontend) | E2E testing | — |
| security (1 FTE, shared) | — | Review | — | Pen testing | — |
| QA (2 FTE) | — | — | — | Test execution | Alpha/Beta validation |

**Estimated FTE per phase:** Phase 1: ~6 | Phase 2: ~8 | Phase 3: ~11 | Phase 4: ~10 | Phase 5: ~7

### External Dependencies

| Dependency | Required By | Fallback |
|------------|-------------|----------|
| PostgreSQL 15+ | Phase 1 start | None — blocking |
| Redis 7+ | Phase 1 start | None — blocking |
| Node.js 20 LTS | Phase 1 start | None — blocking |
| bcryptjs (npm) | Phase 2 (COMP-004) | Alternative bcrypt binding |
| jsonwebtoken (npm) | Phase 2 (COMP-003) | jose library |
| SendGrid API | Phase 3 (API-005, API-006) | Alternative email provider; manual reset as fallback |
| Frontend routing framework | Phase 3 (COMP-006–008) | None — blocking for frontend |
| SEC-POLICY-001 | Phase 2 (security config) | Use NIST SP 800-63B defaults |

---

## Open Questions — Resolution Requirements

| # | Question | Resolution Deadline | Impact if Unresolved |
|---|----------|--------------------|-----------------------|
| **OQ-6** | **Audit log retention: 90 days vs 12 months. Requires stakeholder decision — PRD specifies 12 months for SOC2, but implementation implications (partitioning, archival, cold storage) are non-trivial.** | **Before Phase 1 start (blocking gate)** | **SOC2 compliance failure; schema redesign risk** |
| OQ-1 | API key auth for service-to-service? | Deferred to v1.1 | No impact on v1.0 |
| OQ-2 | Max roles array length? | Before Phase 2 (COMP-005) | UserRepo validation incomplete |
| OQ-3 | Sync vs async password reset emails? | Before Phase 3 (API-005) | API response time unpredictable |
| OQ-4 | Max refresh tokens per user? | Before Phase 2 (COMP-002) | Unbounded Redis growth risk |
| OQ-5 | "Remember me" session extension? | Before Phase 3 (COMP-009) | AuthProvider refresh window undefined |
| **OQ-7** | **Logout endpoint — PRD commits to it. Scoped in this roadmap as: single-device, revoke current refresh token, clear AuthProvider state, redirect to /login. Included as API-007 in Phase 3.** | **Resolved (scoped in roadmap)** | **N/A — included** |
| OQ-8 | Admin audit log query API? Deferred to v1.1. Jordan persona needs acknowledged; v1.0 logs events, v1.1 adds query API. | Deferred to v1.1 | Jordan persona partially unmet in v1.0 |
| **OQ-9** | **GDPR consent field in UserProfile — proactively added as consentTimestamp in DM-001. Cost of inclusion is near zero; cost of omission is GDPR non-compliance.** | **Resolved (included in Phase 1)** | **N/A — included** |
| OQ-10 | Password reset endpoint specs? | Before Phase 3 (API-005, API-006) | Endpoints built from inferred specs |

---

## Architectural Debt Acknowledged

The following capabilities are explicitly deferred from v1.0. This is a deliberate scope decision, not an oversight.

| Debt Item | Deferred To | Rationale |
|-----------|-------------|-----------|
| Admin audit log query API (OQ-8) | v1.1 | Jordan persona needs partially met by log emission; query API adds scope |
| Multi-factor authentication | v1.1+ | Requires SMS/TOTP infrastructure not yet available |
| Social login (Google, GitHub) | v2.0 | Depends on OAuth/OIDC infrastructure |
| API key auth for service-to-service | v1.1 | Sam persona fully served by JWT for v1.0 |

---

## Success Criteria and Validation Approach

All quantitative targets below are preserved from the PRD (S19) without modification.

| # | Metric | Target | Validated In | Method |
|---|--------|--------|-------------|--------|
| SC-001 | Login p95 latency | < 200ms | Phase 4 (NFR-PERF-002) | k6 load test + APM |
| SC-002 | Registration success rate | > 99% | Phase 5 (MIG-002 beta) | Funnel analytics |
| SC-003 | Token refresh p95 latency | < 100ms | Phase 4 (NFR-PERF-002) | APM instrumentation |
| SC-004 | Service availability | 99.9% | Phase 5 (MIG-003 GA+7d) | Health check monitoring |
| SC-005 | Password hash time | < 500ms | Phase 2 (NFR-SEC-001) | Benchmark test |
| SC-006 | Registration conversion | > 60% | Phase 5 (MIG-002+) | Funnel: RegisterPage → confirmed |
| SC-007 | DAU (authenticated) | > 1000 within 30d GA | Phase 5 (GA+30d) | AuthToken issuance counts |
| SC-008 | Average session duration | > 30 min | Phase 5 (GA+30d) | Token refresh event analytics |
| SC-009 | Failed login rate | < 5% | Phase 5 (MIG-002+) | Audit log analysis |
| SC-010 | Password reset completion | > 80% | Phase 5 (GA+30d) | Funnel: reset request → new password |

### Qualitative Validation Gates

| Gate | Validation | Owner | Approval |
|------|-----------|-------|----------|
| Security posture | Penetration test report; zero P0/P1 findings | security-team | CISO or security lead |
| Operational readiness | Runbooks tested with simulated failures; on-call can execute > 95% within 15 min | ops-team | Ops manager |
| Compliance | SOC2 audit logging validated; retention pipeline operational; GDPR consent collected; NIST hashing confirmed | compliance-team | Compliance officer |
| Product quality | Usability testing shows > 60% registration conversion; zero P0 bugs in beta | product-team | Product manager |

---

## Timeline Summary

| Phase | Duration | Cumulative | Key Milestone | Confidence |
|-------|----------|------------|---------------|------------|
| Phase 1: Data Layer | 1 week | Week 1 | Database schemas deployed, Redis operational | High (90%) |
| Phase 2: Backend Services | 2 weeks | Week 3 | All 5 backend components implemented and unit tested | High (85%) |
| Phase 3: API + Frontend + Logout | 2 weeks | Week 5 | All 7 endpoints live, frontend components integrated | Medium (75%) |
| Phase 4: Testing + Compliance | 2 weeks | Week 7 | Security review passed, compliance validated, load test passed | Medium (70%) |
| Phase 5: Migration Rollout | 4 weeks | Week 11 | GA achieved, on-call active, feature flags removed | Medium (70%) |

**Total estimated duration: 11 weeks**

**Buffer recommendation:** Add 1–2 weeks contingency for P1 bug fixes discovered during Phase 3 or 4. Phase 4 security pentest may uncover issues requiring rework. Post-GA on-call ramp-up should extend 2 weeks past Phase 5 to stabilize.

**Critical path:** DM-001 → COMP-005 → COMP-001 → API-001/002/007 → TEST-004/006 → MIG-001 → MIG-003

**Compliance deadline alignment:** GA at Week 11 provides approximately 2 months of buffer before the Q3 2026 SOC2 audit, assuming Phase 1 begins in early April 2026. Confidence ratings reflect that frontend integration (Phase 3) and security pentest findings (Phase 4) carry the highest schedule risk.
