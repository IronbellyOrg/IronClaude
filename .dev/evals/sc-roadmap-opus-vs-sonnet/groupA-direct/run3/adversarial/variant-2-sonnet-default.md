# Roadmap: User Authentication System (Variant 2 -- sonnet)

> **Architectural philosophy**: Layered construction from infrastructure upward, with security controls woven into every layer rather than bolted on at the end. The critical path runs through data-layer design, core auth services, and security hardening; everything else (OAuth2, admin UI, dashboards) branches off that spine and can be parallelized once the core is stable.

---

## Milestone Summary

| Milestone | Name | Duration | Depends On | Key Deliverables | Risk Mitigations |
|-----------|------|----------|------------|------------------|------------------|
| M1 | Infrastructure & Tooling Bootstrap | 5 days | -- | Docker Compose stack, CI pipeline, PostgreSQL 15, Redis 7, SendGrid integration | Operational foundation for NFR-005 |
| M2 | Data Layer & Schema Design | 5 days | M1 | Normalized schema, migration framework, PII encryption at rest (NFR-006), seed data | R-004 (encryption), R-001 (token storage isolation) |
| M3 | Core Auth: Registration, Login, Sessions | 10 days | M2 | JWT issuance, refresh-token rotation, session store in Redis, email verification via SendGrid | R-002 (lockout seed), FR-001, FR-002, FR-006 |
| M4 | OAuth2 Provider Integration | 6 days | M3 | Google + GitHub OAuth2 flows, fallback to email/password | R-003 (provider downtime fallback), FR-003 |
| M5 | RBAC & Authorization Engine | 7 days | M3 | Role/permission tables, middleware guards, hierarchical role model | FR-004 |
| M6 | Security Hardening: 2FA, Rate Limiting, Headers | 8 days | M3, M5 | TOTP-based 2FA, sliding-window rate limiter, CSP + HSTS + HTTP-only cookies, PII encryption in transit | R-001, R-002, NFR-003, NFR-006, FR-007, FR-008 |
| M7 | User Lifecycle Management | 7 days | M3, M5 | Password reset flow, profile CRUD, account deactivation with grace period | FR-005, FR-010, FR-012 |
| M8 | Audit Logging & GDPR Compliance | 6 days | M3, M6 | Structured audit log, GDPR export/delete endpoints, retention policies | NFR-004, FR-009, R-004 |
| M9 | Admin Dashboard & User Management | 8 days | M5, M8 | Admin SPA, user list/search/ban, role assignment UI, audit log viewer | FR-011 |
| M10 | Load Testing & Performance Tuning | 5 days | M3-M8 | Load test suite (10K sessions), p95 latency report, connection pool tuning | NFR-001, NFR-002 |
| M11 | Security Audit & OWASP Compliance | 5 days | M6, M8 | OWASP ZAP scan, penetration test report, remediation backlog | NFR-003, success criteria |
| M12 | Operational Readiness & Launch | 5 days | M10, M11 | Deployment runbook, monitoring/alerting, incident response playbooks, rollback plan | NFR-005, all success criteria |

**Total estimated duration**: ~77 days on the critical path, but M4, M5, M7, M8, and M9 can overlap significantly after M3 ships. Realistic wall-clock with parallelization: **8-9 weeks** for a 3-person team.

---

## Critical Path

```
M1 --> M2 --> M3 ----+--> M6 ----+--> M8 --> M11 --> M12
                      |           |                      |
                      +--> M4     +--> M10 ------^       |
                      |                                   |
                      +--> M5 ----+--> M7                 |
                                  +--> M9 ---------+-----+
```

**Critical path**: M1 -> M2 -> M3 -> M6 -> M8 -> M11 -> M12 (longest sequential chain).

**Parallel branches after M3**:

- M4 (OAuth2) runs in parallel with M5 (RBAC) and M6 (security hardening start).
- M7 (user lifecycle) depends on both M3 and M5; starts when M5 completes.
- M9 (admin dashboard) depends on M5 and M8; starts when both complete.
- M10 (load testing) can begin once M3-M8 are feature-complete.

---

## Implicit Prerequisites (Not in Source Spec)

The source spec lists dependencies but omits several prerequisites that any production auth system requires. These are called out explicitly because they carry schedule risk if discovered late.

| Implicit Prerequisite | Why It Matters | Milestone | Deliverable |
|-----------------------|----------------|-----------|-------------|
| JWT signing key management (rotation, storage) | Stolen signing key = total auth compromise | M3 | D-M3.5 |
| Database connection pooling config | 10K sessions under NFR-002 requires tuned pools | M1 | D-M1.4 |
| Email template system (verification, reset, 2FA) | SendGrid integration needs templated HTML, not raw strings | M3 | D-M3.6 |
| Password hashing algorithm selection (argon2id) | bcrypt is aging; argon2id is current OWASP recommendation | M3 | D-M3.2 |
| CORS and origin allowlist configuration | API consumed by frontend(s); misconfigured CORS = auth bypass | M6 | D-M6.3 |
| Health check and readiness endpoints | Required for Docker orchestration and load balancer probes | M1 | D-M1.5 |
| Database migration framework (golang-migrate or Flyway) | Schema evolution without data loss | M2 | D-M2.2 |
| Environment-based config loading (12-factor) | Secrets must not be in code or Docker images | M1 | D-M1.3 |
| Structured logging framework (JSON logs) | Audit trail and debugging at scale | M1 | D-M1.6 |
| CI/CD pipeline for auth service | Automated testing and deployment | M1 | D-M1.2 |

---

## Milestone Detail

---

### M1: Infrastructure & Tooling Bootstrap (5 days)

**Goal**: Standing development and CI environment with all four declared dependencies (PostgreSQL 15, Redis 7, SendGrid, Docker) operational and verified.

**Scope**:

- Docker Compose stack for local development
- CI pipeline (GitHub Actions or equivalent) with lint, test, build stages
- PostgreSQL 15 with initial database and application user
- Redis 7 with persistence enabled (AOF for session durability)
- SendGrid API key configuration and test email dispatch
- Structured logging framework (e.g., `structlog` for Python, `zap` for Go)
- Health check and readiness endpoints on the auth service
- 12-factor config loading from environment variables

