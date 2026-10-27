# v3.1 TurnLedger Integration -- Spec Refactoring Tasklist

> **Generated**: 2026-03-20
> **Source**: `adversarial/merged-output.md` (Alpha/Beta/Gamma consensus)
> **Target spec**: `.dev/releases/backlog/v3.1_Anti-instincts__/anti-instincts-gate-unified.md`
> **Executor**: `/sc:task-unified`

---

## Summary

| Metric | Value |
|--------|-------|
| Total tasks | 22 |
| Total waves | 6 |
| Edit tasks | 14 |
| Add-section tasks | 3 |
| Verify tasks | 4 |
| Test tasks | 1 |

### Execution Order

```
Wave 1: Independent edits to existing sections (no cross-dependencies)
  └─ Verify Wave 1
Wave 2: New section creation (depends on Wave 1 field/term definitions)
  └─ Verify Wave 2
Wave 3: Downstream sections referencing new sections (depends on Wave 2)
  └─ Verify Wave 3
Wave 4: Cross-cutting verification and consistency audit
```

---

## Wave 1 -- Foundation Edits (parallel, no inter-dependencies)

### Task 001: Add dual-context note to Section 3 (Architecture)
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 3. Architecture
- **Description**: After the pipeline position paragraph (line 99, "Key design property" paragraph), insert a new paragraph: "When the roadmap pipeline executes within a sprint task context, gate results propagate to the sprint-level `TrailingGateRunner` and `TurnLedger` for economic tracking. In standalone mode, gate evaluation is synchronous pass/fail with no budget interaction." Add cross-refs to Sections 9.5 and 16.5.
- **Depends on**: none
- **Acceptance criteria**: Section 3 contains the dual-context note. The architecture diagram itself is unchanged. Cross-refs to 9.5 and 16.5 are present.
- **Risk**: None -- documentation-only addition.
- **Wave**: 1

### Task 002: Add `gate_scope` field to ANTI_INSTINCT_GATE definition
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 8. Gate Definition → `ANTI_INSTINCT_GATE` code block
- **Description**: Add `gate_scope: GateScope = GateScope.TASK` to the `ANTI_INSTINCT_GATE = GateCriteria(...)` definition. This field is consumed by `resolve_gate_mode()` in sprint context. The roadmap pipeline's synchronous evaluation bypasses scope resolution entirely.
- **Depends on**: none
- **Acceptance criteria**: The `GateCriteria(...)` constructor includes `gate_scope=GateScope.TASK`. No other fields in the gate definition are modified.
- **Risk**: If `gate_scope` is omitted, `resolve_gate_mode()` cannot dispatch correctly in sprint context.
- **Wave**: 1

### Task 003: Add Coexistence with Sprint-Pipeline subsection to Section 8
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 8. Gate Definition → after "Coexistence with Unified Audit Gating D-03/D-04" paragraph (spec lines 1077-1083)
- **Description**: Insert a new subsection `### Coexistence with Sprint-Pipeline TurnLedger/TrailingGateRunner (v3.1)` containing: (1) Dual execution context definition (standalone roadmap vs sprint-invoked roadmap), (2) Enforcement tier vs rollout mode distinction (`enforcement_tier="STRICT"` = criteria strictness; `gate_rollout_mode` = consequence of failure), (3) Rollout mode behavior summary (off/shadow/soft/full), (4) Note that `gate_passed()` function signature is unchanged. Use the exact content from the merged plan's Section 8 edits.
- **Depends on**: none
- **Acceptance criteria**: New subsection exists after D-03/D-04 paragraph. Contains dual-context definition, enforcement_tier vs rollout_mode table (off/shadow/soft/full), and `gate_passed()` note. Cross-refs to Sections 9, 9.5, 11 (X-007) are present.
- **Risk**: Without enforcement_tier vs rollout_mode clarification, implementers will conflate criteria strictness with failure consequence.
- **Wave**: 1

