# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis (one agent, opus class; read the plan, the spec and the code they name)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Reusing `_repo_scoped` alone resolves the Task 7 conflict | UNADDRESSED | HIGH | Plan line 113 has a second, runtime clause (the recorded fake-gh argument log shows `--repo` or a `repos/` path on every call); the `gh repo view` fallback (scripts/retrigger-review.sh:50) carries neither. `_repo_scoped` accepts it only through `_REPO_RESOLVE` (tests/pr_submit/test_static_grep.py:128); the scan also needs `_command_lines` (:71-95) and the `_GH_CMD` filter (:31) or comment lines and `gh api \` continuations fail. |
| INV-002 | sufficiency_challenge | Adding cycle_id, applied_edits and target_sha to `resume_decision` alone closes the release-safety gap | UNADDRESSED | HIGH | `published` is keyed on `guard.cycle_id` (source.md:108); no fold row sets `cycle_id` (source.md:196-206); engage row 7 NOOPs on a held guard (source.md:139); release row 8 checks only head == target_sha (source.md:156). Cycle 1 HOLDs its release, cycle 2 edits and crashes before its push; resume sees cycle 1's `push_completed`, and a target_sha taken from it still equals the head: RELEASE(pushed) with unpushed fixes. |
| INV-003 | interaction_effects | The guard cycle id can be reused as the push and `rereview_requested` cycle id | UNADDRESSED | MEDIUM | run_log.py:251-257 counts each cycle_id once; recovery.py:150-155 decides on re-trigger by cycle_id; a stale id carried to a later cycle makes a crash between that push and its re-trigger resume as "already re-triggered". |
| INV-004 | guard_conditions | A zero-edit cycle reaches the release step | UNADDRESSED | MEDIUM | Task 10 puts Release "after push_completed" (plan:150, :153) but a zero-edit cycle never pushes (source.md:276); no SKILL criterion says where `release_decision(applied_edits=0)` is called. |
| INV-005 | collection_boundaries | After `not_applied` erases a first record, the interrupted cycle is re-guarded before its edits | UNADDRESSED | MEDIUM | source.md:278 says "the next cycle engages normally"; with the guard None, resume row 1 NOOPs (source.md:163), so that cycle's Wave 4 edits can run with the PR not draft; plan:166 tests only a later-cycle re-engage. |
| INV-006 | state_variables | This cycle's `applied_edits` is available at resume | UNADDRESSED | MEDIUM | plan:70 defines it per cycle but neither the fold fields (source.md:190-191) nor the event payloads (source.md:184-185) store it. |
| INV-007 | count_divergence | The counts in the plan match the spec | ADDRESSED | LOW | 11, 9 and 9 table rows; 12 tests (plan:169 vs source.md:309-320); 43 to 45 members; 7 idempotency sets unchanged. |

## Summary

- **Total findings**: 7
- **ADDRESSED**: 1
- **UNADDRESSED**: 6
  - HIGH: 2 (INV-001, INV-002)
  - MEDIUM: 4 (INV-003 to INV-006)
  - LOW: 0

Gate: 2 HIGH UNADDRESSED, so convergence is BLOCKED_BY_INVARIANTS. INV-001 and INV-002 refine consensus items (a) and (b) (they say the agreed fixes are not sufficient alone); they are folded into the merged verdict, not debated again (standard depth has no Round 3).
Fault-finder caveat: it states its `_repo_scoped`, recovery and run_log evidence comes from the working tree that already holds the later implementation.
