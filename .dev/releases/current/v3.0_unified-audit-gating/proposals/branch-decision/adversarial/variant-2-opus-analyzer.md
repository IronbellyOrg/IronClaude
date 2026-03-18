# Branch Decision Analysis: Variant 2 (Analyzer)

**Author**: opus:analyzer (forensic implementation analysis)
**Date**: 2026-03-17
**Method**: Independent codebase inspection, spec text close-reading, evidence-based hypothesis testing
**Source documents**: adversarial-delta-review-merged.md, unified-audit-gating-v1.2.1-release-spec.md
**Codebase artifacts inspected**: sprint/executor.py, sprint/models.py, sprint/kpi.py, sprint/config.py, pipeline/trailing_gate.py, pipeline/models.py

---

## Position Summary

Branch (b) -- phase-only audit gates -- is the correct choice for Phase 2 delivery. The spec's task-scope language in sections 4.1, 4.3, and 5.2 is normatively aspirational but structurally unbacked: the sprint executor has never run at task granularity in production, and activating orphaned dead code under time pressure to satisfy a state machine that was designed without knowledge of the actual execution architecture is a recipe for a system that passes spec review but fails in operation. The spec should be amended to scope v1.2.1 audit gates to phase granularity, with task-scope gates deferred to v1.3 contingent on `execute_phase_tasks()` being independently validated and promoted to the mainline.

---

## Spec Text Audit: What sections 4.1, 4.3, 5.2 Actually Mandate

### Section 4.1 -- Legal Transitions

The spec defines three scope levels with explicit state machines:

- **Task scope**: `in_progress -> ready_for_audit_task -> audit_task_running -> audit_task_passed|audit_task_failed -> completed` (6 transitions, 4 audit states)
- **Milestone scope**: Same pattern with `audit_milestone_*` (6 transitions, 4 audit states)
- **Release scope**: Same pattern with `audit_release_*` (6 transitions, 4 audit states, terminal is `released` not `completed`, no override path)

This gives the 12 audit states referenced in the adversarial review. The spec presents all three scopes as equally normative -- there is no conditional language, no "if task-scope execution is available" qualifier, no phased delivery allowance. The task-scope state machine is stated as a flat requirement alongside milestone and release.

**However**, the spec's section 1.1 (Scope) states the system "blocks completion/release transitions unless the corresponding gate passes at three scopes: 1. Task gate 2. Milestone gate 3. Release gate." This language ties the gate to the *transition*, not to the execution granularity. A phase completing is a transition. A task completing within a phase is also a transition -- but only if the executor tracks tasks as discrete execution units with independent lifecycle states.

### Section 4.3 -- Override Rules

"Task and milestone may override failed gate only with approved OverrideRecord." This is structurally neutral on whether "task" means a task-scope subprocess (as `execute_phase_tasks()` would produce) or a task identified within a phase-scope result. The override model does not require task-scope execution; it requires task-scope identity in the override record.

### Section 5.2 -- Pass/Fail Rules

"Completion/release transitions require latest gate `passed` except approved task/milestone override path." The word "latest" is ambiguous (as the adversarial review itself notes in section 9). It implies gate results must be current, but says nothing about the granularity at which they are evaluated.

### Verdict on Spec Mandate

The spec's task-scope language is **normatively explicit but architecturally naive**. It was written assuming that the sprint executor has task-scope execution granularity -- an assumption the adversarial review's MF-1 finding proves false. The spec mandates task-scope gates without acknowledging that the execution substrate does not support them. This is a spec defect, not a branch (b) deviation.

The milestone and release scopes map cleanly to phase-scope and sprint-scope respectively, which the current architecture already supports. The only scope that has no execution surface is task-scope.

---

## Dead Code Activation Cost (Branch a)

### What `execute_phase_tasks()` Actually Is

Located at `sprint/executor.py:350-447`, this function is a complete per-task subprocess orchestration loop. It:

