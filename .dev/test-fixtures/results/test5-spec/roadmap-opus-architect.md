---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
generated: "2026-04-15T00:00:00Z"
generator: "roadmap-agent/opus-4.6"
total_phases: 7
total_task_rows: 94
granularity_floor_target: 80
extraction_ids_preserved: true
---

# User Authentication Service — Project Roadmap

## 1. Executive Summary

This roadmap defines the phased delivery of a stateless JWT-based authentication service covering user login, registration, token refresh with rotation, profile retrieval, and password reset. The system uses RS256 asymmetric signing, bcrypt password hashing (cost factor 12), and refresh token rotation with replay detection.

**Complexity**: MEDIUM (0.6) — well-understood primitives (JWT, bcrypt) elevated by security sensitivity and token rotation state management.

**Key architectural decisions**:
- RS256 asymmetric JWT signing (AC-1) with secrets-manager-stored private keys (AC-6)
- Stateless access tokens, server-side refresh token hash tracking (AC-4, FR-AUTH.3d)
- Feature-flagged rollout with full down-migration support (AC-8, AC-9)
- Dependency-injected components for independent testability (AC-5)

**Scope boundaries**: OAuth/OIDC, MFA, and RBAC are explicitly deferred to v2.0. Audit logging (GAP-2) and token revocation on user deletion (GAP-3) are deferred to v1.1.

**Open questions** (OQ-1 through OQ-7) should be resolved before or during Phase 1; this roadmap flags where each decision impacts implementation.

---

## 2. Integration Points & Wiring Mechanisms

Before the phased plan, this section enumerates every dispatch/wiring mechanism that must be explicitly built.

### 2.1 Dependency Injection Container

- **Named Artifact**: DI container or factory module (manual constructor injection per AC-5)
- **Wired Components**: PasswordHasher → AuthService; JwtService → TokenManager; TokenManager → AuthService, AuthMiddleware; UserRepository → AuthService; RefreshTokenRepository → TokenManager; EmailDispatcher → AuthService
- **Owning Phase**: Phase 2 (AC-5 task creates the wiring scaffold)
- **Consumed By**: Phases 3, 4, 5 (each phase registers new components into the container)

### 2.2 Route Registration

- **Named Artifact**: `AuthRoutes` module registering `/auth/*` route group (COMP-006)
- **Wired Components**: AuthService (handler logic), AuthMiddleware (protected route guard), RateLimiter (login endpoint)
- **Owning Phase**: Phase 5 (COMP-006 task)
- **Consumed By**: Phase 5 (API-001 through API-006 endpoint tasks), Phase 6 (AC-10 opt-in toggle)

### 2.3 Middleware Chain

- **Named Artifact**: Express/framework middleware pipeline
- **Wired Components**: RateLimiter (COMP-011) on `/auth/login`; AuthMiddleware (COMP-005) on `/auth/profile`
- **Owning Phase**: Phase 5
- **Consumed By**: Phase 5 (route handlers), Phase 6 (GAP-1 lockout extension)

### 2.4 Feature Flag Gate

- **Named Artifact**: `AUTH_SERVICE_ENABLED` feature flag (AC-8)
- **Wired Components**: AuthRoutes conditional registration
- **Owning Phase**: Phase 1 (flag infrastructure), Phase 5 (wiring into route registration)
- **Consumed By**: Phase 7 (rollback validation)

### 2.5 Migration Registry

- **Named Artifact**: Migration runner sequence in `src/database/migrations/`
- **Wired Components**: MIG-001 (users), MIG-002 (refresh_tokens), MIG-003 (password_reset_tokens)
- **Owning Phase**: Phase 1 (COMP-007)
- **Consumed By**: Phase 2 (repositories depend on tables existing)

---

## 3. Phased Implementation Plan

### Phase 1: Infrastructure & Data Layer

**Objective**: Provision infrastructure, define data schemas, create migration scripts, and establish foundational operational mechanisms.

**Milestone**: All database tables created, secrets manager configured with RSA key pair, feature flag operational, health check responding.

