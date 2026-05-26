---
id: "AUTH-ROADMAP-V2"
title: "User Authentication Service — Delivery Roadmap (Variant 2: Sonnet Default)"
source-spec: "AUTH-MERGED-PRD-TDD v1.0"
generated-at: "2026-05-22"
variant-tag: "sonnet-default"
---

# User Authentication Service — Delivery Roadmap

## Executive Summary

This roadmap delivers the User Authentication Service as a production-grade identity layer for the platform, spanning six milestones across twelve sprints (approximately 24 weeks). The service provides user registration, login/logout, JWT-based session persistence, profile retrieval, and self-service password reset — collectively forming the prerequisite foundation for the Q2-Q3 2026 personalization roadmap and Q3 SOC2 Type II audit compliance.

The delivery is structured around four concentric capability rings: (1) data foundation and credential management, (2) token lifecycle and session persistence, (3) self-service recovery and profile access, and (4) frontend integration, production hardening, and GA rollout. Each milestone gates on measurable exit criteria derived from the PRD functional requirements (FR-AUTH.1 through FR-AUTH.5, FR-AUTH-001 through FR-AUTH-005) and non-functional requirements (NFR-AUTH.1 through NFR-AUTH.3, NFR-PERF-001, NFR-PERF-002, NFR-REL-001, NFR-SEC-001, NFR-SEC-002). The TDD specifies AuthService, TokenManager, JwtService, and PasswordHasher as the core service components, backed by PostgreSQL 15+ for UserProfile persistence and Redis 7+ for refresh token management.

The phased rollout strategy (internal alpha at 0% traffic, beta at 10%, GA at 100%) mitigates migration risk through feature flags AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH, with explicit rollback triggers for latency degradation exceeding 1000ms p95, error rates above 5%, or any data corruption in UserProfile records.

## Roadmap Overview

| Property | Value |
|----------|-------|
| Total milestones | 6 |
| Total sprints | 12 (2-week sprints) |
| Estimated duration | 24 weeks |
| Target completion | M5 GA by 2026-06-09; M6 hardening complete by 2026-06-23 |
| Sequencing strategy | Bottom-up: schema and hashing first, then token lifecycle, then user-facing flows, then integration and rollout |
| Team | auth-team (3-5 engineers), plus frontend-team for M4 |
| Infrastructure cost | ~$450/month production (3 K8s pods $150, PostgreSQL $200, Redis $100) |

**Milestone summary:**

| Milestone | Name | Sprints | Key PRD/TDD Trace |
|-----------|------|---------|--------------------|
| M1 | Data Foundation and Credential Infrastructure | S1–S2 | FR-AUTH.2, FR-AUTH-002, NFR-SEC-001 |
| M2 | Core Authentication (Login/Logout) | S3–S4 | FR-AUTH.1, FR-AUTH-001, NFR-PERF-001 |
| M3 | Token Lifecycle and Session Persistence | S5–S6 | FR-AUTH.3, FR-AUTH-003, NFR-SEC-002 |
| M4 | Profile, Password Reset, and Audit Logging | S7–S9 | FR-AUTH.4, FR-AUTH.5, FR-AUTH-004, FR-AUTH-005 |
| M5 | Frontend Integration and GA Rollout | S10–S11 | AUTH-E1, AUTH-E2, AUTH-E3, all user stories |
| M6 | Production Hardening and Compliance Validation | S12 | NFR-AUTH.2, NFR-REL-001, SOC2, GDPR |

---

## Milestone 1 — Data Foundation and Credential Infrastructure

### ID and Goal

**M1: Data Foundation and Credential Infrastructure**

Goal: Establish the PostgreSQL schema for UserProfile, implement PasswordHasher with bcrypt cost factor 12, build the UserRepo data-access layer, and validate the registration data path end-to-end. This milestone produces the persistent data foundation that every subsequent milestone depends on.

### Scope

**In scope:**

- PostgreSQL 15+ schema creation (users table, audit_log table)
- PasswordHasher component with bcrypt cost factor 12 (NFR-SEC-001)
- UserRepo data-access layer with connection pooling (pg-pool)
- Email normalization (lowercase) and uniqueness constraint
- Password policy validation (>= 8 chars, >= 1 uppercase, >= 1 number) per NIST SP 800-63B
- Database migration framework setup (versioned migrations)
- GDPR consent recording at registration (consent timestamp column)

**Out of scope:**

- Token issuance (M2/M3)
- Login endpoint (M2)
- API route wiring (M2)
- Frontend components (M5)
- Email delivery integration (M4)

### Deliverables

| Deliverable | Description | PRD/TDD Trace | Validation |
|-------------|-------------|---------------|------------|
| D1.1 | PostgreSQL migration 001: users table with columns id (UUID v4 PK), email (UNIQUE, indexed), password_hash, display_name (2-100 chars), created_at, updated_at, last_login_at, roles (text[] default ["user"]), consent_at, locked_until, failed_login_attempts | FR-AUTH-002 UserProfile schema, GDPR consent requirement | Migration runs idempotently; schema matches TDD Section 7.1 field table exactly |
| D1.2 | PostgreSQL migration 002: audit_log table with columns id, user_id, event_type, ip_address, outcome, created_at, metadata (jsonb) | SOC2 audit logging requirement, PRD Legal/Compliance table | Queryable by user_id and date range per Jordan admin persona JTBD |
| D1.3 | PasswordHasher module: hash(plain) and verify(plain, hash) methods wrapping bcryptjs with cost factor 12; hash operation benchmarks < 500ms | NFR-SEC-001, TDD Section 13 | Unit test asserts cost factor 12; benchmark test confirms < 500ms |
| D1.4 | UserRepo module: findById, findByEmail, create(user), updateLastLogin(id, timestamp), incrementFailedAttempts(id), lockAccount(id, duration), unlockAccount(id), resetFailedAttempts(id) | FR-AUTH-002, FR-AUTH-001 account lockout | Integration tests against real PostgreSQL via testcontainers |
| D1.5 | Input validation module: email format (RFC 5322 simplified), password strength (>= 8 chars, >= 1 uppercase, >= 1 digit), displayName length (2-100 chars) | FR-AUTH-002 acceptance criteria 3 | Unit tests for every boundary: 7-char password, no uppercase, no digit, 1-char display name, 101-char display name, malformed email |
| D1.6 | CI pipeline: GitHub Actions workflow running unit tests (Jest), integration tests (testcontainers PostgreSQL), linting (ESLint), and type checking (TypeScript) | TDD Section 15.1 test pyramid | Pipeline runs on every PR; blocks merge on failure |

### Dependencies

**Within milestone:**

- D1.1 (schema) must complete before D1.4 (UserRepo) can be tested
- D1.3 (PasswordHasher) and D1.5 (validation) are independent of each other and of D1.1

**Cross-milestone:**

- M2 depends on D1.1, D1.3, D1.4, D1.5 for login and registration endpoints
- M3 depends on D1.1 for UserProfile data in JWT payload

### Entry Criteria

- PostgreSQL 15+ instance provisioned and accessible to auth-team
- Node.js 20 LTS runtime configured in CI
- Docker available in CI for testcontainers

### Exit Criteria

- All migrations run successfully against clean PostgreSQL instance
- PasswordHasher unit tests pass with 100% branch coverage (cost factor, verify true/false, error on null input)
- UserRepo integration tests pass: create, findByEmail (found/not-found), duplicate email returns unique constraint error
- Input validation rejects all boundary cases listed in D1.5
- CI pipeline green on main branch
- Schema matches TDD Section 7.1 field table (field names, types, constraints)

### Estimated Effort

2 sprints (4 weeks). Breakdown: D1.1-D1.2 schema (3 days), D1.3 PasswordHasher (2 days), D1.4 UserRepo (5 days), D1.5 validation (3 days), D1.6 CI (2 days), buffer (5 days).

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| PostgreSQL provisioning delayed by infra team | Medium | High | Use Docker Compose for local dev immediately; escalate provisioning request before sprint 1 start |
| bcrypt cost factor 12 exceeds 500ms on CI hardware | Low | Medium | Benchmark on CI hardware in sprint 1 day 1; if > 500ms, document deviation and adjust to cost 11 with security team sign-off |
| NIST SP 800-63B password policy interpretation differs between security and engineering | Medium | Medium | Resolve in M1 entry with security reviewer; document exact validation rules in code comments |

