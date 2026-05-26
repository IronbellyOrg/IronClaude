# User Authentication Service — Implementation Roadmap

**Source:** AUTH-MERGED-PRD-TDD (merged PRD + TDD, 1230 lines)
**Variant:** sonnet-default (general-purpose analyst, no persona)
**Generated:** 2026-05-22
**Target Release:** v1.0, Q2 2026

---

## 1. Vision and Outcome Statement

### 1.1 Business Vision

Deliver a production-grade user authentication service that unblocks $2.4M in projected annual revenue from personalization-dependent features, satisfies SOC2 Type II audit requirements ahead of the Q3 2026 compliance deadline, and eliminates the 30% quarter-over-quarter growth in access-related support tickets. Every platform user gains a secure, frictionless identity within 60 seconds of registration.

### 1.2 Technical Vision

A stateless, JWT-based authentication service (`AuthService`) backed by PostgreSQL for durable user data and Redis for refresh token lifecycle management. The service exposes four RESTful endpoints (`/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`) plus password reset endpoints, all operating at <200ms p95 latency under 500 concurrent requests with 99.9% availability. The architecture supports horizontal scaling from day one via stateless JWT verification across service instances.

### 1.3 Success Definition

The roadmap succeeds when:

- Registration conversion exceeds 60% (FR-AUTH.2)
- Login p95 latency stays below 200ms (NFR-AUTH.1)
- Average session duration exceeds 30 minutes (FR-AUTH.3)
- Failed login rate stays below 5% of attempts (FR-AUTH.1)
- Password reset completion rate exceeds 80% (FR-AUTH.5)
- All auth events are logged with user ID, timestamp, IP, and outcome for SOC2 compliance
- The service passes a dedicated security review and penetration test before production GA

---

## 2. Phasing Strategy

### 2.1 Phase Decomposition Rationale

The source PRD prescribes two phases across six sprints (Section "Phasing" in PRD Section 1). The TDD elaborates five milestones (M1-M5 in TDD Section 23). This roadmap reconciles both by adopting a three-phase structure aligned to TDD milestones:

| Phase | Milestones | Theme | Sprints | Duration |
|-------|-----------|-------|---------|----------|
| **Phase 1: Core Auth** | M1, M2 | Registration, login, token lifecycle | 1-4 | 8 weeks |
| **Phase 2: Completion** | M3, M4 | Password reset, profile, frontend integration | 5-8 | 8 weeks |
| **Phase 3: Hardening & GA** | M5 | Rollout, stabilization, production verification | 9-11 | 6 weeks |

### 2.2 Why Three Phases, Not Two

The PRD's two-phase split places password reset (a security-sensitive email integration) in the same phase as frontend integration. Separating them isolates risk: the email-dependent password reset flow has external dependencies (SendGrid) and unique failure modes (delivery latency, token expiry), while frontend integration is purely internal. Additionally, the TDD's five-milestone structure naturally clusters into a pre-external-dependency core (M1+M2), an integration+completion layer (M3+M4), and a rollout phase (M5).

### 2.3 Parallel Workstreams

Within each phase, the following tracks run in parallel where dependencies allow:

- **Backend track:** AuthService, PasswordHasher, TokenManager, JwtService, database schema
- **Frontend track:** LoginPage, RegisterPage, AuthProvider, ProfilePage
- **Infrastructure track:** PostgreSQL provisioning, Redis provisioning, API Gateway config, CI/CD pipelines
- **Security track:** Password policy enforcement, rate limiting, audit logging, penetration test scheduling
- **Observability track:** Prometheus metrics, OpenTelemetry tracing, alerting, dashboards

---

## 3. Milestones

### 3.1 M1: Core AuthService and Password Hashing

**Target Date:** 2026-04-14 (Sprint 1-2, weeks 1-4)

**Scope:** Build the foundational AuthService orchestration layer with password hashing and user persistence.

**Deliverables:**

| ID | Deliverable | Requirement Trace |
|----|-------------|-------------------|
| D-001 | `AuthService` class with login() and register() methods | FR-AUTH-001, FR-AUTH-002 |
| D-002 | `PasswordHasher` module: bcrypt wrapper with cost factor 12 | NFR-SEC-001, NFR-AUTH.3 |
| D-003 | `UserProfile` PostgreSQL schema (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles) | TDD Section 7.1 |
| D-004 | POST `/auth/register` endpoint with email uniqueness validation and password policy enforcement (min 8 chars, 1 uppercase, 1 number) | FR-AUTH-002, FR-AUTH.2 |
| D-005 | POST `/auth/login` endpoint with bcrypt credential verification | FR-AUTH-001, FR-AUTH.1 |
| D-006 | Account lockout after 5 failed attempts within 15 minutes | TDD Section 13, PRD "Error Handling" |
| D-007 | Generic error responses (no user enumeration on login or registration) | FR-AUTH-001 AC3, PRD Edge Cases |
| D-008 | Unit test suite for AuthService and PasswordHasher (target: 80% coverage) | TDD Section 15.2 |
| D-009 | Database migration scripts for `users` table with unique index on email | TDD Section 7.2 |
| D-010 | Docker Compose development environment (PostgreSQL + Redis + app) | TDD Section 15.3 |

**Entry Criteria:**

- PostgreSQL 15+ instance provisioned and accessible
- Node.js 20 LTS runtime configured
- CI pipeline scaffolding complete (Jest + testcontainers)
- SEC-POLICY-001 password requirements documented

**Exit Criteria:**

- All M1 unit tests pass (80%+ coverage on AuthService, PasswordHasher)
- POST `/auth/register` creates a UserProfile, rejects duplicate emails (409), rejects weak passwords (400)
- POST `/auth/login` returns 200 with accessToken for valid credentials, 401 for invalid
- Account locks after 5 failed logins within 15 minutes, returns 423
- No user enumeration possible: identical error messages for wrong email vs wrong password
- bcrypt cost factor 12 verified in unit test (hash completes in <500ms)
- Integration test against real PostgreSQL passes

**Dependencies:**

- PostgreSQL 15+ provisioned (internal infrastructure dependency)
- SEC-POLICY-001 finalized (policy dependency, Owner: Security team)
- No external service dependencies in this milestone

**Duration Estimate:** 4 weeks (2 sprints)

**Risk Notes:**

- bcrypt cost factor 12 has been benchmarked at ~300ms (TDD Section 17). If real-world latency exceeds the 200ms p95 budget, cost factor may need adjustment. Mitigation: benchmark early in Sprint 1, day 3, against production-equivalent hardware.
- Concurrent registration with the same email must be handled by database unique constraint (TDD Section 12), not application-level checks alone.

---

### 3.2 M2: Token Management and Profile Retrieval

**Target Date:** 2026-04-28 (Sprint 3-4, weeks 5-8)

**Scope:** Implement the JWT-based token lifecycle, refresh token management, and profile endpoint.

**Deliverables:**

