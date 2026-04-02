---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.55
complexity_class: MEDIUM
primary_persona: architect
generated: "2026-03-31T12:00:00Z"
domains: [backend, security, frontend, testing, devops]
---

# User Authentication Service — Comprehensive Project Roadmap

## Executive Summary

The User Authentication Service is a MEDIUM-complexity backend feature enabling secure user registration, login, session persistence, profile management, and password recovery. This roadmap prioritizes the three identified risks (token theft, brute-force, migration data loss), establishes clear architectural constraints (stateless JWT, bcrypt cost 12, Redis refresh tokens), and phases implementation to deliver measurable business value by GA while maintaining operational safety.

**Key architect concerns addressed in this roadmap:**

1. **Security-first sequencing** — Token management and password hashing tested and hardened before frontend integration to avoid token leakage vectors (R-001, NFR-SEC-001, NFR-SEC-002)
2. **Explicit wiring mechanisms** — Every dispatch table, registry, and dependency injection point is named and tracked across phases to prevent "we forgot to wire X" failures
3. **Rollback-safe phasing** — Each phase introduces feature flags (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH) with clear rollback triggers and rollback procedures
4. **Compliance gates** — GDPR consent (NFR-COMP-001) and SOC2 audit logging (NFR-COMP-002) are Phase 3 blocking items, not Phase 4 afterthoughts
5. **Data migration risk** — Parallel operation with legacy auth during Phase 1-2 reduces data loss risk (R-003) by allowing safe cutover

**Timeline: 20 weeks (5 phases)**  
**Team composition:** 5 backend engineers, 2 frontend engineers, 1 QA engineer, 1 DevOps engineer, 1 security engineer (part-time)

---

## Phase 0: Foundation & Setup (Weeks -2 to 0)

**Goal:** Provision infrastructure, finalize security policies, establish development workflows. Prerequisites for Phase 1.

### Milestones

- **M0.1: Infrastructure Provisioned** — PostgreSQL 15+, Redis 7+, staging environment operational
- **M0.2: Security Policies Finalized** — SEC-POLICY-001 resolves OQ-001, OQ-002, password/token policies signed off
- **M0.3: Development Environment Ready** — CI/CD pipeline, local Docker Compose, test database automation

### Deliverables

| Deliverable | Owner | Owner | Success Criteria |
|-------------|-------|-------|------------------|
| PostgreSQL 15+ provisioning with pg-pool (100 connections) | DevOps | Week -2 | Staging DB: 99.9% uptime, <10ms latency for 100 concurrent queries |
| Redis 7+ cluster (1 GB initial capacity) for refresh tokens | DevOps | Week -2 | Staging Redis: 99.9% uptime, sub-millisecond SET/GET latency, automatic failover tested |
| Local development: Docker Compose with PostgreSQL + Redis | DevOps | Week -1 | All developers can run full stack locally in < 5 minutes without manual config |
| CI/CD pipeline (GitHub Actions or equiv.) | DevOps | Week -1 | Every commit triggers unit tests, integration tests, linting; pipeline < 10 minutes |
| SEC-POLICY-001 finalized with password/token requirements | Security | Week -1 | Policies document signed by product and security. Addresses: OQ-001 (API key auth?), OQ-002 (roles array max length?), bcrypt cost, RSA key size, token TTLs, account lockout policy (currently hardcoded to 5/15min; needs formal decision per OQ-006) |
| TDD detailed review and Q&A closure | Engineering Lead | Week 0 | All architect concerns from TDD Section 22 (Open Questions) resolved or explicitly deferred to v1.1 |

### Risk Mitigation

| Risk | Mitigation | Verification |
|------|-----------|--------------|
| Database or Redis unavailable at Phase 1 start | Provision 2 weeks early; run staging workload tests before Phase 1 | Staging health check passes daily from Week -2 onward |
| Security policies undefined or conflicting | Security review meeting with auth-team, platform-team, product; document signing | SEC-POLICY-001 version 1.0 signed and linked from this roadmap by Week 0 |
| Developer environment fragmentation | Provide Docker Compose template; enforce in make verify command | All developers report local stack working identically by Week 0 standup |

### Architecture Decisions Made

1. **PostgreSQL connection pooling:** pg-pool 100 connections per Phase 1 demand forecast; capacity plan for growth in Phase 4 (Section: Capacity Planning).
2. **Redis cluster topology:** Single-node Redis 7+ in staging; HA failover via Kubernetes StatefulSet in production. Discussed and approved by DevOps and platform-team.
3. **Password policy baseline:** NIST SP 800-63B compliant (8+ chars, no common patterns). Enforced by `PasswordHasher` in code; detailed in SEC-POLICY-001 and tested in UT-001.
4. **Token signing key management:** RSA 2048-bit keys (per NFR-SEC-002) generated and stored as Kubernetes secrets; rotation ceremony defined for Q3 2026.

---

## Phase 1: Core Authentication (Weeks 1-4)

**Goal:** Deliver registration, login, and account lockout. Foundation for token management (Phase 2) and profile/reset (Phase 3). Feature flag AUTH_NEW_LOGIN gates new code path.

### Epics Delivered

- **AUTH-E1: Login and Registration** — FR-AUTH-001, FR-AUTH-002 complete
- **Partial AUTH-E2: Token Issuance** — FR-AUTH-003 issuance only (refresh deferred to Phase 2)

### Milestones

- **M1.1: Registration Backend Complete** — FR-AUTH-002, `UserRepo.create()`, email validation, duplicate detection
- **M1.2: Login Backend Complete** — FR-AUTH-001, `PasswordHasher`, `AuthService.login()`, account lockout logic
- **M1.3: Frontend Registration & Login** — `RegisterPage`, `LoginPage`, form validation, error handling
- **M1.4: Unit Tests & Integration Tests** — 80%+ coverage on `AuthService`, `PasswordHasher`, `UserRepo`
- **M1.5: Feature Flag & Smoke Tests Passing** — AUTH_NEW_LOGIN flag controls routing; smoke tests verify both legacy and new paths work

### Requirements Coverage

| Requirement | Status | Component | Test Coverage |
|-------------|--------|-----------|----------------|
| **FR-AUTH-001** | Complete | `AuthService.login()`, `PasswordHasher.verify()`, `UserRepo.findByEmail()` | UT-001, UT-002, IT-001 |
| **FR-AUTH-002** | Complete | `AuthService.register()`, `PasswordHasher.hash()`, `UserRepo.create()` | UT-003, IT-002 |
| **NFR-PERF-001** (< 200ms p95) | Baseline | APM tracing added to `AuthService` methods | No perf test yet; baseline only |
| **NFR-PERF-002** (500 concurrent) | Deferred | Load testing deferred to Phase 4 | — |
| **NFR-SEC-001** (bcrypt cost 12) | Complete | `PasswordHasher` constructor hardcodes cost 12 | UT-004: bcrypt cost assertion |
| **NFR-COMP-001** (GDPR consent at registration) | **Deferred to Phase 3** | Will add consent checkbox to `RegisterPage` and consent_timestamp to `UserProfile` schema | See Phase 3 |
| **NFR-COMP-002** (SOC2 audit logging) | **Deferred to Phase 3** | Audit logging infrastructure deferred | See Phase 3 |

### Deliverables

#### Backend Components

| Component | Owner | Responsibility | Dependencies | Tests | Wiring Required |
|-----------|-------|-----------------|--------------|-------|-----------------|
| **`PasswordHasher`** | auth-team | Hash and verify passwords using bcryptjs cost 12 | bcryptjs library | UT-001, UT-002 | None |
| **`UserRepo`** | auth-team | CRUD on `UserProfile` table; email uniqueness enforcement | PostgreSQL, pg-pool | UT-003, IT-001, IT-002 | None |
| **`AuthService`** | auth-team | Orchestrates registration, login, account lockout logic | `PasswordHasher`, `UserRepo` | UT-001 through UT-005, IT-001 through IT-003 | **Account Lockout Registry** (see below) |
| **API Handler Layer** | auth-team | REST endpoints POST `/auth/login` and POST `/auth/register` | Express/Fastify, middleware | IT-001 through IT-004 | **Error Code Registry**, **Rate Limit Registry** |

#### Frontend Components

| Component | Owner | Responsibility | Dependencies | Tests | Wiring Required |
|-----------|-------|-----------------|--------------|-------|-----------------|
| **`LoginPage`** | frontend-team | Email/password form, POST `/auth/login`, error display | React, `AuthProvider` (stub for Phase 2) | E2E-001 (manual testing) | **Feature Flag Router** (gate rendering) |
| **`RegisterPage`** | frontend-team | Email/password/display-name form, POST `/auth/register`, validation | React, `AuthProvider` (stub for Phase 2) | E2E-002 (manual testing) | **Feature Flag Router** (gate rendering) |

#### Data Model Changes

| Change | SQL | Migration | Tests |
|--------|-----|-----------|-------|
| Create `users` table (`UserProfile`) | `CREATE TABLE users (id UUID PRIMARY KEY, email VARCHAR UNIQUE NOT NULL, display_name VARCHAR NOT NULL, password_hash VARCHAR NOT NULL, failed_login_attempts INT DEFAULT 0, locked_until TIMESTAMP, created_at TIMESTAMP DEFAULT NOW(), updated_at TIMESTAMP DEFAULT NOW(), last_login_at TIMESTAMP)` | Idempotent migration with rollback | UT-003: INSERT succeeds; UT-004: UNIQUE constraint enforced |
| Create `auth_events` table (audit log stub) | `CREATE TABLE auth_events (id UUID PRIMARY KEY, user_id UUID, event_type VARCHAR, ip_address VARCHAR, created_at TIMESTAMP)` | Idempotent; added for Phase 3 audit logging | IT-005: INSERT auth event on login attempt |

