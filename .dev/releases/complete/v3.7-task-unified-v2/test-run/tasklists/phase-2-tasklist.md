# Phase 2 -- Core Authentication Primitives

**Goal:** Implement PasswordHasher, JwtService, and TokenManager as independently testable primitives that the AuthService orchestrator will compose in Phase 3. bcrypt cost=12 benchmarked; RS256 sign/verify round-trip passes with dual-key; refresh rotation with replay detection proven.

### T02.01 -- PasswordHasher with bcrypt cost=12 (COMP-004)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-018 |
| Why | bcrypt wrapper exposing hash and compare with configurable cost factor. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, credentials, password |
| Tier | STRICT |
| Confidence | [████████--] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0006/spec.md`
- `TASKLIST_ROOT/artifacts/D-0006/evidence.md`

**Deliverables:**
- `src/auth/password-hasher.ts` with hash + compare + cost enforcement

**Steps:**
1. **[PLANNING]** Read CRYPTO-003 cost-factor enforcement spec
2. **[PLANNING]** Identify config-loader integration
3. **[EXECUTION]** Implement hash(plain) → bcrypt-hash
4. **[EXECUTION]** Implement compare(plain, hash) → bool with constant-time failure
5. **[VERIFICATION]** Run TEST-M2-001 + benchmark
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Function `hash` returns bcrypt string with cost=12 prefix
- Startup rejects cost<12 when NODE_ENV=production
- Benchmark p95 within 200-350ms band on CI hardware
- Evidence file `D-0006/evidence.md` recorded

**Validation:**
- Manual check: bcrypt hash output prefix `$2b$12$`
- Evidence: linkable artifact produced

**Dependencies:** T01.05
**Rollback:** Revert PR
**Notes:** -

### T02.02 -- JwtService RS256 with dual-key verification (COMP-003)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-019 |
| Why | RS256 sign and verify wrapper supporting multi-key verification during rotation. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, token, encryption |
| Tier | STRICT |
| Confidence | [████████--] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0007/spec.md`
- `TASKLIST_ROOT/artifacts/D-0007/evidence.md`

**Deliverables:**
- `src/auth/jwt-service.ts` with RS256 sign/verify and multi-kid support

**Steps:**
1. **[PLANNING]** Read CRYPTO-001 algorithm whitelist requirement
2. **[PLANNING]** Confirm INFRA-002 secret retrieval contract
3. **[EXECUTION]** Implement sign with kid header
4. **[EXECUTION]** Implement verify supporting kid n and n+1
5. **[VERIFICATION]** Run TEST-M2-002 + TEST-M2-003 (dual-key)
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Algorithm whitelist rejects alg=none and alg=HS256
- Sign emits JWT with kid header
- Verify accepts both kid n and kid n+1 during grace window
- Evidence file `D-0007/evidence.md` recorded

**Validation:**
- Manual check: TEST-M2-002 round-trip green; 4 negative paths proven
- Evidence: linkable artifact produced

**Dependencies:** T01.05
**Rollback:** Revert PR
**Notes:** -

### T02.03 -- TokenManager with refresh rotation + replay detection (COMP-002)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-020 |
| Why | Issues, rotates, and revokes AuthTokenPair with refresh-token replay detection. |
| Effort | L |
| Risk | High |
| Risk Drivers | security, token, auth |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0008/spec.md`
- `TASKLIST_ROOT/artifacts/D-0008/evidence.md`

**Deliverables:**
- `src/auth/token-manager.ts` with issue/refresh/detectReplay

**Steps:**
1. **[PLANNING]** Read REPLAY-001 detection algorithm
2. **[PLANNING]** Identify SHA-256 hash storage approach
3. **[EXECUTION]** Implement issue(userId) → AuthTokenPair
4. **[EXECUTION]** Implement refresh + detectReplay → revokeAllForUser
5. **[VERIFICATION]** Run TEST-M2-005 (replay-detection)
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Refresh rotation produces new pair, marks previous revoked
- Reusing a revoked refresh token revokes all user tokens (replay detection)
- TTLs: access=15min, refresh=7d
- Evidence file `D-0008/evidence.md` recorded

**Validation:**
- Manual check: TEST-M2-004 + TEST-M2-005 green
- Evidence: linkable artifact produced

**Dependencies:** T02.02
**Rollback:** Revert PR
**Notes:** -

### T02.04 -- Password policy + email validators (VALID-001/002)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-021 |
| Why | Pure utilities enforcing 8+ chars, upper/lower/digit + RFC-5322 email format. |
| Effort | S |
| Risk | Low |
| Risk Drivers | password |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0009/spec.md`
- `TASKLIST_ROOT/artifacts/D-0009/evidence.md`

**Deliverables:**
- `src/auth/validators/password-policy.ts` and `src/auth/validators/email.ts`

**Steps:**
1. **[PLANNING]** Read VALID-001/002 acceptance criteria
2. **[PLANNING]** Identify failure-mode enumeration
3. **[EXECUTION]** Implement password-policy validator
4. **[EXECUTION]** Implement email validator
5. **[VERIFICATION]** Run TEST-M2-006 truth tables
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Tests in TEST-M2-006 enumerate all four password failure modes and pass
- Email validator accepts unicode local-part edge cases
- Validators are pure (no IO)
- Evidence file `D-0009/evidence.md` recorded

**Validation:**
- Manual check: pytest validators run green
- Evidence: linkable artifact produced

**Dependencies:** None
**Rollback:** Revert PR
**Notes:** -

### T02.05 -- Checkpoint: M2 Primitives Verified

**Purpose:** Verify all M2 primitives (PasswordHasher, JwtService, TokenManager, validators) are independently testable and pass their unit suites.
**Checkpoint Report Path:** `checkpoints/CP-P02-END.md`

**Verification:**
- TEST-M2-001 (PasswordHasher cost + benchmark) green
- TEST-M2-002 + TEST-M2-003 (JWT round-trip + dual-key) green
- TEST-M2-005 (replay detection) green

**Exit Criteria:**
- bcrypt cost=12 benchmarked within 200-350ms band
- RS256 sign/verify round-trip with dual-key verified
- TokenManager replay-detection revokes all user tokens
