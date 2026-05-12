---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
---

# User Authentication Service — Project Roadmap

## Executive Summary

The User Authentication Service is a medium-complexity (0.6/1.0), security-critical feature that enables user registration, login, session persistence, and self-service account recovery. This roadmap addresses the fundamental challenge: authentication is prerequisite infrastructure for the Q2–Q3 2026 personalization roadmap ($2.4M revenue impact) and SOC2 Type II compliance (Q3 deadline).

**Strategic drivers:**
- Unblocks personalized experiences (40% engagement lift)
- Enables SOC2 audit trail for compliance deadline
- Addresses 30% QoQ churn due to lack of user accounts

**Architectural priorities:**
1. **Token lifecycle security** — JWT rotation with stateless refresh, replay detection, and key rotation
2. **Audit logging as foundation** — SOC2 compliance built into Phase 1, not bolted on
3. **Integration point design** — Explicit dispatch tables, registries, and callback chains for testability and extensibility
4. **Dependency resilience** — Email service failures, secrets management, database availability all architected with fallback paths

**Delivery timeline:** 6 weeks (two 3-week phases) to production-ready state.

---

## Phased Implementation Plan

### Phase 1: Core Authentication and Token Management (Weeks 1–3)

**Objective:** Deliver user registration, login, logout, and stateless session persistence with full token lifecycle management and foundational audit logging.

**Outcomes:**
- Users can register with email/password and create authenticated sessions
- Sessions persist via JWT access tokens + refresh token rotation
- Auth event logging infrastructure ready for SOC2 validation
- Proof of concept for two-device session handling

**Deliverables:**

#### 1.1 Foundation: Architectural Wiring and Secrets Management

**Tasks:**

1. **Secrets Infrastructure Setup**
   - Provision RSA-2048 key pair for JWT RS256 signing
   - Store private key in secrets manager (HashiCorp Vault or AWS Secrets Manager)
   - Export public key for token validation across services
   - Document 90-day key rotation policy; schedule automation
   - **Owner:** DevOps/Platform | **Duration:** 2 days | **Blocker:** Must complete before token signing

2. **Database Schema: Users and RefreshTokens Tables**
   - Migration 003: `users` table (id, email, password_hash, display_name, consent_timestamp, created_at, updated_at, deleted_at)
   - Migration 003b: `refresh_tokens` table (id, user_id, token_hash, rotated_from_id [self-referential for rotation chain], is_revoked, expires_at, created_at)
   - Foreign key: `refresh_tokens.user_id` → `users.id` with ON DELETE CASCADE
   - Index: `refresh_tokens(user_id, is_revoked)` for replay detection queries
   - Index: `users(email)` for uniqueness checks
   - **Owner:** Backend | **Duration:** 3 days | **Depends on:** Secrets infrastructure

3. **Auth Service Dispatch Table**
   - Define route → handler mapping as a registry (not hardcoded routes)
   - Named artifact: `AuthServiceDispatchTable`
   - Wired endpoints:
     - `POST /auth/register` → `RegistrationHandler`
     - `POST /auth/login` → `LoginHandler`
     - `POST /auth/refresh` → `RefreshHandler`
     - `POST /auth/logout` → `LogoutHandler`
     - `GET /auth/profile` → `ProfileHandler`
   - **Owner:** Backend | **Duration:** 2 days | **Depends on:** Database schema

4. **Audit Logging Callback Chain**
   - Named artifact: `AuthEventLogger` (singleton with pluggable handlers)
   - Event types: `LoginAttempt`, `RegistrationAttempt`, `TokenRefreshed`, `LogoutEvent`, `PasswordResetRequested`, `PasswordResetConfirmed`
   - Each event triggers: Event → AuditService.log() → Database (async, non-blocking)
   - Log schema: `user_id`, `event_type`, `timestamp`, `ip_address`, `user_agent`, `outcome`, `error_message` (if failed)
   - **Owner:** Backend | **Duration:** 3 days | **Depends on:** Database schema | **Critical for:** SOC2 compliance (NFR-AUTH.5)

#### 1.2 User Registration (FR-AUTH.2)

**Tasks:**

1. **RegistrationHandler Implementation**
   - Accept: email, password, display_name
   - Validate: email format (RFC 5322), password policy (FR-AUTH.2c: ≥8 chars, 1 uppercase, 1 lowercase, 1 digit)
   - Check: email uniqueness against `users` table; return 409 Conflict if duplicate
   - Hash: password using bcrypt with cost factor 12 (NFR-AUTH.3)
   - Create: user record with email, password_hash, display_name, consent_timestamp = now()
   - Return: 201 Created with user profile (id, email, display_name, created_at)
   - Emit: RegistrationAttempt event to AuthEventLogger (success/failure)
   - **Owner:** Backend | **Duration:** 4 days | **Depends on:** Dispatch table, audit logger
   - **Test coverage:** Unit tests for email validation, password policy, uniqueness check, hash verification; integration test with real DB

2. **Password Policy Registry**
   - Named artifact: `PasswordPolicyValidator`
   - Registered policies:
     - `MinLength(8)`
     - `RequireUppercase(1)`
     - `RequireLowercase(1)`
     - `RequireDigit(1)`
   - Composable: `new PasswordValidator([MinLength(8), RequireUppercase(1), ...]).validate(password)`
   - **Owner:** Backend | **Duration:** 2 days | **Consumed by:** RegistrationHandler, PasswordResetHandler

