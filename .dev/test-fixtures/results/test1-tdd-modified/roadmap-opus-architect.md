---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.65
primary_persona: architect
---

# Project Roadmap: User Authentication Service

## 1. Executive Summary

This roadmap delivers a stateless JWT-based authentication service (`AuthService`) with email/password login, user registration, token refresh, profile retrieval, and password reset capabilities. The system spans five domains (backend, security, frontend, testing, devops) at **MEDIUM complexity (0.65)**, driven primarily by the security surface area (JWT lifecycle, bcrypt hashing, account lockout, token revocation).

The implementation is organized into **four phases** over approximately **7–8 weeks**, progressing from infrastructure and core security primitives through API development, frontend integration, and a three-stage rollout (alpha → 10% beta → GA). Six external dependencies (PostgreSQL 15+, Redis 7+, Node.js 20 LTS, bcryptjs, jsonwebtoken, SendGrid) must be provisioned, and three identified risks (XSS token theft, brute-force attacks, migration data loss) are mitigated through architectural controls and phased deployment.

All nine requirements (FR-AUTH-001 through FR-AUTH-005, NFR-PERF-001, NFR-PERF-002, NFR-REL-001, NFR-SEC-001/NFR-SEC-002) are addressed with explicit phase assignments and validation criteria.

---

## 2. Phased Implementation Plan

### Phase 1: Foundation & Security Primitives (Weeks 1–2)

**Objective:** Establish infrastructure, data models, and core security components that all subsequent work depends on.

**Milestone:** `PasswordHasher`, `JwtService`, `UserRepo`, and `TokenManager` pass unit tests against local PostgreSQL and Redis.

#### 1.1 Infrastructure Provisioning

- [ ] Provision PostgreSQL 15+ with connection pooling (pg-pool, 100 initial pool size) — supports AC-004
- [ ] Provision Redis 7+ with 1 GB memory allocation — supports AC-005
- [ ] Configure Node.js 20 LTS runtime environment — supports AC-006
- [ ] Generate RSA 2048-bit key pair for JWT signing; store in secrets management — supports AC-001
- [ ] Set up Docker Compose for local dev (PostgreSQL + Redis containers) — supports test environment "Local"
- [ ] Configure TLS 1.3 termination — supports AC-008

#### 1.2 Data Model Implementation

- [ ] Create `UserProfile` table schema in PostgreSQL:
  - `id` (UUID v4, PK), `email` (UNIQUE, indexed, NOT NULL), `displayName` (NOT NULL, 2–100 chars), `password_hash` (NOT NULL), `createdAt`, `updatedAt`, `lastLoginAt` (nullable), `roles` (string array, default `["user"]`)
  - Unique constraint on `email` (lowercase normalized)
- [ ] Create audit log table (login attempts, password resets; 90-day retention policy)
- [ ] Implement `UserRepo` — CRUD operations on `UserProfile` via pg-pool

#### 1.3 Security Primitives

- [ ] Implement `PasswordHasher` — bcrypt hashing with cost factor 12, abstracted interface for future argon2id migration — satisfies NFR-SEC-001, AC-003
- [ ] Implement `JwtService` — RS256 signing/verification with 2048-bit RSA keys, 5-second clock skew tolerance — satisfies NFR-SEC-002, AC-001, AC-010
- [ ] Implement `TokenManager` — issues access tokens (15-min expiry) and refresh tokens (7-day TTL in Redis as hashed values), supports revocation — supports FR-AUTH-003

#### 1.4 Integration Points — Dispatch/Wiring Mechanisms

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| `AuthService` facade | Orchestrator/Facade | `PasswordHasher`, `TokenManager`, `UserRepo`, `JwtService` | Phase 1 (skeleton), Phase 2 (full wiring) | Phase 2 (API routes), Phase 3 (frontend) |
| `TokenManager` → Redis binding | Service → Infrastructure | Redis client connection, `JwtService` for access token signing | Phase 1 | Phase 2 (refresh endpoint), Phase 4 (monitoring) |
| `TokenManager` → `JwtService` delegation | Service → Service | `JwtService.sign()`, `JwtService.verify()` | Phase 1 | Phase 2, Phase 3 |
| `PasswordHasher` abstraction layer | Strategy pattern | bcryptjs (current), argon2id (future) | Phase 1 | Phase 2 (login, registration, password reset) |
| `UserRepo` → pg-pool binding | Repository → Connection Pool | PostgreSQL connection pool configuration | Phase 1 | Phase 2 (all user operations) |

