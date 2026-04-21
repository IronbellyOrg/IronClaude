---
spec_source: "test-spec-user-auth.md"
generated: "2026-04-03T00:00:00Z"
generator: "requirements-extraction-agent"
functional_requirements: 5
nonfunctional_requirements: 3
total_requirements: 8
complexity_score: 0.6
complexity_class: MEDIUM
domains_detected: [backend, security]
risks_identified: 3
dependencies_identified: 7
success_criteria_count: 9
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 80.3, started_at: "2026-04-03T14:25:50.394468+00:00", finished_at: "2026-04-03T14:27:10.677363+00:00"}
---

## Functional Requirements

### FR-AUTH.1: User Login

**Description**: The system shall authenticate users via email and password, returning a valid JWT access token and a refresh token upon successful credential verification.

**Acceptance Criteria**:
- FR-AUTH.1a: Given valid email and password, return 200 with access_token (15min TTL) and refresh_token (7d TTL)
- FR-AUTH.1b: Given invalid credentials, return 401 without revealing whether email or password was incorrect
- FR-AUTH.1c: Given a locked account, return 403 indicating account suspension
- FR-AUTH.1d: Rate-limit login attempts to 5 per minute per IP address

**Dependencies**: PasswordHasher, TokenManager, User database table

**Priority**: High — core authentication entry point

---

### FR-AUTH.2: User Registration

**Description**: The system shall register new users with input validation, creating a user record with a securely hashed password and returning confirmation of successful registration.

**Acceptance Criteria**:
- FR-AUTH.2a: Given valid registration data (email, password, display name), create user record and return 201 with user profile
- FR-AUTH.2b: Given an already-registered email, return 409 conflict
- FR-AUTH.2c: Enforce password policy: minimum 8 characters, at least one uppercase, one lowercase, one digit
- FR-AUTH.2d: Validate email format before attempting registration

**Dependencies**: PasswordHasher, User database table

**Priority**: High — required for user onboarding

---

### FR-AUTH.3: Token Refresh

**Description**: The system shall issue and refresh JWT tokens, allowing clients to obtain a new access token using a valid refresh token without re-entering credentials.

**Acceptance Criteria**:
- FR-AUTH.3a: Given a valid refresh token, return new access_token and rotate the refresh_token
- FR-AUTH.3b: Given an expired refresh token, return 401 and require re-authentication
- FR-AUTH.3c: Given a previously-rotated (revoked) refresh token, invalidate all tokens for that user (replay detection)
- FR-AUTH.3d: Store refresh token hashes in the database for revocation support

**Dependencies**: TokenManager, JwtService, RefreshToken database table

**Priority**: High — critical for session continuity and security

---

### FR-AUTH.4: Profile Retrieval

**Description**: The system shall provide authenticated user profile retrieval, returning the current user's profile data when presented with a valid access token.

**Acceptance Criteria**:
- FR-AUTH.4a: Given a valid Bearer access_token, return user profile (id, email, display_name, created_at)
- FR-AUTH.4b: Given an expired or invalid token, return 401
- FR-AUTH.4c: Never return sensitive fields (password_hash, refresh_token_hash) in profile response

**Dependencies**: TokenManager, User database table

**Priority**: Medium — dependent on login/token infrastructure

---

### FR-AUTH.5: Password Reset

**Description**: The system shall support a secure password reset flow, allowing users to request a reset link and set a new password using a time-limited token.

**Acceptance Criteria**:
- FR-AUTH.5a: Given a registered email, generate a password reset token (1-hour TTL) and dispatch a reset email
- FR-AUTH.5b: Given a valid reset token, allow setting a new password and invalidate the reset token
- FR-AUTH.5c: Given an expired or invalid reset token, return 400 with appropriate error message
- FR-AUTH.5d: Invalidate all existing sessions (refresh tokens) upon successful password reset

**Dependencies**: TokenManager, PasswordHasher, Email service (external)

**Priority**: Medium — required for account recovery

---

### Implicit Functional Requirements

- **FR-AUTH.1-IMPL-1** (from Evidence table): The system shall replace all plaintext password storage with bcrypt hashes (addresses security audit finding in 2 modules)
- **FR-AUTH.1-IMPL-2** (from Section 2.1): Access tokens shall be stored in memory on the client; refresh tokens shall be stored in httpOnly cookies to prevent XSS
- **FR-AUTH.1-IMPL-3** (from Section 4.5): The system shall use UUID v4 for all record identifiers
- **FR-AUTH.1-IMPL-4** (from Section 9): The system shall support a feature flag `AUTH_SERVICE_ENABLED` to control authentication routing
- **FR-AUTH.1-IMPL-5** (from Section 9): Database migrations shall include down-migration scripts for rollback

---

## Non-Functional Requirements

### NFR-AUTH.1: Authentication Endpoint Response Time

