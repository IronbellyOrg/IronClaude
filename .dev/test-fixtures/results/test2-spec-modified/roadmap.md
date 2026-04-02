---
spec_source: test-spec-user-auth.md
complexity_score: 0.62
adversarial: true
---

# Project Roadmap: User Authentication Service v1.0
## Merged Final — Adversarial Synthesis (Base: Variant B + Variant A Grafts)

---

## 1. Executive Summary

This roadmap delivers a production-ready JWT-based authentication subsystem with five scoped capabilities: `FR-AUTH.1` login, `FR-AUTH.2` registration, `FR-AUTH.3` stateful refresh token rotation with replay detection, `FR-AUTH.4` authenticated profile retrieval, and `FR-AUTH.5` password reset. The architecture is security-critical but bounded, with medium implementation complexity (0.62) driven primarily by RS256 key management, bcrypt performance/security tradeoffs, stateful token rotation correctness, and open-question closure.

### Architectural Priorities

1. **Security correctness first** — `NFR-AUTH.3`, `RISK-1`, and `RISK-2` are release gates, not backlog polish. Emergency rotation capability and threshold-based replay anomaly alerting are v1.0 scope.
2. **Stateful refresh control inside a stateless JWT model** — database-backed hashed refresh-token records satisfy `FR-AUTH.3 AC-4` and `SC-8` without compromising stateless access-token validation.
3. **Phased rollout with operational safeguards** — `AUTH_SERVICE_ENABLED` feature flag, secrets-manager integration, health checks, and observability must be in place before full traffic exposure.
4. **Open-question closure as a delivery dependency** — `OQ-1`, `OQ-2`, `OQ-6`, `OQ-7`, and `OQ-8` materially affect implementation and must be resolved during Phase 0 with explicit defaults when stakeholders do not decide in time.

### Known Constraint Conflict

The NFR-AUTH.1 latency target (< 200ms p95) is structurally at tension with bcrypt cost factor 12 (~250ms for the hash operation alone). This is the most likely delivery failure mode for v1.0. To contain the risk, an isolated benchmark of the full login code path is added as a Phase 1 task — before service-layer composition begins — so course correction (cost factor tuning, architecture changes, or SLO renegotiation) is available early. The full k6 load test in Phase 4 validates the end-to-end path under production-representative load.

### Delivery Outcome

By the end of this roadmap, the system will:
- Authenticate users with email/password and RS256 JWTs (`FR-AUTH.1`)
- Register users with strong validation and bcrypt hashing (`FR-AUTH.2`, `NFR-AUTH.3`)
- Rotate refresh tokens with replay detection and full-user revocation on reuse (`FR-AUTH.3`, `SC-8`)
- Expose authenticated profile retrieval without sensitive fields (`FR-AUTH.4`)
- Support secure password reset with session invalidation (`FR-AUTH.5`)
- Meet all validation thresholds in `SC-1` through `SC-8`

---

## 2. Phased Implementation Plan

### Phase 0: Architecture Finalization and Delivery Readiness

**Duration**: 2–3 working days
**Goal**: Close blocking architectural questions, lock interfaces and data model, prevent mid-implementation churn.

#### 0.1 Open Question Resolution

- [ ] **OQ-7**: Select secrets manager platform (AWS Secrets Manager / HashiCorp Vault / GCP Secret Manager). Determines key injection mechanism for `jwt-service.ts` and deployment pipeline.
- [ ] **OQ-1 / OQ-6**: Select email service provider; define interface contract, retry policy, SLA, and failure behavior. Synchronous vs. async dispatch decision impacts endpoint latency and infrastructure requirements.
- [ ] **OQ-2**: Define maximum concurrent active refresh tokens per user. Impacts `RefreshToken` table schema, indexing strategy, and revocation blast radius.
- [ ] **OQ-8**: Decide concurrent refresh rotation behavior — idempotency window vs. accepted false-positive invalidation. Assign a technically sound default (transactional rotation) for Phase 2 implementation; if the decision owner selects an idempotency window approach instead, this default must be revisited before Phase 2 implementation begins. Record assigned default explicitly.
- [ ] **OQ-3**: Confirm account lockout policy scope (v1.0 or v1.1). If v1.0: progressive lockout extends Phase 2 scope and addresses RISK-4. If v1.1: document residual gap explicitly.
- [ ] **OQ-4**: Confirm authentication audit logging scope (v1.0 or v1.1). Most likely v1.1; record decision owner and target version.
- [ ] **OQ-5**: Confirm token revocation on user deletion scope (v1.0 or v1.1). Record decision with RISK-5 gap acknowledgment if deferred.
- [ ] **Emergency rotation policy questions** (supporting Phase 4 runbook): Decide whether emergency key rotation invalidates all active sessions, and what the blast radius scope is. These are architectural questions that may affect `TokenManager` design; resolve here, before Phase 1 implementation begins.

