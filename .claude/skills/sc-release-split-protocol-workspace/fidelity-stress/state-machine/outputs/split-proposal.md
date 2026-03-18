---
type: split-proposal
source: fidelity-stress-state-machine.md
depth: deep
phase: discovery
---

# Split Proposal — Pipeline State Machine v2.0

## Discovery Analysis

### Dependency Chain Analysis

The spec defines a tightly coupled state machine system. Every major component references and depends on other components:

1. **State Machine Definition (§2)** is the foundation — everything else builds on it
2. **Error Handling (§3)** directly references transition guards and invariants from §2 (e.g., retry backoff formula `min(2^retry_count * 500, 30000)` is a guard condition in the GATING → RUNNING transition)
3. **Event System (§4)** is a side effect of every transition — the `StateTransitionEvent` schema references `from_state`, `to_state`, `guard_conditions_evaluated` which are defined in §2
4. **Concurrency Model (§5)** defines guards referenced by §2 transitions (e.g., `active_task_count(phase) < phase.concurrency_limit` is a guard on QUEUED → RUNNING)
5. **Observability (§6)** depends on §4 events and §5 lock semantics
6. **Circuit Breaker (§3.3)** modifies phase transition behavior (triggers RUNNING → FAILED regardless of max_failures)
7. **Migration (§7)** maps v1.0 boolean flags to §2 states — requires the state definitions to be stable
8. **Testing (§8)** validates invariants from §2 and incidents that span §2+§3+§5
9. **NFRs (§9)** apply to transitions (§2), audit trail (§4), events (§4), and locks (§5)

### Potential Split Seams Evaluated

**Seam A: Core State Machine (§2+§3+§5) vs. Operational Infrastructure (§4+§6+§7)**
- Problem: §4 (Event System) is a SIDE EFFECT defined inline in §2's transition tables. Every transition row specifies its emitted event. Splitting events from transitions would require duplicating the transition tables or creating forward references that break self-containment.
- Problem: §5 (Concurrency) provides guard conditions used IN the transition table (§2.2, QUEUED → RUNNING). These are not separable.
- Verdict: This seam is artificial. It would split coupled components.

**Seam B: State Machine + Events + Concurrency + Circuit Breaker (R1) vs. Migration + Observability + Full Testing (R2)**
- Problem: Migration (§7) maps v1.0 flags to v2.0 states. This mapping is only meaningful if the states are implemented. Deferring migration means shipping a state machine that can't be deployed (no migration path from v1.0).
- Problem: Observability (§6) metrics like `sm.invariant.violation` are part of the invariant enforcement system. Without metrics, invariant violations go unobserved — defeating the purpose of the state machine (which exists precisely because implicit state management caused production incidents).
- Problem: Testing (§8) includes incident regression tests for INC-041, INC-047, INC-052. These are the MOTIVATING INCIDENTS for the entire spec. Shipping without regression tests means shipping without proof the state machine solves the problems it was built for.
- Verdict: This seam creates a misleading intermediate state — a state machine that can't be deployed, can't be observed, and can't prove it fixes the incidents.

**Seam C: Schema/Definition Only (R1) vs. Full Implementation (R2)**
- This would mean R1 defines states, transitions, invariants on paper; R2 implements them.
- Problem: A "schema only" release delivers zero value. The spec already IS the schema — implementing it as code IS the deliverable. There is no intermediate "schema hardening" step that provides standalone value.
- Verdict: No value in Release 1.

**Seam D: Single-Scope Implementation (Task only in R1) vs. Phase + Pipeline Scopes (R2)**
- The three scopes (task, phase, pipeline) have cross-scope dependencies:
  - Task RUNNING → FAILED increments `phase.failure_count` (§2.2)
  - Phase RUNNING depends on `pipeline.state == RUNNING` (§2.3)
  - Circuit breaker (task-level failures) triggers phase-level transition (§3.3)
  - Pipeline emergency stop kills active tasks (§2.4)
