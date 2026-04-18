---
spec_source: "test-spec-user-auth.md"
generated: "2026-04-15T00:00:00Z"
generator: "requirements-extraction-agent/opus-4.6"
functional_requirements: 5
nonfunctional_requirements: 3
total_requirements: 8
complexity_score: 0.6
complexity_class: MEDIUM
domains_detected: [backend, security]
risks_identified: 3
dependencies_identified: 5
success_criteria_count: 22
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 133.0, started_at: "2026-04-15T16:29:03.394996+00:00", finished_at: "2026-04-15T16:31:16.409996+00:00"}
---

## Functional Requirements

### FR-AUTH.1: User Login

**Source**: Section 3, FR-AUTH.1
**Priority**: High
**Description**: The system shall authenticate users via email and password, returning a valid JWT access token and a refresh token upon successful credential verification.

**Acceptance Criteria**:

| ID | Criterion | Measurable |
|----|-----------|------------|
| FR-AUTH.1a | Given valid email and password, return 200 with access_token (15min TTL) and refresh_token (7d TTL) | Yes — verify HTTP status, token presence, and TTL claims |
| FR-AUTH.1b | Given invalid credentials, return 401 without revealing whether email or password was incorrect | Yes — verify response code and error message wording |
| FR-AUTH.1c | Given a locked account, return 403 indicating account suspension | Yes — verify response code for locked user record |
| FR-AUTH.1d | Rate-limit login attempts to 5 per minute per IP address | Yes — verify 429 response on 6th attempt within 60s |

**Dependencies**: PasswordHasher, TokenManager, User database table

---

### FR-AUTH.2: User Registration

**Source**: Section 3, FR-AUTH.2
**Priority**: High
**Description**: The system shall register new users with input validation, creating a user record with a securely hashed password and returning confirmation of successful registration.

**Acceptance Criteria**:

| ID | Criterion | Measurable |
|----|-----------|------------|
| FR-AUTH.2a | Given valid registration data (email, password, display name), create user record and return 201 with user profile | Yes — verify HTTP 201, database record creation |
| FR-AUTH.2b | Given an already-registered email, return 409 conflict | Yes — verify HTTP 409 on duplicate email |
| FR-AUTH.2c | Enforce password policy: minimum 8 characters, at least one uppercase, one lowercase, one digit | Yes — verify rejection of non-conforming passwords |
| FR-AUTH.2d | Validate email format before attempting registration | Yes — verify rejection of malformed email strings |

**Dependencies**: PasswordHasher, User database table

---

### FR-AUTH.3: Token Refresh

**Source**: Section 3, FR-AUTH.3
**Priority**: High
**Description**: The system shall issue and refresh JWT tokens, allowing clients to obtain a new access token using a valid refresh token without re-entering credentials.

**Acceptance Criteria**:

| ID | Criterion | Measurable |
|----|-----------|------------|
| FR-AUTH.3a | Given a valid refresh token, return a new access_token and rotate the refresh_token | Yes — verify new tokens issued, old refresh token invalidated |
| FR-AUTH.3b | Given an expired refresh token, return 401 and require re-authentication | Yes — verify HTTP 401 with expired token |
| FR-AUTH.3c | Given a previously-rotated (revoked) refresh token, invalidate all tokens for that user (replay detection) | Yes — verify all user tokens revoked on replay |
| FR-AUTH.3d | Store refresh token hashes in the database for revocation support | Yes — verify SHA-256 hash presence in RefreshToken table |

**Dependencies**: TokenManager, JwtService, RefreshToken database table

---

### FR-AUTH.4: Profile Retrieval

**Source**: Section 3, FR-AUTH.4
**Priority**: Medium
**Description**: The system shall provide authenticated user profile retrieval, returning the current user's profile data when presented with a valid access token.

**Acceptance Criteria**:

| ID | Criterion | Measurable |
|----|-----------|------------|
| FR-AUTH.4a | Given a valid Bearer access_token, return user profile (id, email, display_name, created_at) | Yes — verify response body schema |
| FR-AUTH.4b | Given an expired or invalid token, return 401 | Yes — verify HTTP 401 |
| FR-AUTH.4c | Never return sensitive fields (password_hash, refresh_token_hash) in profile response | Yes — verify field absence in response |

**Dependencies**: TokenManager, User database table

---

### FR-AUTH.5: Password Reset

**Source**: Section 3, FR-AUTH.5
**Priority**: Medium
**Description**: The system shall support a secure password reset flow, allowing users to request a reset link and set a new password using a time-limited token.

**Acceptance Criteria**:

