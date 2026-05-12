---
spec_source: test-spec-user-auth.md
generated: "2026-03-27T00:00:00Z"
generator: requirements-extraction-specialist-v1
functional_requirements: 5
nonfunctional_requirements: 3
total_requirements: 8
complexity_score: 0.62
complexity_class: MEDIUM
domains_detected: [backend, security, database]
risks_identified: 3
dependencies_identified: 7
success_criteria_count: 8
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 121.4, started_at: "2026-03-27T15:39:59.373743+00:00", finished_at: "2026-03-27T15:42:00.818363+00:00"}
---

## Functional Requirements

### FR-AUTH.1: User Login

**Priority**: Critical  
**Status**: Specified  
**Description**: The system shall authenticate users via email and password, returning a valid JWT access token and a refresh token upon successful credential verification.

**Acceptance Criteria**:
- AC-1: Given valid email and password → 200 response with `access_token` (15-minute TTL) and `refresh_token` (7-day TTL)
- AC-2: Given invalid credentials → 401 response with generic error; must not reveal whether email or password was incorrect
- AC-3: Given a locked account → 403 response indicating account suspension
- AC-4: Rate-limit login attempts to 5 per minute per IP address

**Component Dependencies**: `PasswordHasher`, `TokenManager`, User database table

---

### FR-AUTH.2: User Registration

**Priority**: Critical  
**Status**: Specified  
**Description**: The system shall register new users with input validation, creating a user record with a securely hashed password and returning confirmation of successful registration.

**Acceptance Criteria**:
- AC-1: Given valid registration data (email, password, display name) → create user record, return 201 with user profile
- AC-2: Given an already-registered email → 409 Conflict response
- AC-3: Enforce password policy: minimum 8 characters, at least one uppercase, one lowercase, one digit
- AC-4: Validate email format before attempting registration

**Component Dependencies**: `PasswordHasher`, User database table

---

### FR-AUTH.3: Token Refresh

**Priority**: High  
**Status**: Specified  
**Description**: The system shall issue and refresh JWT tokens, allowing clients to obtain a new access token using a valid refresh token without re-entering credentials.

**Acceptance Criteria**:
- AC-1: Given a valid refresh token → return new `access_token` and rotate the `refresh_token`
- AC-2: Given an expired refresh token → 401, require re-authentication
- AC-3: Given a previously-rotated (revoked) refresh token → invalidate all tokens for that user (replay detection)
- AC-4: Store refresh token hashes in the database for revocation support

**Component Dependencies**: `TokenManager`, `JwtService`, RefreshToken database table

---

### FR-AUTH.4: Profile Retrieval

**Priority**: High  
**Status**: Specified  
**Description**: The system shall provide authenticated user profile retrieval, returning the current user's profile data when presented with a valid access token.

**Acceptance Criteria**:
- AC-1: Given a valid Bearer `access_token` → return user profile (`id`, `email`, `display_name`, `created_at`)
- AC-2: Given an expired or invalid token → 401 response
- AC-3: Must not return sensitive fields (`password_hash`, `refresh_token_hash`) in the profile response

**Component Dependencies**: `TokenManager`, User database table

---

### FR-AUTH.5: Password Reset

**Priority**: High  
**Status**: Specified  
**Description**: The system shall support a secure password reset flow, allowing users to request a reset link and set a new password using a time-limited token.

**Acceptance Criteria**:
- AC-1: Given a registered email → generate password reset token (1-hour TTL) and dispatch a reset email
- AC-2: Given a valid reset token → allow setting a new password and invalidate the reset token
- AC-3: Given an expired or invalid reset token → 400 with appropriate error message
- AC-4: Invalidate all existing sessions (refresh tokens) upon successful password reset

**Component Dependencies**: `TokenManager`, `PasswordHasher`, Email service (external)

---

## Non-Functional Requirements

### NFR-AUTH.1: Authentication Endpoint Latency

**Category**: Performance  
**Target**: < 200ms p95 under normal load  
**Measurement**: Load testing with k6; monitor p95 latency in production APM  
**Notes**: The 250ms bcrypt hashing budget (NFR-AUTH.3) is the dominant contributor; total target is tight and requires careful profiling of the full login code path.

