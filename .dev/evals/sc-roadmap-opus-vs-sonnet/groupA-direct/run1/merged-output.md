<!-- Provenance: merged via /sc:adversarial on 2026-05-22 -->
<!-- Base: Variant 1 (opus/default) -->
<!-- Merged: 10 V2 strength incorporations + 9 HIGH-severity invariant resolutions = 19 changes -->

# Roadmap: User Authentication System

**Source Spec:** `tests/sc-roadmap/fixtures/sample_spec.md`
**Variant:** Merged (base = V1 opus/default; incorporations from V2 sonnet/default)
**Generated:** 2026-05-22
**Target Release:** v1.0 (Production GA)

---

## Executive Summary

<!-- Source: Base (original) -->

This roadmap delivers a production-grade user authentication system supporting OAuth2, JWT, RBAC, 2FA, and full audit compliance. The work is decomposed into **five sequential milestones** spanning roughly **14 weeks** of focused engineering, with a parallel cross-cutting security and observability track running throughout.

The strategy prioritizes **a hard security foundation first** (M1) — schema, crypto, password handling — before layering interactive flows (M2: login + JWT), federated identity (M3: OAuth2 + 2FA), governance (M4: RBAC + admin + audit), and finally hardening + scale validation (M5). This sequencing is deliberate: every later milestone depends on the cryptographic primitives, token model, and audit hooks established in M1–M2, so we refuse to ship feature-rich-but-fragile slices.

**Opinionated technology choices** (committed in this roadmap, justified inline):

- **Language/framework:** Python 3.12 + FastAPI (async I/O for NFR-001 latency budget; mature OAuth + JWT libraries)
- **JWT library:** `python-jose[cryptography]` with RS256 (asymmetric — lets us rotate signing keys without invalidating verifier secrets across services)
- **Password hashing:** Argon2id via `argon2-cffi` (OWASP 2025 recommendation; bcrypt is acceptable but Argon2 is the forward choice)
- **OAuth client:** `authlib` (battle-tested, supports both Google and GitHub OIDC/OAuth2 flows out of the box)
- **2FA:** TOTP (RFC 6238) via `pyotp` + recovery codes; SMS deliberately excluded due to SS7 risk
- **Session store:** Redis 7 with key-prefix isolation per tenant
- **Rate limiting:** Redis-backed token bucket via `slowapi` (chosen over fixed-window for burst tolerance)
- **Audit sink:** PostgreSQL append-only `auth_events` table + async forwarding to an external SIEM-compatible JSONL stream
- **Observability:** OpenTelemetry SDK → OTLP collector → Grafana/Tempo/Loki stack

**Out-of-scope items** (biometric auth, hardware keys, custom SSO) are honored — no work in this roadmap touches them, and we explicitly carve interface points so a future v2 can plug them in.

**Risk posture:** All four source risks (R-001 through R-004) are addressed in the earliest milestone where the relevant attack surface first exists, never deferred to "hardening later."

### Glossary — Operational Definitions

<!-- Source: invariant-probe INV-009 resolution per refactor-plan #B5 -->

- **Concurrent session** (NFR-002 measurement unit): a refresh-token family that is active (not expired, not revoked) in Redis. Equivalent operationally to: one logged-in user device. Excludes: short-lived access tokens (which may number 10K-30K simultaneously for a 10K-session user base); excludes HTTP connections (which the load balancer manages). The 10K-concurrent-session target therefore corresponds to ~10K active refresh-token families and ~10K-30K live access tokens. This definition is the basis for Redis sizing, soak-test load patterns (D5.1), and the Redis Cluster scaling threshold (Cross-Cutting / Performance).

---

## Milestone Overview

<!-- Source: Base (original) -->

| ID | Title | Duration | Primary FR/NFR Coverage |
|----|-------|----------|-------------------------|
| M1 | Foundation: Identity Core & Crypto Substrate | 3 weeks | FR-001, FR-005, NFR-003, NFR-006, R-004 |
| M2 | Interactive Auth: Login, JWT, Sessions | 3 weeks | FR-002, FR-006, FR-008, NFR-001, R-001, R-002 |
| M3 | Federated Identity & 2FA | 3 weeks | FR-003, FR-007, R-003 |
| M4 | Governance: RBAC, Profile, Admin, Audit | 3 weeks | FR-004, FR-009, FR-010, FR-011, FR-012, NFR-004 |
| M5 | Hardening, Load Validation, GA Readiness | 2 weeks | NFR-002, NFR-005, all NFRs verified |

**Total:** 14 weeks (~7 two-week sprints) with one engineer on the critical path; halve with two engineers paired on independent slices (M3 federated + M4 governance can overlap once M2 ships).

---

## M1: Foundation — Identity Core & Crypto Substrate

<!-- Source: Base (original) -->

### Goal / Outcome

Establish the unshakeable bottom layer: the user table, password storage that meets OWASP 2025, email verification, password reset, encryption-at-rest for PII, and the audit table schema. **No interactive auth endpoint ships in M1** — the deliverable is a verified substrate, not a feature.

### Deliverables

- **D1.1** (FR-001): User registration endpoint `POST /auth/register` with:
  - Email format + disposable-domain validation
  - Argon2id password hash (m=64MB, t=3, p=4 — calibrated to ~250ms on production hardware)
  - Verification token (32-byte CSPRNG, SHA-256 stored, 24-hour TTL)
  - SendGrid template integration with bounce/complaint webhook handling
