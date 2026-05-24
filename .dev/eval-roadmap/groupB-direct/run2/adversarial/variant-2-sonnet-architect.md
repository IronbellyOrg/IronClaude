---
id: "AUTH-001-ROADMAP"
title: "User Authentication Service — Implementation Roadmap"
source: "merged-prd-tdd-user-auth.md (AUTH-MERGED-PRD-TDD)"
generated_by: "system-architect (Sonnet)"
generated_at: "2026-05-22"
version: "1.0"
---

# User Authentication Service — Implementation Roadmap

---

## Executive Summary

This roadmap sequences the delivery of the User Authentication Service (v1.0) across five milestones spanning approximately 10 weeks, targeting general availability by early June 2026 in alignment with the Q2 2026 release window and the Q3 2026 SOC2 Type II audit deadline. The service covers user registration, login, logout, session persistence via JWT access/refresh tokens, profile retrieval, and self-service password reset. Success is measured against concrete targets drawn from the PRD and TDD: registration conversion above 60%, login p95 latency below 200ms, session duration above 30 minutes, failed login rate below 5%, and password reset completion above 80% (PRD Success Metrics table). SOC2 audit logging is embedded from the first milestone rather than bolted on later, and the phased rollout strategy uses feature flags (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH) to de-risk the production cut-over.

---

## Milestones

---

### M1: Infrastructure, Schema, and Security Foundations

**Objective:** Provision all infrastructure dependencies, define and deploy the database schema, implement PasswordHasher, and establish the audit logging pipeline that SOC2 requires from day one.

**Scope:**

- In: PostgreSQL 15+ and Redis 7+ provisioning; users and audit_log table creation; PasswordHasher module with bcrypt cost 12; structured audit log emitter; CI pipeline with testcontainers; Prometheus metrics scaffolding for auth_login_total, auth_login_duration_seconds, auth_registration_total, auth_token_refresh_total (TDD Section 14).
- Out: AuthService orchestration; token issuance; API endpoints; frontend components; email integration.

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D1.1 | PostgreSQL schema migration: users table (id UUID PK, email UNIQUE NOT NULL, password_hash, display_name 2-100 chars, created_at, updated_at, last_login_at, roles TEXT[] DEFAULT '{user}', locked_until TIMESTAMP, failed_login_count INT DEFAULT 0) | TDD Section 7.1 UserProfile fields; PRD FR-AUTH.2 duplicate rejection |
| D1.2 | PostgreSQL schema migration: audit_log table (id, user_id, event_type, ip_address, user_agent, outcome, timestamp) with 12-month retention policy and indexes on (user_id, timestamp) and (event_type, timestamp) | PRD Legal/Compliance table — SOC2 Type II 12-month retention; PRD FR-AUTH.5 audit logging AC |
| D1.3 | PasswordHasher module: hash(plaintext, cost=12) and verify(plaintext, hash) functions with bcrypt; benchmark asserting hash time under 500ms (TDD Section 17) | TDD NFR-SEC-001; TDD Section 6.4 design decisions |
| D1.4 | Audit log emitter: emits structured JSON events for all auth state transitions (registration_attempt, login_attempt, login_success, login_failure, account_locked, password_reset_requested, password_reset_completed, token_revoked) | PRD Legal/Compliance — SOC2 user ID, timestamp, IP, outcome |
| D1.5 | Redis 7+ cluster provisioned with TLS, 1 GB initial allocation, monitoring for >70% utilization (scale to 2 GB trigger) | TDD Section 25.3 capacity planning |
| D1.6 | CI pipeline: Docker Compose for local dev (PostgreSQL, Redis); testcontainers for CI ephemeral databases; Jest + ts-jest configured for 80% unit coverage gate | TDD Section 15.3 test environments |
| D1.7 | Prometheus exporters registered for auth_login_total, auth_login_duration_seconds, auth_registration_total, auth_token_refresh_total; Grafana dashboard skeleton | TDD Section 14 — Observability |

**Acceptance Criteria:**

1. Schema migrations run idempotently on empty PostgreSQL instance; rollback tested.
2. PasswordHasher.hash() produces bcrypt output with cost 12; verify() correctly matches and rejects; benchmark under 500ms on CI hardware (TDD Section 17).
3. Audit log emitter writes a valid JSON record to audit_log table containing user_id, event_type, timestamp, ip_address, outcome for each emitted event.
4. Redis reachable from service network; TLS enforced; ping latency under 5ms.
5. CI pipeline runs on every PR; testcontainers spin up PostgreSQL and Redis; tests pass.

**Dependencies:**

- External: PostgreSQL 15+ cluster provisioned by platform team; Redis 7+ provisioned; SendGrid account credentials available for later milestone.
- Internal: None (this is the first milestone).

**Estimated Duration:** 2 weeks.

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| PostgreSQL provisioning delayed by infra team | Medium | High | Begin schema design in parallel using Docker Compose local environment; trigger provisioning request on day one. |
| bcrypt cost 12 exceeds 500ms on CI hardware | Low | Medium | Profile on CI runners first; if over budget, propose cost 11 with security team sign-off per SEC-POLICY-001. |
| Audit log schema too narrow for future SOC2 control mapping | Medium | Medium | Include extensible metadata JSONB column in audit_log; validate against SOC2 trust service criteria catalog before schema freeze. |

---

### M2: Authentication Core — Registration, Login, Logout

**Objective:** Implement AuthService orchestration for user registration and login/logout flows, wiring PasswordHasher to the database and issuing initial JWT access tokens (refresh tokens deferred to M3 for clean separation).

**Scope:**