### Task 004: Add `gate_scope` to Step definition in Section 9 Change 2
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 9. Executor Integration → Change 2: Anti-Instinct Audit Step After Merge
- **Description**: In the `Step(...)` definition code block, add `gate_scope=GateScope.TASK,` after the `gate=ANTI_INSTINCT_GATE,` line. Expand the `retry_limit=0` comment to include: "Remediation (if available) re-runs the upstream merge step, not this check. DeferredRemediationLog records the failure but exits with BUDGET_EXHAUSTED immediately (no retry budget allocated)."
- **Depends on**: none
- **Acceptance criteria**: Step definition includes `gate_scope=GateScope.TASK`. The `retry_limit=0` comment documents the remediation path and BUDGET_EXHAUSTED behavior.
- **Risk**: Without the remediation note, implementers may try to retry the anti-instinct check itself (pointless for deterministic checks).
- **Wave**: 1

### Task 005: Add KPI Reporting Boundary note to Section 9 Change 3
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 9. Executor Integration → after Change 3 (`_run_anti_instinct_audit()`)
- **Description**: After the `_run_anti_instinct_audit()` code block, insert a **KPI Reporting Boundary** note: "In standalone roadmap mode, anti-instinct audit results are self-contained roadmap-pipeline artifacts. They do NOT feed into `build_kpi_report()` (sprint/kpi.py). In sprint-invoked mode, gate results are wrapped in `TrailingGateResult` and accumulated into the sprint-level `_all_gate_results` list for KPI aggregation."
- **Depends on**: none
- **Acceptance criteria**: KPI boundary note exists after Change 3. Distinguishes standalone vs sprint-invoked behavior. References `TrailingGateResult` and `_all_gate_results`.
- **Risk**: Without this note, implementers may attempt to pipe roadmap gate results into sprint KPI in standalone mode.
- **Wave**: 1

### Task 006: Add TrailingGateResult and DeferredRemediationLog imports to Section 9 Change 4
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 9. Executor Integration → Change 4: Import and Step ID Updates
- **Description**: Expand the Change 4 imports to include `TrailingGateResult` and `DeferredRemediationLog` alongside the existing `ANTI_INSTINCT_GATE` import.
- **Depends on**: none
- **Acceptance criteria**: Change 4 import block includes `TrailingGateResult`, `DeferredRemediationLog`, and `ANTI_INSTINCT_GATE`.
- **Risk**: Missing imports cause implementation to miss sprint-pipeline type dependencies.
- **Wave**: 1

---

## Verify Wave 1

### Task 007: Verify Wave 1 edits are internally consistent
- **Type**: verify
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: Sections 3, 8, 9
- **Description**: Verify: (1) `gate_scope=GateScope.TASK` appears in both Section 8 gate definition and Section 9 Step definition. (2) Dual-context terminology is consistent across Section 3 note, Section 8 subsection, and Section 9 KPI boundary note. (3) `enforcement_tier` vs `gate_rollout_mode` distinction uses identical terminology in Section 8 and will be referenced by Section 9.5. (4) No orphaned cross-references (all referenced sections exist or will be created in Wave 2).
- **Depends on**: 001, 002, 003, 004, 005, 006
- **Acceptance criteria**: All four verification checks pass. No terminology drift between sections. Canonical dual-context terms are "standalone roadmap" and "sprint-invoked roadmap" throughout. For criterion (2), consistency is verified against these canonical terms specifically.
- **Risk**: Terminology inconsistency between sections creates implementer confusion.
- **Wave**: 1-verify

---

## Wave 2 -- New Sections (depend on Wave 1 definitions)

