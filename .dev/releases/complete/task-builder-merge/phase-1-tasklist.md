# Phase 1 -- M1 Architectural Surface + TB-Add Gates

**Phase Goal:** Establish the M1 architectural-surface checkpoint (COMP-001..006 modification points + contract-freeze for DM-001..005 / API-001..004 / NFR-CONV.5 no-new-deps); append 8 strictly-additive structural checks (TB-Add-1..8) to rf-qa task-integrity gate mirrored across `rf-qa.md` 20-item checklist, `SKILL.md` A.10 9-item block, and `SKILL.md` 15-item validation block; preserve zero-trust QA invariant; resolve INV-015 evidence-bound-item probe via TB-Add-8. Duration: 2 weeks (2026-05-15 → 2026-05-29). Exit: `make verify-sync` PASS; no existing rf-qa check renamed/renumbered/removed.

### T01.01 -- Ratify COMP-001..006 architectural surface map

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002, R-003, R-004, R-005, R-006 |
| Why | Single-page anchor enumerating the 6 modification points (TDD §6.2) ratified at the M1 boundary; provides change-detection surface for all downstream FRs. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting, end-to-end |
| Tier | STRICT |
| Confidence | [█████████-] 92% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0001/spec.md`
- `TASKLIST_ROOT/artifacts/D-0001/notes.md`
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md`

**Deliverables:**
- COMP-001..006 surface-map document listing each anchor's `type`, `location`, `modifies`, and preservation constraints.
- Cross-reference table from FR-CONV.1..6 to the COMP-### anchors they touch.
- NO-DRIFT verification statement for COMP-006 (`rf-team-lead.md:417`).

**Steps:**
1. **[PLANNING]** Load roadmap M1 rows 1-6 and cross-reference TDD §6.2 architectural-surface map.
2. **[PLANNING]** Confirm Q-DM-1 resolution is recorded; flag if still open.
3. **[EXECUTION]** Author the surface-map document with the 6 COMP-### anchors and their full metadata as stated in R-001..R-006.
4. **[EXECUTION]** Cross-link each COMP-### entry to the downstream FR-CONV.X that modifies it.
5. **[VERIFICATION]** Re-grep `rf-team-lead.md:417` to confirm NO DRIFT vs the 2026-05-14 baseline.
6. **[COMPLETION]** Write the ratified map to `TASKLIST_ROOT/artifacts/D-0001/spec.md` and link it from execution-log.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0001/spec.md` exists and lists all 6 COMP-001..006 anchors with `location` matching `src/superclaude/skills/task-builder/SKILL.md` and the four `src/superclaude/agents/rf-*.md` paths.
- `grep -n "417" src/superclaude/agents/rf-team-lead.md` returns the existing all-agents-fail escalation line and its byte-content matches the 2026-05-14 NO-DRIFT baseline.
- Surface-map document explicitly forbids `direct-rf-team-lead-invocation` for COMP-001 and labels COMP-006 as `preservation-only`.
- Document recorded in execution-log.md with the M1 contract-freeze ratification timestamp.

**Validation:**
- Manual check: reviewer confirms the COMP-001..006 map is the single authority for the surface-anchor table and that downstream FR-CONV.X rows reference it.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0001/spec.md` plus NO-DRIFT diff output for `rf-team-lead.md:417`.

**Dependencies:** Q-DM-1 resolved
**Rollback:** As stated in roadmap (M1 surface-map is metadata-only; rolling back means removing the ratification entry from execution-log)
**Notes:** Critical-path override applied because COMP-006 preservation guard governs all downstream FR-CONV.6 behavior.