- In: AuthService.login(), AuthService.register(), AuthService.logout(); POST /auth/login, POST /auth/register endpoints; input validation (email format, password policy: minimum 8 chars, uppercase, number); duplicate email handling (409 Conflict); account lockout after 5 failed attempts within 15 minutes (423 Locked); generic error responses preventing user enumeration; API Gateway rate limiting configuration (10 req/min per IP for login, 5 req/min for register).
- Out: Token refresh flow (M3); password reset (M4); profile retrieval (M3); frontend pages (M5).

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D2.1 | AuthService.login(email, password): normalizes email to lowercase; calls PasswordHasher.verify(); on success issues access token via JwtService (15-min TTL); on failure increments failed_login_count; at >=5 failures within 15 min sets locked_until and emits account_locked audit event; returns generic 401 for wrong password, unknown email, and locked accounts (no enumeration) | PRD FR-AUTH.1 AC; TDD FR-AUTH-001 AC items 1-4; PRD Error Handling table — wrong password <5 and >=5 attempts |
| D2.2 | AuthService.register(email, password, displayName): validates email format, password policy (>=8 chars, uppercase, number), displayName (2-100 chars); normalizes email to lowercase; checks uniqueness via DB unique constraint (not application-level check, to handle concurrent registration race); hashes password via PasswordHasher; inserts UserProfile; emits registration_attempt and login_success audit events; auto-logs user in (returns access token) | PRD FR-AUTH.2 AC; TDD FR-AUTH-002 AC items 1-4; PRD Signup Flow — "submit -> logged in and redirected" |
| D2.3 | AuthService.logout(userId): revokes all refresh tokens for user in Redis (TokenManager integration placeholder); emits token_revoked audit event; returns 200 | PRD "Log Out ends session immediately" AC |
| D2.4 | POST /auth/login endpoint: accepts {email, password}; returns 200 with {accessToken, expiresIn: 900, tokenType: "Bearer"} or error; rate limited at 10 req/min per IP at API Gateway | TDD Section 8.2 POST /auth/login |
| D2.5 | POST /auth/register endpoint: accepts {email, password, displayName}; returns 201 with UserProfile or error (400 validation, 409 duplicate); rate limited at 5 req/min per IP | TDD Section 8.2 POST /auth/register |
| D2.6 | JwtService: sign(payload, RS256, 15-min TTL) and verify(token, RS256) with 2048-bit RSA key loaded from secrets mount; 5-second clock skew tolerance; key rotation documented for quarterly cadence | TDD Section 6.4 key decisions; TDD NFR-SEC-002; TDD Section 12 clock skew tolerance |
| D2.7 | Unit tests: valid login returns token; invalid credentials return 401; locked account returns 423; duplicate email returns 409; weak password returns 400 with field-level errors; password never appears in logs | TDD Section 15.2 unit test table |
| D2.8 | Integration tests: full registration flow through PasswordHasher to database insert; concurrent duplicate email race handled by unique constraint; login flow end-to-end against real PostgreSQL | TDD Section 15.2 integration test table |

**Acceptance Criteria:**

1. POST /auth/login with valid credentials returns 200 with accessToken (JWT, RS256-signed, 15-min TTL) within 200ms p95 (TDD NFR-PERF-001).
2. POST /auth/login with wrong password returns 401 with body {error: {code: "AUTH_INVALID_CREDENTIALS", message: "The provided email or password is incorrect.", status: 401}} — identical response for non-existent email (PRD Error Handling — no user enumeration).
3. POST /auth/login after 5 failures within 15 minutes returns 423 Locked (TDD FR-AUTH-001 AC item 4).
4. POST /auth/register with valid input returns 201 with UserProfile including id (UUID v4), email (lowercase), displayName, createdAt, roles=["user"], lastLoginAt=null (TDD FR-AUTH-002 AC item 1).
5. POST /auth/register with duplicate email returns 409 Conflict (TDD FR-AUTH-002 AC item 2).
6. POST /auth/register with password "short" returns 400 with field-level validation errors (TDD FR-AUTH-002 AC item 3).
7. All auth events (login_attempt, login_success, login_failure, registration_attempt, registration_success, account_locked) emitted to audit_log with user_id, timestamp, IP, outcome (PRD SOC2 requirement).
8. Unit test coverage for AuthService and PasswordHasher exceeds 80% (TDD Section 24.1 DoD).
9. Concurrent registration with identical email handled gracefully (first wins, second gets 409; no duplicate rows) (TDD Section 12 — concurrent registration edge case).

**Dependencies:**

- M1 (schema, PasswordHasher, audit logger, Redis provisioned).

**Estimated Duration:** 2 weeks.

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Account lockout threshold (5/15min) too aggressive for legitimate typo-prone users | Medium | Medium | Make lockout threshold and window configurable via environment variables; monitor locked account rate in first 2 weeks of beta; adjust if >2% of users hit lockout. |
| RS256 key rotation not yet automated; manual rotation introduces risk | Medium | Low | Document manual rotation procedure for v1.0; add key rotation automation to v1.1 backlog; rotate once before GA as dry run. |
| API Gateway rate limiting configuration varies between staging and production | Low | High | Define rate limits as infrastructure-as-code (Terraform/Pulumi) applied identically to all environments; validate in staging load test. |

---

### M3: Token Lifecycle, Session Persistence, and Profile Retrieval

**Objective:** Implement TokenManager for the full JWT access/refresh token lifecycle, add the GET /auth/me profile endpoint, and enable multi-device session support with revocation.

**Scope:**

