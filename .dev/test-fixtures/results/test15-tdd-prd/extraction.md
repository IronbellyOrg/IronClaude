---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-17T00:00:00Z
generator: requirements-design-extractor
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.65
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, testing, devops, compliance]
risks_identified: 7
dependencies_identified: 9
success_criteria_count: 10
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 9
test_artifacts_identified: 6
migration_items_identified: 11
operational_items_identified: 10
pipeline_diagnostics: {elapsed_seconds: 147.0, started_at: "2026-04-17T21:30:32.298837+00:00", finished_at: "2026-04-17T21:32:59.319159+00:00"}
---

## Functional Requirements

### FR-AUTH-001
Login with email and password. `AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
Acceptance: (1) Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken. (2) Invalid credentials return 401. (3) Non-existent email returns 401 (no user enumeration). (4) Account locked after 5 failed attempts within 15 minutes.
Traces to: PRD FR-AUTH.1, Epic AUTH-E1, Alex JTBD login.

### FR-AUTH-002
User registration with validation. `AuthService` must create new accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
Acceptance: (1) Valid registration returns 201 with `UserProfile`. (2) Duplicate email returns 409. (3) Weak passwords (<8 chars, no uppercase, no number) return 400. (4) `PasswordHasher` stores bcrypt hash with cost factor 12.
Traces to: PRD FR-AUTH.2, Epic AUTH-E1.

### FR-AUTH-003
JWT token issuance and refresh. `TokenManager` issues JWT access tokens (15-min expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
Acceptance: (1) Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL). (2) POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair. (3) Expired refreshToken returns 401. (4) Revoked refreshToken returns 401.
Traces to: PRD FR-AUTH.3, Epic AUTH-E2, Sam JTBD programmatic auth.

### FR-AUTH-004
User profile retrieval. `AuthService` must return authenticated user's `UserProfile` including id, email, displayName, roles, timestamps.
Acceptance: (1) GET `/auth/me` with valid accessToken returns `UserProfile`. (2) Expired/invalid token returns 401. (3) Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.
Traces to: PRD FR-AUTH.4, Epic AUTH-E3.

### FR-AUTH-005
Password reset flow. `AuthService` supports two-step reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
Acceptance: (1) POST `/auth/reset-request` with valid email sends reset token via email. (2) POST `/auth/reset-confirm` with valid token updates password hash. (3) Reset tokens expire after 1 hour. (4) Used reset tokens cannot be reused.
Traces to: PRD FR-AUTH.5, Epic AUTH-E3, Alex JTBD password recovery.

## Non-Functional Requirements

### NFR-PERF-001
API response time. All auth endpoints must respond in <200ms at p95. Measurement: APM tracing on `AuthService` methods.

### NFR-PERF-002
Concurrent authentication. Support 500 concurrent login requests. Measurement: load testing with k6.

### NFR-REL-001
Service availability. 99.9% uptime measured over 30-day rolling windows. Measurement: uptime monitoring via health check endpoint.

### NFR-SEC-001
Password hashing. `PasswordHasher` must use bcrypt with cost factor 12. Measurement: unit test asserting bcrypt cost parameter.

### NFR-SEC-002
Token signing. `JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Measurement: configuration validation test.

### NFR-COMP-001
GDPR consent at registration (sourced from PRD Legal & Compliance). Users must consent to data collection at registration; consent recorded with timestamp.

### NFR-COMP-002
SOC2 Type II audit logging (sourced from PRD). All auth events logged with user ID, timestamp, IP, and outcome. 12-month retention minimum.

### NFR-COMP-003
NIST SP 800-63B password storage (sourced from PRD). One-way adaptive hashing; raw passwords never persisted or logged.

### NFR-COMP-004
GDPR data minimization (sourced from PRD). Only email, hashed password, and display name collected. No additional PII required.

## Complexity Assessment

- complexity_score: 0.65
- complexity_class: MEDIUM

Rationale:
|Factor|Score|Weight|Notes|
|---|---|---|---|
|Functional breadth|0.6|0.2|5 FRs spanning registration, login, tokens, profile, reset|
|Non-functional demands|0.7|0.2|Strict latency (p95 <200ms), 99.9% uptime, 500 concurrent, compliance (SOC2, GDPR, NIST)|
|Integration surface|0.6|0.15|PostgreSQL, Redis, SendGrid, API Gateway, Kubernetes|
|Security sensitivity|0.8|0.2|Authentication = high blast radius; token theft, brute-force, data privacy|
|Rollout complexity|0.6|0.15|3-phase feature-flagged rollout with rollback procedures|
|Cross-team coordination|0.5|0.1|auth-team owns; frontend, platform, security reviews required|

