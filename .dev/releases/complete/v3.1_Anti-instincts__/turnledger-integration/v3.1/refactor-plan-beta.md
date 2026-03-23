# Refactoring Plan: Anti-Instincts Gate <- TurnLedger Integration (Beta Spec-First)

> **Date**: 2026-03-20
> **Spec under review**: `anti-instincts-gate-unified.md`
> **Design source**: `design.md` (v3.1 TurnLedger + TrailingGateRunner Unified Pipeline Integration)
> **Analysis sources**: `analyze.md`, `brainstorm.md`, `cross-release-summary.md`

---

## Sections Requiring Modification

### Section 8: Gate Definition (ANTI_INSTINCT_GATE)

- **Current**: Gate definition uses `GateCriteria` with 3 semantic checks validated against frontmatter in `anti-instinct-audit.md`. No budget awareness, no rollout modes, no interaction with `TurnLedger`.
- **Change**: design.md introduces `gate_rollout_mode` (shadow/soft/full) that controls whether gate failures are logged-only, warning-with-remediation, or blocking. The `ANTI_INSTINCT_GATE` must declare how it interacts with `resolve_gate_mode()` and `TrailingGateRunner.submit()`. Currently the spec assumes synchronous STRICT enforcement; design.md requires the gate to participate in the trailing-gate evaluation pipeline with rollout-gated severity.
- **Edits**: (1) Add `gate_scope: GateScope` field to `ANTI_INSTINCT_GATE` definition (default `GateScope.TASK` for trailing evaluation, `GateScope.RELEASE` for blocking). (2) Document that when `gate_rollout_mode="shadow"`, the gate fires but does not fail the pipeline. (3) Add coexistence note: `ANTI_INSTINCT_GATE` results feed into `ShadowGateMetrics.record()` and `DeferredRemediationLog` when in trailing mode.
- **Cross-refs**: Section 9 (Executor Integration), Section 11 (Contradiction Resolutions -- X-007 enforcement tier)
- **Risk**: If the gate is always STRICT but the rollout mode is "shadow", the enforcement_tier and rollout_mode semantics conflict. Must clarify that `enforcement_tier="STRICT"` describes the *criteria* strictness (zero tolerance on semantic checks), while `gate_rollout_mode` describes the *consequence* of failure (log vs warn vs block).

### Section 9: Executor Integration

- **Current**: Describes 4 executor changes: structural audit after extract, anti-instinct step after merge, audit runner function, and import updates. The step uses `retry_limit=0` and has no budget/ledger awareness. `_run_anti_instinct_audit()` writes the audit report and returns results but does not interact with any budget system.
- **Change**: design.md requires `execute_phase_tasks()` to instantiate a `TrailingGateRunner` and `DeferredRemediationLog` per phase. The anti-instinct audit step must participate in this lifecycle: (a) its results must be submitted via `runner.submit()` or equivalent, (b) gate failures must flow through `remediation_log.append()`, (c) gate passes must trigger `ledger.credit(turns * reimbursement_rate)` when `gate_rollout_mode` is "soft" or "full". Currently the spec treats the anti-instinct step as a standalone Python function with no interaction with the trailing gate infrastructure.
- **Edits**: (1) Replace the standalone `_run_anti_instinct_audit()` invocation with a call through `run_post_task_gate_hook()` (design.md Section 6.3), passing the anti-instinct step as the evaluated step. (2) Add `ledger` parameter threading: `_run_anti_instinct_audit()` receives `ledger` and calls `ledger.credit()` on pass when mode permits. (3) Add `remediation_log` parameter: failures append to `DeferredRemediationLog`. (4) Wire `ShadowGateMetrics.record(passed, evaluation_ms)` for the anti-instinct check. (5) Document that `retry_limit=0` is correct (deterministic check, retry produces same result) but remediation is still possible via `attempt_remediation()` which re-runs the *upstream* merge step, not the anti-instinct check itself.
- **Cross-refs**: Section 8 (Gate Definition), Section 12 (File Change List -- executor.py changes expand), design.md Section 2 (debit/credit call map), design.md Section 3.3 (TrailingGateRunner wiring)
- **Risk**: The anti-instinct step is a non-LLM pure-Python check. Wrapping it in `TrailingGateRunner.submit()` (which runs on a daemon thread) adds unnecessary threading for a <1s synchronous operation. Consider special-casing: run synchronously, then feed the result into the trailing gate infrastructure for bookkeeping only.

### Section 12: File Change List

