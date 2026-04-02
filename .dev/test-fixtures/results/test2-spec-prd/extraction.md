---
spec_source: "test-spec-user-auth.md"
generated: "2026-03-31T00:00:00Z"
generator: "requirements-extraction-agent"
functional_requirements: 5
nonfunctional_requirements: 7
total_requirements: 12
complexity_score: 0.6
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, infrastructure]
risks_identified: 7
dependencies_identified: 7
success_criteria_count: 8
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 103.4, started_at: "2026-03-31T13:46:49.044262+00:00", finished_at: "2026-03-31T13:48:32.412229+00:00"}
---

## Functional Requirements

### FR-AUTH.1: User Login

**Description**: Authenticate users via email and password, returning JWT access token and refresh token upon successful credential verification.

**Acceptance Criteria**:
- **FR-AUTH.1a**: Valid email and password returns 200 with access_token (15min TTL) and refresh_token (7d TTL)
- **FR-AUTH.1b**: Invalid credentials return 401 without revealing whether email or password was incorrect
- **FR-AUTH.1c**: Locked account returns 403 indicating account suspension
- **FR-AUTH.1d**: Rate-limit login attempts to 5 per minute per IP address

**Dependencies**: PasswordHasher, TokenManager, User database table
**Trace**: Spec §3 FR-AUTH.1; PRD FR-AUTH.1; PRD User Story AUTH-E1 (login)

---

### FR-AUTH.2: User Registration

**Description**: Register new users with input validation, creating a user record with securely hashed password and returning confirmation.

**Acceptance Criteria**:
- **FR-AUTH.2a**: Valid registration data (email, password, display name) creates user record and returns 201 with user profile
- **FR-AUTH.2b**: Already-registered email returns 409 conflict
- **FR-AUTH.2c**: Password policy enforced: minimum 8 characters, at least one uppercase, one lowercase, one digit
- **FR-AUTH.2d**: Email format validated before attempting registration

**Dependencies**: PasswordHasher, User database table
**Trace**: Spec §3 FR-AUTH.2; PRD FR-AUTH.2; PRD User Story AUTH-E1 (registration)

---

### FR-AUTH.3: Token Refresh

**Description**: Issue and refresh JWT tokens, allowing clients to obtain new access tokens using valid refresh tokens without re-entering credentials.

**Acceptance Criteria**:
- **FR-AUTH.3a**: Valid refresh token returns new access_token and rotated refresh_token
- **FR-AUTH.3b**: Expired refresh token returns 401, requiring re-authentication
- **FR-AUTH.3c**: Previously-rotated (revoked) refresh token triggers invalidation of all tokens for that user (replay detection)
- **FR-AUTH.3d**: Refresh token hashes stored in database for revocation support

**Dependencies**: TokenManager, JwtService, RefreshToken database table
**Trace**: Spec §3 FR-AUTH.3; PRD FR-AUTH.3; PRD User Story AUTH-E2 (token refresh)

---

### FR-AUTH.4: Profile Retrieval

**Description**: Provide authenticated user profile retrieval, returning current user's profile data when presented with a valid access token.

**Acceptance Criteria**:
- **FR-AUTH.4a**: Valid Bearer access_token returns user profile (id, email, display_name, created_at)
- **FR-AUTH.4b**: Expired or invalid token returns 401
- **FR-AUTH.4c**: Sensitive fields (password_hash, refresh_token_hash) never included in profile response

**Dependencies**: TokenManager, User database table
**Trace**: Spec §3 FR-AUTH.4; PRD FR-AUTH.4; PRD User Story AUTH-E3 (profile)

---

### FR-AUTH.5: Password Reset

**Description**: Support secure password reset flow allowing users to request a reset link and set a new password using a time-limited token.

**Acceptance Criteria**:
- **FR-AUTH.5a**: Registered email triggers generation of password reset token (1-hour TTL) and dispatch of reset email
- **FR-AUTH.5b**: Valid reset token allows setting a new password and invalidates the reset token
- **FR-AUTH.5c**: Expired or invalid reset token returns 400 with appropriate error message
- **FR-AUTH.5d**: All existing sessions (refresh tokens) invalidated upon successful password reset

**Dependencies**: TokenManager, PasswordHasher, Email service (external)
**Trace**: Spec §3 FR-AUTH.5; PRD FR-AUTH.5; PRD User Story AUTH-E3 (password reset)

---

## Non-Functional Requirements

### NFR-AUTH.1: Authentication Endpoint Response Time

**Requirement**: Authentication endpoint response time < 200ms p95 under normal load. Must sustain 500 concurrent requests (PRD enrichment).
**Measurement**: Load testing with k6; monitor p95 latency in production APM.
**Trace**: Spec §6 NFR-AUTH.1; PRD NFR-AUTH.1

---

### NFR-AUTH.2: Service Availability

**Requirement**: 99.9% uptime (< 8.76 hours downtime/year) over rolling 30-day windows.
**Measurement**: Uptime monitoring via health check endpoint; PagerDuty alerting.
**Trace**: Spec §6 NFR-AUTH.2; PRD NFR-AUTH.2