**Requirement**: Authentication endpoint response time < 200ms at p95 under normal load.

**Measurement**: Load testing with k6; monitor p95 latency in production APM.

**Rationale**: Ensures acceptable user experience during login/token refresh flows.

---

### NFR-AUTH.2: Service Availability

**Requirement**: 99.9% uptime (< 8.76 hours downtime/year).

**Measurement**: Uptime monitoring via health check endpoint; PagerDuty alerting.

**Rationale**: Authentication is a critical path — downtime blocks all authenticated operations.

---

### NFR-AUTH.3: Password Hashing Security

**Requirement**: bcrypt cost factor 12 (approx. 250ms per hash).

**Measurement**: Unit test verifying cost factor; benchmark test for hash timing.

**Rationale**: Balances computational cost against brute-force resistance per OWASP guidelines.

---

### Implicit Non-Functional Requirements

- **NFR-AUTH-IMPL-1** (from Section 2.1): JWT signing shall use RS256 (asymmetric) for stateless verification and key separation
- **NFR-AUTH-IMPL-2** (from Risk Assessment): RSA private keys shall be stored in a secrets manager with 90-day rotation
- **NFR-AUTH-IMPL-3** (from Section 2): All authentication components shall be injectable and independently testable (testability constraint)
- **NFR-AUTH-IMPL-4** (from Section 2.1): The architecture shall support horizontal scalability with no shared session store

---

## Complexity Assessment

**Score**: 0.6 / 1.0
**Class**: MEDIUM

### Scoring Rationale

| Factor | Weight | Score | Justification |
|--------|--------|-------|---------------|
| Number of functional requirements | 0.15 | 0.5 | 5 FRs — moderate scope |
| Cryptographic operations | 0.20 | 0.7 | JWT RS256 signing, bcrypt hashing, token rotation — well-understood but error-prone |
| Data model complexity | 0.10 | 0.4 | 2 tables (users, refresh_tokens) with straightforward relationships |
| Security surface area | 0.25 | 0.7 | Rate limiting, replay detection, sensitive field filtering, secure token storage |
| External integrations | 0.10 | 0.5 | Email service for password reset is the only external dependency |
| State management | 0.10 | 0.6 | Stateless JWT with stateful refresh token revocation creates hybrid complexity |
| Migration/rollout risk | 0.10 | 0.4 | Additive service with feature flag; no breaking changes |

**Weighted total**: 0.59 ≈ **0.6**

The spec is well-bounded with clear scope exclusions (no OAuth, MFA, RBAC). The primary complexity drivers are cryptographic correctness and the refresh token rotation/replay detection mechanism.

---

## Architectural Constraints

1. **Language/Runtime**: TypeScript (evidenced by `.ts` file extensions and TypeScript interfaces in Section 4.5)
2. **Token format**: JWT with RS256 asymmetric signing — mandated, not negotiable
3. **Password hashing**: bcrypt with cost factor 12 — mandated
4. **Token storage strategy**: Access token in memory, refresh token in httpOnly cookie — mandated to prevent XSS
5. **Session strategy**: Stateless JWT — no server-side session store permitted
6. **Module architecture**: Layered dependency graph — `auth-middleware → auth-service → token-manager/password-hasher → jwt-service`
7. **Refresh token persistence**: Refresh token hashes (SHA-256) stored in database — required for revocation
8. **Implementation order**: `password-hasher` and `jwt-service` first (no deps), then `token-manager`, then `auth-service`, then middleware/routes/migrations
9. **Feature flag**: `AUTH_SERVICE_ENABLED` controls routing — required for rollback capability
10. **Migration reversibility**: All database migrations must include down-migration scripts

---

## Risk Inventory

1. **RISK-1: JWT secret key compromise** — Severity: **HIGH**
   - Probability: Low | Impact: High
   - Consequence: Forged tokens grant unauthorized access to any account
   - Mitigation: Use RS256 asymmetric keys; store private key in secrets manager; implement 90-day key rotation
   - Residual risk: Key rotation gap window; compromised secrets manager

2. **RISK-2: Refresh token replay attack** — Severity: **HIGH**
   - Probability: Medium | Impact: High
   - Consequence: Stolen refresh token grants persistent unauthorized access
   - Mitigation: Refresh token rotation with replay detection; revoke all user tokens on suspicious reuse
   - Residual risk: Window between token theft and first reuse detection

3. **RISK-3: bcrypt cost factor obsolescence** — Severity: **MEDIUM**
   - Probability: Low | Impact: Medium
   - Consequence: Future hardware makes current cost factor insufficient against brute-force
   - Mitigation: Configurable cost factor; annual review against OWASP; migration path to Argon2id
   - Residual risk: Requires proactive monitoring schedule

