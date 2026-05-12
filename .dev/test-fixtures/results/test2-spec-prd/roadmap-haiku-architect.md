---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
generated: "2026-04-02T00:00:00Z"
complexity_class: "MEDIUM"
domains: ["backend", "security", "frontend", "infrastructure", "compliance"]
functional_requirements: 5
nonfunctional_requirements: 7
total_requirements: 12
risks_identified: 7
dependencies_identified: 9
---

# User Authentication Service - Project Roadmap

## Executive Summary

The User Authentication Service is a **medium-complexity, security-critical feature** that unblocks the Q2-Q3 2026 personalization roadmap and enables SOC2 Type II compliance. The service introduces user registration, login, session persistence, profile retrieval, and self-service password recovery—foundational identity capabilities required by every downstream personalization feature.

**Strategic Priority**: Highest — $2.4M in projected annual revenue from personalization-dependent features depends on authentication shipping in Q2.

**Compliance Constraint**: SOC2 Type II audit is scheduled Q3 2026. Audit logging (NFR-AUTH.5) is required but the specification defers it to v1.1. **This is a material conflict** that must be resolved in the discovery phase; SOC2 compliance timeline likely forces audit logging into Phase 2 scope.

**Technical Risk Posture**: High. Authentication touches cryptographic operations (JWT signing, password hashing), token lifecycle management (rotation, revocation, replay detection), and compliance-critical audit logging. Implementation errors in these areas directly compromise user security and regulatory standing.

**Timeline Estimate**: 7-10 weeks across 2 phases (4 weeks Phase 1, 3 weeks Phase 2).

---

## Phased Implementation Plan

### Phase 1: Authentication Core (Weeks 1-4)

**Objective**: Deliver login, registration, token management, and profile retrieval — the minimum viable authentication layer.

**Business Value**: Unblocks personalization feature development and establishes identity foundation.

**Functional Scope**:
- FR-AUTH.1: User Login (email/password → access + refresh tokens)
- FR-AUTH.2: User Registration (account creation with validation)
- FR-AUTH.3: Token Refresh (refresh token → new access token)
- FR-AUTH.4: Profile Retrieval (authenticated user profile access)

**Non-Functional Scope**:
- NFR-AUTH.1: Login response time < 200ms (p95)
- NFR-AUTH.3: Password hashing with bcrypt cost factor 12
- NFR-AUTH.6: NIST-compliant password storage (no plaintext)

#### Phase 1 Milestones

**Week 1: Infrastructure & Schema**
- Database schema design and migration generation:
  - `users` table: id, email (unique), password_hash, display_name, created_at, updated_at
  - `refresh_tokens` table: id, user_id, token_hash, expires_at, revoked_at, created_at
  - Index on `users.email` (fast lookup for login), index on `refresh_tokens.user_id` + `expires_at` (efficient revocation queries)
- RSA key pair (RS256) provisioned in secrets manager
- Database migration 003 created and validated in staging environment

**Week 2: Core Service Implementation**
- JWT service (token generation and verification via `jsonwebtoken` + RS256 keys)
- Password hasher (bcrypt cost factor 12, ~250ms per hash per NFR-AUTH.3)
- Token manager (token issuance, expiration enforcement, refresh token rotation)
- Auth service (orchestrates login, registration, token refresh logic)
- User repository (database access layer with prepared statements to prevent SQL injection)

**Week 3: API & Middleware**
- Auth middleware (Bearer token extraction, validation, context injection into request)
- Auth controller with endpoints:
  - `POST /auth/register` — FR-AUTH.2 (registration with inline validation)
  - `POST /auth/login` — FR-AUTH.1 (login with rate limiting 5/min/IP)
  - `POST /auth/refresh` — FR-AUTH.3 (refresh token exchange)
  - `GET /auth/profile` — FR-AUTH.4 (authenticated profile retrieval)
  - `POST /auth/logout` — Log out (implied by PRD user story AUTH-E1 logout; spec gap OQ8)
