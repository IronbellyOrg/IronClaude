---
spec_source: test-tdd-user-auth.md
generated: 2026-04-16T00:00:00Z
generator: requirements-extraction-agent
functional_requirements: 5
nonfunctional_requirements: 6
total_requirements: 11
complexity_score: 0.72
complexity_class: HIGH
domains_detected: [backend, security, frontend, testing, devops, data, compliance]
risks_identified: 7
dependencies_identified: 8
success_criteria_count: 12
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 4
components_identified: 6
test_artifacts_identified: 6
migration_items_identified: 3
operational_items_identified: 5
pipeline_diagnostics: {elapsed_seconds: 130.0, started_at: "2026-04-16T18:44:11.718362+00:00", finished_at: "2026-04-16T18:46:21.734875+00:00"}
---

## Functional Requirements

### FR-AUTH-001
**Login with email and password.** `AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
- Acceptance: Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken.
- Invalid credentials return 401 with error message.
- Non-existent email returns 401 (no user enumeration).
- Account locked after 5 failed attempts within 15 minutes.

### FR-AUTH-002
**User registration with validation.** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
- Valid registration returns 201 with `UserProfile` data.
- Duplicate email returns 409 Conflict.
- Weak passwords (< 8 chars, no uppercase, no number) return 400.
- `PasswordHasher` stores bcrypt hash with cost factor 12.

### FR-AUTH-003
**JWT token issuance and refresh.** `TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
- Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
- POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
- Expired refreshToken returns 401.
- Revoked refreshToken returns 401.

### FR-AUTH-004
**User profile retrieval.** `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
- GET `/auth/me` with valid accessToken returns `UserProfile`.
- Expired or invalid token returns 401.
- Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.

### FR-AUTH-005
**Password reset flow.** `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
- POST `/auth/reset-request` with valid email sends reset token via email.
- POST `/auth/reset-confirm` with valid token updates the password hash.
- Reset tokens expire after 1 hour.
- Used reset tokens cannot be reused.

## Non-Functional Requirements

### NFR-PERF-001
API response time — all auth endpoints must respond in < 200ms at p95. Measured via APM tracing on `AuthService` methods.

### NFR-PERF-002
Concurrent authentication — support 500 concurrent login requests. Measured via k6 load testing.

### NFR-REL-001
Service availability — 99.9% uptime measured over 30-day rolling windows via health check endpoint monitoring.

### NFR-SEC-001
Password hashing — `PasswordHasher` must use bcrypt with cost factor 12. Validated via unit test asserting bcrypt cost parameter.

