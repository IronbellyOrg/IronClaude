---
spec_source: test-spec-user-auth.md
complexity_score: 0.62
primary_persona: architect
---

# 1. Executive Summary

This roadmap delivers a production-ready authentication subsystem with five scoped user-facing capabilities: `FR-AUTH.1` login, `FR-AUTH.2` registration, `FR-AUTH.3` token refresh with replay detection, `FR-AUTH.4` authenticated profile retrieval, and `FR-AUTH.5` password reset. The architecture is security-critical but bounded, with medium implementation complexity driven primarily by RS256 key management, bcrypt performance/security tradeoffs, and refresh-token state correctness.

## Architectural priorities
1. **Security correctness first**
   - Implement `NFR-AUTH.3`, `RISK-1`, and `RISK-2` before broad feature rollout.
   - Treat token lifecycle correctness and secrets handling as release gates, not backlog polish.

2. **Stateful refresh token control inside a stateless JWT model**
   - Preserve stateless access-token validation while using database-backed hashed refresh-token records to satisfy `FR-AUTH.3 AC-4` and `SC-8`.

3. **Phased rollout with operational safeguards**
   - Enforce `AUTH_SERVICE_ENABLED` feature flag, secrets-manager integration, health checks, and observability before full traffic exposure.

4. **Open-question closure as a delivery dependency**
   - `OQ-1`, `OQ-2`, `OQ-6`, `OQ-7`, and `OQ-8` materially affect implementation and must be resolved during early phases, with explicit defaults if stakeholders do not decide in time.

## Delivery outcome
By the end of this roadmap, the system will:
- Authenticate users with email/password and RS256 JWTs (`FR-AUTH.1`).
- Register users with strong validation and bcrypt hashing (`FR-AUTH.2`, `NFR-AUTH.3`).
- Rotate refresh tokens with replay detection and full-user revocation on reuse (`FR-AUTH.3`, `SC-8`).
- Expose authenticated profile retrieval without sensitive fields (`FR-AUTH.4`).
- Support secure password reset with session invalidation (`FR-AUTH.5`).
- Meet measurable validation thresholds in `SC-1` through `SC-8`.

---

# 2. Phased Implementation Plan with Milestones

## Phase 0. Architecture Finalization and Delivery Readiness

### Objectives
1. Close blocking architectural questions.
2. Lock interfaces, data model, and rollout constraints.
3. Prevent mid-implementation churn.

### Scope
- Confirm implementation order from the extraction:
  1. `password-hasher.ts`
  2. `jwt-service.ts`
  3. `token-manager.ts`
  4. `auth-service.ts`
  5. `auth-middleware.ts`
  6. routes + migration `003-auth-tables.ts`

### Key tasks
1. Resolve open questions:
   - `OQ-1`: choose synchronous email dispatch vs async queue for `FR-AUTH.5`.
   - `OQ-2`: define maximum active refresh tokens per user.
   - `OQ-6`: select email provider, retry behavior, and failure contract.
   - `OQ-7`: select secrets manager platform and runtime injection pattern.
   - `OQ-8`: define concurrent refresh behavior and whether an idempotency/grace window is required.
   - `OQ-3`, `OQ-4`, `OQ-5`: explicitly defer or include as controlled scope changes.

2. Approve canonical contracts:
   - `PasswordHasher` interface
   - `JwtService` interface
   - `TokenManager` interface
   - `AuthService` orchestration contract
   - request/response DTOs for `/auth/*`

3. Finalize data model:
   - User table fields required by `FR-AUTH.2` and `FR-AUTH.4`
   - Refresh token table schema required by `FR-AUTH.3 AC-4`
   - reset-token persistence model or token-derivation approach for `FR-AUTH.5`

4. Define rollout and operations policy:
   - `AUTH_SERVICE_ENABLED` semantics
   - RSA key rotation process for `RISK-1`
   - maintenance of bcrypt cost configurability for `RISK-3`

