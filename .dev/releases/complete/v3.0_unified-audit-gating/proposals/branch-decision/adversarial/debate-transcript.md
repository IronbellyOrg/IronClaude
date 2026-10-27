# Debate Transcript: Branch Decision — Phase-Only (b) vs Task-Scope (a)

**Orchestrator**: Claude Opus 4.6 (neutral coordinator)
**Variant 1**: opus:architect (Branch (b), 88% confidence)
**Variant 2**: opus:analyzer (Branch (b), conditions stated)
**Date**: 2026-03-17
**Debate type**: Convergent refinement (both variants agree on Branch (b); debate targets conditions, edge cases, and invariant challenges)
**Rounds**: 3 + invariant probe

---

## Round 1: Debate on Diff Points

### D1-C001: NR-1 Under Branch (b) — Aggregation vs Forward-Compat Emit

**Variant 1 position**: Tasklist emits per-task `audit_gate_required`; the runner aggregates to phase scope (any task flagged -> phase is gated). This preserves the push-model auditability benefit.

**Variant 2 position**: Emit the field for forward compatibility but acknowledge it has no runtime consumer. Can emit or defer entirely.

**Adjudication**: These positions are compatible, not contradictory. Variant 1 is more precise about the *mechanism* (aggregation function), while Variant 2 is more honest about the *operational status* (no consumer in v1.2.1). The merged position is:

> Emit `audit_gate_required` per task in tasklist metadata. Define a phase-level aggregation rule: `phase_requires_audit = any(task.audit_gate_required for task in phase.tasks)`. This aggregation is the v1.2.1 consumer. The per-task field also serves as the v1.3 forward-compatibility contract.

**Convergence**: 95% — both agree on emit; Variant 1's aggregation mechanism is strictly additive.

---

### D1-C003: Total State Machine Complexity

**Variant 1 position**: "8 states instead of 12" — characterizes only the audit state reduction.

**Variant 2 position**: Counts all state machines in the system: PhaseStatus (12) + TaskStatus (4) + AuditWorkflowState (8 or 12) + GateDisplayState (7) = 27 under (b) vs 35 under (a). Provides total system complexity view.

**Adjudication**: Variant 2's characterization is more complete and more useful for implementation planning. Variant 1's "8 vs 12" is correct but narrow — it counts only the audit-specific delta without accounting for cross-machine interaction complexity.

However, a correction is needed: under Branch (b), TaskStatus (4 states) still exists for non-audit purposes. It does not gain audit states, but it still participates in the system. The correct counts are:
- Branch (a): 12 audit + 12 PhaseStatus + 4 TaskStatus + 7 GateDisplayState = 35 enum values, 4 state machines with cross-machine transitions required
- Branch (b): 8 audit + 12 PhaseStatus + 4 TaskStatus + 7 GateDisplayState = 31 enum values, 3 state machines with cross-machine transitions (task-to-phase propagation eliminated)

The operational complexity reduction is not just 4 fewer states — it is the elimination of one entire cross-machine interaction layer (task audit state -> phase status propagation).

**Convergence**: 90% — Variant 2's framing adopted with minor correction.

---

### D1-C005: Branch (a) Delivery Estimate

**Variant 1 position**: No timeline estimate; characterizes risk as "if activation reveals latent defects (likely), Phase 2 slips." Uses qualitative risk language.

**Variant 2 position**: Estimates 2-3 weeks for the core `execute_phase_tasks()` activation path + 5 additional integration items (OutputMonitor, watchdog, state persistence, TUI, real subprocess testing). Characterizes the total as "a separate feature delivery."

**Adjudication**: Variant 2's estimate is more actionable. However, neither variant can verify the 2-3 week estimate without actually attempting the work — the function is dead code, so estimating its activation cost is inherently speculative.

The more important claim is Variant 2's framing: activating `execute_phase_tasks()` constitutes a *separate feature delivery* that the spec assumes already exists. This is a structural argument that does not depend on timeline accuracy. Whether activation takes 2 weeks or 6, it is still a prerequisite that is independent of the audit gate feature.

Variant 1's "likely latent defects" is a probability claim that is well-supported by the base rate for dead code reactivation but is not verified for this specific function. The function does have a test factory injection point, suggesting the author intended it to be testable. However, the tests that exist use factory injection (mock subprocess), not real ClaudeProcess — so the integration surface is still untested.