### Validation/Acceptance Approach

- Automated: CI pipeline with unit + integration tests
- Manual: Schema review by sys-architect against TDD Section 7.1
- Security: PasswordHasher cost factor assertion in unit test (NFR-SEC-001)
- Sign-off: test-lead approves merge of M1 branch

---

## Milestone 2 — Core Authentication (Login/Logout)

### ID and Goal

**M2: Core Authentication (Login/Logout)**

Goal: Implement the AuthService orchestrator with registration (POST /auth/register) and login (POST /auth/login) endpoints, including account lockout after 5 failed attempts within 15 minutes, audit log writes for every auth event, and rate limiting at the API Gateway layer.

### Scope

**In scope:**

- AuthService core orchestrator class
- POST /auth/register endpoint (FR-AUTH.2, FR-AUTH-002)
- POST /auth/logout endpoint
- Account lockout logic: lock after 5 failed attempts within 15 minutes (FR-AUTH-001 AC4)
- Generic error messages for authentication failures (no user enumeration) (FR-AUTH-001 AC3)
- Audit log writes for registration and login events (SOC2 requirement)
- Rate limiting configuration: 10 req/min per IP for /auth/login, 5 req/min per IP for /auth/register (TDD Section 8.1)
- Email case normalization in login path
- GDPR consent recording at registration (timestamp in consent_at column)

**Out of scope:**

- JWT token issuance (returns session identifier placeholder; M3 adds JWT)
- Token refresh endpoint (M3)
- Profile retrieval endpoint (M4)
- Password reset flow (M4)
- Frontend integration (M5)

### Deliverables

| Deliverable | Description | PRD/TDD Trace | Validation |
|-------------|-------------|---------------|------------|
| D2.1 | AuthService class with register(email, password, displayName, consentGiven) and login(email, password) methods | FR-AUTH-002, FR-AUTH-001 | Unit tests with mocked UserRepo and PasswordHasher |
| D2.2 | POST /auth/register route: validates input (D1.5), hashes password (D1.3), creates UserProfile (D1.4), returns 201 with profile data or 400/409 on error | FR-AUTH-002 all acceptance criteria | Integration test: valid registration returns 201; duplicate email returns 409; weak password returns 400 with field-level errors |
| D2.3 | POST /auth/login route: normalizes email to lowercase, verifies password via PasswordHasher, increments failed_attempts on failure, locks account after 5 failures in 15 min window, returns generic 401 for all auth failures, returns 423 for locked accounts | FR-AUTH-001 all acceptance criteria | Integration tests: valid login returns 200; wrong password returns 401 with generic message; 5th failure returns 423; locked account returns 423 even with correct password |
| D2.4 | Audit log writer: writes to audit_log table for every registration, login success, login failure, and account lockout event. Fields: user_id, event_type, ip_address (from request), outcome, created_at, metadata | SOC2 requirement, PRD Legal/Compliance: "user ID, timestamp, IP, and outcome" | Integration test confirms row written for each event type; queryable by user_id and date range |
| D2.5 | API Gateway rate limiting configuration: 10 req/min per IP on /auth/login, 5 req/min per IP on /auth/register, 429 response with Retry-After header | TDD Section 8.1 rate limit column | Load test confirms 11th request within 1 minute returns 429 |
| D2.6 | Logout endpoint: POST /auth/logout invalidates the current session (at this milestone, clears server-side session identifier; M3 will add refresh token revocation) | PRD user story "Log Out" acceptance criteria | Integration test: logout returns 204; subsequent request to protected endpoint returns 401 |

### Dependencies

**Within milestone:**

- D2.1 (AuthService) depends on D1.3 (PasswordHasher), D1.4 (UserRepo), D1.5 (validation)
- D2.2-D2.3 (routes) depend on D2.1
- D2.4 (audit) depends on D1.2 (audit_log schema)
- D2.5 (rate limiting) is independent of service logic

**Cross-milestone:**

- M3 depends on D2.1 (AuthService) for token issuance integration
- M4 depends on D2.4 (audit log) for password reset event logging

### Entry Criteria

- M1 fully complete: schema deployed, PasswordHasher tested, UserRepo tested, CI green
- API Gateway infrastructure available for rate limiting configuration

### Exit Criteria

- POST /auth/register: 201 on valid input, 409 on duplicate email, 400 on validation failure with specific field errors
- POST /auth/login: 200 on valid credentials, 401 with generic "Invalid email or password" on any failure (wrong email, wrong password, non-existent user), 423 after 5 failures in 15 min window
- POST /auth/logout: 204 on success
- Audit log rows written for every registration (success), login (success/failure), lockout event
- Rate limiting enforced: 11th login request within 60 seconds returns 429
- Unit test coverage for AuthService >= 80%
- No user enumeration: login response for non-existent email is byte-identical to wrong-password response (same status code, same error code, same message text, same response time within 50ms)
- p95 login latency < 200ms in local load test with 50 concurrent users (preliminary; M6 validates at 500)

### Estimated Effort

2 sprints (4 weeks). Breakdown: D2.1 AuthService (5 days), D2.2 register route (3 days), D2.3 login route with lockout (5 days), D2.4 audit logging (3 days), D2.5 rate limiting (2 days), D2.6 logout (1 day), buffer (5 days).

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Account lockout timing race: two concurrent login failures at attempt 4 and 5 both read 4, both write 5, neither triggers lock | Medium | Medium | Use PostgreSQL atomic UPDATE with WHERE clause: `UPDATE users SET failed_login_attempts = failed_login_attempts + 1 WHERE id = $1 RETURNING failed_login_attempts`; check returned value >= 5 in application code |
| Timing side-channel on login: non-existent user responds faster than wrong-password (bcrypt verify adds ~300ms) | High | High | For non-existent users, perform a dummy bcrypt verify against a pre-computed hash to normalize response time to within 50ms of the wrong-password path |
| Rate limiting at API Gateway level is bypassed by distributed attack from multiple IPs | Medium | Medium | Defense-in-depth: rate limiting at gateway AND account-level lockout in AuthService. Document that IP-level rate limiting is a first line, not the sole defense |

### Validation/Acceptance Approach

- Automated: Integration tests against real PostgreSQL via testcontainers
- Security: Dedicated test suite for anti-enumeration (response comparison) and timing analysis
- Performance: Local k6 load test at 50 concurrent users
- Sign-off: sec-reviewer reviews login flow for enumeration and timing leaks

---

## Milestone 3 — Token Lifecycle and Session Persistence

### ID and Goal

**M3: Token Lifecycle and Session Persistence**

Goal: Implement TokenManager and JwtService for JWT access token issuance (15-min TTL) and refresh token lifecycle (7-day TTL in Redis), the POST /auth/refresh endpoint, silent token refresh in the backend, and the GET /auth/me profile retrieval endpoint. This milestone completes the stateless session management architecture specified in the TDD.

### Scope

**In scope:**

- JwtService: RS256 signing with 2048-bit RSA keys, 15-min access token TTL, 5-second clock skew tolerance (TDD Section 12)
- TokenManager: refresh token generation, storage in Redis with 7-day TTL, revocation, refresh-token rotation (old token revoked on every refresh)
- POST /auth/refresh endpoint (FR-AUTH-003)
- GET /auth/me endpoint (FR-AUTH-004)
- Integration of token issuance into login and registration flows (updating D2.2, D2.3 from M2)
- AuthToken data model as defined in TDD Section 7.1 (accessToken, refreshToken, expiresIn=900, tokenType="Bearer")
- RSA key loading and quarterly rotation documentation
- Redis unavailability fallback: reject refresh requests rather than serve stale tokens (TDD Section 12)

**Out of scope:**

- Frontend token handling (M5)
- Password reset (M4)
- RS256 key rotation automation (M6 manual; deferred to post-GA for automation)

### Deliverables

