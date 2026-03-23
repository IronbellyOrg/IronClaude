# v3.2 TurnLedger-Native Wiring Gate Brainstorm

Date: 2026-03-20
Spec analyzed: `/config/workspace/IronClaude/.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`

## Framing

Goal: make v3.2 Wiring Verification Gate **TurnLedger-native from day one**, instead of adding TurnLedger semantics later.

Key code reality from the current implementation:

- `TurnLedger` already models `initial_budget`, `consumed`, `reimbursed`, `reimbursement_rate`, `minimum_allocation`, and `minimum_remediation_budget` in `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py`.
- `execute_phase_tasks()` in `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py` already debits launch budget, reconciles actual turns, and calls a post-task wiring hook.
- `attempt_remediation()` in `/config/workspace/IronClaude/src/superclaude/cli/pipeline/trailing_gate.py` already has the retry-once + budget-check state machine needed for gate remediation.
- `GateKPIReport` in `/config/workspace/IronClaude/src/superclaude/cli/sprint/kpi.py` aggregates generic gate/remediation metrics, but not gate-specific dimensions.
- `tests/pipeline/test_full_flow.py` already treats reimbursement semantics as part of the intended integration behavior.
- Important gap: `TurnLedger.reimbursement_rate` is **modeled but not consumed by current production code**. `credit()` accepts raw turns, and production reconciliation currently credits `pre_allocated - actual` directly, without applying `reimbursement_rate`.

Below are three proposals ranked by **spec-change minimality**.

---

## Rank 1 — Proposal A: Documentation-Only TurnLedger Overlay

### Summary
Keep v3.2 architecture almost entirely intact and make the spec explicitly state that wiring gate rollout modes are interpreted through TurnLedger reimbursement semantics. This is the smallest spec delta because it primarily updates rollout language, sprint integration language, and KPI requirements without changing the existing gate structure.

### Core idea
Treat `shadow`, `soft`, and `full` as **TurnLedger reimbursement profiles** for wiring-gate-triggered work:

- **Shadow** → `reimbursement_rate = 1.0`
  - Wiring analysis is observational only.
  - Any ledger debit associated with wiring-gate evaluation/remediation is fully reimbursed if the task itself remains non-blocked.
  - Net effect: zero-cost observation.
- **Soft** → `reimbursement_rate = 0.9`
  - Wiring findings surface warnings and may create deferred remediation records.
  - Most of the gate-related turn spend is returned, leaving a small visible cost signal.
- **Full** → `reimbursement_rate = 0.8`
  - Wiring failures are normal enforcement events.
  - Standard reimbursement economics apply.

### Remediation flow
Minimal integration statement:

1. Task completes in `execute_phase_tasks()`.
2. Post-task wiring hook emits/evaluates the wiring report.
3. On wiring-gate failure that is actionable in the current rollout tier, the sprint runner constructs a remediation step through `SprintGatePolicy`.
4. That remediation step is executed via `attempt_remediation()`.
5. `attempt_remediation()` uses `ledger.can_remediate()` before the first and second attempts, and `ledger.debit(turns_per_attempt)` for each attempt.
6. Reimbursement semantics are applied after the attempt result based on rollout tier:
   - shadow: reimburse 100%
   - soft: reimburse 90%
   - full: reimburse 80%

This keeps the existing retry-once state machine intact and simply declares how the wiring gate should map into it.

### KPI capture
Add wiring-gate-specific KPI requirements without redesigning `GateKPIReport`:

- Require `build_kpi_report()` inputs to include wiring gate results in the existing `gate_results` stream.
- Add a small extension to `GateKPIReport` for a gate-name breakdown, or at minimum require these wiring-specific counters:
  - `wiring_gates_evaluated`
  - `wiring_gates_failed`
  - `wiring_remediations_attempted`
  - `wiring_remediations_resolved`
  - `wiring_shadow_runs`
  - `wiring_soft_warnings`
  - `wiring_full_blocks`
- Record reimbursement economics for observability:
  - `wiring_turns_debited`
  - `wiring_turns_reimbursed`

### Required spec edits
This proposal needs the fewest edits:

1. **Section 4.5 Sprint Integration**
   - Add explicit text that the wiring gate is evaluated under TurnLedger and that rollout mode determines reimbursement behavior.
2. **Section 6.2 Configuration Contract**
   - Add a note that wiring-gate rollout must bind to a TurnLedger reimbursement profile.
3. **Section 8 Rollout Plan**
   - Add the shadow/soft/full reimbursement mapping table.
