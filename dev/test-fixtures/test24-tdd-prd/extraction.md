---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-20T00:00:00Z
generator: tdd-extraction-agent
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.78
complexity_class: HIGH
domains_detected: [backend, security, frontend, testing, devops, compliance, data]
risks_identified: 7
dependencies_identified: 7
success_criteria_count: 17
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 7
test_artifacts_identified: 6
migration_items_identified: 5
operational_items_identified: 8
pipeline_diagnostics: {elapsed_seconds: 147.2, started_at: "2026-04-20T14:46:54.720388+00:00", finished_at: "2026-04-20T14:49:21.918822+00:00"}
---

## Functional Requirements

### FR-AUTH-001
**Login with email and password.** `AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
- AC1: Valid credentials return 200 with `AuthToken` (accessToken + refreshToken).
- AC2: Invalid credentials return 401 with error message.
- AC3: Non-existent email returns 401 (no user enumeration).
- AC4: Account locked after 5 failed attempts within 15 minutes.
- Source: TDD §5.1; PRD FR-AUTH.1 (session persists ≥15 min).

### FR-AUTH-002
**User registration with validation.** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
- AC1: Valid registration returns 201 with `UserProfile` data.
- AC2: Duplicate email returns 409 Conflict.
- AC3: Weak passwords (<8 chars, no uppercase, no number) return 400.
- AC4: `PasswordHasher` stores bcrypt hash with cost factor 12.
- Source: TDD §5.1; PRD FR-AUTH.2.

### FR-AUTH-003
**JWT token issuance and refresh.** `TokenManager` must issue JWT access tokens (15-min expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
- AC1: Login returns accessToken (15 min TTL) + refreshToken (7 day TTL).
- AC2: POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
- AC3: Expired refreshToken returns 401.
- AC4: Revoked refreshToken returns 401.
- Source: TDD §5.1; PRD FR-AUTH.3, AUTH-E2.

### FR-AUTH-004
**User profile retrieval.** `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
- AC1: GET `/auth/me` with valid accessToken returns `UserProfile`.
- AC2: Expired/invalid token returns 401.
- AC3: Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.
- Source: TDD §5.1; PRD FR-AUTH.4.

### FR-AUTH-005
**Password reset flow.** `AuthService` must support two-step password reset: request (email with token) and confirmation (validate token, update password).
- AC1: POST `/auth/reset-request` sends reset token via email.
- AC2: POST `/auth/reset-confirm` with valid token updates password hash.
- AC3: Reset tokens expire after 1 hour.
- AC4: Used reset tokens cannot be reused.
- Source: TDD §5.1; PRD FR-AUTH.5 (new password invalidates all sessions).

## Non-Functional Requirements

### NFR-PERF-001
API response time: all auth endpoints respond <200ms at p95. Measured via APM tracing on `AuthService` methods. (TDD §5.2; PRD NFR-AUTH.1)

### NFR-PERF-002
Concurrent authentication: support 500 concurrent login requests. Load tested with k6. (TDD §5.2; PRD NFR-AUTH.1)

### NFR-REL-001
Service availability: 99.9% uptime over 30-day rolling windows. Monitored via health check endpoint. (TDD §5.2; PRD NFR-AUTH.2)

### NFR-SEC-001
Password hashing: `PasswordHasher` must use bcrypt with cost factor 12. Unit test asserts bcrypt cost. (TDD §5.2; PRD NFR-AUTH.3)

