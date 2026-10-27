# Merge Log: Anti-Instincts Gate Unified Specification

**Protocol**: sc:adversarial Step 5 (Merge Execution)
**Date**: 2026-03-17
**Merge executor**: merge-executor agent
**Base variants**: V2 (7.60) + V5 (7.55) co-bases
**Cherry-picks**: V4-2, V1-C, V1-D+V5-2
**Output**: `anti-instincts-gate-unified.md`

---

## Change Log

### Change 1: Document Scaffold and Metadata

- **Type**: INSERT (new content)
- **Source**: Merge (bridging content)
- **Target section**: Sections 1-3 (Problem Statement, Evidence, Architecture)
- **Before**: No unified document existed.
- **After**: Created document header with status metadata, combined problem statement synthesizing all 5 variant problem descriptions, evidence section from cli-portify forensic report, and architecture diagram from base-selection.md Section 5.
- **Provenance**: `<!-- Source: Merge (new content bridging V2+V5) -->`
- **Validation**: Headings follow H1 > H2 > H3 hierarchy. Architecture diagram matches refactor-plan Section 3. No contradictions introduced.
- **Status**: APPLIED

### Change 2: V2-A Obligation Scanner (Co-Base Primary)

- **Type**: DIRECT ADOPTION
- **Source**: V2, `02-implicit-obligation-tracking.md`, Solution A (lines 58-274)
- **Target section**: Section 4 (Module 1: Obligation Scanner)
- **Before**: V2-A proposed wiring as `SemanticCheck` on `MERGE_GATE`.
- **After**: Code adopted nearly verbatim from V2-A proposal. Gate integration redirected from `MERGE_GATE` to new `ANTI_INSTINCT_GATE`. Added vocabulary management table from V2 Section 5. Added false positive mitigation subsection per refactor-plan Section 6 Weakness 1 (component context extraction, code-block treatment, `# obligation-exempt` escape hatch).
- **Provenance**: `<!-- Source: V2-A (obligation scanner) -->`
- **Adaptations from proposal**:
  - Gate target changed: `MERGE_GATE` -> `ANTI_INSTINCT_GATE`
  - Added false positive mitigations per refactor-plan Section 6 Weakness 1
- **Validation**: Code compiles (pure Python, no imports beyond stdlib). Vocabulary table matches V2 Section 5. False positive mitigations match refactor-plan.
- **Status**: APPLIED

### Change 3: V5-1 Integration Contract Extractor (Co-Base Primary)

- **Type**: DIRECT ADOPTION with pattern expansion
- **Source**: V5, `05-pattern-matching-trap-mitigation.md`, Solution 1 (lines 35-279)
- **Target section**: Section 5 (Module 2: Integration Contract Extractor)
- **Before**: V5-1 had 4 `DISPATCH_PATTERNS` and 3 `WIRING_TASK_PATTERNS`. Proposed own `INTEGRATION_AUDIT_GATE`.
- **After**: Code adopted with expanded pattern library covering all 7 categories from V5 appendix taxonomy (dict dispatch, plugin registry, callback injection, strategy pattern, middleware chain, event binding, DI container). Gate integration redirected from separate `INTEGRATION_AUDIT_GATE` to `ANTI_INSTINCT_GATE` placeholder with executor-level enforcement. Added pattern library expansion table.
- **Provenance**: `<!-- Source: V5-1 (integration contract extractor) -->`
- **Adaptations from proposal**:
  - `DISPATCH_PATTERNS` expanded from 4 to 8 patterns (added strategy, middleware, event, DI)
  - `WIRING_TASK_PATTERNS` expanded from 3 to 4 patterns (added strategy/middleware/event/DI wiring)
  - `_classify_mechanism()` expanded with new categories
  - Gate target changed: `INTEGRATION_AUDIT_GATE` -> `ANTI_INSTINCT_GATE`
  - Real logic moved to executor per refactor-plan multi-file access workaround
- **Validation**: Code compiles. Pattern expansion covers all 7 taxonomy categories from V5 appendix. No overlap with V2-A's scaffold terms.
- **Status**: APPLIED

### Change 4: V4-2 Fingerprint Extraction (Cherry-Pick)

