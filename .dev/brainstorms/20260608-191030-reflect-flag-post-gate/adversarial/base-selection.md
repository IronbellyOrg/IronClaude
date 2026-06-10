# Base Selection

## Quantitative Scoring (50% weight)

| Metric (weight) | V1 architect | V2 refactorer | V3 qa |
|---|---|---|---|
| Requirement coverage (0.30) — all 10 OQs resolved | 1.00 | 0.95 | 0.90 |
| Internal consistency (0.25) | 0.95 | 0.80 (X-001 none/disabled bug) | 0.90 |
| Specificity (0.15) | 0.92 | 0.95 (diffs) | 0.95 (ATs) |
| Dependency completeness (0.15) | 0.95 | 0.92 | 0.88 |
| Section coverage (0.15) | 0.92 | 0.92 | 1.00 (13 sections) |
| **quant_score** | **0.957** | **0.882** | **0.909** |

## Qualitative Scoring (50% weight) — additive binary rubric (/30)

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5/5 | 4/5 | 4/5 |
| Correctness | 5/5 | 3/5 (none-semantics + halt-alias errors) | 4/5 (auto drops S5) |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 5/5 | 5/5 |
| Risk coverage | 5/5 | 5/5 | 4/5 |
| Invariant & edge-case coverage | 5/5 | 4/5 | 5/5 |
| **qual_score** | **29/30 = 0.967** | **26/30 = 0.867** | **27/30 = 0.900** |

Edge-case floor (≥1/5 on invariant dimension): all pass.

## Combined Scoring

| Variant | quant×0.5 | qual×0.5 | **combined** |
|---|---|---|---|
| **V1 architect** | 0.479 | 0.483 | **0.962** |
| V3 qa | 0.455 | 0.450 | 0.905 |
| V2 refactorer | 0.441 | 0.433 | 0.875 |

Margin V1→V3 = 0.057 (> 0.05) → no tiebreaker; **V1 wins outright**.

## Selected Base: Variant 1 (opus:architect)

**Selection rationale:** V1 is the only variant correct on the highest-stakes semantic point — the distinction between `none` (gate off, no item) and `halt` (manual disjoint item present) — which V2 conflated (X-001) and V3 partially flattened. V1's total old→new map, single-producer `reflect_post_mode` oracle, and asymmetric wrapper-fallback rationale form the most complete and internally consistent backbone. Its only weaknesses (the redundant `S2≥3` auto gate; a slightly large mode enum) are minor and corrected by the merge.

**Strengths to preserve (from base V1):** the `{none,1,2,auto}` dial + distinct `halt`/`2-degraded-halt` derived states; the total §5 old→new map; FR-9 single-producer invariant; §8 asymmetric-fallback rationale; mode-fixes-depth / O4-preserved-by-construction (§7).

**Strengths to incorporate (from non-base):**
- **V3 → §9 validation**: replace V1's prose validation with V3's exhaustive **V1–V16 assertion matrix** + per-mode active-assertion map + the **§13 FR→acceptance-test matrix**. (U-001)
- **V2 → §6 templates**: add V2's **unified-diff presentation** of the Mode-2 template against current `:1994–1999`, and V2's **executor-disjointness trade-off table**. (U-002)
- **V2/V3 → §4 auto FER**: drop V1's standalone `S2≥3` gate; adopt the 3-term predicate `S6==1 ∨ S5>0 ∨ TCS≥35 → 2`. (C-002)
- **Invariant probe → §8**: unify the wrapper-availability fallback ladder for fixed-2 AND auto-2 (INV-002).
- **Invariant probe → §4/§10**: advisory warning for fixed `--reflect 1` on S6=1/S5>0 (INV-003).