- **D1.2** (FR-005): Password reset flow `POST /auth/password-reset/request` + `POST /auth/password-reset/confirm` sharing the same token primitive as D1.1; rate-limited at 3/hour/email
- **D1.3** (NFR-006): Encryption-at-rest via PostgreSQL `pgcrypto` for sensitive columns (email is searchable so we use deterministic encryption with a separate column-key; PII fields like name, phone use AES-GCM via a KMS-managed key)
- **D1.4** (NFR-006): TLS 1.3-only ingress (nginx config + HSTS preload), mTLS between API and Redis
- **D1.5** (FR-009 scaffolding): `auth_events` append-only table + `AuditLogger` service interface, called from D1.1 and D1.2 (registration, verification, reset events captured day one)
  <!-- Source: Variant 2 (sonnet/default) D3.9 — merged per refactor-plan #A3 -->
  - **DB role separation:** application connects as `auth_app` role granted only INSERT and SELECT on `auth_events`; UPDATE and DELETE grants are reserved for a separate `auth_admin` role used exclusively by retention/archive jobs. No grant of REFERENCES on this table. Verified by an integration test attempting UPDATE/DELETE from the application role and asserting permission denied.
  <!-- Source: Variant 2 (sonnet/default) D3.9 — merged per refactor-plan #A9 -->
  - **Table partitioning:** PostgreSQL range partitioning on `occurred_at` (monthly partitions); a background job creates next-month partition 7 days before month-end; partitions older than 7 years (retention policy) are detached and archived to S3 Glacier. Partition pruning makes the M4 audit-query API (D4.7) feasible at 10M+ event scale.
  <!-- Source: invariant-probe INV-001 resolution per refactor-plan #B1 -->
  - **Schema migration policy:** `auth_events` schema changes (new columns, new event types) executed exclusively by the `auth_admin` DB role during a scheduled maintenance window; `ALTER TABLE` operations are blue/green where the table is large, using PostgreSQL native `ADD COLUMN ... DEFAULT NULL` (no rewrite). Every milestone that introduces new event types includes a migration plan in its acceptance criteria.
  <!-- Source: invariant-probe INV-017 resolution per refactor-plan #B9 -->
  - **Audit event-type taxonomy (complete v1 enumeration):** `registered`, `email_verified`, `email_verify_failed`, `login_success`, `login_failure`, `logout`, `refresh_rotated`, `refresh_reuse_detected`, `account_locked`, `account_unlocked`, `password_reset_requested`, `password_reset_completed`, `password_reset_failed`, `password_changed`, `oauth_login_success`, `oauth_login_failed`, `oauth_account_linked`, `oauth_account_unlinked`, `oauth_provider_unreachable`, `totp_enrolled`, `totp_disabled`, `totp_verified`, `totp_failed`, `recovery_codes_generated`, `recovery_codes_regenerated`, `recovery_code_used`, `trusted_device_added`, `trusted_device_removed`, `role_assigned`, `role_removed`, `permission_change_propagated`, `account_deactivated`, `account_reactivated`, `account_purged`, `admin_action` (for all admin dashboard mutations with `actor_id`, `target_id`, `action`, `before`, `after`). The acceptance test in D5.8 verifies every event type has at least one E2E test that produces it. Adding a new event type in any future milestone requires adding the event to this taxonomy AND a migration per the schema-migration policy above.
- **D1.6** (NFR-003): Initial OWASP Top 10 baseline — A01 (broken access control test harness), A02 (crypto choices documented in `docs/security/crypto.md`), A03 (input validation via Pydantic v2 strict mode), A07 (the auth flow itself)
- **D1.7** (R-004 mitigation): GDPR data-subject access scaffolding — every PII column tagged with `data_classification` comment for the future export/delete pipeline

### Dependencies

- **External:** PostgreSQL 15+ provisioned, SendGrid account + verified sender domain, KMS (AWS KMS or HashiCorp Vault) for the column-encryption key
- **Internal:** None — this is the root milestone

### Acceptance Criteria

- [ ] `pytest tests/auth/test_registration.py` — all green, ≥95% line coverage on `auth/registration.py`
- [ ] Argon2 parameters benchmarked: registration latency 250ms ± 50ms on a c6i.large equivalent
- [ ] Email verification end-to-end test using a SendGrid sandbox key passes in CI
- [ ] `pgcrypto` round-trip verified: cold-restart Postgres, confirm encrypted columns decrypt with rotated KMS key reference
- [ ] OWASP ZAP baseline scan against the staging deploy returns zero High findings
- [ ] All five initial event types (`registered`, `email_verified`, `reset_requested`, `reset_completed`, `reset_failed`) appear in `auth_events` with the canonical schema documented in `docs/audit/schema.md`
- [ ] DB-role separation verified: integration test asserts UPDATE and DELETE from `auth_app` role return permission denied; only `auth_admin` can perform schema migrations
- [ ] Monthly partition created automatically 7 days before month-end (cron job verified in staging)

### Risks Addressed

- **R-004 (Data breach of PII):** D1.3 (encryption at rest), D1.4 (encryption in transit), D1.5 (audit trail with DB-role tamper resistance for forensic reconstruction)

### Estimated Effort

**3 weeks** (1.5 sprints) — heaviest week is D1.3 due to KMS integration and key-rotation testing.

---

## M2: Interactive Auth — Login, JWT, Sessions, Rate Limiting

<!-- Source: Base (original) -->

### Goal / Outcome

Ship the user-facing login experience: JWT issuance, refresh tokens, HTTP-only cookie delivery, session revocation, and per-user rate limiting. By end of M2, a user can register (M1) → log in (M2) → access a protected endpoint → log out → have their session genuinely killed.

### Deliverables

