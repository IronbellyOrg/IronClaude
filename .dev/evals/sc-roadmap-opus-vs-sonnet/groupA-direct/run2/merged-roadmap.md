# Roadmap: User Authentication System

<!-- Provenance: produced by /sc:adversarial pipeline on 2026-05-22 -->
<!-- Base: Variant 1 (opus / default persona) -->
<!-- Merge date: 2026-05-22 -->

## Overview

<!-- Source: Base (V1, modified) — Change/Patch ID: A2/P-5 — adds schedule pointer -->

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
working integrated build before GA. This document is the output of the
`/sc:adversarial` debate-and-merge pipeline; see Provenance comments inline
for the contributing source of each section.

### Schedule

<!-- Source: Variant 2 (sonnet, default), Section "Milestone Overview" — merged per Change A2 + Patch P-5 — corrected for V1 ordering -->

- **Sequential total**: 15 weeks (M1 3w + M2 2w + M3 2w + M4 2w + M5 2w + M6 2w + M7 2w).
- **With M3 and M4 parallelized after M2**: ~13 weeks. M3 and M4 each need M2's
  auth foundation but do not depend on each other's outputs.
- **Critical path**: M1 → M2 → M3 → M5 → M6 → M7 (or M1 → M2 → M4 → M5 → M6 → M7
  depending on which parallel branch completes first).

---

## Milestone Map

<!-- Source: Base (V1, modified) — Change/Patch ID: A2 — adds Duration column -->

| ID | Milestone                                | Duration | Blocks    | Blocked by |
|----|------------------------------------------|----------|-----------|------------|
| M1 | Foundation & Data Layer                  | 3w       | M2,M3,M4  | —          |
| M2 | Core Authentication (Registration+Login) | 2w       | M3,M4,M5  | M1         |
| M3 | OAuth2 & Session Management              | 2w       | M5,M6     | M2         |
| M4 | RBAC & Authorization                     | 2w       | M5,M6     | M2         |
| M5 | Security Hardening (2FA, Rate Limit, Audit) | 2w    | M6        | M2,M3,M4   |
| M6 | Admin Dashboard & Lifecycle              | 2w       | M7        | M4,M5      |
| M7 | NFR Gates, Compliance, GA Release        | 2w       | —         | M3,M5,M6   |

**Critical path**: M1 → M2 → M3 → M5 → M6 → M7. With M3 // M4 parallelized after
M2, total wall-clock duration ≈ 13 weeks (see Schedule above).

---

## M1 — Foundation & Data Layer

<!-- Source: Base (V1, original) -->

Establish the persistent and ephemeral stores, the encryption baseline, and the
service skeleton. No auth surface is exposed in this milestone.

### D1.1 — Tech-stack lock-in and service scaffold

<!-- Source: Base (V1, modified) — Patch P-2 — adds v2 follow-up note -->

- **Requirements covered:** scaffolding for all FRs; precondition for NFR-005.
- **Artifact:** monorepo with `auth-api/`, `auth-worker/`, `auth-admin/` packages;
  Fastify 4.26 selected; Dockerfile (multi-stage, distroless base, non-root UID 10001).
- **Acceptance criteria:**
  - `docker compose up` brings PostgreSQL 15.4 + Redis 7.2 + auth-api healthy
    in <30s on a clean machine.
  - `npm audit --production` reports 0 high/critical vulnerabilities.
  - CI pipeline (GitHub Actions) runs lint+test+build in <8 min and is required
    on every PR.
- **v2 follow-up (Patch P-2):** Future migration to `pg_tde` or Vault Transit
  for true server-side / HSM-resident decryption is tracked as a v2 follow-up;
  M1 ships the per-request KMS unwrap pattern documented in D1.2.

### D1.2 — PostgreSQL schema with PII encryption

<!-- Source: Base (V1, modified) — Patches P-2, P-3, P-7 — per-request KMS unwrap + encryption inventory + email_lookup_hash sidecar -->

- **Requirements covered:** FR-001 (users table), FR-010 (profile), NFR-004,
  NFR-006, R-004.
- **Artifact:** `users`, `user_profiles`, `user_oauth_identities`,
  `sessions`, `refresh_tokens`, `roles`, `permissions`, `role_permissions`,
  `user_roles`, `audit_events`, `password_reset_tokens`, `mfa_secrets`,
  `pending_email_changes` (new — see Change A3), `user_consents` (new — see
  D4.3) tables.
- **Per-request KMS unwrap pattern (Patch P-2):** PII columns are encrypted via
  `pgp_sym_encrypt(plaintext, dek)`. The DEK is unwrapped from KMS *per
  request* by the application (`kms:GenerateDataKey` returns ciphertext-DEK +
  plaintext-DEK; ciphertext is stored as `dek_ciphertext` on the row;
  plaintext-DEK is held only in request-scoped memory and zeroed in a
  `try/finally` after the SQL transaction commits). The KMS *master key*
  never enters app memory; only ephemeral DEKs do.
