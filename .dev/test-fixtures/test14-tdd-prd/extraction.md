---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-17T00:00:00Z
generator: requirements-extraction-agent
functional_requirements: 5
nonfunctional_requirements: 8
total_requirements: 13
complexity_score: 0.72
complexity_class: HIGH
domains_detected: [backend, security, frontend, testing, devops, compliance]
risks_identified: 7
dependencies_identified: 7
success_criteria_count: 12
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 4
components_identified: 6
test_artifacts_identified: 6
migration_items_identified: 3
operational_items_identified: 5
pipeline_diagnostics: {elapsed_seconds: 148.0, started_at: "2026-04-17T14:26:58.872500+00:00", finished_at: "2026-04-17T14:29:26.893269+00:00"}
---

## Functional Requirements

### FR-AUTH-001: Login with email and password
`AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
**Acceptance Criteria:**
1. Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken.
2. Invalid credentials return 401 with error message.
3. Non-existent email returns 401 (no user enumeration).
4. Account locked after 5 failed attempts within 15 minutes.

**PRD Cross-reference:** FR-AUTH.1 (Alex login JTBD), AUTH-E1 epic.

### FR-AUTH-002: User registration with validation
`AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
**Acceptance Criteria:**
1. Valid registration returns 201 with `UserProfile` data.
2. Duplicate email returns 409 Conflict.
3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
4. `PasswordHasher` stores bcrypt hash with cost factor 12.

**PRD Cross-reference:** FR-AUTH.2, AUTH-E1 epic.

### FR-AUTH-003: JWT token issuance and refresh
`TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
**Acceptance Criteria:**
1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
3. Expired refreshToken returns 401.
4. Revoked refreshToken returns 401.

**PRD Cross-reference:** FR-AUTH.3 (session persistence), Sam API consumer JTBD, AUTH-E2 epic.

### FR-AUTH-004: User profile retrieval
`AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
**Acceptance Criteria:**
1. GET `/auth/me` with valid accessToken returns `UserProfile`.
2. Expired or invalid token returns 401.
3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.

**PRD Cross-reference:** FR-AUTH.4, AUTH-E3 epic.

### FR-AUTH-005: Password reset flow
`AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
**Acceptance Criteria:**
1. POST `/auth/reset-request` with valid email sends reset token via email.
2. POST `/auth/reset-confirm` with valid token updates the password hash.
3. Reset tokens expire after 1 hour.
4. Used reset tokens cannot be reused.

**PRD Cross-reference:** FR-AUTH.5, AUTH-E3 epic.

## Non-Functional Requirements

### NFR-PERF-001: API response time
All auth endpoints must respond in < 200ms at p95. Measured by APM tracing on `AuthService` methods.

### NFR-PERF-002: Concurrent authentication
Support 500 concurrent login requests. Verified via k6 load testing.

### NFR-REL-001: Service availability
99.9% uptime measured over 30-day rolling windows. Monitored via health check endpoint.

### NFR-SEC-001: Password hashing
`PasswordHasher` must use bcrypt with cost factor 12. Verified by unit test asserting bcrypt cost parameter. Aligns with NIST SP 800-63B (PRD legal/compliance).

### NFR-SEC-002: Token signing
`JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Verified via configuration validation test. RSA keys rotated quarterly.

### NFR-COMP-001: GDPR consent at registration (PRD-derived)
Users must consent to data collection at registration; consent recorded with timestamp. Source: PRD Legal & Compliance.

### NFR-COMP-002: SOC2 audit logging (PRD-derived)
All authentication events (login success/failure, registration, token refresh, password reset) must be logged with user ID, timestamp, IP, and outcome with 12-month retention. Source: PRD Legal & Compliance; TDD audit log retention is 90 days, which conflicts with PRD's 12-month requirement — see Open Questions.

### NFR-COMP-003: Data minimization (PRD-derived)
Only email, hashed password, and display name collected; no additional PII. Source: PRD GDPR data minimization.

## Complexity Assessment

**complexity_score: 0.72**
**complexity_class: HIGH**

