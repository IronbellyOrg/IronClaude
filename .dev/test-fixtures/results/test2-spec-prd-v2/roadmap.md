---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
adversarial: true
base_variant: "Variant A (Opus Architect)"
variant_scores: "A:81 B:76"
convergence_score: 0.62
debate_rounds: 2
prd_source: "test-prd-user-auth.md"
---

# User Authentication Service — Final Merged Roadmap

## 1. Executive Summary

This roadmap defines a four-phase implementation plan for the User Authentication Service, delivering secure email/password authentication with JWT session management, self-service password reset, and compliance-grade audit logging. The service is a foundational dependency for the Q2–Q3 2026 personalization roadmap ($2.4M projected annual revenue impact) and the Q3 2026 SOC2 Type II audit deadline.

**Scope**: 5 functional requirements (FR-AUTH.1 through FR-AUTH.5), 6 non-functional requirements (NFR-AUTH.1 through NFR-AUTH.6), across 4 technical domains (backend, security, frontend, infrastructure). Includes one debate-resolved derived requirement (logout endpoint) not explicitly enumerated in the spec but validated as a session lifecycle necessity.

**Complexity**: MEDIUM (0.6) — driven by cryptographic token lifecycle (RS256 + refresh rotation with replay detection) and compliance requirements (GDPR, SOC2, NIST SP 800-63B), offset by modest architectural scope (2 core tables, 4 new files, 3 modified files).

**Architectural priorities** (synthesized from adversarial debate):
1. **Token lifecycle security** — RS256 signing, SHA-256 refresh token hashing (debate-resolved D3), single-use rotation with replay detection
2. **Audit logging as foundation** — SOC2 compliance built into Phase 1, not bolted on
3. **Requirement traceability** — every deliverable tagged to FR/NFR spec IDs with per-phase wiring tables
4. **Operational completeness** — logout endpoint, silent token refresh, email retry strategy, and post-launch monitoring thresholds incorporated from Variant B

**Critical path**: Infrastructure provisioning → PasswordHasher + JwtService → AuthService (login/registration) → TokenManager (refresh rotation) → Password reset with email integration → Compliance hardening.

**Key constraint**: v1.0 is email/password only. OAuth2/OIDC, MFA, RBAC, and social login are explicitly out of scope (PRD S12).

**Delivery timeline**: 7 sprints (~10 weeks) with a 1-day mid-project security checkpoint at the Phase 1/2 boundary (debate-resolved D7). Timeline is stakeholder-adjustable; see Section 6 for a compressed alternative.

---

## 2. Phased Implementation Plan

### Phase 1: Foundation and Infrastructure (Weeks 1–2)

**Objective**: Establish database schema, cryptographic primitives, audit logging infrastructure, and layered service skeleton. No user-facing endpoints yet.

**Epic alignment**: Pre-requisite for AUTH-E1, AUTH-E2, AUTH-E3.

#### 2.1 Deliverables

**1. PostgreSQL schema migration (003)**
- `users` table: `id`, `email` (unique index), `password_hash`, `display_name`, `created_at`, `consent_timestamp`, `locked_at`, `deleted_at`
- `refresh_tokens` table: `id`, `user_id` (FK → users.id, ON DELETE CASCADE), `token_hash`, `rotated_from_id` (self-referential FK for rotation chain auditing), `expires_at`, `revoked_at`, `created_at`
- Index: `refresh_tokens(user_id, revoked_at)` for replay detection queries
- Satisfies data model for all FR-AUTH.* requirements
- GDPR data minimization (NFR-AUTH.6): schema audit confirms only email, hashed password, display_name collected
- GDPR consent (NFR-AUTH.4): `consent_timestamp` column included at schema level
- `deleted_at` column supports future GDPR deletion (zero cost at schema level — debate convergence)
- `rotated_from_id` enables rotation chain auditing (incorporated from Variant B, debate D5)
- **Effort**: 3 days | **Owner**: Backend