#### 0.2 Interface and Data Model Lockdown

- [ ] Approve canonical component interfaces: `PasswordHasher`, `JwtService`, `TokenManager`, `AuthService` orchestration contract
- [ ] Approve request/response DTOs for all `/auth/*` endpoints
- [ ] Finalize `User` table fields required by `FR-AUTH.2` and `FR-AUTH.4`
- [ ] Finalize `RefreshToken` table schema required by `FR-AUTH.3 AC-4`; schema depends on OQ-2 resolution
- [ ] Finalize reset-token persistence model or token-derivation approach for `FR-AUTH.5`

#### 0.3 Infrastructure and Rollout Policy

- [ ] Generate RS256 key pair; store private key in selected secrets manager
- [ ] Configure key rotation automation (90-day period)
- [ ] Provision or configure email service credentials and sandbox
- [ ] Define `AUTH_SERVICE_ENABLED` feature flag semantics
- [ ] Confirm k6 and APM tooling availability for Phase 4 NFR validation

**Milestone M0**: Architecture signoff complete — all blocking OQs have assigned decisions or approved defaults; interface contracts and migration shape are frozen; emergency rotation policy questions resolved.

---

### Phase 1: Security Foundations and Core Infrastructure

**Duration**: 4–6 working days
**Goal**: Build cryptographic and token primitives correctly; establish secrets and configuration wiring; create persistence foundations for auth state.

**Implementation order follows the specification's hard dependency chain.**

#### 1.1 bcrypt Latency Benchmark (Earliest Risk Signal)

Before building the full service path, validate the latency constraint early:

- [ ] Implement `password-hasher.ts` (bcrypt, cost factor 12, configurable; see 1.2 below)
- [ ] Run a benchmark of the **full expected login code path** — hash operation + database read + token signing — not just the hash in isolation
- [ ] Assert p95 against the 200ms budget (`SC-1`, `NFR-AUTH.1`)
- [ ] If 200ms is infeasible: evaluate cost factor tuning, connection pooling, or async optimizations before Phase 2 begins. Escalate SLO renegotiation if no code-path solution is viable.

This task produces an early signal; full k6 load validation under representative concurrency occurs in Phase 4.

#### 1.2 Password Hasher — `password-hasher.ts`

**Covers**: `FR-AUTH.1`, `FR-AUTH.2`, `FR-AUTH.5`; `NFR-AUTH.3`

- [ ] bcrypt cost factor 12 (`NFR-AUTH.3`)
- [ ] Configurable cost factor (RISK-3 mitigation: future Argon2id migration path)
- [ ] Unit tests: cost factor verification, hash timing ≈ 250ms (`SC-3`), valid/invalid password verification, password policy enforcement (`FR-AUTH.2 AC-3`)

#### 1.3 JWT Service — `jwt-service.ts` (parallel with 1.4)

**Covers**: `FR-AUTH.3`, `FR-AUTH.4`; `NFR-AUTH.1`

- [ ] RS256 signing and verification; key from secrets manager (`RISK-1`, OQ-7 decision)
- [ ] Access token TTL = 15 minutes (`SC-5`)
- [ ] Refresh token TTL = 7 days (`SC-5`)
- [ ] Reset token TTL = 1 hour (`SC-7`)
- [ ] Unit tests: generation/decode round-trip, TTL assertions, expired token rejection, invalid/tampered token rejection, RS256 verification

