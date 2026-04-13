# Phase 5 -- Sync, Evidence & Commit

Propagate changes through the component sync pipeline, produce evidence report, and commit as a single atomic unit. This phase transforms canonical source edits into deployable dev copies and produces the final compliance record.

---

### T05.01 -- Run `make sync-dev` to Propagate Changes

| Field | Value |
|---|---|
| Roadmap Item IDs | R-019 |
| Why | The component sync pipeline must propagate `src/superclaude/commands/tdd.md` to `.claude/commands/sc/tdd.md` and SKILL.md changes to `.claude/skills/tdd/SKILL.md`. Dev copies are derived artifacts -- never manually created. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███-------] 35% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0019/evidence.md

**Deliverables:**
- `make sync-dev` terminal output confirming successful propagation of `src/superclaude/commands/tdd.md` to `.claude/commands/sc/tdd.md` and `src/superclaude/skills/tdd/SKILL.md` to `.claude/skills/tdd/SKILL.md`

**Steps:**
1. **[PLANNING]** Confirm Phase 4 hard gate passed (all verification checks)
2. **[PLANNING]** Verify `src/superclaude/` contains the expected changes from Phases 2-3
3. **[EXECUTION]** Run `make sync-dev` from repository root
4. **[EXECUTION]** Capture terminal output for evidence
5. **[VERIFICATION]** Confirm command exits successfully and propagation completed
6. **[COMPLETION]** Record output in D-0019 artifact

**Acceptance Criteria:**
- `make sync-dev` exits with code 0
- `.claude/commands/sc/tdd.md` exists after sync
- `.claude/skills/tdd/SKILL.md` reflects the post-migration state
- Terminal output captured in evidence artifact

**Validation:**
- Manual check: `make sync-dev` exit code is 0
- Evidence: linkable artifact produced at D-0019/evidence.md

**Dependencies:** T04.06 (Phase 4 hard gate cleared)
**Rollback:** Re-run `make sync-dev` after fixing source files
**Notes:** No tier keywords matched in roadmap text; STANDARD assigned by default with low confidence. SC-12 coverage.

---

### T05.02 -- Run `make verify-sync` and Confirm Exit Code 0

| Field | Value |
|---|---|
| Roadmap Item IDs | R-020 |
| Why | SC-12: `make verify-sync` validates parity between `src/superclaude/` and `.claude/`. Must exit 0 before commit. |
| Effort | XS |
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
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0020/evidence.md

**Deliverables:**
- `make verify-sync` terminal output with exit code 0 confirming `src/` and `.claude/` parity

**Steps:**
1. **[PLANNING]** Confirm T05.01 `make sync-dev` completed successfully
2. **[PLANNING]** Define pass criteria: exit code 0
3. **[EXECUTION]** Run `make verify-sync` from repository root
4. **[EXECUTION]** Capture exit code and terminal output
5. **[VERIFICATION]** Confirm exit code is 0 (parity validated)
6. **[COMPLETION]** Record output in D-0020 artifact

**Acceptance Criteria:**
- `make verify-sync` exits with code 0
- No sync drift detected between `src/superclaude/` and `.claude/`
- Terminal output captured with pass/fail indication
- If exit code != 0: error details recorded for corrective action

**Validation:**
- Manual check: `make verify-sync` exit code is 0
- Evidence: linkable artifact produced at D-0020/evidence.md

**Dependencies:** T05.01
**Rollback:** TBD
**Notes:** Read-only verification. SC-12 coverage. Must pass before commit.

---

### T05.03 -- Verify Both Canonical and Dev-Copy File Locations Exist

| Field | Value |
|---|---|
| Roadmap Item IDs | R-021 |
| Why | SC-1: the command file must exist at both `src/superclaude/commands/tdd.md` (canonical) and `.claude/commands/sc/tdd.md` (dev copy) for correct operation. |
| Effort | XS |
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
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0021/evidence.md

**Deliverables:**
- File existence verification confirming `test -f` passes for both `src/superclaude/commands/tdd.md` and `.claude/commands/sc/tdd.md`