1. Iterates over a `list[TaskEntry]`
2. Checks budget against `TurnLedger.can_launch()` before each task
3. Calls `_run_task_subprocess()` (or a test factory) per task
4. Reconciles budget (debit actual, credit back pre-allocation)
5. Returns `(results, remaining_task_ids)` for budget exhaustion

The function is real, non-trivial, and has a test factory injection point (`_subprocess_factory`). It is **not a stub**. But it has critical properties:

### Integration Surface

Wiring `execute_phase_tasks()` into `execute_sprint()` requires replacing the entire phase execution path at lines 574-787. The current mainline:

- Spawns `ClaudeProcess(config, phase)` -- one subprocess per phase
- Monitors output via `OutputMonitor` in a poll loop
- Uses `_determine_phase_status()` for classification
- Writes executor result files, diagnostic reports

`execute_phase_tasks()` operates at a fundamentally different abstraction level. It assumes:

- Tasks are parsed from phase files into `TaskEntry` objects (the parser exists but is not called in the mainline)
- Each task gets its own `ClaudeProcess` with a task-specific prompt
- The `OutputMonitor` would need to reset per task, not per phase
- The TUI would need to show task-level progress within phases
- `_determine_phase_status()` would need to aggregate task results into phase status
- The diagnostic collector would need task-level granularity

**Estimated integration surface**: 8-12 functions need modification, the TUI rendering model changes from phase-list to phase-task-tree, and the state persistence model (`_save_state()`) needs a new schema.

### Test Coverage Gaps

The adversarial review notes test evidence exists at `.dev/releases/complete/unified-audit-gating-v1.2.1/test-evidence/functional/realworld_integration_results_v2.txt`. This test replaces the subprocess with a factory, confirming the function's internal logic works. But:

1. **No integration test with real `ClaudeProcess`**: The function has never spawned a real subprocess in production or CI
2. **No TUI integration test**: The display model for task-within-phase has never been rendered
3. **No state persistence test**: Task-level state has never been serialized/resumed
4. **No stall detection test**: The watchdog at lines 620-653 is per-phase; no equivalent exists per-task
5. **No preflight interaction test**: Phases with `execution_mode in ("python", "skip")` bypass the main loop; their interaction with task-scope execution is undefined

### Rollout Risk

Activating dead code that has never run in production is categorically different from wiring up unwired-but-tested infrastructure. The `SprintGatePolicy` (lines 47-90) is unwired but has a clear, bounded integration point. `execute_phase_tasks()` replaces the entire execution model. This is not "wiring" -- it is an architectural migration within the sprint executor.

**Risk assessment**: HIGH. A failure in `execute_phase_tasks()` during a real sprint means the entire sprint fails with no fallback to the current phase-scope model. There is no feature flag or shadow mode for "try task-scope, fall back to phase-scope."

---

## Phase-Only Scope Cost (Branch b)

### What Actually Breaks

Under branch (b), the following spec items become non-operative:

1. **4 of 12 audit states**: `ready_for_audit_task`, `audit_task_running`, `audit_task_passed`, `audit_task_failed` -- these have no execution surface and are removed
2. **NR-1 (`audit_gate_required` per task)**: No consumer exists. The tasklist generator can still emit this field for forward compatibility, but no executor reads it at task granularity
3. **TurnLedger integration for audit retry**: The ledger's `reimbursement_rate` and per-task budget tracking have no execution surface

### What Is Actually Fine

1. **Milestone-scope gates map to phase-scope gates**: A "milestone" in the current sprint model is a phase. The 4 `audit_milestone_*` states map directly to the existing `PhaseStatus` lifecycle. This is a clean 1:1 mapping.
2. **Release-scope gates map to sprint completion**: The 4 `audit_release_*` states map to `SprintOutcome`. The TUI completion guard (which the adversarial review confirms is absent at `tui.py:254-273`) blocks sprint completion unless `audit_release_passed`.
3. **ShadowGateMetrics**: Already exists at `models.py:571-618` with `--shadow-gates` CLI flag at `config.py:169`. This infrastructure supports the section 7 rollout contract at phase granularity with zero new code.
4. **SprintGatePolicy**: The existing implementation at `executor.py:47-90` is phase-scoped (it references `step_id`, not `task_id`). It can be wired into the existing mainline without architectural changes.
5. **TrailingGateRunner**: The existing infrastructure in `pipeline/trailing_gate.py` operates on `Step` objects, which map to phases in the sprint context.
6. **Override governance**: The `OverrideRecord` model (section 6.2) works at any granularity. Under branch (b), overrides apply to phases (milestone-scope) and sprints (release-scope). The data model is unchanged.
7. **KPI framework**: M1 (latency), M4 (determinism), M5 (evidence completeness), M7 (staleness), M9 (override rate) all work at phase granularity.

