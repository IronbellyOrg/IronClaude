# Phase 3 -- SKILL.md Restructuring

Remove extracted content from SKILL.md, add loading declarations, update cross-references, and merge the B05/B30 duplicate table. Result: a 430-500 line behavioral protocol file that references refs/ for HOW content. Tasks 3.1-3.4 are sequential (all modify the same file); Task 3.5 is a verification gate.

---

### T03.01 -- Remove extracted content blocks from SKILL.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | Removing blocks B11, B14-B21, B22-B23, and B24-B27 from SKILL.md completes the content relocation to refs/ files; these ~800 lines of HOW content are no longer needed in the behavioral spine. |
| Effort | S |
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
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0013/evidence.md`

**Deliverables:**
1. Reduced `.claude/skills/prd/SKILL.md` with content blocks B11 (lines 344-508), B14-B21 (lines 553-967), B22-B23 (lines 969-1106), and B24-B27 (lines 1108-1254) removed while retaining all behavioral blocks (B01-B10, B12-B13, B28-B32)

**Steps:**
1. **[PLANNING]** Read fidelity index to confirm which blocks are removed vs retained
2. **[PLANNING]** Plan removal order: work from highest line numbers downward to avoid line-shift errors (B24-B27 first, then B22-B23, then B14-B21, then B11)
3. **[EXECUTION]** Remove blocks B24-B27 (lines 1108-1254): checklists + assembly + content rules
4. **[EXECUTION]** Remove blocks B22-B23 (lines 969-1106): output structure + synthesis mapping
5. **[EXECUTION]** Remove blocks B14-B21 (lines 553-967): agent prompt templates
6. **[EXECUTION]** Remove block B11 (lines 344-508): BUILD_REQUEST format
7. **[VERIFICATION]** Confirm all behavioral blocks (B01-B10, B12-B13, B28-B32) remain intact; `wc -l` shows significant reduction from 1,373 lines
8. **[COMPLETION]** Record removal inventory and post-removal line count in evidence artifact

**Acceptance Criteria:**
- `.claude/skills/prd/SKILL.md` no longer contains agent prompt templates, BUILD_REQUEST format, output structure, synthesis mapping table, validation checklists, assembly process steps, or content rules table
- All behavioral blocks (B01-B10, B12-B13, B28-B32) remain present and unmodified in SKILL.md
- `grep -c 'Assembly Process' .claude/skills/prd/SKILL.md` returns 0
- SKILL.md line count is significantly reduced from 1,373 (approximately 530 remaining before loading declarations added)

**Validation:**
- `grep -c 'Content Rules' .claude/skills/prd/SKILL.md` returns 0 (confirming content rules removed)
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0013/evidence.md`

**Dependencies:** T02.01, T02.02, T02.03, T02.04 (all refs/ files must exist before removing content from SKILL.md)
**Rollback:** `git checkout -- .claude/skills/prd/SKILL.md` (restores original monolithic version)
**Notes:** CRITICAL: Work from highest line numbers downward to avoid line-shift errors per roadmap instruction.

---

### T03.02 -- Add per-phase loading declarations at Stage A.7

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | Loading declarations tell the orchestrator and builder subagent which refs/ files to load during Stage A.7, following the sc-adversarial-protocol "See refs/" pattern (FR-PRD-R.6). |
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
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0014/evidence.md`

**Deliverables:**
1. SKILL.md Stage A.7 section updated with loading declaration block distinguishing orchestrator loading from builder loading

**Steps:**
1. **[PLANNING]** Identify the Stage A.7 section in the reduced SKILL.md
2. **[PLANNING]** Reference the sc-adversarial-protocol pattern observed in T01.04 for syntax format
3. **[EXECUTION]** Add loading declaration block to Stage A.7 section using concrete inline reference format:
   - **Orchestrator loads**: `refs/build-request-template.md` (to construct the builder prompt)
   - **Builder subagent loads** (referenced within BUILD_REQUEST): `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`
4. **[EXECUTION]** Verify no other phase (A.1-A.6, Stage B) loads refs/ files
5. **[VERIFICATION]** `grep 'refs/' .claude/skills/prd/SKILL.md` shows loading declarations only at A.7; confirm orchestrator loads at most 2 refs simultaneously (SKILL.md + build-request-template.md)
6. **[COMPLETION]** Record grep output in evidence artifact

**Acceptance Criteria:**
- Stage A.7 section in SKILL.md contains a loading declaration block with orchestrator and builder loading paths clearly distinguished
- No phases outside A.7 contain loading declarations for refs/ files. Informational refs/ mentions in other sections are permitted.
- No other phase (A.1-A.6, A.8, Stage B) contains refs/ loading instructions
- Orchestrator context loads at most 2 refs simultaneously (SKILL.md + build-request-template.md) per NFR-PRD-R.2

**Validation:**
- Manual inspection confirms loading declarations (Read/Load directives) for refs/ files appear only in A.7 section
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0014/evidence.md`

