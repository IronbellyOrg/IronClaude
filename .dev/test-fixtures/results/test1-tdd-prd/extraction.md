---
spec_source: "test-tdd-user-auth.md"
generated: "2026-03-31T12:00:00Z"
generator: "requirements-extraction-agent"
functional_requirements: 5
nonfunctional_requirements: 8
total_requirements: 13
complexity_score: 0.55
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, testing, devops]
risks_identified: 3
dependencies_identified: 9
success_criteria_count: 10
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 9
test_artifacts_identified: 6
migration_items_identified: 15
operational_items_identified: 12
pipeline_diagnostics: {elapsed_seconds: 196.7, started_at: "2026-03-31T13:25:03.140018+00:00", finished_at: "2026-03-31T13:28:19.850812+00:00"}
---

## Functional Requirements

### FR-AUTH-001: Login with email and password

- **Description:** `AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
- **Components:** `AuthService`, `PasswordHasher`, `TokenManager`
- **Acceptance Criteria:**
  1. Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken.
  2. Invalid credentials return 401 with error message.
  3. Non-existent email returns 401 (no user enumeration).
  4. Account locked after 5 failed attempts within 15 minutes.
- **API Surface:** POST `/auth/login`
- **Priority:** Highest (Milestone M1)

### FR-AUTH-002: User registration with validation

- **Description:** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
- **Components:** `AuthService`, `PasswordHasher`, `UserRepo`
- **Acceptance Criteria:**
  1. Valid registration returns 201 with `UserProfile` data.
  2. Duplicate email returns 409 Conflict.
  3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
  4. `PasswordHasher` stores bcrypt hash with cost factor 12.
- **API Surface:** POST `/auth/register`
- **Priority:** Highest (Milestone M1)

### FR-AUTH-003: JWT token issuance and refresh

- **Description:** `TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
- **Components:** `TokenManager`, `JwtService`, Redis
- **Acceptance Criteria:**
  1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
  2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
  3. Expired refreshToken returns 401.
  4. Revoked refreshToken returns 401.
- **API Surface:** POST `/auth/refresh`
- **Priority:** Highest (Milestone M2)

### FR-AUTH-004: User profile retrieval

- **Description:** `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
- **Components:** `AuthService`, `UserRepo`
- **Acceptance Criteria:**
  1. GET `/auth/me` with valid accessToken returns `UserProfile`.
  2. Expired or invalid token returns 401.
  3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.
- **API Surface:** GET `/auth/me`
- **Priority:** High (Milestone M2)

### FR-AUTH-005: Password reset flow

- **Description:** `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
- **Components:** `AuthService`, `PasswordHasher`, Email Service (SendGrid)
- **Acceptance Criteria:**
  1. POST `/auth/reset-request` with valid email sends reset token via email.
  2. POST `/auth/reset-confirm` with valid token updates the password hash.
  3. Reset tokens expire after 1 hour.
  4. Used reset tokens cannot be reused.
- **API Surface:** POST `/auth/reset-request`, POST `/auth/reset-confirm`
- **Priority:** High (Milestone M3)

---

## Non-Functional Requirements

### NFR-PERF-001: API response time

- **Category:** Performance
- **Requirement:** All auth endpoints must respond in < 200ms at p95.
- **Measurement:** APM tracing on `AuthService` methods.

### NFR-PERF-002: Concurrent authentication

- **Category:** Performance
- **Requirement:** Support 500 concurrent login requests.
- **Measurement:** Load testing with k6.

### NFR-REL-001: Service availability

- **Category:** Reliability
- **Requirement:** 99.9% uptime measured over 30-day rolling windows.
- **Measurement:** Uptime monitoring via health check endpoint.

### NFR-SEC-001: Password hashing

- **Category:** Security
- **Requirement:** `PasswordHasher` must use bcrypt with cost factor 12.
- **Measurement:** Unit test asserting bcrypt cost parameter.

### NFR-SEC-002: Token signing

- **Category:** Security
- **Requirement:** `JwtService` must sign tokens with RS256 using 2048-bit RSA keys.
- **Measurement:** Configuration validation test.

### NFR-COMP-001: GDPR consent at registration (PRD S17)

- **Category:** Compliance
- **Requirement:** Users must consent to data collection at registration. Consent recorded with timestamp.
- **Source:** PRD AUTH-PRD-001, Legal & Compliance section. Not explicitly stated in TDD.
- **Standard:** GDPR

