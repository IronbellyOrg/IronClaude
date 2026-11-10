# Merge Log

## Metadata
- Base: Variant 1 (reviewer-1, sonnet/analyzer), adversarial/variant-1-original.md
- Executor: merge-executor (opus)
- Plan: adversarial/refactor-plan.md (12 planned changes, 2 rejected)
- Output: ../merged-verdict.md (verdict FAIL, merge_method adversarial, blocking_count 4, findings M-F1..M-F15)
- Changes applied: 12 of 12
- Status: complete, validation passed
- Timestamp: 2026-11-08T18:56:00Z

## Changes Applied

| # | Status | Before | After | Provenance |
|---|---|---|---|---|
| 1 | applied | R1-F1 fix: add test_routing_refresh.py and test_model_alias_policy.py to the run, choose allow-edit or blocked outcome, record in INSTALL.md | M-F1 fix: add "spec-panel-minfix" to `_POST_REFRESH_ADDITIONS` (comment naming #346), add the file to the plan:124 run and Task 5 files, rewrite plan:119 to allow this edit, flag to owner. test_model_alias_policy.py and the INSTALL.md note dropped (plan says "replace"). Claim and evidence extended with plan:119 / INV-001 and V3's comment lines 29-32 | R1-F1, R3-F1, INV-001; C-001, A-001 |
| 2 | applied | absent | M-F2 blocking: reviewer-side exit-2 retry missing from the shipped block; fix = one owner-decision sentence in the source.md:120 paragraph + pin; matrix credit noted as audit artifact error | R2-F1; Round 2 V2 (b), (d); C-002, A-002 |
| 3 | applied | absent | M-F3 blocking: review-3 escalation listing of budget escalations and GRADE-CONFLICT has no task; fix = sentence in the same paragraph + pin | INV-003; INF-032 |
| 4 | applied | absent (R3-F3 minor, [INFERRED]) | M-F4 blocking: .pyc from importlib trips the Task 4 grep; fix = `grep -rnI --exclude-dir=__pycache__`, optional `sys.dont_write_bytecode`, install-copy note | R3-F3; Round 2 V3 (a); INV-005, INV-006; C-009 |
| 5 | applied | R1-F2 fix: wc -l <= 500 AC + lint | M-F5: same AC plus "append the M-F2/M-F3 sentences inside existing paragraphs"; INV-002 evidence (Makefile:403, test.yml:133-135) appended | R1-F2, INV-002; C-004 |
| 6 | applied | absent | M-F11 minor: second exit 2 undefined; fix = handle it like exit 3 (stop and escalate) inside the M-F2 sentence | INV-004 |
| 7 | applied | R1-F6: two dropped items (40-char rule + skill-path pin) | M-F9: 40-character half only; skill-path half dropped (covered by plan:104); Round 2 V1 (b) evidence added | R1-F6; Round 2 V1 (b); C-012 |
| 8 | applied | R1-F7 evidence: plan lines 50 and 52 | M-F10: adds the column-0 anchor and `hash`-only subprocess evidence | R1-F7; Round 2 V1 (c); C-013 |
| 9 | applied | R2-F2: move checks to start of Task 1 | M-F12 minor: necessary but undeclared deviation; fix = declare it in Constraints | R2-F2 reframed; Round 2 V2 (c); C-003, X-001 |
| 10 | applied | R3-F2: path-order pin ambiguous + substring half | M-F13 minor: path-order half only; fix = scope to `## Fix Budget` with lookbehind; same for Task 4 (plan:103) | R3-F2; C-008 |
| 11 | applied | absent | M-F14 (probe fixtures) and M-F15 (write-verb audit; Task 4 does not run the test, plan:106) | R3-F4, R3-F5; Round 2 V3 (c); C-010, C-011 |
| 12 | applied | three separate self-audits and calibration blocks | one Self-Audit (verified / not verified / calibration notes); verdict FAIL; blocking_count 4; Not merged section lists X-002 and original C-003 | all self-audits; INV-006, INV-007, INV-008 |

Base findings carried unchanged (no plan change): R1-F3 -> M-F6, R1-F4 -> M-F7, R1-F5 -> M-F8.

## Post-Merge Validation

### Structural integrity
- Heading levels: `## Merged card` -> `### Findings`, `### Self-Audit`, `### Not merged`. No level gaps; the top level is `##`, matching the base card.
- Findings ordered as instructed: blocking M-F1..M-F4, then minors M-F5..M-F15. 15 findings, 4 graded blocking, matching `blocking_count: 4`.
- Every finding keeps the base field shape (id, grade, class, claim, evidence, tag, fix) plus `sources:`, and has a provenance comment above it.

### Internal references
- M-F ids: 15 defined (M-F1..M-F15); every cross-reference (M-F2 from M-F3, M-F5, M-F11; M-F12 and M-F15 from Self-Audit and Not merged) resolves to a defined id.
- file:line and "plan line(s) N" citations: total 52, resolved 52, broken 0. Each was checked by exact-string match against the concatenated inputs (variants 1-3, invariant-probe.md, round2-v1..v3.md, refactor-plan.md). The extractor also caught the merge timestamp, which is not a citation and is excluded from the count.
- Quoted evidence strings were copied from the sources; no new citation was introduced.

### Contradiction re-scan
- No new contradiction introduced by the merge.
- Carried, not introduced: M-F13 is graded minor while its claim says the whole-file reading of the plan:122 pin fails. The grade comes from debate C-008 (include-minor) and the fix removes the failing reading, so it is an ambiguity rather than an unpassable check; left as planned.
- Carried, not introduced: Change #10 applies the scoped check to Task 4 (plan:103), but R3-F2's Task 4 point was the substring half the plan dropped. Applied as the plan states; the orchestrator may want to confirm that clause.
- M-F5 says the variant lands at exactly 500 lines; the limit fails only above 500 (`-gt 500`), so the minor grade is consistent.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 12 | 12 | 0 | 0 |

Rejected by the plan and recorded under Not merged: X-002; C-003 as originally framed.
