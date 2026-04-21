---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.55
complexity_class: "MEDIUM"
primary_persona: architect
generated_at: "2026-04-02T12:00:00Z"
total_phases: 4
total_duration_weeks: 12
risk_count: 7
dependencies_count: 8
success_criteria_count: 10
---

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service is a MEDIUM-complexity (0.55), security-critical feature that unblocks three strategic business priorities:

1. **Personalization roadmap** — Enables $2.4M in projected Q2-Q3 2026 revenue from identity-dependent personalization features
2. **Compliance audit** — Required for SOC2 Type II audit in Q3 2026 (user-level event logging, 12-month audit retention)
3. **Competitive positioning** — 25% of churned users cite missing user accounts as reason for leaving

**Key Technical Challenges:**
- Security surface is HIGH (0.8) — cryptographic operations (bcrypt cost 12, RS256 JWT), token lifecycle management, brute-force mitigation, XSS prevention
- Three external dependencies (PostgreSQL 15+, Redis 7+, SendGrid) with failover requirements
- Dual-token pattern (short-lived accessToken + long-lived refreshToken) requires careful state management
- Parallel operation with legacy auth during Phases 1-2 to mitigate data loss risk (R-003)

**Architect's Perspective:**
The architecture is sound and well-understood. The facade pattern (`AuthService` orchestrating `PasswordHasher`, `TokenManager`, `JwtService`, `UserRepo`) provides clean separation of concerns. The 0.55 complexity score reflects a mature, battle-tested auth design — not novel infrastructure. Risk mitigation strategy focuses on operational safeguards (rate limiting, account lockout, backup/restore) and staged rollout (alpha → beta 10% → GA) rather than architectural redesign.

**Success Threshold:** Deliver all five functional requirements (FR-AUTH-001 through FR-AUTH-005) with latency < 200ms p95, 99.9% uptime, zero data loss during migration, and audit logging compliant with SOC2 Type II controls by end of Phase 3 (12 weeks).

---

## Phased Implementation Plan

### Phase 0: Design & Foundation (Weeks 1-2)

**Objective:** Establish security architecture, resolve ambiguities, and prepare infrastructure and team for development.

**Key Activities:**

1. **Architecture & Security Review**
   - Conduct threat model review: XSS mitigation (in-memory accessToken, HttpOnly refreshToken cookie), brute-force controls (rate limiting + account lockout), token revocation mechanism
   - Validate JWT RS256 key generation (2048-bit RSA pair) and secure key storage strategy (AWS Secrets Manager or equivalent)
   - Review password hashing strategy: bcrypt cost factor 12 (≈ 250ms hash time) vs. alternative (argon2id) — architect recommends bcrypt for v1.0 given time constraint, with `PasswordHasher` abstraction enabling future migration without API change
   - Document token lifecycle: accessToken (15 min JWT), refreshToken (7-day Redis-backed opaque token), revocation strategy

2. **Resolve Open Questions (OQ-001 through OQ-008)**
   - OQ-001: API key auth for service-to-service calls — **Decision:** Out of scope for v1.0; JWT refresh pattern sufficient for programmatic integrations (Sam persona). API keys deferred to v1.1.
   - OQ-002: Max roles array length — **Decision:** Unbounded for v1.0; documented in `UserProfile` schema as soft constraint (typical max 3-5 roles). Add validation in Phase 1b if needed.
   - OQ-003: Async password reset emails — **Decision:** Async via background queue (Celery/Bull) to avoid blocking login flow. SendGrid delivery SLA: 99.9%; monitor delivery failures and alert support team.
   - OQ-004: Max refresh tokens per user — **Decision:** Unbounded for v1.0; each login issues new token. Implement token rotation in v1.1 if device limit required.
   - OQ-005: "Remember me" extended session — **Decision:** Out of scope for v1.0. Implement via refreshToken TTL extension in v1.1.
   - OQ-006: Service-to-service auth mechanism for Sam persona — **Decision:** JWT refresh pattern sufficient; Sam can exchange credentials for long-lived refreshToken and use refresh loop. Formalize as "Integration Auth" in v1.1.
   - OQ-007: Admin API for log querying and account unlock — **Decision:** Account unlock endpoint (`POST /admin/users/:id/unlock`) required for Jordan persona. Log query API deferred to v1.1; interim solution: direct database query access for auth-team.
   - OQ-008: Logout endpoint — **Decision:** `POST /auth/logout` required for Alex persona. Revokes refreshToken in Redis; clears accessToken client-side.

3. **Infrastructure Setup**
   - Provision PostgreSQL 15+ with connection pooling (pgBouncer, max 100 connections)
   - Provision Redis 7+ cluster with 1 GB RAM initial capacity; configure 7-day TTL eviction policy
   - Set up Kubernetes pods (3 replicas initial, HPA scaling to 10 at CPU > 70%)
   - Configure APM (DataDog or Prometheus + Grafana) with span instrumentation for `AuthService` → `PasswordHasher` → database
   - Set up testcontainers environment for integration tests (PostgreSQL + Redis ephemeral containers)

4. **Compliance & Policy Alignment**
   - Map NFR-COMP-001 through NFR-COMP-004 to audit log schema: log fields = (timestamp, user_id, IP, event_type, outcome, success/failure_reason)
   - Confirm 12-month audit log retention with compliance team (PRD NFR-COMP-002 overrides TDD 90-day default)
   - Validate GDPR consent flow: capture consent checkbox at registration with timestamp in `UserProfile` table