### T01.02 -- Land FR-CONV.1 TB-Add wrapper across three definition surfaces

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | FR-CONV.1 is the umbrella adding TB-Add-1..8 strictly-additive structural checks; mirroring across rf-qa.md 20-item checklist, SKILL.md A.10 9-item block, and SKILL.md 15-item validation block preserves the three definition surfaces. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting, dependencies |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0002/spec.md`
- `TASKLIST_ROOT/artifacts/D-0002/notes.md`
- `TASKLIST_ROOT/artifacts/D-0002/evidence.md`

**Deliverables:**
- FR-CONV.1 wrapper landed in `rf-qa.md` task-integrity 20-item checklist and SKILL.md A.10 9-item block and SKILL.md 15-item validation block.
- Verbatim TB-Add-1..8 stubs appended on each of the three surfaces with unique TB-Add-N item-IDs.
- Diff evidence showing zero existing rf-qa check was renamed/renumbered/removed.

**Steps:**
1. **[PLANNING]** Confirm T01.01 surface map ratified; load TB-Add-1..8 specifications from R-008..R-015.
2. **[PLANNING]** Locate the three definition surfaces in `src/superclaude/agents/rf-qa.md` and `src/superclaude/skills/task-builder/SKILL.md`.
3. **[EXECUTION]** Append TB-Add-1..8 stubs to the rf-qa.md 20-item task-integrity checklist.
4. **[EXECUTION]** Mirror the same TB-Add-1..8 stubs to SKILL.md A.10 9-item block and SKILL.md 15-item validation block.
5. **[VERIFICATION]** Diff the three definition surfaces vs baseline; assert pre-existing checks have byte-identical content.
6. **[COMPLETION]** Run `make verify-sync` and attach output to evidence.

**Acceptance Criteria:**
- `grep -c "TB-Add-[1-8]" src/superclaude/agents/rf-qa.md` returns at least 8 unique TB-Add identifiers in the task-integrity section.
- `grep -c "TB-Add-[1-8]" src/superclaude/skills/task-builder/SKILL.md` returns at least 16 matches (8 stubs × 2 mirror surfaces A.10 + 15-item).
- Diff against pre-edit baseline shows zero renumbering or renaming of existing rf-qa check IDs.
- `make verify-sync` exits 0 after the change.
- Diff confirms no bundle-specific tasklist-only checks introduced (R-007 invariant).

**Validation:**
- Manual check: reviewer confirms the TB-Add-1..8 stubs appear on all three definition surfaces and TB-Add-2 carries the `[ADVISORY]` prefix.
- Evidence: linkable artifact at `TASKLIST_ROOT/artifacts/D-0002/evidence.md` including the three-surface diff and `make verify-sync` log.

**Dependencies:** T01.01
**Rollback:** As stated in roadmap (per-TB-Add revertable line discipline; remove the FR-CONV.1 wrapper stubs)
**Notes:** Strictly-additive per A-002; no existing item renamed.

### T01.03 -- Implement TB-Add-1 placeholder-scan check (Hard, blocking)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | Detect `TBD`/`TODO`/title-only checklist items; emits item-ID-naming error on violation and blocks gate. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0003/spec.md`
- `TASKLIST_ROOT/artifacts/D-0003/evidence.md`

**Deliverables:**
- TB-Add-1 placeholder-scan check live in rf-qa.md task-integrity gate.
- Item-ID-naming error template invoked when `TBD`/`TODO`/title-only patterns are detected.
- Verdict gate FAIL on violation.

**Steps:**
1. **[PLANNING]** Read TB-Add-1 specification at R-008 and TEST-001 fixture expectations at R-025.
2. **[PLANNING]** Identify the rf-qa.md task-integrity insertion point appended by T01.02.
3. **[EXECUTION]** Replace the TB-Add-1 stub with the active placeholder-scan rule using only Read/Grep/Glob/Bash tooling.
4. **[EXECUTION]** Wire the item-ID-naming-error emission template.
5. **[VERIFICATION]** Run the TEST-001 placeholder fixture; assert TB-Add-1 fires and gate verdict is FAIL.
6. **[COMPLETION]** Append PASS/FAIL evidence to `TASKLIST_ROOT/artifacts/D-0003/evidence.md`.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_placeholder_tb_add_1.py -v` exits 0 with TB-Add-1 fixture asserting gate FAIL.
- Gate report contains item-ID-naming error citing source-check-ID `TB-Add-1`.
- No new external dependency introduced (NFR-CONV.5 diff inspection).
- Evidence written to `TASKLIST_ROOT/artifacts/D-0003/evidence.md`.

**Validation:**
- Manual check: reviewer confirms a fixture with `TBD` literal in an item line triggers FAIL with citation.
- Evidence: linkable test log produced by the TEST-001 fixture.

**Dependencies:** T01.02
**Rollback:** As stated in roadmap (per-line revert)
**Notes:** None.

### T01.04 -- Implement TB-Add-2 item-count bounds advisory check

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | Bounds check `≥3 / ≤40-track / ≤50-single-track`; emits `[ADVISORY]` prefix and does NOT block gate pending OPEN-INV-006 calibration. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0004/spec.md`
- `TASKLIST_ROOT/artifacts/D-0004/evidence.md`

**Deliverables:**
- TB-Add-2 item-count bounds advisory check live in rf-qa.md task-integrity gate.
- `[ADVISORY]` prefix emitted; gate verdict NOT affected.
- ADVISORY-until-Phase-2 status flagged in OPEN-INV-006 tracking.