## Architectural Constraints

- JWT-based stateless authentication (rejects server-side sessions).
- bcrypt password hashing mandated with cost factor 12; abstraction via `PasswordHasher` for future migration.
- RS256 signing with 2048-bit RSA keys, rotated quarterly.
- PostgreSQL 15+ for `UserProfile` persistence; Redis 7+ for refresh-token storage; Node.js 20 LTS runtime.
- URL-versioned API (`/v1/auth/*`); non-breaking additions only within major version.
- TLS 1.3 enforced on all endpoints; CORS restricted to known frontend origins.
- Refresh tokens stored as hashed values in Redis to limit theft blast radius.
- Self-hosted rather than third-party IdP (explicitly rejected Auth0/Firebase).
- No OAuth/OIDC, MFA, or RBAC enforcement in v1.0 (explicit non-goals).
- Persona-driven constraints (from PRD): Alex -- frictionless <60s registration, session persistence; Jordan -- admin visibility and audit log queryability; Sam -- programmatic token refresh and stable contracts.
- Scope boundary (PRD S12): email/password only; OAuth/social login and MFA deferred to later versions.

## Risk Inventory

1. R-001 (High severity) -- Token theft via XSS enabling session hijacking. Mitigation: accessToken in memory only, HttpOnly cookies for refreshToken, 15-min expiry, `AuthProvider` clears on tab close. Contingency: `TokenManager` revocation + forced password reset.
2. R-002 (Medium severity) -- Brute-force attacks on login. Mitigation: API Gateway 10 req/min rate limit, 5-attempt lockout, bcrypt cost 12. Contingency: WAF IP blocking + CAPTCHA on `LoginPage`.
3. R-003 (High severity) -- Data loss during migration from legacy auth. Mitigation: parallel run Phases 1-2, idempotent upsert, pre-phase backups. Contingency: rollback + backup restore.
4. R-PRD-001 (High severity, from PRD) -- Low registration adoption due to poor UX. Mitigation: usability testing pre-launch; funnel iteration.
5. R-PRD-002 (Critical severity, from PRD) -- Security breach from implementation flaws. Mitigation: dedicated security review; pen-testing before production.
6. R-PRD-003 (High severity, from PRD) -- Compliance failure from incomplete audit logging. Mitigation: log requirements defined early; QA validation against SOC2 controls.
7. R-PRD-004 (Medium severity, from PRD) -- Email delivery failures blocking password reset. Mitigation: delivery monitoring + alerting; support-channel fallback.

## Dependency Inventory

- PostgreSQL 15+ (infrastructure) -- `UserProfile` persistence, audit log storage.
- Redis 7+ (infrastructure) -- refresh-token storage and revocation by `TokenManager`.
- Node.js 20 LTS (runtime).
- bcryptjs (library) -- `PasswordHasher` implementation.
- jsonwebtoken (library) -- `JwtService` signing/verification.
- SendGrid API (external service) -- password reset email delivery.
- API Gateway (internal) -- rate limiting, CORS.
- Kubernetes (platform) -- `AuthService` pod orchestration, HPA.
- Frontend routing framework (internal, from PRD) -- required to render `LoginPage`, `RegisterPage`, ProfilePage.

## Success Criteria

Technical (from TDD S4.1):
- Login response time (p95) <200ms -- measured via APM on `AuthService.login()`.
- Registration success rate >99% -- ratio of successful to attempts.
- Token refresh latency (p95) <100ms -- APM on `TokenManager.refresh()`.
- Service availability 99.9% uptime over 30-day windows.
- Password hash time <500ms -- benchmark of `PasswordHasher.hash()` at cost 12.

Business (from TDD S4.2 + PRD S19):
- User registration conversion >60% (landing -> confirmed account).
- Daily active authenticated users >1000 within 30 days of GA (via `AuthToken` issuance counts).
- Average session duration >30 minutes (PRD; token-refresh analytics).
- Failed login rate <5% of attempts (PRD; auth event log analysis).
- Password reset completion rate >80% (PRD; reset-requested -> new-password-set funnel).

