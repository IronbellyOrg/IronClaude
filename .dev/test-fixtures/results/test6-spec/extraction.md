---
spec_source: test-spec-user-auth.compressed.md
generated: 2026-04-20T00:00:00Z
generator: requirements-extraction-agent
functional_requirements: 5
nonfunctional_requirements: 3
total_requirements: 8
complexity_score: 0.6
complexity_class: MEDIUM
domains_detected: [backend, security, database]
risks_identified: 3
dependencies_identified: 5
success_criteria_count: 8
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 68.0, started_at: "2026-04-20T20:29:35.197579+00:00", finished_at: "2026-04-20T20:30:43.206882+00:00"}
---

## Functional Requirements

### FR-AUTH.1: User Login
**Endpoint**: `POST /auth/login`
**Description**: Authenticate users via email and password, returning JWT access token and refresh token upon successful credential verification.
**Acceptance Criteria**:
- Valid credentials → 200 with access_token (15min TTL) and refresh_token (7d TTL)
- Invalid credentials → 401 without revealing whether email or password was incorrect
- Locked account → 403 indicating account suspension
- Rate-limit login attempts to 5 per minute per IP address
**Dependencies**: PasswordHasher, TokenManager, User database table

### FR-AUTH.2: User Registration
**Endpoint**: `POST /auth/register` (inferred from `/auth/*` route group)
**Description**: Register new users with input validation, creating a user record with securely hashed password.
**Acceptance Criteria**:
- Valid data (email, password, display name) → 201 with user profile
- Already-registered email → 409 conflict
- Password policy: minimum 8 characters, at least one uppercase, one lowercase, one digit
- Email format validation before registration
**Dependencies**: PasswordHasher, User database table

### FR-AUTH.3: Token Refresh
**Endpoint**: `POST /auth/refresh` (inferred from `/auth/*` route group)
**Description**: Issue and refresh JWT tokens using valid refresh token without re-entering credentials.
**Acceptance Criteria**:
- Valid refresh token → new access_token and rotated refresh_token
- Expired refresh token → 401 (re-authentication required)
- Previously-rotated (revoked) refresh token → invalidate all tokens for user (replay detection)
- Store refresh token hashes in database for revocation support
**Dependencies**: TokenManager, JwtService, RefreshToken database table

### FR-AUTH.4: Profile Retrieval
**Endpoint**: `GET /auth/me`
**Description**: Provide authenticated user profile retrieval when presented with valid access token.
**Acceptance Criteria**:
- Valid Bearer access_token → user profile (id, email, display_name, created_at)
- Expired or invalid token → 401
- Must not return sensitive fields (password_hash, refresh_token_hash)
**Dependencies**: TokenManager, User database table

### FR-AUTH.5: Password Reset
**Endpoint**: `POST /auth/password-reset` (inferred from `/auth/*` route group)
**Description**: Support secure password reset flow with time-limited reset tokens.
**Acceptance Criteria**:
- Registered email → generate password reset token (1-hour TTL) and dispatch reset email
- Valid reset token → allow setting new password and invalidate reset token
- Expired or invalid reset token → 400 with appropriate error message
- Invalidate all existing sessions (refresh tokens) upon successful reset
**Dependencies**: TokenManager, PasswordHasher, Email service (external)

## Non-Functional Requirements

### NFR-AUTH.1: Authentication Endpoint Response Time
**Target**: < 200ms p95 under normal load
**Measurement**: Load testing with k6; monitor p95 latency in production APM
**Domain**: Performance

### NFR-AUTH.2: Service Availability
**Target**: 99.9% uptime (< 8.76 hours downtime/year)
**Measurement**: Uptime monitoring via health check endpoint; PagerDuty alerting
**Domain**: Reliability

### NFR-AUTH.3: Password Hashing Security
**Target**: bcrypt cost factor 12 (approx. 250ms per hash)
**Measurement**: Unit test verifying cost factor; benchmark test for hash timing
**Domain**: Security

## Complexity Assessment

**complexity_score**: 0.6
**complexity_class**: MEDIUM

**Scoring Rationale**:
- **Scope (0.6)**: 5 functional requirements spanning registration, login, refresh, profile, reset — moderate surface area
- **Security sensitivity (0.8)**: Cryptographic primitives (bcrypt, RS256 JWT), key management, replay detection
- **Component count (0.5)**: 4 new modules + 3 modified files + 2 database tables
- **Integration points (0.5)**: External email service, database, middleware pipeline
- **Data model complexity (0.4)**: 3 interfaces with straightforward relationships
- **Risk profile (0.7)**: High-impact risks around token compromise and replay attacks
- **Testability (0.3)**: Clear boundaries, injectable components, pure utilities
- Overall aligns with spec-declared MEDIUM class

