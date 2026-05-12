# Phase 4 -- SKILL.md Reduction & Phase Loading Declarations

Reduce SKILL.md to under 500 lines by removing migrated HOW content and adding explicit refs-loading declarations. The result is a behavioral protocol with phase-aware loading directives. All behavioral blocks (B01-B11, B13, B14) remain unchanged.

---

### T04.01 -- Remove Migrated Content Blocks from SKILL.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-024 |
| Why | Migrated HOW content (BUILD_REQUEST, agent prompts, synthesis mapping, validation checklists, operational guidance) must be removed from SKILL.md to achieve the <500 line target. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0017/evidence.md`

**Deliverables:**
1. Reduced `src/superclaude/skills/tdd/SKILL.md` with all 5 migrated content blocks removed

**Steps:**
1. **[PLANNING]** Load corrected fidelity index (D-0007) to identify exact line ranges for removal
2. **[PLANNING]** Confirm all 5 content blocks already exist in refs files (Phase 2 gate passed)
3. **[EXECUTION]** Remove Block B12 (BUILD_REQUEST template, ~lines 341-492) from SKILL.md
4. **[EXECUTION]** Remove Blocks B15-B22 (agent prompts, ~lines 537-959), B23-B24 (synthesis mapping, ~lines 962-1105), B25-B28 (validation checklists, ~lines 1106-1245), B29-B34 (operational guidance, ~lines 1246-1364)
5. **[VERIFICATION]** Confirm no behavioral blocks (B01-B11, B13, B14) were affected by removal
6. **[COMPLETION]** Record block removal evidence with before/after line counts

**Acceptance Criteria:**
- `src/superclaude/skills/tdd/SKILL.md` no longer contains Block B12, B15-B22, B23-B24, B25-B28, or B29-B34 content
- All behavioral blocks (B01-B11, B13, B14) remain present and unchanged
- No HOW content remains: no agent prompts, no checklists, no mapping tables, no BUILD_REQUEST body
- Evidence records line count reduction (before vs after)

**Validation:**
- Manual check: `grep` for known unique strings from removed blocks returns zero matches in SKILL.md
- Evidence: linkable artifact produced at intended path

**Dependencies:** T02.01, T02.02, T02.03, T02.04, T02.05, T03.01
**Rollback:** Restore SKILL.md from git (`git checkout src/superclaude/skills/tdd/SKILL.md`)

---

### T04.02 -- Insert Loading Declarations in SKILL.md per FR-TDD-R.6

| Field | Value |
|---|---|
| Roadmap Item IDs | R-025 |
| Why | FR-TDD-R.6 requires explicit per-phase loading declarations so SKILL.md declares which refs files load at each phase and by whom (orchestrator vs builder). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0018 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0018/evidence.md`

**Deliverables:**
1. SKILL.md with explicit loading declarations at Stage A.7 and Stage B delegation sections

**Steps:**
1. **[PLANNING]** Load phase loading contract matrix (D-0006) as the source of truth for declarations
2. **[PLANNING]** Identify insertion points in SKILL.md: Stage A.7 section and BUILD_REQUEST/builder delegation section
3. **[EXECUTION]** Insert explicit `Read refs/build-request-template.md` directive at Stage A.7 (FR-TDD-R.6a)
4. **[EXECUTION]** Insert builder load dependencies for 4 builder refs files at Stage B delegation or BUILD_REQUEST section (FR-TDD-R.6b)
5. **[VERIFICATION]** Insert phase contract conformance table declaring loads and forbidden loads per phase (FR-TDD-R.6c)
6. **[COMPLETION]** Validate `declared_loads intersect forbidden_loads = empty set` for every phase

**Acceptance Criteria:**
- Stage A.7 loading declaration for `refs/build-request-template.md` is explicit in SKILL.md (FR-TDD-R.6a)
- Builder load dependencies for `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` are explicit (FR-TDD-R.6b)
- Phase contract conformance table present matching Phase 1 loading contract baseline (FR-TDD-R.6c)
- Contract validation: `declared_loads intersect forbidden_loads = empty set` for every phase (SC-9)