---

### NFR-AUTH.2: Service Availability

**Category**: Reliability  
**Target**: 99.9% uptime (< 8.76 hours downtime per year)  
**Measurement**: Uptime monitoring via health check endpoint; PagerDuty alerting  
**Notes**: No SLO degradation policy or tiered-availability plan is specified for scheduled maintenance windows.

---

### NFR-AUTH.3: Password Hashing Security

**Category**: Security  
**Target**: bcrypt cost factor 12 (≈ 250ms per hash operation)  
**Measurement**: Unit test verifying cost factor; benchmark test for hash timing  
**Notes**: Cost factor must be configurable per the Risk Inventory (RISK-3). Review cadence against OWASP recommendations not formally scheduled.

---

## Complexity Assessment

**Score**: 0.62 / MEDIUM

| Driver | Weight | Rationale |
|--------|--------|-----------|
| Security criticality | High | Cryptographic primitives (RS256, bcrypt), replay detection, rate limiting — all must be implemented correctly with no margin for error |
| Component count | Medium | 4 new files + 3 modified files; layered dependency graph with clear interfaces but non-trivial interaction surface |
| External dependencies | Medium | 7 external dependencies including an email service that is unspecified in implementation detail |
| Functional breadth | Medium | 5 distinct flows, each with 3–4 acceptance criteria; not deeply coupled but span the full stack |
| State management | Medium | Refresh token rotation requires transactional database operations to prevent race conditions on concurrent refresh attempts |
| Explicit out-of-scope | Reduces | OAuth2, MFA, RBAC, and social login are explicitly deferred, tightly bounding implementation scope |
| Test coverage plan | Reduces | Unit, integration, and E2E scenarios are pre-specified, lowering implementation ambiguity |

The spec's self-assessed 0.6 is confirmed. The primary complexity vectors are the security correctness requirements and the stateful refresh token rotation logic, not the breadth of functionality.

---

## Architectural Constraints

**Technology Mandates**
- JWT format using **RS256 asymmetric signing** (not HS256 or PASETO)
- **bcrypt** for password hashing with cost factor 12; Argon2id is a documented future migration path
- Access tokens stored **in memory** on the client; refresh tokens delivered via **httpOnly cookie** (XSS/CSRF mitigation)
- Stateless JWT session model — no shared session store; horizontal scaling is a first-class constraint

**Implementation Order (hard dependency)**
```
1. password-hasher.ts      (no dependencies)
2. jwt-service.ts          (no dependencies, parallel with token-manager once interface defined)
   token-manager.ts        (parallel with jwt-service)
3. auth-service.ts         (depends on 1, 2)
4. auth-middleware.ts      (depends on token-manager)
5. routes + migrations     (depends on 3, 4)
```

**Integration Boundaries**
- `AuthService` is the sole external-facing orchestrator; internal components (`TokenManager`, `JwtService`, `PasswordHasher`) are **not exposed directly** via HTTP
- Authentication middleware integrates into the existing `src/middleware/auth-middleware.ts`; no new middleware framework is introduced
- Routes registered under `/auth/*` group in `src/routes/index.ts`
- Database schema managed via migration `003-auth-tables.ts`; down-migration scripts required (rollback plan)

**Deployment Constraints**
- Feature flag `AUTH_SERVICE_ENABLED` required for phased rollout; existing unauthenticated endpoints remain functional during phase 1
- RSA private key must reside in a secrets manager (not in source or environment variables)
- Key rotation period: 90 days (operational constraint, not just recommendation)

**Explicit Out-of-Scope (v1.0)**
- OAuth2/OIDC federation
- Multi-factor authentication
- Role-based access control (RBAC)
- Social login providers

---

## Risk Inventory

**RISK-1: JWT Private Key Compromise**  
**Severity**: High  
**Probability**: Low  
**Description**: Compromise of the RS256 private key allows an attacker to forge arbitrary valid access tokens, bypassing all authentication.  
**Mitigation**: Use RS256 asymmetric keys with the private key stored in a secrets manager; implement automatic key rotation every 90 days; public key exposed for out-of-band verification.  
**Residual Gap**: No key revocation / emergency rotation procedure is specified for active breach scenarios.

