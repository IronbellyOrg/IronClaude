# User Authentication System — Implementation Roadmap

**Generated**: 2026-05-22
**Source Spec**: `/tests/sc-roadmap/fixtures/sample_spec.md` — User Authentication System v1.0
**Status**: Draft for adversarial comparison
**Target Stack**: Python 3.11+, PostgreSQL 15, Redis 7, Docker 24+

---

## Executive Summary

This roadmap delivers a production-grade user authentication system with OAuth2 social login (Google, GitHub), JWT-based session management, role-based access control, and two-factor authentication. The system targets 10,000 concurrent sessions at sub-200ms API response times, with OWASP Top 10 and GDPR compliance verified by automated testing and third-party audit.

The implementation is organized into five milestones spanning 14 weeks. Milestone 1 (weeks 1–3) establishes the core registration, login, JWT issuance, and refresh-token session layer on PostgreSQL 15 and Redis 7. Milestone 2 (weeks 4–6) adds OAuth2 provider integration, TOTP-based 2FA, and per-user rate limiting. Milestone 3 (weeks 7–8) introduces RBAC enforcement, audit logging, and user profile management. Milestone 4 (weeks 9–10) delivers the admin dashboard and account deactivation workflow. Milestone 5 (weeks 11–14) focuses on production hardening: load testing at 10K sessions, OWASP/GDPR compliance verification, and 99.9% uptime infrastructure.

Every requirement FR-001 through FR-012 and NFR-001 through NFR-006 is mapped to a specific milestone with concrete deliverables and measurable acceptance criteria. All four spec-identified risks (R-001 through R-004) are addressed with milestone-scoped mitigations.

---

## Milestones

### M1 — Core Authentication Infrastructure (Weeks 1–3)

**Goal**: Deliver the foundational user registration, login, JWT token lifecycle, and session management subsystem. This milestone produces the data model, API surface, and token infrastructure that all subsequent milestones depend on.

**Requirements covered**: FR-001, FR-002, FR-005, FR-006, NFR-001, NFR-006

**Dependencies**: None (first milestone).

#### Deliverables

| ID | Deliverable | Description |
|----|------------|-------------|
| D1.1 | User data model | PostgreSQL 15 schema: `users` table with columns `id` (UUID v4 PK), `email` (unique, not null), `password_hash` (bcrypt, cost factor 12), `email_verified` (boolean, default false), `created_at`, `updated_at`. Migration managed by Alembic. |
| D1.2 | Registration API | `POST /api/v1/auth/register` — accepts email + password. Validates password strength (min 12 chars, 1 uppercase, 1 digit, 1 special). Stores bcrypt hash. Triggers SendGrid verification email with expiring token (TTL 15 minutes). Returns HTTP 201 on success, HTTP 409 on duplicate email, HTTP 422 on validation failure. |
| D1.3 | Email verification endpoint | `GET /api/v1/auth/verify-email?token=<jwt>` — validates JWT-signed verification token. Sets `email_verified = true`. Returns HTTP 200 with confirmation payload. Token reuse returns HTTP 410. |
| D1.4 | Login API | `POST /api/v1/auth/login` — accepts email + password. Verifies bcrypt hash (constant-time comparison). Issues access JWT (RS256, 15-minute TTL) and refresh token (opaque, 7-day TTL, stored in Redis 7). Returns HTTP 200 with token pair. Failed attempt increments Redis counter keyed by `auth:fail:{email}` (TTL 15 min). Returns HTTP 401 on mismatch, HTTP 403 if email not verified. |
| D1.5 | Token refresh endpoint | `POST /api/v1/auth/refresh` — accepts refresh token, validates against Redis store, rotates refresh token (old deleted, new issued), issues new access JWT. Returns HTTP 200 with new token pair. Invalid/expired refresh token returns HTTP 401. |
| D1.6 | Password reset flow | `POST /api/v1/auth/forgot-password` triggers SendGrid email with JWT-signed reset token (TTL 30 minutes). `POST /api/v1/auth/reset-password` accepts token + new password, validates strength rules, updates bcrypt hash, invalidates all existing refresh tokens for that user. |
| D1.7 | PII encryption layer | AES-256-GCM encryption for email and profile fields at rest, using a key managed via environment-injected secret (e.g., AWS KMS or HashiCorp Vault). All API responses decrypt on read. All database writes encrypt before persist. TLS 1.3 enforced on all connections (NFR-006). |
| D1.8 | API response time baseline | Configure FastAPI middleware with `X-Response-Time` headers. Target: all auth endpoints return within 200ms p99 (NFR-001). Instrument with Prometheus histogram buckets at 50ms, 100ms, 200ms, 500ms. |

