# Wave 3C blind calibration of the Tier 2 cards (confidence-calibrator x3, class opus, card-only input with persona/model header and self-report stripped)

calibrator_model_class: opus. Reviewer classes: sonnet, haiku, opus. Disjoint set is empty (only Anthropic aliases): calibrator_diversity degraded (class used by one reviewer, highest capability; same class as reviewer 3).

| Card | Reviewer | Card score | Per finding |
|---|---|---|---|
| 1 | analyzer / sonnet | 0.65 | F1 0.80, F2 0.55, F3 0.75 |
| 2 | qa / haiku | 0.72 | F1 0.35, F2 0.55, F3 0.40, F4 0.70, F5 0.65, F6 0.50, F7 0.70, F8 0.60, F9 0.70, F10 0.55, F11 0.55, F12 0.40 |
| 3 | refactorer / opus | 0.66 | F1 0.85, F2 0.70, F3 0.45, F4 0.55 |

All three: escalate (score < 0.85). Calibrator notes: card 2 F1/F2/F3 overstated (plan:124 does specify the one retry; F3 "no mechanism" wrong); card 1 F2 partly holds (spec:107 makes per-cycle applied_edits deliberate; scenario needs a cycle after a held push); card 3 F3/F4 overread plan wording.
