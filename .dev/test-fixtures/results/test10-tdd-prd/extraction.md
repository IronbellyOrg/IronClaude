---
spec_source: "test-tdd-user-auth.md"
generated: "2026-04-16T00:00:00Z"
generator: "superclaude-tdd-extractor"
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.65
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, testing, devops]
risks_identified: 6
dependencies_identified: 8
success_criteria_count: 10
extraction_mode: standard
data_models_identified: 3
api_surfaces_identified: 6
components_identified: 9
test_artifacts_identified: 6
migration_items_identified: 11
operational_items_identified: 9
pipeline_diagnostics: {elapsed_seconds: 262.0, started_at: "2026-04-16T16:13:20.209880+00:00", finished_at: "2026-04-16T16:17:42.243212+00:00"}
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
- **PRD Traceability:** FR-AUTH.1, Epic AUTH-E1, Alex persona JTBD #2

### FR-AUTH-002: User registration with validation
- **Description:** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
- **Components:** `AuthService`, `PasswordHasher`, `UserRepo`
- **Acceptance Criteria:**
  1. Valid registration returns 201 with `UserProfile` data.
  2. Duplicate email returns 409 Conflict.
  3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
  4. `PasswordHasher` stores bcrypt hash with cost factor 12.
- **PRD Traceability:** FR-AUTH.2, Epic AUTH-E1, Alex persona JTBD #1

### FR-AUTH-003: JWT token issuance and refresh
- **Description:** `TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
- **Components:** `TokenManager`, `JwtService`, Redis
- **Acceptance Criteria:**
  1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
  2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
  3. Expired refreshToken returns 401.
  4. Revoked refreshToken returns 401.
- **PRD Traceability:** FR-AUTH.3, Epic AUTH-E2, Sam persona JTBD #4

### FR-AUTH-004: User profile retrieval
- **Description:** `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
- **Components:** `AuthService`, `UserRepo`
- **Acceptance Criteria:**
  1. GET `/auth/me` with valid accessToken returns `UserProfile`.
  2. Expired or invalid token returns 401.
  3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.
- **PRD Traceability:** FR-AUTH.4, Epic AUTH-E3, Alex persona