### Explicit Wiring Mechanisms (Architect's View)

**1. Account Lockout Registry**
- **Mechanism:** Hash map in `AuthService` (in-process) mapping user email → {failed_attempts: int, locked_until: Date}
- **Wired Components:** `AuthService.login()` checks registry before `PasswordHasher.verify()`; on verification failure, increments counter; at 5 attempts, sets locked_until = now + 15min
- **Owning Phase:** Phase 1 M1.2
- **Cross-References:** Phase 1 unit tests (UT-001 validates lockout on 5 failed attempts); Phase 4 rate limiting at API Gateway (separate from in-process lockout for defense-in-depth)
- **Risk:** In-process registry does not persist across service restarts → users unlocked if AuthService crashes. Mitigation: Move to Redis in Phase 2.5 (future enhancement).

**2. Error Code Registry**
- **Mechanism:** Centralized object `ErrorCodes` exporting constants (AUTH_INVALID_CREDENTIALS, AUTH_DUPLICATE_EMAIL, AUTH_WEAK_PASSWORD, etc.)
- **Wired Components:** API handlers use ErrorCodes for consistency; error response serializer converts to standard {error: {code, message, status}} JSON
- **Owning Phase:** Phase 1 M1.3
- **Cross-References:** Phase 2 adds error codes for token endpoints; Phase 3 adds password reset error codes
- **Artifact:** `src/superclaude/auth/ErrorCodes.ts` (TypeScript) or `src/superclaude/auth/error_codes.py` (Python)

**3. Rate Limit Registry**
- **Mechanism:** Centralized config (Redis-backed or in-memory) defining per-endpoint rate limits (10 req/min login, 5 req/min register, etc.)
- **Wired Components:** API Gateway middleware checks registry before forwarding request; rejects with 429 if exceeded
- **Owning Phase:** Phase 1 M1.5 (gate and verify; actual enforcement may be at API Gateway, not in-app)
- **Cross-References:** Phase 4 hardening sets up API Gateway rate limiting
- **Artifact:** `src/superclaude/auth/RateLimits.ts` or configuration file

### Implementation Tasks

| Task | Owner | Sprint | Estimate | Blocking | Tests |
|------|-------|--------|----------|----------|-------|
| Design `UserProfile` schema and PostgreSQL migration | auth-team | W1 | 4h | M1.2 | N/A (design review) |
| Implement `PasswordHasher` (bcryptjs wrapper) | auth-team | W1 | 6h | M1.1 | UT-001, UT-002, UT-004 |
| Implement `UserRepo` (CRUD, email uniqueness) | auth-team | W1-W2 | 8h | M1.2 | UT-003, IT-001, IT-002 |
| Implement `AuthService.register()` | auth-team | W2 | 8h | M1.2 | UT-005, IT-002 |
| Implement `AuthService.login()` with account lockout | auth-team | W2 | 12h | M1.3 | UT-001, UT-006 (lockout behavior) |
| Implement POST `/auth/login` and POST `/auth/register` endpoints | auth-team | W2-W3 | 10h | M1.3 | IT-003, IT-004 |
| Wire **Account Lockout Registry** | auth-team | W2 | 3h | M1.2 | UT-006 |
| Wire **Error Code Registry** | auth-team | W3 | 4h | M1.3 | IT-003 consistency checks |
| Implement `RegisterPage` (React form, validation) | frontend-team | W2-W3 | 10h | M1.4 | Manual smoke test |
| Implement `LoginPage` (React form, validation, error display) | frontend-team | W2-W3 | 10h | M1.4 | Manual smoke test |
| Wire **Feature Flag Router** for `AUTH_NEW_LOGIN` | frontend-team | W3 | 6h | M1.5 | E2E smoke test: both legacy and new paths work |
| Add APM/tracing to `AuthService` methods | DevOps | W3 | 5h | M1.4 | APM dashboard shows metrics |
| Write integration tests (testcontainers PostgreSQL) | QA | W3-W4 | 12h | M1.4 | IT-001 through IT-004 passing |
| Write end-to-end smoke tests (`LoginPage` → `AuthService` → database) | QA | W4 | 8h | M1.5 | E2E-001, E2E-002 passing (manual) |

### Phase 1 Success Criteria

| Criterion | Measurement | Target | Owner |
|-----------|-------------|--------|-------|
| **C1.1: Unit test coverage** | `nyc` or `pytest --cov` on `AuthService`, `PasswordHasher`, `UserRepo` | ≥ 80% | QA |
| **C1.2: Integration tests passing** | All IT-001 through IT-004 pass on CI | 4/4 passing | QA |
| **C1.3: Feature flag gates correctly** | AUTH_NEW_LOGIN flag controls routing; disabling it routes to legacy auth | Verified manually by auth-team | auth-team |
| **C1.4: Password hashing works** | bcrypt cost 12 enforced; UT-004 passes | cost assertion passes | auth-team |
| **C1.5: No production data exposure** | Zero logs of passwords or plaintext credentials | Verified via log scan and code review | Security |
| **C1.6: Account lockout functional** | After 5 failed login attempts, account locked for 15 min; UT-006 passes | UT-006 passing | auth-team |

### Phase 1 Risk Mitigation

| Risk | Probability | Impact | Mitigation | Trigger |
|------|-------------|--------|-----------|---------|
| **Password hash takes > 500ms** (bcrypt cost 12) | Low | Medium | Baseline cost 12 in local testing; Phase 4 perf test will validate; if > 500ms, reduce cost to 10 (lose some security) | Perf test results in Phase 4 |
| **PostgreSQL connection pooling exhausted during testing** | Medium | Medium | pg-pool default 100; monitor active connections; add test isolation (transactions with rollback) | CI pipeline shows > 80 concurrent connections |
| **Feature flag not evaluated correctly by frontend** | Low | High | Comprehensive manual smoke test before M1.5; frontend eng reviews flag evaluation logic | Feature flag returns wrong value in any scenario |

---

## Phase 2: Token Management & Silent Refresh (Weeks 5-8)

**Goal:** Deliver stateless JWT token issuance (FR-AUTH-003), refresh token persistence in Redis, silent token refresh via `AuthProvider`. Enable Phase 3 without re-authentication.

### Epics Delivered

- **Remaining AUTH-E2: Token Refresh & Persistence** — FR-AUTH-003 complete (both issuance and refresh)

### Milestones

- **M2.1: JwtService Complete** — Token signing with RS256 and 2048-bit RSA keys; verification with 5-second clock skew
- **M2.2: TokenManager Complete** — Token pair generation, refresh token storage in Redis with 7-day TTL, revocation
- **M2.3: AuthProvider Integration** — Silent token refresh on page load and background polling; token stored in memory only (not localStorage) per R-001 mitigation
- **M2.4: Token Refresh Endpoint** — POST `/auth/refresh` wired; returns new `AuthToken` pair
- **M2.5: E2E Token Flow Tests** — Full flow: login → get tokens → refresh → new tokens; tokens persist across page navigation

### Requirements Coverage

| Requirement | Status | Component | Test Coverage |
|-------------|--------|-----------|----------------|
| **FR-AUTH-003** (JWT issuance and refresh) | Complete | `JwtService`, `TokenManager`, POST `/auth/refresh` | UT-007, UT-008, IT-005, IT-006, E2E-003 |
| **NFR-PERF-001** (< 200ms p95) | Extended | APM tracing on `TokenManager.refresh()` added | Baseline + refresh latency metrics |
| **NFR-PERF-002** (500 concurrent) | In Progress | Load testing begins Phase 4; Phase 2 does local concurrency checks | Local k6 script with 50 concurrent users |
| **NFR-SEC-002** (RS256 token signing) | Complete | `JwtService` hardcodes RS256; RSA key format validated | UT-009: RSA key format assertion |
| **NFR-REL-001** (99.9% uptime) | Baseline | Redis failover and restart behavior tested | Manual Redis restart → TokenManager recovers |

### Deliverables

#### Backend Components

| Component | Owner | Responsibility | Dependencies | Tests | Wiring Required |
|-----------|-------|-----------------|--------------|-------|-----------------|
| **`JwtService`** | auth-team | Issue and verify JWT access tokens using RS256 and 2048-bit RSA keys; enforce 5-second clock skew tolerance | jsonwebtoken library, RSA keys (from Kubernetes secrets) | UT-007, UT-008, UT-009 | **Token Signing Key Registry** |
| **`TokenManager`** | auth-team | Generate refresh tokens; store in Redis with 7-day TTL; issue token pairs; revoke tokens | Redis client, `JwtService` | UT-008, IT-005, IT-006 | **Token Storage Registry** (Redis connection pool) |
| **POST `/auth/refresh` Endpoint** | auth-team | Accept refresh token; call `TokenManager.refresh()`; return new `AuthToken` pair | `TokenManager` | IT-006 | **Error Code Registry** (extend with token-specific codes) |

#### Frontend Components

| Component | Owner | Responsibility | Dependencies | Tests | Wiring Required |
|-----------|-------|-----------------|--------------|-------|-----------------|
| **`AuthProvider`** | frontend-team | Context provider that manages token lifecycle: stores accessToken in memory, refreshToken in httpOnly cookie (or state), periodically calls POST `/auth/refresh` to refresh tokens silently | React Context, POST `/auth/refresh` endpoint, `AuthService` (API client stub) | E2E-003: token refresh flow end-to-end | **Token Refresh Polling Registry** |

