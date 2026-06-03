# Base Selection — Mastra/Beads Port Reconciliation

## Selection summary

This is a **thesis–antithesis reconciliation**, so base selection separates two questions the panel answered differently:

- **Structural base (the document skeleton we build on): Variant 1 (HYBRID study).** It is the only standalone, buildable artifact — full 5-phase roadmap with rollback paths, a file-level component port matrix, a 13-row risk register, and a "what would have to be true" frame. V2 is a *delta* with no skeleton of its own.
- **Judgment base (the conclusions/scoring the document asserts): Variant 2 (DEFER review).** Its recommendation, V/C/L/R re-score, and sequencing corrections are source-verified (6/6 citations confirmed by the analyzer judge) and are adopted wholesale, with one qualification (X-007).

**Net base decision:** `base_variant = Variant 1 (structure) + Variant 2 (judgments)`. The merged document keeps V1's bones and replaces its conclusions, framing, and sequencing with V2's corrected ones, then adds three+ new gates neither source caught.

---

## Quantitative layer (50%)

| Metric (weight) | Variant 1 | Variant 2 | Notes |
|---|---|---|---|
| Requirement coverage RC (0.30) | 0.95 | 0.70 | V1 covers every topic end-to-end; V2 (delta) omits restating roadmap/matrix. |
| Internal consistency IC (0.25) | 0.78 | 0.95 | V1 carries two live tensions (sprint-first vs its own "sprint not substitution-clean"; "sole task-of-record" vs its own rollback). V2 is source-grounded and self-correcting. |
| Specificity SR (0.15) | 0.82 | 0.93 | V2 cites file:line throughout; V1 is concrete but less verifiable. |
| Dependency completeness DC (0.15) | 0.90 | 0.62 | V1 resolves its own cross-refs; V2 depends on V1 by reference. |
| Section coverage SC (0.15) | 1.00 | 0.45 | V1 = 12 sections; V2 = 5 delta sections. |
| **quant_score** | **0.886** | **0.745** | V1 leads on completeness/structure. |

## Qualitative layer (50%) — dimension subtotals (additive binary, CEV)

| Dimension (5 crit) | V1 | V2 | Evidence highlight |
|---|---|---|---|
| Completeness | 5/5 | 3/5 | V1 covers out-of-scope, deps, success criteria; V2 omits full roadmap restatement. |
| Correctness | 3/5 | 5/5 | V2's claims are source-verified (6/6); V1 contains the refuted "uniformly factory-wrapped" + over-favorable scoring. |
| Structure | 5/5 | 4/5 | V1 logical 12-section flow; V2 well-structured delta. |
| Clarity | 4/5 | 5/5 | V2's "claims survived vs knocked down" + reordered gates are sharper decision aids. |
| Risk coverage | 4/5 | 4/5 | V1 has the falsifiable likelihood/impact register; V2 has better-ordered go/defer gates. Complementary. |
| Invariant & edge-case | 3/5 | 4/5 | V2 surfaces telemetry/round-trip/perm-semantics invariants more sharply; both miss A-001/A-002/A-004 (caught only in this debate). |
| **qual_score** | **24/30 = 0.800** | **25/30 = 0.833** | Near-tie; V2 edges on correctness+clarity. |

## Edge-case floor check
- V1 invariant dimension: 3/5 → eligible. V2: 4/5 → eligible. Floor (≥1/5) satisfied by both.

## Combined
| Variant | quant×0.5 | qual×0.5 | **combined** |
|---|---|---|---|
| V1 | 0.443 | 0.400 | **0.843** |
| V2 | 0.373 | 0.417 | **0.790** |

Margin 0.053 — outside the 5% tiebreaker band, V1 leads **on the combined score that measures document completeness**. This correctly identifies V1 as the **structural base**. It does *not* mean V1's *conclusions* win — the qualitative Correctness dimension (V2 5/5 vs V1 3/5) and the unanimous panel verdict establish that V1's *judgments* are superseded by V2's. The scoring model rewards V1's completeness; the debate rewards V2's correctness. The synthesis honours both: **V1's body, V2's brain.**

## Selected base: Variant 1 (structure) — judgments replaced by Variant 2

**Strengths to preserve (from V1):** 5-phase roadmap scaffold + rollback paths; component port matrix; "what is lost" table; "what would have to be true" frame; 13-row falsifiable risk register; current-state stratification.

**Strengths to incorporate (from V2):** DEFER recommendation reframed as a standalone Phase-0 intelligence sprint; V28/C34/L20/R34 re-score with rationale; "1.2K = narrow seam + broad behavioral coupling" reframing; roadmap-PARTIAL correction; flagship reorder (pipeline→roadmap→sprint-last, sprint gated on telemetry-reconstruction); Backlog.md = derived mirror; reordered go/defer gate list; "claims survived vs knocked down" calibration; convergence.py-stays-agnostic concession.

**New material (from this debate, neither source):** gates G-A (ACP-spec maturity/version-pin), G-B (MCP boundary latency under convergence load), G-C (typed differential spec replacing the unfalsifiable 5% gate); promoted A-003 operating-model/staffing gate; end-to-end tenancy pilot/control-plane gate; explicit INV-013 framing that Phase-0 success only authorizes the next bounded validation phase.
