# Phase 1 -- Core Authentication — Internal Alpha

Deliver registration, login, logout, and token infrastructure to staging. Implement all backend components (AuthService, PasswordHasher, TokenManager, JwtService, UserRepo) and frontend pages (LoginPage, RegisterPage, AuthProvider, ProfilePage). Conduct security checkpoint review. Gate production exposure behind feature flags AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH. PRD personas Alex (core flows) and Sam (token contract) are the primary users for this phase.

### T01.01 -- Provision PostgreSQL with UserProfile Schema and GDPR Fields

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | Database is the foundation for all user data persistence. GDPR consent fields (GAP-004) and 12-month audit retention (GAP-001) must be configured from Day 1. |
| Effort | L |
| Risk | High |
| Risk Drivers | database, schema, migration, compliance, gdpr |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0001, D-0002 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0001/spec.md`
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0002/spec.md`

**Deliverables:**
1. PostgreSQL 15+ instance with `UserProfile` table (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles, consent_given, consent_timestamp, password_hash)
2. Audit log table with 12-month retention policy configured per NFR-COMP-002 / GAP-001

**Steps:**
1. **[PLANNING]** Review TDD §7 Data Models for `UserProfile` schema fields and PRD S17 for GDPR consent requirements
2. **[PLANNING]** Verify INFRA-DB-001 dependency is resolved and PostgreSQL 15+ is available
3. **[EXECUTION]** Create `UserProfile` table with all fields per data model including GDPR fields (consent_given boolean, consent_timestamp ISO 8601) — resolves GAP-004
4. **[EXECUTION]** Create audit log table with structured columns (user_id, event_type, timestamp, ip_address, outcome, details JSON) and 12-month retention policy — resolves GAP-001
5. **[EXECUTION]** Configure database connection pool and environment variables
6. **[VERIFICATION]** Run schema validation: all columns exist with correct types; retention policy active
7. **[COMPLETION]** Document schema in evidence directory

