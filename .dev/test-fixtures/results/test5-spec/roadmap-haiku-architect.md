---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
---

# 1. Executive summary

This roadmap delivers a secure, testable, rollback-safe authentication subsystem centered on RS256 JWTs, bcrypt password hashing, refresh-token rotation, and password reset flows. From an architecture perspective, the critical path is:

1. Establish the security and data foundations first:
   - asymmetric key management
   - durable schema and rollback-ready migrations
   - injectable crypto and token services

2. Build orchestration and request-path integration second:
   - auth service coordination
   - middleware enforcement
   - route registration under feature-flag control

3. Prove correctness and operability before broad rollout:
   - replay detection
   - latency validation
   - uptime instrumentation
   - rollback drills
   - phased enforcement for protected endpoints

Key architectural priorities:

- Preserve stateless access-token architecture while introducing stateful revocation only where required for refresh and reset flows.
- Isolate sensitive responsibilities into independently testable components: PasswordHasher, JwtService, TokenManager, AuthService, AuthMiddleware, AuthRoutes, AuthMigration.
- Make wiring explicit: route registry, middleware chain, dependency-injection bindings, feature-flag gating, and repository integration must each be owned by a defined phase.
- Address the highest-severity risks early:
  - RISK-1 key compromise
  - RISK-2 refresh replay
  - RISK-3 future password-hash erosion

Because the input has relatively few formal IDs but substantial architectural detail, the roadmap expands implementation into 40 granular task rows while preserving every extraction ID as its own row and adding explicit COMP/API/DM/TEST/MIG/OPS entities needed for full architectural coverage.

# 2. Phased implementation plan with milestones

## Phase 1 — Foundations, security baselines, and schema readiness

### Milestones
1. Security decisions codified for RS256, bcrypt cost factor 12, token storage, and secrets handling.
2. Core schema and migration rollback path implemented.
3. Foundational components scaffolded as injectable, independently testable units.
4. Delivery dependencies and unresolved architecture questions surfaced early.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | DM-001 | Define users table schema | Database / users table |  | Schema: id (UUID PK), email (unique varchar/index), display_name (varchar), password_hash (varchar), is_locked (boolean), created_at (timestamptz), updated_at (timestamptz); unique constraint on email documented; schema reviewed against FR-AUTH.2 and FR-AUTH.4 response fields | M | P0 |
| 2 | DM-002 | Define refresh_tokens table schema | Database / refresh_tokens table | DM-001 | Schema: id (UUID PK), user_id (UUID FK -> users.id), refresh_token_hash (char/varchar SHA-256), issued_at (timestamptz), expires_at (timestamptz), revoked_at (timestamptz nullable), replaced_by_token_id (UUID nullable self-reference), created_ip (inet/varchar nullable), user_agent (varchar nullable); supports rotation and replay detection | M | P0 |
| 3 | DM-003 | Define password_reset_tokens table schema | Database / password_reset_tokens table | DM-001 | Schema: id (UUID PK), user_id (UUID FK -> users.id), reset_token_hash (char/varchar), expires_at (timestamptz), consumed_at (timestamptz nullable), created_at (timestamptz); enforces 1-hour TTL and single-use semantics for FR-AUTH.5 | M | P0 |
| 4 | MIG-001 | Author up migration for auth schema | Migration / up path | DM-001, DM-002, DM-003 | Creates users, refresh_tokens, password_reset_tokens tables; creates email uniqueness and token lookup indexes; applies foreign keys and nullable columns exactly as schema definitions specify | M | P0 |
| 5 | MIG-002 | Author down migration for auth schema | Migration / down path | MIG-001 | Down migration removes password_reset_tokens, refresh_tokens, then users in reverse dependency order without orphaned objects; satisfies AC-9 rollback requirement | S | P0 |
| 6 | COMP-007 | Implement AuthMigration component | Migration module `src/database/migrations/003-auth-tables.ts` | MIG-001, MIG-002 | Component exposes executable up/down migration entrypoints; encapsulates creation of users, refresh_tokens, password_reset_tokens artifacts; migration can be invoked independently in tests | S | P0 |
| 7 | DEP-4 | Confirm relational database engine assumptions | Database platform | DM-001, DM-002, DM-003 | Target engine decision documented or compatibility matrix produced for PostgreSQL/MySQL/SQLite differences in UUIDs, indexes, timestamp types, and migration syntax; blocker status for production rollout made explicit | S | P0 |
| 8 | DEP-5 | Integrate secrets manager contract | Secrets management |  | Interface defined for retrieving RSA private key and active/public verification material; no key material stored in source or static config; aligns with AC-6 | M | P0 |
| 9 | DEP-1 | Baseline jsonwebtoken dependency usage | JWT library integration |  | Selected package version supports RS256 sign/verify and key rotation strategy; usage constraints documented for COMP-002; installation and compatibility confirmed | S | P1 |
| 10 | DEP-2 | Baseline bcrypt dependency usage | Password hashing library integration |  | Selected package version supports configurable cost factor 12 and compare operation; benchmark approach defined for NFR-AUTH.3 | S | P1 |
| 11 | DEP-3 | Define email service integration contract | Email integration |  | Interface for reset email dispatch defined with inputs: recipient_email, reset_url/token, expiry; failure modes and timeout expectations documented for FR-AUTH.5 | S | P1 |
| 12 | COMP-001 | Implement PasswordHasher component | `src/auth/password-hasher.ts` | DEP-2 | Component provides hash(password) and compare(password, password_hash) with bcrypt cost factor 12, dependency injection support, and deterministic test seams; all public operations independently unit-testable | M | P0 |
| 13 | COMP-002 | Implement JwtService component | `src/auth/jwt-service.ts` | DEP-1, DEP-5 | Component provides RS256 sign and verify for access, refresh, and reset tokens using secrets-manager supplied key material; no HS256 path present; injectable and independently testable | M | P0 |
| 14 | COMP-008 | Define UserRepository abstraction | Persistence / repository layer | DM-001, DEP-4 | Repository contract covers createUser, findByEmail, findById, updatePasswordHash, setLockStatus, and profile projection; interfaces injectable and mockable without coupling to service code | M | P0 |
| 15 | COMP-009 | Define RefreshTokenRepository abstraction | Persistence / repository layer | DM-002, DEP-4 | Repository contract covers createTokenRecord, findByHash, revokeToken, revokeAllForUser, markRotation, detectReuseChain, and purgeExpired; supports FR-AUTH.3 rotation and replay detection | M | P0 |
| 16 | COMP-010 | Define PasswordResetRepository abstraction | Persistence / repository layer | DM-003, DEP-4 | Repository contract covers createResetToken, findValidResetToken, consumeResetToken, invalidateUserResetTokens; supports single-use reset semantics | M | P1 |
| 17 | OPS-001 | Define feature flag rollout control | Config / feature flags |  | `AUTH_SERVICE_ENABLED` flag semantics documented for route enablement, rollback, and phase-1 opt-in behavior per AC-8 and AC-10 | S | P0 |
| 18 | OQ-3 | Resolve target database engine question | Architecture decision log | DEP-4 | Decision recorded with impact on UUID generation, index syntax, and migration dialect; if unresolved, explicit compatibility work item retained before production cutover | S | P1 |
| 19 | OQ-7 | Resolve RSA key size question | Security architecture | DEP-5, COMP-002 | Selected key length documented (for example 2048-bit or 4096-bit) with tradeoff rationale covering security strength and signing latency; verification path updated accordingly | S | P1 |
| 20 | AC-5 | Enforce injectable testable component design | Architecture standards | COMP-001, COMP-002, COMP-008, COMP-009, COMP-010 | Constructors/contracts for core components avoid hard-coded singletons; each component can be instantiated with test doubles; unit test strategy references independent testability | M | P0 |