- Problem: Implementing task scope alone without phase scope means `phase.failure_count` has no destination, circuit breaker can't trigger phase transitions, and the concurrency model (which is per-phase) has no phase to govern it.
- Verdict: Cross-scope dependencies make this seam impractical without significant rework.

### Cost of Splitting

1. **Integration overhead**: Each split release needs its own migration gate (§7.2 requires 50 pipeline runs with zero divergence). Running this gate twice doubles validation time.
2. **Context switching**: The spec is a single coherent state machine. Developers switching between "R1 state machine" and "R2 state machine" would need to hold the full mental model anyway.
3. **Rework risk**: If R1 ships a partial state machine, R2 may discover that R1's transitions need modification to support phase/pipeline scope. This means rework in R1 code during R2 development.
4. **Misleading intermediate state**: A partial state machine creates a false sense of "state management is solved" when the hard parts (cross-scope coordination, circuit breaker, emergency stop) are deferred.

### Cost of NOT Splitting

1. **Big-bang risk**: The spec is 1200-1600 LOC production code. This is substantial but not extreme.
2. **Delayed feedback**: Feedback on the state machine design comes only after all 10 files are implemented.
3. **Root-cause isolation**: If the state machine has design flaws, they may be harder to isolate in a full implementation.

### Mitigation Without Splitting

These risks can be mitigated within a single release:
- **Staged implementation**: Implement task scope first, then phase, then pipeline — within the same release branch, with incremental testing at each stage.
- **Shadow mode (§7.2 Phase 1)**: The spec already includes a staged deployment strategy. Phase 1 (shadow mode) provides real-world validation before the state machine drives behavior.
- **Property tests (§8.1)**: Hypothesis-based property tests provide strong design validation without splitting.
- **Incident regression tests (§8.2)**: These prove the design prevents known incidents, providing confidence before full deployment.

## Recommendation: DO NOT SPLIT

**Confidence: 0.88**

This release spec describes a tightly coupled state machine where every component has direct dependencies on multiple other components. The dependency chains are not linear — they form a dense graph:

- Transition guards reference concurrency limits (§5 → §2)
- Transition side effects reference events (§4 → §2)
- Error handling modifies transitions (§3 → §2)
- Circuit breaker triggers phase transitions (§3.3 → §2.3)
- Invariants span scopes (INV-T1 references locks from §5)
- Migration requires all states defined (§7 → §2)
- Testing validates invariants across all scopes (§8 → §2+§3+§5)
- NFRs apply to transitions, events, and locks (§9 → §2+§4+§5)

No natural seam exists where Release 1 would deliver independently testable, independently valuable functionality that Release 2 builds on. Every candidate split point either (a) cuts through coupled components, (b) defers the validation that proves the system works, or (c) creates a misleading intermediate state.

The spec already includes its own staged deployment strategy (shadow → soft → full) which provides the early feedback benefits that splitting would otherwise offer.

### Risks of No Split and Mitigations

| Risk | Mitigation |
|------|-----------|
| Large implementation scope (1200-1600 LOC) | Staged internal implementation: task → phase → pipeline. Property tests at each stage. |
| Design flaws discovered late | Shadow mode deployment (§7.2 Phase 1) validates design with zero production risk |
| Incident regression not proven early | INC-041/047/052 regression tests (§8.2) are implemented alongside the state machine, not after |
| Integration complexity | File manifest (§10) is well-partitioned: state_machine.py, events.py, locks.py, circuit_breaker.py |

### Alternative Strategies for Early Validation

1. **Internal milestone gates**: Task scope implementation + property tests → Phase scope + cross-scope tests → Pipeline scope + integration tests → Migration + shadow mode
2. **Design review gate**: Before any code, review the transition tables and invariants with a walkthrough of INC-041/047/052 scenarios
3. **Shadow mode as validation**: §7.2 Phase 1 IS the early validation strategy — the state machine runs alongside v1.0 and logs divergences without affecting behavior