### Spec Deviation Extent

Branch (b) deviates from the spec at exactly one point: section 4.1's task-scope state machine. This affects 4 of 12 audit states and 6 of 18 legal transitions. The milestone and release scopes are fully satisfiable.

The deviation is significant in spec-compliance terms but irrelevant in operational terms, because the task-scope states have no execution surface in the current architecture.

---

## Shippability Assessment

### Branch (a): Spec-Compliant but Undeliverable in Phase 2

The Phase 2 acceptance criterion (section 10.3) is: "timeout/retry paths terminate deterministically (no deadlocks)." Under branch (a), this requires:

1. Activating `execute_phase_tasks()` and integrating it into `execute_sprint()` (estimated 2-3 weeks of engineering for the core path)
2. Adding per-task `OutputMonitor` integration (no existing pattern)
3. Adding per-task watchdog/stall detection (the current watchdog is per-phase at executor.py:620-653, defaults to disabled)
4. Adding per-task state persistence to `_save_state()` (schema change)
5. Modifying the TUI to render task-within-phase progress
6. Testing all of the above under real subprocess conditions (not just factory injection)

Items 1-6 constitute a separate feature delivery (the "task-scope execution" feature) that the spec assumes already exists. Delivering it alongside audit gates doubles the integration surface and creates a compound risk: if task-scope execution has bugs, the audit gates are also broken.

**Verdict**: Branch (a) is not deliverable in Phase 2 without accepting the risk of shipping an untested execution model. The spec's Phase 2 acceptance criteria cannot be verified for task-scope gates because the execution substrate has never been validated.

### Branch (b): Deliverable in Phase 2

Under branch (b), Phase 2 requires:

1. Adding 8 audit states to `PhaseStatus` / creating `AuditWorkflowState` alongside it (model change, bounded)
2. Wiring `SprintGatePolicy` into `execute_sprint()` at the existing post-subprocess integration point (executor.py:668-717) -- the class already exists with real implementations
3. Extending `OutputMonitor` for lease heartbeat events (builds on existing `last_event_time` at monitor.py:256-259)
4. Wiring `ShadowGateMetrics` for shadow mode (infrastructure exists)
5. Adding `--grace-period` CLI flag (MF-8, trivial)

All 5 items integrate into the existing phase-scope execution model without architectural changes. The integration points are identified in the adversarial review with file:line precision and have been independently verified in this analysis.

**Verdict**: Branch (b) is deliverable in Phase 2 because it adds audit gates to an execution model that already works, rather than simultaneously building a new execution model and adding audit gates to it.

---

## Downstream Consequence Matrix

