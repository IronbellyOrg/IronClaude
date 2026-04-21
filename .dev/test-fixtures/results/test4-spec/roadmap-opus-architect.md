---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
generated: "2026-04-15"
generator: "superclaude-roadmap/opus-4.6"
total_phases: 6
total_task_rows: 92
extraction_ids_preserved: 55
derived_entity_ids: 37
---

# Project Roadmap: User Authentication Service

## 1. Executive Summary

This roadmap covers the implementation of a JWT-based authentication service for the platform, encompassing user registration, login, token lifecycle management, profile retrieval, and password reset. The service introduces two new database tables, five API endpoints, and a middleware integration — all scoped to a well-bounded auth module with no OAuth, MFA, or RBAC in v1.0.

**Complexity**: MEDIUM (0.6) — the architectural footprint is modest, but security sensitivity drives the bulk of the effort. Cryptographic operations (RS256, bcrypt), stateful token rotation with replay detection, and a latency constraint that conflicts with the hashing budget (NFR-AUTH.1 vs NFR-AUTH.3) require careful resolution before implementation begins.

**Critical Path**: Open Question resolution (Phase 0) → Database schema + core services (Phase 0) → Registration + Login (Phase 1) → Token refresh + Profile (Phase 2) → Password reset (Phase 3) → NFR hardening (Phase 4) → Validation + Deploy (Phase 5).

**Key Risks**:
- The bcrypt latency (~250ms at cost 12) exceeds the 200ms p95 target — architectural resolution required before Phase 1
- Email service interface is undefined, blocking FR-AUTH.5 completion
- No account lockout policy leaves distributed brute-force attack surface open

---

## 2. Integration Points

### 2.1 Express Middleware Chain

- **Named Artifact**: Middleware pipeline in `src/middleware/index.ts`
- **Wired Components**: `auth-middleware.ts` (Bearer token extraction, JWT verification, user context attachment)
- **Owning Phase**: Phase 0 creates `auth-middleware.ts` (COMP-004); Phase 0 wires it into the pipeline (COMP-005)
- **Cross-Reference**: Phase 1 routes bypass middleware (login/register are public); Phase 2 routes consume middleware (profile is protected); Phase 3 reset-request is public, reset-confirm uses reset token (not Bearer)

### 2.2 Route Registry

- **Named Artifact**: Route registry in `src/routes/index.ts`, `/auth/*` route group
- **Wired Components**: POST `/auth/register` (API-001), POST `/auth/login` (API-002), POST `/auth/refresh` (API-003), GET `/auth/profile` (API-004), POST `/auth/reset-request` (API-005), POST `/auth/reset-confirm` (API-006)
- **Owning Phase**: Phase 0 creates the `/auth/*` group placeholder (COMP-006); Phases 1–3 register individual routes
- **Cross-Reference**: All phases add routes; Phase 4 load tests exercise all registered routes; Phase 5 E2E test traverses the full route set

### 2.3 TokenManager Service Wiring

- **Named Artifact**: `TokenManager` service (COMP-003) — orchestrates access and refresh token lifecycle
- **Wired Components**: `JwtService` (COMP-002) for RS256 signing/verification; `PasswordHasher` (COMP-001) consumed by login/register handlers; `RefreshToken` repository backed by DM-002
- **Owning Phase**: Phase 0 creates all three services; Phase 1–3 consume them from endpoint handlers
- **Cross-Reference**: Phase 2 exercises token rotation and replay detection through TokenManager; Phase 3 triggers full revocation through TokenManager on password reset

### 2.4 Email Service Adapter

- **Named Artifact**: `EmailService` interface + adapter (COMP-007) — strategy pattern for email dispatch
- **Wired Components**: Concrete adapter wired per OQ-1 decision (synchronous HTTP or async message queue)
- **Owning Phase**: Phase 3 defines the interface and implements the adapter
- **Cross-Reference**: Phase 4 implements degradation handling (R-5); Phase 5 E2E test validates email dispatch invocation

---

## 3. Phased Implementation Plan

