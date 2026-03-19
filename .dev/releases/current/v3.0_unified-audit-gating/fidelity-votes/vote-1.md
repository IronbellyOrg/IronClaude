---
high_severity_count: 3
medium_severity_count: 8
low_severity_count: 4
total_deviations: 15
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: Roadmap references FR-NNN requirement IDs (FR-009 through FR-038, NFR-001 through NFR-014) that do not exist anywhere in the specification. The spec uses G-NNN (goals), SC-NNN (success criteria), and D-N (decisions) identifiers exclusively. The roadmap appears to have fabricated a parallel numbering scheme.
- **Spec Quote**: Goals use `G-001` through `G-008`; success criteria use `SC-001` through `SC-014`; decisions use `D1` through `D7`. No `FR-NNN` or `NFR-NNN` identifiers appear in the spec.
- **Roadmap Quote**: `'FR-009, FR-011'` (Task 1.1a), `'FR-010'` (Task 1.1b), `'NFR-003, NFR-004'` (Task 1.7), `'NFR-001'` (Phase 1 validation), and 30+ additional FR/NFR references throughout.
- **Impact**: Implementers cannot trace roadmap tasks back to spec requirements. Traceability is broken — no way to verify coverage or confirm that all spec requirements are addressed without guessing which FR maps to which spec section.
- **Recommended Correction**: Replace all FR-NNN/NFR-NNN references with the actual spec identifiers (G-NNN, SC-NNN, section numbers) or add a traceability matrix mapping FR/NFR IDs to spec sections.

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Deviation**: Spec places analysis functions (`analyze_unwired_callables`, `analyze_orphan_modules`, `analyze_unwired_registries`) in `audit/wiring_gate.py` per Section 5.2 context and module map (Section 4.2: "wiring_gate.py — Core analysis + gate definition + report emitter"). Roadmap places all three analyzers in `cli/audit/wiring_analyzer.py` (Tasks 1.2, 1.3, 1.4).
- **Spec Quote**: Module map Section 4.2: `wiring_gate.py CREATE Core analysis + gate definition + report emitter`; Section 5.2 analysis functions are introduced under the `wiring_gate.py` file header; Section 12 File Manifest: `wiring_gate.py 280-320 Core analysis + gate + emitter`; `wiring_analyzer.py 140-180 AST analyzer for ToolOrchestrator`
- **Roadmap Quote**: `'1.2 Implement unwired callable analysis | cli/audit/wiring_analyzer.py'`, `'1.3 Implement orphan module analysis | cli/audit/wiring_analyzer.py'`, `'1.4 Implement registry analysis | cli/audit/wiring_analyzer.py'`
- **Impact**: The spec designates `wiring_analyzer.py` exclusively for the ToolOrchestrator AST plugin (Section 5.3), while `wiring_gate.py` holds core analysis + gate + emitter. Moving analysis functions to `wiring_analyzer.py` changes the module boundaries, potentially making `wiring_gate.py` undersized (280-320 LOC without analysis code is implausible) and `wiring_analyzer.py` oversized.
- **Recommended Correction**: Align file assignments with spec: analysis functions belong in `wiring_gate.py`; `wiring_analyzer.py` is reserved for the ToolOrchestrator AST plugin per Section 5.3.

