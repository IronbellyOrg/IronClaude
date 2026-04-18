---
spec_source: "test-tdd-user-auth.md"
prd_source: "test-prd-user-auth.md"
extraction_source: "results/test4-spec-prd-tdd/extraction.md"
complexity_score: 0.72
complexity_class: "HIGH"
primary_persona: architect
total_entities: 144
estimated_task_rows: 166
actual_task_rows: 181
domains_covered: [backend, security, frontend, infrastructure, operations, compliance]
milestones: [M1, M2, M3, M4, M5]
phases: 6
target_release: "v1.0"
---

# User Authentication Service — Project Roadmap

## 1. Executive Summary

This roadmap translates the User Authentication Service TDD (AUTH-001-TDD) and its parent PRD (AUTH-PRD-001) into a phased implementation plan covering 181 task rows across 6 phases, targeting GA release by 2026-06-09.

The system delivers secure identity management for the platform through `AuthService` as the primary orchestrator, delegating to `TokenManager`, `JwtService`, and `PasswordHasher` for specialized concerns. It exposes a RESTful API consumed by `LoginPage`, `RegisterPage`, and the `AuthProvider` context wrapper, backed by PostgreSQL for user persistence and Redis for refresh token lifecycle.

**Architectural headline:** JWT-based stateless authentication with dual-token lifecycle (15-minute access / 7-day refresh), bcrypt password hashing at cost factor 12, RS256 token signing, and a 3-phase rollout (alpha → 10% beta → GA) gated by two feature flags.

**Business context (from PRD):** Authentication unblocks ~$2.4M in projected annual revenue from personalization-dependent features and is prerequisite for SOC2 Type II audit compliance in Q3 2026. Registration conversion target > 60%, login p95 < 200ms.

**Complexity assessment:** 0.72 (HIGH) — driven by 6-domain span (backend, security, frontend, infrastructure, operations, compliance), dual data stores, 3-phase rollout with automated rollback criteria, and SOC2/GDPR compliance requirements compounding security surface area.

**Phase summary:**

| Phase | Scope | Timeline | Task Rows | Critical Path |
|-------|-------|----------|-----------|---------------|
| 1 | Foundation & Core Auth | 2026-04-01 → 2026-04-14 | 28 | Yes |
| 2 | Token Management & Session | 2026-04-15 → 2026-04-28 | 26 | Yes |
| 3 | Password Reset & Frontend | 2026-04-29 → 2026-05-26 | 27 | Yes |
| 4 | Security, Testing & QA | 2026-05-27 → 2026-06-02 | 31 | Yes |
| 5 | Migration, Rollout & Ops | 2026-06-03 → 2026-06-09+ | 36 | Yes |
| 6 | PRD Traceability & Acceptance | Continuous / Post-GA | 33 | No |

---

## 2. Integration Points

The following dispatch mechanisms, registries, and wiring points require explicit task coverage beyond standard skeleton→implement phasing:

| # | Named Artifact | Type | Wired Components | Owning Phase | Cross-Reference Phases |
|---|----------------|------|------------------|-------------|----------------------|
| 1 | **AuthService constructor / DI container** | Dependency injection | TokenManager, PasswordHasher, UserRepo | Phase 1 (COMP-001) | Phase 2 (TokenManager wiring, row 42) |
| 2 | **Auth Router (`/auth/*`)** | Middleware chain / route dispatch | login, register, me, refresh, reset-request, reset-confirm handlers | Phase 1 (API-001, API-002) | Phase 2 (API-003, API-004), Phase 3 (API-005, API-006) |
| 3 | **Bearer Token Middleware** | Middleware chain | JwtService.verify(), protected routes (/auth/me, /profile) | Phase 2 (row 44) | Phase 3 (COMP-009) |
| 4 | **AuthProvider React Context** | Context / event binding | LoginPage, RegisterPage, ProfilePage, token refresh interceptor, 401 redirect | Phase 3 (COMP-008) | Phase 3 (COMP-006, COMP-007, COMP-009), Phase 4 (TEST-006) |
| 5 | **Feature Flag Registry** | Strategy / dispatch | AUTH_NEW_LOGIN (gates LoginPage + AuthService), AUTH_TOKEN_REFRESH (gates TokenManager refresh) | Phase 5 (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH) | Phase 5 (MIG-001 through MIG-003) |
| 6 | **Rate Limit Config** | Middleware chain | /auth/login (10/min/IP), /auth/register (5/min/IP), /auth/me (60/min/user), /auth/refresh (30/min/user) | Phase 1 (R-002) | Phase 2 (row 47), Phase 4 (row 100) |
| 7 | **Prometheus Metrics Registry** | Registry | auth_login_total, auth_login_duration_seconds, auth_token_refresh_total, auth_registration_total | Phase 5 (OPS-006 through OPS-009) | Phase 5 (OPS-003/004 alert rules, Grafana dashboard) |
| 8 | **PasswordHasher Strategy** | Strategy pattern | bcrypt implementation (default); interface designed for future argon2id migration | Phase 1 (COMP-004) | Phase 1 (FR-AUTH-001, FR-AUTH-002), Phase 4 (security review) |

---

## 3. Phased Implementation Plan

### Phase 1: Foundation & Core Auth Infrastructure

