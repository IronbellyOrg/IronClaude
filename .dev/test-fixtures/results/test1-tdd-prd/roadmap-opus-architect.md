---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.55
primary_persona: architect
---

# User Authentication Service — Project Roadmap

## 1. Executive Summary

This roadmap defines the phased delivery of a User Authentication Service comprising five functional requirements (FR-AUTH-001 through FR-AUTH-005), nine non-functional requirements, and four compliance mandates. The system follows a facade pattern with `AuthService` orchestrating `PasswordHasher`, `TokenManager`, `JwtService`, and `UserRepo` against PostgreSQL 15+, Redis 7+, and SendGrid.

**Complexity:** MEDIUM (0.55). The security-critical domain elevates risk, but the architectural pattern is well-understood. No novel algorithms or unproven technologies are involved.

**Critical path:** Infrastructure provisioning → data model migration → `AuthService` core (login/register) → token lifecycle → frontend integration → compliance hardening → phased rollout.

**Business driver:** Authentication unblocks ~$2.4M in projected annual revenue from personalization features and is required for SOC2 Type II audit in Q3 2026.

---

## 2. Phased Implementation Plan

### Phase 1: Foundation & Core Authentication (Weeks 1–3)

**Goal:** Standing infrastructure, data model, and core login/registration flows operational in staging.

**Milestone M1:** `AuthService` login and registration endpoints passing integration tests against real PostgreSQL and Redis.

#### 1.1 Infrastructure Provisioning
- Provision PostgreSQL 15+ with connection pooling (100 pool size)
- Provision Redis 7+ cluster (1 GB initial, scaling plan to 2 GB at 70% utilization)
- Configure Docker Compose for local development (PostgreSQL + Redis)
- Set up testcontainers configuration for CI pipeline
- Generate RSA 2048-bit key pair for `JwtService` RS256 signing
- Configure SendGrid API access and verify sender domain

#### 1.2 Data Model & Migration
- Create `UserProfile` table in PostgreSQL:
  - `id` (UUID v4, PK), `email` (UNIQUE, indexed, lowercase), `displayName` (2-100 chars), `password_hash` (NOT NULL), `createdAt`, `updatedAt`, `lastLoginAt` (nullable), `roles` (default `["user"]`)