**Resolves before proceeding**: OQ-3 (database engine), OQ-7 (RSA key size).

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 1 | DEP-4 | Provision relational database instance | Infrastructure | — | Database engine selected (OQ-3 resolved), connection pool configured, connectivity verified from application runtime | M | P0 |
| 2 | DEP-5 | Provision secrets manager and store RSA key pair | Infrastructure | — | Secrets manager instance running; RSA key pair (size per OQ-7 resolution, minimum 2048-bit) stored; application can retrieve private key at runtime | M | P0 |
| 3 | DEP-1 | Install and pin `jsonwebtoken` npm dependency | Dependencies | — | `jsonwebtoken` listed in package.json with pinned version; `npm audit` shows no known vulnerabilities for this package | S | P0 |
| 4 | DEP-2 | Install and pin `bcrypt` npm dependency | Dependencies | — | `bcrypt` listed in package.json with pinned version; native binding compiles successfully in CI environment | S | P0 |
| 5 | DM-001 | Define Users table schema | Data Model | DEP-4 | Schema: id (UUID PK), email (varchar, unique index), display_name (varchar), password_hash (varchar), is_locked (boolean, default false), created_at (timestamptz, default now), updated_at (timestamptz, default now) | M | P0 |
| 6 | DM-002 | Define RefreshTokens table schema | Data Model | DEP-4, DM-001 | Schema: id (UUID PK), user_id (UUID FK → users.id ON DELETE CASCADE), token_hash (varchar, SHA-256), expires_at (timestamptz), revoked (boolean, default false), created_at (timestamptz, default now); index on (user_id, revoked) | M | P0 |
| 7 | DM-003 | Define PasswordResetTokens table schema | Data Model | DEP-4, DM-001 | Schema: id (UUID PK), user_id (UUID FK → users.id ON DELETE CASCADE), token_hash (varchar, SHA-256), expires_at (timestamptz), used (boolean, default false), created_at (timestamptz, default now); index on (token_hash) | M | P0 |
| 8 | MIG-001 | Create Users table up and down migration | Database | DM-001 | Up migration creates users table matching DM-001 schema; down migration drops users table; both scripts execute without error; idempotent guard present | M | P0 |
| 9 | MIG-002 | Create RefreshTokens table up and down migration | Database | DM-002, MIG-001 | Up migration creates refresh_tokens table matching DM-002 schema; down migration drops table; foreign key constraint to users verified | M | P0 |
| 10 | MIG-003 | Create PasswordResetTokens table up and down migration | Database | DM-003, MIG-001 | Up migration creates password_reset_tokens table matching DM-003 schema; down migration drops table; foreign key constraint to users verified | M | P0 |
| 11 | COMP-007 | Implement AuthMigration module at `src/database/migrations/003-auth-tables.ts` | Database | MIG-001, MIG-002, MIG-003 | Migration runner executes MIG-001, MIG-002, MIG-003 in order; rollback executes down-migrations in reverse order; registered in migration sequence | M | P0 |
| 12 | AC-6 | Configure RSA private key retrieval from secrets manager | Security | DEP-5 | JwtService configuration reads RSA private key from secrets manager at startup; no key material in source code, config files, or environment variables; startup fails with clear error if key unavailable | M | P0 |
| 13 | AC-8 | Implement AUTH_SERVICE_ENABLED feature flag | Configuration | — | Feature flag toggleable at runtime; when disabled, auth routes return 503; flag state queryable via health check | S | P0 |
| 14 | AC-9 | Verify all migrations include down-migration scripts | Database | MIG-001, MIG-002, MIG-003 | Each migration file contains both `up()` and `down()` functions; down migrations tested by running up then down then up again successfully | S | P0 |
| 15 | AC-4 | Document and validate stateless JWT architecture | Architecture | — | Architecture decision record confirms no server-side session store; access token validation uses only the public key and token claims; no session lookup on request path | S | P1 |
| 16 | OPS-001 | Implement health check endpoint | Operations | DEP-4 | `GET /health` returns 200 with database connectivity status, feature flag state, and uptime; response time < 50ms | S | P0 |

**Phase 1 total: 16 tasks**

---

### Phase 2: Core Crypto & Repository Components

**Objective**: Build the foundational crypto primitives (PasswordHasher, JwtService) and data access layers (repositories) that all higher-level services depend on. These components are independent and can be built in parallel.