| ID | Deliverable | Requirement Trace |
|----|-------------|-------------------|
| D-011 | `JwtService` module: RS256 JWT signing and verification with 2048-bit RSA keys | NFR-SEC-002 |
| D-012 | `TokenManager` module: access token issuance (15-min TTL), refresh token issuance (7-day TTL), refresh token rotation | FR-AUTH-003, FR-AUTH.3 |
| D-013 | `AuthToken` data model (accessToken, refreshToken, expiresIn, tokenType) | TDD Section 7.1 |
| D-014 | Redis-backed refresh token storage with 7-day TTL and revocation support | TDD Section 7.2 |
| D-015 | POST `/auth/refresh` endpoint: exchange valid refresh token for new AuthToken pair, revoke old token | FR-AUTH-003 |
| D-016 | GET `/auth/me` endpoint: return authenticated user's UserProfile | FR-AUTH-004, FR-AUTH.4 |
| D-017 | JWT authentication middleware for protected endpoints | TDD Section 10.1 |
| D-018 | 5-second clock skew tolerance in JwtService for JWT validation | TDD Section 12 |
| D-019 | Redis unavailability fallback: reject refresh requests rather than serve stale tokens | TDD Section 12 |
| D-020 | Unit test suite for JwtService and TokenManager (80%+ coverage) | TDD Section 15.2 |
| D-021 | Integration tests for refresh token lifecycle against real Redis | TDD Section 15.2 |
| D-022 | Prometheus metrics: `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total` | TDD Section 14 |

**Entry Criteria:**

- M1 complete and all exit criteria met
- Redis 7+ instance provisioned and accessible
- RS256 signing key pair generated and stored in secrets manager

**Exit Criteria:**

- Login returns both accessToken (15-min TTL) and refreshToken (7-day TTL) as `AuthToken`
- POST `/auth/refresh` with valid refreshToken returns new AuthToken pair; old refreshToken is revoked
- POST `/auth/refresh` with expired or revoked refreshToken returns 401
- GET `/auth/me` with valid accessToken returns UserProfile; with invalid/expired token returns 401
- Token refresh latency p95 < 100ms (TDD Section 4.1)
- Redis TTL correctly invalidates expired refresh tokens (integration test verified)
- Clock skew tolerance of 5 seconds confirmed in unit test
- Prometheus metrics exported on `/metrics` endpoint
- All M2 unit and integration tests pass

**Dependencies:**

- M1 complete (blocking)
- Redis 7+ provisioned (internal infrastructure)
- RS256 key pair in secrets manager (security/infrastructure)

**Duration Estimate:** 4 weeks (2 sprints)

**Risk Notes:**

- Refresh token rotation (issue new + revoke old in single operation) requires Redis atomicity. If non-atomic, a race window allows token reuse. Mitigation: use Redis MULTI/EXEC or Lua script for atomic token rotation.
- RS256 key rotation (quarterly per TDD Section 13) must support a grace period where both old and new keys validate tokens. This should be architected in M2 even if first rotation occurs post-GA.

---

### 3.3 M3: Password Reset and Audit Logging

**Target Date:** 2026-05-12 (Sprint 5-6, weeks 9-12)

**Scope:** Implement the self-service password reset flow with email integration and the SOC2-compliant audit logging subsystem.

**Deliverables:**

| ID | Deliverable | Requirement Trace |
|----|-------------|-------------------|
| D-023 | POST `/auth/reset-request` endpoint: accept email, send reset token via SendGrid | FR-AUTH-005, FR-AUTH.5 |
| D-024 | POST `/auth/reset-confirm` endpoint: validate reset token, update password hash, invalidate all sessions | FR-AUTH-005 |
| D-025 | Reset token generation: single-use, 1-hour expiry, stored hashed in database | FR-AUTH-005 AC3-4 |
| D-026 | SendGrid email integration for password reset emails | PRD Dependency table |
| D-027 | Anti-enumeration: identical success response for registered and unregistered emails on reset-request | FR-AUTH.5, PRD Edge Cases |
| D-028 | Audit log table in PostgreSQL: userId, eventType, timestamp, ipAddress, outcome | SOC2 compliance, PRD Section "Legal and Compliance" |
| D-029 | Structured logging for all auth events (login success/failure, registration, token refresh, password reset, account lockout) | TDD Section 14, PRD SOC2 |
| D-030 | Audit log query interface for admin (filter by date range, user, event type) | PRD Admin user story |
| D-031 | Password reset invalidates all existing refresh tokens for the user | FR-AUTH.5 AC: "new password invalidates all sessions" |
| D-032 | Unit and integration tests for password reset flow | TDD Section 15 |
| D-033 | 12-month audit log retention policy enforcement | PRD "Legal and Compliance" |

**Entry Criteria:**

- M2 complete and all exit criteria met
- SendGrid API key provisioned and email templates designed
- Audit log schema reviewed by compliance team

**Exit Criteria:**

- Password reset email delivered within 60 seconds (FR-AUTH.5)
- Reset token expires after 1 hour; used tokens cannot be reused
- New password invalidates all existing refresh tokens (verified via integration test)
- Identical success response for reset-request regardless of email registration status
- All auth events logged with userId, eventType, timestamp, ipAddress, outcome
- Audit logs queryable by date range and user ID
- 12-month retention policy enforced (verified via retention query or TTL mechanism)
- GDPR consent recorded at registration with timestamp (PRD "Legal and Compliance")
- All M3 unit and integration tests pass

**Dependencies:**

- M2 complete (blocking -- refresh token revocation depends on TokenManager)
- SendGrid account and API key provisioned (external dependency)
- Email template for password reset designed and approved (design/content team)
- Compliance team review of audit log schema (SOC2 requirement)

**Duration Estimate:** 4 weeks (2 sprints)

**Risk Notes:**

- SendGrid delivery failures block the password reset flow. The PRD risk analysis (Low likelihood, Medium impact) recommends delivery monitoring and fallback support channel. Concrete mitigation: implement a delivery status webhook from SendGrid, alert on bounce rate > 2%, and provide a support-visible "resend reset email" admin action.
- The source PRD lists an open question (OQ-003 equivalent): "Should password reset emails be sent synchronously or asynchronously?" Resolution required before M3 Sprint 1 kickoff. Recommendation: asynchronous with a queue (e.g., Bull/BullMQ on Redis) to avoid blocking the HTTP response and to provide retry semantics. If async, add a Redis-backed job queue to the infrastructure requirements.
- Reset tokens must be stored hashed (not plaintext) to prevent token theft from the database. This is consistent with the security posture of storing refresh tokens hashed in Redis (TDD Section 13).

---

### 3.4 M4: Frontend Integration

**Target Date:** 2026-05-26 (Sprint 7-8, weeks 13-16)

**Scope:** Build the frontend authentication UI components and integrate with the backend API.

**Deliverables:**

