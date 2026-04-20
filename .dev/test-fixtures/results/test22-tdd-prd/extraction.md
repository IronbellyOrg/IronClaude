---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-19T00:00:00Z
generator: requirements-design-extraction-agent
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.75
complexity_class: HIGH
domains_detected: [backend, security, frontend, testing, devops, compliance]
risks_identified: 7
dependencies_identified: 8
success_criteria_count: 14
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 9
test_artifacts_identified: 6
migration_items_identified: 11
operational_items_identified: 10
pipeline_diagnostics: {elapsed_seconds: 143.0, started_at: "2026-04-19T18:16:14.666988+00:00", finished_at: "2026-04-19T18:18:37.686670+00:00"}
---

## Functional Requirements

### FR-AUTH-001: Login with email and password
`AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
**Acceptance Criteria:**
1. Valid credentials return 200 with `AuthToken` (accessToken + refreshToken)
2. Invalid credentials return 401 with error message
3. Non-existent email returns 401 (no user enumeration)
4. Account locked after 5 failed attempts within 15 minutes
**Source:** TDD §5.1; PRD FR-AUTH.1

### FR-AUTH-002: User registration with validation
`AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
**Acceptance Criteria:**
1. Valid registration returns 201 with `UserProfile` data
2. Duplicate email returns 409 Conflict
3. Weak passwords (<8 chars, no uppercase, no number) return 400
4. `PasswordHasher` stores bcrypt hash with cost factor 12
**Source:** TDD §5.1; PRD FR-AUTH.2

### FR-AUTH-003: JWT token issuance and refresh
`TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
**Acceptance Criteria:**
1. Login returns accessToken (15 min TTL) + refreshToken (7 day TTL)
2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair
3. Expired refreshToken returns 401
4. Revoked refreshToken returns 401
**Source:** TDD §5.1; PRD FR-AUTH.3

### FR-AUTH-004: User profile retrieval
`AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
**Acceptance Criteria:**
1. GET `/auth/me` with valid accessToken returns `UserProfile`
2. Expired or invalid token returns 401
3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles
**Source:** TDD §5.1; PRD FR-AUTH.4

### FR-AUTH-005: Password reset flow
`AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
**Acceptance Criteria:**
1. POST `/auth/reset-request` with valid email sends reset token via email
2. POST `/auth/reset-confirm` with valid token updates the password hash
3. Reset tokens expire after 1 hour
4. Used reset tokens cannot be reused
5. New password invalidates all existing sessions (PRD)
**Source:** TDD §5.1; PRD FR-AUTH.5

## Non-Functional Requirements

### NFR-PERF-001: API response time
All auth endpoints must respond in <200ms at p95. Measured via APM tracing on `AuthService` methods.

### NFR-PERF-002: Concurrent authentication
Support 500 concurrent login requests. Measured via k6 load testing.

### NFR-REL-001: Service availability
99.9% uptime measured over 30-day rolling windows. Measured via uptime monitoring on health check endpoint.

### NFR-SEC-001: Password hashing
`PasswordHasher` must use bcrypt with cost factor 12. Verified via unit test asserting bcrypt cost parameter.

### NFR-SEC-002: Token signing
`JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Verified via configuration validation test.

### NFR-COMP-001: GDPR consent at registration
Users must consent to data collection at registration. Consent recorded with timestamp.
**Source:** PRD Legal & Compliance (GDPR)

### NFR-COMP-002: SOC2 audit logging
All auth events logged with user ID, timestamp, IP, and outcome. 12-month retention.
**Source:** PRD Legal & Compliance (SOC2 Type II)

### NFR-COMP-003: NIST SP 800-63B password storage
One-way adaptive hashing. Raw passwords never persisted or logged.
**Source:** PRD Legal & Compliance (NIST SP 800-63B)

### NFR-COMP-004: GDPR data minimization
Only email, hashed password, and display name collected. No additional PII required.
**Source:** PRD Legal & Compliance (GDPR)

## Complexity Assessment

**complexity_score: 0.75**
**complexity_class: HIGH**

**Scoring Rationale:**
- Security-critical domain (auth, token, password handling): +0.20
- Multiple integrated components (AuthService, TokenManager, JwtService, PasswordHasher, UserRepo): +0.15
- Cross-stack concerns (backend API + frontend components + email service): +0.15
- Phased rollout with feature flags and rollback procedure: +0.10
- Compliance requirements (SOC2, GDPR, NIST): +0.10
- Multi-datastore coordination (PostgreSQL + Redis): +0.05

