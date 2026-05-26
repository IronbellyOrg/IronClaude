# User Authentication Service — Engineering Roadmap

> **Variant:** Sonnet (clarity-first, developer-actionable)
> **Generated:** 2026-05-22
> **Source:** merged-prd-tdd-user-auth.md (AUTH-MERGED-PRD-TDD)

---

## 1. Roadmap Overview

**Vision:** Deliver a production-grade User Authentication Service that enables secure, self-service identity management — registration, login, persistent sessions, profile retrieval, and password reset — forming the foundational identity layer for the entire personalization roadmap.

**Target Release:** v1.0 (Q2 2026)

**Total Estimated Duration:** 9 weeks (2026-04-07 through 2026-06-09)

**Phasing Summary:**

| Phase | Weeks | Milestones | Focus |
|-------|-------|------------|-------|
| Phase 1: Backend Core | W1-W4 | M1, M2 | AuthService, PasswordHasher, TokenManager, JwtService, all four API endpoints |
| Phase 2: Features + Frontend | W5-W7 | M3, M4 | Password reset flow, LoginPage, RegisterPage, AuthProvider, E2E integration |
| Phase 3: Rollout & GA | W8-W9 | M5 | Phased rollout (alpha -> beta 10% -> GA 100%), feature flag removal, stabilization |

---

## 2. Milestones

### M1: Core AuthService

| Field | Detail |
|-------|--------|
| **ID** | M1 |
| **Name** | Core AuthService |
| **Target Date** | 2026-04-14 (end of W2) |
| **Scope** | FR-AUTH-001 (login), FR-AUTH-002 (registration), NFR-SEC-001 (bcrypt hashing), NFR-PERF-001, NFR-PERF-002 |
| **Dependencies** | PostgreSQL 15+ provisioned; SEC-POLICY-001 approved; bcryptjs library vetted |
| **Effort** | 4 engineer-weeks (2 engineers x 2 weeks) |

**Deliverables:**

- `AuthService` class with `login()` and `register()` methods
- `PasswordHasher` module wrapping bcryptjs with cost factor 12
- `UserProfile` PostgreSQL schema (users table with id, email, password_hash, display_name, roles, created_at, updated_at, last_login_at)
- POST `/auth/register` endpoint — validates input, creates `UserProfile`, returns 201 or 409
- POST `/auth/login` endpoint — validates credentials, returns provisional response (no JWT until M2)
- Unit tests: >= 80% coverage on AuthService and PasswordHasher
- Integration tests: registration and login flows against real PostgreSQL instance (testcontainers)

**Exit Criteria:**

- [ ] `PasswordHasher.hash()` completes in < 500ms at cost factor 12 (benchmarked)
- [ ] `PasswordHasher.verify()` correctly validates known-good and known-bad password pairs
- [ ] POST `/auth/register` returns 201 for valid input, 409 for duplicate email, 400 for weak password
- [ ] POST `/auth/login` returns valid response for correct credentials, 401 for incorrect (generic error, no user enumeration)
- [ ] Account lockout triggers after 5 failed attempts within 15 minutes
- [ ] All passwords stored as bcrypt hashes; zero instances of plaintext in logs or responses
- [ ] >= 80% unit test coverage on AuthService and PasswordHasher

---

### M2: Token Management

| Field | Detail |
|-------|--------|
| **ID** | M2 |
| **Name** | Token Management |
| **Target Date** | 2026-04-28 (end of W4) |
| **Scope** | FR-AUTH-003 (token issuance and refresh), FR-AUTH-004 (profile retrieval), NFR-SEC-002 (RS256 signing), NFR-REL-001 |
| **Dependencies** | M1 complete; Redis 7+ provisioned; jsonwebtoken library vetted; RS256 key pair generated |
| **Effort** | 4 engineer-weeks (2 engineers x 2 weeks) |

**Deliverables:**

- `JwtService` module — signs and verifies JWTs with RS256 using 2048-bit RSA keys
- `TokenManager` module — issues `AuthToken` pairs, stores hashed refresh tokens in Redis with 7-day TTL, handles refresh and revocation
- `AuthToken` model (accessToken: JWT with 15-min TTL, refreshToken: opaque with 7-day TTL, expiresIn: 900, tokenType: "Bearer")
- Update POST `/auth/login` to return `AuthToken` pair via `TokenManager`
- POST `/auth/refresh` endpoint — exchanges valid refresh token for new `AuthToken` pair, revokes old token
- GET `/auth/me` endpoint — returns `UserProfile` for authenticated user from JWT payload
- Redis storage schema for refresh tokens (hashed, keyed by user ID + token ID)
- Unit tests: >= 80% coverage on TokenManager and JwtService
- Integration tests: token refresh flow against real Redis instance; expired/revoked token rejection

**Exit Criteria:**

