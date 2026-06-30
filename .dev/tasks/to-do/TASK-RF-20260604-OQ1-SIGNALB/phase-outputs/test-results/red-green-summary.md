# RED → GREEN Summary (Step 4.4)

**Date:** 2026-06-04
**Target test:** `tests/sprint/test_resume.py::TestResumePlanner::test_resume_pass_recovered_counts_as_completed`
**Method:** `git stash push` on `integrity.py` only (byte-exact revert of the Signal B source edit while keeping all test changes), run the targeted test, then `git stash pop` to restore the Opt-2a fix and rerun.

## RED (source fix reverted, tests kept)

Command: `uv run pytest "tests/sprint/test_resume.py::TestResumePlanner::test_resume_pass_recovered_counts_as_completed" -q`
Raw: `phase-outputs/test-results/red-positive-guard-output.txt`
Result: **1 failed** (PYTEST_EXIT: 1)

Failure (the load-bearing assertion, NOT a syntax/import error):

```
tests/sprint/test_resume.py:233: in test_resume_pass_recovered_counts_as_completed
    assert report.validated_last is True
E   AssertionError: assert False is True
E    +  where False = BoundaryReport(validated_last=False, suspects=[BoundaryTask(task_id='T03.01',
        persisted_status=<TaskStatus.PASS_RECOVERED...>, derived=TaskStatus.FAIL_RECOVERABLE,
        artifacts_present=True...)]).validated_last
```

Diagnosis: with the pre-Opt-2a Signal B rule (`signal_b_pass = derived is TaskStatus.PASS`), the `RECOVERED_TRANSCRIPT` derives as `TaskStatus.FAIL_RECOVERABLE`, so `signal_b_pass` is False and the composite `validated_last` is False — even though `persisted_status` is `PASS_RECOVERED` and `artifacts_present` is True. The RED is caused **exactly** by the recovered transcript failing Signal B under the old rule, confirming the test is non-vacuous.

## GREEN (Opt-2a fix restored)

Command: same targeted pytest invocation
Raw: `phase-outputs/test-results/green-positive-guard-output.txt`
Result: **1 passed** (PYTEST_EXIT: 0)

Diagnosis: the Opt-2a exemption (`if lc.persisted_status is TaskStatus.PASS_RECOVERED: signal_b_pass = True`) accepts the recovered seam for Signal B; with the declared deliverable present (`artifacts_ok` True), the composite `validated_last` becomes True and the assertion passes.

## Final worktree state

- `git stash pop` reapplied the Opt-2a edit; `git diff --stat` reported `integrity.py | 15 ++++ (12 insertions, 3 deletions)` — the fix is restored.
- The GREEN run (with the restored source) passed, confirming the worktree is left with the Opt-2a source fix in place.
- No reverted source state remains.

**Verdict:** Genuine RED→GREEN demonstrated. The assertion fails before Opt-2a (Signal B mismatch on the recovered transcript) and passes after, and the worktree retains the Opt-2a fix.
