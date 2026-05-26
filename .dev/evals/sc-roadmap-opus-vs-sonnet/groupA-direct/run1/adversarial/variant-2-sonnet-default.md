# User Authentication System — Implementation Roadmap

**Variant:** 2 (sonnet / default persona)
**Source Spec:** `tests/sc-roadmap/fixtures/sample_spec.md`
**Generated:** 2026-05-22

---

## Executive Summary

This roadmap delivers a production-grade user authentication system over **5 milestones (~8.5 sprints / 17 weeks)**. The design is opinionated: PostgreSQL 15 is the sole durable store, Redis 7 handles session state and rate-limit counters, and the auth surface is a stateless REST API issuing short-lived JWT access tokens (15 min) backed by opaque refresh tokens stored in Redis with a 7-day TTL. OAuth2 flows delegate to Google and GitHub via the standard authorization-code grant with PKCE. RBAC is enforced at a middleware layer, and every mutation flows through a structured audit logger writing to an immutable append-only table.

The sequencing prioritizes **getting credentials working and safe first** (M1-M2), then **layering authorization and observability** (M3), then **surfacing management controls** (M4), and finally **proving performance and compliance** (M5). This ordering minimizes integration risk: by the time the admin dashboard is built, every endpoint it consumes already exists and is audited.

**Key architectural decisions:**

- **JWT over session cookies for the API boundary.** The spec calls for both JWT and session management. Access tokens are stateless JWTs for horizontal scalability; refresh tokens are opaque, server-side-validated strings stored in Redis to allow instant revocation.
- **RBAC with a static role hierarchy, not a dynamic permission matrix.** The spec requires role-based access control but does not call for arbitrary permission composition. Four roles (viewer, editor, admin, superadmin) cover the stated requirements and keep the authorization layer auditable.
- **Rate limiting before the application handler.** A Redis-backed sliding-window counter rejects over-limit requests at the middleware level, consuming zero application CPU — directly mitigating R-002 (brute force).

---

## Milestone 1: Data Layer & Core Authentication

**ID:** M1
**Duration:** 2 sprints (4 weeks)
**Goal:** A running auth service that can register users, verify email, issue JWTs, and refresh sessions. Every credential is hashed, every token is HTTP-only, and every connection is TLS.

### Deliverables

| ID | Deliverable | Source Coverage |
|----|-------------|-----------------|
| D1.1 | PostgreSQL 15 schema: `users`, `roles`, `user_roles`, `refresh_tokens`, `email_verifications` tables | FR-001, FR-006 |
| D1.2 | User registration endpoint (`POST /auth/register`) with SendGrid email verification flow | FR-001 |
| D1.3 | Login endpoint (`POST /auth/login`) issuing JWT access token (15-min TTL) + opaque refresh token (7-day TTL) | FR-002, FR-006 |
| D1.4 | Refresh endpoint (`POST /auth/refresh`) rotating the refresh token on each use | FR-006 |
| D1.5 | Logout endpoint (`POST /auth/logout`) revoking the refresh token in Redis | FR-006 |
| D1.6 | Redis 7 session store: refresh token → user_id mapping with TTL-based expiration | FR-006, NFR-002 |
| D1.7 | TLS termination at the reverse proxy (envoy/nginx); all internal traffic over TLS | NFR-006 |
| D1.8 | PII encryption at rest: AES-256-GCM for email, phone fields using a KMS-managed DEK | NFR-006 |
| D1.9 | Docker Compose dev environment: PostgreSQL, Redis, API service, migration runner | Dependency (Docker, PostgreSQL, Redis) |
| D1.10 | HTTP-only, Secure, SameSite=Strict cookie settings for token delivery | R-001 |

### Dependencies

- PostgreSQL 15 cluster provisioned (cloud-managed or Docker local).
- Redis 7 instance provisioned.
- SendGrid API key provisioned with a verified sender domain.
- Docker installed on all developer machines.

### Acceptance Criteria