**Steps:**
1. **[PLANNING]** Define both file paths to check
2. **[PLANNING]** Define pass criteria: both files exist
3. **[EXECUTION]** Run `test -f src/superclaude/commands/tdd.md` and record result
4. **[EXECUTION]** Run `test -f .claude/commands/sc/tdd.md` and record result
5. **[VERIFICATION]** Confirm both tests pass (exit code 0)
6. **[COMPLETION]** Record evidence in D-0021 artifact

**Acceptance Criteria:**
- `test -f src/superclaude/commands/tdd.md` exits with code 0
- `test -f .claude/commands/sc/tdd.md` exits with code 0
- Both files are non-empty (non-zero byte size)
- Results documented in evidence artifact

**Validation:**
- Manual check: `test -f` on both paths exits 0
- Evidence: linkable artifact produced at D-0021/evidence.md

**Dependencies:** T05.01
**Rollback:** TBD
**Notes:** Read-only verification. SC-1 coverage.

---

### T05.04 -- Final Validation Pass on Dev Copies

| Field | Value |
|---|---|
| Roadmap Item IDs | R-022 |
| Why | Dev copies in `.claude/` are what Claude Code reads at runtime. Key Phase 4 checks must be repeated on dev copies to ensure sync pipeline preserved content integrity. |
| Effort | XS |
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
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0022/evidence.md

**Deliverables:**
- Validation evidence from repeating key Phase 4 checks on `.claude/commands/sc/tdd.md` and `.claude/skills/tdd/SKILL.md` (dev copies)

**Steps:**
1. **[PLANNING]** Select key checks to repeat: line count, zero-leakage grep, activation correctness, migrated content presence
2. **[PLANNING]** Target dev copy paths: `.claude/commands/sc/tdd.md` and `.claude/skills/tdd/SKILL.md`
3. **[EXECUTION]** Run `wc -l .claude/commands/sc/tdd.md` (expect [100, 170]); grep for prohibited keywords (expect 0 matches)
4. **[EXECUTION]** Grep `.claude/commands/sc/tdd.md` for `Skill tdd`; grep for migrated example distinctive strings (expect matches)
5. **[VERIFICATION]** Confirm all repeated checks pass on dev copies matching canonical results
6. **[COMPLETION]** Record evidence in D-0022 artifact

**Acceptance Criteria:**
- `.claude/commands/sc/tdd.md` line count within [100, 170]
- Zero protocol leakage in dev copy (grep for `Stage A`, `Stage B`, `rf-task-builder`, `subagent` returns 0)
- `Skill tdd` present in dev copy Activation section
- Migrated content present in dev copy (matching T04.01 checks)

**Validation:**
- Manual check: dev copy checks produce same pass results as canonical checks
- Evidence: linkable artifact produced at D-0022/evidence.md

**Dependencies:** T05.01
**Rollback:** TBD
**Notes:** Read-only verification. Repeats key Phase 4 checks on `.claude/` dev copies.

---

### T05.05 -- Produce Conditional Evidence Report

| Field | Value |
|---|---|
| Roadmap Item IDs | R-023 |
| Why | This refactor pattern will repeat for other skills (PRD, design, etc.). An evidence report mapping SC and FR/NFR to verification results serves as a reusable template for subsequent refactors. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████-----] 50% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0023 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0023/spec.md

**Deliverables:**
- Evidence report mapping all 12 success criteria (SC-1 through SC-12) and all FR/NFR requirements to their verification task IDs and pass/fail results

**Steps:**
1. **[PLANNING]** Collect all verification results from Phases 2-5 (D-0006 through D-0022)
2. **[PLANNING]** Map each SC (SC-1 through SC-12) and each FR/NFR to its verification task
3. **[EXECUTION]** Build SC-to-task-to-result mapping table from roadmap Section 5 success criteria
4. **[EXECUTION]** Build FR/NFR-to-task-to-result mapping table from phase requirement coverage annotations
5. **[VERIFICATION]** Confirm every SC and FR/NFR has at least one verification task with a result
6. **[COMPLETION]** Write evidence report to D-0023 artifact

