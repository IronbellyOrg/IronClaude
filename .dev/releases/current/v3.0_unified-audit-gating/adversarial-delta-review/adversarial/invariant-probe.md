# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | MF-1 resolution is a binary fork (activate task-scope vs phase-only); downstream consensus is valid only under branch (a) | UNADDRESSED | HIGH | MF-1 has two branches: (a) activate execute_phase_tasks in mainline, (b) scope gates to phase granularity only. Branch (b) invalidates NR-1, parts of §4.1 state machine, and the tasklist metadata emission requirement. The consensus treats MF-1 as a simple P0 prerequisite without specifying which branch. |
| INV-002 | state_variables | The 12-state audit state machine (§4.1) is conditional on MF-1 branch (a); branch (b) reduces it to 8 states | UNADDRESSED | MEDIUM | If task-scope gates are abandoned, 4 of 12 audit states (audit_task_*) become unnecessary, changing Delta 2.8 severity and Phase 1 scope. |
| INV-003 | state_variables | GateDisplayState's "operationally inert" classification assumes is_valid_gate_transition() is never called at runtime | UNADDRESSED | LOW | No advocate verified whether any code path calls is_valid_gate_transition(). |
| INV-004 | guard_conditions | Delta 2.1 HIGH severity assumes the auto-resume call site is unconditional; the call site guard was not verified | UNADDRESSED | MEDIUM | The function is reachable but may be guarded by --resume + specific state conditions. If unreachable in audit gate context, severity drops to LOW. |
| INV-005 | guard_conditions | NR-3's validity depends on whether any §5.1-§5.3 evaluation rule references deviation-analysis.md; this was never checked | UNADDRESSED | HIGH | NR-3 was resolved by majority vote (real independent finding), not by checking whether the spec actually requires audit gates to inspect deviation-analysis.md. If no spec rule references this artifact, the Architect's "false dependency" position is correct. |
| INV-006 | guard_conditions | The stall monitor (120s) used as "heartbeat substrate" is operationally disabled by default (config.stall_timeout=0) | UNADDRESSED | MEDIUM | Building audit lease heartbeat on a disabled-by-default mechanism means the audit system inherits an inert guard condition. |
| INV-007 | count_divergence | 12 PhaseStatus + 12 audit states = 24 states without checking semantic overlap (e.g., audit_task_failed(timeout) vs PhaseStatus.TIMEOUT) | UNADDRESSED | MEDIUM | Two parallel state machines may produce conflicting reports for the same event. |
| INV-008 | count_divergence | Comparing task audit max_attempts=3 vs roadmap remediation max_attempts=2 is cross-domain; the scopes are incommensurable | UNADDRESSED | LOW | Roadmap file-group retries have different cost models than audit evaluation retries. |
| INV-009 | count_divergence | A-004 status changes from UNSTATED to CONTRADICTED between the two diff-analysis tables; summary count uses the derived value without noting the dual classification | UNADDRESSED | LOW | Minor bookkeeping inconsistency. |
| INV-010 | collection_boundaries | cli/audit/ "30+ modules" treated as homogeneously relevant, but no one opened the files; domain semantics may not align with audit gating | UNADDRESSED | HIGH | audit/evidence_gate.GateResult has 2 fields (passed, reason) vs spec's 13-field GateResult — structurally incompatible. The "30+ modules" count creates false importance if domain semantics don't match. |
| INV-011 | collection_boundaries | NR-5/NR-6 merge into one finding conceals two distinct dependency chains (reactive invalidation vs proactive binding) | UNADDRESSED | MEDIUM | Implementing only one half (binding without invalidation, or vice versa) produces a silently incomplete system. |
| INV-012 | collection_boundaries | ShadowGateMetrics tracks pass/fail/latency but not retry counts, M4, M5, M7, or M9; integration opportunity is limited to M1 (latency) | UNADDRESSED | MEDIUM | Only 1 of 5 required KPI dimensions is covered by existing metrics infrastructure. |
| INV-013 | interaction_effects | Removing line citations + MF-1 resolution together leave §10.2 Phase 2 with no anchoring to codebase | UNADDRESSED | MEDIUM | Line citations were the only precision mechanism; MF-1 invalidates the targets. Combined effect leaves implementers with a behavioral statement and no code reference. |
| INV-014 | interaction_effects | If MF-1 resolved via branch (b) (phase-only), NR-1 (audit_gate_required per task) loses its consumer and becomes pointless | UNADDRESSED | HIGH | audit_gate_required is consumed per-task by the sprint executor; if executor operates per-phase only, the field needs phase-level aggregation or becomes unnecessary. |
| INV-015 | interaction_effects | Shadow mode is the calibration mechanism for unjustified defaults, but ShadowGateMetrics lacks retry-count tracking needed for that calibration | UNADDRESSED | MEDIUM | Cannot calibrate task=3/milestone=2/release=1 defaults using metrics that don't record per-entity retry counts. |
| INV-016 | interaction_effects | MF-2 (GateResult collision) severity is conditional on MF-4 (cli/audit/ survey); survey may reveal additional consumers | UNADDRESSED | LOW | Severity assessment is premature without completing the survey. |

## Summary

- **Total findings**: 16
- **ADDRESSED**: 0
- **UNADDRESSED**: 16
  - HIGH: 4 (INV-001, INV-005, INV-010, INV-014)
  - MEDIUM: 8 (INV-002, INV-004, INV-006, INV-007, INV-011, INV-012, INV-013, INV-015)
  - LOW: 4 (INV-003, INV-008, INV-009, INV-016)

## Critical Fault Pattern

The four HIGH findings share a common root: **MF-1 resolution is a branching point that the consensus treats as a simple prerequisite but is actually a binary fork that invalidates different subsets of the consensus depending on which branch is taken.** The consensus is internally consistent only under the implicit assumption that MF-1 is resolved by activating task-scope execution (branch a). If branch (b) is chosen (phase-only granularity), consensus points on NR-1, the 12-state machine, tasklist metadata, and the §4.4 defaults require revision.
