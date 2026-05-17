# Phase 2 -- M2 Execution Context Header

**Phase Goal:** Insert task-level `## Execution Context` block (after frontmatter, before checklist) in generated MDTM task files with exactly three labeled lines (References / Source areas / Key constraints); preserve evidence-bound-item invariant; degrade gracefully to References-only on minimal BUILD_REQUEST. Duration: 2 weeks (2026-05-29 → 2026-06-12). Exit: header renders 3 labeled lines for fully-populated BUILD_REQUEST; degrades to References-only for minimal; `grep -E "src/|/.*:[0-9]+"` against header range returns zero; per-item Context fields retain file:line citations.

### T02.01 -- Land FR-CONV.2 Execution Context header

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032 |
| Why | FR-CONV.2 wrapper inserts the task-level `## Execution Context` block in MDTM template, preserving evidence-bound-item invariant per CASE-D PR-01. |
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
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0016/spec.md`
- `TASKLIST_ROOT/artifacts/D-0016/evidence.md`

**Deliverables:**
- FR-CONV.2 wrapper inserted in MDTM template at SKILL.md + rf-task-builder.md.
- 3-labeled-line block for fully-populated BUILD_REQUEST.
- Per-item Context fields unchanged.

**Steps:**
1. **[PLANNING]** Confirm Phase 1 PASS; DM-001 contract-freeze ratified.
2. **[PLANNING]** Locate MDTM template top in `src/superclaude/skills/task-builder/SKILL.md` post-frontmatter, pre-checklist.
3. **[EXECUTION]** Insert `## Execution Context` block specification into the MDTM template.
4. **[EXECUTION]** Confirm per-item Context fields are untouched.
5. **[VERIFICATION]** Grep generated MDTM for `## Execution Context` heading; assert presence.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "## Execution Context" <generated-mdtm>` returns the block heading line immediately after frontmatter.
- Block contains References, Source areas, Key constraints labeled lines for the fully-populated fixture.
- Per-item Context fields outside the header are unchanged (byte-identical diff outside header range).
- Evidence at `TASKLIST_ROOT/artifacts/D-0016/evidence.md`.

**Validation:**
- Manual check: reviewer confirms the block sits between frontmatter and the first checklist phase.
- Evidence: linkable generated MDTM file.

**Dependencies:** Phase 1 (M1 PASS); DM-001
**Rollback:** As stated in roadmap (disable header generation; per-item Context unchanged)
**Notes:** None.

### T02.02 -- Implement DM-001 emitters (References / SourceAreas / KeyConstraints)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-033, R-034, R-035 |
| Why | DM-001 fields populated from BUILD_REQUEST: References (R-### list), Source areas (no file paths — hidden-input determinism), Key constraints (1-3 entries from BUILD_REQUEST). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0017/spec.md`
- `TASKLIST_ROOT/artifacts/D-0017/evidence.md`

**Deliverables:**
- References emitter producing `R-###: <ref-line>` entries from GOAL/WHY/related_docs.
- Source areas emitter producing module/package names with no file paths.
- Key constraints emitter producing 1-3 entries pulled verbatim from BUILD_REQUEST.

**Steps:**
1. **[PLANNING]** Read R-033, R-034, R-035 emitter specifications.
2. **[PLANNING]** Confirm DM-001 frozen contract (T01.13).
3. **[EXECUTION]** Implement References list emitter in rf-task-builder.md.
4. **[EXECUTION]** Implement Source areas emitter with no-file-paths guard.
5. **[EXECUTION]** Implement Key constraints emitter with 1-3 bounded entries.
6. **[VERIFICATION]** Run `grep -E "src/|/.*:[0-9]+"` against the emitted header range; assert zero hits.

**Acceptance Criteria:**
- `grep -cE "src/|/.*:[0-9]+" <header-range>` returns 0 for the generated header.
- References list is populated as `R-###: <ref-line>` per row from BUILD_REQUEST GOAL/WHY/related_docs.
- Key constraints list has between 1 and 3 entries per BUILD_REQUEST.
- Evidence at `TASKLIST_ROOT/artifacts/D-0017/evidence.md`.

**Validation:**
- Manual check: reviewer confirms no file path leaks into the header.
- Evidence: linkable header sample + grep log.

**Dependencies:** T02.01; DM-001
**Rollback:** As stated in roadmap
**Notes:** None.

### T02.03 -- Update API-001-M2 BUILD_REQUEST contract

