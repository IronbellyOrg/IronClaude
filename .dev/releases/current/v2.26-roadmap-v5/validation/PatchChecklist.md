# Patch Checklist

Generated: 2026-03-16
Total edits: 34 across 6 files

## File-by-file edit checklist

- phase-1-tasklist.md
  - [ ] T01.01: Add OQ-C full resolution to acceptance criteria (from H1)
  - [ ] T01.07: Add test plan independently verifiable criterion to acceptance criteria (from M1)
  - [ ] T01.07: Add _parse_routing_list() placement to module ownership map criterion (from L1)

- phase-2-tasklist.md
  - [ ] T02.01: Add full-suite backward compatibility VERIFICATION step (from M3)
  - [ ] T02.04: Add "failing-value" cases and "distinct log messages" to acceptance criteria (from M2)
  - [ ] T02.05: Add ordering-assertion test requirement to acceptance criteria (from H4)
  - [ ] T02.05: Add complete required fields verification criterion (from M4)
  - [ ] T02.06: Clarify deprecated function docstring scope (from H5)
  - [ ] T02.06: Change test command from tests/sprint/ to full suite (from M5)
  - [ ] T02.08: Change "12" to "11" exit criteria in all references (from H6)

- phase-3-tasklist.md
  - [ ] T03.01: Strengthen frontmatter acceptance criterion to include full FR-011 shape (from L3)
  - [ ] T03.02: Add routing_intent and Spec Update Recommendations acceptance criteria (from H2)
  - [ ] T03.02: Add blast radius analysis acceptance criterion (from H3)
  - [ ] T03.02: Add YAML frontmatter FR-024 and body FR-025 acceptance criterion (from M6)
  - [ ] T03.03: Add ANALYZE NOT_DISCUSSED independently criterion (from L4)
  - [ ] T03.11: Fix integration test deferral phase reference (from M7)

- phase-4-tasklist.md
  - [ ] T04.02: Add coercion verification acceptance criterion or dependency note (from M8)
  - [ ] T04.03: Add configurable max_attempts verification criterion (from H7)
  - [ ] T04.04: Add FR-077 dual-budget extensibility note to deliverables (from M9)
  - [ ] T04.08: Add 3 missing exit criteria verifications (from M10)

- phase-5-tasklist.md
  - [ ] T05.01: Add round citation variant test fixture (from L5)
  - [ ] T05.05: Strengthen stderr content acceptance criteria (from M11)
  - [ ] T05.08: Enumerate all 5 Phase 4 exit criteria explicitly (from M12)

- phase-6-tasklist.md
  - [ ] T06.01: Add failing-value variant and distinct log messages (from L6)
  - [ ] T06.02: Add backward compatibility constructor test (from L7)
  - [ ] T06.03: Add WARNING log assertion for FR-082 (from L8)
  - [ ] T06.04: Add non-integer coercion acceptance criterion (from M14)
  - [ ] T06.04: Enumerate terminal halt stderr content (from L9)
  - [ ] T06.05: Add end-to-end pipeline flow test requirement (from H8)
  - [ ] T06.08: Fix phase reference and add missing release checklist items (from M13)

## Cross-file consistency sweep
- [ ] FR-080 "distinct log messages" requirement referenced consistently in T02.03, T02.04, T06.01
- [ ] All exit-criteria validation tasks (T01.08, T02.08, T03.11, T04.08, T05.08, T06.08) enumerate the correct count of criteria from their respective roadmap phases
- [ ] Phase number cross-references use "(roadmap)" parenthetical consistently when referencing roadmap phase numbering

---

## Precise diff plan

### 1) phase-1-tasklist.md

#### T01.01 acceptance criteria
**A. Add OQ-C resolution (H1)**
Current issue: OQ-C only mentioned as "cascading impact" not as resolved deliverable
Change: Add acceptance criterion after "Cascading impact on OQ-B and OQ-C is documented"
Diff intent: Add line "- OQ-C fully resolved: PRE_APPROVED ID extraction method decided and documented in D-0001/evidence.md"

#### T01.07 acceptance criteria
**B. Add test plan criterion (M1)**
Current issue: Test plan bundled into D-0008 without independent verifiability
Change: Add acceptance criterion
Diff intent: Add line "- Test plan section present as distinct section within D-0008/spec.md, mapping each SC-1 through SC-10 to test file paths and verification methods"

