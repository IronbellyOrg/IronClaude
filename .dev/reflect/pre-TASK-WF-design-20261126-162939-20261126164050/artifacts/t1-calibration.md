# T1 calibration (blind calibrator, opus alias; calibrator_diversity: degraded, all three classes are reviewers)

Self-reported confidence on the card: 0.80. Calibrated C = 0.59 (delta -0.21). Below 0.85, so the rubric escalates (already escalated by rule 4 and the parse-density guard).

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.65 | F1 and F2 citations verify; three claims wrong (gap reading, task numbers in Recommendation 1, F3) |
| Coverage completeness | 0.60 | gap list exists, test-id coverage 0.9259, union figure too low because plan ranges were not expanded; Tasks 12-38 only checked structurally |
| Deviation-classification clarity | 0.30 | findings use Medium/Note labels, not the rubric's categories; the id gap is unclassified |
| Risk surface coverage | 0.75 | blast radius named; F1 breach also occurs in Tasks 21, 24, 29 (plan lines 252, 282, 334), not named |
| Recommendation actionability | 0.65 | Recommendations 1 and 2 name a file and a check but both checks have defects; Recommendation 3 is advice only |

Citations that did not verify (calibrator):
1. Recommendation 1 names "Tasks 3, 14 and 16"; the cited lines 172 and 193 are in Tasks 13 and 15, and Tasks 21, 24, 29 (lines 252, 282, 334) also carry the banned strings.
2. `artifacts/codegraph-grounding.md` lives in the plan package's artifacts folder, not in the reflect folder.
3. Task 12's "Depends on" line is at 154, not 152.
4. The plan cites most ids by range ("FR-110 to FR-118" at 200, "FR-120 to FR-126" at 220, "FR-054 to FR-067" at 334, "AC-01 to AC-21" at 431 and others); the first count did not expand them. Corrected by the orchestrator: union 170 of 199 named (0.8543), 29 not named (`coverage-pass2-ranges.json`).
5. F3 said the plan does not resolve O1; Tasks 12 (line 156) and 17 (line 213) write in the DD-11 reading; what is missing is the owner's confirmation.
6. Recommendation 2's check cannot pass as written: `dependency-check.txt` also has a `NO-DEP-ON-CREATOR` row for Task 20 and `vcs.py`.

Calibrator caveat: it did not count the 199 rows one by one and did not read the design's middle sections.
