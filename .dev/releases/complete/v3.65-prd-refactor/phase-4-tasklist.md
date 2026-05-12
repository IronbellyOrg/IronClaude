# Phase 4 -- Verification and Commit

Full fidelity verification, component sync, behavioral regression test, and atomic commit. This phase confirms zero content loss, validates all 12 success criteria, syncs to src/superclaude/, and produces a single commit on the feature branch.

---

### T04.01 -- Verify zero content loss across all 32 blocks (FR-PRD-R.7)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | Fidelity verification is the critical quality gate: every line of instructional content from the original 1,373-line SKILL.md must appear in exactly one destination file with zero semantic drift or paraphrasing. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | `[########--]` 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct verification (diff + line-count + index reconciliation) |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0018 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0018/evidence.md`

**Deliverables:**
1. Fidelity verification report confirming all 32 content blocks (B01-B32) from the fidelity index appear in exactly one destination file with combined line count between 1,370 and 1,400

**Steps:**
1. **[PLANNING]** Load fidelity index and build block-to-destination mapping for all 32 blocks
2. **[PLANNING]** Identify verification approach: diff each moved block family against original line ranges
3. **[EXECUTION]** Diff each of 8 agent prompt templates (B14-B21) in `refs/agent-prompts.md` against original SKILL.md lines -- confirm zero content changes
4. **[EXECUTION]** Diff checklists (B24-B27) in `refs/validation-checklists.md`, mapping (B22-B23) in `refs/synthesis-mapping.md`, and BUILD_REQUEST (B11) in `refs/build-request-template.md` against originals -- confirm zero content changes (BUILD_REQUEST: only 6 documented path changes)
5. **[EXECUTION]** Verify all behavioral blocks (B01-B10, B12-B13, B28-B32) remain in SKILL.md line-for-line
6. **[EXECUTION]** Compute combined line count: `wc -l .claude/skills/prd/SKILL.md .claude/skills/prd/refs/*` -- target 1,370-1,400 lines
7. **[VERIFICATION]** Update fidelity index with verified destination for each block
8. **[COMPLETION]** Record all diff outputs and combined line count in evidence artifact

**Acceptance Criteria:**
- `diff` of each of 8 agent prompt templates against original SKILL.md lines shows zero content changes
- `diff` of each checklist/table artifact (refs/validation-checklists.md, refs/synthesis-mapping.md) against original shows zero content changes
- `diff` of BUILD_REQUEST against original shows only the 6 documented SKILL CONTEXT FILE path changes
- Combined line count (`wc -l SKILL.md refs/*`) is between 1,370 and 1,400 lines (original 1,373 lines plus ref file headers)
- Fidelity index updated with confirmed "verified" status for each B01-B32 block

