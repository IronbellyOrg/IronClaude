---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
---

# Authentication System Roadmap

## Executive Summary

This roadmap implements a stateless JWT-based authentication system with secure password hashing (bcrypt), refresh token rotation with replay detection, and comprehensive security controls. The implementation spans 6 phases over an estimated 6-8 weeks, with a critical path focused on cryptographic foundations, token management, and database persistence.

**Key Architectural Decisions**:
- **Stateless JWT** with RS256 asymmetric signing for scalability and key separation
- **Hybrid token strategy**: Access tokens in memory (XSS protection), refresh tokens in httpOnly cookies (CSRF-proof)
- **Refresh token rotation** with hash-based revocation for replay attack mitigation
- **Layered service architecture** with explicit dependency injection for testability (NFR-AUTH-IMPL-3)
- **Feature flag gating** (`AUTH_SERVICE_ENABLED`) for zero-downtime rollback capability

**Complexity Mitigation**: While the spec scores 0.6 (MEDIUM), the primary complexity drivers are cryptographic correctness and refresh token state management. These are well-understood patterns; the roadmap isolates them into isolated, testable modules to prevent integration errors.

---

## Phased Implementation Plan

### Phase 0: Cryptographic Foundations (Weeks 1-1.5)
**Objective**: Establish secure crypto library layer with no business logic dependencies.

#### Phase 0.1: JWT Service Implementation
- **Component**: `src/services/jwt-service.ts`
- **Deliverables**:
  - RS256 asymmetric key pair generation/management
  - JWT signing function: `sign(payload: any, expiresIn: string): string`
  - JWT verification function: `verify(token: string): any` (with error handling for expired/malformed tokens)
  - Key rotation placeholder (return RSA private key from secrets manager; actual key retrieval deferred to Phase 3)
  - Unit tests covering: valid tokens, expired tokens, tampered signatures, invalid format
- **Dependencies**: `jsonwebtoken` library; secrets manager (mocked in unit tests, real in Phase 3)
- **Acceptance**: All unit tests pass; benchmark confirms signing latency < 50ms, verification latency < 30ms
- **Owner**: Backend Engineer (Cryptography specialist preferred)
- **Risk Owners**: RISK-1 (JWT secret compromise) — mitigation begins with isolated key handling
- **Estimated Effort**: 3-4 days
- **Wiring Artifacts**: None (foundation module, no consumers yet)

#### Phase 0.2: Password Hasher Implementation
- **Component**: `src/services/password-hasher.ts`
- **Deliverables**:
  - Bcrypt hashing function: `hash(password: string, costFactor?: number): Promise<string>` (default costFactor=12)
  - Bcrypt comparison function: `compare(password: string, hash: string): Promise<boolean>`
  - Input validation: enforce FR-AUTH.2c password policy (8+ chars, 1 uppercase, 1 lowercase, 1 digit) in separate validator function
  - Configuration mechanism for cost factor (NFR-AUTH.3 — cost factor 12 with ~250ms timing)
  - Unit tests covering: valid passwords, policy violations, comparison correctness, cost factor timing
  - Benchmark test confirming cost factor 12 ≈ 250ms per hash (NFR-AUTH.3)
- **Dependencies**: `bcrypt` library
- **Acceptance**: All unit tests pass; benchmark confirms 250ms±50ms timing
- **Owner**: Backend Engineer (Cryptography specialist preferred)
- **Risk Owners**: RISK-3 (bcrypt cost factor obsolescence) — mitigation includes configurable cost factor and annual review trigger
- **Estimated Effort**: 2-3 days
- **Wiring Artifacts**: None (foundation module, no consumers yet)

#### Phase 0 Gate: Cryptographic Validation
- **Gate Activities**:
  - Code review by security engineer: RS256 implementation, key handling, bcrypt configuration
  - Cryptographic audit: verify no keys in logs, secrets manager integration design
  - Integration readiness: confirm both modules export clean interfaces for Phase 1
- **Exit Criteria**: Both modules pass code review; all crypto benchmarks meet targets; design review confirms no architectural surprises in Phase 1

---

### Phase 1: Core Service Layer (Weeks 1.5-3)
**Objective**: Build stateful token management (refresh token rotation/revocation) and unified auth service orchestration.

#### Phase 1.1: Token Manager Service
- **Component**: `src/services/token-manager.ts`
- **Deliverables**:
  - Issue access token: `issueAccessToken(userId: string): string` — calls `jwt-service.sign()` with 15min TTL
  - Issue refresh token pair: `issueRefreshTokenPair(userId: string): { refreshToken: string; refreshTokenHash: string }` — generate token, return plaintext + SHA-256 hash
  - Rotate refresh token: `rotateRefreshToken(oldRefreshTokenHash: string, userId: string): { accessToken: string; newRefreshToken: string; newRefreshTokenHash: string }` — validates old hash, issues new pair, returns both tokens
  - Validate refresh token: `validateRefreshToken(refreshTokenHash: string, userId: string): boolean` — check database (Phase 3) for revoked tokens
  - Revoke user tokens: `revokeAllUserTokens(userId: string)` — invalidate all refresh tokens for a user (used in FR-AUTH.5d password reset, FR-AUTH.3c replay detection)
  - Error handling: differentiate expired vs. revoked vs. tampered tokens
  - Unit tests covering: token issuance, rotation without database, mocked validation, revocation semantics
- **Dependencies**: `jwt-service`, `password-hasher` (for consistency); database connection (mocked in Phase 1 tests, real in Phase 3)
- **Acceptance**: All unit tests pass; rotation flow produces two different tokens with correct TTLs
- **Owner**: Backend Engineer (Services architect preferred)
- **Risk Owners**: RISK-2 (refresh token replay attack) — mitigation includes rotation mechanism and revocation tracking
- **Estimated Effort**: 4-5 days
- **Wiring Artifacts**:
  - **Named Artifact**: `TokenManager dependency injection token`
  - **Wired Components**: Used by AuthService (Phase 1.2), auth routes (Phase 2.1), password reset flow (Phase 4.1)
  - **Owning Phase**: Phase 1.1 (constructor injection pattern)
  - **Cross-Reference**: Phase 1.2 (AuthService consumes), Phase 2.1 (routes consume), Phase 3.1 (database integration)

#### Phase 1.2: Auth Service Implementation
- **Component**: `src/services/auth-service.ts`
- **Deliverables**:
  - Login: `login(email: string, password: string): Promise<{ accessToken: string; refreshToken: string; user: UserProfile }>` 
    - Validate email format
    - Query user by email
    - Compare password with bcrypt (FR-AUTH.1b — no information leakage on invalid credential)
    - Check account lock status (GAP-1 fallback: no lockout yet, but architecture supports Phase 1.1 addition)
    - Call `token-manager.issueAccessToken()` and `issueRefreshTokenPair()`
    - Return both tokens + user profile (sans sensitive fields)
  - Register: `register(email: string, password: string, displayName: string): Promise<{ user: UserProfile }>`
    - Validate email format (FR-AUTH.2d)
    - Check for duplicate email (FR-AUTH.2b)
    - Validate password policy (FR-AUTH.2c)
    - Hash password via `password-hasher.hash()`
    - Insert user record with UUID v4 (FR-AUTH.1-IMPL-3)
    - Return user profile
  - Get profile: `getProfile(userId: string): Promise<UserProfile>`
    - Query user by ID
    - Return profile without sensitive fields (FR-AUTH.4c)
  - Validate access token: `validateAccessToken(token: string): Promise<{ userId: string; email: string }>`
    - Call `jwt-service.verify()`
    - Handle expiration, tampering gracefully
  - Rate limiting: integration point for FR-AUTH.1d (5/min/IP) — service accepts rate limiter middleware injection
  - Unit tests covering: all login/register/profile flows with mocked database, rate limiting with mock timer
  - Integration tests (Phase 5): login→profile, registration→login, token refresh flow
