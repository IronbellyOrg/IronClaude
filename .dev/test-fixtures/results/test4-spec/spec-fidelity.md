---
high_severity_count: 2
medium_severity_count: 5
low_severity_count: 2
total_deviations: 9
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: The `UserRecord` data model in the spec defines an `updated_at: Date` field. The roadmap's database schema task (DM-001) omits this field entirely.
- **Source Quote**: `interface UserRecord { ... updated_at: Date; }` (spec Section 4.5, line 188)
- **Roadmap Quote**: `Schema: id (UUID PK), email (unique index), display_name, password_hash, created_at, locked_at (nullable); reviewed and approved` (roadmap DM-001, line 109)
- **Impact**: Implementations following the roadmap will create a `users` table missing the `updated_at` column. Any downstream consumer expecting this field (profile responses, audit trails, cache invalidation) will fail or require a follow-up migration. The spec explicitly includes it as part of the interface contract.
- **Recommended Correction**: Add `updated_at (timestamptz, NOT NULL, default now())` to DM-001 acceptance criteria. The migration (MIG-001) must include this column. The field should also be returned by FR-AUTH.4a if `updated_at` is part of the profile response DTO.

---

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Deviation**: The spec defines `src/auth/auth-service.ts` as a new file and the central orchestrator in the module dependency graph. The roadmap creates explicit COMP tasks for every other new file (COMP-001 through COMP-007) but has no COMP task for `AuthService`. Endpoint handlers (FR-AUTH.1, FR-AUTH.2, etc.) appear to absorb orchestration logic directly.
- **Source Quote**: `| src/auth/auth-service.ts | Core authentication orchestrator; coordinates login, register, refresh, and reset flows | TokenManager, PasswordHasher, User repository |` (spec Section 4.1, line 149) and the dependency graph: `auth-middleware.ts → auth-service.ts → token-manager.ts / password-hasher.ts` (spec Section 4.4, lines 165-175)
- **Roadmap Quote**: [MISSING] — No COMP-00X task creates `auth-service.ts`. Phase 1 tasks (FR-AUTH.1, FR-AUTH.2) list component as "Auth API" and depend directly on COMP-001 (PasswordHasher) and COMP-003 (TokenManager), bypassing the orchestrator layer.
- **Impact**: Without an explicit `AuthService` class, the spec's layered architecture (routes → AuthService → TokenManager/PasswordHasher) collapses. Business logic (credential verification, token issuance sequencing, session invalidation) may be embedded directly in route handlers, reducing testability and violating the spec's design decision that "all components are injectable and independently testable." The spec's unit tests (Section 8.1) explicitly test `AuthService.login` and `AuthService.register` as methods on this class.
- **Recommended Correction**: Add a COMP task (e.g., COMP-008) in Phase 0 or early Phase 1: "Implement AuthService orchestrator in `src/auth/auth-service.ts`" with dependencies on COMP-001, COMP-003, and DM-001. Update FR-AUTH endpoint tasks to depend on AuthService rather than directly on PasswordHasher and TokenManager.

---

### DEV-003
- **ID**: DEV-003
- **Severity**: MEDIUM
- **Deviation**: The spec's workflow diagram uses the endpoint path `GET /auth/me` for authenticated profile retrieval. The roadmap uses `GET /auth/profile` throughout.
- **Source Quote**: `|-- GET /auth/me ---------->|` and `(Bearer access_token)   |-- verify token -------->|` (spec Section 2.2, line 75)
- **Roadmap Quote**: `GET /auth/profile (API-004)` (roadmap Section 2.3, line 67) and `Wire GET /auth/profile route (protected by AuthMiddlewareChain)` (roadmap Phase 2 API-004, line 176)
- **Impact**: API consumers referencing the spec's workflow diagram would expect `/auth/me`, not `/auth/profile`. If the spec is used as the API contract during development, this naming mismatch will cause confusion or 404 errors on the client side. The deviation is MEDIUM rather than HIGH because FR-AUTH.4 in the spec does not explicitly state the endpoint path — only the workflow diagram does.
- **Recommended Correction**: Align the roadmap to the spec's `GET /auth/me` path, or update the spec's workflow diagram to use `/auth/profile`. The decision should be documented as a deliberate API naming choice.