#### 1.4 Token Manager — `token-manager.ts` (parallel with 1.3)

**Covers**: `FR-AUTH.3` lifecycle; consumed by `FR-AUTH.1`, `FR-AUTH.4`, `FR-AUTH.5`

- [ ] Token issuance and refresh token hash storage (`FR-AUTH.3 AC-4`)
- [ ] Refresh token rotation: invalidate previous, issue new (`FR-AUTH.3 AC-1`)
- [ ] Replay detection: reuse of revoked token → revoke-all-for-user (`FR-AUTH.3 AC-3`, `SC-8`)
- [ ] Enforce max active refresh tokens per user (OQ-2 decision)
- [ ] Session revocation primitive for password reset (`FR-AUTH.5 AC-4`)
- [ ] Unit tests: issuance and hash storage, rotation produces new and invalidates old, replay detection triggers full revocation, expired token rejection, concurrent rotation behavior (per OQ-8 decision)

#### 1.5 Migration — `003-auth-tables.ts`

- [ ] User table additions/creation
- [ ] RefreshToken table (schema reflects OQ-2 decision)
- [ ] Reset token persistence if stored server-side
- [ ] Reversible down-migration; validate rollback in dev environment

#### 1.6 Configuration and Feature Plumbing

- [ ] `AUTH_SERVICE_ENABLED` guard
- [ ] bcrypt cost configuration
- [ ] Key rotation configuration metadata
- [ ] Email service configuration placeholders

#### Integration Points — Phase 1

| Named Artifact | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|
| `TokenManager` token lifecycle registry | Access-token issuer, refresh-token issuer, hash persistence, user-wide revocation, reset-triggered session revocation | Phase 1 | Phase 2 (`auth-service.ts`), Phase 3 (routes), Phase 5 (validation) |
| Configuration binding | `password-hasher.ts`, `jwt-service.ts`, `token-manager.ts`, route registration guard | Phase 1 | Phase 3 (rollout gating), Phase 6 (operations) |
| Database migration `003-auth-tables.ts` | User table, RefreshToken table schemas | Phase 1 | Phase 1.4 (data access), Phase 2 (all auth flows) |
| Secrets manager integration | RSA private key injected into `JwtService` at startup | Phase 0 (provisioned), Phase 1.3 (consumed) | Phase 2 (token signing), Phase 4 (key rotation) |

**Milestone M1**: Security primitives and persistence foundation complete — cryptographic components pass unit tests, migration is reversible, secrets wiring functional in non-production, bcrypt/latency benchmark result documented.

---

### Phase 2: Service-Layer Orchestration and Domain Logic

**Duration**: 5–7 working days
**Goal**: Centralize auth behavior in `AuthService`; implement all business rules and security responses; keep internal components non-HTTP-facing.

#### 2.1 Auth Service — `auth-service.ts`

**Covers**: `FR-AUTH.1`, `FR-AUTH.2`, `FR-AUTH.3`, `FR-AUTH.5`

- [ ] **Registration flow** (`FR-AUTH.2`): email format validation, password policy enforcement, duplicate email detection → 409, user record creation → 201
- [ ] **Login flow** (`FR-AUTH.1`): credential verification, token issuance, generic error on invalid credentials (must not reveal which field was wrong), locked-account response → 403, IP rate-limit hook integration for `FR-AUTH.1 AC-4`. If OQ-3 resolved as v1.0: progressive account lockout (RISK-4 mitigation)
- [ ] **Token refresh flow** (`FR-AUTH.3`): valid token → new access + rotated refresh; expired token → 401; replayed revoked token → full user invalidation. Implement transactional rotation as the default for OQ-8 (see Phase 0 qualifier); revisit if decision owner selects idempotency window
- [ ] **Password reset flow** (`FR-AUTH.5`): reset token generation and email dispatch, 1-hour TTL (`SC-7`); reset token consumption and password update; expired/invalid token → 400; global session invalidation on success

#### 2.2 Email Delivery Adapter

