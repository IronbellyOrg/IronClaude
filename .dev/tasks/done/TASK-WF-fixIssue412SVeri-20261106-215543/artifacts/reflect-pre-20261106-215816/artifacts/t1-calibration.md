# Calibration Report

## Inputs and limits
Reflect UC-1 five-dimension rubric; Tier 1 card only plus installer source spot-checks. Calibrator alias: sonnet, requirements analyst: opus. Actual underlying gateway models remain unverified. The calibrator looked for coverage-matrix.json in the wrong directory and did not read it; this is a failed lookup, not evidence the artifact is absent. The real artifact is sibling coverage-matrix.json of this report. No formation context supplied.

## Scores
| Dimension | Score | Justification |
|---|---:|---|
| Citation grounding | 0.80 | Three installer source claims matched; matrix/test/discovery not independently checked by this calibrator. |
| Coverage completeness | 0.65 | Eight unmatched rows explicitly registered, with lexical versus semantic caveat. |
| Deviation-classification clarity | 0.60 | Six analyst notes not yet adjudicated; not a post-execution audit. |
| Risk surface coverage | 0.80 | Return contract, callers, skills list, timeouts, overwrite, force and UI limits covered. |
| Recommendation actionability | 0.65 | Artifact and boundary named, but no specific resolution success criterion. |

## Result
Arithmetic mean: 0.70. ESCALATE under the confidence-below-0.85 rule. Card support verdict: PASS. No self-reported confidence was supplied or used. Installer early-return, dropped force intent, and discarded child stdout/stderr source claims were independently verified. No pytest pass or runtime cause was asserted.
