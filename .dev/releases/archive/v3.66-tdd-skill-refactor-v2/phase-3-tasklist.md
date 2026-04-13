# Phase 3 -- Content Migration

Migrate ~23 lines of interface-concern content from `skills/tdd/SKILL.md` to the command file created in Phase 2, then remove the migrated content from SKILL.md. Two migration blocks: Effective Prompt Examples (lines 48-63) and Tier Selection table (lines 82-88).

---

### T03.01 -- Migrate Prompt Examples from SKILL.md to Command File

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | FR-TDD-CMD.2a: prompt examples are interface concerns (how users invoke the command) and belong in the command layer, not the skill protocol. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | migration/data keywords (markdown text relocation) |
| Tier | STRICT |
| Confidence | [████------] 42% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0008/spec.md

**Deliverables:**
- Prompt examples (3 strong + 2 weak, ~16 lines from SKILL.md lines 48-63) copied into the command file's Examples section, adapted to `/sc:tdd` invocation syntax

**Steps:**
1. **[PLANNING]** Load D-0004 baseline snapshot to confirm migration block at SKILL.md lines 48-63
2. **[PLANNING]** Confirm T02.01 command file exists with Examples section ready to receive content
3. **[EXECUTION]** Read SKILL.md lines 48-63 (Effective Prompt Examples block, ~16 lines containing 3 strong + 2 weak examples)
4. **[EXECUTION]** Copy content into command file Examples section; adapt invocation syntax to prefix with `/sc:tdd` per FR-TDD-CMD.2a
5. **[VERIFICATION]** Grep command file for distinctive strings from each of the 5 examples to confirm presence
6. **[COMPLETION]** Record migration evidence in D-0008 artifact

**Acceptance Criteria:**
- All 3 strong example distinctive strings found in `src/superclaude/commands/tdd.md` Examples section
- All 2 weak example distinctive strings found in `src/superclaude/commands/tdd.md` Examples section
- Examples adapted to use `/sc:tdd` command invocation syntax
- Content derived from SKILL.md lines 48-63 baseline snapshot (D-0004)

**Validation:**
- Manual check: grep `src/superclaude/commands/tdd.md` for distinctive strings from each of the 5 examples returns matches
- Evidence: linkable artifact produced at D-0008/spec.md

**Dependencies:** T02.01 (command file exists), T01.04 (baseline snapshot)
**Rollback:** Revert command file Examples section to Phase 2 state
**Notes:** Tier conflict: [STRICT vs EXEMPT] -> resolved to STRICT by priority rule. Context: markdown text relocation between .md files, not database migration. Confidence low due to "migrate" keyword triggering STRICT while *.md path pushes EXEMPT.

---

### T03.02 -- Migrate Tier Selection Table from SKILL.md to Command File

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | FR-TDD-CMD.2b: the tier comparison table is reference material for users selecting a tier, which is an interface concern belonging in the command's Options section. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | migration/data keywords (markdown text relocation) |
| Tier | STRICT |
| Confidence | [████------] 42% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0009/spec.md

**Deliverables:**
- Tier selection table (header + 3 data rows: Lightweight, Standard, Heavyweight, ~7 lines from SKILL.md lines 82-88) copied into the command file's Options section as `--tier` reference material

**Steps:**
1. **[PLANNING]** Load D-0004 baseline snapshot to confirm migration block at SKILL.md lines 82-88
2. **[PLANNING]** Confirm T02.01 command file exists with Options section containing `--tier` row
3. **[EXECUTION]** Read SKILL.md lines 82-88 (Tier Selection table with header + 3 data rows: Lightweight, Standard, Heavyweight)
4. **[EXECUTION]** Copy table into command file Options section as `--tier` reference material per FR-TDD-CMD.2b
5. **[VERIFICATION]** Grep command file for `Lightweight`, `Standard`, `Heavyweight` tier row content with all 5 columns
6. **[COMPLETION]** Record migration evidence in D-0009 artifact