**Acceptance Criteria:**
- `UserProfile` table exists with all 10 required columns including `consent_given` and `consent_timestamp` per PRD persona Alex's registration journey
- Audit log table has 12-month retention policy enforced per SOC2 compliance (PRD S17, persona Jordan's audit needs)
- No plaintext passwords stored in any column
- Schema migration scripts documented and version-controlled

**Validation:**
- Manual check: `SELECT column_name FROM information_schema.columns WHERE table_name = 'user_profiles'` returns all expected columns
- Evidence: Schema DDL scripts at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0001/spec.md`

**Dependencies:** INFRA-DB-001
**Rollback:** Drop tables and restore from backup
**Notes:** Critical path — all backend components depend on this schema.

### T01.02 -- Provision Redis Cluster for Refresh Token Storage

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | Redis stores refresh tokens with TTL and powers the account lockout counter. Required by TokenManager and AuthService. |
| Effort | M |
| Risk | High |
| Risk Drivers | performance, memory |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0003/spec.md`

**Deliverables:**
1. Redis 7+ cluster with 1 GB initial allocation, HPA at 70% utilization, replication enabled

**Steps:**
1. **[PLANNING]** Review TDD §8 API Specifications for token storage requirements and TTL values
2. **[PLANNING]** Verify Redis infrastructure availability
3. **[EXECUTION]** Provision Redis 7+ cluster with replication for high availability
4. **[EXECUTION]** Configure HPA scaling trigger at 70% memory utilization
5. **[VERIFICATION]** Connection test: write/read/TTL operations succeed
6. **[COMPLETION]** Document Redis configuration in evidence

**Acceptance Criteria:**
- Redis cluster operational with replication enabled
- HPA scaling configured at 70% threshold
- TTL operations verified (set key with 7-day expiry, confirm expiry)
- Connection pooling configured for concurrent access

**Validation:**
- Manual check: `redis-cli PING` returns PONG on all nodes
- Evidence: Configuration at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0003/spec.md`

**Dependencies:** None
**Rollback:** Deprovision cluster

### T01.03 -- Configure Feature Flag Infrastructure

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | Feature flags AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH gate production traffic routing during phased rollout. |
| Effort | S |
| Risk | Low |
| Risk Drivers | deploy |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0004/spec.md`

**Deliverables:**
1. Feature flag configuration with AUTH_NEW_LOGIN (OFF) and AUTH_TOKEN_REFRESH (OFF) operational in staging

**Steps:**
1. **[PLANNING]** Review roadmap flag definitions and rollout phasing (Phase 1 OFF → Phase 2 10% → Phase 3 100%)
2. **[PLANNING]** Determine flag service (LaunchDarkly or in-house)
3. **[EXECUTION]** Configure both flags with environment-based defaults (OFF)
4. **[EXECUTION]** Implement flag-checking middleware or service integration
5. **[VERIFICATION]** Staging test: verify flags can be toggled and traffic routes correctly
6. **[COMPLETION]** Document flag configuration and toggle procedures

**Acceptance Criteria:**
- Both flags exist and default to OFF
- Flag changes do not require service restart
- Traffic routing correctly splits based on flag state
- Flag state queryable via admin API or dashboard

**Validation:**
- Manual check: Toggle AUTH_NEW_LOGIN ON/OFF in staging, verify traffic routing changes
- Evidence: Configuration documented at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0004/spec.md`

**Dependencies:** None
**Rollback:** Set flags to OFF

### T01.04 -- Generate RS256 Key Pair for JwtService

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | RS256 2048-bit RSA key pair required for JWT access token signing per NFR-SEC-002. |
| Effort | S |
| Risk | High |
| Risk Drivers | security, credentials, secrets, encryption |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0005/spec.md`

**Deliverables:**
1. RS256 2048-bit RSA key pair mounted as Kubernetes secrets with RBAC access control

**Steps:**
1. **[PLANNING]** Review SEC-POLICY-001 key management requirements
2. **[PLANNING]** Verify Kubernetes secret management is available
3. **[EXECUTION]** Generate 2048-bit RSA key pair
4. **[EXECUTION]** Mount keys as Kubernetes secrets with restricted RBAC
5. **[VERIFICATION]** Verify key size ≥ 2048 bits; verify RBAC prevents unauthorized access
6. **[COMPLETION]** Document key rotation procedure (quarterly per roadmap)

**Acceptance Criteria:**
- Key pair generated with RSA 2048-bit minimum
- Keys stored in Kubernetes secrets, not in code or environment variables
- RBAC configured: only JwtService pod can access
- Rotation procedure documented

**Validation:**
- Manual check: `openssl rsa -in private.pem -text -noout | grep "Private-Key"` shows 2048 bit
- Evidence: Key management documentation at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0005/spec.md`

**Dependencies:** SEC-POLICY-001
**Rollback:** Revoke and regenerate keys

### T01.05 -- Set Up Docker Compose for Local Development

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | Local development environment with PostgreSQL and Redis containers for developer productivity. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0006/spec.md`

**Deliverables:**
1. Docker Compose configuration with PostgreSQL 15+ and Redis 7+ containers for local development

**Steps:**
1. **[PLANNING]** Identify service versions matching production (PostgreSQL 15+, Redis 7+)
2. **[EXECUTION]** Create docker-compose.yml with both services, volume mounts, and port mappings
3. **[EXECUTION]** Add seed/migration scripts for UserProfile schema
4. **[VERIFICATION]** `docker compose up` starts both services; app connects successfully
5. **[COMPLETION]** Document setup instructions

**Acceptance Criteria:**
- `docker compose up` starts PostgreSQL and Redis containers
- Application connects to both services on default ports
- Data persists across container restarts via volumes
- README or setup guide documents usage

**Validation:**
- Manual check: `docker compose up -d && docker compose ps` shows both services running
- Evidence: docker-compose.yml at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0006/spec.md`

**Dependencies:** None
**Rollback:** `docker compose down -v`

### Checkpoint: Phase 1 / Tasks 01-05

**Purpose:** Verify infrastructure provisioning is complete before component implementation begins.
**Checkpoint Report Path:** `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/CP-P01-T01-T05.md`
**Verification:**
- PostgreSQL schema with all UserProfile columns and audit log table operational
- Redis cluster accessible with TTL operations verified
- Feature flags configured and toggleable in staging
**Exit Criteria:**
- All infrastructure dependencies resolved (INFRA-DB-001, SEC-POLICY-001)
- Local dev environment functional via Docker Compose
- No blocking issues for component implementation

### T01.06 -- Implement PasswordHasher Component

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Secure password hashing via bcrypt cost factor 12 per NFR-SEC-001. Abstract interface enables future argon2id migration. Critical for persona Alex's registration and login security. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, authentication, encryption |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0007/spec.md`

**Deliverables:**
1. `PasswordHasher` component with bcrypt cost factor 12, abstract interface, hash/verify operations, timing invariance

**Steps:**
1. **[PLANNING]** Review TDD §6 Architecture for PasswordHasher abstraction and TDD §10 Component Inventory
2. **[PLANNING]** Review bcryptjs library API for cost factor configuration
3. **[EXECUTION]** Implement PasswordHasher with pluggable strategy pattern (bcryptjs default, argon2id slot reserved)
4. **[EXECUTION]** Implement hash() and verify() methods with timing-invariant comparison
5. **[VERIFICATION]** Unit tests: hash produces bcrypt output, verify succeeds for correct password, verify fails for incorrect, timing invariance validated, cost factor 12 confirmed in hash output
6. **[COMPLETION]** Document interface contract and migration path to argon2id

**Acceptance Criteria:**
- Unit tests for hash/verify pass: `UT-001` (per TDD §15 Testing Strategy)
- bcrypt cost factor 12 confirmed in generated hash string
- Timing-invariant comparison: no measurable timing difference between valid and invalid passwords
- Abstract interface documented for future algorithm swap

**Validation:**
- Manual check: Unit test `UT-001` passes with bcrypt cost factor 12 verified in hash output
- Evidence: Test results at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0007/evidence.md`

**Dependencies:** T01.01 (PostgreSQL schema)
**Rollback:** Revert to previous implementation
**Notes:** Critical path. AuthService depends on this component.

### T01.07 -- Implement JwtService Component

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | RS256 JWT access token signing and verification per NFR-SEC-002. 15-minute TTL with 5-second clock skew tolerance. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, token, encryption |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0008/spec.md`

**Deliverables:**
1. `JwtService` with RS256 sign/verify, 2048-bit RSA, 5-second clock skew tolerance, configuration validation

**Steps:**
1. **[PLANNING]** Review TDD §8 API Specifications for token format and TDD §10 Component Inventory for JwtService contract
2. **[PLANNING]** Verify RS256 key pair is available (T01.04)
3. **[EXECUTION]** Implement sign() method producing RS256 JWT with standard claims (sub, iat, exp, iss)
4. **[EXECUTION]** Implement verify() method with 5-second clock skew tolerance
5. **[VERIFICATION]** Unit tests: sign produces valid JWT, verify accepts valid token, verify rejects expired token, verify rejects tampered token, clock skew within 5s accepted
6. **[COMPLETION]** Document token format and claims

**Acceptance Criteria:**
- JWT header shows `alg: "RS256"` per NFR-SEC-002
- Key size verified ≥ 2048 bits
- Clock skew tolerance of 5 seconds implemented and tested
- Configuration validation test passes

**Validation:**
- Manual check: JWT decode shows RS256 algorithm and correct claims structure
- Evidence: Test results at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0008/evidence.md`

**Dependencies:** T01.04 (RS256 key pair)
**Rollback:** Revert to previous implementation

### T01.08 -- Implement TokenManager Component

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | Token lifecycle management: access token issuance (15-min TTL) + refresh token storage (7-day TTL in Redis). Refresh tokens hashed before storage. Supports revocation. Required for persona Alex's session persistence (PRD JTBD-2). |
| Effort | L |
| Risk | High |
| Risk Drivers | security, token, session |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0009/spec.md`

**Deliverables:**
1. `TokenManager` with access token issuance (15-min via JwtService), refresh token storage (7-day Redis TTL, hashed), revocation support, max 10 refresh tokens per user (OQ-PRD-002)

**Steps:**
1. **[PLANNING]** Review TDD §8 for token specifications and PRD S14 for FR-AUTH-003 requirements
2. **[PLANNING]** Verify Redis (T01.02) and JwtService (T01.07) dependencies
3. **[EXECUTION]** Implement token issuance: access token via JwtService.sign() (15-min TTL), refresh token via Redis (7-day TTL, hashed before storage)
4. **[EXECUTION]** Implement revocation: delete refresh token from Redis on logout/refresh
5. **[EXECUTION]** Implement max 10 refresh tokens per user with oldest-revoked-on-overflow (OQ-PRD-002 resolution)
6. **[VERIFICATION]** Integration tests: token issuance, refresh rotation, revocation, TTL expiry, max token limit
7. **[COMPLETION]** Document token lifecycle and storage model

**Acceptance Criteria:**
- Access tokens: RS256 JWT with 15-minute TTL, signed by JwtService
- Refresh tokens: stored hashed in Redis with 7-day TTL
- Revocation: refresh token deleted from Redis on explicit revocation
- Max 10 refresh tokens per user enforced (oldest revoked on overflow)

**Validation:**
- Manual check: Integration test `IT-001` passes (per TDD §15) — token issuance and refresh rotation verified
- Evidence: Test results at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0009/evidence.md`

**Dependencies:** T01.02 (Redis), T01.07 (JwtService)
**Rollback:** Revert to previous implementation

### T01.09 -- Implement UserRepo Component

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | CRUD operations against PostgreSQL for UserProfile. Email uniqueness enforcement with lowercase normalization. Required for persona Alex's account creation (PRD FR-AUTH.2). |
| Effort | M |
| Risk | Medium |
| Risk Drivers | database, query |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0010/spec.md`

**Deliverables:**
1. `UserRepo` with CRUD operations, email uniqueness enforcement, lowercase normalization, connection pool management

**Steps:**
1. **[PLANNING]** Review TDD §7 Data Models for UserProfile schema and TDD §10 for UserRepo contract
2. **[PLANNING]** Verify PostgreSQL schema (T01.01) is available
3. **[EXECUTION]** Implement create, read, update operations against UserProfile table
4. **[EXECUTION]** Implement email uniqueness with lowercase normalization (case-insensitive)
5. **[VERIFICATION]** Unit tests: create user, read by id/email, duplicate email rejected, email normalized to lowercase
6. **[COMPLETION]** Document query patterns and connection pool configuration

**Acceptance Criteria:**
- CRUD operations functional against PostgreSQL UserProfile table
- Duplicate email registration returns 409 (case-insensitive check)
- Email stored as lowercase regardless of input case
- Connection pool configured per environment

**Validation:**
- Manual check: Create user with mixed-case email, verify stored as lowercase, attempt duplicate returns error
- Evidence: Test results at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0010/evidence.md`

**Dependencies:** T01.01 (PostgreSQL schema)
**Rollback:** Revert to previous implementation

### T01.10 -- Implement AuthService Facade

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | Central orchestrator for all auth flows. Delegates to PasswordHasher, TokenManager, UserRepo via constructor DI. Required for all persona journeys (Alex login/register, Sam token management). |
| Effort | L |
| Risk | High |
| Risk Drivers | authentication, security, system-wide |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0011/spec.md`

**Deliverables:**
1. `AuthService` facade orchestrating login, registration, logout flows via PasswordHasher, TokenManager, UserRepo (constructor DI)

**Steps:**
1. **[PLANNING]** Review TDD §6 Architecture for AuthService facade pattern and dependency injection configuration
2. **[PLANNING]** Verify all dependencies available: PasswordHasher (T01.06), TokenManager (T01.08), UserRepo (T01.09)
3. **[EXECUTION]** Implement AuthService with constructor injection of PasswordHasher, TokenManager, UserRepo
4. **[EXECUTION]** Implement login flow: validate credentials via PasswordHasher.verify(), issue tokens via TokenManager
5. **[EXECUTION]** Implement registration flow: hash password, create user via UserRepo, issue tokens
6. **[VERIFICATION]** Integration test: login with valid/invalid credentials, registration with valid/duplicate data
7. **[COMPLETION]** Document facade dispatch table and wiring configuration

**Acceptance Criteria:**
- AuthService accepts injected PasswordHasher, TokenManager, UserRepo via constructor
- Login: valid credentials → AuthToken returned; invalid → 401 with no user enumeration
- Registration: valid data → UserProfile + AuthToken; duplicate email → 409
- All auth events trigger audit log callback (T01.17)

**Validation:**
- Manual check: Integration test — register user, then login with same credentials, verify token returned
- Evidence: Test results at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0011/evidence.md`

**Dependencies:** T01.06 (PasswordHasher), T01.08 (TokenManager), T01.09 (UserRepo)
**Rollback:** Revert to previous implementation
**Notes:** Critical path. All API endpoints depend on AuthService.

### Checkpoint: Phase 1 / Tasks 06-10

**Purpose:** Verify all core backend components are implemented and pass unit/integration tests before API endpoint and frontend work.
**Checkpoint Report Path:** `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/CP-P01-T06-T10.md`
**Verification:**
- PasswordHasher, JwtService, TokenManager, UserRepo, AuthService all pass unit tests
- AuthService facade correctly delegates to all injected dependencies
- Integration test: register → login → token issuance passes
**Exit Criteria:**
- All 5 backend components operational with passing tests
- AuthService dependency injection wiring verified
- No P0 bugs in component implementations

### T01.11 -- Implement Logout in AuthService

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | POST /auth/logout revokes refresh token in Redis and clears HttpOnly cookie. Resolves GAP-002 (logout endpoint missing from TDD). |
| Effort | S |
| Risk | Medium |
| Risk Drivers | authentication, session |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0012/spec.md`

**Deliverables:**
1. Logout implementation in AuthService: revoke refresh token in Redis, clear HttpOnly cookie, return 200

**Steps:**
1. **[PLANNING]** Review GAP-002 resolution and PRD AUTH-E1 scope (logout included)
2. **[EXECUTION]** Implement logout method: delete refresh token from Redis via TokenManager
3. **[EXECUTION]** Clear HttpOnly refreshToken cookie in response
4. **[VERIFICATION]** Test: after logout, refresh token is no longer in Redis; cookie cleared
5. **[COMPLETION]** Document logout flow

**Acceptance Criteria:**
- Refresh token deleted from Redis on logout
- HttpOnly cookie cleared in response headers
- Subsequent token refresh attempts return 401
- Audit log entry created for logout event

**Validation:**
- Manual check: Login → get refresh token → logout → attempt refresh → 401
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0012/evidence.md`

**Dependencies:** T01.10 (AuthService), T01.08 (TokenManager)
**Rollback:** Revert logout method

### T01.12 -- Implement POST /auth/login Endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | Core login endpoint per FR-AUTH-001. Returns AuthToken on success, 401 on failure with no user enumeration. Account lockout after 5 failures. Serves persona Alex's primary JTBD (quick login). |
| Effort | M |
| Risk | High |
| Risk Drivers | authentication, security |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0013/spec.md`

**Deliverables:**
1. POST /auth/login endpoint: valid creds → 200 + AuthToken; invalid → 401 (no enumeration); lockout → 423; rate limit 10 req/min/IP

**Steps:**
1. **[PLANNING]** Review TDD §8 API Specifications for /auth/login contract and PRD FR-AUTH.1
2. **[EXECUTION]** Implement endpoint handler calling AuthService.login()
3. **[EXECUTION]** Implement account lockout: Redis counter, 5 failures in 15 min → 423 Locked
4. **[EXECUTION]** Configure rate limiting: 10 req/min per IP
5. **[VERIFICATION]** API tests: valid login → 200, invalid → 401, lockout after 5 → 423, rate limit → 429
6. **[COMPLETION]** Document endpoint contract

**Acceptance Criteria:**
- FR-AUTH-001 AC #1-4 pass: login, invalid creds, no enumeration, lockout
- Rate limiting enforced: 10 req/min per IP → 429
- No user enumeration: same error response for wrong email vs wrong password
- Audit log entry for login success and failure events

**Validation:**
- Manual check: Test all 4 scenarios (valid, invalid, no-enum, lockout) against staging endpoint
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0013/evidence.md`

**Dependencies:** T01.10 (AuthService)
**Rollback:** Disable endpoint

### T01.13 -- Implement POST /auth/register Endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | Registration endpoint per FR-AUTH-002. Creates account with GDPR consent capture (GAP-004). Serves persona Alex's first journey (Signup). Registration conversion target >60% (PRD S19). |
| Effort | M |
| Risk | High |
| Risk Drivers | authentication, security, compliance, gdpr |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0014/spec.md`

**Deliverables:**
1. POST /auth/register endpoint: valid → 201 + UserProfile; duplicate email → 409; weak password → 400; GDPR consent required in body

**Steps:**
1. **[PLANNING]** Review TDD §8 for /auth/register contract and PRD S12 (registration in scope) and PRD S22 (Signup journey)
2. **[EXECUTION]** Implement endpoint handler calling AuthService.register()
3. **[EXECUTION]** Validate GDPR consent field in request body (mandatory per GAP-004)
4. **[EXECUTION]** Configure rate limiting: 5 req/min per IP
5. **[VERIFICATION]** API tests: valid → 201, duplicate → 409, weak password → 400, missing consent → 400
6. **[COMPLETION]** Document endpoint contract including consent requirements

**Acceptance Criteria:**
- FR-AUTH-002 AC #1-4 pass per TDD: registration, duplicate email, weak password, bcrypt storage
- GDPR consent_given and consent_timestamp stored on registration (NFR-COMP-001, persona Alex's journey)
- Rate limiting: 5 req/min per IP → 429
- Audit log entry for registration event

**Validation:**
- Manual check: Register with and without consent field, verify consent stored in database
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0014/evidence.md`

**Dependencies:** T01.10 (AuthService), T01.01 (GDPR schema)
**Rollback:** Disable endpoint

### T01.14 -- Implement POST /auth/refresh Endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | Token refresh per FR-AUTH-003. Valid refresh token → new AuthToken pair, old revoked. Gated behind AUTH_TOKEN_REFRESH flag. Serves persona Sam's programmatic token management and Alex's session persistence (JTBD-2). |
| Effort | M |
| Risk | High |
| Risk Drivers | security, token, session |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0015/spec.md`

**Deliverables:**
1. POST /auth/refresh endpoint: valid → 200 + new AuthToken pair, old refresh revoked; expired → 401; rate limit 30 req/min/user; gated behind AUTH_TOKEN_REFRESH

**Steps:**
1. **[PLANNING]** Review TDD §8 for /auth/refresh contract and feature flag gating strategy
2. **[EXECUTION]** Implement endpoint calling TokenManager.refresh()
3. **[EXECUTION]** Gate behind AUTH_TOKEN_REFRESH flag (returns 404 when OFF)
4. **[VERIFICATION]** Tests: valid refresh → new pair, expired → 401, flag OFF → 404, old token revoked after refresh
5. **[COMPLETION]** Document token rotation behavior

**Acceptance Criteria:**
- Valid refresh → 200 with new access + refresh tokens; old refresh token revoked
- Expired refresh → 401
- AUTH_TOKEN_REFRESH=OFF → 404
- Rate limit: 30 req/min per user → 429

**Validation:**
- Manual check: Full refresh cycle: login → get tokens → refresh → verify new tokens → verify old refresh revoked
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0015/evidence.md`

**Dependencies:** T01.08 (TokenManager), T01.03 (Feature flags)
**Rollback:** Disable endpoint

### T01.15 -- Implement GET /auth/me Endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | Profile retrieval per FR-AUTH-004. Returns UserProfile for authenticated users. Serves persona Alex's profile management journey (PRD S22). |
| Effort | S |
| Risk | Low |
| Risk Drivers | authentication |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0016/spec.md`

**Deliverables:**
1. GET /auth/me endpoint: valid bearer → 200 + UserProfile; invalid/expired → 401; rate limit 60 req/min/user

**Steps:**
1. **[PLANNING]** Review TDD §8 for /auth/me contract
2. **[EXECUTION]** Implement endpoint: extract user ID from JWT, fetch profile via UserRepo
3. **[EXECUTION]** Configure rate limiting: 60 req/min per user
4. **[VERIFICATION]** API tests: valid token → 200 + profile, expired → 401, no token → 401
5. **[COMPLETION]** Document endpoint

**Acceptance Criteria:**
- Authenticated request → 200 with full UserProfile (minus password hash)
- Unauthenticated → 401
- Rate limit: 60 req/min per user
- Response matches UserProfile schema from TDD §7

**Validation:**
- Manual check: Login, use access token on GET /auth/me, verify profile returned
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0016/evidence.md`

**Dependencies:** T01.10 (AuthService), T01.09 (UserRepo)
**Rollback:** Disable endpoint

### Checkpoint: Phase 1 / Tasks 11-15

**Purpose:** Verify all core API endpoints are functional before frontend and cross-cutting work.
**Checkpoint Report Path:** `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/CP-P01-T11-T15.md`
**Verification:**
- All 5 API endpoints respond correctly (login, register, refresh, me, logout)
- Account lockout triggers after 5 failures
- Rate limiting enforced on all endpoints
**Exit Criteria:**
- API test suite passes for all endpoints
- GDPR consent captured on registration
- Token refresh and revocation cycle verified

### T01.16 -- Implement POST /auth/logout Endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | Logout endpoint per GAP-002. Revokes refresh token and clears cookie. Separate from T01.11 (AuthService logic) — this is the HTTP endpoint handler. |
| Effort | S |
| Risk | Low |
| Risk Drivers | authentication |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0017/spec.md`

**Deliverables:**
1. POST /auth/logout endpoint handler: calls AuthService.logout(), returns 200, rate limit 60 req/min/user

**Steps:**
1. **[PLANNING]** Review roadmap 1.3 for logout endpoint specification
2. **[EXECUTION]** Implement endpoint handler delegating to AuthService.logout() (T01.11)
3. **[EXECUTION]** Configure rate limiting: 60 req/min per user
4. **[VERIFICATION]** API test: logout returns 200, subsequent refresh fails
5. **[COMPLETION]** Document endpoint

**Acceptance Criteria:**
- POST /auth/logout returns 200
- Refresh token revoked after logout
- HttpOnly cookie cleared
- Rate limit enforced

**Validation:**
- Manual check: Login → logout → attempt refresh → 401
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0017/evidence.md`

**Dependencies:** T01.11 (AuthService logout logic)
**Rollback:** Disable endpoint

### T01.17 -- Implement Audit Logging Foundation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-017 |
| Why | Structured audit logging for all auth events per NFR-COMP-002. 12-month retention (GAP-001 resolution). Required for persona Jordan's audit investigation needs and SOC2 compliance. |
| Effort | M |
| Risk | High |
| Risk Drivers | compliance, audit |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0018 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0018/spec.md`

**Deliverables:**
1. Audit log writer: structured events (user_id, event_type, timestamp, ip_address, outcome, details JSON) with 12-month retention
2. OpenTelemetry span wiring: AuthService → PasswordHasher → TokenManager → JwtService

**Steps:**
1. **[PLANNING]** Review TDD §25 Operational Readiness and PRD S17 (Legal & Compliance) for audit requirements
2. **[EXECUTION]** Implement structured audit log writer with all required fields
3. **[EXECUTION]** Wire synchronous post-operation callbacks in AuthService for all auth events (login, register, refresh, logout, lockout)
4. **[EXECUTION]** Configure OpenTelemetry spans across auth flow components
5. **[VERIFICATION]** Integration test: perform login, verify audit log entry exists with correct fields; verify 12-month retention policy active
6. **[COMPLETION]** Document audit schema and callback chain

**Acceptance Criteria:**
- All auth events logged: login success/failure, registration, token refresh, logout, lockout
- Log entries contain: user_id, event_type, timestamp, ip_address, outcome, details
- 12-month retention policy active per SOC2 requirements (NFR-COMP-002)
- OpenTelemetry traces span AuthService → PasswordHasher → TokenManager → JwtService

**Validation:**
- Manual check: Perform login, query audit table for entry with correct fields
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0018/evidence.md`

**Dependencies:** T01.01 (audit log table), T01.10 (AuthService)
**Rollback:** Remove callbacks; retain log table

### T01.18 -- Implement LoginPage Frontend Component

| Field | Value |
|---|---|
| Roadmap Item IDs | R-018 |
| Why | Login form UI per TDD §10 Component Inventory. Calls POST /auth/login. Inline validation. Generic error on failure (no enumeration). CAPTCHA after 3 failures (R-002 mitigation). Serves persona Alex's Login journey (PRD S22). |
| Effort | M |
| Risk | Medium |
| Risk Drivers | authentication |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0019/spec.md`

**Deliverables:**
1. `LoginPage` component: email/password form, inline validation, generic error on failure, CAPTCHA after 3 failures

**Steps:**
1. **[PLANNING]** Review TDD §10 for LoginPage component spec and PRD S16 for login UX flow
2. **[EXECUTION]** Implement login form with email and password fields
3. **[EXECUTION]** Integrate with POST /auth/login API; handle success (redirect) and error (generic message)
4. **[EXECUTION]** Add CAPTCHA widget triggered after 3 failed attempts
5. **[VERIFICATION]** Component test: form renders, submission works, error displayed, CAPTCHA appears after failures
6. **[COMPLETION]** Document component props and error handling

**Acceptance Criteria:**
- Login form submits to POST /auth/login
- Invalid credentials show generic error (no user enumeration per security requirements)
- CAPTCHA appears after 3 consecutive failures (R-002 mitigation)
- Successful login redirects to dashboard/profile

**Validation:**
- Manual check: Attempt login with invalid creds 3 times, verify CAPTCHA appears on 4th
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0019/evidence.md`

**Dependencies:** T01.12 (login endpoint)
**Rollback:** Revert component

### T01.19 -- Implement RegisterPage Frontend Component

| Field | Value |
|---|---|
| Roadmap Item IDs | R-019 |
| Why | Registration form UI with GDPR consent checkbox per GAP-004. Client-side password validation. Serves persona Alex's Signup journey (PRD S22, 5 steps). Registration conversion target >60% (PRD S19). |
| Effort | M |
| Risk | Medium |
| Risk Drivers | authentication, compliance, gdpr |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0020/spec.md`

**Deliverables:**
1. `RegisterPage` component: email/password/displayName form, client-side password policy validation, GDPR consent checkbox (mandatory)

**Steps:**
1. **[PLANNING]** Review TDD §10 for RegisterPage spec and PRD S22 for Signup journey steps
2. **[EXECUTION]** Implement form with email, password, displayName, GDPR consent checkbox
3. **[EXECUTION]** Add client-side password policy validation (strength indicator)
4. **[EXECUTION]** Integrate with POST /auth/register; consent field included in request body
5. **[VERIFICATION]** Component test: form validates, consent required, submission succeeds
6. **[COMPLETION]** Document component

**Acceptance Criteria:**
- Registration form includes GDPR consent checkbox (mandatory, cannot submit without)
- Client-side password validation provides feedback before submission
- Successful registration creates account and logs user in
- Form tracks conversion funnel for >60% target measurement

**Validation:**
- Manual check: Submit form without consent checkbox → blocked; with consent → account created
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0020/evidence.md`

**Dependencies:** T01.13 (register endpoint)
**Rollback:** Revert component

### T01.20 -- Implement AuthProvider Context Component

| Field | Value |
|---|---|
| Roadmap Item IDs | R-020 |
| Why | Context provider managing AuthToken state. accessToken in memory only (R-001 mitigation). HttpOnly cookie for refreshToken. Silent refresh handler (401 interceptor). Serves persona Alex's session persistence (JTBD-2). |
| Effort | L |
| Risk | High |
| Risk Drivers | security, token, session |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0021/spec.md`

**Deliverables:**
1. `AuthProvider` context: accessToken in memory, HttpOnly refreshToken cookie, 401 interceptor with silent refresh, logout redirect

**Steps:**
1. **[PLANNING]** Review TDD §10 for AuthProvider spec and Wiring Task 1.5.1 (Silent Token Refresh Middleware Chain)
2. **[EXECUTION]** Implement context provider with token state management (access in memory, refresh in HttpOnly cookie)
3. **[EXECUTION]** Implement HTTP interceptor: detect 401 → call POST /auth/refresh → retry original request
4. **[EXECUTION]** Implement logout handler: clear tokens, redirect to login
5. **[VERIFICATION]** Component test: silent refresh on 401, logout clears state, token stored in memory only (no localStorage)
6. **[COMPLETION]** Document provider API and token lifecycle

**Acceptance Criteria:**
- accessToken stored ONLY in memory (R-001 mitigation) — no localStorage, no sessionStorage
- refreshToken stored as HttpOnly cookie only
- 401 response triggers silent refresh attempt; if refresh fails, redirect to login
- Page refresh preserves session via silent token refresh (persona Alex JTBD-2)

**Validation:**
- Manual check: Login → refresh page → verify no re-login prompt (silent refresh works). Inspect browser storage → no tokens in localStorage.
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0021/evidence.md`

**Dependencies:** T01.14 (refresh endpoint), T01.12 (login endpoint)
**Rollback:** Revert provider

### Checkpoint: Phase 1 / Tasks 16-20

**Purpose:** Verify API endpoints and frontend components are functional before gateway, monitoring, and security phases.
**Checkpoint Report Path:** `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/CP-P01-T16-T20.md`
**Verification:**
- Logout endpoint functional (GAP-002 resolved)
- Audit logging captures all auth events with correct schema
- LoginPage, RegisterPage, AuthProvider render and function correctly
**Exit Criteria:**
- All frontend components connected to API endpoints
- Silent token refresh verified (page refresh preserves session)
- GDPR consent captured at registration with consent checkbox

### T01.21 -- Implement ProfilePage Frontend Component

| Field | Value |
|---|---|
| Roadmap Item IDs | R-021 |
| Why | Displays user profile from GET /auth/me. Serves persona Alex's Profile Management journey (PRD S22). |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0022/spec.md`

**Deliverables:**
1. `ProfilePage` component displaying user profile data from GET /auth/me

**Steps:**
1. **[PLANNING]** Review TDD §10 for ProfilePage spec
2. **[EXECUTION]** Implement page fetching user profile on mount via AuthProvider context
3. **[VERIFICATION]** Component renders with user data from API
4. **[COMPLETION]** Document component

**Acceptance Criteria:**
- ProfilePage displays email, displayName, createdAt from UserProfile
- Page redirects to login if unauthenticated (via AuthProvider)
- Loading state shown while fetching
- Error handling for failed fetch

**Validation:**
- Manual check: Login → navigate to /profile → verify profile data displayed
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0022/spec.md`

**Dependencies:** T01.15 (GET /auth/me endpoint), T01.20 (AuthProvider)
**Rollback:** Revert component

### T01.22 -- Configure Route Protection

| Field | Value |
|---|---|
| Roadmap Item IDs | R-022 |
| Why | Protected routes prevent unauthenticated access to /profile. Public routes for /login and /register. |
| Effort | S |
| Risk | Low |
| Risk Drivers | authentication |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0023 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0023/spec.md`

**Deliverables:**
1. Route configuration: /login → LoginPage, /register → RegisterPage, /profile → ProfilePage (protected)

**Steps:**
1. **[PLANNING]** Review TDD §10 for route mapping
2. **[EXECUTION]** Configure router with public (/login, /register) and protected (/profile) routes
3. **[EXECUTION]** Protected routes redirect to /login if not authenticated
4. **[VERIFICATION]** Test: unauthenticated access to /profile redirects to /login
5. **[COMPLETION]** Document route map

**Acceptance Criteria:**
- /login accessible without authentication
- /register accessible without authentication
- /profile redirects to /login if not authenticated
- Authenticated users can access /profile

**Validation:**
- Manual check: Open /profile in incognito → redirected to /login; login → access /profile → profile shown
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0023/spec.md`

**Dependencies:** T01.20 (AuthProvider), T01.21 (ProfilePage)
**Rollback:** Revert route config

### T01.23 -- Configure API Gateway Rate Limiting

| Field | Value |
|---|---|
| Roadmap Item IDs | R-023 |
| Why | Per-endpoint rate limits prevent abuse. Login: 10/min/IP, register: 5/min/IP, refresh: 30/min/user, me: 60/min/user, logout: 60/min/user. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | performance |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0024 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0024/spec.md`

**Deliverables:**
1. Rate limiting configuration: per-endpoint limits enforced, 429 returned on excess

**Steps:**
1. **[PLANNING]** Review roadmap 1.6 for exact per-endpoint limits
2. **[EXECUTION]** Configure rate limiting middleware/gateway for all 5 endpoints
3. **[VERIFICATION]** Staging test: exceed limit on each endpoint, verify 429 returned
4. **[COMPLETION]** Document rate limiting configuration

**Acceptance Criteria:**
- Login: 10 req/min per IP
- Register: 5 req/min per IP
- Refresh: 30 req/min per user
- Me + Logout: 60 req/min per user
- All return 429 when limit exceeded

**Validation:**
- Manual check: Send 11 requests to /auth/login in 1 minute, verify 11th returns 429
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0024/evidence.md`

**Dependencies:** T01.12-T01.16 (all endpoints)
**Rollback:** Remove rate limiting middleware

### T01.24 -- Configure CORS

| Field | Value |
|---|---|
| Roadmap Item IDs | R-024 |
| Why | CORS configuration allows frontend origin while blocking cross-origin token access. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | security |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0025 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0025/spec.md`

**Deliverables:**
1. CORS configuration: allow frontend origin, disallow cross-origin token access

**Steps:**
1. **[PLANNING]** Identify allowed frontend origins
2. **[EXECUTION]** Configure CORS middleware with allowed origins and methods
3. **[VERIFICATION]** Staging test: CORS headers present, preflight passes from frontend origin
4. **[COMPLETION]** Document CORS configuration

**Acceptance Criteria:**
- CORS headers present on all responses
- Preflight (OPTIONS) requests succeed from allowed origins
- Cross-origin requests from disallowed origins are blocked
- Credentials mode configured for HttpOnly cookies

**Validation:**
- Manual check: Send preflight request from frontend origin → 200 with correct headers
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0025/spec.md`

**Dependencies:** None
**Rollback:** Remove CORS middleware

### T01.25 -- Implement Monitoring and Observability

| Field | Value |
|---|---|
| Roadmap Item IDs | R-025 |
| Why | Prometheus metrics, OpenTelemetry traces, structured logging, and Grafana dashboards for auth service operational visibility. Required for Phase 2 beta monitoring. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0026, D-0027 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0026/spec.md`
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0027/spec.md`

**Deliverables:**
1. Prometheus metrics: auth_login_total, auth_login_duration_seconds, auth_registration_total, auth_token_refresh_total
2. Grafana dashboards: login latency p95, error rate, concurrent requests, Redis memory usage

**Steps:**
1. **[PLANNING]** Review roadmap 1.7 for metric and dashboard specifications
2. **[EXECUTION]** Instrument AuthService endpoints with Prometheus counters and histograms
3. **[EXECUTION]** Configure Grafana dashboards with specified panels
4. **[EXECUTION]** Set up structured logging with user_id and event_type fields
5. **[VERIFICATION]** Staging: perform auth operations, verify metrics appear in Prometheus, dashboards render
6. **[COMPLETION]** Document metric names and dashboard locations

**Acceptance Criteria:**
- All 4 Prometheus metrics emit data on auth operations
- Grafana dashboards display login latency p95, error rate, concurrent requests, Redis memory
- Structured logs searchable by user_id and event_type
- OpenTelemetry traces span full auth flow

**Validation:**
- Manual check: Login → check Prometheus → auth_login_total incremented → Grafana shows data point
- Evidence: `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0026/evidence.md`

**Dependencies:** T01.12-T01.16 (endpoints to instrument)
**Rollback:** Remove instrumentation

### Checkpoint: Phase 1 / Tasks 21-25

**Purpose:** Verify frontend pages, route protection, rate limiting, CORS, and monitoring before security review.
**Checkpoint Report Path:** `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/CP-P01-T21-T25.md`
**Verification:**
- ProfilePage renders user data from API
- Route protection enforces authentication on /profile
- Rate limiting returns 429 on all endpoints when exceeded
**Exit Criteria:**
- All frontend pages functional with API integration
- Monitoring stack operational (Prometheus + Grafana + traces)
- CORS configured and verified

### T01.26 -- Execute Security Checkpoint Review

| Field | Value |
|---|---|
| Roadmap Item IDs | R-026 |
| Why | Early security checkpoint catches crypto implementation bugs when cheapest to fix. Reviews PasswordHasher, JwtService, TokenManager implementations. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, vulnerability, audit |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0028 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0028/spec.md`

**Deliverables:**
1. Security review report covering: PasswordHasher bcrypt cost 12 validation, JwtService RS256 + clock skew, TokenManager refresh storage, HttpOnly cookies, no plaintext passwords in logs/DB

**Steps:**
1. **[PLANNING]** Define review scope: all crypto components (PasswordHasher, JwtService, TokenManager)
2. **[EXECUTION]** Review bcrypt cost factor 12 timing invariance
3. **[EXECUTION]** Review HttpOnly cookie configuration for refreshToken
4. **[EXECUTION]** Review JwtService clock skew handling (5-second tolerance)
5. **[EXECUTION]** Validate no plaintext passwords in logs or database
6. **[VERIFICATION]** All review items pass or findings documented with remediation plan
7. **[COMPLETION]** Security review report filed; remediation window Days 9-10 if needed

**Acceptance Criteria:**
- All crypto implementations reviewed by security-team
- bcrypt cost factor 12 confirmed with timing invariance test
- HttpOnly cookie correctly configured (no JavaScript access to refreshToken)
- Zero plaintext password exposure in any log or database query
- Any findings have remediation plan with estimated fix time

**Validation:**
- Manual check: Security review checklist completed with all items PASS or findings documented
- Evidence: Security review report at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0028/spec.md`

**Dependencies:** T01.06 (PasswordHasher), T01.07 (JwtService), T01.08 (TokenManager), T01.20 (AuthProvider cookies)
**Rollback:** N/A (review only)

### T01.27 -- Execute Manual Testing and Bug Fix

| Field | Value |
|---|---|
| Roadmap Item IDs | R-027 |
| Why | End-to-end manual testing of all auth flows before Phase 1 exit. 13 test scenarios covering all persona journeys. Bug fix window included. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | end-to-end |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0029 |

**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0029/spec.md`

**Deliverables:**
1. Manual test report covering all 13 scenarios from roadmap 1.9 (registration valid/invalid, login valid/invalid/lockout, token refresh valid/expired, profile auth/unauth, session persistence, logout, audit logging)

**Steps:**
1. **[PLANNING]** Review roadmap 1.9 test scenario table for all 13 scenarios
2. **[EXECUTION]** Execute each scenario against staging environment
3. **[EXECUTION]** Document results: pass/fail with evidence for each scenario
4. **[EXECUTION]** Fix any bugs found (2-day remediation window per roadmap)
5. **[VERIFICATION]** Re-test fixed scenarios; E2E test: register → login → profile → refresh → logout → verify audit (per TDD E2E-001)
6. **[COMPLETION]** Test report filed with all scenarios documented

**Acceptance Criteria:**
- All 13 manual test scenarios pass (or bugs documented and fixed)
- E2E-001 test pass: full journey register → login → profile → refresh → logout
- Zero P0/P1 bugs in staging
- Unit test coverage ≥ 80% on all backend components

**Validation:**
- Manual check: Test report shows 13/13 scenarios PASS (or bugs fixed and re-tested)
- Evidence: Test report at `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0029/spec.md`

**Dependencies:** All Phase 1 tasks (T01.01-T01.26)
**Rollback:** N/A (testing only)

### Checkpoint: End of Phase 1

**Purpose:** Final Phase 1 gate. Verify all exit criteria from roadmap are met before proceeding to Phase 2 (Password Reset, Compliance, Beta).
**Checkpoint Report Path:** `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/CP-P01-END.md`
**Verification:**
- FR-AUTH-001 through FR-AUTH-004 acceptance criteria pass
- GDPR consent captured (GAP-004), logout functional (GAP-002), audit log operational (GAP-001)
- Security checkpoint complete with findings remediated
**Exit Criteria:**
- All Phase 1 exit criteria from roadmap met (17 items)
- Zero P0/P1 bugs in staging
- Feature flags AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH both OFF by default