5. **Team & Communication**
   - Assign team roles: 2 backend engineers (FR-AUTH-001/002 lead + FR-AUTH-003/004 lead), 1 frontend engineer (UI), 1 QA engineer, 1 security engineer (review liaison)
   - Schedule weekly architecture sync (auth-team + security + platform teams)
   - Create decision log for OQs resolved in Phase 0 (prevents rework in Phase 1)

**Deliverables:**
- Signed-off architecture design document (threat model, key management strategy, token lifecycle diagram)
- PostgreSQL schema with `users`, `refresh_tokens`, `auth_events` tables
- OpenAPI spec for `/v1/auth/*` endpoints (borrowed from extraction)
- Infrastructure as Code (Terraform) for K8s, RDS, ElastiCache provisioning
- Decision log (OQ-001 through OQ-008 with rationales)

**Success Criteria:**
- All critical OQs resolved by day 10
- PostgreSQL + Redis connectivity verified in dev/staging
- APM instrumentation skeleton in place
- Team training complete (auth architecture, bcrypt, JWT, Redis TTL)

---

### Phase 1: Core Auth & Registration (Weeks 3-7, 5 weeks)

**Objective:** Deliver FR-AUTH-001, FR-AUTH-002, FR-AUTH-003, FR-AUTH-004 with unit/integration tests. Enable silent token refresh. Deploy to staging and run internal alpha validation.

**Requirement Focus:**
- **FR-AUTH-001:** Login with email/password, bcrypt verification, account lockout after 5 failed attempts within 15 minutes
- **FR-AUTH-002:** User registration with email uniqueness, password strength validation, `UserProfile` creation
- **FR-AUTH-003:** JWT issuance (15-min accessToken, 7-day refreshToken), silent refresh via `TokenManager`
- **FR-AUTH-004:** GET `/auth/me` returns authenticated `UserProfile` with id, email, displayName, roles, timestamps

**Architecture: Component Wiring**

| Named Artifact | Purpose | Wiring | Owning Phase | Consumers |
|---|---|---|---|---|
| **AuthService Facade** | Orchestrates login, registration, profile retrieval | Wires `PasswordHasher`, `TokenManager`, `UserRepo` | Phase 1 | LoginPage, RegisterPage, ProfilePage |
| **TokenManager State** | Manages JWT + refresh token lifecycle | Wires `JwtService` (sign/verify), Redis (storage + revocation) | Phase 1 | AuthService, `/auth/refresh` endpoint |
| **Feature Flag: AUTH_NEW_LOGIN** | Gates new login/register paths | Default OFF; enabled in Phase 1 alpha → Phase 2 beta → Phase 3 GA | Phase 1 | Router; legacy auth path remains active |
| **PasswordHasher Abstraction** | One-way password hashing (bcrypt cost 12) | Encapsulates bcryptjs library; enables future argon2id migration | Phase 1 | AuthService.login(), AuthService.register() |
| **JwtService Signing Key Pair** | RS256 key management (2048-bit RSA) | Keys stored in AWS Secrets Manager; rotated annually | Phase 1 | TokenManager.issueTokens() |

**Backend Development (2 engineers, 5 weeks)**

**Week 3 (Component Skeleton):**
- Create `AuthService` facade with method signatures (login, register, getProfile, refreshToken)
- Create `PasswordHasher` abstraction wrapping bcryptjs; write unit tests asserting bcrypt cost = 12
- Create `TokenManager` with `issueTokens()` and `revokeRefreshToken()` signatures
- Create `JwtService` with RS256 sign/verify operations
- Create `UserRepo` CRUD methods (create, findByEmail, findById, updateLastLogin)
- Populate PostgreSQL schema: `users` table with (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles, passwordHash)
- **Integration points:** None wired yet; just signatures

**Week 4 (Login & Token Issuance):**
- Implement `AuthService.login(email, password)`:
  - Fetch user from `UserRepo`
  - Call `PasswordHasher.verify(password, stored_hash)`
  - On success: call `TokenManager.issueTokens(user_id)` → get `AuthToken` with accessToken (JWT) + refreshToken (opaque)
  - On failure: increment failed_attempts counter; lock account after 5 failures within 15 min
  - **Wiring complete:** AuthService → PasswordHasher, TokenManager
- Implement `TokenManager.issueTokens(user_id)`:
  - Call `JwtService.sign({ sub: user_id, roles: user.roles })` → accessToken (15-min expiry)
  - Generate opaque refreshToken; store in Redis with 7-day TTL
  - Return `AuthToken` object
  - **Wiring complete:** TokenManager → JwtService, Redis
- Implement `POST /auth/login` endpoint (no auth required)
- Write unit tests for `AuthService.login()`, `PasswordHasher.verify()`, `TokenManager.issueTokens()` (target 80% coverage)
- Write integration test: login via HTTP → database query → Redis storage → response verification
- **Milestone:** Login path working end-to-end

**Week 5 (Registration):**
- Implement `AuthService.register(email, password, displayName)`:
  - Validate email format and uniqueness (query `UserRepo`)
  - Validate password strength (>= 8 chars, >=1 uppercase, >=1 number)
  - Call `PasswordHasher.hash(password, cost=12)` → bcrypt hash
  - Call `UserRepo.create(email, hash, displayName)` → new `UserProfile`
  - Call `TokenManager.issueTokens(new_user_id)` → auto-login
  - Capture GDPR consent checkbox + timestamp
  - Return `UserProfile` object
- Implement `POST /auth/register` endpoint (no auth required); rate limit to 5 req/min per IP
- Write unit tests for password validation, email uniqueness, bcrypt hashing
- Write integration test: registration → database insert → JWT issuance → response
- **Milestone:** Registration path working end-to-end