### Task 008: Add Section 9.5 -- Sprint Executor Integration
- **Type**: add-section
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: New section 9.5, inserted between Section 9 and Section 10
- **Description**: Insert new section `### 9.5 Sprint Executor Integration` containing: (1) 6-step lifecycle for gate result flow in sprint context (audit execution -> TrailingGateResult wrapping -> accumulation -> credit on PASS -> remediation on FAIL -> ShadowGateMetrics recording), (2) Reimbursement clarification: applies to upstream merge step's turn cost, not anti-instinct step (0 LLM turns), (3) TurnLedger None-safety guard (`if ledger is not None`), (4) Threading note: synchronous execution preferred over daemon thread for <1s operation, (5) Rollout Mode Behavior Matrix table (off/shadow/soft/full columns: Gate fires?, Failure logged?, Remediation attempted?, TaskResult mutated?, Reimbursement on pass?), (6) Anti-instinct x wiring gate ordering note: "Anti-instinct gate and wiring-integrity gate evaluate independently as trailing gates. No ordering constraint exists between them; both read the merged output and neither mutates it." (7) Structural audit budget impact note (Phase 2): "Structural audit is pure-Python (0 LLM turns). If a future version introduces LLM-assisted structural analysis, its TurnLedger cost must be budgeted separately from the anti-instinct gate." Use the exact content from the merged plan's Section 9.5 plus the above additions.
- **Depends on**: 002, 003, 004, 005 (references dual-context terms and gate_scope field defined in Wave 1)
- **Acceptance criteria**: Section 9.5 exists between Sections 9 and 10. Contains all 6 lifecycle steps, reimbursement note, None-safety guard, threading note, and rollout mode behavior matrix. Cross-refs to Sections 8, 9, 16.5, and design.md 3.3/6.3.
- **Risk**: If omitted, the dual-context execution model is undefined and implementers will either skip sprint integration entirely or wire it incorrectly.
- **Wave**: 2

### Task 009: Add Section 9.6 -- KPI Report Integration
- **Type**: add-section
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: New section 9.6, inserted after Section 9.5
- **Description**: Insert new section `### 9.6 KPI Report Integration` defining how anti-instinct gate metrics feed into `build_kpi_report()`. Content: (1) `GateKPIReport` receives anti-instinct results via `build_kpi_report()` at sprint completion, (2) Contributed metrics: `gate_pass_rate`/`gate_fail_rate`, `gate_latency_p50`/`gate_latency_p95` (expected <1s), `turns_reimbursed_total` (soft/full mode on pass only), (3) Clarification: KPI consumes `TrailingGateResult.passed` and `TrailingGateResult.evaluation_ms`, not audit report content, (4) KPI aggregation occurs only in sprint context; standalone roadmap runs do not produce `GateKPIReport`. Use exact content from merged plan's Section 9.6.
- **Depends on**: 008 (references Section 9.5 concepts)
- **Acceptance criteria**: Section 9.6 exists after Section 9.5. Contains KPI metrics list, data source clarification, and sprint-only aggregation note. Cross-refs to Section 9.5 and design.md Section 5.
- **Risk**: Without this section, KPI report integration is undefined and must be reverse-engineered from design.md.
- **Wave**: 2

### Task 010: Add Section 16.5 -- TurnLedger Integration Contract
- **Type**: add-section
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: New section 16.5, inserted between Section 16 and end of document
- **Description**: Insert new section `### 16.5 TurnLedger Integration Contract` defining the economic interaction model. Content: (1) On gate PASS (soft/full): `ledger.credit(int(upstream_merge_turns * ledger.reimbursement_rate))` with note that reimbursement applies to upstream merge step, (2) On gate FAIL: `remediation_log.append(gate_result)`, remediation re-runs upstream merge step, exits with BUDGET_EXHAUSTED (retry_limit=0), (3) On FAIL + full mode: `TaskResult.status = FAIL`, (4) On off/standalone: gate fires normally, result not submitted to sprint infrastructure, backward compatible, (5) Invariant: anti-instinct gate TurnLedger cost is always 0 (pure Python). Use exact content from merged plan's Section 16.5.
- **Depends on**: 002, 003, 008 (references gate_scope from Task 002, enforcement_tier vs rollout_mode from Section 8, and Section 9.5 lifecycle steps from Task 008)
- **Acceptance criteria**: Section 16.5 exists after Section 16. Contains all 5 economic paths. All credit/debit calls show None-safety. Cross-refs to Sections 8, 9.5, and design.md 2.2.
- **Risk**: Without this contract, the economic interaction model must be inferred from scattered references.
- **Wave**: 2

---

## Verify Wave 2

