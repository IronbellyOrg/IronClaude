---
high_severity_count: 3
medium_severity_count: 8
low_severity_count: 5
total_deviations: 16
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: Roadmap omits audit-comparator and audit-consolidator agent extensions specified in Section 6
- **Spec Quote**: "| audit-comparator (Sonnet) | Read, Grep, Glob | Add cross-file wiring consistency check | ... | audit-consolidator (Sonnet) | Read, Grep, Glob, Write | Add 'Wiring Health' section to report |" (Section 6.1)
- **Roadmap Quote**: Phase 5 lists only 3 tasks: "T10: Extend audit-scanner ... T11: Extend audit-analyzer ... T12: Extend audit-validator" — audit-comparator and audit-consolidator are absent.
- **Impact**: Two of the five specified agent extensions (audit-comparator cross-file wiring consistency, audit-consolidator "Wiring Health" report section) have no corresponding tasks. An implementer following the roadmap will produce incomplete agent coverage.
- **Recommended Correction**: Add T10a (audit-comparator: cross-file wiring consistency check) and T10b (audit-consolidator: "Wiring Health" section) to Phase 5, or explicitly note them as deferred with rationale.

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Deviation**: Roadmap task numbering diverges from spec tasklist, creating cross-reference confusion
- **Spec Quote**: "| T07 | Unit tests + fixtures | T02-T06 | 400 | ... | T08 | Roadmap pipeline integration | T05 | 35 | ... | T09 | Sprint integration (shadow hook) | T05 | 28 | ... | T10 | Audit agent extensions | T01 | 50 | ... | T11 | Integration tests | T07-T10 | 80 | ... | T12 | Retrospective: run against cli_portify/ | T11 | -- |" (Section 13)
- **Roadmap Quote**: "T07: Add WIRING_GATE to ALL_GATES ... T08: Add wiring-verification as step ... T09: Add wiring_gate_mode ... T10: Extend audit-scanner ... T11: Extend audit-analyzer ... T12: Extend audit-validator ... T13: Unit tests ... T14: Integration tests ... T15: Pre-activation checklist"
- **Impact**: The spec defines T07 as unit tests and T08 as roadmap integration; the roadmap defines T07 as gates.py modification and T08 as executor integration. Task IDs are not interchangeable between documents. Any downstream tasklist or sprint referencing task IDs will have ambiguous cross-references.
- **Recommended Correction**: Either align roadmap task IDs to match spec Section 13, or add an explicit mapping table between the two numbering schemes in the roadmap.

### DEV-003
- **ID**: DEV-003
- **Severity**: HIGH
- **Deviation**: Roadmap omits the spec's retrospective task (T12 in spec) to validate against known cli-portify defects
- **Spec Quote**: "| T12 | Retrospective: run against cli_portify/ | T11 | -- |" (Section 13)
- **Roadmap Quote**: T15 mentions "retrospective validation against known cli-portify no-op defect class" as one bullet in a pre-activation checklist, but does not define it as a standalone task with a dependency chain.
- **Impact**: SC-009 ("Catches cli-portify executor no-op bug") depends on a dedicated retrospective validation run. Burying it as a sub-bullet of a checklist task reduces its visibility and may cause it to be skipped or insufficiently validated.
- **Recommended Correction**: Elevate the cli-portify retrospective to a standalone task (matching spec T12) with explicit dependency on integration tests, or clearly map it as a required sub-deliverable of T15 with its own acceptance criteria.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Roadmap assigns T01 to WiringConfig and T02 to WiringFinding/WiringReport, reversing the spec's single-task data model definition
- **Spec Quote**: "| T01 | Data models (WiringFinding, WiringReport, WiringConfig) | -- | 100 |" (Section 13)
- **Roadmap Quote**: "T01: WiringConfig dataclass + whitelist loader ... T02: WiringFinding + WiringReport dataclasses" (Phase 1)
- **Impact**: The spec treats all data models as a single task (T01). The roadmap splits them into two tasks (T01=config, T02=data models). While functionally reasonable, it changes the dependency graph: spec T02 (unwired callable analysis) depends on a single T01, while roadmap T03 depends on both T01 and T02. This could cause confusion when referencing task dependencies.
- **Recommended Correction**: Document the split explicitly as a roadmap refinement of spec T01, or note the mapping.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits spec's detailed unwired callable analysis algorithm (Section 5.2.1)
- **Spec Quote**: "1. AST-parse all Python files in target directory 2. For each class __init__: a. Extract params where: - ast.unparse(annotation) matches \bCallable\b pattern - default is ast.Constant with value None b. Record: (class_name, param_name, file_path, line) 3. For each injectable: a. Search all Python files for call sites ... b. Check if any call site provides the parameter by keyword c. Zero providers -> WiringFinding(unwired_callable)" (Section 5.2.1)
- **Roadmap Quote**: "T03: Core analysis: run_wiring_analysis() — AST parsing, callable detection, orphan detection, registry detection, severity classification"
- **Impact**: An implementer has the spec for algorithm details, but the roadmap provides no guidance on the specific detection algorithms. If the roadmap is used as the primary implementation guide, the algorithm specifics could be missed or implemented differently.
- **Recommended Correction**: Add cross-references to spec sections 5.2.1-5.2.3 in the T03 task description, or summarize key algorithmic constraints.

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits whitelist validation strictness rules specified for Phase 1 vs Phase 2+
- **Spec Quote**: "Validation: entries missing `symbol` or `reason` are MALFORMED. In Phase 1 (shadow), malformed entries are logged as WARNING and skipped. In Phase 2+, malformed entries raise `WiringConfigError`." (Section 5.2.1)
- **Roadmap Quote**: "T01: WiringConfig dataclass + whitelist loader with strict validation"
- **Impact**: The roadmap says "strict validation" but the spec defines phase-dependent validation behavior (lenient in shadow, strict in soft/full). "Strict validation" in T01 could be misinterpreted as always-strict, conflicting with the shadow-mode leniency requirement.
- **Recommended Correction**: Clarify that whitelist validation is mode-aware: WARNING+skip in shadow, error in soft/full.

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits the spec's `files_skipped` frontmatter field from the gate contract
- **Spec Quote**: "| `files_skipped` | int | >= 0 |" (Section 8.2, Gate Contract table)
- **Roadmap Quote**: "YAML frontmatter (15 fields via yaml.safe_dump())" — mentions 15 fields but does not enumerate them individually. The 15 fields listed in the spec's Section 5.4 include `files_skipped`.
- **Impact**: If an implementer counts the fields from the roadmap's T04 description and misses `files_skipped`, the gate contract would be violated.
- **Recommended Correction**: Either enumerate all 15 required frontmatter fields in the roadmap's T04/T05 descriptions, or add an explicit cross-reference to spec Section 5.4 / 8.2.