**Merged position**: Branch (a) activation is estimated at 2-3 weeks minimum for core path (Variant 2), with high probability of latent defects extending that timeline (Variant 1). The critical framing is that this is a separate deliverable, not an incremental cost.

**Convergence**: 92%.

---

### D1-X002: Spec Amendment Language — "Deferred" vs "Retain with [v1.3] Marker"

**Variant 1 position**: "SS 4.1 task-scope transitions must be marked as 'deferred to future release.'"

**Variant 2 position**: "Do NOT delete the task-scope state machine from the spec. Retain it in section 4.1 with a status marker (`[v1.3 -- deferred]`)."

**Adjudication**: These are semantically identical but Variant 2 is more explicit about the anti-pattern being prevented: accidental deletion of the design intent. Variant 1's "marked as deferred" is ambiguous — it could mean "annotate in place" or "move to a deferred section." Variant 2's "retain with marker" is unambiguous.

**Merged position**: Retain the task-scope state machine in section 4.1 with a `[v1.3 -- deferred]` marker on each task-scope transition. Do not delete or move the transitions. The marker makes the design intent clear while preventing implementers from treating task-scope as a v1.2.1 requirement.

**Convergence**: 98% — effectively the same recommendation; Variant 2's phrasing is strictly clearer.

---

### D1-U001: Downstream Consequence Matrix (Variant 2 Unique)

**Assessment**: Variant 2's 9-row consequence matrix (NR-1, ShadowGateMetrics, TurnLedger, state machine complexity, phase ordering, TUI impact, `_save_state()` persistence, preflight bypass, `cli/audit/` subsystem reuse, rollback safety) surfaces three items not covered by Variant 1:

1. **Preflight bypass (MF-10)**: Under Branch (a), preflight phases with `execution_mode in ("python", "skip")` create a new decision surface — do their tasks get audited? This is an undefined interaction. Under Branch (b), it is binary: phase is exempt or gated.

2. **`_save_state()` schema impact**: Branch (a) requires per-task audit state persistence with schema migration. Branch (b) adds fields to existing phase-level records without schema change.

3. **Rollback safety**: Branch (a) requires two-variable rollback (disable audit gates AND revert task-scope execution). Branch (b) requires single-variable rollback (disable audit gates only).

**Verdict**: The matrix surfaces real operational concerns (especially rollback safety and preflight bypass) that strengthen the Branch (b) case. These do not change the decision direction but they add conditions that the merged recommendation must address. The preflight bypass issue in particular should be documented as a resolved design question under Branch (b).

**Convergence**: N/A (unique contribution, adopted into merged output).

---

### D1-A002: Phase-Scope Gate Value — Neither Variant Verifies in Production

**Challenge posed**: Both variants assume that phase-scope audit gates deliver meaningful operational value without presenting evidence that phase-scope granularity catches quality issues. If a phase contains 10 tasks of wildly varying quality, does a phase-scope gate catch the failing task?

**Variant 1 implicit response**: Cites shadow mode as the validation mechanism but does not elaborate on what constitutes "sufficient."

**Variant 2 explicit response**: "Phase-scope audit gates miss quality issues at task granularity — this is an empirical claim that should be tested during shadow mode." Also: "If phase-scope gates consistently miss quality issues that task-scope gates would catch, that is evidence for prioritizing task-scope execution in v1.3."

**Adjudication**: Both variants acknowledge the gap. The question is whether this gap is a *blocking* concern or an *empirical* one. The answer depends on what the audit gate evaluator actually inspects:

- If the evaluator inspects per-task output artifacts (individual task output files), then phase-scope gating still evaluates at task granularity — it just aggregates the result to a phase-level pass/fail. The gate fires per phase, but the evidence examination is per artifact.
- If the evaluator inspects only the phase-level aggregate output, then task-level quality issues could be masked.

Neither variant specifies which model the evaluator uses. This is a design decision that must be made during Phase 1 (deterministic contracts + evaluator). The merged recommendation must include a condition that the phase-scope evaluator examines per-task artifacts even though the gate fires at phase scope.

