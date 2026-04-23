# Phase 1 -- Foundation, Data Layer, Key Management

**Goal:** Provision the persistence layer, entity models, repositories, cryptographic key material, and feature-flag plumbing that every later milestone depends on. Migrations apply and roll back cleanly in CI; RSA keypair stored in secrets manager; feature flag wired.

### T01.01 -- AuthTablesMigration orchestrator

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | Migration module orchestrating users + refresh_tokens table creation with reversible down (COMP-007). |
| Effort | M |
| Risk | High |
| Risk Drivers | migration, schema, data |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0001/spec.md`
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md`

**Deliverables:**
- `database/migrations/003-auth-tables.ts` orchestrator with up/down

**Steps:**
1. **[PLANNING]** Load roadmap COMP-007 spec
2. **[PLANNING]** Confirm MIG-001/002/003 ordering
3. **[EXECUTION]** Author forward migration that creates both tables
4. **[EXECUTION]** Author down migration that drops in reverse order
5. **[VERIFICATION]** Run CI up→down→up cycle (TEST-M1-003)
6. **[COMPLETION]** Record evidence path under `TASKLIST_ROOT/evidence/`

**Acceptance Criteria:**
- File `database/migrations/003-auth-tables.ts` contains up/down for both tables
- up creates both tables; down drops in reverse order
- Idempotent on rerun (verified by CI)
- Evidence artifact `D-0001/evidence.md` exists

**Validation:**
- Manual check: CI job proves up→down→up green
- Evidence: linkable artifact produced

**Dependencies:** None
**Rollback:** Down migration reverses table creation
**Notes:** Critical path override applied (migrations).

### T01.02 -- users table migration (MIG-001)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | Forward/backward migration creating users table with unique email index. |
| Effort | S |
| Risk | High |
| Risk Drivers | migration, schema |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0002/spec.md`
- `TASKLIST_ROOT/artifacts/D-0002/evidence.md`

**Deliverables:**
- users table forward + backward migration script

**Steps:**
1. **[PLANNING]** Read roadmap MIG-001 column list
2. **[PLANNING]** Verify FK target for refresh_tokens
3. **[EXECUTION]** Implement forward migration
4. **[EXECUTION]** Implement down migration
5. **[VERIFICATION]** Apply on test DB; assert columns + unique constraint
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Columns id:UUID-PK, email:unique-idx, display_name, password_hash, is_locked, created_at, updated_at exist
- email unique constraint enforced at DB level
- Down migration drops the table cleanly
- Evidence file `D-0002/evidence.md` recorded

**Validation:**
- Manual check: schema matches MIG-001 spec
- Evidence: linkable artifact produced

**Dependencies:** None
**Rollback:** Down script
**Notes:** -

### T01.03 -- refresh_tokens table migration (MIG-002)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | Forward/backward migration creating refresh_tokens with FK and indexes. |
| Effort | S |
| Risk | High |
| Risk Drivers | migration, schema, auth |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0003/spec.md`
- `TASKLIST_ROOT/artifacts/D-0003/evidence.md`

**Deliverables:**
- refresh_tokens migration with FK to users + idx(user_id) + idx(token_hash)

**Steps:**
1. **[PLANNING]** Read MIG-002 column list
2. **[PLANNING]** Confirm FK constraint target
3. **[EXECUTION]** Implement forward migration
4. **[EXECUTION]** Implement down migration
5. **[VERIFICATION]** Apply on test DB; verify indexes
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Columns id:UUID-PK, user_id:FK→users.id, token_hash, expires_at, revoked, created_at exist
- idx(user_id) and idx(token_hash) created
- Down migration drops cleanly
- Evidence file `D-0003/evidence.md` recorded

**Validation:**
- Manual check: schema matches MIG-002 spec
- Evidence: linkable artifact produced

**Dependencies:** T01.02
**Rollback:** Down script
**Notes:** -

### T01.04 -- UserRepository (COMP-008)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | Persistence-layer abstraction for UserRecord CRUD. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | auth |
| Tier | STRICT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0004/spec.md`
- `TASKLIST_ROOT/artifacts/D-0004/evidence.md`

**Deliverables:**
- `src/auth/repositories/user-repository.ts` with full CRUD

**Steps:**
1. **[PLANNING]** Load IUserRepository contract from roadmap
2. **[PLANNING]** Identify negative paths
3. **[EXECUTION]** Implement findByEmail / findById / create / updatePasswordHash / setLocked
4. **[EXECUTION]** Add updatedAt auto-bump on write
5. **[VERIFICATION]** Run tests/auth coverage with branch coverage = 100%
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Methods findByEmail, findById, create, updatePasswordHash, setLocked all return per spec
- 100% branch coverage including not-found and dup-email negative paths
- updatedAt auto-bumps on write (verified by test)
- Evidence file `D-0004/evidence.md` recorded

**Validation:**
- Manual check: TEST-M1-001 passes
- Evidence: linkable artifact produced

**Dependencies:** T01.02
**Rollback:** Revert PR
**Notes:** -

### T01.05 -- INFRA-001 RSA key pair generation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | Tooling to generate RS256-compatible RSA key pair (2048-bit min) for JWT signing. |
| Effort | S |
| Risk | High |
| Risk Drivers | security, credentials, secrets |
| Tier | STRICT |
| Confidence | [████████--] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0005/spec.md`
- `TASKLIST_ROOT/artifacts/D-0005/evidence.md`

**Deliverables:**
- `infra/scripts/gen-keys` script + 2048-bit RSA private/public PEM files

**Steps:**
1. **[PLANNING]** Resolve OI-9 rotation strategy (dual-key vs cutover)
2. **[PLANNING]** Confirm secrets-manager PEM format
3. **[EXECUTION]** Implement keygen script enforcing 2048-bit minimum
4. **[EXECUTION]** Wire output to secrets-manager-friendly format
5. **[VERIFICATION]** Generate, inspect, and validate keypair
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Script `infra/scripts/gen-keys` enforces 2048-bit RSA minimum (rejects weaker)
- Private and public PEM files produced
- Public key embeddable in JWKS endpoint
- Evidence file `D-0005/evidence.md` recorded

**Validation:**
- Manual check: keygen output validated by openssl rsa -text
- Evidence: linkable artifact produced

**Dependencies:** None
**Rollback:** Discard keypair, regenerate
**Notes:** Critical path override (crypto/security).

### T01.06 -- Checkpoint: M1 Foundation Verified

**Purpose:** Verify M1 foundation deliverables (migrations, repositories, key material) before proceeding to M2 primitives.
**Checkpoint Report Path:** `checkpoints/CP-P01-END.md`

**Verification:**
- TEST-M1-001 (UserRepository unit tests) green
- TEST-M1-003 (migration up→down→up cycle) green in CI
- INFRA-001 keygen produces ≥2048-bit keys

**Exit Criteria:**
- All migrations reversible in CI
- RSA keypair stored in secrets manager (or local PEM during dev)
- Feature flag CFG-002 wired (off in M1)