- **Type**: INSERT (new module from non-base variant)
- **Source**: V4, `04-self-audit-blindness-mitigation.md`, Solution 2 (lines 232-336)
- **Target section**: Section 6 (Module 3: Fingerprint Extraction)
- **Rationale**: Fingerprints scored highest single-check efficacy (95% confidence). Catches any code-level identifier omission regardless of ID format. Fills V2's D1=7 gap.
- **Before**: V4-2 proposed adding fingerprints to `SPEC_FIDELITY_GATE`.
- **After**: Code adopted with minor adaptations. Return signature changed from `tuple[bool, list[Fingerprint]]` to `tuple[bool, float, list[Fingerprint], list[Fingerprint]]` to expose coverage ratio and all fingerprints for the audit report. Constant exclusion list extracted to `_EXCLUDED_CONSTANTS` frozenset. Gate integration via `ANTI_INSTINCT_GATE` with executor-level enforcement. Added threshold rationale and A-009 interaction subsections.
- **Provenance**: `<!-- Source: V4-2 (fingerprint extraction) -->`
- **Adaptations from proposal**:
  - Return signature expanded for audit report needs
  - Exclusion list made a module-level constant
  - Gate target changed: `SPEC_FIDELITY_GATE` -> `ANTI_INSTINCT_GATE`
  - Real logic moved to executor per multi-file access workaround
- **Validation**: Code compiles. Threshold rationale matches refactor-plan Section 6 Weakness 4. A-009 interaction explanation consistent with diff analysis.
- **Status**: APPLIED

### Change 5: V1-C Spec Structural Audit (Cherry-Pick)

- **Type**: INSERT (new module from non-base variant)
- **Source**: V1, `01-completeness-bias-mitigation.md`, Solution C (lines 279-346)
- **Target section**: Section 7 (Module 4: Spec Structural Audit)
- **Rationale**: Only upstream guard on extraction quality. V2-Advocate and V5-Advocate both conceded this gap exists.
- **Before**: V1-C proposed as inline executor hook between extract and generate.
- **After**: Code adopted with adaptations: `audit_spec_structure()` returns a dataclass instead of modifying `total_structural_indicators` post-init. Added `check_extraction_adequacy()` wrapper function that performs the ratio comparison. Phase 1 enforcement is warning-only. Added enforcement strategy subsection.
- **Provenance**: `<!-- Source: V1-C (spec structural audit) -->`
- **Adaptations from proposal**:
  - Extracted `check_extraction_adequacy()` as public API
  - `total_structural_indicators` computed inline instead of post-init
  - Phase 1: warning-only enforcement per refactor-plan
- **Validation**: Code compiles. Threshold (0.5) matches refactor-plan Section 2 Change 2. Warning-only enforcement matches refactor-plan.
- **Status**: APPLIED

### Change 6: ANTI_INSTINCT_GATE Definition

- **Type**: INSERT (new gate definition)
- **Source**: Refactor-plan Section 3 (Gate Definition), synthesizing V2-A + V5-1 + V4-2
- **Target section**: Section 8 (Gate Definition)
- **Before**: No anti-instinct gate existed. V2-A proposed MERGE_GATE semantic check. V5-1 proposed INTEGRATION_AUDIT_GATE. V4-2 proposed SPEC_FIDELITY_GATE semantic check.
- **After**: Single `ANTI_INSTINCT_GATE` with 3 semantic checks, all validating frontmatter from the executor-produced audit report. Gate positioned between `merge` and `test-strategy` in `ALL_GATES`. Audit report format specified with complete YAML frontmatter schema.
- **Provenance**: `<!-- Source: Merge (new content bridging V2+V5) -->`
- **Contradiction resolution**: X-007 (enforcement tier). Deterministic checks get STRICT. Matches refactor-plan.
- **Validation**: Gate definition follows existing `GateCriteria` pattern. All 3 check functions validate frontmatter fields. Position in `ALL_GATES` matches refactor-plan Section 3.
- **Status**: APPLIED

### Change 7: Executor Integration