3. **GDPR Consent Tracking**
   - At registration form submission, user must explicitly check "I consent to data collection."
   - On accept, record `consent_timestamp = now()` in `users` table
   - Audit log the consent decision (event: RegistrationAttempt with consent flag)
   - **Owner:** Frontend + Backend | **Duration:** 2 days | **Compliance:** NFR-AUTH.4

#### 1.3 User Login (FR-AUTH.1)

**Tasks:**

1. **LoginHandler Implementation**
   - Accept: email, password
   - Query: `users` table by email
   - If not found: return 401 "Invalid email or password" (no enumeration — FR-AUTH.1b)
   - Hash compare: bcrypt.compare(password, password_hash)
   - If mismatch: increment failed attempt counter (in-memory cache or DB); return 401 "Invalid email or password"
   - If match: emit LoginAttempt event (success), issue tokens, return 200 with tokens
   - **Owner:** Backend | **Duration:** 4 days | **Depends on:** Dispatch table, TokenManager (below)
   - **Test coverage:** Unit tests for credential verification, failed attempt tracking, token issuance; integration test with real DB and bcrypt timing

2. **Rate Limiter: 5 Failed Attempts per Minute per IP**
   - Middleware or handler-level check: `RedisKeyRateLimiter` with key = `login:failures:{ip}:{email}` (sliding window, 1-min expiry)
   - Threshold: 5 failed attempts within 60 seconds → return 429 Too Many Requests
   - On successful login: reset counter for that IP/email
   - On 10+ failures in 5 minutes: flag for manual review or temporary account lock (OI-3 — deferred to Phase 2)
   - **Owner:** Backend | **Duration:** 3 days | **Depends on:** LoginHandler | **Compliance:** FR-AUTH.1d
   - **Note:** Redis or in-memory cache required; architect decision on backend

3. **TokenManager: Access Token Issuance**
   - Named artifact: `AccessTokenManager`
   - Wired component: `JwtService` (RS256 RS256 signing with private key from secrets manager)
   - Token claims: `user_id`, `email`, `iat` (issued at), `exp` (expiry = now + 15 minutes)
   - Return format: Bearer token (JWT string, no server-side session)
   - Validation: JwtService.verify(token, publicKey) → decoded claims or error
   - Storage: Access token in memory (frontend in-memory variable or httpOnly cookie — architecture decision)
   - **Owner:** Backend | **Duration:** 3 days | **Depends on:** Secrets infrastructure, JwtService
   - **Compliance:** FR-AUTH.1a (15min TTL), NFR-AUTH.1 (latency < 200ms)

4. **TokenManager: Refresh Token Issuance and Rotation**
   - Named artifact: `RefreshTokenManager`
   - On login/registration success: issue new refresh token (random 32-byte string, hashed with bcrypt before storage)
   - Store: `refresh_tokens` table with (user_id, token_hash, rotated_from_id=null, is_revoked=false, expires_at=now+7d)
   - Return format: httpOnly, Secure, SameSite=Strict cookie with token value (NOT hashed)
   - Validation at refresh endpoint: hash incoming token, query DB for match, verify not revoked, verify not expired
   - **Owner:** Backend | **Duration:** 4 days | **Depends on:** Database schema, Secrets infrastructure | **Critical:** FR-AUTH.3a
   - **Compliance:** FR-AUTH.1a (7d TTL), NFR-AUTH.3 (no plain-text storage)

5. **Replay Detection: Refresh Token Rotation**
   - On every token refresh: check `rotated_from_id` chain — if same token is used twice, flag entire chain as compromised
   - Compromised detection: query `refresh_tokens` where `rotated_from_id` points to reused token
   - Action: set `is_revoked=true` for entire rotation chain for that user; emit SecurityAlertEvent; trigger account lock (v1.1 feature)
   - Design: `RefreshTokenValidator.detectReplay()` checks if incoming token_hash exists with `is_revoked=true` or is being replayed
   - **Owner:** Backend | **Duration:** 3 days | **Depends on:** RefreshTokenManager, Database | **Critical:** FR-AUTH.3c (replay detection)
   - **Note:** Requires architectural decision: alert user immediately or silently lock and notify support?

#### 1.4 Session Persistence and Logout (FR-AUTH.1 + Derived)

**Tasks:**

1. **TokenRefresh Endpoint** (FR-AUTH.3)
   - Handler: `RefreshHandler`
   - Input: refresh token (from httpOnly cookie)
   - Validation:
     - Hash incoming token
     - Query `refresh_tokens` table for token_hash match
     - Check `is_revoked=false` and `expires_at > now`
     - Check for replay attack (see above)
   - On success:
     - Mark old token as rotated: `refresh_tokens.id` from DB
     - Issue new access token (15min TTL)
     - Issue new refresh token (7d TTL) with `rotated_from_id` = old token's ID
     - Return new tokens; client updates in-memory token or cookie
   - Emit: TokenRefreshed event to AuthEventLogger
   - **Owner:** Backend | **Duration:** 4 days | **Depends on:** RefreshTokenManager, replay detection | **Compliance:** FR-AUTH.3a, FR-AUTH.3c
   - **Test coverage:** Rotation chain validation, replay detection, expiry checks, concurrent refresh handling

