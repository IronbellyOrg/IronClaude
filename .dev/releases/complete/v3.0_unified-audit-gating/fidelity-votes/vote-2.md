---
high_severity_count: 3
medium_severity_count: 7
low_severity_count: 5
total_deviations: 15
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Dimension**: Signatures
- **Deviation**: Roadmap references non-existent FR-NNN requirement IDs throughout all phase task tables. The spec uses G-NNN (goals), SC-NNN (success criteria), and NFR-NNN naming but does not define numbered functional requirements (FR-009 through FR-038). The roadmap invents 30 FR identifiers with no spec backing.
- **Spec Quote**: Goals table uses 'G-001' through 'G-008'; success criteria use 'SC-001' through 'SC-014'; NFRs referenced as 'NFR-007' etc. No 'FR-NNN' identifiers appear anywhere in the specification.
- **Roadmap Quote**: 'FR-009, FR-011' (Task 1.1a), 'FR-010' (Task 1.1b), 'FR-012, FR-014' (Task 1.2), 'FR-015, FR-016, FR-017' (Task 1.3), ... through 'FR-038' (Task 4.3)
- **Impact**: Implementers cannot trace roadmap tasks back to specification requirements. The traceability chain is broken — every task references requirements that don't exist in the spec. This undermines the entire gate-based verification model.
- **Recommended Correction**: Replace all FR-NNN references with the actual spec identifiers. Map each roadmap task to the corresponding G-NNN goal, SC-NNN success criterion, or spec section number. Alternatively, add a formal FR requirements section to the spec and trace each FR to its parent goal/SC.

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Dimension**: Signatures
- **Deviation**: Roadmap references NFR identifiers (NFR-001, NFR-003, NFR-004, NFR-005, NFR-006, NFR-008, NFR-009, NFR-011, NFR-012, NFR-013, NFR-014) that are not defined in the spec. The spec references NFR-007 (layering constraint) contextually but has no enumerated NFR table.
- **Spec Quote**: 'Preserve layering (NFR-007)' in Section 3.2. No other NFR identifiers are defined.
- **Roadmap Quote**: 'Performance: < 2s for 50-file fixture (NFR-001)' (Phase 1), '90% coverage on wiring_gate.py and wiring_analyzer.py' referencing 'NFR-003' (Phase 2), 'NFR-013' for additive-only agent extensions (Phase 4)
- **Impact**: 13 of the 14 NFR references in the roadmap point to undefined requirements. Implementers have no authoritative definition for performance targets (NFR-001), coverage thresholds (NFR-003), test count minimums (NFR-004), or other non-functional constraints. The spec contains these requirements as prose (e.g., Section 10.3 specifies >=90% coverage) but they lack formal NFR identifiers.
- **Recommended Correction**: Either (a) add a formal NFR table to the spec enumerating all referenced NFRs with their definitions, or (b) replace roadmap NFR references with spec section citations (e.g., "Section 10.3: >=90% coverage" instead of "NFR-003").

