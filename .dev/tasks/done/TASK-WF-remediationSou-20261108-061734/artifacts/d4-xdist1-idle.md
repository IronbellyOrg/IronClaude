# SUMMARY (executor-added, one line): worst 64KB max 840.2 ms (git-status-lines-64KB); worst overall max 840.2 ms; D4 vs D1: xdist-1 idle medians/maxima within noise of serial idle (D1 maxima 675.9/605.0/893.9/544.1 ms vs D4 627.4/592.5/840.2/541.1 ms; worst-64KB delta 893.9->840.2 ms, about 6 percent lower; xdist plumbing adds no cost).
# COMMAND USED (executor-added): LL_SPEED_RESULTS=.dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d4-xdist1-idle.md uv run pytest tests/hooks/test_launch_level_guard.py -k test_speed_large_commands -n 1 -rP
# Task 15: hook speed results

Written by the test module tests/hooks/test_launch_level_guard.py (section
"Task 15: speed") at the end of the run below; no number is edited by hand.

- Run: 2026-11-08 07:06 UTC, `LL_SPEED_RESULTS=<this file> uv run pytest tests/hooks/test_launch_level_guard.py -k "SPD or speed"`.
- Host: GNU bash, version 5.2.37(1)-release (x86_64-pc-linux-gnu); 28 CPUs; load average 3.23 2.70 2.92 when the file was written; Python 3.11.15.
- Method: each run is one real subprocess (bash and the hook script), timed with time.monotonic() around subprocess.run after one untimed warm-up run. p95 is the inclusive 95th percentile. PATH holds only a temporary bin directory; HOME is a temporary directory. T-SPD-5 uses 100 runs per command (each run takes 0.5 to 0.9 s); the envelope stress case uses 5 runs, with p95 taken from those runs.
- Asserted (design section 8): T-SPD-3 (guard median at most 1.5 times block-bare-python.sh) and T-SPD-5 (every run under 1 s). Every other row is reported only.

| Case | Runs | Median | p95 | Target | Result |
|---|---|---|---|---|---|
| T-SPD-5 guard, governed FS, heredoc-git-words-64KB | 100 | 520.2 ms | 549.2 ms | every run under 1 s (asserted outside xdist) | PASS: max 627.4 ms; exit [2] |
| T-SPD-5 guard, governed FS, backslash-lines-64KB | 100 | 503.5 ms | 528.0 ms | every run under 1 s (asserted outside xdist) | PASS: max 592.5 ms; exit [0] |
| T-SPD-5 guard, governed FS, git-status-lines-64KB | 100 | 745.3 ms | 792.4 ms | every run under 1 s (asserted outside xdist) | PASS: max 840.2 ms; exit [0] |
| T-SPD-5 guard, governed FS, 1MB-big | 100 | 449.0 ms | 474.2 ms | every run under 1 s (asserted outside xdist) | PASS: max 541.1 ms; exit [2] |

## Reported targets exceeded

None.

## Asserted targets failed

None.
