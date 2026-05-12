---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
---

# 1. Executive summary

This roadmap delivers a medium-complexity authentication subsystem centered on secure credential handling, RS256 JWT issuance, refresh-token rotation, authenticated profile access, and password reset. Although the functional scope is modest, the architecture is security-sensitive and operationally non-trivial because of asymmetric key management, token replay detection, refresh-token revocation, external email dependency, and an explicit conflict between latency and bcrypt requirements.

## Architectural priorities

1. **Security correctness before feature breadth**
   - RS256 key custody, refresh-token hashing, replay detection, enumeration resistance, and session invalidation are the critical-path controls.
2. **Explicit state boundaries**
   - Access tokens remain stateless JWTs, while refresh-token lifecycle and password reset flows rely on durable database-backed state.
3. **Operational resilience**
   - Availability, migration reversibility, secrets integration, and rollback controls must be implemented alongside feature code, not deferred.
4. **Validation-led delivery**
   - Unit, integration, security, benchmark, load, migration, and E2E verification must be phased with implementation.
5. **Decision closure on open questions**
   - The bcrypt latency contradiction, email dispatch mode, session concurrency policy, and key rotation strategy require early architectural resolution.

## Recommended delivery stance

- Treat **FR-AUTH.1**, **FR-AUTH.2**, **FR-AUTH.3**, **NFR-AUTH.2**, and **NFR-AUTH.3** as the backbone.
- Defer release signoff until:
  - replay detection is validated,
  - token revocation behavior is proven,
  - migration rollback is tested,
  - secrets manager integration is operational,
  - latency contradiction has an explicit decision record.

---

# 2. Phased implementation plan with milestones

## Phase 1 — Architecture, data model, and security foundations

### Milestone
Establish the auth subsystem foundation: schema, cryptographic services, secrets integration, route skeletons, middleware entry points, and explicit wiring mechanisms.

### Phase objectives

1. Finalize unresolved architectural decisions that affect all downstream work.
2. Create persistence primitives for users and refresh tokens.
3. Stand up RS256 signing, bcrypt hashing, and auth middleware integration.
4. Register route and DI/registry wiring explicitly.

### Integration points

1. **Named Artifact**: `AuthRouteRegistry`
   - **Wired Components**: login handler, registration handler, refresh handler, profile handler, password-reset handlers
   - **Owning Phase**: Phase 1
   - **Cross-Reference**: Consumed in Phases 2, 3, and 4 by endpoint implementation, testing, and rollout validation

2. **Named Artifact**: `SecurityServiceContainer`
   - **Wired Components**: `JwtService`, `TokenManager`, `PasswordHasher`, `SecretsProvider`, `RateLimiter`
   - **Owning Phase**: Phase 1
   - **Cross-Reference**: Consumed in Phases 2 and 3 by auth flows and tests

3. **Named Artifact**: `AuthMiddlewareChain`
   - **Wired Components**: Bearer extractor, JWT verifier, user-context loader, unauthorized-response guard
   - **Owning Phase**: Phase 1
   - **Cross-Reference**: Consumed in Phases 2 and 3 by profile retrieval and regression/security tests

