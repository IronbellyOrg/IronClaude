# Refactoring Plan: Anti-Instincts Gate <-- TurnLedger Integration (Gamma Interleaved)

> **Date**: 2026-03-20
> **Spec**: `anti-instincts-gate-unified.md` (Sections 1-16)
> **Design**: `design.md` (Sections 1-10)
> **Analysis**: `analyze.md` (Findings F-1 through F-8)
> **Brainstorm**: `brainstorm.md` (Proposals 1-3)
> **Cross-release**: `cross-release-summary.md` (Execution order, shared extensions)

---

## Sections Requiring Modification

### Section 8: Gate Definition (ANTI_INSTINCT_GATE)

- **Current**: Defines `ANTI_INSTINCT_GATE` as a pure frontmatter-validation gate with 3 semantic checks, positioned between `merge` and `test-strategy` in the roadmap pipeline. Zero awareness of TurnLedger or reimbursement economics.
- **Change**: Design.md Section 3.2 introduces `gate_rollout_mode` (shadow/soft/full) and couples gate outcomes to `TurnLedger.credit()`. The anti-instinct gate must declare its `GateScope` so `resolve_gate_mode()` can determine blocking vs trailing behavior. Gate pass must trigger reimbursement; gate fail must feed `DeferredRemediationLog`.
- **Edits**: Add `gate_scope: GateScope = GateScope.TASK` to `ANTI_INSTINCT_GATE`. Add a note that the gate's enforcement_tier="STRICT" interacts with `gate_rollout_mode` -- STRICT means zero tolerance on the semantic checks, but the rollout mode governs whether failure blocks (full), warns (soft), or logs (shadow). Add cross-reference to design.md Section 6.2 rollout phases.
- **Cross-refs**: Section 9 (executor integration), Section 11 (contradiction resolutions -- X-007 enforcement tier), design.md Section 6.
- **Risk**: If `GateScope` is not added, `resolve_gate_mode()` cannot dispatch correctly for the anti-instinct gate, causing it to fall through to a default mode that may be wrong.

### Section 9: Executor Integration (Changes 1-4)

- **Current**: Defines `_run_anti_instinct_audit()` as a non-LLM step with `retry_limit=0`. The step runs between merge and test-strategy. No budget tracking, no reimbursement, no trailing gate runner involvement.
- **Change**: Design.md Section 2.4 specifies that the anti-instinct step should participate in the same `run_post_task_gate_hook()` pattern as all other task-level gates. The step itself is deterministic (retry is pointless), but its gate outcome must flow into the TurnLedger reimbursement loop. Design.md Section 5 requires `build_kpi_report()` at sprint end, which needs anti-instinct gate results accumulated into the sprint-level `_all_gate_results` list.
- **Edits**: (1) In Change 2, add `gate_scope=GateScope.TASK` to the Step definition. (2) In Change 3, after `_run_anti_instinct_audit()` writes the audit report, wire the gate result into the sprint-level accumulator: `_all_gate_results.append(TrailingGateResult(...))`. (3) Add a note that although `retry_limit=0`, the remediation path still applies -- a persistent anti-instinct failure goes to `DeferredRemediationLog` with no retry budget consumed. (4) In Change 4, add import for `TrailingGateResult` and `DeferredRemediationLog`.
- **Cross-refs**: Section 8 (gate definition), design.md Sections 3.3, 4.2, 5.1.
- **Risk**: The anti-instinct step is in the roadmap pipeline, not the sprint pipeline. The `run_post_task_gate_hook()` pattern from design.md is sprint-specific. The spec must clarify that when anti-instinct runs in the roadmap pipeline, it uses the pipeline executor's retry/gate pattern (Section 2.2 of analyze.md), not the sprint gate hook. TurnLedger integration only applies when the roadmap pipeline is invoked from within a sprint.

### Section 12: File Change List

- **Current**: Lists 4 new files + 3 modified files with ~1,040 total LOC. No mention of TurnLedger-related changes.
- **Change**: Design.md Section 9 requires modifications to `models.py` (add `gate_rollout_mode`), additional wiring in `executor.py` (sprint side), and new test scenarios. The file change list must expand to include sprint-side integration files.
- **Edits**: Add rows: (1) `src/superclaude/cli/sprint/models.py` -- add `gate_rollout_mode` field to `SprintConfig`. (2) `src/superclaude/cli/sprint/executor.py` -- add `run_post_task_gate_hook()`, instantiate `TrailingGateRunner` + `DeferredRemediationLog`, call `build_kpi_report()`. (3) `tests/sprint/test_shadow_mode.py` -- extend with gate_rollout_mode="shadow" integration test. (4) `tests/pipeline/test_full_flow.py` -- add scenario 5 for production reimbursement_rate consumption.
- **Cross-refs**: Section 9 (executor integration), design.md Section 9.
- **Risk**: LOC estimate increases by ~150-200 (sprint-side wiring). If these files are not listed, implementers will miss half the integration.