**Milestone**: PasswordHasher hashes and verifies passwords at bcrypt cost 12. JwtService signs and verifies RS256 JWTs. Both repositories perform CRUD against their tables. All components are injectable. Unit tests pass.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 17 | COMP-001 | Implement PasswordHasher at `src/auth/password-hasher.ts` | Auth | DEP-2 | Exports `hash(password): Promise<string>` and `compare(password, hash): Promise<boolean>`; constructor accepts configurable cost factor; injectable via interface | M | P0 |
| 18 | AC-2 | Configure bcrypt cost factor 12 as default | Auth | COMP-001 | Default cost factor is 12; unit test verifies hash timing is ~250ms ±100ms; cost factor overridable via constructor parameter | S | P0 |
| 19 | COMP-002 | Implement JwtService at `src/auth/jwt-service.ts` | Auth | DEP-1, DEP-5, AC-6 | Exports `sign(payload, expiresIn): string` and `verify(token): JwtPayload`; uses RS256 algorithm exclusively; retrieves RSA key pair from secrets manager; injectable via interface | M | P0 |
| 20 | AC-1 | Enforce RS256 signing algorithm in JwtService | Auth | COMP-002 | Algorithm parameter hardcoded to RS256; unit test confirms HS256 tokens are rejected by verify; sign output contains `"alg":"RS256"` in header | S | P0 |
| 21 | AC-3 | Document token storage strategy for clients | Auth | — | Documentation specifies: access tokens stored in client memory only (never localStorage/cookies); refresh tokens stored in httpOnly secure cookies; implementation guide for frontend consumers | S | P1 |
| 22 | COMP-008 | Implement UserRepository | Data Access | DM-001, COMP-007 | Exports `findByEmail(email)`, `findById(id)`, `create(userData)`, `updatePassword(id, hash)`, `setLocked(id, locked)`; all methods return typed results; injectable via interface | M | P0 |
| 23 | COMP-009 | Implement RefreshTokenRepository | Data Access | DM-002, COMP-007 | Exports `create(userId, tokenHash, expiresAt)`, `findByHash(hash)`, `revokeByHash(hash)`, `revokeAllForUser(userId)`; injectable via interface | M | P0 |
| 24 | AC-5 | Establish dependency injection wiring scaffold | Architecture | COMP-001, COMP-002, COMP-008, COMP-009 | All Phase 2 components registered in DI container or factory; each component constructable with explicit dependency arguments; no module-level singletons; integration test verifies wiring | M | P0 |
| 25 | TEST-001 | Write PasswordHasher unit test suite | Testing | COMP-001, AC-2 | Tests cover: hash produces bcrypt format string; compare returns true for matching password; compare returns false for wrong password; cost factor 12 verified in hash output; timing benchmark within 150-350ms range | M | P0 |
| 26 | TEST-002 | Write JwtService unit test suite | Testing | COMP-002, AC-1 | Tests cover: sign produces valid JWT string; verify decodes correct payload; verify rejects expired token; verify rejects HS256 token; verify rejects tampered token; RS256 algorithm in header | M | P0 |
| 27 | TEST-003 | Write UserRepository unit test suite | Testing | COMP-008 | Tests cover: create inserts record; findByEmail returns user; findByEmail returns null for missing; findById returns user; updatePassword changes hash; setLocked toggles is_locked; duplicate email throws | M | P1 |
| 28 | TEST-004 | Write RefreshTokenRepository unit test suite | Testing | COMP-009 | Tests cover: create inserts record; findByHash returns token; revokeByHash sets revoked=true; revokeAllForUser revokes all user tokens; findByHash returns null for revoked token | M | P1 |
| 29 | NFR-AUTH.3 | Benchmark password hashing at cost factor 12 | Testing | COMP-001, AC-2 | Benchmark confirms bcrypt cost factor 12 produces ~250ms hash time; results documented; test fails if hash time < 100ms (cost too low) or > 500ms (environment issue) | S | P0 |

**Phase 2 total: 13 tasks**

---

### Phase 3: Token Management

**Objective**: Build the TokenManager that orchestrates JWT lifecycle — issuance, refresh with rotation, and revocation with replay detection.

**Milestone**: TokenManager issues access/refresh token pairs, rotates refresh tokens on use, detects replay attacks and triggers full user revocation. Unit and integration tests pass.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 30 | COMP-003 | Implement TokenManager at `src/auth/token-manager.ts` | Auth | COMP-002, COMP-009 | Exports `issueTokenPair(userId)`, `refreshTokens(refreshToken)`, `revokeAllUserTokens(userId)`, `verifyAccessToken(token)`; depends on JwtService and RefreshTokenRepository; injectable via interface | L | P0 |
| 31 | FR-AUTH.3 | Implement token refresh flow in TokenManager | Auth | COMP-003 | `refreshTokens()` accepts a raw refresh token, validates it, issues new token pair, and handles all error cases (expired, revoked, replayed) | L | P0 |
| 32 | FR-AUTH.3a | Implement refresh token rotation on successful refresh | Auth | FR-AUTH.3, COMP-009 | On valid refresh: new access_token (15min TTL) and new refresh_token (7d TTL) issued; old refresh token hash marked revoked in database; SC-9 validated | M | P0 |
| 33 | FR-AUTH.3b | Implement expired refresh token rejection | Auth | FR-AUTH.3 | Expired refresh token returns 401 status indicator; no new tokens issued; SC-10 validated | S | P0 |
| 34 | FR-AUTH.3c | Implement replay detection with full user token revocation | Auth | FR-AUTH.3, COMP-009 | When a previously-rotated (revoked) refresh token is presented: all refresh tokens for that user are revoked via `revokeAllForUser()`; returns 401; SC-11 validated | M | P0 |
| 35 | FR-AUTH.3d | Store refresh token hashes as SHA-256 in database | Auth | COMP-003, COMP-009 | Raw refresh tokens are never stored; only SHA-256 hashes persisted in RefreshToken table; unit test verifies hash format; SC-12 validated | S | P0 |
| 36 | AC-7 | Implement RSA key rotation support (90-day cycle) | Auth | COMP-002, DEP-5 | JwtService supports key versioning via `kid` (key ID) header claim; verify accepts tokens signed by current or previous key; rotation runbook documented | M | P1 |
| 37 | RISK-2 | Validate refresh token replay attack mitigation | Security | FR-AUTH.3c | Integration test: issue tokens → refresh (rotates) → replay old refresh token → verify all user tokens revoked; test passes consistently | M | P0 |
| 38 | TEST-005 | Write TokenManager unit test suite | Testing | COMP-003, FR-AUTH.3 | Tests cover: issueTokenPair returns both tokens with correct TTLs; refreshTokens rotates tokens; refreshTokens rejects expired; refreshTokens detects replay; revokeAllUserTokens clears all; token hashes are SHA-256 | L | P0 |
| 39 | TEST-006 | Write token rotation integration test suite | Testing | COMP-003, COMP-009 | Integration tests against real database: full rotation lifecycle; replay detection with database state verification; concurrent refresh handling | M | P0 |