| ID | Criterion | Measurable |
|----|-----------|------------|
| FR-AUTH.5a | Given a registered email, generate a password reset token (1-hour TTL) and dispatch a reset email | Yes — verify token creation and email dispatch |
| FR-AUTH.5b | Given a valid reset token, allow setting a new password and invalidate the reset token | Yes — verify password update, token single-use |
| FR-AUTH.5c | Given an expired or invalid reset token, return 400 with appropriate error | Yes — verify HTTP 400 |
| FR-AUTH.5d | Invalidate all existing sessions (refresh tokens) upon successful password reset | Yes — verify all refresh tokens revoked |

**Dependencies**: TokenManager, PasswordHasher, Email service (external)

---

## Non-Functional Requirements

### NFR-AUTH.1: Authentication Endpoint Response Time

**Source**: Section 6
**Category**: Performance
**Target**: < 200ms p95 under normal load
**Measurement**: Load testing with k6; monitor p95 latency in production APM
**Rationale**: Authentication is on the critical path of every user session; latency directly impacts perceived responsiveness.

### NFR-AUTH.2: Service Availability

**Source**: Section 6
**Category**: Reliability
**Target**: 99.9% uptime (< 8.76 hours downtime/year)
**Measurement**: Uptime monitoring via health check endpoint; PagerDuty alerting
**Rationale**: Authentication unavailability locks all users out of the application.

### NFR-AUTH.3: Password Hashing Security

**Source**: Section 6
**Category**: Security
**Target**: bcrypt cost factor 12 (approximately 250ms per hash operation)
**Measurement**: Unit test verifying cost factor; benchmark test for hash timing
**Rationale**: Cost factor must balance resistance to brute-force attacks against acceptable login latency.

---

## Complexity Assessment

**Score**: 0.6 / 1.0
**Class**: MEDIUM

### Scoring Rationale

| Factor | Weight | Score | Justification |
|--------|--------|-------|---------------|
| Number of components | 0.15 | 0.5 | 4 new files, 3 modified files — moderate surface area |
| Cryptographic operations | 0.20 | 0.7 | JWT RS256 signing, bcrypt hashing, refresh token rotation — well-understood but security-critical |
| External integrations | 0.15 | 0.4 | Email service is the only external integration; database is standard |
| Dependency depth | 0.15 | 0.5 | 4-layer dependency graph (middleware → service → manager → crypto) — straightforward |
| Security sensitivity | 0.20 | 0.8 | Authentication is a high-value target; errors have outsized security impact |
| State management | 0.15 | 0.6 | Stateless JWT simplifies runtime, but refresh token rotation adds revocation state |

**Weighted total**: (0.15×0.5) + (0.20×0.7) + (0.15×0.4) + (0.15×0.5) + (0.20×0.8) + (0.15×0.6) = 0.075 + 0.14 + 0.06 + 0.075 + 0.16 + 0.09 = **0.60**

The MEDIUM classification is appropriate. The individual components are well-understood (JWT, bcrypt), but the security sensitivity and refresh token rotation logic elevate complexity above LOW. The absence of OAuth/OIDC, MFA, and RBAC (deferred to v2.0) keeps it below HIGH.

---

## Architectural Constraints

| ID | Constraint | Source |
|----|-----------|--------|
| AC-1 | JWT tokens must use RS256 (asymmetric) signing, not HS256 (symmetric) | Section 2.1 — Design Decisions |
| AC-2 | Password hashing must use bcrypt with cost factor 12 | Section 2.1 — Design Decisions; NFR-AUTH.3 |
| AC-3 | Access tokens stored in client memory only; refresh tokens in httpOnly cookies | Section 2.1 — Token storage decision |
| AC-4 | Stateless JWT architecture; no server-side session store | Section 2.1 — Session strategy |
| AC-5 | All components must be injectable and independently testable | Section 2, paragraph 2 |
| AC-6 | RSA private key must be stored in a secrets manager, not in code or config files | Section 7, Risk 1 mitigation |
| AC-7 | Key rotation every 90 days | Section 7, Risk 1 mitigation |
| AC-8 | Feature flag `AUTH_SERVICE_ENABLED` must control routing for rollback capability | Section 9 — Rollback plan |
| AC-9 | Database migrations must include down-migration scripts | Section 9 — Rollback plan |
| AC-10 | Authentication is opt-in during phase 1, required for protected endpoints in phase 2 | Section 9 — Backwards compatibility |

---

## Component Inventory

