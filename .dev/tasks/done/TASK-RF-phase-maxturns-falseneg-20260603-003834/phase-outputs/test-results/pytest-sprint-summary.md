# pytest tests/sprint/ (full suite) — Summary (Step 6.2)

**Command:** `uv run pytest tests/sprint/`
**Overall result:** 57 failed, 947 passed (20 warnings) — **all 57 failures are PRE-EXISTING; ZERO are caused by this task.**
**This task's verdict:** PASS — no regressions. The full failure set is byte-identical between baseline and post-change.

## Counts

| Metric | Count |
|--------|-------|
| Total | 1004 |
| Passed | 947 |
| Failed | 57 (all pre-existing) |
| Warnings | 20 |

**Final summary line:** `57 failed, 947 passed, 20 warnings in 6.00s`

## Regression proof (baseline vs post-change diff)

Captured the sorted `FAILED` list post-change (57), then `git stash`-ed all
three changed files (models.py, executor.py, test_executor.py) to revert to
baseline `e101951a`, re-ran the full suite (57 failed), `git stash pop`-ed, and
diffed the two sorted failure lists with `comm`:

- **Failures present now but NOT on baseline (regressions introduced):** `0` (empty)
- **Failures on baseline now fixed/changed:** `0` (empty)

The failure sets are **identical**. This task introduces **zero new failures**.

## Nature of the pre-existing failures (out of scope)

The 57 failures cluster in test-infrastructure / unrelated subsystems:

- `test_executor.py` integration coverage + backward-compat — fake `Popen`
  doubles (`_PassPopen`/`_HaltPopen`/`_TimeoutPopen`/`_InterruptPopen`) lack a
  `stdin` attribute the production path reads.
- `test_tui_monitor.py`, `test_watchdog.py`, `test_phase8_halt_fix.py`,
  `test_regression_gaps.py` — TUI/monitor/watchdog/tmux/halt fixtures.

None of these exercise the `TaskStatus` enum semantics, the per-task recovery
branch, or the phase aggregation that this task changed. The new tests added by
this task (the per-task recovery suite + the aggregation count test) all PASS.

Recorded as a follow-up item; fixing repo-wide pre-existing red is out of this
task's scope (scope discipline) and must not be used to weaken exit-124 timeout
behaviour.