- **Current**: Lists 4 new files + 3 modified files. `executor.py` changes are scoped to adding the anti-instinct step, structural audit hook, audit runner, and imports.
- **Change**: design.md demands additional modifications to `executor.py` beyond what the spec lists: (1) `execute_sprint()` must instantiate `TurnLedger` (currently it does not -- analyze.md Finding F-2). (2) `execute_phase_tasks()` must instantiate `TrailingGateRunner` + `DeferredRemediationLog`. (3) `run_post_task_gate_hook()` is a new function (~60 LOC). (4) `build_kpi_report()` call added after phase loop. (5) `models.py` gains `gate_rollout_mode` field on `SprintConfig`.
- **Edits**: (1) Add `models.py` to modified files list with change: `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` on `SprintConfig`. (2) Expand `executor.py` change description to include `run_post_task_gate_hook()`, `TrailingGateRunner` instantiation, `DeferredRemediationLog` instantiation, `build_kpi_report()` call, and `TurnLedger` creation in `execute_sprint()`. (3) Update total new LOC estimate (add ~100 LOC for gate hook + wiring). (4) Update "Existing model changes" from 0 to 1 (`SprintConfig` gains `gate_rollout_mode`).
- **Cross-refs**: Section 14 (Assumptions -- A-007 single-file limitation is partly addressed by the audit report pattern, but the trailing gate runner adds a second evaluation path)
- **Risk**: Scope creep. The anti-instincts spec was scoped to 0 model changes and ~680 new LOC. Adding TurnLedger wiring roughly doubles the executor.py diff. Consider whether the TurnLedger wiring is a v3.1 *prerequisite* that lands in a separate PR before the anti-instincts modules.

### Section 13: Implementation Phases

