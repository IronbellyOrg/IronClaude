---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.55
primary_persona: architect
---

# Project Roadmap — User Authentication Service

**Source Specification:** AUTH-001-TDD v1.2
**Supplementary PRD:** AUTH-PRD-001 v1.0
**Complexity:** MEDIUM (0.55)
**Domains:** Backend, Security, Frontend, Testing, DevOps

---

## 1. Executive Summary

This roadmap defines the phased delivery of a User Authentication Service providing registration, login, JWT token management, profile retrieval, and password reset. The service is built on a stateless REST architecture with PostgreSQL for persistence, Redis for token storage, and SendGrid for transactional email.

**Strategic context:** Authentication is the prerequisite for the entire Q2-Q3 2026 personalization roadmap (~$2.4M projected revenue) and a SOC2 Type II compliance gate in Q3 2026. Delivery is time-sensitive.

**Key architectural decisions:**
- Stateless `AuthService` facade orchestrating `PasswordHasher`, `TokenManager`, `UserRepo`
- RS256 JWT access tokens (15-min TTL) + opaque Redis-stored refresh tokens (7-day TTL)
- bcrypt cost factor 12 via `PasswordHasher` abstraction (future-proofs for argon2id migration)
- Feature-flag-gated rollout (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`) with automatic rollback criteria

**Scope:** 5 functional requirements (FR-AUTH-001 through FR-AUTH-005), 8 non-functional requirements, 6 API endpoints, 9 components (5 backend, 4 frontend), 3-phase rollout.

**Critical gaps requiring resolution before implementation:**
- GAP-001: Audit log retention must be reconciled to 12 months (PRD/SOC2 wins over TDD's 90-day spec)
- GAP-002: Logout endpoint missing from TDD but in-scope per PRD
- GAP-004: GDPR consent field missing from `UserProfile` schema and `/auth/register` request body

---

## 2. Phased Implementation Plan

### Phase 1: Core Authentication (Milestone M1) — Weeks 1–3

**Objective:** Deliver registration and login with credential validation, token issuance, and account lockout. This phase addresses the highest-value user need (JTBD-1, JTBD-2) and unblocks all downstream phases.

**PRD Alignment:** Epics AUTH-E1 and AUTH-E2 (Phase 1, Sprints 1-3). Persona Alex's core flows.

#### 1.1 Infrastructure Provisioning

1. Provision PostgreSQL 15+ with `UserProfile` table schema including:
   - All fields per data model (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles)
   - **GDPR consent fields** (consent boolean, consent timestamp) — resolves GAP-004
   - Audit log table with **12-month retention policy** — resolves GAP-001
   - Password hash column (bcrypt, not part of `UserProfile` interface)
2. Provision Redis 7+ cluster for refresh token storage (1 GB initial, HPA at 70%)
3. Configure feature flag infrastructure for `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` (both OFF)
4. Generate RS256 2048-bit RSA key pair for `JwtService`; mount as Kubernetes secrets
5. Set up Docker Compose for local dev (PostgreSQL + Redis containers)

**Dependencies:** INFRA-DB-001 (database provisioning), SEC-POLICY-001 (key management policy)

#### 1.2 Backend Core Components

| Task | Component | Requirement | Detail |
|------|-----------|-------------|--------|
| Implement `PasswordHasher` | `PasswordHasher` | NFR-SEC-001 | bcrypt with cost factor 12. Abstract interface for future algorithm migration. Unit tests asserting cost parameter and hash/verify correctness. |
| Implement `JwtService` | `JwtService` | NFR-SEC-002 | RS256 sign/verify with 2048-bit RSA. 5-second clock skew tolerance. Configuration validation test. |
| Implement `UserRepo` | `UserRepo` | FR-AUTH-002 | CRUD operations against PostgreSQL. Email uniqueness enforcement. Lowercase normalization. |
| Implement `TokenManager` | `TokenManager` | FR-AUTH-003 | Token issuance (access 15-min + refresh 7-day). Refresh token hashed before Redis storage. Revocation support. |
| Implement `AuthService` facade | `AuthService` | FR-AUTH-001, FR-AUTH-002 | Orchestrates login and registration flows. Delegates to `PasswordHasher`, `TokenManager`, `UserRepo`. |

#### 1.3 API Endpoints — Core

| Endpoint | Requirement | Key Behaviors |
|----------|-------------|---------------|
| POST `/auth/login` | FR-AUTH-001 | Valid creds → 200 + `AuthToken`. Invalid → 401 (no enumeration). Lockout after 5 failures in 15 min → 423. Rate limit: 10 req/min per IP. |
| POST `/auth/register` | FR-AUTH-002 | Valid → 201 + `UserProfile`. Duplicate email → 409. Weak password → 400. **Must include GDPR consent field in request body** (GAP-004 resolution). |

#### 1.4 Audit Logging Foundation

1. Implement structured audit log writer (user ID, timestamp, IP, event type, outcome)
2. Configure **12-month retention** per NFR-COMP-002 (not 90 days — GAP-001 resolution)
3. Log all login attempts (success/failure), registrations, and lockout events
4. Wire OpenTelemetry spans: `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`

#### 1.5 Frontend — Login and Registration

| Task | Component | Detail |
|------|-----------|--------|
| Implement `LoginPage` | `LoginPage` | Email/password form. Calls POST `/auth/login`. Inline validation. Generic error on failure (no enumeration). CAPTCHA after 3 failures (R-002 mitigation). |
| Implement `RegisterPage` | `RegisterPage` | Email/password/displayName form. Client-side password policy validation. **GDPR consent checkbox** (GAP-004). Calls POST `/auth/register`. |
| Implement `AuthProvider` | `AuthProvider` | Context provider managing `AuthToken` state. Stores accessToken in memory only (R-001 mitigation). HttpOnly cookie for refreshToken. Intercepts 401 responses. |

#### 1.6 Integration Wiring — Phase 1

**Named Artifact: `AuthService` Facade Dispatch**
- **Mechanism:** Constructor dependency injection
- **Wired Components:** `PasswordHasher`, `TokenManager`, `UserRepo` injected into `AuthService`
- **Owning Phase:** Phase 1 (Task 1.2)
- **Consumers:** All API endpoint handlers (Phase 1–3)

**Named Artifact: `AuthProvider` React Context**
- **Mechanism:** React Context Provider wrapping route tree
- **Wired Components:** Token storage (memory for access, HttpOnly cookie for refresh), 401 interceptor, silent refresh handler
- **Owning Phase:** Phase 1 (Task 1.5)
- **Consumers:** `LoginPage`, `RegisterPage` (Phase 1), `ProfilePage` (Phase 2), all protected routes

**Named Artifact: Feature Flag Registry**
- **Mechanism:** Feature flag service (e.g., LaunchDarkly / custom)
- **Wired Components:** `AUTH_NEW_LOGIN` (gates `LoginPage` + `/auth/login`), `AUTH_TOKEN_REFRESH` (gates refresh flow in `TokenManager`)
- **Owning Phase:** Phase 1 (Task 1.1)
- **Consumers:** Phase 2 (beta rollout), Phase 3 (GA + cleanup)

**Named Artifact: Route Registry**
- **Mechanism:** Frontend router configuration
- **Wired Components:** `/login` → `LoginPage`, `/register` → `RegisterPage` (Phase 1); `/profile` → `ProfilePage` (Phase 2)
- **Owning Phase:** Phase 1 (Task 1.5), extended in Phase 2
- **Consumers:** `AuthProvider` for protected route enforcement

#### Phase 1 Exit Criteria

- [ ] FR-AUTH-001 acceptance criteria 1–4 pass (login, invalid creds, no enumeration, lockout)
- [ ] FR-AUTH-002 acceptance criteria 1–4 pass (registration, duplicate, weak password, bcrypt)
- [ ] NFR-SEC-001 validated (bcrypt cost 12 unit test)
- [ ] NFR-SEC-002 validated (RS256 config test)
- [ ] NFR-COMP-001 validated (GDPR consent captured at registration)
- [ ] Unit test coverage ≥ 80% on `AuthService`, `PasswordHasher`, `JwtService`, `TokenManager`, `UserRepo`
- [ ] Integration tests pass: registration → DB persistence, login → token issuance
- [ ] Audit logging operational with 12-month retention configured
- [ ] `LoginPage` and `RegisterPage` functional behind `AUTH_NEW_LOGIN` flag

---

### Phase 2: Token Management and Profile (Milestone M2) — Weeks 4–5

**Objective:** Deliver JWT refresh flow, profile retrieval, logout, and deploy to staging for internal testing. Addresses session persistence (JTBD-2) and persona Sam's programmatic token needs.

**PRD Alignment:** Completes AUTH-E2 (token refresh), begins AUTH-E3 (profile). Enters Migration Phase 1 (Internal Alpha).

#### 2.1 Token Refresh Endpoint

| Endpoint | Requirement | Key Behaviors |
|----------|-------------|---------------|
| POST `/auth/refresh` | FR-AUTH-003 | Valid refresh token → 200 + new `AuthToken` pair. Old refresh token revoked. Expired → 401. Revoked → 401. Rate limit: 30 req/min per user. |

- Wire `AuthProvider` silent refresh: intercept 401, attempt refresh, retry original request
- Gate behind `AUTH_TOKEN_REFRESH` feature flag

#### 2.2 Profile Endpoint

| Endpoint | Requirement | Key Behaviors |
|----------|-------------|---------------|
| GET `/auth/me` | FR-AUTH-004 | Valid accessToken → 200 + `UserProfile` (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles). Invalid/expired token → 401. Rate limit: 60 req/min per user. |

- Implement `ProfilePage` frontend component
- Wire `/profile` route into Route Registry (protected, requires auth)

#### 2.3 Logout Endpoint (GAP-002 Resolution)

| Endpoint | Requirement | Key Behaviors |
|----------|-------------|---------------|
| POST `/auth/logout` | PRD Scope (AUTH-E1) | Revoke refresh token in Redis via `TokenManager`. Clear HttpOnly cookie. Return 200. |

- **Note:** This endpoint is specified in the PRD (AUTH-E1 user story) but absent from the TDD. It is in-scope per PRD scope definition and essential for persona Alex ("secure my session on shared device").
- Audit log: record logout events

#### 2.4 Observability Setup

1. Deploy Prometheus metrics: `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total`
2. Configure Grafana dashboards for auth metrics
3. Set up alerts: high login failure rate (>20% over 5 min), high latency (p95 >500ms), Redis connection errors
4. Verify OpenTelemetry traces cover full `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService` chain

#### 2.5 Integration Wiring — Phase 2

**Named Artifact: `TokenManager` ↔ Redis Refresh Store**
- **Mechanism:** Redis key-value store with TTL (hashed refresh tokens)
- **Wired Components:** `TokenManager.issueTokens()` writes, `TokenManager.refresh()` reads/rotates, `TokenManager.revoke()` deletes
- **Owning Phase:** Phase 1 (creation), Phase 2 (refresh + revocation wiring)
- **Consumers:** POST `/auth/refresh`, POST `/auth/logout`, rollback criteria monitors

**Named Artifact: API Gateway Rate Limit Configuration**
- **Mechanism:** API Gateway middleware (upstream of `AuthService`)
- **Wired Components:** Per-endpoint rate limits (login: 10/min/IP, register: 5/min/IP, refresh: 30/min/user, me: 60/min/user)
- **Owning Phase:** Phase 2 (pre-staging deployment)
- **Consumers:** All endpoints, CORS enforcement

#### 2.6 Migration Phase 1: Internal Alpha (1 week)

- Deploy `AuthService` to staging environment
- auth-team and QA manually test all endpoints (FR-AUTH-001 through FR-AUTH-004 + logout)
- `LoginPage` and `RegisterPage` behind `AUTH_NEW_LOGIN` flag
- Run integration test suite against staging PostgreSQL and Redis

#### Phase 2 Exit Criteria

- [ ] FR-AUTH-003 acceptance criteria 1–4 pass (token issuance, refresh, expired, revoked)
- [ ] FR-AUTH-004 acceptance criteria 1–3 pass (profile retrieval, auth required, full fields)
- [ ] Logout functional: refresh token revoked, cookie cleared
- [ ] NFR-COMP-002 validated (audit logs include user ID, timestamp, IP, outcome for all auth events)
- [ ] NFR-PERF-001 validated in staging (p95 < 200ms on all endpoints)
- [ ] NFR-PERF-002 validated (500 concurrent login load test with k6)
- [ ] Observability stack operational (metrics, dashboards, alerts, traces)
- [ ] Migration Phase 1 complete: zero P0/P1 bugs in staging
- [ ] E2E test passes: register → login → profile view → token refresh → logout

---

### Phase 3: Password Reset and GA Rollout (Milestone M3) — Weeks 6–9

**Objective:** Deliver password reset flow, resolve remaining gaps, execute phased production rollout, and achieve GA. Addresses JTBD-3 and completes the PRD scope.

**PRD Alignment:** Completes AUTH-E3 (password reset, admin audit logs). Migration Phases 2–3.

#### 3.1 Password Reset Implementation

| Endpoint | Requirement | Key Behaviors |
|----------|-------------|---------------|
| POST `/auth/reset-request` | FR-AUTH-005 | Email in body. Sends reset token via SendGrid. Same response regardless of registration (no enumeration). Token: 1-hour TTL, single-use. |
| POST `/auth/reset-confirm` | FR-AUTH-005 | Token + new password in body. Validates token, updates password hash via `PasswordHasher`. Invalidates all refresh tokens. |

- **Open question resolution needed:** OQ-PRD-001 (sync vs async email). Recommend async (queue-based) for resilience; proceed with async unless stakeholder overrides.
- **Gap resolution:** GAP-005 — define full request/response schemas for both endpoints before implementation.
- Implement email delivery monitoring and alerting (Risk #7 mitigation)
- Implement fallback support channel documentation for email delivery failures

#### 3.2 Admin Audit Log Query (GAP-003 Resolution)

- Implement query endpoint for auth event logs (persona Jordan requirement)
- Queryable by date range, user ID, event type
- Protected by admin role authorization
- Validates NFR-COMP-002 (SOC2 audit logging) end-to-end

#### 3.3 Security Hardening

1. **Penetration testing** before production (Risk #5 mitigation)
   - Focus areas: XSS token theft (R-001), brute force (R-002), user enumeration
2. **Security review** of `PasswordHasher`, `JwtService`, `TokenManager` implementations
3. Validate NIST SP 800-63B password policy compliance
4. Verify NFR-COMP-003 (data minimization): only email, hashed password, displayName collected
5. Confirm HttpOnly cookie configuration for refreshToken across all supported browsers

#### 3.4 Integration Wiring — Phase 3

**Named Artifact: SendGrid Email Service Integration**
- **Mechanism:** External API client (async queue recommended per OQ-PRD-001)
- **Wired Components:** `AuthService.resetRequest()` → email queue → SendGrid API
- **Owning Phase:** Phase 3 (Task 3.1)
- **Consumers:** POST `/auth/reset-request`

**Named Artifact: Feature Flag Cleanup Schedule**
- **Mechanism:** Feature flag service
- **Wired Components:** `AUTH_NEW_LOGIN` removed at GA, `AUTH_TOKEN_REFRESH` removed GA + 2 weeks
- **Owning Phase:** Phase 3 (Task 3.5)
- **Consumers:** All components previously gated

#### 3.5 Migration Phase 2: Beta 10% (2 weeks)

1. Enable `AUTH_NEW_LOGIN` for 10% of production traffic
2. Monitor continuously:
   - p95 latency < 200ms (NFR-PERF-001)
   - Error rate < 0.1%
   - Redis connection health
   - Registration conversion funnel (target >60%)
3. **Automatic rollback triggers:**
   - p95 latency > 1000ms for > 5 minutes
   - Error rate > 5% for > 2 minutes
   - Redis connection failures > 10/minute
   - Any `UserProfile` data corruption
4. Rollback procedure: disable `AUTH_NEW_LOGIN` → verify legacy login → investigate root cause

#### 3.6 Migration Phase 3: GA 100% (1 week)

1. Remove `AUTH_NEW_LOGIN` flag — all users on new `AuthService`
2. Enable `AUTH_TOKEN_REFRESH` for all users
3. Deprecate legacy auth system
4. Validate 99.9% uptime over 7 days (NFR-REL-001)
5. Remove `AUTH_TOKEN_REFRESH` flag at GA + 2 weeks
6. Activate 24/7 on-call rotation for auth-team (first 2 weeks post-GA)

#### Phase 3 Exit Criteria

- [ ] FR-AUTH-005 acceptance criteria 1–4 pass (reset request, confirm, expiry, single-use)
- [ ] GAP-002 resolved (logout endpoint live in production)
- [ ] GAP-003 resolved (admin audit log query operational)
- [ ] GAP-004 resolved (GDPR consent captured and stored)
- [ ] GAP-005 resolved (reset endpoint schemas fully specified and implemented)
- [ ] Penetration test complete with no critical or high findings unresolved
- [ ] All success criteria met (see Section 5)
- [ ] Production at 100% traffic with all dashboards green for 7 consecutive days
- [ ] Feature flags cleaned up
- [ ] Runbooks published and validated for Scenario 1 (service down) and Scenario 2 (refresh failures)
- [ ] On-call rotation active

---

## 3. Risk Assessment and Mitigation

### Technical Risks

| ID | Risk | Prob. | Impact | Phase | Mitigation | Contingency |
|----|------|-------|--------|-------|------------|-------------|
| R-001 | Token theft via XSS → session hijacking | Medium | High | 1 | accessToken in memory only; HttpOnly cookie for refreshToken; 15-min access TTL | Immediate revocation via `TokenManager`; force password reset for affected accounts |
| R-002 | Brute-force login attacks | High | Medium | 1 | Rate limit 10 req/min/IP; lockout after 5 failures in 15 min; bcrypt cost 12 | WAF IP blocking; CAPTCHA on `LoginPage` after 3 failures |
| R-003 | Data loss during legacy auth migration | Low | High | 3 | Parallel run during Phases 1-2; idempotent upserts; full DB backup before each phase | Rollback to legacy; restore from pre-migration backup |
| R-005 | Security breach from implementation flaws | Low | Critical | 3 | Dedicated security review + penetration testing pre-production | Incident response; emergency patch; forced password reset |

### Business/Product Risks

| # | Risk | Prob. | Impact | Phase | Mitigation |
|---|------|-------|--------|-------|------------|
| 4 | Low registration adoption (poor UX) | Medium | High | 3 | Usability testing before beta; iterate based on funnel analytics |
| 6 | Compliance failure (incomplete audit logging) | Medium | High | 1–2 | Define 12-month retention early (Phase 1); validate against SOC2 controls in Phase 2 QA |
| 7 | Email delivery failures blocking password reset | Low | Medium | 3 | SendGrid delivery monitoring + alerting; document fallback support channel |

### Architectural Risks

| Risk | Prob. | Impact | Mitigation |
|------|-------|--------|------------|
| Redis single point of failure for token refresh | Medium | High | Redis cluster with replication; graceful degradation (users re-login if Redis unavailable) |
| RSA key compromise | Low | Critical | Keys in Kubernetes secrets with RBAC; quarterly rotation; revocation procedure documented |
| Audit log retention conflict (GAP-001) | Resolved | — | 12-month retention per PRD/SOC2; explicitly overrides TDD's 90-day spec |

---

## 4. Resource Requirements and Dependencies

### Team Resources

| Role | Allocation | Phase Coverage | Key Responsibilities |
|------|-----------|----------------|---------------------|
| Backend engineer (2) | Full-time | Phases 1–3 | `AuthService`, `TokenManager`, `PasswordHasher`, `JwtService`, `UserRepo`, API endpoints |
| Frontend engineer (1) | Full-time | Phases 1–3 | `LoginPage`, `RegisterPage`, `AuthProvider`, `ProfilePage` |
| DevOps engineer (1) | Part-time | Phases 1, 2 | Infrastructure provisioning, CI/CD, observability, feature flags |
| QA engineer (1) | Part-time (P1), Full-time (P2-3) | Phases 1–3 | Test strategy execution, load testing, E2E automation |
| Security reviewer (1) | Part-time | Phase 3 | Penetration testing, security review |

### Infrastructure Dependencies (Pre-Phase 1)

| # | Dependency | Type | Required By | Status |
|---|-----------|------|-------------|--------|
| 1 | PostgreSQL 15+ | Database | Phase 1 start | Requires INFRA-DB-001 |
| 2 | Redis 7+ | Cache | Phase 1 start | Provisioning needed |
| 3 | Node.js 20 LTS | Runtime | Phase 1 start | Standard |
| 4 | Feature flag service | Infrastructure | Phase 1 start | Must support `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH` |
| 5 | RSA key pair (2048-bit) | Security | Phase 1 start | SEC-POLICY-001 governs |
| 6 | SendGrid API | External SaaS | Phase 3 start | Account + API key needed |
| 10 | Frontend routing framework | Internal | Phase 1 start | Must support client-side routing + token auth |

### Library Dependencies

| # | Library | Version | Component | Phase |
|---|---------|---------|-----------|-------|
| 4 | bcryptjs | Latest stable | `PasswordHasher` | 1 |
| 5 | jsonwebtoken | Latest stable | `JwtService` | 1 |

### Document Dependencies

| # | Document | Relationship | Required Resolution |
|---|----------|-------------|---------------------|
| 7 | AUTH-PRD-001 | Upstream requirements | Active (this roadmap) |
| 8 | INFRA-DB-001 | Database provisioning | Must be complete before Phase 1 |
| 9 | SEC-POLICY-001 | Security policy | Must be available for key management and password policy |

---

## 5. Success Criteria and Validation

### Technical Metrics

| # | Metric | Target | Validation Phase | Method |
|---|--------|--------|-----------------|--------|
| 1 | Login response time (p95) | < 200ms | Phase 2 (staging), Phase 3 (production) | APM on `AuthService.login()` — NFR-PERF-001 |
| 2 | Registration success rate | > 99% | Phase 2 | Ratio of successful registrations to valid attempts — FR-AUTH-002 |
| 3 | Token refresh latency (p95) | < 100ms | Phase 2 | APM on `TokenManager.refresh()` — FR-AUTH-003 |
| 4 | Service availability | 99.9% uptime | Phase 3 (7-day post-GA window) | Health check monitoring — NFR-REL-001 |
| 5 | Password hash time | < 500ms | Phase 1 | Benchmark `PasswordHasher.hash()` — NFR-SEC-001 |

### Business Metrics (Measured Post-GA)

| # | Metric | Target | Method | Timeline |
|---|--------|--------|--------|----------|
| 6 | Registration conversion | > 60% | Funnel analytics (`RegisterPage` → confirmed account) — FR-AUTH-002 | GA + 30 days |
| 7 | Daily active authenticated users | > 1000 | `AuthToken` issuance counts | GA + 30 days |
| 8 | Average session duration | > 30 minutes | Token refresh event analytics | GA + 30 days |
| 9 | Failed login rate | < 5% of attempts | Auth event log analysis | GA + 14 days |
| 10 | Password reset completion | > 80% | Funnel: reset requested → new password set | GA + 30 days |

### Compliance Validation

| Requirement | Validation Method | Phase |
|-------------|-------------------|-------|
| NFR-COMP-001 (GDPR consent) | Registration integration test asserts consent field stored with timestamp | Phase 1 |
| NFR-COMP-002 (SOC2 audit logging) | Audit log query returns events with required fields; 12-month retention verified | Phase 2 |
| NFR-COMP-003 (GDPR data minimization) | Schema review confirms only email, hashed password, displayName collected | Phase 1 |

### Test Coverage Targets

| Level | Target | Phase |
|-------|--------|-------|
| Unit | 80% on all backend components | Phase 1–2 |
| Integration | All API endpoints with DB + Redis | Phase 1–2 |
| E2E | Full user journey (register → login → profile → refresh → logout → password reset) | Phase 2–3 |
| Load | 500 concurrent logins (k6) | Phase 2 |
| Security | Penetration test with zero unresolved critical/high findings | Phase 3 |

---

## 6. Timeline Summary

| Phase | Duration | Weeks | Key Deliverables | Milestone |
|-------|----------|-------|------------------|-----------|
| **Phase 1: Core Auth** | 3 weeks | 1–3 | Login, registration, `AuthService` facade, `PasswordHasher`, `TokenManager`, `JwtService`, `UserRepo`, `LoginPage`, `RegisterPage`, `AuthProvider`, audit logging, GDPR consent | M1 |
| **Phase 2: Tokens + Profile** | 2 weeks | 4–5 | Token refresh, profile endpoint, logout, `ProfilePage`, observability, staging deployment, Internal Alpha | M2 |
| **Phase 3: Reset + GA** | 4 weeks | 6–9 | Password reset (2 endpoints), admin audit query, security hardening, Beta 10% (2 weeks), GA 100% (1 week), feature flag cleanup | M3 |
| **Post-GA stabilization** | 2 weeks | 10–11 | 24/7 on-call, metric validation, feature flag removal, post-mortem if needed | — |

**Total: 9 weeks to GA, 11 weeks including stabilization**

### Critical Path

```
INFRA-DB-001 + Redis provisioning
  → PasswordHasher + JwtService + UserRepo (parallel)
    → TokenManager (depends on JwtService + Redis)
      → AuthService facade (depends on all services)
        → API endpoints (depends on AuthService)
          → Frontend components (depends on API endpoints)
            → Staging deployment (Internal Alpha)
              → Beta 10% → GA 100%
```

### Open Questions Requiring Resolution

| ID | Question | Impact | Recommended Resolution | Blocking Phase |
|----|----------|--------|----------------------|----------------|
| OQ-001 | API key auth for service-to-service? | Scope expansion | Defer to v1.1; not blocking core auth | None |
| OQ-002 | Max `UserProfile` roles array length? | Schema constraint | Set to 20; enforce at `UserRepo` layer | Phase 1 |
| OQ-PRD-001 | Sync vs async password reset emails? | Architecture | Async (queue-based) for resilience | Phase 3 |
| OQ-PRD-002 | Max refresh tokens per user? | Redis storage | Set to 10; revoke oldest on overflow | Phase 2 |
| OQ-PRD-003 | "Remember me" extended sessions? | UX | Defer to v1.1; 7-day refresh is sufficient for v1.0 | None |