## Open Questions

- OQ-001 (TDD) -- Should `AuthService` support API key authentication for service-to-service calls? Owner: test-lead. Target: 2026-04-15. Status: Open; deferred to v1.1 discussion.
- OQ-002 (TDD) -- Maximum allowed `UserProfile` roles array length? Owner: auth-team. Target: 2026-04-01. Status: Open; pending RBAC design review.
- OQ-PRD-001 -- Should password reset emails be sent synchronously or asynchronously? Owner: Engineering.
- OQ-PRD-002 -- Maximum number of refresh tokens allowed per user across devices? Owner: Product. (Gap: no TDD FR covers device-session limits; Sam's JTBD for programmatic integrations could be affected.)
- OQ-PRD-003 -- Account lockout policy after N consecutive failed attempts? Owner: Security. (Partial: TDD FR-AUTH-001 sets 5/15min but PRD requests confirmation.)
- OQ-PRD-004 -- Should we support "remember me" to extend session duration? Owner: Product.
- JTBD Gap -- Jordan (Platform Admin) JTBD "see who attempted access and lock compromised accounts" has no corresponding functional requirement in the TDD. Admin/operational surface not specified beyond runbook.

## Data Models and Interfaces

### DM-001
Name: `UserProfile`. PostgreSQL 15 table.
Fields:
|Field|Type|Constraints|
|---|---|---|
|id|string (UUID v4)|PRIMARY KEY, NOT NULL|
|email|string|UNIQUE, NOT NULL, indexed, lowercase normalized|
|displayName|string|NOT NULL, 2-100 chars|
|createdAt|ISO 8601|NOT NULL, DEFAULT now()|
|updatedAt|ISO 8601|NOT NULL, auto-updated|
|lastLoginAt|ISO 8601|NULLABLE|
|roles|string[]|NOT NULL, DEFAULT ["user"]|

Relationships: referenced by `AuthToken` (user ownership in JWT payload); audit log entries reference id. Retention: indefinite.

### DM-002
Name: `AuthToken`. Transient response envelope; refresh-token record stored in Redis by `TokenManager`.
Fields:
|Field|Type|Constraints|
|---|---|---|
|accessToken|string (JWT, RS256)|NOT NULL; payload includes user id + roles|
|refreshToken|string (opaque)|NOT NULL, unique; stored in Redis with 7-day TTL|
|expiresIn|number|NOT NULL; always 900 seconds|
|tokenType|string|NOT NULL; always "Bearer"|

Relationships: refreshToken revocation surface managed by `TokenManager`. Retention: 7-day TTL in Redis.

Data Flow: Client -> API Gateway -> `AuthService` -> `PasswordHasher.verify()` -> `TokenManager.issueTokens()` -> `JwtService.sign()` -> Redis (refresh record) + PostgreSQL (lastLoginAt update) -> Response envelope.

Storage Strategy: Users indefinite in PostgreSQL; refresh tokens 7-day TTL in Redis 7; audit log 90-day retention in PostgreSQL (extendable to 12 months for SOC2 per PRD NFR-COMP-002).

## API Specifications

### API-001
POST `/auth/login`. Auth: No. Rate limit: 10 req/min per IP.
Request: `{email, password}`. Response 200: `AuthToken {accessToken, refreshToken, expiresIn, tokenType}`.
Errors: 401 invalid credentials; 423 account locked; 429 rate limited.

### API-002
POST `/auth/register`. Auth: No. Rate limit: 5 req/min per IP.
Request: `{email, password, displayName}`. Response 201: `UserProfile`.
Errors: 400 validation (weak password, invalid email); 409 email conflict.

### API-003
GET `/auth/me`. Auth: Bearer access token required. Rate limit: 60 req/min per user.
Response 200: `UserProfile` with id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.
Errors: 401 missing/expired/invalid token.

### API-004
POST `/auth/refresh`. Auth: refresh token in body. Rate limit: 30 req/min per user.
Request: `{refreshToken}`. Response 200: new `AuthToken` pair (old revoked).
Errors: 401 expired/revoked refresh token.

### API-005
POST `/auth/reset-request` (inferred from FR-AUTH-005). Auth: No.
Request: `{email}`. Response: 200 with generic confirmation (prevents enumeration). Sends time-limited (1h) reset token via email.

### API-006
POST `/auth/reset-confirm` (inferred from FR-AUTH-005). Auth: reset token.
Request: `{resetToken, newPassword}`. Response: 200 on password update; invalidates existing sessions. Errors: 400 expired/used token.

Versioning: URL-prefix `/v1/auth/*`; breaking changes require new major version; additive non-breaking changes permitted within version.
Error envelope: `{error: {code, message, status}}`.
Governance: deprecation policy not explicitly defined -- open item.

## Component Inventory

### COMP-001
Name: `LoginPage`. Type: frontend route page. Location: `/login`. Auth: No.
Props: `onSuccess: () => void, redirectUrl?: string`. Calls POST `/auth/login`; stores `AuthToken` via `AuthProvider`.

### COMP-002
Name: `RegisterPage`. Type: frontend route page. Location: `/register`. Auth: No.
Props: `onSuccess: () => void, termsUrl: string`. Client-side password strength validation; calls POST `/auth/register`.

### COMP-003
Name: ProfilePage. Type: frontend route page. Location: `/profile`. Auth: Yes.
Calls GET `/auth/me`; displays `UserProfile`.

### COMP-004
Name: `AuthProvider`. Type: React context provider. Location: app root.
Props: `children: ReactNode`. Manages `AuthToken` state, silent refresh via `TokenManager`, 401 interception, redirect to `LoginPage` for protected routes.

### COMP-005
Name: `AuthService`. Type: backend service (orchestrator). Dependencies: `PasswordHasher`, `TokenManager`, `UserRepo`. Delegated to by API Gateway.

### COMP-006
Name: `TokenManager`. Type: backend service. Dependencies: `JwtService`, Redis. Handles JWT issuance, refresh lifecycle, revocation.

### COMP-007
Name: `JwtService`. Type: backend service. Uses RS256 with 2048-bit RSA keys; 5-second clock-skew tolerance; sign/verify <5ms targets.

### COMP-008
Name: `PasswordHasher`. Type: backend service. bcrypt cost 12; abstraction permits future algorithm migration.

### COMP-009
Name: `UserRepo`. Type: backend data-access. Dependencies: PostgreSQL 15 with pg-pool.

Component hierarchy (frontend):
```
App
└── AuthProvider
    ├── PublicRoutes (LoginPage, RegisterPage)
    └── ProtectedRoutes (ProfilePage)
```

## Testing Strategy

Pyramid: Unit 80% target (Jest, ts-jest); Integration 15% (Supertest, testcontainers); E2E 5% (Playwright).

### TEST-001
Unit -- Login with valid credentials returns `AuthToken`. Component: `AuthService`. Validates FR-AUTH-001. Input: valid email/password. Expected: `PasswordHasher.verify()` then `TokenManager.issueTokens()` returns valid `AuthToken`. Mocks: `PasswordHasher`, `TokenManager`.

### TEST-002
Unit -- Login with invalid credentials returns error. Component: `AuthService`. Validates FR-AUTH-001. Input: invalid credentials. Expected: 401; no `AuthToken` issued.

### TEST-003
Unit -- Token refresh with valid refresh token. Component: `TokenManager`. Validates FR-AUTH-003. Expected: old token revoked, new `AuthToken` pair issued via `JwtService`.

### TEST-004
Integration -- Registration persists `UserProfile` to database. Scope: `AuthService` + PostgreSQL. Validates FR-AUTH-002. Full request -> `PasswordHasher` -> database insert.

### TEST-005
Integration -- Expired refresh token rejected by `TokenManager`. Scope: `TokenManager` + Redis. Validates FR-AUTH-003 expiration path.

### TEST-006
E2E -- User registers and logs in. Flow: `RegisterPage` -> `LoginPage` -> ProfilePage. Validates FR-AUTH-001, FR-AUTH-002 through `AuthProvider`.

Environments: Local (Docker Compose PG+Redis), CI (testcontainers), Staging (seeded accounts, isolated). Ownership: auth-team.

## Migration and Rollout Plan

### MIG-001
Phase 1: Internal Alpha. Duration: 1 week. Tasks: deploy `AuthService` to staging; auth-team and QA test all endpoints; `LoginPage`/`RegisterPage` behind `AUTH_NEW_LOGIN` flag. Exit: all FR-AUTH-001..005 pass manual; zero P0/P1 bugs.

### MIG-002
Phase 2: Beta (10% traffic). Duration: 2 weeks. Depends on MIG-001. Tasks: enable `AUTH_NEW_LOGIN` for 10% traffic; monitor `AuthService` latency, error rates, `TokenManager` Redis usage. Exit: p95 <200ms; error rate <0.1%; zero Redis connection failures.

### MIG-003
Phase 3: GA (100%). Duration: 1 week. Depends on MIG-002. Tasks: remove `AUTH_NEW_LOGIN` flag; deprecate legacy auth endpoints; `AUTH_TOKEN_REFRESH` flag enables refresh flow. Exit: 99.9% uptime over first 7 days; all dashboards green.

### MIG-004
Feature flag: `AUTH_NEW_LOGIN`. Purpose: gates new `LoginPage` + `AuthService` login endpoint. Default: OFF. Cleanup: after Phase 3 GA. Owner: auth-team.

### MIG-005
Feature flag: `AUTH_TOKEN_REFRESH`. Purpose: enables refresh-token flow in `TokenManager` (OFF = access-only). Default: OFF. Cleanup: Phase 3 + 2 weeks. Owner: auth-team.

### MIG-006
Rollback step 1: Disable `AUTH_NEW_LOGIN` flag to route traffic to legacy auth.

### MIG-007
Rollback step 2: Verify legacy login via smoke tests.

### MIG-008
Rollback step 3: Investigate `AuthService` failure root cause via structured logs and traces.

### MIG-009
Rollback step 4: If `UserProfile` corruption detected, restore from last known-good backup.

### MIG-010
Rollback step 5: Notify auth-team and platform-team via incident channel.

### MIG-011
Rollback step 6: Post-mortem within 48 hours.

Rollback triggers: p95 >1000ms for >5 min; error rate >5% for >2 min; Redis failures >10/min; any data loss/corruption in `UserProfile`.

## Operational Readiness

### OPS-001
Runbook -- `AuthService` down. Symptoms: 5xx on all `/auth/*`; `LoginPage`/`RegisterPage` error state. Diagnosis: Kubernetes pod health, PostgreSQL connectivity, `PasswordHasher`/`TokenManager` init logs. Resolution: restart pods; PG failover to read replica; Redis-down path forces re-login. Escalation: auth-team on-call; 15-min unresolved -> platform-team.

### OPS-002
Runbook -- Token refresh failures. Symptoms: unexpected logouts; `AuthProvider` redirect loop; `auth_token_refresh_total` error spike. Diagnosis: Redis connectivity from `TokenManager`; `JwtService` signing key availability; `AUTH_TOKEN_REFRESH` flag state. Resolution: scale Redis; re-mount secrets; re-enable flag. Escalation: auth-team on-call -> platform-team for Redis cluster.

### OPS-003
On-call expectations. Response: P1 ack <15 min. Coverage: auth-team 24/7 rotation first 2 weeks post-GA. Tooling: Kubernetes dashboards, Grafana, Redis CLI, PG admin. Escalation path: auth-team on-call -> test-lead -> eng-manager -> platform-team.

### OPS-004
Capacity -- `AuthService` pods. Current: 3 replicas. Expected: 500 concurrent users. Scaling: HPA to 10 replicas on CPU >70%.

### OPS-005
Capacity -- PostgreSQL connections. Current: pool 100. Expected: ~50 avg concurrent queries. Scaling trigger: increase to 200 if connection wait time >50ms.

### OPS-006
Capacity -- Redis memory. Current: 1 GB. Expected: ~100K refresh tokens (~50 MB). Scaling: monitor; 2 GB if >70% utilized.

### OPS-007
Metrics (Prometheus): `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter). Tracing via OpenTelemetry across `AuthService`, `PasswordHasher`, `TokenManager`, `JwtService`.

### OPS-008
Alert -- login failure rate >20% over 5 minutes.

### OPS-009
Alert -- p95 latency >500ms.

### OPS-010
Alert -- `TokenManager` Redis connection failures.

Logging: structured logs for login success/failure, registration, token refresh, password reset; sensitive fields (password, tokens) excluded from application logs; 12-month retention required for SOC2 (PRD NFR-COMP-002).