| ID | Deliverable | Requirement Trace |
|----|-------------|-------------------|
| D-034 | `LoginPage` component: email/password form, error display, redirect on success | TDD Section 10.2 |
| D-035 | `RegisterPage` component: email/password/displayName form with inline validation, GDPR consent checkbox | TDD Section 10.2, PRD "Legal and Compliance" |
| D-036 | `AuthProvider` context: manages AuthToken state, silent token refresh, 401 interception, redirect to LoginPage | TDD Section 10.2 |
| D-037 | `ProfilePage` component: displays UserProfile data (name, email, creation date) | FR-AUTH-004, FR-AUTH.4 |
| D-038 | Password reset page: email submission form + new password form (linked from reset email) | FR-AUTH-005 |
| D-039 | Client-side password strength validation (matches server policy: 8+ chars, uppercase, number) | FR-AUTH-002 AC3 |
| D-040 | Authenticated route guard: redirect unauthenticated users to LoginPage | TDD Section 10.3 |
| D-041 | Silent token refresh in AuthProvider: detect expiring accessToken, refresh via TokenManager before expiry | FR-AUTH.3, FR-AUTH-003 |
| D-042 | "Log Out" action: clear tokens, redirect to landing page | PRD "Log Out" user story |
| D-043 | E2E test suite: registration flow, login flow, profile view, token refresh, password reset | TDD Section 15.2 |
| D-044 | Form renders in < 1 second (PRD Journey: "Login form loads in under 1 second") | PRD Customer Journey |
| D-045 | Registration completes and redirects to dashboard within 2 seconds of form submission | PRD Customer Journey |

**Entry Criteria:**

- M2 complete (blocking -- frontend needs working API endpoints)
- M3 at minimum needs reset-request endpoint (reset-confirm can be developed in parallel with frontend)
- Frontend routing framework configured and available (PRD Dependency table)

**Exit Criteria:**

- LoginPage renders in < 1 second
- Successful login redirects to dashboard
- Failed login shows generic "Invalid email or password" error (no user enumeration)
- Registration form validates password strength inline before submission
- GDPR consent checkbox required at registration; consent recorded with timestamp
- Successful registration creates account and logs user in immediately (PRD User Story)
- AuthProvider silently refreshes tokens before accessToken expiry
- ProfilePage displays displayName, email, and createdAt
- Log Out ends session and redirects to landing page
- Password reset flow completes end-to-end in E2E test
- All E2E tests pass (Playwright, TDD Section 15.2)
- Registration + redirect completes in < 2 seconds

**Dependencies:**

- M2 complete (blocking -- all frontend components consume backend API)
- M3 reset-request endpoint available (blocking for password reset page)
- Frontend routing framework operational (internal dependency)

**Duration Estimate:** 4 weeks (2 sprints)

**Parallelization:** LoginPage and RegisterPage can be developed in parallel by two frontend engineers. AuthProvider is a prerequisite for ProfilePage and route guards, so it should be prioritized in Sprint 7.

**Risk Notes:**

- accessToken stored in memory only (not localStorage) to mitigate XSS-based token theft (TDD Risk R-001). This means tokens are lost on tab close. AuthProvider must handle this gracefully by checking for an active refreshToken on mount and re-authenticating silently.
- The PRD mentions "preserve work locally and prompt login" when a token expires during active editing. This requires application-level save-state logic in the AuthProvider that is outside the scope of the auth service itself but must be coordinated with the frontend team.

---

### 3.5 M5: Hardening, Rollout, and General Availability

**Target Date:** 2026-06-09 (Sprint 9-11, weeks 17-22)

**Scope:** Production hardening, phased rollout with feature flags, security review, penetration testing, and GA release.

**Deliverables:**

| ID | Deliverable | Requirement Trace |
|----|-------------|-------------------|
| D-046 | Feature flag `AUTH_NEW_LOGIN`: gates new LoginPage and AuthService endpoints | TDD Section 19.2 |
| D-047 | Feature flag `AUTH_TOKEN_REFRESH`: enables refresh token flow in TokenManager | TDD Section 19.2 |
| D-048 | Phase 1 Internal Alpha: deploy to staging, auth-team + QA test all endpoints (1 week) | TDD Section 19.1 |
| D-049 | Phase 2 Beta (10%): enable for 10% of traffic, monitor latency/error rates/Redis usage (2 weeks) | TDD Section 19.1 |
| D-050 | Phase 3 GA (100%): remove feature flags, all users route through new AuthService (1 week) | TDD Section 19.1 |
| D-051 | Security review: PasswordHasher bcrypt cost verified, JwtService RS256 key rotation documented | TDD Section 24.1 |
| D-052 | Penetration test by external security firm | PRD Risk Analysis |
| D-053 | Performance test: confirm < 200ms p95 under 500 concurrent users (k6 load test) | NFR-PERF-001, NFR-PERF-002 |
| D-054 | Rollback procedure tested in staging: disable feature flag, verify legacy flow operational | TDD Section 19.3 |
| D-055 | Monitoring dashboards: auth_login_total, auth_login_duration_seconds, auth_token_refresh_total, auth_registration_total | TDD Section 14 |
| D-056 | Alerting: login failure rate > 20% over 5 minutes, p95 latency > 500ms, Redis connection failures | TDD Section 14 |
| D-057 | Runbooks published for on-call team: AuthService down, token refresh failures | TDD Section 25.1 |
| D-058 | OpenTelemetry distributed tracing: full request lifecycle through AuthService, PasswordHasher, TokenManager, JwtService | TDD Section 14 |
| D-059 | 99.9% uptime verified over first 7 days in production (GA exit criterion) | NFR-REL-001 |
| D-060 | Feature flags removed after Phase 3 + 2 weeks stable operation | TDD Section 19.2 |

**Entry Criteria:**

- M3 and M4 complete and all exit criteria met
- All FR-AUTH-001 through FR-AUTH-005 implemented and verified with passing tests
- Unit test coverage > 80% for AuthService, TokenManager, JwtService, PasswordHasher
- Integration tests for all API endpoints pass against real PostgreSQL and Redis

**Exit Criteria (GA):**

- 99.9% uptime over first 7 production days
- p95 latency < 200ms on all auth endpoints under production load
- Error rate < 0.1% during Beta phase (10% traffic)
- Zero P0/P1 bugs at GA
- Security review completed and sign-off received
- Penetration test results reviewed; all Critical/High findings remediated
- Runbooks reviewed and published
- Go/no-go sign-off from test-lead and eng-manager (TDD Section 24.2)
- All monitoring dashboards verified and alerting tested
- Rollback procedure tested in staging

**Rollback Triggers (from TDD Section 19.4):**

- p95 latency > 1000ms for more than 5 minutes
- Error rate > 5% for more than 2 minutes
- Redis connection failures > 10 per minute
- Any data loss or corruption in UserProfile records

**Rollback Procedure (from TDD Section 19.3):**

1. Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth
2. Verify legacy login flow operational via smoke tests
3. Investigate failure root cause using structured logs and traces
4. If UserProfile data corruption detected, restore from last known-good backup
5. Notify auth-team and platform-team via incident channel
6. Post-mortem within 48 hours of rollback

**Dependencies:**

- M3, M4 complete (blocking)
- External penetration testing firm engaged and scheduled (external)
- Feature flag infrastructure available (internal)
- Kubernetes HPA configuration tested (infrastructure)

**Duration Estimate:** 6 weeks (3 sprints)

**Risk Notes:**