4. **Section 10 Success Criteria**
   - Add a success criterion that wiring rollout semantics are observable in TurnLedger accounting and KPI output.

### Why this ranks first
It changes the spec narrative, not the spec shape. No major new data models are required.

---

## Rank 2 — Proposal B: First-Class WiringGateLedgerPolicy in the Spec

### Summary
Introduce a small explicit policy object in the v3.2 spec so rollout semantics are no longer implied. This is still moderate in scope, but cleaner than Proposal A because it makes TurnLedger integration part of the release contract rather than commentary layered onto existing sections.

### Core idea
Add a new configuration/policy contract such as:

```python
@dataclass
class WiringGateLedgerPolicy:
    rollout_mode: Literal["shadow", "soft", "full"] = "shadow"
    reimbursement_rate: float = 1.0
    remediation_turns_per_attempt: int = 3
    deferred_in_soft_mode: bool = True
    blocking_in_full_mode: bool = True
```

Then specify the default rollout mapping:

- `shadow` → `reimbursement_rate = 1.0`
- `soft` → `reimbursement_rate = 0.9`
- `full` → `reimbursement_rate = 0.8`

This makes the dead `TurnLedger.reimbursement_rate` field immediately relevant to the v3.2 release story.

### Remediation flow
Specify a concrete lifecycle:

1. `execute_phase_tasks()` completes task execution and reconciles actual task turns.
2. Wiring hook evaluates the report.
3. If the wiring result is:
   - **shadow**: log only, no blocking, no mandatory remediation
   - **soft**: create warning + optional/deferred remediation entry
   - **full**: invoke `SprintGatePolicy.build_remediation_step()` immediately
4. Immediate remediation is executed via `attempt_remediation()` with:
   - pre-check: `ledger.can_remediate()`
   - debit per attempt
   - retry once on failure
5. After each remediation outcome, reimbursement is computed from the wiring gate ledger policy rate.
6. If remediation cannot start because budget is below `minimum_remediation_budget`, the failure is logged as budget-exhausted and surfaced in resume/HALT output.

This explicitly aligns wiring failures with the existing trailing gate remediation machinery instead of leaving `...` in the spec.

### KPI capture
Extend `GateKPIReport` from a generic report to a category-aware report. Suggested additions:

- `gate_family_counts: dict[str, int]`
- `gate_family_failures: dict[str, int]`
- `gate_family_latency_ms: dict[str, list[float]]`
- `reimbursement_turns_by_gate: dict[str, int]`
- `budget_exhausted_remediations_by_gate: dict[str, int]`

For wiring specifically, require KPI output for:

- wiring pass/fail count
- wiring remediation first-pass success rate
- wiring persistent failure count
- wiring budget-exhausted count
- wiring reimbursed-turn total by rollout tier

### Required spec edits
1. **Section 4.1 or 6.2**
   - Add `WiringGateLedgerPolicy` or equivalent contract.
2. **Section 4.5 Sprint Integration**
   - Replace the current mode pseudocode with TurnLedger-aware pseudocode.
3. **Section 6.1 Public API**
   - Optionally add policy/ledger parameters to wiring integration entry points.
4. **Section 8 Rollout Plan**
   - Define rollout tiers through reimbursement policy instead of prose only.
5. **Section 9 Testing Strategy**
   - Add tests that verify shadow/soft/full reimbursement accounting.
6. **Section 10 Success Criteria**
   - Add TurnLedger-native success criteria for reimbursement and budget-exhaustion handling.

### Why this ranks second
It is cleaner and more durable than Proposal A, but it adds a new first-class concept to the spec and therefore requires more edits.

---

## Rank 3 — Proposal C: TurnLedger as the Primary Rollout Authority

### Summary
Refactor the v3.2 spec so rollout is no longer described as `wiring_gate_mode` first. Instead, TurnLedger economics become the canonical control surface, and gate mode is derived from ledger policy. This is the most coherent long-term design, but it requires the most spec restructuring.

### Core idea
Define rollout in terms of a unified ledger-native gate profile:

```python
@dataclass
class GateRolloutBudgetProfile:
    gate_name: str
    reimbursement_rate: float
    blocking: bool
    warning_only: bool
    defer_remediation: bool
```

For wiring gate:

- profile `shadow`:
  - `reimbursement_rate = 1.0`
  - `blocking = False`
  - `warning_only = False`
  - `defer_remediation = True`
- profile `soft`:
  - `reimbursement_rate = 0.9`
  - `blocking = False`
  - `warning_only = True`
  - `defer_remediation = True`
