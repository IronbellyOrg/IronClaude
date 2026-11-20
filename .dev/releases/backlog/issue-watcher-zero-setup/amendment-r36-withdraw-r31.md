# Amendment R36: withdraw R31 (the void-on-change rule)

Decision: owner, 2026-11-20 ("Yes, withdraw"). Row R36 of `requirements.md`. R31 said an approval is void when the Project item's Status or Pipeline changed after it. R36 says the approval (the `Approved` issue field set to `Yes`, R35) still counts after such a change.

## Why this is a separate file and not an edit of the running plan

The plan `.dev/tasks/to-do/TASK-WF-requirements-20261119-143917-2/` is being run by `/sc:implement` (its ledger records the plan hash and had Task 14 started at 2026-11-20 01:30 UTC). Editing the plan or its ledger mid-run would break the hash check. R31's code was built by that run (Task 5, compliant), so the withdrawal is a change to finished work and needs its own pass after the run has finished, or at a point where the run's owner stops it.

## What to change (found by reading `predicates.py` and Grep on 2026-11-20; every item is for the executor to verify against the code before editing)

Remove:
- `value_changed_after` in `src/superclaude/cli/issue_watch/predicates.py` (line 302 on 2026-11-20) and its two calls, one in `_examine` and one in `_revalidate` in `src/superclaude/cli/issue_watch/cycle.py`.
- The tests that exist only for it (`tests/issue_watch/test_predicates.py`, `tests/issue_watch/test_cycle.py`: the value-time cases, the overlap case "Pipeline lowered with a value time after the approval ends `edited_after_approval`", and the empty-Pipeline case written for P4-2).
- `status_changed_at` and `pipeline_changed_at` (`predicates.py:128-129`) and their parsing in `github.py` `_project_item`, but only if no other task still reads them. The read of the `Approved` field events (Task 4a) is separate and stays.

Keep:
- `unchanged_since` (an issue body, comment or title edited after the approval voids it).
- In `_revalidate`: the approval reread, then `project_check`, then the examined-versus-reread comparison of Status and Pipeline (`revalidation_failed`). This still stops a change between examine and launch inside one cycle; it does not stop a change made before the next cycle.
- The Pipeline read itself (Task 3) and the closed ship gate (Task 8, `level_gated`).

Reword:
- `WORKER-CONTRACT.md:245` and `docs/designs/issue-watcher-status-pipelines.md:83` (the Full Submit push rule): the go is "the owner's Pipeline value plus an approval in the `Approved` field", without "an approval later than the last Project change".
- `docs/designs/issue-watcher-status-pipelines.md:79` (effect on the approval): the coordinator's move to In review no longer voids the approval; In review still fails `project_check`, so a relaunch needs the owner to move the Status back to an allowed value.
- Task 26 documentation (`docs/designs/issue-watcher.md`, `issue-watcher-setup.md`) and the Task 28 record in `requirements.md`: R31 is withdrawn, R36 decided.

Retire:
- Task 4's observation of the value times (`artifacts/t4-updatedat-observation.md`). It has no rule left to decide. Keep the file as history.

## Safety effect, stated plainly

With R31 gone, an issue approved at Pipeline None can have its Pipeline raised to Full Submit afterwards and the approval still counts. While `GOVERNED_LEVELS_ALLOWED` is `False` (Task 8) nothing above `none` launches, so this is held back by the gate alone. Before the gate is ever opened, the owner should decide whether the approval should be re-given after a Pipeline change. That is a different rule from R31 and is not decided here. Until then the owner should raise the Pipeline before setting `Approved`.

## Order

1. Let the running plan finish (or stop it on a task boundary).
2. Run the removal as a separate `/sc:implement` pass with this file as its source.
3. Run the post-execution reflect on the combined result.
