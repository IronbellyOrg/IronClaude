# Evidence Validation Report (B): REPORT.md

Saved by the orchestrator from the validator's returned report (evidence-validator agent, sonnet class, read-only). The per-row verdict table is condensed.

Total citations: 46 (24 INF rows, 22 other file:line citations)
Verified: 46
Dropped: 0
Suggested report status: success

All 24 INF quotes occur verbatim in their cited source.md lines (longest INF-001 about 146 characters and INF-004 about 145; all at most 150). The 22 other citations (PLAN:24, 53, 62, 65, 72, 78, 87, 110, 115, 134, 146, 148, 157-165, 169, 171, 209; source.md:17; README.md:33; stage3-request.md:14; SPEC:404, 740, 945) were re-read and verified. The manual-mapping plan lines in the INF table (PLAN:19-27, 36-37, 46, 49, 59, 66, 84, 96-100, 212, 221-226) each hold the content the row says.

## Dropped citations

none

## Statement checks

- (a) Findings F1 to F9 agree in grade and subject with merged-review-card.md (F1 and F2 blocking; F3 to F9 non-blocking; F4 dissent and F9 "T1 only, not debated" match the card).
- (b) Verdict and Tier numbers agree with tier_decision.yaml (tier 2, rule 4, S_dev_density 0.3333, C 0.71, coverage_pct_union 0.6667, parsed 0 / inferred 24), reviewer-calibration.yaml (0.77, 0.75, 0.76; OpenAI identity mismatch for reviewer 2) and t1-calibration.yaml (0.71); "16 of 16, 13 unanimous, 3 by 2 of 3" agrees with convergence-tracking.tsv (16 data rows; majority rows C-004, C-008, X-001); "matched 16 of 24" is correct.
- (c) Every file named in Recommendations exists and each plan line named holds what the recommendation says (PLAN:53, 72, 78, 110, 134, 146, 157-165, 169; stage3-request.md:14). SPEC:740 files the stoprule and finding-grader rows as installed-only and says align or retire is OD10. PLAN:171's lint/estimate point was not independently checked by this validator (validator A's glob confirms it).

## Notes

- The front matter `confidence_calibrated: 0.76` is the mean (and median) of the three reviewer calibrations, not the T1 card's 0.71 in tier_decision.yaml; label the field.
- INF-020's manual note says the end point was "applied once (PLAN:65)"; PLAN:65 says "until the stage 4 package", not "until Task N": still an end point, wording looser than the rule.
- R-001 names classifier_inputs.py, classify_cmd.py and safety_route.py, which do not exist yet (Tasks 10, 12 and 13 create them); expected, the recommendation refers to planned files.
- The front-matter citation total was an upstream count the validator did not reproduce; the Run notes (35-file tree hash and similar) were not verified by the validator.
- Strict cases checked: the longest quotes against the 150-character cap, the trailing `\.dev/` in INF-013, and "task skill" in INF-022; all hold.
