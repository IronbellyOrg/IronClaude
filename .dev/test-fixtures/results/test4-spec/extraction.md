---
spec_source: "test-spec-user-auth.md"
generated: "2026-04-15T12:00:00Z"
generator: "superclaude-requirements-extractor/opus-4.6"
functional_requirements: 5
nonfunctional_requirements: 3
total_requirements: 8
complexity_score: 0.6
complexity_class: MEDIUM
domains_detected: [backend, security]
risks_identified: 3
dependencies_identified: 6
success_criteria_count: 22
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 116.0, started_at: "2026-04-15T00:13:09.814345+00:00", finished_at: "2026-04-15T00:15:05.828973+00:00"}
---

## Functional Requirements

### FR-AUTH.1: User Login

**Description**: Authenticate users via email and password, returning a valid JWT access token and a refresh token upon successful credential verification.

**Acceptance Criteria**:

| ID | Criterion | Verification |
|----|-----------|--------------|
| FR-AUTH.1a | Given valid email and password, return 200 with access_token (15min TTL) and refresh_token (7d TTL) | Integration test: valid credential login flow |
| FR-AUTH.1b | Given invalid credentials, return 401 with error message; must not reveal whether email or password was incorrect | Unit test: error message content; security test: enumeration resistance |
| FR-AUTH.1c | Given a locked account, return 403 indicating account suspension | Unit test: locked account path |
| FR-AUTH.1d | Rate-limit login attempts to 5 per minute per IP address | Load test: verify 6th request within 60s is rejected |

**Dependencies**: PasswordHasher, TokenManager, User database table

**Priority**: Critical — core authentication entry point; all other FRs depend on the token model established here.

---

### FR-AUTH.2: User Registration

**Description**: Register new users with input validation, creating a user record with a securely hashed password and returning confirmation of successful registration.

**Acceptance Criteria**:

| ID | Criterion | Verification |
|----|-----------|--------------|
| FR-AUTH.2a | Given valid registration data (email, password, display name), create user record and return 201 with user profile | Integration test: full registration flow |
| FR-AUTH.2b | Given an already-registered email, return 409 conflict | Unit test: duplicate email rejection |
| FR-AUTH.2c | Enforce password policy: minimum 8 characters, at least one uppercase, one lowercase, one digit | Unit test: policy boundary cases (7 chars, missing class) |
| FR-AUTH.2d | Validate email format before attempting registration | Unit test: malformed email rejection |

**Dependencies**: PasswordHasher, User database table

**Priority**: Critical — required before any login can occur.

---

### FR-AUTH.3: Token Refresh

**Description**: Issue and refresh JWT tokens, allowing clients to obtain a new access token using a valid refresh token without re-entering credentials.

**Acceptance Criteria**:

| ID | Criterion | Verification |
|----|-----------|--------------|
| FR-AUTH.3a | Given a valid refresh token, return a new access_token and rotate the refresh_token | Integration test: refresh flow returns new pair |
| FR-AUTH.3b | Given an expired refresh token, return 401 and require re-authentication | Unit test: expired token rejection |
| FR-AUTH.3c | Given a previously-rotated (revoked) refresh token, invalidate all tokens for that user (replay detection) | Integration test: reuse of old refresh token triggers full revocation |
| FR-AUTH.3d | Store refresh token hashes in the database for revocation support | Unit test: verify SHA-256 hash stored, not plaintext |

**Dependencies**: TokenManager, JwtService, RefreshToken database table

**Priority**: High — directly affects session UX; addresses JIRA-2847 (forced re-login every 15 minutes).

---

### FR-AUTH.4: Profile Retrieval

**Description**: Provide authenticated user profile retrieval, returning the current user's profile data when presented with a valid access token.

**Acceptance Criteria**:

| ID | Criterion | Verification |
|----|-----------|--------------|
| FR-AUTH.4a | Given a valid Bearer access_token, return user profile (id, email, display_name, created_at) | Integration test: authenticated profile fetch |
| FR-AUTH.4b | Given an expired or invalid token, return 401 | Unit test: expired/malformed token rejection |
| FR-AUTH.4c | Must not return sensitive fields (password_hash, refresh_token_hash) in the profile response | Unit test: assert excluded fields; security test: response schema validation |

