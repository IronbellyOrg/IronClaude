# SUMMARY (executor-added, one line): worst 64KB max 5536.1 ms (git-status-lines-64KB); worst overall max 5536.1 ms; D2 vs D1: loaded maxima rise clearly above idle (worst 64KB 893.9 -> 5536.1 ms, 6.2x; medians 761.1 -> 2422.1 ms) under 56 busy loops (2x oversubscription, load average ~74 during the run); all four cases FAIL the current 1 s assert in serial mode, as the 1.23 s local report predicted. Note: 2x oversubscription is deliberately harsher than CI (4 workers on 4 vCPUs = 1x); this arm is the contention mechanism probe.
# COMMAND USED (executor-added): LL_SPEED_RESULTS=.dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d2-serial-loaded.md uv run pytest tests/hooks/test_launch_level_guard.py -k test_speed_large_commands -p no:xdist -rP   # load: for i in $(seq 56); do timeout 900 yes > /dev/null 2>&1 & done (self-terminates after 900 s)
# Task 15: hook speed results

Written by the test module tests/hooks/test_launch_level_guard.py (section
"Task 15: speed") at the end of the run below; no number is edited by hand.

- Run: 2026-11-08 07:24 UTC, `LL_SPEED_RESULTS=<this file> uv run pytest tests/hooks/test_launch_level_guard.py -k "SPD or speed"`.
- Host: GNU bash, version 5.2.37(1)-release (x86_64-pc-linux-gnu); 28 CPUs; load average 74.27 66.35 41.36 when the file was written; Python 3.11.15.
- Method: each run is one real subprocess (bash and the hook script), timed with time.monotonic() around subprocess.run after one untimed warm-up run. p95 is the inclusive 95th percentile. PATH holds only a temporary bin directory; HOME is a temporary directory. T-SPD-5 uses 100 runs per command (each run takes 0.5 to 0.9 s); the envelope stress case uses 5 runs, with p95 taken from those runs.
- Asserted (design section 8): T-SPD-3 (guard median at most 1.5 times block-bare-python.sh) and T-SPD-5 (every run under 1 s). Every other row is reported only.

| Case | Runs | Median | p95 | Target | Result |
|---|---|---|---|---|---|
| T-SPD-5 guard, governed FS, heredoc-git-words-64KB | 100 | 1695.0 ms | 2945.9 ms | every run under 1 s (asserted outside xdist) | FAIL: max 4199.0 ms; exit [2] |
| T-SPD-5 guard, governed FS, backslash-lines-64KB | 100 | 1694.3 ms | 2566.7 ms | every run under 1 s (asserted outside xdist) | FAIL: max 2991.6 ms; exit [0] |
| T-SPD-5 guard, governed FS, git-status-lines-64KB | 100 | 2422.1 ms | 4151.5 ms | every run under 1 s (asserted outside xdist) | FAIL: max 5536.1 ms; exit [0] |
| T-SPD-5 guard, governed FS, 1MB-big | 100 | 1614.8 ms | 2981.2 ms | every run under 1 s (asserted outside xdist) | FAIL: max 3828.5 ms; exit [2] |

## Reported targets exceeded

None.

## Asserted targets failed

- T-SPD-5 guard, governed FS, heredoc-git-words-64KB FAILED its asserted target (every run under 1 s (asserted outside xdist)): FAIL: max 4199.0 ms; exit [2].
- T-SPD-5 guard, governed FS, backslash-lines-64KB FAILED its asserted target (every run under 1 s (asserted outside xdist)): FAIL: max 2991.6 ms; exit [0].
- T-SPD-5 guard, governed FS, git-status-lines-64KB FAILED its asserted target (every run under 1 s (asserted outside xdist)): FAIL: max 5536.1 ms; exit [0].
- T-SPD-5 guard, governed FS, 1MB-big FAILED its asserted target (every run under 1 s (asserted outside xdist)): FAIL: max 3828.5 ms; exit [2].
