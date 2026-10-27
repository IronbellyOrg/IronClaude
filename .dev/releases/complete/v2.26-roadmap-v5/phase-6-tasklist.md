# Phase 6 -- Integration Testing and Release

Validate the complete pipeline against real and mock scenarios, confirming all success criteria (SC-1 through SC-10) with evidence. Complete unit and integration test suites, execute manual validation run, and produce the release readiness checklist.

### T06.01 -- Complete test_gates_data.py Unit Tests for All Semantic Checks

| Field | Value |
|---|---|
| Roadmap Item IDs | R-077 |
| Why | SC-9: all 10 semantic check functions must have boundary-input unit tests including missing, malformed, and failing-value cases |
| Effort | L |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0045 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0045/evidence.md`

**Deliverables:**
1. Complete `tests/roadmap/test_gates_data.py` with boundary-input unit tests for all 10 semantic check functions (SC-9): valid, invalid, missing, malformed inputs for each

**Steps:**
1. **[PLANNING]** Enumerate all 10 semantic check functions requiring tests
2. **[PLANNING]** Define boundary inputs for each: valid, invalid, missing, malformed
3. **[EXECUTION]** Write tests for 6 DEVIATION_ANALYSIS_GATE checks: `_no_ambiguous_deviations`, `_validation_complete_true`, `_routing_consistent_with_slip_count`, `_pre_approved_not_in_fix_roadmap`, `_slip_count_matches_routing`, `_total_analyzed_consistent`
4. **[EXECUTION]** Write tests for `_certified_is_true`: true/false/missing/malformed
5. **[EXECUTION]** Write tests for `_total_annotated_consistent`: sum matches / doesn't match
6. **[EXECUTION]** Write tests for `_routing_ids_valid`: valid DEV-\d+ / invalid / empty / mixed
7. **[VERIFICATION]** `uv run pytest tests/roadmap/test_gates_data.py -v` exits 0 with all boundary tests passing
8. **[COMPLETION]** Document test coverage in `D-0045/evidence.md`

**Acceptance Criteria:**
- All 10 semantic check functions have tests with valid, invalid, missing, malformed, and failing-value inputs
- Tests verify distinct log messages for failure modes (FR-080)
- Each DEVIATION_ANALYSIS_GATE check has correct return for all 4 input variants
- `_routing_ids_valid` tests include: valid DEV-\d+, invalid format, empty, mixed valid/invalid
- `uv run pytest tests/roadmap/test_gates_data.py -v` exits 0

**Validation:**
- `uv run pytest tests/roadmap/test_gates_data.py -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0045/evidence.md`

**Dependencies:** T05.08 (Phase 5 exit)
**Rollback:** TBD (test file; no production code changes)

---

### T06.02 -- Complete test_models.py Unit Tests for Finding deviation_class

| Field | Value |
|---|---|
| Roadmap Item IDs | R-078 |
| Why | Finding with deviation_class must be tested for existing + new field behavior and default compatibility |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0046 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0046/evidence.md`

**Deliverables:**
1. Complete `tests/roadmap/test_models.py` with Finding deviation_class tests: default value, valid classes, invalid class ValueError, backward compatibility

**Steps:**
1. **[PLANNING]** Review Finding dataclass changes from T02.01
2. **[PLANNING]** Define test cases: default, each valid class, invalid class, backward compatibility
3. **[EXECUTION]** Write test: `Finding("test")` defaults to `"UNCLASSIFIED"`
4. **[EXECUTION]** Write tests: each of 5 valid deviation classes accepted
5. **[EXECUTION]** Write test: invalid class raises `ValueError`
6. **[VERIFICATION]** `uv run pytest tests/roadmap/test_models.py -v` exits 0
7. **[COMPLETION]** Document test coverage in `D-0046/evidence.md`

**Acceptance Criteria:**
- Default deviation_class = "UNCLASSIFIED" verified
- All 5 valid deviation classes construct successfully
- Invalid deviation class raises ValueError
- Backward compatibility verified: existing `Finding` constructors without `deviation_class` continue to work without modification
- `uv run pytest tests/roadmap/test_models.py -v` exits 0

**Validation:**
- `uv run pytest tests/roadmap/test_models.py -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0046/evidence.md`

**Dependencies:** T02.01 (Finding changes)
**Rollback:** TBD (test file)

---