- The phased rollout (Internal Alpha 1 week + Beta 2 weeks + GA 1 week) is aggressive. If Beta reveals unexpected issues, the GA date slips. Mitigation: build a 1-week buffer into the schedule (hidden from the public timeline) between Beta and GA.
- Legacy auth system must remain functional throughout Phase 1 and Phase 2 as a rollback target. Decommissioning legacy auth should not begin until Phase 3 completes with 7 stable production days.

---

## 4. Cross-Cutting Workstreams

### 4.1 Security Workstream

**Runs:** Continuous, Sprint 1 through GA

| Activity | Sprint | Owner | Deliverable |
|----------|--------|-------|-------------|
| Define password policy per NIST SP 800-63B | Sprint 1 | Security team | SEC-POLICY-001 document |
| Configure rate limiting at API Gateway (10 req/min per IP for login, 5 req/min for registration) | Sprint 2 | Platform team | API Gateway config |
| Implement account lockout (5 failures / 15 minutes) | Sprint 2 | auth-team | AuthService lockout logic |
| CORS restriction to known frontend origins | Sprint 4 | auth-team | CORS middleware config |
| RS256 key rotation mechanism (quarterly, with grace period for old+new keys) | Sprint 4 | auth-team | Key rotation runbook |
| TLS 1.3 enforcement on all endpoints | Sprint 5 | Platform team | Infrastructure config |
| External penetration test | Sprint 9 | External firm | Pentest report |
| Security review sign-off | Sprint 10 | sec-reviewer | Sign-off document |
| Store refresh tokens hashed in Redis | Sprint 3 | auth-team | TokenManager hashing logic |
| Store reset tokens hashed in database | Sprint 5 | auth-team | Reset token storage logic |
|accessToken in memory only (not localStorage) | Sprint 7 | Frontend team | AuthProvider implementation |

### 4.2 Observability Workstream

**Runs:** Sprint 2 through GA

| Activity | Sprint | Owner | Deliverable |
|----------|--------|-------|-------------|
| Structured logging format for AuthService events | Sprint 2 | auth-team | Log format specification |
| Prometheus metrics: auth_login_total, auth_login_duration_seconds | Sprint 4 | auth-team | /metrics endpoint |
| Prometheus metrics: auth_token_refresh_total, auth_registration_total | Sprint 4 | auth-team | Additional metrics |
| Grafana dashboard: login rates, latency, error rates | Sprint 4 | auth-team | Dashboard JSON |
| OpenTelemetry distributed tracing setup | Sprint 5 | auth-team | OTel SDK integration |
| Alerting: login failure rate > 20% over 5 min | Sprint 5 | auth-team | AlertManager rules |
| Alerting: p95 latency > 500ms | Sprint 5 | auth-team | AlertManager rules |
| Alerting: Redis connection failures | Sprint 5 | auth-team | AlertManager rules |
| Runbooks: AuthService down, token refresh failures | Sprint 8 | auth-team | Published runbooks |

### 4.3 Testing Workstream

**Runs:** Sprint 1 through GA

| Activity | Sprint | Owner | Deliverable |
|----------|--------|-------|-------------|
| Jest + ts-jest unit test scaffolding | Sprint 1 | auth-team | Test configuration |
| Unit tests: AuthService, PasswordHasher | Sprint 2 | auth-team | 80%+ coverage |
| Unit tests: JwtService, TokenManager | Sprint 4 | auth-team | 80%+ coverage |
| Integration tests: testcontainers (PostgreSQL + Redis) | Sprint 2 | auth-team | CI pipeline config |
| Integration tests: all 4+ API endpoints | Sprint 4 | auth-team | Endpoint test suite |
| E2E test scaffolding (Playwright) | Sprint 7 | QA team | Playwright config |
| E2E tests: full user journey (register -> login -> profile) | Sprint 8 | QA team | E2E test suite |
| k6 load testing: 500 concurrent users | Sprint 9 | QA team | Load test scripts + results |
| Penetration test coordination | Sprint 9 | Security team | Pentest scheduling |
| Regression test suite for rollback verification | Sprint 10 | QA team | Rollback test plan |

### 4.4 Documentation Workstream

**Runs:** Sprint 3 through GA

| Activity | Sprint | Owner | Deliverable |
|----------|--------|-------|-------------|
| API documentation (OpenAPI/Swagger spec) | Sprint 4 | auth-team | OpenAPI YAML |
| Runbooks for on-call team | Sprint 8 | auth-team | Runbook documents |
| Key rotation procedure documentation | Sprint 4 | auth-team | Runbook |
| Capacity planning documentation | Sprint 10 | auth-team | Scaling guide |
| Post-GA: API consumer integration guide for Sam persona | Sprint 11 | Developer relations | Integration guide |

### 4.5 Infrastructure Workstream

**Runs:** Sprint 1 through GA

| Activity | Sprint | Owner | Deliverable |
|----------|--------|-------|-------------|
| PostgreSQL 15+ provisioning and connection pooling config | Sprint 1 | Platform team | Database instance |
| Redis 7+ provisioning | Sprint 3 | Platform team | Redis instance |
| API Gateway rate limiting configuration | Sprint 2 | Platform team | Gateway config |
| Kubernetes deployment manifests + HPA (3 replicas, scale to 10 on CPU > 70%) | Sprint 4 | Platform team | K8s manifests |
| CI/CD pipeline: build, test, deploy to staging | Sprint 2 | DevOps | Pipeline config |
| Feature flag infrastructure setup | Sprint 8 | Platform team | Flag system config |
| Production environment provisioning | Sprint 9 | Platform team | Prod K8s namespace |

---

## 5. Risk Register

