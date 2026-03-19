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
- **Severity**: MEDIUM
- **Deviation**: Roadmap references FR-NNN requirement IDs (e.g., FR-009, FR-010, FR-012) that do not exist in the specification. The spec uses G-NNN (goals), SC-NNN (success criteria), and D-NNN (decisions) — no "FR-" identifiers are defined anywhere.
- **Spec Quote**: Goals table uses `G-001` through `G-008`; Success Criteria uses `SC-001` through `SC-014`; no `FR-` prefix appears.
- **Roadmap Quote**: `"FR-009, FR-011"` (Phase 1, Task 1.1a), `"FR-010"` (Task 1.1b), `"FR-012, FR-014"` (Task 1.2), etc. — over 30 FR-references throughout.
- **Impact**: Implementers cannot trace roadmap tasks back to spec requirements. Every "Requirements" column in the roadmap task tables references phantom identifiers, breaking traceability.
- **Recommended Correction**: Replace all FR-NNN references with the corresponding G-NNN, SC-NNN, or spec section numbers. If functional requirements are intended, they must first be defined in the spec.

### DEV-002
- **ID**: DEV-002
- **Severity**: MEDIUM
- **Deviation**: Roadmap references NFR-NNN identifiers (NFR-001, NFR-003, NFR-004, NFR-005, NFR-006, NFR-007, NFR-008, NFR-009, NFR-011, NFR-012, NFR-013, NFR-014) that are not defined in the specification. The spec mentions NFR-007 as a label for the layering constraint but does not define a numbered NFR table.
- **Spec Quote**: `"### 3.2 Preserve layering (NFR-007)"` — only NFR-007 is mentioned by ID; no NFR enumeration table exists.
- **Roadmap Quote**: `"NFR-003, NFR-004"` (Phase 1 validation), `"NFR-001"` (Phase 1 checkpoint), `"NFR-005"` (Phase 2 Task 2.1), etc.
- **Impact**: NFR traceability is broken for all but NFR-007. Implementers cannot verify which non-functional requirements are being addressed.
- **Recommended Correction**: Either add a formal NFR table to the spec (defining NFR-001 through NFR-014), or replace roadmap NFR references with direct spec section citations.

### DEV-003
- **ID**: DEV-003
- **Severity**: HIGH
- **Deviation**: Roadmap places analysis functions (`analyze_unwired_callables`, `analyze_orphan_modules`, `analyze_unwired_registries`) in `cli/audit/wiring_analyzer.py`, but the spec places the core analysis functions and data models in `cli/audit/wiring_gate.py` (280-320 LOC for "Core analysis + gate definition + report emitter").
- **Spec Quote**: `"src/superclaude/cli/audit/wiring_gate.py | 280-320 | Core analysis + gate + emitter"` (Section 12, File Manifest); Section 5.1 shows data models under comment `# src/superclaude/cli/audit/wiring_gate.py`
- **Roadmap Quote**: `"1.2 Implement unwired callable analysis | cli/audit/wiring_analyzer.py"`, `"1.3 Implement orphan module analysis | cli/audit/wiring_analyzer.py"`, `"1.4 Implement registry analysis | cli/audit/wiring_analyzer.py"`
- **Impact**: The spec's `wiring_analyzer.py` (140-180 LOC) is exclusively the ToolOrchestrator AST plugin. Moving core analysis into it conflates two components with different cut criteria — the analyzer plugin is deferrable (Section 5.3.1), but core analysis is not. File LOC budgets will also be wrong.
- **Recommended Correction**: Move analysis function tasks (1.2, 1.3, 1.4) to target `cli/audit/wiring_gate.py` per the spec's file manifest and module map.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Spec defines `wiring_analyzer.py` as exclusively the ToolOrchestrator AST plugin (140-180 LOC), but the roadmap uses it as the location for both core analysis functions AND the ToolOrchestrator plugin, blurring the separation.
- **Spec Quote**: `"src/superclaude/cli/audit/wiring_analyzer.py | 140-180 | AST analyzer for ToolOrchestrator"` (Section 12)
- **Roadmap Quote**: Phase 1 tasks 1.2-1.4 and 1.6 all target `cli/audit/wiring_analyzer.py`; Phase 5 task 5.1 also targets `cli/audit/wiring_analyzer.py`
- **Impact**: The spec's clean separation between core gate logic and the optional ToolOrchestrator plugin is lost. The cut criteria in Section 5.3.1 assume these are separate modules.
- **Recommended Correction**: Ensure Phase 1 core analysis functions go in `wiring_gate.py`; reserve `wiring_analyzer.py` for Phase 5 ToolOrchestrator plugin only.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Roadmap adds `wiring_whitelist.yaml` as a new file in the file manifest, but the spec does not list it as a new file — it only describes the whitelist schema within Section 5.2.1.
- **Spec Quote**: Section 12 New Files table lists 7 entries: `wiring_gate.py`, `wiring_config.py`, `wiring_analyzer.py`, `test_wiring_gate.py`, `test_wiring_analyzer.py`, `test_wiring_integration.py`, `fixtures/`
- **Roadmap Quote**: `"wiring_whitelist.yaml | Optional suppression config"` (New Files section)
- **Impact**: LOW — the whitelist file is implied by the spec's whitelist schema. However, adding it without spec authorization could cause confusion about scope.
- **Recommended Correction**: Either add `wiring_whitelist.yaml` to the spec's file manifest as an optional file, or note it as an implementation artifact in the roadmap.

