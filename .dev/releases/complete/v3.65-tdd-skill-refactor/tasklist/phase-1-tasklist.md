# Phase 1 -- Baseline Verification & Line-Range Anchoring

Resolve all open questions, establish verified source ranges, and document the phase loading contract baseline before any content moves. This phase produces the corrected fidelity index with correct line ranges anchored to the spec baseline (1,364) and the documented loading contract for cross-checking during migration.

---

### T01.01 -- Count Actual SKILL.md Lines via wc -l

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | The fidelity index and spec baseline anchor to 1,364 lines. Empirical count must be recorded before content migration begins to detect any discrepancy. |
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
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0001/evidence.md`

**Deliverables:**
1. Recorded SKILL.md line count with comparison against 1,364 baseline

**Steps:**
1. **[PLANNING]** Identify canonical SKILL.md path at `src/superclaude/skills/tdd/SKILL.md`
2. **[PLANNING]** Confirm no pending edits to SKILL.md that would alter line count
3. **[EXECUTION]** Run `wc -l src/superclaude/skills/tdd/SKILL.md` and record output
4. **[EXECUTION]** Compare observed value against 1,364 baseline from spec
5. **[VERIFICATION]** Document any discrepancy with exact delta
6. **[COMPLETION]** Record result in evidence artifact

**Acceptance Criteria:**
- `wc -l src/superclaude/skills/tdd/SKILL.md` output recorded in `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0001/evidence.md`
- Discrepancy (if any) between observed count and 1,364 baseline explicitly documented
- Result is deterministic and repeatable (same file yields same count)
- Evidence artifact includes timestamp and exact command used

**Validation:**
- Manual check: line count recorded and baseline comparison documented
- Evidence: linkable artifact produced at intended path

**Dependencies:** None
**Rollback:** N/A (read-only operation)
**Notes:** Spec cites 1,387 in master prompt vs 1,364 in-repo. GAP-TDD-01 addresses this discrepancy.

---

### T01.02 -- Re-anchor Fidelity Index Block Ranges B01-B34

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | The fidelity index uses a 1,364-line baseline. Every block range must be verified against actual file content to prevent mapping errors during extraction. |
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
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0002/evidence.md`

**Deliverables:**
1. Re-anchored fidelity index with verified block ranges for B01-B34

**Steps:**
1. **[PLANNING]** Load fidelity index from `.dev/releases/backlog/tdd-skill-refactor/fidelity-index.md`
2. **[PLANNING]** Load canonical SKILL.md and T01.01 line count result
3. **[EXECUTION]** For each block B01-B34, verify stated line range against actual content
4. **[EXECUTION]** Verify checksum markers (first 10 / last 10 words) match actual file content at stated ranges
5. **[VERIFICATION]** Record any range mismatches and block migration if discrepancy unresolved
6. **[COMPLETION]** Produce re-anchored fidelity index with verified ranges

**Acceptance Criteria:**
- All 34 blocks (B01-B34) have verified line ranges matching actual `src/superclaude/skills/tdd/SKILL.md` content
- Checksum markers (first 10 / last 10 words per block) confirmed against source
- Any discrepancy between fidelity index ranges and actual content documented with exact delta
- Evidence artifact records block-by-block verification results

**Validation:**
- Manual check: every block range verified against source file content
- Evidence: linkable artifact produced at intended path

**Dependencies:** T01.01
**Rollback:** N/A (read-only analysis)

---