- [ ] Wire selected email provider client (OQ-1/OQ-6 decisions)
- [ ] Implement retry/failure policy per contract defined in Phase 0
- [ ] Synchronous vs. async dispatch mode per OQ-1 resolution

#### Integration Points — Phase 2

| Named Artifact | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|
| `AuthService` orchestration dispatch | `PasswordHasher`, `JwtService`, `TokenManager`, user repository, refresh token repository, email adapter, login rate-limiter | Phase 2 | Phase 3 (route handlers, middleware-protected profile retrieval) |
| Password reset delivery adapter | Email provider client, reset template payload builder, retry/failure policy (OQ-1/OQ-6) | Phase 2 | Phase 3 (`/auth/password-reset/request` endpoint), Phase 5 (failure-path tests) |
| Login rate-limit binding | IP-based rate-limiter, login endpoint service call | Phase 2 | Phase 3 (route registration), Phase 5 (`SC-4` validation) |

**Milestone M2**: Auth domain logic complete — all primary flows work through service-level tests; replay detection and reset session invalidation semantics are verified.

---

### Phase 3: HTTP Surface, Middleware Integration, and Feature-Flagged Exposure

**Duration**: 3–4 working days
**Goal**: Expose required `/auth/*` HTTP surface; integrate with existing middleware; preserve existing unauthenticated system behavior during phased rollout.

#### 3.1 Auth Middleware — `auth-middleware.ts`

**Covers**: `FR-AUTH.4`

- [ ] Bearer token extraction and verification via `TokenManager`
- [ ] Valid token → attach user context to request
- [ ] Invalid/expired token → 401 (`FR-AUTH.4 AC-2`)
- [ ] Integrate into existing `src/middleware/auth-middleware.ts` — no new middleware framework

#### 3.2 Routes and Migration Application

- [ ] Register routes in `src/routes/index.ts` under `/auth/*`:
  - `POST /auth/login` (`FR-AUTH.1`)
  - `POST /auth/register` (`FR-AUTH.2`)
  - `POST /auth/refresh` (`FR-AUTH.3`)
  - `GET /auth/profile` (`FR-AUTH.4`) — protected by auth middleware
  - `POST /auth/password-reset/request` + `POST /auth/password-reset/confirm` (`FR-AUTH.5`)
- [ ] `AUTH_SERVICE_ENABLED` feature flag gates all new routes; existing unauthenticated endpoints unaffected
- [ ] Apply migration `003-auth-tables.ts`; verify down-migration rollback
- [ ] Refresh token delivered via httpOnly cookie (XSS/CSRF mitigation)
- [ ] Sensitive fields (`password_hash`, `refresh_token_hash`) excluded from profile response (`FR-AUTH.4 AC-3`)

#### Integration Points — Phase 3

| Named Artifact | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|
| Route registry (`src/routes/index.ts`) | `/auth/*` route group wired to `AuthService` methods, feature-flag guard | Phase 3 | Phase 4 (performance instrumentation), Phase 5 (E2E validation) |
| Auth middleware chain (`src/middleware/auth-middleware.ts`) | `TokenManager.verify()`, `JwtService` verification, user context injection | Phase 3 | Phase 3 (`/auth/profile` route), all future authenticated endpoints |
| HTTP cookie/response binding | Refresh-token issuance path, rotation path, cookie flags and expiry alignment | Phase 3 | Phase 5 (integration/E2E for `FR-AUTH.1`, `FR-AUTH.3`) |

#### Integration Tests (Phase 3 exit gate)

All 5 functional requirements verified against acceptance criteria:

- Login: valid credentials → 200 + tokens; invalid → 401 generic; locked → 403; rate limit → 429 on 6th attempt (`SC-4`)
- Registration: valid → 201; duplicate email → 409; weak password → 400 with policy; invalid email → 400
- Refresh: valid → new tokens; expired → 401; replayed revoked → full invalidation (`SC-8`)
- Profile: valid token → user data without sensitive fields; expired/invalid → 401
- Password reset: registered email → dispatch; valid reset token → changed + sessions invalidated; expired → 400 (`SC-7`)
- Feature flag toggle verified (on/off)