2. **Logout Handler** (Derived from FR-AUTH.1)
   - Handler: `LogoutHandler`
   - Input: refresh token (from httpOnly cookie)
   - Action: mark token as revoked in `refresh_tokens` table
   - Response: 200 OK; clear httpOnly cookie on client
   - Emit: LogoutEvent to AuthEventLogger
   - **Owner:** Backend | **Duration:** 1 day | **Depends on:** RefreshTokenManager
   - **Note:** Optional: include `LogoutAllDevices` endpoint that revokes all refresh tokens for a user (useful if password compromised)

3. **Silent Token Refresh on Frontend** (FR-AUTH.3d implied)
   - Implement client-side refresh logic: if access token expires and refresh token valid, silently refresh in background
   - No page redirect; no re-login prompt unless refresh token also expired
   - **Owner:** Frontend | **Duration:** 3 days | **Depends on:** RefreshHandler | **Compliance:** FR-AUTH.3a (session persistence)

#### 1.5 Compliance and Testing

**Tasks:**

1. **SOC2 Audit Logging Validation**
   - Integration test: verify all auth events logged with required fields (user_id, timestamp, IP, outcome)
   - Test scenarios: successful login, failed login, registration, token refresh, logout, password reset request (Phase 2)
   - Validate: logs queryable by date range and user ID (OI-6)
   - **Owner:** QA + Backend | **Duration:** 2 days | **Depends on:** AuthEventLogger
   - **Compliance:** NFR-AUTH.5 (SOC2 audit logging)

2. **Performance Baseline**
   - Load test: k6 script simulating 500 concurrent users registering, logging in, and refreshing tokens
   - Measure: login endpoint p95 latency (target < 200ms)
   - Measure: registration endpoint p95 latency (target < 200ms)
   - Identify bottlenecks: bcrypt hashing, DB queries, token signing
   - Tune: bcrypt cost factor (if needed), connection pooling, caching strategy
   - **Owner:** Backend + QA | **Duration:** 3 days | **Depends on:** All handlers | **Compliance:** NFR-AUTH.1

3. **Security Review Checkpoint**
   - Code review: token signing, bcrypt usage, SQL injection prevention, rate limiting logic
   - Static analysis: SAST tool (e.g., SonarQube) to detect hardcoded secrets, weak cryptography
   - Manual review: token claims design, replay detection logic, GDPR consent implementation
   - **Owner:** Security | **Duration:** 2 days | **Checkpoint:** Must pass before proceeding to Phase 2

**Phase 1 Duration:** 3 weeks | **Milestone:** Registration, login, logout, and token refresh functional; audit logging operational; SOC2 compliance readiness validated.

---

### Phase 2: Profile Retrieval, Password Reset, and Compliance Hardening (Weeks 4–6)

**Objective:** Deliver profile retrieval, self-service password reset with email integration, admin audit tools, and full SOC2 compliance validation.

**Outcomes:**
- Users can retrieve and view profile information
- Self-service password reset via email with 1-hour TTL reset tokens
- Admin-facing audit log query interface (Jordan persona support)
- SOC2 Type II audit trail complete and validated
- End-to-end user lifecycle testing demonstrates all scenarios

**Deliverables:**

#### 2.1 Profile Retrieval (FR-AUTH.4)

**Tasks:**

1. **ProfileHandler Implementation**
   - Handler: `ProfileHandler`
   - Input: Bearer access token (from Authorization header)
   - Validation: JwtService.verify(token) → extract user_id
   - Query: `users` table by user_id; return (id, email, display_name, created_at)
   - Exclude: password_hash, refresh_token_hash, consent_timestamp (sensitive fields — FR-AUTH.4c)
   - Response: 200 OK with profile JSON
   - Emit: ProfileRetrieved event to AuthEventLogger (optional, for analytics)
   - **Owner:** Backend | **Duration:** 1 day | **Depends on:** Dispatch table, TokenManager
   - **Compliance:** FR-AUTH.4a, FR-AUTH.4c
   - **Test coverage:** Unit test for field filtering, integration test with real DB, token expiry handling

#### 2.2 Password Reset Flow (FR-AUTH.5)

**Tasks:**

1. **Password Reset Request Handler** (FR-AUTH.5a)
   - Handler: `PasswordResetRequestHandler`
   - Input: email
   - Action (regardless of email registration status — prevents enumeration):
     - Query `users` table by email
     - If found: generate reset token (random 32-byte string), hash it, store in new `password_reset_tokens` table (id, user_id, token_hash, expires_at=now+1h, is_used=false)
     - Emit: PasswordResetRequested event to AuthEventLogger (with user_id if found; null if not)
     - Trigger: async email send to email address with reset link (OI-1: architecture decision on sync vs async)
     - Return: 200 OK "If email is registered, reset link sent" (no enumeration)
   - **Owner:** Backend | **Duration:** 3 days | **Depends on:** Database schema extension (password_reset_tokens table), Email service integration
   - **Compliance:** FR-AUTH.5a
   - **Note:** Async email send via message queue (e.g., Bull, Celery) preferred to avoid blocking

2. **Email Service Integration**
   - Named artifact: `EmailServiceDispatcher`
   - Wired components: SendGrid adapter or equivalent
   - Email templates:
     - `PasswordResetTemplate`: Subject "Reset Your Password", body with reset link (includes token in query param), 1-hour expiry warning
     - Test mode: in dev/staging, email may be printed to console or mocked
   - Delivery monitoring: track delivery status and failures; alert on > 10% failure rate
   - Resilience: if email service fails, queue job for retry (exponential backoff, max 5 attempts)
   - **Owner:** Backend + DevOps | **Duration:** 3 days | **Depends on:** SendGrid account provisioning | **Dependency:** Dep-3 (email service)

