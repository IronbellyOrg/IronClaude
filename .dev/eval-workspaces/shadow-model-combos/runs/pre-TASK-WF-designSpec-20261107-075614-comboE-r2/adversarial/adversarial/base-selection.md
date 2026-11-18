# Base Selection (orchestrator-written, simplified; deviations in debate-transcript.md)
## Quantitative scoring (50%)
| Metric (weight) | V1 | V2 | V3 |
|---|---|---|---|
| Requirement coverage (0.30): rows checked / 48 | 0.50 | 1.00 | 0.50 |
| Internal consistency (0.25): 1 - contradicted claims / claims | 0.78 (F1 ownership claim wrong, F8 refuted) | 1.00 | 1.00 |
| Specificity (0.15) | 0.95 | 0.95 | 0.95 |
| Dependency completeness (0.15): citations that resolve | 0.90 | 1.00 | 0.90 |
| Section coverage (0.15) | 1.00 | 1.00 | 1.00 |
| quant_score | 0.7725 | 0.9925 | 0.8425 |
## Qualitative scoring (50%)
Proxy: blind-calibrated card confidence C from the confidence-calibrator (V1 0.60, V2 0.57, V3 0.60). The 30-criterion document rubric was not applied (it targets documents, not reviewer cards). No position-bias second pass was run.
## Combined
- V1 = 0.5 x 0.7725 + 0.5 x 0.60 = 0.686
- V2 = 0.5 x 0.9925 + 0.5 x 0.57 = 0.781
- V3 = 0.5 x 0.8425 + 0.5 x 0.60 = 0.721
- Margin V2 over V3: 0.060 (above the 5% tiebreak band); no tiebreaker.
## Selected Base: Variant 2 (reviewer-2, qa lens, haiku class)
Rationale: full row coverage and no contradicted claim. Strengths to incorporate from the others: V1's interface-level gaps (M1 to M5, M11) and V3's pin finding (M7).
