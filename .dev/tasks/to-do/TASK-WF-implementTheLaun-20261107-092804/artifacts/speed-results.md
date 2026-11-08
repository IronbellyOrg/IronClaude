# Task 15: hook speed results

Written by the test module tests/hooks/test_launch_level_guard.py (section
"Task 15: speed") at the end of the run below; no number is edited by hand.

- Run: 2026-11-07 17:22 UTC, `LL_SPEED_RESULTS=<this file> uv run pytest tests/hooks/test_launch_level_guard.py -k "SPD or speed"`.
- Host: GNU bash, version 5.2.37(1)-release (x86_64-pc-linux-gnu); 28 CPUs; load average 2.54 2.45 2.26 when the file was written; Python 3.11.15.
- Method: each run is one real subprocess (bash and the hook script), timed with time.monotonic() around subprocess.run after one untimed warm-up run. p95 is the inclusive 95th percentile. PATH holds only a temporary bin directory; HOME is a temporary directory. T-SPD-5 uses 100 runs per command (each run takes 0.5 to 0.9 s); the envelope stress case uses 5 runs, with p95 taken from those runs.
- Asserted (design section 8): T-SPD-3 (guard median at most 1.5 times block-bare-python.sh) and T-SPD-5 (every run under 1 s). Every other row is reported only.

| Case | Runs | Median | p95 | Target | Result |
|---|---|---|---|---|---|
| T-SPD-1 guard, ordinary, empty store | 100 | 2.9 ms | 3.5 ms | median 20 ms, p95 50 ms | within (reported only) |
| T-SPD-2 guard, ordinary, store of 1,050 files | 100 | 8.6 ms | 9.6 ms | median 20 ms, p95 50 ms | within (reported only) |
| T-SPD-3 block-bare-python.sh, ordinary, empty store (same run) | 100 | 7.2 ms | 8.2 ms | baseline for T-SPD-3 | baseline |
| T-SPD-3 guard, ordinary, empty store (same run) | 100 | 3.3 ms | 4.0 ms | median at most 1.5 times block-bare-python.sh (asserted) | PASS: ratio 0.45 |
| T-SPD-3 block-bare-python.sh, ordinary, store of 1,050 files (same run) | 100 | 7.4 ms | 8.3 ms | baseline for T-SPD-3 | baseline |
| T-SPD-3 guard, ordinary, store of 1,050 files (same run) | 100 | 8.6 ms | 9.5 ms | median at most 1.5 times block-bare-python.sh (asserted) | PASS: ratio 1.16 |
| T-SPD-4 guard, governed F, allow `git status` | 100 | 14.2 ms | 15.9 ms | p95 60 ms | within (reported only) |
| T-SPD-4 guard, governed F, block `git commit -m x` | 100 | 14.4 ms | 15.9 ms | p95 60 ms | within (reported only) |
| T-SPD-5 guard, governed FS, heredoc-git-words-64KB | 100 | 516.7 ms | 549.2 ms | every run under 1 s (asserted) | PASS: max 829.2 ms; exit [2] |
| T-SPD-5 guard, governed FS, backslash-lines-64KB | 100 | 495.0 ms | 513.3 ms | every run under 1 s (asserted) | PASS: max 568.6 ms; exit [0] |
| T-SPD-5 guard, governed FS, git-status-lines-64KB | 100 | 735.4 ms | 754.7 ms | every run under 1 s (asserted) | PASS: max 869.7 ms; exit [0] |
| T-SPD-5 guard, governed FS, 1MB-big | 100 | 436.0 ms | 451.6 ms | every run under 1 s (asserted) | PASS: max 457.7 ms; exit [2] |
| Envelope stress, guard, ordinary, 32 MiB description field | 5 | 890.0 ms | 897.6 ms | none; report time and memory, or a timeout | completed, exit [0], peak RSS 162 MiB (largest process of the hook tree) |
| Envelope stress, guard, governed F, 32 MiB description field | 5 | 906.7 ms | 928.6 ms | none; report time and memory, or a timeout | completed, exit [0], peak RSS 162 MiB (largest process of the hook tree) |
| F2 launch-job-identity.sh, ordinary Bash, no store | 100 | 2.0 ms | 2.4 ms | median 20 ms, p95 50 ms (ordinary budget, reported only) | within (reported only) |
| F2 launch-job-identity.sh, ordinary Bash, store with only pending/ | 100 | 78.9 ms | 85.6 ms | median 20 ms, p95 50 ms (ordinary budget, reported only) | EXCEEDED (reported only) |

## Reported targets exceeded

- F2 launch-job-identity.sh, ordinary Bash, store with only pending/ exceeded its reported target (median 20 ms, p95 50 ms (ordinary budget, reported only)); follow-up: a follow-up change to launch-job-identity.sh that checks sessions/<session_id> in bash before starting uv (this plan does not modify that script).

## Asserted targets failed

None.
