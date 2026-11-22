# Base Selection

DEGRADED SCORING (recorded loudly): the two variants are review cards of one plan, not two drafts of one artifact, and both are cut off by a transport limit. The 30-criterion, dual-pass rubric was therefore reduced by the orchestrator to one pass at the six-dimension level, with dimension subtotals assigned by hand and tied to the evidence below. The scores are judgments, not deterministic computations; they only decide which card is the base of the merge. The merged verdict does not depend on them, because every verified finding of both cards is carried into it.

## Quantitative Scoring (50% weight)

Source "requirements" for coverage = the seven verified or accepted points: ordering (C-001), helper fetch (C-002), patch-and-bundle (C-003), pull-request step (C-004), 15 rows (C-005), fallback conflict (C-006), open-pull-request proof (new).

| Metric | Weight | Variant 1 | Variant 2 |
|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 3 of 7 = 0.43 | 4 of 7 = 0.57 |
| Internal consistency (IC) | 0.25 | 0.85 (two slips: PLAN:99 attribution, Task 2 overstated) | 0.90 (F2 grade overstated, confidence 0.95 too high) |
| Specificity ratio (SR) | 0.15 | 0.95 | 0.95 |
| Dependency completeness (DC) | 0.15 | 1.00 (every cite resolved) | 1.00 (every cite resolved) |
| Section coverage (SC) | 0.15 | 0.85 | 1.00 |
| quant_score | | 0.43x0.30 + 0.85x0.25 + 0.95x0.15 + 1.00x0.15 + 0.85x0.15 = 0.762 | 0.57x0.30 + 0.90x0.25 + 0.95x0.15 + 1.00x0.15 + 1.00x0.15 = 0.839 |

## Qualitative Scoring (50% weight)

| Dimension (5 criteria each) | Variant 1 | Variant 2 | Evidence |
|---|---|---|---|
| Completeness | 2 | 3 | V2 adds four distinct points, V1 three; neither shows its coverage-gaps section (cut off) |
| Correctness | 4 | 3 | V1 grades follow the rule; V2's F2 and F3 were regraded or disputed in the debate |
| Structure | 4 | 4 | Both use claim, evidence, consequence, fix |
| Clarity | 4 | 4 | Both plain and cited |
| Risk coverage | 3 | 4 | V2 names the recorder blind spot and the dropped capability |
| Invariant and edge-case coverage | 2 | 3 | V2's canned-reply blind spot; V1's collector-test gap |
| Subtotal | 19 of 30 = 0.633 | 21 of 30 = 0.700 | |

Edge-case floor (at least 1 of 5): both pass.

## Position-Bias Mitigation

Not run as a second pass (see the degraded-scoring note). The order effect is limited by the fact that the scores above were checked against the debate's per-point verdicts, which were produced by advocates of both cards.

## Combined Scoring

| Variant | Quant (50%) | Qual (50%) | Combined |
|---|---|---|---|
| 1 | 0.762 | 0.633 | 0.698 |
| 2 | 0.839 | 0.700 | 0.770 |

Margin 7.2 percent (more than 5 percent): no tiebreaker applied.

## Selected Base: Variant 2 (haiku class, qa lens)

Selection rationale: broader coverage of distinct plan defects (hidden helper side effects, dropped capability, missing finish step) and a wider risk surface, at the cost of two over-graded findings, which the merge corrects from the debate.

Strengths to preserve: F1 to F4 headlines and evidence lines; the recorder blind-spot observation.

Strengths to incorporate from variant 1: the wider scope of the ordering finding (Tasks 2, 3, 4, 5, 11, 12) and the collector-test gap; the 14 versus 15 row finding; the Task 1 fallback conflict; the correct grades. From the debate: the open-pull-request proof point. From the invariant probe: INV-001 to INV-009.
