# Phase 2 -- Content Extraction

Extract HOW content from SKILL.md into 4 refs/ files with word-for-word fidelity. Tasks 2.1-2.3 extract from independent, non-overlapping line ranges and are parallelizable. Task 2.4 depends on 2.1-2.3 destination paths and must run sequentially after them.

---

### T02.01 -- Create refs/agent-prompts.md with 8 agent templates

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | The 8 agent prompt templates (lines 553-967, ~415 lines) are HOW content loaded only during Stage A.7; extracting them to refs/ enables per-phase lazy loading and reduces invocation token cost by ~1,500 tokens. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | `[########--]` 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0005, D-0006 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0005/spec.md`
- `.dev/releases/current/v3.8/artifacts/D-0006/evidence.md`

**Deliverables:**
1. File `.claude/skills/prd/refs/agent-prompts.md` containing all 8 agent prompt templates extracted word-for-word from original SKILL.md lines 553-967
2. Diff verification log confirming zero content changes across all 8 templates (whitespace normalization only)

**Steps:**
1. **[PLANNING]** Read fidelity index blocks B14-B21 to identify exact line ranges for each of 8 agent prompt templates
2. **[PLANNING]** Read original `.claude/skills/prd/SKILL.md` lines 553-967 to capture source content
3. **[EXECUTION]** Create `.claude/skills/prd/refs/agent-prompts.md` with header explaining purpose ("Agent prompt templates for the PRD pipeline, loaded during Stage A.7 by the builder subagent")
4. **[EXECUTION]** Copy section header + introductory paragraph (lines 553-557) and all 8 templates verbatim, including "Common web research topics for PRDs" list (lines 679-686)
5. **[VERIFICATION]** Diff each of 8 templates against original line ranges; confirm zero content changes
6. **[COMPLETION]** Record diff results in evidence artifact; confirm ~415 lines extracted

**Acceptance Criteria:**
- File `.claude/skills/prd/refs/agent-prompts.md` exists and contains all 8 agent prompt templates: Codebase Research, Web Research, Synthesis, Research Analyst, Research QA, Synthesis QA, Report Validation QA, Assembly
- `diff` of each template against original SKILL.md line ranges shows zero content changes (whitespace normalization permitted)
- File includes section header "Agent Prompt Templates" and introductory paragraph from lines 553-557
- File line count is approximately 415 lines (within 10% tolerance)

**Validation:**
- `diff` output for each of 8 templates against original line ranges returns empty (zero changes)
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0006/evidence.md`

**Dependencies:** T01.03 (refs/ directory must exist)
**Rollback:** `rm .claude/skills/prd/refs/agent-prompts.md`
**Notes:** Parallelizable with T02.02 and T02.03 (independent, non-overlapping line ranges).

---

### T02.02 -- Create refs/synthesis-mapping.md with output structure and mapping table

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | The Output Structure and Synthesis Mapping Table (lines 969-1106, ~137 lines) are HOW content used by the builder subagent during task file creation; extracting them enables lazy loading and reduces invocation cost by ~500 tokens. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | `[########--]` 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0007, D-0008 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0007/spec.md`
- `.dev/releases/current/v3.8/artifacts/D-0008/evidence.md`

**Deliverables:**
1. File `.claude/skills/prd/refs/synthesis-mapping.md` containing Output Structure + Synthesis Mapping Table extracted word-for-word from original SKILL.md lines 969-1106
2. Diff verification log confirming zero content changes

**Steps:**
1. **[PLANNING]** Read fidelity index blocks B22-B23 to identify exact line ranges
2. **[PLANNING]** Read original `.claude/skills/prd/SKILL.md` lines 969-1106 to capture source content
3. **[EXECUTION]** Create `.claude/skills/prd/refs/synthesis-mapping.md` with header explaining purpose ("Output Structure reference and Synthesis Mapping Table, loaded during Stage A.7 by the builder subagent")
4. **[EXECUTION]** Copy Output Structure (lines 969-1085) and Synthesis Mapping Table (lines 1087-1106) verbatim; retain all `> **Note:**` reference documentation markers
5. **[VERIFICATION]** Diff against original line ranges; confirm zero content changes
6. **[COMPLETION]** Record diff results in evidence artifact; confirm ~140 lines extracted

**Acceptance Criteria:**
- File `.claude/skills/prd/refs/synthesis-mapping.md` exists with Output Structure (PRD section outline from "1. Executive Summary" through "Document Approval") and 9-row Synthesis Mapping Table
- `diff` against original SKILL.md lines 969-1106 shows zero content changes
- All `> **Note:**` reference documentation markers retained
- File line count is approximately 140 lines (plus header)

**Validation:**
- `diff` output against original line ranges returns empty (zero changes)
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0008/evidence.md`

