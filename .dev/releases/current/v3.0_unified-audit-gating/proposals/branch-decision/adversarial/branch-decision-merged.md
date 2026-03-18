# Branch Decision: Merged Recommendation

**Decision**: Branch (b) -- Phase-Only Audit Gates for v1.2.1
**Status**: CONFIRMED after adversarial debate + invariant probe
**Convergence**: 93% (3 rounds + 3 invariant probes)
**Base variant**: Variant 2 (opus:analyzer), with Variant 1 (opus:architect) contributions integrated
**Date**: 2026-03-17

---

## 1. Decision Statement

Implement audit gates at phase (milestone) and sprint (release) scope only for v1.2.1. Defer task-scope audit gates to v1.3, contingent on independent validation and mainline promotion of `execute_phase_tasks()`.

This is a deliberate, evidence-based scope reduction, not a deferral of convenience. The spec's section 4.1 task-scope state machine was authored without knowledge that the sprint executor has never run at task granularity (MF-1, CRITICAL, unanimous in adversarial review). Activating orphaned dead code under delivery pressure to satisfy a state machine designed against a nonexistent execution substrate is an unacceptable compound risk.

---

## 2. Conditions for Branch (b) Adoption

### C1. Spec Amendment (section 4.1)

Retain the task-scope state machine in section 4.1 with a `[v1.3 -- deferred]` marker on each task-scope transition. Do not delete or relocate the transitions. The amendment text:

> "Task-scope audit gates (section 4.1 Task scope) are deferred to v1.3, contingent on independent validation and mainline promotion of the task-scope execution model (`execute_phase_tasks()`). The v1.2.1 implementation satisfies section 1.1 'Task gate' via phase-scope gating: tasks are evaluated within phase-scope gate runs using per-task output artifacts."

### C2. NR-1 Resolution (audit_gate_required per task)

Emit `audit_gate_required` per task in tasklist metadata. Define a deterministic phase-level aggregation rule:

```
phase_requires_audit = any(task.audit_gate_required for task in phase.tasks)
```

This aggregation is the v1.2.1 runtime consumer. The per-task field establishes the data contract for v1.3 task-scope gating.

### C3. Evaluator Scope Constraint (Phase 1 deliverable)

When a phase-scope gate fires, the evaluator MUST examine per-task output artifacts within the phase, not only the aggregate phase output. The gate decision is phase-level pass/fail, but evidence collection is per-task. This ensures task-level quality issues are caught even at phase-scope granularity.

**Validation checkpoint**: During Phase 1, verify that phase subprocess output contains identifiable per-task artifacts. If task outputs are not individually addressable within phase output, escalate to the program manager -- this condition weakens the Branch (b) value proposition and may require architectural changes before proceeding.

### C4. KPI Framework Calibration

The following KPI adjustments are required for Branch (b):

| KPI | Issue Under Branch (b) | Resolution |
|---|---|---|
| M1 (Tier-1 runtime P95, <=8s) | No task-scope evaluations exist. M1 is defined for "Task" scope. | Redefine M1 as phase-scope runtime for v1.2.1 with recalibrated threshold (8s was for per-task; per-phase will be longer). Calibrate during shadow mode. |
| M5 (evidence completeness) | Unaffected. Denominator is checks, not scopes. | No change. |
| M8 (false-block rate, T1 <1.0%) | Tier-1 threshold inapplicable (no task-scope gates). Tier-2 measurable but false-positive blast radius is larger at phase scope. | Apply M8 at Tier-2 only. Consider tightening T2 threshold during shadow calibration to account for larger blast radius. |

### C5. TurnLedger Deferral

Defer resolution of `reimbursement_rate` (sprint/models.py:485). The field is confirmed dead (zero usage sites per Delta 2.4). Making a decision about it now adds no value. File as a separate cleanup work item.

### C6. Separate Work Item for Task-Scope Execution

File a standalone work item for `execute_phase_tasks()` mainline activation with:
- Independent acceptance criteria (not tied to audit gate delivery)
- Dedicated integration test suite (real ClaudeProcess, not factory injection only)
- Stall detection and watchdog coverage
- TUI rendering for task-within-phase progress
- State persistence schema for per-task lifecycle
- Delivery milestone independent of v1.2.1

This work item is a prerequisite for v1.3 task-scope audit gates.

### C7. Locked Decision Record (per section 9.3)

Document Branch (b) selection as a locked decision with:
- **Owner**: [to be assigned]
- **UTC deadline**: [to be assigned]
- **Effective rollout phase**: All phases (shadow/soft/full) of v1.2.1
- **Rationale**: MF-1 dead code finding; spec section 4.1 defect; compound delivery risk under Branch (a)

---

## 3. P2b Scope Under Branch (b)

The Phase 2 deliverable is reduced to:

1. Wire `SprintGatePolicy` (executor.py:47-90) into `execute_sprint()` at the post-subprocess integration point (executor.py:668-717) -- phase scope only
2. Extend `OutputMonitor` for lease heartbeat events (builds on existing `last_event_time` at monitor.py:256-259)
3. Wire `TrailingGateRunner` (pipeline/trailing_gate.py) for phase-scope evaluation
4. Wire `ShadowGateMetrics` (models.py:571-618) for shadow mode data collection
5. Add `--grace-period` CLI flag (MF-8)

**Removed from P2b**: "Activate `execute_phase_tasks()` within `execute_sprint()` mainline." This is deferred to the C6 work item.

All 5 items integrate into the existing phase-scope execution model on proven code paths. No dead code activation is on the critical path.

---

## 4. Residual Risks and Caveats

### R1. Phase Output Artifact Identifiability (HIGH)

If Phase 1 investigation reveals that phase subprocess output does not contain individually addressable per-task artifacts, the evaluator cannot perform per-task evidence collection at phase scope. This weakens the core Branch (b) value proposition. Mitigation: validate during Phase 1 before Phase 2 integration begins. If artifacts are not identifiable, decide whether to (a) restructure phase output or (b) accept coarser evaluation granularity.

### R2. Shadow Mode Metric Validity (MEDIUM)

M1 and M8 require recalibration for phase-scope under Branch (b). If shadow mode launches before calibration, the collected metrics may be misleading. Mitigation: complete KPI calibration (C4) as a Phase 1 deliverable, before shadow mode produces promotion-decision data.

### R3. Stakeholder Spec-Compliance Objection (LOW)

Branch (b) violates section 4.1 normative text. Some stakeholders may object to shipping with a known spec deviation. Mitigation: the spec amendment (C1) converts the deviation into a documented, justified scope decision. The evidence base (MF-1 dead code, compound delivery risk) is strong.

### R4. Task-Scope Granularity Insufficiency (LOW, EMPIRICAL)

Phase-scope gates may miss quality issues that task-scope gates would catch. Mitigation: shadow mode data collection (C4/C5 of original Variant 2) provides empirical evidence. If phase-scope consistently misses issues, this informs v1.3 prioritization.

---

## 5. Scenario That Would Reverse This Decision

One scenario was identified that could reverse Branch (b) in favor of Branch (a):

**If phase subprocess output does not contain identifiable per-task artifacts**, the phase-scope evaluator cannot perform meaningful per-task evidence collection. In this case, Phase-scope gating reduces to inspecting an opaque blob, and the "tasks are evaluated within phase-scope gate runs" claim in the spec amendment (C1) becomes false.

This scenario must be tested during Phase 1 as a go/no-go checkpoint for proceeding with Branch (b) into Phase 2.

No other reversal scenario was identified. The absence of downstream consumers of `audit_task_*` states, the absence of regulatory task-scope mandates, and the confirmed dead-code status of `execute_phase_tasks()` all hold.

---

## 6. Evidence Index

| Evidence | Source | Verification |
|---|---|---|
| MF-1 (dead code, CRITICAL) | Adversarial review Section 4 | Unanimous across 3 advocates |
| Section 4.1 (task-scope state machine) | Release spec lines 102-108 | Normative text, 6 transitions |
| Section 1.1 (three scopes) | Release spec lines 25-28 | "Task gate" listed without execution granularity constraint |
| execute_phase_tasks() location | sprint/executor.py:350-447 | Zero call sites in mainline |
| SprintGatePolicy location | sprint/executor.py:47-90 | Real implementations, unwired |
| ShadowGateMetrics location | sprint/models.py:571-618 | Functional, --shadow-gates flag exists |
| TurnLedger.reimbursement_rate dead | sprint/models.py:485 | Zero usage sites (Delta 2.4) |
| Phase 2 acceptance criterion | Release spec line 352 (section 10.3) | "timeout/retry paths terminate deterministically" |
| M1 scope definition | metrics-and-gates.md KPI table | Scope: "Task", threshold <=8s |
| M8 scope definition | metrics-and-gates.md KPI table | Tier-1/2, false-block rate |

---

## 7. Debate Provenance

- **Debate transcript**: `adversarial/debate-transcript.md`
- **Diff analysis**: `adversarial/diff-analysis.md`
- **Variant 1 (Architect)**: `adversarial/variant-1-opus-architect.md`
- **Variant 2 (Analyzer)**: `adversarial/variant-2-opus-analyzer.md`
- **Overall convergence**: 93% after 3 rounds + invariant probe
- **Base selection**: Variant 2 (Analyzer) -- score 8.1/10 vs Variant 1 (Architect) 6.9/10
- **Variant 1 contributions integrated**: NR-1 aggregation mechanism (C-001), concise action checklist format (U-004)