### NFR-SEC-002
Token signing: `JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Configuration validation test. (TDD §5.2)

### NFR-SEC-003 (from PRD)
TLS 1.3 enforced on all endpoints; sensitive fields (passwords, tokens) excluded from logs. (TDD §13)

### NFR-COMP-001 (from PRD)
GDPR consent at registration: consent recorded with timestamp. (PRD Legal & Compliance)

### NFR-COMP-002 (from PRD)
SOC2 Type II audit logging: all auth events logged with user ID, timestamp, IP, outcome; 12-month retention (TDD stores 90 days — conflict flagged in Open Questions). (PRD Legal & Compliance; TDD §7.2)

### NFR-COMP-003 (from PRD)
NIST SP 800-63B compliance for password storage and data minimization (email, hashed password, displayName only). (PRD Legal & Compliance)

## Complexity Assessment

**Score: 0.78 — Class: HIGH**

Scoring rationale:
- Security-critical domain (auth + tokens + crypto): +0.20
- Cross-component orchestration (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo`): +0.15
- Multi-store persistence (PostgreSQL + Redis + SMTP): +0.10
- Phased rollout with feature flags and rollback plan: +0.10
- Frontend integration (`AuthProvider`, `LoginPage`, `RegisterPage`): +0.08
- Compliance constraints (SOC2, GDPR, NIST): +0.10
- Moderate requirement count (5 FR + 9 NFR) bounded scope: +0.05
- Total: 0.78 → HIGH

## Architectural Constraints

1. Stateless JWT-based session mechanism; no server-side sessions.
2. bcrypt via `PasswordHasher` with cost factor 12 (abstracted for future migration).
3. `JwtService` must use RS256 with 2048-bit RSA keys rotated quarterly.
4. Refresh tokens stored hashed in Redis with 7-day TTL via `TokenManager`.
5. PostgreSQL 15+ for `UserProfile`; Redis 7+ for refresh tokens; Node.js 20 LTS runtime.
6. API versioned via URL prefix (`/v1/auth/*`); breaking changes require new major version.
7. TLS 1.3 required; CORS restricted to known frontend origins.
8. Rate limiting enforced at API Gateway (10/min login, 5/min register, 60/min /me, 30/min refresh).
9. Persona-driven design requirements (from PRD):
   - Alex (end user): <60 sec registration, seamless session persistence, self-service password reset.
   - Jordan (admin): audit trail visibility; account lock/unlock; queryable auth event logs.
   - Sam (API consumer): programmatic refresh, stable contracts, clear error codes.
10. Scope boundaries (from PRD): email/password only in v1.0; no OAuth/OIDC, no MFA, no RBAC enforcement.
11. Clock skew tolerance of 5 seconds in `JwtService` JWT validation.

## Risk Inventory

1. **R-001 — Token theft via XSS (Medium/High)**: Mitigate with in-memory accessToken storage, HttpOnly cookies for refreshToken, 15-min access expiry. Contingency: immediate `TokenManager` revocation + force password reset. (TDD §20)
2. **R-002 — Brute-force attacks on login (High/Medium)**: API Gateway rate limit (10 req/min/IP), account lockout after 5 failures, bcrypt cost 12. Contingency: WAF IP blocks + CAPTCHA on `LoginPage`. (TDD §20)
3. **R-003 — Data loss during migration from legacy auth (Low/High)**: Parallel run Phases 1–2, idempotent upsert, full DB backup. Contingency: rollback + restore from backup. (TDD §20)
4. **R-PRD-001 — Low registration adoption due to poor UX (Medium/High)**: Usability testing pre-launch, iterate on funnel data. (PRD Risk Analysis)
5. **R-PRD-002 — Security breach from implementation flaws (Low/Critical)**: Dedicated security review, penetration testing. (PRD Risk Analysis)
6. **R-PRD-003 — Compliance failure from incomplete audit logging (Medium/High)**: Define log requirements early; validate SOC2 controls in QA. *Not covered in TDD risks — surfaced from PRD.* (PRD Risk Analysis)
7. **R-PRD-004 — Email delivery failures blocking password reset (Low/Medium)**: Delivery monitoring/alerting; fallback support channel. *Not covered in TDD risks — surfaced from PRD.* (PRD Risk Analysis)

## Dependency Inventory