---

**RISK-2: Refresh Token Replay Attack**  
**Severity**: High  
**Probability**: Medium  
**Description**: A stolen refresh token, if used before the legitimate client, can hijack a session. Without replay detection the attack is silent.  
**Mitigation**: Implement refresh token rotation — each use invalidates the previous token and issues a new one. On detection of reuse of a revoked token, invalidate all tokens for that user.  
**Residual Gap**: The window between token theft and first legitimate use remains exploitable; no anomaly alerting on rapid token rotation is specified.

---

**RISK-3: bcrypt Cost Factor Becoming Insufficient**  
**Severity**: Medium  
**Probability**: Low  
**Description**: Hardware improvements may reduce bcrypt cost-12 to below acceptable cracking resistance over the service lifetime.  
**Mitigation**: Make cost factor configurable; review annually against OWASP recommendations; documented migration path to Argon2id.  
**Residual Gap**: No automated alerting or scheduled review process is defined to trigger the review.

---

*Additional risks surfaced by gap analysis (not in spec Risk Assessment table):*

**RISK-4: No Progressive Account Lockout Policy (from GAP-1)**  
**Severity**: Medium  
**Probability**: Medium  
**Description**: Rate limiting (5/minute/IP) does not prevent slow brute-force or distributed attacks. An explicit lockout policy after N consecutive failures is absent.  
**Mitigation**: Extend FR-AUTH.1 to include progressive lockout with configurable threshold; add GAP-1 resolution to v1.0 scope.

**RISK-5: Token State on User Deletion (from GAP-3)**  
**Severity**: Medium  
**Probability**: Low  
**Description**: Active refresh tokens for a deleted user are not invalidated, allowing continued API access post-deletion.  
**Mitigation**: Add a user-deletion hook that cascades refresh token revocation; defer to v1.1 only if deletion is not a v1.0 use case.

---

## Dependency Inventory

| # | Dependency | Type | Used By | Notes |
|---|------------|------|---------|-------|
| 1 | `jsonwebtoken` library | External library | `jwt-service.ts` | JWT signing/verification with RS256; must validate library is actively maintained and CVE-free |
| 2 | `bcrypt` library | External library | `password-hasher.ts` | Password hashing; cost factor 12 |
| 3 | RSA key pair (secrets manager) | External infrastructure | `jwt-service.ts` | Private key for signing; public key for verification; secrets manager unspecified (AWS Secrets Manager, Vault, etc.) |
| 4 | Email service | External service | `auth-service.ts` (FR-AUTH.5) | Required for password reset flow; provider completely unspecified — interface, retry policy, and failure handling undefined |
| 5 | User database table | Internal database | FR-AUTH.1, FR-AUTH.2, FR-AUTH.4, FR-AUTH.5 | Created by migration `003-auth-tables.ts`; schema defined in spec (UserRecord interface) |
| 6 | RefreshToken database table | Internal database | FR-AUTH.3 | Created by migration `003-auth-tables.ts`; schema defined in spec (RefreshTokenRecord interface) |
| 7 | k6 + APM tooling | Testing / observability | NFR-AUTH.1, NFR-AUTH.2 | Load testing and production latency monitoring; tooling selection not constrained beyond "k6" and "production APM" |

---

## Success Criteria