| ID | Risk | Probability | Impact | P x I | Mitigation | Contingency | Owner | Monitoring |
|----|------|-------------|--------|-------|------------|-------------|-------|------------|
| RR-001 | bcrypt cost 12 exceeds 200ms p95 budget on production hardware | Low (benchmarked at 300ms standalone, ~100ms with connection pooling per TDD Section 17) | High (blocks NFR-PERF-001) | Medium | Benchmark on production-equivalent hardware in Sprint 1, day 3. Profile AuthService.login() latency breakdown. | Reduce cost factor to 11 if latency budget exceeded; document security trade-off. Re-evaluate if NIST guidance changes. | auth-team lead | APM latency alerting on login endpoint |
| RR-002 | SendGrid delivery failures block password reset flow | Low (PRD Risk Analysis) | Medium (users cannot self-serve password reset) | Low | Delivery monitoring via SendGrid webhook. Alert on bounce rate > 2%. Retry queue with exponential backoff (3 retries, max 5 min). | Fallback: support team can trigger manual password reset via admin tool. Provide "resend reset email" button. | auth-team | SendGrid delivery status dashboard + alerting |
| RR-003 | Redis unavailability causes mass token refresh failures | Low (managed Redis SLA 99.9%) | High (all users with active refresh tokens forced to re-login) | Medium | TokenManager fallback: reject refresh requests, return clear error, do not serve stale tokens (TDD Section 12). | Users re-login via LoginPage. AuthService issues new AuthToken pair. If Redis outage persists > 15 min, page auth-team on-call. Scale Redis cluster. | Platform team | Redis connection failure alert (> 10/min triggers rollback per TDD Section 19.4) |
| RR-004 | XSS attack leads to accessToken theft via localStorage | Medium (web application attack surface) | High (session hijacking, per TDD Risk R-001) | High | Store accessToken in memory only, not localStorage. AuthProvider clears tokens on tab close. HttpOnly cookies for refreshToken. 15-min accessToken TTL limits exposure window. | Immediate token revocation via TokenManager. Force password reset for affected UserProfile accounts. Security incident response. | Frontend team + Security | CSP headers audit, XSS scanning in CI |
| RR-005 | Brute-force attacks on login endpoint | High (public-facing login) | Medium (account compromise, per TDD Risk R-002) | High | Rate limiting: 10 req/min per IP at API Gateway. Account lockout after 5 failures in 15 min. bcrypt cost 12 makes offline cracking expensive. | Block offending IPs at WAF. Enable CAPTCHA on LoginPage after 3 failed attempts. Notify admin on lockout. | Security team | auth_login_total failure rate alert (> 20% over 5 min) |
| RR-006 | Data loss during migration from legacy auth (if applicable) | Low (TDD Risk R-003) | High (user data loss) | Medium | Run AuthService in parallel with legacy during Phase 1 and Phase 2. Idempotent upsert for UserProfile migration. Full DB backup before each rollout phase. | Rollback to legacy auth. Restore UserProfile from pre-migration backup. Post-mortem within 48 hours. | auth-team lead | Data integrity checks between legacy and new system during parallel run |
| RR-007 | Low registration adoption due to poor UX | Medium (PRD Risk Analysis) | High (blocks personalization revenue) | High | Usability testing before launch with 5+ target users. Iterate on form design based on funnel analytics. Inline validation, minimal fields, < 60-second registration target. | A/B test form variations post-launch. Consider reducing fields further (email + password only, display name optional). | Product team | Registration conversion funnel analytics (> 60% target) |
| RR-008 | Compliance failure from incomplete audit logging | Medium (SOC2 audit scheduled Q3 2026) | High (SOC2 audit failure, enterprise account risk) | High | Define log requirements in Sprint 1 (before any code). Validate against SOC2 controls in QA. 12-month retention policy enforced programmatically. | Remediate missing log entries before audit. Add retroactive logging for events that can be reconstructed. | Compliance team | Audit log completeness checks in CI, quarterly compliance review |
| RR-009 | RS256 signing key exposure | Low (secrets manager, quarterly rotation) | Critical (all tokens forgeable) | Medium | Keys stored in secrets manager with access audit. Quarterly rotation with grace period for old+new key validation. Never log or expose keys. | Immediate key rotation. Revoke all issued tokens. Force re-login for all users. Security incident investigation. | Security team | Secrets access audit logs, key age monitoring |
| RR-010 | Scope creep: MFA, OAuth, RBAC demands during v1.0 development | Medium (stakeholder pressure) | Medium (schedule delay) | Medium | Explicit out-of-scope list in PRD (v1.0 excludes OAuth/OIDC, MFA, RBAC, social login). Refer stakeholders to Non-Goals NG-001 through NG-003. | Defer to v1.1/v1.2 backlog. Do not accept scope changes without schedule re-baseline. | Product Owner | Sprint scope adherence tracking |
| RR-011 | Race condition in concurrent refresh token rotation | Low (requires specific timing) | Medium (token replay attack) | Low | Atomic Redis operations (MULTI/EXEC or Lua script) for token rotation. Single-use refresh tokens. | Monitor for duplicate refresh attempts (security event). Force re-login if pattern detected. | auth-team | TokenManager anomaly alerting |
| RR-012 | Clock skew across service instances invalidates valid JWTs | Low (5-second tolerance built in per TDD Section 12) | Low (false 401 responses) | Low | 5-second clock skew tolerance in JwtService validation. NTP synchronization on all service instances. | Increase tolerance to 30 seconds if clock drift detected. Investigate NTP configuration. | Platform team | JWT validation failure rate monitoring |

---

## 6. Dependencies and Sequencing

### 6.1 Critical Path

```
Sprint 1-2: M1 (Core AuthService + PasswordHasher)
     |
     v
Sprint 3-4: M2 (TokenManager + JwtService + Profile)
     |
     +---------------------------+
     |                           |
     v                           v
Sprint 5-6: M3 (Password Reset)   Sprint 7-8: M4 (Frontend)*
     |                           |
     +---------------------------+
     |
     v
Sprint 9-11: M5 (Rollout + GA)
```

*Note: M4 frontend development can begin in Sprint 5-6 in parallel with M3, using M2's completed API endpoints for LoginPage, RegisterPage, and AuthProvider. Only the password reset page depends on M3's reset-request endpoint.

### 6.2 Dependency Matrix

| Dependency | From | To | Type | Impact if Late |
|-----------|------|----|------|----------------|
| PostgreSQL provisioned | Infrastructure | M1 | Hard | M1 blocked by 1-2 weeks |
| Redis provisioned | Infrastructure | M2 | Hard | M2 blocked by 1-2 weeks |
| SEC-POLICY-001 finalized | Security team | M1 | Hard | Password policy undefined; registration cannot be implemented correctly |
| SendGrid API key + templates | External | M3 | Hard | Password reset flow blocked |
| RS256 key pair in secrets manager | Security/Infra | M2 | Hard | JwtService cannot sign tokens |
| Frontend routing framework | Internal | M4 | Hard | Auth pages cannot render |
| M1 complete | M1 | M2 | Hard | Token management requires login/register endpoints |
| M2 complete | M2 | M3 | Hard | Password reset requires TokenManager for session invalidation |
| M2 complete | M2 | M4 | Hard | Frontend needs working API endpoints |
| M3 reset-request endpoint | M3 | M4 (partial) | Soft | Only password reset page blocked; LoginPage/RegisterPage can proceed |
| M3 + M4 complete | M3, M4 | M5 | Hard | Cannot rollout incomplete features |
| External pentest scheduled | Security team | M5 | Hard | GA blocked without security review |
| Feature flag infrastructure | Platform team | M5 | Hard | Phased rollout not possible without feature flags |

### 6.3 Parallelization Opportunities

| Work | Sprint Window | Parallel Tracks |
|------|---------------|-----------------|
| M1 + Infrastructure setup | Sprint 1-2 | AuthService development (backend) parallel with PostgreSQL provisioning, CI/CD setup |
| M2 + Observability | Sprint 3-4 | TokenManager/JwtService development parallel with Prometheus metrics, Grafana dashboards, Redis provisioning |
| M3 + M4 frontend (partial) | Sprint 5-8 | Password reset backend (M3) parallel with LoginPage/RegisterPage/AuthProvider frontend (M4) |
| M5 rollout + Documentation | Sprint 9-11 | Phased rollout parallel with runbook finalization, API docs, integration guide |
| Testing runs alongside all phases | Sprint 1-11 | Unit tests with each sprint, integration tests at M1/M2/M3 exits, E2E at M4 exit, load test at M5 |

---

## 7. Success Metrics and Acceptance Criteria

### 7.1 Business Metrics (Tied to PRD Success Metrics)

