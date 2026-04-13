# Phase 4 -- Fidelity Verification

Verify migration correctness with zero collateral damage. This phase is a **hard gate** -- if any check fails, do not proceed to Phase 5. All 6 tasks are read-only verification operations. The 26 verification checks across tasks are independent and can be batched into parallel invocations.

---

### T04.01 -- Verify Migrated Content Presence in Command File

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | FR-TDD-CMD.3a/3b/3c: must confirm all migrated content (3 strong examples, 2 weak examples, 3 tier rows) is present in the command file with correct structure. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0013/evidence.md

**Deliverables:**
- Grep evidence confirming presence of all migrated content in `src/superclaude/commands/tdd.md`: 3 strong example distinctive strings, 2 weak example distinctive strings, `Lightweight`/`Standard`/`Heavyweight` tier rows with all 5 columns

**Steps:**
1. **[PLANNING]** Load D-0004 baseline to identify distinctive strings from migrated blocks
2. **[PLANNING]** Define 8+ grep targets: 3 strong example strings, 2 weak example strings, 3 tier row identifiers
3. **[EXECUTION]** Grep `src/superclaude/commands/tdd.md` for each of the 3 strong example distinctive strings
4. **[EXECUTION]** Grep for 2 weak example distinctive strings and for `Lightweight`, `Standard`, `Heavyweight` tier rows with column content
5. **[VERIFICATION]** Confirm all 8+ grep searches return matches
6. **[COMPLETION]** Record evidence in D-0013 artifact

**Acceptance Criteria:**
- Grep for 3 strong example distinctive strings in `src/superclaude/commands/tdd.md` returns matches for all 3
- Grep for 2 weak example distinctive strings returns matches for both
- Grep for `Lightweight`, `Standard`, `Heavyweight` returns matches with 5-column structure
- All 8+ checks pass (zero misses)

**Validation:**
- Manual check: all grep commands return non-empty results
- Evidence: linkable artifact produced at D-0013/evidence.md

**Dependencies:** T03.01, T03.02, T03.05
**Rollback:** TBD
**Notes:** Read-only verification. FR-TDD-CMD.3a/3b/3c coverage. Can run in parallel with T04.02-T04.06.

---

### T04.02 -- Verify Behavioral Protocol Sections Untouched in SKILL.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | FR-TDD-CMD.3d and NFR-TDD-CMD.5: the behavioral protocol (Stage A, Stage B, critical rules, session management) must have zero changes to guarantee no behavioral regression. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0014/evidence.md

**Deliverables:**
- Section-level diff evidence comparing SKILL.md Stage A, Stage B, critical rules, and session management sections pre/post migration (expected: zero changes in all 4 sections)

**Steps:**
1. **[PLANNING]** Load D-0004 baseline snapshot with pre-migration SKILL.md content
2. **[PLANNING]** Identify section boundaries for: Stage A, Stage B, critical rules, session management
3. **[EXECUTION]** Diff SKILL.md Stage A section against D-0004 baseline -- expect zero changes
4. **[EXECUTION]** Diff Stage B, critical rules, and session management sections against baseline -- expect zero changes for each
5. **[VERIFICATION]** Confirm all 4 section diffs return empty (zero changes)
6. **[COMPLETION]** Record diff evidence in D-0014 artifact

**Acceptance Criteria:**
- Diff of SKILL.md Stage A section pre/post migration returns empty
- Diff of Stage B section returns empty
- Diff of critical rules section returns empty
- Diff of session management section returns empty

**Validation:**
- Manual check: all 4 section-level diffs show zero changes
- Evidence: linkable artifact produced at D-0014/evidence.md

**Dependencies:** T03.03 (content removed from SKILL.md), T01.04 (baseline snapshot)
**Rollback:** TBD
**Notes:** Read-only verification. FR-TDD-CMD.3d, NFR-TDD-CMD.5 coverage. Hard gate: failure blocks Phase 5.