| Deliverable | Description | PRD/TDD Trace | Validation |
|-------------|-------------|---------------|------------|
| D3.1 | JwtService: sign(payload, expiresIn) and verify(token) methods using RS256 with 2048-bit RSA key. JWT payload contains user id and roles. Clock skew tolerance of 5 seconds. | FR-AUTH-003, NFR-SEC-002 | Unit tests: sign/verify round-trip; expired token rejected; clock-skew token within 5s accepted; tampered payload rejected |
| D3.2 | TokenManager: issueTokens(userId, roles) generates AuthToken pair (access via JwtService, refresh as crypto-random 256-bit opaque token stored hashed in Redis with 7-day TTL). refresh(oldRefreshToken) validates, revokes old, issues new pair. revoke(refreshToken) deletes from Redis. revokeAllForUser(userId) deletes all user's refresh tokens. | FR-AUTH-003 all acceptance criteria | Unit tests with mocked Redis; integration tests with real Redis via testcontainers |
| D3.3 | POST /auth/refresh endpoint: accepts {refreshToken}, calls TokenManager.refresh(), returns 200 with new AuthToken or 401 for expired/revoked tokens. Rate limit: 30 req/min per user. | FR-AUTH-003 AC2, AC3, AC4 | Integration test: valid refresh returns 200 with new pair; second refresh with same old token returns 401 (rotation prevents reuse); expired refresh returns 401 |
| D3.4 | GET /auth/me endpoint: validates Bearer token via JwtService, fetches UserProfile from UserRepo, returns 200 with profile data. 401 on invalid/expired/missing token. Rate limit: 60 req/min per user. | FR-AUTH-004 all acceptance criteria | Integration test: valid token returns full UserProfile; expired token returns 401; tampered token returns 401 |
| D3.5 | Update POST /auth/login (D2.3) to return AuthToken pair via TokenManager instead of session placeholder | FR-AUTH.1 "receive a persistent session" | Integration test: login response now includes accessToken, refreshToken, expiresIn=900, tokenType="Bearer" |
| D3.6 | Update POST /auth/register (D2.2) to auto-login after registration and return AuthToken pair | FR-AUTH.2 "creates account and logs user in" | Integration test: registration returns 201 with both UserProfile data and AuthToken |
| D3.7 | RSA key management: key pair loaded from filesystem path (Kubernetes secret mount). Documentation for quarterly rotation procedure. | NFR-SEC-002 | Key loading tested in unit test; rotation procedure documented in runbook |
| D3.8 | Prometheus metrics: auth_token_refresh_total (counter, labels: outcome=success/expired/revoked), auth_token_refresh_duration_seconds (histogram) | TDD Section 14 | Metric emitted and verifiable in test environment |

### Dependencies

**Within milestone:**

- D3.1 (JwtService) must complete before D3.2 (TokenManager, which calls JwtService)
- D3.2 must complete before D3.3, D3.4, D3.5, D3.6
- D3.7 (key management) can proceed in parallel with D3.1-D3.2

**Cross-milestone:**

- M2 D2.2 and D2.3 must be updated (D3.5, D3.6) to return AuthToken
- M4 depends on D3.2 TokenManager.revokeAllForUser() for password reset session invalidation
- M5 depends on D3.5, D3.6 for frontend token storage

### Entry Criteria

- M2 fully complete: AuthService, login, register, audit logging, rate limiting all tested
- Redis 7+ instance provisioned and accessible
- RSA 2048-bit key pair generated and available as Kubernetes secret

### Exit Criteria

- POST /auth/refresh: 200 on valid refresh token with new AuthToken pair; 401 on expired token; 401 on previously-used refresh token (rotation enforced); 401 on revoked token
- GET /auth/me: 200 with full UserProfile (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles) on valid Bearer token; 401 on missing/invalid/expired token
- POST /auth/login returns AuthToken with expiresIn=900, tokenType="Bearer"
- POST /auth/register returns 201 with UserProfile AND AuthToken
- TokenManager.revokeAllForUser(userId) deletes all refresh tokens for that user from Redis (validated in integration test)
- Redis unavailability: POST /auth/refresh returns 503 with clear error (not 200 with stale data)
- JWT payload contains exactly: sub (userId), roles (array), iat, exp. No PII in JWT.
- Unit test coverage for JwtService and TokenManager >= 80%
- Token refresh latency p95 < 100ms (TDD Section 4.1)

### Estimated Effort

2 sprints (4 weeks). Breakdown: D3.1 JwtService (3 days), D3.2 TokenManager (5 days), D3.3 refresh endpoint (2 days), D3.4 /auth/me (2 days), D3.5-D3.6 login/register updates (2 days), D3.7 key management (1 day), D3.8 metrics (1 day), buffer (4 days).

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Refresh token rotation race: two concurrent refresh requests with same token both attempt to redeem it | Medium | High | Use Redis SETNX or Lua script for atomic compare-and-delete. If token does not exist when SETNX is attempted, return 401. This makes refresh token use exactly-once by construction. |
| Redis key eviction under memory pressure loses valid refresh tokens, forcing unexpected re-logins | Low | Medium | Set maxmemory-policy to allkeys-lru. Monitor Redis memory utilization; alert at 70% (per TDD Section 25.3: scale to 2GB if > 70%). Size estimate: 100K tokens at ~500 bytes each = 50MB, well within 1GB allocation. |
| RSA key rotation causes brief signing verification failures during the switchover window | Low | Medium | During rotation, load both old and new keys. JwtService.verify() tries new key first, falls back to old key. Remove old key only after all access tokens issued under it have expired (15 min). Document this procedure. |

### Validation/Acceptance Approach

- Automated: Unit tests for JwtService and TokenManager with mocked Redis; integration tests with real Redis via testcontainers
- Security: Verify JWT does not contain email or other PII (only sub and roles)
- Performance: k6 test for POST /auth/refresh p95 < 100ms
- Sign-off: sec-reviewer approves RS256 key management procedure

---

## Milestone 4 — Profile, Password Reset, and Audit Logging

### ID and Goal

**M4: Profile, Password Reset, and Audit Logging**

Goal: Implement the self-service password reset flow (FR-AUTH.5, FR-AUTH-005) with SendGrid email delivery, reset token generation with 1-hour TTL and single-use enforcement, session invalidation on password change, and the admin-facing audit log query endpoint. This milestone completes all backend API functionality.

### Scope

**In scope:**

- Password reset request endpoint: POST /auth/reset-request (FR-AUTH-005 AC1)
- Password reset confirmation endpoint: POST /auth/reset-confirm (FR-AUTH-005 AC2, AC3, AC4)
- Reset token generation: crypto-random token, stored hashed in Redis with 1-hour TTL
- Email delivery integration with SendGrid API
- Session invalidation on password change: TokenManager.revokeAllForUser() (D3.2 dependency)
- Anti-enumeration: same success response for registered and unregistered emails (FR-AUTH.5 acceptance, PRD error handling table)
- Audit log query endpoint for admin persona (Jordan): GET /admin/auth-events?userId=&startDate=&endDate=&eventType=
- Password policy enforcement on new password during reset (same rules as registration: >= 8 chars, >= 1 uppercase, >= 1 digit)

**Out of scope:**

- Frontend reset flow UI (M5)
- Email template design (use SendGrid default transactional template)
- MFA (NG-002)
- RBAC enforcement on admin endpoint (NG-003; admin endpoint protected by roles field but enforcement is soft)

### Deliverables