Scoring rationale:
- **Domain breadth (0.20):** Spans backend service, security, frontend integration, testing, devops, and compliance — six domains.
- **Security criticality (0.20):** Authentication is a high-risk surface; bcrypt, RS256 JWT, refresh-token revocation, account lockout, brute-force mitigation, XSS hardening all required.
- **Integration footprint (0.15):** PostgreSQL, Redis, SendGrid, API Gateway, frontend `AuthProvider` — multiple stateful and external integrations.
- **Phased rollout with feature flags (0.10):** Three-phase rollout, two feature flags, dual-write/parallel-run with legacy auth and rollback procedures.
- **Compliance overhead (0.07):** SOC2 audit logging, GDPR consent, NIST SP 800-63B password policy add cross-cutting requirements.

Mitigating factors: well-bounded API surface (4 endpoints), no MFA/OAuth scope, no RBAC enforcement, single new service rather than cross-system refactor.

## Architectural Constraints

1. **Stateless service design:** `AuthService` is stateless; session state lives only in JWT tokens and Redis-backed refresh tokens.
2. **JWT with RS256:** `JwtService` must use RS256 with 2048-bit RSA keys, rotated quarterly.
3. **bcrypt cost factor 12:** Mandated by `PasswordHasher`; abstraction layer required for future algorithm migration.
4. **Versioning via URL prefix:** All endpoints under `/v1/auth/*` in production; breaking changes require new major version.
5. **TLS 1.3 enforcement:** All endpoints must require TLS 1.3.
6. **CORS allowlist:** Restricted to known frontend origins.
7. **API Gateway boundary:** Rate limiting and CORS handled at gateway, not within `AuthService`.
8. **Email via SendGrid:** Password reset emails delivered through SendGrid SMTP/API.
9. **Storage technology mandates:** PostgreSQL 15+ for persistence, Redis 7+ for refresh tokens, Node.js 20 LTS runtime.
10. **No social/OAuth login (v1.0):** Deferred to v1.1.
11. **No MFA (v1.0):** Deferred to v1.2.
12. **No RBAC enforcement:** `roles` field stored on `UserProfile` but not enforced by `AuthService`.

**Persona-driven design constraints (from PRD):**
- **Alex the End User:** Quick registration (<60s), seamless cross-device session persistence, self-service password recovery.
- **Jordan the Platform Admin:** Authentication event logs queryable by date range and user; account lock/unlock visibility.
- **Sam the API Consumer:** Programmatic auth with stable contracts, clear error codes, refresh-token capability without user interaction.

**Scope boundaries (from PRD S12 — validated against TDD):**
- In scope: registration, login, logout, token refresh, profile retrieval, password reset (all covered by TDD FR-AUTH-001..005).
- Out of scope: OAuth/OIDC, MFA, RBAC, social login. Permanently out of scope items not stated; v1.1+ deferrals listed.

## Risk Inventory

1. **R-001 — Token theft via XSS allows session hijacking** (severity: high). Mitigation: store accessToken in memory only (not localStorage); `AuthProvider` clears tokens on tab close; HttpOnly cookies for refreshToken; 15-minute access token expiry. Contingency: immediate revocation via `TokenManager`; force password reset on affected `UserProfile` accounts.
2. **R-002 — Brute-force attacks on login endpoint** (severity: medium). Mitigation: 10 req/min per IP gateway rate limit; account lockout after 5 failed attempts; bcrypt cost 12 on `PasswordHasher`. Contingency: WAF IP block; CAPTCHA on `LoginPage` after 3 failures.
3. **R-003 — Data loss during migration from legacy auth** (severity: high). Mitigation: parallel run with legacy during Phases 1–2; idempotent `UserProfile` upserts; full DB backup before each phase. Contingency: rollback to legacy; restore `UserProfile` from pre-migration backup.
4. **R-PRD-001 — Low registration adoption due to poor UX** (severity: high; PRD-derived business risk). Mitigation: usability testing pre-launch; iterate on funnel data.
5. **R-PRD-002 — Compliance failure from incomplete audit logging** (severity: high; PRD-derived). Mitigation: define log fields against SOC2 controls early; QA validation. Note: TDD's 90-day audit retention conflicts with PRD's 12-month requirement (see OQ-003).
6. **R-PRD-003 — Email delivery failures blocking password reset** (severity: medium; PRD-derived operational risk). Mitigation: SendGrid delivery monitoring/alerting; fallback support channel.
7. **R-PRD-004 — Security breach from implementation flaws** (severity: critical; PRD-derived). Mitigation: dedicated security review; pen-test before production.

## Dependency Inventory