**Dependencies from spec**: PostgreSQL 15+, Redis, SendGrid, Docker -- all addressed here.

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M1.1 | Docker Compose stack (`docker-compose.yml` + supporting files) | `docker compose up` brings up postgres, redis, auth-service; health checks pass within 60s |
| D-M1.2 | CI pipeline (`.github/workflows/auth-ci.yml`) | On push: lint, unit tests, integration tests against containerized postgres/redis all pass |
| D-M1.3 | Config loading module (`config/`) | All secrets from env vars; no hardcoded credentials; `.env.example` documented; fails fast on missing required vars |
| D-M1.4 | PostgreSQL connection pool config | PgBouncer or built-in pool configured for 100 min / 200 max connections; verified via `pg_stat_activity` |
| D-M1.5 | Health/readiness endpoints (`/healthz`, `/readyz`) | `/healthz` returns 200 when process alive; `/readyz` returns 200 only when postgres + redis connections are valid |
| D-M1.6 | Structured logging setup | All log output is JSON with timestamp, level, trace_id, message; configurable log level via env var |
| D-M1.7 | SendGrid integration verification | Test email sent and received via sandbox API key; delivery webhook endpoint stubbed |

**Exit criteria**: `docker compose up` + `make test` both pass green in CI. SendGrid test email received. No hardcoded secrets in the codebase.

**FR/NFR mapping**: Foundational -- no direct FR/NFR, but enables NFR-005 (uptime infrastructure) and all subsequent milestones.

---

### M2: Data Layer & Schema Design (5 days)

**Goal**: Normalized relational schema for users, roles, permissions, sessions, and audit events. Migration framework operational. PII encryption at rest implemented.

**Scope**:

- Entity-relationship design for all auth domain objects
- PostgreSQL migration files (numbered, reversible)
- Application-level PII encryption (email, phone) using envelope encryption with a KMS-managed key
- Index strategy for high-query columns (email lookups, session tokens, audit timestamps)
- Seed data and development fixtures
- Schema documentation

**Schema design (key tables)**:

```sql
-- Core user table
users (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email         TEXT NOT NULL,          -- encrypted at application layer
  password_hash TEXT NOT NULL,          -- argon2id hash
  email_verified BOOLEAN DEFAULT FALSE,
  two_factor_enabled BOOLEAN DEFAULT FALSE,
  two_factor_secret TEXT,               -- encrypted at application layer
  is_active     BOOLEAN DEFAULT TRUE,
  deactivation_requested_at TIMESTAMPTZ,
  created_at    TIMESTAMPTZ DEFAULT now(),
  updated_at    TIMESTAMPTZ DEFAULT now()
)

-- Separate table isolates blast radius for token lookups
refresh_tokens (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL REFERENCES users(id),
  token_hash    TEXT NOT NULL UNIQUE,    -- hashed, never stored plaintext
  expires_at    TIMESTAMPTZ NOT NULL,
  revoked_at    TIMESTAMPTZ,
  created_at    TIMESTAMPTZ DEFAULT now()
)

-- RBAC tables
roles (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name          TEXT NOT NULL UNIQUE,    -- e.g., 'admin', 'user', 'moderator'
  description   TEXT,
  created_at    TIMESTAMPTZ DEFAULT now()
)

permissions (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name          TEXT NOT NULL UNIQUE,    -- e.g., 'users:read', 'users:write'
  description   TEXT
)

role_permissions (role_id UUID REFERENCES roles(id), permission_id UUID REFERENCES permissions(id), PRIMARY KEY (role_id, permission_id))
user_roles (user_id UUID REFERENCES users(id), role_id UUID REFERENCES roles(id), granted_at TIMESTAMPTZ DEFAULT now(), granted_by UUID REFERENCES users(id), PRIMARY KEY (user_id, role_id))

-- OAuth2 identity linking
oauth_identities (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL REFERENCES users(id),
  provider      TEXT NOT NULL,           -- 'google' or 'github'
  provider_uid  TEXT NOT NULL,
  access_token  TEXT,                    -- encrypted, nullable
  created_at    TIMESTAMPTZ DEFAULT now(),
  UNIQUE(provider, provider_uid)
)

-- Audit log (append-only, partitioned by month)
audit_events (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_id      UUID REFERENCES users(id),
  action        TEXT NOT NULL,           -- e.g., 'auth.login.success'
  resource_type TEXT,
  resource_id   UUID,
  metadata      JSONB,
  ip_address    INET,
  user_agent    TEXT,
  created_at    TIMESTAMPTZ DEFAULT now()
) PARTITION BY RANGE (created_at)

-- Rate limit counters (in Redis, but schema tracks per-user config)
rate_limit_overrides (
  user_id       UUID PRIMARY KEY REFERENCES users(id),
  requests_per_minute INT NOT NULL DEFAULT 60,
  updated_at    TIMESTAMPTZ DEFAULT now()
)
```

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M2.1 | Migration files `migrations/00001_initial_schema.up.sql` + `.down.sql` | `migrate up` creates all tables; `migrate down` drops cleanly; idempotent |
| D-M2.2 | Migration runner script or CLI integration | `make migrate-up` and `make migrate-down` work in Docker and local dev |
| D-M2.3 | PII encryption module (`crypto/pii.py`) | Email and 2FA secret encrypted with AES-256-GCM; envelope encryption with KMS key; decrypt roundtrip verified |
| D-M2.4 | Index strategy document | Explain-analyze output showing < 1ms for: email lookup, token hash lookup, audit event range scan |
| D-M2.5 | Seed data script (`scripts/seed_dev.py`) | Creates test users with all role combinations; verification tokens; expired refresh tokens for testing |
| D-M2.6 | Schema documentation (`docs/schema.md`) | ER diagram + column descriptions + encryption annotations for PII columns |

**Risk mitigation**: R-004 (data breach) -- encryption at rest for all PII columns (email, 2FA secret, OAuth tokens) means a raw DB dump exposes no usable personal data. Envelope encryption with a KMS-managed DEK means the encryption key is never in the database.

**Exit criteria**: All migrations apply cleanly. PII encryption roundtrip test passes. Seed data loads without error. `make migrate-down && make migrate-up` is idempotent.

---

### M3: Core Auth -- Registration, Login, Sessions (10 days)

**Goal**: Functional authentication spine: users can register, verify email, log in, receive JWT + refresh token, and have their sessions tracked in Redis.

