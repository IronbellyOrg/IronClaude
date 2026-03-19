---
type: split-proposal-final
source: fidelity-stress-state-machine.md
depth: deep
verdict: no-split
adversarial:
  agents: [opus:architect, haiku:analyzer]
  convergence_score: 0.92
  base_variant: opus:architect
  artifacts_dir: null
  unresolved_conflicts: 0
  fallback_mode: true
---

# Adversarial Review — Release Split Proposal

## Original Proposal Summary

The Part 1 discovery analysis evaluated 4 candidate split seams for the Pipeline State Machine v2.0 spec and found none viable. The spec describes a tightly coupled state machine across 3 scopes (task, phase, pipeline) with dense cross-component dependencies: transition guards reference concurrency limits, side effects reference events, error handling modifies transitions, circuit breakers trigger phase transitions, and invariants span scopes. The recommendation was DO NOT SPLIT with 0.88 confidence.

## Advocate Position (Arguing FOR No-Split)

The advocate for keeping the release intact presents these arguments:

1. **Dense dependency graph prevents clean separation.** The transition table in §2.2 directly embeds references to:
   - `phase.concurrency_limit` (defined in §5.1) as a guard on QUEUED → RUNNING
   - `phase.failure_count` (defined in §2.3 invariant INV-P2) as a side effect of RUNNING → FAILED
   - Event emissions (defined in §4.1) as side effects on every transition
   - Lock acquisition (defined in §5.3) as a side effect of QUEUED → RUNNING
   - Gate retry backoff `min(2^retry_count * 500, 30000)` (§3.1) as part of GATING → RUNNING

   These are not loose couplings — they are inline references within the same transition rows. Splitting them requires either duplicating the transition table or creating incomplete tables with forward references.

2. **The spec already contains its own staged deployment.** §7.2 defines a 3-phase migration (shadow → soft → full) with a quantitative gate: "Phase 2 activation requires zero state divergences between v1.0 and v2.0 for a minimum of 50 pipeline runs." This IS the early validation strategy. Splitting the release would add a release boundary on top of a deployment boundary, doubling coordination overhead for no additional validation power.

3. **Incident regression tests validate the entire design.** The three motivating incidents (INC-041, INC-047, INC-052) each span multiple components:
   - INC-041 (out-of-order phases): Requires phase transition guards (§2.3) + INV-P1
   - INC-047 (skipped gate): Requires task transition guards (§2.2) + INV-T3 + gate enforcement tiers
   - INC-052 (infinite retry): Requires retry semantics (§3.1) + circuit breaker (§3.3) + INV-T6

   These tests cannot be meaningfully run against a partial implementation.

4. **The file manifest is already well-partitioned.** §10 defines 10 files with clear single-responsibility boundaries: `state_machine.py`, `events.py`, `locks.py`, `circuit_breaker.py`, etc. This partitioning enables staged internal development without requiring a release boundary.

## Skeptic Position (Arguing AGAINST No-Split)

The skeptic challenges the no-split recommendation:

1. **Is "tightly coupled" overstated?** The event system (§4) and observability (§6) are consumers of state machine data, not producers. They could theoretically be implemented as separate concerns with a defined interface. If the state machine core (§2+§3+§5) were Release 1 and the event/observability/migration layers (§4+§6+§7) were Release 2, the core could be tested without full event infrastructure.

   **Counter**: The event emissions are SIDE EFFECTS defined in the transition table itself. Every transition row in §2.2 specifies "Emit `task.queued` event" or similar. The event system isn't just a consumer — it's an integral part of the transition contract. Removing events from transitions means changing the transition definitions, not just deferring a downstream consumer. Furthermore, the audit trail (§4.3) is part of the invariant enforcement system — rejected transitions "MUST be logged at WARNING level." Without the audit trail, invariant violations are silently swallowed, which contradicts the spec's core purpose.

2. **Could task scope alone be valuable?** Task-level state management with guards and invariants would prevent INC-047 (gate bypass) even without phase/pipeline scope.

   **Counter**: Task transitions reference phase-level state (`phase.state == RUNNING` is a guard on PENDING → QUEUED; `phase.concurrency_limit` is a guard on QUEUED → RUNNING). A task-scope-only implementation would need stub values for phase state, defeating the purpose of formal state management. Additionally, INC-041 (out-of-order phases) is a phase-scope problem — task-scope alone doesn't address it.

3. **Is 1200-1600 LOC too much for a single release?** This is a substantial implementation. Could the risk of a large release be underestimated?

   **Counter**: 1200-1600 LOC across 10 files averages 120-160 LOC per file. The largest file (`state_machine.py` at 400-500 LOC) is a data-driven transition table — complex but not algorithmically novel. The shadow mode deployment (§7.2) provides a safety net that splitting does not: the old system continues to drive behavior while the new system logs divergences. This is stronger validation than any release split could provide.