| Metric | Target | Measurement | Measurement Point | Owner |
|--------|--------|-------------|-------------------|-------|
| Registration conversion rate | > 60% | Funnel: landing page visit -> registration form -> confirmed account | 30 days post-GA | Product team |
| Login response time (p95) | < 200ms | APM instrumentation on AuthService.login() | Continuous, from Sprint 2 | auth-team |
| Average session duration | > 30 minutes | Token refresh event analytics (time between first and last refresh) | 30 days post-GA | Product team |
| Failed login rate | < 5% of attempts | auth_login_total counter (failed / total) | Continuous, from Sprint 2 | Security team |
| Password reset completion | > 80% | Funnel: reset-request -> reset-confirm -> new password set | 30 days post-GA | Product team |
| Daily active authenticated users | > 1,000 within 30 days of GA | AuthToken issuance counts | 30 days post-GA | Product team |

### 7.2 Technical Acceptance Criteria (Per Milestone)

**M1 Acceptance:**

- [ ] POST `/auth/register` returns 201 for valid input, 409 for duplicate email, 400 for weak password
- [ ] POST `/auth/login` returns 200 with accessToken for valid credentials, 401 for invalid
- [ ] Account locks after 5 failed attempts in 15 minutes (423 response)
- [ ] No user enumeration: identical error responses for wrong-email and wrong-password
- [ ] bcrypt cost factor 12 verified, hash completes in < 500ms
- [ ] Unit test coverage > 80% for AuthService and PasswordHasher

**M2 Acceptance:**

- [ ] Login returns AuthToken with accessToken (15-min TTL) and refreshToken (7-day TTL)
- [ ] POST `/auth/refresh` with valid refreshToken returns new AuthToken pair, old token revoked
- [ ] POST `/auth/refresh` with expired/revoked token returns 401
- [ ] GET `/auth/me` returns UserProfile with valid token, 401 with invalid/expired token
- [ ] Token refresh latency p95 < 100ms
- [ ] Redis TTL correctly expires refresh tokens
- [ ] Unit test coverage > 80% for JwtService and TokenManager

**M3 Acceptance:**

- [ ] POST `/auth/reset-request` sends email within 60 seconds
- [ ] Reset token expires after 1 hour, single-use
- [ ] POST `/auth/reset-confirm` updates password and invalidates all sessions
- [ ] Identical response for registered and unregistered emails on reset-request
- [ ] All auth events logged with userId, eventType, timestamp, ipAddress, outcome
- [ ] Audit logs queryable by date range and user ID
- [ ] GDPR consent recorded at registration with timestamp

**M4 Acceptance:**

- [ ] LoginPage renders in < 1 second
- [ ] Registration + redirect to dashboard completes in < 2 seconds
- [ ] AuthProvider silently refreshes tokens before accessToken expiry
- [ ] ProfilePage displays displayName, email, createdAt
- [ ] Log Out ends session and redirects to landing page
- [ ] All E2E tests pass (Playwright)

**M5 Acceptance (GA):**

- [ ] 99.9% uptime over first 7 production days
- [ ] p95 latency < 200ms under production load
- [ ] Error rate < 0.1% during Beta (10% traffic)
- [ ] Zero P0/P1 bugs at GA
- [ ] Security review sign-off received
- [ ] Penetration test Critical/High findings remediated
- [ ] Runbooks published and reviewed
- [ ] Rollback procedure tested in staging
- [ ] Go/no-go sign-off from test-lead and eng-manager

### 7.3 Edge Case Coverage

| Edge Case | Expected Behavior | Verification |
|-----------|-------------------|--------------|
| Duplicate email at registration | Error suggesting login or password reset. No account created. | Integration test |
| Wrong password < 5 attempts | Generic "Invalid email or password" error. No user enumeration. | Unit test |
| Wrong password >= 5 attempts | Account locked (423). Admin notified. User told to try later or reset. | Integration test |
| Reset for unregistered email | Same success response as registered email. No email sent. No enumeration. | Unit test |
| Expired reset link (> 1 hour) | Clear error with option to request new link. | Integration test |
| Concurrent login from multiple devices | Both sessions valid. Multi-device is expected behavior. | Integration test |
| Token expires during active editing | Silent refresh if possible; otherwise preserve work locally and prompt login. | E2E test (frontend responsibility) |
| Weak password at registration | Inline validation shows unmet requirements. Form not submitted. | E2E test |
| Empty email or password fields | Validation error before submission. | Unit + E2E test |
| Email with leading/trailing whitespace | Trim before validation and storage. | Unit test |
| displayName < 2 chars or > 100 chars | Validation error. | Unit test |
| Concurrent registration with same email | Database unique constraint rejects second attempt. No race condition. | Integration test (concurrent requests) |
| JWT clock skew (> 5 seconds) | JwtService tolerates up to 5 seconds of clock skew. | Unit test |
| Redis unavailable during refresh | Reject refresh request with clear error. Do not serve stale tokens. | Integration test (Redis stopped) |
| Maximum refresh tokens per user | Source PRD lists this as Open Question. Recommend: 10 active refresh tokens per user, oldest evicted on new issuance. | Configuration + unit test |
| Roles array empty or missing | Default to ["user"] per UserProfile schema. | Unit test |
| lastLoginAt null (never logged in) | ProfilePage displays "N/A" or equivalent. | Frontend test |

---

## 8. Out of Scope

The following items are explicitly out of scope for this roadmap and the v1.0 release:

| Item | Rationale | Planned For |
|------|-----------|-------------|
| OAuth2/OIDC provider integration | Requires third-party infrastructure not yet available. Adds complexity without addressing core v1.0 needs. | v2.0 (NG-001) |
| Multi-factor authentication (TOTP, SMS) | Requires SMS/TOTP infrastructure. Separate security architecture review needed. | v1.1 (NG-002) |
| Social login (Google, GitHub, etc.) | Depends on OAuth2/OIDC infrastructure not yet available. | v2.0 |
| Role-based access control (RBAC) | Authorization is a separate concern from authentication. UserProfile includes a roles field but enforcement is out of scope. Dedicated PRD required. | Separate feature |
| API key authentication for service-to-service calls | Open question OQ-001. Deferred to v1.1 scope discussion. | v1.1 |
| Account deletion / right-to-be-forgotten (GDPR Article 17) | Not mentioned in PRD scope. Requires data anonymization strategy. | Post-v1.0 |
| Email verification as a registration step | PRD lists this as "(Optional)" in the customer journey. Not required for v1.0 launch. | v1.1 |
| "Remember me" extended session duration | Open question in PRD. Resolution needed before implementation if included. | TBD |
| Admin dashboard for user management | Admin user stories are limited to viewing audit logs. Full CRUD user management is out of scope. | v1.2+ |
| Account lockout self-service unlock | PRD specifies lockout notification to admin. Self-service unlock is not specified. | v1.1 |
| Password change (while logged in) | Not explicitly mentioned in PRD functional requirements. Only password reset (forgotten password) is in scope. | v1.1 |

---

## 9. Open Questions and Assumptions

### 9.1 Open Questions Requiring Resolution

