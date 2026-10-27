---
high_severity_count: 2
medium_severity_count: 7
low_severity_count: 4
total_deviations: 13
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: Roadmap references fabricated requirement IDs (FR-009 through FR-038, NFR-001 through NFR-014) that do not exist in the specification
- **Spec Quote**: The specification defines goals as G-001 through G-008, success criteria as SC-001 through SC-014, and decisions as D1 through D7. No "FR-NNN" or "NFR-NNN" identifiers appear anywhere in the specification.
- **Roadmap Quote**: Tasks reference `FR-009, FR-011` (Phase 1, Task 1.1a), `FR-010` (Task 1.1b), `FR-012, FR-014` (Task 1.2), `NFR-001` (Phase 1 validation), `NFR-003, NFR-004` (Task 1.7), etc. — over 30 fabricated requirement IDs across all phases.
- **Impact**: Implementers cannot trace roadmap tasks back to specification requirements. The traceability chain is broken — any task tagged with a non-existent FR/NFR ID has no verifiable source of truth. This undermines the entire gate-based validation approach.
- **Recommended Correction**: Replace all FR-NNN/NFR-NNN references with the actual spec identifiers (G-001–G-008, SC-001–SC-014, D1–D7) or with specific spec section references (e.g., "Section 5.2.1", "Section 5.6"). If the roadmap author intended to derive functional requirements from goals, those derived requirements must be documented explicitly with traceability to the spec.

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Deviation**: Roadmap places analysis functions in `wiring_analyzer.py` but spec places them in `wiring_gate.py`
- **Spec Quote**: Section 4.2 Module Map: `wiring_gate.py CREATE Core analysis + gate definition + report emitter`; Section 5.1 code block header: `# src/superclaude/cli/audit/wiring_gate.py`; Section 12 File Manifest: `wiring_gate.py 280-320 Core analysis + gate + emitter`
- **Roadmap Quote**: Phase 1 tasks 1.2–1.4: `Implement unwired callable analysis | cli/audit/wiring_analyzer.py`, `Implement orphan module analysis | cli/audit/wiring_analyzer.py`, `Implement registry analysis | cli/audit/wiring_analyzer.py`
- **Impact**: The spec explicitly defines `wiring_gate.py` as containing core analysis + gate + emitter (280-320 LOC), and `wiring_analyzer.py` as the ToolOrchestrator AST plugin only (140-180 LOC). Moving the three analysis functions into `wiring_analyzer.py` changes the module boundaries, alters the dependency graph, and contradicts the file manifest LOC estimates. It may also break the dependency direction specified in Section 8.3.
- **Recommended Correction**: Align roadmap file assignments with spec: unwired callable, orphan module, and registry analysis functions belong in `wiring_gate.py`. `wiring_analyzer.py` should contain only the `ast_analyze_file()` ToolOrchestrator plugin and its helpers.