- [ ] `JwtService.sign()` produces valid RS256 JWTs with correct claims (sub, exp, iat, roles)
- [ ] `JwtService.verify()` rejects expired, malformed, and wrongly-signed tokens
- [ ] Clock skew tolerance of 5 seconds implemented in `JwtService`
- [ ] `TokenManager.issueTokens()` stores hashed refresh token in Redis with 7-day TTL
- [ ] POST `/auth/refresh` with valid token returns new `AuthToken` pair and revokes old token
- [ ] POST `/auth/refresh` with expired/revoked token returns 401
- [ ] GET `/auth/me` with valid accessToken returns correct `UserProfile` (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles)
- [ ] GET `/auth/me` with invalid/expired token returns 401
- [ ] Redis unavailability causes `TokenManager` to reject refresh requests (not serve stale tokens)
- [ ] >= 80% unit test coverage on TokenManager and JwtService

---

### M3: Password Reset

| Field | Detail |
|-------|--------|
| **ID** | M3 |
| **Name** | Password Reset |
| **Target Date** | 2026-05-12 (end of W6) |
| **Scope** | FR-AUTH-005 (password reset flow), GDPR consent at registration, SOC2 audit logging |
| **Dependencies** | M1 complete; SendGrid API key provisioned; email templates designed |
| **Effort** | 3 engineer-weeks (2 engineers x 1.5 weeks) |

**Deliverables:**

- POST `/auth/reset-request` endpoint — generates time-limited reset token, sends email via SendGrid
- POST `/auth/reset-confirm` endpoint — validates reset token, updates password via `PasswordHasher`, invalidates all existing sessions
- Reset token storage in Redis with 1-hour TTL, single-use enforcement
- Email delivery integration with SendGrid (reset email template, delivery monitoring)
- Same-response-for-all-emails behavior: registered and unregistered emails produce identical responses (no user enumeration)
- GDPR consent field and timestamp added to `UserProfile` schema
- Audit log table (PostgreSQL): user_id, event_type, timestamp, ip_address, outcome — 12-month retention
- Structured logging for all auth events (login, registration, token refresh, password reset)
- Integration tests: full reset flow end-to-end; token expiry; single-use enforcement

**Exit Criteria:**

- [ ] POST `/auth/reset-request` with registered email sends reset email within 60 seconds
- [ ] POST `/auth/reset-request` with unregistered email returns identical success response (no enumeration)
- [ ] Reset tokens expire after 1 hour; expired tokens return clear error with re-request option
- [ ] Used reset tokens cannot be reused (single-use enforced)
- [ ] Successful password reset invalidates all existing sessions and refresh tokens for that user
- [ ] GDPR consent recorded with timestamp at registration
- [ ] Audit log captures all auth events with user ID, event type, timestamp, IP, and outcome
- [ ] Password is never logged or returned in any API response

---

### M4: Frontend Integration

| Field | Detail |
|-------|--------|
| **ID** | M4 |
| **Name** | Frontend Integration |
| **Target Date** | 2026-05-26 (end of W8) |
| **Scope** | G-005 (frontend integration), FR-AUTH-001 through FR-AUTH-005 (frontend consumption), UX requirements from PRD |
| **Dependencies** | M2 complete (API endpoints functional); M3 complete (reset flow available for frontend); frontend routing framework available |
| **Effort** | 3 engineer-weeks (2 frontend engineers x 1.5 weeks) |

**Deliverables:**

- `LoginPage` component — email/password form, calls POST `/auth/login`, stores `AuthToken` via `AuthProvider`, redirect on success
- `RegisterPage` component — email/password/displayName form with inline validation (password strength), calls POST `/auth/register`, consent checkbox for GDPR, redirect to dashboard on success
- `AuthProvider` context wrapper — manages `AuthToken` state, silent token refresh when accessToken nears expiry, intercepts 401 responses, stores accessToken in memory only (not localStorage), clears tokens on tab close
- ProfilePage component — calls GET `/auth/me`, displays displayName, email, createdAt
- Password reset UI — "Forgot Password" link on LoginPage, email submission form, new password form
- Route guards: unauthenticated users redirected to LoginPage; authenticated users redirected away from LoginPage/RegisterPage
- E2E tests (Playwright): full registration -> login -> profile view journey; token refresh under simulated expiry; password reset flow
- CORS configuration on API Gateway restricted to known frontend origins

**Exit Criteria:**

- [ ] `LoginPage` successfully authenticates and redirects to dashboard
- [ ] `RegisterPage` creates account with inline validation and GDPR consent
- [ ] `AuthProvider` silently refreshes tokens when accessToken is within 1 minute of expiry
- [ ] `AuthProvider` redirects to LoginPage on expired/revoked refresh token
- [ ] ProfilePage displays correct user data from GET `/auth/me`
- [ ] Password reset flow works end-to-end from "Forgot Password" through new password
- [ ] No user enumeration possible through frontend error messages or timing differences
- [ ] E2E test suite passes: registration journey, login journey, token refresh, password reset
- [ ] CORS rejects requests from unauthorized origins