#### 1.5 Unit Tests (Phase 1)

- [ ] Test `PasswordHasher.hash()` produces bcrypt hash with cost factor 12 — validates NFR-SEC-001
- [ ] Test `PasswordHasher.verify()` correctly validates passwords
- [ ] Test `JwtService.sign()` produces RS256-signed JWT — validates NFR-SEC-002
- [ ] Test `JwtService.verify()` rejects expired tokens and accepts valid tokens with ≤5s clock skew
- [ ] Test `TokenManager.issueTokens()` returns `AuthToken` with correct TTLs
- [ ] Test `TokenManager` stores hashed refresh tokens in Redis with 7-day TTL
- [ ] Benchmark `PasswordHasher.hash()` completes in < 500ms — validates Success Criterion #5

**Deliverables:** Working security primitives, data layer, infrastructure. All unit tests green.

---

### Phase 2: API Development & Core Auth Flows (Weeks 3–4)

**Objective:** Wire `AuthService` facade and implement all API endpoints with full error handling, rate limiting, and account lockout.

**Milestone:** All four primary endpoints and two password reset endpoints pass integration tests. p95 response time < 200ms on local.

#### 2.1 AuthService Orchestrator Wiring

- [ ] Wire `AuthService` as facade over `PasswordHasher`, `TokenManager`, `UserRepo` — completes the `AuthService` facade dispatch mechanism from Phase 1
- [ ] Implement consistent JSON error format: `{ error: { code, message, status } }` — satisfies AC-009
- [ ] Configure API versioning: all routes under `/v1/auth/*` — satisfies AC-007

#### 2.2 Endpoint Implementation

- [ ] **POST `/v1/auth/login`** — satisfies FR-AUTH-001
  - Validate email/password against `UserRepo` + `PasswordHasher`
  - Return `AuthToken` (200) or 401 (no user enumeration for missing emails)
  - Account lockout after 5 failed attempts in 15 minutes (423 response)
  - Rate limit: 10 req/min per IP
- [ ] **POST `/v1/auth/register`** — satisfies FR-AUTH-002
  - Email uniqueness validation (409 on duplicate)
  - Password strength: ≥ 8 chars, uppercase, number (400 on failure)
  - `PasswordHasher` stores bcrypt hash; `UserRepo` creates `UserProfile`
  - Rate limit: 5 req/min per IP
- [ ] **GET `/v1/auth/me`** — satisfies FR-AUTH-004
  - Bearer JWT authentication middleware
  - Returns `UserProfile` (id, email, displayName, roles, createdAt, updatedAt, lastLoginAt)
  - Rate limit: 60 req/min per user
- [ ] **POST `/v1/auth/refresh`** — satisfies FR-AUTH-003
  - Validates refresh token via `TokenManager`
  - Revokes old refresh token, issues new `AuthToken` pair
  - Rate limit: 30 req/min per user

#### 2.3 Password Reset Flow

- [ ] **POST `/v1/auth/reset-request`** — satisfies FR-AUTH-005 (step 1)
  - Generates time-limited reset token (1-hour expiry)
  - Sends email via SendGrid API
  - Note: email template and sender identity pending OQ-003 resolution
- [ ] **POST `/v1/auth/reset-confirm`** — satisfies FR-AUTH-005 (step 2)
  - Validates reset token (rejects expired/used tokens)
  - Updates password hash via `PasswordHasher`
  - Note: rate limits for these endpoints pending OQ-005 resolution