### Integration points for Phase 1

1. **Named Artifact**: Dependency Injection Container / Service Registry  
   - **Wired Components**: PasswordHasher (COMP-001), JwtService (COMP-002), UserRepository (COMP-008), RefreshTokenRepository (COMP-009), PasswordResetRepository (COMP-010)  
   - **Owning Phase**: Phase 1  
   - **Cross-Reference**: Consumed by Phase 2 for TokenManager/AuthService assembly and by Phase 3 for middleware/routes

2. **Named Artifact**: Migration Registry / Migration Runner  
   - **Wired Components**: MIG-001, MIG-002, COMP-007  
   - **Owning Phase**: Phase 1  
   - **Cross-Reference**: Consumed by Phase 4 rollback validation and deployment runbooks

3. **Named Artifact**: Feature Flag Configuration `AUTH_SERVICE_ENABLED`  
   - **Wired Components**: COMP-006 AuthRoutes, protected-route enablement controls  
   - **Owning Phase**: Phase 1  
   - **Cross-Reference**: Consumed by Phase 3 route exposure and Phase 5 rollout

---

## Phase 2 — Token lifecycle and authentication orchestration

### Milestones
1. Token issuance, verification, rotation, revocation, and replay detection implemented.
2. Registration, login, refresh, profile, and reset orchestration completed in AuthService.
3. Primary functional requirements satisfied at service level.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | COMP-003 | Implement TokenManager component | `src/auth/token-manager.ts` | COMP-002, COMP-009, DM-002 | Component issues access tokens (15 min TTL), refresh tokens (7 day TTL), stores SHA-256 refresh token hashes, rotates refresh tokens, revokes old tokens, and triggers full-user revocation on replay detection; independently testable | L | P0 |
| 2 | COMP-004 | Implement AuthService orchestrator | `src/auth/auth-service.ts` | COMP-001, COMP-003, COMP-008, COMP-009, COMP-010, DEP-3 | Component coordinates register, login, refresh, profile, password-reset-request, password-reset-confirm flows using injected collaborators; no direct crypto or DB hard-coding | L | P0 |
| 3 | FR-AUTH.2 | Implement user registration flow | AuthService / registration | COMP-004, COMP-001, COMP-008, DM-001 | Valid email, password, and display name create user record and return 201 profile; duplicate email returns 409; password policy enforced (min 8, upper, lower, digit); malformed email rejected before persistence | M | P0 |
| 4 | FR-AUTH.1 | Implement login flow | AuthService / login | COMP-004, COMP-001, COMP-003, COMP-008, FR-AUTH.2 | Valid email/password returns access token (15 min TTL) and refresh token (7 day TTL); invalid credentials return generic 401; locked account returns 403; rate-limited path delegates to request layer | L | P0 |
| 5 | FR-AUTH.3 | Implement token refresh flow | TokenManager / AuthService | COMP-003, COMP-004, COMP-009, DM-002 | Valid refresh token returns new access token and rotated refresh token; expired token returns 401; reused rotated token triggers full user token revocation; hashed refresh token persisted | L | P0 |
| 6 | FR-AUTH.4 | Implement profile retrieval flow | AuthService / profile | COMP-004, COMP-008 | Valid authenticated request returns id, email, display_name, created_at only; invalid/expired access token handled by middleware path; sensitive fields excluded | M | P1 |
| 7 | FR-AUTH.5 | Implement password reset flow | AuthService / password reset | COMP-004, COMP-001, COMP-003, COMP-010, COMP-009, DEP-3, DM-003 | Registered email triggers reset token generation with 1-hour TTL and email dispatch; valid reset token updates password, invalidates token, and revokes all refresh tokens; invalid/expired token returns 400 | L | P1 |
| 8 | API-001 | Define POST /auth/register contract | API / registration endpoint | FR-AUTH.2 | Request schema includes email, password, display_name; success response 201 returns profile fields id, email, display_name, created_at; error contracts cover 409 and validation failures | S | P0 |
| 9 | API-002 | Define POST /auth/login contract | API / login endpoint | FR-AUTH.1 | Request schema includes email and password; success response 200 returns access_token and refresh_token; error contracts cover 401, 403, 429 with generic invalid-credentials wording | S | P0 |
| 10 | API-003 | Define POST /auth/refresh contract | API / refresh endpoint | FR-AUTH.3 | Request contract accepts refresh token via httpOnly cookie or equivalent adapter contract; success response returns rotated access_token and refresh token; error contracts cover 401 and replay revocation semantics | S | P0 |
| 11 | API-004 | Define GET /auth/profile contract | API / profile endpoint | FR-AUTH.4 | Requires Bearer access token; success schema contains id, email, display_name, created_at only; 401 returned for invalid/expired tokens | S | P1 |
| 12 | API-005 | Define POST /auth/password-reset/request contract | API / reset request endpoint | FR-AUTH.5 | Request schema accepts email; success contract avoids account enumeration; reset token TTL and email dispatch behavior documented; dependency on email service explicit | S | P1 |
| 13 | API-006 | Define POST /auth/password-reset/confirm contract | API / reset confirm endpoint | FR-AUTH.5 | Request schema accepts reset_token and new_password; success contract invalidates token and sessions; invalid/expired token returns 400 | S | P1 |
| 14 | AC-1 | Enforce RS256-only token signing | JwtService / TokenManager | COMP-002, COMP-003 | Access, refresh, and reset tokens are signed and verified exclusively with RS256; no symmetric signing code path remains; tests assert algorithm selection | M | P0 |
| 15 | AC-2 | Enforce bcrypt cost factor 12 | PasswordHasher | COMP-001 | Hashing configuration fixed/configurable at cost factor 12 and referenced by tests/benchmarks; no weaker default present | S | P0 |
| 16 | AC-3 | Enforce token storage strategy | API / client contract | API-002, API-003, API-004 | Access token usage documented for in-memory client storage only; refresh token transport modeled as httpOnly cookie; profile endpoint does not rely on refresh token in JS-visible storage | M | P1 |
| 17 | AC-4 | Preserve stateless access token architecture | Auth architecture | COMP-003, COMP-005 | Access-token validation requires no server-side session store; only refresh/reset revocation state persisted; architecture note and tests confirm stateless access path | M | P0 |
| 18 | OQ-1 | Resolve reset email delivery mode | Architecture decision / email integration | DEP-3, FR-AUTH.5 | Decision recorded between synchronous dispatch and queue-based dispatch with impact on endpoint latency, resilience, and failure handling; chosen mode reflected in API contract and ops plan | S | P1 |
| 19 | OQ-2 | Resolve active refresh token cap per user | Token policy | COMP-003, DM-002 | Maximum active refresh-token count per user explicitly defined; repository and revocation behavior updated to support chosen multi-device policy | S | P1 |
| 20 | RISK-2 | Implement replay-attack mitigation path | Token security | COMP-003, FR-AUTH.3, DM-002 | Refresh token rotation, replaced_by_token_id lineage, old-token invalidation, and full-user revocation on reused token are implemented and testable end-to-end | L | P0 |