**Phase 3 total: 10 tasks**

---

### Phase 4: Authentication Service & Email Integration

**Objective**: Build the AuthService orchestrator that coordinates login, registration, profile retrieval, and password reset flows using the underlying crypto and token components.

**Milestone**: All five functional requirements (FR-AUTH.1 through FR-AUTH.5) implemented with acceptance criteria passing at the service layer. Email dispatch integrated.

**Resolves before proceeding**: OQ-1 (sync vs. async email dispatch), OQ-2 (max refresh tokens per user).

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 40 | COMP-004 | Implement AuthService orchestrator at `src/auth/auth-service.ts` | Auth | COMP-001, COMP-003, COMP-008, COMP-010 | Exports `login(email, password)`, `register(email, password, displayName)`, `getProfile(userId)`, `requestPasswordReset(email)`, `confirmPasswordReset(token, newPassword)`; depends on PasswordHasher, TokenManager, UserRepository, EmailDispatcher; injectable via interface | L | P0 |
| 41 | FR-AUTH.1 | Implement login flow in AuthService | Auth | COMP-004, COMP-001, COMP-003, COMP-008 | `login()` retrieves user by email, verifies password via PasswordHasher, checks lock status, issues token pair via TokenManager; returns tokens or appropriate error | M | P0 |
| 42 | FR-AUTH.1a | Implement successful login response (200 + tokens) | Auth | FR-AUTH.1 | Given valid email and password: return access_token with 15min TTL and refresh_token with 7d TTL; SC-1 validated | S | P0 |
| 43 | FR-AUTH.1b | Implement invalid credentials response (401 generic) | Auth | FR-AUTH.1 | Given invalid email or password: return 401 with message that does not reveal whether email or password was wrong (e.g., "Invalid credentials"); SC-2 validated | S | P0 |
| 44 | FR-AUTH.1c | Implement locked account response (403) | Auth | FR-AUTH.1, COMP-008 | Given a user with `is_locked=true`: return 403 indicating account suspension before checking password; SC-3 validated | S | P0 |
| 45 | FR-AUTH.2 | Implement registration flow in AuthService | Auth | COMP-004, COMP-001, COMP-008 | `register()` validates input, checks email uniqueness, hashes password, creates user record, returns user profile | M | P0 |
| 46 | FR-AUTH.2a | Implement successful registration response (201) | Auth | FR-AUTH.2 | Given valid email, password, display_name: create user record in database; return 201 with user profile (id, email, display_name, created_at); SC-5 validated | S | P0 |
| 47 | FR-AUTH.2b | Implement duplicate email rejection (409) | Auth | FR-AUTH.2, COMP-008 | Given an already-registered email: return 409 conflict; no partial record created; SC-6 validated | S | P0 |
| 48 | FR-AUTH.2c | Implement password policy enforcement | Auth | FR-AUTH.2 | Password must be ≥8 characters with ≥1 uppercase, ≥1 lowercase, ≥1 digit; non-conforming passwords rejected with descriptive error before hashing; SC-7 validated | S | P0 |
| 49 | FR-AUTH.2d | Implement email format validation | Auth | FR-AUTH.2 | Malformed email strings rejected with 400 before database lookup; validation uses RFC 5322 compliant check; SC-8 validated | S | P0 |
| 50 | FR-AUTH.4 | Implement profile retrieval flow in AuthService | Auth | COMP-004, COMP-008 | `getProfile()` accepts userId (extracted from token by middleware), returns profile data | S | P0 |
| 51 | FR-AUTH.4a | Implement profile response schema (id, email, display_name, created_at) | Auth | FR-AUTH.4 | Response includes exactly: id, email, display_name, created_at; SC-13 validated | S | P0 |
| 52 | FR-AUTH.4b | Implement invalid token rejection for profile endpoint | Auth | FR-AUTH.4 | Given expired or invalid access token: return 401; SC-14 validated (enforcement delegated to AuthMiddleware in Phase 5) | S | P0 |
| 53 | FR-AUTH.4c | Exclude sensitive fields from profile response | Auth | FR-AUTH.4 | Response never includes password_hash or refresh_token_hash; unit test asserts field absence; SC-15 validated | S | P0 |
| 54 | FR-AUTH.5 | Implement password reset flow in AuthService | Auth | COMP-004, COMP-003, COMP-001, COMP-010 | `requestPasswordReset()` generates time-limited token and dispatches email; `confirmPasswordReset()` validates token, updates password, revokes sessions | M | P0 |
| 55 | FR-AUTH.5a | Implement reset token generation and email dispatch | Auth | FR-AUTH.5, COMP-010 | Generate password reset token with 1-hour TTL; store SHA-256 hash in password_reset_tokens table; dispatch email via EmailDispatcher; SC-16 validated | M | P0 |
| 56 | FR-AUTH.5b | Implement password update with valid reset token | Auth | FR-AUTH.5, COMP-001, COMP-008 | Given valid reset token: hash new password, update user record, mark reset token as used (single-use); SC-17 validated | S | P0 |
| 57 | FR-AUTH.5c | Implement invalid/expired reset token rejection (400) | Auth | FR-AUTH.5 | Given expired or invalid reset token: return 400 with appropriate error; SC-18 validated | S | P0 |
| 58 | FR-AUTH.5d | Implement session invalidation on password reset | Auth | FR-AUTH.5, COMP-003 | On successful password reset: revoke all refresh tokens for the user via TokenManager; SC-19 validated | S | P0 |
| 59 | DEP-3 | Integrate external email service for password reset | Integration | — | Email service client configured (provider per OQ-1 resolution — sync or message queue); connection tested; send capability verified | M | P0 |
| 60 | COMP-010 | Implement EmailDispatcher adapter | Auth | DEP-3 | Exports `sendPasswordResetEmail(email, resetLink): Promise<void>`; wraps external email service; injectable via interface; supports both sync and async dispatch based on configuration | M | P0 |
| 61 | TEST-007 | Write AuthService login flow unit tests | Testing | FR-AUTH.1, FR-AUTH.1a, FR-AUTH.1b, FR-AUTH.1c | Tests cover: valid credentials return tokens; invalid password returns 401 generic; unknown email returns 401 generic; locked account returns 403 before password check | M | P0 |
| 62 | TEST-008 | Write AuthService registration flow unit tests | Testing | FR-AUTH.2, FR-AUTH.2a, FR-AUTH.2b, FR-AUTH.2c, FR-AUTH.2d | Tests cover: valid data returns 201 + profile; duplicate email returns 409; weak password rejected; malformed email rejected; password is hashed not stored plain | M | P0 |
| 63 | TEST-009 | Write AuthService password reset flow unit tests | Testing | FR-AUTH.5, FR-AUTH.5a, FR-AUTH.5b, FR-AUTH.5c, FR-AUTH.5d | Tests cover: reset request creates token and sends email; valid token updates password; expired token returns 400; used token returns 400; sessions invalidated after reset | M | P0 |
| 64 | TEST-010 | Write AuthService profile retrieval unit tests | Testing | FR-AUTH.4, FR-AUTH.4a, FR-AUTH.4c | Tests cover: valid userId returns correct profile schema; sensitive fields absent from response; unknown userId returns appropriate error | S | P0 |

