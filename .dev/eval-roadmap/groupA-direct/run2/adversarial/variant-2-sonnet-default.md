# User Authentication System — Implementation Roadmap

> **Source**: `tests/sc-roadmap/fixtures/sample_spec.md`
> **Scope**: Full-stack auth system — OAuth2, JWT, RBAC, 2FA, audit logging, admin dashboard
> **Stack**: PostgreSQL 15+, Redis 7.x, SendGrid API v3, Docker Compose, Node.js 20 LTS / Fastify 4.x
> **Variant**: 2 (sonnet / default persona)

---

## Milestone Overview

| Milestone | Theme | FRs Covered | Depends On | Est. Duration |
|-----------|-------|-------------|------------|---------------|
| M1 | Core Auth Foundation | FR-001, FR-002, FR-006 | — | 3 weeks |
| M2 | OAuth2 & Password Recovery | FR-003, FR-005 | M1 | 2 weeks |
| M3 | RBAC & Profile Management | FR-004, FR-010 | M1 | 2 weeks |
| M4 | 2FA, Rate Limiting & Session Hardening | FR-007, FR-008 | M1, M3 | 2 weeks |
| M5 | Audit Logging & Compliance | FR-009, NFR-003, NFR-004, NFR-006 | M1 | 2 weeks |
| M6 | Admin Dashboard & Account Lifecycle | FR-011, FR-012 | M3, M5 | 2 weeks |
| M7 | Performance, Scale & Reliability Gates | NFR-001, NFR-002, NFR-005 | M1–M6 | 2 weeks |