- Route registration in main route index

**Week 4: Testing & Security Hardening**
- Unit tests: password hashing, JWT signing/verification, token rotation
- Integration tests: full login/register/refresh flows
- Security tests:
  - Invalid credentials do not reveal whether email or password was wrong (prevents enumeration)
  - Expired tokens return 401 without revealing token state
  - Locked accounts return 403 (address OQ3 account lockout policy with engineering)
- Performance testing with k6 (validate NFR-AUTH.1 < 200ms p95 on login endpoint)
- Security code review focused on cryptographic operations and token handling

**Phase 1 Exit Gate**:
- All FR-AUTH.1, FR-AUTH.2, FR-AUTH.3, FR-AUTH.4 acceptance criteria pass
- NFR-AUTH.1 (< 200ms p95) verified under load
- NFR-AUTH.3 (bcrypt cost 12) verified in unit tests
- NFR-AUTH.6 (no plaintext passwords) verified via code audit
- Security review clearance obtained

---

### Phase 2: Recovery, Compliance & Hardening (Weeks 5-7)

**Objective**: Deliver password reset, compliance baselines (GDPR consent, audit logging), and token rotation hardening.

**Business Value**: Enables self-service account recovery (reduces support burden), establishes SOC2 compliance foundation, and hardens token security against replay attacks.

**Functional Scope**:
- FR-AUTH.5: Password Reset (email-driven recovery flow)

**Non-Functional Scope**:
- NFR-AUTH.2: 99.9% availability (infrastructure & monitoring)
- NFR-AUTH.4: GDPR consent at registration
- NFR-AUTH.5: SOC2 audit logging (per PRD compliance deadline Q3 2026)
- NFR-AUTH.7: GDPR data minimization (schema audit)

**Architecture Consideration**: **OQ6 Conflict Resolution**. The specification defers audit logging to v1.1, but the PRD requires SOC2 audit logging with Q3 2026 deadline. This roadmap **includes audit logging in Phase 2** based on the PRD compliance driver. The product team and engineering lead must confirm this scope decision in the discovery phase kickoff.

#### Phase 2 Milestones

**Week 5: Password Reset & Email Integration**
- Password reset token generation and storage (1-hour TTL, one-time use)
- Password reset controller:
  - `POST /auth/forgot-password` — Request reset token via email
  - `POST /auth/reset-password` — Consume reset token and set new password
- Email service integration (SendGrid):
  - Template for password reset link (includes 1-hour TTL token)
  - Delivery monitoring and retry logic
- **Email Flow Decision (OQ1)**: Resolve whether password reset emails are sent synchronously or asynchronously
  - Recommend: Asynchronous (message queue) for latency and resilience
  - Task: Add email job queue (Redis-backed or similar) to infrastructure
- Session invalidation on successful password reset (all user tokens revoked)

**Week 6: Compliance & Audit Logging**
- Audit logging schema design:
  - `auth_events` table: id, user_id, event_type (login, register, logout, token_refresh, password_reset, account_locked), timestamp, ip_address, user_agent, outcome (success/failure), error_code
  - 12-month retention policy via TTL or archival job
  - Index on (user_id, timestamp) for SOC2 audit queries
- Event emission integration:
  - Login success/failure → log
  - Registration success/failure → log
  - Token refresh → log
  - Password reset requested/completed → log
  - Logout → log
  - Account lock/unlock (future, OQ3) → log
- GDPR consent mechanism at registration:
  - Add `consent_to_data_collection` boolean flag to users table (with timestamp)
  - Registration form includes explicit consent checkbox
  - Consent recorded at account creation time
- Data minimization audit:
  - Verify users table contains only: id, email, password_hash, display_name, consent_timestamp, created_at, updated_at
  - Document that no extraneous PII is collected

