

---
convergence_score: 0.78
rounds_completed: 3
---

# Adversarial Debate: Opus Architect vs Haiku Architect Roadmaps

## Round 1: Initial Positions on Divergence Points

### Variant A (Opus Architect)

**On G-012 Phase Placement (D-01):** Smoke Test Gate G-012 belongs in Phase 1 alongside Silent Success and D-03/D-04. All three behavioral gates share a common validation contract — they detect false-positive execution outcomes. Building them together enables cross-gate unit testing from day one. Deferring G-012 to Phase 2 means you cannot validate the full gate trio until integration is already underway, which is precisely when you want confidence in your foundation, not questions about it.

**On TUI Placement (D-02):** TUI must wait until Phase 3. The operator experience depends on knowing the actual shape of `AuditWorkflowState`, which won't stabilize until integration is complete. Building TUI in Phase 2 while the state machine is still being wired invites rework. Integration learnings should inform operator guidance — not the other way around.

**On Timeline Granularity (D-03):** Day-level estimates enable sprint-level planning. A 0.92-complexity program needs tighter tracking, not looser. Week-level ranges (e.g., "3-4 weeks") hide a 33% variance that makes resource allocation impossible. Day ranges force honest decomposition.

**On Module Placement (D-04):** Explicit file-level guidance eliminates ambiguity. `silent_success.py` under `cli/pipeline/` because it's a cross-cutting concern. `smoke_gate.py` under `cli/cli_portify/` because it tests portify execution. `fidelity_inventory.py` under `cli/roadmap/`. Leaving this to implementers invites inconsistency.

**On Shadow Window (D-07):** Two weeks minimum, non-negotiable. With provisional thresholds throughout the system, skipping or shortening the shadow window produces immediate false-positive cascades. Schedule pressure is precisely the condition under which shadow observation is most valuable.

### Variant B (Haiku Architect)

**On G-012 Phase Placement (D-01):** G-012 is fundamentally an integration gate — it tests whether a real executor run produces expected artifacts. Building it in Phase 1, before the lease model and executor wiring exist, means you're building a gate that cannot exercise its actual runtime path. You'll write the gate, then rewrite its integration surface in Phase 2. Coupling G-012 with its infrastructure in Phase 2 reduces total engineering effort and produces a gate that's tested against its real integration points from the start.

**On TUI Placement (D-02):** TUI in Phase 2 enables operator feedback during the most architecturally active phase. If integration surfaces unexpected state shapes, operators can flag usability problems while the state machine is still malleable. Waiting until Phase 3 means any TUI-driven state model feedback requires reopening integration work.

**On Timeline Granularity (D-03):** Day-level precision for a 10-16 week program is false precision. At 0.92 complexity with cross-cutting integration, the dominant schedule risks are blocker ownership latency, calibration window length, and C3 resolution — none of which respond to day-level planning. Week-level estimates with named schedule drivers give stakeholders honest uncertainty bounds. Day-level estimates will be wrong and will erode trust when they slip.

**On Module Placement (D-04):** Prescribing file paths in a roadmap conflates architectural guidance with implementation detail. The roadmap should specify module responsibilities and integration contracts. File placement is an implementation decision that belongs in sprint planning, where the team can account for current directory structure and naming conventions.

**On Shadow Window (D-07):** A hard 2-week minimum is an arbitrary constraint. The Reliability Owner should determine the observation window based on traffic volume, gate invocation frequency, and threshold confidence intervals. Some deployments may need 3 weeks; others may reach statistical significance in 10 days. Prescribing a floor without data is the kind of premature constraint that creates schedule conflicts without improving safety.

---

## Round 2: Rebuttals

### Variant A (Opus) Rebuts Variant B (Haiku)