**Acceptance Criteria:**
- Grep `src/superclaude/commands/tdd.md` for `Lightweight` tier row returns match with all 5 columns
- Grep for `Standard` tier row returns match with all 5 columns
- Grep for `Heavyweight` tier row returns match with all 5 columns
- Table header row present in command Options section

**Validation:**
- Manual check: grep command file for each of the 3 tier names returns matches within a table structure
- Evidence: linkable artifact produced at D-0009/spec.md

**Dependencies:** T02.01 (command file exists), T01.04 (baseline snapshot)
**Rollback:** Revert command file Options section to Phase 2 state
**Notes:** Tier conflict: [STRICT vs EXEMPT] -> resolved to STRICT by priority rule. Same context as T03.01: markdown text relocation, not database migration.

---

### T03.03 -- Remove Migrated Content from SKILL.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | FR-TDD-CMD.2c/2d/2e: after migration, the source content must be removed from SKILL.md to prevent duplication. Retention rules: keep 4-input description (lines 34-46), keep incomplete-prompt template (lines 65-76), keep tier selection rules (lines 90-94). |
| Effort | M |
| Risk | Medium |
| Risk Drivers | migration/data keywords (content removal with retention rules) |
| Tier | EXEMPT |
| Confidence | [█████-----] 50% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0010/evidence.md

**Deliverables:**
- Modified `src/superclaude/skills/tdd/SKILL.md` with Effective Prompt Examples block (lines 48-63) removed and tier table rows (lines 82-88) removed, while retaining: 4-input description (lines 34-46), incomplete-prompt template (lines 65-76), tier selection introductory sentence + rules (lines 90-94)

**Steps:**
1. **[PLANNING]** Load D-0004 baseline snapshot to confirm exact line ranges for removal
2. **[PLANNING]** Identify retention boundaries: lines 34-46 (4-input description), lines 65-76 (incomplete-prompt template), lines 90-94 (tier selection rules)
3. **[EXECUTION]** Remove Effective Prompt Examples block (SKILL.md lines 48-63, ~16 lines) per FR-TDD-CMD.2e
4. **[EXECUTION]** Remove tier table rows (lines 82-88, ~7 lines), retain introductory sentence + selection rules (lines 90-94) per FR-TDD-CMD.2d
5. **[VERIFICATION]** Confirm retained content (lines 34-46, 65-76, 90-94) is intact and unmodified
6. **[COMPLETION]** Record removal evidence in D-0010 artifact

**Acceptance Criteria:**
- SKILL.md lines 48-63 (Effective Prompt Examples) no longer present in `src/superclaude/skills/tdd/SKILL.md`
- SKILL.md tier table rows (lines 82-88) no longer present
- 4-input description (originally lines 34-46) retained and unmodified
- Incomplete-prompt template (originally lines 65-76) retained and unmodified
- Tier selection introductory sentence + rules (originally lines 90-94) retained and unmodified

**Validation:**
- Manual check: grep SKILL.md for distinctive strings from removed blocks returns 0 matches; grep for retained content returns matches
- Evidence: linkable artifact produced at D-0010/evidence.md

**Dependencies:** T03.01 (examples migrated to command), T03.02 (tier table migrated to command)
**Rollback:** Restore SKILL.md from git: `git checkout -- src/superclaude/skills/tdd/SKILL.md`
**Notes:** Edit operation on SKILL.md. Algorithm classified EXEMPT due to *.md path booster overriding "remove" STANDARD keyword. FR-TDD-CMD.2c/2d/2e coverage.

---

### T03.04 -- Verify SKILL.md Post-Migration Line Count (400-440)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | NFR-TDD-CMD.3 and FR-TDD-CMD.2f mandate the post-migration SKILL.md stays within 400-440 lines, confirming approximately ~23 lines were removed and no unintended content was affected. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0011/evidence.md

