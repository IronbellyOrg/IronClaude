---
spec_source: "test-tdd-user-auth.md"
generated: "2026-04-02T12:00:00Z"
generator: "requirements-design-extraction-agent"
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.55
complexity_class: "MEDIUM"
domains_detected: [backend, security, frontend, testing, devops]
risks_identified: 7
dependencies_identified: 8
success_criteria_count: 10
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 4
components_identified: 9
test_artifacts_identified: 6
migration_items_identified: 15
operational_items_identified: 9
pipeline_diagnostics: {elapsed_seconds: 327.2, started_at: "2026-04-03T02:33:31.077677+00:00", finished_at: "2026-04-03T02:38:58.282043+00:00"}
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
- **PRD Trace:** FR-AUTH.1, Epic AUTH-E1

### FR-AUTH-002: User registration with validation

- **Description:** `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation.
- **Components:** `AuthService`, `PasswordHasher`, `UserRepo`
- **Acceptance Criteria:**
  1. Valid registration returns 201 with `UserProfile` data.
  2. Duplicate email returns 409 Conflict.
  3. Weak passwords (< 8 chars, no uppercase, no number) return 400.
  4. `PasswordHasher` stores bcrypt hash with cost factor 12.
- **PRD Trace:** FR-AUTH.2, Epic AUTH-E1

### FR-AUTH-003: JWT token issuance and refresh

- **Description:** `TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh.
- **Components:** `TokenManager`, `JwtService`, Redis
- **Acceptance Criteria:**
  1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL).
  2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair.
  3. Expired refreshToken returns 401.
  4. Revoked refreshToken returns 401.
- **PRD Trace:** FR-AUTH.3, Epic AUTH-E2

### FR-AUTH-004: User profile retrieval

- **Description:** `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps.
- **Components:** `AuthService`, `UserRepo`
- **Acceptance Criteria:**
  1. GET `/auth/me` with valid accessToken returns `UserProfile`.
  2. Expired or invalid token returns 401.
  3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.
- **PRD Trace:** FR-AUTH.4, Epic AUTH-E3

### FR-AUTH-005: Password reset flow

- **Description:** `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`).
- **Components:** `AuthService`, `PasswordHasher`, Email Service (SendGrid)
- **Acceptance Criteria:**
  1. POST `/auth/reset-request` with valid email sends reset token via email.
  2. POST `/auth/reset-confirm` with valid token updates the password hash.
  3. Reset tokens expire after 1 hour.
  4. Used reset tokens cannot be reused.
- **PRD Trace:** FR-AUTH.5, Epic AUTH-E3

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

### NFR-COMP-001: GDPR consent at registration (from PRD S17)

- **Category:** Compliance
- **Requirement:** Users must consent to data collection at registration. Consent recorded with timestamp.
- **Standard:** GDPR
- **PRD Source:** Legal & Compliance Requirements

### NFR-COMP-002: SOC2 audit logging (from PRD S17)

- **Category:** Compliance
- **Requirement:** All auth events logged with user ID, timestamp, IP, and outcome. 12-month retention.
- **Standard:** SOC2 Type II
- **PRD Source:** Legal & Compliance Requirements
- **Note:** TDD Section 14 defines Prometheus metrics and structured logs, but does not explicitly specify 12-month retention or IP logging. This PRD requirement adds specificity.

### NFR-COMP-003: NIST password storage (from PRD S17)

- **Category:** Compliance
- **Requirement:** One-way adaptive hashing. Raw passwords never persisted or logged.
- **Standard:** NIST SP 800-63B
- **PRD Source:** Legal & Compliance Requirements
- **Note:** Aligns with NFR-SEC-001 (bcrypt cost 12) but adds the explicit NIST compliance framing.

### NFR-COMP-004: GDPR data minimization (from PRD S17)

- **Category:** Compliance
- **Requirement:** Only email, hashed password, and display name collected. No additional PII required.
- **Standard:** GDPR
- **PRD Source:** Legal & Compliance Requirements

---

## Complexity Assessment

- **Complexity Score:** 0.55
- **Complexity Class:** MEDIUM

**Scoring Rationale:**

| Factor | Score | Rationale |
|--------|-------|-----------|
| Architectural scope | 0.5 | Single backend service with clear component boundaries (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`). Well-defined facade pattern. |
| Data model complexity | 0.3 | Two primary entities (`UserProfile`, `AuthToken`) with straightforward schemas. No complex relationships. |
| Integration surface | 0.6 | Three external systems (PostgreSQL, Redis, SendGrid). Connection pooling and failover required. |
| Security surface | 0.8 | Cryptographic operations (bcrypt, RS256 JWT), token lifecycle management, brute-force mitigation, XSS prevention. Security-critical domain. |
| Frontend scope | 0.4 | Three page components (`LoginPage`, `RegisterPage`, ProfilePage) plus `AuthProvider` context. Standard form/auth patterns. |
| Rollout complexity | 0.6 | Three-phase rollout with feature flags, rollback criteria, and parallel legacy operation. |
| Testing breadth | 0.5 | Standard test pyramid with unit, integration, and E2E. Requires testcontainers for database/cache integration tests. |

