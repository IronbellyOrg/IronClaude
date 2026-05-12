---
spec_source: "test-tdd-user-auth.md"
generated: "2026-04-03T12:00:00Z"
generator: "requirements-extraction-agent"
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.65
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, testing, devops]
risks_identified: 7
dependencies_identified: 8
success_criteria_count: 10
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 9
test_artifacts_identified: 6
migration_items_identified: 6
operational_items_identified: 6
pipeline_diagnostics: {elapsed_seconds: 344.1, started_at: "2026-04-04T01:04:12.188727+00:00", finished_at: "2026-04-04T01:09:56.294347+00:00"}
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
- **PRD Traceability:** FR-AUTH.1, Epic AUTH-E1, Alex persona JTBD #2.

### FR-AUTH-002: User registration with validation

- **Description:** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
- **Components:** `AuthService`, `PasswordHasher`, `UserRepo`
- **Acceptance Criteria:**
  1. Valid registration returns 201 with `UserProfile` data.
  2. Duplicate email returns 409 Conflict.
  3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
  4. `PasswordHasher` stores bcrypt hash with cost factor 12.
- **PRD Traceability:** FR-AUTH.2, Epic AUTH-E1, Alex persona JTBD #1.

### FR-AUTH-003: JWT token issuance and refresh

- **Description:** `TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
- **Components:** `TokenManager`, `JwtService`, Redis
- **Acceptance Criteria:**
  1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
  2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
  3. Expired refreshToken returns 401.
  4. Revoked refreshToken returns 401.
- **PRD Traceability:** FR-AUTH.3, Epic AUTH-E2, Sam persona JTBD #4.

### FR-AUTH-004: User profile retrieval

- **Description:** `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
- **Components:** `AuthService`, `UserRepo`
- **Acceptance Criteria:**
  1. GET `/auth/me` with valid accessToken returns `UserProfile`.
  2. Expired or invalid token returns 401.
  3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.
- **PRD Traceability:** FR-AUTH.4, Epic AUTH-E3, Alex persona.

### FR-AUTH-005: Password reset flow

