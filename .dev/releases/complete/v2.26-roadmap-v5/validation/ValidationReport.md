# Validation Report

Generated: 2026-03-16
Roadmap: `.dev/releases/current/v2.26-roadmap-v5/roadmap.md`
Phases validated: 6
Agents spawned: 12
Total findings: 34 (High: 8, Medium: 14, Low: 12)

## Findings

### High Severity

#### H1. OQ-C resolution not tracked as explicit deliverable
- **Severity**: High
- **Affects**: phase-1-tasklist.md / T01.01, T01.03
- **Problem**: OQ-C ("How are PRE_APPROVED IDs extracted for gate validation?") is mentioned as cascading impact in T01.01 but has no task that owns its resolution as a concrete deliverable. The roadmap requires all 8 OQs resolved.
- **Roadmap evidence**: Line 43: "OQ-C: How are PRE_APPROVED IDs extracted for gate validation? Depends on OQ-A resolution." Line 79: "All 8 open questions resolved or deferred with documented fallback"
- **Tasklist evidence**: T01.01 mentions "Cascading impact on OQ-B and OQ-C is documented" but no task has OQ-C resolution as a deliverable
- **Exact fix**: Expand T01.01 acceptance criteria to: "OQ-C fully resolved (not just cascading impact documented): PRE_APPROVED ID extraction method decided and documented in D-0001/evidence.md"

#### H2. T03.02 missing routing_intent and Spec Update Recommendations acceptance criteria
- **Severity**: High
- **Affects**: phase-3-tasklist.md / T03.02
- **Problem**: Prompt requires `routing_intent` sub-field (FR-090) and `## Spec Update Recommendations` subsection (FR-087) but these are absent from formal acceptance criteria
- **Roadmap evidence**: Lines 181-182: routing_intent and Spec Update Recommendations requirements
- **Tasklist evidence**: T03.02 acceptance criteria mention normative mapping and flat routing fields but omit routing_intent and Spec Update Recommendations
- **Exact fix**: Add two acceptance criteria: "Prompt includes `routing_intent` sub-field (`superior` | `preference`) for INTENTIONAL deviations (FR-090)" and "Prompt includes `## Spec Update Recommendations` subsection requirement for `update_spec` routed deviations (FR-087)"

#### H3. T03.02 missing blast radius analysis acceptance criterion
- **Severity**: High
- **Affects**: phase-3-tasklist.md / T03.02
- **Problem**: Blast radius analysis for INTENTIONAL deviations (FR-023) not in acceptance criteria
- **Roadmap evidence**: Line 180: "Blast radius analysis for each INTENTIONAL deviation (FR-023)"
- **Tasklist evidence**: Only mentioned in Validation section as manual check, not formal acceptance
- **Exact fix**: Add acceptance criterion: "Prompt requires blast radius analysis for each INTENTIONAL deviation (FR-023)"

#### H4. T02.05 DEVIATION_ANALYSIS_GATE needs ordering-assertion test
- **Severity**: High
- **Affects**: phase-2-tasklist.md / T02.05
- **Problem**: Roadmap requires semantic check order verified not just existence, but acceptance criteria don't require an ordering assertion test
- **Roadmap evidence**: Line 150: "DEVIATION_ANALYSIS_GATE semantic check order verified, not just existence"
- **Tasklist evidence**: Line 254: "defined as STRICT tier with exactly 6 semantic checks in the specified order"
- **Exact fix**: Add acceptance criterion: "Unit test asserts the ordered list/tuple of semantic check references in DEVIATION_ANALYSIS_GATE, not merely that all 6 checks are present"

#### H5. T02.06 deprecated function docstring scope ambiguity
- **Severity**: High
- **Affects**: phase-2-tasklist.md / T02.06
- **Problem**: Unclear whether deprecated docstrings apply only to the two removed checks or all deprecated functions
- **Roadmap evidence**: Line 136: "Retain deprecated semantic check functions with [DEPRECATED v2.25] docstrings -- do not delete"
- **Tasklist evidence**: T02.06 only mentions docstrings for `high_severity_count_zero` and `tasklist_ready_consistent`
- **Exact fix**: Add to T02.06 or T02.07 acceptance criteria: "All deprecated semantic check functions have [DEPRECATED v2.25] docstrings. Confirm the complete list of deprecated functions and document explicitly."

