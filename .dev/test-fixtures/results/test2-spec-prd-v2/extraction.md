---
spec_source: "test-spec-user-auth.md"
generated: "2026-04-03T00:00:00Z"
generator: "requirements-extraction-agent"
functional_requirements: 5
nonfunctional_requirements: 6
total_requirements: 11
complexity_score: 0.6
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, infrastructure]
risks_identified: 7
dependencies_identified: 7
success_criteria_count: 7
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 96.4, started_at: "2026-04-03T15:05:10.630800+00:00", finished_at: "2026-04-03T15:06:46.981785+00:00"}
---

## Functional Requirements

### FR-AUTH.1: User Login

**Description**: Authenticate users via email and password, returning JWT access token and refresh token upon successful credential verification.

**Acceptance Criteria**:
- **FR-AUTH.1a**: Valid email/password returns 200 with access_token (15min TTL) and refresh_token (7d TTL)
- **FR-AUTH.1b**: Invalid credentials return 401 without revealing whether email or password was incorrect
- **FR-AUTH.1c**: Locked account returns 403 indicating account suspension
- **FR-AUTH.1d**: Rate-limit login attempts to 5 per minute per IP address

**Dependencies**: PasswordHasher, TokenManager, User database table
**Complexity**: Medium — standard credential validation with rate limiting
**PRD Trace**: FR-AUTH.1 (PRD), AUTH-E1 epic, Alex persona login story

---

### FR-AUTH.2: User Registration

**Description**: Register new users with input validation, creating a user record with securely hashed password and returning confirmation.

**Acceptance Criteria**:
- **FR-AUTH.2a**: Valid registration data (email, password, display name) creates user record and returns 201 with user profile
- **FR-AUTH.2b**: Already-registered email returns 409 conflict response
- **FR-AUTH.2c**: Password policy enforced: minimum 8 characters, at least one uppercase, one lowercase, one digit
- **FR-AUTH.2d**: Email format validated before attempting registration

**Dependencies**: PasswordHasher, User database table
**Complexity**: Medium — input validation, uniqueness checks, hashing
**PRD Trace**: FR-AUTH.2 (PRD), AUTH-E1 epic, Alex persona registration story

---

### FR-AUTH.3: Token Refresh

**Description**: Issue and refresh JWT tokens, allowing clients to obtain new access tokens using valid refresh tokens without re-entering credentials.

**Acceptance Criteria**:
- **FR-AUTH.3a**: Valid refresh token returns new access_token and rotated refresh_token
- **FR-AUTH.3b**: Expired refresh token returns 401, requires re-authentication
- **FR-AUTH.3c**: Previously-rotated (revoked) refresh token triggers invalidation of all tokens for that user (replay detection)
- **FR-AUTH.3d**: Refresh token hashes stored in database for revocation support

**Dependencies**: TokenManager, JwtService, RefreshToken database table
**Complexity**: High — token rotation with replay detection is the most complex auth flow
**PRD Trace**: FR-AUTH.3 (PRD), AUTH-E2 epic, Sam persona token refresh story

---

### FR-AUTH.4: Profile Retrieval

**Description**: Authenticated user profile retrieval, returning current user's profile data when presented with a valid access token.

**Acceptance Criteria**:
- **FR-AUTH.4a**: Valid Bearer access_token returns user profile (id, email, display_name, created_at)
- **FR-AUTH.4b**: Expired or invalid token returns 401
- **FR-AUTH.4c**: Sensitive fields (password_hash, refresh_token_hash) never included in profile response

**Dependencies**: TokenManager, User database table
**Complexity**: Low — straightforward token verification and data retrieval
**PRD Trace**: FR-AUTH.4 (PRD), AUTH-E3 epic, Alex persona profile story

---

### FR-AUTH.5: Password Reset

**Description**: Secure password reset flow allowing users to request a reset link and set a new password using a time-limited token.

**Acceptance Criteria**:
- **FR-AUTH.5a**: Registered email triggers password reset token (1-hour TTL) and dispatches reset email
- **FR-AUTH.5b**: Valid reset token allows setting new password and invalidates the reset token
- **FR-AUTH.5c**: Expired or invalid reset token returns 400 with appropriate error
- **FR-AUTH.5d**: Successful password reset invalidates all existing sessions (refresh tokens)

**Dependencies**: TokenManager, PasswordHasher, Email service (external)
**Complexity**: Medium — multi-step async flow with external email dependency
**PRD Trace**: FR-AUTH.5 (PRD), AUTH-E3 epic, Alex persona password reset story

---

## Non-Functional Requirements

### NFR-AUTH.1: Authentication Endpoint Response Time

**Requirement**: Authentication endpoint response time < 200ms at p95 under normal load.
**Measurement**: Load testing with k6; production APM monitoring of p95 latency.
**Source**: Spec Section 6, PRD Success Metrics

