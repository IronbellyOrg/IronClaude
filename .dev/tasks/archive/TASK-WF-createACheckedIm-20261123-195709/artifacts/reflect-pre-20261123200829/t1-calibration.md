# Calibration Report

**Card under calibration**: ./t1-card.md
**Rubric**: /home/coder/.claude/skills/sc-reflect-protocol/refs/reflection-rubric.md
**Card tier**: 1

## Per-dimension scores

| Dimension | Score | Independent justification |
|---|---:|---|
| Citation grounding | 0.85 | Source claims verified by locating and Reading named symbols; card lacks line-number citations and relies on the coverage receipt for some claims. |
| Coverage completeness | 0.55 | Literal union coverage 0.5 is below the rubric floor; explicit gaps and matching scope Constraints prevent an even lower score, but semantic coverage cannot replace algorithm output. |
| Deviation-classification clarity | 0.35 | Six lexical gaps and three candidates are deferred to Tier 2 without deviation categories. |
| Risk surface coverage | 0.85 | Parser, correct red failures, inline custom, historical status and registration scope are addressed; other untouched mentions are not explicit in the card. |
| Recommendation actionability | 0.80 | Concrete Tier 2 adjudication targets, but no invocation target or exact success criterion. |

## Confidence

Independent requested opus-class calibrator; no numeric self-reported confidence inherited. Five-dimension arithmetic mean: (0.85 + 0.55 + 0.35 + 0.85 + 0.80) / 5 = **0.68**. The troubleshoot six-dimension gated-minimum formula was not applied.

## Escalation recommendation

ESCALATE to Tier 2: confidence <0.85; independently, S_dev_density=0.5 exceeds 0.20 and inferred requirements outnumber parsed rows. This does not authorize implementation.

## Notes

Calibrator independently Read commands.py help blocks, public registrations, preflight field gate, schema inline-custom allowance, docs field note, coverage receipt and task plan. No spot-check mismatch or remote URL. Card had no frontmatter, which is not required by the supplied reflection rubric; no runtime check was inferred. No tests, commands or files were written by the calibrator. Requested model class differs from the coverage analyst's requested sonnet; actual executor and gateway identities are not proven. The calibrated score measures the initial reflection card, not a 68% probability that the plan or proposed product fix is correct.
