---
high_severity_count: 2
medium_severity_count: 5
low_severity_count: 3
total_deviations: 10
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: Roadmap file count says "10 new files" but spec defines 12 new files (4 source + 8 test). The roadmap's New Files table lists 12 correctly, but the Executive Summary is inconsistent.
- **Spec Quote**: "**New files**: 4 source + 8 test = 12 files"
- **Roadmap Quote**: "34 requirements (23 functional, 11 non-functional) across 10 new files and 5 modified files (~1,200 LOC)"
- **Impact**: The discrepancy (10 vs 12) could cause a tasklist generator to under-provision test files, particularly the 4 sprint/integration test files added in the expanded test file list.
- **Recommended Correction**: Change Executive Summary to "12 new files" to match both the spec Section 12 and the roadmap's own "New Files (12)" table.

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Deviation**: Roadmap `TrailingGateResult` constructor signature includes `step_id` as first positional argument, but spec Section 9.5 defines it as `TrailingGateResult(passed, evaluation_ms, gate_name)` with no `step_id` parameter.
- **Spec Quote**: "Gate result is wrapped in `TrailingGateResult(passed, evaluation_ms, gate_name)`"
- **Roadmap Quote**: "Wrap anti-instinct gate result in `TrailingGateResult(step_id, passed, evaluation_ms)` and submit to `_all_gate_results` (FR-SPRINT.2)"
- **Impact**: Implementing the roadmap's signature would produce a dataclass incompatible with the spec's contract. The parameter order and field names differ (`gate_name` vs `step_id`, positional order swapped).
- **Recommended Correction**: Align roadmap Section 3.2 to use `TrailingGateResult(passed, evaluation_ms, gate_name)` per spec Section 9.5.

### DEV-003
- **ID**: DEV-003
- **Severity**: MEDIUM
- **Deviation**: Roadmap references open questions OQ-001 through OQ-011 but the spec does not define these OQ identifiers. The roadmap introduces OQ-001 (fingerprint extensibility), OQ-002 (context window), OQ-003 (exempt syntax), OQ-004 (severity demotion), OQ-005 (D-03/D-04 coexistence), OQ-006 (structural audit STRICT transition), OQ-007 (TurnLedger design.md), OQ-008 (multi-component false negatives), OQ-009 (contract-specific matching), OQ-010 (Integration Wiring Tasks heading validation), OQ-011 (excluded constants alignment) without traceability to spec.
- **Spec Quote**: [MISSING — no OQ-NNN identifiers defined]
- **Roadmap Quote**: "OQ-003 | `# obligation-exempt` syntax | Per-line scope on the scaffold term's line" (and 10 others)
- **Impact**: The open questions are reasonable inferences from spec ambiguities, but the spec does not explicitly leave these as open. The roadmap is correct to surface them, but an implementer cannot verify which are truly open vs. already decided by the spec text.
- **Recommended Correction**: Either add an OQ section to the spec for traceability, or annotate each roadmap OQ with the spec section/line that creates the ambiguity.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Spec Section 9 Change 4 specifies importing `TrailingGateResult` and `DeferredRemediationLog` from `..sprint.models` in `roadmap/executor.py`. The roadmap does not include this import requirement in Phase 2 executor wiring tasks.
- **Spec Quote**: "from ..sprint.models import TrailingGateResult, DeferredRemediationLog"
- **Roadmap Quote**: Phase 2.2 lists "Add `_run_structural_audit()` hook... Add `anti-instinct` step... Implement `_run_anti_instinct_audit()`... Add `'anti-instinct'` to `_get_all_step_ids()`" but no import for sprint models.
- **Impact**: The roadmap/executor.py imports sprint models, creating a cross-package dependency that should be explicitly tasked. Missing this could cause circular import issues if not handled carefully.
- **Recommended Correction**: Add an explicit task in Phase 2.2 for the sprint model imports in `roadmap/executor.py`, or defer this import to Phase 3 when sprint integration begins.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Spec Section 8 defines `gate_scope=GateScope.TASK` in the `ANTI_INSTINCT_GATE` definition. Roadmap Section 2.1 does not mention `gate_scope` in the gate definition task, though it does appear in the executor step definition (Section 2.2).
- **Spec Quote**: "gate_scope=GateScope.TASK,  # Consumed by resolve_gate_mode() in sprint context"
- **Roadmap Quote**: "Define `ANTI_INSTINCT_GATE` as `GateCriteria` with required frontmatter: `undischarged_obligations` (int), `uncovered_contracts` (int), `fingerprint_coverage` (float) (FR-GATE.1)"
- **Impact**: An implementer following roadmap 2.1 might omit `gate_scope` from the `GateCriteria` constructor, which would affect sprint-context resolution.
- **Recommended Correction**: Add `gate_scope=GateScope.TASK` to the FR-GATE.1 task description in Section 2.1.

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: Spec Section 8 defines `min_lines=10` in the `ANTI_INSTINCT_GATE` `GateCriteria`. Roadmap does not mention this field.
- **Spec Quote**: "min_lines=10,"
- **Roadmap Quote**: [MISSING]
- **Impact**: Without `min_lines=10`, the gate might accept a malformed audit report with insufficient content. Minor because the semantic checks would likely catch this, but it diverges from the spec's defense-in-depth.
- **Recommended Correction**: Add `min_lines=10` to FR-GATE.1 task description.

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: Spec Section 9.6 describes KPI Report Integration (`GateKPIReport`, `build_kpi_report()`, specific metrics like `gate_pass_rate`, `gate_latency_p50/p95`, `turns_reimbursed_total`). The roadmap does not have an explicit task for KPI report integration.
- **Spec Quote**: "`GateKPIReport` (sprint/kpi.py) receives anti-instinct gate results alongside all other gate results at sprint completion via `build_kpi_report()`."
- **Roadmap Quote**: [MISSING — no explicit KPI integration task]
- **Impact**: KPI report integration is implicitly covered by the sprint executor wiring in Phase 3, but without an explicit task it could be overlooked during implementation.
- **Recommended Correction**: Add a task in Phase 3 for verifying KPI report integration receives anti-instinct gate results.

