---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-19T00:00:00Z
generator: requirements-extraction-agent
functional_requirements: 5
nonfunctional_requirements: 5
total_requirements: 10
complexity_score: 0.72
complexity_class: HIGH
domains_detected: [backend, security, frontend, testing, devops, data, api]
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
pipeline_diagnostics: {elapsed_seconds: 151.0, started_at: "2026-04-19T17:03:05.054893+00:00", finished_at: "2026-04-19T17:05:36.073130+00:00"}
---

## Functional Requirements

### FR-AUTH-001: Login with email and password
`AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
**Acceptance Criteria:**
1. Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken.
2. Invalid credentials return 401 with error message.
3. Non-existent email returns 401 (no user enumeration).
4. Account locked after 5 failed attempts within 15 minutes.

### FR-AUTH-002: User registration with validation
`AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
**Acceptance Criteria:**
1. Valid registration returns 201 with `UserProfile` data.
2. Duplicate email returns 409 Conflict.
3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
4. `PasswordHasher` stores bcrypt hash with cost factor 12.

### FR-AUTH-003: JWT token issuance and refresh
`TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
**Acceptance Criteria:**
1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
3. Expired refreshToken returns 401.
4. Revoked refreshToken returns 401.

### FR-AUTH-004: User profile retrieval
`AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
**Acceptance Criteria:**
1. GET `/auth/me` with valid accessToken returns `UserProfile`.
2. Expired or invalid token returns 401.
3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.

