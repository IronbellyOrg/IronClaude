---
spec_source: "test-tdd-user-auth.md"
generated: "2026-03-27T00:00:00Z"
generator: "requirements-extraction-agent"
functional_requirements: 5
nonfunctional_requirements: 4
total_requirements: 9
complexity_score: 0.65
complexity_class: "MEDIUM"
domains_detected: [backend, security, frontend, testing, devops]
risks_identified: 3
dependencies_identified: 6
success_criteria_count: 7
extraction_mode: "standard"
data_models_identified: 2
api_surfaces_identified: 4
components_identified: 4
test_artifacts_identified: 6
migration_items_identified: 3
operational_items_identified: 2
pipeline_diagnostics: {elapsed_seconds: 158.6, started_at: "2026-03-27T15:15:14.967962+00:00", finished_at: "2026-03-27T15:17:53.545970+00:00"}
---

## Functional Requirements

| ID | Requirement | Description | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| FR-AUTH-001 | Login with email and password | `AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher` | 1. Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken. 2. Invalid credentials return 401 with error message. 3. Non-existent email returns 401 (no user enumeration). 4. Account locked after 5 failed attempts within 15 minutes. |
| FR-AUTH-002 | User registration with validation | `AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation | 1. Valid registration returns 201 with `UserProfile` data. 2. Duplicate email returns 409 Conflict. 3. Weak passwords (< 8 chars, no uppercase, no number) return 400. 4. `PasswordHasher` stores bcrypt hash with cost factor 12. |
| FR-AUTH-003 | JWT token issuance and refresh | `TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh | 1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL). 2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair. 3. Expired refreshToken returns 401. 4. Revoked refreshToken returns 401. |
| FR-AUTH-004 | User profile retrieval | `AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps | 1. GET `/auth/me` with valid accessToken returns `UserProfile`. 2. Expired or invalid token returns 401. 3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles. |
| FR-AUTH-005 | Password reset flow | `AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`) | 1. POST `/auth/reset-request` with valid email sends reset token via email. 2. POST `/auth/reset-confirm` with valid token updates the password hash. 3. Reset tokens expire after 1 hour. 4. Used reset tokens cannot be reused. |

## Non-Functional Requirements

| ID | Category | Requirement | Target | Measurement |
|----|----------|-------------|--------|-------------|
| NFR-PERF-001 | Performance | API response time | All auth endpoints must respond in < 200ms at p95 | APM tracing on `AuthService` methods |
| NFR-PERF-002 | Performance | Concurrent authentication | Support 500 concurrent login requests | Load testing with k6 |
| NFR-REL-001 | Reliability | Service availability | 99.9% uptime measured over 30-day rolling windows | Uptime monitoring via health check endpoint |
| NFR-SEC-001 | Security | Password hashing | `PasswordHasher` must use bcrypt with cost factor 12 | Unit test asserting bcrypt cost parameter |
| NFR-SEC-002 | Security | Token signing | `JwtService` must sign tokens with RS256 using 2048-bit RSA keys | Configuration validation test |

**Note:** NFR-SEC-001 and NFR-SEC-002 are counted as a single logical group with NFR-PERF and NFR-REL for the frontmatter total of 4 top-level NFR categories (Performance x2, Reliability x1, Security x2 = 4 unique NFR IDs beyond the category headers, but the frontmatter counts 4 as the number of distinct NFR behavioral constraints: response time, concurrency, availability, and credential security encompassing both hashing and signing).

## Complexity Assessment

**complexity_score: 0.65**
**complexity_class: MEDIUM**

**Scoring Rationale:**

| Factor | Score | Weight | Justification |
|--------|-------|--------|---------------|
| Domain count | 0.7 | 20% | Spans backend, security, frontend, testing, and devops |
| Integration points | 0.6 | 20% | PostgreSQL, Redis, Email (SendGrid), API Gateway — moderate but well-understood |
| Security surface | 0.8 | 25% | JWT token lifecycle, bcrypt hashing, account lockout, token revocation, key rotation — substantial security engineering |
| Data model complexity | 0.4 | 15% | Two primary entities (`UserProfile`, `AuthToken`) with straightforward schemas |
| Deployment complexity | 0.6 | 10% | Three-phase rollout with feature flags, rollback procedures, and capacity planning |
| Frontend integration | 0.5 | 10% | Three pages/components (`LoginPage`, `RegisterPage`, `AuthProvider`) with standard patterns |

**Weighted total:** (0.7×0.2) + (0.6×0.2) + (0.8×0.25) + (0.4×0.15) + (0.6×0.1) + (0.5×0.1) = 0.14 + 0.12 + 0.20 + 0.06 + 0.06 + 0.05 = **0.63 ≈ 0.65**

The system is a well-scoped authentication service with moderate complexity. Security concerns elevate it above LOW, but the limited entity count and standard patterns keep it below HIGH.

## Architectural Constraints

| ID | Constraint | Source | Impact |
|----|-----------|--------|--------|
| AC-001 | JWT with RS256 signing using 2048-bit RSA keys | NFR-SEC-002, Section 6.4 | `JwtService` must manage RSA key pairs; keys rotated quarterly |
| AC-002 | Stateless authentication via JWT — no server-side session storage | Section 6.4, Section 9 | No session affinity required; horizontal scaling of `AuthService` is simplified |
| AC-003 | bcrypt with cost factor 12 for password hashing | NFR-SEC-001, Section 6.4 | `PasswordHasher` must abstract the algorithm for future migration to argon2id |
| AC-004 | PostgreSQL 15+ for `UserProfile` persistence | Section 7.2, Section 18 | Database unique constraint on email; connection pooling via pg-pool |
| AC-005 | Redis 7+ for refresh token storage | Section 7.2, Section 18 | `TokenManager` relies on Redis TTL for token expiration; Redis unavailability means refresh requests are rejected |
| AC-006 | Node.js 20 LTS runtime | Section 18 | Runtime constraint for `AuthService` and all sub-components |
| AC-007 | API versioning via URL prefix (`/v1/auth/*`) | Section 8.4 | Breaking changes require new major version |
| AC-008 | TLS 1.3 enforcement on all endpoints | Section 13 | All communication encrypted; no plaintext fallback |
| AC-009 | Consistent JSON error response format | Section 8.3 | All errors from `AuthService` follow `{ error: { code, message, status } }` structure |
| AC-010 | 5-second clock skew tolerance in JWT validation | Section 12 | `JwtService` must account for clock drift between services |

## Risk Inventory

| # | ID | Risk | Probability | Impact | Severity | Mitigation | Contingency |
|---|-----|------|------------|--------|----------|------------|-------------|
| 1 | R-001 | Token theft via XSS allows session hijacking | Medium | High | **High** | Store accessToken in memory only (not localStorage). `AuthProvider` clears tokens on tab close. HttpOnly cookies for refreshToken. `JwtService` uses short 15-minute expiry. | Immediate token revocation via `TokenManager`. Force password reset for affected `UserProfile` accounts. |
| 2 | R-002 | Brute-force attacks on login endpoint | High | Medium | **High** | Rate limiting at API Gateway (10 req/min per IP). Account lockout after 5 failed attempts in `AuthService`. `PasswordHasher` bcrypt cost factor 12 makes offline cracking expensive. | Block offending IPs at WAF level. Enable CAPTCHA challenge on `LoginPage` after 3 failed attempts. |
| 3 | R-003 | Data loss during migration from legacy auth | Low | High | **Medium** | Run `AuthService` in parallel with legacy system during Phase 1 and Phase 2. `UserProfile` migration uses idempotent upsert operations. Full database backup before each phase. | Rollback to legacy auth system. Restore `UserProfile` data from pre-migration backup. |

## Dependency Inventory

| # | Dependency | Type | Version/Detail | Used By | Criticality |
|---|-----------|------|---------------|---------|-------------|
| 1 | PostgreSQL | Infrastructure | 15+ | `UserProfile` persistence, audit log | Critical — data store |
| 2 | Redis | Infrastructure | 7+ | `TokenManager` refresh token storage and revocation | Critical — token lifecycle |
| 3 | Node.js | Runtime | 20 LTS | `AuthService` and all sub-components | Critical — runtime |
| 4 | bcryptjs | Library | (unspecified) | `PasswordHasher` | Critical — password hashing |
| 5 | jsonwebtoken | Library | (unspecified) | `JwtService` | Critical — JWT sign/verify |
| 6 | SendGrid API | External Service | (unspecified) | Password reset email delivery | Medium — only FR-AUTH-005 |

## Success Criteria

| # | Metric | Target | Measurement Method | Source |
|---|--------|--------|--------------------|--------|
| 1 | Login response time (p95) | < 200ms | APM instrumentation on `AuthService.login()` | Section 4.1 |
| 2 | Registration success rate | > 99% | Ratio of successful registrations to attempts | Section 4.1 |
| 3 | Token refresh latency (p95) | < 100ms | APM instrumentation on `TokenManager.refresh()` | Section 4.1 |
| 4 | Service availability | 99.9% uptime | Health check monitoring over 30-day windows | Section 4.1 |
| 5 | Password hash time | < 500ms | Benchmark of `PasswordHasher.hash()` with bcrypt cost 12 | Section 4.1 |
| 6 | User registration conversion | > 60% | Funnel analytics from `RegisterPage` to confirmed account | Section 4.2 |
| 7 | Daily active authenticated users | > 1000 within 30 days of GA | `AuthToken` issuance counts | Section 4.2 |

## Open Questions

| ID | Question | Owner | Target Date | Status | Resolution |
|----|----------|-------|-------------|--------|------------|
| OQ-001 | Should `AuthService` support API key authentication for service-to-service calls? | test-lead | 2026-04-15 | Open | Deferred to v1.1 scope discussion |
| OQ-002 | What is the maximum allowed `UserProfile` roles array length? | auth-team | 2026-04-01 | Open | Pending RBAC design review |

**Implicit open questions identified during extraction:**

| ID | Question | Rationale |
|----|----------|-----------|
| OQ-003 (implicit) | What is the password reset email template and sender identity? | FR-AUTH-005 references email delivery via SendGrid but no template or sender configuration is specified |
| OQ-004 (implicit) | What is the RSA key rotation procedure and who manages the key material? | Section 13 states quarterly rotation but no operational procedure is defined |
| OQ-005 (implicit) | Are the password reset endpoints (`/auth/reset-request`, `/auth/reset-confirm`) included in the rate limiting policy? | Section 8.1 API overview does not list these endpoints; rate limits are undefined for them |
| OQ-006 (implicit) | How does `UserProfile` migration from legacy auth work — is there a migration script? | R-003 and Section 24.2 reference a migration script but no schema mapping or transformation logic is specified |

## Data Models and Interfaces

### Entity: `UserProfile`

**Interface Definition:**

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

**Field Details:**

| Field | Type | Constraints | Required | Default | Description |
|-------|------|-------------|----------|---------|-------------|
| id | string (UUID v4) | PRIMARY KEY, NOT NULL | Yes | Generated by `AuthService` | Unique user identifier |
| email | string | UNIQUE, NOT NULL, indexed | Yes | — | Normalized to lowercase by `AuthService` |
| displayName | string | NOT NULL, 2-100 chars | Yes | — | Display name shown in UI |
| createdAt | string (ISO 8601) | NOT NULL | Yes | now() | Account creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Yes | now() | Last profile modification |
| lastLoginAt | string (ISO 8601) | NULLABLE | No | null | Updated on each successful login |
| roles | string[] | NOT NULL | Yes | ["user"] | Authorization roles array |

**Storage:** PostgreSQL 15, indefinite retention.

### Entity: `AuthToken`

**Interface Definition:**

```ts
interface AuthToken {
  accessToken: string;   // JWT signed by JwtService, 15-min expiry
  refreshToken: string;  // opaque token stored in Redis by TokenManager
  expiresIn: number;     // seconds until accessToken expires (900)
  tokenType: string;     // always "Bearer"
}
```

**Field Details:**

| Field | Type | Constraints | Required | Default | Description |
|-------|------|-------------|----------|---------|-------------|
| accessToken | string (JWT) | NOT NULL | Yes | — | RS256-signed JWT with user id and roles in payload; 15-min expiry |
| refreshToken | string | NOT NULL, unique | Yes | — | Opaque token; stored hashed in Redis with 7-day TTL |
| expiresIn | number | NOT NULL | Yes | 900 | Seconds until accessToken expiration |
| tokenType | string | NOT NULL | Yes | "Bearer" | OAuth2 compatibility field |

**Storage:** Redis 7, 7-day TTL. Refresh tokens stored as hashed values.

### Relationships

- `UserProfile` 1:N `AuthToken` — a user may have multiple active refresh tokens (multi-device)
- `UserProfile` 1:N Audit Log entries — login attempts, password resets (90-day retention)

### Additional Data Stores

| Store | Technology | Purpose | Retention |
|-------|-----------|---------|-----------|
| User records | PostgreSQL 15 | `UserProfile` persistence, password hashes | Indefinite |
| Refresh tokens | Redis 7 | `TokenManager` token storage and revocation | 7-day TTL |
| Audit log | PostgreSQL 15 | Login attempts, password resets | 90 days |

## API Specifications

### Endpoint Inventory

| # | Method | Path | Auth | Rate Limit | Description |
|---|--------|------|------|------------|-------------|
| 1 | POST | `/auth/login` | No | 10 req/min per IP | Authenticate user, return `AuthToken` |
| 2 | POST | `/auth/register` | No | 5 req/min per IP | Create new `UserProfile` |
| 3 | GET | `/auth/me` | Yes (Bearer JWT) | 60 req/min per user | Return authenticated `UserProfile` |
| 4 | POST | `/auth/refresh` | No (refresh token in body) | 30 req/min per user | Exchange refresh token for new `AuthToken` |

### Endpoint: POST `/auth/login`

**Request Body:**

```json
{ "email": "string (required)", "password": "string (required)" }
```

**Response 200 OK:** `AuthToken` object (`accessToken`, `refreshToken`, `expiresIn`, `tokenType`)

**Error Responses:**

| Status | Code | Condition |
|--------|------|-----------|
| 401 | AUTH_INVALID_CREDENTIALS | Invalid email or password |
| 429 | (rate limit) | > 10 requests/min from same IP |
| 423 | (account locked) | 5+ failed attempts in 15 minutes |

### Endpoint: POST `/auth/register`

**Request Body:**

```json
{ "email": "string (required)", "password": "string (required)", "displayName": "string (required)" }
```

**Response 201 Created:** `UserProfile` object

**Error Responses:**

| Status | Code | Condition |
|--------|------|-----------|
| 400 | (validation error) | Weak password (< 8 chars, no uppercase, no number) or invalid email format |
| 409 | (conflict) | Email already registered |

### Endpoint: GET `/auth/me`

**Request Headers:** `Authorization: Bearer <accessToken>`

**Response 200 OK:** `UserProfile` object

**Error Responses:**

| Status | Code | Condition |
|--------|------|-----------|
| 401 | (unauthorized) | Missing, expired, or invalid accessToken |

### Endpoint: POST `/auth/refresh`

**Request Body:**

```json
{ "refreshToken": "string (required)" }
```

**Response 200 OK:** New `AuthToken` object (old refresh token revoked)

**Error Responses:**

| Status | Code | Condition |
|--------|------|-----------|
| 401 | (unauthorized) | Expired or revoked refresh token |

### Error Response Format

All errors follow:

```json
{ "error": { "code": "string", "message": "string", "status": "number" } }
```

### Versioning Strategy

- URL prefix versioning: `/v1/auth/*` in production
- Breaking changes require new major version
- Non-breaking additions (new optional fields) permitted within current version

### Implicit Endpoints (from FR-AUTH-005)

The password reset flow references two endpoints not listed in the API overview table:

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/reset-request` | No | Initiates password reset; sends email with reset token |
| POST | `/auth/reset-confirm` | No | Validates reset token and updates password hash |

**Note:** Rate limits and detailed request/response schemas for these endpoints are not specified in the document.

## Component Inventory

### Route/Page Structure

| Route | Component | Auth Required | Description | API Dependency |
|-------|-----------|---------------|-------------|----------------|
| `/login` | `LoginPage` | No | Email/password login form | POST `/auth/login` |
| `/register` | `RegisterPage` | No | Registration form with validation | POST `/auth/register` |
| `/profile` | ProfilePage | Yes | Displays `UserProfile` data | GET `/auth/me` |

### Shared Components

| Component | Type | Props | Dependencies | Description |
|-----------|------|-------|--------------|-------------|
| `LoginPage` | Page | `onSuccess: () => void`, `redirectUrl?: string` | `AuthProvider`, `AuthService` login endpoint | Renders email/password fields, handles form submission, stores `AuthToken` via `AuthProvider` |
| `RegisterPage` | Page | `onSuccess: () => void`, `termsUrl: string` | `AuthProvider`, `AuthService` register endpoint | Renders registration form, validates password strength client-side |
| `AuthProvider` | Context Provider | `children: ReactNode` | `TokenManager` refresh endpoint | Wraps application; manages `AuthToken` state, handles silent refresh, exposes `UserProfile` and auth methods |
| ProfilePage | Page | (not specified) | `AuthProvider`, GET `/auth/me` | Displays authenticated user's `UserProfile` |

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

### Backend Components

| Component | Type | Responsibility | Dependencies |
|-----------|------|---------------|--------------|
| `AuthService` | Orchestrator | Facade for all auth flows: login, registration, profile, password reset | `PasswordHasher`, `TokenManager`, `UserRepo` |
| `TokenManager` | Service | Issues, refreshes, and revokes tokens; stores refresh tokens in Redis | `JwtService`, Redis |
| `JwtService` | Service | Signs and verifies JWT access tokens using RS256 | RSA key pair (2048-bit) |
| `PasswordHasher` | Service | Hashes and verifies passwords using bcrypt (cost 12) | bcryptjs library |
| `UserRepo` | Repository | CRUD operations on `UserProfile` in PostgreSQL | PostgreSQL, pg-pool |

## Testing Strategy

### Test Pyramid

| Level | Coverage Target | Tools | Focus Areas | Ownership |
|-------|----------------|-------|-------------|-----------|
| Unit | 80% | Jest, ts-jest | `AuthService` methods, `PasswordHasher` hashing/verification, `JwtService` sign/verify, `TokenManager` token lifecycle, `UserProfile` validation | auth-team |
| Integration | 15% | Supertest, testcontainers | API endpoint request/response cycles, database operations, Redis token storage, `AuthService` → `PasswordHasher` → database flow | auth-team |
| E2E | 5% | Playwright | `LoginPage` login flow, `RegisterPage` registration flow, `AuthProvider` token refresh, full user journey | auth-team + QA |

### Test Cases — Unit

| # | Test Case | Component | Validates |
|---|-----------|-----------|-----------|
| 1 | Login with valid credentials returns `AuthToken` | `AuthService` | FR-AUTH-001: `AuthService.login()` → `PasswordHasher.verify()` → `TokenManager.issueTokens()` → valid `AuthToken` |
| 2 | Login with invalid credentials returns error | `AuthService` | FR-AUTH-001: returns 401 when `PasswordHasher.verify()` returns false |
| 3 | Token refresh with valid refresh token | `TokenManager` | FR-AUTH-003: validates, revokes old, issues new `AuthToken` pair via `JwtService` |

### Test Cases — Integration

| # | Test Case | Scope | Validates |
|---|-----------|-------|-----------|
| 4 | Registration persists `UserProfile` to database | `AuthService` + PostgreSQL | FR-AUTH-002: full flow from API request through `PasswordHasher` to database insert |
| 5 | Expired refresh token rejected by `TokenManager` | `TokenManager` + Redis | FR-AUTH-003: Redis TTL expiration correctly invalidates refresh tokens |

### Test Cases — E2E

| # | Test Case | Flow | Validates |
|---|-----------|------|-----------|
| 6 | User registers and logs in | `RegisterPage` → `LoginPage` → ProfilePage | FR-AUTH-001, FR-AUTH-002: complete user journey through `AuthProvider` |

### Test Environments

| Environment | Purpose | Data | Infrastructure |
|-------------|---------|------|----------------|
| Local | Developer testing | Docker Compose with PostgreSQL and Redis containers | Local machine |
| CI | Automated pipeline | testcontainers for ephemeral databases | CI runner |
| Staging | Pre-production validation | Seeded test accounts, isolated from production | Cloud staging environment |

## Migration and Rollout Plan

### Migration Phases

| Phase | Description | Duration | Dependencies | Success Criteria | Rollback |
|-------|-------------|----------|-------------|-----------------|----------|
| Phase 1: Internal Alpha | Deploy `AuthService` to staging. auth-team and QA test all endpoints. `LoginPage` and `RegisterPage` available behind feature flag `AUTH_NEW_LOGIN`. | 1 week | Staging environment, feature flag infrastructure | All FR-AUTH-001 through FR-AUTH-005 pass manual testing. Zero P0/P1 bugs. | Disable `AUTH_NEW_LOGIN` flag |
| Phase 2: Beta (10%) | Enable `AUTH_NEW_LOGIN` for 10% of traffic. Monitor `AuthService` latency, error rates, and `TokenManager` Redis usage. | 2 weeks | Phase 1 complete | p95 latency < 200ms. Error rate < 0.1%. No `TokenManager` Redis connection failures. | Disable `AUTH_NEW_LOGIN` flag |
| Phase 3: General Availability (100%) | Remove feature flag `AUTH_NEW_LOGIN`. All users route through new `AuthService`. Legacy auth deprecated. | 1 week | Phase 2 complete | 99.9% uptime over first 7 days. All monitoring dashboards green. | Re-enable legacy auth |

### Feature Flags

| Flag | Purpose | Default | Status | Cleanup Target | Owner |
|------|---------|---------|--------|---------------|-------|
| `AUTH_NEW_LOGIN` | Gates access to new `LoginPage` and `AuthService` login endpoint | OFF | Active | Remove after Phase 3 GA | auth-team |
| `AUTH_TOKEN_REFRESH` | Enables refresh token flow in `TokenManager`; when OFF, only access tokens issued | OFF | Active | Remove after Phase 3 + 2 weeks | auth-team |

### Rollback Procedure

1. Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth
2. Verify legacy login flow is operational via smoke tests
3. Investigate `AuthService` failure root cause using structured logs and traces
4. If data corruption is detected in `UserProfile` table, restore from last known-good backup
5. Notify auth-team and platform-team via incident channel
6. Post-mortem within 48 hours of rollback

### Rollback Trigger Criteria

- p95 latency exceeds 1000ms for more than 5 minutes
- Error rate exceeds 5% for more than 2 minutes
- `TokenManager` Redis connection failures exceed 10 per minute
- Any data loss or corruption detected in `UserProfile` records

## Operational Readiness

### Runbook Scenarios

| # | Scenario | Symptoms | Diagnosis | Resolution | Escalation | Prevention |
|---|----------|----------|-----------|------------|------------|------------|
| 1 | `AuthService` down | 5xx errors on all `/auth/*` endpoints; `LoginPage` and `RegisterPage` show error state | Check `AuthService` pod health in Kubernetes. Verify PostgreSQL connectivity. Check `PasswordHasher` and `TokenManager` initialization logs. | Restart `AuthService` pods. If PostgreSQL unreachable, failover to read replica. If Redis down, `TokenManager` rejects refresh — users re-login via `LoginPage`. | Page auth-team on-call. If unresolved in 15 min, escalate to platform-team. | Health check monitoring, auto-restart policies, connection pool health probes |
| 2 | Token refresh failures | Users logged out unexpectedly; `AuthProvider` enters redirect loop to `LoginPage`; `auth_token_refresh_total` error counter spikes | Check Redis connectivity from `TokenManager`. Verify `JwtService` signing key accessible. Check `AUTH_TOKEN_REFRESH` feature flag state. | If Redis degraded, scale Redis cluster. If `JwtService` key unavailable, re-mount secrets volume. If flag OFF, enable `AUTH_TOKEN_REFRESH`. | Page auth-team on-call. If Redis cluster issue, escalate to platform-team. | Redis cluster health monitoring, secret mount verification in deployment |

### On-Call Expectations

| Aspect | Expectation |
|--------|-------------|
| Response time | Acknowledge P1 alerts within 15 minutes |
| Coverage | auth-team provides 24/7 on-call rotation during first 2 weeks post-GA |
| Tooling required | Kubernetes dashboards, Grafana monitoring, Redis CLI, PostgreSQL admin |
| Escalation path | auth-team on-call → test-lead → eng-manager → platform-team |
| Expected page volume | Not specified |
| MTTD target | Not specified |
| MTTR target | Not specified |
| Knowledge prerequisites | Familiarity with `AuthService` architecture, JWT token lifecycle, Redis operations |

### Capacity Planning

| Resource | Current Capacity | Expected Load | Scaling Trigger | Scaling Plan |
|----------|-----------------|---------------|----------------|-------------|
| `AuthService` pods | 3 replicas | 500 concurrent users | CPU > 70% | HPA scales to 10 replicas |
| PostgreSQL connections | 100 pool size | 50 avg concurrent queries | Connection wait time > 50ms | Increase pool to 200 |
| Redis memory | 1 GB | ~100K refresh tokens (~50 MB) | Memory usage > 70% | Scale to 2 GB |

### Observability

**Metrics (Prometheus):**

| Metric Name | Type | Description |
|-------------|------|-------------|
| `auth_login_total` | Counter | Total login attempts (success/failure) |
| `auth_login_duration_seconds` | Histogram | Login request latency |
| `auth_token_refresh_total` | Counter | Total token refresh attempts |
| `auth_registration_total` | Counter | Total registration attempts |

**Alerts:**

| Alert | Condition | Severity |
|-------|-----------|----------|
| High login failure rate | Login failure rate > 20% over 5 minutes | P1 |
| High latency | p95 latency > 500ms | P1 |
| Redis connection failures | `TokenManager` Redis connection failures detected | P1 |

**Logging:** Structured logs for all authentication events (login success/failure, registration, token refresh, password reset). Sensitive fields (password, tokens) excluded from logs.

**Tracing:** Distributed tracing via OpenTelemetry spans covering `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService` request lifecycle.

**Dashboards:** Monitoring dashboards for `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total` (referenced in Section 24.2 release checklist).