**Deliverables:**
- Post-migration line count verification showing `wc -l src/superclaude/skills/tdd/SKILL.md` in range [400, 440]

**Steps:**
1. **[PLANNING]** Confirm T03.03 completed (content removed from SKILL.md)
2. **[PLANNING]** Load D-0004 baseline line count for comparison
3. **[EXECUTION]** Run `wc -l src/superclaude/skills/tdd/SKILL.md`
4. **[EXECUTION]** Compare against [400, 440] range and against baseline (expected delta: ~23 lines removed)
5. **[VERIFICATION]** Record pass/fail with actual count and delta from baseline
6. **[COMPLETION]** Record evidence in D-0011 artifact

**Acceptance Criteria:**
- `wc -l src/superclaude/skills/tdd/SKILL.md` returns a value between 400 and 440 inclusive
- Delta from baseline line count is approximately 23 lines (within tolerance)
- Actual line count and delta recorded in evidence
- If fail: deviation amount noted for corrective action

**Validation:**
- Manual check: `wc -l src/superclaude/skills/tdd/SKILL.md` output verified against [400, 440]
- Evidence: linkable artifact produced at D-0011/evidence.md

**Dependencies:** T03.03
**Rollback:** TBD
**Notes:** Read-only verification task. NFR-TDD-CMD.3, FR-TDD-CMD.2f coverage.

---

### T03.05 -- Verify No Duplication Across Command and SKILL.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | FR-TDD-CMD.2e requires each migrated string to appear in exactly one file. Duplication would violate the single-source-of-truth principle. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0012/evidence.md

**Deliverables:**
- No-duplication verification evidence showing each distinctive migrated string appears in exactly one of: `src/superclaude/commands/tdd.md` (present) or `src/superclaude/skills/tdd/SKILL.md` (absent)

**Steps:**
1. **[PLANNING]** Identify distinctive strings from each migrated block (3 strong examples, 2 weak examples, 3 tier rows)
2. **[PLANNING]** Define pass criteria: each string found in command file AND absent from SKILL.md
3. **[EXECUTION]** Grep `src/superclaude/commands/tdd.md` for each distinctive string (expect matches)
4. **[EXECUTION]** Grep `src/superclaude/skills/tdd/SKILL.md` for same strings (expect 0 matches)
5. **[VERIFICATION]** Confirm no string appears in both files simultaneously
6. **[COMPLETION]** Record evidence in D-0012 artifact

**Acceptance Criteria:**
- Each distinctive migrated string found in `src/superclaude/commands/tdd.md`
- Each distinctive migrated string absent from `src/superclaude/skills/tdd/SKILL.md`
- Zero strings appear in both files simultaneously
- All 8+ distinctive strings tested (3 strong examples + 2 weak examples + 3 tier rows)

**Validation:**
- Manual check: cross-file grep for migrated strings confirms single-file presence
- Evidence: linkable artifact produced at D-0012/evidence.md

**Dependencies:** T03.01, T03.02, T03.03
**Rollback:** TBD
**Notes:** Read-only verification task. FR-TDD-CMD.2e coverage. This is the final Phase 3 gate.

---

### Checkpoint: End of Phase 3

**Purpose:** Confirm content migration complete: all examples and tier table in command file, migrated content removed from SKILL.md, no duplication, and SKILL.md within line budget.
**Checkpoint Report Path:** .dev/releases/current/v3.66-tdd-skill-refactor-v2/checkpoints/CP-P03-END.md

**Verification:**
- 5 prompt examples and tier table present in command file (T03.01, T03.02)
- Migrated content removed from SKILL.md (T03.03)
- SKILL.md line count within [400, 440] range (T03.04)

**Exit Criteria:**
- D-0008 through D-0012 artifacts exist at intended paths
- Zero duplication detected across command and SKILL.md (T03.05)
- Migration blocks relocated cleanly; retained content (4-input description, incomplete-prompt template, tier selection rules) confirmed intact
