# Blind calibration of the three reviewer cards (confidence-calibrator x3, run in parallel, model opus)
calibrator_diversity: degraded (reviewer classes sonnet, haiku, opus leave no disjoint class among the three aliases; opus chosen as highest capability)

| card | citation grounding | coverage completeness | classification clarity | risk surface | actionability | C |
|---|---|---|---|---|---|---|
| reviewer-1 (analyzer, agent aa94e2bb2767a6364) | 0.93 | 0.75 | 0.50 | 0.85 | 0.78 | 0.76 |
| reviewer-2 (qa, agent ad382bdb9dca9ce43) | 0.85 | 0.75 | 0.90 | 0.60 | 0.55 | 0.73 |
| reviewer-3 (refactorer, agent ae209fec1c0175562) | 0.92 | 0.85 | 0.72 | 0.80 | 0.60 | 0.78 |

Calibrator notes carried into Wave 4:
- reviewer-1 F6 (second half): the stale-docstring claim for collector.py:131 probably does not hold, because Task 5 removes :128-142 and keeps a two-line method (the plan's rewrite covers the docstring).
- reviewer-3 F2: overstated. tests/observe/test_adapter.py:174-175 already pins that run-use appears in adapter.py only inside the forbidden set, and plan:127 plus tests/observe/test_commands.py:727-728 pin the help sentence. The dropped git status --short scope check is a real gap.
- No card finding had an unconfirmed citation apart from reviewer-3 F2 "exactly 2 hits" (not checkable read-only) and reviewer-1's uncited "Not adopted" note.