| Deliverable | Description | PRD/TDD Trace | Validation |
|-------------|-------------|---------------|------------|
| D4.1 | POST /auth/reset-request: accepts {email}. If email exists: generate reset token (crypto-random 256-bit), store SHA-256 hash in Redis with 1-hour TTL, send email via SendGrid with reset link containing token. If email does not exist: do nothing. Always return 200 with same response body: {"message": "If an account exists with this email, a reset link has been sent."} | FR-AUTH-005 AC1, PRD error handling: "Reset requested for unregistered email — Same success response" | Integration test: registered email triggers SendGrid call AND returns 200; unregistered email returns identical 200 response; response body byte-identical for both cases |
| D4.2 | POST /auth/reset-confirm: accepts {token, newPassword}. Validates token (SHA-256 compare against Redis), checks token not previously used, validates new password against policy, hashes new password via PasswordHasher, updates user row, deletes reset token from Redis, calls TokenManager.revokeAllForUser() to invalidate all sessions | FR-AUTH-005 AC2, AC3, AC4 | Integration tests: valid token updates password and revokes all refresh tokens; expired token returns 401 with clear error; reused token returns 401; weak new password returns 400 |
| D4.3 | SendGrid email integration module: sendResetEmail(toEmail, resetToken) constructs reset URL, calls SendGrid API, handles delivery failures with retry (3 attempts with exponential backoff: 1s, 4s, 16s) | PRD dependency: "Email delivery service (SendGrid)" | Unit test with mocked SendGrid; integration test verifies email payload format |
| D4.4 | Reset token storage: tokens stored as SHA-256 hashes in Redis with key prefix `reset:` and 1-hour TTL. Token comparison uses constant-time comparison to prevent timing attacks. | NFR-SEC-001, TDD Section 13 | Unit test confirms SHA-256 hashing; timing test confirms constant comparison |
| D4.5 | GET /admin/auth-events: queryable by userId, startDate, endDate, eventType. Returns paginated results (default 50, max 200). Requires Bearer token with "admin" in roles array. | Jordan admin persona JTBD, SOC2 audit logging | Integration test: query returns expected events; non-admin user gets 403; pagination works correctly |
| D4.6 | Audit log writes for password reset events: reset-requested, reset-email-sent, reset-completed, reset-failed (per D2.4 audit writer) | SOC2 "all auth events logged" | Integration test confirms rows in audit_log for each event type |
| D4.7 | Email delivery monitoring: Prometheus counter auth_email_send_total (labels: outcome=success/failure), alert if failure rate > 5% over 10 minutes | TDD Section 14, PRD risk table "Email delivery failures" | Metric verifiable in test environment |

### Dependencies

**Within milestone:**

- D4.1 must complete before D4.2 (confirm needs to understand token format)
- D4.3 and D4.4 are independent of each other
- D4.5 (audit query) depends on D1.2 (audit_log schema) and D2.4 (audit writer)

**Cross-milestone:**

- D4.2 depends on M3 D3.2 TokenManager.revokeAllForUser()
- D4.2 depends on M1 D1.3 PasswordHasher for new password hashing
- M5 depends on D4.1, D4.2 for frontend password reset flow

### Entry Criteria

- M3 fully complete: TokenManager with revokeAllForUser() available
- SendGrid API key provisioned and tested (send a test email)
- Redis available for reset token storage

### Exit Criteria

- POST /auth/reset-request: 200 for both registered and unregistered emails with identical response; registered email triggers SendGrid call; reset token stored in Redis with 1-hour TTL
- POST /auth/reset-confirm: 200 on valid token with new password; 401 on expired/invalid/reused token; 400 on weak password; all refresh tokens revoked on success; user can log in with new password immediately
- GET /admin/auth-events: returns paginated audit events filterable by userId, date range, event type; 403 for non-admin
- Reset email delivered within 60 seconds in staging environment
- Anti-enumeration: response for unregistered email is byte-identical to registered email (same status, same body, same timing within 50ms)
- Unit test coverage for reset flow >= 80%
- Email delivery failure rate < 1% in staging

### Estimated Effort

3 sprints (6 weeks). This is the largest milestone due to the external SendGrid integration and the admin audit endpoint. Breakdown: D4.1 reset-request (3 days), D4.2 reset-confirm (4 days), D4.3 SendGrid integration (3 days), D4.4 token storage (2 days), D4.5 audit query (3 days), D4.6 audit events (1 day), D4.7 monitoring (1 day), buffer (5 days).

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| SendGrid API downtime blocks password reset flow | Low | High | SendGrid SLA is 99.99%. Queue reset emails in local buffer with retry (D4.3 retry logic). If SendGrid is down for > 30 min, surface error to user: "Reset email delayed. Please try again in a few minutes." Do NOT reveal whether email is registered. |
| Reset token reused before first use is consumed (concurrent reset-confirm requests) | Medium | High | Use Redis atomic compare-and-delete (Lua script: GET key, compare hash, DEL if match). Only one concurrent request succeeds; others get 401. |
| Reset token brute-force: attacker guesses 256-bit random tokens | Negligible | High | 256-bit tokens provide 2^256 entropy. Even at 1M guesses/sec, expected time exceeds age of universe. Rate-limit reset-confirm to 10 req/min per IP. |
| Admin audit endpoint returns too much data, causing slow queries on large audit_log table | Medium | Low | Require at least one filter (userId OR startDate). Enforce max date range of 90 days per query. Add composite index on (user_id, created_at) and (created_at, event_type). |

### Validation/Acceptance Approach

- Automated: Integration tests against real PostgreSQL + Redis + mocked SendGrid
- Manual: Send actual reset email in staging, verify delivery within 60 seconds
- Security: Anti-enumeration test suite (response comparison for registered vs unregistered)
- Compliance: Audit log query returns all required SOC2 fields (user_id, timestamp, IP, outcome)
- Sign-off: sec-reviewer approves reset flow for single-use token enforcement

---

## Milestone 5 — Frontend Integration and GA Rollout

### ID and Goal

**M5: Frontend Integration and GA Rollout**

Goal: Build the frontend authentication components (LoginPage, RegisterPage, AuthProvider, ProfilePage), wire them to the backend API, execute the phased rollout (alpha -> beta 10% -> GA 100%), and remove feature flags. This milestone delivers the complete user-facing authentication experience described in the PRD user journeys.

### Scope

**In scope:**

- LoginPage component (TDD Section 10.2): email/password form, calls POST /auth/login, stores AuthToken via AuthProvider
- RegisterPage component (TDD Section 10.2): registration form with inline validation, calls POST /auth/register, GDPR consent checkbox
- AuthProvider context wrapper (TDD Section 10.2): manages AuthToken state, silent token refresh via POST /auth/refresh, intercepts 401 responses, redirects to LoginPage for protected routes
- ProfilePage component: displays UserProfile data from GET /auth/me
- Password reset frontend flow: "Forgot Password" link on LoginPage, reset-request form, reset-confirm form
- Route structure: /login (public), /register (public), /profile (protected), /reset-password (public), /reset-password/confirm?token= (public)
- AuthProvider stores accessToken in memory only (not localStorage) per TDD Section 13 risk R-001; refreshToken in HttpOnly cookie (set by backend)
- Silent token refresh: AuthProvider checks accessToken expiry before each API call; if < 30 seconds remaining, refreshes via POST /auth/refresh before making the original request
- Feature flag integration: AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH

**Out of scope:**

- Social login UI (NG-001)
- MFA UI (NG-002)
- Admin dashboard UI (backend only in v1.0)
- Email verification flow (not in PRD v1.0 scope)

### Deliverables

| Deliverable | Description | PRD/TDD Trace | Validation |
|-------------|-------------|---------------|------------|
| D5.1 | LoginPage: email/password form with loading state, error display (generic "Invalid email or password"), calls POST /auth/login, stores tokens via AuthProvider, redirects to dashboard on success. Form loads in < 1 second. | PRD user journey "Returning User Login", PRD "Login Flow" UX | E2E test: valid credentials -> dashboard; invalid credentials -> error message; page load < 1s |
| D5.2 | RegisterPage: email/password/displayName form with inline validation (password strength indicator, email format check), GDPR consent checkbox (required), calls POST /auth/register, auto-login and redirect to dashboard. Inline validation shows unmet requirements. | PRD "Signup Flow" UX, FR-AUTH.2, GDPR "consent at registration" | E2E test: valid registration -> dashboard; weak password -> inline error; no consent -> form blocked; duplicate email -> friendly error |
| D5.3 | AuthProvider: React context wrapping all routes. State: accessToken, refreshToken (HttpOnly cookie managed by backend), UserProfile. Methods: login(), register(), logout(), refreshToken(), getUserProfile(). Intercepts 401 on any API call and attempts silent refresh before redirecting to /login. Clears tokens on tab close (accessToken in memory only). | TDD Section 10.2 AuthProvider, TDD Section 13 R-001 | E2E test: token expires during navigation -> silent refresh succeeds -> user stays on page; refresh fails -> redirect to /login |
| D5.4 | ProfilePage: displays displayName, email, createdAt from GET /auth/me. Page renders in < 1 second. Redirects to /login if not authenticated. | FR-AUTH.4, FR-AUTH-004, PRD "Profile Management" journey | E2E test: authenticated -> profile displays; unauthenticated -> redirect to /login |
| D5.5 | Password reset frontend: "Forgot Password" link on LoginPage -> reset-request form (email input) -> confirmation message -> email link -> reset-confirm form (new password + confirm) -> redirect to /login. Confirmation message shown regardless of email registration. | PRD "Password Reset Flow" UX, FR-AUTH.5 | E2E test: full reset flow; confirmation shown for unregistered email; expired token shows clear error with "request new link" option |
| D5.6 | Feature flag configuration: AUTH_NEW_LOGIN gates new LoginPage/RegisterPage; AUTH_TOKEN_REFRESH gates refresh token flow in AuthProvider. Flags configured in feature flag service. | TDD Section 19.2 | Flag ON -> new flow; Flag OFF -> legacy flow (if applicable) |
| D5.7 | Rollout execution: Phase 1 internal alpha (1 week) -> Phase 2 beta 10% (2 weeks) -> Phase 3 GA 100% (1 week). Rollback criteria: p95 > 1000ms for 5 min, error rate > 5% for 2 min, Redis failures > 10/min, data corruption. | TDD Section 19.1, 19.4 | Each phase has explicit go/no-go meeting with test-lead and eng-manager |
| D5.8 | Feature flag removal: AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH removed from codebase 2 weeks after successful Phase 3 GA | TDD Section 19.2 "Removal Target" | Flags no longer referenced in code; dead flag configuration cleaned up |