**Validation:**
- Manual check: `grep 'refs/' src/superclaude/skills/tdd/SKILL.md` returns all 5 refs file declarations
- Evidence: linkable artifact produced at intended path

**Dependencies:** T04.01, T01.06
**Rollback:** Restore SKILL.md from git

---

### T04.03 -- Insert Load-Point Replacement Markers in SKILL.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-026 |
| Why | Where each content block was removed, a brief directive must be inserted so readers understand the delegation to refs files. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0019/evidence.md`

**Deliverables:**
1. SKILL.md with load-point replacement markers at each removed content block location

**Steps:**
1. **[PLANNING]** Identify the 5 locations where content blocks were removed in T04.01
2. **[PLANNING]** Determine appropriate marker text for each location
3. **[EXECUTION]** Insert replacement markers at each removed block location, e.g.:
   - `> **Loaded at runtime from** refs/agent-prompts.md`
   - `> **Loaded at runtime from** refs/build-request-template.md`
   - `> **Loaded at runtime from** refs/synthesis-mapping.md`
   - `> **Loaded at runtime from** refs/validation-checklists.md`
   - `> **Loaded at runtime from** refs/operational-guidance.md`
4. **[EXECUTION]** Verify markers are placed at correct locations in the document flow
5. **[VERIFICATION]** Confirm 5 markers present, one per removed block group
6. **[COMPLETION]** Document marker placement with line numbers

**Acceptance Criteria:**
- 5 load-point replacement markers present in `src/superclaude/skills/tdd/SKILL.md`, one per removed content block group
- Each marker names the specific refs file that replaced the removed content
- Markers do not alter behavioral protocol content
- `grep 'Loaded at runtime from' src/superclaude/skills/tdd/SKILL.md | wc -l` returns 5

**Validation:**
- Manual check: 5 replacement markers present at correct document locations
- Evidence: linkable artifact produced at intended path

**Dependencies:** T04.01
**Rollback:** Remove inserted markers from SKILL.md

---

### T04.04 -- Verify All Behavioral Blocks B01-B11, B13, B14 Preserved

| Field | Value |
|---|---|
| Roadmap Item IDs | R-027 |
| Why | Behavioral blocks (frontmatter, purpose, input, tier selection, output locations, execution overview, Stage A steps, Stage B delegation) must remain unchanged in SKILL.md. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0020/evidence.md`

**Deliverables:**
1. Behavioral blocks preservation confirmation report

**Steps:**
1. **[PLANNING]** Load corrected fidelity index (D-0007) with block ranges for B01-B11, B13, B14
2. **[PLANNING]** Extract expected content for each behavioral block from the fidelity index checksum markers
3. **[EXECUTION]** For each behavioral block, verify its content is present and unchanged in reduced SKILL.md
4. **[EXECUTION]** Check checksum markers (first 10 / last 10 words) for each behavioral block
5. **[VERIFICATION]** Confirm zero drift in any behavioral block
6. **[COMPLETION]** Document block-by-block verification results

**Acceptance Criteria:**
- All 13 behavioral blocks (B01-B11, B13, B14) present in reduced SKILL.md
- Checksum markers (first 10 / last 10 words) match source for every behavioral block
- Zero content modifications to behavioral blocks (only surrounding context changed by block removal)
- Evidence records block-by-block verification status

**Validation:**
- Manual check: sample 3 behavioral blocks and verify verbatim content match
- Evidence: linkable artifact produced at intended path

**Dependencies:** T04.01, T04.02, T04.03
**Rollback:** N/A (read-only verification)

---

### T04.05 -- Validate SKILL.md Line Count Under 500

