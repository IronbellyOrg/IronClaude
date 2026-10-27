# Validation Report
Generated: 2026-03-16
Roadmap: .dev/releases/backlog/v2.25.5-PreFlightExecutor/roadmap.md
Phases validated: 5
Agents spawned: 10
Total findings: 14 (High: 4, Medium: 6, Low: 4)

## Findings

### High Severity

#### H1. T03.07 EXEMPT tier contradicts RISK-001 compatibility fixture
- **Severity**: High
- **Affects**: phase-3-tasklist.md / T03.07
- **Problem**: T03.07 implements the compatibility fixture that is the sole mitigation for RISK-001 (High severity — Result File Format Drift). Assigning EXEMPT tier with "Skip verification" means the most critical test in Phase 3 has no enforcement gate, contradicting the roadmap's risk treatment.
- **Roadmap evidence**: "RISK-001: Result File Format Drift (High)" and "Shared compatibility fixture validates both preflight-origin and Claude-origin result files"
- **Tasklist evidence**: "Tier | EXEMPT" and "Verification Method | Skip verification" in T03.07
- **Exact fix**: Change T03.07 Tier from EXEMPT to STANDARD, Verification Method from "Skip verification" to "Direct test execution", Fallback Allowed from Yes to No.

#### H2. T04.06 EXEMPT tier contradicts RISK-005 regression test
- **Severity**: High
- **Affects**: phase-4-tasklist.md / T04.06
- **Problem**: T04.06 is the dedicated regression test for RISK-005 (Orchestration Regression, Medium severity). EXEMPT tier with "Skip verification" allows bypassing the primary mitigation for regression risk.
- **Roadmap evidence**: "RISK-005: Orchestration Regression in Existing Claude Flow (Medium)" and "Dedicated regression test for all-Claude tasklists"
- **Tasklist evidence**: "Tier | EXEMPT" and "Verification Method | Skip verification" in T04.06
- **Exact fix**: Change T04.06 Tier from EXEMPT to STANDARD, Verification Method from "Skip verification" to "Direct test execution", Fallback Allowed from Yes to No.

#### H3. T05.04 EXEMPT tier contradicts release gate criterion SC-007
- **Severity**: High
- **Affects**: phase-5-tasklist.md / T05.04
- **Problem**: T05.04 verifies SC-007 (single-line rollback), which is an explicit release gate criterion. EXEMPT tier allows an automated sprint executor to skip this task, while the roadmap requires rollback to be demonstrated before ship.
- **Roadmap evidence**: "Verify SC-007: single-line rollback works" and "Release gate criteria: Ship only when: ... Rollback is demonstrated"
- **Tasklist evidence**: "Tier | EXEMPT" and "Verification Method | Skip verification" in T05.04
- **Exact fix**: Change T05.04 Tier from EXEMPT to STANDARD, Verification Method from "Skip verification" to "Direct test execution", Fallback Allowed from Yes to No.

#### H4. T03.03 missing output filename in acceptance criteria
- **Severity**: High
- **Affects**: phase-3-tasklist.md / T03.03
- **Problem**: The roadmap specifies writing to `phase-N-result.md`, but T03.03 acceptance criteria and deliverables do not specify the output file name. An implementer could generate correctly-formatted content written to a wrong filename, breaking `_determine_phase_status()` file lookup.
- **Roadmap evidence**: "Write phase-N-result.md via AggregatedPhaseReport.to_markdown()"
- **Tasklist evidence**: T03.03 Deliverables say "Phase result file generation" without naming the file; Acceptance Criteria say "Phase result file is generated" without specifying the `phase-N-result.md` name.
- **Exact fix**: Add to T03.03 Acceptance Criteria bullet 1: "Phase result file is written to `phase-N-result.md` (matching the naming convention used by `_determine_phase_status()` for file lookup)". Add `phase-N-result.md` filename to Deliverables.

### Medium Severity

