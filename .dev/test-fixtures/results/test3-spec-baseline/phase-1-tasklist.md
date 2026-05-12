# Phase 1 -- Foundation Layer

**Goal**: Build zero-dependency base components, database schema, and DI wiring. Everything in later phases depends on this layer.

**Tasks**: T01.01 -- T01.16
**Roadmap Items**: R-001 -- R-016
**Deliverables**: D-0001 -- D-0016

---

### T01.01 -- Create users table migration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | The users table is the foundational schema for all authentication operations; every subsequent service depends on it. |
| Effort | M |
| Risk | High |
| Risk Drivers | database, migration, schema |
| Tier | STRICT |
| Confidence | [████████--] 90% |
| Critical Path Override | Yes |
| Verification Method | Automated tests + manual review |
| Deliverable IDs | D-0001 |

**Deliverables:**
- Migration file creating `users` table with columns: id (UUID v4 PK), email (unique index), display_name, password_hash, is_locked (boolean default false), created_at, updated_at
- Down-migration file reversing the creation

**Steps:**
1. [PLANNING] Define column types and constraints per FR-AUTH.2, FR-AUTH.1-IMPL-3, FR-AUTH.1-IMPL-5
2. [EXECUTION] Write up-migration with UUID primary key, unique email index, and all specified columns
3. [EXECUTION] Write down-migration that drops the users table cleanly
4. [VERIFICATION] Run migration up, inspect schema, run migration down, confirm clean state

**Acceptance Criteria:**
- Migration creates users table with all specified columns and correct types
- Unique index exists on email column
- Down-migration drops table and index cleanly
- Migration is idempotent (running up twice does not error)

**Validation:**
- Manual check: Run `\d users` in psql after migration up to confirm schema
- Evidence: Migration files committed; CI runs up/down cycle

**Dependencies:** None

---

### T01.02 -- Create refresh_tokens table migration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | Refresh token storage enables stateful token rotation and replay detection, a core security mechanism. |
| Effort | M |
| Risk | High |
| Risk Drivers | database, migration, schema, token |
| Tier | STRICT |
| Confidence | [████████--] 90% |
| Critical Path Override | Yes |
| Verification Method | Automated tests + manual review |
| Deliverable IDs | D-0002 |

**Deliverables:**
- Migration file creating `refresh_tokens` table with columns: id (UUID v4 PK), user_id (FK to users, cascade delete), token_hash (SHA-256, unique), expires_at, revoked_at, created_at
- Indexes on user_id and expires_at
- Down-migration file

**Steps:**
1. [PLANNING] Define FK relationship to users table with cascade delete behavior
2. [EXECUTION] Write up-migration with all columns, FK constraint, and indexes
3. [EXECUTION] Write down-migration that drops table, indexes, and FK
4. [VERIFICATION] Run migration up/down cycle and verify clean state

**Acceptance Criteria:**
- Table has FK to users with ON DELETE CASCADE
- Unique index on token_hash column
- Indexes exist on user_id and expires_at
- Down-migration removes all artifacts cleanly

**Validation:**
- Manual check: Run `\d refresh_tokens` and `\di` to confirm indexes
- Evidence: Migration files committed; CI runs up/down cycle

**Dependencies:** T01.01

---

### T01.03 -- Verify all migrations are reversible

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | Reversible migrations are required by FR-AUTH.1-IMPL-5 and enable safe rollback during deployment. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | migration, database |
| Tier | STRICT |
| Confidence | [█████████-] 92% |
| Critical Path Override | Yes |
| Verification Method | Automated test suite |
| Deliverable IDs | D-0003 |

**Deliverables:**
- Automated test that runs all migrations up then down and asserts clean database state

**Steps:**
1. [PLANNING] Design test to run full migration cycle
2. [EXECUTION] Write test: migrate up all, migrate down all, assert no tables remain
3. [VERIFICATION] Run test in CI; confirm zero residual schema

**Acceptance Criteria:**
- Test runs all migrations up then all down in sequence
- Assert database has no auth-related tables after full down-migration
- Test passes in CI environment

**Validation:**
- Manual check: Run test locally and inspect database
- Evidence: Test file committed; CI green

**Dependencies:** T01.01, T01.02

---

### T01.04 -- Implement PasswordHasher class

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | Secure password hashing is the first line of defense for stored credentials; bcrypt with configurable cost is required. |
| Effort | M |
| Risk | High |
| Risk Drivers | crypto, password, security |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Critical Path Override | Yes |
| Verification Method | Automated tests + security review |
| Deliverable IDs | D-0004 |