### FR-AUTH-005: Password reset flow
- **Description:** `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
- **Components:** `AuthService`, `PasswordHasher`, Email Service (SendGrid)
- **Acceptance Criteria:**
  1. POST `/auth/reset-request` with valid email sends reset token via email.
  2. POST `/auth/reset-confirm` with valid token updates the password hash.
  3. Reset tokens expire after 1 hour.
  4. Used reset tokens cannot be reused.
- **PRD Traceability:** FR-AUTH.5, Epic AUTH-E3, Alex persona JTBD #3

## Non-Functional Requirements

### NFR-PERF-001: API response time
- **Category:** Performance
- **Target:** All auth endpoints must respond in < 200ms at p95
- **Measurement:** APM tracing on `AuthService` methods

### NFR-PERF-002: Concurrent authentication
- **Category:** Performance
- **Target:** Support 500 concurrent login requests
- **Measurement:** Load testing with k6

### NFR-REL-001: Service availability
- **Category:** Reliability
- **Target:** 99.9% uptime measured over 30-day rolling windows
- **Measurement:** Uptime monitoring via health check endpoint

### NFR-SEC-001: Password hashing
- **Category:** Security
- **Target:** `PasswordHasher` must use bcrypt with cost factor 12
- **Measurement:** Unit test asserting bcrypt cost parameter

### NFR-SEC-002: Token signing
- **Category:** Security
- **Target:** `JwtService` must sign tokens with RS256 using 2048-bit RSA keys
- **Measurement:** Configuration validation test

### NFR-COMP-001: GDPR consent at registration
- **Category:** Compliance
- **Source:** PRD Legal & Compliance (S17)
- **Target:** Users must consent to data collection at registration. Consent recorded with timestamp.
- **Measurement:** Registration flow audit; consent record verification
- **Note:** Not explicitly addressed in TDD. Implementation design needed.

### NFR-COMP-002: SOC2 audit logging
- **Category:** Compliance
- **Source:** PRD Legal & Compliance (S17)
- **Target:** All auth events logged with user ID, timestamp, IP, and outcome. 12-month retention.
- **Measurement:** Log retention policy validation; SOC2 control testing
- **Discrepancy:** TDD Section 7.2 specifies 90-day audit log retention. PRD specifies 12-month retention. PRD wins on business intent — retention must be 12 months.

### NFR-COMP-003: NIST SP 800-63B password storage
- **Category:** Compliance
- **Source:** PRD Legal & Compliance (S17)
- **Target:** One-way adaptive hashing. Raw passwords never persisted or logged.
- **Measurement:** Security review of `PasswordHasher` and log configurations
- **Note:** TDD's bcrypt cost 12 satisfies the hashing requirement. The "never logged" constraint must be verified across all log sinks.

### NFR-COMP-004: GDPR data minimization
- **Category:** Compliance
- **Source:** PRD Legal & Compliance (S17)
- **Target:** Only email, hashed password, and display name collected. No additional PII required.
- **Measurement:** Schema audit of `UserProfile` entity
- **Note:** TDD's `UserProfile` includes roles[] and timestamps beyond the PRD's stated minimum. Verify these do not constitute additional PII.

## Complexity Assessment

**complexity_score: 0.65** | **complexity_class: MEDIUM**

| Factor | Score | Rationale |
|---|---|---|
| Component count | 0.7 | 9 components across backend and frontend layers |
| Data store diversity | 0.6 | PostgreSQL + Redis — two distinct storage technologies with different access patterns |
| External integrations | 0.5 | Single external dependency (SendGrid) with well-defined interface |
| Security criticality | 0.8 | Authentication is security-critical; bcrypt, JWT RS256, token revocation, account lockout |
| Rollout complexity | 0.6 | 3-phase rollout with feature flags and rollback procedures |
| Cross-team coordination | 0.6 | auth-team, platform-team, frontend-team involvement |
| API surface area | 0.5 | 6 endpoints with standard REST patterns |
| State management | 0.5 | Stateless JWT plus Redis-backed refresh tokens — moderate |

Overall: well-scoped single-service feature with moderate complexity driven primarily by security requirements and multi-phase rollout. No novel algorithmic challenges or distributed systems concerns.

## Architectural Constraints

| ID | Constraint | Source |
|---|---|---|
| AC-001 | JWT-based stateless authentication with RS256 signing (no server-side sessions) | TDD Section 6.4 |
| AC-002 | bcrypt password hashing with cost factor 12 via `PasswordHasher` abstraction | TDD Section 6.4, NFR-SEC-001 |
| AC-003 | PostgreSQL 15+ for `UserProfile` persistence; Redis 7+ for refresh token storage | TDD Section 7.2 |
| AC-004 | Node.js 20 LTS runtime | TDD Section 18 |
| AC-005 | RESTful API with JSON request/response; versioned via URL prefix `/v1/auth/*` | TDD Section 8.4 |
| AC-006 | `AuthService` as facade pattern orchestrating `TokenManager`, `PasswordHasher`, `UserRepo` | TDD Section 6.2 |
| AC-007 | TLS 1.3 enforced on all endpoints | TDD Section 13 |
| AC-008 | Access token expiry: 15 minutes; refresh token expiry: 7 days | TDD FR-AUTH-003 |
| AC-009 | CORS restricted to known frontend origins | TDD Section 13 |
| AC-010 | Email/password only in v1.0 — no social login or MFA | PRD Scope Definition (S12) |
| AC-011 | `AuthService` interface must accommodate future OAuth2 and MFA without breaking changes | TDD Section 3.3 |
| AC-012 | Persona-driven: must serve Alex (end user — frictionless UX), Jordan (admin — audit visibility), Sam (API consumer — programmatic token management) | PRD User Personas (S7) |
| AC-013 | Password policy must comply with NIST SP 800-63B | PRD Constraints |

## Risk Inventory

| ID | Risk | Severity | Probability | Source | Mitigation |
|---|---|---|---|---|---|
| R-001 | Token theft via XSS allows session hijacking | High | Medium | TDD S20 | Store accessToken in memory only (not localStorage). HttpOnly cookies for refreshToken. 15-minute expiry. Immediate revocation via `TokenManager` if detected. |
| R-002 | Brute-force attacks on login endpoint | Medium | High | TDD S20 | Rate limiting 10 req/min per IP. Account lockout after 5 failed attempts. bcrypt cost 12 makes offline cracking expensive. WAF IP blocking and CAPTCHA escalation. |
| R-003 | Data loss during migration from legacy auth | High | Low | TDD S20 | Parallel operation during Phase 1-2. Idempotent upsert for `UserProfile` migration. Full database backup before each phase. Rollback to legacy with backup restore. |
| R-004 | Low registration adoption due to poor UX | High | Medium | PRD Risk Analysis | Usability testing before launch. Iterate based on funnel data. Target > 60% conversion rate. |
| R-005 | Compliance failure from incomplete audit logging | High | Medium | PRD Risk Analysis | Define log requirements early. Validate against SOC2 controls in QA. Ensure 12-month retention per PRD. |
| R-006 | Email delivery failures blocking password reset | Medium | Low | PRD Risk Analysis | Delivery monitoring and alerting on SendGrid. Fallback support channel for manual recovery. |

## Dependency Inventory

| ID | Dependency | Type | Version | Purpose | Impact if Unavailable |
|---|---|---|---|---|---|
| DEP-001 | PostgreSQL | Infrastructure | 15+ | `UserProfile` persistence, audit log storage | No user storage; service non-functional |
| DEP-002 | Redis | Infrastructure | 7+ | Refresh token storage and revocation by `TokenManager` | Token refresh fails; users must re-authenticate on every access token expiry |
| DEP-003 | Node.js | Runtime | 20 LTS | Service runtime | Cannot run `AuthService` |
| DEP-004 | bcryptjs | Library | Latest | Password hashing in `PasswordHasher` | Cannot hash or verify passwords |
| DEP-005 | jsonwebtoken | Library | Latest | JWT sign/verify in `JwtService` | Cannot issue or validate tokens |
| DEP-006 | SendGrid API | External Service | N/A | Password reset email delivery | Password reset flow blocked (FR-AUTH-005) |
| DEP-007 | Frontend routing framework | Internal | N/A | Rendering `LoginPage`, `RegisterPage`, `AuthProvider` | Auth pages cannot render |
| DEP-008 | SEC-POLICY-001 | Policy Document | N/A | Password and token security policy definitions | Password and token policies undefined |

## Success Criteria

| ID | Metric | Target | Source | Measurement Method |
|---|---|---|---|---|
| SC-001 | Login response time (p95) | < 200ms | TDD S4.1, PRD S19 | APM instrumentation on `AuthService.login()` |
| SC-002 | Registration success rate | > 99% | TDD S4.1 | Ratio of successful registrations to attempts |
| SC-003 | Token refresh latency (p95) | < 100ms | TDD S4.1 | APM instrumentation on `TokenManager.refresh()` |
| SC-004 | Service availability | 99.9% uptime | TDD S4.1 | Health check monitoring over 30-day windows |
| SC-005 | Password hash time | < 500ms | TDD S4.1 | Benchmark of `PasswordHasher.hash()` with bcrypt cost 12 |
| SC-006 | User registration conversion | > 60% | TDD S4.2, PRD S19 | Funnel analytics from `RegisterPage` to confirmed account |
| SC-007 | Daily active authenticated users | > 1000 within 30 days of GA | TDD S4.2 | `AuthToken` issuance counts |
| SC-008 | Average session duration | > 30 minutes | PRD S19 | Token refresh event analytics |
| SC-009 | Failed login rate | < 5% of attempts | PRD S19 | Auth event log analysis |
| SC-010 | Password reset completion | > 80% | PRD S19 | Funnel: reset requested → new password set |

## Open Questions

| ID | Question | Owner | Target Date | Status | Source |
|---|---|---|---|---|---|
| OQ-001 | Should `AuthService` support API key authentication for service-to-service calls? | test-lead | 2026-04-15 | Open (overdue) | TDD S22 |
| OQ-002 | What is the maximum allowed `UserProfile` roles array length? | auth-team | 2026-04-01 | Open (overdue) | TDD S22 |
| OQ-003 | Audit log retention discrepancy: TDD specifies 90 days (S7.2), PRD specifies 12 months (S17). Which is authoritative? | auth-team / compliance | — | Open | Extraction analysis |
| OQ-004 | No logout endpoint defined in TDD. PRD lists logout as in-scope. Is logout implemented as client-side token clearing via `AuthProvider`, or does `AuthService` need a server-side logout endpoint for refresh token revocation? | auth-team | — | Open | PRD Scope vs TDD gap |
| OQ-005 | PRD user story: "As Jordan (admin), I want to view authentication event logs." No corresponding admin API or FR in TDD. Is admin log access deferred or missing? | test-lead | — | Open | PRD Epic AUTH-E3 gap |
| OQ-006 | Should password reset emails be sent synchronously or asynchronously? | Engineering | — | Open | PRD S14 |
| OQ-007 | Maximum number of refresh tokens allowed per user across devices? | Product | — | Open | PRD S14 |
| OQ-008 | Should "remember me" functionality extend session duration beyond 7 days? | Product | — | Open | PRD S14 |
| OQ-009 | GDPR consent mechanism at registration (NFR-COMP-001) has no implementation design in TDD. How should consent be captured and stored? | auth-team | — | Open | PRD S17 |
| OQ-010 | `UserProfile` includes roles[] and timestamps beyond PRD's stated GDPR data minimization scope (email, hashed password, display name). Are these fields compliant? | compliance | — | Open | NFR-COMP-004 analysis |

## Data Models and Interfaces

### DM-001: UserProfile
- **Source:** TDD Section 7.1
- **Storage:** PostgreSQL 15 (TDD S7.2)
- **Retention:** Indefinite

| Field | Type | Constraints | Required | Description |
|---|---|---|---|---|
| id | string (UUID v4) | PRIMARY KEY, NOT NULL | Yes | Unique user identifier generated by `AuthService` |
| email | string | UNIQUE, NOT NULL, indexed, lowercase normalized | Yes | User email, normalized to lowercase by `AuthService` |
| displayName | string | NOT NULL, 2-100 chars | Yes | Display name shown in UI |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Yes | Account creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Yes | Last profile modification timestamp |
| lastLoginAt | string (ISO 8601) | NULLABLE | No | Updated by `AuthService` on each successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Yes | Authorization roles; enforced downstream |

- **Relationships:** Referenced by `AuthToken` (access token JWT payload contains user id and roles). Associated with audit log entries.

### DM-002: AuthToken
- **Source:** TDD Section 7.1
- **Storage:** accessToken is stateless (JWT); refreshToken stored in Redis 7 by `TokenManager` (TDD S7.2)
- **Retention:** accessToken: 15 minutes; refreshToken: 7-day TTL in Redis

| Field | Type | Constraints | Required | Description |
|---|---|---|---|---|
| accessToken | string (JWT) | NOT NULL | Yes | Signed by `JwtService` using RS256; contains user id and roles in payload |
| refreshToken | string | NOT NULL, unique | Yes | Opaque token managed by `TokenManager`; stored hashed in Redis |
| expiresIn | number | NOT NULL | Yes | Seconds until accessToken expiration; always 900 |
| tokenType | string | NOT NULL | Yes | Always "Bearer"; OAuth2 compatibility |

- **Relationships:** accessToken JWT payload references `UserProfile.id` and `UserProfile.roles`. refreshToken maps to a `UserProfile` in Redis.

### DM-003: Audit Log
- **Source:** TDD Section 7.2, PRD S17
- **Storage:** PostgreSQL 15
- **Retention:** 90 days (TDD) / 12 months (PRD) — **discrepancy, see OQ-003**

| Field | Type | Constraints | Required | Description |
|---|---|---|---|---|
| userId | string (UUID) | NOT NULL | Yes | Reference to `UserProfile.id` |
| eventType | string | NOT NULL | Yes | e.g., login_success, login_failure, registration, password_reset |
| timestamp | string (ISO 8601) | NOT NULL | Yes | When the event occurred |
| ipAddress | string | NOT NULL | Yes | Source IP (per PRD S17 SOC2 requirement) |
| outcome | string | NOT NULL | Yes | Success or failure with reason |

- **Note:** Schema inferred from PRD SOC2 requirements and TDD S7.2 mention. Not fully specified in TDD as an interface.

## API Specifications

### API-001: POST `/auth/login`
- **Auth Required:** No
- **Rate Limit:** 10 req/min per IP
- **Description:** Authenticate user via `AuthService`, issue `AuthToken` pair
- **Request Body:**
  - `email` (string, required): User email
  - `password` (string, required): User password
- **Response (200):** `AuthToken` object (accessToken, refreshToken, expiresIn: 900, tokenType: "Bearer")
- **Error Responses:**
  - 401 Unauthorized: Invalid email or password (AUTH_INVALID_CREDENTIALS)
  - 423 Locked: Account locked after 5 failed attempts
  - 429 Too Many Requests: Rate limit exceeded
- **FR Traceability:** FR-AUTH-001

### API-002: POST `/auth/register`
- **Auth Required:** No
- **Rate Limit:** 5 req/min per IP
- **Description:** Create new `UserProfile` via `AuthService`
- **Request Body:**
  - `email` (string, required): New user email
  - `password` (string, required): Must meet strength policy (>= 8 chars, uppercase, number)
  - `displayName` (string, required): 2-100 characters
- **Response (201):** `UserProfile` object (id, email, displayName, createdAt, updatedAt, lastLoginAt: null, roles: ["user"])
- **Error Responses:**
  - 400 Bad Request: Validation errors (weak password, invalid email)
  - 409 Conflict: Email already registered
- **FR Traceability:** FR-AUTH-002

### API-003: GET `/auth/me`
- **Auth Required:** Yes (Bearer token in Authorization header)
- **Rate Limit:** 60 req/min per user
- **Description:** Return authenticated user's `UserProfile`
- **Request Headers:** `Authorization: Bearer <accessToken>`
- **Response (200):** `UserProfile` object
- **Error Responses:**
  - 401 Unauthorized: Missing, expired, or invalid accessToken
- **FR Traceability:** FR-AUTH-004

### API-004: POST `/auth/refresh`
- **Auth Required:** No (refresh token in body)
- **Rate Limit:** 30 req/min per user
- **Description:** Exchange valid refresh token for new `AuthToken` pair via `TokenManager`
- **Request Body:**
  - `refreshToken` (string, required): Previously issued refresh token
- **Response (200):** New `AuthToken` object (old refresh token revoked)
- **Error Responses:**
  - 401 Unauthorized: Expired or revoked refresh token
- **FR Traceability:** FR-AUTH-003

### API-005: POST `/auth/reset-request`
- **Auth Required:** No
- **Rate Limit:** Not specified (inherits default)
- **Description:** Request password reset; sends email with time-limited token
- **Request Body:**
  - `email` (string, required): Account email
- **Response:** Success response regardless of registration status (prevents enumeration)
- **Error Responses:** Not specified
- **FR Traceability:** FR-AUTH-005 (AC 1)
- **Note:** Endpoint implied by FR-AUTH-005 but not detailed in TDD Section 8. Request/response schema needs specification.

### API-006: POST `/auth/reset-confirm`
- **Auth Required:** No
- **Rate Limit:** Not specified
- **Description:** Validate reset token and update password
- **Request Body:**
  - `token` (string, required): Reset token from email
  - `password` (string, required): New password (must meet strength policy)
- **Response:** Success confirmation
- **Error Responses:** Expired token, already-used token
- **FR Traceability:** FR-AUTH-005 (AC 2-4)
- **Note:** Endpoint implied by FR-AUTH-005 but not detailed in TDD Section 8. Request/response schema needs specification.

**Error Response Format (all endpoints):**
```json
{
  "error": {
    "code": "AUTH_ERROR_CODE",
    "message": "Human-readable description",
    "status": 401
  }
}
```

**Versioning:** URL prefix `/v1/auth/*` in production. Breaking changes require new major version. Non-breaking additions permitted within current version.

## Component Inventory

### COMP-001: AuthService
- **Type:** Backend service (facade/orchestrator)
- **Location:** Backend service layer
- **Description:** Primary orchestrator for all auth flows. Receives requests from API Gateway and delegates to specialized components.
- **Dependencies:** COMP-002 (TokenManager), COMP-004 (PasswordHasher), COMP-005 (UserRepo), Email Service (SendGrid)
- **Implements:** FR-AUTH-001, FR-AUTH-002, FR-AUTH-004, FR-AUTH-005

### COMP-002: TokenManager
- **Type:** Backend module
- **Location:** Within `AuthService` boundary
- **Description:** Manages JWT access/refresh token lifecycle. Issues, validates, refreshes, and revokes tokens. Stores refresh tokens in Redis.
- **Dependencies:** COMP-003 (JwtService), Redis
- **Implements:** FR-AUTH-003

### COMP-003: JwtService
- **Type:** Backend module
- **Location:** Within `TokenManager`
- **Description:** Signs and verifies JWT tokens using RS256 with 2048-bit RSA keys. 5-second clock skew tolerance.
- **Dependencies:** RSA key pair (rotated quarterly)
- **Implements:** NFR-SEC-002

### COMP-004: PasswordHasher
- **Type:** Backend module
- **Location:** Within `AuthService` boundary
- **Description:** Abstraction over bcrypt with configurable cost factor (12). Designed for future algorithm migration.
- **Dependencies:** bcryptjs library
- **Implements:** NFR-SEC-001

### COMP-005: UserRepo
- **Type:** Data access layer
- **Location:** Within `AuthService` boundary
- **Description:** Handles `UserProfile` persistence operations against PostgreSQL. Connection pooling via pg-pool.
- **Dependencies:** PostgreSQL 15+, pg-pool

### COMP-006: LoginPage
- **Type:** Frontend page component
- **Location:** Route `/login`
- **Auth Required:** No
- **Props:** `onSuccess: () => void`, `redirectUrl?: string`
- **Description:** Email/password login form. Handles form submission to `AuthService` login endpoint. Stores `AuthToken` via `AuthProvider`.
- **Dependencies:** COMP-009 (AuthProvider), API-001

### COMP-007: RegisterPage
- **Type:** Frontend page component
- **Location:** Route `/register`
- **Auth Required:** No
- **Props:** `onSuccess: () => void`, `termsUrl: string`
- **Description:** Registration form with email, password, displayName fields. Client-side password strength validation before API call.
- **Dependencies:** COMP-009 (AuthProvider), API-002

### COMP-008: ProfilePage
- **Type:** Frontend page component
- **Location:** Route `/profile`
- **Auth Required:** Yes
- **Description:** Displays `UserProfile` data via GET `/auth/me`.
- **Dependencies:** COMP-009 (AuthProvider), API-003

### COMP-009: AuthProvider
- **Type:** Frontend context provider (React)
- **Location:** Wraps all routes at application root
- **Props:** `children: ReactNode`
- **Description:** Manages `AuthToken` state. Handles silent refresh via `TokenManager`. Exposes `UserProfile` and auth methods to child components. Intercepts 401 responses, triggers token refresh, redirects unauthenticated users to `LoginPage`.
- **Dependencies:** API-004, COMP-006 (redirect target)

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
- **Input:** Valid email and password
- **Expected Output:** `AuthToken` with accessToken and refreshToken
- **Mocks:** `PasswordHasher.verify()` returns true, `TokenManager.issueTokens()` returns token pair
- **Validates:** FR-AUTH-001

### TEST-002: Login with invalid credentials returns error
- **Level:** Unit
- **Component:** `AuthService`
- **Input:** Valid email, wrong password
- **Expected Output:** 401 error response
- **Mocks:** `PasswordHasher.verify()` returns false
- **Validates:** FR-AUTH-001

### TEST-003: Token refresh with valid refresh token
- **Level:** Unit
- **Component:** `TokenManager`
- **Input:** Valid, non-expired refresh token
- **Expected Output:** New `AuthToken` pair; old refresh token revoked
- **Mocks:** Redis returns valid token record
- **Validates:** FR-AUTH-003

### TEST-004: Registration persists UserProfile to database
- **Level:** Integration
- **Scope:** `AuthService` + PostgreSQL
- **Input:** Valid registration request (email, password, displayName)
- **Expected Output:** `UserProfile` persisted with bcrypt-hashed password
- **Mocks:** None (real PostgreSQL via testcontainers)
- **Validates:** FR-AUTH-002

### TEST-005: Expired refresh token rejected by TokenManager
- **Level:** Integration
- **Scope:** `TokenManager` + Redis
- **Input:** Refresh token past 7-day TTL
- **Expected Output:** 401 rejection
- **Mocks:** None (real Redis via testcontainers)
- **Validates:** FR-AUTH-003

### TEST-006: User registers and logs in (full journey)
- **Level:** E2E
- **Flow:** `RegisterPage` → `LoginPage` → ProfilePage
- **Input:** New user registration data, then login with same credentials
- **Expected Output:** Account created, login succeeds, profile page displays user data
- **Tools:** Playwright
- **Validates:** FR-AUTH-001, FR-AUTH-002

**Test Pyramid:**

| Level | Coverage Target | Tools | Ownership |
|---|---|---|---|
| Unit | 80% | Jest, ts-jest | auth-team |
| Integration | 15% | Supertest, testcontainers | auth-team |
| E2E | 5% | Playwright | QA |

**Test Environments:**

| Environment | Purpose | Infrastructure |
|---|---|---|
| Local | Developer testing | Docker Compose (PostgreSQL + Redis) |
| CI | Automated pipeline | testcontainers (ephemeral) |
| Staging | Pre-production validation | Seeded test accounts, isolated |

## Migration and Rollout Plan

### MIG-001: Phase 1 — Internal Alpha
- **Duration:** 1 week
- **Description:** Deploy `AuthService` to staging. auth-team and QA test all endpoints. `LoginPage` and `RegisterPage` available behind feature flag `AUTH_NEW_LOGIN`.
- **Dependencies:** All FR-AUTH-001 through FR-AUTH-005 implemented
- **Success Criteria:** All FRs pass manual testing. Zero P0/P1 bugs.
- **Rollback:** Disable `AUTH_NEW_LOGIN` flag

### MIG-002: Phase 2 — Beta (10%)
- **Duration:** 2 weeks
- **Description:** Enable `AUTH_NEW_LOGIN` for 10% of traffic. Monitor `AuthService` latency, error rates, and `TokenManager` Redis usage. `AuthProvider` handles token refresh under real load.
- **Dependencies:** MIG-001 complete
- **Success Criteria:** p95 latency < 200ms. Error rate < 0.1%. No `TokenManager` Redis connection failures.
- **Rollback:** Disable `AUTH_NEW_LOGIN` flag

### MIG-003: Phase 3 — General Availability (100%)
- **Duration:** 1 week
- **Description:** Remove feature flag `AUTH_NEW_LOGIN`. All users route through new `AuthService`. Legacy auth endpoints deprecated. `AUTH_TOKEN_REFRESH` flag enables refresh token flow.
- **Dependencies:** MIG-002 complete
- **Success Criteria:** 99.9% uptime over first 7 days. All monitoring dashboards green.
- **Rollback:** Re-enable `AUTH_NEW_LOGIN` flag to route to legacy

### MIG-004: Feature Flag — AUTH_NEW_LOGIN
- **Purpose:** Gates access to new `LoginPage` and `AuthService` login endpoint
- **Default:** OFF
- **Removal Target:** After Phase 3 GA

### MIG-005: Feature Flag — AUTH_TOKEN_REFRESH
- **Purpose:** Enables refresh token flow in `TokenManager`; when OFF, only access tokens issued
- **Default:** OFF
- **Removal Target:** Phase 3 + 2 weeks

### MIG-006: Rollback Step 1 — Disable feature flag
- **Action:** Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth

### MIG-007: Rollback Step 2 — Verify legacy
- **Action:** Verify legacy login flow is operational via smoke tests

### MIG-008: Rollback Step 3 — Investigate root cause
- **Action:** Investigate `AuthService` failure root cause using structured logs and traces

### MIG-009: Rollback Step 4 — Restore data if needed
- **Action:** If data corruption detected in `UserProfile` table, restore from last known-good backup

### MIG-010: Rollback Step 5 — Notify teams
- **Action:** Notify auth-team and platform-team via incident channel

### MIG-011: Rollback Step 6 — Post-mortem
- **Action:** Post-mortem within 48 hours of rollback

**Rollback Triggers:**
- p95 latency exceeds 1000ms for more than 5 minutes
- Error rate exceeds 5% for more than 2 minutes
- `TokenManager` Redis connection failures exceed 10 per minute
- Any data loss or corruption detected in `UserProfile` records

## Operational Readiness

### OPS-001: Runbook — AuthService Down
- **Symptoms:** 5xx errors on all `/auth/*` endpoints; `LoginPage` and `RegisterPage` show error state
- **Diagnosis:** Check `AuthService` pod health in Kubernetes. Verify PostgreSQL connectivity. Check `PasswordHasher` and `TokenManager` initialization logs.
- **Resolution:** Restart `AuthService` pods. If PostgreSQL unreachable, failover to read replica. If Redis down, `TokenManager` rejects refresh requests — users must re-login.
- **Escalation:** Page auth-team on-call. If unresolved in 15 minutes, escalate to platform-team.
- **Prevention:** Health check monitoring, pod auto-restart via Kubernetes liveness probes

### OPS-002: Runbook — Token Refresh Failures
- **Symptoms:** Users logged out unexpectedly; `AuthProvider` enters redirect loop to `LoginPage`; `auth_token_refresh_total` error counter spikes
- **Diagnosis:** Check Redis connectivity from `TokenManager`. Verify `JwtService` signing key accessible. Check `AUTH_TOKEN_REFRESH` feature flag state.
- **Resolution:** If Redis degraded, scale Redis cluster. If `JwtService` key unavailable, re-mount secrets volume. If feature flag OFF, enable `AUTH_TOKEN_REFRESH`.
- **Escalation:** Page auth-team on-call. If Redis cluster issue, escalate to platform-team.
- **Prevention:** Redis cluster monitoring, key availability checks in health endpoint

### OPS-003: On-Call Expectations
- **Response Time:** Acknowledge P1 alerts within 15 minutes
- **Coverage:** auth-team provides 24/7 on-call rotation during first 2 weeks post-GA
- **Tooling:** Kubernetes dashboards, Grafana monitoring, Redis CLI, PostgreSQL admin
- **Escalation Path:** auth-team on-call → test-lead → eng-manager → platform-team
- **Knowledge Prerequisites:** Familiarity with `AuthService`, `TokenManager`, `JwtService` internals

### OPS-004: Capacity — AuthService Pods
- **Current:** 3 replicas
- **Expected Load:** 500 concurrent users
- **Scaling Plan:** HPA scales to 10 replicas based on CPU > 70%

### OPS-005: Capacity — PostgreSQL Connections
- **Current:** 100 pool size
- **Expected Load:** 50 avg concurrent queries
- **Scaling Trigger:** Increase pool to 200 if connection wait time > 50ms

### OPS-006: Capacity — Redis Memory
- **Current:** 1 GB
- **Expected Load:** ~100K refresh tokens (~50 MB)
- **Scaling Trigger:** Scale to 2 GB if > 70% utilized

### OPS-007: Alert — Login Failure Rate
- **Metric:** Login failure rate
- **Threshold:** Exceeding 20% over 5 minutes
- **Source:** `auth_login_total` counter (Prometheus)
- **Action:** Investigate via runbook OPS-001

### OPS-008: Alert — P95 Latency
- **Metric:** Auth endpoint p95 latency
- **Threshold:** Exceeding 500ms
- **Source:** `auth_login_duration_seconds` histogram (Prometheus)
- **Action:** Check `AuthService` pod resources and database query performance

### OPS-009: Alert — Redis Connection Failures
- **Metric:** `TokenManager` Redis connection failures
- **Threshold:** Any sustained failures
- **Source:** `TokenManager` structured logs
- **Action:** Investigate via runbook OPS-002

**Observability Stack:**
- **Logging:** Structured logs for all auth events (login, registration, token refresh, password reset)
- **Metrics:** Prometheus — `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter)
- **Tracing:** OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`
- **Dashboards:** Grafana dashboards for `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`
