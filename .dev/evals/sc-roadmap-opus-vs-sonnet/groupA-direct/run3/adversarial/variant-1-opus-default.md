# Roadmap: User Authentication System (Variant 1 — opus)

## Architectural Philosophy

This roadmap is constructed on three load-bearing principles:

1. **Security as a first-class layer, not a cross-cutting afterthought.** Cryptographic primitives, secrets management, and threat models are established in M0/M1 — before a single user record is written. OWASP/GDPR posture is "shifted left" into the schema and middleware, not retrofitted.
2. **Strict layering with thin contracts at each boundary.** Database (PostgreSQL 15) → Domain services (Python/Node) → HTTP API (REST + OpenAPI 3.1) → UI (admin dashboard). Each layer has its own test pyramid; no layer reaches across a boundary.
3. **Observability and operability are non-negotiable for the NFR-005 99.9% target.** SLOs, dashboards, runbooks, and incident drills are M7 deliverables — not "nice-to-haves" deferred to after launch.

Critical sequencing decision: **OAuth2 (FR-003) is intentionally deferred to M5, after RBAC (M4)** because OAuth claim → role mapping is otherwise undefined and creates an authorization vacuum. **2FA (FR-007) precedes OAuth** because TOTP is a self-contained crypto primitive while OAuth has external-provider blast-radius risk.

---

## Milestone Summary Table

| ID | Milestone | Duration | Depends On | Primary Deliverables | Risks Addressed |
|----|-----------|----------|------------|----------------------|-----------------|
| M0 | Foundations & Threat Model | 2 weeks | — | Docker stack, secrets layer, ADRs, threat model | R-001, R-004 (prep) |
| M1 | Data Layer & Crypto Primitives | 2 weeks | M0 | PostgreSQL schema, encryption-at-rest, Argon2id hashing | R-004 |
| M2 | Core Auth: Register + Login + JWT | 3 weeks | M1 | FR-001, FR-002, email verification, JWT issuer | R-001, R-002 |
| M3 | Sessions, Refresh Tokens & Password Reset | 2 weeks | M2 | FR-005, FR-006, Redis session store, refresh rotation | R-001 |
| M4 | RBAC & Authorization | 2 weeks | M2 | FR-004, FR-010, FR-012, permission middleware | R-004 |
| M5 | OAuth2 (Google + GitHub) | 2 weeks | M4 | FR-003, provider fallback logic | R-003 |
| M6 | 2FA, Rate Limiting & Audit Logging | 3 weeks | M3, M4 | FR-007, FR-008, FR-009, append-only audit store | R-002, R-004 |
| M7 | Admin Dashboard & Operational Readiness | 3 weeks | M4, M6 | FR-011, dashboards, runbooks, SLOs | — |
| M8 | Verification: Load, Security, Compliance | 2 weeks | M7 | NFR-001 through NFR-006 verification | All |
| M9 | Production Cutover & Hardening | 1 week | M8 | Canary rollout, on-call rotation, post-launch review | — |

**Total estimated duration:** 22 weeks (with 2 weeks built-in slack); critical path = M0→M1→M2→M3→M6→M8→M9 (~17 weeks).

---

## M0 — Foundations & Threat Model

**Duration:** 2 weeks
**Goal:** Establish infrastructure, secrets, and security baseline *before* any auth code is written. This milestone exists because retrofitting secrets management and threat models after launch is an order of magnitude more expensive than doing it first.

### Deliverables

- **D-M0.1** — Containerized development stack (Dependency: Docker)
  - `docker-compose.yml` with PostgreSQL 15.5, Redis 7.2, MailHog (dev SMTP), and the auth service
  - Multi-stage Dockerfiles with distroless base images (gcr.io/distroless/python3-debian12)
  - Non-root container user (UID 10001), read-only root filesystem where possible
- **D-M0.2** — Secrets management layer
  - HashiCorp Vault dev mode locally; AWS Secrets Manager (or equivalent) reference architecture for staging/prod
  - Zero secrets in environment variables in production; sidecar injection pattern documented
  - JWT signing keys: RSA-256 (RS256) with key rotation hooks stubbed (rotation itself ships in M9)
- **D-M0.3** — Threat model document (STRIDE)
  - Per-asset analysis: credentials, tokens, sessions, PII
  - Explicit mapping to R-001 (XSS/token theft), R-002 (brute force), R-004 (PII breach)
  - Counter-control catalog: HTTP-only + Secure + SameSite=Strict cookies, CSP `default-src 'self'`, HSTS max-age 63072000
- **D-M0.4** — ADRs (Architecture Decision Records)
  - ADR-001: Token strategy (JWT short-lived access + opaque refresh in HTTP-only cookie)
  - ADR-002: Password hashing (Argon2id, memory=64MB, iterations=3, parallelism=4)
  - ADR-003: Schema-per-bounded-context vs. shared schema (decision: shared schema, separate migrations namespace)
  - ADR-004: Framework choice (FastAPI 0.115+ for async + OpenAPI native, OR NestJS 10+ for typed DI — pick one, document why)
