# Roadmap: User Authentication System

## Overview

This roadmap operationalises the User Authentication System spec into seven sequential
milestones (M1–M7) culminating in a production-ready OAuth2 + JWT + RBAC platform
with 2FA, audit logging, and an admin dashboard. Every Functional Requirement
(FR-001..FR-012), Non-Functional Requirement (NFR-001..NFR-006), and Risk
(R-001..R-004) from `tests/sc-roadmap/fixtures/sample_spec.md` is bound to a
specific deliverable with falsifiable acceptance criteria. The implementation
stack is fixed: PostgreSQL 15.4, Redis 7.2, SendGrid (v3 API), Docker 24+,
Node.js 20 LTS with Fastify 4.x as the HTTP layer (alternative: FastAPI 0.110
on Python 3.12 — chosen at M1.D1.1), `jsonwebtoken` 9.x (or `python-jose` 3.x),
`argon2id` (memory=64MiB, t=3, p=4) for password hashing, and Keycloak-free
in-house RBAC.

The roadmap is sequenced so that security primitives (encryption, hashing,
session storage) land before exposed authentication surfaces, and so that
NFR enforcement gates (load, security scan, GDPR DPIA) are evaluated against a
working integrated build before GA.

---

## Milestone Map

| ID | Milestone                                | Blocks    | Blocked by |
|----|------------------------------------------|-----------|------------|
| M1 | Foundation & Data Layer                  | M2,M3,M4  | —          |
| M2 | Core Authentication (Registration+Login) | M3,M4,M5  | M1         |
| M3 | OAuth2 & Session Management              | M5,M6     | M2         |
| M4 | RBAC & Authorization                     | M5,M6     | M2         |
| M5 | Security Hardening (2FA, Rate Limit, Audit) | M6     | M2,M3,M4   |
| M6 | Admin Dashboard & Lifecycle              | M7        | M4,M5      |
| M7 | NFR Gates, Compliance, GA Release        | —         | M3,M5,M6   |

---

## M1 — Foundation & Data Layer

Establish the persistent and ephemeral stores, the encryption baseline, and the
service skeleton. No auth surface is exposed in this milestone.

### D1.1 — Tech-stack lock-in and service scaffold

- **Requirements covered:** scaffolding for all FRs; precondition for NFR-005.
- **Artifact:** monorepo with `auth-api/`, `auth-worker/`, `auth-admin/` packages;
  Fastify 4.26 selected; Dockerfile (multi-stage, distroless base, non-root UID 10001).
- **Acceptance criteria:**
  - `docker compose up` brings PostgreSQL 15.4 + Redis 7.2 + auth-api healthy
    in <30s on a clean machine.
  - `npm audit --production` reports 0 high/critical vulnerabilities.
  - CI pipeline (GitHub Actions) runs lint+test+build in <8 min and is required
    on every PR.

### D1.2 — PostgreSQL schema with PII encryption

- **Requirements covered:** FR-001 (users table), FR-010 (profile), NFR-004,
  NFR-006, R-004.
- **Artifact:** `users`, `user_profiles`, `user_oauth_identities`,
  `sessions`, `refresh_tokens`, `roles`, `permissions`, `role_permissions`,
  `user_roles`, `audit_events`, `password_reset_tokens`, `mfa_secrets` tables.
- **Acceptance criteria:**
  - PII columns (`email`, `phone`, `full_name`, `address`) stored using
    `pgcrypto` AEAD (`pgp_sym_encrypt`) with a KMS-managed DEK rotated every 90
    days. Verified by `SELECT pg_column_size(email) > length('user@example.com')`
    on inserted rows.
  - `password_hash` column rejects values shorter than argon2id's encoded
    length (>= 96 bytes) via CHECK constraint.
  - Migrations applied with `node-pg-migrate` 7.x; rollback verified in CI.

### D1.3 — Secrets management & TLS

- **Requirements covered:** NFR-006, R-001, R-004.
- **Artifact:** Vault (HashiCorp 1.15) or AWS Secrets Manager integration;
  TLS 1.3 only on ingress; HSTS `max-age=63072000; includeSubDomains; preload`.
- **Acceptance criteria:**
  - `testssl.sh` grade A+; no TLS 1.0/1.1/1.2 ciphers offered.
  - No secret value appears in any container env var dump (`docker inspect`)
    or in process listing (`/proc/<pid>/environ`).
  - Key rotation runbook executes end-to-end in <10 min in staging.

---

## M2 — Core Authentication (Registration + Login)

### D2.1 — User registration with email verification (FR-001)

- **Artifact:** `POST /v1/auth/register`, `GET /v1/auth/verify?token=…`,
  SendGrid template `tpl_register_verify_v1`.
