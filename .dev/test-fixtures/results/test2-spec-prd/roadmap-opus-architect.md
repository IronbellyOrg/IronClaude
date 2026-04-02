---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
generated: "2026-03-31T00:00:00Z"
generator: "roadmap-architect"
total_phases: 4
total_milestones: 8
risk_count: 7
open_questions: 10
---

# User Authentication Service — Project Roadmap

## 1. Executive Summary

This roadmap defines a four-phase implementation plan for the User Authentication Service, delivering secure email/password authentication with JWT session management, self-service password reset, and compliance-ready audit logging. The system serves three distinct personas (end user, platform admin, API consumer) and must satisfy both SOC2 Type II and GDPR requirements before the Q3 2026 compliance deadline.

**Complexity**: MEDIUM (0.6). Security sensitivity and stateful token rotation elevate this above standard CRUD, but well-bounded scope (no OAuth/OIDC, no MFA, no RBAC in v1.0) keeps delivery predictable.

**Critical path**: Infrastructure provisioning → database schema → password hashing + JWT signing → login/registration endpoints → token refresh with rotation → password reset with email integration → audit logging → compliance validation.

**Key architectural decisions**:
- Stateless JWT with RS256 asymmetric signing (no server-side session store)
- Refresh token rotation with replay detection (database-backed)
- Layered injectable architecture: AuthService → TokenManager → JwtService, with PasswordHasher as parallel utility
- Feature flag `AUTH_SERVICE_ENABLED` for rollback capability
- TypeScript implementation against PostgreSQL 15+

---

## 2. Phased Implementation Plan

### Phase 1: Foundation & Infrastructure (Sprints 1–2)

**Objective**: Establish all infrastructure, dependencies, and core security primitives required by every subsequent phase.

