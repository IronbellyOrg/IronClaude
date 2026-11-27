# Calibration Report (Tier 1 card), saved by the orchestrator from the calibrator's returned text

**Card under calibration**: .dev/reflect/pre-issueSummary-20261126132809/t1-card.md
**Rubric**: reflection-rubric.md (five dimensions)
**Calibrator class**: sonnet alias (claude-gw-tier1b). Note: this is also the executor's class, so the executor / calibrator separation is degraded (see audit.log).

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.92 | Almost every spot-checked citation matches. C12 and C13 are INFERRED and carry anchors. C4's "17 passed" was not re-run by the calibrator (no execution tool) but source.md:37 reports the same figure. |
| Coverage completeness | 0.65 | Mechanical coverage 6 of 13 rows (0.4615). The card explains INF-001, 003, 005, 007 and 009 but never mentions INF-002 and INF-004, so "every unmapped row has coverage somewhere" is only partly shown. |
| Deviation-classification clarity | 0.40 | The card tags findings Grounded or INFERRED. That is an evidence label, not the deviation taxonomy. C8, C12 and C13 get no class. |
| Risk surface coverage | 0.78 | Primary risks covered (C2, C6, C7, C8, C12). Missing: import coupling of the new module to tests/skills/test_issue_protocol.py, and run non-determinism across the eight model runs. |
| Recommendation actionability | 0.35 | The card has no recommendations section; C7, C8, C12 and C13 imply plan edits without naming them. |

C = (0.92 + 0.65 + 0.40 + 0.78 + 0.35) / 5 = 0.62

Gated-minimum formula, claim-class cross-tab, structural C-rules and the troubleshoot escalation rubric: not applicable (reflect rubric).

## Spot-check notes (calibrator)

- C1, C2, C3, C7, C8, C10, C11: cited lines match (plan lines 29, 47, 85, 98, 159, 163, 180, 191; source.md:35, 43; refs/create.md:38, 86).
- C4: not independently re-run; corroborated by source.md:37.
- C5: scripts/create_issue.py is absent and origin_repo.py is present; the calibrator could not list the folder (Read cannot list directories), so "only three files" is partly verified. The orchestrator listed the folder earlier: clickup_claim.py, orca_worktree.py, origin_repo.py.
- C6: installed refs/create.md line 84 holds the old rule; src/ holds the new one at 84-86.
- C9: matrix values match artifacts/coverage-matrix.json. INF-002 and INF-004 are not discussed in the card.
- C12: comment blocks at templates/draft-notes.md lines 7 and 13 contain item-like text such as "Assumption: <text>"; Task 1 (plan line 33) only says the reader drops the empty marker.
- C13: plan line 171 says the issue text is quoted in ./source.md through the summary; source.md only paraphrases it, and accuracy-check.md and the analysis file it links to are not in the package folder.
- Independence weakness: the card was written by the same orchestrator that wrote the plan.

## Confidence

- Calibrated: 0.62. Below the 0.85 floor of the rubric guidance, so the rubric says ESCALATE. S_dev_density 0.5385 is above the 0.20 line (rule 5). The calibrator does not decide the verdict; section 5.3 of the protocol does, together with the table-wide parsed-sparse pre-filter.

C = 0.62