### NFR-COMP-002: SOC2 audit logging (PRD S17)

- **Category:** Compliance
- **Requirement:** All auth events must be logged with user ID, timestamp, IP, and outcome. 12-month retention.
- **Source:** PRD AUTH-PRD-001, Legal & Compliance section. TDD Section 7.2 specifies 90-day audit log retention, which conflicts with the PRD's 12-month requirement. See Open Questions.
- **Standard:** SOC2 Type II

### NFR-COMP-003: GDPR data minimization (PRD S17)

- **Category:** Compliance
- **Requirement:** Only email, hashed password, and display name collected. No additional PII required.
- **Source:** PRD AUTH-PRD-001, Legal & Compliance section.
- **Standard:** GDPR

---

## Complexity Assessment

**Complexity Score:** 0.55
**Complexity Class:** MEDIUM

**Scoring Rationale:**

| Factor | Score | Rationale |
|--------|-------|-----------|
| Domain complexity | 0.5 | Authentication is a well-understood domain with established patterns (JWT, bcrypt, refresh tokens). No novel algorithmic challenges. |
| Integration surface | 0.6 | Three external systems (PostgreSQL, Redis, SendGrid) plus API Gateway and frontend components. All use standard protocols. |
| Data model complexity | 0.3 | Two primary entities (`UserProfile`, `AuthToken`) with straightforward schemas. No complex relationships or hierarchies. |
| Security sensitivity | 0.8 | Credential handling, token management, and brute-force mitigation require careful implementation. High impact of errors. |
| Migration risk | 0.5 | Three-phase rollout with feature flags. Parallel operation with legacy system reduces risk but adds operational complexity. |
| Team coordination | 0.6 | Cross-team impact (auth-team, platform-team, frontend-team). Frontend integration adds coordination overhead. |

**Overall:** Standard backend service with elevated security requirements. Well-scoped with clear boundaries and proven technology choices. The phased rollout and feature flag strategy are appropriate for the risk level.

---

## Architectural Constraints

1. **Stateless authentication via JWT.** `JwtService` signs access tokens with RS256 using 2048-bit RSA keys. No server-side session storage for access tokens. (Section 6.4)
2. **bcrypt password hashing with cost factor 12.** `PasswordHasher` abstracts the algorithm for future migration but must use bcrypt in v1.0. (Section 6.4, NFR-SEC-001)
3. **Refresh tokens stored in Redis.** `TokenManager` stores refresh tokens with 7-day TTL in Redis. Redis unavailability causes refresh rejection, not stale token serving. (Section 6.2, Section 12)
4. **PostgreSQL 15+ for persistence.** `UserProfile` records and audit logs stored in PostgreSQL with connection pooling via pg-pool. (Section 7.2)
5. **Node.js 20 LTS runtime.** Mandated runtime for the `AuthService`. (Section 18)
6. **API versioned via URL prefix.** Production endpoints use `/v1/auth/*`. Breaking changes require new major version. (Section 8.4)
7. **TLS 1.3 enforced on all endpoints.** No plaintext HTTP. (Section 13)
8. **5-second clock skew tolerance in JWT validation.** `JwtService` allows ±5 seconds for distributed clock drift. (Section 12)
9. **CORS restricted to known frontend origins.** (Section 13)
10. **Persona-driven design (PRD S7):** Three user personas (Alex the End User, Jordan the Platform Admin, Sam the API Consumer) drive API design decisions. Alex requires frictionless UX; Sam requires programmatic token management; Jordan requires audit log access. Admin-facing features (audit log querying) are present in PRD user stories but not explicitly covered by TDD functional requirements.

---

## Risk Inventory

1. **R-001: Token theft via XSS allows session hijacking** — Severity: HIGH. Probability: Medium. Mitigation: Store accessToken in memory only (not localStorage); `AuthProvider` clears tokens on tab close; HttpOnly cookies for refreshToken; `JwtService` uses short 15-minute expiry. Contingency: Immediate token revocation via `TokenManager`; force password reset for affected accounts.

2. **R-002: Brute-force attacks on login endpoint** — Severity: MEDIUM. Probability: High. Mitigation: Rate limiting at API Gateway (10 req/min per IP); account lockout after 5 failed attempts; bcrypt cost factor 12 makes offline cracking expensive. Contingency: Block offending IPs at WAF level; enable CAPTCHA on `LoginPage` after 3 failed attempts.

