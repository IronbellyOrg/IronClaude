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
pipeline_diagnostics: {elapsed_seconds: 93.0, started_at: "2026-04-15T18:37:43.841157+00:00", finished_at: "2026-04-15T18:39:16.854018+00:00"}
---

## Functional Requirements

### FR-AUTH.1: User Login
**Description**: Authenticate users via email and password, returning JWT access token and refresh token upon successful credential verification.
**Endpoints**: `POST /auth/login` (Section 2.2 workflow diagram, Section 4.2 route group `/auth/*`)
**Acceptance Criteria**:
- FR-AUTH.1a: Valid email/password returns 200 with `access_token` (15min TTL) and `refresh_token` (7d TTL)
- FR-AUTH.1b: Invalid credentials return 401; must not reveal whether email or password was incorrect
- FR-AUTH.1c: Locked account returns 403 indicating account suspension
- FR-AUTH.1d: Rate-limit login attempts to 5 per minute per IP address
**Dependencies**: PasswordHasher, TokenManager, User database table

### FR-AUTH.2: User Registration
**Description**: Register new users with input validation, creating a user record with securely hashed password and returning confirmation.
**Endpoints**: Implied `POST /auth/register` (Section 4.2 route group `/auth/*`; no explicit path in spec)
**Acceptance Criteria**:
- FR-AUTH.2a: Valid registration data (email, password, display name) creates user record, returns 201 with user profile
- FR-AUTH.2b: Already-registered email returns 409 conflict
- FR-AUTH.2c: Password policy enforced: min 8 chars, at least one uppercase, one lowercase, one digit
- FR-AUTH.2d: Email format validated before registration attempt
**Dependencies**: PasswordHasher, User database table

### FR-AUTH.3: Token Refresh
**Description**: Issue and refresh JWT tokens, allowing clients to obtain new access token using valid refresh token without re-entering credentials.
**Endpoints**: Implied `POST /auth/refresh` (Section 4.2 route group `/auth/*`; no explicit path in spec)
**Acceptance Criteria**:
- FR-AUTH.3a: Valid refresh token returns new `access_token` and rotated `refresh_token`
- FR-AUTH.3b: Expired refresh token returns 401, requires re-authentication
- FR-AUTH.3c: Previously-rotated (revoked) refresh token triggers invalidation of all tokens for that user (replay detection)
- FR-AUTH.3d: Refresh token hashes stored in database for revocation support
**Dependencies**: TokenManager, JwtService, RefreshToken database table

### FR-AUTH.4: Profile Retrieval
**Description**: Provide authenticated user profile retrieval, returning current user's profile data when presented with valid access token.
**Endpoints**: `GET /auth/me` (Section 2.2 workflow diagram, with `Bearer access_token` header)
**Acceptance Criteria**:
- FR-AUTH.4a: Valid Bearer `access_token` returns user profile (id, email, display_name, created_at)
- FR-AUTH.4b: Expired or invalid token returns 401
- FR-AUTH.4c: Sensitive fields (`password_hash`, `refresh_token_hash`) excluded from response
**Dependencies**: TokenManager, User database table

### FR-AUTH.5: Password Reset
**Description**: Support secure password reset flow allowing users to request a reset link and set a new password using a time-limited token.
**Endpoints**: Implied `POST /auth/reset-password` (request) and `POST /auth/reset-password/confirm` (execute) (Section 4.2 route group `/auth/*`; no explicit paths in spec)
**Acceptance Criteria**:
- FR-AUTH.5a: Registered email triggers password reset token generation (1-hour TTL) and reset email dispatch
- FR-AUTH.5b: Valid reset token allows setting new password; token invalidated after use
- FR-AUTH.5c: Expired or invalid reset token returns 400 with appropriate error
- FR-AUTH.5d: Successful password reset invalidates all existing sessions (refresh tokens)
**Dependencies**: TokenManager, PasswordHasher, Email service (external)

## Non-Functional Requirements

### NFR-AUTH.1: Authentication Endpoint Response Time
**Target**: < 200ms p95 under normal load
**Measurement**: Load testing with k6; monitor p95 latency in production APM
**Affected FRs**: FR-AUTH.1, FR-AUTH.2, FR-AUTH.3, FR-AUTH.4, FR-AUTH.5

### NFR-AUTH.2: Service Availability
**Target**: 99.9% uptime (< 8.76 hours downtime/year)
**Measurement**: Uptime monitoring via health check endpoint; PagerDuty alerting

### NFR-AUTH.3: Password Hashing Security
**Target**: bcrypt cost factor 12 (approx. 250ms per hash)
**Measurement**: Unit test verifying cost factor; benchmark test for hash timing
**Affected FRs**: FR-AUTH.1, FR-AUTH.2, FR-AUTH.5

## Complexity Assessment

**Score**: 0.6 / **Class**: MEDIUM