### DEV-006
- **ID**: DEV-006
- **Severity**: LOW
- **Deviation**: Spec's test LOC estimate is "370-480 lines test code" (frontmatter) and "~420-560 test" (Section 12), but the roadmap states "~420-560 LOC test code" in the executive summary.
- **Spec Quote**: `"estimated_scope: 480-580 lines production code, 370-480 lines test code"` (frontmatter)
- **Roadmap Quote**: `"~420-560 LOC test code"` (Executive Summary)
- **Impact**: Minor inconsistency. The roadmap uses the Section 12 estimate rather than the frontmatter estimate.
- **Recommended Correction**: Reconcile the spec's own inconsistency (frontmatter says 370-480, Section 12 says 420-560) and use the canonical number.

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: The roadmap adds risk R9 (merge conflicts with concurrent PRs) which is not in the spec's risk table. While the spec's Section 15 discusses merge coordination, it does not assign it a risk ID.
- **Spec Quote**: Risk table (Section 9) lists R1-R8 only. Section 15 discusses merge conflict risk narratively.
- **Roadmap Quote**: `"R9: Merge conflicts with concurrent PRs | Integration delays"` (Medium Severity risks)
- **Impact**: Adds a risk not formally defined in the spec. This is beneficial but represents a deviation.
- **Recommended Correction**: Either add R9 to the spec's risk table, or note in the roadmap that R9 is roadmap-originated, not spec-originated.

### DEV-008
- **ID**: DEV-008
- **Severity**: HIGH
- **Deviation**: The spec's tasklist (Section 13) shows T05 depends on T01 only, but the roadmap sequences analysis functions (Phase 1) before report emission (Phase 2), effectively making T05 depend on T02-T04 as well. More critically, the spec's critical path shows `T01 -> T02/T03/T04/T06 (parallel) -> T05`, meaning T05 starts after T02-T04 complete. The roadmap correctly follows this sequencing, BUT the roadmap's Phase 1 Task 1.6 (`ast_analyze_file()`) is placed as a core analysis task while the spec assigns it to T06 (ToolOrchestrator plugin, deferrable).
- **Spec Quote**: `"T06 | AST analyzer plugin for ToolOrchestrator | T01 | 160"` (Section 13); Section 5.3.1: `"Core wiring gate functionality (T01-T05, T07-T10) does not depend on the ToolOrchestrator plugin"`
- **Roadmap Quote**: `"1.6 Implement ast_analyze_file() utility | cli/audit/wiring_analyzer.py | FR-020, FR-021 | 40-50"` (Phase 1)
- **Impact**: The roadmap places `ast_analyze_file()` in the core Phase 1 (non-deferrable) while the spec assigns it to T06 (deferrable, with explicit cut criteria). This undermines the spec's explicit risk mitigation: if Phase 1 runs long, the implementer won't know that `ast_analyze_file()` can be deferred.
- **Recommended Correction**: Move Task 1.6 to Phase 5 (ToolOrchestrator Plugin) to match spec's T06 assignment and cut criteria.

### DEV-009
- **ID**: DEV-009
- **Severity**: MEDIUM
- **Deviation**: The roadmap's Phase 3a validation checkpoint mentions layering check as `"No imports from pipeline/* into roadmap/* or audit/*"` which reverses the spec's layering direction.
- **Spec Quote**: `"pipeline/* --MUST NOT import--> roadmap/*, audit/*, sprint/*"` (Section 3.2)
- **Roadmap Quote**: `"No imports from pipeline/* into roadmap/* or audit/* violating layering (NFR-007)"` (Phase 3a validation)
- **Impact**: The roadmap text says "from pipeline/* into roadmap/*" which means pipeline importing from roadmap — this actually matches the spec's intent. The phrasing is correct but uses "into" ambiguously. Minor clarity issue.
- **Recommended Correction**: Rephrase to: "No imports in pipeline/* from roadmap/*, audit/*, or sprint/*" for unambiguous direction.