**Week 7: Security Hardening & Monitoring**
- Refresh token replay detection hardening:
  - On refresh token use, check if token was previously rotated (in revocation log)
  - If token is replayed (used after rotation), revoke all user tokens (FR-AUTH.3c)
- Account lockout policy definition (OQ3):
  - After 5 consecutive failed login attempts, lock account for 15 minutes
  - Log account lock event
  - Admin unlock capability (Jordan persona)
- Rate limiting enforcement:
  - 5 login attempts per minute per IP (FR-AUTH.1d)
  - 10 password reset requests per hour per email (prevent email bombing)
- Monitoring and alerting:
  - Alert on excessive failed login attempts (> 20/minute)
  - Alert on unusual refresh token reuse patterns (potential breach)
  - APM dashboard for auth endpoint latency and error rates
- Health check endpoint for availability monitoring (NFR-AUTH.2)

**Phase 2 Exit Gate**:
- All FR-AUTH.5 acceptance criteria pass
- NFR-AUTH.2 (99.9% availability) infrastructure in place and monitored
- NFR-AUTH.4 (GDPR consent) recorded at registration
- NFR-AUTH.5 (SOC2 audit logging) complete with 12-month retention
- NFR-AUTH.7 (data minimization) verified via schema audit
- Security code review clearance obtained
- Penetration testing for password reset flow, token replay detection completed
- SOC2 audit log requirements validated against SAC 2 control objectives (CC6.1, CC7.2, etc.)

---

## Architectural Components & Integration Points

### Component Dependency Graph

```
Request → Auth Middleware → Auth Service → {Token Manager, Password Hasher, User Repository}
                                        → {JWT Service (RS256)}
                                        → {Email Service} [Phase 2]
                                        → {Audit Logger} [Phase 2]
```

### Named Artifacts & Wiring

| Artifact | Type | Components Wired | Owning Phase | Consumed By |
|----------|------|------------------|-------------|------------|
| **Auth Middleware** | Middleware chain | JWT verifier, bearer token extractor | Phase 1 | All protected endpoints (Phase 1-2) |
| **Auth Service Dependency Injection** | DI container | TokenManager, PasswordHasher, JwtService, UserRepository, EmailService | Phase 1 (core), Phase 2 (email) | Auth controller (Phase 1-2) |
| **Route Registry** | Route table | AuthController methods (register, login, logout, refresh, getProfile, forgotPassword, resetPassword) | Phase 1 (core 6 routes), Phase 2 (+2 reset routes) | HTTP routing layer (Phase 1-2) |
| **Password Hasher Strategy** | Strategy pattern | Bcrypt hasher (cost 12) | Phase 1 | Auth service for registration/password reset (Phase 1-2) |
| **Token Rotation Mechanism** | State machine | RefreshToken table, revocation tracker | Phase 1 (basic rotation), Phase 2 (replay detection hardening) | Token refresh endpoint (Phase 1-2) |
| **Email Event Dispatcher** | Event emitter | EmailService (SendGrid), template engine | Phase 2 | Password reset flow (Phase 2 only) |
| **Audit Logger** | Logger | AuthEvent table, timestamp/IP/outcome capture | Phase 2 | All auth endpoints (Phase 2 logging) |
| **Account Lock Registry** | State machine | Failed login counter, lock expiration timestamp | Phase 2 | Login endpoint (Phase 2 hardening) |

**Critical Wiring Decision (Phase 1/2 Boundary)**:
- The password hasher and token manager must be wired into the auth service in Phase 1 and remain stable through Phase 2 (no breaking changes).
- Email service wiring is deferred to Phase 2 (password reset). Auth service must support dependency injection of EmailService to avoid coupling in Phase 1.
- Audit logger wiring is deferred to Phase 2. All auth endpoints must support audit event emission but logging can be conditional (no-op in Phase 1, active in Phase 2).

---

## Risk Assessment & Mitigation Strategy

