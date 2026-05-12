---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.65
primary_persona: architect
---

## 1. Executive summary

This roadmap delivers a medium-complexity authentication platform centered on `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo`, and the frontend `AuthProvider`/page flows. The architecture should prioritize security hardening and operational correctness before broad rollout because the highest-risk areas are token lifecycle, brute-force protection, migration safety, and key management.

### Primary architectural objectives
1. Deliver the core user-facing flows required by:
   - `FR-AUTH-001`
   - `FR-AUTH-002`
   - `FR-AUTH-003`
   - `FR-AUTH-004`
   - `FR-AUTH-005`
2. Satisfy the platform constraints and security controls required by:
   - `NFR-PERF-001`
   - `NFR-PERF-002`
   - `NFR-REL-001`
   - `NFR-SEC-001`
   - `NFR-SEC-002`
   - `AC-001` through `AC-010`
3. De-risk rollout by sequencing:
   - infrastructure and secrets first
   - core auth primitives second
   - API and UI integration third
   - testing, migration, and observability before traffic exposure
4. Preserve rollback safety for `R-003` by keeping legacy auth available until GA acceptance is met.

### Architectural priorities
1. **Security-first implementation**
   - Land `AC-001`, `AC-003`, `AC-008`, and `AC-010` before public traffic.
   - Treat refresh token storage and revocation as a critical-path subsystem for `FR-AUTH-003`.
2. **Clear system boundaries**
   - Stateless access-token validation per `AC-002`.
   - Redis-backed refresh lifecycle per `AC-005`.
   - PostgreSQL-backed user and audit persistence per `AC-004`.
3. **Operational readiness before scale**
   - Instrument latency, token refresh, lockout, and failure modes before Beta.
4. **Migration safety**
   - Idempotent migration and reversible feature-flag cutover are mandatory due to `R-003`.

---

## 2. Phased implementation plan with milestones

## Phase 0 — Architecture baseline and delivery controls
**Timeline:** 3-5 working days

### Goals
Establish the delivery foundation, finalize unresolved architecture decisions, and lock the interfaces needed by downstream phases.

### Scope
1. Confirm API contract and versioning:
   - `/v1/auth/login`
   - `/v1/auth/register`
   - `/v1/auth/me`
   - `/v1/auth/refresh`
   - `/v1/auth/reset-request`
   - `/v1/auth/reset-confirm`
2. Finalize cross-cutting policies:
   - JSON error schema per `AC-009`
   - TLS 1.3 enforcement per `AC-008`
   - 5-second JWT skew tolerance per `AC-010`
   - rate-limit policy coverage for reset endpoints from `OQ-005`
3. Resolve or explicitly defer open questions:
   - `OQ-001`
   - `OQ-002`
   - `OQ-003`
   - `OQ-004`
   - `OQ-005`
   - `OQ-006`

### Deliverables
1. Architecture decision record covering:
   - RS256 key lifecycle for `AC-001`
   - bcrypt abstraction boundary for `AC-003`
   - stateless access-token model for `AC-002`
2. Final API contract and error catalog.
3. Rollout guardrails:
   - rollback trigger confirmation
   - feature-flag ownership model
   - production readiness checklist

### Requirements addressed
- `AC-001` to `AC-010`
- planning dependencies for `FR-AUTH-001` to `FR-AUTH-005`
- planning dependencies for `NFR-PERF-001`, `NFR-PERF-002`, `NFR-REL-001`, `NFR-SEC-001`, `NFR-SEC-002`

### Milestone
**M0:** Architecture and interface freeze approved by auth-team, platform-team, and QA.

---

## Phase 1 — Core infrastructure, persistence, and security primitives
**Timeline:** 1-1.5 weeks

### Goals
Stand up the runtime, persistence, secrets, and foundational services required for secure auth flows.

### Scope
1. Provision and configure:
   - Node.js 20 LTS runtime per `AC-006`
   - PostgreSQL 15+ per `AC-004`
   - Redis 7+ per `AC-005`
2. Define persistence schema:
   - `UserProfile`
   - audit log store
   - refresh-token persistence model