| Concern | Branch (a): Task-Scope | Branch (b): Phase-Only |
|---|---|---|
| **NR-1 (`audit_gate_required` per task)** | Required. Tasklist generator must emit per-task flag. Sprint executor must parse and evaluate per-task. Two new integration surfaces. | Optional for forward compatibility. No executor consumer. Can emit for documentation purposes only, or defer entirely. |
| **ShadowGateMetrics wiring** | Must track per-task gate evaluations. `total_evaluated` count inflates by task count per phase. Percentile latency calculations change semantics. Existing `ShadowGateMetrics` at models.py:571-618 needs structural changes. | Direct reuse. `total_evaluated` = number of phases gated. Latency is per-phase-gate. No structural changes to `ShadowGateMetrics`. |
| **TurnLedger integration** | Required. Per-task budget allocation via `execute_phase_tasks()` lines 386-433. Audit retry consumes from same budget pool, creating contention between task execution and audit gate retry. | Not needed. Audit gate evaluation runs within the phase-scope subprocess timeout ceiling. No budget contention. |
| **State machine complexity** | 12 audit states + existing 12 `PhaseStatus` + 4 `TaskStatus` + 7 `GateDisplayState` = 35 enum values across 4 state machines. Transition validation must cover cross-machine interactions (e.g., task audit failure affecting phase status). | 8 audit states + existing 12 `PhaseStatus` + 7 `GateDisplayState` = 27 enum values across 3 state machines. Task-to-phase state propagation is not needed because there is no task-scope state machine. |
| **Phase ordering** | P2a (tasklist metadata) and P2b (executor activation) are both required and have a dependency: P2a produces metadata that P2b consumes. Serialized delivery within Phase 2. | P2a is scope-reduced to optional metadata. P2b is wiring existing `SprintGatePolicy` into existing mainline. Can be parallelized. |
| **TUI impact** | Phase table (tui.py:174-203) must become a tree: phase rows with expandable task sub-rows, each showing audit state. Significant rendering change. | Phase table gains an audit state column per phase. Minimal rendering change, same table structure. |
| **`_save_state()` persistence** | Must persist per-task audit state, lease status, and retry counts. Schema change to the state file format. Resume-from-halt must restore task-level audit state. | Must persist per-phase audit state. Adds fields to existing phase-level state records. No schema migration needed. |
| **Preflight bypass (MF-10)** | Preflight phases (`execution_mode in ("python", "skip")`) produce `PREFLIGHT_PASS` without entering the main loop. Under task-scope, must decide: do preflight phases have tasks? If yes, do those tasks get audited? New decision surface. | Preflight phases are phase-scope. Decision is binary: exempt or gated. Clean. |
| **`cli/audit/` subsystem reuse (MF-4)** | Existing `GateResult` in `audit/evidence_gate.py` has 2 fields. Spec requires 13-field `AuditGateResult`. Namespace collision (MF-2). Per-task evaluation would need to integrate with the existing audit subsystem's budget/checkpoint model, which operates at a different granularity. | Same namespace collision exists but is contained to phase-scope. No interaction with per-task audit budget model. |
| **Rollback safety** | If task-scope audit gates fail in production, rollback requires disabling both the audit gates AND the task-scope execution model -- returning to phase-scope execution. This is a two-variable rollback, harder to diagnose. | Rollback disables audit gates only. Execution model is unchanged. Single-variable rollback. |

---

## Counter-Arguments Addressed

### "The spec says task-scope, so we must build task-scope"

The spec was written without knowledge that `execute_phase_tasks()` is orphaned dead code. Section 4.1 assumes an execution substrate that does not exist. Building that substrate is a prerequisite to task-scope audit gates, not part of the audit gate feature. Conflating "build task-scope execution" with "add audit gates" violates scope discipline and creates compound delivery risk.

### "We should activate `execute_phase_tasks()` anyway because it is good engineering"

This may be true, but it is a separate engineering decision with its own risk profile. The function has never run in production. Activating it requires integration testing that is independent of audit gate testing. These should be separate work items with separate delivery milestones. Bundling them guarantees that if either fails, both fail.

### "Phase-scope audit gates are too coarse to catch task-level quality issues"

This is an empirical claim that should be tested during shadow mode. If phase-scope gates consistently miss quality issues that task-scope gates would catch, that is evidence for prioritizing task-scope execution in v1.3. If phase-scope gates catch the same issues (because a phase that contains a failing task also fails at phase scope), then task-scope adds complexity without value.

### "The 8-state machine is still over-engineered"

A fair challenge. The 8 states under branch (b) are:

- `ready_for_audit_milestone`, `audit_milestone_running`, `audit_milestone_passed`, `audit_milestone_failed` (4 states for phase-scope)
- `ready_for_audit_release`, `audit_release_running`, `audit_release_passed`, `audit_release_failed` (4 states for sprint-scope)