**Dependencies**: TokenManager, User database table

**Priority**: High — primary consumer of access tokens; validates the token verification pipeline.

---

### FR-AUTH.5: Password Reset

**Description**: Support a secure password reset flow, allowing users to request a reset link and set a new password using a time-limited token.

**Acceptance Criteria**:

| ID | Criterion | Verification |
|----|-----------|--------------|
| FR-AUTH.5a | Given a registered email, generate a password reset token (1-hour TTL) and dispatch a reset email | Integration test: reset request flow; verify email dispatch invoked |
| FR-AUTH.5b | Given a valid reset token, allow setting a new password and invalidate the reset token | Integration test: reset completion; verify token single-use |
| FR-AUTH.5c | Given an expired or invalid reset token, return 400 with appropriate error message | Unit test: expired/invalid reset token paths |
| FR-AUTH.5d | Invalidate all existing sessions (refresh tokens) upon successful password reset | Integration test: verify all refresh tokens revoked post-reset |

**Dependencies**: TokenManager, PasswordHasher, Email service (external)

**Priority**: High — security-critical flow; also addresses session hygiene on credential change.

---

## Non-Functional Requirements

### NFR-AUTH.1: Authentication Endpoint Response Time

**Requirement**: Authentication endpoint response time under 200ms at p95 under normal load.

**Target**: < 200ms p95

**Measurement**: Load testing with k6; monitor p95 latency in production APM.

**Rationale**: Login and token refresh are user-facing latency-sensitive operations. The 200ms budget includes bcrypt hashing (~250ms at cost 12), which implies the bcrypt operation dominates and may need async handling or careful budgeting.

**Note**: There is an implicit tension — bcrypt at cost factor 12 is specified to take ~250ms (NFR-AUTH.3), yet p95 latency target is < 200ms. This requires clarification (see Open Questions).

---

### NFR-AUTH.2: Service Availability

**Requirement**: 99.9% uptime (< 8.76 hours downtime/year).

**Target**: 99.9%

**Measurement**: Uptime monitoring via health check endpoint; PagerDuty alerting.

**Rationale**: Authentication is a critical path — any downtime blocks all authenticated operations across the platform.

---

### NFR-AUTH.3: Password Hashing Security

**Requirement**: bcrypt cost factor 12 (approx. 250ms per hash).

**Target**: Cost factor 12; ~250ms hash time.

**Measurement**: Unit test verifying cost factor; benchmark test for hash timing.

**Rationale**: OWASP-recommended minimum. Configurable to allow future increase without code changes.

---

## Complexity Assessment

**Score**: 0.6 / 1.0
**Class**: MEDIUM

### Scoring Rationale

| Factor | Score | Weight | Rationale |
|--------|-------|--------|-----------|
| Architectural scope | 0.5 | 20% | 4 new files, 3 modified files; well-bounded module with clear dependency graph |
| Security sensitivity | 0.8 | 25% | Cryptographic operations (JWT RS256, bcrypt), token lifecycle management, replay detection — errors here are high-impact |
| Integration surface | 0.5 | 15% | One external dependency (email service); database integration is standard ORM; middleware hook is single-point |
| State management | 0.7 | 20% | Refresh token rotation with replay detection introduces stateful complexity; revocation cascades across sessions |
| Domain familiarity | 0.4 | 10% | Authentication is well-understood domain with abundant reference implementations and libraries |
| Testing complexity | 0.6 | 10% | Requires unit, integration, and E2E tests; security-specific test scenarios (replay, timing, enumeration) |

**Weighted score**: (0.5×0.20) + (0.8×0.25) + (0.5×0.15) + (0.7×0.20) + (0.4×0.10) + (0.6×0.10) = 0.10 + 0.20 + 0.075 + 0.14 + 0.04 + 0.06 = **0.615 → 0.6**

The spec's self-assessed complexity of 0.6/MEDIUM is consistent with the weighted analysis. The security sensitivity is the primary driver of complexity; the architectural scope itself is modest.

---

## Architectural Constraints

### Technology Mandates