- [ ] `POST /auth/register` creates a user with `bcrypt`-hashed password, sets `email_verified=false`, dispatches a verification email via SendGrid, and returns `201 Created`.
- [ ] Clicking the verification link sets `email_verified=true` and redirects to the login page.
- [ ] `POST /auth/login` returns `401` for unverified emails, `401` for wrong passwords, and `200` with a JWT + refresh token for valid credentials.
- [ ] JWT payload contains `sub` (user_id), `roles`, `iat`, `exp`; signed with RS256 (asymmetric key pair).
- [ ] `POST /auth/refresh` returns a new access + refresh pair and invalidates the old refresh token. Reuse of an old refresh token revokes the entire token family (refresh token rotation with replay detection).
- [ ] All tokens delivered via HTTP-only cookies; `Authorization: Bearer` header also accepted for API-only clients.
- [ ] Automated test suite: unit tests for each endpoint, integration test hitting a real PostgreSQL + Redis in Docker.
- [ ] Response time for `/auth/login` and `/auth/register` measured at < 200ms p95 locally (NFR-001 baseline).
- [ ] Database migration scripts are idempotent and run via a versioned migration tool (golang-migrate or Alembic).

### Risks Addressed

| Risk | Mitigation in M1 |
|------|-------------------|
| R-001: Token theft via XSS | D1.10 — HTTP-only, Secure, SameSite=Strict cookies; CSP headers set on all responses. No token in localStorage. |
| R-004: Data breach of PII | D1.7, D1.8 — TLS in transit, AES-256-GCM at rest. Passwords never stored plaintext (bcrypt, cost factor 12). |

### Estimated Effort

**2 sprints** (4 weeks). Schema + migrations: 2 days. Registration + email verification: 3 days. Login + JWT: 2 days. Refresh token rotation: 2 days. Redis integration: 1 day. Encryption layer: 2 days. Docker Compose + CI: 1 day. Testing + hardening: 3 days.

---

## Milestone 2: OAuth2 Providers & Password Recovery

**ID:** M2
**Duration:** 1.5 sprints (3 weeks)
**Goal:** Users can authenticate via Google or GitHub OAuth2 and recover their password through a time-limited email link. The system degrades gracefully if an OAuth provider is down.

### Deliverables

| ID | Deliverable | Source Coverage |
|----|-------------|-----------------|
| D2.1 | OAuth2 authorization-code flow with PKCE for Google | FR-003 |
| D2.2 | OAuth2 authorization-code flow with PKCE for GitHub | FR-003 |
| D2.3 | `GET /auth/oauth/{provider}/redirect` — initiates the flow | FR-003 |
| D2.4 | `GET /auth/oauth/{provider}/callback` — exchanges code, upserts user, issues tokens | FR-003 |
| D2.5 | Password reset request endpoint (`POST /auth/password-reset/request`) sending a time-limited (15-min) token via SendGrid | FR-005 |
| D2.6 | Password reset confirmation endpoint (`POST /auth/password-reset/confirm`) validating the token and updating the password | FR-005 |
| D2.7 | OAuth provider health-check circuit breaker: if Google/GitHub returns 5xx on token exchange, fall back to email/password login with a user-facing message | R-003 |

### Dependencies

- M1 complete (user schema, JWT issuance, SendGrid integration).
- Google Cloud Console project with OAuth2 client ID/secret.
- GitHub OAuth App registered with callback URL.

### Acceptance Criteria