### Integration points for Phase 2

1. **Named Artifact**: Token Lifecycle Policy / Strategy  
   - **Wired Components**: JwtService (COMP-002), TokenManager (COMP-003), RefreshTokenRepository (COMP-009), API-003 refresh endpoint  
   - **Owning Phase**: Phase 2  
   - **Cross-Reference**: Consumed by Phase 3 middleware verification and Phase 4 security/integration tests

2. **Named Artifact**: AuthService Orchestration Graph  
   - **Wired Components**: PasswordHasher, TokenManager, UserRepository, RefreshTokenRepository, PasswordResetRepository, Email service adapter  
   - **Owning Phase**: Phase 2  
   - **Cross-Reference**: Consumed by Phase 3 route/controller bindings and Phase 4 test harnesses

3. **Named Artifact**: API Contract Registry for `/auth/*`  
   - **Wired Components**: API-001 through API-006  
   - **Owning Phase**: Phase 2  
   - **Cross-Reference**: Consumed by Phase 3 route registration and client integration guidance

---

## Phase 3 — Request-path integration, middleware wiring, and protected endpoint rollout

### Milestones
1. Middleware and route registration completed.
2. Rate limiting and feature-flag gating integrated into live request path.
3. Protected endpoints can opt in during phase 1 and become mandatory in phase 2 rollout.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | COMP-005 | Implement AuthMiddleware component | `src/middleware/auth-middleware.ts` | COMP-003, API-004 | Middleware extracts Bearer token, verifies access token, attaches authenticated user context, and returns 401 for invalid/expired tokens; independently testable | M | P0 |
| 2 | COMP-006 | Implement AuthRoutes component | `src/routes/index.ts` | COMP-004, COMP-005, API-001, API-002, API-003, API-004, API-005, API-006, OPS-001 | `/auth/*` route group registered behind `AUTH_SERVICE_ENABLED`; protected profile route applies middleware; route handlers delegate to AuthService only | M | P0 |
| 3 | COMP-011 | Implement request validation layer | API boundary / validators | API-001, API-002, API-005, API-006 | Validators enforce email format, password policy, required fields, and request schema consistency before service execution; malformed payloads rejected predictably | M | P1 |
| 4 | COMP-012 | Implement login rate limiter | Middleware / abuse protection | API-002 | Login attempts limited to 5/minute/IP with 429 on 6th attempt within 60 seconds; limiter scope and reset window documented | M | P0 |
| 5 | FR-AUTH.1d | Wire rate limiting into login endpoint | Login request path | COMP-012, COMP-006, FR-AUTH.1 | `POST /auth/login` enforces 5 attempts/minute/IP and returns 429 on threshold breach before credential processing | S | P0 |
| 6 | FR-AUTH.4a | Expose authenticated profile response | Profile route | COMP-005, COMP-006, FR-AUTH.4 | Valid Bearer token returns profile fields id, email, display_name, created_at exactly; no extra sensitive fields appear | S | P1 |
| 7 | FR-AUTH.4b | Enforce unauthorized response behavior on profile | Profile route | COMP-005, COMP-006 | Expired or invalid token returns 401 consistently through middleware path | S | P1 |
| 8 | FR-AUTH.4c | Exclude sensitive fields from profile output | Serialization / response mapping | FR-AUTH.4, COMP-004, COMP-006 | password_hash, refresh_token_hash, reset_token_hash, and other internal token state are absent from profile responses | S | P1 |
| 9 | AC-8 | Gate auth routing with feature flag | Route registration / config | OPS-001, COMP-006 | `AUTH_SERVICE_ENABLED` controls exposure of `/auth/*` routes and allows rollback without code removal; on/off states validated | S | P0 |
| 10 | AC-10 | Support phased auth enforcement rollout | Middleware adoption plan | COMP-005, COMP-006, OPS-001 | Phase 1 keeps authentication opt-in; Phase 2 requires middleware on protected endpoints; enforcement matrix documented and routable by config | M | P0 |
| 11 | COMP-013 | Implement auth context attachment model | Request context / middleware output | COMP-005, COMP-008 | Authenticated request context contains user_id, token_subject, token_expiry, and authorization status for downstream handlers; no sensitive token material propagated | S | P1 |
| 12 | COMP-014 | Implement route-handler adapter layer | Controller / handler bindings | COMP-006, COMP-004 | Handlers translate HTTP input/output to service calls, status codes, and cookie/header behavior without embedding business logic | M | P1 |
| 13 | COMP-015 | Implement error mapping strategy | API error handling | COMP-014, FR-AUTH.1, FR-AUTH.2, FR-AUTH.3, FR-AUTH.5 | Domain errors map to 400/401/403/409/429 without credential leakage; generic invalid-login messaging preserved | M | P0 |
| 14 | OPS-002 | Define health-check strategy for auth availability | Operations / monitoring | COMP-006 | Health endpoint or auth dependency checks defined to support uptime monitoring and PagerDuty alerting for NFR-AUTH.2 | S | P1 |
| 15 | OQ-4 | Resolve account lockout policy beyond rate limiting | Security policy | COMP-012, FR-AUTH.1d | Decision recorded on whether progressive per-account lockout is in v1.0 or deferred; residual risk accepted or implementation task added with owner | S | P1 |
| 16 | GAP-1 | Address lockout-policy gap | Security controls | OQ-4, FR-AUTH.1d | Gap disposition documented: either progressive lockout implemented with thresholds or explicit deferral/risk acceptance captured for release review | S | P1 |
| 17 | AC-6 | Enforce private-key isolation in secrets manager | Security operations / JwtService | DEP-5, COMP-002 | Runtime path loads RSA private key from secrets manager only; no key material in repository, env file templates, or source config | M | P0 |
| 18 | AC-7 | Implement 90-day key rotation process | Security operations / key management | AC-6, COMP-002 | Rotation procedure defined with activation, verification, overlap/rollout, and rollback steps; 90-day cadence scheduled and testable in staging | M | P1 |
| 19 | RISK-1 | Mitigate key compromise risk | Security architecture | AC-1, AC-6, AC-7 | Asymmetric key model, secrets-manager storage, and rotation controls collectively reduce forged-token blast radius; incident response path documented | M | P0 |
| 20 | COMP-016 | Wire cookie/header transport handling | HTTP transport layer | API-002, API-003, AC-3 | Login/refresh handlers set and consume refresh-token transport according to httpOnly cookie strategy while access token remains Bearer-based for protected endpoints | M | P1 |