### Milestone
- **M0: Architecture signoff complete**
  - All blocking OQs have assigned decisions or approved defaults.
  - Interface contracts and migration shape are frozen.

### Requirement coverage
- `FR-AUTH.1`
- `FR-AUTH.2`
- `FR-AUTH.3`
- `FR-AUTH.4`
- `FR-AUTH.5`
- `NFR-AUTH.3`
- `RISK-1`
- `RISK-2`
- `RISK-3`

### Timeline estimate
- **2–3 working days**

---

## Phase 1. Security Foundations and Core Infrastructure

### Objectives
1. Build the cryptographic and token primitives correctly.
2. Establish secrets and configuration wiring.
3. Create persistence foundations for auth state.

### Key tasks
1. Implement `password-hasher.ts`
   - bcrypt cost factor defaulted to 12 for `NFR-AUTH.3`
   - configurable cost factor to mitigate `RISK-3`
   - benchmark and unit validation for `SC-3`

2. Implement `jwt-service.ts`
   - RS256 signing and verification only
   - access token TTL = 15 minutes for `SC-5`
   - refresh token TTL = 7 days for `SC-5`
   - reset token TTL = 1 hour for `SC-7`
   - key retrieval from chosen secrets manager for `RISK-1`

3. Implement `token-manager.ts`
   - token issuance
   - refresh token hashing and storage support
   - rotation support
   - revoke-all-for-user primitive for `FR-AUTH.3 AC-3` and `FR-AUTH.5 AC-4`

4. Create migration `003-auth-tables.ts`
   - user table additions/creation as needed
   - refresh token table
   - reset token persistence if stored server-side
   - required rollback/down migration

5. Establish feature/config plumbing
   - `AUTH_SERVICE_ENABLED`
   - bcrypt cost configuration
   - key rotation configuration metadata
   - email service configuration placeholders

### Integration Points

1. **Named Artifact**: `TokenManager` token lifecycle registry/mechanism
   - **Wired Components**:
     - access-token issuer
     - refresh-token issuer
     - refresh-token hash persistence
     - user-wide revocation operation
     - reset-triggered session revocation
   - **Owning Phase**: Phase 1
   - **Cross-Reference**: Consumed by Phase 2 (`auth-service.ts`), Phase 3 (`auth-middleware.ts`, routes), and Phase 5 validation

2. **Named Artifact**: configuration binding mechanism for `AUTH_SERVICE_ENABLED`, bcrypt cost, token TTLs, and secrets-manager-backed RSA keys
   - **Wired Components**:
     - `password-hasher.ts`
     - `jwt-service.ts`
     - `token-manager.ts`
     - route registration guard
   - **Owning Phase**: Phase 1
   - **Cross-Reference**: Consumed by Phase 3 rollout gating and Phase 6 operations

### Milestone
- **M1: Security primitives and persistence foundation complete**
  - Cryptographic components pass unit tests.
  - Migration is reversible.
  - Secrets wiring is functional in non-production environment.

### Requirement coverage
- `FR-AUTH.1 AC-1`
- `FR-AUTH.2 AC-1`
- `FR-AUTH.3 AC-1`
- `FR-AUTH.3 AC-4`
- `FR-AUTH.5 AC-1`
- `NFR-AUTH.3`
- `RISK-1`
- `RISK-2`
- `RISK-3`
- `SC-3`
- `SC-5`
- `SC-7`

### Timeline estimate
- **4–6 working days**

---

## Phase 2. Service-Layer Orchestration and Domain Logic

### Objectives
1. Centralize auth behavior in `AuthService`.
2. Implement business rules and security responses.
3. Keep internal components non-HTTP-facing per architectural constraint.

### Key tasks
1. Implement `auth-service.ts` as the sole orchestrator
   - registration flow for `FR-AUTH.2`
   - login flow for `FR-AUTH.1`
   - refresh flow for `FR-AUTH.3`
   - password reset request and completion for `FR-AUTH.5`
   - profile read orchestration support for `FR-AUTH.4`