- In: TokenManager (issue, refresh, revoke); POST /auth/refresh endpoint; GET /auth/me endpoint; refresh token storage in Redis with 7-day TTL; opaque refresh tokens (not JWT); rotation-on-refresh (old token revoked, new pair issued); silent token refresh in AuthProvider (placeholder contract for M5); multi-device concurrent sessions (both valid per PRD Error Handling — "Concurrent login from multiple devices: Both sessions valid"); Redis unavailability graceful degradation (reject refresh, force re-login).
- Out: Password reset flow (M4); frontend components (M5).

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D3.1 | TokenManager.issueTokens(userId, roles): generates access token (JwtService, 15-min TTL) and opaque refresh token (crypto-random, 256-bit); stores hashed refresh token in Redis keyed by userId with 7-day TTL; returns AuthToken {accessToken, refreshToken, expiresIn: 900, tokenType: "Bearer"} | TDD Section 7.1 AuthToken interface; TDD FR-AUTH-003 AC item 1 |
| D3.2 | TokenManager.refresh(oldRefreshToken): validates old token against Redis; on match, revokes old token (DEL), issues new AuthToken pair (rotation-on-refresh); emits token_refresh_success audit event; on mismatch/expiry returns 401 with AUTH_TOKEN_EXPIRED or AUTH_TOKEN_REVOKED error code; emits token_refresh_failure audit event | TDD FR-AUTH-003 AC items 2-4; TDD Section 12 — revoked vs expired distinction |
| D3.3 | TokenManager.revokeAllForUser(userId): deletes all refresh tokens for a user from Redis; used by logout and password reset flows | PRD FR-AUTH.5 AC — "new password invalidates all sessions" |
| D3.4 | POST /auth/refresh endpoint: accepts {refreshToken}; returns 200 with new AuthToken pair or 401; rate limited at 30 req/min per user | TDD Section 8.2 POST /auth/refresh; TDD Section 8.1 rate limit table |
| D3.5 | GET /auth/me endpoint: validates Bearer accessToken; returns UserProfile with id, email, displayName, createdAt, updatedAt, lastLoginAt, roles; returns 401 for missing/expired/invalid token | TDD Section 8.2 GET /auth/me; TDD FR-AUTH-004 AC items 1-3 |
| D3.6 | AuthService.logout wiring: calls TokenManager.revokeAllForUser(userId); invalidates all sessions; redirects to landing page per PRD AC | PRD "Log Out" AC |
| D3.7 | Redis unavailability handling: if Redis unreachable during refresh, return 401 AUTH_SERVICE_UNAVAILABLE with retry-after header; do not serve stale tokens; alert fires via existing Redis connection failure monitoring (TDD Section 14) | TDD Section 12 — Redis fallback |
| D3.8 | Unit tests: token refresh with valid token returns new pair; expired refresh token returns 401; revoked refresh token returns 401; rotation-on-refresh prevents reuse of old token | TDD Section 15.2 TokenManager test cases |
| D3.9 | Integration tests: full token lifecycle against real Redis (issue, refresh, verify old token revoked); expired Redis TTL correctly invalidates refresh tokens | TDD Section 15.2 integration — "Expired refresh token rejected by TokenManager" |
| D3.10 | Load test script (k6): simulate 500 concurrent token refresh operations; validate p95 < 100ms for refresh (TDD Section 4.1 technical metrics) | TDD NFR-PERF-002; TDD Section 4.1 token refresh latency target |

**Acceptance Criteria:**

1. POST /auth/refresh with valid refresh token returns 200 with new AuthToken pair; old refresh token is revoked (subsequent use returns 401) (TDD FR-AUTH-003 AC items 2, 4).
2. POST /auth/refresh with expired refresh token returns 401 with AUTH_TOKEN_EXPIRED error code (TDD FR-AUTH-003 AC item 3).
3. GET /auth/me with valid accessToken returns UserProfile with all fields matching TDD Section 7.1 schema (TDD FR-AUTH-004 AC item 1).
4. GET /auth/me with expired token returns 401 (TDD FR-AUTH-004 AC item 2).
5. Token refresh latency p95 < 100ms under 500 concurrent requests (TDD Section 4.1).
6. Redis failure during refresh returns 401 (not stale data) and triggers alert (TDD Section 12).
7. Logout revokes all refresh tokens for the user; subsequent refresh attempts return 401.
8. All token lifecycle events (token_issued, token_refreshed, token_revoked, token_expired) emitted to audit_log.
9. JWT access token payload includes userId and roles; signed RS256; expires in exactly 900 seconds (TDD Section 7.1 AuthToken fields).
10. 7-day refresh token TTL enforced by Redis TTL; verified via integration test that sets TTL to 1 second and confirms expiration.

**Dependencies:**

- M1 (Redis provisioned, JwtService keys).
- M2 (AuthService login/register emitting initial access tokens).

**Estimated Duration:** 2 weeks.

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Refresh token rotation creates race condition when two tabs refresh simultaneously | Medium | High | Use Redis WATCH/MULTI (optimistic locking) on refresh token key; only first refresh succeeds, second gets 401 and must re-authenticate. Document this as expected behavior for concurrent tab scenarios. |
| Redis single point of failure for all sessions | Medium | High | Deploy Redis in sentinel or cluster mode from day one; test failover in staging. If budget constrains, document SPOW risk and add cluster to v1.1 hardening backlog. |
| 7-day refresh TTL too long for security posture; too short for user experience | Low | Medium | Make TTL configurable via environment variable (default 7 days per TDD spec); monitor average session duration metric against >30 min target; adjust in Phase 2 beta based on data. |

---

### M4: Password Reset, Email Integration, and Admin Audit Views

**Objective:** Complete the self-service password reset flow with email delivery, implement admin-facing audit log querying, and harden the reset flow against enumeration and replay attacks.

**Scope:**