3. Implement security primitives:
   - `PasswordHasher` with bcrypt cost 12 for `NFR-SEC-001` and `AC-003`
   - `JwtService` with RS256 and 2048-bit RSA keys for `NFR-SEC-002` and `AC-001`
4. Establish secret handling and rotation framework:
   - RSA private/public key loading
   - quarterly rotation procedure for `OQ-004`
5. Implement database constraints:
   - unique email index
   - lowercase normalization enforcement
   - timestamps and audit retention policies

### Deliverables
1. PostgreSQL schema for:
   - `UserProfile`
   - password hashes
   - audit logs
2. Redis key schema for:
   - hashed refresh tokens
   - TTL and revocation tracking
3. Production secret-management specification for RSA key material.
4. Benchmark evidence for:
   - bcrypt hashing target tied to Success Criterion 5
   - JWT signing/verifying viability under expected load

### Requirements addressed
- `FR-AUTH-002`
- `FR-AUTH-003`
- `FR-AUTH-005`
- `NFR-SEC-001`
- `NFR-SEC-002`
- `AC-001`
- `AC-003`
- `AC-004`
- `AC-005`
- `AC-006`

### Milestone
**M1:** Security primitives and storage layers validated in isolation.

---

## Phase 2 — Backend auth domain services and API surface
**Timeline:** 1.5-2 weeks

### Goals
Implement the full backend authentication behavior and expose the API contract.

### Scope
1. Implement `UserRepo`
   - create/read/update `UserProfile`
   - last-login updates
   - uniqueness conflict handling
2. Implement `TokenManager`
   - issue access and refresh tokens for `FR-AUTH-003`
   - revoke old refresh tokens on refresh
   - validate expired/revoked token cases
3. Implement `AuthService`
   - login for `FR-AUTH-001`
   - registration for `FR-AUTH-002`
   - profile retrieval for `FR-AUTH-004`
   - password reset request/confirm for `FR-AUTH-005`
4. Implement lockout and abuse protections:
   - 5 failed attempts in 15 minutes for `FR-AUTH-001`
   - gateway and endpoint-aligned throttling for `R-002`
5. Implement HTTP layer:
   - `/v1/auth/*` per `AC-007`
   - consistent error payloads per `AC-009`
   - bearer token validation for `/v1/auth/me`
6. Implement audit logging for:
   - login success/failure
   - registration
   - refresh
   - password reset request/confirm

### Deliverables
1. Production backend endpoints for all required auth flows.
2. Auth error taxonomy mapped to status codes.
3. Refresh-token revocation semantics.
4. Account lockout and unlock policy.

### Requirements addressed
- `FR-AUTH-001`
- `FR-AUTH-002`
- `FR-AUTH-003`
- `FR-AUTH-004`
- `FR-AUTH-005`
- `AC-002`
- `AC-007`
- `AC-009`
- `AC-010`

### Milestone
**M2:** Backend API is functionally complete and internally testable.

---

## Phase 3 — Frontend auth integration and UX hardening
**Timeline:** 1-1.5 weeks

### Goals
Integrate the frontend auth experience without compromising token security or introducing usability regressions.

### Scope
1. Implement `AuthProvider`
   - in-memory access-token handling to mitigate `R-001`
   - refresh-token exchange behavior
   - silent refresh orchestration for `FR-AUTH-003`
   - authenticated user state for `FR-AUTH-004`
2. Implement pages:
   - `LoginPage`
   - `RegisterPage`
   - `ProfilePage`
3. Add client validation and UX rules:
   - password-strength checks aligned to `FR-AUTH-002`
   - generic login error messaging to prevent user enumeration for `FR-AUTH-001`
   - post-auth redirect handling
4. Add recovery UX:
   - reset-request and reset-confirm pages/forms for `FR-AUTH-005`
   - lockout and cooldown messaging
5. Add abuse friction:
   - CAPTCHA hook after repeated failures as contingency path for `R-002`

### Deliverables
1. End-to-end browser-auth flows.
2. Secure frontend token handling model.
3. Error-state UX aligned with API semantics.