- **D-M0.5** — CI/CD skeleton
  - GitHub Actions: lint (ruff/eslint), type check (mypy strict / tsc strict), unit tests, SAST (Semgrep), dependency scan (Trivy)
  - Pre-commit hooks: detect-secrets, no-debugger, no-print-statements

### Exit Criteria

- `docker compose up` produces a healthy stack passing readiness probes within 30s
- Threat model reviewed by ≥2 engineers; STRIDE coverage matrix at 100%
- All four ADRs merged with rationale and alternatives-considered sections
- CI pipeline green on an empty `auth-service` skeleton

### Implicit Prerequisites Surfaced

- Time-source synchronization (NTP) — required for TOTP and JWT `exp`/`nbf`
- TLS termination strategy (decision: terminate at ALB/ingress, mTLS internally optional for M9)
- Service discovery for Redis (decision: direct DNS in M0–M7, ElastiCache cluster mode in M9)

---

## M1 — Data Layer & Crypto Primitives

**Duration:** 2 weeks
**Goal:** Lock down the database schema and cryptographic primitives. The schema is the longest-lived artifact in the system; getting it right now prevents painful migrations later. (Dependency: PostgreSQL 15+)

### Deliverables

- **D-M1.1** — PostgreSQL 15 schema (initial migration)
  - `users` (id UUID v7, email CITEXT UNIQUE, password_hash TEXT, email_verified_at TIMESTAMPTZ, status ENUM('pending','active','suspended','deactivated'), created_at, updated_at)
  - `roles` (id, name, description), `permissions` (id, resource, action), `role_permissions` (role_id, permission_id), `user_roles` (user_id, role_id) — pure relational RBAC, no ad-hoc claim arrays
  - `oauth_identities` (user_id, provider ENUM, provider_user_id, linked_at) — separate from `users` to allow multi-provider linking later
  - `audit_events` partitioned by month (RANGE partition on `occurred_at`) — sized for retention rather than retrofitted
  - `email_verification_tokens`, `password_reset_tokens`, `refresh_tokens` (all with hashed token values, never raw)
  - Indexes: `users(email)`, partial index on `users(status) WHERE status='active'`, `refresh_tokens(user_id, revoked_at)`
- **D-M1.2** — Encryption-at-rest (Addresses NFR-006, R-004)
  - PostgreSQL TDE via pgcrypto for column-level encryption of PII fields (phone, name) using application-layer envelope encryption with KMS-wrapped DEKs
  - Disk-level encryption (LUKS in dev, AWS EBS gp3 with KMS in cloud) for defense-in-depth
- **D-M1.3** — Argon2id password hashing module
  - Library: `argon2-cffi` (Python) or `node-argon2`
  - Parameters tuned to ~250ms per hash on target hardware (m=64MB, t=3, p=4); benchmarked and recorded
  - Pepper stored in Vault (not DB), applied as HMAC pre-hash
- **D-M1.4** — Migration tooling
  - Alembic (Python) or Prisma Migrate (Node) — selected per M0 ADR-004
  - Forward-only migrations; rollbacks via compensating migrations only (documented policy)
- **D-M1.5** — Repository pattern with parameterized queries only
  - Zero string-concatenated SQL; static analysis (Semgrep rule `python.sqlalchemy.security.sqlalchemy-execute-raw-query`) enforced in CI

### Exit Criteria

- Schema migrated successfully forward and the chain replayed from empty on a fresh DB
- 100 sample users seeded with hashed passwords; hash verification round-trips in <300ms p95
- All PII columns encrypted at rest; verified by querying raw page contents via `pg_read_binary_file` and confirming ciphertext
- Repository unit tests achieve ≥90% line coverage with parameterized-query assertions

### Risks Addressed

- **R-004 (PII breach):** Column-level encryption + KMS + disk encryption = three layers of defense

---

## M2 — Core Auth: Registration + Login + JWT (FR-001, FR-002)

**Duration:** 3 weeks
**Goal:** The minimum viable authentication surface. Email-verified registration and JWT-issuing login. (Dependency: SendGrid)

### Deliverables

- **D-M2.1** — User registration endpoint (FR-001)
  - `POST /api/v1/auth/register` — accepts email + password
  - Password policy enforced server-side: zxcvbn score ≥3, minimum length 12, no top-1M breached passwords (HIBP k-anonymity check)
  - Rate-limited at 5 req/min/IP at this stage (full FR-008 in M6)
  - Generates verification token (32-byte CSPRNG, SHA-256 hashed in DB, raw value in email link)
  - Status flow: `pending` → email verified → `active`
- **D-M2.2** — Email verification flow
  - `GET /api/v1/auth/verify-email?token=...` — constant-time token comparison
  - Tokens expire in 24h; single-use; revoked on consumption