- In: POST /auth/reset-request; POST /auth/reset-confirm; reset token generation (single-use, 1-hour TTL); SendGrid email integration; reset email template; enumeration prevention (identical response for registered and unregistered emails); session invalidation on password change; admin audit log query endpoint (by user_id, date_range, event_type); GDPR consent recording at registration.
- Out: Frontend pages (M5); rollout and feature flags (M6).

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D4.1 | AuthService.requestPasswordReset(email): generates crypto-random reset token (256-bit); stores hashed token in Redis with 1-hour TTL keyed by email; sends email via SendGrid with reset link containing token; returns identical success response for registered and unregistered emails (no enumeration); emits password_reset_requested audit event | PRD FR-AUTH.5 AC; TDD FR-AUTH-005 AC items 1, 3; PRD Error Handling — "Reset requested for unregistered email: Same success response" |
| D4.2 | AuthService.confirmPasswordReset(token, newPassword): validates token against Redis; on match, hashes new password via PasswordHasher; updates users table; deletes reset token (single-use enforcement); calls TokenManager.revokeAllForUser(userId) to invalidate all sessions; emits password_reset_completed audit event; returns success redirect to login | TDD FR-AUTH-005 AC items 2, 4; PRD Password Reset Flow — "new password invalidates all sessions"; PRD Error Handling — expired reset link |
| D4.3 | POST /auth/reset-request endpoint: accepts {email}; returns 200 with confirmation message (identical for all emails); rate limited at 3 req/min per IP; email delivered within 60 seconds (PRD target) | PRD Password Reset Flow — "email delivered within 60 seconds" |
| D4.4 | POST /auth/reset-confirm endpoint: accepts {token, password}; returns 200 on success or 400/401 on failure; expired tokens return clear error with option to re-request | PRD Error Handling — "Expired reset link: Clear error with option to request a new link" |
| D4.5 | SendGrid integration module: transactional email template for password reset; includes user agent and IP in email for suspicious activity awareness; delivery monitoring with alerting on bounce rate >5% | PRD Dependencies table — SendGrid dependency; TDD Section 18 external deps |
| D4.6 | GDPR consent recording: registration endpoint records consent timestamp in audit_log alongside registration event; consent text version stored in event metadata for audit trail | PRD Legal/Compliance — "Consent at registration: consent recorded with timestamp" |
| D4.7 | Admin audit query API: GET /admin/audit-logs?user_id=&event_type=&from=&to= (internal, requires admin role); returns paginated results from audit_log; queryable by date range, user, and event type per PRD AC | PRD FR-AUTH.5 admin story — "Logs include user ID, event type, timestamp, IP address, and outcome. Queryable by date range and user." |
| D4.8 | Integration tests: full reset flow (request -> email mock -> confirm -> verify password changed -> verify sessions revoked); expired token rejection; reused token rejection; concurrent reset request handling | TDD Section 15.2 integration test pattern |
| D4.9 | Load test for reset flow: 100 concurrent reset requests; email delivery pipeline does not block API response (async dispatch); p95 for POST /auth/reset-request under 200ms | PRD Open Question 1 — async email dispatch is the correct architectural choice |

**Acceptance Criteria:**

1. POST /auth/reset-request for registered email sends reset email within 60 seconds; returns 200 with generic confirmation (PRD FR-AUTH.5 AC).
2. POST /auth/reset-request for unregistered email returns identical 200 response; no email sent (PRD Error Handling).
3. POST /auth/reset-confirm with valid token and strong password updates password hash; all existing refresh tokens revoked; all active sessions terminated (TDD FR-AUTH-005 AC item 2; PRD AC "new password invalidates all sessions").
4. POST /auth/reset-confirm with expired token (TTL > 1 hour) returns error with AUTH_RESET_TOKEN_EXPIRED code and message suggesting re-request (PRD Error Handling).
5. POST /auth/reset-confirm with already-used token returns 401; single-use enforcement verified (TDD FR-AUTH-005 AC item 4).
6. Admin audit query returns results filtered by user_id, event_type, and date range with pagination; results include user ID, event type, timestamp, IP, outcome (PRD admin AC).
7. GDPR consent recorded at registration with timestamp and consent text version in audit_log metadata.
8. SendGrid delivery monitoring alert fires if bounce rate exceeds 5% over 1-hour window.

**Dependencies:**

- M1 (audit_log schema, Redis).
- M2 (AuthService, PasswordHasher).
- M3 (TokenManager.revokeAllForUser for session invalidation on password change).
- External: SendGrid API credentials and approved sender domain configured.

**Estimated Duration:** 2 weeks.

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| SendGrid downtime blocks password reset flow entirely | Low | High | Implement email delivery as async queue (not blocking API response); monitor delivery queue depth; alert on queue backlog >100; document fallback support channel for reset during outages (PRD risk table). |
| Reset token race: user clicks link in two emails, both reset tokens valid | Low | Medium | Enforce single-use at Redis level: first confirm consumes token; second attempt gets 401. Send only one valid reset token per email at a time (new request invalidates previous). |
| Admin audit query performance degrades with 12-month data volume | Medium | Medium | Index on (user_id, timestamp) and (event_type, timestamp) from D1.2; paginate all queries; add query timeout at 5 seconds; consider partitioning by month if volume exceeds 10M rows. |
| Password reset email lands in spam | Medium | High | Pre-warm SendGrid domain; configure SPF, DKIM, DMARC before beta; include plaintext version of email; test against major providers (Gmail, Outlook) in staging. |

---

### M5: Frontend Integration, E2E Validation, and Security Hardening

**Objective:** Build and integrate LoginPage, RegisterPage, AuthProvider, and ProfilePage; validate all user journeys end-to-end; conduct security review and penetration testing against OWASP ASVS L2.

**Scope:**