**Week 6 (Token Refresh & Profile):**
- Implement `TokenManager.refresh(refreshToken)`:
  - Validate refreshToken exists in Redis (not expired, not revoked)
  - Extract user_id from refreshToken key/metadata
  - Revoke old token from Redis
  - Issue new `AuthToken` pair (new accessToken, new refreshToken)
  - Return `AuthToken` object
- Implement `AuthService.getProfile(user_id)`:
  - Fetch `UserProfile` from `UserRepo`
  - Update `lastLoginAt` on first request after login
  - Return profile data
- Implement `POST /auth/refresh` endpoint (refreshToken in body, no Bearer auth required)
- Implement `GET /auth/me` endpoint (requires Bearer token; validates accessToken via `JwtService.verify()`)
- Write unit tests for token refresh, expiry validation, revocation logic
- Write integration test: refresh flow → Redis TTL update → new token issuance
- **Milestone:** Silent token refresh working; profile endpoint live

**Week 7 (Testing & Stabilization):**
- Achieve 80% unit test coverage across AuthService, PasswordHasher, TokenManager, JwtService
- Run integration test suite against testcontainers (PostgreSQL + Redis)
- Performance baseline: measure `AuthService.login()` latency (target < 200ms p95)
- Load test with k6: 100 concurrent logins → confirm response time target
- Security checklist: no password logging, no plaintext tokens in logs, no SQL injection vectors
- Bug fixes from testing; iterate until no critical issues
- **Milestone:** Ready for alpha deployment

**Frontend Development (1 engineer, 5 weeks, parallel)**

**Week 3-4 (LoginPage & AuthProvider):**
- Create `AuthProvider` context component:
  - State: `{ authToken, user, isLoading, error }`
  - Methods: `login(email, password)`, `register(email, password, displayName)`, `logout()`, `refreshToken()`
  - Token storage: accessToken in memory (XSS mitigation); refreshToken in HttpOnly cookie (if possible, else sessionStorage)
  - Auto-refresh logic: when accessToken nears expiry (< 2 min), call `refreshToken()` silently
  - Clear tokens on tab close
- Create `LoginPage` component:
  - Form fields: email, password
  - Client-side validation: email format, password non-empty
  - Error handling: display generic "Invalid email or password" (no user enumeration)
  - Success: call `AuthProvider.login()` → redirect to dashboard
  - Loading state: disable submit during API call
- Test: LoginPage → AuthProvider.login() → /auth/login API call → token reception
- **Milestone:** Users can log in via UI

**Week 5-6 (RegisterPage & ProtectedRoutes):**
- Create `RegisterPage` component:
  - Form fields: email, password, password confirmation, display name
  - GDPR consent checkbox (required)
  - Client-side validation: email format, password strength (>= 8, uppercase, number), matching passwords, display name 2-100 chars
  - Error handling: email uniqueness (backend), password policy (backend), form submission
  - Success: call `AuthProvider.register()` → auto-login → redirect to dashboard
- Create `ProtectedRoute` wrapper:
  - Check `AuthProvider.authToken` exists and is valid
  - If missing/expired and no refreshToken: redirect to LoginPage
  - If valid: render protected component
- Create `ProfilePage` component:
  - Fetch user data from `AuthProvider` or GET `/auth/me`
  - Display: email, displayName, account creation date
  - Add logout button (calls `AuthProvider.logout()` → DELETE refreshToken → clear state)
- Test: RegisterPage → AuthProvider.register() → /auth/register API call → auto-login → ProfilePage
- **Milestone:** Complete registration + login + logout user flow

**Week 7 (E2E Testing & UX Polish):**
- Write E2E test: user journey from landing → RegisterPage → login confirmation → dashboard
- Test token refresh: navigate between pages → confirm background refresh → no re-login
- Test error cases: invalid password, duplicate email, weak password, account lockout
- UX polish: loading spinners, error message clarity, form validation timing
- Accessibility: form labels, error announcements, keyboard navigation
- **Milestone:** Ready for alpha deployment

**QA & Testing (1 engineer, concurrent with dev)**

**Throughout Phase 1:**
- Unit test coverage tracking (target 80%): daily metrics in CI pipeline
- Integration test environment: testcontainers for PostgreSQL + Redis
- Manual regression testing: all FR-AUTH-001 through FR-AUTH-004 acceptance criteria
- Security checklist: no credentials in logs, no plaintext tokens, rate limiting active
- Performance baseline: APM instrumentation live; latency dashboard configured

**Phase 1 Deployment & Alpha Validation (Week 8)**

**Internal Alpha on Staging:**
- Feature flag `AUTH_NEW_LOGIN` = OFF (legacy auth remains default)
- Deploy AuthService, TokenManager, JwtService, LoginPage, RegisterPage to staging environment
- Enable `AUTH_NEW_LOGIN` flag for auth-team and QA only
- Smoke test: alpha users register and log in without issues
- Latency validation: p95 < 200ms confirmed via APM
- Load test: 500 concurrent requests → response time under 500ms
- Security review: penetration test of login/register endpoints
- Metrics: zero data loss, zero token validation failures, account lockout working as designed

**Phase 1 Success Criteria:**
- ✅ FR-AUTH-001 (login) passes acceptance criteria: valid/invalid credentials, account lockout
- ✅ FR-AUTH-002 (registration) passes acceptance criteria: uniqueness, password strength, UserProfile creation
- ✅ FR-AUTH-003 (token issuance & refresh) passes acceptance criteria: 15-min accessToken, 7-day refreshToken, refresh endpoint
- ✅ FR-AUTH-004 (profile retrieval) passes acceptance criteria: GET /auth/me returns full UserProfile
- ✅ Performance: p95 latency < 200ms for login, register, refresh, profile
- ✅ Test coverage: 80% unit, 15% integration across backend components
- ✅ Zero P0/P1 bugs blocking alpha
- ✅ Security review sign-off from security-engineer