- **D-M2.3** — SendGrid integration
  - Wrapper service with circuit breaker (resilience4j-style); fallback to queued retry via Redis-backed BullMQ/Celery
  - Templates: verification, password-reset, security-alert (login from new device)
  - DKIM/SPF/DMARC documented for production sender domain
- **D-M2.4** — Login endpoint (FR-002)
  - `POST /api/v1/auth/login` — accepts email + password
  - Constant-time password comparison (Argon2id `verify` is constant-time by library design)
  - **Issues short-lived JWT access token (15min) + opaque refresh token (30d) as HTTP-only Secure SameSite=Strict cookies** (addresses R-001 token theft via XSS)
  - JWT claims: `sub` (UUID), `iat`, `exp`, `jti` (for revocation list), `aud`, `iss`
  - Failed-login counter increments per email AND per IP; account lockout after 10 failures in 15 minutes (preliminary; tuned in M6)
- **D-M2.5** — JWT issuer/verifier middleware
  - RS256 signature verification; `kid` in header for future key rotation
  - JWKS endpoint: `GET /.well-known/jwks.json` (public key only)
  - Token revocation: `jti` checked against Redis denylist (M3 expansion)
- **D-M2.6** — Security headers middleware
  - CSP, X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Referrer-Policy: strict-origin-when-cross-origin
  - HSTS preload-ready: `max-age=63072000; includeSubDomains; preload`

### Exit Criteria

- Happy-path: register → receive email → click link → login → receive token chain in 100% of test runs
- Login p95 latency <150ms (leaves headroom for NFR-001 200ms total)
- Password hash verification cost confirmed <300ms (acceptable login UX)
- SAST scan reports zero high/critical findings
- Integration test suite covers ≥95% of register/login state machine transitions

### Risks Addressed

- **R-001 (token theft via XSS):** HTTP-only cookies prevent JS access; CSP blocks inline scripts
- **R-002 (brute force):** preliminary rate limit + lockout; full implementation in M6

---

## M3 — Sessions, Refresh Tokens & Password Reset (FR-005, FR-006)

**Duration:** 2 weeks
**Goal:** Production-grade session lifecycle and self-service password recovery. (Dependency: Redis)

### Deliverables

- **D-M3.1** — Refresh token rotation (FR-006)
  - `POST /api/v1/auth/refresh` — verifies opaque refresh token, issues new access + new refresh, revokes old refresh
  - **Reuse detection:** if a revoked refresh is presented, *all* tokens for that user are revoked (compromised-family invalidation) — RFC 6819 §5.2.2.3 pattern
  - Refresh tokens stored as SHA-256 hashes; tied to a `device_id` cookie for session enumeration
- **D-M3.2** — Redis session store
  - Key schema: `session:{user_id}:{session_id}` → JSON blob (device, IP, UA, last_seen)
  - TTL = refresh token lifetime (30d); sliding expiration on activity
  - Redis configured with `maxmemory-policy allkeys-lru` and AOF persistence (`appendfsync everysec`)
- **D-M3.3** — Logout endpoints
  - `POST /api/v1/auth/logout` — current session only (revokes refresh, denylists access JWT `jti` until natural expiry)
  - `POST /api/v1/auth/logout-all` — revokes all sessions for user (security event triggers this automatically; see D-M6.4)
- **D-M3.4** — Password reset flow (FR-005)
  - `POST /api/v1/auth/forgot-password` — *always* returns 200 regardless of email existence (prevents enumeration)
  - Email contains time-limited (1h) single-use token (same CSPRNG + hashed-storage pattern as M2)
  - `POST /api/v1/auth/reset-password` — token + new password; on success: revokes ALL sessions (forces re-login everywhere), sends security-alert email
- **D-M3.5** — Session enumeration API (groundwork for FR-010)
  - `GET /api/v1/auth/sessions` — current user's active sessions with last-seen, IP, UA
  - `DELETE /api/v1/auth/sessions/:id` — revoke a specific session

### Exit Criteria

- Refresh-token rotation cycle works for 100 consecutive refreshes without drift
- Reuse-detection test: presenting a revoked refresh triggers full revocation; reproducible in integration test
- Password reset E2E: request → email → click → set new password → all sessions revoked → security email sent
- Redis failure injected via chaos test — auth degrades to "no new logins" but existing JWTs still validate until expiry (graceful degradation documented)
- Email enumeration via `/forgot-password` confirmed prevented (timing-attack-resistant: response time variance <5ms across known/unknown emails)

### Risks Addressed

- **R-001:** Reuse detection means stolen refresh tokens self-destruct on second use

---

## M4 — RBAC & Authorization (FR-004, FR-010, FR-012)

**Duration:** 2 weeks
**Goal:** Permission system that scales beyond two roles. This *must* land before OAuth (M5) because OAuth identity → role mapping has nowhere to land otherwise.

### Deliverables

- **D-M4.1** — Role and permission model
  - Default roles: `user`, `admin`, `support`, `auditor` (read-only access to audit logs)
  - Permission format: `resource:action` (e.g., `user:read`, `user:write`, `audit:read`, `admin:impersonate`)
  - All assignments stored in DB tables from M1; no hardcoded roles in code