**Milestone M3**: Auth API surface available behind feature flag — endpoints respond correctly in integration environment; middleware gating and response contracts stable.

---

### Phase 4: Reliability, Performance, and Operational Hardening

**Duration**: 4–5 working days
**Goal**: Prove the auth subsystem meets non-functional targets; establish operational controls for uptime and key hygiene.

#### 4.1 Performance Validation

- [ ] k6 load tests: login, refresh, profile retrieval p95 latency under normal load (`NFR-AUTH.1`, `SC-1`)
  - Profile full login code path; bcrypt (~250ms) is the dominant contributor against the 200ms budget
  - If Phase 1.1 benchmark flagged feasibility risk, execute any already-identified mitigations here
  - If target not met: evaluate bcrypt cost factor tuning, connection pooling, or async optimizations
- [ ] Verify bcrypt hash timing benchmark (`SC-3`)
- [ ] Set up APM dashboard for production latency monitoring

#### 4.2 Availability Validation

- [ ] Health check integration (`NFR-AUTH.2`, `SC-2`)
- [ ] PagerDuty alerting for auth service degradation
- [ ] Degraded dependency behavior, especially for email service paths

#### 4.3 Key Management Operationalization

**Covers**: RISK-1 full mitigation chain

- [ ] Validate 90-day key rotation procedure is functional
- [ ] Produce emergency key rotation runbook (policy decisions resolved in Phase 0): documents blast radius, session invalidation scope, communication procedure
- [ ] Validate public key distribution/verification path
- [ ] Drill: execute emergency rotation in staging; confirm `TokenManager` and active sessions behave per Phase 0 policy decisions

#### 4.4 Replay Anomaly Observability

**Covers**: RISK-2 residual gap (threshold-based, no baseline calibration required)

- [ ] Instrument `revoke-all-for-user` events with deterministic threshold signals: alert when the revoke-all operation triggers more than N times in M seconds for the same user ID (N and M set per OQ-8 policy decision in Phase 0)
- [ ] Wire alert to APM/PagerDuty
- [ ] Document behavior for duplicate concurrent refreshes per OQ-8

#### 4.5 bcrypt Reviewability

- [ ] Config-driven cost factor with `RISK-3` mitigation path documented
- [ ] Annual review runbook entry
- [ ] Benchmark repeatability verified in CI

#### Integration Points — Phase 4

| Named Artifact | Wired Components | Owning Phase | Consumed By |
|---|---|---|---|
| Observability/monitoring binding | Health check endpoint, APM latency dashboard, PagerDuty alerting, k6 test suite outputs | Phase 4 | Phase 6 (production rollout governance, post-release validation) |
| Key rotation operational mechanism | Secrets manager key versioning, `jwt-service.ts` key retrieval, deployment/runtime reload procedure | Phase 4 | Phase 6 (operations), incident response for RISK-1 |
| Replay anomaly threshold signals | revoke-all event counters, alerting bindings | Phase 4 | Phase 6 (monitoring), incident response for RISK-2 |

**Milestone M4**: Non-functional readiness achieved — performance, availability, key-ops controls, and anomaly observability demonstrated in staging/pre-production.

---

### Phase 5: Verification, Security Validation, and Release Readiness

**Duration**: 4–6 working days
**Goal**: Validate every functional and non-functional requirement; prove rollback safety; block launch on any security regression.

#### 5.1 Unit Validation

- [ ] bcrypt cost factor and timing (`SC-3`, `NFR-AUTH.3`)
- [ ] JWT TTLs and RS256 signing algorithm enforcement (`SC-5`, `SC-7`)
- [ ] Email/password validation rules, response filtering helpers

#### 5.2 Integration Validation

- [ ] Registration: happy and conflict paths
- [ ] Login: success, invalid credentials, locked account, rate limiting (`SC-4`)
- [ ] Refresh: success, expiry, replay detection, revocation persistence (`SC-8`)
- [ ] Profile: authenticated retrieval with sensitive-field exclusion
- [ ] Password reset: request, expiry, invalid token, success, session invalidation (`SC-7`)

#### 5.3 End-to-End Validation

