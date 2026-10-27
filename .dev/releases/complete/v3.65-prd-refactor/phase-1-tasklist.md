# Phase 1 -- Preparation and Validation

Confirm all prerequisites exist and the implementation environment is stable before content extraction begins. This phase verifies the fidelity index, freezes the SKILL.md baseline, creates the feature branch and refs/ directory, and confirms the reference implementation pattern.

---

### T01.01 -- Verify fidelity index completeness

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | The fidelity index maps all 32 content blocks (B01-B32) to destinations; verifying it before implementation prevents extraction errors and ensures no line range gaps or overlaps exist. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | `[########--]` 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Manual verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0001/evidence.md`

**Deliverables:**
1. Verified fidelity index confirming all 32 blocks (B01-B32) have line ranges, type classifications, destinations, and first/last 10-word markers with no gaps or overlaps

**Steps:**
1. **[PLANNING]** Read `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md` and identify block inventory structure
2. **[PLANNING]** Establish verification criteria: each block needs line range, type, destination, first/last markers
3. **[EXECUTION]** Check that blocks B01 through B32 are present with no missing IDs
4. **[EXECUTION]** Verify line ranges are contiguous (last line of B(N) + 1 = first line of B(N+1) or accounted for by whitespace/heading lines)
5. **[EXECUTION]** Cross-check total line coverage against SKILL.md length (1,373 lines)
6. **[VERIFICATION]** Confirm zero gaps and zero overlaps in line ranges
7. **[COMPLETION]** Record verification result in evidence artifact

**Acceptance Criteria:**
- File `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md` contains entries for all 32 blocks B01-B32 with non-empty line range, type, destination, and marker fields
- No overlapping line ranges between any two blocks
- Combined block line ranges account for all 1,373 lines of SKILL.md with zero unmapped gaps and zero overlaps
- Verification evidence recorded with block count and coverage summary

**Validation:**
- Manual check: each block entry in fidelity-index.md has all 5 required fields populated
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0001/evidence.md`

**Dependencies:** None
**Rollback:** N/A (read-only verification task)
**Notes:** This task addresses the prerequisite check in the roadmap's Phase 1 entry.

---