**Steps:**
1. **[PLANNING]** Read TB-Add-2 advisory specification at R-009.
2. **[PLANNING]** Confirm `[ADVISORY]` prefix is documented as gate-non-blocking.
3. **[EXECUTION]** Implement the bounds check as a counting rule on the checklist items.
4. **[EXECUTION]** Emit `[ADVISORY]` prefix on out-of-bounds without affecting gate verdict.
5. **[VERIFICATION]** Run an out-of-bounds fixture; assert `[ADVISORY]` is emitted AND gate verdict remains PASS.
6. **[COMPLETION]** Document the OPEN-INV-006 calibration dependency in evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_item_count_advisory.py -v` exits 0; fixture asserts `[ADVISORY]` prefix and unchanged gate verdict.
- Gate verdict is NOT affected by TB-Add-2 emission on out-of-bounds fixtures.
- TB-Add-2 emission carries the literal `[ADVISORY]` prefix.
- Evidence written to `TASKLIST_ROOT/artifacts/D-0004/evidence.md` referencing OPEN-INV-006.

**Validation:**
- Manual check: reviewer confirms TB-Add-2 stays advisory until Phase-2 OPEN-INV-006 calibration completes.
- Evidence: linkable test log.

**Dependencies:** T01.02
**Rollback:** As stated in roadmap
**Notes:** Tier conflict: STRICT (security keywords absent) vs STANDARD — resolved to STANDARD by priority rule.

### T01.05 -- Implement TB-Add-3 clarification-adjacency check (Hard, blocking)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | Detect items requiring clarification that are not adjacent to their resolving context; blocks gate on violation. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0005/spec.md`
- `TASKLIST_ROOT/artifacts/D-0005/evidence.md`

**Deliverables:**
- TB-Add-3 clarification-adjacency check live.
- Item-ID-naming error citing non-adjacent clarification.
- Gate verdict FAIL on violation.

**Steps:**
1. **[PLANNING]** Read TB-Add-3 specification at R-010.
2. **[PLANNING]** Identify how clarification items are marked in MDTM (e.g., title prefix `Clarify:`).
3. **[EXECUTION]** Implement adjacency check ensuring clarification items immediately precede the blocked item.
4. **[EXECUTION]** Emit named item-ID on violation.
5. **[VERIFICATION]** Run a non-adjacent clarification fixture; assert FAIL.
6. **[COMPLETION]** Append evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_clarification_adjacency.py -v` exits 0; fixture asserts FAIL on non-adjacent clarification.
- Gate report names the offending item ID.
- TB-Add-3 source-check-ID present in the error citation.
- Evidence written to `TASKLIST_ROOT/artifacts/D-0005/evidence.md`.

**Validation:**
- Manual check: reviewer confirms an adjacent clarification fixture passes while a non-adjacent fails.
- Evidence: linkable test log.

**Dependencies:** T01.02
**Rollback:** As stated in roadmap
**Notes:** None.

### T01.06 -- Checkpoint: Phase 1 / Tasks T01.01-T01.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002, R-003, R-004, R-005, R-006, R-007, R-008, R-009, R-010 |
| Why | Gate: verify outputs of tasks T01.01-T01.05 before continuing. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP01-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md`

**Purpose:** Verify COMP-001..006 surface-map ratified, FR-CONV.1 wrapper landed, and TB-Add-1..3 checks operational before proceeding to remaining TB-Add additions.

**Verification:**
- COMP-001..006 surface-map document at `TASKLIST_ROOT/artifacts/D-0001/spec.md` is present and complete.
- TB-Add-1..3 fixtures (`tests/audit/test_placeholder_tb_add_1.py`, `test_item_count_advisory.py`, `test_clarification_adjacency.py`) all exit 0.
- TB-Add-1..3 stubs present on all 3 surfaces (rf-qa.md + SKILL.md A.10 + SKILL.md 15-item).
- `make verify-sync` PASS after T01.02 wrapper landing.

**Exit Criteria:**
- All 5 regular tasks in this slice report PASS.
- No existing rf-qa check renamed/renumbered/removed across the three surfaces.
- TB-Add-2 confirmed as ADVISORY (non-blocking) on out-of-bounds fixtures.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks (LIGHT inspection of evidence files).
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T01.01-T01.05.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.01..T01.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T01.07 -- Implement TB-Add-4 circular-dependency DAG check (Hard, blocking)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | Detect circular intra-/inter-phase dependencies; blocks gate on violation. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0006/spec.md`
- `TASKLIST_ROOT/artifacts/D-0006/evidence.md`

**Deliverables:**
- TB-Add-4 circular-dependency DAG detector live in rf-qa.md.
- 100% detection on synthetic cycle fixtures.
- Gate verdict FAIL with TB-Add-4 citation on violation.

**Steps:**
1. **[PLANNING]** Read TB-Add-4 specification at R-011 and TEST-002 fixture at R-026.
2. **[PLANNING]** Identify the dependency graph representation in MDTM (Dependencies field).
3. **[EXECUTION]** Implement DAG-cycle detection via topological sort over Dependencies fields.
4. **[EXECUTION]** Emit gate FAIL with TB-Add-4 source-check-ID on cycle detection.
5. **[VERIFICATION]** Run TEST-002 synthetic cycle fixture; assert FAIL.
6. **[COMPLETION]** Append cycle-detection evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_dag_cycle_tb_add_4.py -v` exits 0; fixture asserts FAIL on circular dependency.
- 100% detection rate on synthetic cycle fixtures.
- TB-Add-4 source-check-ID appears in gate report on FAIL.
- Evidence written to `TASKLIST_ROOT/artifacts/D-0006/evidence.md`.