## Architectural Constraints

1. **Token format mandate**: JWT with RS256 asymmetric signing (not HS256/opaque tokens)
2. **Password hashing mandate**: bcrypt with cost factor 12 (not Argon2id/scrypt)
3. **Token storage constraint**: Access token in memory, refresh token in httpOnly cookie (no localStorage/sessionStorage)
4. **Session strategy**: Stateless JWT with refresh rotation (no server-side session store)
5. **Layered architecture**: AuthService → TokenManager → JwtService; PasswordHasher as leaf utility
6. **Dependency injection**: All components must be injectable and independently testable
7. **Key storage**: Private RSA key stored in secrets manager with 90-day rotation cadence
8. **Feature flag gating**: `AUTH_SERVICE_ENABLED` controls routing for rollback capability
9. **Backwards compatibility**: Additive only; existing unauthenticated endpoints remain functional during rollout
10. **Migration reversibility**: Database migrations must include down-migration scripts
11. **TypeScript implementation**: All new files use `.ts` extension (per file table)
12. **Route namespace**: All endpoints under `/auth/*` route group

## Component Inventory

| ID | Name | Source File | Role | Dependencies | Source Reference |
|---|---|---|---|---|---|
| COMP-001 | AuthService | `src/auth/auth-service.ts` | Core authentication orchestrator; coordinates login, register, refresh, and reset flows | TokenManager, PasswordHasher, User repository | §4.1 |
| COMP-002 | TokenManager | `src/auth/token-manager.ts` | JWT lifecycle management; issues, refreshes, and revokes token pairs | JwtService, RefreshToken repository | §4.1 |
| COMP-003 | JwtService | `src/auth/jwt-service.ts` | Low-level JWT signing and verification using RS256 | `jsonwebtoken` library, RSA key pair | §4.1 |
| COMP-004 | PasswordHasher | `src/auth/password-hasher.ts` | bcrypt password hashing and comparison with configurable cost factor | `bcrypt` library | §4.1 |
| COMP-005 | AuthMiddleware | `src/middleware/auth-middleware.ts` | Bearer token extraction and verification in request pipeline | TokenManager | §4.2 |
| COMP-006 | RoutesIndex | `src/routes/index.ts` | Registers `/auth/*` route group | AuthService, AuthMiddleware | §4.2 |
| COMP-007 | AuthTablesMigration | `src/database/migrations/003-auth-tables.ts` | Creates users and refresh_tokens database tables | Database migration framework | §4.2 |
| COMP-008 | UserRepository | (inferred) | Persistence layer for UserRecord CRUD | Database, UserRecord | §4.1 (referenced) |
| COMP-009 | RefreshTokenRepository | (inferred) | Persistence layer for RefreshTokenRecord CRUD | Database, RefreshTokenRecord | §4.1 (referenced) |
| COMP-010 | EmailService | (external) | Dispatches password reset emails | External integration | §3 FR-AUTH.5 |
| DM-001 | UserRecord | (embedded in auth schema) | User persistence model | — | §4.5 |
| DM-002 | RefreshTokenRecord | (embedded in auth schema) | Refresh token persistence model with FK to UserRecord | UserRecord | §4.5 |
| DM-003 | AuthTokenPair | (response DTO) | Token pair response returned from login/refresh endpoints | — | §4.5 |

### Data Model Field Details

**DM-001 UserRecord**:
- `id: string` (UUID v4)
- `email: string` (Unique, indexed)
- `display_name: string`
- `password_hash: string` (bcrypt hash)
- `is_locked: boolean` (Account suspension flag)
- `created_at: Date`
- `updated_at: Date`

**DM-002 RefreshTokenRecord**:
- `id: string` (UUID v4)
- `user_id: string` (FK to UserRecord.id)
- `token_hash: string` (SHA-256 hash of refresh token)
- `expires_at: Date`
- `revoked: boolean`
- `created_at: Date`

**DM-003 AuthTokenPair**:
- `access_token: string` (JWT, 15-minute TTL)
- `refresh_token: string` (Opaque token, 7-day TTL)

## Risk Inventory