---

### M5: GA Release

| Field | Detail |
|-------|--------|
| **ID** | M5 |
| **Name** | GA Release |
| **Target Date** | 2026-06-09 (end of W9) |
| **Scope** | All FRs and NFRs; rollout phases 1-3; monitoring; runbooks; feature flag lifecycle |
| **Dependencies** | M1-M4 complete; security review passed; penetration testing complete; performance test under 500 concurrent users passed |
| **Effort** | 2 engineer-weeks (2 engineers x 1 week) |

**Deliverables:**

- Phased rollout execution: Phase 1 (Internal Alpha, 1 week) -> Phase 2 (Beta 10%, 2 weeks) -> Phase 3 (GA 100%, 1 week)
- Feature flags configured in production: `AUTH_NEW_LOGIN` (OFF), `AUTH_TOKEN_REFRESH` (OFF)
- Monitoring dashboards: `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total`
- Alerting rules: login failure rate > 20% over 5 min; p95 latency > 500ms; Redis connection failures > 10/min
- Runbook published for AuthService down and token refresh failure scenarios
- Rollback procedure tested in staging
- 24/7 on-call rotation for auth-team during first 2 weeks post-GA
- Feature flag removal: `AUTH_NEW_LOGIN` after Phase 3; `AUTH_TOKEN_REFRESH` 2 weeks after Phase 3
- Capacity planning validated: 3 AuthService replicas, PostgreSQL pool 100, Redis 1GB

**Exit Criteria:**

- [ ] All FR-AUTH-001 through FR-AUTH-005 pass manual and automated testing with zero P0/P1 bugs
- [ ] Unit test coverage >= 80% for AuthService, TokenManager, JwtService, PasswordHasher
- [ ] Integration tests pass against real PostgreSQL and Redis for all four API endpoints
- [ ] Security review completed: bcrypt cost factor 12 verified, RS256 key rotation documented, OWASP review passed
- [ ] Performance: all endpoints < 200ms p95 under 500 concurrent users (k6 load test)
- [ ] Phased rollout complete: 100% traffic on new AuthService
- [ ] 99.9% uptime over first 7 days in production
- [ ] Monitoring dashboards green; no unresolved P1 alerts
- [ ] Runbooks reviewed and accessible to on-call team
- [ ] Go/no-go sign-off from test-lead and eng-manager

---

## 3. Workstreams

### WS-A: Backend Core (auth-team)

**Owner:** auth-team (2 backend engineers)

**Sequencing:**

| Week | Activity |
|------|----------|
| W1-W2 | M1: AuthService, PasswordHasher, UserProfile schema, /auth/register, /auth/login |
| W3-W4 | M2: TokenManager, JwtService, AuthToken model, /auth/refresh, /auth/me |
| W5-W6 | M3: Password reset endpoints, SendGrid integration, audit logging, GDPR consent |

**Handoffs:**

- W2 -> WS-B: API contract finalized (/auth/register, /auth/login request/response schemas)
- W4 -> WS-B: Token refresh contract finalized (/auth/refresh request/response, AuthToken structure)
- W6 -> WS-C: Audit log schema and query interface available for observability dashboard

---

### WS-B: Frontend (frontend-team)

**Owner:** frontend-team (2 frontend engineers)

**Sequencing:**

| Week | Activity |
|------|----------|
| W1-W4 | Parallel development: LoginPage, RegisterPage component scaffolding; AuthProvider state management design; mock API integration |
| W5-W6 | Staged integration: wire LoginPage and RegisterPage to staging API; implement AuthProvider token refresh; ProfilePage and password reset UI |
| W7-W8 | M4 full integration: E2E test suite, CORS validation, UX polish, accessibility review |

**Handoffs:**

- W4 -> WS-A: Frontend consumes finalized /auth/login and /auth/register contracts
- W8 -> WS-D: Frontend ready for phased rollout behind AUTH_NEW_LOGIN feature flag

---

### WS-C: Observability & Compliance (platform-team)

**Owner:** platform-team (1 engineer, part-time)

**Sequencing:**

| Week | Activity |
|------|----------|
| W1-W2 | Provision PostgreSQL 15+, Redis 7+; configure connection pooling; generate RS256 key pair |
| W3-W4 | Prometheus metrics setup: auth_login_total, auth_login_duration_seconds, auth_token_refresh_total, auth_registration_total |
| W5-W6 | Audit log schema design; SOC2 log retention policy (12-month); GDPR consent validation |
| W7-W8 | Grafana dashboards; alert rules; runbook authoring |

**Handoffs:**