## Architectural Constraints

1. **Runtime:** Node.js 20 LTS mandated
2. **Datastores:** PostgreSQL 15+ for user data; Redis 7+ for refresh tokens
3. **Auth mechanism:** JWT stateless with refresh tokens (server-side sessions rejected)
4. **Hashing algorithm:** bcrypt cost 12 (argon2id/scrypt rejected)
5. **Token signing:** RS256 with 2048-bit RSA keys, rotated quarterly
6. **Transport:** TLS 1.3 required; CORS restricted to known frontend origins
7. **API versioning:** URL prefix `/v1/auth/*`; breaking changes require new major version
8. **Email provider:** SendGrid for password reset
9. **Deployment:** Kubernetes with HPA scaling
10. **Persona-driven design (PRD):** Must serve Alex (end user - fast UX), Jordan (admin - audit/lock tooling), Sam (API consumer - programmatic refresh)
11. **Scope boundary:** v1.0 excludes OAuth/social login, MFA, RBAC enforcement (roles field stored but not enforced)
12. **Password policy:** Must comply with NIST SP 800-63B

## Risk Inventory

1. **R-001** (High severity) — Token theft via XSS allows session hijacking. Mitigation: in-memory accessToken storage, HttpOnly cookie for refreshToken, 15-min expiry, clear on tab close. Contingency: `TokenManager` revocation + forced password reset.
2. **R-002** (Medium severity) — Brute-force attacks on login endpoint. Mitigation: API Gateway rate limiting (10 req/min/IP), 5-attempt account lockout, bcrypt cost 12. Contingency: WAF IP block, CAPTCHA after 3 failures.
3. **R-003** (High severity) — Data loss during migration from legacy auth. Mitigation: parallel operation in Phase 1-2, idempotent upserts, full DB backup before each phase. Contingency: rollback + restore.
4. **R-PRD-001** (High severity, from PRD) — Low registration adoption due to poor UX. Mitigation: pre-launch usability testing; iterate from funnel data.
5. **R-PRD-002** (Critical severity, from PRD) — Security breach from implementation flaws. Mitigation: dedicated security review; pen testing before production.
6. **R-PRD-003** (High severity, from PRD) — Compliance failure from incomplete audit logging. Mitigation: define log requirements early; validate against SOC2 in QA.
7. **R-PRD-004** (Medium severity, from PRD) — Email delivery failures blocking password reset. Mitigation: delivery monitoring/alerting; fallback support channel.

## Dependency Inventory

1. **PostgreSQL 15+** — `UserProfile` persistence, password hashes, audit log
2. **Redis 7+** — Refresh token storage and revocation via `TokenManager`
3. **Node.js 20 LTS** — Runtime
4. **bcryptjs** library — `PasswordHasher` implementation
5. **jsonwebtoken** library — `JwtService` implementation
6. **SendGrid API** — Password reset email delivery (external SMTP/API)
7. **Frontend routing framework** — Required for `/login`, `/register`, `/profile` routes
8. **SEC-POLICY-001** — Organization security policy governing password/token configurations

## Success Criteria

**Technical Metrics (from TDD §4.1):**
1. Login response time p95 < 200ms (APM on `AuthService.login()`)
2. Registration success rate > 99%
3. Token refresh latency p95 < 100ms
4. Service availability 99.9% uptime over 30-day windows
5. Password hash time < 500ms (bcrypt cost 12 benchmark)

**Business Metrics (from TDD §4.2):**
6. User registration conversion > 60% (`RegisterPage` funnel)
7. Daily active authenticated users > 1000 within 30 days of GA

**Definition of Done (from TDD §24.1):**
8. FR-AUTH-001 through FR-AUTH-005 implemented with passing tests
9. Unit test coverage >80% for `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`
10. Integration tests pass for all four API endpoints against real PostgreSQL + Redis
11. Security review complete (bcrypt cost verified, RS256 key rotation documented)
12. Performance testing confirms <200ms p95 under 500 concurrent users

**PRD Product Metrics (cross-reference):**
13. Average session duration > 30 minutes (token refresh analytics)
14. Failed login rate < 5% of attempts; Password reset completion > 80%

## Open Questions