- **Dependencies**: `jwt-service`, `password-hasher`, `token-manager`; database (mocked in Phase 1 tests)
- **Acceptance**: All unit tests pass; integration tests confirm login→profile flow works end-to-end (Phase 5)
- **Owner**: Backend Engineer (Services architect preferred)
- **Risk Owners**: RISK-1 (secret compromise) — application-layer token validation; RISK-2 (replay) — service orchestrates token-manager; RISK-4 (email dependency) — implicit in password reset (Phase 4)
- **Estimated Effort**: 5-6 days
- **Wiring Artifacts**:
  - **Named Artifact**: `AuthService dependency injection token`
  - **Wired Components**: Depends on TokenManager (Phase 1.1), PasswordHasher (Phase 0.2), JwtService (Phase 0.1)
  - **Owning Phase**: Phase 1.2 (constructor injection, interface contract definition)
  - **Cross-Reference**: Phase 2.1 (auth routes consume), Phase 3.1 (database integration), Phase 4.1 (password reset flow)

#### Phase 1 Gate: Service Integration Readiness
- **Gate Activities**:
  - Architecture review: token-manager rotation logic, auth-service orchestration, dependency injection patterns
  - Integration testing: confirm Phase 1 modules can be composed without Phase 2 or Phase 3
  - Database schema design review: preview tables/columns needed for Phase 3
- **Exit Criteria**: All services pass unit tests; integration tests within Phase 1 modules pass; database schema peer-reviewed

---

### Phase 2: API Route & Middleware Integration (Weeks 3-4)
**Objective**: Wire services into HTTP routes and middleware; implement rate limiting and error responses.

#### Phase 2.1: Authentication Routes
- **Component**: `src/routes/auth-routes.ts`
- **Deliverables**:
  - `POST /auth/login` — calls `auth-service.login()`, returns 200 with access_token + refresh_token (as JSON body; cookie handling in middleware Phase 2.2)
  - `POST /auth/register` — calls `auth-service.register()`, returns 201 with user profile
  - `POST /auth/refresh` — extracts refresh token from httpOnly cookie (Phase 2.2), calls `token-manager.rotateRefreshToken()`, returns new access_token + rotated refresh_token
  - `GET /auth/profile` — extracts Bearer token from Authorization header (Phase 2.2), calls `auth-service.validateAccessToken()`, calls `auth-service.getProfile()`, returns user profile (sans sensitive fields)
  - Error responses: 
    - 401 on invalid/expired access token (FR-AUTH.1b, FR-AUTH.4b)
    - 403 on locked account (FR-AUTH.1c)
    - 409 on duplicate email (FR-AUTH.2b)
    - 400 on validation failure (password policy, email format, missing fields)
  - Rate limiting middleware integration: 5/min/IP on login/register (FR-AUTH.1d)
  - Input validation middleware: email format, password policy enforcement
  - Unit tests (Phase 5): mock auth-service responses, confirm route status codes and response shapes
- **Dependencies**: `auth-service` (Phase 1.2), Express/HTTP framework
- **Acceptance**: All routes return correct status codes; mocked auth-service calls produce expected responses
- **Owner**: Backend Engineer (API specialist preferred)
- **Risk Owners**: RISK-2 (replay detection) — service layer handles, routes just pass through
- **Estimated Effort**: 3-4 days
- **Wiring Artifacts**:
  - **Named Artifact**: `Express Router for /auth/* routes`
  - **Wired Components**: Routes depend on AuthService, TokenManager, PasswordHasher (via AuthService), JwtService (via AuthService and TokenManager)
  - **Owning Phase**: Phase 2.1 (router definition and route-to-service wiring)
  - **Cross-Reference**: Phase 3.1 (database integration into AuthService), Phase 5 (route integration tests)

#### Phase 2.2: Auth Middleware
- **Component**: `src/middleware/auth-middleware.ts` (extend existing if present; create if not)
- **Deliverables**:
  - Bearer token extraction: `req.headers.authorization` → parse "Bearer <token>"
  - Refresh token extraction: `req.cookies.refresh_token` (httpOnly, secure flags)
  - Token validation: call `auth-service.validateAccessToken()` or `token-manager.validateRefreshToken()`
  - Error handling: return 401 on missing/invalid tokens, propagate to error handler
  - Middleware chain integration: ensure called before route handlers; set `req.user = { userId, email }` on success
  - Cookie management: ensure refresh_token cookie is httpOnly, secure, SameSite=Strict (XSS/CSRF protection per FR-AUTH.1-IMPL-2)
  - Unit tests: mock token validation, confirm req.user is set correctly
- **Dependencies**: `auth-service`, `token-manager`, Express middleware
- **Acceptance**: Middleware sets req.user correctly; returns 401 on missing tokens
- **Owner**: Backend Engineer (Middleware specialist preferred)
- **Risk Owners**: None directly; foundational for all protected routes
- **Estimated Effort**: 2-3 days
- **Wiring Artifacts**:
  - **Named Artifact**: `Express middleware registration (app.use(authMiddleware))`
  - **Wired Components**: Middleware depends on AuthService, TokenManager; called before all protected routes
  - **Owning Phase**: Phase 2.2 (middleware definition and app-level registration)
  - **Cross-Reference**: Phase 5 (integration tests verify middleware blocks unauthenticated requests)

#### Phase 2.3: Rate Limiting & Error Handling
- **Component**: `src/middleware/rate-limit-middleware.ts`, `src/middleware/error-handler.ts`
- **Deliverables**:
  - Rate limiter: 5 login attempts per minute per IP (FR-AUTH.1d)
    - Middleware captures IP address (`req.ip` or custom X-Forwarded-For handling)
    - In-memory store (with TTL cleanup) or Redis (if available)
    - Return 429 on limit exceeded
  - Error handler: centralized catch-all for auth errors
    - Convert service exceptions to HTTP responses (401, 403, 409, 400)
    - Sanitize error messages to prevent information leakage (FR-AUTH.1b)
    - Log errors with timestamp, IP, user_id (if available) for audit trail (GAP-2 deferred to v1.1, but log structure now)
  - Unit tests: mock IP capture, confirm rate limit triggers, error conversion
- **Dependencies**: Express middleware, optional Redis client
- **Acceptance**: Rate limiting returns 429 after 5 attempts; errors return appropriate status codes
- **Owner**: Backend Engineer (DevOps/Infra preferred)
- **Risk Owners**: None directly; supports FR-AUTH.1d implementation
- **Estimated Effort**: 2-3 days
- **Wiring Artifacts**:
  - **Named Artifact**: `Express middleware chain registration`
  - **Wired Components**: Rate limiter middleware, error handler middleware; applied globally or per-route
  - **Owning Phase**: Phase 2.3 (middleware registration in main app file)
  - **Cross-Reference**: Phase 5 (integration tests verify rate limit behavior)

#### Phase 2 Gate: Route & Middleware Readiness
- **Gate Activities**:
  - Integration testing: confirm auth routes return correct HTTP status codes with mocked services
  - Middleware integration testing: confirm Bearer extraction, cookie handling, error responses work end-to-end
  - Security review: cookie flags (httpOnly, secure, SameSite), header sanitization, rate limiting logic
  - API contract review: response schemas match spec requirements
- **Exit Criteria**: All routes return correct status codes; middleware integration tests pass; security review passed

---

### Phase 3: Data Persistence & Database Integration (Weeks 4-5)
**Objective**: Implement database schema, migrations, and service-layer database integration.