| Risk ID | Risk | Severity | Phase | Mitigation Strategy | Success Indicator |
|---------|------|----------|-------|-------------------|-------------------|
| **R1** | JWT private key compromise allows forged tokens | High | All | (1) Store RS256 private key in secrets manager (not in code/env files). (2) Enable key rotation: quarterly key generation, 30-day overlap window, old key deprecated. (3) Monitor for unauthorized token signing (anomaly detection on token issue rate). (4) Pre-production: AWS Secrets Manager or HashiCorp Vault. Production: dedicated HSM or KMS. | Private key never appears in code, logs, or CI/CD. Key rotation tested quarterly. |
| **R2** | Refresh token replay attack after theft | High | Phase 1-2 | (1) Implement refresh token rotation on every use (FR-AUTH.3c). (2) Hash refresh tokens before storage (like passwords). (3) Track issued token hashes; detect re-use of rotated token. (4) On replay detection, revoke all user tokens immediately. (5) Phase 2 hardening: add refresh token rotation history table for forensics. | Replay detection test: stolen token cannot be re-used. Audit log shows token revocation. |
| **R3** | bcrypt cost factor insufficient for future hardware | Medium | Phase 1-2 | (1) Cost factor configurable via environment variable (currently 12, minimum). (2) Annual OWASP review of recommended cost factor. (3) Define Argon2id migration path for v1.1 (faster to implement than bcrypt upgrade). (4) Monitor bcrypt benchmarks; alert if hash time < 100ms (indicates weak hardware or cost misconfiguration). | Bcrypt cost verified in unit tests. Migration path documented. |
| **R4** | Low registration adoption due to poor UX | High | Phase 1-2 | (1) Registration form testing with 5+ users per persona (Alex, Sam). (2) Inline validation with real-time error feedback (password policy, email format). (3) A/B test: single-step vs. multi-step registration. (4) Success metric: > 60% registration conversion rate (PRD target). (5) If < 50% at week 3 Phase 1, iterate form design before go-live. | Conversion funnel metrics tracked daily. A/B test results analyzed. |
| **R5** | Security breach from implementation flaws | High | Phase 1-2 | (1) **Phase 1 security review**: Dedicated code review for JWT signing, password hashing, token storage. (2) **Penetration testing** pre-production: Test for XSS via token exfiltration, SQL injection in auth queries, token enumeration. (3) **OWASP Top 10 checklist** at exit gate for each phase. (4) **Threat modeling session** with security architect at Phase 1 kickoff. | Security review clearance. Penetration test zero critical findings. |
| **R6** | Compliance failure from incomplete audit logging | High | Phase 2 | (1) **Early definition**: Define SOC2 control mappings (CC6.1 = login audit events, CC7.2 = logout events). (2) **Audit schema review** by compliance team before Phase 2 dev. (3) **Validation at Phase 2 exit**: Compliance audit of log schema against SAC 2 control objectives. (4) **Retention enforcement**: Database TTL or archival job ensures 12-month minimum. (5) **Queryability test**: Verify audit logs are queryable by date/user/event type. | Audit log schema approved by compliance. Phase 2 QA validates completeness. |
| **R7** | Email delivery failures blocking password reset | Medium | Phase 2 | (1) **Email service monitoring**: SendGrid delivery status tracking. Alert on bounce/delay rates > 5%. (2) **Fallback channel**: If email fails, send in-app notification or SMS code (future). (3) **Delivery SLA**: SendGrid guarantees 99.9% delivery; configure retry logic for transient failures. (4) **Queue-based delivery** (async): Use message queue (Redis) to decouple password reset endpoint from email delivery latency. (5) **Support runbook**: Manual reset process for users with persistent delivery issues. | Email delivery rate > 95%. Reset email sent within 60 seconds. Support runbook documented. |

---

## Resource Requirements & Dependencies

### Team Composition