### T06.03 -- Complete test_remediate.py Unit Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-079 |
| Why | deviations_to_findings() and _parse_routing_list() must have complete unit test coverage |
| Effort | M |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0047 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0047/evidence.md`

**Deliverables:**
1. Complete `tests/roadmap/test_remediate.py` with tests for `deviations_to_findings()` (severity mappings, empty routing with slips, missing IDs) and `_parse_routing_list()` (empty, whitespace, invalid, valid, mixed)

**Steps:**
1. **[PLANNING]** Enumerate test cases for deviations_to_findings and _parse_routing_list
2. **[PLANNING]** Define fixture data for each test case
3. **[EXECUTION]** Write tests for `deviations_to_findings()`: HIGH->BLOCKING, MEDIUM->WARNING, LOW->INFO mappings
4. **[EXECUTION]** Write tests: ValueError on empty routing with slip_count > 0; WARNING on missing routing ID
5. **[EXECUTION]** Write tests for `_parse_routing_list()`: empty, whitespace, invalid IDs, valid IDs, mixed
6. **[VERIFICATION]** `uv run pytest tests/roadmap/test_remediate.py -v` exits 0
7. **[COMPLETION]** Document test coverage in `D-0047/evidence.md`

**Acceptance Criteria:**
- `deviations_to_findings()` severity mappings tested: HIGH->BLOCKING, MEDIUM->WARNING, LOW->INFO
- ValueError on empty routing with slip_count > 0 verified
- `_parse_routing_list()` handles empty, whitespace, invalid, valid, mixed inputs
- WARNING log verified when routing ID not found in fidelity table (FR-082)
- `uv run pytest tests/roadmap/test_remediate.py -v` exits 0

**Validation:**
- `uv run pytest tests/roadmap/test_remediate.py -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0047/evidence.md`

**Dependencies:** T03.09 (deviations_to_findings), T02.03 (_parse_routing_list)
**Rollback:** TBD (test file)

---

### T06.04 -- Complete test_executor.py Unit Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-080 |
| Why | _check_annotate_deviations_freshness() 9 test cases, _check_remediation_budget(), _print_terminal_halt() stderr assertions must all be covered |
| Effort | L |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0048 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0048/evidence.md`

**Deliverables:**
1. Complete `tests/roadmap/test_executor.py` with freshness check (9 cases), budget check, and terminal halt stderr assertion tests

**Steps:**
1. **[PLANNING]** Enumerate all test cases: 9 freshness, budget boundary, terminal halt stderr
2. **[PLANNING]** Define fixture data and expected outcomes
3. **[EXECUTION]** Write 9 freshness test cases: matching hash, mismatched hash, missing file, missing field, read error, empty file, corrupt frontmatter, missing roadmap.md, None hash
4. **[EXECUTION]** Write budget tests: attempts 1-2 pass, attempt 3 triggers halt, non-integer coercion
5. **[EXECUTION]** Write terminal halt tests with stderr content assertions
6. **[VERIFICATION]** `uv run pytest tests/roadmap/test_executor.py -v` exits 0
7. **[COMPLETION]** Document test coverage in `D-0048/evidence.md`

**Acceptance Criteria:**
- 9 freshness test cases all pass (SC-8)
- Budget tests verify: 2 attempts allowed, third triggers halt
- Terminal halt stderr assertions verify: attempt count, remaining failing finding count, per-finding details, manual-fix instructions including certification report path and resume command
- Non-integer `remediation_attempts` coerced to 0 with WARNING log verified
- `uv run pytest tests/roadmap/test_executor.py -v` exits 0

**Validation:**
- `uv run pytest tests/roadmap/test_executor.py -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0048/evidence.md`

**Dependencies:** T04.01 (freshness), T04.03 (budget), T04.04 (terminal halt)
**Rollback:** TBD (test file)

---

### Checkpoint: Phase 6 / Tasks 1-5

**Purpose:** Verify all unit test suites are complete before integration testing.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P06-T01-T05.md`
**Verification:**
- All semantic check functions have boundary-input tests
- Freshness check has all 9 SC-8 test cases
- Terminal halt stderr content verified by assertions
**Exit Criteria:**
- All 4 test files pass: `uv run pytest tests/roadmap/test_gates_data.py tests/roadmap/test_models.py tests/roadmap/test_remediate.py tests/roadmap/test_executor.py -v` exits 0
- D-0045 through D-0048 evidence artifacts exist
- No test failures or skipped tests

---

### T06.05 -- Complete test_integration_v5_pipeline.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-081 |
| Why | End-to-end integration test with v2.24 scenario fixtures validating SC-1 through SC-6 pipeline behaviors |
| Effort | L |
| Risk | Medium |
| Risk Drivers | End-to-end, system-wide, multi-file |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0049 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0049/spec.md`