3. **Password Reset Confirmation Handler** (FR-AUTH.5b)
   - Handler: `PasswordResetConfirmHandler`
   - Input: reset_token (from email link), new_password
   - Validation:
     - Hash incoming reset_token
     - Query `password_reset_tokens` table for token_hash match
     - Check `is_used=false` and `expires_at > now` (FR-AUTH.5c)
     - Validate new_password against PasswordPolicyValidator
   - On success:
     - Hash new_password with bcrypt cost factor 12
     - Update `users` table with new password_hash
     - Mark reset token as used: `password_reset_tokens.is_used = true`
     - **Revoke all refresh tokens** for that user (FR-AUTH.5d): set `refresh_tokens.is_revoked=true` where user_id matches
     - Emit: PasswordResetConfirmed event to AuthEventLogger
     - Return: 200 OK "Password reset successful; please log in" (no auto-login — security best practice)
   - On expired/invalid token: return 400 "Invalid or expired reset link"
   - **Owner:** Backend | **Duration:** 3 days | **Depends on:** Database schema (password_reset_tokens), PasswordPolicyValidator, RefreshTokenManager
   - **Compliance:** FR-AUTH.5b, FR-AUTH.5c, FR-AUTH.5d
   - **Test coverage:** Unit test for token validation, policy validation, token revocation; integration test with email link simulation

4. **Password Reset Token Cleanup Job**
   - Scheduled job: delete expired password_reset_tokens (expires_at < now) daily at off-peak hours
   - Prevents database bloat; archives to audit log if required by compliance
   - **Owner:** Backend/DevOps | **Duration:** 1 day | **Recurring:** Daily

#### 2.3 Admin Audit Interface (Jordan Persona Support — OI-6 derived)

**Tasks:**

1. **Audit Log Query Handler**
   - Handler: `AuditLogQueryHandler` (requires admin authentication — separate from user auth, scoped to INTERNAL use or future admin panel)
   - Input: filters (date_from, date_to, user_id, event_type)
   - Query: `auth_events` table with WHERE conditions
   - Return: paginated JSON list of events (limit 1000 per page to prevent huge response)
   - Columns: user_id, event_type, timestamp, ip_address, user_agent, outcome, error_message
   - **Owner:** Backend | **Duration:** 2 days | **Depends on:** AuthEventLogger, Database
   - **Note:** Admin panel UI is out of scope for v1.0 (OI-8 scope question); API exists for future admin dashboard

2. **Audit Log Retention Policy**
   - Enforce: retain audit logs for 12 months minimum (NFR-AUTH.5, SOC2 requirement)
   - Archive: logs older than 12 months to cold storage (S3, GCS)
   - Job: monthly archival task run on first day of month
   - **Owner:** DevOps/Backend | **Duration:** 2 days | **Recurring:** Monthly

#### 2.4 Feature Flag and Rollback Strategy

**Tasks:**

1. **Feature Flag: AUTH_SERVICE_ENABLED**
   - Named artifact: `AuthServiceFeatureFlag`
   - Behavior: if flag disabled, route all auth requests to fallback handler (returns 503 "Service Unavailable — authentication temporarily offline")
   - Use case: quick rollback if critical security issue discovered post-deployment
   - Stored: environment variable or feature flag service (LaunchDarkly, Unleash)
   - **Owner:** DevOps/Backend | **Duration:** 1 day
   - **Compliance:** Architectural constraint (Constraint-8)

#### 2.5 End-to-End Testing and Compliance Validation

**Tasks:**

