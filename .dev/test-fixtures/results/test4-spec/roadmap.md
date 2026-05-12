---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
adversarial: true
base_variant: "opus-architect"
merge_source: "haiku-architect"
primary_persona: architect
generated: "2026-04-15"
generator: "superclaude-roadmap/merge"
total_phases: 6
total_task_rows: 101
extraction_ids_preserved: 55
derived_entity_ids: 46
convergence_score: 0.62
debate_rounds: 2
---

# Project Roadmap: User Authentication Service (Merged)

## 1. Executive Summary

This roadmap covers the implementation of a JWT-based authentication service for the platform, encompassing user registration, login, token lifecycle management, profile retrieval, and password reset. The service introduces two new database tables, five API endpoints, and a middleware integration — all scoped to a well-bounded auth module with no OAuth, MFA, or RBAC in v1.0.

**Complexity**: MEDIUM (0.6) — the architectural footprint is modest, but security sensitivity drives the bulk of the effort. Cryptographic operations (RS256, bcrypt), stateful token rotation with replay detection, and a latency constraint that conflicts with the hashing budget (NFR-AUTH.1 vs NFR-AUTH.3) require careful resolution before implementation begins.

### Architectural Priorities

1. **Security correctness before feature breadth** — RS256 key custody, refresh-token hashing, replay detection, enumeration resistance, and session invalidation are the critical-path controls. Security-sensitive interfaces (JWT signing, token management) receive explicit contract definitions before implementation.
2. **Explicit state boundaries** — Access tokens remain stateless JWTs, while refresh-token lifecycle and password reset flows rely on durable database-backed state.
3. **Integration visibility** — Named artifacts (`SecurityServiceContainer`, `AuthRouteRegistry`, `AuthMiddlewareChain`) make wiring decisions explicit and auditable across phases.
4. **Validation-led delivery** — A test strategy matrix is defined in Phase 0; unit and integration tests are co-located with implementation; cross-cutting security, load, E2E, and regression tests consolidate in Phases 4–5. Open question decisions receive evidence-based validation before release.
5. **Operational completeness** — The roadmap delivers through production deployment, including feature flag rollout, staging smoke tests, and monitoring activation.

**Critical Path**: Open Question resolution (Phase 0) → Security contracts + Database schema + core services (Phase 0) → Registration + Login (Phase 1) → Token refresh + Profile (Phase 2) → Password reset (Phase 3) → NFR hardening (Phase 4) → Validation + OQ closure + Deploy (Phase 5).

**Key Risks**:
- The bcrypt latency (~250ms at cost 12) exceeds the 200ms p95 target — architectural resolution required before Phase 1
- Email service interface is undefined, blocking FR-AUTH.5 completion
- No account lockout policy leaves distributed brute-force attack surface open
- Refresh token replay remains the highest residual risk after mitigation

### Merge Provenance

This roadmap uses the Opus-architect variant (score: 81.6) as its structural foundation and incorporates targeted improvements from the Haiku-architect variant (score: 78.6) identified through structured adversarial debate (convergence: 0.62 after 2 rounds). Incorporated from Haiku: early feature flag, security-interface contracts for JWT and TokenManager, test strategy matrix, test fixture planning, evidence-based OQ closure, mid-phase checkpoint, named integration artifacts, and explicit release gate criteria.

---

## 2. Integration Points

### 2.1 SecurityServiceContainer

- **Named Artifact**: `SecurityServiceContainer` — central service registry for all auth module dependencies
- **Wired Components**: `JwtService` (COMP-002), `TokenManager` (COMP-003), `PasswordHasher` (COMP-001), secrets provider (OPS-002), rate limiter (FR-AUTH.1d)
- **Owning Phase**: Phase 0 creates all services and registers them; Phase 3 adds `EmailAdapter` (COMP-007)
- **Cross-Reference**: Phase 1–3 endpoint handlers resolve services from the container; Phase 4 hardening tasks modify service configuration; Phase 5 E2E tests validate the full container

### 2.2 AuthMiddlewareChain

- **Named Artifact**: `AuthMiddlewareChain` — middleware pipeline in `src/middleware/index.ts`
- **Wired Components**: Bearer token extractor, JWT verifier (via `JwtService`), user context loader, unauthorized-response guard
- **Owning Phase**: Phase 0 creates `auth-middleware.ts` (COMP-004); Phase 0 wires it into the Express pipeline (COMP-005)
- **Cross-Reference**: Phase 1 routes bypass middleware (login/register are public); Phase 2 routes consume middleware (profile is protected); Phase 3 reset-request is public, reset-confirm uses reset token (not Bearer); Phase 5 regression tests verify middleware ordering with feature flag on/off

### 2.3 AuthRouteRegistry

- **Named Artifact**: `AuthRouteRegistry` — route group in `src/routes/index.ts`, `/auth/*` prefix
- **Wired Components**: POST `/auth/register` (API-001), POST `/auth/login` (API-002), POST `/auth/refresh` (API-003), GET `/auth/profile` (API-004), POST `/auth/reset-request` (API-005), POST `/auth/reset-confirm` (API-006)
- **Owning Phase**: Phase 0 creates the `/auth/*` group placeholder (COMP-006) and feature flag gate (OPS-009); Phases 1–3 register individual routes
- **Cross-Reference**: All phases add routes; Phase 4 load tests exercise all registered routes; Phase 5 E2E test traverses the full route set; feature flag (OPS-009) gates the entire route group

### 2.4 TokenManager Service Wiring