- [ ] Client-observable auth flows
- [ ] Cookie behavior for refresh tokens
- [ ] Feature-flag enable/disable paths

#### 5.4 Migration Validation

- [ ] Apply `003-auth-tables.ts`
- [ ] Run down-migration successfully
- [ ] Verify rollback without auth-state corruption

#### 5.5 Release Review

- [ ] Unresolved OQs either closed or explicitly accepted as risks with owner and target version
- [ ] Deferments (`OQ-4`, possibly `OQ-5`) recorded per Section 7 format
- [ ] Security signoff: no open high-severity findings
- [ ] RISK-1 and RISK-2 mitigations verified as implemented, not merely documented

**Milestone M5**: Release approval — all success criteria pass, rollback plan verified, security signoff complete.

---

### Phase 6: Controlled Rollout and Post-Launch Stabilization

**Duration**: 3–5 working days of monitored rollout/stabilization
**Goal**: Minimize blast radius during production introduction; detect regressions quickly; convert operational learnings into next-scope decisions.

#### 6.1 Staged Traffic Enablement

- [ ] Enable `AUTH_SERVICE_ENABLED` in progression: internal/staging → limited production cohort → full production
- [ ] Monitor each stage before advancing: latency and uptime (`SC-1`, `SC-2`), login failure rates, refresh replay/revocation events, password reset email delivery health

#### 6.2 Post-Launch Review

- [ ] Assess need to promote `OQ-3` (lockout policy) into next release
- [ ] Assess need for `OQ-4` (audit logging)
- [ ] Assess need for `OQ-5` (token revocation on user deletion)
- [ ] Assess observed concurrency issues from `OQ-8`
- [ ] Confirm down-migration rollback procedure is documented and tested in production context
- [ ] Remove or archive `AUTH_SERVICE_ENABLED` feature flag after full rollout is stable

**Milestone M6**: Production steady state — full rollout completed with no unresolved Sev-1/Sev-2 auth defects.

---

## 3. Risk Assessment

### Primary Security Risks

| Risk | Severity | Phase Addressed | Mitigation | Residual Gap |
|---|---|---|---|---|
| **RISK-1**: JWT private key compromise | High | Phase 0 (provisioning), Phase 1.3 (implementation), Phase 4.3 (runbook + drill) | RS256 + secrets manager + 90-day rotation + v1.0 emergency rotation runbook | None — v1.0 ships complete mitigation chain |
| **RISK-2**: Refresh token replay attack | High | Phase 1.4 (rotation logic), Phase 3 (integration test SC-8), Phase 4.4 (anomaly alerting) | Token rotation + replay detection + full revocation + threshold-based alerting | Window between theft and first legitimate use — narrowed by Phase 4 observability |
| **RISK-3**: bcrypt cost factor insufficient | Medium | Phase 1.1/1.2 (configurable cost), Phase 4.5 (reviewability) | Configurable cost factor; Argon2id migration path; annual review runbook | No automated cost-factor upgrade — requires manual review |
| **RISK-4**: No progressive account lockout | Medium | Phase 0 (OQ-3 decision), Phase 2 (if in scope) | If v1.0: progressive lockout in `AuthService`; if v1.1: document gap | Distributed brute-force partially mitigated by IP rate limiting regardless |
| **RISK-5**: Token state on user deletion | Medium | Phase 0 (OQ-5 decision) | If v1.0: deletion hook with cascade revocation; if v1.1: document 7-day TTL gap | Depends on whether user deletion is a v1.0 use case |

### Risk Prioritization

**Priority 1 — RISK-1 and RISK-2**: Both enable session hijacking. Both are on the critical path and must be fully mitigated — not merely documented — before v1.0 launch. The release gate explicitly states: RISK-1 and RISK-2 mitigations are implemented, not merely documented.

**Priority 2 — Latency constraint conflict**: The NFR-AUTH.1 (< 200ms p95) vs. bcrypt cost factor 12 (~250ms) tension is the most likely delivery failure mode. Phase 1.1 provides the earliest feasibility signal. Phase 4.1 provides the production-representative validation. If the target proves infeasible, options are: cost factor reduction (security tradeoff requiring security review), code-path optimization, or SLO renegotiation with stakeholders. None of these are week-long rework if caught in Phase 1.

