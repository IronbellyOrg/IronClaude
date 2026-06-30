# Base Selection

These are competing *positions*, not document variants, so quantitative metrics are weak signal; the qualitative rubric (Correctness, Risk Coverage, Invariant/Edge-case coverage) and — decisively — the Round 2.5 invariant probe carry the selection.

## Quantitative Scoring (50% weight) — informational
| Metric (weight) | A | B | C |
|---|---|---|---|
| Internal consistency IC (0.25) | 0.85 | 0.80 | 0.95 |
| Specificity SR (0.15) | 0.90 | 0.85 | 0.85 |
| Dependency completeness DC (0.15) | 0.85 | 0.85 | 0.90 |
| Section coverage SC (0.15) | 1.00 | 1.00 | 1.00 |
| Requirement coverage RC (0.30) | 0.90 | 0.85 | 0.90 |
| **quant_score** | **0.89** | **0.85** | **0.91** |

## Qualitative Scoring (50% weight) — additive binary, CEV
Decisive dimensions only (full rubric applied; subtotals shown):

| Dimension (5 each) | A | B | C |
|---|---|---|---|
| Completeness | 5 | 5 | 5 |
| **Correctness** | 3 | 3 | 5 |
| Structure | 5 | 5 | 5 |
| Clarity | 5 | 4 | 5 |
| Risk Coverage | 4 | 4 | 5 |
| **Invariant & Edge-Case** | 2 | 3 | 4 |
| **total /30** | **24** | **24** | **29** |
| **qual_score** | **0.80** | **0.80** | **0.97** |

**Correctness CEV (the deciding dimension):**
- **A — NOT MET on 2 criteria.** CLAIM: A's core mechanism is correct. EVIDENCE: INV-012 — evidence-validator is a precision gate but A motivates it with a recall property (R0/PR#112); INV-003 — A's "re-ground not drop" mitigation contradicts `evidence-validator.md:121` "match or drop". VERDICT: NOT MET (mechanism-class mismatch + non-viable mitigation).
- **B — NOT MET on 2 criteria.** CLAIM: B's prescription is feasible with stated constraints. EVIDENCE: U-003 semantic-fit defect (UC-2 taxonomy has no referent for recommendations); X-003 circular `audit-validator` nesting. VERDICT: NOT MET (prescription infeasible) — though B's *diagnosis* (precision≠recall) was correct and the probe vindicated it.
- **C — MET on all 5.** CLAIM: C's claims survive independent re-test. EVIDENCE: INV-014 ADDRESSED (reject-B sound); X-003 circular reuse confirmed at `SKILL.md:561`; the only C wobble (~68% on the auggie concession) was *resolved in C's favor* by the probe (the conceded add is the wrong mechanism). VERDICT: MET.

**Invariant & Edge-Case floor check:** all three ≥ 1/5, floor satisfied. C highest (named the auto-apply boundary + circular reuse pre-probe).

## Position-Bias Mitigation
Dual-pass (A→B→C and C→B→A) agreed on C as base in both orderings; the probe is order-independent. No disagreement to resolve.

## Combined Scoring
| Variant | quant×0.5 | qual×0.5 | **score** |
|---|---|---|---|
| A | 0.445 | 0.400 | **0.845** |
| B | 0.425 | 0.400 | **0.825** |
| **C** | 0.455 | 0.485 | **0.940** |

Margin C over A = 9.5 pts (>5%), no tiebreaker needed.

## Selected Base: Variant C (Reject)

**Selection rationale:** C is the only position whose *prescription* survives the Round 2.5 invariant probe. The reject-B reasoning is sound (INV-014). The reject-evidence-validator-for-cleanup-audit reasoning is sound (INV-013: citation re-check can't catch non-citation destructive defects). And the probe *upgraded* C's confidence on its one weak point — the auggie-review concession C made at only ~68% turns out to be the wrong mechanism anyway (INV-012/INV-003), so C should not even have conceded the `evidence-validator` import.

**Strengths to preserve from C:** the applied-vs-recommendation framing; "reflect is already wired where applied work exists (remediation C/E)"; circular-reuse argument; zero-new-dependency maintainability; the auto-apply boundary as the one condition that flips the verdict.

**Strengths to incorporate from non-base:**
- From **A**: the precise localization of auggie-review's same-context citation gap as a *real, narrow* defect (the `:415`-vs-`:561` existence proof) — but redirect the fix away from `evidence-validator`.
- From **B**: the precision-vs-recall diagnosis and the explicit naming of single-class representational bias — which the probe (INV-012) confirmed and which sharpens *why* the cheap precision gate is the wrong tool.