### Task table

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | COMP-001 | Define auth module boundaries and package layout | Auth architecture | None | Module boundaries documented; ownership of services/routes/models agreed | M | P0 |
| 2 | COMP-002 | Define user domain model contract | Domain model | COMP-001 | User entity fields and invariants approved for implementation | S | P0 |
| 3 | COMP-003 | Define refresh token domain model contract | Domain model | COMP-001 | Refresh-token entity fields, statuses, and lifecycle states documented | S | P0 |
| 4 | COMP-004 | Define auth service orchestration layer | Service layer | COMP-001 | Service responsibilities for login/register/refresh/profile/reset are partitioned | M | P0 |
| 5 | COMP-005 | Define JWT signing and verification service contract | Security services | COMP-001 | JWT interface covers issue, verify, key versioning, and TTL inputs | M | P0 |
| 6 | COMP-006 | Define password hasher service contract | Security services | COMP-001 | Hasher API supports hash, verify, configurable cost factor, benchmark hook | S | P0 |
| 7 | COMP-007 | Define token manager contract for access/refresh/reset lifecycle | Token lifecycle | COMP-004, COMP-005 | Token manager contract covers issuance, rotation, revocation, reset token flow | M | P0 |
| 8 | COMP-008 | Define auth middleware contract | Middleware | COMP-001 | Middleware contract covers bearer extraction, verification, user context, 401 behavior | S | P0 |
| 9 | COMP-009 | Define email adapter contract for password reset dispatch | Integration adapter | COMP-004 | Interface specifies payload, retry semantics, and failure reporting | M | P1 |
| 10 | DM-001 | Create users table schema | Database | COMP-002 | Schema includes id, email, password_hash, display_name, created_at and constraints | M | P0 |
| 11 | DM-002 | Create refresh_tokens table schema | Database | COMP-003 | Schema includes token hash, user_id, expiry, revoked/rotated metadata | M | P0 |
| 12 | DM-003 | Add unique index on user email | Database | DM-001 | Duplicate email inserts are rejected at DB level | S | P0 |
| 13 | DM-004 | Add lookup indexes for refresh-token queries | Database | DM-002 | User and token-hash lookups meet expected query plans | S | P0 |
| 14 | MIG-003 | Implement forward migration for auth tables | Migrations | DM-001, DM-002, DM-003, DM-004 | Migration creates both tables and indexes successfully in clean environment | M | P0 |
| 15 | MIG-003.DOWN | Implement reversible down migration for auth tables | Migrations | MIG-003 | Down migration removes auth schema cleanly without orphaned objects | S | P0 |
| 16 | API-001 | Register /auth route group in main router | Routing | COMP-001 | `/auth/*` group is discoverable and routed without affecting existing endpoints | S | P0 |
| 17 | API-002 | Create POST /auth/login route skeleton | Routing | API-001, COMP-004 | Route exists with placeholder handler and agreed request/response contract | S | P0 |
| 18 | API-003 | Create POST /auth/register route skeleton | Routing | API-001, COMP-004 | Route exists with placeholder handler and agreed request/response contract | S | P0 |
| 19 | API-004 | Create POST /auth/refresh route skeleton | Routing | API-001, COMP-004 | Route exists with cookie-aware request contract | S | P0 |
| 20 | API-005 | Create GET /auth/profile route skeleton | Routing | API-001, COMP-008 | Route exists behind auth middleware contract | S | P0 |
| 21 | API-006 | Create POST /auth/password-reset/request route skeleton | Routing | API-001, COMP-009 | Route exists with reset-request request/response contract | S | P1 |
| 22 | API-007 | Create POST /auth/password-reset/confirm route skeleton | Routing | API-001, COMP-007 | Route exists with reset-confirm request/response contract | S | P1 |
| 23 | OPS-001 | Integrate secrets manager contract for RSA private key retrieval | Secrets integration | COMP-005 | Service startup can resolve signing key via external secrets interface | M | P0 |
| 24 | OPS-002 | Define RSA key rotation operating model | Security operations | OPS-001, COMP-005 | Rotation cadence, versioning, and fallback behavior documented and approved | M | P0 |
| 25 | OPS-003 | Add auth feature flag and rollback control | Runtime configuration | API-001 | `AUTH_SERVICE_ENABLED` can disable auth route behavior predictably | S | P0 |
| 26 | OPS-004 | Define health check coverage for auth dependencies | Operations | OPS-001, COMP-009 | Health strategy covers database, secrets, and email dependency states | S | P1 |
| 27 | FR-AUTH.2 | Design registration flow sequence and data ownership | Registration flow | COMP-002, COMP-006, API-003 | End-to-end control flow for validation, hashing, persistence, and response is approved | M | P0 |
| 28 | FR-AUTH.1 | Design login flow sequence and security controls | Login flow | COMP-004, COMP-006, COMP-007, API-002 | Flow covers credential verification, token issuance, rate limiting, and error paths | M | P0 |
| 29 | FR-AUTH.3 | Design refresh flow with rotation and replay detection | Refresh flow | COMP-003, COMP-007, API-004 | Rotation, replay detection, and revocation rules are explicitly defined | M | P0 |
| 30 | FR-AUTH.4 | Design authenticated profile retrieval flow | Profile flow | COMP-008, API-005 | Profile retrieval contract defines claims-to-user resolution and response schema | S | P1 |
| 31 | FR-AUTH.5 | Design password reset flow and token invalidation rules | Password reset flow | COMP-007, COMP-009, API-006, API-007 | Request/confirm steps, TTL, single-use, and session invalidation are specified | M | P1 |
| 32 | NFR-AUTH.2 | Define availability architecture for auth critical path | Reliability design | OPS-004, COMP-004 | 99.9% uptime dependencies and failure domains are mapped | M | P0 |
| 33 | NFR-AUTH.3 | Define bcrypt configuration strategy at cost factor 12 | Security configuration | COMP-006 | Cost-factor configuration path is fixed and externally configurable | S | P0 |
| 34 | NFR-AUTH.1 | Resolve latency-budget architecture and contradiction | Performance design | FR-AUTH.1, FR-AUTH.3, NFR-AUTH.3 | Explicit decision recorded for meeting or revising <200ms p95 target | M | P0 |
| 35 | TEST-ARCH-001 | Define test strategy matrix across unit/integration/security/load/E2E | QA architecture | COMP-001, FR-AUTH.1, FR-AUTH.5, NFR-AUTH.1 | Test inventory maps every FR/NFR to verification type and environment | M | P0 |
| 36 | TEST-ARCH-002 | Define test fixtures for auth data and token lifecycle | QA foundation | DM-001, DM-002, TEST-ARCH-001 | Fixtures cover users, active sessions, revoked tokens, expired tokens, locked accounts | S | P1 |
| 37 | DEC-001 | Decide sync vs async password-reset email dispatch | Architecture decision | FR-AUTH.5, COMP-009 | Decision includes latency, resilience, and infrastructure implications | M | P0 |
| 38 | DEC-002 | Decide maximum active refresh tokens per user | Security policy | FR-AUTH.3, DM-002 | Session concurrency cap or explicit no-cap policy is approved | S | P1 |
| 39 | DEC-003 | Decide account lockout policy beyond per-IP rate limiting | Security policy | FR-AUTH.1 | Decision captured with rationale for v1 inclusion or deferral | M | P1 |
| 40 | DEC-004 | Decide token revocation behavior on user deletion | Lifecycle policy | FR-AUTH.3, FR-AUTH.4 | Deletion-time token invalidation behavior is defined for implementation | S | P1 |