**Deliverables:**
1. Complete `tests/roadmap/test_integration_v5_pipeline.py` with v2.24 scenario fixtures (pre-recorded subprocess outputs, no live Claude calls) validating SC-1, SC-2, SC-3, SC-4, SC-6

**Steps:**
1. **[PLANNING]** Design v2.24 scenario fixtures with pre-recorded subprocess outputs
2. **[PLANNING]** Map SC-1 through SC-6 to specific test scenarios
3. **[EXECUTION]** SC-1: Pipeline reaches certify without manual intervention
4. **[EXECUTION]** SC-2: D-02 and D-04 pre-approved, excluded from HIGH count
5. **[EXECUTION]** SC-3: DEV-002 and DEV-003 classified as SLIP, routed to fix_roadmap
6. **[EXECUTION]** SC-4: Remediation modifies only SLIP-routed elements (diff-based verification)
7. **[EXECUTION]** SC-6: Terminal halt after 2 failed remediation attempts with stderr detail assertions
8. **[VERIFICATION]** `uv run pytest tests/roadmap/test_integration_v5_pipeline.py -v` exits 0
9. **[COMPLETION]** Document integration test results in `D-0049/spec.md`

**Acceptance Criteria:**
- SC-1: Pipeline completes to certify step without manual intervention
- SC-2: Pre-approved deviations (D-02, D-04) excluded from HIGH count
- SC-3: DEV-002, DEV-003 classified SLIP and routed to fix_roadmap
- SC-4: Remediation diff shows SLIP-only changes
- SC-6: Terminal halt with stderr assertions after 2 failed remediations
- At least one integration test validates the complete pipeline flow from extract through certify as a single sequential execution

**Validation:**
- `uv run pytest tests/roadmap/test_integration_v5_pipeline.py -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0049/spec.md`

**Dependencies:** T06.01-T06.04 (unit tests complete)
**Rollback:** TBD (test file)

---

### T06.06 -- Verify NFR-009/NFR-010 Zero Modifications via Static Diff

| Field | Value |
|---|---|
| Roadmap Item IDs | R-082 |
| Why | pipeline/executor.py and pipeline/models.py must have zero modifications; verified by static diff review |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0050 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0050/evidence.md`

**Deliverables:**
1. Static diff evidence confirming zero modifications to `pipeline/executor.py` and `pipeline/models.py`

**Steps:**
1. **[PLANNING]** Identify generic pipeline layer files: `pipeline/executor.py`, `pipeline/models.py`
2. **[PLANNING]** Determine diff baseline (pre-v2.26 commit)
3. **[EXECUTION]** Run `git diff` against baseline for both files
4. **[EXECUTION]** Confirm diff output is empty for both files
5. **[VERIFICATION]** SC-7: no new classes in `pipeline/models.py` or `pipeline/executor.py`
6. **[COMPLETION]** Document diff evidence in `D-0050/evidence.md`

**Acceptance Criteria:**
- `git diff` for `pipeline/executor.py` shows zero changes
- `git diff` for `pipeline/models.py` shows zero changes
- SC-7 verified: no new classes in generic pipeline layer
- NFR-009/NFR-010 confirmed by static diff

**Validation:**
- Manual check: git diff output for both files is empty
- Evidence: linkable artifact produced at `D-0050/evidence.md`

**Dependencies:** None (can run anytime)
**Rollback:** TBD (verification task)

---

### T06.07 -- Execute Manual Validation Run Against v2.24 Spec

| Field | Value |
|---|---|
| Roadmap Item IDs | R-083, R-084, R-085, R-086 |
| Why | Full pipeline execution against v2.24 spec file with artifact inspection for SC-1, SC-7, SC-10 verification |
| Effort | L |
| Risk | Medium |
| Risk Drivers | End-to-end, system-wide |
| Tier | STRICT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0051 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0051/evidence.md`

**Deliverables:**
1. Manual validation evidence: full pipeline run against v2.24 spec, artifact inspection of `spec-deviations.md`, `deviation-analysis.md`, `spec-fidelity.md`, and verification of SC-1, SC-7, SC-10