### Requirements addressed
- `FR-AUTH-001`
- `FR-AUTH-002`
- `FR-AUTH-003`
- `FR-AUTH-004`
- `FR-AUTH-005`
- mitigation support for `R-001` and `R-002`

### Milestone
**M3:** Full user journey works in staging with secure client behavior.

---

## Phase 4 — Observability, performance, reliability, and operational readiness
**Timeline:** 1 week

### Goals
Ensure the system can be safely operated and validated against NFRs before external rollout.

### Scope
1. Implement metrics and tracing:
   - `auth_login_total`
   - `auth_login_duration_seconds`
   - `auth_token_refresh_total`
   - `auth_registration_total`
   - OpenTelemetry spans across `AuthService` → `PasswordHasher` → `TokenManager` → `JwtService`
2. Configure alerts:
   - login failure spikes
   - latency breaches
   - Redis connection failures
3. Validate performance targets:
   - `NFR-PERF-001`
   - `NFR-PERF-002`
4. Validate availability and recovery:
   - `NFR-REL-001`
   - health checks
   - restart and failover readiness
5. Prepare operational assets:
   - runbooks
   - on-call checklist
   - rollback rehearsal
   - feature-flag rollback verification

### Deliverables
1. Dashboard set for auth traffic and latency.
2. Alerting configuration.
3. Load-test results showing behavior at 500 concurrent logins.
4. Operational runbooks for outage and refresh-failure scenarios.

### Requirements addressed
- `NFR-PERF-001`
- `NFR-PERF-002`
- `NFR-REL-001`
- operational support for `R-001`, `R-002`, `R-003`

### Milestone
**M4:** System is operationally ready for limited production exposure.

---

## Phase 5 — Migration, staged rollout, and GA cutover
**Timeline:** 4 weeks total
- Internal Alpha: 1 week
- Beta 10%: 2 weeks
- GA: 1 week

### Goals
Migrate safely from legacy auth to the new system using phased exposure and measurable gates.

### Scope
1. Execute migration plan for `R-003`
   - idempotent upsert migration
   - schema mapping and dry-run validation for `OQ-006`
   - backup verification before each rollout stage
2. Stage rollout by feature flag:
   - Alpha behind `AUTH_NEW_LOGIN`
   - Beta at 10%
   - GA at 100%
3. Monitor acceptance gates:
   - latency
   - error rate
   - Redis health
   - uptime
   - registration funnel
4. Remove transitional controls:
   - retire legacy auth routing after GA stability window
   - remove `AUTH_NEW_LOGIN`
   - remove `AUTH_TOKEN_REFRESH` after stabilization window

### Deliverables
1. Migration execution report.
2. Rollout gate evidence by phase.
3. Legacy deprecation plan and cleanup tasks.

### Requirements addressed
- all `FR-AUTH-*`
- all `NFR-*`
- `R-003`
- rollout requirements in the migration plan

### Milestones
1. **M5A:** Internal Alpha passes manual and automated acceptance.
2. **M5B:** Beta meets p95 latency, error-rate, and Redis stability gates.
3. **M5C:** GA completes with 99.9% uptime across the initial validation window.

---

## 3. Integration points

The following mechanisms require explicit wiring ownership rather than implicit implementation sequencing.

### 3.1 Dependency injection and service composition
1. **Named Artifact:** `AuthService` constructor dependency graph  
   - **Wired Components:** `PasswordHasher`, `TokenManager`, `UserRepo`  
   - **Owning Phase:** Phase 2  
   - **Cross-Reference:** Consumed by Phase 2 API handlers, Phase 4 tracing, Phase 5 production rollout

2. **Named Artifact:** `TokenManager` constructor dependency graph  
   - **Wired Components:** `JwtService`, Redis client  
   - **Owning Phase:** Phase 2  
   - **Cross-Reference:** Consumed by `FR-AUTH-001`, `FR-AUTH-003`, Phase 4 metrics, Phase 5 rollout gates

3. **Named Artifact:** `UserRepo` persistence wiring  
   - **Wired Components:** PostgreSQL pool, `UserProfile` schema mappings, audit log persistence  
   - **Owning Phase:** Phase 1  
   - **Cross-Reference:** Consumed by Phase 2 `AuthService` operations and Phase 5 migration