#### Data Model Changes

None. JWT tokens are stateless; no database changes. Redis schema is implicit (refresh token → {userId, issuedAt, expiresAt}).

### Explicit Wiring Mechanisms

**1. Token Signing Key Registry**
- **Mechanism:** Kubernetes Secret mount or environment variables containing RSA private key (for signing) and public key (for verification). `JwtService` reads keys on startup.
- **Wired Components:** `JwtService.sign()` uses private key; token verifiers use public key. Separate keys for development vs. production.
- **Owning Phase:** Phase 2 M2.1
- **Cross-References:** Phase 4 key rotation ceremony; Phase 0 DevOps provisioning
- **Artifact:** `src/superclaude/auth/KeyManager.ts` — singleton managing key loading and caching
- **Risk:** Private key leak allows forging tokens. Mitigation: Keys only in Kubernetes secrets, not in code repo; rotation every 90 days (Q3 2026 ceremony).

**2. Token Storage Registry**
- **Mechanism:** Centralized Redis client config (host, port, auth, TLS) and connection pool (10 connections) abstracted in `RedisClient` singleton.
- **Wired Components:** `TokenManager.storeRefreshToken()` uses `RedisClient.set()`; `TokenManager.validateRefreshToken()` uses `RedisClient.get()`; revocation uses `RedisClient.del()`.
- **Owning Phase:** Phase 2 M2.2
- **Cross-References:** Phase 0 Redis provisioning; Phase 4 monitoring Redis connection pool health
- **Artifact:** `src/superclaude/redis/RedisClient.ts` (TypeScript) or similar
- **Risk:** Redis unavailability prevents refresh → users must re-login. Mitigation: Automatic fallback to password re-entry; runbook for Redis recovery.

**3. Token Refresh Polling Registry**
- **Mechanism:** `AuthProvider` initiates refresh polls using setInterval (configurable interval, default 10 minutes) to keep accessToken fresh. Polls triggered when accessToken is within 5 minutes of expiry.
- **Wired Components:** `AuthProvider.useEffect()` sets up interval; calls POST `/auth/refresh` via `AuthService.refreshToken()` API client.
- **Owning Phase:** Phase 2 M2.3
- **Cross-References:** Phase 3 extends to handle logout (clear interval); Phase 4 observability adds metrics for refresh success/failure
- **Artifact:** Token refresh logic in `AuthProvider` component or custom hook
- **Risk:** Polling intervals not coordinated → thundering herd of simultaneous refresh requests. Mitigation: Stagger refresh requests per user based on token expiry times (deterministic, not random).

### Implementation Tasks

| Task | Owner | Sprint | Estimate | Blocking | Tests |
|------|-------|--------|----------|----------|-------|
| Generate RSA key pair (2048-bit) for signing | DevOps | W5 | 2h | M2.1 | Manual verification of key format |
| Design JWT token payload schema (include user id, roles, iat, exp, 5-sec skew) | auth-team | W5 | 4h | M2.1 | Design review with security |
| Implement `JwtService` (sign, verify, clock skew) | auth-team | W5 | 10h | M2.1 | UT-007, UT-008, UT-009 |
| Wire **Token Signing Key Registry** | auth-team | W5 | 6h | M2.1 | UT-009: key format assertion |
| Implement `TokenManager` (issue pair, store refresh, revoke, validate) | auth-team | W5-W6 | 12h | M2.2 | UT-008, IT-005, IT-006 |
| Wire **Token Storage Registry** (Redis connection pool, RedisClient singleton) | auth-team | W5 | 8h | M2.2 | IT-005: Redis SET/GET behavior |
| Implement POST `/auth/refresh` endpoint | auth-team | W6 | 8h | M2.4 | IT-006 |
| Implement `AuthProvider` with silent token refresh | frontend-team | W6-W7 | 12h | M2.3 | E2E-003 (manual testing) |
| Wire **Token Refresh Polling Registry** (setInterval, refresh logic) | frontend-team | W7 | 6h | M2.3 | E2E-003: verify tokens refresh without user action |
| Test token refresh under load (k6 script, 50 concurrent users) | QA | W7 | 8h | M2.5 | Load test results: < 200ms p95 refresh latency |
| Add APM tracing to `TokenManager.refresh()` | DevOps | W7 | 5h | M2.5 | APM dashboard shows refresh latency |
| Write E2E test: login → get tokens → refresh → tokens persist across page nav | QA | W7-W8 | 10h | M2.5 | E2E-003 passing |

### Phase 2 Success Criteria

| Criterion | Measurement | Target | Owner |
|-----------|-------------|--------|-------|
| **C2.1: Token issuance works** | POST `/auth/login` returns valid JWT with correct payload (user id, roles, exp = now + 15min) | IT-005 passing | auth-team |
| **C2.2: Token refresh works** | POST `/auth/refresh` with valid refresh token returns new pair; old refresh token revoked | IT-006 passing | auth-team |
| **C2.3: Expired refresh token rejected** | POST `/auth/refresh` with Redis-expired token returns 401 | IT-006 negative test passing | auth-team |
| **C2.4: Silent refresh functional** | `AuthProvider` polls and refreshes tokens without prompting user; tokens persist across page navigation | E2E-003 manual pass | frontend-team |
| **C2.5: RSA key format validated** | `JwtService` asserts RSA 2048-bit key format on startup | UT-009 passing | auth-team |
| **C2.6: Clock skew tolerated** | Token with iat = now + 3sec still validates (5-sec tolerance) | UT-007 passing | auth-team |
| **C2.7: Load test baseline** | 50 concurrent token refreshes complete in < 200ms p95 | k6 script results | QA |

### Phase 2 Risk Mitigation

| Risk | Probability | Impact | Mitigation | Trigger |
|------|-------------|--------|-----------|---------|
| **Token theft via XSS** (R-001) | High | Critical | AccessToken stored in memory only (not localStorage); refreshToken in httpOnly cookie; `AuthProvider` clears tokens on tab close | Security review + XSS test in Phase 4 |
| **Redis unavailability causes cascade** | Low | High | Fallback to password re-entry when refresh fails; runbook documents recovery; Phase 3 adds monitoring and alerting | Redis connection failures in logs |
| **JWT clock skew issues in distributed system** | Medium | Medium | 5-second tolerance per architectural constraint; Phase 4 monitoring watches for excessive skew rejections | Skew rejection rate > 0.1% in APM metrics |

---

## Phase 3: User Profile, Password Reset & Compliance (Weeks 9-12)

**Goal:** Deliver profile retrieval (FR-AUTH-004), password reset (FR-AUTH-005), compliance logging (NFR-COMP-001, NFR-COMP-002), and admin audit log access. Full feature parity with PRD.

### Epics Delivered

- **AUTH-E3: Profile and Password Reset** — FR-AUTH-004, FR-AUTH-005 complete
- **AUTH-E4: Compliance & Audit Logging** — NFR-COMP-001, NFR-COMP-002, NFR-COMP-003 complete

### Milestones

- **M3.1: User Profile Retrieval** — GET `/auth/me` endpoint, ProfilePage frontend
- **M3.2: Password Reset Flow** — `AuthService.resetPasswordRequest()`, `AuthService.resetPasswordConfirm()`, POST `/auth/reset-request`, POST `/auth/reset-confirm` endpoints
- **M3.3: SendGrid Integration** — Email delivery for password reset links (1-hour TTL tokens)
- **M3.4: Audit Logging Infrastructure** — Audit event recording for all auth actions (login, registration, refresh, password reset); PostgreSQL `auth_events` table; 90-day (TDD) or 12-month (PRD — **OQ-EXT-001**) retention policy resolved
- **M3.5: Admin Log Query API** — Endpoint or dashboard for Jordan (admin persona) to query audit logs by user and date range
- **M3.6: GDPR Consent Recording** — Consent checkbox added to `RegisterPage`; `UserProfile.consent_timestamp` field added; Phase 3 gates registration on consent acceptance

### Requirements Coverage

| Requirement | Status | Component | Test Coverage |
|-------------|--------|-----------|----------------|
| **FR-AUTH-004** (user profile retrieval) | Complete | GET `/auth/me`, `AuthService.getProfile()`, ProfilePage | UT-010, IT-007, E2E-004 |
| **FR-AUTH-005** (password reset) | Complete | `AuthService.resetPasswordRequest()`, `AuthService.resetPasswordConfirm()`, SendGrid integration | UT-011, UT-012, IT-008, IT-009, E2E-005 |
| **NFR-COMP-001** (GDPR consent) | Complete | Consent timestamp recorded in `UserProfile.consent_timestamp`; checkbox in `RegisterPage` | UT-013, IT-010 |
| **NFR-COMP-002** (SOC2 audit logging) | Complete | Audit events logged to `auth_events` table; 90-day retention (TDD) vs. 12-month (PRD) — **must resolve OQ-EXT-001** | IT-011, IT-012 |
| **NFR-COMP-003** (GDPR data minimization) | Complete | `UserProfile` schema contains only email, hashed password, display name (no extra PII) | UT-014: schema validation |

### Deliverables

#### Backend Components

