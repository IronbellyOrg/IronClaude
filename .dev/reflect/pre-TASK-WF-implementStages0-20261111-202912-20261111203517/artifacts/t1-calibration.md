# Calibration report: Tier 1 card (saved by orchestrator from the calibrator's return)

calibrator_model_class: opus (disjoint set empty: reviewers use sonnet, haiku, opus; calibrator_diversity: degraded)
rubric: reflect 5-dimension rubric (refs/reflection-rubric.md)

| Dimension | Score |
|---|---|
| Citation grounding | 0.60 |
| Coverage completeness | 0.65 |
| Deviation-classification clarity | 0.30 |
| Risk surface coverage | 0.50 |
| Recommendation actionability | 0.45 |

- calibrated C = 0.50 (self-reported 0.80, delta -0.30)
- verdict: ESCALATE (low_confidence); forced to Tier 2 anyway by `--tier 2`
- leads confirmed by the calibrator: L1 (plan 135 vs Task 11), L2 (plan 182), L3 (no task verifies judge identity field), L8 (spec 470 names only the test file)
- leads not checked: L7 code line numbers; spec sha256 (no Bash)
- extra items it surfaced, not yet reviewed as findings:
  - Task 7 says "the five exit items" but lists four (plan 102; spec 408 lists four)
  - Task 17 has no "one total deadline" from the Execution contract (spec 363)
  - Task 19 has no Fable-judge assertion (spec 185, 240)
  - Risks rows 4, 5, 11 (spec 512-519) are in fact covered by Tasks 14, 19, 20; the card's "unmapped" claim was partly wrong
  - spec 436 and 438 already state the 7 null convergence scores (L5 answered)
