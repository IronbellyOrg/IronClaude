---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
generated: "2026-04-03"
generator: "architect-roadmap-agent"
phases: 4
total_requirements: 11
total_risks: 7
epics: ["AUTH-E1", "AUTH-E2", "AUTH-E3"]
---

# User Authentication Service — Project Roadmap

## 1. Executive Summary

This roadmap defines a four-phase implementation plan for the User Authentication Service, delivering secure email/password authentication with JWT session management, self-service password reset, and compliance-grade audit logging. The service is a foundational dependency for the Q2-Q3 2026 personalization roadmap and Q3 2026 SOC2 Type II audit.

**Scope**: 5 functional requirements (FR-AUTH.1 through FR-AUTH.5), 6 non-functional requirements (NFR-AUTH.1 through NFR-AUTH.6), across 4 technical domains (backend, security, frontend, infrastructure).

**Complexity**: MEDIUM (0.6) — driven by cryptographic token lifecycle (RS256 + refresh rotation with replay detection) and compliance requirements (GDPR, SOC2, NIST SP 800-63B), offset by modest architectural scope (2 tables, 4 new files, 3 modified files).

**Critical path**: Infrastructure provisioning → PasswordHasher + JwtService → AuthService (login/registration) → TokenManager (refresh rotation) → Password reset with email integration → Compliance hardening.

**Key constraint**: v1.0 is email/password only. OAuth2/OIDC, MFA, RBAC, and social login are explicitly out of scope.

---

## 2. Phased Implementation Plan

### Phase 1: Foundation & Infrastructure (Sprints 1–2)

**Objective**: Establish database schema, cryptographic primitives, and layered service skeleton. No user-facing endpoints yet.

**Epic alignment**: Pre-requisite for AUTH-E1, AUTH-E2, AUTH-E3.

#### Deliverables

1. **PostgreSQL schema migration (003)**
   - `users` table: id, email (unique), password_hash, display_name, created_at, consent_timestamp, locked_at
   - `refresh_tokens` table: id, user_id (FK), token_hash, expires_at, revoked_at, created_at
   - Satisfies data model for all FR-AUTH.* requirements
   - GDPR data minimization (NFR-AUTH.6): schema audit confirms only email, hashed password, display_name collected
   - GDPR consent (NFR-AUTH.4): consent_timestamp column included at schema level