| # | Criterion | Source | Threshold | Measurement Method |
|---|-----------|--------|-----------|-------------------|
| SC-1 | Authentication endpoint p95 latency | NFR-AUTH.1 | < 200ms under normal load | k6 load test; production APM dashboard |
| SC-2 | Service availability | NFR-AUTH.2 | ≥ 99.9% uptime | Health check monitoring; PagerDuty incident log |
| SC-3 | Password hash timing | NFR-AUTH.3 | ≈ 250ms per hash (cost factor 12) | Unit benchmark test verifying cost factor |
| SC-4 | Login rate limiting enforced | FR-AUTH.1 AC-4 | ≤ 5 attempts/minute/IP before rejection | Integration test: 6th attempt within 60s → 429 |
| SC-5 | Token TTLs correct | FR-AUTH.1 AC-1 / FR-AUTH.3 AC-1 | Access token: 15min; Refresh token: 7 days | JWT decode in unit tests; expiry assertions |
| SC-6 | Password policy enforced | FR-AUTH.2 AC-3 | Min 8 chars, ≥1 upper, ≥1 lower, ≥1 digit | Unit + integration tests with boundary inputs |
| SC-7 | Reset token TTL | FR-AUTH.5 AC-1 | 1-hour TTL; expired token returns 400 | Integration test: attempt use after 1 hour |
| SC-8 | Replay detection triggers full revocation | FR-AUTH.3 AC-3 | Reuse of rotated refresh token → all user tokens invalidated | Integration test with token reuse scenario |

---

## Open Questions

**OQ-1 (OI-1): Password Reset Email Delivery Mode**  
Should reset emails be dispatched synchronously within the request lifecycle or via a message queue?  
**Impact**: Synchronous dispatch simplifies implementation but ties endpoint latency to email provider availability; async queue adds infrastructure but improves resilience and latency.  
**Resolution Target**: Sprint planning for v1.0  
**Blocking**: FR-AUTH.5 implementation

---

**OQ-2 (OI-2): Maximum Active Refresh Tokens Per User**  
What is the maximum number of concurrent refresh tokens a single user may hold?  
**Impact**: Affects multi-device support (unlimited = one token per device/session), storage capacity planning for the RefreshToken table, and the blast radius of a replay attack triggering full revocation.  
**Resolution Target**: Architecture review meeting  
**Blocking**: FR-AUTH.3 implementation; RefreshToken table sizing

---

**OQ-3 (GAP-1): Account Lockout Policy**  
FR-AUTH.1 specifies rate limiting (5/minute/IP) but no progressive account lockout after N consecutive failed attempts for a given user account. Is lockout policy in or out of scope for v1.0?  
**Impact**: Without lockout, distributed brute-force attacks (multiple source IPs, same target account) bypass rate limiting entirely.  
**Severity**: Medium (partially mitigated but not resolved by current spec)

---

**OQ-4 (GAP-2): Authentication Audit Logging**  
No NFR or functional requirement specifies audit logging for authentication events (login success/failure, token refresh, password reset, account lockout).  
**Impact**: Compliance (SOC 2, GDPR incident response) and forensic investigation capability; absence means security events are untracked.  
**Severity**: Low — deferred to v1.1 per gap analysis, but should be explicitly confirmed as out of scope for v1.0

---

**OQ-5 (GAP-3): Token Revocation on User Deletion**  
There is no requirement for invalidating active refresh tokens when a user account is deleted.  
**Impact**: A deleted user's active session tokens remain valid until TTL expiry (up to 7 days).  
**Severity**: Medium — should be confirmed as a v1.1 item or addressed in FR-AUTH scope

---

**OQ-6: Email Service Provider and Failure Handling**  
The email service dependency for FR-AUTH.5 is described only as "external." The specific provider, interface contract, retry behavior on delivery failure, and SLA are entirely unspecified.  
**Impact**: If the email service is unavailable, the password reset flow silently fails; no fallback or user-visible error behavior is defined.  
**Blocking**: FR-AUTH.5 implementation

---

**OQ-7: Secrets Manager for RSA Key Pair**  
The RSA private key must be stored in a secrets manager, but no specific platform is identified (AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager, etc.).  
**Impact**: Key injection mechanism into `jwt-service.ts` at runtime differs materially across providers.  
**Blocking**: `jwt-service.ts` implementation and deployment pipeline

---

**OQ-8: Concurrent Refresh Token Rotation Race Condition**  
The spec does not address the case where two clients simultaneously submit the same valid refresh token (e.g., after a network retry). One request will succeed and rotate the token; the second will encounter a now-revoked token and trigger full user session invalidation — logging out a legitimate user.  
**Impact**: Could cause false-positive session invalidation in high-latency or mobile network environments.  
**Severity**: Medium — requires either idempotency window or documented accepted behavior