| ID | Question | Owner | Resolution Deadline | Impact if Unresolved | Recommended Resolution |
|----|----------|-------|---------------------|---------------------|----------------------|
| OQ-A | Should password reset emails be sent synchronously or asynchronously? | Engineering | Before M3 Sprint 1 kickoff (Sprint 5) | Reset email delivery architecture undecided. | **Asynchronous** via Redis-backed job queue (Bull/BullMQ). Avoids blocking HTTP response. Provides retry semantics. Adds ~50 lines of code + Redis queue infrastructure. |
| OQ-B | Maximum number of refresh tokens allowed per user across devices? | Product | Before M2 Sprint 1 kickoff (Sprint 3) | Token storage sizing unclear. No eviction policy. | **10 active refresh tokens per user.** Oldest evicted on new issuance. Covers typical multi-device usage (phone, tablet, laptop, work computer, + spare). |
| OQ-C | Account lockout policy: should locked accounts auto-unlock after time period? | Security | Before M1 Sprint 1 kickoff (Sprint 1) | Lockout behavior undefined for ongoing operations. | **Auto-unlock after 30 minutes.** Admin can manually unlock earlier. User can always reset password to regain access. |
| OQ-D | Should "remember me" extend session duration beyond 7 days? | Product | Before M4 Sprint 1 kickoff (Sprint 7) | Frontend checkbox implementation unclear. | **Defer to v1.1.** v1.0 ships with fixed 7-day refresh token window. "Remember me" UX can be added later without breaking changes. |
| OQ-E | Maximum allowed UserProfile roles array length? (TDD OQ-002) | auth-team | 2026-04-01 | Validation logic incomplete. | **Default: 10 roles max.** Sufficient for current and near-term RBAC needs. Adjustable via configuration. |
| OQ-F | Should AuthService support API key authentication for service-to-service calls? (TDD OQ-001) | test-lead | 2026-04-15 | v1.1 scope boundary unclear. | **Defer to v1.1.** v1.0 supports only user-facing JWT auth. API key auth requires separate token type and revocation strategy. |

### 9.2 Assumptions

1. **Email delivery infrastructure (SendGrid) is available** before M3 development begins (Sprint 5). If unavailable, M3 is blocked and the schedule slips by the duration of the delay.

2. **PostgreSQL 15+ is provisioned and accessible** before M1 Sprint 1 (Sprint 1). This is a hard prerequisite for UserProfile persistence.

3. **Redis 7+ is provisioned and accessible** before M2 Sprint 1 (Sprint 3). This is a hard prerequisite for refresh token storage.

4. **The frontend supports client-side routing and token-based authentication.** The frontend framework must be configured before M4 (Sprint 7).

5. **SEC-POLICY-001 (password and token security policy) is finalized** before M1 Sprint 1. Without it, password policy enforcement cannot be implemented correctly.

6. **There is no existing legacy auth system** requiring migration. The PRD describes a greenfield implementation ("the platform currently operates without any user identity system"). If a legacy system exists, M5 must include migration scripts and the rollback procedure changes.

7. **Node.js 20 LTS is the runtime environment** per TDD Section 18. No Python, Go, or other runtime.

8. **The password policy minimum** is 8 characters, at least 1 uppercase letter, and at least 1 number (derived from FR-AUTH-002 AC3: "Weak passwords (< 8 chars, no uppercase, no number) return 400"). Special characters are not required but are accepted.

9. **RS256 key rotation is quarterly** per TDD Section 13, with a grace period where both old and new keys can validate tokens. Key rotation infrastructure should be architected in M2 even if the first rotation occurs post-GA.

10. **Cost estimate: $450/month for production** per TDD Section 26 (3 K8s pods $150, managed PostgreSQL $200, managed Redis $100). Budget approval assumed complete before infrastructure provisioning begins.

---

## 10. Capacity Planning and Resource Allocation

### 10.1 Team Composition

| Role | Allocation | Sprints Active |
|------|-----------|----------------|
| Backend Engineer 1 (AuthService + PasswordHasher) | 100% | Sprint 1-8 |
| Backend Engineer 2 (TokenManager + JwtService) | 100% | Sprint 3-8 |
| Backend Engineer 3 (Password reset + audit logging) | 100% | Sprint 5-8 |
| Frontend Engineer 1 (LoginPage + RegisterPage) | 100% | Sprint 7-8 |
| Frontend Engineer 2 (AuthProvider + ProfilePage + reset page) | 100% | Sprint 7-8 |
| QA Engineer | 50% | Sprint 1-4, 100% Sprint 5-11 |
| Security Engineer | 25% | Sprint 1-2 (policy), Sprint 9-10 (review) |
| DevOps Engineer | 25% | Sprint 1 (CI/CD), Sprint 4 (K8s), Sprint 9 (prod) |
| Product Manager | 10% | Sprint 1-11 (oversight, metric review) |

### 10.2 Infrastructure Sizing (from TDD Section 25.3)

| Resource | Initial Capacity | Scaling Trigger | Max Capacity |
|----------|-----------------|-----------------|--------------|
| AuthService pods | 3 replicas | CPU > 70% | 10 replicas (HPA) |
| PostgreSQL connection pool | 100 connections | Connection wait > 50ms | 200 connections |
| Redis memory | 1 GB (~100K tokens, ~50 MB) | > 70% utilized | 2 GB |

### 10.3 Cost Projection

| Component | Monthly Cost | Scaling Factor |
|-----------|-------------|----------------|
| Kubernetes pods (3 replicas) | $150 | +$50 per additional replica |
| Managed PostgreSQL | $200 | +$50 per 10K additional users |
| Managed Redis | $100 | +$50 when scaling to 2 GB |
| SendGrid (email delivery) | $0 (free tier initially) | Varies by volume |
| External pentest (one-time) | $5,000-$15,000 | N/A |
| **Total Monthly (production)** | **~$450** | ~$50/additional 10K users |

---

## 11. Timeline Summary

```
Sprint 1-2 (Weeks 1-4):  M1 — Core AuthService + PasswordHasher
                          Infrastructure: PostgreSQL provisioned, CI/CD setup

Sprint 3-4 (Weeks 5-8):  M2 — TokenManager + JwtService + Profile Endpoint
                          Infrastructure: Redis provisioned, K8s manifests
                          Security: RS256 key pair generated
                          Observability: Prometheus metrics, Grafana dashboards

Sprint 5-6 (Weeks 9-12): M3 — Password Reset + Audit Logging
                          External: SendGrid integration
                          Security: TLS 1.3 enforcement
                          Testing: Integration test coverage complete

Sprint 7-8 (Weeks 13-16): M4 — Frontend Integration
                           Components: LoginPage, RegisterPage, AuthProvider, ProfilePage
                           Testing: E2E tests (Playwright)

Sprint 9 (Weeks 17-18):  M5 Phase 1 — Internal Alpha (staging deploy)
                          M5 Phase 2 start — Beta (10% traffic)
                          Security: External penetration test

Sprint 10 (Weeks 19-20): M5 Phase 2 complete — Beta monitoring
                          Security: Review sign-off, pentest remediation
                          Load testing: k6 at 500 concurrent users

Sprint 11 (Weeks 21-22): M5 Phase 3 — GA (100% traffic)
                          Feature flags removed after 2 weeks stable
                          Documentation: Runbooks, API docs finalized
                          Post-GA: Begin v1.1 planning (MFA, API keys)
```