**Scope**:

- User registration endpoint with input validation and email verification
- Password hashing with argon2id (OWASP-recommended)
- Login endpoint with JWT (RS256, signed with RSA private key) and refresh token issuance
- Refresh token rotation: each use issues a new refresh token, old one is revoked
- Session storage in Redis with configurable TTL
- JWT signing key pair generation and secure storage
- Email verification flow (token generation, SendGrid dispatch, verification endpoint)
- Account lockout after N failed attempts (seed for R-002 mitigation)

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M3.1 | Registration endpoint `POST /auth/register` | Validates email format, password strength (>=12 chars, mixed case, digit, symbol); hashes with argon2id; stores encrypted email; sends verification email via SendGrid; returns 201 |
| D-M3.2 | Password hashing module (`auth/password.py`) | Argon2id with OWASP-recommended parameters (m=65536, t=3, p=4); hash verification in < 500ms on target hardware; unit tests for hash/verify roundtrip |
| D-M3.3 | Email verification endpoint `GET /auth/verify?token=...` | Token is cryptographically random, single-use, expires after 24h; sets `email_verified=true`; returns redirect to frontend |
| D-M3.4 | Login endpoint `POST /auth/login` | Validates credentials; checks email_verified; checks account not locked; issues access JWT (15min TTL) + refresh token (7d TTL); stores session in Redis; logs audit event |
| D-M3.5 | JWT signing key management (`auth/keys.py`) | RSA 2048-bit key pair; private key stored in KMS or encrypted file; key rotation endpoint that accepts new key and gracefully handles tokens signed with previous key during overlap period |
| D-M3.6 | Email template system (`emails/`) | HTML templates for: verification, password reset, 2FA codes; SendGrid dynamic template IDs configured; preview endpoint for dev |
| D-M3.7 | Refresh token endpoint `POST /auth/refresh` | Accepts valid refresh token; revokes old token; issues new access JWT + new refresh token; detects reuse of revoked token (token theft detection) and revokes all tokens for that user |
| D-M3.8 | Session store module (`auth/sessions.py`) | Sessions in Redis with user ID, device fingerprint, IP; TTL matches refresh token TTL; session listing endpoint `GET /auth/sessions`; session revocation `DELETE /auth/sessions/:id` |
| D-M3.9 | Account lockout module (`auth/lockout.py`) | Tracks failed attempts in Redis (keyed by email + IP); locks after 5 failures in 15min; auto-unlocks after 30min; admin override unlock; logs lockout events to audit |
| D-M3.10 | Integration tests for full registration-to-login flow | Test suite covers: register -> verify -> login -> refresh -> session list -> logout; negative tests for expired tokens, wrong passwords, locked accounts |

**Risk mitigation**: R-002 (brute force) addressed by D-M3.9 lockout module. R-001 (token theft) partially addressed by D-M3.7 reuse detection.

**FR mapping**: FR-001 (D-M3.1, D-M3.3, D-M3.6), FR-002 (D-M3.4, D-M3.5), FR-006 (D-M3.7, D-M3.8).

**Exit criteria**: Full registration-to-login-to-refresh flow passes in integration tests. All tokens are correctly signed. Refresh token reuse triggers revocation. Account lockout activates after 5 failed attempts. Email verification link received and functional.

---

### M4: OAuth2 Provider Integration (6 days)

**Goal**: Users can authenticate via Google and GitHub OAuth2 flows. New users get auto-provisioned accounts. Existing users can link OAuth identities.

**Scope**:

- OAuth2 authorization code flow (PKCE-enabled) for Google and GitHub
- State parameter with CSRF protection
- Identity linking: existing users can connect Google/GitHub to their account
- Fallback to email/password when OAuth providers are down (R-003)
- OAuth token storage (encrypted) in `oauth_identities` table

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M4.1 | OAuth2 client configuration (`auth/oauth.py`) | Google and GitHub client IDs/secrets from env vars; redirect URIs configurable per environment; PKCE challenge/verifier generation |
| D-M4.2 | OAuth2 initiation endpoint `GET /auth/oauth/:provider` | Generates state + PKCE challenge; redirects to provider authorization URL; stores state in Redis with 10min TTL |
| D-M4.3 | OAuth2 callback endpoint `GET /auth/oauth/:provider/callback` | Validates state parameter; exchanges code for tokens; fetches user profile from provider; auto-creates user if new; links identity if existing user; issues JWT + refresh token |
| D-M4.4 | Identity linking endpoint `POST /auth/oauth/:provider/link` | Requires authenticated user; links OAuth identity to existing account; prevents linking an identity already linked to another account |
| D-M4.5 | Provider health check (`auth/oauth_health.py`) | Periodic (5min) check of Google and GitHub well-known endpoints; exposes `/auth/oauth/:provider/status` returning healthy/degraded; frontend uses this to hide/disable OAuth buttons when provider is down |
| D-M4.6 | OAuth2 E2E tests | Test with provider sandbox/test apps: full authorization code flow for both Google and GitHub; new user auto-provisioning; identity linking; state tampering rejection; expired code rejection |

**Risk mitigation**: R-003 (OAuth provider downtime) addressed by D-M4.5 health check and graceful degradation. Email/password always available as fallback (M3 already built).

**FR mapping**: FR-003 (D-M4.1 through D-M4.6).

**Exit criteria**: Google and GitHub OAuth2 flows complete successfully in test environment. New users are auto-provisioned. Existing users can link identities. Provider downtime is detected within 5 minutes.

---

### M5: RBAC & Authorization Engine (7 days)

**Goal**: Hierarchical role-based access control with permission checks enforced at the API middleware layer.

**Scope**:

- Role and permission seed data (admin, user, moderator roles; granular permissions)
- Authorization middleware that checks permissions on every request
- Role assignment API (admin-only)
- Permission inheritance (admin inherits all user permissions)
- Default role assignment on registration

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M5.1 | Permission seed data (`scripts/seed_rbac.py`) | Roles: admin (all permissions), moderator (users:read, users:suspend), user (self:read, self:write). Permissions: `users:read`, `users:write`, `users:delete`, `users:suspend`, `roles:assign`, `audit:read`, `admin:dashboard` |
| D-M5.2 | Authorization middleware (`middleware/authz.py`) | Extracts user ID from JWT; loads roles + permissions from DB (cached in Redis for 5min); checks required permission against user permissions; returns 403 if insufficient; supports `@require_permission('users:read')` decorator |
| D-M5.3 | Role assignment endpoint `PUT /admin/users/:id/roles` | Admin-only; validates role exists; records who granted the role and when; revokes previous role if assignment changes; audit log entry created |
| D-M5.4 | Permission check API `GET /auth/permissions` | Returns current user's effective permissions (union of all role permissions); used by frontend for UI gating |
| D-M5.5 | Default role hook | New users via registration or OAuth auto-provisioning get 'user' role; no user exists without at least one role |
| D-M5.6 | RBAC unit and integration tests | Tests: admin can access all endpoints; moderator can read users but not assign roles; regular user can only access own profile; role revocation takes effect immediately (cache invalidation) |

**FR mapping**: FR-004 (D-M5.1 through D-M5.6).

**Exit criteria**: Three-role hierarchy operational. Permission checks enforce correctly on all protected endpoints. Role assignment is audit-logged. Cache invalidation works within one request cycle.

---

### M6: Security Hardening -- 2FA, Rate Limiting, Headers (8 days)

**Goal**: TOTP-based two-factor authentication, API rate limiting, and comprehensive HTTP security headers. This milestone directly addresses R-001, R-002, and NFR-003.

**Scope**:

- TOTP-based 2FA (time-based one-time passwords, RFC 6238)
- Sliding-window rate limiter backed by Redis
- HTTP security headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- HTTP-only, Secure, SameSite cookies for JWT storage (not localStorage)
- CSRF protection for cookie-based auth
- PII encryption in transit enforcement (TLS config)

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M6.1 | TOTP 2FA setup endpoint `POST /auth/2fa/enable` | Generates TOTP secret (Base32); returns QR code as SVG for authenticator apps; stores encrypted secret; does not activate until first successful verification |
| D-M6.2 | TOTP 2FA verify endpoint `POST /auth/2fa/verify` | Accepts 6-digit code; validates against stored secret with +/- 1 period drift tolerance; on success, sets `two_factor_enabled=true` and issues session with 2FA flag |
| D-M6.3 | 2FA challenge in login flow | If `two_factor_enabled=true`, login endpoint returns `202 Accepted` with a challenge token instead of JWT; client must `POST /auth/2fa/challenge` with TOTP code to complete login |
| D-M6.4 | Recovery codes endpoint `POST /auth/2fa/recovery-codes` | Generates 10 single-use recovery codes (bcrypt-hashed storage); user must save them; each code can bypass 2FA once; remaining count tracked |
| D-M6.5 | Rate limiter middleware (`middleware/ratelimit.py`) | Redis-backed sliding window; default 60 req/min per user (by JWT sub); configurable per-endpoint overrides (e.g., 5 req/min for login); returns 429 with `Retry-After` header; respects `rate_limit_overrides` table |
| D-M6.6 | HTTP security headers middleware | CSP: default-src 'none', script-src 'self'; HSTS: max-age=31536000; X-Frame-Options: DENY; X-Content-Type-Options: nosniff; Referrer-Policy: strict-origin-when-cross-origin; all applied via middleware on every response |
| D-M6.7 | Cookie-based JWT storage | Access JWT stored in HTTP-only, Secure, SameSite=Strict cookie named `__Host-auth-token`; no JWT in response body for browser clients; API clients can opt into `Authorization: Bearer` header via `Accept: application/json` |
| D-M6.8 | CSRF protection (`middleware/csrf.py`) | Double-submit cookie pattern: `__Host-csrf-token` cookie + matching header on state-changing requests; validated on POST/PUT/DELETE/PATCH; GET/OPTIONS/HEAD exempt |
| D-M6.9 | TLS configuration (`docs/tls-config.md`) | Minimum TLS 1.2; TLS 1.3 preferred; cipher suite allowlist; HSTS preloading instructions; certificate rotation runbook |
| D-M6.10 | Security hardening test suite | Tests: 2FA enrollment + verification + recovery; rate limiter blocks at threshold; CSRF token rejection on mismatch; CSP header present on all responses; cookie flags verified (HttpOnly, Secure, SameSite) |

**Risk mitigation**: R-001 (XSS token theft) addressed by D-M6.7 (HTTP-only cookies, no localStorage) and D-M6.6 (CSP). R-002 (brute force) reinforced by D-M6.5 (rate limiting on login). R-004 (data breach) reinforced by D-M6.9 (TLS hardening for encryption in transit).

**FR mapping**: FR-007 (D-M6.1 through D-M6.4), FR-008 (D-M6.5).
**NFR mapping**: NFR-003 (D-M6.6, D-M6.7, D-M6.8, D-M6.9), NFR-006 (D-M6.7, D-M6.9).

**Exit criteria**: 2FA enrollment + verification + recovery code flow works end-to-end. Rate limiter blocks requests exceeding threshold. All security headers present on every response. JWT never appears in localStorage. CSRF tokens required on all state-changing requests. TLS config documented and verified.

---

### M7: User Lifecycle Management (7 days)

**Goal**: Complete user account management: password reset, profile editing, and account deactivation with grace period.

**Scope**:

- Password reset flow (token-based, email-mediated)
- Profile CRUD (name, avatar URL, timezone, preferences)
- Account deactivation with 30-day grace period and reactivation
- Email change with re-verification
- Password change for authenticated users

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M7.1 | Password reset request `POST /auth/password-reset/request` | Generates cryptographically random token (32 bytes); stores hash in Redis with 1h TTL; sends email with reset link via SendGrid template; rate-limited to 3 requests per hour per email |
| D-M7.2 | Password reset confirmation `POST /auth/password-reset/confirm` | Validates token; enforces same password strength rules as registration; hashes new password; revokes all existing refresh tokens; sends confirmation email |
| D-M7.3 | Profile endpoints `GET/PUT /auth/profile` | GET returns user profile (excluding password hash, 2FA secret); PUT allows updating display name, avatar URL, timezone, preferences; validates input; updates `updated_at` timestamp |
| D-M7.4 | Email change endpoint `POST /auth/profile/email` | Sends verification to new email; old email remains active until new one verified; both emails notified of the change attempt |
| D-M7.5 | Password change endpoint `POST /auth/profile/password` | Requires current password; enforces new password strength; cannot reuse last 5 passwords (history table); revokes all other sessions |
| D-M7.6 | Account deactivation `POST /auth/account/deactivate` | Sets `is_active=false` and `deactivation_requested_at=now()`; schedules permanent deletion after 30 days; user can reactivate by logging in within grace period; revokes all tokens immediately; sends confirmation email |
| D-M7.7 | Account reactivation `POST /auth/account/reactivate` | Only valid during 30-day grace period; sets `is_active=true`; requires password authentication; sends confirmation email |
| D-M7.8 | User lifecycle test suite | Covers: password reset happy path + expired token + reused token; profile update + validation; email change + unverified new email; deactivation + reactivation within grace period + after grace period |

