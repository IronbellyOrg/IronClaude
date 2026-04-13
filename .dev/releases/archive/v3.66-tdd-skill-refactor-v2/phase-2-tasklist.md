# Phase 2 -- Command File Creation

Create `src/superclaude/commands/tdd.md` following the adversarial.md gold-standard structure with all 10 required sections. Verify the file meets line budget (100-170) and contains zero protocol leakage.

---

### T02.01 -- Create `src/superclaude/commands/tdd.md` Command File

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | Developer Guide Section 9.3 requires every skill to have a command in front of it. The TDD skill currently lacks a command layer, violating this architectural rule. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████----] 50% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0005/spec.md

**Deliverables:**
- Command file `src/superclaude/commands/tdd.md` containing all 10 sections: Frontmatter, Required Input, Usage, Arguments, Options Table (7 flags), Behavioral Summary, Examples (5-6), Activation (`> Skill tdd`), Boundaries (Will/Will Not), Related Commands

**Steps:**
1. **[PLANNING]** Load D-0001 notes (adversarial.md template analysis) for section ordering reference
2. **[PLANNING]** Confirm `src/superclaude/commands/` directory exists and no `tdd.md` already present
3. **[EXECUTION]** Create `src/superclaude/commands/tdd.md` with Frontmatter: `name: tdd`, `description`, `category: documentation`, `complexity: advanced`, `allowed-tools`, `mcp-servers`, `personas`
4. **[EXECUTION]** Add Required Input, Usage (`/sc:tdd <component> [options]`), Arguments (`<component>` positional), Options Table (7 flags: `<component>`, `--tier`, `--prd`, `--resume`, `--output`, `--focus`, `--from-prd`), Behavioral Summary (one paragraph, zero protocol details), Examples (3 strong, 2 weak annotated, 1 resume/tier override), Activation (`> Skill tdd` with "Do NOT proceed" guard), Boundaries (Will/Will Not), Related Commands (`/sc:prd`, `/sc:design`, `/sc:workflow`, `/sc:brainstorm`)
5. **[VERIFICATION]** Run `wc -l src/superclaude/commands/tdd.md` and confirm 100-170 lines
6. **[COMPLETION]** Record creation evidence in D-0005 artifact

**Acceptance Criteria:**
- File `src/superclaude/commands/tdd.md` exists with all 10 sections matching adversarial.md ordering
- Options table contains all 7 flags: `<component>`, `--tier`, `--prd`, `--resume`, `--output`, `--focus`, `--from-prd`
- Activation section contains `> Skill tdd` with "Do NOT proceed" guard (FR-TDD-CMD.1i)
- Line count is between 100 and 170 inclusive (NFR-TDD-CMD.1)

**Validation:**
- Manual check: `wc -l src/superclaude/commands/tdd.md` returns value in range [100, 170]
- Evidence: linkable artifact produced at D-0005/spec.md

**Dependencies:** T01.01 (template analysis), T01.03 (Developer Guide rules)
**Rollback:** `rm src/superclaude/commands/tdd.md`
**Notes:** Tier conflict: *.md path booster pushed EXEMPT, but task is file creation (STANDARD action). Classified EXEMPT by algorithm; flagged for confirmation. FR-TDD-CMD.1a through 1m coverage.

---

### T02.02 -- Verify Command File Line Count (100-170 Lines)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | NFR-TDD-CMD.1 mandates the command file stay within the 100-170 line budget to match the adversarial.md scale. |
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
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0006/evidence.md

**Deliverables:**
- Line count verification evidence showing `wc -l` output for `src/superclaude/commands/tdd.md` in range [100, 170]

**Steps:**
1. **[PLANNING]** Confirm T02.01 completed and command file exists
2. **[PLANNING]** Define acceptance: line count >= 100 AND <= 170
3. **[EXECUTION]** Run `wc -l src/superclaude/commands/tdd.md`
4. **[EXECUTION]** Compare output against [100, 170] range
5. **[VERIFICATION]** Record pass/fail result with actual line count
6. **[COMPLETION]** Record evidence in D-0006 artifact

**Acceptance Criteria:**
- `wc -l src/superclaude/commands/tdd.md` returns a value between 100 and 170 inclusive
- Actual line count recorded in evidence artifact
- Pass/fail determination documented
- If fail: deviation amount noted for corrective action

**Validation:**
- Manual check: `wc -l src/superclaude/commands/tdd.md` output verified against [100, 170]
- Evidence: linkable artifact produced at D-0006/evidence.md

**Dependencies:** T02.01
**Rollback:** TBD
**Notes:** Read-only verification task. NFR-TDD-CMD.1, FR-TDD-CMD.1l coverage.

---

### T02.03 -- Verify Zero Protocol Leakage in Command File

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | NFR-TDD-CMD.2 requires zero protocol leakage. The command must not reference Stage A, Stage B, rf-task-builder, or subagent -- those are skill-layer concerns. |
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
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.66-tdd-skill-refactor-v2/artifacts/D-0007/evidence.md

**Deliverables:**
- Zero-leakage verification evidence showing grep output for prohibited keywords `Stage A`, `Stage B`, `rf-task-builder`, `subagent` returns 0 matches in `src/superclaude/commands/tdd.md`

**Steps:**
1. **[PLANNING]** Define prohibited keywords: `Stage A`, `Stage B`, `rf-task-builder`, `subagent`
2. **[PLANNING]** Confirm T02.01 completed and command file exists
3. **[EXECUTION]** Grep `src/superclaude/commands/tdd.md` for each prohibited keyword
4. **[EXECUTION]** Record match count for each keyword (expected: 0 for all)
5. **[VERIFICATION]** Confirm all 4 grep searches return 0 matches
6. **[COMPLETION]** Record evidence in D-0007 artifact

**Acceptance Criteria:**
- Grep for `Stage A` in `src/superclaude/commands/tdd.md` returns 0 matches
- Grep for `Stage B` returns 0 matches
- Grep for `rf-task-builder` returns 0 matches
- Grep for `subagent` returns 0 matches

**Validation:**
- Manual check: all 4 grep commands return empty results
- Evidence: linkable artifact produced at D-0007/evidence.md

**Dependencies:** T02.01
**Rollback:** TBD
**Notes:** Read-only verification task. NFR-TDD-CMD.2, FR-TDD-CMD.1m coverage.

---

### Checkpoint: End of Phase 2

**Purpose:** Confirm command file created with correct structure, within line budget, and free of protocol leakage before content migration begins.
**Checkpoint Report Path:** .dev/releases/current/v3.66-tdd-skill-refactor-v2/checkpoints/CP-P02-END.md

**Verification:**
- `src/superclaude/commands/tdd.md` exists with all 10 sections in adversarial.md ordering
- Line count within [100, 170] range (NFR-TDD-CMD.1)
- Zero matches for prohibited keywords: `Stage A`, `Stage B`, `rf-task-builder`, `subagent` (NFR-TDD-CMD.2)

**Exit Criteria:**
- D-0005 through D-0007 artifacts exist at intended paths
- Command file structurally complete and verified before content migration
- No protocol leakage detected