**Aligns with:** Milestone M1 (Core AuthService by 2026-04-14), PRD Sprint 1-3 start, Epic AUTH-E1 partial
**Exit criteria:** Login and registration pass integration tests against PostgreSQL; all unit tests for AuthService and PasswordHasher pass
**Duration:** 2 weeks (2026-04-01 → 2026-04-14)

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 1 | AUTH-001-TDD | Establish TDD as authoritative design specification | Documentation | — | TDD reviewed and baselined by auth-team; all sections verified complete | S | P0 |
| 2 | AUTH-PRD-001 | Validate PRD-to-TDD requirement traceability mapping | Documentation | AUTH-001-TDD | All 5 FR pairs (FR-AUTH-001↔FR-AUTH.1 through FR-AUTH-005↔FR-AUTH.5) mapped; no orphan requirements | S | P0 |
| 3 | SEC-POLICY-001 | Review and integrate security policy requirements into design | Security | AUTH-001-TDD | bcrypt cost factor 12 and RS256 2048-bit confirmed per SEC-POLICY-001 | S | P0 |
| 4 | INFRA-DB-001 | Provision PostgreSQL 15+ with connection pooling | Infrastructure | — | PostgreSQL accessible; pg-pool configured with 100 connections; connection verified from app layer | M | P0 |
| 5 | — | Provision Redis 7+ for refresh token storage | Infrastructure | — | Redis cluster running with 1GB memory; RESP protocol accessible; latency < 10ms from app | M | P0 |
| 6 | — | Initialize Node.js 20 LTS project with TypeScript configuration | Infrastructure | — | Project scaffolded with tsconfig strict mode, ESLint, package.json with dependencies | S | P0 |
| 7 | — | Configure API Gateway with CORS, TLS 1.3, and route mapping | Infrastructure | INFRA-DB-001 | Gateway routes /auth/* to AuthService; TLS 1.3 enforced; CORS restricted to known origins | M | P1 |
| 8 | G-001 | Define AuthService login and registration interface contracts | AuthService | SEC-POLICY-001 | TypeScript interfaces for login(), register() with input/output types defined and reviewed | S | P0 |
| 9 | DM-001 | Create UserProfile database schema and migrations | Database | INFRA-DB-001 | users table with id (UUID PK), email (UNIQUE, indexed), displayName, createdAt, updatedAt, lastLoginAt, roles; migration scripts versioned | M | P0 |
| 10 | — | Implement UserProfile field validations and constraints | Database | DM-001 | Email normalized to lowercase; displayName 2-100 chars; UUID v4 primary key; roles defaults to ["user"] | S | P0 |
| 11 | — | Create UserProfile TypeScript interface and DTO | AuthService | DM-001 | Interface matches TDD §7.1 field table exactly; DTO handles serialization | S | P0 |
| 12 | — | Create audit_log table schema for auth events | Database | INFRA-DB-001 | Table stores login attempts, password resets with user_id, event_type, timestamp, ip_address, outcome; 90-day retention policy | M | P1 |
| 13 | COMP-005 | Implement UserRepo data access layer | AuthService | DM-001 | CRUD operations for UserProfile; connection pooling via pg-pool; parameterized queries (no SQL injection) | M | P0 |
| 14 | — | Implement UserRepo findByEmail with indexed lookup | AuthService | COMP-005 | Email lookup < 10ms on indexed column; returns null for non-existent (no enumeration) | S | P0 |
| 15 | NFR-SEC-001 | Implement PasswordHasher with bcrypt cost factor 12 | AuthService | SEC-POLICY-001 | hash() and verify() methods; cost factor 12; hash time benchmarked < 500ms | M | P0 |
| 16 | COMP-004 | Build PasswordHasher abstraction layer with strategy interface | AuthService | NFR-SEC-001 | Algorithm-agnostic interface; bcrypt as default implementation; designed for future argon2id migration | M | P0 |
| 17 | COMP-001 | Implement AuthService orchestration layer with dependency injection | AuthService | COMP-004, COMP-005 | Facade accepts injected PasswordHasher and UserRepo; no direct DB or crypto access; constructor validates dependencies | L | P0 |
| 18 | FR-AUTH-001 | Implement login flow: validate credentials and return AuthToken | AuthService | COMP-001, COMP-004 | Valid creds → 200 with AuthToken; invalid → 401; non-existent email → 401 (no enumeration); locked → 423 after 5 failures in 15 min | L | P0 |
| 19 | — | Implement account lockout after 5 failed attempts within 15 minutes | AuthService | FR-AUTH-001 | 6th failed attempt within 15 min returns 423 Locked; lockout clears automatically after 15 min; lockout tracked per email | M | P0 |
| 20 | FR-AUTH-002 | Implement registration flow: validate, hash password, persist UserProfile | AuthService | COMP-001, COMP-004, DM-001 | Valid input → 201 with UserProfile; duplicate email → 409 Conflict; weak password → 400; bcrypt hash stored via PasswordHasher | L | P0 |
| 21 | — | Implement password strength validation rules | AuthService | FR-AUTH-002 | Minimum 8 characters, at least 1 uppercase letter, at least 1 number required; 400 with field-level error on violation | S | P0 |
| 22 | — | Implement email format validation and uniqueness enforcement | AuthService | FR-AUTH-002, COMP-005 | RFC 5322 email format check; database unique constraint catches race conditions; 409 on duplicate | S | P0 |
| 23 | API-001 | Implement POST /auth/login endpoint handler | API | FR-AUTH-001 | JSON request/response per TDD §8.2; returns 200/401/429/423 status codes with standardized error format | M | P0 |
| 24 | API-002 | Implement POST /auth/register endpoint handler | API | FR-AUTH-002 | JSON request/response per TDD §8.2; returns 201/400/409 status codes with standardized error format | M | P0 |
| 25 | — | Implement standardized error response format across all endpoints | API | API-001, API-002 | All errors follow `{error: {code, message, status}}` per TDD §8.3; error codes are AUTH_* prefixed | S | P0 |
| 26 | R-002 | Configure API Gateway rate limiting on login and register endpoints | API Gateway | API-001, API-002 | /auth/login: 10 req/min per IP; /auth/register: 5 req/min per IP; 429 returned on exceed | M | P0 |
| 27 | — | Implement API versioning with /v1/ URL prefix | API | API-001, API-002 | All endpoints accessible under /v1/auth/*; versioning strategy documented | S | P1 |
| 28 | M1 | **Milestone gate:** Core AuthService complete | Milestone | FR-AUTH-001, FR-AUTH-002, API-001, API-002 | Login and registration pass integration tests against PostgreSQL; all unit tests pass; auth-team sign-off | S | P0 |

**Phase 1 total: 28 rows**

---

### Phase 2: Token Management & Session Persistence

**Aligns with:** Milestone M2 (Token Management by 2026-04-28), PRD Sprint 1-3 continuation, Epic AUTH-E2
**Exit criteria:** Token issuance, refresh, and revocation pass integration tests against Redis; p95 latency confirmed < 200ms
**Duration:** 2 weeks (2026-04-15 → 2026-04-28)

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 29 | G-002 | Define stateless token-based session architecture | Architecture | M1 | JWT access + opaque refresh token design documented; dual-token lifecycle approved by architect | S | P0 |
| 30 | DM-002 | Create AuthToken response interface and DTO | AuthService | G-002 | Interface with accessToken, refreshToken, expiresIn (900), tokenType ("Bearer") per TDD §7.1 | S | P0 |
| 31 | — | Create refresh_tokens Redis key schema with TTL | Database | G-002 | Key format defined; 7-day TTL per token; hash-before-store strategy documented | S | P0 |
| 32 | NFR-SEC-002 | Generate and configure RS256 2048-bit RSA key pair | Security | SEC-POLICY-001 | Key pair generated; private key stored in secrets manager; public key distributable for verification | M | P0 |
| 33 | — | Implement RSA key rotation mechanism with quarterly cadence | Security | NFR-SEC-002 | Rotation procedure documented; old keys remain valid for verification during 30-day transition window | M | P1 |
| 34 | COMP-003 | Implement JwtService sign and verify operations with RS256 | AuthService | NFR-SEC-002 | sign() returns RS256 JWT with payload; verify() validates signature and expiry; < 5ms per operation | M | P0 |
| 35 | — | Configure JWT payload structure with user id and roles | AuthService | COMP-003, DM-001 | JWT payload contains sub (user id), roles array, iat, exp; no sensitive data in payload | S | P0 |
| 36 | — | Implement 5-second clock skew tolerance in JwtService verification | AuthService | COMP-003 | Token verification tolerates ±5s clock drift per TDD §12 edge case specification | S | P1 |
| 37 | COMP-002 | Implement TokenManager token lifecycle management | AuthService | COMP-003 | issueTokens() creates access + refresh pair; stores refresh token hash in Redis with 7-day TTL | L | P0 |
| 38 | — | Implement refresh token hashing before Redis storage | TokenManager | COMP-002 | Refresh tokens stored as hashed values in Redis; raw token never persisted server-side | M | P0 |
| 39 | — | Implement refresh token revocation in TokenManager | TokenManager | COMP-002 | revokeToken() atomically deletes hash from Redis; subsequent refresh attempts return 401 | M | P0 |
| 40 | — | Implement token rotation on refresh (old revoked, new issued) | TokenManager | COMP-002 | Old refresh token revoked atomically when new AuthToken pair issued; no window for replay | M | P0 |
| 41 | FR-AUTH-003 | Implement JWT access tokens (15-min) and refresh tokens (7-day) | TokenManager | COMP-002, COMP-003 | Access token 900s TTL via JwtService; refresh token 604800s TTL in Redis via TokenManager | L | P0 |
| 42 | — | Wire TokenManager into AuthService login flow | AuthService | FR-AUTH-003, FR-AUTH-001 | Successful login calls TokenManager.issueTokens() and returns AuthToken to client | M | P0 |
| 43 | FR-AUTH-004 | Implement user profile retrieval from JWT access token | AuthService | COMP-003, COMP-005 | Extract user ID from JWT sub claim; query UserRepo; return UserProfile with all 7 fields per TDD §8.2 | M | P0 |
| 44 | — | Implement Bearer token extraction and verification middleware | API | COMP-003 | Authorization header parsed; "Bearer " prefix stripped; JwtService.verify() called; 401 on failure | M | P0 |
| 45 | API-003 | Implement GET /auth/me endpoint with JWT authentication | API | FR-AUTH-004 | Returns UserProfile JSON for valid Bearer token; 401 for missing, expired, or invalid token | M | P0 |
| 46 | API-004 | Implement POST /auth/refresh endpoint with token rotation | API | FR-AUTH-003 | Accepts refreshToken in body; returns new AuthToken pair via TokenManager; 401 for expired or revoked | M | P0 |
| 47 | — | Configure rate limiting on /auth/me and /auth/refresh endpoints | API Gateway | API-003, API-004 | /auth/me: 60 req/min per user; /auth/refresh: 30 req/min per user; 429 on exceed | S | P1 |
| 48 | — | Handle Redis unavailability gracefully for refresh requests | TokenManager | COMP-002 | Redis unreachable → reject refresh with 401 (fail closed); log error; do not serve stale tokens | M | P1 |
| 49 | NFR-PERF-001 | Validate all auth endpoints respond < 200ms at p95 | Performance | API-001, API-002, API-003, API-004 | k6 load test confirms p95 < 200ms across all four endpoints under normal load | M | P0 |
| 50 | NFR-PERF-002 | Validate support for 500 concurrent login requests | Performance | API-001 | k6 script simulates 500 concurrent logins; zero 5xx errors; p95 remains < 200ms | M | P0 |
| 51 | NFR-REL-001 | Configure health check endpoint for availability monitoring | Operations | COMP-001 | GET /health returns 200 when PostgreSQL and Redis reachable; monitoring polls every 30s; feeds 99.9% SLA tracking | S | P0 |
| 52 | — | Implement connection pool monitoring and alerting | Infrastructure | INFRA-DB-001 | pg-pool metrics exposed via Prometheus; alert configured on connection wait time > 50ms | S | P1 |
| 53 | G-004 | Validate profile management flow end-to-end | Validation | FR-AUTH-004, API-003 | GET /auth/me returns accurate UserProfile including updated lastLoginAt timestamp after login | S | P0 |
| 54 | M2 | **Milestone gate:** Token Management validated | Milestone | FR-AUTH-003, FR-AUTH-004, API-003, API-004 | Token issuance, refresh, and revocation pass integration tests against Redis; p95 latency confirmed | S | P0 |

**Phase 2 total: 26 rows | Cumulative: 54 rows**

---

### Phase 3: Password Reset & Frontend Integration

**Aligns with:** Milestones M3 (Password Reset by 2026-05-12) and M4 (Frontend Integration by 2026-05-26), PRD Sprint 4-6, Epics AUTH-E1 completion + AUTH-E3
**Exit criteria:** E2E tests pass through LoginPage and RegisterPage; password reset flow verified with email delivery
**Duration:** 4 weeks (2026-04-29 → 2026-05-26)

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 55 | G-003 | Define password reset two-step flow architecture | Architecture | M2 | Request → email with token → confirm with new password flow documented; 1-hour TTL and single-use constraints specified | S | P0 |
| 56 | FR-AUTH-005 | Implement password reset request and confirmation in AuthService | AuthService | G-003, COMP-004 | POST /reset-request sends email; POST /reset-confirm updates hash via PasswordHasher; token expires after 1 hour; single-use enforced | L | P0 |
| 57 | API-005 | Implement POST /auth/reset-request endpoint | API | FR-AUTH-005 | Accepts email in body; sends reset token via email; returns 200 regardless of registration status (no enumeration) | M | P0 |
| 58 | API-006 | Implement POST /auth/reset-confirm endpoint | API | FR-AUTH-005 | Validates reset token; updates password via PasswordHasher; invalidates all existing sessions via TokenManager | M | P0 |
| 59 | — | Implement cryptographic reset token generation and storage | AuthService | FR-AUTH-005 | Cryptographically random token generated; stored as hash with 1-hour TTL; single-use flag tracked | M | P0 |
| 60 | — | Implement reset token expiry validation and reuse prevention | AuthService | FR-AUTH-005 | Expired tokens → 400 with clear message; used tokens → 400; old tokens cleaned up on schedule | S | P0 |
| 61 | — | Integrate SendGrid API for password reset email delivery | AuthService | FR-AUTH-005 | Reset email delivered within 60 seconds of request; contains reset link with token; branded template | M | P0 |
| 62 | — | Implement email delivery monitoring and single retry on failure | Operations | API-005 | Failed deliveries logged and retried once; alert fires if failure rate > 5% over 5 minutes | M | P1 |
| 63 | — | Prevent user enumeration on reset-request endpoint | Security | API-005 | Identical 200 response body and timing for registered and unregistered emails | S | P0 |
| 64 | G-005 | Define frontend integration contracts and component specifications | Architecture | M2 | API contracts for LoginPage, RegisterPage, AuthProvider, ProfilePage documented; prop interfaces defined | S | P0 |
| 65 | COMP-006 | Implement LoginPage component with email/password form | Frontend | API-001, G-005 | Renders email and password fields; submits to POST /auth/login; stores AuthToken via AuthProvider; redirects on success | L | P0 |
| 66 | — | Implement LoginPage error states and messaging | Frontend | COMP-006 | 401 → generic "Invalid email or password"; 423 → locked message with retry timing; 429 → rate limit message | M | P0 |
| 67 | — | Implement LoginPage "Forgot Password" navigation | Frontend | COMP-006, API-005 | Links to password reset request form; accessible from login page | S | P1 |
| 68 | COMP-007 | Implement RegisterPage component with validation | Frontend | API-002, G-005 | Renders email, password, displayName fields; client-side validation; submits to POST /auth/register; handles success and errors | L | P0 |
| 69 | — | Implement RegisterPage inline password strength feedback | Frontend | COMP-007 | Real-time validation: min 8 chars, 1 uppercase, 1 number; visual indicators for met/unmet criteria | S | P0 |
| 70 | — | Implement RegisterPage duplicate email error handling | Frontend | COMP-007 | 409 → suggest login or password reset with actionable links; no duplicate account created | S | P0 |
| 71 | COMP-008 | Implement AuthProvider context wrapper for application-wide auth state | Frontend | COMP-003, FR-AUTH-003 | Manages AuthToken state; exposes user, login(), logout(), isAuthenticated to component tree via React context | L | P0 |
| 72 | — | Implement silent token refresh in AuthProvider before access token expiry | Frontend | COMP-008 | Monitors access token exp claim; triggers POST /auth/refresh transparently before expiry; no user interruption | M | P0 |
| 73 | — | Implement 401 response interception and redirect in AuthProvider | Frontend | COMP-008 | 401 on any request → attempt token refresh; if refresh fails → redirect to LoginPage with return URL | M | P0 |
| 74 | — | Implement secure token storage strategy per R-001 mitigation | Frontend | COMP-008, R-001 | accessToken held in memory only (not localStorage); refreshToken in HttpOnly cookie; tokens cleared on tab close | M | P0 |
| 75 | COMP-009 | Implement ProfilePage component displaying UserProfile data | Frontend | API-003, COMP-008 | Displays displayName, email, createdAt from GET /auth/me; renders in < 1 second; requires authentication | M | P1 |
| 76 | — | Implement frontend routing for all auth pages | Frontend | COMP-006, COMP-007, COMP-009 | /login → LoginPage; /register → RegisterPage; /profile → ProfilePage (protected); 404 for unknown auth routes | M | P0 |
| 77 | — | Implement protected route guard using AuthProvider context | Frontend | COMP-008 | Unauthenticated access to /profile redirects to /login with return URL preserved | S | P0 |
| 78 | FE-AUTH-001-TDD | Document frontend accessibility requirements handoff | Documentation | COMP-006, COMP-007 | Accessibility spec referenced for LoginPage and RegisterPage; ARIA labels, keyboard nav, screen reader compatibility noted | S | P1 |
| 79 | R-001 | Implement XSS token theft mitigations across frontend | Security | COMP-008 | Access token memory-only storage; HttpOnly refresh cookie; CSP headers; tokens cleared on tab close | M | P0 |
| 80 | M3 | **Milestone gate:** Password Reset flow validated | Milestone | FR-AUTH-005, API-005, API-006 | Reset request and confirm pass integration tests; email delivery verified within 60s; single-use enforced | S | P0 |
| 81 | M4 | **Milestone gate:** Frontend Integration validated | Milestone | COMP-006, COMP-007, COMP-008, COMP-009 | LoginPage, RegisterPage, AuthProvider, ProfilePage functional in staging environment | S | P0 |

**Phase 3 total: 27 rows | Cumulative: 81 rows**

---

### Phase 4: Security, Testing & Quality Assurance

**Aligns with:** TDD §15 Testing Strategy, TDD §13 Security Considerations, TDD §24 Release Criteria
**Exit criteria:** Unit coverage > 80% for core components; integration tests pass against real PostgreSQL and Redis; E2E tests pass through UI; security review completed
**Duration:** 1 week (2026-05-27 → 2026-06-02)

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 82 | TEST-001 | Unit test: Login with valid credentials returns AuthToken | Testing | FR-AUTH-001 | AuthService.login() → PasswordHasher.verify() true → TokenManager.issueTokens() → valid AuthToken with accessToken and refreshToken | M | P0 |
| 83 | TEST-002 | Unit test: Login with invalid credentials returns error | Testing | FR-AUTH-001 | AuthService.login() returns 401 when PasswordHasher.verify() returns false; no AuthToken issued; no user enumeration | S | P0 |
| 84 | TEST-003 | Unit test: Token refresh with valid refresh token | Testing | FR-AUTH-003 | TokenManager.refresh() validates token hash in Redis, revokes old token, issues new AuthToken pair via JwtService | M | P0 |
| 85 | — | Unit test: Registration with valid data creates UserProfile | Testing | FR-AUTH-002 | AuthService.register() validates input, calls PasswordHasher.hash(), persists via UserRepo, returns UserProfile with all fields | M | P0 |
| 86 | — | Unit test: Registration with duplicate email returns 409 | Testing | FR-AUTH-002 | Database unique constraint violation caught and mapped to 409 Conflict with AUTH_EMAIL_EXISTS error code | S | P0 |
| 87 | — | Unit test: Password strength validation rejects weak passwords | Testing | FR-AUTH-002 | Passwords < 8 chars, without uppercase, without number each return 400 with specific field-level error codes | S | P0 |
| 88 | — | Unit test: PasswordHasher uses bcrypt cost factor 12 | Testing | NFR-SEC-001 | Generated hash prefix confirms cost factor 12; verify() round-trip succeeds; hash time < 500ms | S | P0 |
| 89 | — | Unit test: JwtService signs with RS256 and 2048-bit key | Testing | NFR-SEC-002 | Token header alg field equals "RS256"; key length verified ≥ 2048 bits via key introspection | S | P0 |
| 90 | — | Unit test: Account lockout triggers after 5 failed attempts | Testing | FR-AUTH-001 | 5 failures with valid email in 15 min → 6th attempt returns 423 Locked; different email unaffected | M | P0 |
| 91 | — | Unit test: Password reset token single-use enforcement | Testing | FR-AUTH-005 | First confirmation succeeds; second confirmation with same token returns 400 with AUTH_TOKEN_USED error | S | P0 |
| 92 | — | Unit test: Password reset token 1-hour expiry | Testing | FR-AUTH-005 | Token created; clock advanced > 1 hour; confirmation returns 400 with AUTH_TOKEN_EXPIRED error | S | P0 |
| 93 | — | Unit test: UserProfile field validation constraints | Testing | DM-001 | displayName 2-100 chars enforced; email normalized to lowercase; empty roles defaults to ["user"] | S | P0 |
| 94 | TEST-004 | Integration test: Registration persists UserProfile to PostgreSQL | Testing | FR-AUTH-002, INFRA-DB-001 | Full flow from API request → AuthService → PasswordHasher → PostgreSQL insert; UserProfile queryable by email | L | P0 |
| 95 | TEST-005 | Integration test: Expired refresh token rejected by TokenManager | Testing | FR-AUTH-003 | Redis TTL expiration → TokenManager.refresh() returns 401; no new token pair issued | M | P0 |
| 96 | — | Integration test: POST /auth/login returns valid AuthToken | Testing | API-001 | Supertest: seed user → POST /auth/login → 200 with valid JWT; accessToken verifiable with public key | M | P0 |
| 97 | — | Integration test: POST /auth/register persists and returns UserProfile | Testing | API-002 | Supertest: POST /auth/register → 201 with UserProfile; user queryable in database | M | P0 |
| 98 | — | Integration test: GET /auth/me returns UserProfile for valid token | Testing | API-003 | Supertest: login → GET /auth/me with Bearer → 200 with UserProfile matching registered data | M | P0 |
| 99 | — | Integration test: POST /auth/refresh rotates token pair | Testing | API-004 | POST /auth/refresh → new AuthToken; old refresh token no longer valid in Redis | M | P0 |
| 100 | — | Integration test: Rate limiting enforced on auth endpoints | Testing | R-002 | 11th request to /auth/login from same IP within 1 min returns 429 Too Many Requests | M | P1 |
| 101 | TEST-006 | E2E test: User registers and logs in through complete UI journey | Testing | COMP-006, COMP-007 | Playwright: navigate to /register → fill form → submit → redirected → navigate to /login → login → see profile | L | P0 |
| 102 | — | E2E test: AuthProvider performs silent token refresh during session | Testing | COMP-008 | Session active; access token approaches expiry; AuthProvider refreshes silently; no user-visible interruption | M | P1 |
| 103 | — | E2E test: Password reset end-to-end flow through UI | Testing | COMP-006, API-005, API-006 | Click forgot password → submit email → check email → click link → set new password → login with new password succeeds | L | P1 |
| 104 | — | Configure local test environment with Docker Compose | Testing | INFRA-DB-001 | docker-compose.yml provides PostgreSQL 15 and Redis 7 containers; seeds test data; teardown between runs | M | P0 |
| 105 | — | Configure CI test environment with testcontainers | Testing | — | CI pipeline uses testcontainers for ephemeral PostgreSQL and Redis per test suite run | M | P0 |
| 106 | — | Configure staging test environment with seeded accounts | Testing | — | Staging environment with 100 seeded test accounts; isolated from production; data reset daily | M | P1 |
| 107 | — | Security review: PasswordHasher bcrypt configuration and logging | Security | NFR-SEC-001 | Independent verification of cost factor 12; no plaintext password in application logs or error messages | M | P0 |
| 108 | — | Security review: JwtService RS256 key management and rotation | Security | NFR-SEC-002 | Key rotation procedure documented; private key not exposed in logs, responses, or error stack traces | M | P0 |
| 109 | — | Security review: Token storage, transmission, and lifecycle | Security | R-001 | No tokens in localStorage; HttpOnly cookies configured; TLS 1.3 enforced end-to-end; token cleared on logout | M | P0 |
| 110 | — | Performance test: p95 latency under 500 concurrent users across all endpoints | Performance | NFR-PERF-001, NFR-PERF-002 | k6 load test: 500 concurrent users; all endpoints < 200ms p95; zero 5xx errors; results documented | L | P0 |
| 111 | — | Performance test: PasswordHasher bcrypt benchmark at cost 12 | Performance | NFR-SEC-001 | bcrypt hash() with cost factor 12 completes in < 500ms averaged over 100 iterations | S | P0 |
| 112 | — | Validate unit test coverage exceeds 80% for all core components | Testing | TEST-001, TEST-002, TEST-003 | Coverage report: AuthService > 80%, TokenManager > 80%, JwtService > 80%, PasswordHasher > 80% | M | P0 |

**Phase 4 total: 31 rows | Cumulative: 112 rows**

---

### Phase 5: Migration, Rollout & Operations

**Aligns with:** Milestone M5 (GA Release by 2026-06-09), TDD §19 Migration & Rollout, TDD §14 Observability, TDD §25 Operational Readiness
**Exit criteria:** 99.9% uptime over first 7 days in production; all monitoring dashboards green; feature flags removed
**Duration:** 1 week deploy + 4 weeks stabilization (2026-06-03 → 2026-07-07)

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 113 | AUTH_NEW_LOGIN | Configure AUTH_NEW_LOGIN feature flag in production | Operations | M4 | Flag defaults OFF; gates new LoginPage rendering and AuthService login endpoint routing | S | P0 |
| 114 | AUTH_TOKEN_REFRESH | Configure AUTH_TOKEN_REFRESH feature flag in production | Operations | FR-AUTH-003 | Flag defaults OFF; when OFF only access tokens issued; when ON full refresh token flow via TokenManager enabled | S | P0 |
| 115 | MIG-001 | Deploy AuthService to staging for Internal Alpha (Phase 1) | Migration | M4, AUTH_NEW_LOGIN | AuthService running in staging behind AUTH_NEW_LOGIN flag; all FR-AUTH-001–005 pass manual testing by auth-team and QA; zero P0/P1 bugs | L | P0 |
| 116 | — | Execute auth-team and QA manual testing of all endpoints in Alpha | Migration | MIG-001 | All 6 endpoints (4 specified + 2 reset) manually verified; edge cases from TDD §12 tested; sign-off documented | M | P0 |
| 117 | MIG-002 | Enable AUTH_NEW_LOGIN for 10% Beta traffic (Phase 2) | Migration | MIG-001 | Feature flag set to 10% rollout; canary deployment active; monitoring dashboards baselined | M | P0 |
| 118 | — | Monitor p95 latency during 2-week 10% Beta period | Migration | MIG-002 | p95 < 200ms sustained; any spike > 500ms triggers investigation; daily latency report generated | M | P0 |
| 119 | — | Monitor error rates during 2-week 10% Beta period | Migration | MIG-002 | Error rate < 0.1% sustained; any spike > 1% triggers investigation; daily error report generated | M | P0 |
| 120 | — | Monitor TokenManager Redis usage during Beta | Migration | MIG-002 | Zero Redis connection failures; memory utilization < 70% of 1GB; refresh token count tracking | M | P0 |
| 121 | MIG-003 | Remove AUTH_NEW_LOGIN flag and route 100% traffic to AuthService (Phase 3 GA) | Migration | MIG-002 | All traffic through new AuthService; legacy auth endpoints deprecated; flag configuration removed | M | P0 |
| 122 | — | Enable AUTH_TOKEN_REFRESH for all users post-GA | Migration | MIG-003 | Refresh token flow active for 100% of users; TokenManager handling production refresh volume | S | P0 |
| 123 | — | Deprecate and redirect legacy auth endpoints | Migration | MIG-003 | Legacy endpoints return 301 redirect to new /v1/auth/* endpoints; deprecation notice in response headers | M | P1 |
| 124 | MIG-004 | Document and test complete rollback procedure | Operations | MIG-001 | Rollback tested in staging; disable AUTH_NEW_LOGIN → verify legacy login → investigate → restore flow documented | M | P0 |
| 125 | MIG-005 | Configure automated rollback trigger: p95 latency > 1000ms for 5 min | Operations | MIG-004 | Prometheus alert rule fires; PagerDuty notification sent; runbook link included in alert | S | P0 |
| 126 | MIG-006 | Configure automated rollback trigger: error rate > 5% for 2 min | Operations | MIG-004 | Prometheus alert rule fires; PagerDuty notification sent; auto-rollback script available | S | P0 |
| 127 | MIG-007 | Configure automated rollback trigger: Redis failures > 10/min | Operations | MIG-004 | Prometheus alert rule fires; escalation to platform-team if Redis cluster issue | S | P0 |
| 128 | MIG-008 | Configure automated rollback trigger: data loss or corruption detection | Operations | MIG-004 | Integrity check runs every 5 min during rollout; detects UserProfile record corruption; triggers rollback | M | P0 |
| 129 | MIG-009 | Validate UserProfile data migration script with production-like dataset | Migration | DM-001 | Idempotent upsert operations; tested against 100K+ user dataset; zero data loss; migration reversible | L | P0 |
| 130 | MIG-010 | Execute legacy auth endpoint removal 2 weeks post-GA | Migration | MIG-003 | Legacy endpoints removed; communication sent to platform-team and frontend-team; 301 redirects remain for 30 days | M | P1 |
| 131 | OPS-001 | Create runbook: AuthService down scenario | Operations | COMP-001 | Symptoms, diagnosis (pod health, PostgreSQL, PasswordHasher/TokenManager init), resolution, escalation per TDD §25.1 | M | P0 |
| 132 | OPS-002 | Create runbook: Token refresh failure scenario | Operations | COMP-002 | Redis connectivity check, JwtService key check, AUTH_TOKEN_REFRESH flag check, escalation path documented per TDD §25.1 | M | P0 |
| 133 | OPS-003 | Configure Prometheus alert: login failure rate > 20% over 5 min | Monitoring | OPS-001 | Alert rule deployed; routes to auth-team PagerDuty; includes runbook link | S | P0 |
| 134 | OPS-004 | Configure Prometheus alert: p95 latency exceeding 500ms | Monitoring | OPS-001 | Alert rule deployed; routes to auth-team on-call; includes dashboard link | S | P0 |
| 135 | OPS-005 | Configure Prometheus alert: TokenManager Redis connection failures | Monitoring | OPS-002 | Alert rule deployed; escalates to platform-team if unresolved in 15 min | S | P0 |
| 136 | OPS-006 | Implement auth_login_total Prometheus counter metric | Monitoring | COMP-001 | Counter increments on every login attempt; labeled by outcome (success/failure/locked) | S | P0 |
| 137 | OPS-007 | Implement auth_login_duration_seconds Prometheus histogram | Monitoring | COMP-001 | Histogram with buckets [0.01, 0.05, 0.1, 0.2, 0.5, 1.0] for login latency distribution | S | P0 |
| 138 | OPS-008 | Implement auth_token_refresh_total Prometheus counter metric | Monitoring | COMP-002 | Counter for refresh attempts; labeled by outcome (success/expired/revoked/error) | S | P0 |
| 139 | OPS-009 | Implement auth_registration_total Prometheus counter metric | Monitoring | COMP-001 | Counter for registration attempts; labeled by outcome (success/duplicate/validation_error) | S | P0 |
| 140 | — | Configure OpenTelemetry distributed tracing across auth components | Monitoring | COMP-001, COMP-002, COMP-003, COMP-004 | Spans cover full request lifecycle: AuthService → PasswordHasher → TokenManager → JwtService; trace ID propagated | M | P1 |
| 141 | — | Build Grafana monitoring dashboard for auth service metrics | Monitoring | OPS-006, OPS-007, OPS-008, OPS-009 | Dashboard displays all 4 metrics with time-series; linked to alert rules; accessible to on-call team | M | P1 |
| 142 | OPS-010 | Configure Kubernetes HPA for AuthService pod auto-scaling | Infrastructure | COMP-001 | Scale from 3 to 10 replicas when CPU > 70%; verified under 500-concurrent-user load test | M | P0 |
| 143 | OPS-011 | Configure PostgreSQL connection pool scaling with monitoring | Infrastructure | INFRA-DB-001 | Increase pool from 100 to 200 if connection wait time > 50ms; alert on pool exhaustion | S | P1 |
| 144 | OPS-012 | Configure Redis memory auto-scaling with monitoring | Infrastructure | — | Scale from 1GB to 2GB if utilization > 70%; alert on memory pressure; ~100K tokens ≈ 50MB baseline | S | P1 |
| 145 | — | Establish auth-team 24/7 on-call rotation for post-GA period | Operations | OPS-001, OPS-002 | Rotation covers first 2 weeks post-GA; P1 acknowledge within 15 min; escalation path tested | M | P0 |
| 146 | — | Execute and verify full database backup before each migration phase | Operations | MIG-001 | Backup taken before Alpha, Beta, and GA phases; backup restoration tested; RPO < 1 hour | M | P0 |
| 147 | R-003 | Implement data loss mitigation strategy during migration | Migration | MIG-009 | AuthService runs parallel with legacy during Phases 1-2; idempotent upserts; pre-migration backup verified restorable | M | P0 |
| 148 | M5 | **Milestone gate:** GA Release validated | Milestone | MIG-003 | 99.9% uptime over first 7 days; all Grafana dashboards green; AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH flags removed post-stabilization | S | P0 |

**Phase 5 total: 36 rows | Cumulative: 148 rows**

---

### Phase 6: PRD Traceability & Acceptance Validation

**Aligns with:** PRD acceptance criteria, legal/compliance requirements, customer journey validation, epic sign-off
**Exit criteria:** All PRD FRs, NFRs, user stories, and compliance requirements validated against implemented system; traceability matrix complete
**Duration:** Continuous during Phases 4-5 and post-GA (2026-05-27 → 2026-07-07)

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|-----|------|-----------|--------------|---------------------|--------|----------|
| 149 | FR-AUTH.1 | Verify login delivers persistent session per PRD acceptance criteria | Validation | FR-AUTH-001 | Valid credentials authenticate user for ≥ 15 minutes without re-entry; session maintained across navigations | S | P0 |
| 150 | FR-AUTH.2 | Verify registration creates account per PRD acceptance criteria | Validation | FR-AUTH-002 | Unique email + valid password creates account and logs user in immediately; duplicate emails rejected with helpful message | S | P0 |
| 151 | FR-AUTH.3 | Verify session persists across page refreshes per PRD acceptance criteria | Validation | FR-AUTH-003 | Active sessions extend automatically within 7-day refresh window; no re-login on page refresh | S | P0 |
| 152 | FR-AUTH.4 | Verify profile shows name, email, creation date per PRD acceptance criteria | Validation | FR-AUTH-004 | Authenticated users see displayName, email, createdAt on profile page; data matches registration input | S | P0 |
| 153 | FR-AUTH.5 | Verify self-service password reset via email per PRD acceptance criteria | Validation | FR-AUTH-005 | Reset email with time-limited link (1 hour); new password invalidates all existing sessions | S | P0 |
| 154 | NFR-AUTH.1 | Validate 200ms p95 response time and 500 concurrent capacity per PRD | Validation | NFR-PERF-001, NFR-PERF-002 | Load test results documented confirming PRD NFR-AUTH.1 targets met under production-like conditions | S | P0 |
| 155 | NFR-AUTH.2 | Validate 99.9% availability over 30-day rolling window per PRD | Validation | NFR-REL-001 | Uptime monitoring confirms 99.9% over first 30 days post-GA; SLA calculation documented | S | P0 |
| 156 | NFR-AUTH.3 | Validate industry-standard one-way password hashing per PRD | Validation | NFR-SEC-001 | bcrypt with cost factor 12 verified; no plaintext storage or logging confirmed by security review | S | P0 |
| 157 | AUTH-E1 | Validate Epic: Login and Registration complete with all user stories passing | Validation | FR-AUTH-001, FR-AUTH-002 | Register, login, and logout user stories pass acceptance criteria; no P0/P1 defects open | S | P0 |
| 158 | AUTH-E2 | Validate Epic: Token Management complete with all user stories passing | Validation | FR-AUTH-003 | Session persistence and programmatic token refresh user stories pass acceptance criteria | S | P0 |
| 159 | AUTH-E3 | Validate Epic: Profile and Password Reset complete with all user stories passing | Validation | FR-AUTH-004, FR-AUTH-005 | Profile view, password reset, and audit log user stories pass acceptance criteria | S | P0 |
| 160 | — | Validate user story: Alex registers with email and password (AUTH-E1) | Validation | AUTH-E1, COMP-007 | Form accepts email/password/displayName; duplicate emails rejected with helpful message; success logs user in immediately | S | P0 |
| 161 | — | Validate user story: Alex logs in with email and password (AUTH-E1) | Validation | AUTH-E1, COMP-006 | Correct credentials grant access; incorrect show generic error; no user enumeration possible | S | P0 |
| 162 | — | Validate user story: Alex logs out to secure shared device (AUTH-E1) | Validation | AUTH-E1, COMP-008 | Logout ends session immediately; tokens cleared; redirect to landing page | S | P0 |
| 163 | — | Validate user story: Alex session persists across page refreshes (AUTH-E2) | Validation | AUTH-E2, COMP-008 | Sessions active up to 7 days of inactivity; expiry prompts re-login with clear message | S | P0 |
| 164 | — | Validate user story: Sam refreshes tokens programmatically (AUTH-E2) | Validation | AUTH-E2, API-004 | Valid refresh token exchangeable for new access token; expired tokens return clear error code | S | P0 |
| 165 | — | Validate user story: Alex views profile details (AUTH-E3) | Validation | AUTH-E3, COMP-009 | Profile page shows display name, email, account creation date accurately | S | P0 |
| 166 | — | Validate user story: Alex resets forgotten password via email (AUTH-E3) | Validation | AUTH-E3, API-005, API-006 | Reset email sent within 60 seconds; link expires after 1 hour; new password invalidates all sessions | S | P0 |
| 167 | — | Validate user story: Jordan views authentication event logs (AUTH-E3) | Validation | AUTH-E3 | Logs include user ID, event type, timestamp, IP address, outcome; queryable by date range and user ID | M | P1 |
| 168 | — | Validate customer journey: First-time signup flow | Validation | COMP-007, COMP-008 | Sign Up CTA visible above fold → form fills → submit → logged in and on dashboard within 2 seconds | S | P0 |
| 169 | — | Validate customer journey: Returning user login flow | Validation | COMP-006, COMP-008 | Login form loads < 1 second; login completes < 200ms p95; silent refresh active; 7-day expiry shows clear message | S | P0 |
| 170 | — | Validate customer journey: Password reset flow | Validation | API-005, API-006 | Forgot Password → email → link (60s delivery, 1hr TTL) → new password → redirected to login | S | P0 |
| 171 | — | Validate customer journey: Profile management flow | Validation | COMP-009 | Profile page renders < 1 second; data matches registration input; timestamps accurate | S | P0 |
| 172 | — | Validate GDPR consent collection at registration | Compliance | COMP-007 | Consent mechanism present at registration; consent timestamp recorded with user record; mechanism documented | M | P0 |
| 173 | — | Validate SOC2 Type II audit logging completeness | Compliance | OPS-006, OPS-007, OPS-008, OPS-009 | All auth events logged with user ID, timestamp, IP, outcome; 12-month retention configured; queryable for auditors | M | P0 |
| 174 | — | Validate NIST SP 800-63B password storage compliance | Compliance | NFR-SEC-001 | One-way adaptive hashing confirmed; raw passwords never persisted or logged; policy documented | S | P0 |
| 175 | PLATFORM-PRD-001 | Verify alignment with platform-level product requirements | Validation | AUTH-PRD-001 | Auth service scope, interfaces, and data contracts align with platform PRD expectations; no conflicts identified | S | P1 |
| 176 | COMPLIANCE-001 | Verify SOC2 audit logging requirements fully covered | Compliance | OPS-006, OPS-007, OPS-008, OPS-009 | Audit log schema, retention policy (12 months), queryability confirmed per COMPLIANCE-001 requirements | S | P0 |
| 177 | OQ-001 | Resolve open question: API key auth for service-to-service calls | Decision | M2 | Decision documented and communicated; either deferred to v1.1 scope or design specified for implementation | S | P1 |
| 178 | OQ-002 | Resolve open question: Maximum UserProfile roles array length | Decision | DM-001 | Maximum length defined based on RBAC design review; validation constraint implemented in UserProfile schema | S | P1 |
| 179 | NG-001 | Document social/OAuth login deferral and extensibility design | Documentation | — | Non-goal documented; AuthService interface analyzed for OAuth extension without breaking changes; v1.1 scope noted | S | P2 |
| 180 | NG-002 | Document MFA deferral and extension points for v1.2 | Documentation | — | Non-goal documented; TokenManager and AuthService analyzed for MFA integration points; no blocking design debt | S | P2 |
| 181 | NG-003 | Document RBAC enforcement out-of-scope boundary | Documentation | — | roles field present in UserProfile but enforcement explicitly excluded; boundary documented for downstream teams | S | P2 |

**Phase 6 total: 33 rows | Cumulative: 181 rows**

---

## 4. Risk Assessment & Mitigation Strategies

### 4.1 Technical Risks (from TDD)

| ID | Risk | Probability | Impact | Phase Exposed | Mitigation Strategy | Contingency |
|----|------|-------------|--------|---------------|---------------------|-------------|
| R-001 | Token theft via XSS enables session hijacking | Medium | High | Phase 3 | accessToken in memory only; refreshToken in HttpOnly cookie; CSP headers; 15-min access expiry limits exposure window | Immediate token revocation via TokenManager; force password reset for affected accounts |
| R-002 | Brute-force attacks on login endpoint | High | Medium | Phase 1 | Rate limiting (10 req/min/IP); account lockout after 5 failures; bcrypt cost 12 makes offline cracking expensive | WAF IP blocking; CAPTCHA on LoginPage after 3 failures |
| R-003 | Data loss during migration from legacy auth | Low | High | Phase 5 | Parallel operation during Alpha and Beta; idempotent upsert migrations; full backup before each phase | Rollback to legacy via AUTH_NEW_LOGIN flag; restore from pre-migration backup |

### 4.2 Business Risks (from PRD)

| Risk | Probability | Impact | Phase Exposed | Mitigation |
|------|-------------|--------|---------------|------------|
| Low registration adoption due to poor UX | Medium | High | Phase 3, Phase 6 | Usability testing before launch; inline validation on RegisterPage; < 60s registration target; iterate on funnel data post-GA |
| Security breach from implementation flaws | Low | Critical | Phase 4 | Dedicated security review in Phase 4; penetration testing before production; OWASP top-10 coverage |
| Compliance failure from incomplete audit logging | Medium | High | Phase 5, Phase 6 | Audit log schema defined in Phase 1; SOC2 validation task in Phase 6; 12-month retention confirmed before GA |
| Email delivery failures blocking password reset | Low | Medium | Phase 3 | SendGrid monitoring and alerting; single retry on failure; fallback support channel documented in runbook |

### 4.3 Architectural Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Redis single point of failure for refresh tokens | Medium | High | Redis cluster configuration; fail-closed behavior (reject refresh, force re-login); Redis replication |
| JWT key compromise | Low | Critical | RS256 key in secrets manager; quarterly rotation; old keys valid during transition; revocation via TokenManager |
| PostgreSQL connection pool exhaustion under load | Medium | Medium | Pool starts at 100, scales to 200; monitoring on wait time > 50ms; HPA scales AuthService pods to reduce per-pod load |
| SendGrid dependency for password reset | Low | Medium | Email delivery monitoring; retry on transient failures; manual support channel as backup |

---

## 5. Resource Requirements & Dependencies

### 5.1 Team Resources

| Role | Allocation | Phase Coverage | Responsibilities |
|------|------------|----------------|------------------|
| Backend Engineer (2x) | Full-time | Phases 1-5 | AuthService, TokenManager, JwtService, PasswordHasher, API endpoints, database schemas |
| Frontend Engineer (1x) | Full-time | Phases 3-5 | LoginPage, RegisterPage, ProfilePage, AuthProvider |
| Security Engineer (1x) | Part-time (40%) | Phases 1, 4, 5 | Security policy review, bcrypt/JWT configuration audit, penetration testing |
| QA Engineer (1x) | Full-time | Phases 4-6 | Test automation, manual testing during Alpha/Beta, PRD acceptance validation |
| DevOps Engineer (1x) | Part-time (30%) | Phases 1, 5 | Infrastructure provisioning, Kubernetes HPA, monitoring stack, feature flags |
| Tech Lead (test-lead) | Oversight | All phases | Architecture decisions, milestone sign-offs, escalation point |

### 5.2 Infrastructure Dependencies

| Dependency | Required By | Status | Impact if Unavailable |
|------------|-------------|--------|----------------------|
| PostgreSQL 15+ | Phase 1 start | INFRA-DB-001 referenced | Blocks all data persistence; no UserProfile storage |
| Redis 7+ | Phase 2 start | Not yet provisioned | Blocks token management; no refresh token lifecycle |
| Node.js 20 LTS | Phase 1 start | Standard runtime | Blocks all backend development |
| SendGrid API access | Phase 3 start | External dependency | Blocks password reset email delivery |
| Kubernetes cluster | Phase 5 start | Assumed available | Blocks production deployment and auto-scaling |
| Secrets manager | Phase 2 start | Assumed available | Blocks RSA key storage for JwtService |

### 5.3 External Dependencies

| Dependency | Type | Owner | Required By |
|------------|------|-------|-------------|
| SEC-POLICY-001 | Policy document | Security team | Phase 1 (bcrypt and JWT configuration) |
| AUTH-PRD-001 | Product requirements | Product team | Phase 1 (requirement traceability) |
| FE-AUTH-001-TDD | Frontend accessibility spec | Frontend team | Phase 3 (LoginPage, RegisterPage accessibility) |
| COMPLIANCE-001 | SOC2 audit requirements | Compliance team | Phase 6 (audit logging validation) |
| PLATFORM-PRD-001 | Platform-level requirements | Product team | Phase 6 (scope alignment) |

---

## 6. Success Criteria & Validation Approach

### 6.1 Technical Success Criteria

| Criteria | Target | Validation Method | Phase Validated |
|----------|--------|-------------------|-----------------|
| All FRs implemented | FR-AUTH-001 through FR-AUTH-005 pass automated tests | Unit + integration test suites | Phase 4 |
| Unit test coverage | > 80% for AuthService, TokenManager, JwtService, PasswordHasher | Coverage report (Istanbul/c8) | Phase 4 |
| API response latency | < 200ms p95 across all endpoints | k6 load test at 500 concurrent users | Phase 4 |
| Concurrent capacity | 500 simultaneous logins without 5xx | k6 load test with ramp-up | Phase 4 |
| Service availability | 99.9% over 30-day rolling window | Health check monitoring | Phase 5 (post-GA) |
| Password hash security | bcrypt cost factor 12; hash time < 500ms | Unit test + benchmark | Phase 4 |
| Token signing security | RS256 with 2048-bit RSA keys | Configuration validation test | Phase 4 |

### 6.2 Business Success Criteria (from PRD)

| Criteria | Target | Validation Method | Phase Validated |
|----------|--------|-------------------|-----------------|
| Registration conversion rate | > 60% | Funnel analytics: landing → register → confirmed | Phase 6 (post-GA) |
| Login response time (p95) | < 200ms | APM instrumentation | Phase 4, ongoing |
| Average session duration | > 30 minutes | Token refresh event analytics | Phase 6 (post-GA) |
| Failed login rate | < 5% of attempts | Auth event log analysis | Phase 6 (post-GA) |
| Password reset completion | > 80% | Funnel: reset requested → new password set | Phase 6 (post-GA) |
| Daily active authenticated users | > 1000 within 30 days of GA | AuthToken issuance count | Phase 6 (post-GA) |

### 6.3 Compliance Success Criteria

| Criteria | Standard | Validation Method | Phase Validated |
|----------|----------|-------------------|-----------------|
| GDPR consent at registration | GDPR | Consent field and timestamp in UserProfile | Phase 6 |
| Audit trail for all auth events | SOC2 Type II | Audit log query with user ID, timestamp, IP, outcome | Phase 6 |
| Password storage compliance | NIST SP 800-63B | Security review confirms one-way adaptive hashing | Phase 4, Phase 6 |
| Data minimization | GDPR | Only email, hashed password, displayName collected | Phase 6 |

### 6.4 Validation Approach

1. **Continuous integration:** Unit and integration tests run on every commit; merge blocked if coverage drops below 80%
2. **Milestone gates:** Each milestone (M1-M5) has explicit exit criteria validated before proceeding to next phase
3. **Security review:** Dedicated review in Phase 4 covering PasswordHasher, JwtService, token storage, and OWASP top-10
4. **Load testing:** k6 scripts validate performance NFRs at 500 concurrent users before Alpha deployment
5. **PRD traceability:** Phase 6 systematically validates every PRD requirement, user story, and customer journey against the implemented system
6. **Compliance audit:** SOC2 and GDPR requirements validated against audit logs and data collection practices before GA

---

## 7. Timeline Estimates

### 7.1 Phase Timeline

| Phase | Start | End | Duration | Blocking Dependencies |
|-------|-------|-----|----------|----------------------|
| Phase 1: Foundation & Core Auth | 2026-04-01 | 2026-04-14 | 2 weeks | PostgreSQL provisioned; SEC-POLICY-001 reviewed |
| Phase 2: Token Management | 2026-04-15 | 2026-04-28 | 2 weeks | Phase 1 complete (M1); Redis provisioned |
| Phase 3: Password Reset & Frontend | 2026-04-29 | 2026-05-26 | 4 weeks | Phase 2 complete (M2); SendGrid access; frontend routing available |
| Phase 4: Testing & QA | 2026-05-27 | 2026-06-02 | 1 week | Phase 3 complete (M3, M4); test environments configured |
| Phase 5: Rollout & Operations | 2026-06-03 | 2026-07-07 | 1 week deploy + 4 weeks stabilization | Phase 4 complete; Kubernetes cluster; monitoring stack |
| Phase 6: PRD Traceability | 2026-05-27 | 2026-07-07 | Continuous (overlaps 4-5) | Implementation phases complete for respective validations |

### 7.2 Milestone Timeline

| Milestone | Target Date | Deliverables | Sign-off Required |
|-----------|------------|-------------|-------------------|
| M1 | 2026-04-14 | AuthService, PasswordHasher, UserProfile schema, /auth/register, /auth/login | test-lead |
| M2 | 2026-04-28 | TokenManager, JwtService, AuthToken, /auth/refresh, /auth/me | test-lead, sys-architect |
| M3 | 2026-05-12 | Password reset flow, email integration | test-lead |
| M4 | 2026-05-26 | LoginPage, RegisterPage, AuthProvider, ProfilePage | test-lead, eng-manager |
| M5 | 2026-06-09 | Phase 3 rollout complete, feature flags removed, 99.9% uptime confirmed | test-lead, eng-manager, sec-reviewer |

### 7.3 Critical Path

```
INFRA-DB-001 → DM-001 → COMP-005 → COMP-001 → FR-AUTH-001 → API-001 → M1
    → COMP-003 → COMP-002 → FR-AUTH-003 → API-004 → M2
        → FR-AUTH-005 → API-005/006 → M3
            → COMP-006/007/008 → M4
                → TEST-006 → MIG-001 → MIG-002 → MIG-003 → M5
```

The critical path runs 10 weeks from infrastructure provisioning through GA, with 4 additional weeks for stabilization monitoring. Any delay in PostgreSQL provisioning (INFRA-DB-001) or security policy review (SEC-POLICY-001) directly impacts the M1 milestone date.

### 7.4 Buffer and Risk Margin

- **Built-in buffer:** Phase 3 has 4 weeks for 2 milestones (M3 at week 2, M4 at week 4), providing internal flexibility
- **Stabilization period:** 4 weeks post-deploy allows for the 2-week Beta period plus 2 weeks of GA monitoring
- **Total project duration:** 14 weeks (April 1 → July 7) including stabilization
- **Hard deadline sensitivity:** SOC2 audit in Q3 2026 requires GA + 30 days of audit data before audit window opens