### Integration points for Phase 3

1. **Named Artifact**: Route Registry `src/routes/index.ts`  
   - **Wired Components**: AuthRoutes (COMP-006), route-handler adapters (COMP-014), feature flag `AUTH_SERVICE_ENABLED`, API-001..API-006  
   - **Owning Phase**: Phase 3  
   - **Cross-Reference**: Consumed by Phase 4 integration/performance tests and Phase 5 rollout

2. **Named Artifact**: Middleware Chain for protected endpoints  
   - **Wired Components**: AuthMiddleware (COMP-005), auth context model (COMP-013), error mapping strategy (COMP-015)  
   - **Owning Phase**: Phase 3  
   - **Cross-Reference**: Consumed by Phase 4 validation of protected-resource access and Phase 5 enforcement expansion

3. **Named Artifact**: Abuse-Protection Registry / Rate Limiter  
   - **Wired Components**: Login rate limiter (COMP-012), login route API-002  
   - **Owning Phase**: Phase 3  
   - **Cross-Reference**: Consumed by Phase 4 load/security tests and release readiness review

4. **Named Artifact**: Key Management Rotation Runbook  
   - **Wired Components**: Secrets manager integration, JwtService verification material, ops rotation schedule  
   - **Owning Phase**: Phase 3  
   - **Cross-Reference**: Consumed by Phase 5 operations handoff and ongoing compliance reviews

