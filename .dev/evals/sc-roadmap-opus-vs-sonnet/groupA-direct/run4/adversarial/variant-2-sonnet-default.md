# Roadmap: User Authentication System

## Executive Summary

This roadmap implements a production-grade user authentication system with OAuth2, JWT-based session management, role-based access control, and comprehensive audit logging. The system targets OWASP Top 10 compliance, 10,000 concurrent sessions, and sub-200ms API response times across all auth endpoints. Delivery is structured across six sequential milestones over approximately 18 weeks, with security hardening and compliance validation as an explicit final gate before launch.

## Goals & Success Metrics

| Goal | Metric | Source |
|------|--------|--------|
| Registration and login flows | 100% of FR-001, FR-002 test cases pass with email verification confirmed | FR-001, FR-002 |
| Token-based session management | JWT issuance + refresh token rotation complete; 10,000 concurrent sessions sustained in load test | FR-006, NFR-002, NFR-001 |
| OAuth2 provider integration | Google and GitHub login flows pass end-to-end; graceful fallback to email/password on provider outage | FR-003, R-003 |
| Role-based access control | RBAC enforcement verified across 4 roles (admin, editor, viewer, unverified); unauthorized access returns 403 | FR-004 |
| Password recovery and 2FA | Password reset email delivered within 60 seconds; TOTP-based 2FA enrollment and verification functional | FR-005, FR-007 |
| API rate limiting | Per-user rate limiting enforces configurable thresholds (default: 100 req/min for auth endpoints) | FR-008, R-002 |
| Audit logging | Every auth event (login, logout, token refresh, password change, role change) persisted to append-only log within 500ms | FR-009, NFR-004 |
| User management | Profile CRUD and account deactivation workflow complete; admin dashboard shows active sessions and user list | FR-010, FR-011, FR-012 |
| Performance | p99 response time < 200ms for all /auth/* endpoints under 10K concurrent sessions | NFR-001, NFR-002 |
| Availability | 99.9% uptime measured over 30-day rolling window | NFR-005 |
| Security compliance | Zero critical/high findings in OWASP ZAP scan; all PII encrypted at rest (AES-256) and in transit (TLS 1.3) | NFR-003, NFR-006, R-001, R-004 |
| GDPR compliance | User data export, right-to-deletion, and consent tracking implemented and tested | NFR-004 |

## Milestones

### M1: Foundation and Core Auth (Weeks 1-3)

**Goal:** Establish infrastructure, database schema, and core registration/login flows.

**Deliverables:**

- D1.1: PostgreSQL 15 schema with `users`, `roles`, `permissions`, `user_roles`, and `refresh_tokens` tables. Columns include `id` (UUID), `email` (unique, normalized), `password_hash` (argon2id), `email_verified` (boolean, default false), `created_at`, `updated_at`, `deactivated_at` (nullable). Migration scripts versioned in `/migrations/`.
- D1.2: Redis 7 configuration for session caching. Key structure: `session:{user_id}:{session_id}` with TTL aligned to refresh token expiry. Connection pooling configured for 10K concurrent connections.
- D1.3: Docker Compose file defining `auth-api`, `postgres`, `redis` services with health checks and network isolation. Dockerfiles for each service using multi-stage builds (base image: `python:3.12-slim`).
- D1.4: User registration endpoint `POST /auth/register` accepting email + password. Validates email format (RFC 5322), password strength (min 12 chars, mixed case, digit, symbol). Stores argon2id hash. Sends verification email via SendGrid.
- D1.5: Email verification endpoint `GET /auth/verify?token={jwt}`. Token expires after 24 hours. Sets `email_verified = true` on success.
- D1.6: Login endpoint `POST /auth/login` accepting email + password. Returns access token (JWT, 15-min TTL) in response body and refresh token (opaque, 7-day TTL) in HTTP-only, Secure, SameSite=Strict cookie. Argon2id verification with constant-time comparison.
- D1.7: Unit test suite covering registration (valid, duplicate email, weak password), login (valid, wrong password, unverified email, deactivated account), and email verification (valid token, expired token, already verified).

**Mapped requirements:** FR-001, FR-002, NFR-001, NFR-006 (partial — TLS termination and password hashing)

**Entry criteria:** Development environment provisioned; PostgreSQL 15 and Redis 7 available; SendGrid API key configured.

**Exit criteria:** All D1.1-D1.7 deliverables reviewed and merged; unit test coverage >= 90% on auth module; registration-to-verified-login flow passes manual smoke test.

**Estimated duration:** 3 weeks.

### M2: Token Management and Session Lifecycle (Weeks 4-5)

**Goal:** Implement full session lifecycle with refresh token rotation, logout, and concurrent session limits.

**Deliverables:**

- D2.1: Refresh token endpoint `POST /auth/refresh` accepting refresh token from cookie. Validates token existence in Redis and PostgreSQL, issues new access token + new refresh token (rotation), invalidates old refresh token. Detects reuse of previously invalidated token and revokes all sessions for that user (security event).
- D2.2: Logout endpoint `POST /auth/logout` invalidates current refresh token in Redis and PostgreSQL, clears cookie.
- D2.3: Logout-all endpoint `POST /auth/logout-all` invalidates all refresh tokens for the authenticated user.
- D2.4: Session listing endpoint `GET /auth/sessions` returns active sessions with device info, IP, and created timestamp. Supports revocation of individual sessions via `DELETE /auth/sessions/{session_id}`.
- D2.5: Configurable maximum concurrent sessions per user (default: 5). Oldest session evicted when limit exceeded.
- D2.6: Integration tests covering: token refresh happy path, refresh token reuse detection, concurrent session eviction, logout invalidation, and session listing accuracy.

**Mapped requirements:** FR-006, NFR-002 (session scaling), R-001 (token theft detection via reuse)

**Entry criteria:** M1 complete and merged.

**Exit criteria:** All D2.1-D2.6 tests pass; token refresh latency < 50ms at p99; refresh token reuse triggers session revocation and audit event.

**Estimated duration:** 2 weeks.

### M3: OAuth2 Provider Integration (Weeks 6-7)

**Goal:** Integrate Google and GitHub OAuth2 flows with graceful fallback.

**Deliverables:**

- D3.1: OAuth2 authorization flow for Google (using `google-auth-library-oauthlib`). Endpoints: `GET /auth/oauth/google` (redirect), `GET /auth/oauth/google/callback` (code exchange). Scopes: `openid email profile`.
- D3.2: OAuth2 authorization flow for GitHub (using `Authlib`). Endpoints: `GET /auth/oauth/github` (redirect), `GET /auth/oauth/github/callback` (code exchange). Scopes: `read:user user:email`.
- D3.3: Account linking: if OAuth email matches existing account, link provider to that account. If no match, create new account with `email_verified = true` (provider-verified). Store provider metadata in `oauth_providers` table (`user_id`, `provider`, `provider_user_id`, `linked_at`).
- D3.4: Fallback handler: on OAuth provider error (timeout, 5xx, invalid state), redirect to `/login` with `error=oauth_unavailable` and display email/password form. Log provider error for monitoring.
- D3.5: CSRF protection via `state` parameter with PKCE-like verifier stored in server-side session (Redis, 10-min TTL).
- D3.6: End-to-end tests for Google and GitHub flows using mock OAuth servers; test for provider timeout (simulate 30s response), invalid callback state, and account linking for existing vs. new users.

**Mapped requirements:** FR-003, R-003 (provider downtime fallback)

**Entry criteria:** M2 complete; Google and GitHub OAuth applications registered (client ID + secret available); callback URLs configured.

**Exit criteria:** Google and GitHub login flows pass end-to-end in staging; provider fallback returns to email/password within 5 seconds of failure; CSRF protection verified (replayed state rejected).

**Estimated duration:** 2 weeks.

### M4: RBAC, Rate Limiting, and Security Controls (Weeks 8-10)

**Goal:** Implement role-based access control, per-user rate limiting, and baseline security hardening.

**Deliverables:**

- D4.1: Role and permission schema seeded in PostgreSQL: 4 roles (`admin`, `editor`, `viewer`, `unverified`). Permission table with entries: `user:read`, `user:write`, `user:delete`, `user:manage_roles`, `audit:read`, `session:revoke`. Role-permission mapping via `role_permissions` join table.
- D4.2: Middleware that extracts JWT claims (`user_id`, `role`), checks permission against required permission for the endpoint, returns 403 if insufficient. Applied to all protected routes except `/auth/login`, `/auth/register`, `/auth/verify`, `/auth/oauth/*`, `/auth/refresh`.
- D4.3: Admin-only endpoints: `GET /admin/users` (list, paginated, filterable by role/status), `PUT /admin/users/{id}/role` (change role), `DELETE /admin/users/{id}` (soft-delete / deactivate). All require `user:manage_roles` permission.
- D4.4: Per-user rate limiting using Redis sliding window. Key: `ratelimit:{user_id}:{endpoint_group}`. Default limits: auth endpoints = 100 req/min, admin endpoints = 200 req/min, general = 1000 req/min. Returns `429 Too Many Requests` with `Retry-After` header when exceeded.
- D4.5: Brute force protection: account lockout after 5 consecutive failed login attempts within 15 minutes. Locked for 30 minutes. Unlock via email link or admin override. Lockout counter stored in Redis with TTL.
- D4.6: Security headers middleware: `Content-Security-Policy` (default-src 'self'), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security: max-age=31536000; includeSubDomains`. All cookies set with `HttpOnly`, `Secure`, `SameSite=Strict`.
- D4.7: Integration tests covering: role-permission enforcement (each role against each endpoint), rate limit triggering and `Retry-After` header, account lockout after 5 failures, lockout expiry, admin user management CRUD.

**Mapped requirements:** FR-004, FR-008, R-001 (XSS mitigation via CSP + HTTP-only cookies), R-002 (brute force via lockout + rate limiting)

**Entry criteria:** M3 complete; role/permission definitions approved by product owner.

**Exit criteria:** All D4.1-D4.7 tests pass; rate limiting enforces configured thresholds within +/- 5% tolerance; security headers present on all responses (verified by automated check).

**Estimated duration:** 3 weeks.

### M5: Password Reset, 2FA, Profile, and Account Lifecycle (Weeks 11-13)

**Goal:** Complete user-facing auth features: password recovery, two-factor authentication, profile management, and account deactivation.

**Deliverables:**

- D5.1: Password reset request endpoint `POST /auth/forgot-password` accepting email. Generates time-limited token (1-hour expiry), stores hash in `password_resets` table, sends reset link via SendGrid. Returns `200 OK` regardless of email existence (prevents enumeration).
- D5.2: Password reset confirmation endpoint `POST /auth/reset-password` accepting token + new password. Validates token, enforces password strength policy (same as registration), updates password hash, invalidates all existing refresh tokens, sends confirmation email.
- D5.3: TOTP-based 2FA enrollment: `POST /auth/2fa/enroll` generates TOTP secret, returns QR code (Base64-encoded PNG) and manual entry key. Secret stored encrypted (AES-256-GCM) in `user_2fa` table. Enrollment not active until `POST /auth/2fa/verify` confirms first valid TOTP code.
- D5.4: 2FA verification integrated into login flow: after successful password check, if 2FA enrolled, login returns `401` with `X-2FA-Required: true` header. Client submits `POST /auth/2fa/challenge` with TOTP code. On success, tokens issued. Backup codes (10 single-use, 8-char alphanumeric) generated on enrollment, stored hashed.
- D5.5: User profile endpoints: `GET /auth/profile` (current user), `PUT /auth/profile` (update display name, timezone), `PUT /auth/password` (authenticated password change requiring current password). All changes emit audit events.
- D5.6: Account deactivation: `POST /auth/deactivate` (self-service) or `DELETE /admin/users/{id}` (admin). Soft-delete: sets `deactivated_at` timestamp, invalidates all sessions, removes from login queries. 30-day grace period before hard delete (GDPR right-to-deletion). Hard delete removes PII, retains anonymized audit records.
- D5.7: GDPR compliance endpoints: `GET /auth/export-data` (JSON export of all user data), `DELETE /auth/account` (immediate deletion with re-authentication). Consent tracking in `user_consents` table.
- D5.8: Integration tests covering: password reset happy path, expired token, reused token, 2FA enrollment + verification + backup code, profile update, account deactivation + grace period + hard delete, data export completeness.

**Mapped requirements:** FR-005, FR-007, FR-010, FR-012, NFR-004 (GDPR), R-004 (PII encryption in 2FA secrets)

**Entry criteria:** M4 complete; SendGrid templates for password reset and 2FA enrollment approved; TOTP library selected (e.g., `pyotp`).

**Exit criteria:** All D5.1-D5.8 tests pass; password reset email delivered within 60 seconds in staging; 2FA QR code scannable by Google Authenticator and Authy; account deactivation prevents login within 1 second; data export includes all stored PII fields.

**Estimated duration:** 3 weeks.

### M6: Audit Logging, Admin Dashboard, and Compliance Validation (Weeks 14-16)

**Goal:** Implement comprehensive audit logging, build admin dashboard, and validate all NFRs through security scanning and load testing.

**Deliverables:**

- D6.1: Append-only audit log table `audit_events` with columns: `id` (UUID), `event_type` (enum: login, logout, token_refresh, password_change, role_change, account_deactivate, 2fa_enroll, 2fa_verify, oauth_link, data_export, rate_limit_exceeded, account_lockout), `actor_user_id`, `target_user_id` (nullable), `ip_address`, `user_agent`, `metadata` (JSONB), `created_at`. Index on `(actor_user_id, created_at)` and `(event_type, created_at)`.
- D6.2: Audit event emission from every auth endpoint. Events written synchronously to PostgreSQL (data integrity priority) with async fan-out to a separate read replica for dashboard queries. Event written within 500ms of action.
- D6.3: Admin dashboard API: `GET /admin/audit` (paginated, filterable by event_type, user_id, date range), `GET /admin/stats` (active users, sessions, failed logins in last 24h), `GET /admin/users/{id}/activity` (recent audit events for a specific user).
- D6.4: Admin dashboard frontend (single-page app, React or server-rendered): user list with search/filter, session management, audit log viewer with export to CSV, role assignment, account deactivation. Served from `/admin/` behind `user:manage_roles` permission.
- D6.5: OWASP ZAP security scan executed against staging environment. All critical and high findings resolved before exit. Scan results documented in `/security/scan-reports/`.
- D6.6: Load test plan using k6 or Locust: ramp to 10,000 concurrent sessions over 10 minutes, sustain for 30 minutes. Assert: p99 response time < 200ms for `/auth/login`, `/auth/refresh`, `/auth/profile`; zero 5xx errors; Redis connection pool stable.
- D6.7: Uptime monitoring configuration: health check endpoint `GET /health` returning PostgreSQL and Redis connectivity status. Alerting threshold: 3 consecutive failures trigger incident. Target: 99.9% over 30-day window (max 43.2 minutes downtime/month).
- D6.8: PII encryption verification: confirm `password_hash` is argon2id (not reversible), TOTP secrets encrypted with AES-256-GCM, email addresses stored in encrypted column (`pgcrypto`), TLS 1.3 enforced on all endpoints, all cookies `Secure` flag set.

**Mapped requirements:** FR-009, FR-011, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-006, R-004

**Entry criteria:** M5 complete; staging environment mirrors production configuration; OWASP ZAP and k6 installed and configured.

**Exit criteria:** OWASP ZAP scan shows zero critical/high findings; load test sustains 10K sessions with p99 < 200ms; audit log captures all 12 event types; admin dashboard functional end-to-end; health check passes; all PII encryption verified.

**Estimated duration:** 3 weeks.

### M7: Production Hardening and Launch (Weeks 17-18)

**Goal:** Final production readiness: edge case validation, monitoring, runbooks, and go-live.

**Deliverables:**

- D7.1: Edge case validation test suite covering: empty database (first user registration), single-user system (admin creates own account), max-load (10K sessions + audit writes simultaneously), token expiry at exact boundary, refresh token reuse race condition (two simultaneous refresh requests), OAuth callback with malformed state parameter, rate limit at exact threshold boundary.
- D7.2: Monitoring and alerting: Prometheus metrics for request latency (p50/p95/p99), error rate, active sessions, rate limit rejections, failed login attempts. Grafana dashboards for auth service health. Alerts for: error rate > 1%, p99 > 300ms, active sessions approaching Redis limit, audit event write failures.
- D7.3: Incident response runbook: token rotation failure, Redis connectivity loss, PostgreSQL failover, OAuth provider outage, suspected breach response (revoke all tokens, force password reset, notify affected users).
- D7.4: Production deployment: Kubernetes manifests (Deployment, Service, ConfigMap, Secret), horizontal pod autoscaler (min 3 replicas, max 10, CPU target 70%), database connection pooling via PgBouncer, Redis Sentinel for high availability.
- D7.5: Launch readiness checklist: all M1-M6 exit criteria verified in production-equivalent staging, rollback procedure tested, communication plan for users (password policy changes, 2FA availability), support team trained on admin dashboard.

**Mapped requirements:** NFR-002 (scaling via HPA), NFR-005 (uptime via redundancy), R-001 through R-004 (operational mitigations)

**Entry criteria:** M6 complete; staging passes all load and security tests; production infrastructure provisioned.

**Exit criteria:** Launch readiness checklist 100% complete; rollback procedure verified by deploying a known-bad image and confirming automatic rollback; monitoring dashboards live; support team acknowledges readiness.

**Estimated duration:** 2 weeks.

## Dependency Graph

```
M1 (Foundation)
 |
 +--> M2 (Token Management)
       |
       +--> M3 (OAuth2)
       |     |
       |     +--> M4 (RBAC + Security) -- depends on D3.3 account linking for OAuth user roles
       |           |
       |           +--> M5 (2FA + Profile + GDPR)
       |                 |
       |                 +--> M6 (Audit + Dashboard + Compliance)
       |                       |
       |                       +--> M7 (Production Hardening)
       |
       +--> M4 (RBAC + Security) -- D4.1 role schema independent of OAuth
```

**Explicit prerequisites:**

- M2 requires M1: depends on D1.1 (user schema), D1.6 (JWT issuance), D1.3 (Redis).
- M3 requires M2: OAuth callback issues tokens through the session lifecycle established in M2.
- M4 requires M3: OAuth users need roles assigned; D3.3 account linking feeds into D4.2 permission middleware.
- M5 requires M4: profile endpoints and account deactivation must enforce RBAC permissions from D4.2.
- M6 requires M5: audit logging must capture all event types including 2FA and deactivation events from M5.
- M7 requires M6: production launch requires compliance validation (D6.5, D6.6) to pass.

**Parallelism opportunity:** M3 (OAuth2) and the RBAC schema design portion of M4 (D4.1) can proceed in parallel since role definitions are independent of OAuth provider integration. However, D4.2 (permission middleware) must wait for D3.3 (account linking) to handle OAuth-authenticated users correctly.

## Risk Register

| ID | Risk | Impact | Probability | Mitigation | Milestone |
|----|------|--------|------------|------------|-----------|
| R-001 | Token theft via XSS | High | Medium | HTTP-only cookies for refresh tokens; CSP headers (D4.6); SameSite=Strict on all cookies; no tokens in localStorage or URL parameters | M2 (D2.1), M4 (D4.6) |
| R-002 | Brute force attacks | High | High | Per-user rate limiting (D4.4, 100 req/min on auth endpoints); account lockout after 5 failures (D4.5, 30-min lockout); argon2id hashing with high memory cost (D1.4) | M4 (D4.4, D4.5) |
| R-003 | OAuth provider downtime | Medium | Low | Fallback to email/password login with user-facing error message (D3.4); provider health check in monitoring (D7.2); cached provider metadata to reduce dependency | M3 (D3.4), M7 (D7.2) |
| R-004 | Data breach of PII | Critical | Low | AES-256-GCM encryption for TOTP secrets (D5.3); pgcrypto for email column (D6.8); TLS 1.3 enforced; argon2id for passwords; append-only audit log for forensic trail (D6.1); RBAC limits data access (D4.2); 30-day hard delete grace period limits data retention (D5.6) | M1 (D1.4), M4 (D4.2), M5 (D5.3, D5.6), M6 (D6.1, D6.8) |
| R-005 | Redis single point of failure | High | Medium | Redis Sentinel for HA in production (D7.4); graceful degradation on Redis loss — accept login with direct PostgreSQL token validation (slower, but functional); alert on Redis connectivity (D7.2) | M7 (D7.4) |
| R-006 | SendGrid delivery failures block registration | High | Low | Email delivery is async — registration completes, user marked `email_verified = false` and can request resend; admin can manually verify; fallback: queue emails in PostgreSQL for retry with exponential backoff (3 attempts over 24 hours) | M1 (D1.4, D1.5) |
| R-007 | JWT secret rotation without session invalidation | Medium | Medium | Support multiple active signing keys; new tokens signed with new key, old tokens validated against key list; key rotation procedure documented in runbook (D7.3) | M2 (D2.1), M7 (D7.3) |
| R-008 | Race condition on concurrent refresh token requests | Medium | Medium | Redis `WATCH/MULTI/EXEC` for atomic token invalidation + issuance; test explicitly in edge case suite (D7.1); if reuse detected, revoke all sessions as compromise indicator | M2 (D2.1), M7 (D7.1) |

## Open Questions

1. **Password policy strength**: The spec says "password" without specifying policy. This roadmap assumes 12-character minimum with mixed case, digit, and symbol. Does the product owner want a configurable policy or is this fixed?
2. **OAuth provider list**: Only Google and GitHub are specified. Is there a timeline for adding additional providers (Microsoft, Apple, GitLab)? This affects the `oauth_providers` schema extensibility in D3.3.
3. **2FA enforcement**: Should admins be able to require 2FA for specific roles or all users? The current design makes 2FA optional per user. Mandatory 2FA for admin roles would add a conditional check in D4.2.
4. **Session TTL values**: This roadmap assumes 15-minute access tokens and 7-day refresh tokens. Are these acceptable, or does the product owner have specific requirements? Longer refresh token TTL increases the window for token theft.
5. **Audit log retention**: How long should audit events be retained? GDPR may require deletion after a period, but compliance (SOC 2, etc.) may require 1+ year retention. This affects D6.1 storage planning.
6. **Account deactivation vs. deletion naming**: FR-012 says "deactivation" but GDPR requires right to deletion. This roadmap implements both (soft deactivation with 30-day grace period, then hard delete). Confirm this is acceptable.
7. **Admin dashboard technology**: D6.4 assumes a separate frontend (React or server-rendered). Is there an existing frontend framework this should integrate with, or is a standalone dashboard acceptable?
8. **Rate limit configuration**: Default limits are proposed (100/200/1000 req/min). Should these be configurable per-tenant, per-role, or is a global default sufficient?
9. **Concurrent session limit**: D2.5 defaults to 5 sessions. Is this the right number for the target user base? Enterprise customers may expect higher limits.
10. **Database scaling strategy**: PostgreSQL 15 handles 10K concurrent connections poorly without pooling. This roadmap uses PgBouncer (D7.4). Is the team familiar with connection pooling, or is training needed?

## Out of Scope

The following are explicitly excluded from this roadmap, consistent with the source specification:

- **Biometric authentication**: Fingerprint, face recognition, or other biometric modalities (source spec: out of scope).
- **Hardware security keys**: FIDO2/WebAuthn/U2F support (source spec: out of scope). Could be added as a future M8 milestone if needed.
- **Custom SSO protocol implementation**: SAML, CAS, or proprietary SSO (source spec: out of scope). Standard OAuth2 client is in scope (M3).
- **Multi-tenancy**: The system assumes a single tenant. Organization-level isolation, tenant-specific RBAC, and tenant provisioning are not addressed.
- **Mobile SDK**: This roadmap addresses server-side auth endpoints. A dedicated mobile SDK for iOS/Android token management is out of scope.
- **Email template customization**: SendGrid templates are assumed to be static. A/B testing or user-selectable email themes are out of scope.
- **Internationalization (i18n)**: Error messages and email templates are in English only. Localization is deferred to a future release.
- **Passwordless login**: Magic link or passwordless email login is not included. The auth system supports password + OAuth2 + 2FA only.
- **IP-based access control**: Geofencing or IP allowlisting for login is not included. Rate limiting (D4.4) is IP-unaware at the permission level.

## Success Criteria

| Criterion | Satisfied By | Verification Method |
|-----------|-------------|---------------------|
| All FR requirements implemented and tested | M1 (FR-001, FR-002), M2 (FR-006), M3 (FR-003), M4 (FR-004, FR-008), M5 (FR-005, FR-007, FR-010, FR-012), M6 (FR-009, FR-011) | All deliverable tests pass; exit criteria met for M1-M6 |
| OWASP compliance verified via security scan | M6 (D6.5) | OWASP ZAP scan with zero critical/high findings |
| Load testing confirms 10K concurrent sessions | M6 (D6.6) | k6/Locust load test: 10K sessions sustained for 30 minutes, p99 < 200ms, zero 5xx |
| OAuth2 flow works for Google and GitHub | M3 (D3.1, D3.2) | End-to-end tests pass for both providers in staging |
| Audit logs capture all auth events | M6 (D6.1, D6.2) | Verify all 12 event types present in audit log after full-flow integration test |
| API response time < 200ms for auth endpoints | M6 (D6.6) | Load test p99 measurements |
| 99.9% uptime for auth services | M6 (D6.7), M7 (D7.4) | 30-day rolling measurement post-launch; health check monitoring active |
| All PII encrypted at rest and in transit | M6 (D6.8) | Automated verification: pgcrypto on emails, AES-256-GCM on TOTP secrets, TLS 1.3 enforced |
| GDPR compliance for user data | M5 (D5.6, D5.7) | Data export endpoint tested; deletion removes PII; consent tracking functional |