**Priority 3 — Email service dependency (OQ-6)**: Provider selection slippage blocks `FR-AUTH.5` and delays Phase 2 scope finalization. Treat as a schedule risk requiring active stakeholder tracking from Phase 0.

### Delivery Risks from Ambiguity

| Risk | Blocking OQ | Phase Resolution | Mitigation |
|---|---|---|---|
| Email service ambiguity | OQ-1, OQ-6 | Phase 0 | Select provider and delivery mode; bind contract in Phase 2; validate degraded behavior in Phase 4 |
| Secrets manager ambiguity | OQ-7 | Phase 0 | Select platform before Phase 1 begins |
| Concurrent refresh race | OQ-8 | Phase 0 (policy), Phase 2 (implementation) | Assign transactional rotation as default; revisit if idempotency window selected; validate in Phase 5 |

---

## 4. Resource Requirements

### Team Roles

| Role | Responsibilities |
|---|---|
| **Backend engineer** (primary) | Service implementation, routes, middleware, migration, token logic |
| **Security engineer / reviewer** | RS256 usage, secrets management, replay detection, password reset flow, rollout controls, Phase 4.3 runbook drill |
| **Platform / DevOps engineer** | Secrets manager integration, key rotation process, health checks, monitoring, deployment flagging |
| **QA / test engineer** | Integration, concurrency, and E2E validation; k6 performance coverage |
| **Product / architecture owner** | Resolves OQ-1 through OQ-8 — especially scope decisions around lockout, audit logging, and deletion revocation; required before Phase 1 can begin |

### External Dependencies

| # | Dependency | Blocking | Action Required |
|---|---|---|---|
| 1 | `jsonwebtoken` library | Phase 1.3 | Security review and maintenance check before adoption |
| 2 | `bcrypt` library | Phase 1.2 | Standard; validate cost-factor configuration API |
| 3 | RSA key pair (secrets manager) | Phase 0.3 | Select platform; provision keys |
| 4 | Email service | Phase 2.2 | Select provider; define interface contract |
| 5 | User database table | Phase 1.4+ | Migration `003-auth-tables.ts` |
| 6 | RefreshToken database table | Phase 1.4+ | Migration; schema depends on OQ-2 resolution |
| 7 | k6 + APM tooling | Phase 4.1 | Confirm installed; APM dashboard provisioned |

### Parallel Work Opportunities

- Phase 1.3 (`jwt-service.ts`) and Phase 1.4 (`token-manager.ts`) — parallel after interfaces are defined
- Phase 4.1 (performance) and Phase 4.2 (availability) — overlap permitted
- Phase 0 decision resolution and infrastructure provisioning — concurrent

---

## 5. Success Criteria and Validation

### Criteria Traceability

| Criterion | Requirement Source | Phase Validated | Test Type |
|---|---|---|---|
| **SC-1**: Auth endpoint p95 < 200ms | `NFR-AUTH.1` | Phase 1.1 (early signal), Phase 4.1 (full validation) | Unit benchmark + k6 load test + APM |
| **SC-2**: ≥ 99.9% uptime | `NFR-AUTH.2` | Phase 4.2, Phase 6 | Health check monitoring, PagerDuty |
| **SC-3**: Hash timing ≈ 250ms at cost factor 12 | `NFR-AUTH.3` | Phase 1.1, Phase 1.2 | Unit benchmark |
| **SC-4**: Rate limiting 5/min/IP | `FR-AUTH.1 AC-4` | Phase 3 integration tests | Integration: 6th attempt → 429 |
| **SC-5**: Token TTLs correct | `FR-AUTH.1 AC-1`, `FR-AUTH.3 AC-1` | Phase 1.3, Phase 1.4 | Unit: JWT decode + expiry assertion |
| **SC-6**: Password policy enforced | `FR-AUTH.2 AC-3` | Phase 1.2, Phase 3 | Unit + integration: boundary inputs |
| **SC-7**: Reset token 1-hour TTL | `FR-AUTH.5 AC-1` | Phase 3, Phase 5 | Integration: use after expiry → 400 |
| **SC-8**: Replay detection → full revocation | `FR-AUTH.3 AC-3` | Phase 1.4, Phase 3, Phase 4.4 | Unit + integration + observability drill |