**Acceptance Criteria:**
- File `.dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0023/spec.md` exists with SC and FR/NFR mapping tables
- All 12 success criteria (SC-1 through SC-12) mapped to verification tasks
- All FR-TDD-CMD and NFR-TDD-CMD requirements mapped to verification tasks
- Report usable as template for subsequent skill refactors (PRD, design, etc.)

**Validation:**
- Manual check: evidence report covers all 12 SCs and all FR/NFR requirements with task references
- Evidence: linkable artifact produced at D-0023/spec.md

**Dependencies:** T04.01 through T05.04 (all verification results needed)
**Rollback:** TBD
**Notes:** Conditional per roadmap: recommended when pattern will repeat. Algorithm classified EXEMPT due to *.md path booster; flagged for confirmation.

---

### Checkpoint: Phase 5 / Tasks 1-5

**Purpose:** Interim gate confirming sync pipeline succeeded and dev copies validated before commit.
**Checkpoint Report Path:** .dev/releases/current/v3.66-tdd-skill-refactor-v2/checkpoints/CP-P05-T01-T05.md

**Verification:**
- `make sync-dev` and `make verify-sync` both exited with code 0 (T05.01, T05.02)
- Both file locations confirmed to exist (T05.03)
- Dev copy validation checks pass (T05.04)

**Exit Criteria:**
- D-0019 through D-0023 artifacts exist at intended paths
- Sync pipeline confirmed operational
- Dev copies validated against key Phase 4 checks

---

### T05.06 -- Commit as Single Atomic Commit

| Field | Value |
|---|---|
| Roadmap Item IDs | R-024 |
| Why | Roadmap Architect Recommendation #5: this is an atomic refactoring. Command creation and content migration are logically one change. Ship as one commit for clean `git bisect` and `git revert`. |
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
| Deliverable IDs | D-0024 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0024/evidence.md

**Deliverables:**
- Single atomic git commit with message: `refactor(tdd): create command layer and migrate interface content from SKILL.md`

**Steps:**
1. **[PLANNING]** Confirm all Phase 5 prerequisites passed (T05.01-T05.05)
2. **[PLANNING]** Identify all changed files for staging: `src/superclaude/commands/tdd.md` (new), `src/superclaude/skills/tdd/SKILL.md` (modified), `.claude/commands/sc/tdd.md` (new via sync), `.claude/skills/tdd/SKILL.md` (modified via sync)
3. **[EXECUTION]** Stage all changed files: `git add` the 4 affected files
4. **[EXECUTION]** Commit with message: `refactor(tdd): create command layer and migrate interface content from SKILL.md`
5. **[VERIFICATION]** Verify commit created successfully with `git log --oneline -1`
6. **[COMPLETION]** Record commit hash and evidence in D-0024 artifact

**Acceptance Criteria:**
- Git commit created with message `refactor(tdd): create command layer and migrate interface content from SKILL.md`
- Commit includes exactly 4 files: 2 canonical sources + 2 dev copies
- `git log --oneline -1` shows the expected commit message
- No extraneous files included in the commit

**Validation:**
- Manual check: `git log --oneline -1` output matches expected commit message
- Evidence: linkable artifact produced at D-0024/evidence.md

**Dependencies:** T05.01 through T05.05
**Rollback:** `git revert HEAD`
**Notes:** Single atomic commit per Architect Recommendation #5. EXEMPT tier via git operation keyword. SC-12 coverage.

---

### Checkpoint: End of Phase 5

**Purpose:** Final gate confirming sync pipeline, evidence report, and atomic commit all completed successfully. This is the terminal checkpoint for the entire tasklist.
**Checkpoint Report Path:** .dev/releases/current/v3.66-tdd-skill-refactor-v2/checkpoints/CP-P05-END.md

**Verification:**
- `make sync-dev` and `make verify-sync` passed (T05.01, T05.02)
- Both file locations exist with validated content (T05.03, T05.04)
- Atomic commit created with correct message and file set (T05.06)

**Exit Criteria:**
- D-0019 through D-0024 artifacts exist at intended paths
- All 12 success criteria (SC-1 through SC-12) satisfied across Phases 2-5
- Single atomic commit recorded in git history
