# Reflect deviation patterns — bs346-ponytail

## pre-spec-20261108-reflect-1 (UC-1, issue 346 ponytail fix-audit plan)
- Verdict: partial (tier 2, calibrated 0.77, adversarial convergence 1.0 but two undebated fault-finder candidates). 2 blocking, 7 minor plan findings; 0 citations dropped of 22.
- Recurring pattern: a spec with no labelled ids yields 0 Pass-1 ids, so coverage_degraded parsed-sparse forces T2; 109 inferred rows, containment 0.789.
- Recurring plan-defect class: a "byte copy plus listed differences" variant command inherits text the spec's own static pins forbid (a `src/superclaude` path at the original's line 220; Usage-line flags whose defining section was removed). Check every copied line against every pin before planning.
- Recurring plan-defect class: protection rules stated by label (CRITICAL, FR-8, FR-9) are lost when the plan records only severity and blocking flag; record a protected flag explicitly.
- Lesson: the self-authored T1 card calibrated at 0.57; the plan author should not be the only reviewer.