---

### Phase 2: Profile, Password Reset & Audit Logging (Weeks 8-10, 3 weeks)

**Objective:** Deliver FR-AUTH-005 (password reset), enable audit logging for SOC2 compliance (NFR-COMP-001 through NFR-COMP-004), and launch beta (10% traffic).

**Requirement Focus:**
- **FR-AUTH-005:** Password reset via email — request sends link (1-hour TTL), confirmation updates password and revokes all sessions
- **NFR-COMP-001:** GDPR consent recorded at registration
- **NFR-COMP-002:** SOC2 audit logging (user ID, timestamp, IP, outcome; 12-month retention)
- **NFR-COMP-003:** NIST password hashing (bcrypt cost 12; passwords never logged)
- **NFR-COMP-004:** GDPR data minimization (only email, hash, displayName collected)

**Architecture: Component Wiring (Additions)**

| Named Artifact | Purpose | Wiring | Owning Phase | Consumers |
|---|---|---|---|---|
| **AuditLogger Service** | Structured auth event logging (SOC2 compliance) | Wires to PostgreSQL `auth_events` table with 12-month retention | Phase 2 | All AuthService methods |
| **EmailService Wrapper** | Async password reset email delivery via SendGrid | Wires to SendGrid API with delivery monitoring/alerts | Phase 2 | AuthService.resetPassword() |
| **PasswordResetTokenManager** | Manages reset tokens (opaque, 1-hour TTL, single-use) | Stores in PostgreSQL `password_reset_tokens` table with TTL | Phase 2 | AuthService password reset flow |
| **Feature Flag: AUTH_TOKEN_REFRESH** | Gates refresh token flow (enables silent refresh) | Default OFF during alpha; enabled in Phase 2 beta | Phase 2 | TokenManager.refresh(), AuthProvider |

**Backend Development (2 engineers, 3 weeks)**

**Week 8 (Password Reset Flow):**
- Implement `PasswordResetTokenManager`:
  - `generateResetToken(user_id)` → create opaque token, store in PostgreSQL `password_reset_tokens` table with 1-hour TTL + user_id + used=false
  - `validateResetToken(token)` → check exists, not expired, not used
  - `markTokenUsed(token)` → set used=true to prevent reuse
- Implement `AuthService.resetRequest(email)`:
  - Find user by email (if not found, still return success to prevent enumeration)
  - Generate reset token via `PasswordResetTokenManager`
  - Queue async email job: send reset link to user's email (SendGrid)
  - Log event: `AUTH_RESET_REQUESTED` with user_id, timestamp, IP
- Implement `AuthService.resetConfirm(token, newPassword)`:
  - Validate token via `PasswordResetTokenManager.validateResetToken()`
  - Extract user_id from token
  - Hash new password via `PasswordHasher.hash(newPassword, cost=12)`
  - Update user's `passwordHash` in database
  - Mark token as used
  - Revoke all refresh tokens for this user (clear from Redis)
  - Log event: `AUTH_PASSWORD_RESET` with user_id, timestamp, IP
  - Return success
- Implement `POST /auth/reset-request` endpoint (no auth required); rate limit 5 req/min per IP
- Implement `POST /auth/reset-confirm` endpoint (no auth required); validate token + new password
- Write unit tests for token generation, validation, expiry, reuse prevention
- Write integration test: reset request → email job queued → token stored → reset confirm → password updated → sessions revoked
- **Milestone:** Password reset flow working end-to-end

**Week 9 (Audit Logging & SOC2 Compliance):**
- Create `AuditLogger` service:
  - Method `log(event_type, user_id, ip_address, outcome, details)` → structured log to PostgreSQL
  - Log schema: `auth_events(id, timestamp, user_id, event_type, ip_address, outcome, details, created_at)`
  - Retention: 12-month policy enforced by job that deletes rows older than 12 months
  - Non-blocking: audit logging failures do not fail auth operations
- Integrate AuditLogger into all AuthService methods:
  - `login()`: log `AUTH_LOGIN_SUCCESS` or `AUTH_LOGIN_FAILURE` with failure reason (invalid creds, account locked)
  - `register()`: log `AUTH_REGISTRATION_SUCCESS`
  - `resetRequest()`: log `AUTH_RESET_REQUESTED`
  - `resetConfirm()`: log `AUTH_PASSWORD_RESET_SUCCESS` or failure
  - `getProfile()`: log `AUTH_PROFILE_RETRIEVED`
- Verify GDPR compliance:
  - Consent checkbox stored in `users.gdpr_consent_at` (timestamp of consent)
  - Data minimization: users table contains only (id, email, displayName, passwordHash, roles, createdAt, updatedAt, lastLoginAt, gdprConsentAt)
  - No additional PII collected
- Verify NIST compliance:
  - Passwords hashed with bcrypt cost 12 (one-way)
  - Raw passwords never logged (check all log statements)
  - Password fields never appear in API responses
- Create dashboard to query audit logs: filter by date range, user ID, event type (for Jordan admin persona)
- Write integration test: all auth events logged with correct fields and timestamps
- **Milestone:** Audit logging live; SOC2 controls in place