**2. PasswordHasher module** (`password-hasher.ts`)
- bcrypt with cost factor 12 (NFR-AUTH.3, NIST SP 800-63B)
- Password policy validation: min 8 chars, uppercase, lowercase, digit (FR-AUTH.2c)
- Dependency: `bcrypt` NPM package (Dependency #2)
- Unit tests: hash roundtrip, cost factor verification, timing benchmark (~250ms)
- **Effort**: 2 days | **Owner**: Backend

**3. JwtService module** (`jwt-service.ts`)
- RS256 asymmetric signing with configurable key pair
- Access token generation (15min TTL) and verification
- Dependency: `jsonwebtoken` NPM package (Dependency #1)
- Dependency: RSA key pair provisioned in secrets manager (Dependency #5)
- Unit tests: sign/verify roundtrip, expired token rejection, invalid signature rejection
- **Effort**: 2 days | **Owner**: Backend

**4. Feature flag**: `AUTH_SERVICE_ENABLED` routing gate wired into request pipeline (Architectural Constraint #8)
- If disabled, returns 503 with rollback messaging
- **Effort**: 0.5 days | **Owner**: Backend/DevOps

**5. Audit logging infrastructure** (NFR-AUTH.5)
- Structured auth event logger: `user_id`, `event_type`, `timestamp`, `ip_address`, `user_agent`, `outcome`, `error_message`
- Event types: `LoginAttempt`, `RegistrationAttempt`, `TokenRefreshed`, `LogoutEvent`, `PasswordResetRequested`, `PasswordResetConfirmed`
- Async, non-blocking dispatch pattern
- 12-month log retention policy configured
- **Effort**: 3 days | **Owner**: Backend

**6. Project configuration**
- RSA key pair generation and secrets manager integration (90-day rotation policy documented)
- Environment configuration for token TTLs, bcrypt cost factor, rate limit thresholds
- **Effort**: 2 days | **Owner**: DevOps

#### 2.2 Integration Points — Wiring Mechanisms

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| `AUTH_SERVICE_ENABLED` feature flag | Routing gate | Auth route middleware | Phase 1 | Phases 2, 3, 4 (all auth endpoints) |
| Auth event logger | Logging middleware | Structured log emitter | Phase 1 | Phases 2, 3 (all auth operations must call logger) |
| DI container bindings | Dependency injection | PasswordHasher, JwtService registered as injectable singletons | Phase 1 | Phase 2 (AuthService, TokenManager receive injected instances) |

#### 2.3 Milestone: Foundation Ready

- [ ] Migration 003 applied to dev database with `rotated_from_id` and `deleted_at` columns
- [ ] PasswordHasher unit tests pass with bcrypt cost factor 12
- [ ] JwtService signs and verifies RS256 tokens
- [ ] Audit logger emits structured events to configured sink
- [ ] Feature flag toggles auth routes on/off

#### 2.4 Open Questions to Resolve Before Phase 2

- **OQ-2**: Maximum active refresh tokens per user — **Recommended: 5** (covers desktop, mobile, tablet + headroom; evict oldest on overflow)
- **OQ-3**: Account lockout policy after N failed attempts — **Recommended: progressive** (5 failures → 15min lock, 10 → 1hr, 20 → admin unlock)
- **OQ-6**: Exact SOC2 auth events to log — **Must resolve Sprint 1** (defines event_type enum)

---

### Phase 2: Core Authentication (Weeks 3–5)

**Objective**: Deliver login, registration, logout, token refresh, and silent token refresh — the complete session lifecycle. This phase addresses the highest-value user flows (Alex registration/login, Sam programmatic token refresh).

**Epic alignment**: AUTH-E1 (Login & Registration), AUTH-E2 (Token Management).

#### 2.5 Deliverables

**1. AuthService module** (`auth-service.ts`)
- Orchestrates PasswordHasher, TokenManager, User repository
- Layered architecture per Constraint #6: AuthService → TokenManager → JwtService
- **Effort**: 2 days | **Owner**: Backend

**2. FR-AUTH.1: User Login endpoint** (`POST /auth/login`)
- FR-AUTH.1a: Valid credentials → 200 with `access_token` (15min) + `refresh_token` (7d)
- FR-AUTH.1b: Invalid credentials → 401 with generic error (no email enumeration — Alex persona)
- FR-AUTH.1c: Locked account → 403
- FR-AUTH.1d: Rate limiting — 5 attempts per minute per IP
- Audit log: `LOGIN_SUCCESS`, `LOGIN_FAILURE`, `ACCOUNT_LOCKED` events
- **Effort**: 4 days | **Owner**: Backend

**3. FR-AUTH.2: User Registration endpoint** (`POST /auth/register`)
- FR-AUTH.2a: Valid data → 201 with user profile
- FR-AUTH.2b: Duplicate email → 409
- FR-AUTH.2c: Password policy enforcement (NIST SP 800-63B)
- FR-AUTH.2d: Email format validation
- NFR-AUTH.4: GDPR consent capture (`consent_timestamp` recorded)
- Audit log: `REGISTRATION_SUCCESS`, `REGISTRATION_FAILURE` events
- Alex persona: registration completes in under 60 seconds (PRD customer journey)
- PRD success target: > 60% registration conversion rate (S19)
- **Effort**: 4 days | **Owner**: Backend

**4. TokenManager module** (`token-manager.ts`)
- Issues access + refresh token pairs
- Refresh tokens hashed with **SHA-256** before storage (debate-resolved D3 — SHA-256 is appropriate for randomly-generated tokens; bcrypt's dictionary-attack resistance is irrelevant and its 250ms cost degrades hot-path performance)
- Coordinates with JwtService for signing
- **Effort**: 3 days | **Owner**: Backend

**5. FR-AUTH.3: Token Refresh endpoint** (`POST /auth/token/refresh`)
- FR-AUTH.3a: Valid refresh token → new `access_token` + rotated `refresh_token`
- FR-AUTH.3b: Expired refresh token → 401
- FR-AUTH.3c: **Replay detection** — reuse of revoked refresh token invalidates ALL user tokens; `rotated_from_id` chain traced for forensic analysis
- FR-AUTH.3d: Refresh token hashes stored for revocation
- Audit log: `TOKEN_REFRESH_SUCCESS`, `TOKEN_REPLAY_DETECTED` events
- Sam persona: programmatic refresh without user interaction (PRD JTBD #4)
- Alex persona: session persists across page refreshes for up to 7 days (PRD JTBD #2)
- **Effort**: 4 days | **Owner**: Backend

**6. Logout endpoint** (`POST /auth/logout`) — debate-resolved D2
- Revoke refresh token, clear httpOnly cookie, return 200
- Audit log: `LOGOUT` event
- Scope: single-session logout only; `LogoutAllDevices` deferred to v1.1
- Alex persona: "log out so that I can secure my session on a shared device" (PRD user story AUTH-E1)
- **Effort**: 1 day | **Owner**: Backend

**7. Silent token refresh** (frontend) — debate-resolved D8
- Client-side interceptor: detect 401 → queue pending requests → refresh token → replay queued requests
- No page redirect or re-login prompt unless refresh token also expired
- Explicit deliverable, not assumed — the debate confirmed this is non-trivial (request queuing, race conditions, error cascading)
- **Effort**: 3 days | **Owner**: Frontend

**8. Rate limiting middleware**
- Per-IP rate limiting for login endpoint (FR-AUTH.1d)
- Wired into request pipeline behind `AUTH_SERVICE_ENABLED` flag
- Dual-key (IP+email) approach documented as Phase 4 hardening item (debate-resolved D5)
- **Effort**: 2 days | **Owner**: Backend

**9. Token storage strategy** (frontend)
- Access token: in-memory only (Constraint #3)
- Refresh token: httpOnly, Secure, SameSite=Strict cookie (Constraint #3)
- No localStorage or sessionStorage
- **Effort**: included in silent token refresh deliverable

#### 2.6 Mid-Project Security Checkpoint — debate-resolved D7

**Duration**: 1 day, scheduled at Phase 1/2 boundary (after core token infrastructure, before password reset builds on top)

**Scope**:
- Review cryptographic primitives: bcrypt usage, SHA-256 refresh token hashing, RS256 signing
- Review token lifecycle: rotation logic, replay detection, revocation paths
- Static analysis (SAST) for hardcoded secrets, weak cryptography
- **Not** a full pentest — that remains in Phase 4

**Gate**: Findings must be resolved before Phase 3 begins. This catches foundational security flaws at 3 weeks invested, not 8.

#### 2.7 Integration Points — Wiring Mechanisms

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| AuthService DI registration | Dependency injection | AuthService depends on TokenManager, PasswordHasher, UserRepository, AuditLogger | Phase 2 | Phase 3 (password reset extends AuthService) |
| TokenManager DI registration | Dependency injection | TokenManager depends on JwtService, RefreshTokenRepository | Phase 2 | Phase 3 (password reset calls token revocation) |
| Rate limiter middleware | Middleware chain | Bound to `/auth/login` route | Phase 2 | Phase 4 (hardening may extend to dual-key) |
| Refresh token rotation strategy | Strategy pattern | Single-use rotation with replay detection; `rotated_from_id` chain | Phase 2 | Phase 3 (password reset bulk revocation) |
| Auth route registrations | Route registry | `/auth/login`, `/auth/register`, `/auth/token/refresh`, `/auth/logout` | Phase 2 | Guarded by `AUTH_SERVICE_ENABLED` from Phase 1 |

#### 2.8 Milestone: Core Auth Complete

- [ ] Login returns JWT pair for valid credentials, 401 for invalid, 403 for locked
- [ ] Registration creates user with hashed password and consent timestamp
- [ ] Token refresh rotates tokens; replay triggers full user token revocation via `rotated_from_id` chain
- [ ] Logout revokes refresh token and clears cookie
- [ ] Silent token refresh works end-to-end on frontend without page redirect
- [ ] Rate limiting blocks >5 login attempts/min/IP
- [ ] All auth events logged with user_id, timestamp, IP, outcome
- [ ] Mid-project security checkpoint passed with no critical findings
- [ ] Integration tests cover the full login → refresh → logout → re-login lifecycle

#### 2.9 Success Criteria Checkpoints

- Success Criterion #1: Login p95 < 200ms (initial benchmark with k6)
- Success Criterion #7: Login + refresh + logout E2E scenario returns expected status codes

---

### Phase 3: Profile and Password Reset (Weeks 5–7)

**Objective**: Complete the user self-service surface: profile retrieval and password reset. Integrates external email dependency with production-grade retry strategy.

**Epic alignment**: AUTH-E3 (Profile and Password Reset).

#### 2.10 Deliverables

**1. FR-AUTH.4: Profile Retrieval endpoint** (`GET /auth/profile`)
- FR-AUTH.4a: Valid Bearer token → user profile (`id`, `email`, `display_name`, `created_at`)
- FR-AUTH.4b: Expired/invalid token → 401
- FR-AUTH.4c: `password_hash` and `refresh_token_hash` NEVER included in response
- Alex persona: profile page renders current account details (PRD customer journey)
- **Effort**: 1 day | **Owner**: Backend

**2. FR-AUTH.5: Password Reset flow**
- FR-AUTH.5a: `POST /auth/password-reset/request` — generates reset token (1-hour TTL), dispatches email asynchronously
- FR-AUTH.5b: `POST /auth/password-reset/confirm` — validates token, sets new password, invalidates token
- FR-AUTH.5c: Expired/invalid reset token → 400
- FR-AUTH.5d: Successful reset invalidates ALL existing refresh tokens for the user
- Dependency: Email delivery service — SendGrid or equivalent (Dependency #3)
- Audit log: `PASSWORD_RESET_REQUESTED`, `PASSWORD_RESET_COMPLETED` events
- PRD customer journey: reset email delivered within 60 seconds, link has 1-hour TTL
- PRD success target: > 80% password reset completion rate (S19)
- **Effort**: 6 days | **Owner**: Backend

**3. Email service integration with retry strategy** — debate-resolved D13
- Async dispatch via message queue (recommended resolution for OQ-1 — async avoids blocking the reset endpoint on email service latency; improves p95 response time and resilience)
- Exponential backoff retry: max 5 attempts
- SendGrid delivery monitoring via event webhook; alert on > 10% failure rate
- Fallback support channel documented for manual account recovery
- **Effort**: 3 days | **Owner**: Backend + DevOps

**4. Password reset token cleanup job** — incorporated from Variant B
- Scheduled daily: delete expired `password_reset_tokens` where `expires_at < now()`
- Prevents database bloat
- **Effort**: 1 day | **Owner**: Backend/DevOps

**5. Frontend auth pages** (Dependency #6: frontend routing framework)
- Login page with generic error messaging
- Registration page with inline validation (password policy, email format)
- Password reset request and confirmation pages
- Profile page (authenticated)
- Token storage: access token in memory, refresh token in httpOnly cookie
- **Effort**: 5 days | **Owner**: Frontend

**6. Email enumeration prevention**
- Password reset request returns identical response for registered and unregistered emails
- Consistent with login error messaging (FR-AUTH.1b)

#### 2.11 Integration Points — Wiring Mechanisms

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| Password reset token store | Database table / TokenManager extension | Reset token hashes stored in `password_reset_tokens` table | Phase 3 | Phase 3 only |
| Email service integration | External service adapter + message queue | SendGrid client with async dispatch and retry | Phase 3 | Phase 3 (password reset dispatch) |
| Auth route registrations (extension) | Route registry | `/auth/profile`, `/auth/password-reset/request`, `/auth/password-reset/confirm` added | Phase 3 | Guarded by `AUTH_SERVICE_ENABLED` from Phase 1 |
| Bulk token revocation | TokenManager method | Called by password reset success handler; reuses replay-detection revocation from Phase 2 | Phase 2 (method), Phase 3 (caller) | Phase 3 |

#### 2.12 Milestone: Full Feature Complete

- [ ] Profile endpoint returns correct fields, excludes sensitive data
- [ ] Password reset email dispatched asynchronously within 60s of request
- [ ] Reset token expires after 1 hour; cleanup job removes expired tokens daily
- [ ] Successful reset invalidates all user sessions
- [ ] Frontend pages render with inline validation
- [ ] E2E: register → login → view profile → reset password → login with new password

#### 2.13 Open Question Resolutions

- **OQ-1 (Resolved)**: Async email dispatch via message queue — debate-resolved D13
- **OQ-7**: Headless/API-only auth flows — confirm FR-AUTH.3 is sufficient for Sam persona or if additional endpoints needed

---

### Phase 4: Hardening, Compliance, and Launch (Weeks 8–10)

**Objective**: Performance validation, security review, compliance certification, and production launch. No new features — exclusively hardening and verification.

#### 2.14 Deliverables

**1. Performance validation** (NFR-AUTH.1)
- k6 load tests: login, registration, token refresh, profile, password reset at 500 concurrent requests
- p95 response time < 200ms confirmed (PRD S19: login response time target)
- Benchmark bcrypt at cost factor 12 under load
- **Effort**: 3 days | **Owner**: QA + Backend

**2. Availability validation** (NFR-AUTH.2)
- Health check endpoint wired into monitoring
- PagerDuty alerting configured
- 99.9% uptime target baselined (PRD S19)
- **Effort**: 2 days | **Owner**: DevOps

**3. Security review and penetration testing** (Risk #5)
- Dedicated security review of all auth endpoints
- Penetration testing: credential stuffing, token replay, injection attacks
- JWT key rotation procedure validated (Risk #1: 90-day rotation)
- Refresh token replay detection verified under adversarial conditions (Risk #2)
- **Effort**: 5 days | **Owner**: Security

**4. Compliance validation**
- NFR-AUTH.4 (GDPR consent): verify `consent_timestamp` recorded for all registrations
- NFR-AUTH.5 (SOC2 audit logging): validate all auth events logged with required fields; verify 12-month retention; generate 100-event audit trail sample for external auditor
- NFR-AUTH.6 (GDPR data minimization): schema audit confirms no additional PII
- NFR-AUTH.3 (NIST): bcrypt cost factor 12 verified; no plaintext password storage or logging
- **Effort**: 2 days | **Owner**: Backend + Compliance

**5. Rate limiting hardening** — debate-resolved D5
- Evaluate and implement dual-key rate limiting (IP+email) as documented Phase 2 hardening item
- If implemented: mitigates distributed credential stuffing attacks
- If deferred: document risk acceptance with rationale
- **Effort**: 2 days | **Owner**: Backend

**6. Post-launch monitoring thresholds** — incorporated from Variant B
- p95 latency alert at 250ms (20% above target)
- Availability alert at 99.8% (rolling 30-day)
- Failed login rate alert at 10% (2× the 5% target)
- Registration conversion: weekly dashboard, monthly product review
- Email delivery rate alert at 95% (SendGrid event webhook)
- Audit log growth monitoring for anomalies (spike = potential attack)
- **Effort**: 2 days | **Owner**: DevOps

**7. Email delivery monitoring** (Risk #7)
- SendGrid delivery rate dashboard live
- Fallback support channel documented for account recovery
- **Effort**: 1 day | **Owner**: DevOps

**8. Registration UX validation** (Risk #4)
- Usability testing: registration completion under 60 seconds (PRD customer journey)
- Funnel analytics instrumented: landing → register → confirmed
- PRD success target: > 60% registration conversion rate (S19)
- **Effort**: 2 days | **Owner**: Product + QA

**9. E2E test suite** (Success Criterion #7)
- Full user lifecycle: register → login → refresh → profile → logout → reset → re-login
- Scenario coverage per PRD: Alex signup, Alex session persistence, Alex password reset, Sam token refresh, rate limiting, replay detection
- All steps return expected status codes per Spec Section 8.3
- **Effort**: 4 days | **Owner**: QA

**10. Feature flag rollout plan**
- Staged rollout via `AUTH_SERVICE_ENABLED`
- Rollback procedure documented and tested
- **Effort**: 1 day | **Owner**: DevOps

#### 2.15 Conditional Item: Admin Audit API — debate-resolved D6

**Status**: Conditional on compliance team input. If compliance confirms database-level access is insufficient for Q3 SOC2 audit:

- `AuditLogQueryHandler`: read-only paginated endpoint with date/user/event filters
- Authentication: internal network or basic auth (scoped to internal use)
- Serves Jordan persona (PRD S7): "view authentication event logs to investigate incidents and satisfy auditors"
- **Effort**: 2 days | **Owner**: Backend

If compliance approves database-level access, this is deferred to v1.1.

#### 2.16 Milestone: Production Launch

- [ ] k6 load test: p95 < 200ms at 500 concurrent (Success Criterion #1)
- [ ] Security review and pentest complete with no critical findings
- [ ] SOC2 audit log query returns complete auth event records (Success Criterion #6)
- [ ] GDPR consent and data minimization audits pass
- [ ] Registration conversion rate measurable, baseline established (Success Criterion #3, PRD > 60% target)
- [ ] Password reset completion rate measurable (PRD > 80% target)
- [ ] Post-launch monitoring alerts configured and tested
- [ ] Feature flag enabled in production; rollback tested

---

## 3. Risk Assessment and Mitigation Strategies

| # | Risk | Severity | Phase Addressed | Mitigation Strategy | Validation |
|---|------|----------|----------------|---------------------|------------|
| R1 | JWT private key compromise | **High** | Phase 1 (key provisioning), Phase 4 (rotation) | RS256 asymmetric keys in secrets manager; 90-day automated rotation; key never in code or logs; grep codebase for "PRIVATE KEY" patterns in CI | Phase 4: rotation procedure tested end-to-end |
| R2 | Refresh token replay attack | **High** | Phase 2 (implementation), Phase 4 (pentest) | Single-use rotation; `rotated_from_id` chain tracking; replay detection triggers full user token revocation (FR-AUTH.3c) | Phase 4: adversarial replay test in pentest |
| R3 | bcrypt cost factor insufficiency | **Medium** | Phase 1 (configurable), Phase 4 (benchmark) | Cost factor is configurable (env var); annual OWASP review; Argon2id migration path documented | Phase 4: benchmark under load confirms ~250ms |
| R4 | Low registration adoption | **High** | Phase 3 (UX), Phase 4 (testing) | Inline validation; registration < 60s; funnel analytics; A/B test form variants | Phase 4: usability test + baseline conversion rate (PRD > 60%) |
| R5 | Security breach from implementation flaws | **High** | Phase 2 (mid-project checkpoint), Phase 4 (pentest) | Mid-project security checkpoint at Phase 1/2 boundary catches foundational flaws early; comprehensive pentest before production | Phase 2: checkpoint report; Phase 4: pentest report with no critical findings |
| R6 | Incomplete SOC2 audit logging | **High** | Phase 1 (infrastructure), Phase 4 (validation) | Audit logger built in Phase 1; all auth operations log events from Phase 2 onward; 100-event sample for external auditor | Phase 4: SOC2 control validation query |
| R7 | Email delivery failures | **Medium** | Phase 3 (integration), Phase 4 (monitoring) | Async dispatch with exponential backoff (max 5 retries); SendGrid delivery monitoring + alerting at 95% threshold; fallback support channel | Phase 4: delivery rate dashboard live |
| R8 | Database connection exhaustion under load | **Medium** | Phase 2 (baseline), Phase 4 (validation) | Connection pooling configured (pgBouncer); max connections tuned based on bcrypt latency; load tested at 500 concurrent | Phase 4: k6 validates no connection exhaustion |
| R9 | Distributed rate-limit evasion | **Medium** | Phase 2 (IP-only), Phase 4 (hardening) | IP-only rate limiting in Phase 2; dual-key (IP+email) evaluated in Phase 4 hardening; X-Forwarded-For validated from trusted proxy only | Phase 4: documented risk acceptance or dual-key implementation |

**Risk sequencing rationale**: R1, R2, and R6 are addressed early (Phases 1–2) because they are structural — retrofitting security primitives and audit logging is far more expensive than building them in. R5 is mitigated both early (mid-project checkpoint) and late (comprehensive pentest), following the "shift left" principle validated in debate D7.

---

## 4. Resource Requirements and Dependencies

### Team and Effort Estimates

| Role | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Total |
|------|---------|---------|---------|---------|-------|
| **Backend Engineer (Lead)** | 2 weeks | 3 weeks | 2 weeks | 1 week | 8 weeks |
| **Backend Engineer (Secondary)** | — | 2 weeks | 2 weeks | 1 week | 5 weeks |
| **Frontend Engineer** | — | 1 week | 2 weeks | — | 3 weeks |
| **Security Engineer** | — | 1 day (checkpoint) | — | 5 days (review + pentest) | ~1.5 weeks |
| **QA Engineer** | — | 1 week | 1 week | 2 weeks | 4 weeks |
| **DevOps Engineer** | 1 week | — | 0.5 weeks | 1 week | 2.5 weeks |
| **Product Manager** | — | — | — | 0.5 weeks | 0.5 weeks |

**Total effort**: ~24–26 person-weeks (aligned with Variant B's estimate; applied to Variant A's phase structure)

### External Dependencies — Resolution Timeline

| # | Dependency | Required By | Resolution Deadline | Impact if Late |
|---|-----------|-------------|--------------------|----|
| 1 | `jsonwebtoken` NPM package | Phase 1 (JwtService) | Sprint 1 Day 1 | **Blocking**: no token signing |
| 2 | `bcrypt` NPM package | Phase 1 (PasswordHasher) | Sprint 1 Day 1 | **Blocking**: no password hashing |
| 3 | Email delivery service (SendGrid) | Phase 3 (FR-AUTH.5) | Sprint 4 start | **Blocking** for password reset; does not impact Phases 1–2 |
| 4 | PostgreSQL 15+ | Phase 1 (migration) | Sprint 1 Day 1 | **Blocking**: no persistent storage |
| 5 | RSA key pair + secrets manager | Phase 1 (JwtService) | Sprint 1 | **Blocking**: no token signing |
| 6 | Frontend routing framework | Phase 3 (auth pages) | Sprint 4 start | **Blocking** for UI; API endpoints functional without it |
| 7 | Security policy (SEC-POLICY-001) | Phase 1 (password policy) | Sprint 1 | **Risk**: policy undefined; using NIST SP 800-63B as interim standard |

---

## 5. Success Criteria and Validation Approach

### Quantitative Targets (PRD S19 — preserved without modification)

| # | Criterion | Target | Phase Validated | Method | Gate Type |
|---|-----------|--------|----------------|--------|-----------|
| S1 | Login p95 response time | < 200ms | Phase 2 (baseline), Phase 4 (under load) | k6 load test at 500 concurrent; production APM | **Launch blocker** |
| S2 | Service availability | 99.9% (rolling 30-day) | Phase 4 (monitoring), Post-launch | Health check endpoint + PagerDuty | Post-launch monitoring |
| S3 | Registration conversion rate | > 60% | Phase 4 (baseline) | Funnel analytics: landing → register → confirmed | **Launch baseline** |
| S4 | Average session duration | > 30 minutes | Post-launch | Token refresh event analytics | Post-launch tracking |
| S5 | Failed login rate | < 5% of attempts | Post-launch | Auth event log analysis | Post-launch tracking |
| S6 | Password reset completion | > 80% | Phase 4 (baseline) | Funnel: reset requested → new password set | **Launch baseline** |
| S7 | E2E lifecycle passes | All scenarios pass | Phase 4 | Automated E2E test suite (6 scenarios) | **Launch blocker** |

### Compliance Gates (PRD S17 — strongest variant gates preserved)

| Requirement | Standard | Validation | Phase | Gate |
|-------------|----------|-----------|-------|------|
| Consent at registration | GDPR (NFR-AUTH.4) | `consent_timestamp` recorded for all registrations; validated in E2E | Phase 2 | **Phase 2 exit** |
| Audit logging | SOC2 (NFR-AUTH.5) | All auth events logged; 12-month retention; 100-event sample for auditor | Phase 4 | **Launch blocker** |
| Password storage | NIST SP 800-63B (NFR-AUTH.3) | bcrypt cost factor 12; no plaintext in logs or storage | Phase 1 | **Phase 1 exit** |
| Data minimization | GDPR (NFR-AUTH.6) | Schema audit: only email, hashed password, display_name collected | Phase 1 | **Phase 1 exit** |

### Post-Launch Monitoring Thresholds (incorporated from Variant B)

| Metric | Alert Threshold | Rationale |
|--------|----------------|-----------|
| p95 latency | > 250ms | 20% above target — early warning before SLA breach |
| Availability | < 99.8% (30-day rolling) | Buffer below 99.9% target |
| Failed login rate | > 10% | 2× target — potential attack or UX regression |
| Email delivery rate | < 95% | SendGrid webhook monitoring |
| Audit log growth | Anomaly detection | Spike = potential credential stuffing or bot activity |

**Validation approach**: S1 and S7 are launch blockers — the service does not ship if they fail. S3 and S6 are baselined at launch and tracked post-launch with iteration targets. All PRD quantitative targets are preserved as-is, not averaged or weakened.

---

## 6. Timeline Estimates

### Primary Timeline (4 phases, ~10 weeks)

| Phase | Duration | Weeks | Key Dependencies |
|-------|----------|-------|-----------------|
| **Phase 1**: Foundation & Infrastructure | 2 weeks | Weeks 1–2 | PostgreSQL, NPM packages, RSA key pair |
| **Phase 2**: Core Authentication | 3 weeks | Weeks 3–5 | Phase 1 complete; OQ-2 and OQ-3 resolved; mid-project security checkpoint |
| **Phase 3**: Profile & Password Reset | 3 weeks | Weeks 5–7 | Phase 2 complete; email service provisioned; OQ-1 resolved (async) |
| **Phase 4**: Hardening & Launch | 2 weeks | Weeks 8–10 | Phase 3 complete; security review scheduled |

**Phase overlap**: Phases 2–3 overlap in Week 5 (token refresh stabilization concurrent with profile endpoint). Phases 3–4 overlap in Week 7 (password reset finalization concurrent with load test setup).

**Critical path**: PostgreSQL + key provisioning (Phase 1) → PasswordHasher + JwtService (Phase 1) → AuthService + login (Phase 2) → TokenManager + refresh rotation (Phase 2) → Security checkpoint → Password reset + email (Phase 3) → Security review + load test (Phase 4).

### Visual Timeline

```
Week  1    2    3    4    5    6    7    8    9    10
      |----|----|----|----|----|----|----|----|----|----|
P1    ████████████                                       Foundation
P2              ▐██████████████████                      Core Auth
      ·         ▐·                                       Security Checkpoint (1 day)
P3              ·         ▐██████████████████             Profile + Reset
P4              ·         ·         ▐██████████████████   Hardening + Launch
      ·         ·         ·         ·    ·    ▐          Launch Gate
```

### Compressed Alternative (for stakeholder discussion — debate D1)

If the Q3 SOC2 deadline requires faster delivery, the 4-phase plan can be compressed to ~8 weeks by:
1. Parallelizing Phase 1 and early Phase 2 work (backend + infra concurrent from Week 1)
2. Reducing Phase 4 to 1.5 weeks (pentest + load test overlap)
3. Adding a 1-week buffer (total: 8 weeks vs. Variant B's 6-week proposal)

This preserves the structural benefits (traceability, dedicated hardening phase, scope guardrails) while partially addressing the speed concern raised in the debate. The 6-week timeline from Variant B remains available as a maximum-compression option if stakeholders accept the zero-buffer risk.

---

## 7. Open Questions — Resolution Plan

| # | Question | Blocking Phase | Recommended Resolution | Owner |
|---|----------|---------------|----------------------|-------|
| OQ-1 | Sync vs. async password reset email | Phase 3 | **Resolved: Async** via message queue with exponential backoff (debate D13) | Engineering |
| OQ-2 | Max active refresh tokens per user | Phase 2 | **Recommend 5** — covers typical device count; evict oldest on overflow | Product |
| OQ-3 | Account lockout after N failures | Phase 2 | **Recommend progressive**: 5→15min, 10→1hr, 20→admin unlock | Security |
| OQ-4 | "Remember me" extending session | Post-v1.0 | **Defer** — 7-day refresh TTL provides good persistence | Product |
| OQ-5 | Token revocation on user deletion | Phase 2 | **Recommend immediate** — cascade delete + 15min access token natural expiry | Architecture |
| OQ-6 | SOC2 audit event scope | Phase 1 | **Must resolve Sprint 1** — defines event_type enum | Engineering + Compliance |
| OQ-7 | Headless/API-only auth completeness | Phase 2 | FR-AUTH.3 covers token refresh; service accounts deferred to v1.1 | Engineering |
| OQ-8 | Admin audit API scope (Jordan persona) | Pre-Phase 4 | **Conditional on compliance team input** (debate D6); 2-day effort if needed | Product + Compliance |

---

## 8. Scope Guardrails

Per PRD Scope Definition (S12) and Architectural Constraint #9, the following are **explicitly out of scope** for this roadmap:

| Capability | Rationale | Deferred To |
|------------|-----------|-------------|
| OAuth2/OIDC integration | Adds complexity without addressing v1.0 needs | v2.0 |
| Multi-factor authentication (MFA) | Requires SMS/TOTP infrastructure | v1.1 |
| Role-based access control (RBAC) | Authorization is a separate concern | Dedicated PRD |
| Social login (Google, GitHub) | Depends on OAuth/OIDC infrastructure | v2.0 |
| Admin UI for account management | Jordan persona partial coverage via logs/API | v1.1 |
| API keys / service account auth | Sam persona covered by token refresh only | v1.1 |
| `LogoutAllDevices` endpoint | Debate-resolved: deferred alongside account lockout | v1.1 |
| User-agent fingerprinting for rate limiting | Variant B R10 mitigation; premature for v1.0 | v1.1 |

Any request to add these capabilities should be routed to a v1.1+ planning cycle with its own PRD and roadmap.

---

## 9. Persona Coverage Matrix (PRD S7)

| Persona | Coverage in v1.0 | Gaps | Notes |
|---------|-------------------|------|-------|
| **Alex (End User)** | Full | None | Registration, login, logout, session persistence, profile, password reset all addressed |
| **Jordan (Admin)** | Partial | Admin UI deferred; audit API conditional | Audit logs are queryable via database; API endpoint conditional on compliance input (OQ-8) |
| **Sam (API Consumer)** | Partial | Service accounts deferred | Token refresh (FR-AUTH.3) enables programmatic session management; API keys deferred to v1.1 |