**Dependencies:** T03.01 (extracted content must be removed before adding loading declarations)
**Rollback:** Remove the loading declaration block from Stage A.7 section

---

### T03.03 -- Update internal cross-references to use refs/ paths

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | Any remaining prose references in SKILL.md pointing to "the Agent Prompt Templates section" or similar must be updated to refs/ file paths; stale references would cause confusion during execution (addresses Risk #2). |
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
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0015/evidence.md`

**Deliverables:**
1. SKILL.md with all former prose section references (e.g., "Agent Prompt Templates section in SKILL.md") replaced with correct refs/ file paths

**Steps:**
1. **[PLANNING]** Identify all stale section references by running `grep` for pattern variations: "section", "Agent Prompt", "Synthesis Mapping", "Assembly Process", "Validation Checklist", "Content Rules"
2. **[PLANNING]** Map each stale reference to its correct refs/ file path using the cross-reference map from spec Section 12.2
3. **[EXECUTION]** Replace each stale prose reference with the corresponding refs/ file path
4. **[EXECUTION]** B13 (Stage B) reference describes what was baked into the task file -- this is informational, not a stale section reference per the roadmap's intent (source: spec Section 12.2)
5. **[VERIFICATION]** `grep -c '".*section"' .claude/skills/prd/SKILL.md` returns 0 matches (no stale section references remain)
6. **[COMPLETION]** Record grep output and replacement inventory in evidence artifact

**Acceptance Criteria:**
- `grep -c 'Agent Prompt Templates section' .claude/skills/prd/SKILL.md` returns 0
- `grep -c 'Synthesis Mapping Table section' .claude/skills/prd/SKILL.md` returns 0
- `grep -c 'Assembly Process section' .claude/skills/prd/SKILL.md` returns 0
- All prose section references replaced with refs/ file paths per cross-reference map

**Validation:**
- All of the following return 0: `grep -c 'Agent Prompt Templates section'`, `grep -c 'Synthesis Mapping.*section'`, `grep -c 'Assembly Process.*section'`, `grep -c 'Validation Checklist.*section'`, `grep -c 'Content Rules.*section'`
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0015/evidence.md`

**Dependencies:** T03.01, T03.02 (content removed and loading declarations added first)
**Rollback:** Revert cross-reference changes via `git diff` review
**Notes:** B13 Stage B reference to refs/ content is informational only (per spec Section 12.2 note) -- do not remove it.

---

### T03.04 -- Merge B05/B30 Artifact Locations table

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | Block B30 (lines 1327-1347) is a near-duplicate of B05 Output Locations with additional QA report paths; merging per GAP-01 eliminates redundancy while preserving all unique entries. |
| Effort | S |
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
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0016/evidence.md`

**Deliverables:**
1. SKILL.md with B05 Artifact Locations table expanded to include B30's 6 specific QA paths, standalone B30 section removed

**Steps:**
1. **[PLANNING]** Read B05 (Output Locations) and B30 (Artifact Locations) from fidelity index to identify content and line ranges
2. **[PLANNING]** Identify B30's unique entries not already in B05 (the 6 specific QA paths: analyst-completeness-report, analyst-synthesis-review, qa-research-gate-report, qa-synthesis-gate-report, qa-report-validation, qa-qualitative-review)
3. **[EXECUTION]** Append B30's 6 specific QA paths as additional rows below B05's existing table without renaming B30 filenames; preserve B05 existing rows and keep B30 cosmetic variant as-is
4. **[EXECUTION]** Remove the standalone B30 section (which previously duplicated B05)
5. **[VERIFICATION]** Confirm merged table contains all original B05 rows plus B30's unique QA paths; no rows lost
6. **[COMPLETION]** Record merge inventory in evidence artifact

**Acceptance Criteria:**
- B05 Artifact Locations table in SKILL.md contains all original rows plus 6 appended QA paths from B30
- Standalone B30 section no longer exists in SKILL.md
- B30's `[NN]-[topic].md` naming variant coexists with B05's `[NN]-[topic-name].md` convention (cosmetic inconsistency preserved per spec -- not resolved during this refactoring)
- No rows from either B05 or B30 were dropped during the merge

**Validation:**
- Manual check: merged table row count equals original B05 rows + 6 new QA path rows
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0016/evidence.md`

**Dependencies:** T03.01 (B30 standalone section must be identifiable before merge)
**Rollback:** Restore B05 and B30 from git history
**Notes:** Per spec and roadmap OQ-2: do NOT resolve the B30 `[NN]-[topic].md` vs B05 `[NN]-[topic-name].md` naming inconsistency. Content preservation takes priority.

---

### T03.05 -- Verify SKILL.md line count within 430-500 target

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | The 500-line hard ceiling is the primary compliance target (Developer Guide Section 9.3); verifying line count confirms the refactoring achieved its goal and catches accidental over- or under-extraction. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | `[########--]` 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct verification (wc -l + token estimate) |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0017/evidence.md`

**Deliverables:**
1. Line count verification report confirming SKILL.md is within 430-500 lines with token estimate

**Steps:**
1. **[PLANNING]** Identify verification targets: 430-500 line range (hard ceiling at 500), ~2,000 token estimate (soft target)
2. **[EXECUTION]** Run `wc -l .claude/skills/prd/SKILL.md` and record result
3. **[EXECUTION]** Compute estimated token count: line count * 4.5 tokens/line
4. **[VERIFICATION]** If over 500: identify lowest-priority behavioral content for further decomposition. If under 430: verify no content accidentally over-extracted. Per OQ-1: 500-line hard ceiling takes precedence; 2,000-token target is soft (accept up to ~3.5% overshoot).
5. **[COMPLETION]** Record line count, token estimate, and pass/fail determination in evidence artifact

**Acceptance Criteria:**
- `wc -l .claude/skills/prd/SKILL.md` returns a value between 430 and 500 inclusive
- Estimated token count (line count * 4.5) is advisory; do not fail if line count is 430-500. Record estimate and note if materially above ~2,000.
- If >500: lowest-priority behavioral candidates for decomposition identified. If <430: explicit over-extraction verification result documented.
- Verification evidence recorded with exact counts

**Validation:**
- `wc -l .claude/skills/prd/SKILL.md` returns value in range [430, 500]
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0017/evidence.md`

**Dependencies:** T03.01, T03.02, T03.03, T03.04 (all SKILL.md modifications must be complete)
**Rollback:** N/A (read-only verification task; if line count fails, remediation is a separate concern)

---

### Checkpoint: End of Phase 3

**Purpose:** Confirm SKILL.md is a compliant behavioral spine with correct loading declarations, updated cross-references, and merged B05/B30 table.
**Checkpoint Report Path:** `.dev/releases/current/v3.8/checkpoints/CP-P03-END.md`
**Verification:**
- SKILL.md line count is within 430-500 range (hard ceiling)
- `grep` for stale prose section references returns 0 matches
- Loading declarations present at A.7 with correct refs/ paths; no other phase loads refs/
**Exit Criteria:**
- All 5 Phase 3 tasks (T03.01-T03.05) completed with deliverables D-0013 through D-0017 produced
- Risks #2 (cross-reference breakage) and #3 (loading order wrong) retired per roadmap risk burn-down
- Token estimate is approximately 2,000 (soft target per OQ-1)
