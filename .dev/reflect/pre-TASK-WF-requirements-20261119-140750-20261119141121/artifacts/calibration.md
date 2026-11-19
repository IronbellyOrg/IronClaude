# Blind calibration of the reviewer cards (confidence-calibrator, sonnet class, one instance per card)

Calibrator class sonnet equals reviewer 1's class (card 1); calibrator_diversity: degraded (all three model classes are used by reviewers).

| Card | Reviewer | Calibrated confidence | Dimensions (citation, coverage, classification, risk, actionability) | Calibrator note |
|---|---|---|---|---|
| reviewer-1-card.md | analyzer, sonnet | 0.80 | 0.75, 0.85, 0.85, 0.80, 0.75 | STOP. Two spot-check paths used the wrong directory (`issue_pipeline/cycle.py` does not exist; the card means `issue_watch/cycle.py`), so grounding was held below 0.85. |
| reviewer-2-card.md | qa, haiku | 0.79 | 0.85, 0.85, 0.60, 0.75, 0.90 | Do not escalate. Accept findings, but fix the severity grades in the merge: QA-1 to QA-3 are labelled Blocking while the card's own severity column says MEDIUM. |
| reviewer-3-card.md | refactorer, opus | 0.88 | 0.85, 0.90, 0.90, 0.85, 0.90 | Accept. Confirm B-1's `REPO` hard-wire (card cites only `github.py:37`). |

Orchestrator check of the two items the calibrators could not confirm: see `artifacts/orchestrator-checks.md`.
