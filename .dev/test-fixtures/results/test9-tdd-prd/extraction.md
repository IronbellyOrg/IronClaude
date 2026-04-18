---
spec_source: "test-tdd-user-auth.md"
generated: "2026-04-15T00:00:00Z"
generator: "superclaude-extraction-agent"
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.65
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, testing, devops]
risks_identified: 7
dependencies_identified: 7
success_criteria_count: 10
extraction_mode: standard
data_models_identified: 3
api_surfaces_identified: 6
components_identified: 9
test_artifacts_identified: 6
migration_items_identified: 7
operational_items_identified: 4
pipeline_diagnostics: {elapsed_seconds: 241.0, started_at: "2026-04-15T23:22:36.668627+00:00", finished_at: "2026-04-15T23:26:37.697474+00:00"}
---

## Functional Requirements

### FR-AUTH-001: Login with email and password
- **Description:** `AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`.
- **Source:** TDD Section 5.1
- **Components:** `AuthService`, `PasswordHasher`, `TokenManager`
- **Acceptance Criteria:**
  1. Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken.
  2. Invalid credentials return 401 with error message.
  3. Non-existent email returns 401 (no user enumeration).
  4. Account locked after 5 failed attempts within 15 minutes.
- **PRD Trace:** FR-AUTH.1, Epic AUTH-E1

### FR-AUTH-002: User registration with validation
- **Description:** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
- **Source:** TDD Section 5.1
- **Components:** `AuthService`, `PasswordHasher`, `UserRepo`
- **Acceptance Criteria:**
  1. Valid registration returns 201 with `UserProfile` data.
  2. Duplicate email returns 409 Conflict.
  3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
  4. `PasswordHasher` stores bcrypt hash with cost factor 12.
- **PRD Trace:** FR-AUTH.2, Epic AUTH-E1

### FR-AUTH-003: JWT token issuance and refresh
- **Description:** `TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
- **Source:** TDD Section 5.1
- **Components:** `TokenManager`, `JwtService`, Redis
- **Acceptance Criteria:**
  1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
  2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
  3. Expired refreshToken returns 401.
  4. Revoked refreshToken returns 401.
- **PRD Trace:** FR-AUTH.3, Epic AUTH-E2

### FR-AUTH-004: User profile retrieval
- **Description:** `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
- **Source:** TDD Section 5.1
- **Components:** `AuthService`, `UserRepo`
- **Acceptance Criteria:**
  1. GET `/auth/me` with valid accessToken returns `UserProfile`.
  2. Expired or invalid token returns 401.
  3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.
- **PRD Trace:** FR-AUTH.4, Epic AUTH-E3