#### Acceptance Criteria

- Registration + email verification + login end-to-end flow passes automated test (happy path) in under 5 seconds.
- Refresh token rotation works: old token is rejected after rotation, new token is accepted.
- Password reset flow completes successfully; old refresh tokens are revoked.
- All auth endpoints respond in < 200ms p99 under 100 concurrent requests (k6 load test).
- Email and profile data are unreadable via direct SQL `SELECT` without decryption function.
- Unit test coverage >= 90% for auth service module.

**Estimated duration**: 3 weeks.

---

### M2 — OAuth2 Integration and Enhanced Security (Weeks 4–6)

**Goal**: Add third-party OAuth2 login via Google and GitHub, implement TOTP-based two-factor authentication, and enforce per-user API rate limiting. This milestone hardens the auth surface against the two highest-probability risks (R-001, R-002).

**Requirements covered**: FR-003, FR-007, FR-008, NFR-003 (partial), R-001, R-002

**Dependencies**: M1 (user model, JWT infrastructure, session store).

#### Deliverables

| ID | Deliverable | Description |
|----|------------|-------------|
| D2.1 | Google OAuth2 provider | `GET /api/v1/auth/oauth/google` redirects to Google consent screen (scope: `openid email profile`). Callback `GET /api/v1/auth/oauth/google/callback` exchanges authorization code for Google ID token, validates `iss`, `aud`, `exp` claims, upserts user record (email from Google `email` claim, `email_verified = true`), issues JWT access + refresh token pair. Uses `google-auth` library v2.x. |
| D2.2 | GitHub OAuth2 provider | `GET /api/v1/auth/oauth/github` redirects to GitHub authorize endpoint (scope: `user:email`). Callback `GET /api/v1/auth/oauth/github/callback` exchanges code for GitHub access token via `POST https://github.com/login/oauth/access_token`, fetches user profile from `GET https://api.github.com/user`, upserts user, issues JWT pair. Falls back to email/password if GitHub API returns HTTP 5xx (R-003 mitigation). |
| D2.3 | OAuth account linking | `POST /api/v1/auth/oauth/link` — authenticated endpoint that links an additional OAuth provider to an existing account. Prevents duplicate linking. Stores `oauth_providers` table with columns `user_id`, `provider` (enum: google, github), `provider_user_id`. |
| D2.4 | TOTP two-factor authentication | `POST /api/v1/auth/2fa/enable` generates QR code (RFC 6238 TOTP, SHA-1, 30-second step, 6-digit code) using `pyotp` library v2.x. User verifies enrollment by submitting a valid code. `POST /api/v1/auth/login` flow modified: if 2FA enabled, login returns HTTP 202 with a `2fa_required` flag and a short-lived challenge token (5-minute TTL). Client submits code to `POST /api/v1/auth/2fa/verify` which validates TOTP within +/- 1 time step. |
| D2.5 | 2FA recovery codes | On 2FA enrollment, generate 10 single-use recovery codes (8-character alphanumeric, cryptographically random). Store bcrypt-hashed codes in `recovery_codes` table. `POST /api/v1/auth/2fa/recover` accepts a recovery code, invalidates it, issues tokens. |
| D2.6 | Per-user rate limiting | Redis-backed sliding window rate limiter. Default: 100 requests/minute per user for general API, 5 requests/minute for login endpoint, 3 requests/minute for password reset. `POST /api/v1/auth/login` lockout after 10 consecutive failures within 15 minutes (R-002 mitigation). Uses `fastapi-limiter` with Redis backend. Returns HTTP 429 with `Retry-After` header. |
| D2.7 | XSS and CSP hardening | JWT stored in HTTP-only, Secure, SameSite=Strict cookies (not localStorage) (R-001 mitigation). Content-Security-Policy header set to `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'`. X-Content-Type-Options: nosniff. X-Frame-Options: DENY. |

