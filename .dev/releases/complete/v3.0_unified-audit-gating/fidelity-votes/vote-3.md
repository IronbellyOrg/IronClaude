---
high_severity_count: 2
medium_severity_count: 6
low_severity_count: 4
total_deviations: 12
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: Roadmap references FR-NNN requirement IDs (FR-009 through FR-038, NFR-001 through NFR-014) that do not exist anywhere in the specification. The spec uses Goal IDs (G-001–G-008), Success Criteria (SC-001–SC-014), Decision IDs (D1–D7), and Risk IDs (R1–R8). No "FR-" or "NFR-" prefixed requirements are defined.
- **Spec Quote**: Goals table uses `G-001` through `G-008`; Success Criteria table uses `SC-001` through `SC-014`; no "FR-" or "NFR-" identifiers appear anywhere in the specification.
- **Roadmap Quote**: Task 1.1a references `FR-009, FR-011`; Task 1.2 references `FR-012, FR-014`; Task 2.1 references `FR-004, FR-022, FR-023, NFR-005`; Phase 1 checkpoint references `NFR-001`; etc. (dozens of FR/NFR references throughout).
- **Impact**: Traceability between roadmap tasks and specification requirements is broken. An implementer cannot verify which spec requirement a task satisfies because the FR/NFR IDs are phantom references. This undermines the entire gate-passing verification chain.
- **Recommended Correction**: Replace all FR-NNN and NFR-NNN references in the roadmap with the correct spec identifiers (G-NNN, SC-NNN, Section references, or Decision IDs). Alternatively, add a formal requirements traceability matrix to the spec defining FR/NFR IDs mapping to existing goals and success criteria.

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Deviation**: Roadmap places analysis functions (`analyze_unwired_callables`, `analyze_orphan_modules`, `analyze_unwired_registries`) in `cli/audit/wiring_analyzer.py`, but the spec places them in `cli/audit/wiring_gate.py`. The spec's Module Map (Section 4.2) defines `wiring_gate.py` as "Core analysis + gate definition + report emitter" and `wiring_analyzer.py` as "AST analyzer plugin for ToolOrchestrator". The data model code block in Section 5.1 explicitly shows `# src/superclaude/cli/audit/wiring_gate.py` as the file containing `WiringFinding` and `WiringReport`, and Section 5.2's algorithms are implicitly in the same module. Section 12's File Manifest confirms: `wiring_gate.py` at 280-320 LOC for "Core analysis + gate + emitter" vs `wiring_analyzer.py` at 140-180 LOC for "AST analyzer for ToolOrchestrator".
- **Spec Quote**: Module Map: `wiring_gate.py CREATE Core analysis + gate definition + report emitter`; `wiring_analyzer.py CREATE AST analyzer plugin for ToolOrchestrator`. File Manifest: `wiring_gate.py 280-320 Core analysis + gate + emitter`; `wiring_analyzer.py 140-180 AST analyzer for ToolOrchestrator`.
- **Roadmap Quote**: Phase 1 tasks: `1.2 Implement unwired callable analysis | cli/audit/wiring_analyzer.py`; `1.3 Implement orphan module analysis | cli/audit/wiring_analyzer.py`; `1.4 Implement registry analysis | cli/audit/wiring_analyzer.py`.
- **Impact**: File organization mismatch will produce incorrect module boundaries. The spec's `wiring_gate.py` is designed as a 280-320 LOC monolith containing analysis + gate + emitter; the roadmap splits analysis into `wiring_analyzer.py` which the spec reserves exclusively for the ToolOrchestrator AST plugin.
- **Recommended Correction**: Update roadmap Phase 1 tasks 1.2, 1.3, 1.4 to target `cli/audit/wiring_gate.py` for the three analysis functions, matching the spec's module map and file manifest. Keep `wiring_analyzer.py` exclusively for the `ast_analyze_file()` ToolOrchestrator plugin (Phase 5).

