# Phase 3 -- BUILD_REQUEST Cross-Reference Wiring

Apply the 6 allowlisted path-reference updates to `refs/build-request-template.md` so that all SKILL CONTEXT references resolve to existing refs files. This phase depends on Phase 2 completion (all destination files must exist for references to resolve).

---

### T03.01 -- Apply 6 Path-Reference Updates to build-request-template.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-019 |
| Why | FR-TDD-R.5c and FR-TDD-R.5d require exactly 6 section-name references in BUILD_REQUEST replaced with concrete refs file paths. This is the highest-risk integration point. |
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
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0014/evidence.md`

**Deliverables:**
1. Updated `src/superclaude/skills/tdd/refs/build-request-template.md` with exactly 6 path-reference replacements

**Steps:**
1. **[PLANNING]** Load cross-reference map from spec Section 12.2 (6 replacements)
2. **[PLANNING]** Confirm all 4 target refs files exist (agent-prompts.md, synthesis-mapping.md, validation-checklists.md x3 refs)
3. **[EXECUTION]** Apply targeted string replacements per the closed allowlist:
   - "Agent Prompt Templates section" -> `refs/agent-prompts.md`
   - "Synthesis Mapping Table section" -> `refs/synthesis-mapping.md`
   - "Synthesis Quality Review Checklist section" -> `refs/validation-checklists.md`
   - "Assembly Process section" -> `refs/validation-checklists.md`
   - "Validation Checklist section" -> `refs/validation-checklists.md`
   - "Content Rules section" -> `refs/validation-checklists.md`
4. **[EXECUTION]** Verify "Tier Selection section" reference remains unchanged (points to SKILL.md)
5. **[VERIFICATION]** Grep for all 6 updated references — all match; grep for original section-name references — zero matches
6. **[COMPLETION]** Record all 6 replacements with before/after evidence

**Acceptance Criteria:**
- Exactly 6 path-reference changes applied to `src/superclaude/skills/tdd/refs/build-request-template.md` per FR-TDD-R.5c/d allowlist
- `grep` for original section-name references in build-request-template.md returns zero matches
- `grep` for all 6 updated `refs/` paths returns matches
- No other content in build-request-template.md modified (only allowlisted changes)

**Validation:**
- Manual check: `diff` against pre-wiring version shows exactly 6 changes and nothing else
- Evidence: linkable artifact produced at intended path

**Dependencies:** T02.04, T02.01, T02.02, T02.03
**Rollback:** Restore verbatim Block B12 content to build-request-template.md (re-extract from T02.04)
**Notes:** "Tier Selection section" intentionally remains pointing to SKILL.md per roadmap — no update needed.

---

### T03.02 -- Validate All Updated References Resolve to Existing Files

| Field | Value |
|---|---|
| Roadmap Item IDs | R-020 |
| Why | Each of the 6 updated path references must resolve to an existing file under src/superclaude/skills/tdd/ to prevent silent Stage A.7 failures. |
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
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0015/evidence.md`

**Deliverables:**
1. Reference resolution validation report confirming all 6 paths resolve

**Steps:**
1. **[PLANNING]** Extract all refs paths from updated build-request-template.md
2. **[PLANNING]** Construct full paths under `src/superclaude/skills/tdd/`
3. **[EXECUTION]** For each of the 6 updated references, verify target file exists at the stated path
4. **[EXECUTION]** Confirm `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md` all exist
5. **[VERIFICATION]** All 6 references resolve; zero dangling references
6. **[COMPLETION]** Document resolution results per reference

**Acceptance Criteria:**
- All 4 unique target files (`refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, and SKILL.md for Tier Selection) exist
- Zero dangling references in build-request-template.md
- Resolution check performed against `src/superclaude/skills/tdd/` canonical paths
- Evidence records each reference and its resolution status

**Validation:**
- Manual check: `ls src/superclaude/skills/tdd/refs/` confirms target files present
- Evidence: linkable artifact produced at intended path

**Dependencies:** T03.01
**Rollback:** N/A (read-only verification)

---

### T03.03 -- Diff BUILD_REQUEST Against Source Block B12

| Field | Value |
|---|---|
| Roadmap Item IDs | R-021 |
| Why | Only the 6 allowlisted path-reference changes should appear in the diff. Any other diff is a defect indicating unintended modifications. |
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
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0016/evidence.md`

**Deliverables:**
1. Block B12 diff report showing exactly 6 allowlisted changes

**Steps:**
1. **[PLANNING]** Extract Block B12 content from `src/superclaude/skills/tdd/SKILL.md` using corrected fidelity index ranges
2. **[PLANNING]** Load current `src/superclaude/skills/tdd/refs/build-request-template.md` (post-wiring)
3. **[EXECUTION]** Run diff between source Block B12 content and post-wiring build-request-template.md
4. **[EXECUTION]** Count and classify all differences
5. **[VERIFICATION]** Confirm exactly 6 differences, all matching the allowlisted path-reference changes (SC-7)
6. **[COMPLETION]** Document diff results with line-by-line evidence

**Acceptance Criteria:**
- Diff between source Block B12 and post-wiring build-request-template.md shows exactly 6 changes
- All 6 changes are path-reference replacements matching the spec Section 12.2 allowlist
- Zero non-allowlisted changes detected (SC-7)
- Evidence records the full diff output with change classification
- FR-TDD-R.5c and FR-TDD-R.5d acceptance criteria met per roadmap verification gate

**Validation:**
- Manual check: diff output reviewed and each change mapped to allowlist entry
- Evidence: linkable artifact produced at intended path

**Dependencies:** T03.01, T03.02
**Rollback:** N/A (read-only verification)

---

### Checkpoint: End of Phase 3

**Purpose:** Confirm BUILD_REQUEST cross-reference wiring is complete with only allowlisted changes before proceeding to SKILL.md reduction.
**Checkpoint Report Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/CP-P03-END.md`
**Verification:**
- All 6 path-reference updates applied and verified
- Zero original section-name references remain in build-request-template.md
- Diff against source Block B12 shows exactly 6 allowlisted changes
- FR-TDD-R.5c and FR-TDD-R.5d acceptance criteria met
**Exit Criteria:**
- SC-7 (only allowlisted transformations) confirmed
- SC-10 (BUILD_REQUEST references resolve) confirmed
- Phase 4 prerequisites (Phases 2+3 gates) satisfied