### Task 011: Verify new sections are complete and cross-referenced
- **Type**: verify
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: Sections 9.5, 9.6, 16.5
- **Description**: Verify: (1) Section 9.5 rollout mode behavior matrix matches Section 8 coexistence subsection's mode descriptions (off/shadow/soft/full semantics are consistent), (2) Section 9.6 KPI metrics reference correct `TrailingGateResult` fields, (3) Section 16.5 economic paths are consistent with Section 9.5 lifecycle steps (credit on PASS matches step 4, FAIL matches step 5), (4) All cross-references from Wave 1 sections (3, 8, 9) to new sections (9.5, 9.6, 16.5) resolve correctly, (5) None-safety is mentioned in both Section 9.5 and Section 16.5.
- **Depends on**: 008, 009, 010
- **Acceptance criteria**: All 5 consistency checks pass. No contradictions between new sections and Wave 1 edits.
- **Risk**: Inconsistent rollout mode semantics between sections creates implementation ambiguity.
- **Wave**: 2-verify

---

## Wave 3 -- Downstream Sections (reference new content from Waves 1-2; 012/016/017 parallel, then 013->014->015 sequential)

### Task 012: Add coordination table to Section 12 (File Change List)
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 12. File Change List → after "Modified Files (3)" table
- **Description**: Insert a new subsection `### Coordination with TurnLedger Integration (v3.1 Sprint Pipeline)` containing a 4-row file coordination table: (1) `pipeline/gates.py` -- additive vs read-only, no conflict, (2) `roadmap/executor.py` -- anti-instinct changes only, no TurnLedger changes, (3) `sprint/executor.py` -- TurnLedger changes only, no anti-instinct changes, (4) `sprint/models.py` -- TurnLedger changes only. Include conclusion: "Zero merge conflicts expected."
- **Depends on**: 008 (Section 9.5 defines the sprint executor integration that motivates the coordination table)
- **Acceptance criteria**: Coordination table exists with all 4 rows. Conflict risk column shows "None" for all rows. Conclusion states zero merge conflicts.
- **Risk**: Without the coordination table, parallel implementers may assume conflicts exist where none do.
- **Wave**: 3

### Task 013: Add sprint-side files to Section 12 Modified Files list
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 12. File Change List → Modified Files table and New Test Files
- **Description**: (1) Add to modified files: `src/superclaude/cli/sprint/models.py` (add `gate_rollout_mode` field to SprintConfig) and `src/superclaude/cli/sprint/executor.py` (add `run_post_task_gate_hook()`, `TrailingGateRunner`/`DeferredRemediationLog` instantiation, `build_kpi_report()` call). (2) Add to new test files: `tests/sprint/test_shadow_mode.py` and `tests/pipeline/test_full_flow.py`. (3) Update total LOC estimate from ~1,040 to ~1,190-1,240. (4) Update "Existing model changes" from 0 to 1 (`SprintConfig` gains `gate_rollout_mode`).
- **Depends on**: 012 (coordination table provides context for the expanded file list)
- **Acceptance criteria**: Modified files list includes sprint-side files. Test files list includes shadow mode and full flow tests. LOC estimate updated. Model changes count updated to 1.
- **Risk**: Without the expanded file list, sprint-side integration files are missed during implementation.
- **Wave**: 3

### Task 014: Add parallelism note to Section 13 (Implementation Phases)
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 13. Implementation Phases → Phase 1, after implementation sequence
- **Description**: Insert a parallelism note: "The Anti-Instincts Gate modules (Sections 4-7, roadmap pipeline) have zero dependency on TurnLedger wiring (sprint pipeline). These can be implemented in parallel: Branch A: Anti-instinct modules + roadmap executor wiring (tasks 1-6a, 7-8). Branch B: Sprint executor wiring + TurnLedger instantiation (task 6b). The only shared artifact is `pipeline/gates.py` (additive vs read-only)."
- **Depends on**: 012 (coordination table validates the zero-conflict claim)
- **Acceptance criteria**: Parallelism note exists in Phase 1. Branch A and Branch B are defined. Shared artifact is identified as `pipeline/gates.py`.
- **Risk**: Without this note, project planning may serialize workstreams unnecessarily.
- **Wave**: 3

