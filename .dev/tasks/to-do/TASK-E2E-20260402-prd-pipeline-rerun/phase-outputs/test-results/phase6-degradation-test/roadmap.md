---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.55
adversarial: true
base_variant: "Haiku (Variant B)"
variant_scores: "A:71 B:81"
convergence_score: 0.72
debate_rounds: 2
prd_source: "test-prd-user-auth.md"
---

# User Authentication Service — Merged Project Roadmap

## Executive Summary

The User Authentication Service is a MEDIUM-complexity (0.55), security-critical feature delivering five functional requirements (FR-AUTH-001 through FR-AUTH-005), nine non-functional requirements, and four compliance mandates. The system follows a facade pattern with `AuthService` orchestrating `PasswordHasher`, `TokenManager`, `JwtService`, and `UserRepo` against PostgreSQL 15+, Redis 7+, and SendGrid.

**Business Drivers:**
1. **Personalization roadmap** — Enables ~$2.4M in projected annual revenue from identity-dependent personalization features planned for Q2-Q3 2026
2. **Compliance deadline** — Required for SOC2 Type II audit in Q3 2026 (user-level event logging, 12-month audit retention)
3. **Competitive positioning** — 25% of churned users cite missing user accounts as reason for leaving

**Key Technical Challenges:**
- Security surface is HIGH (0.8) — cryptographic operations (bcrypt cost 12, RS256 JWT), token lifecycle management, brute-force mitigation, XSS prevention
- Three external dependencies (PostgreSQL 15+, Redis 7+, SendGrid) with failover requirements
- Dual-token pattern (short-lived accessToken + long-lived refreshToken) requires careful state management across frontend and backend
- Parallel operation with legacy auth during rollout to mitigate data loss risk (R-003)

**Delivery Strategy:**
- 4-phase plan with explicit Phase 0 for design, OQ resolution, and infrastructure provisioning — eliminating ambiguity before coding starts
- Parallel frontend/backend development enabled by contract-first OpenAPI spec from Phase 0
- Early observability instrumentation from Phase 0 onwards — no blind development
- 12.5-week timeline with extended beta (minimum 10 days) to capture full refresh token lifecycle before GA
- Feature-flagged phased rollout (alpha → beta 10% → GA 100%) with explicit numeric rollback criteria

**Success Threshold:** Deliver all five functional requirements with latency < 200ms p95, 99.9% uptime, zero data loss during migration, and audit logging compliant with SOC2 Type II controls by Week 12.5.

---

## Phased Implementation Plan

### Phase 0: Design and Foundation (Weeks 1–2)

**Objective:** Establish security architecture, resolve all open questions, provision infrastructure, and prepare the team for parallel development tracks.

#### Architecture and Security Review

- Conduct threat model review: XSS mitigation (in-memory accessToken, HttpOnly refreshToken cookie), brute-force controls (rate limiting + account lockout), token revocation mechanism
- Validate JWT RS256 key generation (2048-bit RSA pair) and secure key storage strategy
- Review password hashing strategy: bcrypt cost factor 12 (~250ms hash time) with `PasswordHasher` abstraction enabling future argon2id migration without API change
- Document token lifecycle: accessToken (15-min JWT), refreshToken (7-day Redis-backed opaque token), revocation strategy
- Set up APM instrumentation skeleton so every `AuthService` method emits spans from day one

#### Open Question Resolution (OQ-001 through OQ-008)

| OQ | Question | Decision | Rationale |
|----|----------|----------|-----------|
| OQ-001 | API key auth for service-to-service? | Out of scope for v1.0 | JWT refresh pattern sufficient for Sam persona; API keys deferred to v1.1 |
| OQ-002 | Max roles array length? | Unbounded for v1.0 | Soft constraint documented (typical 3-5); add validation in Phase 1 if needed |
| OQ-003 | Sync vs async password reset emails? | Async via background queue | Avoids blocking login flow; SendGrid SLA 99.9%; monitor delivery failures |
| OQ-004 | Max refresh tokens per user? | Unbounded for v1.0 | Each login issues new token; token rotation in v1.1 if device limit required |
| OQ-005 | "Remember me" extended sessions? | Deferred to v1.1 | Product decision with UX implications; out of scope per PRD S12 |
| OQ-006 | Service-to-service auth for Sam? | JWT refresh pattern sufficient | Formalize as "Integration Auth" in v1.1 |
| OQ-007 | Admin API for log query + account unlock? | Account unlock endpoint required | `POST /admin/users/:id/unlock` for Jordan persona; log query API deferred to v1.1 |
| OQ-008 | Logout endpoint? | `POST /auth/logout` required | Alex persona explicitly needs logout; revokes refreshToken in Redis, clears client-side |

