# Stage 2 timing (issue 607)

Same machine and scripts as `./stage1-timing.md`. `scan_sessions.py` is called once for the worktree view (`--here`, and `--ask`, which shows that list); `--list` and `--here --all` need no start folder and keep the Stage 1 shell code. Other sessions were running; the load average of each run is in the raw files under `.dev/issues/607/` (3.2 to 3.7 for the final runs below).

## Scale store (477 names in the repo list, 585 in 19 lists, 439 transcripts)

| View | Original (3 runs, s) | After Stage 1 (3 runs, s) | After Stage 2 (3 runs, s) |
|---|---|---|---|
| `--here` (the list `--ask` shows) | 22.244, 22.070, 22.016 | 8.291, 7.622, 7.906 | 3.146, 2.983, 2.965 |
| `--list` | 10.675, 11.052, 11.524 | 5.075, 5.044, 5.047 | 4.508, 4.444, 4.515 |

The source's derived Stage 2 target for `--here` was 2.7 to 4.6 s: met (3.0 s). `--list` and `--here --all` do not use the helper, so their gain is Stage 1's.

## Cold page cache (gate A-002)

An earlier build of Stage 2 (the helper also used for `--list`, which the final code does not do; the `--here` path is the same) with `posix_fadvise(DONTNEED)` on all 1025 files of the scale store before each run (eviction cannot be checked without root): `--here` 2.916 s and 2.648 s cold, against 2.637 s and 2.615 s warm right after. The original script cold: 22.297 s. Raw: `.dev/issues/607/gates-A002-cold-cache.txt`.

## This machine's real store (113 names)

| View | Original (s) | After Stage 1 (s) | After Stage 2 (s) |
|---|---|---|---|
| `--here` | 1.799, 1.632, 1.623 | 0.684, 0.725, 0.697 | 0.429, 0.429, 0.466 |
| `--list` | 1.821, 1.744, 1.664 | 0.941, 0.945, 0.941 | 1.005, 1.005, 1.237 |

## Why the helper is not used for `--list`

A first build called the helper for every list. On this machine's real store (15 lists) `--list` then took 1.2 s instead of Stage 1's 0.94 s: each call costs about 36 ms (python3 startup 21 ms, plus a scan of the projects folder 15 ms) and `--list` has no start-folder work for it to save. The worktree view has one list and 4.7 s of start-folder work, so it is the only one that calls the helper.

## Trace by function after Stage 2 (scale store, `--here`)

session_place 1.419, list_sessions 0.573, epoch_to_var 0.302, scan_topics 0.257 (the whole helper call and its parsing), stat_times 0.158, file_to_name 0.132. session_home is gone (it was 4.7 s after Stage 1). Stat and date together cost 0.46 s on `--here`, well under the source's 2 s threshold for Stage 3, so Stage 3 stays out.

## Helper alone

`scan_sessions.py` over the 476 sessions of the scale store: 0.155 s wall (including `uv run` startup), against 4.7 s for the shell code that it replaces.