- In: LoginPage component (email/password form, generic errors, rate limit UX, lockout messaging); RegisterPage component (email/password/displayName form, inline validation, GDPR consent checkbox, password strength meter); AuthProvider context (token storage in memory — not localStorage — per TDD R-001 mitigation, silent refresh on 401 interception, redirect to LoginPage on refresh failure); ProfilePage component (display name, email, creation date); E2E test suite (Playwright); security review (RS256 key validation, bcrypt cost verification, OWASP ASVS L2 checklist); penetration testing.
- Out: Production rollout (M6).

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D5.1 | LoginPage: email/password fields; submit calls POST /auth/login; stores AuthToken in memory via AuthProvider (not localStorage — TDD R-001 mitigation); displays generic "Invalid email or password" on 401; displays lockout message on 423; redirects to dashboard on success; loads in under 1 second (PRD Returning User Login journey — "Login form loads in under 1 second") | TDD Section 10.2 LoginPage props; PRD Login Flow; PRD UX Requirements |
| D5.2 | RegisterPage: email, password, displayName fields with inline validation (email format, password >=8 chars + uppercase + number, displayName 2-100 chars); GDPR consent checkbox with timestamp recording; submit calls POST /auth/register; auto-login on success; redirect to dashboard within 2 seconds of form submission (PRD First-Time Signup journey — "redirected to the dashboard within 2 seconds") | TDD Section 10.2 RegisterPage props; PRD Signup Flow |
| D5.3 | AuthProvider: React context managing AuthToken state in memory; transparent token refresh via POST /auth/refresh when accessToken expires or 401 intercepted; redirect to LoginPage when refresh fails; clears tokens on tab/window close; exposes userProfile and isAuthenticated to children; wraps all routes per TDD Section 10.3 component hierarchy | TDD Section 10.2 AuthProvider; TDD Section 10.3 hierarchy; PRD FR-AUTH.3 — "Sessions persist across page refreshes" |
| D5.4 | ProfilePage: fetches GET /auth/me; displays displayName, email, createdAt; renders in under 1 second; shows login prompt if unauthenticated | TDD Section 10.1 route table — /profile; PRD FR-AUTH.4 AC |
| D5.5 | E2E test suite (Playwright): (1) Full registration -> auto-login -> profile view; (2) Login with valid credentials -> navigate -> session persists on refresh; (3) Login with invalid credentials -> generic error; (4) Token expires during active session -> silent refresh -> no data loss; (5) Password reset flow end-to-end; (6) Logout -> verify session terminated -> verify redirected to landing page | TDD Section 15.2 E2E test table |
| D5.6 | Security review report: bcrypt cost factor 12 verified; RS256 2048-bit key rotation schedule documented; no passwords or tokens in application logs; CORS restricted to known frontend origins; TLS 1.3 enforced on all endpoints; OWASP ASVS L2 checklist items addressed | TDD Section 13; PRD NFR-AUTH.3; PRD Risk Analysis — "Security breach" mitigation |
| D5.7 | Penetration test report: automated scan (OWASP ZAP or equivalent) plus manual testing of: login brute-force lockout enforcement, token theft scenarios, XSS token exfiltration attempts, concurrent session handling, reset token replay, user enumeration via timing analysis | PRD Risk Analysis — "Dedicated security review; penetration testing before production" |

**Acceptance Criteria:**

1. LoginPage submits credentials to POST /auth/login; success redirects to dashboard; failure shows generic error with no timing-based user enumeration (response time variance <50ms between valid and invalid email).
2. RegisterPage validates all fields client-side before submission; password strength requirements visible; GDPR consent mandatory (form disabled without checkbox); duplicate email shows user-friendly message.
3. AuthProvider stores accessToken in memory only (not localStorage, not sessionStorage); silent refresh triggers when accessToken within 60 seconds of expiry; tab close clears tokens (TDD R-001).
4. ProfilePage displays all UserProfile fields; redirects to LoginPage when unauthenticated.
5. E2E test suite covers all 6 scenarios listed in D5.5; all pass against staging environment.
6. Security review report confirms: bcrypt cost 12 enforced, RS256 signing active, no secrets in logs, CORS whitelisted, TLS 1.3 only.
7. Penetration test report shows zero critical findings; any high findings have documented remediation plan before M6 gate.
8. Registration form submission to dashboard redirect completes in under 2 seconds (PRD First-Time Signup).
9. Registration conversion funnel tracking instrumented: landing -> register click -> form submitted -> account created -> dashboard loaded (PRD >60% conversion target measurement).

**Dependencies:**

- M2 (login/register endpoints).
- M3 (token refresh, GET /auth/me).
- M4 (password reset endpoints).
- External: Frontend build pipeline; staging environment with backend deployed.

**Estimated Duration:** 2 weeks (can partially overlap with M4 backend work for LoginPage/RegisterPage scaffolding).

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Penetration test reveals critical vulnerability blocking GA | Low | Critical | Schedule pen test at start of M5 (not end); allocate 3-day buffer for remediation; if critical finding found, extend M5 by up to 1 week before blocking M6 gate. |
| AuthProvider silent refresh causes redirect loop on stale tokens | Medium | High | Implement circuit breaker: after 3 consecutive refresh failures, redirect to LoginPage with expired_session message instead of retrying. |
| Frontend build pipeline incompatible with AuthProvider token-in-memory pattern | Low | Medium | Validate AuthProvider pattern in isolated POC during M3; ensure SSR/hydration compatibility if applicable. |

---

### M6: Phased Rollout, Monitoring Validation, and General Availability

**Objective:** Execute the three-phase rollout strategy (Internal Alpha, 10% Beta, 100% GA), validate all monitoring and runbooks, remove feature flags, and achieve 99.9% uptime over 7 days in production.

**Scope:**

- In: Feature flag deployment (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH); Phase 1 Internal Alpha (1 week — auth-team + QA); Phase 2 Beta at 10% traffic (2 weeks — monitoring latency, error rates, Redis usage); Phase 3 GA at 100% (1 week); rollback procedure validation; runbook review; on-call rotation setup (24/7 for first 2 weeks post-GA); feature flag removal; capacity validation (3 AuthService replicas, 100 PostgreSQL connections, 1 GB Redis); success metrics baseline measurement.
- Out: New feature development (post-GA backlog).