1. **OQ-001** — Should `AuthService` support API key authentication for service-to-service calls? (Owner: test-lead, Target: 2026-04-15, Status: Open — deferred to v1.1)
2. **OQ-002** — What is the maximum allowed `UserProfile.roles` array length? (Owner: auth-team, Target: 2026-04-01, Status: Open — pending RBAC design review)
3. **OQ-PRD-001** — Should password reset emails be sent synchronously or asynchronously? (Owner: Engineering)
4. **OQ-PRD-002** — Maximum number of refresh tokens allowed per user across devices? (Owner: Product)
5. **OQ-PRD-003** — Account lockout policy after N consecutive failed login attempts? (Owner: Security) — Note: TDD §13 states 5 attempts/15 min, but PRD flags as open; TDD wins on implementation detail.
6. **OQ-PRD-004** — Should we support "remember me" to extend session duration? (Owner: Product)
7. **JTBD gap** — PRD JTBD #4 (Sam the API Consumer's programmatic auth) is partially covered by FR-AUTH-003 refresh flow; however, API key/machine-token use case (OQ-001) has no corresponding FR in v1.0.

## Data Models and Interfaces

### DM-001: UserProfile
**Storage:** PostgreSQL 15 (indefinite retention)
**Fields:**
| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string (UUID v4) | PRIMARY KEY, NOT NULL | Generated by `AuthService` |
| email | string | UNIQUE, NOT NULL, indexed | Lowercase-normalized |
| displayName | string | NOT NULL, 2-100 chars | Shown in UI |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Account creation |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Last modification |
| lastLoginAt | string (ISO 8601) | NULLABLE | Updated on login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Enforced downstream |

### DM-002: AuthToken
**Storage:** refreshToken in Redis 7 (7-day TTL); accessToken ephemeral
**Fields:**
| Field | Type | Constraints | Description |
|---|---|---|---|
| accessToken | string (JWT) | NOT NULL | RS256-signed; carries id + roles |
| refreshToken | string | NOT NULL, unique | Opaque; stored hashed in Redis |
| expiresIn | number | NOT NULL | 900 (15 min) |
| tokenType | string | NOT NULL | Always "Bearer" |

**Additional store:** Audit log in PostgreSQL 15 (90-day retention) for login attempts and password resets.

**Data Flow:** Registration → `AuthService` validates → `PasswordHasher.hash()` → PG insert. Login → PG lookup → `PasswordHasher.verify()` → `TokenManager.issueTokens()` → `JwtService.sign()` + Redis write → return `AuthToken`. Refresh → Redis lookup → revoke old → issue new pair.

## API Specifications

### API-001: POST `/auth/login`
**Auth:** None | **Rate limit:** 10 req/min per IP
**Request:** `{email, password}`
**Response 200:** `AuthToken` (accessToken, refreshToken, expiresIn=900, tokenType="Bearer")
**Errors:** 401 (invalid credentials), 429 (rate limit), 423 (account locked after 5 failed attempts)

### API-002: POST `/auth/register`
**Auth:** None | **Rate limit:** 5 req/min per IP
**Request:** `{email, password, displayName}`
**Response 201:** Full `UserProfile` (id, email, displayName, createdAt, updatedAt, lastLoginAt=null, roles=["user"])
**Errors:** 400 (validation: weak password / invalid email), 409 (email already registered)

### API-003: GET `/auth/me`
**Auth:** Required (Bearer accessToken) | **Rate limit:** 60 req/min per user
**Request headers:** `Authorization: Bearer <jwt>`
**Response 200:** `UserProfile`
**Errors:** 401 (missing / expired / invalid accessToken)

### API-004: POST `/auth/refresh`
**Auth:** None (refreshToken in body) | **Rate limit:** 30 req/min per user
**Request:** `{refreshToken}`
**Response 200:** New `AuthToken` pair (old refreshToken revoked)
**Errors:** 401 (expired or revoked refresh token)

### API-005: POST `/auth/reset-request`
**Auth:** None | **Rate limit:** not specified in TDD
**Behavior:** Sends email with reset token (1-hour TTL). Returns uniform response regardless of email existence (anti-enumeration per PRD).

### API-006: POST `/auth/reset-confirm`
**Auth:** None (reset token in body)
**Behavior:** Validates reset token, calls `PasswordHasher` to update hash, invalidates all existing sessions (per PRD). Single-use tokens.

**Error Format (all endpoints):** `{error: {code, message, status}}` e.g., `AUTH_INVALID_CREDENTIALS`.
**Versioning:** URL prefix `/v1/auth/*`. Breaking changes require new major version; non-breaking additions permitted in-version.