#### Acceptance Criteria

- Google OAuth2 login completes end-to-end: consent screen -> callback -> JWT issued -> authenticated API call succeeds.
- GitHub OAuth2 login completes end-to-end with the same flow.
- GitHub OAuth2 gracefully falls back to email/password form when GitHub returns HTTP 5xx.
- TOTP 2FA enrollment and verification work with Google Authenticator and Authy apps.
- Recovery code consumption works; reused recovery code is rejected.
- Login rate limiter blocks the 11th failed attempt within 15 minutes and returns HTTP 429.
- JWT is not accessible via `document.cookie` in browser JavaScript (HTTP-only verification).
- CSP header present on all responses; no inline script execution possible.
- Unit + integration test coverage >= 85% for new modules.

**Estimated duration**: 3 weeks.

---

### M3 — RBAC, Audit Logging, and User Profiles (Weeks 7–8)

**Goal**: Implement role-based access control with three roles (admin, user, suspended), structured audit logging for all auth events, and user profile CRUD. This milestone delivers the authorization layer and compliance-ready audit trail.

**Requirements covered**: FR-004, FR-009, FR-010, NFR-004, NFR-006

**Dependencies**: M1 (user model, JWT), M2 (2FA, rate limiting).

#### Deliverables

| ID | Deliverable | Description |
|----|------------|-------------|
| D3.1 | Role and permission model | `roles` table: `id`, `name` (enum: `admin`, `user`, `suspended`), `description`. `permissions` table: `id`, `name`, `resource`, `action`. `role_permissions` join table. Default role on registration: `user`. JWT access token includes `role` claim. Middleware on every protected endpoint checks `role` against required permission. |
| D3.2 | RBAC enforcement middleware | FastAPI dependency `require_permission(permission_name)` that extracts JWT `role` claim, queries cached role-permission mapping (Redis, TTL 5 minutes), returns HTTP 403 if permission absent. Admin-only endpoints guarded with `require_permission("admin:access")`. Suspended users blocked from all authenticated endpoints. |
| D3.3 | Role management API | `GET /api/v1/admin/roles` (admin only) — list roles and permissions. `PUT /api/v1/admin/users/{id}/role` (admin only) — change user role. Returns HTTP 200. Role change invalidates user's active JWT (via Redis token blacklist with remaining TTL). |
| D3.4 | Audit logging service | Structured JSON logs for every auth event: registration, login (success/failure), logout, token refresh, password reset request, password reset completion, 2FA enable/disable, OAuth link/unlink, role change, account deactivation. Log schema: `{"timestamp": "ISO-8601", "event_type": "string", "user_id": "UUID", "ip_address": "string", "user_agent": "string", "metadata": {}}`. Written to PostgreSQL `audit_logs` table (append-only, no UPDATE/DELETE grants) and streamed to stdout for external log aggregation (ELK / CloudWatch). |
| D3.5 | Audit log query API | `GET /api/v1/admin/audit-logs` (admin only) — paginated, filterable by `event_type`, `user_id`, date range. Returns HTTP 200 with `{results: [], total: int, page: int, per_page: int}`. Default page size 50, max 200. |
| D3.6 | User profile CRUD | `GET /api/v1/users/me` — returns profile (email, display_name, avatar_url, created_at, 2fa_enabled). `PUT /api/v1/users/me` — updates mutable fields (display_name, avatar_url). `PUT /api/v1/users/me/email` — triggers email verification flow for new email; old email remains active until verified. `PUT /api/v1/users/me/password` — requires current password confirmation, applies strength rules, revokes all refresh tokens. |
| D3.7 | GDPR data export | `POST /api/v1/users/me/export` — creates a JSON archive of all user data (profile, auth events, OAuth providers, audit log entries) within 72 hours. Sends download link via SendGrid. Implements right-of-access under GDPR Article 15 (NFR-004). |
| D3.8 | GDPR account deletion request | `POST /api/v1/users/me/delete-request` — flags account for deletion. Executes soft delete after 30-day retention period (GDPR right to erasure, Article 17). Hard delete removes PII, retains anonymized audit records. |