2. Implement registration rules
   - email format validation for `FR-AUTH.2 AC-4`
   - password policy enforcement for `FR-AUTH.2 AC-3`
   - duplicate email handling for `FR-AUTH.2 AC-2`

3. Implement login rules
   - generic credential error behavior for `FR-AUTH.1 AC-2`
   - locked-account response for `FR-AUTH.1 AC-3`
   - IP rate-limit hook integration for `FR-AUTH.1 AC-4`

4. Implement refresh logic
   - valid refresh token exchange for `FR-AUTH.3 AC-1`
   - expired token rejection for `FR-AUTH.3 AC-2`
   - replay detection with full-user invalidation for `FR-AUTH.3 AC-3`
   - transactional rotation to reduce race-condition exposure from `OQ-8`

5. Implement password reset logic
   - token generation and email dispatch for `FR-AUTH.5 AC-1`
   - reset completion and token invalidation for `FR-AUTH.5 AC-2`
   - expired/invalid token handling for `FR-AUTH.5 AC-3`
   - global session invalidation on successful reset for `FR-AUTH.5 AC-4`

### Integration Points

1. **Named Artifact**: `AuthService` orchestration dispatch mechanism
   - **Wired Components**:
     - `PasswordHasher`
     - `JwtService`
     - `TokenManager`
     - user repository/database access
     - refresh token repository/database access
     - email service adapter
     - login rate-limiter integration
   - **Owning Phase**: Phase 2
   - **Cross-Reference**: Consumed by Phase 3 route handlers and middleware-protected profile retrieval

2. **Named Artifact**: password reset delivery adapter binding
   - **Wired Components**:
     - selected email provider client
     - password reset template payload builder
     - retry/failure policy chosen from `OQ-1` and `OQ-6`
   - **Owning Phase**: Phase 2
   - **Cross-Reference**: Consumed by Phase 3 `/auth/password-reset/request` endpoint and Phase 5 failure-path tests

3. **Named Artifact**: login rate-limit binding
   - **Wired Components**:
     - IP-based rate-limiter
     - login endpoint service call
   - **Owning Phase**: Phase 2
   - **Cross-Reference**: Consumed by Phase 3 route registration and Phase 5 `SC-4` validation

### Milestone
- **M2: Auth domain logic complete**
  - All primary flows work through service-level tests.
  - Replay detection and reset invalidation semantics are verified.

### Requirement coverage
- `FR-AUTH.1`
- `FR-AUTH.2`
- `FR-AUTH.3`
- `FR-AUTH.5`
- `RISK-2`
- `SC-4`
- `SC-6`
- `SC-8`

### Timeline estimate
- **5–7 working days**

---

## Phase 3. HTTP Surface, Middleware Integration, and Feature-Flagged Exposure

### Objectives
1. Expose only the required `/auth/*` HTTP surface.
2. Integrate with existing middleware and route registration.
3. Preserve existing unauthenticated system behavior during phased rollout.

### Key tasks
1. Implement `auth-middleware.ts`
   - Bearer token extraction and verification
   - user context resolution for `FR-AUTH.4`
   - invalid/expired token rejection for `FR-AUTH.4 AC-2`

2. Register `/auth/*` routes in `src/routes/index.ts`
   - login
   - registration
   - refresh
   - profile
   - password reset request
   - password reset confirm

3. Apply rollout guard
   - use `AUTH_SERVICE_ENABLED` to enable phased exposure
   - ensure existing unauthenticated endpoints remain unaffected

4. Enforce response-shape and data-minimization contracts
   - `FR-AUTH.4 AC-1`
   - `FR-AUTH.4 AC-3`
   - generic login error response shape from `FR-AUTH.1 AC-2`

5. Integrate cookie strategy
   - refresh token via httpOnly cookie per architectural constraints
   - access token usage expectations aligned with in-memory client handling

### Integration Points