- **Named Artifact**: `TokenManager` service (COMP-003) — orchestrates access and refresh token lifecycle
- **Wired Components**: `JwtService` (COMP-002) for RS256 signing/verification; `PasswordHasher` (COMP-001) consumed by login/register handlers; `RefreshToken` repository backed by DM-002
- **Owning Phase**: Phase 0 defines contract (CONT-002), then creates the service; Phases 1–3 consume it from endpoint handlers
- **Cross-Reference**: Phase 2 exercises token rotation and replay detection through TokenManager; Phase 3 triggers full revocation through TokenManager on password reset; contract (CONT-002) reviewed by security engineer before implementation

### 2.5 Email Service Adapter

- **Named Artifact**: `EmailService` interface + adapter (COMP-007) — strategy pattern for email dispatch
- **Wired Components**: Concrete adapter wired per OQ-1 decision (synchronous HTTP or async message queue)
- **Owning Phase**: Phase 3 defines the interface and implements the adapter
- **Cross-Reference**: Phase 4 implements degradation handling (R-5); Phase 5 E2E test validates email dispatch invocation; OQ-1-VAL provides evidence-based closure on dispatch mode

---

## 3. Phased Implementation Plan

### Phase 0: Foundation, Architecture Resolution & Security Contracts

**Objective**: Resolve architectural ambiguities, define security-critical interface contracts, provision infrastructure, build core service components, establish test strategy, and enable feature flag — all before any endpoint work begins.

**Duration**: 1.5 weeks