**Deliverables:**

| ID | Deliverable | Traceability |
|----|-------------|--------------|
| D6.1 | Feature flags AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH deployed to production (default OFF); flag toggle documented in runbook | TDD Section 19.2 feature flag table |
| D6.2 | Phase 1 Internal Alpha: AUTH_NEW_LOGIN ON for auth-team and QA; all FR-AUTH-001 through FR-AUTH-005 pass manual testing against staging; zero P0/P1 bugs | TDD Section 19.1 Phase 1 criteria |
| D6.3 | Phase 2 Beta (10%): AUTH_NEW_LOGIN ON for 10% of traffic; monitor p95 latency <200ms, error rate <0.1%, zero TokenManager Redis connection failures over 2 weeks | TDD Section 19.1 Phase 2 criteria |
| D6.4 | Phase 3 GA (100%): AUTH_NEW_LOGIN ON for all traffic; legacy auth endpoints deprecated; AUTH_TOKEN_REFRESH enabled; validate 99.9% uptime over first 7 days | TDD Section 19.1 Phase 3 criteria |
| D6.5 | Rollback procedure tested in staging: disable AUTH_NEW_LOGIN -> verify legacy flow operational -> smoke test -> document elapsed time | TDD Section 19.3 rollback procedure steps 1-6 |
| D6.6 | Runbook published and reviewed: AuthService down scenario (pod restart, PostgreSQL failover, Redis-down graceful degradation); token refresh failure scenario; escalation path (auth-team on-call -> test-lead -> eng-manager -> platform-team) | TDD Section 25.1 runbook; TDD Section 25.2 on-call expectations |
| D6.7 | Success metrics dashboard live: registration conversion (>60%), login p95 (<200ms), session duration (>30 min), failed login rate (<5%), password reset completion (>80%) | PRD Success Metrics table |
| D6.8 | Capacity validation report: 3 AuthService replicas handling 500 concurrent users; PostgreSQL connection pool at 100 with <50ms wait; Redis at <50 MB of 1 GB with <10ms latency; HPA scales to 10 replicas at CPU >70% | TDD Section 25.3 capacity planning |
| D6.9 | SOC2 audit evidence package: audit log sample covering all event types; retention policy documentation; access control documentation; incident response runbook; consent recording evidence | PRD Legal/Compliance — SOC2 Type II; Q3 2026 audit deadline |

**Acceptance Criteria:**

1. Phase 1 Internal Alpha: all FR-AUTH-001 through FR-AUTH-005 pass; zero P0/P1 bugs (TDD Section 19.1).
2. Phase 2 Beta: p95 latency <200ms sustained over 2 weeks; error rate <0.1%; no Redis connection failures; rollback not triggered (TDD Section 19.1).
3. Phase 3 GA: 99.9% uptime over first 7 days; all monitoring dashboards green; feature flags AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH removed from configuration (TDD Section 19.1).
4. Rollback procedure tested end-to-end in staging; completed in under 15 minutes from flag toggle to legacy flow confirmation (TDD Section 19.4 rollback criteria: latency >1000ms for 5 min, error rate >5% for 2 min, Redis failures >10/min, data corruption).
5. Runbook reviewed and signed off by auth-team on-call engineer; escalation path validated.
6. Success metrics baselined: registration conversion measured, login p95 confirmed <200ms under real traffic, session duration tracked.
7. SOC2 audit evidence package compiled and reviewed by compliance team before Q3 audit.
8. On-call rotation active 24/7 for first 2 weeks post-GA; acknowledgment time <15 minutes for P1 alerts (TDD Section 25.2).
9. Feature flags removed from codebase; legacy auth endpoints marked deprecated with removal timeline.

**Dependencies:**

- M1-M5 all complete.
- External: Production Kubernetes cluster configured; monitoring infrastructure (Grafana, Prometheus, alerting) deployed; compliance team available for evidence review.

**Estimated Duration:** 4 weeks (1 week Alpha + 2 weeks Beta + 1 week GA stabilization).

**Risks and Mitigations:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Beta reveals performance regression not caught in load testing | Medium | High | Maintain legacy auth as fallback throughout beta; rollback criteria defined in TDD Section 19.4; extend beta by 1 week if p95 exceeds 200ms. |
| Legacy auth system already deprecated or removed, leaving no rollback path | Low | Critical | Verify legacy auth is operational and tested before Phase 1 begins; if legacy is already gone, Phase 1 Internal Alpha becomes the rollback validation point. |
| SOC2 evidence package incomplete at audit time | Medium | Critical | Begin evidence collection from M1 (audit_log operational); review evidence completeness at each milestone gate; engage compliance team at M4 for pre-review. |
| 10% beta traffic insufficient to surface concurrency issues that appear at 100% | Medium | Medium | Supplement beta traffic with synthetic load during beta window; push to 25% if first week shows no issues; have capacity to scale AuthService replicas from 3 to 10 via HPA. |

---

## Cross-Cutting Concerns

### Security

- **Password storage:** bcrypt cost 12 via PasswordHasher; raw passwords never persisted or logged (PRD NFR-AUTH.3; TDD NFR-SEC-001). Verified in M1, enforced in M2.
- **Token signing:** RS256 with 2048-bit RSA keys; quarterly rotation schedule documented (TDD NFR-SEC-002). Implemented in M2, key rotation documented in M5 security review.
- **User enumeration prevention:** All authentication failure paths (wrong email, wrong password, locked account) return identical response bodies and timing (PRD Error Handling table; TDD Section 12). Validated in M2.
- **Account lockout:** 5 failed attempts within 15 minutes triggers 423 Locked (TDD FR-AUTH-001 AC item 4). Implemented in M2, lockout threshold configurable.
- **Token storage in frontend:** AuthToken stored in memory only, not localStorage; cleared on tab close (TDD R-001 mitigation). Enforced in M5.
- **CORS:** Restricted to known frontend origins (TDD Section 13). Configured at API Gateway, validated in M5 security review.
- **TLS 1.3:** Enforced on all endpoints (TDD Section 13). Validated in M5 penetration test.
- **Penetration testing:** Pre-production security review with OWASP ASVS L2 checklist plus manual testing (PRD Risk Analysis). Executed in M5.