**Week 10 (Beta Deployment & E2E Testing):**
- Enable `AUTH_NEW_LOGIN` for internal auth-team + QA (Stage 1) → all test pass
- Deploy to production with `AUTH_NEW_LOGIN` = OFF, `AUTH_TOKEN_REFRESH` = OFF (legacy still default)
- Enable `AUTH_NEW_LOGIN` = ON for 10% of production traffic (beta users via feature flag or gradual rollout)
- Monitor Phase 1 success criteria + new Phase 2 metrics:
  - Password reset completion rate (target > 80%)
  - Email delivery success rate (target > 99.5%)
  - Audit log ingestion latency (target < 10ms p99)
  - Zero account lockout false positives
- Write E2E test: user journey with password reset (register → forgot password → reset link → new password → login with new password)
- Load test: 500 concurrent resets + refresh requests
- Security review: password reset token security, email link validation, session revocation
- **Milestone:** Beta live to 10% traffic

**Phase 2 Success Criteria:**
- ✅ FR-AUTH-005 (password reset) passes acceptance criteria: request sends email, confirm updates password, revokes sessions
- ✅ NFR-COMP-001 through NFR-COMP-004 (compliance) pass validation: consent recorded, audit logs complete, bcrypt cost 12, no extra PII
- ✅ Audit log query API available for Jordan (admin) persona
- ✅ Email delivery success > 99.5% over beta period
- ✅ Password reset completion rate > 80%
- ✅ Beta metrics: p95 latency < 200ms, error rate < 0.5%
- ✅ Security review sign-off for password reset + audit logging

---

### Phase 3: Production GA & Stabilization (Weeks 11-12, 2 weeks)

**Objective:** Monitor beta metrics, stabilize production, and launch full GA. Deprecate legacy auth. Achieve 99.9% uptime and < 0.1% error rate.

**Activities:**

**Week 11 (GA Preparation & Cutover):**
- Monitor beta (10%) metrics for 7 days:
  - p95 login latency: target < 200ms ✅
  - Error rate: target < 0.5% → accept if < 1%, rollback if > 2%
  - Email delivery: target > 99.5% ✅
  - Password reset completion: target > 80% ✅
  - Zero data loss or corruption incidents ✅
  - Audit log ingestion: zero failures ✅
- If all metrics green: enable `AUTH_NEW_LOGIN` = ON for remaining 90% of production traffic (gradual rollout or big bang)
- Parallel legacy auth operation: both pathways live; gradual user migration as existing sessions expire
- Enable `AUTH_TOKEN_REFRESH` = ON: activate silent token refresh in `AuthProvider`
- Verify rollback criteria are not triggered
- Test full failover: if `AuthService` pod crashes, verify fallback to legacy auth works
- Capacity planning: confirm HPA settings (3 replicas baseline → 10 at CPU > 70%)
- **Milestone:** GA live to 100% traffic

**Week 12 (Stabilization & Deprecation):**
- Monitor production metrics across all users (100%):
  - Uptime: target 99.9% (< 43 min downtime/month)
  - p95 latency: target < 200ms ✅
  - Error rate: target < 0.1% (vs. Phase 1-2 targets of 0.5-1%)
  - Authentication throughput: peak concurrent users stable
  - Cache hit rate (Redis): > 95% for refresh tokens
- Deprecate legacy auth:
  - Disable legacy login endpoint; users with legacy tokens forced to re-login via new AuthService
  - Purge legacy session data from old system
  - Update documentation + API references to point to new `/v1/auth/*` endpoints
- Remove feature flags:
  - Delete `AUTH_NEW_LOGIN` flag (new auth now default)
  - Keep `AUTH_TOKEN_REFRESH` for 2+ weeks post-GA (allow safe rollback if refresh logic bugs discovered)
  - Delete `AUTH_TOKEN_REFRESH` after stabilization period (week 14+)
- Operational readiness:
  - Run runbook drills (auth-team on-call): scenario 1 (AuthService down), scenario 2 (Redis failures), scenario 3 (token refresh loop)
  - Validate on-call rotation (24/7 coverage for first 2 weeks post-GA)
  - Confirm escalation paths: auth-team → test-lead → eng-manager → platform-team
- Post-launch analysis:
  - Calculate actual success metrics vs. targets (all 10 success criteria)
  - Measure business impact: registration conversion rate, DAU, average session duration, failed login rate
  - Document lessons learned (what went well, what surprised us, improvements for v1.1)
- **Milestone:** Production GA stabilized; legacy auth deprecated

**Phase 3 Success Criteria:**
- ✅ Uptime: 99.9% measured over rolling 30-day window
- ✅ p95 latency: < 200ms (all auth endpoints)
- ✅ Error rate: < 0.1%
- ✅ Zero data loss or corruption post-cutover
- ✅ All 10 success criteria met (from Success Criteria & Validation section below)
- ✅ Audit trail complete: all auth events logged per SOC2 requirements
- ✅ Legacy auth fully deprecated; new auth as single source of truth
- ✅ On-call team trained and ready for 24/7 support

---

## Risk Assessment & Mitigation Strategies

### Risk Inventory & Mitigations

