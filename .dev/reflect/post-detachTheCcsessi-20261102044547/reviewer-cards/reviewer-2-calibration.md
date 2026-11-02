# Reviewer 2 calibration (confidence-calibrator, model class opus; persisted on receipt 2026-11-02T05:22Z)

Calibrated C = 0.76 (self-report 0.86).

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.80 | 23 of 24 held; R2-F1's "no artifact documents the guard" is contradicted by the inline comment at local-gateway-alias-proxy.py:859-862 |
| Coverage completeness | 0.90 | all 13 AC and all changed regions mapped; hunk list from tasklist-diff-map.md (disclosed G1) |
| Deviation-classification clarity | 0.55 | 2 of 4 findings contradict the taxonomy's own signals (R2-F1, R2-F2) |
| Risk surface coverage | 0.80 | process-group regression check, untested tty branch, bash/CHANGELOG verification gaps covered; missed macOS/bash 3.2 not exercised (plan:21) and running shims stay exposed until restarted |
| Recommendation actionability | 0.75 | CHANGELOG rewording concrete; "record the guard's justification" targets something already written; R2-F2/F3 have no success criterion |

Not held: R2-F1 "no artifact documents" the guard (comment at :859-862). Partly held: "plan mandates unconditional setsid" (plan:52 names no condition; "unconditional" is not in the plan text).
Held (23): proxy:863-867; plan:52; remediation-source.md:12; ccsession:808; test:598, 1536, 1538, 1510-1516, 1512, 1540-1543, 1052, 575-615, 612-615; CHANGELOG.md:9, 11, 24; t1-before.log:15-20, 22-23, 29-38, 40-41; t5-checks.log:11, 23-30, 31-40; after.txt:2-5.

Misclassifications:
- R2-F1 → necessary, LOW (inline rationale present; no AC contradicted; both plan start paths are non-terminal and call setsid). Sub-points stand as a documentation note: tty branch untested; CHANGELOG.md:11 overstates.
- R2-F2 → necessary at most (lines belong to Task 1's own test; commented at :1513, :1538; serves plan:15 goal; timeout=30 matches join(30) at :1534).
- R2-F3 drift (LOW) defensible. R2-F4 necessary holds (t5-checks.log:31).

Side note: refs/reflection-rubric.md dimension-3 class list disagrees with refs/deviation-taxonomy.md.