---

## Phase 4 — Validation, non-functional hardening, and release readiness

### Milestones
1. Functional correctness validated with unit, integration, and security-focused tests.
2. Performance, availability, and crypto-cost targets measured.
3. Rollback readiness and deferred-gap handling documented for release governance.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | TEST-001 | Create registration unit test suite | Tests / registration | FR-AUTH.2, API-001 | Covers successful registration, duplicate email 409, password policy failures, malformed email rejection, and created profile shape | M | P0 |
| 2 | TEST-002 | Create login unit test suite | Tests / login | FR-AUTH.1, API-002 | Covers valid credential login, generic 401 behavior, locked-account 403, token TTL assertions, and no credential leakage in errors | M | P0 |
| 3 | TEST-003 | Create refresh rotation unit test suite | Tests / token refresh | FR-AUTH.3, COMP-003 | Covers valid refresh rotation, expired refresh 401, revoked-token rejection, replay-triggered full-user revocation, and hashed token persistence | L | P0 |
| 4 | TEST-004 | Create profile access unit test suite | Tests / profile | FR-AUTH.4, COMP-005 | Covers valid profile retrieval, invalid token 401, and exclusion of password_hash / refresh_token_hash from response | M | P1 |
| 5 | TEST-005 | Create password reset unit test suite | Tests / password reset | FR-AUTH.5, API-005, API-006 | Covers reset request token creation, email dispatch invocation, valid reset completion, expired/invalid reset token 400, and session invalidation | L | P1 |
| 6 | TEST-006 | Create middleware integration test suite | Tests / middleware and routes | COMP-005, COMP-006 | Verifies Bearer extraction, authenticated context propagation, route protection, and status code mapping in live request pipeline | M | P0 |
| 7 | TEST-007 | Create migration up/down test suite | Tests / migrations | COMP-007, MIG-001, MIG-002 | Verifies schema creation and rollback on target DB engine; no residual auth tables/indexes remain after down migration | M | P0 |
| 8 | TEST-008 | Create rate-limit integration test suite | Tests / abuse protection | FR-AUTH.1d, COMP-012 | Verifies 429 on 6th login attempt from same IP within 60 seconds and reset behavior after window expiry | M | P0 |
| 9 | TEST-009 | Create load test for auth latency | Performance tests | NFR-AUTH.1, API-002, API-003 | k6 or equivalent demonstrates auth endpoint p95 latency < 200ms under normal load; results captured for release signoff | M | P0 |
| 10 | TEST-010 | Create uptime and health-check validation | Reliability tests / ops | NFR-AUTH.2, OPS-002 | Monitoring path validates health endpoint behavior and alertability to support 99.9% uptime objective | S | P1 |
| 11 | TEST-011 | Create bcrypt cost factor benchmark | Security/performance tests | NFR-AUTH.3, COMP-001, AC-2 | Benchmark verifies bcrypt cost factor 12 and approximate 250ms/hash envelope; deviations reported as release blockers | S | P0 |
| 12 | NFR-AUTH.1 | Validate authentication endpoint response time | Performance engineering | TEST-009, COMP-003, COMP-004, COMP-006 | p95 latency under 200ms confirmed under normal load and bottlenecks identified/remediated if exceeded | M | P0 |
| 13 | NFR-AUTH.2 | Validate service availability target | Reliability engineering | TEST-010, OPS-002 | Monitoring, health checks, and alert routing support 99.9% uptime objective with documented SLO ownership | M | P1 |
| 14 | NFR-AUTH.3 | Validate password hashing security target | Security engineering | TEST-011, COMP-001 | Cost factor 12 is enforced and benchmarked; security/performance tradeoff accepted for production | S | P0 |
| 15 | SC-1 | Verify login success criterion | Release validation / login | TEST-002 | HTTP 200 with access_token 15-minute TTL and refresh_token 7-day TTL demonstrated in unit and integration evidence | S | P0 |
| 16 | SC-11 | Verify replay detection success criterion | Release validation / refresh security | TEST-003 | Reuse of rotated token revokes all user tokens and produces expected defensive behavior in test evidence | S | P0 |
| 17 | SC-20 | Verify latency success criterion | Release validation / performance | TEST-009, NFR-AUTH.1 | Load-test evidence shows p95 < 200ms under normal load and report is archived for signoff | S | P0 |
| 18 | SC-21 | Verify availability success criterion | Release validation / ops | TEST-010, NFR-AUTH.2 | Monitoring evidence and alert routing demonstrate operational readiness for 99.9% uptime target | S | P1 |
| 19 | SC-22 | Verify bcrypt security criterion | Release validation / crypto | TEST-011, NFR-AUTH.3 | Unit and benchmark evidence confirm cost factor 12 and acceptable timing envelope | S | P0 |
| 20 | MIG-003 | Execute rollback rehearsal | Deployment / rollback validation | MIG-002, AC-8, AC-9, COMP-007 | Staging rehearsal proves feature flag disablement plus down migration restore pre-auth state without orphaned data structures or broken routing | M | P0 |