| Field | Value |
|---|---|
| Roadmap Item IDs | R-036 |
| Why | Implement EXECUTION_CONTEXT_REQUIREMENTS optional signal in BUILD_REQUEST schema; generated MDTM file MUST contain `## Execution Context` block at top after frontmatter. |
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
| Deliverable IDs | D-0018 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0018/spec.md`
- `TASKLIST_ROOT/artifacts/D-0018/evidence.md`

**Deliverables:**
- API-001-M2 contract update preserving 15-field BUILD_REQUEST schema + adding optional EXECUTION_CONTEXT_REQUIREMENTS signal.
- Emission rule for fully-populated vs minimal BUILD_REQUEST documented.
- MALFORMED retry max-2 failure-mode preserved.

**Steps:**
1. **[PLANNING]** Confirm API-001 contract-freeze (T01.14).
2. **[PLANNING]** Read R-036 implementation constraints.
3. **[EXECUTION]** Add EXECUTION_CONTEXT_REQUIREMENTS optional signal to BUILD_REQUEST schema in SKILL.md.
4. **[EXECUTION]** Document fully-populated vs minimal emission rules.
5. **[VERIFICATION]** Spawn quality-engineer sub-agent to validate the 15-field schema remains intact.
6. **[COMPLETION]** Evidence + sub-agent report.

**Acceptance Criteria:**
- BUILD_REQUEST 15-field schema unchanged (byte-diff zero in the existing 15 fields).
- EXECUTION_CONTEXT_REQUIREMENTS documented as optional in `src/superclaude/skills/task-builder/SKILL.md`.
- MALFORMED retry max-2 failure-mode preserved (verbatim text retained).
- Generated MDTM from updated BUILD_REQUEST contract contains `## Execution Context` block after frontmatter, before first phase (post-update contract-conformance check).
- Sub-agent report confirms producer/consumer/transport unchanged.

**Validation:**
- Manual check: reviewer confirms the optional signal is non-breaking.
- Evidence: sub-agent report + schema diff.

**Dependencies:** T02.01; T01.14
**Rollback:** As stated in roadmap
**Notes:** Critical-path override applied because API-001-M2 is the wire contract.

### T02.04 -- Publish DM-005-M2 Phase Contract row

| Field | Value |
|---|---|
| Roadmap Item IDs | R-037 |
| Why | DM-005 10-field producer/consumer agreement published as standalone row at M2 to enable M3 spawn-prompt injection (rf-qa → rf-qa-qualitative). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0019/spec.md`
- `TASKLIST_ROOT/artifacts/D-0019/evidence.md`

**Deliverables:**
- DM-005 explicit row published in SKILL.md with the 10-field schema.
- Producer/consumer pairing (rf-qa → rf-qa-qualitative) documented.
- schema_version 1.0.0 baseline asserted.

**Steps:**
1. **[PLANNING]** Confirm DM-005 contract-freeze at T01.13.
2. **[PLANNING]** Read R-037 row specification.
3. **[EXECUTION]** Author DM-005 row with all 10 fields (producer, consumer, artifact, schema_version, delivery_semantics, freshness_rule, enumeration_rule, consumer_obligation, anti_inflation, failure_mode).
4. **[VERIFICATION]** Spawn quality-engineer sub-agent to validate the 10-field row against DM-005 contract-freeze.
5. **[VERIFICATION]** Confirm published row is referenced by M3 spawn-prompt injection plan.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "schema_version: 1.0.0" src/superclaude/skills/task-builder/SKILL.md` returns the DM-005 row line.
- All 10 fields present in the published DM-005 row.
- Producer = rf-qa; Consumer = rf-qa-qualitative; explicitly named.
- Sub-agent quality-engineer report confirms field-for-field match against DM-005 frozen contract.

**Validation:**
- Manual check: reviewer confirms the row is standalone (not embedded in another section).
- Evidence: sub-agent report.

**Dependencies:** T01.13; T02.01
**Rollback:** As stated in roadmap
**Notes:** None.

### T02.05 -- Wire degradation rule + hidden-input guard