**Total Duration:** 22 weeks (~5.5 months), Sprint 1 through Sprint 11.

---

## 12. Rollback and Incident Response

### 12.1 Rollback Strategy

The phased rollout with feature flags (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) provides a rapid rollback mechanism. The procedure is:

1. **Immediate (< 2 minutes):** Disable `AUTH_NEW_LOGIN` feature flag. All traffic routes back to legacy behavior (or, for greenfield, displays a maintenance page).
2. **Verification (< 5 minutes):** Run smoke tests against the fallback path to confirm users can still access the platform.
3. **Investigation (ongoing):** Use structured logs and OpenTelemetry traces to diagnose the AuthService failure.
4. **Data recovery (if needed):** Restore UserProfile table from last known-good backup if data corruption is detected.
5. **Communication:** Notify auth-team and platform-team via incident channel. Post-mortem within 48 hours.

### 12.2 Incident Response During Rollout

During the Beta phase (10% traffic), auth-team provides 24/7 on-call coverage (TDD Section 25.2):

- **P1 response time:** Acknowledge within 15 minutes
- **Escalation path:** auth-team on-call -> test-lead -> eng-manager -> platform-team
- **Tooling access:** Kubernetes dashboards, Grafana, Redis CLI, PostgreSQL admin

### 12.3 Known Failure Modes

| Failure Mode | Detection | Automated Response | Manual Response |
|-------------|-----------|---------------------|-----------------|
| AuthService pod crash | Kubernetes liveness probe failure | Pod restart (K8s) | Investigate logs, scale up if recurring |
| PostgreSQL connection exhaustion | Connection pool wait > 50ms | Alert triggered | Increase pool size to 200 |
| Redis cluster failure | Redis connection failures > 10/min | Alert triggered, rollback triggered per TDD 19.4 | Failover to Redis replica, investigate |
| SendGrid outage | Password reset email bounce rate > 2% | Alert triggered | Postpone reset emails, provide admin manual reset |
| JWT signing key unavailable | JwtService initialization failure | AuthService fails health check, removed from load balancer | Remount secrets volume, restart pods |
| Runaway token issuance | Redis memory > 70% utilized | Alert triggered | Investigate token volume, add per-user token limits |

---

## 13. Post-GA Considerations

### 13.1 v1.1 Planning (Target: Q3 2026)

- Multi-factor authentication (TOTP via authenticator app) -- NG-002
- API key authentication for service-to-service calls -- OQ-001
- "Remember me" extended session duration -- OQ-D
- Email verification as registration step
- Password change while logged in
- Account self-service unlock after lockout

### 13.2 v2.0 Planning (Target: Q4 2026)

- OAuth2/OIDC provider integration -- NG-001
- Social login (Google, GitHub) -- PRD Out of Scope
- Role-based access control (RBAC) enforcement -- Separate PRD
- Admin dashboard for user management

### 13.3 Ongoing Maintenance

- Quarterly RS256 key rotation (first rotation at M5 + 3 months)
- bcrypt cost factor review (monitor NIST guidance, hardware improvements)
- SOC2 audit log retention verification (quarterly)
- Dependency updates (Node.js LTS, bcryptjs, jsonwebtoken, Redis, PostgreSQL)
- Capacity review when daily active authenticated users approach 10,000

---

## Appendix A: Requirement Traceability Matrix

| Requirement | Milestone | Deliverable(s) | Sprint |
|-------------|-----------|----------------|--------|
| FR-AUTH.1 (Login with session) | M1, M2 | D-005, D-012, D-015 | 2, 4 |
| FR-AUTH.2 (Registration) | M1 | D-004, D-009 | 1-2 |
| FR-AUTH.3 (Session persistence) | M2, M4 | D-012, D-041 | 4, 7-8 |
| FR-AUTH.4 (Profile retrieval) | M2, M4 | D-016, D-037 | 4, 8 |
| FR-AUTH.5 (Password reset) | M3, M4 | D-023, D-024, D-038 | 5-6, 8 |
| FR-AUTH-001 (Login endpoint) | M1, M2 | D-005, D-011, D-012 | 2, 4 |
| FR-AUTH-002 (Registration endpoint) | M1 | D-004 | 2 |
| FR-AUTH-003 (Token issuance + refresh) | M2 | D-011, D-012, D-015 | 3-4 |
| FR-AUTH-004 (Profile endpoint) | M2 | D-016 | 4 |
| FR-AUTH-005 (Password reset flow) | M3 | D-023, D-024, D-025 | 5-6 |
| NFR-AUTH.1 (Performance < 200ms) | M1, M2, M5 | D-001, D-011, D-053 | 2, 4, 9 |
| NFR-AUTH.2 (99.9% availability) | M5 | D-059 | 9-11 |
| NFR-AUTH.3 (Password hashing) | M1 | D-002 | 2 |
| NFR-PERF-001 (< 200ms p95) | M1, M2, M5 | D-001, D-053 | 2, 4, 9 |
| NFR-PERF-002 (500 concurrent) | M5 | D-053 | 9 |
| NFR-REL-001 (99.9% uptime) | M5 | D-059 | 9-11 |
| NFR-SEC-001 (bcrypt cost 12) | M1 | D-002 | 2 |
| NFR-SEC-002 (RS256 signing) | M2 | D-011 | 3 |
| GDPR consent at registration | M4 | D-035 | 7 |
| SOC2 audit logging | M3 | D-028, D-029, D-030 | 5-6 |
| NIST SP 800-63B password storage | M1 | D-002 | 2 |

---

## Appendix B: Feature Flag Lifecycle

| Flag | Created | Enabled | Disabled | Removed |
|------|---------|---------|----------|---------|
| `AUTH_NEW_LOGIN` | Sprint 8 (M5 prep) | Sprint 9 (Alpha) | On rollback only | Sprint 11 + 2 weeks |
| `AUTH_TOKEN_REFRESH` | Sprint 8 (M5 prep) | Sprint 9 (Alpha) | On rollback only | Sprint 11 + 4 weeks |

Both flags default to OFF. They are enabled per-phase during rollout and removed only after sustained production stability.

---

## Appendix C: API Endpoint Summary

| Endpoint | Method | Auth | Rate Limit | Milestone | Sprint |
|----------|--------|------|------------|-----------|--------|
| `/auth/login` | POST | No | 10 req/min/IP | M1 | 2 |
| `/auth/register` | POST | No | 5 req/min/IP | M1 | 2 |
| `/auth/refresh` | POST | No (body) | 30 req/min/user | M2 | 4 |
| `/auth/me` | GET | Bearer | 60 req/min/user | M2 | 4 |
| `/auth/reset-request` | POST | No | 5 req/min/IP | M3 | 6 |
| `/auth/reset-confirm` | POST | No | 5 req/min/IP | M3 | 6 |

Production URLs use `/v1/auth/*` prefix per TDD Section 8.4.