### Task 015: Split task 6 and add task 9 in Section 13
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 13. Implementation Phases → Phase 1, implementation sequence
- **Description**: (1) Split existing task 6 (`executor.py`) into: "6a: Roadmap executor -- anti-instinct step + structural audit hook" and "6b: Sprint executor -- `run_post_task_gate_hook()`, TurnLedger instantiation, KPI report call". (2) Add task 9: "Shadow-mode validation run. Graduation criteria: `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprints before advancing to soft mode." (3) Add note: Phase 1 ships with `gate_rollout_mode` defaulting to `"off"`.
- **Depends on**: 014 (parallelism note provides the Branch A/B context for the task split)
- **Acceptance criteria**: Task 6 is split into 6a and 6b. Task 9 exists with graduation criteria. Default mode is documented as "off".
- **Risk**: Without task splitting, implementers face scope confusion between roadmap and sprint executor changes.
- **Wave**: 3

### Task 016: Add deferred item to Section 13 Phase 2
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 13. Implementation Phases → Phase 2: Deferred Items table
- **Description**: Add a new row to the Phase 2 deferred items table: "Sprint-pipeline gate reimbursement via TurnLedger | design.md | Separate v3.1 workstream; activates `reimbursement_rate`. No dependency on Anti-Instincts Gate modules."
- **Depends on**: none
- **Acceptance criteria**: New row exists in Phase 2 deferred items table with correct source and adoption condition.
- **Risk**: None -- additive table row.
- **Wave**: 3

### Task 017: Add assumptions A-011 through A-014 to Section 14
- **Type**: edit
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: 14. Shared Assumptions and Known Risks → assumptions table
- **Description**: Add four new rows to the assumptions table: (1) A-011: `execute_sprint()` will instantiate TurnLedger before anti-instinct gates fire. Risk if wrong: reimbursement is a no-op, gate failures are never budget-tracked. Mitigation: v3.1 TurnLedger wiring is a prerequisite; anti-instinct gate degrades gracefully (None-safe). (2) A-012: `gate_rollout_mode` defaults to `"off"`. Risk if wrong: false positives block sprints before shadow validation. Mitigation: Phase 1 ships with "off" default; shadow validation required before advancing. (3) A-013: Reimbursement rate of 0.8 is shared across all gate types. Risk if wrong: per-gate-type rates may be needed. Mitigation: single rate sufficient for v3.1; extensibility noted. (4) A-014: `SprintGatePolicy` is instantiated in the sprint loop. Risk if wrong: gate failures have no remediation path. Mitigation: design.md Section 6.3 specifies instantiation. Additionally, add explicit backward compatibility statements for merged plan notes 4, 5, 8, and 9: (5) Note 4 -- "Implementation can be staged: anti-instinct modules first, sprint wiring second. Neither blocks the other." (6) Note 5 -- "Execution order between anti-instinct gate and other trailing gates is unconstrained; each gate evaluates independently." (7) Note 8 -- "TurnLedger migration from sprint/models.py to pipeline/models.py is a separate concern outside v3.1 scope." (8) Note 9 -- "Existing tests pass without modification; all new behavior is additive and gated behind gate_rollout_mode=off default."
- **Depends on**: none
- **Acceptance criteria**: Assumptions table contains A-011 through A-014 with ID, Assumption, Risk If Wrong, and Mitigation columns populated. Section 14 also contains explicit backward compatibility statements for merged plan notes 4, 5, 8, and 9 (staged implementation, unconstrained execution order, TurnLedger migration out-of-scope, existing tests unmodified). Cross-refs to Sections 8, 9.5, and design.md Section 10 are present.
- **Risk**: Without A-011, implementers may assume anti-instinct gate is self-contained. Without A-014, `SprintGatePolicy` remains uninstantiated.
- **Wave**: 3

---

## Verify Wave 3

### Task 018: Verify Section 12-14 edits are consistent with Waves 1-2
- **Type**: verify
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: Sections 12, 13, 14
- **Description**: Verify: (1) Section 12 coordination table's conflict analysis is consistent with Section 9.5's sprint executor integration scope, (2) Section 12 modified files list matches the files referenced in Sections 9.5 and 9.6, (3) Section 13 task 6a/6b split aligns with the parallelism note's Branch A/B definitions, (4) Section 13 graduation criteria reference `ShadowGateMetrics` which is defined in Section 9.5's rollout mode behavior matrix, (5) Section 14 assumptions A-011 through A-014 cross-reference the correct sections, (6) Section 12 LOC estimate increase (~150-200 LOC) is plausible given the sprint-side additions.
- **Depends on**: 012, 013, 014, 015, 016, 017
- **Acceptance criteria**: All 6 verification checks pass. No orphaned cross-references. For criterion (6), LOC estimate is validated by specific breakdown: ~80-100 LOC for `sprint/executor.py` (hook + instantiation + KPI call), ~20-30 LOC for `sprint/models.py` (field addition), ~50-70 LOC for new test files. Total delta of ~150-200 LOC is arithmetically consistent with the per-file breakdown.
- **Risk**: Inconsistent file lists or task definitions create implementation confusion.
- **Wave**: 3-verify