**C. Add _parse_routing_list() to module map (L1)**
Current issue: Module map criterion missing _parse_routing_list()
Change: Strengthen existing acceptance criterion
Diff intent: Change "Every requirement (FR-xxx) mentioned in roadmap appears in the traceability matrix" to add also: "- Module ownership map includes confirmed `_parse_routing_list()` placement decision from T01.06 (D-0006)"

### 2) phase-2-tasklist.md

#### T02.01
**D. Add full-suite verification step (M3)**
Current issue: Step 6 only runs test_models.py
Change: Add step after step 6
Diff intent: Add "6b. **[VERIFICATION]** Run `uv run pytest tests/sprint/ -v` to confirm all existing Finding constructors across codebase still work with default deviation_class"

#### T02.04
**E. Strengthen acceptance criteria (M2)**
Current issue: Missing "failing-value" and "distinct log messages"
Change: Replace acceptance criterion
Diff intent: Change "Each function has unit tests covering valid, invalid, missing, and malformed inputs" to "Each function has unit tests covering valid, invalid, missing, malformed, and failing-value inputs -- with distinct log messages verified for each failure mode"

#### T02.05
**F. Add ordering assertion (H4)**
Current issue: No ordering-specific test requirement
Change: Add acceptance criterion
Diff intent: Add "- Unit test asserts the ordered list/tuple of semantic check references in `DEVIATION_ANALYSIS_GATE`, not merely that all 6 checks are present"

**G. Add required fields completeness (M4)**
Current issue: Only verifies roadmap_hash presence
Change: Add acceptance criterion
Diff intent: Add "- `ANNOTATE_DEVIATIONS_GATE` required fields list is complete per FR-013 and FR-070, not limited to `roadmap_hash` alone"

#### T02.06
**H. Clarify deprecated scope (H5)**
Current issue: Unclear if docstrings apply to all deprecated functions
Change: Strengthen acceptance criterion
Diff intent: Change existing deprecation criterion to "All deprecated semantic check functions (including but not limited to `high_severity_count_zero` and `tasklist_ready_consistent`) have `[DEPRECATED v2.25]` docstrings; complete list of deprecated functions documented explicitly"

**I. Fix test command scope (M5)**
Current issue: Tests sprint only, roadmap requires full suite
Change: Update validation command
Diff intent: Change "`uv run pytest tests/sprint/ -v` exits 0 confirming no regressions" to "`uv run pytest -v` exits 0 confirming full test suite passes (STANDARD downgrade is relaxation, confirm no regressions)"

#### T02.08
**J. Fix exit criteria count (H6)**
Current issue: References "12" when roadmap has 11
Change: Replace all "12" with "11"
Diff intent: Change "12 exit criteria" to "11 exit criteria" in 3 locations (description, steps, acceptance criteria)

### 3) phase-3-tasklist.md

#### T03.01
**K. Strengthen frontmatter criterion (L3)**
Current issue: Only checks schema_version, not full shape
Change: Strengthen acceptance criterion
Diff intent: Change "Output contract specifies `schema_version: \"2.25\"` as first frontmatter field" to "Output contract specifies complete YAML frontmatter per FR-011, with `schema_version: \"2.25\"` as first field, and body format per FR-012"

#### T03.02
**L. Add routing_intent and Spec Update Recommendations (H2)**
Change: Add 2 acceptance criteria after existing ones
Diff intent: Add "- Prompt includes `routing_intent` sub-field (`superior` | `preference`) for INTENTIONAL deviations (FR-090)" and "- Prompt includes `## Spec Update Recommendations` subsection requirement for `update_spec` routed deviations (FR-087)"

**M. Add blast radius (H3)**
Change: Add acceptance criterion
Diff intent: Add "- Prompt requires blast radius analysis for each INTENTIONAL deviation (FR-023)"

**N. Add YAML/body format (M6)**
Change: Add acceptance criterion
Diff intent: Add "- Output contract specifies YAML frontmatter per FR-024 and body format per FR-025"

#### T03.03
**O. Add NOT_DISCUSSED criterion (L4)**
Change: Add acceptance criterion
Diff intent: Add "- When `spec_deviations_path` is provided, prompt includes instruction to ANALYZE NOT_DISCUSSED deviations independently"