- W2 -> WS-A: PostgreSQL and Redis available in staging and CI environments
- W4 -> WS-A: Prometheus scrape endpoint documented; auth metrics available for instrumentation
- W8 -> WS-D: Monitoring dashboards and alerting rules ready for production rollout

---

### WS-D: Security & Release (security-team + auth-team lead)

**Owner:** security-team (1 engineer) + auth-team lead

**Sequencing:**

| Week | Activity |
|------|----------|
| W3 | Security checkpoint 1: review PasswordHasher bcrypt cost, input validation, no plaintext logging |
| W5 | Security checkpoint 2: review JwtService RS256 configuration, key rotation plan, refresh token hashing in Redis |
| W7 | Penetration testing against staging environment; OWASP Authentication Cheat Sheet compliance review |
| W8-W9 | Feature flag configuration; phased rollout execution; rollback drill; post-GA monitoring |

**Handoffs:**

- W5 -> WS-A: Security review findings actioned before password reset flow ships
- W7 -> M5: Pen test report with zero critical findings required before Phase 1 rollout

---

## 4. Requirement Traceability

| Requirement | Description | Owning Milestone | Owning Workstream | Acceptance Test |
|-------------|-------------|-----------------|-------------------|-----------------|
| FR-AUTH-001 | Login with email/password | M1 | WS-A (Backend Core) | Unit: valid/invalid credentials; Integration: full login flow to PostgreSQL |
| FR-AUTH-002 | User registration with validation | M1 | WS-A (Backend Core) | Unit: valid registration, duplicate email (409), weak password (400); Integration: UserProfile persisted |
| FR-AUTH-003 | JWT token issuance and refresh | M2 | WS-A (Backend Core) | Unit: JwtService sign/verify, TokenManager issue/refresh/revoke; Integration: Redis token lifecycle |
| FR-AUTH-004 | User profile retrieval | M2 | WS-A (Backend Core) | Unit: valid token returns profile, expired token returns 401; Integration: GET /auth/me against PostgreSQL |
| FR-AUTH-005 | Password reset flow | M3 | WS-A (Backend Core) | Integration: full reset-request -> email -> reset-confirm flow; single-use enforcement; 1-hour expiry |
| NFR-PERF-001 | < 200ms p95 response time | M5 | WS-D (Security & Release) | k6 load test: 500 concurrent users, p95 < 200ms on all endpoints |
| NFR-PERF-002 | 500 concurrent requests | M5 | WS-D (Security & Release) | k6 load test: sustained 500 concurrent logins without degradation |
| NFR-REL-001 | 99.9% availability | M5 | WS-C (Observability) | Uptime monitoring over 30-day rolling window post-GA |
| NFR-SEC-001 | bcrypt cost factor 12 | M1 | WS-A (Backend Core) | Unit test: assert bcrypt cost parameter = 12; benchmark hash < 500ms |
| NFR-SEC-002 | RS256 2048-bit keys | M2 | WS-A (Backend Core) | Unit test: assert JwtService uses RS256 algorithm; key length validation |
| G-001 | Secure registration/login | M1 | WS-A (Backend Core) | All FR-AUTH-001 and FR-AUTH-002 tests pass |
| G-002 | Stateless token sessions | M2 | WS-A (Backend Core) | All FR-AUTH-003 tests pass |
| G-003 | Self-service password reset | M3 | WS-A (Backend Core) | All FR-AUTH-005 tests pass |
| G-004 | Profile management | M2 | WS-A (Backend Core) | All FR-AUTH-004 tests pass |
| G-005 | Frontend integration | M4 | WS-B (Frontend) | E2E: RegisterPage -> LoginPage -> ProfilePage journey |

---

## 5. Critical Path & Dependencies

### 5.1 Sequenced Dependency Chain

```
SEC-POLICY-001 approved
    |
    v
PostgreSQL 15+ provisioned ──────────────────────────────┐
Redis 7+ provisioned ──────────────────────────────────┐  |
    |                                                   |  |
    v                                                   v  v
M1: AuthService + PasswordHasher ──────────────────────►M2: TokenManager + JwtService
    |                                                      |
    |                                                      v
    |                                                   M4: Frontend Integration
    |                                                      ^
    v                                                      |
M3: Password Reset + Audit Logging ───────────────────────┘
    |
    v
Security Review (bcrypt, RS256, OWASP) ── Penetration Testing
    |
    v
M5: GA Release (Phase 1 Alpha -> Phase 2 Beta -> Phase 3 GA)
```

### 5.2 External Dependencies

| Dependency | Provider | Impact if Unavailable | Status | Resolution Deadline |
|------------|----------|-----------------------|--------|---------------------|
| SendGrid API | External SaaS | Password reset flow blocked (FR-AUTH-005) | Pending provision | 2026-04-07 (W1) |
| PostgreSQL 15+ | Infrastructure | No UserProfile persistence; AuthService cannot function | Pending provision | 2026-04-07 (W1) |
| Redis 7+ | Infrastructure | No refresh token storage; TokenManager cannot function | Pending provision | 2026-04-21 (W3) |
| SEC-POLICY-001 | Security team | Password and token policies undefined; blocking M1 design | Pending approval | 2026-04-07 (W1) |
| RS256 key pair | Security team | JwtService cannot sign tokens; blocking M2 | Pending generation | 2026-04-21 (W3) |