---

### T04.03 -- Verify Loading Declarations Untouched in SKILL.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | FR-TDD-CMD.3e: the Phase Loading Contract table must be identical pre/post migration. Any change would alter skill loading behavior. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0015/evidence.md

**Deliverables:**
- Diff evidence comparing SKILL.md Phase Loading Contract table pre/post migration (expected: zero changes)

**Steps:**
1. **[PLANNING]** Load D-0004 baseline snapshot with pre-migration Phase Loading Contract table
2. **[PLANNING]** Locate Phase Loading Contract table in current SKILL.md
3. **[EXECUTION]** Diff the Phase Loading Contract table section against D-0004 baseline
4. **[EXECUTION]** Record diff output (expected: empty)
5. **[VERIFICATION]** Confirm diff returns empty (zero changes)
6. **[COMPLETION]** Record evidence in D-0015 artifact

**Acceptance Criteria:**
- Diff of Phase Loading Contract table pre/post migration returns empty
- Table structure, row count, and cell content identical to baseline
- No adjacent content inadvertently modified
- Pass/fail result documented

**Validation:**
- Manual check: section diff shows zero changes to Phase Loading Contract table
- Evidence: linkable artifact produced at D-0015/evidence.md

**Dependencies:** T03.03, T01.04
**Rollback:** TBD
**Notes:** Read-only verification. FR-TDD-CMD.3e coverage.

---

### T04.04 -- Verify All 5 Refs Files Untouched

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | FR-TDD-CMD.3f: all 5 refs/ files must be completely unmodified. Any change would indicate scope creep beyond the command-layer refactoring. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0016/evidence.md

**Deliverables:**
- Git diff evidence showing all 5 refs/ files return empty diffs: `refs/build-request-template.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md`

**Steps:**
1. **[PLANNING]** List all 5 refs/ files to verify
2. **[PLANNING]** Define pass criteria: `git diff` returns empty for each file
3. **[EXECUTION]** Run `git diff` on `refs/build-request-template.md` and `refs/agent-prompts.md`
4. **[EXECUTION]** Run `git diff` on `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, and `refs/operational-guidance.md`
5. **[VERIFICATION]** Confirm all 5 git diffs return empty
6. **[COMPLETION]** Record evidence in D-0016 artifact

**Acceptance Criteria:**
- `git diff` on `refs/build-request-template.md` returns empty
- `git diff` on `refs/agent-prompts.md` returns empty
- `git diff` on `refs/synthesis-mapping.md` returns empty
- `git diff` on `refs/validation-checklists.md` returns empty
- `git diff` on `refs/operational-guidance.md` returns empty

**Validation:**
- Manual check: `git diff` on all 5 refs/ files returns empty output
- Evidence: linkable artifact produced at D-0016/evidence.md

**Dependencies:** T03.03
**Rollback:** TBD
**Notes:** Read-only verification. FR-TDD-CMD.3f coverage. All 5 checks are independent and can run in parallel.

---

### T04.05 -- Verify Activation Correctness in Command File

| Field | Value |
|---|---|
| Roadmap Item IDs | R-017 |
| Why | NFR-TDD-CMD.4: the Activation section must contain `Skill tdd` to correctly wire the command to the skill at runtime. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0017/evidence.md

**Deliverables:**
- Grep evidence confirming `Skill tdd` present in `src/superclaude/commands/tdd.md` Activation section

**Steps:**
1. **[PLANNING]** Define search target: `Skill tdd` within the Activation section of the command file
2. **[PLANNING]** Confirm T02.01 command file exists
3. **[EXECUTION]** Grep `src/superclaude/commands/tdd.md` for `Skill tdd`
4. **[EXECUTION]** Verify match is within the `## Activation` section context
5. **[VERIFICATION]** Confirm grep returns at least 1 match in the correct section
6. **[COMPLETION]** Record evidence in D-0017 artifact