**FR mapping**: FR-005 (D-M7.1, D-M7.2), FR-010 (D-M7.3, D-M7.4, D-M7.5), FR-012 (D-M7.6, D-M7.7).

**Exit criteria**: Password reset flow works end-to-end with email delivery. Profile updates persist correctly. Account deactivation blocks all auth within one request cycle. Grace period reactivation works. All edge cases tested (expired tokens, reused tokens, post-grace-period reactivation).

---

### M8: Audit Logging & GDPR Compliance (6 days)

**Goal**: Comprehensive audit trail for all auth events and GDPR-compliant data handling (export, deletion, retention).

**Scope**:

- Structured audit logging to `audit_events` table
- GDPR data export endpoint (right to access)
- GDPR data deletion endpoint (right to erasure)
- Data retention policies
- Audit log query API (admin-only)

**Audit events captured**:

| Event | Trigger | Fields |
|-------|---------|--------|
| `auth.register.success` | User registration | email (hashed), ip, user_agent |
| `auth.register.fail` | Registration validation failure | attempted_email (hashed), ip, reason |
| `auth.login.success` | Successful login | user_id, ip, user_agent, mfa_used |
| `auth.login.fail` | Failed login | attempted_email (hashed), ip, reason |
| `auth.login.lockout` | Account lockout triggered | user_id, ip, failure_count |
| `auth.logout` | Explicit logout | user_id, session_id |
| `auth.refresh.success` | Token refresh | user_id, old_token_id (hashed) |
| `auth.refresh.reuse` | Reused refresh token detected | user_id, token_id (hashed), ip |
| `auth.2fa.enable` | 2FA enabled | user_id |
| `auth.2fa.verify` | 2FA verification | user_id, success |
| `auth.password.reset.request` | Password reset requested | user_id, ip |
| `auth.password.reset.success` | Password reset completed | user_id |
| `auth.oauth.link` | OAuth identity linked | user_id, provider |
| `auth.oauth.login` | OAuth login | user_id, provider |
| `auth.role.assign` | Role assigned | user_id, role_id, granted_by |
| `auth.account.deactivate` | Account deactivated | user_id, ip |
| `auth.account.reactivate` | Account reactivated | user_id |
| `auth.profile.update` | Profile updated | user_id, changed_fields |

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M8.1 | Audit logger module (`audit/logger.py`) | Async write to `audit_events` table; accepts actor_id, action, resource_type, resource_id, metadata, ip, user_agent; fires-and-forgets to avoid blocking auth flow; batch inserts for throughput |
| D-M8.2 | Audit event instrumentation | All events in the table above are emitted at the correct points in the auth flow; verified by integration test that checks audit table after each auth operation |
| D-M8.3 | GDPR export endpoint `POST /auth/gdpr/export` | Returns JSON with all user data: profile, roles, login history (last 90 days), active sessions, OAuth identities; no internal IDs exposed to user; rate-limited to 1 per day |
| D-M8.4 | GDPR deletion endpoint `DELETE /auth/gdpr/delete` | Anonymizes PII (replaces with `anonymized_<uuid>`); retains audit events with nullified actor_id; revokes all tokens; schedules hard deletion after 30 days; verification code sent to email to confirm |
| D-M8.5 | Retention policy script (`scripts/enforce_retention.py`) | Deletes audit events older than 2 years (configurable); runs as daily cron; logs count of deleted records; respects GDPR deletion overrides |
| D-M8.6 | Audit query endpoint `GET /admin/audit` | Admin-only; paginated; filterable by user_id, action, date range; sortable; returns event details with user context |
| D-M8.7 | Audit and GDPR test suite | Tests: all 18+ event types emit correct records; GDPR export contains expected data; GDPR deletion anonymizes PII; retention policy deletes old records; audit query pagination works |

**Risk mitigation**: R-004 (data breach) reinforced by D-M8.4 (GDPR deletion reduces data at risk) and D-M8.5 (retention limits exposure window).

**FR mapping**: FR-009 (D-M8.1, D-M8.2, D-M8.6).
**NFR mapping**: NFR-004 (D-M8.3, D-M8.4, D-M8.5).

**Exit criteria**: All 18+ audit event types are captured in the database. GDPR export returns complete user data. GDPR deletion anonymizes all PII. Retention policy runs without error. Audit query returns paginated, filterable results.

---

### M9: Admin Dashboard & User Management (8 days)

**Goal**: Web-based admin interface for user management, role assignment, and audit log review.

**Scope**:

- Admin SPA (React or equivalent) served as static assets
- User list with search, filter, sort
- User detail view with role management and audit history
- Audit log browser
- System health overview (Redis, PostgreSQL, OAuth providers)
- Admin-only API endpoints powering the dashboard

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M9.1 | Admin API: user list `GET /admin/users` | Paginated; searchable by email (exact match on encrypted = admin-only decryption for search); filterable by role, status, verification; sortable by created_at, last_login |
| D-M9.2 | Admin API: user detail `GET /admin/users/:id` | Full user profile, roles, permissions, recent audit events, active sessions, OAuth identities linked |
| D-M9.3 | Admin API: user actions `POST /admin/users/:id/:action` | Actions: suspend (sets is_active=false), unsuspend, force-password-reset, revoke-all-sessions, assign-role, remove-role; all audit-logged; all require specific permissions |
| D-M9.4 | Admin SPA: user list page | Table with columns: email, roles, status, created, last login; search bar; role filter dropdown; pagination; click-through to detail |
| D-M9.5 | Admin SPA: user detail page | Profile section, roles section (assign/remove with dropdown), sessions section (revoke individual or all), audit history section (paginated), actions dropdown |
| D-M9.6 | Admin SPA: audit log browser | Full-width table: timestamp, actor, action, resource, IP; date range filter; action type filter; actor search; pagination; CSV export |
| D-M9.7 | Admin SPA: system health panel | Cards showing: PostgreSQL connection count, Redis memory usage, active sessions count, OAuth provider status (from D-M4.5); auto-refresh every 30s |
| D-M9.8 | Admin dashboard E2E tests | Playwright or Cypress tests: login as admin, search user, view detail, suspend user, assign role, view audit log; verify non-admin cannot access dashboard |