**Total estimated timeline: ~13 weeks (M1–M7, with M2//M3 parallel after M1).**

---

## Dependency Graph

```
M1 ──┬──> M2 (OAuth + password reset)
     ├──> M3 (RBAC + profiles) ──┬──> M4 (2FA + rate limiting)
     │                            └──> M6 (admin dashboard)
     └──> M5 (audit + compliance) ────> M6
M1–M6 ─────────────────────────────────> M7 (perf/scale gates)
```

Critical path: **M1 → M3 → M4 → M7** (RBAC must land before 2FA enforcement rules; perf gates close the pipeline).

---

## M1 — Core Auth Foundation (Weeks 1–3)

### D1.1 — User Registration with Email Verification (FR-001)

**Implementation**: Fastify route `/auth/register` accepting `{ email, password, display_name }`. Password hashed with Argon2id (memory=64 MiB, time=3, parallelism=4). Email verification token is a 256-bit random hex stored in PostgreSQL `email_verification_tokens` table with `expires_at = now() + 24h`. SendGrid Transactional Templates API sends verification link to `GET /auth/verify?token=<hex>`.

**Edge cases**: Reject disposable-email domains via `disposable-email-domains` npm list. Re-send verification endpoint `POST /auth/verify/resend` rate-limited to 3 requests/hour per email. Unverified accounts auto-pruned after 72 hours via cron job.

**Acceptance criteria**:

- [ ] Registration returns 201 with `{ user_id, verification_sent: true }`; password never appears in logs or response bodies.
- [ ] Unverified users cannot call any authenticated endpoint (middleware returns 403 with `X-Verification-Required: true` header).
- [ ] Verification link click sets `email_verified_at` timestamp and returns 302 to login page.
- [ ] Argon2id hash verified with `argon2.verify()` on subsequent login; no plaintext storage anywhere.

### D1.2 — Login with JWT Generation (FR-002)

**Implementation**: `POST /auth/login` validates credentials against Argon2id hash. On success, mints two tokens:

- **Access token**: RS256-signed JWT (via `node-jose`), 15-minute TTL, payload `{ sub: user_id, roles: [...], email_verified: bool }`. Private key stored in Vault / env var `JWT_PRIVATE_KEY`.
- **Refresh token**: 256-bit opaque random string stored in `refresh_tokens` table with `expires_at = now() + 30d`, `rotated_at`, `revoked_at`.

Access token returned in response body. Refresh token set as HTTP-only, Secure, SameSite=Strict cookie with path `/auth/token/refresh`.

**Edge cases**: Failed-login counter incremented in Redis key `login_failures:<user_id>` with TTL 15 min; at 5 failures, account locked for 30 min (R-002 mitigation start). Concurrent login detection: invalidate older refresh token if same user logs in from new device within 60 seconds (configurable).

**Acceptance criteria**:

- [ ] Valid credentials return 200 with access JWT + refresh cookie; invalid credentials return 401 with generic "Invalid credentials" (no user enumeration).
- [ ] JWT contains `sub`, `roles`, `iat`, `exp` claims; `exp` is exactly 900 seconds after `iat`.
- [ ] Refresh token rotation: each use issues a new refresh token and revokes the old one. Reuse of a revoked refresh token revokes the entire token family (refresh token theft detection per RFC 6819 §5.2.2).

### D1.3 — Session Management with Refresh Tokens (FR-006)

**Implementation**: `POST /auth/token/refresh` reads opaque token from cookie, looks up `refresh_tokens` row. If valid and not revoked, issues new access JWT + new refresh token (rotation). Maintains `token_family` column to detect theft: if a previously-valid refresh token is reused, all tokens in that family are revoked and the user is notified via email.

Session listing: `GET /auth/sessions` returns active sessions with `{ session_id, ip, user_agent, created_at, last_used_at }`. Revoke single session: `DELETE /auth/sessions/:id`. Revoke all: `DELETE /auth/sessions`.

**Acceptance criteria**:

- [ ] Token rotation produces a new refresh token on every use; old token's `revoked_at` is set within the same database transaction.
- [ ] Token-family theft detection triggers revocation of all sessions for the user + notification email within 60 seconds.
- [ ] `GET /auth/sessions` returns at most 50 active sessions per user; oldest sessions auto-evicted on new login.

---

## M2 — OAuth2 & Password Recovery (Weeks 4–5)

**Depends on**: M1 (user model, JWT minting, email infrastructure)

### D2.1 — OAuth2 Integration: Google + GitHub (FR-003)

**Implementation**: Authorization Code flow with PKCE (`S256` code challenge). OAuth state stored in Redis with 10-minute TTL.

- **Google**: `openid` + `profile` + `email` scopes via `googleapis` npm package. Discovery doc at `https://accounts.google.com/.well-known/openid-configuration`.
- **GitHub**: `read:user` + `user:email` scopes via REST API `https://api.github.com/user`.

On first OAuth login: create user record with `email_verified_at = now()` (Google) or verify via `GET /user/emails` (GitHub). Link `oauth_identities` table: `{ provider, provider_uid, user_id }`. Multiple providers can link to one user account.

**Edge cases — OAuth provider downtime (R-003)**: If Google/GitHub token endpoint returns 5xx or times out (10s connect, 30s total), return 503 with `{ error: "oauth_provider_unavailable", fallback: "email_password" }` and log the failure. UI shows "Sign in with email/password instead" message. Health check endpoint `/health/oauth` checks provider reachability every 60 seconds and exposes `{ google: "up|down", github: "up|down" }` for monitoring.

**Acceptance criteria**:

- [ ] Google OAuth completes end-to-end: redirect → consent → callback → user created/linked → JWT issued, all in < 3 seconds at p95.
- [ ] GitHub OAuth completes end-to-end with same performance budget.
- [ ] When provider is down, login page shows email/password fallback within 2 seconds of failed OAuth attempt; no 500 error to the user.
- [ ] Linking a second OAuth provider to an existing account merges identities without creating a duplicate user.

### D2.2 — Password Reset via Email (FR-005)

**Implementation**: `POST /auth/password-reset/request` accepts `{ email }`, always returns 200 (no user enumeration). If email exists, generates 256-bit token in `password_reset_tokens` table with `expires_at = now() + 1 hour`. SendGrid sends link to `GET /auth/password-reset/confirm?token=<hex>`. Frontend renders password entry form; `POST /auth/password-reset/confirm` validates token and sets new Argon2id hash.

**Edge cases**: Token is single-use (set `used_at` on consumption). Rate-limit reset requests: 3 per email per hour. If user has active sessions, all refresh tokens are revoked on successful password change (force re-login).

**Acceptance criteria**:

- [ ] Reset token expires exactly 1 hour after creation; expired tokens return 410 Gone.
- [ ] Successful password change revokes all existing sessions and forces re-authentication.
- [ ] Rate limiting: 4th reset request within 1 hour returns 429 with `Retry-After` header.

---

## M3 — RBAC & Profile Management (Weeks 4–5, parallel with M2)

**Depends on**: M1 (user model, JWT claims)

### D3.1 — Role-Based Access Control (FR-004)

**Implementation**: Three-table model: `roles`, `permissions`, `role_permissions`. Default roles: `admin`, `editor`, `viewer`. Permission format: `resource:action` (e.g., `users:read`, `users:write`, `users:delete`). User-to-role mapping via `user_roles` table (many-to-many).

Middleware: `requirePermission('users:write')` decorator on routes. Permission check: resolve all roles for user, union their permissions, check if required permission is in the set. Permission cache in Redis with 5-minute TTL, keyed by `user_id`; invalidated on role/permission change via `PUBLISH perm_invalidate:<user_id>` on the role-change code path.

**Edge cases — RBAC cache invalidation**: When admin changes a user's role, the permission cache for that user is invalidated immediately. When a role's permissions change, all users with that role have their cache invalidated (fan-out via `SMEMBERS role_users:<role_id>` then `DEL perm_cache:<user_id>` for each).

**Acceptance criteria**:

- [ ] `requirePermission('users:write')` returns 403 for users without that permission; 200 for users with it.
- [ ] Role change takes effect within 5 seconds (cache TTL) for in-flight requests; new requests see updated permissions immediately.
- [ ] Admin can create custom roles with arbitrary permission sets via `POST /admin/roles`.

### D3.2 — User Profile Management (FR-010)

**Implementation**: `GET /auth/profile` returns `{ user_id, email, display_name, roles, oauth_providers, two_fa_enabled, created_at }`. `PATCH /auth/profile` accepts `{ display_name }` (email change requires re-verification: send verification to new email, keep old email until confirmed). `POST /auth/profile/avatar` accepts multipart upload (max 2 MiB, JPEG/PNG/WebP only), stored in S3-compatible storage, resized to 128x128 and 256x256 via Sharp.

**Acceptance criteria**:

- [ ] Email change sends verification to new address; old email remains active until verification completes.
- [ ] Avatar upload rejects files > 2 MiB with 413; accepts only image/* MIME types; non-image files rejected with 415.
- [ ] Profile changes reflected in subsequent JWT (roles updated on next token refresh).

---

## M4 — 2FA, Rate Limiting & Session Hardening (Weeks 6–7)

**Depends on**: M1 (auth foundation), M3 (RBAC — 2FA enforcement may depend on roles)

### D4.1 — Two-Factor Authentication (FR-007)

**Implementation**: TOTP via `otpauth` npm package (RFC 6238). User enables 2FA: server generates random secret, displays QR code (Google Authenticator compatible, `otpauth://totp/AppName:user@email?secret=...&issuer=AppName`). User verifies by submitting first TOTP code; only then is `two_fa_secret` stored (encrypted with AES-256-GCM, key from `TWO_FA_ENCRYPTION_KEY` env var).

Login flow when 2FA enabled: after credentials validated, return 202 with `{ requires_2fa: true, temp_token: <jwt 5min TTL> }`. Frontend submits `POST /auth/2fa/verify` with `{ code, temp_token }`.

**Edge cases — 2FA recovery codes**: On 2FA enablement, generate 10 single-use recovery codes (8-char alphanumeric, `crypto.randomBytes`). Store SHA-256 hashes. User instructed to save codes securely. `POST /auth/2fa/recover` accepts a recovery code, disables 2FA, and sends notification email. Each code is single-use; after 3 failed TOTP attempts within 5 minutes, require recovery code or email-based reset.

**Acceptance criteria**:

- [ ] TOTP codes accepted within ±1 time step (30-second window) to account for clock drift.
- [ ] Recovery codes are exactly 10, single-use, 8 characters; using one invalidates it permanently.
- [ ] After 3 consecutive wrong TOTP codes, further TOTP attempts are blocked for 5 minutes (rate-limited per user).
- [ ] 2FA secret is stored encrypted at rest (AES-256-GCM); decryption key never logged.

### D4.2 — API Rate Limiting per User (FR-008)

**Implementation**: Sliding-window rate limiter in Redis using `INCR` + `EXPIRE` pattern (or `EVALSHA` with Lua script for atomicity). Default limits:

- Auth endpoints (`/auth/login`, `/auth/register`, `/auth/password-reset/*`): 20 requests/minute per IP.
- General API: 100 requests/minute per user_id (resolved from JWT).
- Admin endpoints: 200 requests/minute per user_id.

Rate-limit headers on every response: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (Unix timestamp). Exceeded limit returns 429 with `Retry-After` header.

**Edge cases — Rate-limit bypass detection**: Middleware logs requests where `X-Forwarded-For` header changes mid-session (possible header spoofing). If a single IP exceeds 1000 requests/minute across all rate-limit buckets, auto-block IP for 1 hour and alert via `POST /internal/alerts` webhook. Audit log entry created for every rate-limit threshold breach (feeds FR-009).

**Acceptance criteria**:

- [ ] 21st request to `/auth/login` within 1 minute from same IP returns 429 with correct `Retry-After`.
- [ ] Rate-limit headers present on every API response (including 429 responses).
- [ ] Burst detection: 1001st request/minute from single IP triggers auto-block + alert webhook within 5 seconds.

---

## M5 — Audit Logging & Compliance (Weeks 6–7, parallel with M4)

**Depends on**: M1 (auth events to log)

### D5.1 — Audit Logging for Auth Events (FR-009)

**Implementation**: Append-only `audit_logs` table with columns: `{ id (UUIDv7 for time-ordering), event_type, actor_user_id, target_user_id, ip_address, user_agent, metadata (JSONB), created_at }`. Indexed on `event_type`, `actor_user_id`, `created_at`.

Event types: `auth.login.success`, `auth.login.failure`, `auth.logout`, `auth.register`, `auth.password_reset.request`, `auth.password_reset.complete`, `auth.2fa.enable`, `auth.2fa.disable`, `auth.2fa.verify`, `auth.oauth.link`, `auth.role.change`, `auth.account.deactivate`, `auth.rate_limit.exceeded`, `auth.token.revoke`, `auth.permission.change`.

**Edge cases — Audit log tamper-evidence**: Monthly merkle-tree checkpoint: compute merkle root of all audit entries for the month, store root hash in `audit_checkpoints` table signed with server's private key. API endpoint `GET /admin/audit/verify/:month` recomputes merkle root and compares. Any insertion/deletion of intermediate entries changes the root, detected as tampering.

**Acceptance criteria**:

- [ ] Every auth event listed above produces an audit log entry within the same database transaction as the event itself.
- [ ] `audit_logs` table is INSERT-only: no GRANT for UPDATE or DELETE to application role; only DBA can modify.
- [ ] Merkle checkpoint verification detects any single-row insertion or deletion with 100% recall.

### D5.2 — OWASP Top 10 Compliance (NFR-003)

**Implementation**: Run `zaproroxy/zap-baseline` Docker image against staging environment in CI pipeline (GitHub Actions). CSP headers: `Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'` (R-001 mitigation). All cookies: `HttpOnly; Secure; SameSite=Strict`. CORS: whitelist exact origins, no `*`. SQL via parameterized queries only (Fastify + `pg` driver). CSRF: `SameSite=Strict` cookies + double-submit cookie pattern for state-changing requests.

**Acceptance criteria**:

- [ ] ZAP baseline scan passes with 0 high/medium alerts on every CI run.
- [ ] No auth cookies accessible via `document.cookie` (verified by Playwright test: `expect(await page.evaluate(() => document.cookie)).not.toContain('refresh')`).
- [ ] SQL injection test: `POST /auth/login` with `email: "' OR 1=1 --"` returns 401, not 200.

### D5.3 — GDPR Compliance (NFR-004) & PII Encryption (NFR-006)

**Implementation**:

- **Data export**: `POST /auth/gdpr/export` generates JSON dump of all user data (profile, sessions, audit logs, OAuth identities) within 72 hours. Stored as encrypted file in S3; download link emailed.
- **Right to erasure**: `POST /auth/gdpr/delete` soft-deletes user (anonymizes email to `erased_<uuid>@erased.local`, deletes profile data, retains audit logs with `actor_user_id` set to `ERASED_<uuid>` for compliance). Deletion completes within 30 days.
- **Consent tracking**: `user_consents` table records `{ user_id, consent_type, granted_at, revoked_at }`. Registration requires explicit consent to privacy policy (version tracked).
- **PII at rest**: Email addresses encrypted with AES-256-GCM in `users` table. Display names encrypted similarly. Encryption key managed via env var `PII_ENCRYPTION_KEY` (32 bytes, rotated quarterly).
- **PII in transit**: TLS 1.3 enforced on all endpoints. HSTS header: `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`.

**Acceptance criteria**:

- [ ] GDPR export completes within 72 hours of request; file is downloadable for 7 days then auto-deleted from S3.
- [ ] Erasure request anonymizes all PII within 30 days; no query on `users` table can recover original email.
- [ ] All PII columns (`email`, `display_name`, `two_fa_secret`) are stored as encrypted ciphertext; `SELECT email FROM users WHERE user_id = X` returns ciphertext, not plaintext, to any direct DB query outside the application's decryption layer.
- [ ] TLS test: `nmap --script ssl-enum-ciphers -p 443 <host>` shows only TLS 1.3 ciphers.

---

## M6 — Admin Dashboard & Account Lifecycle (Weeks 8–9)

**Depends on**: M3 (RBAC — admin role required), M5 (audit log data feeds dashboard)

### D6.1 — Admin Dashboard (FR-011)

**Implementation**: Single-page admin UI (React 18 + TanStack Table). Endpoints (all require `admin:read` / `admin:write` permissions):

- `GET /admin/users` — paginated user list (cursor-based, 50/page) with filters: role, email verification status, 2FA status, account status.
- `GET /admin/users/:id` — user detail with full audit history.
- `PATCH /admin/users/:id` — change role, force password reset, disable 2FA (with audit log entry).
- `GET /admin/audit` — search audit logs by event type, date range, actor, target.
- `GET /admin/stats` — dashboard metrics: total users, active sessions, login rate (requests/min), failed login rate.

**Acceptance criteria**:

- [ ] Admin dashboard loads user list in < 500ms with 10,000 users in database (measured via Playwright navigation timing).
- [ ] Role change from admin UI takes effect within 5 seconds (RBAC cache invalidation from D3.1).
- [ ] Audit log search returns results within 2 seconds for queries spanning up to 90 days.

### D6.2 — Account Deactivation Workflow (FR-012)

**Implementation**: `POST /auth/account/deactivate` (user self-service) and `POST /admin/users/:id/deactivate` (admin action). Deactivation sets `account_status = 'deactivated'`, `deactivated_at = now()`, revokes all refresh tokens (sessions terminated), disables future login. User data retained for 30-day reactivation window: `POST /auth/account/reactivate` with email verification.

After 30 days, scheduled job permanently anonymizes account (GDPR erasure pipeline from D5.3).

**Edge cases**: Admin cannot deactivate own account (prevent lockout). Deactivation of a user with active OAuth links also revokes OAuth tokens (Google: `POST https://oauth2.googleapis.com/revoke?token=...`; GitHub: `DELETE https://api.github.com/applications/:client_id/grant`).

**Acceptance criteria**:

- [ ] Deactivated user's login returns 403 with `{ error: "account_deactivated", reactivation_possible: true|false }` based on whether 30-day window has elapsed.
- [ ] All sessions revoked within 5 seconds of deactivation (verified by attempting refresh token use after deactivation — must return 401).
- [ ] After 31 days, account data is fully anonymized; reactivation returns 410 Gone.

---

## M7 — Performance, Scale & Reliability Gates (Weeks 10–11)

**Depends on**: M1–M6 (all features complete; this milestone gates production readiness)

### D7.1 — API Response Time Gate (NFR-001)

**Implementation**: k6 load test suite (`k6 run --vus 100 --duration 5m load-test.js`). Thresholds enforced in CI:

- `http_req_duration{endpoint:auth}: p(95) < 200` — 95th percentile under 200ms for all `/auth/*` endpoints.
- `http_req_duration{endpoint:login}: p(99) < 500` — 99th percentile under 500ms for login specifically.

Test data: 10,000 pre-seeded users. Test scenarios: login burst (100 concurrent logins), registration trickle (5/second), token refresh sustained (50/second).

**Acceptance criteria**:

- [ ] k6 test passes with 0 threshold failures on 3 consecutive CI runs.
- [ ] No auth endpoint exceeds 200ms at p95 under 100 concurrent virtual users.

### D7.2 — Concurrent Session Scale Gate (NFR-002)

**Implementation**: k6 stress test ramping from 0 to 10,000 VUs over 10 minutes, each holding an active session (login → receive JWT → idle loop hitting `GET /auth/profile` every 30s). Redis cluster (3 nodes, no replicas for this test — mirroring production config). PostgreSQL connection pool: `pg` driver with `max: 50`, `idleTimeoutMillis: 30000`.

**Acceptance criteria**:

- [ ] 10,000 concurrent sessions sustained for 10 minutes with < 1% error rate.
- [ ] Redis memory usage reported at < 2 GiB for 10,000 sessions.
- [ ] No OOM kills or connection pool exhaustion in logs.

### D7.3 — Uptime & Reliability Gate (NFR-005)

**Implementation**: Docker Compose with health checks (`HEALTHCHECK CMD curl -f http://localhost:3000/health || exit 1`). Restart policy: `unless-stopped`. Readiness probe returns 200 only when PostgreSQL + Redis connections are healthy. Graceful shutdown: `SIGTERM` triggers 30-second drain period (in-flight requests complete, new requests receive 503).

Monitoring: Prometheus metrics endpoint at `/metrics` (using `prom-client`). Alerting rules: `auth_error_rate > 0.01` for 5 minutes → PagerDuty. `auth_p99_latency > 1000` for 3 minutes → PagerDuty.

**Acceptance criteria**:

- [ ] Rolling deploy (kill one of two app containers) results in zero 5xx responses to load balancer (verified by k6 test during deploy).
- [ ] Health check responds in < 50ms under load.
- [ ] Prometheus scrape succeeds with all auth metrics exported (`auth_login_total`, `auth_login_failures`, `auth_token_refresh_total`, `auth_active_sessions`).

---

## Risk-to-Milestone Mapping

| Risk | Mitigation | Milestone | Deliverable |
|------|-----------|-----------|-------------|
| R-001: Token theft via XSS | HTTP-only cookies, CSP headers, no token in localStorage | M5 | D5.2 (ZAP scan enforces cookie security + CSP) |
| R-002: Brute force attacks | Account lockout after 5 failures + IP rate limiting + burst detection | M1 + M4 | D1.2 (lockout) + D4.2 (rate limiting + bypass detection) |
| R-003: OAuth provider downtime | Fallback to email/password, health check monitoring | M2 | D2.1 (OAuth with downtime fallback) |
| R-004: Data breach of PII | AES-256-GCM encryption at rest, TLS 1.3 in transit, audit logging with tamper-evidence | M5 | D5.3 (encryption) + D5.1 (tamper-evident audit) |

---

## NFR Enforcement Strategy

| NFR | Enforcement Mechanism | Gate Milestone | Specific Threshold |
|-----|----------------------|----------------|-------------------|
| NFR-001: < 200ms p95 | k6 load test in CI, p95 threshold per endpoint | M7 (D7.1) | `p(95) < 200ms` for all `/auth/*` |
| NFR-002: 10K sessions | k6 stress test, 10K VUs sustained | M7 (D7.2) | `< 1% error rate` at 10K sessions |
| NFR-003: OWASP Top 10 | ZAP baseline scan in CI | M5 (D5.2) | `0 high/medium alerts` |
| NFR-004: GDPR | Automated export + erasure pipeline | M5 (D5.3) | Export in 72h, erasure in 30d |
| NFR-005: 99.9% uptime | Health checks, rolling deploy test, Prometheus alerting | M7 (D7.3) | Zero 5xx during rolling deploy |
| NFR-006: PII encryption | AES-256-GCM at rest, TLS 1.3 in transit | M5 (D5.3) | All PII columns ciphertext in DB |

---

## Out-of-Scope Reaffirmation

The following items are **explicitly excluded** per the source specification and will NOT be implemented in any milestone:

- **Biometric authentication** — fingerprint, face recognition, voice print
- **Hardware security keys** — FIDO2/WebAuthn U2F tokens, YubiKey support
- **Custom SSO protocol implementation** — SAML, LDAP, or proprietary SSO integrations

These boundaries are fixed. Any request to include them requires a spec revision and roadmap re-plan.

---

## Success Criteria → Milestone Traceability

| Success Criterion | Verified In | Evidence |
|-------------------|-------------|----------|
| All FR requirements implemented and tested | M1–M6 | Each FR has acceptance tests; CI regression suite covers all 12 FRs |
| OWASP compliance verified via security scan | M5 (D5.2) | ZAP baseline scan passes with 0 high/medium alerts |
| Load testing confirms 10K concurrent sessions | M7 (D7.2) | k6 stress test: 10K VUs, < 1% error rate, 10-minute sustain |
| OAuth2 flow works for Google and GitHub | M2 (D2.1) | E2E Playwright tests for both providers; fallback tested with provider mock returning 503 |
| Audit logs capture all auth events | M5 (D5.1) | 15 event types enumerated; each verified by integration test asserting audit row exists after action |

---

## FR Coverage Matrix

| FR | Milestone | Deliverable | Key Acceptance Test |
|----|-----------|-------------|---------------------|
| FR-001 | M1 | D1.1 | Registration → 201; unverified → 403; verify link → 302 |
| FR-002 | M1 | D1.2 | Login → 200 + JWT + refresh cookie; wrong creds → 401 |
| FR-003 | M2 | D2.1 | Google/GitHub OAuth E2E; provider-down → 503 + fallback |
| FR-004 | M3 | D3.1 | `requirePermission` enforces; cache invalidation < 5s |
| FR-005 | M2 | D2.2 | Reset request → email; token single-use; password change → sessions revoked |
| FR-006 | M1 | D1.3 | Token rotation; theft detection → family revocation |
| FR-007 | M4 | D4.1 | TOTP ±1 step; 10 recovery codes; 3 wrong → 5-min lockout |
| FR-008 | M4 | D4.2 | 21st request → 429; burst detection → IP auto-block |
| FR-009 | M5 | D5.1 | 15 event types logged; INSERT-only table; merkle tamper detection |
| FR-010 | M3 | D3.2 | Profile CRUD; email change re-verifies; avatar upload validation |
| FR-011 | M6 | D6.1 | User list < 500ms at 10K users; audit search < 2s/90 days |
| FR-012 | M6 | D6.2 | Deactivate → sessions revoked in 5s; 30-day reactivation window |

---

## Technology & Version Pinning

| Component | Version | Rationale |
|-----------|---------|-----------|
| PostgreSQL | 15.x | Spec dependency; JSONB + UUIDv7 support |
| Redis | 7.x | Spec dependency; Lua scripting for atomic rate limits |
| SendGrid | API v3 | Spec dependency; transactional templates |
| Docker | 24.x + Compose v2 | Spec dependency; health checks + rolling deploys |
| Node.js | 20 LTS | Long-term support through October 2026 |
| Fastify | 4.x | Low overhead (~2ms per request), schema validation |
| Argon2id | via `argon2` npm | OWASP recommended password hash |
| k6 | 0.47+ | Thresholds + checks in CI |
| ZAP | weekly Docker image | Baseline scan in CI pipeline |
| Prometheus + prom-client | 2.x / 15.x | Metrics + alerting for NFR-005 |

---

*End of roadmap. All 12 FRs, 6 NFRs, and 4 risks addressed with concrete, falsifiable acceptance criteria.*
