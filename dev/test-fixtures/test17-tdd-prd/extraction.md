---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-18T00:00:00Z
generator: requirements-extraction-agent
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.65
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, testing, devops, compliance]
risks_identified: 7
dependencies_identified: 10
success_criteria_count: 12
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 6
test_artifacts_identified: 6
migration_items_identified: 7
operational_items_identified: 10
pipeline_diagnostics: {elapsed_seconds: 153.0, started_at: "2026-04-18T15:42:05.009021+00:00", finished_at: "2026-04-18T15:44:38.027310+00:00"}
---

## Functional Requirements

### FR-AUTH-001
**Login with email and password.** `AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
Acceptance:
- Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken.
- Invalid credentials return 401 with error message.
- Non-existent email returns 401 (no user enumeration).
- Account locked after 5 failed attempts within 15 minutes.

### FR-AUTH-002
**User registration with validation.** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
Acceptance:
- Valid registration returns 201 with `UserProfile` data.
- Duplicate email returns 409 Conflict.
- Weak passwords (<8 chars, no uppercase, no number) return 400.
- `PasswordHasher` stores bcrypt hash with cost factor 12.

### FR-AUTH-003
**JWT token issuance and refresh.** `TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
Acceptance:
- Login returns accessToken (15 min TTL) and refreshToken (7 day TTL).
- POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
- Expired refreshToken returns 401.
- Revoked refreshToken returns 401.

### FR-AUTH-004
**User profile retrieval.** `AuthService` must return authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
Acceptance:
- GET `/auth/me` with valid accessToken returns `UserProfile`.
- Expired or invalid token returns 401.
- Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.

### FR-AUTH-005
**Password reset flow.** `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
Acceptance:
- POST `/auth/reset-request` with valid email sends reset token via email.
- POST `/auth/reset-confirm` with valid token updates password hash.
- Reset tokens expire after 1 hour.
- Used reset tokens cannot be reused.
- (PRD FR-AUTH.5) New password invalidates all existing sessions.

## Non-Functional Requirements

### NFR-PERF-001
**API response time.** All auth endpoints must respond in <200ms at p95. Measured via APM tracing on `AuthService` methods.

### NFR-PERF-002
**Concurrent authentication.** Support 500 concurrent login requests. Measured via k6 load testing.

### NFR-REL-001
**Service availability.** 99.9% uptime measured over 30-day rolling windows. Measured via health check endpoint.

### NFR-SEC-001
**Password hashing.** `PasswordHasher` must use bcrypt with cost factor 12. Verified via unit test asserting bcrypt cost parameter.

### NFR-SEC-002
**Token signing.** `JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Verified via configuration validation test.

### NFR-COMPLIANCE-001
**GDPR consent at registration (from PRD).** Users must consent to data collection at registration; consent recorded with timestamp.

### NFR-COMPLIANCE-002
**SOC2 Type II audit logging (from PRD).** All auth events logged with user ID, timestamp, IP address, and outcome. 12-month retention. Audit log table retains 90 days per TDD S7.2 (conflict: PRD mandates 12 months — PRD wins on business intent).

### NFR-COMPLIANCE-003
**NIST SP 800-63B password storage (from PRD).** One-way adaptive hashing required; raw passwords never persisted or logged. Satisfied by NFR-SEC-001 bcrypt.

### NFR-COMPLIANCE-004
**GDPR data minimization (from PRD).** Only email, hashed password, and display name collected. No additional PII.

## Complexity Assessment

**complexity_score: 0.65 — complexity_class: MEDIUM**

Rationale:
- Scope: 5 FRs covering login, registration, token lifecycle, profile, and password reset — moderate surface area.
- Integration: PostgreSQL + Redis + SMTP (SendGrid) + API Gateway = 4 external integration points.
- Security burden: bcrypt cost tuning, RS256 key rotation, refresh token revocation, rate limiting, account lockout, anti-enumeration — high security rigor.
- Frontend surface: 3 routes + `AuthProvider` context with silent refresh — moderate.
- Rollout: 3-phase staged rollout with 2 feature flags and documented rollback — adds process complexity.
- Compliance: GDPR + SOC2 + NIST — elevates validation requirements.
- Not HIGH: no MFA, no OAuth, no RBAC enforcement, single service boundary, well-understood primitives.

## Architectural Constraints