- **D-M4.2** — Authorization middleware
  - Declarative: `@require_permission("user:write")` decorator / NestJS guard
  - Permissions loaded with JWT claims at token-issue time and cached in Redis (TTL = access-token lifetime = 15min)
  - Permission changes invalidate cache immediately via Redis pub/sub
- **D-M4.3** — Profile management endpoints (FR-010)
  - `GET /api/v1/users/me` — own profile
  - `PATCH /api/v1/users/me` — update name, phone, preferences (PII fields encrypted per M1.2)
  - `POST /api/v1/users/me/change-password` — requires current password; revokes all other sessions
  - Email change is a *separate* two-step flow: request → verification email to new address → confirm
- **D-M4.4** — Account deactivation workflow (FR-012)
  - `POST /api/v1/users/me/deactivate` — soft-delete: status → `deactivated`, PII pseudonymized (email → `deleted-{uuid}@deleted.invalid`)
  - 30-day grace period before hard-delete (GDPR Article 17 reconciled with audit-log retention requirements)
  - Hard delete: cryptographic erasure (rotate the column-encryption DEK so historical ciphertext is undecryptable) — addresses GDPR + maintains audit log integrity
  - Admin reactivation endpoint within grace period: `POST /api/v1/admin/users/:id/reactivate`
- **D-M4.5** — Authorization audit hooks
  - Every authorization decision (allow OR deny on protected endpoints) logged to in-process buffer; flushed to audit store in M6

### Exit Criteria

- 100% of API endpoints covered by either `@public` or `@require_permission(...)` — verified by automated route inspector
- Role assignment changes propagate within 5 seconds (cache invalidation test)
- Deactivation → 30-day timer → cryptographic erasure: tested end-to-end with time-travel fixture
- Authorization bypass attempts (privilege escalation, IDOR) tested in security suite; zero successful bypasses

### Risks Addressed

- **R-004:** Deactivation pseudonymization + DEK rotation = GDPR-compliant erasure without breaking audit chain

---

## M5 — OAuth2 (Google + GitHub) (FR-003)

**Duration:** 2 weeks
**Goal:** Third-party identity federation with safe fallback.

### Deliverables

- **D-M5.1** — OAuth2 authorization code + PKCE flow
  - `GET /api/v1/auth/oauth/:provider/start` — generates state (CSRF) + PKCE verifier, stores in Redis with 10min TTL
  - `GET /api/v1/auth/oauth/:provider/callback` — validates state, exchanges code, fetches user info
  - PKCE mandatory even for confidential clients (defense-in-depth)
- **D-M5.2** — Google OAuth2 provider adapter
  - Endpoints: `https://accounts.google.com/.well-known/openid-configuration` (auto-discovery)
  - Requested scopes: `openid email profile` only (minimal scope; GDPR data minimization)
- **D-M5.3** — GitHub OAuth2 provider adapter
  - GitHub does not implement OIDC discovery; endpoints hardcoded with periodic verification
  - Requested scopes: `read:user user:email`
- **D-M5.4** — Identity linking strategy
  - **First sign-in with OAuth:** auto-create user with `email_verified_at=now()` (provider already verified email), assign default role `user`
  - **Existing email collision:** require existing-account login to link OAuth identity (prevents account takeover via OAuth)
  - `oauth_identities` table from M1 holds the (provider, provider_user_id) → user_id mapping
- **D-M5.5** — Provider downtime fallback (Addresses R-003)
  - Health check on OAuth providers' `.well-known` endpoints every 60s
  - When provider degraded: login page shows banner + emphasizes email/password option
  - Circuit breaker prevents cascade failures: 5 consecutive provider errors → 60s open circuit
- **D-M5.6** — OAuth-specific audit events
  - `oauth.initiated`, `oauth.callback_success`, `oauth.callback_failure`, `oauth.identity_linked`, `oauth.identity_unlinked`

### Exit Criteria

- Google E2E: button click → consent → callback → JWT issued (verified in Playwright)
- GitHub E2E: same as above
- State-CSRF attack: tampered `state` parameter rejected with 400
- Account-collision test: OAuth callback for existing email *without* existing session → linking flow triggered (not silent takeover)
- Provider downtime simulated (block egress to `accounts.google.com`); fallback banner appears within 60s

### Risks Addressed

- **R-003 (OAuth provider downtime):** Circuit breaker + visible fallback to email/password

---

## M6 — 2FA, Rate Limiting & Audit Logging (FR-007, FR-008, FR-009)

**Duration:** 3 weeks
**Goal:** Defense-in-depth controls and compliance-grade audit trail. Largest milestone — three substantial features bundled because they share the "intercept all auth events" plumbing.

### Deliverables