**Phase 4 total: 25 tasks**

---

### Phase 5: Middleware, Routes & API Layer

**Objective**: Build the HTTP layer — AuthMiddleware for token verification, RateLimiter for login protection, route registration, and all six API endpoints.

**Milestone**: All API endpoints operational behind feature flag. Rate limiting enforced. Protected routes require valid Bearer token. Integration tests pass against running server.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 65 | COMP-005 | Implement AuthMiddleware at `src/middleware/auth-middleware.ts` | Middleware | COMP-003 | Extracts Bearer token from Authorization header; verifies via TokenManager.verifyAccessToken(); injects userId into request context on success; returns 401 on missing/invalid/expired token; injectable via interface | M | P0 |
| 66 | COMP-011 | Implement RateLimiter middleware for login endpoint | Middleware | — | Rate limits by IP address; configurable window (default 60s) and max attempts (default 5); returns 429 with Retry-After header when limit exceeded; injectable via interface | M | P0 |
| 67 | FR-AUTH.1d | Wire rate limiting to login endpoint (5 per minute per IP) | Middleware | COMP-011, COMP-006 | RateLimiter applied to POST /auth/login; 6th attempt within 60s from same IP returns 429; SC-4 validated | S | P0 |
| 68 | COMP-006 | Implement AuthRoutes at `src/routes/index.ts` | Routes | COMP-004, COMP-005, AC-8 | Registers `/auth/*` route group; conditionally enabled by AUTH_SERVICE_ENABLED feature flag; wires AuthService handlers and AuthMiddleware to appropriate routes | M | P0 |
| 69 | API-001 | Implement POST /auth/login endpoint | API | COMP-006, FR-AUTH.1, COMP-011 | Accepts `{email, password}` body; delegates to AuthService.login(); returns 200 with tokens, 401 on invalid, 403 on locked, 429 on rate limit; sets refresh token in httpOnly cookie | M | P0 |
| 70 | API-002 | Implement POST /auth/register endpoint | API | COMP-006, FR-AUTH.2 | Accepts `{email, password, display_name}` body; delegates to AuthService.register(); returns 201 with profile, 409 on duplicate, 400 on validation failure | M | P0 |
| 71 | API-003 | Implement POST /auth/refresh endpoint | API | COMP-006, FR-AUTH.3 | Reads refresh token from httpOnly cookie; delegates to TokenManager.refreshTokens(); returns 200 with new token pair, 401 on expired/revoked/replayed | M | P0 |
| 72 | API-004 | Implement GET /auth/profile endpoint | API | COMP-006, FR-AUTH.4, COMP-005 | Protected by AuthMiddleware; reads userId from request context; delegates to AuthService.getProfile(); returns 200 with profile, 401 on invalid token | S | P0 |
| 73 | API-005 | Implement POST /auth/reset-request endpoint | API | COMP-006, FR-AUTH.5a | Accepts `{email}` body; delegates to AuthService.requestPasswordReset(); always returns 200 (prevents email enumeration); dispatches email only if user exists | S | P0 |
| 74 | API-006 | Implement POST /auth/reset-confirm endpoint | API | COMP-006, FR-AUTH.5b | Accepts `{token, new_password}` body; delegates to AuthService.confirmPasswordReset(); returns 200 on success, 400 on invalid/expired token | S | P0 |
| 75 | AC-10 | Configure auth opt-in for phase 1 (non-mandatory) | Configuration | COMP-006, AC-8 | Auth endpoints available but not required for existing routes; no existing endpoint breaks; feature flag allows full disable; rollback path validated | S | P0 |
| 76 | TEST-011 | Write AuthMiddleware unit test suite | Testing | COMP-005 | Tests cover: valid Bearer token passes and injects userId; missing Authorization header returns 401; malformed token returns 401; expired token returns 401; non-Bearer scheme returns 401 | M | P0 |
| 77 | TEST-012 | Write RateLimiter unit test suite | Testing | COMP-011 | Tests cover: requests under limit pass through; request at limit returns 429; Retry-After header present; limit resets after window; different IPs tracked independently | M | P0 |
| 78 | TEST-013 | Write route integration test suite | Testing | COMP-006, API-001 through API-006 | Integration tests against running server for all 6 endpoints; happy path + primary error cases for each; feature flag toggle verified | L | P0 |
| 79 | TEST-014 | Write API endpoint contract tests | Testing | API-001 through API-006 | Contract tests verify: response schemas match spec; HTTP status codes correct; error response format consistent; no sensitive data leakage in error responses | M | P1 |