1. **PostgreSQL 15+** — `UserProfile` and audit log persistence.
2. **Redis 7+** — `TokenManager` refresh token storage and revocation.
3. **Node.js 20 LTS** — service runtime.
4. **bcryptjs** — `PasswordHasher` implementation.
5. **jsonwebtoken** — `JwtService` implementation.
6. **SendGrid** (external SMTP/API) — password reset email delivery.
7. **API Gateway** — rate limiting and CORS upstream of `AuthService`.

PRD-stated dependencies cross-checked: SEC-POLICY-001 (policy), frontend routing framework (internal — implicit in `AuthProvider`), email delivery (SendGrid satisfies).

## Success Criteria

**Technical (TDD §4.1):**
1. Login p95 latency < 200ms.
2. Registration success rate > 99%.
3. Token refresh p95 latency < 100ms.
4. Service availability ≥ 99.9% uptime over 30-day windows.
5. `PasswordHasher.hash()` < 500ms with bcrypt cost 12.
6. Support 500 concurrent login requests (NFR-PERF-002).

**Business (TDD §4.2 + PRD):**
7. User registration conversion > 60% (`RegisterPage` funnel).
8. Daily active authenticated users > 1,000 within 30 days of GA (`AuthToken` issuance).
9. Average session duration > 30 minutes (PRD; token refresh event analytics).
10. Failed login rate < 5% of attempts (PRD; auth event log analysis).
11. Password reset completion > 80% (PRD; reset funnel).

**Release / Phase exit (TDD §19, §24):**
12. Phase 2 beta: p95 latency < 200ms, error rate < 0.1%, zero `TokenManager` Redis connection failures over 2 weeks at 10% traffic.

## Open Questions

1. **OQ-001 (TDD):** Should `AuthService` support API key authentication for service-to-service calls? Owner: test-lead. Target: 2026-04-15. Status: Open — deferred to v1.1 scope discussion.
2. **OQ-002 (TDD):** What is the maximum allowed `UserProfile.roles` array length? Owner: auth-team. Target: 2026-04-01. Status: Open — pending RBAC design review.
3. **OQ-003 (cross-doc conflict):** TDD §7.2 specifies 90-day audit log retention; PRD legal & compliance requires 12-month SOC2 retention. PRD wins on business intent — TDD must increase retention to 12 months or document an explicit exemption. Owner: compliance + auth-team.
4. **OQ-004 (PRD):** Synchronous vs asynchronous password reset email delivery? Owner: Engineering.
5. **OQ-005 (PRD):** Maximum number of refresh tokens allowed per user across devices? Owner: Product. Note: TDD assumes multi-device but does not cap.
6. **OQ-006 (PRD):** Account lockout policy after N consecutive failed attempts? Partially answered in TDD FR-AUTH-001 (5 attempts / 15 minutes); confirm with Security.
7. **OQ-007 (PRD):** Support a "remember me" option to extend session duration? Owner: Product. Not covered by TDD.
8. **OQ-008 (JTBD coverage):** PRD JTBD #3 (Jordan admin) — view authentication event logs, lock/unlock accounts. TDD FR-AUTH-001..005 do not include admin endpoints. Either out-of-scope or missing functional requirement.

## Data Models and Interfaces

### DM-001: UserProfile
**Storage:** PostgreSQL 15. **Retention:** Indefinite.
**Relationships:** One-to-many with refresh tokens (Redis-managed); referenced by audit log entries.

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string (UUID v4) | PRIMARY KEY, NOT NULL | Unique user identifier generated by `AuthService` |
| email | string | UNIQUE, NOT NULL, indexed, lowercase-normalized | User email |
| displayName | string | NOT NULL, 2–100 chars | Display name shown in UI |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Account creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Last profile modification |
| lastLoginAt | string (ISO 8601) | NULLABLE | Updated on successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Authorization roles; not enforced by `AuthService` |

### DM-002: AuthToken
**Storage:** refreshToken in Redis 7 with 7-day TTL; accessToken not persisted (stateless JWT).
**Relationships:** Issued for a `UserProfile`; refreshToken revoked/rotated on use.

| Field | Type | Constraints | Description |
|---|---|---|---|
| accessToken | string (JWT) | NOT NULL | Signed by `JwtService` (RS256); payload contains user id and roles |
| refreshToken | string | NOT NULL, unique | Opaque token managed by `TokenManager`; Redis-stored hashed value, 7-day TTL |
| expiresIn | number | NOT NULL | Seconds until accessToken expiration; always 900 |
| tokenType | string | NOT NULL | Always "Bearer" |