### 5.3 Internal Component Dependencies

```
AuthService
    ├── PasswordHasher (bcrypt hash/verify) — M1
    ├── UserRepo (PostgreSQL read/write) — M1
    └── TokenManager — M2
         └── JwtService (RS256 sign/verify) — M2
              └── RSA key pair — provisioned W3

AuthProvider (frontend)
    ├── consumes POST /auth/login — M1 backend, W5 frontend
    ├── consumes POST /auth/register — M1 backend, W5 frontend
    ├── consumes POST /auth/refresh — M2 backend, W6 frontend
    └── consumes GET /auth/me — M2 backend, W6 frontend
```

### 5.4 Risk-Bearing Dependencies

| Dependency | Risk | Mitigation |
|------------|------|------------|
| SendGrid deliverability | Email latency or delivery failures block password reset | Delivery monitoring with alert on > 60s send time; fallback support channel for manual reset |
| Redis availability during M2 | TokenManager cannot issue or validate refresh tokens | Redis cluster with sentinel; fallback: reject refresh requests, force re-login via LoginPage |
| SEC-POLICY-001 approval timeline | Blocks PasswordHasher configuration and cost factor decision | Escalate to security-team lead if not approved by W1; use NIST SP 800-63B as interim baseline |
| RS256 key pair generation | Blocks JwtService implementation | Generate self-signed pair for development; coordinate with security-team for production keys by W3 |

---

## 6. Risk Register & Mitigations

| ID | Risk | Likelihood | Impact | Mitigation | Contingency | Owning Milestone | Trigger |
|----|------|-----------|--------|------------|-------------|-----------------|---------|
| R-001 | Token theft via XSS allows session hijacking | Medium | High | Store accessToken in memory only (not localStorage); AuthProvider clears tokens on tab close; HttpOnly cookies for refreshToken; JwtService 15-minute expiry limits exposure window | Immediate revocation via TokenManager; force password reset for affected UserProfile accounts; security incident post-mortem | M2, M4 | XSS vulnerability report or suspicious token usage pattern detected |
| R-002 | Brute-force attacks on login endpoint | High | Medium | API Gateway rate limiting: 10 req/min per IP; AuthService account lockout after 5 failed attempts in 15 min; PasswordHasher bcrypt cost 12 makes offline cracking expensive | Block offending IPs at WAF; enable CAPTCHA on LoginPage after 3 failed attempts; notify user of suspicious activity | M1, M4 | Login failure rate exceeds 20% over 5-minute window for any single IP |
| R-003 | Data loss during migration from legacy auth | Low | High | AuthService runs parallel with legacy during Phase 1 and Phase 2; UserProfile migration uses idempotent upsert operations; full database backup before each phase | Rollback to legacy auth; restore UserProfile from pre-migration backup; post-mortem within 48 hours | M5 | Any data loss or corruption detected in UserProfile records |
| R-004 | SendGrid outage blocks password reset | Low | Medium | Email delivery monitoring with alerting on send latency > 60s; queue reset emails with retry (3 attempts over 15 min); fallback support channel for manual password reset | Activate support-team manual reset workflow; post SendGrid status page notice to users | M3 | Password reset email delivery latency exceeds 60 seconds or delivery failure rate > 5% |
| R-005 | Redis cluster failure during production | Medium | High | Redis cluster with sentinel for HA; TokenManager fallback rejects refresh requests rather than serving stale tokens; users forced to re-login via LoginPage | Scale Redis cluster; re-mount persistence volume; if data loss, all users re-login (refresh tokens regenerated) | M5 | TokenManager Redis connection failures exceed 10 per minute |
| R-006 | Registration conversion below 60% target | Medium | Medium | Usability testing before launch (M4); inline validation on RegisterPage; A/B test form field count and CTA copy; monitor funnel analytics weekly post-GA | Simplify registration to email + password only (remove displayName); add social proof or incentive messaging | M4, M5 | Registration conversion below 50% in first 2 weeks of beta |
| R-007 | Concurrent registration race condition | Low | Medium | PostgreSQL unique constraint on email column; AuthService handles 409 gracefully with helpful error suggesting login or password reset | No additional action needed — database constraint is the safety net | M1 | Duplicate key violation in users table (monitored via structured logs) |

---

## 7. Rollout & Release Gates

### 7.1 Phase 1: Internal Alpha (1 week)