### DEV-003
- **ID**: DEV-003
- **Severity**: MEDIUM
- **Deviation**: Roadmap adds a new risk R9 (merge conflicts) not present in the specification's risk assessment
- **Spec Quote**: Section 9 Risk Assessment lists R1–R8. Section 15 Coordination Notes discusses merge conflict risk qualitatively but does not assign it a risk ID.
- **Roadmap Quote**: `**R9**: Merge conflicts with concurrent PRs | Integration delays | Sequence: complete Phases 1-2 before touching shared files`
- **Impact**: Minor — the roadmap elevates coordination notes to a formal risk, which is reasonable but introduces an identifier not in the spec. Could cause confusion when cross-referencing risk mitigations.
- **Recommended Correction**: Either annotate R9 as roadmap-originated (not from spec) or align with spec Section 15 by referencing it as a coordination concern rather than a numbered risk.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Spec's tasklist critical path has T05 depending on T02-T04 completing first; roadmap restructures this as separate phases
- **Spec Quote**: Section 13 Tasklist: `T05 Report emitter + WIRING_GATE + semantic checks | T01 | 100` — T05 depends only on T01. Critical path: `T01 -> T02/T03/T04/T06 (parallel) -> T05 -> T07`
- **Roadmap Quote**: Phase 2 (Report & Gate) is sequenced after Phase 1 (Core Engine) which includes tasks 1.2-1.4 (analyzers). Phase 2 depends on Phase 1 completion.
- **Impact**: The roadmap introduces a stricter dependency than the spec requires. Per the spec, T05 (report emitter + gate) depends only on T01 (data models), not on T02-T04 (analyzers). The roadmap's Phase 2 cannot start until Phase 1 (including analyzers) completes, adding unnecessary serialization to the critical path.
- **Recommended Correction**: Allow report emitter/gate definition work (Phase 2) to begin as soon as data models are complete, parallel with analyzer implementation, matching the spec's dependency graph.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits the `audit_artifacts_used` field from the gate contract frontmatter listing
- **Spec Quote**: Section 8.2 Gate Contract table includes `audit_artifacts_used` as a required frontmatter field. Section 5.6 WIRING_GATE `required_frontmatter_fields` includes `"audit_artifacts_used"`.
- **Roadmap Quote**: Phase 2 validation checkpoint: `Report frontmatter contains all 17 required fields` — correct count but `audit_artifacts_used` is not explicitly called out anywhere in the roadmap task descriptions for implementation.
- **Impact**: The field is implicitly covered by "17 required fields" but has no task or requirement reference ensuring it gets implemented. The Phase 0 OQ-1 asks how it's located/counted, suggesting it needs explicit task coverage.
- **Recommended Correction**: Add explicit task coverage for `audit_artifacts_used` computation logic in Phase 2, with traceability to the Phase 0 OQ-1 decision.

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: Roadmap does not cover the `_get_all_step_ids()` update as an explicit task
- **Spec Quote**: Section 5.7 Step 5: `_get_all_step_ids()` MUST be updated to include `"wiring-verification"` after `"spec-fidelity"` and before `"remediate"`.
- **Roadmap Quote**: Phase 3a validation checkpoint mentions: `_get_all_step_ids() returns wiring-verification between spec-fidelity and remediate`. But no task in Phase 3a explicitly covers updating `_get_all_step_ids()` — only `_build_steps()` (3a.2), executor special-casing (3a.3), and `ALL_GATES` (3a.4).
- **Impact**: The `_get_all_step_ids()` update is a spec MUST requirement (INV-003). It appears in the validation checkpoint but not as an implementable task, risking it being overlooked during execution.
- **Recommended Correction**: Add `_get_all_step_ids()` update as an explicit sub-task of 3a.2 or as a separate task 3a.5 (renumbering integration tests).

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: Roadmap does not mention the `roadmap_run_step()` executor special-casing pattern from the spec
- **Spec Quote**: Section 5.7.1: `In roadmap_run_step(), detect step.id == "wiring-verification": report = run_wiring_analysis(target_dir=config.source_dir) ...`
- **Roadmap Quote**: Task 3a.3: `Special-case executor for wiring-verification step | roadmap/executor.py | FR-031, NFR-011`
- **Impact**: The task title mentions special-casing but references fabricated FR-031/NFR-011 instead of quoting the spec's explicit code pattern. An implementer without the spec cannot determine what "special-case" means from the roadmap alone.
- **Recommended Correction**: Add a brief description referencing spec Section 5.7.1's `roadmap_run_step()` pattern, or at minimum reference the spec section directly.

### DEV-008
- **ID**: DEV-008
- **Severity**: MEDIUM
- **Deviation**: Spec test LOC estimate range differs from roadmap
- **Spec Quote**: Section 12 File Manifest: `Total: ~480-580 new prod + ~420-560 test + ~113 modified`; also spec frontmatter: `estimated_scope: 480-580 lines production code, 370-480 lines test code`
- **Roadmap Quote**: Executive Summary: `~480-580 LOC production code, ~420-560 LOC test code`
- **Impact**: The spec's own frontmatter says 370-480 test LOC while Section 12 says 420-560. The roadmap uses 420-560 (Section 12's number). The spec has an internal inconsistency that the roadmap should flag rather than silently choosing one value.
- **Recommended Correction**: Flag the spec's internal inconsistency (frontmatter says 370-480, Section 12 says 420-560) and document which estimate the roadmap follows.

### DEV-009
- **ID**: DEV-009
- **Severity**: MEDIUM
- **Deviation**: Roadmap Phase 1 validation checkpoint uses `< 2s` performance target; spec Section 9 says `< 2s` but spec SC-008 says `< 5s`
- **Spec Quote**: SC-008: `Analysis < 5s for 50 files`; Section 9 R4: `AST-only, no subprocess; < 2s`
- **Roadmap Quote**: Phase 1 validation: `Performance: < 2s for 50-file fixture (NFR-001)`; Risk R4: `<2s target; <5s hard budget`
- **Impact**: The roadmap correctly identifies both thresholds (2s target, 5s budget) in the risk section but uses only the aspirational 2s target as the Phase 1 validation checkpoint. This could cause false test failures if analysis takes 3s — acceptable per SC-008 but failing the roadmap's checkpoint.
- **Recommended Correction**: Use SC-008's `< 5s` as the pass/fail validation criterion, with `< 2s` as an aspirational target consistent with the risk section's dual threshold.