| Risk ID | Title | Severity | Probability | Impact | Mitigation | Contingency | Owner | Monitoring |
|---------|-------|----------|-------------|--------|-----------|-------------|-------|------------|
| **R-001** | Token theft via XSS | HIGH | Medium | High | Store accessToken in memory only (not localStorage). HttpOnly cookie for refreshToken. 15-min expiry. `AuthProvider` clears tokens on tab close. Content Security Policy (CSP) headers. Input sanitization on all forms. | Immediate token revocation via `TokenManager`. Force password reset for affected accounts. Post-incident email notification. | security-engineer | APM traces for token-to-credential events; CSP violation logs |
| **R-002** | Brute-force attacks on login | HIGH | High | Medium | API Gateway rate limiting: 10 req/min per IP. Account lockout: 5 failed attempts within 15 min. bcrypt cost 12 (~250ms/hash). CAPTCHA on `LoginPage` after 3 failures. | IP blocking at WAF. Enable CAPTCHA for entire region if sustained attack. Enable advanced threat detection (API GW rules). | platform-team | Failed login counter; IP blocklist length; rate limit violations |
| **R-003** | Data loss during migration | HIGH | Low | High | Run `AuthService` in parallel with legacy during Phases 1-2. Idempotent upsert operations. Full database backup before each phase. Test restore procedure. Gradual rollout (Phase 2 beta 10%, Phase 3 GA). | Rollback to legacy auth via feature flag. Restore from pre-migration backup. Incident post-mortem. | backend-lead | Backup completion logs; restore test success; row count validation |
| **R-004** | Low registration adoption | HIGH | Medium | High | Usability testing before beta launch. Analyze funnel metrics: landing → register → email confirm → logged in. A/B test form simplification. Monitor conversion rate target (> 60%). | Iterate RegisterPage design based on funnel data. Reduce required fields (name optional in v1.1). Add password strength meter. | frontend-lead / product-manager | Funnel analytics; conversion rate dashboard |
| **R-005** | Security breach from implementation flaws | CRITICAL | Low | Critical | Dedicated security review before Phase 1 (threat model, code review). Penetration testing before GA (Week 10). Static analysis (SAST) in CI/CD. Dependency scanning for CVEs. | Immediate patch release. Security advisory notification. Affected user password reset. Incident response activation. | security-engineer | SAST scan results; pentest findings; CVE alerts |
| **R-006** | Compliance failure from incomplete audit logging | HIGH | Medium | High | Define audit log schema early (Phase 0). Validate against SOC2 controls in Phase 2 QA. Map all auth events to log entries. Confirm 12-month retention policy. | Backfill missing logs from backup (if possible). Document gaps in audit trail for compliance team. | compliance-officer | Log completeness check (Phase 2); retention policy enforcement; audit report |
| **R-007** | Email delivery failures | MEDIUM | Low | Medium | SendGrid delivery SLA: 99.9%; monitor bounce rates. Configure retry logic (3 attempts, exponential backoff). Fallback support channel for undelivered resets. Email delivery dashboard (SendGrid metrics). | Manual password reset by support team. In-app notification of delivery delay. | backend-lead | SendGrid bounce rate; reset email latency; support ticket volume |

---

## Resource Requirements & Dependencies

### Team Composition

| Role | Count | Weeks Allocated | Responsibility |
|------|-------|-----------------|-----------------|
| Backend Engineer (Auth) | 2 | 12 weeks | FR-AUTH-001/002 implementation, AuthService, PasswordHasher, TokenManager |
| Backend Engineer (Auth) | (continued) | 12 weeks | FR-AUTH-003/004/005 implementation, TokenManager, AuditLogger, password reset flow |
| Frontend Engineer | 1 | 12 weeks | LoginPage, RegisterPage, ProfilePage, AuthProvider, E2E tests |
| QA Engineer | 1 | 12 weeks | Unit/integration/E2E test strategy, regression testing, load testing, security checklist |
| Security Engineer (Review) | 1 | Phases 0, 1a, 2, 3 (4 weeks) | Threat model review, code review, penetration testing, SOC2 audit validation |
| Product Manager | 1 | Phases 0, 2, 3 (2 weeks) | Requirements clarification, success metrics tracking, stakeholder communication |
| Platform/DevOps Engineer | 1 | Phase 0, 3 (2 weeks) | Infrastructure provisioning, CI/CD setup, monitoring/alerting, on-call runbooks |

**Total Effort:** ~55 person-weeks (12 weeks × 4.5 FTE average)

### Infrastructure Dependencies

| Resource | Requirement | Current Status | Impact if Unavailable |
|----------|-------------|-----------------|----------------------|
| PostgreSQL | 15+ with connection pooling (100 conn min) | Needs provisioning | Cannot persist users; service non-functional |
| Redis | 7+ with 1+ GB RAM; 7-day TTL eviction | Needs provisioning | Token refresh unavailable; users must re-login |
| Node.js | 20 LTS runtime | Already available | Service cannot run |
| Kubernetes | 3+ node cluster for pod deployments | Assumed available | Cannot scale AuthService |
| SendGrid | Email API for password reset | Needs contract + testing | Password reset flow blocked |
| APM Tool | DataDog or Prometheus + Grafana | Needs setup | Cannot measure latency/errors; blind to performance |
| SAST Tool | rg or SonarQube for code analysis | Assumed available | Cannot detect injection vulnerabilities |

### External Dependencies

| Dependency | Type | Version | Purpose | Contingency |
|-----------|------|---------|---------|------------|
| bcryptjs | Library | ^2.4.3 | Password hashing | Fallback to Node.js native bcrypt module (different API) |
| jsonwebtoken | Library | ^9.x | JWT sign/verify | Fallback to jose library (compatible) |
| SendGrid | External Service | API | Password reset emails | Fallback to AWS SES (needs integration work) |
| PostgreSQL | Infrastructure | 15+ | User/audit log persistence | Failover to read replica or restore from backup |
| Redis | Infrastructure | 7+ | Refresh token storage | In-memory token store (non-persistent, loses tokens on restart) |

---

## Success Criteria & Validation Approach

### Success Metrics (10 Total)