| Component | Owner | Responsibility | Dependencies | Tests | Wiring Required |
|-----------|-------|-----------------|--------------|-------|-----------------|
| **`AuthService.getProfile()`** | auth-team | Return authenticated user's `UserProfile` | `UserRepo`, JWT verification | UT-010, IT-007 | None |
| **GET `/auth/me` Endpoint** | auth-team | Protected endpoint requiring Bearer token; calls `AuthService.getProfile()` | `AuthService`, middleware for token validation | IT-007 | **Auth Middleware Registry** (extend from Phase 1) |
| **`AuthService.resetPasswordRequest()`** | auth-team | Generate 1-hour TTL reset token; send email via SendGrid | `PasswordHasher`, SendGrid API, `UserRepo` | UT-011, IT-008 | **Reset Token Registry** |
| **`AuthService.resetPasswordConfirm()`** | auth-team | Validate reset token; update password hash; invalidate all tokens for user | `PasswordHasher`, `TokenManager`, `UserRepo` | UT-012, IT-009 | **Reset Token Registry** |
| **POST `/auth/reset-request` Endpoint** | auth-team | Unprotected endpoint; accepts email; calls `AuthService.resetPasswordRequest()` | `AuthService` | IT-008 | **Error Code Registry** |
| **POST `/auth/reset-confirm` Endpoint** | auth-team | Unprotected endpoint; accepts reset token and new password; calls `AuthService.resetPasswordConfirm()` | `AuthService` | IT-009 | **Error Code Registry** |
| **Audit Logger** | auth-team | Singleton that records auth events to `auth_events` table and/or structured logging | PostgreSQL, logging framework | IT-011, IT-012 | **Audit Event Registry** |
| **Admin Audit Log Query API** | auth-team | Endpoint(s) for Jordan (admin persona) to query `auth_events` by user_id and date range. Pagination. | `auth_events` table, authentication, authorization checks | IT-013 | **Admin Authorization Middleware** |

#### Frontend Components

| Component | Owner | Responsibility | Dependencies | Tests | Wiring Required |
|-----------|-------|-----------------|--------------|-------|-----------------|
| **ProfilePage** | frontend-team | Display authenticated user's profile (name, email, creation date, last login). GET `/auth/me`. | React, GET `/auth/me` endpoint | E2E-004 | **Protected Route Guard** |
| **`RegisterPage` (updated)** | frontend-team | Add GDPR consent checkbox before submit; POST `/auth/register` must include consent flag | React, POST `/auth/register` | E2E-006: consent checkbox blocks submit until checked | **Consent Recording** (backend acceptance) |
| **Password Reset Flow** (new) | frontend-team | Two-step flow: request form (email input) + confirmation form (new password input). Links opened from email. | React, POST `/auth/reset-request`, POST `/auth/reset-confirm` | E2E-005: full reset flow | None |

#### Data Model Changes

| Change | SQL | Migration | Tests |
|--------|-----|-----------|-------|
| Add `consent_timestamp` to `users` table | `ALTER TABLE users ADD COLUMN consent_timestamp TIMESTAMP;` | Idempotent migration; backfill existing users with NULL | UT-013: consent field present on new registrations |
| Create `auth_events` table | `CREATE TABLE auth_events (id UUID PRIMARY KEY, user_id UUID, event_type VARCHAR, ip_address VARCHAR, created_at TIMESTAMP);` | Idempotent; supports indexing on user_id, created_at | IT-011: event logged on each auth action |
| Add index on `auth_events.user_id, created_at` for query performance | `CREATE INDEX idx_auth_events_user_created ON auth_events(user_id, created_at);` | Idempotent | IT-013: query performance < 100ms for 90-day range |

### Explicit Wiring Mechanisms

**1. Reset Token Registry**
- **Mechanism:** In-process cache (or Redis, for distributed deployments) mapping reset token hash → {userId, createdAt, expiresAt}. Tokens single-use: record consumed_at timestamp to prevent reuse.
- **Wired Components:** `AuthService.resetPasswordRequest()` generates token and stores in registry; `AuthService.resetPasswordConfirm()` validates token (checks existence, expiry, prior consumption), marks consumed, and invalidates.
- **Owning Phase:** Phase 3 M3.2
- **Cross-References:** Phase 2 `TokenManager` uses similar pattern for refresh tokens
- **Artifact:** `src/superclaude/auth/ResetTokenManager.ts`
- **Risk:** If stored in-process, tokens lost on restart. Mitigation: Move to Redis (like refresh tokens) or add durability to in-process cache.

**2. Audit Event Registry**
- **Mechanism:** Centralized `AuditLogger` singleton that serializes auth events (event_type, user_id, ip_address, timestamp, outcome) and writes to `auth_events` table and/or structured logging sink (e.g., ELK, Datadog).
- **Wired Components:** Every auth endpoint (`login`, `register`, `refresh`, `reset-confirm`) calls `AuditLogger.record({...})`. `AuditLogger` writes to PostgreSQL asynchronously (non-blocking).
- **Owning Phase:** Phase 3 M3.4
- **Cross-References:** Phase 4 monitoring and alerting consume audit logs; Phase 3.5 admin query API reads audit logs
- **Artifact:** `src/superclaude/auth/AuditLogger.ts`
- **Risk:** Audit logging overhead may impact latency. Mitigation: Async writes; batch inserts; separate database connection pool for audit writes.

**3. Admin Authorization Middleware**
- **Mechanism:** Middleware that checks JWT token's `roles` claim for "admin" privilege before allowing access to sensitive endpoints (admin log query API).
- **Wired Components:** Applied to GET `/auth/admin/logs` endpoint. Verifies `roles.includes('admin')` in JWT payload.
- **Owning Phase:** Phase 3 M3.5
- **Cross-References:** Phase 1 `JwtService` encodes roles in token payload; Phase 2 `TokenManager` issues tokens with roles
- **Artifact:** `src/superclaude/auth/AdminAuthMiddleware.ts`
- **Risk:** Role-based access control is coarse; future phases may need fine-grained permissions. Mitigation: Extensible middleware that checks dynamic ACL (not just hardcoded role check).

**4. Consent Recording Mechanism**
- **Mechanism:** `RegisterPage` checkbox for GDPR consent. If unchecked, form submit disabled. Upon registration success, `UserProfile.consent_timestamp` set to current time.
- **Wired Components:** POST `/auth/register` handler validates request.body.consentGiven === true; rejects with 400 if false. `AuthService.register()` records consent_timestamp in `UserProfile`.
- **Owning Phase:** Phase 3 M3.6
- **Cross-References:** Phase 3 audit logging records consent acceptance as audit event for compliance
- **Artifact:** `RegisterPage` component, `AuthService.register()` logic
- **Risk:** Consent timestamp only recorded at registration; if user revokes later, no timestamp update. Mitigation: Add consent management page in Phase 4 (v1.1 feature).

### Implementation Tasks

| Task | Owner | Sprint | Estimate | Blocking | Tests |
|------|-------|--------|----------|----------|-------|
| Design password reset token schema and reset flow | auth-team | W9 | 4h | M3.2 | Design review |
| Implement `AuthService.resetPasswordRequest()` with SendGrid integration | auth-team | W9 | 10h | M3.2 | UT-011, IT-008 |
| Implement `AuthService.resetPasswordConfirm()` | auth-team | W9-W10 | 8h | M3.2 | UT-012, IT-009 |
| Wire **Reset Token Registry** | auth-team | W9 | 6h | M3.2 | UT-011, UT-012 |
| Implement POST `/auth/reset-request` and POST `/auth/reset-confirm` endpoints | auth-team | W10 | 8h | M3.2 | IT-008, IT-009 |
| Resolve **OQ-EXT-001**: Audit log retention (90 days vs. 12 months)? | product-team + security | W9 | 2h | M3.4 | Decision documented and linked |
| Implement `AuditLogger` singleton | auth-team | W10 | 8h | M3.4 | IT-011, IT-012 |
| Wire **Audit Event Registry** into all endpoints (login, register, refresh, reset) | auth-team | W10 | 10h | M3.4 | IT-011, IT-012: every endpoint calls AuditLogger |
| Implement GET `/auth/me` endpoint | auth-team | W10 | 6h | M3.1 | IT-007 |
| Implement `AuthService.getProfile()` | auth-team | W9 | 4h | M3.1 | UT-010 |
| Wire **Admin Authorization Middleware** | auth-team | W11 | 6h | M3.5 | IT-014: admin can access log query; non-admin cannot |
| Implement admin audit log query API (GET `/auth/admin/logs`) with pagination | auth-team | W11 | 12h | M3.5 | IT-13: query by user_id + date range returns filtered results |
| Add `consent_timestamp` to `UserProfile` schema and migration | auth-team | W10 | 4h | M3.6 | IT-010: migration runs cleanly |
| Implement GDPR consent checkbox in `RegisterPage` | frontend-team | W10-W11 | 6h | M3.6 | E2E-006: checkbox required to submit |
| Implement ProfilePage with GET `/auth/me` call | frontend-team | W10 | 8h | M3.1 | E2E-004: profile displays correct user data |
| Implement password reset flow (request + confirm forms) in frontend | frontend-team | W11-W12 | 12h | M3.2 | E2E-005: full reset flow works end-to-end |
| Write integration tests for reset token lifecycle | QA | W11 | 10h | M3.2 | IT-008, IT-009 passing |
| Write integration tests for audit logging (event recorded on each action) | QA | W11-W12 | 10h | M3.4 | IT-011, IT-012 passing |
| Write E2E test: password reset flow (request + email + confirm) | QA | W12 | 10h | M3.2 | E2E-005 passing |

### Phase 3 Success Criteria