#### Acceptance Criteria

- Three roles (admin, user, suspended) enforce correct access: admin can access all endpoints, user cannot access admin endpoints, suspended user is blocked from all authenticated endpoints.
- Changing a user's role immediately invalidates their active sessions.
- Every auth event (login, logout, password change, 2FA toggle, role change, OAuth link) produces an audit log entry queryable via the admin API.
- Audit log table has no UPDATE or DELETE grants verified by CI migration test.
- User profile update and password change flows work end-to-end.
- GDPR export produces a valid JSON file containing profile, auth events, and OAuth provider data.
- Unit + integration test coverage >= 85% for new modules.

**Estimated duration**: 2 weeks.

---

### M4 — Admin Dashboard and Account Lifecycle (Weeks 9–10)

**Goal**: Build the admin dashboard for user management and the account deactivation workflow. This milestone completes the remaining functional requirements and provides operators with visibility and control over the user base.

**Requirements covered**: FR-011, FR-012, NFR-004 (admin data handling)

**Dependencies**: M1 (user model), M2 (2FA, rate limiting), M3 (RBAC, audit logging).

#### Deliverables

| ID | Deliverable | Description |
|----|------------|-------------|
| D4.1 | Admin user list view | `GET /api/v1/admin/users` — paginated list of all users with columns: email, role, 2fa_status, created_at, last_login, status (active/suspended/deactivated). Filterable by role, status, date range. Sortable by any column. Page size 50, max 200. |
| D4.2 | Admin user detail view | `GET /api/v1/admin/users/{id}` — full user detail including auth history summary (login count last 30 days, failed login count, last password change), linked OAuth providers, active sessions count. |
| D4.3 | Admin user actions | `PUT /api/v1/admin/users/{id}/suspend` — sets role to `suspended`, revokes all tokens. `PUT /api/v1/admin/users/{id}/reactivate` — restores previous role. `DELETE /api/v1/admin/users/{id}` — schedules hard deletion per GDPR retention policy (30-day delay). All actions produce audit log entries with admin user ID. |
| D4.4 | Session management admin view | `GET /api/v1/admin/users/{id}/sessions` — list active refresh tokens for a user (device info, IP, created_at, last_used). `DELETE /api/v1/admin/users/{id}/sessions/{session_id}` — revoke individual session. |
| D4.5 | Admin dashboard frontend | Single-page React 18 application (TypeScript) served from `/admin/`. Three views: User List, User Detail, Audit Log Viewer. Authentication via admin JWT. Uses TanStack Table for sortable/filterable data grids. Responsive layout, tested on Chrome 120+ and Firefox 121+. |
| D4.6 | Account self-deactivation workflow | `POST /api/v1/users/me/deactivate` — requires password confirmation. Sets user status to `deactivated`, revokes all tokens, disables 2FA. User receives confirmation email via SendGrid. Deactivated accounts cannot log in (returns HTTP 403 with message "Account deactivated"). |
| D4.7 | Account reactivation flow | `POST /api/v1/auth/reactivate` — accepts email + password. If account is within 30-day deactivation window, reactivates and sends confirmation email. After 30 days, reactivation is denied and account enters GDPR deletion queue. |

#### Acceptance Criteria