---

### NFR-AUTH.3: Password Hashing Security

**Requirement**: bcrypt cost factor 12 (approx. 250ms per hash). Passwords never stored or logged in plain text.
**Measurement**: Unit test verifying cost factor; benchmark test for hash timing.
**Trace**: Spec §6 NFR-AUTH.3; PRD NFR-AUTH.3

---

### NFR-AUTH.4: GDPR Consent at Registration
*(Surfaced from PRD Legal & Compliance section)*

**Requirement**: Users must consent to data collection at registration. Consent recorded with timestamp.
**Standard**: GDPR
**Measurement**: Registration flow audit; consent records queryable in database.
**Trace**: PRD §Legal & Compliance (GDPR consent)

---

### NFR-AUTH.5: SOC2 Audit Logging

*(Surfaced from PRD Legal & Compliance section)*

**Requirement**: All authentication events logged with user ID, timestamp, IP address, and outcome. 12-month retention minimum.
**Standard**: SOC2 Type II
**Measurement**: Log completeness audit; retention policy verification.
**Trace**: PRD §Legal & Compliance (SOC2); also related to Spec GAP-2

---

### NFR-AUTH.6: Data Minimization

*(Surfaced from PRD Legal & Compliance section)*

**Requirement**: Only email, hashed password, and display name collected at registration. No additional PII required.
**Standard**: GDPR
**Measurement**: Schema review; data flow audit.
**Trace**: PRD §Legal & Compliance (GDPR data minimization)

---

### NFR-AUTH.7: NIST Password Compliance

*(Surfaced from PRD Legal & Compliance section)*

**Requirement**: Password storage must use one-way adaptive hashing per NIST SP 800-63B. Raw passwords never persisted or logged.
**Standard**: NIST SP 800-63B
**Measurement**: Security review of hashing implementation; log audit for password leakage.
**Trace**: PRD §Legal & Compliance (NIST SP 800-63B); reinforces Spec NFR-AUTH.3

---

## Complexity Assessment

**Score**: 0.6 / 1.0
**Class**: MEDIUM

**Scoring Rationale**:

| Factor | Score | Rationale |
|--------|-------|-----------|
| Number of components | 0.5 | 4 new files, 3 modified files — moderate scope |
| Security sensitivity | 0.8 | Authentication is security-critical; JWT, bcrypt, token rotation all require careful implementation |
| External integrations | 0.4 | Single external dependency (email service); database is standard |
| Data model complexity | 0.5 | 2 new tables (users, refresh_tokens) with straightforward schemas |
| Concurrency/state management | 0.7 | Refresh token rotation with replay detection introduces stateful complexity |
| API surface area | 0.5 | 5 endpoints with well-defined contracts |
| Test coverage requirements | 0.6 | Unit, integration, and E2E tests required across all flows |

**Aggregate**: Weighted average yields 0.6. The security sensitivity and token rotation logic elevate complexity above trivial CRUD, but the well-defined scope and lack of external federation (OAuth/OIDC deferred) keep it in MEDIUM range.

---

## Architectural Constraints

1. **Token format**: JWT with RS256 asymmetric signing. No opaque tokens or PASETO.
2. **Password hashing**: bcrypt with configurable cost factor (default 12). Migration path to Argon2id noted but not required for v1.0.
3. **Token storage strategy**: Access token in memory (client-side), refresh token in httpOnly cookie. No localStorage or sessionStorage for tokens.
4. **Session model**: Stateless JWT with refresh rotation. No server-side session store.
5. **Implementation language**: TypeScript (inferred from `.ts` file extensions in spec §4.1).
6. **Database**: PostgreSQL 15+ (PRD dependency).
7. **Layered architecture**: AuthService → TokenManager → JwtService; PasswordHasher is a parallel utility. All components injectable and independently testable.
8. **Scope boundary**: Email/password only. No OAuth2/OIDC, MFA, RBAC, or social login in v1.0.
9. **Feature flag**: `AUTH_SERVICE_ENABLED` controls routing for rollback capability.
10. **Migration support**: Database migrations must include down-migration scripts.

**Persona-driven design requirements** *(from PRD §User Personas)*:
- **Alex (End User)**: Registration must complete in < 60 seconds. Inline validation on forms. No user enumeration in error messages.
- **Jordan (Platform Admin)**: Auth event logs must be queryable by date range and user. Account lock/unlock capability needed (partially out of v1.0 scope per spec).
- **Sam (API Consumer)**: Programmatic token refresh without user interaction. Clear, standardized error codes.

---

## Risk Inventory