- **`email_lookup_hash` sidecar (Patch P-7):** `users.email_lookup_hash BYTEA
  NOT NULL`, computed as `HMAC-SHA256(lookup_key, lower(email))` where
  `lookup_key` is a separate KMS-managed key (NOT the encryption DEK;
  `lookup_key` has its own rotation cadence — quarterly with re-hash backfill
  migration). Unique index `users_email_lookup_hash_uidx` on
  `(email_lookup_hash)`. The plaintext email remains encrypted in
  `users.email`. The same pattern applies to
  `pending_email_changes.new_email_lookup_hash`.
- **PII Encryption Inventory (Patch P-3):**

  | Table | Column | PII type | Encryption | Lookup hash sidecar |
  |-------|--------|----------|------------|----------------------|
  | users | email | direct | pgcrypto AEAD | email_lookup_hash (Patch P-7) |
  | users | phone | direct | pgcrypto AEAD | — |
  | users | full_name | direct | pgcrypto AEAD | — |
  | users | address | direct | pgcrypto AEAD | — |
  | user_profiles | display_name | direct | pgcrypto AEAD | — |
  | mfa_secrets | secret | secret | pgcrypto AEAD | — |
  | password_reset_tokens | (token only; no PII) | — | — | — |
  | email_verification_tokens | token, email_ref | indirect | pgcrypto AEAD | — |
  | pending_email_changes (Change A3) | new_email | direct | pgcrypto AEAD | new_email_lookup_hash |
  | user_consents (D4.3) | user_id, consent_type, policy_version | non-PII | — | — |
  | user_oauth_identities | provider_uid, email_from_provider | indirect | pgcrypto AEAD | — |
  | audit_events | actor_id, target_id, ip, user_agent | indirect | ip + user_agent stored as hashed values; user_id columns become `ERASED_<uuid>` after erasure | — |

- **Acceptance criteria:**
  - PII columns (`email`, `phone`, `full_name`, `address`) stored using
    `pgcrypto` AEAD (`pgp_sym_encrypt`) with a KMS-managed DEK rotated every 90
    days. Verified by `SELECT pg_column_size(email) > length('user@example.com')`
    on inserted rows.
  - `password_hash` column rejects values shorter than argon2id's encoded
    length (>= 96 bytes) via CHECK constraint.
  - Migrations applied with `node-pg-migrate` 7.x; rollback verified in CI.
  - Memory probe (`valgrind` or eBPF) on a soak-test pod shows no DEK
    plaintext bytes outside request lifetimes. `pg_log_statement = off` in
    production (verified via `SHOW log_statement`); query payloads containing
    keys are not logged.
  - Login path `EXPLAIN ANALYZE` shows an index scan on
    `users_email_lookup_hash_uidx` with cost <1ms at 10K users; p95 login
    latency ≤200ms under k6 NFR-001 load with `email_lookup_hash` in the query
    plan (NFR-001 met).

### D1.3 — Secrets management & TLS

<!-- Source: Base (V1, modified) — Change A14 + Patch P-2 — adds nmap test, key residency note -->

- **Requirements covered:** NFR-006, R-001, R-004.
- **Artifact:** Vault (HashiCorp 1.15) or AWS Secrets Manager integration;
  TLS 1.3 only on ingress; HSTS `max-age=63072000; includeSubDomains; preload`.
- **Acceptance criteria:**
  - `testssl.sh` grade A+; no TLS 1.0/1.1/1.2 ciphers offered.
  - `nmap --script ssl-enum-ciphers -p 443 $HOST` enumerates ONLY TLS 1.3
    cipher suites (no TLS 1.0/1.1/1.2 entries); test scripted into the staging
    pre-deploy smoke suite (complementary to `testssl.sh` grade A+).
  - No secret value appears in any container env var dump (`docker inspect`)
    or in process listing (`/proc/<pid>/environ`).
  - Key rotation runbook executes end-to-end in <10 min in staging (sized for
    the PII Encryption Inventory enumerated in D1.2; expanded surface is
    accounted for in INV-017 follow-up).

---

## M2 — Core Authentication (Registration + Login)

<!-- Source: Base (V1, original) -->

### D2.1 — User registration with email verification (FR-001)

<!-- Source: Base (V1, modified) — Changes A9, A10 + Patch P-7 — disposable-email check, prune cron, email_lookup_hash lookup -->

- **Artifact:** `POST /v1/auth/register`, `GET /v1/auth/verify?token=…`,
  SendGrid template `tpl_register_verify_v1`.
- Cron `prune-unverified-users` runs daily at 03:00 UTC; deletes user rows
  where `email_verified_at IS NULL AND created_at < now() - INTERVAL '72
  hours' AND verification_token_expires_at < now() - INTERVAL '1 minute'` —
  the +1 min buffer respects V1's 24h ± 1 min verification token tolerance,
  preventing race per INV-012 (Patch-additional-7).
- **Acceptance criteria:**
  - Registration rejects emails failing RFC 5322; rejects passwords failing
    zxcvbn score >= 3 OR length < 12.
  - Registration rejects emails whose domain appears in the
    `disposable-email-domains` npm list (locked to version 1.0.x; refreshed by
    quarterly dependabot PR with regression-test sample — covers INV-006).
  - Insert path computes `email_lookup_hash` before INSERT; pre-insert query
    `SELECT 1 FROM users WHERE email_lookup_hash = $1` enforces uniqueness
    without decrypting any row (Patch P-7).
  - Verification token is 256-bit random, stored as SHA-256 hash, single-use,
    expiring in exactly 24h ± 1 min.
  - Re-sending verification is rate-limited to 3 per 24h per email.
  - On successful registration, `audit_events` row written with
    `event_type=user.registered`.