### Observability

- **Metrics (Prometheus):** auth_login_total (counter), auth_login_duration_seconds (histogram), auth_token_refresh_total (counter), auth_registration_total (counter) (TDD Section 14). Scaffolded in M1, populated per endpoint in M2-M4.
- **Structured logging:** All auth events logged as JSON with user_id, event_type, timestamp, ip_address, outcome (TDD Section 14). Audit emitter built in M1.
- **Distributed tracing:** OpenTelemetry spans covering AuthService, PasswordHasher, TokenManager, JwtService request lifecycle (TDD Section 14). Instrumented in M2-M3.
- **Alerting:** Login failure rate >20% over 5 minutes; p95 latency >500ms; TokenManager Redis connection failures; email bounce rate >5% (TDD Section 14; M4). Configured in M6 with runbook links.
- **Dashboards:** Grafana dashboards for auth health; success metrics funnel dashboard (registration conversion, session duration, failed login rate) (TDD Section 24.2). Live in M6.

### Testing

- **Unit (80% coverage target):** AuthService methods, PasswordHasher, JwtService sign/verify, TokenManager lifecycle, UserProfile validation. Jest + ts-jest (TDD Section 15.1). Enforced from M2 onward via CI coverage gate.
- **Integration (15%):** API endpoint request/response cycles; database operations; Redis token storage; end-to-end through AuthService -> PasswordHasher -> database. Supertest + testcontainers (TDD Section 15.1). Each milestone adds integration tests for new endpoints.
- **E2E (5%):** Full user journeys through LoginPage, RegisterPage, AuthProvider. Playwright (TDD Section 15.1). Comprehensive suite in M5.
- **Load testing:** k6 scripts validating 500 concurrent users; p95 <200ms for all auth endpoints; p95 <100ms for token refresh (TDD NFR-PERF-001/002). First load test in M3 (token refresh), comprehensive in M5.

### Compliance (SOC2 Type II)

- **Audit logging:** All auth events recorded from M1 with user_id, event_type, timestamp, IP, outcome; 12-month retention (PRD Legal/Compliance). Audit log schema and emitter in M1.
- **Evidence collection:** Begin from M1; compile into audit evidence package at M6; engage compliance team at M4 for pre-review (Q3 2026 audit deadline).
- **Consent recording:** GDPR consent at registration with timestamp and consent text version (PRD Legal/Compliance). Implemented in M4.
- **Data minimization:** Only email, hashed password, and display name collected (PRD Legal/Compliance). Enforced in schema design (M1) and API validation (M2).
- **Password policy:** NIST SP 800-63B compliance; one-way adaptive hashing; no plaintext storage or logging (PRD Legal/Compliance). Implemented via PasswordHasher (M1).

### Performance Budgets

| Endpoint | p95 Target | Load Condition | Measurement |
|----------|-----------|----------------|-------------|
| POST /auth/login | <200ms | 500 concurrent | APM + k6 load test (TDD NFR-PERF-001/002) |
| POST /auth/register | <200ms | 500 concurrent | APM + k6 load test |
| GET /auth/me | <200ms | 500 concurrent | APM + k6 load test |
| POST /auth/refresh | <100ms | 500 concurrent | APM + k6 load test (TDD Section 4.1) |
| PasswordHasher.hash() | <500ms | Single operation | Benchmark in CI (TDD Section 17) |
| JwtService sign/verify | <5ms | Single operation | Unit test benchmark (TDD Section 17) |
| TokenManager Redis ops | <10ms | Single operation | Redis latency monitoring (TDD Section 17) |

---

## Risk Register

| ID | Risk | Probability | Impact | Mitigation | Owner | Traceability |
|----|------|-------------|--------|------------|-------|--------------|
| RR-1 | Low registration adoption due to poor UX; conversion falls below 60% target | Medium | High | Usability testing during M5 E2E validation; iterate on LoginPage/RegisterPage based on funnel analytics; A/B test form field order and validation messaging. | Product + Frontend | PRD Risk Analysis — "Low registration adoption" |
| RR-2 | Security breach from implementation flaw (token theft, XSS, injection) | Low | Critical | Defense-in-depth: memory-only token storage, short access token TTL (15 min), bcrypt cost 12, RS256 signing, CORS restrictions; dedicated pen test in M5; no P0 security findings allowed for GA gate. | Security + Auth-team | PRD Risk Analysis — "Security breach"; TDD R-001 (XSS token theft) |
| RR-3 | SOC2 compliance failure from incomplete audit logging | Medium | High | Audit logging built from M1; audit_log schema covers all event types; 12-month retention enforced; evidence package compiled incrementally; compliance team pre-review at M4. | Compliance + Auth-team | PRD Risk Analysis — "Compliance failure" |
| RR-4 | Email delivery failures block password reset flow | Low | Medium | Async email dispatch (does not block API response); delivery monitoring with >5% bounce rate alerting; queue depth monitoring; documented fallback support channel for manual reset during outages. | Auth-team + Infra | PRD Risk Analysis — "Email delivery failures"; PRD Dependencies — SendGrid |
| RR-5 | Redis unavailability causes mass session invalidation or refresh failures | Medium | High | Redis deployed in sentinel/cluster mode; graceful degradation (reject refresh, force re-login rather than serve stale tokens); alerting on Redis connection failures; runbook for Redis failover. | Platform + Auth-team | TDD R-003 (data loss during migration); TDD Section 12 — Redis fallback |
| RR-6 | Concurrent token refresh race condition (two tabs, one user) | Medium | Medium | Redis optimistic locking (WATCH/MULTI) on refresh token keys; first refresh wins, second gets 401 and re-authenticates; documented as expected behavior. | Auth-team | TDD Section 12 — edge cases |
| RR-7 | bcrypt cost 12 exceeds 500ms budget on production hardware | Low | Medium | Profile on CI runners and production-equivalent staging in M1; if over budget, negotiate cost 11 with security team per SEC-POLICY-001; PasswordHasher abstraction allows cost factor change without touching call sites. | Auth-team | TDD Section 17 — performance budgets |
| RR-8 | Rollback to legacy auth fails during beta emergency | Low | Critical | Validate legacy auth operational before Phase 1; test rollback in staging before beta; run rollback drill during Internal Alpha; document rollback time budget (<15 minutes). | Auth-team + Platform | TDD Section 19.3 rollback procedure |