### DEV-003
- **ID**: DEV-003
- **Severity**: MEDIUM
- **Deviation**: Spec defines `audit_artifacts_used` as a required frontmatter field in the gate contract (Section 8.2) and in the `WIRING_GATE.required_frontmatter_fields` list (Section 5.6), but the roadmap's Phase 2 validation checkpoint says "Report frontmatter contains all 17 required fields" — the spec lists 16 fields in the `required_frontmatter_fields` array, not 17.
- **Spec Quote**: `required_frontmatter_fields` list in Section 5.6 contains 16 entries: `gate`, `target_dir`, `files_analyzed`, `rollout_mode`, `analysis_complete`, `unwired_callable_count`, `orphan_module_count`, `unwired_registry_count`, `critical_count`, `major_count`, `info_count`, `total_findings`, `blocking_findings`, `whitelist_entries_applied`, `files_skipped`, `audit_artifacts_used`.
- **Roadmap Quote**: Phase 2 validation checkpoint: "Report frontmatter contains all 17 required fields"
- **Impact**: Minor count mismatch (16 vs 17) could cause confusion during validation. The spec's gate contract table in Section 8.2 lists 16 rows (omitting `audit_artifacts_used` from the table but including it in the code). Either the roadmap miscounted or there's an implicit field.
- **Recommended Correction**: Verify the exact field count. The `required_frontmatter_fields` list in Section 5.6 has 16 entries. Update the roadmap to say "all 16 required fields" or reconcile the discrepancy.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Spec Section 5.7 Step 5 explicitly requires updating `_get_all_step_ids()` as part of roadmap integration. The roadmap's Phase 3a validation checkpoint mentions it ("_get_all_step_ids() returns wiring-verification between spec-fidelity and remediate") but no Phase 3a task explicitly covers this update. Task 3a.4 only covers `ALL_GATES` registration.
- **Spec Quote**: "**Step 5**: Update `_get_all_step_ids()` (line 538) and `ALL_GATES` (line 933). `_get_all_step_ids()` MUST be updated to include `"wiring-verification"` after `"spec-fidelity"` and before `"remediate"`."
- **Roadmap Quote**: Task 3a.4: "Register `WIRING_GATE` in `ALL_GATES` | `roadmap/gates.py`" — no task mentions updating `_get_all_step_ids()` in `roadmap/executor.py`.
- **Impact**: The `_get_all_step_ids()` update could be forgotten during implementation since it's only in the validation checkpoint, not in a task. The spec calls this out as a synchronization requirement (INV-003) because resume behavior depends on it.
- **Recommended Correction**: Add explicit sub-task to Phase 3a covering `_get_all_step_ids()` update in `roadmap/executor.py`, or explicitly note it as part of task 3a.2.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Spec Section 8.2 Gate Contract table lists `audit_artifacts_used` as a required frontmatter field with type `int` and condition `>= 0`, but this field is missing from the roadmap's Gate Contract table (the roadmap doesn't reproduce the gate contract table, so this is validated against the validation checkpoints and field references). More specifically, the roadmap's OQ-1 acknowledges `audit_artifacts_used` as an open question but doesn't resolve it — it's deferred to Phase 0.
- **Spec Quote**: Section 5.4 report format example: `audit_artifacts_used: 0`; Section 5.6 `required_frontmatter_fields` includes `"audit_artifacts_used"`.
- **Roadmap Quote**: Phase 0 OQ-1: "How are `audit_artifacts_used` located/counted? | Glob for `*-audit-report.yaml` in output dir"
- **Impact**: The field is defined in the spec but its counting mechanism is treated as an open question in the roadmap. This is acceptable for Phase 0 resolution but the roadmap should acknowledge the spec already commits to the field's existence (just not its counting method).
- **Recommended Correction**: Clarify that `audit_artifacts_used` is a committed field per spec; only the discovery mechanism is open.

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: Spec Section 5.2.1 defines whitelist validation behavior: "entries missing `symbol` or `reason` are MALFORMED. In Phase 1 (shadow), malformed entries are logged as WARNING and skipped. In Phase 2+, malformed entries raise `WiringConfigError`." The roadmap's OQ-3 treats whitelist strictness as an open question with a proposed default matching the spec.
- **Spec Quote**: "Validation: entries missing `symbol` or `reason` are MALFORMED. In Phase 1 (shadow), malformed entries are logged as WARNING and skipped. In Phase 2+, malformed entries raise `WiringConfigError`."
- **Roadmap Quote**: OQ-3: "Is whitelist strictness derived from `rollout_mode`? | shadow → WARNING; soft/full → `WiringConfigError`"
- **Impact**: The spec already commits to this behavior. Treating it as an open question risks re-debating a settled design decision.
- **Recommended Correction**: Remove OQ-3 from the open questions list; reference the spec's committed behavior directly.

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: Spec's tasklist (Section 13) shows T05 depends on T01 only, with critical path `T01 -> T02/T03/T04/T06 (parallel) -> T05`. The roadmap's phasing puts analysis (Phase 1) before report+gate (Phase 2), matching this dependency. However, the roadmap adds a new risk R9 ("Merge conflicts with concurrent PRs") not present in the spec's risk table (Section 9).
- **Spec Quote**: Risk table (Section 9) lists R1-R8 only.
- **Roadmap Quote**: "**R9**: Merge conflicts with concurrent PRs | Integration delays | Sequence: complete Phases 1-2 before touching shared files (`roadmap/gates.py`); coordinate merge window | 3a"
- **Impact**: The roadmap adds a risk not in the spec. While this is a useful addition, it creates a divergence from the spec's risk register. The spec's Section 15 (Coordination Notes) does address merge conflict risk but without an R-ID.
- **Recommended Correction**: This is a valid roadmap enhancement. Either accept as-is or backport R9 to the spec's risk table for consistency.