---

## Wave 4 -- Final Consistency Audit

### Task 019: Verify unchanged sections are truly unchanged
- **Type**: verify
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: Sections 1, 2, 4, 5, 6, 7, 10, 11, 15, 16
- **Description**: Confirm that no edits from Waves 1-3 inadvertently modified the following sections (all three adversarial plans agreed these are unchanged): (1) Section 1: Problem Statement, (2) Section 2: Evidence, (3) Sections 4-7: Modules 1-4 (pure Python, no TurnLedger interaction), (4) Section 10: Prompt Modifications, (5) Section 11: Contradiction Resolutions (X-001 through X-008), (6) Section 15: V5-3 AP-001 Subsumption, (7) Section 16: Rejected Alternatives. Run a diff against the original spec to confirm.
- **Depends on**: 018
- **Acceptance criteria**: Diff shows zero modifications to the listed sections. Only Sections 3, 8, 9, 12, 13, 14 and new sections 9.5, 9.6, 16.5 were touched.
- **Risk**: Accidental edits to unchanged sections introduce spec drift.
- **Wave**: 4

### Task 020: Validate all interaction effects are documented
- **Type**: verify
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: All modified/new sections
- **Description**: Verify each of the 10 merged interaction effects from the adversarial analysis is addressed in the spec: (1) Enforcement tier x rollout mode -- Section 8 coexistence subsection, (2) Dual execution context -- Sections 3, 8, 9.5, (3) Anti-instinct x wiring gate ordering -- Section 9.5 (added via Task 008 gate ordering note), (4) Anti-instinct x spec-fidelity gate ordering -- Section 8 ALL_GATES, (5) Reimbursement x pre-allocation reconciliation -- Section 16.5, (6) DeferredRemediationLog x retry_limit=0 -- Sections 9 and 16.5, (7) Structural audit budget impact -- Section 9.5 (added via Task 008 Phase 2 budget note), (8) Per-gate-type reimbursement rate -- Section 14 A-013, (9) Section 8 <-> Section 14 assumption pairing -- A-011, (10) Section 12 coordination <-> Section 13 parallelism -- Tasks 012 and 014.
- **Depends on**: 019
- **Acceptance criteria**: All 10 interaction effects are traceable to specific spec sections. No interaction effect is undocumented.
- **Risk**: Undocumented interaction effects cause implementation surprises.
- **Wave**: 4

### Task 021: Validate backward compatibility invariants
- **Type**: verify
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: All modified/new sections
- **Description**: Verify the 9 backward compatibility notes from the merged plan are maintained: (1) `gate_rollout_mode` defaults to "off", (2) TurnLedger is None-safe throughout, (3) No model changes to existing dataclasses (only additions: `gate_rollout_mode` on SprintConfig, `gate_scope` on ANTI_INSTINCT_GATE), (4) Implementation can be staged, (5) Execution order unconstrained, (6) SprintGatePolicy activation is a cross-cutting dependency, (7) `pipeline/gates.py` additive change is safe, (8) TurnLedger migration to `pipeline/models.py` is a separate concern, (9) Existing tests pass without modification. Confirm each is explicitly stated or implied by the spec edits.
- **Depends on**: 020
- **Acceptance criteria**: All 9 backward compatibility invariants are verifiable from the spec text. No invariant is contradicted by the edits.
- **Risk**: Backward compatibility regression breaks existing users.
- **Wave**: 4