| # | Metric | Source | Target | Phase Gate | Measurement Method | Owner |
|---|--------|--------|--------|-----------|-------------------|-------|
| 1 | Login response time (p95) | TDD/Extraction | < 200ms | Phase 1, Phase 3 | APM histogram on `AuthService.login()` endpoint | backend-lead |
| 2 | Registration success rate | TDD/Extraction | > 99% | Phase 1, Phase 3 | Ratio of successful registrations to attempts (tracking in logs) | backend-lead |
| 3 | Token refresh latency (p95) | TDD/Extraction | < 100ms | Phase 2, Phase 3 | APM histogram on `POST /auth/refresh` endpoint | backend-lead |
| 4 | Service availability | TDD/Extraction + NFR | 99.9% uptime | Phase 3 | Health check monitoring over rolling 30-day window | platform-engineer |
| 5 | Password hash time | TDD/Extraction | < 500ms (bcrypt cost 12) | Phase 1 (unit test) | Benchmark of `PasswordHasher.hash()` with bcrypt cost 12 | backend-lead |
| 6 | Registration conversion rate | PRD S19 | > 60% | Phase 2, Phase 3 | Funnel analytics: landing → register → email confirm → logged in | product-manager |
| 7 | Daily active authenticated users | PRD S19 | > 1000 within 30 days of GA | Phase 3 (post-launch) | Count of unique user IDs in `AuthToken` issuance events over 24hr window | product-manager |
| 8 | Average session duration | PRD S19 | > 30 minutes | Phase 3 (post-launch) | Time between login and logout/expiry; tracked via token refresh events | product-manager |
| 9 | Failed login rate | PRD S19 | < 5% of attempts | Phase 2, Phase 3 | Ratio of failed login attempts (invalid creds, locked account) to total attempts | backend-lead |
| 10 | Password reset completion | PRD S19 | > 80% | Phase 2, Phase 3 | Funnel: reset requested → email opened → reset confirm → success | product-manager |

### Validation Gates by Phase

**Phase 1 Gate (Week 7):**
- ✅ Metric 1 (login latency < 200ms) measured via APM; target achieved in load test
- ✅ Metric 2 (registration success > 99%) measured via test results (no failures in 100+ integration tests)
- ✅ Metric 5 (password hash time < 500ms) validated via bcrypt benchmark
- ✅ Metric 3 (refresh latency) measured but less critical at this phase
- ✅ Gate: all critical metrics pass OR documented with mitigation plan
- **Decision:** Proceed to Phase 2 alpha → beta, or rollback to design

**Phase 2 Gate (Week 10):**
- ✅ Metric 3 (refresh latency < 100ms) measured via APM during beta
- ✅ Metric 4 (availability 99.9%) approximated during beta (target rolling 30-day window)
- ✅ Metric 9 (failed login < 5%) measured via audit logs; monitor for lockout false positives
- ✅ Metric 10 (reset completion > 80%) measured via funnel analytics during beta
- ✅ Gate: beta error rate < 1%, no data loss, SOC2 audit controls validated
- **Decision:** Proceed to Phase 3 GA, or extend beta and iterate

**Phase 3 Gate (Week 12):**
- ✅ Metric 4 (uptime 99.9%) achieved over first 7 days of GA
- ✅ Metric 1 (login latency < 200ms) sustained under production load
- ✅ Metric 6 (registration conversion > 60%) confirmed via product analytics
- ✅ Metric 7 (DAU > 1000) tracked 30+ days post-launch
- ✅ Metric 8 (session duration > 30min) measured via token refresh patterns
- ✅ All 10 metrics published in post-launch report
- **Decision:** Declare GA successful, or enter stabilization period if metrics not met

---

## Timeline & Milestones

### Master Timeline

| Phase | Weeks | Start | End | Key Milestones | Gate Decision |
|-------|-------|-------|-----|----------------|---------------|
| **Phase 0: Design & Foundation** | 1-2 | Week 1 | Week 2 | ✅ Architecture signed off ✅ OQs resolved ✅ Infrastructure ready ✅ Team trained | Proceed to Phase 1 |
| **Phase 1: Core Auth & Registration** | 3-7 | Week 3 | Week 7 | ✅ FR-AUTH-001/002 implemented ✅ Login/register E2E working ✅ 80% test coverage ✅ Alpha on staging | Proceed to Phase 2 |
| **Phase 1 Alpha Validation** | 8 | Week 8 | Week 8 | ✅ Staging smoke tests pass ✅ Latency < 200ms ✅ Load test 500 concurrent ✅ Security review sign-off | Proceed to Phase 2 |
| **Phase 2: Profile, Reset & Audit** | 8-10 | Week 8 | Week 10 | ✅ FR-AUTH-005 implemented ✅ Audit logging live ✅ Beta 10% traffic ✅ Password reset > 80% completion | Proceed to Phase 3 |
| **Phase 3: GA & Stabilization** | 11-12 | Week 11 | Week 12 | ✅ GA 100% traffic ✅ 99.9% uptime achieved ✅ Legacy deprecated ✅ Post-launch metrics report | Go-live success |

### Weekly Cadence (by Phase)

**Phase 0 (Week 1-2):**
- **Mon (Day 1):** Architecture review kickoff; OQ triage begins
- **Wed:** Infrastructure provisioning started; team role assignments
- **Fri:** Design doc signed off; OQs resolved; Phase 1 kickoff prep

**Phase 1 (Week 3-7):**
- **Mon:** Weekly architecture sync (auth-team + security + platform)
- **Wed:** Integration test results reviewed; blockers escalated
- **Fri:** Build status check; Phase gate prep (Week 7 only)

**Phase 2 (Week 8-10):**
- **Mon:** Beta metrics review (Week 9-10)
- **Wed:** Audit logging validation; SOC2 control mapping
- **Fri:** Beta readiness check; Phase gate prep (Week 10 only)