**FR mapping**: FR-011 (D-M9.1 through D-M9.8).

**Exit criteria**: Admin dashboard loads and all CRUD operations work. Role assignment is immediate and reflected in the user's next request. Audit log shows all admin actions. Non-admin users receive 403 on all admin endpoints.

---

### M10: Load Testing & Performance Tuning (5 days)

**Goal**: Verify NFR-001 (200ms p95) and NFR-002 (10K concurrent sessions) under realistic load. Identify and fix bottlenecks.

**Scope**:

- Load test suite using k6 or Locust
- Baseline performance measurement
- Bottleneck identification and remediation
- Connection pool tuning
- Redis performance tuning
- Query optimization

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M10.1 | Load test suite (`load-tests/`) | k6 scripts for: registration burst (1000 users in 60s), sustained login (500 req/s for 10min), token refresh storm (2000 concurrent refreshes), mixed read/write profile operations |
| D-M10.2 | Baseline performance report | Documented p50/p95/p99 latencies for each endpoint; throughput (req/s); error rate; resource utilization (CPU, memory, DB connections, Redis memory) |
| D-M10.3 | Bottleneck remediation | If p95 > 200ms: identify slow queries via `pg_stat_statements`, add missing indexes, tune connection pool; if throughput < target: add read replicas, tune Redis pipelining; document all changes |
| D-M10.4 | 10K concurrent session validation | Test with 10,000 simultaneous active sessions in Redis; verify login, token refresh, and session list all respond within 200ms p95; verify Redis memory usage is within budget |
| D-M10.5 | Performance regression CI job | k6 smoke test (lightweight, 30s) runs on every PR; gates merge if p95 > 300ms (with margin for CI noise) |

**NFR mapping**: NFR-001 (D-M10.2, D-M10.3), NFR-002 (D-M10.4).

**Exit criteria**: All auth endpoints respond within 200ms at p95 under 10K concurrent sessions. No performance regressions in CI smoke test. Bottleneck remediation documented.

---

### M11: Security Audit & OWASP Compliance (5 days)

**Goal**: Independent security verification. OWASP Top 10 compliance. Remediation of findings.

**Scope**:

- Automated OWASP ZAP scan
- Manual penetration testing checklist
- Remediation of critical/high findings
- Security report

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M11.1 | OWASP ZAP automated scan | Full scan against staging environment; baseline + active scan modes; report in HTML and JSON; no critical or high findings without documented remediation |
| D-M11.2 | Manual penetration test checklist | Covers: SQL injection on all inputs, XSS on all reflected output, CSRF bypass attempts, token tampering, privilege escalation, IDOR on user endpoints, session fixation, brute force effectiveness, OAuth state tampering, 2FA bypass |
| D-M11.3 | Remediation backlog | All findings triaged by severity; critical/high fixed before launch; medium documented with timeline; low accepted or deferred |
| D-M11.4 | Security compliance report | Maps each OWASP Top 10 category to: status (pass/fail/partial), evidence, remediation if applicable; sign-off from security lead |

**NFR mapping**: NFR-003 (D-M11.1 through D-M11.4).

**Exit criteria**: OWASP ZAP scan shows zero critical or high findings. Manual pentest checklist completed with all critical/high items remediated. Security compliance report signed off.

---

### M12: Operational Readiness & Launch (5 days)

**Goal**: Production deployment infrastructure, monitoring, alerting, and incident response procedures to meet NFR-005 (99.9% uptime).

**Scope**:

- Production deployment pipeline (blue-green or canary)
- Monitoring and alerting (metrics, logs, traces)
- Incident response runbook
- Rollback procedure
- Database backup and recovery verification
- Launch checklist

**Deliverables**:

| ID | Deliverable | Acceptance Criteria |
|----|-------------|---------------------|
| D-M12.1 | Deployment pipeline | Docker image build + push to registry; blue-green deployment with health check gate; automatic rollback if health checks fail within 5min; zero-downtime deployments |
| D-M12.2 | Monitoring stack | Prometheus metrics: auth request rate, latency histogram, error rate by endpoint, active sessions gauge, token issuance rate, rate limit rejections; Grafana dashboards for each metric |
| D-M12.3 | Alerting rules | PagerDuty or equivalent integration; alerts: error rate > 1% for 2min, p95 latency > 500ms for 5min, active sessions drop > 20% in 1min, Redis connection failures, PostgreSQL replication lag > 1s |
| D-M12.4 | Incident response runbook (`docs/incident-response.md`) | Playbooks for: token signing key compromise, database failover, Redis failover, OAuth provider outage, brute force attack in progress, data breach response; each with: detection, containment, remediation, communication steps |
| D-M12.5 | Database backup verification | Automated daily pg_dump + PITR WAL archiving; restore test on staging succeeds; RTO < 1 hour, RPO < 5 minutes documented |
| D-M12.6 | Rollback procedure (`docs/rollback.md`) | One-command rollback to previous image; database migration rollback procedure; rollback tested on staging; rollback time < 5 minutes |
| D-M12.7 | Launch checklist (`docs/launch-checklist.md`) | 30+ item checklist covering: security scan pass, load test pass, monitoring verified, alerting tested, backup restore verified, runbooks reviewed, stakeholder sign-offs |
| D-M12.8 | Production smoke test | Post-deploy automated test: register, verify email, login, refresh token, OAuth flow (one provider), 2FA, profile update; all pass against production within 5 minutes of deploy |

**NFR mapping**: NFR-005 (D-M12.1 through D-M12.8).

**Exit criteria**: Blue-green deployment works with automatic rollback. All monitoring dashboards populated. Alerting triggers correctly in test. Incident response runbook reviewed. Backup restore verified. Launch checklist all green.

