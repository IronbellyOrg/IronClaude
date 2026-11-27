# Calibration of reviewer 2 card, second review (saved by the orchestrator from the calibrator's returned text)

Calibrator class: sonnet alias (disjoint from the reviewer classes haiku and opus; the same class as the executor).

Citation spot-check: the decisive citation of each of the 22 rows was read and matched (plan, source.md, refs/create.md, templates/draft-notes.md, SKILL.md, refs/claim.md, templates/launch-prompt.md, origin_repo.py:156-174, issue-worker-t3.md:33, CLAUDE.md:37, Makefile:13-15, the contract3 workflow file, the installed refs/create.md:84), plus a sample of secondary citations. No mismatch. Two things the calibrator could not verify: the INF-row matrix the card audits, and whether origin/integration has moved on the three AC4 files.

Blocking rows (does the cited evidence support the claim): row 1 supported (conditional on the dry run using the real home; a plan gap; blocking is defensible for a safety issue); row 2 supported (depends on a later integration commit touching those files, which the card could not check; the logic is sound and the plan fixed the same mistake for R-023); row 3 supported and the strongest of the four (plan:76 and plan:81 conflict as described); row 4 supported factually, blocking severity arguable (the scan task precedes any end-of-run staging).

| Dimension | Score |
|---|---|
| Citation grounding | 0.95 |
| Coverage completeness | 0.92 |
| Deviation-classification clarity | 0.78 |
| Risk surface coverage | 0.93 |
| Recommendation actionability | 0.70 |

C = (0.95 + 0.92 + 0.78 + 0.93 + 0.70) / 5 = 0.856, rounded 0.86 (above the 0.85 medium-confidence floor, below the 0.90 ceiling).

Weak points noted by the calibrator: "14 fully adherent" has no per-unit evidence; R-003 is listed adherent although finding 1 cites it as a forbidden outcome; only about 7 of 22 rows give an explicit fix.