| Field | Value |
|---|---|
| Roadmap Item IDs | R-038, R-039 |
| Why | Block degrades to References-only when GOAL is the only populated field (other lines explicitly omitted, not blank); header MUST NOT contain specific file paths or `file:line` citations (NFR-CONV.3 hidden-input determinism). |
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
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0020/spec.md`
- `TASKLIST_ROOT/artifacts/D-0020/evidence.md`

**Deliverables:**
- Degradation rule producing References-only header on minimal BUILD_REQUEST.
- Hidden-input guard rejecting any file path or file:line in header.
- TB-Add-7 (M1) cross-validator integration verified.

**Steps:**
1. **[PLANNING]** Read R-038 degradation spec and R-039 hidden-input guard spec.
2. **[PLANNING]** Identify minimal BUILD_REQUEST fixture parameters.
3. **[EXECUTION]** Implement degradation logic: omit Source areas + Key constraints lines on minimal.
4. **[EXECUTION]** Implement no-file-paths guard scanning header range.
5. **[VERIFICATION]** Run minimal-BUILD_REQUEST fixture; assert References-only and absent other lines.
6. **[VERIFICATION]** Run `grep -E "src/|/.*:[0-9]+"` against header; assert 0 hits.

**Acceptance Criteria:**
- Minimal-BUILD_REQUEST fixture generates header with only `References:` line; Source areas and Key constraints lines are absent (not blank-but-present).
- `grep -cE "src/|/.*:[0-9]+" <header-range>` returns 0.
- TB-Add-7 cross-validator tolerates the degraded form (no FAIL emitted).
- Evidence at `TASKLIST_ROOT/artifacts/D-0020/evidence.md`.

**Validation:**
- Manual check: reviewer confirms minimal fixture omits lines (not blanks them).
- Evidence: header sample + grep log.

**Dependencies:** T02.01, T02.02; TB-Add-7 from Phase 1
**Rollback:** As stated in roadmap
**Notes:** None.

### T02.06 -- Checkpoint: Phase 2 / Tasks T02.01-T02.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032, R-033, R-034, R-035, R-036, R-037, R-038, R-039 |
| Why | Gate: verify FR-CONV.2 wrapper, DM-001 emitters, API-001-M2 contract update, DM-005-M2 publication, and degradation/hidden-input guards before SKILL.md template edits. |
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
| Deliverable IDs | D-CP02-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md`

**Purpose:** Mid-phase gate after T02.01-T02.05 verifying header wrapper + DM-001 emitters + contract publication land cleanly.

**Verification:**
- FR-CONV.2 wrapper renders `## Execution Context` block in generated MDTM (D-0016 evidence).
- DM-001 emitter outputs pass the no-file-paths grep (D-0017 evidence).
- API-001-M2 + DM-005-M2 sub-agent reports confirm contract intact (D-0018, D-0019).

**Exit Criteria:**
- All 5 regular tasks T02.01-T02.05 report PASS.
- Degraded References-only fixture produces gate PASS via TB-Add-7 tolerance.
- `grep -cE "src/|/.*:[0-9]+" <header>` returns 0 across all fixtures.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T02.01-T02.05.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.01..T02.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T02.07 -- Edit COMP-001-M2 SKILL.md template + guidance

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040, R-041 |
| Why | Insert Execution Context block specification into MDTM template at SKILL.md:1407-1487 and update BUILD_REQUEST guidance near SKILL.md:715-725 with header generation rules. |
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
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0021/spec.md`
- `TASKLIST_ROOT/artifacts/D-0021/evidence.md`

**Deliverables:**
- Execution Context block inserted at SKILL.md:1407-1487.
- BUILD_REQUEST guidance updated at SKILL.md:715-725 enumerating 3-line vs degraded forms.
- NFR-CONV.3 hidden-input rule cited in guidance.

**Steps:**
1. **[PLANNING]** Confirm T02.01..T02.05 PASS.
2. **[PLANNING]** Read R-040, R-041 edit constraints.
3. **[EXECUTION]** Insert Execution Context spec at lines 1407-1487.
4. **[EXECUTION]** Update BUILD_REQUEST guidance at lines 715-725.
5. **[VERIFICATION]** `grep -n "Execution Context" src/superclaude/skills/task-builder/SKILL.md`; assert presence at expected line range.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "## Execution Context" src/superclaude/skills/task-builder/SKILL.md` returns a line number within 1407-1487.
- BUILD_REQUEST guidance section at 715-725 enumerates the 3-line vs degraded forms verbatim.
- NFR-CONV.3 hidden-input rule referenced by name in the guidance.
- Evidence at `TASKLIST_ROOT/artifacts/D-0021/evidence.md`.

**Validation:**
- Manual check: reviewer confirms line ranges match the spec.
- Evidence: linkable grep output.