1. **RISK-1: JWT secret key compromise allows forged tokens** — Severity: HIGH (Low probability × High impact). Mitigation: RS256 asymmetric keys; private key in secrets manager; 90-day rotation cadence.
2. **RISK-2: Refresh token replay attack after token theft** — Severity: HIGH (Medium probability × High impact). Mitigation: Refresh token rotation with replay detection; revoke all user tokens on suspicious reuse.
3. **RISK-3: bcrypt cost factor insufficient for future hardware** — Severity: MEDIUM (Low probability × Medium impact). Mitigation: Configurable cost factor; annual OWASP review; documented migration path to Argon2id.
4. **RISK-4 (GAP-1): No account lockout policy after N failed attempts** — Severity: MEDIUM. Mitigation: Rate-limiting in FR-AUTH.1 partially addresses; progressive lockout deferred to v1.1.
5. **RISK-5 (GAP-2): Audit logging for authentication events not specified** — Severity: LOW. Mitigation: Deferred to v1.1; does not block core functionality.
6. **RISK-6 (GAP-3): Token revocation on user deletion not addressed** — Severity: MEDIUM. Mitigation: Deferred to v1.1; architect review pending.

## Dependency Inventory

1. **`jsonwebtoken` (npm)** — JWT signing/verification; used by JwtService (COMP-003)
2. **`bcrypt` (npm)** — Password hashing; used by PasswordHasher (COMP-004)
3. **RSA key pair** — Cryptographic material for RS256 signing; stored in secrets manager
4. **Email service (external)** — Dispatches password reset emails for FR-AUTH.5
5. **Database (users table)** — Persistent storage for UserRecord
6. **Database (refresh_tokens table)** — Persistent storage for RefreshTokenRecord
7. **Secrets manager** — Stores private RSA key with rotation support
8. **Rate-limiting infrastructure** — Enforces 5/min/IP on login endpoint
9. **APM/uptime monitoring** — Measures NFR-AUTH.1 and NFR-AUTH.2
10. **PagerDuty** — Alerting backbone for NFR-AUTH.2

## Success Criteria

| ID | Criterion | Acceptance Threshold | Source |
|---|---|---|---|
| SC-1 | Login endpoint latency | p95 < 200ms under normal load | NFR-AUTH.1 |
| SC-2 | Service uptime | ≥ 99.9% (≤ 8.76h downtime/year) | NFR-AUTH.2 |
| SC-3 | bcrypt cost factor | Exactly 12 (≈250ms per hash) | NFR-AUTH.3 |
| SC-4 | Login rate limiting | ≤ 5 attempts/minute/IP enforced | FR-AUTH.1 |
| SC-5 | Token TTLs | access=15min, refresh=7d, reset=1h | FR-AUTH.1, FR-AUTH.5 |
| SC-6 | Password policy enforcement | 8+ chars, upper, lower, digit all required | FR-AUTH.2 |
| SC-7 | Refresh token replay detection | Reused rotated token triggers revocation of all user tokens | FR-AUTH.3 |
| SC-8 | End-to-end lifecycle test passes | Register → login → /auth/me → refresh → reset → login with new password all succeed | §8.3 E2E Scenario |

## Open Questions

1. **OI-1**: Should password reset emails be sent synchronously or via a message queue? (Impact: latency of reset endpoint and system resilience; resolution target: sprint planning for v1.0)
2. **OI-2**: What is the maximum number of active refresh tokens per user? (Impact: storage requirements and multi-device support; resolution target: architecture review meeting)
3. **OI-3 (derived)**: What is the exact endpoint path for registration? Spec references `/auth/*` route group but does not name the path explicitly.
4. **OI-4 (derived)**: What is the exact endpoint path for token refresh?
5. **OI-5 (derived)**: What is the exact endpoint path for password reset request vs. password reset confirmation (two-step flow)?
6. **OI-6 (derived from GAP-1)**: What progressive lockout policy should apply after N failed login attempts beyond rate-limiting?
7. **OI-7 (derived from GAP-2)**: Which authentication events require audit logging, and where do logs persist?
8. **OI-8 (derived from GAP-3)**: How are refresh tokens revoked when a user account is deleted?
9. **OI-9 (derived)**: How is the RSA key pair rotated in production without invalidating active tokens (grace period / dual-key support)?
10. **OI-10 (derived)**: What email service vendor/protocol is used for password reset dispatch (SMTP, SendGrid, SES)?