### Timeline estimate

1. **Architecture and decision closure**: 2–3 working days
2. **Schema, migrations, and route skeletons**: 2–3 working days
3. **Security/ops foundation and wiring**: 2–3 working days

**Phase estimate**: 1.5–2 weeks

---

## Phase 2 — Core authentication feature implementation

### Milestone
Deliver functional registration, login, refresh, profile retrieval, and password reset flows on the established security and persistence foundation.

### Phase objectives

1. Implement all five functional requirements completely.
2. Wire services into the route registry and middleware chain.
3. Build the critical-path controls for hashing, tokens, cookies, replay detection, and session invalidation.

### Integration points

1. **Named Artifact**: `AuthRouteRegistry`
   - **Wired Components**: concrete handlers for login, register, refresh, profile, password-reset request, password-reset confirm
   - **Owning Phase**: Phase 2 populates the registry with implementations
   - **Cross-Reference**: Consumed in Phase 3 by integration/E2E tests and in Phase 4 by operational rollout

2. **Named Artifact**: `SecurityServiceContainer`
   - **Wired Components**: production `JwtService`, `PasswordHasher`, `TokenManager`, `RateLimiter`, `EmailAdapter`
   - **Owning Phase**: Phase 2 completes production bindings
   - **Cross-Reference**: Consumed in Phases 3 and 4 for testing and runtime validation

3. **Named Artifact**: `AuthMiddlewareChain`
   - **Wired Components**: token extractor, verifier, context loader, profile authorization gate
   - **Owning Phase**: Phase 2 finalizes behavior
   - **Cross-Reference**: Consumed by profile endpoint and security regression tests in Phase 3