**Validation:**
- Manual check: reviewer confirms an acyclic fixture passes and a cyclic fixture fails.
- Evidence: linkable test log.

**Dependencies:** T01.02
**Rollback:** As stated in roadmap
**Notes:** None.

### T01.08 -- Implement TB-Add-5 granularity/XL-has-subtasks check (Hard, blocking)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | Detect XL-effort items lacking subtask decomposition; blocks gate on violation. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0007/spec.md`
- `TASKLIST_ROOT/artifacts/D-0007/evidence.md`

**Deliverables:**
- TB-Add-5 granularity check live.
- Gate verdict FAIL on XL items without subtasks.
- Item-ID identified in error.

**Steps:**
1. **[PLANNING]** Read TB-Add-5 specification at R-012.
2. **[PLANNING]** Define what "subtask decomposition" means in MDTM (e.g., nested checklist children).
3. **[EXECUTION]** Implement XL-detector scanning the Effort field for XL.
4. **[EXECUTION]** Cross-check that XL items carry a subtask block; emit FAIL otherwise.
5. **[VERIFICATION]** Run XL-without-subtasks fixture; assert FAIL with item-ID named.
6. **[COMPLETION]** Append evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_xl_subtasks_tb_add_5.py -v` exits 0 with XL-without-subtasks fixture asserting FAIL.
- Gate report identifies the offending XL item by ID.
- TB-Add-5 source-check-ID present in error.
- Evidence written to `TASKLIST_ROOT/artifacts/D-0007/evidence.md`.

**Validation:**
- Manual check: reviewer confirms an XL item with subtasks passes and one without fails.
- Evidence: linkable test log.

**Dependencies:** T01.02
**Rollback:** As stated in roadmap
**Notes:** None.

### T01.09 -- Implement TB-Add-6 Confidence/Verification format consistency check

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | Validate per-item Confidence field uses HIGH/MEDIUM/LOW enum with rationale and Verification field is command/inspection/test; blocks gate on violation. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0008/spec.md`
- `TASKLIST_ROOT/artifacts/D-0008/evidence.md`

**Deliverables:**
- TB-Add-6 format consistency check live.
- Format errors named per item-ID.
- Gate verdict FAIL on malformed Confidence or Verification field.

**Steps:**
1. **[PLANNING]** Confirm Q-DM-1 resolved; load the resolved per-item schema (5-field PRD §25.4 OR existing SKILL.md schema).
2. **[PLANNING]** Read TB-Add-6 specification at R-013.
3. **[EXECUTION]** Implement format validators for Confidence (enum) and Verification (command/inspection/test).
4. **[EXECUTION]** Emit per-item-ID format errors on violation.
5. **[VERIFICATION]** Run malformed-Confidence and malformed-Verification fixtures; assert FAIL with item-IDs named.
6. **[COMPLETION]** Append evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_confidence_verification_format.py -v` exits 0; fixtures assert FAIL on malformed fields.
- Each format error in the gate report names a specific item-ID.
- TB-Add-6 source-check-ID present in error.
- Evidence written to `TASKLIST_ROOT/artifacts/D-0008/evidence.md` including the resolved Q-DM-1 schema reference.

**Validation:**
- Manual check: reviewer confirms the active schema matches Q-DM-1 resolution.
- Evidence: linkable test log including the resolved schema citation.

**Dependencies:** T01.02; Q-DM-1
**Rollback:** As stated in roadmap
**Notes:** Confidence reduced to 80% pending Q-DM-1 resolution; Requires Confirmation flagged.

### T01.10 -- Implement TB-Add-7 Execution-Context source-areas cross-validation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | Validate each Source areas entry from the Execution Context header reappears in at least 1 per-item Context field; blocks gate on drift; must tolerate References-only degraded form. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0009/spec.md`
- `TASKLIST_ROOT/artifacts/D-0009/evidence.md`

**Deliverables:**
- TB-Add-7 cross-validation check live.
- Gate verdict FAIL on header source-area absent from items.
- Degraded References-only header tolerated.