### DEV-008
- **ID**: DEV-008
- **Severity**: MEDIUM
- **Deviation**: Spec Section 10.1 specifies minimum 20 unit tests with a specific breakdown (5+5+3+4+3=20). The roadmap's Phase 1 allocates 200-250 LOC for unit tests, and Phase 2 allocates 100-130 LOC, but the per-function test count breakdown from the spec is not reproduced in the roadmap tasks.
- **Spec Quote**: Section 10.1: "`analyze_unwired_callables` 5 tests; `analyze_orphan_modules` 5 tests; `analyze_unwired_registries` 3 tests; `emit_report` + gate 4 tests; `ast_analyze_file` 3 tests"
- **Roadmap Quote**: Phase 1 Task 1.7: "Unit tests for all three analyzers + whitelist | `tests/audit/` | NFR-003, NFR-004, SC-001–SC-003, SC-007 | 200-250"; Phase 2 Task 2.6: "Unit tests for report + gate + semantic checks | `tests/audit/` | SC-004, SC-014, NFR-003 | 100-130"
- **Impact**: The specific test-count-per-function requirement from the spec could be overlooked. However, the roadmap does reference NFR-004 (≥20 unit + 3 integration tests), so the aggregate minimum is tracked.
- **Recommended Correction**: Add the per-function test count targets from spec Section 10.1 as acceptance criteria in Phase 1 and Phase 2 validation checkpoints.

### DEV-009
- **ID**: DEV-009
- **Severity**: LOW
- **Deviation**: Spec Section 7 Phase 1 pre-activation checklist item 2 says ">50 files must produce >0 findings". The roadmap Phase 3b task 3b.3 references SC-010 for "Pre-activation safeguards (zero-match warning, whitelist validation)" but doesn't reproduce the specific ">50 files must produce >0 findings" threshold.
- **Spec Quote**: "First-run zero-findings sanity check (>50 files must produce >0 findings)"
- **Roadmap Quote**: Task 3b.3: "Pre-activation safeguards (zero-match warning, whitelist validation) | `sprint/executor.py` | SC-010 | 15-20"
- **Impact**: The specific threshold (>50 files) could be implemented differently. SC-010 references help but the exact criterion is not restated.
- **Recommended Correction**: Add the ">50 files must produce >0 findings" threshold to the Phase 3b validation checkpoint or task description.

