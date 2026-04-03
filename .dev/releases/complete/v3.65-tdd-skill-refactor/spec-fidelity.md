---
high_severity_count: 0
medium_severity_count: 5
low_severity_count: 2
total_deviations: 7
validation_complete: true
tasklist_ready: true
---

## Deviation Report

### DEV-001
- **Severity**: MEDIUM
- **Deviation**: NFR-TDD-R.4 mischaracterized in the Requirement Traceability Matrix. The spec defines it as "Maintainability" with measurement "Auditable source-to-destination mapping table"; the roadmap labels it "sync compatibility" and maps verification to `make verify-sync`.
- **Source Quote**: `"NFR-TDD-R.4 | Maintainability | Clear file ownership by concern | Auditable source-to-destination mapping table"`
- **Roadmap Quote**: `"NFR-TDD-R.4 (sync compatibility) | Phase 5 | B | make verify-sync"`
- **Impact**: The fidelity index audit in Phase 5 Task 4 does serve as the "auditable mapping table," so the actual verification work is present — but the traceability matrix mislabels the requirement and points to the wrong verification method. An auditor checking the matrix would conclude NFR-TDD-R.4 is about sync, not maintainability.
- **Recommended Correction**: Rename the traceability matrix entry to `"NFR-TDD-R.4 (maintainability — file ownership clarity)"` and change the verification method to `"Fidelity index audit (source-to-destination mapping table)"`, referencing Phase 5 Task 4.

### DEV-002
- **Severity**: MEDIUM
- **Deviation**: Sentinel placeholder test scope in the roadmap only covers `refs/` files, not the refactored SKILL.md itself. The spec test plan says the test covers "both generated spec files."
- **Source Quote**: `"Placeholder sentinel test | both generated spec files | Zero template sentinel placeholders remain"`
- **Roadmap Quote**: `"grep -rn '{{' src/superclaude/skills/tdd/refs/ and grep -rn '<placeholder>' src/superclaude/skills/tdd/refs/ both return empty"`
- **Impact**: If the SKILL.md reduction in Phase 4 inadvertently introduces sentinel placeholders (e.g., in load-point replacement markers), they would not be caught by the roadmap's Phase 5 grep test.
- **Recommended Correction**: Extend Phase 5 Task 5 grep commands to also cover `src/superclaude/skills/tdd/SKILL.md` in addition to the `refs/` directory.

### DEV-003
- **Severity**: MEDIUM
- **Deviation**: The spec's contract validation rules include two invariants; the roadmap's Phase 4 verification gate only explicitly checks one.
- **Source Quote**: `"contract_validation_rule: - \"declared_loads ∩ forbidden_loads = ∅ for every phase\" - \"runtime_loaded_refs ⊆ declared_loads for every phase\""`
- **Roadmap Quote**: `"Phase contract validation: declared_loads ∩ forbidden_loads = ∅ for every phase"`
- **Impact**: The second rule (`runtime_loaded_refs ⊆ declared_loads`) is the runtime enforcement invariant. Without explicit verification, a phase could load an undeclared ref without failing the gate. The Phase 5 dry run (Task 9) implicitly tests this but doesn't state it as a gate criterion.
- **Recommended Correction**: Add `"runtime_loaded_refs ⊆ declared_loads for every phase"` to the Phase 4 verification gate, and add it as an explicit check in the Phase 5 behavioral parity dry run (Task 9).

### DEV-004
- **Severity**: MEDIUM
- **Deviation**: FR-TDD-R.6 acceptance criteria lists builder load dependencies as "prompts/mapping/checklists" (3 files). The roadmap extends this to "4 builder refs files" including operational-guidance, following the Section 5.3 phase contract but going beyond the FR text.
- **Source Quote**: `"Builder load dependencies for prompts/mapping/checklists are explicit."`
- **Roadmap Quote**: `"At Stage B delegation or BUILD_REQUEST: explicit builder load dependencies for the 4 builder refs files (FR-TDD-R.6b)"`
- **Impact**: The roadmap correctly follows Section 5.3 which is more complete, but claims to satisfy FR-TDD-R.6b while extending its scope. An auditor checking FR-TDD-R.6 acceptance criteria verbatim would find 4 files declared where 3 are specified. This is the spec's internal inconsistency, but the roadmap doesn't flag it.
- **Recommended Correction**: Add a note in the roadmap's Phase 4 Task 2 acknowledging the spec inconsistency: FR-TDD-R.6 text lists 3 files but Section 5.3 phase contract lists 4 (adding operational-guidance.md). The roadmap follows the phase contract as authoritative.