**Steps:**
1. **[PLANNING]** Read TB-Add-7 specification at R-014 and DM-001 contract at R-016.
2. **[PLANNING]** Identify the Execution Context header range (post-frontmatter, pre-checklist).
3. **[EXECUTION]** Extract Source areas line and per-item Context fields.
4. **[EXECUTION]** Cross-validate every Source areas entry appears in ≥1 per-item Context.
5. **[VERIFICATION]** Run header-source-area-absent fixture (FAIL) and References-only-degraded fixture (PASS).
6. **[COMPLETION]** Append evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_source_areas_cross_validation.py -v` exits 0 with both fixtures asserting expected verdicts.
- Header-source-area-absent fixture produces gate FAIL with TB-Add-7 citation.
- Degraded References-only fixture produces gate PASS (tolerated).
- Evidence written to `TASKLIST_ROOT/artifacts/D-0009/evidence.md`.

**Validation:**
- Manual check: reviewer confirms degraded References-only header is tolerated.
- Evidence: linkable test log.

**Dependencies:** T01.02; FR-CONV.2 (M2) for full validation
**Rollback:** As stated in roadmap
**Notes:** TB-Add-7 lands in M1 but is also a retroactive consumer of FR-CONV.2 header from M2.

### T01.11 -- Implement TB-Add-8 per-item Context citation check (resolves INV-015)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | Validate per-item Context field has at least one file:line citation OR justified-absence comment; resolves INV-015 evidence-bound-item probe; blocks gate on violation. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0010/spec.md`
- `TASKLIST_ROOT/artifacts/D-0010/evidence.md`

**Deliverables:**
- TB-Add-8 per-item Context citation check live.
- INV-015 evidence-bound-item probe resolved.
- Three-fixture verification (bare-path FAIL, file:line PASS, justified-absence PASS).

**Steps:**
1. **[PLANNING]** Confirm Q-DM-1 resolved; load resolved schema's Context field expectation.
2. **[PLANNING]** Read TB-Add-8 specification at R-015 and TEST-003 three-fixture triple at R-027.
3. **[EXECUTION]** Implement Context-field validator scanning for `file:line` pattern.
4. **[EXECUTION]** Implement justified-absence-comment recognizer.
5. **[VERIFICATION]** Run all three TEST-003 sub-fixtures; assert FAIL/PASS/PASS verdicts.
6. **[COMPLETION]** Document INV-015 resolution in evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_evidence_bound_tb_add_8.py -v` exits 0; three sub-fixtures assert (bare-path FAIL, file:line PASS, justified-absence PASS).
- Gate report cites TB-Add-8 on the bare-path failure.
- INV-015 evidence-bound-item probe documented as resolved.
- Evidence written to `TASKLIST_ROOT/artifacts/D-0010/evidence.md`.

**Validation:**
- Manual check: reviewer confirms the three-fixture triple matches the spec.
- Evidence: linkable test log + INV-015 resolution note.

**Dependencies:** T01.02; Q-DM-1
**Rollback:** As stated in roadmap
**Notes:** Confidence 80% pending Q-DM-1 schema authoritative source.

### T01.12 -- Checkpoint: Phase 1 / Tasks T01.07-T01.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011, R-012, R-013, R-014, R-015 |
| Why | Gate: verify outputs of tasks T01.07-T01.11 before continuing. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP01-MID-T07-T11 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-T07-T11.md`

**Purpose:** Verify TB-Add-4..8 checks are live and pass their synthetic fixtures before proceeding to contract-freeze and migration tasks.

**Verification:**
- TB-Add-4..8 fixtures (DAG cycle, XL subtasks, format consistency, source-areas cross-validation, per-item citation) all exit 0.
- INV-015 evidence-bound-item probe marked resolved by TB-Add-8.
- Q-DM-1 resolution status confirmed for TB-Add-6 and TB-Add-8 gating.

**Exit Criteria:**
- All 5 regular tasks T01.07-T01.11 report PASS.
- Three-fixture TEST-003 triple all pass per spec.
- `make verify-sync` PASS.