#### Milestone 1.1: Infrastructure Provisioning
- [ ] Provision PostgreSQL 15+ instance with connection pooling
- [ ] Create database migrations (with down-migration scripts per Constraint #10):
  - `users` table: id (UUID), email (unique), password_hash, display_name, created_at, updated_at, locked_at
  - `refresh_tokens` table: id (UUID), user_id (FK), token_hash, expires_at, revoked_at, created_at
- [ ] Generate RS256 key pair; store private key in secrets manager (Risk #1 mitigation)
- [ ] Configure key rotation schedule (90-day cycle)
- [ ] Set up `AUTH_SERVICE_ENABLED` feature flag in configuration layer
- [ ] Provision email delivery service (SendGrid or equivalent) — Dependency #3
- [ ] Establish CI pipeline with lint, type-check, unit test stages

**Requirements addressed**: Architectural Constraints #1, #4, #5, #6, #9, #10; Dependencies #4, #5

#### Milestone 1.2: Core Security Primitives
- [ ] Implement **PasswordHasher** module
  - bcrypt with configurable cost factor (default 12) per NFR-AUTH.3
  - Benchmark test verifying ~250ms hash time
  - Unit test confirming cost factor configuration
  - Raw passwords never logged or persisted (NFR-AUTH.7)
- [ ] Implement **JwtService** module
  - RS256 sign/verify with injected key material
  - Access token: 15-minute TTL
  - Claims: sub (user_id), iat, exp, jti
- [ ] Implement **TokenManager** module
  - Token generation (access + refresh)
  - Refresh token hash storage in database
  - Token validation and expiry checking

**Requirements addressed**: NFR-AUTH.3, NFR-AUTH.7; Dependencies #1, #2

#### Integration Points — Phase 1

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|----------------|------|-------------------|--------------|-------------|
| `PasswordHasher` | Injectable utility | bcrypt adapter | Phase 1.2 | Phase 2 (registration, login, password reset) |
| `JwtService` | Injectable service | RS256 signer/verifier | Phase 1.2 | Phase 2 (login), Phase 3 (refresh, profile) |
| `TokenManager` | Injectable service | JwtService, RefreshToken repository | Phase 1.2 | Phase 2 (login), Phase 3 (refresh, reset) |
| Database migration registry | Migration runner | users, refresh_tokens schemas | Phase 1.1 | All phases (schema is foundational) |
| Feature flag registry | Config service | `AUTH_SERVICE_ENABLED` flag | Phase 1.1 | Phase 2 (route gating) |

**Exit criteria**: All migrations run and rollback successfully. PasswordHasher, JwtService, and TokenManager pass unit tests in isolation. RS256 key pair is stored in secrets manager and accessible to JwtService. CI pipeline green.

---

### Phase 2: Core Authentication (Sprints 2–3)

**Objective**: Deliver registration, login, and GDPR consent — the minimum viable authentication surface.

#### Milestone 2.1: User Registration (FR-AUTH.2)
- [ ] Implement registration endpoint (`POST /auth/register`)
  - **FR-AUTH.2a**: Valid input (email, password, display_name) → create user record → return 201 with user profile
  - **FR-AUTH.2b**: Duplicate email → return 409 conflict
  - **FR-AUTH.2c**: Password policy enforcement: min 8 chars, 1 uppercase, 1 lowercase, 1 digit
  - **FR-AUTH.2d**: Email format validation before database interaction
- [ ] Wire **PasswordHasher** into registration flow (hash before storage)
- [ ] Implement GDPR consent capture at registration (NFR-AUTH.4)
  - Consent checkbox required before submission
  - Record consent timestamp in `users` table (or dedicated `consents` table)
  - Schema migration for consent field(s)
- [ ] Implement data minimization validation (NFR-AUTH.6): reject any PII fields beyond email, password, display_name
- [ ] Frontend: registration form with inline validation (Persona: Alex — < 60 seconds to complete)
  - Inline password policy feedback
  - Email format validation on blur
  - No user enumeration in error responses

**Requirements addressed**: FR-AUTH.2 (all sub-criteria), NFR-AUTH.4, NFR-AUTH.6

#### Milestone 2.2: User Login (FR-AUTH.1)
- [ ] Implement login endpoint (`POST /auth/login`)
  - **FR-AUTH.1a**: Valid credentials → 200 with access_token (15min TTL) and refresh_token (7d TTL)
  - **FR-AUTH.1b**: Invalid credentials → 401 with generic message (no email/password distinction)
  - **FR-AUTH.1c**: Locked account → 403 indicating suspension
  - **FR-AUTH.1d**: Rate limiting: 5 attempts per minute per IP address
- [ ] Wire **PasswordHasher** (verify) and **TokenManager** (issue) into login flow
- [ ] Set refresh token as httpOnly cookie (Constraint #3) — never in localStorage/sessionStorage
- [ ] Access token returned in response body for client-side memory storage
- [ ] Frontend: login form with generic error messaging (no user enumeration per Persona: Alex)
- [ ] Gate all auth routes behind `AUTH_SERVICE_ENABLED` feature flag

**Requirements addressed**: FR-AUTH.1 (all sub-criteria)

#### Integration Points — Phase 2

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|----------------|------|-------------------|--------------|-------------|
| Auth route registry | Express/framework router | register, login handlers | Phase 2 | Phase 3 (refresh, profile, reset endpoints added) |
| Rate limiter middleware | Middleware chain | IP-based limiter on `/auth/login` | Phase 2.2 | Phase 2.2 (login), potentially Phase 3 (reset) |
| Consent recording mechanism | Database + validation | Registration handler → consents storage | Phase 2.1 | Phase 4 (compliance audit) |
| Feature flag gate middleware | Middleware chain | `AUTH_SERVICE_ENABLED` → route enable/disable | Phase 2.2 | All auth routes (Phases 2–3) |

**Exit criteria**: Registration and login endpoints pass integration tests. Rate limiting verified under load. GDPR consent recorded in database. Refresh token set as httpOnly cookie. No sensitive data (password_hash) in any response. Feature flag toggles routing on/off.

---

### Phase 3: Session Management & Account Recovery (Sprints 3–5)

**Objective**: Complete the authentication surface with token refresh, profile retrieval, and password reset.

#### Milestone 3.1: Token Refresh (FR-AUTH.3)
- [ ] Implement refresh endpoint (`POST /auth/token/refresh`)
  - **FR-AUTH.3a**: Valid refresh token → new access_token + rotated refresh_token
  - **FR-AUTH.3b**: Expired refresh token → 401 requiring re-authentication
  - **FR-AUTH.3c**: Replay detection — reuse of previously-rotated token → revoke ALL user tokens
  - **FR-AUTH.3d**: Refresh token hashes stored in database for revocation support
- [ ] Wire **TokenManager** rotation logic: old token marked revoked, new token hash stored
- [ ] Frontend: silent background token refresh (Persona: Alex — no re-login prompts during active use; Persona: Sam — programmatic refresh without user interaction)

**Requirements addressed**: FR-AUTH.3 (all sub-criteria)

#### Milestone 3.2: Profile Retrieval (FR-AUTH.4)
- [ ] Implement profile endpoint (`GET /auth/profile`)
  - **FR-AUTH.4a**: Valid Bearer token → return user profile (id, email, display_name, created_at)
  - **FR-AUTH.4b**: Expired/invalid token → 401
  - **FR-AUTH.4c**: Sensitive fields (password_hash, refresh_token_hash) excluded from response
- [ ] Wire authentication middleware that validates access tokens via **JwtService**
- [ ] Frontend: profile page rendering (Persona: Alex)

**Requirements addressed**: FR-AUTH.4 (all sub-criteria)

#### Milestone 3.3: Password Reset (FR-AUTH.5)
- [ ] Implement reset request endpoint (`POST /auth/password-reset/request`)
  - **FR-AUTH.5a**: Registered email → generate reset token (1-hour TTL) → dispatch email
  - Return identical response for unregistered emails (no user enumeration)
- [ ] Implement reset execution endpoint (`POST /auth/password-reset/confirm`)
  - **FR-AUTH.5b**: Valid reset token → set new password → invalidate reset token
  - **FR-AUTH.5c**: Expired/invalid token → 400 with clear error
  - **FR-AUTH.5d**: All existing refresh tokens invalidated upon successful reset
- [ ] Wire **PasswordHasher** (new hash), **TokenManager** (revoke all refresh tokens), and email service
- [ ] Frontend: reset request form, reset confirmation form (email within 60 seconds per Customer Journey)
- [ ] Decision required: synchronous vs. async email dispatch (Open Question #1) — recommend async via message queue for resilience, but synchronous acceptable for v1.0 given low volume

**Requirements addressed**: FR-AUTH.5 (all sub-criteria); Dependency #3 (email service)

#### Integration Points — Phase 3

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|----------------|------|-------------------|--------------|-------------|
| Auth middleware (token validation) | Middleware chain | JwtService → request context injection | Phase 3.2 | All protected endpoints (profile, future features) |
| Token rotation mechanism | Database + TokenManager | Refresh handler → revoke old, issue new | Phase 3.1 | Phase 3.3 (revoke-all on password reset) |
| Email dispatch service | Service adapter | Reset handler → SendGrid adapter | Phase 3.3 | Phase 3.3 (password reset); future features |
| Token revocation cascade | Database operation | Password reset → bulk revoke refresh tokens | Phase 3.3 | Phase 3.3 |

**Exit criteria**: Token refresh with rotation passes integration tests including replay detection. Profile endpoint returns correct data with sensitive fields excluded. Password reset end-to-end flow works including email delivery. All existing sessions invalidated on password change.

---

### Phase 4: Compliance, Performance & Launch Readiness (Sprints 5–6)

**Objective**: Satisfy NFRs, compliance requirements, and production readiness gates.

#### Milestone 4.1: Audit Logging & Compliance (NFR-AUTH.5, NFR-AUTH.4)
- [ ] Implement structured audit logging for all auth events:
  - Fields: user_id, event_type, timestamp, IP address, outcome (NFR-AUTH.5)
  - Events: login_success, login_failure, registration, token_refresh, password_reset_request, password_reset_complete, token_revocation
  - 12-month retention policy configured
- [ ] Validate GDPR consent records are complete and queryable (NFR-AUTH.4)
- [ ] Validate data minimization — schema review confirms no extra PII (NFR-AUTH.6)
- [ ] Validate password hashing meets NIST SP 800-63B (NFR-AUTH.7, NFR-AUTH.3)
- [ ] Note: Admin audit log UI (Persona: Jordan) is out of v1.0 scope per Open Question #9 — logs are queryable via database/tooling but no dedicated admin interface

**Requirements addressed**: NFR-AUTH.4, NFR-AUTH.5, NFR-AUTH.6, NFR-AUTH.7; Success Criterion #8

#### Milestone 4.2: Performance & Reliability
- [ ] Load testing with k6 (NFR-AUTH.1):
  - Target: < 200ms p95 for all auth endpoints
  - Target: sustain 500 concurrent requests
- [ ] Health check endpoint for uptime monitoring (NFR-AUTH.2)
  - PagerDuty alerting integration
  - Target: 99.9% availability (< 8.76 hours downtime/year)
- [ ] Connection pool tuning and database query optimization
- [ ] Email delivery monitoring and alerting (Risk #7 mitigation)

**Requirements addressed**: NFR-AUTH.1, NFR-AUTH.2; Success Criteria #2, #6

#### Milestone 4.3: Security Review & Launch
- [ ] Dedicated security review of:
  - JWT implementation (RS256, key storage, token validation)
  - Refresh token rotation and replay detection
  - Password hashing configuration
  - Rate limiting effectiveness
  - Input validation and injection prevention
  - No user enumeration in any endpoint
- [ ] Penetration testing before production (Risk #5 mitigation)
- [ ] Validate all success criteria (see Section 5)
- [ ] E2E test suite covering all customer journeys (signup, login, refresh, reset, profile)
- [ ] Production deployment with `AUTH_SERVICE_ENABLED` flag initially disabled → gradual rollout

**Requirements addressed**: Risk #5; Success Criterion #7

#### Integration Points — Phase 4

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|----------------|------|-------------------|--------------|-------------|
| Audit logger | Logging middleware/service | All auth handlers → structured log emitter | Phase 4.1 | All auth endpoints (retroactive wiring into Phase 2–3 handlers) |
| Health check endpoint | HTTP handler | Database ping, service status | Phase 4.2 | Monitoring infrastructure |
| Feature flag rollout | Config service | `AUTH_SERVICE_ENABLED` → gradual enable | Phase 4.3 | Production deployment |

**Exit criteria**: All NFRs validated with evidence. Security review and penetration test completed with no critical findings. All 8 success criteria met. E2E tests green. Production deployment successful with feature flag rollout.

---

## 3. Risk Assessment and Mitigation

| # | Risk | Severity | Probability | Mitigation Strategy | Phase Addressed |
|---|------|----------|-------------|---------------------|-----------------|
| 1 | JWT private key compromise allows forged tokens | High | Low | RS256 asymmetric keys in secrets manager; 90-day key rotation; key access auditing | Phase 1.1 |
| 2 | Refresh token replay attack after theft | High | Medium | Token rotation with replay detection in Phase 3.1; suspicious reuse triggers full revocation (FR-AUTH.3c) | Phase 3.1 |
| 3 | bcrypt cost factor insufficient for future hardware | Medium | Low | Configurable cost factor; annual review against OWASP; Argon2id migration path documented | Phase 1.2 |
| 4 | Low registration adoption due to poor UX | High | Medium | Inline validation, < 60s target, usability testing pre-launch; post-launch funnel monitoring (Success Criterion #1) | Phase 2.1, Phase 4.3 |
| 5 | Security breach from implementation flaws | Critical | Low | Dedicated security review + penetration testing in Phase 4.3; no production deployment without sign-off | Phase 4.3 |
| 6 | Compliance failure from incomplete audit logging | High | Medium | Audit log requirements defined in Phase 4.1; validated against SOC2 controls; spec GAP-2 must be resolved before Phase 4 | Phase 4.1 |
| 7 | Email delivery failures blocking password reset | Medium | Low | Delivery monitoring + alerting in Phase 4.2; fallback support channel documented | Phase 3.3, Phase 4.2 |

**Architect's risk notes**:
- Risk #2 (replay attack) is the most architecturally significant risk. The rotation + replay detection pattern in FR-AUTH.3c is well-designed but must be implemented with database-level atomicity (compare-and-swap on token hash) to prevent race conditions under concurrent refresh requests.
- Risk #6 requires resolving Open Question #5 and spec GAP-2 before Phase 4 begins. If audit logging requirements remain undefined, Phase 4.1 cannot be completed.

---

## 4. Resource Requirements and Dependencies

### External Dependencies (must be resolved before development starts)

| # | Dependency | Required By Phase | Status | Action Required |
|---|-----------|-------------------|--------|-----------------|
| 1 | `jsonwebtoken` NPM package | Phase 1.2 | Available | Add to package.json |
| 2 | `bcrypt` NPM package | Phase 1.2 | Available | Add to package.json |
| 3 | Email delivery service (SendGrid) | Phase 3.3 | **Assumed available** | Confirm provisioning and API credentials |
| 4 | PostgreSQL 15+ | Phase 1.1 | **Assumed available** | Confirm provisioning and access |
| 5 | RSA key pair + secrets manager | Phase 1.1 | **Not provisioned** | DevOps must provision before Phase 1 starts |
| 6 | Frontend routing framework | Phase 2.1 | **Assumed available** | Confirm framework supports auth page routing |
| 7 | Security policy SEC-POLICY-001 | Phase 1.2 | **Unknown** | Security team must provide or confirm policy |

### Team Capabilities Required

- **Backend engineer(s)**: TypeScript, JWT, bcrypt, PostgreSQL, REST API design
- **Frontend engineer**: Auth forms, inline validation, token management (httpOnly cookies, silent refresh)
- **DevOps/Infrastructure**: PostgreSQL provisioning, secrets management, CI/CD, monitoring
- **Security reviewer**: Dedicated review in Phase 4 (can be external)
- **QA**: Integration testing, load testing (k6), E2E test authoring

---

## 5. Success Criteria and Validation Approach

| # | Criterion | Target | Validation Method | Phase Validated |
|---|-----------|--------|-------------------|-----------------|
| 1 | Registration conversion rate | > 60% | Post-launch funnel analytics (landing → confirmed account) | Post-launch (monitor) |
| 2 | Login endpoint response time (p95) | < 200ms | k6 load test in staging; APM in production | Phase 4.2 |
| 3 | Average session duration | > 30 minutes | Token refresh event analytics post-launch | Post-launch (monitor) |
| 4 | Failed login rate | < 5% of total attempts | Auth event log analysis post-launch | Post-launch (monitor) |
| 5 | Password reset completion rate | > 80% | Reset funnel analytics (requested → new password set) | Post-launch (monitor) |
| 6 | Service availability (rolling 30-day) | ≥ 99.9% | Health check monitoring + PagerDuty | Phase 4.2 (infra), post-launch (ongoing) |
| 7 | All tests passing | 100% pass rate | CI pipeline: unit + integration + E2E | Phase 4.3 (gate) |
| 8 | SOC2 audit log completeness | All auth events captured; 12-month retention | Log completeness audit; retention policy verification | Phase 4.1 |

**Pre-launch gates** (must pass before production): Criteria #2, #6, #7, #8.
**Post-launch monitoring** (measured after rollout): Criteria #1, #3, #4, #5.

---

## 6. Timeline Estimates

| Phase | Description | Sprints | Duration (2-week sprints) | Dependencies |
|-------|-------------|---------|---------------------------|--------------|
| **Phase 1** | Foundation & Infrastructure | 1–2 | 4 weeks | External: PostgreSQL, secrets manager, CI pipeline |
| **Phase 2** | Core Authentication | 2–3 | 3 weeks | Phase 1 complete; frontend framework available |
| **Phase 3** | Session Management & Recovery | 3–5 | 4 weeks | Phase 2 complete; email service provisioned |
| **Phase 4** | Compliance, Perf & Launch | 5–6 | 3 weeks | Phase 3 complete; security reviewer available |
| **Total** | | 1–6 | **~14 weeks** | |

**Note**: Phases 1–2 overlap in Sprint 2 (infrastructure completes while core auth begins on completed primitives). Phases 3–4 have a similar overlap in Sprint 5.

**Critical milestones**:
- **Week 4**: Infrastructure + security primitives ready (Phase 1 exit)
- **Week 7**: Registration + login functional (Phase 2 exit)
- **Week 11**: Full auth surface complete (Phase 3 exit)
- **Week 14**: Production-ready with compliance sign-off (Phase 4 exit)

**Target release**: End of Sprint 6, aligning with PRD target of Q2 2026.

---

## 7. Open Questions Requiring Resolution

The following open questions from the extraction must be resolved at the indicated phases. Unresolved questions will block the listed phase.

| # | Question | Blocks Phase | Recommended Resolution | Decision Owner |
|---|----------|--------------|------------------------|----------------|
| 1 | Sync vs. async email dispatch for password reset? | Phase 3.3 | Async (message queue) for resilience; sync acceptable if volume is low | Engineering |
| 2 | Max active refresh tokens per user? | Phase 3.1 | Cap at 5 (covers phone + laptop + tablet + 2 API clients); oldest revoked on overflow | Product |
| 3 | Account lockout policy after N failures? | Phase 2.2 | Progressive: 5 failures → 15-min lockout; 10 failures → 1-hour; 20 → admin unlock. Complements FR-AUTH.1d rate limiting | Security |
| 4 | "Remember me" extending session beyond 7 days? | Phase 3.1 | Defer to v1.1. 7-day refresh TTL is sufficient for v1.0 | Product |
| 5 | Audit logging field requirements (GAP-2)? | **Phase 4.1 (blocker)** | Adopt PRD specification: user_id, event_type, timestamp, IP, outcome. 12-month retention | Security/Compliance |
| 6 | Token revocation on account deletion? | Post-v1.0 | Account deletion not in v1.0 scope; document as v1.1 requirement | Architecture |
| 7 | GDPR consent — v1.0 hard requirement? | **Phase 2.1 (blocker)** | Yes — include in Phase 2.1. GDPR applies at data collection time; deferral creates compliance risk | Legal/Product |
| 8 | JTBD #2 work-state preservation? | Out of scope | Not an auth concern; separate feature. Auth provides session continuity only | Product |
| 9 | Admin audit log UI in v1.0? | Phase 4.1 | Out of v1.0. Logs queryable via database tooling; admin UI in v1.1 | Product/Engineering |
| 10 | Explicit logout endpoint? | **Phase 2.2** | Include in v1.0 — PRD user story exists, minimal implementation effort (revoke refresh token + clear cookie) | Product |

**Architect's recommendation**: Questions #5, #7, and #10 should be resolved immediately as they affect Phase 2 planning. Question #5 blocks Phase 4 but should be settled early to avoid rework.

---

## 8. Scope Guardrails

Per the PRD Scope Definition, the following are explicitly **out of scope** for this roadmap:

| Capability | Status | Notes |
|------------|--------|-------|
| OAuth2/OIDC federation | Out of scope | Planned v2.0 |
| Multi-factor authentication | Out of scope | Planned v1.1; requires SMS/TOTP infrastructure |
| Role-based access control | Out of scope | Separate PRD for authorization |
| Social login (Google, GitHub) | Out of scope | Depends on OAuth/OIDC |
| Admin UI for user management | Out of scope | Logs queryable via database; admin UI in v1.1 |
| Account deletion | Out of scope | v1.1; Open Question #6 |
| Work-state preservation | Out of scope | Separate feature; Open Question #8 |

Any request to add these capabilities during v1.0 development should be redirected to the appropriate future release PRD.