#### 2.4 Integration Points — Dispatch/Wiring Mechanisms

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| Express/Fastify route table | Route registry | `/v1/auth/login`, `/v1/auth/register`, `/v1/auth/me`, `/v1/auth/refresh`, `/v1/auth/reset-request`, `/v1/auth/reset-confirm` | Phase 2 | Phase 3 (frontend calls), Phase 4 (monitoring) |
| Rate limiting middleware chain | Middleware registry | Per-endpoint rate limits (10/5/60/30 req/min), account lockout logic | Phase 2 | Phase 2 (all endpoints), Phase 4 (monitoring alerts) |
| JWT authentication middleware | Middleware | `JwtService.verify()` bound to protected routes (`/auth/me`) | Phase 2 | Phase 3 (`AuthProvider` relies on 401 responses) |
| SendGrid email dispatch | External service binding | SendGrid API client wired into password reset handler | Phase 2 | Phase 2 (FR-AUTH-005 only) |
| Feature flag registry | Config mechanism | `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH` flags | Phase 2 (created) | Phase 4 (rollout gating) |

#### 2.5 Integration Tests

- [ ] Test case #4: Registration persists `UserProfile` to database — validates FR-AUTH-002 end-to-end
- [ ] Test case #5: Expired refresh token rejected by `TokenManager` via Redis TTL — validates FR-AUTH-003
- [ ] Test login → lockout after 5 failures → unlock after 15 minutes
- [ ] Test password reset request → email sent → confirm with valid token → password updated
- [ ] Test password reset with expired/reused token returns 401
- [ ] Configure testcontainers for CI environment (ephemeral PostgreSQL + Redis)

#### 2.6 Performance Validation

- [ ] Verify p95 login latency < 200ms — validates NFR-PERF-001, Success Criterion #1
- [ ] Verify p95 token refresh latency < 100ms — validates Success Criterion #3

**Deliverables:** All six endpoints functional, rate-limited, and integration-tested. Feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` created (OFF by default).

---

### Phase 3: Frontend Integration & E2E Testing (Weeks 5–6)

**Objective:** Build frontend components, wire them to the API, and validate the complete user journey.

**Milestone:** E2E tests pass for registration → login → profile view → silent refresh. All Success Criteria measurable.

#### 3.1 Frontend Components

- [ ] Implement `AuthProvider` (React Context) — manages `AuthToken` state, handles silent refresh via `/v1/auth/refresh`, exposes `UserProfile` and auth methods
  - Store `accessToken` in memory only (not localStorage) — mitigates R-001
  - Use HttpOnly cookies for `refreshToken` — mitigates R-001
  - Clear tokens on tab close — mitigates R-001
- [ ] Implement `LoginPage` — email/password form, calls POST `/v1/auth/login`, stores `AuthToken` via `AuthProvider`
  - Props: `onSuccess`, optional `redirectUrl`
- [ ] Implement `RegisterPage` — registration form with client-side password strength validation, calls POST `/v1/auth/register`
  - Props: `onSuccess`, `termsUrl`
- [ ] Implement `ProfilePage` — displays `UserProfile` from GET `/v1/auth/me`, requires authentication

#### 3.2 Route Structure & Component Hierarchy Wiring

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| React Router route table | Route registry | `/login` → `LoginPage`, `/register` → `RegisterPage`, `/profile` → `ProfilePage` | Phase 3 | Phase 3 (E2E tests), Phase 4 (feature flag gating) |
| `AuthProvider` context binding | Context/DI | `AuthProvider` wraps all routes; provides `AuthToken`, `UserProfile`, `login()`, `logout()`, `refresh()` methods | Phase 3 | Phase 3 (`LoginPage`, `RegisterPage`, `ProfilePage`), Phase 4 |
| Protected route guard | Middleware/HOC | Checks `AuthProvider` auth state; redirects unauthenticated users to `/login` | Phase 3 | Phase 3 (`ProfilePage`) |

#### 3.3 E2E Tests

- [ ] Test case #6: User registers on `RegisterPage` → logs in on `LoginPage` → views `ProfilePage` — validates FR-AUTH-001, FR-AUTH-002
- [ ] Test `AuthProvider` silent refresh: access token expires → automatic refresh → user remains authenticated — validates FR-AUTH-003
- [ ] Test failed login shows error; no user enumeration (same message for wrong email vs wrong password) — validates FR-AUTH-001 AC #3
- [ ] Configure Playwright for E2E test execution

#### 3.4 Load Testing

- [ ] k6 load test: 500 concurrent login requests — validates NFR-PERF-002
- [ ] Verify system handles load without degradation below p95 < 200ms — validates NFR-PERF-001

#### 3.5 Funnel Analytics

- [ ] Instrument `RegisterPage` → confirmed account funnel — supports Success Criterion #6 (> 60% conversion)
- [ ] Instrument `AuthToken` issuance counting — supports Success Criterion #7 (> 1000 DAU within 30 days of GA)

**Deliverables:** Frontend components wired and functional. E2E and load tests pass. All seven Success Criteria have measurement instrumentation in place.

---

### Phase 4: Observability, Migration & Rollout (Weeks 6–8)

**Objective:** Deploy observability stack, execute three-phase rollout, and achieve GA with 99.9% uptime.

**Milestone:** GA reached with all monitoring green, zero P0/P1 bugs, and rollback procedures verified.

#### 4.1 Observability Setup

- [ ] Configure Prometheus metrics:
  - `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter)
