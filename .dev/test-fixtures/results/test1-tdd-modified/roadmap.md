---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.65
adversarial: true
---

## Executive Summary

This roadmap delivers a stateless JWT-based authentication platform (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo`) with email/password login, registration, token refresh, profile retrieval, password reset, and corresponding frontend flows (`AuthProvider`, `LoginPage`, `RegisterPage`, `ProfilePage`). The system spans five domains — backend, security, frontend, testing, devops — at **MEDIUM complexity (0.65)**, driven primarily by the security surface area: JWT lifecycle with RS256, bcrypt cost management, account lockout, token revocation, and safe legacy migration.

All nine requirements (FR-AUTH-001–005, NFR-PERF-001–002, NFR-REL-001, NFR-SEC-001–002) are addressed with explicit phase assignments, per-phase checklist tasks, inline wiring tables, and measurable validation criteria. Three spec risks (R-001–003) are covered with full roadmap-controls traceability; three architect-identified risks (R-004–006) are added using the same structure.

The implementation proceeds through **six phases** over approximately **9–11 weeks**: a 3–5 day architecture baseline (Phase 0), then infrastructure and security primitives (Phase 1), backend domain services (Phase 2), frontend integration (Phase 3), observability and operational readiness (Phase 4), and a four-week staged rollout to GA (Phase 5). Observability is explicitly separated from rollout to break the circular dependency identified in the adversarial debate: the Beta gate requires p95 < 200ms and error rate < 0.1%, which require Prometheus metrics to measure — metrics that must be validated *before* rollout traffic is exposed, not during it.

Phase 0 is retained from the base variant because six open questions (OQ-001–006) include implementation-level decisions the spec deliberately defers — error code taxonomy, Redis key schema, reset token format, audit log schema — that cause mid-sprint interface churn if resolved ad hoc. The 3–5 day investment prevents scattered rework across every subsequent phase.

---

## Phased Implementation Plan

### Phase 0 — Architecture Baseline and Delivery Controls

**Timeline:** 3–5 working days

**Objective:** Lock API contracts, resolve or explicitly defer open questions, and establish rollout guardrails before a single implementation dependency is created.

**Milestone — M0:** Architecture and interface freeze approved by auth-team, platform-team, and QA.

#### Scope and Checklist

- [ ] Confirm API contract: `/v1/auth/login`, `/v1/auth/register`, `/v1/auth/me`, `/v1/auth/refresh`, `/v1/auth/reset-request`, `/v1/auth/reset-confirm` — all under `/v1/auth/*` per AC-007
- [ ] Finalize JSON error schema per AC-009: `{ error: { code, message, status } }` — assign error codes to all domain failure cases
- [ ] Finalize TLS 1.3 enforcement policy per AC-008
- [ ] Finalize 5-second JWT clock-skew tolerance per AC-010
- [ ] Resolve or explicitly defer each open question:
  - OQ-001: API key auth for service-to-service → *defer to v1.1*
  - OQ-002: Max roles array length → *default to 20; revisit post-RBAC review*
  - OQ-003: Password reset email template and sender identity → *resolve before Phase 2 begins*
  - OQ-004: RSA key rotation procedure → *document manual rotation; automate in v1.1*
  - OQ-005: Rate limits on reset endpoints → *apply 5 req/min per IP (same as registration)*
  - OQ-006: Legacy auth migration schema mapping → *require schema mapping document before Phase 5*
- [ ] Produce architecture decision record (ADR) covering: RS256 key lifecycle (AC-001), bcrypt abstraction boundary (AC-003), stateless access-token model (AC-002), Redis key schema for hashed refresh tokens
- [ ] Document audit log schema: event types, field names, retention policy (90 days)
- [ ] Establish feature-flag ownership model: `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`
- [ ] Confirm rollback trigger thresholds:
  - p95 latency > 1000ms sustained for > 5 minutes
  - Error rate > 5% for > 2 minutes
  - `TokenManager` Redis failures > 10/min
  - Any `UserProfile` data loss or corruption
- [ ] Produce production readiness checklist for M4 signoff

**Requirements addressed:** AC-001–AC-010 (contract level); planning dependencies for FR-AUTH-001–005, NFR-PERF-001–002, NFR-REL-001, NFR-SEC-001–002.

**Security review checkpoint:** Auth-team lead and one security-aware reviewer sign off on ADR before Phase 1 begins.

---

### Phase 1 — Core Infrastructure, Persistence, and Security Primitives

**Timeline:** 1–1.5 weeks

**Objective:** Stand up runtime, persistence, secrets, and foundational services that all subsequent phases depend on.

**Milestone — M1:** `PasswordHasher`, `JwtService`, and storage layers validated in isolation; benchmark evidence produced.

#### Infrastructure Provisioning

- [ ] Provision PostgreSQL 15+ with connection pooling (pg-pool, 100 initial pool size); ~1 week lead time for managed cloud — blocks all data persistence work
- [ ] Provision Redis 7+ with 1 GB memory allocation; ~1 week lead time for managed cloud — blocks `TokenManager` implementation
- [ ] Configure Node.js 20 LTS runtime per AC-006 — minimal lead time
- [ ] Generate RSA 2048-bit key pair for JWT signing; store in secrets management, not filesystem — AC-001
- [ ] Document RSA key loading procedure and quarterly rotation procedure (OQ-004)
- [ ] Set up Docker Compose for local dev (PostgreSQL + Redis containers)
- [ ] Configure TLS 1.3 termination per AC-008

#### Data Model Implementation

- [ ] Create `UserProfile` table in PostgreSQL:
  - `id` (UUID v4, PK), `email` (UNIQUE indexed NOT NULL, lowercase normalized), `displayName` (NOT NULL, 2–100 chars), `password_hash` (NOT NULL), `createdAt`, `updatedAt`, `lastLoginAt` (nullable), `roles` (string array, default `["user"]`, max 20 elements per OQ-002)
- [ ] Create audit log table: event type, user id, IP, timestamp, outcome; 90-day retention policy; co-write atomicity with relevant `AuthService` operations
- [ ] Create Redis key schema for hashed refresh tokens: key format `rt:{userId}:{tokenId}`, 7-day TTL, revocation support
- [ ] Implement `UserRepo`: `create(profile)`, `findByEmail(email)`, `findById(id)`, `update(id, fields)` — thin CRUD with uniqueness conflict propagation; Phase 1 position enables early integration tests against real PostgreSQL before `AuthService` exists

#### Security Primitives

- [ ] Implement `PasswordHasher`: bcrypt hashing with cost factor 12, abstracted interface for future argon2id migration — NFR-SEC-001, AC-003
- [ ] Implement `JwtService`: RS256 signing/verification with 2048-bit RSA keys, 5-second clock-skew tolerance — NFR-SEC-002, AC-001, AC-010
- [ ] Implement `TokenManager` skeleton: issue access tokens (15-min expiry), issue refresh tokens (7-day TTL stored as hashed values in Redis), revocation support — FR-AUTH-003

#### Per-Phase Wiring Table

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| `PasswordHasher` abstraction | Strategy pattern | bcryptjs at cost 12; future argon2id seam | Phase 1 | Phase 2 login/register/reset |
| `JwtService` signing/verification | Service | RS256 signer, RS256 verifier, key-loading, skew-tolerance validator | Phase 1 | Phase 2 token issuance/validation, Phase 4 reliability |
| `TokenManager` skeleton | Service | `JwtService`, Redis client | Phase 1 (skeleton) | Phase 2 (full wiring), Phase 4 metrics, Phase 5 gates |
| `UserRepo` persistence | Repository | PostgreSQL pg-pool, `UserProfile` schema, audit log co-writes | Phase 1 | Phase 2 `AuthService` operations, Phase 5 migration |
| `AuthService` facade | Orchestrator | `PasswordHasher`, `TokenManager`, `UserRepo`, `JwtService` | Phase 1 (skeleton) | Phase 2 (full wiring), Phase 3 frontend |

#### Unit Tests

- [ ] `PasswordHasher.hash()` produces bcrypt hash with cost factor 12 — NFR-SEC-001
- [ ] `PasswordHasher.verify()` correctly validates correct and incorrect passwords
- [ ] `JwtService.sign()` produces RS256-signed JWT — NFR-SEC-002
- [ ] `JwtService.verify()` rejects expired tokens; accepts valid tokens with ≤ 5s clock skew
- [ ] `TokenManager.issueTokens()` returns `AuthToken` with correct TTLs
- [ ] `TokenManager` stores hashed refresh tokens in Redis with 7-day TTL
- [ ] Benchmark: `PasswordHasher.hash()` completes in < 500ms — Success Criterion 5
- [ ] `UserRepo.create()` persists `UserProfile` and audit log atomically

**Requirements addressed:** FR-AUTH-002, FR-AUTH-003 (primitives), FR-AUTH-005 (primitives), NFR-SEC-001, NFR-SEC-002, AC-001, AC-003, AC-004, AC-005, AC-006.

**Phase gate (M1 → Phase 2):** All unit tests green. `PasswordHasher` benchmark < 500ms. PostgreSQL and Redis connectivity verified. RSA key loading confirmed.

**Parallelization:** `PasswordHasher` and `JwtService` can be developed in parallel; `UserRepo` can proceed alongside both.

---

### Phase 2 — Backend Auth Domain Services and API Surface

**Timeline:** 1.5–2 weeks

**Objective:** Wire `AuthService` facade and implement all six API endpoints with full error handling, rate limiting, and account lockout.

**Milestone — M2:** Backend API functionally complete and internally testable; p95 latency < 200ms locally.

#### AuthService Wiring

- [ ] Wire `AuthService` as facade over `PasswordHasher`, `TokenManager`, `UserRepo` — completes Phase 1 skeleton
- [ ] Implement consistent JSON error format: `{ error: { code, message, status } }` per AC-009 and OQ-error-code ADR
- [ ] Confirm all routes under `/v1/auth/*` per AC-007

#### Endpoint Implementation

- [ ] **POST `/v1/auth/login`** — FR-AUTH-001
  - Validate credentials via `UserRepo` + `PasswordHasher`
  - Return `AuthToken` (200) or 401 — no user enumeration for missing emails
  - Account lockout after 5 failed attempts in 15 minutes (423 response); unlock after 15-minute window
  - Rate limit: 10 req/min per IP (application layer)
  - Write login success/failure to audit log
- [ ] **POST `/v1/auth/register`** — FR-AUTH-002
  - Email uniqueness validation (409 on duplicate)
  - Password strength: ≥ 8 chars, uppercase, number (400 on failure)
  - `PasswordHasher` stores bcrypt hash; `UserRepo` creates `UserProfile` + audit log atomically
  - Rate limit: 5 req/min per IP
- [ ] **GET `/v1/auth/me`** — FR-AUTH-004
  - Bearer JWT authentication middleware: token extraction, `JwtService.verify()`, clock-skew handling per AC-010, user-context injection
  - Returns `UserProfile` (id, email, displayName, roles, createdAt, updatedAt, lastLoginAt)
  - Rate limit: 60 req/min per user
- [ ] **POST `/v1/auth/refresh`** — FR-AUTH-003
  - Validates refresh token via `TokenManager`; rejects expired and revoked tokens
  - Revokes old refresh token; issues new `AuthToken` pair
  - Rate limit: 30 req/min per user
- [ ] **POST `/v1/auth/reset-request`** — FR-AUTH-005, step 1
  - Generates time-limited reset token (1-hour expiry)
  - Sends email via SendGrid; uses template and sender resolved by OQ-003
  - Rate limit: 5 req/min per IP per OQ-005
  - Write reset-request to audit log
- [ ] **POST `/v1/auth/reset-confirm`** — FR-AUTH-005, step 2
  - Validates reset token (rejects expired and used tokens)
  - Updates password hash via `PasswordHasher`
  - Write reset-confirm to audit log
- [ ] Create feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` (OFF by default)

#### Per-Phase Wiring Table

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| Express/Fastify route table | Route registry | Six `/v1/auth/*` endpoints | Phase 2 | Phase 3 frontend, Phase 4 monitoring |
| Rate-limiting middleware chain | Middleware | Per-endpoint limits (10/5/60/30/5 req/min), application lockout | Phase 2 | Phase 2 all endpoints, Phase 4 alert integration |
| Bearer-auth middleware (`/auth/me`) | Middleware | `JwtService.verify()`, clock-skew, user-context injection | Phase 2 | Phase 3 `AuthProvider`, Phase 4 observability |
| Error-response formatter | Middleware | Domain exceptions → HTTP status → JSON serializer per AC-009 | Phase 2 | All auth endpoints, Phase 3 UI error rendering |
| SendGrid email dispatch | External binding | SendGrid API client wired to reset-request handler | Phase 2 | FR-AUTH-005 only |
| Feature-flag registry | Config mechanism | `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH` | Phase 2 (created) | Phase 5 rollout gating |

#### Integration Tests

- [ ] Registration persists `UserProfile` to database — FR-AUTH-002 end-to-end
- [ ] Expired refresh token rejected by `TokenManager` via Redis TTL — FR-AUTH-003
- [ ] Login → lockout after 5 failures → 423 → unlock after 15-minute window
- [ ] Password reset: issue token → send email → confirm with valid token → password updated
- [ ] Password reset with expired token returns 401; with reused token returns 401
- [ ] No user enumeration: wrong email and wrong password return identical 401 response
- [ ] Configure testcontainers for CI (ephemeral PostgreSQL + Redis)

#### Performance Validation

- [ ] Verify p95 login latency < 200ms locally — NFR-PERF-001, Success Criterion 1
- [ ] Verify p95 token refresh latency < 100ms locally — Success Criterion 3

**Requirements addressed:** FR-AUTH-001–005, AC-002, AC-007, AC-009, AC-010.

**Phase gate (M2 → Phase 3):** All integration tests green. p95 latency < 200ms locally. All six endpoints return correct responses. Feature flags created (OFF).

**Parallelization:** Login/register endpoints can be built in parallel with password reset endpoints. SendGrid integration is off critical path.

**Security review checkpoint:** Bearer-auth middleware and token-handling semantics reviewed before Phase 3 begins.

---

### Phase 3 — Frontend Auth Integration and UX Hardening

**Timeline:** 1–1.5 weeks

**Objective:** Build frontend components, wire them to the API, and validate the complete user journey with E2E tests.

**Milestone — M3:** Full user journey works in staging with secure client token handling.

#### Frontend Components

- [ ] Implement `AuthProvider` (React Context):
  - Store `accessToken` in memory only — never localStorage — R-001 mitigation
  - Use HttpOnly cookies for `refreshToken` — R-001 mitigation
  - Silent refresh orchestration for FR-AUTH-003
  - Clear tokens on tab close — R-001 mitigation
  - Expose `UserProfile`, `login()`, `logout()`, `refresh()` methods
- [ ] Implement `LoginPage`:
  - Email/password form; calls POST `/v1/auth/login`
  - Generic error messaging — no user enumeration (same message for wrong email vs wrong password)
  - Lockout and cooldown messaging
  - Props: `onSuccess`, optional `redirectUrl`
  - CAPTCHA hook after repeated failures (contingency path for R-002)
- [ ] Implement `RegisterPage`:
  - Client-side password-strength validation aligned to FR-AUTH-002
  - Calls POST `/v1/auth/register`
  - Props: `onSuccess`, `termsUrl`
  - Post-registration routing
- [ ] Implement `ProfilePage`:
  - Displays `UserProfile` from GET `/v1/auth/me`; requires authentication via protected route guard
- [ ] Implement reset-request and reset-confirm forms for FR-AUTH-005

#### Per-Phase Wiring Table

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| React Router route table | Route registry | `/login` → `LoginPage`, `/register` → `RegisterPage`, `/profile` → `ProfilePage` | Phase 3 | Phase 3 E2E, Phase 5 staged rollout |
| `AuthProvider` context binding | Context/DI | All routes; provides `AuthToken`, `UserProfile`, `login()`, `logout()`, `refresh()` | Phase 3 | `LoginPage`, `RegisterPage`, `ProfilePage`, Phase 5 |
| Protected route guard | HOC/Middleware | Checks `AuthProvider` auth state; redirects unauthenticated users to `/login` | Phase 3 | `ProfilePage` |
| `AuthProvider` auth-state event bindings | Event wiring | Login success, logout, silent refresh scheduler, token-expiry handler, tab-close cleanup | Phase 3 | R-001 mitigation, Phase 5 acceptance testing |
| `LoginPage` callback wiring | Callbacks | `onSuccess`, redirect handler, error renderer, lockout renderer | Phase 3 | FR-AUTH-001, Alpha/Beta acceptance |
| `RegisterPage` callback wiring | Callbacks | `onSuccess`, password-strength validator, terms-link, post-registration routing | Phase 3 | FR-AUTH-002, registration conversion measurement |

#### E2E and Load Tests

- [ ] User registers on `RegisterPage` → logs in on `LoginPage` → views `ProfilePage` — FR-AUTH-001, FR-AUTH-002
- [ ] `AuthProvider` silent refresh: access token expires → automatic refresh → user remains authenticated — FR-AUTH-003
- [ ] Failed login shows generic error; no user enumeration — FR-AUTH-001 AC-003
- [ ] Password reset journey: request form → email link → confirm form → new password accepted
- [ ] Configure Playwright for E2E test execution
- [ ] k6 load test: 500 concurrent login requests — NFR-PERF-002
- [ ] Verify p95 < 200ms under load — NFR-PERF-001

#### Funnel Instrumentation

- [ ] Instrument `RegisterPage` → confirmed account funnel — Success Criterion 6 (> 60% conversion)
- [ ] Instrument `AuthToken` issuance counting — Success Criterion 7 (> 1000 DAU within 30 days of GA)

**Requirements addressed:** FR-AUTH-001–005, R-001 and R-002 mitigation support.

**Phase gate (M3 → Phase 4):** E2E tests pass. k6 load test sustains 500 concurrent logins. Frontend components render correctly. Funnel instrumentation confirmed.

**Parallelization:** `LoginPage`, `RegisterPage`, and `ProfilePage` can be built in parallel. Reset UX can begin while `AuthProvider` is being finalized.

---

### Phase 4 — Observability, Performance, Reliability, and Operational Readiness

**Timeline:** 1 week

**Objective:** Validate that the system can be safely operated and that all NFR gates are measurable *before* production traffic is exposed. Observability is separated from rollout to break the circular dependency: Beta gates require metric evidence (p95 < 200ms, error rate < 0.1%) that can only be evaluated if Prometheus is validated independently.

**Milestone — M4:** System operationally ready for limited production exposure.

#### Metrics and Tracing

- [ ] Configure Prometheus metrics:
  - `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter)
- [ ] Configure OpenTelemetry tracing: spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`
- [ ] Build Grafana dashboards for auth traffic and latency
- [ ] Implement structured logging for all auth events (sensitive fields excluded); verify no token leakage in logs or traces — R-001 roadmap control
- [ ] Implement health check endpoint — NFR-REL-001

#### Alerting

- [ ] Login failure rate > 20% over 5 minutes → P1
- [ ] p95 latency > 500ms → P1
- [ ] `TokenManager` Redis connection failures → P1
- [ ] Redis memory usage > 70% → warning

#### Deployment Configuration

- [ ] Configure Kubernetes HPA: 3 replicas baseline, scale to 10 at CPU > 70%
- [ ] Configure PostgreSQL connection pool: 100 initial, scale to 200 at wait time > 50ms
- [ ] Configure Redis memory: 1 GB initial, scale to 2 GB at > 70% usage
- [ ] Wire API Gateway rate-limit policy set for all six endpoints — R-002 roadmap control, Phase 5 rollout protection

#### Migration Preparation

- [ ] Develop `UserProfile` migration script from legacy auth using schema mapping from OQ-006:
  - Idempotent upsert operations
  - Schema mapping and transformation logic
  - Dry-run validation against staging copy of legacy data
- [ ] Document and test full database backup procedure
- [ ] Validate rollback runbook rehearsal — R-003 roadmap control
- [ ] Test rollback procedure end-to-end:
  1. Disable `AUTH_NEW_LOGIN` → traffic routes to legacy
  2. Smoke test legacy login flow
  3. Root cause investigation via structured logs and traces
  4. If `UserProfile` data corruption: restore from pre-migration backup
  5. Incident notification and 48-hour post-mortem

#### Performance and Reliability Validation

- [ ] Confirm p95 login latency < 200ms under production-like load — NFR-PERF-001
- [ ] Confirm p95 token refresh latency < 100ms — Success Criterion 3
- [ ] Load test: 500 concurrent logins sustain < 200ms p95 — NFR-PERF-002
- [ ] Validate health checks, restart behavior, and staged uptime evidence — NFR-REL-001

#### Operational Assets

- [ ] Publish runbooks:
  - Scenario 1: `AuthService` down
  - Scenario 2: Token refresh failures
  - Scenario 3: Redis unavailability
- [ ] Establish auth-team 24/7 on-call rotation for first 2 weeks post-GA
- [ ] Confirm SLA: P1 alerts acknowledged within 15 minutes

#### Per-Phase Wiring Table

| Named Artifact | Type | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|---|
| Prometheus metrics registry | Metrics exporter | Four counters/histograms | Phase 4 | Grafana dashboards, Phase 5 Beta gates |
| Alert rules configuration | Alert binding | Three P1 rules → PagerDuty/incident channel | Phase 4 | On-call, Phase 5 rollout monitoring |
| OpenTelemetry trace pipeline | Tracing middleware | Spans across full `AuthService` call graph | Phase 4 | Debugging, runbooks |
| API Gateway rate-limit policy | Gateway config | Six endpoint rate limits | Phase 4 | R-002 mitigation, Phase 5 protection |
| Feature flag controller | Rollout mechanism | `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH` | Phase 2 (created) | Phase 5 gating and rollback |

**Requirements addressed:** NFR-PERF-001–002, NFR-REL-001; operational support for R-001, R-002, R-003.

**Phase gate (M4 → Phase 5):** Metrics ingestion confirmed. Alerts routed and tested. Load-test results at target. Rollback rehearsed. Migration dry run complete. Staging acceptance green.

**Environment readiness gate before Phase 5:**
- Rollback rehearsed and documented
- Migration dry run complete against staging data
- Staging acceptance green on all M3 criteria

---

### Phase 5 — Migration, Staged Rollout, and GA Cutover

**Timeline:** 4 weeks total (Alpha 1 week, Beta 2 weeks, GA 1 week)

**Objective:** Migrate safely from legacy auth using phased exposure, measurable gates, and full rollback readiness throughout.

**Milestones — M5A / M5B / M5C:** Alpha passes, Beta meets all metric gates, GA achieves 99.9% uptime.

#### Migration Execution

- [ ] Execute idempotent upsert migration for `UserProfile` using script validated in Phase 4
- [ ] Full database backup before each rollout stage
- [ ] Run parallel systems during Alpha and Beta; keep legacy auth alive until GA stability confirmed — R-003 roadmap control

#### Internal Alpha (Week 1)

- [ ] Deploy to staging behind `AUTH_NEW_LOGIN` flag (OFF for public traffic)
- [ ] auth-team and QA manually test all FR-AUTH-001 through FR-AUTH-005
- [ ] Monitor p95 latency, error rate, Redis connection stability using Phase 4 metrics
- [ ] **M5A gate:** Zero P0/P1 bugs. All manual test cases pass.

#### Beta 10% (Weeks 2–3)

- [ ] Enable `AUTH_NEW_LOGIN` for 10% of traffic
- [ ] Monitor: p95 latency < 200ms, error rate < 0.1%, no Redis connection failures from `TokenManager`
- [ ] Monitor login failure rate during Beta — R-002 roadmap control
- [ ] Review registration funnel conversion rate — Success Criterion 6
- [ ] **M5B gate:** All metrics within thresholds for full 2-week period.

#### General Availability (Week 4)

- [ ] Remove `AUTH_NEW_LOGIN` feature flag — 100% traffic to new `AuthService`
- [ ] Deprecate legacy auth routing
- [ ] Enable `AUTH_TOKEN_REFRESH` for all users
- [ ] **M5C gate:** 99.9% uptime over first 7 days — NFR-REL-001, Success Criterion 4
- [ ] Remove `AUTH_TOKEN_REFRESH` flag 2 weeks post-GA
- [ ] Deliver legacy deprecation plan and cleanup tasks

**Requirements addressed:** All FR-AUTH-*, all NFR-*, R-003; full rollout requirements.

---

## Integration Points

The following mechanisms require explicit wiring ownership. Developers get per-phase context (tables above); this section provides the system-topology view confirming `TokenManager` wiring is consistent across the three phases that touch it.

### Dependency Injection and Service Composition

1. **`AuthService` constructor dependency graph** — Wired: `PasswordHasher`, `TokenManager`, `UserRepo`. Owning Phase: 2. Consumed by: Phase 2 API handlers, Phase 4 tracing, Phase 5 production rollout.
2. **`TokenManager` constructor dependency graph** — Wired: `JwtService`, Redis client. Owning Phase: 2. Consumed by: FR-AUTH-001, FR-AUTH-003, Phase 4 metrics, Phase 5 rollout gates.
3. **`UserRepo` persistence wiring** — Wired: PostgreSQL pool, `UserProfile` schema mappings, audit log co-write. Owning Phase: 1. Consumed by: Phase 2 `AuthService` operations, Phase 5 migration.

### Middleware and Request Pipeline Wiring

1. **Bearer-auth middleware chain (`/v1/auth/me`)** — Wired: token extraction, `JwtService.verify()`, clock-skew handling per AC-010, user-context injection. Owning Phase: 2. Consumed by: FR-AUTH-004, Phase 4 observability, Phase 5 rollout.
2. **Error-response middleware/formatter** — Wired: domain exceptions, HTTP status mapping, JSON serializer per AC-009. Owning Phase: 2. Consumed by: all auth endpoints, Phase 3 UI error rendering.
3. **API Gateway rate-limit policy set** — Wired: all six `/auth/*` endpoints. Owning Phase: 4. Consumed by: Phase 5 rollout protection, R-002 mitigation.

### Frontend Callback and Event Wiring

1. **`AuthProvider` auth-state event bindings** — Wired: login success, logout, silent refresh scheduler, token-expiry handler, tab-close cleanup. Owning Phase: 3. Consumed by: `LoginPage`, `RegisterPage`, `ProfilePage`, R-001 mitigation.
2. **`LoginPage` callback wiring** — Wired: `onSuccess`, redirect handler, generic error renderer, lockout-state renderer. Owning Phase: 3. Consumed by: FR-AUTH-001, Alpha/Beta acceptance.
3. **`RegisterPage` callback wiring** — Wired: `onSuccess`, password-strength validator, terms-link, post-registration routing. Owning Phase: 3. Consumed by: FR-AUTH-002, registration conversion measurement.

### Feature-Flag and Rollout Wiring

1. **`AUTH_NEW_LOGIN`** — Wired: `LoginPage`, new auth backend routing, rollout cohort control. Created Phase 2. Consumed by: Alpha, Beta 10%, GA cutover.
2. **`AUTH_TOKEN_REFRESH`** — Wired: `TokenManager` refresh flow, `AuthProvider` silent refresh path. Created Phase 2. Consumed by: Beta monitoring, post-GA stabilization.

### Strategy and Abstraction Wiring

1. **`PasswordHasher` algorithm abstraction** — Wired: bcryptjs at cost 12, future argon2id migration seam per AC-003. Owning Phase: 1. Consumed by: Phase 2 login/register/reset, Phase 4 benchmark validation.
2. **`JwtService` signing/verification strategy** — Wired: RS256 signer, RS256 verifier, key-loading mechanism, skew-tolerance validator. Owning Phase: 1. Consumed by: Phase 2 token issuance/validation, Phase 4 reliability validation.

---

## Risk Assessment

### R-001 — Token Theft via XSS Allows Session Hijacking

**Architectural significance:** Highest-impact client-side risk; undermines all authenticated flows.

**Mitigation:**
1. Keep access tokens in memory only — never localStorage.
2. Use HttpOnly cookies for refresh tokens.
3. Minimize access-token lifetime to 15 minutes per FR-AUTH-003.
4. Clear in-memory auth state on tab close in `AuthProvider`.
5. Review all frontend pages for unsafe token exposure in logs, storage, and error telemetry.

**Roadmap controls:** Phase 3 implements token handling and cleanup semantics. Phase 4 validates no token leakage in logs/traces. Phase 5 includes revocation runbook testing.

**Contingency:** Immediate refresh-token revocation via `TokenManager`. Force password reset for impacted users. Use audit logs to identify blast radius.

---

### R-002 — Brute-Force Attacks on Login Endpoint

**Architectural significance:** High probability, medium impact; directly tied to auth perimeter exposure.

**Mitigation:**
1. API Gateway limit of 10 req/min per IP on `/auth/login` (Phase 4).
2. Account lockout after 5 failed attempts in 15 minutes for FR-AUTH-001 (Phase 2).
3. bcrypt cost 12 for offline resistance via NFR-SEC-001.
4. Explicit rate limits on reset endpoints per OQ-005 resolution (Phase 0 decision, Phase 2 implementation).
5. CAPTCHA hook after repeated failures as contingency path in `LoginPage`.

**Roadmap controls:** Phase 2 implements lockout logic and audit tracking. Phase 4 wires gateway controls and alerting. Phase 5 watches login failure rate during Beta.

**Contingency:** WAF IP blocks. CAPTCHA escalation on `LoginPage`. Incident triage using `auth_login_total` and audit events.

---

### R-003 — Data Loss During Migration from Legacy Auth

**Architectural significance:** Lower probability but release-blocking if mishandled.

**Mitigation:**
1. Idempotent upserts for user migration.
2. Parallel systems during Alpha and Beta.
3. Verified backups before each migration stage.
4. Dry-run schema transformation before production traffic.
5. Defer legacy shutdown until GA success criteria are stable.

**Roadmap controls:** Phase 5 owns migration execution. Phase 4 validates rollback runbook. Phase 0 resolves OQ-006 scope and migration artifact design.

**Contingency:** Disable `AUTH_NEW_LOGIN`. Re-route to legacy auth. Restore from known-good backup if corruption detected.

---

### R-004 — RSA Key Compromise or Rotation Failure

**Architectural significance:** Medium. A compromised private key invalidates all active sessions and allows arbitrary token forgery; an unplanned key rotation without dual-key support causes immediate auth outage.

**Mitigation:**
1. Store RSA private key in secrets manager, never on filesystem.
2. Document manual rotation procedure with dual-key window during transition — OQ-004.
3. Load public key from configurable path to allow zero-downtime key rollover.
4. Plan automated rotation for v1.1.

**Roadmap controls:** Phase 1 establishes key-loading mechanism and secrets storage. Phase 0 produces ADR for rotation procedure. Phase 4/5 operational runbooks include key rotation scenario.

**Contingency:** Rotate key via emergency procedure. Force re-authentication for all active sessions by flushing Redis refresh tokens. Notify auth-team on-call within 15 minutes per SLA.

---

### R-005 — Redis Single Point of Failure for Refresh Tokens

**Architectural significance:** Medium. Redis unavailability terminates all active refresh token flows; users must re-authenticate. At scale this becomes a wide-impact session outage.

**Mitigation:**
1. Degrade gracefully: Redis unavailability surfaces as "session expired, please re-login" rather than a hard error.
2. Monitor Redis health with dedicated P1 alert on connection failure rate.
3. Evaluate Redis Sentinel or Cluster for high-availability during Phase 4 infrastructure planning.

**Roadmap controls:** Phase 1 provisioning decision: document single-node vs. HA choice and its SLA implications. Phase 4 configures Redis failure alert and adds Redis recovery to runbooks. Phase 5 Beta validates Redis stability under real traffic before GA.

**Contingency:** If Redis fails during rollout, disable `AUTH_TOKEN_REFRESH` flag and route all token exchange to re-authentication. Provision Redis Sentinel if failure rate exceeds acceptable threshold.

---

### R-006 — SendGrid Outage Blocks Password Reset

**Architectural significance:** Low. FR-AUTH-005 is the only consumer. Login, registration, and token refresh are unaffected.

**Mitigation:**
1. Queue reset emails for retry on SendGrid API failure.
2. Alert on SendGrid API failures with dedicated non-P1 alert.
3. Resolve OQ-003 (sender identity verification, 2–5 day lead time) before Phase 2 begins.

**Roadmap controls:** Phase 2 integrates SendGrid with retry logic. Phase 4 configures SendGrid failure alerting. Phase 5 Beta confirms reset flow is exercised before GA.

**Contingency:** Surface "email sending delayed, please retry in a few minutes" UX on reset-request form. Manually re-queue failed sends from email provider dashboard.

---

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Phase Needed | Provisioning Lead Time | Risk if Delayed |
|---|---|---|---|
| PostgreSQL 15+ | Phase 1 (Week 1) | ~1 day (Docker local); ~1 week (managed cloud) | Blocks all data persistence and `UserRepo` work |
| Redis 7+ | Phase 1 (Week 1) | ~1 day (Docker local); ~1 week (managed cloud) | Blocks `TokenManager` implementation; Beta cannot start without stable Redis metrics |
| Node.js 20 LTS | Phase 1 (Week 1) | Minimal | Blocks all backend work |
| bcryptjs | Phase 1 (Week 1) | npm install | Blocks `PasswordHasher` |
| jsonwebtoken | Phase 1 (Week 1) | npm install | Blocks `JwtService` |
| SendGrid API | Phase 2 (Week 3) | 2–5 days for sender identity verification (OQ-003) | Blocks FR-AUTH-005 only; non-critical path but must resolve before Phase 2 end |

### Team Roles

| Role | Phase(s) | Responsibility |
|---|---|---|
| Backend engineers | 0–5 | `AuthService`, `TokenManager`, `JwtService`, `UserRepo`, API endpoints, migration tooling |
| Frontend engineers | 3, 5 | `AuthProvider`, `LoginPage`, `RegisterPage`, `ProfilePage`, reset UX |
| Platform/DevOps | 0, 1, 4, 5 | PostgreSQL/Redis provisioning, secret management, TLS, feature-flag delivery, monitoring, alerts |
| QA | 2–5 | Integration tests, E2E tests, manual Alpha testing, rollout gate verification |
| Security reviewer | 0, 2, 4 | RS256 key lifecycle ADR (Phase 0), bearer-auth and token-handling review (Phase 2 gate), token-leakage validation (Phase 4 gate) |

### Operational Dependencies

1. Feature-flag infrastructure
2. APM / OpenTelemetry
3. Prometheus and Grafana
4. Health-check endpoint monitoring
5. CI with ephemeral PostgreSQL and Redis (testcontainers)
6. Staging environment mirroring production topology
7. k6 load-test environment

---

## Success Criteria and Validation

### Functional Validation by Requirement

| Requirement | Unit | Integration | E2E | Gate |
|---|---|---|---|---|
| FR-AUTH-001 | Valid/invalid credential handling | Login endpoint, lockout, audit | `LoginPage` journey | M2, M3, M5B |
| FR-AUTH-002 | Password policy, duplicate-email | Database persistence | Full registration journey | M2, M3, M5B |
| FR-AUTH-003 | Token issuance/refresh/revocation | Redis-backed expiration | Silent refresh via `AuthProvider` | M2, M3, M5B |
| FR-AUTH-004 | — | Bearer token validation, `/auth/me` | Profile rendering after login | M2, M3 |
| FR-AUTH-005 | Reset token issue/consume/expire | End-to-end reset flow | Password reset journey | M2, M3, M5B |

### NFR Validation

| Requirement | Method | Gate |
|---|---|---|
| NFR-PERF-001: p95 < 200ms | APM spans on `AuthService.login()` | M2 (local), M5B (production) |
| NFR-PERF-002: 500 concurrent logins | k6 load test | M3, M4 |
| NFR-REL-001: 99.9% uptime | Health check monitoring, 7-day window | M5C |
| NFR-SEC-001: bcrypt cost 12 | Benchmark + unit tests on `PasswordHasher` | M1 |
| NFR-SEC-002: RS256 2048-bit | Config verification + sign/verify tests on `JwtService` | M1 |

### Success Criteria Mapping

| # | Criterion | Target | Validation Phase | Method |
|---|---|---|---|---|
| 1 | Login p95 latency | < 200ms | M2 local, M5B production | APM on `AuthService.login()` |
| 2 | Registration success rate | > 99% | M5B | Ratio of 201 to total POST `/auth/register` |
| 3 | Token refresh p95 latency | < 100ms | M2 local, M5B production | APM on `TokenManager.refresh()` |
| 4 | Service availability | 99.9% uptime | M5C (7-day window) | Health check monitoring |
| 5 | Password hash time | < 500ms | M1 | Benchmark of `PasswordHasher.hash()` |
| 6 | Registration conversion | > 60% | Post-M5B (30-day window) | Funnel analytics from `RegisterPage` |
| 7 | Daily active authenticated users | > 1000 within 30 days of GA | M5C + 30 days | `AuthToken` issuance counts |

### Validation Stages

| Stage | Description | Required For |
|---|---|---|
| A — Unit/integration completeness | All unit and integration tests green | M2 |
| B — E2E and staging acceptance | E2E tests pass; load tests pass | M3 |
| C — Observability and load evidence | Dashboards live; alerts routed; runbooks tested | M4 |
| D — Alpha/Beta/GA gate review | Metric gates met at each rollout stage | M5A, M5B, M5C |

---

## Timeline and Sequencing

### Phase Timeline

| Phase | Description | Duration | Cumulative |
|---|---|---|---|
| Phase 0 | Architecture baseline and delivery controls | 3–5 working days | Days 1–5 |
| Phase 1 | Core infrastructure, persistence, and security primitives | 1–1.5 weeks | Weeks 1–2 |
| Phase 2 | Backend auth domain services and API surface | 1.5–2 weeks | Weeks 3–4 |
| Phase 3 | Frontend auth integration and UX hardening | 1–1.5 weeks | Weeks 5–6 |
| Phase 4 | Observability, performance, reliability, and operational readiness | 1 week | Week 6–7 |
| Phase 5a | Internal Alpha | 1 week | Week 7–8 |
| Phase 5b | Beta 10% | 2 weeks | Weeks 8–9 |
| Phase 5c | General Availability | 1 week | Weeks 10–11 |

**Total program duration:** ~9–11 weeks (engineering implementation through staging: ~5–7 weeks; rollout and stabilization: ~4 weeks).

### Parallelization Opportunities

- **Phase 1:** `PasswordHasher` and `JwtService` in parallel; `UserRepo` alongside both.
- **Phase 2:** Login/register endpoints in parallel with password reset endpoints. SendGrid integration is off critical path.
- **Phase 3:** `LoginPage`, `RegisterPage`, and `ProfilePage` in parallel. Reset UX begins while `AuthProvider` is being finalized. Phase 4 observability setup can begin in the final days of Phase 3.
- **Phase 5:** Migration script development overlaps with Alpha testing.

### Sequencing Constraints

1. Do not start frontend token orchestration before `JwtService`, `TokenManager`, and error semantics are stable (M2 achieved).
2. Do not expose Beta traffic until: Redis failure alerts are live, rollback is rehearsed, and reset endpoints have explicit rate limits.
3. Do not remove legacy auth until GA stability (M5C) is proven; do not compress Alpha/Beta/GA into a single release motion.
4. Treat OQ-003 (SendGrid sender identity), OQ-004 (RSA rotation), OQ-005 (reset rate limits), and OQ-006 (migration schema) as release-relevant — each must be resolved before the phase that consumes it.
5. Do not begin Phase 5 until observability is independently validated in Phase 4; the Beta gate metric thresholds require working Prometheus — this is a hard sequencing dependency, not a style preference.