1. **Named Artifact**: existing authentication middleware chain in `src/middleware/auth-middleware.ts`
   - **Wired Components**:
     - `TokenManager` verification path
     - `JwtService` verification path
     - authenticated user context injection
   - **Owning Phase**: Phase 3
   - **Cross-Reference**: Consumed by Phase 3 `/auth/profile` route and all future authenticated endpoints

2. **Named Artifact**: route registry in `src/routes/index.ts`
   - **Wired Components**:
     - `/auth/login`
     - `/auth/register`
     - `/auth/refresh`
     - `/auth/profile`
     - `/auth/password-reset/request`
     - `/auth/password-reset/confirm`
     - feature-flag guard `AUTH_SERVICE_ENABLED`
   - **Owning Phase**: Phase 3
   - **Cross-Reference**: Consumed by Phase 4 performance/availability instrumentation and Phase 5 end-to-end validation

3. **Named Artifact**: HTTP cookie/response binding for refresh-token delivery
   - **Wired Components**:
     - refresh-token issuance path
     - refresh-token rotation path
     - cookie flags and expiry alignment
   - **Owning Phase**: Phase 3
   - **Cross-Reference**: Consumed by Phase 5 integration/E2E validation for `FR-AUTH.1` and `FR-AUTH.3`

### Milestone
- **M3: Auth API surface available behind feature flag**
  - Endpoints respond correctly in integration environment.
  - Middleware gating and response contracts are stable.

### Requirement coverage
- `FR-AUTH.1`
- `FR-AUTH.2`
- `FR-AUTH.3`
- `FR-AUTH.4`
- `FR-AUTH.5`
- `SC-4`
- `SC-5`
- `SC-6`
- `SC-7`
- `SC-8`

### Timeline estimate
- **3–4 working days**

---

## Phase 4. Reliability, Performance, and Operational Hardening

### Objectives
1. Prove the auth subsystem can meet non-functional targets.
2. Establish operational controls for uptime and key hygiene.
3. Reduce production rollout risk.

### Key tasks
1. Validate performance target `NFR-AUTH.1`
   - k6 scenarios for login, refresh, and profile retrieval
   - profile p95 latency under normal load
   - analyze bcrypt contribution versus end-to-end latency budget
   - tune I/O, database access, and middleware overhead as needed

2. Validate availability target `NFR-AUTH.2`
   - health check integration
   - alert routing to PagerDuty
   - degraded dependency behavior, especially for email service paths

3. Operationalize key management for `RISK-1`
   - 90-day rotation procedure
   - documented emergency rotation process to close residual gap
   - public key distribution/verification path

4. Harden token replay and race handling for `RISK-2`
   - instrumentation around refresh rotation failures
   - anomaly signals for rapid repeated refresh attempts
   - documented behavior for duplicate concurrent refreshes per `OQ-8`

5. Ensure bcrypt reviewability for `RISK-3`
   - config-driven cost factor
   - annual review runbook entry
   - benchmark repeatability

### Integration Points

1. **Named Artifact**: observability/monitoring binding for auth service health and latency
   - **Wired Components**:
     - health check endpoint
     - APM latency dashboard
     - PagerDuty alerting
     - k6 test suite outputs
   - **Owning Phase**: Phase 4
   - **Cross-Reference**: Consumed by Phase 6 production rollout governance and post-release validation

2. **Named Artifact**: key rotation operational mechanism
   - **Wired Components**:
     - secrets manager key versioning
     - `jwt-service.ts` key retrieval
     - deployment/runtime reload procedure
   - **Owning Phase**: Phase 4
   - **Cross-Reference**: Consumed by Phase 6 operations and incident response for `RISK-1`

### Milestone
- **M4: Non-functional readiness achieved**
  - Performance, availability, and key-ops controls are demonstrated in staging/pre-prod.

### Requirement coverage
- `NFR-AUTH.1`
- `NFR-AUTH.2`
- `NFR-AUTH.3`
- `RISK-1`
- `RISK-2`
- `RISK-3`
- `SC-1`
- `SC-2`
- `SC-3`

