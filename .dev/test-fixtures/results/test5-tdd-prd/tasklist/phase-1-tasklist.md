# Phase 1 -- Foundation -- Data + Auth + Consent

**Phase Goal:** Stand up PostgreSQL data model, AuthService facade, core login/register flows, GDPR consent capture, lockout/rate-limit/error envelope cross-cutting guards, and NFR-SEC-001 / NFR-PERF-001 instrumentation so M1 demo is runnable end-to-end.

**Task Count:** 24 (T01.01 - T01.24)

---

## T01.01 -- DM-001 UserProfile PostgreSQL schema

- **Roadmap Item IDs:** R-001
- **Why:** M1 table structure for auth identities; every downstream flow binds to user_profiles columns per TDD Section 7.1.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** data, schema
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `models/`, `migrations/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0001
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0001/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0001 Migration file creating `user_profiles` with id UUID PK, email citext UNIQUE, password_hash, display_name, roles text[] DEFAULT '{user}', consent_accepted_at:timestamptz nullable, consent_version:varchar nullable, created_at, updated_at, last_login_at, indexes (email, created_at) per roadmap DM-001.

**Steps:**
1. **[PLANNING]** Load TDD Section 7.1 field list and constraint definitions.
2. **[PLANNING]** Check migration-framework convention and prior-migration ordinal.
3. **[EXECUTION]** Write forward migration and paired down migration.
4. **[EXECUTION]** Add indexes for email lookup and created_at reporting.
5. **[EXECUTION]** Seed integration-test fixture factory for UserProfile.
6. **[VERIFICATION]** Run migration up then down against a clean test database.
7. **[COMPLETION]** Record migration evidence path and sync Serena memory.

**Acceptance Criteria:**
- Migration creates `user_profiles` table with exactly the fields enumerated in TDD Section 7.1 and primary key is UUID.
- Down migration reverses the change with zero data loss on an empty database.
- Migration is idempotent: repeated up/down produces identical schema hash.
- Schema change recorded in `TASKLIST_ROOT/evidence/T01.01/schema.sql` and cross-linked in Deliverable Registry.

**Validation:**
- Manual check: run migration up/down on fresh test database and diff schema.
- Evidence: linkable artifact produced (schema diff log stored at TASKLIST_ROOT/evidence/T01.01/).

**Dependencies:** None
**Rollback:** Execute paired down migration.
**Notes:** Critical path override triggered by `models/` + `migrations/` path pattern.

---

## T01.02 -- DM-AUDIT Audit log PostgreSQL schema

- **Roadmap Item IDs:** R-002
- **Why:** SOC2 Type II event trail for login/register/password/admin actions, prerequisite for OPS-004 12-month retention.
- **Effort:** S
- **Risk:** High
- **Risk Drivers:** data, schema, audit, compliance
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `models/`, `migrations/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0002
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0002/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0002 Migration creating `auth_audit_log` with event_id UUID PK, user_id nullable FK, event_type enum, ip, user_agent, payload JSONB, created_at.

**Steps:**
1. **[PLANNING]** Enumerate event_type values required by M1..M6 (login_success, login_failure, register, consent_recorded, lockout_triggered).
2. **[PLANNING]** Confirm JSONB payload size limits and GIN index policy.
3. **[EXECUTION]** Write forward migration with enum and JSONB column.
4. **[EXECUTION]** Add index on (user_id, created_at DESC) and (event_type, created_at DESC).
5. **[VERIFICATION]** Run migration up/down and assert enum values present.
6. **[COMPLETION]** Record artifact paths and expose schema hash to evidence.

**Acceptance Criteria:**
- `auth_audit_log` is created with enum event_type covering the five M1 event values.
- Composite indexes allow tail-N queries per user and per event_type.
- Down migration fully reverses schema creation.
- Evidence captured at `TASKLIST_ROOT/evidence/T01.02/`.

**Validation:**
- Manual check: verify index presence via `\d+ auth_audit_log` in psql.
- Evidence: linkable artifact produced (schema script saved under evidence path).

**Dependencies:** None
**Rollback:** Down migration.
**Notes:** 12-month retention is implemented in T06.09 via OPS-004 archival job.

---

## T01.03 -- COMP-AUTHSVC AuthService orchestrator class

- **Roadmap Item IDs:** R-003
- **Why:** Facade layer keeps routes thin and centralizes password hashing, token issuance (M2), consent recording.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0003
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0003/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0003 `src/services/auth-service.ts` exporting `AuthService` facade with `login`, `register`, `changePassword`, `requestReset`, `confirmReset` method stubs typed per TDD.