**Data flow:** API Gateway → `AuthService` → `PasswordHasher` (verify) → `TokenManager` → `JwtService` (sign access) + Redis (write hashed refresh) → response. Refresh: `AuthService` → `TokenManager` (validate + revoke old in Redis) → `JwtService` (issue new pair) → response.

**Audit log entity (implied, TDD §7.2):** Login attempts, password resets stored in PostgreSQL, 90-day retention (CONFLICT with PRD 12-month — see OQ-003).

## API Specifications

**Versioning:** URL prefix `/v1/auth/*` in production. Breaking changes require new major version; non-breaking optional fields allowed in current version.
**Common error envelope:** `{ "error": { "code": "AUTH_*", "message": "...", "status": <int> } }`.
**Auth scheme:** Bearer JWT in `Authorization` header for protected endpoints.

### API-001: POST /auth/login
- **Auth:** None. **Rate limit:** 10 req/min per IP.
- **Request body:** `{ email: string, password: string }`.
- **200 OK response:** `AuthToken` (`accessToken`, `refreshToken`, `expiresIn=900`, `tokenType="Bearer"`).
- **Errors:** 401 invalid credentials; 423 Locked after 5 failed attempts in 15 min; 429 rate limit exceeded.
- **Implements:** FR-AUTH-001.

### API-002: POST /auth/register
- **Auth:** None. **Rate limit:** 5 req/min per IP.
- **Request body:** `{ email: string, password: string, displayName: string }`.
- **201 Created response:** `UserProfile` (`id`, `email`, `displayName`, `createdAt`, `updatedAt`, `lastLoginAt: null`, `roles: ["user"]`).
- **Errors:** 400 validation (weak password, invalid email); 409 Conflict (duplicate email).
- **Implements:** FR-AUTH-002.

### API-003: GET /auth/me
- **Auth:** Required (Bearer accessToken). **Rate limit:** 60 req/min per user.
- **Request headers:** `Authorization: Bearer <accessToken>`.
- **200 OK response:** Full `UserProfile`.
- **Errors:** 401 missing/expired/invalid accessToken.
- **Implements:** FR-AUTH-004.

### API-004: POST /auth/refresh
- **Auth:** None at HTTP layer; refreshToken in body. **Rate limit:** 30 req/min per user.
- **Request body:** `{ refreshToken: string }`.
- **200 OK response:** New `AuthToken` pair (old refreshToken revoked, new issued).
- **Errors:** 401 expired/revoked refresh token.
- **Implements:** FR-AUTH-003.

**Implied endpoints (FR-AUTH-005, not enumerated in §8.1 inventory):** `POST /auth/reset-request`, `POST /auth/reset-confirm`. Listed for completeness; counted under FR-AUTH-005 acceptance criteria, not API surface count.

## Component Inventory

### COMP-001: LoginPage
- **Type:** Frontend page/route. **Location:** `/login`. **Auth required:** No.
- **Props:** `onSuccess: () => void`, `redirectUrl?: string`.
- **Dependencies:** `AuthProvider` (token storage), POST `/auth/login` (API-001).
- **Description:** Renders email/password fields; submits to `AuthService` login endpoint; stores `AuthToken` via `AuthProvider`.

### COMP-002: RegisterPage
- **Type:** Frontend page/route. **Location:** `/register`. **Auth required:** No.
- **Props:** `onSuccess: () => void`, `termsUrl: string`.
- **Dependencies:** `AuthProvider`, POST `/auth/register` (API-002), client-side password validation.
- **Description:** Renders registration form (email, password, displayName); enforces password strength client-side before calling `AuthService`.

### COMP-003: ProfilePage
- **Type:** Frontend page/route. **Location:** `/profile`. **Auth required:** Yes.
- **Dependencies:** GET `/auth/me` (API-003), `AuthProvider`.
- **Description:** Displays `UserProfile` data for authenticated user.

### COMP-004: AuthProvider
- **Type:** React context provider (shared component).
- **Props:** `children: ReactNode`.
- **Dependencies:** `TokenManager` (silent refresh), all auth API endpoints.
- **Description:** Wraps application; manages `AuthToken` state; intercepts 401 responses; triggers token refresh; redirects unauthenticated users from protected routes to `LoginPage`.

### COMP-005: AuthService
- **Type:** Backend service / orchestration facade. **Location:** Node.js 20 service.
- **Dependencies:** `PasswordHasher`, `TokenManager`, `JwtService`, PostgreSQL via UserRepo, SendGrid (reset emails).
- **Description:** Primary orchestrator for all auth flows: login, registration, profile, refresh, password reset.