**Overall:** MEDIUM complexity. The security-critical nature elevates risk, but the architectural pattern (single service, well-known auth flows) is well-understood. No novel algorithms or unproven technologies.

---

## Architectural Constraints

1. **Stateless authentication:** JWT-based via `JwtService`. No server-side session state. Refresh tokens in Redis are the only server-side state.
2. **Facade pattern:** `AuthService` is the sole orchestrator. All auth logic is accessed through this component — no direct calls to `PasswordHasher`, `TokenManager`, or `JwtService` from external consumers.
3. **Technology mandates:** PostgreSQL 15+, Redis 7+, Node.js 20 LTS. No alternatives without architecture review.
4. **Token lifecycle:** Access tokens are 15-minute JWTs signed with RS256. Refresh tokens are 7-day opaque tokens stored in Redis. Dual-token pattern is mandatory.
5. **Password hashing algorithm:** bcrypt via `PasswordHasher` with cost factor 12. The `PasswordHasher` abstraction exists to enable future migration to argon2id without API changes.
6. **API versioning:** URL prefix versioning (`/v1/auth/*`). Breaking changes require new major version.
7. **Error response format:** Consistent JSON structure with `error.code`, `error.message`, `error.status`.
8. **No user enumeration:** Login failures and password reset requests for unknown emails must return identical responses.
9. **Persona-driven design requirements (from PRD S7):**
   - **Alex (end user):** Registration must complete in under 60 seconds. Session persistence across page refreshes without re-login.
   - **Jordan (admin):** Auth event logs must be queryable by date range and user. Account lock/unlock capability required.
   - **Sam (API consumer):** Programmatic token refresh without user interaction. Clear error codes for automation.
10. **Scope boundaries (from PRD S12):** OAuth/OIDC, MFA, RBAC, and social login are explicitly out of scope for v1.0. Designs must not introduce dependencies on these capabilities.

---

## Risk Inventory

1. **R-001 — Token theft via XSS (Severity: HIGH)**
   - Probability: Medium | Impact: High
   - Mitigation: Store accessToken in memory only (not localStorage). `AuthProvider` clears tokens on tab close. HttpOnly cookies for refreshToken. `JwtService` uses short 15-minute expiry.
   - Contingency: Immediate token revocation via `TokenManager`. Force password reset for affected accounts.

2. **R-002 — Brute-force attacks on login endpoint (Severity: HIGH)**
   - Probability: High | Impact: Medium
   - Mitigation: Rate limiting at API Gateway (10 req/min per IP). Account lockout after 5 failed attempts. bcrypt cost factor 12.
   - Contingency: Block offending IPs at WAF. Enable CAPTCHA on `LoginPage` after 3 failed attempts.

3. **R-003 — Data loss during migration from legacy auth (Severity: HIGH)**
   - Probability: Low | Impact: High
   - Mitigation: Run `AuthService` in parallel with legacy during Phase 1 and 2. Idempotent upsert operations. Full database backup before each phase.
   - Contingency: Rollback to legacy. Restore from pre-migration backup.

4. **R-004 — Low registration adoption due to poor UX (Severity: HIGH, from PRD)**
   - Probability: Medium | Impact: High
   - Mitigation: Usability testing before launch; iterate based on funnel data.

5. **R-005 — Security breach from implementation flaws (Severity: CRITICAL, from PRD)**
   - Probability: Low | Impact: Critical
   - Mitigation: Dedicated security review; penetration testing before production.

6. **R-006 — Compliance failure from incomplete audit logging (Severity: HIGH, from PRD)**
   - Probability: Medium | Impact: High
   - Mitigation: Define log requirements early; validate against SOC2 controls in QA.