2. **PasswordHasher module** (`password-hasher.ts`)
   - bcrypt with cost factor 12 (NFR-AUTH.3)
   - NIST SP 800-63B password policy validation (FR-AUTH.2c): min 8 chars, uppercase, lowercase, digit
   - Dependency: `bcrypt` NPM package (Dependency #2)
   - Unit tests: hash roundtrip, cost factor verification, timing benchmark (~250ms)

3. **JwtService module** (`jwt-service.ts`)
   - RS256 asymmetric signing with configurable key pair
   - Access token generation (15min TTL) and verification
   - Dependency: `jsonwebtoken` NPM package (Dependency #1)
   - Dependency: RSA key pair provisioned in secrets manager (Dependency #5)
   - Unit tests: sign/verify roundtrip, expired token rejection, invalid signature rejection

4. **Feature flag**: `AUTH_SERVICE_ENABLED` routing gate wired into request pipeline (Architectural Constraint #8)

5. **Audit logging infrastructure** (NFR-AUTH.5)
   - Structured auth event logger: user_id, timestamp, IP address, event_type, outcome
   - 12-month log retention policy configured
   - This is elevated to Phase 1 because the PRD makes SOC2 audit logging a hard compliance requirement, not deferrable to v1.1

6. **Project configuration**
   - RSA key pair generation and secrets manager integration
   - Environment configuration for token TTLs, bcrypt cost factor, rate limit thresholds

#### Integration Points — Wiring Mechanisms

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| `AUTH_SERVICE_ENABLED` feature flag | Routing gate | Auth route middleware | Phase 1 | Phases 2, 3, 4 (all auth endpoints) |
| Auth event logger | Logging middleware | Structured log emitter | Phase 1 | Phases 2, 3 (all auth operations must call logger) |
| DI container bindings | Dependency injection | PasswordHasher, JwtService registered as injectable singletons | Phase 1 | Phase 2 (AuthService, TokenManager receive injected instances) |

#### Milestone: Foundation Ready
- [ ] Migration 003 applied to dev database
- [ ] PasswordHasher unit tests pass with bcrypt cost factor 12
- [ ] JwtService signs and verifies RS256 tokens
- [ ] Audit logger emits structured events to configured sink
- [ ] Feature flag toggles auth routes on/off

#### Open Questions to Resolve Before Phase 2
- **OQ-2**: Maximum active refresh tokens per user (affects `refresh_tokens` table indexing strategy)
- **OQ-3**: Account lockout policy after N failed attempts (affects `users.locked_at` logic in Phase 2)
- **OQ-6**: Exact SOC2 auth events to log (affects logger event_type enum)

---

### Phase 2: Core Authentication (Sprints 2–4)

**Objective**: Deliver login, registration, and token refresh endpoints — the complete session lifecycle. This phase addresses the highest-value user flows (Alex registration/login, Sam programmatic token refresh).

**Epic alignment**: AUTH-E1 (Login & Registration), AUTH-E2 (Token Management).

#### Deliverables

1. **AuthService module** (`auth-service.ts`)
   - Orchestrates PasswordHasher, TokenManager, User repository
   - Layered architecture per Constraint #6: AuthService → TokenManager → JwtService

2. **FR-AUTH.1: User Login endpoint** (`POST /auth/login`)
   - FR-AUTH.1a: Valid credentials → 200 with access_token (15min) + refresh_token (7d)
   - FR-AUTH.1b: Invalid credentials → 401 with generic error (no email enumeration — Alex persona requirement)
   - FR-AUTH.1c: Locked account → 403
   - FR-AUTH.1d: Rate limiting — 5 attempts per minute per IP
   - Audit log: LOGIN_SUCCESS, LOGIN_FAILURE, ACCOUNT_LOCKED events

3. **FR-AUTH.2: User Registration endpoint** (`POST /auth/register`)
   - FR-AUTH.2a: Valid data → 201 with user profile
   - FR-AUTH.2b: Duplicate email → 409
   - FR-AUTH.2c: Password policy enforcement (NIST SP 800-63B)
   - FR-AUTH.2d: Email format validation
   - NFR-AUTH.4: GDPR consent capture (consent_timestamp recorded)
   - Audit log: REGISTRATION_SUCCESS, REGISTRATION_FAILURE events
   - Alex persona: registration completes in under 60 seconds

4. **TokenManager module** (`token-manager.ts`)
   - Issues access + refresh token pairs
   - Stores refresh token hashes in database (FR-AUTH.3d)
   - Coordinates with JwtService for signing

5. **FR-AUTH.3: Token Refresh endpoint** (`POST /auth/token/refresh`)
   - FR-AUTH.3a: Valid refresh token → new access_token + rotated refresh_token
   - FR-AUTH.3b: Expired refresh token → 401
   - FR-AUTH.3c: **Replay detection** — reuse of revoked refresh token invalidates ALL user tokens
   - FR-AUTH.3d: Refresh token hashes stored for revocation
   - Audit log: TOKEN_REFRESH_SUCCESS, TOKEN_REPLAY_DETECTED events
   - Sam persona: programmatic refresh without user interaction
   - Alex persona: session persists across page refreshes for up to 7 days

6. **Token storage strategy** (frontend)
   - Access token: in-memory only (Constraint #3)
   - Refresh token: httpOnly cookie (Constraint #3)
   - No localStorage or sessionStorage

7. **Rate limiting middleware**
   - Per-IP rate limiting for login endpoint (FR-AUTH.1d)
   - Wired into request pipeline behind `AUTH_SERVICE_ENABLED` flag

#### Integration Points — Wiring Mechanisms

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| AuthService DI registration | Dependency injection | AuthService depends on TokenManager, PasswordHasher, UserRepository, AuditLogger | Phase 2 | Phase 3 (password reset extends AuthService) |
| TokenManager DI registration | Dependency injection | TokenManager depends on JwtService, RefreshTokenRepository | Phase 2 | Phase 3 (password reset calls token revocation) |
| Rate limiter middleware | Middleware chain | Bound to `/auth/login` route | Phase 2 | Phase 2 only (may extend to other endpoints in future) |
| Refresh token rotation strategy | Strategy pattern | Single-use rotation with replay detection | Phase 2 | Phase 2 (token refresh endpoint), Phase 3 (password reset bulk revocation) |
| Auth route registrations | Route registry | `/auth/login`, `/auth/register`, `/auth/token/refresh` | Phase 2 | Guarded by `AUTH_SERVICE_ENABLED` from Phase 1 |

#### Milestone: Core Auth Complete
- [ ] Login returns JWT pair for valid credentials, 401 for invalid, 403 for locked
- [ ] Registration creates user with hashed password and consent timestamp
- [ ] Token refresh rotates tokens; replay triggers full user token revocation
- [ ] Rate limiting blocks >5 login attempts/min/IP
- [ ] All auth events logged with user_id, timestamp, IP, outcome
- [ ] Integration tests cover the full login→refresh→re-login lifecycle

#### Success Criteria Checkpoints
- Success Criterion #1: Login p95 < 200ms (initial benchmark with k6)
- Success Criterion #7: Login + refresh E2E scenario returns expected status codes

---

### Phase 3: Profile & Password Reset (Sprints 4–6)

**Objective**: Complete the user self-service surface: profile retrieval and password reset. Integrates external email dependency.

**Epic alignment**: AUTH-E3 (Profile and Password Reset).

#### Deliverables

1. **FR-AUTH.4: Profile Retrieval endpoint** (`GET /auth/profile`)
   - FR-AUTH.4a: Valid Bearer token → user profile (id, email, display_name, created_at)
   - FR-AUTH.4b: Expired/invalid token → 401
   - FR-AUTH.4c: password_hash and refresh_token_hash NEVER included in response
   - Alex persona: profile page renders current account details

2. **FR-AUTH.5: Password Reset flow**
   - FR-AUTH.5a: `POST /auth/password-reset/request` — generates reset token (1-hour TTL), dispatches email
   - FR-AUTH.5b: `POST /auth/password-reset/confirm` — validates token, sets new password, invalidates token
   - FR-AUTH.5c: Expired/invalid reset token → 400
   - FR-AUTH.5d: Successful reset invalidates ALL existing refresh tokens for the user
   - Dependency: Email delivery service — SendGrid or equivalent (Dependency #3)
   - Audit log: PASSWORD_RESET_REQUESTED, PASSWORD_RESET_COMPLETED events
   - PRD customer journey: reset email delivered within 60 seconds, link has 1-hour TTL

3. **Frontend auth pages** (Dependency #6: frontend routing framework)
   - Login page with generic error messaging
   - Registration page with inline validation (password policy, email format)
   - Password reset request and confirmation pages
   - Profile page (authenticated)
   - Token storage: access token in memory, refresh token in httpOnly cookie

4. **Email enumeration prevention**
   - Password reset request returns identical response for registered and unregistered emails
   - Consistent with login error messaging (FR-AUTH.1b)

#### Integration Points — Wiring Mechanisms

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| Password reset token store | Database table / TokenManager extension | Reset token hashes stored alongside or parallel to refresh tokens | Phase 3 | Phase 3 only |
| Email service integration | External service adapter | SendGrid client wired into password reset handler | Phase 3 | Phase 3 (password reset dispatch) |
| Auth route registrations (extension) | Route registry | `/auth/profile`, `/auth/password-reset/request`, `/auth/password-reset/confirm` added | Phase 3 | Guarded by `AUTH_SERVICE_ENABLED` from Phase 1 |
| Bulk token revocation | TokenManager method | Called by password reset success handler; reuses replay-detection revocation from Phase 2 | Phase 2 (method), Phase 3 (caller) | Phase 3 |

#### Milestone: Full Feature Complete
- [ ] Profile endpoint returns correct fields, excludes sensitive data
- [ ] Password reset email dispatched within 60s of request
- [ ] Reset token expires after 1 hour
- [ ] Successful reset invalidates all user sessions
- [ ] Frontend pages render with inline validation
- [ ] E2E: register → login → view profile → reset password → login with new password

#### Open Question Resolution Required
- **OQ-1**: Synchronous vs. async email dispatch — must be decided before implementing FR-AUTH.5a
- **OQ-7**: Headless/API-only auth flows — confirm FR-AUTH.3 is sufficient for Sam persona or if additional endpoints needed

---

### Phase 4: Hardening, Compliance & Launch (Sprints 6–7)

**Objective**: Performance validation, security review, compliance certification, and production launch. No new features — exclusively hardening and verification.

#### Deliverables

1. **Performance validation** (NFR-AUTH.1)
   - k6 load tests: login, registration, token refresh at 500 concurrent requests
   - p95 response time < 200ms confirmed
   - Benchmark bcrypt at cost factor 12 under load

2. **Availability validation** (NFR-AUTH.2)
   - Health check endpoint wired into monitoring
   - PagerDuty alerting configured
   - 99.9% uptime target baselined

3. **Security review and penetration testing** (Risk #5)
   - Dedicated security review of all auth endpoints
   - Penetration testing: credential stuffing, token replay, injection attacks
   - JWT key rotation procedure validated (Risk #1: 90-day rotation)
   - Refresh token replay detection verified under adversarial conditions (Risk #2)

4. **Compliance validation**
   - NFR-AUTH.4 (GDPR consent): verify consent_timestamp recorded for all registrations
   - NFR-AUTH.5 (SOC2 audit logging): validate all auth events logged with required fields; verify 12-month retention
   - NFR-AUTH.6 (GDPR data minimization): schema audit confirms no additional PII
   - NFR-AUTH.3 (NIST): bcrypt cost factor 12 verified; no plaintext password storage or logging

5. **Email delivery monitoring** (Risk #7)
   - SendGrid delivery rate monitoring and alerting
   - Fallback support channel documented for account recovery

6. **Registration UX validation** (Risk #4)
   - Usability testing: registration completion under 60 seconds
   - Funnel analytics instrumented: landing → register → confirmed

7. **E2E test suite** (Success Criterion #7)
   - Full user lifecycle: register → login → refresh → profile → reset → re-login
   - All steps return expected status codes per Spec Section 8.3

8. **Feature flag rollout plan**
   - Staged rollout via `AUTH_SERVICE_ENABLED`
   - Rollback procedure documented and tested

#### Milestone: Production Launch
- [ ] k6 load test: p95 < 200ms at 500 concurrent (Success Criterion #1)
- [ ] Security review and pentest complete with no critical findings
- [ ] SOC2 audit log query returns complete auth event records (Success Criterion #6 proxy)
- [ ] GDPR consent and data minimization audits pass
- [ ] Registration conversion rate measurable (Success Criterion #3 — baseline established)
- [ ] Feature flag enabled in production; rollback tested

---

## 3. Risk Assessment and Mitigation Strategies

| # | Risk | Severity | Phase Addressed | Mitigation Strategy | Validation |
|---|------|----------|----------------|---------------------|------------|
| 1 | JWT private key compromise | **High** | Phase 1 (key provisioning), Phase 4 (rotation) | RS256 asymmetric keys in secrets manager; 90-day automated rotation; key never in code or logs | Phase 4: rotation procedure tested end-to-end |
| 2 | Refresh token replay attack | **High** | Phase 2 (implementation), Phase 4 (pentest) | Single-use rotation; replay detection triggers full user token revocation (FR-AUTH.3c) | Phase 4: adversarial replay test in pentest |
| 3 | bcrypt cost factor insufficiency | **Medium** | Phase 1 (configurable), Phase 4 (benchmark) | Cost factor is configurable; annual OWASP review; Argon2id migration path documented | Phase 4: benchmark under load confirms ~250ms |
| 4 | Low registration adoption | **High** | Phase 3 (UX), Phase 4 (testing) | Inline validation; registration < 60s; funnel analytics | Phase 4: usability test + baseline conversion rate |
| 5 | Security breach from implementation flaws | **High** | Phase 4 | Dedicated security review + penetration testing before production | Phase 4: pentest report with no critical findings |
| 6 | Incomplete SOC2 audit logging | **High** | Phase 1 (infrastructure), Phase 4 (validation) | Audit logger built in Phase 1; all auth operations log events from Phase 2 onward | Phase 4: SOC2 control validation query |
| 7 | Email delivery failures | **Medium** | Phase 3 (integration), Phase 4 (monitoring) | SendGrid delivery monitoring + alerting; fallback support channel | Phase 4: delivery rate dashboard live |

**Architect's note on risk sequencing**: Risks 1, 2, and 6 are addressed early (Phases 1–2) because they are structural — retrofitting security primitives and audit logging is far more expensive than building them in. Risk 5 (pentest) is Phase 4 by necessity but the architecture enables it: clean layering means each component can be tested in isolation.

---

## 4. Resource Requirements and Dependencies

### External Dependencies — Resolution Timeline

| # | Dependency | Required By | Resolution Deadline | Risk if Late |
|---|-----------|-------------|--------------------|----|
| 1 | `jsonwebtoken` NPM package | Phase 1 (JwtService) | Sprint 1 Day 1 | **Blocking**: no token signing |
| 2 | `bcrypt` NPM package | Phase 1 (PasswordHasher) | Sprint 1 Day 1 | **Blocking**: no password hashing |
| 3 | Email delivery service (SendGrid) | Phase 3 (FR-AUTH.5) | Sprint 4 start | **Blocking**: password reset disabled; can defer to Phase 3 without impacting Phases 1–2 |
| 4 | PostgreSQL 15+ | Phase 1 (migration) | Sprint 1 Day 1 | **Blocking**: no persistent storage |
| 5 | RSA key pair + secrets manager | Phase 1 (JwtService) | Sprint 1 | **Blocking**: no token signing |
| 6 | Frontend routing framework | Phase 3 (auth pages) | Sprint 4 start | **Blocking** for UI; API endpoints functional without it |
| 7 | Security policy (SEC-POLICY-001) | Phase 1 (password policy) | Sprint 1 | **Risk**: policy requirements undefined; using NIST SP 800-63B as interim standard |

### Team Skills Required

- **Backend TypeScript engineer** (Phases 1–3): Auth service, token management, API endpoints
- **Security engineer** (Phase 1 review, Phase 4 pentest): Crypto review, penetration testing
- **Frontend engineer** (Phase 3): Auth pages, token storage, inline validation
- **DevOps/Infrastructure** (Phase 1 setup, Phase 4 monitoring): PostgreSQL, secrets manager, monitoring, alerting
- **QA engineer** (Phases 2–4): Integration tests, E2E tests, load tests

---

## 5. Success Criteria and Validation Approach

| # | Criterion | Target | Phase Validated | Method |
|---|-----------|--------|----------------|--------|
| 1 | Login p95 response time | < 200ms | Phase 2 (baseline), Phase 4 (under load) | k6 load test at 500 concurrent; production APM |
| 2 | Service availability | 99.9% (rolling 30-day) | Phase 4 (monitoring), Post-launch | Health check endpoint + PagerDuty |
| 3 | Registration conversion rate | > 60% | Phase 4 (baseline) | Funnel analytics: landing → register → confirmed |
| 4 | Average session duration | > 30 minutes | Post-launch | Token refresh event analytics |
| 5 | Failed login rate | < 5% | Post-launch | Auth event log analysis |
| 6 | Password reset completion | > 80% | Phase 4 (baseline) | Funnel: reset requested → new password set |
| 7 | E2E lifecycle passes | All steps correct status codes | Phase 4 | Automated E2E test suite |

**Validation approach**: Criteria 1 and 7 are gatekeeping — the service does not launch if they fail. Criteria 3, 4, 5, 6 are baselined at launch and tracked post-launch with iteration targets.

---

## 6. Timeline Estimates Per Phase

| Phase | Duration | Sprints | Key Dependencies |
|-------|----------|---------|-----------------|
| **Phase 1**: Foundation & Infrastructure | 2 weeks | Sprints 1–2 | PostgreSQL, NPM packages, RSA key pair |
| **Phase 2**: Core Authentication | 3 weeks | Sprints 2–4 | Phase 1 complete; OQ-2 and OQ-3 resolved |
| **Phase 3**: Profile & Password Reset | 3 weeks | Sprints 4–6 | Phase 2 complete; email service provisioned; OQ-1 resolved |
| **Phase 4**: Hardening & Launch | 2 weeks | Sprints 6–7 | Phase 3 complete; security review scheduled |

**Total estimated duration**: 7 sprints (~10 weeks), assuming 2-week sprints with ~1 sprint overlap between phases.

**Critical path**: PostgreSQL + key provisioning (Phase 1) → PasswordHasher + JwtService (Phase 1) → AuthService + login endpoint (Phase 2) → TokenManager + refresh rotation (Phase 2) → Password reset + email (Phase 3) → Security review + load test (Phase 4).

**Phase overlap**: Phases 1–2 overlap in Sprint 2 (JwtService tests finalize while login endpoint development begins). Phases 2–3 overlap in Sprint 4 (token refresh stabilization concurrent with profile endpoint). Phases 3–4 overlap in Sprint 6 (password reset finalization concurrent with load test setup).

---

## 7. Open Questions — Resolution Plan

| # | Question | Blocking Phase | Recommended Owner | Recommended Resolution |
|---|----------|---------------|-------------------|----------------------|
| 1 | Sync vs. async password reset email | Phase 3 | Engineering | **Recommend async** (message queue) — decouples reset endpoint latency from email delivery; aligns with resilience goals (Risk #7) |
| 2 | Max active refresh tokens per user | Phase 2 | Product | **Recommend 5** — covers desktop, mobile, tablet, plus headroom; enforced by evicting oldest on overflow |
| 3 | Account lockout after N failures | Phase 2 | Security | **Recommend progressive**: 5 failures → 15min lock, 10 failures → 1hr lock, 20 failures → admin unlock required |
| 4 | "Remember me" extending session | Post-v1.0 | Product | **Recommend deferring** — 7-day refresh TTL already provides good persistence; "remember me" adds UX complexity |
| 5 | Token revocation on user deletion | Phase 2 | Architecture | **Recommend immediate revocation** — delete user cascade deletes refresh_tokens; access tokens expire naturally within 15min |
| 6 | SOC2 audit event scope | Phase 1 | Engineering + Compliance | **Must resolve Sprint 1** — defines the event_type enum for the audit logger |
| 7 | Headless/API-only auth completeness | Phase 2 | Engineering | FR-AUTH.3 covers token refresh; service accounts / API keys deferred to v1.1 |
| 8 | Admin persona scope (Jordan) | Pre-Phase 1 | Product | **Recommend out of v1.0 scope** — audit logs queryable via database; admin UI deferred to v1.1 per spec boundary |

---

## 8. Scope Guardrails

Per PRD Scope Definition (S12) and Architectural Constraint #9, the following are **explicitly out of scope** for this roadmap:

- OAuth2/OIDC integration
- Multi-factor authentication (MFA)
- Role-based access control (RBAC)
- Social login (Google, GitHub)
- Admin UI for account management (Jordan persona — partial coverage via logs only)
- API keys or service account authentication (Sam persona — token refresh only in v1.0)

Any request to add these capabilities should be routed to a v1.1+ planning cycle with its own PRD and roadmap.