- **Acceptance criteria:**
  - Registration rejects emails failing RFC 5322; rejects passwords failing
    zxcvbn score >= 3 OR length < 12.
  - Verification token is 256-bit random, stored as SHA-256 hash, single-use,
    expiring in exactly 24h ± 1 min.
  - Re-sending verification is rate-limited to 3 per 24h per email.
  - On successful registration, `audit_events` row written with
    `event_type=user.registered`.

### D2.2 — Password storage and login (FR-002)

- **Artifact:** `POST /v1/auth/login` issuing JWT (HS256 disallowed; RS256 with
  rotating 4096-bit RSA key pair) + refresh token cookie.
- **Acceptance criteria:**
  - Passwords hashed with argon2id (m=65536, t=3, p=4); verified by inspecting
    `password_hash` prefix `$argon2id$v=19$m=65536,t=3,p=4$…`.
  - Access token TTL = 15 min; refresh token TTL = 30 days; both claims
    include `iss`, `aud`, `sub`, `jti`, `iat`, `exp`.
  - Failed login increments `failed_attempts`; account locks for 15 min after
    5 consecutive failures (mitigates R-002).
  - Successful login emits `audit.login.success`; failure emits
    `audit.login.failure` with redacted credentials.

### D2.3 — Password reset (FR-005)

- **Artifact:** `POST /v1/auth/password/reset-request`,
  `POST /v1/auth/password/reset` with token.
- **Acceptance criteria:**
  - Reset token: 256-bit random, SHA-256-hashed at rest, 1h TTL, single-use.
  - Reset always returns HTTP 202 regardless of whether email exists (prevents
    enumeration; mitigates R-002 secondary path).
  - Old refresh tokens for the user are revoked on successful reset.
  - Reset event written to audit log.

---

## M3 — OAuth2 & Session Management

### D3.1 — OAuth2 integration (FR-003)

- **Artifact:** Google + GitHub providers via `simple-oauth2` 5.x; PKCE
  enforced; state parameter is 256-bit CSRF token bound to a 10-min Redis key.
- **Acceptance criteria:**
  - Authorization Code + PKCE flow only; implicit flow disabled in code paths.
  - Linking flow merges OAuth identity into existing `users` row by verified
    email; conflicts (different existing account) return 409 and audit event.
  - **Fallback (R-003):** when Google or GitHub OIDC discovery endpoint
    returns 5xx or times out > 3s, login falls back to email/password and an
    operator alert is emitted via PagerDuty webhook.
  - Smoke test in CI exercises both providers against staging credentials.

### D3.2 — Session management with refresh tokens (FR-006)

- **Artifact:** Redis-backed `sessions:<sid>` keys; refresh token rotation on
  every use.
- **Acceptance criteria:**
  - Refresh token reuse (same `jti` used twice) revokes the entire token
    family for that user (token-theft detection; mitigates R-001).
  - Session list endpoint `GET /v1/sessions` returns active sessions with
    `device`, `ip`, `last_seen`; revocation via `DELETE /v1/sessions/{id}`.
  - **Token revocation edge case:** revoking a refresh token also invalidates
    associated access tokens within ≤ 60s via Redis pub/sub denylist consulted
    on every request.

### D3.3 — Cookie hardening (R-001 primary mitigation)

- **Artifact:** All session cookies set with `HttpOnly`, `Secure`,
  `SameSite=Lax`, `Path=/`, `__Host-` prefix; CSP header
  `default-src 'self'; script-src 'self'; object-src 'none';
  frame-ancestors 'none'; base-uri 'self'`.
- **Acceptance criteria:**
  - `Set-Cookie` headers verified by integration test asserting exact flag set.
  - CSP enforced (not report-only) in production config; report-uri configured
    to the audit pipeline.

---

## M4 — RBAC & Authorization

### D4.1 — Role and permission model (FR-004)

- **Artifact:** Roles: `user`, `moderator`, `admin`, `support`,
  `billing_read`. Permissions are dotted strings (e.g., `user.read`,
  `user.write`, `audit.read`); evaluation is `permission ∈ union(role.perms)`.
- **Acceptance criteria:**
  - 100% of HTTP routes registered with explicit `requiredPermission` metadata;
    a CI check fails the build if any route lacks it.
  - Admin can assign/revoke roles via `PATCH /v1/admin/users/{id}/roles`
    (audited).
  - `permission-deny` produces HTTP 403 with no information leakage about
    resource existence.

### D4.2 — Permission cache and invalidation

- **Artifact:** Per-user permission set cached in Redis (`perms:<uid>`, TTL
  10 min). On any role change, key is invalidated via `DEL` and a
  `perms:invalidated` pub/sub event.