7. **R-007 — Email delivery failures blocking password reset (Severity: MEDIUM, from PRD)**
   - Probability: Low | Impact: Medium
   - Mitigation: Delivery monitoring and alerting; fallback support channel.

---

## Dependency Inventory

| # | Dependency | Type | Version | Purpose | Impact if Unavailable |
|---|-----------|------|---------|---------|----------------------|
| 1 | PostgreSQL | Infrastructure | 15+ | `UserProfile` persistence, password hashes, audit log | No user storage; service non-functional |
| 2 | Redis | Infrastructure | 7+ | Refresh token storage and revocation by `TokenManager` | Token refresh unavailable; users must re-login |
| 3 | Node.js | Runtime | 20 LTS | Service runtime | Service cannot run |
| 4 | bcryptjs | Library | — | Password hashing in `PasswordHasher` | Cannot hash or verify passwords |
| 5 | jsonwebtoken | Library | — | JWT sign/verify in `JwtService` | Cannot issue or validate tokens |
| 6 | SendGrid | External Service | API | Password reset emails | Password reset flow blocked (FR-AUTH-005) |
| 7 | SEC-POLICY-001 | Policy Document | — | Password and token security requirements | Policy non-compliance risk |
| 8 | Frontend routing framework | Internal | — | Rendering `LoginPage`, `RegisterPage`, ProfilePage | Auth pages cannot render |

---

## Success Criteria

| # | Metric | Target | Source | Measurement Method |
|---|--------|--------|--------|-------------------|
| 1 | Login response time (p95) | < 200ms | TDD S4.1 | APM instrumentation on `AuthService.login()` |
| 2 | Registration success rate | > 99% | TDD S4.1 | Ratio of successful registrations to attempts |
| 3 | Token refresh latency (p95) | < 100ms | TDD S4.1 | APM instrumentation on `TokenManager.refresh()` |
| 4 | Service availability | 99.9% uptime | TDD S4.1 | Health check monitoring over 30-day windows |
| 5 | Password hash time | < 500ms | TDD S4.1 | Benchmark of `PasswordHasher.hash()` with bcrypt cost 12 |
| 6 | User registration conversion | > 60% | TDD S4.2 / PRD S19 | Funnel analytics from `RegisterPage` to confirmed account |
| 7 | Daily active authenticated users | > 1000 within 30 days of GA | TDD S4.2 | `AuthToken` issuance counts |
| 8 | Average session duration | > 30 minutes | PRD S19 | Token refresh event analytics |
| 9 | Failed login rate | < 5% of attempts | PRD S19 | Auth event log analysis |
| 10 | Password reset completion | > 80% | PRD S19 | Funnel: reset requested -> new password set |

---

## Open Questions

| # | ID | Question | Owner | Target Date | Status | Source |
|---|-----|---------|-------|-------------|--------|--------|
| 1 | OQ-001 | Should `AuthService` support API key authentication for service-to-service calls? | test-lead | 2026-04-15 | Open | TDD S22 |
| 2 | OQ-002 | What is the maximum allowed `UserProfile` roles array length? | auth-team | 2026-04-01 | Open | TDD S22 |
| 3 | OQ-003 | Should password reset emails be sent synchronously or asynchronously? | Engineering | — | Open | PRD S13 |
| 4 | OQ-004 | Maximum number of refresh tokens allowed per user across devices? | Product | — | Open | PRD S13 |
| 5 | OQ-005 | Should the platform support "remember me" to extend session duration? | Product | — | Open | PRD S13 |
| 6 | OQ-006 | PRD JTBD #4 (programmatic token refresh for integrations) is covered by FR-AUTH-003, but no explicit service-to-service auth mechanism exists. Does Sam (API consumer) persona require API key auth beyond JWT? | Product / Engineering | — | Open | PRD S6/S7 gap |
| 7 | OQ-007 | PRD user story for Jordan (admin) requires auth event log querying and account lock/unlock. The TDD defines account lockout (FR-AUTH-001 AC4) but no admin unlock endpoint or log query API. Is an admin API in scope for v1.0? | Product / Engineering | — | Open | PRD S20 gap |
| 8 | OQ-008 | PRD specifies logout functionality (AUTH-E1 user story) but the TDD does not define a logout endpoint. Is POST `/auth/logout` needed for v1.0, or is client-side token deletion sufficient? | Engineering | — | Open | PRD/TDD gap |

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
| email | string | UNIQUE, NOT NULL, indexed | Yes | User email, normalized to lowercase |
| displayName | string | NOT NULL, 2-100 chars | Yes | Display name shown in UI |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Yes | Account creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Yes | Last profile modification timestamp |
| lastLoginAt | string (ISO 8601) | NULLABLE | No | Updated on each successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Yes | Authorization roles; enforced downstream |

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
| accessToken | string (JWT) | NOT NULL | Yes | Signed by `JwtService` using RS256; contains user id and roles |
| refreshToken | string | NOT NULL, unique | Yes | Opaque token; stored in Redis with 7-day TTL |
| expiresIn | number | NOT NULL | Yes | Seconds until accessToken expiration; always 900 |
| tokenType | string | NOT NULL | Yes | Always "Bearer"; OAuth2 compatibility |