**Milestone**: All open questions documented with decisions; security-interface contracts (JWT, TokenManager) reviewed and approved; database migration runs cleanly; PasswordHasher, JwtService, and TokenManager pass unit tests; auth-middleware wired into pipeline; test strategy matrix defined; feature flag operational.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|------|------|-----------|--------------|---------------------|--------|----------|
| 1 | OQ-3 | Resolve latency conflict between NFR-AUTH.1 (< 200ms p95) and NFR-AUTH.3 (bcrypt cost 12 ~250ms) | Architecture | — | Decision documented: async hashing, adjusted p95 target, or reduced cost factor; stakeholder sign-off obtained | S | P0 |
| 2 | OQ-1 | Decide sync vs async password reset email dispatch | Architecture | — | Decision documented: synchronous HTTP or message queue; infrastructure implications identified | S | P1 |
| 3 | OQ-2 | Define maximum active refresh tokens per user | Architecture | — | Numeric limit defined (e.g., 10); cleanup strategy for excess tokens documented | S | P1 |
| 4 | OQ-7 | Define email service interface contract (SDK, API, or SMTP) | Architecture | OQ-1 | Interface specified with method signatures, error types, and retry semantics | S | P1 |
| 5 | OQ-4 | Define progressive account lockout policy beyond rate limiting | Architecture | — | Policy specified: threshold (e.g., 10 failures/hour across all IPs), lockout duration, unlock mechanism | S | P1 |
| 6 | OQ-5 | Define token revocation policy on user account deletion | Architecture | — | Policy documented: immediate revocation vs expiry-based; implementation approach chosen | S | P2 |
| 7 | OQ-6 | Decide on audit logging scope for authentication events | Architecture | — | Decision documented: deferred to v1.1 or minimal logging scoped for v1.0 | S | P2 |
| 8 | OQ-8 | Define RSA key rotation procedure with key versioning strategy | Architecture | — | Rotation mechanism documented; key ID (kid) in JWT header specified; zero-downtime rotation plan confirmed | M | P1 |
| 9 | TEST-ARCH-001 | Define test strategy matrix across unit/integration/security/load/E2E | QA Architecture | OQ-3, OQ-1 | Test inventory maps every FR/NFR to verification type, environment, and owning phase; coverage gaps identified before implementation begins | M | P0 |
| 10 | TEST-ARCH-002 | Define shared test fixtures for auth data and token lifecycle | QA Foundation | DM-001, DM-002, TEST-ARCH-001 | Fixtures cover: valid users, locked accounts, expired tokens, revoked sessions, active refresh tokens; reusable across Phases 1–5 test tasks | S | P1 |
| 11 | DM-001 | Design users database table schema | Database | OQ-5 | Schema: id (UUID PK), email (unique index), display_name, password_hash, created_at, locked_at (nullable); reviewed and approved | M | P0 |
| 12 | DM-002 | Design refresh_tokens database table schema | Database | OQ-2 | Schema: id (UUID PK), user_id (FK → users, indexed), token_hash (SHA-256), expires_at, revoked_at (nullable), created_at; reviewed and approved | M | P0 |
| 13 | MIG-001 | Create database migration 003 — up (create users and refresh_tokens tables) | Database | DM-001, DM-002 | Migration executes cleanly; tables created with correct columns, types, indexes, and foreign keys | M | P0 |
| 14 | MIG-002 | Create database migration 003 — down (rollback: drop tables) | Database | MIG-001 | Down-migration drops both tables cleanly with no orphaned objects; idempotent execution | S | P0 |
| 15 | OPS-001 | Generate RSA key pair for JWT RS256 signing | Infrastructure | — | 2048+ bit RSA key pair generated; private key not committed to repository | S | P0 |
| 16 | OPS-002 | Integrate secrets manager for RSA private key storage and retrieval | Infrastructure | OPS-001 | Private key stored in secrets manager; application retrieves key at startup; local dev fallback documented | M | P0 |
| 17 | CONT-001 | Define JWT service interface contract (RS256 signing, verification, key versioning) | Security Contract | OQ-8, OPS-002 | Interface specifies: sign(payload, ttl), verify(token), key versioning via kid header, TTL inputs, error types; reviewed and approved by security engineer | S | P0 |
| 18 | CONT-002 | Define TokenManager interface contract (access/refresh/reset token lifecycle) | Security Contract | CONT-001 | Interface specifies: issueTokenPair(userId), rotateRefreshToken(token), revokeAllUserTokens(userId), issueResetToken(userId); rotation and replay detection semantics explicit; reviewed and approved by security engineer | S | P0 |
| 19 | COMP-001 | Implement PasswordHasher service with configurable bcrypt cost factor | Auth Module | — | Exposes hash(password) and verify(password, hash); cost factor configurable via environment variable (default 12); TypeScript | M | P0 |
| 20 | COMP-002 | Implement JwtService with RS256 signing and verification | Auth Module | OPS-002, CONT-001 | Signs tokens with RS256 private key; verifies with public key; supports configurable TTL; includes kid header for key rotation; conforms to CONT-001 contract | M | P0 |
| 21 | COMP-003 | Implement TokenManager (access + refresh token orchestration) | Auth Module | COMP-002, CONT-002 | Generates access tokens (15min TTL) and refresh tokens (7d TTL); delegates signing to JwtService; stores refresh token hash via repository; conforms to CONT-002 contract | M | P0 |
| 22 | COMP-004 | Implement auth-middleware.ts (Bearer token extraction and JWT verification) | Middleware | COMP-002 | Extracts Bearer token from Authorization header; verifies JWT via JwtService; attaches decoded user context to request object; returns 401 on failure | M | P0 |
| 23 | COMP-005 | Wire auth-middleware into AuthMiddlewareChain | Middleware | COMP-004 | Middleware registered in AuthMiddlewareChain; protects routes marked as authenticated; passes through public routes (/auth/login, /auth/register) | S | P0 |
| 24 | COMP-006 | Register /auth/* route group in AuthRouteRegistry | Routes | — | Route group created and exported; ready for individual endpoint registration in subsequent phases | S | P0 |
| 25 | OPS-009 | Implement AUTH_SERVICE_ENABLED feature flag for auth route group | Runtime Config | COMP-006 | Feature flag gates /auth/* route group; defaults to enabled in development; toggleable without redeployment; flag-off returns 503 or routes to previous behavior; enables regression testing with flag on/off across all phases | S | P0 |

---

### Phase 1: Core Authentication — Registration & Login

**Objective**: Deliver working registration and login endpoints with full acceptance criteria coverage.

**Duration**: 1.5 weeks

**Milestone**: Users can register, login, and receive JWT tokens. All FR-AUTH.1 and FR-AUTH.2 acceptance criteria pass in integration tests.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|------|------|-----------|--------------|---------------------|--------|----------|
| 1 | FR-AUTH.2 | Implement user registration endpoint (POST /auth/register) | Auth API | COMP-001, COMP-003, MIG-001 | Endpoint scaffolded: accepts email, password, display_name; delegates to PasswordHasher and user repository | L | P0 |
| 2 | FR-AUTH.2a | Implement valid registration flow with user record creation and 201 response | Auth API | FR-AUTH.2 | Given valid data, user record created with hashed password; returns 201 with user profile (id, email, display_name, created_at) | M | P0 |
| 3 | FR-AUTH.2b | Implement duplicate email conflict detection (409 response) | Auth API | FR-AUTH.2, DM-001 | Given already-registered email, returns 409 Conflict; no partial user record created | S | P0 |
| 4 | FR-AUTH.2c | Implement password policy enforcement (min 8 chars, uppercase, lowercase, digit) | Auth API | FR-AUTH.2 | Passwords violating policy return 400 with specific violation message; boundary cases (7 chars, missing class) rejected | S | P0 |
| 5 | FR-AUTH.2d | Implement email format validation before registration attempt | Auth API | FR-AUTH.2 | Malformed emails rejected with 400 before any database interaction; RFC 5322 basic validation | S | P0 |
| 6 | API-001 | Wire POST /auth/register route in AuthRouteRegistry | Routes | COMP-006, FR-AUTH.2 | Route registered in /auth/* group; request dispatched to registration handler; no auth-middleware applied | S | P0 |
| 7 | FR-AUTH.1 | Implement user login endpoint (POST /auth/login) | Auth API | COMP-001, COMP-003, FR-AUTH.2 | Endpoint scaffolded: accepts email + password; verifies credentials via PasswordHasher; returns tokens via TokenManager | L | P0 |
| 8 | FR-AUTH.1a | Implement successful login returning access_token (15min TTL) and refresh_token (7d TTL) | Auth API | FR-AUTH.1, COMP-003 | Valid credentials return 200 with access_token and refresh_token; TTLs match specification; refresh_token set as httpOnly cookie | M | P0 |
| 9 | FR-AUTH.1b | Implement generic invalid credentials response (enumeration resistance) | Auth API | FR-AUTH.1 | Invalid email or password returns 401 with identical error message; response timing does not leak whether email exists | S | P0 |
| 10 | FR-AUTH.1c | Implement locked account rejection (403 response) | Auth API | FR-AUTH.1, DM-001 | Account with non-null locked_at returns 403 with suspension message; no token issued | S | P0 |
| 11 | FR-AUTH.1d | Implement login rate limiting (5 requests/minute/IP) | Auth API | FR-AUTH.1 | 6th login attempt within 60s from same IP returns 429 Too Many Requests; rate limiter resets after window | M | P1 |
| 12 | API-002 | Wire POST /auth/login route in AuthRouteRegistry | Routes | COMP-006, FR-AUTH.1 | Route registered; request dispatched to login handler; no auth-middleware applied | S | P0 |
| 13 | TEST-001 | Write unit tests for PasswordHasher (hash generation, verification, cost factor) | Testing | COMP-001 | Tests cover: hash roundtrip, wrong password rejection, cost factor == 12 assertion; all pass | M | P0 |
| 14 | TEST-002 | Write unit tests for JwtService (RS256 sign, verify, expiry, invalid token) | Testing | COMP-002 | Tests cover: sign/verify roundtrip, expired token rejection, malformed token rejection, kid header presence; all pass | M | P0 |
| 15 | TEST-003 | Write integration tests for registration flow covering FR-AUTH.2a through FR-AUTH.2d | Testing | FR-AUTH.2a, FR-AUTH.2b, FR-AUTH.2c, FR-AUTH.2d | All 4 acceptance criteria verified: valid registration (201), duplicate email (409), password policy (400), email validation (400) | M | P0 |
| 16 | TEST-004 | Write integration tests for login flow covering FR-AUTH.1a through FR-AUTH.1d | Testing | FR-AUTH.1a, FR-AUTH.1b, FR-AUTH.1c, FR-AUTH.1d | All 4 acceptance criteria verified: valid login (200 + tokens), invalid creds (401), locked account (403), rate limit (429) | M | P0 |

---

### Phase 2: Token Lifecycle & Profile Retrieval

**Objective**: Deliver token refresh with rotation and replay detection, and authenticated profile retrieval.

**Duration**: 1 week

**Milestone**: Clients can refresh tokens without re-authentication; replay attacks trigger full session revocation; authenticated users can retrieve their profile with no sensitive field leakage.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|------|------|-----------|--------------|---------------------|--------|----------|
| 1 | FR-AUTH.3 | Implement token refresh endpoint (POST /auth/refresh) | Auth API | COMP-003, MIG-001 | Endpoint scaffolded: reads refresh token from httpOnly cookie; validates and rotates via TokenManager | L | P0 |
| 2 | FR-AUTH.3a | Implement refresh token rotation returning new access + refresh token pair | Auth API | FR-AUTH.3, COMP-003 | Valid refresh token returns new access_token and rotated refresh_token; old refresh token marked revoked in database | M | P0 |
| 3 | FR-AUTH.3b | Implement expired refresh token rejection requiring re-authentication | Auth API | FR-AUTH.3 | Expired refresh token (> 7d) returns 401 with re-authentication required message | S | P0 |
| 4 | FR-AUTH.3c | Implement replay detection with full user token revocation | Auth API | FR-AUTH.3, DM-002 | Reuse of a previously-rotated (revoked) refresh token invalidates ALL refresh tokens for that user; returns 401 | M | P0 |
| 5 | FR-AUTH.3d | Store refresh token hashes (SHA-256) in database — never plaintext | Auth API | FR-AUTH.3, DM-002 | SHA-256 hash of refresh token stored in token_hash column; plaintext token never persisted; verified by unit test | S | P0 |
| 6 | API-003 | Wire POST /auth/refresh route in AuthRouteRegistry | Routes | COMP-006, FR-AUTH.3 | Route registered; request dispatched to refresh handler; no Bearer auth required (uses cookie) | S | P0 |
| 7 | FR-AUTH.4 | Implement profile retrieval endpoint (GET /auth/profile) | Auth API | COMP-004, DM-001 | Endpoint scaffolded: reads user context from AuthMiddlewareChain; queries user record; returns filtered profile | M | P0 |
| 8 | FR-AUTH.4a | Implement authenticated profile fetch returning user data fields | Auth API | FR-AUTH.4, COMP-004 | Valid Bearer access_token returns 200 with id, email, display_name, created_at | M | P0 |
| 9 | FR-AUTH.4b | Implement expired/invalid token rejection for profile endpoint | Auth API | FR-AUTH.4, COMP-004 | Expired or malformed Bearer token returns 401; handled by AuthMiddlewareChain before reaching handler | S | P0 |
| 10 | FR-AUTH.4c | Exclude sensitive fields (password_hash, refresh_token_hash) from profile response | Auth API | FR-AUTH.4 | Response DTO explicitly allowlists fields; password_hash and token_hash never serialized; schema validation test confirms | S | P0 |
| 11 | API-004 | Wire GET /auth/profile route (protected by AuthMiddlewareChain) | Routes | COMP-005, FR-AUTH.4 | Route registered with auth-middleware enforced; unauthenticated requests return 401 before handler executes | S | P0 |
| 12 | TEST-005 | Write integration tests for token refresh flow covering FR-AUTH.3a through FR-AUTH.3d | Testing | FR-AUTH.3a, FR-AUTH.3b, FR-AUTH.3c, FR-AUTH.3d | All 4 criteria verified: rotation (new pair), expired rejection (401), replay detection (full revocation), hash storage (SHA-256) | M | P0 |
| 13 | TEST-006 | Write integration tests for profile retrieval covering FR-AUTH.4a through FR-AUTH.4c | Testing | FR-AUTH.4a, FR-AUTH.4b, FR-AUTH.4c | All 3 criteria verified: valid fetch (200 + fields), expired token (401), no sensitive fields in response | M | P0 |
| 14 | TEST-007 | Write security tests for response schema validation across all endpoints | Testing | FR-AUTH.4c | Automated scan of all /auth/* endpoint responses asserts zero occurrences of password_hash, token_hash, or refresh_token plaintext | M | P1 |

---

### Checkpoint B: Mid-Implementation Review (Advisory)

**Trigger**: Phase 2 milestone achieved (token refresh and profile retrieval functional).

**Purpose**: Catch integration issues between Phases 1 and 2 before building password reset on top. This is an advisory checkpoint, not a blocking gate — work on Phase 3 may begin if the email service interface (OQ-7) was resolved in Phase 0.

**Review Checklist**:
- Registration → Login → Profile → Refresh lifecycle executes end-to-end in integration environment
- Replay detection correctly triggers full session revocation
- AuthMiddlewareChain correctly distinguishes public vs protected routes
- SecurityServiceContainer resolves all wired services at runtime
- No sensitive field leakage detected in TEST-007
- Feature flag (OPS-009) toggles auth routes on/off without affecting existing endpoints

**Attendees**: Backend engineer (required), Security engineer (required), QA engineer (recommended).

---

### Phase 3: Password Reset Flow

**Objective**: Deliver two-step password reset (request token, confirm reset) with session invalidation and email service integration.

**Duration**: 1 week

**Milestone**: Users can request password reset via email and set a new password; all existing sessions are invalidated on successful reset; email service adapter is operational and registered in SecurityServiceContainer.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|------|------|-----------|--------------|---------------------|--------|----------|
| 1 | COMP-007 | Implement email service adapter (interface definition + concrete adapter) | Email | OQ-1, OQ-7 | EmailService interface defined with sendResetEmail(to, token) method; adapter implements dispatch per OQ-1 decision (sync or queue); retry logic included; registered in SecurityServiceContainer | M | P1 |
| 2 | FR-AUTH.5 | Implement password reset flow (two endpoints: request + confirm) | Auth API | COMP-001, COMP-003, COMP-007 | Flow scaffolded: request endpoint generates reset token; confirm endpoint validates token and sets new password | L | P0 |
| 3 | FR-AUTH.5a | Implement reset token generation (1-hour TTL) and email dispatch | Auth API | FR-AUTH.5, COMP-007 | Given registered email, generate cryptographically random reset token with 1h expiry; invoke EmailService; return 200 (regardless of email existence, to prevent enumeration) | M | P0 |
| 4 | FR-AUTH.5b | Implement password reset confirmation with single-use token invalidation | Auth API | FR-AUTH.5, COMP-001 | Valid reset token allows setting new password; token marked used/invalidated immediately; cannot be reused | M | P0 |
| 5 | FR-AUTH.5c | Implement expired/invalid reset token rejection (400 response) | Auth API | FR-AUTH.5 | Expired (> 1h) or invalid reset token returns 400 with descriptive error message | S | P0 |
| 6 | FR-AUTH.5d | Implement session invalidation on successful password reset | Auth API | FR-AUTH.5, DM-002 | All refresh tokens for the user are revoked (revoked_at set) upon successful password change; forces re-authentication on all devices | M | P0 |
| 7 | API-005 | Wire POST /auth/reset-request route in AuthRouteRegistry | Routes | COMP-006, FR-AUTH.5 | Route registered; no auth-middleware (public endpoint); dispatches to reset request handler | S | P0 |
| 8 | API-006 | Wire POST /auth/reset-confirm route in AuthRouteRegistry | Routes | COMP-006, FR-AUTH.5 | Route registered; no Bearer auth required (uses reset token in body); dispatches to reset confirmation handler | S | P0 |
| 9 | TEST-008 | Write integration tests for password reset flow covering FR-AUTH.5a through FR-AUTH.5d | Testing | FR-AUTH.5a, FR-AUTH.5b, FR-AUTH.5c, FR-AUTH.5d | All 4 criteria verified: token generation + email dispatch, reset confirmation + token invalidation, expired token rejection, session revocation | M | P0 |

---

### Phase 4: Non-Functional Requirements & Security Hardening

**Objective**: Meet all NFR targets, mitigate identified risks, and establish operational monitoring.

**Duration**: 1.5 weeks

**Milestone**: p95 latency < 200ms verified via load test; bcrypt cost factor enforced; health check and APM monitoring operational; replay detection hardened; progressive lockout implemented.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|------|------|-----------|--------------|---------------------|--------|----------|
| 1 | NFR-AUTH.1 | Tune authentication endpoint latency to < 200ms p95 under normal load | Performance | OQ-3, FR-AUTH.1, FR-AUTH.3 | p95 latency < 200ms measured by k6 load test; implementation matches OQ-3 resolution (async hashing, adjusted target, or reduced cost factor) | L | P0 |
| 2 | NFR-AUTH.2 | Implement health check endpoint and configure uptime monitoring (99.9% SLA) | Operations | — | GET /health returns 200 with service status including auth dependency readiness; uptime monitoring tool configured; PagerDuty integration active | M | P1 |
| 3 | NFR-AUTH.3 | Verify bcrypt cost factor 12 enforcement with configurable override | Auth Module | COMP-001 | Unit test asserts cost factor == 12 at runtime; config allows increase without code change; benchmark confirms ~250ms per hash | S | P0 |
| 4 | R-1 | Implement RS256 key security controls: secrets manager storage, 90-day rotation schedule, key versioning via kid header | Security | OPS-002, OQ-8 | Private key in secrets manager; rotation runbook documented; kid header in JWT enables key coexistence during rotation; anomalous token pattern alerting defined | M | P0 |
| 5 | R-2 | Harden refresh token replay detection; evaluate client fingerprint binding | Security | FR-AUTH.3c | Replay detection confirmed via integration test; client fingerprint binding evaluated and decision documented (implement or defer with rationale) | M | P0 |
| 6 | R-3 | Ensure bcrypt cost factor is configurable; document Argon2id migration path | Security | COMP-001 | Cost factor changeable via env var without redeployment; Argon2id migration plan documented with timeline trigger (annual OWASP review) | S | P1 |
| 7 | R-4 | Implement architectural resolution for bcrypt latency vs. p95 target conflict | Performance | OQ-3, NFR-AUTH.1, NFR-AUTH.3 | Resolution from OQ-3 implemented in code; both NFR targets achievable simultaneously; load test confirms | M | P0 |
| 8 | R-5 | Implement email service graceful degradation with retry/queue pattern | Resilience | COMP-007 | Email dispatch failure does not return 500 to caller; retry with exponential backoff operational; user sees appropriate messaging on degradation | M | P1 |
| 9 | R-6 | Implement progressive account lockout policy (per OQ-4 decision) | Security | OQ-4, DM-001 | Account locks after N failures across all IPs within defined window; locked_at set in users table; unlock mechanism functional | M | P1 |
| 10 | OPS-003 | Configure PagerDuty alerting for auth service health check failures | Operations | NFR-AUTH.2 | Alerts fire within 60s of health check failure; escalation policy defined and tested | S | P1 |
| 11 | OPS-004 | Build k6 load testing suite for all auth endpoints | Performance | NFR-AUTH.1, API-001 through API-006 | k6 scripts cover login, register, refresh, profile, reset-request, reset-confirm; configurable user count and duration; p95 latency extractable | M | P1 |
| 12 | OPS-005 | Configure production APM dashboard for auth endpoint latency monitoring | Operations | NFR-AUTH.1 | Dashboard displays p95/p99 latency per endpoint; alert threshold at 200ms p95; historical trend visible | M | P1 |
| 13 | TEST-009 | Write security test for user enumeration resistance on login endpoint (FR-AUTH.1b) | Testing | FR-AUTH.1b | Timing analysis across valid-email-wrong-password vs. invalid-email confirms < 10ms variance; response bodies identical | M | P1 |
| 14 | TEST-010 | Write load test for rate limiting verification (FR-AUTH.1d) | Testing | FR-AUTH.1d, OPS-004 | k6 test sends 6 requests in 60s from same IP; 6th request returns 429; 7th request after window reset succeeds | S | P1 |
| 15 | TEST-011 | Write benchmark test for bcrypt hash timing at cost factor 12 (~250ms) | Testing | NFR-AUTH.3, COMP-001 | Benchmark over 100 iterations confirms mean hash time within ±20% of 250ms | S | P1 |

---

### Phase 5: Validation, OQ Closure, Deployment & Launch

**Objective**: Validate all 14 success criteria, close open questions with measured evidence, execute E2E lifecycle test, verify feature flag rollback, and deploy to production.

**Duration**: 1 week

**Milestone**: All SC-1 through SC-14 criteria pass; OQ-1, OQ-3, OQ-7, OQ-8 closed with implementation evidence; E2E lifecycle scenario green; feature flag rollback verified; release gate criteria satisfied; production deployment successful with monitoring active.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|------|------|-----------|--------------|---------------------|--------|----------|
| 1 | SC-1 | Validate all FR-AUTH.1 acceptance criteria pass (4/4) | Validation | TEST-004 | All 4 login criteria green in CI: valid login, invalid creds, locked account, rate limit | S | P0 |
| 2 | SC-2 | Validate all FR-AUTH.2 acceptance criteria pass (4/4) | Validation | TEST-003 | All 4 registration criteria green in CI: valid registration, duplicate email, password policy, email format | S | P0 |
| 3 | SC-3 | Validate all FR-AUTH.3 acceptance criteria pass (4/4) | Validation | TEST-005 | All 4 token refresh criteria green in CI: rotation, expired rejection, replay detection, hash storage | S | P0 |
| 4 | SC-4 | Validate all FR-AUTH.4 acceptance criteria pass (3/3) | Validation | TEST-006 | All 3 profile criteria green in CI: valid fetch, invalid token rejection, sensitive field exclusion | S | P0 |
| 5 | SC-5 | Validate all FR-AUTH.5 acceptance criteria pass (4/4) | Validation | TEST-008 | All 4 password reset criteria green in CI: token generation, reset confirmation, expired rejection, session revocation | S | P0 |
| 6 | TEST-012 | Write E2E test suite for full user lifecycle (register → login → profile → refresh → reset → re-login) | Testing | FR-AUTH.1 through FR-AUTH.5 | Automated 6-step scenario executes end-to-end; all status codes match expectations; runs in CI | L | P0 |
| 7 | SC-6 | Execute E2E user lifecycle scenario and confirm all 6 steps pass | Validation | TEST-012 | register (201) → login (200) → profile (200) → refresh (200) → reset-request (200) → re-login (200); all pass in sequence | M | P0 |
| 8 | SC-7 | Run automated security scan confirming zero sensitive field leakage | Validation | TEST-007 | 0 occurrences of password_hash or token_hash in any /auth/* API response across all test scenarios | S | P0 |
| 9 | SC-8 | Execute k6 load test and verify p95 latency < 200ms | Validation | OPS-004, NFR-AUTH.1 | k6 report shows p95 < 200ms under configured normal load scenario | M | P0 |
| 10 | SC-9 | Validate uptime monitoring and alerting are operational | Validation | NFR-AUTH.2, OPS-003 | Health check responds; simulated failure triggers PagerDuty alert within 60s | S | P0 |
| 11 | SC-10 | Verify bcrypt cost factor == 12 via unit test assertion | Validation | NFR-AUTH.3, TEST-011 | Unit test assertion for cost factor 12 passes in CI | S | P0 |
| 12 | SC-11 | Execute bcrypt benchmark and confirm ~250ms timing | Validation | NFR-AUTH.3, TEST-011 | Benchmark test mean within ±20% of 250ms; passes in CI | S | P0 |
| 13 | SC-12 | Run full CI regression suite — verify zero breaking changes to existing endpoints | Validation | SC-1 through SC-5 | All pre-existing integration tests pass alongside new auth test suite; no regressions | M | P0 |
| 14 | SC-13 | Verify feature flag rollback (AUTH_SERVICE_ENABLED=false reverts behavior) | Validation | OPS-009 | Disabling feature flag causes auth endpoints to return 503 or route to previous behavior; manually verified in staging | M | P0 |
| 15 | SC-14 | Verify database migration 003 rollback drops tables cleanly | Validation | MIG-002 | Down-migration executes; tables removed; no orphaned constraints or sequences; idempotent re-run confirmed | S | P0 |
| 16 | OQ-1-VAL | Validate email dispatch mode decision with implementation evidence | OQ Closure | COMP-007, TEST-008 | Email dispatch mode (sync or queue) is implemented and tested; round-trip evidence from integration test confirms behavior matches OQ-1 decision | S | P0 |
| 17 | OQ-3-VAL | Validate latency resolution with measured load test evidence | OQ Closure | NFR-AUTH.1, OPS-004, SC-8 | k6 load test results demonstrate that OQ-3 decision achieves < 200ms p95 or documents approved exception with stakeholder sign-off | S | P0 |
| 18 | OQ-7-VAL | Validate email service interface implementation against contract | OQ Closure | COMP-007, OQ-1-VAL | Email service implementation matches OQ-7 interface specification; method signatures, error types, and retry semantics verified | S | P0 |
| 19 | OQ-8-VAL | Validate RSA key rotation procedure with operational evidence | OQ Closure | R-1, OPS-002 | Key rotation procedure executed in staging; kid-based versioning confirmed; zero-downtime rotation demonstrated or documented as tested | S | P0 |
| 20 | OPS-006 | Configure feature flag for gradual production rollout (canary percentage, monitoring thresholds) | Deployment | OPS-009 | Feature flag rollout percentage configurable; canary → full rollout sequence defined; rollback < 30s | S | P0 |
| 21 | OPS-007 | Deploy to staging environment and execute smoke tests | Deployment | SC-6, SC-12 | All auth endpoints functional in staging; E2E lifecycle passes; no regressions in existing endpoints | M | P0 |
| 22 | OPS-008 | Deploy to production with feature flag enabled; confirm monitoring active | Deployment | OPS-007, SC-13 | Production deploy successful; feature flag enabled for canary percentage; APM and health check monitoring confirm normal operation | M | P0 |

---

## 4. Risk Assessment & Mitigation Strategies

| Risk | Probability | Severity | Mitigation Strategy | Addressed By | Architect Recommendation |
|------|-------------|----------|---------------------|--------------|--------------------------|
| **R-1: JWT private key compromise** | Low | High | RS256 asymmetric keys (private never leaves secrets manager); 90-day rotation with kid-based versioning; anomalous token pattern monitoring | OPS-002, OQ-8, R-1 task, OQ-8-VAL | Release should be blocked if key versioning is not operationally defined |
| **R-2: Refresh token replay attack** | Medium | High | Token rotation on every refresh; replay detection triggers full user revocation (FR-AUTH.3c); client fingerprint binding evaluated (R-2 task); hashed refresh-token storage | FR-AUTH.3c, R-2 task, CONT-002 | Treat replay tests as mandatory P0 gating |
| **R-3: bcrypt cost factor obsolescence** | Low | Medium | Cost factor configurable via environment; annual OWASP benchmark review; Argon2id migration path documented | COMP-001, R-3 task | Annual review mechanism must be documented, not just the migration path |
| **R-4: Latency conflict (bcrypt vs. p95)** | Medium | Medium | **Must resolve in Phase 0** (OQ-3). Options: (a) async hashing offloaded to worker, (b) adjust p95 target to 300ms for login only, (c) reduce cost factor to 10. Decision drives NFR-AUTH.1 implementation. Evidence-based validation in Phase 5 (OQ-3-VAL). | OQ-3, R-4 task, NFR-AUTH.1, OQ-3-VAL | Do not silently "best effort" this requirement; force a stakeholder decision |
| **R-5: Email service unavailability** | Medium | Low | Email adapter with retry + exponential backoff; queue-based dispatch (if OQ-1 resolves to async); graceful user messaging on failure | COMP-007, R-5 task, OQ-1-VAL | Prefer async dispatch if infrastructure exists; otherwise document synchronous latency/availability tradeoff |
| **R-6: Distributed brute-force (no lockout)** | Medium | Medium | Progressive account lockout policy (OQ-4); account-level failure tracking across IPs; automated unlock after cooling period | OQ-4, R-6 task | At minimum, document the gap and attach follow-up ownership |

**Residual risk after mitigation**: R-2 (replay) remains the highest residual risk. Token rotation with replay detection reduces it significantly, but a stolen refresh token used before the legitimate client refreshes creates a race condition. Client fingerprint binding (evaluated in R-2 task) would further reduce this surface.

### Secondary Delivery Risks

1. Migration reversibility not actually tested — mitigated by SC-14 and MIG-002
2. Feature flag rollback not exercised before release — mitigated by early flag (OPS-009) enabling testing across all phases, and SC-13
3. Profile endpoint accidentally leaking internal fields — mitigated by TEST-007 schema validation
4. Secrets manager integration behaving differently across environments — mitigated by OQ-8-VAL staging validation
5. Session concurrency policy left undefined — mitigated by OQ-2 decision in Phase 0

---

## 5. Resource Requirements & Dependencies

### Team Resources

| Role | Allocation | Phase Coverage |
|------|-----------|----------------|
| Backend Engineer | 1 FTE | Phases 0–3 (core implementation) |
| Security Engineer | 0.5 FTE | Phase 0 (contract review, architecture), Phase 4 (hardening) |
| QA/Test Engineer | 0.5 FTE | Phases 1–5 (test suite, load testing, E2E) |
| DevOps Engineer | 0.25 FTE | Phases 0, 4–5 (infrastructure, monitoring, deployment) |

### External Dependencies

| Dependency | Required By | Risk if Delayed |
|------------|-------------|-----------------|
| **Email service** (interface contract) | Phase 3 (COMP-007, FR-AUTH.5) | Password reset flow blocked; can proceed with stub adapter for testing |
| **Secrets manager** access | Phase 0 (OPS-002) | JWT signing blocked; local dev fallback possible but production blocked |
| **Database migration slot** | Phase 0 (MIG-001) | All data-dependent work blocked; coordinate with DB team for migration 003 scheduling |
| **RSA key pair** provisioning | Phase 0 (OPS-001) | JwtService blocked; can use local dev keys temporarily |
| **k6 load testing infrastructure** | Phase 4 (OPS-004) | NFR-AUTH.1 validation delayed; not on critical path |
| **PagerDuty integration** | Phase 4 (OPS-003) | Monitoring setup delayed; not on critical path |

### Library Dependencies

| Library | Version Strategy | Notes |
|---------|-----------------|-------|
| `jsonwebtoken` | Pin to latest stable | RS256 support required; verify no known CVEs |
| `bcrypt` | Pin to latest stable | Requires native addon compilation; verify platform compatibility in CI |

---

## 6. Success Criteria & Validation Approach

### Validation Strategy

Validation is layered across four tiers, guided by the test strategy matrix (TEST-ARCH-001) defined in Phase 0:

1. **Unit tests** (Phases 0–1): Verify individual components — PasswordHasher, JwtService, TokenManager, auth-middleware — in isolation. ~15 test cases. Shared fixtures from TEST-ARCH-002.
2. **Integration tests** (Phases 1–3): Verify each endpoint against its full acceptance criteria with a real database. ~20 test cases covering FR-AUTH.1 through FR-AUTH.5.
3. **E2E + Security + Load tests** (Phases 4–5): Verify the complete user lifecycle, sensitive field exclusion, enumeration resistance, rate limiting behavior, and p95 latency. ~10 test cases.
4. **Evidence-based OQ closure** (Phase 5): Validate Phase 0 architectural decisions against measured implementation evidence. 4 validation tasks (OQ-1-VAL, OQ-3-VAL, OQ-7-VAL, OQ-8-VAL).

### Success Criteria Traceability

| SC ID | Validates | Method | Phase Verified |
|-------|-----------|--------|---------------|
| SC-1 | FR-AUTH.1 (Login) | TEST-004 integration suite | Phase 5 |
| SC-2 | FR-AUTH.2 (Registration) | TEST-003 integration suite | Phase 5 |
| SC-3 | FR-AUTH.3 (Token Refresh) | TEST-005 integration suite | Phase 5 |
| SC-4 | FR-AUTH.4 (Profile) | TEST-006 integration suite | Phase 5 |
| SC-5 | FR-AUTH.5 (Password Reset) | TEST-008 integration suite | Phase 5 |
| SC-6 | Full user lifecycle | TEST-012 E2E suite | Phase 5 |
| SC-7 | No sensitive field leakage | TEST-007 schema validation | Phase 5 |
| SC-8 | p95 < 200ms | OPS-004 k6 load test | Phase 5 |
| SC-9 | 99.9% uptime | OPS-003 PagerDuty + health check | Phase 5 |
| SC-10 | bcrypt cost factor == 12 | TEST-011 unit assertion | Phase 5 |
| SC-11 | bcrypt ~250ms timing | TEST-011 benchmark | Phase 5 |
| SC-12 | Zero regressions | CI regression suite | Phase 5 |
| SC-13 | Feature flag rollback | OPS-009 + OPS-006 verification | Phase 5 |
| SC-14 | Migration rollback | MIG-002 rollback test | Phase 5 |

### Release Gate Criteria

Release only when **all** of the following are true:

1. **SC-1 through SC-14** are green in CI, or have formally approved exceptions with documented rationale.
2. **OQ-1, OQ-3, OQ-7, and OQ-8** are closed with implementation evidence (OQ-*-VAL tasks complete). Decisions validated by measured results, not solely stakeholder sign-off.
3. **R-1, R-2, and R-4** security and architecture reviews are complete with documented findings.
4. **Feature flag rollback** (AUTH_SERVICE_ENABLED=false) is proven in staging — disabling the flag restores pre-auth behavior without deployment rollback.
5. **Migration rollback** (MIG-002) is proven — down migration drops auth tables cleanly and repeatably in CI.
6. **Security-sensitive response-schema leakage tests** (TEST-007) are green across all /auth/* endpoints.
7. **Regression suite** (SC-12) confirms zero breaking changes to existing endpoints with auth both enabled and disabled.

This is a binary go/no-go gate. Any failing criterion blocks release until resolved or formally exempted.

---

## 7. Timeline Estimates

| Phase | Duration | Cumulative | Key Dependency |
|-------|----------|------------|----------------|
| **Phase 0**: Foundation, Architecture & Contracts | 1.5 weeks | Week 1.5 | OQ-3 resolution gates all performance work; security contracts reviewed before implementation |
| **Phase 1**: Registration & Login | 1.5 weeks | Week 3 | Phase 0 services, migration, and contracts |
| **Phase 2**: Token Lifecycle & Profile | 1 week | Week 4 | Phase 1 login (tokens required for profile auth) |
| **Checkpoint B**: Mid-Implementation Review | — | Week 4 | Advisory; does not add calendar time |
| **Phase 3**: Password Reset | 1 week | Week 5 | OQ-7 email interface; Phase 0 services |
| **Phase 4**: NFR & Hardening | 1.5 weeks | Week 6.5 | All functional endpoints complete |
| **Phase 5**: Validation, OQ Closure & Deploy | 1 week | **Week 7.5** | All phases complete; OQ evidence collected |

**Total estimated duration**: ~7.5 weeks with 1 backend FTE + fractional security/QA/DevOps support.

**Parallelization opportunity**: Phase 3 (password reset) can begin concurrently with Phase 2 if the email service interface (OQ-7) is resolved in Phase 0. This could compress the timeline to ~6.5 weeks.

**Critical path**: OQ-3 → Phase 0 infra + contracts → Phase 1 login → Phase 2 token refresh → Phase 5 E2E validation + OQ closure → Release gate → Production deploy.

**Merge impact on timeline**: The 9 additional tasks (2 contracts, 2 test architecture, 1 feature flag, 4 OQ validations) are all S-effort. Phase 0 grows by < 1 day; Phase 5 grows by < 0.5 days. Total timeline impact is negligible (< 0.5 weeks), as most additions are S-effort planning or validation artifacts.