**Phase 5 total: 15 tasks**

---

### Phase 6: Security Hardening & Performance

**Objective**: Validate security mitigations, perform load testing, establish monitoring, and implement operational automation.

**Milestone**: All RISK mitigations verified. NFR-AUTH.1 (p95 < 200ms) and NFR-AUTH.2 (99.9% uptime monitoring) validated. Key rotation automated. GAP-1 addressed.

**Resolves before proceeding**: OQ-4 (account lockout policy beyond rate limiting).

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 80 | RISK-1 | Validate JWT key compromise mitigation controls | Security | AC-1, AC-6, AC-7 | Verified: RS256 in use (not HS256); private key in secrets manager only; key rotation mechanism operational; no key material in logs, config, or source; penetration test confirms forged tokens rejected | M | P0 |
| 81 | RISK-3 | Validate bcrypt cost factor future-proofing | Security | COMP-001, AC-2 | Cost factor configurable without code change; documented review cadence (annual); migration path to Argon2id documented if bcrypt becomes insufficient; OWASP recommendation compliance verified | S | P1 |
| 82 | GAP-1 | Design and implement progressive account lockout | Security | COMP-011, COMP-008, FR-AUTH.1d | Per OQ-4 resolution: implement progressive lockout (e.g., lock after N failed attempts across all IPs); lock sets `is_locked=true` on user record; admin unlock mechanism; complements IP-based rate limiting | M | P1 |
| 83 | NFR-AUTH.1 | Execute authentication endpoint performance load tests | Performance | API-001 through API-006 | k6 load test: login, register, refresh, profile endpoints at expected load; p95 latency < 200ms for all auth endpoints; SC-20 validated; results documented | L | P0 |
| 84 | NFR-AUTH.2 | Configure service availability monitoring | Operations | OPS-001 | Health check polled at 30s interval; PagerDuty alert on 3 consecutive failures; 99.9% uptime target tracked in dashboard; SC-21 validated | M | P0 |
| 85 | OPS-002 | Automate RSA key rotation on 90-day schedule | Operations | AC-7, DEP-5 | Automated job rotates RSA key pair every 90 days; new key stored in secrets manager; old key retained for token verification grace period; `kid` header updated; zero-downtime rotation verified | M | P1 |
| 86 | OPS-003 | Integrate APM monitoring for auth endpoints | Operations | API-001 through API-006 | APM agent captures p50/p95/p99 latency for all auth endpoints; error rate tracking; dashboard created; alerting on p95 > 200ms | M | P1 |
| 87 | OPS-004 | Configure PagerDuty alerting for auth service | Operations | NFR-AUTH.2, OPS-003 | Alerts configured: service down (P1), p95 > 200ms sustained 5min (P2), error rate > 5% (P1), replay attack detected (P1) | S | P1 |
| 88 | TEST-015 | Write security-focused test suite | Testing | RISK-1, RISK-2, RISK-3 | Tests cover: JWT tampering rejected; HS256 downgrade rejected; timing-safe password comparison; refresh token replay triggers revocation; bcrypt cost factor verified; SQL injection in auth inputs blocked | L | P0 |
| 89 | TEST-016 | Write k6 load test scripts for auth endpoints | Testing | NFR-AUTH.1 | k6 scripts for login, register, refresh, profile; configurable virtual users and duration; threshold assertions for p95 < 200ms; CI-runnable | M | P0 |