1. **Runtime mandate:** Node.js 20 LTS.
2. **Datastore mandate:** PostgreSQL 15+ for `UserProfile` and audit log; Redis 7+ for refresh tokens.
3. **Crypto mandate:** bcrypt cost factor 12 (`PasswordHasher`); RS256 with 2048-bit RSA keys rotated quarterly (`JwtService`).
4. **API style:** RESTful JSON; URL-prefix versioning (`/v1/auth/*`).
5. **Transport:** TLS 1.3 enforced end-to-end.
6. **Token model:** Stateless JWT access tokens (15-min TTL) + opaque refresh tokens in Redis (7-day TTL).
7. **Policy anchor:** Must comply with SEC-POLICY-001 and NIST SP 800-63B.
8. **Deployment:** Kubernetes pods behind API Gateway with HPA on CPU >70%.
9. **Email provider:** SendGrid (external dependency for reset flow).
10. **Upstream requirement:** Implements AUTH-PRD-001 Epics AUTH-E1, AUTH-E2, AUTH-E3.
11. **Persona-driven constraints (from PRD):**
    - Alex (end user) — registration <60s, silent refresh, generic error messages (no enumeration).
    - Jordan (admin) — queryable audit logs by date/user required.
    - Sam (API consumer) — programmatic refresh-token flow, stable error codes, clear contracts.
12. **Scope boundary (from PRD):** Email/password only in v1.0. Out-of-scope: OAuth/OIDC (v2.0), MFA (v1.1), RBAC enforcement (separate PRD), social login.
13. **CORS:** Restricted to known frontend origins only.
14. **Clock skew tolerance:** `JwtService` accepts ±5-second skew.

## Risk Inventory

1. **R-001 Token theft via XSS (Medium/High)** — Mitigation: in-memory accessToken storage, HttpOnly cookie refreshToken, 15-min expiry. Contingency: revoke via `TokenManager`, force password reset.
2. **R-002 Brute-force on login (High/Medium)** — Mitigation: Gateway rate limit 10 req/min/IP, lockout after 5 failures, bcrypt cost 12. Contingency: WAF IP block, CAPTCHA after 3 failures.
3. **R-003 Data loss during migration (Low/High)** — Mitigation: parallel run with legacy, idempotent upserts, pre-phase backups. Contingency: rollback + restore.
4. **R-PRD-001 Low registration adoption from poor UX (Medium/High)** — Mitigation: usability testing pre-launch, iterate on funnel data.
5. **R-PRD-002 Security breach from implementation flaws (Low/Critical)** — Mitigation: dedicated security review and penetration testing before prod.
6. **R-PRD-003 Compliance failure from incomplete audit logging (Medium/High)** — Mitigation: define logging requirements early, validate against SOC2 controls in QA.
7. **R-PRD-004 Email delivery failures blocking password reset (Low/Medium)** — Mitigation: delivery monitoring/alerting, fallback support channel.

## Dependency Inventory

1. PostgreSQL 15+ (user records, audit log).
2. Redis 7+ (refresh token storage/revocation via `TokenManager`).
3. Node.js 20 LTS runtime.
4. `bcryptjs` library (used by `PasswordHasher`).
5. `jsonwebtoken` library (used by `JwtService`).
6. SendGrid API (password reset email delivery).
7. AUTH-PRD-001 (upstream product requirements).
8. SEC-POLICY-001 (security policy governing hashing/signing).
9. INFRA-DB-001 (infrastructure database provisioning).
10. Frontend routing framework (hosts `LoginPage`, `RegisterPage`, `AuthProvider`).

## Success Criteria

1. Login response time p95 <200ms (technical).
2. Registration success rate >99%.
3. Token refresh latency p95 <100ms.
4. Service availability 99.9% over 30-day windows.
5. Password hash time <500ms at bcrypt cost 12.
6. User registration conversion >60% (business).
7. Daily active authenticated users >1000 within 30 days of GA.
8. Unit test coverage >80% for `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`.
9. All 4 API endpoints meet <200ms p95 under 500 concurrent users (release gate).
10. **Average session duration >30 minutes (PRD business metric).**
11. **Failed login rate <5% of attempts (PRD business metric).**
12. **Password reset completion rate >80% of reset requests (PRD business metric).**

## Open Questions