3. **R-003: Data loss during migration from legacy auth** — Severity: HIGH. Probability: Low. Mitigation: Run `AuthService` in parallel with legacy system during Phase 1 and Phase 2; `UserProfile` migration uses idempotent upsert operations; full database backup before each phase. Contingency: Rollback to legacy auth system; restore `UserProfile` data from pre-migration backup.

---

## Dependency Inventory

| # | Dependency | Type | Version/Detail | Used By | Impact if Unavailable |
|---|-----------|------|----------------|---------|----------------------|
| 1 | PostgreSQL | Infrastructure | 15+ | `UserRepo`, Audit log | No persistent user storage; total service failure |
| 2 | Redis | Infrastructure | 7+ | `TokenManager` | Refresh token flow broken; users must re-login |
| 3 | Node.js | Runtime | 20 LTS | `AuthService` (all components) | Service cannot run |
| 4 | bcryptjs | Library | — | `PasswordHasher` | Password hashing/verification impossible |
| 5 | jsonwebtoken | Library | — | `JwtService` | Token signing/verification impossible |
| 6 | SendGrid API | External Service | — | Password reset emails | FR-AUTH-005 password reset flow blocked |
| 7 | AUTH-PRD-001 | Upstream Document | — | Requirements source | No product requirements to implement against |
| 8 | INFRA-DB-001 | Infrastructure Dependency | — | Database provisioning | No database available |
| 9 | SEC-POLICY-001 | Policy Document | — | `PasswordHasher`, `JwtService` config | Password and token policies undefined |

---

## Success Criteria

### From TDD (Section 4)

| # | Metric | Target | Measurement Method |
|---|--------|--------|--------------------|
| 1 | Login response time (p95) | < 200ms | APM instrumentation on `AuthService.login()` |
| 2 | Registration success rate | > 99% | Ratio of successful registrations to attempts |
| 3 | Token refresh latency (p95) | < 100ms | APM instrumentation on `TokenManager.refresh()` |
| 4 | Service availability | 99.9% uptime | Health check monitoring over 30-day windows |
| 5 | Password hash time | < 500ms | Benchmark of `PasswordHasher.hash()` with bcrypt cost 12 |
| 6 | User registration conversion | > 60% | Funnel analytics from `RegisterPage` to confirmed account |
| 7 | Daily active authenticated users | > 1000 within 30 days of GA | `AuthToken` issuance counts |

### From PRD Success Metrics (S19 — supplementary)

| # | Metric | Target | Measurement Method | Business Rationale |
|---|--------|--------|--------------------|--------------------|
| 8 | Average session duration | > 30 minutes | Token refresh event analytics | Longer sessions = engaged users |
| 9 | Failed login rate | < 5% of attempts | Auth event log analysis | High failure = UX or security issue |
| 10 | Password reset completion | > 80% | Funnel: reset requested -> new password set | Validates self-service recovery |

---

## Open Questions

### From TDD (Section 22)

| ID | Question | Owner | Target Date | Status |
|----|----------|-------|-------------|--------|
| OQ-001 | Should `AuthService` support API key authentication for service-to-service calls? | test-lead | 2026-04-15 | Open |
| OQ-002 | What is the maximum allowed `UserProfile` roles array length? | auth-team | 2026-04-01 | Open |

### From PRD (Section — Open Questions)

| ID | Question | Owner | Status |
|----|----------|-------|--------|
| OQ-PRD-001 | Should password reset emails be sent synchronously or asynchronously? | Engineering | Open |
| OQ-PRD-002 | Maximum number of refresh tokens allowed per user across devices? | Product | Open |
| OQ-PRD-003 | Should we support "remember me" to extend session duration? | Product | Open |

### Extraction-Identified Gaps