### 3.2 Middleware and request pipeline wiring
1. **Named Artifact:** Bearer-auth middleware chain for `/v1/auth/me`  
   - **Wired Components:** token extraction, `JwtService` verification, clock-skew handling per `AC-010`, user-context injection  
   - **Owning Phase:** Phase 2  
   - **Cross-Reference:** Consumed by `FR-AUTH-004`, Phase 4 observability, Phase 5 staged rollout

2. **Named Artifact:** Error-response middleware/formatter  
   - **Wired Components:** domain exceptions, HTTP status mapping, JSON error serializer per `AC-009`  
   - **Owning Phase:** Phase 2  
   - **Cross-Reference:** Consumed by all auth endpoints and Phase 3 UI error rendering

3. **Named Artifact:** API Gateway rate-limit policy set  
   - **Wired Components:** `/auth/login`, `/auth/register`, `/auth/refresh`, `/auth/reset-request`, `/auth/reset-confirm`  
   - **Owning Phase:** Phase 4  
   - **Cross-Reference:** Consumed by Phase 5 rollout protection and `R-002` mitigation

### 3.3 Frontend callback and event wiring
1. **Named Artifact:** `AuthProvider` auth-state event bindings  
   - **Wired Components:** login success handler, logout handler, silent refresh scheduler, token-expiry handler, tab-close token cleanup  
   - **Owning Phase:** Phase 3  
   - **Cross-Reference:** Consumed by `LoginPage`, `RegisterPage`, `ProfilePage`, and `R-001` mitigation

2. **Named Artifact:** `LoginPage` callback wiring  
   - **Wired Components:** `onSuccess`, redirect handler, generic error renderer, lockout-state renderer  
   - **Owning Phase:** Phase 3  
   - **Cross-Reference:** Consumed by `FR-AUTH-001`, Alpha/Beta acceptance testing

3. **Named Artifact:** `RegisterPage` callback wiring  
   - **Wired Components:** `onSuccess`, password-strength validator, terms-link dependency, post-registration routing  
   - **Owning Phase:** Phase 3  
   - **Cross-Reference:** Consumed by `FR-AUTH-002` and registration conversion measurement

### 3.4 Feature-flag and rollout wiring
1. **Named Artifact:** `AUTH_NEW_LOGIN` feature flag  
   - **Wired Components:** `LoginPage`, new auth backend routing, rollout cohort control  
   - **Owning Phase:** Phase 5  
   - **Cross-Reference:** Consumed by Internal Alpha, Beta 10%, and GA cutover

2. **Named Artifact:** `AUTH_TOKEN_REFRESH` feature flag  
   - **Wired Components:** `TokenManager` refresh flow, `AuthProvider` silent refresh path  
   - **Owning Phase:** Phase 5  
   - **Cross-Reference:** Consumed by Beta monitoring and post-GA stabilization

### 3.5 Strategy and abstraction wiring
1. **Named Artifact:** `PasswordHasher` algorithm abstraction  
   - **Wired Components:** bcrypt implementation at cost 12, future migration seam for argon2id per `AC-003`  
   - **Owning Phase:** Phase 1  
   - **Cross-Reference:** Consumed by Phase 2 login/registration/reset flows and Phase 4 benchmark validation

2. **Named Artifact:** `JwtService` signing/verification strategy  
   - **Wired Components:** RS256 signer, RS256 verifier, key-loading mechanism, skew-tolerance validator  
   - **Owning Phase:** Phase 1  
   - **Cross-Reference:** Consumed by Phase 2 token issuance/validation and Phase 4 reliability validation

---

## 4. Risk assessment and mitigation strategies

## Risk `R-001` — Token theft via XSS allows session hijacking
**Architectural significance:** Highest-impact client-side risk because it undermines all authenticated flows.

### Mitigation
1. Keep access tokens in memory only.
2. Use HttpOnly cookies for refresh tokens.
3. Minimize access-token lifetime to 15 minutes per `FR-AUTH-003`.
4. Clear in-memory auth state on tab close in `AuthProvider`.
5. Review frontend pages for unsafe token exposure in logs, storage, and error telemetry.