| Role | Headcount | Expertise | Responsibilities |
|------|-----------|-----------|------------------|
| **Backend Engineer** | 1.5 FTE | Node.js/TypeScript, async patterns, databases | Implement auth service, token manager, password hasher, database migrations |
| **Security Engineer** | 0.5 FTE | Cryptography, OAuth/JWT, OWASP Top 10 | Security code review, threat modeling, penetration testing, SOC2 mapping |
| **Database Engineer** | 0.5 FTE | PostgreSQL, schema design, migration management | User & refresh_token schema design, migration creation, indexing strategy |
| **Frontend Engineer** | 1.0 FTE | React, form validation, UX | Registration, login, password reset UI; inline validation; token lifecycle on client |
| **QA Engineer** | 1.0 FTE | API testing, load testing (k6), security testing | Integration test coverage, performance testing, compliance validation |
| **Product Manager** | 0.5 FTE | Requirements, prioritization, persona alignment | Open question resolution (OQ1-8), scope confirmation, success metrics tracking |

**Total Effort**: 4.5 FTE for 7-10 weeks = ~180-200 engineer-days.

### External Dependencies

| Dependency | Type | Required By | Status | Resolution Timeline |
|-----------|------|-----------|--------|-------------------|
| **SendGrid (Email Service)** | External SaaS | FR-AUTH.5 (Phase 2) | Must provision before Phase 2 week 5 | Provision in week 3 Phase 1; allow 2 weeks for API integration & testing |
| **PostgreSQL 15+** | Infrastructure | User & RefreshToken tables | Assume available; verify in discovery | Verify in discovery kickoff; if not available, provision immediately |
| **RS256 Key Pair** | Cryptographic asset | JWT service | Generate during Phase 1 week 1 | Use OpenSSL: `openssl genrsa -out private.pem 4096` → secrets manager |
| **Frontend Routing Framework** | Internal | Auth page rendering | Assume available | Confirm in discovery with frontend team |
| **Message Queue (Redis)** | Infrastructure | Email delivery (async, Phase 2) | Optional for Phase 1; recommended for Phase 2 | Provision in Phase 2 week 5 if OQ1 resolves to async email |
| **APM/Monitoring Tool** | Infrastructure | NFR-AUTH.1, NFR-AUTH.2 | Phase 1 (planning), Phase 2 (implementation) | Confirm existing tool (e.g., Datadog, New Relic); integrate auth endpoints in Phase 2 |
| **Compliance Policy (SEC-POLICY-001)** | Policy document | Password/token policy definitions | Referenced but may be incomplete | Confirm password policy (min 8 chars, 1 upper/lower/digit) and token TTLs (15m access, 7d refresh) in discovery |

### Infrastructure Assumptions

1. **PostgreSQL 15+** provisioned and accessible to engineering team
2. **Secrets manager** (AWS Secrets Manager, HashiCorp Vault) for RS256 private key storage
3. **SendGrid account** with API key access (Phase 2)
4. **Staging environment** for pre-production security testing
5. **APM/logging platform** for production monitoring

---

## Open Questions Requiring Resolution

**All open questions must be resolved before Phase kickoff to prevent mid-phase scope creep.**