- **Description:** `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
- **Components:** `AuthService`, `PasswordHasher`, Email Service
- **Acceptance Criteria:**
  1. POST `/auth/reset-request` with valid email sends reset token via email.
  2. POST `/auth/reset-confirm` with valid token updates the password hash.
  3. Reset tokens expire after 1 hour.
  4. Used reset tokens cannot be reused.
- **PRD Traceability:** FR-AUTH.5, Epic AUTH-E3, Alex persona JTBD #3.

---

## Non-Functional Requirements

### NFR-PERF-001: API response time

- **Category:** Performance
- **Target:** All auth endpoints must respond in < 200ms at p95.
- **Measurement:** APM tracing on `AuthService` methods.

### NFR-PERF-002: Concurrent authentication

- **Category:** Performance
- **Target:** Support 500 concurrent login requests.
- **Measurement:** Load testing with k6.

### NFR-REL-001: Service availability

- **Category:** Reliability
- **Target:** 99.9% uptime measured over 30-day rolling windows.
- **Measurement:** Uptime monitoring via health check endpoint.

### NFR-SEC-001: Password hashing

- **Category:** Security
- **Target:** `PasswordHasher` must use bcrypt with cost factor 12.
- **Measurement:** Unit test asserting bcrypt cost parameter.

### NFR-SEC-002: Token signing

- **Category:** Security
- **Target:** `JwtService` must sign tokens with RS256 using 2048-bit RSA keys.
- **Measurement:** Configuration validation test.

### NFR-COMP-001: GDPR consent at registration

- **Category:** Compliance
- **Source:** PRD Legal & Compliance (S17)
- **Target:** Users must consent to data collection at registration. Consent recorded with timestamp.
- **Standard:** GDPR
- **Note:** Not explicitly addressed in TDD. Must be added to `AuthService` registration flow and `UserProfile` schema (consent timestamp field).

### NFR-COMP-002: SOC2 audit logging

- **Category:** Compliance
- **Source:** PRD Legal & Compliance (S17)
- **Target:** All auth events logged with user ID, timestamp, IP, and outcome. 12-month retention.
- **Standard:** SOC2 Type II
- **Note:** TDD Section 7.2 specifies 90-day audit log retention. PRD requires 12-month retention. **Conflict identified — PRD wins on business intent: retention must be 12 months.**

### NFR-COMP-003: NIST password storage compliance

- **Category:** Compliance
- **Source:** PRD Legal & Compliance (S17)
- **Target:** One-way adaptive hashing. Raw passwords never persisted or logged.
- **Standard:** NIST SP 800-63B
- **Note:** Covered by NFR-SEC-001 (bcrypt cost 12) but NIST compliance should be explicitly validated.

### NFR-COMP-004: GDPR data minimization

- **Category:** Compliance
- **Source:** PRD Legal & Compliance (S17)
- **Target:** Only email, hashed password, and display name collected. No additional PII required.
- **Standard:** GDPR
- **Note:** `UserProfile` schema is consistent with this requirement.

---

## Complexity Assessment

- **Complexity Score:** 0.65
- **Complexity Class:** MEDIUM

**Scoring Rationale:**

| Factor | Score | Rationale |
|--------|-------|-----------|
| Component count | 0.6 | 9 components (5 backend, 4 frontend) — moderate but well-bounded |
| Integration complexity | 0.7 | PostgreSQL, Redis, Email (SendGrid), API Gateway — multiple external systems |
| Security surface | 0.8 | JWT token lifecycle, bcrypt hashing, account lockout, token revocation, CORS, TLS — high security complexity |
| Data model complexity | 0.4 | 2 data entities with clear schemas — straightforward |
| API surface | 0.5 | 6 endpoints (4 fully specified, 2 referenced) — moderate |
| Migration complexity | 0.7 | 3-phase rollout with feature flags, rollback procedures, parallel legacy operation |
| Team coordination | 0.6 | auth-team, platform-team, frontend-team — moderate cross-team dependencies |
| **Weighted average** | **0.65** | |

---

## Architectural Constraints

1. **Session mechanism:** JWT with refresh tokens (stateless). Server-side sessions explicitly rejected (Section 6.4).
2. **Password hashing:** bcrypt via `PasswordHasher` abstraction. Cost factor 12. Argon2id and scrypt rejected.
3. **Token signing:** RS256 with 2048-bit RSA keys. Keys rotated quarterly.
4. **Runtime:** Node.js 20 LTS.
5. **Data stores:** PostgreSQL 15+ for user records and audit logs. Redis 7+ for refresh token storage.
6. **API versioning:** URL prefix (`/v1/auth/*`). Breaking changes require new major version.
7. **Stateless design:** No server-side session state. All state in JWT tokens and Redis refresh tokens.
8. **Refresh token storage:** Hashed values in Redis (not plaintext) to prevent token theft.
9. **Clock skew tolerance:** 5-second tolerance in `JwtService` for JWT validation.
10. **Connection pooling:** pg-pool for PostgreSQL connections.
11. **Persona-driven design requirements (from PRD S7):**
    - **Alex (End User):** Registration must complete in < 60 seconds. Login must feel instant (< 200ms). Sessions must persist across page refreshes.
    - **Jordan (Platform Admin):** Requires visibility into failed logins, account lock/unlock, and compliance audit trail. Admin auth event log querying is implied but not specified in TDD.
    - **Sam (API Consumer):** Requires programmatic token management, stable auth contracts, and clear error codes.

---

## Risk Inventory

1. **R-001 — Token theft via XSS** (Severity: HIGH, Probability: Medium)
   - **Mitigation:** Store accessToken in memory only. HttpOnly cookies for refreshToken. `JwtService` 15-minute expiry. `AuthProvider` clears tokens on tab close.
   - **Contingency:** Immediate token revocation via `TokenManager`. Force password reset for affected accounts.

2. **R-002 — Brute-force attacks on login endpoint** (Severity: MEDIUM, Probability: High)
   - **Mitigation:** Rate limiting at API Gateway (10 req/min per IP). Account lockout after 5 failed attempts. bcrypt cost factor 12.
   - **Contingency:** WAF IP blocking. CAPTCHA on `LoginPage` after 3 failed attempts.

3. **R-003 — Data loss during migration from legacy auth** (Severity: HIGH, Probability: Low)
   - **Mitigation:** Parallel operation with legacy system in Phases 1-2. Idempotent upsert migrations. Full database backup before each phase.
   - **Contingency:** Rollback to legacy auth. Restore from pre-migration backup.

4. **R-004 — Low registration adoption due to poor UX** (Severity: HIGH, Probability: Medium)
   - **Source:** PRD Risk Analysis
   - **Mitigation:** Usability testing before launch; iterate based on funnel data.

5. **R-005 — Security breach from implementation flaws** (Severity: CRITICAL, Probability: Low)
   - **Source:** PRD Risk Analysis
   - **Mitigation:** Dedicated security review; penetration testing before production.

6. **R-006 — Compliance failure from incomplete audit logging** (Severity: HIGH, Probability: Medium)
   - **Source:** PRD Risk Analysis
   - **Mitigation:** Define log requirements early; validate against SOC2 controls in QA.
   - **Note:** TDD specifies 90-day retention but PRD requires 12 months — this risk materializes if the TDD retention is implemented as-is.

7. **R-007 — Email delivery failures blocking password reset** (Severity: MEDIUM, Probability: Low)
   - **Source:** PRD Risk Analysis
   - **Mitigation:** Delivery monitoring and alerting; fallback support channel.

---

## Dependency Inventory

| # | Dependency | Type | Version/Detail | Impact if Unavailable |
|---|-----------|------|----------------|----------------------|
| 1 | PostgreSQL | Infrastructure | 15+ | No `UserProfile` persistence or audit logging |
| 2 | Redis | Infrastructure | 7+ | `TokenManager` cannot store/revoke refresh tokens; users must re-login on every access token expiry |
| 3 | Node.js | Runtime | 20 LTS | Service cannot run |
| 4 | bcryptjs | Library | npm package | `PasswordHasher` cannot hash/verify passwords |
| 5 | jsonwebtoken | Library | npm package | `JwtService` cannot sign/verify JWTs |
| 6 | SendGrid | External Service | API | Password reset flow (FR-AUTH-005) blocked |
| 7 | Frontend routing framework | Internal | — | `LoginPage`, `RegisterPage`, `ProfilePage` cannot render |
| 8 | SEC-POLICY-001 | Policy Document | — | Password and token policies undefined; security configurations ungoverned |

---

## Success Criteria

| # | Metric | Target | Source | Measurement Method |
|---|--------|--------|--------|-------------------|
| 1 | Login response time (p95) | < 200ms | TDD §4.1 + PRD | APM instrumentation on `AuthService.login()` |
| 2 | Registration success rate | > 99% | TDD §4.1 | Ratio of successful registrations to attempts |
| 3 | Token refresh latency (p95) | < 100ms | TDD §4.1 | APM instrumentation on `TokenManager.refresh()` |
| 4 | Service availability | 99.9% uptime | TDD §4.1 | Health check monitoring over 30-day windows |
| 5 | Password hash time | < 500ms | TDD §4.1 | Benchmark of `PasswordHasher.hash()` with bcrypt cost 12 |
| 6 | User registration conversion | > 60% | TDD §4.2 + PRD | Funnel analytics from `RegisterPage` to confirmed account |
| 7 | Daily active authenticated users | > 1000 within 30 days of GA | TDD §4.2 | `AuthToken` issuance counts |
| 8 | Average session duration | > 30 minutes | PRD S19 | Token refresh event analytics |
| 9 | Failed login rate | < 5% of attempts | PRD S19 | Auth event log analysis |
| 10 | Password reset completion | > 80% | PRD S19 | Funnel: reset requested → new password set |

---

## Open Questions

| # | Question | Source | Owner | Status |
|---|----------|--------|-------|--------|
| 1 | Should `AuthService` support API key authentication for service-to-service calls? | TDD OQ-001 | test-lead | Open — deferred to v1.1 |
| 2 | What is the maximum allowed `UserProfile` roles array length? | TDD OQ-002 | auth-team | Open — pending RBAC design |
| 3 | Should password reset emails be sent synchronously or asynchronously? | PRD S13 | Engineering | Open |
| 4 | Maximum number of refresh tokens allowed per user across devices? | PRD S13 | Product | Open |
| 5 | Should "remember me" extend session duration beyond 7-day refresh window? | PRD S13 | Product | Open |
| 6 | **Audit log retention conflict:** TDD §7.2 specifies 90-day retention; PRD §S17 requires 12-month retention for SOC2. Which governs? | Extraction gap | auth-team + compliance | Open — **must resolve before implementation** |
| 7 | **Logout endpoint missing:** PRD Epic AUTH-E1 includes a logout user story ("log out to secure session on shared device") but the TDD defines no logout endpoint or `AuthService.logout()` method. How are sessions terminated? | PRD/TDD gap | Engineering | Open |
| 8 | **Admin audit log query missing:** PRD user story for Jordan (admin) requires queryable auth event logs (by date range and user). TDD §14 defines log emission but no query API. Is a separate admin API in scope? | PRD/TDD gap | Product + Engineering | Open |
| 9 | **GDPR consent field missing:** NFR-COMP-001 requires consent recording at registration. `UserProfile` schema lacks a consent timestamp field. | PRD/TDD gap | Engineering | Open |
| 10 | **Password reset endpoints unspecified:** FR-AUTH-005 references `/auth/reset-request` and `/auth/reset-confirm` but TDD §8 provides no detailed specifications for these endpoints. | TDD gap | Engineering | Open |

---

## Data Models and Interfaces

### DM-001: UserProfile

- **Source:** TDD §7.1
- **Storage:** PostgreSQL 15
- **Retention:** Indefinite

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string (UUID v4) | PRIMARY KEY, NOT NULL | Unique user identifier generated by `AuthService` |
| email | string | UNIQUE, NOT NULL, indexed, lowercase normalized | User email |
| displayName | string | NOT NULL, 2-100 chars | Display name shown in UI |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Account creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Last profile modification timestamp |
| lastLoginAt | string (ISO 8601) | NULLABLE | Updated by `AuthService` on each successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Authorization roles; enforcement is downstream |

**Relationships:**
- One-to-many with refresh tokens (stored in Redis, keyed by user id)
- One-to-many with audit log entries

**Missing fields identified (from PRD compliance):**
- `consentTimestamp` — required by NFR-COMP-001 (GDPR consent at registration)
- `passwordHash` — implied by `PasswordHasher` but not in the `UserProfile` interface (likely intentional separation; stored in same DB row but not exposed via API)

### DM-002: AuthToken

- **Source:** TDD §7.1
- **Storage:** accessToken is ephemeral (in-memory client-side); refreshToken stored in Redis 7 with 7-day TTL
- **Retention:** 7-day TTL for refresh tokens

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| accessToken | string (JWT) | NOT NULL | Signed by `JwtService` using RS256; contains user id and roles in payload |
| refreshToken | string | NOT NULL, unique | Opaque token managed by `TokenManager`; stored as hashed value in Redis |
| expiresIn | number | NOT NULL, always 900 | Seconds until accessToken expiration (15 minutes) |
| tokenType | string | NOT NULL, always "Bearer" | OAuth2 compatibility field |

**Additional storage noted (TDD §7.2):**

| Store | Technology | Purpose | Retention |
|-------|-----------|---------|-----------|
| User records | PostgreSQL 15 | `UserProfile` persistence, password hashes | Indefinite |
| Refresh tokens | Redis 7 | Token storage and revocation | 7-day TTL |
| Audit log | PostgreSQL 15 | Login attempts, password resets | 90 days (TDD) / 12 months (PRD — conflict) |

---

## API Specifications

### API-001: POST `/auth/login`

- **Auth Required:** No
- **Rate Limit:** 10 req/min per IP
- **Description:** Authenticate user via `AuthService`, validate credentials through `PasswordHasher`, issue tokens via `TokenManager`.
- **Request Body:** `{ email: string, password: string }`
- **Response (200):** `AuthToken` — `{ accessToken, refreshToken, expiresIn: 900, tokenType: "Bearer" }`
- **Error Responses:**
  - 401 Unauthorized: Invalid email or password (code: `AUTH_INVALID_CREDENTIALS`)
  - 423 Locked: Account locked after 5 failed attempts
  - 429 Too Many Requests: Rate limit exceeded
- **Traces to:** FR-AUTH-001

### API-002: POST `/auth/register`

- **Auth Required:** No
- **Rate Limit:** 5 req/min per IP
- **Description:** Create new user account. Validates email uniqueness, enforces password policy, hashes via `PasswordHasher`, persists `UserProfile`.
- **Request Body:** `{ email: string, password: string, displayName: string }`
- **Response (201):** `UserProfile` — `{ id, email, displayName, createdAt, updatedAt, lastLoginAt: null, roles: ["user"] }`
- **Error Responses:**
  - 400 Bad Request: Validation errors (weak password, invalid email format)
  - 409 Conflict: Email already registered
- **Traces to:** FR-AUTH-002

### API-003: GET `/auth/me`

- **Auth Required:** Yes (Bearer token in Authorization header)
- **Rate Limit:** 60 req/min per user
- **Description:** Returns authenticated user's `UserProfile`. Requires valid JWT accessToken from `JwtService`.
- **Request Headers:** `Authorization: Bearer <accessToken>`
- **Response (200):** `UserProfile` — `{ id, email, displayName, createdAt, updatedAt, lastLoginAt, roles }`
- **Error Responses:**
  - 401 Unauthorized: Missing, expired, or invalid accessToken
- **Traces to:** FR-AUTH-004

### API-004: POST `/auth/refresh`

- **Auth Required:** No (refresh token in body)
- **Rate Limit:** 30 req/min per user
- **Description:** Exchange valid refresh token for new `AuthToken` pair via `TokenManager`. Old refresh token revoked.
- **Request Body:** `{ refreshToken: string }`
- **Response (200):** `AuthToken` — `{ accessToken, refreshToken, expiresIn: 900, tokenType: "Bearer" }`
- **Error Responses:**
  - 401 Unauthorized: Expired or revoked refresh token
- **Traces to:** FR-AUTH-003

### API-005: POST `/auth/reset-request`

- **Auth Required:** No
- **Rate Limit:** Not specified (gap)
- **Description:** Initiates password reset flow. Sends email with reset token if email is registered. Returns success regardless to prevent enumeration.
- **Request Body:** `{ email: string }` (inferred)
- **Response:** Success confirmation (inferred)
- **Note:** **Endpoint referenced in FR-AUTH-005 but not detailed in TDD §8.** Specification gap.
- **Traces to:** FR-AUTH-005 (step 1)

### API-006: POST `/auth/reset-confirm`

- **Auth Required:** No
- **Rate Limit:** Not specified (gap)
- **Description:** Validates reset token and updates password hash via `PasswordHasher`. Token is single-use with 1-hour expiry.
- **Request Body:** `{ token: string, newPassword: string }` (inferred)
- **Response:** Success confirmation (inferred)
- **Note:** **Endpoint referenced in FR-AUTH-005 but not detailed in TDD §8.** Specification gap.
- **Traces to:** FR-AUTH-005 (step 2)

### API Governance

- **Versioning:** URL prefix (`/v1/auth/*` in production)
- **Breaking changes:** Require new major version
- **Non-breaking additions:** Permitted within current version (new optional fields)
- **Error format:** Consistent JSON structure: `{ error: { code, message, status } }`

---

## Component Inventory

### COMP-001: AuthService

- **Type:** Backend Service (orchestrator)
- **Location:** Core service layer
- **Description:** Primary facade receiving requests from API Gateway. Orchestrates all auth flows: login, registration, profile retrieval, password reset.
- **Dependencies:** COMP-002 (TokenManager), COMP-004 (PasswordHasher), COMP-005 (UserRepo)

### COMP-002: TokenManager

- **Type:** Backend Service (token lifecycle)
- **Location:** Core service layer
- **Description:** Manages JWT access/refresh token lifecycle. Issues, validates, refreshes, and revokes tokens. Stores refresh tokens as hashed values in Redis.
- **Dependencies:** COMP-003 (JwtService), Redis

### COMP-003: JwtService

- **Type:** Backend Service (token signing)
- **Location:** Nested within TokenManager
- **Description:** Signs and verifies JWT tokens using RS256 with 2048-bit RSA keys. 5-second clock skew tolerance. Keys rotated quarterly.
- **Dependencies:** RSA key pair

### COMP-004: PasswordHasher

- **Type:** Backend Service (cryptography)
- **Location:** Core service layer
- **Description:** Abstraction over bcrypt with configurable cost factor (set to 12). Handles password hashing and verification. Designed for future algorithm migration.
- **Dependencies:** bcryptjs library

### COMP-005: UserRepo

- **Type:** Backend Repository (data access)
- **Location:** Data layer
- **Description:** Data access layer for `UserProfile` persistence in PostgreSQL. Connection pooling via pg-pool.
- **Dependencies:** PostgreSQL 15+

### COMP-006: LoginPage

- **Type:** Frontend Page Component
- **Location:** Route `/login`
- **Auth Required:** No
- **Props:** `onSuccess: () => void, redirectUrl?: string`
- **Description:** Renders email/password login form. Handles submission to `AuthService` login endpoint. Stores `AuthToken` via `AuthProvider`.
- **Dependencies:** COMP-009 (AuthProvider)

### COMP-007: RegisterPage

- **Type:** Frontend Page Component
- **Location:** Route `/register`
- **Auth Required:** No
- **Props:** `onSuccess: () => void, termsUrl: string`
- **Description:** Renders registration form with email, password, displayName fields. Validates password strength client-side before calling `AuthService`.
- **Dependencies:** COMP-009 (AuthProvider)

### COMP-008: ProfilePage

- **Type:** Frontend Page Component
- **Location:** Route `/profile`
- **Auth Required:** Yes
- **Description:** Displays `UserProfile` data via GET `/auth/me`.
- **Dependencies:** COMP-009 (AuthProvider)

### COMP-009: AuthProvider

- **Type:** Frontend Context Provider
- **Location:** Wraps entire application
- **Props:** `children: ReactNode`
- **Description:** Context provider managing `AuthToken` state. Handles silent refresh via `TokenManager`. Exposes `UserProfile` and auth methods. Intercepts 401 responses, triggers token refresh, redirects unauthenticated users.
- **Dependencies:** API-001, API-003, API-004

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

---

## Testing Strategy

### TEST-001: Login with valid credentials returns AuthToken (Unit)

- **Level:** Unit
- **Component:** `AuthService`
- **Tools:** Jest, ts-jest
- **Validates:** FR-AUTH-001 — `AuthService.login()` calls `PasswordHasher.verify()`, then `TokenManager.issueTokens()`, returns valid `AuthToken` with accessToken and refreshToken.
- **Input:** Valid email and password
- **Expected Output:** `AuthToken` with both tokens populated
- **Mocks:** `PasswordHasher.verify()` returns true, `TokenManager.issueTokens()` returns mock token pair

### TEST-002: Login with invalid credentials returns error (Unit)

- **Level:** Unit
- **Component:** `AuthService`
- **Tools:** Jest, ts-jest
- **Validates:** FR-AUTH-001 — `AuthService.login()` returns 401 when `PasswordHasher.verify()` returns false; no `AuthToken` is issued.
- **Input:** Valid email, incorrect password
- **Expected Output:** 401 error response
- **Mocks:** `PasswordHasher.verify()` returns false

### TEST-003: Token refresh with valid refresh token (Unit)

- **Level:** Unit
- **Component:** `TokenManager`
- **Tools:** Jest, ts-jest
- **Validates:** FR-AUTH-003 — `TokenManager.refresh()` validates the refresh token, revokes old token, issues new `AuthToken` pair via `JwtService`.
- **Input:** Valid refresh token
- **Expected Output:** New `AuthToken` pair; old refresh token revoked
- **Mocks:** Redis lookup returns valid token record

### TEST-004: Registration persists UserProfile to database (Integration)

- **Level:** Integration
- **Scope:** `AuthService` + PostgreSQL
- **Tools:** Supertest, testcontainers
- **Validates:** FR-AUTH-002 — full flow from API request through `PasswordHasher` to database insert.
- **Input:** Valid registration payload
- **Expected Output:** `UserProfile` persisted in PostgreSQL; 201 response with profile data

### TEST-005: Expired refresh token rejected by TokenManager (Integration)

- **Level:** Integration
- **Scope:** `TokenManager` + Redis
- **Tools:** Supertest, testcontainers
- **Validates:** FR-AUTH-003 — Redis TTL expiration correctly invalidates refresh tokens.
- **Input:** Expired refresh token
- **Expected Output:** 401 response

### TEST-006: User registers and logs in (E2E)

- **Level:** E2E
- **Flow:** `RegisterPage` → `LoginPage` → ProfilePage
- **Tools:** Playwright
- **Validates:** FR-AUTH-001, FR-AUTH-002 — complete user journey through `AuthProvider`.
- **Input:** New user registration data, then login credentials
- **Expected Output:** Successful registration, successful login, profile page displays correct data

### Test Pyramid Summary

| Level | Coverage Target | Tools | Focus |
|-------|----------------|-------|-------|
| Unit | 80% | Jest, ts-jest | `AuthService`, `PasswordHasher`, `JwtService`, `TokenManager`, `UserProfile` validation |
| Integration | 15% | Supertest, testcontainers | API endpoint cycles, DB operations, Redis token storage |
| E2E | 5% | Playwright | Full user journeys through frontend components |

### Test Environments

| Environment | Purpose | Data |
|-------------|---------|------|
| Local | Developer testing | Docker Compose with PostgreSQL and Redis containers |
| CI | Automated pipeline | testcontainers for ephemeral databases |
| Staging | Pre-production validation | Seeded test accounts, isolated from production |

---

## Migration and Rollout Plan

### MIG-001: Phase 1 — Internal Alpha

- **Description:** Deploy `AuthService` to staging. auth-team and QA test all endpoints. `LoginPage` and `RegisterPage` available behind feature flag `AUTH_NEW_LOGIN`.
- **Duration:** 1 week
- **Dependencies:** All FR-AUTH-001 through FR-AUTH-005 implemented
- **Success Criteria:** All functional requirements pass manual testing. Zero P0/P1 bugs.
- **Rollback:** Disable `AUTH_NEW_LOGIN` flag.

### MIG-002: Phase 2 — Beta (10%)

- **Description:** Enable `AUTH_NEW_LOGIN` for 10% of traffic. Monitor `AuthService` latency, error rates, and `TokenManager` Redis usage. `AuthProvider` handles token refresh under real load.
- **Duration:** 2 weeks
- **Dependencies:** MIG-001 completed successfully
- **Success Criteria:** p95 latency < 200ms. Error rate < 0.1%. No `TokenManager` Redis connection failures.
- **Rollback:** Disable `AUTH_NEW_LOGIN` flag.

### MIG-003: Phase 3 — General Availability (100%)

- **Description:** Remove feature flag `AUTH_NEW_LOGIN`. All users route through new `AuthService`. Legacy auth endpoints deprecated. `AUTH_TOKEN_REFRESH` flag enables refresh token flow.
- **Duration:** 1 week
- **Dependencies:** MIG-002 completed successfully
- **Success Criteria:** 99.9% uptime over first 7 days. All monitoring dashboards green.
- **Rollback:** Re-enable legacy auth endpoints.

### MIG-004: Feature Flag — AUTH_NEW_LOGIN

- **Purpose:** Gates access to new `LoginPage` and `AuthService` login endpoint
- **Default:** OFF
- **Removal Target:** After Phase 3 GA

### MIG-005: Feature Flag — AUTH_TOKEN_REFRESH

- **Purpose:** Enables refresh token flow in `TokenManager`; when OFF, only access tokens are issued
- **Default:** OFF
- **Removal Target:** After Phase 3 + 2 weeks

### MIG-006: Rollback Procedure

- **Steps:**
  1. Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth
  2. Verify legacy login flow is operational via smoke tests
  3. Investigate `AuthService` failure root cause using structured logs and traces
  4. If data corruption detected in `UserProfile` table, restore from last known-good backup
  5. Notify auth-team and platform-team via incident channel
  6. Post-mortem within 48 hours of rollback
- **Rollback Triggers:**
  - p95 latency exceeds 1000ms for more than 5 minutes
  - Error rate exceeds 5% for more than 2 minutes
  - `TokenManager` Redis connection failures exceed 10 per minute
  - Any data loss or corruption detected in `UserProfile` records

---

## Operational Readiness

### OPS-001: Runbook — AuthService Down

- **Symptoms:** 5xx errors on all `/auth/*` endpoints; `LoginPage` and `RegisterPage` show error state.
- **Diagnosis:** Check `AuthService` pod health in Kubernetes. Verify PostgreSQL connectivity. Check `PasswordHasher` and `TokenManager` initialization logs.
- **Resolution:** Restart `AuthService` pods. If PostgreSQL unreachable, failover to read replica. If Redis down, `TokenManager` rejects refresh requests — users must re-login via `LoginPage`.
- **Escalation:** Page auth-team on-call. If unresolved in 15 minutes, escalate to platform-team.
- **Prevention:** Health check monitoring, pod auto-restart policies, database connection pooling.

### OPS-002: Runbook — Token Refresh Failures

- **Symptoms:** Users report unexpected logouts; `AuthProvider` enters redirect loop to `LoginPage`; `auth_token_refresh_total` error counter spikes.
- **Diagnosis:** Check Redis connectivity from `TokenManager`. Verify `JwtService` signing key accessible. Check `AUTH_TOKEN_REFRESH` feature flag state.
- **Resolution:** If Redis degraded, scale Redis cluster. If `JwtService` key unavailable, re-mount secrets volume. If feature flag OFF, enable `AUTH_TOKEN_REFRESH`.
- **Escalation:** Page auth-team on-call. If Redis cluster issue, escalate to platform-team.
- **Prevention:** Redis cluster monitoring, secrets rotation validation, feature flag auditing.

### OPS-003: On-Call Expectations

- **Response time:** Acknowledge P1 alerts within 15 minutes.
- **Coverage:** auth-team provides 24/7 on-call rotation during first 2 weeks post-GA.
- **Tooling:** Kubernetes dashboards, Grafana monitoring, Redis CLI, PostgreSQL admin.
- **Escalation path:** auth-team on-call → test-lead → eng-manager → platform-team.
- **Knowledge prerequisites:** Familiarity with `AuthService` architecture, JWT token lifecycle, Redis operations, PostgreSQL administration.

### OPS-004: Capacity Planning — AuthService Pods

- **Resource:** `AuthService` Kubernetes pods
- **Current Capacity:** 3 replicas
- **Expected Load:** 500 concurrent users
- **Scaling Plan:** HPA scales to 10 replicas based on CPU > 70%.

### OPS-005: Capacity Planning — PostgreSQL Connections

- **Resource:** PostgreSQL connection pool
- **Current Capacity:** 100 pool size
- **Expected Load:** 50 avg concurrent queries
- **Scaling Trigger:** Increase pool to 200 if connection wait time > 50ms.

### OPS-006: Capacity Planning — Redis Memory

- **Resource:** Redis memory
- **Current Capacity:** 1 GB
- **Expected Load:** ~100K refresh tokens (~50 MB)
- **Scaling Trigger:** Scale to 2 GB if memory utilization > 70%.

### Observability Summary

- **Metrics (Prometheus):** `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter)
- **Tracing:** OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`
- **Logging:** Structured logs for all auth events (login success/failure, registration, token refresh, password reset)
- **Alerts:**
  - Login failure rate > 20% over 5 minutes
  - p95 latency > 500ms
  - `TokenManager` Redis connection failures