### Roadmap controls
- Phase 3 implements token handling and cleanup semantics.
- Phase 4 validates no token leakage in logs/traces.
- Phase 5 includes revocation runbook testing.

### Contingency
1. Immediate refresh-token revocation via `TokenManager`.
2. Force password reset for impacted users.
3. Use audit logs to identify blast radius.

---

## Risk `R-002` — Brute-force attacks on login endpoint
**Architectural significance:** High probability, medium impact, directly tied to auth perimeter exposure.

### Mitigation
1. API Gateway limit of 10 req/min per IP on `/auth/login`.
2. Lock account after 5 failed attempts in 15 minutes for `FR-AUTH-001`.
3. Use bcrypt cost 12 for offline resistance via `NFR-SEC-001`.
4. Extend explicit rate limits to reset endpoints from `OQ-005`.
5. Add CAPTCHA contingency after repeated failures.

### Roadmap controls
- Phase 2 implements lockout logic and audit tracking.
- Phase 4 wires gateway controls and alerting.
- Phase 5 watches login failure rate during Beta.

### Contingency
1. WAF IP blocks.
2. CAPTCHA escalation on `LoginPage`.
3. Incident triage using `auth_login_total` and audit events.

---

## Risk `R-003` — Data loss during migration from legacy auth
**Architectural significance:** Lower probability but release-blocking if mishandled.

### Mitigation
1. Use idempotent upserts for user migration.
2. Run parallel systems during Alpha and Beta.
3. Verify backups before each migration stage.
4. Dry-run schema transformation before production traffic.
5. Defer legacy shutdown until GA success criteria are stable.

### Roadmap controls
- Phase 5 owns migration execution.
- Phase 4 validates rollback runbook.
- Phase 0 resolves `OQ-006` scope and migration artifact design.

### Contingency
1. Disable `AUTH_NEW_LOGIN`.
2. Re-route to legacy auth.
3. Restore from known-good backup if corruption is detected.

---

## 5. Resource requirements and dependencies

## Team roles
1. **Backend engineers**
   - `AuthService`
   - `TokenManager`
   - `JwtService`
   - `UserRepo`
   - migration tooling
2. **Frontend engineers**
   - `AuthProvider`
   - `LoginPage`
   - `RegisterPage`
   - reset UX
   - `ProfilePage`
3. **Platform/DevOps**
   - Redis and PostgreSQL readiness
   - secret management
   - TLS 1.3 enforcement
   - feature-flag delivery
   - monitoring and alerts
4. **QA**
   - integration and E2E validation
   - rollout gate verification
5. **Security review**
   - RS256 key lifecycle
   - token handling model
   - brute-force and XSS controls

## External dependencies
1. **PostgreSQL 15+**
   - Critical for `UserProfile` and audit logs
   - Must be available before Phase 1 completion
2. **Redis 7+**
   - Critical for refresh-token lifecycle
   - Beta cannot start without stable Redis metrics
3. **Node.js 20 LTS**
   - Runtime baseline
4. **bcryptjs**
   - Required for `PasswordHasher`
5. **jsonwebtoken**
   - Required for `JwtService`
6. **SendGrid API**
   - Required for `FR-AUTH-005`
   - Password reset cannot reach GA until sender identity and template are finalized from `OQ-003`

## Operational dependencies
1. Feature-flag infrastructure
2. APM / OpenTelemetry
3. Prometheus and Grafana
4. Health-check endpoint monitoring
5. CI with ephemeral PostgreSQL and Redis
6. Staging environment mirroring production topology

## Environment readiness gates
1. **Before Phase 2**
   - DB schema deployed
   - Redis available
   - key material loading tested
2. **Before Phase 4**
   - metrics ingestion working
   - alerts routed
   - load-test environment available
3. **Before Phase 5**
   - rollback rehearsed
   - migration dry run complete
   - staging acceptance green

---

## 6. Success criteria and validation approach

## Functional validation
Each requirement must map to automated and staged validation.