### DEV-008
- **ID**: DEV-008
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits the spec's YAML injection prevention requirement for string-valued frontmatter fields
- **Spec Quote**: "All string-valued frontmatter fields MUST use yaml.safe_dump() to prevent YAML injection. Integer/boolean gate-evaluated fields are exempt." (Section 5.4)
- **Roadmap Quote**: "YAML frontmatter (15 fields via yaml.safe_dump())"
- **Impact**: The roadmap mentions `yaml.safe_dump()` but only in the context of emission format, not as a security requirement. The spec's explicit YAML injection prevention rationale is lost, which could lead an implementer to use string formatting instead of safe_dump for individual fields.
- **Recommended Correction**: Add a note in T04 that string-valued frontmatter fields require `yaml.safe_dump()` for YAML injection prevention.

### DEV-009
- **ID**: DEV-009
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits the spec's `grace_period` interaction note for shadow mode
- **Spec Quote**: "Roadmap configurations should set grace_period > 0 during shadow rollout to enable GateMode.TRAILING behavior via TrailingGateRunner. If grace_period = 0 forces BLOCKING, shadow mode still passes because _zero_blocking_findings_for_mode reads rollout_mode=shadow from frontmatter and returns True unconditionally" (Section 7, Phase 1 operational note)
- **Roadmap Quote**: '[MISSING]'
- **Impact**: Without this operational note, a deployment with `grace_period=0` could cause unexpected BLOCKING behavior during shadow rollout, though the semantic check safeguard would prevent actual failures.
- **Recommended Correction**: Add the `grace_period` interaction as an operational note in Phase 3 or the Deployment Readiness Prerequisites.

### DEV-010
- **ID**: DEV-010
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits spec's Phase 2 FPR calibration method details
- **Spec Quote**: "Calibration method (adapted from governance framework): 1. Collect FPR/TPR/p95 for at least two shadow windows 2. Compute baseline distributions per analysis type (unwired_callable, orphan_module, unwired_registry) 3. Propose thresholds and FPR noise floor 4. Obtain sign-off for soft activation" (Section 7, Phase 2)
- **Roadmap Quote**: "FPR measurement | Baseline established | After shadow window" and "Soft promotion requires all: FPR < 15%, TPR > 50%, p95 < 5s"
- **Impact**: The roadmap states promotion thresholds but omits the 4-step calibration method and the per-analysis-type baseline computation requirement. Promotion decisions could be made without proper statistical rigor.
- **Recommended Correction**: Add the calibration method steps to the Shadow Calibration section or Deployment Readiness Prerequisites.