### Dependencies

**Within milestone:**

- D5.3 (AuthProvider) must complete before D5.1, D5.2, D5.4 (all depend on auth context)
- D5.5 (password reset) depends on D5.1 (LoginPage for "Forgot Password" link)
- D5.6-D5.8 (rollout) are sequential

**Cross-milestone:**

- D5.1-D5.5 depend on M2-M4 backend endpoints being deployed and tested
- D5.5 depends on M4 D4.1, D4.2 (reset endpoints)
- D5.7 rollout depends on staging environment matching production

### Entry Criteria

- M4 fully complete: all backend endpoints deployed to staging
- Frontend routing framework available and configured
- Feature flag service operational
- Staging environment mirrors production topology (API Gateway, PostgreSQL, Redis, Kubernetes)

### Exit Criteria

- LoginPage: loads in < 1s; valid login redirects to dashboard; invalid login shows generic error; no user enumeration
- RegisterPage: inline validation for password strength; GDPR consent required; successful registration auto-logs in
- AuthProvider: silent refresh works; 401 interception works; tokens cleared on tab close; no accessToken in localStorage or sessionStorage
- ProfilePage: displays correct UserProfile data; unauthenticated users redirected
- Password reset: full E2E flow works; anti-enumeration on reset-request
- Phase 1 (alpha): all FR-AUTH-001 through FR-AUTH-005 pass manual testing; zero P0/P1 bugs
- Phase 2 (beta 10%): p95 latency < 200ms; error rate < 0.1%; no Redis connection failures; 14 days of monitoring data
- Phase 3 (GA 100%): 99.9% uptime over first 7 days; all monitoring dashboards green
- Feature flags removed 2 weeks post-GA
- Registration conversion rate > 60% (measured 30 days post-GA)

### Estimated Effort

2 sprints (4 weeks). Breakdown: D5.3 AuthProvider (4 days), D5.1 LoginPage (3 days), D5.2 RegisterPage (3 days), D5.4 ProfilePage (2 days), D5.5 password reset frontend (3 days), D5.6 feature flags (1 day), D5.7 rollout execution (4 weeks wall-clock, ~3 days engineering time for monitoring and flag toggling), D5.8 flag removal (1 day).

Note: D5.7 rollout spans 4 weeks wall-clock (1 week alpha + 2 weeks beta + 1 week GA) but only ~3 days of active engineering work. The rest is monitoring time.

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| AuthProvider token refresh loop: access token expires, refresh fails (Redis down), user redirected to login, but login page is behind auth check | Medium | High | LoginPage and RegisterPage must be in PUBLIC routes that do not trigger AuthProvider refresh. Explicit route-level auth/no-auth flag. |
| Frontend stores accessToken in localStorage despite requirement (developer habit) | Medium | High | Code review checklist item: "grep localStorage in auth-related files". Add ESLint rule to flag localStorage usage in auth module. |
| Silent refresh fails during active form submission; user loses form data | Medium | Medium | AuthProvider should attempt refresh BEFORE the API call. If refresh fails, save form state to sessionStorage (non-sensitive data only), redirect to login, restore on return. |
| Beta users encounter edge case not caught in alpha (e.g., slow network causes timeout during login) | Medium | Low | Beta phase has explicit monitoring with alerts. Rollback criteria are clearly defined. Support channel monitored during beta. |
| Registration conversion rate < 60% due to UX friction | Medium | Medium | Funnel analytics instrumented from day 1. A/B test registration form variations if conversion < 50% in first week of beta. |

### Validation/Acceptance Approach

- Automated: Playwright E2E tests for all four user journeys (signup, login, profile, password reset)
- Manual: UX review of all auth pages by design lead
- Performance: k6 load test at 500 concurrent users (NFR-PERF-002)
- Rollout: Each phase has a go/no-go meeting with test-lead, eng-manager, and product
- Business: Registration conversion tracking via funnel analytics from RegisterPage to confirmed account

---

## Milestone 6 — Production Hardening and Compliance Validation

### ID and Goal

**M6: Production Hardening and Compliance Validation**

Goal: Conduct penetration testing, validate SOC2 audit log compliance, confirm GDPR data handling, complete performance validation at full 500-concurrent-user scale, finalize runbooks, and establish the on-call rotation. This milestone ensures the service meets all non-functional requirements and is operationally ready for long-term production use.

### Scope

**In scope:**

- Penetration testing by external security firm (PRD risk table: "Dedicated security review; penetration testing before production")
- SOC2 audit log validation: all auth events logged with required fields (user ID, timestamp, IP, outcome), 12-month retention confirmed
- GDPR validation: consent recording, data minimization (only email, hashed password, display name collected), right-to-erasure endpoint
- Performance validation at 500 concurrent users (NFR-PERF-002): all endpoints < 200ms p95
- 99.9% availability validation over 30-day rolling window baseline (NFR-REL-001)
- Runbook finalization (TDD Section 25.1 scenarios)
- On-call rotation establishment (TDD Section 25.2)
- Capacity planning review (TDD Section 25.3)
- RS256 key rotation dry run (quarterly procedure)
- Password hash migration dry run (for future bcrypt -> argon2id migration path)

**Out of scope:**

- New features or endpoints
- Frontend changes
- Infrastructure changes beyond scaling adjustments

### Deliverables

| Deliverable | Description | PRD/TDD Trace | Validation |
|-------------|-------------|---------------|------------|
| D6.1 | Penetration test report: external firm tests login, registration, token lifecycle, password reset, session management. Findings categorized as Critical/High/Medium/Low. All Critical and High findings must be remediated before M6 exit. | PRD risk: "Security breach from implementation flaws" | No Critical or High findings remaining; Medium findings have documented remediation timeline |
| D6.2 | SOC2 audit log validation report: confirm all auth events (registration, login success, login failure, lockout, token refresh, password reset request, password reset complete) are logged with required fields. Confirm 12-month retention policy is configured on audit_log table. Confirm logs queryable by user ID and date range. | SOC2 Type II requirement, PRD Legal/Compliance table | Independent audit of sample events; all required fields present; retention confirmed |
| D6.3 | GDPR compliance checklist: consent_at populated for all users registered after launch; only email, hashed password, display_name stored (no additional PII); right-to-erasure endpoint (DELETE /auth/me) available and tested | GDPR requirements: consent, data minimization | Consent field verified for 100% of post-launch registrations; deletion removes all PII within 30 days |
| D6.4 | Performance validation report: k6 load test at 500 concurrent users for 30 minutes. Metrics: login p95 < 200ms, registration p95 < 200ms, refresh p95 < 100ms, /auth/me p95 < 100ms. Zero 5xx errors. | NFR-PERF-001, NFR-PERF-002, TDD Section 17 | All latency targets met; zero errors; report includes p50, p90, p95, p99 |
| D6.5 | Finalized runbooks: AuthService down scenario, Token refresh failure scenario, Redis unavailability, PostgreSQL failover, SendGrid outage, RS256 key rotation procedure | TDD Section 25.1 | Each runbook reviewed by on-call engineer; at least one dry-run per runbook |
| D6.6 | On-call rotation: auth-team 24/7 rotation for first 2 weeks post-GA, then business-hours + P1 page. Escalation path documented: auth-team on-call -> test-lead -> eng-manager -> platform-team. | TDD Section 25.2 | Rotation schedule published; on-call engineer acknowledges |
| D6.7 | Capacity planning review: current resource utilization documented; scaling thresholds confirmed (HPA at CPU > 70%, PostgreSQL pool at connection wait > 50ms, Redis at memory > 70%) | TDD Section 25.3 | Utilization report matches TDD estimates within 20% |