## Component Inventory

### COMP-001: LoginPage
**Type:** Frontend route/page (`/login`) | **Auth:** Public
**Props:** `onSuccess: () => void, redirectUrl?: string`
**Behavior:** Renders email/password fields, submits to POST `/auth/login`, stores `AuthToken` via `AuthProvider`.

### COMP-002: RegisterPage
**Type:** Frontend route/page (`/register`) | **Auth:** Public
**Props:** `onSuccess: () => void, termsUrl: string`
**Behavior:** Renders email/password/displayName fields, client-side password strength validation, submits to POST `/auth/register`.

### COMP-003: ProfilePage
**Type:** Frontend route/page (`/profile`) | **Auth:** Required
**Behavior:** Calls GET `/auth/me` and renders `UserProfile` data.

### COMP-004: AuthProvider
**Type:** React context provider (shared) | **Location:** Wraps `App`
**Props:** `children: ReactNode`
**Behavior:** Manages `AuthToken` state, silent refresh via `TokenManager`, intercepts 401s, redirects unauthenticated users to `LoginPage`, exposes `UserProfile` and auth methods.
**Hierarchy:** `App → AuthProvider → (PublicRoutes[LoginPage, RegisterPage] | ProtectedRoutes[ProfilePage])`

### COMP-005: AuthService
**Type:** Backend orchestrator (primary facade)
**Dependencies:** `TokenManager`, `PasswordHasher`, UserRepo
**Behavior:** Receives API requests; orchestrates login/register/profile/reset flows.

### COMP-006: TokenManager
**Type:** Backend service
**Dependencies:** `JwtService`, Redis
**Behavior:** Dual-token (access/refresh) lifecycle; stores refresh tokens hashed in Redis; handles revocation.

### COMP-007: JwtService
**Type:** Backend service (nested within `TokenManager`)
**Behavior:** RS256 signing/verification with 2048-bit RSA keys; 5-second clock skew tolerance.

### COMP-008: PasswordHasher
**Type:** Backend service
**Behavior:** bcrypt hash/verify with cost factor 12; algorithm abstracted for future migration.

### COMP-009: UserRepo
**Type:** Backend data access layer | **Dependencies:** PostgreSQL via pg-pool
**Behavior:** `UserProfile` CRUD operations.

## Testing Strategy

**Test Pyramid:** Unit 80% (Jest, ts-jest) | Integration 15% (Supertest, testcontainers) | E2E 5% (Playwright)

### TEST-001: Login with valid credentials returns AuthToken
**Level:** Unit | **Component:** `AuthService` | **Validates:** FR-AUTH-001
**Expected:** `AuthService.login()` calls `PasswordHasher.verify()`, then `TokenManager.issueTokens()`, returns valid `AuthToken`.

### TEST-002: Login with invalid credentials returns error
**Level:** Unit | **Component:** `AuthService` | **Validates:** FR-AUTH-001
**Expected:** Returns 401 when `PasswordHasher.verify()` returns false; no `AuthToken` issued.

### TEST-003: Token refresh with valid refresh token
**Level:** Unit | **Component:** `TokenManager` | **Validates:** FR-AUTH-003
**Expected:** Validates refresh token, revokes old, issues new `AuthToken` pair via `JwtService`.

### TEST-004: Registration persists UserProfile to database
**Level:** Integration | **Scope:** `AuthService` + PostgreSQL | **Validates:** FR-AUTH-002
**Expected:** Full flow from API request through `PasswordHasher` to database insert.

### TEST-005: Expired refresh token rejected by TokenManager
**Level:** Integration | **Scope:** `TokenManager` + Redis | **Validates:** FR-AUTH-003
**Expected:** Redis TTL expiration correctly invalidates refresh tokens.

### TEST-006: User registers and logs in (end-to-end)
**Level:** E2E | **Flow:** `RegisterPage` → `LoginPage` → ProfilePage | **Validates:** FR-AUTH-001, FR-AUTH-002
**Expected:** Complete user journey through `AuthProvider`.

**Environments:** Local (Docker Compose), CI (testcontainers), Staging (seeded test accounts).

## Migration and Rollout Plan

### MIG-001: Phase 1 - Internal Alpha
**Duration:** 1 week | **Audience:** auth-team + QA
**Tasks:** Deploy `AuthService` to staging; test all endpoints; enable `AUTH_NEW_LOGIN` for internal only.
**Exit criteria:** FR-AUTH-001 through FR-AUTH-005 pass manual testing; zero P0/P1 bugs.