1. **OQ-001** Should `AuthService` support API key authentication for service-to-service calls? (Owner: test-lead; target 2026-04-15; deferred to v1.1.)
2. **OQ-002** Maximum allowed `UserProfile` roles array length? (Owner: auth-team; target 2026-04-01; pending RBAC design review.)
3. **OQ-PRD-001** Should password reset emails be sent synchronously or asynchronously? (Owner: Engineering.)
4. **OQ-PRD-002** Maximum number of refresh tokens allowed per user across devices? (Owner: Product.) — Related to JTBD #4 (Sam's programmatic refresh) but lacks corresponding FR.
5. **OQ-PRD-003** Account lockout policy after N consecutive failed login attempts? (Owner: Security.) — TDD specifies 5 attempts / 15 min; PRD question may refine threshold.
6. **OQ-PRD-004** Should "remember me" be supported to extend session duration? (Owner: Product.)
7. **JTBD coverage gap:** Admin JTBD ("view auth event logs to investigate incidents") from user story AUTH-E3 admin flow has no corresponding FR in the TDD — audit log table exists (S7.2) but no query API or admin UI is specified.
8. **Audit retention conflict:** PRD mandates 12-month retention; TDD S7.2 lists 90 days. Resolution owner needed.

## Data Models and Interfaces

### DM-001 UserProfile
Persisted in PostgreSQL 15. TypeScript interface:
```ts
interface UserProfile {
  id: string;            // UUID v4, PK
  email: string;         // unique, indexed, lowercase
  displayName: string;   // 2-100 chars
  createdAt: string;     // ISO 8601
  updatedAt: string;     // ISO 8601
  lastLoginAt: string;   // ISO 8601, nullable
  roles: string[];       // default ["user"]
}
```
Fields:
|Field|Type|Constraints|Notes|
|---|---|---|---|
|id|string (UUID)|PK, NOT NULL|Generated by `AuthService`|
|email|string|UNIQUE, NOT NULL, indexed|Lowercase normalized|
|displayName|string|NOT NULL, 2-100 chars|Shown in UI|
|createdAt|ISO 8601|NOT NULL, DEFAULT now()|Creation timestamp|
|updatedAt|ISO 8601|NOT NULL, auto-updated|Modification timestamp|
|lastLoginAt|ISO 8601|NULLABLE|Set on successful login|
|roles|string[]|NOT NULL, DEFAULT ["user"]|Enforcement out of scope|

Relationships: 1→N with refresh tokens in Redis (keyed by user id); 1→N with audit log rows.

### DM-002 AuthToken
Returned by login/refresh; not persisted as a single record (accessToken ephemeral, refreshToken hashed in Redis).
```ts
interface AuthToken {
  accessToken: string;   // JWT RS256, 15-min expiry
  refreshToken: string;  // opaque, stored in Redis
  expiresIn: number;     // 900 (seconds)
  tokenType: string;     // "Bearer"
}
```
Fields:
|Field|Type|Constraints|Notes|
|---|---|---|---|
|accessToken|string (JWT)|NOT NULL|Signed by `JwtService` RS256; payload carries id + roles|
|refreshToken|string|NOT NULL, unique|Stored hashed in Redis with 7-day TTL by `TokenManager`|
|expiresIn|number|NOT NULL|Always 900|
|tokenType|string|NOT NULL|"Bearer" (OAuth2 compat)|

**Data flow:** login/register → `PasswordHasher` verify/hash → `UserProfile` read/insert in PostgreSQL → `TokenManager.issueTokens()` → `JwtService.sign()` → write hashed refreshToken in Redis → return `AuthToken`. Refresh: read refreshToken hash → validate/revoke → issue new pair. Reset: email token (1h TTL) → `PasswordHasher.hash()` → update PostgreSQL → invalidate all sessions (per PRD FR-AUTH.5).

**Storage strategy:** PostgreSQL (user records indefinite, audit log 90d per TDD / 12m per PRD — unresolved); Redis (refresh tokens 7-day TTL).

## API Specifications

Versioning: URL prefix `/v1/auth/*`. Breaking changes require major version bump; additive fields allowed within a major version. Unified JSON error envelope: `{error:{code,message,status}}`.

### API-001 POST /auth/login
Auth: none. Rate limit: 10 req/min per IP. Request: `{email, password}`. Response 200: `AuthToken`. Errors: 401 invalid credentials (generic, no enumeration); 423 Locked after 5 failures in 15 min; 429 rate limited.

### API-002 POST /auth/register
Auth: none. Rate limit: 5 req/min per IP. Request: `{email, password, displayName}`. Response 201: `UserProfile`. Errors: 400 validation (weak password, invalid email); 409 duplicate email.

### API-003 GET /auth/me
Auth: Bearer accessToken. Rate limit: 60 req/min per user. Request headers: `Authorization: Bearer <JWT>`. Response 200: `UserProfile` (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles). Errors: 401 missing/expired/invalid token.