4. **Is "keep it together" risk avoidance?** Perhaps the real risk is a monolithic deployment where everything must work or nothing works.

   **Counter**: The shadow mode deployment IS the answer to this. Phase 1 runs both systems in parallel. Phase 2 switches primary but keeps v1.0 for backward compatibility. Phase 3 removes v1.0 only after proven. This is a 3-phase graduated rollout within a single release — more granular than any 2-release split.

## Pragmatist Assessment

1. **Does any split enable real-world tests that couldn't happen without shipping?** No. The shadow mode deployment (§7.2 Phase 1) enables real-world validation of the state machine against actual pipeline runs without splitting the release. The "50 pipeline runs with zero divergence" gate is a concrete, measurable validation that doesn't require a release boundary.

2. **Is the overhead of two releases justified by feedback velocity?** No. The feedback from a split would be: "Task-scope state machine works in isolation." This is less valuable than the feedback from shadow mode: "Full state machine agrees with production system across 50 real pipeline runs." The shadow mode feedback is strictly more informative.

3. **Are there hidden coupling risks?** No hidden risks — the coupling is EXPLICIT. The spec openly defines cross-scope references in its transition tables. There's no surprise coupling to discover during R2.

4. **Blast radius if the no-split decision is wrong?** Low. If the full implementation reveals design problems:
   - Shadow mode (Phase 1) catches divergences before the state machine drives behavior
   - The 50-run validation gate prevents premature activation
   - Phase 2 keeps v1.0 for backward compatibility
   - Phase 3 only removes v1.0 after extended validation

5. **Reversibility?** Not applicable — there's nothing to reverse. But if the team later decides to implement in stages, the file manifest (§10) already supports staged development within a single branch.

## Key Contested Points

| Point | Advocate (No-Split) | Skeptic (Split) | Pragmatist | Resolution |
|-------|---------------------|-----------------|------------|------------|
| Event system separability | Events are inline side effects in transition table | Events could be a downstream consumer | Events are contractual — removing them changes transition semantics | NO SPLIT — events are integral |
| Task-scope standalone value | Task guards reference phase state | INC-047 is task-scope only | Task scope alone needs phase stubs, defeating purpose | NO SPLIT — task scope is not independent |
| Implementation risk (1200-1600 LOC) | Shadow mode mitigates deployment risk | Large scope increases development risk | 10 well-partitioned files + shadow mode = manageable risk | NO SPLIT — risk is manageable |
| Early feedback mechanism | Shadow mode provides real-world feedback | Split provides earlier partial feedback | Shadow mode feedback is strictly more informative | NO SPLIT — shadow mode is superior |

## Verdict: DON'T SPLIT

### Decision Rationale

The Pipeline State Machine v2.0 spec is a single coherent system with dense cross-component dependencies that prevent meaningful decomposition. Every candidate split seam cuts through coupled components, defers critical validation, or creates a misleading intermediate state. The spec already includes a superior validation strategy (shadow → soft → full migration with a 50-run zero-divergence gate) that provides more informative real-world feedback than any release split could offer.

### Strongest Argument For (No-Split)

The shadow mode deployment strategy (§7.2) is strictly superior to splitting for risk mitigation: it validates the COMPLETE state machine against REAL pipeline behavior without requiring the new system to drive production until proven. A split would provide weaker feedback ("partial system works in isolation") at higher coordination cost.

### Strongest Argument Against (No-Split)

The implementation scope (1200-1600 LOC, 10 files) is substantial. If the state machine design has a fundamental flaw in cross-scope coordination (e.g., the circuit breaker interaction with phase transitions in §3.3), that flaw won't surface until late in implementation when all scopes are integrated.

**What would change the decision**: If the spec's cross-scope dependencies were weaker — e.g., if task, phase, and pipeline scopes had well-defined interfaces rather than inline cross-references — a scope-based split would become viable.

### Remaining Risks

1. **Design flaw in cross-scope coordination**: The circuit breaker (§3.3) triggers phase transitions from task-level events. If this interaction has edge cases not covered by the invariants, they'll surface during integration.
2. **Migration complexity**: The v1.0 → v2.0 mapping (§7.1) includes an ambiguous case (`is_running=True, has_error=True` → `RUNNING`). Shadow mode testing may reveal this mapping is insufficient.
3. **Performance under concurrency**: NFRs (§9) require p99 < 5ms transition latency. Lock contention under concurrent task execution may challenge this.

### Confidence-Increasing Evidence

- A design walkthrough of INC-041/047/052 scenarios against the transition tables, confirming the guards prevent each incident
- A prototype of the circuit breaker's interaction with phase transitions, validating the SKIPPED-transparency semantics (§3.3)
- A lock contention analysis under max concurrency (10 tasks per phase) against the 5ms p99 requirement

> **Warning**: Adversarial result produced via fallback path (not primary Skill invocation).
> Quality may be reduced. Review the merged output manually before proceeding.