### Task 022: End-to-end spec coherence test
- **Type**: test
- **Target file**: `anti-instincts-gate-unified.md`
- **Section**: Full document
- **Description**: Read the complete modified spec end-to-end and verify: (1) Section numbering is correct and sequential (1-16, with 9.5, 9.6, 16.5 properly interleaved), (2) All internal cross-references resolve (no "see Section X" pointing to nonexistent sections), (3) No duplicate content between Section 8 coexistence subsection and Section 9.5 (they should complement, not repeat), (4) The merged plan's "Sections Unchanged" table is accurate after all edits, (5) Document reads coherently as a unified spec (not as a patchwork of adversarial plan fragments).
- **Depends on**: 021
- **Acceptance criteria**: Spec passes all 5 coherence checks. For criterion (5), "coherently" means: no verbatim repetition across sections, same concept uses same term throughout (canonical terms: "standalone roadmap" and "sprint-invoked roadmap"), and no contradictory statements between sections. Document is ready for implementation handoff.
- **Risk**: Incoherent spec causes implementer confusion and rework.
- **Wave**: 4

---

## Dependency Graph

```
Wave 1 (parallel):
  001 ─┐
  002 ─┤
  003 ─┼──> 007 (verify)
  004 ─┤
  005 ─┤
  006 ─┘

Wave 2 (parallel, after 007):
  008 (needs 002,003,004,005) ─┐
  009 (needs 008)              ├──> 011 (verify)
  010 (needs 002,003,008)      ─┘

Wave 3 (after 011; 012/016/017 parallel, then 013->014->015 sequential):
  012 (needs 008)     ─┐
  013 (needs 012)      │ sequential
  014 (needs 012)      │ chain
  015 (needs 014)     ─┼──> 018 (verify)
  016 (no deps)       ─┤
  017 (no deps)       ─┘

Wave 4 (sequential, after 018):
  019 ──> 020 ──> 021 ──> 022
```

## Notes

- All tasks target a single file: `anti-instincts-gate-unified.md`
- The merged plan resolves the central architectural disagreement (Gamma's dual-context model wins over Alpha's roadmap-only and Beta's always-sprint views)
- `GateScope.TASK` is the correct scope assignment (not `GateScope.RELEASE`)
- Alpha's 8.5 "Non-Applicability" section is NOT created (replaced by the dual-context model in Section 8 coexistence subsection)
- Total new spec content: ~3 new subsections + ~14 edits to existing sections
- No implementation code changes -- this tasklist modifies only the specification document

---

## Post-Reflection Amendments

> **Date**: 2026-03-20
> **Source**: `adversarial/reflection/merged-reflection.md`

1. **(G-1, MEDIUM)** Expanded Task 017 description and acceptance criteria to include explicit backward compatibility statements for merged plan notes 4, 5, 8, and 9. Without this, Task 021 would verify notes that no task ever created.

2. **(AC-1, LOW)** Sharpened Task 022 acceptance criterion (5): replaced subjective "reads coherently" with objective checks -- no verbatim repetition, canonical term consistency, no contradictions.

3. **(AC-2, LOW)** Sharpened Task 018 acceptance criterion (6): replaced subjective "plausible LOC estimate" with specific per-file LOC breakdown (~80-100 executor, ~20-30 models, ~50-70 tests) and arithmetic consistency check.

4. **(AC-3, LOW)** Sharpened Task 007 acceptance criterion (2): added canonical terms "standalone roadmap" and "sprint-invoked roadmap" as the reference list for consistency verification.

5. **(G-2, LOW)** Added anti-instinct x wiring gate ordering note to Task 008 description item (6), covering interaction effect 3.

6. **(G-3, LOW)** Added structural audit budget impact Phase 2 note to Task 008 description item (7), covering interaction effect 7.

7. **(DEP-1, LOW)** Added Task 008 dependency on Task 002 (GateScope field reference).

8. **(DEP-2, LOW)** Added Task 010 dependency on Task 002 (gate_scope reference).

9. **(DEP-3, LOW)** Added Task 010 dependency on Task 008 (Section 16.5 references 9.5 lifecycle steps).

10. **(WO-4, LOW)** Clarified Wave 3 header and dependency graph to indicate that Tasks 013->014->015 form a sequential chain within the wave, while 012/016/017 are parallel.

11. **Task 020 interaction effects 3 and 7**: Updated traceability references to note these are now covered by Task 008 additions (items 6 and 7).