**Acceptance Criteria:**
- Grep for `Skill tdd` in `src/superclaude/commands/tdd.md` returns at least 1 match
- Match located within the `## Activation` section of the command file
- "Do NOT proceed" guard text present near the activation directive
- Activation wiring consistent with adversarial.md gold-standard pattern

**Validation:**
- Manual check: grep output confirms `Skill tdd` in Activation section
- Evidence: linkable artifact produced at D-0017/evidence.md

**Dependencies:** T02.01
**Rollback:** TBD
**Notes:** Read-only verification. NFR-TDD-CMD.4, SC-4 coverage.

---

### Checkpoint: Phase 4 / Tasks 1-5

**Purpose:** Interim verification gate covering migrated content presence, behavioral protocol integrity, loading declarations, refs/ files, and activation correctness.
**Checkpoint Report Path:** .dev/releases/current/v3.66-tdd-skill-refactor-v2/checkpoints/CP-P04-T01-T05.md

**Verification:**
- All migrated content (examples + tier table) confirmed present in command file (T04.01)
- Behavioral protocol sections (Stage A, B, critical rules, session mgmt) zero-diff confirmed (T04.02)
- All 5 refs/ files confirmed unmodified (T04.04)

**Exit Criteria:**
- T04.01 through T04.05 all pass with evidence artifacts produced
- Zero collateral damage detected so far
- Activation wiring confirmed correct (T04.05)

---

### T04.06 -- Verify Migrated Content Removed from SKILL.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-018 |
| Why | SC-8: migrated content must not remain in SKILL.md after removal. Lingering content would create duplication and violate the single-source-of-truth principle. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0018 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0018/evidence.md

**Deliverables:**
- Grep evidence confirming distinctive migrated strings are absent from `src/superclaude/skills/tdd/SKILL.md` (0 matches for each)

**Steps:**
1. **[PLANNING]** Load distinctive strings from D-0004 baseline migration blocks
2. **[PLANNING]** Define pass criteria: 0 matches in SKILL.md for each distinctive string
3. **[EXECUTION]** Grep `src/superclaude/skills/tdd/SKILL.md` for distinctive strings from Effective Prompt Examples block
4. **[EXECUTION]** Grep for distinctive strings from Tier Selection table rows
5. **[VERIFICATION]** Confirm all grep searches return 0 matches
6. **[COMPLETION]** Record evidence in D-0018 artifact

**Acceptance Criteria:**
- Grep for strong example distinctive strings in `src/superclaude/skills/tdd/SKILL.md` returns 0 matches
- Grep for weak example distinctive strings returns 0 matches
- Grep for tier row identifiers (`Lightweight`, `Standard`, `Heavyweight` in table context) returns 0 matches
- All migrated content confirmed absent from SKILL.md

**Validation:**
- Manual check: all grep commands return empty results
- Evidence: linkable artifact produced at D-0018/evidence.md

**Dependencies:** T03.03
**Rollback:** TBD
**Notes:** Read-only verification. SC-8 coverage. Complements T04.01 (presence check) to form the complete migration integrity proof.

---

### Checkpoint: End of Phase 4

**Purpose:** Hard gate confirming all 26 verification checks pass with zero collateral damage. Phase 5 is blocked until this checkpoint clears.
**Checkpoint Report Path:** .dev/releases/current/v3.66-tdd-skill-refactor-v2/checkpoints/CP-P04-END.md

**Verification:**
- All 6 tasks (T04.01-T04.06) pass with evidence artifacts produced
- Zero collateral damage: behavioral protocol, loading declarations, and refs/ files all unmodified
- Migration integrity confirmed: content present in command, absent from SKILL.md

**Exit Criteria:**
- D-0013 through D-0018 artifacts exist at intended paths
- All 26 individual verification checks documented as passing
- No failures detected; if any failure found, Phase 5 is blocked until fixed