### Integration points for Phase 4

1. **Named Artifact**: Test Matrix / Validation Registry  
   - **Wired Components**: TEST-001 through TEST-011, SC-1, SC-11, SC-20, SC-21, SC-22  
   - **Owning Phase**: Phase 4  
   - **Cross-Reference**: Consumed by Phase 5 go/no-go decision

2. **Named Artifact**: Performance Harness (k6 or equivalent)  
   - **Wired Components**: API-002 login, API-003 refresh, NFR-AUTH.1 validation  
   - **Owning Phase**: Phase 4  
   - **Cross-Reference**: Consumed by production capacity planning and future regression checks

3. **Named Artifact**: Rollback Mechanism  
   - **Wired Components**: Feature flag `AUTH_SERVICE_ENABLED`, MIG-002 down migration, MIG-003 rollback rehearsal  
   - **Owning Phase**: Phase 4  
   - **Cross-Reference**: Consumed by Phase 5 deployment readiness and incident response

---

## Phase 5 — Operationalization, deferred-gap disposition, and controlled launch

### Milestones
1. Release governance completed with documented risk acceptance or mitigation.
2. Deployment, monitoring, and ownership handoff finalized.
3. Remaining open questions and deferred gaps assigned into post-v1 roadmap.

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | OPS-003 | Produce deployment runbook | Operations / release management | COMP-006, MIG-003, AC-8 | Runbook covers migration order, feature-flag enablement, secrets prerequisites, health checks, rollback steps, and owner handoffs | M | P0 |
| 2 | OPS-004 | Produce key rotation runbook | Operations / security | AC-7, RISK-1 | Runbook defines 90-day rotation steps, verification window, rollback path, and operational ownership | S | P1 |
| 3 | OPS-005 | Configure alerting and dashboards | Operations / observability | OPS-002, NFR-AUTH.1, NFR-AUTH.2 | Alerts and dashboards exist for auth latency, health-check failures, and error-rate anomalies; escalation path documented | M | P1 |
| 4 | OQ-5 | Resolve audit logging requirements | Compliance / observability | OPS-005 | Decision recorded on login, refresh, reset, and lockout event logging scope, format, and destination; if deferred, follow-on version tagged explicitly | S | P1 |
| 5 | GAP-2 | Address audit logging gap | Product/security backlog | OQ-5 | Gap disposition recorded with either implementation commitment for v1.1 or approved deferral/risk acceptance from stakeholders | S | P2 |
| 6 | OQ-6 | Resolve token revocation on user deletion | Auth lifecycle policy | COMP-003, COMP-008 | Policy recorded for token behavior when user is deleted; race condition and 15-minute access-token window explicitly addressed | S | P1 |
| 7 | GAP-3 | Address user-deletion revocation gap | Product/security backlog | OQ-6 | Gap disposition documented with implementation follow-up or explicit deferral to v1.1 and accepted residual risk | S | P2 |
| 8 | RISK-3 | Establish future password-hash review policy | Security governance | NFR-AUTH.3, OPS-004 | Annual review cadence defined for bcrypt cost factor suitability and Argon2id migration trigger points; ownership assigned | S | P2 |
| 9 | AC-9 | Enforce rollback-capable database migration policy | Release governance | MIG-003, OPS-003 | Release checklist requires tested down migrations for auth-related schema changes before promotion | S | P0 |
| 10 | SC-2 | Verify invalid-credential non-leakage criterion | Release validation / security | TEST-002, COMP-015 | Error messaging for invalid login remains generic and does not disclose whether email or password was incorrect | S | P0 |
| 11 | SC-4 | Verify login rate-limiting criterion | Release validation / abuse protection | TEST-008 | 429 response on 6th attempt within 60 seconds demonstrated in evidence pack | S | P0 |
| 12 | SC-12 | Verify refresh-hash persistence criterion | Release validation / token storage | TEST-003, DM-002 | RefreshToken storage contains SHA-256 hash only and not raw refresh token values | S | P0 |
| 13 | SC-16 | Verify reset-token issuance criterion | Release validation / password reset | TEST-005 | Registered email flow creates 1-hour reset token and dispatches email integration call as defined | S | P1 |
| 14 | SC-19 | Verify session invalidation on password reset | Release validation / password reset security | TEST-005, FR-AUTH.5 | Successful password reset revokes all outstanding refresh tokens for user across active sessions | S | P1 |
| 15 | OQ-1A | Record final decision and owner for reset email delivery implementation | Architecture decision tracking | OQ-1, OPS-003 | Chosen delivery mode is reflected in deployment and resiliency plan with named owner for ongoing operations | S | P2 |
| 16 | OQ-2A | Record final decision and owner for multi-device token policy | Product/security policy | OQ-2 | Active token cap policy and user experience tradeoff are approved and communicated to downstream consumers | S | P2 |
| 17 | COMP-017 | Publish auth module ownership map | Team/process | COMP-001, COMP-002, COMP-003, COMP-004, COMP-005, COMP-006, COMP-007 | Ownership matrix identifies maintainers for crypto, token lifecycle, routes, middleware, migrations, and operations artifacts | S | P1 |
| 18 | OPS-006 | Execute staged rollout and verification | Deployment / launch | OPS-003, OPS-005, AC-10 | Phase-1 opt-in launch completed, smoke checks pass, then protected endpoint enforcement proceeds per plan with rollback path retained | M | P0 |
| 19 | SC-5 | Verify registration success criterion | Release validation / registration | TEST-001 | HTTP 201 and database record creation evidenced for valid registration path | S | P1 |
| 20 | SC-9 | Verify token rotation success criterion | Release validation / refresh flow | TEST-003 | New token pair issued and prior refresh token invalidated for valid refresh requests | S | P1 |