### DEV-003
- **ID**: DEV-003
- **Severity**: HIGH
- **Dimension**: Data Models
- **Deviation**: Roadmap places all three analysis functions (`analyze_unwired_callables`, `analyze_orphan_modules`, `analyze_unwired_registries`) in `cli/audit/wiring_analyzer.py`, whereas the spec places the analysis functions and data models in `cli/audit/wiring_gate.py` (Section 5.1-5.2) and reserves `wiring_analyzer.py` solely for the ToolOrchestrator AST plugin (Section 5.3).
- **Spec Quote**: Section 4.2 Module Map: 'wiring_gate.py CREATE Core analysis + gate definition + report emitter' and 'wiring_analyzer.py CREATE AST analyzer plugin for ToolOrchestrator'. Section 5.2 analysis functions are under the heading '# src/superclaude/cli/audit/wiring_gate.py'.
- **Roadmap Quote**: Phase 1 tasks: '1.2 Implement unwired callable analysis | cli/audit/wiring_analyzer.py', '1.3 Implement orphan module analysis | cli/audit/wiring_analyzer.py', '1.4 Implement registry analysis | cli/audit/wiring_analyzer.py'
- **Impact**: Implementers following the roadmap will create a different file layout than the spec prescribes. The spec's `wiring_gate.py` at 280-320 LOC includes analysis + gate + emitter. Moving analysis to `wiring_analyzer.py` changes the module responsibilities and may conflict with the ToolOrchestrator plugin's location in the same file. The LOC estimates also become inconsistent.
- **Recommended Correction**: Align roadmap file assignments with spec Section 4.2: analysis functions go in `wiring_gate.py`, and `wiring_analyzer.py` is reserved for the `ast_analyze_file()` ToolOrchestrator plugin only.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Dimension**: Gates
- **Deviation**: Roadmap's Phase 1 validation checkpoint specifies "< 2s for 50-file fixture" while the spec states "< 5s for 50 files" (SC-008) with "< 2s" mentioned only as the sprint performance target (R4).
- **Spec Quote**: 'SC-008 | Analysis < 5s for 50 files | Benchmark' (Section 11) and 'R4: Sprint performance impact | L | M | AST-only, no subprocess; < 2s' (Section 9)
- **Roadmap Quote**: 'Performance: < 2s for 50-file fixture (NFR-001)' (Phase 1 validation checkpoint) and 'AST-only analysis; <2s target; <5s hard budget' (R4 mitigation)
- **Impact**: The roadmap conflates the sprint-specific < 2s target with the general analysis benchmark of < 5s. Phase 1 builds the standalone analyzer — the < 2s target is sprint-context-specific. Using the stricter target for standalone validation may cause unnecessary optimization work.
- **Recommended Correction**: Phase 1 checkpoint should use SC-008's "< 5s for 50 files". The < 2s target applies to Phase 3b sprint integration context.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Dimension**: Gates
- **Deviation**: Roadmap adds `audit_artifacts_used` to the Gate Contract frontmatter fields list (visible in Phase 2 validation: "17 required fields") but the spec's Gate Contract table in Section 8.2 lists only 16 fields — `audit_artifacts_used` is missing from the Section 8.2 table while present in the Section 5.4 example frontmatter and Section 5.6 WIRING_GATE definition.
- **Spec Quote**: Section 8.2 Gate Contract table contains 16 rows ending with 'whitelist_entries_applied'. Section 5.6 WIRING_GATE `required_frontmatter_fields` includes 'audit_artifacts_used'. Section 5.4 example frontmatter includes 'audit_artifacts_used: 0'.
- **Roadmap Quote**: 'Report frontmatter contains all 17 required fields' (Phase 2 validation checkpoint)
- **Impact**: Internal spec inconsistency that the roadmap correctly resolves (17 fields matching Section 5.6), but the spec's Section 8.2 contract table is authoritative for interface contracts and is missing `audit_artifacts_used`. This is a spec defect that the roadmap silently corrects.
- **Recommended Correction**: Add `audit_artifacts_used | int | >= 0` to the spec's Section 8.2 Gate Contract table to resolve the internal inconsistency.

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Dimension**: CLI Options
- **Deviation**: Roadmap adds a new risk R9 ("Merge conflicts with concurrent PRs") not present in the spec's risk table.
- **Spec Quote**: Section 9 Risk Assessment contains R1-R8. No R9 is defined.
- **Roadmap Quote**: 'R9: Merge conflicts with concurrent PRs | Integration delays | Sequence: complete Phases 1-2 before touching shared files' (Medium Severity risks)
- **Impact**: The roadmap introduces a risk that the spec didn't identify. While the risk is valid (and the spec's Section 15 discusses merge coordination), the numbered risk R9 has no spec backing. This is an improvement but creates traceability ambiguity.
- **Recommended Correction**: Either add R9 to the spec's Section 9 risk table, or reference it as an operational risk from Section 15 coordination notes rather than assigning it a new R-number.

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Dimension**: Gates
- **Deviation**: Spec's tasklist (Section 13) shows T05 depends on T01 only, but roadmap's Phase 2 depends on Phase 1 completion (all of T01-T04 + T06). The spec's critical path is `T01 -> T02/T03/T04/T06 (parallel) -> T05`, meaning T05 waits for the analyzers. The roadmap's phasing (Phase 2 after Phase 1) correctly reflects this but doesn't note the dependency change.
- **Spec Quote**: 'T05 | Report emitter + WIRING_GATE + semantic checks | T01 | 100' and 'Critical path: T01 -> T02/T03/T04/T06 (parallel) -> T05'
- **Roadmap Quote**: Phase 2 depends on Phase 1 completion (which includes T01-T04 + T06 equivalent tasks)
- **Impact**: The spec's task table says T05 depends only on T01, but the critical path shows T05 follows T02-T04. The roadmap resolves this inconsistency by making Phase 2 follow Phase 1 entirely, but doesn't acknowledge the spec's internal contradiction. An implementer reading only the spec's task dependency column might attempt T05 immediately after T01.
- **Recommended Correction**: Update spec Section 13 task table to show T05 depends on T02-T04 (matching the critical path), or document the roadmap's dependency interpretation.