---

### NFR-AUTH.2: Service Availability

**Requirement**: 99.9% uptime (< 8.76 hours downtime per year) over rolling 30-day windows.
**Measurement**: Health check endpoint uptime monitoring; PagerDuty alerting.
**Source**: Spec Section 6

---

### NFR-AUTH.3: Password Hashing Security

**Requirement**: bcrypt cost factor 12 (approximately 250ms per hash operation). Passwords never stored or logged in plain text.
**Measurement**: Unit test verifying cost factor; benchmark test for hash timing.
**Source**: Spec Section 6, PRD Legal & Compliance (NIST SP 800-63B)

---

### NFR-AUTH.4: GDPR Registration Consent (PRD-derived)

**Requirement**: Users must explicitly consent to data collection at registration. Consent must be recorded with a timestamp.
**Measurement**: Registration flow includes consent checkbox; database stores consent timestamp per user.
**Source**: PRD Legal & Compliance — GDPR requirement
**Note**: Not present in spec; surfaced from PRD Section S17.

---

### NFR-AUTH.5: SOC2 Audit Logging (PRD-derived)

**Requirement**: All authentication events must be logged with user ID, timestamp, IP address, and outcome. Logs retained for 12 months minimum.
**Measurement**: Log query returning complete auth event records; retention policy verification.
**Source**: PRD Legal & Compliance — SOC2 Type II requirement
**Note**: Identified as GAP-2 in spec Section 12. The PRD elevates this to a hard compliance requirement.

---

### NFR-AUTH.6: GDPR Data Minimization (PRD-derived)

**Requirement**: Only email, hashed password, and display name collected at registration. No additional PII required.
**Measurement**: Schema audit confirming no additional PII columns; registration form field audit.
**Source**: PRD Legal & Compliance — GDPR requirement

---

## Complexity Assessment

**Score**: 0.6 / 1.0
**Class**: MEDIUM

**Scoring Rationale**:

| Factor | Weight | Score | Justification |
|--------|--------|-------|---------------|
| Number of functional requirements | 0.15 | 0.5 | 5 requirements — moderate scope |
| Cryptographic complexity | 0.20 | 0.7 | JWT RS256 signing, bcrypt hashing, refresh token rotation with replay detection |
| External integrations | 0.15 | 0.5 | Single external dependency (email service); database is standard |
| Security sensitivity | 0.20 | 0.8 | Authentication is a high-security domain; errors have outsized impact |
| Data model complexity | 0.10 | 0.4 | Two tables (users, refresh_tokens); straightforward schema |
| Compliance requirements | 0.10 | 0.6 | GDPR consent, SOC2 audit logging, NIST password standards |
| Architectural scope | 0.10 | 0.5 | 4 new files, 3 modified files; clean layered architecture |

**Weighted Total**: 0.61 → rounded to **0.6**

The complexity is driven primarily by the security sensitivity of authentication (credential handling, token lifecycle, replay detection) and compliance requirements (GDPR, SOC2). The architectural scope is modest — a well-contained service with clear boundaries.

---

## Architectural Constraints

1. **Token format**: JWT with RS256 asymmetric signing. No opaque tokens or alternative formats.
2. **Password hashing**: bcrypt with cost factor 12. Argon2id is an acknowledged future option but not for v1.0.
3. **Token storage strategy**: Access token in memory, refresh token in httpOnly cookie. No localStorage or sessionStorage.
4. **Session strategy**: Stateless JWT with refresh rotation. No server-side session store.
5. **Database**: PostgreSQL 15+ required (PRD constraint). Users and refresh_tokens tables via migration 003.
6. **Layered architecture**: `AuthService` → `TokenManager` → `JwtService` with `PasswordHasher` as a peer utility. All components injectable and independently testable.
7. **Implementation language**: TypeScript (inferred from `.ts` file extensions in spec Section 4.1).
8. **Feature flag**: `AUTH_SERVICE_ENABLED` controls routing for rollback capability.
9. **Scope boundary (v1.0)**: Email/password only. No OAuth2/OIDC, no MFA, no RBAC, no social login.
10. **NIST SP 800-63B compliance**: Password policy must meet NIST guidelines (PRD constraint).

**Persona-driven design requirements** (from PRD Section S7):
- **Alex (End User)**: Registration must complete in under 60 seconds. Login UX must not enumerate valid emails. Session must persist across page refreshes for up to 7 days.
- **Jordan (Platform Admin)**: Auth event logs must be queryable by date range and user ID. Account lock/unlock capability required (partially addressed by FR-AUTH.1c, but admin tooling is out of spec scope).
- **Sam (API Consumer)**: Token refresh must work programmatically without user interaction. Error codes must be clear and documented.

---

## Risk Inventory