### FR-AUTH-005: Password reset flow
- **Description:** `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
- **Source:** TDD Section 5.1
- **Components:** `AuthService`, `PasswordHasher`, Email Service
- **Acceptance Criteria:**
  1. POST `/auth/reset-request` with valid email sends reset token via email.
  2. POST `/auth/reset-confirm` with valid token updates the password hash.
  3. Reset tokens expire after 1 hour.
  4. Used reset tokens cannot be reused.
- **PRD Trace:** FR-AUTH.5, Epic AUTH-E3

## Non-Functional Requirements

### NFR-PERF-001: API response time
- **Category:** Performance
- **Requirement:** All auth endpoints must respond in < 200ms at p95.
- **Measurement:** APM tracing on `AuthService` methods.
- **Source:** TDD Section 5.2

### NFR-PERF-002: Concurrent authentication
- **Category:** Performance
- **Requirement:** Support 500 concurrent login requests.
- **Measurement:** Load testing with k6.
- **Source:** TDD Section 5.2

### NFR-REL-001: Service availability
- **Category:** Reliability
- **Requirement:** 99.9% uptime measured over 30-day rolling windows.
- **Measurement:** Uptime monitoring via health check endpoint.
- **Source:** TDD Section 5.2

### NFR-SEC-001: Password hashing
- **Category:** Security
- **Requirement:** `PasswordHasher` must use bcrypt with cost factor 12.
- **Measurement:** Unit test asserting bcrypt cost parameter.
- **Source:** TDD Section 5.2

### NFR-SEC-002: Token signing
- **Category:** Security
- **Requirement:** `JwtService` must sign tokens with RS256 using 2048-bit RSA keys.
- **Measurement:** Configuration validation test.
- **Source:** TDD Section 5.2

### NFR-COMP-001: GDPR consent at registration
- **Category:** Compliance
- **Requirement:** Users must consent to data collection at registration. Consent recorded with timestamp.
- **Standard:** GDPR
- **Source:** PRD Section Legal & Compliance. Not present in TDD -- surfaced from PRD.

### NFR-COMP-002: SOC2 audit logging
- **Category:** Compliance
- **Requirement:** All auth events logged with user ID, timestamp, IP, and outcome. 12-month retention.
- **Standard:** SOC2 Type II
- **Source:** PRD Section Legal & Compliance. **Conflict:** TDD Section 7.2 specifies 90-day audit log retention; PRD specifies 12-month. PRD wins on business intent -- retention must be 12 months.

### NFR-COMP-003: NIST password storage
- **Category:** Compliance
- **Requirement:** Password storage must comply with NIST SP 800-63B guidelines (one-way adaptive hashing, raw passwords never persisted or logged).
- **Standard:** NIST SP 800-63B
- **Source:** PRD Section Legal & Compliance. TDD covers bcrypt but does not explicitly cite NIST compliance.

### NFR-COMP-004: GDPR data minimization
- **Category:** Compliance
- **Requirement:** Only email, hashed password, and display name collected. No additional PII required.
- **Standard:** GDPR
- **Source:** PRD Section Legal & Compliance. Not present in TDD -- surfaced from PRD.

## Complexity Assessment

**Score:** 0.65 | **Class:** MEDIUM

**Rationale:**
| Factor | Score | Weight | Justification |
|---|---|---|---|
| Component count | 0.6 | 20% | 9 components across backend and frontend; clear separation of concerns |
| Data store diversity | 0.7 | 15% | PostgreSQL + Redis + external email service |
| Security criticality | 0.8 | 20% | Password hashing, JWT signing, token revocation, brute-force protection |
| Integration surface | 0.5 | 15% | 6 API endpoints, 1 external service (SendGrid), well-defined boundaries |
| Compliance requirements | 0.7 | 15% | GDPR, SOC2, NIST -- adds audit logging and consent constraints |
| Rollout complexity | 0.6 | 15% | 3-phase rollout with feature flags and rollback procedures |

The system is well-scoped (single service domain) with clear component boundaries, but security criticality and compliance obligations elevate it above LOW. It does not reach HIGH because there are no distributed system coordination challenges, no complex state machines, and the data model is straightforward.

## Architectural Constraints

1. **Stateless REST API.** `AuthService` is stateless; all session state is carried in JWT tokens. No server-side session store.
2. **JWT with RS256.** `JwtService` must use RS256 with 2048-bit RSA keys. Keys rotated quarterly (TDD Section 13).
3. **bcrypt cost factor 12.** `PasswordHasher` must use cost factor 12. Benchmarked at ~300ms per hash (TDD Section 17).
4. **Connection pooling.** `AuthService` to PostgreSQL via pg-pool. Pool size 100, scalable to 200 (TDD Section 25.3).
5. **Refresh tokens in Redis.** `TokenManager` stores refresh tokens as hashed values in Redis with 7-day TTL (TDD Section 7.2).
6. **API versioned via URL prefix.** Production URL prefix `/v1/auth/*`. Breaking changes require new major version (TDD Section 8.4).
7. **TLS 1.3 enforced.** All endpoints enforce TLS 1.3 (TDD Section 13).
8. **CORS restricted.** CORS restricted to known frontend origins (TDD Section 13).
9. **No social/OAuth login in v1.0.** Deferred to v1.1 (TDD Section 3.2, NG-001).
10. **No MFA in v1.0.** Planned for v1.2 (TDD Section 3.2, NG-002).
11. **No RBAC enforcement.** `UserProfile.roles` field exists but enforcement is out of scope (TDD Section 3.2, NG-003).
12. **Email/password only in v1.0.** PRD constraint -- no social login providers.
13. **Persona-driven design (PRD):** Three personas drive design requirements:
    - **Alex (End User):** Quick registration (<60s), fast login, seamless session persistence, self-service recovery.
    - **Jordan (Platform Admin):** Visibility into failed logins, account lock/unlock, compliance audit trail.
    - **Sam (API Consumer):** Programmatic token management, stable auth contracts, clear error codes.

## Risk Inventory

1. **R-001 — Token theft via XSS** | Severity: HIGH | Probability: Medium
   - **Mitigation:** Store accessToken in memory only (not localStorage). HttpOnly cookies for refreshToken. `JwtService` uses 15-minute expiry.
   - **Contingency:** Immediate token revocation via `TokenManager`. Force password reset for affected accounts.

2. **R-002 — Brute-force attacks on login** | Severity: MEDIUM | Probability: High
   - **Mitigation:** Rate limiting at API Gateway (10 req/min per IP). Account lockout after 5 failed attempts. bcrypt cost factor 12.
   - **Contingency:** Block offending IPs at WAF. Enable CAPTCHA on `LoginPage` after 3 failures.

3. **R-003 — Data loss during migration** | Severity: HIGH | Probability: Low
   - **Mitigation:** Parallel operation during Phase 1-2. Idempotent upsert operations. Full backup before each phase.
   - **Contingency:** Rollback to legacy auth. Restore from pre-migration backup.

4. **R-004 — Low registration adoption** | Severity: HIGH | Probability: Medium | Source: PRD
   - **Mitigation:** Usability testing before launch; iterate based on funnel data.

5. **R-005 — Security breach from implementation flaws** | Severity: CRITICAL | Probability: Low | Source: PRD
   - **Mitigation:** Dedicated security review; penetration testing before production.

6. **R-006 — Compliance failure from incomplete audit logging** | Severity: HIGH | Probability: Medium | Source: PRD
   - **Mitigation:** Define log requirements early; validate against SOC2 controls in QA.

7. **R-007 — Email delivery failures blocking password reset** | Severity: MEDIUM | Probability: Low | Source: PRD
   - **Mitigation:** Delivery monitoring and alerting; fallback support channel.

## Dependency Inventory

| ID | Dependency | Type | Version | Purpose | Impact if Unavailable |
|---|---|---|---|---|---|
| DEP-001 | PostgreSQL | Infrastructure | 15+ | `UserProfile` persistence, password hashes, audit log | No persistent user storage |
| DEP-002 | Redis | Infrastructure | 7+ | Refresh token storage and revocation by `TokenManager` | Token refresh disabled; users must re-login |
| DEP-003 | Node.js | Runtime | 20 LTS | `AuthService` runtime | Service cannot start |
| DEP-004 | bcryptjs | Library | — | Password hashing in `PasswordHasher` | Registration and login broken |
| DEP-005 | jsonwebtoken | Library | — | JWT sign/verify in `JwtService` | Token issuance broken |
| DEP-006 | SendGrid | External Service | API | Password reset email delivery | Password reset flow blocked (FR-AUTH-005) |
| DEP-007 | Frontend routing framework | Internal | — | Client-side routing for `LoginPage`, `RegisterPage`, `AuthProvider` | Auth pages cannot render |

## Success Criteria

| ID | Metric | Target | Measurement | Source |
|---|---|---|---|---|
| SC-001 | Login response time (p95) | < 200ms | APM on `AuthService.login()` | TDD 4.1, PRD |
| SC-002 | Registration success rate | > 99% | Ratio of successful registrations to attempts | TDD 4.1 |
| SC-003 | Token refresh latency (p95) | < 100ms | APM on `TokenManager.refresh()` | TDD 4.1 |
| SC-004 | Service availability | 99.9% uptime | Health check monitoring, 30-day windows | TDD 4.1 |
| SC-005 | Password hash time | < 500ms | Benchmark `PasswordHasher.hash()` with bcrypt cost 12 | TDD 4.1 |
| SC-006 | Registration conversion | > 60% | Funnel analytics from `RegisterPage` to confirmed account | TDD 4.2, PRD |
| SC-007 | Daily active authenticated users | > 1000 within 30 days of GA | `AuthToken` issuance counts | TDD 4.2 |
| SC-008 | Average session duration | > 30 minutes | Token refresh event analytics | PRD |
| SC-009 | Failed login rate | < 5% of attempts | Auth event log analysis | PRD |
| SC-010 | Password reset completion | > 80% | Funnel: reset requested -> new password set | PRD |

## Open Questions

### From TDD
| ID | Question | Owner | Target Date | Status |
|---|---|---|---|---|
| OQ-001 | Should `AuthService` support API key authentication for service-to-service calls? | test-lead | 2026-04-15 | Open |
| OQ-002 | What is the maximum allowed `UserProfile` roles array length? | auth-team | 2026-04-01 | Open |

### From PRD
| ID | Question | Owner | Status |
|---|---|---|---|
| OQ-003 | Should password reset emails be sent synchronously or asynchronously? | Engineering | Open |
| OQ-004 | Maximum number of refresh tokens allowed per user across devices? | Product | Open |
| OQ-005 | Should the system support "remember me" to extend session duration? | Product | Open |

### JTBD Coverage Gaps (PRD)
| ID | Gap | Detail |
|---|---|---|
| OQ-006 | Logout functionality missing from TDD | PRD Epic AUTH-E1 includes a logout user story ("As Alex, I want to log out so I can secure my session on a shared device"). No corresponding FR, API endpoint, or component exists in the TDD. |
| OQ-007 | Admin audit log viewing missing from TDD | PRD Epic AUTH-E3 includes an admin user story ("As Jordan, I want to view authentication event logs"). No corresponding FR or API endpoint for log querying exists in the TDD. The TDD mentions audit log storage (Section 7.2) but no query interface. |

### Conflict Resolution
| ID | Conflict | Resolution |
|---|---|---|
| OQ-008 | Audit log retention: TDD says 90 days (Section 7.2), PRD says 12 months (Legal & Compliance) | PRD wins on business intent per extraction rules. 12-month retention required. TDD Section 7.2 must be updated. |

## Data Models and Interfaces

### DM-001: UserProfile
- **Source:** TDD Section 7.1
- **Storage:** PostgreSQL 15 (DEP-001)
- **Retention:** Indefinite

| Field | Type | Constraints | Required | Description |
|---|---|---|---|---|
| id | string (UUID v4) | PRIMARY KEY, NOT NULL | Yes | Unique user identifier generated by `AuthService` |
| email | string | UNIQUE, NOT NULL, indexed, lowercase normalized | Yes | User email |
| displayName | string | NOT NULL, 2-100 chars | Yes | Display name shown in UI |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Yes | Account creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Yes | Last profile modification timestamp |
| lastLoginAt | string (ISO 8601) | NULLABLE | No | Updated on each successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Yes | Authorization roles; enforcement downstream |

**Relationships:** Referenced by `AuthToken` (via JWT payload containing user id and roles). Persisted by `UserRepo` in PostgreSQL.

### DM-002: AuthToken
- **Source:** TDD Section 7.1
- **Storage:** accessToken is ephemeral (in-memory); refreshToken stored in Redis (DEP-002) with 7-day TTL
- **Retention:** accessToken 15 minutes; refreshToken 7 days

| Field | Type | Constraints | Required | Description |
|---|---|---|---|---|
| accessToken | string (JWT) | NOT NULL | Yes | Signed by `JwtService` using RS256; contains user id and roles |
| refreshToken | string | NOT NULL, unique | Yes | Opaque token managed by `TokenManager`; stored hashed in Redis |
| expiresIn | number | NOT NULL, always 900 | Yes | Seconds until accessToken expiration |
| tokenType | string | NOT NULL, always "Bearer" | Yes | OAuth2 compatibility field |

**Relationships:** accessToken payload references `UserProfile.id` and `UserProfile.roles`. refreshToken managed by `TokenManager` with Redis backend.

### DM-003: AuditLog
- **Source:** TDD Section 7.2, PRD Legal & Compliance
- **Storage:** PostgreSQL 15 (DEP-001)
- **Retention:** 12 months (per PRD NFR-COMP-002; TDD states 90 days but PRD overrides)
- **Note:** No interface definition provided in TDD. Fields inferred from PRD and TDD observability requirements.

| Field | Type | Constraints | Required | Description |
|---|---|---|---|---|
| userId | string | NOT NULL | Yes | User associated with the event |
| eventType | string | NOT NULL | Yes | e.g., login_success, login_failure, registration, password_reset |
| timestamp | string (ISO 8601) | NOT NULL | Yes | Event timestamp |
| ipAddress | string | NOT NULL | Yes | Client IP address (per PRD) |
| outcome | string | NOT NULL | Yes | Success or failure with detail |

**Data Flow:** `AuthService` emits structured logs for all authentication events -> persisted to PostgreSQL audit_log table.

## API Specifications

### API-001: POST /auth/login
- **Auth Required:** No
- **Rate Limit:** 10 req/min per IP
- **Description:** Authenticate user via `AuthService`, return `AuthToken`.
- **Request Body:**
  - `email` (string, required): User email
  - `password` (string, required): User password
- **Response (200):** `AuthToken` object (accessToken, refreshToken, expiresIn, tokenType)
- **Errors:** 401 (invalid credentials), 423 (account locked after 5 failures), 429 (rate limit)
- **FR Trace:** FR-AUTH-001

### API-002: POST /auth/register
- **Auth Required:** No
- **Rate Limit:** 5 req/min per IP
- **Description:** Create new user account via `AuthService`, return `UserProfile`.
- **Request Body:**
  - `email` (string, required): Unique email address
  - `password` (string, required): Min 8 chars, uppercase, number required
  - `displayName` (string, required): 2-100 characters
- **Response (201):** `UserProfile` object
- **Errors:** 400 (validation: weak password, invalid email), 409 (duplicate email)
- **FR Trace:** FR-AUTH-002

### API-003: GET /auth/me
- **Auth Required:** Yes (Bearer token in Authorization header)
- **Rate Limit:** 60 req/min per user
- **Description:** Return authenticated user's `UserProfile`.
- **Request Headers:** `Authorization: Bearer <accessToken>`
- **Response (200):** `UserProfile` object (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles)
- **Errors:** 401 (missing, expired, or invalid accessToken)
- **FR Trace:** FR-AUTH-004

### API-004: POST /auth/refresh
- **Auth Required:** No (refresh token in body)
- **Rate Limit:** 30 req/min per user
- **Description:** Exchange valid refresh token for new `AuthToken` pair via `TokenManager`. Old refresh token revoked.
- **Request Body:**
  - `refreshToken` (string, required): Previously issued refresh token
- **Response (200):** New `AuthToken` object
- **Errors:** 401 (expired or revoked refresh token)
- **FR Trace:** FR-AUTH-003

### API-005: POST /auth/reset-request
- **Auth Required:** No
- **Rate Limit:** Not specified (gap)
- **Description:** Initiate password reset by sending email with reset token.
- **Request Body:**
  - `email` (string, required): User email address
- **Response:** Success response regardless of email registration status (prevents enumeration)
- **Note:** Endpoint implied by FR-AUTH-005 acceptance criteria but not detailed in TDD Section 8.2. Full request/response schema is a gap.
- **FR Trace:** FR-AUTH-005

### API-006: POST /auth/reset-confirm
- **Auth Required:** No
- **Rate Limit:** Not specified (gap)
- **Description:** Complete password reset by validating token and updating password hash.
- **Request Body:**
  - `token` (string, required): Reset token from email (1-hour TTL, single-use)
  - `password` (string, required): New password meeting strength requirements
- **Response:** Success confirmation
- **Note:** Endpoint implied by FR-AUTH-005 acceptance criteria but not detailed in TDD Section 8.2. Full request/response schema is a gap.
- **FR Trace:** FR-AUTH-005

**Error Response Format (all endpoints):**
```json
{
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS",
    "message": "The provided email or password is incorrect.",
    "status": 401
  }
}
```

**Versioning:** URL prefix `/v1/auth/*` in production. Breaking changes require new major version. Non-breaking additions permitted within current version.

## Component Inventory

### COMP-001: AuthService
- **Type:** Backend Service (orchestrator)
- **Location:** Backend
- **Description:** Primary orchestrator for all auth flows. Receives requests from API Gateway, delegates to specialized components.
- **Dependencies:** COMP-002 (TokenManager), COMP-004 (PasswordHasher), COMP-005 (UserRepo)

### COMP-002: TokenManager
- **Type:** Backend Module
- **Location:** Backend
- **Description:** Manages JWT access/refresh token lifecycle. Issues tokens via `JwtService`, stores refresh tokens in Redis, handles revocation.
- **Dependencies:** COMP-003 (JwtService), DEP-002 (Redis)

### COMP-003: JwtService
- **Type:** Backend Module
- **Location:** Backend
- **Description:** Signs and verifies JWT tokens using RS256 with 2048-bit RSA keys. 5-second clock skew tolerance.
- **Dependencies:** DEP-005 (jsonwebtoken)

### COMP-004: PasswordHasher
- **Type:** Backend Module
- **Location:** Backend
- **Description:** Abstraction over bcrypt with configurable cost factor (default 12). Designed for future algorithm migration.
- **Dependencies:** DEP-004 (bcryptjs)

### COMP-005: UserRepo
- **Type:** Backend Data Access
- **Location:** Backend
- **Description:** Data access layer for `UserProfile` persistence in PostgreSQL. Connection pooling via pg-pool.
- **Dependencies:** DEP-001 (PostgreSQL)

### COMP-006: LoginPage
- **Type:** Frontend Page Component
- **Location:** Route `/login`
- **Auth Required:** No
- **Props:** `onSuccess: () => void`, `redirectUrl?: string`
- **Description:** Email/password login form. Handles submission to `AuthService` login endpoint. Stores `AuthToken` via `AuthProvider`.
- **Dependencies:** COMP-009 (AuthProvider), API-001

### COMP-007: RegisterPage
- **Type:** Frontend Page Component
- **Location:** Route `/register`
- **Auth Required:** No
- **Props:** `onSuccess: () => void`, `termsUrl: string`
- **Description:** Registration form with email, password, displayName fields. Client-side password strength validation before calling `AuthService`.
- **Dependencies:** COMP-009 (AuthProvider), API-002

### COMP-008: ProfilePage
- **Type:** Frontend Page Component
- **Location:** Route `/profile`
- **Auth Required:** Yes
- **Description:** Displays `UserProfile` data retrieved via GET `/auth/me`.
- **Dependencies:** COMP-009 (AuthProvider), API-003

### COMP-009: AuthProvider
- **Type:** Frontend Context Provider
- **Location:** Wraps all routes (App root)
- **Props:** `children: ReactNode`
- **Description:** Context provider managing `AuthToken` state, silent refresh via `TokenManager`, 401 interception, and redirect logic. Exposes `UserProfile` and auth methods to child components.
- **Dependencies:** API-004 (refresh), API-003 (profile)

**Component Hierarchy:**
```
App
├── AuthProvider (COMP-009)
│   ├── PublicRoutes
│   │   ├── LoginPage (COMP-006)
│   │   └── RegisterPage (COMP-007)
│   └── ProtectedRoutes
│       └── ProfilePage (COMP-008)
```

## Testing Strategy

### TEST-001: Login with valid credentials returns AuthToken
- **Level:** Unit
- **Component:** `AuthService`
- **Validates:** FR-AUTH-001
- **Input:** Valid email/password credentials
- **Expected Output:** `AuthService.login()` calls `PasswordHasher.verify()`, then `TokenManager.issueTokens()`, returns valid `AuthToken` with accessToken and refreshToken
- **Mocks:** `PasswordHasher`, `TokenManager`, `UserRepo`

### TEST-002: Login with invalid credentials returns error
- **Level:** Unit
- **Component:** `AuthService`
- **Validates:** FR-AUTH-001
- **Input:** Valid email, wrong password
- **Expected Output:** 401 error when `PasswordHasher.verify()` returns false; no `AuthToken` issued
- **Mocks:** `PasswordHasher` (returns false), `UserRepo`

### TEST-003: Token refresh with valid refresh token
- **Level:** Unit
- **Component:** `TokenManager`
- **Validates:** FR-AUTH-003
- **Input:** Valid, non-expired, non-revoked refresh token
- **Expected Output:** Old token revoked, new `AuthToken` pair issued via `JwtService`
- **Mocks:** Redis client, `JwtService`

### TEST-004: Registration persists UserProfile to database
- **Level:** Integration
- **Scope:** `AuthService` + PostgreSQL
- **Validates:** FR-AUTH-002
- **Input:** Valid registration request (email, password, displayName)
- **Expected Output:** Full flow from API request through `PasswordHasher` to database insert; `UserProfile` retrievable from PostgreSQL
- **Mocks:** None (real PostgreSQL via testcontainers)

### TEST-005: Expired refresh token rejected by TokenManager
- **Level:** Integration
- **Scope:** `TokenManager` + Redis
- **Validates:** FR-AUTH-003
- **Input:** Refresh token with expired Redis TTL
- **Expected Output:** 401 response; Redis TTL expiration correctly invalidates refresh tokens
- **Mocks:** None (real Redis via testcontainers)

### TEST-006: User registers and logs in (E2E)
- **Level:** E2E
- **Flow:** `RegisterPage` -> `LoginPage` -> ProfilePage
- **Validates:** FR-AUTH-001, FR-AUTH-002
- **Tools:** Playwright
- **Expected Output:** Complete user journey through `AuthProvider`; user sees profile data after login

**Test Pyramid Breakdown:**

| Level | Coverage Target | Tools | Ownership |
|---|---|---|---|
| Unit | 80% | Jest, ts-jest | auth-team |
| Integration | 15% | Supertest, testcontainers | auth-team |
| E2E | 5% | Playwright | auth-team + QA |

**Test Environments:**

| Environment | Purpose | Data |
|---|---|---|
| Local | Developer testing | Docker Compose with PostgreSQL and Redis containers |
| CI | Automated pipeline | testcontainers for ephemeral databases |
| Staging | Pre-production validation | Seeded test accounts, isolated from production |

## Migration and Rollout Plan

### MIG-001: Phase 1 — Internal Alpha
- **Duration:** 1 week
- **Description:** Deploy `AuthService` to staging. auth-team and QA test all endpoints. `LoginPage` and `RegisterPage` available behind feature flag `AUTH_NEW_LOGIN`.
- **Dependencies:** All FR-AUTH-001 through FR-AUTH-005 implemented.
- **Exit Criteria:** All FRs pass manual testing. Zero P0/P1 bugs.
- **Rollback:** Disable `AUTH_NEW_LOGIN` flag.

### MIG-002: Phase 2 — Beta (10%)
- **Duration:** 2 weeks
- **Description:** Enable `AUTH_NEW_LOGIN` for 10% of traffic. Monitor `AuthService` latency, error rates, and `TokenManager` Redis usage. `AuthProvider` handles token refresh under real load.
- **Dependencies:** MIG-001 complete.
- **Exit Criteria:** p95 latency < 200ms. Error rate < 0.1%. No `TokenManager` Redis connection failures.
- **Rollback:** Disable `AUTH_NEW_LOGIN` flag.

### MIG-003: Phase 3 — General Availability (100%)
- **Duration:** 1 week
- **Description:** Remove feature flag `AUTH_NEW_LOGIN`. All users route through new `AuthService`. Legacy auth endpoints deprecated. `AUTH_TOKEN_REFRESH` flag enables refresh token flow.
- **Dependencies:** MIG-002 complete.
- **Exit Criteria:** 99.9% uptime over first 7 days. All monitoring dashboards green.
- **Rollback:** Re-enable `AUTH_NEW_LOGIN` flag to route back to legacy.

### MIG-004: Feature Flag — AUTH_NEW_LOGIN
- **Purpose:** Gates access to new `LoginPage` and `AuthService` login endpoint.
- **Default:** OFF
- **Removal Target:** After Phase 3 GA (MIG-003).

### MIG-005: Feature Flag — AUTH_TOKEN_REFRESH
- **Purpose:** Enables refresh token flow in `TokenManager`; when OFF, only access tokens are issued.
- **Default:** OFF
- **Removal Target:** Phase 3 + 2 weeks.

### MIG-006: Rollback Procedure
- **Steps:**
  1. Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth.
  2. Verify legacy login flow is operational via smoke tests.
  3. Investigate `AuthService` failure root cause using structured logs and traces.
  4. If data corruption detected in `UserProfile` table, restore from last known-good backup.
  5. Notify auth-team and platform-team via incident channel.
  6. Post-mortem within 48 hours of rollback.

### MIG-007: Rollback Criteria
- **Triggers (any one initiates rollback):**
  1. p95 latency exceeds 1000ms for > 5 minutes.
  2. Error rate exceeds 5% for > 2 minutes.
  3. `TokenManager` Redis connection failures exceed 10 per minute.
  4. Any data loss or corruption detected in `UserProfile` records.

## Operational Readiness

### OPS-001: Runbook — AuthService Down
- **Symptoms:** 5xx errors on all `/auth/*` endpoints; `LoginPage` and `RegisterPage` show error state.
- **Diagnosis:** Check `AuthService` pod health in Kubernetes. Verify PostgreSQL connectivity. Check `PasswordHasher` and `TokenManager` initialization logs.
- **Resolution:** Restart `AuthService` pods. If PostgreSQL unreachable, failover to read replica. If Redis down, `TokenManager` rejects refresh requests — users must re-login via `LoginPage`.
- **Escalation:** Page auth-team on-call. If unresolved in 15 minutes, escalate to platform-team.
- **Prevention:** Health check monitoring, HPA autoscaling, connection pool monitoring.

### OPS-002: Runbook — Token Refresh Failures
- **Symptoms:** Users report unexpected logouts; `AuthProvider` enters redirect loop to `LoginPage`; `auth_token_refresh_total` error counter spikes.
- **Diagnosis:** Check Redis connectivity from `TokenManager`. Verify `JwtService` signing key is accessible. Check `AUTH_TOKEN_REFRESH` feature flag state.
- **Resolution:** If Redis degraded, scale Redis cluster. If `JwtService` key unavailable, re-mount secrets volume. If feature flag OFF, enable `AUTH_TOKEN_REFRESH`.
- **Escalation:** Page auth-team on-call. If Redis cluster issue, escalate to platform-team.

### OPS-003: On-Call Expectations
- **Response Time:** Acknowledge P1 alerts within 15 minutes.
- **Coverage:** auth-team provides 24/7 on-call rotation during first 2 weeks post-GA.
- **Tooling:** Kubernetes dashboards, Grafana monitoring, Redis CLI, PostgreSQL admin.
- **Escalation Path:** auth-team on-call -> test-lead -> eng-manager -> platform-team.
- **Knowledge Prerequisites:** Familiarity with `AuthService`, `TokenManager`, Redis operations, JWT token lifecycle.

### OPS-004: Capacity Planning
| Resource | Current Capacity | Expected Load | Scaling Trigger | Scaling Plan |
|---|---|---|---|---|
| `AuthService` pods | 3 replicas | 500 concurrent users | CPU > 70% | HPA scales to 10 replicas |
| PostgreSQL connections | 100 pool size | 50 avg concurrent queries | Connection wait time > 50ms | Increase pool to 200 |
| Redis memory | 1 GB | ~100K refresh tokens (~50 MB) | Memory > 70% utilized | Scale to 2 GB |

**Observability:**
- **Metrics (Prometheus):** `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter)
- **Tracing:** OpenTelemetry spans covering `AuthService` -> `PasswordHasher` -> `TokenManager` -> `JwtService`
- **Logging:** Structured logs for all auth events (login success/failure, registration, token refresh, password reset)
- **Alerts:**
  - Login failure rate > 20% over 5 minutes
  - p95 latency > 500ms
  - `TokenManager` Redis connection failures
- **Infrastructure Cost:** $450/month production (3 K8s pods $150, PostgreSQL $200, Redis $100). Scales ~$50/month per 10K additional users.