### DEV-003
- **ID**: DEV-003
- **Severity**: HIGH
- **Deviation**: Spec Section 5.7 Step 5 explicitly requires updating `_get_all_step_ids()` as part of roadmap integration. The roadmap's Phase 3a task list covers `_build_steps()` (3a.2), executor special-casing (3a.3), and `ALL_GATES` registration (3a.4), but has no explicit task for updating `_get_all_step_ids()`.
- **Spec Quote**: `'Step 5: Update _get_all_step_ids() (line 538) and ALL_GATES (line 933). _get_all_step_ids() MUST be updated to include "wiring-verification" after "spec-fidelity" and before "remediate".'`
- **Roadmap Quote**: Phase 3a validation checkpoint mentions `'_get_all_step_ids() returns wiring-verification between spec-fidelity and remediate'` but no task explicitly creates this change. Task 3a.4 only covers `ALL_GATES`.
- **Impact**: `_get_all_step_ids()` is critical for resume behavior (Section 5.7.2). Omitting it as an explicit task risks it being missed, breaking pipeline resume for the wiring-verification step.
- **Recommended Correction**: Add explicit task or expand 3a.2/3a.4 to include `_get_all_step_ids()` update with clear reference to spec Section 5.7 Step 5.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Roadmap Phase 1 validation checkpoint states performance target as `< 2s for 50-file fixture (NFR-001)`, while the spec states `< 5s for 50 files` in SC-008 and `< 2s` only for sprint performance (R4 mitigation). The roadmap conflates the sprint-specific 2s target with the general analysis benchmark.
- **Spec Quote**: SC-008: `'Analysis < 5s for 50 files | Benchmark'`; Risk R4: `'AST-only, no subprocess; < 2s'` (sprint-specific context)
- **Roadmap Quote**: Phase 1 validation: `'Performance: < 2s for 50-file fixture (NFR-001)'`; Phase 3b: `'<2s target; <5s hard budget'`
- **Impact**: Phase 1 may unnecessarily fail validation against a 2s target when the spec allows 5s. The Phase 3b section correctly distinguishes both targets but Phase 1 does not.
- **Recommended Correction**: Phase 1 validation should use `< 5s` (SC-008) as the benchmark target; the `< 2s` aspiration applies to sprint integration context.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Spec Section 5.2.1 defines whitelist validation behavior: "In Phase 1 (shadow), malformed entries are logged as WARNING and skipped. In Phase 2+, malformed entries raise `WiringConfigError`." The roadmap's OQ-3 treats this as an open question with a "Proposed Default" rather than a settled spec decision.
- **Spec Quote**: `'Validation: entries missing symbol or reason are MALFORMED. In Phase 1 (shadow), malformed entries are logged as WARNING and skipped. In Phase 2+, malformed entries raise WiringConfigError.'`
- **Roadmap Quote**: OQ-3: `'Is whitelist strictness derived from rollout_mode? | shadow → WARNING; soft/full → WiringConfigError | Opus'`
- **Impact**: Treating a decided spec requirement as an open question could lead to re-deliberation and divergent implementation if Phase 0 reaches a different conclusion.
- **Recommended Correction**: Remove OQ-3 from open questions; reference spec Section 5.2.1 as the decided behavior.

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: Spec Section 7 Phase 1 pre-activation checklist has two items including "First-run zero-findings sanity check (>50 files must produce >0 findings)". The roadmap places pre-activation safeguards in Phase 3b (Task 3b.3) under sprint integration, not as a Phase 1 deliverable.
- **Spec Quote**: `'Pre-activation checklist (blocking): 1. Confirm provider_dir_names matches at least one real directory 2. First-run zero-findings sanity check (>50 files must produce >0 findings)'`
- **Roadmap Quote**: Task 3b.3: `'Pre-activation safeguards (zero-match warning, whitelist validation) | sprint/executor.py | SC-010 | 15-20'`
- **Impact**: Deferring pre-activation checks to Phase 3b means Phase 1 could produce a seemingly-working analyzer that actually scans zero relevant files, wasting Phases 2-3a.
- **Recommended Correction**: Add pre-activation sanity check as a Phase 1 validation item in addition to the sprint-specific safeguards in Phase 3b.

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: Spec Section 5.4 requires `yaml.safe_dump()` for string-valued frontmatter fields to prevent YAML injection. No roadmap task explicitly addresses this serialization safety requirement.
- **Spec Quote**: `'Serialization: All string-valued frontmatter fields MUST use yaml.safe_dump() to prevent YAML injection. Integer/boolean gate-evaluated fields are exempt.'`
- **Roadmap Quote**: Task 2.1 mentions `'NFR-005'` but provides no detail on YAML injection prevention. '[MISSING]' as explicit task or validation criterion.
- **Impact**: YAML injection in report frontmatter could corrupt gate evaluation. Without an explicit task or test, this security requirement may be overlooked.
- **Recommended Correction**: Add explicit acceptance criterion to Task 2.1 or Task 2.6 covering `yaml.safe_dump()` usage for string fields.

