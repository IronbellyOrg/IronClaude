---
convergence_score: 0.74
rounds_completed: 2
---

# Adversarial Debate — Opus-Architect (Variant A) vs Sonnet-Architect (Variant B)

**Subject:** Decomposition of the identical 8-phase cross-framework analytical sprint (complexity 0.85 HIGH, architect persona, non-adversarial). 18 shared assumptions; 14 divergence points, all in milestone packaging, verification sequencing, and registry granularity — none in analytical content. Variant A = 8 milestones / 13 weeks (1:1 phase mapping + foundation M0). Variant B = 5 composite milestones / 12 weeks.

## Round 1 — Initial Positions

### Divergence 1 & 5 — Restartability timing (NFR-5) and scope-locking

**Variant A:** Restartability must be proven in M0, on a no-op gate, before any of the 35+ artifacts exist. A phase-gated sprint whose `--start` resume is broken is a latent catastrophe; the cost of discovering it is monotonically increasing in artifacts written. Proving it on day one costs a single no-op gate test. Same logic drives locking the comparison-pair set (OQ-PAIRSET) and artifact root (OQ-ROOT) in M0: every downstream path reference and every M3 `min_artifacts` derive from these, so resolving them before inventory eliminates a whole class of cascade drift.

**Variant B:** Restartability is a property of the sprint executor (COMP-003), not of the artifacts — it does not decay as work accumulates, so verifying it at M5 (NFR-XFDA.5) is functionally adequate and keeps the foundation milestone lean. Scope-locking is respected too, but with calibrated deadlines: artifact root (OI-4) is a hard precondition resolved *before M1 start*, and the pair set (OI-5) is resolved before M3 exit — locking it earlier than needed forecloses bounded, legitimate pair expansion that the strategy docs in M2 might justify.

### Divergence 2 & 3 — Milestone granularity (8 vs 5) and the standalone foundation week

**Variant A:** One milestone per spec phase plus a dedicated M0 gives gate-by-gate traceability and per-phase risk isolation. The entire duration delta (13 vs 12 weeks) is M0 — one week buying an explicit "infrastructure before artifacts" hard gate. Authoring the phase-gate contract (DM-002), the 8 gate-criteria rows (DM-003), and proving resume is genuinely prerequisite work; folding it into inventory interleaves contract authoring with the very work the contract governs.

**Variant B:** Five composite milestones reduce gate-boundary overhead and management ceremony without losing a single deterministic checkpoint — the 8 §5.2 phase gates still exist *inside* the milestones; only the milestone wrapper count drops. Contracts (DM-002/DM-003) are small (S-effort) and naturally co-resolve with inventory under one M1 gate. The extra Opus week is pure milestone-boundary tax, not analytical work.

### Divergence 4 & 14 — Validation/assembly separation and adversarial-validation prominence

**Variant A:** Adversarial validation (M6, typed **Quality**, P0) must be a discrete pass/fail boundary that closes *before* assembly (M7, Integration, P1) begins. Validation is where scope-creep and unverifiable citations get caught; burying it as step one of an assembly milestone lowers its structural visibility and lets assembly pressure compress the check.

**Variant B:** Validation is modeled as FR-XFDA-001.7 inside M5 with its own pass/fail per item and a corrected `final-improve-plan.md` — it is not weakened, only co-located with assembly so the closing pipeline runs as one coordinated 2-week unit. The pass/fail gate is identical; what changes is one fewer milestone transition at the most schedule-sensitive point.

### Divergence 8, 9, 10 — Priorities, risk granularity, parent-FR closure

**Variant A:** Every COMP row is P0 because the gate requires all 19 regardless — tiering is inert signal. Risk register R1–R10 is compact and folds related modes. End-to-end traceability is distributed across the M7 artifact-index check; no separate closure row needed.

**Variant B:** P0/P1/P2 tiers encode adoption-likelihood for triage under time pressure. The 17-row register (R-001–R-017) surfaces strategy-bias, citation-variance, shell-overfit, and field-completeness as discrete, individually-mitigated failure modes. A dedicated `FR-XFDA-001` closure row gives one auditable "8 child FRs + 6 NFRs + 19 components + 3 contracts traced" assertion — a single feature-done gate rather than an inference across the index.

## Round 2 — Rebuttals

### On restartability timing

**B rebuts A:** The "monotonically increasing cost" argument conflates *artifact loss* with *resume defect*. Incremental writes (which both variants mandate) preserve artifacts regardless of when resume is *verified*. A no-op M0 test also proves less than it claims: resume across a *real* phase boundary with real incremental state is the actual risk surface, and that can't exist in M0. So A pays a sequencing cost for a weaker proof.

**A rebuts B:** The objection proves A's point in reverse. Yes, a no-op test is a smoke test — but a *failing* smoke test on day one is the cheapest possible discovery of a structurally broken executor (wrong `--start` semantics, gate registry not loading, checkpoint format mismatch). B's "verify at M5" means the *first* resume attempt in anger could be the post-crash recovery itself, week 12, with no prior signal. A early test does not replace M5 validation; it de-risks the executor before 12 weeks depend on it. This remains A's strongest, least-contested advantage.