### Task table

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | FR-AUTH.2a | Implement successful registration persistence and response flow | Registration service | FR-AUTH.2, DM-001, API-003, COMP-006 | Valid input creates user and returns 201 with profile payload | M | P0 |
| 2 | FR-AUTH.2b | Implement duplicate-email conflict handling | Registration service | FR-AUTH.2a, DM-003 | Existing email returns 409 without partial writes | S | P0 |
| 3 | FR-AUTH.2c | Implement password policy enforcement | Registration validation | FR-AUTH.2, COMP-006 | Passwords violating length/case/digit rules are rejected consistently | S | P0 |
| 4 | FR-AUTH.2d | Implement email-format validation | Registration validation | FR-AUTH.2 | Malformed emails are rejected before database access | S | P0 |
| 5 | FR-AUTH.1a | Implement successful login token issuance | Login service | FR-AUTH.1, API-002, COMP-007, OPS-001 | Valid credentials return 200, 15m access token, and 7d refresh token | M | P0 |
| 6 | FR-AUTH.1b | Implement generic invalid-credential response path | Login security | FR-AUTH.1, FR-AUTH.1a | Invalid credentials return 401 with enumeration-resistant message | S | P0 |
| 7 | FR-AUTH.1c | Implement locked-account rejection path | Login security | FR-AUTH.1, DM-001 | Suspended/locked accounts return 403 and do not issue tokens | S | P1 |
| 8 | FR-AUTH.1d | Implement per-IP login rate limiting at 5 requests/minute | Rate limiting | FR-AUTH.1, COMP-008 | Sixth request in 60 seconds per IP is rejected | M | P0 |
| 9 | FR-AUTH.3a | Implement refresh-token rotation and new token issuance | Refresh service | FR-AUTH.3, DM-002, API-004, COMP-007 | Valid refresh token returns new access token and rotated refresh token | M | P0 |
| 10 | FR-AUTH.3b | Implement expired refresh-token rejection | Refresh service | FR-AUTH.3a | Expired refresh token returns 401 and no new token pair | S | P0 |
| 11 | FR-AUTH.3c | Implement replay detection with full user-session revocation | Refresh security | FR-AUTH.3a, DM-002, DEC-002 | Reuse of rotated token revokes all user refresh sessions | L | P0 |
| 12 | FR-AUTH.3d | Implement refresh-token hash storage instead of plaintext | Token persistence | FR-AUTH.3, DM-002, COMP-007 | Database persists SHA-256 or approved hash form only, never raw token | S | P0 |
| 13 | FR-AUTH.4a | Implement authenticated profile retrieval response | Profile endpoint | FR-AUTH.4, API-005, COMP-008, DM-001 | Valid bearer token returns id, email, display_name, created_at | S | P0 |
| 14 | FR-AUTH.4b | Implement invalid/expired access-token rejection | Middleware | FR-AUTH.4, COMP-008, COMP-005 | Invalid or expired access tokens return 401 consistently | S | P0 |
| 15 | FR-AUTH.4c | Implement sensitive-field exclusion in profile responses | Response shaping | FR-AUTH.4a, COMP-002 | password_hash and refresh token data are absent from profile responses | S | P0 |
| 16 | FR-AUTH.5a | Implement password-reset request token generation and dispatch | Password reset | FR-AUTH.5, API-006, COMP-009, DEC-001 | Registered email triggers 1-hour reset token generation and email dispatch | M | P0 |
| 17 | FR-AUTH.5b | Implement password-reset confirmation and single-use invalidation | Password reset | FR-AUTH.5a, API-007, COMP-006, COMP-007 | Valid token permits password change once and invalidates reset token | M | P0 |
| 18 | FR-AUTH.5c | Implement invalid/expired reset-token rejection | Password reset | FR-AUTH.5b | Invalid or expired reset token returns 400 with appropriate message | S | P0 |
| 19 | FR-AUTH.5d | Implement refresh-session revocation on successful password reset | Session revocation | FR-AUTH.5b, FR-AUTH.3c, DM-002 | Successful password reset invalidates all active refresh tokens | M | P0 |
| 20 | API-001.W1 | Populate `AuthRouteRegistry` with auth handlers | Routing/wiring | API-002, API-003, API-004, API-005, API-006, API-007 | Registry maps each `/auth/*` route to concrete handler implementation | S | P0 |
| 21 | API-002.W1 | Wire login handler into route registry | Routing/wiring | FR-AUTH.1a, API-001.W1 | POST /auth/login resolves to login controller in runtime | S | P0 |
| 22 | API-003.W1 | Wire registration handler into route registry | Routing/wiring | FR-AUTH.2a, API-001.W1 | POST /auth/register resolves to registration controller in runtime | S | P0 |
| 23 | API-004.W1 | Wire refresh handler into route registry | Routing/wiring | FR-AUTH.3a, API-001.W1 | POST /auth/refresh resolves to refresh controller in runtime | S | P0 |
| 24 | API-005.W1 | Wire profile handler behind auth middleware | Routing/wiring | FR-AUTH.4a, API-001.W1, MW-001 | GET /auth/profile executes middleware then profile handler | S | P0 |
| 25 | API-006.W1 | Wire reset-request handler into route registry | Routing/wiring | FR-AUTH.5a, API-001.W1 | POST /auth/password-reset/request resolves to reset-request controller | S | P1 |
| 26 | API-007.W1 | Wire reset-confirm handler into route registry | Routing/wiring | FR-AUTH.5b, API-001.W1 | POST /auth/password-reset/confirm resolves to reset-confirm controller | S | P1 |
| 27 | MW-001 | Populate `AuthMiddlewareChain` with bearer extraction and verification | Middleware/wiring | COMP-008, COMP-005, FR-AUTH.4b | Middleware chain executes extractor, verifier, and unauthorized guard in order | M | P0 |
| 28 | MW-002 | Add user-context loading to middleware chain | Middleware/wiring | MW-001, DM-001 | Verified token loads current user context for downstream handlers | S | P0 |
| 29 | DI-001 | Bind JwtService implementation into `SecurityServiceContainer` | Dependency injection | COMP-005, OPS-001 | Runtime container resolves production JwtService successfully | S | P0 |
| 30 | DI-002 | Bind PasswordHasher implementation into `SecurityServiceContainer` | Dependency injection | COMP-006, NFR-AUTH.3 | Runtime container resolves bcrypt hasher with configured cost factor | S | P0 |
| 31 | DI-003 | Bind TokenManager implementation into `SecurityServiceContainer` | Dependency injection | COMP-007, DI-001, DI-002 | Runtime container resolves token manager with JWT/hasher dependencies | S | P0 |
| 32 | DI-004 | Bind RateLimiter implementation into `SecurityServiceContainer` | Dependency injection | FR-AUTH.1d | Runtime container resolves rate limiter for login path | S | P0 |
| 33 | DI-005 | Bind EmailAdapter implementation into `SecurityServiceContainer` | Dependency injection | COMP-009, DEC-001 | Runtime container resolves reset-email adapter with failure semantics | S | P1 |
| 34 | OPS-005 | Implement secure cookie configuration for refresh tokens | Runtime security | FR-AUTH.3a, API-004 | Refresh token is issued in httpOnly cookie with correct security attributes | M | P0 |
| 35 | OPS-006 | Implement access-token TTL and refresh-token TTL configuration | Runtime security | FR-AUTH.1a, FR-AUTH.3a | Access TTL=15m and refresh TTL=7d are externally configurable and enforced | S | P0 |
| 36 | OPS-007 | Implement reset-token TTL configuration | Runtime security | FR-AUTH.5a | Reset token TTL=1 hour is configurable and enforced | S | P1 |
| 37 | OPS-008 | Implement user-session revocation routine | Security operations | FR-AUTH.3c, FR-AUTH.5d, DEC-004 | Single routine can revoke all active user refresh tokens deterministically | M | P0 |
| 38 | NFR-AUTH.3.I1 | Implement bcrypt cost-factor configuration path | Security configuration | NFR-AUTH.3, DI-002 | Runtime uses configurable cost factor defaulting to 12 | S | P0 |
| 39 | NFR-AUTH.1.I1 | Implement performance instrumentation for auth endpoints | Observability | NFR-AUTH.1, API-002, API-004 | Endpoint latency metrics emitted for login and refresh requests | M | P1 |
| 40 | NFR-AUTH.2.I1 | Implement auth-aware health checks and failure reporting | Reliability | NFR-AUTH.2, OPS-004 | Health endpoint reports critical dependency readiness without exposing secrets | M | P1 |