### DEV-008
- **ID**: DEV-008
- **Severity**: MEDIUM
- **Deviation**: Spec Section 5.7 defines the executor special-case returning `StepResult(step=step, status=StepStatus.PASS)`, which always returns PASS regardless of analysis results (gate evaluation happens separately). The roadmap Task 3a.3 does not specify this return behavior.
- **Spec Quote**: `'if step.id == "wiring-verification": report = run_wiring_analysis(target_dir=config.source_dir) emit_report(report, step.output_file, enforcement_mode=config.wiring_rollout_mode) return StepResult(step=step, status=StepStatus.PASS)'`
- **Roadmap Quote**: Task 3a.3: `'Special-case executor for wiring-verification step | roadmap/executor.py | FR-031, NFR-011 | 20-30'`
- **Impact**: If the implementer misinterprets the executor special-case and gates within the step execution (rather than via the separate gate evaluation), the shadow/trailing mode semantics break.
- **Recommended Correction**: Add note to Task 3a.3 specifying that the executor must return `StepStatus.PASS` unconditionally and rely on gate evaluation for enforcement.

### DEV-009
- **ID**: DEV-009
- **Severity**: MEDIUM
- **Deviation**: Spec Section 5.7.2 documents resume behavior requirements (3 conditions for correct resume). The roadmap has no task or validation criterion covering resume behavior.
- **Spec Quote**: `'No special resume handling is required. The existing resume mechanism detects the output file, evaluates the gate, and skips the step if the gate passes.'` with 3 preconditions listed.
- **Roadmap Quote**: '[MISSING]'
- **Impact**: Resume behavior correctness depends on deterministic output and `_get_all_step_ids()` update. Without explicit validation, resume regressions could go undetected.
- **Recommended Correction**: Add resume behavior validation to Phase 3a integration tests (Task 3a.5).

### DEV-010
- **ID**: DEV-010
- **Severity**: MEDIUM
- **Deviation**: Spec Section 7 Phase 1 includes `grace_period` interaction note documenting the relationship between `grace_period=0` and BLOCKING mode. The roadmap's OQ-6 treats `grace_period` ownership as an open question but does not capture the specific interaction behavior documented in the spec.
- **Spec Quote**: `'Roadmap configurations should set grace_period > 0 during shadow rollout to enable GateMode.TRAILING behavior via TrailingGateRunner. If grace_period = 0 forces BLOCKING (per pipeline/executor.py:160-163), shadow mode still passes because _zero_blocking_findings_for_mode reads rollout_mode=shadow from frontmatter and returns True unconditionally'`
- **Roadmap Quote**: OQ-6: `'Rollout ownership for grace_period? | Single accountable owner for shadow metrics and activation'`
- **Impact**: The operational detail about `grace_period` interaction is important for correct shadow deployment but is reduced to an ownership question in the roadmap.
- **Recommended Correction**: Add a deployment note to Phase 3a or 6a documenting the `grace_period > 0` requirement for clean TRAILING semantics.

### DEV-011
- **ID**: DEV-011
- **Severity**: MEDIUM
- **Deviation**: Spec Section 8.2 Gate Contract table lists `audit_artifacts_used` as a required frontmatter field, but the roadmap's OQ-1 treats its location/counting mechanism as an open question.
- **Spec Quote**: Section 5.4 report format includes `'audit_artifacts_used: 0'`; Section 5.6 WIRING_GATE `required_frontmatter_fields` includes `'audit_artifacts_used'`
- **Roadmap Quote**: OQ-1: `'How are audit_artifacts_used located/counted? | Glob for *-audit-report.yaml in output dir'`
- **Impact**: The field is spec-required but the counting mechanism is unresolved. Minor: the spec defines the field as required but leaves the counting mechanism implicit.
- **Recommended Correction**: Resolve as a design detail in Phase 1 (Task 1.1a config) rather than a Phase 0 open question, since the field existence is already decided.