| # | Risk | Severity | Probability | Mitigation |
|---|------|----------|-------------|------------|
| 1 | JWT private key compromise allows forged tokens | High | Low | Use RS256 asymmetric keys; store private key in secrets manager; implement key rotation every 90 days |
| 2 | Refresh token replay attack after token theft | High | Medium | Refresh token rotation with replay detection; revoke all user tokens on suspicious reuse |
| 3 | bcrypt cost factor insufficient for future hardware | Medium | Low | Make cost factor configurable; review annually against OWASP recommendations; migration path to Argon2id |
| 4 | Low registration adoption due to poor UX | High | Medium | Usability testing before launch; iterate based on funnel data (PRD) |
| 5 | Security breach from implementation flaws | Critical | Low | Dedicated security review; penetration testing before production (PRD) |
| 6 | Compliance failure from incomplete audit logging | High | Medium | Define log requirements early; validate against SOC2 controls in QA (PRD). Note: spec GAP-2 flags this as unspecified |
| 7 | Email delivery failures blocking password reset | Medium | Low | Delivery monitoring and alerting; fallback support channel (PRD) |

---

## Dependency Inventory

| # | Dependency | Type | Required By | Impact if Unavailable |
|---|-----------|------|-------------|----------------------|
| 1 | `jsonwebtoken` library | NPM package | JwtService (jwt-service.ts) | Cannot sign or verify JWT tokens |
| 2 | `bcrypt` library | NPM package | PasswordHasher (password-hasher.ts) | Cannot hash or verify passwords |
| 3 | Email delivery service (SendGrid or equivalent) | External service | FR-AUTH.5 (password reset) | Password reset flow completely blocked |
| 4 | PostgreSQL 15+ | Infrastructure | All FRs (user + refresh_token tables) | No persistent storage for auth data |
| 5 | RSA key pair + secrets manager | Infrastructure | JwtService (RS256 signing) | Cannot issue or verify tokens |
| 6 | Frontend routing framework | Internal | Auth pages (login, register, reset) | Auth UI cannot render |
| 7 | Security policy (SEC-POLICY-001) | Policy document | Password and token policy definitions | Policy compliance unverifiable |

---

## Success Criteria

| # | Criterion | Target | Source |
|---|-----------|--------|--------|
| 1 | Registration conversion rate (landing → confirmed account) | > 60% | PRD Success Metrics |
| 2 | Login endpoint response time (p95) | < 200ms | Spec NFR-AUTH.1; PRD Success Metrics |
| 3 | Average session duration | > 30 minutes | PRD Success Metrics |
| 4 | Failed login rate | < 5% of total attempts | PRD Success Metrics |
| 5 | Password reset completion rate (requested → new password set) | > 80% | PRD Success Metrics |
| 6 | Service availability (rolling 30-day) | ≥ 99.9% | Spec NFR-AUTH.2 |
| 7 | All unit, integration, and E2E tests passing | 100% pass rate | Spec §8 Test Plan |
| 8 | SOC2 audit log completeness | All auth events captured with required fields; 12-month retention | PRD Legal & Compliance |

---

## Open Questions

| # | Question | Source | Owner | Impact |
|---|----------|--------|-------|--------|
| 1 | Should password reset emails be sent synchronously or via a message queue? | Spec OI-1; PRD OQ-1 | Engineering | Affects reset endpoint latency and system resilience |
| 2 | What is the maximum number of active refresh tokens per user? | Spec OI-2; PRD OQ-2 | Product | Affects storage requirements and multi-device support |
| 3 | What is the account lockout policy after N consecutive failed login attempts? | Spec GAP-1; PRD OQ-3 | Security | Rate limiting (FR-AUTH.1d) partially addresses this but progressive lockout is undefined |
| 4 | Should "remember me" functionality extend session duration beyond 7 days? | PRD OQ-4 | Product | Affects refresh token TTL and UX |
| 5 | What audit logging fields and retention are required for auth events? | Spec GAP-2; PRD NFR (SOC2) | Security/Compliance | PRD specifies fields and 12-month retention, but spec has no corresponding FR or NFR — needs formal requirement |
| 6 | How should token revocation behave on user account deletion? | Spec GAP-3 | Architecture | Unaddressed edge case for user lifecycle management |
| 7 | Is GDPR consent collection (NFR-AUTH.4) a v1.0 hard requirement or can it be deferred? | PRD Legal & Compliance | Legal/Product | Spec does not mention GDPR consent; PRD states it is required — needs alignment |
| 8 | **JTBD coverage gap**: PRD JTBD #2 ("pick up where I left off") implies state preservation beyond session persistence. Is preserving in-progress work across session expiry in scope? | PRD §JTBD | Product | No FR addresses work-state preservation; only token refresh is specified |
| 9 | PRD includes a user story for Jordan (admin) viewing auth event logs, but the spec defers audit logging (GAP-2) to v1.1. Is admin audit log access in or out of v1.0 scope? | PRD User Stories AUTH-E3; Spec GAP-2 | Product/Engineering | Scope conflict between PRD and spec |
| 10 | PRD includes a logout user story ("As Alex, I want to log out") but the spec has no corresponding FR for logout. Is explicit logout/session termination a v1.0 requirement? | PRD User Stories AUTH-E1 | Product | Missing functional requirement if logout is in scope |