**Dependencies:** T01.03 (refs/ directory must exist)
**Rollback:** `rm .claude/skills/prd/refs/synthesis-mapping.md`
**Notes:** Parallelizable with T02.01 and T02.03 (independent, non-overlapping line ranges).

---

### T02.03 -- Create refs/validation-checklists.md with checklists and content rules

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | The Synthesis Quality Review Checklist, Assembly Process, Validation Checklist, and Content Rules (lines 1108-1254, ~150 lines plus header) are HOW content used during Phase 5-6; extracting them reduces invocation cost by ~500 tokens. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | `[########--]` 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009, D-0010 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0009/spec.md`
- `.dev/releases/current/v3.8/artifacts/D-0010/evidence.md`

**Deliverables:**
1. File `.claude/skills/prd/refs/validation-checklists.md` containing 4 validation content blocks extracted word-for-word from original SKILL.md lines 1108-1254
2. Diff verification log confirming zero content changes

**Steps:**
1. **[PLANNING]** Read fidelity index blocks B24-B27 to identify exact line ranges
2. **[PLANNING]** Read original `.claude/skills/prd/SKILL.md` lines 1108-1254 to capture source content
3. **[EXECUTION]** Create `.claude/skills/prd/refs/validation-checklists.md` with header explaining purpose ("Synthesis Quality Review, Assembly Process, Validation Checklist, and Content Rules, loaded during Stage A.7 by the builder subagent")
4. **[EXECUTION]** Copy all 4 blocks verbatim: Synthesis Quality Review Checklist (9 criteria, lines 1108-1128), Assembly Process Steps 8-11 (lines 1130-1193), Validation Checklist 18+4 items (lines 1195-1235), Content Rules table 10 rows (lines 1237-1254); retain all `> **Note:**` markers
5. **[VERIFICATION]** Diff against original line ranges; confirm zero content changes
6. **[COMPLETION]** Record diff results in evidence artifact; confirm ~150 lines extracted

**Acceptance Criteria:**
- File `.claude/skills/prd/refs/validation-checklists.md` exists with all 4 content blocks: Synthesis Quality Review (9 criteria), Assembly Process (Steps 8-11), Validation Checklist (18 structural/semantic + 4 content quality), Content Rules (10 rows)
- `diff` against original SKILL.md lines 1108-1254 shows zero content changes
- All `> **Note:**` reference documentation markers retained
- File line count is approximately 150 lines (plus header)

**Validation:**
- `diff` output against original line ranges returns empty (zero changes)
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0010/evidence.md`

**Dependencies:** T01.03 (refs/ directory must exist)
**Rollback:** `rm .claude/skills/prd/refs/validation-checklists.md`
**Notes:** Parallelizable with T02.01 and T02.02 (independent, non-overlapping line ranges).

---