#### M1. T02.02 tests only exit_code 1 for fail path
- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.02
- **Problem**: The classifier contract is any non-zero exit code returns "fail", but acceptance criteria and validation only test exit_code 1. Other non-zero codes (2, 127) are untested.
- **Roadmap evidence**: "Returns classification label (e.g., 'pass', 'fail')" — exit_code is an int, not restricted to 0/1.
- **Tasklist evidence**: "empirical_gate_v1(1, '', 'error output') returns 'fail'" — only tests 1.
- **Exact fix**: Add to T02.02 Acceptance Criteria: "empirical_gate_v1(127, '', 'command not found') returns 'fail'" to verify the general non-zero contract.

#### M2. T03.04 missing dependency on T03.07
- **Severity**: Medium
- **Affects**: phase-3-tasklist.md / T03.04
- **Problem**: T03.04 Step 6 references the compatibility fixture created in T03.07, but T03.07 is not listed as a dependency. Since T03.04 executes before T03.07, Step 6 is unexecutable as written.
- **Roadmap evidence**: "Compatibility fixture: validate both preflight-origin and Claude-origin result files parse identically"
- **Tasklist evidence**: T03.04 Dependencies: "T03.03" — T03.07 absent.
- **Exact fix**: Either (a) add T03.07 to T03.04 Dependencies, or (b) restructure T03.04 Step 6 to create a minimal inline compatibility check rather than referencing T03.07's fixture. Option (b) is preferred since it avoids circular ordering. Change Step 6 to: "Create a minimal Claude-origin result file sample and compare parsing output with the preflight-generated file from Step 4."

#### M3. T02.03 TaskStatus.FAIL mapping is documentation-only
- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.03
- **Problem**: The roadmap requires "error" classification to be "treated as TaskStatus.FAIL" as a functional behavior. T02.03 demotes this to a documentation note rather than a verifiable acceptance criterion.
- **Roadmap evidence**: "return 'error' classification, treat as TaskStatus.FAIL"
- **Tasklist evidence**: T02.03 Step 5: "Document that 'error' classification maps to TaskStatus.FAIL at the executor level"
- **Exact fix**: Add to T02.03 Acceptance Criteria: "The 'error' classification returned by run_classifier() is mapped to TaskStatus.FAIL by the executor (verifiable via T03.01 integration)."

#### M4. T01.07/T01.08 test marker instructions missing
- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.07, T01.08
- **Problem**: Acceptance criteria and validation commands reference `-m unit` and `-m integration` marker filters, but no step instructs the implementer to apply `@pytest.mark.unit` or `@pytest.mark.integration` to test functions. Without markers, the validation commands collect zero tests and exit 0 (silent false pass).
- **Roadmap evidence**: "Unit tests for Phase with all three execution modes" / "Round-trip test"
- **Tasklist evidence**: T01.07 AC: "uv run pytest ... -v -m unit" but no step mentions applying the marker.
- **Exact fix**: Add to T01.07 Step 4 (before writing tests): "Apply @pytest.mark.unit to all unit test functions." Add to T01.08 Step 3: "Apply @pytest.mark.integration to the round-trip test function."

#### M5. T05.03 conflates SC-001 and SC-002 thresholds
- **Severity**: Medium
- **Affects**: phase-5-tasklist.md / T05.03
- **Problem**: T05.03 Step 6 introduces a `<30s` expectation for SC-002, but the roadmap only assigns the `<30s` threshold to SC-001. SC-002 is a deadlock-only criterion with 120s timeout as backstop.
- **Roadmap evidence**: "SC-001: <30s, zero tokens" vs "SC-002: Nested claude --print works without deadlock"
- **Tasklist evidence**: T05.03 Step 6: "Confirm no deadlock: command returns within reasonable time (<30s for a simple prompt)"
- **Exact fix**: Change T05.03 Step 6 to: "Confirm no deadlock: command completes within the 120s timeout." Remove the `<30s` sub-bound.