### MIG-002: Phase 2 - Beta (10%)
**Duration:** 2 weeks | **Audience:** 10% of production traffic
**Tasks:** Enable `AUTH_NEW_LOGIN` for 10%; monitor latency, error rates, Redis usage.
**Exit criteria:** p95 <200ms, error rate <0.1%, no Redis connection failures.

### MIG-003: Phase 3 - General Availability (100%)
**Duration:** 1 week | **Audience:** 100%
**Tasks:** Remove `AUTH_NEW_LOGIN` flag; deprecate legacy endpoints; enable `AUTH_TOKEN_REFRESH`.
**Exit criteria:** 99.9% uptime over first 7 days; all dashboards green.

### MIG-004: Feature flag AUTH_NEW_LOGIN
**Default:** OFF | **Owner:** auth-team | **Cleanup:** After Phase 3 GA
**Purpose:** Gates access to new `LoginPage` + `AuthService` login endpoint.

### MIG-005: Feature flag AUTH_TOKEN_REFRESH
**Default:** OFF | **Owner:** auth-team | **Cleanup:** After Phase 3 + 2 weeks
**Purpose:** Enables refresh token flow in `TokenManager`; when OFF, only access tokens issued.

### MIG-006: Rollback step 1
Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth.

### MIG-007: Rollback step 2
Verify legacy login flow operational via smoke tests.

### MIG-008: Rollback step 3
Investigate `AuthService` failure root cause using structured logs + traces.

### MIG-009: Rollback step 4
If data corruption detected in `UserProfile` table, restore from last known-good backup.

### MIG-010: Rollback step 5
Notify auth-team + platform-team via incident channel.

### MIG-011: Rollback step 6
Post-mortem within 48 hours of rollback.

**Rollback Triggers:** p95 >1000ms for >5 min; error rate >5% for >2 min; Redis connection failures >10/min; any data loss/corruption in `UserProfile`.

## Operational Readiness

### OPS-001: Runbook - AuthService down
**Symptoms:** 5xx on all `/auth/*`; `LoginPage`/`RegisterPage` error state
**Diagnosis:** K8s pod health; PG connectivity; `PasswordHasher`/`TokenManager` init logs
**Resolution:** Restart pods; PG failover to read replica; Redis down → reject refresh, force re-login
**Escalation:** auth-team on-call → 15 min unresolved → platform-team

### OPS-002: Runbook - Token refresh failures
**Symptoms:** Users logged out unexpectedly; `AuthProvider` redirect loop; `auth_token_refresh_total` error spike
**Diagnosis:** Redis connectivity from `TokenManager`; `JwtService` signing key access; `AUTH_TOKEN_REFRESH` flag state
**Resolution:** Scale Redis cluster if degraded; re-mount secrets if key unavailable; enable flag if OFF
**Escalation:** auth-team on-call → Redis issue → platform-team

### OPS-003: On-call expectations
P1 acknowledgment within 15 minutes; 24/7 auth-team rotation during first 2 weeks post-GA; tooling access: K8s dashboards, Grafana, Redis CLI, PG admin; escalation path: auth-team → test-lead → eng-manager → platform-team.

### OPS-004: Capacity - AuthService pods
Current: 3 replicas | Expected: 500 concurrent users | Scaling: HPA to 10 replicas at CPU >70%.

### OPS-005: Capacity - PostgreSQL connections
Current: 100 pool size | Avg: 50 concurrent queries | Scaling: increase to 200 if wait time >50ms.

### OPS-006: Capacity - Redis memory
Current: 1 GB | Expected: ~100K refresh tokens (~50 MB) | Scaling: monitor, scale to 2 GB at >70% utilization.

### OPS-007: Metrics (Prometheus)
`auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter).

### OPS-008: Alert - login failure rate
Trigger: login failure rate >20% over 5 minutes.

### OPS-009: Alert - p95 latency breach
Trigger: p95 latency >500ms.

### OPS-010: Alert - TokenManager Redis failures
Trigger: `TokenManager` Redis connection failures.

**Observability:** Structured logs for all auth events (login success/failure, registration, token refresh, password reset); OpenTelemetry distributed tracing across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`; audit log retained 90 days in PG (12 months per PRD SOC2 requirement — PRD wins on business intent, implies retention extension needed).
