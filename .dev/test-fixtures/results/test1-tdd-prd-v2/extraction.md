---
spec_source: "test-tdd-user-auth.md"
generated: "2026-04-03T00:00:00Z"
generator: "extraction-agent-opus-4.6"
functional_requirements: 5
nonfunctional_requirements: 8
total_requirements: 13
complexity_score: 0.55
complexity_class: "MEDIUM"
domains_detected: [backend, security, frontend, testing, devops]
risks_identified: 7
dependencies_identified: 10
success_criteria_count: 10
extraction_mode: "standard"
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 9
test_artifacts_identified: 6
migration_items_identified: 15
operational_items_identified: 9
pipeline_diagnostics: {elapsed_seconds: 353.0, started_at: "2026-04-03T14:31:03.947966+00:00", finished_at: "2026-04-03T14:36:56.953469+00:00"}
---

# Requirements and Design Extraction — User Authentication Service

**Source:** test-tdd-user-auth.md (AUTH-001-TDD v1.2)
**Supplementary PRD:** test-prd-user-auth.md (AUTH-PRD-001 v1.0)

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
- **Priority:** Core (Milestone M1)
- **PRD Traceability:** FR-AUTH.1, Epic AUTH-E1

### FR-AUTH-002: User registration with validation

- **Description:** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
- **Components:** `AuthService`, `PasswordHasher`, `UserRepo`
- **Acceptance Criteria:**
  1. Valid registration returns 201 with `UserProfile` data.
  2. Duplicate email returns 409 Conflict.
  3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
  4. `PasswordHasher` stores bcrypt hash with cost factor 12.
- **API Surface:** POST `/auth/register`
- **Priority:** Core (Milestone M1)
- **PRD Traceability:** FR-AUTH.2, Epic AUTH-E1

### FR-AUTH-003: JWT token issuance and refresh

- **Description:** `TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
- **Components:** `TokenManager`, `JwtService`, Redis
- **Acceptance Criteria:**
  1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
  2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
  3. Expired refreshToken returns 401.
  4. Revoked refreshToken returns 401.
- **API Surface:** POST `/auth/refresh`
- **Priority:** Core (Milestone M2)
- **PRD Traceability:** FR-AUTH.3, Epic AUTH-E2

### FR-AUTH-004: User profile retrieval

- **Description:** `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
- **Components:** `AuthService`, `UserRepo`
- **Acceptance Criteria:**
  1. GET `/auth/me` with valid accessToken returns `UserProfile`.
  2. Expired or invalid token returns 401.
  3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.
- **API Surface:** GET `/auth/me`
- **Priority:** Standard (Milestone M2)
- **PRD Traceability:** FR-AUTH.4, Epic AUTH-E3

### FR-AUTH-005: Password reset flow

