# Round 1 — ARCHITECT Judge (Panel Mode)

**Lens:** systems architecture & sequencing soundness — phase ordering, the reuse thesis,
the MCP/HTTP boundary as permanent architecture, flagship readiness, buildability.
**Stance:** panel judge. I score both variants; I do not advocate. Source line citations are
taken on trust from V2 (the analyzer judge verifies them).

---

## Steelman V1 (HYBRID — conditional go via strangler-fig)

The strongest version of V1's position:

The codebase was *designed* for runtime substitution, and that is an architectural fact, not
a hope. `pipeline/executor.py` runs against an injected `StepRunner` Protocol; the domain mass
(gates, convergence, FMEA, audit, spec_parser, models, ~62K LOC) carries only `TYPE_CHECKING`
imports — it is genuinely runtime-agnostic. That means the *shape* of the migration is a seam
swap, and seam swaps are the lowest-risk class of large-system change. V1's deepest architectural
virtue is the **strangler-fig with a live benchmark**: the existing CLI stays fully operational
as oracle and rollback throughout, so every phase is independently reversible and the blast
radius of any single step is bounded. That is textbook-correct migration architecture.

V1 is also the only variant that is *buildable as written*. It carries the executable scaffolding:
a 5-phase roadmap with effort sizing, explicit dependencies, and per-phase rollback paths
(U-001); a file-by-file Component Port Matrix with reuse/adapt/rewrite/drop dispositions across
~20 modules (U-002); a "what is lost" severity table; and an explicit "what would have to be
true" continuation frame (a-f). A reviewer can pick this up and start. V1 also already names —
not buries — the five hardest unknowns as gates, and explicitly self-corrects its own base
("sprint is *not* substitution-clean... must be sized very-high"), which is intellectually honest
and means V1 does not actually believe its own "tiny seam" headline applies to sprint.

Crucially, V1's posture is **conditional**, gated on a Phase-0 spike that has not run. Read
charitably, "HYBRID conditional go" and "DEFER until Phase 0 passes" are close to the same
operational instruction: do the cheap spike before committing. V1 simply frames the spike as
Phase 0 of the plan rather than as a precondition to having a plan.

## Steelman V2 (DEFER — buy down unknowns before committing to a roadmap)

The strongest version of V2's position:

V2's central insight is an architectural decomposition that V1 blurs: the project is really
*three* projects with different risk profiles — (a) swap the Claude subprocess seam, (b)
service-ify orchestration behind MCP/HTTP, (c) deliver paid-or-DIY multi-tenant RBAC. Only (a)
has strong source support. V1's single recommendation averages across all three; V2 refuses to,
and that refusal is sound systems thinking — you do not buy a roadmap whose strategic payoff
(c) rests on an *unverified commercial* gate.

V2's flagship-order correction is the sharpest architectural point on the board. V1 sequences
**sprint first** while conceding sprint's seam is a private `_subprocess_factory` test hook, not
a Protocol — i.e., V1 leads with its *least* substitution-clean target. V2 reorders to
**pipeline (verified-clean Protocol) → roadmap (partially factory-wrapped) → sprint (last,
gated on telemetry reconstruction)**. That is monotonic in seam cleanliness and de-risking
order: prove the abstraction on the surface that was actually built for it, accumulate the
event-adapter and MCP-contract learnings, then attempt the hard one last. This is correct
sequencing and V1 is internally contradictory not to have done it.

V2's `roadmap` correction (X-004) is load-bearing: roadmap is **PARTIAL**, not uniformly
factory-wrapped — ordinary steps instantiate `ClaudeProcess` directly at 1107; only the
semantic-layer path (1358) is wrapped. V1's "easier flagship" claim overstates readiness.

V2's EE-gate relocation (X-007) is the deepest sequencing-philosophy correction: a
commercially-gated strategic driver must be validated **before** sunk-cost engineering momentum
accumulates, not after four phases. Killing the late Phase 5 is not a scope cut; it is fixing a
sequencing defect that would otherwise let the org build (a)+(b) and discover (c) is unaffordable.

Finally, V2 reclassifies `monitor.py` from "stream-json parser to replace" to "load-bearing
reliability signal source" — the budget/stall/error provenance for sprint. That reframing
changes the risk math correctly: the hard part was never the seam, it is reconstructing
load-bearing telemetry invariants from a lossier event stream.