### D2.2 — Password storage and login (FR-002)

<!-- Source: Base (V1, modified) — Patch P-7 — email lookup via hash sidecar -->

- **Artifact:** `POST /v1/auth/login` issuing JWT (HS256 disallowed; RS256 with
  rotating 4096-bit RSA key pair) + refresh token cookie.
- **Acceptance criteria:**
  - Passwords hashed with argon2id (m=65536, t=3, p=4); verified by inspecting
    `password_hash` prefix `$argon2id$v=19$m=65536,t=3,p=4$…`.
  - Access token TTL = 15 min; refresh token TTL = 30 days; both claims
    include `iss`, `aud`, `sub`, `jti`, `iat`, `exp`.
  - Login flow looks up user by `WHERE email_lookup_hash = $1`; loads
    encrypted `email` only for the candidate row; decrypts in app memory via
    Patch P-2 path; compares post-decrypt against submitted email to reject
    hash collisions (HMAC collision probability ~2^-256, but checked
    defensively).
  - Failed login increments `failed_attempts`; account locks for 15 min after
    5 consecutive failures (mitigates R-002).
  - Successful login emits `audit.login.success`; failure emits
    `audit.login.failure` with redacted credentials.

### D2.3 — Password reset (FR-005)

<!-- Source: Base (V1, original) -->

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

<!-- Source: Base (V1, original) -->

### D3.1 — OAuth2 integration (FR-003)

<!-- Source: Base (V1, modified) — Change A8 + Patch-additional-5 — adds /health/oauth + lagging-indicator note -->

- **Artifact:** Google + GitHub providers via `simple-oauth2` 5.x; PKCE
  enforced; state parameter is 256-bit CSRF token bound to a 10-min Redis key.
- `GET /health/oauth` — polls Google OIDC discovery + GitHub `/zen` endpoints
  every 60s; exposes `{google: up|down, github: up|down, last_check:
  ISO-8601}`. Discrepancy with the live-request fallback path is tolerated;
  the live-request fallback is authoritative for routing decisions per
  INV-020 (Patch-additional-5: on-call documentation explains the contract —
  `/health/oauth` is a lagging indicator at 60s cadence; the >3s live timeout
  is the source of truth).
- **Acceptance criteria:**
  - Authorization Code + PKCE flow only; implicit flow disabled in code paths.
  - Linking flow merges OAuth identity into existing `users` row by verified
    email; conflicts (different existing account) return 409 and audit event.
  - **Fallback (R-003):** when Google or GitHub OIDC discovery endpoint
    returns 5xx or times out > 3s, login falls back to email/password and an
    operator alert is emitted via PagerDuty webhook.
  - Smoke test in CI exercises both providers against staging credentials.

### D3.2 — Session management with refresh tokens (FR-006)

<!-- Source: Base (V1, modified) — Patch P-1 (TTL-keyed denylist replaces pub/sub) + Change A11 (session cap + concurrent-login) -->

- **Artifact:** Redis-backed `sessions:<sid>` keys; refresh token rotation on
  every use; Redis-backed denylist keyed `denylist:<jti>`.