### Timeline estimate
- **4–5 working days**

---

## Phase 5. Verification, Security Validation, and Release Readiness

### Objectives
1. Validate every functional and non-functional requirement.
2. Prove rollback safety and release confidence.
3. Block launch on any security regression.

### Key tasks
1. Unit validation
   - bcrypt cost factor and timing
   - JWT TTLs and signing algorithm enforcement
   - validation rules for email/password

2. Integration validation
   - registration happy and conflict paths
   - login success, invalid credentials, locked account, and rate limiting
   - refresh success, expiry, replay detection, and revocation persistence
   - profile retrieval with sensitive-field exclusion
   - password reset request, expiry, invalid token, success, and session invalidation

3. End-to-end validation
   - client-observable auth flows
   - cookie behavior for refresh tokens
   - feature-flag enable/disable paths

4. Migration validation
   - apply migration `003-auth-tables.ts`
   - run down migration successfully
   - verify rollback without auth-state corruption

5. Release review
   - unresolved OQs either closed or explicitly accepted as risks
   - deferments (`OQ-4`, possibly `OQ-5`) recorded with owner and target version

### Milestone
- **M5: Release approval**
  - All success criteria pass.
  - Rollback plan is verified.
  - Security signoff is complete.

### Requirement coverage
- `FR-AUTH.1`
- `FR-AUTH.2`
- `FR-AUTH.3`
- `FR-AUTH.4`
- `FR-AUTH.5`
- `NFR-AUTH.1`
- `NFR-AUTH.2`
- `NFR-AUTH.3`
- `SC-1`
- `SC-2`
- `SC-3`
- `SC-4`
- `SC-5`
- `SC-6`
- `SC-7`
- `SC-8`

### Timeline estimate
- **4–6 working days**

---

## Phase 6. Controlled Rollout and Post-Launch Stabilization

### Objectives
1. Minimize blast radius during production introduction.
2. Detect regressions quickly.
3. Convert operational learnings into next-scope decisions.

### Key tasks
1. Enable `AUTH_SERVICE_ENABLED` in staged progression
   - internal/staging
   - limited production cohort
   - full production exposure

2. Monitor launch metrics
   - latency and uptime against `SC-1` and `SC-2`
   - login failure rates
   - refresh replay/revocation events
   - password reset email delivery health

3. Execute post-launch review
   - assess need to promote `OQ-3` lockout policy into next release
   - assess need for `OQ-4` audit logging
   - assess need for `OQ-5` token revocation on user deletion
   - assess observed concurrency issues from `OQ-8`

### Milestone
- **M6: Production steady state**
  - Full rollout completed with no unresolved Sev-1/Sev-2 auth defects.

### Timeline estimate
- **3–5 working days of monitored rollout/stabilization**

---

# 3. Risk Assessment and Mitigation Strategies

## Primary delivery risks

1. **RISK-1: JWT Private Key Compromise**
   - **Impact**: total authentication bypass through forged tokens.
   - **Mitigation plan**:
     - store private key only in secrets manager.
     - use RS256 exclusively.
     - implement 90-day rotation before production launch.
     - add emergency rotation runbook in Phase 4.
   - **Roadmap control point**: M1 and M4 gates.
   - **Release rule**: no production enablement without secrets-manager-backed signing and tested rotation.

2. **RISK-2: Refresh Token Replay Attack**
   - **Impact**: session hijack and account compromise.
   - **Mitigation plan**:
     - rotate refresh tokens on each use.
     - store only refresh token hashes.
     - detect reuse of rotated token and revoke all user tokens.
     - use transactional rotation logic.
     - add observability for replay anomalies.
   - **Roadmap control point**: M2 and M5 gates.
   - **Release rule**: `SC-8` must pass before launch.

3. **RISK-3: bcrypt Cost Factor Becoming Insufficient**
   - **Impact**: reduced password-cracking resistance over time.
   - **Mitigation plan**:
     - configurable cost factor with default 12.
     - benchmark validation in CI.
     - annual review process added to runbook.
   - **Roadmap control point**: M1 and M4 gates.