| ID | Question | Source |
|----|----------|--------|
| OQ-EXT-001 | TDD audit log retention is 90 days (Section 7.2) but PRD requires 12-month retention for SOC2 (S17). Which value is authoritative? | TDD Section 7.2 vs PRD S17 |
| OQ-EXT-002 | PRD user story for Jordan (admin) requires queryable auth event logs (by date range and user). No corresponding TDD API endpoint or functional requirement exists. Is admin log access in scope for v1.0? | PRD AUTH-E3 user stories |
| OQ-EXT-003 | PRD user story requires logout functionality. No TDD functional requirement or API endpoint for logout exists. Is logout in scope? | PRD AUTH-E1 user stories |
| OQ-EXT-004 | PRD JTBD #4 (Sam the API consumer: programmatic authentication and token refresh) lacks a dedicated TDD functional requirement beyond FR-AUTH-003. Is service-to-service auth covered by OQ-001, or does it need a separate FR? | PRD S6 JTBD #4 |
| OQ-EXT-005 | PRD requires GDPR consent recording at registration (S17). TDD `UserProfile` schema has no consent field. Should a consent timestamp be added to the data model? | PRD S17 vs TDD Section 7.1 |
| OQ-EXT-006 | PRD specifies account lockout policy as an open question (OQ-PRD, Owner: Security), but TDD hardcodes 5 attempts / 15 minutes in FR-AUTH-001. Has this been formally decided? | PRD Open Questions vs TDD FR-AUTH-001 |

---

## Data Models and Interfaces

### Entity: UserProfile

```ts
interface UserProfile {
  id: string;            // UUID v4, primary key
  email: string;         // unique, indexed, lowercase normalized
  displayName: string;   // user-chosen display name, 2-100 chars
  createdAt: string;     // ISO 8601 timestamp
  updatedAt: string;     // ISO 8601 timestamp
  lastLoginAt: string;   // ISO 8601 timestamp, nullable
  roles: string[];       // e.g., ["user"], ["user", "admin"]
}
```

| Field | Type | Constraints | Required | Description |
|-------|------|-------------|----------|-------------|
| id | string (UUID v4) | PRIMARY KEY, NOT NULL | Yes | Unique user identifier generated by `AuthService` |
| email | string | UNIQUE, NOT NULL, indexed, lowercase normalized | Yes | User email address |
| displayName | string | NOT NULL, 2-100 chars | Yes | Display name shown in UI |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Yes | Account creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Yes | Last profile modification timestamp |
| lastLoginAt | string (ISO 8601) | NULLABLE | No | Updated by `AuthService` on successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Yes | Authorization roles; enforcement is downstream |

### Entity: AuthToken

```ts
interface AuthToken {
  accessToken: string;   // JWT signed by JwtService, 15-min expiry
  refreshToken: string;  // opaque token stored in Redis by TokenManager
  expiresIn: number;     // seconds until accessToken expires (900)
  tokenType: string;     // always "Bearer"
}
```

| Field | Type | Constraints | Required | Description |
|-------|------|-------------|----------|-------------|
| accessToken | string (JWT) | NOT NULL | Yes | Signed by `JwtService` using RS256; payload contains user id and roles |
| refreshToken | string | NOT NULL, unique | Yes | Opaque token managed by `TokenManager`; stored in Redis with 7-day TTL |
| expiresIn | number | NOT NULL | Yes | Seconds until accessToken expiration; always 900 (15 minutes) |
| tokenType | string | NOT NULL | Yes | Always "Bearer"; included for OAuth2 compatibility |

### Entity Relationships

- `AuthService.login()` validates credentials → produces `AuthToken` for a given `UserProfile`
- `TokenManager` stores `refreshToken` in Redis keyed to `UserProfile.id`
- `JwtService` encodes `UserProfile.id` and `UserProfile.roles` into `accessToken` payload

### Data Storage Strategy

| Store | Technology | Purpose | Retention |
|-------|-----------|---------|-----------|
| User records | PostgreSQL 15 | `UserProfile` persistence, password hashes | Indefinite |
| Refresh tokens | Redis 7 | `TokenManager` token storage and revocation | 7-day TTL |
| Audit log | PostgreSQL 15 | Login attempts, password resets | 90 days (TDD) / 12 months (PRD — see OQ-EXT-001) |

---

## API Specifications

### Endpoint Inventory

| # | Method | Path | Auth Required | Rate Limit | Description |
|---|--------|------|---------------|------------|-------------|
| 1 | POST | `/auth/login` | No | 10 req/min per IP | Authenticate user, return `AuthToken` |
| 2 | POST | `/auth/register` | No | 5 req/min per IP | Create new `UserProfile`, return profile data |
| 3 | GET | `/auth/me` | Yes (Bearer) | 60 req/min per user | Return authenticated user's `UserProfile` |
| 4 | POST | `/auth/refresh` | No (refresh token in body) | 30 req/min per user | Exchange refresh token for new `AuthToken` |
| 5 | POST | `/auth/reset-request` | No | — | Request password reset email |
| 6 | POST | `/auth/reset-confirm` | No | — | Confirm password reset with token |