| Criterion | Measurement | Target | Owner |
|-----------|-------------|--------|-------|
| **C3.1: Profile retrieval works** | GET `/auth/me` returns authenticated user's `UserProfile` with correct data (id, email, displayName, timestamps) | IT-007 passing | auth-team |
| **C3.2: Password reset flow works** | Request email sent; reset link in email is valid; confirm endpoint updates password and invalidates other sessions | IT-008, IT-009 passing | auth-team |
| **C3.3: Audit events logged** | Every login, registration, token refresh, and password reset creates a row in `auth_events` table | IT-011, IT-012 passing | auth-team |
| **C3.4: Admin can query logs** | GET `/auth/admin/logs?user_id=X&from=Y&to=Z` returns filtered audit events; non-admin request rejected | IT-13, IT-14 passing | auth-team |
| **C3.5: GDPR consent recorded** | `UserProfile.consent_timestamp` populated on registration; empty for pre-existing users | UT-013, IT-010 passing | auth-team |
| **C3.6: Data minimization enforced** | Code review confirms `UserProfile` contains only email, password hash, display name, timestamps, roles, consent_timestamp | Security code review | Security |
| **C3.7: Audit retention policy finalized** | **OQ-EXT-001** resolved: decision on 90 days (TDD) vs. 12 months (PRD) documented and linked | Policy document signed | product-team |

### Phase 3 Risk Mitigation

| Risk | Probability | Impact | Mitigation | Trigger |
|------|-------------|--------|-----------|---------|
| **Password reset token reuse** | Medium | High | Token marked consumed after first use; code review confirms check-then-use pattern | Code review finds reuse vulnerability |
| **Audit log performance degradation** | Medium | Medium | Async audit writes; separate connection pool; indexes on (user_id, created_at); monitor INSERT latency | Audit INSERT latency > 100ms |
| **Audit log table grows to terabytes** | Low | Medium | Retention policy enforced via cron job; archive/delete old events per retention_days config | Audit table size > 100GB |
| **Password reset email spoofing** | Low | High | Validate reset links are valid before accepting new password; log reset attempts for anomaly detection | Anomaly detection in Phase 4 |

---

## Phase 4: Integration, Hardening & API Versioning (Weeks 13-16)

**Goal:** Harden all components against identified risks (R-001, R-002, R-003), validate compliance, implement API versioning, set up feature flags, configure rate limiting, establish SLOs and observability.

### Epics Delivered

- **AUTH-E5: Operational Readiness** — Monitoring, runbooks, SLO dashboards, on-call procedures
- **AUTH-E6: Security Hardening** — Penetration testing, XSS prevention, brute-force mitigation, rollback procedures
- **AUTH-E7: API Versioning & Rate Limiting** — `/v1/auth/*` endpoints, feature flag infrastructure, request throttling

### Milestones

- **M4.1: Security Testing Complete** — Penetration test results, XSS prevention validated, account lockout stress-tested
- **M4.2: Feature Flag Infrastructure** — AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH flags fully wired; rollback procedures tested
- **M4.3: API Versioning & Rate Limiting** — All endpoints versioned under `/v1/auth/*`; API Gateway rate limiting configured and tested
- **M4.4: Observability & SLOs** — Prometheus metrics, Grafana dashboards, alert rules, SLO targets defined
- **M4.5: Runbook Coverage** — Operational runbooks for all identified failure scenarios; on-call playbooks tested
- **M4.6: Performance Validated** — Load testing confirms p95 < 200ms, 500 concurrent users; Redis and PostgreSQL capacity verified

### Requirements Coverage

| Requirement | Status | Component | Test Coverage |
|-------------|--------|-----------|----------------|
| **NFR-PERF-001** (< 200ms p95) | Validated | Full load test with k6 (500 concurrent users) | k6 test results, APM dashboards |
| **NFR-PERF-002** (500 concurrent) | Validated | Load test sustained for 30 minutes | k6 results, CPU/memory under 70% |
| **NFR-REL-001** (99.9% uptime) | Operationalized | SLO dashboards, alert rules, runbooks | Runbook testing, chaos engineering (optional) |
| **NFR-SEC-001** (bcrypt cost 12) | Reinforced | Code audit confirms cost 12 enforced; no bypass paths | Code review, UT-004 |
| **NFR-SEC-002** (RS256 signing) | Reinforced | Code audit confirms RS256 only; no fallback to HS256 | Code review, UT-009 |
| **All requirements** | Ready for GA | Feature flag gates ensure rollback capability | Rollback testing for each flag |

### Deliverables

#### Infrastructure & DevOps

| Deliverable | Owner | Responsibility | Tests |
|-------------|-------|-----------------|-------|
| **API Gateway Rate Limiting Config** | DevOps | Configure rate limits per endpoint (10 req/min login, 5 req/min register, etc.). Implement at API Gateway, not in-app. | Manual: curl with excess requests returns 429 |
| **Feature Flag Infrastructure** | DevOps | Set up feature flag service (e.g., LaunchDarkly, custom Redis-backed flags) and wire into routing layer | Feature flag toggle test: AUTH_NEW_LOGIN ON/OFF correctly routes traffic |
| **Prometheus Metrics Collection** | DevOps | Scrape metrics from `AuthService` (counters, histograms, gauges) and expose on `/metrics` endpoint | Metrics endpoint returns valid Prometheus format |
| **Grafana Dashboards** | DevOps | Build dashboards for login latency, error rates, token refresh latency, Redis operations, PostgreSQL connections | Dashboard loads; panels display real data from staging |
| **Alert Rules (Prometheus AlertManager)** | DevOps | Define alerts for: login error rate > 20%, p95 latency > 500ms, Redis connection failures, PostgreSQL connection pool exhaustion | Alert fires when condition triggered in staging |
| **Kubernetes Deployment Manifests** | DevOps | Stateless `AuthService` deployments with HPA (CPU target 70%), liveness/readiness probes, resource requests/limits | Pods auto-scale on high CPU; liveness probes work |
| **Secrets Management** | DevOps | Store RSA signing keys, SendGrid API key, database credentials in Kubernetes secrets; rotation ceremony documented | Secrets mounted correctly; no secrets in logs |

#### Security & Testing

| Deliverable | Owner | Responsibility | Tests |
|-------------|-------|-----------------|-------|
| **Penetration Test Report** | Security | Third-party security firm (or internal red team) tests for XSS, CSRF, injection, token theft, brute-force, data leakage | Report signed off; all P0/P1 findings resolved |
| **XSS Prevention Code Review** | Security | Verify token storage (memory only, not localStorage), httpOnly cookie usage, input sanitization in `LoginPage`/`RegisterPage` | Code review checklist signed |
| **Brute-Force Stress Test** | Security | Simulate 1000 login attempts per second for 10 minutes; verify account lockout, rate limiting, and no downtime | Test results show lockout triggered; no DoS |
| **Load Test (k6)** | QA | 500 concurrent users, all auth endpoints, 30-minute duration | p95 latency < 200ms, error rate < 0.1%, Redis/PostgreSQL healthy |
| **Chaos Engineering (optional)** | QA | Kill Redis pod; kill PostgreSQL pod; test fallback behavior and recovery time | Service degrades gracefully; recovery < 5 minutes |

#### Operational Runbooks

| Runbook | Owner | Content | Testing |
|---------|-------|---------|---------|
| **AuthService Down** | auth-team | Diagnosis steps, recovery steps, escalation path, post-mortem template | Simulated outage; team follows runbook and recovers in < 15 min |
| **Token Refresh Failures** | auth-team | Redis health check, `JwtService` key validation, feature flag state, rollback to password re-entry | Simulated Redis failure; team executes runbook |
| **Database Connection Pool Exhaustion** | auth-team | Monitor active connections, identify slow queries, scale pool or restart service | Simulated pool exhaustion; mitigation successful |
| **Password Reset Email Delivery Failure** | auth-team | SendGrid health check, manual email override, alert to support team | Simulated SendGrid outage; fallback email sent |
| **Rollback Procedure (Feature Flag Disabled)** | auth-team | Step-by-step: disable AUTH_NEW_LOGIN, verify legacy path works, smoke tests, post-mortem | Rollback executed in < 10 min; no data loss |

#### Observability & Monitoring

| Artifact | Owner | Responsibility |
|----------|-------|-----------------|
| **SLO Dashboard** | DevOps | Real-time display of p95 latency, error rate, uptime vs. SLO targets (99.9% uptime, < 200ms p95, < 0.1% error rate) |
| **Alert Rules** | DevOps | Pages on-call for: error rate > 5%, p95 latency > 500ms, Redis connection failures, data corruption detected |
| **Tracing (OpenTelemetry)** | DevOps | Full request traces from API Gateway → AuthService → PasswordHasher → UserRepo → PostgreSQL, with latency breakdown per component |
| **Audit Log Dashboard** | DevOps | Real-time view of auth events, failed login attempts, account lockouts, password resets for triage and compliance |

### Implementation Tasks