### Timeline estimate

1. **Registration + login**: 3–4 working days
2. **Refresh + replay detection**: 3–4 working days
3. **Profile + password reset + wiring**: 3–4 working days

**Phase estimate**: 2–2.5 weeks

---

## Phase 3 — Validation, resilience, and release hardening

### Milestone
Prove the auth subsystem against all functional, non-functional, migration, rollback, and operational success criteria.

### Phase objectives

1. Execute full verification against FR and NFR criteria.
2. Validate operational behavior under failure and rollback conditions.
3. Close release blockers around latency, migration reversibility, and regression risk.

### Integration points

1. **Named Artifact**: `AuthTestMatrix`
   - **Wired Components**: unit tests, integration tests, security tests, E2E tests, load tests, benchmark tests, rollback tests
   - **Owning Phase**: Phase 3
   - **Cross-Reference**: Consumed in Phase 4 release approval

2. **Named Artifact**: `OperationalReadinessChecklist`
   - **Wired Components**: monitoring, alerts, feature-flag rollback, migration rollback, key-rotation readiness
   - **Owning Phase**: Phase 3
   - **Cross-Reference**: Consumed in Phase 4 cutover and support

### Task table

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | TEST-001 | Create unit tests for registration validation logic | Unit tests | FR-AUTH.2b, FR-AUTH.2c, FR-AUTH.2d, TEST-ARCH-001 | Duplicate email, password policy, and email-format cases are automated | M | P0 |
| 2 | TEST-002 | Create integration tests for successful registration | Integration tests | FR-AUTH.2a, TEST-ARCH-002 | Full registration flow persists user and returns expected response | M | P0 |
| 3 | TEST-003 | Create unit tests for login invalid-credential and locked-account paths | Unit tests | FR-AUTH.1b, FR-AUTH.1c | 401/403 behaviors are validated with enumeration-safe messaging | M | P0 |
| 4 | TEST-004 | Create integration tests for successful login token issuance | Integration tests | FR-AUTH.1a | Valid login returns expected token pair and status code | M | P0 |
| 5 | TEST-005 | Create load tests for login rate limiting | Load tests | FR-AUTH.1d, NFR-AUTH.1.I1 | Sixth request per minute per IP is rejected under scripted load | M | P0 |
| 6 | TEST-006 | Create integration tests for refresh rotation flow | Integration tests | FR-AUTH.3a, OPS-005 | Refresh flow returns rotated token pair and persists new token state | M | P0 |
| 7 | TEST-007 | Create unit tests for expired refresh-token rejection | Unit tests | FR-AUTH.3b | Expired refresh token returns 401 and does not rotate tokens | S | P0 |
| 8 | TEST-008 | Create integration tests for replay detection and full revocation | Security/integration tests | FR-AUTH.3c, OPS-008 | Reuse of rotated token revokes all user sessions deterministically | L | P0 |
| 9 | TEST-009 | Create unit tests for refresh-token hash persistence | Unit tests | FR-AUTH.3d | Persistence layer stores only hashed refresh tokens | S | P0 |
| 10 | TEST-010 | Create integration tests for authenticated profile retrieval | Integration tests | FR-AUTH.4a, MW-002 | Valid bearer token returns expected profile response | S | P0 |
| 11 | TEST-011 | Create unit tests for invalid/expired access-token rejection | Unit tests | FR-AUTH.4b | Invalid and expired access tokens produce 401 responses | S | P0 |
| 12 | TEST-012 | Create security tests for sensitive-field exclusion | Security tests | FR-AUTH.4c | password_hash and token hashes never appear in profile or auth responses | S | P0 |
| 13 | TEST-013 | Create integration tests for password-reset request dispatch | Integration tests | FR-AUTH.5a, DI-005 | Registered email triggers reset dispatch and expected API response | M | P0 |
| 14 | TEST-014 | Create integration tests for password-reset confirmation | Integration tests | FR-AUTH.5b | Valid reset token permits password change once | M | P0 |
| 15 | TEST-015 | Create unit tests for invalid and expired reset tokens | Unit tests | FR-AUTH.5c | Invalid and expired reset tokens return 400 paths as specified | S | P0 |
| 16 | TEST-016 | Create integration tests for session revocation after password reset | Security/integration tests | FR-AUTH.5d, OPS-008 | Existing refresh tokens are unusable after successful password reset | M | P0 |
| 17 | TEST-017 | Create benchmark tests for bcrypt timing | Benchmark tests | NFR-AUTH.3.I1 | Benchmark reports ~250ms/hash at configured cost factor under test environment | M | P0 |
| 18 | TEST-018 | Create load tests for auth endpoint latency | Performance tests | NFR-AUTH.1.I1, NFR-AUTH.1 | k6 suite reports p95 latency against target or captures justified variance | M | P0 |
| 19 | TEST-019 | Create availability and health-check validation tests | Reliability tests | NFR-AUTH.2.I1, NFR-AUTH.2 | Health checks and alert hooks verify dependency readiness behavior | M | P1 |
| 20 | TEST-020 | Create migration forward and rollback tests | Migration tests | MIG-003, MIG-003.DOWN | Up/down migrations execute cleanly in CI database lifecycle | S | P0 |
| 21 | TEST-021 | Create regression suite for pre-existing endpoints | Regression tests | API-001, OPS-003 | Existing endpoints remain green with auth feature enabled and disabled | M | P0 |
| 22 | TEST-022 | Create end-to-end authenticated user lifecycle scenario | E2E tests | FR-AUTH.2a, FR-AUTH.1a, FR-AUTH.3a, FR-AUTH.4a, FR-AUTH.5b | Registration→login→profile→refresh→reset→relogin lifecycle passes | L | P0 |
| 23 | SC-1 | Validate all FR-AUTH.1 criteria to green | Release validation | TEST-003, TEST-004, TEST-005 | 4/4 login acceptance criteria pass in CI evidence set | S | P0 |
| 24 | SC-2 | Validate all FR-AUTH.2 criteria to green | Release validation | TEST-001, TEST-002 | 4/4 registration acceptance criteria pass in CI evidence set | S | P0 |
| 25 | SC-3 | Validate all FR-AUTH.3 criteria to green | Release validation | TEST-006, TEST-007, TEST-008, TEST-009 | 4/4 refresh acceptance criteria pass in CI evidence set | S | P0 |
| 26 | SC-4 | Validate all FR-AUTH.4 criteria to green | Release validation | TEST-010, TEST-011, TEST-012 | 3/3 profile acceptance criteria pass in CI evidence set | S | P0 |
| 27 | SC-5 | Validate all FR-AUTH.5 criteria to green | Release validation | TEST-013, TEST-014, TEST-015, TEST-016 | 4/4 password-reset acceptance criteria pass in CI evidence set | S | P0 |
| 28 | SC-6 | Validate end-to-end user lifecycle scenario | Release validation | TEST-022 | Six-step lifecycle passes with expected statuses and token transitions | S | P0 |
| 29 | SC-7 | Validate zero sensitive-field leakage across responses | Security validation | TEST-012 | Security scan/test evidence reports 0 leaked sensitive fields | S | P0 |
| 30 | SC-8 | Validate authentication endpoint p95 latency target | Performance validation | TEST-018, NFR-AUTH.1 | Evidence records <200ms p95 or approved exception/decision note | M | P0 |
| 31 | SC-9 | Validate 99.9% availability readiness | Reliability validation | TEST-019, NFR-AUTH.2 | Monitoring and alerting evidence supports 99.9% operational posture | M | P1 |
| 32 | SC-10 | Validate bcrypt cost factor equals 12 | Security validation | TEST-017, NFR-AUTH.3 | Automated assertion confirms cost factor configuration equals 12 | S | P0 |
| 33 | SC-11 | Validate bcrypt timing benchmark | Security/performance validation | TEST-017 | Benchmark evidence shows timing near 250ms/hash with documented environment | S | P0 |
| 34 | SC-12 | Validate zero breaking changes to existing endpoints | Regression validation | TEST-021 | Pre-existing integration suite remains fully green | S | P0 |
| 35 | SC-13 | Validate feature-flag rollback behavior | Operational rollback | OPS-003, TEST-021 | Disabling auth flag restores pre-auth behavior without deployment rollback | S | P0 |
| 36 | SC-14 | Validate reversible migrations | Migration validation | TEST-020 | Down migration drops auth tables cleanly and repeatably | S | P0 |
| 37 | R-1 | Execute secrets and key-custody review for JWT signing | Security review | OPS-001, OPS-002 | Review confirms private key not stored in code/env and rotation path exists | M | P0 |
| 38 | R-2 | Execute replay-attack resilience review | Security review | FR-AUTH.3c, TEST-008 | Review confirms replay attempt triggers full revocation with no reuse gap | M | P0 |
| 39 | R-3 | Execute password-hash future-proofing review | Security review | NFR-AUTH.3.I1, TEST-017 | Review confirms configurable cost factor and annual review mechanism | S | P1 |
| 40 | R-4 | Execute latency-conflict decision validation | Architecture review | NFR-AUTH.1, TEST-018 | Chosen mitigation is validated and documented for release approval | M | P0 |
| 41 | R-5 | Execute email-dependency failure-mode validation | Resilience review | DI-005, TEST-013 | Reset-request flow exhibits approved failure behavior when email service is unavailable | M | P1 |
| 42 | R-6 | Execute brute-force mitigation gap review | Security review | FR-AUTH.1d, DEC-003 | Residual risk of distributed brute force is documented with approved disposition | M | P1 |
| 43 | OQ-1 | Close email dispatch mode question with implementation evidence | Architecture closure | DEC-001, TEST-013 | Reset-email mode is final, implemented, and validated | S | P0 |
| 44 | OQ-2 | Close refresh-token concurrency question with runtime policy evidence | Architecture closure | DEC-002, FR-AUTH.3c | Active-session limit policy is implemented and validated | S | P1 |
| 45 | OQ-3 | Close latency contradiction with measured evidence | Architecture closure | DEC-001, NFR-AUTH.1, TEST-018 | Signed-off resolution exists for bcrypt vs p95 contradiction | S | P0 |
| 46 | OQ-4 | Close account lockout policy question | Security closure | DEC-003, R-6 | v1 posture on account-level lockout is explicitly approved | S | P1 |
| 47 | OQ-5 | Close token revocation on user deletion question | Lifecycle closure | DEC-004, OPS-008 | User-deletion token behavior is documented and testable | S | P1 |
| 48 | OQ-6 | Close audit-logging question for auth events | Observability closure | NFR-AUTH.2.I1 | Explicit decision recorded for logging inclusion or deferment | S | P2 |
| 49 | OQ-7 | Close email service interface question | Integration closure | COMP-009, DI-005 | Email service contract is fully specified and implemented | S | P0 |
| 50 | OQ-8 | Close RSA key-rotation procedure question | Security closure | OPS-002, R-1 | Rotation/versioning procedure is operationally documented and approved | S | P0 |