### Endpoint Details

#### 1. POST `/auth/login`

- **Auth:** None
- **Rate Limit:** 10 req/min per IP
- **Request Body:**
  ```json
  { "email": "string", "password": "string" }
  ```
- **Response (200):** `AuthToken` object (accessToken, refreshToken, expiresIn, tokenType)
- **Error Responses:**
  - 401 Unauthorized: Invalid email or password (code: `AUTH_INVALID_CREDENTIALS`)
  - 423 Locked: Account locked after 5 failed attempts
  - 429 Too Many Requests: Rate limit exceeded

#### 2. POST `/auth/register`

- **Auth:** None
- **Rate Limit:** 5 req/min per IP
- **Request Body:**
  ```json
  { "email": "string", "password": "string", "displayName": "string" }
  ```
- **Response (201):** `UserProfile` object
- **Error Responses:**
  - 400 Bad Request: Validation errors (weak password, invalid email)
  - 409 Conflict: Email already registered

#### 3. GET `/auth/me`

- **Auth:** Bearer token (JWT accessToken)
- **Rate Limit:** 60 req/min per user
- **Request Headers:** `Authorization: Bearer <accessToken>`
- **Response (200):** `UserProfile` object
- **Error Responses:**
  - 401 Unauthorized: Missing, expired, or invalid accessToken

#### 4. POST `/auth/refresh`

- **Auth:** None (refresh token in body)
- **Rate Limit:** 30 req/min per user
- **Request Body:**
  ```json
  { "refreshToken": "string" }
  ```
- **Response (200):** New `AuthToken` object (old refresh token revoked)
- **Error Responses:**
  - 401 Unauthorized: Expired or revoked refresh token

#### 5. POST `/auth/reset-request`

- **Auth:** None
- **Request Body:** `{ "email": "string" }`
- **Response:** Success response regardless of email existence (prevents enumeration)

#### 6. POST `/auth/reset-confirm`

- **Auth:** None
- **Request Body:** `{ "token": "string", "newPassword": "string" }`
- **Response:** Success on valid token; password updated
- **Error Responses:** 400/401 for invalid/expired/used tokens

### Error Response Format

All errors follow a consistent structure:
```json
{
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS",
    "message": "The provided email or password is incorrect.",
    "status": 401
  }
}
```

### Versioning Strategy

- URL prefix versioning: `/v1/auth/*` in production
- Breaking changes require a new major version
- Non-breaking additions (new optional fields) permitted within current version

---

## Component Inventory

### Backend Components

| # | Component | Type | Dependencies | Responsibility |
|---|-----------|------|-------------|----------------|
| 1 | `AuthService` | Backend Service (Orchestrator) | `PasswordHasher`, `TokenManager`, `UserRepo` | Facade that orchestrates all auth flows: login, registration, profile, password reset |
| 2 | `TokenManager` | Backend Module | `JwtService`, Redis | Issues, refreshes, and revokes token pairs; stores refresh tokens in Redis |
| 3 | `JwtService` | Backend Module | RSA key pair | Signs and verifies JWT access tokens using RS256 with 2048-bit keys |
| 4 | `PasswordHasher` | Backend Module | bcryptjs | Hashes and verifies passwords using bcrypt with cost factor 12 |
| 5 | `UserRepo` | Data Access Layer | PostgreSQL | CRUD operations on `UserProfile` records |

### Frontend Components

| # | Component | Type | Props | Dependencies |
|---|-----------|------|-------|-------------|
| 6 | `LoginPage` | Page Component | `onSuccess: () => void`, `redirectUrl?: string` | `AuthProvider`, POST `/auth/login` |
| 7 | `RegisterPage` | Page Component | `onSuccess: () => void`, `termsUrl: string` | `AuthProvider`, POST `/auth/register` |
| 8 | ProfilePage | Page Component | — | `AuthProvider`, GET `/auth/me` |
| 9 | `AuthProvider` | Context Provider | `children: ReactNode` | `TokenManager` (via API), token storage |

### Component Hierarchy