4. **RISK-4: Email service dependency for password reset** (implicit) — Severity: **MEDIUM**
   - Probability: Medium | Impact: Medium
   - Consequence: Email service outage blocks password reset flow entirely
   - Mitigation: Not specified in spec — see Open Questions
   - Residual risk: No fallback mechanism defined

---

## Dependency Inventory

### External Libraries

| Dependency | Purpose | Used By |
|------------|---------|---------|
| `jsonwebtoken` | JWT signing and verification (RS256) | `jwt-service.ts` |
| `bcrypt` | Password hashing with configurable cost factor | `password-hasher.ts` |

### External Services

| Dependency | Purpose | Used By |
|------------|---------|---------|
| Email service | Dispatch password reset emails | FR-AUTH.5 (password reset flow) |
| Secrets manager | Store RSA private key for JWT signing | `jwt-service.ts`, key rotation |

### Infrastructure

| Dependency | Purpose | Used By |
|------------|---------|---------|
| Database (users table) | Persistent user record storage | FR-AUTH.1, FR-AUTH.2, FR-AUTH.4 |
| Database (refresh_tokens table) | Refresh token hash storage for revocation | FR-AUTH.3 |
| k6 load testing tool | NFR-AUTH.1 performance validation | Test plan |

### Internal Dependencies

| Dependency | Purpose |
|------------|---------|
| `src/middleware/auth-middleware.ts` (existing, modified) | Bearer token extraction integration |
| `src/routes/index.ts` (existing, modified) | Route registration for `/auth/*` |

---

## Success Criteria

1. **SC-1**: All 5 functional requirements (FR-AUTH.1 through FR-AUTH.5) pass their acceptance criteria as defined in Section 3
2. **SC-2**: Authentication endpoint p95 latency < 200ms under normal load (NFR-AUTH.1)
3. **SC-3**: Service uptime ≥ 99.9% measured over first 30 days post-deploy (NFR-AUTH.2)
4. **SC-4**: bcrypt cost factor verified at 12 with hash timing ~250ms (NFR-AUTH.3)
5. **SC-5**: All unit tests pass — PasswordHasher, JwtService, TokenManager, AuthService (Section 8.1)
6. **SC-6**: All integration tests pass — full login flow, token refresh with rotation, registration-then-login (Section 8.2)
7. **SC-7**: E2E lifecycle scenario completes successfully — register → login → profile → refresh → reset → re-login (Section 8.3)
8. **SC-8**: No sensitive fields (password_hash, refresh_token_hash) exposed in any API response
9. **SC-9**: Rollback via `AUTH_SERVICE_ENABLED=false` feature flag restores pre-auth behavior without data loss

---

## Open Questions

### From Spec (Section 11 — Open Items)

1. **OI-1**: Should password reset emails be sent synchronously or via a message queue?
   - Impact: Affects latency of reset endpoint and system resilience
   - Resolution target: Sprint planning for v1.0
   - Recommendation: Async via message queue for resilience; synchronous as MVP fallback

2. **OI-2**: What is the maximum number of active refresh tokens per user?
   - Impact: Affects storage requirements and multi-device support
   - Resolution target: Architecture review meeting
   - Recommendation: Cap at 5-10 active tokens; oldest revoked on overflow

### From Gap Analysis (Section 12)

3. **GAP-1**: No account lockout policy defined after N failed attempts
   - Severity: Medium
   - Current state: Rate limiting (5/min/IP) partially addresses this but does not lock accounts after cumulative failures
   - Recommendation: Define progressive lockout (e.g., lock after 10 cumulative failures within 1 hour; unlock after 30 minutes or admin action)

4. **GAP-2**: Audit logging for authentication events not specified
   - Severity: Low (deferred to v1.1)
   - Recommendation: Log login success/failure, registration, token refresh, password reset events with timestamp, IP, and user_id

5. **GAP-3**: Token revocation on user deletion not addressed
   - Severity: Medium (deferred to v1.1)
   - Recommendation: Cascade-delete all refresh_tokens records on user deletion; add user_id to a JWT denylist until max token TTL expires

### Extracted Ambiguities

6. **OQ-1**: What constitutes "normal load" for NFR-AUTH.1 (< 200ms p95)? Concurrent user count and request rate are not defined.

7. **OQ-2**: The spec mandates RS256 but does not specify key size. Industry standard is 2048-bit minimum; 4096-bit recommended. Which should be used?

8. **OQ-3**: Rate limiting (FR-AUTH.1d) is specified per IP. Should there also be per-account rate limiting to prevent distributed brute-force attacks across multiple IPs?

9. **OQ-4**: The password reset flow (FR-AUTH.5) dispatches email but does not specify the reset link URL format, frontend integration, or token delivery mechanism (link vs. code).

10. **OQ-5**: The spec states refresh tokens are stored in httpOnly cookies (Section 2.1) but FR-AUTH.1 returns them in the JSON response body. These are contradictory — which is the intended transport mechanism?