**Validation:**
- Combined `wc -l` of SKILL.md + all refs/ files returns value in range [1370, 1400]
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0018/evidence.md`

**Dependencies:** T03.05 (all Phase 3 restructuring must be complete and line count verified)
**Rollback:** N/A (read-only verification task)

---

### T04.02 -- Run all 12 success criteria checks

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | The 12 success criteria from the roadmap's Success Criteria table provide a comprehensive validation sweep covering line counts, file counts, fidelity, stale refs, loading declarations, cross-refs, token budget, concurrent refs, and behavioral regression. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | `[########--]` 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0019/evidence.md`

**Deliverables:**
1. Success criteria sweep report with pass/fail result for each of the 12 checks

**Steps:**
1. **[PLANNING]** Load the 12 success criteria from the roadmap's Success Criteria table
2. **[EXECUTION]** Execute checks 1-6: `wc -l SKILL.md` (430-500), `ls refs/ | wc -l` (4), combined line count (1,370-1,400), diff agent prompts (zero), diff checklists (zero), diff BUILD_REQUEST (only 6 changes)
3. **[EXECUTION]** Execute checks 7-11: `grep -c '".*section"' SKILL.md` (0), `grep 'refs/' SKILL.md` (A.7 matches), `grep 'refs/agent-prompts.md' refs/build-request-template.md` (match), token estimate (<=2,000 soft), manual concurrent refs inspection (<=2)
4. **[VERIFICATION]** Tally results: all 12 must pass. Criterion #12 result sourced from T04.04 E2E outcome.
5. **[COMPLETION]** Record all 12 check results with exact command outputs in evidence artifact

**Acceptance Criteria:**
- All 12 success criteria checks produce pass results, including criterion #12 behavioral regression
- Each check recorded with exact command output and pass/fail determination
- `grep -c '".*section"' .claude/skills/prd/SKILL.md` returns 0 (criterion #7)
- Evidence report at `.dev/releases/current/v3.8/artifacts/D-0019/evidence.md` contains all 12 results

**Validation:**
- Manual check: all 12 criteria from roadmap's Success Criteria table verified
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0019/evidence.md`

**Dependencies:** T04.01 (fidelity verification must pass first)
**Rollback:** N/A (read-only verification task)

---

### T04.03 -- Run component sync (make sync-dev + make verify-sync)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | Component sync propagates `.claude/skills/prd/` changes to `src/superclaude/skills/prd/` ensuring the source of truth and dev copies match; required before commit. |
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
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0020/evidence.md`

**Deliverables:**
1. Synced `src/superclaude/skills/prd/` directory matching `.claude/skills/prd/` with `make verify-sync` passing

**Steps:**
1. **[PLANNING]** Confirm `.claude/skills/prd/` has all expected files (SKILL.md + 4 refs/ files)
2. **[EXECUTION]** Run `make sync-dev` to propagate `.claude/skills/prd/` to `src/superclaude/skills/prd/`
3. **[EXECUTION]** Run `make verify-sync` to confirm both sides match
4. **[VERIFICATION]** Verify `src/superclaude/skills/prd/refs/` contains all 4 refs/ files: agent-prompts.md, build-request-template.md, synthesis-mapping.md, validation-checklists.md
5. **[COMPLETION]** Record sync and verify-sync output in evidence artifact

**Acceptance Criteria:**
- `make sync-dev` completes without errors
- `make verify-sync` reports all files in sync (exit code 0)
- `ls src/superclaude/skills/prd/refs/` shows exactly 4 files matching `.claude/skills/prd/refs/`
- Evidence recorded with full sync and verify-sync command output

**Validation:**
- `make verify-sync` exits with code 0 (all files in sync)
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0020/evidence.md`

**Dependencies:** T04.02 (success criteria must pass before syncing ensures we only sync verified content)
**Rollback:** Re-run `make sync-dev` after correcting source content

---

### T04.04 -- Execute behavioral regression test (E2E)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-017 |
| Why | The E2E test confirms zero behavioral regression (NFR-PRD-R.4): the refactored skill must produce identical execution behavior to the monolithic version -- Stage A completes, task file created with all prompts baked in, and Stage B produces PRD output. |
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
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0021/evidence.md`

**Deliverables:**
1. E2E regression test transcript showing PRD skill invocation with Stage A completion, task file creation, Stage B completion, and PRD output at expected location

**Steps:**
1. **[PLANNING]** Identify a suitable test product/codebase for PRD skill invocation
2. **[PLANNING]** Define expected outputs: task file with embedded agent prompts, PRD at expected output location
3. **[EXECUTION]** Invoke PRD skill on the test product
4. **[EXECUTION]** Capture execution transcript showing Stage A completion (scope discovery, task file creation) and Stage B completion (delegation to /task)
5. **[VERIFICATION]** Verify: Stage A completes, task file contains all 8 agent prompts baked in, Stage B produces PRD at expected output location, output structure matches pre-refactoring behavior
6. **[VERIFICATION]** (Supplemental) Grep task file for stale references -- informational check, not a required gate
7. **[COMPLETION]** Record full execution transcript and output structure comparison in evidence artifact

**Acceptance Criteria:**
- PRD skill invocation completes Stage A (scope discovery through task file creation) without errors
- Generated task file contains all 8 agent prompt templates baked in (not referencing SKILL.md sections)
- Stage B completes with PRD output written to expected location
- (Supplemental) `grep -c 'section' <task-file>` returns 0 stale references -- informational

**Validation:**
- Manual check: PRD skill produces identical execution behavior (Stage A + Stage B completion) to pre-refactoring baseline
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0021/evidence.md`

**Dependencies:** T04.03 (component sync must complete so both .claude/ and src/ are consistent)
**Rollback:** If regression detected: `git revert` the feature branch commit restores monolithic SKILL.md
**Notes:** Addresses roadmap Risk #4 (builder path resolution failure) and criteria #12 (behavioral regression). Content quality of PRD output is out of scope for this refactoring test.

---

### T04.05 -- Create atomic commit on feature branch

| Field | Value |
|---|---|
| Roadmap Item IDs | R-018 |
| Why | A single atomic commit groups all refactoring changes (SKILL.md modification + 4 new refs/ files + synced src/ files) per Architectural Constraint #6, enabling clean rollback via `git revert`. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | `[#########-]` 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0022/notes.md`

**Deliverables:**
1. Single atomic commit on `refactor/prd-skill-decompose` branch with message `refactor: decompose PRD SKILL.md into behavioral spine + 4 refs/ files`

**Steps:**
1. **[PLANNING]** Verify all expected files are staged: modified SKILL.md, 4 new refs/ files, synced src/ counterparts
2. **[EXECUTION]** Stage all relevant files: `.claude/skills/prd/SKILL.md`, `.claude/skills/prd/refs/agent-prompts.md`, `.claude/skills/prd/refs/build-request-template.md`, `.claude/skills/prd/refs/synthesis-mapping.md`, `.claude/skills/prd/refs/validation-checklists.md`, `src/superclaude/skills/prd/SKILL.md`, `src/superclaude/skills/prd/refs/*`
3. **[EXECUTION]** Create commit with message: `refactor: decompose PRD SKILL.md into behavioral spine + 4 refs/ files`
4. **[VERIFICATION]** `git log -1 --oneline` shows the new commit; `git diff HEAD~1 --stat` shows expected file list
5. **[COMPLETION]** Record commit SHA and file list in notes artifact

**Acceptance Criteria:**
- `git log -1 --format="%s"` returns exactly: `refactor: decompose PRD SKILL.md into behavioral spine + 4 refs/ files`
- `git diff HEAD~1 --stat` shows: Modified: `.claude/skills/prd/SKILL.md`, `src/superclaude/skills/prd/SKILL.md`. Added: `.claude/skills/prd/refs/agent-prompts.md`, `.claude/skills/prd/refs/build-request-template.md`, `.claude/skills/prd/refs/synthesis-mapping.md`, `.claude/skills/prd/refs/validation-checklists.md`, `src/superclaude/skills/prd/refs/agent-prompts.md`, `src/superclaude/skills/prd/refs/build-request-template.md`, `src/superclaude/skills/prd/refs/synthesis-mapping.md`, `src/superclaude/skills/prd/refs/validation-checklists.md`
- Commit is a single atomic commit (not split across multiple commits)
- Rollback path confirmed: `git revert <commit-sha>` would restore monolithic SKILL.md

**Validation:**
- `git log -1 --format="%s"` returns exactly: "refactor: decompose PRD SKILL.md into behavioral spine + 4 refs/ files"
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0022/notes.md`

**Dependencies:** T04.04 (E2E regression must pass before committing)
**Rollback:** `git revert <commit-sha>`
**Notes:** Per roadmap: single commit per Architectural Constraint #6. Do not push to remote without explicit user authorization.

---

### Checkpoint: End of Phase 4

**Purpose:** Confirm all verification passes, component sync succeeds, behavioral regression test passes, and atomic commit is on the feature branch.
**Checkpoint Report Path:** `.dev/releases/current/v3.8/checkpoints/CP-P04-END.md`
**Verification:**
- All 12 success criteria pass (T04.02 evidence)
- `make verify-sync` passes with exit code 0 (T04.03)
- E2E behavioral regression test passes: Stage A + Stage B complete with correct output structure (T04.04)
**Exit Criteria:**
- Single atomic commit exists on `refactor/prd-skill-decompose` branch
- All 4 evidence artifacts produced (fidelity verification, success criteria sweep, sync verification, E2E transcript)
- Risks #4 (builder path resolution) and #7 (spec freshness) retired per roadmap risk burn-down