### API-004 POST /auth/refresh
Auth: refreshToken in body. Rate limit: 30 req/min per user. Request: `{refreshToken}`. Response 200: new `AuthToken` pair; old refreshToken revoked. Errors: 401 expired or revoked.

### API-005 POST /auth/reset-request
Auth: none (implied from FR-AUTH-005). Request: `{email}`. Response 200 regardless of email registration (anti-enumeration per PRD error handling). Side effect: reset token email with 1-hour TTL.

### API-006 POST /auth/reset-confirm
Auth: none (reset token in body, implied). Request: `{token, newPassword}`. Updates password via `PasswordHasher`; invalidates all existing sessions (PRD FR-AUTH.5). Errors: 400 expired/used token; 400 weak password.

## Component Inventory

### COMP-001 /login route → LoginPage
Type: page. Auth: no. Location: frontend route `/login`. Calls API-001. Props: `onSuccess:()=>void`, `redirectUrl?:string`. Stores `AuthToken` via `AuthProvider`.

### COMP-002 /register route → RegisterPage
Type: page. Auth: no. Location: frontend route `/register`. Calls API-002. Props: `onSuccess:()=>void`, `termsUrl:string`. Validates password strength client-side before submit.

### COMP-003 /profile route → ProfilePage
Type: page. Auth: yes. Location: frontend route `/profile`. Calls API-003. Displays `UserProfile` data.

### COMP-004 AuthProvider
Type: React context provider. Location: wraps `App`. Props: `children:ReactNode`. Responsibilities: manage `AuthToken` state, intercept 401s, trigger silent refresh via `TokenManager` (API-004), redirect unauthenticated users from protected routes, expose `UserProfile` + auth methods.

### COMP-005 PublicRoutes
Type: route group. Children: `LoginPage`, `RegisterPage`. No auth required.

### COMP-006 ProtectedRoutes
Type: route group. Children: `ProfilePage`. Enforces authentication via `AuthProvider` redirect.

Hierarchy:
```
App → AuthProvider → {PublicRoutes→(LoginPage,RegisterPage), ProtectedRoutes→(ProfilePage)}
```
No explicit state store beyond `AuthProvider` context (S9 marked N/A).

## Testing Strategy

**Test pyramid:**
|Level|Coverage|Tools|Focus|Owner|
|---|---|---|---|---|
|Unit|80%|Jest, ts-jest|`AuthService`, `PasswordHasher`, `JwtService`, `TokenManager`, `UserProfile` validation|auth-team|
|Integration|15%|Supertest, testcontainers|API endpoints, PostgreSQL ops, Redis token storage|auth-team|
|E2E|5%|Playwright|`LoginPage`, `RegisterPage`, `AuthProvider` refresh, full journey|QA|

**Environments:** Local (docker-compose PG+Redis) / CI (testcontainers) / Staging (seeded test accounts, isolated).

### TEST-001 Login with valid credentials returns AuthToken
Level: unit. Component: `AuthService`. Input: valid email/password. Mocks: `PasswordHasher.verify()`=true, `TokenManager.issueTokens()`. Expected: 200 + valid `AuthToken` with access+refresh. Validates FR-AUTH-001.

### TEST-002 Login with invalid credentials returns 401
Level: unit. Component: `AuthService`. Input: wrong password. Mocks: `PasswordHasher.verify()`=false. Expected: 401; no `AuthToken` issued; no `TokenManager` call. Validates FR-AUTH-001.

### TEST-003 Token refresh with valid refresh token
Level: unit. Component: `TokenManager`. Input: valid refreshToken. Mocks: Redis lookup hit, `JwtService.sign()`. Expected: old token revoked; new pair issued. Validates FR-AUTH-003.

### TEST-004 Registration persists UserProfile to database
Level: integration. Scope: `AuthService` + PostgreSQL via testcontainers. Input: valid registration payload. Expected: 201 + row in `users` table; password column is bcrypt hash. Validates FR-AUTH-002.

### TEST-005 Expired refresh token rejected by TokenManager
Level: integration. Scope: `TokenManager` + Redis. Input: refreshToken past 7-day TTL. Expected: 401 on API-004. Validates FR-AUTH-003.

### TEST-006 User registers and logs in
Level: E2E. Flow: `RegisterPage` → `LoginPage` → ProfilePage. Tool: Playwright. Validates FR-AUTH-001 + FR-AUTH-002 through `AuthProvider`.

## Migration and Rollout Plan

