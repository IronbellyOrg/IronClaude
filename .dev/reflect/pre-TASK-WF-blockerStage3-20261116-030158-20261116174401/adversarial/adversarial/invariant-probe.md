# Invariant Probe Results

## Round 2.5: Fault-finder analysis (sonnet class, agent aa5e506907ac92efe; read-only, persisted by the orchestrator)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Rewriting the Task 5 acceptance lines is enough to make the seeded-recall gate sound | UNADDRESSED | HIGH | SKILL.md:131 "Q1 EXEC" before :140 "Q3 REVIEW"; Q5 has no legal fix (PLAN:21); retry.md:109 "nothing has been reverted"; retry.md:158 "the A5 tree stays"; qa.md:248 ruling completes Task 5 with the edit kept. Only a check-only task before Task 5 breaks it |
| INV-002 | guard_conditions | PLAN:94's ruling rule is what lets Task 5 proceed | UNADDRESSED | MEDIUM | qa.md:254 "A clear user confirmation in the current conversation is sufficient"; the protocol Ruling needs no SHA-256 |
| INV-003 | collection_boundaries | The "with and without that reviewer" recall variants are computable | UNADDRESSED | HIGH | PLAN:80 "at least 2 of the 3"; with one reviewer dropped the rule is 2 of 2; with two dropped it cannot be met, so recall is 0 and R1b fails by construction |
| INV-004 | collection_boundaries | An empty confirmation file gives "safety misses 0"; one gate gives a usable RT5 threshold | UNADDRESSED | MEDIUM | PLAN:39 "an empty file means none was confirmed"; S2:138 defines "not computable" only for a missing file; S2:141 has no empty-file case |
| INV-005 | count_divergence | Task 2 supplies every baseline Task 13 quotes | UNADDRESSED | MEDIUM | PLAN:230 quotes 8 metrics; Task 2 counts 3; M6, M9 and M11 baselines exist (S2:138, SPEC:970, SPEC:973) |
| INV-006 | count_divergence | "all 13 lines in 10 files" (OD11) is met | UNADDRESSED | LOW | PLAN:22 vs the two exempt lines in skills/task/SKILL.md (PLAN:23); counts 13, 11, 161, 139 verified sound |
| INV-007 | interaction_effects | L3 text beside the cap sentence leaves the Task 10 fixture rows true | UNADDRESSED | MEDIUM | fixture lines 29 and 45 end "...open blocking findings."; test_review_severity_rule.py:256 fails a row when its `new` is not in the text; PLAN:196 allows fixture edits only for digest or cadence rows |
| INV-008 | interaction_effects | Re-pinning Rule 6 and the block hash (Task 11) is enough | UNADDRESSED | MEDIUM | test_severity_floor_unweakened.py:197 SOFTENING_TOKENS include "typically"; rule 9 at rf-qa-qualitative.md:993 sits inside the hashed block |
| INV-009 | interaction_effects | Recording kept gates in refs/scale-map.md is harmless to the stage 1 and Task 12 checks | UNADDRESSED | MEDIUM | S1:74 "prints nothing" path check; PLAN:140 and :154 name no section or row format |
| INV-010 | guard_conditions | The CLI named in the new fix-cycle text exists wherever the installed agent runs | UNADDRESSED | MEDIUM | PLAN:140 "superclaude review fixcheck"; the stage 2 paragraph (S2:72) has a "missing `superclaude` command" clause, the L2 text has none |
| INV-011 | state_variables | The old-arm text read "at run time" is old | UNADDRESSED | MEDIUM | PLAN:76 reads live pragmatic.md; Task 5 edits it; a halt leaves the edit (retry.md:158) |
| INV-012 | guard_conditions | The ledger row can hold what Tasks 1, 3 and 5 read from it | UNADDRESSED | MEDIUM | README:15 has one column "Owner go (date, where)"; PLAN:39 and PLAN:94 need a date, a folder list, a file path, a line id and a SHA-256 |
| INV-013 | sufficiency_challenge | The consensus verdict NEEDS-REVISION is sufficient | UNADDRESSED | MEDIUM | the fix list is incomplete without INV-001, INV-003, INV-007, INV-008; no defect found in the floor-slice test, the plugin scan or tests/review/test_review_cli.py |

## Summary

- **Total findings**: 13
- **ADDRESSED**: 0
- **UNADDRESSED**: 13
  - HIGH: 2 (INV-001, INV-003)
  - MEDIUM: 10
  - LOW: 1

Treatment at depth standard (no Round 3): both HIGH items are carried into the merged card as blocking findings (F1 and F2) instead of being debated again; the MEDIUM items are carried as non-blocking findings or follow-up candidates. Convergence is reported as BLOCKED_BY_INVARIANTS until the merge, then resolved by inclusion; `unaddressed_invariants` in the return contract lists INV-001 and INV-003.