### DEV-011
- **ID**: DEV-011
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits spec's explicit `_get_all_step_ids()` ordering requirement
- **Spec Quote**: "_get_all_step_ids() MUST be updated to include 'wiring-verification' after 'spec-fidelity' and before 'remediate'." (Section 5.7)
- **Roadmap Quote**: "update _get_all_step_ids()" (T08, mentioned but without the ordering constraint)
- **Impact**: The ordering constraint (`after spec-fidelity, before remediate`) is critical for resume behavior. Without it, an implementer might append it at the end of the step ID list.
- **Recommended Correction**: Add the ordering constraint to T08's description.

### DEV-012
- **ID**: DEV-012
- **Severity**: LOW
- **Deviation**: Roadmap scope estimate slightly differs from spec
- **Spec Quote**: "480-580 lines production code, 370-480 lines test code" (frontmatter)
- **Roadmap Quote**: "~500 lines production code, ~400 lines test code" (Executive Summary)
- **Impact**: Minor approximation. The roadmap rounds to round numbers within the spec's ranges.
- **Recommended Correction**: None required; approximation is within spec range.

### DEV-013
- **ID**: DEV-013
- **Severity**: LOW
- **Deviation**: Roadmap critical path omits T04 between T03 and T05
- **Spec Quote**: "Critical path: T01 -> T02/T03/T04/T06 (parallel) -> T05 -> T07 -> T08/T09/T10 (parallel) -> T11 -> T12" (Section 13)
- **Roadmap Quote**: "Task-level: T01 → T02 → T03 → T05 → T07 → T08" (Critical Paths)
- **Impact**: The roadmap's critical path shows T01→T02→T03→T05 which implies T04 (emit_report) is not on the critical path, but T05 (WIRING_GATE) depends on T04. The dependency is captured in the Phase 1 task table (T05 depends on T04) so this is a presentation inconsistency.
- **Recommended Correction**: Update critical path to include T04: T01→T02→T03→T04→T05→T07→T08.

### DEV-014
- **ID**: DEV-014
- **Severity**: LOW
- **Deviation**: Roadmap does not reproduce the spec's dependency direction diagram (Section 8.3)
- **Spec Quote**: "audit/wiring_gate.py --> pipeline/models.py (GateCriteria, SemanticCheck) ... pipeline/* --> NOTHING from audit/roadmap/sprint" (Section 8.3)
- **Roadmap Quote**: '[MISSING]' — dependency direction is mentioned implicitly ("preserve substrate signatures and import boundaries") but not diagrammed.
- **Impact**: Minor; the layering constraint is referenced via NFR-007 mentions but not explicitly diagrammed for implementers.
- **Recommended Correction**: Add a brief dependency direction summary or cross-reference to spec Section 8.3.

### DEV-015
- **ID**: DEV-015
- **Severity**: LOW
- **Deviation**: Roadmap omits spec's Appendix B (Forensic Cross-Reference) and Appendix C (Out of Scope) detail
- **Spec Quote**: Full Appendix B forensic cross-reference table and Appendix C out-of-scope list (Sections after 13)
- **Roadmap Quote**: '[MISSING]'
- **Impact**: Minimal for implementation. Forensic cross-references are informational. Out-of-scope items are partially covered by the roadmap's cut decisions and non-goals context.
- **Recommended Correction**: None required; these are reference appendices. A cross-reference to the spec for these would suffice.

### DEV-016
- **ID**: DEV-016
- **Severity**: LOW
- **Deviation**: Roadmap adds a "Phase 0: Architecture Confirmation" phase not present in spec
- **Spec Quote**: Section 13 tasklist begins with "T01: Data models" with no architecture confirmation phase.
- **Roadmap Quote**: "Phase 0: Architecture Confirmation ... Timeboxed to 0.5–1 session maximum." (Phase 0)
- **Impact**: Positive deviation — the roadmap adds a valuable pre-implementation confirmation step. This does not contradict the spec but extends it.
- **Recommended Correction**: None required; this is a beneficial addition.

---

## Summary

**Severity Distribution**: 3 HIGH, 8 MEDIUM, 5 LOW (16 total)

The roadmap is a faithful and well-structured translation of the specification with strong coverage of core analysis, gate definition, pipeline integration, and rollout strategy. However, three HIGH-severity deviations must be resolved before tasklist generation:

1. **Missing agent extensions**: audit-comparator and audit-consolidator are specified but have no roadmap tasks.
2. **Task ID divergence**: The roadmap renumbers all tasks from T07 onward, creating cross-reference ambiguity with the spec's Section 13 tasklist.
3. **Missing retrospective task**: The spec's dedicated cli-portify retrospective (T12) is demoted to a sub-bullet, risking inadequate validation of SC-009.

The MEDIUM-severity deviations are predominantly omissions of implementation detail (algorithms, validation rules, operational notes) that exist in the spec but are not surfaced in the roadmap. These are manageable if the spec is used as the authoritative reference alongside the roadmap, but would cause issues if the roadmap were used standalone.