1. **End-to-End User Lifecycle Test Suite** (Success Criterion #7)
   - Test scenarios:
     - **Scenario 1 (Alex - Signup):** Register with email/password → receive confirmation → login → view profile → logout → attempt to use old session (fails)
     - **Scenario 2 (Alex - Session Persistence):** Login → refresh page → session persists across refresh → return after 7 days → session expired, prompted to login
     - **Scenario 3 (Alex - Password Reset):** Forget password → request reset → click email link → set new password → old sessions revoked → login with new password
     - **Scenario 4 (Sam - Token Refresh):** Login programmatically → use access token → get 401 when expired → refresh token programmatically → use new access token
     - **Scenario 5 (Rate Limiting):** Attempt login 6 times in 60 seconds → 5th fails with 401, 6th returns 429 Too Many Requests
     - **Scenario 6 (Replay Detection):** Steal refresh token → use it once (succeeds) → attacker replays old token (fails + triggers alert)
   - Tool: Playwright or similar E2E framework
   - Coverage: all happy paths + error paths
   - **Owner:** QA | **Duration:** 4 days | **Depends on:** All Phase 1 & 2 components
   - **Compliance:** Success Criteria #1, #2, #6, #7

2. **Performance Validation**
   - Run load test (k6) with Phase 2 additions: password reset request, password reset confirm, profile retrieval
   - Measure: all endpoints p95 latency < 200ms (NFR-AUTH.1)
   - Database performance: verify indexes on (users.email, refresh_tokens.user_id, password_reset_tokens.token_hash) are being used
   - **Owner:** QA + Backend | **Duration:** 2 days | **Depends on:** Phase 2 handlers

3. **Security Review: Phase 2**
   - Code review: password reset token generation, email link construction (CSRF protection?), token revocation logic
   - Threat model review: password reset email interception, token reuse, timing attacks on bcrypt verification
   - Penetration testing: attempt to bypass password policy, forge reset tokens, replay refresh tokens
   - **Owner:** Security | **Duration:** 3 days | **Checkpoint:** Must pass before production deploy

4. **SOC2 Audit Readiness**
   - Validate: all auth events logged with required fields (user_id, timestamp, IP, outcome)
   - Validate: logs retained for 12 months
   - Validate: no plain-text passwords logged or stored
   - Validate: bcrypt cost factor 12 in effect
   - Generate: audit trail sample (100 events across all auth scenarios) for external auditor review
   - **Owner:** Backend + Compliance | **Duration:** 2 days | **Checkpoint:** Audit trail certified before production deploy

**Phase 2 Duration:** 3 weeks | **Milestone:** Full user lifecycle operational; SOC2 audit trail validated; production-ready state achieved.

---

## Risk Assessment and Mitigation Strategies

### Critical Risks (Severity: High)

| # | Risk | Mitigation Strategy | Owner | Timeline |
|---|------|---------------------|-------|----------|
| **R1** | JWT private key compromise allows forged tokens | RS256 asymmetric signing; private key in secrets manager only; 90-day automated key rotation; revoke compromised key immediately and re-sign all existing tokens | DevOps/Security | During Phase 1 (Sec 1.1) |
| **R2** | Refresh token replay attack after theft | Refresh token rotation on every use; replay detection logic that revokes entire rotation chain; user notification on suspicious reuse; manual account recovery process | Backend | During Phase 1 (Sec 1.3) + Phase 2 (Sec 2.5) |
| **R3** | Security breach from implementation flaws (cryptography, SQL injection, timing attacks) | Dedicated security code review (Phase 1 + Phase 2 checkpoints); penetration testing pre-production; SAST tooling (SonarQube) in CI/CD; threat modeling session with security team | Security | Phase 1 checkpoint (day 19) + Phase 2 checkpoint (week 6) |
| **R4** | Low registration adoption due to poor UX (> 40% drop-off) | Usability testing with 5-10 representative users before launch; A/B test form variants (inline validation, field count, labels); funnel analytics tracking signup-to-login conversion; iterate based on data | Product/Design | Week 2 (Phase 1) for testing + week 6 for pre-launch |
| **R5** | Compliance failure from incomplete audit logging (SOC2 audit fails) | Audit logging built into Phase 1 (not bolted on); validation test suite (NFR-AUTH.5) in Phase 2; external auditor review of sample logs before launch; gap analysis against SOC2 control checklist | Compliance/Backend | Phase 1 (Sec 1.1) + Phase 2 checkpoint (week 6) |
| **R6** | JWT private key exposure in logs or error messages | Exclude key material from all error/debug output; sanitize logs before writing to disk; grep entire codebase for patterns like "PRIVATE KEY" and "-----BEGIN"; add linting rule to CI/CD | Security/Backend | During Phase 1 (Sec 1.1) |

### Medium Risks (Severity: Medium)

| # | Risk | Mitigation Strategy | Owner | Timeline |
|---|------|---------------------|-------|----------|
| **R7** | bcrypt cost factor becomes insufficient for future hardware | Configurable cost factor (environment variable); annual security review against OWASP recommendations; migration path documented (Argon2id to be evaluated in v1.1) | Backend/Security | Phase 1 (Sec 1.2) + annual review |
| **R8** | Email delivery failures blocking password reset (SLA < 99%) | Delivery monitoring and alerting (sendgrid events webhook); fallback support channel for account recovery documented; max 5 retry attempts with exponential backoff | Backend/DevOps | Phase 2 (Sec 2.2) |
| **R9** | Database connection exhaustion under peak load | Connection pooling configured (e.g., pgBouncer); max connection count tuned based on bcrypt hashing latency; load test to validate under 500 concurrent users | Backend/DevOps | Phase 1 (performance baseline) |
| **R10** | Rate limiter evasion via distributed IP spoofing | Rate limiting keyed on IP + email (not user_id, which requires auth); X-Forwarded-For header validated only if from trusted reverse proxy; implement user-agent fingerprinting as secondary signal (v1.1) | Backend | Phase 1 (Sec 1.3) |

---

## Resource Requirements and Dependencies

### Personnel

| Role | Phase 1 | Phase 2 | Notes |
|------|---------|---------|-------|
| **Backend Engineer (Lead)** | 3 weeks | 3 weeks | Token management, dispatch tables, database schema; owns architecture decisions |
| **Backend Engineer (Secondary)** | 2 weeks | 2 weeks | Handlers (login, register, profile, reset); testing support |
| **Frontend Engineer** | 1 week (late phase 1) | 2 weeks | UI (registration, login, logout, profile, reset forms); client-side token refresh |
| **QA Engineer** | 2 weeks (phase 1 late, phase 2 early) | 3 weeks | Load testing, E2E testing, security test scenarios, SOC2 validation |
| **Security Specialist** | 2 days (phase 1 checkpoint) | 3 days (phase 2 checkpoint) | Code review, threat modeling, penetration testing, key rotation strategy |
| **DevOps Engineer** | 1 week (phase 1 early) | 3 days (phase 2) | Secrets manager setup, RSA key provisioning, email service integration, feature flag setup |
| **Product Manager** | 2 days (phase 1) | 3 days (phase 2) | Scope decisions (OI-2, OI-4, OI-8), UX testing coordination, launch readiness |

**Total Effort:** ~24–26 person-weeks

### External Dependencies

| Dependency | Type | Required By | Mitigation | Status |
|-----------|------|-------------|-----------|--------|
| **SendGrid** (or equivalent email service) | External service | Phase 2 (Sec 2.2) | Fallback: SMTP backend for staging; documented account recovery process for email failures | Assume pre-provisioned |
| **PostgreSQL 15+** | Infrastructure | Phase 1 (Sec 1.1) | Database must be available before development begins; staging and production databases required | Assume pre-provisioned |
| **RSA Key Pair** | Configuration / Secrets | Phase 1 (Sec 1.1) | Generate during Phase 1 week 1; 90-day rotation automated | Owned by DevOps |
| **Frontend Routing Framework** | Internal | Phase 1 (late) + Phase 2 | Routing framework must support client-side token storage and refresh; compatibility review required | Assume available |
| **Secrets Manager** (HashiCorp Vault, AWS Secrets Manager, or equivalent) | Infrastructure | Phase 1 (Sec 1.1) | Must be operational before RSA keys provisioned; audit trail required for key access | Assume pre-provisioned |
| **Feature Flag Service** (LaunchDarkly, Unleash, or equivalent) | Infrastructure | Phase 1 (late) or Phase 2 (Sec 2.4) | Optional but recommended for rollback capability; can use environment variables as fallback | Recommend before launch |

### Technology Stack (Confirmed from Extraction + PRD)

- **Language:** TypeScript
- **Backend Framework:** (Inferred: Express, NestJS, or Fastify; not specified; architect should decide)
- **Cryptography:** `bcrypt` (bcrypt library, cost factor 12), `jsonwebtoken` (RS256)
- **Database:** PostgreSQL 15+
- **Email:** SendGrid API or SMTP
- **Rate Limiting:** Redis or in-memory cache
- **Audit Logging:** Application database (auth_events table)
- **Secrets Manager:** HashiCorp Vault or AWS Secrets Manager
- **Testing:** Jest (unit), Playwright (E2E), k6 (load)

---

## Success Criteria and Validation Approach

### Measurable Success Criteria

| # | Criterion | Target | Measurement Method | Validation Timeline | Pass/Fail Gate |
|---|-----------|--------|---------------------|----------------------|----|
| **S1** | Login endpoint response time (p95) | < 200ms | k6 load test (500 concurrent users, 10-min duration); APM dashboard (DataDog, New Relic) in production | Phase 2 week 3 | Fail: block production deployment |
| **S2** | Service availability | 99.9% uptime (rolling 30-day) | Health check endpoint (GET /health returns 200); PagerDuty uptime alert | Phase 2 week 3 (validate baseline); ongoing post-launch | Monitor post-launch; alert if < 99.8% |
| **S3** | Registration conversion rate | > 60% (funnel: landing → register → confirmed) | Analytics event: `signup_initiated`, `signup_completed` tracked; conversion = completed / initiated | Phase 2 week 3 (pre-launch) | Fail: conduct UX review, iterate |
| **S4** | Average session duration | > 30 minutes | Analytics: track `session_start` and `session_end` events; calculate mean duration | Phase 2 week 3 (pre-launch) | Monitor post-launch; < 20 min = UX issue |
| **S5** | Failed login rate | < 5% of attempts | Auth event logs: failed_login / (successful_login + failed_login) | Phase 2 week 3 (pre-launch) | > 5% = investigate credential quality or usability issue |
| **S6** | Password reset completion rate | > 80% (funnel: reset_requested → new_password_set) | Analytics: `password_reset_requested`, `password_reset_confirmed` events | Phase 2 week 3 (pre-launch) | < 80% = iterate on email delivery or UX |
| **S7** | E2E user lifecycle test suite | All scenarios pass (6 scenarios: signup, session persistence, password reset, programmatic auth, rate limiting, replay detection) | Automated test suite in CI/CD; must pass on every commit | Phase 2 week 3 (before merge to main) | Fail: blocker for merge |

### Compliance Validation (SOC2 & GDPR)

| Requirement | Validation Method | Owner | Timeline | Gate |
|-------------|-------------------|-------|----------|------|
| **SOC2: Audit Trail** (NFR-AUTH.5) | Audit event log contains user_id, timestamp, IP, outcome for all 6+ auth events | QA + Compliance | Phase 2 week 2 | Must pass before production |
| **SOC2: 12-Month Retention** | Database migration includes archival job; cold storage configured | DevOps | Phase 2 week 2 | Must be operational before launch |
| **GDPR: Consent at Registration** (NFR-AUTH.4) | Consent checkbox required; timestamp recorded in users.consent_timestamp | Frontend + Backend | Phase 1 week 2 | Must validate in E2E test (S7) |
| **GDPR: Data Minimization** (NFR-AUTH.6) | Schema audit: only email, password_hash, display_name, consent_timestamp in users table | Backend | Phase 1 week 1 | Blocker for Phase 1 completion |
| **NIST SP 800-63B: Password Hashing** (NFR-AUTH.3) | Unit test verifies bcrypt cost factor 12; benchmark test confirms ~250ms hash time | Backend | Phase 1 week 1 | Blocker for login handler implementation |

### Post-Launch Monitoring

- **P95 Latency:** Alert if > 250ms (20% above target)
- **Availability:** Alert if < 99.8% (rolling 30-day)
- **Failed Login Rate:** Alert if > 10% (2x target)
- **Registration Conversion:** Weekly dashboard; monthly review with product
- **Email Delivery Rate:** Alert if < 95% (SendGrid event webhook)
- **Audit Log Growth:** Monitor for anomalies (e.g., spike in failed logins = potential attack)

---

## Timeline and Phasing Summary

```
PHASE 1: Core Authentication (Weeks 1–3)
├─ Week 1
│  ├─ Sec 1.1: Secrets + Schema + Dispatch Table (Days 1–5) — BLOCKER for all handlers
│  └─ Sec 1.4: Audit Logger (Days 3–5) — BLOCKER for logging
├─ Week 2
│  ├─ Sec 1.2: Registration Handler (Days 6–9)
│  ├─ Sec 1.3: Login + TokenManager (Days 6–12) — CRITICAL PATH
│  └─ Sec 1.3: Rate Limiter (Days 9–11)
├─ Week 3
│  ├─ Sec 1.3: Refresh + Replay Detection (Days 13–16)
│  ├─ Sec 1.4: Logout + Silent Refresh (Days 14–17)
│  ├─ Sec 1.5: SOC2 Validation + Performance Baseline (Days 16–19)
│  └─ ⚠️ SECURITY CHECKPOINT (Day 19): Code review, SAST, threat model
│
PHASE 2: Profile + Password Reset + Compliance (Weeks 4–6)
├─ Week 4
│  ├─ Sec 2.1: Profile Handler (Days 20–21)
│  ├─ Sec 2.2: Password Reset Request + Email Integration (Days 20–23)
│  └─ Sec 2.2: Password Reset Confirm (Days 21–24)
├─ Week 5
│  ├─ Sec 2.3: Admin Audit Interface (Days 25–27)
│  ├─ Sec 2.4: Feature Flag + Rollback (Days 27–28)
│  └─ Sec 2.5: E2E Test Suite (Days 25–29)
├─ Week 6
│  ├─ Sec 2.5: Performance Validation (Days 30–31)
│  ├─ Sec 2.5: Security Review Phase 2 (Days 32–35) — BLOCKER for launch
│  ├─ Sec 2.5: SOC2 Audit Readiness (Days 35–36)
│  └─ ⚠️ LAUNCH GATE (Day 36): All success criteria (S1–S7) + compliance gates passed
│
PRODUCTION DEPLOYMENT: Week 7 (conditional on launch gate)
```

---

## Architectural Integration Points (Explicit Wiring)

### 1. Auth Service Dispatch Table
- **Named Artifact:** `AuthServiceDispatchTable`
- **Owning Phase:** Phase 1, Sec 1.2 (Day 5)
- **Wired Components:**
  - `POST /auth/register` → `RegistrationHandler`
  - `POST /auth/login` → `LoginHandler`
  - `POST /auth/refresh` → `RefreshHandler`
  - `POST /auth/logout` → `LogoutHandler`
  - `GET /auth/profile` → `ProfileHandler` (Phase 2)
  - `POST /auth/password-reset/request` → `PasswordResetRequestHandler` (Phase 2)
  - `POST /auth/password-reset/confirm` → `PasswordResetConfirmHandler` (Phase 2)
- **Cross-Reference:**
  - Phase 1: All token lifecycle flows depend on dispatch routing
  - Phase 2: Password reset flows added to table

### 2. Token Manager Registry
- **Named Artifact:** `TokenManager` (composite pattern)
  - `AccessTokenManager` (JWT RS256)
  - `RefreshTokenManager` (httpOnly cookie + DB storage)
  - `PasswordResetTokenManager` (Phase 2)
- **Owning Phase:** Phase 1, Sec 1.3 (Day 8)
- **Wired Components:**
  - `JwtService` (RS256 signing via private key from secrets manager)
  - `PasswordHasher` (bcrypt cost factor 12)
  - `RefreshTokenValidator` (with replay detection)
- **Cross-Reference:**
  - Phase 1: LoginHandler, RefreshHandler, LogoutHandler
  - Phase 2: PasswordResetConfirmHandler (token revocation)

### 3. Auth Event Logger (Callback Chain)
- **Named Artifact:** `AuthEventLogger` (event emitter pattern)
- **Owning Phase:** Phase 1, Sec 1.4 (Day 5)
- **Wired Components:**
  - Event types: `LoginAttempt`, `RegistrationAttempt`, `TokenRefreshed`, `LogoutEvent`, `PasswordResetRequested`, `PasswordResetConfirmed`
  - Each event → `AuditService.log()` → `auth_events` table (async, non-blocking)
- **Cross-Reference:**
  - Phase 1: LoginHandler, RegistrationHandler, RefreshHandler, LogoutHandler
  - Phase 2: PasswordResetRequestHandler, PasswordResetConfirmHandler, ProfileHandler

### 4. Password Policy Registry
- **Named Artifact:** `PasswordPolicyValidator`
- **Owning Phase:** Phase 1, Sec 1.2 (Day 3)
- **Wired Components:**
  - `MinLength(8)`
  - `RequireUppercase(1)`
  - `RequireLowercase(1)`
  - `RequireDigit(1)`
- **Cross-Reference:**
  - Phase 1: RegistrationHandler
  - Phase 2: PasswordResetConfirmHandler

### 5. Email Service Dispatcher
- **Named Artifact:** `EmailServiceDispatcher`
- **Owning Phase:** Phase 2, Sec 2.2 (Day 20)
- **Wired Components:**
  - SendGrid adapter (primary)
  - SMTP fallback (dev/staging)
- **Templates:**
  - `PasswordResetTemplate` (1-hour TTL)
  - `RegistrationConfirmationTemplate` (optional, Phase 2)
- **Cross-Reference:**
  - Phase 2: PasswordResetRequestHandler

### 6. Rate Limiter (Redis/In-Memory)
- **Named Artifact:** `RedisKeyRateLimiter` or `InMemoryRateLimiter`
- **Owning Phase:** Phase 1, Sec 1.3 (Day 9)
- **Configuration:**
  - Key: `login:failures:{ip}:{email}`
  - Threshold: 5 failed attempts per 60 seconds
  - Window: sliding 1-minute expiry
- **Cross-Reference:**
  - Phase 1: LoginHandler (FR-AUTH.1d)

---

## Key Decisions and Open Items Requiring Stakeholder Input

### Architectural Decisions (Architect's Recommendations)

1. **Sync vs. Async Email (OI-1)** — **ARCHITECT RECOMMENDATION: Async via message queue (Bull, Celery)**
   - Rationale: Prevents login/reset endpoint blocking on email service latency; improves p95 response time and resilience
   - Trade-off: User sees "check email" message before email is actually sent (eventual consistency); requires monitoring for delivery failures
   - Implementation: Phase 2, Sec 2.2

2. **Max Refresh Tokens per User (OI-2)** — **ARCHITECT RECOMMENDATION: No hard limit; recommend 10–50 tokens (one per device)**
   - Rationale: Supports multi-device usage without forcing logout on other devices
   - Storage: ~1KB per token in DB; negligible at scale
   - Monitoring: Alert if user has > 100 tokens (potential compromise)
   - Implementation: Phase 1 (no explicit limit in code); document in API

3. **Refresh Token Replay Detection (R2)** — **ARCHITECT DECISION: Rotation chain + full revocation**
   - When same token used twice: mark entire rotation chain as revoked, not just that token
   - Notify user immediately? Or silently lock and notify support? **ARCHITECT RECOMMENDATION: Silent lock + support notification**
   - Implementation: Phase 1, Sec 1.3

4. **Token Storage: Memory vs. Cookie (Constraint-3)** — **ARCHITECT DECISION: Access token in memory (variable or localStorage); refresh token in httpOnly cookie**
   - Access token: httpOnly cookie blocks JavaScript access (prevents XSS steal) but also prevents reading token value in console; memory allows dev tooling access for debugging
   - Refresh token: httpOnly cookie (cannot be accessed by JavaScript; CSRF protected with SameSite=Strict)
   - Hybrid approach: both tokens in httpOnly cookies for maximum security (accepted trade-off: no console access)
   - Implementation: Phase 1, Sec 1.3 (decision must be made before coding)

5. **Account Lockout After Failed Attempts (OI-3)** — **OUT OF SCOPE for v1.0; deferred to v1.1**
   - Current: Rate limiter blocks login after 5 failed attempts per minute per IP
   - v1.1: Progressive account lock (e.g., lock after 10 failed attempts per day; require support unlock or CAPTCHA + email verification)
   - Implementation placeholder: None in Phase 1/2; log high-failure patterns for manual review

6. **Key Rotation Automation (R1)** — **ARCHITECT RECOMMENDATION: Automated 90-day rotation with zero-downtime transition**
   - Process: Generate new key pair → upload to secrets manager → update application to accept both old and new keys (grace period) → stop accepting old key after 7 days
   - Testing: Rotation dry-run in staging; automated test for key rollover
   - Implementation: Phase 1, Sec 1.1 (post-launch automation)

---

## Handoff and Next Phases

### Phase 1 Deliverable
- **Working codebase:** All handlers (register, login, refresh, logout) passing E2E test suite
- **Infrastructure:** Database schema, secrets manager, feature flag service configured
- **Documentation:** API spec (OpenAPI/Swagger), architecture decision record, security review findings
- **Deployment:** Staging environment ready; feature flag disabled in production

### Phase 2 Deliverable
- **Working codebase:** Profile, password reset, admin audit interface operational
- **Compliance:** SOC2 audit trail certified; GDPR consent tracking validated
- **Deployment:** Production deployment approved; feature flag enabled in production

### Future Phases (Out of Scope for v1.0)

1. **v1.1 (Q3 2026):** Multi-factor authentication (TOTP/SMS), account lockout with progressive enforcement, admin dashboard UI
2. **v2.0 (Q4 2026):** OAuth2/OIDC, social login (Google, GitHub), service account API keys
3. **v2.1+:** Role-based access control (RBAC), attribute-based access control (ABAC), API rate limiting

---

## Approval and Sign-Off

This roadmap is ready for stakeholder review and approval. Key checkpoints:

- **Engineering Lead:** Confirm feasibility of 6-week timeline and resource allocation
- **Product Manager:** Validate phasing aligns with personalization roadmap dependencies
- **Security:** Approve threat model and risk mitigation strategy
- **Compliance:** Validate SOC2 and GDPR approach; confirm audit log requirements
- **Executive Sponsor:** Approve $2.4M value creation and Q3 compliance deadline alignment

**Recommended Next Step:** Schedule architecture design session (Day 1 of Phase 1) to finalize token storage strategy, email service choice, and secrets manager configuration before development begins.