1. `FR-AUTH-001`
   - unit: valid/invalid credential handling
   - integration: login endpoint response and lockout behavior
   - E2E: login through `LoginPage`
2. `FR-AUTH-002`
   - unit: password policy and duplicate-email rules
   - integration: database persistence
   - E2E: full registration journey
3. `FR-AUTH-003`
   - unit: token issuance/refresh/revocation
   - integration: Redis-backed token expiration
   - E2E: silent refresh via `AuthProvider`
4. `FR-AUTH-004`
   - integration: bearer token validation and `/auth/me`
   - E2E: profile rendering after login
5. `FR-AUTH-005`
   - integration: reset token issue/consume/expire flow
   - E2E: password reset journey once UX is implemented

## NFR validation
1. `NFR-PERF-001`
   - validate p95 < 200ms across auth endpoints
   - measured via APM spans
2. `NFR-PERF-002`
   - validate 500 concurrent login requests
   - measured with k6 load test
3. `NFR-REL-001`
   - validate health checks, restart behavior, and staged uptime evidence
4. `NFR-SEC-001`
   - validate bcrypt cost factor 12 through tests and benchmark output
5. `NFR-SEC-002`
   - validate RS256 with 2048-bit RSA keys through configuration and sign/verify tests

## Success criteria mapping
1. **Login response time (p95) < 200ms**
   - Gate for Beta and GA
2. **Registration success rate > 99%**
   - Beta and GA funnel check
3. **Token refresh latency (p95) < 100ms**
   - Required before broad activation of `AUTH_TOKEN_REFRESH`
4. **Service availability 99.9%**
   - Required during GA validation window
5. **Password hash time < 500ms**
   - Required before performance signoff
6. **User registration conversion > 60%**
   - Reviewed after Beta
7. **Daily active authenticated users > 1000 within 30 days of GA**
   - Post-launch KPI, not a launch blocker

## Validation stages
1. **Stage A — Unit/integration completeness**
   - Required for M2
2. **Stage B — E2E and staging acceptance**
   - Required for M3
3. **Stage C — Observability and load evidence**
   - Required for M4
4. **Stage D — Alpha/Beta/GA gate review**
   - Required for M5A/M5B/M5C

---

## 7. Timeline estimates per phase

| Phase | Duration | Primary outputs | Exit gate |
|---|---:|---|---|
| Phase 0 — Architecture baseline and delivery controls | 3-5 working days | ADRs, API contract, unresolved-question triage | M0 |
| Phase 1 — Core infrastructure, persistence, and security primitives | 1-1.5 weeks | DB/Redis/key setup, `PasswordHasher`, `JwtService` | M1 |
| Phase 2 — Backend auth domain services and API surface | 1.5-2 weeks | `AuthService`, `TokenManager`, `UserRepo`, `/v1/auth/*` | M2 |
| Phase 3 — Frontend auth integration and UX hardening | 1-1.5 weeks | `AuthProvider`, pages, reset UX, secure token handling | M3 |
| Phase 4 — Observability, performance, reliability, and operational readiness | 1 week | metrics, alerts, load tests, runbooks | M4 |
| Phase 5 — Migration, staged rollout, and GA cutover | 4 weeks | Alpha, Beta, GA, migration and flag removal | M5A/M5B/M5C |

### Overall roadmap estimate
1. **Engineering implementation through staging readiness:** ~5-7 weeks
2. **Rollout and stabilization:** ~4 weeks
3. **Total program duration:** ~9-11 weeks

---

## 8. Recommended sequencing decisions

1. Do **not** start frontend token orchestration before `JwtService`, `TokenManager`, and error semantics are stable.
2. Do **not** expose Beta traffic until:
   - Redis failure alerts are live
   - rollback is rehearsed
   - reset endpoints have explicit rate limits
3. Treat `OQ-003`, `OQ-004`, `OQ-005`, and `OQ-006` as release-relevant.
4. Keep legacy auth alive until GA stability is proven; do not compress Alpha/Beta/GA into a single release motion.
5. Make the integration artifacts above explicit work items in the implementation backlog; they are not implied by generic “service implementation” tasks.