### Dependencies

**Within milestone:**

- D6.1 (pen test) can run in parallel with D6.4 (load test)
- D6.2, D6.3 require production data to validate against

**Cross-milestone:**

- All M1-M5 deliverables must be in production before D6.1, D6.4 can execute

### Entry Criteria

- M5 Phase 3 GA complete: all traffic routing through new AuthService
- At least 7 days of production traffic data available
- External penetration testing firm engaged and scheduled

### Exit Criteria

- Penetration test: zero Critical findings, zero High findings, all Medium findings have remediation plan
- SOC2: audit log validation passes; all required fields present for sampled events; 12-month retention confirmed
- GDPR: consent_at populated for 100% of post-launch registrations; data minimization confirmed
- Performance: all latency targets met at 500 concurrent users
- Runbooks: all 6 scenarios reviewed and dry-run confirmed
- On-call: rotation schedule published; escalation path verified
- Capacity: resource utilization within expected bounds
- RS256 key rotation dry run: completed without service interruption

### Estimated Effort

1 sprint (2 weeks). Breakdown: D6.1 pen test coordination (ongoing during sprint; ~2 days engineering time for remediation), D6.2 SOC2 validation (2 days), D6.3 GDPR validation (1 day), D6.4 performance testing (3 days), D6.5 runbooks (2 days), D6.6 on-call setup (1 day), D6.7 capacity review (1 day).

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Penetration test finds Critical vulnerability requiring architectural change | Low | Critical | Budget 3 buffer days in sprint for remediation. If more time needed, extend sprint by 1 week rather than shipping with known Critical. |
| Performance targets not met at 500 concurrent users due to bcrypt bottleneck | Medium | High | bcrypt cost factor 12 at 500 concurrent users may saturate CPU. If p95 > 200ms, consider: (1) increase AuthService replicas via HPA, (2) reduce bcrypt cost to 11 with security approval, (3) implement credential verification queue with backpressure. |
| SOC2 audit reveals missing event types in audit log | Low | High | M2 and M4 wrote audit events for all defined flows. Review audit_log table contents against SOC2 control matrix before auditor arrives. |

### Validation/Acceptance Approach

- External: Penetration test report from security firm
- Internal: SOC2 validation against control matrix
- Automated: Performance test results from k6
- Manual: Runbook dry runs by on-call engineers
- Sign-off: eng-manager, sec-reviewer, and compliance team approve M6 exit

---

## Cross-Milestone Dependencies

### Dependency Graph

```
M1 (Data Foundation)
 ├──> M2 (Core Auth: Login/Logout)
 │     ├──> M3 (Token Lifecycle)
 │     │     ├──> M4 (Password Reset + Profile)
 │     │     │     └──> M5 (Frontend Integration + Rollout)
 │     │     │           └──> M6 (Hardening + Compliance)
 │     └──> M4 (audit log writer from M2 feeds M4 admin query)
 └──> M3 (UserProfile schema needed for JWT payload)
```

### Dependency Table

| From | To | Deliverable Linkage | Impact if Delayed |
|------|----|---------------------|-------------------|
| M1 D1.1 (schema) | M2 D2.1 (AuthService) | AuthService reads/writes UserProfile table | M2 blocked entirely |
| M1 D1.3 (PasswordHasher) | M2 D2.3 (login) | Login verifies credentials via PasswordHasher | M2 blocked entirely |
| M1 D1.4 (UserRepo) | M2 D2.2 (register) | Register creates UserProfile via UserRepo | M2 blocked entirely |
| M1 D1.2 (audit_log schema) | M2 D2.4 (audit writer) | Audit writer inserts into audit_log table | Audit logging blocked |
| M2 D2.1 (AuthService) | M3 D3.5, D3.6 | Token issuance integrated into login/register | M3 scope reduced (no token return on login/register) |
| M3 D3.2 (TokenManager) | M4 D4.2 (reset-confirm) | Reset invalidates all sessions via revokeAllForUser() | Password reset cannot invalidate sessions |
| M4 D4.1, D4.2 | M5 D5.5 | Frontend password reset wires to backend endpoints | Password reset UI has no backend |
| M5 D5.7 (GA rollout) | M6 (all) | Hardening validates production system | M6 cannot start until GA is stable |

### Critical Path

M1 -> M2 -> M3 -> M4 -> M5 (rollout) -> M6. All milestones are on the critical path. There is no parallelism in the milestone sequence because each milestone produces components that the next milestone directly consumes or extends.

The only parallelism available is within milestones (e.g., D4.3 SendGrid integration and D4.4 token storage can proceed in parallel within M4), and the parallel work of penetration testing (D6.1) and load testing (D6.4) within M6.

---

## Risk Register

| ID | Risk | Probability | Impact | Mitigation | Owner | Contingency |
|----|------|-------------|--------|------------|-------|-------------|
| RR-01 | bcrypt cost factor 12 causes p95 > 200ms at 500 concurrent users | Medium | High | Benchmark in M1; load test in M6; HPA to 10 replicas | auth-team lead | Reduce cost to 11 with security approval; increase replicas beyond 10 |
| RR-02 | Refresh token rotation race condition allows token reuse | Medium | High | Atomic Redis Lua script for compare-and-delete | auth-team | If race detected post-launch, emergency deploy to add distributed lock |
| RR-03 | SendGrid outage blocks password reset flow | Low | Medium | Retry logic (3 attempts, exponential backoff); queue for delayed delivery | auth-team | Fallback support channel; manual reset by admin via direct DB operation |
| RR-04 | User enumeration via timing attack on login endpoint | High | High | Dummy bcrypt verify for non-existent users; normalize response time within 50ms | sec-reviewer | If timing difference > 100ms, add fixed-delay padding to all login responses |
| RR-05 | Redis unavailability during production causes mass logout | Medium | Medium | Redis cluster with replication; fallback: reject refresh (users re-login); alert at connection failures > 10/min | platform-team | Scale Redis cluster; if persistent, switch to database-backed refresh token storage |
| RR-06 | XSS steals access token stored in JavaScript memory | Medium | High | Store accessToken in memory only; clear on tab close; 15-min TTL limits window; refreshToken in HttpOnly cookie | frontend-team | Force password reset for affected users; revoke all refresh tokens for user |
| RR-07 | GDPR compliance gap: consent_at not recorded for some registration paths | Low | High | Integration test asserts consent_at is non-null for all registrations; GDPR validation in M6 D6.3 | auth-team | Data migration to backfill consent_at; notify affected users for re-consent |
| RR-08 | SOC2 audit log missing required fields for some event types | Medium | High | M2 D2.4 and M4 D6 write audit events for all defined flows; M6 D6.2 validates sample against control matrix | auth-team | Emergency patch to add missing fields; manual log reconstruction from application logs |
| RR-09 | Registration conversion rate < 60% due to UX friction | Medium | Medium | Inline validation; minimal fields (email, password, display name); funnel analytics from day 1 | product-team | A/B test simplified registration flow; reduce to email + password only |
| RR-10 | RS256 key rotation causes brief verification failures during switchover | Low | Medium | Load both keys during rotation; verify tries new then old; remove old key only after 15-min TTL expires | auth-team | Immediate rollback to old key if errors spike |

---

## Success Metrics