- **TTL-keyed denylist (Patch P-1 — replaces V1's pub/sub denylist):**
  - Denylist entries are written via `SETEX denylist:<jti> <ttl> "1"` where
    `<ttl> = access-token-TTL + 60s grace`; checked synchronously on every
    authenticated request (≤5ms per check via Redis pipelining). Pub/sub
    fan-out is NOT used; subscribers are not required.
  - Per-pod in-memory cache of denylist entries with TTL ≤30s +
    clock-skew tolerance ≤5s + Sentinel-failover reconnect ≤10s.
  - **Revocation latency budget:** 5ms Redis check + 30s pod cache TTL + 5s
    clock skew + 10s Sentinel reconnect ≈ ≤50s ≤ 60s claim (10s margin).
    Resolves INV-001 + INV-009 + INV-022.
  - Sentinel failover preserves keys via AOF persistence (`appendonly yes;
    appendfsync everysec`). Chaos test in D7.4 verifies no in-flight `SETEX`
    is lost during primary kill.
- **Acceptance criteria:**
  - Refresh token reuse (same `jti` used twice) revokes the entire token
    family for that user (token-theft detection; mitigates R-001).
  - Session list endpoint `GET /v1/sessions` returns active sessions with
    `device`, `ip`, `last_seen`; revocation via `DELETE /v1/sessions/{id}`.
  - **Token revocation edge case:** revoking a refresh token also invalidates
    associated access tokens within ≤ 60s via the TTL-keyed denylist
    consulted on every request (per budget above).
  - **Session cap (Change A11):** 50 active refresh tokens per user; on
    creation of 51st, oldest is revoked AND its associated access-token `jti`
    is published to the denylist (binds eviction → revocation invariant —
    patches INV-003 / Patch-additional-6).
  - **Concurrent-login detection (Change A11):** if a login from a new device
    IP occurs within 60s of a prior login, the older refresh token is
    invalidated and the user is notified via SendGrid.

### D3.3 — Cookie hardening (R-001 primary mitigation)

<!-- Source: Base (V1, modified) — Patch-additional-1 — admin subdomain guard -->

- **Artifact:** All session cookies set with `HttpOnly`, `Secure`,
  `SameSite=Lax`, `Path=/`, `__Host-` prefix; CSP header
  `default-src 'self'; script-src 'self'; object-src 'none';
  frame-ancestors 'none'; base-uri 'self'`.
- **Acceptance criteria:**
  - `Set-Cookie` headers verified by integration test asserting exact flag set.
  - CSP enforced (not report-only) in production config; report-uri configured
    to the audit pipeline.
  - **Admin subdomain guard (Patch-additional-1, INV-007):** `__Host-` prefix
    REQUIRES Secure + Path=/ + no Domain attribute. Admin SPA (D6.2) MUST be
    served on the SAME registrable domain (e.g., `example.com/admin/`), NOT a
    subdomain (`admin.example.com`), else `__Host-` cookies are not sent.
    Deployment runbook validates the constraint pre-cutover. See also D7.4
    deployment guard.

---

## M4 — RBAC & Authorization

<!-- Source: Base (V1, original) -->

### D4.1 — Role and permission model (FR-004)

<!-- Source: Base (V1, modified) — Patch-additional-3 — unverified_user empty-role default -->

- **Artifact:** Roles: `user`, `moderator`, `admin`, `support`,
  `billing_read`. Permissions are dotted strings (e.g., `user.read`,
  `user.write`, `audit.read`); evaluation is `permission ∈ union(role.perms)`.
- Custom-role extension: `POST /admin/roles` allows runtime creation of
  additional roles beyond the 5-role default (audited).
- **Unverified-user role (Patch-additional-3, INV-013):** newly-created users
  in the 72-hour verification window receive the `unverified_user` role with
  permissions = {`user.profile.read.own`, `user.profile.complete-verification`}.
  Full `user` role is granted on `email_verified_at` set.
- **Acceptance criteria:**
  - 100% of HTTP routes registered with explicit `requiredPermission` metadata;
    a CI check fails the build if any route lacks it.
  - Admin can assign/revoke roles via `PATCH /v1/admin/users/{id}/roles`
    (audited).
  - `permission-deny` produces HTTP 403 with no information leakage about
    resource existence.

### D4.2 — Permission cache and invalidation

<!-- Source: Base (V1, original) -->

- **Artifact:** Per-user permission set cached in Redis (`perms:<uid>`, TTL
  10 min). On any role change, key is invalidated via `DEL` and a
  `perms:invalidated` pub/sub event (this pub/sub fan-out is per-user-id
  cache invalidation only, NOT the access-token denylist — denylist uses
  TTL-keyed entries per Patch P-1).
- **Acceptance criteria:**
  - **Cache invalidation edge case:** revoking a role from an active user
    blocks the next authorised request within ≤ 2s end-to-end (measured by
    integration test).
  - Cache hit ratio ≥ 90% in steady-state load test (verifies NFR-001 path).

### D4.3 — Consent ledger

<!-- Source: Variant 2 (sonnet, default), Section D5.3 user_consents — merged per Change A4 -->

- **Artifact:** `user_consents` table with `{user_id, consent_type,
  policy_version, granted_at, revoked_at}`. Registration writes a consent
  row for privacy policy + ToS acceptance.
- **Acceptance criteria:**
  - Each consent row carries `policy_version` so that policy changes can be
    detected and re-consent solicited.
  - Consent revocation is visible in audit log via D5.3
    (`audit.consent.revoked`).
  - `user_consents` is enumerated in the D1.2 PII Encryption Inventory
    (Patch P-3) — `user_id` and `consent_type` are non-PII metadata, so no
    pgcrypto encryption is required, but the table is in scope for the
    plaintext-PII grep CI test in D7.2.
- **Rationale:** GDPR Article 7 requires demonstrable consent with policy
  versioning.

---

## M5 — Security Hardening (2FA, Rate Limit, Audit)

<!-- Source: Base (V1, original) -->

### D5.1 — Two-factor authentication (FR-007)

<!-- Source: Base (V1, original) -->

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

<!-- Source: Base (V1, modified) — Change A6 + Patch P-8 + Patch-additional-2 — burst-block, allowlist, lockout composition -->

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
  - **Burst-detection (Change A6):** IP exceeding 1000 req/min across all
    rate-limit buckets is auto-blocked for 1 hour; alert fired via PagerDuty
    webhook within 5 seconds.
  - **Burst-block allowlist (Patch P-8, INV-008):** burst-block exempts IPs
    listed in `RATE_LIMIT_IP_ALLOWLIST` (env var, CIDR-supporting; enterprise
    NAT egress IPs registered via support ticket). Allowlisted IPs are still
    subject to per-account lockout and per-route rate limits — only the
    IP-wide auto-block is bypassed. Allowlist is loaded at boot and reloaded
    on SIGHUP; audit log captures every allowlist change.
  - **Lockout × burst-block composition (Patch-additional-2, INV-011):**
    account lockout (15 min from D2.2) and IP burst-block (1 hour) are
    evaluated independently. The user-visible block time is
    `max(account_lockout_remaining, ip_burst_block_remaining)`. Both
    controls fire `audit.lockout` / `audit.ip_burst_block` events.

### D5.3 — Audit logging (FR-009, R-004 secondary)

<!-- Source: Base (V1, modified) — Change A7 + Patches P-4, P-6 + Patch-additional-4 — GRANT, single-writer queue, DBA runbook, genesis row -->

- **Artifact:** Append-only `audit_events` table with `prev_hash` column
  forming a hash chain (SHA-256 of canonicalised prior row + current row).
- **Hash-chain append serialization (Patch P-4):** A per-cluster Postgres
  advisory lock (`pg_advisory_xact_lock('audit_events'::regclass::oid)`) is
  acquired at the start of each `INSERT INTO audit_events` transaction.
  Concurrent writers serialize on the lock; throughput ≥1000 inserts/sec
  sustained per the D7.1 perf gate. Alternative: dedicated audit-writer
  worker consuming from a Redis stream — documented as v2 path. Resolves
  INV-004.
- **DB GRANT restriction (Change A7):** DB role `auth_app` has only `INSERT`
  and `SELECT` privileges on `audit_events`; `UPDATE` and `DELETE` are
  revoked. Schema migration includes
  `REVOKE UPDATE, DELETE ON audit_events FROM auth_app`.
- **DBA repair runbook (Patches P-4 / P-6, INV-019):** When the hourly
  `audit-verify` cron flags chain corruption (suspected race or tamper), DBA
  executes `audit-repair --from-checkpoint <last-good-row>` which (a) requires
  the DBA role since `auth_app` lacks UPDATE per Change A7, (b) replays event
  log from the previous hourly checkpoint, (c) recomputes `prev_hash` chain
  forward, (d) re-runs `audit-verify` to confirm green. SLA: investigation
  begins within 15 min of PagerDuty alert; chain restored within 60 min.
- **Genesis row (Patch-additional-4, INV-015):** First row (`row_id = 1`) has
  `prev_hash = '0000000000000000000000000000000000000000000000000000000000000000'`
  (32 zero bytes hex-encoded). `audit-verify` cron treats genesis row as
  valid by definition; for fresh deployments with empty `audit_events`, cron
  emits `audit.fresh-deployment` and returns success.
- **Acceptance criteria:**
  - **Tamper-evidence edge case:** modifying any historical row fails the
    `audit-verify` cron job (runs hourly) within 1 cycle; alert fires to
    PagerDuty.
  - Captured events: `user.registered`, `login.success`, `login.failure`,
    `password.reset.requested`, `password.reset.completed`, `mfa.enrolled`,
    `mfa.bypass_attempt`, `role.assigned`, `role.revoked`, `oauth.linked`,
    `account.deactivated`, `admin.action`, `consent.granted`,
    `consent.revoked`, `ip_burst_block`, `lockout`.
  - Each event row includes `actor_id`, `target_id`, `ip`, `user_agent`,
    `request_id`, `created_at` (UTC, microsecond precision).

---

## M6 — Admin Dashboard & Lifecycle

<!-- Source: Base (V1, original) -->

### D6.1 — User profile management (FR-010)

<!-- Source: Base (V1, modified) — Changes A3, A12 — email-change re-verification, avatar upload -->

- **Artifact:** `GET/PATCH /v1/users/me`, `GET /v1/users/me/sessions`,
  `POST /v1/users/me/export` (GDPR Article 20 data export, returns a signed
  S3 URL valid 24h).
- **Email-change re-verification (Change A3):** `PATCH /v1/users/me/email`
  accepts a new email; sends verification to the new address via the D2.1
  path; the original email remains the active account identifier until
  verification completes. The new email is stored in `pending_email_changes`
  (encrypted per Patch P-3; `new_email_lookup_hash` sidecar per Patch P-7)
  until consumed. Patches V1 silence on account-takeover via email change.
- **Avatar upload (Change A12):** `POST /v1/users/me/avatar`: multipart,
  ≤2 MiB, content-type allowlist {image/jpeg, image/png, image/webp},
  server-side magic-byte verification, Sharp v0.33 resize to 128×128 and
  256×256, stored in S3 with `Cache-Control: max-age=31536000, immutable`.
- **Acceptance criteria:**
  - Profile updates re-encrypt PII fields on write via the D1.2 path.
  - Email change sends verification to the new address; the old email
    remains active until verification completes; the pending row is purged
    after consumption or 24h expiry.
  - Avatar upload rejects files > 2 MiB with HTTP 413; non-image / disallowed
    MIME types rejected with HTTP 415; magic-byte mismatch rejected with 415.
  - Export JSON includes all PII, sessions, and audit events for the user;
    verified by snapshot test.

### D6.2 — Admin dashboard for user management (FR-011)

<!-- Source: Base (V1, original) -->

- **Artifact:** Next.js 14 admin SPA at `/admin/*` served behind
  `permission=admin.access`; tables for users, roles, sessions, audit feed.
  (Per Patch-additional-1 in D3.3, MUST share the registrable domain — no
  `admin.example.com` subdomain.)
- **Acceptance criteria:**
  - All admin actions (user lookup, role change, force-logout, lock account)
    appear in audit log within 5s.
  - Dashboard enforces re-authentication (sudo mode) before destructive
    operations (delete user, mass role revoke).

### D6.3 — Account deactivation workflow (FR-012)

<!-- Source: Base (V1, modified) — Change A5 + Patch P-9 — erased_<uuid> anonymization + idempotency guard -->

- **Artifact:** `POST /v1/users/me/deactivate` (soft delete + 30-day grace),
  `POST /v1/admin/users/{id}/deactivate` (immediate, admin-initiated).
- **Acceptance criteria:**
  - Soft delete sets `users.deactivated_at`; user cannot login but data is
    retained for 30 days.
  - **GDPR right-to-erasure (Change A5):** after the grace period a worker
    replaces `email` with `erased_<uuid>@erased.local`, replaces
    `display_name`/`phone`/`address` with NULL, and retains
    `actor_user_id = ERASED_<uuid>` in `audit_events` for compliance-mandated
    event-actor traceability. Preserves audit hash-chain integrity that the
    prior "overwrite with NULL" pattern would have broken.
  - **Idempotency guard (Patch P-9, INV-016):** the erasure path is gated by
    `WHERE users.deactivated_at IS NOT NULL AND users.deactivated_at < now()
    - INTERVAL '30 days' AND users.erased_at IS NULL` and atomically sets
    `users.erased_at = now()` in the same transaction as the anonymization
    writes. Repeated invocation of `erase-expired-deactivated` cron observes
    `users.erased_at IS NOT NULL` and skips the row; chain references to
    `actor_user_id = ERASED_<uuid>` remain stable.
  - All active sessions and refresh tokens for the deactivated user revoked
    within 30s (the access-token `jti` for each is published to the
    TTL-keyed denylist per Patch P-1).

---

## M7 — NFR Gates, Compliance, GA Release

<!-- Source: Base (V1, original) -->

This milestone is purely verification and gating; no new feature work.

### D7.1 — Performance gate (NFR-001, NFR-002)

<!-- Source: Base (V1, original) -->

- **Tool:** k6 0.49 running against a 3-node staging cluster (4 vCPU / 8GiB
  each, Redis cluster mode, PostgreSQL with 100 max_connections).
- **Acceptance criteria:**
  - p95 latency for `/auth/login`, `/auth/refresh`, `/auth/verify-token`
    ≤ 200ms under 10,000 concurrent virtual users for a 15-min sustained load.
  - Error rate < 0.1%. Build blocked if exceeded.
  - Email-lookup queries use the `email_lookup_hash` index path per Patch
    P-7; latency budget includes this index scan.

### D7.2 — Security gate (NFR-003, R-001, R-002, R-004)

<!-- Source: Base (V1, modified) — Patch P-3 — plaintext-email grep CI test -->

- **Tools:** OWASP ZAP 2.14 baseline scan; Semgrep `p/owasp-top-ten`;
  `npm audit --production`; custom adversarial suite for rate-limit bypass
  and token-theft scenarios.
- **Acceptance criteria:**
  - Zero High or Critical findings on OWASP Top 10 categories A01–A10 (2021).
  - Pen-test report from external vendor (one-time at GA) with no
    unmitigated High findings.
  - **Plaintext-PII grep CI test (Patch P-3, INV-002/INV-005/INV-024):** post
    integration-test-suite, run `pg_dump --column-inserts --data-only` and
    grep the dump for any line matching
    `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$` outside the
    `audit_events.target_id` column (which legitimately contains
    `erased_<uuid>@erased.local` strings). Any match fails the build with the
    offending table/column.

### D7.3 — Compliance gate (NFR-004, NFR-006, R-004)

<!-- Source: Base (V1, modified) — Patch-additional-1 deployment-guard reference -->

- **Artifacts:** GDPR DPIA document, Data Processing Register, encryption
  inventory listing every PII column + transport channel (cross-references
  D1.2 PII Encryption Inventory).
- **Acceptance criteria:**
  - DPIA signed off by Data Protection Officer.
  - All PII columns confirmed encrypted at rest (D1.2) and all traffic on
    TLS 1.3 (D1.3); evidence stored in the compliance evidence repository.
  - **Deployment guard (Patch-additional-1):** pre-cutover runbook validates
    that the admin SPA is served on the same registrable domain as the
    auth-api (no `admin.example.com` subdomain), so `__Host-` cookies remain
    in scope (see D3.3).

### D7.4 — Reliability gate (NFR-005)

<!-- Source: Base (V1, modified) — Change A15 + Patch P-1 — Prometheus alerting + Sentinel chaos test -->

- **Artifacts:** Three-AZ deployment on Kubernetes 1.29; PostgreSQL with
  streaming replication + Patroni; Redis Sentinel; PodDisruptionBudgets
  (`minAvailable: 2` on auth-api).
- **Acceptance criteria:**
  - Chaos test (kill one auth-api pod, one Redis replica, one Postgres
    replica in sequence) yields zero 5xx visible to clients.
  - **Sentinel chaos test (Patch P-1):** the chaos sequence includes killing
    the Redis primary mid-revocation; verify that no in-flight
    `SETEX denylist:<jti> …` is lost (AOF + Sentinel promotion preserves the
    write) and that the denylist key is visible from the new primary within
    ≤10s.
  - SLO dashboard (Grafana) shows 99.9% availability over 30-day rolling
    window before GA sign-off. Error-budget burn alerts wired to PagerDuty.
  - **Prometheus alerting (Change A15):** Prometheus `/metrics` endpoint
    exposes `auth_login_total`, `auth_login_failures_total`,
    `auth_token_refresh_total`, `auth_active_sessions`,
    `auth_request_duration_seconds`. Alertmanager rules:
    - `auth_error_rate > 0.01` sustained 5 min → PagerDuty P2.
    - `auth_p99_latency > 1.0s` sustained 3 min → PagerDuty P2.
    - `auth_denylist_publish_lag_seconds > 30` sustained 1 min → PagerDuty
      P1 (binds to the ≤60s revocation invariant per Patch P-1).

---

## Dependency Graph

<!-- Source: Base (V1, modified) — Patch P-5 parallel-branch callout -->

```
M1 ──► M2 ──► M3 ──► M5 ──► M6 ──► M7
        └──► M4 ──┘          ▲
                   └─────────┘
```

- M1 unblocks M2, M3, M4 (all need schema + secrets + TLS).
- M2 unblocks M3 (sessions need users) and M4 (RBAC binds to users).
- **M3 and M4 can run in parallel after M2** (neither depends on the
  other's outputs); critical path collapses to whichever branch finishes
  later — ~13 weeks wall-clock with the parallel branch versus 15 weeks
  fully sequential.
- M3 + M4 unblock M5 (hardening sits on top of working auth + authz).
- M6 requires M4 (admin permissions) and M5 (audit log to render).
- M7 requires M3, M5, M6 (full surface needed for end-to-end gates).

---

## Risk-to-Milestone Mapping

<!-- Source: Base (V1, modified) — D-ref deltas: D4.3 consent + D5.2 burst-block -->

| Risk  | Primary mitigation         | Milestone(s)        |
|-------|----------------------------|---------------------|
| R-001 | HTTP-only cookies, CSP, refresh-token reuse detection, TTL-keyed denylist | D3.2, D3.3 |
| R-002 | Per-user rate limit + account lockout + reset enumeration prevention + IP burst-block | D2.2, D2.3, D5.2 |
| R-003 | OAuth provider downtime → email/password fallback + alert + /health/oauth | D3.1 |
| R-004 | PII encryption (inventory + per-request KMS unwrap + email_lookup_hash), RBAC, tamper-evident audit (hash chain + GRANT + advisory lock), consent ledger, key rotation | D1.2, D1.3, D4.1, D4.3, D5.3, D7.3 |

---

## NFR Enforcement Strategy

<!-- Source: Base (V1, modified) — augments NFR-001 with denylist budget reference -->

- **NFR-001 (≤200ms):** k6 load gate in D7.1; per-route p95 budget enforced in
  CI by replaying recorded production traces against staging. Email-lookup
  queries use the `email_lookup_hash` index (Patch P-7) to stay within
  budget. The ≤60s revocation budget for denylist propagation (Patch P-1) is
  separately monitored via `auth_denylist_publish_lag_seconds` (D7.4).
- **NFR-002 (10K concurrent sessions):** same k6 scenario; Redis session store
  sized at 4 GiB with eviction policy `noeviction` to surface capacity issues.
- **NFR-003 (OWASP Top 10):** ZAP + Semgrep gates in D7.2; build blocked on
  High/Critical; plaintext-PII grep CI test (Patch P-3).
- **NFR-004 (GDPR):** D6.1 export, D6.3 erasure, D7.3 DPIA + Data Processing
  Register; D4.3 consent ledger; D6.1 email-change re-verification.
- **NFR-005 (99.9% uptime):** D7.4 multi-AZ + chaos test (incl. Redis-primary
  kill mid-revocation) + SLO burn alerts + Prometheus alerting rules.
- **NFR-006 (encrypt PII):** D1.2 (`pgcrypto` AEAD + per-request KMS unwrap +
  PII Encryption Inventory), D1.3 (TLS 1.3 + nmap acceptance test);
  inventory document audited in D7.3.

---

## Out-of-Scope Reaffirmation

<!-- Source: Base (V1, original) -->

The following are explicitly **not** delivered by this roadmap and must be
rejected if proposed mid-stream:

- Biometric authentication (fingerprint, face ID).
- Hardware security keys (WebAuthn / FIDO2 / U2F).
- Custom SSO protocol implementation (SAML, custom token formats).

Adding any of these requires a new spec amendment and a re-planning cycle;
they do not piggy-back onto M5 or M6.

---

## FR Coverage Matrix

<!-- Source: Variant 2 (sonnet, default), Section "FR Coverage Matrix" — merged per Change A1 — references back-populated to merged D{M}.{N} -->

| FR | Milestone | Deliverable | Key Acceptance Test |
|----|-----------|-------------|---------------------|
| FR-001 | M2 | D2.1 | Registration → 201; unverified → 403; verify link → 302; disposable-email rejected; prune cron at 72h+1min |
| FR-002 | M2 | D2.2 | Login → 200 + JWT (RS256) + refresh cookie; wrong creds → 401; email_lookup_hash index path used |
| FR-003 | M3 | D3.1 | Google/GitHub OAuth E2E; provider-down → fallback within 3s; /health/oauth available |
| FR-004 | M4 | D4.1 | `requiredPermission` enforced on every route; cache invalidation ≤2s; unverified_user role default |
| FR-005 | M2 | D2.3 | Reset request → 202 always; token single-use; password change → all refresh tokens revoked |
| FR-006 | M3 | D3.2 | Token rotation; family revocation on reuse; 50-session cap with eviction → denylist publish; ≤60s revocation budget |
| FR-007 | M5 | D5.1 | TOTP RFC 6238; 10 single-use recovery codes; bypass attempt → 401 + audit |
| FR-008 | M5 | D5.2 | Sliding-window limit; X-Forwarded-For collapse; burst-block 1000/min → 1h with allowlist |
| FR-009 | M5 | D5.3 | Hash chain + advisory lock + INSERT-only GRANT; tamper detection ≤1h; DBA repair runbook |
| FR-010 | M6 | D6.1 | Profile CRUD; email-change re-verification via pending_email_changes; avatar ≤2MiB + Sharp resize |
| FR-011 | M6 | D6.2 | Admin SPA at /admin/* (same domain per __Host-); admin actions audited within 5s |
| FR-012 | M6 | D6.3 | Deactivate → sessions revoked within 30s; 30-day grace; idempotent erasure with erased_<uuid> |

---

## Technology & Version Pinning

<!-- Source: Variant 2 (sonnet, default), Section "Technology & Version Pinning" — merged per Change A13 — V1-specific entries appended -->

| Component | Version | Rationale |
|-----------|---------|-----------|
| PostgreSQL | 15.4 | Spec dependency; pgcrypto AEAD + advisory locks |
| Redis | 7.2 | Spec dependency; Lua scripting + AOF persistence for denylist durability |
| SendGrid | API v3 | Spec dependency; transactional templates |
| Docker | 24+ + Compose v2 | Spec dependency; multi-stage distroless build |
| Kubernetes | 1.29 | NFR-005 multi-AZ topology with PodDisruptionBudgets |
| Patroni | 3.x | PostgreSQL streaming replication + automated failover |
| Redis Sentinel | bundled w/ Redis 7.2 | Primary failover; AOF preserves denylist keys |
| Node.js | 20 LTS | Long-term support through October 2026 |
| Fastify | 4.26 | Low overhead per request; schema validation |
| Argon2id | via `argon2` npm | m=65536, t=3, p=4; OWASP-recommended password hash |
| `jsonwebtoken` | 9.x (or `python-jose` 3.x) | JWT mint/verify with RS256 |
| `simple-oauth2` | 5.x | OAuth Authorization Code + PKCE (D3.1) |
| `otplib` | 12.x | TOTP RFC 6238 (D5.1) — chosen over `otpauth` since V1 is base |
| `pgcrypto` | built-in PG 15.4 | AEAD for PII (D1.2) |
| HashiCorp Vault | 1.15 | KMS / secrets management (D1.3) |
| `node-pg-migrate` | 7.x | Schema migrations with rollback (D1.2) |
| Semgrep | `p/owasp-top-ten` ruleset | Static analysis in D7.2 |
| OWASP ZAP | 2.14 | Baseline scan in D7.2 |
| k6 | 0.49 | NFR-001 / NFR-002 load gates (D7.1) |
| Sharp | v0.33 | Avatar resize (D6.1) |
| Prometheus + prom-client | 2.x / 15.x | Metrics + alerting for NFR-005 (D7.4) |
| `disposable-email-domains` | 1.0.x | Registration domain check (D2.1) |
| Keycloak | NOT USED | In-house RBAC per spec (D4.1) |

---

## Success Criteria → Milestone Mapping

<!-- Source: Base (V1, original) -->

| Spec success criterion                             | Delivered by         |
|----------------------------------------------------|----------------------|
| All FR requirements implemented and tested         | M2..M6 (FR-001..FR-012) — see FR Coverage Matrix |
| OWASP compliance verified via security scan        | D7.2                 |
| Load testing confirms 10K concurrent sessions      | D7.1                 |
| OAuth2 flow works for Google and GitHub            | D3.1                 |
| Audit logs capture all auth events                 | D5.3                 |

---

## Merged Postscript

<!-- Source: Merge — reaffirmation of GA cutover gates -->

GA cutover requires all four D7.x gates to be green and signed off:

- **D7.1 — Performance gate**: signed off by Engineering.
- **D7.2 — Security gate**: signed off by Security (incl. plaintext-PII grep
  pass and external pen-test).
- **D7.3 — Compliance gate**: signed off by the Data Protection Officer
  (DPIA + Data Processing Register + admin-subdomain deployment guard).
- **D7.4 — Reliability gate**: signed off by Engineering (chaos test incl.
  Redis-primary mid-revocation kill + 30-day SLO window + Prometheus
  alerting rules).

This document is the output of the `/sc:adversarial` debate-and-merge
pipeline on 2026-05-22; see inline Provenance comments for the contributing
source of each section. Convergence achieved: all 9 HIGH UNADDRESSED
invariant findings (INV-001, INV-002, INV-005, INV-009, INV-010, INV-021,
INV-022, INV-023, INV-024) are patched.
