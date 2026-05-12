# Phase 1 -- Preparation & Template Study

Read all reference materials, confirm current state matches extraction assumptions, and freeze baseline for verification. All tasks in this phase are read-only; no files are modified. The baseline snapshot (T01.04) is critical for Phase 4 fidelity verification.

---

### T01.01 -- Read `commands/sc/adversarial.md` Gold-Standard Template

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | The adversarial.md command file (167 lines) defines the structural template that the TDD command must follow exactly. |
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
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0001/notes.md

**Deliverables:**
- Template analysis notes documenting section ordering, frontmatter fields, activation pattern, and boundaries format from `commands/sc/adversarial.md`

**Steps:**
1. **[PLANNING]** Identify `commands/sc/adversarial.md` as the gold-standard reference (canonical: `src/superclaude/commands/adversarial.md`)
2. **[PLANNING]** Confirm file accessibility and expected line count (~167 lines)
3. **[EXECUTION]** Read `commands/sc/adversarial.md` end-to-end
4. **[EXECUTION]** Record section ordering: Frontmatter, Required Input, Usage, Arguments, Options, Behavioral Summary, Examples, Activation, Boundaries, Related Commands
5. **[VERIFICATION]** Confirm all 10 sections identified and ordering noted
6. **[COMPLETION]** Record analysis notes in D-0001 artifact

**Acceptance Criteria:**
- File `.dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0001/notes.md` exists with section ordering from `adversarial.md`
- All 10 structural sections identified and documented
- Notes are derived solely from reading the file, not from memory or assumption
- Section ordering recorded matches the actual file structure

**Validation:**
- Manual check: notes list all 10 sections in the order they appear in `adversarial.md`
- Evidence: linkable artifact produced at D-0001/notes.md

**Dependencies:** None
**Rollback:** TBD
**Notes:** Read-only task. No files modified.

---

### T01.02 -- Read and Verify `skills/tdd/SKILL.md` Current State

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | Must confirm SKILL.md line count matches expected 438 and locate the exact migration blocks before any edits occur. |
| Effort | S |
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
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0002/notes.md

**Deliverables:**
- SKILL.md state verification notes confirming line count and migration block locations (lines 48-63, lines 82-88)

**Steps:**
1. **[PLANNING]** Identify canonical path: `src/superclaude/skills/tdd/SKILL.md`
2. **[PLANNING]** Define expected state: 438 lines, migration blocks at lines 48-63 and 82-88
3. **[EXECUTION]** Read `skills/tdd/SKILL.md` and run `wc -l`
4. **[EXECUTION]** Locate Effective Prompt Examples block (expected lines 48-63, ~16 lines) and Tier Selection table (expected lines 82-88, ~7 lines)
5. **[VERIFICATION]** Confirm line count and block locations match roadmap expectations
6. **[COMPLETION]** Record findings in D-0002 artifact; flag deviations if any

**Acceptance Criteria:**
- File `.dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0002/notes.md` exists with verified line count and block locations
- Line count recorded and compared against expected 438
- Migration blocks located; if at expected lines 48-63 and 82-88, content boundaries confirmed; if at different lines, actual locations recorded and deviation flagged
- Any deviations from expected state explicitly flagged

**Validation:**
- Manual check: `wc -l src/superclaude/skills/tdd/SKILL.md` output matches recorded line count
- Evidence: linkable artifact produced at D-0002/notes.md

**Dependencies:** None
**Rollback:** TBD
**Notes:** Read-only task. "Migration" in context refers to identifying text blocks for relocation, not database migration.

---

### T01.03 -- Read Developer Guide Sections 9.3, 9.7, and 5.10

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | Developer Guide Section 9.3 (separation of concerns), Section 9.7 (skill/command boundaries), and Section 5.10 (checklist) are the authoritative architectural rules governing this refactoring. |
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
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0003/notes.md

**Deliverables:**
- Reference notes from Developer Guide Section 9.3 (separation of concerns), Section 9.7 (skill/command boundaries), and Section 5.10 (command creation checklist)

**Steps:**
1. **[PLANNING]** Locate Developer Guide file in repository
2. **[PLANNING]** Identify Sections 9.3 and 5.10 within the document
3. **[EXECUTION]** Read Section 9.3 on separation of concerns between command and skill layers
4. **[EXECUTION]** Read Section 9.7 on skill/command layer boundaries
5. **[EXECUTION]** Read Section 5.10 on command creation checklist
6. **[VERIFICATION]** Confirm all three sections located and key rules extracted
6. **[COMPLETION]** Record reference notes in D-0003 artifact

**Acceptance Criteria:**
- File `.dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0003/notes.md` exists with key rules from all three sections
- Section 9.3 separation-of-concerns rules documented
- Section 9.7 skill/command boundary rules documented
- Section 5.10 checklist items documented

**Validation:**
- Manual check: notes reference specific rules from Sections 9.3 and 5.10
- Evidence: linkable artifact produced at D-0003/notes.md

**Dependencies:** None
**Rollback:** TBD
**Notes:** Read-only task. Developer Guide sections are authoritative architectural reference.

---

### T01.04 -- Snapshot Pre-Migration Baseline State

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | MANDATORY per roadmap: baseline measurements enable precise Phase 4 diff verification. Without this snapshot, fidelity verification cannot confirm zero collateral damage. |
| Effort | S |
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
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0004/evidence.md

**Deliverables:**
- Pre-migration baseline snapshot containing: `wc -l` output for SKILL.md, `git diff --stat` baseline, and verbatim copies of migration blocks (lines 48-63 and 82-88)

**Steps:**
1. **[PLANNING]** Identify all measurements needed: line count, git diff stat, migration block copies
2. **[PLANNING]** Confirm T01.02 findings are available for cross-reference
3. **[EXECUTION]** Run `wc -l src/superclaude/skills/tdd/SKILL.md` and record output
4. **[EXECUTION]** Run `git diff --stat` and record baseline; save verbatim copies of SKILL.md lines 48-63 (Effective Prompt Examples) and lines 82-88 (Tier Selection table)
5. **[VERIFICATION]** Confirm snapshot contains all three baseline measurements
6. **[COMPLETION]** Record complete snapshot in D-0004 artifact

**Acceptance Criteria:**
- File `.dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0004/evidence.md` exists with all three baseline measurements
- `wc -l` output recorded for SKILL.md
- Verbatim copies of lines 48-63 and lines 82-88 saved for Phase 4 diffing
- `git diff --stat` baseline recorded

**Validation:**
- Manual check: snapshot contains line count, git diff stat, and both migration block copies
- Evidence: linkable artifact produced at D-0004/evidence.md

**Dependencies:** T01.02
**Rollback:** TBD
**Notes:** MANDATORY task per roadmap. This snapshot is consumed by Phase 4 (T04.02 through T04.06) for fidelity verification.

---

### Checkpoint: End of Phase 1

**Purpose:** Confirm all reference materials are read and pre-migration baseline is frozen before any file modifications begin in Phase 2.
**Checkpoint Report Path:** .dev/releases/current/v3.66-tdd-skill-refactor-v2/checkpoints/CP-P01-END.md

**Verification:**
- All 4 tasks (T01.01-T01.04) completed with deliverable artifacts produced
- SKILL.md line count and migration block locations confirmed against roadmap expectations
- Pre-migration snapshot saved and reviewable for Phase 4 consumption

**Exit Criteria:**
- D-0001 through D-0004 artifacts exist at intended paths
- No files modified during this phase (read-only operations only)
- Any deviations from expected state flagged and recorded before proceeding
