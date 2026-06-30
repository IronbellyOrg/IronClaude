---
convergence_score: 0.74
rounds_completed: 2
---

# Adversarial Debate — `roadmap validate` Roadmap Variants

**Variant A:** Opus/architect — 6 weeks, linear chain, executor-folded merge, leaner deliverable set (~48).
**Variant B:** Sonnet/architect — 10 weeks, DAG with cross-edges, dedicated semantics milestone, granular deliverable set (~70).
**Premise:** Both variants share 20 architectural assumptions (same modules, reuse contract, single code path, 7 dimensions, non-blocking exit). The debate is over *milestone packaging, schedule, and contract-lock sequencing* — not over what gets built.

## Round 1 — Initial Positions

### Divergence 1: Timeline (6w vs 10w)
**Variant A:** Effort-sized milestones are the honest model. M1 (config + contracts) and M4 (CLI wiring) are genuinely 1-week surfaces; padding them to 2 weeks manufactures slack that hides where the real cost lives. The work concentrates in the executor — so concentrate the schedule there (2-week M3) and keep the rest tight. 6 weeks is a credible critical-path estimate, not an aggressive one.
**Variant B:** Uniform 2-week blocks are defensible because every milestone here carries contract risk, not just construction risk. M1 isn't "just config" — it's locking the public CLI/report contract and resolving seven open questions. A 1-week M1 under-budgets the analysis that prevents downstream rework. 10 weeks buys the buffer that the shared #2 risk (false positives / contract churn) demands.

### Divergence 2/3/4/14: Report-semantics boundary & executor placement
**Variant A:** Fold FR-050.6/050.7 (report schema, adversarial merge, agreement table) into the M3 executor. The executor *produces* the report and *runs* the merge — co-locating the logic with its producer minimizes hand-off seams. CLI wires last (M4) against a frozen report contract.
**Variant B:** Extract report semantics + merge into a dedicated M4, move the executor up to M2. The merge resolution, count-recalculation, and citation enforcement are the single highest-error-rate surface in the feature. Isolating them into their own milestone with focused review is a correctness hedge. Wire CLI earlier (M3) so end-to-end plumbing is demoable before the report internals are perfected.

### Divergence 6/7: Safety-mechanism sequencing
**Variant A:** Build the NFR-050.2 import-scan test in **M1** and run it as a standing CI gate from day one. The circular-dependency risk is rated High and shared by both variants — catching it the moment it's introduced beats deferring to the release gate. OQ resolution is distributed just-in-time at each point of need.
**Variant B:** Resolve **all** OQ-001..007 before M2 exit. Locking the public CLI/report contract before implementation is the stronger hedge against late churn — a late OQ-005 (N≥3 merge) discovered in M3 forces executor rework. Import-scan design is approved in M1; enforcement deferred to M5 (TEST-010).

### Divergence 5/8/9: Granularity & edge-path coverage
**Variant A:** ~48 deliverables. The resolver/factory boundaries (filename resolver, model-precedence resolver, step factories) are implementation detail a competent implementer infers. Making them first-class adds tracking overhead without adding decisions. Gate-failure artifact policy lives as M3 risk mitigation, not a standalone unit.
**Variant B:** ~70 deliverables. COMP-009/010/011 and OPS-001/002/003 make implicit sub-tasks testable and unambiguous — model precedence, partial-report policy (OQ-007), and resume paths are real gaps Opus leaves to inference. R-010 explicitly threads resume/gate-failure edge coverage. Explicitness lowers executor ambiguity for parallel or junior teams.

### Divergence 11: WARNING-dims & DM-007 priority (P0 vs P1)
**Variant A:** Keep FR-050.5e/5f (interleave/decomposition) and DM-007 (agreement row) at **P0**. They are part of the committed dimension surface; shipping without them ships a partial feature.
**Variant B:** Downgrade to **P1**. The two WARNING dims are advisory by severity, and the agreement row is a presentation contract — both are legitimate descoping levers if schedule tightens, without compromising the BLOCKING-dimension core.

### Divergence 13: Success-criteria attribution
**Variant A:** Distribute success criteria to the milestone where each is first provable (gate criteria at M2, dispatch at M3). Enables per-milestone exit verification on local evidence.
**Variant B:** Attribute nearly all criteria to M5. Simpler gate model; centralizes proof at the release milestone where the E2E harness exists.

## Round 2 — Rebuttals

### A rebuts B
- **On timeline:** "Every milestone carries contract risk" proves too much — it's an argument for *front-loading the contract* (which I do via M1 type contracts + OQ-001 triage), not for inflating *construction* milestones to 2 weeks each. M1 and M4 staying at 1 week doesn't shortchange analysis; it refuses to bill CLI plumbing at executor rates. B's 67%-larger estimate is buffer disguised as scope.
- **On the dedicated M4 semantics milestone:** isolating merge into its own milestone *creates* the hand-off seam it claims to remove — the executor (M2) now emits a report whose semantics are finalized two milestones later, so M2's executor is built against an unfrozen report contract. That's the exact late-churn risk B says it wants to avoid, relocated inside its own plan.
- **On deferring the import gate to M5:** this is B's weakest move. Both of us rate circular-dependency High. A design "approved in M1" with enforcement in M5 means a violation introduced in M2's executor (the densest module) sits undetected for six weeks. Concede the OQ front-load; do not concede the day-one gate.
- **On granularity:** COMP-009/010/011 are resolver *decisions*, and I agree those decisions must be made — but they belong to OQ-001/OQ-004 resolution, not to 6 additional tracked deliverables. B is double-counting the same decision as both an open question and a component.

