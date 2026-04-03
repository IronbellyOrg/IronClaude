# Phase 2 -- Content Migration: Parallel Extraction

Create the 5 refs files with verbatim content from verified source ranges. All 5 extraction tasks are parallelizable since they extract from non-overlapping line ranges into separate files. Zero textual drift from source is the acceptance standard.

---

### T02.01 -- Create refs/agent-prompts.md from Blocks B15-B22

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | FR-TDD-R.2 requires all 8 agent prompt templates extracted verbatim from source lines ~537-959 to enable lazy loading at Stage A.7 builder context. |
| Effort | S |
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
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0008/evidence.md`

**Deliverables:**
1. `src/superclaude/skills/tdd/refs/agent-prompts.md` containing all 8 agent prompt templates verbatim

**Steps:**
1. **[PLANNING]** Load corrected fidelity index (D-0007) to get verified line ranges for B15-B22
2. **[PLANNING]** Confirm source ranges are non-overlapping with other extraction targets
3. **[EXECUTION]** Extract blocks B15-B22 from `src/superclaude/skills/tdd/SKILL.md` at verified line ranges
4. **[EXECUTION]** Write extracted content to `src/superclaude/skills/tdd/refs/agent-prompts.md`
5. **[VERIFICATION]** Verify all 8 agent prompts present: Codebase, Web, Synthesis, Research Analyst, Research QA, Synthesis QA, Report Validation QA, Assembly
6. **[COMPLETION]** Run block-wise diff against source ranges to confirm zero drift

**Acceptance Criteria:**
- File exists at `src/superclaude/skills/tdd/refs/agent-prompts.md` with all 8 named agent prompts (FR-TDD-R.2a-d)
- Block-wise diff against source line ranges (B15-B22) shows zero textual drift
- Checksum markers (first 10 / last 10 words per block) match source
- No template sentinel placeholders (`{{`, `<placeholder>`, `TODO`, `FIXME`) present

**Validation:**
- Manual check: `grep -c '## .* Prompt' src/superclaude/skills/tdd/refs/agent-prompts.md` returns 8
- Evidence: linkable artifact produced at intended path

**Dependencies:** T01.07
**Rollback:** Delete `src/superclaude/skills/tdd/refs/agent-prompts.md`

---

### T02.02 -- Create refs/validation-checklists.md from Blocks B25-B28

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | FR-TDD-R.3 requires synthesis quality checklist, assembly process, validation checklist, and content rules extracted verbatim from source lines ~1106-1245. |
| Effort | S |
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
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0009/evidence.md`

**Deliverables:**
1. `src/superclaude/skills/tdd/refs/validation-checklists.md` containing all checklist content verbatim

**Steps:**
1. **[PLANNING]** Load corrected fidelity index (D-0007) to get verified line ranges for B25-B28
2. **[PLANNING]** Confirm source ranges cover all checklist sections without gaps
3. **[EXECUTION]** Extract blocks B25-B28 from `src/superclaude/skills/tdd/SKILL.md` at verified line ranges
4. **[EXECUTION]** Write extracted content to `src/superclaude/skills/tdd/refs/validation-checklists.md`
5. **[VERIFICATION]** Verify checklist numbering and checkbox structure preserved exactly (SC-12)
6. **[COMPLETION]** Run block-wise diff and structural diff against source ranges

**Acceptance Criteria:**
- File exists at `src/superclaude/skills/tdd/refs/validation-checklists.md` (FR-TDD-R.3a-d)
- Checklist numbering preserved exactly — no renumbering, no reordering (SC-12)
- Checkbox structure (`- [ ]` markers) preserved verbatim
- No template sentinel placeholders present

**Validation:**
- Manual check: checklist numbering and checkbox count match source line ranges
- Evidence: linkable artifact produced at intended path

**Dependencies:** T01.07
**Rollback:** Delete `src/superclaude/skills/tdd/refs/validation-checklists.md`

---

### T02.03 -- Create refs/synthesis-mapping.md from Blocks B23-B24

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | FR-TDD-R.4 requires output structure and synthesis mapping table extracted verbatim from source lines ~962-1105 for builder context loading. |
| Effort | S |
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
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0010/evidence.md`

**Deliverables:**
1. `src/superclaude/skills/tdd/refs/synthesis-mapping.md` containing mapping table and output structure verbatim

**Steps:**
1. **[PLANNING]** Load corrected fidelity index (D-0007) to get verified line ranges for B23-B24
2. **[PLANNING]** Confirm source ranges for synthesis mapping and output structure sections
3. **[EXECUTION]** Extract blocks B23-B24 from `src/superclaude/skills/tdd/SKILL.md` at verified line ranges
4. **[EXECUTION]** Write extracted content to `src/superclaude/skills/tdd/refs/synthesis-mapping.md`
5. **[VERIFICATION]** Verify all section headers and markdown tables preserved verbatim (FR-TDD-R.4a-d)
6. **[COMPLETION]** Run block-wise diff confirming zero drift in template section numbering

**Acceptance Criteria:**
- File exists at `src/superclaude/skills/tdd/refs/synthesis-mapping.md` (FR-TDD-R.4a-d)
- All section headers preserved verbatim with no renames
- All markdown tables preserved with identical column structure and content
- No template sentinel placeholders present

**Validation:**
- Manual check: section headers and table structure match source line ranges
- Evidence: linkable artifact produced at intended path

**Dependencies:** T01.07
**Rollback:** Delete `src/superclaude/skills/tdd/refs/synthesis-mapping.md`

---

### T02.04 -- Create refs/build-request-template.md from Block B12 (Verbatim Only)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | FR-TDD-R.5 requires the BUILD_REQUEST template extracted verbatim from source lines ~341-492. Path-reference updates are deferred to Phase 3. |
| Effort | S |
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
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0011/evidence.md`

**Deliverables:**
1. `src/superclaude/skills/tdd/refs/build-request-template.md` containing BUILD_REQUEST body verbatim (pre-wiring)

**Steps:**
1. **[PLANNING]** Load corrected fidelity index (D-0007) to get verified line range for B12
2. **[PLANNING]** Confirm Block B12 covers the complete BUILD_REQUEST template section
3. **[EXECUTION]** Extract block B12 from `src/superclaude/skills/tdd/SKILL.md` at verified line range
4. **[EXECUTION]** Write extracted content to `src/superclaude/skills/tdd/refs/build-request-template.md`
5. **[VERIFICATION]** Verify verbatim extraction — no path rewrites at this stage (FR-TDD-R.5a, R.5b)
6. **[COMPLETION]** Run block-wise diff confirming exact match with source

**Acceptance Criteria:**
- File exists at `src/superclaude/skills/tdd/refs/build-request-template.md` (FR-TDD-R.5a, R.5b)
- BUILD_REQUEST body is verbatim copy of Block B12 with zero modifications
- Original section-name references still present (path rewrites deferred to Phase 3)
- No template sentinel placeholders present

**Validation:**
- Manual check: `diff` against source Block B12 shows zero differences
- Evidence: linkable artifact produced at intended path

**Dependencies:** T01.07
**Rollback:** Delete `src/superclaude/skills/tdd/refs/build-request-template.md`
**Notes:** Path-reference updates deferred to T03.01 (Phase 3). Destination files must exist before references can resolve.

---

### T02.05 -- Create refs/operational-guidance.md from Blocks B29-B34

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | Architecture Section 4.1 and FR-TDD-R.7 fidelity scope require operational guidance content relocated to keep SKILL.md under 500 lines while preserving every line verbatim. |
| Effort | S |
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
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0012/evidence.md`

**Deliverables:**
1. `src/superclaude/skills/tdd/refs/operational-guidance.md` containing critical rules, quality signals, artifact locations, pipeline, and session guidance verbatim

**Steps:**
1. **[PLANNING]** Load corrected fidelity index (D-0007) to get verified line ranges for B29-B34
2. **[PLANNING]** Confirm OQ-2 resolution (T01.04) verified range 1246-1364 as operational guidance
3. **[EXECUTION]** Extract blocks B29-B34 from `src/superclaude/skills/tdd/SKILL.md` at verified line ranges
4. **[EXECUTION]** Write extracted content to `src/superclaude/skills/tdd/refs/operational-guidance.md`
5. **[VERIFICATION]** Verify zero textual drift from source (FR-TDD-R.7 fidelity checks)
6. **[COMPLETION]** Run block-wise diff and checksum marker verification

**Acceptance Criteria:**
- File exists at `src/superclaude/skills/tdd/refs/operational-guidance.md`
- Block-wise diff against source line ranges (B29-B34) shows zero textual drift
- Checksum markers (first 10 / last 10 words per block) match source
- No template sentinel placeholders present

**Validation:**
- Manual check: content matches source lines 1246-1364 with only line-ending/whitespace normalization
- Evidence: linkable artifact produced at intended path

**Dependencies:** T01.07, T01.04
**Rollback:** Delete `src/superclaude/skills/tdd/refs/operational-guidance.md`

---

### Checkpoint: Phase 2 / Tasks T02.01-T02.05

**Purpose:** Verify all 5 refs files extracted before running contract cross-check and advancing to Phase 3 wiring.
**Checkpoint Report Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/CP-P02-T01-T05.md`
**Verification:**
- All 5 refs files exist at canonical paths under `src/superclaude/skills/tdd/refs/`
- Block-wise diffs show zero drift for all extracted blocks
- Checksum markers verified for every block in every refs file
**Exit Criteria:**
- 5/5 files created (SC-2)
- Zero textual drift confirmed (SC-6)
- No sentinel placeholders in any refs file (SC-8)

---

### T02.06 -- Post-Extraction Contract Cross-Check

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | The extracted file set must match the phase loading contract documented in Phase 1 to confirm no unexpected refs files were created and no expected files are missing. |
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
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0013/evidence.md`

**Deliverables:**
1. Contract cross-check report confirming extracted files match loading contract

**Steps:**
1. **[PLANNING]** Load phase loading contract matrix (D-0006) from Phase 1
2. **[PLANNING]** List all files in `src/superclaude/skills/tdd/refs/`
3. **[EXECUTION]** Verify every refs file in the contract exists on disk
4. **[EXECUTION]** Verify no unexpected refs files were created beyond the contract
5. **[VERIFICATION]** Confirm 1:1 match between contract and filesystem
6. **[COMPLETION]** Document cross-check results

**Acceptance Criteria:**
- `ls src/superclaude/skills/tdd/refs/` lists exactly 5 files matching the loading contract
- Every file referenced in the Phase 1 loading contract matrix exists
- No files exist in `refs/` that are not in the loading contract
- Cross-check report documents the file-by-file comparison

**Validation:**
- Manual check: `ls src/superclaude/skills/tdd/refs/ | wc -l` returns 5
- Evidence: linkable artifact produced at intended path

**Dependencies:** T02.01, T02.02, T02.03, T02.04, T02.05, T01.06
**Rollback:** N/A (read-only verification)

---

### Checkpoint: End of Phase 2

**Purpose:** Confirm all content migration is complete with zero drift and full contract compliance before advancing to cross-reference wiring.
**Checkpoint Report Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/CP-P02-END.md`
**Verification:**
- All 5 refs files exist at canonical paths (SC-2)
- Block-wise diffs show zero drift for all blocks (SC-6)
- Contract cross-check confirms 1:1 match with loading contract
**Exit Criteria:**
- SC-2 (5/5 files exist), SC-6 (zero drift), SC-8 (no sentinels), SC-11 (8 agent prompts), SC-12 (checklist numbering) all pass
- Post-extraction contract cross-check passed
- Phase 3 prerequisites satisfied