- Admin user list loads in < 500ms with 50,000 user records (pagination query performance verified with `EXPLAIN ANALYZE`).
- Admin suspend/reactivate/delete actions complete and produce audit entries viewable in the audit log API.
- Session revocation by admin immediately invalidates the targeted refresh token.
- Dashboard renders correctly on Chrome 120+ and Firefox 121+ at 1280px and 1920px widths.
- Account deactivation prevents login and revokes all sessions.
- Account reactivation succeeds within 30-day window and fails after.
- All admin actions are audit-logged with the acting admin's user ID.

**Estimated duration**: 2 weeks.

---

### M5 — Production Hardening and Compliance Verification (Weeks 11–14)

**Goal**: Validate all non-functional requirements at production scale: load test 10,000 concurrent sessions, complete OWASP Top 10 security scan, verify GDPR compliance, and confirm 99.9% uptime architecture. This milestone converts the system from "feature complete" to "production ready."

**Requirements covered**: NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-006, R-001, R-002, R-003, R-004

**Dependencies**: M1, M2, M3, M4 (all functional requirements complete).

#### Deliverables

| ID | Deliverable | Description |
|----|------------|-------------|
| D5.1 | Load testing suite | k6 test scripts simulating: (a) 10,000 concurrent logins over 5 minutes, (b) sustained 10,000 active sessions with periodic token refresh, (c) burst of 500 registrations/minute. Assert: p99 response time < 200ms for login, < 100ms for token refresh. Assert: zero HTTP 5xx errors. |
| D5.2 | Database optimization | PostgreSQL connection pooling via PgBouncer (max 100 connections). Indexes on `users.email` (unique btree), `audit_logs.created_at` (btree), `audit_logs.user_id` (btree), `refresh_tokens.user_id` (btree). Query plans verified with `EXPLAIN ANALYZE` for all frequently-used queries — all must use index scans, not sequential scans. |
| D5.3 | Redis session optimization | Redis configured with `maxmemory-policy allkeys-lru`, max memory 4GB. Refresh tokens stored with TTL matching expiry. Session keys use `session:{user_id}:{token_id}` pattern. |
| D5.4 | OWASP Top 10 security scan | Run OWASP ZAP v2.15 automated scan against full API surface. Manual penetration test for: SQL injection on all input fields, XSS on all reflected output, CSRF on state-changing endpoints, broken access control (vertical and horizontal privilege escalation). Remediate all findings classified Medium or above. |
| D5.5 | GDPR compliance verification | Verify: (a) data export produces complete user data within 72 hours, (b) deletion removes all PII within 30 days, (c) consent records are stored for email verification, (d) data processing activities are documented in a register, (e) privacy policy endpoint `GET /api/v1/privacy-policy` returns current policy. |
| D5.6 | High availability infrastructure | Docker Compose configuration with: 2 FastAPI app replicas behind nginx load balancer, PostgreSQL with streaming replication (1 primary + 1 hot standby), Redis Sentinel for automatic failover, health check endpoints `GET /health` returning HTTP 200 with `{"status": "healthy", "db": "ok", "redis": "ok"}`. Target: 99.9% uptime (max 8.76 hours downtime/year). |
| D5.7 | Monitoring and alerting | Prometheus metrics: request latency histograms, error rate counters, active session gauge, database connection pool utilization. Grafana dashboard with panels for p50/p95/p99 latency, requests/second, error rate, active sessions. Alerts: p99 latency > 200ms for 5 minutes, error rate > 1% for 2 minutes, active sessions approaching Redis memory limit, database replication lag > 5 seconds. |
| D5.8 | Incident response runbook | Documented procedures for: OAuth provider outage (fallback flow activation), Redis failover (Sentinel promotion verification), database failover (application reconnection), token key rotation (RS256 key pair rotation without session invalidation). |

#### Acceptance Criteria

- k6 load test passes: 10,000 concurrent sessions sustained for 5 minutes with p99 < 200ms and zero 5xx errors (NFR-001, NFR-002).
- OWASP ZAP scan reports zero Medium/High/Critical findings (NFR-003).
- Manual pentest report confirms no SQL injection, XSS, CSRF, or access control vulnerabilities.
- GDPR export and deletion flows verified by compliance checklist (NFR-004).
- Docker Compose HA setup survives kill of one app replica, one Redis node, with zero dropped requests (NFR-005).
- All PII encrypted at rest (AES-256-GCM) and in transit (TLS 1.3) verified by network capture and database inspection (NFR-006).
- Grafana dashboards render live metrics; all four alert thresholds trigger correctly under simulated failure.