| Factor | Score | Rationale |
|---|---|---|
| Component count | 0.5 | 4 new files, 3 modified files — moderate scope |
| Integration surface | 0.6 | External email service, database migrations, middleware integration |
| Security sensitivity | 0.8 | Authentication is security-critical; JWT, bcrypt, token rotation require careful implementation |
| Parallelizability | 0.4 | PasswordHasher and JwtService are independent; later components have linear dependencies |
| Domain complexity | 0.6 | Well-understood patterns (JWT, bcrypt) but replay detection and token rotation add nuance |
| Testing burden | 0.5 | 5 unit test files, 3 integration tests, 1 E2E scenario — moderate |

Weighted average: **0.6**. The security sensitivity elevates risk, but the well-defined scope and established patterns keep overall complexity in the MEDIUM band.

## Architectural Constraints

| Constraint | Source | Impact |
|---|---|---|
| JWT with RS256 signing (asymmetric) | Section 2.1 | Requires RSA key pair management; private key in secrets manager |
| bcrypt with cost factor 12 | Section 2.1 | ~250ms per hash operation; affects login/register latency budget |
| Access token in memory, refresh token in httpOnly cookie | Section 2.1 | Client-side storage strategy; affects CORS and cookie configuration |
| Stateless JWT (no server-side session store) | Section 2.1 | Horizontal scalability enabled; token revocation requires refresh-token DB check |
| Refresh token rotation with replay detection | Section 2.1, FR-AUTH.3 | All user tokens invalidated on reuse of revoked token |
| Feature flag `AUTH_SERVICE_ENABLED` for rollback | Section 9 | Routing must be conditionally enabled |
| Layered architecture: AuthService → TokenManager → JwtService | Section 2, 4.4 | Components must be injectable and independently testable |
| Implementation order: hasher/jwt → token-manager → auth-service → middleware → routes | Section 4.6 | Constrains parallelization of implementation tasks |
| TypeScript language | Section 4.1 (file extensions `.ts`) | All new and modified files are TypeScript |
| Database migration required (003-auth-tables) | Section 4.2 | Must include down-migration scripts for rollback |

## Component Inventory

### Services & Modules

| ID | Name | Path | Role | Dependencies | Source |
|---|---|---|---|---|---|
| COMP-001 | AuthService | `src/auth/auth-service.ts` | Core authentication orchestrator; coordinates login, register, refresh, and reset flows | COMP-002, COMP-004, User repository | Section 4.1 |
| COMP-002 | TokenManager | `src/auth/token-manager.ts` | JWT lifecycle management; issues, refreshes, and revokes token pairs | COMP-003, RefreshToken repository | Section 4.1 |
| COMP-003 | JwtService | `src/auth/jwt-service.ts` | Low-level JWT signing and verification using RS256 | `jsonwebtoken` library, RSA key pair | Section 4.1 |
| COMP-004 | PasswordHasher | `src/auth/password-hasher.ts` | bcrypt password hashing and comparison with configurable cost factor | `bcrypt` library | Section 4.1 |
| COMP-005 | AuthMiddleware | `src/middleware/auth-middleware.ts` | Bearer token extraction and verification in request pipeline | COMP-002 | Section 4.2 |
| COMP-006 | AuthRoutes | `src/routes/index.ts` | Register `/auth/*` route group to expose authentication endpoints | COMP-001 | Section 4.2 |
| COMP-007 | AuthMigration | `src/database/migrations/003-auth-tables.ts` | Database migration adding `users` and `refresh_tokens` tables | Database | Section 4.2 |

### Data Models (Interfaces/DTOs)

| ID | Name | Role | Fields | Source |
|---|---|---|---|---|
| DM-001 | UserRecord | Persistent user entity in database | `id: string` (UUID v4), `email: string` (unique, indexed), `display_name: string`, `password_hash: string` (bcrypt), `is_locked: boolean`, `created_at: Date`, `updated_at: Date` | Section 4.5 |
| DM-002 | RefreshTokenRecord | Persistent refresh token entity for revocation support | `id: string` (UUID v4), `user_id: string` (FK → UserRecord.id), `token_hash: string` (SHA-256), `expires_at: Date`, `revoked: boolean`, `created_at: Date` | Section 4.5 |
| DM-003 | AuthTokenPair | Response DTO for token issuance | `access_token: string` (JWT, 15min TTL), `refresh_token: string` (opaque, 7d TTL) | Section 4.5 |

## Risk Inventory

| # | Risk | Probability | Impact | Severity | Mitigation |
|---|---|---|---|---|---|
| R-1 | JWT secret key compromise allows forged tokens | Low | High | **High** | Use RS256 asymmetric keys; store private key in secrets manager; implement key rotation every 90 days |
| R-2 | Refresh token replay attack after token theft | Medium | High | **High** | Implement refresh token rotation with replay detection; revoke all user tokens on suspicious reuse |
| R-3 | bcrypt cost factor too low for future hardware | Low | Medium | **Medium** | Make cost factor configurable; review annually against OWASP recommendations; migration path to Argon2id if needed |

**From Gap Analysis** (not in formal risk table but affecting risk posture):
| # | Gap | Severity | Affected Area |
|---|---|---|---|
| GAP-1 | No account lockout policy after N failed attempts | Medium | FR-AUTH.1 (partially addressed by rate limiting) |
| GAP-2 | Audit logging for authentication events not specified | Low | NFRs |
| GAP-3 | Token revocation on user deletion not addressed | Medium | FR-AUTH.3 |