### DEV-010
- **ID**: DEV-010
- **Severity**: LOW
- **Deviation**: Spec Section 5.7.2 describes resume behavior requirements (3 conditions). The roadmap does not explicitly address resume behavior for the wiring-verification step.
- **Spec Quote**: "No special resume handling is required. The existing resume mechanism detects the output file, evaluates the gate, and skips the step if the gate passes."
- **Roadmap Quote**: '[MISSING]'
- **Impact**: Low — the spec itself says no special handling is required, so the absence in the roadmap is consistent with the conclusion. However, the preconditions (deterministic output, reproducible gate, step ID in `_get_all_step_ids()`) should be validated.
- **Recommended Correction**: Add a note in Phase 3a validation checkpoint confirming resume behavior works correctly for the wiring-verification step.

### DEV-011
- **ID**: DEV-011
- **Severity**: LOW
- **Deviation**: Spec Section 5.4 requires "`yaml.safe_dump()` to prevent YAML injection" for string-valued frontmatter fields. The roadmap does not explicitly reference this serialization requirement.
- **Spec Quote**: "All string-valued frontmatter fields MUST use `yaml.safe_dump()` to prevent YAML injection."
- **Roadmap Quote**: '[MISSING]'
- **Impact**: Low — this is an implementation detail that would naturally be covered during report emitter development (Phase 2 task 2.1), but the explicit YAML injection prevention requirement is not called out.
- **Recommended Correction**: Add `yaml.safe_dump()` requirement to Phase 2 task 2.1 description or validation checkpoint.

### DEV-012
- **ID**: DEV-012
- **Severity**: LOW
- **Deviation**: Spec Section 5.4 example report shows `blocking_findings: 3` for a report with `rollout_mode: shadow`, but per the spec's own blocking_for_mode logic (Section 5.1), shadow mode should always have `blocking_findings: 0`.
- **Spec Quote**: Section 5.4 example: `rollout_mode: shadow` with `blocking_findings: 3`. Section 5.6: "shadow: `blocking_findings = 0` always"
- **Roadmap Quote**: Not directly relevant — this is an internal spec inconsistency the roadmap inherits.
- **Impact**: Low — this is a spec-internal inconsistency (the example contradicts the logic). The roadmap correctly implements the logic ("shadow always passes") in its validation checkpoints.
- **Recommended Correction**: Fix the spec example to show `blocking_findings: 0` when `rollout_mode: shadow`.

## Summary

**Severity Distribution**: 2 HIGH, 6 MEDIUM, 4 LOW (12 total)

The two HIGH deviations are significant:

1. **DEV-001** (phantom FR/NFR IDs): The roadmap references ~30+ requirement IDs (FR-004 through FR-038, NFR-001 through NFR-014) that don't exist in the spec. This breaks traceability entirely — no implementer can verify which spec requirement a task satisfies.

2. **DEV-002** (analysis function file placement): The roadmap places the three core analysis functions in `wiring_analyzer.py`, but the spec explicitly reserves that file for the ToolOrchestrator AST plugin and places analysis in `wiring_gate.py`. This will produce incorrect module boundaries if followed literally.

The MEDIUM deviations are mostly cases where the roadmap treats spec-committed decisions as open questions (DEV-005, DEV-006), omits explicit tasks for spec-required updates (DEV-004), or loses implementation detail (DEV-008). The LOW deviations are minor specification details not reproduced in the roadmap that would likely be caught during implementation.

**Tasklist readiness**: NOT READY — 2 HIGH severity deviations must be resolved before generating a tasklist.
