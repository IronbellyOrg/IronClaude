# Calibration of reviewer 1 card, second review (saved by the orchestrator from the calibrator's returned text)

Calibrator class: sonnet alias (disjoint from the reviewer classes haiku and opus; the same class as the executor).

Citation spot-check: every cited line was read and matched (plan lines 96-109, 142-150, 191, 195, 203, 205, 212, 234, 239; source.md lines 58, 65, 71; refs/create.md:99). All three findings are supported by what the cited lines say. Judgement notes: finding 3 is a real gap but the plan cannot open the pull request itself (the story agent does), so "blocking" is arguable and a handoff requirement is the fair fix; finding 2 holds (the dry-run excerpt is a model-run output, so it falls under "every run output").

| Dimension | Score |
|---|---|
| Citation grounding | 0.95 |
| Coverage completeness | 0.90 |
| Deviation-classification clarity | 0.70 |
| Risk surface coverage | 0.60 |
| Recommendation actionability | 0.60 |

C = (0.95 + 0.90 + 0.70 + 0.60 + 0.60) / 5 = 0.75

Score drivers: a Regression label on a pure plan omission, no stated fixes with success criteria, no plan-level risk register, the unauthenticated criterion quotations, and the card being a reconstruction ("saved in substance by the orchestrator").