- **D2.1** (FR-002): `POST /auth/login` issuing:
  - **Access token:** JWT RS256, 15-minute TTL, claims `{sub, iat, exp, jti, roles: []}` (roles empty until M4)
  <!-- Source: Base (modified per refactor-plan #A7) — hybrid: 7-day rotation + 30-day family ceiling -->
  - **Refresh token:** Opaque 32-byte token, stored hashed in Redis with **7-day rolling TTL** rotated on each use (family-rotation pattern per IETF OAuth 2.0 Security BCP); the family has an **absolute lifetime ceiling of 30 days** after which the user must re-authenticate regardless of activity. Family revocation on reuse detection unchanged.
  - Cookies: `HttpOnly`, `Secure`, `SameSite=Lax` for access; `SameSite=Strict` for refresh; both with `__Host-` prefix
- **D2.2** (FR-006): `POST /auth/refresh` + `POST /auth/logout` with refresh-token rotation; logout revokes the entire refresh-token family and adds the access-token `jti` to a Redis bloom-filter denylist with TTL = access-token TTL
- **D2.3** (FR-006): Session listing endpoint `GET /auth/sessions` (foundation for "log out other devices" UX) and `DELETE /auth/sessions/{id}`
- **D2.4** (FR-008): Rate limiting middleware via `slowapi` + Redis:
  - Login: 5 attempts / 15 minutes / IP+email composite key
  - Refresh: 30 / hour / user
  - Password reset (M1 endpoint, now rate-limited): 3 / hour / email
  - All other auth endpoints: 60 / minute / user
  <!-- Source: invariant-probe INV-008 resolution per refactor-plan #B4 -->
  - **Rate-limit key strategy at Redis Cluster scale:** rate-limit keys use a hash tag `{user:<user_id>}` to force co-location of all per-user counters on a single shard, enabling atomic Lua-script execution of the token-bucket algorithm. IP-only rate limits (pre-auth) use `{ip:<bucket>}` where `<bucket>` is the /24 (IPv4) or /48 (IPv6) network. Clock-skew between API nodes is bounded by NTP (chrony with stratum ≤ 3); rate-limit calculations use the Redis server clock, not the API node's clock.
- **D2.5** (FR-002 + R-002): Account lockout
  <!-- Source: Base (modified per refactor-plan #A6) — adopt V2's tighter 5/15min lockout -->
  - **5 consecutive failed logins in 15 minutes** triggers lockout (per-account, IP+email composite scope for the attempt counter); lockout duration 15 minutes with admin override available via D4.5.
  - Separate from rate limit — rate limit returns 429, lockout returns 423 with `Retry-After`. The 423 status is mandatory: an attacker probing during a rate-limit window must still be able to distinguish "throttled" from "locked".
- **D2.6** (FR-009): Audit events `login_success`, `login_failure`, `logout`, `refresh_rotated`, `refresh_reuse_detected`, `account_locked`, `account_unlocked` wired through the M1 `AuditLogger`
- **D2.7** (NFR-001): Performance budget enforced in CI — `pytest-benchmark` asserts p95 < 200ms for `/login`, `/refresh`, `/logout` against a seeded 100k-user DB
- **D2.8** (R-001 mitigation): CSP header middleware emitting `default-src 'self'; script-src 'self' 'strict-dynamic' 'nonce-{nonce}'; object-src 'none'; base-uri 'self'`; SRI hashes on any externally-loaded JS in admin UI scaffold

### Dependencies

- **M1 complete** (specifically D1.1, D1.5)
- **External:** Redis 7 provisioned with persistence (AOF every-second), RSA-2048 keypair generated for JWT signing and stored in KMS

### Acceptance Criteria

- [ ] JWT issued by service A verifiable by service B using only the public key (asymmetric verification works)
- [ ] Refresh-token reuse detected within 100ms and triggers family revocation in integration test
- [ ] Refresh-token family ceiling enforced: integration test creates a family at T=0, exercises rotation hourly for 30 days (accelerated clock), confirms re-auth required at T=30d regardless of activity
- [ ] `siege -c 100 -t 60s https://staging/auth/login` returns p95 < 200ms with zero 5xx
- [ ] Account lockout test: 5 consecutive failed logins → 6th returns 423; lockout auto-expires after 15 minutes; manual unlock via admin API (stub OK, fleshed out in M4) succeeds
- [ ] Rate-limit hash-tag co-location test: simulate Redis Cluster (or single-node with hash-tag emulation), confirm rate-limit Lua script executes atomically and an attacker hitting two API nodes cannot exceed the per-user budget
- [ ] CSP violations logged to `/csp-report` endpoint and surfaced in audit log
- [ ] Bloom-filter denylist false-positive rate measured < 0.1% with 100k revoked `jti`s
- [ ] All M2 audit events present in `auth_events` and exported to the JSONL stream

### Risks Addressed

- **R-001 (Token theft via XSS):** D2.1 (HttpOnly cookies, `__Host-` prefix), D2.8 (CSP + SRI)
- **R-002 (Brute force):** D2.4 (rate limiting with cluster-safe key strategy), D2.5 (tightened account lockout 5/15min)

### Estimated Effort

**3 weeks** (1.5 sprints) — refresh-token family rotation with the 30-day ceiling and the denylist bloom filter are the non-obvious complexity.

---

## M3: Federated Identity & Two-Factor Authentication

<!-- Source: Base (original) -->

### Goal / Outcome

Add the two identity-expansion features: OAuth2 (Google, GitHub) for users who don't want a password at all, and TOTP-based 2FA for users who want defense-in-depth on top of their password. By end of M3, the auth system supports three login modes: password, password+2FA, and OAuth (with TOTP layered when enrolled).

### Deliverables

- **D3.1** (FR-003): OAuth2 / OIDC integration via `authlib`:
  - Google: full OIDC flow, `id_token` verified against Google's JWKS endpoint with 10-minute cache
  - GitHub: OAuth2 + supplementary `/user/emails` call to retrieve primary verified email
  - Account-linking rules documented in `docs/auth/oauth-linking.md`: matching verified email → link; mismatch → create new account with explicit user confirmation
  - PKCE enforced even for confidential clients (defense-in-depth against authorization-code injection)
  <!-- Source: invariant-probe INV-004 resolution per refactor-plan #B3 -->
  - **Email canonicalization (account-linking guard):** all email comparisons use NFC Unicode normalization + ASCII-lowercase of the domain part + preserve case of local-part per RFC 5321 (most providers ignore local-part case in practice, but we preserve to avoid breaking edge cases). Gmail-specific normalization (dot-stripping, plus-tag removal) is NOT applied at our layer — we treat `user.test+a@gmail.com` and `usertest@gmail.com` as distinct, deferring to Google's verified-email assertion. OAuth-provided emails arrive as canonicalized strings; our stored email is canonicalized at registration. A `UNIQUE (lower(email_domain), email_local)` index enforces the boundary. This rule explicitly mitigates the case/Unicode/plus-tag account-takeover risk.
- **D3.2** (FR-003 + R-003): Fallback path — if Google/GitHub return 5xx or timeout > 5s, surface a clear "Try email/password instead" UI affordance; never block the user
- **D3.3** (FR-007): TOTP 2FA enrollment `POST /auth/2fa/enroll` returning provisioning URI + QR-code SVG; secret stored AES-GCM-encrypted with a KMS key separate from the column-encryption key in M1 (defense-in-depth: a compromised DB doesn't yield TOTP secrets)
- **D3.4** (FR-007): TOTP verification at login — when `user.totp_enabled = true`, `/auth/login` returns `202 Accepted` with `{requires: "totp"}` instead of tokens; client then `POST /auth/2fa/verify` with the 6-digit code to receive tokens
  <!-- Source: invariant-probe INV-013 resolution per refactor-plan #B6 -->
  - **OAuth + 2FA interaction policy:** if a user has TOTP enrolled, OAuth completion DOES trigger the TOTP prompt (response: 202 with `requires: totp` even after OAuth callback). Rationale: TOTP enrollment is an explicit user opt-in for defense-in-depth; bypassing it on OAuth would reduce a user's stated security posture. Exception: trusted-device cookie (D3.6) suppresses TOTP for 30 days regardless of OAuth path. The OAuth login audit event (`oauth_login_pending_2fa`) records the 2FA-pending state for forensic clarity; this event type is registered in the D1.5 taxonomy.
- **D3.5** (FR-007): Recovery codes — 10 single-use codes generated at enrollment, hashed individually with bcrypt-12 (Argon2 is overkill for short high-entropy strings, and bcrypt's slower verify path here is acceptable since recovery is rare)
- **D3.6** (FR-007): Trusted-device flow — optional 30-day "remember this device" cookie (separate from the M2 access cookie; signed JWT bound to user agent + IP /24)
- **D3.7** (FR-009): Audit events `oauth_login_success`, `oauth_login_failed`, `oauth_login_pending_2fa`, `oauth_account_linked`, `oauth_account_unlinked`, `oauth_provider_unreachable`, `totp_enrolled`, `totp_disabled`, `totp_verified`, `totp_failed`, `recovery_codes_generated`, `recovery_code_used`, `trusted_device_added`, `trusted_device_removed`
- **D3.8** (R-003): OAuth provider health check — background task pings Google/GitHub discovery endpoints every 60s; status surfaced on `/healthz` so the load balancer knows to route around a provider outage

### Dependencies

- **M2 complete** (we need the JWT issuance and session machinery)
- **External:** Google OAuth credentials (client ID/secret) provisioned in GCP Console, GitHub OAuth App created, both with prod + staging callback URLs registered

### Acceptance Criteria

- [ ] End-to-end OAuth integration test using mocked provider (`pytest-httpx`) covers both Google and GitHub success + 5xx + invalid `id_token` cases
- [ ] PKCE `code_verifier` is generated client-side, never logged server-side (verified via grep against staging logs)
- [ ] Email canonicalization test: `User+Test@Example.com` and `user+test@example.com` resolve to the same canonical record; `user.test+a@gmail.com` and `usertest@gmail.com` remain distinct (Gmail-rule deference verified)
- [ ] TOTP code verified within ±1 time-step window (30s) to tolerate clock skew; window of 2+ rejected
- [ ] OAuth+TOTP interaction test: user with TOTP enrolled completes Google OAuth → response is 202 + `requires: totp`; user must complete `/auth/2fa/verify` to receive tokens; trusted-device-cookie exception verified separately
- [ ] Recovery code single-use enforced: same code used twice returns 401 on second attempt
- [ ] OAuth provider outage simulation (block egress to `accounts.google.com`) — `/healthz` reports degraded, fallback UI surfaces within 5s
- [ ] All M3 audit events present and queryable by `event_type` in < 100ms with the indexes added in this milestone

### Risks Addressed

- **R-003 (OAuth provider downtime):** D3.2 (fallback to email/password), D3.8 (health check + load-balancer signal)
- **R-001 reinforced:** TOTP secrets encrypted with a key distinct from the DB column key (D3.3); OAuth-with-TOTP enforcement (D3.4) prevents OAuth from silently downgrading a user's stated security posture

### Estimated Effort

**3 weeks** (1.5 sprints) — OAuth account-linking edge cases (existing-email collisions, unverified-email providers, deleted-then-re-registered accounts, case/Unicode canonicalization) consume more time than the happy path.

---

## M4: Governance — RBAC, Profile, Admin Dashboard, Audit, Deactivation

<!-- Source: Base (original) -->

### Goal / Outcome

Layer the organizational and compliance features on top of the auth substrate: roles + permissions, user profile management, an admin dashboard, full audit-event API, and the account deactivation workflow that satisfies GDPR Article 17 ("right to erasure").

### Deliverables

- **D4.1** (FR-004): RBAC schema — `roles` table, `permissions` table, `role_permissions` join, `user_roles` join; permissions follow a `resource:action` convention (e.g., `users:read`, `users:write`, `audit:read`).
  <!-- Source: Base (modified per refactor-plan #A8) — V2's 4-role static hierarchy seeded on V1's dynamic schema -->
  - **Four seeded roles forming a static hierarchy:** `viewer` (read own profile), `editor` (read+write own profile), `admin` (manage users + roles), `superadmin` (manage admins). New users are seeded with the `viewer` role at registration time (the audit event `role_assigned` is emitted for the implicit assignment). Underlying schema (roles, permissions, role_permissions, user_roles tables) is retained for v2 extensibility to fine-grained permissions, but **no permission composition is exposed in v1** — the v1 surface is strictly the four-role hierarchy.
- **D4.2** (FR-004): RBAC enforcement via FastAPI dependency `requires_permission("users:write")`; permissions baked into the JWT `roles` and `perms` claims at login time (denormalized for speed — NFR-001 budget doesn't permit a DB lookup per request)
- **D4.3** (FR-004): Permission-change propagation — when an admin modifies a user's roles, that user's existing access tokens are added to the M2 denylist; their next refresh re-mints with the new perms. Audit event `permission_change_propagated` records the propagation.
- **D4.4** (FR-010): User profile endpoints `GET /users/me`, `PATCH /users/me` (email change re-triggers M1 verification flow; password change requires current-password re-auth)
  <!-- Source: Variant 2 (sonnet/default) D4.2 — merged per refactor-plan #A1 -->
  - **Avatar upload:** `POST /users/me/avatar` storing to S3/R2 (or compatible object store) with a 5MB cap, MIME-type whitelist (image/png, image/jpeg, image/webp), virus scan via ClamAV sidecar before final upload; download via signed URL (15-min TTL). Avatar URL field added to the user profile row; replaces any prior avatar atomically.
- **D4.5** (FR-011): Admin dashboard (React 18 + TanStack Query + shadcn/ui) at `/admin`:
  - User search (paginated, indexed on `email`, `created_at`, `last_login_at`)
  - User detail: profile, roles, active sessions, recent audit events
  - Actions: assign/revoke roles, force-logout all sessions, manually unlock locked account, trigger password reset
  - All admin actions require `admin` (or higher) role AND emit a `admin_action` audit event with `actor_id`, `target_id`, `action`, `before`, `after`
- **D4.6** (FR-012): Account deactivation workflow `POST /users/me/deactivate`:
  <!-- Source: Base (modified per refactor-plan #A5) — adopt V2's 14-day grace -->
  - **Soft delete** by default: `users.deactivated_at` set, all sessions revoked, login blocked with 410 Gone, PII columns nulled except hashed email (for rejoin-prevention)
  - **Hard delete** after 14-day grace period (background job runs daily, scanning for `deactivated_at < now - 14 days`): full row deletion, audit event `account_purged` retained with `user_id` only (GDPR Article 17 compliance — audit log itself is a legitimate-interest exception)
  - Admin override to immediately hard-delete (legal-request path)
  <!-- Source: Variant 2 (sonnet/default) D4.6 — merged per refactor-plan #A2 -->
  - **Reactivation:** `POST /auth/reactivate` during the grace window requires email verification (re-send verification link), restores the user row, emits `account_reactivated` audit event, regenerates a fresh `email_hash` salt to avoid collision with a future re-registration.
  <!-- Source: invariant-probe INV-014 resolution per refactor-plan #B7 -->
  - **Deactivation invariant (in-flight access-token race):** when a user is deactivated (by self or admin), the deactivation transaction MUST: 1) revoke all refresh-token families in Redis, 2) add all currently-active access-token `jti` values (looked up from Redis where they were stored as a short-TTL secondary index) to the denylist, regardless of the global bloom-filter-config flag. Acceptance: a deactivation followed by an access-token usage within the TTL window returns 401 within 1s, verified by integration test.
- **D4.7** (FR-009): Audit-event API `GET /admin/audit?user_id=&event_type=&from=&to=` with cursor pagination; response time p95 < 500ms on a 10M-event table (requires the composite index `(user_id, occurred_at DESC)` and partial index on high-frequency `event_type`s, plus the monthly partitioning established in D1.5)
- **D4.8** (NFR-004): GDPR data-export endpoint `POST /users/me/export` — async job, emails a signed download URL when ready; export includes all PII, all audit events, all sessions, in machine-readable JSON

### Dependencies

- **M3 complete** (the JWT claim structure is finalized after M3 — adding `perms[]` is additive, but we need 2FA fully wired before exposing the admin UI to avoid a privilege-escalation gap)
- **External:** S3-compatible object store (avatar uploads), ClamAV deployment (virus scan sidecar)

### Acceptance Criteria

- [ ] Privilege-escalation test: a `viewer` calling an `admin`-protected endpoint returns 403 with no leaked information about whether the endpoint exists
- [ ] Default role assignment: a freshly registered user has exactly the `viewer` role; `role_assigned` audit event emitted at registration
- [ ] Permission propagation test: admin removes `editor` from user X → user X's next request with the old token returns 401 within 1s (denylist effective)
- [ ] Avatar upload test: 5MB+1byte file rejected with 413; `.exe` MIME rejected with 415; signed URL returns the image and expires after 15 min
- [ ] Admin dashboard accessibility scan (axe-core) returns zero serious or critical violations
- [ ] Deactivation soft-delete: 14 days post-deactivation, scheduled job purges; row gone, audit event remains
- [ ] Deactivation race test: issue access token at T=0 (TTL 15min), deactivate at T=10s, attempt token use at T=20s → 401 within 1s
- [ ] Reactivation test: deactivate, then reactivate within grace period, verify email re-verification triggered, `account_reactivated` audit event emitted
- [ ] GDPR export delivered within 30 days (NFR-004 / Article 12) — measured: median 5 minutes in load test
- [ ] Audit-event API p95 < 500ms on 10M-row test fixture (partition pruning + indexes verified)

### Risks Addressed

- **R-004 reinforced:** D4.6 (14-day grace + tighter deactivation pipeline limits long-tail PII exposure), D4.7 (forensic audit access), D4.8 (GDPR compliance), deactivation-denylist invariant closes the in-flight-token race

### Estimated Effort

**3 weeks** (1.5 sprints) — admin dashboard UI is the longest-tail item; consider parallelizing with a frontend engineer pair.

---

## M5: Hardening, Load Validation, GA Readiness

<!-- Source: Base (original) -->

### Goal / Outcome

Final pre-GA milestone: prove the system meets every NFR under realistic load, complete the OWASP audit, finalize runbooks, ship the SLO dashboard. Nothing new in scope — everything here is validation, polish, and operational readiness.

### Deliverables

- **D5.1** (NFR-002): Load test with k6 or Locust simulating 10,000 concurrent active sessions (login, 5min idle, refresh, 5min activity, logout)
  <!-- Source: Base (modified per refactor-plan #A4) — adopt V2's 4-hour soak duration -->
  - **Sustained for 4 hours** (replaces V1's original 1-hour duration); capture p50/p95/p99 latencies across all auth endpoints; capture Redis memory growth slope and PostgreSQL connection-pool saturation at hour 1, hour 2, hour 4 markers; alert if slope is non-linear (signals slow leak).
  <!-- Source: invariant-probe INV-009 resolution per refactor-plan #B5 (mirror) -->
  - **Definition of "10K concurrent sessions"** for this measurement: 10K active refresh-token families in Redis (per Executive Summary glossary). The load generator maintains 10K logical "user devices" with the login → idle → refresh → activity → logout pattern; access-token live count is incidental (typically 10K–30K depending on overlap).
- **D5.2** (NFR-005): Chaos engineering pass — kill Redis primary mid-traffic (failover within 10s expected), kill one API replica, partition the DB read-replica; SLO impact measured and documented. Chaos drills run concurrently with a scaled-down soak (1K sessions) to verify NFR-001 p95 holds under failure conditions, not just under steady state.
- **D5.3** (NFR-005): SLO dashboard in Grafana: error rate, p95 latency, refresh-token reuse rate (security signal), failed-login rate (R-002 signal), audit-event ingest lag, replica lag (read-replica health); alert rules wired to PagerDuty
- **D5.4** (NFR-003): Full OWASP Top 10 audit — external pentest engagement (Cobalt or similar) OR internal team with documented methodology covering all 10 categories; high/critical findings block GA
  <!-- Source: invariant-probe INV-016 resolution per refactor-plan #B8 -->
  - **OWASP Top 10 compliance gate criteria:** (a) targeted list is **OWASP Top 10 2021** (current authoritative list at GA cut; will reassess against a 2025 list when published); (b) compliance claim requires zero Critical and zero High findings open at GA; Medium findings require documented risk acceptance signed by the security lead OR remediation; Low/Info findings are tracked but do not block GA; (c) external pentest report signed by the engagement vendor (Cobalt or equivalent) is the authoritative artifact; ZAP CI scan is a continuous regression check, not the compliance basis.
- **D5.5** (NFR-005): Disaster-recovery runbook — RTO 1 hour, RPO 5 minutes; tabletop exercise executed and signed off
- **D5.6** (NFR-005): Key rotation runbook — JWT signing key rotation (RS256 supports overlapping `kid`s), column-encryption key rotation; rotation drill executed in staging
  <!-- Source: invariant-probe INV-002 resolution per refactor-plan #B2 -->
  - **JWKS cache TTL pinned to 10 minutes;** key rotation procedure: 1) publish new `kid` in JWKS endpoint, 2) wait 11 minutes for all verifiers to refresh, 3) cut signer over to new `kid`, 4) old `kid` remains in JWKS for 24 hours to verify in-flight tokens, 5) drop old `kid` after 24 hours + access-token-TTL safety margin. Drill verifies zero auth failures during the 24-hour overlap window.
- **D5.7** (R-004): Incident-response playbook for PII breach scenario, including: 72-hour GDPR notification timeline, audit-log forensic queries, customer communication template
- **D5.8** (All FRs): Final acceptance test suite — every FR-XXX has at least one E2E test in `tests/acceptance/test_fr_NNN.py`; suite runs in CI on every PR and against staging on every merge. The audit-event taxonomy (D1.5) is independently asserted: every event type in the v1 enumeration has at least one E2E test that produces it.
- **D5.9** (Documentation): Public API docs published (OpenAPI 3.1 spec auto-generated by FastAPI); auth integration guide; OAuth provider setup guide; 2FA user guide

### Dependencies

- **M4 complete**
- **External:** Pentest vendor engaged (4-week lead time — start outreach in M3)

### Acceptance Criteria

- [ ] k6 load test: 10K concurrent sessions sustained **4 hours**, zero 5xx, p95 < 200ms on critical paths (NFR-001 + NFR-002 jointly verified); Redis memory slope linear across hour markers
- [ ] Chaos drill: Redis primary failover transparent to end users (no visible 5xx burst); p95 under concurrent 1K-session load stays within 2× steady-state during the 10s failover window (NFR-001 + NFR-005 jointly verified)
- [ ] SLO dashboard live in production Grafana with at least 7 days of pre-GA data
- [ ] OWASP audit report: zero High/Critical findings open at GA cut; gate criteria (severity threshold + sign-off + Top-10 list version) documented and met
- [ ] DR drill: RTO measured ≤ 60min, RPO ≤ 5min from synthetic disaster
- [ ] Key-rotation drill: JWT signing key rotated in staging with zero auth failures during the 10-minute JWKS-cache refresh and 24-hour overlap windows
- [ ] All FR-001 through FR-012 have a green E2E test in CI; all event types from the D1.5 taxonomy produced by at least one E2E test

### Risks Addressed

- **All four risks** receive their final validation pass in M5; this is where we prove the mitigations from M1–M4 actually hold under stress, not just in unit tests

### Estimated Effort

**2 weeks** (1 sprint) — assumes M1–M4 quality has been high; if M5 surfaces structural problems we re-open earlier milestones.

---

## Cross-Cutting Concerns

<!-- Source: Base (original) -->

These tracks run continuously across all five milestones rather than being concentrated in one. Each milestone's acceptance criteria include the cross-cutting checks relevant to its surface area.

### Security (NFR-003, NFR-006, R-001–R-004)

- **Dependency scanning:** `pip-audit` + Dependabot, blocking on High/Critical CVEs in CI from M1 day 1
- **Static analysis:** `bandit` for Python, `semgrep` with the `p/owasp-top-ten` ruleset, both blocking
- **Secret scanning:** `gitleaks` pre-commit + GitHub Advanced Security
- **Threat modeling:** STRIDE pass at the start of M2, M3, M4 (each new feature surface gets a threat model)
- **Pen test cadence:** External pentest in M5 (pre-GA); thereafter, lightweight quarterly + full annual
- **Cryptographic agility:** Algorithm choices isolated behind `auth.crypto` module so future migration (e.g., Argon2 → next-gen) is a single-module change

### Observability

- **Structured logging:** All services emit JSON logs with `trace_id`, `user_id`, `event` fields; no PII or token values ever logged (enforced by a `LogScrubber` middleware unit-tested in M1)
- **Distributed tracing:** OpenTelemetry from M1; every external call (DB, Redis, SendGrid, OAuth providers) wrapped in a span
- **Metrics:** Prometheus scrape endpoint on every service exposing RED metrics (Rate, Errors, Duration) per endpoint
- **Audit-vs-logs distinction:** Audit events are **business records** (in Postgres, queryable, retained 7 years for compliance); application logs are **operational telemetry** (in Loki, retained 30 days)

### Performance (NFR-001, NFR-002)

- **Async-by-default:** All I/O via `asyncio` (FastAPI native); no blocking calls in request path
- **Connection pooling:** PgBouncer in transaction mode in front of Postgres; `aioredis` pool sized to 2× worker count
- **Caching strategy:** JWKS cache (OAuth providers) 10min; user roles cache 5min with explicit invalidation on D4.3 propagation; JWKS cache for our own RS256 verifiers also pinned at 10min (see D5.6)
- **CI perf budget:** `pytest-benchmark` regression check on every PR — a 20% p95 regression on any critical endpoint fails the build
- **Redis Cluster trigger:** at the operational definition of >10K active refresh-token families (NFR-002), shard Redis with the hash-tag key strategy in D2.4 to maintain atomic rate-limit and denylist operations
  <!-- Source: Variant 2 (sonnet/default) Cross-Cutting / Database Operations — merged per refactor-plan #A10 -->
- **Read replica routing:** admin dashboard queries (D4.5, D4.7) and audit-export queries (D4.8) are routed to a PostgreSQL read replica via a separate connection-string env var; replica lag tolerated up to 5s (asserted in the SLO dashboard D5.3). Auth write path (registration, login, refresh, role change) is unaffected — it remains on the primary.

### Compliance (NFR-004, R-004)

- **Data classification:** Every column tagged `public | internal | pii | sensitive_pii` in schema comments from M1
- **DPIA (Data Protection Impact Assessment):** Drafted in M1, finalized in M4, signed off in M5
- **Retention policies:** User data: lifetime of account + 14-day grace; audit events: 7 years; logs: 30 days; backups: 90 days encrypted
- **Right-to-erasure pipeline:** D4.6 implements (14-day grace, daily purge job); M5 verifies via tabletop exercise

### CI/CD & Quality Gates

- Every PR: lint, typecheck (`mypy --strict`), tests, security scans, perf benchmark — all green or no merge
- Trunk-based development; feature flags via `unleash` for risky rollouts (specifically: OAuth, 2FA, deactivation hard-delete)
- Staging deploy on every merge to `main`; production deploy weekly with rollback drill quarterly

---

## Risk Register

<!-- Source: Base (modified) — mitigation deliverables updated to reflect merged changes -->

| Source Risk | Description | Impact | Probability | Mitigation Deliverables | Primary Milestone(s) | Residual Risk |
|------------|-------------|--------|------------|-------------------------|----------------------|---------------|
| **R-001** | Token theft via XSS | High | Medium | D2.1 (HttpOnly + `__Host-` cookies, `SameSite`, 7-day rotation + 30-day family ceiling), D2.8 (CSP + SRI), D3.3 (TOTP secrets in distinct KMS key), D3.4 (OAuth-with-TOTP enforcement) | M2, M3 | Low — XSS still possible in admin UI; M4 axe-core scan + M5 pentest mitigate further |
| **R-002** | Brute-force attacks | High | High | D2.4 (token-bucket rate limit with hash-tag co-location for cluster correctness), D2.5 (tightened 5/15min account lockout, 423 distinct from 429), D5.3 (failed-login SLO alert) | M2, M5 | Low — distributed brute force across many IPs still possible; mitigated by per-account lockout independent of IP |
| **R-003** | OAuth provider downtime | Medium | Low | D3.2 (fallback to email/password), D3.8 (provider health check + `/healthz` signal) | M3 | Very Low — only impacts users who registered exclusively via OAuth with no password fallback; M3 acceptance includes "set a password" prompt for OAuth-only accounts |
| **R-004** | Data breach of PII | Critical | Low | D1.3 (column encryption), D1.4 (TLS 1.3, mTLS), D1.5 (audit trail with DB-role tamper resistance + monthly partitioning), D4.6 (14-day grace + deactivation-denylist invariant), D4.7 (forensic audit access), D4.8 (GDPR export), D5.7 (IR playbook) | M1, M4, M5 | Low — defense in depth; biggest residual is insider threat, partially mitigated by audit trail + DB-role separation + role hierarchy |

---

## Success Criteria Mapping

<!-- Source: Base (original) -->

| Source Success Criterion | Mapped Deliverable(s) | Validated In |
|---------------------------|------------------------|---------------|
| All FR requirements implemented and tested | D1.1, D1.2 (FR-001, FR-005); D2.1, D2.2, D2.3 (FR-002, FR-006); D2.4, D2.5 (FR-008); D3.1, D3.2 (FR-003); D3.3–D3.6 (FR-007); D4.1–D4.3 (FR-004); D2.6, D3.7, D4.7 (FR-009); D4.4 (FR-010, incl. avatar); D4.5 (FR-011); D4.6 (FR-012, incl. reactivation) | D5.8 — every FR has a green E2E test in CI at GA; every event type in the D1.5 taxonomy is produced by at least one E2E test |
| OWASP compliance verified via security scan | D1.6 (baseline), D2.8 (CSP), D5.4 (external pentest with documented gate criteria) | M5 acceptance gate — zero Critical/High open, gate sign-off recorded |
| Load testing confirms 10K concurrent sessions | D5.1 (k6 / Locust 4-hour sustained test); operational definition of "concurrent session" pinned in Executive Summary glossary | M5 acceptance — measurement against NFR-001 + NFR-002 jointly; chaos drill verifies the SLO holds during failure (D5.2) |
| OAuth2 flow works for Google and GitHub | D3.1 (authlib integration, with email canonicalization), D3.7 (audit events `oauth_login_success`) | M3 acceptance — E2E test with mocked + real provider; OAuth+TOTP interaction test |
| Audit logs capture all auth events | D1.5 (table + service + complete taxonomy of ~35 event types), D2.6 / D3.7 (event coverage), D4.7 (query API) | Continuous — every milestone adds events; M5 final reconciliation asserts every taxonomy entry has a producing test |

---

## FR / NFR Coverage Matrix

<!-- Source: Base (modified) — updated for merged deliverables (D4.4 avatar, D4.6 reactivation, etc.) -->

| ID | Description | Milestone(s) | Deliverable(s) |
|----|-------------|--------------|----------------|
| **FR-001** | User registration with email verification | M1 | D1.1 |
| **FR-002** | Login with JWT generation | M2 | D2.1 |
| **FR-003** | OAuth2 (Google, GitHub) | M3 | D3.1, D3.2 |
| **FR-004** | RBAC | M4 | D4.1, D4.2, D4.3 |
| **FR-005** | Password reset via email | M1 | D1.2 |
| **FR-006** | Session management + refresh tokens | M2 | D2.1, D2.2, D2.3 |
| **FR-007** | 2FA | M3 | D3.3, D3.4, D3.5, D3.6 |
| **FR-008** | API rate limiting per user | M2 | D2.4 |
| **FR-009** | Audit logging for auth events | M1, M2, M3, M4 | D1.5 (taxonomy + DB-role + partition), D2.6, D3.7, D4.7 |
| **FR-010** | User profile management | M4 | D4.4 (incl. avatar upload) |
| **FR-011** | Admin dashboard | M4 | D4.5 |
| **FR-012** | Account deactivation workflow | M4 | D4.6 (incl. 14-day grace + reactivation + deactivation-denylist invariant) |
| **NFR-001** | API < 200ms for auth endpoints | M2, M5 | D2.7, D5.1, D5.2 (chaos-paired) |
| **NFR-002** | 10K concurrent sessions | M5 | D5.1 (with operational definition + 4-hour soak) |
| **NFR-003** | OWASP Top 10 compliance | M1, M5 | D1.6, D5.4 (with documented gate criteria) |
| **NFR-004** | GDPR compliance | M1, M4, M5 | D1.7, D4.6 (14-day grace), D4.8, D5.7 |
| **NFR-005** | 99.9% uptime | M5 | D5.2 (chaos), D5.3 (SLO dashboard), D5.5 (DR), D5.6 (key rotation with JWKS TTL) |
| **NFR-006** | Encrypt PII at rest + in transit | M1 | D1.3, D1.4 |

**Coverage:** 12/12 FRs, 6/6 NFRs, 4/4 risks — 100%.

---

## Out of Scope

<!-- Source: Base (original) -->

These items from the source spec are explicitly **not** delivered in this roadmap:

- **Biometric authentication** — no fingerprint/face/voice in this release. Interface point: the 2FA module in M3 (`auth.twofactor`) is structured with a `TwoFactorMethod` protocol so a future `BiometricMethod` can plug in without re-architecting.
- **Hardware security keys (FIDO2 / WebAuthn)** — not delivered. Same extension point as above (`TwoFactorMethod` protocol).
- **Custom SSO protocol implementation** — we ship only standards-based OAuth2/OIDC (M3). No SAML, no proprietary SSO. Enterprises requiring SAML are routed to a future v2 feature flag.

**Additional clarifications** (judgment calls not in the source spec but worth pinning):

- **No SMS-based 2FA** — TOTP only. SMS adds SS7-attack surface and PSTN cost without commensurate security benefit. (R-001 reasoning applies.)
- **No social login beyond Google/GitHub** in v1 — Facebook/Twitter/Apple are out of scope. Same `authlib` foundation in M3 makes adding them later a configuration task.
- **No multi-tenant isolation primitives** in v1 — single-tenant by deployment. If multi-tenancy is needed, it becomes a v2 milestone (significant schema changes).
- **No fine-grained permission composition exposed in v1** — RBAC schema retains the underlying tables for forward-compatibility, but v1 surface is strictly the four-role static hierarchy (per D4.1).

---

## Appendix: Suggested Sprint Layout (Two-Week Sprints)

<!-- Source: Base (original) -->

| Sprint | Milestone | Focus |
|--------|-----------|-------|
| S1 (wk 1–2) | M1 | D1.1, D1.5 (with taxonomy + DB-role + partitioning + migration policy), D1.6 (registration + audit scaffold + OWASP baseline) |
| S2 (wk 3–4) | M1 → M2 start | D1.2, D1.3, D1.4, D1.7 (reset, encryption, TLS, GDPR tagging); D2.1 begins |
| S3 (wk 5–6) | M2 | D2.1 (7-day rotation + 30-day ceiling), D2.2, D2.3 (login, refresh, sessions) |
| S4 (wk 7–8) | M2 → M3 start | D2.4 (cluster-safe rate limit), D2.5 (5/15min lockout), D2.6, D2.7, D2.8 (rate limit, lockout, perf budget, CSP); D3.1 begins |
| S5 (wk 9–10) | M3 | D3.1 (with email canonicalization), D3.2–D3.8 (OAuth + 2FA complete, OAuth+TOTP interaction wired) |
| S6 (wk 11–12) | M4 | D4.1 (4-role seed on dynamic schema), D4.2, D4.3, D4.4 (with avatar), D4.6 (14-day grace + reactivation + deactivation-denylist) |
| S7 (wk 13–14) | M4 → M5 | D4.5, D4.7, D4.8 (admin UI, audit API, GDPR export); D5.1 (4-hour soak)–D5.9 (hardening + GA, JWKS TTL pinned, OWASP gate criteria) |

**Critical path:** M1 → M2 is non-overlapping (M2 needs M1's audit logger and user model). M3 and M4 can partially overlap by sprint 5 if a second engineer joins (M3 federated + M4 RBAC schema have minimal coupling). M5 strictly serial — it validates the whole.

---

*End of roadmap.*