- **D-M6.1** — TOTP-based 2FA (FR-007)
  - `POST /api/v1/auth/2fa/enroll` — generates secret (RFC 6238), returns QR code provisioning URI for authenticator apps
  - `POST /api/v1/auth/2fa/verify-enrollment` — user enters 6-digit code; only on success is 2FA enabled
  - Login flow modification: if user has 2FA enabled, login returns `mfa_required` instead of tokens; second call to `POST /api/v1/auth/2fa/login` with code completes auth
  - TOTP secret encrypted at rest (per M1 envelope encryption)
  - Time-window: ±1 step (90s total) to accommodate clock drift
  - **Recovery codes:** 10 single-use codes generated at enrollment, hashed in DB, shown ONCE
  - Rate limit: 5 TOTP attempts per 15min per user → 15min lockout
- **D-M6.2** — API rate limiting (FR-008)
  - Token-bucket algorithm in Redis (atomic Lua script for consistency)
  - Tiered limits by endpoint sensitivity:
    - `/login`, `/register`, `/forgot-password`: 10/min/IP, 5/min/email
    - `/refresh`: 60/min/user
    - General authenticated endpoints: 1000/min/user
  - `Retry-After` and `X-RateLimit-*` headers returned per IETF draft-ietf-httpapi-ratelimit-headers
  - Burst allowance: 2x sustained rate for 10s
  - **Distributed:** Redis-backed so it works across N application replicas
- **D-M6.3** — Account lockout (Hardening of M2 prelim)
  - 10 failed login attempts per email in 15min → 15min lockout
  - 50 failed attempts per IP in 1h → 1h IP block (separate from per-email)
  - Lockouts logged as security events; admin can unlock via M7 dashboard