```
App
├── AuthProvider
│   ├── PublicRoutes
│   │   ├── LoginPage        (/login, no auth)
│   │   └── RegisterPage     (/register, no auth)
│   └── ProtectedRoutes
│       └── ProfilePage      (/profile, auth required)
```

### Route Structure

| Route | Page Component | Auth Required |
|-------|---------------|---------------|
| `/login` | `LoginPage` | No |
| `/register` | `RegisterPage` | No |
| `/profile` | ProfilePage | Yes |

---

## Testing Strategy

### Test Pyramid

| Level | Coverage Target | Tools | Focus Areas | Ownership |
|-------|----------------|-------|-------------|-----------|
| Unit | 80% | Jest, ts-jest | `AuthService` methods, `PasswordHasher` hashing/verification, `JwtService` sign/verify, `TokenManager` token lifecycle, `UserProfile` validation | auth-team |
| Integration | 15% | Supertest, testcontainers | API endpoint request/response cycles, database operations, Redis token storage, `AuthService`→`PasswordHasher`→database flow | auth-team |
| E2E | 5% | Playwright | `LoginPage` login flow, `RegisterPage` registration flow, `AuthProvider` token refresh, full user journey | QA |

### Unit Test Cases

| ID | Test Case | Component | Validates |
|----|-----------|-----------|-----------|
| UT-001 | Login with valid credentials returns `AuthToken` | `AuthService` | FR-AUTH-001: calls `PasswordHasher.verify()` then `TokenManager.issueTokens()` |
| UT-002 | Login with invalid credentials returns error | `AuthService` | FR-AUTH-001: returns 401 when `PasswordHasher.verify()` returns false |
| UT-003 | Token refresh with valid refresh token | `TokenManager` | FR-AUTH-003: validates, revokes old token, issues new pair via `JwtService` |

### Integration Test Cases

| ID | Test Case | Scope | Validates |
|----|-----------|-------|-----------|
| IT-001 | Registration persists `UserProfile` to database | `AuthService` + PostgreSQL | FR-AUTH-002: full flow from API request through `PasswordHasher` to database insert |
| IT-002 | Expired refresh token rejected by `TokenManager` | `TokenManager` + Redis | FR-AUTH-003: Redis TTL expiration correctly invalidates refresh tokens |

### E2E Test Cases

| ID | Test Case | Flow | Validates |
|----|-----------|------|-----------|
| E2E-001 | User registers and logs in | `RegisterPage` → `LoginPage` → ProfilePage | FR-AUTH-001, FR-AUTH-002: complete journey through `AuthProvider` |

### Test Environments

| Environment | Purpose | Data Strategy |
|-------------|---------|---------------|
| Local | Developer testing | Docker Compose with PostgreSQL and Redis containers |
| CI | Automated pipeline | testcontainers for ephemeral databases |
| Staging | Pre-production validation | Seeded test accounts, isolated from production |

---

## Migration and Rollout Plan

### Migration Phases

| Phase | Description | Duration | Dependencies | Success Criteria | Rollback |
|-------|-------------|----------|-------------|-----------------|----------|
| Phase 1: Internal Alpha | Deploy `AuthService` to staging. auth-team and QA test all endpoints. `LoginPage` and `RegisterPage` behind feature flag `AUTH_NEW_LOGIN`. | 1 week | Staging environment provisioned | All FR-AUTH-001 through FR-AUTH-005 pass manual testing. Zero P0/P1 bugs. | Disable `AUTH_NEW_LOGIN` flag |
| Phase 2: Beta (10%) | Enable `AUTH_NEW_LOGIN` for 10% of traffic. Monitor latency, error rates, Redis usage. `AuthProvider` handles token refresh under real load. | 2 weeks | Phase 1 complete | p95 latency < 200ms. Error rate < 0.1%. No Redis connection failures. | Reduce traffic to 0% via flag |
| Phase 3: General Availability (100%) | Remove `AUTH_NEW_LOGIN`. All users route through new `AuthService`. Legacy auth deprecated. `AUTH_TOKEN_REFRESH` enables refresh flow. | 1 week | Phase 2 complete | 99.9% uptime over first 7 days. All monitoring dashboards green. | Re-enable `AUTH_NEW_LOGIN` as gate |

### Feature Flags