### T02.04 -- Create refs/build-request-template.md with updated cross-references

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | The BUILD_REQUEST format (lines 344-508, ~165 lines) is the dispatch table wiring builder subagent phases to refs/ files; extracting it with updated SKILL CONTEXT FILE references completes the refs/ architecture. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | `[#######---]` 75% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011, D-0012 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0011/spec.md`
- `.dev/releases/current/v3.8/artifacts/D-0012/evidence.md`

**Deliverables:**
1. File `.claude/skills/prd/refs/build-request-template.md` containing the BUILD_REQUEST format from original SKILL.md lines 344-508 with exactly 6 SKILL CONTEXT FILE reference path updates
2. Cross-reference update verification confirming only the documented 6 path changes and zero other content changes

**Steps:**
1. **[PLANNING]** Read fidelity index block B11 to identify exact line range (344-508)
2. **[PLANNING]** Read the cross-reference update map (spec Section 12.2) to identify the 6 required path changes
3. **[EXECUTION]** Create `.claude/skills/prd/refs/build-request-template.md` with header explaining purpose ("BUILD_REQUEST format for spawning the rf-task-builder subagent, loaded during Stage A.7 by the orchestrator")
4. **[EXECUTION]** Copy BUILD_REQUEST block verbatim from lines 344-508, then apply exactly 6 SKILL CONTEXT FILE path updates: "Agent Prompt Templates section" -> `refs/agent-prompts.md`, "Synthesis Mapping Table section" -> `refs/synthesis-mapping.md`, "Synthesis Quality Review Checklist section" -> `refs/validation-checklists.md`, "Assembly Process section" -> `refs/validation-checklists.md`, "Validation Checklist section" -> `refs/validation-checklists.md`, "Content Rules section" -> `refs/validation-checklists.md`
5. **[EXECUTION]** Update Phase 2 task file references: `from SKILL.md` -> `from refs/agent-prompts.md` (and similar per spec Section 12.2)
6. **[VERIFICATION]** Diff against original lines 344-508; confirm ONLY the 6 documented SKILL CONTEXT FILE path changes and Phase 2 reference updates; zero other content changes
7. **[COMPLETION]** Record diff results and cross-reference update inventory in evidence artifact

**Acceptance Criteria:**
- File `.claude/skills/prd/refs/build-request-template.md` exists with complete BUILD_REQUEST format including TEMPLATE 02 PATTERN MAPPING, SKILL PHASES TO ENCODE, GRANULARITY REQUIREMENT, ESCALATION rules, and STEPS list
- `diff` against original SKILL.md lines 344-508 shows exactly the 6 documented SKILL CONTEXT FILE path changes and the Phase 2 task file reference updates documented in spec Section 12.2; zero other content changes
- `grep 'refs/agent-prompts.md' refs/build-request-template.md` returns match confirming updated path
- "Tier Selection" section reference remains pointing to SKILL.md (unchanged)

**Validation:**
- `diff` output against original shows only documented path changes
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0012/evidence.md`

**Dependencies:** T02.01, T02.02, T02.03 (must know destination file paths for cross-reference updates)
**Rollback:** `rm .claude/skills/prd/refs/build-request-template.md`
**Notes:** Sequential after T02.01-T02.03 due to cross-reference dependency. Addresses roadmap Risk #2 (cross-reference breakage).

---

### Checkpoint: End of Phase 2

**Purpose:** Confirm all 4 refs/ files are created with verified word-for-word fidelity against original SKILL.md line ranges.
**Checkpoint Report Path:** `.dev/releases/current/v3.8/checkpoints/CP-P02-END.md`
**Verification:**
- 4 files exist in `.claude/skills/prd/refs/`: agent-prompts.md, synthesis-mapping.md, validation-checklists.md, build-request-template.md
- `diff` of agent prompts (8 templates), synthesis mapping, and validation checklists against original line ranges shows zero content changes
- `diff` of BUILD_REQUEST shows exactly 6 SKILL CONTEXT FILE path changes and zero other content changes
**Exit Criteria:**
- Combined refs/ line count is approximately 870 lines (within 30-line tolerance)
- All diff verification logs produced (D-0006, D-0008, D-0010, D-0012)
- Risks #1 (content loss), #5 (B05/B30 merge), and #6 (missing refs) largely retired per roadmap risk burn-down