**Merged position**: Phase-scope gating is operationally sufficient IF the evaluator examines per-task output artifacts within the phase. The gate decision aggregates to phase scope, but evidence collection must be per-task. This must be specified as a Phase 1 deliverable condition. Shadow mode data (Variant 2's condition 5) validates whether this approach catches the same issues as task-scope gating would.

**Convergence**: 85% — both acknowledge the gap; merged position resolves it with a concrete design constraint.

---

## Round 2: Invariant Probe

Three invariants were probed against the emerging Branch (b) consensus.

### INV-1: Does Phase-Scope Gating Satisfy Section 1.1's "Task Gate" Requirement?

**Spec text** (section 1.1): "blocks completion/release transitions unless the corresponding gate passes at three scopes: 1. Task gate 2. Milestone gate 3. Release gate"

**Probe**: Is renaming task-scope evaluation to phase-scope a legitimate interpretation, or is it a spec violation?

**Analysis**:

The spec's section 1.1 uses the term "Task gate" without defining its execution granularity. Section 4.1 provides the detailed state machine, which explicitly defines per-task transitions (`in_progress -> ready_for_audit_task`). These are two different levels of specificity:

- Section 1.1 establishes the *intent*: three scopes of gating exist.
- Section 4.1 establishes the *mechanism*: per-task state transitions.

Under Branch (b), the intent (section 1.1) is satisfiable: tasks are gated, just at phase granularity rather than individual granularity. The mechanism (section 4.1) is not satisfiable: the `audit_task_*` transitions do not exist.

**Verdict**: This is a genuine spec violation of section 4.1, not a reinterpretation. The merged recommendation must acknowledge this as a deviation requiring a formal spec amendment. The amendment text should state: "Section 1.1 'Task gate' is implemented as phase-scope gating in v1.2.1. The section 4.1 task-scope state machine is deferred to v1.3." Framing it as "the spec was wrong" (Variant 2) or "the spec should be amended to match reality" (Variant 1) are equivalent — both mean the spec must change. The key is that this is a *known, documented, justified* deviation, not a silent omission.

**Impact on decision**: Does not reverse Branch (b). The deviation is bounded (4 of 12 audit states) and the spec amendment is a documentation task with zero runtime risk. The alternative (activating dead code to satisfy a spec requirement) carries runtime risk that outweighs spec-compliance value.

---

### INV-2: Gate Trigger Mechanism Under Branch (b)

**Probe**: If a phase contains 10 tasks of which 3 are STRICT-tier, does the gate fire? What triggers the phase-level audit gate if not `audit_gate_required` per task?

**Analysis**:

Under Branch (b) with the C-001 merged resolution:

1. The tasklist generator emits `audit_gate_required` per task based on task tier, profile, and policy.
2. The phase-level aggregation rule `phase_requires_audit = any(task.audit_gate_required for task in phase.tasks)` evaluates to `True` if any task in the phase requires audit.
3. The phase-scope gate fires after the phase subprocess completes.
4. The evaluator examines the phase output (per the A-002 resolution: including per-task artifacts).

So for 10 tasks with 3 STRICT-tier: `audit_gate_required = True` for those 3 tasks, `phase_requires_audit = True`, gate fires, evaluator examines all 10 task outputs within the phase.

**Follow-up concern**: What if the 3 STRICT tasks pass but 7 non-gated tasks fail quality? The answer depends on the evaluator's scope. If the evaluator examines all task artifacts in a gated phase (recommended), then all 10 are evaluated. If it only examines STRICT-tier task artifacts, then the 7 are missed.

**Verdict**: The trigger mechanism is well-defined. The evaluator scope must be specified: when a phase is gated, ALL task artifacts in the phase are evaluated, not just those from tasks with `audit_gate_required = True`. This is a Phase 1 design constraint.

**Impact on decision**: Does not reverse Branch (b). Adds a concrete design constraint to the conditions.

---

### INV-3: Shadow Mode KPI Denominator Under Branch (b)

**Probe**: ShadowGateMetrics tracks `total_evaluated` at phase scope. M5 (evidence completeness) and M8 (false-block rate) use evaluation counts as denominators. Phases are coarser than tasks — does the metric's meaning change?

**Analysis**:

Metrics affected by granularity change:

- **M1 (Tier-1 runtime P95)**: Defined with scope "Task" and threshold "<=8s". Under Branch (b), there are no task-scope gate evaluations. M1 either (a) measures phase-scope Tier-1 evaluations (but Tier-1 is defined as task-tier, and phases are milestone-tier), or (b) is inapplicable under Branch (b).

  This is a real problem. M1 is defined for "Task" scope with an 8-second threshold. Under Branch (b), there is no task-scope evaluation to measure. The metric must be reinterpreted: M1 measures the lowest-scope gate evaluation available, which under Branch (b) is phase-scope (milestone-tier). The 8-second threshold was calibrated for per-task evaluation and may be inappropriate for per-phase evaluation.

- **M5 (evidence completeness)**: Scope is "Failed checks." Under Branch (b), failed checks are per-phase. If the evaluator examines per-task artifacts (INV-2 resolution), evidence completeness is still per-check — the denominator is checks, not evaluations. M5 is unaffected by scope change.

- **M8 (false-block rate)**: Defined for Tier-1/2 with thresholds "<1.0% (T1), <0.5% (T2)". Under Branch (b), Tier-1 (task-scope) has no gate evaluations. M8's T1 threshold is inapplicable. M8 at T2 (milestone/phase scope) is measurable. The false-block *rate* denominator is "total phase evaluations," which is well-defined.

  However, the false-positive *meaning* changes. A false block at task scope means one task was incorrectly blocked. A false block at phase scope means an entire phase (potentially containing 10+ tasks) was incorrectly blocked. The blast radius of a false positive is larger, which could argue for a *tighter* M8 threshold at phase scope, not the same threshold.

**Verdict**: The KPI framework needs a Branch (b)-specific calibration note:
1. M1 is inapplicable at task-scope under Branch (b); redefine as phase-scope runtime or defer M1 to v1.3.
2. M5 is unaffected (denominator is checks, not scopes).
3. M8 at Tier-1 is inapplicable; M8 at Tier-2 is measurable but false-positive blast radius is larger than originally designed. Consider tightening M8 T2 threshold during shadow calibration.

**Impact on decision**: Does not reverse Branch (b) but identifies a concrete KPI calibration task that must be completed during Phase 1. This is a risk of shipping without the calibration note — shadow mode could produce metrics that are meaningless or misleadingly favorable.

---

## Round 3: Edge Case — When Would Branch (a) Be Correct?

**Probe**: Is there any scenario where the Branch (b) consensus should be reversed in favor of Branch (a)?

**Identified scenarios**:

1. **Scenario**: A downstream consumer already depends on per-task audit state transitions (e.g., a CI/CD integration that reads `audit_task_passed` to unblock deployments).
   **Status**: No evidence of such a consumer exists. The `audit_task_*` states do not yet exist in the codebase (PhaseStatus has 12 non-audit states; TaskStatus has 4 non-audit states). No external integration could depend on states that have never been implemented.

2. **Scenario**: `execute_phase_tasks()` has been recently tested and validated outside the mainline (e.g., in a feature branch with integration tests).
   **Status**: The adversarial review's MF-1 finding (CRITICAL, unanimous) states the function is orphaned with zero production history. The test evidence uses factory injection, not real subprocess integration. No feature branch evidence has been presented.

3. **Scenario**: Regulatory or compliance requirements mandate per-task audit granularity.
   **Status**: No regulatory context has been presented. The spec's three-scope model originates from the project's own requirements spec, not an external mandate.

4. **Scenario**: The phase-scope evaluator cannot meaningfully assess quality at task granularity because task output artifacts are not individually identifiable within phase output.
   **Status**: This is an architectural question about the sprint executor's output format. If phase subprocess output intermingles task outputs without clear boundaries, per-task evidence collection (INV-2 resolution) may not be feasible. This would weaken Branch (b) because the gate evaluator would be inspecting an opaque blob rather than structured per-task evidence.

   **Assessment**: Scenario 4 is the most plausible reversal condition. If investigation during Phase 1 reveals that phase output does not contain identifiable per-task artifacts, Branch (b)'s value proposition weakens significantly. The merged recommendation must include a Phase 1 validation checkpoint for this.

**Convergence**: 93% — Branch (b) consensus holds. Scenario 4 is promoted to a Phase 1 validation gate.

---

## Scoring Matrix

### Diff Point Scores

| ID | Category | Topic | V1 Score | V2 Score | Winner | Merged Resolution |
|---|---|---|---|---|---|---|
| S-001 | Structural | Conclusion framing | 7/10 | 8/10 | V2 | "Spec defect" framing is more precise than "doc vs runtime risk" |
| S-002 | Structural | Branch (b) conditions | 7/10 | 9/10 | V2 | V2 has 6 conditions with forward-compat emphasis; V1's 5 are a subset |
| S-003 | Structural | Counter-arguments | 0/10 | 8/10 | V2 | V2 provides systematic counter-argument section; V1 omits |
| C-001 | Content | NR-1 resolution | 8/10 | 7/10 | V1 | V1 specifies aggregation mechanism; V2 is vaguer |
| C-002 | Content | TurnLedger | 7/10 | 7/10 | Tie | Both reach "defer"; V1 says "already dead," V2 says "not needed" |
| C-003 | Content | State machine complexity | 6/10 | 9/10 | V2 | V2 counts all state machines; V1 counts only audit delta |
| C-004 | Content | execute_phase_tasks() detail | 7/10 | 9/10 | V2 | V2 enumerates integration surface (8-12 functions); V1 is qualitative |
| C-005 | Content | Branch (a) delivery | 6/10 | 8/10 | V2 | V2 provides timeline estimate + "separate feature" framing |
| C-006 | Content | Spec deviation extent | 7/10 | 8/10 | V2 | V2 gives precise count (4/12 states, 6/18 transitions) |
| C-007 | Content | Rollback safety | 6/10 | 8/10 | V2 | V2 explicitly models single-variable vs two-variable rollback |
| X-001 | Contradiction | 8-state sufficiency | 7/10 | 8/10 | V2 | V2 raises AND resolves the question; V1 asserts without defense |
| X-002 | Contradiction | Spec amendment language | 6/10 | 9/10 | V2 | V2 is unambiguous ("retain with marker"); V1 is ambiguous ("mark as deferred") |
| U-001 | Unique | Downstream matrix | -- | 9/10 | V2 | Surfaces preflight bypass, rollback safety, state persistence |
| U-002 | Unique | Counter-arguments | -- | 8/10 | V2 | Systematic defense of four challenges |
| U-003 | Unique | Shippability assessment | -- | 8/10 | V2 | References Phase 2 acceptance criterion (section 10.3) |
| U-004 | Unique | Action checklist | 8/10 | -- | V1 | V1's 5-item checklist is more concise and immediately actionable |
| A-001 | Assumption | MF-1 dead code | 8/10 | 8/10 | Tie | Both correctly cite MF-1 |
| A-002 | Assumption | Phase-scope sufficiency | 5/10 | 6/10 | V2 (marginal) | V2 explicitly acknowledges the gap and proposes shadow-mode validation; V1 is implicit |

### Aggregate Scores

| Variant | Avg Score (scored items) | Unique Contributions | Overall |
|---|---|---|---|
| V1 (Architect) | 6.9/10 | 1 (U-004) | Strong on concise action items and NR-1 mechanism. Weaker on total system analysis and counter-argument coverage. |
| V2 (Analyzer) | 8.1/10 | 3 (U-001, U-002, U-003) | Stronger on forensic detail, total complexity analysis, and systematic defense. Weaker on nothing material. |

### Base Selection

**Variant 2 (Analyzer) is the recommended base** for the merged decision, with Variant 1's NR-1 aggregation mechanism (C-001) and action checklist (U-004) integrated.

---

## Invariant Probe Results

| ID | Invariant Tested | Result | Impact on Decision |
|---|---|---|---|
| INV-1 | Section 1.1 "Task gate" satisfaction | VIOLATION of section 4.1; satisfiable under section 1.1 with reinterpretation | Requires spec amendment (already planned). Does not reverse Branch (b). |
| INV-2 | Phase-scope gate trigger with mixed-tier tasks | Well-defined via aggregation rule. Evaluator scope must include all task artifacts in gated phase. | Adds Phase 1 design constraint. Does not reverse Branch (b). |
| INV-3 | KPI denominator under phase-scope | M1 inapplicable at task-scope. M5 unaffected. M8 blast radius larger than designed. | Adds KPI calibration task to Phase 1. Does not reverse Branch (b). |

---

## Final Convergence Assessment

| Area | Convergence | Status |
|---|---|---|
| Branch selection (b) | 98% | CONVERGED |
| Spec amendment approach | 98% | CONVERGED (retain with [v1.3] marker) |
| NR-1 resolution | 95% | CONVERGED (emit + aggregate) |
| A-002 (phase-scope sufficiency) | 85% | CONDITIONALLY CONVERGED (requires Phase 1 artifact identifiability check) |
| KPI calibration | 88% | CONVERGED (M1 redef, M8 recalibration needed) |
| Action items | 93% | CONVERGED (V2's 6 conditions + V1's checklist format) |

**Overall convergence: 93%** (above 85% threshold).