### Entity Relationships

- `AuthService.login()` validates credentials via `PasswordHasher`, then creates an `AuthToken` via `TokenManager`/`JwtService`.
- `UserProfile` is persisted in PostgreSQL; `AuthToken.refreshToken` is stored in Redis.
- `AuthToken.accessToken` JWT payload contains `UserProfile.id` and `UserProfile.roles`.

### Data Storage Strategy

| Store | Technology | Purpose | Retention |
|-------|-----------|---------|-----------|
| User records | PostgreSQL 15 | `UserProfile` persistence, password hashes | Indefinite |
| Refresh tokens | Redis 7 | Token storage and revocation | 7-day TTL |
| Audit log | PostgreSQL 15 | Login attempts, password resets | 90 days (TDD) / 12 months (PRD NFR-COMP-002) |

**Note:** TDD specifies 90-day audit log retention, but PRD compliance requirement (NFR-COMP-002) requires 12-month retention for SOC2. The PRD wins on this business constraint — audit log retention should be 12 months.

---

## API Specifications

### Endpoint Inventory

| # | Method | Path | Auth | Rate Limit | Description |
|---|--------|------|------|------------|-------------|
| 1 | POST | `/auth/login` | No | 10 req/min per IP | Authenticate user, return `AuthToken` |
| 2 | POST | `/auth/register` | No | 5 req/min per IP | Create `UserProfile`, return profile data |
| 3 | GET | `/auth/me` | Bearer token | 60 req/min per user | Return authenticated user's `UserProfile` |
| 4 | POST | `/auth/refresh` | No (refresh token in body) | 30 req/min per user | Exchange refresh token for new `AuthToken` |

### POST `/auth/login`

- **Auth:** None
- **Rate Limit:** 10 req/min per IP
- **Request Body:**
  ```json
  { "email": "string", "password": "string" }
  ```
- **Response 200:** `AuthToken` object (`accessToken`, `refreshToken`, `expiresIn`, `tokenType`)
- **Error Responses:**
  - 401 `AUTH_INVALID_CREDENTIALS` — Invalid email or password
  - 423 Locked — Account locked after 5 failed attempts
  - 429 Too Many Requests — Rate limit exceeded

### POST `/auth/register`

- **Auth:** None
- **Rate Limit:** 5 req/min per IP
- **Request Body:**
  ```json
  { "email": "string", "password": "string", "displayName": "string" }
  ```
- **Response 201:** `UserProfile` object
- **Error Responses:**
  - 400 Bad Request — Validation errors (weak password, invalid email)
  - 409 Conflict — Email already registered

### GET `/auth/me`

- **Auth:** Bearer token (Authorization header)
- **Rate Limit:** 60 req/min per user
- **Request Headers:** `Authorization: Bearer <accessToken>`
- **Response 200:** `UserProfile` object
- **Error Responses:**
  - 401 Unauthorized — Missing, expired, or invalid accessToken

### POST `/auth/refresh`

- **Auth:** None (refresh token in body)
- **Rate Limit:** 30 req/min per user
- **Request Body:**
  ```json
  { "refreshToken": "string" }
  ```
- **Response 200:** New `AuthToken` object (old refresh token revoked)
- **Error Responses:**
  - 401 Unauthorized — Expired or revoked refresh token