---

## Traceability Matrix

### Functional Requirements

| Requirement | Milestone | Deliverable(s) | Verification |
|-------------|-----------|----------------|--------------|
| FR-001: User registration with email verification | M3 | D-M3.1, D-M3.3, D-M3.6 | Integration test: register -> receive email -> verify -> account active |
| FR-002: Login with JWT token generation | M3 | D-M3.4, D-M3.5 | Integration test: login returns JWT + refresh; JWT validates; refresh rotation works |
| FR-003: OAuth2 integration (Google, GitHub) | M4 | D-M4.1 through D-M4.6 | E2E test with provider sandbox; auto-provisioning verified |
| FR-004: Role-based access control (RBAC) | M5 | D-M5.1 through D-M5.6 | RBAC tests: admin/moderator/user permission boundaries enforced |
| FR-005: Password reset via email | M7 | D-M7.1, D-M7.2 | Test: request reset -> receive email -> confirm reset -> login with new password |
| FR-006: Session management with refresh tokens | M3 | D-M3.7, D-M3.8 | Test: refresh rotation; session list; session revocation; reuse detection |
| FR-007: Two-factor authentication (2FA) | M6 | D-M6.1 through D-M6.4 | Test: enable 2FA -> login requires TOTP -> verify code -> recovery code works |
| FR-008: API rate limiting per user | M6 | D-M6.5 | Test: exceed rate -> 429 response; admin override works; different users independent |
| FR-009: Audit logging for auth events | M8 | D-M8.1, D-M8.2, D-M8.6 | Test: perform auth action -> audit record exists with correct fields |
| FR-010: User profile management | M7 | D-M7.3, D-M7.4, D-M7.5 | Test: update profile -> read back matches; email change requires verification; password change requires current password |
| FR-011: Admin dashboard for user management | M9 | D-M9.1 through D-M9.8 | E2E test: admin CRUD operations; non-admin blocked |
| FR-012: Account deactivation workflow | M7 | D-M7.6, D-M7.7 | Test: deactivate -> cannot login -> reactivate within grace -> login works |

### Non-Functional Requirements

| Requirement | Milestone | Deliverable(s) | Verification |
|-------------|-----------|----------------|--------------|
| NFR-001: API response < 200ms | M10 | D-M10.2, D-M10.3 | k6 load test report showing p95 < 200ms for all auth endpoints |
| NFR-002: 10,000 concurrent sessions | M10 | D-M10.4 | k6 test with 10K active sessions; Redis memory within budget |
| NFR-003: OWASP Top 10 compliance | M6, M11 | D-M6.6 through D-M6.9, D-M11.1 through D-M11.4 | OWASP ZAP scan + manual pentest; zero critical/high findings |
| NFR-004: GDPR compliance | M8 | D-M8.3, D-M8.4, D-M8.5 | GDPR export complete; deletion anonymizes; retention enforced |
| NFR-005: 99.9% uptime | M12 | D-M12.1 through D-M12.8 | Blue-green deployment; monitoring; alerting; incident runbooks |
| NFR-006: Encrypt PII at rest and in transit | M2, M6 | D-M2.3, D-M6.7, D-M6.9 | AES-256-GCM for PII at rest; TLS 1.2+ for transit; verified in security audit |

### Risk Mitigations

| Risk | Milestone | Deliverable(s) | Mechanism |
|------|-----------|----------------|-----------|
| R-001: Token theft via XSS | M6 | D-M6.6, D-M6.7, D-M6.8 | HTTP-only cookies (no JS access); CSP headers block inline scripts; SameSite=Strict prevents CSRF |
| R-002: Brute force attacks | M3, M6 | D-M3.9, D-M6.5 | Account lockout after 5 failures; rate limiting on login (5 req/min); IP-based rate limiting |
| R-003: OAuth provider downtime | M4 | D-M4.5 | Provider health checks; graceful degradation to email/password; frontend hides OAuth buttons when provider is down |
| R-004: Data breach of PII | M2, M6, M8 | D-M2.3, D-M6.9, D-M8.4, D-M8.5 | AES-256-GCM encryption at rest; TLS 1.2+ in transit; GDPR deletion reduces data at risk; retention policy limits exposure window |

### Success Criteria Verification

| Success Criterion | Verification Method | Milestone |
|-------------------|---------------------|-----------|
| All FR requirements implemented and tested | Traceability matrix (above) shows every FR mapped to passing tests | M9 (last FR delivery) |
| OWASP compliance verified via security scan | OWASP ZAP scan + manual pentest with zero critical/high findings | M11 |
| Load testing confirms 10K concurrent sessions | k6 load test report: 10K sessions, p95 < 200ms, < 1% error rate | M10 |
| OAuth2 flow works for Google and GitHub | E2E test with provider sandbox apps for both providers | M4 |
| Audit logs capture all auth events | Integration test verifies all 18+ event types are recorded with correct fields | M8 |

---

## Sequencing & Critical Path Analysis

### Dependency Graph (text)

```
M1 (Infrastructure)
 |
 v
M2 (Schema)
 |
 v
M3 (Core Auth) --------+--------+--------+
 |                      |        |        |
 v                      v        v        v
M4 (OAuth2)        M5 (RBAC)   M6 (Security)
 |                      |        |
 |                      v        v
 |                 M7 (User Lifecycle)
 |                      |
 |                +-----+------+
 |                v            v
 |           M8 (Audit)   M9 (Admin Dashboard)
 |                |
 v                v
M10 (Load Testing -- requires M3-M8 feature-complete)
 |
 v
M11 (Security Audit -- requires M6 hardening + M8 audit)
 |
 v
M12 (Launch -- requires M10 + M11)
```

### Critical Path

**M1 -> M2 -> M3 -> M6 -> M8 -> M11 -> M12** = 5 + 5 + 10 + 8 + 6 + 5 + 5 = **44 days** on the critical path.

### Parallelization Opportunities

With a 3-person team (Backend A, Backend B, Frontend/DevOps):