#### T03.11
**P. Fix phase reference (M7)**
Change: Fix acceptance criterion wording
Diff intent: Change "sequenced after Phase 4 budget mechanism" to "sequenced after Phase 4 (tasklist) / Phase 3 (roadmap) completes budget mechanism; may be scaffolded now, completed in Phase 4 (tasklist)"

### 4) phase-4-tasklist.md

#### T04.02
**Q. Add coercion note (M8)**
Change: Add acceptance criterion or dependency note
Diff intent: Add "- Note: coercion of `remediation_attempts` to int on read is completed in T04.05; T04.02 is not independently shippable without T04.05 coercion hardening"

#### T04.03
**R. Add max_attempts verification (H7)**
Change: Add acceptance criterion
Diff intent: Add "- Configurable `max_attempts` verified: `max_attempts=1` triggers halt on second attempt; `max_attempts=3` allows third attempt"

#### T04.04
**S. Add extensibility note (M9)**
Change: Add note to deliverables
Diff intent: Add to deliverables: "Function signature and output structure must accommodate FR-077 dual-budget-exhaustion note (implemented in T04.07)"

#### T04.08
**T. Add 3 missing exit criteria (M10)**
Change: Add 3 acceptance criteria
Diff intent: Add "- `_print_terminal_halt()` stderr content covered by assertion-based unit tests", "- `_apply_resume_after_spec_patch()` retained but unreachable from normal v2.25 execution", "- Non-integer `remediation_attempts` coercion to 0 with WARNING verified"

### 5) phase-5-tasklist.md

#### T05.01
**U. Add round citation variant (L5)**
Change: Add acceptance criterion
Diff intent: Add "- Test fixture with D-XX present but missing round citation also causes HIGH severity in spec-fidelity output"

#### T05.05
**V. Strengthen stderr criteria (M11)**
Change: Replace weakened acceptance criterion
Diff intent: Change "Stderr output includes: attempt count, remaining failing findings, manual-fix instructions" to "Stderr output includes: attempt count, remaining failing finding count, per-finding details, manual-fix instructions with certification report path and resume command"

#### T05.08
**W. Enumerate all 5 exit criteria (M12)**
Change: Rewrite acceptance criteria
Diff intent: Replace with 5 explicit criteria: (1) All 5 refusal behaviors verified, (2) SC-4 with diff, (3) SC-5 with true/false/missing/malformed tests, (4) SC-6 with failing-certify integration test including stderr assertion, (5) No prohibited file modifications

### 6) phase-6-tasklist.md

#### T06.01
**X. Add failing-value and log messages (L6)**
Change: Strengthen acceptance criteria
Diff intent: Change "valid, invalid, missing, and malformed inputs" to "valid, invalid, missing, malformed, and failing-value inputs"; Add "Tests verify distinct log messages for failure modes (FR-080)"

#### T06.02
**Y. Add backward compatibility test (L7)**
Change: Add acceptance criterion
Diff intent: Add "- Backward compatibility verified: existing Finding constructors without deviation_class continue to work"

#### T06.03
**Z. Add WARNING log assertion (L8)**
Change: Add acceptance criterion
Diff intent: Add "- WARNING log verified when routing ID not found in fidelity table (FR-082)"

#### T06.04
**AA. Add coercion criterion (M14)**
Change: Add acceptance criterion
Diff intent: Add "- Non-integer `remediation_attempts` coerced to 0 with WARNING log verified"

**AB. Enumerate stderr content (L9)**
Change: Replace generic acceptance criterion
Diff intent: Change "Terminal halt tests assert specific stderr content" to "Terminal halt stderr assertions verify: attempt count, remaining failing finding count, per-finding details, manual-fix instructions including certification report path and resume command"

#### T06.05
**AC. Add end-to-end flow test (H8)**
Change: Add acceptance criterion
Diff intent: Add "- At least one integration test validates the complete pipeline flow from extract through certify as a single sequential execution"

#### T06.08
**AD. Fix phase reference and add items (M13)**
Change: Fix step 5 and add 3 acceptance criteria
Diff intent: Change "from Phase 5" to "from Phase 4 (roadmap)"; Add 3 criteria: "No unresolved open questions in code comments", ".roadmap-state.json backward compatibility for missing remediation_attempts", "_apply_resume_after_spec_patch() retained but unreachable"