**Steps:**
1. **[PLANNING]** Load TDD component diagram and dependency list.
2. **[PLANNING]** Define public method signatures only (implementations land in later tasks).
3. **[EXECUTION]** Introduce constructor-injection for PasswordHasher, UserRepo, TokenManager, ConsentRecorder.
4. **[EXECUTION]** Add type-only interfaces for each injected dependency.
5. **[VERIFICATION]** Assert type-checker builds clean with placeholder implementations.
6. **[COMPLETION]** Document method ownership table in notes.md.

**Acceptance Criteria:**
- `AuthService` exposes the five facade methods with TDD-aligned signatures.
- All injected dependencies are interface-typed, enabling test doubles.
- File compiles with `tsc --noEmit` against the repo config.
- Facade registered in DI container per repo convention.

**Validation:**
- Manual check: run `tsc --noEmit` and verify no diagnostics.
- Evidence: linkable artifact produced (build log at TASKLIST_ROOT/evidence/T01.03/).

**Dependencies:** T01.01
**Rollback:** Revert facade file and DI registration commit.
**Notes:** Intentionally does not implement methods yet; those land in T01.04-T01.11.

---

## T01.04 -- COMP-PWDHASH PasswordHasher component

- **Roadmap Item IDs:** R-004
- **Why:** Enforces NFR-SEC-001 cost-12 bcrypt floor; central abstraction so future PHC upgrade is a single-file change.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** auth, security
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0004
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0004/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0004 `src/services/password-hasher.ts` wrapping bcrypt with `hash(password)` and `verify(hash, password)`; cost factor hard-coded to 12 with exported `BCRYPT_COST = 12` constant.

**Steps:**
1. **[PLANNING]** Confirm bcrypt binding version and platform availability.
2. **[EXECUTION]** Implement hash() using cost 12 and verify() using timing-safe compare.
3. **[EXECUTION]** Reject cost lower than 12 at runtime with explicit error.
4. **[VERIFICATION]** Unit-test happy + invalid-cost paths.
5. **[COMPLETION]** Attach module notes referencing NFR-SEC-001.

**Acceptance Criteria:**
- `PasswordHasher.hash` produces a bcrypt hash with cost 12 (prefix `$2b$12$`).
- `PasswordHasher.verify` returns true only for matching password/hash pair.
- Runtime rejects attempts to construct with cost < 12.
- Module documented in notes.md linking NFR-SEC-001.

**Validation:**
- Manual check: inspect produced hash prefix `$2b$12$`.
- Evidence: linkable artifact produced (unit test run log at evidence/T01.04/).

**Dependencies:** T01.03
**Rollback:** Remove file and unregister DI binding.
**Notes:** T01.14 is the dedicated cost-floor unit test.

---

## T01.05 -- COMP-USERREPO UserRepo data-access component