### DEV-008
- **ID**: DEV-008
- **Severity**: MEDIUM
- **Dimension**: Data Models
- **Deviation**: Spec defines `wiring_gate_mode` type as `Literal["off", "shadow", "soft", "full"]` with default `"shadow"`, but the roadmap's Phase 3b doesn't mention the `"off"` mode or its default value.
- **Spec Quote**: 'wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"' (Section 5.8)
- **Roadmap Quote**: 'Add wiring_gate_mode to SprintConfig | sprint/models.py | FR-034 | 5' (Task 3b.1). Validation checkpoint: 'Sprint hook logs findings without affecting task status (shadow), Sprint hook warns on critical findings (soft), Sprint hook blocks on critical+major findings (full)'
- **Impact**: The `"off"` mode is omitted from the roadmap's validation checkpoint. An implementer might not test the off mode or might not implement the `if config.wiring_gate_mode != "off"` guard.
- **Recommended Correction**: Add `"off"` mode to Phase 3b validation checkpoint: "Sprint hook is completely bypassed when mode is 'off'."

### DEV-009
- **ID**: DEV-009
- **Severity**: MEDIUM
- **Dimension**: Signatures
- **Deviation**: Roadmap places `ast_analyze_file()` implementation in Phase 1 (Task 1.6) as a utility, but the spec describes it as the ToolOrchestrator plugin in Section 5.3 with a distinct purpose. The roadmap's Phase 5 then re-implements it for ToolOrchestrator integration, creating ambiguity about whether there are two functions or one.
- **Spec Quote**: Section 5.3: 'ast_analyze_file(file_path: Path, content: str) -> FileAnalysis' with 'from .tool_orchestrator import FileAnalysis' and 'Usage: ToolOrchestrator(analyzer=ast_analyze_file)'
- **Roadmap Quote**: Phase 1 Task 1.6: 'Implement ast_analyze_file() utility | cli/audit/wiring_analyzer.py | FR-020, FR-021 | 40-50'. Phase 5 Task 5.1: 'Implement AST plugin for ToolOrchestrator | cli/audit/wiring_analyzer.py | FR-008, FR-020 | 40-50'
- **Impact**: It's unclear whether Task 1.6 and Task 5.1 are the same function or different implementations. The spec has a single `ast_analyze_file()` function. If Task 1.6 builds it in Phase 1, Phase 5's cut criteria become moot since the function already exists.
- **Recommended Correction**: Clarify that Task 1.6 builds internal AST helper functions for the analyzers (not `ast_analyze_file()` which returns `FileAnalysis`), and Task 5.1 builds the ToolOrchestrator-specific `ast_analyze_file()`. Alternatively, move Task 1.6 into Phase 5 and have Phase 1 analyzers use inline AST parsing.

### DEV-010
- **ID**: DEV-010
- **Severity**: MEDIUM
- **Dimension**: Gates
- **Deviation**: Spec explicitly requires `_get_all_step_ids()` to be updated (Section 5.7, Step 5), but the roadmap's Phase 3a task list has no explicit task for this. It appears in the validation checkpoint but not as a task.
- **Spec Quote**: 'Step 5: Update _get_all_step_ids() (line 538) and ALL_GATES (line 933). _get_all_step_ids() MUST be updated to include "wiring-verification" after "spec-fidelity" and before "remediate".'
- **Roadmap Quote**: Phase 3a tasks: 3a.2 (Step to _build_steps), 3a.4 (WIRING_GATE in ALL_GATES). Validation checkpoint: '_get_all_step_ids() returns wiring-verification between spec-fidelity and remediate'
- **Impact**: `_get_all_step_ids()` update is validated but not explicitly tasked. An implementer might miss this modification since it's only in the checkpoint, not a work item. The spec calls this out as a MUST requirement with specific ordering constraints.
- **Recommended Correction**: Add explicit task "3a.5: Update `_get_all_step_ids()` to include 'wiring-verification'" or merge it into Task 3a.2.

### DEV-011
- **ID**: DEV-011
- **Severity**: LOW
- **Dimension**: Gates
- **Deviation**: Spec Section 10.1 specifies exact unit test counts per function (5+5+3+4+3 = 20 minimum), but the roadmap's Phase 1 allocates "200-250 LOC" of tests and Phase 2 allocates "100-130 LOC" without specifying per-function test counts.
- **Spec Quote**: 'analyze_unwired_callables | 5 | Detection, negative, whitelist, parse error, multi-class' ... 'ast_analyze_file | 3 | References populated, registry metadata, syntax error'
- **Roadmap Quote**: 'Unit tests for all three analyzers + whitelist | tests/audit/ | NFR-003, NFR-004, SC-001–SC-003, SC-007 | 200-250'
- **Impact**: Per-function test count guidance is lost. The overall minimum (20 unit + 3 integration) is referenced via NFR-004 but the specific distribution is not preserved.
- **Recommended Correction**: Add per-function test count targets from spec Section 10.1 to roadmap Phase 1/2 task descriptions.