| Gate | Criteria |
|------|----------|
| **Entry** | M1-M4 complete; all E2E tests pass; security review checkpoint 1 and 2 passed |
| **Scope** | auth-team + QA test all four API endpoints; LoginPage and RegisterPage available behind `AUTH_NEW_LOGIN` flag |
| **Exit** | All FR-AUTH-001 through FR-AUTH-005 pass manual testing; zero P0/P1 bugs; AuthService deployed to staging and smoke-tested |
| **Duration** | 2026-05-26 through 2026-06-01 |

### 7.2 Phase 2: Beta 10% (2 weeks)

| Gate | Criteria |
|------|----------|
| **Entry** | Phase 1 exit criteria met; penetration testing complete with zero critical findings |
| **Scope** | Enable `AUTH_NEW_LOGIN` for 10% of traffic; monitor AuthService latency, error rates, TokenManager Redis usage; AuthProvider handles token refresh under real load |
| **Exit** | p95 latency < 200ms; error rate < 0.1%; zero TokenManager Redis connection failures; no P0 bugs |
| **Duration** | 2026-06-02 through 2026-06-08 |

### 7.3 Phase 3: GA 100% (1 week)

| Gate | Criteria |
|------|----------|
| **Entry** | Phase 2 exit criteria met; go/no-go sign-off from test-lead and eng-manager |
| **Scope** | Remove `AUTH_NEW_LOGIN` feature flag; all users route through new AuthService; enable `AUTH_TOKEN_REFRESH` flag |
| **Exit** | 99.9% uptime over first 7 days; all monitoring dashboards green; feature flags removed per schedule |
| **Duration** | 2026-06-09 through 2026-06-15 (stabilization) |

### 7.4 Feature Flag Plan

| Flag | Purpose | Default | Enable At | Remove After |
|------|---------|---------|-----------|--------------|
| `AUTH_NEW_LOGIN` | Gates access to new LoginPage and AuthService login endpoint | OFF | Phase 2 start (10% traffic) | Phase 3 GA confirmed (2026-06-15) |
| `AUTH_TOKEN_REFRESH` | Enables refresh token flow in TokenManager; when OFF, only access tokens issued | OFF | Phase 3 start (100% traffic) | Phase 3 + 2 weeks (2026-06-29) |

### 7.5 Rollback Triggers and Procedures

**Rollback triggers** (any single condition):

- p95 latency exceeds 1000ms for more than 5 minutes
- Error rate exceeds 5% for more than 2 minutes
- TokenManager Redis connection failures exceed 10 per minute
- Any data loss or corruption detected in UserProfile records
- Security incident requiring immediate service isolation

**Rollback procedure:**

1. Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth
2. Verify legacy login flow is operational via smoke tests
3. Investigate AuthService failure root cause using structured logs and OpenTelemetry traces
4. If UserProfile data corruption detected, restore from last known-good backup
5. Notify auth-team and platform-team via incident channel
6. Post-mortem within 48 hours of rollback

---

## 8. Quality & Testing Gates

### 8.1 Coverage Targets

| Milestone | Unit Coverage | Integration Coverage | E2E Coverage | Tooling |
|-----------|--------------|---------------------|-------------|---------|
| M1 | >= 80% on AuthService, PasswordHasher | Registration + login flows against PostgreSQL (testcontainers) | Not applicable | Jest, ts-jest, Supertest, testcontainers |
| M2 | >= 80% on TokenManager, JwtService | Token refresh against Redis; profile retrieval against PostgreSQL | Not applicable | Jest, ts-jest, Supertest, testcontainers |
| M3 | >= 80% on reset service methods | Full reset-request -> email -> reset-confirm flow; single-use enforcement; expiry | Not applicable | Jest, Supertest, testcontainers |
| M4 | Not applicable | API integration via AuthProvider | Full journey: RegisterPage -> LoginPage -> ProfilePage; token refresh; password reset | Playwright |
| M5 | All prior gates sustained | All four endpoints against real infra | Full regression suite | k6 (load), Playwright (E2E) |

### 8.2 Security Review Checkpoints

| Checkpoint | Timing | Scope | Gate |
|------------|--------|-------|------|
| Checkpoint 1 | W3 (after M1) | PasswordHasher bcrypt cost factor 12 verified; no plaintext passwords in logs or responses; input validation prevents SQL injection and XSS on registration | Pass required before M2 begins |
| Checkpoint 2 | W5 (after M2) | JwtService RS256 2048-bit key configuration; refresh tokens hashed in Redis; TLS 1.3 enforced on all endpoints; CORS restricted to known frontend origins | Pass required before M3 begins |
| Checkpoint 3 (Pen test) | W7 | Full OWASP Authentication Cheat Sheet compliance; no user enumeration on login, registration, or reset; account lockout mechanism validated; token theft scenario tested | Zero critical findings required before Phase 1 rollout |

### 8.3 Performance Gate