| Task | Owner | Sprint | Estimate | Blocking | Tests |
|------|-------|--------|----------|----------|-------|
| Configure API Gateway rate limiting | DevOps | W13 | 6h | M4.3 | Manual 429 response test |
| Set up feature flag service (LaunchDarkly or custom) and wire into routing | DevOps | W13 | 12h | M4.2 | Feature flag toggle test |
| Build Prometheus metrics collection from `AuthService` | DevOps | W13 | 10h | M4.4 | `/metrics` endpoint returns valid Prometheus format |
| Build Grafana dashboards (latency, errors, redis, postgres) | DevOps | W13-W14 | 12h | M4.4 | Dashboards load with real data from staging |
| Define Prometheus alert rules and test in staging | DevOps | W14 | 8h | M4.4 | Alerts fire when condition triggered |
| Write API versioning middleware (`/v1/auth/*` prefix) | auth-team | W13 | 6h | M4.3 | Endpoints accessible under `/v1/auth/*` only |
| Migrate all endpoints to `/v1/auth/` prefix | auth-team | W13 | 4h | M4.3 | All endpoint tests updated to use `/v1/auth/*` |
| Implement external rollback test for feature flags | QA | W14 | 8h | M4.2 | Feature flag toggled; traffic routes correctly; no data loss |
| Run penetration test (third-party or internal) | Security | W13-W14 | 20h | M4.1 | Penetration test report completed; P0/P1 findings resolved |
| Run brute-force stress test (1000 req/sec, 10 min) | QA | W14 | 8h | M4.1 | Account lockout triggered; no DoS |
| Run load test (k6): 500 concurrent, 30 min duration | QA | W14-W15 | 12h | M4.6 | p95 < 200ms, error rate < 0.1% |
| Validate Redis and PostgreSQL capacity | DevOps | W14 | 6h | M4.6 | Connections < 70% max; no timeouts |
| Write operational runbooks (5 scenarios) | auth-team | W15 | 12h | M4.5 | Runbooks signed by tech lead |
| Run runbook drills (team executes each runbook) | auth-team | W15 | 8h | M4.5 | Drills documented; team achieves target recovery times |
| Set up on-call rotation and escalation procedures | DevOps | W15 | 4h | M4.5 | On-call schedule published; escalation paths clear |
| Configure Kubernetes HPA and pod auto-scaling | DevOps | W15 | 6h | M4.6 | Pods scale to 10 replicas on high CPU; scale back on low CPU |
| Write smoke tests for staging environment | QA | W16 | 6h | M4.5 | Smoke test runs on every deployment to staging |
| Code review: security hardening (token storage, input validation, logging) | Security | W15-W16 | 8h | M4.1 | Code review checklist signed |

### Phase 4 Success Criteria

| Criterion | Measurement | Target | Owner |
|-----------|-------------|--------|-------|
| **C4.1: Load test passing** | 500 concurrent users, 30-minute duration, p95 latency, error rate | p95 < 200ms, error rate < 0.1% | QA |
| **C4.2: Feature flags wired correctly** | AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH toggle correctly route traffic; no state leaks | Verified in staging; traffic routes correctly both ways | DevOps |
| **C4.3: API versioning enforced** | All endpoints accessible under `/v1/auth/*`; legacy `/auth/*` paths return 410 Gone or redirect | All endpoint tests updated; legacy paths disabled | auth-team |
| **C4.4: Rate limiting active** | Excess requests return 429; limits are per-endpoint and per-IP | Manual curl test and load test results show 429s | DevOps |
| **C4.5: Security audit complete** | Penetration test performed; XSS, CSRF, injection, token theft, brute-force tested; no P0/P1 findings | Audit report signed; findings tracked and resolved | Security |
| **C4.6: Observability operational** | Prometheus metrics, Grafana dashboards, alert rules all operational | Dashboards load with real data; alerts fire correctly | DevOps |
| **C4.7: Runbooks tested** | Team executes each runbook; recovery times meet targets | Runbook drills documented; all scenarios covered | auth-team |
| **C4.8: Rollback procedure validated** | Feature flags disabled; legacy auth path works; no data loss | Rollback test completed successfully | QA |

### Phase 4 Risk Mitigation

| Risk | Probability | Impact | Mitigation | Trigger |
|------|-------------|--------|-----------|---------|
| **Load test finds p95 > 200ms** | Medium | High | Profile bottlenecks (database, Redis, PasswordHasher); optimize slowest path; scale resources | Load test results show p95 > 200ms |
| **Penetration test finds XSS vulnerability** | Medium | Critical | Fix XSS (token storage, input sanitization) before GA; re-test | Penetration test finds XSS |
| **Rollback procedure doesn't work** | Low | Critical | Test rollback in staging before GA; dry-run with team | Rollback test fails |
| **Feature flag service down** | Low | High | Fallback to hardcoded feature flag state (conservative: assume new code is disabled); runbook for flag service recovery | Feature flag service unavailable |

---

## Phase 5: Rollout & GA (Weeks 17-20)

**Goal:** Execute three-phase rollout (Alpha → Beta 10% → GA 100%) with monitoring, observability, and on-call support. Achieve 99.9% uptime and < 200ms p95 latency in production.

### Milestones

- **M5.1: Alpha Deployment** — Deploy to staging; auth-team and QA test all flows; feature flag AUTH_NEW_LOGIN disabled by default
- **M5.2: Beta 10% Rollout** — Enable AUTH_NEW_LOGIN for 10% of production traffic; monitor latency, error rates, Redis usage; scale if needed
- **M5.3: GA 100% Rollout** — Remove AUTH_NEW_LOGIN gate; all users route to new `AuthService`; legacy auth deprecated
- **M5.4: 30-Day Stability** — Monitor first 30 days post-GA; verify SLOs met (99.9% uptime, < 200ms p95); respond to issues with on-call runbooks

### Rollout Phases

#### Phase 5a: Alpha (Internal Testing, Week 17)

| Step | Owner | Action | Success Criteria |
|------|-------|--------|-----------------|
| Deploy to staging | DevOps | Build Docker image, deploy to staging Kubernetes cluster | Pods healthy; liveness probes passing |
| Run smoke tests | QA | Execute smoke test suite: registration, login, profile, password reset | All smoke tests passing |
| Run load test (100 concurrent) | QA | 100-user load test on staging; confirm < 200ms p95 | p95 latency < 200ms, error rate < 0.1% |
| Manual end-to-end testing | auth-team, frontend-team | Full user flows: signup → login → profile → password reset; test on multiple browsers | All flows working; no errors; UX acceptable |
| Review logs and metrics | DevOps | Verify logs are clean (no exceptions); metrics are flowing; traces complete | No ERROR or WARN logs; all metrics present |
| **Go/No-Go Decision** | auth-team lead | Decide to proceed to Beta or hold for fixes | **GO → proceed to Beta** |

#### Phase 5b: Beta 10% (1 Week, Week 18)

| Step | Owner | Action | Success Criteria |
|------|-------|--------|-----------------|
| **Before Rollout:** Notify stakeholders | Product | Send announcement to product, support, customer success | All stakeholders aware; support has runbooks |
| Enable AUTH_NEW_LOGIN for 10% | DevOps | Set feature flag to route 10% of login/register traffic to new `AuthService` | Grafana shows ~10% traffic to new service |
| Monitor latency, errors, Redis | DevOps | Watch APM dashboards; alerts fire if p95 > 500ms, error rate > 5%, Redis connection failures | Metrics within normal ranges; no alerts |
| Monitor user feedback (support tickets) | Support | Watch support channels for auth-related issues | No issues reported; or issues are minor and tracked |
| Scale if needed | DevOps | If CPU > 70% or latency rising, add pods | HPA triggers scale-up; latency remains < 200ms |
| Review incident log | auth-team | Any failures? Root cause analysis? | No incidents; or minor incidents resolved quickly |
| **Go/No-Go Decision** | auth-team lead | Proceed to GA or reduce traffic and investigate | **GO → proceed to GA** |

#### Phase 5c: GA 100% (1 Week, Week 19)

| Step | Owner | Action | Success Criteria |
|------|-------|--------|-----------------|
| Remove AUTH_NEW_LOGIN gate | DevOps | Update feature flag to route 100% of traffic to new `AuthService`; legacy auth no longer used | All login/register traffic to new service |
| Monitor closely for 24 hours | DevOps | Watch dashboards every 30 minutes; be ready to rollback if issues | Latency stable, error rate < 0.1%, no cascading failures |
| Deprecate legacy auth | Engineering | Mark legacy auth code as deprecated; schedule removal for Q3 2026 | Deprecation notice added to code |
| Monitor for 7 days | DevOps | Daily review of metrics, logs, incidents | All metrics green; uptime > 99.9%; no escalations |
| **GA Celebration** | Product | Announce feature to customers | Announcement published; metrics confirm adoption |

#### Phase 5d: 30-Day Stability (Weeks 20-24, post-GA)

| Metric | Target | Measurement | Owner |
|--------|--------|-------------|-------|
| **Uptime** | 99.9% | Uptime monitoring via health check endpoint | DevOps |
| **p95 Latency** | < 200ms | APM dashboards (login, refresh, reset endpoints) | DevOps |
| **Error Rate** | < 0.1% | Error counter in APM divided by total requests | DevOps |
| **User Adoption** | > 1000 daily active users | Count of unique users with valid tokens | Product |
| **Registration Conversion** | > 60% (PRD target) | Funnel: landing → register → confirmed | Product |
| **Support Tickets** | < 5% auth-related | Ratio of auth tickets to total support volume | Support |
| **On-Call Incidents** | < 3 P1 incidents in 30 days | Incident tracker | auth-team |

### Post-GA Maintenance

- **Weeks 21-24:** On-call support (auth-team rotates); daily metrics review; respond to high-priority bugs
- **Week 25+:** Feature flag AUTH_TOKEN_REFRESH remains ON; full feature available; begin planning v1.1 (MFA, OAuth, etc.)

### Success Criteria for Phase 5

| Criterion | Measurement | Target | Owner |
|-----------|-------------|--------|-------|
| **C5.1: Alpha ready** | All smoke tests pass; no blocking bugs | 100% smoke tests passing | QA |
| **C5.2: Beta stable** | 10% traffic, 1 week, no escalations | p95 < 200ms, error rate < 0.1% | DevOps |
| **C5.3: GA traffic routed** | 100% login/register on new service | Grafana shows all traffic to new service | DevOps |
| **C5.4: 30-day SLO met** | Uptime, latency, error rate targets achieved | 99.9% uptime, < 200ms p95, < 0.1% errors | DevOps |
| **C5.5: User adoption** | Registration and daily active users meet PRD targets | > 1000 DAU within 30 days | Product |