#### Phase 3.1: Database Schema & Migrations
- **Component**: `src/db/migrations/001_create_users_table.sql`, `002_create_refresh_tokens_table.sql`
- **Deliverables**:
  - Users table (Migration 001):
    - `id` (UUID v4, primary key) — FR-AUTH.1-IMPL-3
    - `email` (VARCHAR, unique, not null)
    - `password_hash` (VARCHAR, bcrypt hash, not null) — replaces plaintext storage (FR-AUTH.1-IMPL-1)
    - `display_name` (VARCHAR, not null)
    - `is_locked` (BOOLEAN, default false) — prepared for GAP-1 account lockout logic
    - `created_at` (TIMESTAMP, default NOW(), not null)
    - `updated_at` (TIMESTAMP, default NOW(), on update, not null)
    - Indexes: `email` (unique), `created_at` (for auditing)
  - Refresh tokens table (Migration 002):
    - `id` (UUID v4, primary key)
    - `user_id` (UUID, foreign key → users.id, not null, cascade delete) — supports FR-AUTH.5d token invalidation on password reset
    - `token_hash` (VARCHAR, SHA-256 hash, not null, unique) — prevents token plaintext storage
    - `is_revoked` (BOOLEAN, default false) — supports FR-AUTH.3c replay detection
    - `expires_at` (TIMESTAMP, not null) — 7-day TTL per FR-AUTH.1a
    - `created_at` (TIMESTAMP, default NOW(), not null)
    - Indexes: `user_id`, `expires_at`, `is_revoked` (for query performance)
  - Down migrations (rollback scripts) — FR-AUTH.1-IMPL-5 (required for rollback capability)
  - Migration runner integration: confirm migrations execute in order, produce expected schema
- **Dependencies**: Database driver (e.g., pg for PostgreSQL), migration runner (e.g., Knex, Typeorm)
- **Acceptance**: Migrations produce correct schema; down migrations restore previous state; integration tests confirm schema matches service expectations
- **Owner**: Database Engineer / DevOps Engineer
- **Risk Owners**: None directly; enables all persistence-dependent features
- **Estimated Effort**: 2-3 days
- **Wiring Artifacts**: None (pure schema; no application code wiring)

#### Phase 3.2: AuthService Database Integration
- **Component**: Update `src/services/auth-service.ts` to use real database
- **Deliverables**:
  - Inject database connection (constructor injection) into AuthService
  - `login()`: query users table by email, compare password
  - `register()`: insert into users table, check for constraint violations (duplicate email → 409)
  - `getProfile()`: query user by ID, return all non-sensitive fields
  - `revokeAllUserTokens()`: delete from refresh_tokens table where user_id matches (FR-AUTH.5d)
  - Handle connection pooling and transaction semantics (Phase 3.4)
  - Error mapping: database errors → HTTP errors (constraint violation → 409, connection error → 503)
  - Unit tests: mock database client (using test containers or in-memory DB)
  - Integration tests (Phase 5): real database with schema from Phase 3.1
- **Dependencies**: Database driver, connection pool
- **Acceptance**: Unit tests with mocked DB pass; integration tests with real DB pass
- **Owner**: Backend Engineer (Database specialist preferred)
- **Risk Owners**: None directly; enables critical FR-AUTH.1, FR-AUTH.2, FR-AUTH.4
- **Estimated Effort**: 3-4 days
- **Wiring Artifacts**:
  - **Named Artifact**: `Database connection injection (constructor parameter)`
  - **Wired Components**: AuthService now depends on Database client; instantiated in app bootstrap (Phase 3.3)
  - **Owning Phase**: Phase 3.2 (refactor AuthService constructor + methods)
  - **Cross-Reference**: Phase 3.3 (dependency injection container setup), Phase 5 (integration tests)

#### Phase 3.3: TokenManager Database Integration
- **Component**: Update `src/services/token-manager.ts` to use real database
- **Deliverables**:
  - Inject database connection into TokenManager
  - `issueRefreshTokenPair()`: hash plaintext token (SHA-256), insert into refresh_tokens table
  - `rotateRefreshToken()`: query refresh_tokens by hash, check is_revoked, insert new token, update old token is_revoked=true (atomic transaction)
  - `validateRefreshToken()`: query by hash, check expiration + is_revoked status
  - `revokeAllUserTokens()`: called by auth-service; update all refresh_tokens for user_id with is_revoked=true (or delete, depending on audit requirements)
  - Transaction management: ensure rotation is atomic (old token revoked + new token inserted together or rolled back)
  - Error handling: expired token → specific error; revoked token (replay attack) → alert error; invalid hash → 401
  - Unit tests: mock database; verify rotation produces correct state changes
  - Integration tests (Phase 5): real database, verify rotation behavior with concurrent requests (race condition testing)
- **Dependencies**: Database driver, transaction support
- **Acceptance**: Unit tests with mocked DB pass; integration tests verify atomic rotation and replay detection
- **Owner**: Backend Engineer (Database + Concurrency specialist preferred)
- **Risk Owners**: RISK-2 (refresh token replay attack) — mitigation depends on atomic rotation in Phase 3.3
- **Estimated Effort**: 4-5 days
- **Wiring Artifacts**:
  - **Named Artifact**: `Database connection injection (TokenManager constructor)`
  - **Wired Components**: TokenManager depends on Database client; instantiated in app bootstrap (Phase 3.3)
  - **Owning Phase**: Phase 3.3 (refactor TokenManager methods + transaction logic)
  - **Cross-Reference**: Phase 3.4 (dependency injection container), Phase 5 (concurrency tests)

#### Phase 3.4: Dependency Injection Container Setup
- **Component**: `src/di/container.ts` (or use existing DI framework)
- **Deliverables**:
  - Service registration:
    - Singleton: JwtService (shared key material)
    - Singleton: PasswordHasher (shared bcrypt config)
    - Singleton: Database connection pool
    - Singleton: TokenManager (depends on Database)
    - Singleton: AuthService (depends on TokenManager, PasswordHasher, JwtService, Database)
  - Factory functions for routes and middleware to request services from container
  - Testability support: container accepts mock implementations for unit testing
  - Constructor injection enforcement: all services receive dependencies via constructor, no global state
  - Documentation: wiring diagram showing service dependency graph
- **Dependencies**: DI framework (e.g., InversifyJS, tsyringe) or manual factory pattern
- **Acceptance**: Container produces correct service instances; unit tests can inject mocks; all services are singletons where appropriate
- **Owner**: Backend Engineer (Architecture specialist preferred)
- **Risk Owners**: None directly; foundational for testability (NFR-AUTH-IMPL-3)
- **Estimated Effort**: 2-3 days
- **Wiring Artifacts**:
  - **Named Artifact**: `DI Container (src/di/container.ts)`
  - **Wired Components**: All Phase 0-3 services registered with dependency relationships
  - **Owning Phase**: Phase 3.4 (container definition and registration)
  - **Cross-Reference**: Phase 2 (routes use container to get services), Phase 5 (tests inject mocks via container)

#### Phase 3 Gate: Persistence Readiness
- **Gate Activities**:
  - Database schema review: confirm tables match service expectations, indexes are appropriate
  - Migration testing: run migrations forward and backward; confirm schema changes are reversible (FR-AUTH.1-IMPL-5)
  - Integration testing: services with real database; verify data consistency under concurrent access
  - Container wiring review: confirm dependency graph is correct; no cycles or unresolved deps
- **Exit Criteria**: All migrations pass; services work with real database; DI container produces correct instances; integration tests pass

---

### Phase 4: Advanced Features & External Integration (Weeks 5-6)
**Objective**: Implement password reset flow (external email service), feature flag gating, and advanced configurations.