#### Infrastructure Setup

- Provision PostgreSQL 15+ with connection pooling (pgBouncer, max 100 connections)
- Provision Redis 7+ cluster with 1 GB RAM initial capacity; configure 7-day TTL eviction policy
- Set up Kubernetes pods (3 replicas initial, HPA scaling to 10 at CPU > 70%)
- Configure APM (Prometheus + Grafana) with span instrumentation for `AuthService` → `PasswordHasher` → database
- Set up testcontainers environment for integration tests (PostgreSQL + Redis ephemeral containers)
- Generate RSA 2048-bit key pair for `JwtService` RS256 signing
- Configure SendGrid API access and verify sender domain

#### Compliance and Policy Alignment

- Map NFR-COMP-001 through NFR-COMP-004 to audit log schema: fields = (timestamp, user_id, IP, event_type, outcome, success/failure_reason)
- Confirm 12-month audit log retention with compliance team (PRD NFR-COMP-002 overrides TDD 90-day default)
- Validate GDPR consent flow: capture consent checkbox at registration with timestamp in `UserProfile` table

#### Team and Communication

- Assign team roles: 2 backend engineers, 1 frontend engineer, 1 QA engineer, 1 security engineer (review liaison)
- Schedule weekly architecture sync (auth-team + security + platform teams)
- Create decision log for OQs resolved in Phase 0

**Deliverables:**
- Signed-off architecture design document (threat model, key management, token lifecycle diagram)
- PostgreSQL schema with `users`, `refresh_tokens`, `auth_events` tables
- OpenAPI spec for `/v1/auth/*` endpoints (enables parallel frontend development)
- Infrastructure as Code for K8s, RDS, ElastiCache provisioning
- Decision log (OQ-001 through OQ-008 with rationales)
- APM instrumentation skeleton in place
- Library dependencies confirmed (see Resource Requirements)

**Phase 0 Exit Criteria:**
- All critical OQs resolved by day 10
- PostgreSQL + Redis connectivity verified in dev/staging
- OpenAPI spec reviewed and signed off by frontend and backend leads
- Team training complete (auth architecture, bcrypt, JWT, Redis TTL)

---

### Phase 1: Core Auth, Registration, and Token Lifecycle (Weeks 3–7)

**Objective:** Deliver FR-AUTH-001, FR-AUTH-002, FR-AUTH-003, FR-AUTH-004 with unit/integration tests. Enable silent token refresh. Deploy to staging and run internal alpha validation.

#### Backend Development (2 engineers, 5 weeks)

**Week 3 — Component Skeleton:**
- Create `AuthService` facade with method signatures (login, register, getProfile, refreshToken, logout)
- Create `PasswordHasher` abstraction wrapping bcryptjs; unit tests asserting bcrypt cost = 12
- Create `TokenManager` with `issueTokens()`, `revokeRefreshToken()`, and `refresh()` signatures
- Create `JwtService` with RS256 sign/verify operations
- Create `UserRepo` CRUD methods (create, findByEmail, findById, updateLastLogin)
- Populate PostgreSQL schema: `users` table with (id UUID v4, email UNIQUE indexed lowercase, displayName 2-100 chars, passwordHash, createdAt, updatedAt, lastLoginAt nullable, roles default ["user"], gdprConsentAt)
- Create `failed_login_attempts` tracking table for brute-force mitigation
- Write idempotent migration scripts with rollback support

**Week 4 — Login and Token Issuance (FR-AUTH-001, FR-AUTH-003):**
- Implement `AuthService.login(email, password)`:
  - Fetch user from `UserRepo`; call `PasswordHasher.verify(password, stored_hash)`
  - On success: call `TokenManager.issueTokens(user_id)` → `AuthToken` with accessToken (JWT) + refreshToken (opaque)
  - On failure: increment failed_attempts counter; lock account after 5 failures within 15 min (FR-AUTH-001 AC4)
  - Identical error responses for invalid credentials and non-existent email (no user enumeration)