1. **PostgreSQL 15+** — `UserProfile` persistence, audit log storage.
2. **Redis 7+** — refresh token storage and revocation via `TokenManager`.
3. **Node.js 20 LTS** — runtime.
4. **bcryptjs** — `PasswordHasher` implementation.
5. **jsonwebtoken** — `JwtService` implementation.
6. **SendGrid (external)** — password reset email delivery (SMTP/API).
7. **Frontend routing framework** — required to render auth pages (`LoginPage`, `RegisterPage`, ProfilePage).

Related policy/document dependencies: AUTH-PRD-001, SEC-POLICY-001, INFRA-DB-001, COMPLIANCE-001 (SOC2).

## Success Criteria

**Technical (TDD §4.1):**
1. Login response time p95 <200ms.
2. Registration success rate >99%.
3. Token refresh latency p95 <100ms.
4. Service availability 99.9% uptime (30-day windows).
5. Password hash time <500ms (bcrypt cost 12).

**Business (TDD §4.2 + PRD Success Metrics):**
6. User registration conversion >60% (funnel landing → confirmed account).
7. Daily active authenticated users >1000 within 30 days of GA.
8. Average session duration >30 minutes (PRD).
9. Failed login rate <5% of attempts (PRD).
10. Password reset completion rate >80% (PRD).

**Goal-level (TDD §3.1):**
11. G-001: Secure registration/login via `AuthService` + bcrypt.
12. G-002: Stateless token sessions via `JwtService`.
13. G-003: Self-service password reset via email verification.
14. G-004: `UserProfile` CRUD via `/auth/me`.
15. G-005: Frontend integration (`LoginPage`, `RegisterPage`, `AuthProvider`).

**Release Criteria (TDD §24.1):**
16. All FR-AUTH-001 through FR-AUTH-005 implemented and test-verified; unit coverage >80%; integration tests pass against real PostgreSQL/Redis.
17. Security review complete (bcrypt cost verified, JwtService key rotation documented); 500-concurrent-user p95 <200ms validated.

## Open Questions

1. **OQ-001** (TDD): Should `AuthService` support API key authentication for service-to-service calls? Owner: test-lead, Target: 2026-04-15 — deferred to v1.1.
2. **OQ-002** (TDD): Maximum allowed `UserProfile` roles array length? Owner: auth-team, Target: 2026-04-01 — pending RBAC design review.
3. **OQ-PRD-1**: Password reset emails synchronous or asynchronous? Owner: Engineering.
4. **OQ-PRD-2**: Maximum refresh tokens per user across devices? Owner: Product.
5. **OQ-PRD-3**: Account lockout policy (N consecutive failures)? TDD states 5/15min; PRD still open — reconcile.
6. **OQ-PRD-4**: Support "remember me" to extend session duration? Owner: Product.
7. **CONFLICT-1**: Audit log retention — PRD mandates 12 months for SOC2 (NFR-COMP-002) but TDD §7.2 specifies 90 days. Requires reconciliation.
8. **JTBD-gap-1**: PRD JTBD #4 (Sam the API consumer programmatic auth) has no explicit FR — refresh is covered (FR-AUTH-003) but no dedicated API-key/service-account path.
9. **JTBD-gap-2**: Jordan the Admin persona ("view authentication event logs", "lock compromised accounts") has no FR in the TDD — audit log emission exists in §14 but no admin query/management surface.

## Data Models and Interfaces

### DM-001
**`UserProfile`** — User entity persisted in PostgreSQL 15.
```ts
interface UserProfile {
  id: string;            // UUID v4, primary key
  email: string;         // unique, indexed, lowercase normalized
  displayName: string;   // 2-100 chars
  createdAt: string;     // ISO 8601
  updatedAt: string;     // ISO 8601
  lastLoginAt: string;   // ISO 8601, nullable
  roles: string[];       // default ["user"]
}
```
|Field|Type|Constraints|
|---|---|---|
|id|string(UUID)|PK, NOT NULL|
|email|string|UNIQUE, NOT NULL, indexed, lowercase-normalized|
|displayName|string|NOT NULL, 2-100 chars|
|createdAt|string(ISO8601)|NOT NULL, DEFAULT now()|
|updatedAt|string(ISO8601)|NOT NULL, auto-updated|
|lastLoginAt|string(ISO8601)|NULLABLE; updated on each login|
|roles|string[]|NOT NULL, DEFAULT ["user"]; not enforced by `AuthService`|