### Validation Layers

1. **Unit tests**: crypto primitives, token TTL calculations, validation rules, response filtering helpers
2. **Integration tests**: service + database + token lifecycle, migration correctness, rate limiting, session invalidation after reset
3. **End-to-end tests**: route behavior, cookies and auth headers, feature-flagged enablement, real client-observable flows
4. **Performance and resilience tests**: k6 for latency, dependency degradation scenarios for email service, refresh-race scenarios for OQ-8
5. **Operational validation**: key rotation drill, rollback exercise via down migration, alerting verification

### Release Gates

1. No open high-severity security defects
2. SC-1 through SC-8 all pass
3. RISK-1 and RISK-2 mitigations are **implemented**, not merely documented
4. Emergency key rotation runbook is produced and drilled in staging
5. Feature flag rollback path verified
6. Migration rollback succeeds cleanly

---

## 6. Timeline

| Phase | Name | Estimate |
|---|---|---:|
| Phase 0 | Architecture Finalization and Delivery Readiness | 2–3 working days |
| Phase 1 | Security Foundations and Core Infrastructure | 4–6 working days |
| Phase 2 | Service-Layer Orchestration and Domain Logic | 5–7 working days |
| Phase 3 | HTTP Surface, Middleware Integration, and Feature-Flagged Exposure | 3–4 working days |
| Phase 4 | Reliability, Performance, and Operational Hardening | 4–5 working days |
| Phase 5 | Verification, Security Validation, and Release Readiness | 4–6 working days |
| Phase 6 | Controlled Rollout and Post-Launch Stabilization | 3–5 working days |
| **Total** | | **25–36 working days** |

### Critical Path

1. Resolve OQ-1, OQ-2, OQ-6, OQ-7, OQ-8 (Phase 0) — including emergency rotation policy questions
2. Phase 1 security primitives + bcrypt latency benchmark
3. Phase 2 token rotation, replay logic, and password reset flows
4. Phase 3 routes, middleware, and integration test suite
5. Phase 4 NFR validation, emergency rotation drill, anomaly alerting
6. Phase 5 release gates

### Schedule Risk Notes

Most likely schedule slips, in order:
1. Secrets manager selection and integration (OQ-7)
2. Email service/provider uncertainty (OQ-1, OQ-6)
3. Refresh rotation race-condition handling (OQ-8)
4. Meeting NFR-AUTH.1 while honoring NFR-AUTH.3 — surfaced early by Phase 1.1 benchmark

If schedule compression is required: preserve Phases 1, 2, and 5 intact. Reduce scope by formally deferring unresolved gap items to v1.1 rather than weakening security or validation rigor.

---

## 7. Items Deferred to v1.1 (Confirmed Out of Scope)

The following items are confirmed out of scope for v1.0. Each is recorded with its residual risk or gap acknowledgment:

1. **OAuth2/OIDC federation** — no spec requirement for v1.0
2. **Multi-factor authentication (MFA)** — no spec requirement for v1.0
3. **Role-based access control (RBAC)** — no spec requirement for v1.0
4. **Social login providers** — no spec requirement for v1.0
5. **Authentication audit logging** (OQ-4) — decision owner and target version to be recorded at Phase 0; residual risk: no tamper-evident auth event trail in v1.0
6. **Token revocation on user deletion** (OQ-5 / RISK-5) — if deferred: deleted-user sessions survive until 7-day TTL expiry; document operational workaround (manual revoke-all) and record explicit risk acceptance
7. **Progressive account lockout** (OQ-3) — if deferred: distributed brute-force partially mitigated by IP rate limiting only; document residual RISK-4 gap
8. **Statistical anomaly alerting** — v1.0 ships deterministic threshold-based alerts (Phase 4.4); percentile-based anomaly detection requires production baseline data available after launch