- **Acceptance criteria:**
  - **Cache invalidation edge case:** revoking a role from an active user
    blocks the next authorised request within ≤ 2s end-to-end (measured by
    integration test).
  - Cache hit ratio ≥ 90% in steady-state load test (verifies NFR-001 path).

---

## M5 — Security Hardening (2FA, Rate Limit, Audit)

### D5.1 — Two-factor authentication (FR-007)

- **Artifact:** TOTP via `otplib` 12.x (RFC 6238, 30s step, SHA-1, 6 digits)
  with QR enrolment; recovery codes (10 single-use codes, 128-bit each,
  argon2id-hashed at rest).
- **Acceptance criteria:**
  - Enrolment requires re-entering current password (sudo mode, 5-min window).
  - **2FA recovery edge case:** lost-device flow consumes one recovery code,
    invalidates remaining sessions, and forces re-enrolment; recovery codes
    cannot be reused (single-use enforced atomically via SQL `UPDATE … WHERE
    used_at IS NULL RETURNING …`).
  - 2FA bypass attempt (skipping the `mfa_required` claim) returns 401 and
    emits `audit.mfa.bypass_attempt`.

### D5.2 — API rate limiting per user (FR-008)

- **Artifact:** Sliding-window log algorithm in Redis via Lua script; limits:
  10 req/min on `/auth/login`, 5 req/min on `/auth/password/reset-request`,
  300 req/min on authenticated routes.
- **Acceptance criteria:**
  - Returns HTTP 429 with `Retry-After` header (seconds, integer).
  - **Rate-limit bypass detection:** requests with rotating `X-Forwarded-For`
    headers from the same authenticated user collapse to a single bucket keyed
    by `user_id`, not IP. Verified by adversarial test in M7.D7.2.
  - Account lockout from D2.2 is enforced in addition to rate limiting
    (defence in depth; mitigates R-002).

### D5.3 — Audit logging (FR-009, R-004 secondary)

- **Artifact:** Append-only `audit_events` table with `prev_hash` column
  forming a hash chain (SHA-256 of canonicalised prior row + current row).
- **Acceptance criteria:**
  - **Tamper-evidence edge case:** modifying any historical row fails the
    `audit-verify` cron job (runs hourly) within 1 cycle; alert fires to
    PagerDuty.
  - Captured events: `user.registered`, `login.success`, `login.failure`,
    `password.reset.requested`, `password.reset.completed`, `mfa.enrolled`,
    `mfa.bypass_attempt`, `role.assigned`, `role.revoked`, `oauth.linked`,
    `account.deactivated`, `admin.action`.
  - Each event row includes `actor_id`, `target_id`, `ip`, `user_agent`,
    `request_id`, `created_at` (UTC, microsecond precision).

---

## M6 — Admin Dashboard & Lifecycle

### D6.1 — User profile management (FR-010)

- **Artifact:** `GET/PATCH /v1/users/me`, `GET /v1/users/me/sessions`,
  `POST /v1/users/me/export` (GDPR Article 20 data export, returns a signed
  S3 URL valid 24h).
- **Acceptance criteria:**
  - Profile updates re-encrypt PII fields on write via D1.2 path.
  - Export JSON includes all PII, sessions, and audit events for the user;
    verified by snapshot test.

### D6.2 — Admin dashboard for user management (FR-011)

- **Artifact:** Next.js 14 admin SPA at `/admin/*` served behind
  `permission=admin.access`; tables for users, roles, sessions, audit feed.
- **Acceptance criteria:**
  - All admin actions (user lookup, role change, force-logout, lock account)
    appear in audit log within 5s.
  - Dashboard enforces re-authentication (sudo mode) before destructive
    operations (delete user, mass role revoke).

### D6.3 — Account deactivation workflow (FR-012)

- **Artifact:** `POST /v1/users/me/deactivate` (soft delete + 30-day grace),
  `POST /v1/admin/users/{id}/deactivate` (immediate, admin-initiated).
- **Acceptance criteria:**
  - Soft delete sets `users.deactivated_at`; user cannot login but data is
    retained for 30 days.
  - **GDPR right-to-erasure:** after grace period a worker hard-deletes PII
    (overwrites encrypted columns with NULL, purges audit PII fields while
    retaining event metadata for compliance).
  - All active sessions and refresh tokens for the deactivated user revoked
    within 30s.

---

## M7 — NFR Gates, Compliance, GA Release

This milestone is purely verification and gating; no new feature work.

### D7.1 — Performance gate (NFR-001, NFR-002)

- **Tool:** k6 0.49 running against a 3-node staging cluster (4 vCPU / 8GiB
  each, Redis cluster mode, PostgreSQL with 100 max_connections).
- **Acceptance criteria:**
  - p95 latency for `/auth/login`, `/auth/refresh`, `/auth/verify-token`
    ≤ 200ms under 10,000 concurrent virtual users for a 15-min sustained load.
  - Error rate < 0.1%. Build blocked if exceeded.

