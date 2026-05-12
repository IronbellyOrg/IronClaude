---
spec_source: "test-spec-user-auth.md"
generated: "2026-04-02T00:00:00Z"
generator: "requirements-extraction-agent"
functional_requirements: 5
nonfunctional_requirements: 7
total_requirements: 12
complexity_score: 0.6
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, infrastructure, compliance]
risks_identified: 7
dependencies_identified: 9
success_criteria_count: 6
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 94.3, started_at: "2026-04-03T03:07:23.818688+00:00", finished_at: "2026-04-03T03:08:58.149023+00:00"}
---

## Functional Requirements

### FR-AUTH.1: User Login

**Source**: Spec §3, FR-AUTH.1
**Description**: Authenticate users via email and password, returning a valid JWT access token and refresh token upon successful credential verification.

**Acceptance Criteria**:
- **FR-AUTH.1a**: Valid email/password returns 200 with access_token (15min TTL) and refresh_token (7d TTL)
- **FR-AUTH.1b**: Invalid credentials return 401 without revealing whether email or password was incorrect
- **FR-AUTH.1c**: Locked account returns 403 indicating account suspension
- **FR-AUTH.1d**: Rate-limit login attempts to 5 per minute per IP address

**Dependencies**: PasswordHasher, TokenManager, User database table
**Priority**: Critical — blocks all authenticated functionality

---

### FR-AUTH.2: User Registration

**Source**: Spec §3, FR-AUTH.2
**Description**: Register new users with input validation, creating a user record with securely hashed password and returning confirmation.

**Acceptance Criteria**:
- **FR-AUTH.2a**: Valid registration data (email, password, display name) creates user record and returns 201 with user profile
- **FR-AUTH.2b**: Already-registered email returns 409 conflict
- **FR-AUTH.2c**: Password policy enforced: minimum 8 characters, at least one uppercase, one lowercase, one digit
- **FR-AUTH.2d**: Email format validated before attempting registration

**Dependencies**: PasswordHasher, User database table
**Priority**: Critical — prerequisite for all user identity

---

### FR-AUTH.3: Token Refresh

**Source**: Spec §3, FR-AUTH.3
**Description**: Issue and refresh JWT tokens, allowing clients to obtain new access tokens using valid refresh tokens without re-entering credentials.

**Acceptance Criteria**:
- **FR-AUTH.3a**: Valid refresh token returns new access_token and rotated refresh_token
- **FR-AUTH.3b**: Expired refresh token returns 401 requiring re-authentication
- **FR-AUTH.3c**: Previously-rotated (revoked) refresh token triggers invalidation of all tokens for that user (replay detection)
- **FR-AUTH.3d**: Refresh token hashes stored in database for revocation support