### Phase 0: Foundation & Architecture Resolution

**Objective**: Resolve architectural ambiguities, provision infrastructure, and build core service components before any endpoint work begins.

**Duration**: 1.5 weeks

**Milestone**: All open questions documented with decisions; database migration runs cleanly; PasswordHasher, JwtService, and TokenManager pass unit tests; auth-middleware wired into pipeline.

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
| 9 | DM-001 | Design users database table schema | Database | OQ-5 | Schema: id (UUID PK), email (unique index), display_name, password_hash, created_at, locked_at (nullable); reviewed and approved | M | P0 |
| 10 | DM-002 | Design refresh_tokens database table schema | Database | OQ-2 | Schema: id (UUID PK), user_id (FK → users, indexed), token_hash (SHA-256), expires_at, revoked_at (nullable), created_at; reviewed and approved | M | P0 |
| 11 | MIG-001 | Create database migration 003 — up (create users and refresh_tokens tables) | Database | DM-001, DM-002 | Migration executes cleanly; tables created with correct columns, types, indexes, and foreign keys | M | P0 |
| 12 | MIG-002 | Create database migration 003 — down (rollback: drop tables) | Database | MIG-001 | Down-migration drops both tables cleanly with no orphaned objects; idempotent execution | S | P0 |
| 13 | OPS-001 | Generate RSA key pair for JWT RS256 signing | Infrastructure | — | 2048+ bit RSA key pair generated; private key not committed to repository | S | P0 |
| 14 | OPS-002 | Integrate secrets manager for RSA private key storage and retrieval | Infrastructure | OPS-001 | Private key stored in secrets manager; application retrieves key at startup; local dev fallback documented | M | P0 |
| 15 | COMP-001 | Implement PasswordHasher service with configurable bcrypt cost factor | Auth Module | — | Exposes hash(password) and verify(password, hash); cost factor configurable via environment variable (default 12); TypeScript | M | P0 |
| 16 | COMP-002 | Implement JwtService with RS256 signing and verification | Auth Module | OPS-002 | Signs tokens with RS256 private key; verifies with public key; supports configurable TTL; includes kid header for key rotation | M | P0 |
| 17 | COMP-003 | Implement TokenManager (access + refresh token orchestration) | Auth Module | COMP-002 | Generates access tokens (15min TTL) and refresh tokens (7d TTL); delegates signing to JwtService; stores refresh token hash via repository | M | P0 |
| 18 | COMP-004 | Implement auth-middleware.ts (Bearer token extraction and JWT verification) | Middleware | COMP-002 | Extracts Bearer token from Authorization header; verifies JWT via JwtService; attaches decoded user context to request object; returns 401 on failure | M | P0 |
| 19 | COMP-005 | Wire auth-middleware into Express middleware pipeline | Middleware | COMP-004 | Middleware registered in pipeline; protects routes marked as authenticated; passes through public routes (/auth/login, /auth/register) | S | P0 |
| 20 | COMP-006 | Register /auth/* route group in src/routes/index.ts | Routes | — | Route group created and exported; ready for individual endpoint registration in subsequent phases | S | P0 |

---

### Phase 1: Core Authentication — Registration & Login

**Objective**: Deliver working registration and login endpoints with full acceptance criteria coverage.

**Duration**: 1.5 weeks

**Milestone**: Users can register, login, and receive JWT tokens. All FR-AUTH.1 and FR-AUTH.2 acceptance criteria pass in integration tests.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|------|------|-----------|--------------|---------------------|--------|----------|
| 21 | FR-AUTH.2 | Implement user registration endpoint (POST /auth/register) | Auth API | COMP-001, COMP-003, MIG-001 | Endpoint scaffolded: accepts email, password, display_name; delegates to PasswordHasher and user repository | L | P0 |
| 22 | FR-AUTH.2a | Implement valid registration flow with user record creation and 201 response | Auth API | FR-AUTH.2 | Given valid data, user record created with hashed password; returns 201 with user profile (id, email, display_name, created_at) | M | P0 |
| 23 | FR-AUTH.2b | Implement duplicate email conflict detection (409 response) | Auth API | FR-AUTH.2, DM-001 | Given already-registered email, returns 409 Conflict; no partial user record created | S | P0 |
| 24 | FR-AUTH.2c | Implement password policy enforcement (min 8 chars, uppercase, lowercase, digit) | Auth API | FR-AUTH.2 | Passwords violating policy return 400 with specific violation message; boundary cases (7 chars, missing class) rejected | S | P0 |
| 25 | FR-AUTH.2d | Implement email format validation before registration attempt | Auth API | FR-AUTH.2 | Malformed emails rejected with 400 before any database interaction; RFC 5322 basic validation | S | P0 |
| 26 | API-001 | Wire POST /auth/register route in route registry | Routes | COMP-006, FR-AUTH.2 | Route registered in /auth/* group; request dispatched to registration handler; no auth-middleware applied | S | P0 |
| 27 | FR-AUTH.1 | Implement user login endpoint (POST /auth/login) | Auth API | COMP-001, COMP-003, FR-AUTH.2 | Endpoint scaffolded: accepts email + password; verifies credentials via PasswordHasher; returns tokens via TokenManager | L | P0 |
| 28 | FR-AUTH.1a | Implement successful login returning access_token (15min TTL) and refresh_token (7d TTL) | Auth API | FR-AUTH.1, COMP-003 | Valid credentials return 200 with access_token and refresh_token; TTLs match specification; refresh_token set as httpOnly cookie | M | P0 |
| 29 | FR-AUTH.1b | Implement generic invalid credentials response (enumeration resistance) | Auth API | FR-AUTH.1 | Invalid email or password returns 401 with identical error message; response timing does not leak whether email exists | S | P0 |
| 30 | FR-AUTH.1c | Implement locked account rejection (403 response) | Auth API | FR-AUTH.1, DM-001 | Account with non-null locked_at returns 403 with suspension message; no token issued | S | P0 |
| 31 | FR-AUTH.1d | Implement login rate limiting (5 requests/minute/IP) | Auth API | FR-AUTH.1 | 6th login attempt within 60s from same IP returns 429 Too Many Requests; rate limiter resets after window | M | P1 |
| 32 | API-002 | Wire POST /auth/login route in route registry | Routes | COMP-006, FR-AUTH.1 | Route registered; request dispatched to login handler; no auth-middleware applied | S | P0 |
| 33 | TEST-001 | Write unit tests for PasswordHasher (hash generation, verification, cost factor) | Testing | COMP-001 | Tests cover: hash roundtrip, wrong password rejection, cost factor == 12 assertion; all pass | M | P0 |
| 34 | TEST-002 | Write unit tests for JwtService (RS256 sign, verify, expiry, invalid token) | Testing | COMP-002 | Tests cover: sign/verify roundtrip, expired token rejection, malformed token rejection, kid header presence; all pass | M | P0 |
| 35 | TEST-003 | Write integration tests for registration flow covering FR-AUTH.2a through FR-AUTH.2d | Testing | FR-AUTH.2a, FR-AUTH.2b, FR-AUTH.2c, FR-AUTH.2d | All 4 acceptance criteria verified: valid registration (201), duplicate email (409), password policy (400), email validation (400) | M | P0 |
| 36 | TEST-004 | Write integration tests for login flow covering FR-AUTH.1a through FR-AUTH.1d | Testing | FR-AUTH.1a, FR-AUTH.1b, FR-AUTH.1c, FR-AUTH.1d | All 4 acceptance criteria verified: valid login (200 + tokens), invalid creds (401), locked account (403), rate limit (429) | M | P0 |

---

### Phase 2: Token Lifecycle & Profile Retrieval

**Objective**: Deliver token refresh with rotation and replay detection, and authenticated profile retrieval.

**Duration**: 1 week

**Milestone**: Clients can refresh tokens without re-authentication; replay attacks trigger full session revocation; authenticated users can retrieve their profile with no sensitive field leakage.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|------|------|-----------|--------------|---------------------|--------|----------|
| 37 | FR-AUTH.3 | Implement token refresh endpoint (POST /auth/refresh) | Auth API | COMP-003, MIG-001 | Endpoint scaffolded: reads refresh token from httpOnly cookie; validates and rotates via TokenManager | L | P0 |
| 38 | FR-AUTH.3a | Implement refresh token rotation returning new access + refresh token pair | Auth API | FR-AUTH.3, COMP-003 | Valid refresh token returns new access_token and rotated refresh_token; old refresh token marked revoked in database | M | P0 |
| 39 | FR-AUTH.3b | Implement expired refresh token rejection requiring re-authentication | Auth API | FR-AUTH.3 | Expired refresh token (> 7d) returns 401 with re-authentication required message | S | P0 |
| 40 | FR-AUTH.3c | Implement replay detection with full user token revocation | Auth API | FR-AUTH.3, DM-002 | Reuse of a previously-rotated (revoked) refresh token invalidates ALL refresh tokens for that user; returns 401 | M | P0 |
| 41 | FR-AUTH.3d | Store refresh token hashes (SHA-256) in database — never plaintext | Auth API | FR-AUTH.3, DM-002 | SHA-256 hash of refresh token stored in token_hash column; plaintext token never persisted; verified by unit test | S | P0 |
| 42 | API-003 | Wire POST /auth/refresh route in route registry | Routes | COMP-006, FR-AUTH.3 | Route registered; request dispatched to refresh handler; no Bearer auth required (uses cookie) | S | P0 |
| 43 | FR-AUTH.4 | Implement profile retrieval endpoint (GET /auth/profile) | Auth API | COMP-004, DM-001 | Endpoint scaffolded: reads user context from auth-middleware; queries user record; returns filtered profile | M | P0 |
| 44 | FR-AUTH.4a | Implement authenticated profile fetch returning user data fields | Auth API | FR-AUTH.4, COMP-004 | Valid Bearer access_token returns 200 with id, email, display_name, created_at | M | P0 |
| 45 | FR-AUTH.4b | Implement expired/invalid token rejection for profile endpoint | Auth API | FR-AUTH.4, COMP-004 | Expired or malformed Bearer token returns 401; handled by auth-middleware before reaching handler | S | P0 |
| 46 | FR-AUTH.4c | Exclude sensitive fields (password_hash, refresh_token_hash) from profile response | Auth API | FR-AUTH.4 | Response DTO explicitly allowlists fields; password_hash and token_hash never serialized; schema validation test confirms | S | P0 |
| 47 | API-004 | Wire GET /auth/profile route (protected by auth-middleware) | Routes | COMP-005, FR-AUTH.4 | Route registered with auth-middleware enforced; unauthenticated requests return 401 before handler executes | S | P0 |
| 48 | TEST-005 | Write integration tests for token refresh flow covering FR-AUTH.3a through FR-AUTH.3d | Testing | FR-AUTH.3a, FR-AUTH.3b, FR-AUTH.3c, FR-AUTH.3d | All 4 criteria verified: rotation (new pair), expired rejection (401), replay detection (full revocation), hash storage (SHA-256) | M | P0 |
| 49 | TEST-006 | Write integration tests for profile retrieval covering FR-AUTH.4a through FR-AUTH.4c | Testing | FR-AUTH.4a, FR-AUTH.4b, FR-AUTH.4c | All 3 criteria verified: valid fetch (200 + fields), expired token (401), no sensitive fields in response | M | P0 |
| 50 | TEST-007 | Write security tests for response schema validation across all endpoints | Testing | FR-AUTH.4c | Automated scan of all /auth/* endpoint responses asserts zero occurrences of password_hash, token_hash, or refresh_token plaintext | M | P1 |

---

### Phase 3: Password Reset Flow

**Objective**: Deliver two-step password reset (request token, confirm reset) with session invalidation and email service integration.

**Duration**: 1 week

**Milestone**: Users can request password reset via email and set a new password; all existing sessions are invalidated on successful reset; email service adapter is operational.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|------|------|-----------|--------------|---------------------|--------|----------|
| 51 | COMP-007 | Implement email service adapter (interface definition + concrete adapter) | Email | OQ-1, OQ-7 | EmailService interface defined with sendResetEmail(to, token) method; adapter implements dispatch per OQ-1 decision (sync or queue); retry logic included | M | P1 |
| 52 | FR-AUTH.5 | Implement password reset flow (two endpoints: request + confirm) | Auth API | COMP-001, COMP-003, COMP-007 | Flow scaffolded: request endpoint generates reset token; confirm endpoint validates token and sets new password | L | P0 |
| 53 | FR-AUTH.5a | Implement reset token generation (1-hour TTL) and email dispatch | Auth API | FR-AUTH.5, COMP-007 | Given registered email, generate cryptographically random reset token with 1h expiry; invoke EmailService; return 200 (regardless of email existence, to prevent enumeration) | M | P0 |
| 54 | FR-AUTH.5b | Implement password reset confirmation with single-use token invalidation | Auth API | FR-AUTH.5, COMP-001 | Valid reset token allows setting new password; token marked used/invalidated immediately; cannot be reused | M | P0 |
| 55 | FR-AUTH.5c | Implement expired/invalid reset token rejection (400 response) | Auth API | FR-AUTH.5 | Expired (> 1h) or invalid reset token returns 400 with descriptive error message | S | P0 |
| 56 | FR-AUTH.5d | Implement session invalidation on successful password reset | Auth API | FR-AUTH.5, DM-002 | All refresh tokens for the user are revoked (revoked_at set) upon successful password change; forces re-authentication on all devices | M | P0 |
| 57 | API-005 | Wire POST /auth/reset-request route in route registry | Routes | COMP-006, FR-AUTH.5 | Route registered; no auth-middleware (public endpoint); dispatches to reset request handler | S | P0 |
| 58 | API-006 | Wire POST /auth/reset-confirm route in route registry | Routes | COMP-006, FR-AUTH.5 | Route registered; no Bearer auth required (uses reset token in body); dispatches to reset confirmation handler | S | P0 |
| 59 | TEST-008 | Write integration tests for password reset flow covering FR-AUTH.5a through FR-AUTH.5d | Testing | FR-AUTH.5a, FR-AUTH.5b, FR-AUTH.5c, FR-AUTH.5d | All 4 criteria verified: token generation + email dispatch, reset confirmation + token invalidation, expired token rejection, session revocation | M | P0 |

---

### Phase 4: Non-Functional Requirements & Security Hardening

**Objective**: Meet all NFR targets, mitigate identified risks, and establish operational monitoring.

**Duration**: 1.5 weeks

**Milestone**: p95 latency < 200ms verified via load test; bcrypt cost factor enforced; health check and APM monitoring operational; replay detection hardened; progressive lockout implemented.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|------|------|-----------|--------------|---------------------|--------|----------|
| 60 | NFR-AUTH.1 | Tune authentication endpoint latency to < 200ms p95 under normal load | Performance | OQ-3, FR-AUTH.1, FR-AUTH.3 | p95 latency < 200ms measured by k6 load test; implementation matches OQ-3 resolution (async hashing, adjusted target, or reduced cost factor) | L | P0 |
| 61 | NFR-AUTH.2 | Implement health check endpoint and configure uptime monitoring (99.9% SLA) | Operations | — | GET /health returns 200 with service status; uptime monitoring tool configured; PagerDuty integration active | M | P1 |
| 62 | NFR-AUTH.3 | Verify bcrypt cost factor 12 enforcement with configurable override | Auth Module | COMP-001 | Unit test asserts cost factor == 12 at runtime; config allows increase without code change; benchmark confirms ~250ms per hash | S | P0 |
| 63 | R-1 | Implement RS256 key security controls: secrets manager storage, 90-day rotation schedule, key versioning via kid header | Security | OPS-002, OQ-8 | Private key in secrets manager; rotation runbook documented; kid header in JWT enables key coexistence during rotation; anomalous token pattern alerting defined | M | P0 |
| 64 | R-2 | Harden refresh token replay detection; evaluate client fingerprint binding | Security | FR-AUTH.3c | Replay detection confirmed via integration test; client fingerprint binding evaluated and decision documented (implement or defer with rationale) | M | P0 |
| 65 | R-3 | Ensure bcrypt cost factor is configurable; document Argon2id migration path | Security | COMP-001 | Cost factor changeable via env var without redeployment; Argon2id migration plan documented with timeline trigger (annual OWASP review) | S | P1 |
| 66 | R-4 | Implement architectural resolution for bcrypt latency vs. p95 target conflict | Performance | OQ-3, NFR-AUTH.1, NFR-AUTH.3 | Resolution from OQ-3 implemented in code; both NFR targets achievable simultaneously; load test confirms | M | P0 |
| 67 | R-5 | Implement email service graceful degradation with retry/queue pattern | Resilience | COMP-007 | Email dispatch failure does not return 500 to caller; retry with exponential backoff operational; user sees appropriate messaging on degradation | M | P1 |
| 68 | R-6 | Implement progressive account lockout policy (per OQ-4 decision) | Security | OQ-4, DM-001 | Account locks after N failures across all IPs within defined window; locked_at set in users table; unlock mechanism functional | M | P1 |
| 69 | OPS-003 | Configure PagerDuty alerting for auth service health check failures | Operations | NFR-AUTH.2 | Alerts fire within 60s of health check failure; escalation policy defined and tested | S | P1 |
| 70 | OPS-004 | Build k6 load testing suite for all auth endpoints | Performance | NFR-AUTH.1, API-001 through API-006 | k6 scripts cover login, register, refresh, profile, reset-request, reset-confirm; configurable user count and duration; p95 latency extractable | M | P1 |
| 71 | OPS-005 | Configure production APM dashboard for auth endpoint latency monitoring | Operations | NFR-AUTH.1 | Dashboard displays p95/p99 latency per endpoint; alert threshold at 200ms p95; historical trend visible | M | P1 |
| 72 | TEST-009 | Write security test for user enumeration resistance on login endpoint (FR-AUTH.1b) | Testing | FR-AUTH.1b | Timing analysis across valid-email-wrong-password vs. invalid-email confirms < 10ms variance; response bodies identical | M | P1 |
| 73 | TEST-010 | Write load test for rate limiting verification (FR-AUTH.1d) | Testing | FR-AUTH.1d, OPS-004 | k6 test sends 6 requests in 60s from same IP; 6th request returns 429; 7th request after window reset succeeds | S | P1 |
| 74 | TEST-011 | Write benchmark test for bcrypt hash timing at cost factor 12 (~250ms) | Testing | NFR-AUTH.3, COMP-001 | Benchmark over 100 iterations confirms mean hash time within ±20% of 250ms | S | P1 |

---

### Phase 5: Validation, Deployment & Launch

**Objective**: Validate all 14 success criteria, execute E2E lifecycle test, verify feature flag rollback, and deploy to production.

**Duration**: 1 week

**Milestone**: All SC-1 through SC-14 criteria pass; E2E lifecycle scenario green; feature flag rollback verified; production deployment successful with monitoring active.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|------|------|-----------|--------------|---------------------|--------|----------|
| 75 | SC-1 | Validate all FR-AUTH.1 acceptance criteria pass (4/4) | Validation | TEST-004 | All 4 login criteria green in CI: valid login, invalid creds, locked account, rate limit | S | P0 |
| 76 | SC-2 | Validate all FR-AUTH.2 acceptance criteria pass (4/4) | Validation | TEST-003 | All 4 registration criteria green in CI: valid registration, duplicate email, password policy, email format | S | P0 |
| 77 | SC-3 | Validate all FR-AUTH.3 acceptance criteria pass (4/4) | Validation | TEST-005 | All 4 token refresh criteria green in CI: rotation, expired rejection, replay detection, hash storage | S | P0 |
| 78 | SC-4 | Validate all FR-AUTH.4 acceptance criteria pass (3/3) | Validation | TEST-006 | All 3 profile criteria green in CI: valid fetch, invalid token rejection, sensitive field exclusion | S | P0 |
| 79 | SC-5 | Validate all FR-AUTH.5 acceptance criteria pass (4/4) | Validation | TEST-008 | All 4 password reset criteria green in CI: token generation, reset confirmation, expired rejection, session revocation | S | P0 |
| 80 | TEST-012 | Write E2E test suite for full user lifecycle (register → login → profile → refresh → reset → re-login) | Testing | FR-AUTH.1 through FR-AUTH.5 | Automated 6-step scenario executes end-to-end; all status codes match expectations; runs in CI | L | P0 |
| 81 | SC-6 | Execute E2E user lifecycle scenario and confirm all 6 steps pass | Validation | TEST-012 | register (201) → login (200) → profile (200) → refresh (200) → reset-request (200) → re-login (200); all pass in sequence | M | P0 |
| 82 | SC-7 | Run automated security scan confirming zero sensitive field leakage | Validation | TEST-007 | 0 occurrences of password_hash or token_hash in any /auth/* API response across all test scenarios | S | P0 |
| 83 | SC-8 | Execute k6 load test and verify p95 latency < 200ms | Validation | OPS-004, NFR-AUTH.1 | k6 report shows p95 < 200ms under configured normal load scenario | M | P0 |
| 84 | SC-9 | Validate uptime monitoring and alerting are operational | Validation | NFR-AUTH.2, OPS-003 | Health check responds; simulated failure triggers PagerDuty alert within 60s | S | P0 |
| 85 | SC-10 | Verify bcrypt cost factor == 12 via unit test assertion | Validation | NFR-AUTH.3, TEST-011 | Unit test assertion for cost factor 12 passes in CI | S | P0 |
| 86 | SC-11 | Execute bcrypt benchmark and confirm ~250ms timing | Validation | NFR-AUTH.3, TEST-011 | Benchmark test mean within ±20% of 250ms; passes in CI | S | P0 |
| 87 | SC-12 | Run full CI regression suite — verify zero breaking changes to existing endpoints | Validation | SC-1 through SC-5 | All pre-existing integration tests pass alongside new auth test suite; no regressions | M | P0 |
| 88 | SC-13 | Verify feature flag rollback (AUTH_SERVICE_ENABLED=false reverts behavior) | Validation | OPS-006 | Disabling feature flag causes auth endpoints to return 503 or route to previous behavior; manually verified in staging | M | P0 |
| 89 | SC-14 | Verify database migration 003 rollback drops tables cleanly | Validation | MIG-002 | Down-migration executes; tables removed; no orphaned constraints or sequences; idempotent re-run confirmed | S | P0 |
| 90 | OPS-006 | Configure feature flag (AUTH_SERVICE_ENABLED) for gradual production rollout | Deployment | — | Feature flag toggles auth service availability; defaults to disabled; rollback < 30s | S | P0 |
| 91 | OPS-007 | Deploy to staging environment and execute smoke tests | Deployment | SC-6, SC-12 | All auth endpoints functional in staging; E2E lifecycle passes; no regressions in existing endpoints | M | P0 |
| 92 | OPS-008 | Deploy to production with feature flag enabled; confirm monitoring active | Deployment | OPS-007, SC-13 | Production deploy successful; feature flag enabled for canary percentage; APM and health check monitoring confirm normal operation | M | P0 |

---

## 4. Risk Assessment & Mitigation Strategies

| Risk | Probability | Severity | Mitigation Strategy | Addressed By |
|------|-------------|----------|---------------------|--------------|
| **R-1: JWT private key compromise** | Low | High | RS256 asymmetric keys (private never leaves secrets manager); 90-day rotation with kid-based versioning; anomalous token pattern monitoring | OPS-002, OQ-8, R-1 task |
| **R-2: Refresh token replay attack** | Medium | High | Token rotation on every refresh; replay detection triggers full user revocation (FR-AUTH.3c); client fingerprint binding evaluated (R-2 task) | FR-AUTH.3c, R-2 task |
| **R-3: bcrypt cost factor obsolescence** | Low | Medium | Cost factor configurable via environment; annual OWASP benchmark review; Argon2id migration path documented | COMP-001, R-3 task |
| **R-4: Latency conflict (bcrypt vs. p95)** | Medium | Medium | **Must resolve in Phase 0** (OQ-3). Options: (a) async hashing offloaded to worker, (b) adjust p95 target to 300ms for login only, (c) reduce cost factor to 10. Decision drives NFR-AUTH.1 implementation. | OQ-3, R-4 task, NFR-AUTH.1 |
| **R-5: Email service unavailability** | Medium | Low | Email adapter with retry + exponential backoff; queue-based dispatch (if OQ-1 resolves to async); graceful user messaging on failure | COMP-007, R-5 task |
| **R-6: Distributed brute-force (no lockout)** | Medium | Medium | Progressive account lockout policy (OQ-4); account-level failure tracking across IPs; automated unlock after cooling period | OQ-4, R-6 task |

**Residual risk after mitigation**: R-2 (replay) remains the highest residual risk. Token rotation with replay detection reduces it significantly, but a stolen refresh token used before the legitimate client refreshes creates a race condition. Client fingerprint binding (evaluated in R-2 task) would further reduce this surface.

---

## 5. Resource Requirements & Dependencies

### Team Resources

| Role | Allocation | Phase Coverage |
|------|-----------|----------------|
| Backend Engineer | 1 FTE | Phases 0–3 (core implementation) |
| Security Engineer | 0.5 FTE | Phases 0, 4 (architecture review, hardening) |
| QA/Test Engineer | 0.5 FTE | Phases 1–5 (test suite, load testing) |
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

Validation is layered across three tiers:

1. **Unit tests** (Phase 0–1): Verify individual components — PasswordHasher, JwtService, TokenManager, auth-middleware — in isolation. ~15 test cases.
2. **Integration tests** (Phase 1–3): Verify each endpoint against its full acceptance criteria with a real database. ~20 test cases covering FR-AUTH.1 through FR-AUTH.5.
3. **E2E + Security + Load tests** (Phase 4–5): Verify the complete user lifecycle, sensitive field exclusion, enumeration resistance, rate limiting behavior, and p95 latency. ~10 test cases.

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
| SC-13 | Feature flag rollback | OPS-006 manual verification | Phase 5 |
| SC-14 | Migration rollback | MIG-002 rollback test | Phase 5 |

---

## 7. Timeline Estimates

| Phase | Duration | Cumulative | Key Dependency |
|-------|----------|------------|----------------|
| **Phase 0**: Foundation & Architecture | 1.5 weeks | Week 1.5 | OQ-3 resolution gates all performance work |
| **Phase 1**: Registration & Login | 1.5 weeks | Week 3 | Phase 0 services and migration |
| **Phase 2**: Token Lifecycle & Profile | 1 week | Week 4 | Phase 1 login (tokens required for profile auth) |
| **Phase 3**: Password Reset | 1 week | Week 5 | OQ-7 email interface; Phase 0 services |
| **Phase 4**: NFR & Hardening | 1.5 weeks | Week 6.5 | All functional endpoints complete |
| **Phase 5**: Validation & Deploy | 1 week | **Week 7.5** | All phases complete |

**Total estimated duration**: ~7.5 weeks with 1 backend FTE + fractional security/QA/DevOps support.

**Parallelization opportunity**: Phase 3 (password reset) can begin concurrently with Phase 2 if the email service interface (OQ-7) is resolved in Phase 0. This could compress the timeline to ~6.5 weeks.

**Critical path**: OQ-3 → Phase 0 infra → Phase 1 login → Phase 2 token refresh → Phase 5 E2E validation → Production deploy.