- **Description:** `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
- **Components:** `AuthService`, `PasswordHasher`, Email Service (SendGrid)
- **Acceptance Criteria:**
  1. POST `/auth/reset-request` with valid email sends reset token via email.
  2. POST `/auth/reset-confirm` with valid token updates the password hash.
  3. Reset tokens expire after 1 hour.
  4. Used reset tokens cannot be reused.
- **API Surface:** POST `/auth/reset-request`, POST `/auth/reset-confirm`
- **Priority:** Standard (Milestone M3)
- **PRD Traceability:** FR-AUTH.5, Epic AUTH-E3

---

## Non-Functional Requirements

### Performance

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-PERF-001 | API response time | All auth endpoints < 200ms at p95 | APM tracing on `AuthService` methods |
| NFR-PERF-002 | Concurrent authentication | Support 500 concurrent login requests | Load testing with k6 |

### Reliability

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-REL-001 | Service availability | 99.9% uptime over 30-day rolling windows | Uptime monitoring via health check endpoint |

### Security

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-SEC-001 | Password hashing | `PasswordHasher` must use bcrypt with cost factor 12 | Unit test asserting bcrypt cost parameter |
| NFR-SEC-002 | Token signing | `JwtService` must sign tokens with RS256 using 2048-bit RSA keys | Configuration validation test |

### Compliance (sourced from PRD AUTH-PRD-001, Section S17)

| ID | Requirement | Standard | Detail |
|----|-------------|----------|--------|
| NFR-COMP-001 | GDPR consent at registration | GDPR | Users must consent to data collection at registration. Consent recorded with timestamp. |
| NFR-COMP-002 | SOC2 audit logging | SOC2 Type II | All auth events logged with user ID, timestamp, IP, and outcome. 12-month retention. |
| NFR-COMP-003 | GDPR data minimization | GDPR | Only email, hashed password, and display name collected. No additional PII required. |

> **Note:** NFR-COMP-001 through NFR-COMP-003 are derived from the PRD's Legal & Compliance section. The TDD specifies 90-day audit log retention (Section 7.2), while the PRD requires 12-month retention for SOC2. **The PRD wins on business/compliance intent** — the TDD's 90-day retention must be reconciled to 12 months.

---

## Complexity Assessment

**Score:** 0.55 / 1.0
**Class:** MEDIUM

**Scoring Rationale:**

| Factor | Score | Rationale |
|--------|-------|-----------|
| Scope breadth | 0.5 | 5 functional requirements across auth, token management, and password reset — well-bounded |
| Architectural complexity | 0.5 | Standard layered architecture with facade pattern (`AuthService`). No microservice orchestration. Clear component boundaries. |
| Integration surface | 0.6 | 3 infrastructure dependencies (PostgreSQL, Redis, SendGrid), 6 API endpoints, frontend integration |
| Security sensitivity | 0.8 | Password hashing, JWT signing, token revocation, account lockout, XSS mitigations. Security-critical domain. |
| Data model complexity | 0.3 | 2 data entities (`UserProfile`, `AuthToken`) with straightforward schemas |
| Migration/rollout | 0.6 | 3-phase rollout with feature flags, rollback procedures, and rollback criteria |
| Operational burden | 0.5 | Runbooks, on-call rotation, capacity planning, monitoring dashboards |

**Overall:** Standard backend service with elevated security concerns. Well-defined scope with no ambiguous architectural decisions. Medium complexity driven by security requirements and phased rollout rather than structural complexity.

---

## Architectural Constraints

1. **Stateless API:** `AuthService` is a stateless REST API. All session state resides in JWT tokens (`JwtService`) and Redis refresh tokens (`TokenManager`). No server-side session storage.

2. **JWT with RS256:** `JwtService` must use RS256 with 2048-bit RSA keys. Keys rotated quarterly. 5-second clock skew tolerance.

3. **bcrypt cost factor 12:** `PasswordHasher` abstracts bcrypt with cost factor 12. Benchmarked at ~300ms per hash. The abstraction supports future algorithm migration (e.g., argon2id) without API changes.

4. **Dual-token lifecycle:** Access tokens (15-min TTL, JWT) and refresh tokens (7-day TTL, opaque, Redis-stored). `TokenManager` handles issuance, rotation, and revocation.

5. **Technology mandates:** PostgreSQL 15+, Redis 7+, Node.js 20 LTS. No alternatives permitted for v1.0.

6. **URL-prefix versioning:** Production API versioned via `/v1/auth/*`. Breaking changes require new major version.

7. **API Gateway boundary:** Rate limiting and CORS enforced at API Gateway, upstream of `AuthService`.

8. **Feature flag gating:** Rollout gated by `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` flags.

9. **Persona-driven design requirements (from PRD):**
   - **Alex (end user):** Registration in < 60 seconds. Seamless session persistence. No forced re-login on refresh.
   - **Jordan (admin):** Visibility into failed logins. Account lock/unlock. Queryable audit logs.
   - **Sam (API consumer):** Programmatic token refresh. Stable auth contracts. Clear error codes.

10. **NIST SP 800-63B compliance:** Password policy must comply with NIST guidelines (PRD constraint).

---

## Risk Inventory

### Risks from TDD (Section 20)

| # | ID | Risk | Probability | Impact | Mitigation | Contingency |
|---|-----|------|------------|--------|------------|-------------|
| 1 | R-001 | Token theft via XSS allows session hijacking | Medium | High | Store accessToken in memory only. HttpOnly cookies for refreshToken. 15-minute access token expiry. | Immediate token revocation via `TokenManager`. Force password reset for affected accounts. |
| 2 | R-002 | Brute-force attacks on login endpoint | High | Medium | Rate limiting (10 req/min per IP). Account lockout after 5 failures. bcrypt cost 12. | Block IPs at WAF. Enable CAPTCHA on `LoginPage` after 3 failures. |
| 3 | R-003 | Data loss during migration from legacy auth | Low | High | Parallel run during Phase 1-2. Idempotent upsert operations. Full DB backup before each phase. | Rollback to legacy. Restore from pre-migration backup. |

### Risks from PRD (Risk Analysis section)

| # | Risk | Probability | Impact | Mitigation |
|---|------|------------|--------|------------|
| 4 | Low registration adoption due to poor UX | Medium | High | Usability testing before launch; iterate based on funnel data. |
| 5 | Security breach from implementation flaws | Low | Critical | Dedicated security review; penetration testing before production. |
| 6 | Compliance failure from incomplete audit logging | Medium | High | Define log requirements early; validate against SOC2 controls in QA. |
| 7 | Email delivery failures blocking password reset | Low | Medium | Delivery monitoring and alerting; fallback support channel. |

---

## Dependency Inventory

### Infrastructure Dependencies

| # | Dependency | Type | Version | Purpose | Impact if Unavailable |
|---|-----------|------|---------|---------|----------------------|
| 1 | PostgreSQL | Database | 15+ | `UserProfile` persistence, password hashes, audit log | No user storage; service non-functional |
| 2 | Redis | Cache/Store | 7+ | Refresh token storage and revocation by `TokenManager` | Token refresh disabled; users must re-login |
| 3 | Node.js | Runtime | 20 LTS | `AuthService` runtime | Service cannot run |

### Library Dependencies

| # | Dependency | Purpose | Component |
|---|-----------|---------|-----------|
| 4 | bcryptjs | Password hashing | `PasswordHasher` |
| 5 | jsonwebtoken | JWT sign/verify | `JwtService` |

### External Service Dependencies

| # | Dependency | Type | Purpose | Impact if Unavailable |
|---|-----------|------|---------|----------------------|
| 6 | SendGrid API | External SaaS | Password reset emails | Password reset flow blocked (FR-AUTH-005) |

### Document Dependencies

| # | Dependency | Type | Relationship |
|---|-----------|------|-------------|
| 7 | AUTH-PRD-001 | Upstream | Product requirements this TDD implements |
| 8 | INFRA-DB-001 | Infrastructure | Database provisioning prerequisite |
| 9 | SEC-POLICY-001 | Policy | Governs `PasswordHasher` and `JwtService` configurations |

### Internal Dependencies (from PRD)

| # | Dependency | Type | Impact if Unavailable |
|---|-----------|------|-----------------------|
| 10 | Frontend routing framework | Internal | Auth pages (`LoginPage`, `RegisterPage`) cannot render |

---

## Success Criteria

### Technical Metrics (from TDD Section 4.1)

| # | Metric | Target | Measurement | Requirement Link |
|---|--------|--------|-------------|-----------------|
| 1 | Login response time (p95) | < 200ms | APM on `AuthService.login()` | NFR-PERF-001 |
| 2 | Registration success rate | > 99% | Ratio of successful registrations to attempts | FR-AUTH-002 |
| 3 | Token refresh latency (p95) | < 100ms | APM on `TokenManager.refresh()` | FR-AUTH-003 |
| 4 | Service availability | 99.9% uptime | Health check monitoring, 30-day windows | NFR-REL-001 |
| 5 | Password hash time | < 500ms | Benchmark `PasswordHasher.hash()` with bcrypt cost 12 | NFR-SEC-001 |

### Business Metrics (from TDD Section 4.2)

| # | Metric | Target | Measurement | Requirement Link |
|---|--------|--------|-------------|-----------------|
| 6 | User registration conversion | > 60% | Funnel analytics from `RegisterPage` to confirmed account | FR-AUTH-002 |
| 7 | Daily active authenticated users | > 1000 within 30 days of GA | `AuthToken` issuance counts | G-001 |

### Supplementary Business Metrics (from PRD Section S19)

| # | Metric | Target | Measurement | Business Rationale |
|---|--------|--------|-------------|--------------------|
| 8 | Average session duration | > 30 minutes | Token refresh event analytics | Longer sessions = engaged users |
| 9 | Failed login rate | < 5% of attempts | Auth event log analysis | High failure = UX or security issue |
| 10 | Password reset completion | > 80% | Funnel: reset requested -> new password set | Validates self-service recovery |

---

## Open Questions

### From TDD (Section 22)

| ID | Question | Owner | Target Date | Status |
|----|----------|-------|-------------|--------|
| OQ-001 | Should `AuthService` support API key authentication for service-to-service calls? | test-lead | 2026-04-15 | Open |
| OQ-002 | What is the maximum allowed `UserProfile` roles array length? | auth-team | 2026-04-01 | Open (overdue) |

### From PRD (Section: Open Questions)

| ID | Question | Owner | Status |
|----|----------|-------|--------|
| OQ-PRD-001 | Should password reset emails be sent synchronously or asynchronously? | Engineering | Open |
| OQ-PRD-002 | Maximum number of refresh tokens allowed per user across devices? | Product | Open |
| OQ-PRD-003 | Should we support "remember me" to extend session duration? | Product | Open |

> **Note:** PRD OQ-003 ("Account lockout policy after N consecutive failed login attempts?") is answered by the TDD: 5 failed attempts within 15 minutes triggers lockout (FR-AUTH-001, AC #4).

### JTBD Coverage Gaps

| JTBD | Corresponding FR | Gap |
|------|-----------------|-----|
| JTBD-1: Create account quickly | FR-AUTH-002 | Covered |
| JTBD-2: Return and pick up where I left off | FR-AUTH-003 | Covered |
| JTBD-3: Reset forgotten password | FR-AUTH-005 | Covered |
| JTBD-4: Authenticate programmatically and refresh tokens | FR-AUTH-003 | **Partial** — silent refresh is specified but no explicit API-consumer documentation or SDK guidance is provided |

### Extraction-Identified Gaps

| ID | Gap | Severity |
|----|-----|----------|
| GAP-001 | **Audit log retention conflict:** TDD specifies 90-day retention (Section 7.2); PRD requires 12-month retention for SOC2 (Section S17). PRD wins on compliance intent. | High |
| GAP-002 | **Logout endpoint missing:** PRD includes logout as in-scope (Epic AUTH-E1 user story). TDD does not specify a logout endpoint or token revocation-on-logout flow. | Medium |
| GAP-003 | **Admin audit log query API missing:** PRD persona Jordan requires queryable auth event logs (AUTH-E3 story). TDD has no admin-facing audit log query endpoint. | Medium |
| GAP-004 | **GDPR consent mechanism unspecified:** NFR-COMP-001 requires consent at registration. Neither the `UserProfile` schema nor the `/auth/register` request body includes a consent field. | Medium |
| GAP-005 | **Password reset endpoints not fully specified:** FR-AUTH-005 references `/auth/reset-request` and `/auth/reset-confirm` but Section 8 (API Specifications) does not include detailed request/response schemas for these endpoints. | Medium |

---

## Data Models and Interfaces

### Entity: `UserProfile`

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
| email | string | UNIQUE, NOT NULL, indexed | Yes | Normalized to lowercase by `AuthService` |
| displayName | string | NOT NULL, 2-100 chars | Yes | Display name shown in UI |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Yes | Account creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Yes | Last profile modification timestamp |
| lastLoginAt | string (ISO 8601) | NULLABLE | No | Updated by `AuthService` on each successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Yes | Authorization roles; enforcement is downstream |

**Relationships:** One-to-many with refresh tokens (via `TokenManager` in Redis). One-to-many with audit log entries.

### Entity: `AuthToken`

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
| accessToken | string (JWT) | NOT NULL | Yes | RS256-signed by `JwtService`; payload contains user id and roles |
| refreshToken | string | NOT NULL, unique | Yes | Opaque token; stored hashed in Redis with 7-day TTL |
| expiresIn | number | NOT NULL | Yes | Always 900 (15 minutes) |
| tokenType | string | NOT NULL | Yes | Always "Bearer" (OAuth2 compatibility) |

### Data Storage Strategy

| Store | Technology | Purpose | Retention |
|-------|-----------|---------|-----------|
| User records | PostgreSQL 15 | `UserProfile` persistence, password hashes | Indefinite |
| Refresh tokens | Redis 7 | Token storage and revocation | 7-day TTL |
| Audit log | PostgreSQL 15 | Login attempts, password resets | 90 days (TDD) / **12 months required (PRD/SOC2)** |

### Data Flow: Login

1. Client submits email/password to POST `/auth/login`
2. `AuthService` retrieves user record from PostgreSQL via `UserRepo`
3. `PasswordHasher.verify()` compares plaintext against stored bcrypt hash
4. On success, `TokenManager.issueTokens()` generates access/refresh pair via `JwtService`
5. Refresh token stored (hashed) in Redis with 7-day TTL
6. `AuthToken` response returned to client
7. `AuthService` updates `lastLoginAt` on `UserProfile`
8. Audit log entry written to PostgreSQL

---

## API Specifications

### Endpoint Inventory

| # | Method | Path | Auth | Rate Limit | Description | Req Link |
|---|--------|------|------|------------|-------------|----------|
| 1 | POST | `/auth/login` | No | 10 req/min per IP | Authenticate user, return `AuthToken` | FR-AUTH-001 |
| 2 | POST | `/auth/register` | No | 5 req/min per IP | Create `UserProfile`, return profile data | FR-AUTH-002 |
| 3 | GET | `/auth/me` | Yes (Bearer) | 60 req/min per user | Return authenticated user's `UserProfile` | FR-AUTH-004 |
| 4 | POST | `/auth/refresh` | No (refresh token in body) | 30 req/min per user | Exchange refresh token for new `AuthToken` | FR-AUTH-003 |
| 5 | POST | `/auth/reset-request` | No | Not specified | Send password reset email | FR-AUTH-005 |
| 6 | POST | `/auth/reset-confirm` | No | Not specified | Validate reset token, update password | FR-AUTH-005 |

### Endpoint Detail: POST `/auth/login`

**Request Body:**
```json
{ "email": "string", "password": "string" }
```

**Success Response (200):** `AuthToken` object (accessToken, refreshToken, expiresIn, tokenType)

**Error Responses:**
| Code | Condition | Error Code |
|------|-----------|------------|
| 401 | Invalid email or password | AUTH_INVALID_CREDENTIALS |
| 423 | Account locked (5 failed attempts in 15 min) | — |
| 429 | Rate limit exceeded | — |

### Endpoint Detail: POST `/auth/register`

**Request Body:**
```json
{ "email": "string", "password": "string", "displayName": "string" }
```

**Success Response (201):** `UserProfile` object

**Error Responses:**
| Code | Condition |
|------|-----------|
| 400 | Validation errors (weak password, invalid email) |
| 409 | Email already registered |

### Endpoint Detail: GET `/auth/me`

**Request Headers:** `Authorization: Bearer <accessToken>`

**Success Response (200):** `UserProfile` object

**Error Responses:**
| Code | Condition |
|------|-----------|
| 401 | Missing, expired, or invalid accessToken |

### Endpoint Detail: POST `/auth/refresh`

**Request Body:**
```json
{ "refreshToken": "string" }
```

**Success Response (200):** New `AuthToken` object (old refresh token revoked)

**Error Responses:**
| Code | Condition |
|------|-----------|
| 401 | Expired or revoked refresh token |

### Endpoint Detail: POST `/auth/reset-request` (partially specified)

**Request Body:** `{ "email": "string" }`
**Behavior:** Sends reset token via email. Same response regardless of registration status (prevents enumeration).
**Note:** Full request/response schemas not provided in TDD Section 8 (see GAP-005).

### Endpoint Detail: POST `/auth/reset-confirm` (partially specified)

**Request Body:** Token + new password (schema not fully specified).
**Behavior:** Validates token (1-hour TTL, single-use), updates password hash.
**Note:** Full request/response schemas not provided in TDD Section 8 (see GAP-005).

### Error Response Format

All errors follow a consistent structure:
```json
{
  "error": {
    "code": "string (e.g., AUTH_INVALID_CREDENTIALS)",
    "message": "string (human-readable)",
    "status": "number (HTTP status code)"
  }
}
```

### Versioning

- URL-prefix versioning: `/v1/auth/*` in production
- Breaking changes require new major version
- Non-breaking additions (new optional fields) permitted within current version

---

## Component Inventory

### Backend Components

| # | Component | Type | Responsibility | Dependencies |
|---|-----------|------|---------------|-------------|
| 1 | `AuthService` | Service (Facade) | Orchestrates all auth flows: login, registration, profile, password reset | `PasswordHasher`, `TokenManager`, `UserRepo` |
| 2 | `TokenManager` | Service | JWT access/refresh token lifecycle: issuance, refresh, revocation | `JwtService`, Redis |
| 3 | `JwtService` | Service | JWT sign and verify operations using RS256/2048-bit RSA | jsonwebtoken library |
| 4 | `PasswordHasher` | Service | bcrypt hash and verify abstraction with configurable cost factor | bcryptjs library |
| 5 | `UserRepo` | Repository | `UserProfile` CRUD operations against PostgreSQL | PostgreSQL |

### Frontend Components

| # | Component | Type | Props | Description |
|---|-----------|------|-------|-------------|
| 6 | `LoginPage` | Page | onSuccess: () => void, redirectUrl?: string | Email/password login form; calls POST `/auth/login`; stores `AuthToken` via `AuthProvider` |
| 7 | `RegisterPage` | Page | onSuccess: () => void, termsUrl: string | Registration form with client-side password validation; calls POST `/auth/register` |
| 8 | `AuthProvider` | Context Provider | children: ReactNode | Manages `AuthToken` state, handles silent refresh, intercepts 401s, exposes `UserProfile` and auth methods |
| 9 | ProfilePage | Page | (not specified) | Displays `UserProfile` data; calls GET `/auth/me` |

### Route Structure

| Route | Component | Auth Required |
|-------|-----------|---------------|
| `/login` | `LoginPage` | No |
| `/register` | `RegisterPage` | No |
| `/profile` | ProfilePage | Yes |

### Component Hierarchy

```
App
├── AuthProvider
│   ├── PublicRoutes
│   │   ├── LoginPage
│   │   └── RegisterPage
│   └── ProtectedRoutes
│       └── ProfilePage
```

`AuthProvider` wraps all routes, intercepts 401 responses, triggers token refresh through `TokenManager`, and redirects unauthenticated users to `LoginPage`.

---

## Testing Strategy

### Test Pyramid

| Level | Coverage Target | Tools | Focus Areas | Ownership |
|-------|----------------|-------|-------------|-----------|
| Unit | 80% | Jest, ts-jest | `AuthService` methods, `PasswordHasher` hashing/verification, `JwtService` sign/verify, `TokenManager` lifecycle, `UserProfile` validation | auth-team |
| Integration | 15% | Supertest, testcontainers | API endpoint request/response, database operations, Redis token storage, `AuthService` → `PasswordHasher` → DB flow | auth-team |
| E2E | 5% | Playwright | `LoginPage` login, `RegisterPage` registration, `AuthProvider` token refresh, full user journey | auth-team + QA |

### Test Cases — Unit

| # | Test Case | Component | Validates |
|---|-----------|-----------|-----------|
| 1 | Login with valid credentials returns `AuthToken` | `AuthService` | FR-AUTH-001: `AuthService.login()` calls `PasswordHasher.verify()`, then `TokenManager.issueTokens()` |
| 2 | Login with invalid credentials returns error | `AuthService` | FR-AUTH-001: Returns 401 when `PasswordHasher.verify()` returns false |
| 3 | Token refresh with valid refresh token | `TokenManager` | FR-AUTH-003: Validates refresh token, revokes old, issues new `AuthToken` pair |

### Test Cases — Integration

| # | Test Case | Scope | Validates |
|---|-----------|-------|-----------|
| 4 | Registration persists `UserProfile` to database | `AuthService` + PostgreSQL | FR-AUTH-002: Full flow from API request through `PasswordHasher` to database insert |
| 5 | Expired refresh token rejected by `TokenManager` | `TokenManager` + Redis | FR-AUTH-003: Redis TTL expiration correctly invalidates refresh tokens |

### Test Cases — E2E

| # | Test Case | Flow | Validates |
|---|-----------|------|-----------|
| 6 | User registers and logs in | `RegisterPage` → `LoginPage` → ProfilePage | FR-AUTH-001, FR-AUTH-002: Complete user journey through `AuthProvider` |

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
| Phase 1: Internal Alpha | Deploy `AuthService` to staging. auth-team and QA test all endpoints. `LoginPage` and `RegisterPage` behind `AUTH_NEW_LOGIN` flag. | 1 week | Staging environment, feature flag infrastructure | FR-AUTH-001 through FR-AUTH-005 pass manual testing. Zero P0/P1 bugs. | Disable `AUTH_NEW_LOGIN` flag |
| Phase 2: Beta (10%) | Enable `AUTH_NEW_LOGIN` for 10% of traffic. Monitor latency, error rates, Redis usage. | 2 weeks | Phase 1 exit criteria met | p95 latency < 200ms. Error rate < 0.1%. No Redis connection failures. | Reduce traffic to 0%, disable flag |
| Phase 3: GA (100%) | Remove `AUTH_NEW_LOGIN` flag. All users on new `AuthService`. Legacy auth deprecated. `AUTH_TOKEN_REFRESH` enables refresh flow. | 1 week | Phase 2 exit criteria met | 99.9% uptime over 7 days. All dashboards green. | Rollback procedure below |

### Feature Flags

| Flag | Purpose | Default | Cleanup Target |
|------|---------|---------|---------------|
| `AUTH_NEW_LOGIN` | Gates access to new `LoginPage` and `AuthService` login endpoint | OFF | Remove after Phase 3 GA |
| `AUTH_TOKEN_REFRESH` | Enables refresh token flow in `TokenManager`; when OFF, only access tokens issued | OFF | Remove Phase 3 + 2 weeks |

### Rollback Procedure (sequential — order implies dependency)

1. Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth
2. Verify legacy login flow is operational via smoke tests
3. Investigate `AuthService` failure root cause using structured logs and traces
4. If data corruption detected in `UserProfile` table, restore from last known-good backup
5. Notify auth-team and platform-team via incident channel
6. Post-mortem within 48 hours of rollback

### Rollback Criteria (automatic trigger)

| # | Condition | Threshold |
|---|-----------|-----------|
| 1 | p95 latency | Exceeds 1000ms for > 5 minutes |
| 2 | Error rate | Exceeds 5% for > 2 minutes |
| 3 | Redis connection failures | Exceeds 10/minute |
| 4 | Data integrity | Any data loss or corruption in `UserProfile` records |

---

## Operational Readiness

### Runbook Scenarios

#### Scenario 1: `AuthService` Down

| Aspect | Detail |
|--------|--------|
| **Symptoms** | 5xx errors on all `/auth/*` endpoints; `LoginPage` and `RegisterPage` show error state |
| **Diagnosis** | Check `AuthService` pod health in Kubernetes. Verify PostgreSQL connectivity. Check `PasswordHasher` and `TokenManager` initialization logs. |
| **Resolution** | Restart `AuthService` pods. If PostgreSQL unreachable, failover to read replica. If Redis down, `TokenManager` rejects refresh — users must re-login. |
| **Escalation** | Page auth-team on-call. If unresolved in 15 minutes, escalate to platform-team. |
| **Prevention** | Health checks, pod auto-restart, connection pool monitoring |

#### Scenario 2: Token Refresh Failures

| Aspect | Detail |
|--------|--------|
| **Symptoms** | Users logged out unexpectedly; `AuthProvider` redirect loop to `LoginPage`; `auth_token_refresh_total` error counter spikes |
| **Diagnosis** | Check Redis connectivity from `TokenManager`. Verify `JwtService` signing key accessible. Check `AUTH_TOKEN_REFRESH` flag state. |
| **Resolution** | If Redis degraded, scale cluster. If signing key unavailable, re-mount secrets volume. If flag OFF, enable `AUTH_TOKEN_REFRESH`. |
| **Escalation** | Page auth-team on-call. Redis cluster issues → escalate to platform-team. |
| **Prevention** | Redis cluster monitoring, key rotation alerts, feature flag state dashboards |

### On-Call Expectations

| Aspect | Expectation |
|--------|-------------|
| Response time | Acknowledge P1 alerts within 15 minutes |
| Coverage | auth-team 24/7 rotation during first 2 weeks post-GA |
| Tooling | Kubernetes dashboards, Grafana, Redis CLI, PostgreSQL admin |
| Escalation path | auth-team on-call → test-lead → eng-manager → platform-team |

### Capacity Planning

| Resource | Current | Expected Load | Scaling Trigger |
|----------|---------|---------------|-----------------|
| `AuthService` pods | 3 replicas | 500 concurrent users | HPA scales to 10 at CPU > 70% |
| PostgreSQL connections | 100 pool size | 50 avg concurrent queries | Increase to 200 if wait time > 50ms |
| Redis memory | 1 GB | ~100K refresh tokens (~50 MB) | Scale to 2 GB if > 70% utilized |

### Observability

**Metrics (Prometheus):**
- `auth_login_total` (counter) — login attempts by outcome
- `auth_login_duration_seconds` (histogram) — login latency
- `auth_token_refresh_total` (counter) — refresh attempts by outcome
- `auth_registration_total` (counter) — registration attempts

**Distributed Tracing:** OpenTelemetry spans covering `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`

**Structured Logging:** All auth events (login success/failure, registration, token refresh, password reset)

**Alerts:**
| Alert | Condition |
|-------|-----------|
| High login failure rate | > 20% over 5 minutes |
| High latency | p95 > 500ms |
| Redis connection failures | Any `TokenManager` Redis errors |