| Week | Backend A | Backend B | Frontend/DevOps |
|------|-----------|-----------|-----------------|
| 1 | M1 infrastructure | M1 infrastructure (pair) | M1 CI/CD pipeline |
| 2 | M2 schema + encryption | M2 schema (pair) | M1 logging + health checks |
| 3-4 | M3 core auth (registration, login) | M3 core auth (JWT, sessions, lockout) | M3 email templates + test infra |
| 5 | M4 OAuth2 | M5 RBAC | M6 security headers + cookie setup |
| 6 | M4 OAuth2 (cont.) + M5 RBAC (cont.) | M6 2FA + rate limiting | M7 user lifecycle APIs |
| 7 | M7 password reset + deactivation | M8 audit logging | M9 admin dashboard start |
| 8 | M8 GDPR endpoints | M9 admin APIs | M9 admin SPA |
| 9 | M10 load testing | M10 load testing (pair) | M9 admin E2E tests |
| 10 | M11 security audit | M11 pentest support | M12 deployment + monitoring |
| 11 | M12 operational readiness | M12 incident runbooks | M12 launch verification |

**Wall-clock estimate**: ~10-11 weeks with parallelization, 15+ weeks if fully sequential.

---

## Verification & Success-Criteria Section

### Verification Strategy by Milestone

Every milestone has a verification gate. No milestone is considered complete until its exit criteria are met AND the following verification checks pass:

1. **Unit tests**: All new code has unit test coverage >= 80% for the modules introduced in that milestone.
2. **Integration tests**: Cross-module interactions are tested against real PostgreSQL and Redis (not mocks).
3. **Linting**: Zero lint errors from `ruff` (or equivalent) on new code.
4. **Documentation**: Public API endpoints documented in OpenAPI/Swagger spec.

### Pre-Launch Verification Checklist

Before the system goes live, ALL of the following must pass:

- [ ] **Auth flow smoke test** (D-M12.8): Registration, email verification, login, token refresh, 2FA, profile update -- all pass against production within 5 minutes of deployment.
- [ ] **OAuth2 E2E**: Google and GitHub authorization code flows complete successfully in production (with production OAuth apps, not sandbox).
- [ ] **Load test baseline**: 10,000 concurrent sessions with p95 latency < 200ms and error rate < 0.1%.
- [ ] **OWASP ZAP scan**: Zero critical or high findings against production URL.
- [ ] **GDPR export**: Test user can request and download their data within 24 hours.
- [ ] **GDPR deletion**: Test user can request deletion; PII anonymized within 30 days; hard deletion on schedule.
- [ ] **Monitoring dashboards**: All Grafana dashboards populated with real data; no gaps.
- [ ] **Alerting**: At least one alert triggered and delivered to on-call during staging test.
- [ ] **Backup restore**: Database restore from backup completes successfully on staging; RTO < 1 hour verified.
- [ ] **Rollback**: One-command rollback tested on staging; completes in < 5 minutes.
- [ ] **Rate limiting**: Verified that exceeding rate limits returns 429 with correct `Retry-After` header.
- [ ] **Account lockout**: Verified that 5 failed login attempts locks the account for 30 minutes.
- [ ] **Token theft detection**: Reuse of a revoked refresh token revokes all tokens for that user.
- [ ] **CSP headers**: Verified on production that CSP blocks inline script execution.
- [ ] **PII encryption**: Verified that raw database dump contains no plaintext emails or 2FA secrets.

### Ongoing Verification (Post-Launch)

- **Daily**: Automated smoke test against production (D-M12.8 extended).
- **Weekly**: OWASP ZAP baseline scan against staging; results compared to previous week.
- **Monthly**: Load test at 1.5x current peak to verify headroom; update capacity forecast.
- **Quarterly**: Full penetration test by external firm; findings tracked to remediation.
- **Annually**: Full GDPR compliance audit; retention policy effectiveness review.

---

## Technology Decisions & Rationale

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Password hashing | argon2id (m=65536, t=3, p=4) | OWASP 2023 recommendation; resistant to GPU-based attacks; configurable memory/time cost |
| JWT algorithm | RS256 (RSA 2048-bit) | Asymmetric: auth service holds private key, all services verify with public key; enables key rotation without redistributing secrets |
| Refresh token storage | PostgreSQL (hashed) + Redis (fast lookup) | Hashed in DB for durability; Redis for fast validation; dual-write ensures no token loss on Redis failure |
| Session store | Redis 7 with AOF persistence | Sub-millisecond reads for session validation; AOF ensures sessions survive Redis restart |
| PII encryption | AES-256-GCM with KMS envelope encryption | Industry standard; authenticated encryption prevents tampering; envelope encryption separates DEK from data |
| Rate limiting | Redis sliding window (sorted sets) | Accurate sliding window; atomic operations; minimal memory overhead; per-user and per-IP dimensions |
| 2FA | TOTP (RFC 6238) | No SMS dependency; works with all authenticator apps (Google Authenticator, Authy, 1Password); offline-capable |
| Audit log storage | PostgreSQL with monthly partitioning | Append-only partitioned table; efficient range queries; native SQL for compliance reporting; partition drops for retention |
| Email delivery | SendGrid with template IDs | Reliable delivery; template management separate from code; webhook for delivery status tracking |
| Deployment | Blue-green with automatic rollback | Zero downtime; instant rollback; health check gate prevents broken deploys from receiving traffic |
| Database migrations | golang-migrate (or Flyway) | Versioned, reversible migrations; CI integration; supports PostgreSQL-specific features (partitions, UUID) |

---

## Blast Radius Analysis

Design choices that limit the impact of individual failures:

1. **Token storage isolation**: Refresh tokens in a separate table from user data. A compromised refresh token cannot expose user PII.
2. **Redis as session cache, not session authority**: Sessions are validated against the DB on sensitive operations (password change, role change). Redis failure degrades to slower DB lookups, not auth failure.
3. **OAuth identity linking is additive**: Linking a Google account does not replace email/password. If OAuth is down, email/password still works.
4. **Audit log is append-only**: Even if the auth service is compromised, audit logs cannot be tampered with (separate table, no UPDATE/DELETE permissions for the app user).
5. **Rate limiter is separate from auth logic**: If rate limiting fails open (Redis down), auth still works. If it fails closed, users get 429s but the system is protected.
6. **Encryption keys in KMS, not in the database**: Even full database access does not yield encryption keys. Key rotation does not require re-encrypting all data (envelope encryption).

---

*End of roadmap. Total: 12 milestones, 60+ deliverables, 44-day critical path, ~10-11 weeks wall-clock with parallelization.*