Relationships: 1:N with audit log entries; 1:N with refresh tokens in Redis. Retention: indefinite.

### DM-002
**`AuthToken`** — Token pair returned by `AuthService` and `TokenManager`.
```ts
interface AuthToken {
  accessToken: string;   // JWT RS256, 15-min expiry
  refreshToken: string;  // opaque, stored in Redis 7-day TTL
  expiresIn: number;     // 900 seconds
  tokenType: string;     // "Bearer"
}
```
|Field|Type|Constraints|
|---|---|---|
|accessToken|string(JWT)|NOT NULL; RS256-signed; payload contains user id + roles|
|refreshToken|string|NOT NULL, unique; stored hashed in Redis|
|expiresIn|number|NOT NULL; always 900|
|tokenType|string|NOT NULL; always "Bearer"|

Relationships: references `UserProfile.id` in JWT payload.

**Data Flow:** Login → `PasswordHasher.verify()` → `TokenManager.issueTokens()` → `JwtService.sign()` (accessToken) + Redis SET (hashed refreshToken, TTL 7d) → response. Registration → validate → `PasswordHasher.hash()` → INSERT into PostgreSQL `users` → response.

**Storage Strategy:**
|Store|Tech|Purpose|Retention|
|---|---|---|---|
|User records|PostgreSQL 15|`UserProfile`, password hashes|Indefinite|
|Refresh tokens|Redis 7|Token storage + revocation|7-day TTL|
|Audit log|PostgreSQL 15|Login attempts, password resets|90 days (TDD) — PRD requires 12 mo|

## API Specifications

### API-001 — POST `/auth/login`
Authenticates user; returns `AuthToken`.
- Auth: No | Rate limit: 10 req/min/IP
- Request: `{ email, password }`
- Response 200: `{ accessToken, refreshToken, expiresIn: 900, tokenType: "Bearer" }`
- Errors: 401 invalid creds; 423 account locked; 429 rate limit.

### API-002 — POST `/auth/register`
Creates `UserProfile`; returns profile.
- Auth: No | Rate limit: 5 req/min/IP
- Request: `{ email, password, displayName }`
- Response 201: `UserProfile`
- Errors: 400 validation; 409 duplicate email.

### API-003 — GET `/auth/me`
Returns authenticated `UserProfile`.
- Auth: Yes (Bearer) | Rate limit: 60 req/min/user
- Request: Authorization: Bearer <accessToken>
- Response 200: `UserProfile`
- Errors: 401 missing/expired/invalid token.

### API-004 — POST `/auth/refresh`
Exchanges refresh token for new `AuthToken`; revokes old refreshToken.
- Auth: No (refresh in body) | Rate limit: 30 req/min/user
- Request: `{ refreshToken }`
- Response 200: `AuthToken`
- Errors: 401 expired/revoked.

### API-005 — POST `/auth/reset-request`
Sends password reset email with 1-hour single-use token.
- Auth: No | Rate limit: not specified (TBD)
- Request: `{ email }`
- Response: confirmation shown regardless of email registration (no enumeration).
- Errors: standard error envelope.

### API-006 — POST `/auth/reset-confirm`
Validates reset token; updates password via `PasswordHasher`; invalidates all sessions (PRD).
- Auth: No | Rate limit: not specified (TBD)
- Request: `{ token, newPassword }`
- Errors: 400 invalid/expired token; 400 weak password.

**Error Envelope:** `{ "error": { "code": "AUTH_INVALID_CREDENTIALS", "message": "...", "status": 401 } }`

**Governance/Versioning:** URL-prefix versioning (`/v1/auth/*`). Breaking changes → new major version. Non-breaking optional fields permitted within a version. Deprecation policy: not explicitly defined — flag as open question.

## Component Inventory