**Steps:**
1. **[VERIFICATION]** Confirm each fixture listed in Verification produces the expected verdict.
2. **[VERIFICATION]** Inspect evidence files for the 5 deliverables D-0006..D-0010.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P01-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T01.07-T01.11.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.07..T01.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T01.13 -- Freeze DM-001..005 schemas at M1 boundary

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016, R-017, R-018, R-019, R-020 |
| Why | M1 contract-freeze for the five data-model schemas (Execution Context Header, Inherited Structural Verdict Block, Synthetic DNSP Finding, Per-Item Checklist Schema, Phase Contract); enables change-detection at milestone boundary rather than commit time. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting, schema |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0011/spec.md`
- `TASKLIST_ROOT/artifacts/D-0011/notes.md`
- `TASKLIST_ROOT/artifacts/D-0011/evidence.md`

**Deliverables:**
- DM-001 Execution Context Header schema frozen.
- DM-002 Inherited Structural Verdict Block schema frozen.
- DM-003 Synthetic DNSP Finding schema frozen (7 fields incl. dedup_key + found_n_times).
- DM-004 Per-Item Checklist Schema frozen against Q-DM-1 resolution.
- DM-005 Phase Contract schema frozen (10-field producer/consumer).

**Steps:**
1. **[PLANNING]** Confirm Q-DM-1 resolution recorded; identify the authoritative per-item schema.
2. **[PLANNING]** Read R-016..R-020 schema constraints.
3. **[EXECUTION]** Author each DM-### schema in the M1 contract-freeze document with full field listing.
4. **[EXECUTION]** Cross-reference each DM-### to its consuming FR (DM-001→FR-CONV.2, DM-002→FR-CONV.3, DM-003→FR-CONV.6, DM-004→TB-Add-6/8, DM-005→FR-CONV.3 spawn-prompt).
5. **[VERIFICATION]** Spawn quality-engineer sub-agent to validate all 5 schemas against TDD §6 entity definitions.
6. **[COMPLETION]** Publish `TASKLIST_ROOT/artifacts/D-0011/spec.md` as the M1 contract-freeze artifact.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0011/spec.md` exists and lists all 5 DM-001..005 schemas with full field tables.
- DM-003 schema explicitly enumerates the 7 fields including `dedup_key` (2-tuple `(range, exhaust_point)`) and `found_n_times` (int default 1).
- DM-004 schema names the Q-DM-1-resolved field set and identifies TB-Add-6 and TB-Add-8 as enforcement points.
- DM-002 schema enumerates `rf_qa_table_verbatim`, `prompt_directive` (fixed-string), `reinjection_rule` (INV-002 cycle-N fresh). DM-005 enumerates 10 producer/consumer fields including `schema_version: 1.0.0` and INV-019 Self-Audit obligation.
- Sub-agent quality-engineer report confirms all 5 schemas match the TDD entity definitions.

**Validation:**
- Manual check: reviewer confirms Q-DM-1 resolution is recorded against DM-004.
- Evidence: linkable artifact at `TASKLIST_ROOT/artifacts/D-0011/spec.md` + sub-agent report.

**Dependencies:** T01.01; Q-DM-1
**Rollback:** As stated in roadmap (contract-freeze is a metadata commitment; rollback amends the artifact and re-runs sub-agent verification)
**Notes:** Critical-path override applied because schema changes propagate to all downstream FRs.

### T01.14 -- Freeze API-001..004 contracts at M1 boundary

| Field | Value |
|---|---|
| Roadmap Item IDs | R-021, R-022, R-023, R-024 |
| Why | M1 contract-freeze for the four inter-agent API contracts (BUILD_REQUEST→MDTM, Structural Verdict Handoff, Partition Finding Stream, Fix-Loop Halt Signals); pins consumer/producer wire shapes before per-FR implementation. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0012/spec.md`
- `TASKLIST_ROOT/artifacts/D-0012/notes.md`
- `TASKLIST_ROOT/artifacts/D-0012/evidence.md`

**Deliverables:**
- API-001 BUILD_REQUEST → MDTM contract frozen (15-field schema + EXECUTION_CONTEXT_REQUIREMENTS optional signal).
- API-002 Structural Verdict Handoff contract frozen (spawn-prompt injection mechanics).
- API-003 Partition Finding Stream contract frozen (synthetic DNSP emission stream + dedup).
- API-004 Fix-Loop Halt Signals contract frozen (halt-message ordering rule).

**Steps:**
1. **[PLANNING]** Read R-021..R-024 contract constraints.
2. **[PLANNING]** Identify producer/consumer for each API.
3. **[EXECUTION]** Author each API-### contract spec with transport, payload, and error-mode fields.
4. **[EXECUTION]** Cross-reference to consuming FR milestones (API-001→FR-CONV.2 M2, API-002→FR-CONV.3 M3, API-003→FR-CONV.6 M6, API-004→FR-CONV.5 M5).
5. **[VERIFICATION]** Spawn quality-engineer sub-agent to validate the 4 contracts against TDD §8 API specs.
6. **[COMPLETION]** Publish artifact.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0012/spec.md` exists and lists all 4 API-001..004 contracts with producer/consumer/transport/payload tables.
- API-001 preserves the existing 15-field BUILD_REQUEST schema; EXECUTION_CONTEXT_REQUIREMENTS recorded as optional.
- API-002 records placement-after-TARGET-FILES-before-INSTRUCTIONS and missing-verdict-halt-before-A.10.5. API-003 records all-fail routes to `rf-team-lead.md:417` NO-DNSP.
- API-004 explicitly enumerates the halt-message ordering (regression → monotonicity → hard-cap → proceed).
- Sub-agent quality-engineer report confirms all 4 contracts match TDD §8 API specs.

