# Invariant Probe Results

## Round 2.5 - Fault-Finder Analysis

Source: the fault-finder agent's returned message (sonnet class, a different class from both advocates). The orchestrator re-checked INV-001, INV-003 and INV-005 against the plan and `tests/skills/test_worker_contract.py:1893-1957`; INV-007 is refined (see the note under the table).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | The listed fixes make the plan fit for /sc:implement | UNADDRESSED | HIGH | Task 20 requires "the recorded command list in the .json output"; Tasks 6 and 12 write JSON of "the same rows" only; no task writes a command list |
| INV-002 | sufficiency_challenge | Giving item 1 its own fallback settles the removal path | UNADDRESSED | HIGH | Items 1 and 2 stay NOT PROVEN by design (plan Task 1); item 1's fallback is "Use only git worktree remove" (source.md:297, 374); Task 11 still runs `orca worktree rm` for Orca-listed worktrees; the "deregister from Orca" step has no verb in any task |
| INV-003 | guard_conditions | Task 2's runner is the allowlist the spec adopts | UNADDRESSED | HIGH | Task 2 lists only banned shapes (a denylist); source.md:323 says "Adopted: the script runs commands only through one runner with an allowlist"; unlisted mutating commands (git reset, mv, find -delete) would pass |
| INV-004 | guard_conditions | Task 1's reasons for PROVEN and NOT PROVEN are sound | UNADDRESSED | HIGH | Item 7 is read-only (compare `linkedPR` with `gh`, source.md:303) yet Task 1 marks it NOT PROVEN with a write-based reason; item 4 is marked PROVEN by "write the definition" while source.md:300 says to test with a fake /proc |
| INV-005 | interaction_effects | Tasks 14 and 16 pass as written | UNADDRESSED | MEDIUM | `tests/skills/test_worker_contract.py:1893-1957` scans `src/superclaude/commands` for `git push`, `git worktree remove`, `gh pr` lines and fails on any unclassified hit; the plan never mentions the `WRITE_VERB_CLASSIFICATION` table |
| INV-006 | interaction_effects | A pull-request task is a clean fix for C-004 | ADDRESSED (partial) | MEDIUM | Plan Constraints say "no other repo is pushed to"; the pull request may be opened only through /sc:pr-submit --monitor 3; the PR needs a "Generator-Constraint Considered" section if a gate or validator file is touched (UNVERIFIED); use a final handoff note, not an executing task |
| INV-007 | state_variables | The save state and the second check cover the .dev window | UNADDRESSED | MEDIUM | Task 6 shows `removable` at save state `needed` while rule 5 allows `.dev` only at `verified`; the order of save and decision under `--apply` is unstated; Task 13 and source.md:248 test only a commit, a tracked edit and an untracked file outside `.dev`, not a new ignored `.dev` file. Orchestrator refinement: Task 11 does re-read the untracked and ignored lists after the close, so the gap is test coverage and the unstated order, not a missing check |
| INV-008 | interaction_effects | Moving Task 7 after Task 2 is a plain reorder | ADDRESSED (partial) | MEDIUM | Task 7's "removal reports kept" check needs Task 11; the `check_allowed` registration call arrives in Task 11; "by Task 7" and "Task 13" references in Tasks 3, 4, 10, 13 and 19 need renumbering; Task 7 must be split |
| INV-009 | count_divergence | Task 20 dependencies are complete | UNADDRESSED | LOW | Task 20 lists only Tasks 12 and 19 but its criteria record the full suite, lint and sync; Tasks 13 and 15 to 18 are missing |

Category 6 result (sufficiency_challenge): the FAIL verdict survives without assumption A-001, because INV-001 to INV-004 are independent blockers; the suggested fixes alone do not make the plan fit for /sc:implement.

## Summary

- **Total findings**: 9
- **ADDRESSED**: 2 (both partial)
- **UNADDRESSED**: 7
  - HIGH: 4 (INV-001, INV-002, INV-003, INV-004)
  - MEDIUM: 2 (INV-005, INV-007)
  - LOW: 1 (INV-009)