| Field | Value |
|---|---|
| Roadmap Item IDs | R-028 |
| Why | FR-TDD-R.1a requires the refactored SKILL.md to be strictly under 500 lines. This is a hard pass/fail gate. |
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
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0021/evidence.md`

**Deliverables:**
1. Line count validation result confirming SKILL.md < 500 lines

**Steps:**
1. **[PLANNING]** Identify canonical SKILL.md path
2. **[PLANNING]** Confirm all reduction operations (T04.01-T04.03) are complete
3. **[EXECUTION]** Run `wc -l src/superclaude/skills/tdd/SKILL.md`
4. **[EXECUTION]** Compare result against 500-line budget
5. **[VERIFICATION]** Confirm line count is strictly less than 500 (FR-TDD-R.1a)
6. **[COMPLETION]** Record line count with pass/fail determination

**Acceptance Criteria:**
- `wc -l src/superclaude/skills/tdd/SKILL.md` output is strictly less than 500
- Result recorded in evidence with exact count
- Pass/fail determination documented
- Token reduction percentage calculated vs original 1,364-line baseline

**Validation:**
- Manual check: `wc -l src/superclaude/skills/tdd/SKILL.md` returns value < 500
- Evidence: linkable artifact produced at intended path

**Dependencies:** T04.01, T04.02, T04.03
**Rollback:** N/A (read-only verification)

---

### Checkpoint: Phase 4 / Tasks T04.01-T04.05

**Purpose:** Verify SKILL.md reduction is complete with behavioral blocks preserved and line count under budget before advancing to final validation.
**Checkpoint Report Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/CP-P04-T01-T05.md`
**Verification:**
- SKILL.md line count < 500 confirmed
- All behavioral blocks (B01-B11, B13, B14) present and unchanged
- Loading declarations inserted and contract-compliant
**Exit Criteria:**
- SC-1 (<500 lines) confirmed
- No HOW content remains in SKILL.md
- Phase contract conformance validated

---

### T04.06 -- Validate Retained Content per FR-TDD-R.1b Through FR-TDD-R.1e

| Field | Value |
|---|---|
| Roadmap Item IDs | R-029 |
| Why | FR-TDD-R.1b-e requires SKILL.md retains specific content categories: frontmatter/metadata, Purpose/Input/Tier, Stage A/B protocols, Will Do/Will Not Do, and refs loading declarations. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0022/evidence.md`

**Deliverables:**
1. Retained content validation confirming all FR-TDD-R.1b-e categories present

**Steps:**
1. **[PLANNING]** Load FR-TDD-R.1b-e acceptance criteria from spec
2. **[PLANNING]** Load reduced SKILL.md from `src/superclaude/skills/tdd/SKILL.md`
3. **[EXECUTION]** Verify presence of: frontmatter and extended metadata (FR-TDD-R.1b)
4. **[EXECUTION]** Verify presence of: Purpose/Input/Tier sections (FR-TDD-R.1c), Stage A protocol and Stage B delegation (FR-TDD-R.1d), Will Do / Will Not Do boundaries (FR-TDD-R.1e), explicit refs loading declarations
5. **[VERIFICATION]** All 5 content categories confirmed present
6. **[COMPLETION]** Document per-category validation results

**Acceptance Criteria:**
- SKILL.md contains YAML frontmatter and extended metadata comment (FR-TDD-R.1b)
- SKILL.md contains Purpose, Input, and Tier sections (FR-TDD-R.1c)
- SKILL.md contains Stage A protocol and Stage B delegation protocol (FR-TDD-R.1d)
- SKILL.md contains Will Do / Will Not Do boundaries and explicit refs loading declarations (FR-TDD-R.1e)

**Validation:**
- Manual check: grep for section headings confirming all required sections present
- Evidence: linkable artifact produced at intended path

**Dependencies:** T04.01, T04.02, T04.03
**Rollback:** N/A (read-only verification)

---

### Checkpoint: End of Phase 4

**Purpose:** Confirm SKILL.md is fully reduced to behavioral protocol with loading declarations and all retention criteria met before advancing to sync and final validation.
**Checkpoint Report Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/CP-P04-END.md`
**Verification:**
- SKILL.md < 500 lines (SC-1)
- All behavioral blocks preserved (B01-B11, B13, B14)
- All FR-TDD-R.1b-e content categories present
**Exit Criteria:**
- SC-1 (<500 lines), SC-9 (phase contract conformance), SC-13 (behavioral parity prereq), SC-14 (token reduction prereq) satisfied
- Loading declarations match Phase 1 contract baseline
- Phase 5 prerequisites (Phase 4 gate) satisfied