- **Roadmap Item IDs:** R-005
- **Why:** Single DB access layer for UserProfile; keeps transaction boundaries out of AuthService.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** data
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `models/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0005
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0005/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0005 `src/repositories/user-repo.ts` with `findByEmail`, `createUser`, `updateProfile`, `updatePasswordHash` using pg Pool or Prisma per repo convention.

**Steps:**
1. **[PLANNING]** Confirm existing DB client abstraction.
2. **[EXECUTION]** Implement findByEmail with case-insensitive citext lookup.
3. **[EXECUTION]** Implement createUser enforcing unique email with 409 error mapping.
4. **[EXECUTION]** Implement updateProfile and updatePasswordHash with row-version guard.
5. **[VERIFICATION]** Integration-test CRUD against test DB from T01.01.
6. **[COMPLETION]** Document transaction policy in notes.md.

**Acceptance Criteria:**
- CRUD methods match the AuthService facade dependency interface.
- Unique email violation surfaces as domain-specific error, not raw SQL error.
- Updates are transactional per request.
- Evidence: integration log capturing CRUD assertions.

**Validation:**
- Manual check: run integration tests against user_profiles.
- Evidence: linkable artifact produced (log at evidence/T01.05/).

**Dependencies:** T01.01, T01.03
**Rollback:** Remove repo class and DI binding.
**Notes:** Unit tests for repo live alongside; integration test covered by T01.21.

---

Checkpoint: Phase 1 / Tasks 1-5

- **Purpose:** Confirm schema + core component scaffolding are coherent before implementing business logic.
- **Verification:**
  - Migrations for `user_profiles` and `auth_audit_log` apply cleanly up/down.
  - AuthService, PasswordHasher, UserRepo TypeScript compiles with no diagnostics.
  - DI wiring registers all three components under documented keys.
- **Exit Criteria:**
  - Evidence paths populated for T01.01-T01.05.
  - Schema hashes recorded for both tables.
  - No STRICT task flagged "Requires Confirmation" unresolved.

---

## T01.06 -- COMP-CONSENT-REC ConsentRecorder component

- **Roadmap Item IDs:** R-006
- **Why:** GDPR consent is pulled forward from M3 to M1 to satisfy data-minimization: registration row persists consent with timestamp and audit event.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** compliance
- **Tier:** STRICT
- **Confidence:** [████████--] 80%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0006
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0006/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0006 `src/services/consent-recorder.ts` writing consent_accepted_at + consent_version to UserProfile and emitting `consent_recorded` audit event.

**Steps:**
1. **[PLANNING]** Align field names with DM-001 schema.
2. **[EXECUTION]** Implement `record(userId, consentFlag)` updating UserProfile and writing audit log.
3. **[EXECUTION]** Add validation: consentFlag must be boolean; reject null.
4. **[VERIFICATION]** Unit-test record() on accept/reject paths.
5. **[COMPLETION]** Link to NFR-GDPR-CONSENT and R-PRD-001 in notes.

**Acceptance Criteria:**
- Consent write is atomic with audit emission (single transaction).
- Rejects non-boolean consent value.
- Audit event payload includes user_id, consent_accepted_at+consent_version, timestamp.
- Artifact trail stored at TASKLIST_ROOT/evidence/T01.06/.

**Validation:**
- Manual check: trigger record() and query auth_audit_log for consent_recorded.
- Evidence: linkable artifact produced (test run log).

**Dependencies:** T01.01, T01.02, T01.05
**Rollback:** Remove service and revert AuthService.register wiring when T01.16 lands.
**Notes:** Actual wiring into /auth/register occurs in T01.16.

---

## T01.07 -- FR-AUTH-001 Login authentication logic

- **Roadmap Item IDs:** R-007
- **Why:** First vertical slice -- AuthService.login validates credentials via PasswordHasher and emits audit log with IP/UA.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0007
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0007/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0007 `AuthService.login()` returning profile summary + tokens (tokens stubbed until M2) and logging login_success / login_failure.

**Steps:**
1. **[PLANNING]** Refine contract: return type excludes password_hash.
2. **[EXECUTION]** Fetch user by email; map not-found to generic 401.
3. **[EXECUTION]** Verify password via PasswordHasher.
4. **[EXECUTION]** Emit login_success or login_failure audit event with IP/UA.
5. **[VERIFICATION]** Unit-test valid + invalid paths (see T01.19, T01.20).
6. **[COMPLETION]** Record open TODO for token issuance wiring in Phase 2.

**Acceptance Criteria:**
- Valid credential path returns UserProfile summary without password_hash.
- Invalid credential path returns 401 with no user enumeration.
- Audit entry created on every attempt (success or failure).
- Method honors PasswordHasher timing-safe compare.

**Validation:**
- Manual check: unit tests for login valid/invalid assert behavior.
- Evidence: linkable artifact produced (unit test log).

**Dependencies:** T01.03, T01.04, T01.05, T01.02
**Rollback:** Revert method body to throw NotImplementedError.
**Notes:** Token issuance stubbed until T02.06 implements FR-AUTH-003.

---

## T01.08 -- FR-AUTH-002 Registration with validation

- **Roadmap Item IDs:** R-008
- **Why:** Creates UserProfile with email-uniqueness policy and (per CONFLICT-2) returns 201 without auto-login.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0008
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0008/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0008 `AuthService.register()` persisting new UserProfile, invoking ConsentRecorder, returning 201 with profile summary (no tokens).

**Steps:**
1. **[PLANNING]** Confirm registration input schema per TDD Section 8.2.
2. **[EXECUTION]** Validate email format and password complexity.
3. **[EXECUTION]** Hash password then persist via UserRepo.createUser.
4. **[EXECUTION]** Record consent via ConsentRecorder (T01.06).
5. **[VERIFICATION]** Integration-test register persistence (T01.21).
6. **[COMPLETION]** Note CONFLICT-2 decision in notes.md.

**Acceptance Criteria:**
- Registration returns 201 with UserProfile summary and no access/refresh tokens.
- Duplicate email returns domain conflict (409 mapping at route layer).
- Consent flag and timestamp persisted atomically with profile creation.
- Password never logged or returned.

**Validation:**
- Manual check: integration test asserts 201 + no tokens on POST /auth/register.
- Evidence: linkable artifact produced (integration log).

**Dependencies:** T01.04, T01.05, T01.06
**Rollback:** Revert method body and routing binding.
**Notes:** CONFLICT-2 committed default: register returns 201 and client redirects to /login.

---

## T01.09 -- API-001 POST /auth/login endpoint

- **Roadmap Item IDs:** R-009
- **Why:** HTTP contract for login per TDD Section 8.2; binds AuthService.login to Express/Fastify router with error envelope.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0009
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0009/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0009 `src/routes/auth/login.ts` POST route binding AuthService.login with request validation and unified error envelope.

**Steps:**
1. **[PLANNING]** Load TDD Section 8.2 request/response schema.
2. **[EXECUTION]** Validate request body (email, password).
3. **[EXECUTION]** Call AuthService.login and map errors to {error:{code,message,status}}.
4. **[EXECUTION]** Return 200 with profile summary on success; 401 on invalid credentials.
5. **[VERIFICATION]** Route contract test covering 200/400/401.
6. **[COMPLETION]** Record OpenAPI stub path.

**Acceptance Criteria:**
- 200 response on valid credentials with profile summary (no password field).
- 401 on invalid credentials with unified error envelope.
- 400 on malformed request body.
- Route registered with rate-limit policy in T01.13.

**Validation:**
- Manual check: call POST /auth/login with Postman fixtures.
- Evidence: linkable artifact produced (contract test log).

**Dependencies:** T01.07, T01.12
**Rollback:** Unregister route and revert commit.
**Notes:** Access/refresh token issuance arrives in Phase 2 via T02.08.

---

## T01.10 -- API-002 POST /auth/register endpoint

- **Roadmap Item IDs:** R-010
- **Why:** HTTP contract for register per TDD Section 8.2; CONFLICT-2 committed default 201-without-auto-login.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0010
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0010/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0010 `src/routes/auth/register.ts` POST route binding AuthService.register returning 201 profile + Location header `/auth/login`.

**Steps:**
1. **[PLANNING]** Load TDD Section 8.2 and confirm CONFLICT-2 default.
2. **[EXECUTION]** Validate registration payload (email, password, consent_accepted_at+consent_version).
3. **[EXECUTION]** Call AuthService.register; map duplicate-email to 409.
4. **[EXECUTION]** Return 201 with Location header pointing to /auth/login.
5. **[VERIFICATION]** Contract test for 201, 400, 409 cases.
6. **[COMPLETION]** Document CONFLICT-2 decision in notes.md.

**Acceptance Criteria:**
- 201 response with profile summary and Location header; no access/refresh tokens.
- 409 Conflict on duplicate email via unified error envelope.
- 400 on validation failures (missing or malformed fields).
- CONFLICT-2 decision linked in notes.md.

**Validation:**
- Manual check: POST /auth/register asserts 201 and absent tokens.
- Evidence: linkable artifact produced (contract test log).

**Dependencies:** T01.08, T01.12
**Rollback:** Unregister route.
**Notes:** Client redirects to /auth/login per CONFLICT-2 default.

---

Checkpoint: Phase 1 / Tasks 6-10

- **Purpose:** Validate login/register vertical slices are wired end-to-end before lockout + NFR work.
- **Verification:**
  - POST /auth/login happy path returns 200 profile summary.
  - POST /auth/register happy path returns 201 + Location header with consent persisted.
  - Audit log entries created for login_success, login_failure, register, consent_recorded.
- **Exit Criteria:**
  - Contract tests for both routes pass.
  - No PII or password-hash appears in any log.
  - CONFLICT-2 decision recorded in Phase 1 notes.

---

## T01.11 -- FEAT-LOCK Account lockout enforcement

- **Roadmap Item IDs:** R-011
- **Why:** Lockout after 5 failed attempts within 15 minutes; prevents brute-force and feeds METRIC-LOGIN lockout signal.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** security, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0011
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0011/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0011 `src/services/account-lockout.ts` Redis-backed counter (key per email), 15-min rolling window, 5-attempt threshold, 423 response mapping.

**Steps:**
1. **[PLANNING]** Define Redis key pattern `lockout:<email>` and TTL 15m.
2. **[EXECUTION]** Increment on login_failure; clear on login_success.
3. **[EXECUTION]** Return locked state to AuthService.login and map to 423 Locked at route.
4. **[EXECUTION]** Emit lockout_triggered audit event at threshold.
5. **[VERIFICATION]** Unit-test threshold, window-reset, and unlock paths.
6. **[COMPLETION]** Link to FEAT-LOCK docs in notes.md.

**Acceptance Criteria:**
- 5th failure within 15 minutes produces 423 Locked.
- Counter resets after successful login.
- Audit event `lockout_triggered` emitted exactly once per lock.
- Unit tests cover threshold, rolling window reset, unlock.

**Validation:**
- Manual check: replay 5 failures via curl and observe 423.
- Evidence: linkable artifact produced (unit test log).

**Dependencies:** T01.07
**Rollback:** Disable lockout middleware flag.
**Notes:** Admin unlock endpoint arrives in Phase 5 (T05.03).

---

## T01.12 -- API-ERR Unified error envelope middleware

- **Roadmap Item IDs:** R-012
- **Why:** All /auth/* endpoints must share `{error:{code,message,status}}` shape for client parsers.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0012
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0012/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0012 `src/middleware/error-envelope.ts` mapping domain errors to unified JSON envelope with status propagation.

**Steps:**
1. **[PLANNING]** Enumerate domain error types produced by AuthService.
2. **[EXECUTION]** Build middleware translating each domain error to envelope.
3. **[EXECUTION]** Register middleware after all /auth/* routes.
4. **[VERIFICATION]** Integration test: trigger each error class and assert envelope.
5. **[COMPLETION]** Document code ids (e.g., AUTH_INVALID_CREDENTIALS, AUTH_LOCKED).

**Acceptance Criteria:**
- Every /auth/* error response matches `{error:{code,message,status}}`.
- Status codes align with per-route matrices (400/401/409/423/429).
- No stack traces emitted to clients.
- Codes documented in notes.md.

**Validation:**
- Manual check: trigger 401 and 423 responses; diff JSON shape.
- Evidence: linkable artifact produced (integration log).

**Dependencies:** T01.09, T01.10
**Rollback:** Remove middleware registration.
**Notes:** Reused by all later auth routes (refresh, logout, password).

---

## T01.13 -- API-RATE Rate limiting configuration

- **Roadmap Item IDs:** R-013
- **Why:** 10/min login per IP and 5/min register per IP; defense-in-depth against credential stuffing.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0013
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0013/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0013 API gateway configuration (or express-rate-limit middleware) enforcing 10/min login + 5/min register per IP with 429 envelope response.

**Steps:**
1. **[PLANNING]** Confirm infra gateway vs app-layer approach (committed default: app-layer for parity across environments).
2. **[EXECUTION]** Configure per-IP limiter keyed on X-Forwarded-For.
3. **[EXECUTION]** Return 429 via unified error envelope when exceeded.
4. **[VERIFICATION]** Load test burst > threshold and assert 429.
5. **[COMPLETION]** Document limiter config in notes.md.

**Acceptance Criteria:**
- Login: 10 req/min per IP, 11th returns 429.
- Register: 5 req/min per IP, 6th returns 429.
- 429 responses use unified error envelope.
- Limiter config version-controlled.

**Validation:**
- Manual check: burst-send via `hey` or `ab` and confirm 429 threshold.
- Evidence: linkable artifact produced (load test log).

**Dependencies:** T01.12
**Rollback:** Disable limiter flag.
**Notes:** Policy reversible via config; no external dependency added.

---

## T01.14 -- NFR-SEC-001 bcrypt cost 12 validation test

- **Roadmap Item IDs:** R-014
- **Why:** Regression gate ensures PasswordHasher never silently drops to cost < 12.
- **Effort:** XS
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [████████--] 80%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0014
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0014/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0014 `tests/unit/password-hasher.spec.ts` asserting cost factor 12 in generated hash prefix and rejection at construction with lower cost.

**Steps:**
1. **[PLANNING]** Confirm bcrypt prefix pattern `$2b$12$`.
2. **[EXECUTION]** Write passing test for cost-12 prefix.
3. **[EXECUTION]** Write failing-construction test for cost < 12.
4. **[VERIFICATION]** Run test suite; expect both passing.

**Acceptance Criteria:**
- Test fails if bcrypt cost drops below 12.
- Test green on HEAD after T01.04 implementation.
- No runtime dependency beyond unit test harness.
- Test file path recorded in notes.

**Validation:**
- Manual check: `pytest tests/unit/password-hasher.spec.ts` returns green.
- Evidence: linkable artifact produced (test result log).

**Dependencies:** T01.04
**Rollback:** Remove test file.
**Notes:** Minimal regression guard; extends when PHC library swaps.

---

## T01.15 -- NFR-SEC-003 Transport and log redaction baseline

- **Roadmap Item IDs:** R-015
- **Why:** TLS 1.3 at ingress + Pino redact list prevents secrets/password leakage in logs.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** security, audit
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0015
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0015/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0015 Ingress TLS 1.3 config + Pino `redact: ['password','token','authorization','cookie']` middleware applied globally.

**Steps:**
1. **[PLANNING]** Review current ingress TLS version.
2. **[EXECUTION]** Update ingress manifest to enforce TLS 1.3 only.
3. **[EXECUTION]** Apply Pino redact config globally.
4. **[VERIFICATION]** Emit a log line containing password field; assert `[Redacted]` substitute.
5. **[COMPLETION]** Document redaction key list in notes.md.

**Acceptance Criteria:**
- Ingress rejects TLS < 1.3.
- Logs never contain raw password, token, authorization, or cookie values.
- Redaction config held in source control.
- Evidence includes before/after log sample.

**Validation:**
- Manual check: curl over TLS 1.2 is rejected.
- Evidence: linkable artifact produced (redacted log sample).

**Dependencies:** T01.12
**Rollback:** Re-enable TLS 1.2 for break-glass only.
**Notes:** Redaction list re-used by OBS-002 in T05.08.

---

Checkpoint: Phase 1 / Tasks 11-15

- **Purpose:** Confirm abuse-resistance (lockout, rate limit) and baseline secure transport/logging before NFR wave.
- **Verification:**
  - Lockout produces 423 on 5th failure within 15 min.
  - Rate limiter returns 429 at 11 login / 6 register per IP per min.
  - TLS 1.3 enforced and redaction applied globally.
- **Exit Criteria:**
  - Audit events include lockout_triggered.
  - Unified error envelope covers 401/409/423/429.
  - No credential leakage observed in redacted log sample.

---

## T01.16 -- NFR-GDPR-CONSENT Consent capture at registration

- **Roadmap Item IDs:** R-016
- **Why:** Wires ConsentRecorder into /auth/register path for data-minimization; required for R-PRD-001.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** compliance
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0016
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0016/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0016 Wiring in AuthService.register + /auth/register validation to require consent_accepted_at+consent_version and invoke ConsentRecorder.

**Steps:**
1. **[PLANNING]** Confirm consent_accepted_at+consent_version is mandatory at registration (no soft-opt).
2. **[EXECUTION]** Add schema validation: consent_accepted_at+consent_version must be boolean true for service ToS.
3. **[EXECUTION]** Invoke ConsentRecorder inside the same transaction as createUser.
4. **[VERIFICATION]** Integration test asserts UserProfile.consent_accepted_at+consent_version=true and audit event emitted.
5. **[COMPLETION]** Document R-PRD-001 compliance in notes.md.

**Acceptance Criteria:**
- Missing consent_accepted_at+consent_version returns 400 with unified envelope.
- UserProfile.consent_accepted_at + consent_version persisted in single transaction.
- Audit event `consent_recorded` contains user_id and timestamp.
- Compliance traceability linked in notes.

**Validation:**
- Manual check: register without consent_accepted_at+consent_version returns 400.
- Evidence: linkable artifact produced (integration log).

**Dependencies:** T01.06, T01.08
**Rollback:** Revert validation + service call.
**Notes:** Pulled forward from M3 per roadmap decision.

---

## T01.17 -- NFR-PERF-001 Login latency p95 instrumentation

- **Roadmap Item IDs:** R-017
- **Why:** Prometheus histogram + p95 alert rule provides SLO signal for login latency < 200ms.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0017
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0017/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0017 `auth_login_duration_ms` histogram metric + `AlertLoginLatencyHigh` Prometheus rule (p95 > 200ms sustained 5m).

**Steps:**
1. **[PLANNING]** Define histogram bucket boundaries aligned to SLO.
2. **[EXECUTION]** Instrument AuthService.login start/stop timers.
3. **[EXECUTION]** Commit Prometheus rule file to `ops/prometheus/rules/auth.yml`.
4. **[VERIFICATION]** Run load harness and observe p95 in Grafana.
5. **[COMPLETION]** Record rule path in notes.md.

**Acceptance Criteria:**
- Histogram exposed at /metrics.
- Alert rule fires when p95 > 200ms for 5m.
- Bucket boundaries documented and reproducible.
- Rule version-controlled.

**Validation:**
- Manual check: query `histogram_quantile(0.95, sum(rate(auth_login_duration_ms_bucket[5m])) by (le))`.
- Evidence: linkable artifact produced (alert rule file + Grafana screenshot).

**Dependencies:** T01.09
**Rollback:** Remove histogram + rule.
**Notes:** Rule wired into Phase 6 ALERT-LATENCY (T06.12) for rollback trigger.

---

## T01.18 -- NFR-PERF-002 k6 500-user concurrent profile

- **Roadmap Item IDs:** R-018
- **Why:** Verifies 500 concurrent logins sustain <200ms p95 before GA freeze.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** performance
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0018
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0018/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0018 `tests/load/login.js` k6 script ramping to 500 VUs for 10m with thresholds `http_req_duration{p(95)}<200`.

**Steps:**
1. **[PLANNING]** Confirm staging env capacity and dedicated DB.
2. **[EXECUTION]** Author k6 script with ramp, hold, cool-down stages.
3. **[EXECUTION]** Register threshold assertions per roadmap NFR.
4. **[VERIFICATION]** Run script against staging; capture HTML report.
5. **[COMPLETION]** Store baseline report in evidence path.

**Acceptance Criteria:**
- k6 report shows p95 < 200ms at 500 VUs sustained 10m.
- Error rate < 1%.
- Threshold assertions pass in k6 exit code 0.
- Baseline committed to evidence.

**Validation:**
- Manual check: `k6 run tests/load/login.js` threshold pass.
- Evidence: linkable artifact produced (k6 html/json report).

**Dependencies:** T01.17
**Rollback:** Retire load script.
**Notes:** Separate from E2E; runs manually before GA freeze.

---

## T01.19 -- TEST-001 Unit login valid credentials

- **Roadmap Item IDs:** R-019
- **Why:** Locks in FR-AUTH-001 happy path regression gate per TDD Section 15.2.
- **Effort:** XS
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [████████--] 80%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0019
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0019/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0019 `tests/unit/auth-service.login-valid.spec.ts` asserting AuthService.login returns profile summary (no password_hash) and emits login_success audit.

**Steps:**
1. **[PLANNING]** Seed test user via factory.
2. **[EXECUTION]** Stub PasswordHasher.verify to true.
3. **[EXECUTION]** Call AuthService.login and assert return shape.
4. **[VERIFICATION]** Verify audit spy captured login_success.

**Acceptance Criteria:**
- Returned payload excludes password_hash.
- login_success audit emitted exactly once.
- No network or DB side effect outside test fixtures.
- Test file path recorded in notes.

**Validation:**
- Manual check: run targeted test file.
- Evidence: linkable artifact produced (test run log).

**Dependencies:** T01.07
**Rollback:** Remove test file.
**Notes:** Happy path gate; failure path in T01.20.

---

## T01.20 -- TEST-002 Unit login invalid credentials

- **Roadmap Item IDs:** R-020
- **Why:** Locks in FR-AUTH-001 invalid path (401 + no user enumeration) per TDD Section 15.2.
- **Effort:** XS
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [████████--] 80%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0020
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0020/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0020 `tests/unit/auth-service.login-invalid.spec.ts` asserting 401 mapping + login_failure audit + no user enumeration.

**Steps:**
1. **[PLANNING]** Confirm domain error is AuthInvalidCredentials.
2. **[EXECUTION]** Stub PasswordHasher.verify to false.
3. **[EXECUTION]** Assert thrown domain error maps to 401 + envelope.
4. **[VERIFICATION]** Verify audit spy captured login_failure.

**Acceptance Criteria:**
- Thrown error is AuthInvalidCredentials.
- Response body never discloses whether email exists.
- login_failure audit emitted on every attempt.
- Test file referenced in notes.

**Validation:**
- Manual check: run targeted test file.
- Evidence: linkable artifact produced (test run log).

**Dependencies:** T01.07
**Rollback:** Remove test file.
**Notes:** Pair with T01.19 for full login contract coverage.

---

Checkpoint: Phase 1 / Tasks 16-20

- **Purpose:** Validate NFR/test gates before logging/metrics finishing sprint of Phase 1.
- **Verification:**
  - GDPR consent required on /auth/register.
  - Login latency histogram + alert rule green in staging.
  - Unit tests TEST-001 and TEST-002 pass.
- **Exit Criteria:**
  - k6 script committed with baseline report.
  - p95 stays under 200ms in staging baseline.
  - No regression in login contract.

---

## T01.21 -- TEST-004 Integration register persists UserProfile

- **Roadmap Item IDs:** R-021
- **Why:** End-to-end verifier that /auth/register persists UserProfile with consent per TDD Section 15.2.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [████████--] 80%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0021
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0021/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0021 `tests/integration/register.spec.ts` POSTing /auth/register then asserting row in user_profiles and audit entries.

**Steps:**
1. **[PLANNING]** Prepare test DB via migration from T01.01.
2. **[EXECUTION]** POST /auth/register via supertest.
3. **[EXECUTION]** Query user_profiles and auth_audit_log for expected rows.
4. **[VERIFICATION]** Assert consent_accepted_at+consent_version=true, hashed password persisted, two audit events present.

**Acceptance Criteria:**
- New user row exists with matching email and consent_accepted_at+consent_version=true.
- Password column holds bcrypt hash (starts with $2b$12$).
- Two audit events: register, consent_recorded.
- Location header on 201 equals `/auth/login`.

**Validation:**
- Manual check: run integration suite against test DB.
- Evidence: linkable artifact produced (integration log).

**Dependencies:** T01.10, T01.16
**Rollback:** Remove test file.
**Notes:** Lives in `tests/integration` to align with pytest-based convention.

---

## T01.22 -- OPS-LOG-M1 Structured login/registration logging

- **Roadmap Item IDs:** R-022
- **Why:** stdout JSON logs for login_success/failure/register enable centralized Loki ingestion in Phase 6.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0022
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0022/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0022 Structured logger wiring (pino) emitting `event`, `user_id`, `ip`, `ua`, `outcome` for each login/register request.

**Steps:**
1. **[PLANNING]** Select logger per repo convention (pino).
2. **[EXECUTION]** Add log emission helpers in AuthService.login / register.
3. **[EXECUTION]** Ensure redact list applied (see T01.15).
4. **[VERIFICATION]** Integration test captures stdout and asserts JSON shape.

**Acceptance Criteria:**
- Every login attempt produces a JSON log line with outcome + ip + ua.
- Every registration produces a log line with event=register.
- Redacted fields absent from emitted JSON.
- Log schema documented in notes.md.

**Validation:**
- Manual check: tail stdout during integration test and grep outcome=failure.
- Evidence: linkable artifact produced (captured stdout sample).

**Dependencies:** T01.09, T01.10, T01.15
**Rollback:** Remove log calls.
**Notes:** Feeds OBS-002/003 pipeline in Phase 5 and Loki in Phase 6.

---

## T01.23 -- METRIC-REG Registration counter

- **Roadmap Item IDs:** R-023
- **Why:** `auth_registration_total` counter is required by OPS-004 audit reporting and Grafana dashboards.
- **Effort:** XS
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0023
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0023/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0023 Prometheus counter `auth_registration_total` incremented on successful register, exposed via /metrics.

**Steps:**
1. **[PLANNING]** Verify metric name free of collision.
2. **[EXECUTION]** Define counter + increment in AuthService.register.
3. **[VERIFICATION]** Hit /metrics and grep counter.

**Acceptance Criteria:**
- Counter increments once per successful register.
- Exposed at /metrics in Prometheus exposition format.
- Label set is empty (total) to keep cardinality low.
- Name matches roadmap id.

**Validation:**
- Manual check: curl /metrics | grep auth_registration_total.
- Evidence: linkable artifact produced (metrics scrape sample).

**Dependencies:** T01.10
**Rollback:** Remove counter registration.
**Notes:** Re-used by Grafana board in Phase 5 (T05.10).

---

## T01.24 -- METRIC-LOGIN Login counter

- **Roadmap Item IDs:** R-024
- **Why:** `auth_login_total{outcome=success|failure|locked}` feeds SLI + rollback triggers.
- **Effort:** XS
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0024
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0024/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0024 Prometheus counter `auth_login_total` with `outcome` label (success|failure|locked), incremented per attempt.

**Steps:**
1. **[PLANNING]** Define label cardinality and outcome values.
2. **[EXECUTION]** Register counter; increment in AuthService.login for each outcome.
3. **[VERIFICATION]** Assert three distinct outcome buckets appear after mixed test traffic.

**Acceptance Criteria:**
- Counter increments exactly once per login attempt.
- Label `outcome` takes only the enumerated values.
- Exposed at /metrics.
- Used downstream by ALERT-LOGIN-FAIL (T06.11) and ROLLBACK-AUTO-ERR (T06.15).

**Validation:**
- Manual check: curl /metrics | grep auth_login_total.
- Evidence: linkable artifact produced (metrics scrape sample).

**Dependencies:** T01.07, T01.11
**Rollback:** Remove counter registration.
**Notes:** Outcome=locked ties to FEAT-LOCK threshold event.

---

Checkpoint: Phase 1 / Tasks 21-24 + End of Phase

- **Purpose:** Confirm M1 scope complete with metrics + logs backing observability handoff into M2.
- **Verification:**
  - Integration test TEST-004 passes.
  - Structured logs produced on every auth event.
  - `auth_login_total` and `auth_registration_total` exported at /metrics.
- **Exit Criteria:**
  - All 24 tasks marked complete with evidence paths populated.
  - No STRICT task left open.
  - Phase 1 exit review signed off.

Checkpoint: End of Phase 1

- **Purpose:** M1 foundation ready for M2 token-management wiring.
- **Verification:**
  - Demo: register -> login -> login fail x5 -> locked -> admin unlock pending in Phase 5.
  - NFR-SEC-001 cost-12 gate green.
  - NFR-PERF-001 p95 baseline under 200ms in staging.
- **Exit Criteria:**
  - M1 DoD items (1)-(10) from roadmap satisfied with evidence.
  - Phase 2 Clarification Task T02.01 ready to start.
  - No carry-over STRICT defects open.