---

## Per-Point Verdicts

| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| **X-001** recommendation posture (HYBRID vs DEFER) | **V2 (decision posture); synthesis on substance** | 78% | The *operational* delta is small (both gate on Phase 0), but as a **posture** V2 is sounder: you do not open a 5-phase roadmap whose strategic payoff sits behind an unverified commercial gate. V2's three-projects decomposition (§1) is the better framing. V1's own self-correction (§2, sprint "very-high") concedes the seam thesis doesn't hold uniformly — which is the DEFER argument in V1's own voice. |
| **X-004** roadmap abstraction (uniform-wrap vs PARTIAL/1107-direct) | **V2** | 88% | Source-verified: 1107-1118 direct `ClaudeProcess` for ordinary steps vs 1358-1365 factory-wrapped semantic path. Consequence for flagship readiness: roadmap is *partially* ready — the semantic-layer path is a legitimately clean first target, but V1's "easier flagship" framing implies whole-file readiness it does not have. Materially changes Phase-2 scoping. |
| **X-005** flagship sequencing (sprint-first vs pipeline-first/sprint-last) | **V2** | 90% | This is the cleanest architectural win in the set. Correct de-risking order is monotonic in seam cleanliness: pipeline (clean Protocol) → roadmap semantic path (wrapped) → sprint (private test hook, load-bearing monitor). V1 sequences its hardest, least-clean target first while *admitting* it is not clean — an internal contradiction. Sprint-last lets the event-adapter + MCP-contract learnings compound before the hard target. |
| **X-007** EE/RBAC placement (late Phase 5 vs day-zero) | **V2** | 80% | Right philosophy: a commercially-gated driver gates the program, so its evidence (EE quote, `@mastra/acp` license) belongs at day zero. *Qualify:* V1 is right that the *engineering* of tenancy should stay last (you cannot build RBAC before a runtime exists). The true synthesis: move the **decision/evidence** to Phase 0; keep the **build** at the end. V2's "kill Phase 5" is rhetorically strong but the *work* still lands late — V2 is correcting *when you decide*, not *when you build*. |
| **X-008** Phase 1 scope (wrap all ~62K vs 3-5 gates first) | **V2** | 82% | Incremental contract-proving beats big-bang exposure. You must validate the MCP/HTTP boundary's schema/error/latency/observability behavior on a few verified-pure checkers (gates.py, wiring_gate.py, fmea_classifier.py) before extracting 62K LOC — because if the boundary has a latency or schema-fidelity problem (see A-002), you want to find it on 3 modules, not 20. This is standard interface-risk-first sequencing. |
| **U-001/U-002** V1 roadmap + component matrix survival | **V1 (must survive into merge)** | 92% | This is where V1 is unambiguously stronger and the panel should resist discarding it. V2 is a *delta* — it revises phases and never restates them; it has no standalone roadmap and no component matrix. Strip V1's scaffolding and you have critique without a buildable plan. The matrix's file-level dispositions and the per-phase rollback paths are exactly the load-bearing detail an executor needs. **The merge base must be V1's structure; V2's corrections graft onto it.** |

---

## Shared-Assumption Responses

**A-001 — ACP is mature enough to be the substitution target.**
**QUALIFY (lean reject-as-unverified).** Architecturally this is the most dangerous unexamined
assumption, and *both* variants share the blind spot: they scrutinize Mastra's churn and
`@mastra/acp` licensing but treat the **ACP spec itself** as a stable destination contract.
A substitution target that is itself a young, evolving, lossy lowest-common-denominator protocol
is not a safe permanent boundary — if ACP's own event schema churns, every tool adapter and the
rewritten `monitor.py` reconstruction churn with it. This must be promoted to a Phase-0 gate
*alongside* the `@mastra/acp` license check: pin an ACP spec version and verify governance/
stability, not just the wrapper. Neither variant does this; the merge must add it.