- [ ] `GET /auth/oauth/google/redirect` returns a `302` to Google's authorization URL with PKCE `code_challenge`.
- [ ] `GET /auth/oauth/google/callback` creates a new user if none exists (with `email_verified=true` from Google's ID token), links to existing user by email, and issues JWT + refresh token.
- [ ] Same flow works for GitHub with GitHub's user API as the identity source.
- [ ] If the OAuth provider token endpoint returns 5xx or times out (5s deadline), the user sees: "Google sign-in is temporarily unavailable. Please use email/password." and the login page renders normally — no 500 error page.
- [ ] Password reset email contains a link with a signed JWT (15-min `exp`). Clicking it pre-fills the reset form.
- [ ] After password reset, all existing refresh tokens for that user are revoked (force re-login on all devices).
- [ ] Each OAuth flow has an end-to-end integration test using a mock OAuth server (or provider sandbox).
- [ ] Password reset flow tested: request, receive token, confirm with new password, verify old password fails.

### Risks Addressed

| Risk | Mitigation in M2 |
|------|-------------------|
| R-003: OAuth provider downtime | D2.7 — Circuit breaker with fallback to email/password. No hard dependency on OAuth availability for login. |

### Estimated Effort

**1.5 sprints** (3 weeks). Google OAuth2: 3 days. GitHub OAuth2: 2 days. PKCE + state management: 1 day. Password reset: 2 days. Circuit breaker: 1 day. Testing: 2 days. Edge-case handling (account linking, email conflict): 2 days.

---

## Milestone 3: Security Controls, RBAC & Audit

**ID:** M3
**Duration:** 2 sprints (4 weeks)
**Goal:** The system enforces role-based access, rate-limits every auth endpoint, supports TOTP-based 2FA, and writes an immutable audit trail for every authentication event.

### Deliverables

| ID | Deliverable | Source Coverage |
|----|-------------|-----------------|
| D3.1 | Role model: four roles (`viewer`, `editor`, `admin`, `superadmin`) stored in `user_roles` table with a static permission map | FR-004 |
| D3.2 | RBAC middleware: decorator/middleware that checks the JWT's `roles` claim against the required permission for each endpoint | FR-004 |
| D3.3 | Role management endpoints: `POST /admin/roles/assign`, `DELETE /admin/roles/revoke` (admin-only) | FR-004 |
| D3.4 | TOTP-based 2FA setup: `POST /auth/2fa/setup` generates a QR code (TOTP secret stored encrypted in `user_2fa` table) | FR-007 |
| D3.5 | 2FA verification step in login flow: if 2FA is enabled, `/auth/login` returns `202 Accepted` with a `2fa_required=true` flag; client calls `POST /auth/2fa/verify` with the TOTP code to complete login | FR-007 |
| D3.6 | 2FA backup codes: generated at setup, hashed and stored, each usable once | FR-007 |
| D3.7 | Redis sliding-window rate limiter: 10 requests/minute for `/auth/login`, 5/minute for `/auth/password-reset/*`, 100/minute for general API endpoints | FR-008, R-002 |
| D3.8 | Account lockout: after 5 consecutive failed login attempts, lock account for 15 minutes (with admin override) | R-002 |
| D3.9 | Audit log table (`audit_events`): immutable, append-only, partitioned by month. Columns: `event_id`, `event_type`, `user_id`, `ip_address`, `user_agent`, `metadata` (JSONB), `created_at` | FR-009 |
| D3.10 | Audit event emission: structured log on registration, login, login_failure, logout, token_refresh, password_reset, role_change, 2fa_setup, 2fa_verify, oauth_login | FR-009 |
| D3.11 | OWASP Top 10 hardening pass: CSP headers, X-Frame-Options, X-Content-Type-Options, input validation (zod/pydantic), parameterized queries (already enforced by ORM) | NFR-003 |

### Dependencies

- M1 complete (JWT with role claims, Redis connectivity).
- TOTP library (e.g., `pyotp` for Python, `otp` for Go).

### Acceptance Criteria

- [ ] `viewer` role can read own profile only. `editor` can update own profile. `admin` can manage all users' roles. `superadmin` can manage admins.
- [ ] RBAC middleware rejects unauthorized access with `403 Forbidden` and an audit event.
- [ ] 2FA setup generates a valid TOTP QR code. Authenticator apps (Google Authenticator, Authy) produce codes that pass verification.
- [ ] Login with 2FA enabled follows the two-step flow: `/auth/login` returns `202` with `2fa_required`, `/auth/2fa/verify` with valid TOTP returns `200` with tokens. Invalid TOTP returns `401`.
- [ ] Rate limiter returns `429 Too Many Requests` with a `Retry-After` header when the sliding window is exceeded.
- [ ] Account lockout triggers after 5 failed attempts and auto-unlocks after 15 minutes. Admin can manually unlock via `POST /admin/users/{id}/unlock`.
- [ ] Every audit event has all required columns populated. The `audit_events` table has no UPDATE/DELETE grants for the application role — only INSERT and SELECT.
- [ ] Automated OWASP ZAP baseline scan against a running instance returns zero high/medium alerts.
- [ ] No reflected or stored XSS in any input field (verified by injecting `<script>` payloads in registration and profile fields).

### Risks Addressed

| Risk | Mitigation in M3 |
|------|-------------------|
| R-001: Token theft via XSS | D3.11 — CSP headers, input validation. Defense in depth beyond M1's HTTP-only cookies. |
| R-002: Brute force attacks | D3.7, D3.8 — Sliding-window rate limiter + account lockout. Multi-layered protection. |
| R-004: Data breach of PII | D3.9, D3.10 — Comprehensive audit trail enables breach detection and forensic analysis. |

### Estimated Effort

**2 sprints** (4 weeks). RBAC model + middleware: 3 days. Role management endpoints: 2 days. 2FA setup + verify + backup codes: 4 days. Rate limiter: 2 days. Account lockout: 1 day. Audit logger + table: 2 days. OWASP hardening pass: 2 days. Testing: 4 days.

---

## Milestone 4: User Management & Admin Dashboard

**ID:** M4
**Duration:** 1.5 sprints (3 weeks)
**Goal:** Users manage their own profiles. Admins manage all users through a web dashboard. Account deactivation is a controlled workflow with a grace period. GDPR rights are operational.

### Deliverables

| ID | Deliverable | Source Coverage |
|----|-------------|-----------------|
| D4.1 | User profile endpoints: `GET /auth/me`, `PATCH /auth/me` (name, avatar URL, timezone) | FR-010 |
| D4.2 | Avatar upload endpoint: `POST /auth/me/avatar` storing to S3/R2 with a signed URL for download | FR-010 |
| D4.3 | Admin dashboard: React SPA with user list, user detail, role assignment, and account status management | FR-011 |
| D4.4 | Admin API endpoints: `GET /admin/users` (paginated, filterable), `GET /admin/users/{id}`, `PATCH /admin/users/{id}` (status, roles) | FR-011 |
| D4.5 | Account deactivation workflow: `POST /auth/me/deactivate` (self-service) or `POST /admin/users/{id}/deactivate` (admin). Sets status to `pending_deactivation`, 14-day grace period, then `deactivated` with PII scrubbing | FR-012 |
| D4.6 | Account reactivation: `POST /auth/reactivate` during grace period restores the account | FR-012 |
| D4.7 | GDPR data export: `POST /auth/me/export` generates a JSON/ZIP of all user data within 72 hours, delivered via email link | NFR-004 |
| D4.8 | GDPR right to erasure: after the 14-day grace period, all PII is replaced with `REDACTED_<hash>` and the email is anonymized. Audit log entries retain `user_id` but no PII | NFR-004 |

### Dependencies

- M1 and M3 complete (auth endpoints, RBAC, audit logging).
- S3-compatible storage bucket for avatar uploads.
- Frontend build pipeline (Vite + React).

### Acceptance Criteria

- [ ] `GET /auth/me` returns the authenticated user's profile without exposing password hash or 2FA secret.
- [ ] `PATCH /auth/me` updates allowed fields only; email change triggers re-verification.
- [ ] Admin dashboard renders user list with server-side pagination (20 per page) and filters by role, status, and registration date.
- [ ] Admin can assign/revoke roles and the change is immediately reflected in subsequent JWT refreshes.
- [ ] Account deactivation sets status to `pending_deactivation`. User receives a confirmation email. During the 14-day grace period, login returns `403` with a reactivation link.
- [ ] After 14 days, a scheduled job scrubs PII: email → `redacted_<sha256(user_id)>@deleted.internal`, name → `REDACTED`, password hash → invalidated. The user row persists for audit referential integrity.
- [ ] GDPR data export produces a complete JSON dump: profile, login history (from audit log), roles, active sessions. Download link expires in 24 hours.
- [ ] Only `admin` and `superadmin` roles can access `/admin/*` endpoints (enforced by RBAC middleware from M3).

### Risks Addressed

| Risk | Mitigation in M4 |
|------|-------------------|
| R-004: Data breach of PII | D4.5, D4.8 — Grace period + PII scrubbing. Breached data from deactivated accounts is irrecoverable. |

### Estimated Effort

**1.5 sprints** (3 weeks). Profile endpoints: 2 days. Avatar upload: 1 day. Admin API: 3 days. Admin dashboard (React): 5 days. Deactivation workflow + scheduled job: 3 days. GDPR export + erasure: 2 days. Testing: 2 days.

---

## Milestone 5: Performance Validation, Compliance & Launch

**ID:** M5
**Duration:** 1 sprint (2 weeks)
**Goal:** The system is proven to meet every non-functional requirement and success criterion. Production readiness is demonstrated, not claimed.

### Deliverables

| ID | Deliverable | Source Coverage |
|----|-------------|-----------------|
| D5.1 | Load test suite: k6 or Locust script simulating 10,000 concurrent sessions performing login, token refresh, and API calls | NFR-001, NFR-002 |
| D5.2 | P95 latency report: all auth endpoints under 200ms under 10K concurrent load | NFR-001 |
| D5.3 | Sustained-load soak test: 10K sessions over 4 hours with zero error-rate increase, measuring Redis memory and PostgreSQL connection pool stability | NFR-002, NFR-005 |
| D5.4 | OWASP ZAP full scan report with zero high/medium findings (repeat of M3 baseline, now against the complete system) | NFR-003 |
| D5.5 | GDPR compliance checklist: data inventory, retention policy document, DPA with SendGrid, consent logging verification | NFR-004 |
| D5.6 | Uptime validation: deploy to staging with health checks, verify 99.9% uptime over a 7-day observation window (or argue equivalence from architecture: multi-AZ, no single point of failure, automated failover) | NFR-005 |
| D5.7 | Encryption audit: verify TLS 1.2+ on all endpoints, AES-256-GCM for PII at rest, key rotation procedure documented | NFR-006 |
| D5.8 | Production deployment runbook: step-by-step guide for deploying to production, rolling back, and scaling | — |
| D5.9 | Monitoring and alerting: Prometheus metrics (request latency, error rate, active sessions, token issuance rate) + Grafana dashboard + PagerDuty alert on p95 > 200ms or error rate > 1% | NFR-001, NFR-005 |

### Dependencies

- M1 through M4 complete and merged.
- Staging environment mirroring production topology.
- Load testing infrastructure (k6 Cloud, or self-hosted k6/Locust cluster).

### Acceptance Criteria

- [ ] Load test results: 10,000 concurrent sessions, p95 latency < 200ms for all `/auth/*` endpoints, p99 < 500ms.
- [ ] Zero session drops during 4-hour soak test. Redis memory usage documented and within 70% of allocated limit.
- [ ] OWASP ZAP full scan: zero high, zero medium findings. Low findings documented with justification for acceptance.
- [ ] GDPR checklist fully completed and reviewed by legal/privacy team (or proxy).
- [ ] Health check endpoint (`GET /health`) returns `200` with `{"status": "ok", "db": "ok", "redis": "ok"}`.
- [ ] Grafana dashboard shows real-time metrics for latency, error rate, active sessions, and token issuance.
- [ ] PagerDuty alert fires within 60 seconds of p95 latency exceeding 200ms for 2 consecutive minutes.
- [ ] Production deployment runbook reviewed and dry-run executed on staging.

### Risks Addressed

| Risk | Mitigation in M5 |
|------|-------------------|
| R-001: Token theft via XSS | D5.4 — Full OWASP scan confirms no XSS vectors. |
| R-002: Brute force attacks | D5.1 — Load test validates rate limiter behavior under 10K concurrent sessions. |
| R-004: Data breach of PII | D5.5, D5.7 — GDPR compliance verification + encryption audit. |

### Estimated Effort

**1 sprint** (2 weeks). Load test authoring + execution: 3 days. OWASP full scan + remediation: 2 days. GDPR compliance review: 1 day. Monitoring setup: 2 days. Deployment runbook: 1 day. Soak test + analysis: 1 day.

---

## Cross-Cutting Concerns

### Security

Security is not a single milestone — it is a thread running through every phase.

| Concern | M1 | M2 | M3 | M4 | M5 |
|---------|----|----|----|----|-----|
| TLS everywhere | D1.7 | — | — | — | D5.7 |
| Encryption at rest | D1.8 | — | — | — | D5.7 |
| HTTP-only cookies / CSP | D1.10 | — | D3.11 | — | D5.4 |
| Rate limiting | — | — | D3.7 | — | D5.1 |
| Account lockout | — | — | D3.8 | — | — |
| 2FA | — | — | D3.4-D3.6 | — | — |
| Audit logging | — | — | D3.9-D3.10 | — | — |
| GDPR rights | — | — | — | D4.7-D4.8 | D5.5 |
| OWASP compliance | — | — | D3.11 | — | D5.4 |

### Observability

Structured logging (JSON) is emitted from every handler starting in M1. In M5, this is codified into a Prometheus + Grafana stack:

- **Metrics:** `auth_login_total`, `auth_login_failure_total`, `auth_token_issued_total`, `auth_request_duration_seconds` (histogram), `auth_active_sessions` (gauge from Redis).
- **Logs:** JSON-structured, correlated by `request_id` and `user_id`. Shipped to a centralized log store (ELK or Loki).
- **Alerts:** PagerDuty integration for p95 > 200ms (2-min window), error rate > 1% (5-min window), health check failures.

### Performance

- **Connection pooling:** PgBouncer in front of PostgreSQL with a 100-connection pool. Application uses a 20-connection pool per instance.
- **Redis optimization:** Pipeline refresh token lookups and rate-limit increments. Use Redis Cluster if >10K sessions require more than a single node's memory.
- **JWT validation:** Stateless — no database lookup. The RS256 public key is cached by verifying services. Token revocation uses a short TTL + refresh token rotation (no revocation list needed for access tokens).

### Database Operations

- Migrations are versioned, reversible, and run as a pre-deploy step.
- The `audit_events` table is range-partitioned by month. Partitions older than the retention period (configurable, default 2 years) are archived to cold storage and dropped.
- Read replicas for dashboard queries (D4.3) to avoid impacting auth write latency.

---

## Risk Register

| Risk ID | Description | Impact | Probability | Primary Mitigation Milestone | Secondary Mitigation |
|---------|-------------|--------|-------------|------------------------------|----------------------|
| R-001 | Token theft via XSS | High | Medium | M1 (D1.10: HTTP-only cookies) | M3 (D3.11: CSP + input validation), M5 (D5.4: full OWASP scan) |
| R-002 | Brute force attacks | High | High | M3 (D3.7: rate limiter, D3.8: lockout) | M5 (D5.1: validated under load) |
| R-003 | OAuth provider downtime | Medium | Low | M2 (D2.7: circuit breaker + fallback) | M1 (email/password always available as baseline) |
| R-004 | Data breach of PII | Critical | Low | M1 (D1.7-D1.8: TLS + encryption) | M3 (D3.9-D3.10: audit trail), M4 (D4.8: PII scrubbing), M5 (D5.5, D5.7) |

---

## Success Criteria Mapping

The source spec defines five success criteria. Here is where each is validated:

| Success Criterion | Primary Milestone | Deliverables | Validation Method |
|-------------------|-------------------|--------------|-------------------|
| All FR requirements implemented and tested | M1-M4 | D1.1-D4.8 (all 12 FRs) | Automated test suite (unit + integration + E2E). Zero skipped tests. |
| OWASP compliance verified via security scan | M5 | D5.4 | OWASP ZAP full scan report with zero high/medium findings. |
| Load testing confirms 10K concurrent sessions | M5 | D5.1, D5.2, D5.3 | k6 load test report: 10K sessions, p95 < 200ms, 4-hour soak with zero session drops. |
| OAuth2 flow works for Google and GitHub | M2 | D2.1-D2.4 | E2E integration test with mock OAuth server + manual smoke test against real provider sandboxes. |
| Audit logs capture all auth events | M3 | D3.9, D3.10 | Automated test: perform each auth action, query `audit_events`, verify all 10 event types are present with correct metadata. |

### FR Coverage Matrix

| FR | Milestone | Deliverable(s) |
|----|-----------|----------------|
| FR-001 | M1 | D1.1, D1.2 |
| FR-002 | M1 | D1.3 |
| FR-003 | M2 | D2.1, D2.2, D2.3, D2.4 |
| FR-004 | M3 | D3.1, D3.2, D3.3 |
| FR-005 | M2 | D2.5, D2.6 |
| FR-006 | M1 | D1.3, D1.4, D1.5, D1.6 |
| FR-007 | M3 | D3.4, D3.5, D3.6 |
| FR-008 | M3 | D3.7 |
| FR-009 | M3 | D3.9, D3.10 |
| FR-010 | M4 | D4.1, D4.2 |
| FR-011 | M4 | D4.3, D4.4 |
| FR-012 | M4 | D4.5, D4.6 |

### NFR Coverage Matrix

| NFR | Milestone | Deliverable(s) |
|-----|-----------|----------------|
| NFR-001 | M1 (baseline), M5 (validated) | D5.2, D5.9 |
| NFR-002 | M1 (Redis design), M5 (validated) | D1.6, D5.1, D5.3 |
| NFR-003 | M3 (hardening), M5 (validated) | D3.11, D5.4 |
| NFR-004 | M4 (GDPR ops), M5 (reviewed) | D4.7, D4.8, D5.5 |
| NFR-005 | M5 | D5.3, D5.6, D5.9 |
| NFR-006 | M1 (encryption), M5 (audited) | D1.7, D1.8, D5.7 |

---

## Out of Scope

The following items are explicitly out of scope, mirroring the source specification:

- **Biometric authentication** — Fingerprint, face recognition, or voice-based auth. These require platform-specific SDKs and hardware integration that are not part of this system's web-first authentication model.
- **Hardware security keys** — FIDO2/WebAuthn support. This is a valuable future enhancement but adds significant complexity (credential management, recovery flows) that is not justified for the initial release.
- **Custom SSO protocol implementation** — SAML, CAS, or proprietary SSO protocols. OAuth2 with Google and GitHub covers the stated third-party auth needs. SAML integration for enterprise customers is a potential M6 if demand emerges.

Additionally, the following are out of scope for this roadmap but noted for future consideration:

- Multi-tenancy / organization-level roles (the current RBAC is user-global).
- WebSocket-based real-time session revocation notifications.
- Internationalization of email templates and error messages.
- Mobile SDK (the API is designed to be mobile-friendly but no native SDK is built).

---

## Timeline Summary

```
Week  1-4  │██ M1: Data Layer & Core Auth █████████████████│
Week  5-7  │██ M2: OAuth2 & Password Recovery ████████████│
Week  8-11 │██ M3: Security Controls, RBAC & Audit ████████│
Week 12-14 │██ M4: User Management & Admin Dashboard ██████│
Week 15-16 │██ M5: Performance Validation & Launch ████████│
```

**Total: ~17 weeks (8.5 sprints).**

Critical path: M1 → M2 → M3 → M4 → M5 (strictly sequential). M2 and M3 could partially overlap if two teams work in parallel, but the RBAC middleware (M3) should be in place before the admin dashboard (M4) consumes role-managed endpoints.

---

## Opinionated Choices & Justifications

1. **RS256 over HS256 for JWT signing.** Asymmetric keys allow the auth service to be the sole signer while any service can verify using the public key. This avoids sharing a symmetric secret across services and supports future microservice decomposition without key redistribution.

2. **Opaque refresh tokens over JWT refresh tokens.** Storing refresh tokens in Redis enables instant revocation (delete the key) without maintaining a revocation list. This is simpler and more operationally robust than JWT-based refresh tokens, which would require a revocation check on every refresh.

3. **Four static roles over a dynamic permission system.** The spec requires RBAC, not ABAC or a fine-grained permission matrix. A static hierarchy (viewer → editor → admin → superadmin) is auditable, testable, and sufficient for the described use case. If fine-grained permissions are needed later, the `user_roles` table can be extended with a `permissions` JSONB column without schema migration.

4. **Rate limiting at the middleware layer, not the application layer.** Rejected requests consume zero application CPU and never reach the database. The Redis sliding-window algorithm is O(1) per request and accurate to within one window granularity (60 seconds).

5. **14-day grace period for account deactivation.** This balances user protection (accidental deactivation, account recovery) with GDPR compliance (right to erasure). The grace period length is configurable; 14 days aligns with common industry practice and gives users enough time to reactivate without retaining data unnecessarily long.

6. **Append-only audit table with no UPDATE/DELETE grants.** This is a hard constraint at the database role level, not just application logic. Even a compromised application cannot tamper with audit history. Monthly partitioning keeps query performance acceptable as the table grows.

7. **SendGrid for transactional email.** The spec names SendGrid as a dependency. I recommend using SendGrid's template engine for verification and password-reset emails, with a plain-text fallback. The email sending layer should be abstracted behind an interface to allow swapping providers later without business logic changes.
