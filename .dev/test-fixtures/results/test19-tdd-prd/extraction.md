---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-19T00:00:00Z
generator: requirements-extractor
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.68
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, testing, devops, data, compliance]
risks_identified: 7
dependencies_identified: 8
success_criteria_count: 10
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 8
test_artifacts_identified: 6
migration_items_identified: 11
operational_items_identified: 8
pipeline_diagnostics: {elapsed_seconds: 152.0, started_at: "2026-04-19T16:15:01.580154+00:00", finished_at: "2026-04-19T16:17:33.601229+00:00"}
---

## Functional Requirements

### FR-AUTH-001
**Login with email and password.** `AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
**Acceptance Criteria:**
1. Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken.
2. Invalid credentials return 401 with error message.
3. Non-existent email returns 401 (no user enumeration).
4. Account locked after 5 failed attempts within 15 minutes.

### FR-AUTH-002
**User registration with validation.** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
**Acceptance Criteria:**
1. Valid registration returns 201 with `UserProfile` data.
2. Duplicate email returns 409 Conflict.
3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
4. `PasswordHasher` stores bcrypt hash with cost factor 12.

### FR-AUTH-003
**JWT token issuance and refresh.** `TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
**Acceptance Criteria:**
1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
3. Expired refreshToken returns 401.
4. Revoked refreshToken returns 401.

### FR-AUTH-004
**User profile retrieval.** `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
**Acceptance Criteria:**
1. GET `/auth/me` with valid accessToken returns `UserProfile`.
2. Expired or invalid token returns 401.
3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.

### FR-AUTH-005
**Password reset flow.** `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
**Acceptance Criteria:**
1. POST `/auth/reset-request` with valid email sends reset token via email.
2. POST `/auth/reset-confirm` with valid token updates the password hash.
3. Reset tokens expire after 1 hour.
4. Used reset tokens cannot be reused.

## Non-Functional Requirements

### NFR-PERF-001
**API response time.** All auth endpoints must respond in < 200ms at p95. Measured via APM tracing on `AuthService` methods.

### NFR-PERF-002
**Concurrent authentication.** Support 500 concurrent login requests. Measured via load testing with k6.

### NFR-REL-001
**Service availability.** 99.9% uptime measured over 30-day rolling windows via health check endpoint.

### NFR-SEC-001
**Password hashing.** `PasswordHasher` must use bcrypt with cost factor 12. Validated via unit test asserting bcrypt cost parameter.