| ID | Component | File Path | Role | Dependencies | Source Reference |
|----|-----------|-----------|------|-------------- |-----------------|
| COMP-001 | PasswordHasher | `src/auth/password-hasher.ts` | Encapsulates bcrypt password hashing and comparison with configurable cost factor | `bcrypt` library | Section 4.1, Section 4.4 |
| COMP-002 | JwtService | `src/auth/jwt-service.ts` | Low-level JWT signing and verification using RS256 with RSA key pair | `jsonwebtoken` library, RSA key pair | Section 4.1, Section 4.4 |
| COMP-003 | TokenManager | `src/auth/token-manager.ts` | JWT lifecycle management; issues, refreshes, and revokes token pairs | COMP-002 (JwtService), RefreshToken repository | Section 4.1, Section 4.4 |
| COMP-004 | AuthService | `src/auth/auth-service.ts` | Core authentication orchestrator; coordinates login, register, refresh, and reset flows | COMP-001 (PasswordHasher), COMP-003 (TokenManager), User repository | Section 4.1, Section 4.4 |
| COMP-005 | AuthMiddleware | `src/middleware/auth-middleware.ts` | Bearer token extraction and verification in request pipeline | COMP-003 (TokenManager) | Section 4.2, Section 4.4 |
| COMP-006 | AuthRoutes | `src/routes/index.ts` | Register `/auth/*` route group to expose authentication endpoints | COMP-004 (AuthService), COMP-005 (AuthMiddleware) | Section 4.2 |
| COMP-007 | AuthMigration | `src/database/migrations/003-auth-tables.ts` | Database migration for users and refresh_tokens tables | Database engine | Section 4.2 |

### Dependency Order (from Section 4.6)

```
Phase 1 (parallel): COMP-001 (PasswordHasher), COMP-002 (JwtService)
Phase 2 (parallel): COMP-003 (TokenManager) — after COMP-002 interface defined
Phase 3:            COMP-004 (AuthService) — depends on COMP-001, COMP-003
Phase 4:            COMP-005 (AuthMiddleware) — depends on COMP-003
Phase 5:            COMP-006 (AuthRoutes), COMP-007 (AuthMigration) — depends on COMP-004, COMP-005
```

---

## Risk Inventory

| ID | Risk | Probability | Impact | Severity | Mitigation |
|----|------|-------------|--------|----------|------------ |
| RISK-1 | JWT secret key compromise allows forged tokens | Low | High | **High** | Use RS256 asymmetric keys; store private key in secrets manager; implement key rotation every 90 days |
| RISK-2 | Refresh token replay attack after token theft | Medium | High | **High** | Implement refresh token rotation with replay detection; revoke all user tokens on suspicious reuse |
| RISK-3 | bcrypt cost factor too low for future hardware | Low | Medium | **Medium** | Make cost factor configurable; review annually against OWASP recommendations; migration path to Argon2id if needed |

### Gap-Derived Risks (from Section 12)

| ID | Gap | Severity | Status |
|----|-----|----------|--------|
| GAP-1 | No account lockout policy defined after N failed attempts | Medium | Partially addressed by FR-AUTH.1d rate limiting; needs progressive lockout |
| GAP-2 | Audit logging for authentication events not specified | Low | Deferred to v1.1 |
| GAP-3 | Token revocation on user deletion not addressed | Medium | Deferred to v1.1 |

---

## Dependency Inventory

| ID | Dependency | Type | Used By | Notes |
|----|-----------|------|---------|-------|
| DEP-1 | `jsonwebtoken` (npm) | Library | COMP-002 (JwtService) | JWT signing/verification with RS256 support |
| DEP-2 | `bcrypt` (npm) | Library | COMP-001 (PasswordHasher) | Password hashing with configurable cost factor |
| DEP-3 | Email service | External service | FR-AUTH.5 (Password Reset) | Dispatches password reset emails; delivery mechanism unspecified (see OI-1) |
| DEP-4 | Relational database | Infrastructure | COMP-004, COMP-007 | Persistent storage for users and refresh_tokens tables; specific engine not mandated |
| DEP-5 | Secrets manager | Infrastructure | COMP-002 (JwtService) | Stores RSA private key for JWT signing; specific provider not mandated |

---

## Success Criteria

