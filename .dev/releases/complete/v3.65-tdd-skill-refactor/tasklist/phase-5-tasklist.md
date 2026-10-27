# Phase 5 -- Sync, Full Fidelity Gate & Acceptance

Propagate to dev copies, verify full system integrity, and confirm all 14 success criteria pass. This phase validates the complete refactoring end-to-end including sync pipeline, fidelity audits, sentinel checks, reference resolution, behavioral parity, and token reduction.

---

### T05.01 -- Run make sync-dev to Propagate Refs to Dev Copies

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032 |
| Why | `make sync-dev` propagates `src/superclaude/skills/tdd/` (SKILL.md + refs/) to `.claude/skills/tdd/` for Claude Code runtime use. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 70% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0023 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0023/evidence.md`

**Deliverables:**
1. Synced dev copies at `.claude/skills/tdd/` including `refs/` directory

**Steps:**
1. **[PLANNING]** Confirm all canonical files at `src/superclaude/skills/tdd/` are in final state
2. **[PLANNING]** Verify `make sync-dev` target handles new `refs/` directory propagation
3. **[EXECUTION]** Run `make sync-dev`
4. **[EXECUTION]** Capture command output and exit code
5. **[VERIFICATION]** Confirm exit code 0 and no error output
6. **[COMPLETION]** Record sync output as evidence

**Acceptance Criteria:**
- `make sync-dev` exits with code 0
- `.claude/skills/tdd/SKILL.md` is updated copy of `src/superclaude/skills/tdd/SKILL.md`
- `.claude/skills/tdd/refs/` directory created with all 5 refs files
- No error messages in sync output

**Validation:**
- Manual check: `make sync-dev` completes successfully
- Evidence: linkable artifact produced at intended path

**Dependencies:** T04.06
**Rollback:** `git checkout .claude/skills/tdd/`

---

### T05.02 -- Run make verify-sync for Src-Dev Parity

| Field | Value |
|---|---|
| Roadmap Item IDs | R-033 |
| Why | `make verify-sync` must exit 0 with zero drift to confirm src/ and .claude/ copies are identical (SC-4). |
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
| Deliverable IDs | D-0024 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0024/evidence.md`

**Deliverables:**
1. Sync verification result confirming zero drift between src/ and .claude/

**Steps:**
1. **[PLANNING]** Confirm T05.01 sync completed successfully
2. **[PLANNING]** Understand `make verify-sync` checks both files and refs directory
3. **[EXECUTION]** Run `make verify-sync`
4. **[EXECUTION]** Capture exit code and output
5. **[VERIFICATION]** Confirm exit code 0 with zero drift reported (SC-4)
6. **[COMPLETION]** Record verification output as evidence

**Acceptance Criteria:**
- `make verify-sync` exits with code 0
- Zero drift detected between `src/superclaude/skills/tdd/` and `.claude/skills/tdd/`
- Refs directory and all 5 refs files included in parity check
- Verification output recorded as evidence

**Validation:**
- Manual check: `make verify-sync` exits 0
- Evidence: linkable artifact produced at intended path

**Dependencies:** T05.01
**Rollback:** N/A (read-only verification)

---

### T05.03 -- Verify Dev Copy Refs File Existence

| Field | Value |
|---|---|
| Roadmap Item IDs | R-034 |
| Why | SC-3 requires all 5 refs files synced to `.claude/skills/tdd/refs/` for Claude Code runtime access. |
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
| Deliverable IDs | D-0025 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0025/evidence.md`

**Deliverables:**
1. Dev copy refs existence confirmation listing all 5 files

**Steps:**
1. **[PLANNING]** Confirm expected file list: agent-prompts.md, validation-checklists.md, synthesis-mapping.md, build-request-template.md, operational-guidance.md
2. **[PLANNING]** Confirm sync (T05.01) completed
3. **[EXECUTION]** Run `ls .claude/skills/tdd/refs/`
4. **[EXECUTION]** Verify all 5 expected files are present
5. **[VERIFICATION]** Confirm 5/5 files exist (SC-3)
6. **[COMPLETION]** Record file listing as evidence

**Acceptance Criteria:**
- `ls .claude/skills/tdd/refs/` lists exactly 5 files (SC-3)
- All expected filenames present: agent-prompts.md, build-request-template.md, operational-guidance.md, synthesis-mapping.md, validation-checklists.md
- No unexpected files in refs directory
- Evidence records full `ls` output

**Validation:**
- Manual check: `ls .claude/skills/tdd/refs/ | wc -l` returns 5
- Evidence: linkable artifact produced at intended path

**Dependencies:** T05.01
**Rollback:** N/A (read-only verification)

---

### T05.04 -- Full Fidelity Index Audit per FR-TDD-R.7

| Field | Value |
|---|---|
| Roadmap Item IDs | R-035 |
| Why | FR-TDD-R.7 requires comprehensive fidelity verification: 100% coverage, destination+checksum markers, allowlisted transforms only, forbidden transforms absent, normalized diff policy, no sentinels. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0026 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0026/spec.md`