### Integration points for Phase 5

1. **Named Artifact**: Release Readiness Checklist  
   - **Wired Components**: OPS-003, OPS-006, AC-9, SC-* evidence tasks, rollback rehearsal results  
   - **Owning Phase**: Phase 5  
   - **Cross-Reference**: Consumes outputs from Phases 1–4 to authorize launch

2. **Named Artifact**: Operations Dashboard and Alert Routing  
   - **Wired Components**: OPS-005, NFR-AUTH.1, NFR-AUTH.2, health-check strategy  
   - **Owning Phase**: Phase 5  
   - **Cross-Reference**: Consumed by on-call and uptime governance after launch

3. **Named Artifact**: Risk / Gap Decision Register  
   - **Wired Components**: OQ-5, OQ-6, GAP-2, GAP-3, RISK-3  
   - **Owning Phase**: Phase 5  
   - **Cross-Reference**: Feeds v1.1 planning and security review backlog

# 3. Risk assessment and mitigation strategies

## High-priority architectural risks

1. **RISK-1 — JWT signing key compromise**
   - **Why it matters**: A compromised signing key can enable forged tokens and total auth bypass.
   - **Mitigation strategy**:
     - Enforce RS256 only (AC-1).
     - Store private key exclusively in secrets manager (AC-6).
     - Rotate keys every 90 days (AC-7).
     - Maintain incident runbook for emergency key replacement and token invalidation.
   - **Release gate**:
     - No plaintext private key in code/config.
     - Rotation rehearsal documented before production.

2. **RISK-2 — Refresh token replay after theft**
   - **Why it matters**: Replay defeats silent-session continuity and can preserve attacker access.
   - **Mitigation strategy**:
     - Persist only refresh token hashes.
     - Rotate on every refresh.
     - Track replacement lineage.
     - Revoke all active tokens for user on suspicious reuse.
   - **Release gate**:
     - Integration evidence for replay-triggered global revocation.

3. **RISK-3 — bcrypt cost factor becomes insufficient over time**
   - **Why it matters**: Today’s secure setting can become tomorrow’s weak baseline.
   - **Mitigation strategy**:
     - Start at cost factor 12.
     - Benchmark and monitor login latency impact.
     - Add annual security review.
     - Define migration trigger to Argon2id if bcrypt is no longer acceptable.
   - **Release gate**:
     - Cost factor tested and governance owner assigned.

## Gap-derived risks

1. **GAP-1 — No progressive account lockout**
   - Near-term mitigation: IP-based rate limiting.
   - Recommended architect action: resolve whether account-centric lockout belongs in v1.0 or is explicitly deferred with security approval.

2. **GAP-2 — Audit logging unspecified**
   - Near-term mitigation: define minimum event taxonomy before wider rollout.
   - Recommended architect action: treat as v1.1 minimum if compliance is not in current scope, but do not leave ownership ambiguous.