### COMP-006: TokenManager + JwtService + PasswordHasher (subcomponents)
- **Type:** Backend internal modules.
- **TokenManager:** issues/refreshes/revokes `AuthToken` pairs; stores hashed refresh tokens in Redis with 7-day TTL.
- **JwtService:** signs/verifies JWT access tokens using RS256 (2048-bit RSA), 5s clock skew tolerance.
- **PasswordHasher:** bcrypt cost factor 12; abstracts algorithm for future migration.

**Hierarchy:** `App → AuthProvider → {PublicRoutes → [LoginPage, RegisterPage], ProtectedRoutes → ProfilePage}`.

## Testing Strategy

**Test pyramid (TDD §15.1):**
- Unit (80% coverage): Jest, ts-jest. Targets `AuthService` methods, `PasswordHasher`, `JwtService`, `TokenManager`, `UserProfile` validation.
- Integration (15%): Supertest + testcontainers. Targets API endpoint cycles, DB ops, Redis token storage, end-to-end flow `AuthService → PasswordHasher → DB`.
- E2E (5%): Playwright. Targets `LoginPage` flow, `RegisterPage` flow, `AuthProvider` token refresh, full registration→profile journey.

**Environments (TDD §15.3):**
- Local: Docker Compose (PostgreSQL + Redis).
- CI: testcontainers (ephemeral DBs).
- Staging: seeded test accounts, isolated from production.

### TEST-001: Login with valid credentials returns AuthToken (Unit)
**Scope:** `AuthService`. **Validates:** FR-AUTH-001. **Assertion:** `AuthService.login()` calls `PasswordHasher.verify()` then `TokenManager.issueTokens()`; returns valid `AuthToken` with both tokens.

### TEST-002: Login with invalid credentials returns error (Unit)
**Scope:** `AuthService`. **Validates:** FR-AUTH-001. **Assertion:** Returns 401 when `PasswordHasher.verify()` returns false; no `AuthToken` issued.

### TEST-003: Token refresh with valid refresh token (Unit)
**Scope:** `TokenManager`. **Validates:** FR-AUTH-003. **Assertion:** `TokenManager.refresh()` validates token, revokes old, issues new pair via `JwtService`.

### TEST-004: Registration persists UserProfile to database (Integration)
**Scope:** `AuthService` + PostgreSQL. **Validates:** FR-AUTH-002. **Assertion:** Full flow from API request through `PasswordHasher` to DB insert.

### TEST-005: Expired refresh token rejected by TokenManager (Integration)
**Scope:** `TokenManager` + Redis. **Validates:** FR-AUTH-003. **Assertion:** Redis TTL expiration correctly invalidates refresh tokens.

### TEST-006: User registers and logs in (E2E)
**Scope:** `RegisterPage → LoginPage → ProfilePage`. **Validates:** FR-AUTH-001, FR-AUTH-002. **Assertion:** Complete user journey through `AuthProvider`.

**Implicit additional coverage required (not in source test table):** NFR-SEC-001 (bcrypt cost assertion), NFR-SEC-002 (RS256 config validation), load test for NFR-PERF-002 (k6, 500 concurrent), audit-logging integration test for NFR-COMP-002.

## Migration and Rollout Plan

### MIG-001: Phase 1 — Internal Alpha (Sequence 1)
- **Duration:** 1 week.
- **Description:** Deploy `AuthService` to staging; auth-team and QA test all endpoints; `LoginPage` and `RegisterPage` available behind feature flag `AUTH_NEW_LOGIN`.
- **Success criteria:** All FR-AUTH-001..005 pass manual testing; zero P0/P1 bugs.
- **Dependencies:** None upstream.
- **Feature flag:** `AUTH_NEW_LOGIN` (OFF by default; enabled for internal users).

### MIG-002: Phase 2 — Beta at 10% (Sequence 2)
- **Duration:** 2 weeks.
- **Description:** Enable `AUTH_NEW_LOGIN` for 10% of traffic; monitor `AuthService` latency, error rates, `TokenManager` Redis usage; `AuthProvider` handles token refresh under real load.
- **Success criteria:** p95 latency < 200ms; error rate < 0.1%; zero `TokenManager` Redis connection failures.
- **Dependencies:** MIG-001 complete.
- **Rollback triggers:** p95 > 1000ms for >5 min; error rate > 5% for >2 min; >10 Redis connection failures/min; any `UserProfile` data corruption.