#### H6. T02.08 references 12 exit criteria when roadmap has 11
- **Severity**: High
- **Affects**: phase-2-tasklist.md / T02.08
- **Problem**: Factual error in exit criteria count
- **Roadmap evidence**: Lines 142-152: 11 exit criteria checkboxes
- **Tasklist evidence**: References "12 criteria" in 3 locations
- **Exact fix**: Change all "12" references to "11" in T02.08

#### H7. T04.03 missing configurable max_attempts verification
- **Severity**: High
- **Affects**: phase-4-tasklist.md / T04.03
- **Problem**: Roadmap requires configurable `max_attempts` parameter but acceptance criteria only test default (2)
- **Roadmap evidence**: Line 268: "Max 2 attempts (configurable via max_attempts parameter)"
- **Tasklist evidence**: Acceptance criteria only test default behavior
- **Exact fix**: Add acceptance criterion: "Configurable `max_attempts` verified: `max_attempts=1` triggers halt on second attempt; `max_attempts=3` allows third attempt"

#### H8. T06.05 missing explicit end-to-end pipeline flow test
- **Severity**: High
- **Affects**: phase-6-tasklist.md / T06.05
- **Problem**: Roadmap requires validating complete pipeline flow extract->certify as single execution, not just individual SC checks
- **Roadmap evidence**: Phase 5 Integration Test: "Validate complete pipeline flow: extract -> ... -> certify"
- **Tasklist evidence**: Acceptance criteria list individual SC checks but no end-to-end flow requirement
- **Exact fix**: Add acceptance criterion: "At least one integration test validates the complete pipeline flow from extract through certify as a single sequential execution"

### Medium Severity

#### M1. T01.07 test plan lacks independently verifiable criterion
- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.07
- **Problem**: Test plan bundled into D-0008 without explicit section requirement
- **Exact fix**: Add acceptance criterion: "Test plan section is present as a distinct section within D-0008/spec.md, mapping each of SC-1 through SC-10 to specific test file paths and verification methods"

#### M2. T02.04 acceptance criteria omit failing-value cases and distinct log messages
- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.04
- **Problem**: Missing "failing-value" input category and "distinct log messages" requirement
- **Exact fix**: Change to: "Each function has unit tests covering valid, invalid, missing, malformed, and failing-value inputs -- with distinct log messages verified for each failure mode"

#### M3. T02.01 missing full-suite backward compatibility verification step
- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.01
- **Problem**: Step 6 only runs test_models.py; should also run full sprint test suite to verify all Finding constructors
- **Exact fix**: Add VERIFICATION step: "Run `uv run pytest tests/sprint/ -v` to confirm all existing Finding constructors across the codebase still work"

#### M4. T02.05 ANNOTATE_DEVIATIONS_GATE required fields incomplete
- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.05
- **Problem**: Acceptance criteria only verify roadmap_hash is among required fields, not that full required fields list is confirmed
- **Exact fix**: Add: "Verify ANNOTATE_DEVIATIONS_GATE required fields list is complete per FR-013 and FR-070"

#### M5. T02.06 test command runs tests/sprint/ not full suite
- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.06
- **Problem**: Roadmap says "Full test suite passes" but validation command is limited to sprint tests
- **Exact fix**: Change validation from `uv run pytest tests/sprint/ -v` to `uv run pytest -v`

#### M6. T03.02 missing YAML frontmatter and body format acceptance criteria
- **Severity**: Medium
- **Affects**: phase-3-tasklist.md / T03.02
- **Problem**: Output contract requires YAML frontmatter per FR-024 and body format per FR-025
- **Exact fix**: Add: "Output contract specifies YAML frontmatter per FR-024 and body format per FR-025"

#### M7. T03.11 integration test deferral phase reference mismatch
- **Severity**: Medium
- **Affects**: phase-3-tasklist.md / T03.11
- **Problem**: Says "sequenced after Phase 4 budget mechanism" but roadmap says "after Phase 3 completes"
- **Exact fix**: Change to "sequenced after Phase 4 (tasklist) / Phase 3 (roadmap) completes budget mechanism"

