---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-19T00:00:00Z
generator: sc-tdd-extractor
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.70
complexity_class: HIGH
domains_detected: [backend, security, frontend, testing, devops, data, compliance]
risks_identified: 6
dependencies_identified: 8
success_criteria_count: 10
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 4
test_artifacts_identified: 6
migration_items_identified: 6
operational_items_identified: 9
---

## Functional Requirements

### FR-AUTH-001
**Login with email and password.** `AuthService` authenticates users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
- Valid credentials return 200 with `AuthToken` (accessToken + refreshToken).
- Invalid credentials return 401 (no user enumeration).
- Non-existent email returns 401.
- Account locked after 5 failed attempts within 15 minutes.

### FR-AUTH-002
**User registration with validation.** `AuthService` creates new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
- Valid registration returns 201 with `UserProfile` data.
- Duplicate email returns 409 Conflict.
- Weak passwords (< 8 chars, no uppercase, no number) return 400.
- `PasswordHasher` stores bcrypt hash with cost factor 12.

### FR-AUTH-003
**JWT token issuance and refresh.** `TokenManager` issues JWT access tokens (15-min expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
- Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
- POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
- Expired/revoked refreshToken returns 401.

### FR-AUTH-004
**User profile retrieval.** `AuthService` returns authenticated user's `UserProfile` including id, email, displayName, roles, timestamps.
- GET `/auth/me` with valid accessToken returns `UserProfile`.
- Expired/invalid token returns 401.
- Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.

### FR-AUTH-005
**Password reset flow.** `AuthService` supports a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
- POST `/auth/reset-request` with valid email sends reset token via email.
- POST `/auth/reset-confirm` with valid token updates the password hash.
- Reset tokens expire after 1 hour.
- Used reset tokens cannot be reused.

## Non-Functional Requirements

### NFR-PERF-001
API response time: all auth endpoints must respond in < 200ms at p95. Measured via APM tracing on `AuthService` methods.

### NFR-PERF-002
Concurrent authentication: support 500 concurrent login requests. Measured via k6 load testing.

### NFR-REL-001
Service availability: 99.9% uptime measured over 30-day rolling windows via health check endpoint.

### NFR-SEC-001
Password hashing: `PasswordHasher` must use bcrypt with cost factor 12. Verified via unit test asserting bcrypt cost parameter.

### NFR-SEC-002
Token signing: `JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Verified via configuration validation test.

### NFR-COMP-001
GDPR consent at registration: users must consent to data collection at registration with timestamped consent record. (PRD legal requirement)

### NFR-COMP-002
SOC2 audit logging: all auth events logged with user ID, timestamp, IP, and outcome; 12-month retention. (PRD legal requirement)

### NFR-COMP-003
NIST SP 800-63B password storage: one-way adaptive hashing; raw passwords never persisted or logged. (PRD legal requirement, reinforces NFR-SEC-001)

### NFR-COMP-004
GDPR data minimization: only email, hashed password, and display name collected; no additional PII. (PRD legal requirement)

## Complexity Assessment

**complexity_score: 0.70**
**complexity_class: HIGH**

Scoring rationale:
- **Security-critical surface** (+0.20): authentication, bcrypt, JWT, RS256 keys, token revocation, account lockout.
- **Multi-system integration** (+0.15): PostgreSQL, Redis, SendGrid, API Gateway, frontend.
- **Stateful token lifecycle** (+0.10): dual-token (access + refresh), Redis-backed revocation, silent refresh.
- **Compliance obligations** (+0.10): SOC2, GDPR, NIST SP 800-63B.
- **Phased rollout with feature flags** (+0.10): two flags, three rollout phases, rollback plan.
- **Cross-team scope** (+0.05): backend, frontend, security, platform, product teams.

## Architectural Constraints

1. **Stateless JWT-based authentication** — no server-side sessions beyond refresh token records in Redis.
2. **JWT signing: RS256 with 2048-bit RSA keys** rotated quarterly.
3. **Password hashing: bcrypt cost factor 12** via `PasswordHasher` abstraction.
4. **Runtime: Node.js 20 LTS**.
5. **Persistence: PostgreSQL 15+** for `UserProfile`, audit log; **Redis 7+** for refresh tokens.
6. **API versioning via URL prefix** (`/v1/auth/*`); breaking changes require new major version.
7. **TLS 1.3 enforced** on all endpoints; CORS restricted to known frontend origins.
8. **API Gateway owns rate limiting and CORS** upstream of `AuthService`.
9. **Persona-driven design requirements** (from PRD): must serve Alex (end user quick registration/login), Jordan (admin audit/lock), Sam (API consumer programmatic token refresh).
10. **Email delivery via SendGrid** for password reset emails.
11. **Refresh tokens stored as hashed values** in Redis to mitigate theft.
12. **Roles field present on `UserProfile`** but enforcement is downstream, not in `AuthService`.

## Risk Inventory

1. **R-001 Token theft via XSS allows session hijacking** — Medium probability, High impact. Mitigation: accessToken in memory only, HttpOnly cookies for refresh, 15-min access TTL, `JwtService` short expiry. Contingency: `TokenManager` revocation, forced password reset.
2. **R-002 Brute-force attacks on login endpoint** — High probability, Medium impact. Mitigation: rate limiting (10 req/min/IP), 5-attempt lockout, bcrypt cost 12. Contingency: WAF IP blocking, CAPTCHA after 3 failures.
3. **R-003 Data loss during migration from legacy auth** — Low probability, High impact. Mitigation: parallel run, idempotent upserts, pre-phase backup. Contingency: rollback + restore.
4. **Low registration adoption due to poor UX** — Medium/High (PRD). Mitigation: usability testing pre-launch, funnel iteration.
5. **Compliance failure from incomplete audit logging** — Medium/High (PRD). Mitigation: early log spec, SOC2 control validation in QA.
6. **Email delivery failures blocking password reset** — Low/Medium (PRD). Mitigation: delivery monitoring, fallback support channel.

## Dependency Inventory

1. **PostgreSQL 15+** — `UserProfile`, password hashes, audit log persistence.
2. **Redis 7+** — refresh token storage and revocation by `TokenManager`.
3. **Node.js 20 LTS** — runtime.
4. **bcryptjs** — `PasswordHasher` bcrypt implementation.
5. **jsonwebtoken** — `JwtService` JWT signing/verification.
6. **SendGrid (SMTP/API)** — password reset email delivery.
7. **Frontend routing framework** — renders `LoginPage`, `RegisterPage`, profile.
8. **SEC-POLICY-001** — organizational security policy governing `PasswordHasher` and `JwtService` configuration.

## Success Criteria

1. Login response time p95 < 200ms (APM on `AuthService.login()`).
2. Registration success rate > 99% (successful/total attempts).
3. Token refresh latency p95 < 100ms (APM on `TokenManager.refresh()`).
4. Service availability ≥ 99.9% uptime (30-day rolling).
5. Password hash time < 500ms (benchmark `PasswordHasher.hash()` cost 12).
6. User registration conversion > 60% (funnel `RegisterPage` → confirmed account).
7. Daily active authenticated users > 1000 within 30 days of GA (`AuthToken` issuance counts).
8. Average session duration > 30 minutes (PRD, token refresh event analytics).
9. Failed login rate < 5% of attempts (PRD, auth event log analysis).
10. Password reset completion > 80% (PRD, funnel reset-requested → new-password-set).

## Open Questions

1. **OQ-001** — Should `AuthService` support API key authentication for service-to-service calls? Owner: test-lead. Target: 2026-04-15. Status: Open (deferred to v1.1 discussion).
2. **OQ-002** — Maximum allowed `UserProfile` roles array length? Owner: auth-team. Target: 2026-04-01. Status: Open (pending RBAC design review).
3. **PRD-OQ-1** — Password reset emails sent synchronously or asynchronously? Owner: Engineering.
4. **PRD-OQ-2** — Maximum refresh tokens per user across devices? Owner: Product.
5. **PRD-OQ-3** — Account lockout policy after N consecutive failed logins? Owner: Security. (TDD states 5 attempts / 15 min; reconcile with Security.)
6. **PRD-OQ-4** — Should "remember me" extend session duration? Owner: Product.
7. **JTBD-gap** — PRD JTBD #3 (self-service password reset) is covered by FR-AUTH-005, but no explicit FR covers PRD JTBD #4 (programmatic token refresh without user interaction for API consumers like Sam) beyond the generic FR-AUTH-003; confirm whether a service-to-service auth mode is required (ties to OQ-001).

## Data Models and Interfaces

### DM-001
**UserProfile** (PostgreSQL table).
Fields:
| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string (UUID v4) | PRIMARY KEY, NOT NULL | Unique user identifier |
| email | string | UNIQUE, NOT NULL, indexed, lowercase-normalized | User email |
| displayName | string | NOT NULL, 2-100 chars | UI display name |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Last modification |
| lastLoginAt | string (ISO 8601) | NULLABLE | Updated on successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Authorization roles (enforced downstream) |

Relationships: referenced by `AuthToken` (via user id in JWT payload), by audit log records.

### DM-002
**AuthToken** (DTO / Redis-backed).
Fields:
| Field | Type | Constraints | Description |
|---|---|---|---|
| accessToken | string (JWT) | NOT NULL | RS256-signed by `JwtService`; contains user id + roles |
| refreshToken | string | NOT NULL, unique | Opaque token stored in Redis with 7-day TTL |
| expiresIn | number | NOT NULL | Seconds until accessToken expiry (900) |
| tokenType | string | NOT NULL | Always "Bearer" (OAuth2 compatibility) |

Relationships: bound to `UserProfile.id` via JWT payload; refresh token managed by `TokenManager` in Redis.

**Storage Strategy:**
| Store | Tech | Purpose | Retention |
|---|---|---|---|
| User records | PostgreSQL 15 | `UserProfile`, password hashes | Indefinite |
| Refresh tokens | Redis 7 | `TokenManager` storage + revocation | 7-day TTL |
| Audit log | PostgreSQL 15 | Login attempts, password resets | 90 days (TDD) / 12 months (PRD SOC2) — reconcile |

Data flow: `AuthService` orchestrates → `PasswordHasher` hashes/verifies → PostgreSQL persists `UserProfile` → `TokenManager` writes refresh token to Redis → `JwtService` signs access JWT.

## API Specifications

### API-001
**POST `/auth/login`** — Public. Rate limit 10 req/min per IP.
Request: `{ email, password }`.
Response 200: `AuthToken` (`accessToken`, `refreshToken`, `expiresIn:900`, `tokenType:"Bearer"`).
Errors: 401 (invalid creds / non-existent email), 423 (locked after 5 failures/15 min), 429 (rate limit).

### API-002
**POST `/auth/register`** — Public. Rate limit 5 req/min per IP.
Request: `{ email, password, displayName }`.
Response 201: `UserProfile` JSON (id, email, displayName, createdAt, updatedAt, lastLoginAt=null, roles).
Errors: 400 (weak password, invalid email), 409 (duplicate email).

### API-003
**GET `/auth/me`** — Bearer auth required. Rate limit 60 req/min per user.
Request headers: `Authorization: Bearer <JWT>`.
Response 200: `UserProfile` JSON.
Errors: 401 (missing/expired/invalid token).

### API-004
**POST `/auth/refresh`** — Public (refresh token in body). Rate limit 30 req/min per user.
Request: `{ refreshToken }`.
Response 200: new `AuthToken` pair; old refresh token revoked.
Errors: 401 (expired/revoked refresh token).

### API-005
**POST `/auth/reset-request`** — Public (implied by FR-AUTH-005).
Request: `{ email }`.
Response: confirmation regardless of registration (no enumeration); email sent with 1-hour reset token.

### API-006
**POST `/auth/reset-confirm`** — Public (implied by FR-AUTH-005).
Request: `{ token, newPassword }`.
Response: password hash updated; reset token consumed (single-use); all existing sessions invalidated.
Errors: 400 (invalid/expired/used token).

**Governance:** versioned via URL prefix (`/v1/auth/*`); breaking changes → new major; additive optional fields allowed in-version. All errors use JSON envelope `{ error: { code, message, status } }`. `JwtService` permits 5-second clock-skew tolerance.

## Component Inventory

### COMP-001
**LoginPage** — route `/login`, no auth required.
Props: `onSuccess: () => void`, `redirectUrl?: string`.
Renders email/password fields; submits to POST `/auth/login`; stores `AuthToken` via `AuthProvider`.

### COMP-002
**RegisterPage** — route `/register`, no auth required.
Props: `onSuccess: () => void`, `termsUrl: string`.
Renders email/password/displayName; validates password strength client-side; calls `AuthService` register.

### COMP-003
**ProfilePage** — route `/profile`, auth required.
Displays `UserProfile` (displayName, email, creation date, timestamps) via GET `/auth/me`.

### COMP-004
**AuthProvider** — React context wrapper.
Props: `children: ReactNode`.
Manages `AuthToken` state, handles silent refresh via `TokenManager`, intercepts 401s, exposes `UserProfile` and auth methods, redirects unauthenticated users from protected routes to `LoginPage`.

**Hierarchy:**
```
App
└─ AuthProvider
   ├─ PublicRoutes → LoginPage, RegisterPage
   └─ ProtectedRoutes → ProfilePage
```

## Testing Strategy

**Pyramid:** Unit 80% (Jest, ts-jest), Integration 15% (Supertest, testcontainers), E2E 5% (Playwright).

### TEST-001
**Unit — Login with valid credentials returns AuthToken.** Component: `AuthService`. Validates FR-AUTH-001: `login()` invokes `PasswordHasher.verify()` → `TokenManager.issueTokens()` → returns valid `AuthToken` (accessToken+refreshToken). Mocks: `PasswordHasher`, `TokenManager`.

### TEST-002
**Unit — Login with invalid credentials returns error.** Component: `AuthService`. Validates FR-AUTH-001: `login()` returns 401 when `PasswordHasher.verify()` → false; no `AuthToken` issued. Mocks: `PasswordHasher`.

### TEST-003
**Unit — Token refresh with valid refresh token.** Component: `TokenManager`. Validates FR-AUTH-003: `refresh()` validates token, revokes old, issues new `AuthToken` pair via `JwtService`. Mocks: Redis, `JwtService`.

### TEST-004
**Integration — Registration persists UserProfile to database.** Scope: `AuthService` + PostgreSQL. Validates FR-AUTH-002: full flow from API request through `PasswordHasher` to DB insert. Real PostgreSQL via testcontainers.

### TEST-005
**Integration — Expired refresh token rejected by TokenManager.** Scope: `TokenManager` + Redis. Validates FR-AUTH-003: Redis TTL expiration invalidates refresh tokens. Real Redis via testcontainers.

### TEST-006
**E2E — User registers and logs in.** Flow: `RegisterPage` → `LoginPage` → ProfilePage. Validates FR-AUTH-001 + FR-AUTH-002 end-to-end through `AuthProvider`. Tool: Playwright.

**Environments:**
| Env | Purpose | Data |
|---|---|---|
| Local | Dev testing | Docker Compose (PostgreSQL + Redis) |
| CI | Automated pipeline | testcontainers (ephemeral) |
| Staging | Pre-prod validation | Seeded test accounts |

## Migration and Rollout Plan

### MIG-001
**Phase 1: Internal Alpha** — 1 week. Deploy `AuthService` to staging; auth-team + QA test all endpoints; `LoginPage`/`RegisterPage` gated by `AUTH_NEW_LOGIN`. Exit: FR-AUTH-001..005 pass manual tests, zero P0/P1 bugs.

### MIG-002
**Phase 2: Beta (10%)** — 2 weeks. Enable `AUTH_NEW_LOGIN` for 10% traffic; monitor latency/error/Redis. Exit: p95 < 200ms, error rate < 0.1%, no `TokenManager` Redis failures.

### MIG-003
**Phase 3: General Availability (100%)** — 1 week. Remove `AUTH_NEW_LOGIN`; enable `AUTH_TOKEN_REFRESH`; deprecate legacy endpoints. Exit: 99.9% uptime over 7 days, dashboards green.

### MIG-004
**Feature flag `AUTH_NEW_LOGIN`** — default OFF. Gates new `LoginPage` + `AuthService` login endpoint. Removal target: after Phase 3 GA. Owner: auth-team.

### MIG-005
**Feature flag `AUTH_TOKEN_REFRESH`** — default OFF. Enables refresh token flow in `TokenManager`; when OFF, only access tokens issued. Removal target: Phase 3 + 2 weeks. Owner: auth-team.

### MIG-006
**Rollback Procedure** (sequential, preserves dependencies):
1. Disable `AUTH_NEW_LOGIN` to route to legacy auth.
2. Verify legacy login via smoke tests.
3. Investigate `AuthService` root cause via logs/traces.
4. If `UserProfile` corruption detected, restore from last known-good backup.
5. Notify auth-team + platform-team via incident channel.
6. Post-mortem within 48 hours.

**Rollback triggers:** p95 > 1000ms for > 5 min; error rate > 5% for > 2 min; `TokenManager` Redis failures > 10/min; any `UserProfile` data loss/corruption.

## Operational Readiness

### OPS-001
**Runbook: AuthService down.** Symptoms: 5xx on all `/auth/*`; `LoginPage`/`RegisterPage` error. Diagnosis: pod health, PostgreSQL connectivity, `PasswordHasher`/`TokenManager` init logs. Resolution: restart pods; PG failover to read replica; if Redis down, users must re-login. Escalation: auth-team on-call → platform-team at 15 min.

### OPS-002
**Runbook: Token refresh failures.** Symptoms: unexpected logouts; `AuthProvider` redirect loop; `auth_token_refresh_total` error spike. Diagnosis: Redis connectivity from `TokenManager`, `JwtService` signing key access, `AUTH_TOKEN_REFRESH` flag state. Resolution: scale Redis cluster; re-mount secrets; enable flag. Escalation: auth-team on-call → platform-team for Redis cluster issues.

### OPS-003
**On-Call Expectations.** P1 ack < 15 min. auth-team 24/7 rotation first 2 weeks post-GA. Tooling: K8s dashboards, Grafana, Redis CLI, PostgreSQL admin. Escalation: auth-team → test-lead → eng-manager → platform-team.

### OPS-004
**Capacity: AuthService pods.** Current 3 replicas; expected 500 concurrent users; HPA scales to 10 replicas at CPU > 70%.

### OPS-005
**Capacity: PostgreSQL connections.** Pool 100; avg 50 concurrent queries; increase to 200 if connection wait > 50ms.

### OPS-006
**Capacity: Redis memory.** 1 GB baseline; ~100K refresh tokens (~50 MB); scale to 2 GB at > 70% utilization.

### OPS-007
**Logging.** Structured logs for all auth events (login success/failure, registration, token refresh, password reset). Sensitive fields (password, tokens) excluded. 90-day retention per TDD; PRD SOC2 requires 12-month retention — reconcile.

### OPS-008
**Metrics (Prometheus).** `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter). Tracing: OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`.

### OPS-009
**Alerts.** Login failure rate > 20% over 5 min; p95 latency > 500ms; `TokenManager` Redis connection failures.