## Additional surfaced risks

4. **RISK-4: No Progressive Account Lockout Policy**
   - **Impact**: distributed brute-force remains only partially mitigated.
   - **Mitigation strategy**:
     - minimum v1 behavior remains IP rate limiting for `FR-AUTH.1 AC-4`.
     - architecture should leave room for account-centric lockout extension.
     - if stakeholders accept deferment, document as residual v1 risk.
   - **Decision gate**: resolve under `OQ-3` in Phase 0.

5. **RISK-5: Token State on User Deletion**
   - **Impact**: deleted-user sessions may survive until TTL expiry.
   - **Mitigation strategy**:
     - decide in Phase 0 whether this is v1.0 or v1.1.
     - if deferred, document explicit risk acceptance and operational workaround.
   - **Decision gate**: resolve under `OQ-5`.

## Delivery risks from ambiguity

6. **Email service ambiguity (`OQ-1`, `OQ-6`)**
   - **Impact**: blocks `FR-AUTH.5`, introduces latency/reliability uncertainty.
   - **Mitigation**:
     - select provider and delivery mode in Phase 0.
     - bind contract in Phase 2.
     - validate degraded behavior in Phase 4.

7. **Secrets manager ambiguity (`OQ-7`)**
   - **Impact**: blocks production-safe `jwt-service.ts`.
   - **Mitigation**:
     - select platform before Phase 1 implementation begins.

8. **Concurrent refresh race (`OQ-8`)**
   - **Impact**: legitimate users may be logged out due to false replay detection.
   - **Mitigation**:
     - choose explicit behavior in Phase 0.
     - implement transactional controls in Phase 2.
     - test concurrency path in Phase 5.

---

# 4. Resource Requirements and Dependencies

## Team roles required

1. **Backend engineer**
   - Owns service implementation, routes, middleware, migration, and token logic.

2. **Security engineer / security reviewer**
   - Reviews RS256 usage, secrets management, replay detection, password-reset flow, and rollout controls.

3. **Platform / DevOps engineer**
   - Owns secrets manager integration, key rotation process, health checks, monitoring, and deployment flagging.

4. **QA / test engineer**
   - Owns integration, concurrency, and end-to-end validation, plus k6 performance coverage.

5. **Product / architecture owner**
   - Resolves `OQ-1` through `OQ-8`, especially scope decisions around lockout, audit logging, and deletion revocation.

## Dependency plan

1. **`jsonwebtoken` library**
   - Needed for `jwt-service.ts`.
   - Must pass security review and maintenance check before adoption.

2. **`bcrypt` library**
   - Needed for `password-hasher.ts`.
   - Must support cost-factor validation and benchmark testing.

3. **RSA key pair via secrets manager**
   - Critical dependency for RS256.
   - Blocking for production-safe token issuance.

4. **Email service**
   - Blocking dependency for `FR-AUTH.5`.
   - Contract must define request format, timeout, retry policy, and error semantics.

5. **User database table**
   - Supports `FR-AUTH.1`, `FR-AUTH.2`, `FR-AUTH.4`, `FR-AUTH.5`.

6. **RefreshToken database table**
   - Supports `FR-AUTH.3` and revocation/replay detection.

7. **k6 + APM tooling**
   - Required for `NFR-AUTH.1`, `NFR-AUTH.2`, `SC-1`, and `SC-2`.

## Environment and infrastructure requirements

1. Staging environment with:
   - secrets-manager access
   - test RSA keys
   - email service sandbox/test mode
   - representative database
   - APM instrumentation

2. CI/CD requirements:
   - unit, integration, and E2E test stages
   - migration up/down validation
   - benchmark coverage for bcrypt timing
   - feature-flag-aware deployment path

---

# 5. Success Criteria and Validation Approach

## Success criteria traceability