| # | Risk | Severity | Source | Mitigation |
|---|------|----------|--------|------------|
| 1 | JWT private key compromise allows forged tokens | **High** | Spec R1 | RS256 asymmetric keys; private key in secrets manager; 90-day key rotation |
| 2 | Refresh token replay attack after token theft | **High** | Spec R2 | Refresh token rotation with replay detection; full user token revocation on suspicious reuse |
| 3 | bcrypt cost factor becomes insufficient for future hardware | **Medium** | Spec R3 | Configurable cost factor; annual review against OWASP; migration path to Argon2id |
| 4 | Low registration adoption due to poor UX | **High** | PRD Risk | Usability testing before launch; funnel analytics; iterate on registration conversion |
| 5 | Security breach from implementation flaws | **High** | PRD Risk | Dedicated security review; penetration testing before production deployment |
| 6 | Compliance failure from incomplete audit logging | **High** | PRD Risk | Define log requirements early (NFR-AUTH.5); validate against SOC2 controls in QA |
| 7 | Email delivery failures blocking password reset | **Medium** | PRD Risk | Delivery monitoring and alerting; fallback support channel for account recovery |

---

## Dependency Inventory

| # | Dependency | Type | Required By | Impact if Unavailable |
|---|-----------|------|-------------|----------------------|
| 1 | `jsonwebtoken` library | NPM package | JwtService (jwt-service.ts) | Cannot sign or verify JWT tokens |
| 2 | `bcrypt` library | NPM package | PasswordHasher (password-hasher.ts) | Cannot hash or verify passwords |
| 3 | Email delivery service (SendGrid or equivalent) | External service | FR-AUTH.5 (Password Reset) | Password reset flow completely blocked |
| 4 | PostgreSQL 15+ | Infrastructure | All requirements | No persistent user or token storage |
| 5 | RSA key pair | Configuration / Secrets | JwtService (RS256 signing) | Cannot issue or verify tokens |
| 6 | Frontend routing framework | Internal | Auth UI pages | Registration, login, and reset pages cannot render |
| 7 | Security policy (SEC-POLICY-001) | Policy document | Password and token policies | Policy requirements undefined; compliance risk |

---

## Success Criteria

| # | Criterion | Target | Measurement Method | Source |
|---|-----------|--------|--------------------|--------|
| 1 | Login endpoint response time (p95) | < 200ms | k6 load testing; production APM | Spec NFR-AUTH.1, PRD Success Metrics |
| 2 | Service availability | 99.9% uptime (rolling 30-day) | Health check endpoint monitoring | Spec NFR-AUTH.2 |
| 3 | Registration conversion rate | > 60% | Funnel: landing → register → confirmed | PRD Success Metrics |
| 4 | Average session duration | > 30 minutes | Token refresh event analytics | PRD Success Metrics |
| 5 | Failed login rate | < 5% of attempts | Auth event log analysis | PRD Success Metrics |
| 6 | Password reset completion rate | > 80% | Funnel: reset requested → new password set | PRD Success Metrics |
| 7 | E2E user lifecycle scenario passes | All steps return expected status codes | Automated E2E test (Spec Section 8.3) | Spec Test Plan |

---

## Open Questions

| # | Question | Source | Owner | Impact |
|---|----------|--------|-------|--------|
| 1 | Should password reset emails be sent synchronously or via a message queue? | Spec OI-1, PRD OQ-1 | Engineering | Affects reset endpoint latency and system resilience |
| 2 | What is the maximum number of active refresh tokens per user? | Spec OI-2, PRD OQ-2 | Product | Affects storage requirements and multi-device support |
| 3 | What is the account lockout policy after N consecutive failed attempts? | Spec GAP-1, PRD OQ-3 | Security | Rate limiting (FR-AUTH.1d) is defined but progressive lockout is not |
| 4 | Should "remember me" functionality extend session duration beyond 7 days? | PRD OQ-4 | Product | Affects refresh token TTL and UX for returning users |
| 5 | Token revocation on user deletion — what happens to active tokens? | Spec GAP-3 | Architecture | Tokens could remain valid after account deletion without explicit handling |
| 6 | Audit logging scope — which exact auth events must be logged for SOC2? | Spec GAP-2, PRD NFR-AUTH.5 elevated | Engineering / Compliance | NFR-AUTH.5 (derived) requires this but spec defers to v1.1; PRD makes it a hard requirement |
| 7 | JTBD #4 (Sam: programmatic auth) — does the spec fully cover headless/API-only auth flows? | PRD JTBD analysis | Engineering | FR-AUTH.3 covers token refresh but no dedicated API key or service account mechanism is specified |
| 8 | Jordan (Admin) persona needs — admin auth event log viewing and account lock/unlock are in the PRD but absent from the spec's functional requirements. Are these v1.0 scope? | PRD persona gap | Product | Potential scope gap between PRD user stories and spec FRs |
