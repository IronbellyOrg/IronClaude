---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
adversarial: true
base_variant: "Haiku (Variant B)"
variant_scores: "A:71 B:77"
convergence_score: 0.72
debate_rounds: 2
---

# User Authentication Service — Merged Project Roadmap

## Executive Summary

This roadmap defines a three-phase, 8–10 week implementation plan for the User Authentication Service, delivering secure email/password authentication with JWT session management, self-service password reset, and compliance-ready audit logging. The system serves three personas — Alex (end user), Sam (API consumer), and Jordan (platform admin) — and must satisfy SOC2 Type II and GDPR requirements before the Q3 2026 compliance deadline.

**Complexity**: MEDIUM (0.6). Security sensitivity and stateful token rotation elevate this above standard CRUD, but well-bounded scope (no OAuth/OIDC, no MFA, no RBAC in v1.0) keeps delivery predictable.

**Critical path**: Infrastructure provisioning → TokenManager + JwtService → AuthService → API endpoints → token refresh + password reset → compliance validation → production launch.

**Key architectural decisions**:
- Stateless JWT with RS256 asymmetric signing (no server-side session store)
- Refresh token rotation with replay detection (database-backed, atomic compare-and-swap)
- Layered injectable architecture: AuthService → TokenManager → JwtService, with PasswordHasher as parallel utility
- Five named integration artifacts: TokenTypeStrategy, AuthErrorRegistry, MiddlewareChain, AuditEventRegistry, ResetTokenDispatch
- Incremental audit event wiring from Phase 1 (debate-validated: lower risk than retrofit)
- Mid-stream security review at Week 3 plus pre-production review (debate-validated: catches foundational flaws early)
- Feature flag `AUTH_SERVICE_ENABLED` for rollback capability
- TypeScript implementation against PostgreSQL 15+

**Phase structure** (debate convergence — 3 phases from 4/2 compromise):
1. **Foundation & Core Authentication** (Weeks 1–3): Infrastructure, security primitives, registration, login, logout
2. **Session Management, Profile & Password Reset** (Weeks 4–7): Token refresh, profile, password reset, audit event dispatch
3. **Compliance, Performance & Launch** (Weeks 8–10): SOC2/GDPR validation, load testing, security review, production deployment

---

## Phased Implementation Plan

### Phase 1: Foundation & Core Authentication (Weeks 1–3)

**Business Outcome**: Users can register, log in, and log out with persistent session management. All auth events are logged from the start. Security primitives reviewed before expanding scope.

#### 1.1 Infrastructure & Dependency Injection Foundation (Week 1)