**Steps:**
1. **[PLANNING]** Prepare v2.24 spec file and pipeline configuration
2. **[PLANNING]** Define artifact inspection checklist
3. **[EXECUTION]** Execute full pipeline against v2.24 spec file
4. **[EXECUTION]** Inspect `spec-deviations.md`: classification correctness, citation format, `roadmap_hash` present, `schema_version: "2.25"` first
5. **[EXECUTION]** Inspect `deviation-analysis.md`: routing correctness, blast radius entries, `schema_version: "2.25"` first
6. **[EXECUTION]** Inspect `spec-fidelity.md`: excluded intentional deviations from HIGH count
7. **[VERIFICATION]** SC-1: pipeline completes without halting at fidelity
8. **[VERIFICATION]** SC-7: no new classes in `pipeline/models.py` or `pipeline/executor.py`
9. **[VERIFICATION]** SC-10: `schema_version: "2.25"` in artifacts, ordered first
10. **[COMPLETION]** Document validation evidence in `D-0051/evidence.md`

**Acceptance Criteria:**
- Pipeline completes full run against v2.24 spec without fidelity halt (SC-1)
- `spec-deviations.md` has correct classifications, citations, roadmap_hash, schema_version first (SC-10)
- `deviation-analysis.md` has correct routing, blast radius, schema_version first (SC-10)
- No new classes in generic pipeline layer (SC-7)

**Validation:**
- Manual check: Full pipeline run logs reviewed; all artifact fields inspected
- Evidence: linkable artifact produced at `D-0051/evidence.md`

**Dependencies:** T06.05 (integration tests pass first)
**Rollback:** TBD (validation task)

---

### T06.08 -- Complete Release Readiness Checklist

| Field | Value |
|---|---|
| Roadmap Item IDs | R-087, R-088 |
| Why | Final release gate: all SC-1 through SC-10 verified, all refusal behaviors confirmed, no regressions, no unresolved issues |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0052 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0052/spec.md`

**Deliverables:**
1. Release readiness checklist with all 10 criteria verified: SC-1 through SC-10 with evidence references, 5 refusal behaviors confirmed, no regressions, zero generic pipeline layer modifications, schema_version ordering, backward compatibility, spec-patch retirement

**Steps:**
1. **[PLANNING]** Load release readiness checklist from roadmap (10+ criteria)
2. **[PLANNING]** Gather evidence from all phases
3. **[EXECUTION]** Verify: all unit tests pass (`uv run pytest tests/roadmap/ -v`)
4. **[EXECUTION]** Verify: SC-1 through SC-10 all marked verified with explicit test or artifact references
5. **[EXECUTION]** Verify: all 5 refusal behaviors from Phase 4 (roadmap) verified with evidence
6. **[EXECUTION]** Verify: no regressions, zero generic pipeline modifications, schema_version ordering, backward compatibility
7. **[VERIFICATION]** Cross-check every SC criterion against its evidence artifact
8. **[COMPLETION]** Write release readiness checklist to `D-0052/spec.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0052/spec.md` exists with all criteria verified
- SC-1 through SC-10 each have explicit test or artifact references
- All 5 refusal behaviors verified
- No unresolved open questions remain in code comments or documentation
- `.roadmap-state.json` backward compatibility confirmed for state files without `remediation_attempts` field
- `_apply_resume_after_spec_patch()` retained in codebase but unreachable from normal v2.26 execution paths
- `uv run pytest tests/ -v` exits 0 with no regressions across entire test suite

**Validation:**
- `uv run pytest tests/ -v` exits 0 with no regressions
- Evidence: linkable artifact produced at `D-0052/spec.md`

**Dependencies:** T06.07
**Rollback:** TBD (documentation task)

---

### Checkpoint: End of Phase 6

**Purpose:** Confirm release readiness — all success criteria verified with evidence, all tests passing, no regressions.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P06-END.md`
**Verification:**
- SC-1 through SC-10 all verified with explicit evidence references
- All unit and integration tests pass with no regressions
- Release readiness checklist complete with no unresolved items
**Exit Criteria:**
- `uv run pytest tests/ -v` exits 0 with full test suite passing
- D-0045 through D-0052 artifacts exist and are non-empty
- Release readiness checklist (D-0052) shows all criteria verified with evidence