### NFR-SEC-002
Token signing — `JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Validated via configuration test.

### NFR-COMPLIANCE-001
(From PRD S17) Audit logging — all auth events logged with user ID, timestamp, IP, and outcome; 12-month retention to satisfy SOC2 Type II. GDPR consent recorded at registration; data minimization limited to email, hashed password, display name; NIST SP 800-63B password storage compliance.

## Complexity Assessment

- **Complexity score:** 0.72
- **Complexity class:** HIGH

**Rationale:**
- Cross-cutting security concerns (bcrypt, RS256 JWT, refresh token revocation, account lockout)
- Multiple data stores (PostgreSQL for users/audit, Redis for refresh tokens)
- External integrations (SendGrid email)
- Phased rollout with feature flags and rollback procedure
- Frontend + backend coordination (`AuthProvider` silent refresh, `LoginPage`, `RegisterPage`)
- Compliance burden (SOC2, GDPR, NIST SP 800-63B)
- 5 FRs with multi-criteria acceptance, 6 NFRs with measurable targets, 7 risks
- Offsetting factor: well-bounded scope (v1.0 explicitly excludes OAuth, MFA, RBAC)

## Architectural Constraints

1. **Runtime:** Node.js 20 LTS.
2. **Primary datastore:** PostgreSQL 15+ for `UserProfile`, password hashes, audit log.
3. **Cache/token store:** Redis 7+ for refresh tokens (7-day TTL) managed by `TokenManager`.
4. **Password hashing:** bcrypt with cost factor 12 via `PasswordHasher`; abstraction required for future algorithm migration.
5. **JWT signing:** RS256 with 2048-bit RSA keys rotated quarterly via `JwtService`.
6. **Session mechanism:** Stateless JWT access token (15 min) + opaque refresh token (7 day); no server-side session storage beyond Redis refresh records.
7. **Transport security:** TLS 1.3 mandated; CORS restricted to known frontend origins.
8. **API versioning:** URL prefix `/v1/auth/*`; breaking changes require new major version.
9. **Rate limiting:** Enforced at API Gateway (10/min login, 5/min register, 60/min `/auth/me`, 30/min refresh).
10. **Email provider:** SendGrid for password reset email delivery.
11. **Deployment:** Kubernetes with HPA (3→10 replicas, CPU>70% trigger).
12. **Logging:** Passwords and tokens must never appear in application logs.
13. **Persona-driven design constraints (from PRD S7):**
    - Alex (end user) — <60s registration, silent session persistence, self-service reset.
    - Jordan (admin) — queryable audit logs by date/user, account lock/unlock visibility.
    - Sam (API consumer) — programmatic token refresh, stable OAuth2-compatible contracts, clear error codes.
14. **Scope boundary validation (from PRD S12):** Extracted FRs cover registration, login, token refresh, profile retrieval, password reset — all in-scope. No OAuth/OIDC, MFA, RBAC, or social login extracted (confirmed out of scope).

## Risk Inventory

1. **R-001 — Token theft via XSS allows session hijacking.** Severity: HIGH (probability Medium × impact High). Mitigation: accessToken in memory only; HttpOnly cookies for refreshToken; 15-min expiry; clear on tab close; `TokenManager` revocation; force password reset for affected accounts.
2. **R-002 — Brute-force attacks on login endpoint.** Severity: MEDIUM (probability High × impact Medium). Mitigation: API Gateway rate limiting (10/min/IP); account lockout after 5 failed attempts; bcrypt cost 12; WAF IP blocking; CAPTCHA after 3 failed attempts.
3. **R-003 — Data loss during migration from legacy auth.** Severity: HIGH (probability Low × impact High). Mitigation: parallel operation in Phase 1-2; idempotent upserts; pre-phase database backup; rollback with restore capability.
4. **R-004 — Redis unavailability disabling refresh flow.** Severity: MEDIUM. Mitigation: `TokenManager` fails closed (rejects refresh, forces re-login); monitoring and scale-out.
5. **R-005 — Clock skew breaking JWT validation.** Severity: LOW. Mitigation: `JwtService` applies 5-second tolerance window.
6. **R-006 — Email delivery failure blocking password reset (PRD-derived).** Severity: MEDIUM. Mitigation: SendGrid delivery monitoring/alerts; fallback support channel.
7. **R-007 — Compliance failure from incomplete audit logging (PRD-derived).** Severity: HIGH. Mitigation: define log requirements early; validate against SOC2 controls in QA; 12-month retention.

## Dependency Inventory

1. **PostgreSQL 15+** — `UserProfile` persistence, password hashes, audit log.
2. **Redis 7+** — refresh token storage and revocation for `TokenManager`.
3. **Node.js 20 LTS** — runtime.
4. **bcryptjs** — `PasswordHasher` implementation.
5. **jsonwebtoken** — `JwtService` implementation.
6. **SendGrid API (SMTP/HTTP)** — password reset email delivery.
7. **API Gateway** — rate limiting, CORS enforcement upstream of `AuthService`.
8. **SEC-POLICY-001** — security policy governing hashing and signing configuration.

Related PRD: AUTH-PRD-001 (parent requirements); INFRA-DB-001 (database infrastructure).

## Success Criteria

### Technical
1. Login p95 response time < 200ms (APM on `AuthService.login()`).
2. Registration success rate > 99%.
3. Token refresh p95 latency < 100ms (`TokenManager.refresh()`).
4. Service availability 99.9% over 30-day windows.
5. `PasswordHasher.hash()` < 500ms with bcrypt cost 12.
6. Unit test coverage > 80% across `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`.
7. All four API endpoints pass integration tests against real PostgreSQL and Redis.
8. Performance: 500 concurrent users with < 200ms p95.

### Business (from PRD S19)
9. Registration conversion rate > 60% (funnel landing → register → confirmed).
10. Daily active authenticated users > 1000 within 30 days of GA.
11. Average session duration > 30 minutes (refresh event analytics).
12. Failed login rate < 5% of attempts; password reset completion > 80%.

## Open Questions

1. **OQ-001** — Should `AuthService` support API key authentication for service-to-service calls? (Owner: test-lead; Target 2026-04-15; deferred to v1.1 discussion.)
2. **OQ-002** — Maximum allowed `UserProfile.roles` array length? (Owner: auth-team; Target 2026-04-01; pending RBAC design review.)
3. **OQ-003 (PRD)** — Should password reset emails be sent synchronously or asynchronously? (Owner: Engineering.)
4. **OQ-004 (PRD)** — Maximum number of refresh tokens allowed per user across devices? (Owner: Product.)
5. **OQ-005 (PRD)** — Account lockout policy after N consecutive failed login attempts? (Owner: Security; TDD specifies 5 in 15 min — pending confirmation.)
6. **OQ-006 (PRD)** — Should we support "remember me" to extend session duration? (Owner: Product.)
7. **JTBD coverage gap (PRD S6):** Jordan (admin) JTBD "see who attempted access and lock compromised accounts" is only partially covered by extracted FRs. Account lockout exists in FR-AUTH-001 but there is no explicit FR for admin-side audit log query/account unlock. Flag for stakeholder clarification.

## Data Models and Interfaces

### DM-001
**`UserProfile`** — PostgreSQL-backed user entity.

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string (UUID v4) | PRIMARY KEY, NOT NULL | Unique user identifier |
| email | string | UNIQUE, NOT NULL, indexed, lowercase | Normalized email |
| displayName | string | NOT NULL, 2–100 chars | UI display name |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Last modification |
| lastLoginAt | string (ISO 8601) | NULLABLE | Updated on successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Authorization roles (enforced downstream) |

Relationships: owns refresh token records in Redis (logical, by user id); referenced by audit log rows in PostgreSQL.

### DM-002
**`AuthToken`** — Token pair returned by login/refresh.

| Field | Type | Constraints | Description |
|---|---|---|---|
| accessToken | string (JWT) | NOT NULL | Signed RS256 by `JwtService`; contains user id and roles; 15-min TTL |
| refreshToken | string | NOT NULL, unique | Opaque; managed by `TokenManager`; Redis-stored hashed; 7-day TTL |
| expiresIn | number | NOT NULL | Seconds to accessToken expiry; always 900 |
| tokenType | string | NOT NULL | Always "Bearer" (OAuth2 compat) |

### Data Storage Summary
| Store | Tech | Purpose | Retention |
|---|---|---|---|
| User records | PostgreSQL 15 | `UserProfile`, password hashes | Indefinite |
| Refresh tokens | Redis 7 | Token lifecycle/revocation | 7-day TTL |
| Audit log | PostgreSQL 15 | Login attempts, password resets | 90 days (TDD) / 12 months (PRD SOC2) — **conflict: PRD wins on retention → 12 months** |

## API Specifications

All endpoints under `/v1/auth/*`; errors use uniform envelope `{ error: { code, message, status } }`.

### API-001
**POST `/auth/login`** — Authenticate user.
- Auth: none. Rate limit: 10 req/min per IP.
- Request: `{ email, password }`.
- Response 200: `AuthToken` (accessToken, refreshToken, expiresIn=900, tokenType="Bearer").
- Errors: 401 invalid credentials; 423 account locked (5 failed attempts); 429 rate limited.

### API-002
**POST `/auth/register`** — Create new account.
- Auth: none. Rate limit: 5 req/min per IP.
- Request: `{ email, password, displayName }`.
- Response 201: `UserProfile`.
- Errors: 400 validation (weak password/invalid email); 409 email conflict.

### API-003
**GET `/auth/me`** — Return authenticated user's profile.
- Auth: Bearer accessToken required. Rate limit: 60 req/min per user.
- Request headers: `Authorization: Bearer <JWT>`.
- Response 200: `UserProfile`.
- Errors: 401 missing/expired/invalid token.

### API-004
**POST `/auth/refresh`** — Exchange refresh token for new pair.
- Auth: refresh token in body (not Bearer). Rate limit: 30 req/min per user.
- Request: `{ refreshToken }`.
- Response 200: new `AuthToken` pair (old refresh token revoked).
- Errors: 401 expired or revoked refresh token.

Versioning: URL prefix `/v1/`; breaking changes → new major; non-breaking additions allowed in-version. Deprecation: legacy auth endpoints deprecated after Phase 3 GA.

## Component Inventory

### COMP-001
**`LoginPage`** — Page / route `/login`. Public. Props: `onSuccess: () => void, redirectUrl?: string`. Renders email/password form; calls POST `/auth/login`; stores `AuthToken` via `AuthProvider`. Location: frontend routes.

### COMP-002
**`RegisterPage`** — Page / route `/register`. Public. Props: `onSuccess: () => void, termsUrl: string`. Renders email/password/displayName form with client-side password strength validation; calls POST `/auth/register`.

### COMP-003
**`ProfilePage`** — Page / route `/profile`. Auth required. Displays `UserProfile` data via GET `/auth/me`.

### COMP-004
**`AuthProvider`** — React Context provider. Props: `children: ReactNode`. Wraps `PublicRoutes` + `ProtectedRoutes`; manages `AuthToken` state; handles silent refresh via `TokenManager`; intercepts 401 to trigger refresh or redirect to `LoginPage`; exposes `UserProfile` and auth methods to children.

### COMP-005
**`AuthService`** — Backend orchestration component. Type: service/facade. Location: backend. Dependencies: `PasswordHasher`, `TokenManager`, `JwtService`, `UserRepo` (PostgreSQL). Responsibilities: login, registration, profile retrieval, password reset, lockout enforcement, email normalization.

### COMP-006
**`TokenManager`** — Backend token lifecycle component. Dependencies: `JwtService`, Redis. Responsibilities: issue access+refresh pairs, store hashed refresh tokens with 7-day TTL, revoke on rotation, reject expired/revoked tokens. Composes `JwtService` internally.

Supporting: `JwtService` (RS256 sign/verify, 5s clock skew), `PasswordHasher` (bcrypt cost 12 abstraction), `UserRepo` (PostgreSQL access). Hierarchy: `App → AuthProvider → { PublicRoutes{LoginPage, RegisterPage}, ProtectedRoutes{ProfilePage} }`.

## Testing Strategy

### Test Pyramid
| Level | Coverage | Tools | Focus |
|---|---|---|---|
| Unit | 80% | Jest, ts-jest | `AuthService`, `PasswordHasher`, `JwtService`, `TokenManager`, `UserProfile` validation |
| Integration | 15% | Supertest, testcontainers | API endpoints, PostgreSQL, Redis, cross-component flows |
| E2E | 5% | Playwright | `LoginPage`, `RegisterPage`, `AuthProvider` token refresh, full user journey |

### TEST-001
**Login with valid credentials returns `AuthToken`** (unit, `AuthService`). Input: valid email/password. Expected: `PasswordHasher.verify()` called, then `TokenManager.issueTokens()`, returns `AuthToken` with both tokens. Validates FR-AUTH-001. Mocks: `PasswordHasher`, `TokenManager`.

### TEST-002
**Login with invalid credentials returns error** (unit, `AuthService`). Input: bad password. Expected: 401 returned, no `AuthToken` issued. Validates FR-AUTH-001. Mocks: `PasswordHasher.verify()` → false.

### TEST-003
**Token refresh with valid refresh token** (unit, `TokenManager`). Input: valid refresh token. Expected: token validated, old revoked, new pair issued via `JwtService`. Validates FR-AUTH-003. Mocks: Redis client, `JwtService`.

### TEST-004
**Registration persists `UserProfile` to database** (integration, `AuthService` + PostgreSQL via testcontainers). Input: API request. Expected: full flow through `PasswordHasher` to DB insert with bcrypt hash. Validates FR-AUTH-002.

### TEST-005
**Expired refresh token rejected by `TokenManager`** (integration, `TokenManager` + Redis via testcontainers). Input: refresh token past TTL. Expected: Redis TTL expiry → 401. Validates FR-AUTH-003.

### TEST-006
**User registers and logs in** (E2E, Playwright). Flow: `RegisterPage` → `LoginPage` → `ProfilePage`. Expected: complete user journey succeeds through `AuthProvider`. Validates FR-AUTH-001, FR-AUTH-002.

### Test Environments
| Env | Purpose | Data |
|---|---|---|
| Local | Developer testing | Docker Compose (PostgreSQL + Redis) |
| CI | Automated pipeline | testcontainers for ephemeral DBs |
| Staging | Pre-prod validation | Seeded test accounts, isolated from prod |

## Migration and Rollout Plan

### MIG-001
**Phase 1 — Internal Alpha.** Milestone: staging deploy. Duration: 1 week. Exit criteria: FR-AUTH-001…005 pass manual QA by auth-team; zero P0/P1 bugs. `LoginPage`, `RegisterPage` behind `AUTH_NEW_LOGIN`. Rollback: disable feature flag.

### MIG-002
**Phase 2 — Beta (10% traffic).** Duration: 2 weeks. Exit criteria: p95 < 200ms, error rate < 0.1%, zero `TokenManager` Redis failures. Monitor `AuthProvider` refresh under real load. Rollback: reduce flag percentage to 0%.

### MIG-003
**Phase 3 — General Availability (100%).** Duration: 1 week. Exit criteria: 99.9% uptime over first 7 days; all dashboards green. Remove `AUTH_NEW_LOGIN`; legacy endpoints deprecated; `AUTH_TOKEN_REFRESH` enables refresh flow. Rollback: re-enable legacy via flag.

### Feature Flags
| Flag | Purpose | Default | Cleanup | Owner |
|---|---|---|---|---|
| `AUTH_NEW_LOGIN` | Gate new `LoginPage` + `AuthService` login | OFF | After Phase 3 GA | auth-team |
| `AUTH_TOKEN_REFRESH` | Enable refresh-token flow in `TokenManager`; access-only when OFF | OFF | Phase 3 + 2 weeks | auth-team |

### Rollback Procedure (ordered)
1. Disable `AUTH_NEW_LOGIN` to route traffic to legacy auth.
2. Smoke-test legacy login flow.
3. Investigate `AuthService` failure via structured logs and traces.
4. If `UserProfile` table corruption detected, restore from last known-good backup.
5. Notify auth-team and platform-team via incident channel.
6. Post-mortem within 48 hours of rollback.

### Rollback Triggers
- p95 latency > 1000ms for > 5 min
- Error rate > 5% for > 2 min
- `TokenManager` Redis connection failures > 10/min
- Any `UserProfile` data loss/corruption

### Timeline
| Milestone | Target | Deliverables |
|---|---|---|
| M1 Core AuthService | 2026-04-14 | `AuthService`, `PasswordHasher`, `UserProfile` schema, login+register endpoints |
| M2 Token Management | 2026-04-28 | `TokenManager`, `JwtService`, `AuthToken`, refresh + `/auth/me` |
| M3 Password Reset | 2026-05-12 | FR-AUTH-005 flow, email integration |
| M4 Frontend Integration | 2026-05-26 | `LoginPage`, `RegisterPage`, `AuthProvider` |
| M5 GA Release | 2026-06-09 | Phase 3 complete, feature flags removed |

## Operational Readiness

### OPS-001
**Runbook — `AuthService` down.** Symptoms: 5xx on all `/auth/*`; `LoginPage`/`RegisterPage` error state. Diagnosis: K8s pod health, PostgreSQL connectivity, `PasswordHasher`/`TokenManager` init logs. Resolution: restart pods; failover PostgreSQL to read replica; if Redis down, `TokenManager` rejects refresh → users re-login. Escalation: auth-team on-call → platform-team after 15 min.

### OPS-002
**Runbook — Token refresh failures.** Symptoms: unexpected logouts; `AuthProvider` redirect loop to `LoginPage`; `auth_token_refresh_total` error spike. Diagnosis: Redis connectivity from `TokenManager`; `JwtService` signing key accessibility; `AUTH_TOKEN_REFRESH` flag state. Resolution: scale Redis cluster; re-mount secrets; toggle flag ON. Escalation: auth-team → platform-team for Redis cluster issues.

### OPS-003
**On-call expectations.** P1 ack within 15 min; auth-team 24/7 rotation first 2 weeks post-GA. Tooling: K8s dashboards, Grafana, Redis CLI, PostgreSQL admin. Escalation path: auth-team on-call → test-lead → eng-manager → platform-team. MTTD: alert-driven (login failure rate > 20% / 5 min; p95 > 500ms; Redis failures). MTTR target: < 60 min for P1.

### OPS-004
**Capacity planning.** Current: 3 `AuthService` replicas, PostgreSQL pool 100, Redis 1 GB. Expected: 500 concurrent users; ~100K refresh tokens (~50 MB Redis). Triggers: HPA to 10 replicas at CPU > 70%; PG pool → 200 if wait > 50ms; Redis → 2 GB if > 70% utilized.

### OPS-005
**Observability.** Structured logs for every auth event (login success/failure, registration, refresh, password reset), with passwords/tokens excluded. Metrics (Prometheus): `auth_login_total` counter, `auth_login_duration_seconds` histogram, `auth_token_refresh_total` counter, `auth_registration_total` counter. Tracing: OpenTelemetry spans across `AuthService` → `PasswordHasher` / `TokenManager` / `JwtService`. Alerts: login failure rate > 20% over 5 min; p95 latency > 500ms; Redis connection failures. Dashboards verified at release: `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`. Audit log retention: 12 months (PRD/SOC2 authoritative) supersedes TDD's 90-day figure.