Each scope needs exactly 4 states to represent the audit lifecycle (ready, running, passed, failed). This is the minimum viable state machine for a lease-based audit model with retry. Reducing further would mean collapsing "running" into "ready" (losing lease tracking) or collapsing "passed/failed" into a single terminal (losing the retry path). Neither reduction is safe.

---

## Recommendation

**Choose branch (b): phase-only audit gates for v1.2.1.**

Conditions:

1. **Amend section 4.1** to scope v1.2.1 to milestone (phase) and release (sprint) audit gates. Add a forward reference: "Task-scope audit gates (section 4.1 Task scope) are deferred to v1.3, contingent on independent validation and mainline promotion of the task-scope execution model."

2. **Do not delete the task-scope state machine from the spec.** Retain it in section 4.1 with a status marker (`[v1.3 -- deferred]`) so the design intent is preserved.

3. **File a separate work item** for `execute_phase_tasks()` mainline activation, with its own acceptance criteria, integration tests, and delivery milestone. This work item is a prerequisite for v1.3 task-scope audit gates but is independent of v1.2.1.

4. **Emit `audit_gate_required` in tasklist metadata** as a forward-compatibility measure even under branch (b). The field has no runtime consumer in v1.2.1 but establishes the data contract for v1.3. This is low-cost (tasklist generator change only) and reduces future migration friction.

5. **Use shadow mode at phase granularity** to collect empirical data on whether phase-scope gates are sufficient or whether task-scope granularity is needed. This data informs the v1.3 decision with evidence rather than spec assumptions.

6. **Document the branch decision as a locked decision per section 9.3** with owner, UTC deadline, and effective rollout phase. This is not a deferral -- it is a scoping decision backed by architectural evidence (MF-1) that the spec did not account for.

### Risk Under This Recommendation

The primary risk is that phase-scope audit gates miss quality issues at task granularity. This risk is mitigated by:

- Shadow mode data collection (condition 5)
- Forward-compatible data model (condition 4)
- Preserved spec design intent (condition 2)
- Independent execution model validation (condition 3)

The secondary risk is stakeholder objection to spec deviation. This is mitigated by the evidence that the spec's task-scope requirement was written against a nonexistent execution substrate -- the deviation is a correction, not a compromise.

---

## Evidence Index

| Claim | Evidence Location | Verification |
|---|---|---|
| `execute_phase_tasks()` is orphaned | `sprint/executor.py:350-447` -- defined; grep shows zero call sites in executor mainline | CONFIRMED |
| `execute_sprint()` operates at phase scope | `sprint/executor.py:491-787` -- `ClaudeProcess(config, phase)` at line 578 | CONFIRMED |
| `ShadowGateMetrics` exists and is functional | `sprint/models.py:571-618`, `sprint/config.py:169` (`shadow_gates: bool = False`) | CONFIRMED |
| `SprintGatePolicy` is implemented but unwired | `sprint/executor.py:47-90` -- full implementations, never instantiated in `execute_sprint()` | CONFIRMED |
| `PhaseStatus` has 12 states, none audit-related | `sprint/models.py:206-249` | CONFIRMED |
| `TaskStatus` has 4 states | `sprint/models.py:40-46` | CONFIRMED |
| `GateDisplayState` has formal transition model | `sprint/models.py:107-114` (`GATE_DISPLAY_TRANSITIONS` frozenset) | CONFIRMED |
| `TurnLedger.reimbursement_rate` is unused | `sprint/models.py:485` -- single definition, zero usage sites | CONFIRMED |
| Spec section 4.1 mandates task-scope without conditional language | `unified-audit-gating-v1.2.1-release-spec.md` lines 102-108 | CONFIRMED |
| Spec section 10.3 Phase 2 criterion is "timeout/retry paths terminate deterministically" | `unified-audit-gating-v1.2.1-release-spec.md` line 352 | CONFIRMED |