### Timeline estimate

1. **Functional/security test implementation**: 1–1.5 weeks
2. **Performance/reliability/regression validation**: 0.5–1 week
3. **Risk/open-question closure and release evidence**: 0.5 week

**Phase estimate**: 2–2.5 weeks

---

# 3. Risk assessment and mitigation strategies

## 3.1 Primary risks

1. **R-1: JWT key compromise**
   - **Impact**: Unauthorized token minting and broad privilege abuse.
   - **Mitigation**:
     - RS256 asymmetric signing only
     - secrets-manager retrieval at startup/runtime
     - key versioning and 90-day rotation
     - no private key in code or plain env vars
   - **Architect recommendation**: Release should be blocked if key versioning is not operationally defined.

2. **R-2: Refresh-token replay**
   - **Impact**: Persistent unauthorized sessions after token theft.
   - **Mitigation**:
     - rotation on every refresh
     - hashed refresh-token storage
     - replay detection path
     - full session revocation on suspicious reuse
   - **Architect recommendation**: Treat replay tests as mandatory P0 gating.

3. **R-4: Latency contradiction**
   - **Impact**: Spec cannot satisfy both bcrypt security target and p95 latency target simultaneously without explicit architectural treatment.
   - **Mitigation**:
     - decision record in Phase 1
     - instrumentation in Phase 2
     - measured validation in Phase 3
   - **Architect recommendation**: Do not silently “best effort” this requirement; force a stakeholder decision.