### COMP-001
**`LoginPage`** — Route `/login`, auth not required. Props: `onSuccess: () => void, redirectUrl?: string`. Renders email/password form; calls POST `/auth/login`; stores tokens via `AuthProvider`. Client-side CAPTCHA after 3 failed attempts (R-002 mitigation).

### COMP-002
**`RegisterPage`** — Route `/register`, auth not required. Props: `onSuccess: () => void, termsUrl: string`. Registration form (email, password, displayName); client-side password strength validation; calls POST `/auth/register`.

### COMP-003
**`ProfilePage`** — Route `/profile`, auth required. Displays `UserProfile`; calls GET `/auth/me`.

### COMP-004
**`AuthProvider`** — React Context wrapper. Props: `children: ReactNode`. Manages `AuthToken` state (in-memory access, HttpOnly-cookie refresh); intercepts 401s; triggers silent refresh via `TokenManager`; redirects unauthenticated users from protected routes to `LoginPage`.

### COMP-005
**`AuthService`** — Backend orchestrator. Delegates to `PasswordHasher`, `TokenManager`, `UserRepo`. Methods: `login`, `register`, `getProfile`, `resetRequest`, `resetConfirm`. Location: src/auth/auth-service.

### COMP-006
**`TokenManager`** — Manages JWT access + refresh lifecycle; uses `JwtService`; persists refresh tokens in Redis. Methods: `issueTokens`, `refresh`, `revoke`.

### COMP-007
**`JwtService` + `PasswordHasher`** — Crypto primitives. `JwtService` signs/verifies RS256 JWTs; `PasswordHasher` wraps bcrypt (cost 12).

**Component Hierarchy:**
```
App
├── AuthProvider
│   ├── PublicRoutes
│   │   ├── LoginPage
│   │   └── RegisterPage
│   └── ProtectedRoutes
│       └── ProfilePage
```

## Testing Strategy

**Test Pyramid (TDD §15.1):**
|Level|Coverage|Tools|Focus|
|---|---|---|---|
|Unit|80%|Jest, ts-jest|`AuthService`, `PasswordHasher`, `JwtService`, `TokenManager`, `UserProfile` validation|
|Integration|15%|Supertest, testcontainers|API endpoints, PostgreSQL, Redis|
|E2E|5%|Playwright|`LoginPage`, `RegisterPage`, `AuthProvider` refresh, full journey|

### TEST-001
**Unit — Login with valid credentials returns `AuthToken`.** Component: `AuthService`. Input: valid email/password. Expected: `PasswordHasher.verify()` called, `TokenManager.issueTokens()` returns token pair. Mocks: `PasswordHasher`, `TokenManager`. Validates FR-AUTH-001.

### TEST-002
**Unit — Login with invalid credentials returns 401.** Component: `AuthService`. Input: invalid password. Expected: 401; no `AuthToken` issued. Mocks: `PasswordHasher.verify() → false`. Validates FR-AUTH-001.

### TEST-003
**Unit — Token refresh with valid refresh token.** Component: `TokenManager`. Input: valid refreshToken. Expected: old token revoked, new pair issued via `JwtService`. Validates FR-AUTH-003.

### TEST-004
**Integration — Registration persists `UserProfile`.** Scope: `AuthService` + PostgreSQL (testcontainers). Validates full flow incl. `PasswordHasher` hash + DB insert. Validates FR-AUTH-002.

### TEST-005
**Integration — Expired refresh token rejected.** Scope: `TokenManager` + Redis. Validates Redis TTL expiration correctly invalidates tokens. Validates FR-AUTH-003.

### TEST-006
**E2E — User registers and logs in.** Flow: `RegisterPage` → `LoginPage` → ProfilePage via `AuthProvider`. Tool: Playwright. Validates FR-AUTH-001 + FR-AUTH-002.

**Test Environments:**
|Env|Purpose|Data|
|---|---|---|
|Local|Dev testing|Docker Compose (PostgreSQL + Redis)|
|CI|Pipeline|testcontainers (ephemeral)|
|Staging|Pre-prod|Seeded test accounts, isolated|