- Implement `TokenManager.issueTokens(user_id)`:
  - Call `JwtService.sign({ sub: user_id, roles: user.roles })` → accessToken (15-min expiry)
  - Generate opaque refreshToken; store in Redis with 7-day TTL
  - Return `AuthToken` object
- Implement `POST /v1/auth/login` — 10 req/min per IP rate limit
- Unit tests UT-001, UT-002: `AuthService` login flows; `PasswordHasher.verify()`; `TokenManager.issueTokens()`
- Integration test IT-001: login via HTTP → database query → Redis storage → response verification

**Week 5 — Registration (FR-AUTH-002):**
- Implement `AuthService.register(email, password, displayName)`:
  - Validate email format and uniqueness (query `UserRepo`)
  - Validate password strength (≥8 chars, ≥1 uppercase, ≥1 number)
  - Call `PasswordHasher.hash(password, cost=12)` → bcrypt hash
  - Call `UserRepo.create(email, hash, displayName)` → new `UserProfile`
  - Capture GDPR consent checkbox + timestamp (NFR-COMP-001)
  - Call `TokenManager.issueTokens(new_user_id)` → auto-login
  - Data minimization: only email, hashed password, displayName collected (NFR-COMP-004)
- Implement `POST /v1/auth/register` — 5 req/min per IP rate limit
- Unit tests for password validation, email uniqueness, bcrypt hashing
- Integration test: registration → database insert → JWT issuance → response

**Week 6 — Token Refresh and Profile (FR-AUTH-003, FR-AUTH-004):**
- Implement `TokenManager.refresh(refreshToken)`:
  - Validate refreshToken exists in Redis (not expired, not revoked)
  - Revoke old token from Redis before issuing new pair (rotation)
  - Issue new `AuthToken` pair (new accessToken, new refreshToken)
- Implement `AuthService.getProfile(user_id)`:
  - Fetch `UserProfile` from `UserRepo`; update `lastLoginAt`
  - Return full profile: id, email, displayName, createdAt, updatedAt, lastLoginAt, roles
- Implement `AuthService.logout(refreshToken)`:
  - Revoke refreshToken in Redis; return success
- Implement `POST /v1/auth/refresh` — 30 req/min per user
- Implement `GET /v1/auth/me` — 60 req/min per user, Bearer token auth
- Implement `POST /v1/auth/logout` — revokes refresh token
- Unit tests for token refresh, expiry validation, revocation logic
- Integration test: refresh flow → Redis TTL update → new token issuance
- Concurrent authentication load test baseline (NFR-PERF-002: 500 concurrent logins)

**Week 7 — Testing and Stabilization:**
- Achieve 80% unit test coverage across AuthService, PasswordHasher, TokenManager, JwtService
- Run integration test suite against testcontainers (PostgreSQL + Redis)
- Performance baseline: measure `AuthService.login()` latency (target < 200ms p95)
- Load test with k6: 500 concurrent logins → confirm response time target
- Security checklist: no password logging, no plaintext tokens in logs, no SQL injection vectors
- Bug fixes from testing; iterate until no critical issues

#### Frontend Development (1 engineer, parallel from Week 3)

**Weeks 3–4 — LoginPage and AuthProvider:**
- Create `AuthProvider` context component:
  - State: `{ authToken, user, isLoading, error }`
  - Methods: `login(email, password)`, `register(email, password, displayName)`, `logout()`, `refreshToken()`
  - Token storage: accessToken in memory only (XSS mitigation per R-001); refreshToken in HttpOnly cookie
  - Auto-refresh logic: when accessToken nears expiry (< 2 min), call `refreshToken()` silently
  - Clear tokens on tab close
- Create `LoginPage` component:
  - Form fields: email, password
  - Client-side validation: email format, password non-empty
  - Generic error messages (no user enumeration)
  - Success: call `AuthProvider.login()` → redirect to dashboard

**Weeks 5–6 — RegisterPage and ProtectedRoutes:**
- Create `RegisterPage` component:
  - Form fields: email, password, password confirmation, display name
  - GDPR consent checkbox (required, per NFR-COMP-001)
  - Inline password strength feedback; `termsUrl` prop for legal compliance link
  - Success: call `AuthProvider.register()` → auto-login → redirect to dashboard
