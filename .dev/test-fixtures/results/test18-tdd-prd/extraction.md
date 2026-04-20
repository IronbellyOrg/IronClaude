---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-19T00:00:00Z
generator: requirements-extraction-agent
functional_requirements: 5
nonfunctional_requirements: 5
total_requirements: 10
complexity_score: 0.72
complexity_class: HIGH
domains_detected: [backend, security, frontend, testing, devops, compliance]
risks_identified: 3
dependencies_identified: 6
success_criteria_count: 12
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 4
components_identified: 6
test_artifacts_identified: 6
migration_items_identified: 3
operational_items_identified: 5
pipeline_diagnostics: {elapsed_seconds: 122.0, started_at: "2026-04-19T15:28:39.438243+00:00", finished_at: "2026-04-19T15:30:41.457422+00:00"}
---

## Functional Requirements

### FR-AUTH-001: Login with email and password
`AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
**Acceptance Criteria:**
1. Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken.
2. Invalid credentials return 401 with error message.
3. Non-existent email returns 401 (no user enumeration).
4. Account locked after 5 failed attempts within 15 minutes.
**PRD Traceability:** FR-AUTH.1 (persistent session ≥15 min), AUTH-E1 Login.

### FR-AUTH-002: User registration with validation
`AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
**Acceptance Criteria:**
1. Valid registration returns 201 with `UserProfile` data.
2. Duplicate email returns 409 Conflict.
3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
4. `PasswordHasher` stores bcrypt hash with cost factor 12.
**PRD Traceability:** FR-AUTH.2, AUTH-E1 Registration.

### FR-AUTH-003: JWT token issuance and refresh
`TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
**Acceptance Criteria:**
1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
3. Expired refreshToken returns 401.
4. Revoked refreshToken returns 401.
**PRD Traceability:** FR-AUTH.3 (session persistence), AUTH-E2 Token Management.

### FR-AUTH-004: User profile retrieval
`AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
**Acceptance Criteria:**
1. GET `/auth/me` with valid accessToken returns `UserProfile`.
2. Expired or invalid token returns 401.
3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.
**PRD Traceability:** FR-AUTH.4, AUTH-E3 Profile.

### FR-AUTH-005: Password reset flow
`AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
**Acceptance Criteria:**
1. POST `/auth/reset-request` with valid email sends reset token via email.
2. POST `/auth/reset-confirm` with valid token updates the password hash.
3. Reset tokens expire after 1 hour.
4. Used reset tokens cannot be reused.
**PRD Traceability:** FR-AUTH.5, AUTH-E3 Password Reset.

## Non-Functional Requirements

### NFR-PERF-001: API response time
All auth endpoints must respond in < 200ms at p95. Measurement: APM tracing on `AuthService` methods. PRD: NFR-AUTH.1.

### NFR-PERF-002: Concurrent authentication
Support 500 concurrent login requests. Measurement: Load testing with k6. PRD: NFR-AUTH.1.

### NFR-REL-001: Service availability
99.9% uptime measured over 30-day rolling windows. Measurement: Uptime monitoring via health check endpoint. PRD: NFR-AUTH.2.

### NFR-SEC-001: Password hashing
`PasswordHasher` must use bcrypt with cost factor 12. Measurement: Unit test asserting bcrypt cost parameter. PRD: NFR-AUTH.3, NIST SP 800-63B.

### NFR-SEC-002: Token signing
`JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Measurement: Configuration validation test.

### NFR-COMPLIANCE-001 (from PRD): GDPR consent at registration
Users must consent to data collection at registration; consent recorded with timestamp. Source: PRD Legal & Compliance.

### NFR-COMPLIANCE-002 (from PRD): SOC2 audit logging
All auth events logged with user ID, timestamp, IP, outcome; 12-month retention. Source: PRD Legal & Compliance.

### NFR-COMPLIANCE-003 (from PRD): Data minimization
Only email, hashed password, and display name collected. Source: PRD GDPR.

## Complexity Assessment

**complexity_score: 0.72 (HIGH)**

