# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

- Role: independent fault-finder (sonnet class, agent a132c84bc6e265043), not an advocate. Full text: `debate/round2.5-fault-finder.md`.
- Inputs: diff-analysis.md, debate/round1-advocate-1.md, round1-advocate-2.md, round2-advocate-1.md, round2-advocate-2.md, variant-1-original.md, variant-2-original.md.
- Categories probed: state_variables, guard_conditions, count_divergence, collection_boundaries, interaction_effects, sufficiency_challenge.
- The last column is the orchestrator's verification after the probe (it re-read the cited lines).

| ID | Category | Assumption | Status | Severity | Evidence | Orchestrator check |
|----|----------|------------|--------|----------|----------|--------------------|
| INV-001 | state_variables | The C-001 fix (run `shadow_summary.py` inside this package) can satisfy "the owner has read it" after the go | UNADDRESSED | HIGH | source.md:3; PLAN:36; stage 2 PLAN:110 | holds: the regenerated summary must exist before the owner reads it and says go; folded into merged F1 |
| INV-002 | guard_conditions | A failed acceptance line halts and nothing alters the evidence file | UNADDRESSED | HIGH | sc-implement-protocol/SKILL.md:145 | partly handled: refs/qa.md:249 stops an "executor-invented approval" (E-NO-RULING); a fix pass editing a result file is not named; graded MEDIUM; folded into merged F1 and F3 as a "do not rewrite evidence" clause |
| INV-003 | collection_boundaries | The Task 3 gate can be passed on the seeded set | UNADDRESSED | HIGH | PLAN:33; stage 0 :106, :109 | holds: "the cosmetic block share falls" cannot hold when the old rule blocks 0 cosmetic items; folded into merged F3 |
| INV-004 | guard_conditions | Adding the registry test to PLAN:125 is enough | UNADDRESSED | MEDIUM | stage 1 :209, :213; PLAN:75-79, 87-91 | holds: Tasks 4 and 5 have no acceptance line that the row is `v2`; folded into merged F5 |
| INV-005 | sufficiency_challenge | U-006 is only under-specification | UNADDRESSED | MEDIUM | tests/skills/test_review_severity_rule.py:181-203; PLAN:122 | holds as a defect of Task 8's text; the executor can dispatch by registry state; kept minor in merged F9 |
| INV-006 | interaction_effects | `make sync-dev` makes the rule live | UNADDRESSED | MEDIUM | Makefile:108-130; pragmatic-subagent.js:7 | holds; folded into merged F4 |
| INV-007 | sufficiency_challenge | Tasks 4 to 7 cover the carriers' cap and fix-step edits | UNADDRESSED | MEDIUM | spec :866; rf-qa-qualitative.md:809, :994 | holds: spec :866 lists rf-qa-qualitative lines 110, 809, 994; Task 5 edits none; carried over from the base plan; merged F10 (non-blocking) |
| INV-008 | guard_conditions | The L2 helper can be called by the text that requires it | UNADDRESSED | MEDIUM | PLAN:45; stage 1 :171 | holds: Task 2 creates a module and a test only; merged F11 (non-blocking) |
| INV-009 | sufficiency_challenge | Tasks 8 and 9 re-run every test the edits can break | UNADDRESSED | MEDIUM | tests/skills/test_task_builder_merge.py:434-439; rf-qa.md:403, :405, :416 | holds: the pinned tokens sit in the Fix Cycle text Task 4 rewrites; the test is in neither re-run list; merged F12 (non-blocking) |
| INV-010 | state_variables | Task 1 tests the digest Task 3 ships | UNADDRESSED | MEDIUM | PLAN:33, :63 | holds, small; folded into merged F5 |
| INV-011 | guard_conditions | The answer key stays hidden | UNADDRESSED | MEDIUM | stage 0 :106, :111; PLAN:40 | minor: PLAN:40 already requires the key not be among the files given; not carried |
| INV-012 | collection_boundaries | Recall is computed on a clear unit | UNADDRESSED | MEDIUM | PLAN:33 | holds; folded into merged F3 |
| INV-013 | sufficiency_challenge | Task 11 states the baselines the window needs | UNADDRESSED | MEDIUM | spec :962, :989; stage 2 :110 | holds; folded into merged F7 |
| INV-014 | state_variables | The revert in PLAN:162 undoes the pilot | UNADDRESSED | MEDIUM | PLAN:162; spec :981 | holds; folded into merged F4 |
| INV-015 | count_divergence | The counts in the plan match the files | ADDRESSED | LOW | phrase scan (artifacts/phrase-scan.txt); rf-qa-qualitative.md:240-784 | counts hold |
| INV-016 | collection_boundaries | The Task 10 allow-list is always readable | UNADDRESSED | LOW | PLAN:149 | not carried (speculative about the executor's implementation) |
| INV-017 | guard_conditions | Task 1 does not decide whether the run proceeds | UNADDRESSED | LOW | PLAN:33, :36 | not carried (the go-before-result order is the source's own: source.md:3) |

## Summary

- **Total findings**: 17
- **ADDRESSED**: 1
- **UNADDRESSED**: 16
  - HIGH: 3 (INV-001, INV-002, INV-003)
  - MEDIUM: 11
  - LOW: 2
- Convergence rule: the 3 HIGH items block convergence until addressed. They are carried into the merged card (INV-001 into F1, INV-002 into F1 and F3 after being graded MEDIUM, INV-003 into F3), not accepted as risk.