### T01.03 -- Resolve OQ-5: Lines 493-536 Disposition

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | The fidelity index maps B13 as lines 493-510 and B14 as lines 513-535. Lines 511-512 and 536 must be confirmed as blank/separator to ensure no content falls through unmapped. |
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
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0003/evidence.md`

**Deliverables:**
1. OQ-5 resolution document confirming lines 511-512 and 536 content disposition

**Steps:**
1. **[PLANNING]** Identify target lines 493-536 in `src/superclaude/skills/tdd/SKILL.md`
2. **[PLANNING]** Cross-reference fidelity index B13 (493-510) and B14 (513-535) mappings
3. **[EXECUTION]** Read lines 511-512 and 536 from SKILL.md and classify as blank/separator/content
4. **[EXECUTION]** Confirm no content lines fall through unmapped between B13 and B14
5. **[VERIFICATION]** Verify complete coverage of lines 493-536 with zero unmapped content
6. **[COMPLETION]** Document OQ-5 resolution with line-by-line evidence

**Acceptance Criteria:**
- Lines 511-512 and 536 of `src/superclaude/skills/tdd/SKILL.md` classified with exact content shown
- Zero content lines in 493-536 range are unmapped by fidelity index
- Resolution explicitly states whether B13/B14 boundary is clean (blank separators only)
- Evidence artifact includes verbatim line content for the gap lines

**Validation:**
- Manual check: gap lines verified as blank/separator with no content loss
- Evidence: linkable artifact produced at intended path

**Dependencies:** T01.02
**Rollback:** N/A (read-only analysis)

---

### T01.04 -- Resolve OQ-2: Operational Guidance Range Verification

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | Confirm lines 1246-1364 contain operational guidance content with no gap/overlap versus validation-checklists blocks (B25-B28). Any extension beyond 1364 requires spec amendment. |
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
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0004/evidence.md`

**Deliverables:**
1. OQ-2 resolution confirming operational guidance range and B25-B28 boundary

**Steps:**
1. **[PLANNING]** Identify blocks B25-B28 end range and B29-B34 start range in fidelity index
2. **[PLANNING]** Load lines 1246-1364 from `src/superclaude/skills/tdd/SKILL.md`
3. **[EXECUTION]** Confirm B29-B34 ranges cover lines 1246-1364 with no gap vs B25-B28
4. **[EXECUTION]** Verify no content extends beyond line 1364
5. **[VERIFICATION]** Document boundary between validation-checklists and operational-guidance content
6. **[COMPLETION]** Record OQ-2 resolution with evidence

**Acceptance Criteria:**
- Lines 1246-1364 of `src/superclaude/skills/tdd/SKILL.md` confirmed as operational guidance content
- No gap or overlap between B25-B28 (validation-checklists) and B29-B34 (operational-guidance) ranges
- Any content beyond line 1364 flagged for spec amendment
- Evidence artifact includes boundary line content

**Validation:**
- Manual check: range boundary verified with no gap/overlap
- Evidence: linkable artifact produced at intended path

**Dependencies:** T01.02
**Rollback:** N/A (read-only analysis)

---

### T01.05 -- Resolve OQ-4: Frontmatter Coverage Verification

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Confirm B01 (lines 1-4) covers the full YAML frontmatter block including the closing ---. |
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
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0005/evidence.md`

**Deliverables:**
1. OQ-4 resolution confirming frontmatter block coverage

**Steps:**
1. **[PLANNING]** Identify B01 range (lines 1-4) in fidelity index
2. **[PLANNING]** Load first 10 lines of `src/superclaude/skills/tdd/SKILL.md`
3. **[EXECUTION]** Verify lines 1-4 contain complete YAML frontmatter including opening and closing `---`
4. **[EXECUTION]** Confirm no frontmatter content extends beyond line 4
5. **[VERIFICATION]** Validate B01 fully covers the YAML frontmatter block
6. **[COMPLETION]** Document OQ-4 resolution

**Acceptance Criteria:**
- Lines 1-4 of `src/superclaude/skills/tdd/SKILL.md` shown verbatim with frontmatter boundaries identified
- B01 confirmed as covering complete YAML frontmatter including closing `---`
- No frontmatter content outside B01 range
- Evidence artifact includes verbatim lines 1-4

**Validation:**
- Manual check: frontmatter boundaries verified at lines 1-4
- Evidence: linkable artifact produced at intended path

**Dependencies:** T01.02
**Rollback:** N/A (read-only analysis)

---

### Checkpoint: Phase 1 / Tasks T01.01-T01.05

**Purpose:** Verify all open questions (OQ-2, OQ-4, OQ-5) are resolved and fidelity index ranges are re-anchored before producing the corrected fidelity index.
**Checkpoint Report Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/CP-P01-T01-T05.md`
**Verification:**
- T01.01 line count recorded and compared to 1,364 baseline
- T01.02 all 34 block ranges verified against source
- T01.03/T01.04/T01.05 all OQ resolutions documented with evidence
**Exit Criteria:**
- Zero unresolved open questions in OQ-2, OQ-4, OQ-5
- Fidelity index block ranges match actual file content
- No content lines in gap regions found unmapped