- **Type**: INSERT (new executor wiring)
- **Source**: Refactor-plan Section 4 (Executor Wiring)
- **Target section**: Section 9 (Executor Integration)
- **Before**: No anti-instinct step in pipeline.
- **After**: Four executor changes specified: (1) structural audit hook after extract, (2) anti-instinct step in `_build_steps()`, (3) `_run_anti_instinct_audit()` function, (4) import and step ID updates. Non-LLM step pattern follows recommended Option A from refactor-plan.
- **Provenance**: `<!-- Source: Merge (new content bridging V2+V5) -->`
- **Validation**: Step definition follows existing `Step` pattern. Non-LLM step has `prompt=""`, `retry_limit=0`, `timeout_seconds=30`. Structural audit hook follows `_inject_pipeline_diagnostics` pattern.
- **Status**: APPLIED

### Change 8: Prompt Modifications (V1-D + V5-2 Merged)

- **Type**: APPEND (merged prompt blocks)
- **Source**: V1-D (`01-completeness-bias-mitigation.md` lines 356-393) + V5-2 (`05-pattern-matching-trap-mitigation.md` lines 346-393)
- **Target section**: Section 10 (Prompt Modifications)
- **Before**: V1-D proposed integration task injection constraint. V5-2 proposed forced integration enumeration block. Both modified `build_generate_prompt()`.
- **After**: Merged into single `INTEGRATION_ENUMERATION_BLOCK` using V5-2 as base text, incorporating V1-D's specific examples (dispatch tables, constructor injection, import chains, registration) and V1-D's dispatch-table-to-functions anti-pattern naming. Added `INTEGRATION_WIRING_DIMENSION` as 6th comparison dimension for `build_spec_fidelity_prompt()`.
- **Provenance**: `<!-- Source: V1-D+V5-2 merged (prompt constraint) -->`
- **Contradiction resolution**: X-002 (V1-D vs V5-2 overlap). V5-2's enumeration requirement subsumes V1-D's constraint. Merged per refactor-plan Section 1 Change 3.
- **Validation**: Merged block contains all 4 required elements from refactor-plan: (1) enumerate ALL integration points (V5-2), (2) separate wiring tasks from component implementation (V1-D), (3) `## Integration Wiring Tasks` output section (V5-2), (4) dispatch-table-to-functions anti-pattern named (V1-D).
- **Status**: APPLIED

### Change 9: Contradiction Resolutions

- **Type**: INSERT (summary table)
- **Source**: Diff analysis X-001 through X-008, resolved per refactor-plan
- **Target section**: Section 11 (Contradiction Resolutions)
- **Before**: 8 contradictions identified in diff analysis.
- **After**: All 8 contradictions documented with resolution status. Each resolution traceable to refactor-plan or debate transcript evidence.
- **Validation**: Every X-NNN from diff analysis has a corresponding row. Resolutions match refactor-plan Sections 1, 2, and 7.
- **Status**: APPLIED

### Change 10: File Change List and Implementation Phases

- **Type**: INSERT (implementation guide)
- **Source**: Refactor-plan Sections 8-10
- **Target sections**: Sections 12-13 (File Change List, Implementation Phases)
- **Before**: File manifests distributed across 5 separate proposals.
- **After**: Single consolidated file change list with 4 new source files, 4 new test files, 3 modified files. Implementation phases with Phase 1 (immediate) execution sequence and Phase 2 (deferred) backlog with adoption conditions.
- **Validation**: File counts match refactor-plan Section 8. Dependency graph matches refactor-plan Section 9.
- **Status**: APPLIED

### Change 11: V5-3 AP-001 Subsumption Documentation

- **Type**: INSERT (design decision documentation)
- **Source**: Refactor-plan Section 2 (V5-3 AP-001 Subsumption)
- **Target section**: Section 15
- **Before**: V5-3 proposed separate anti-pattern rule engine with AP-001, AP-002, AP-003.
- **After**: Documented that V2-A subsumes AP-001, V5-1 subsumes AP-003, AP-002 is too imprecise for STRICT enforcement. Rule engine framework deferred to Phase 2.
- **Contradiction resolution**: X-004 (V2-A vs V5-3 AP-001).
- **Validation**: Matches refactor-plan Section 2 and diff analysis X-004.
- **Status**: APPLIED

### Change 12: Rejected Alternatives