### DEV-010
- **ID**: DEV-010
- **Severity**: LOW
- **Deviation**: The spec explicitly documents `_get_all_step_ids()` synchronization as a mandatory Step 5 of the 5-step integration process. The roadmap mentions it only in a validation checkpoint, not as an explicit task.
- **Spec Quote**: `"Step 5: Update _get_all_step_ids() (line 538) and ALL_GATES (line 933). _get_all_step_ids() MUST be updated to include 'wiring-verification' after 'spec-fidelity' and before 'remediate'."` (Section 5.7)
- **Roadmap Quote**: Phase 3a validation checkpoint: `"_get_all_step_ids() returns wiring-verification between spec-fidelity and remediate"` — but no explicit task for updating `_get_all_step_ids()`.
- **Impact**: The `_get_all_step_ids()` update is implied by Task 3a.2/3a.3 but not called out explicitly. An implementer could miss this synchronization requirement.
- **Recommended Correction**: Add an explicit sub-task in Phase 3a for updating `_get_all_step_ids()`, or note it as part of Task 3a.2.

### DEV-011
- **ID**: DEV-011
- **Severity**: LOW
- **Deviation**: The spec's Section 8.2 Gate Contract table lists `audit_artifacts_used` as a required frontmatter field, but the roadmap's Phase 0 lists it as an open question (OQ-1: "How are audit_artifacts_used located/counted?").
- **Spec Quote**: Report format (Section 5.4) shows `audit_artifacts_used: 0` in frontmatter; Gate Definition (Section 5.6) includes it in `required_frontmatter_fields`
- **Roadmap Quote**: `"OQ-1 | How are audit_artifacts_used located/counted? | Glob for *-audit-report.yaml in output dir"` (Phase 0)
- **Impact**: The field is specified but the counting mechanism is left as an open question — this is appropriate roadmap behavior (surfacing implementation detail gaps), not a true deviation.
- **Recommended Correction**: No action needed. The open question addresses implementation mechanics, not whether the field exists.

### DEV-012
- **ID**: DEV-012
- **Severity**: MEDIUM
- **Deviation**: The spec defines the `run_wiring_analysis()` public API signature with `config: WiringConfig | None = None` (Section 8.1), but the roadmap does not reference the `config` parameter in any integration task. The roadmap's executor special-case code (Phase 3a.3) will need to pass `config` but no task mentions sourcing `WiringConfig` from `RoadmapConfig` or `SprintConfig`.
- **Spec Quote**: `"def run_wiring_analysis(target_dir: Path, config: WiringConfig | None = None) -> WiringReport"` (Section 8.1)
- **Roadmap Quote**: No task addresses how `WiringConfig` is instantiated or plumbed through roadmap/sprint configuration. Phase 3a.3 describes special-casing but doesn't mention config parameter.
- **Impact**: Implementers may miss the config plumbing, resulting in `None` always being passed and default config always used. This may be intentional for v2.0 but is not stated.
- **Recommended Correction**: Add a note to Phase 3a.3 or 3b.2 about whether `WiringConfig` is explicitly constructed from pipeline/sprint config or left as `None` (default) for v2.0.

### DEV-013
- **ID**: DEV-013
- **Severity**: LOW
- **Deviation**: The spec describes the `build_wiring_verification_prompt()` signature as `(merge_file: Path, spec_source: str) -> str` (Section 5.7), but the roadmap describes it only as a "stub" without specifying the signature parameters.
- **Spec Quote**: `"def build_wiring_verification_prompt(merge_file: Path, spec_source: str) -> str:"` (Section 5.7, Step 2)
- **Roadmap Quote**: `"3a.1 Add build_wiring_verification_prompt() stub | roadmap/prompts.py | FR-029 | 5"` (Phase 3a)
- **Impact**: Minor — the signature is fully specified in the spec. The roadmap omitting it in the task description is a detail-level gap.
- **Recommended Correction**: No action needed; implementers should reference the spec for the full signature.

---

## Summary

**Severity Distribution**: 2 HIGH, 7 MEDIUM, 4 LOW (13 total deviations)

**HIGH severity issues** (blocking tasklist generation):

1. **DEV-003/DEV-004**: Core analysis functions are mapped to `wiring_analyzer.py` in the roadmap but belong in `wiring_gate.py` per the spec. This conflates the deferrable ToolOrchestrator plugin with non-deferrable core analysis, breaking the spec's file boundaries and LOC budgets.

2. **DEV-008**: `ast_analyze_file()` is placed in Phase 1 (core, non-deferrable) by the roadmap, but the spec assigns it to T06 (ToolOrchestrator plugin) with explicit cut criteria allowing deferral to v2.1.

**Key MEDIUM issues**: Phantom FR-NNN and NFR-NNN requirement identifiers throughout the roadmap (DEV-001, DEV-002) break traceability. WiringConfig plumbing is unaddressed (DEV-012).

**Overall assessment**: The roadmap faithfully captures the spec's architecture, rollout strategy, and phasing structure. The deviations are primarily in file-to-task mapping (where analysis code lives) and requirement identifier traceability. Correcting DEV-003/DEV-008 is required before tasklist generation.