---

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: The spec defines `UserRecord.is_locked` as a `boolean` field. The roadmap's schema (DM-001) uses `locked_at (nullable)` — a nullable timestamp — which changes the field's type and semantics.
- **Source Quote**: `is_locked: boolean;       // Account suspension flag` (spec Section 4.5, line 185)
- **Roadmap Quote**: `Schema: id (UUID PK), email (unique index), display_name, password_hash, created_at, locked_at (nullable)` (roadmap DM-001, line 109)
- **Impact**: The roadmap's `locked_at` is arguably a better design (captures when the lock occurred), but it contradicts the spec's interface definition. Code written against the spec's `UserRecord` interface would check `if (user.is_locked)` while the roadmap's implementation would check `if (user.locked_at !== null)`. The roadmap's FR-AUTH.1c acceptance criteria already adapts to this change ("Account with non-null locked_at"), showing internal consistency — but the spec-roadmap contract is broken.
- **Recommended Correction**: Update the spec's `UserRecord` interface to use `locked_at: Date | null` if the timestamp approach is preferred, or revert DM-001 to `is_locked (boolean, default false)` to match the spec.

---

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: The spec defines `RefreshTokenRecord.revoked` as a `boolean` field. The roadmap's schema (DM-002) uses `revoked_at (nullable)` — a nullable timestamp.
- **Source Quote**: `revoked: boolean;` (spec Section 4.5, line 194)
- **Roadmap Quote**: `Schema: id (UUID PK), user_id (FK → users, indexed), token_hash (SHA-256), expires_at, revoked_at (nullable), created_at` (roadmap DM-002, line 110)
- **Impact**: Same category as DEV-004. The semantic change from boolean to timestamp alters the query pattern (`WHERE revoked = true` vs `WHERE revoked_at IS NOT NULL`) and the interface contract. The roadmap's Phase 3 FR-AUTH.5d references `revoked_at set` (line 216), confirming internal consistency with the changed schema, but divergence from the spec's interface definition.
- **Recommended Correction**: Align spec and roadmap on the field type. If `revoked_at` is preferred, update the spec's `RefreshTokenRecord` interface.

---

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: The spec's test plan (Section 8.1) lists a dedicated unit test for `TokenManager`: "TokenManager issues token pairs and rotates refresh tokens" in file `tests/auth/token-manager.test.ts`. The roadmap Phase 0 milestone claims "TokenManager pass unit tests" but no TEST task in any phase creates TokenManager unit tests. The closest test (TEST-005) is an integration test for the refresh flow, not a unit test for the TokenManager class.
- **Source Quote**: `| TokenManager issues token pairs and rotates refresh tokens | tests/auth/token-manager.test.ts | FR-AUTH.3: Access/refresh pair generation; rotation invalidates old refresh token |` (spec Section 8.1, line 246)
- **Roadmap Quote**: Phase 0 milestone: `TokenManager pass unit tests` (roadmap line 95). No corresponding TEST task creates these tests. TEST-005: `Write integration tests for token refresh flow covering FR-AUTH.3a through FR-AUTH.3d` (roadmap Phase 2, line 177).
- **Impact**: The Phase 0 milestone is unverifiable — it asserts a test pass condition that no task delivers. TokenManager unit tests (testing token pair generation, rotation logic, replay detection, and hash storage in isolation) are distinct from integration tests and provide faster, more targeted regression coverage.
- **Recommended Correction**: Add a TEST task (e.g., TEST-013) in Phase 0 or Phase 1: "Write unit tests for TokenManager (pair issuance, rotation, replay detection, hash storage)" targeting `tests/auth/token-manager.test.ts`.