**Deliverables:**
1. Fidelity index audit report confirming FR-TDD-R.7a-f compliance

**Steps:**
1. **[PLANNING]** Load corrected fidelity index (D-0007) as the audit baseline
2. **[PLANNING]** Load all 5 refs files and reduced SKILL.md
3. **[EXECUTION]** Verify fidelity index covers lines 1-1364 with 100% coverage (SC-5, FR-TDD-R.7a)
4. **[EXECUTION]** Verify every block has destination + checksum markers (FR-TDD-R.7b); verify only allowlisted transformations (FR-TDD-R.7c, SC-7); confirm forbidden transformations absent (FR-TDD-R.7d)
5. **[VERIFICATION]** Confirm normalized diff policy (FR-TDD-R.7e): only line-ending/trailing-whitespace normalization allowed
6. **[COMPLETION]** Produce comprehensive audit report with per-block results

**Acceptance Criteria:**
- Fidelity index covers 100% of lines 1-1364 with every block mapped (SC-5, FR-TDD-R.7a)
- Every block has verified destination file and matching checksum markers (FR-TDD-R.7b)
- Only allowlisted transformations (path-reference rewrites per spec Section 12.2) applied (FR-TDD-R.7c)
- No forbidden transformations: no wording edits, header renames, numbering changes, checklist reorder, table schema changes (FR-TDD-R.7d)

**Validation:**
- Manual check: audit report covers all 34 blocks with pass/fail per criterion
- Evidence: linkable artifact produced at intended path

**Dependencies:** T04.06, T03.03
**Rollback:** N/A (read-only audit)

---

### T05.05 -- Sentinel Grep Test Across All Refs Files