#### Phase 4.1: Password Reset Flow
- **Component**: `src/services/password-reset-service.ts`, `src/routes/auth-routes.ts` (extend)
- **Deliverables**:
  - Request password reset: `POST /auth/password-reset/request`
    - Accept email address
    - Query user by email (don't reveal if email exists per FR-AUTH.1b pattern)
    - Generate reset token (JWT with 1-hour TTL and user_id claim) — FR-AUTH.5a
    - Store reset token hash in a temporary table (reset_tokens) with expiration
    - Dispatch email with reset link (async via message queue per OI-1) — FR-AUTH.5a
    - Return 200 (always, whether email exists or not)
  - Reset password: `POST /auth/password-reset/confirm`
    - Accept reset token + new password
    - Validate reset token (not expired, not already used) — FR-AUTH.5c
    - Hash new password via password-hasher
    - Update user record with new password_hash
    - Mark reset_tokens record as used (is_used=true)
    - Revoke all existing refresh tokens for user (via token-manager.revokeAllUserTokens()) — FR-AUTH.5d
    - Return 200 with success message (or optionally auto-login with new tokens)
  - External integration: Email service abstraction (interface) — concrete implementation (SendGrid, Mailgun, etc.) injected
  - Error handling: token expired → 400; token already used → 400; user not found → 200 (no information leakage)
  - Unit tests: mock email service, confirm flow with mocked database
  - Integration tests (Phase 5): real database, real email service (or mock), verify token expiration
- **Dependencies**: `password-hasher`, `token-manager`, `auth-service`, Email service (abstract)
- **Acceptance**: Flow produces correct database state; emails dispatched; expired tokens rejected
- **Owner**: Backend Engineer (Services architect preferred)
- **Risk Owners**: RISK-4 (email service dependency) — mitigation through async dispatch (OI-1) reduces failure impact
- **Estimated Effort**: 5-6 days
- **Wiring Artifacts**:
  - **Named Artifact**: `Email service interface + injectable implementation`
  - **Wired Components**: PasswordResetService depends on TokenManager, PasswordHasher, Database, Email service
  - **Owning Phase**: Phase 4.1 (service definition and email integration)
  - **Cross-Reference**: Phase 3.4 (DI container registration), Phase 5 (integration tests with mock email)

#### Phase 4.2: Feature Flag Implementation
- **Component**: `src/config/feature-flags.ts`, middleware integration
- **Deliverables**:
  - `AUTH_SERVICE_ENABLED` flag (FR-AUTH.1-IMPL-4) — gates entire /auth/* route group
  - Feature flag service: `isEnabled(flagName: string): boolean` — reads from environment variables
  - Middleware integration: if `AUTH_SERVICE_ENABLED=false`, return 503 on /auth/* routes (fallback to legacy auth if available)
  - Rollback capability: set `AUTH_SERVICE_ENABLED=false`, redeploy; existing auth behavior is preserved
  - Configuration: environment variable + optional configuration file support
  - Logging: log flag state on startup for visibility
  - Unit tests: confirm flag logic works correctly
- **Dependencies**: Configuration management (env vars, config files)
- **Acceptance**: Flag gates routes correctly; switching flag toggles behavior
- **Owner**: DevOps Engineer / Backend Engineer
- **Risk Owners**: RISK-1, RISK-2, RISK-3 (mitigation via rollback flag)
- **Estimated Effort**: 1-2 days
- **Wiring Artifacts**:
  - **Named Artifact**: `Feature flag middleware`
  - **Wired Components**: Middleware checks flag before route handlers execute
  - **Owning Phase**: Phase 4.2 (middleware definition and app registration)
  - **Cross-Reference**: Phase 5 (tests verify flag behavior), Phase 6 (deployment uses flag for gradual rollout)

#### Phase 4.3: Advanced Configuration & Customization
- **Component**: `src/config/auth-config.ts`
- **Deliverables**:
  - Configurable parameters (all with secure defaults):
    - JWT signing algorithm (currently RS256, but extensible)
    - Bcrypt cost factor (currently 12, configurable per NFR-AUTH.3 with annual review trigger)
    - Token TTLs (access token 15min, refresh token 7d, reset token 1hr)
    - Rate limiting thresholds (currently 5/min/IP per FR-AUTH.1d)
    - Maximum active refresh tokens per user (OQ-2; recommendation 5-10, deferred to v1.0 architecture review)
    - Account lockout policy (GAP-1; progressive lockout after N failures, deferred to v1.1)
  - Environment variable overrides for all parameters
  - Validation: confirm parameters are reasonable (e.g., cost factor 10-14, TTLs > 0)
  - Logging: log config on startup
- **Dependencies**: Configuration framework
- **Acceptance**: All parameters are configurable; validation prevents invalid configs
- **Owner**: Backend Engineer (DevOps specialist preferred)
- **Risk Owners**: RISK-3 (cost factor obsolescence) — annual review trigger + configurable cost factor
- **Estimated Effort**: 1-2 days
- **Wiring Artifacts**: None (config is read-only after startup)

#### Phase 4 Gate: Feature Completeness
- **Gate Activities**:
  - Password reset flow testing: end-to-end with real/mock email service
  - Feature flag testing: confirm flag gates routes correctly and fallback behavior works
  - Configuration testing: confirm parameters are read correctly, validation works
  - Security review: email dispatch timing (async vs. sync per OI-1), token expiration, replay detection with password reset
- **Exit Criteria**: All features work end-to-end; rollback via feature flag verified; configuration is correct

---

### Phase 5: Comprehensive Testing & Validation (Weeks 6-7)
**Objective**: Implement full test suite covering units, integration, e2e, security, and performance.

#### Phase 5.1: Unit Tests (Foundation Modules & Services)
- **Coverage**: Phase 0-1-2 modules
- **Deliverables**:
  - `tests/unit/jwt-service.test.ts`: signing, verification, expiration, tampering, key rotation
  - `tests/unit/password-hasher.test.ts`: hashing, comparison, policy validation, cost factor timing
  - `tests/unit/token-manager.test.ts`: issuance, rotation, revocation, validation logic
  - `tests/unit/auth-service.test.ts`: login, register, profile, validation (with mocked database/email)
  - `tests/unit/rate-limiter.test.ts`: limit tracking, reset after TTL, per-IP isolation
  - Minimum coverage target: 90% line coverage, 85% branch coverage
  - Test doubles: mock database, mock email service, mock tokens
- **Acceptance**: All tests pass; coverage meets targets
- **Owner**: Backend Engineer / QA Engineer
- **Estimated Effort**: 5-6 days
- **Wiring Artifacts**: None (tests verify individual modules)

#### Phase 5.2: Integration Tests (Service Composition & Database)
- **Coverage**: Phase 3 database integration, Phase 2 routes with real services
- **Deliverables**:
  - `tests/integration/auth-flow.test.ts`:
    - Register → Login → Get Profile (full flow) — SC-7
    - Login → Refresh Token → Get Profile with new token — FR-AUTH.3a
    - Refresh with revoked token → error — FR-AUTH.3c (replay detection)
    - Password reset → invalidate tokens → re-login — FR-AUTH.5d
    - Login with locked account → 403 — FR-AUTH.1c (if account lockout implemented)
  - `tests/integration/database.test.ts`: schema validation, migration testing, constraint enforcement
  - `tests/integration/routes.test.ts`: HTTP status codes, response schemas, error handling
  - `tests/integration/rate-limit.test.ts`: concurrent login attempts, limit enforcement, IP tracking
  - Database fixtures: test data setup/teardown, schema reset between tests
  - Test database: isolated instance (Docker container or in-memory) per test suite
  - Minimum coverage target: 95% of critical paths (login, token refresh, password reset)
- **Acceptance**: All tests pass; critical paths fully tested
- **Owner**: Backend Engineer / QA Engineer
- **Estimated Effort**: 6-7 days
- **Wiring Artifacts**: None (tests verify integration)

#### Phase 5.3: E2E Lifecycle Tests (Full User Journeys)
- **Coverage**: SC-7 requirement — end-to-end scenarios
- **Deliverables**:
  - `tests/e2e/user-lifecycle.test.ts`:
    1. Register new user (email validation, password policy, conflict detection)
    2. Login with new credentials
    3. Get profile (verify non-sensitive fields only)
    4. Refresh access token (rotate refresh token, verify new token works)
    5. Request password reset
    6. Confirm password reset with new password
    7. Verify old tokens are invalidated
    8. Login with new password
    9. Verify account is active and unlocked
  - Scenario 2 (error paths):
    - Invalid email format → 400
    - Weak password → 400
    - Duplicate email → 409
    - Incorrect password → 401 (no info leakage)
    - Expired reset token → 400
    - Revoked refresh token (replay) → 401
  - Assertion checklist: SC-1 through SC-9
- **Acceptance**: All scenarios pass; lifecycle completes successfully
- **Owner**: QA Engineer / Backend Engineer
- **Estimated Effort**: 4-5 days
- **Wiring Artifacts**: None (tests verify end-to-end flow)

#### Phase 5.4: Security & Compliance Testing
- **Coverage**: Risk mitigation validation, OWASP top 10 prevention
- **Deliverables**:
  - `tests/security/password-policy.test.ts`: enforce FR-AUTH.2c policy (8+ chars, 1 upper, 1 lower, 1 digit)
  - `tests/security/xss-prevention.test.ts`: verify access token not in response body (in-memory storage); refresh token in httpOnly cookie only (FR-AUTH.1-IMPL-2)
  - `tests/security/replay-detection.test.ts`: attempt reuse of rotated refresh token; verify all user tokens revoked (FR-AUTH.3c)
  - `tests/security/information-leakage.test.ts`: verify FR-AUTH.1b (no password/email difference on 401); no sensitive fields in profile (FR-AUTH.4c); rate limit doesn't reveal user existence
  - `tests/security/jwt-validation.test.ts`: tampered JWT rejected; expired JWT rejected; invalid signature rejected
  - `tests/security/bcrypt-config.test.ts`: verify cost factor 12 (NFR-AUTH.3); timing ≈250ms
  - Assertion checklist: RISK-1, RISK-2, RISK-3 mitigations verified
- **Acceptance**: All security tests pass; no information leakage observed
- **Owner**: Security Engineer / Backend Engineer
- **Estimated Effort**: 3-4 days
- **Wiring Artifacts**: None (tests verify security properties)

#### Phase 5.5: Performance & Load Testing
- **Coverage**: NFR-AUTH.1 (p95 latency < 200ms)
- **Deliverables**:
  - `tests/performance/load-test.k6.js` (using k6 tool per spec):
    - Simulate concurrent login requests: 50-500 concurrent users
    - Measure p50, p95, p99 latency for login, token refresh, profile endpoints
    - Target: p95 < 200ms under normal load (defined as 50-100 concurrent users)
    - Failure rate: < 0.1%
  - Benchmark test for password hashing: confirm ~250ms per bcrypt(cost=12) operation
  - Benchmark test for JWT signing/verification: < 50ms per operation
  - Load test results report: latency distribution, throughput, error rates
- **Acceptance**: p95 latency < 200ms confirmed; no performance regressions from baseline
- **Owner**: Performance Engineer / QA Engineer (DevOps specialist preferred)
- **Estimated Effort**: 3-4 days
- **Wiring Artifacts**: None (tests verify performance)

#### Phase 5 Gate: Test Coverage & Readiness
- **Gate Activities**:
  - Coverage report review: confirm 90%+ coverage on units, 95%+ on critical paths
  - Test quality review: tests are independent, deterministic, maintainable
  - Performance validation: confirm NFR-AUTH.1 met under load
  - Security validation: confirm all RISK and OWASP mitigations tested
  - Regression test plan: define tests to run in CI/CD pipeline (Phase 6)
- **Exit Criteria**: All test suites pass; coverage targets met; performance validated; security mitigations verified

---

### Phase 6: Deployment, Monitoring & Documentation (Weeks 7-8)
**Objective**: Production readiness, deployment, monitoring, and documentation.

#### Phase 6.1: Production Configuration & Secrets Management
- **Component**: Production environment setup
- **Deliverables**:
  - Secrets manager integration (e.g., AWS Secrets Manager, HashiCorp Vault):
    - RSA private key for JWT signing (RISK-1 mitigation: restrict access, enable audit logging)
    - Database connection string (credentials, connection pool settings)
    - Email service API key (if external service)
    - Feature flag overrides
  - Configuration management:
    - Development: in-memory secrets, test database
    - Staging: secrets manager, staging database
    - Production: secrets manager, production database
  - Key rotation implementation (RISK-1 mitigation):
    - Automated key rotation on 90-day schedule (NFR-AUTH-IMPL-2)
    - Grace period for key transitions (old key accepted for verification during rotation window)
    - Rotation logging and alerting
  - Documentation: secrets manager setup, key rotation schedule, emergency key recovery procedure
- **Acceptance**: Secrets are not in code/logs; key rotation works; access audit logs are populated
- **Owner**: DevOps Engineer / Security Engineer
- **Risk Owners**: RISK-1 (JWT secret compromise) — mitigation via secrets manager + rotation
- **Estimated Effort**: 3-4 days
- **Wiring Artifacts**: None (infrastructure setup)

#### Phase 6.2: Monitoring & Alerting
- **Component**: Observability setup
- **Deliverables**:
  - Application metrics:
    - Login success/failure rate
    - Token refresh rate
    - Password reset rate (broken down by request/confirm steps)
    - API endpoint latency (p50, p95, p99)
    - Rate limit trigger count
    - Error rate by endpoint
  - Security metrics:
    - Failed login attempts (by IP, by email)
    - Suspicious token reuse (refresh token replays)
    - Account lockout events (if implemented)
    - Secrets manager access audit log
  - Health checks:
    - Periodic login test (synthetic transaction)
    - Database connectivity check
    - Email service connectivity check
    - Secrets manager connectivity check
  - Alerting thresholds:
    - Login error rate > 5% → critical alert
    - API p95 latency > 300ms → warning alert
    - Refresh token replay detected → security alert
    - Email service failures → warning alert
    - Database connection failures → critical alert
  - Dashboards: Grafana/CloudWatch dashboard showing key metrics
  - Documentation: alerting runbook (what to do when alert fires)
- **Acceptance**: Metrics are populated; alerts fire correctly; dashboards are readable
- **Owner**: DevOps Engineer / SRE Engineer
- **Risk Owners**: NFR-AUTH.2 (uptime 99.9%) — mitigation via monitoring and alerting; RISK-2 (replay attacks) — detection via metrics
- **Estimated Effort**: 3-4 days
- **Wiring Artifacts**: None (infrastructure setup)

#### Phase 6.3: Deployment Pipeline & Rollout Strategy
- **Component**: CI/CD configuration
- **Deliverables**:
  - CI pipeline (GitHub Actions, GitLab CI, or equivalent):
    - Run all test suites (unit, integration, e2e, security, performance)
    - Lint and format checks
    - Coverage report (fail if < 90%)
    - Build Docker image or deployable artifact
    - Push to artifact repository (ECR, Docker Hub, etc.)
  - CD pipeline:
    - Staging deployment: run full test suite against staging environment
    - Production deployment (with feature flag gating):
      1. Deploy with `AUTH_SERVICE_ENABLED=false` (no traffic routed to new service)
      2. Run smoke tests and manual validation
      3. Gradually enable flag: 10% traffic → monitor metrics for 1 hour
      4. Ramp to 50% → monitor for 1 hour
      5. Ramp to 100% → full cutover
    - Rollback procedure: set `AUTH_SERVICE_ENABLED=false`, redeploy
  - Deployment documentation: step-by-step deployment guide, rollback procedure, troubleshooting
  - Feature flag management: UI or CLI tool to manage flag state without redeployment (optional, for faster rollbacks)
- **Acceptance**: CI pipeline passes for all commits; staged deployment works; rollback is fast (< 5 min)
- **Owner**: DevOps Engineer
- **Risk Owners**: All risks (controlled rollout + feature flag enables fast mitigation)
- **Estimated Effort**: 3-4 days
- **Wiring Artifacts**: None (CI/CD configuration)

#### Phase 6.4: Documentation & Runbooks
- **Component**: Documentation deliverables
- **Deliverables**:
  - **API Documentation**:
    - OpenAPI/Swagger spec for all /auth/* endpoints
    - Request/response examples for each endpoint
    - Error codes and meanings (401, 403, 409, 400, 429, 503)
    - Rate limiting policy and behavior
  - **Architecture Documentation**:
    - Service dependency diagram (Phase 3.4 DI container)
    - Sequence diagrams: login flow, token refresh, password reset, replay detection
    - Database schema documentation (users, refresh_tokens, reset_tokens tables)
  - **Operational Runbooks**:
    - How to deploy new version
    - How to rollback using feature flag
    - How to monitor key metrics
    - How to respond to security alerts (replay detected, rate limit spike, etc.)
    - How to manage secrets and rotate JWT key
    - How to investigate failed authentication attempts
  - **Security Documentation**:
    - Threat model (per RISK-1, RISK-2, RISK-3, RISK-4)
    - Security controls mapping (which control mitigates which risk)
    - Compliance checklist (OWASP top 10, etc.)
    - Incident response plan for compromised JWT key
  - **Developer Guide**:
    - How to add new endpoints to auth service
    - How to extend authentication (e.g., add OAuth support in future)
    - How to write tests for auth components
    - Local development setup instructions
- **Acceptance**: Documentation is complete, accurate, and accessible
- **Owner**: Technical Writer / Backend Engineer
- **Estimated Effort**: 3-4 days
- **Wiring Artifacts**: None (documentation artifacts)

#### Phase 6.5: Post-Deployment Validation & Optimization
- **Component**: Production verification
- **Deliverables**:
  - Initial deployment validation (first 24 hours):
    - Confirm no alert spikes
    - Verify login success rate > 99% (except rate-limited requests)
    - Confirm API latency p95 < 200ms
    - Spot-check database for correct data (passwords hashed, tokens stored correctly)
    - Test manual scenarios: register, login, profile, refresh, password reset, replay detection
  - Week 1 optimization review:
    - Identify any performance bottlenecks (if p95 latency creeping up)
    - Check error logs for any systemic issues
    - Review metrics for unexpected patterns
    - Optimize database indexes or queries if needed
  - Month 1 retrospective:
    - Confirm NFR-AUTH.2 (99.9% uptime) is on track
    - Identify any operational gaps (missing monitoring, unclear runbooks, etc.)
    - Plan v1.1 improvements (GAP-1, GAP-2, GAP-3)
- **Acceptance**: Deployment is stable; no critical issues in first month; metrics match expectations
- **Owner**: DevOps Engineer / Backend Engineer
- **Estimated Effort**: Ongoing (1-2 hours per day for first week, then weekly reviews)
- **Wiring Artifacts**: None (operational activity)

#### Phase 6 Gate: Production Readiness
- **Gate Activities**:
  - Secrets manager integration verified; keys secured and rotated
  - Monitoring and alerting configured; dashboards populated
  - CI/CD pipeline working end-to-end
  - Documentation complete and reviewed
  - Deployment plan approved and rehearsed
  - Team is trained on runbooks and incident response
- **Exit Criteria**: All Phase 6 deliverables complete; production infrastructure ready; team trained; green light for go-live

---

## Risk Assessment & Mitigation Strategies

| Risk ID | Risk | Severity | Probability | Mitigation Strategy | Residual Risk | Responsible |
|---------|------|----------|-------------|--------------------|--------------------|-------------|
| RISK-1 | JWT secret key compromise | HIGH | Low | Use RS256 asymmetric keys; store private key in secrets manager; implement 90-day key rotation (Phase 6.1); restrict access with audit logging; emergency key recovery procedure | Key rotation gap window (max 90 days); compromised secrets manager | Security Engineer + DevOps Engineer |
| RISK-2 | Refresh token replay attack | HIGH | Medium | Refresh token rotation with hash-based revocation (Phase 1.1, Phase 3.3); atomic database transactions; replay detection metrics (Phase 6.2); immediate revocation of all user tokens on suspicious reuse | Window between theft and detection (minutes); detection relies on monitoring | Backend Engineer + SRE Engineer |
| RISK-3 | bcrypt cost factor obsolescence | MEDIUM | Low | Configurable cost factor with defaults (Phase 0.2); annual review trigger; migration path documented; performance benchmarks in CI (Phase 5.5) | Requires proactive annual review; migration requires careful rollout | Backend Engineer + DevOps Engineer |
| RISK-4 | Email service dependency (implicit) | MEDIUM | Medium | Async dispatch via message queue (OI-1 resolution, Phase 4.1); fallback error handling; service monitoring and alerting (Phase 6.2); consider DNS/SMTP retry mechanism | Email delivery failures block password reset; no fallback defined in spec | Backend Engineer + DevOps Engineer |
| RISK-5 | Account takeover via brute-force | MEDIUM | Medium | Rate limiting (5/min/IP, Phase 2.3); account lockout after N failures (GAP-1, deferred to v1.1); progressive backoff for failed attempts | Rate limiting doesn't prevent distributed attacks; account lockout not yet implemented | Backend Engineer |
| RISK-6 | Insufficient password entropy | MEDIUM | Low | Password policy enforcement (8+ chars, 1 upper, 1 lower, 1 digit, Phase 0.2); configuration via environment variable; documented OWASP guidelines | Policy is conservative; real-world breaches suggest stronger policies needed (Phase 2.0+) | Security Engineer |

---

## Resource Requirements & Dependencies

### Team Composition

| Role | Count | Key Responsibilities | Phases |
|------|-------|----------------------|--------|
| Backend Engineer (Cryptography) | 1 | JWT service, password hasher, security validation | 0, 5.4 |
| Backend Engineer (Services Architect) | 1 | Token manager, auth service, feature flag | 1, 4, 5.1 |
| Backend Engineer (API/Middleware) | 1 | Routes, middleware, rate limiting, error handling | 2, 5.1 |
| Database Engineer | 1 | Schema design, migrations, integration | 3 |
| Backend Engineer (QA/Testing) | 1 | Unit/integration/e2e tests, security tests | 5 |
| Performance Engineer | 1 | Load testing, optimization, benchmarks | 5.5 |
| DevOps Engineer | 1 | Infrastructure, secrets, CI/CD, monitoring | 6, 3 |
| Security Engineer | 1 | Code review, threat modeling, compliance | 0, 6.1 |
| Technical Writer | 1 | API docs, runbooks, architecture docs | 6.4 |

**Total: 9 roles (can be consolidated to 5-6 engineers if cross-skilled)**

### External Dependencies

| Dependency | Purpose | Phase | Status | Mitigation |
|------------|---------|-------|--------|-----------|
| `jsonwebtoken` npm library | JWT RS256 signing/verification | 0.1 | Available | Use latest stable version; security audits in CI |
| `bcrypt` npm library | Password hashing | 0.2 | Available | Use latest stable version; benchmark against alternatives (Argon2) |
| Database (PostgreSQL/MySQL) | User + token storage | 3 | Pre-existing (assumed) | Ensure connection pooling configured; backup/restore procedures |
| Email service (SendGrid, Mailgun, etc.) | Password reset emails | 4.1 | To be chosen | Abstract interface; mock in tests; fallback to sync dispatch if async queue not available |
| Secrets manager (AWS Secrets Manager, Vault) | Store RSA private key | 6.1 | To be chosen | Ensure audit logging enabled; key rotation tooling available |
| Load testing tool (k6) | Performance validation | 5.5 | Available | Install via npm; scripts provided in deliverables |
| Message queue (optional, for async email) | Async password reset dispatch | 4.1 | Optional | Deferred to v1.0 if not available; sync dispatch as fallback (OI-1) |

### Infrastructure Requirements

| Component | Minimum Spec | Recommendation | Justification |
|-----------|--------------|-----------------|---------------|
| Application server memory | 512 MB | 2 GB | JWT signing/verification is CPU-bound; bcrypt hashing is CPU-bound; in-memory rate limiter needs space |
| Database connections | 5 | 20 | Single app instance needs 1-2; connection pool prevents exhaustion; load test requires many concurrent connections |
| Database storage | 100 MB | 1 GB | Users table grows linearly; refresh_tokens table can grow with concurrent sessions; reset_tokens table is temporary |
| Secrets manager | 1 RSA key + 2 connection strings | 5+ secrets (includes future API keys) | Initial: JWT key, DB creds, email key; future: session store creds, external API keys |
| Monitoring (Prometheus/CloudWatch) | 5 GB/month | 50 GB/month | Metrics: 100+ time series × 60 queries/day × 30 days; logs: authentication events |
| Log aggregation (ELK, DataDog) | 1 GB/month | 10 GB/month | Login/registration/password reset events; error logs; security audit logs |

---

## Success Criteria & Validation Approach

### Functional Validation (SC-1 through SC-5)

| Criterion | Validation Method | Phase | Owner |
|-----------|-------------------|-------|-------|
| **SC-1**: All 5 FRs pass acceptance criteria | Integration tests (Phase 5.2) + E2E tests (Phase 5.3) | 5 | QA Engineer |
| **SC-2**: p95 latency < 200ms (NFR-AUTH.1) | k6 load test (Phase 5.5); production APM (Phase 6.2) | 5, 6 | Performance Engineer |
| **SC-3**: 99.9% uptime (NFR-AUTH.2) | Uptime monitoring (Phase 6.2); measure over first 30 days | 6 | SRE Engineer |
| **SC-4**: bcrypt cost factor 12, ~250ms (NFR-AUTH.3) | Benchmark test (Phase 5.5); unit test (Phase 5.1) | 5 | Backend Engineer |
| **SC-5**: Unit tests pass | `uv run pytest tests/unit/` (Phase 5.1) | 5 | QA Engineer |

### Integration Validation (SC-6 through SC-8)

| Criterion | Validation Method | Phase | Owner |
|-----------|-------------------|-------|-------|
| **SC-6**: Integration tests pass | `uv run pytest tests/integration/` (Phase 5.2) | 5 | QA Engineer |
| **SC-7**: E2E lifecycle scenario passes | `uv run pytest tests/e2e/user-lifecycle.test.ts` (Phase 5.3); manual walkthrough (Phase 6.5) | 5, 6 | QA Engineer |
| **SC-8**: No sensitive fields exposed | Security tests (Phase 5.4); code review (Phase 0, Phase 3, Phase 6); response schema validation | 5 | Security Engineer |
| **SC-9**: Rollback via feature flag works | Rollback test (Phase 6.3); manual verification (Phase 6.5) | 6 | DevOps Engineer |

### Security Validation (Risk Mitigation)

| Risk | Validation Method | Phase | Owner |
|------|-------------------|-------|-------|
| RISK-1 (JWT compromise) | Secrets manager audit (Phase 6.1); key rotation test; emergency recovery drill | 6 | Security Engineer |
| RISK-2 (Replay attacks) | Replay detection test (Phase 5.4); concurrent token rotation test (Phase 5.2) | 5 | Backend Engineer |
| RISK-3 (Cost factor obsolescence) | Benchmark test (Phase 5.5); annual review checklist (Phase 6.4) | 5, 6 | Security Engineer |
| RISK-4 (Email dependency) | Email service failure test (Phase 5.2); alerting test (Phase 6.2) | 5, 6 | DevOps Engineer |

### Validation Checkpoints (Phase Gates)

| Gate | Activities | Criteria | Owner |
|------|-----------|----------|-------|
| **Phase 0 Gate** | Crypto code review, benchmark validation | All crypto tests pass; latencies meet targets | Security Engineer |
| **Phase 1 Gate** | Service integration testing, DI design review | Services compose correctly; mocked DB/email work | Backend Engineer |
| **Phase 2 Gate** | Route/middleware integration, security review | Routes return correct status codes; rate limiting works | Backend Engineer |
| **Phase 3 Gate** | Database schema review, migration testing | Schema matches service expectations; migrations reversible | Database Engineer |
| **Phase 4 Gate** | Feature flag testing, rollback verification | Flag gates routes; rollback behavior works | DevOps Engineer |
| **Phase 5 Gate** | Coverage report, performance validation | 90%+ coverage; NFR-AUTH.1 met; security tests pass | QA Engineer |
| **Phase 6 Gate** | Production readiness review, team training | Secrets configured; monitoring ready; team trained | DevOps Engineer |

---

## Timeline Estimates

### Phase Durations

| Phase | Duration | Start | End | Slack | Rationale |
|-------|----------|-------|-----|-------|-----------|
| Phase 0 (Crypto) | 1.5 weeks | Week 0 | Week 1.5 | 2 days | Well-understood, high risk; conservative estimate |
| Phase 1 (Services) | 1.5 weeks | Week 1.5 | Week 3 | 2 days | Moderate complexity; token rotation requires care |
| Phase 2 (Routes/Middleware) | 1 week | Week 3 | Week 4 | 1 day | Straightforward after Phase 1 |
| Phase 3 (Database) | 1.5 weeks | Week 4 | Week 5.5 | 1 day | Schema design + integration is critical path |
| Phase 4 (Advanced) | 1 week | Week 5.5 | Week 6.5 | 1 day | Password reset + feature flag; low risk |
| Phase 5 (Testing) | 1.5 weeks | Week 6.5 | Week 8 | 2 days | Testing is comprehensive; may run in parallel with Phase 4 |
| Phase 6 (Deploy) | 1 week | Week 8 | Week 9 | 2 days | Infrastructure + monitoring; can start in Phase 5 |

**Critical Path**: Phase 0 → Phase 1 → Phase 3 (database integration) → Phase 6 (deployment) = 5.5 weeks minimum

**Parallel Opportunities**:
- Phase 2 (Routes) can start during Phase 1 (Services) once interface contracts are defined (~Week 1.5)
- Phase 5 (Testing) can start during Phase 2-3 (begin with unit tests in Phase 0-1)
- Phase 6 (Deployment setup) can start during Phase 4-5 (early infrastructure provisioning)

**Optimized Timeline with Parallelization**:
- Weeks 0-1.5: Phase 0 (Crypto) + early Phase 1 (Service contracts)
- Weeks 1.5-3: Phase 1 (Services) + Phase 2 (Routes in parallel) + Phase 5.1 (Unit tests start)
- Weeks 3-5.5: Phase 3 (Database) + Phase 5.2 (Integration tests) + Phase 6 infrastructure planning
- Weeks 5.5-7.5: Phase 4 (Advanced) + Phase 5.3-5.5 (E2E, security, performance tests) + Phase 6 setup
- Weeks 7.5-9: Phase 6 (Deployment, monitoring, documentation) + Phase 5 final validation

**Total Duration: 8-9 weeks (6 weeks critical path + slack)**

---

## Critical Path & Dependency Chain

```
Phase 0 (Crypto Foundation)
├─ JWT Service [3-4 days]
└─ Password Hasher [2-3 days]
    ↓
Phase 1 (Core Services)
├─ Token Manager [4-5 days] (depends on JWT Service)
└─ Auth Service [5-6 days] (depends on Token Manager, Password Hasher)
    ├─ Phase 2 Routes [3-4 days] (can start after Auth Service interface is defined)
    ├─ Phase 2 Middleware [2-3 days]
    └─ Phase 3 Database Integration [4-5 days] (Phase 3.1 schema parallel with Phase 1)
        ├─ Phase 3.2 AuthService DB integration [3-4 days]
        ├─ Phase 3.3 TokenManager DB integration [4-5 days]
        └─ Phase 3.4 DI Container setup [2-3 days]
            ↓
Phase 4 (Advanced Features)
├─ Password Reset [5-6 days] (depends on Token Manager, Auth Service)
└─ Feature Flag [1-2 days]
    ↓
Phase 5 (Testing — can start after Phase 1, run in parallel with Phase 3-4)
├─ Unit Tests [5-6 days] (depends on Phase 0-1)
├─ Integration Tests [6-7 days] (depends on Phase 3)
├─ E2E Tests [4-5 days] (depends on Phase 4)
├─ Security Tests [3-4 days] (depends on Phase 0-4)
└─ Performance Tests [3-4 days] (depends on Phase 3)
    ↓
Phase 6 (Deployment — can start in Phase 5)
├─ Secrets & Config [3-4 days]
├─ Monitoring & Alerting [3-4 days]
├─ CI/CD Pipeline [3-4 days]
├─ Documentation [3-4 days]
└─ Post-Deployment [ongoing]
```

### Critical Blocking Points

1. **Phase 0 → Phase 1**: JWT Service must be complete before Token Manager can be tested
2. **Phase 1 → Phase 3**: Service interfaces must be finalized before database integration
3. **Phase 3 → Phase 4**: Database must be working before password reset (external service) can be integrated
4. **Phase 1-4 → Phase 5**: All features must be implemented before comprehensive testing
5. **Phase 5 → Phase 6**: Testing must pass before deployment to production

---

## Appendix: Architectural Wiring Diagrams

### Dependency Injection Container (Phase 3.4)

```
DI Container (src/di/container.ts)
├─ JwtService (singleton)
│  └─ Used by: TokenManager, Auth routes
├─ PasswordHasher (singleton)
│  └─ Used by: AuthService, Password reset
├─ Database Client (singleton)
│  └─ Used by: AuthService, TokenManager, Password reset
├─ TokenManager (singleton, depends on JwtService, Database)
│  └─ Used by: AuthService, Auth routes, Password reset
└─ AuthService (singleton, depends on TokenManager, PasswordHasher, Database, JwtService)
   └─ Used by: Auth routes, Middleware
```

### Request Flow (Login)

```
HTTP: POST /auth/login
├─ Rate limiter middleware (5/min/IP)
│  └─ Limit exceeded? → 429
├─ Input validation middleware
│  └─ Invalid email/password format? → 400
├─ Route handler
│  └─ Call AuthService.login(email, password)
│     ├─ Query Database: User by email
│     │  └─ Not found? → (no info leak) return error
│     ├─ Call PasswordHasher.compare(password, stored_hash)
│     │  └─ Mismatch? → (no info leak) return 401
│     ├─ Check user.is_locked
│     │  └─ Locked? → return 403
│     ├─ Call TokenManager.issueAccessToken(userId)
│     │  └─ Call JwtService.sign({ userId, exp: now+15min })
│     │     └─ Use RSA private key from secrets manager
│     └─ Call TokenManager.issueRefreshTokenPair(userId)
│        ├─ Generate random token
│        ├─ Hash token (SHA-256)
│        └─ Insert into refresh_tokens table
├─ Response handler
│  ├─ Set Cookie: refresh_token (httpOnly, secure, SameSite=Strict)
│  └─ Return 200 with access_token + user profile (no sensitive fields)
```

### Token Refresh Flow (Rotation)

```
HTTP: POST /auth/refresh
├─ Auth middleware
│  └─ Extract refresh_token from cookie
├─ Route handler
│  └─ Call TokenManager.rotateRefreshToken(refreshToken, userId)
│     ├─ Hash token (SHA-256)
│     ├─ Query refresh_tokens: WHERE token_hash = ? AND user_id = ?
│     │  └─ Not found? → 401
│     ├─ Check is_revoked
│     │  └─ Revoked? → SECURITY ALERT: Replay attack detected
│     │     └─ Call TokenManager.revokeAllUserTokens(userId)
│     │        └─ Update refresh_tokens: SET is_revoked=true WHERE user_id = ?
│     │        └─ Return 401 (all tokens revoked)
│     ├─ Check expiration
│     │  └─ Expired? → 401
│     ├─ [BEGIN TRANSACTION]
│     ├─ Update refresh_tokens: SET is_revoked=true WHERE id = ?
│     ├─ Call TokenManager.issueAccessToken(userId)
│     ├─ Call TokenManager.issueRefreshTokenPair(userId)
│     │  └─ Insert into refresh_tokens table
│     └─ [COMMIT TRANSACTION]
└─ Response handler
   ├─ Set Cookie: new refresh_token
   └─ Return 200 with new access_token
```

### Password Reset Flow

```
HTTP: POST /auth/password-reset/request
├─ Route handler
│  └─ Call PasswordResetService.requestReset(email)
│     ├─ Query Database: User by email (don't reveal if found)
│     ├─ Generate reset token (JWT with userId claim, 1h TTL)
│     ├─ Hash token (SHA-256)
│     ├─ Insert into reset_tokens table
│     ├─ [ASYNC] Call EmailService.dispatch(email, resetLink)
│     │  └─ Link contains reset token
│     └─ Return 200 (always, whether user exists or not)

HTTP: POST /auth/password-reset/confirm
├─ Route handler
│  └─ Call PasswordResetService.confirmReset(resetToken, newPassword)
│     ├─ Validate reset token (JWT verify)
│     │  └─ Expired? → 400
│     ├─ Query reset_tokens: WHERE token_hash = ?
│     │  └─ Not found? → 400
│     ├─ Check is_used
│     │  └─ Already used? → 400
│     ├─ Validate password policy
│     │  └─ Invalid? → 400
│     ├─ [BEGIN TRANSACTION]
│     ├─ Call PasswordHasher.hash(newPassword)
│     ├─ Update users: SET password_hash = ? WHERE id = ?
│     ├─ Update reset_tokens: SET is_used=true WHERE id = ?
│     ├─ Call TokenManager.revokeAllUserTokens(userId)
│     │  └─ Invalidate all refresh tokens
│     └─ [COMMIT TRANSACTION]
└─ Response handler
   └─ Return 200 with success message (or auto-login tokens)
```

---

## Open Questions & Recommendations

### Spec Ambiguities (from Extraction OQ-1 through OQ-5)

1. **OQ-1**: Define "normal load" for NFR-AUTH.1
   - **Recommendation**: Set to 50-100 concurrent users; k6 test script should validate p95 < 200ms at this level
   - **Phase**: 5.5 (performance testing)
   - **Action**: Add to Phase 5.5 deliverables: load test configuration with defined user counts

2. **OQ-2**: RSA key size for RS256
   - **Recommendation**: 4096-bit (future-proof against hardware advances); 2048-bit minimum
   - **Phase**: 0.1 (JWT service)
   - **Action**: Configuration parameter in Phase 4.3; default to 4096-bit

3. **OQ-3**: Per-account rate limiting (distributed brute-force)
   - **Recommendation**: Add per-account rate limiting (e.g., 10 failures/hour locks account for 30 min)
   - **Phase**: 1.2 (Auth service); currently deferred to v1.1 as GAP-1
   - **Action**: Add to Phase 4.3 advanced configuration; roadmap inclusion in v1.1

4. **OQ-4**: Password reset link/code mechanism
   - **Recommendation**: Token-based link (easier for users than code entry); implement in Phase 4.1 with configurable TTL
   - **Phase**: 4.1 (password reset)
   - **Action**: Include in password reset deliverables

5. **OQ-5**: Refresh token transport (httpOnly cookie vs. JSON response)
   - **Recommendation**: Use httpOnly cookie (CSRF-proof); JSON response is an anti-pattern
   - **Phase**: 2.2 (middleware); 4.1 (reset response)
   - **Action**: Clear documentation in Phase 6.4; middleware enforces httpOnly cookies

### Deferred Items (v1.1 and Beyond)

| Item | Reason | Estimated Effort | v1.1 Roadmap |
|------|--------|------------------|--------------|
| **GAP-1**: Account lockout after N failures | Security hardening; requires careful UI/UX | 3-4 days | Q3 2026 |
| **GAP-2**: Audit logging for auth events | Compliance/observability; low immediate impact | 2-3 days | Q3 2026 |
| **GAP-3**: Token revocation on user deletion | Data integrity; requires cascade logic | 1-2 days | Q2 2026 |
| **OI-2**: Max active refresh tokens per user | Multi-device support; need architecture review | 2-3 days | Q2 2026 |
| **RISK-3 Mitigation**: Migration to Argon2id | Future-proofing; not urgent | 3-4 days | Q4 2026 annual review |
| **OAuth/Social Login**: Support external providers | Market request; out of scope v1.0 | 5-7 days | v2.0 |
| **RBAC**: Role-based access control | Enterprise feature; out of scope v1.0 | 8-10 days | v2.0 |

---

## Success Definition

The authentication system is **production-ready** when:

1. **Functional completeness**: All 5 FRs + 3 NFRs meet acceptance criteria; all 9 success criteria validated
2. **Security assurance**: All 4 identified risks mitigated and tested; no information leakage; OWASP top 10 controls in place
3. **Operational readiness**: Monitoring + alerting configured; runbooks written; team trained; rollback tested
4. **Quality standards**: Test coverage 90%+ (units), 95%+ (critical paths); performance validated (p95 < 200ms); security code review passed
5. **Stability**: First 30 days in production with 99.9%+ uptime; error rate < 0.1%; no security incidents

**Go/No-Go Decision**: Phase 6 gate approval + production readiness checklist sign-off by DevOps + Security + Backend lead engineers.
