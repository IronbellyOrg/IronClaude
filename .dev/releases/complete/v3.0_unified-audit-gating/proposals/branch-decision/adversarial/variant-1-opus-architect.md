# Branch Decision Analysis: Variant 1 (Architect)

**Author**: opus:architect
**Date**: 2026-03-17
**Decision**: Branch (b) -- Phase-Only Scope
**Confidence**: 88%

---

## Position Summary

Branch (b) is the architecturally superior choice. The spec mandates task-scope gates in normative language, but the codebase has never executed task-level orchestration -- `execute_phase_tasks()` is dead code confirmed by three independent adversarial advocates (MF-1, severity CRITICAL). Activating dead code to satisfy a spec requirement inverts the correct dependency: the spec should be amended to match the architecture that actually runs in production, not the other way around. Branch (b) delivers a shippable Phase 2 with an 8-state machine on proven execution paths, while branch (a) introduces an unbounded activation risk on code that has zero production history.

---

## Spec Compliance Analysis

### What the spec actually requires

**SS 4.1 -- Legal transitions**: Defines three scope blocks: task, milestone, release. The task scope block specifies six transitions including `in_progress -> ready_for_audit_task`, `audit_task_running -> audit_task_passed | audit_task_failed`, and the retry/override paths. This is normative text. Four of the twelve audit states (`audit_task_*`) exist only to serve task-scope gating.

**SS 4.3 -- Override rules**: "Task and milestone may override failed gate only with approved `OverrideRecord`." This presupposes that task-scope gates produce pass/fail outcomes, which requires a task-scope execution surface.

**SS 5.2 -- Pass/fail rules**: "Completion/release transitions require latest gate `passed` except approved task/milestone override path." The word "completion" applies to tasks completing, which again presupposes task-scope gate evaluation.

**SS 1.1 -- Scope**: Explicitly lists "1. Task gate, 2. Milestone gate, 3. Release gate" as the three scopes.

**Verdict**: The spec unambiguously requires task-scope gates. Branch (b) deviates from SS 4.1 and SS 1.1. This is a real cost. But it is a cost that can be managed through a spec amendment, whereas the alternative cost -- activating dead code -- cannot be managed through documentation.

---

## Branch (a) Assessment: Activate Task-Scope

### Benefits

1. **Full spec compliance**: All 12 audit states from SS 4.1 are implementable. No spec amendment required.
2. **NR-1 consumer exists**: `audit_gate_required` per task has a direct consumer in the task-level execution loop.
3. **TurnLedger integration becomes operative**: The per-task turn budgeting model gains its execution surface.
4. **Finer-grained audit**: Individual tasks can be gated, retried, and overridden independently.

### Costs (with evidence)

1. **Dead code activation risk (CRITICAL)**: `execute_phase_tasks()` at `sprint/executor.py:350-447` has never been called from `execute_sprint()` or anywhere else in the codebase. The adversarial review confirmed this unanimously (MF-1). The mainline loop at `executor.py:574-787` spawns per-phase subprocesses via `ClaudeProcess(config, phase)`. This is not a matter of "wiring up a helper" -- it is activating an entire orchestration model that has zero production runtime history.

2. **Unknown interaction surface**: The dead function presumably interacts with `TurnLedger`, `OutputMonitor`, `SprintGatePolicy`, and the subprocess lifecycle. None of these interaction paths have been exercised. The number of latent bugs in an untested orchestration function is unknowable a priori, but the base rate for dead code reactivation is poor. Every integration point is a potential failure mode.

3. **Testing burden**: Branch (a) requires integration tests for task-level subprocess isolation, per-task lease management, per-task TurnLedger budgeting, task-level retry semantics, and the interaction between task-scope and milestone-scope gates. This is not incremental -- it is a new execution model that must be validated from scratch.

4. **Delivery timeline impact**: P2b under branch (a) includes "Activate `execute_phase_tasks()` within `execute_sprint()` mainline (MF-1 resolution)." This is a prerequisite for all task-scope audit gates. If activation reveals latent defects (likely), the entire P2 timeline slips. The critical path for Phase 2 delivery runs directly through dead code activation.

5. **Regression risk to existing sprint execution**: The current `execute_sprint()` mainline is the production execution path. Restructuring it to call `execute_phase_tasks()` changes the control flow for all sprints, not just audited ones. A regression in the mainline loop affects every user, not just those using audit gates.

### Risk summary

The fundamental problem is that branch (a) treats `execute_phase_tasks()` as "existing infrastructure that needs wiring." The adversarial review explicitly rejects this framing: "The entire task-level orchestration model exists only in the orphaned function" (MF-1). Code that has never run is not infrastructure. It is a hypothesis.