| Flag | Purpose | Default State | Cleanup Target |
|------|---------|---------------|----------------|
| `AUTH_NEW_LOGIN` | Gates access to new `LoginPage` and `AuthService` login endpoint | OFF | Remove after Phase 3 GA |
| `AUTH_TOKEN_REFRESH` | Enables refresh token flow in `TokenManager`; when OFF, only access tokens issued | OFF | Remove after Phase 3 + 2 weeks |

### Rollback Procedure

1. Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth.
2. Verify legacy login flow is operational via smoke tests.
3. Investigate `AuthService` failure root cause using structured logs and traces.
4. If data corruption detected in `UserProfile` table, restore from last known-good backup.
5. Notify auth-team and platform-team via incident channel.
6. Post-mortem within 48 hours of rollback.

### Rollback Trigger Criteria

| # | Condition |
|---|-----------|
| 1 | p95 latency exceeds 1000ms for > 5 minutes |
| 2 | Error rate exceeds 5% for > 2 minutes |
| 3 | `TokenManager` Redis connection failures exceed 10 per minute |
| 4 | Any data loss or corruption detected in `UserProfile` records |

---

## Operational Readiness

### Runbook Scenarios

#### Scenario 1: AuthService Down

| Aspect | Detail |
|--------|--------|
| **Symptoms** | 5xx errors on all `/auth/*` endpoints; `LoginPage` and `RegisterPage` show error state |
| **Diagnosis** | Check `AuthService` pod health in Kubernetes. Verify PostgreSQL connectivity. Check `PasswordHasher` and `TokenManager` initialization logs. |
| **Resolution** | Restart `AuthService` pods. If PostgreSQL unreachable, failover to read replica. If Redis down, `TokenManager` rejects refresh requests — users must re-login via `LoginPage`. |
| **Escalation** | Page auth-team on-call. If unresolved in 15 minutes, escalate to platform-team. |
| **Prevention** | Health check monitoring, pod auto-restart via Kubernetes liveness probes. |

#### Scenario 2: Token Refresh Failures

| Aspect | Detail |
|--------|--------|
| **Symptoms** | Users report unexpected logouts; `AuthProvider` enters redirect loop to `LoginPage`; `auth_token_refresh_total` error counter spikes |
| **Diagnosis** | Check Redis connectivity from `TokenManager`. Verify `JwtService` signing key accessible. Check `AUTH_TOKEN_REFRESH` feature flag state. |
| **Resolution** | If Redis degraded, scale Redis cluster. If `JwtService` key unavailable, re-mount secrets volume. If flag OFF, enable `AUTH_TOKEN_REFRESH`. |
| **Escalation** | Page auth-team on-call. If Redis cluster issue, escalate to platform-team. |
| **Prevention** | Redis cluster monitoring with automatic failover; secrets rotation alerting. |

### On-Call Expectations

| Aspect | Expectation |
|--------|-------------|
| Response time | Acknowledge P1 alerts within 15 minutes |
| Coverage | auth-team provides 24/7 on-call rotation during first 2 weeks post-GA |
| Tooling | Kubernetes dashboards, Grafana monitoring, Redis CLI, PostgreSQL admin |
| Escalation path | auth-team on-call → test-lead → eng-manager → platform-team |

### Capacity Planning

| Resource | Current Capacity | Expected Load | Scaling Trigger | Scaling Plan |
|----------|-----------------|---------------|----------------|-------------|
| `AuthService` pods | 3 replicas | 500 concurrent users | CPU > 70% | HPA scales to 10 replicas |
| PostgreSQL connections | 100 pool size | 50 avg concurrent queries | Connection wait > 50ms | Increase pool to 200 |
| Redis memory | 1 GB | ~100K refresh tokens (~50 MB) | Memory > 70% | Scale to 2 GB |

### Observability

**Metrics (Prometheus):**
- `auth_login_total` (counter) — login attempts by outcome
- `auth_login_duration_seconds` (histogram) — login latency
- `auth_token_refresh_total` (counter) — token refresh attempts
- `auth_registration_total` (counter) — registration attempts

**Alerts:**
- Login failure rate > 20% over 5 minutes
- p95 latency > 500ms
- `TokenManager` Redis connection failures

**Tracing:** OpenTelemetry spans covering full request lifecycle through `AuthService`, `PasswordHasher`, `TokenManager`, and `JwtService`.

**Logging:** Structured logs for all auth events (login success/failure, registration, token refresh, password reset). Sensitive fields (password, tokens) excluded from logs.