**Phase 6 total: 10 tasks**

---

### Phase 7: Validation & Release Readiness

**Objective**: Execute full success criteria validation, document deferred items, create operational runbooks, and perform final regression testing.

**Milestone**: All 22 success criteria (SC-1 through SC-22) validated. Deferred items (GAP-2, GAP-3) documented with v1.1 tracking. Runbooks complete. Regression suite green.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 90 | GAP-2 | Document audit logging requirements for v1.1 | Documentation | — | Requirements document for authentication event logging (login attempts, token refreshes, password resets, lockouts); log format and destination specified; ticket created for v1.1 backlog | S | P2 |
| 91 | GAP-3 | Document token revocation on user deletion for v1.1 | Documentation | — | Design document addressing: access token validity window after deletion (up to 15min); proposed mitigation (token blacklist or short-lived tokens); ticket created for v1.1 backlog | S | P2 |
| 92 | TEST-017 | Execute full success criteria validation suite | Testing | SC-1 through SC-22 | All 22 success criteria pass: SC-1 (login tokens), SC-2 (generic 401), SC-3 (locked 403), SC-4 (rate limit 429), SC-5 (register 201), SC-6 (duplicate 409), SC-7 (password policy), SC-8 (email validation), SC-9 (token rotation), SC-10 (expired refresh 401), SC-11 (replay revocation), SC-12 (SHA-256 hashes), SC-13 (profile schema), SC-14 (invalid token 401), SC-15 (no sensitive fields), SC-16 (reset token + email), SC-17 (password update), SC-18 (invalid reset 400), SC-19 (session invalidation), SC-20 (p95 < 200ms), SC-21 (99.9% uptime), SC-22 (bcrypt cost 12) | L | P0 |
| 93 | TEST-018 | Execute end-to-end regression test suite | Testing | All phases | Full user journey tests: register → login → access profile → refresh token → logout; password reset flow end-to-end; concurrent user simulation; feature flag toggle regression; rollback (down-migration) regression | L | P0 |
| 94 | OPS-005 | Create operational runbook for auth service | Operations | All phases | Runbook covers: key rotation procedure, incident response for token compromise, account lockout/unlock procedure, feature flag rollback steps, database migration rollback, monitoring dashboard walkthrough | M | P1 |

**Phase 7 total: 5 tasks**

---

**Grand total: 94 task rows across 7 phases**

---

## 4. Risk Assessment & Mitigation Strategies

### Primary Risks (from extraction)

| Risk | Severity | Mitigation Strategy | Phase Addressed | Validation |
|------|----------|---------------------|-----------------|------------|
| **RISK-1**: JWT secret key compromise | High | RS256 asymmetric keys (AC-1); private key in secrets manager (AC-6); 90-day key rotation (AC-7); `kid` header for key versioning | Phase 1 (infra), Phase 3 (rotation), Phase 6 (validation) | TEST-015, RISK-1 task |
| **RISK-2**: Refresh token replay attack | High | Refresh token rotation on every use (FR-AUTH.3a); replay detection triggers full user revocation (FR-AUTH.3c); SHA-256 hash storage, never raw tokens (FR-AUTH.3d) | Phase 3 (implementation), Phase 6 (validation) | TEST-006, RISK-2 task |
| **RISK-3**: bcrypt cost factor obsolescence | Medium | Configurable cost factor (COMP-001); annual review cadence; documented Argon2id migration path | Phase 2 (implementation), Phase 6 (validation) | RISK-3 task |

### Gap-Derived Risks

| Gap | Severity | Strategy | Timeline |
|-----|----------|----------|----------|
| **GAP-1**: No progressive account lockout | Medium | Design in Phase 6 per OQ-4 resolution; complements IP-based rate limiting | v1.0 Phase 6 |
| **GAP-2**: No audit logging | Low | Document requirements; defer implementation to v1.1 | v1.1 |
| **GAP-3**: Token validity after user deletion | Medium | Document design; defer implementation to v1.1 | v1.1 |

### Architectural Risk: Open Questions

Unresolved open questions (OQ-1 through OQ-7) pose schedule risk if decisions are delayed:

- **OQ-3** (database engine) and **OQ-7** (RSA key size) block Phase 1 — must resolve before sprint start
- **OQ-1** (email dispatch strategy) and **OQ-2** (max refresh tokens per user) block Phase 4
- **OQ-4** (lockout policy) blocks Phase 6 GAP-1 task
- **OQ-5** (audit logging) and **OQ-6** (deletion revocation) are v1.1 and do not block v1.0

---

## 5. Resource Requirements & Dependencies

### External Dependencies

| ID | Dependency | Type | Risk Level | Mitigation |
|----|-----------|------|------------|------------|
| DEP-1 | `jsonwebtoken` (npm) | Library | Low | Well-maintained, widely used; pin version; audit for CVEs |
| DEP-2 | `bcrypt` (npm) | Library | Low | Native binding requires build tools in CI; test compilation in CI pipeline |
| DEP-3 | Email service | External | Medium | Abstract behind EmailDispatcher interface; support sync + async dispatch; mock in tests |
| DEP-4 | Relational database | Infrastructure | Low | Standard infrastructure; abstract behind repository interfaces; engine-agnostic migrations where possible |
| DEP-5 | Secrets manager | Infrastructure | Medium | Required for RSA key storage; startup fails clearly if unavailable; local dev fallback (env var) for development only |

### Team Skills Required

- **Backend TypeScript**: Service layer, middleware, route handlers
- **Security**: JWT implementation review, bcrypt configuration, penetration testing
- **Database**: Migration authoring, index optimization, query performance
- **DevOps**: Secrets manager setup, monitoring/alerting configuration, key rotation automation
- **QA**: Load testing (k6), security testing, integration test authoring

### Infrastructure Requirements

- Relational database instance (development, staging, production)
- Secrets manager instance with RSA key pair
- Email service account or message queue
- APM/monitoring platform
- PagerDuty (or equivalent) for alerting
- CI/CD pipeline with native build tool support (for bcrypt)

---

## 6. Success Criteria & Validation Approach

### Validation Matrix

All 22 success criteria from the extraction are validated across three testing tiers:

**Tier 1 — Unit Tests** (Phases 2-5): SC-2, SC-3, SC-6, SC-7, SC-8, SC-10, SC-12, SC-13, SC-14, SC-15, SC-16, SC-17, SC-18, SC-22

**Tier 2 — Integration Tests** (Phases 3-5): SC-1, SC-4, SC-5, SC-9, SC-11, SC-19

**Tier 3 — System/Load Tests** (Phase 6-7): SC-20, SC-21

### Validation Execution

1. **Continuous**: Unit tests run on every commit (Phases 2-5 TEST tasks)
2. **Phase gates**: Integration tests run at phase completion (TEST-006, TEST-013)
3. **Pre-release**: Full success criteria suite (TEST-017) and regression suite (TEST-018)
4. **Post-deploy**: Load tests (TEST-016), availability monitoring (NFR-AUTH.2)

### Acceptance Threshold

Release is gated on:
- All 22 SC criteria passing (TEST-017)
- p95 latency < 200ms under expected load (SC-20)
- Zero critical or high security findings in TEST-015
- Feature flag rollback tested and verified (AC-8, AC-10)
- Down-migration scripts verified (AC-9)

---

## 7. Timeline Estimates

| Phase | Description | Estimated Duration | Parallelism | Cumulative |
|-------|-------------|--------------------|-------------|------------|
| **Phase 1** | Infrastructure & Data Layer | 3-4 days | High (DEP tasks parallel, DM tasks parallel after DEP-4) | Week 1 |
| **Phase 2** | Core Crypto & Repositories | 3-4 days | High (COMP-001 ∥ COMP-002 ∥ COMP-008 ∥ COMP-009) | Week 1-2 |
| **Phase 3** | Token Management | 3-4 days | Low (sequential dependency on COMP-002, COMP-009) | Week 2 |
| **Phase 4** | Authentication Service | 5-6 days | Medium (FR-AUTH.1 ∥ FR-AUTH.2 after COMP-004; FR-AUTH.4 ∥ FR-AUTH.5) | Week 3 |
| **Phase 5** | Middleware, Routes & API | 4-5 days | Medium (COMP-005 ∥ COMP-011; then API endpoints parallel) | Week 4 |
| **Phase 6** | Security & Performance | 3-4 days | High (RISK tasks ∥ NFR tasks ∥ OPS tasks) | Week 4-5 |
| **Phase 7** | Validation & Release | 2-3 days | Low (sequential validation) | Week 5 |

**Total estimated duration**: 4-5 weeks with a single developer; 2.5-3.5 weeks with two developers leveraging Phase 2 parallelism and Phase 4 flow independence.

### Critical Path

```
DEP-4 → DM-001 → MIG-001 → COMP-007 → COMP-008 → COMP-001 → COMP-003 → COMP-004 → COMP-006 → API-001 → TEST-013 → TEST-017
     ↘ DEP-5 → AC-6 → COMP-002 ↗                    ↗ COMP-005 ↗
```

The critical path runs through database provisioning, migration, both crypto components (parallel), TokenManager, AuthService, route registration, and validation. Total critical-path length: ~18-22 working days.