- Create audit log table in PostgreSQL with 12-month retention policy (per NFR-COMP-002, overriding TDD's 90-day specification)
- Create `failed_login_attempts` tracking table for brute-force mitigation
- Write idempotent migration scripts with rollback support

#### 1.3 Core Backend Components
- **`PasswordHasher`** — bcrypt hash/verify with cost factor 12 (NFR-SEC-001, NFR-COMP-003)
  - Abstraction layer to enable future argon2id migration without API changes
  - Validate raw passwords are never persisted or logged (NFR-COMP-003)
- **`UserRepo`** — CRUD operations against PostgreSQL `UserProfile` table
  - Email uniqueness enforcement at database level
  - Lowercase normalization on write
- **`AuthService`** (facade) — orchestrates `PasswordHasher` + `UserRepo` for:
  - **FR-AUTH-001:** Login with email/password validation
    - Account lockout after 5 failed attempts within 15 minutes (FR-AUTH-001 AC4)
    - Identical error responses for invalid credentials and non-existent email (no user enumeration)
  - **FR-AUTH-002:** Registration with email uniqueness, password strength validation (≥8 chars, uppercase, number), GDPR consent capture with timestamp (NFR-COMP-001)
  - Data minimization: only email, hashed password, displayName collected (NFR-COMP-004)

#### 1.4 API Layer (Partial)
- POST `/v1/auth/login` — 10 req/min per IP rate limit
- POST `/v1/auth/register` — 5 req/min per IP rate limit
- Consistent error response schema: `{ error: { code, message, status } }`
- URL prefix versioning (`/v1/auth/*`)

#### 1.5 Testing — Wave 1
- Unit tests UT-001, UT-002: `AuthService` login flows
- Integration test IT-001: Registration persists `UserProfile` to database
- Unit tests for `PasswordHasher`: bcrypt cost factor 12 assertion (NFR-SEC-001)
- Password strength validation test cases

#### 1.6 Compliance Gate (Phase 1)
- Verify GDPR consent field captured at registration (NFR-COMP-001)
- Verify audit log table schema includes: user ID, timestamp, IP address, outcome (NFR-COMP-002)
- Verify raw passwords never appear in logs or database (NFR-COMP-003)
- Verify data minimization — no PII beyond email, hash, displayName (NFR-COMP-004)

**Deliverables:** Working login + registration endpoints, database schema, infrastructure running in staging.

---

### Phase 2: Token Lifecycle & Session Management (Weeks 4–5)

**Goal:** Full JWT token issuance, refresh, and revocation operational. Session persistence across page refreshes.

**Milestone M2:** Token refresh cycle passing end-to-end with Redis TTL enforcement.

#### 2.1 Token Components
- **`JwtService`** — JWT sign/verify with RS256 using 2048-bit RSA keys (NFR-SEC-002)
  - Access token: 15-minute expiry, payload contains `UserProfile.id` and `UserProfile.roles`
  - Configuration validation test for RS256 signing
- **`TokenManager`** — Token lifecycle management
  - Issue `AuthToken` pair (accessToken + refreshToken) on login
  - Store refresh tokens in Redis with 7-day TTL
  - Revoke old refresh token on refresh (rotation)
  - Token revocation capability for security incidents (R-001 contingency)

#### 2.2 API Layer (Completion)
- POST `/v1/auth/refresh` — 30 req/min per user rate limit
- GET `/v1/auth/me` — 60 req/min per user, Bearer token auth (FR-AUTH-004)
  - Returns full `UserProfile`: id, email, displayName, createdAt, updatedAt, lastLoginAt, roles

#### 2.3 Integration Wiring
- Wire `TokenManager` into `AuthService.login()`: after `PasswordHasher.verify()` succeeds, call `TokenManager.issueTokens()` via `JwtService`
- Wire `AuthService.getProfile()` to validate accessToken via `JwtService`, then fetch from `UserRepo`

#### 2.4 Testing — Wave 2
- Unit test UT-003: Token refresh with valid refresh token
- Integration test IT-002: Expired refresh token rejected (Redis TTL)
- Token signing validation tests (NFR-SEC-002)
- Concurrent authentication load test baseline (NFR-PERF-002: 500 concurrent logins)

**Deliverables:** Complete auth API (4 endpoints), token lifecycle, profile retrieval.

---

### Phase 3: Password Reset & Email Integration (Weeks 6–7)

**Goal:** Self-service password reset flow operational end-to-end via SendGrid.

**Milestone M3:** Password reset email delivered, token validated, password updated, old sessions invalidated.

#### 3.1 Password Reset Implementation (FR-AUTH-005)
- POST `/v1/auth/reset-request` — generates cryptographically random reset token, 1-hour TTL
  - Identical response for registered and unregistered emails (no user enumeration)
  - Sends reset email via SendGrid with time-limited link
- POST `/v1/auth/reset-confirm` — validates token, updates password hash via `PasswordHasher`, invalidates all existing refresh tokens via `TokenManager`
  - Used reset tokens cannot be reused (single-use enforcement)

#### 3.2 Email Service Integration
- SendGrid API integration with delivery monitoring
- Email template for password reset link
- Delivery failure alerting (R-007 mitigation)

#### 3.3 Testing — Wave 3
- Unit tests for reset token generation, expiry, single-use enforcement
- Integration test: full reset flow (request → email → confirm → login with new password)
- SendGrid integration test (staging environment)

#### 3.4 Open Question Resolution Gate
- OQ-003: Synchronous vs asynchronous reset email sending — decision needed before implementation
- OQ-008: POST `/auth/logout` endpoint — determine if needed for v1.0 or client-side token deletion sufficient

**Deliverables:** Complete password reset flow, SendGrid integration, all 5 functional requirements implemented.

---

### Phase 4: Frontend Integration (Weeks 7–9)

**Goal:** All frontend components integrated with backend API, auth state management operational.

**Milestone M4:** E2E test E2E-001 passing (register → login → profile).

#### 4.1 Frontend Components
- **`AuthProvider`** (Context Provider) — manages `AuthToken` state in memory (not localStorage — R-001 mitigation)
  - Silent refresh via `TokenManager` refresh endpoint
  - Clear tokens on tab close
  - HttpOnly cookies for refreshToken
  - Expose auth methods to child components
- **`LoginPage`** — email/password form, calls POST `/v1/auth/login`
  - Generic error messages (no user enumeration)
  - Redirect to dashboard on success
- **`RegisterPage`** — registration form with client-side validation
  - Inline password strength feedback
  - GDPR consent checkbox (NFR-COMP-001)
  - `termsUrl` prop for legal compliance link
- **ProfilePage** — displays `UserProfile` from GET `/v1/auth/me`

#### 4.2 Route Structure & Protection
- `/login` → `LoginPage` (public)
- `/register` → `RegisterPage` (public)
- `/profile` → ProfilePage (protected — redirect to `/login` if unauthenticated)
- Component hierarchy: `App > AuthProvider > PublicRoutes | ProtectedRoutes`

#### 4.3 Persona-Driven UX Validation
- **Alex (end user):** Registration completes in under 60 seconds; session persists across page refreshes
- **Sam (API consumer):** Programmatic token refresh works without user interaction; clear error codes returned

#### 4.4 Testing — Wave 4
- E2E test E2E-001: User registers and logs in (RegisterPage → LoginPage → ProfilePage)
- `AuthProvider` silent refresh test
- XSS prevention validation (R-001): verify tokens not in localStorage/DOM

**Deliverables:** All frontend components, auth state management, E2E tests passing.

---

### Phase 5: Observability, Compliance & Hardening (Weeks 9–11)

**Goal:** Production-ready observability, compliance validation, security hardening complete.

**Milestone M5:** All NFRs validated, compliance audit checklist green, security review passed.

#### 5.1 Observability Stack
- **Prometheus metrics:**
  - `auth_login_total` (counter) — login attempts by outcome
  - `auth_login_duration_seconds` (histogram) — login latency
  - `auth_token_refresh_total` (counter) — refresh operations
  - `auth_registration_total` (counter) — registration attempts
- **Alerts:**
  - Login failure rate > 20% over 5 minutes
  - p95 latency > 500ms
  - `TokenManager` Redis connection failures
- **OpenTelemetry tracing:** Spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`
- **Structured logging:** All auth events with user ID, timestamp, IP address, and outcome (NFR-COMP-002)

#### 5.2 Audit Log Hardening
- Validate 12-month retention policy (NFR-COMP-002 — PRD overrides TDD's 90-day)
- Validate IP address logging in all auth events
- Validate log queryability by date range and user (Jordan admin persona requirement)

#### 5.3 Performance Validation
- NFR-PERF-001: All auth endpoints < 200ms at p95 (APM instrumentation on `AuthService` methods)
- NFR-PERF-002: 500 concurrent login requests (k6 load test)
- NFR-REL-001: Health check endpoint for 99.9% uptime monitoring
- Success Criteria #3: Token refresh latency < 100ms at p95
- Success Criteria #5: Password hash time < 500ms with bcrypt cost 12

#### 5.4 Security Review
- Penetration testing before production (R-005 mitigation)
- XSS token theft prevention validation (R-001)
- Brute-force protection validation: rate limiting + account lockout (R-002)
- No user enumeration across all endpoints (login, register, password reset)

#### 5.5 Compliance Final Gate
- NFR-COMP-001: GDPR consent with timestamp at registration — verified
- NFR-COMP-002: SOC2 audit logging with 12-month retention — verified
- NFR-COMP-003: NIST SP 800-63B password storage — verified
- NFR-COMP-004: GDPR data minimization — verified

**Deliverables:** Full observability, compliance validation report, security review sign-off.

---

### Phase 6: Phased Rollout (Weeks 11–15)

**Goal:** Production deployment via feature-flagged phased rollout with rollback capability.

**Milestone M6 (GA):** 100% traffic on new auth service, legacy deprecated.

#### 6.1 Feature Flag Setup
| Flag | Purpose | Default | Cleanup Target |
|------|---------|---------|----------------|
| `AUTH_NEW_LOGIN` | Gates new `LoginPage` and `AuthService` login endpoint | OFF | Remove after GA |
| `AUTH_TOKEN_REFRESH` | Enables refresh token flow in `TokenManager` | OFF | Remove GA + 2 weeks |

#### 6.2 Phase 1 — Internal Alpha (1 week)
- Deploy `AuthService` to staging
- auth-team and QA validate all FR-AUTH-001 through FR-AUTH-005
- `LoginPage` and `RegisterPage` behind `AUTH_NEW_LOGIN` flag
- **Gate:** Zero P0/P1 bugs. All functional requirements pass manual testing.
- **Rollback:** Disable `AUTH_NEW_LOGIN` flag

#### 6.3 Phase 2 — Beta 10% (2 weeks)
- Enable `AUTH_NEW_LOGIN` for 10% of traffic
- Monitor: p95 latency, error rates, Redis usage, registration conversion
- Run parallel with legacy auth (R-003 mitigation)
- **Gate:** p95 latency < 200ms. Error rate < 0.1%. No Redis connection failures.
- **Rollback:** Disable `AUTH_NEW_LOGIN` flag

#### 6.4 Phase 3 — GA 100% (1 week)
- Remove `AUTH_NEW_LOGIN` flag — all traffic to `AuthService`
- Enable `AUTH_TOKEN_REFRESH` for refresh flow
- Legacy auth deprecated
- **Gate:** 99.9% uptime over 7 days. All dashboards green.
- **Rollback:** Re-enable legacy auth

#### 6.5 Rollback Criteria
Rollback triggers if any occur:
- p95 latency > 1000ms for > 5 minutes
- Error rate > 5% for > 2 minutes
- `TokenManager` Redis connection failures > 10/minute
- Any data loss or corruption in `UserProfile` records

#### 6.6 Operational Readiness
- Runbooks deployed for: `AuthService` down, token refresh failures
- On-call: auth-team 24/7 rotation for first 2 weeks post-GA
- Capacity: HPA scales `AuthService` pods to 10 at CPU > 70%

**Deliverables:** Production deployment at 100%, legacy deprecated, operational runbooks active.

---

## 3. Integration Points & Dispatch Mechanisms

### 3.1 AuthService Facade (Dispatch Table)

- **Named Artifact:** `AuthService` method dispatch — all external consumers call `AuthService` exclusively
- **Wired Components:** `PasswordHasher`, `TokenManager`, `UserRepo`, `JwtService` (indirect via `TokenManager`)
- **Owning Phase:** Phase 1 creates the facade with `PasswordHasher` + `UserRepo`; Phase 2 wires `TokenManager`
- **Cross-Reference:** Phase 3 (password reset) and Phase 4 (frontend) consume the facade

### 3.2 TokenManager → JwtService Wiring

- **Named Artifact:** `TokenManager` dependency on `JwtService` for JWT sign/verify
- **Wired Components:** `JwtService` (RS256 signing), Redis (refresh token storage)
- **Owning Phase:** Phase 2 creates and wires this mechanism
- **Cross-Reference:** Phase 3 (reset invalidates tokens), Phase 4 (`AuthProvider` silent refresh), Phase 6 (feature flag `AUTH_TOKEN_REFRESH`)

### 3.3 AuthProvider → API Binding

- **Named Artifact:** `AuthProvider` React context — binds frontend auth state to backend API
- **Wired Components:** `LoginPage`, `RegisterPage`, ProfilePage consume context; `AuthProvider` calls `/v1/auth/login`, `/v1/auth/refresh`, `/v1/auth/me`
- **Owning Phase:** Phase 4 creates the context provider and wires all page components
- **Cross-Reference:** Phase 6 rollout gates frontend behind `AUTH_NEW_LOGIN` flag

### 3.4 Feature Flag Registry

- **Named Artifact:** Feature flag configuration (`AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`)
- **Wired Components:** API gateway routing, `AuthProvider` refresh logic, `LoginPage`/`RegisterPage` rendering
- **Owning Phase:** Phase 6 creates and manages flags
- **Cross-Reference:** Phase 6.2–6.4 progressively enable; cleanup targets defined per flag

### 3.5 Rate Limiting Configuration

- **Named Artifact:** API Gateway rate limit rules per endpoint
- **Wired Components:** `/v1/auth/login` (10/min/IP), `/v1/auth/register` (5/min/IP), `/v1/auth/me` (60/min/user), `/v1/auth/refresh` (30/min/user)
- **Owning Phase:** Phase 1 configures login/register limits; Phase 2 adds me/refresh limits
- **Cross-Reference:** Phase 5 validates under load; Phase 6 monitors in production

---

## 4. Risk Assessment & Mitigation

| Risk | Severity | Phase Addressed | Mitigation Strategy |
|------|----------|----------------|---------------------|
| **R-001** Token theft via XSS | HIGH | Phase 4 | Store accessToken in memory only (not localStorage). HttpOnly cookies for refreshToken. 15-minute access token expiry. `AuthProvider` clears on tab close. |
| **R-002** Brute-force attacks | HIGH | Phase 1, 5 | Rate limiting at API gateway. Account lockout after 5 failed attempts. bcrypt cost 12. CAPTCHA escalation after 3 failures. |
| **R-003** Data loss during migration | HIGH | Phase 6 | Parallel operation with legacy during beta. Idempotent upserts. Full database backup before each rollout phase. |
| **R-004** Low registration adoption | HIGH | Phase 4 | Usability testing before launch. Registration < 60 seconds target. Iterate on funnel data post-GA. |
| **R-005** Security breach from flaws | CRITICAL | Phase 5 | Dedicated security review. Penetration testing before production. No shortcuts on crypto implementations. |
| **R-006** Incomplete audit logging | HIGH | Phase 5 | Define log requirements in Phase 1 schema. Validate against SOC2 controls in Phase 5. 12-month retention. |
| **R-007** Email delivery failures | MEDIUM | Phase 3 | SendGrid delivery monitoring and alerting. Fallback support channel documented. |

---

## 5. Resource Requirements & Dependencies

### Team Requirements
- **Backend engineers:** 2 (core auth service, token lifecycle, API layer)
- **Frontend engineer:** 1 (auth pages, AuthProvider, route protection)
- **Security engineer:** 0.5 (review in Phase 5, advisory throughout)
- **QA engineer:** 1 (test pyramid execution, load testing, E2E)
- **DevOps:** 0.5 (infrastructure provisioning, observability, rollout)

### Infrastructure Dependencies (Must Be Ready Before Phase 1)
| Dependency | Version | Owner | Lead Time |
|------------|---------|-------|-----------|
| PostgreSQL | 15+ | Platform team | 1 week |
| Redis | 7+ | Platform team | 1 week |
| Node.js | 20 LTS | Engineering | Available |
| SendGrid API | — | Platform team | 2-3 days |
| RSA key pair generation | 2048-bit | Security team | 1 day |
| Frontend routing framework | — | Frontend team | Available |

### Library Dependencies
- `bcryptjs` — password hashing in `PasswordHasher`
- `jsonwebtoken` — JWT sign/verify in `JwtService`
- Jest + ts-jest — unit testing
- Supertest — API integration testing
- testcontainers — CI database/cache testing
- Playwright — E2E testing
- k6 — load testing (Phase 5)

---

## 6. Success Criteria & Validation

| # | Metric | Target | Validation Phase | Method |
|---|--------|--------|-----------------|--------|
| 1 | Login response time (p95) | < 200ms | Phase 5 | APM on `AuthService.login()` |
| 2 | Registration success rate | > 99% | Phase 5 | Ratio of successful registrations |
| 3 | Token refresh latency (p95) | < 100ms | Phase 5 | APM on `TokenManager.refresh()` |
| 4 | Service availability | 99.9% uptime | Phase 6 (post-GA) | Health check monitoring, 30-day window |
| 5 | Password hash time | < 500ms | Phase 1 | Benchmark `PasswordHasher.hash()` |
| 6 | Registration conversion | > 60% | Phase 6 (post-GA) | Funnel analytics |
| 7 | Daily active authenticated users | > 1000 within 30 days | Phase 6 (post-GA) | `AuthToken` issuance counts |
| 8 | Average session duration | > 30 minutes | Phase 6 (post-GA) | Token refresh analytics |
| 9 | Failed login rate | < 5% | Phase 6 (post-GA) | Auth event log analysis |
| 10 | Password reset completion | > 80% | Phase 6 (post-GA) | Funnel: requested → new password set |

---

## 7. Timeline Summary

| Phase | Weeks | Duration | Key Milestone |
|-------|-------|----------|---------------|
| Phase 1: Foundation & Core Auth | 1–3 | 3 weeks | M1: Login/register endpoints passing integration tests |
| Phase 2: Token Lifecycle | 4–5 | 2 weeks | M2: Token refresh cycle with Redis TTL |
| Phase 3: Password Reset & Email | 6–7 | 2 weeks | M3: End-to-end password reset flow |
| Phase 4: Frontend Integration | 7–9 | 2 weeks (overlaps Phase 3) | M4: E2E-001 passing |
| Phase 5: Observability & Hardening | 9–11 | 2 weeks | M5: All NFRs validated, security review passed |
| Phase 6: Phased Rollout | 11–15 | 4 weeks | M6: GA at 100%, legacy deprecated |
| **Total** | | **~13 weeks** | |

**Note:** Phases 3 and 4 overlap — frontend work on `LoginPage`/`RegisterPage` can begin while password reset backend is developed. Phase 4's `AuthProvider` silent refresh depends on Phase 2 completion.

---

## 8. Open Questions Requiring Resolution

These open questions from the extraction should be resolved per the indicated timeline to avoid blocking development:

| ID | Question | Blocks Phase | Recommended Resolution Date |
|----|----------|-------------|----------------------------|
| OQ-001 | API key auth for service-to-service? | Post-v1.0 | 2026-04-15 (per extraction) |
| OQ-002 | Max `UserProfile` roles array length? | Phase 1 (schema) | Before Phase 1 start |
| OQ-003 | Sync vs async password reset emails? | Phase 3 | Before Phase 3 start |
| OQ-004 | Max refresh tokens per user? | Phase 2 | Before Phase 2 start |
| OQ-005 | "Remember me" extended sessions? | Phase 2 | Before Phase 2 start |
| OQ-006 | API key auth beyond JWT for Sam persona? | Post-v1.0 (out of scope per PRD S12) | Defer |
| OQ-007 | Admin API for log query + account unlock? | Phase 5 or post-v1.0 | Before Phase 5 start |
| OQ-008 | POST `/auth/logout` endpoint needed? | Phase 4 | Before Phase 4 start |

**Scope note:** Per PRD S12, OAuth/OIDC, MFA, RBAC, and social login are explicitly out of scope for v1.0. OQ-001 and OQ-006 (service-to-service auth) should be deferred unless the product decision brings them into v1.0 scope.