| Constraint | Source | Impact |
|------------|--------|--------|
| **JWT with RS256 signing** | Section 2.1 | Requires RSA key pair management; asymmetric keys must be stored securely |
| **bcrypt with cost factor 12** | Section 2.1, NFR-AUTH.3 | ~250ms per hash operation; constrains endpoint latency budget |
| **TypeScript implementation** | Section 4.1 (file extensions `.ts`) | All new modules must be TypeScript |
| **Stateless JWT sessions** | Section 2.1 | No server-side session store; all session state encoded in tokens |
| **Refresh token in httpOnly cookie** | Section 2.1 | Requires server to set cookies; affects CORS configuration |
| **Access token in memory** | Section 2.1 | Client-side responsibility; not persisted across page reloads |

### Integration Boundaries

| Boundary | Constraint |
|----------|-----------|
| **Database** | Requires two new tables (users, refresh_tokens) via migration 003 |
| **Middleware pipeline** | Must integrate via `auth-middleware.ts` modification; Bearer token extraction |
| **Route registration** | Must register under `/auth/*` route group in `src/routes/index.ts` |
| **Email service** | External dependency for password reset (FR-AUTH.5); interface not yet defined |
| **Secrets manager** | RSA private key must be stored externally; not in code or environment variables |

### Explicit Exclusions (v1.0 Scope Boundary)

- OAuth2/OIDC federation
- Multi-factor authentication (MFA)
- Role-based access control (RBAC)
- Social login providers
- Account lockout escalation (beyond rate limiting)
- Audit logging for auth events

---

## Risk Inventory

| # | Risk | Probability | Severity | Mitigation |
|---|------|-------------|----------|------------|
| R-1 | **JWT secret key compromise** allows forged tokens granting unauthorized access | Low | High | Use RS256 asymmetric keys; store private key in secrets manager; implement 90-day key rotation; monitor for anomalous token patterns |
| R-2 | **Refresh token replay attack** after token theft allows persistent unauthorized sessions | Medium | High | Refresh token rotation with replay detection (FR-AUTH.3c); full user token revocation on suspicious reuse; consider binding tokens to client fingerprint |
| R-3 | **bcrypt cost factor becomes insufficient** as hardware accelerates, weakening password security | Low | Medium | Make cost factor configurable; annual review against OWASP benchmarks; pre-plan migration path to Argon2id |
| R-4 | **NFR-AUTH.1 / NFR-AUTH.3 latency conflict** — bcrypt at cost 12 (~250ms) exceeds the 200ms p95 target | Medium | Medium | Implicit risk: the spec's own numbers conflict. Requires architectural resolution — async hashing, adjusted target, or reduced cost factor |
| R-5 | **Email service unavailability** blocks password reset flow entirely | Medium | Low | Define email service interface with retry/queue pattern (relates to OI-1); implement graceful degradation messaging |
| R-6 | **No account lockout policy** — rate limiting alone may not prevent distributed brute-force attacks | Medium | Medium | Identified as GAP-1 in spec; should define progressive lockout (e.g., lock after 10 failed attempts across all IPs within 1 hour) |

---

## Dependency Inventory

### External Libraries

| Dependency | Purpose | Used By | Version Constraint |
|------------|---------|---------|-------------------|
| `jsonwebtoken` | JWT signing and verification (RS256) | `jwt-service.ts` | Not specified; recommend pinning to latest stable |
| `bcrypt` | Password hashing with configurable cost factor | `password-hasher.ts` | Not specified; requires native addon compilation |

### External Services

| Dependency | Purpose | Used By | Availability Requirement |
|------------|---------|---------|------------------------|
| **Email service** | Dispatch password reset emails | FR-AUTH.5 | Interface undefined; sync vs async unresolved (OI-1) |
| **Secrets manager** | Store RSA private key for JWT signing | `jwt-service.ts`, key rotation | Must support key retrieval at service startup and rotation |

### Infrastructure

| Dependency | Purpose | Details |
|------------|---------|---------|
| **Database** (SQL) | Store users and refresh_tokens tables | Migration 003; requires UUID support, indexing on email and user_id |
| **RSA key pair** | Asymmetric JWT signing (RS256) | Must be generated and managed outside the application; 90-day rotation |

---

## Success Criteria

### Functional Success Criteria