**A-002 — 62K Python behind MCP/HTTP is performant enough on orchestration hot-paths.**
**QUALIFY.** This is an architecture-defining assumption, not a footnote. The MCP/HTTP boundary
is declared *permanent* architecture (V1 risk register: "treat as permanent, not a stopgap").
A permanent in-loop boundary that is crossed on every gate/convergence cycle (the 3-cycle
convergence loop, FMEA passes, audit sweeps) can turn "keep Python, don't rewrite" into a
latency regression that silently degrades throughput vs the in-process CLI benchmark. V2 surfaces
"prove latency contracts" in Phase 1 but does **not** make it a go/defer gate — it should be one.
The correct posture: a per-call latency + convergence-loop throughput benchmark is a Phase-0/1
**hard gate**, because the whole reuse thesis is invalid if the boundary is too slow for the
hot path. Accept the boundary as architecture *only after* it is benchmarked under convergence load.

**A-004 — V1's "5% tolerance acceptance gate" is operationally measurable.**
**REJECT as written.** This is the weakest piece of V1's architecture. A parallel-run safety net
is only as good as its oracle, and "identical outcomes within 5%" never defines the metric:
final artifacts? gate pass/fail vectors? token totals? turn counts? convergence iterations? These
are not commensurable and "5%" means something different for each. An undefined acceptance metric
is an unfalsifiable gate — it cannot fail, which means it cannot protect. The merge must replace
it with a **typed differential spec**: e.g. gate pass/fail must match exactly (0% tolerance on
correctness), artifact structural diff within a defined schema tolerance, and *separately*-bounded
economic drift (tokens/turns) as advisory, not pass/fail. The single scalar "5%" must die.

---

## Overall Verdict

**Synthesis, with V1 as the structural base and V2's corrections grafted in.**

V2 wins the *judgment* battles — flagship order (X-005), roadmap-readiness (X-004), EE-gate
timing (X-007), Phase-1 scope (X-008), and the `monitor.py` reclassification are all
architecturally correct and source-grounded. V2's three-projects decomposition is the better
mental model and its scoring inversion (V<R) is the honest consequence of taking the verified
coupling seriously.

But V2 is **not a buildable artifact** — it is a delta. It revises phases it never states and
carries no component matrix. A panel that simply "picks V2" ships critique without a plan. V1's
executable scaffolding (U-001, U-002) is load-bearing and must survive.

The DEFER-vs-HYBRID dispute is, architecturally, **smaller than it looks**: both gate on a
Phase-0 spike. The real disagreement is *posture and sequencing*, not whether to run the spike.
DEFER is the more honest label because it forbids momentum before evidence; but the deliverable
is still V1's roadmap, reordered (sprint-last), rescoped (gates-first), and with the EE evidence
pulled to day zero.

## Recommended Base + What to Graft

**Base: V1** (its 12-section structure, roadmap scaffolding, and component matrix).

**Graft from V2:**
1. **Flagship order → pipeline-first, roadmap-semantic-second, sprint-last** (X-005). Rewrite
   V1 Phase 2 accordingly. *(highest-value graft)*
2. **roadmap = PARTIAL** in the component matrix and Phase 4 — split the roadmap disposition into
   "semantic-layer path: adapt/factory-wrapped" vs "ordinary steps: rewrite (1107 direct)" (X-004).
3. **EE evidence → Phase 0** as a commercial blocker; keep tenancy *build* last (X-007 with my
   qualifier — decide early, build late).
4. **Phase 1 = 3-5 verified-pure gates first**, contracts proven, before 62K extraction (X-008).
5. **`monitor.py` reclassified** as load-bearing reliability signal source in the risk register,
   not a parser swap.
6. **Backlog.md = derived mirror until lossless round-trip proven** (X-006), then promote.
7. **Recommendation label → DEFER (conditional-go pending Phase-0 evidence package)** — adopt V2's
   posture and the V<R scoring honestly.

**Graft from my own lens (neither variant has these):**
8. **Promote A-001 (ACP-spec maturity) to a Phase-0 gate** — pin a spec version; verify governance.
9. **Promote A-002 (boundary latency under convergence load) to a Phase-0/1 hard gate** before
   declaring the MCP boundary permanent architecture.
10. **Replace the "5% tolerance" scalar with a typed differential spec** (A-004): 0% on gate
    correctness, schema-bounded artifact diff, advisory-only economic drift.

**Net:** V2 is right about *what is true*; V1 is right about *what to hand a builder*. Merge =
V1's body with V2's judgments and three architecture-level gates the panel should not let either
variant's blind spot carry forward.