**Dependencies**: TokenManager, JwtService, RefreshToken database table
**Priority**: High — required for session persistence (PRD JTBD #2, #4)

---

### FR-AUTH.4: Profile Retrieval

**Source**: Spec §3, FR-AUTH.4
**Description**: Provide authenticated user profile retrieval, returning current user's profile data when presented with a valid access token.

**Acceptance Criteria**:
- **FR-AUTH.4a**: Valid Bearer access_token returns user profile (id, email, display_name, created_at)
- **FR-AUTH.4b**: Expired or invalid token returns 401
- **FR-AUTH.4c**: Sensitive fields (password_hash, refresh_token_hash) never included in profile response

**Dependencies**: TokenManager, User database table
**Priority**: Medium

---

### FR-AUTH.5: Password Reset

**Source**: Spec §3, FR-AUTH.5
**Description**: Secure password reset flow allowing users to request a reset link and set a new password using a time-limited token.

**Acceptance Criteria**:
- **FR-AUTH.5a**: Registered email triggers password reset token (1-hour TTL) and dispatches reset email
- **FR-AUTH.5b**: Valid reset token allows setting new password and invalidates the reset token
- **FR-AUTH.5c**: Expired or invalid reset token returns 400 with appropriate error
- **FR-AUTH.5d**: All existing sessions (refresh tokens) invalidated upon successful password reset

**Dependencies**: TokenManager, PasswordHasher, Email service (external)
**Priority**: High — directly supports self-service recovery (PRD JTBD #3)

---

## Non-Functional Requirements

### NFR-AUTH.1: Authentication Response Time

**Source**: Spec §6; PRD §Success Metrics
**Requirement**: Authentication endpoint response time < 200ms p95 under normal load
**Measurement**: Load testing with k6; production APM monitoring

---

### NFR-AUTH.2: Service Availability

**Source**: Spec §6
**Requirement**: 99.9% uptime (< 8.76 hours downtime/year)
**Measurement**: Health check endpoint uptime monitoring; PagerDuty alerting

---

### NFR-AUTH.3: Password Hashing Security

**Source**: Spec §6
**Requirement**: bcrypt cost factor 12 (approx. 250ms per hash)
**Measurement**: Unit test verifying cost factor; benchmark test for hash timing

---

### NFR-AUTH.4: GDPR Consent at Registration

**Source**: PRD §Legal & Compliance
**Requirement**: Users must consent to data collection at registration. Consent recorded with timestamp.
**Measurement**: Registration flow includes consent checkbox; consent records queryable in database
**Note**: Not explicitly addressed in spec — derived from PRD compliance requirements.

---

### NFR-AUTH.5: SOC2 Audit Logging

**Source**: PRD §Legal & Compliance; PRD §User Stories (Jordan the Admin)
**Requirement**: All auth events logged with user ID, timestamp, IP address, and outcome. 12-month retention minimum.
**Measurement**: Log completeness audit; queryable by date range and user
**Note**: Identified as GAP-2 in spec §12. PRD elevates this to a compliance requirement for SOC2 Type II audit (Q3 2026 deadline).

---

### NFR-AUTH.6: NIST-Compliant Password Storage

**Source**: PRD §Legal & Compliance; PRD §Assumptions and Constraints
**Requirement**: One-way adaptive hashing per NIST SP 800-63B. Raw passwords never persisted or logged.
**Measurement**: Security review; code audit confirming no plaintext password storage or logging

---

### NFR-AUTH.7: GDPR Data Minimization

**Source**: PRD §Legal & Compliance
**Requirement**: Only email, hashed password, and display name collected. No additional PII required.
**Measurement**: Schema audit confirming no extraneous PII fields in user table

---

## Complexity Assessment

**Score**: 0.6 / 1.0
**Class**: MEDIUM

**Scoring Rationale**:

| Factor | Score | Rationale |
|--------|-------|-----------|
| Functional breadth | 0.5 | 5 functional requirements — moderate scope, well-bounded |
| Security sensitivity | 0.8 | Authentication is security-critical; JWT, bcrypt, token rotation, replay detection |
| Integration surface | 0.5 | External email service dependency; database migrations; middleware integration |
| Architectural novelty | 0.4 | Standard layered auth architecture; well-understood patterns (JWT, bcrypt) |
| Data model complexity | 0.5 | Two new tables (users, refresh_tokens); foreign key relationships; indexed fields |
| Compliance burden | 0.7 | GDPR consent, SOC2 audit logging, NIST password standards |
| Open questions | 0.6 | 2 spec open items + 4 PRD open questions; some affect architecture (async email, lockout policy) |

**Composite**: Weighted average yields 0.6. The domain (authentication) is well-understood but security-sensitive, requiring careful implementation of cryptographic operations, token lifecycle management, and compliance controls. No novel algorithmic challenges, but the consequences of implementation errors are high.

---

## Architectural Constraints

### Technology Mandates (from Spec)
1. **JWT with RS256 signing** — asymmetric key pair required; no symmetric (HS256) fallback
2. **bcrypt with cost factor 12** — configurable but not negotiable below 12
3. **Refresh token in httpOnly cookie** — access token in memory; prevents XSS vector
4. **Stateless JWT sessions** — no server-side session store; horizontal scalability required
5. **TypeScript implementation** — file paths and interfaces indicate TypeScript codebase

### Integration Boundaries
6. **Layered module dependency** — auth-middleware → auth-service → token-manager/password-hasher → jwt-service
7. **Database migration required** — new `users` and `refresh_tokens` tables via migration 003
8. **Middleware integration** — Bearer token extraction added to existing request pipeline
9. **Route registration** — `/auth/*` route group added to existing route index

### Persona-Driven Design Requirements (from PRD)
10. **Alex (End User)** — registration must complete in < 60 seconds; inline validation; no user enumeration on errors; silent token refresh during active sessions
11. **Jordan (Platform Admin)** — auth event logs must be queryable by date range and user; account lock/unlock capability needed (partially out of scope per spec GAP-1)
12. **Sam (API Consumer)** — programmatic token refresh without user interaction; clear error codes; stable auth contract

### Infrastructure Assumptions (from PRD)
13. **PostgreSQL 15+** — required for persistent user storage
14. **Email delivery service (SendGrid)** — required before development of FR-AUTH.5
15. **Frontend routing framework** — required for auth page rendering

---

## Risk Inventory

| # | Risk | Severity | Source | Mitigation |
|---|------|----------|--------|------------|
| R1 | JWT private key compromise allows forged tokens | **High** | Spec §7 | RS256 asymmetric keys; private key in secrets manager; 90-day key rotation |
| R2 | Refresh token replay attack after theft | **High** | Spec §7 | Refresh token rotation with replay detection; revoke all user tokens on suspicious reuse |
| R3 | bcrypt cost factor insufficient for future hardware | **Medium** | Spec §7 | Configurable cost factor; annual OWASP review; migration path to Argon2id |
| R4 | Low registration adoption due to poor UX | **High** | PRD §Risk Analysis | Usability testing before launch; iterate based on funnel conversion data |
| R5 | Security breach from implementation flaws | **High** | PRD §Risk Analysis | Dedicated security review; penetration testing before production deployment |
| R6 | Compliance failure from incomplete audit logging | **High** | PRD §Risk Analysis | Define log schema early; validate against SOC2 controls in QA; 12-month retention |
| R7 | Email delivery failures blocking password reset | **Medium** | PRD §Risk Analysis | Delivery monitoring and alerting; fallback support channel for manual reset |

---

## Dependency Inventory

| # | Dependency | Type | Required By | Impact if Unavailable |
|---|-----------|------|-------------|----------------------|
| D1 | `jsonwebtoken` library | NPM package | jwt-service.ts | Cannot sign/verify JWT tokens |
| D2 | `bcrypt` library | NPM package | password-hasher.ts | Cannot hash/verify passwords |
| D3 | RSA key pair (RS256) | Cryptographic asset | jwt-service.ts | Cannot sign tokens; must be provisioned in secrets manager |
| D4 | PostgreSQL 15+ | Infrastructure | User & RefreshToken tables | No persistent storage for auth data |
| D5 | Email delivery service (SendGrid) | External service | FR-AUTH.5 (password reset) | Password reset flow completely blocked |
| D6 | User database table (migration 003) | Database schema | FR-AUTH.1, FR-AUTH.2, FR-AUTH.4 | No user records possible |
| D7 | RefreshToken database table (migration 003) | Database schema | FR-AUTH.3 | No refresh token revocation/rotation |
| D8 | Frontend routing framework | Internal | Auth page rendering | Login/registration UI cannot render |
| D9 | SEC-POLICY-001 (Security Policy) | Policy document | Password/token policy definitions | Policy requirements undefined |

---

## Success Criteria

| # | Criterion | Target | Source | Measurement Method |
|---|-----------|--------|--------|-------------------|
| SC1 | Registration conversion rate | > 60% | PRD §Success Metrics | Funnel: landing → register → confirmed account |
| SC2 | Login response time (p95) | < 200ms | Spec §6 / PRD §Success Metrics | k6 load testing; production APM on login endpoint |
| SC3 | Average session duration | > 30 minutes | PRD §Success Metrics | Token refresh event analytics |
| SC4 | Failed login rate | < 5% of total attempts | PRD §Success Metrics | Auth event log analysis |
| SC5 | Password reset completion rate | > 80% | PRD §Success Metrics | Funnel: reset requested → new password set |
| SC6 | Service availability | 99.9% uptime | Spec §6 | Health check endpoint monitoring; rolling 30-day windows |

---

## Open Questions

| # | Question | Source | Owner | Impact |
|---|----------|--------|-------|--------|
| OQ1 | Should password reset emails be sent synchronously or via a message queue? | Spec OI-1 / PRD OQ-1 | Engineering | Affects reset endpoint latency and system resilience; async preferred for scalability but adds infrastructure dependency |
| OQ2 | Maximum number of active refresh tokens per user? | Spec OI-2 / PRD OQ-2 | Product | Affects storage requirements, multi-device support, and security posture |
| OQ3 | Account lockout policy after N consecutive failed attempts? | Spec GAP-1 / PRD OQ-3 | Security | Currently only rate-limiting (5/min/IP) is specified; progressive lockout not defined. Affects FR-AUTH.1 |
| OQ4 | Should "remember me" extend session duration beyond 7 days? | PRD OQ-4 | Product | Affects refresh token TTL and UX for returning users |
| OQ5 | Token revocation on user deletion — what happens to active sessions? | Spec GAP-3 | Architecture | Not addressed in spec; could leave orphaned tokens if user record is deleted |
| OQ6 | Audit logging scope and implementation — is this in scope for v1.0? | Spec GAP-2 / PRD NFR (SOC2) | Product/Engineering | PRD requires SOC2 audit logging (Q3 2026 deadline), but spec defers to v1.1. **Conflict**: PRD compliance timeline may force this into v1.0 scope |
| OQ7 | GDPR consent mechanism at registration — explicit checkbox or terms acceptance? | PRD §Legal & Compliance | Product/Legal | Spec does not address consent collection; PRD requires it. Must be added to FR-AUTH.2 |
| OQ8 | Logout endpoint — spec does not define FR for logout, but PRD user stories include it | PRD §User Stories (AUTH-E1) | Engineering | PRD includes "log out" as a user story with acceptance criteria, but spec has no corresponding FR. Needs reconciliation |
| OQ9 | PRD JTBD #2 (returning user picks up where they left off) — no spec requirement maps to state persistence beyond session tokens | PRD §JTBD | Product | JTBD implies application state persistence, not just session persistence. May be out of scope but should be confirmed |