## Dependency Inventory

| # | Dependency | Type | Used By | Purpose |
|---|---|---|---|---|
| DEP-1 | `jsonwebtoken` (npm) | Library | COMP-003 (JwtService) | JWT signing and verification with RS256 |
| DEP-2 | `bcrypt` (npm) | Library | COMP-004 (PasswordHasher) | Password hashing with configurable cost factor |
| DEP-3 | Email service | External service | FR-AUTH.5 (Password Reset) | Dispatch password reset emails |
| DEP-4 | Database (users, refresh_tokens tables) | Infrastructure | COMP-001, COMP-002, COMP-007 | Persistent storage for user records and refresh token hashes |
| DEP-5 | Secrets manager | Infrastructure | COMP-003 (JwtService) | Secure storage for RSA private key |

**Testing dependencies** (non-runtime):
- k6 (load testing for NFR-AUTH.1)
- PagerDuty (alerting for NFR-AUTH.2)

## Success Criteria

| # | Criterion | Threshold | Source |
|---|---|---|---|
| SC-1 | Valid login returns 200 with access_token (15min TTL) and refresh_token (7d TTL) | Pass/Fail | FR-AUTH.1a |
| SC-2 | Invalid credentials return 401 without leaking which field was wrong | Pass/Fail | FR-AUTH.1b |
| SC-3 | Locked account returns 403 | Pass/Fail | FR-AUTH.1c |
| SC-4 | Login rate-limited to 5/min/IP | ≤ 5 successful attempts per minute per IP | FR-AUTH.1d |
| SC-5 | Valid registration returns 201 with user profile | Pass/Fail | FR-AUTH.2a |
| SC-6 | Duplicate email returns 409 | Pass/Fail | FR-AUTH.2b |
| SC-7 | Password policy enforced (8+ chars, upper, lower, digit) | Pass/Fail | FR-AUTH.2c |
| SC-8 | Email format validated | Pass/Fail | FR-AUTH.2d |
| SC-9 | Valid refresh token returns new token pair with rotation | Pass/Fail | FR-AUTH.3a |
| SC-10 | Expired refresh token returns 401 | Pass/Fail | FR-AUTH.3b |
| SC-11 | Revoked refresh token triggers full user token invalidation | Pass/Fail | FR-AUTH.3c |
| SC-12 | Refresh token hashes persisted in database | Pass/Fail | FR-AUTH.3d |
| SC-13 | Valid Bearer token returns profile (id, email, display_name, created_at) | Pass/Fail | FR-AUTH.4a |
| SC-14 | Expired/invalid token returns 401 on profile endpoint | Pass/Fail | FR-AUTH.4b |
| SC-15 | Sensitive fields excluded from profile response | Pass/Fail | FR-AUTH.4c |
| SC-16 | Password reset token generated (1h TTL) and email dispatched | Pass/Fail | FR-AUTH.5a |
| SC-17 | Valid reset token allows new password; token invalidated | Pass/Fail | FR-AUTH.5b |
| SC-18 | Expired/invalid reset token returns 400 | Pass/Fail | FR-AUTH.5c |
| SC-19 | Password reset invalidates all refresh tokens | Pass/Fail | FR-AUTH.5d |
| SC-20 | Auth endpoint p95 latency < 200ms | < 200ms | NFR-AUTH.1 |
| SC-21 | Service uptime ≥ 99.9% | < 8.76h downtime/year | NFR-AUTH.2 |
| SC-22 | bcrypt cost factor = 12 (~250ms/hash) | Cost factor 12 | NFR-AUTH.3 |

## Open Questions

| # | Question | Impact | Resolution Target | Source |
|---|---|---|---|---|
| OQ-1 | Should password reset emails be sent synchronously or via a message queue? | Affects latency of reset endpoint and system resilience; synchronous dispatch may cause timeouts under load | Sprint planning for v1.0 | OI-1, Section 11 |
| OQ-2 | What is the maximum number of active refresh tokens per user? | Affects storage requirements, multi-device support, and cleanup/eviction strategy | Architecture review meeting | OI-2, Section 11 |
| OQ-3 | What progressive lockout policy should apply after N failed login attempts? | GAP-1 is only partially mitigated by rate limiting; need threshold (e.g., lock after 10 failures) and unlock mechanism (time-based vs. admin) | v1.1 scope decision | GAP-1, Section 12 |
| OQ-4 | What audit logging format and destination for auth events? | Compliance and incident response readiness; may require structured logging infrastructure | v1.1 scope decision | GAP-2, Section 12 |
| OQ-5 | Should all tokens be revoked when a user is deleted? | Data integrity and security posture; affects user deletion flow and token validation logic | Architecture review meeting | GAP-3, Section 12 |
| OQ-6 | Exact REST paths for registration, token refresh, and password reset endpoints? | Spec names the route group `/auth/*` and shows `POST /auth/login` and `GET /auth/me` explicitly, but remaining endpoint paths are not specified | Before implementation | Sections 2.2, 4.2 |