---

## Comprehensive Risk Assessment

### Identified Risks (from Extraction)

| Risk ID | Risk | Severity | Probability | Mitigation Strategy | Phase | Trigger |
|---------|------|----------|-------------|---------------------|-------|---------|
| **R-001** | Token theft via XSS allows session hijacking | HIGH | Medium | AccessToken in memory only; refreshToken in httpOnly cookie; short 15-min expiry; `AuthProvider` clears on tab close; immediate token revocation endpoint (Phase 5 feature) | Phase 2 + Phase 4 | Penetration test finds XSS |
| **R-002** | Brute-force attacks on login endpoint | MEDIUM | High | Rate limiting (10 req/min per IP) at API Gateway; account lockout after 5 attempts; bcrypt cost 12 makes offline cracking expensive; CAPTCHA after 3 failed attempts (Phase 5 feature) | Phase 1 + Phase 4 | Load test triggers account lockout; brute-force stress test |
| **R-003** | Data loss during migration from legacy auth | HIGH | Low | Parallel operation of new and legacy auth (Phase 1-2); idempotent upsert for `UserProfile` migration; full database backup before each phase; rollback to legacy system if issues detected | Phase 0 + Phase 1 | Rollback test; backup validation |

### Additional Architectural Risks

| Risk | Category | Severity | Mitigation | Phase |
|------|----------|----------|-----------|-------|
| **Redis single point of failure** | Reliability | MEDIUM | Kubernetes StatefulSet with automatic failover; refresh token flow degrades gracefully (users re-login); monitoring and alerting for Redis health | Phase 0, Phase 4 |
| **PostgreSQL connection pool exhaustion** | Scalability | MEDIUM | pg-pool 100 connections; monitor active connections; slow query analysis; horizontal scaling (read replica) in Phase 5+ | Phase 0, Phase 4 |
| **Password hash timing attacks** | Security | LOW | bcryptjs library handles constant-time comparison; no custom comparison logic | Phase 1 |
| **JWT clock skew issues** | Security | MEDIUM | 5-second skew tolerance per architectural constraint; Phase 4 monitoring for skew rejection rate | Phase 2, Phase 4 |
| **Compliance audit failure** | Compliance | HIGH | Clear policy resolution (OQ-EXT-001); audit logging infrastructure (Phase 3); GDPR consent recording; 90-day or 12-month retention enforced | Phase 3 |
| **Feature flag service failure** | Operational | MEDIUM | Fallback to conservative default (assume new code disabled); runbook for flag service recovery | Phase 4, Phase 5 |

---

## Resource Requirements

### Team Composition

| Role | Count | Responsibility | Timeline |
|------|-------|-----------------|----------|
| **Backend Engineer (Auth)** | 3 | AuthService, PasswordHasher, TokenManager, JwtService, UserRepo, API endpoints, audit logging | W1-W16 (full-time), W17-W20 (on-call) |
| **Backend Engineer (Infrastructure/Integration)** | 2 | Database schema, migrations, API Gateway, rate limiting, feature flags, deployment manifests | W0-W16 (full-time), W17-W20 (part-time) |
| **Frontend Engineer** | 2 | LoginPage, RegisterPage, ProfilePage, AuthProvider, token refresh, form validation, error handling | W1-W12 (full-time), W13-W20 (on-call) |
| **DevOps Engineer** | 1 | Infrastructure provisioning, Kubernetes deployments, monitoring, alerting, on-call support | W-2 (full-time), W1-W16 (part-time), W17-W20 (on-call) |
| **QA Engineer** | 1 | Unit tests, integration tests, E2E tests, load testing, penetration testing coordination, runbook testing | W1-W16 (full-time), W17-W20 (on-call) |
| **Security Engineer (Part-Time)** | 1 (0.5 FTE) | Security policy finalization, code review, penetration testing, XSS/CSRF prevention, compliance validation | W-2, W1, W9-W10, W13-W15 |
| **Product/Project Lead** | 1 | Requirement clarification, stakeholder communication, milestone tracking, go/no-go decisions | W-2 (full-time), W0-W16 (part-time), W17-W20 (on-call) |

**Total Team Effort:** ~11 FTE over 20 weeks

### External Dependencies

| Dependency | Type | Status | Impact | Mitigation |
|------------|------|--------|--------|-----------|
| **PostgreSQL 15+** | Infrastructure | Must be provisioned by Week -2 | No DB → can't start Phase 1 | Provision in parallel; verify staging DB is ready |
| **Redis 7+** | Infrastructure | Must be provisioned by Week -2 | No Redis → can't store refresh tokens; Phase 2 blocked | Provision in parallel; HA failover configured |
| **SendGrid API** | External Service | API key obtained; test sending enabled | Password reset blocked if SendGrid down | Fallback email sending; alerting for SendGrid status |
| **Kubernetes Cluster** | Infrastructure | Staging and production available | No K8s → can't deploy; scaling impossible | Use existing cluster; request resource quota increase |
| **Node.js 20 LTS** | Runtime | Already available | Mandated by architectural constraint | Verify all development machines use v20 |
| **bcryptjs, jsonwebtoken Libraries** | Dependencies | npm packages available | Authentication broken without these | Explicit dependency pinning; security scanning in CI |
| **SEC-POLICY-001** | Policy Document | Must be finalized by Week -1 | Policy undefined → implementation guesses; compliance risk | Schedule security review meeting; target sign-off by Week -1 |

### Technology Stack

| Component | Technology | Justification | Risk Mitigation |
|-----------|-----------|---------------|-----------------|
| **Password Hashing** | bcryptjs v2.4+ | Industry standard; cost factor 12 per NIST; slow by design to resist offline cracking | Version pinned; cost parameter validated in tests |
| **JWT Signing** | jsonwebtoken + RSA 2048-bit | Stateless tokens; RS256 standard; key rotation support | Key rotation ceremony Q3 2026; code review ensures RS256 only |
| **Token Storage** | Redis 7+ | Sub-millisecond GET/SET; TTL auto-expiry; distributed HA failover | Kubernetes StatefulSet; replication enabled |
| **User Persistence** | PostgreSQL 15+ | ACID compliance; connection pooling via pg-pool; audit log retention | Regular backups; index tuning; replication for HA |
| **Email Delivery** | SendGrid v3 API | High deliverability; templating support; webhook events for bounce tracking | Fallback: manual email for urgent resets; monitoring |
| **API Framework** | Express.js / Fastify (Node.js) | Lightweight; middleware ecosystem; async/await support | Middleware stack code review; input validation on all endpoints |
| **Frontend Framework** | React | State management via Context API; hooks for token refresh logic | Token refresh testing via E2E; manual regression testing |

---

## Timeline Summary

```
Phase 0 (Weeks -2 to 0): Foundation
├─ M0.1: Infrastructure provisioned
├─ M0.2: Security policies finalized
└─ M0.3: Dev environment ready

Phase 1 (Weeks 1-4): Core Auth
├─ M1.1: Registration backend
├─ M1.2: Login backend + account lockout
├─ M1.3: Frontend LoginPage + RegisterPage
├─ M1.4: Unit & integration tests (80%+)
└─ M1.5: Feature flag AUTH_NEW_LOGIN + smoke tests

Phase 2 (Weeks 5-8): Token Management
├─ M2.1: JwtService (RS256)
├─ M2.2: TokenManager (Redis refresh tokens)
├─ M2.3: AuthProvider (silent refresh)
├─ M2.4: POST /auth/refresh endpoint
└─ M2.5: E2E token flow tests

Phase 3 (Weeks 9-12): Profile & Compliance
├─ M3.1: GET /auth/me + ProfilePage
├─ M3.2: Password reset flow + SendGrid
├─ M3.3: SendGrid email delivery
├─ M3.4: Audit logging (NFR-COMP-002)
├─ M3.5: Admin log query API
└─ M3.6: GDPR consent recording (NFR-COMP-001)

Phase 4 (Weeks 13-16): Hardening & Ops
├─ M4.1: Security testing (penetration, XSS, brute-force)
├─ M4.2: Feature flags fully wired
├─ M4.3: API versioning (/v1/auth/*) + rate limiting
├─ M4.4: Observability (Prometheus, Grafana, alerts)
├─ M4.5: Operational runbooks
└─ M4.6: Performance validated (load test, capacity plan)

Phase 5 (Weeks 17-20): GA Rollout
├─ M5.1: Alpha (internal testing)
├─ M5.2: Beta 10% (1 week)
├─ M5.3: GA 100% (production deployment)
└─ M5.4: 30-day stability monitoring
```

**Total Duration:** 20 weeks (5 months) from Phase 0 start to GA completion

---

## Compliance & Governance

### Regulatory Alignment

| Standard | Requirement | Phase Implementation | Validation |
|----------|-------------|----------------------|-----------|
| **GDPR** | Consent at registration + data minimization | Phase 3 M3.6 | Consent checkbox + `UserProfile` schema audit |
| **SOC2 Type II** | Audit logging with 12-month retention (PRD) or 90-day (TDD — **OQ-EXT-001**) | Phase 3 M3.4 | Audit log table; retention policy enforced via cron |
| **NIST SP 800-63B** | Adaptive password hashing + PBKDF2/bcrypt | Phase 1 M1.2 | bcrypt cost 12; UT-004 enforcement |
| **OWASP Top 10** | Token storage (XSS), CSRF, injection, brute-force | Phase 2 + Phase 4 | Penetration test; code review |

