# Invariant Probe Results

| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | state_variables | Only owner words set AGREED | UNADDRESSED | HIGH | issue-summary.md lines 58-59, 69: numbers are a relayed proposal, not Clay's words; variant-A.md section 4 item 1 needs owner words; line 89 never says who may mark AGREED |
| INV-002 | state_variables | Stored table answers are frozen | UNADDRESSED | HIGH | No hash list holds `table-answers.jsonl` (variant-A.md section 4 item 5, variant-B.md NFR-007); RUN_INVALID covers hashed files only |
| INV-003 | state_variables | Sign-test scorer is pinned and tested | UNADDRESSED | HIGH | variant-A.md NFR-004 hashes runner, not scorer; variant-B.md NFR-007 pins by commit, but section 5 leaves folder maybe uncommitted |
| INV-004 | state_variables | Spend and attempt counters survive a crash or new run id | UNADDRESSED | MEDIUM | variant-B.md NFR-008 gives reruns new run ids; cap is per experiment (variant-C.md cost cap); no carry-over |
| INV-005 | count_divergence | "Rerun" has one meaning | UNADDRESSED | MEDIUM | Per-prompt (issue-summary.md line 79) versus whole-run (variant-A.md NFR-005, variant-B.md NFR-008) |
| INV-006 | guard_conditions | Sign test with b+c = 0 or c at least b | ADDRESSED | LOW | issue-summary.md line 77 integer form: b+c = 0 gives 20 < 1, false; no tie possible at 0.05. No test for b+c = 0 (variant-A.md T-10) |
| INV-007 | guard_conditions | Rerun succeeds after timeout | ADDRESSED | LOW | issue-summary.md line 80: rerun answer scored, timeout counts 10 s in slowest, so 5 s limit fails |
| INV-008 | guard_conditions | No prompt appears twice | UNADDRESSED | MEDIUM | variant-B.md FR-001, T-01 reject duplicate ids only; same text under two ids counts twice in b or c |
| INV-009 | guard_conditions | Noul at exactly 0.3 or 0.7 fixed before AGREED | UNADDRESSED | MEDIUM | Required by variant-B.md gate step 2, variant-A.md FR-014; rule block (issue-summary.md lines 85-89) lacks it |
| INV-010 | count_divergence | One median population and definition | UNADDRESSED | MEDIUM | issue-summary.md line 80 drops twice-failed prompts; r2-advocate-C.md rejects imputing 10 s; even-count median unstated (variant-A.md T-06) |
| INV-011 | count_divergence | About 30 prompts; no swap after freezing | UNADDRESSED | MEDIUM | variant-B.md FR-002 passes 8 prompts; variant-A.md NFR-002 swap breaks FR-002 once table answers exist |
| INV-012 | collection_boundaries | Real ambiguous and none-fit public prompts exist | UNADDRESSED | MEDIUM | diff-analysis.md A-001 has no fallback; r1-advocate-A.md forbids padding; no verdict state for a blocked corpus |
| INV-013 | interaction_effects | One agent may label and apply the table | UNADDRESSED | HIGH | Labels freeze first, so variant-A.md FR-004 and FR-011 cannot both hold for one person (section 8 open); a model reading prose is not "as written" (FR-008) |
| INV-014 | interaction_effects | "Ambiguous" fits the label basis | UNADDRESSED | HIGH | variant-A.md FR-003 basis is the public fix, naming one type; "ambiguous" then comes from text, the table's own rule (FR-010); unset-is-right (issue-summary.md line 85) makes these favour the table |
| INV-015 | interaction_effects | One gate fits both orderings | UNADDRESSED | MEDIUM | variant-B.md gate step 4 needs table answers stored; r2-advocate-B.md section 1 defers table until AGREED; needs two gates |
| INV-016 | interaction_effects | Seen-by-table prompts do not tilt verdict | UNADDRESSED | MEDIUM | variant-A.md FR-005 split is report only; rule (issue-summary.md lines 86-88) scores all prompts |
| INV-017 | sufficiency_challenge | Systemic failure is not a Jev loss | UNADDRESSED | HIGH | issue-summary.md line 88 makes errors "not clearly"; variant-B.md section 4 run-incomplete was dropped. An outage closes 612 on no evidence |
| INV-018 | sufficiency_challenge | Each gate input passes | UNADDRESSED | MEDIUM | None shown: no corpus or labels (variant-B.md FR-002); AGREED fails (issue-summary.md line 83); table method open (variant-A.md FR-009); price unverified (NFR-001); response contract unverified (diff-analysis.md A-002) |

## Summary

- Total findings: 18
- ADDRESSED: 2; UNADDRESSED: 16
- UNADDRESSED by severity: HIGH 6 (INV-001, 002, 003, 013, 014, 017); MEDIUM 10; LOW 0