## Migration and Rollout Plan

### MIG-001
**Phase 1: Internal Alpha** | 1 week | Deploy `AuthService` to staging; auth-team + QA test all endpoints behind `AUTH_NEW_LOGIN`. Exit: all FR-AUTH-001..005 pass manual tests; zero P0/P1.

### MIG-002
**Phase 2: Beta (10%)** | 2 weeks | Enable `AUTH_NEW_LOGIN` for 10% traffic; monitor latency, error rates, Redis. Exit: p95 <200ms, error <0.1%, no Redis failures.

### MIG-003
**Phase 3: General Availability (100%)** | 1 week | Remove feature flag; legacy endpoints deprecated; `AUTH_TOKEN_REFRESH` enabled. Exit: 99.9% uptime over first 7 days.

### MIG-004
**Feature Flag — `AUTH_NEW_LOGIN`** | Gates `LoginPage`/`AuthService` login | Default OFF | Removal target: post-Phase 3 | Owner: auth-team.

### MIG-005
**Feature Flag — `AUTH_TOKEN_REFRESH`** | Enables refresh flow in `TokenManager` | Default OFF | Removal target: Phase 3 + 2 weeks | Owner: auth-team.

**Rollback Procedure (sequential):**
1. Disable `AUTH_NEW_LOGIN` → route to legacy auth.
2. Verify legacy flow via smoke tests.
3. Investigate root cause via structured logs/traces.
4. If `UserProfile` corruption: restore from last known-good backup.
5. Notify auth-team + platform-team via incident channel.
6. Post-mortem within 48 hours.

**Rollback Triggers:** p95 >1000ms for 5+ min; error rate >5% for 2+ min; Redis connection failures >10/min; any `UserProfile` data loss/corruption.

## Operational Readiness

### OPS-001
**Runbook — `AuthService` down.** Symptoms: 5xx on all `/auth/*`; `LoginPage`/`RegisterPage` error state. Diagnosis: check pod health, PostgreSQL connectivity, `PasswordHasher`/`TokenManager` init logs. Resolution: restart pods; failover to read replica; if Redis down, reject refreshes → users re-login. Escalation: auth-team on-call → 15 min → platform-team. Prevention: HPA, connection pool tuning.

### OPS-002
**Runbook — Token refresh failures.** Symptoms: unexpected logouts; `AuthProvider` redirect loop; `auth_token_refresh_total` error spike. Diagnosis: Redis connectivity from `TokenManager`; `JwtService` signing key availability; `AUTH_TOKEN_REFRESH` flag state. Resolution: scale Redis; re-mount secrets; enable flag. Escalation: auth-team on-call → platform-team for Redis cluster issues.

### OPS-003
**On-Call Expectations.** P1 ack within 15 min; 24/7 rotation first 2 weeks post-GA; tooling: K8s dashboards, Grafana, Redis CLI, PostgreSQL admin; escalation path: auth-team on-call → test-lead → eng-manager → platform-team.

### OPS-004
**Capacity — `AuthService` pods.** Current: 3 replicas. Expected: 500 concurrent users. HPA to 10 replicas on CPU >70%.

### OPS-005
**Capacity — PostgreSQL.** Current: pool 100. Expected: 50 avg concurrent queries. Scale pool to 200 if wait >50ms.

### OPS-006
**Capacity — Redis memory.** Current: 1 GB. Expected: ~100K refresh tokens (~50 MB). Scale to 2 GB at >70% utilization.

### OPS-007
**Observability — Logging / Metrics / Tracing.** Structured logs for login success/failure, registration, refresh, password reset. Prometheus metrics: `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter). OpenTelemetry tracing across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`. Sensitive fields excluded from logs.

### OPS-008
**Alerts.** Login failure rate >20% over 5 min; p95 latency >500ms; `TokenManager` Redis connection failures. Dashboards: login/refresh/registration counters + duration histograms in Grafana.