### Decision Tracking

All open questions and decision points tracked in dedicated documents:

| Issue | Raised | Owner | Status | Phase |
|-------|--------|-------|--------|-------|
| **OQ-001** | TDD S22 | Security | API key auth for service-to-service? | Open (deferred to v1.1) |
| **OQ-002** | TDD S22 | auth-team | Max roles array length? | Open (default to 10, validate in Phase 1) |
| **OQ-EXT-001** | Extraction | product-team + security | Audit log retention: 90 days (TDD) or 12 months (PRD)? | **MUST RESOLVE by Phase 3 M3.4** |
| **OQ-EXT-002** | Extraction | auth-team | Admin log query API in v1.0 scope? | Yes, Phase 3 M3.5 |
| **OQ-EXT-003** | Extraction | auth-team | Logout endpoint in v1.0 scope? | Deferred to Phase 5 (v1.1) — OQ-PRD-003 |
| **OQ-EXT-004** | Extraction | auth-team | Service-to-service auth (Sam persona)? | Addressed by FR-AUTH-003 (token refresh); API keys deferred |
| **OQ-EXT-005** | Extraction | auth-team | Consent field in `UserProfile`? | Yes, Phase 3 M3.6: `consent_timestamp` |
| **OQ-EXT-006** | Extraction | security | Account lockout policy (currently hardcoded 5/15min)? | **MUST FORMALIZE in SEC-POLICY-001 by Phase 0** |

### Approval Gates

| Phase | Gate | Approvers | Success Criteria |
|-------|------|-----------|-----------------|
| **Phase 0 → Phase 1** | Infrastructure Ready | DevOps, auth-team lead | PostgreSQL, Redis, CI/CD operational; SEC-POLICY-001 signed |
| **Phase 1 → Phase 2** | Registration & Login Tested | auth-team lead, QA | 80%+ unit test coverage; no P0 bugs; feature flag working |
| **Phase 2 → Phase 3** | Token Management Validated | auth-team lead, security | Load test p95 < 200ms; penetration test clear for Phase 2 components |
| **Phase 3 → Phase 4** | Compliance Ready | product-team, security, compliance | Audit logging working; consent recorded; OQ-EXT-001 resolved |
| **Phase 4 → Phase 5a (Alpha)** | Security Hardened | security lead, auth-team lead | Penetration test signed off; all P0/P1 findings resolved; runbooks tested |
| **Phase 5a → Phase 5b (Beta)** | Alpha Tested | auth-team lead, QA | Smoke tests 100% passing; no blocking bugs; on-call team ready |
| **Phase 5b → Phase 5c (GA)** | Beta Stable | DevOps, auth-team lead | 1 week at 10% traffic, no escalations; metrics healthy |
| **Phase 5c → Production** | GA Complete | CTO or senior eng lead | 100% traffic routed; 30-day SLOs tracked |

---

## Appendix: Explicit Component Wiring Checklist

This table enumerates every registry, dispatch mechanism, and cross-phase dependency. Architects and implementers use this as a checklist to ensure no wiring is missed.

| Mechanism | Type | Owning Phase | Responsibility | Wired Components | Cross-Phase Dependencies | Status |
|-----------|------|--------------|-----------------|------------------|------------------------|--------|
| **Account Lockout Registry** | In-process map | Phase 1 M1.2 | `AuthService` | AuthService.login() checks and increments | Phase 4: Move to Redis for persistence | Planned |
| **Error Code Registry** | Centralized constants | Phase 1 M1.3 | API handlers | ErrorCodes exported; handlers use codes | Phase 2, Phase 3 extend with new codes | Planned |
| **Rate Limit Registry** | Centralized config | Phase 1 M1.5 | API Gateway middleware | Per-endpoint limits (10 login, 5 register) | Phase 4: API Gateway enforces | Planned |
| **Token Signing Key Registry** | Kubernetes secrets | Phase 2 M2.1 | `JwtService`, KeyManager | RS256 private key (signing), public key (verification) | Phase 0: Key generation; Phase 4: Key rotation | Planned |
| **Token Storage Registry** | Redis client config | Phase 2 M2.2 | `TokenManager`, `RedisClient` | Refresh token SET/GET/DEL operations | Phase 0: Redis provisioning; Phase 4: Monitoring | Planned |
| **Token Refresh Polling Registry** | setInterval config | Phase 2 M2.3 | `AuthProvider` | Polling interval, refresh trigger logic | Phase 3: Logout stops polling | Planned |
| **Reset Token Registry** | In-process map or Redis | Phase 3 M3.2 | `AuthService`, `ResetTokenManager` | Reset token generation, validation, consumption | Phase 4: Move to Redis for distributed deployments | Planned |
| **Audit Event Registry** | Centralized logger | Phase 3 M3.4 | `AuditLogger`, all endpoints | Event types, schemas, PostgreSQL writes | Phase 4: Monitoring consumes audit logs | Planned |
| **Admin Authorization Middleware** | Middleware function | Phase 3 M3.5 | Admin endpoints | Role check (JWT.roles includes 'admin') | Phase 1/2: JWT issued with roles | Planned |
| **Feature Flag Registry** | Feature flag service | Phase 4 M4.2 | Routing layer, middleware | AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH flags | Phase 5: Flags toggled during rollout | Planned |
| **Prometheus Metrics Registry** | Metric exports | Phase 4 M4.4 | APM instrumentation, endpoint handlers | Counters, histograms, gauges for all components | Phase 5: Dashboards consume metrics | Planned |
| **Alert Rules Registry** | Prometheus AlertManager | Phase 4 M4.4 | DevOps, on-call | Rules fire on error rate, latency, connection failures | Phase 5: Pages on-call when fired | Planned |
| **Consent Recording Registry** | `UserProfile` consent_timestamp field | Phase 3 M3.6 | `RegisterPage`, `AuthService.register()` | Checkbox gated submit; timestamp recorded on success | Phase 4: Compliance audit uses field | Planned |

---

## Open Questions Requiring Resolution

| ID | Question | Owner | Target Date | Impact if Unresolved |
|----|----------|-------|-------------|----------------------|
| **OQ-EXT-001** | Audit log retention: 90 days (TDD S7.2) or 12 months (PRD S17)? | product-team + security | Week 0 | Phase 3 M3.4 blocked; compliance uncertainty |
| **OQ-EXT-006** | Account lockout policy currently hardcoded (5 attempts / 15 min in FR-AUTH-001). Has this been formally decided, or is it up for discussion? | security + product | Week -1 | Implementation in Phase 1 M1.2 depends on this |
| **OQ-EXT-003** | Logout functionality: Is logout (clear tokens, end session) in v1.0 scope? PRD user story AUTH-E1 mentions it. TDD has no corresponding FR or endpoint. | product + auth-team | Week 0 | If yes, adds 1-2 tasks to Phase 3; if no, document deferral to v1.1 |
| **OQ-PRD-001** | Async or sync email delivery for password reset? | Engineering | Phase 3 start (W9) | Async is safer (non-blocking); sync is simpler but risks timeout on high load |
| **OQ-PRD-002** | Max refresh tokens per user across devices? | Product | Phase 2 start (W5) | Affects `TokenManager` design; unlimited vs. 5-per-user |
| **OQ-001** | Should `AuthService` support API key authentication for service-to-service calls? | test-lead | 2026-04-15 (W4) | Deferred to v1.1; document rationale |

---

## Success Metrics (Roadmap-Level)

| Metric | Baseline | Target (GA) | Phase Validated |
|--------|----------|------------|-----------------|
| **Engineering Quality** | 0% | 80%+ unit test coverage, 0 P0 bugs, <3 P1 bugs at GA | Phase 4 |
| **Performance** | Unknown | p95 login < 200ms, p95 refresh < 100ms | Phase 4 load test |
| **Reliability** | 0% | 99.9% uptime (30-day rolling) | Phase 5 |
| **Security** | Unaudited | Penetration test passed, no P0/P1 findings, token theft mitigated | Phase 4 |
| **Compliance** | Non-compliant | GDPR consent + SOC2 audit logging operational | Phase 3 |
| **User Adoption** (from PRD) | 0 users | >1000 DAU within 30 days; >60% registration conversion | Phase 5 |
| **Feature Flag Readiness** | No flags | Both AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH operational and tested | Phase 4 |
| **Runbook Coverage** | None | 5 scenarios documented and team-tested | Phase 4 |

---

## Conclusion

This roadmap delivers the User Authentication Service in five phases over 20 weeks with explicit risk mitigation, architectural precision, and compliance gates. The phased approach prioritizes security-first sequencing (token management hardened before frontend exposure), compliance-first integration (GDPR and SOC2 built into Phase 3, not bolted on afterward), and operational readiness (runbooks, monitoring, SLOs defined by Phase 4, tested before GA).

Key architect priorities honored throughout:
1. **No surprise wiring failures** — Every registry, dispatch mechanism, and dependency explicitly enumerated
2. **Rollback-safe** — Feature flags with clear triggers and procedures; all major phases reversible
3. **Risk-mitigated** — R-001 (token theft), R-002 (brute-force), R-003 (data loss) addressed with specific mitigations and phase gates
4. **Observable** — Monitoring, alerting, and tracing in place by Phase 4; on-call runbooks by Phase 4; SLOs tracked at GA

Success criteria are measurable, enforceable, and tied to business outcomes (PRD Success Metrics: registration conversion > 60%, session duration > 30 min, failed login rate < 5%).