### Section 13: Implementation Phases

- **Current**: Phase 1 has 8 tasks in a dependency graph. Phase 2 lists 5 deferred items. All tasks are roadmap-pipeline scoped.
- **Change**: Design.md Section 6 introduces a three-phase rollout (shadow/soft/full) that is orthogonal to the implementation phases. The spec's Phase 1 tasks 5-6 (gates.py, executor.py) must include sprint-side wiring from design.md. Implementation task 6 must be split: roadmap executor wiring (original) + sprint executor wiring (new from design.md).
- **Edits**: (1) Split task 6 into 6a (roadmap executor -- anti-instinct step + structural audit hook) and 6b (sprint executor -- `run_post_task_gate_hook()`, TurnLedger instantiation in `execute_sprint()`, KPI report call). (2) Add task 9: shadow-mode validation run (design.md Section 6.2 graduation criteria). (3) Add note that Phase 1 ships with `gate_rollout_mode` defaulting to `"off"` -- no behavioral change until shadow validation passes.
- **Cross-refs**: Section 12 (file list), design.md Section 6.
- **Risk**: If sprint-side wiring is deferred to a separate release, the anti-instinct gate works only in standalone roadmap runs, not in sprints. The cross-release summary explicitly recommends v3.1 as the foundational wiring release.

### Section 14: Shared Assumptions and Known Risks

- **Current**: 7 assumptions (A-001 through A-010, some skipped). No assumptions about TurnLedger availability, sprint vs roadmap execution context, or rollout mode defaults.
- **Change**: Design.md Section 10 and analyze.md Section 4 surface risks around reimbursement inflating budget, remediation consuming entire budget, and backward compatibility. These must be reflected as assumptions in the spec.
- **Edits**: Add: (A-011) `execute_sprint()` will be modified to instantiate TurnLedger -- risk if not done: anti-instinct gate results never feed KPI or reimbursement. (A-012) `gate_rollout_mode` defaults to `"off"` -- risk if changed prematurely: false positives from anti-instinct gate block sprints before shadow validation. (A-013) Reimbursement rate of 0.8 is shared across all gate types -- risk: may need per-gate-type rates in future (see cross-release summary Section 2.2).
- **Cross-refs**: Section 13 (phases), design.md Sections 6.3, 10.
- **Risk**: Without A-011, implementers may assume the anti-instinct gate is self-contained in the roadmap pipeline and skip sprint integration entirely.

---

## New Sections Required

### Section 9.5 (New): Sprint Executor Integration

- **Purpose**: The current Section 9 covers only roadmap executor wiring. A new section is needed for sprint-side integration: how anti-instinct gate results flow through `run_post_task_gate_hook()`, how TurnLedger reimbursement is triggered, and how `DeferredRemediationLog` captures failures.
- **Content**: Import design.md Section 6.3's `run_post_task_gate_hook()` function verbatim. Add a note that the anti-instinct gate only participates in sprint-level gate evaluation when the roadmap pipeline is invoked as a sprint task (i.e., `superclaude sprint run` with a tasklist that includes roadmap generation). In standalone `superclaude roadmap run`, TurnLedger is not available and the gate operates in pure pass/fail mode without reimbursement.
- **Cross-refs**: Section 8 (gate definition), Section 9 (roadmap executor), design.md Sections 3.3, 6.3.

### Section 9.6 (New): KPI Report Integration

- **Purpose**: Section 9 has no mention of `build_kpi_report()`. Design.md Section 5 specifies it runs once at sprint completion. The spec needs to define what anti-instinct gate metrics feed into the KPI report.
- **Content**: Define that `GateKPIReport` receives anti-instinct gate results alongside all other gate results. The anti-instinct gate contributes to `gate_pass_rate`, `gate_fail_rate`, and latency metrics. If brainstorm Proposal 3 is adopted, extend KPI with `turns_reimbursed_total` and `failed_gate_budget_loss`.
- **Cross-refs**: design.md Section 5, brainstorm.md Proposal 3.

### Section 16.5 (New): TurnLedger Integration Contract

- **Purpose**: The spec currently has no section that explicitly states how anti-instinct gate results interact with TurnLedger economics. This is the integration contract that cross-release-summary.md Section 2.1 says must be documented.
- **Content**: (1) On gate PASS: `ledger.credit(int(turns_consumed * ledger.reimbursement_rate))`. (2) On gate FAIL: `remediation_log.append(gate_result)`, no credit. (3) On FAIL + `gate_rollout_mode="full"`: `TaskResult.status = FAIL`. (4) TurnLedger is `None`-safe: all credit/debit calls are guarded by `if ledger is not None`.
- **Cross-refs**: Section 8, Section 9.5, design.md Section 2.2, brainstorm.md Proposal 1.

---