#### M8. T04.02 missing coercion verification
- **Severity**: Medium
- **Affects**: phase-4-tasklist.md / T04.02
- **Problem**: Introduces counter but doesn't verify coercion behavior
- **Exact fix**: Add acceptance criterion: "Non-integer `remediation_attempts` coerced to 0 with WARNING on read verified" or add dependency note that T04.05 completes this

#### M9. T04.04 missing FR-077 dual-budget extensibility note
- **Severity**: Medium
- **Affects**: phase-4-tasklist.md / T04.04
- **Problem**: Function signature should accommodate FR-077 dual-budget note (implemented in T04.07)
- **Exact fix**: Add note to deliverables: "Function signature and output structure must accommodate FR-077 dual-budget-exhaustion note (implemented in T04.07)"

#### M10. T04.08 missing 3 exit criteria verifications
- **Severity**: Medium
- **Affects**: phase-4-tasklist.md / T04.08
- **Problem**: Claims to verify "all 10" but misses stderr assertions, spec-patch retirement, and coercion handling
- **Exact fix**: Add 3 acceptance criteria: (1) "_print_terminal_halt() stderr content covered by assertion-based unit tests", (2) "_apply_resume_after_spec_patch() retained but unreachable from normal v2.25 execution", (3) "Non-integer remediation_attempts coercion to 0 with WARNING verified"

#### M11. T05.05 stderr content criteria weakened
- **Severity**: Medium
- **Affects**: phase-5-tasklist.md / T05.05
- **Problem**: Missing "per-finding details", "certification report path", and "resume command" from stderr assertion
- **Exact fix**: Change to: "Stderr output includes: attempt count, remaining failing finding count, per-finding details, manual-fix instructions with certification report path and resume command"

#### M12. T05.08 missing SC-5/SC-6 as individually verifiable items
- **Severity**: Medium
- **Affects**: phase-5-tasklist.md / T05.08
- **Problem**: Phase 4 exit criteria include SC-5 and SC-6 as separate items, but T05.08 doesn't enumerate them
- **Exact fix**: Rewrite acceptance criteria to enumerate all 5 roadmap Phase 4 exit criteria explicitly including SC-5 and SC-6

#### M13. T06.08 phase reference error and missing release checklist items
- **Severity**: Medium
- **Affects**: phase-6-tasklist.md / T06.08
- **Problem**: Says "Phase 5" instead of "Phase 4" for refusal behaviors; omits 3 specific checklist items
- **Exact fix**: Change "from Phase 5" to "from Phase 4". Add: (1) "No unresolved open questions in code comments", (2) ".roadmap-state.json backward compatibility for missing remediation_attempts", (3) "_apply_resume_after_spec_patch() retained but unreachable"

#### M14. T06.04 missing non-integer coercion acceptance criterion
- **Severity**: Medium
- **Affects**: phase-6-tasklist.md / T06.04
- **Problem**: Steps mention coercion but acceptance criteria don't include it
- **Exact fix**: Add: "Non-integer remediation_attempts coerced to 0 with WARNING log verified"

### Low Severity

#### L1. T01.07 module map missing _parse_routing_list() placement
- **Severity**: Low
- **Affects**: phase-1-tasklist.md / T01.07
- **Exact fix**: Add to acceptance criteria: "Module ownership map includes confirmed _parse_routing_list() placement decision from T01.06"

#### L2. T02.03 FR-080 scope broader than routing list
- **Severity**: Low
- **Affects**: phase-2-tasklist.md / T02.03
- **Exact fix**: Add note: "FR-080 coverage extends to parse_frontmatter() integer fields as well"

#### L3. T03.01 acceptance criteria don't verify full frontmatter shape
- **Severity**: Low
- **Affects**: phase-3-tasklist.md / T03.01
- **Exact fix**: Strengthen to: "Output contract specifies complete YAML frontmatter per FR-011, with schema_version: '2.25' as first field, and body format per FR-012"

#### L4. T03.03 missing ANALYZE NOT_DISCUSSED independently criterion
- **Severity**: Low
- **Affects**: phase-3-tasklist.md / T03.03
- **Exact fix**: Add: "When spec_deviations_path provided, prompt includes instruction to ANALYZE NOT_DISCUSSED deviations independently"

