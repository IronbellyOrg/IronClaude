# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis

The first fault-finder agent stopped at its 50-turn limit with no findings (recorded as an agent failure, retried once per the error matrix). The retry (a fresh read-only agent with a 22-call budget) produced the table below. Orchestrator re-checks are noted under the table.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | No test is left red by the template and prompt edits | ADDRESSED | LOW | `tests/skills/test_review_severity_rule.py:181-203` pins S1 to S3 and S5 of all ten files; S3 Task 11 (S3:218) dispatches those pins by registry state; P4 Task 5 (P4:120) runs the test; the fixtures hold no row with the P4 target strings (NO LENIENCY, "close enough", "When in doubt", "follow-up candidates", "once per loop", merge phrases) |
| INV-002 | count_divergence | The quoted counts match the live files | ADDRESSED | LOW | HALT 2/5/6 (P4:45), cap 5/6/1/2 (P4:80), `NO LENIENCY` on lines 95, 96, 100 of `agent_template_qa.md`; the old sentence is in exactly 11 `src` files (4 templates, 4 prompts, `rf-qa.md`, `rf-qa-qualitative.md`, `pragmatic.md`) |
| INV-003 | guard_conditions | The doubt-line wording in Constraints can be copied and still pass the Task 2 grep | UNADDRESSED | MEDIUM | P4:25 "no item fails a review for being close enough or probably fine" against P4:65 "`grep -c -iE 'close enough\|probably what was intended\|almost right'` ... print 0"; a verbatim copy prints 1 |
| INV-004 | sufficiency_challenge | The Task 5 pinning run covers the Constraint that no softening token enters Task 1 and Task 2 text | UNADDRESSED | MEDIUM (probe grade) | P4:25 names `tests/audit/test_severity_floor_unweakened.py`; the 14-file list at P4:120 holds no `tests/audit` file; the probe did not check whether other tests pin the template PASS/FAIL bullets |
| INV-005 | interaction_effects | Strict T2 passes on `doctor.py` and the skill folder | ADDRESSED | LOW | no old-sentence copy in `src/superclaude/cli`; S1:52 greps the skill folder; S1:234 names `STRICT_T2` (so P4:114 "did not name the switch" is stale); case (b) needs a `strict` parameter or a monkeypatch of the constant |
| INV-006 | interaction_effects | Task 3's folder-wide grep can reach nothing | ADDRESSED | LOW | the grep over the four skill folders hits only the six lines Task 3 edits; Task 2's `cp` is in the same task as the source edit (P4:61) |
| INV-007 | collection_boundaries | The stage 3 `Kept mechanical gates` section exists when Task 1 needs it | UNADDRESSED | LOW | P4:48 accepts a remaining "Any CRITICAL or IMPORTANT issue exists" line if listed in `refs/scale-map.md`; the section is created in stage 3 only on a first keep (S3:162, S3:182); P4 does not say to create it |
| INV-008 | sufficiency_challenge | P4 as written can be run to a passing Task 5 and Task 6 with no blocking defect | ADDRESSED | LOW | falsifying conditions named: (a) stage 3's registry-state dispatch mis-handles rows flipped one at a time (caught by Task 5's run), (b) the owner-go cell or the stage 3 `FINAL: pass` line is not true (the run halts cleanly), (c) an unlisted test pins template text (INV-004) |

### Orchestrator re-checks

- INV-004: `grep -rn -E "Any CRITICAL or IMPORTANT issue|No CRITICAL or IMPORTANT issues|Report honestly|NO LENIENCY" tests` printed nothing, and the test files that name the template and prompt carriers are `test_review_severity_rule.py`, `test_review_prompt_overrides.py`, `tests/unit/test_cli_install.py` (a file-name inventory) and the two fixture tables; `test_severity_floor_unweakened.py` scans only the `rf-qa-qualitative.md` Critical Rules block, which no P4 task edits. The softening-token sentence in P4:25 is therefore harmless but also unnecessary for these files. Re-graded LOW (no gap in what the plan ships).
- INV-003 repeats debate point C-002; the probe's MEDIUM grade is adopted in the merged card (two parts of the same plan contradict each other).

## Summary

- Total findings: 8
- ADDRESSED: 5
- UNADDRESSED: 3
  - HIGH: 0
  - MEDIUM: 2 (INV-003, INV-004; INV-004 re-graded LOW after re-check)
  - LOW: 1 (INV-007)
- Gate result: count(HIGH + UNADDRESSED) = 0, so convergence is NOT blocked. MEDIUM items are logged as warnings.