### D7.2 — Security gate (NFR-003, R-001, R-002, R-004)

- **Tools:** OWASP ZAP 2.14 baseline scan; Semgrep `p/owasp-top-ten`;
  `npm audit --production`; custom adversarial suite for rate-limit bypass
  and token-theft scenarios.
- **Acceptance criteria:**
  - Zero High or Critical findings on OWASP Top 10 categories A01–A10 (2021).
  - Pen-test report from external vendor (one-time at GA) with no
    unmitigated High findings.

### D7.3 — Compliance gate (NFR-004, NFR-006, R-004)

- **Artifacts:** GDPR DPIA document, Data Processing Register, encryption
  inventory listing every PII column + transport channel.
- **Acceptance criteria:**
  - DPIA signed off by Data Protection Officer.
  - All PII columns confirmed encrypted at rest (D1.2) and all traffic on
    TLS 1.3 (D1.3); evidence stored in compliance evidence repository.

### D7.4 — Reliability gate (NFR-005)

- **Artifacts:** Three-AZ deployment on Kubernetes 1.29; PostgreSQL with
  streaming replication + Patroni; Redis Sentinel; PodDisruptionBudgets
  (`minAvailable: 2` on auth-api).
- **Acceptance criteria:**
  - Chaos test (kill one auth-api pod, one Redis replica, one Postgres
    replica in sequence) yields zero 5xx visible to clients.
  - SLO dashboard (Grafana) shows 99.9% availability over 30-day rolling
    window before GA sign-off. Error-budget burn alerts wired to PagerDuty.

---

## Dependency Graph

```
M1 ──► M2 ──► M3 ──► M5 ──► M6 ──► M7
        └──► M4 ──┘          ▲
                   └─────────┘
```

- M1 unblocks M2, M3, M4 (all need schema + secrets + TLS).
- M2 unblocks M3 (sessions need users) and M4 (RBAC binds to users).
- M3 + M4 unblock M5 (hardening sits on top of working auth + authz).
- M6 requires M4 (admin permissions) and M5 (audit log to render).
- M7 requires M3, M5, M6 (full surface needed for end-to-end gates).

---

## Risk-to-Milestone Mapping

| Risk  | Primary mitigation         | Milestone(s)        |
|-------|----------------------------|---------------------|
| R-001 | HTTP-only cookies, CSP, refresh-token reuse detection | D3.2, D3.3 |
| R-002 | Per-user rate limit + account lockout + reset enumeration prevention | D2.2, D2.3, D5.2 |
| R-003 | OAuth provider downtime → email/password fallback + alert | D3.1 |
| R-004 | PII encryption, RBAC, tamper-evident audit, key rotation | D1.2, D1.3, D4.1, D5.3, D7.3 |

---

## NFR Enforcement Strategy

- **NFR-001 (≤200ms):** k6 load gate in D7.1; per-route p95 budget enforced in
  CI by replaying recorded production traces against staging.
- **NFR-002 (10K concurrent sessions):** same k6 scenario; Redis session store
  sized at 4 GiB with eviction policy `noeviction` to surface capacity issues.
- **NFR-003 (OWASP Top 10):** ZAP + Semgrep gates in D7.2; build blocked on
  High/Critical.
- **NFR-004 (GDPR):** D6.1 export, D6.3 erasure, D7.3 DPIA + Data Processing
  Register.
- **NFR-005 (99.9% uptime):** D7.4 multi-AZ + chaos test + SLO burn alerts.
- **NFR-006 (encrypt PII):** D1.2 (`pgcrypto` AEAD), D1.3 (TLS 1.3); inventory
  document audited in D7.3.

---

## Out-of-Scope Reaffirmation

The following are explicitly **not** delivered by this roadmap and must be
rejected if proposed mid-stream:

- Biometric authentication (fingerprint, face ID).
- Hardware security keys (WebAuthn / FIDO2 / U2F).
- Custom SSO protocol implementation (SAML, custom token formats).

Adding any of these requires a new spec amendment and a re-planning cycle;
they do not piggy-back onto M5 or M6.

---

## Success Criteria → Milestone Mapping

| Spec success criterion                             | Delivered by         |
|----------------------------------------------------|----------------------|
| All FR requirements implemented and tested         | M2..M6 (FR-001..FR-012) |
| OWASP compliance verified via security scan       | D7.2                 |
| Load testing confirms 10K concurrent sessions     | D7.1                 |
| OAuth2 flow works for Google and GitHub           | D3.1                 |
| Audit logs capture all auth events                | D5.3                 |

GA cutover requires all four D7.x gates to be green and signed off by
Engineering, Security, and the DPO.