| ID | Question | Impact | Recommendation | Owner | Target Resolution |
|----|----------|--------|-----------------|-------|-------------------|
| **OQ1** | Async or sync email for password reset? | Endpoint latency, infrastructure complexity | Recommend: **Async** (message queue) for latency and resilience. Sync acceptable if < 1% password reset requests. Decide in discovery. | Engineering + Product | Week 1 of project |
| **OQ2** | Max refresh tokens per user? | Storage, multi-device UX, security posture | Recommend: **Unlimited** with per-device rotation. Simplifies UX, enables JTBD #2 (multi-device session persistence). | Product | Week 1 of project |
| **OQ3** | Account lockout policy after N failed attempts? | Security hardening, user experience | Recommend: **5 consecutive failures → 15-minute lock**. Log lock event for SOC2. Matches industry standard. | Security + Product | Week 1 of project |
| **OQ4** | "Remember me" to extend session beyond 7 days? | Refresh token TTL, UX for returning users | Recommend: **Out of scope for v1.0**. Implement in v1.1. Complexity increases token management; JTBD #2 covered by multi-device refresh. | Product | Week 1 of project |
| **OQ5** | Token revocation on user deletion? | Data consistency, orphaned tokens | Recommend: **Delete all refresh tokens on user account deletion**. Verify cascade delete in migration. | Engineering + Security | Phase 1 schema design |
| **OQ6** | **Audit logging scope — v1.0 or v1.1?** | **COMPLIANCE CONFLICT** — SOC2 Q3 2026 deadline | **Recommend: Phase 2 (v1.0)**. PRD requires SOC2 audit logging. Spec defers to v1.1. Spec is wrong. Audit logging MUST be in Phase 2 scope. | Product + Engineering | **Immediate — blocks roadmap approval** |
| **OQ7** | GDPR consent mechanism? | Compliance, registration UX | Recommend: **Explicit checkbox** at registration: "I consent to data collection per our privacy policy." Record timestamp. | Product + Legal | Week 1 of project |
| **OQ8** | Logout endpoint — in scope? | User persona (Alex), PRD user story AUTH-E1 | **Recommend: Phase 1 scope**. PRD includes logout user story. Spec gap OQ8 requires resolution. Add `POST /auth/logout` endpoint (invalidates token client-side; optional server-side tracking). | Product + Engineering | Week 1 of project |

**Critical**: OQ6 (audit logging scope) must be resolved immediately. If audit logging is deferred to v1.1, this roadmap is invalid and the product does not meet SOC2 Q3 2026 deadline.

---

## Success Criteria & Validation Approach

### Measurable Success Thresholds

| Criterion | Target | Measurement Method | Validation Phase | Owner |
|-----------|--------|-------------------|------------------|-------|
| **SC1: Registration Conversion Rate** | > 60% | Funnel analytics: landing → register form → account confirmed | Phase 2 QA + Product | Product Manager |
| **SC2: Login Response Time (p95)** | < 200ms | k6 load test (500 concurrent users); production APM on `/auth/login` | Phase 1 QA + Phase 2 Monitoring | QA Engineer |
| **SC3: Average Session Duration** | > 30 minutes | Token refresh event analytics; requires frontend instrumentation | Post-launch (Week 1) | Product Manager |
| **SC4: Failed Login Rate** | < 5% of total attempts | Audit log analysis: failed login / total login attempts | Post-launch (Week 1) | Product Manager |
| **SC5: Password Reset Completion Rate** | > 80% | Funnel analytics: reset requested → new password set | Phase 2 QA + Post-launch | Product Manager |
| **SC6: Service Availability (99.9% uptime)** | < 8.76 hrs downtime/year | Health check endpoint monitoring; rolling 30-day windows | Phase 2 Monitoring (ongoing) | SRE/DevOps |

### Validation Gates Per Phase

**Phase 1 Exit Gate** (Week 4):
- ✓ All FR-AUTH.1, FR-AUTH.2, FR-AUTH.3, FR-AUTH.4 acceptance criteria pass (integration tests)
- ✓ NFR-AUTH.1 verified: login endpoint < 200ms p95 under 500 concurrent load (k6)
- ✓ NFR-AUTH.3 verified: bcrypt cost factor 12 confirmed in unit tests (~250ms hash time)
- ✓ NFR-AUTH.6 verified: code audit confirms no plaintext password storage or logging
- ✓ Security review clearance: no critical/high findings on JWT signing, token handling, SQL injection vectors
- ✓ Registration UX testing: > 60% target conversion funnel passes (5+ user tests)
- ✓ All open questions (OQ1-8) resolved; scope confirmed with product