**Phase 3 (Week 11-12):**
- **Daily (Mon-Fri):** Prod metrics monitoring; on-call handoff
- **Fri:** Weekly success metrics report; lessons learned doc

---

## Risk Mitigation Summary

### High-Risk Mitigation Efforts

**R-001 (Token theft via XSS):** Token security is CRITICAL. Architect emphasizes:
- In-memory accessToken (not localStorage, not sessionStorage) prevents XSS exfiltration
- HttpOnly + Secure + SameSite cookies for refreshToken (if possible) prevent JS access
- Content Security Policy (CSP) headers prevent inline script injection
- Short 15-min expiry limits damage window
- Clear tokens on tab close reduces session hijacking risk
**Contingency:** Revoke tokens in bulk if compromise detected

**R-002 (Brute-force attacks):** Defense-in-depth approach:
- API Gateway rate limiting (10 req/min per IP) stops volumetric attacks
- Account lockout (5 failures in 15 min) stops credential stuffing
- CAPTCHA on form (after 3 failures) adds friction
- bcrypt cost 12 (~250ms hash) slows offline dictionary attacks
- WAF IP blocking (platform team) scales response if attack persists
**Contingency:** Regional CAPTCHA enablement; advanced threat detection rules

**R-003 (Data loss during migration):** Architect recommends PARALLEL OPERATION:
- New `AuthService` and legacy auth run simultaneously Phases 1-2
- Users migrate naturally as refresh tokens expire (7-day window)
- No forced cutover = no single point of failure
- Full database backup before each phase
- Tested restore procedure (weekly drills)
**Contingency:** Rollback to legacy via feature flag in < 5 minutes

---

## Operational Readiness (Post-GA)

### On-Call & Escalation

**Coverage:** 24/7 rotation for first 2 weeks post-GA (auth-team)

**Runbook Scenarios:**
1. **AuthService down** → Check pod health → Restart pods → If PostgreSQL unreachable, failover to read replica → Notify platform-team
2. **Token refresh failures** → Check Redis connectivity → Verify JwtService key mounted → Restart TokenManager pods → Fallback to users re-login
3. **Email delivery failures** → Check SendGrid status → Verify queue depth → Manual reset email via support → Escalate to SendGrid support

**Escalation Path:** auth-team on-call (15 min SLA) → test-lead (30 min) → eng-manager (1 hr) → platform-team (critical infra issues)

### Monitoring & Alerting

**Prometheus Metrics (real-time):**
- `auth_login_total` (counter) — login attempts by outcome
- `auth_login_duration_seconds` (histogram) — p50/p95/p99 latencies
- `auth_token_refresh_total` (counter) — refresh operations by outcome
- `auth_registration_total` (counter) — registrations by status
- `redis_connection_errors_total` (counter) — Redis connectivity issues

**Alerts (triggered immediately):**
- Login failure rate > 20% over 5 min window
- p95 latency > 500ms
- Redis connection failures > 10 per minute
- Email delivery failures > 10% over 1 hour
- Uptime drop below 99.8% in rolling 24-hour window

**Dashboards:**
- **Latency dashboard:** p50/p95/p99 by endpoint (login, register, refresh, profile)
- **Error rate dashboard:** Failed logins, registrations, resets by error type
- **Capacity dashboard:** PostgreSQL conn pool utilization, Redis memory, CPU/memory by pod
- **Business metrics:** Registration conversion, DAU, session duration, password reset completion

---

## Conclusion & Architect's Recommendations

**Overall Assessment:** MEDIUM complexity (0.55) with well-understood architecture. The dual-token pattern, stateless JWT design, and facade-based orchestration are battle-tested. Primary risks are operational (data loss during migration, email delivery, brute-force attacks) rather than architectural.

**Key Recommendations:**

1. **Parallel Operation is Critical (R-003):** Never attempt a big-bang cutover from legacy to new auth. Phases 1-2 must run both systems in parallel. Feature flags enable gradual user migration. This single decision de-risks the entire roadmap.

2. **Security Review is Non-Negotiable:** Dedicate a security engineer to Phase 0 threat model, Phase 1 code review, and Phase 2 penetration testing. XSS and brute-force attacks are real risks; skip-it shortcuts lead to PR disasters.

3. **Audit Logging for Compliance:** Phase 2's audit logging (12-month retention, SOC2 controls) is a business blocker, not a nice-to-have. Validate schema early; don't discover audit log gaps in Q3 compliance review.

4. **Phased Rollout is Non-Negotiable:** Alpha (staging) → Beta (10% prod) → GA (100%). Each phase gates on latency, error rate, and business metrics. Rushing to GA skips learning and recovery opportunities.

5. **Load Testing Baseline:** Week 7 must confirm 500 concurrent login requests complete with p95 < 200ms. Week 10 must confirm 500 refresh requests do the same. These gates prevent Saturday 3am incidents.

6. **On-Call Readiness:** Runbook drills (Week 11-12) must cover pod failures, Redis outages, and email delivery issues. First 2 weeks post-GA will expose blindspots; prepare the team.

**Success Definition:** Ship all five functional requirements (FR-AUTH-001 through FR-AUTH-005) with < 200ms p95 latency, 99.9% uptime, zero data loss, and audit logging passing SOC2 validation by end of Phase 3 (12 weeks). Unblock the Q2-Q3 2026 personalization roadmap. Enable $2.4M in projected annual revenue.

**Timeline Confidence:** 90%+ confidence in 12-week delivery IF resource commitments hold and no critical unknowns emerge from Phase 0 design review. Risk is operational execution, not technical feasibility.