---

### T01.06 -- Document Phase Loading Contract Matrix from Spec Section 5.3

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | The loading contract from spec Section 5.3 must be documented as a verification baseline to cross-check during migration. This captures the contract-first principle. |
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
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0006/spec.md`

**Deliverables:**
1. Phase loading contract matrix transcribed from spec Section 5.3

**Steps:**
1. **[PLANNING]** Load spec Section 5.3 phase contracts YAML from `tdd-refactor-spec.md`
2. **[PLANNING]** Identify all phases: invocation, A.1-A.6, A.7 (orchestrator+builder), A.8, Stage B
3. **[EXECUTION]** Transcribe per-phase declared loads and forbidden loads into matrix format
4. **[EXECUTION]** Validate contract rule: `declared_loads intersect forbidden_loads = empty set` for every phase
5. **[VERIFICATION]** Cross-check matrix against roadmap Phase 1 Task 6 table
6. **[COMPLETION]** Produce loading contract matrix document

**Acceptance Criteria:**
- Phase loading contract matrix at `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0006/spec.md` covering all 6 phases
- Every phase has explicit Phase, Actor, Declared Loads, and Forbidden Loads columns matching the roadmap table schema
- Contract validation rule (`declared_loads intersect forbidden_loads = empty set`) confirmed for all phases
- Matrix content matches spec Section 5.3 `phase_contracts` YAML verbatim

**Validation:**
- Manual check: matrix covers all phases from spec Section 5.3 with no omissions
- Evidence: linkable artifact produced at intended path

**Dependencies:** None
**Rollback:** N/A (documentation artifact)

---

### T01.07 -- Produce Corrected Fidelity Index with Verified Ranges

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | The corrected fidelity index becomes the authoritative mapping for all subsequent phases. Block ranges must be aligned to the spec baseline (1,364). |
| Effort | S |
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
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0007/spec.md`

**Deliverables:**
1. Corrected fidelity index covering lines 1-1364 with verified block ranges and checksum markers

**Steps:**
1. **[PLANNING]** Gather T01.01 line count, T01.02 re-anchored ranges, T01.03-T01.05 OQ resolutions
2. **[PLANNING]** Load existing fidelity index from `.dev/releases/backlog/tdd-skill-refactor/fidelity-index.md`
3. **[EXECUTION]** Produce corrected fidelity index incorporating all verified ranges and OQ resolutions
4. **[EXECUTION]** Ensure 100% coverage of lines 1-1364 with zero unmapped content lines
5. **[VERIFICATION]** Validate corrected index covers all blocks B01-B34 with updated checksum markers
6. **[COMPLETION]** Write corrected fidelity index as authoritative mapping

**Acceptance Criteria:**
- Corrected fidelity index at `.dev/releases/backlog/tdd-skill-refactor/tasklist/artifacts/D-0007/spec.md` covers lines 1-1364
- Every block B01-B34 has destination file, verified line range, and checksum markers (first 10 / last 10 words)
- Zero unmapped content lines (blank/separator lines excluded)
- All OQ resolutions (OQ-1 through OQ-5) reflected in the corrected index

**Validation:**
- Manual check: fidelity index covers 100% of lines 1-1364 with no gaps
- Evidence: linkable artifact produced at intended path

**Dependencies:** T01.01, T01.02, T01.03, T01.04, T01.05, T01.06
**Rollback:** Revert to original fidelity index at `.dev/releases/backlog/tdd-skill-refactor/fidelity-index.md`

---

### Checkpoint: End of Phase 1

**Purpose:** Confirm all baseline verification is complete and the corrected fidelity index is ready to serve as the authoritative mapping for content migration.
**Checkpoint Report Path:** `.dev/releases/backlog/tdd-skill-refactor/tasklist/checkpoints/CP-P01-END.md`
**Verification:**
- Corrected fidelity index covers lines 1-1364 with zero unmapped content lines
- Every block's checksum markers match actual file content at stated ranges
- OQ-1 through OQ-5 all resolved with documented answers
- Phase loading contract matrix documented and available for cross-checking
**Exit Criteria:**
- Phase loading contract matrix documented and available for Phase 4 cross-checking
- No unresolved discrepancies blocking content migration
- Corrected fidelity index committed as authoritative reference for Phases 2-5