### DEV-005
- **Severity**: MEDIUM
- **Deviation**: The spec's Section 9 "Migration & Rollout" contains four explicit commitments (no breaking changes, backwards compatibility preserved, rollback plan via git revert, single-commit migration path). The roadmap has no corresponding section restating these commitments.
- **Source Quote**: `"Breaking changes: None; external skill interface remains unchanged. Backwards compatibility: Preserved; Stage B still delegates to /task and task items remain self-contained. Rollback plan: Revert to monolithic SKILL.md via git. Migration path: Single refactor commit plus sync/verify pass"`
- **Roadmap Quote**: [MISSING]
- **Impact**: Implementers reading only the roadmap would lack the explicit rollback strategy and compatibility guarantees. While "revert via git" is obvious for a refactoring, the spec commits to it and the roadmap should too.
- **Recommended Correction**: Add a brief "Migration & Rollout" section to the roadmap (after Resource Requirements or in the Executive Summary) restating the four commitments from spec Section 9.

### DEV-006
- **Severity**: LOW
- **Deviation**: The spec's Section 4.6 Implementation Order numbers ref file creation as sequential steps 1-5 in a specific sequence (build-request-template first). The roadmap's Phase 2 reorders them (agent-prompts first, build-request-template fourth) and declares them parallelizable.
- **Source Quote**: `"1. Create refs/build-request-template.md from source lines 341-492. 2. Create refs/agent-prompts.md from source lines 537-959."`
- **Roadmap Quote**: `"Tasks (parallelizable — each extracts from non-overlapping line ranges into separate files) 1. Create refs/agent-prompts.md (FR-TDD-R.2) ... 4. Create refs/build-request-template.md (FR-TDD-R.5)"`
- **Impact**: Minimal. The roadmap correctly identifies that extraction from non-overlapping ranges is parallelizable, and defers BUILD_REQUEST wiring to Phase 3. The reordering is an optimization, not a correctness issue.
- **Recommended Correction**: No correction needed, but the roadmap could add a note: "Extraction order differs from spec Section 4.6 numbering; all extractions are independent and parallelizable."

### DEV-007
- **Severity**: LOW
- **Deviation**: Spec Section 4.6 step 0 establishes an explicit procedural constraint: "Edit/create canonical files under `src/superclaude/skills/tdd/` only." The roadmap has no corresponding explicit task or constraint statement.
- **Source Quote**: `"0. Edit/create canonical files under /config/workspace/IronClaude/src/superclaude/skills/tdd/ only."`
- **Roadmap Quote**: [MISSING as explicit constraint, but implicit in all file paths]
- **Impact**: Low. All roadmap tasks specify `src/superclaude/skills/tdd/` paths, making the constraint implicit. However, without an explicit statement, an implementer might edit `.claude/` directly during iteration.
- **Recommended Correction**: Add a brief constraint note to the Executive Summary or Phase 2 preamble: "All edits target canonical paths under `src/superclaude/skills/tdd/` only; `.claude/` copies are produced exclusively via `make sync-dev`."

## Summary

**Distribution**: 0 HIGH, 5 MEDIUM, 2 LOW (7 total)

The roadmap is a faithful and thorough operationalization of the spec. No functional requirements or architectural commitments are missing. The 5 MEDIUM deviations are:
- One mischaracterized NFR in the traceability matrix (DEV-001)
- One sentinel test with insufficient scope (DEV-002)
- One missing contract validation rule in the gate criteria (DEV-003)
- One undocumented spec inconsistency in FR-TDD-R.6 scope (DEV-004)
- One missing migration/rollout section (DEV-005)

All are addressable with minor additions or annotations. The roadmap adds value beyond the spec with its phased gate structure, integration points index, cross-cutting gate summary, and open questions resolution plan. No deviations risk incorrect implementation if the spec is also available during execution.
