# Base Selection Report: Q17

Performed by: the orchestrating session (group 4 worker), inline, as the debate-orchestrator role. Variant 1 = proposal-A (yes, panel in release 3), Variant 2 = proposal-B (not now), Variant 3 = proposal-C (never).

## Quantitative Scoring (50% weight)

Source "requirements" = 6 items the question rests on: OB-09, SW-11, Q9, NFR-001, the contract-note verbatim-words rule (ADJ line 253), and the 78 percent judgement (ADJ line 361).

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 1.00 (6 of 6) | 1.00 (6 of 6) | 0.67 (4 of 6; no Q9, no NFR-001) |
| internal_consistency | 0.25 | 1.00 | 1.00 | 1.00 |
| specificity_ratio | 0.15 | 0.85 | 0.80 | 0.80 |
| dependency_completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **0.978** | **0.970** | **0.870** |

## Qualitative Scoring (50% weight): Additive Binary Rubric (CEV, condensed)

| Dimension / criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|
| Completeness 1: covers OB-09 and SW-11 | MET | MET | MET | All three state the OB-09 condition (3) and SW-11 effect |
| Completeness 2: edge cases and failures | MET | MET | MET | V1 freshness; V2 drift; V3 reversal cost |
| Completeness 3: dependencies | MET | MET | MET | PR #539, Q9 or v2 named |
| Completeness 4: completion criteria | MET | MET | MET | Ledger record in each |
| Completeness 5: out of scope stated | NOT MET | NOT MET | NOT MET | None states what the answer does not authorize |
| Correctness 1: no factual errors | NOT MET | MET | MET | V1 cites Q22 as the staleness question for sweep reports; Q22 covers snapshot or workspace records (MR line 549) |
| Correctness 2: feasible under stated constraints | NOT MET | MET | MET | V1 needs PR #539 merged, Q9 overridden, Q19 choosing Decision Desk |
| Correctness 3: consistent terminology | MET | MET | MET | |
| Correctness 4: no internal contradiction | MET | MET | MET | |
| Correctness 5: claims supported | MET | MET | NOT MET | V3's "never" and its reverse clause ("the sweep reads no observer output") have no source; its advocate conceded |
| Structure 1 to 5 | 5 MET | 5 MET | 5 MET | Identical layout |
| Clarity 1, 2, 3, 5 | 4 MET | 4 MET | 4 MET | |
| Clarity 4: ids glossed | NOT MET | NOT MET | NOT MET | SW-11 or OB-09 unglossed in each |
| Risk 1: probability and impact | NOT MET | NOT MET | NOT MET | |
| Risk 2: mitigation per risk | MET | NOT MET | NOT MET | V1: report age label, capture before stored file |
| Risk 3: failure and recovery | NOT MET | MET | MET | V2: a later yes has the rule waiting; V3: reversal path named |
| Risk 4: external dependencies | MET | MET | MET | PR #539 open |
| Risk 5: monitoring | NOT MET | NOT MET | NOT MET | |
| Invariant 1: collection boundaries | NOT MET | NOT MET | NOT MET | |
| Invariant 2: state across components | MET | NOT MET | MET | V1 freshness gap; V3 vocabulary mix |
| Invariant 3: guard gaps | MET | MET | NOT MET | V1 age label; V2 keeps the verbatim rule for a later yes |
| Invariant 4: count divergence | NOT MET | NOT MET | NOT MET | Not applicable |
| Invariant 5: interaction effects | MET | NOT MET | MET | V1 two sources on one screen; V3 incompatible JSON shapes |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4/5 | 4/5 | 4/5 |
| Correctness | 3/5 | 5/5 | 4/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 2/5 | 2/5 | 2/5 |
| Invariant and Edge Case | 3/5 | 1/5 | 2/5 |
| **qual_score** | **21/30 = 0.700** | **21/30 = 0.700** | **21/30 = 0.700** |

### Edge Case Floor Check
All at least 1/5; all eligible.

## Position-Bias Mitigation
Single evaluator, two passes (1, 2, 3 then 3, 2, 1). The passes disagreed on Correctness 1 for V1 (is a mis-scoped question reference a factual error?). Re-evaluated as NOT MET: the claim misstates what Q22 covers. Disagreements re-evaluated: 1. Final verdicts changed: 0 relative to pass 1.

## Combined Scoring

| Variant | Quant x 0.50 | Qual x 0.50 | Final Score |
|---|---|---|---|
| V1 (proposal-A) | 0.489 | 0.350 | 0.839 |
| V2 (proposal-B) | 0.485 | 0.350 | 0.835 |
| V3 (proposal-C) | 0.435 | 0.350 | 0.785 |

Margin V1 over V2: 0.4 points (below the 5 point threshold). Tiebreaker applied: yes, level 1 (debate points won): V2 won 9 points (C-001, C-002, C-003, X-001, X-002, X-003, U-002, A-001, A-002), V1 won 3 (C-004, C-005, U-001), V3 won 1 (U-003).

## Selected Base: Variant 2 (proposal-B, not now)

### Selection Rationale
Tied on the scored rubric with Variant 1, but decisively ahead in the debate (9 of 13 points) and the unanimous overall choice of all three advocates (62, 70, 62 percent), including the advocates for Variants 1 and 3. Its scope matches the spec answer (MR line 544), the 78 percent judgement scoped to "now" (ADJ line 361) and both sides of the source split (round2-rebuttal-V5.md line 69).

### Strengths to Preserve from Base
1. No panel now; OB-09 plans on snapshot v1 only; the soft edge stays.
2. Q9 and NFR-001 untouched.
3. The verbatim-words and report-age rule kept live for a later yes.

### Strengths to Incorporate from Non-Base Variants
1. Advocates 1, 2, 3: a written re-ask trigger.
2. From V1 (U-001, C-005): the freshness gap recorded in the contract note as a constraint for any later yes (WC-16 is a cap, not a schedule).
3. From V1 advocate: one sentence in OB-09 that a sweep-facts area may be added later.
4. From V3 (C-004): name v2 as a possible home for a joined view, marked unbuilt.
