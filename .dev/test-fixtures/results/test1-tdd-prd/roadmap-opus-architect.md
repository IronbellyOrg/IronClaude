---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.55
primary_persona: architect
generated: "2026-03-31"
generator: "roadmap-architect"
total_phases: 5
total_milestones: 8
total_requirements_mapped: 13
risks_mitigated: 3
open_questions: 12
---

# User Authentication Service — Project Roadmap

## 1. Executive Summary

This roadmap defines the phased delivery of a User Authentication Service covering registration, login, JWT token management, profile retrieval, and password reset. The system is a **MEDIUM complexity** (0.55) backend service with elevated security sensitivity, integrating PostgreSQL, Redis, and SendGrid across five technical domains (backend, security, frontend, testing, devops).

**Key architectural drivers:**

- Stateless JWT authentication (RS256, 2048-bit keys) with Redis-backed refresh tokens
- bcrypt password hashing (cost factor 12) behind a `PasswordHasher` abstraction
- Three-phase progressive rollout using feature flags (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`)
- GDPR consent recording and SOC2 audit logging requirements with an **unresolved retention conflict** (90 days TDD vs 12 months PRD — see OQ-EXT-001)

**Business context:** Authentication unblocks ~$2.4M in projected annual revenue from personalization-dependent features. SOC2 Type II audit deadline is Q3 2026. The personalization roadmap is blocked today.

**Critical path:** Infrastructure provisioning → Core auth components → Token management → Frontend integration → Progressive rollout

---

## 2. Phased Implementation Plan

### Phase 1: Foundation & Infrastructure (Week 1–2)

**Milestone M0: Infrastructure Ready**

**Objective:** Provision all infrastructure dependencies and establish the project skeleton with CI/CD, so that component development can proceed without blockers.

**Tasks:**

1. Provision PostgreSQL 15+ instance with connection pooling (pg-pool, 100-connection pool)
   - Create `user_profiles` table schema matching `UserProfile` entity
   - Create `audit_log` table with retention policy (⚠️ blocked on OQ-EXT-001 resolution — implement 12-month retention as the more conservative default)
   - Configure read replica for failover scenarios
2. Provision Redis 7+ cluster (1 GB initial, HPA to 2 GB at 70% memory)
   - Configure TTL-based eviction for refresh tokens (7-day default)
3. Generate RSA 2048-bit key pair for `JwtService` token signing (NFR-SEC-002)
   - Store in Kubernetes secrets volume with rotation alerting
4. Configure SendGrid API integration for password reset emails (Dependency #6)
5. Set up Node.js 20 LTS project skeleton with:
   - TLS 1.3 enforcement on all endpoints
   - CORS configuration restricted to known frontend origins
   - URL-prefix versioning (`/v1/auth/*`)
   - Structured logging (sensitive field exclusion for passwords/tokens)
   - OpenTelemetry tracing instrumentation
6. Configure CI pipeline with testcontainers (PostgreSQL + Redis)
7. Set up Prometheus metrics stubs: `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total`
8. Configure feature flags: `AUTH_NEW_LOGIN` (OFF), `AUTH_TOKEN_REFRESH` (OFF)

**Dependencies resolved:** INFRA-DB-001, SEC-POLICY-001, Node.js 20 LTS, PostgreSQL 15+, Redis 7+

**Exit criteria:**
- PostgreSQL and Redis accessible from staging
- CI pipeline green with testcontainers
- RSA key pair mounted and accessible
- Health check endpoint (`/health`) responding 200

---

### Phase 2: Core Authentication (Week 2–4)

**Milestone M1: Login & Registration Operational**

**Objective:** Deliver FR-AUTH-001 (login) and FR-AUTH-002 (registration) with full security controls, satisfying PRD Epic AUTH-E1 (minus logout — see OQ-EXT-003).

**Tasks:**

1. **Implement `PasswordHasher` module**
   - bcrypt hashing with cost factor 12 (NFR-SEC-001)
   - `hash(password): string` and `verify(password, hash): boolean` methods
   - Abstraction layer for future algorithm migration
   - Unit test: UT benchmark `hash()` < 500ms (Success Criterion #5)

2. **Implement `UserRepo` data access layer**
   - CRUD operations on `UserProfile` records in PostgreSQL
   - Email uniqueness enforcement (unique index, lowercase normalized)
   - `displayName` validation (2–100 chars)
   - Integration test: IT-001 (registration persists `UserProfile` to database)

3. **Implement `AuthService` orchestrator — login flow (FR-AUTH-001)**
   - Validate email/password via `PasswordHasher.verify()`
   - Return 401 for invalid credentials AND non-existent email (no user enumeration)
   - Account lockout after 5 failed attempts within 15 minutes
   - Return 423 Locked when account is locked
   - Rate limiting: 10 req/min per IP on POST `/auth/login`
   - Unit tests: UT-001, UT-002

4. **Implement `AuthService` orchestrator — registration flow (FR-AUTH-002)**
   - Email uniqueness check → 409 Conflict on duplicate
   - Password strength validation (≥ 8 chars, uppercase, number) → 400 on failure
   - `PasswordHasher.hash()` with cost factor 12
   - Create `UserProfile` with UUID v4, default role `["user"]`
   - **GDPR consent recording** (NFR-COMP-001): Add consent timestamp field to `UserProfile` (⚠️ depends on OQ-EXT-005 resolution — implement proactively per PRD S17)
   - Rate limiting: 5 req/min per IP on POST `/auth/register`

5. **Implement API Gateway rate limiting**
   - Per-IP limits on public endpoints (login: 10/min, register: 5/min)
   - 429 Too Many Requests response with Retry-After header

6. **SOC2 audit logging foundation** (NFR-COMP-002)
   - Log all auth events: user ID, timestamp, IP address, outcome
   - Structured log format for downstream querying
   - ⚠️ Retention: implement 12-month as conservative default pending OQ-EXT-001

**Integration points — Dispatch/Wiring mechanisms:**

| Named Artifact | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|
| `AuthService` dependency injection | `PasswordHasher`, `UserRepo` | Phase 2 | Phase 2 (login/register), Phase 3 (tokens), Phase 4 (profile, reset) |
| API route registry (`/v1/auth/*`) | `POST /auth/login`, `POST /auth/register` | Phase 2 | Phase 3 adds `/auth/refresh`, Phase 4 adds `/auth/me`, `/auth/reset-*` |
| Rate limiter middleware chain | Per-IP limits on login, register endpoints | Phase 2 | Phase 3 adds per-user limits on refresh, me |
| Error response formatter | `AUTH_INVALID_CREDENTIALS`, `AUTH_EMAIL_CONFLICT`, `AUTH_WEAK_PASSWORD` | Phase 2 | All phases add error codes |

**Exit criteria:**
- POST `/auth/login` returns 200 with stub token on valid credentials, 401 on invalid
- POST `/auth/register` returns 201 with `UserProfile`, 409 on duplicate, 400 on weak password
- Account lockout triggers after 5 failed attempts
- All unit tests (UT-001, UT-002) and integration test (IT-001) passing
- Audit log entries written for all login/registration events

---

### Phase 3: Token Management (Week 4–5)

**Milestone M2: JWT + Refresh Token Operational**

**Objective:** Deliver FR-AUTH-003 (token issuance/refresh) and FR-AUTH-004 (profile retrieval), completing PRD Epics AUTH-E1 (login returns tokens) and AUTH-E2 (session persistence).

**Tasks:**

1. **Implement `JwtService` module**
   - Sign JWT access tokens with RS256 using 2048-bit RSA keys (NFR-SEC-002)
   - Payload: `UserProfile.id`, `UserProfile.roles`, `iat`, `exp`
   - 15-minute expiry on access tokens
   - 5-second clock skew tolerance for distributed environments
   - Configuration validation test for RS256 + 2048-bit keys

2. **Implement `TokenManager` module**
   - Issue `AuthToken` pair (accessToken via `JwtService` + opaque refreshToken)
   - Store refreshToken in Redis keyed to `UserProfile.id` with 7-day TTL
   - `refresh()`: validate refreshToken → revoke old → issue new pair
   - `revoke()`: remove refreshToken from Redis
   - Rate limiting: 30 req/min per user on POST `/auth/refresh`
   - Unit test: UT-003
   - Integration test: IT-002 (expired refresh token rejected)

3. **Wire `TokenManager` into `AuthService.login()`**
   - Login now returns full `AuthToken` (accessToken, refreshToken, expiresIn: 900, tokenType: "Bearer")
   - Update POST `/auth/login` response to match `AuthToken` schema

4. **Implement POST `/auth/refresh` endpoint (FR-AUTH-003)**
   - Accept `{ refreshToken }` body
   - Return new `AuthToken` pair on valid refresh
   - Return 401 on expired or revoked refreshToken

5. **Implement GET `/auth/me` endpoint (FR-AUTH-004)**
   - Bearer token authentication middleware
   - Return `UserProfile` (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles)
   - Return 401 on expired/invalid accessToken
   - Rate limiting: 60 req/min per user

6. **Implement JWT authentication middleware**
   - Extract Bearer token from Authorization header
   - Verify signature and expiry via `JwtService`
   - Attach user context to request for downstream handlers

**Integration points — Dispatch/Wiring mechanisms:**

| Named Artifact | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|
| `TokenManager` dependency injection | `JwtService`, Redis client | Phase 3 | Phase 3 (refresh), Phase 2 updated (login returns tokens) |
| `AuthService` DI update | Add `TokenManager` to existing `PasswordHasher`, `UserRepo` | Phase 3 | Phase 4 (password reset invalidates tokens) |
| JWT auth middleware | Registered on protected routes (`/auth/me`, future protected endpoints) | Phase 3 | Phase 4 (profile), all future authenticated endpoints |
| API route registry update | Add `POST /auth/refresh`, `GET /auth/me` | Phase 3 | Consumed immediately |
| Rate limiter middleware update | Add per-user limits (refresh: 30/min, me: 60/min) | Phase 3 | Consumed immediately |
| Feature flag `AUTH_TOKEN_REFRESH` | Gates refresh token flow in `TokenManager` | Phase 3 | Phase 5 rollout |

**Exit criteria:**
- Login returns valid `AuthToken` with working JWT (verifiable with public key)
- POST `/auth/refresh` exchanges valid refresh token for new pair
- GET `/auth/me` returns `UserProfile` for authenticated user, 401 for invalid token
- IT-002 passing (expired refresh token rejection)
- Token refresh latency < 100ms at p95 (Success Criterion #3)

---

### Phase 4: Password Reset & Frontend (Week 5–7)

**Milestone M3: Full Feature Set**

**Objective:** Deliver FR-AUTH-005 (password reset) and all frontend components, completing PRD Epic AUTH-E3 and enabling end-to-end user journeys.

**Tasks:**

1. **Implement password reset flow (FR-AUTH-005)**
   - POST `/auth/reset-request`: generate reset token, send via SendGrid
     - Same success response regardless of email existence (no enumeration)
     - Reset token: 1-hour expiry, single-use
   - POST `/auth/reset-confirm`: validate token → update password via `PasswordHasher` → invalidate all existing sessions (revoke all refresh tokens for user)
   - ⚠️ OQ-PRD-001: Implement asynchronous email sending as the safer default (queue-based via Redis)

2. **Implement `AuthProvider` context provider (Component #9)**
   - Token storage: accessToken in memory only (not localStorage — R-001 mitigation)
   - refreshToken in HttpOnly cookie
   - Silent refresh on token expiry via `POST /auth/refresh`
   - Clear tokens on tab close
   - Redirect to `LoginPage` on authentication failure

3. **Implement `LoginPage` (Component #6)**
   - Form: email + password fields with inline validation
   - Call POST `/auth/login` via `AuthProvider`
   - Generic error message on failure (no user enumeration)
   - CAPTCHA after 3 failed attempts (R-002 contingency)
   - Redirect to dashboard on success

4. **Implement `RegisterPage` (Component #7)**
   - Form: email + password + displayName with inline validation
   - Password strength indicator showing requirements
   - GDPR consent checkbox (NFR-COMP-001) with timestamp recording
   - Call POST `/auth/register` via `AuthProvider`
   - Redirect to dashboard on success

5. **Implement `ProfilePage` (Component #8)**
   - Display: displayName, email, createdAt via GET `/auth/me`
   - Protected route requiring authentication

6. **Implement frontend routing**
   - `/login` → `LoginPage` (public)
   - `/register` → `RegisterPage` (public)
   - `/profile` → `ProfilePage` (protected, redirects to `/login` if unauthenticated)

7. **E2E test: E2E-001** — User registers on `RegisterPage` → logs in on `LoginPage` → views `ProfilePage`

**Integration points — Dispatch/Wiring mechanisms:**

| Named Artifact | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|
| `AuthProvider` token state machine | `LoginPage`, `RegisterPage`, `ProfilePage`, silent refresh | Phase 4 | All frontend components |
| Frontend route registry | `/login` → `LoginPage`, `/register` → `RegisterPage`, `/profile` → `ProfilePage` | Phase 4 | Phase 5 (feature flag gates route access) |
| `AuthService` DI update | Add Email Service (SendGrid) for password reset | Phase 4 | FR-AUTH-005 flow |
| API route registry update | Add `POST /auth/reset-request`, `POST /auth/reset-confirm` | Phase 4 | Consumed immediately |
| Error code registry update | Add `AUTH_RESET_TOKEN_EXPIRED`, `AUTH_RESET_TOKEN_USED` | Phase 4 | Consumed immediately |

**Exit criteria:**
- Password reset email delivered within 60 seconds (Success Criterion #10 — >80% completion)
- All four frontend pages render and function correctly
- E2E-001 passing end-to-end
- All FR-AUTH-001 through FR-AUTH-005 functional
- Silent token refresh works without user interaction

---

### Phase 5: Hardening, Rollout & GA (Week 7–10)

**Milestone M4: Production Ready**
**Milestone M5: Internal Alpha Complete**
**Milestone M6: Beta (10%) Complete**
**Milestone M7: General Availability**

**Objective:** Validate all NFRs under load, execute the three-phase progressive rollout, and achieve production stability.

#### Sub-Phase 5a: Hardening (Week 7–8)

1. **Load testing with k6** (NFR-PERF-002)
   - Validate 500 concurrent login requests
   - Verify p95 latency < 200ms (NFR-PERF-001, Success Criterion #1)
   - Verify token refresh latency < 100ms at p95 (Success Criterion #3)
2. **Security review**
   - Penetration testing on all `/auth/*` endpoints
   - Verify XSS mitigation: accessToken in memory, HttpOnly refreshToken cookie
   - Verify brute-force mitigation: rate limiting + account lockout
   - Verify TLS 1.3 enforcement
   - Verify CORS configuration
3. **Observability validation**
   - Grafana dashboards for all Prometheus metrics
   - Alert rules: login failure rate >20%/5min, p95 >500ms, Redis connection failures
   - OpenTelemetry traces covering `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`
4. **Runbook validation**
   - Simulate Scenario 1 (AuthService down) and Scenario 2 (token refresh failures)
   - Verify escalation paths and rollback procedures
5. **Compliance validation gate**
   - GDPR: consent recorded at registration with timestamp (NFR-COMP-001)
   - GDPR: only email, hashed password, displayName collected (NFR-COMP-003)
   - SOC2: all auth events logged with required fields (NFR-COMP-002)
   - ⚠️ Audit log retention must be resolved (OQ-EXT-001) before GA

**M4 Exit criteria:** All NFRs validated, security review passed, runbooks tested

#### Sub-Phase 5b: Internal Alpha (Week 8–9, 1 week)

- Deploy to staging
- auth-team and QA manual testing of all FR-AUTH-001 through FR-AUTH-005
- `AUTH_NEW_LOGIN` remains OFF in production

**M5 Exit criteria:** Zero P0/P1 bugs. All FRs pass manual testing.

#### Sub-Phase 5c: Beta 10% (Week 9–10, 2 weeks)

- Enable `AUTH_NEW_LOGIN` for 10% of traffic
- Enable `AUTH_TOKEN_REFRESH`
- Monitor: p95 latency, error rates, Redis usage, `AuthProvider` token refresh under real load

**M6 Exit criteria:**
- p95 latency < 200ms
- Error rate < 0.1%
- No Redis connection failures
- No data corruption in `UserProfile` records

**Rollback triggers:**
1. p95 latency > 1000ms for > 5 minutes
2. Error rate > 5% for > 2 minutes
3. `TokenManager` Redis connection failures > 10/min
4. Any `UserProfile` data loss or corruption

#### Sub-Phase 5d: General Availability (Week 10+, 1 week)

- Remove `AUTH_NEW_LOGIN` flag — 100% traffic to new `AuthService`
- Legacy auth system deprecated
- auth-team 24/7 on-call rotation for first 2 weeks
- `AUTH_TOKEN_REFRESH` flag removed after GA + 2 weeks

**M7 Exit criteria:**
- 99.9% uptime over first 7 days (NFR-REL-001)
- All monitoring dashboards green
- Daily active authenticated users trending toward 1000 within 30 days (Success Criterion #7)
- Registration conversion > 60% (Success Criterion #6)

---

## 3. Risk Assessment and Mitigation

| Risk ID | Risk | Severity | Probability | Phase Mitigated | Mitigation Strategy | Contingency |
|---------|------|----------|-------------|-----------------|---------------------|-------------|
| R-001 | Token theft via XSS enables session hijacking | HIGH | Medium | Phase 3 (token design), Phase 4 (frontend storage) | accessToken in memory only; HttpOnly cookie for refreshToken; `AuthProvider` clears on tab close; 15-min access token expiry | Immediate token revocation via `TokenManager`; forced password reset |
| R-002 | Brute-force attacks on login endpoint | MEDIUM | High | Phase 2 (rate limiting, lockout) | API Gateway rate limiting 10 req/min/IP; account lockout after 5 failures/15 min; bcrypt cost 12 | WAF IP blocking; CAPTCHA on `LoginPage` after 3 failures |
| R-003 | Data loss during legacy auth migration | HIGH | Low | Phase 5 (parallel operation) | Parallel operation with legacy during Phases 5b–5c; idempotent upsert for `UserProfile` migration; full DB backup before each phase | Rollback to legacy via `AUTH_NEW_LOGIN` flag; restore from backup |
| R-004 (new) | Unresolved open questions delay delivery | MEDIUM | Medium | All phases | Track OQ resolution dates; implement conservative defaults where safe (12-month retention, async email, proactive consent field) | Descope affected features to post-GA if blocking |
| R-005 (new) | Redis unavailability degrades token refresh | MEDIUM | Low | Phase 3, Phase 5a | Redis cluster with automatic failover; memory monitoring with scaling trigger | Refresh rejection (users re-login via `LoginPage`); not stale token serving |

---

## 4. Resource Requirements and Dependencies

### Team Allocation

| Team | Phase Involvement | Key Responsibilities |
|------|-------------------|---------------------|
| auth-team | All phases | `AuthService`, `PasswordHasher`, `TokenManager`, `JwtService`, `UserRepo` implementation |
| platform-team | Phase 1, Phase 5 | Infrastructure provisioning, Redis/PostgreSQL operations, Kubernetes configuration |
| frontend-team | Phase 4 | `LoginPage`, `RegisterPage`, `ProfilePage`, `AuthProvider` |
| QA | Phase 4–5 | E2E testing (Playwright), manual testing during alpha |
| security | Phase 5a | Penetration testing, security review |

### Infrastructure Dependencies

| Dependency | Required By | Provisioning Owner | Lead Time |
|------------|------------|-------------------|-----------|
| PostgreSQL 15+ (INFRA-DB-001) | Phase 1 start | platform-team | 1–2 days |
| Redis 7+ | Phase 1 start | platform-team | 1–2 days |
| SendGrid API access | Phase 4 start | platform-team | 1 week (account setup + DNS) |
| RSA key pair generation | Phase 1 | auth-team + security | 1 day |
| Staging environment | Phase 5b | platform-team | Assumed available |

### Library Dependencies

| Library | Used By | Risk |
|---------|---------|------|
| bcryptjs | `PasswordHasher` | Low — mature, well-audited |
| jsonwebtoken | `JwtService` | Low — widely used, active maintenance |
| pg / pg-pool | `UserRepo` | Low — standard PostgreSQL client |
| ioredis | `TokenManager` | Low — production-grade Redis client |

---

## 5. Success Criteria and Validation Approach

### Quantitative Validation Matrix

| # | Criterion | Target | Validation Method | Phase Validated |
|---|-----------|--------|-------------------|-----------------|
| 1 | Login response time (p95) | < 200ms | APM on `AuthService.login()` | Phase 5a (load test) |
| 2 | Registration success rate | > 99% | Ratio: successful / attempted | Phase 5c (beta monitoring) |
| 3 | Token refresh latency (p95) | < 100ms | APM on `TokenManager.refresh()` | Phase 5a (load test) |
| 4 | Service availability | 99.9% uptime / 30 days | Health check monitoring | Phase 5d (GA + 30 days) |
| 5 | Password hash time | < 500ms | Benchmark `PasswordHasher.hash()` | Phase 2 (unit test) |
| 6 | Registration conversion | > 60% | Funnel: `RegisterPage` → confirmed | Phase 5d (GA + 30 days) |
| 7 | Daily active authenticated users | > 1000 within 30 days GA | `AuthToken` issuance counts | Phase 5d (GA + 30 days) |
| 8 | Average session duration | > 30 minutes | Token refresh event analytics | Phase 5d (GA + 30 days) |
| 9 | Failed login rate | < 5% of attempts | Auth event log analysis | Phase 5c–5d |
| 10 | Password reset completion | > 80% | Funnel: reset requested → new password | Phase 5c–5d |

### Qualitative Validation

- **Security review sign-off** before beta (Phase 5a)
- **Compliance validation** against GDPR and SOC2 requirements before GA (Phase 5a)
- **Runbook dry-run** for both operational scenarios before beta (Phase 5a)
- **On-call readiness** confirmed: auth-team 24/7 rotation staffed for GA (Phase 5d)

### Test Coverage Targets

| Level | Target | Tool | Phase |
|-------|--------|------|-------|
| Unit | 80% | Jest, ts-jest | Phase 2–4 |
| Integration | 15% | Supertest, testcontainers | Phase 2–4 |
| E2E | 5% | Playwright | Phase 4 |

---

## 6. Timeline Summary

| Phase | Duration | Weeks | Key Milestone | Dependencies |
|-------|----------|-------|---------------|-------------|
| Phase 1: Foundation | 2 weeks | 1–2 | M0: Infrastructure Ready | INFRA-DB-001, SEC-POLICY-001 |
| Phase 2: Core Auth | 2 weeks | 2–4 | M1: Login & Registration | Phase 1 complete |
| Phase 3: Token Mgmt | 1.5 weeks | 4–5 | M2: JWT + Refresh | Phase 2 complete |
| Phase 4: Reset & Frontend | 2 weeks | 5–7 | M3: Full Feature Set | Phase 3 complete, SendGrid |
| Phase 5a: Hardening | 1 week | 7–8 | M4: Production Ready | Phase 4 complete |
| Phase 5b: Alpha | 1 week | 8–9 | M5: Alpha Complete | M4 |
| Phase 5c: Beta 10% | 2 weeks | 9–10 | M6: Beta Complete | M5 |
| Phase 5d: GA | 1 week | 10+ | M7: General Availability | M6 |

**Total estimated duration:** 10–11 weeks

**Critical path:** PostgreSQL/Redis provisioning → `PasswordHasher` + `UserRepo` → `AuthService` login → `TokenManager` + `JwtService` → Frontend integration → Load testing → Progressive rollout

---

## 7. Open Questions Requiring Resolution

### Blocking (must resolve before affected phase)

| ID | Question | Blocks | Recommended Default |
|----|----------|--------|---------------------|
| OQ-EXT-001 | Audit log retention: 90 days (TDD) vs 12 months (PRD)? | Phase 5a compliance gate | Implement 12-month (PRD/SOC2 is more conservative) |
| OQ-EXT-005 | Add GDPR consent timestamp to `UserProfile` schema? | Phase 2 registration | Yes — add field proactively per PRD S17 |
| OQ-002 | Maximum `UserProfile` roles array length? | Phase 2 `UserRepo` validation | 10 roles (reasonable default, easily adjustable) |

### Non-blocking (track but proceed with defaults)

| ID | Question | Default Applied |
|----|----------|-----------------|
| OQ-PRD-001 | Sync vs async password reset emails? | Async via Redis queue |
| OQ-PRD-002 | Max refresh tokens per user across devices? | Unlimited in v1.0; revisit post-GA |
| OQ-PRD-003 | "Remember me" extended session? | Out of scope for v1.0 |
| OQ-001 | API key auth for service-to-service? | Deferred — tracked for v1.1 |
| OQ-EXT-003 | Logout endpoint? | Implement as `POST /auth/logout` (revoke refresh token) — low effort, PRD requires it |
| OQ-EXT-002 | Admin log query endpoint? | Defer to post-GA; Jordan persona needs are acknowledged but not in TDD v1.0 scope |
| OQ-EXT-004 | Dedicated service-to-service auth FR? | Covered by OQ-001; defer to v1.1 |
| OQ-EXT-006 | Account lockout policy formally decided? | TDD value (5 attempts / 15 min) is implemented; confirm with Security team |

---

## 8. Scope Guardrails (from PRD S12)

The following are **explicitly out of scope** per the PRD and must not creep into this roadmap:

- OAuth/OIDC (planned v2.0)
- Multi-factor authentication (planned v1.1)
- Role-based access control (separate PRD)
- Social login (depends on OAuth infrastructure)

Any requirement that touches these areas should be flagged and deferred rather than partially implemented.