### MIG-003: Phase 3 — General Availability at 100% (Sequence 3)
- **Duration:** 1 week.
- **Description:** Remove `AUTH_NEW_LOGIN`; route all users through new `AuthService`; deprecate legacy auth endpoints; `AUTH_TOKEN_REFRESH` enables refresh-token flow.
- **Success criteria:** 99.9% uptime over first 7 days; all monitoring dashboards green.
- **Dependencies:** MIG-002 complete.
- **Feature flags:** Remove `AUTH_NEW_LOGIN` after Phase 3; remove `AUTH_TOKEN_REFRESH` after Phase 3 + 2 weeks.

**Feature flags (TDD §19.2):**
- `AUTH_NEW_LOGIN`: gates new `LoginPage` and login endpoint; default OFF; remove post-Phase 3.
- `AUTH_TOKEN_REFRESH`: enables refresh-token flow in `TokenManager`; when OFF only access tokens issued; remove Phase 3 + 2 weeks.

**Rollback procedure (TDD §19.3, sequential):**
1. Disable `AUTH_NEW_LOGIN`; route to legacy auth.
2. Verify legacy login operational via smoke tests.
3. Investigate `AuthService` failure root cause via structured logs/traces.
4. If `UserProfile` data corruption detected, restore from last known-good backup.
5. Notify auth-team and platform-team via incident channel.
6. Post-mortem within 48 hours of rollback.

## Operational Readiness

### OPS-001: Runbook — AuthService down
- **Symptoms:** 5xx on all `/auth/*`; `LoginPage`/`RegisterPage` show error state.
- **Diagnosis:** Check `AuthService` pod health (Kubernetes); verify PostgreSQL connectivity; check `PasswordHasher`/`TokenManager` init logs.
- **Resolution:** Restart `AuthService` pods; PostgreSQL failover to read replica if unreachable; if Redis down, `TokenManager` rejects refresh — users re-login via `LoginPage`.
- **Escalation:** Page auth-team on-call; if unresolved in 15 min, escalate to platform-team.
- **Prevention:** HPA on CPU; multi-AZ Redis; DB connection pool tuning.

### OPS-002: Runbook — Token refresh failures
- **Symptoms:** Users logged out unexpectedly; `AuthProvider` redirect-loop to `LoginPage`; `auth_token_refresh_total` error counter spikes.
- **Diagnosis:** Check Redis connectivity from `TokenManager`; verify `JwtService` signing key access; check `AUTH_TOKEN_REFRESH` flag state.
- **Resolution:** Scale Redis cluster if degraded; re-mount secrets volume if `JwtService` key unavailable; enable `AUTH_TOKEN_REFRESH` if OFF.
- **Escalation:** Page auth-team; Redis cluster issue → platform-team.
- **Prevention:** Redis HA; secret-mount monitoring.

### OPS-003: On-call expectations
- **Response time:** Acknowledge P1 alerts within 15 minutes.
- **Coverage:** auth-team 24/7 rotation during first 2 weeks post-GA.
- **Tooling:** Kubernetes dashboards, Grafana, Redis CLI, PostgreSQL admin.
- **Escalation path:** auth-team on-call → test-lead → eng-manager → platform-team.

### OPS-004: Capacity planning
- **AuthService pods:** 3 replicas baseline; HPA scales to 10 on CPU > 70%; supports 500 concurrent users.
- **PostgreSQL connections:** 100 pool size; ~50 avg concurrent queries; increase to 200 if connection wait > 50ms.
- **Redis memory:** 1 GB baseline (~100K refresh tokens, ~50 MB); scale to 2 GB at >70% utilization.

### OPS-005: Observability — logs, metrics, traces, alerts
- **Structured logs:** All authentication events (login success/failure, registration, token refresh, password reset). Sensitive fields (password, tokens) excluded.
- **Metrics (Prometheus):** `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter).
- **Distributed tracing:** OpenTelemetry spans across `AuthService → PasswordHasher → TokenManager → JwtService`.
- **Alerts:** login failure rate > 20% over 5 min; p95 latency > 500ms; `TokenManager` Redis connection failures.
- **Audit logging gap:** PRD requires SOC2-grade event log with user ID, timestamp, IP, outcome, 12-month retention; TDD specifies 90-day retention — reconcile via OQ-003.