- profile `full`:
  - `reimbursement_rate = 0.8`
  - `blocking = True`
  - `warning_only = False`
  - `defer_remediation = False`

Under this proposal, `wiring_gate_mode` becomes either:
- derived from the reimbursement profile, or
- removed from the public v3.2 configuration contract in favor of a gate rollout profile.

### Remediation flow
This proposal gives the most explicit end-to-end budget semantics:

1. Task launch and reconciliation stay in `execute_phase_tasks()`.
2. Wiring evaluation produces a `TrailingGateResult`-compatible outcome with gate family `wiring-verification`.
3. The active `GateRolloutBudgetProfile` determines whether the result is observation-only, warning-only, deferred remediation, or immediate blocking remediation.
4. Immediate remediation always flows through `attempt_remediation()`.
5. `attempt_remediation()` debits each attempt using TurnLedger.
6. On successful remediation, reimbursement is computed from the active profile rate.
7. On persistent failure, no reimbursement is applied.
8. On budget exhaustion, the profile emits a budget-governed HALT or deferred remediation record, depending on rollout profile.

This proposal also lets the spec state plainly that rollout progression is a **budget-governed behavioral contract**, not just a UI mode switch.

### KPI capture
Make `GateKPIReport` profile-aware. Require per-gate and per-rollout metrics:

- `gates_by_profile` (`shadow`, `soft`, `full`)
- `wiring_findings_by_type` (`unwired_callable`, `orphan_module`, `unwired_registry`)
- `wiring_budget_exhausted_events`
- `wiring_deferred_remediations`
- `wiring_immediate_remediations`
- `wiring_reimbursement_rate_observed`
- `wiring_turns_debited`
- `wiring_turns_reimbursed`
- `wiring_net_turn_cost`

This gives a direct way to verify that shadow was truly zero-net-cost, soft was low-cost, and full used standard economics.

### Required spec edits
1. **Section 3 Architecture**
   - Update the system context and data flow to show TurnLedger as a first-class runtime dependency.
2. **Section 4.1 Data Models**
   - Add a rollout budget profile data model.
3. **Section 4.5 Sprint Integration**
   - Replace `wiring_gate_mode` pseudocode with ledger-native control flow.
4. **Section 6.2 Configuration Contract**
   - Replace or subordinate `wiring_gate_mode` under profile-based configuration.
5. **Section 6.3 Gate Contract**
   - Add frontmatter or metadata requirements for rollout profile / reimbursement observability.
6. **Section 8 Rollout Plan**
   - Reframe the entire rollout section around TurnLedger-native profiles.
7. **Section 9 Testing Strategy**
   - Add integration tests for profile-driven reimbursement, budget exhaustion, and KPI reporting.
8. **Section 11 Dependency Map**
   - Show `sprint/models.py` and `sprint/kpi.py` as direct design dependencies.

### Why this ranks third
It produces the strongest long-term architecture, but it is no longer a light-touch adaptation of the current v3.2 spec. It meaningfully reshapes the release contract.

---

## Recommendation

**Recommended choice: Proposal A** if the immediate objective is to make v3.2 clearly TurnLedger-native with the fewest spec edits.

Why:

- It preserves the current release structure.
- It directly resolves the spec blind spot around rollout economics.
- It gives a clean bridge from current sprint/trailing-gate behavior to future production wiring of `reimbursement_rate`.
- It avoids overcommitting v3.2 to a larger configuration redesign.

**Recommended choice: Proposal B** if the goal is still v3.2 delivery, but with a stronger explicit contract that prevents future ambiguity.

---

## Minimal spec patch checklist

If choosing the smallest viable TurnLedger-native update, the spec should explicitly add these statements:

1. **Rollout semantics**
   - Shadow = reimbursement rate 1.0, observation only, zero net turn cost.
   - Soft = reimbursement rate 0.9, warning-oriented, low net turn cost.
   - Full = reimbursement rate 0.8, standard enforcement cost.

2. **Remediation semantics**
   - Wiring failures that enter remediation must flow through `attempt_remediation()`.
   - Remediation must honor `ledger.can_remediate()` and `minimum_remediation_budget`.
   - Persistent failure consumes debited turns with no reimbursement.

3. **KPI semantics**
   - KPI reporting must expose wiring-gate counts, remediation outcomes, budget exhaustion, and reimbursed turns.

4. **Known implementation gap**
   - The spec should note that `TurnLedger.reimbursement_rate` exists today but is not yet consumed by production accounting, so v3.2 implementation must either wire it or explicitly compute equivalent reimbursement behavior at the integration layer.