**Dependencies:** T02.06
**Rollback:** As stated in roadmap
**Notes:** None.

### T02.08 -- Edit COMP-002-M2 rf-task-builder header emission

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042 |
| Why | Modify rf-task-builder.md to emit `## Execution Context` block at task-file top so generated MDTM contains the header after frontmatter, before Phase 1. |
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
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0022/spec.md`
- `TASKLIST_ROOT/artifacts/D-0022/evidence.md`

**Deliverables:**
- rf-task-builder.md emits Execution Context block after frontmatter, before Phase 1.
- MALFORMED retry max-2 failure-mode preserved.
- Header emission rule documented.

**Steps:**
1. **[PLANNING]** Read R-042 emission logic spec.
2. **[PLANNING]** Locate the rf-task-builder.md task-file template assembly section.
3. **[EXECUTION]** Add header emission step after frontmatter, before checklist.
4. **[EXECUTION]** Preserve MALFORMED retry max-2 failure-mode.
5. **[VERIFICATION]** Generate a sample MDTM; grep for `## Execution Context` and confirm position.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- Generated MDTM contains `## Execution Context` heading after frontmatter and before the first `### T<PP>.<TT>` task.
- MALFORMED retry max-2 failure-mode appears verbatim in rf-task-builder.md.
- Evidence at `TASKLIST_ROOT/artifacts/D-0022/evidence.md`.

**Validation:**
- Manual check: reviewer confirms emission ordering.
- Evidence: sample MDTM file.

**Dependencies:** T02.07
**Rollback:** As stated in roadmap
**Notes:** None.

### T02.09 -- Commit TEST-004..006 fixtures

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043, R-044, R-045 |
| Why | TEST-004 asserts 3-labeled-line block; TEST-005 asserts References-only degradation; TEST-006 asserts grep returns 0 in header range. |
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
| Deliverable IDs | D-0023 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0023/spec.md`
- `TASKLIST_ROOT/artifacts/D-0023/evidence.md`

**Deliverables:**
- TEST-004 fully-populated fixture asserting all 3 labeled lines.
- TEST-005 minimal fixture asserting References-only degradation.
- TEST-006 hidden-input fixture asserting `grep -E "src/|/.*:[0-9]+"` returns 0.

**Steps:**
1. **[PLANNING]** Read R-043, R-044, R-045 fixture specs.
2. **[PLANNING]** Author fixture data under `tests/audit/fixtures/execution_context/`.
3. **[EXECUTION]** Author TEST-004 fully-populated fixture.
4. **[EXECUTION]** Author TEST-005 minimal-BUILD_REQUEST fixture.
5. **[EXECUTION]** Author TEST-006 hidden-input grep assertion fixture.
6. **[VERIFICATION]** Run all three via `uv run pytest tests/audit/test_execution_context_*.py -v`; assert green.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_execution_context_full.py tests/audit/test_execution_context_minimal_buildrequest.py tests/audit/test_execution_context_no_file_paths.py -v` exits 0.
- TEST-005 asserts Source areas and Key constraints lines are absent (not blank).
- TEST-006 asserts `grep` over header range returns 0.
- Evidence at `TASKLIST_ROOT/artifacts/D-0023/evidence.md`.

**Validation:**
- Manual check: reviewer confirms each fixture's assertions match roadmap text.
- Evidence: pytest log.

**Dependencies:** T02.07, T02.08
**Rollback:** As stated in roadmap
**Notes:** None.