#### M6. T04.02 AC-4 unverifiable at task completion
- **Severity**: Medium
- **Affects**: phase-4-tasklist.md / T04.02
- **Problem**: Acceptance criterion 4 ("Skip-mode phase results are included in the final sprint outcome") cannot be verified at T04.02 completion because the merge logic (T04.03) has not been built yet.
- **Roadmap evidence**: "Merge preflight PhaseResult list with main loop results"
- **Tasklist evidence**: T04.02 AC-4: "Skip-mode phase results are included in the final sprint outcome"
- **Exact fix**: Move AC-4 to T04.03 acceptance criteria. Replace T04.02 AC-4 with: "Skip-mode PhaseResult object is created with correct status and returned from the skip handler."

### Low Severity

#### L1. T02.04 Step 2 count mismatch
- **Severity**: Low
- **Affects**: phase-2-tasklist.md / T02.04
- **Problem**: Step 2 says "Plan 3 test functions" but Steps 3-5 define 4 functions and AC requires "4+ tests passing."
- **Exact fix**: Change T02.04 Step 2 from "Plan 3 test functions" to "Plan 4 test functions matching R-020, R-021, R-022 (split R-020 into pass and fail tests)."

#### L2. T02.01 AC references T02.02 deliverable
- **Severity**: Low
- **Affects**: phase-2-tasklist.md / T02.01
- **Problem**: T02.01 AC states "Registry is initially populated with at least the empirical_gate_v1 classifier (added in T02.02)" — this is unverifiable at T02.01 completion.
- **Exact fix**: Remove the parenthetical "(added in T02.02)" and reword: "CLASSIFIERS registry is importable and accepts classifier registrations."

#### L3. T05.07 D-0043 artifact path undefined
- **Severity**: Low
- **Affects**: phase-5-tasklist.md / T05.07
- **Problem**: D-0043 is listed as a deliverable ID but has no corresponding artifact path in the Artifacts section.
- **Exact fix**: Add to T05.07 Artifacts section: ".dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0035/spec.md" for D-0043 (the spec already exists in the Deliverable Registry).

#### L4. T04.03 invented implementation details
- **Severity**: Low
- **Affects**: phase-4-tasklist.md / T04.03
- **Problem**: Step 2 specifies "preflight results keyed by phase index, main loop fills remaining slots" and AC references `config.active_phases` — both are implementation specifics not in the roadmap.
- **Exact fix**: Change T04.03 Step 2 to: "Design merge strategy that preserves original phase ordering from config." Change AC-1 from "in config.active_phases order" to "in the original phase order defined by the sprint config."

## Verification Results
Verified: 2026-03-16
Findings resolved: 14/14

| Finding | Status | Notes |
|---------|--------|-------|
| H1 | RESOLVED | T03.07 Tier changed from EXEMPT to STANDARD, Verification Method to Direct test execution |
| H2 | RESOLVED | T04.06 Tier changed from EXEMPT to STANDARD, Verification Method to Direct test execution |
| H3 | RESOLVED | T05.04 Tier changed from EXEMPT to STANDARD, Verification Method to Direct test execution |
| H4 | RESOLVED | T03.03 AC and Deliverables now include `phase-N-result.md` filename |
| M1 | RESOLVED | T02.02 AC now includes `empirical_gate_v1(127, '', 'command not found')` test |
| M2 | RESOLVED | T03.04 Step 6 changed to inline Claude-origin comparison (no T03.07 dependency) |
| M3 | RESOLVED | T02.03 AC now requires TaskStatus.FAIL mapping (verifiable via T03.01) |
| M4 | RESOLVED | T01.07 Step 4 adds @pytest.mark.unit; T01.08 Step 3 adds @pytest.mark.integration |
| M5 | RESOLVED | T05.03 Step 6 now uses "within the 120s timeout" only |
| M6 | RESOLVED | T04.02 AC-4 changed to "PhaseResult object created with correct status" |
| L1 | RESOLVED | T02.04 Step 2 changed to "Plan 4 test functions" |
| L2 | RESOLVED | T02.01 AC reworded to "importable and accepts classifier registrations" |
| L3 | RESOLVED | T05.07 Artifacts section now includes D-0043 path |
| L4 | RESOLVED | T04.03 Step 2 and AC-1 use generic ordering language |
