# SUMMARY (executor-added, one line): worst 64KB max 893.9 ms (git-status-lines-64KB); worst overall max 893.9 ms (git-status-lines-64KB); all four maxima under 1 s idle serial.
# COMMAND USED (executor-added): LL_SPEED_RESULTS=.dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d1-serial-idle.md uv run pytest tests/hooks/test_launch_level_guard.py -k test_speed_large_commands -p no:xdist -rP
# Task 15: hook speed results

Written by the test module tests/hooks/test_launch_level_guard.py (section
"Task 15: speed") at the end of the run below; no number is edited by hand.

- Run: 2026-11-08 06:47 UTC, `LL_SPEED_RESULTS=<this file> uv run pytest tests/hooks/test_launch_level_guard.py -k "SPD or speed"`.
- Host: GNU bash, version 5.2.37(1)-release (x86_64-pc-linux-gnu); 28 CPUs; load average 3.82 4.21 3.61 when the file was written; Python 3.11.15.
- Method: each run is one real subprocess (bash and the hook script), timed with time.monotonic() around subprocess.run after one untimed warm-up run. p95 is the inclusive 95th percentile. PATH holds only a temporary bin directory; HOME is a temporary directory. T-SPD-5 uses 100 runs per command (each run takes 0.5 to 0.9 s); the envelope stress case uses 5 runs, with p95 taken from those runs.
- Asserted (design section 8): T-SPD-3 (guard median at most 1.5 times block-bare-python.sh) and T-SPD-5 (every run under 1 s). Every other row is reported only.

| Case | Runs | Median | p95 | Target | Result |
|---|---|---|---|---|---|
| T-SPD-5 guard, governed FS, heredoc-git-words-64KB | 100 | 526.5 ms | 559.4 ms | every run under 1 s (asserted outside xdist) | PASS: max 675.9 ms; exit [2] |
| T-SPD-5 guard, governed FS, backslash-lines-64KB | 100 | 510.4 ms | 547.7 ms | every run under 1 s (asserted outside xdist) | PASS: max 605.0 ms; exit [0] |
| T-SPD-5 guard, governed FS, git-status-lines-64KB | 100 | 761.1 ms | 786.7 ms | every run under 1 s (asserted outside xdist) | PASS: max 893.9 ms; exit [0] |
| T-SPD-5 guard, governed FS, 1MB-big | 100 | 451.0 ms | 465.9 ms | every run under 1 s (asserted outside xdist) | PASS: max 544.1 ms; exit [2] |

## Reported targets exceeded

None.

## Asserted targets failed

None.