**Estimated duration**: 4 weeks.

---

## Cross-Cutting Concerns

### Security

- **Authentication**: RS256 JWT with 2048-bit RSA key pair, 15-minute access token TTL, 7-day refresh token TTL with rotation on every refresh.
- **Password storage**: bcrypt with cost factor 12 (targets ~250ms hash time on current hardware).
- **Transport**: TLS 1.3 enforced; HSTS header with 1-year max-age and includeSubDomains.
- **Token storage (client)**: HTTP-only, Secure, SameSite=Strict cookies. No localStorage or sessionStorage for tokens (R-001 mitigation).
- **Headers**: CSP, X-Content-Type-Options, X-Frame-Options on every response.
- **Rate limiting**: Redis sliding window — 5 req/min login, 3 req/min password reset, 100 req/min general API (R-002 mitigation).
- **Key management**: RSA signing key and AES encryption key injected from environment; never committed to source control. Rotation procedure documented in D5.8.
- **Dependency scanning**: `pip-audit` and `safety` run in CI on every push; vulnerabilities rated >= 7.0 CVSS block merge.

### Observability

- **Structured logging**: JSON format to stdout, captured by Docker logging driver. Fields: timestamp, level, event_type, user_id, request_id, duration_ms.
- **Distributed tracing**: OpenTelemetry traces propagated via `traceparent` header. Span for each HTTP request and database query.
- **Metrics**: Prometheus exposition at `/metrics`. Key metrics: `auth_requests_total` (counter by endpoint/status), `auth_request_duration_seconds` (histogram), `active_sessions` (gauge), `auth_errors_total` (counter by type).
- **Health checks**: `/health` endpoint checks PostgreSQL connectivity, Redis connectivity, and returns component status.

### Testing Strategy

| Layer | Tool | Coverage Target | Frequency |
|-------|------|-----------------|-----------|
| Unit tests | pytest + pytest-cov | >= 90% line coverage for `auth/`, `rbac/`, `audit/` modules | Every commit (CI) |
| Integration tests | pytest + httpx TestClient | All API endpoints tested for happy path + error cases | Every commit (CI) |
| Contract tests | Schemathesis | API contract conformance against OpenAPI 3.1 spec | Every PR (CI) |
| Load tests | k6 | 10K concurrent sessions, p99 < 200ms | Nightly + pre-release |
| Security tests | OWASP ZAP + manual pentest | Zero Medium+ findings | Pre-release |
| E2E tests | Playwright | OAuth2 login flow (Google, GitHub), 2FA enrollment, admin dashboard | Nightly |

---

## Risk Register

| Risk ID | Risk Description | Impact | Probability | Affected Milestones | Mitigation | Verification |
|---------|-----------------|--------|-------------|---------------------|------------|--------------|
| R-001 | Token theft via XSS | High | Medium | M2, M5 | HTTP-only cookies for JWT storage (D2.7). CSP headers block inline scripts. No token exposure in client-side JavaScript. | OWASP ZAP XSS scan (D5.4). Manual verification that `document.cookie` returns empty for auth tokens. |
| R-002 | Brute force attacks on login | High | High | M2, M5 | Per-user rate limiting: 5 login attempts/minute, lockout after 10 failures in 15 minutes (D2.6). Account lockout notification email via SendGrid. | k6 brute force simulation: 20 rapid login attempts verify HTTP 429 after threshold. Audit log confirms lockout event. |
| R-003 | OAuth provider (Google/GitHub) downtime | Medium | Low | M2, M5 | Login page always shows email/password as primary option; OAuth buttons are secondary (D2.1, D2.2). Error message: "Provider unavailable, please use email/password." Graceful degradation: OAuth callback returns HTTP 502 with user-friendly message and fallback redirect. | Simulate provider 5xx: mock Google/GitHub endpoints returning HTTP 500, verify fallback UI appears within 2 seconds. |
| R-004 | Data breach exposing PII | Critical | Low | M1, M3, M5 | AES-256-GCM encryption at rest for email and profile fields (D1.7). TLS 1.3 in transit. RBAC restricts admin-only data access (D3.2). Append-only audit log tracks all data access (D3.4). Principle of least privilege on database roles. | Database direct-read test: `SELECT email FROM users` returns ciphertext without decryption key. Pentest verifies no unauthorized data access paths. |