**On G-012 deferral:** Haiku argues G-012 needs its "real runtime path" — but that conflates unit testing with integration testing. In Phase 1, G-012 can be fully unit-tested against fixture inputs: does it detect timing anomalies? Does it flag artifact absence? Does it route content evidence failures correctly? These are self-contained behaviors. The integration surface (how it's invoked by the executor) is Phase 2 work regardless. Building the gate logic early means Phase 2 focuses purely on wiring, not on gate logic AND wiring simultaneously.

**On TUI in Phase 2:** "Operator feedback during the most architecturally active phase" sounds valuable until you consider the cost. Phase 2 is when lease models, retry budgets, and executor wiring are being built. Adding TUI development to this phase splits engineering attention across the most complex integration work AND a user-facing surface. If the state model changes — which Haiku acknowledges is likely — the TUI rework compounds Phase 2's already-high risk. The feedback loop Haiku wants can be achieved with log output during integration; formal TUI can wait.

**On timeline precision:** Haiku's "named schedule drivers" are valuable — I concede that. But "1-2 weeks" for Phase 0 is a 100% variance range. That's not honest uncertainty; that's not having decomposed the work. Day ranges force you to identify what actually takes the time. The right answer is day ranges within phases with explicit schedule-driver callouts at the program level — which is what a merged document should contain.

**On module placement:** "Implementation detail" is exactly what a roadmap for a 0.92-complexity program must provide. The team implementing this will face dozens of placement decisions. A roadmap that says "the team can account for current directory structure" is a roadmap that produces inconsistent placement and a follow-up refactor. Guidance is not a mandate — it's a recommendation that prevents the most common mistake.

### Variant B (Haiku) Rebuts Variant A (Opus)

**On G-012 in Phase 1:** Opus's unit-testing argument is valid for the check logic itself, but misses the key risk: interface assumptions. If G-012 is built in Phase 1 against assumed interfaces, and Phase 2 integration reveals those interfaces need adjustment, you've created rework. The total effort is higher, not lower. Phase 2 builds G-012 against real interfaces, producing a gate that's tested end-to-end on first pass. The unit tests Opus wants can still be written — they just run against the actual integration contract.

**On TUI timing:** Opus argues Phase 2 is too complex to add TUI. But TUI work is largely independent of lease/retry implementation — it reads `AuditWorkflowState`, which is defined in Phase 1's data model work. The TUI engineer doesn't need to understand lease internals; they need the state enum and its transitions. Parallel workstreams within Phase 2 are feasible if the team is larger than one person.

**On timeline:** Opus concedes that named schedule drivers are valuable, which is the core of my position. Day-range decomposition is appropriate for sprint planning within phases — not for a program-level roadmap. A roadmap that says "Phase 1: 10-14 days" will be treated as a commitment by stakeholders, and when it slips to 18 days because of a C3 ambiguity, the roadmap loses credibility. "2-3 weeks with C3 resolution as primary schedule driver" sets correct expectations.

**On module placement:** If placement guidance is valuable, it belongs in an architecture decision record or a Phase 1 design document — not embedded in the roadmap. Mixing implementation specifics into the roadmap makes the roadmap harder to maintain and review. The roadmap should be stable across minor implementation decisions.

**On shadow window:** Opus's "non-negotiable 2 weeks" is a policy decision masquerading as an architectural constraint. What if the system processes 1000 gate evaluations per day and reaches statistical significance in 5 days? What if it processes 10 per day and needs 4 weeks? The Reliability Owner exists precisely to make this call with data. Hardcoding a floor substitutes judgment for evidence — the opposite of what an evidence-based audit system should do.

---

## Round 3: Concessions and Remaining Disagreements

### Variant A (Opus) — Concessions

1. **Timeline granularity:** I concede that week-level estimates with named schedule drivers are more appropriate for program-level communication. Day-level decomposition should appear in sprint planning, not the roadmap. A merged document should use week ranges at the program level with schedule driver callouts, and reserve day-level estimates for phase-internal sprint planning.

2. **Shadow window:** I concede that a hard 2-week floor is prescriptive without data. However, I maintain that the roadmap must require a *minimum observation threshold* — whether expressed as a time floor or a minimum gate-evaluation count. "Reliability Owner discretion" without any guardrail risks a 3-day shadow window under delivery pressure. The merged document should state: "minimum observation window determined by Reliability Owner, with a provisional floor of 2 weeks pending calibration data."

3. **Sequencing guardrails:** Haiku's standalone guardrails are cleaner than my embedded checklists for program-level enforcement. I concede this format is superior for the four critical sequencing rules.

### Variant A (Opus) — Remaining Disagreements

1. **G-012 must be Phase 1.** The unit-testable gate logic is substantial (~400 lines) and has zero dependency on integration interfaces. Building it early de-risks Phase 2 by reducing its scope. The "interface assumption" risk Haiku raises is mitigated by the fact that gate inputs are defined by `AuditGateResult`, which is Phase 1 work.

2. **TUI must be Phase 3.** Even with parallel workstreams, TUI in Phase 2 adds coordination overhead to the highest-risk phase. The downside of waiting (delayed operator feedback) is smaller than the downside of rework (TUI changes driven by integration discoveries).

3. **Module placement belongs in the roadmap.** For a 0.92-complexity program, reducing ambiguity at every level is worth the maintenance cost. An ADR is fine too, but the roadmap is the document the team will actually read.

### Variant B (Haiku) — Concessions

1. **File manifest:** I concede that Opus's enumeration of 7 source files and 7 test files with line estimates is immediately actionable for sprint planning. My roadmap should include a comparable manifest, even if file paths are treated as recommendations rather than mandates.

2. **Requirement traceability:** Opus's FR/NFR/SC inline codes make audit and compliance straightforward. My concern-based grouping is better for test strategy, but the merged document needs both: inline traceability for individual sections AND concern-based grouping in the validation strategy.

3. **Shadow window floor:** I concede that pure Reliability Owner discretion without any guardrail is insufficient. A provisional floor with an explicit override mechanism (Reliability Owner can shorten with documented justification) is a reasonable compromise.

### Variant B (Haiku) — Remaining Disagreements

1. **G-012 belongs in Phase 2.** The gate's value is in integration testing, not unit testing. A 400-line module built against assumed interfaces that needs re-wiring in Phase 2 is not "de-risking" — it's front-loading work that will be partially invalidated. The total cost is lower when built against real interfaces.

2. **TUI in Phase 2 is feasible and valuable.** The TUI reads a state enum, not lease internals. If the team cannot parallelize TUI work with integration work, that's a resourcing problem, not an architectural one. Early operator feedback is worth the coordination cost.

3. **Module placement does not belong in the roadmap.** The roadmap is a living document reviewed by stakeholders beyond the implementation team. Implementation-specific file paths reduce readability for non-engineers and create false change signals when paths are adjusted during implementation.

---

## Convergence Assessment

### Areas of Agreement (Strong Convergence)

1. **Phase structure**: Both agree on 5 phases (P0-P4) with Foundation → Integration → Rollout progression.
2. **P0 prerequisites**: Identical defect fixes, dead code retirement, and canonical term definitions.
3. **Silent Success Detector**: Same signals, formula, bands, and Phase 1 placement.
4. **D-03/D-04 fidelity checks**: Same logic, same phase, same deterministic override rule.
5. **Lease model**: Same fields, same heartbeat formula, same timeout behavior.
6. **Rollout sequence**: Shadow → Soft → Full with KPI gates.
7. **Override rules**: Hard-fail never overridable at release scope.
8. **Timeline approach** (after concessions): Week-level program estimates with named schedule drivers; day-level reserved for sprint planning.
9. **File manifest value**: Both agree an enumerated file list aids sprint planning.
10. **Traceability + validation grouping**: Both needed in the merged document.

### Areas of Partial Convergence

1. **Shadow window**: Provisional 2-week floor, Reliability Owner can override with documented justification. (~85% converged)
2. **Sequencing guardrails**: Standalone rules preferred, supplemented by per-phase checklists. (~90% converged)
3. **Risk treatment**: Merge Opus's owner-assignment column with Haiku's governance-risk category. (~80% converged)

### Remaining Disputes (Require Stakeholder Decision)

1. **G-012 phase placement**: Phase 1 (Opus) vs Phase 2 (Haiku). Core disagreement on whether unit-testable gate logic should be built before or alongside its integration surface. **Recommend: Architect decides based on team size.** Single implementer → Phase 2 (Haiku). Multiple implementers → Phase 1 with integration wiring in Phase 2 (Opus).

2. **TUI placement**: Phase 3 (Opus) vs Phase 2 (Haiku). Core disagreement on whether operator feedback during integration outweighs coordination cost. **Recommend: If a dedicated TUI engineer exists, Phase 2. Otherwise, Phase 3.**

3. **Module placement in roadmap**: Include (Opus) vs defer to ADR (Haiku). **Recommend: Include as "Architect Recommendation" appendix, clearly marked as guidance not mandate.** This preserves readability for non-engineer stakeholders while providing actionable guidance.