### On granularity and the extra week

**A rebuts B:** "The 8 gates still exist inside 5 milestones" concedes the gates but loses *milestone-level accountability* — when M2 bundles Phases 2+3, a Phase-2 defect and a Phase-3 defect share one exit gate and one owner, blurring which sub-phase failed. Per-phase milestones give per-phase ownership.

**B rebuts A:** That blur is illusory — DM-003 already defines *per-phase* deterministic minima and semantic checks, so the Phase-2 vs Phase-3 failure is attributable at the gate-row level whether or not they share a milestone wrapper. A is paying a real calendar week (8.3% of schedule) for a reporting-granularity nicety already delivered by the gate-criteria registry. The week is the weakest part of A's case.

**A concedes partially:** The week is defensible only if M0's contract-authoring + resume-proof genuinely cannot overlap inventory — which is largely true for contract authoring (it must precede the gates it defines) but *not* strictly true for the resume smoke test, which could run in parallel with early M1. A's M0 could compress toward S-effort within a 12-week envelope.

### On validation/assembly separation

**B rebuts A:** "Assembly pressure compresses the check" is a process-discipline fear, not a structural one — the pass/fail-per-item AC is identical and gate-enforced in both. A's separate Quality milestone adds a transition without adding a check.

**A rebuts B:** The transition *is* the check's teeth: an independent P0 Quality gate cannot be silently absorbed into "we're assembling now." But A acknowledges this is a prominence/visibility argument, not a correctness one — the verification content is equivalent. Genuine residual dispute, low stakes.

### On priorities, risk, closure

**A concedes to B (closure + risk):** B's `FR-XFDA-001` closure row and 17-row register are strict supersets — they add auditable surface with no contradiction. A's distributed M7 traceability is *equivalent*, so grafting B's consolidated closure assertion into A's M7 is pure gain. A should adopt both.

**B concedes to A (priorities):** A is correct that tiers are inert *if the gate requires all 19* — which it does. B's P0/P1/P2 only matters under partial-completion triage, which the strict-sequential gate never permits. The tiers are defensible as documentation of centrality but carry no behavioral force. Effectively resolved in A's favor.

**On ID scheme (Divergence 7):** Both concede this is cosmetic. B's flat OI-1..6 cross-references more uniformly; A's semantic OQ-ROOT/OQ-PAIRSET self-document better. Trivially mergeable — adopt flat IDs with semantic aliases.

## Convergence Assessment

**Areas of agreement reached (resolved):**
- **Risk register:** Adopt B's 17-row superset — no contradiction, strictly more visibility. (A concedes)
- **Parent-FR closure:** Graft B's consolidated `FR-XFDA-001` closure row into A's M7. (A concedes)
- **Component priorities:** Uniform P0 is correct under an all-19-required gate; tiers are non-behavioral. (B concedes)
- **ID scheme:** Merge to flat IDs with semantic aliases. (Both concede, cosmetic)
- **Scope-locking deadlines:** Functionally equivalent — root before M1 start, pair set before it gates M3. The M0-vs-just-in-time framing difference is immaterial once both are resolved pre-dependency.

**Strong lean, not full consensus:**
- **Restartability timing → A (early proof).** B's "resume doesn't decay" point narrows the *value* of an M0 test but does not defeat it; cheapest-possible discovery of a structurally broken executor is real and uncontested. A wins on substance; B wins the narrow point that a no-op test ≠ full resume validation (so keep *both* an M0 smoke test and M5 validation).
- **The extra week → B (fold toward 12).** A conceded the resume smoke test can overlap M1, collapsing most of M0's standalone justification. Contract authoring still wants to precede the gates, but fits within a foundation *sub-phase* of M1 rather than a dedicated week.

**Genuine residual disputes (unresolved):**
- **Milestone granularity (8 vs 5):** A true value judgment between per-phase milestone-level accountability and operational leanness. DM-003 delivers per-phase attribution either way, which weakens A's case but does not eliminate the ownership-clarity preference. Not forced to agreement.
- **Validation/assembly separation (M6/M7 vs M5):** Equivalent verification content; the dispute is structural prominence vs schedule compression. Low-stakes, unresolved.

**Synthesis direction:** The debate converges on a hybrid — adopt B's leaner 12-week envelope and superset registries (risk rows, closure assertion, flat IDs, conceded inert tiers), while preserving A's two substantive wins: an **M0/M1 foundation sub-phase** that authors DM-002/DM-003 before the gates and runs a `--start` resume **smoke test early** (retaining M5 full validation), and an **independent P0 validation boundary** even if co-located in the closing milestone. The score reflects strong content agreement and four fully-resolved divergences, with two honest, non-forced disputes (milestone count, validation prominence) remaining.