---

## Branch (b) Assessment: Phase-Only

### Benefits

1. **Proven execution surface**: The mainline loop at `executor.py:574-787` is the production code path. Audit gates at phase granularity attach to code that runs every sprint. Zero activation risk.

2. **Reduced state machine complexity**: 8 states instead of 12. The four `audit_task_*` states are eliminated. The transition table shrinks proportionally. The validator is simpler to implement and test.

3. **ShadowGateMetrics integration is straightforward**: `ShadowGateMetrics` at `sprint/models.py:571-618` already tracks per-evaluation metrics. Phase-scope gates produce one evaluation per phase -- a clean 1:1 mapping to the existing metrics model. Task-scope gates would require aggregation logic that does not exist.

4. **SprintGatePolicy wiring is contained**: `SprintGatePolicy` at `executor.py:47-90` has real implementations (not stubs, per the adversarial review's correction of Delta 2.6). Wiring it into the phase-level execution loop is a bounded integration task with clear input/output contracts.

5. **Delivery timeline**: Phase 2 becomes shippable without the dead code activation prerequisite. The critical path is: data models (P1) -> SprintGatePolicy wiring + lease/heartbeat (P2b) -> TUI + release guards (P3). All steps operate on proven code paths.

6. **Milestone and release scopes are unaffected**: Both milestone and release scopes operate above task granularity by definition. Branch (b) delivers full audit gating for all three spec scopes -- task scope is simply evaluated at phase granularity rather than individual-task granularity.

### Costs (with evidence)

1. **Spec deviation**: SS 4.1 explicitly defines task-scope transitions. Branch (b) collapses these to phase-scope, which means the `audit_task_*` states do not exist. This requires a formal spec amendment. The amendment is: "Task-scope audit gates evaluate at phase granularity. Individual task completion within a phase is not independently gated."

2. **NR-1 becomes phase-level**: `audit_gate_required` per task loses its direct consumer. The field either becomes a phase-level aggregation (any task in phase requires audit -> phase requires audit) or is deferred. The adversarial review notes this explicitly: "NR-1 loses its consumer -> no-op or phase-level aggregation." Phase-level aggregation is the correct resolution -- it preserves the push-model auditability benefit (you can inspect the tasklist to see which phases will be gated) without requiring task-level execution.

3. **TurnLedger integration is deferred**: Per-task turn budgeting has no execution surface. This is a capability loss, but given that TurnLedger's `reimbursement_rate` field is already confirmed dead (Delta 2.4, zero usages), the operational impact is minimal -- the integration target itself is partially dead.

4. **Future task-scope gating requires additional work**: If task-scope gates are later required, the work deferred by branch (b) must be done then. However, doing that work later -- after the phase-scope system has production runtime -- is strictly safer than doing it now on dead code.

---

## Downstream Consequence Comparison

### NR-1 (audit_gate_required per task)

| Aspect | Branch (a) | Branch (b) |
|---|---|---|
| Consumer | `execute_phase_tasks()` task loop | Phase-level aggregation function |
| Derivation | Per-task boolean | Per-task boolean aggregated to phase |
| Tasklist schema change | Required (per-task field) | Required (per-task field, consumed as phase aggregate) |
| Determinism argument | Identical -- derivation function is deterministic either way (per adversarial consensus on NR-1) |

Branch (b) does not eliminate NR-1. It changes the consumption model from "per-task gate decision" to "phase-level gate decision derived from per-task metadata." The tasklist can still emit per-task `audit_gate_required` for transparency; the runner aggregates at phase scope.

### ShadowGateMetrics wiring

| Aspect | Branch (a) | Branch (b) |
|---|---|---|
| Evaluation count | N evaluations per phase (one per task) | 1 evaluation per phase |
| Metrics model fit | Requires new aggregation for `total_evaluated` | Clean 1:1 fit with existing model |
| Latency tracking | Per-task latency requires new percentile buckets | Per-phase latency maps directly to existing `latency_ms` |
| Coverage | M1 only (per INV-012) | M1 only (same limitation) |

Branch (b) produces a cleaner metrics integration. Branch (a) requires ShadowGateMetrics to handle N evaluations per phase, which changes the semantics of `total_evaluated` and `latency_ms` percentiles.

### TurnLedger model

| Aspect | Branch (a) | Branch (b) |
|---|---|---|
| Integration | Per-task budgeting becomes operative | Not needed |
| `reimbursement_rate` | Must be resolved (wire or remove) | Can be deferred (already dead per Delta 2.4) |
| Operational risk | Untested budgeting model on untested execution path | None |

Branch (b) avoids compounding two unknowns: dead execution code AND dead model fields.

### Phase ordering

| Aspect | Branch (a) | Branch (b) |
|---|---|---|
| P2a (tasklist metadata) | Full scope -- per-task emission required | Reduced scope -- phase-level aggregation |
| P2b (executor integration) | Includes dead code activation as prerequisite | Excludes dead code activation entirely |
| P3 (TUI + guards) | 12-state display | 8-state display |
| Critical path risk | Dead code activation is on critical path | No dead code on critical path |

---

## Recommendation

**Branch (b): Phase-Only Scope.**

### Full rationale

The architectural argument reduces to a single question: is it safer to amend a spec or to activate dead code?

Amending a spec is a documentation change. It requires the spec owner to approve collapsing task-scope gates to phase-scope gates. The amendment is bounded, reversible, and has zero runtime risk. The adversarial review already provides the exact text: "Under branch (b), items marked with dagger become no-ops" (Section 5). The scope of the amendment is known.

Activating dead code is a runtime change with unbounded risk. `execute_phase_tasks()` has never run. Its interactions with `TurnLedger`, `OutputMonitor`, the subprocess lifecycle, and the stall-detection watchdog are untested. The adversarial review classified MF-1 as CRITICAL -- the highest severity in the entire review -- and all three advocates concurred. The review explicitly states: "The entire task-level orchestration model exists only in the orphaned function."

The spec compliance cost of branch (b) is real but manageable. Four of twelve audit states are eliminated. The override rules in SS 4.3 still apply at milestone scope. The pass/fail rules in SS 5.2 still apply -- "completion transitions require latest gate passed" simply means phase completion rather than task completion. The three-scope model from SS 1.1 is preserved: task scope exists, it simply evaluates at phase granularity.

The delivery cost of branch (a) is real and potentially unbounded. If `execute_phase_tasks()` contains latent defects -- and the base rate for dead code reactivation strongly suggests it will -- the Phase 2 timeline slips. Every day spent debugging an untested orchestration function is a day not spent on the audit gate system that is the actual deliverable.

The correct architectural sequence is:

1. Ship phase-scope audit gates on proven execution paths (branch (b), v1.2.1).
2. Validate the audit gate system in production with shadow/soft/full rollout.
3. If task-scope granularity proves necessary based on production evidence, activate `execute_phase_tasks()` in a subsequent release with dedicated testing, dedicated timeline, and the safety net of a working phase-scope system to fall back to.

This sequence respects the principle that production runtime evidence outweighs spec-level aspirations. The spec can be amended to match reality; reality cannot be amended to match the spec.

### Required actions if branch (b) is adopted

1. **Spec amendment**: SS 4.1 task-scope transitions must be marked as "deferred to future release." The 8-state machine (milestone + release scopes) becomes normative for v1.2.1.
2. **NR-1 resolution**: `audit_gate_required` per task is emitted in tasklist metadata but consumed as a phase-level aggregate by the runner.
3. **TurnLedger decision**: Defer `reimbursement_rate` resolution. It is already dead; making a decision about it now adds no value.
4. **P2b scope reduction**: Remove "Activate `execute_phase_tasks()`" from P2b. The P2b deliverable becomes: SprintGatePolicy wiring + OutputMonitor lease extension + TrailingGateRunner integration + ShadowGateMetrics wiring -- all at phase scope.
5. **Locked decision**: Document branch (b) selection per SS 9.3 with owner, deadline, and rationale.

---

## Appendix: Evidence Index

| Evidence | Source | Location |
|---|---|---|
| MF-1 (dead code) | Adversarial review | Section 4, MF-1 |
| SS 4.1 (task-scope transitions) | Release spec | Section 4.1 |
| SS 4.3 (override rules) | Release spec | Section 4.3 |
| SS 5.2 (pass/fail rules) | Release spec | Section 5.2 |
| SS 1.1 (three scopes) | Release spec | Section 1.1 |
| Delta 2.4 (reimbursement_rate dead) | Adversarial review | Section 1, Delta 2.4 |
| ShadowGateMetrics | Adversarial review | Section 4, MF-3 |
| SprintGatePolicy characterization | Adversarial review | Section 1, Delta 2.6 |
| NR-1 determinism correction | Adversarial review | Section 1, Delta 2.11 note |
| Phase plan (branch conditional) | Adversarial review | Section 5 |
| Branch decision framework | Adversarial review | Section 10 |
