---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-20T00:00:00Z
generator: requirements-extraction-agent
functional_requirements: 5
nonfunctional_requirements: 5
total_requirements: 10
complexity_score: 0.72
complexity_class: HIGH
domains_detected: [backend, security, frontend, testing, devops, compliance]
risks_identified: 6
dependencies_identified: 7
success_criteria_count: 12
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 4
components_identified: 6
test_artifacts_identified: 6
migration_items_identified: 3
operational_items_identified: 5
pipeline_diagnostics: {elapsed_seconds: 113.2, started_at: "2026-04-20T18:39:52.493493+00:00", finished_at: "2026-04-20T18:41:45.687147+00:00"}
---

## Functional Requirements

### FR-AUTH-001
**Login with email and password.** `AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
Acceptance:
1. Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken.
2. Invalid credentials return 401 with error message.
3. Non-existent email returns 401 (no user enumeration).
4. Account locked after 5 failed attempts within 15 minutes.

### FR-AUTH-002
**User registration with validation.** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
Acceptance:
1. Valid registration returns 201 with `UserProfile` data.
2. Duplicate email returns 409 Conflict.
3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
4. `PasswordHasher` stores bcrypt hash with cost factor 12.

### FR-AUTH-003
**JWT token issuance and refresh.** `TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
Acceptance:
1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
3. Expired refreshToken returns 401.
4. Revoked refreshToken returns 401.

### FR-AUTH-004
**User profile retrieval.** `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
Acceptance:
1. GET `/auth/me` with valid accessToken returns `UserProfile`.
2. Expired or invalid token returns 401.
3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.

### FR-AUTH-005
**Password reset flow.** `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
Acceptance:
1. POST `/auth/reset-request` with valid email sends reset token via email.
2. POST `/auth/reset-confirm` with valid token updates the password hash.
3. Reset tokens expire after 1 hour.
4. Used reset tokens cannot be reused.

## Non-Functional Requirements

### NFR-PERF-001
API response time: all auth endpoints must respond in < 200ms at p95. Measured via APM tracing on `AuthService` methods.

### NFR-PERF-002
Concurrent authentication: support 500 concurrent login requests. Validated via k6 load testing.

### NFR-REL-001
Service availability: 99.9% uptime measured over 30-day rolling windows. Validated via uptime monitoring of health check endpoint.

### NFR-SEC-001
Password hashing: `PasswordHasher` must use bcrypt with cost factor 12. Validated via unit test asserting bcrypt cost parameter.