**Deliverables:**
- `PasswordHasher` class with `hash(plaintext): Promise<string>` and `verify(plaintext, hash): Promise<boolean>` methods
- Configurable bcrypt cost factor (default 12)

**Steps:**
1. [PLANNING] Define interface per FR-AUTH.1, FR-AUTH.2, FR-AUTH.1-IMPL-1
2. [EXECUTION] Implement PasswordHasher with bcrypt library, externalized cost factor
3. [VERIFICATION] Unit test round-trip hash/verify; benchmark timing

**Acceptance Criteria:**
- hash() returns a bcrypt hash string
- verify() correctly validates matching and non-matching passwords
- Cost factor is configurable via environment variable, defaults to 12
- No plaintext passwords logged or stored

**Validation:**
- Manual check: Inspect hash output format is bcrypt ($2b$ prefix)
- Evidence: Unit test file and class implementation committed

**Dependencies:** None

---

### T01.05 -- Implement password policy validator

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | Password policy enforcement (FR-AUTH.2c) prevents weak passwords from entering the system. |
| Effort | S |
| Risk | Low |
| Risk Drivers | password, security |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Critical Path Override | Yes |
| Verification Method | Automated tests |
| Deliverable IDs | D-0005 |

**Deliverables:**
- Standalone password policy validation function enforcing: min 8 chars, 1 uppercase, 1 lowercase, 1 digit

**Steps:**
1. [PLANNING] Define validation rules per FR-AUTH.2c
2. [EXECUTION] Implement validator as pure function with descriptive error messages
3. [VERIFICATION] Unit tests with boundary values (7 chars, 8 chars, missing each class)

**Acceptance Criteria:**
- Rejects passwords shorter than 8 characters
- Rejects passwords missing uppercase, lowercase, or digit
- Accepts valid passwords meeting all criteria
- Returns descriptive error for each failing rule

**Validation:**
- Manual check: Test with edge-case passwords
- Evidence: Validator function and test file committed

**Dependencies:** None

---

> **CHECKPOINT 1** (after T01.05): Verify T01.01--T01.05 pass all acceptance criteria. Schema migrations run cleanly. PasswordHasher and policy validator have passing unit tests.

---

### T01.06 -- Configure bcrypt cost factor 12

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | NFR-AUTH.3 mandates bcrypt cost factor 12 for appropriate security/performance balance. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | crypto, security |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0006 |

**Deliverables:**
- Configuration entry for bcrypt cost factor with environment variable override

**Steps:**
1. [PLANNING] Define config key and env var name
2. [EXECUTION] Add config with default value of 12
3. [VERIFICATION] Test that config reads from env and defaults correctly

**Acceptance Criteria:**
- Default cost factor is 12
- Can be overridden via environment variable
- PasswordHasher reads from config (not hardcoded)

**Validation:**
- Manual check: Set env var, verify PasswordHasher uses it
- Evidence: Config file and test committed

**Dependencies:** T01.04

---

### T01.07 -- Unit tests for PasswordHasher and policy

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | SC-5 requires all services to be unit tested; benchmarking confirms NFR-AUTH.3 timing requirements. |
| Effort | S |
| Risk | Low |
| Risk Drivers | security |
| Tier | STRICT |
| Confidence | [█████████-] 93% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0007 |

**Deliverables:**
- Unit test suite covering: hash timing ~250ms, verify round-trip, policy validation edge cases

**Steps:**
1. [PLANNING] Identify test cases: timing benchmark, round-trip, policy boundaries
2. [EXECUTION] Write tests asserting 200-400ms hash timing, correct verify behavior, all policy rules
3. [VERIFICATION] Run tests; confirm benchmark within range on CI hardware

**Acceptance Criteria:**
- Benchmark test asserts bcrypt hash takes 200-400ms
- Round-trip test: hash then verify returns true
- Negative test: verify with wrong password returns false
- Policy tests cover all boundary conditions

**Validation:**
- Manual check: Review test output for timing values
- Evidence: Test file committed; CI green

**Dependencies:** T01.04, T01.05, T01.06

---

### T01.08 -- Implement JwtService class

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | JWT signing and verification is the core mechanism for stateless access token authentication. |
| Effort | M |
| Risk | High |
| Risk Drivers | crypto, token, security |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Critical Path Override | Yes |
| Verification Method | Automated tests + security review |
| Deliverable IDs | D-0008 |

**Deliverables:**
- `JwtService` class with `sign(payload, ttl): string` and `verify(token): Payload | null` methods
- RS256 algorithm enforcement