**Milestone 1.1.1: Database Schema & Migrations**
- Create `users` table: id (UUID), email (unique), display_name, password_hash, failed_attempts (integer, default 0), locked_until (timestamp, nullable), created_at, updated_at
- Create `refresh_tokens` table: id (UUID), user_id (FK), token_hash, expires_at, revoked_at, created_at
- Create `audit_logs` table: id, user_id, event_type, timestamp, ip_address, outcome — pre-provisioned for NFR-AUTH.5 (SOC2)
- Write down-migrations for rollback capability (architectural constraint #10)
- Execute schema validation against PostgreSQL 15+

**Dependencies**: Database access, migration tooling

**Acceptance Criteria**:
- Schema created and tested on PostgreSQL 15+
- Down-migrations execute without data loss
- `failed_attempts` and `locked_until` columns provisioned (data capture for v1.1 lockout; no endpoint logic in v1.0)
- Audit log schema supports all NFR-AUTH.5 fields
- `refresh_tokens.token_hash` indexed for revocation lookups

**Architect Notes**:
- Pre-provisioning `audit_logs` ensures events are captured from first deployment (debate convergence D3)
- `failed_attempts` / `locked_until` capture lockout data without adding v1.0 endpoint scope (debate convergence D11)
- Use surrogate keys (UUID) for all tables; no natural keys

---

**Milestone 1.1.2: Configuration & Secrets Management**
- Define configuration schema: bcrypt cost factor (default 12), JWT algorithm (RS256, configurable), token TTLs (access 15min, refresh 7d), rate limit (5/min/IP)
- Provision RSA key pair; store private key in secrets manager
- Provision `AUTH_SERVICE_ENABLED` feature flag in configuration layer (from Opus — production rollback capability)
- Load configuration from environment and policy document (SEC-POLICY-001)
- Implement configuration validation at startup (fail-fast)

**Dependencies**: Secrets manager access, SEC-POLICY-001 policy document

**Acceptance Criteria**:
- Configuration loads from environment variables
- RSA private key never logged or exposed in error messages
- Configuration validation prevents deployment with invalid values (e.g., cost factor < 10)
- Feature flag toggles all auth routes on/off

---

**Milestone 1.1.3: Dependency Injection Container**
- Create injectable interface definitions: `PasswordHasher`, `JwtService`, `TokenManager`, `UserRepository`, `RefreshTokenRepository`
- Implement DI container wiring all components
- Register all service implementations
- Ensure all services independently testable

**Acceptance Criteria**:
- All core services are injectable interfaces
- Container resolves without circular references
- Unit tests can mock any service without full container
- Constructor injection throughout (no service locator)

---

#### 1.2 Core Security Components (Weeks 1–2)

**Milestone 1.2.1: PasswordHasher Implementation**
- Implement password hashing using bcrypt with configurable cost factor (default 12) per NFR-AUTH.3
- Implement constant-time password verification
- Add guard assertion: reject passwords failing policy (8-char min, 1 uppercase, 1 lowercase, 1 digit) as defense-in-depth backstop (debate convergence D7)
- Benchmark test confirming ~250ms hash time
- Raw passwords never logged or persisted (NFR-AUTH.7)

**Dependencies**: `bcrypt` NPM package

**Acceptance Criteria**:
- All passwords hashed with bcrypt cost 12 (configurable)
- Guard rejects weak passwords even if endpoint validation is bypassed
- Hash operation ~250ms (NFR-AUTH.3 benchmark passes)
- Verification is constant-time
- No password in logs, errors, or test output

---

**Milestone 1.2.2: JwtService Implementation**
- Implement JWT signing with `jsonwebtoken` library using RS256
- Implement verification with public key
- Define payload: `{ sub: user_id, iat, exp, type: "access" | "refresh" }`
- Support configurable TTLs (15min access, 7d refresh)
- Unit tests: valid token, expired token, tampered payload, algorithm confusion attack

**Dependencies**: `jsonwebtoken` NPM package, RSA key pair from 1.1.2

**Acceptance Criteria**:
- Signs with RS256 and private key; verifies with public key
- Expired/tampered/algorithm-mismatched tokens rejected
- Token type field distinguishes access vs refresh
- No token contents in error logs

---

**Milestone 1.2.3: TokenManager Implementation**

**INTEGRATION POINT: TokenTypeStrategy Registry**
- **Artifact**: `TokenTypeStrategy` interface + dispatcher
- **Components**: `AccessTokenStrategy` (15min TTL, stateless), `RefreshTokenStrategy` (7d TTL, rotation, database-backed)
- **Owning Phase**: Phase 1, Milestone 1.2.3
- **Consumed By**: FR-AUTH.1 (login), FR-AUTH.3 (refresh), FR-AUTH.5 (password reset invalidation)

**Implementation**:
- `TokenManager.issueTokenPair(userId)` → {accessToken, refreshToken}
- `TokenManager.verifyAccessToken(token)` → userId or 401
- `TokenManager.rotateRefreshToken(oldToken)` → new pair or 401

**Refresh Token Rotation & Replay Detection (FR-AUTH.3c)**:
1. Verify oldToken valid and not previously rotated
2. Check `refresh_tokens.token_hash` for revocation status
3. If `revoked_at` set from a different rotation → replay detected → invalidate ALL user tokens
4. If valid → hash new token, store, mark old as revoked
5. Return new token pair

**Acceptance Criteria**:
- Token pair issued correctly with proper TTLs
- Rotation is atomic: failure leaves database unchanged
- Replay detection invalidates all user sessions
- Dispatch registry routes access vs refresh strategies correctly

**Architect Notes** (from Opus — critical implementation detail):
- Rotation MUST use database-level compare-and-swap on token hash to prevent race conditions under concurrent refresh requests. A naive read-then-write creates a window where two concurrent refreshes both succeed, breaking the rotation chain.

---

#### 1.3 User Repository & Authentication Service (Week 2)

**Milestone 1.3.1: UserRepository Implementation**
- CRUD for users table: `findByEmail()`, `findById()`, `create()`, `updatePassword()`
- Unique constraint validation on email (FR-AUTH.2b → 409)
- All queries parameterized (SQL injection prevention)
- `password_hash` never selected except for login verification

**Acceptance Criteria**:
- Prepared statements throughout
- Duplicate email raises ConstraintError → 409
- `create()` returns user without password_hash
- Database transactions ensure atomicity

---

**Milestone 1.3.2: AuthService Implementation**

**INTEGRATION POINT: AuthErrorRegistry**
- **Artifact**: `AuthErrorRegistry` map
- **Components**: InvalidCredentials→401, UserAlreadyExists→409, AccountLocked→403, RateLimitExceeded→429, InvalidToken→401
- **Owning Phase**: Phase 1, Milestone 1.3.2
- **Consumed By**: All API endpoints

**Implementation**:
- Orchestrate registration (FR-AUTH.2): validate → hash → create → issue tokens
- Orchestrate login (FR-AUTH.1): lookup → verify → issue tokens → rate limit → 401 generic on failure
- Orchestrate logout: invalidate refresh token
- Emit audit events for all auth operations (register, login, login_failed, logout)

**Acceptance Criteria**:
- Registration validates email, password policy (endpoint-level for UX messages, per debate D7), and uniqueness
- Login is constant-time (no enumeration)
- Failed attempts counted and rate-limited per IP
- All auth events logged with user_id, event_type, timestamp, ip_address, outcome
- Error codes registered in AuthErrorRegistry

---

#### 1.4 API Endpoints & Middleware (Weeks 2–3)

**Milestone 1.4.1: Authentication Middleware**

**INTEGRATION POINT: MiddlewareChain**
- **Artifact**: `MiddlewareChain` (request pipeline)
- **Components**: AuthMiddleware (Bearer → verify → user context), RateLimitMiddleware (5/min/IP on login), AuditLoggingMiddleware (log all auth calls)
- **Owning Phase**: Phase 1, Milestone 1.4.1
- **Consumed By**: All endpoints in Phases 1–3

**Acceptance Criteria**:
- Bearer token extracted and verified
- Verification failures return 401 via AuthErrorRegistry
- User context available to downstream handlers

---

**Milestone 1.4.2: POST /register (FR-AUTH.2)**
- Input: { email, password, display_name }
- Endpoint-level password policy validation with inline error hints (FR-AUTH.2c) — provides UX-friendly messages (debate convergence D7)
- Email format validation (FR-AUTH.2d)
- On success: 201 with user profile + tokens
- On duplicate: 409 (FR-AUTH.2b)
- No password_hash in response
- Gate behind `AUTH_SERVICE_ENABLED` feature flag
- Audit event emitted

---

**Milestone 1.4.3: POST /login (FR-AUTH.1)**
- Input: { email, password }
- On success: 200 with access_token (body) + refresh_token (httpOnly cookie, Secure, SameSite=Strict)
- On invalid: 401 generic (FR-AUTH.1b, no enumeration)
- On locked: 403 (FR-AUTH.1c, conditional on lockout state)
- Rate limit: 5/min/IP → 429 (FR-AUTH.1d)
- Audit event emitted (success and failure)

---

**Milestone 1.4.4: POST /logout**
- Requires authentication (Bearer token or cookie)
- Invalidates refresh token (sets `revoked_at`)
- Returns 204
- Audit event emitted
- Resolves Open Question #10 (PRD user story AUTH-E1)

**Acceptance Criteria**:
- Subsequent use of invalidated token returns 401
- Audit log entry created

---

#### 1.5 Integration Testing & Security Checkpoint (Week 3)

**Milestone 1.5.1: Phase 1 Integration Test Suite**
- E2E: register → login → verify token → logout
- Token expiration: access expires 15min, refresh valid 7d
- Rate limiting: 6th attempt in 1min → 429
- Duplicate email → 409
- Audit log validation: all events logged with correct fields
- Token rotation: rotate refresh, old becomes invalid

---

**Milestone 1.5.2: Mid-Stream Security Review (Checkpoint)**
- Code review by security engineer: password hashing, JWT signing, token storage, rate limiting, secrets management
- Verify: no hard-coded secrets, no sensitive data in logs, no SQL injection, constant-time comparisons, bcrypt cost factor
- Approve proceeding to Phase 2

**Dependencies**: Security engineer availability (budgeted at 0.3 FTE)

**Acceptance Criteria**:
- No critical or high-severity findings
- Password, token, and secrets handling approved

---

**Phase 1 Completion Criteria**:
- All Milestones 1.1–1.5 complete
- FR-AUTH.1, FR-AUTH.2 passing acceptance criteria
- Token dispatch registry, error registry, middleware chain functional
- Audit events emitting for all operations
- Security review signed off
- **Estimated Effort**: 3 weeks (~5.4 engineer-weeks at 1.0 + 0.5 + 0.3 FTE)

---

### Phase 2: Session Management, Profile & Password Reset (Weeks 4–7)

**Business Outcome**: Users maintain persistent sessions across page refreshes, view profiles, self-serve password resets. Audit event dispatch is complete. GDPR consent captured.

#### 2.1 Token Refresh & Client Persistence (Week 4)

**Milestone 2.1.1: POST /refresh (FR-AUTH.3)**
- Input: refresh_token (httpOnly cookie or body)
- On success: 200 with new access + rotated refresh tokens (FR-AUTH.3a)
- On expired: 401 requiring re-login (FR-AUTH.3b)
- On replayed: invalidate ALL user tokens (FR-AUTH.3c)
- Refresh token hash stored in database (FR-AUTH.3d)
- Audit event emitted

**Acceptance Criteria**:
- Valid refresh returns new pair
- Expired → 401
- Replayed → full user token invalidation
- Hash stored (not plain token)

---

**Milestone 2.1.2: Client-Side Token Persistence**
- Access token in memory (lost on page refresh)
- Refresh token in httpOnly cookie (Secure + SameSite=Strict)
- Silent refresh transparent to user (no login prompt within 7d window)
- Persona coverage: Alex (seamless UX), Sam (programmatic refresh)

---

#### 2.2 User Profile (Week 4)

**Milestone 2.2.1: GET /profile (FR-AUTH.4)**
- Requires Bearer token
- Returns: id, email, display_name, created_at (FR-AUTH.4a)
- Never includes password_hash or token data (FR-AUTH.4c)
- Expired/invalid → 401 (FR-AUTH.4b)
- Audit event emitted

---

#### 2.3 Password Reset Flow (Weeks 4–5)

**Milestone 2.3.1: Password Reset Token Service**

**INTEGRATION POINT: ResetTokenDispatch**
- **Artifact**: `ResetTokenGenerator` + `ResetTokenValidator`
- **Components**: Email-based reset (v1.0), SMS-based (deferred v2.0)
- **Owning Phase**: Phase 2, Milestone 2.3.1
- **Consumed By**: FR-AUTH.5

**Implementation**:
- Generate cryptographically secure reset token
- Store hash in dedicated `password_reset_tokens` table (user_id, token_hash, expires_at, consumed_at)
- Schema migration for dedicated table (architecturally superior to sharing refresh_tokens — debate-validated)
- 1-hour configurable TTL

---

**Milestone 2.3.2: POST /password-reset/request (FR-AUTH.5a)**
- Input: { email }
- Always returns 200 (no enumeration)
- If email exists: generate token, store hash, dispatch email
- Email within 60 seconds
- Rate limit: 3/hour/email
- Email dispatch: synchronous acceptable for v1.0 given low volume; recommend async via message queue for v1.1 resilience (from Opus — pragmatic nuance)

---

**Milestone 2.3.3: POST /password-reset/confirm (FR-AUTH.5b, 5d)**
- Input: { reset_token, new_password }
- Validate token (hash, TTL, not consumed)
- On invalid/expired: 400 (FR-AUTH.5c)
- On valid: hash new password, update user, invalidate ALL refresh tokens (FR-AUTH.5d), mark token consumed
- Audit event emitted

---

#### 2.4 Audit Logging & GDPR Compliance (Weeks 5–6)

**Milestone 2.4.1: Audit Event Dispatch Completion**

**INTEGRATION POINT: AuditEventRegistry**
- **Artifact**: `AuditEventType` enum + `AuditEventDispatcher`
- **Components**: register, login, login_failed, logout, refresh_token, password_reset_requested, password_reset_confirmed, profile_accessed
- **Owning Phase**: Phase 2, Milestone 2.4.1 (completion; initial wiring in Phase 1)
- **Consumed By**: All endpoints

**Implementation**:
- Verify all Phase 2 endpoints emit events
- Ensure atomic logging (fail-secure: audit write failure rolls back transaction)
- 12-month retention policy configured

---

**Milestone 2.4.2: Audit Log Query Interface**
- Query by user_id, date range, event_type
- Retention validation test: 12-month minimum
- Note: Admin UI deferred to v1.1; logs queryable via database tooling (Persona: Jordan — deferred)

---

**Milestone 2.4.3: GDPR Consent Capture (NFR-AUTH.4)**
- Add `consents` table: user_id, consent_type, timestamp, version
- Registration flow: consent checkbox required before submission
- Record stored with timestamp (auditable proof)
- Registration blocked without consent

---

#### 2.5 Phase 2 Integration Testing (Week 7)

**Milestone 2.5.1: Phase 2 E2E Test Suite**
- E2E: register → login → refresh → profile → password reset → re-login
- Token rotation and replay detection validated end-to-end
- Audit trail completeness: lifecycle sample generated
- All FR-AUTH.3, FR-AUTH.4, FR-AUTH.5 passing

---

**Phase 2 Completion Criteria**:
- All Milestones 2.1–2.5 complete
- Full auth surface functional
- Audit event dispatch complete for all endpoints
- GDPR consent implemented
- **Estimated Effort**: 4 weeks (~7.2 engineer-weeks at 1.0 + 0.5 + 0.3 FTE)

---

### Phase 3: Compliance, Performance & Launch (Weeks 8–10)

**Business Outcome**: System validated against NFRs, compliance requirements met, production-ready with controlled rollout.

#### 3.1 Compliance Validation (Week 8)

**Milestone 3.1.1: SOC2 Compliance Validation (NFR-AUTH.5)**
- Audit log field completeness verified
- 12-month retention policy enforced
- Lifecycle audit trail sample: register → login → refresh → logout
- Compliance checklist signed off

---

**Milestone 3.1.2: NIST SP 800-63B Validation (NFR-AUTH.7)**
- Passwords hashed with one-way adaptive hashing (bcrypt) ✓
- Raw passwords never persisted or logged ✓
- Constant-time comparison ✓
- Security team sign-off

---

**Milestone 3.1.3: GDPR Data Minimization Validation (NFR-AUTH.6)**
- Schema audit: only email, password_hash, display_name collected
- No extraneous PII fields
- Consent records complete for all users

---

#### 3.2 Performance & Reliability (Week 9)

**Milestone 3.2.1: Load Testing (NFR-AUTH.1)**
- k6 load test: < 200ms p95 for all auth endpoints
- Sustain 500 concurrent requests
- Connection pool tuning and query optimization

---

**Milestone 3.2.2: Health Check & Monitoring (NFR-AUTH.2)**
- Health check endpoint for uptime monitoring
- PagerDuty alerting integration
- Target: 99.9% availability
- Email delivery monitoring and alerting

---

#### 3.3 Security Review & Launch (Weeks 9–10)

**Milestone 3.3.1: Pre-Production Security Review**
- Comprehensive review: JWT implementation, token rotation, replay detection, password hashing, rate limiting, input validation, user enumeration prevention
- Penetration testing
- E2E test suite covering all customer journeys

---

**Milestone 3.3.2: Production Deployment**
- Deploy with `AUTH_SERVICE_ENABLED` flag initially disabled (from Opus)
- Gradual rollout: 5% → 25% → 50% → 100%
- Monitor error rates, latency, audit log volume at each stage
- All success criteria validated before 100% rollout

---

**Phase 3 Completion Criteria**:
- All NFRs validated with evidence
- Security review + pen test complete, no critical findings
- All success criteria met
- Production deployed with controlled rollout
- **Estimated Effort**: 2–3 weeks (~4.5 engineer-weeks at 1.0 + 0.5 + 0.3 FTE)

---

## Risk Assessment and Mitigation

| # | Risk | Severity | Probability | Mitigation | Phase | Notes |
|---|------|----------|-------------|------------|-------|-------|
| 1 | JWT private key compromise | High | Low | RS256 asymmetric keys in secrets manager; 90-day rotation; key access auditing | 1.1 | |
| 2 | Refresh token replay attack | High | Medium | Rotation with replay detection (FR-AUTH.3c); database-level compare-and-swap for atomicity under concurrent requests | 1.2, 2.1 | Opus architect note: naive read-then-write creates race condition window |
| 3 | bcrypt cost factor insufficient | Medium | Low | Configurable cost factor; annual OWASP review; Argon2id migration path | 1.2 | |
| 4 | Low registration adoption | High | Medium | Inline validation, < 60s target, usability testing; post-launch funnel monitoring | 1.4, 3.3 | |
| 5 | Security breach from implementation flaws | Critical | Low | Mid-stream review (Week 3) + pre-production review + pen test; no deployment without sign-off | 1.5, 3.3 | Two checkpoints per debate convergence D4 |
| 6 | Incomplete audit logging | High | Medium | Incremental wiring from Phase 1; validated against SOC2 in Phase 3 | 1.3–2.4, 3.1 | Early wiring per debate convergence D3 |
| 7 | Email delivery failures | Medium | Low | Delivery monitoring + alerting; retry logic; fallback support channel | 2.3, 3.2 | Sync acceptable v1.0; async recommended v1.1 |

---

## Resource Requirements

### Human Resources

| Role | FTE | Duration | Key Responsibilities |
|------|-----|----------|---------------------|
| Backend Engineer (Lead) | 1.0 | 8–10 weeks | Core services, TokenManager, AuthService, integration tests |
| Backend Engineer (Support) | 0.5 | 8–10 weeks | API endpoints, password reset, unit tests |
| Security Engineer | 0.3 | 8–10 weeks | Architecture review (Week 3), code review, pen test scoping |
| QA Engineer | 0.5 | 8–10 weeks | Integration/E2E tests, load testing, audit validation |
| DevOps | 0.2 | 8–10 weeks | Database, secrets, email service, monitoring, deployment |
| Compliance/Legal | 0.1 | 8–10 weeks | GDPR requirements, SOC2 readiness |
| Product Manager | 0.2 | 8–10 weeks | Open question resolution, success metrics |

**Total**: ~2.8 FTE over 8–10 weeks (~22–28 engineer-weeks)

### Technical Dependencies

| Dependency | Required By | Status | Action |
|-----------|-------------|--------|--------|
| `jsonwebtoken` NPM | Phase 1.2 | Available | Pin version |
| `bcrypt` NPM | Phase 1.2 | Available | Pin version |
| Email service (SendGrid) | Phase 2.3 | Must procure | Provision Week 1 |
| PostgreSQL 15+ | Phase 1.1 | Must provision | Provision before start |
| RSA key pair + secrets manager | Phase 1.1 | Not provisioned | DevOps must provision before Phase 1 |
| Frontend routing framework | Phase 1.4 | Assumed available | Confirm before start |
| SEC-POLICY-001 | Phase 1.2 | Unknown | Security team must provide |

---

## Success Criteria and Validation

### Pre-Launch Gates (must pass before production)

| # | Criterion | Target | Validation | Phase |
|---|-----------|--------|-----------|-------|
| 1 | Login p95 response time | < 200ms | k6 load test | 3.2 |
| 2 | Service availability | ≥ 99.9% | Health check + PagerDuty | 3.2 |
| 3 | All tests passing | 100% | CI: unit + integration + E2E | 3.3 |
| 4 | SOC2 audit log completeness | All events; 12-month retention | Log audit + retention verification | 3.1 |

### Post-Launch Monitoring (measured after rollout)

| # | Criterion | Target | Validation | Owner |
|---|-----------|--------|-----------|-------|
| 5 | Registration conversion rate | > 60% | Funnel analytics | Product |
| 6 | Average session duration | > 30 min | Token refresh analytics | Product |
| 7 | Failed login rate | < 5% | Auth event log analysis | Product |
| 8 | Password reset completion | > 80% | Reset funnel analytics | Product |

---

## Timeline Estimates

| Phase | Weeks | Duration | Key Gates |
|-------|-------|----------|-----------|
| **Phase 1**: Foundation & Core Auth | 1–3 | 3 weeks | Security review checkpoint (Week 3) |
| **Phase 2**: Session, Profile, Reset | 4–7 | 4 weeks | Full auth surface complete (Week 7) |
| **Phase 3**: Compliance & Launch | 8–10 | 2–3 weeks | Production deployment (Week 9–10) |
| **Total** | | **8–10 weeks** | Depends on team capacity |

**Note**: Timeline assumes ~2 FTE backend + fractional security/QA/DevOps. With 1 FTE, extend to 12–14 weeks. With 2.8 FTE and aggressive parallelization, 8 weeks is achievable. The debate convergence estimate of 8–10 weeks with ~2 FTE is the recommended planning baseline.

**Critical milestones**:
- **Week 3**: Infrastructure + security primitives ready, security review passed
- **Week 7**: Full auth surface complete (register, login, logout, refresh, profile, reset)
- **Week 9–10**: Production-ready with compliance sign-off

---

## Open Questions Requiring Resolution

| # | Question | Blocks Phase | Recommended Resolution | Decision Owner |
|---|----------|--------------|------------------------|----------------|
| 1 | Sync vs. async email dispatch? | 2.3 | Sync acceptable v1.0 (low volume); async via message queue for v1.1 | Engineering |
| 2 | Max active refresh tokens per user? | 2.1 | Cap at 5 (phone + laptop + tablet + 2 API clients); oldest revoked on overflow | Product |
| 3 | Account lockout policy after N failures? | Post-v1.0 | v1.0: schema provisioned (failed_attempts, locked_until); v1.1: progressive lockout (5→15min, 10→1hr, 20→admin) | Security |
| 4 | "Remember me" extending session beyond 7d? | Post-v1.0 | Defer to v1.1; 7d refresh TTL sufficient for v1.0 | Product |
| 5 | Audit logging field requirements (GAP-2)? | **3.1 (blocker)** | Adopt PRD spec: user_id, event_type, timestamp, IP, outcome. 12-month retention. Resolve early to avoid rework | Security/Compliance |
| 6 | Token revocation on account deletion? | Post-v1.0 | Account deletion not in scope; document as v1.1 | Architecture |
| 7 | GDPR consent — v1.0 hard requirement? | **1.4 / 2.4** | Yes — include. GDPR applies at data collection time; deferral creates compliance risk | Legal/Product |
| 8 | JTBD #2 work-state preservation? | Out of scope | Not an auth concern; separate feature | Product |
| 9 | Admin audit log UI in v1.0? | 2.4 | Out of v1.0. Logs queryable via database; admin UI in v1.1 | Product/Engineering |
| 10 | Explicit logout endpoint? | **1.4** | Include — PRD user story exists, minimal effort (revoke refresh + clear cookie) | Product |

**Architect's recommendation**: Questions #5, #7, and #10 must be resolved immediately — they affect Phase 1 planning. Question #3 requires only schema provisioning for v1.0 (already addressed in Milestone 1.1.1).

---

## Scope Guardrails

Per the PRD Scope Definition, the following are explicitly **out of scope** for this roadmap:

| Capability | Status | Redirect |
|------------|--------|----------|
| OAuth2/OIDC federation | Out of scope | v2.0 PRD |
| Multi-factor authentication | Out of scope | v1.1; requires SMS/TOTP infrastructure |
| Role-based access control | Out of scope | Separate authorization PRD |
| Social login (Google, GitHub) | Out of scope | Depends on OAuth/OIDC (v2.0) |
| Admin UI for user management | Out of scope | v1.1; logs queryable via database in v1.0 |
| Account deletion | Out of scope | v1.1; Open Question #6 |
| Account lockout logic | Schema only in v1.0 | v1.1 full implementation |
| Work-state preservation | Out of scope | Separate feature; Open Question #8 |

Any request to add these capabilities during v1.0 development should be redirected to the appropriate future release PRD.

---

## Appendix: Integration Points Summary

| # | Artifact | Type | Owning Milestone | Consumed By |
|---|----------|------|-----------------|-------------|
| 1 | TokenTypeStrategy Registry | Dispatcher | 1.2.3 | Login, refresh, password reset invalidation |
| 2 | AuthErrorRegistry | Map | 1.3.2 | All API endpoints |
| 3 | MiddlewareChain | Pipeline | 1.4.1 | All protected endpoints |
| 4 | AuditEventRegistry | Dispatcher | 1.3.2 (initial), 2.4.1 (complete) | All endpoints, SOC2 validation |
| 5 | ResetTokenDispatch | Generator + Validator | 2.3.1 | Password reset endpoints |

These registries require explicit factory/wiring code — they are not implicit in the component design. The roadmap specifies creation and consumption phases for each to prevent integration gaps.

---

## Pre-Phase 1 Checklist

- [ ] Finalize SEC-POLICY-001 (password policy, token TTLs, bcrypt cost factor)
- [ ] Resolve Open Questions #5, #7, #10 with Product, Security, Compliance
- [ ] Provision PostgreSQL 15+, RSA key pair, email service, secrets manager
- [ ] Assign Backend Lead, Backend Support, Security Engineer, QA
- [ ] Schedule security review checkpoint (Phase 1, Week 3)
- [ ] Confirm frontend routing framework availability