- Create `ProtectedRoute` wrapper:
  - Check `AuthProvider.authToken` exists and is valid
  - If missing/expired and no refreshToken: redirect to LoginPage
- Create `ProfilePage` component:
  - Display: email, displayName, account creation date
  - Logout button (calls `AuthProvider.logout()`)

**Week 7 — E2E Testing and UX Polish:**
- E2E test E2E-001: user journey from landing → RegisterPage → login → ProfilePage
- Test token refresh: navigate between pages → confirm background refresh → no re-login
- Test error cases: invalid password, duplicate email, weak password, account lockout
- Accessibility: form labels, error announcements, keyboard navigation

#### Phase 1 Compliance Gate

Before proceeding to Phase 2, validate:
- GDPR consent field captured at registration with timestamp (NFR-COMP-001)
- Audit log table schema includes: user ID, timestamp, IP address, outcome (NFR-COMP-002)
- Raw passwords never appear in logs or database (NFR-COMP-003)
- Data minimization — no PII beyond email, hash, displayName (NFR-COMP-004)

#### Phase 1 Alpha Validation (End of Week 7)

- Feature flag `AUTH_NEW_LOGIN` = OFF (legacy auth remains default)
- Deploy to staging; enable flag for auth-team and QA only
- Smoke test: alpha users register and log in without issues
- Latency validation: p95 < 200ms confirmed via APM
- Load test: 500 concurrent requests → response time under 500ms
- Security review sign-off from security-engineer

**Phase 1 Exit Criteria:**
- FR-AUTH-001 (login), FR-AUTH-002 (registration), FR-AUTH-003 (token refresh), FR-AUTH-004 (profile) pass acceptance criteria
- Performance: p95 latency < 200ms for login, register, refresh, profile
- Test coverage: 80% unit, 15% integration across backend components
- Phase 1 compliance gate passed
- Zero P0/P1 bugs; security review sign-off

---

### Phase 2: Password Reset, Audit Logging, and Observability (Weeks 8–10)

**Objective:** Deliver FR-AUTH-005 (password reset), production-grade audit logging for SOC2 compliance, observability hardening, and launch beta at 10% traffic.

#### Backend Development (2 engineers, 3 weeks)

**Week 8 — Password Reset Flow (FR-AUTH-005):**
- Implement `PasswordResetTokenManager`:
  - `generateResetToken(user_id)` → opaque token, stored in PostgreSQL with 1-hour TTL + single-use flag
  - `validateResetToken(token)` → check exists, not expired, not used
  - `markTokenUsed(token)` → prevent reuse
- Implement `AuthService.resetRequest(email)`:
  - Find user by email; return success regardless (no enumeration)
  - Generate reset token; queue async email job via SendGrid
  - Log event: `AUTH_RESET_REQUESTED`
- Implement `AuthService.resetConfirm(token, newPassword)`:
  - Validate token; hash new password via `PasswordHasher`; update database
  - Mark token as used; revoke all refresh tokens for user (clear from Redis)
  - Log event: `AUTH_PASSWORD_RESET`
- Implement `POST /v1/auth/reset-request` — 5 req/min per IP
- Implement `POST /v1/auth/reset-confirm` — validates token + new password
- Integration test: full reset flow (request → email → confirm → login with new password)

**Week 9 — Audit Logging, Compliance, and Observability Hardening:**
- Create `AuditLogger` service:
  - Method `log(event_type, user_id, ip_address, outcome, details)` → structured log to PostgreSQL `auth_events` table
  - 12-month retention enforced by scheduled cleanup job
  - Non-blocking: audit logging failures do not fail auth operations
- Integrate AuditLogger into all AuthService methods (login, register, resetRequest, resetConfirm, getProfile, logout)
- Verify all compliance controls:
  - NFR-COMP-001: GDPR consent with timestamp at registration
  - NFR-COMP-002: SOC2 audit logging with 12-month retention
  - NFR-COMP-003: NIST password hashing (bcrypt cost 12; never logged)
  - NFR-COMP-004: GDPR data minimization