---

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: The spec's test plan (Section 8.1) lists two unit tests for the `AuthService` class: `AuthService.login` and `AuthService.register`, both in `tests/auth/auth-service.test.ts`. The roadmap has no unit test tasks for AuthService — only integration tests (TEST-003, TEST-004) that verify the same flows through the HTTP layer.
- **Source Quote**: `| AuthService.login returns tokens for valid credentials | tests/auth/auth-service.test.ts | FR-AUTH.1: Successful login flow; invalid credentials rejected |` and `| AuthService.register creates user with hashed password | tests/auth/auth-service.test.ts | FR-AUTH.2: Registration stores bcrypt hash; duplicate email rejected |` (spec Section 8.1, lines 247-248)
- **Roadmap Quote**: TEST-003: `Write integration tests for registration flow` (roadmap Phase 1, line 151). TEST-004: `Write integration tests for login flow` (roadmap Phase 1, line 152). No unit-level test tasks for AuthService exist.
- **Impact**: Related to DEV-002 — without an AuthService class, there is nothing to unit test. However, the spec explicitly requires unit tests that verify `AuthService.login` and `AuthService.register` in isolation (without HTTP transport). Integration tests alone leave the orchestrator logic untested at the unit level, reducing fault isolation during debugging.
- **Recommended Correction**: After resolving DEV-002, add a TEST task for AuthService unit tests: "Write unit tests for AuthService.login and AuthService.register in `tests/auth/auth-service.test.ts`."

---

### DEV-008
- **ID**: DEV-008
- **Severity**: LOW
- **Deviation**: The spec defines an `AuthTokenPair` TypeScript interface (Section 4.5) with `access_token` and `refresh_token` fields. The roadmap does not explicitly define or reference this interface as a named artifact.
- **Source Quote**: `interface AuthTokenPair { access_token: string; refresh_token: string; }` (spec Section 4.5, lines 199-202)
- **Roadmap Quote**: [MISSING] — The roadmap uses the concept implicitly (e.g., FR-AUTH.1a: "return 200 with access_token and refresh_token") but does not define `AuthTokenPair` as a formal interface or DTO.
- **Impact**: Minor. The roadmap's endpoint acceptance criteria specify the correct fields. The absence of a formal DTO definition could lead to inconsistent return shapes across endpoints, but this is a code-quality concern rather than a correctness issue.
- **Recommended Correction**: Optionally add `AuthTokenPair` interface definition to CONT-001 or CONT-002 contract tasks to ensure consistent typing across all token-returning endpoints.

---

### DEV-009
- **ID**: DEV-009
- **Severity**: LOW
- **Deviation**: The spec's implementation order (Section 4.6) places "routes + migrations" as step 5 (last), after `auth-service.ts`. The roadmap places database migrations (MIG-001, MIG-002) in Phase 0, before any service implementation tasks.
- **Source Quote**: `5. routes + migrations     -- depends on 3, 4` (spec Section 4.6, line 213)
- **Roadmap Quote**: Phase 0 tasks MIG-001 (#13) and MIG-002 (#14) appear in Phase 0 alongside service component creation, before Phase 1 endpoint work (roadmap lines 111-112).
- **Impact**: Negligible. The spec's ordering describes code-level dependencies (routes depend on auth-service). The roadmap pragmatically front-loads database migrations so that service code can immediately query the tables during development. The resulting execution sequence is sound — tables must exist before code that queries them can be tested.
- **Recommended Correction**: No action required. Document the rationale for the reordering if the spec is considered binding on execution sequence.

---

## Summary

**Severity Distribution**: 2 HIGH, 5 MEDIUM, 2 LOW (9 total deviations)

The roadmap demonstrates strong fidelity to the source specification across functional requirements (FR-AUTH.1 through FR-AUTH.5), non-functional requirements (NFR-AUTH.1 through NFR-AUTH.3), risk mitigations, open item coverage, and gap analysis resolution. Integration wiring is exceptionally well-documented through named artifacts (SecurityServiceContainer, AuthMiddlewareChain, AuthRouteRegistry).

The two HIGH severity deviations require resolution before tasklist generation:

1. **Missing `updated_at` field** (DEV-001): A specified data model field is absent from the roadmap's schema definition, which will produce an incomplete database table.
2. **Missing `AuthService` orchestrator** (DEV-002): The spec's central architectural component has no corresponding roadmap task. This collapses the layered architecture and makes spec-mandated unit tests (DEV-007) impossible to write.

The MEDIUM deviations (DEV-003 through DEV-007) reflect a pattern of the roadmap making reasonable design improvements (timestamps over booleans, integration tests over unit tests, pragmatic endpoint naming) that nevertheless diverge from the spec's explicit definitions. These should be reconciled — either by updating the spec to ratify the improvements, or by reverting the roadmap to match the spec.