### NFR-SEC-002
Token signing: `JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Validated via configuration test.

### NFR-COMP-001 (PRD-derived)
Compliance: audit log all auth events (user ID, event, timestamp, IP, outcome) with 12-month retention for SOC2 Type II. Passwords hashed per NIST SP 800-63B; GDPR consent captured at registration; data minimization enforced (email, hashed password, display name only).

## Complexity Assessment

complexity_score: 0.72, complexity_class: HIGH.
Rationale: multi-component backend service (AuthService, TokenManager, JwtService, PasswordHasher) with multi-store persistence (PostgreSQL + Redis), cross-cutting security posture (bcrypt, RS256, lockout, CORS, TLS 1.3), frontend integration surface (LoginPage, RegisterPage, AuthProvider), staged rollout with feature flags, compliance obligations (SOC2, GDPR, NIST SP 800-63B), and operational runbooks. Moderate scope (5 FRs / 4 endpoints) keeps it below 0.85, but security, compliance, and cross-system coordination push well above MEDIUM.

## Architectural Constraints

- Runtime: Node.js 20 LTS.
- Persistence: PostgreSQL 15+ for `UserProfile` and audit log; Redis 7+ for refresh tokens.
- Session mechanism: JWT access (15 min) + opaque refresh (7 day) via `TokenManager`/`JwtService`; stateless services.
- Cryptography: bcrypt cost 12 for passwords; RS256 with 2048-bit RSA keys (quarterly rotation) for JWT.
- Transport: TLS 1.3 enforced on all endpoints; CORS restricted to known frontend origins.
- API surface: RESTful JSON; URL-versioned (`/v1/auth/*`).
- Email: SendGrid API for password reset delivery.
- Frontend integration: React-style `AuthProvider` context wrapping routed pages; accessToken in memory, refreshToken in HttpOnly cookie.
- Parent contract: implements AUTH-PRD-001 Epics AUTH-E1/E2/E3; governed by SEC-POLICY-001.
- Persona-driven design (PRD): Alex (end user) — <60s signup, silent refresh, persistent sessions; Jordan (admin) — queryable audit logs, lockout visibility; Sam (API consumer) — programmatic auth with refresh and clear error codes.
- Scope boundaries (PRD): in-scope — registration, login, logout, refresh, profile, password reset. Out-of-scope — OAuth/social login (v1.1+), MFA (v1.2), RBAC enforcement (separate PRD).

## Risk Inventory

1. R-001 — Token theft via XSS enabling session hijacking. Severity: HIGH. Mitigation: accessToken in memory only; refreshToken in HttpOnly cookie; 15-min access TTL; `AuthProvider` clears tokens on tab close; revoke via `TokenManager` and force password reset.
2. R-002 — Brute-force attacks on login endpoint. Severity: MEDIUM. Mitigation: API Gateway rate limit 10 req/min per IP; lockout after 5 failed attempts; bcrypt cost 12; WAF IP blocks and CAPTCHA after 3 failures as contingency.
3. R-003 — Data loss during migration from legacy auth. Severity: HIGH. Mitigation: parallel run in Phase 1/2; idempotent upserts; pre-phase backups; rollback to legacy + restore from backup.
4. R-PRD-001 — Low registration adoption due to poor UX (PRD S20). Severity: MEDIUM/HIGH. Mitigation: usability testing before launch; iterate on funnel data.
5. R-PRD-002 — Compliance failure from incomplete audit logging (PRD S20). Severity: HIGH. Mitigation: define log schema early; validate SOC2 controls in QA; enforce 12-month retention.
6. R-PRD-003 — Email delivery failure blocking password reset (PRD S20). Severity: MEDIUM. Mitigation: delivery monitoring and alerting; fallback support channel.

## Dependency Inventory

- PostgreSQL 15+ (user records, audit log).
- Redis 7+ (refresh token storage/revocation).
- Node.js 20 LTS (runtime).
- `bcryptjs` (password hashing).
- `jsonwebtoken` (JWT sign/verify).
- SendGrid API (password reset email).
- API Gateway (rate limiting, CORS).
- Upstream: AUTH-PRD-001 product requirements; SEC-POLICY-001 security policy.
- Infra (PRD): provisioned PostgreSQL and frontend routing framework; email delivery infrastructure available pre-development.

## Success Criteria

- Login p95 < 200ms (APM on `AuthService.login()`).
- Registration success rate > 99%.
- Token refresh p95 < 100ms (APM on `TokenManager.refresh()`).
- Service availability 99.9% / 30 days.
- `PasswordHasher.hash()` < 500ms at bcrypt cost 12.
- Registration conversion > 60% (funnel `RegisterPage` → confirmed).
- Daily active authenticated users > 1000 within 30 days of GA.
- Unit coverage ≥ 80% across `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`.
- All four endpoints pass integration tests against real PostgreSQL/Redis.
- 500 concurrent users sustained under < 200ms p95.
- (PRD) Average session duration > 30 minutes; failed login rate < 5%.
- (PRD) Password reset completion > 80%.

## Open Questions

- OQ-001 — Should `AuthService` support API key authentication for service-to-service calls? Owner: test-lead, target 2026-04-15, deferred to v1.1.
- OQ-002 — Maximum allowed `UserProfile` roles array length? Owner: auth-team, target 2026-04-01, pending RBAC design review.
- OQ-PRD-1 — Password reset emails synchronous vs asynchronous? (PRD) Owner: Engineering.
- OQ-PRD-2 — Max refresh tokens per user across devices? (PRD) Owner: Product.
- OQ-PRD-3 — Exact lockout policy after N failed attempts (threshold/window/unlock)? (PRD) Owner: Security.
- OQ-PRD-4 — "Remember me" to extend session duration? (PRD) Owner: Product.
- JTBD coverage: PRD JTBD #2 ("pick up where I left off" across devices) lacks an explicit FR beyond token persistence — confirm whether cross-device session continuity is in scope.

## Data Models and Interfaces

### DM-001
**Name:** `UserProfile` (PostgreSQL table).
Fields:
- `id` string/UUID — PRIMARY KEY, NOT NULL.
- `email` string — UNIQUE, NOT NULL, indexed, lowercased by `AuthService`.
- `displayName` string — NOT NULL, 2-100 chars.
- `createdAt` ISO 8601 — NOT NULL, DEFAULT now().
- `updatedAt` ISO 8601 — NOT NULL, auto-updated.
- `lastLoginAt` ISO 8601 — NULLABLE; updated on successful login.
- `roles` string[] — NOT NULL, DEFAULT `["user"]`; enforcement downstream.
Relationships: referenced by audit log records; consumed by `/auth/me`, `/auth/login`, `/auth/register`.

### DM-002
**Name:** `AuthToken` (response model; refresh token stored in Redis).
Fields:
- `accessToken` JWT — NOT NULL, signed by `JwtService` (RS256), carries user id and roles.
- `refreshToken` string — NOT NULL, unique, opaque; stored in Redis (7-day TTL) by `TokenManager`, hashed at rest.
- `expiresIn` number — NOT NULL, seconds (always 900).
- `tokenType` string — NOT NULL, always `"Bearer"`.
Relationships: issued for a given `UserProfile.id`; refresh tokens revocable by `TokenManager`.

Data flow: login → `AuthService` → `PasswordHasher.verify` → `TokenManager.issueTokens` → `JwtService.sign` → persist refresh in Redis → return `AuthToken`. Registration → validate → `PasswordHasher.hash` → insert `UserProfile` → return profile.

Storage strategy:
- PostgreSQL 15 — `UserProfile` and password hashes, indefinite retention.
- Redis 7 — refresh tokens, 7-day TTL.
- PostgreSQL 15 — audit log (login attempts, password resets), 90-day retention (TDD) / 12-month for SOC2 (PRD) — reconcile during implementation.

## API Specifications

### API-001
**POST `/auth/login`** — auth: none; rate limit: 10 req/min per IP.
Request: `{ email, password }`.
Response 200: `AuthToken` (`accessToken`, `refreshToken`, `expiresIn: 900`, `tokenType: "Bearer"`).
Errors: 401 invalid credentials; 423 locked after 5 failures; 429 rate limited.

### API-002
**POST `/auth/register`** — auth: none; rate limit: 5 req/min per IP.
Request: `{ email, password, displayName }`.
Response 201: full `UserProfile`.
Errors: 400 validation (weak password, invalid email); 409 duplicate email.

### API-003
**GET `/auth/me`** — auth: Bearer accessToken; rate limit: 60 req/min per user.
Response 200: `UserProfile` (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles).
Errors: 401 missing/expired/invalid token.

### API-004
**POST `/auth/refresh`** — auth: refresh token in body; rate limit: 30 req/min per user.
Request: `{ refreshToken }`.
Response 200: new `AuthToken` pair (old refresh revoked, new issued).
Errors: 401 expired/revoked refresh token.

Governance: URL-versioned (`/v1/auth/*`). Breaking changes require new major version; additive non-breaking changes permitted within a version. Unified error envelope `{ error: { code, message, status } }` (e.g., `AUTH_INVALID_CREDENTIALS`). TLS 1.3 enforced; sensitive fields excluded from logs.

## Component Inventory

### COMP-001
**Route `/login`** → page component `LoginPage`. Auth: none. Purpose: email/password login form calling POST `/auth/login`.

### COMP-002
**Route `/register`** → page component `RegisterPage`. Auth: none. Purpose: registration form with client-side password strength validation calling POST `/auth/register`.

### COMP-003
**Route `/profile`** → page component `ProfilePage`. Auth: required. Purpose: display `UserProfile` via GET `/auth/me`.

### COMP-004
**Shared: `LoginPage`.** Props: `onSuccess: () => void`, `redirectUrl?: string`. Renders email/password, submits to `AuthService`, stores `AuthToken` via `AuthProvider`.

### COMP-005
**Shared: `RegisterPage`.** Props: `onSuccess: () => void`, `termsUrl: string`. Renders email/password/displayName, validates password strength client-side, calls `AuthService` register.

### COMP-006
**Shared: `AuthProvider`.** Props: `children: ReactNode`. Context provider managing `AuthToken` state, silent refresh via `TokenManager`, 401 interception, redirects unauthenticated users to `LoginPage`, exposes `UserProfile` and auth methods.

Hierarchy:
```
App
└─ AuthProvider
   ├─ PublicRoutes → LoginPage, RegisterPage
   └─ ProtectedRoutes → ProfilePage
```

## Testing Strategy

Test pyramid: Unit 80% (Jest/ts-jest), Integration 15% (Supertest + testcontainers), E2E 5% (Playwright).
Environments: Local (Docker Compose Postgres+Redis), CI (testcontainers), Staging (seeded test accounts, isolated).

### TEST-001
**Unit — Login with valid credentials returns `AuthToken`.** Component: `AuthService`. Validates FR-AUTH-001. Mocks `PasswordHasher.verify` → true, `TokenManager.issueTokens`; asserts returned `AuthToken` shape and call order.

### TEST-002
**Unit — Login with invalid credentials returns 401.** Component: `AuthService`. Validates FR-AUTH-001. Mocks `PasswordHasher.verify` → false; asserts 401 and no tokens issued.

### TEST-003
**Unit — Token refresh with valid refresh token.** Component: `TokenManager`. Validates FR-AUTH-003. Asserts old token revoked and new `AuthToken` pair issued via `JwtService`.

### TEST-004
**Integration — Registration persists `UserProfile` to database.** Scope: `AuthService` + PostgreSQL. Validates FR-AUTH-002 end-to-end from API request through `PasswordHasher` to DB insert.

### TEST-005
**Integration — Expired refresh token rejected by `TokenManager`.** Scope: `TokenManager` + Redis. Validates FR-AUTH-003; asserts Redis TTL expiration invalidates refresh.

### TEST-006
**E2E — User registers and logs in.** Flow: `RegisterPage` → `LoginPage` → `ProfilePage`. Validates FR-AUTH-001 and FR-AUTH-002 through `AuthProvider`.

## Migration and Rollout Plan

### MIG-001
**Phase 1 — Internal Alpha (1 week).** Deploy `AuthService` to staging; auth-team/QA test all endpoints; `LoginPage`/`RegisterPage` behind `AUTH_NEW_LOGIN` flag. Exit: all FR-AUTH-001..005 pass manual testing; zero P0/P1 bugs.

### MIG-002
**Phase 2 — Beta 10% (2 weeks).** Enable `AUTH_NEW_LOGIN` for 10% traffic; monitor latency, error rate, Redis usage; `AuthProvider` token refresh under real load. Exit: p95 < 200ms; error rate < 0.1%; no `TokenManager` Redis failures.

### MIG-003
**Phase 3 — GA 100% (1 week).** Remove `AUTH_NEW_LOGIN`; all users route through new `AuthService`; legacy endpoints deprecated; `AUTH_TOKEN_REFRESH` enables refresh flow. Exit: 99.9% uptime over first 7 days; all monitoring green.

Feature flags:
- `AUTH_NEW_LOGIN` — default OFF; remove after Phase 3 GA.
- `AUTH_TOKEN_REFRESH` — default OFF; remove 2 weeks after Phase 3.

Rollback procedure (sequential):
1. Disable `AUTH_NEW_LOGIN` to route traffic back to legacy.
2. Verify legacy login via smoke tests.
3. Investigate root cause via structured logs/traces.
4. If `UserProfile` corruption detected, restore from last known-good backup.
5. Notify auth-team and platform-team via incident channel.
6. Post-mortem within 48 hours.

Rollback triggers: p95 > 1000ms for >5 min; error rate > 5% for >2 min; `TokenManager` Redis failures > 10/min; any `UserProfile` data loss or corruption.

## Operational Readiness

### OPS-001
**Runbook — `AuthService` down.** Symptoms: 5xx on `/auth/*`; `LoginPage`/`RegisterPage` error state. Diagnosis: pod health, PostgreSQL connectivity, `PasswordHasher`/`TokenManager` init logs. Resolution: restart pods; failover Postgres to read replica; if Redis down, reject refresh (users re-login). Escalation: auth-team on-call → platform-team after 15 min.

### OPS-002
**Runbook — Token refresh failures.** Symptoms: users logged out unexpectedly; `AuthProvider` redirect loops; `auth_token_refresh_total` error spikes. Diagnosis: Redis connectivity from `TokenManager`; `JwtService` signing key availability; `AUTH_TOKEN_REFRESH` flag state. Resolution: scale Redis cluster; remount secrets; enable flag if OFF. Escalation: auth-team on-call; platform-team if Redis-cluster issue.

### OPS-003
**On-call expectations.** P1 ack within 15 min; auth-team 24/7 rotation first 2 weeks post-GA; tooling: Kubernetes dashboards, Grafana, Redis CLI, Postgres admin; escalation: on-call → test-lead → eng-manager → platform-team.

### OPS-004
**Observability.** Structured logs for login success/failure, registration, refresh, password reset (exclude passwords/tokens). Prometheus metrics: `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total`. OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`. Alerts: login failure rate > 20% over 5 min; p95 > 500ms; `TokenManager` Redis connection failures.

### OPS-005
**Capacity planning.** `AuthService`: 3 replicas baseline, HPA to 10 at CPU > 70%, target 500 concurrent users. PostgreSQL: 100-connection pool, raise to 200 if connection wait > 50ms. Redis: 1 GB baseline (~100K refresh tokens ≈ 50 MB); scale to 2 GB at > 70% utilization.
