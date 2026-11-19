# Calibration of reviewer-1-card.md (persisted by the parent from the confidence-calibrator agent's returned report)

Calibrator: confidence-calibrator on the sonnet alias (claude-gw-tier1b), disjoint from the reviewer classes (opus, haiku). It is also the executor's class, so the executor-vs-calibrator separation is not met.

| Dimension | Score | Why |
|---|---|---|
| Citation grounding | 0.95 | Every `file:line` opened matched. The two claims the card could not open or run are labelled: `[INFERRED]` for the `orca_worktree.py` flaw, and the old file is taken from the quoted diff. |
| Coverage completeness | 0.90 | All five spec requirements are mapped to the plan, the code and the test. The card did not run the install tests, so "stay green" rests on the plan and the recorded log. |
| Deviation-classification clarity | 0.75 | One severity per finding with a reason; the card never uses Aligned/Refinement/Drift/Regression labels. Few deviations, so little cost. |
| Risk surface coverage | 0.85 | Covers the import cycle, other callers of `_same_content`, the other installers, the test setup, the `IndexError` failure mode and the sibling flaw in `orca_worktree.py`. Does not mention other callers of `install_core_files` (`main.py:178` and `:365`, `tests/unit/test_cli_install.py:967`). |
| Recommendation actionability | 0.95 | One concrete assert line with its placement, the verification command, and a backlog issue naming three line numbers. |

Arithmetic mean: (0.95 + 0.90 + 0.75 + 0.85 + 0.95) / 5 = 0.88. Calibrated confidence: 0.88. The card states no numeric confidence, so there is no delta.

Citations: 21 checked, 0 failed. Not verified by the calibrator: the Grep claims ("no `_same_content` left", "no other callers") and the passing test run (it had Read only).

Escalation recommendation: STOP, reason none (C = 0.88 is at or above 0.85; scope 2 files, 2 domains; dev density about 0).
