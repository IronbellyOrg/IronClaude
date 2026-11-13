# Wave 1D — T1 card blind calibration (confidence-calibrator, opus class)

calibrator_class: opus (collides with reviewer class t1a; all three available classes seated — legal degraded path, calibrator_diversity: degraded)
formation_context: stripped (card file only + cited files)

## Scores

| Dimension | Score |
|-----------|-------|
| Citation grounding | 0.95 |
| Coverage completeness | 0.85 |
| Deviation-classification clarity | 0.90 |
| Risk surface coverage | 0.75 |
| Recommendation actionability | 0.70 |

**C = 0.83** (self-assessed 0.86; delta -0.03). Escalation recommendation: **ESCALATE to T2**.

## Calibrator-noted gaps in the T1 card (feed T2)

- Task 11 "find them with grep under tests/" is vague.
- Task 10's wording variant is undefined while its check only counts grep hits.
- Stale-checkout warning in issue-summary.md:29 (49 commits behind) not carried.
- verify-sync may fail from unrelated drift.
- F1 rated medium while its own text says execution risk low (severity tension).

## Resolution

T2 already pinned by --tier 2; parsed-sparse pre-filter independently forbids T1 stop. Rubric row 6 (C < 0.85) would also have escalated. No conflict.