- Implement `POST /admin/users/:id/unlock` for Jordan persona (OQ-007)
- Harden observability stack:
  - **Prometheus metrics:** `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total`, `redis_connection_errors_total`
  - **Alerts:** Login failure rate > 20% over 5 min; p95 latency > 500ms; Redis failures > 10/min; email delivery > 10% failures over 1 hour
  - **OpenTelemetry tracing:** Spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`
  - **Structured logging:** All auth events with user ID, timestamp, IP, outcome
- Performance validation:
  - NFR-PERF-001: All auth endpoints < 200ms at p95
  - NFR-PERF-002: 500 concurrent login requests (k6 load test)
  - Token refresh latency < 100ms at p95
  - Password hash time < 500ms with bcrypt cost 12
- Penetration testing of all auth endpoints

**Week 10 — Beta Deployment (10% traffic):**
- Deploy to production with `AUTH_NEW_LOGIN` = OFF
- Enable `AUTH_NEW_LOGIN` for 10% of production traffic
- Monitor metrics:
  - p95 latency < 200ms
  - Error rate < 0.5%
  - Email delivery > 99.5%
  - Password reset completion > 80%
  - Zero data loss or corruption
  - Audit log ingestion: zero failures
- E2E test: full password reset user journey
- Load test: 500 concurrent resets + refresh requests

#### Persona-Driven Validation

- **Alex (end user):** Registration completes in under 60 seconds; session persists across page refreshes; password reset email arrives within 60 seconds; logout works cleanly
- **Sam (API consumer):** Programmatic token refresh works without user interaction; clear error codes returned; expired tokens produce actionable 401 responses
- **Jordan (admin):** Account unlock endpoint operational; audit logs queryable by date range and user; failed login visibility confirmed

**Phase 2 Exit Criteria:**
- FR-AUTH-005 (password reset) passes acceptance criteria
- NFR-COMP-001 through NFR-COMP-004 validated
- All observability dashboards operational; alerts firing correctly
- Beta metrics: p95 latency < 200ms, error rate < 0.5%
- Security review sign-off for password reset + audit logging
- Penetration test completed with no critical findings

---

### Phase 3: Production GA and Stabilization (Weeks 10.5–12.5)

**Objective:** Extended beta validation capturing full refresh token lifecycle, GA cutover, legacy deprecation, and post-launch stabilization.

#### Extended Beta Period (Week 10.5–11.5, minimum 10 days)

The debate identified that a 7-day refresh token TTL means the first forced re-authentication occurs at the beta boundary. To capture at least one full refresh lifecycle before GA:

- Beta (10% traffic) runs for minimum 10 days (started mid-Week 10)
- Monitor daily:
  - p95 login latency: target < 200ms
  - Error rate: target < 0.5%; rollback if > 2%
  - Token refresh success rate across the 7-day TTL boundary
  - Email delivery: target > 99.5%
  - Password reset completion: target > 80%
  - Zero data loss or corruption incidents
  - Audit log completeness
- Validate that users who logged in on beta Day 1 successfully re-authenticate after Day 7 (refresh token expiry)

#### GA Cutover (Week 11.5–12)

- If all metrics green: enable `AUTH_NEW_LOGIN` for remaining 90% of traffic
- Enable `AUTH_TOKEN_REFRESH` for silent refresh in `AuthProvider`
- Parallel legacy auth operation: both pathways live; gradual user migration as sessions expire
- Verify failover: if `AuthService` pod crashes, confirm fallback to legacy auth works
- Capacity: confirm HPA settings (3 replicas baseline → 10 at CPU > 70%)

#### Stabilization and Deprecation (Week 12–12.5)

- Monitor production metrics at 100% traffic:
  - Uptime: 99.9% target (< 43 min downtime/month)
  - p95 latency: < 200ms sustained
  - Error rate: < 0.1%
  - Cache hit rate (Redis): > 95% for refresh tokens
- Deprecate legacy auth:
  - Disable legacy login endpoint; legacy token holders forced to re-login via new AuthService
  - Purge legacy session data
  - Update documentation and API references to `/v1/auth/*` endpoints
- Remove feature flags:
  - Delete `AUTH_NEW_LOGIN` flag (new auth now default)
  - Keep `AUTH_TOKEN_REFRESH` for 2 weeks post-GA; delete after stabilization (Week 14+)
- Run runbook drills:
  - Scenario 1: AuthService down → check pod health → restart → failover to read replica
  - Scenario 2: Redis failures → verify connectivity → restart TokenManager pods → users re-login
  - Scenario 3: Email delivery failures → check SendGrid → verify queue → manual support fallback
- Post-launch analysis:
  - Calculate actual success metrics vs. targets (all 10 criteria)
  - Measure business impact: registration conversion, DAU, session duration, failed login rate
  - Document lessons learned

#### Rollback Criteria

Immediate rollback triggered if any condition occurs during beta or GA:
- p95 latency > 1000ms for > 5 minutes
- Error rate > 5% for > 2 minutes
- `TokenManager` Redis connection failures > 10/minute
- Any data loss or corruption in `UserProfile` records

Rollback mechanism: disable `AUTH_NEW_LOGIN` feature flag (< 5 minute execution).

**Phase 3 Exit Criteria:**
- 99.9% uptime measured over rolling 7-day window post-GA
- p95 latency < 200ms sustained under production load
- Error rate < 0.1%
- Zero data loss post-cutover
- All 10 success criteria met (see Success Criteria section)
- Audit trail complete per SOC2 requirements
- Legacy auth fully deprecated
- On-call team trained with runbook drills completed

---

## Integration Points and Dispatch Mechanisms

### AuthService Facade (Dispatch Table)

- **Named Artifact:** `AuthService` method dispatch — all external consumers call `AuthService` exclusively
- **Wired Components:** `PasswordHasher`, `TokenManager`, `UserRepo`, `JwtService` (indirect via `TokenManager`), `AuditLogger`
- **Owning Phase:** Phase 1 creates the facade with `PasswordHasher` + `UserRepo` + `TokenManager`; Phase 2 adds `AuditLogger`
- **Consumers:** LoginPage, RegisterPage, ProfilePage, `/v1/auth/*` endpoints

### TokenManager to JwtService Wiring

- **Named Artifact:** `TokenManager` dependency on `JwtService` for JWT sign/verify
- **Wired Components:** `JwtService` (RS256 signing), Redis (refresh token storage and revocation)
- **Owning Phase:** Phase 1 creates and wires this mechanism
- **Cross-References:** Phase 2 (reset invalidates tokens), Phase 1 (`AuthProvider` silent refresh), Phase 3 (feature flag `AUTH_TOKEN_REFRESH`)

### AuthProvider to API Binding

- **Named Artifact:** `AuthProvider` React context — binds frontend auth state to backend API
- **Wired Components:** `LoginPage`, `RegisterPage`, `ProfilePage` consume context; `AuthProvider` calls `/v1/auth/login`, `/v1/auth/refresh`, `/v1/auth/me`, `/v1/auth/logout`
- **Owning Phase:** Phase 1 creates the context provider and wires all page components
- **Cross-References:** Phase 3 rollout gates frontend behind `AUTH_NEW_LOGIN` flag

### Feature Flag Registry

| Flag | Purpose | Default | Cleanup Target |
|------|---------|---------|----------------|
| `AUTH_NEW_LOGIN` | Gates new `LoginPage` and `AuthService` login endpoint | OFF | Remove after GA (Week 12) |
| `AUTH_TOKEN_REFRESH` | Enables refresh token flow in `TokenManager` | OFF | Remove GA + 2 weeks (Week 14+) |

- **Wired Components:** API gateway routing, `AuthProvider` refresh logic, `LoginPage`/`RegisterPage` rendering
- **Owning Phase:** Phase 1 creates; Phase 3 progressively enables and cleans up

### Rate Limiting Configuration

| Endpoint | Limit | Keyed By | Owning Phase |
|----------|-------|----------|--------------|
| `POST /v1/auth/login` | 10 req/min | IP | Phase 1 |
| `POST /v1/auth/register` | 5 req/min | IP | Phase 1 |
| `GET /v1/auth/me` | 60 req/min | User | Phase 1 |
| `POST /v1/auth/refresh` | 30 req/min | User | Phase 1 |
| `POST /v1/auth/reset-request` | 5 req/min | IP | Phase 2 |
| `POST /v1/auth/reset-confirm` | 5 req/min | IP | Phase 2 |

---

## Risk Assessment and Mitigation Strategies

| Risk ID | Title | Severity | Probability | Impact | Mitigation | Contingency | Owner | Monitoring |
|---------|-------|----------|-------------|--------|------------|-------------|-------|------------|
| **R-001** | Token theft via XSS | HIGH | Medium | High | Store accessToken in memory only (not localStorage). HttpOnly + Secure + SameSite cookies for refreshToken. 15-min expiry. `AuthProvider` clears on tab close. CSP headers. Input sanitization. | Immediate token revocation via `TokenManager`. Force password reset for affected accounts. Post-incident notification. | security-engineer | APM traces for token events; CSP violation logs |
| **R-002** | Brute-force attacks on login | HIGH | High | Medium | API Gateway rate limiting: 10 req/min per IP. Account lockout: 5 failed attempts within 15 min. bcrypt cost 12 (~250ms/hash). CAPTCHA after 3 failures. | IP blocking at WAF. Regional CAPTCHA enablement. Advanced threat detection rules. | platform-team | Failed login counter; IP blocklist length; rate limit violations |
| **R-003** | Data loss during migration | HIGH | Low | High | Run `AuthService` in parallel with legacy during Phases 1–3. Idempotent upsert operations. Full database backup before each phase. Test restore procedure. Gradual rollout (beta 10% → GA). | Rollback to legacy via feature flag in < 5 minutes. Restore from pre-migration backup. Incident post-mortem. | backend-lead | Backup completion logs; restore test success; row count validation |
| **R-004** | Low registration adoption | HIGH | Medium | High | Usability testing before beta. Funnel analytics: landing → register → confirmed. A/B test form simplification. Monitor conversion target (> 60% per PRD S19). | Iterate RegisterPage design based on funnel data. Reduce required fields in v1.1. Add password strength meter. | frontend-lead | Funnel analytics; conversion rate dashboard |
| **R-005** | Security breach from flaws | CRITICAL | Low | Critical | Dedicated security review in Phase 0 (threat model). Penetration testing in Phase 2 (before GA). SAST in CI/CD. Dependency scanning for CVEs. | Immediate patch release. Security advisory. Affected user password reset. Incident response activation. | security-engineer | SAST scan results; pentest findings; CVE alerts |
| **R-006** | Incomplete audit logging | HIGH | Medium | High | Define log schema in Phase 0. Validate against SOC2 controls in Phase 2. Map all auth events to log entries. Confirm 12-month retention. Phase 1 compliance gate catches early gaps. | Backfill missing logs from backup. Document gaps for compliance team. | compliance-officer | Log completeness check; retention policy enforcement; audit report |
| **R-007** | Email delivery failures | MEDIUM | Low | Medium | SendGrid SLA 99.9%. Retry logic (3 attempts, exponential backoff). Delivery monitoring dashboard. Fallback support channel documented. | Manual password reset by support. In-app notification of delivery delay. | backend-lead | SendGrid bounce rate; reset email latency; support ticket volume |

---

## Resource Requirements and Dependencies

### Team Composition

| Role | Count | Weeks | Responsibility |
|------|-------|-------|----------------|
| Backend Engineer | 2 | 12.5 | AuthService, PasswordHasher, TokenManager, AuditLogger, password reset |
| Frontend Engineer | 1 | 12.5 | LoginPage, RegisterPage, ProfilePage, AuthProvider, E2E tests |
| QA Engineer | 1 | 12.5 | Test strategy, regression, load testing, security checklist |
| Security Engineer | 1 | 4 weeks (Phases 0, 1, 2, 3) | Threat model, code review, penetration testing, SOC2 validation |
| Product Manager | 1 | 2 weeks (Phases 0, 2, 3) | Requirements clarification, success metrics, stakeholder communication |
| Platform/DevOps Engineer | 1 | 2 weeks (Phases 0, 3) | Infrastructure provisioning, CI/CD, monitoring, on-call runbooks |

**Total Effort:** ~55 person-weeks

### Infrastructure Dependencies

| Resource | Version | Owner | Lead Time | Impact if Unavailable |
|----------|---------|-------|-----------|----------------------|
| PostgreSQL | 15+ | Platform team | 1 week | Cannot persist users; service non-functional |
| Redis | 7+ (1 GB) | Platform team | 1 week | Token refresh unavailable; users must re-login each session |
| Node.js | 20 LTS | Engineering | Available | Service cannot run |
| Kubernetes | 3+ nodes | Platform team | Available | Cannot scale AuthService |
| SendGrid | API | Platform team | 2-3 days | Password reset flow blocked |
| RSA key pair | 2048-bit | Security team | 1 day | JWT signing impossible |
| APM (Prometheus + Grafana) | — | Platform team | 1 week | Cannot measure performance or alert |

### Library Dependencies

| Library | Purpose | Component |
|---------|---------|-----------|
| bcryptjs | Password hashing (cost 12) | `PasswordHasher` |
| jsonwebtoken | JWT sign/verify (RS256) | `JwtService` |
| Jest + ts-jest | Unit testing | All backend |
| Supertest | API integration testing | All endpoints |
| testcontainers | CI database/cache testing | Integration tests |
| Playwright | E2E testing | Frontend flows |
| k6 | Load testing | Phase 1/2 performance |

---

## Success Criteria and Validation Approach

| # | Metric | Target | Source | Validation Phase | Measurement Method | Owner |
|---|--------|--------|--------|-----------------|-------------------|-------|
| 1 | Login response time (p95) | < 200ms | TDD + PRD S19 | Phase 1, 3 | APM histogram on `AuthService.login()` | backend-lead |
| 2 | Registration success rate | > 99% | TDD | Phase 1, 3 | Ratio of successful registrations to attempts | backend-lead |
| 3 | Token refresh latency (p95) | < 100ms | TDD | Phase 1, 3 | APM histogram on `POST /auth/refresh` | backend-lead |
| 4 | Service availability | 99.9% uptime | NFR-REL-001 | Phase 3 (post-GA) | Health check monitoring, 30-day window | platform-engineer |
| 5 | Password hash time | < 500ms | TDD | Phase 1 (unit test) | Benchmark `PasswordHasher.hash()` bcrypt cost 12 | backend-lead |
| 6 | Registration conversion rate | > 60% | PRD S19 | Phase 2, 3 | Funnel: landing → register → confirmed | product-manager |
| 7 | Daily active authenticated users | > 1000 within 30 days | PRD S19 | Phase 3 (post-launch) | Unique user IDs in `AuthToken` issuance over 24hr | product-manager |
| 8 | Average session duration | > 30 minutes | PRD S19 | Phase 3 (post-launch) | Token refresh event analytics | product-manager |
| 9 | Failed login rate | < 5% of attempts | PRD S19 | Phase 2, 3 | Auth event log analysis | backend-lead |
| 10 | Password reset completion | > 80% | PRD S19 | Phase 2, 3 | Funnel: requested → new password set | product-manager |

### Validation Gates

**Phase 1 Gate (Week 7):** Metrics 1, 2, 3, 5 must pass. Compliance gate must pass. Zero P0/P1 bugs. Security review sign-off.

**Phase 2 Gate (Week 10):** Metrics 3, 9, 10 must pass. All compliance controls validated. Beta error rate < 1%. Penetration test clear.

**Phase 3 Gate (Week 12.5):** All 10 metrics published in post-launch report. 99.9% uptime over 7 days. Legacy deprecated. On-call team operational.

---

## Timeline Summary

| Phase | Weeks | Duration | Key Milestone |
|-------|-------|----------|---------------|
| Phase 0: Design and Foundation | 1–2 | 2 weeks | Architecture signed off, OQs resolved, infrastructure ready |
| Phase 1: Core Auth and Registration | 3–7 | 5 weeks | FR-AUTH-001/002/003/004 live, alpha on staging, compliance gate passed |
| Phase 2: Password Reset, Audit, Observability | 8–10 | 3 weeks | FR-AUTH-005 live, SOC2 controls validated, beta 10% launched |
| Phase 3: GA and Stabilization | 10.5–12.5 | 2.5 weeks | Extended beta (10+ days), GA 100%, legacy deprecated |
| **Total** | | **12.5 weeks** | All 5 FRs delivered, all 10 success metrics measurable |

### Operational Readiness (Post-GA)

- **On-call:** 24/7 auth-team rotation for first 2 weeks post-GA
- **Escalation path:** auth-team on-call (15 min SLA) → test-lead (30 min) → eng-manager (1 hr) → platform-team (critical infra)
- **Capacity:** HPA scales `AuthService` pods to 10 at CPU > 70%
- **Dashboards:** Latency (p50/p95/p99 by endpoint), error rate (by type), capacity (PostgreSQL pool, Redis memory, pod CPU), business metrics (conversion, DAU, session duration)