**Steps:**
1. [PLANNING] Define interface per FR-AUTH.1, FR-AUTH.3, NFR-AUTH-IMPL-1
2. [EXECUTION] Implement using jsonwebtoken library with RS256 algorithm
3. [VERIFICATION] Unit test sign/verify round-trip

**Acceptance Criteria:**
- sign() produces a valid JWT with RS256 signature
- verify() returns payload for valid tokens, null for invalid
- Algorithm is locked to RS256 (no algorithm confusion attacks)
- Tokens include standard claims (iat, exp, sub)

**Validation:**
- Manual check: Decode a produced JWT and inspect header/payload
- Evidence: Class implementation and test file committed

**Dependencies:** None

---

### T01.09 -- RS256 key pair loading from secrets manager

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | NFR-AUTH-IMPL-2 requires keys loaded from secrets manager; hardcoded keys are a critical security risk. |
| Effort | M |
| Risk | High |
| Risk Drivers | crypto, security, encryption |
| Tier | STRICT |
| Confidence | [███████---] 82% |
| Critical Path Override | Yes |
| Verification Method | Automated tests + security review |
| Deliverable IDs | D-0009 |

**Deliverables:**
- Key loading module that reads RSA 4096-bit private/public key pair from configured secrets manager
- Fallback to file-based loading for development

**Steps:**
1. [PLANNING] Design key loading interface abstracting secrets manager vs file
2. [EXECUTION] Implement secrets manager integration with dev fallback
3. [VERIFICATION] Test key loading with mock secrets manager; verify 4096-bit key size

**Acceptance Criteria:**
- Private key loaded for signing, public key for verification
- Keys are 4096-bit RSA per OQ-2 resolution
- No keys written to logs or console
- Supports both secrets manager and file-based loading

**Validation:**
- Manual check: Confirm key bit length via openssl inspection
- Evidence: Key loader module and test committed

**Dependencies:** T01.08

---

### T01.10 -- Access token TTL configuration (15 minutes)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | FR-AUTH.1a specifies 15-minute access token TTL; must be configurable for operational flexibility. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | token |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0010 |

**Deliverables:**
- Configuration entry for access token TTL with environment variable override, default 15 minutes

**Steps:**
1. [PLANNING] Define config key and env var
2. [EXECUTION] Add TTL config; wire into JwtService.sign()
3. [VERIFICATION] Test that tokens expire at configured TTL

**Acceptance Criteria:**
- Default TTL is 15 minutes (900 seconds)
- Configurable via environment variable
- JwtService uses config value for token expiration

**Validation:**
- Manual check: Decode token and verify exp claim
- Evidence: Config and test committed

**Dependencies:** T01.08

---

> **CHECKPOINT 2** (after T01.10): Verify T01.06--T01.10 pass. JwtService signs/verifies correctly. Key loading works. TTL configuration applied.

---

### T01.11 -- Unit tests for JwtService

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | SC-5 requires all services tested; JWT failure modes must be verified to prevent authentication bypasses. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | token, security |
| Tier | STRICT |
| Confidence | [█████████-] 93% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0011 |

**Deliverables:**
- Unit test suite: sign/verify round-trip, expired token rejection, tampered token rejection, wrong algorithm rejection

**Steps:**
1. [PLANNING] Identify test cases: happy path + 3 failure modes
2. [EXECUTION] Write tests for valid token, expired token, tampered payload, tampered signature
3. [VERIFICATION] Run tests; confirm all 4+ cases pass

**Acceptance Criteria:**
- Valid token: sign then verify returns original payload
- Expired token: verify returns null
- Tampered token: verify returns null
- Wrong algorithm: verify returns null

**Validation:**
- Manual check: Review test assertions for completeness
- Evidence: Test file committed; CI green

**Dependencies:** T01.08, T01.09, T01.10

---

### T01.12 -- Configure DI container with injectable services

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | NFR-AUTH-IMPL-3 requires all components to be independently testable via dependency injection. |
| Effort | S |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [█████████-] 92% |
| Critical Path Override | No |
| Verification Method | Automated test |
| Deliverable IDs | D-0012 |

**Deliverables:**
- DI container configuration supporting mock injection for all registered services

**Steps:**
1. [PLANNING] Select DI framework and define registration pattern
2. [EXECUTION] Configure container with injectable service interfaces
3. [VERIFICATION] Test that mock services can be injected

**Acceptance Criteria:**
- Container supports singleton and transient lifetimes
- All services are injectable via interface
- Mock injection works for testing