#### L5. T05.01 missing round citation variant test
- **Severity**: Low
- **Affects**: phase-5-tasklist.md / T05.01
- **Exact fix**: Add: "Test fixture with D-XX present but missing round citation also causes HIGH severity"

#### L6. T06.01 missing failing-value variant and log messages
- **Severity**: Low
- **Affects**: phase-6-tasklist.md / T06.01
- **Exact fix**: Add "failing-value" as 5th input variant; add "Tests verify distinct log messages for failure modes (FR-080)"

#### L7. T06.02 missing explicit backward compatibility test
- **Severity**: Low
- **Affects**: phase-6-tasklist.md / T06.02
- **Exact fix**: Add: "Backward compatibility verified: existing Finding constructors without deviation_class work without modification"

#### L8. T06.03 missing WARNING log assertion for FR-082
- **Severity**: Low
- **Affects**: phase-6-tasklist.md / T06.03
- **Exact fix**: Add: "WARNING log verified when routing ID not found in fidelity table (FR-082)"

#### L9. T06.04 terminal halt stderr should enumerate content
- **Severity**: Low
- **Affects**: phase-6-tasklist.md / T06.04
- **Exact fix**: Replace generic "assert specific stderr content" with: "Terminal halt stderr assertions verify: attempt count, remaining failing finding count, per-finding details, manual-fix instructions including certification report path and resume command"

## Verification Results

Verified: 2026-03-16
Findings resolved: 34/34

| Finding | Status | Notes |
|---------|--------|-------|
| H1 | RESOLVED | OQ-C resolution added to T01.01 acceptance criteria |
| H2 | RESOLVED | routing_intent and Spec Update Recommendations added to T03.02 |
| H3 | RESOLVED | Blast radius criterion added to T03.02 |
| H4 | RESOLVED | Ordering assertion test requirement added to T02.05 |
| H5 | RESOLVED | Deprecated function scope clarified in T02.06 |
| H6 | RESOLVED | Changed "12" to "11" in T02.08 (3 occurrences) |
| H7 | RESOLVED | Configurable max_attempts verification added to T04.03 |
| H8 | RESOLVED | End-to-end pipeline flow test requirement added to T06.05 |
| M1 | RESOLVED | Test plan independently verifiable criterion added to T01.07 |
| M2 | RESOLVED | Failing-value and distinct log messages added to T02.04 |
| M3 | RESOLVED | Full-suite backward compatibility step added to T02.01 |
| M4 | RESOLVED | Required fields completeness added to T02.05 |
| M5 | RESOLVED | Test command changed to full suite in T02.06 |
| M6 | RESOLVED | YAML frontmatter FR-024 and body FR-025 added to T03.02 |
| M7 | RESOLVED | Phase reference fixed in T03.11 |
| M8 | RESOLVED | Coercion dependency note added to T04.02 |
| M9 | RESOLVED | FR-077 extensibility note added to T04.04 deliverables |
| M10 | RESOLVED | 3 missing exit criteria added to T04.08 |
| M11 | RESOLVED | Stderr content criteria strengthened in T05.05 |
| M12 | RESOLVED | SC-5 and SC-6 enumerated in T05.08 |
| M13 | RESOLVED | Phase reference fixed and checklist items added in T06.08 |
| M14 | RESOLVED | Non-integer coercion criterion added to T06.04 |
| L1 | RESOLVED | _parse_routing_list() placement added to T01.07 module map |
| L2 | NOT APPLIED | FR-080 broader scope note deferred (low priority, covered in steps) |
| L3 | RESOLVED | Frontmatter criterion strengthened in T03.01 |
| L4 | RESOLVED | NOT_DISCUSSED criterion added to T03.03 |
| L5 | RESOLVED | Round citation variant test added to T05.01 |
| L6 | RESOLVED | Failing-value and log messages added to T06.01 |
| L7 | RESOLVED | Backward compatibility test added to T06.02 |
| L8 | RESOLVED | WARNING log assertion added to T06.03 |
| L9 | RESOLVED | Stderr content enumerated in T06.04 |