**Phase 2 Exit Gate** (Week 7):
- ✓ All FR-AUTH.5 acceptance criteria pass (password reset flow)
- ✓ NFR-AUTH.2 infrastructure in place: health check endpoint configured; 99.9% availability monitoring active
- ✓ NFR-AUTH.4 verified: GDPR consent checkbox recorded at registration with timestamp
- ✓ NFR-AUTH.5 complete: audit log schema approved; 12-month retention configured; SOC2 control mappings verified
- ✓ NFR-AUTH.7 verified: schema audit confirms only email, password_hash, display_name collected
- ✓ Security review clearance: penetration testing zero critical findings on password reset, token replay detection
- ✓ Email delivery monitoring active: SendGrid integration delivering > 95% of reset emails within 60 seconds
- ✓ Compliance validation: audit log requirements signed off by compliance team against SAC 2 objectives
- ✓ Performance testing: password reset endpoint < 500ms (p95)

---

## Risk Priorities for Architecture Review

From an architect's perspective, the following risks require **upfront architectural decisions** before Phase 1 coding begins:

1. **R1 (JWT Key Compromise)** → Secrets manager integration, key rotation strategy
2. **R2 (Token Replay)** → Refresh token rotation state machine, revocation tracking design
3. **R5 (Security Breach)** → Threat modeling session, OWASP checklist, secure coding guidelines
4. **R6 (Compliance Failure)** → SOC2 control mapping, audit log schema review, retention design

These should be addressed in a **Security & Compliance Architecture Review** during week 1 of Phase 1 (before coding starts).

---

## Timeline Summary

| Phase | Duration | Effort | Key Milestone | Business Value | Exit Criteria |
|-------|----------|--------|---------------|-----------------|---------------|
| **Phase 1** | 4 weeks | ~120 engineer-days | Working login + registration + session refresh | Unblocks personalization dev | All FR-AUTH.1-4 + NFR-AUTH.1,3,6 + security review clearance |
| **Phase 2** | 3 weeks | ~80 engineer-days | Password reset + audit logging + compliance | Self-service recovery + SOC2 readiness | All FR-AUTH.5 + NFR-AUTH.2,4,5,7 + penetration test clearance |
| **Buffer** | 2-3 weeks | Contingency | Risk mitigation, OQ resolution, regression testing | Risk absorption | Allows 20-30% slip without missing Q2 deadline |
| **Total** | 7-10 weeks | ~200 engineer-days | Production-ready v1.0 | Full feature complete | Go/no-go decision week 10 |

**Go-Live Target**: End of Q2 2026 (by June 30). If 10-week estimate holds, development complete by May 30, leaving 4 weeks for hardening, load testing, and production validation.

---

## Conclusion

The User Authentication Service is a **well-scoped, medium-complexity feature** with clear functional and non-functional requirements. However, **three architectural and scope conflicts require immediate resolution**:

1. **OQ6 (Audit Logging Scope)**: PRD requires SOC2 compliance with Q3 2026 deadline. Specification defers audit logging to v1.1. This roadmap assumes **Phase 2 scope** based on the PRD compliance driver. **Product and engineering must confirm this in discovery kickoff.**

2. **OQ3 (Account Lockout)**: Specification defines rate limiting (5/min/IP) but does not define progressive account lockout. This roadmap recommends 5-failure → 15-minute lock in Phase 2 hardening.

3. **OQ8 (Logout)**: PRD includes logout user story; specification does not define FR for logout. This roadmap includes logout endpoint in Phase 1 scope.

**Success hinges on cryptographic security** (JWT keys, token rotation, password hashing) and **compliance completeness** (audit logging, GDPR consent, NIST password storage). Allocate security review resources early and validate compliance requirements before Phase 2 coding begins.

The 7-10 week timeline is realistic given the team composition and open question resolution. Risk absorption (2-3 week buffer) is critical given the security-critical nature of authentication and the compliance deadline pressure.