| Field | Value |
|---|---|
| Roadmap Item IDs | R-036 |
| Why | SC-8 and FR-TDD-R.7f require zero template sentinel placeholders in any output file. |
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
| Deliverable IDs | D-0027 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0027/evidence.md`

**Deliverables:**
1. Sentinel grep test result confirming zero placeholders

**Steps:**
1. **[PLANNING]** Define sentinel patterns: `{{`, `<placeholder>`, `TODO`, `FIXME`
2. **[PLANNING]** Target all refs files under `src/superclaude/skills/tdd/refs/`
3. **[EXECUTION]** Run `grep -rn '{{' src/superclaude/skills/tdd/refs/`
4. **[EXECUTION]** Run `grep -rn '<placeholder>' src/superclaude/skills/tdd/refs/`
5. **[VERIFICATION]** Both grep commands return empty (zero matches) (SC-8, FR-TDD-R.7f)
6. **[COMPLETION]** Record grep output (empty results) as evidence

**Acceptance Criteria:**
- `grep -rn '{{' src/superclaude/skills/tdd/refs/` returns empty
- `grep -rn '<placeholder>' src/superclaude/skills/tdd/refs/` returns empty
- Zero sentinel placeholders in any refs file (SC-8)
- Evidence records both grep command outputs

**Validation:**
- Manual check: both sentinel grep commands return zero matches
- Evidence: linkable artifact produced at intended path

**Dependencies:** T02.01, T02.02, T02.03, T02.04, T02.05
**Rollback:** N/A (read-only test)

---

### Checkpoint: Phase 5 / Tasks T05.01-T05.05

**Purpose:** Verify sync pipeline and basic fidelity checks pass before proceeding to detailed resolution, count, and parity tests.
**Checkpoint Report Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/CP-P05-T01-T05.md`
**Verification:**
- `make sync-dev` and `make verify-sync` both exit 0
- All 5 dev copy refs files exist
- Full fidelity audit and sentinel test pass
**Exit Criteria:**
- SC-3 (dev refs exist), SC-4 (verify-sync passes), SC-5 (fidelity coverage), SC-8 (no sentinels) confirmed
- Sync pipeline handles refs directory correctly
- No blockers for remaining validation tasks

---

### T05.06 -- Normalized Diff Policy Test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-037 |
| Why | FR-TDD-R.7e requires only line-ending/trailing-whitespace normalization in source-vs-migrated block diffs. Any semantic/textual content drift fails the gate. |
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
| Deliverable IDs | D-0028 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0028/evidence.md`

**Deliverables:**
1. Normalized diff policy test result for all migrated blocks

**Steps:**
1. **[PLANNING]** Identify all migrated blocks and their source line ranges from corrected fidelity index
2. **[PLANNING]** Identify corresponding content in destination refs files
3. **[EXECUTION]** For each migrated block, diff source content against destination content
4. **[EXECUTION]** Classify each diff as: (a) no diff, (b) line-ending/whitespace only, (c) semantic/textual content change
5. **[VERIFICATION]** Confirm all diffs are category (a) or (b) only; any category (c) diff fails the test
6. **[COMPLETION]** Record per-block diff classifications

**Acceptance Criteria:**
- All migrated block diffs classified as either identical or line-ending/whitespace normalization only
- Zero semantic/textual content drift detected across any migrated block
- Policy test covers all blocks in all 5 refs files
- Evidence records per-block diff classification results

**Validation:**
- Manual check: no non-whitespace diffs in any migrated block
- Evidence: linkable artifact produced at intended path

**Dependencies:** T05.04
**Rollback:** N/A (read-only test)

---

### T05.07 -- BUILD_REQUEST Resolution Test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-038 |
| Why | SC-10 requires all 6 updated references in build-request-template.md point to files that exist under src/superclaude/skills/tdd/. |
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
| Deliverable IDs | D-0029 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0029/evidence.md`

**Deliverables:**
1. BUILD_REQUEST resolution test result confirming all 6 references resolve (SC-10)

**Steps:**
1. **[PLANNING]** Load `src/superclaude/skills/tdd/refs/build-request-template.md`
2. **[PLANNING]** Extract all `refs/` path references from the file
3. **[EXECUTION]** For each of the 6 path references, verify target file exists
4. **[EXECUTION]** Confirm no stale section-name references remain
5. **[VERIFICATION]** All 6 references resolve to existing files (SC-10)
6. **[COMPLETION]** Record per-reference resolution status

**Acceptance Criteria:**
- All 6 updated references in build-request-template.md resolve to existing files under `src/superclaude/skills/tdd/`
- Zero stale section-name references remain
- Resolution test covers the complete cross-reference map from spec Section 12.2
- Evidence records each reference and its resolution status

**Validation:**
- Manual check: all 6 references resolve; zero old-style references found
- Evidence: linkable artifact produced at intended path

**Dependencies:** T03.01, T05.01
**Rollback:** N/A (read-only test)

---

### T05.08 -- Agent Prompt Count Audit

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | SC-11 requires refs/agent-prompts.md contains all 8 named agent prompts. |
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
| Deliverable IDs | D-0030 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0030/evidence.md`

**Deliverables:**
1. Agent prompt count audit confirming 8 named prompts present (SC-11)

**Steps:**
1. **[PLANNING]** Define expected prompt names: Codebase, Web, Synthesis, Research Analyst, Research QA, Synthesis QA, Report Validation QA, Assembly
2. **[PLANNING]** Load `src/superclaude/skills/tdd/refs/agent-prompts.md`
3. **[EXECUTION]** Search for each of the 8 named prompts in the file
4. **[EXECUTION]** Count total agent prompt sections
5. **[VERIFICATION]** Confirm all 8 prompts found, count equals 8 (SC-11)
6. **[COMPLETION]** Record per-prompt presence confirmation

**Acceptance Criteria:**
- All 8 named agent prompts found in `src/superclaude/skills/tdd/refs/agent-prompts.md` (SC-11)
- Prompts: Codebase, Web, Synthesis, Research Analyst, Research QA, Synthesis QA, Report Validation QA, Assembly
- No duplicate or unnamed prompts
- Evidence records each prompt name and its presence status

**Validation:**
- Manual check: grep for each prompt name returns a match
- Evidence: linkable artifact produced at intended path

**Dependencies:** T02.01
**Rollback:** N/A (read-only audit)

---

### T05.09 -- Token Count Comparison Pre vs Post Refactor

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | SC-14 requires confirmed token reduction in pre-refactor vs post-refactor SKILL.md to validate NFR-TDD-R.1 invocation efficiency improvement. |
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
| Deliverable IDs | D-0031 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0031/evidence.md`

**Deliverables:**
1. Token count comparison report showing pre-refactor vs post-refactor SKILL.md (SC-14)

**Steps:**
1. **[PLANNING]** Determine token counting method (character-based approximation: chars/4)
2. **[PLANNING]** Obtain pre-refactor SKILL.md size (1,364 lines baseline from T01.01)
3. **[EXECUTION]** Count characters/tokens in post-refactor `src/superclaude/skills/tdd/SKILL.md`
4. **[EXECUTION]** Calculate reduction percentage and absolute token savings
5. **[VERIFICATION]** Confirm post-refactor count is meaningfully lower than pre-refactor (SC-14)
6. **[COMPLETION]** Produce comparison report with pre/post metrics

**Acceptance Criteria:**
- Pre-refactor and post-refactor SKILL.md token counts documented
- Token reduction percentage calculated and recorded
- Post-refactor count is lower than pre-refactor count (SC-14)
- Evidence includes method used for token estimation

**Validation:**
- Manual check: post-refactor SKILL.md is demonstrably smaller
- Evidence: linkable artifact produced at intended path

**Dependencies:** T04.05
**Rollback:** N/A (read-only comparison)

---

### T05.10 -- Behavioral Parity Dry Run

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041 |
| Why | SC-13 requires Stage A/B behavioral parity verified via dry run: Stage A completes through A.7, BUILD_REQUEST generated with correct refs paths, Stage B delegation succeeds. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [███████---] 70% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0032 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0032/evidence.md`

**Deliverables:**
1. Behavioral parity dry run result confirming Stage A/B execution with refactored skill (SC-13)

**Steps:**
1. **[PLANNING]** Design trivial test component for TDD skill invocation
2. **[PLANNING]** Confirm dev copy SKILL.md and refs/ are current (T05.01 sync completed)
3. **[EXECUTION]** Invoke TDD skill on trivial test component
4. **[EXECUTION]** Verify Stage A completes through A.7 with BUILD_REQUEST containing correct refs paths
5. **[VERIFICATION]** Verify Stage B delegation succeeds and deterministic checklist gate expectations match
6. **[COMPLETION]** Document dry run results with stage-by-stage evidence

**Acceptance Criteria:**
- Stage A completes through A.7 with BUILD_REQUEST generated containing `refs/` paths (not old section-name references)
- Stage B delegation to `/task` succeeds without refs-related errors
- Deterministic checklist gate expectations match expected outcomes (SC-13)
- Evidence captures stage-by-stage execution trace

**Validation:**
- Manual check: dry run completes without errors; BUILD_REQUEST contains correct refs paths
- Evidence: linkable artifact produced at intended path

**Dependencies:** T05.01, T05.02
**Rollback:** N/A (dry run does not modify source)

---

### Checkpoint: Phase 5 / Tasks T05.06-T05.10

**Purpose:** Verify all detailed validation tests pass before final spec review.
**Checkpoint Report Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/CP-P05-T06-T10.md`
**Verification:**
- Normalized diff, BUILD_REQUEST resolution, agent prompt count, token comparison, and behavioral parity tests all pass
- SC-7, SC-10, SC-11, SC-13, SC-14 confirmed
- No blocking issues in validation results
**Exit Criteria:**
- All 14 success criteria have been individually verified
- No unresolved test failures
- Ready for final spec review and acceptance

---

### T05.11 -- Command-Level Spec Review via sc:spec-panel

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042 |
| Why | Final architecture/fidelity gap check by running /sc:spec-panel and reflection passes on the release spec to confirm no critical gaps. |
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
| Deliverable IDs | D-0033 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0033/evidence.md`

**Deliverables:**
1. Spec review result from `/sc:spec-panel` confirming no critical architecture/fidelity gaps

**Steps:**
1. **[PLANNING]** Identify release spec at `.dev/releases/backlog/tdd-skill-refactor/tdd-refactor-spec.md`
2. **[PLANNING]** Confirm all prior validation tasks completed
3. **[EXECUTION]** Run `/sc:spec-panel` on the release spec
4. **[EXECUTION]** Run reflection passes on the refactoring results
5. **[VERIFICATION]** Confirm no critical architecture or fidelity gaps found
6. **[COMPLETION]** Document spec review findings

**Acceptance Criteria:**
- `/sc:spec-panel` executed against `.dev/releases/backlog/tdd-skill-refactor/tdd-refactor-spec.md`
- No critical architecture gaps identified
- No critical fidelity gaps identified
- Review results documented with any advisory findings noted

**Validation:**
- Manual check: spec review reports no critical gaps
- Evidence: linkable artifact produced at intended path

**Dependencies:** T05.04, T05.10
**Rollback:** N/A (read-only review)

---

### Checkpoint: End of Phase 5

**Purpose:** Final gate confirming all 14 success criteria pass and the TDD skill refactoring is complete.
**Checkpoint Report Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/CP-P05-END.md`
**Verification:**
- All 14 success criteria (SC-1 through SC-14) verified and passing
- All 4 cross-cutting gates (A-D) satisfied
- Updated fidelity index committed alongside refactored files
**Exit Criteria:**
- Gate A (Structural completeness): SC-1, SC-2, SC-3 pass
- Gate B (Sync and contract integrity): SC-4, SC-9, SC-10 pass
- Gate C (Fidelity and semantic immutability): SC-5, SC-6, SC-7, SC-8, SC-11, SC-12 pass
- Gate D (Runtime behavioral parity): SC-13, SC-14 pass