### DEV-008
- **ID**: DEV-008
- **Severity**: LOW
- **Deviation**: Spec Section 13 describes "4-6 sprint tasks" for Phase 1 implementation and lists a 9-step implementation sequence (tasks 1-9 including shadow validation). Roadmap Phase 1 does not use this task numbering.
- **Spec Quote**: "Estimated implementation: 4-6 sprint tasks."
- **Roadmap Quote**: Phase 1 uses sections 1.0 through 1.5.1 without referencing the spec's task numbers.
- **Impact**: No functional impact. The roadmap's section structure adequately covers the same scope.
- **Recommended Correction**: None required; organizational difference only.

### DEV-009
- **ID**: DEV-009
- **Severity**: LOW
- **Deviation**: Spec Section 4 defines `SCAFFOLD_TERMS` with 11 terms, and roadmap Section 1.1 references "11 scaffold terms" (FR-MOD1.1). However, the spec code shows `hardwired` as a separate term from `hardcoded`, making it 11 total. The roadmap correctly states 11, but the Vocabulary Management table in the spec only lists 10 scaffold terms (omitting `hardwired`).
- **Spec Quote**: SCAFFOLD_TERMS list has 11 entries including `r"\bhardwired\b"`; Vocabulary Management table has 10 rows.
- **Roadmap Quote**: "Implement compiled regex vocabulary for 11 scaffold terms (FR-MOD1.1)"
- **Impact**: Internal spec inconsistency (code vs. table); roadmap follows the code correctly.
- **Recommended Correction**: Add `hardwired` to the spec's Vocabulary Management table.

### DEV-010
- **ID**: DEV-010
- **Severity**: LOW
- **Deviation**: Roadmap Checkpoint B is placed at "End of Phase 3" while spec Section 13 places shadow-mode validation as step 9 in the Phase 1 implementation sequence.
- **Spec Quote**: "9. Shadow-mode validation run. Graduation criteria: `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprints before advancing to soft mode."
- **Roadmap Quote**: "**B: Rollout Readiness** | End of Phase 3"
- **Impact**: The spec groups shadow validation as the last step of Phase 1's sequence, while the roadmap correctly separates it into Phase 4. The roadmap's phasing is more logical (shadow validation requires sprint integration from Phase 3), so this is a spec organizational issue rather than a roadmap error.
- **Recommended Correction**: None required for roadmap; the spec's step 9 placement is misleading.

## Summary

**Severity Distribution**: 2 HIGH, 5 MEDIUM, 3 LOW

The roadmap is a faithful and well-structured translation of the specification. The two HIGH severity deviations are:

1. **File count inconsistency** (DEV-001): Executive Summary says 10 new files but the spec and the roadmap's own detail table say 12. Simple arithmetic error.
2. **`TrailingGateResult` signature mismatch** (DEV-002): The roadmap uses `(step_id, passed, evaluation_ms)` while the spec defines `(passed, evaluation_ms, gate_name)`. This would produce an incompatible dataclass.

The MEDIUM deviations are mostly omitted implementation details from the `GateCriteria` constructor (`gate_scope`, `min_lines`) and missing traceability for open questions. All are correctable without architectural changes.