**Validation:**
- Manual check: Resolve a service from container in test
- Evidence: DI config and test committed

**Dependencies:** None

---

### T01.13 -- Register PasswordHasher and JwtService as singletons

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | Singleton registration ensures consistent state and efficient resource usage for crypto services. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [█████████-] 95% |
| Critical Path Override | No |
| Verification Method | Automated test |
| Deliverable IDs | D-0013 |

**Deliverables:**
- DI registrations for PasswordHasher and JwtService as singletons

**Steps:**
1. [PLANNING] Confirm no cross-dependencies between these services
2. [EXECUTION] Register both as singletons in DI container
3. [VERIFICATION] Test resolution returns same instance

**Acceptance Criteria:**
- Resolving PasswordHasher twice returns same instance
- Resolving JwtService twice returns same instance
- No cross-dependencies at this layer

**Validation:**
- Manual check: Identity check in test (===)
- Evidence: Registration code and test committed

**Dependencies:** T01.04, T01.08, T01.12

---

### T01.14 -- Register database connection pool as singleton

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | Database pool must be available as a singleton for Phase 2 service integration. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | database |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0014 |

**Deliverables:**
- Database connection pool registered as singleton in DI container

**Steps:**
1. [PLANNING] Define pool configuration (size, timeout, connection string)
2. [EXECUTION] Register pool factory in DI container as singleton
3. [VERIFICATION] Test that pool resolves and connects to database

**Acceptance Criteria:**
- Pool is configured via environment variables
- Singleton resolution returns same pool instance
- Pool can execute a simple query (SELECT 1)

**Validation:**
- Manual check: Verify pool connects to test database
- Evidence: Pool registration and test committed

**Dependencies:** T01.12

---

### T01.15 -- Security engineer code review of PasswordHasher and JwtService

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | NFR-AUTH-IMPL-1 and NFR-AUTH.3 require security review of all cryptographic code before downstream consumption. |
| Effort | L |
| Risk | High |
| Risk Drivers | crypto, security |
| Tier | STRICT |
| Confidence | [███████---] 78% |
| Critical Path Override | Yes |
| Verification Method | Manual security review sign-off |
| Deliverable IDs | D-0015 |

**Deliverables:**
- Signed-off security review document covering: no keys in logs, correct bcrypt usage, RS256 key handling, secrets manager integration design

**Steps:**
1. [PLANNING] Prepare review checklist from NFR-AUTH-IMPL-1, NFR-AUTH.3
2. [EXECUTION] Security engineer reviews PasswordHasher and JwtService implementations
3. [VERIFICATION] Review document signed off; any findings addressed

**Acceptance Criteria:**
- No cryptographic keys or secrets in log output
- bcrypt used correctly (proper salt generation, cost factor applied)
- RS256 key handling follows best practices
- Secrets manager integration design approved
- All findings resolved before Phase 2

**Validation:**
- Manual check: Review sign-off document exists with engineer signature
- Evidence: Review document committed to repository

**Dependencies:** T01.04, T01.07, T01.08, T01.11

---

> **CHECKPOINT 3** (after T01.15): Verify T01.11--T01.15 pass. DI container wires correctly. Crypto review signed off.

---

### T01.16 -- Verify crypto module interfaces for Phase 2 consumption

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | Service contracts must be stable before downstream services build on them to prevent rework. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [█████████-] 93% |
| Critical Path Override | No |
| Verification Method | Interface review |
| Deliverable IDs | D-0016 |

**Deliverables:**
- Interface verification document confirming PasswordHasher and JwtService contracts are stable and ready for Phase 2

**Steps:**
1. [PLANNING] List all public methods and their signatures
2. [EXECUTION] Verify interfaces match Phase 2 consumption requirements
3. [VERIFICATION] Document confirmed interfaces

**Acceptance Criteria:**
- PasswordHasher interface: hash(plaintext) and verify(plaintext, hash) confirmed
- JwtService interface: sign(payload, ttl) and verify(token) confirmed
- No breaking changes needed for Phase 2 services

**Validation:**
- Manual check: Review interface document against Phase 2 task requirements
- Evidence: Interface verification document committed

**Dependencies:** T01.15

---

> **END-OF-PHASE CHECKPOINT** (Phase 1 Gate): All units pass. Crypto review signed off. Benchmark confirms ~250ms bcrypt timing and <50ms JWT sign/verify. Migrations run up and down cleanly. DI container wires correctly. All deliverables D-0001 through D-0016 produced and verified.