---

## Success Criteria

Mapping each spec requirement to its verification approach:

| Requirement | Verification Approach | Milestone |
|------------|----------------------|-----------|
| FR-001: User registration with email verification | Automated test: register -> receive verification email mock -> click verify -> assert `email_verified = true` | M1 |
| FR-002: Login with JWT token generation | Automated test: login -> assert JWT structure (RS256, correct claims, 15-min exp) -> call protected endpoint -> assert HTTP 200 | M1 |
| FR-003: OAuth2 integration (Google, GitHub) | E2E test with Playwright against sandbox Google/GitHub OAuth apps. Both providers complete login and issue JWT. | M2 |
| FR-004: Role-based access control | Test matrix: admin/user/suspended roles against admin-only, user-level, and public endpoints. Assert correct HTTP 200/403. | M3 |
| FR-005: Password reset via email | Automated test: request reset -> receive token mock -> submit new password -> login with new password succeeds, old password fails. | M1 |
| FR-006: Session management with refresh tokens | Automated test: login -> use refresh token -> assert new token pair issued -> assert old refresh token rejected. Concurrent session test: 5 sessions per user, all valid. | M1 |
| FR-007: Two-factor authentication | Manual test: enroll TOTP with Google Authenticator -> submit code -> login requires 2FA -> recovery code works as fallback. | M2 |
| FR-008: API rate limiting per user | k6 test: 200 requests in 60 seconds to rate-limited endpoint -> assert HTTP 429 after threshold -> assert `Retry-After` header present. | M2 |
| FR-009: Audit logging for auth events | Automated test: perform each auth action -> query audit log API -> assert entry exists with correct event_type, user_id, timestamp. | M3 |
| FR-010: User profile management | Automated test: update display_name -> assert updated in GET response. Update email -> verify new email -> assert old email no longer works for login. | M3 |
| FR-011: Admin dashboard for user management | Playwright E2E: admin logs in -> views user list -> suspends user -> asserts suspended user cannot login -> reactivates user. | M4 |
| FR-012: Account deactivation workflow | Automated test: deactivate account -> assert login returns HTTP 403 -> reactivate within 30 days -> assert login succeeds. Test post-30-day reactivation denial. | M4 |
| NFR-001: API response < 200ms | k6 load test: p99 latency < 200ms for all auth endpoints under 10K concurrent sessions (D5.1). Prometheus alert triggers if threshold breached. | M5 |
| NFR-002: 10,000 concurrent sessions | k6 sustained load test: 10K active sessions for 5 minutes with zero HTTP 5xx (D5.1). Redis memory usage monitored; must stay below 4GB. | M5 |
| NFR-003: OWASP Top 10 compliance | OWASP ZAP v2.15 automated scan + manual pentest: zero Medium/High/Critical findings (D5.4). | M5 |
| NFR-004: GDPR compliance | Checklist verification: data export within 72h, deletion within 30d, consent records, privacy policy endpoint, processing activity register (D5.5). | M5 |
| NFR-005: 99.9% uptime | HA infrastructure test: kill one app replica, one Redis node, verify zero dropped requests (D5.6). Calculate theoretical availability: 2 replicas + failover = 99.95% per component. | M5 |
| NFR-006: PII encrypted at rest and in transit | Verification: (a) direct SQL SELECT returns ciphertext, (b) TLS 1.3 confirmed by network capture, (c) no PII in application logs (D1.7, D5.4). | M1, M5 |