| Metric | Target | Source | Measurement Method | Measurement Frequency | Owner |
|--------|--------|--------|--------------------|-----------------------|-------|
| Registration conversion rate | > 60% | PRD Success Metrics | Funnel: landing page visit -> register -> confirmed account | Daily | product-team |
| Login response time (p95) | < 200ms | FR-AUTH.1, NFR-PERF-001 | APM histogram on POST /auth/login | Continuous | auth-team |
| Token refresh latency (p95) | < 100ms | TDD Section 4.1 | APM histogram on POST /auth/refresh | Continuous | auth-team |
| Service availability | 99.9% | NFR-REL-001 | Health check monitoring over 30-day rolling windows | Continuous | auth-team |
| Average session duration | > 30 minutes | PRD Success Metrics | Token refresh event analytics | Weekly | product-team |
| Failed login rate | < 5% of attempts | PRD Success Metrics | auth_login_total counter (failure / total) | Daily | auth-team |
| Password reset completion | > 80% | PRD Success Metrics | Funnel: reset-requested -> reset-completed | Weekly | product-team |
| Registration success rate | > 99% | TDD Section 4.1 | Successful registrations / total registration attempts | Daily | auth-team |
| Unit test coverage | >= 80% | TDD Section 15.1 | Jest coverage report | Per-PR | auth-team |
| Email delivery within 60 seconds | 100% | PRD UX requirements | SendGrid delivery timestamp - request timestamp | Continuous | auth-team |
| Zero Critical/High pen test findings | 0 | PRD Risk Analysis | External penetration test report | At M6 | sec-reviewer |

---

## Out of Scope / Deferred

| Capability | Rationale | Planned For |
|------------|-----------|-------------|
| OAuth2/OIDC login (Google, GitHub) | Requires third-party integration infrastructure not yet available; adds complexity without addressing core v1.0 needs | v2.0 |
| Multi-factor authentication (SMS/TOTP) | Requires SMS/TOTP infrastructure; separate security project | v1.2 (per TDD NG-002) |
| Social login providers | Depends on OAuth/OIDC infrastructure | v2.0 |
| Role-based access control (RBAC) | Authorization is a separate concern; UserProfile.roles field exists but enforcement is deferred | Dedicated PRD |
| Email verification flow | PRD marks as "(Optional)" in signup journey; not required for v1.0 | v1.1 |
| API key authentication for service-to-service | Open question OQ-001 deferred to v1.1 | v1.1 |
| "Remember me" extended session | Open question from PRD; not resolved for v1.0 | v1.1 |
| Maximum refresh tokens per user | Open question from PRD; no limit enforced in v1.0 (re-evaluate if abuse observed) | v1.1 |
| Automated RS256 key rotation | Manual quarterly rotation in v1.0; automation deferred | Post-GA |
| Password hash migration (bcrypt -> argon2id) | PasswordHasher abstraction supports future migration; no migration planned yet | Post-GA |
| Admin dashboard UI | Backend admin API exists (GET /admin/auth-events); no dedicated frontend in v1.0 | v1.1 |

---

## Assumptions

1. **Email delivery infrastructure**: SendGrid API key is provisioned and operational before M4 development begins. If SendGrid is unavailable, a functionally equivalent transactional email service (e.g., AWS SES, Mailgun) can be substituted with <= 2 days of integration work.

2. **PostgreSQL 15+ availability**: A managed PostgreSQL 15+ instance is provisioned and accessible to auth-team before M1 begins. Connection string and credentials are available via Kubernetes secrets.

3. **Redis 7+ availability**: A managed Redis 7+ instance is provisioned before M3 begins. Auth-team has network access and can configure maxmemory-policy.

4. **Frontend framework compatibility**: The frontend supports client-side routing, React context API, and can make authenticated HTTP requests. The AuthProvider integration assumes React 18+ with hooks.

5. **API Gateway capability**: The API Gateway supports per-IP rate limiting with configurable thresholds (10 req/min, 5 req/min, 30 req/min, 60 req/min) and can add CORS headers restricted to known frontend origins.

6. **Kubernetes deployment**: AuthService runs as a Kubernetes Deployment with Horizontal Pod Autoscaler. RSA keys are mounted as Kubernetes secrets. The platform-team supports pod scaling to 10 replicas.

7. **No legacy auth migration**: There is no existing user data to migrate. The platform currently has no user accounts. Migration scripts are for future use only.

8. **Account lockout threshold**: 5 failed attempts within 15 minutes triggers account lockout. This is the threshold stated in FR-AUTH-001 AC4 and the PRD error handling table. This can be adjusted via environment variable without code changes.

9. **Password policy**: Minimum 8 characters, at least 1 uppercase letter, at least 1 digit. This is the interpretation of NIST SP 800-63B for v1.0. Security team has not yet reviewed; M1 entry requires confirmation.

10. **Single-region deployment**: v1.0 deploys to a single region. Cross-region replication, geo-distributed token validation, and region-failover are post-GA concerns.

11. **Email case sensitivity**: Emails are normalized to lowercase before storage and comparison. Two registrations that differ only in email casing are treated as duplicates.