### DEV-010
- **ID**: DEV-010
- **Severity**: LOW
- **Deviation**: Roadmap omits spec Section 5.4's YAML serialization security requirement
- **Spec Quote**: Section 5.4: `All string-valued frontmatter fields MUST use yaml.safe_dump() to prevent YAML injection.`
- **Roadmap Quote**: '[MISSING]' — no task or checkpoint mentions `yaml.safe_dump()` or YAML injection prevention.
- **Impact**: Low because the report emitter task (2.1) implicitly covers this, but the MUST-level security requirement has no explicit validation checkpoint.
- **Recommended Correction**: Add `yaml.safe_dump()` usage as an explicit acceptance criterion for Task 2.1.

### DEV-011
- **ID**: DEV-011
- **Severity**: LOW
- **Deviation**: Roadmap omits spec Section 5.7's `retry_limit=0` semantics documentation requirement
- **Spec Quote**: Section 5.7 (INV-012): `retry_limit=0 semantics: Per pipeline/executor.py:158, max_attempts = retry_limit + 1. So retry_limit=0 means the step executes exactly once with no retries.`
- **Roadmap Quote**: Task 3a.2 mentions `retry_limit=0` as a parameter value but does not reference the semantics invariant.
- **Impact**: Low — the parameter is set correctly. The invariant documentation is for implementer understanding, not a functional requirement.
- **Recommended Correction**: No action required; the parameter value is correctly specified.

### DEV-012
- **ID**: DEV-012
- **Severity**: LOW
- **Deviation**: Roadmap omits spec Section 5.7.2 Resume Behavior requirements
- **Spec Quote**: Section 5.7.2: `No special resume handling is required. The existing resume mechanism detects the output file, evaluates the gate, and skips the step if the gate passes.` Three conditions listed.
- **Roadmap Quote**: '[MISSING]' — no mention of resume behavior validation.
- **Impact**: Low because the spec itself says no special handling is needed. However, the three conditions (deterministic output, reproducible gate result, step ID in `_get_all_step_ids()`) could serve as useful test assertions.
- **Recommended Correction**: Add resume behavior as a test assertion in Phase 3a integration tests.

### DEV-013
- **ID**: DEV-013
- **Severity**: LOW
- **Deviation**: Roadmap omits whitelist `wiring_whitelist.yaml` from new files in Phase 1 task listing
- **Spec Quote**: Section 5.2.1: `Whitelist: wiring_whitelist.yaml with schema: ...`
- **Roadmap Quote**: New Files table includes `wiring_whitelist.yaml | Optional suppression config` but no Phase 1 task explicitly creates or templates this file.
- **Impact**: Low — the file is listed in the resource section but not assigned to a specific implementation task. Task 1.5 covers whitelist loading but not the file itself.
- **Recommended Correction**: Add whitelist template file creation as part of Task 1.5 or 1.1a.

---

## Summary

**Severity Distribution**: 2 HIGH, 7 MEDIUM, 4 LOW (13 total deviations)

**Critical findings**:

1. **Fabricated requirement IDs (DEV-001)**: The roadmap references over 30 FR-NNN and NFR-NNN identifiers that do not exist anywhere in the specification. This completely breaks requirement traceability — the foundational purpose of a spec-to-roadmap fidelity check.

2. **Module boundary violation (DEV-002)**: The roadmap places core analysis functions in `wiring_analyzer.py` instead of `wiring_gate.py`, contradicting the spec's module map, file manifest, and LOC estimates.

**Medium findings** cluster around: dependency ordering stricter than spec requires (DEV-004), implicit coverage of explicit spec requirements without task-level traceability (DEV-005, DEV-006, DEV-007), and performance threshold ambiguity (DEV-009).

**Recommendation**: The roadmap cannot proceed to tasklist generation until DEV-001 and DEV-002 are resolved. DEV-001 requires a full traceability pass replacing fabricated IDs with spec-native references. DEV-002 requires correcting file assignments to match the spec's module map.