## Sections Unchanged

| Section | Reason |
|---------|--------|
| 1. Problem Statement | Describes LLM failure modes. TurnLedger integration does not change the problem, only the enforcement economics. |
| 2. Evidence: The cli-portify Bug | Historical evidence. No TurnLedger relevance. |
| 3. Architecture | Pipeline position diagram is correct as-is. TurnLedger is an orthogonal layer (economics, not detection). |
| 4. Module 1: Obligation Scanner | Pure-function module. No TurnLedger dependency. Input/output unchanged. |
| 5. Module 2: Integration Contract Extractor | Pure-function module. No TurnLedger dependency. |
| 6. Module 3: Fingerprint Extraction | Pure-function module. No TurnLedger dependency. |
| 7. Module 4: Spec Structural Audit | Pure-function module. No TurnLedger dependency. |
| 10. Prompt Modifications | Prompt content is independent of gate economics. |
| 11. Contradiction Resolutions | All X-001 through X-008 resolutions remain valid. TurnLedger does not introduce new contradictions. |
| 15. V5-3 AP-001 Subsumption | Design decision unaffected by budget integration. |
| 16. Rejected Alternatives | No previously rejected alternative becomes viable due to TurnLedger. |

---

## Interaction Effects

### Effect 1: Anti-Instinct Gate x Gate Rollout Mode

The spec defines `enforcement_tier="STRICT"` (Section 8). Design.md introduces `gate_rollout_mode` (shadow/soft/full). These are independent axes: STRICT governs the semantic check threshold (zero tolerance), while rollout mode governs the consequence of failure (log/warn/block). In shadow mode, a STRICT gate that fails is logged but does not block. This is intentional -- it allows calibration before enforcement. The spec must explicitly state this interaction to prevent confusion.

### Effect 2: Anti-Instinct Step x Pipeline vs Sprint Context

The anti-instinct step is defined in the roadmap pipeline (Section 9). TurnLedger lives in the sprint executor. When a roadmap pipeline runs inside a sprint task, the anti-instinct gate result must be propagated up to the sprint-level gate hook. When the roadmap pipeline runs standalone, TurnLedger is absent and the step operates in legacy mode (pass/fail, no economics). The spec must define both paths.

### Effect 3: Reimbursement Rate x Multiple Gate Types

Cross-release summary Section 1 shows three releases consuming `reimbursement_rate` with different semantics. The anti-instinct gate uses the same rate as all task-level gates (design.md Section 2.2). If future gates need different rates, `reimbursement_rate` must become per-gate-type. For now, the single rate is sufficient, but the spec should note this as a future extensibility consideration.

### Effect 4: DeferredRemediationLog x Retry-Limit=0

The anti-instinct step has `retry_limit=0` because it is deterministic. However, `DeferredRemediationLog` still records the failure for KPI reporting and `--resume` support. The remediation path is entered but immediately exits with `BUDGET_EXHAUSTED` (since no retry budget is allocated). This is correct behavior but non-obvious -- the spec should document it.

### Effect 5: Structural Audit (Section 9 Change 1) x Sprint Budget

The structural audit runs between extract and generate in the roadmap pipeline. If it fails (warning-only in Phase 1), no budget impact occurs. In Phase 2 (STRICT enforcement), a failure would halt the pipeline, which in sprint context means the sprint task fails and debits actual turns with no reimbursement. The budget impact of a structural audit failure is indirect but real.

---

## Migration / Backward Compatibility Notes

1. **`gate_rollout_mode` defaults to `"off"`**: No behavioral change for existing users. The anti-instinct gate runs and produces its audit report, but gate economics (reimbursement, remediation) are inactive until explicitly opted in via `--gate-mode shadow`.

2. **`TurnLedger` is None-safe throughout**: All new code paths guard on `if ledger is not None`. Standalone `superclaude roadmap run` (no sprint context) works identically to pre-integration behavior.

3. **No model changes to existing dataclasses**: `TurnLedger`, `SemanticCheck`, `GateCriteria`, `Step`, and `PipelineConfig` retain their current fields. The only model addition is `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` on `SprintConfig`.

4. **Test backward compatibility**: Existing tests in `tests/pipeline/test_full_flow.py` pass without modification. New test scenarios (shadow mode, reimbursement production path) are additive.

5. **TurnLedger location**: Cross-release summary recommends migrating `TurnLedger` from `sprint/models.py` to `pipeline/models.py` as a prerequisite. This is a separate refactor that should be done before or alongside v3.1, not as part of the anti-instinct gate spec. The spec should note this dependency but not own it.

6. **SprintGatePolicy activation**: Design.md Section 6.3 uses `SprintGatePolicy.build_remediation_step()`. This class exists but is never instantiated in production (analyze.md Finding F-3). v3.1 must instantiate it. This is a cross-cutting change that affects the sprint executor generally, not just the anti-instinct gate.