- **D-M6.4** — Audit logging (FR-009)
  - Append-only `audit_events` table from M1 (monthly RANGE partitions)
  - Event schema: `event_id` (UUID v7), `occurred_at` (TIMESTAMPTZ), `actor_user_id`, `actor_ip`, `actor_ua`, `event_type`, `resource_type`, `resource_id`, `outcome`, `metadata` (JSONB)
  - Event types: `user.registered`, `user.email_verified`, `user.login_succeeded`, `user.login_failed`, `user.logout`, `user.password_changed`, `user.password_reset_requested`, `user.password_reset_completed`, `user.2fa_enrolled`, `user.2fa_disabled`, `user.2fa_succeeded`, `user.2fa_failed`, `user.account_locked`, `user.account_unlocked`, `user.deactivated`, `user.reactivated`, `oauth.*` (from M5), `admin.user_modified`, `authz.permission_denied`
  - **Write path:** synchronous DB insert for security-critical events (auth decisions); async fan-out to long-term store (S3 with Object Lock for WORM compliance) for retention
  - **Tamper-evidence:** hash chain — each event includes hash of previous event_id+payload; daily Merkle root anchored to immutable log
  - Retention: 7 years (financial-services bar; covers most compliance regimes including GDPR's reasonable retention)
- **D-M6.5** — Security alert emails
  - Triggered on: new-device login, password change, 2FA disabled, multiple failed logins, password reset completed
  - Includes IP geolocation, device/UA, timestamp, and "wasn't me" link → triggers logout-all + password-reset prompt

### Exit Criteria

- 2FA E2E: enroll → scan QR with Google Authenticator → verify → log out → log in → prompted for code → success
- TOTP replay attack blocked (same code rejected within validity window)
- Rate limit verified under 10k req/s synthetic load: limits enforced, no false positives at legitimate use rates
- Audit hash-chain integrity: tampering with any historical row detected by chain-verification job
- Audit-event count after a synthetic 100-user, 1000-action workload matches expected count (zero loss)

### Risks Addressed

- **R-002 (brute force):** Multi-layer rate limiting + account lockout + 2FA
- **R-004 (PII breach):** Tamper-evident audit chain enables forensics and breach-notification compliance

---

## M7 — Admin Dashboard & Operational Readiness (FR-011)

**Duration:** 3 weeks
**Goal:** UI for human operators + the operability infrastructure NFR-005 (99.9% uptime) actually requires. This is where "we built it" becomes "we can run it."

### Deliverables

- **D-M7.1** — Admin dashboard (FR-011) — React + TypeScript SPA
  - User list with filters (status, role, signup date, last login); cursor-paginated
  - User detail: profile, roles, sessions, recent audit events
  - Actions: force-logout-all, reset-password, lock/unlock, role assignment, deactivate, reactivate, impersonate (with full audit trail and time-limited 1h impersonation tokens)
  - Audit log viewer with structured filters (event_type, actor, time range, outcome)
  - Built with strict CSP (no `unsafe-inline`, no `unsafe-eval`); nonce-based script loading
- **D-M7.2** — Observability stack
  - **Metrics:** Prometheus with golden signals per endpoint (rate, errors, duration, saturation); custom auth metrics (`auth_logins_total{outcome}`, `auth_active_sessions`, `auth_token_refreshes_total`, `auth_rate_limit_hits_total`)
  - **Logging:** Structured JSON logs (correlation IDs, no PII in logs ever — enforced via lint rule on log field names)
  - **Tracing:** OpenTelemetry with W3C Trace Context; auth → DB → Redis → SendGrid spans
- **D-M7.3** — Dashboards & alerting
  - Grafana dashboards: SLI overview, latency percentiles, error rate, 2FA adoption, OAuth provider health, audit-log write rate
  - Alertmanager rules:
    - `AuthErrorRateHigh`: 5xx > 1% for 5min → page
    - `LoginLatencyP95High`: p95 > 180ms for 10min → ticket (NFR-001 buffer)
    - `RefreshTokenReuseDetected`: >0 in 5min → page (potential breach)
    - `OAuthProviderDown`: provider error rate >50% for 2min → ticket
    - `AuditLogWriteFailure`: any failure → page (compliance impact)
- **D-M7.4** — SLOs & error budgets
  - Auth API availability SLO: 99.9% (NFR-005) → 43.8min/month error budget
  - Login latency SLO: 99% of requests <200ms (NFR-001)
  - Error-budget burn-rate alerts (Google SRE multi-window multi-burn-rate pattern)
- **D-M7.5** — Runbooks
  - Incident response for: Redis outage, PostgreSQL primary failure, SendGrid outage, OAuth provider outage, suspected credential leak, rate-limit storm, audit-log lag
  - On-call escalation tree; recovery objectives: RTO 15min, RPO 1min (DB), RPO 0 (audit events — synchronous write)
- **D-M7.6** — Backup & restore
  - PostgreSQL: pgBackRest with WAL archiving (RPO 1min, point-in-time recovery)
  - Redis: AOF + periodic RDB snapshots (session loss tolerated; refresh-token DB is canonical)
  - **Quarterly restore drill** scripted and required

### Exit Criteria

- Dashboard usability test passes with two real operators completing 5 representative tasks unaided
- Alert fired in staging by injecting a fault → on-call receives page within 2min
- Restore drill: backup from previous day restored to scratch DB in <30min; data integrity verified
- All 6 runbooks reviewed by an engineer not involved in their authoring
- Grafana dashboards show <60s data lag end-to-end

---

## M8 — Verification: Load, Security, Compliance (NFR-001 through NFR-006)

**Duration:** 2 weeks
**Goal:** Prove the NFRs with evidence, not assertions.

### Deliverables

- **D-M8.1** — Load testing (NFR-001, NFR-002)
  - Tool: k6 or Locust; scenarios scripted and version-controlled
  - **Scenario A:** 10,000 concurrent sessions (NFR-002) — steady-state, validates connection pools, Redis memory, DB connections
  - **Scenario B:** Login spike — 1,000 logins/sec for 10min, measure p95 (target <200ms = NFR-001)
  - **Scenario C:** Token refresh storm — 5,000 refreshes/sec
  - Connection pool tuning evidence: PgBouncer transaction pooling, sized to (CPU cores × 2) + effective_io_concurrency
- **D-M8.2** — Security scanning (NFR-003, OWASP Top 10)
  - **DAST:** OWASP ZAP automated baseline + active scan
  - **SAST:** Semgrep with OWASP Top 10 ruleset (already in CI from M0; final clean run required)
  - **Dependency scan:** Trivy + `npm audit` / `pip-audit`; zero high/critical
  - **Penetration test:** External vendor engagement; deliverable = pen-test report + remediation
  - Coverage matrix mapping each OWASP Top 10 category to specific tests:
    - A01 Broken Access Control → IDOR tests in M4 suite
    - A02 Cryptographic Failures → M1 encryption tests, JWT algorithm-confusion test (`alg: none`)
    - A03 Injection → SAST + parameterized-query lint
    - A04 Insecure Design → threat model review (M0)
    - A05 Security Misconfiguration → ZAP + headers test
    - A06 Vulnerable Components → Trivy
    - A07 Identification & Auth Failures → 2FA + rate limit + lockout tests
    - A08 Software & Data Integrity → SBOM + signed builds (cosign)
    - A09 Logging & Monitoring → M6 audit suite
    - A10 SSRF → outbound allowlist for SendGrid + OAuth providers only
- **D-M8.3** — GDPR compliance verification (NFR-004)
  - Right-to-access endpoint: `GET /api/v1/users/me/data-export` — returns all PII as JSON
  - Right-to-erasure tested end-to-end via M4 deactivation flow
  - Data Processing Agreement template for SendGrid and OAuth providers
  - Privacy notice and consent capture on registration (verified UX)
  - DPIA (Data Protection Impact Assessment) document completed
- **D-M8.4** — OAuth E2E re-verification (Success Criteria)
  - Playwright suite covering full Google + GitHub flows, including consent, error, and cancel paths
- **D-M8.5** — Chaos / resilience testing
  - Kill PostgreSQL replica during sustained load → confirm failover within SLO
  - Kill 1 of 3 Redis nodes → confirm sessions preserved
  - SendGrid 503 injection → verify queued retry + alert fires

### Exit Criteria

- All NFRs have measured evidence attached to a verification report
- Load test: 10K concurrent sessions sustained for 1h with p95 <200ms and error rate <0.1%
- Security scan: zero high/critical; medium findings either fixed or have written acceptance from security lead
- GDPR data export returns complete, correct user data in <30s for a user with 1k audit events
- Penetration test report received; all high/critical findings remediated

---

## M9 — Production Cutover & Hardening

**Duration:** 1 week
**Goal:** Land in production with low blast radius and a smooth rollback path.

### Deliverables

- **D-M9.1** — Production infrastructure
  - Multi-AZ PostgreSQL with synchronous replica, Multi-AZ Redis cluster, multi-replica auth service behind ALB
  - Auto-scaling: scale on CPU 70% + custom metric `auth_active_sessions`
- **D-M9.2** — JWT signing key rotation
  - Operationalize the stubbed rotation from M0: dual-key serving (old `kid` still validates), 90-day rotation cadence
  - First production rotation drilled and documented before going live
- **D-M9.3** — Canary rollout
  - Initial: 1% traffic via header-based routing, observe for 24h
  - Then 10% for 48h, then 50% for 48h, then 100%
  - Automated rollback if error budget consumed >25% in any window
- **D-M9.4** — On-call rotation
  - PagerDuty schedules established with primary + secondary
  - Each on-call engineer has completed at least one runbook walkthrough
  - First 2 weeks post-launch: senior engineer shadow on-call
- **D-M9.5** — Post-launch review (after 2 weeks of production)
  - Metric review against SLOs
  - Lessons-learned document
  - Backlog of M10+ improvements

### Exit Criteria

- 14 days at 100% traffic with zero SLO breaches
- One unforced rotation of JWT signing keys completed without user impact
- Two incident drills (simulated outages) successfully executed by on-call

---

## Traceability Matrix

### Functional Requirements

| Req | Milestone | Deliverable(s) |
|-----|-----------|----------------|
| FR-001 (Registration + email verification) | M2 | D-M2.1, D-M2.2, D-M2.3 |
| FR-002 (Login + JWT) | M2 | D-M2.4, D-M2.5 |
| FR-003 (OAuth2 Google + GitHub) | M5 | D-M5.1–D-M5.6 |
| FR-004 (RBAC) | M4 | D-M4.1, D-M4.2 |
| FR-005 (Password reset via email) | M3 | D-M3.4 |
| FR-006 (Sessions + refresh tokens) | M3 | D-M3.1, D-M3.2, D-M3.3 |
| FR-007 (2FA) | M6 | D-M6.1 |
| FR-008 (Rate limiting per user) | M6 | D-M6.2, D-M6.3 |
| FR-009 (Audit logging) | M6 | D-M6.4, D-M6.5 |
| FR-010 (Profile management) | M4 | D-M4.3 |
| FR-011 (Admin dashboard) | M7 | D-M7.1 |
| FR-012 (Account deactivation) | M4 | D-M4.4 |

### Non-Functional Requirements

| Req | Milestone | Deliverable(s) | Verification |
|-----|-----------|----------------|---------------|
| NFR-001 (<200ms auth latency) | M2, M7, M8 | D-M2.4 (impl), D-M7.4 (SLO), D-M8.1 (load test) | k6 Scenario B |
| NFR-002 (10K concurrent sessions) | M3, M8 | D-M3.2 (Redis sizing), D-M8.1 | k6 Scenario A |
| NFR-003 (OWASP Top 10) | M0, M1, M6, M8 | D-M0.3 (threat model), D-M8.2 | OWASP ZAP + Semgrep + pen-test |
| NFR-004 (GDPR) | M4, M8 | D-M4.4 (erasure), D-M8.3 | DPIA + export endpoint test |
| NFR-005 (99.9% uptime) | M7, M9 | D-M7.4 (SLOs), D-M9.1 (multi-AZ), D-M9.3 (canary) | SLO measurement post-launch |
| NFR-006 (PII encryption) | M1 | D-M1.2 | Raw page inspection test |

### Risks

| Risk | Milestone(s) | Mitigation Deliverable(s) |
|------|--------------|---------------------------|
| R-001 (Token theft via XSS) | M0, M2, M3 | D-M0.3 (CSP), D-M2.4 (HTTP-only cookies), D-M2.6 (headers), D-M3.1 (reuse detection) |
| R-002 (Brute force) | M2, M6 | D-M2.4 (prelim lockout), D-M6.2 (rate limit), D-M6.3 (lockout), D-M6.1 (2FA) |
| R-003 (OAuth provider downtime) | M5 | D-M5.5 (circuit breaker + fallback) |
| R-004 (PII breach) | M1, M4, M6 | D-M1.2 (encryption), D-M4.4 (crypto erasure), D-M6.4 (tamper-evident audit) |

### Dependencies

| Dependency | First Used | Milestone Establishing It |
|------------|------------|---------------------------|
| PostgreSQL 15+ | M1 | D-M0.1, D-M1.1 |
| Redis 7.2 | M3 | D-M0.1, D-M3.2 |
| SendGrid | M2 | D-M2.3 |
| Docker | M0 | D-M0.1 |

### Success Criteria

| Criterion | Verified By |
|-----------|-------------|
| All FRs implemented and tested | Traceability matrix + per-milestone exit criteria |
| OWASP compliance via security scan | D-M8.2 |
| Load test 10K concurrent sessions | D-M8.1 Scenario A |
| OAuth2 works for Google + GitHub | D-M5.1–D-M5.3, D-M8.4 |
| Audit logs capture all auth events | D-M6.4 + integration suite |

---

## Sequencing & Critical Path

```
M0 ──► M1 ──► M2 ──► M3 ──► M6 ──► M8 ──► M9
                │      │      ▲      ▲
                │      └──────┤      │
                └──► M4 ──► M5┤      │
                       │      │      │
                       └──► M7┴──────┘
```

**Critical path:** M0 → M1 → M2 → M3 → M6 → M8 → M9 (≈17 weeks)

**Parallelizable opportunities:**

- M4 (RBAC) can begin midway through M3 once M2 contracts are stable
- M5 (OAuth) waits on M4, but the provider-adapter scaffolding can be prototyped in parallel
- M7 (dashboard + ops) can start at end of M4; backend prerequisites for the admin endpoints come from M4 & M6
- M8 verification can begin partial runs after M6 lands; full pass requires M7

**Hard sequencing constraints (do not violate):**

1. **M0 before any code** — secrets and threat model must precede implementation
2. **M1 before M2** — no auth logic without schema and crypto primitives
3. **M4 before M5** — OAuth identity → role mapping requires RBAC to exist
4. **M6 before M8** — security verification cannot meaningfully run without rate limiting, 2FA, and audit logs in place
5. **M7 before M9** — observability and runbooks are launch prerequisites for the 99.9% NFR

**Soft sequencing (recommended but flexible):**

- 2FA (M6) before OAuth (M5) would have been arguable; chosen sequence puts OAuth first because it unblocks more user-facing demos. Acceptable to swap if security review demands earlier 2FA.

---

## Verification & Success Criteria Summary

### Per-Milestone Gates

Each milestone has explicit exit criteria above. No milestone is "complete" until those gates are met.

### Cross-Cutting Verification Suites (continuous from M2 onward)

- **Unit tests:** ≥90% coverage on auth-critical modules (hashing, token issuance, authorization)
- **Integration tests:** Full state-machine coverage per flow (registration, login, refresh, reset, OAuth, 2FA)
- **Contract tests:** OpenAPI schema validated on every PR; breaking changes blocked
- **Security regression:** Each disclosed CVE / lesson-learned becomes a permanent test case
- **Performance regression:** k6 smoke test on every PR catches >20% p95 regression

### Compliance Sign-Offs (M8 deliverables)

- OWASP Top 10 coverage matrix signed by security lead
- GDPR DPIA signed by data-protection officer (or designated equivalent)
- Penetration test report with all high/critical findings remediated

### Launch Gate (M9)

- 14 days of canary at progressive traffic levels with zero SLO breaches
- One full incident drill executed by on-call rotation
- Backup restore drill within last 30 days

---

## Implicit Prerequisites Surfaced

These were not in the source spec but are required for a credible launch:

1. **NTP-synchronized clocks** — TOTP, JWT `exp`/`nbf`, audit timestamps
2. **TLS termination strategy** — ALB or equivalent; HSTS preload
3. **Sender domain DKIM/SPF/DMARC** — without these, SendGrid emails will land in spam
4. **CORS policy** — explicit allowlist, no wildcard for credentialed requests
5. **Frontend domain decisions** — same-site cookie behavior depends on domain structure
6. **Mobile/native client strategy** — refresh-token-in-cookie pattern needs an alternative (PKCE + secure storage) for native; not in scope for v1 but should be documented
7. **Localization plan** — email templates and error messages need i18n hooks even if only English ships
8. **DPO and security-lead engagement** — sign-off authorities for NFR-003 and NFR-004
9. **Cost model for SendGrid** — at 10k concurrent sessions, transactional email volume must be priced

---

## Risks Created by This Roadmap (Meta-Risks)

| Risk | Mitigation |
|------|-----------|
| M0 scope creep — "while we're here, let's also..." | Strict ADR review; defer non-foundation work to backlog |
| M6 bundle is too large (2FA + rate limit + audit) | Allow internal split into M6a/M6b/M6c if velocity demands |
| M8 verification surfaces blockers late | Run partial verification continuously from M2; M8 is the *final* pass, not the *first* |
| OAuth provider API changes mid-build | M5.2/M5.3 isolate provider logic behind adapter interface; contract tests guard against silent drift |

---

*End of roadmap.*