4. **R-5: Email dependency fragility**
   - **Impact**: Password reset becomes unavailable or user-visible failures increase.
   - **Mitigation**:
     - explicit adapter contract
     - sync/async decision
     - graceful failure behavior
     - retry/queue if async path chosen
   - **Architect recommendation**: Prefer async dispatch if infrastructure exists; otherwise document synchronous latency/availability tradeoff.

5. **R-6: Brute-force residual risk**
   - **Impact**: Distributed attacks bypass per-IP throttling.
   - **Mitigation**:
     - ship per-IP rate limiting in v1
     - explicitly decide whether account-level lockout is in scope
     - capture residual risk if deferred
   - **Architect recommendation**: At minimum, document the gap and attach follow-up ownership.

## 3.2 Secondary delivery risks

1. Migration reversibility not actually tested.
2. Feature flag rollback not exercised before release.
3. Profile endpoint accidentally leaking internal fields.
4. Secrets manager integration behaving differently across environments.
5. Session concurrency policy left undefined, causing storage or UX issues.

---

# 4. Resource requirements and dependencies

## 4.1 Engineering roles

1. **Backend engineer**
   - Schema, services, middleware, routes, token lifecycle, reset flow
2. **Security engineer / reviewer**
   - key management, replay detection, enumeration resistance, cookie security