| ID | Criterion | Threshold | Verification Method |
|----|-----------|-----------|-------------------|
| SC-1 | All FR-AUTH.1 acceptance criteria pass | 4/4 criteria green | Unit + integration tests |
| SC-2 | All FR-AUTH.2 acceptance criteria pass | 4/4 criteria green | Unit + integration tests |
| SC-3 | All FR-AUTH.3 acceptance criteria pass | 4/4 criteria green | Unit + integration tests |
| SC-4 | All FR-AUTH.4 acceptance criteria pass | 3/3 criteria green | Unit + integration tests |
| SC-5 | All FR-AUTH.5 acceptance criteria pass | 4/4 criteria green | Unit + integration tests |
| SC-6 | E2E user lifecycle scenario passes | All 6 steps return expected status codes | E2E test suite |
| SC-7 | No sensitive fields leaked in any API response | 0 occurrences of password_hash/token_hash in responses | Security test: response schema validation |

### Non-Functional Success Criteria

| ID | Criterion | Threshold | Verification Method |
|----|-----------|-----------|-------------------|
| SC-8 | Authentication endpoint p95 latency | < 200ms | k6 load test; production APM dashboard |
| SC-9 | Service availability | >= 99.9% | Health check monitoring; PagerDuty |
| SC-10 | bcrypt cost factor verified | Cost factor == 12 | Unit test assertion |
| SC-11 | bcrypt hash timing | ~250ms per operation | Benchmark test |

### Deployment Success Criteria

| ID | Criterion | Threshold | Verification Method |
|----|-----------|-----------|-------------------|
| SC-12 | Zero breaking changes to existing endpoints | All pre-existing integration tests pass | CI regression suite |
| SC-13 | Feature flag rollback functional | Disabling `AUTH_SERVICE_ENABLED` reverts to pre-auth behavior | Manual verification |
| SC-14 | Database migrations reversible | Down-migration drops tables cleanly | Migration rollback test |

---

## Open Questions

| # | Question | Source | Severity | Impact if Unresolved |
|---|----------|--------|----------|---------------------|
| OQ-1 | **Sync vs async password reset emails**: Should reset emails be sent synchronously (blocking the request) or via a message queue? | OI-1 (spec Section 11) | Medium | Synchronous dispatch adds latency and couples availability to email service; async requires message queue infrastructure not yet specified |
| OQ-2 | **Maximum active refresh tokens per user**: What is the limit on concurrent sessions (devices)? | OI-2 (spec Section 11) | Medium | No limit risks unbounded storage growth; too-low limit breaks multi-device UX. Affects RefreshToken table sizing and cleanup strategy |
| OQ-3 | **Latency conflict between NFR-AUTH.1 and NFR-AUTH.3**: bcrypt at cost factor 12 takes ~250ms, but p95 latency target is < 200ms. How is this reconciled? | Implicit contradiction between Sections 6 | High | The login endpoint cannot meet both requirements simultaneously without architectural changes (e.g., async hashing, adjusted target, or lower cost factor) |
| OQ-4 | **Account lockout policy beyond rate limiting**: Rate limiting (5/min/IP) is specified, but there is no progressive lockout after N total failures. Should one be defined? | GAP-1 (spec Section 12) | Medium | Distributed attacks from multiple IPs bypass per-IP rate limits. Without account-level lockout, brute-force remains feasible |
| OQ-5 | **Token revocation on user deletion**: What happens to outstanding tokens when a user account is deleted? | GAP-3 (spec Section 12) | Medium | Deleted users could retain valid tokens until expiry, accessing resources after account removal |
| OQ-6 | **Audit logging for authentication events**: Should login attempts, password changes, and token operations be logged for security monitoring? | GAP-2 (spec Section 12) | Low | Without audit logs, security incidents cannot be investigated or detected through log analysis |
| OQ-7 | **Email service interface contract**: The external email service is a dependency of FR-AUTH.5 but no interface, SDK, or API contract is specified. | Implicit from Section 4.1 | Medium | Cannot implement FR-AUTH.5 to completion without knowing how to dispatch emails |
| OQ-8 | **RSA key rotation procedure**: 90-day rotation is specified as mitigation for R-1, but no rotation mechanism or key versioning strategy is defined. | Implicit from Section 7 | Medium | Key rotation without versioning will invalidate all outstanding tokens simultaneously, causing mass forced re-authentication |