---

## Definition of Done

### Per Milestone

1. All deliverables for the milestone are implemented and code-reviewed.
2. All acceptance criteria for the milestone pass with automated test evidence.
3. Unit test coverage for new code exceeds 80%.
4. Integration tests for new endpoints pass against real PostgreSQL and Redis.
5. Audit log events for all new state transitions are emitted and verified.
6. No P0 or P1 bugs open against the milestone scope.
7. Performance targets for new endpoints validated (p95 <200ms under load).

### Overall (Release Gate)

1. All functional requirements FR-AUTH-001 through FR-AUTH-005 implemented and verified with passing tests (TDD Section 24.1).
2. Unit test coverage for AuthService, TokenManager, JwtService, and PasswordHasher exceeds 80% (TDD Section 24.1).
3. Integration tests for all API endpoints pass against real PostgreSQL and Redis instances (TDD Section 24.1).
4. Security review completed: PasswordHasher bcrypt cost verified, JwtService RS256 key rotation documented, pen test report shows zero critical findings (TDD Section 24.1).
5. Performance testing confirms all endpoints meet <200ms p95 latency under 500 concurrent users (TDD Section 24.1).
6. E2E tests (Playwright) cover all 6 user journey scenarios and pass against staging (TDD Section 15.2).
7. Runbooks reviewed and published; on-call rotation established (TDD Section 24.2).
8. Monitoring dashboards verified: auth_login_total, auth_login_duration_seconds, auth_token_refresh_total (TDD Section 24.2).
9. Rollback procedure tested in staging (TDD Section 24.2).
10. 99.9% uptime sustained over 7 days in production (TDD Section 19.1 Phase 3 criteria).
11. SOC2 audit evidence package compiled and reviewed by compliance (Q3 2026 audit readiness).

---

## Open Questions and Assumptions

### Open Questions (from PRD and TDD)

| ID | Question | Owner | Target Resolution | Impact on Roadmap |
|----|----------|-------|-------------------|-------------------|
| OQ-PRD-1 | Should password reset emails be sent synchronously or asynchronously? (PRD Open Questions #1) | Engineering | Before M4 | Architecture decision: async queue recommended (non-blocking API response, delivery monitoring). Assumed async in D4.9. |
| OQ-PRD-2 | Maximum number of refresh tokens allowed per user across devices? (PRD Open Questions #2) | Product | Before M3 | Affects Redis storage and TokenManager design. Assumed unlimited in v1.0 (multi-device expected per PRD Error Handling). If capped, add oldest-token eviction to M3 scope. |
| OQ-PRD-3 | Account lockout policy: auto-unlock after window, or admin-only? (PRD Open Questions #3) | Security | Before M2 | Affects D2.1 lockout implementation. Assumed auto-unlock after 15-minute window with admin notification. If admin-only, add admin unlock API to M4 scope. |
| OQ-PRD-4 | Should "remember me" extend session beyond 7 days? (PRD Open Questions #4) | Product | Before M5 | Affects AuthProvider token handling. Assumed no for v1.0 (7-day max per TDD spec). If yes, add extended TTL option to TokenManager in M3. |
| OQ-TDD-1 | Should AuthService support API key authentication for service-to-service calls? (TDD OQ-001) | test-lead | Deferred to v1.1 | No v1.0 impact. Noted for future RBAC design. |
| OQ-TDD-2 | Maximum allowed UserProfile roles array length? (TDD OQ-002) | auth-team | Before M2 | Affects D1.1 schema. Assumed no explicit limit in v1.0 (roles enforcement is out of scope per TDD NG-003). |

### Assumptions

1. PostgreSQL 15+ is provisioned and accessible before M1 begins (PRD Assumptions).
2. Redis 7+ is provisioned and accessible before M1 begins (TDD Dependencies).
3. SendGrid API credentials and approved sender domain are configured before M4 (PRD Dependencies).
4. Frontend routing framework supports client-side token-based authentication (PRD Assumptions).
5. Security policy SEC-POLICY-001 defines password and token parameters before M2 (PRD Dependencies).
6. Node.js 20 LTS is the runtime environment (TDD Dependencies).
7. No legacy user data to migrate (greenfield deployment); if migration is needed, add a dedicated pre-M1 data migration workstream.
8. Email/password only in v1.0; no OAuth, social login, or MFA (PRD Scope — Out of Scope).
9. The API Gateway supports per-IP and per-user rate limiting configuration (TDD Section 8.1 rate limits).
10. Production Kubernetes cluster supports horizontal pod autoscaling (HPA) for AuthService (TDD Section 25.3).