3. **QA / SDET**
   - integration, E2E, security, load, and benchmark validation
4. **Platform / DevOps support**
   - secrets manager access, health checks, monitoring, rollout controls

## 4.2 External dependencies

1. **Libraries**
   - `jsonwebtoken`
   - `bcrypt`

2. **Services**
   - Email service for reset dispatch
   - Secrets manager for RSA key storage/retrieval

3. **Infrastructure**
   - SQL database with UUID support
   - migration execution environment
   - load-test environment
   - monitoring/alerting stack
   - RSA key-pair generation and rotation process

## 4.3 Environment prerequisites

1. Non-production secrets-manager integration for testing
2. Test email sink or mockable adapter boundary
3. CI support for migration up/down tests
4. Performance test harness with k6
5. Benchmark environment stable enough to interpret bcrypt timing

## 4.4 Critical dependency sequencing

1. Schema and migration readiness before integration tests
2. Secrets integration before login/refresh implementation
3. Email contract decision before password reset completion
4. Latency decision before NFR signoff
5. Feature flag and health checks before production rollout

---

# 5. Success criteria and validation approach

## 5.1 Functional validation

1. Validate every FR acceptance criterion independently.
2. Preserve one row of evidence per ID:
   - FR-AUTH.1a–d
   - FR-AUTH.2a–d
   - FR-AUTH.3a–d
   - FR-AUTH.4a–c
   - FR-AUTH.5a–d

## 5.2 Non-functional validation

1. **NFR-AUTH.1**
   - k6 load test on login and refresh
   - APM instrumentation in deployed environment
   - explicit exception note if target is infeasible under accepted bcrypt posture

2. **NFR-AUTH.2**
   - health check coverage
   - dependency readiness validation
   - alerting runbook readiness

3. **NFR-AUTH.3**
   - automated cost-factor assertion
   - benchmark evidence of approximate hashing time

## 5.3 Deployment validation

1. Run regression suite with auth enabled.
2. Run rollback validation with `AUTH_SERVICE_ENABLED` disabled.
3. Run migration up/down in isolated database lifecycle.
4. Confirm route registration does not disrupt pre-existing paths.

## 5.4 Release gate recommendation

Release only when all are true:

1. SC-1 through SC-14 are green or have formally approved exceptions.
2. OQ-1, OQ-3, OQ-7, and OQ-8 are closed.
3. R-1, R-2, and R-4 reviews are complete.
4. Feature flag rollback and migration rollback are proven.
5. Security-sensitive response-schema leakage tests are green.

---

# 6. Timeline estimates per phase

## Phase 1 — Architecture, data model, and security foundations
- **Estimate**: 1.5–2 weeks
- **Exit criteria**:
  1. schema and migration design complete
  2. route skeletons and middleware contract in place
  3. wiring artifacts explicitly defined
  4. key architecture decisions closed or escalated

## Phase 2 — Core authentication feature implementation
- **Estimate**: 2–2.5 weeks
- **Exit criteria**:
  1. all FR flows implemented
  2. route registry and service container populated
  3. replay detection and reset invalidation functioning
  4. cookie, TTL, and revocation controls active

## Phase 3 — Validation, resilience, and release hardening
- **Estimate**: 2–2.5 weeks
- **Exit criteria**:
  1. SC-1 through SC-14 validated
  2. risk reviews complete
  3. rollback and migration reversibility proven
  4. open questions resolved or formally deferred

## Overall roadmap estimate
- **Total**: approximately **5.5–7 weeks**

## Suggested milestone checkpoints

1. **Checkpoint A**
   - End of Phase 1
   - Architecture and security foundation approved

2. **Checkpoint B**
   - Mid Phase 2
   - Registration/login/refresh flows functional in integration environment

3. **Checkpoint C**
   - End of Phase 2
   - Full feature set implemented and wired

4. **Checkpoint D**
   - End of Phase 3
   - Validation evidence complete and release-ready

---

# Architect recommendations

1. Resolve the **bcrypt vs latency** contradiction first; it influences performance design, acceptance expectations, and stakeholder trust.
2. Treat **replay detection**, **key rotation**, and **session revocation** as first-class architecture, not edge cases.
3. Keep **route/DI/middleware wiring explicit** through named artifacts to avoid hidden integration debt.
4. Do not release password reset until the **email contract** and **failure mode** are fully defined.
5. Preserve the **v1 scope boundary**:
   - no OAuth
   - no MFA
   - no RBAC
   - no social login
   - no speculative extras unless an open question is explicitly resolved into scope.
