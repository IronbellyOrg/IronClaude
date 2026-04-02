---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.55
adversarial: true
base_variant: "Opus (Variant A)"
variant_scores: "A:79 B:73"
convergence_score: 0.62
debate_rounds: 2
generated: "2026-03-31"
total_phases: 6
total_milestones: 9
total_requirements_mapped: 13
risks_mitigated: 5
open_questions: 12
team_size_fte: 9
timeline_weeks: 15
---

# User Authentication Service — Merged Project Roadmap

## 1. Executive Summary

This roadmap defines the phased delivery of a User Authentication Service covering registration, login, JWT token management, profile retrieval, and password reset. The system is a **MEDIUM complexity** (0.55) backend service with elevated security sensitivity, integrating PostgreSQL, Redis, and SendGrid across five technical domains (backend, security, frontend, testing, devops).

This merged roadmap uses the Opus variant as its structural foundation (5-phase + Phase 0) and incorporates targeted improvements from the Haiku variant as identified through adversarial debate: team composition, wiring checklist, per-phase risk tables, runbook drills, lightweight approval gates, and phase-level effort estimates.

**Key architectural drivers:**

- Stateless JWT authentication (RS256, 2048-bit keys) with Redis-backed refresh tokens
- bcrypt password hashing (cost factor 12) behind a `PasswordHasher` abstraction
- Three-phase progressive rollout using feature flags (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`)
- GDPR consent recording and SOC2 audit logging requirements with an **unresolved retention conflict** (90 days TDD vs 12 months PRD — see OQ-EXT-001)
- Early schema integration for compliance fields (debate convergence) with grouped compliance validation gate

**Business context:** Authentication unblocks ~$2.4M in projected annual revenue from personalization-dependent features. SOC2 Type II audit deadline is Q3 2026. A 15-week timeline targets GA by mid-July, preserving 6+ weeks of SOC2 buffer.

**Critical path:** Infrastructure provisioning → Core auth components → Token management → Frontend integration + Compliance validation → Progressive rollout

**Timeline: 15 weeks** (debate-converged from Opus's 10 and Haiku's 20) with ~9 FTE.

---

## 2. Team Composition

*Incorporated from Haiku variant per debate convergence point 9.*

| Role | Count | Responsibility | Timeline |
|------|-------|----------------|----------|
| Backend Engineer (Auth) | 3 | AuthService, PasswordHasher, TokenManager, JwtService, UserRepo, API endpoints, audit logging | W1–W12 full-time, W13–W15 on-call |
| Backend Engineer (Infra/Integration) | 1 | Database schema, migrations, API Gateway, rate limiting, feature flags, deployment manifests | W0–W12 full-time, W13–W15 part-time |
| Frontend Engineer | 2 | LoginPage, RegisterPage, ProfilePage, AuthProvider, token refresh, form validation | W3–W10 full-time, W11–W15 on-call |
| DevOps Engineer | 1 | Infrastructure provisioning, Kubernetes, monitoring, alerting, on-call support | W0 full-time, W1–W12 part-time, W13–W15 on-call |
| QA Engineer | 1 | Unit tests, integration tests, E2E tests, load testing, pen test coordination | W1–W12 full-time, W13–W15 on-call |
| Security Engineer | 0.5 FTE | Security policy finalization, code review, penetration testing, compliance validation | W0, W1, W7–W8, W11–W12 |

**Total: ~9 FTE over 15 weeks**

---

## 3. Phased Implementation Plan

### Phase 0: Foundation and Infrastructure (Week 0, 1 week)

*Added per debate convergence point 5 — compressed from Haiku's 2 weeks.*

**Milestone M0: Infrastructure Ready**

**Objective:** Provision all infrastructure dependencies, finalize security policies, and establish the project skeleton so that component development can proceed without blockers.

**Effort estimate:** ~60 person-hours

**Tasks:**

1. Provision PostgreSQL 15+ instance with connection pooling (pg-pool, 100-connection pool)
   - Create `user_profiles` table schema matching `UserProfile` entity
   - Create `audit_log` table with retention policy (implement 12-month as conservative default pending OQ-EXT-001)
   - Add `consent_timestamp` field to `user_profiles` schema (zero-cost early integration per debate convergence point 10)
2. Provision Redis 7+ cluster (1 GB initial, HPA to 2 GB at 70% memory)
   - Configure TTL-based eviction for refresh tokens (7-day default)
3. Generate RSA 2048-bit key pair for `JwtService` token signing (NFR-SEC-002)
   - Store in Kubernetes secrets volume with rotation alerting
4. Configure SendGrid API integration for password reset emails
5. Set up Node.js 20 LTS project skeleton with TLS 1.3, CORS, URL-prefix versioning (`/v1/auth/*`), structured logging, OpenTelemetry tracing
6. Configure CI pipeline with testcontainers (PostgreSQL + Redis)
7. Set up Prometheus metrics stubs and feature flags (`AUTH_NEW_LOGIN` OFF, `AUTH_TOKEN_REFRESH` OFF)
8. Finalize SEC-POLICY-001 with password/token requirements (cross-team sign-off)

**Phase 0 risks:**

| Risk | Probability | Impact | Mitigation | Trigger |
|------|-------------|--------|------------|---------|
| Database or Redis unavailable at Phase 1 start | Low | High | Provision early in Week 0; run staging workload tests | Staging health check fails on Day 3 |
| Security policies undefined or conflicting | Medium | Medium | Security review meeting with auth-team, platform-team, product; document signing | SEC-POLICY-001 not signed by end of Week 0 |

**Exit criteria:**
- PostgreSQL and Redis accessible from staging
- CI pipeline green with testcontainers
- RSA key pair mounted and accessible
- Health check endpoint (`/health`) responding 200
- SEC-POLICY-001 signed

**Approval gate: Pre-Development** (Gate 1 of 3)
- Approvers: DevOps lead, auth-team lead, security engineer
- Criteria: Infrastructure operational, SEC-POLICY-001 signed, OQ-EXT-006 (lockout policy) formalized

---

### Phase 1: Core Authentication (Week 1–3)

**Milestone M1: Login and Registration Operational**

**Objective:** Deliver FR-AUTH-001 (login) and FR-AUTH-002 (registration) with full security controls, satisfying PRD Epic AUTH-E1 (minus logout — see OQ-EXT-003).

**Effort estimate:** ~140 person-hours

**Tasks:**

1. **Implement `PasswordHasher` module**
   - bcrypt hashing with cost factor 12 (NFR-SEC-001)
   - `hash(password): string` and `verify(password, hash): boolean` methods
   - Abstraction layer for future algorithm migration
   - Unit test: benchmark `hash()` < 500ms (Success Criterion #5)

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

4. **Implement `AuthService` orchestrator — registration flow (FR-AUTH-002)**
   - Email uniqueness check → 409 Conflict on duplicate
   - Password strength validation (≥ 8 chars, uppercase, number) → 400 on failure
   - `PasswordHasher.hash()` with cost factor 12
   - Create `UserProfile` with UUID v4, default role `["user"]`
   - GDPR consent recording: `consent_timestamp` populated at registration (schema field added in Phase 0)
   - Rate limiting: 5 req/min per IP on POST `/auth/register`

5. **Implement API Gateway rate limiting**
   - Per-IP limits on public endpoints (login: 10/min, register: 5/min)
   - 429 Too Many Requests response with Retry-After header

6. **SOC2 audit logging foundation** (NFR-COMP-002)
   - Log all auth events: user ID, timestamp, IP address, outcome
   - Structured log format for downstream querying

**Integration points:**

| Named Artifact | Wired Components | Consumed By |
|---|---|---|
| `AuthService` dependency injection | `PasswordHasher`, `UserRepo` | Phase 2 (tokens), Phase 3 (profile, reset) |
| API route registry (`/v1/auth/*`) | `POST /auth/login`, `POST /auth/register` | Phase 2 adds `/auth/refresh`, Phase 3 adds `/auth/me`, `/auth/reset-*` |
| Rate limiter middleware chain | Per-IP limits on login, register | Phase 2 adds per-user limits |
| Error response formatter | `AUTH_INVALID_CREDENTIALS`, `AUTH_EMAIL_CONFLICT`, `AUTH_WEAK_PASSWORD` | All phases add error codes |

**Phase 1 risks:**

| Risk | Probability | Impact | Mitigation | Trigger |
|------|-------------|--------|------------|---------|
| Password hash takes > 500ms | Low | Medium | Baseline cost 12 in local testing; if > 500ms, reduce to 10 | Unit test benchmark exceeds 500ms |
| PostgreSQL connection pool exhaustion | Medium | Medium | pg-pool 100; monitor active connections; test isolation via transactions | CI shows > 80 concurrent connections |

**Exit criteria:**
- POST `/auth/login` returns 200 with stub token on valid credentials, 401 on invalid
- POST `/auth/register` returns 201 with `UserProfile`, 409 on duplicate, 400 on weak password
- Account lockout triggers after 5 failed attempts
- All unit tests (UT-001, UT-002) and integration test (IT-001) passing
- Audit log entries written for all login/registration events
- `consent_timestamp` populated on new registrations

---

### Phase 2: Token Management (Week 3–5)

**Milestone M2: JWT and Refresh Token Operational**

**Objective:** Deliver FR-AUTH-003 (token issuance/refresh) and FR-AUTH-004 (profile retrieval), completing PRD Epics AUTH-E1 (login returns tokens) and AUTH-E2 (session persistence).

**Effort estimate:** ~120 person-hours

**Tasks:**

1. **Implement `JwtService` module**
   - Sign JWT access tokens with RS256 using 2048-bit RSA keys (NFR-SEC-002)
   - Payload: `UserProfile.id`, `UserProfile.roles`, `iat`, `exp`
   - 15-minute expiry on access tokens
   - 5-second clock skew tolerance for distributed environments

2. **Implement `TokenManager` module**
   - Issue `AuthToken` pair (accessToken via `JwtService` + opaque refreshToken)
   - Store refreshToken in Redis keyed to `UserProfile.id` with 7-day TTL
   - `refresh()`: validate refreshToken → revoke old → issue new pair
   - `revoke()`: remove refreshToken from Redis
   - Rate limiting: 30 req/min per user on POST `/auth/refresh`

3. **Wire `TokenManager` into `AuthService.login()`**
   - Login now returns full `AuthToken` (accessToken, refreshToken, expiresIn: 900, tokenType: "Bearer")

4. **Implement POST `/auth/refresh` endpoint (FR-AUTH-003)**

5. **Implement GET `/auth/me` endpoint (FR-AUTH-004)**
   - Bearer token authentication middleware
   - Return `UserProfile` (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles)
   - Rate limiting: 60 req/min per user

6. **Implement JWT authentication middleware**

**Integration points:**

| Named Artifact | Wired Components | Consumed By |
|---|---|---|
| `TokenManager` dependency injection | `JwtService`, Redis client | Phase 2 (refresh), Phase 1 updated (login returns tokens) |
| `AuthService` DI update | Add `TokenManager` to existing `PasswordHasher`, `UserRepo` | Phase 3 (password reset invalidates tokens) |
| JWT auth middleware | Registered on protected routes | Phase 3, all future authenticated endpoints |
| Feature flag `AUTH_TOKEN_REFRESH` | Gates refresh token flow | Phase 5 rollout |

**Phase 2 risks:**

| Risk | Probability | Impact | Mitigation | Trigger |
|------|-------------|--------|------------|---------|
| Token theft via XSS (R-001) | High | Critical | AccessToken in memory only; HttpOnly cookie for refreshToken; 15-min expiry | Security review in Phase 4 |
| Redis unavailability (R-005) | Low | High | Redis cluster with automatic failover; fallback to password re-entry | Redis connection failures > 10/min |
| JWT clock skew issues | Medium | Medium | 5-second tolerance; monitoring for skew rejection rate | Skew rejection rate > 0.1% |

**Exit criteria:**
- Login returns valid `AuthToken` with working JWT
- POST `/auth/refresh` exchanges valid refresh token for new pair
- GET `/auth/me` returns `UserProfile` for authenticated user, 401 for invalid token
- IT-002 passing (expired refresh token rejection)
- Token refresh latency < 100ms at p95

---

### Phase 3: Password Reset, Frontend, and Compliance Validation (Week 5–8)

**Milestone M3: Full Feature Set**

**Objective:** Deliver FR-AUTH-005 (password reset), all frontend components, and complete compliance validation. Frontend starts here per debate convergence point 8 — after API contract is stable from Phases 1–2.

**Effort estimate:** ~200 person-hours

**Tasks:**

1. **Implement password reset flow (FR-AUTH-005)**
   - POST `/auth/reset-request`: generate reset token, send via SendGrid (async via Redis queue per OQ-PRD-001 default)
   - POST `/auth/reset-confirm`: validate token → update password → invalidate all sessions
   - Same success response regardless of email existence (no enumeration)
   - Reset token: 1-hour expiry, single-use

2. **Implement `AuthProvider` context provider (Component #9)**
   - Token storage: accessToken in memory only (not localStorage — R-001 mitigation)
   - refreshToken in HttpOnly cookie
   - Silent refresh on token expiry
   - Clear tokens on tab close
   - Redirect to `LoginPage` on authentication failure

3. **Implement `LoginPage` (Component #6)**
   - Form: email + password with inline validation
   - Generic error message on failure (no user enumeration)
   - CAPTCHA after 3 failed attempts (R-002 contingency)

4. **Implement `RegisterPage` (Component #7)**
   - Form: email + password + displayName with inline validation
   - Password strength indicator
   - GDPR consent checkbox (NFR-COMP-001) with timestamp recording

5. **Implement `ProfilePage` (Component #8)**
   - Display: displayName, email, createdAt via GET `/auth/me`
   - Protected route requiring authentication

6. **Implement frontend routing** (`/login`, `/register`, `/profile`)

7. **Compliance validation gate** (debate convergence point 10 — grouped validation from Haiku)
   - GDPR: consent recorded at registration with timestamp (NFR-COMP-001)
   - GDPR: only email, hashed password, displayName collected (NFR-COMP-003)
   - SOC2: all auth events logged with required fields (NFR-COMP-002)
   - Audit log retention resolved (OQ-EXT-001 must be resolved before Phase 4)

8. **Admin audit log query API** (conditional — see decision gate below)
   - GET `/auth/admin/logs` with pagination, user_id and date range filtering
   - Admin authorization middleware checking JWT `roles` claim
   - Decision gate at Week 0: if SOC2 audit requires application-level admin access, include in Phase 3; otherwise defer to post-GA

9. **E2E test: E2E-001** — User registers → logs in → views profile

**Integration points:**

| Named Artifact | Wired Components | Consumed By |
|---|---|---|
| `AuthProvider` token state machine | All frontend pages, silent refresh | Phase 4 feature flag gates |
| Frontend route registry | `/login`, `/register`, `/profile` | Phase 5 rollout |
| Email Service (SendGrid) | `AuthService` password reset flow | FR-AUTH-005 |
| Audit Logger singleton | All auth endpoints | Phase 4 monitoring, admin query API |

**Phase 3 risks:**

| Risk | Probability | Impact | Mitigation | Trigger |
|------|-------------|--------|------------|---------|
| Password reset token reuse | Medium | High | Token marked consumed after first use; code review | Code review finds reuse vulnerability |
| Audit log performance degradation | Medium | Medium | Async writes; separate connection pool; indexes | Audit INSERT latency > 100ms |
| SendGrid delivery failure | Low | Medium | Fallback manual email; alerting for SendGrid status | Email delivery rate drops below 95% |
| Frontend built against unstable APIs | Low | Low | API contract stable after Phase 2; only AuthProvider touches token internals | API changes after Phase 2 completion |

**Exit criteria:**
- Password reset email delivered within 60 seconds (>80% completion rate)
- All four frontend pages render and function correctly
- E2E-001 passing end-to-end
- All FR-AUTH-001 through FR-AUTH-005 functional
- Silent token refresh works without user interaction
- Compliance validation gate passed: GDPR consent, SOC2 audit logging confirmed

**Approval gate: Pre-Hardening** (Gate 2 of 3)
- Approvers: auth-team lead, security engineer, product owner
- Criteria: All FRs complete, compliance validation passed, OQ-EXT-001 resolved

---

### Phase 4: Hardening and Operational Readiness (Week 8–10)

**Milestone M4: Production Ready**

**Objective:** Validate all NFRs under load, complete security review, establish observability, and test all runbooks.

**Effort estimate:** ~120 person-hours

#### Sub-Phase 4a: Load Testing and Security Review (Week 8–9)

1. **Load testing with k6** (NFR-PERF-002)
   - Validate 500 concurrent login requests
   - Verify p95 latency < 200ms (NFR-PERF-001)
   - Verify token refresh latency < 100ms at p95

2. **Security review**
   - Penetration testing on all `/auth/*` endpoints
   - Verify XSS mitigation: accessToken in memory, HttpOnly refreshToken cookie
   - Verify brute-force mitigation: rate limiting + account lockout
   - Verify TLS 1.3 enforcement and CORS configuration

3. **Observability validation**
   - Grafana dashboards for all Prometheus metrics
   - Alert rules: login failure rate >20%/5min, p95 >500ms, Redis connection failures
   - OpenTelemetry traces covering full request chain

#### Sub-Phase 4b: Runbook Validation and Drills (Week 9–10)

*Incorporated from Haiku per debate convergence point 5.*

4. **Runbook creation and validation**
   - Document runbooks for: AuthService down, token refresh failures, DB pool exhaustion, SendGrid outage, rollback procedure
   - **Team executes each runbook scenario** — simulated outage drills with target recovery times
   - Verify escalation paths and on-call rotation

**Phase 4 risks:**

| Risk | Probability | Impact | Mitigation | Trigger |
|------|-------------|--------|------------|---------|
| Load test finds p95 > 200ms | Medium | High | Profile bottlenecks; optimize slowest path; scale resources | k6 results show p95 > 200ms |
| Penetration test finds XSS | Medium | Critical | Fix before GA; re-test after fix | Pen test report contains P0/P1 |
| Rollback procedure doesn't work | Low | Critical | Test rollback in staging before GA; dry-run with team | Rollback test fails in staging |

**Exit criteria:**
- All NFRs validated under load
- Security review passed, no unresolved P0/P1 findings
- Runbooks tested via team drills with documented recovery times
- All monitoring dashboards operational with real data

**Approval gate: Pre-GA** (Gate 3 of 3)
- Approvers: security lead, auth-team lead, DevOps lead
- Criteria: Penetration test signed off, load test passed, runbooks drill-tested, on-call rotation staffed

---

### Phase 5: Rollout and General Availability (Week 10–15)

**Milestone M5: Internal Alpha Complete**
**Milestone M6: Beta (10%) Complete**
**Milestone M7: General Availability**
**Milestone M8: 30-Day Stability Confirmed**

**Objective:** Execute three-phase progressive rollout and achieve production stability.

**Effort estimate:** ~80 person-hours (primarily monitoring and on-call)

#### Sub-Phase 5a: Internal Alpha (Week 10–11, 1 week)

- Deploy to staging
- auth-team and QA manual testing of all FR-AUTH-001 through FR-AUTH-005
- `AUTH_NEW_LOGIN` remains OFF in production

**M5 exit criteria:** Zero P0/P1 bugs. All FRs pass manual testing.

#### Sub-Phase 5b: Beta 10% (Week 11–13, 2 weeks)

- Enable `AUTH_NEW_LOGIN` for 10% of traffic
- Enable `AUTH_TOKEN_REFRESH`
- Monitor: p95 latency, error rates, Redis usage, `AuthProvider` token refresh under real load

**M6 exit criteria:**
- p95 latency < 200ms
- Error rate < 0.1%
- No Redis connection failures
- No data corruption in `UserProfile` records

**Rollback triggers:**
1. p95 latency > 1000ms for > 5 minutes
2. Error rate > 5% for > 2 minutes
3. `TokenManager` Redis connection failures > 10/min
4. Any `UserProfile` data loss or corruption

*Thresholds from Opus; runbook drill process from Haiku ensures team can execute rollback under pressure.*

#### Sub-Phase 5c: General Availability (Week 13–14, 1 week)

- Remove `AUTH_NEW_LOGIN` flag — 100% traffic to new `AuthService`
- Legacy auth system deprecated
- auth-team 24/7 on-call rotation for first 2 weeks
- `AUTH_TOKEN_REFRESH` flag removed after GA + 2 weeks

#### Sub-Phase 5d: 30-Day Stability Monitoring (Week 14+)

**M7/M8 exit criteria:**
- 99.9% uptime over first 7 days (NFR-REL-001)
- All monitoring dashboards green
- Daily active authenticated users trending toward 1000 within 30 days
- Registration conversion > 60%

---

## 4. Risk Assessment

### Primary Risks

| Risk ID | Risk | Severity | Probability | Mitigation Strategy | Contingency |
|---------|------|----------|-------------|---------------------|-------------|
| R-001 | Token theft via XSS enables session hijacking | HIGH | Medium | accessToken in memory only; HttpOnly cookie for refreshToken; 15-min expiry; `AuthProvider` clears on tab close | Immediate token revocation via `TokenManager`; forced password reset |
| R-002 | Brute-force attacks on login endpoint | MEDIUM | High | API Gateway rate limiting 10 req/min/IP; account lockout after 5 failures/15 min; bcrypt cost 12 | WAF IP blocking; CAPTCHA on `LoginPage` after 3 failures |
| R-003 | Data loss during legacy auth migration | HIGH | Low | Parallel operation with legacy during Phase 5b–5c; idempotent upsert; full DB backup before each phase | Rollback to legacy via `AUTH_NEW_LOGIN` flag; restore from backup |
| R-004 | Unresolved open questions delay delivery | MEDIUM | Medium | Track OQ resolution dates; implement conservative defaults (12-month retention, async email, proactive consent field) | Descope affected features to post-GA if blocking |
| R-005 | Redis unavailability degrades token refresh | MEDIUM | Low | Redis cluster with automatic failover; memory monitoring | Refresh rejection (users re-login); not stale token serving |

### Additional Architectural Risks

*Incorporated from Haiku's per-phase risk tables.*

| Risk | Severity | Phase Mitigated | Trigger |
|------|----------|-----------------|---------|
| PostgreSQL connection pool exhaustion | MEDIUM | Phase 0, Phase 4 | Active connections > 80 |
| Password hash timing attacks | LOW | Phase 1 | Code review finds custom comparison logic |
| JWT clock skew issues | MEDIUM | Phase 2, Phase 4 | Skew rejection rate > 0.1% |
| Compliance audit failure (SOC2) | HIGH | Phase 3 | OQ-EXT-001 unresolved at Phase 3 gate |
| Feature flag service failure | MEDIUM | Phase 4, Phase 5 | Flag service unavailable; fallback to conservative default |
| Audit log table unbounded growth | MEDIUM | Phase 3 | Table size > 100GB |

---

## 5. Resource Requirements and Dependencies

### Infrastructure Dependencies

| Dependency | Required By | Provisioning Owner | Lead Time |
|------------|------------|-------------------|-----------|
| PostgreSQL 15+ (INFRA-DB-001) | Phase 0 | platform-team | 1–2 days |
| Redis 7+ | Phase 0 | platform-team | 1–2 days |
| SendGrid API access | Phase 3 start | platform-team | 1 week (account setup + DNS) |
| RSA key pair generation | Phase 0 | auth-team + security | 1 day |
| Staging environment | Phase 5a | platform-team | Assumed available |

### Library Dependencies

| Library | Used By | Risk |
|---------|---------|------|
| bcryptjs | `PasswordHasher` | Low — mature, well-audited |
| jsonwebtoken | `JwtService` | Low — widely used, active maintenance |
| pg / pg-pool | `UserRepo` | Low — standard PostgreSQL client |
| ioredis | `TokenManager` | Low — production-grade Redis client |

---

## 6. Success Criteria and Validation Approach

### Quantitative Validation Matrix

| # | Criterion | Target | Validation Method | Phase Validated |
|---|-----------|--------|-------------------|-----------------|
| 1 | Login response time (p95) | < 200ms | APM on `AuthService.login()` | Phase 4a (load test) |
| 2 | Registration success rate | > 99% | Ratio: successful / attempted | Phase 5b (beta monitoring) |
| 3 | Token refresh latency (p95) | < 100ms | APM on `TokenManager.refresh()` | Phase 4a (load test) |
| 4 | Service availability | 99.9% uptime / 30 days | Health check monitoring | Phase 5d (GA + 30 days) |
| 5 | Password hash time | < 500ms | Benchmark `PasswordHasher.hash()` | Phase 1 (unit test) |
| 6 | Registration conversion | > 60% | Funnel: `RegisterPage` → confirmed | Phase 5d (GA + 30 days) |
| 7 | Daily active authenticated users | > 1000 within 30 days GA | `AuthToken` issuance counts | Phase 5d (GA + 30 days) |
| 8 | Average session duration | > 30 minutes | Token refresh event analytics | Phase 5d (GA + 30 days) |
| 9 | Failed login rate | < 5% of attempts | Auth event log analysis | Phase 5b–5d |
| 10 | Password reset completion | > 80% | Funnel: reset requested → new password | Phase 5b–5d |

### Qualitative Validation

- Security review sign-off before beta (Phase 4a)
- Compliance validation against GDPR and SOC2 before hardening (Phase 3 gate)
- Runbook dry-runs with team drills before beta (Phase 4b)
- On-call readiness confirmed: auth-team 24/7 rotation staffed for GA

### Test Coverage Targets

| Level | Target | Tool | Phase |
|-------|--------|------|-------|
| Unit | 80% | Jest / ts-jest | Phase 1–3 |
| Integration | 15% | Supertest, testcontainers | Phase 1–3 |
| E2E | 5% | Playwright | Phase 3 |

---

## 7. Timeline Summary

| Phase | Duration | Weeks | Key Milestone | Effort (person-hours) |
|-------|----------|-------|---------------|----------------------|
| Phase 0: Foundation | 1 week | 0 | M0: Infrastructure Ready | ~60h |
| Phase 1: Core Auth | 2.5 weeks | 1–3 | M1: Login & Registration | ~140h |
| Phase 2: Token Mgmt | 2 weeks | 3–5 | M2: JWT + Refresh | ~120h |
| Phase 3: Reset, Frontend, Compliance | 3 weeks | 5–8 | M3: Full Feature Set | ~200h |
| Phase 4: Hardening | 2 weeks | 8–10 | M4: Production Ready | ~120h |
| Phase 5a: Alpha | 1 week | 10–11 | M5: Alpha Complete | ~20h |
| Phase 5b: Beta 10% | 2 weeks | 11–13 | M6: Beta Complete | ~20h |
| Phase 5c–d: GA + Monitoring | 2 weeks | 13–15 | M7/M8: GA & Stability | ~20h |

**Total estimated duration:** 15 weeks (~700 person-hours across ~9 FTE)

**Critical path:** PostgreSQL/Redis provisioning → `PasswordHasher` + `UserRepo` → `AuthService` login → `TokenManager` + `JwtService` → Frontend + Compliance validation → Load testing → Progressive rollout

---

## 8. Component Wiring Checklist

*Incorporated from Haiku variant — the strongest architectural contribution identified in debate.*

| Mechanism | Type | Owning Phase | Wired Components | Cross-Phase Dependencies | Risk |
|-----------|------|--------------|------------------|-------------------------|------|
| Account Lockout Registry | In-process map | Phase 1 | `AuthService.login()` checks/increments | Phase 4: move to Redis for persistence | Users unlocked on service restart |
| Error Code Registry | Centralized constants | Phase 1 | API handlers use codes for consistency | Phase 2, 3 extend with new codes | None |
| Rate Limit Registry | Centralized config | Phase 1 | API Gateway middleware checks before forwarding | Phase 4 API Gateway enforcement | None |
| Token Signing Key Registry | Kubernetes secrets | Phase 2 | `JwtService.sign()` uses private key | Phase 0: key generation; Phase 4: rotation | Private key leak allows forging |
| Token Storage Registry | Redis client config | Phase 2 | `TokenManager` SET/GET/DEL operations | Phase 0: Redis provisioning; Phase 4: monitoring | Redis unavailability → users re-login |
| Token Refresh Polling | setInterval config | Phase 3 | `AuthProvider` polling interval, refresh logic | Logout stops polling | Thundering herd; mitigate with stagger |
| Reset Token Registry | Redis-backed | Phase 3 | `AuthService` reset generation/validation | Phase 2 `TokenManager` similar pattern | Token reuse if not marked consumed |
| Audit Event Registry | Centralized logger | Phase 3 | All auth endpoints call `AuditLogger.record()` | Phase 4 monitoring consumes logs | Async write overhead |
| Admin Authorization Middleware | Middleware function | Phase 3 (conditional) | Admin endpoints check JWT `roles` | Phase 1/2: JWT issued with roles | Coarse RBAC; extensible for future |
| Feature Flag Registry | Feature flag service | Phase 4 | Routing layer, middleware | Phase 5: flags toggled during rollout | Flag service down → conservative default |
| Prometheus Metrics Registry | Metric exports | Phase 4 | APM instrumentation, endpoint handlers | Phase 5: dashboards consume metrics | None |
| Consent Recording | `UserProfile` field | Phase 0 (schema), Phase 3 (UX) | `RegisterPage`, `AuthService.register()` | Phase 4 compliance audit uses field | No revocation mechanism in v1.0 |

---

## 9. Open Questions Requiring Resolution

### Blocking

| ID | Question | Blocks | Recommended Default | Decision Deadline |
|----|----------|--------|---------------------|-------------------|
| OQ-EXT-001 | Audit log retention: 90 days (TDD) vs 12 months (PRD)? | Phase 3 compliance gate | 12-month (PRD/SOC2 is more conservative) | Week 0 |
| OQ-EXT-005 | Add GDPR consent timestamp to `UserProfile` schema? | Phase 0 schema creation | Yes — add field proactively per PRD S17 | Week 0 |
| OQ-002 | Maximum `UserProfile` roles array length? | Phase 1 `UserRepo` validation | 10 roles (reasonable default) | Week 0 |
| OQ-EXT-002 | Admin log query endpoint in v1.0? | Phase 3 scope | Escalate to product owner Week 0 (debate convergence point 8) | Week 0 |

### Non-blocking

| ID | Question | Default Applied |
|----|----------|-----------------|
| OQ-PRD-001 | Sync vs async password reset emails? | Async via Redis queue |
| OQ-PRD-002 | Max refresh tokens per user across devices? | Unlimited in v1.0; revisit post-GA |
| OQ-PRD-003 | "Remember me" extended session? | Out of scope for v1.0 |
| OQ-001 | API key auth for service-to-service? | Deferred to v1.1 |
| OQ-EXT-003 | Logout endpoint? | Implement as `POST /auth/logout` — low effort, PRD requires it |
| OQ-EXT-004 | Dedicated service-to-service auth FR? | Covered by OQ-001; defer to v1.1 |
| OQ-EXT-006 | Account lockout policy formally decided? | TDD value (5/15 min) implemented; confirm with Security in Phase 0 |

---

## 10. Scope Guardrails (from PRD S12)

The following are **explicitly out of scope** per the PRD and must not creep into this roadmap:

- OAuth/OIDC (planned v2.0)
- Multi-factor authentication (planned v1.1)
- Role-based access control beyond basic admin check (separate PRD)
- Social login (depends on OAuth infrastructure)

Any requirement that touches these areas should be flagged and deferred rather than partially implemented.