- **Current**: Phase 1 has 8 implementation tasks in a defined dependency graph. Phase 2 lists 5 deferred items. No mention of rollout modes, shadow metrics, or TurnLedger wiring.
- **Change**: design.md defines a three-phase rollout (shadow -> soft -> full) with graduation criteria. The implementation sequence must account for: (a) `gate_rollout_mode` field addition before executor wiring, (b) shadow mode as the initial deployment (not STRICT), (c) graduation criteria that reference `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprints.
- **Edits**: (1) Insert task 5.5: "Add `gate_rollout_mode` to `SprintConfig` in models.py". (2) Modify task 6 (executor.py) to include `run_post_task_gate_hook()` and `TrailingGateRunner`/`DeferredRemediationLog` instantiation. (3) Add task 8.5: "Wire `build_kpi_report()` at sprint completion in `execute_sprint()`". (4) Revise Phase 1 enforcement: initial deployment should be `gate_rollout_mode="shadow"` (not STRICT), with STRICT as Phase 2 graduation. (5) Add graduation criteria from design.md Section 6.2.
- **Cross-refs**: Section 7 (Spec Structural Audit enforcement strategy already uses warning-only Phase 1), Section 8 (enforcement_tier vs rollout_mode distinction)
- **Risk**: Phase 1 scope expansion conflicts with the spec's "4-6 sprint tasks" estimate. If rollout wiring is included, estimate rises to 8-10 tasks.

### Section 14: Shared Assumptions and Known Risks

- **Current**: Lists 7 assumptions (A-001 through A-010, non-contiguous). No assumption about TurnLedger availability or budget tracking.
- **Change**: design.md reveals two new assumptions: (1) `execute_sprint()` will instantiate a TurnLedger (currently it does not -- this is a hard dependency for reimbursement). (2) The anti-instinct gate will participate in a trailing gate pipeline with budget-aware remediation. Additionally, Finding F-3 from analyze.md (`SprintGatePolicy` is dead code) becomes relevant: the anti-instinct gate's remediation path depends on `SprintGatePolicy.build_remediation_step()` being instantiated.
- **Edits**: (1) Add A-011: "TurnLedger is instantiated by `execute_sprint()` before anti-instinct gates fire. Risk if wrong: reimbursement is a no-op, gate failures are never budget-tracked. Mitigation: v3.1 TurnLedger wiring is a prerequisite." (2) Add A-012: "`SprintGatePolicy` is instantiated in the sprint loop. Risk if wrong: gate failures have no remediation path. Mitigation: design.md Section 6.3 specifies instantiation." (3) Add A-013: "Anti-instinct check latency is <1s. Risk if wrong: trailing gate timeout (30s) is too generous and masks performance issues. Mitigation: shadow-mode p95 measurement validates this assumption."
- **Cross-refs**: Section 9 (Executor Integration), design.md Section 10 (Risks and Mitigations)
- **Risk**: Accepting these assumptions makes the anti-instincts spec dependent on v3.1 TurnLedger landing first. If they ship independently, the anti-instincts gate works but with no budget integration (acceptable degradation).

---

## New Sections Required

### New Section 9.5: TurnLedger Interaction Model

**Purpose**: Define how the anti-instinct gate interacts with the TurnLedger economic model. Currently absent from the spec.

**Contents**:
- The anti-instinct step itself consumes 0 LLM turns (pure Python). Its TurnLedger cost is 0.
- Gate-pass reimbursement applies to the *upstream merge step's* turn cost, not the anti-instinct step's cost. When the anti-instinct gate passes, the merge step's actual turns are eligible for `floor(actual_turns * reimbursement_rate)` credit.
- Gate failure enters `DeferredRemediationLog`. Remediation re-runs the merge step (not the anti-instinct check). Remediation budget comes from `TurnLedger.minimum_remediation_budget`.
- When `gate_rollout_mode="off"`, the anti-instinct gate runs but does not interact with TurnLedger at all (backward compatible).

### New Section 9.6: Rollout Mode Behavior Matrix

**Purpose**: Disambiguate `enforcement_tier="STRICT"` from `gate_rollout_mode`.

**Contents**:

| `gate_rollout_mode` | Gate fires? | Failure logged? | Remediation attempted? | TaskResult mutated? | Reimbursement on pass? |
|---------------------|------------|----------------|----------------------|--------------------|-----------------------|
| off                 | Yes        | No             | No                   | No                 | No                    |
| shadow              | Yes        | Yes (metrics)  | No                   | No                 | No                    |
| soft                | Yes        | Yes (warning)  | Yes                  | No                 | Yes                   |
| full                | Yes        | Yes (error)    | Yes                  | Yes (FAIL)         | Yes                   |

---

## Sections Unchanged

### Section 1: Problem Statement
No change. The four failure modes and their detection modules are independent of TurnLedger.

### Section 2: Evidence (cli-portify Bug)
No change. Historical evidence is not affected by integration design.

### Section 3: Architecture
No change. The pipeline position diagram (merge -> anti-instinct -> test-strategy) remains accurate. TurnLedger wiring is executor-level plumbing, not architectural.

### Section 4: Module 1 (Obligation Scanner)
No change. Pure function, no I/O, no budget interaction.

### Section 5: Module 2 (Integration Contract Extractor)
No change. Pure function, no I/O, no budget interaction.

### Section 6: Module 3 (Fingerprint Extraction)
No change. Pure function, no I/O, no budget interaction.

### Section 7: Module 4 (Spec Structural Audit)
No change. The warning-only Phase 1 enforcement is compatible with the shadow rollout mode.

### Section 10: Prompt Modifications
No change. Prompt changes are generation-time, not gate-evaluation-time.

### Section 11: Contradiction Resolutions
No change, but X-007 (enforcement tier) should be cross-referenced from the new Section 9.6 rollout matrix.

### Section 15: V5-3 AP-001 Subsumption
No change.

### Section 16: Rejected Alternatives
No change.

---

## Interaction Effects

### Anti-Instinct Gate + Wiring Gate (v3.0)
Both gates run post-task in `execute_phase_tasks()`. The wiring gate uses `run_post_task_wiring_hook()` (executor.py:418); the anti-instinct gate uses the new `run_post_task_gate_hook()` (design.md Section 6.3). These are **sequential, not competing**: wiring hook fires first (step [4] in the call map), then gate hook fires (step [5]). Both share the same `DeferredRemediationLog` and `ledger` instance. A task that fails both gates gets two remediation log entries.

### Anti-Instinct Gate + Spec Fidelity Gate
The anti-instinct gate runs *before* spec-fidelity in `ALL_GATES`. If anti-instinct fails in "full" mode, the pipeline halts before spec-fidelity runs. This is correct: anti-instinct catches structural omissions that spec-fidelity's LLM review would miss (the whole point of the spec). No change needed.

### TurnLedger Reimbursement + Pre-Allocation Reconciliation
The current reconciliation logic (executor.py:582-589) credits unused pre-allocation. design.md replaces this with a two-stage model: debit actual, then credit reimbursement on gate pass. These must not double-credit. The spec should note that the reconciliation refactor is a v3.1 prerequisite, not an anti-instincts-spec responsibility.

### Gate KPI Report
The anti-instinct gate's pass/fail results feed into `build_kpi_report()` at sprint completion. The spec should ensure the audit report's frontmatter fields are sufficient for KPI aggregation. Current fields (`undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage`) are gate-specific; the KPI report needs `passed: bool` and `evaluation_ms: int` which come from the `TrailingGateResult` wrapper, not the audit report itself.

---

## Migration / Backward Compatibility Notes

1. **`gate_rollout_mode` defaults to `"off"`**: No behavioral change for existing users. The anti-instinct gate fires and writes its audit report, but failures do not affect TaskResult or budget. This is equivalent to the spec's current design where the gate is STRICT but independent of the sprint control loop.

2. **TurnLedger instantiation is optional**: If `execute_sprint()` does not pass a ledger (pre-v3.1), `run_post_task_gate_hook()` checks `ledger is not None` before any credit/debit. All budget paths are None-safe.

3. **Audit report format unchanged**: The `anti-instinct-audit.md` frontmatter (Section 8) does not need TurnLedger fields. Budget data lives in the `GateKPIReport`, not the gate artifact.

4. **Implementation can be staged**: Ship anti-instinct modules (Sections 4-7) and gate definition (Section 8) first, with `gate_rollout_mode="off"` default. Then ship executor wiring (Section 9 + new sections 9.5/9.6) as a follow-up when TurnLedger instantiation lands.

5. **SprintGatePolicy activation**: The spec's `ANTI_INSTINCT_GATE` will need a corresponding case in `SprintGatePolicy.build_remediation_step()` that constructs a merge re-run step. This is new code in the policy, not a spec change, but it must be implemented alongside the executor wiring.