| Metric | Target | Measurement | Gate Timing |
|--------|--------|-------------|-------------|
| Login response time (p95) | < 200ms | k6 load test, 500 concurrent users | M5 Phase 1 entry |
| Registration response time (p95) | < 200ms | k6 load test, 500 concurrent users | M5 Phase 1 entry |
| Token refresh latency (p95) | < 100ms | APM on TokenManager.refresh() | M5 Phase 2 entry |
| PasswordHasher hash time | < 500ms | Benchmark at cost factor 12 | M1 exit |
| JwtService sign/verify | < 5ms | Micro-benchmark | M2 exit |
| TokenManager Redis operations | < 10ms | Redis latency monitoring | M2 exit |

### 8.4 Compliance Gate

| Requirement | Standard | Verification | Timing |
|-------------|----------|-------------|--------|
| Password storage: one-way adaptive hashing | NIST SP 800-63B | Unit test: assert bcrypt cost >= 12; audit: no plaintext passwords in any log or response | M1 exit |
| Audit logging with 12-month retention | SOC2 Type II | Integration test: every auth event produces audit log entry with user_id, event_type, timestamp, ip, outcome; retention policy verified | M3 exit |
| Consent at registration with timestamp | GDPR | Integration test: registration without consent checkbox fails; consent timestamp recorded in UserProfile | M3 exit |
| Data minimization | GDPR | Schema review: only email, hashed password, displayName stored; no additional PII | M1 exit |
| TLS 1.3 on all endpoints | Security policy | Infrastructure config review; automated TLS scan | M5 Phase 1 entry |

---

## 9. Open Questions & Decisions Needed

### PRD Open Questions

| # | Question | Owner | Decision Deadline | Blocking Milestone | Recommendation |
|---|----------|-------|-------------------|-------------------|----------------|
| 1 | Should password reset emails be sent synchronously or asynchronously? | Engineering | 2026-04-07 (W1) | M1 | Send asynchronously via queue. Synchronous send blocks the login response and degrades p95 latency. Queue with retry handles SendGrid transient failures. |
| 2 | Maximum number of refresh tokens allowed per user across devices? | Product | 2026-04-21 (W3) | M2 | Limit to 5 concurrent refresh tokens per user. Oldest token evicted when limit reached. Balances multi-device support with Redis memory and token theft surface area. |
| 3 | Account lockout policy after N consecutive failed login attempts? | Security | 2026-04-07 (W1) | M1 | Lock after 5 failed attempts within 15 minutes (already specified in TDD FR-AUTH-001). Unlock after 30-minute cooldown or via password reset. |
| 4 | Should we support "remember me" to extend session duration? | Product | 2026-05-12 (W6) | M4 | Defer to v1.1. Current 7-day refresh window is sufficient for v1.0. Adding "remember me" introduces UX complexity (checkbox, extended TTL, security review) that does not justify the engineering cost in this release. |

### TDD Open Questions

| ID | Question | Owner | Decision Deadline | Blocking Milestone | Recommendation |
|----|----------|-------|-------------------|-------------------|----------------|
| OQ-001 | Should AuthService support API key authentication for service-to-service calls? | test-lead | 2026-04-15 (W2) | M2 (design only) | Defer to v1.1. Design the AuthService interface to accept multiple authentication strategies (strategy pattern) so API key auth can be added without breaking changes. Do not implement in v1.0. |
| OQ-002 | What is the maximum allowed UserProfile roles array length? | auth-team | 2026-04-07 (W1) | M1 (schema design) | Set maximum to 10 roles. RBAC is out of scope for v1.0 (NG-003), but the roles field exists in UserProfile. A limit of 10 is generous for future RBAC while preventing unbounded array growth in PostgreSQL. |

---

## 10. Success Metrics & Measurement

### 10.1 PRD Success Metrics

| Metric | Target | Instrumentation | Review Milestone |
|--------|--------|-----------------|------------------|
| Registration conversion rate | > 60% | Funnel analytics: landing page view -> RegisterPage submit -> 201 response -> dashboard load. Instrumented via frontend analytics SDK on RegisterPage component. | M5 (2 weeks post-GA) |
| Login response time (p95) | < 200ms | APM histogram on POST /auth/login via OpenTelemetry span. Prometheus metric: `auth_login_duration_seconds` (histogram). Grafana dashboard p95 aggregation over 5-minute windows. | M2 (continuous); M5 (load test gate) |
| Average session duration | > 30 minutes | Token refresh event analytics: measure time between first AuthToken issuance and last refresh per user-session. Derived from TokenManager Redis keys with TTL tracking. | M5 (2 weeks post-GA) |
| Failed login rate | < 5% of attempts | Auth event log analysis: count 401 responses on POST /auth/login divided by total login attempts. Prometheus counter: `auth_login_total{status="failure"}` / `auth_login_total`. Alert if > 5% sustained over 1 hour. | M5 (continuous post-GA) |
| Password reset completion | > 80% | Funnel: POST /auth/reset-request -> email delivery confirmed -> POST /auth/reset-confirm. Tracked via audit log event_type correlation (reset_requested -> reset_completed). | M5 (2 weeks post-GA) |