- [ ] Configure alerts:
  - Login failure rate > 20% over 5 min → P1
  - p95 latency > 500ms → P1
  - `TokenManager` Redis connection failures → P1
- [ ] Implement structured logging for all auth events (sensitive fields excluded)
- [ ] Configure OpenTelemetry tracing: `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`
- [ ] Build Grafana dashboards for auth metrics
- [ ] Implement health check endpoint — supports NFR-REL-001

#### 4.2 Deployment Configuration

- [ ] Configure Kubernetes HPA: 3 replicas baseline, scale to 10 at CPU > 70%
- [ ] Configure PostgreSQL connection pool: 100 initial, scale to 200 at wait time > 50ms
- [ ] Configure Redis memory: 1 GB initial, scale to 2 GB at > 70% usage

#### 4.3 Migration Preparation

- [ ] Develop `UserProfile` migration script from legacy auth — addresses R-003
  - Idempotent upsert operations
  - Schema mapping and transformation logic (pending OQ-006 resolution)
- [ ] Full database backup procedure documented and tested
- [ ] Parallel operation plan: new `AuthService` runs alongside legacy during Phase 1 and Phase 2 of rollout

#### 4.4 Integration Points — Dispatch/Wiring Mechanisms

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| Prometheus metrics registry | Metrics exporter | `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total` | Phase 4 | Phase 4 (Grafana dashboards, alerts) |
| Alert rules configuration | Alert binding | Three P1 rules wired to PagerDuty/incident channel | Phase 4 | Phase 4 (on-call) |
| OpenTelemetry trace pipeline | Tracing middleware | Spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService` | Phase 4 | Phase 4 (debugging, runbooks) |
| Feature flag controller | Rollout mechanism | `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` flags controlling traffic routing | Phase 2 (created) | Phase 4 (rollout gating, rollback) |

#### 4.5 Three-Phase Rollout

**Phase 4a — Internal Alpha (1 week):**
- [ ] Deploy to staging behind `AUTH_NEW_LOGIN` flag (OFF for public)
- [ ] auth-team and QA manually test all FR-AUTH-001 through FR-AUTH-005
- [ ] Gate: Zero P0/P1 bugs before proceeding

**Phase 4b — Beta 10% (2 weeks):**
- [ ] Enable `AUTH_NEW_LOGIN` for 10% of traffic
- [ ] Monitor: p95 latency < 200ms, error rate < 0.1%, no Redis connection failures from `TokenManager`
- [ ] Gate: All metrics within thresholds for full 2-week period

**Phase 4c — General Availability (1 week):**
- [ ] Remove `AUTH_NEW_LOGIN` feature flag — 100% traffic to new `AuthService`
- [ ] Deprecate legacy auth system
- [ ] Enable `AUTH_TOKEN_REFRESH` for all users
- [ ] Gate: 99.9% uptime over first 7 days — validates NFR-REL-001, Success Criterion #4
- [ ] Clean up `AUTH_TOKEN_REFRESH` flag 2 weeks post-GA

#### 4.6 Rollback Readiness

- [ ] Document and test rollback procedure:
  1. Disable `AUTH_NEW_LOGIN` → traffic routes to legacy
  2. Smoke test legacy login flow
  3. Root cause investigation via structured logs and traces
  4. If `UserProfile` data corruption: restore from backup
  5. Incident notification and 48-hour post-mortem
- [ ] Define rollback triggers:
  - p95 latency > 1000ms for > 5 minutes
  - Error rate > 5% for > 2 minutes
  - `TokenManager` Redis failures > 10/min
  - Any `UserProfile` data loss or corruption

#### 4.7 Operational Handoff

- [ ] Publish runbooks (Scenario 1: `AuthService` down, Scenario 2: token refresh failures)
- [ ] Establish auth-team 24/7 on-call rotation for first 2 weeks post-GA
- [ ] Acknowledge SLA: P1 alerts within 15 minutes

**Deliverables:** Full observability stack, successful GA rollout, operational runbooks, on-call rotation active.

---

## 3. Risk Assessment and Mitigation

| ID | Risk | Severity | Phase Addressed | Mitigation Strategy | Contingency |
|----|------|----------|----------------|---------------------|-------------|
| R-001 | Token theft via XSS | **High** | Phase 3 | `accessToken` stored in memory only (not localStorage). HttpOnly cookies for `refreshToken`. `AuthProvider` clears tokens on tab close. 15-minute access token expiry via `JwtService`. | Immediate token revocation via `TokenManager`. Force password reset for affected `UserProfile` accounts. |
| R-002 | Brute-force attacks on login | **High** | Phase 2 | Rate limiting at API Gateway (10 req/min per IP). Account lockout after 5 failed attempts in `AuthService`. bcrypt cost factor 12 makes offline cracking expensive. | Block IPs at WAF level. Enable CAPTCHA on `LoginPage` after 3 failed attempts. |
| R-003 | Data loss during legacy migration | **Medium** | Phase 4 | Parallel operation during alpha and beta. Idempotent upsert migration. Full database backup before each rollout phase. | Rollback to legacy auth. Restore `UserProfile` from pre-migration backup. |

**Architect-identified additional risks:**

| ID | Risk | Severity | Phase Addressed | Mitigation |
|----|------|----------|----------------|------------|
| R-004 (implicit) | RSA key compromise or rotation failure | Medium | Phase 1, Phase 4 | Key stored in secrets manager (not filesystem). Quarterly rotation procedure must be documented (OQ-004). Dual-key support during rotation window. |
| R-005 (implicit) | Redis single-point-of-failure for refresh tokens | Medium | Phase 1, Phase 4 | Redis unavailability degrades gracefully (users re-authenticate via `LoginPage`). Monitor Redis health. Consider Redis Sentinel/Cluster for HA. |
| R-006 (implicit) | SendGrid outage blocks password reset | Low | Phase 2 | FR-AUTH-005 is the only consumer. Queue reset emails for retry. Alert on SendGrid API failures. |

---

## 4. Resource Requirements and Dependencies

### External Dependencies

| Dependency | Phase Needed | Provisioning Lead Time | Risk if Delayed |
|---|---|---|---|
| PostgreSQL 15+ | Phase 1 (Week 1) | ~1 day (Docker local), ~1 week (managed cloud) | Blocks all data persistence work |
| Redis 7+ | Phase 1 (Week 1) | ~1 day (Docker local), ~1 week (managed cloud) | Blocks `TokenManager` implementation |
| Node.js 20 LTS | Phase 1 (Week 1) | Minimal | Blocks all backend work |
| bcryptjs | Phase 1 (Week 1) | npm install | Blocks `PasswordHasher` |
| jsonwebtoken | Phase 1 (Week 1) | npm install | Blocks `JwtService` |
| SendGrid API | Phase 2 (Week 3) | API key provisioning, ~2–5 days | Blocks FR-AUTH-005 only; non-critical path |

### Team Requirements

| Role | Phase(s) | Responsibility |
|---|---|---|
| Backend engineer (auth-team) | 1–4 | `AuthService`, `PasswordHasher`, `JwtService`, `TokenManager`, `UserRepo`, API endpoints |
| Frontend engineer (auth-team) | 3 | `LoginPage`, `RegisterPage`, `ProfilePage`, `AuthProvider` |
| QA engineer | 2–4 | Integration tests, E2E tests, manual testing during alpha |
| DevOps/SRE | 1, 4 | Infrastructure provisioning, Kubernetes config, observability, on-call |

### Open Questions Requiring Resolution

| ID | Question | Blocks | Target Date | Recommended Default |
|----|----------|--------|-------------|---------------------|
| OQ-001 | API key auth for service-to-service? | Nothing (deferred to v1.1) | 2026-04-15 | Exclude from scope |
| OQ-002 | Max `UserProfile` roles array length? | Phase 1 schema | 2026-04-01 | Set to 20; revisit post-RBAC review |
| OQ-003 | Password reset email template/sender? | Phase 2, FR-AUTH-005 | Before Week 3 | Use generic template; sender = noreply@{domain} |
| OQ-004 | RSA key rotation procedure? | Phase 4, operational readiness | Before Week 6 | Document manual rotation; automate in v1.1 |
| OQ-005 | Rate limits on reset endpoints? | Phase 2, FR-AUTH-005 | Before Week 3 | Apply 5 req/min per IP (same as registration) |
| OQ-006 | Legacy auth migration script details? | Phase 4, migration | Before Week 6 | Require schema mapping document from auth-team |

---

## 5. Success Criteria and Validation Approach

| # | Criterion | Target | Validation Phase | Method |
|---|-----------|--------|-----------------|--------|
| 1 | Login response time (p95) | < 200ms | Phase 2 (local), Phase 4b (production) | APM on `AuthService.login()` |
| 2 | Registration success rate | > 99% | Phase 4b | Ratio of 201 to total POST `/auth/register` |
| 3 | Token refresh latency (p95) | < 100ms | Phase 2 (local), Phase 4b (production) | APM on `TokenManager.refresh()` |
| 4 | Service availability | 99.9% uptime | Phase 4c (7-day window) | Health check monitoring |
| 5 | Password hash time | < 500ms | Phase 1 | Benchmark of `PasswordHasher.hash()` |
| 6 | Registration conversion | > 60% | Phase 4c (30-day window) | Funnel analytics from `RegisterPage` |
| 7 | Daily active authenticated users | > 1000 within 30 days | Phase 4c + 30 days | `AuthToken` issuance counts |

**Validation gates between phases:**

- **Phase 1 → Phase 2:** All unit tests pass. `PasswordHasher` benchmark < 500ms. Infrastructure connectivity verified.
- **Phase 2 → Phase 3:** All integration tests pass. p95 latency < 200ms locally. All six endpoints return correct responses.
- **Phase 3 → Phase 4:** E2E tests pass. k6 load test sustains 500 concurrent logins. Frontend components render correctly.
- **Phase 4a → 4b:** Zero P0/P1 bugs from alpha testing.
- **Phase 4b → 4c:** p95 < 200ms, error rate < 0.1%, zero Redis failures over 2 weeks.

---

## 6. Timeline Summary

| Phase | Description | Duration | Cumulative |
|-------|-------------|----------|------------|
| Phase 1 | Foundation & Security Primitives | 2 weeks | Weeks 1–2 |
| Phase 2 | API Development & Core Auth Flows | 2 weeks | Weeks 3–4 |
| Phase 3 | Frontend Integration & E2E Testing | 1.5 weeks | Weeks 5–6 |
| Phase 4a | Internal Alpha | 1 week | Week 6–7 |
| Phase 4b | Beta (10%) | 2 weeks | Weeks 7–8 |
| Phase 4c | General Availability | 1 week | Week 8–9 |

**Critical path:** Infrastructure (Phase 1) → `AuthService` + endpoints (Phase 2) → Frontend + E2E (Phase 3) → Rollout (Phase 4). SendGrid integration (FR-AUTH-005) is off critical path and can proceed in parallel during Phase 2.

**Parallelization opportunities:**
- Phase 1: `PasswordHasher` and `JwtService` can be developed in parallel
- Phase 2: Login/register endpoints vs. password reset endpoints
- Phase 3: Frontend components (parallel across `LoginPage`, `RegisterPage`, `ProfilePage`) while observability setup begins
- Phase 4: Migration script development can overlap with alpha testing