### T02.10 -- Verify NFR-CONV.7 evidence-bound preservation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-046 |
| Why | Per-item Context fields MUST retain file:line citations OR justified-absence comments (validated by TB-Add-8 from M1); integration with TB-Add-8 verified. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0024 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0024/spec.md`
- `TASKLIST_ROOT/artifacts/D-0024/evidence.md`

**Deliverables:**
- Three-fixture triple confirming bare path FAIL, file:line PASS, justified-absence PASS.
- TB-Add-8 integration evidence from M1 fixture re-run against M2 MDTM.
- NFR-CONV.7 preservation report.

**Steps:**
1. **[PLANNING]** Read R-046 invariant spec.
2. **[PLANNING]** Identify TEST-003 three-fixture triple from M1.
3. **[EXECUTION]** Re-run the triple against M2-generated MDTM with the new header.
4. **[VERIFICATION]** Assert bare-path FAIL, file:line PASS, justified-absence PASS verdicts.
5. **[VERIFICATION]** Confirm TB-Add-8 still cites per-item Context fields, not the header.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- TEST-003 triple re-run produces FAIL/PASS/PASS verdicts unchanged from M1.
- TB-Add-8 error citations refer to per-item Context fields, not the header.
- NFR-CONV.7 preservation report written to `TASKLIST_ROOT/artifacts/D-0024/evidence.md`.
- Per-item Context fields retain `file:line` form post-M2.

**Validation:**
- Manual check: reviewer confirms TB-Add-8 unaffected by header introduction.
- Evidence: linkable triple-fixture pytest log.

**Dependencies:** T02.09; TB-Add-8 (Phase 1)
**Rollback:** As stated in roadmap
**Notes:** None.

### T02.11 -- Execute MIG-002 PR-01 landing migration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-047, R-048 |
| Why | Strictly-additive header emission single-commit landing with FF_EXECUTION_CONTEXT_HEADER feature-flag governance; rollback disables header generation, per-item Context unchanged. |
| Effort | M |
| Risk | High |
| Risk Drivers | migration |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0025 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0025/spec.md`
- `TASKLIST_ROOT/artifacts/D-0025/evidence.md`

**Deliverables:**
- MIG-002 single commit landing FR-CONV.2 header emission.
- `make verify-sync` PASS post-commit.
- FF_EXECUTION_CONTEXT_HEADER governance entry referenced for M7 consolidation.

**Steps:**
1. **[PLANNING]** Confirm Phase 2 tasks T02.01-T02.10 PASS.
2. **[PLANNING]** Run `make verify-sync` on clean baseline.
3. **[EXECUTION]** Stage SKILL.md (1407-1487, 715-725) + rf-task-builder.md edits.
4. **[EXECUTION]** Author commit message documenting per-line revert path (disable header generation block).
5. **[VERIFICATION]** Run `make verify-sync` post-commit; assert PASS.
6. **[COMPLETION]** Spawn quality-engineer sub-agent for diff spot-check.

**Acceptance Criteria:**
- `make verify-sync` exits 0 immediately after MIG-002 commit.
- Commit body documents header-generation-block disable path as rollback.
- Sub-agent report confirms strictly-additive change (no existing item modified beyond named edit ranges).
- FF_EXECUTION_CONTEXT_HEADER entry recorded at `TASKLIST_ROOT/artifacts/D-0025/spec.md` with cleanup window cross-referenced to M7.

**Validation:**
- Manual check: reviewer confirms commit body documents the rollback procedure.
- Evidence: `make verify-sync` log + commit diff + sub-agent report.

**Dependencies:** T02.10
**Rollback:** As stated in roadmap (disable header generation block; per-item Context unchanged)
**Notes:** Critical-path override applied because MIG-002 is the M2 landing gate.

### T02.12 -- Checkpoint: End of Phase 2

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032, R-033, R-034, R-035, R-036, R-037, R-038, R-039, R-040, R-041, R-042, R-043, R-044, R-045, R-046, R-047, R-048 |
| Why | Gate: verify FR-CONV.2 Execution Context header live with 3-line and degraded forms, TB-Add-7/8 still tolerant, MIG-002 merged before unblocking M3. |
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
| Deliverable IDs | D-CP02 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-END.md`

**Purpose:** End-of-Phase-2 gate confirming Execution Context header renders both fully-populated and degraded forms, TB-Add-7/8 invariants preserved, MIG-002 merged with `make verify-sync` PASS.

**Verification:**
- Generated MDTM contains `## Execution Context` block with 3 labeled lines on fully-populated fixture (D-0023 evidence).
- Minimal-BUILD_REQUEST fixture produces References-only header (Source areas + Key constraints lines absent) (D-0023 evidence).
- MIG-002 commit landed with `make verify-sync` PASS (D-0025 evidence).

**Exit Criteria:**
- All 11 regular tasks T02.01-T02.11 (skipping checkpoint slots) report PASS.
- M2 Exit Conditions per roadmap (3 labeled lines, degradation to References-only, grep zero, per-item Context preserved) all met.
- TB-Add-7 cross-validator tolerates degraded header; TB-Add-8 unaffected by header introduction.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Inspect M2 Exit Conditions checklist; assert every item is satisfied.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above with `Overall: Pass`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P02-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T02.01-T02.11 it covers.

**Validation:**
- Manual check: reviewer confirms the report declares M2 PASS and unblocks M3.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.01..T02.11
**Rollback:** N/A (checkpoints are read-only verifications)