1. **SC-1: Authentication endpoint p95 latency < 200ms**
   - Validate in Phase 4 with k6 and APM.
   - Primary concern: login path may be strained by `NFR-AUTH.3` bcrypt budget.

2. **SC-2: Service availability ≥ 99.9%**
   - Validate via health check monitoring and PagerDuty-linked uptime tracking.

3. **SC-3: Password hash timing ≈ 250ms at cost factor 12**
   - Validate with unit benchmark and config assertions.

4. **SC-4: Login rate limiting enforced**
   - Integration test: 6th attempt in 60 seconds rejected.
   - Traceable to `FR-AUTH.1 AC-4`.

5. **SC-5: Token TTLs correct**
   - Unit validation of 15-minute access token and 7-day refresh token.
   - Traceable to `FR-AUTH.1 AC-1` and `FR-AUTH.3 AC-1`.

6. **SC-6: Password policy enforced**
   - Unit and integration validation of complexity rules.
   - Traceable to `FR-AUTH.2 AC-3`.

7. **SC-7: Reset token TTL = 1 hour**
   - Integration validation of expiry behavior.
   - Traceable to `FR-AUTH.5 AC-1` and `FR-AUTH.5 AC-3`.

8. **SC-8: Replay detection triggers full revocation**
   - Integration/concurrency scenario verifies all-user-token invalidation on reuse.
   - Traceable to `FR-AUTH.3 AC-3`.

## Validation approach by layer

1. **Unit tests**
   - crypto primitives
   - token TTL calculations
   - validation rules
   - response filtering helpers

2. **Integration tests**
   - service + database + token lifecycle
   - migration correctness
   - rate limiting
   - session invalidation after reset

3. **End-to-end tests**
   - route behavior
   - cookies and auth headers
   - feature-flagged enablement
   - real client-observable flows

4. **Performance and resilience tests**
   - k6 for latency
   - dependency degradation scenarios for email service
   - refresh-race scenarios for `OQ-8`

5. **Operational validation**
   - key rotation drill
   - rollback exercise using migration down path
   - alerting verification

## Release gates
1. No open High-severity security defects.
2. `SC-1` through `SC-8` all pass.
3. `RISK-1` and `RISK-2` mitigations are implemented, not merely documented.
4. Feature flag rollback path is verified.
5. Migration rollback succeeds cleanly.

---

# 6. Timeline Estimates per Phase

| Phase | Name | Estimate |
|---|---|---:|
| Phase 0 | Architecture Finalization and Delivery Readiness | 2–3 working days |
| Phase 1 | Security Foundations and Core Infrastructure | 4–6 working days |
| Phase 2 | Service-Layer Orchestration and Domain Logic | 5–7 working days |
| Phase 3 | HTTP Surface, Middleware Integration, and Feature-Flagged Exposure | 3–4 working days |
| Phase 4 | Reliability, Performance, and Operational Hardening | 4–5 working days |
| Phase 5 | Verification, Security Validation, and Release Readiness | 4–6 working days |
| Phase 6 | Controlled Rollout and Post-Launch Stabilization | 3–5 working days |

## Overall delivery range
- **Total estimated effort**: **25–36 working days**

## Critical path
1. Resolve `OQ-1`, `OQ-2`, `OQ-6`, `OQ-7`, `OQ-8`
2. Implement Phase 1 security primitives
3. Complete Phase 2 token rotation and replay logic
4. Expose Phase 3 routes and middleware
5. Prove Phase 4 non-functional targets
6. Pass Phase 5 release gates

## Schedule risk notes
- The most likely schedule slips are:
  1. secrets manager selection and integration (`OQ-7`)
  2. email service/provider uncertainty (`OQ-1`, `OQ-6`)
  3. refresh rotation race-condition handling (`OQ-8`)
  4. meeting `NFR-AUTH.1` while honoring `NFR-AUTH.3`

If schedule compression is required, preserve Phases 1, 2, and 5 intact; reduce scope by formally deferring unresolved gap items rather than weakening security or validation rigor.
