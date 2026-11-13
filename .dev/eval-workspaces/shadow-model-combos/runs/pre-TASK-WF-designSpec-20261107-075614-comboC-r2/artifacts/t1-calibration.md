# Wave 1D: blind calibration of the Tier 1 card

Calibrator: `confidence-calibrator` agent (frontmatter model class sonnet; served model = `ANTHROPIC_DEFAULT_SONNET_MODEL`). Input: the card file only. `calibrator_diversity: degraded` (reviewer classes are sonnet, haiku, opus; no disjoint class is available).

| Dimension | Score |
|---|---|
| Citation grounding | 0.85 |
| Coverage completeness | 0.60 |
| Deviation-classification clarity | 0.50 |
| Risk surface coverage | 0.55 |
| Recommendation actionability | 0.45 |
| **C (mean)** | **0.59** |

Calibrator notes (verbatim gist): line cites for F1 to F9 hold; F3 overstates (Task 1 O1 and Task 8 already ask for one minted cycle id place); the 14 unmapped rows are not named in the card; six of nine findings are tagged "other"; findings name a task and line but rarely a concrete fix; dependency ordering and the pinned-sentence/classification-table risks are not judged.

Routing: C = 0.59 < 0.85, so rule 6 also says ESCALATE; the `--tier 2` pin already forces Tier 2.