12. **Refresh token limits**: No maximum number of refresh tokens per user is enforced in v1.0 (PRD open question #2 is unresolved). Each refresh creates a new token and revokes the old one, so the number of concurrent tokens equals the number of active devices.

13. **Clock synchronization**: All service instances use NTP with < 1 second drift. JwtService tolerates 5 seconds of clock skew (TDD Section 12), which is well within NTP accuracy.

---

## Compliance and Security Considerations

### SOC2 Type II Mapping

| SOC2 Control | Implementation | Milestone | Validation |
|--------------|----------------|-----------|------------|
| User access logging | audit_log table records all auth events with user_id, timestamp, IP, outcome | M2 D2.4, M4 D4.6 | M6 D6.2 |
| Access modification logging | Password reset events logged; session invalidation logged | M4 D4.6 | M6 D6.2 |
| Data retention | audit_log configured with 90-day retention in PostgreSQL; extensible to 12 months via partitioning | M6 D6.2 | Retention policy verified |
| Encryption at rest | PostgreSQL TDE enabled (managed service default); Redis persistence encrypted | Infrastructure | Verified in provisioning |
| Encryption in transit | TLS 1.3 on all endpoints (API Gateway terminates) | Infrastructure | Verified in M5 rollout |

### GDPR Mapping

| GDPR Requirement | Implementation | Milestone |
|-------------------|----------------|-----------|
| Consent at registration | consent_at timestamp column populated on registration; GDPR consent checkbox required on RegisterPage | M2 D2.2, M5 D5.2 |
| Data minimization | Only email, hashed password, display name collected. No additional PII fields. | M1 D1.1 schema |
| Right to erasure | DELETE /auth/me endpoint removes all PII (nullifies email, deletes password hash, anonymizes display_name) within 30 days | M6 D6.3 |
| Data portability | GET /auth/me returns all stored user data in structured JSON | M3 D3.4 |

### Threat Model Summary

| Threat Vector | Attack | Mitigation | Control Location |
|---------------|--------|------------|------------------|
| Credential brute-force | Automated password guessing | bcrypt cost 12 + rate limiting (10 req/min) + account lockout (5 failures / 15 min) | M1 D1.3, M2 D2.3, D2.5 |
| User enumeration | Login/reset-request reveals registered emails | Generic error messages + timing normalization + identical response bodies | M2 D2.3, M4 D4.1 |
| Token theft (XSS) | Malicious script steals access token | Access token in memory only (not localStorage); 15-min TTL; clear on tab close | M5 D5.3 |
| Token theft (network) | MITM intercepts tokens | TLS 1.3; HttpOnly cookies for refresh token | Infrastructure, M3 D3.2 |
| Refresh token replay | Stolen refresh token reused | Token rotation (old revoked on every refresh); atomic Redis compare-and-delete | M3 D3.2 |
| Password reset token reuse | Intercepted reset link used twice | Single-use tokens (deleted from Redis on use); 1-hour TTL; atomic Redis operations | M4 D4.2, D4.4 |
| Privilege escalation | User modifies JWT to add admin role | RS256 signing prevents tampering; verify signature on every request | M3 D3.1 |
| SQL injection | Malicious input in email/password fields | Parameterized queries via pg-pool; input validation; no string concatenation in SQL | M1 D1.4 |
| Timing attack on login | Attacker measures response time to enumerate users | Dummy bcrypt verify for non-existent users; response time normalized within 50ms | M2 D2.3 |

---

## Operational Readiness

### Observability Stack

| Signal | Tool | Metric/Log | Alert Threshold |
|--------|------|------------|-----------------|
| Login failures | Prometheus | auth_login_total{outcome="failure"} | > 20% failure rate over 5 minutes |
| Login latency | Prometheus | auth_login_duration_seconds | p95 > 500ms |
| Token refresh errors | Prometheus | auth_token_refresh_total{outcome!="success"} | > 10 errors/min |
| Registration count | Prometheus | auth_registration_total{outcome="success"} | (dashboard only) |
| Redis connection failures | Prometheus | redis_connection_errors_total | > 10 failures/min |
| Email delivery failures | Prometheus | auth_email_send_total{outcome="failure"} | > 5% failure rate over 10 minutes |
| Structured logs | stdout (JSON) | All auth events with correlation IDs | Log aggregation picks up |
| Distributed traces | OpenTelemetry | Spans: AuthService, PasswordHasher, TokenManager, JwtService | Trace sampling at 10% |

### Runbook Scenarios

| Scenario | Symptoms | Resolution Summary |
|----------|----------|-------------------|
| AuthService down | 5xx on all /auth/* endpoints | Restart pods; check PostgreSQL connectivity; check PasswordHasher/TokenManager init |
| Token refresh failures | Users logged out unexpectedly; refresh error counter spike | Check Redis connectivity; verify JwtService signing key; check AUTH_TOKEN_REFRESH flag |
| Redis unavailable | POST /auth/refresh returns 503; users must re-login | Scale Redis cluster; if persistent, switch to DB-backed tokens |
| PostgreSQL failover | Connection errors; writes failing | Failover to read replica; verify connection string update |
| SendGrid outage | Password reset emails not delivered | Retry queue; monitor SendGrid status page; fallback to support channel |
| RS256 key rotation | Token verification errors during rotation | Load both keys; remove old key only after 15-min TTL window |
| Account lockout storm | Many users locked simultaneously | Check for brute-force attack pattern; consider IP-level blocking at WAF |

### On-Call Expectations

| Aspect | Expectation |
|--------|-------------|
| Response time | Acknowledge P1 alerts within 15 minutes |
| Coverage | auth-team 24/7 on-call rotation for first 2 weeks post-GA, then business-hours + P1 page |
| Tooling access | Kubernetes dashboards, Grafana, Redis CLI, PostgreSQL admin, SendGrid dashboard |
| Escalation path | auth-team on-call -> test-lead -> eng-manager -> platform-team |
| Incident response | Structured logs and traces available for diagnosis; rollback procedure documented and tested |

### Capacity Planning

| Resource | Current Capacity | Expected Load (v1.0) | Scaling Threshold | Scale Target |
|----------|-----------------|---------------------|-------------------|--------------|
| AuthService pods | 3 replicas | 500 concurrent users | CPU > 70% | 10 replicas via HPA |
| PostgreSQL connections | 100 pool size | 50 avg concurrent queries | Connection wait > 50ms | Pool to 200 |
| Redis memory | 1 GB | ~100K tokens (~50 MB) | Memory > 70% utilized | 2 GB |
| SendGrid | 100 emails/day | ~1000 resets/day estimated | N/A (high limit) | N/A |

---

## Sequencing Rationale

### Why this order and not another?

**M1 before M2**: The data schema, password hasher, and repository are the foundation. No authentication logic can function without persistent storage and credential verification. Attempting to build the login endpoint without a tested UserRepo and PasswordHasher would produce untestable code.

**M2 before M3**: AuthService registration and login must exist before token issuance can be integrated into them. The account lockout logic and anti-enumeration measures in M2 are security-critical and must be validated independently, before token logic adds complexity. Building tokens first would require stubbing the login flow, then reworking it.

**M3 before M4**: Password reset (M4) requires TokenManager.revokeAllForUser() to invalidate sessions on password change. Building password reset before token management would leave a gap where changed passwords do not invalidate existing sessions — a security vulnerability that would need to be patched later.

**M4 before M5**: Frontend integration requires all backend endpoints to be stable and tested. Building frontend components against incomplete or changing backend APIs produces rework and fragile integration tests. The password reset frontend (D5.5) specifically requires the reset-request and reset-confirm endpoints from M4.

**M5 before M6**: Hardening and compliance validation (penetration testing, SOC2 audit, performance testing at scale) require the complete system to be running in production with real traffic. Testing an incomplete system would produce misleading results.

**Alternative considered — Frontend-first with mocked backend**: This would allow parallel frontend/backend development but introduces risk of mock drift (frontend works against mocks but fails against real API). Given the small team size (3-5 engineers), the serial approach reduces coordination overhead and eliminates mock-drift risk entirely.

**Alternative considered — Token-first (M3 before M2)**: JwtService and TokenManager have no dependency on login/registration logic and could be built first. However, tokens have no meaning without a use case. Building tokens first creates unvalidated code that may need rework once login/registration requirements are fully understood during implementation.

---

## Appendix A: Open Questions Resolution Status

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| PRD OQ1 | Password reset emails: sync or async? | Resolved in M4 | Async with retry (3 attempts, exponential backoff). Sync would block the HTTP response and add latency to the reset-request endpoint. |
| PRD OQ2 | Max refresh tokens per user? | Deferred to v1.1 | No limit enforced in v1.0. Rotation ensures one token per refresh; concurrent devices each have their own token. If abuse is observed, add per-user limit. |
| PRD OQ3 | Account lockout policy? | Resolved in M2 | 5 failed attempts within 15 minutes locks the account. locked_until column stores unlock timestamp. Admin can unlock manually via direct DB operation. |
| PRD OQ4 | "Remember me" support? | Deferred to v1.1 | Not implemented in v1.0. Refresh token already provides 7-day session persistence. "Remember me" would extend this to 30 days, requiring product decision on security trade-off. |
| TDD OQ1 | API key auth for service-to-service? | Deferred to v1.1 | Not in v1.0 scope. Services should use JWT tokens obtained via client-credentials flow (future OAuth2 infrastructure). |
| TDD OQ2 | Max UserProfile roles array length? | Deferred to RBAC PRD | No limit enforced in v1.0. roles field is a text[] with default ["user"]. RBAC design will define valid roles and constraints. |

---

## Appendix B: State-Mechanics Invariants

This section documents the state invariants that must hold at all times. Violation of any invariant is a P1 bug.

| Invariant ID | Invariant | Enforcement Location | Validation |
|--------------|-----------|---------------------|------------|
| INV-01 | Passwords are never stored in plaintext anywhere (database, logs, error messages, debug output) | PasswordHasher.hash() always returns bcrypt hash; AuthService never logs password parameter; error responses never include password | Code review + grep test in CI |
| INV-02 | Each refresh token is used exactly once (rotation) | TokenManager.refresh() atomically deletes old token and creates new one via Redis Lua script | Integration test: second use of same token returns 401 |
| INV-03 | Password reset invalidates all existing sessions | AuthService calls TokenManager.revokeAllForUser() after password update | Integration test: refresh token rejected after password change |
| INV-04 | Password reset tokens are single-use | Redis key deleted on successful reset-confirm | Integration test: second confirm with same token returns 401 |
| INV-05 | Account lockout is atomic: 5th failed attempt triggers lock even under concurrent requests | PostgreSQL atomic UPDATE + RETURNING pattern | Integration test: 5 concurrent failed logins result in exactly 1 lock |
| INV-06 | Login responses for non-existent users are indistinguishable from wrong-password responses (status code, body, timing within 50ms) | AuthService performs dummy bcrypt verify for non-existent users | Automated timing comparison test |
| INV-07 | JWT payload contains no PII (only sub=userId, roles, iat, exp) | JwtService.sign() constructs payload from explicitly listed fields | Unit test asserts JWT payload structure |
| INV-08 | All auth events produce an audit log row with required fields (user_id, event_type, ip_address, outcome, created_at) | Audit writer called in every auth flow path (success and failure) | Integration test for each event type |
| INV-09 | Email addresses are normalized to lowercase before comparison and storage | AuthService.register() and AuthService.login() call email.toLowerCase() before any lookup or insert | Unit test with mixed-case email |
| INV-10 | Access tokens are never stored in localStorage or sessionStorage by the frontend | AuthProvider uses in-memory state only; refreshToken in HttpOnly cookie set by backend | ESLint rule + Playwright test verifying no localStorage access in auth module |