### DEV-012
- **ID**: DEV-012
- **Severity**: LOW
- **Deviation**: Spec test LOC estimate is "370-480 lines test code" (frontmatter) and "~420-560 test" (Section 12). Roadmap states "~420-560 LOC test code".
- **Spec Quote**: Frontmatter: `'estimated_scope: 480-580 lines production code, 370-480 lines test code'`; Section 12: `'~480-580 new prod + ~420-560 test + ~113 modified'`
- **Roadmap Quote**: `'~420-560 LOC test code'`
- **Impact**: Internal spec inconsistency between frontmatter (370-480) and body (420-560). Roadmap follows the body number. No practical impact.
- **Recommended Correction**: Reconcile spec frontmatter with Section 12 estimate.

### DEV-013
- **ID**: DEV-013
- **Severity**: LOW
- **Deviation**: Roadmap adds a risk R9 (merge conflicts with concurrent PRs) that is not in the spec's risk table (Section 9). The spec covers this in Section 15 (Coordination Notes) but not as a numbered risk.
- **Spec Quote**: Section 15: `'Merge conflict risk when modifying roadmap/gates.py -- coordinate with...'`
- **Roadmap Quote**: `'R9: Merge conflicts with concurrent PRs | Integration delays | Sequence: complete Phases 1-2 before touching shared files'`
- **Impact**: Additive; captures spec content as a formal risk. No correctness issue.
- **Recommended Correction**: None required; the roadmap's formalization is reasonable.

### DEV-014
- **ID**: DEV-014
- **Severity**: LOW
- **Deviation**: Spec Section 10.2 lists integration test SC-010 as "cli-portify fixture produces exactly 1 unwired_callable finding". Roadmap maps SC-010 to "Run with misconfigured `provider_dir_names`, verify WARNING emitted" (manual validation).
- **Spec Quote**: Section 10.2: `'SC-010: cli-portify fixture produces exactly 1 unwired_callable finding'`; Section 11: `'SC-010 | Pre-activation warns on zero matches | Integration'`
- **Roadmap Quote**: Manual validation: `'SC-010 | Run with misconfigured provider_dir_names, verify WARNING emitted'`
- **Impact**: Internal spec inconsistency — Section 10.2 and Section 11 describe different SC-010 behaviors. Roadmap follows Section 11. The cli-portify fixture test appears to be SC-009 content misplaced in Section 10.2.
- **Recommended Correction**: Fix spec Section 10.2 to align SC-010 with Section 11's definition. Roadmap is correct.

### DEV-015
- **ID**: DEV-015
- **Severity**: LOW
- **Deviation**: Spec Section 13 tasklist shows T05 depending on T01 only, while roadmap Phase 2 (corresponding to T05) depends on Phase 1 which includes T01-T04 and T06. The roadmap's dependency is stricter.
- **Spec Quote**: `'T05 | Report emitter + WIRING_GATE + semantic checks | T01 | 100'`
- **Roadmap Quote**: Phase 2 dependencies: `'Phase 1'` (which includes all of T01-T06 equivalent tasks)
- **Impact**: Stricter dependency is conservative and correct — the emitter needs analysis functions to test against. No correctness issue.
- **Recommended Correction**: None required; roadmap's stricter phasing is prudent.

---

## Summary

**Severity Distribution**: 3 HIGH, 8 MEDIUM, 4 LOW (15 total)

**HIGH findings** center on traceability and structural fidelity:
1. **Fabricated requirement IDs** (DEV-001): The roadmap introduces FR/NFR numbering that doesn't exist in the spec, breaking traceability entirely.
2. **Module boundary violation** (DEV-002): Analysis functions placed in `wiring_analyzer.py` instead of `wiring_gate.py`, contradicting the spec's module map and LOC estimates.
3. **Missing `_get_all_step_ids()` task** (DEV-003): A spec-mandated update critical for resume behavior has no explicit roadmap task.

**MEDIUM findings** involve requirement detail loss (YAML injection, resume testing, pre-activation timing), open questions that should be closed decisions, and missing acceptance criteria for spec-defined behaviors.

**LOW findings** are internal spec inconsistencies and additive roadmap content.

**Recommendation**: Resolve all 3 HIGH deviations before generating a tasklist. DEV-001 requires a traceability matrix; DEV-002 requires file assignment correction; DEV-003 requires an explicit task addition.