**Validation:**
- Manual check: reviewer confirms API-001 preservation of 15-field schema.
- Evidence: linkable artifact + sub-agent report.

**Dependencies:** T01.01
**Rollback:** As stated in roadmap
**Notes:** Critical-path override applied because API-002 and API-003 wire shapes govern M3 and M6.

### T01.15 -- Commit TEST-001..003 synthetic fixtures

| Field | Value |
|---|---|
| Roadmap Item IDs | R-025, R-026, R-027 |
| Why | TEST-001 (placeholder), TEST-002 (DAG cycle), TEST-003 (three-fixture evidence-bound triple) are the M1 synthetic fixtures asserting TB-Add-1, TB-Add-4, and TB-Add-8 behavior. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0013/spec.md`
- `TASKLIST_ROOT/artifacts/D-0013/evidence.md`

**Deliverables:**
- TEST-001 placeholder fixture under `tests/audit/`.
- TEST-002 DAG cycle fixture under `tests/audit/`.
- TEST-003 three-fixture evidence-bound triple under `tests/audit/`.

**Steps:**
1. **[PLANNING]** Read R-025..R-027 fixture specs.
2. **[PLANNING]** Identify fixture-data placement under `tests/audit/fixtures/`.
3. **[EXECUTION]** Author TEST-001 placeholder fixture asserting TB-Add-1 emits item-ID-naming error and gate FAILs.
4. **[EXECUTION]** Author TEST-002 DAG cycle fixture asserting 100% TB-Add-4 detection on synthetic cycles.
5. **[EXECUTION]** Author TEST-003 three-fixture triple (bare path FAIL, file:line PASS, justified-absence PASS).
6. **[VERIFICATION]** Run all three fixtures via `uv run pytest tests/audit/ -v`; assert all green.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_placeholder_tb_add_1.py tests/audit/test_dag_cycle_tb_add_4.py tests/audit/test_evidence_bound_tb_add_8.py -v` exits 0.
- TEST-002 detection rate is 100% on the synthetic cycle fixture.
- TEST-003 three sub-fixtures all match the spec (FAIL, PASS, PASS).
- Evidence written to `TASKLIST_ROOT/artifacts/D-0013/evidence.md`.

**Validation:**
- Manual check: reviewer confirms each fixture name matches the roadmap text.
- Evidence: linkable pytest log.

**Dependencies:** T01.03, T01.07, T01.11
**Rollback:** As stated in roadmap
**Notes:** None.

### T01.16 -- Execute MIG-001 PR-06 landing migration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-028 |
| Why | Strictly-additive single commit landing TB-Add-1..8 across the three definition surfaces with per-line revert path documented; `make verify-sync` PASS gate. |
| Effort | M |
| Risk | High |
| Risk Drivers | migration, scope:cross-cutting |
| Tier | STRICT |
| Confidence | [█████████-] 92% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0014/spec.md`
- `TASKLIST_ROOT/artifacts/D-0014/notes.md`
- `TASKLIST_ROOT/artifacts/D-0014/evidence.md`

**Deliverables:**
- Single commit landing FR-CONV.1 (TB-Add-1..8 across 3 surfaces).
- Per-line revert path documented in commit body.
- `make verify-sync` PASS after merge.

**Steps:**
1. **[PLANNING]** Confirm T01.13 + T01.14 contract-freezes ratified and Q-DM-1 resolved.
2. **[PLANNING]** Run `make verify-sync` on the clean baseline; assert PASS.
3. **[EXECUTION]** Stage the TB-Add-1..8 edits across `src/superclaude/agents/rf-qa.md` and `src/superclaude/skills/task-builder/SKILL.md` (3 surface mirror).
4. **[EXECUTION]** Author commit message enumerating per-TB-Add revert lines and citing TEST-001..003 fixture coverage.
5. **[VERIFICATION]** Run `make verify-sync` after commit; assert PASS.
6. **[COMPLETION]** Spawn quality-engineer sub-agent to spot-check the diff for renumbered/renamed existing checks.

**Acceptance Criteria:**
- `make verify-sync` exits 0 immediately after the MIG-001 commit lands.
- Commit body lists 8 per-TB-Add revert lines (one per TB-Add-1..8).
- Sub-agent quality-engineer report confirms zero existing rf-qa check was renamed or renumbered.
- Evidence written to `TASKLIST_ROOT/artifacts/D-0014/evidence.md` referencing the commit SHA.

**Validation:**
- Manual check: reviewer confirms commit body enumerates per-TB-Add revert lines.
- Evidence: `make verify-sync` PASS log + commit diff.

**Dependencies:** T01.02, T01.11, T01.13, T01.14, T01.15
**Rollback:** As stated in roadmap (per-TB-Add line revert OR full commit revert)
**Notes:** Critical-path override applied because MIG-001 is the M1 landing gate for all downstream milestones.

### T01.17 -- Verify NFR-CONV.1 + NFR-CONV.5 audits and FF_TB_ADD governance

| Field | Value |
|---|---|
| Roadmap Item IDs | R-029, R-030, R-031 |
| Why | NFR-CONV.1 byte-identical structural verdict across two runs; NFR-CONV.5 no-new-dependencies diff inspection; FF_TB_ADD_1_THROUGH_8 per-line revertable governance (logical flag, no runtime flag). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0015/spec.md`
- `TASKLIST_ROOT/artifacts/D-0015/evidence.md`