### FR-AUTH-005: Password reset flow
`AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
**Acceptance Criteria:**
1. POST `/auth/reset-request` with valid email sends reset token via email.
2. POST `/auth/reset-confirm` with valid token updates the password hash.
3. Reset tokens expire after 1 hour.
4. Used reset tokens cannot be reused.

## Non-Functional Requirements

### NFR-PERF-001: API response time
All auth endpoints must respond in < 200ms at p95. Measured via APM tracing on `AuthService` methods.

### NFR-PERF-002: Concurrent authentication
Support 500 concurrent login requests. Measured via load testing with k6.

### NFR-REL-001: Service availability
99.9% uptime measured over 30-day rolling windows. Measured via uptime monitoring on health check endpoint.

### NFR-SEC-001: Password hashing
`PasswordHasher` must use bcrypt with cost factor 12. Verified via unit test asserting bcrypt cost parameter.

### NFR-SEC-002: Token signing
`JwtService` must sign tokens with RS256 using 2048-bit RSA keys. Verified via configuration validation test.

### NFR-COMPLIANCE-001 (from PRD): Audit logging (SOC2 Type II)
All auth events logged with user ID, timestamp, IP, and outcome. 12-month retention.

### NFR-COMPLIANCE-002 (from PRD): GDPR consent at registration
Users must consent to data collection at registration. Consent recorded with timestamp.

### NFR-COMPLIANCE-003 (from PRD): Password storage (NIST SP 800-63B)
One-way adaptive hashing. Raw passwords never persisted or logged.

### NFR-COMPLIANCE-004 (from PRD): Data minimization (GDPR)
Only email, hashed password, and display name collected. No additional PII required.

## Complexity Assessment

**complexity_score:** 0.72
**complexity_class:** HIGH

**Rationale:**
| Factor | Weight | Score | Contribution |
|---|---|---|---|
| Requirement count (5 FR, 5 NFR + 4 compliance) | 0.15 | 0.65 | 0.098 |
| Cross-cutting security concerns (bcrypt, RS256, XSS, brute-force) | 0.20 | 0.85 | 0.170 |
| Multi-store data architecture (PostgreSQL + Redis + SMTP) | 0.15 | 0.75 | 0.113 |
| Stateful token lifecycle (JWT access + opaque refresh + revocation) | 0.15 | 0.80 | 0.120 |
| Frontend-backend integration (AuthProvider, silent refresh) | 0.10 | 0.70 | 0.070 |
| Phased rollout with feature flags | 0.10 | 0.65 | 0.065 |
| Regulatory compliance (SOC2, GDPR, NIST) | 0.15 | 0.60 | 0.090 |
| **Total** | 1.00 |  | **0.726** |

HIGH classification driven by: multi-component coordination (AuthService, TokenManager, JwtService, PasswordHasher), dual-store persistence, security-critical code paths, and cross-team frontend integration.

## Architectural Constraints

1. **Runtime mandate**: Node.js 20 LTS
2. **Primary datastore**: PostgreSQL 15+ (connection pooling via pg-pool)
3. **Cache/token store**: Redis 7+ (refresh token storage, TTL-based revocation)
4. **Email delivery**: SendGrid (SMTP/API) for password reset
5. **Token format**: JWT signed via RS256, 2048-bit RSA keys, quarterly rotation
6. **Password hashing**: bcrypt (cost factor 12), abstracted behind `PasswordHasher`
7. **Deployment**: Kubernetes pods behind API Gateway (rate limiting, CORS)
8. **API versioning**: URL prefix (`/v1/auth/*`); breaking changes require new major version
9. **TLS**: TLS 1.3 enforced on all endpoints
10. **CORS**: Restricted to known frontend origins
11. **Stateless service**: No server-side session state beyond Redis refresh tokens
12. **Observability stack**: Prometheus metrics, OpenTelemetry tracing, structured logs
13. **Frontend integration**: React-based `AuthProvider` context; accessToken in memory only (not localStorage), refreshToken via HttpOnly cookie
14. **Persona-driven design (from PRD)**:
    - Alex (end user): < 60s registration, seamless cross-device session persistence
    - Jordan (admin): centralized user management, audit log queryability
    - Sam (API consumer): programmatic token refresh, stable auth contracts
15. **Scope boundary (from PRD)**: Email/password only in v1.0; OAuth/OIDC, MFA, RBAC, social login out of scope
16. **Parent doc lineage**: Implements AUTH-PRD-001 Epics AUTH-E1, AUTH-E2, AUTH-E3

## Risk Inventory

1. **R-001 — Token theft via XSS allows session hijacking** (Probability: Medium, Impact: High)
   Mitigation: accessToken in memory only; HttpOnly cookie for refreshToken; 15-min access TTL; `AuthProvider` clears on tab close.
   Contingency: Immediate revocation via `TokenManager`; force password reset for affected `UserProfile`.

2. **R-002 — Brute-force attacks on login endpoint** (Probability: High, Impact: Medium)
   Mitigation: Gateway rate limit (10 req/min per IP); account lockout after 5 failed attempts; bcrypt cost 12.
   Contingency: WAF IP block; CAPTCHA on `LoginPage` after 3 failed attempts.

3. **R-003 — Data loss during migration from legacy auth** (Probability: Low, Impact: High)
   Mitigation: Parallel run during Phase 1-2; idempotent upsert for `UserProfile`; full DB backup per phase.
   Contingency: Rollback to legacy; restore from pre-migration backup.

**Additional risks cross-referenced from PRD (not in TDD risk inventory):**

4. **R-BUS-001 (PRD) — Low registration adoption due to poor UX** (Likelihood: Medium, Impact: High)
   Mitigation: Usability testing pre-launch; funnel iteration.

5. **R-COMP-001 (PRD) — Compliance failure from incomplete audit logging** (Likelihood: Medium, Impact: High)
   Mitigation: Define log requirements early; validate against SOC2 controls in QA.
   Gap: TDD Observability section lists metrics/logs but does not explicitly confirm SOC2-required fields (user ID, IP, outcome, 12-month retention).

6. **R-OPS-001 (PRD) — Email delivery failures blocking password reset** (Likelihood: Low, Impact: Medium)
   Mitigation: Delivery monitoring/alerting; fallback support channel.
   Gap: TDD does not define SendGrid delivery monitoring or alerting thresholds.

## Dependency Inventory

1. **PostgreSQL 15+** — `UserProfile` persistence, audit log storage
2. **Redis 7+** — Refresh token storage and revocation, TTL management
3. **Node.js 20 LTS** — Runtime
4. **bcryptjs library** — Used by `PasswordHasher`
5. **jsonwebtoken library** — Used by `JwtService` for RS256 signing/verification
6. **SendGrid API** — Password reset email delivery (SMTP/API)
7. **API Gateway** — Upstream rate limiting, CORS
8. **Prometheus** — Metrics scraping
9. **OpenTelemetry** — Distributed tracing
10. **AUTH-PRD-001** — Parent product requirements document
11. **INFRA-DB-001** — Database infrastructure dependency (from frontmatter)
12. **SEC-POLICY-001** — Organizational security policy for password/token configuration
13. **Frontend routing framework (PRD)** — Required for auth page rendering

## Success Criteria

**Technical (from TDD):**
1. Login response time (p95) < 200ms (measured via APM on `AuthService.login()`)
2. Registration success rate > 99% (successful / attempts)
3. Token refresh latency (p95) < 100ms (measured via APM on `TokenManager.refresh()`)
4. Service availability 99.9% uptime (30-day windows, via health check)
5. Password hash time < 500ms (benchmark of `PasswordHasher.hash()` with bcrypt cost 12)
6. Unit test coverage > 80% for `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`
7. All 5 FRs implemented with passing tests
8. Integration tests pass against real PostgreSQL and Redis
9. Load test: 500 concurrent users with endpoints < 200ms p95

**Business (from TDD):**
10. User registration conversion > 60% (funnel from `RegisterPage` to confirmed account)
11. Daily active authenticated users > 1000 within 30 days of GA (via `AuthToken` issuance counts)

**Business (from PRD — additional):**
12. Average session duration > 30 minutes (via token refresh event analytics)
13. Failed login rate < 5% of attempts (auth event log analysis)
14. Password reset completion > 80% (funnel: reset requested → new password set)

## Open Questions

1. **OQ-001** — Should `AuthService` support API key authentication for service-to-service calls? (Owner: test-lead, Target: 2026-04-15, Status: Open; deferred to v1.1 scope discussion)
2. **OQ-002** — What is the maximum allowed `UserProfile` roles array length? (Owner: auth-team, Target: 2026-04-01, Status: Open; pending RBAC design review)

**Additional open questions carried from PRD (not addressed in TDD):**
3. **OQ-PRD-001** — Should password reset emails be sent synchronously or asynchronously? (Owner: Engineering) — TDD does not specify.
4. **OQ-PRD-002** — Maximum number of refresh tokens allowed per user across devices? (Owner: Product) — TDD implies unlimited; no cap defined.
5. **OQ-PRD-003** — Account lockout policy after N consecutive failed login attempts? (Owner: Security) — TDD specifies 5 attempts/15 min for login; PRD mentions 5 attempts triggers admin notification, but admin notification mechanism is not in TDD.
6. **OQ-PRD-004** — Should we support "remember me" to extend session duration? (Owner: Product) — TDD does not address.

**JTBD-to-FR coverage gaps:**
7. PRD JTBD for Jordan (admin) — "view authentication event logs to investigate incidents and satisfy auditors" — no corresponding FR in TDD. Audit log is mentioned in Data Storage (90-day retention) but no API for admin access. **Note:** PRD requires 12-month retention (NFR-COMPLIANCE-001); TDD defines 90-day retention — conflict requiring resolution.
8. PRD user story — "log out" endpoint — not present in TDD API surface (no POST `/auth/logout`).

## Data Models and Interfaces

### DM-001: UserProfile

**Type:** TypeScript interface / PostgreSQL entity
**Storage:** PostgreSQL 15, indefinite retention
**Source:** TDD S7.1

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

**Fields:**
| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string (UUID) | PRIMARY KEY, NOT NULL | Generated by `AuthService` |
| email | string | UNIQUE, NOT NULL, indexed | Normalized lowercase |
| displayName | string | NOT NULL, 2-100 chars | UI display |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Last modification |
| lastLoginAt | string (ISO 8601) | NULLABLE | Updated on successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Authorization roles; enforcement downstream |

**Relationships:** Referenced by `AuthToken` (via id embedded in JWT payload); referenced by audit log entries.

### DM-002: AuthToken

**Type:** TypeScript interface / Redis record (refresh portion)
**Storage:** accessToken stateless (JWT); refreshToken in Redis with 7-day TTL
**Source:** TDD S7.1

```ts
interface AuthToken {
  accessToken: string;   // JWT, 15-min expiry
  refreshToken: string;  // opaque, Redis-backed
  expiresIn: number;     // 900 (seconds)
  tokenType: string;     // "Bearer"
}
```

**Fields:**
| Field | Type | Constraints | Description |
|---|---|---|---|
| accessToken | string (JWT) | NOT NULL | RS256-signed; contains user id and roles |
| refreshToken | string | NOT NULL, unique | Opaque token in Redis (hashed at rest); 7-day TTL |
| expiresIn | number | NOT NULL | Always 900 (15 min) |
| tokenType | string | NOT NULL | Always "Bearer" (OAuth2 compatibility) |

**Relationships:** Contains user id from `UserProfile` in JWT payload.

**Data Flow:** Login → `PasswordHasher.verify()` → `TokenManager.issueTokens()` → `JwtService.sign()` → Redis insert (refreshToken hash). Refresh → Redis lookup → revoke old → issue new pair. Logout path: not defined in TDD.

**Audit Log Entity (implicit):** PostgreSQL, 90-day retention per TDD §7.2 (conflicts with PRD 12-month requirement). Fields not fully enumerated in TDD.

## API Specifications

### API-001: POST /auth/login

**Auth:** None (public)
**Rate limit:** 10 req/min per IP
**Description:** Authenticate user via `AuthService`; validates email/password via `PasswordHasher`; issues tokens via `TokenManager`.

**Request:**
```json
{ "email": "user@example.com", "password": "SecurePass123!" }
```

**Response 200:**
```json
{ "accessToken": "eyJhbGci...", "refreshToken": "dGhpcyBp...", "expiresIn": 900, "tokenType": "Bearer" }
```

**Errors:** 401 (invalid creds), 423 (locked after 5 failed), 429 (rate limit).

### API-002: POST /auth/register

**Auth:** None
**Rate limit:** 5 req/min per IP
**Description:** Creates new `UserProfile`; validates email uniqueness; enforces password policy; hashes via `PasswordHasher`.

**Request:**
```json
{ "email": "newuser@example.com", "password": "SecurePass123!", "displayName": "New User" }
```

**Response 201:** Full `UserProfile` JSON (id, email, displayName, createdAt, updatedAt, lastLoginAt=null, roles=["user"]).

**Errors:** 400 (validation: weak password, invalid email), 409 (duplicate email).

### API-003: GET /auth/me

**Auth:** Required (Bearer accessToken)
**Rate limit:** 60 req/min per user
**Description:** Returns authenticated user's `UserProfile`.

**Request headers:** `Authorization: Bearer <jwt>`

**Response 200:** `UserProfile` JSON.

**Errors:** 401 (missing, expired, or invalid accessToken).

### API-004: POST /auth/refresh

**Auth:** Refresh token in body
**Rate limit:** 30 req/min per user
**Description:** Exchange valid refreshToken for new `AuthToken` pair via `TokenManager`; old refresh token revoked.

**Request:**
```json
{ "refreshToken": "dGhpcyBp..." }
```

**Response 200:** New `AuthToken` pair (JWT access + new opaque refresh).

**Errors:** 401 (expired or revoked refresh token).

**API Governance:**
- Versioning: URL prefix `/v1/auth/*` in production
- Breaking changes require new major version
- Non-breaking additions (optional fields) permitted within current version
- Error envelope: `{ "error": { "code": "AUTH_*", "message": "...", "status": NNN } }`

**Implicit but not defined in TDD API surface (gaps):**
- POST `/auth/reset-request` — referenced in FR-AUTH-005 but no detailed endpoint spec
- POST `/auth/reset-confirm` — referenced in FR-AUTH-005 but no detailed endpoint spec
- POST `/auth/logout` — referenced in PRD but absent from TDD

## Component Inventory

### COMP-001: LoginPage

**Type:** Frontend route/page component
**Location:** Route `/login`
**Props:** `onSuccess: () => void`, `redirectUrl?: string`
**Auth required:** No
**Description:** Email/password login form; calls POST `/auth/login`; stores `AuthToken` via `AuthProvider`.
**Dependencies:** `AuthProvider`, `AuthService` login endpoint.

### COMP-002: RegisterPage

**Type:** Frontend route/page component
**Location:** Route `/register`
**Props:** `onSuccess: () => void`, `termsUrl: string`
**Auth required:** No
**Description:** Registration form (email, password, displayName); client-side password strength validation; calls POST `/auth/register`.
**Dependencies:** `AuthService` register endpoint.

### COMP-003: ProfilePage

**Type:** Frontend route/page component
**Location:** Route `/profile`
**Auth required:** Yes
**Description:** Displays `UserProfile` data; calls GET `/auth/me`.
**Dependencies:** `AuthProvider`, `AuthService` me endpoint.

### COMP-004: AuthProvider

**Type:** React context provider (shared component)
**Props:** `children: ReactNode`
**Description:** Wraps application; manages `AuthToken` state; silent refresh via `TokenManager`; exposes `UserProfile` and auth methods; intercepts 401s; redirects unauthenticated users to `LoginPage`.
**Dependencies:** `TokenManager` (via API), `AuthService`.

### COMP-005: AuthService

**Type:** Backend orchestration service
**Description:** Facade receiving API Gateway requests; delegates to `PasswordHasher`, `TokenManager`, `JwtService`, user repo.
**Dependencies:** `PasswordHasher`, `TokenManager`, `JwtService`, PostgreSQL, Redis, SendGrid.

### COMP-006: TokenManager

**Type:** Backend service
**Description:** JWT lifecycle management; issues, refreshes, revokes tokens; Redis-backed refresh token store with 7-day TTL.
**Dependencies:** `JwtService`, Redis.

### COMP-007: JwtService

**Type:** Backend service
**Description:** JWT sign/verify using RS256, 2048-bit RSA keys, 5s clock skew tolerance, quarterly key rotation.
**Dependencies:** RSA keypair (secrets volume).

### COMP-008: PasswordHasher

**Type:** Backend service
**Description:** bcrypt-based password hashing and verification; cost factor 12; abstracts algorithm for future migration.
**Dependencies:** bcryptjs library.

**Component Hierarchy (Frontend):**
```
App
└── AuthProvider
    ├── PublicRoutes
    │   ├── LoginPage
    │   └── RegisterPage
    └── ProtectedRoutes
        └── ProfilePage
```

**Component Hierarchy (Backend):**
```
API Gateway → AuthService
                ├── PasswordHasher → bcrypt
                ├── TokenManager → JwtService → RSA keys
                │   └── Redis (refresh tokens)
                ├── UserRepo → PostgreSQL
                └── Email → SendGrid
```

## Testing Strategy

**Test Pyramid:**
| Level | Coverage Target | Tools | Focus |
|---|---|---|---|
| Unit | 80% | Jest, ts-jest | AuthService methods, PasswordHasher, JwtService, TokenManager, UserProfile validation |
| Integration | 15% | Supertest, testcontainers | Endpoint cycles, DB ops, Redis storage, AuthService→PasswordHasher→DB flow |
| E2E | 5% | Playwright | LoginPage, RegisterPage, AuthProvider refresh, registration→profile journey |

### TEST-001: Login with valid credentials returns AuthToken
**Level:** Unit
**Component:** `AuthService`
**Validates:** FR-AUTH-001
**Input:** Valid email/password.
**Expected:** `AuthService.login()` calls `PasswordHasher.verify()` → `TokenManager.issueTokens()` → returns valid `AuthToken` with accessToken + refreshToken.
**Mocks:** `PasswordHasher`, `TokenManager`.

### TEST-002: Login with invalid credentials returns error
**Level:** Unit
**Component:** `AuthService`
**Validates:** FR-AUTH-001
**Input:** Invalid password.
**Expected:** 401 returned; no `AuthToken` issued when `PasswordHasher.verify()` returns false.
**Mocks:** `PasswordHasher` returning false.

### TEST-003: Token refresh with valid refresh token
**Level:** Unit
**Component:** `TokenManager`
**Validates:** FR-AUTH-003
**Input:** Valid refresh token.
**Expected:** `TokenManager.refresh()` validates, revokes old, issues new pair via `JwtService`.
**Mocks:** Redis, `JwtService`.

### TEST-004: Registration persists UserProfile to database
**Level:** Integration
**Scope:** `AuthService` + PostgreSQL
**Validates:** FR-AUTH-002
**Input:** POST `/auth/register` with valid payload.
**Expected:** `UserProfile` row inserted; bcrypt hash stored; 201 returned.
**Environment:** testcontainers PostgreSQL.

### TEST-005: Expired refresh token rejected by TokenManager
**Level:** Integration
**Scope:** `TokenManager` + Redis
**Validates:** FR-AUTH-003
**Input:** Refresh token past 7-day TTL.
**Expected:** Redis TTL expiration → 401.
**Environment:** testcontainers Redis.

### TEST-006: User registers and logs in end-to-end
**Level:** E2E
**Flow:** `RegisterPage` → `LoginPage` → `ProfilePage`
**Validates:** FR-AUTH-001, FR-AUTH-002
**Expected:** Full journey through `AuthProvider`; tokens persist; profile rendered.
**Environment:** Playwright against staging.

**Test Environments:**
| Environment | Purpose | Data |
|---|---|---|
| Local | Developer testing | Docker Compose (PostgreSQL + Redis) |
| CI | Automated pipeline | testcontainers (ephemeral) |
| Staging | Pre-production validation | Seeded test accounts, isolated |

## Migration and Rollout Plan

### MIG-001: Phase 1 — Internal Alpha
**Duration:** 1 week
**Description:** Deploy `AuthService` to staging; auth-team + QA test all endpoints; `LoginPage` and `RegisterPage` behind `AUTH_NEW_LOGIN` flag.
**Success criteria:** All FR-AUTH-001 through FR-AUTH-005 pass manual testing; zero P0/P1 bugs.
**Dependencies:** None (starting phase).

### MIG-002: Phase 2 — Beta (10%)
**Duration:** 2 weeks
**Description:** Enable `AUTH_NEW_LOGIN` for 10% of traffic; monitor `AuthService` latency, error rates, `TokenManager` Redis usage; `AuthProvider` handles refresh under real load.
**Success criteria:** p95 latency < 200ms; error rate < 0.1%; no Redis connection failures.
**Dependencies:** MIG-001 complete.

### MIG-003: Phase 3 — General Availability (100%)
**Duration:** 1 week
**Description:** Remove `AUTH_NEW_LOGIN` flag; all users route through new `AuthService`; legacy endpoints deprecated; `AUTH_TOKEN_REFRESH` enables refresh flow.
**Success criteria:** 99.9% uptime over first 7 days; all dashboards green.
**Dependencies:** MIG-002 complete.

**Feature Flags:**
| Flag | Purpose | Default | Removal Target | Owner |
|---|---|---|---|---|
| `AUTH_NEW_LOGIN` | Gates new `LoginPage` + `AuthService` login endpoint | OFF | After Phase 3 GA | auth-team |
| `AUTH_TOKEN_REFRESH` | Enables refresh token flow in `TokenManager` | OFF | Phase 3 + 2 weeks | auth-team |

**Rollback Procedure:**
1. Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth
2. Verify legacy login flow via smoke tests
3. Investigate `AuthService` failure root cause via structured logs and traces
4. If `UserProfile` data corruption detected, restore from last known-good backup
5. Notify auth-team and platform-team via incident channel
6. Post-mortem within 48 hours of rollback

**Rollback Criteria:**
- p95 latency > 1000ms for > 5 minutes
- Error rate > 5% for > 2 minutes
- `TokenManager` Redis connection failures > 10 per minute
- Any `UserProfile` data loss or corruption

**Milestones:**
| Milestone | Target Date | Deliverables |
|---|---|---|
| M1: Core AuthService | 2026-04-14 | `AuthService`, `PasswordHasher`, `UserProfile` schema, /register, /login |
| M2: Token Management | 2026-04-28 | `TokenManager`, `JwtService`, `AuthToken`, /refresh, /me |
| M3: Password Reset | 2026-05-12 | FR-AUTH-005, email integration |
| M4: Frontend Integration | 2026-05-26 | `LoginPage`, `RegisterPage`, `AuthProvider` |
| M5: GA Release | 2026-06-09 | Phase 3 complete, feature flags removed |

## Operational Readiness

### OPS-001: Runbook — AuthService down
**Symptoms:** 5xx on all `/auth/*`; `LoginPage`/`RegisterPage` show error state.
**Diagnosis:** Check pod health; verify PostgreSQL connectivity; check `PasswordHasher`/`TokenManager` init logs.
**Resolution:** Restart pods; failover PostgreSQL to read replica if unreachable; if Redis down, `TokenManager` rejects refresh (users re-login).
**Escalation:** auth-team on-call → 15 min → platform-team.
**Prevention:** HPA scaling, health checks, connection pooling, Redis HA.

### OPS-002: Runbook — Token refresh failures
**Symptoms:** Users logged out unexpectedly; `AuthProvider` redirect loop; `auth_token_refresh_total` error counter spikes.
**Diagnosis:** Check Redis connectivity from `TokenManager`; verify `JwtService` signing key accessible; check `AUTH_TOKEN_REFRESH` flag state.
**Resolution:** Scale Redis cluster if degraded; re-mount secrets volume if key unavailable; enable flag if OFF.
**Escalation:** auth-team on-call → Redis cluster issues → platform-team.
**Prevention:** Redis monitoring, secret rotation runbook, feature-flag alerts.

### OPS-003: On-Call Expectations
**Response time:** Acknowledge P1 alerts within 15 minutes.
**Coverage:** auth-team provides 24/7 on-call rotation during first 2 weeks post-GA.
**Tooling:** Kubernetes dashboards, Grafana, Redis CLI, PostgreSQL admin.
**Escalation path:** auth-team on-call → test-lead → eng-manager → platform-team.
**Knowledge prerequisites:** Runbook familiarity (OPS-001, OPS-002), feature flag operations.

### OPS-004: Capacity Planning
**AuthService pods:** Current 3 replicas; expected 500 concurrent users; HPA scales to 10 replicas on CPU > 70%.
**PostgreSQL connections:** Current pool 100; expected 50 avg concurrent queries; increase to 200 if wait time > 50ms.
**Redis memory:** Current 1 GB; expected ~100K refresh tokens (~50 MB); scale to 2 GB if > 70% utilized.

### OPS-005: Observability
**Logs:** Structured logs for login success/failure, registration, token refresh, password reset. Sensitive fields (password, tokens) excluded.
**Metrics (Prometheus):**
- `auth_login_total` (counter)
- `auth_login_duration_seconds` (histogram)
- `auth_token_refresh_total` (counter)
- `auth_registration_total` (counter)
**Tracing:** OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`.
**Alerts:**
- Login failure rate > 20% over 5 minutes
- p95 latency > 500ms
- `TokenManager` Redis connection failures
**Dashboards:** Grafana (login volume, latency histograms, refresh success rate, error rates).

**Gap vs PRD compliance (NFR-COMPLIANCE-001):** TDD observability does not explicitly enumerate SOC2-required audit log fields (user ID, IP, outcome) or 12-month retention. TDD §7.2 specifies 90-day audit log retention in PostgreSQL — conflicts with PRD 12-month requirement; requires resolution before SOC2 readiness.