### 10.2 TDD Technical Metrics

| Metric | Target | Instrumentation | Review Milestone |
|--------|--------|-----------------|------------------|
| Login response time (p95) | < 200ms | APM on `AuthService.login()` — OpenTelemetry span with `auth.login` operation name | M2 (automated check); M5 (load test) |
| Registration success rate | > 99% | Ratio: 201 responses / total POST /auth/register attempts. Prometheus counter: `auth_registration_total{status="success"}` / `auth_registration_total`. | M5 (continuous) |
| Token refresh latency (p95) | < 100ms | APM on `TokenManager.refresh()` — OpenTelemetry span with `auth.token.refresh` operation name | M2 (automated check); M5 (load test) |
| Service availability | 99.9% uptime | Health check endpoint `/health` polled every 30s. Uptime calculated over 30-day rolling windows. | M5 (30-day post-GA) |
| Password hash time | < 500ms | Benchmark of `PasswordHasher.hash()` in CI pipeline. Fail build if > 500ms at cost factor 12. | M1 (CI gate) |
| User registration conversion | > 60% | Same as PRD metric above | M5 (2 weeks post-GA) |
| Daily active authenticated users | > 1000 within 30 days of GA | `AuthToken` issuance count: unique user IDs with at least one token issued in 24-hour window. Queried from Prometheus `auth_login_total` grouped by user_id cardinality. | M5 (30 days post-GA) |

### 10.3 Post-Launch Review Schedule

| Review | Timing | Scope | Attendees |
|--------|--------|-------|-----------|
| Week 1 health check | 2026-06-16 (1 week post-GA) | System stability, error rates, latency p95, Redis memory usage, registration conversion funnel | auth-team, platform-team, product |
| Week 2 metrics review | 2026-06-23 (2 weeks post-GA) | All 5 PRD success metrics + 7 TDD technical metrics; on-call incident review; feature flag removal readiness | auth-team, product, security |
| Week 4 success gate | 2026-07-07 (4 weeks post-GA) | Final assessment against all success targets; decision to remove AUTH_TOKEN_REFRESH flag; capacity review; v1.1 planning kickoff | auth-team, product, engineering manager |
| Day-30 DAU check | 2026-07-09 (30 days post-GA) | Confirm > 1000 daily active authenticated users | product, auth-team |

---

## Appendix A: Invariant & Edge Case Coverage

| Invariant / Edge Case | Owning Component | Test Level | Milestone |
|-----------------------|------------------|------------|-----------|
| No user enumeration on login (identical error for wrong email and wrong password) | AuthService | Unit + Integration | M1 |
| No user enumeration on password reset (identical response for registered and unregistered email) | AuthService | Integration | M3 |
| Password never logged or returned in API response | AuthService, PasswordHasher | Unit (log assertion) | M1 |
| Account lockout after 5 failed attempts within 15 min | AuthService | Unit + Integration | M1 |
| Clock skew tolerance of 5 seconds in JWT validation | JwtService | Unit | M2 |
| Redis unavailability causes TokenManager to reject refresh (not serve stale tokens) | TokenManager | Integration (Redis disconnect test) | M2 |
| Concurrent registration with same email handled by DB unique constraint | AuthService + PostgreSQL | Integration (parallel requests) | M1 |
| Single-use reset tokens (cannot be reused after successful reset) | AuthService + Redis | Integration | M3 |
| Refresh token hashing in Redis (plaintext never stored) | TokenManager | Unit | M2 |
| RS256 2048-bit key enforcement | JwtService | Unit (config validation) | M2 |
| TLS 1.3 on all endpoints | Infrastructure | Config review | M5 |
| CORS restricted to known frontend origins | API Gateway | Integration (origin header test) | M4 |
| accessToken stored in memory only, not localStorage | AuthProvider | E2E (storage inspection) | M4 |
| Tokens cleared on tab close | AuthProvider | E2E | M4 |

---

## Appendix B: Timeline Gantt View

```
Week:  W1      W2      W3      W4      W5      W6      W7      W8      W9
       Apr 7   Apr 14  Apr 21  Apr 28  May 5   May 12  May 19  May 26  Jun 9

WS-A   [=== M1 ===][=== M2 ===][=== M3 ===]
BE
WS-B                  (scaffold)[  M4 integration  ][ E2E ]
FE
WS-C   [infra ][ metrics ][audit+SOC2 ][dashboards ]
PLAT
WS-D            [sec-1  ][sec-2  ][pen test ][rollout     ]
SEC

       |       |       |       |       |       |       |       |
       M1      M2              M3              M4      M5
       done    done            done            done    GA
```