Scoring rationale:
- **Breadth (0.20):** 5 FRs spanning login, registration, token lifecycle, profile, and password reset; 4 REST endpoints; frontend + backend integration.
- **Depth (0.18):** JWT RS256 signing, bcrypt cost 12, refresh token revocation via Redis, two-step password reset with expiring tokens.
- **Cross-cutting concerns (0.15):** Security (NFR-SEC-001/002), compliance (SOC2, GDPR, NIST), observability (Prometheus metrics, OpenTelemetry), rollout via feature flags.
- **Integration surface (0.10):** PostgreSQL, Redis, SendGrid SMTP, API Gateway, Kubernetes HPA.
- **Risk profile (0.09):** Token theft, brute-force, migration data loss — all high-impact.

Class HIGH justified by multi-component orchestration (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`), phased rollout with dual feature flags, and cross-team frontend/backend/platform dependencies.

## Architectural Constraints

| # | Constraint | Source |
|---|---|---|
| AC-001 | JWT stateless sessions with RS256 2048-bit RSA | TDD S6.4, NFR-SEC-002 |
| AC-002 | bcrypt cost factor 12 via `PasswordHasher` abstraction | TDD S6.4, NFR-SEC-001 |
| AC-003 | PostgreSQL 15+ for `UserProfile` persistence | TDD S18 |
| AC-004 | Redis 7+ for refresh token storage/revocation | TDD S18 |
| AC-005 | Node.js 20 LTS runtime | TDD S18 |
| AC-006 | URL-prefix API versioning (`/v1/auth/*`) | TDD S8.4 |
| AC-007 | TLS 1.3 for all endpoints | TDD S13 |
| AC-008 | CORS restricted to known frontend origins | TDD S13 |
| AC-009 | Quarterly JWT signing key rotation | TDD S13 |
| AC-010 | Feature flags `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH` gate rollout | TDD S19.2 |
| AC-011 | No MFA, no OAuth, no RBAC enforcement in v1.0 | TDD S3.2, PRD Scope |
| AC-012 | Stateless service — no server-side session beyond Redis refresh tokens | TDD S9 |

**Persona-driven design requirements (from PRD):**
- AC-P-001 Alex (End User): Registration < 60s; session persistence across devices; self-service password reset.
- AC-P-002 Jordan (Admin): Auth event visibility and account lock capability (downstream; logging contract required).
- AC-P-003 Sam (API Consumer): Programmatic token refresh; stable error codes; OAuth2-compatible `tokenType: "Bearer"`.

## Risk Inventory

1. **R-001 Token theft via XSS (Medium prob, High impact)** — Mitigation: accessToken memory-only in `AuthProvider`; HttpOnly cookie for refreshToken; 15-min expiry; quarterly key rotation. Contingency: revoke via `TokenManager`; force password reset.
2. **R-002 Brute-force on login (High prob, Medium impact)** — Mitigation: 10 req/min IP rate limit; lockout after 5 failed attempts in 15 min; bcrypt cost 12. Contingency: WAF IP block; CAPTCHA on `LoginPage` after 3 failures.
3. **R-003 Data loss during migration (Low prob, High impact)** — Mitigation: parallel legacy run Phases 1-2; idempotent upsert; pre-phase backup. Contingency: rollback to legacy; restore from backup.

**PRD-surfaced risks (not explicit in TDD):**
4. **R-004 Low registration adoption (Medium/High — PRD)** — Mitigation: usability testing; funnel iteration.
5. **R-005 Compliance failure from incomplete audit logging (Medium/High — PRD)** — Mitigation: validate SOC2 controls in QA; define log schema early.
6. **R-006 Email delivery failures block password reset (Low/Medium — PRD)** — Mitigation: SendGrid delivery monitoring + alerting; fallback support channel.

## Dependency Inventory

1. **PostgreSQL 15+** — `UserProfile` persistence, audit log (90d retention).
2. **Redis 7+** — `TokenManager` refresh token storage with 7-day TTL.
3. **Node.js 20 LTS** — runtime.
4. **bcryptjs** — `PasswordHasher` library.
5. **jsonwebtoken** — `JwtService` library.
6. **SendGrid** — password reset email delivery (external).
7. **API Gateway** — rate limiting, CORS (upstream).
8. **Kubernetes** — `AuthService` pod orchestration, HPA scaling.
9. **Prometheus** — metrics scraping.
10. **OpenTelemetry** — distributed tracing.
11. **AUTH-PRD-001** — parent product requirements.
12. **SEC-POLICY-001** — organizational security policy.
13. **INFRA-DB-001** — database infrastructure dependency (frontmatter `depends_on`).

## Success Criteria

**Technical (TDD S4.1):**
- SC-001 Login p95 < 200ms.
- SC-002 Registration success rate > 99%.
- SC-003 Token refresh p95 < 100ms.
- SC-004 Service availability 99.9% over 30-day windows.
- SC-005 `PasswordHasher.hash()` < 500ms with bcrypt cost 12.

**Business (TDD S4.2 + PRD):**
- SC-006 User registration conversion > 60% (TDD S4.2 / PRD).
- SC-007 ≥ 1000 DAU authenticated within 30 days of GA.
- SC-008 Average session duration > 30 minutes (PRD).
- SC-009 Failed login rate < 5% of attempts (PRD).
- SC-010 Password reset completion > 80% (PRD funnel).

**Release (TDD S24):**
- SC-011 Unit coverage ≥ 80% for `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`.
- SC-012 All 5 FRs verified by passing integration tests against real Postgres + Redis.

## Open Questions

| ID | Question | Owner | Target | Source |
|---|---|---|---|---|
| OQ-001 | Should `AuthService` support API key auth for service-to-service calls? | test-lead | 2026-04-15 | TDD S22 |
| OQ-002 | Maximum allowed `UserProfile.roles` array length? | auth-team | 2026-04-01 | TDD S22 |
| OQ-003 | Should password reset emails be sent sync or async? | Engineering | — | PRD |
| OQ-004 | Max refresh tokens per user across devices? | Product | — | PRD |
| OQ-005 | Account lockout policy thresholds (N attempts)? | Security | — | PRD (partially addressed by TDD: 5/15min) |
| OQ-006 | Support "remember me" for extended sessions? | Product | — | PRD |
| OQ-007 | PRD JTBD for Jordan (admin audit log UI) has no corresponding FR in TDD — is admin tooling in scope v1.0? | product-team | — | PRD gap analysis |

## Data Models and Interfaces

### DM-001: UserProfile
TypeScript interface persisted in PostgreSQL 15.
```ts
interface UserProfile {
  id: string; email: string; displayName: string;
  createdAt: string; updatedAt: string; lastLoginAt: string;
  roles: string[];
}
```
| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID v4 string | PK, NOT NULL | generated by `AuthService` |
| email | string | UNIQUE, NOT NULL, indexed | lowercase-normalized |
| displayName | string | NOT NULL, 2-100 chars | shown in `LoginPage`/`RegisterPage` |
| createdAt | ISO 8601 | NOT NULL, DEFAULT now() | |
| updatedAt | ISO 8601 | NOT NULL, auto-updated | |
| lastLoginAt | ISO 8601 | NULLABLE | updated on successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | enforcement downstream |

**Relationships:** 1:N with refresh token records in Redis (keyed by user id). 1:N with audit log entries (Postgres, 90-day retention).

### DM-002: AuthToken
Return-shape interface for login/refresh responses.
```ts
interface AuthToken {
  accessToken: string; refreshToken: string;
  expiresIn: number; tokenType: string;
}
```
| Field | Type | Constraints | Notes |
|---|---|---|---|
| accessToken | JWT string | NOT NULL | RS256 signed by `JwtService`; payload = user id + roles |
| refreshToken | opaque string | NOT NULL, unique | stored hashed in Redis by `TokenManager`; 7-day TTL |
| expiresIn | number | NOT NULL | always 900 (seconds) |
| tokenType | string | NOT NULL | always "Bearer" (OAuth2 compat) |

**Storage Strategy:** PostgreSQL 15 (indefinite for users, 90d for audit log); Redis 7 (7-day TTL for refresh tokens).

## API Specifications

### API-001: POST /auth/login
Auth: None · Rate limit: 10/min/IP · Versioned at `/v1/auth/login`.
Request: `{ email, password }` → 200 returns `AuthToken`.
Errors: 401 invalid creds (generic, no enumeration); 423 locked after 5 failures/15min; 429 rate-limited.
Delegates: `PasswordHasher.verify()` → `TokenManager.issueTokens()` → `JwtService`.

### API-002: POST /auth/register
Auth: None · Rate limit: 5/min/IP.
Request: `{ email, password, displayName }` → 201 returns `UserProfile`.
Errors: 400 validation (weak password, invalid email); 409 duplicate email.
Delegates: password-policy check → `PasswordHasher.hash()` (bcrypt 12) → Postgres insert.

### API-003: GET /auth/me
Auth: Bearer accessToken · Rate limit: 60/min/user.
Headers: `Authorization: Bearer <jwt>` → 200 returns full `UserProfile`.
Errors: 401 missing/expired/invalid token.

### API-004: POST /auth/refresh
Auth: refreshToken in body · Rate limit: 30/min/user.
Request: `{ refreshToken }` → 200 returns new `AuthToken` pair; old token revoked.
Errors: 401 expired/revoked refresh.

**Error envelope (all endpoints):** `{ error: { code, message, status } }` — e.g. `AUTH_INVALID_CREDENTIALS`/401.
**Governance:** URL-prefix versioning; breaking changes require new major version; additive optional fields permitted in-version.
**Note:** `/auth/reset-request` and `/auth/reset-confirm` referenced in FR-AUTH-005 but not enumerated in TDD S8.1 table — see OQ-003 (sync/async).

## Component Inventory

### COMP-001: LoginPage
Type: Frontend page/route (`/login`) · Auth: No.
Props: `onSuccess: () => void, redirectUrl?: string`.
Dependencies: `AuthProvider`, API-001. Renders email/password; stores `AuthToken` via context.

### COMP-002: RegisterPage
Type: Frontend page/route (`/register`) · Auth: No.
Props: `onSuccess: () => void, termsUrl: string`.
Dependencies: `AuthProvider`, API-002. Client-side password-strength validation before submit.

### COMP-003: ProfilePage
Type: Frontend page/route (`/profile`) · Auth: Yes.
Dependencies: `AuthProvider`, API-003. Renders `UserProfile` fields.

### COMP-004: AuthProvider
Type: React context provider (wraps App).
Props: `children: ReactNode`.
Responsibilities: holds `AuthToken` state; silent refresh via `TokenManager`; intercepts 401 → refresh or redirect to `LoginPage`; clears tokens on tab close.

### COMP-005: AuthService (backend)
Type: Backend orchestrator/facade.
Dependencies: `TokenManager`, `PasswordHasher`, `UserRepo` (Postgres), Email service.
Responsibilities: login/register/profile/reset flows; input validation; audit logging.

### COMP-006: TokenManager (+ JwtService)
Type: Backend module within `AuthService`.
Dependencies: Redis (refresh storage), `JwtService` (RS256 sign/verify).
Responsibilities: issue access+refresh pair; validate refresh; revoke on rotation; 7d TTL.

**Hierarchy (TDD S10.3):**
```
App
└─ AuthProvider
   ├─ PublicRoutes → LoginPage, RegisterPage
   └─ ProtectedRoutes → ProfilePage
```

## Testing Strategy

**Pyramid:** Unit 80% (Jest/ts-jest) · Integration 15% (Supertest + testcontainers) · E2E 5% (Playwright).
**Environments:** Local (Docker Compose PG+Redis) · CI (testcontainers) · Staging (seeded, isolated).

### TEST-001 (Unit): Login with valid credentials returns AuthToken
Component: `AuthService`. Validates FR-AUTH-001. Input: valid email+password. Expected: `AuthService.login()` invokes `PasswordHasher.verify()` then `TokenManager.issueTokens()`; returns `AuthToken` with both tokens. Mocks: `PasswordHasher`, `TokenManager`.

### TEST-002 (Unit): Login with invalid credentials returns error
Component: `AuthService`. Validates FR-AUTH-001. Expected: 401 when `PasswordHasher.verify()` → false; no `AuthToken` issued.

### TEST-003 (Unit): Token refresh with valid refresh token
Component: `TokenManager`. Validates FR-AUTH-003. Expected: validates refresh → revokes old → issues new pair via `JwtService`.

### TEST-004 (Integration): Registration persists UserProfile to database
Scope: `AuthService` + PostgreSQL. Validates FR-AUTH-002 end-to-end through `PasswordHasher` to insert.

### TEST-005 (Integration): Expired refresh token rejected by TokenManager
Scope: `TokenManager` + Redis. Validates FR-AUTH-003 Redis TTL expiration invalidates refresh tokens.

### TEST-006 (E2E): User registers and logs in
Flow: `RegisterPage` → `LoginPage` → `ProfilePage`. Validates FR-AUTH-001, FR-AUTH-002 through `AuthProvider`.

## Migration and Rollout Plan

**Strategy:** Three-phase feature-flagged rollout; parallel run with legacy auth during Phases 1-2.

### MIG-001: Phase 1 — Internal Alpha (1 week)
Deploy `AuthService` to staging; auth-team + QA test all endpoints; `LoginPage`/`RegisterPage` behind `AUTH_NEW_LOGIN` (default OFF). Exit: all FR-AUTH-001..005 pass manual; zero P0/P1.

### MIG-002: Phase 2 — Beta 10% (2 weeks)
Enable `AUTH_NEW_LOGIN` for 10% traffic; monitor p95 latency, error rate, Redis. Exit: p95 < 200ms; error < 0.1%; no Redis failures.

### MIG-003: Phase 3 — General Availability (1 week)
Remove `AUTH_NEW_LOGIN`; deprecate legacy endpoints; `AUTH_TOKEN_REFRESH` flag enables refresh flow. Exit: 99.9% uptime over 7 days; dashboards green.

**Feature flags:**
- `AUTH_NEW_LOGIN` (default OFF) — gates new `LoginPage`/login endpoint; remove after Phase 3.
- `AUTH_TOKEN_REFRESH` (default OFF) — gates refresh flow in `TokenManager`; remove Phase 3 + 2 weeks.

**Rollback procedure (ordered):**
1. Disable `AUTH_NEW_LOGIN` → route to legacy.
2. Smoke-test legacy login.
3. Root-cause `AuthService` failure via logs/traces.
4. If `UserProfile` corruption → restore from last-known-good backup.
5. Notify auth-team + platform-team via incident channel.
6. Post-mortem within 48 hours.

**Rollback triggers:** p95 > 1000ms for > 5 min; error rate > 5% for > 2 min; Redis failures > 10/min; any `UserProfile` data loss/corruption.

## Operational Readiness

### OPS-001: Runbook — AuthService down
Symptoms: 5xx on all `/auth/*`; `LoginPage`/`RegisterPage` error state. Diagnosis: pod health, PG connectivity, `PasswordHasher`/`TokenManager` init logs. Resolution: restart pods; PG failover to replica; Redis down → reject refresh (users re-login). Escalation: auth-team on-call → 15 min → platform-team.

### OPS-002: Runbook — Token refresh failures
Symptoms: unexpected logouts; `AuthProvider` redirect loop to `LoginPage`; `auth_token_refresh_total` error spike. Diagnosis: Redis connectivity, `JwtService` key access, `AUTH_TOKEN_REFRESH` flag state. Resolution: scale Redis; re-mount secrets; enable flag. Escalation: auth-team on-call → Redis issue → platform-team.

### OPS-003: On-call expectations
P1 ack within 15 min; 24/7 auth-team rotation first 2 weeks post-GA; access to k8s dashboards, Grafana, Redis CLI, PG admin; path: auth-team → test-lead → eng-manager → platform-team.

### OPS-004: Capacity planning
`AuthService`: 3 replicas, HPA to 10 at CPU > 70% (target 500 concurrent users). Postgres: 100-conn pool, grow to 200 if wait > 50ms. Redis: 1 GB (~100K tokens, ~50 MB); scale to 2 GB at > 70% utilization.

### OPS-005: Observability
**Logs:** structured JSON for login success/failure, registration, refresh, password reset; sensitive fields excluded.
**Metrics (Prometheus):** `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter).
**Tracing:** OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`.
**Alerts:** login failure rate > 20% over 5 min; p95 > 500ms; `TokenManager` Redis connection failures.
**Audit log (compliance):** user ID, event type, timestamp, IP, outcome; 12-month retention (SOC2); 90-day operational retention in Postgres.