**Deliverables:**
- NFR-CONV.1 two-run determinism diff report (byte-identical structural verdict).
- NFR-CONV.5 diff-inspection audit confirming no new external dependency beyond Read/Grep/Glob/Bash.
- FF_TB_ADD_1_THROUGH_8 governance entry in M7 consolidated table reference.

**Steps:**
1. **[PLANNING]** Read R-029, R-030, R-031 constraints.
2. **[PLANNING]** Identify two BUILD_REQUEST fixtures for the determinism run.
3. **[EXECUTION]** Run TB-Add-1..8 twice on the same BUILD_REQUEST + source tree; diff structural verdicts.
4. **[EXECUTION]** Inspect MIG-001 diff for any new MCP servers, libraries, or synchronous network calls.
5. **[VERIFICATION]** Assert byte-identical structural verdict (diff empty) and zero new deps.
6. **[COMPLETION]** Reference FF_TB_ADD entry in the future M7 consolidated governance table.

**Acceptance Criteria:**
- `diff` of two-run structural verdict outputs is empty (byte-identical).
- Diff inspection of MIG-001 commit reports zero new MCP servers, libraries, or synchronous network calls.
- FF_TB_ADD_1_THROUGH_8 entry recorded in `TASKLIST_ROOT/artifacts/D-0015/spec.md` with cleanup window cross-referenced to M7.
- Evidence written to `TASKLIST_ROOT/artifacts/D-0015/evidence.md` including the determinism diff log.

**Validation:**
- Manual check: reviewer confirms the determinism diff is empty.
- Evidence: linkable diff output + NFR-CONV.5 audit log.

**Dependencies:** T01.16
**Rollback:** As stated in roadmap
**Notes:** None.

### T01.18 -- Checkpoint: End of Phase 1

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002, R-003, R-004, R-005, R-006, R-007, R-008, R-009, R-010, R-011, R-012, R-013, R-014, R-015, R-016, R-017, R-018, R-019, R-020, R-021, R-022, R-023, R-024, R-025, R-026, R-027, R-028, R-029, R-030, R-031 |
| Why | Gate: verify all M1 deliverables (surface map, TB-Add-1..8, DM-001..005 + API-001..004 contract-freezes, TEST-001..003 fixtures, MIG-001 landing, NFR-CONV.1/.5 audits) before unblocking M2. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP01 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-END.md`

**Purpose:** End-of-Phase-1 gate confirming M1 architectural surface ratified, TB-Add catalogue live, contract-freeze artifacts published, MIG-001 merged, and `make verify-sync` PASS — unblocking M2 entry.

**Verification:**
- COMP-001..006 surface-map + DM-001..005 + API-001..004 contract-freeze artifacts at `TASKLIST_ROOT/artifacts/D-0001/`, `D-0011/`, `D-0012/`.
- TB-Add-1..8 active on all three definition surfaces with TEST-001..003 fixtures green.
- MIG-001 landing commit merged with `make verify-sync` PASS evidence in `D-0014/evidence.md`.

**Exit Criteria:**
- All 15 regular tasks T01.01-T01.05, T01.07-T01.11, T01.13-T01.17 report PASS.
- M1 Exit Conditions per roadmap (surface map ratified, contracts frozen, TB-Add fires distinct item-ID errors, TB-Add-2 advisory, 6 fixtures PASS, no existing check renamed) all met.
- TB-Add-2 confirmed emits literal `[ADVISORY]` prefix and does NOT block gate verdict on out-of-bounds fixture.
- NFR-CONV.1 byte-identical determinism diff is empty; NFR-CONV.5 diff inspection finds zero new deps.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present and complete.
2. **[VERIFICATION]** Inspect M1 Exit Conditions checklist; assert every item is satisfied.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above with `Overall: Pass`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P01-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T01.01-T01.17 it covers.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path declares M1 PASS and unblocks M2.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.01..T01.17
**Rollback:** N/A (checkpoints are read-only verifications)