| ID | Criterion | Threshold | Measurement Method | Source |
|----|-----------|-----------|-------------------|--------|
| SC-1 | Login with valid credentials returns tokens | HTTP 200 with access_token (15min TTL) and refresh_token (7d TTL) | Unit test + integration test | FR-AUTH.1a |
| SC-2 | Invalid credentials rejected without information leakage | HTTP 401 with generic error message | Unit test | FR-AUTH.1b |
| SC-3 | Locked account access denied | HTTP 403 | Unit test | FR-AUTH.1c |
| SC-4 | Login rate limiting enforced | HTTP 429 after 5 attempts/min/IP | Integration test | FR-AUTH.1d |
| SC-5 | User registration succeeds with valid data | HTTP 201 with user profile; record in database | Unit test + integration test | FR-AUTH.2a |
| SC-6 | Duplicate email rejected | HTTP 409 | Unit test | FR-AUTH.2b |
| SC-7 | Password policy enforced | Rejection of passwords failing: ≥8 chars, ≥1 upper, ≥1 lower, ≥1 digit | Unit test | FR-AUTH.2c |
| SC-8 | Email format validation | Rejection of malformed emails | Unit test | FR-AUTH.2d |
| SC-9 | Token refresh with rotation | New token pair issued; old refresh token invalidated | Unit test + integration test | FR-AUTH.3a |
| SC-10 | Expired refresh token rejected | HTTP 401 | Unit test | FR-AUTH.3b |
| SC-11 | Replay detection triggers full revocation | All user tokens revoked on reuse of rotated token | Unit test + integration test | FR-AUTH.3c |
| SC-12 | Refresh token hashes persisted | SHA-256 hash present in RefreshToken table | Unit test | FR-AUTH.3d |
| SC-13 | Authenticated profile retrieval | Correct fields (id, email, display_name, created_at) returned | Unit test | FR-AUTH.4a |
| SC-14 | Invalid token rejected on profile endpoint | HTTP 401 | Unit test | FR-AUTH.4b |
| SC-15 | Sensitive fields excluded from profile | password_hash and refresh_token_hash absent | Unit test | FR-AUTH.4c |
| SC-16 | Password reset token issued and email sent | Token with 1hr TTL created; email dispatched | Unit test | FR-AUTH.5a |
| SC-17 | Password reset with valid token | Password updated; reset token invalidated | Unit test | FR-AUTH.5b |
| SC-18 | Invalid/expired reset token rejected | HTTP 400 | Unit test | FR-AUTH.5c |
| SC-19 | Sessions invalidated on password reset | All refresh tokens revoked | Unit test + integration test | FR-AUTH.5d |
| SC-20 | Authentication endpoint p95 latency | < 200ms under normal load | k6 load test; production APM | NFR-AUTH.1 |
| SC-21 | Service availability | 99.9% uptime | Health check monitoring; PagerDuty | NFR-AUTH.2 |
| SC-22 | Password hashing cost factor | bcrypt cost factor 12 (~250ms/hash) | Unit test + benchmark | NFR-AUTH.3 |

---

## Open Questions

| ID | Question | Source | Impact | Resolution Target |
|----|----------|--------|--------|-------------------|
| OQ-1 | Should password reset emails be sent synchronously or via a message queue? | OI-1 (Section 11) | Synchronous dispatch adds latency to the reset endpoint and creates a hard dependency on email service availability. Message queue adds infrastructure complexity but improves resilience. | Sprint planning for v1.0 |
| OQ-2 | What is the maximum number of active refresh tokens per user? | OI-2 (Section 11) | Determines whether multi-device login is supported and affects storage requirements for the refresh_tokens table. Unbounded tokens increase storage and revocation scan cost. | Architecture review meeting |
| OQ-3 | What specific relational database engine is targeted? | Implicit (Section 4) | Migration syntax, indexing strategy, and UUID generation differ across PostgreSQL, MySQL, and SQLite. The spec does not mandate a database engine. | Architecture review meeting |
| OQ-4 | How should the account lockout policy work beyond rate limiting? | GAP-1 (Section 12) | FR-AUTH.1d rate-limits by IP but does not define progressive account lockout (e.g., lock after 10 failed attempts across all IPs). This leaves credential stuffing attacks from distributed sources partially unaddressed. | Security review for v1.0 |
| OQ-5 | What audit logging is required for authentication events? | GAP-2 (Section 12) | Compliance and incident response may require logging of login attempts, token refreshes, password resets, and account lockouts. No logging format or destination is specified. | v1.1 planning |
| OQ-6 | How should token revocation behave when a user account is deleted? | GAP-3 (Section 12) | If a user is deleted but their access token remains valid (up to 15 minutes), they could continue accessing protected resources. The spec does not address this race condition. | v1.1 planning |
| OQ-7 | What is the RSA key size for RS256 signing? | Implicit (Section 2.1) | The spec mandates RS256 but does not specify key length (2048-bit vs 4096-bit). This affects both security strength and signing/verification latency. | Architecture review meeting |