### Error Response Schema

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "status": "number"
  }
}
```

### Versioning Strategy

URL prefix versioning: `/v1/auth/*` in production. Breaking changes require a new major version. Non-breaking additions (new optional fields) permitted within current version.

---

## Component Inventory

### Backend Components

| Component | Type | Purpose | Dependencies |
|-----------|------|---------|-------------|
| `AuthService` | Service (Facade) | Orchestrates all auth flows | `PasswordHasher`, `TokenManager`, `UserRepo` |
| `TokenManager` | Service | JWT token lifecycle, refresh token storage | `JwtService`, Redis |
| `JwtService` | Service | JWT sign/verify with RS256 | RSA key pair (2048-bit) |
| `PasswordHasher` | Service | bcrypt hash/verify abstraction | bcryptjs library |
| `UserRepo` | Repository | `UserProfile` CRUD operations | PostgreSQL |

### Frontend Components

| Component | Type | Props | Description |
|-----------|------|-------|-------------|
| `LoginPage` | Page | `onSuccess: () => void`, `redirectUrl?: string` | Email/password login form; calls POST `/auth/login` |
| `RegisterPage` | Page | `onSuccess: () => void`, `termsUrl: string` | Registration form with client-side validation |
| ProfilePage | Page | — | Displays `UserProfile`; calls GET `/auth/me` |
| `AuthProvider` | Context Provider | `children: ReactNode` | Manages `AuthToken` state, silent refresh, exposes auth methods |

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

---

## Testing Strategy

### Test Pyramid

| Level | Coverage Target | Tools | Focus Areas |
|-------|----------------|-------|-------------|
| Unit | 80% | Jest, ts-jest | `AuthService` methods, `PasswordHasher` hashing/verification, `JwtService` sign/verify, `TokenManager` token lifecycle, `UserProfile` validation |
| Integration | 15% | Supertest, testcontainers | API endpoint cycles, database operations, Redis token storage, `AuthService`-to-`PasswordHasher`-to-database flow |
| E2E | 5% | Playwright | `LoginPage` login flow, `RegisterPage` registration flow, `AuthProvider` token refresh, full user journey |

### Unit Test Cases

| ID | Test Case | Component | Validates |
|----|-----------|-----------|-----------|
| UT-001 | Login with valid credentials returns `AuthToken` | `AuthService` | FR-AUTH-001: login -> `PasswordHasher.verify()` -> `TokenManager.issueTokens()` |
| UT-002 | Login with invalid credentials returns error | `AuthService` | FR-AUTH-001: returns 401 when `PasswordHasher.verify()` returns false |
| UT-003 | Token refresh with valid refresh token | `TokenManager` | FR-AUTH-003: validates, revokes old, issues new `AuthToken` pair |

### Integration Test Cases

| ID | Test Case | Scope | Validates |
|----|-----------|-------|-----------|
| IT-001 | Registration persists `UserProfile` to database | `AuthService` + PostgreSQL | FR-AUTH-002: full flow through `PasswordHasher` to database |
| IT-002 | Expired refresh token rejected | `TokenManager` + Redis | FR-AUTH-003: Redis TTL correctly invalidates tokens |

### E2E Test Cases

| ID | Test Case | Flow | Validates |
|----|-----------|------|-----------|
| E2E-001 | User registers and logs in | `RegisterPage` -> `LoginPage` -> ProfilePage | FR-AUTH-001, FR-AUTH-002: complete journey through `AuthProvider` |

### Test Environments

| Environment | Purpose | Data |
|-------------|---------|------|
| Local | Developer testing | Docker Compose with PostgreSQL and Redis |
| CI | Automated pipeline | testcontainers for ephemeral databases |
| Staging | Pre-production validation | Seeded test accounts, isolated from production |

---

## Migration and Rollout Plan

### Migration Phases

| Phase | Description | Duration | Dependencies | Success Criteria | Rollback |
|-------|-------------|----------|-------------|-----------------|----------|
| Phase 1: Internal Alpha | Deploy `AuthService` to staging. auth-team and QA test all endpoints. `LoginPage` and `RegisterPage` behind `AUTH_NEW_LOGIN` flag. | 1 week | Staging environment, PostgreSQL, Redis | All FR-AUTH-001 through FR-AUTH-005 pass manual testing. Zero P0/P1 bugs. | Disable `AUTH_NEW_LOGIN` flag |
| Phase 2: Beta (10%) | Enable `AUTH_NEW_LOGIN` for 10% of traffic. Monitor latency, error rates, Redis usage. | 2 weeks | Phase 1 complete | p95 latency < 200ms. Error rate < 0.1%. No Redis connection failures. | Disable `AUTH_NEW_LOGIN` flag |
| Phase 3: GA (100%) | Remove `AUTH_NEW_LOGIN` flag. All users route through `AuthService`. Legacy deprecated. `AUTH_TOKEN_REFRESH` enables refresh flow. | 1 week | Phase 2 complete | 99.9% uptime over 7 days. All dashboards green. | Re-enable legacy auth |

### Feature Flags

| Flag | Purpose | Default | Cleanup Target |
|------|---------|---------|---------------|
| `AUTH_NEW_LOGIN` | Gates access to new `LoginPage` and `AuthService` login endpoint | OFF | Remove after Phase 3 GA |
| `AUTH_TOKEN_REFRESH` | Enables refresh token flow in `TokenManager` | OFF | Remove after Phase 3 + 2 weeks |

### Rollback Procedure

1. Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth.
2. Verify legacy login flow is operational via smoke tests.
3. Investigate `AuthService` failure root cause using structured logs and traces.
4. If data corruption detected in `UserProfile` table, restore from last known-good backup.
5. Notify auth-team and platform-team via incident channel.
6. Post-mortem within 48 hours of rollback.

### Rollback Criteria

Rollback is triggered if any of the following occur:
- p95 latency exceeds 1000ms for more than 5 minutes
- Error rate exceeds 5% for more than 2 minutes
- `TokenManager` Redis connection failures exceed 10 per minute
- Any data loss or corruption detected in `UserProfile` records

---

## Operational Readiness

### Runbook Scenarios

| # | Scenario | Symptoms | Diagnosis | Resolution | Escalation | Prevention |
|---|----------|----------|-----------|------------|------------|------------|
| 1 | `AuthService` down | 5xx errors on all `/auth/*` endpoints; `LoginPage`/`RegisterPage` show error state | Check pod health in Kubernetes. Verify PostgreSQL connectivity. Check `PasswordHasher`/`TokenManager` init logs. | Restart pods. If PostgreSQL unreachable, failover to read replica. If Redis down, `TokenManager` rejects refreshes — users re-login via `LoginPage`. | Page auth-team on-call. 15-min escalation to platform-team. | Health check monitoring, auto-restart policies |
| 2 | Token refresh failures | Users logged out unexpectedly; `AuthProvider` redirect loop to `LoginPage`; `auth_token_refresh_total` error counter spikes | Check Redis connectivity from `TokenManager`. Verify `JwtService` signing key. Check `AUTH_TOKEN_REFRESH` flag state. | Scale Redis cluster if degraded. Re-mount secrets volume if key unavailable. Enable `AUTH_TOKEN_REFRESH` if OFF. | Page auth-team on-call. Redis issues escalate to platform-team. | Redis cluster monitoring, key rotation alerts |

### On-Call Expectations

| Aspect | Expectation |
|--------|-------------|
| Response time | Acknowledge P1 alerts within 15 minutes |
| Coverage | auth-team 24/7 rotation during first 2 weeks post-GA |
| Tooling | Kubernetes dashboards, Grafana, Redis CLI, PostgreSQL admin |
| Escalation path | auth-team on-call -> test-lead -> eng-manager -> platform-team |

### Capacity Planning

| Resource | Current Capacity | Expected Load | Scaling Trigger |
|----------|-----------------|---------------|----------------|
| `AuthService` pods | 3 replicas | 500 concurrent users | HPA scales to 10 replicas at CPU > 70% |
| PostgreSQL connections | 100 pool size | 50 avg concurrent queries | Increase to 200 if wait time > 50ms |
| Redis memory | 1 GB | ~100K refresh tokens (~50 MB) | Scale to 2 GB if > 70% utilized |

### Observability

**Metrics (Prometheus):**
- `auth_login_total` (counter) — login attempts
- `auth_login_duration_seconds` (histogram) — login latency
- `auth_token_refresh_total` (counter) — token refresh operations
- `auth_registration_total` (counter) — registration attempts

**Alerts:**
- Login failure rate > 20% over 5 minutes
- p95 latency > 500ms
- `TokenManager` Redis connection failures

**Tracing:** OpenTelemetry spans across `AuthService` -> `PasswordHasher` -> `TokenManager` -> `JwtService`.

**Logging:** Structured logs for all authentication events (login success/failure, registration, token refresh, password reset).