- **Type**: INSERT (design decision documentation)
- **Source**: Refactor-plan Section 7
- **Target section**: Section 16
- **Before**: Rejection rationale distributed across refactor-plan.
- **After**: Summary table of all rejected alternatives with source and reason.
- **Validation**: All items from refactor-plan Section 7 present. No rejected item appears in Phase 1 specification.
- **Status**: APPLIED

---

## Structural Integrity Checks

### Heading Hierarchy

- H1: 1 (document title)
- H2: 16 sections (numbered 1-16)
- H3: Subsections within each H2 (Concept, Detection Axis, Implementation, etc.)
- No heading level skips detected.

### Internal Cross-References

| Reference | Target | Status |
|---|---|---|
| Section 4 references V2-A | `obligation_scanner.py` code present | RESOLVED |
| Section 5 references V5-1 | `integration_contracts.py` code present | RESOLVED |
| Section 6 references V4-2 | `fingerprint.py` code present | RESOLVED |
| Section 7 references V1-C | `spec_structural_audit.py` code present | RESOLVED |
| Section 8 references check functions | All 3 check functions defined | RESOLVED |
| Section 9 references gate import | `ANTI_INSTINCT_GATE` import specified | RESOLVED |
| Section 9 references all 4 modules | All module imports in `_run_anti_instinct_audit()` | RESOLVED |
| Section 12 file list matches Sections 4-10 | 4 new files + 3 modified files all documented | RESOLVED |
| Section 13 dependency graph matches Section 12 | Files and dependencies consistent | RESOLVED |

### Contradiction Re-Scan

| Check | Result |
|---|---|
| V2-A gate target consistent | ANTI_INSTINCT_GATE throughout (not MERGE_GATE) |
| V5-1 gate target consistent | ANTI_INSTINCT_GATE throughout (not INTEGRATION_AUDIT_GATE) |
| V4-2 gate target consistent | ANTI_INSTINCT_GATE throughout (not SPEC_FIDELITY_GATE) |
| Fingerprint threshold consistent | 0.7 in code, 0.7 in gate check, 0.70 in audit report |
| Structural audit threshold consistent | 0.5 in code and refactor-plan reference |
| Enforcement tier consistent | STRICT for all deterministic checks |
| Phase 1 scope consistent | No deferred items appear in Phase 1 code |
| No duplicate modules | Each module has exactly one implementation |

### Provenance Coverage

Every major section has a provenance annotation:

| Section | Provenance Tag |
|---|---|
| Sections 1-3 | `<!-- Source: Merge (new content bridging V2+V5) -->` |
| Section 4 | `<!-- Source: V2-A (obligation scanner) -->` |
| Section 5 | `<!-- Source: V5-1 (integration contract extractor) -->` |
| Section 6 | `<!-- Source: V4-2 (fingerprint extraction) -->` |
| Section 7 | `<!-- Source: V1-C (spec structural audit) -->` |
| Section 8 | `<!-- Source: Merge (new content bridging V2+V5) -->` |
| Section 9 | `<!-- Source: Merge (new content bridging V2+V5) -->` |
| Section 10 | `<!-- Source: V1-D+V5-2 merged (prompt constraint) -->` |
| Section 11 | `<!-- Source: Merge (new content bridging V2+V5) -->` |
| Sections 12-16 | `<!-- Source: Merge (new content bridging V2+V5) -->` |
| Subsection provenance | Vocabulary table (V2-A), Pattern expansion (V5-1), False positive mitigation (V2-A adapted), Enforcement strategy (V1-C adapted), Threshold rationale (V4-2 adapted), A-009 interaction (V4-2 + V5-1), AP-001 subsumption (V2-A + V5-1) |

---

## Summary

- **Total changes applied**: 12
- **Changes from V2 (co-base)**: 1 (obligation scanner)
- **Changes from V5 (co-base)**: 1 (integration contract extractor)
- **Changes from V4 (cherry-pick)**: 1 (fingerprint extraction)
- **Changes from V1 (cherry-pick)**: 2 (spec structural audit, prompt constraint contribution)
- **Merged content**: 1 (V1-D + V5-2 prompt block)
- **Bridging/structural content**: 6 (document scaffold, gate definition, executor wiring, contradiction resolutions, file list, rejected alternatives)
- **Changes skipped or blocked**: 0
- **Issues escalated to orchestrator**: 0