### MIG-001 Phase 1: Internal Alpha
Duration: 1 week. Tasks: deploy `AuthService` to staging; auth-team + QA test all endpoints; `LoginPage`/`RegisterPage` behind `AUTH_NEW_LOGIN`. Exit: FR-AUTH-001..005 pass; zero P0/P1 bugs. Depends on: INFRA-DB-001 provisioned.

### MIG-002 Phase 2: Beta (10%)
Duration: 2 weeks. Tasks: enable `AUTH_NEW_LOGIN` at 10% traffic; monitor latency, error rate, Redis; validate `AuthProvider` refresh under load. Exit: p95 <200ms, error rate <0.1%, no `TokenManager` Redis failures. Depends on: MIG-001 complete.

### MIG-003 Phase 3: GA (100%)
Duration: 1 week. Tasks: remove `AUTH_NEW_LOGIN` flag; route all users; deprecate legacy endpoints; enable `AUTH_TOKEN_REFRESH`. Exit: 99.9% uptime over 7 days; all dashboards green. Depends on: MIG-002 complete.

### MIG-004 Feature flag AUTH_NEW_LOGIN
Purpose: gate access to new `LoginPage`/`AuthService`. Default OFF. Owner: auth-team. Cleanup: remove after MIG-003 GA.

### MIG-005 Feature flag AUTH_TOKEN_REFRESH
Purpose: enable refresh token flow in `TokenManager`; when OFF only access tokens issued. Default OFF. Owner: auth-team. Cleanup: remove MIG-003 + 2 weeks.

### MIG-006 Rollback procedure
Ordered steps: (1) disable `AUTH_NEW_LOGIN` → legacy auth; (2) smoke-test legacy login; (3) investigate `AuthService` root cause via logs/traces; (4) if `UserProfile` corruption, restore from last known-good backup; (5) notify auth-team + platform-team; (6) post-mortem within 48h.

### MIG-007 Rollback criteria
Triggers: p95 >1000ms for >5 min; error rate >5% for >2 min; `TokenManager` Redis failures >10/min; any `UserProfile` data loss/corruption.

## Operational Readiness

### OPS-001 Runbook: AuthService down
Symptoms: 5xx across `/auth/*`; `LoginPage`/`RegisterPage` error state. Diagnosis: pod health, PostgreSQL connectivity, `PasswordHasher`/`TokenManager` init logs. Resolution: restart pods; PG failover to replica; if Redis down, refresh rejected → users re-login. Escalation: auth-team on-call → platform-team after 15 min. Prevention: health-check monitoring, replica warm.

### OPS-002 Runbook: Token refresh failures
Symptoms: users report unexpected logouts; `AuthProvider` redirect loop; `auth_token_refresh_total` error spike. Diagnosis: Redis connectivity, `JwtService` key mount, `AUTH_TOKEN_REFRESH` flag state. Resolution: scale Redis; re-mount secrets volume; enable flag if off. Escalation: auth-team → platform-team for Redis cluster issues. Prevention: key rotation runbook, Redis memory alerts.

### OPS-003 On-call expectations
P1 ack within 15 min. auth-team 24/7 coverage first 2 weeks post-GA. Tooling: k8s dashboards, Grafana, Redis CLI, PG admin. Escalation: on-call → test-lead → eng-manager → platform-team. Knowledge prerequisites: JWT signing flow, bcrypt tuning, feature-flag system.

### OPS-004 Capacity: AuthService pods
Current 3 replicas; expected 500 concurrent users. Scaling: HPA to 10 replicas at CPU >70%. Trigger: sustained CPU >70% or p95 latency breach.

### OPS-005 Capacity: PostgreSQL connections
Current pool 100; expected ~50 avg concurrent queries. Scaling: grow pool to 200 if connection wait >50ms.

### OPS-006 Capacity: Redis memory
Current 1 GB; expected ~100K refresh tokens (~50 MB). Scaling: alert at 70% utilization; grow to 2 GB.

### OPS-007 Logging
Structured logs for login success/failure, registration, refresh, password reset. Must include user id, IP, timestamp, outcome (SOC2). Sensitive fields (password, tokens) excluded. Retention: 12 months (PRD) supersedes 90 days (TDD).

### OPS-008 Metrics (Prometheus)
`auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter).

### OPS-009 Alerts
Login failure rate >20% over 5 min; p95 latency >500ms; `TokenManager` Redis connection failures. Additionally triggers MIG-007 rollback gates.

### OPS-010 Tracing
Distributed tracing via OpenTelemetry across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService` for full request lifecycle. Sampling strategy unspecified — candidate open question.