### B rebuts A
- **On timeline:** A's 2-week M3 is the real risk concentration. Folding executor + merge + report schema + count-recalculation + agreement table into one milestone means a single milestone owns the feature's highest-error surface *and* its tightest schedule. If M3 slips in a linear chain, the entire downstream (M4 CLI, M5 tests) slips with zero slack. My uniform schedule isn't padding — it's distributing the blast radius A concentrated.
- **On the executor-folded merge:** "co-locate logic with its producer" is fine for low-risk code; for the highest-error surface it's exactly backwards. Merge resolution and count-recalculation deserve a focused-review milestone precisely *because* they're error-prone. My M2 executor emits the report *structure*; M4 refines merge *semantics* — gated by OQ-003/005/006/007 which I resolve in M1, so the contract is in fact frozen before M4 touches it.
- **On the import gate:** I concede A's M1 day-one import-scan is strictly better than my M5 deferral. There is no schedule cost to building a static scan test early. Adopt it.
- **On granularity:** A calls OPS-003 (gate-failure artifact policy) a "risk note." A risk note is not testable; OPS-003 paired with TEST-013 is. OQ-007 asks whether a partial report ships as `tasklist_ready:false` or "unknown" — that's a shipped-behavior contract, not a mitigation. Leaving it implicit risks shipping the behavior under-specified.
- **On P0/P1:** keeping interleave/decomposition at P0 is fine *if* the 6-week schedule holds. Since A's schedule has no slack, A is the variant that most needs the P1 descoping lever it refuses to define.

## Convergence Assessment

**Convergence score: 0.74** — high, because the architectural core was never in dispute (20 shared assumptions) and three of the five contested points reached explicit or near-explicit agreement.

### Areas of agreement reached
1. **Import-scan gate from M1 (Divergence 7):** *Resolved.* Variant B conceded — build the NFR-050.2 static scan in M1 as a standing CI gate. No schedule cost, strictly dominant for the shared High-rated circular-dependency risk.
2. **OQ front-loading (Divergence 6):** *Resolved toward B.* A's "just-in-time" stance does not actually conflict with locking contract-shaping OQs (001/004/005/007) early; A already front-loads type contracts. The synthesis both endorse: resolve contract-defining OQs before the executor milestone, while permitting genuinely local OQs (002/006) to settle in place. **Adopt both safety mechanisms early** — this was the diff analysis's predicted strongest synthesis and the debate confirmed it.
3. **Gate-failure artifact policy as a tracked, tested unit (Divergence 8):** *Resolved toward B.* A's rebuttal conceded only that the *decision* matters; B's point that shipped behavior (partial vs missing report → `tasklist_ready` value) must be testable (OPS-003 + TEST-013) stands unrebutted. Make it a deliverable.

### Remaining genuine disputes
1. **Timeline 6w vs 10w (Divergence 1):** *Unresolved — empirical.* Neither side moved. The honest resolution is not rhetorical: effort-load M3's deliverables against actual team velocity. A is correct that uniform blocks over-bill M1/M4; B is correct that A's linear chain gives a 2-week M3 zero downstream slack. **Synthesis:** A's effort-sizing principle + an explicit slack/buffer allocation on the executor milestone (a middle estimate of ~7-8 weeks with a sized, not padded, executor block).
2. **Report-semantics boundary (Divergence 2/3/4/14):** *Unresolved — the single largest structural fork.* Both exposed a real seam in the other: A showed B's M2-executor builds against a report contract finalized in M4; B showed A's M3 concentrates the highest-error surface under the tightest schedule. The reconciling move neither fully articulated: **freeze the report+merge *contract* in M1/M2 (B's contract-lock) but implement merge semantics co-located with the executor (A's seam-minimization)** — i.e., separate *contract milestone* from *implementation milestone* without giving merge logic its own late milestone. This requires a product/architecture call.
3. **P0/P1 descoping of WARNING dims + DM-007 (Divergence 11):** *Unresolved — product call.* Turns on whether advisory interleave/decomposition coverage is launch-blocking. B landed a clean rebuttal (A's slack-free schedule is the one that most needs a descoping lever), but neither can resolve it without a product decision on release-criticality of WARNING-severity coverage.
4. **Granularity ~48 vs ~70 (Divergence 5):** *Partially resolved.* Agreement that resolver *decisions* must exist; residual dispute over whether they are tracked deliverables or OQ-resolution outputs. Resolution is team-shape-dependent (parallel/junior teams favor B's explicitness; a senior solo implementer favors A's leaner set) — a deployment-context call, not a correctness call.

**Net:** The variants agree on *what to build* and have now converged on *both safety mechanisms early*. The durable forks are schedule realism, the report-semantics milestone boundary, and the WARNING-dimension launch bar — none of which a debate can close without team-velocity data and a product release-criticality decision. No agreement was forced: disputes 1, 2, and 3 above remain genuinely open and are flagged as such.
