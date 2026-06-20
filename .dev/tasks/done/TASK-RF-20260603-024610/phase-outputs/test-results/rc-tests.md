# Phase RC — Roadmap-Completion Test & Lint Summary (Step RC.5)

**Captured:** 2026-06-03 21:48
**Raw output:** `rc-tests.txt`
**Command:** `uv run pytest tests/sprint/ tests/cli/eval/test_isolation_layers_probe.py tests/integration/test_sprint_wiring.py -q`

## Pytest counts (exact)

| Metric | Count |
|--------|-------|
| Passed | 1068 |
| Failed | 54 |
| Skipped | 0 |
| Exit code | 1 |

Summary line: `54 failed, 1068 passed, 20 warnings in 38.02s`

## Lint

`make lint` → **PASS** ("All checks passed!", exit 0).

## Regression analysis vs `pre-change-baseline.md` — ZERO regressions

Failing node-id set is **PROVABLY IDENTICAL** to the Phase-1 baseline (set diff
empty both directions). All 54 are the pre-existing `.stdin`/IndexError baseline.

One regression surfaced mid-step and was fixed: `test_prior_context_reaches_per_task_prompt`
(my own Stage-1 test) used a fake `_process` (`SimpleNamespace`) lacking `poll()`;
RC.2's watchdog calls `underlying.poll()`. Fixed the test's fake to mimic a finished
Popen (`poll=lambda: 0`). Re-run → back to the baseline 54.

## RC items validated

- RC.1 — `aggregate_task_results` live caller (per-task phase synthesis); execute_sprint
  integration tests remain on the baseline `.stdin` list (orthogonal).
- RC.2 — per-task wait runs under `_poll_with_stall_watchdog`; the real-spawn e2e_real
  tests (isolation smoke, turn count, rerun happy path) pass under it.
- RC.3 — per-worker independent timers (satisfied by construction; verified).
- RC.4 — `_write_preliminary_result` O_EXCL atomic write; `TestWritePreliminaryResult`
  unit tests (t001/t002/t002b/t005) all pass (t005 updated to inject OSError at `os.open`).

## Verdict

Phase RC (roadmap-completion C-018→C-021) is green: aggregate wired live, per-task
stall watchdog + per-worker timers, O_EXCL preliminary write. Full sprint suite +
probe + wiring integration show the identical-to-baseline failure set (ZERO
regressions) and lint is clean.
