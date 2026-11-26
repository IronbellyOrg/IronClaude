# Calibration of reviewer 2 card (saved by the orchestrator from the calibrator's returned text)

Calibrator class: sonnet alias (disjoint from the reviewer classes haiku and opus; the same class as the executor, so executor/calibrator separation is degraded).

Spot-check: the calibrator read the decisive citation of every one of the 18 rows (plan, source.md, accuracy-check.md, analyze-sc-issue-protocol.md, CLAUDE.md:37, .gitignore:85, refs/create.md, draft-notes.md, the contract3 workflow file, test_issue_protocol.py) and found all matching, with one small slip: row 14 cites the installed refs/create.md at line 82, but the old rule text is at line 84 and line 82 is only the heading.

Not independently verified by the calibrator: helper lines test_issue_protocol.py:33-34, 115, 123; tests/__init__.py; artifacts/coverage-matrix.json figures; the card's claims about unread user config (git credential helper, MCP), which the card itself marks unverified.

Blocking rows (calibrator's view of whether the cited evidence supports the claim): row 1 supported (consequence slightly strong: the plan's paraphrase is close for AC1 to AC3; the AC4 citation-list gap is real); row 2 supported (the plan records the issue-create count at plan:128 but nothing makes a wrong count fail); row 3 supported; row 4 supported (a scenario test is not a "static wording test", so it could still pass the Task 9 guard); row 5 supported (Blocking vs Medium is a judgement call); row 6 supported as a plan gap (the mechanism covers gh only; staging of raw logs confirmed by CLAUDE.md:37 and .gitignore:85; actual write capability through git credentials or MCP not verified).

| Dimension | Score |
|---|---|
| Citation grounding | 0.92 |
| Coverage completeness | 0.90 |
| Deviation-classification clarity | 0.80 |
| Risk surface coverage | 0.85 |
| Recommendation actionability | 0.78 |

C = (0.92 + 0.90 + 0.80 + 0.85 + 0.78) / 5 = 0.85 (at the rubric's medium-confidence floor).