### NFR-SEC-002
**Token signing.** `JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Validated via configuration test.

### NFR-COMPLIANCE-001
**GDPR consent at registration** (from PRD). Users must consent to data collection at registration. Consent recorded with timestamp.

### NFR-COMPLIANCE-002
**SOC2 Type II audit logging** (from PRD). All auth events logged with user ID, timestamp, IP, and outcome. 12-month retention requirement.

### NFR-COMPLIANCE-003
**NIST SP 800-63B password storage** (from PRD). One-way adaptive hashing. Raw passwords never persisted or logged.

### NFR-COMPLIANCE-004
**GDPR data minimization** (from PRD). Only email, hashed password, and display name collected. No additional PII required.

## Complexity Assessment

**Score: 0.68 (MEDIUM)**

Scoring rationale:
| Dimension | Score | Justification |
|---|---|---|
| Requirement count | 0.55 | 5 FRs + 9 NFRs across multiple domains |
| Component breadth | 0.70 | 8 components across backend + frontend |
| Integration surface | 0.75 | PostgreSQL, Redis, SendGrid, API Gateway |
| Security sensitivity | 0.85 | Auth-critical; XSS, brute-force, token theft risks |
| Rollout complexity | 0.70 | 3-phase rollout, 2 feature flags, parallel legacy |
| Compliance burden | 0.65 | SOC2, GDPR, NIST explicit requirements |

Auth is inherently security-sensitive but the scope is narrow (email/password only, no OAuth/MFA in v1.0). Well-scoped MEDIUM complexity.

## Architectural Constraints

- **Tech stack mandated**: Node.js 20 LTS, PostgreSQL 15+, Redis 7+
- **Password hashing**: bcrypt with cost factor 12 (via `PasswordHasher`); no alternative algorithms in v1.0
- **Token signing**: RS256 with 2048-bit RSA keys rotated quarterly
- **Stateless API**: No server-side session state; JWT-only with Redis-backed refresh tokens
- **API versioning**: URL-prefix versioning (`/v1/auth/*`); breaking changes require major version
- **TLS**: TLS 1.3 enforced on all endpoints
- **CORS**: Restricted to known frontend origins only
- **Persona-driven design (from PRD)**: Must serve Alex (end user — fast signup, silent refresh), Jordan (admin — audit log visibility), Sam (API consumer — programmatic token refresh)
- **Scope boundaries (from PRD)**: Email/password only; NO OAuth/social login, NO MFA, NO RBAC enforcement (roles field stored but not enforced)
- **Compliance**: SOC2 Type II audit trail required before Q3 2026; GDPR consent + data minimization mandatory

## Risk Inventory

1. **R-001 Token theft via XSS (High severity)** — Mitigation: accessToken in memory only, HttpOnly cookies for refreshToken, 15-min access expiry, `AuthProvider` clears on tab close. Contingency: immediate `TokenManager` revocation, force password reset.
2. **R-002 Brute-force attacks on login (Medium severity)** — Mitigation: API Gateway rate limit 10/min per IP, 5-attempt account lockout, bcrypt cost 12. Contingency: WAF IP block, CAPTCHA after 3 failed attempts.
3. **R-003 Data loss during migration (High severity)** — Mitigation: parallel legacy+new run during Phases 1-2, idempotent upsert, full backup before each phase. Contingency: rollback to legacy, restore from backup.
4. **R-PRD-001 Low registration adoption from poor UX (Medium severity, from PRD)** — Mitigation: usability testing pre-launch, funnel iteration.
5. **R-PRD-002 Security breach from implementation flaws (Critical severity, from PRD)** — Mitigation: dedicated security review, pentest before production.
6. **R-PRD-003 Compliance failure from incomplete audit logging (High severity, from PRD)** — Mitigation: define log requirements early, validate against SOC2 controls in QA.
7. **R-PRD-004 Email delivery failures block password reset (Medium severity, from PRD)** — Mitigation: delivery monitoring and alerting, fallback support channel.

## Dependency Inventory

| # | Dependency | Type | Purpose |
|---|---|---|---|
| 1 | PostgreSQL 15+ | Infrastructure | `UserProfile` persistence, audit log |
| 2 | Redis 7+ | Infrastructure | Refresh token storage by `TokenManager` |
| 3 | Node.js 20 LTS | Runtime | Service runtime |
| 4 | bcryptjs | Library | `PasswordHasher` implementation |
| 5 | jsonwebtoken | Library | `JwtService` JWT operations |
| 6 | SendGrid API | External service | Password reset email delivery |
| 7 | API Gateway | Infrastructure | Rate limiting, CORS, TLS termination |
| 8 | Frontend routing framework | Internal | Host `LoginPage`, `RegisterPage`, `AuthProvider` |

## Success Criteria

| # | Criterion | Target | Source |
|---|---|---|---|
| 1 | Login response time p95 | < 200ms | TDD S4.1 |
| 2 | Registration success rate | > 99% | TDD S4.1 |
| 3 | Token refresh latency p95 | < 100ms | TDD S4.1 |
| 4 | Service availability | 99.9% uptime / 30-day window | TDD S4.1 |
| 5 | Password hash time | < 500ms (bcrypt cost 12) | TDD S4.1 |
| 6 | User registration conversion | > 60% | TDD S4.2 + PRD |
| 7 | Daily active authenticated users | > 1000 within 30 days of GA | TDD S4.2 |
| 8 | Average session duration | > 30 minutes | PRD |
| 9 | Failed login rate | < 5% of attempts | PRD |
| 10 | Password reset completion rate | > 80% | PRD |

## Open Questions

- **OQ-001** — Should `AuthService` support API key authentication for service-to-service calls? (Owner: test-lead; Target: 2026-04-15; deferred to v1.1)
- **OQ-002** — What is the maximum allowed `UserProfile` roles array length? (Owner: auth-team; Target: 2026-04-01; pending RBAC review)
- **OQ-PRD-001** — Password reset emails: synchronous or asynchronous delivery? (Owner: Engineering)
- **OQ-PRD-002** — Maximum refresh tokens allowed per user across devices? (Owner: Product)
- **OQ-PRD-003** — Account lockout policy after N consecutive failed attempts — is 5 the final number? (Owner: Security)
- **OQ-PRD-004** — Support "remember me" to extend session duration? (Owner: Product)
- **JTBD gap** — Admin persona (Jordan) JTBD of "view authentication event logs for incident investigation" lacks a corresponding TDD functional requirement; audit log surfacing is implied by NFR-COMPLIANCE-002 but no admin-facing API/UI is specified.

## Data Models and Interfaces

### DM-001
**Name:** `UserProfile`
**Storage:** PostgreSQL 15, indefinite retention
**Interface:**
```ts
interface UserProfile {
  id: string; email: string; displayName: string;
  createdAt: string; updatedAt: string; lastLoginAt: string;
  roles: string[];
}
```
| Field | Type | Constraints |
|---|---|---|
| id | UUID | PRIMARY KEY, NOT NULL |
| email | string | UNIQUE, NOT NULL, indexed, lowercase-normalized |
| displayName | string | NOT NULL, 2-100 chars |
| createdAt | ISO 8601 | NOT NULL, DEFAULT now() |
| updatedAt | ISO 8601 | NOT NULL, auto-updated |
| lastLoginAt | ISO 8601 | NULLABLE; set by `AuthService` on login |
| roles | string[] | NOT NULL, DEFAULT ["user"]; not enforced by `AuthService` |

**Relationships:** 1:N with refresh tokens (Redis-backed, non-relational); 1:N with audit log entries (PostgreSQL, 90-day retention).

### DM-002
**Name:** `AuthToken`
**Storage:** refreshToken → Redis 7 with 7-day TTL (managed by `TokenManager`); accessToken not persisted.
**Interface:**
```ts
interface AuthToken {
  accessToken: string; refreshToken: string;
  expiresIn: number; tokenType: string;
}
```
| Field | Type | Constraints |
|---|---|---|
| accessToken | JWT | NOT NULL; RS256-signed by `JwtService`; payload: user id + roles |
| refreshToken | opaque string | NOT NULL, unique; 7-day TTL in Redis |
| expiresIn | number | NOT NULL; always 900 seconds |
| tokenType | string | NOT NULL; always "Bearer" (OAuth2 compat) |

**Additional storage:** Audit log in PostgreSQL (90-day retention) captures login attempts and password resets.

## API Specifications

**Versioning:** URL-prefix (`/v1/auth/*`). Breaking changes require major version bump. Non-breaking additions allowed.
**Error envelope (all endpoints):** `{ "error": { "code": "AUTH_*", "message": "...", "status": N } }`

### API-001
**POST `/auth/login`** — Authenticates user; returns `AuthToken`.
- Auth: none. Rate limit: 10/min per IP.
- Request: `{ email, password }`
- Response 200: `AuthToken` (accessToken, refreshToken, expiresIn=900, tokenType="Bearer")
- Errors: 401 invalid credentials; 423 account locked (5 failed in 15 min); 429 rate limit.

### API-002
**POST `/auth/register`** — Creates `UserProfile`; returns profile.
- Auth: none. Rate limit: 5/min per IP.
- Request: `{ email, password, displayName }`
- Response 201: full `UserProfile`
- Errors: 400 validation (weak password, invalid email); 409 email conflict.

### API-003
**GET `/auth/me`** — Returns authenticated user's `UserProfile`.
- Auth: Bearer accessToken. Rate limit: 60/min per user.
- Headers: `Authorization: Bearer <jwt>`
- Response 200: `UserProfile`
- Errors: 401 missing/expired/invalid token.

### API-004
**POST `/auth/refresh`** — Exchanges refresh token for new `AuthToken` pair; old refresh token revoked.
- Auth: refresh token in body. Rate limit: 30/min per user.
- Request: `{ refreshToken }`
- Response 200: new `AuthToken`
- Errors: 401 expired/revoked refresh token.

### API-005
**POST `/auth/reset-request`** — Sends password-reset email with 1-hour token (FR-AUTH-005).
- Auth: none. Request: `{ email }`. Response 200 regardless of email existence (no enumeration).

### API-006
**POST `/auth/reset-confirm`** — Completes password reset; invalidates all sessions (FR-AUTH-005).
- Auth: reset token in body. Request: `{ resetToken, newPassword }`. Response 200 on success; 400 expired/used token.

## Component Inventory

### COMP-001
**`LoginPage`** — Frontend Route/Page at `/login`. Auth: no. Props: `onSuccess: () => void, redirectUrl?: string`. Renders email/password form; submits to `/auth/login`; stores `AuthToken` via `AuthProvider`. Dependencies: `AuthProvider`, `AuthService` API.

### COMP-002
**`RegisterPage`** — Frontend Route/Page at `/register`. Auth: no. Props: `onSuccess: () => void, termsUrl: string`. Renders registration form with email/password/displayName; client-side password strength validation; calls `/auth/register`. Dependencies: `AuthProvider`, `AuthService` API.

### COMP-003
**`ProfilePage`** — Frontend Route/Page at `/profile`. Auth: yes. Displays `UserProfile` via GET `/auth/me`. Dependencies: `AuthProvider`.

### COMP-004
**`AuthProvider`** — Frontend React context provider. Props: `children: ReactNode`. Manages `AuthToken` state, silent refresh via `TokenManager`, intercepts 401s, redirects unauthenticated users to `LoginPage`. Dependencies: `AuthService` API, `TokenManager` semantics.

### COMP-005
**`AuthService`** — Backend orchestrator. Exposes login/register/profile/refresh/reset flows; delegates to `PasswordHasher`, `TokenManager`, UserRepo. Location: backend service. Dependencies: PostgreSQL, `PasswordHasher`, `TokenManager`, SendGrid (reset).

### COMP-006
**`TokenManager`** — Backend token lifecycle manager. Issues/revokes/refreshes tokens; stores refresh tokens (hashed) in Redis with 7-day TTL. Dependencies: Redis, `JwtService`.

### COMP-007
**`JwtService`** — Backend JWT sign/verify. RS256 with 2048-bit RSA keys rotated quarterly; 5-second clock-skew tolerance. Dependencies: key material (secrets volume).

### COMP-008
**`PasswordHasher`** — Backend bcrypt abstraction. Cost factor 12; abstracts algorithm for future migration. Benchmarked at ~300ms per hash. Dependencies: bcryptjs library.

**Component hierarchy:**
```
App
├── AuthProvider (COMP-004)
│   ├── PublicRoutes → LoginPage (COMP-001), RegisterPage (COMP-002)
│   └── ProtectedRoutes → ProfilePage (COMP-003)
```

## Testing Strategy

**Pyramid:** Unit 80% coverage (Jest, ts-jest) · Integration 15% (Supertest, testcontainers) · E2E 5% (Playwright).
**Environments:** Local (Docker Compose PG+Redis), CI (testcontainers ephemeral), Staging (seeded test accounts, isolated from prod).

### TEST-001
**Unit — Login with valid credentials returns `AuthToken`** (validates FR-AUTH-001). `AuthService.login()` calls `PasswordHasher.verify()` → `TokenManager.issueTokens()` → returns valid `AuthToken` with both tokens.

### TEST-002
**Unit — Login with invalid credentials returns error** (validates FR-AUTH-001). `AuthService.login()` returns 401 when `PasswordHasher.verify()` returns false; no `AuthToken` issued.

### TEST-003
**Unit — Token refresh with valid refresh token** (validates FR-AUTH-003). `TokenManager.refresh()` validates refresh token, revokes old token, issues new `AuthToken` pair via `JwtService`.

### TEST-004
**Integration — Registration persists `UserProfile` to database** (validates FR-AUTH-002). Full flow: API → `PasswordHasher` → PostgreSQL insert.

### TEST-005
**Integration — Expired refresh token rejected by `TokenManager`** (validates FR-AUTH-003). Redis TTL expiration correctly invalidates refresh tokens.

### TEST-006
**E2E — User registers and logs in** (validates FR-AUTH-001, FR-AUTH-002). Complete journey: `RegisterPage` → `LoginPage` → `ProfilePage` via `AuthProvider`.

## Migration and Rollout Plan

### MIG-001
**Phase 1: Internal Alpha** — Duration: 1 week. Deploy `AuthService` to staging; auth-team + QA test all endpoints; `LoginPage`/`RegisterPage` behind `AUTH_NEW_LOGIN`. Exit: FR-AUTH-001..005 pass manual test, zero P0/P1 bugs. Depends on: completed implementation of M1-M4.

### MIG-002
**Phase 2: Beta (10% traffic)** — Duration: 2 weeks. Enable `AUTH_NEW_LOGIN` for 10% of traffic; monitor latency, error rates, Redis usage; `AuthProvider` refresh under real load. Exit: p95 < 200ms, error < 0.1%, zero Redis connection failures. Depends on: MIG-001.

### MIG-003
**Phase 3: General Availability (100%)** — Duration: 1 week. Remove `AUTH_NEW_LOGIN`; deprecate legacy endpoints; `AUTH_TOKEN_REFRESH` enabled. Exit: 99.9% uptime over first 7 days, all dashboards green. Depends on: MIG-002.

### MIG-004
**Feature flag `AUTH_NEW_LOGIN`** — Gates new `LoginPage`/`AuthService` login. Default OFF. Owner: auth-team. Cleanup: remove after MIG-003 GA.

### MIG-005
**Feature flag `AUTH_TOKEN_REFRESH`** — Enables refresh token flow in `TokenManager`; when OFF, access-only. Default OFF. Owner: auth-team. Cleanup: remove MIG-003 + 2 weeks.

### MIG-006
**Rollback step 1** — Disable `AUTH_NEW_LOGIN` flag; route traffic to legacy auth.

### MIG-007
**Rollback step 2** — Verify legacy login via smoke tests.

### MIG-008
**Rollback step 3** — Investigate `AuthService` root cause via structured logs + traces.

### MIG-009
**Rollback step 4** — If `UserProfile` data corruption detected, restore from last known-good backup.

### MIG-010
**Rollback step 5** — Notify auth-team + platform-team via incident channel.

### MIG-011
**Rollback step 6** — Post-mortem within 48 hours of rollback.

**Rollback triggers:** p95 > 1000ms for 5 min · error rate > 5% for 2 min · Redis connection failures > 10/min · any `UserProfile` data corruption.

## Operational Readiness

### OPS-001
**Runbook: `AuthService` down.** Symptoms: 5xx on `/auth/*`; `LoginPage`/`RegisterPage` error state. Diagnosis: check pod health (K8s); PG connectivity; `PasswordHasher`/`TokenManager` init logs. Resolution: restart pods; PG failover to read replica if unreachable; if Redis down, refresh requests rejected and users re-login. Escalation: page auth-team on-call → platform-team at 15 min.

### OPS-002
**Runbook: Token refresh failures.** Symptoms: users logged out unexpectedly; `AuthProvider` redirect loop to `LoginPage`; `auth_token_refresh_total` error counter spike. Diagnosis: Redis connectivity from `TokenManager`; `JwtService` signing key access; `AUTH_TOKEN_REFRESH` flag state. Resolution: scale Redis cluster; re-mount secrets volume; enable flag if OFF. Escalation: auth-team → platform-team on Redis cluster issue.

### OPS-003
**On-call expectations.** P1 ack ≤ 15 min · auth-team 24/7 rotation for first 2 weeks post-GA · tooling: K8s dashboards, Grafana, Redis CLI, PG admin · path: auth-team on-call → test-lead → eng-manager → platform-team.

### OPS-004
**Capacity: `AuthService` pods.** Current: 3 replicas. Expected: 500 concurrent users. Scaling trigger: HPA to 10 replicas at CPU > 70%.

### OPS-005
**Capacity: PostgreSQL.** Current: 100 pool. Expected: ~50 avg concurrent queries. Scaling trigger: increase pool to 200 if wait time > 50ms.

### OPS-006
**Capacity: Redis.** Current: 1 GB. Expected: ~100K refresh tokens (~50 MB). Scaling trigger: scale to 2 GB at > 70% utilization.

### OPS-007
**Observability.** Structured logs for login/register/refresh/reset events. Prometheus metrics: `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter). OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`.

### OPS-008
**Alerts.** Login failure rate > 20% over 5 min · p95 latency > 500ms · `TokenManager` Redis connection failures (threshold per operational runbook). Sensitive fields (password, tokens) excluded from logs.
