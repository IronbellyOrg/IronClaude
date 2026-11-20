# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Independent probe of the emerging consensus (17 confirmed findings, 1 dropped, verdict FAIL) against the 6-category checklist. Consensus input: both cards, both calibrations, the T1 calibration, and the verification reads of the plan, runbook, source and orca_worktree.py.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The consensus assumes the state file (/tmp/ob/state.env, plan:35) can record whether session E set `extensions.worktreeConfig` so cleanup step 3 can undo exactly what the run set | ADDRESSED | HIGH | R1-F02 merged row requires the state key; runbook:669 sets the flag conditionally and runbook:806 is the only scripted undo |
| INV-002 | state_variables | The consensus assumes the baseline files survive until the plan:263 diff is run; in the plan step 7 (plan:208, runbook:830) deletes /tmp/ob which holds them (runbook:833) | ADDRESSED | HIGH | R1-F03 merged row requires cleanup.sh to print the diff before step 7 |
| INV-003 | guard_conditions | The consensus assumes each `send` can distinguish a fresh `Blocked:` line from a stale one; the plan (70-75) has no per-send baseline for the screen scan | ADDRESSED | HIGH | R1-F01 confirmed blocking; Stop-event count is baselined (plan:71) but the Blocked scan is not |
| INV-004 | guard_conditions | The consensus assumes the push-URL assertion runs inline before the push prompt, not only in the self-test | ADDRESSED | MEDIUM | R1-F06 recommendation makes it inline; plan:159 only self-tests it |
| INV-005 | count_divergence | The consensus assumes the Stop-event count baseline (plan:71) and the item-5 typed-prompt count (runbook:322) stay consistent when notices interleave with typed prompts | ADDRESSED | HIGH | QA-1 confirmed blocking: no wait condition reaches the background-completion notice |
| INV-006 | collection_boundaries | The consensus assumes a missing or empty results file is handled at every governed subcommand entry, including `c` | ADDRESSED | MEDIUM | QA-2 merged row (downgraded minor) requires the entry check for every subcommand; plan:156 covers b, d, e only |
| INV-007 | collection_boundaries | The consensus assumes the 12-block results file exists on a gated-out run (sessions skipped); plan:250 requires 12 blocks regardless | ADDRESSED | MEDIUM | QA-3 confirmed blocking: gated skips have no valid outcome path in Task 10/11 ACs |
| INV-008 | interaction_effects | The consensus combines fixes from both cards; no two recommendations conflict (driver subcommand addition in F07 vs stop-condition change in F01/QA-1 touch the same file but different functions) | ADDRESSED | LOW | refactor-plan.md change list; no overlapping edits |
| INV-009 | interaction_effects | The consensus assumes staging (plan:259) and the secret scan (plan:185) interact safely; screens capture everything the observed agent printed and the scan has 4 patterns | ADDRESSED | HIGH | R1-F12 raised to blocking; scan widening + owner review required |
| INV-010 | sufficiency_challenge | Claim under probe: "fixing the confirmed findings makes the plan executable". Downstream condition that would falsify it: an unreviewed defect outside both cards' coverage surfaces (calibrations list: Task 8 `--force` rule plan:205, `--delete-branch` ordering plan:206, `git branch -D` runbook:823, session d's 90-minute in-script wait vs the timeout constraint plan:26/145). Named condition: if the `--force` heuristic at plan:205 ("nothing but files the run created") misjudges a worktree with pre-existing dirt, cleanup destroys another session's work | UNADDRESSED | MEDIUM | Not covered by either card; flagged into refactor-plan.md as a pre-execution review item. MEDIUM does not block convergence. |
| INV-011 | sufficiency_challenge | For each filter/gate between fix site and assertion site: the dialog-answer path (F07 fix) must pass the driver's marker refusal (plan:81) and the run-log recording (plan:245); an `answer` subcommand sharing the send path satisfies both | ADDRESSED | LOW | R1-F07 recommendation specifies shared refusal + logging |

## Summary

- **Total findings**: 11
- **ADDRESSED**: 10
- **UNADDRESSED**: 1
  - HIGH: 0
  - MEDIUM: 1 (INV-010 — cleanup `--force`/`--delete-branch`/`branch -D` destructive-path review not covered by either card)
  - LOW: 0

Convergence gate: no HIGH-severity UNADDRESSED invariants; convergence is not blocked. INV-010 is carried into the refactor plan as a pre-execution review item.