### T01.02 -- Freeze SKILL.md baseline SHA

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | Recording the baseline SHA ensures implementation proceeds against a known state; any concurrent modifications will be detectable via hash mismatch (addresses Risk #7). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | `[#########-]` 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Manual verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0002/notes.md`

**Deliverables:**
1. Baseline SHA record from `git hash-object .claude/skills/prd/SKILL.md` with confirmation of no pending changes

**Steps:**
1. **[PLANNING]** Identify target file: `.claude/skills/prd/SKILL.md`
2. **[PLANNING]** Check for pending changes on current branch that affect SKILL.md
3. **[EXECUTION]** Run `git hash-object .claude/skills/prd/SKILL.md` to record SHA
4. **[EXECUTION]** Run `git status .claude/skills/prd/SKILL.md` to confirm clean state
5. **[VERIFICATION]** Confirm SHA is a valid 40-character hex string and file is unmodified
6. **[COMPLETION]** Record SHA and status in notes artifact

**Acceptance Criteria:**
- `git hash-object .claude/skills/prd/SKILL.md` produces a 40-character SHA hex string
- `git status` shows no pending modifications to `.claude/skills/prd/SKILL.md`
- SHA value recorded in `.dev/releases/current/v3.8/artifacts/D-0002/notes.md`


**Validation:**
- Manual check: `git hash-object .claude/skills/prd/SKILL.md` returns non-empty SHA
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0002/notes.md`

**Dependencies:** None
**Rollback:** N/A (read-only task)
**Notes:** Addresses roadmap Risk #7 (spec freshness). Implementation must proceed against this exact baseline.

---

### T01.03 -- Create feature branch and refs/ directory

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | A dedicated feature branch isolates the refactoring work, and creating the refs/ directory is a prerequisite for all Phase 2 extraction tasks. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | `[#######---]` 75% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0003/notes.md`

**Deliverables:**
1. Feature branch `refactor/prd-skill-decompose` created from current HEAD with empty `.claude/skills/prd/refs/` directory

**Steps:**
1. **[PLANNING]** Confirm current branch and HEAD commit for branch base
2. **[PLANNING]** Verify `.claude/skills/prd/` exists and is the correct target directory
3. **[EXECUTION]** Run `git checkout -b refactor/prd-skill-decompose`
4. **[EXECUTION]** Create directory `.claude/skills/prd/refs/`
5. **[EXECUTION]** Confirm `src/superclaude/skills/prd/refs/` will be created by `make sync-dev`
6. **[VERIFICATION]** Confirm branch exists via `git branch --show-current` and directory exists via `ls .claude/skills/prd/refs/`
7. **[COMPLETION]** Record branch name and base commit in notes artifact

**Acceptance Criteria:**
- `git branch --show-current` returns `refactor/prd-skill-decompose`
- Directory `.claude/skills/prd/refs/` exists and is empty
- `src/superclaude/skills/prd/refs/` creation via `make sync-dev` confirmed
- Branch is created from current HEAD at time of execution
- Notes artifact records branch name, base commit SHA, and creation timestamp

**Validation:**
- Manual check: `git branch --show-current` returns expected branch name and `ls .claude/skills/prd/refs/` shows empty directory
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0003/notes.md`

**Dependencies:** None
**Rollback:** `git checkout -` and `git branch -d refactor/prd-skill-decompose`
**Notes:** Tier confidence below 80% due to mixed EXEMPT/STANDARD signals (git branch creation is EXEMPT but directory creation is a write operation). Confirm tier is appropriate.

---

### T01.04 -- Verify reference implementation accessibility

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | The sc-adversarial-protocol skill's refs/ directory serves as the architectural pattern to follow; confirming it is readable prevents implementation guesswork. |
| Effort | XS |
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
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.8/artifacts/D-0004/notes.md`

**Deliverables:**
1. Notes documenting the cross-reference syntax pattern used in sc-adversarial-protocol refs/ (e.g., `See refs/filename.md` inline references)

**Steps:**
1. **[PLANNING]** Identify reference implementation: `.claude/skills/sc-adversarial-protocol/refs/`
2. **[PLANNING]** Determine what patterns to observe (file naming, cross-reference syntax)
3. **[EXECUTION]** List files in `.claude/skills/sc-adversarial-protocol/refs/` and read one to note the header/reference pattern
4. **[VERIFICATION]** Confirm the `See refs/...` inline reference pattern is present and documented
5. **[COMPLETION]** Record observed patterns in notes artifact

**Acceptance Criteria:**
- `.claude/skills/sc-adversarial-protocol/refs/` directory is readable and contains refs/ files
- Cross-reference syntax pattern identified and recorded (e.g., `See refs/filename.md`)
- Pattern notes recorded in `.dev/releases/current/v3.8/artifacts/D-0004/notes.md`

**Validation:**
- Manual check: `ls .claude/skills/sc-adversarial-protocol/refs/` returns file listing
- Evidence: linkable artifact produced at `.dev/releases/current/v3.8/artifacts/D-0004/notes.md`

**Dependencies:** None
**Rollback:** N/A (read-only task)

---

### Checkpoint: End of Phase 1

**Purpose:** Confirm all prerequisites are verified and the implementation environment is ready for content extraction.
**Checkpoint Report Path:** `.dev/releases/current/v3.8/checkpoints/CP-P01-END.md`
**Verification:**
- Fidelity index verified complete: all 32 blocks mapped with no line gaps
- SKILL.md baseline SHA recorded and no pending changes detected
- Feature branch created with empty refs/ directory and reference implementation pattern confirmed
**Exit Criteria:**
- All 4 Phase 1 tasks (T01.01-T01.04) completed with deliverables D-0001 through D-0004 produced
- Feature branch `refactor/prd-skill-decompose` is the active branch
- Green light confirmed for Phase 2 content extraction to begin