### DEV-012
- **ID**: DEV-012
- **Severity**: LOW
- **Dimension**: Data Models
- **Deviation**: Spec explicitly documents the `_FRONTMATTER_RE` regex duplication rationale (Section 5.5), but the roadmap makes no mention of this design decision.
- **Spec Quote**: 'Uses the _FRONTMATTER_RE regex pattern (duplicated from pipeline/gates.py:77 as a private constant to preserve NFR-007 layering)'
- **Roadmap Quote**: 'Implement _extract_frontmatter_values() helper | cli/audit/wiring_gate.py | FR-024 | 15' — no mention of regex duplication
- **Impact**: Minor. An implementer might attempt to import the regex from pipeline/gates.py, violating NFR-007 layering. The spec's rationale prevents this.
- **Recommended Correction**: Add a note to Task 2.2 that the frontmatter regex must be duplicated (not imported) per NFR-007.

### DEV-013
- **ID**: DEV-013
- **Severity**: LOW
- **Dimension**: Signatures
- **Deviation**: Spec documents `build_wiring_verification_prompt()` signature as `(merge_file: Path, spec_source: str) -> str` (Section 5.7), but the roadmap only says "stub" without specifying the signature.
- **Spec Quote**: 'def build_wiring_verification_prompt(merge_file: Path, spec_source: str) -> str'
- **Roadmap Quote**: 'Add build_wiring_verification_prompt() stub | roadmap/prompts.py | FR-029 | 5'
- **Impact**: Minor. The signature is a trivial stub returning empty string, but omitting it could lead to a different signature.
- **Recommended Correction**: Include the full signature in Task 3a.1 description.

### DEV-014
- **ID**: DEV-014
- **Severity**: LOW
- **Dimension**: NFRs
- **Deviation**: Spec's test LOC estimate is "370-480 lines test code" (frontmatter), while the roadmap says "~420-560 LOC test code" (Executive Summary).
- **Spec Quote**: 'estimated_scope: 480-580 lines production code, 370-480 lines test code' (frontmatter)
- **Roadmap Quote**: '~420-560 LOC test code' (Executive Summary)
- **Impact**: Minor scope estimate mismatch. The roadmap's range extends higher (560 vs 480), possibly reflecting added tests from the Phase 0 open questions or the roadmap's additional validation checkpoints.
- **Recommended Correction**: Reconcile test LOC estimates. The roadmap's higher estimate may be more accurate given added integration test phases.

### DEV-015
- **ID**: DEV-015
- **Severity**: LOW
- **Dimension**: Data Models
- **Deviation**: Spec mentions `wiring_whitelist.yaml` only as a schema example in Section 5.2.1, but the roadmap lists it as a new file to create.
- **Spec Quote**: 'Whitelist: wiring_whitelist.yaml with schema:' (Section 5.2.1) — described as a schema, no file manifest entry
- **Roadmap Quote**: 'wiring_whitelist.yaml | Optional suppression config' (New Files table)
- **Impact**: Minor. The spec's file manifest (Section 12) doesn't include `wiring_whitelist.yaml`. The roadmap adds it, which is reasonable but diverges from the explicit file manifest.
- **Recommended Correction**: Add `wiring_whitelist.yaml` to the spec's Section 12 file manifest as an optional configuration file.

---

## Summary

**Severity Distribution**: 3 HIGH, 7 MEDIUM, 5 LOW (15 total deviations)

The three HIGH-severity deviations all concern **traceability**:

1. **DEV-001**: The roadmap invents ~30 FR-NNN identifiers that don't exist in the spec, breaking requirement traceability for every implementation task.
2. **DEV-002**: Similarly, 13 of 14 NFR references point to undefined identifiers.
3. **DEV-003**: Analysis function file placement contradicts the spec's module map, risking incorrect file layout.

The MEDIUM deviations involve performance target conflation (DEV-004), an internal spec inconsistency the roadmap silently corrects (DEV-005), missing validation for the "off" mode (DEV-008), ambiguous function ownership between Phase 1 and Phase 5 (DEV-009), and a missing explicit task for `_get_all_step_ids()` (DEV-010).

**Recommendation**: The roadmap is **not tasklist-ready**. The FR/NFR phantom references (DEV-001, DEV-002) must be resolved to establish traceability, and the file placement contradiction (DEV-003) must be reconciled before implementation tasks can be reliably assigned.