3. **GAP-3 — User-deletion revocation unspecified**
   - Near-term mitigation: document residual exposure from access-token TTL window.
   - Recommended architect action: add lifecycle rule in next increment if user deletion is common or regulated.

# 4. Resource requirements and dependencies

## Team roles required

1. **Backend engineer**
   - AuthService, TokenManager, middleware, route integration
2. **Security engineer / architect**
   - RS256 key strategy, replay mitigation, hash-policy review, threat review
3. **Database engineer**
   - Schema design, migration correctness, engine-specific compatibility
4. **QA / test engineer**
   - Integration, load, rollback, and security-path verification
5. **DevOps / platform engineer**
   - Secrets manager integration, monitoring, alerting, rollout/rollback runbooks

## External dependencies

1. **DEP-1 — `jsonwebtoken`**
   - Required for RS256 signing/verification.
   - Must support key rotation-compatible usage.

2. **DEP-2 — `bcrypt`**
   - Required for secure password hashing.
   - Must support configurable cost factor and stable benchmarking.

3. **DEP-3 — Email service**
   - Required for password reset dispatch.
   - Delivery mode decision needed: synchronous vs queued.

4. **DEP-4 — Relational database**
   - Required for users, refresh_tokens, password_reset_tokens persistence.
   - Engine decision affects migration syntax and indexing strategy.

5. **DEP-5 — Secrets manager**
   - Required for RSA private-key storage and secure retrieval.
   - Must be operational before JwtService can be productionized.

## Architectural dependency chain

1. Schema and secrets first
2. Crypto components second
3. TokenManager and repositories third
4. AuthService fourth
5. Middleware/routes fifth
6. Performance/security validation sixth
7. Rollout and governance last

# 5. Success criteria and validation approach

## Validation strategy

1. **Unit validation**
   - PasswordHasher correctness
   - JwtService RS256 behavior
   - Token rotation/replay logic
   - Validation and error mapping
   - Password reset token lifecycle

2. **Integration validation**
   - `/auth/register`
   - `/auth/login`
   - `/auth/refresh`
   - `/auth/profile`
   - `/auth/password-reset/*`
   - middleware enforcement
   - migration up/down
   - rate limiting

3. **Non-functional validation**
   - p95 auth latency under load
   - uptime monitoring and alertability
   - bcrypt timing benchmark

4. **Operational validation**
   - feature flag enable/disable
   - rollback rehearsal
   - secrets retrieval path
   - key rotation process

## Critical release criteria to treat as hard gates

1. SC-1 login success
2. SC-2 no credential leakage on failure
3. SC-4 rate-limit enforcement
4. SC-11 replay-detection revocation
5. SC-12 hashed refresh-token persistence
6. SC-20 p95 latency target
7. SC-22 bcrypt cost-factor verification

## Recommended evidence pack

- API contract definitions
- unit/integration test results
- load-test report
- migration rollback rehearsal report
- secrets/key rotation checklist
- release readiness checklist with risk dispositions

# 6. Timeline estimates per phase

## Phase 1 — Foundations, security baselines, and schema readiness
- **Estimated duration**: 1.0–1.5 engineering weeks
- **Primary outputs**:
  - schemas
  - migrations
  - crypto foundations
  - repository abstractions
  - secrets contract
- **Critical path**:
  - DEP-4, DEP-5, DM-001/002/003, MIG-001/002, COMP-001/002

## Phase 2 — Token lifecycle and authentication orchestration
- **Estimated duration**: 1.5–2.0 engineering weeks
- **Primary outputs**:
  - TokenManager
  - AuthService
  - auth API contracts
  - refresh rotation and reset flow
- **Critical path**:
  - COMP-003, COMP-004, FR-AUTH.1, FR-AUTH.2, FR-AUTH.3

## Phase 3 — Request-path integration and rollout controls
- **Estimated duration**: 1.0–1.5 engineering weeks
- **Primary outputs**:
  - middleware
  - route registration
  - rate limiter
  - feature-flag gating
  - key handling operationalization
- **Critical path**:
  - COMP-005, COMP-006, COMP-012, AC-8, AC-10

## Phase 4 — Validation and hardening
- **Estimated duration**: 1.0–1.5 engineering weeks
- **Primary outputs**:
  - unit/integration/performance test suites
  - rollback rehearsal
  - non-functional evidence
- **Critical path**:
  - TEST-003, TEST-009, TEST-011, NFR-AUTH.1, MIG-003

## Phase 5 — Operationalization and controlled launch
- **Estimated duration**: 0.5–1.0 engineering weeks
- **Primary outputs**:
  - runbooks
  - alerting
  - staged rollout
  - gap dispositions
  - ownership map
- **Critical path**:
  - OPS-003, OPS-005, OPS-006, AC-9

## Overall architect recommendation

- **Total estimated delivery window**: 5.0–7.5 engineering weeks for a production-ready v1.0
- **Shortest safe path**:
  1. complete Phases 1–3
  2. do not skip Phase 4 replay/performance/rollback validation
  3. launch through Phase 5 staged enablement, not big-bang activation

If you want, I can also convert this roadmap into a machine-checkable markdown artifact aligned to your repo’s `roadmap` template conventions.
