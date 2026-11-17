# Stage 1 timing (issue 607)

Same machine, same script path (the worktree copy `src/superclaude/skills/ccsession-tag/ccsession`), `CCSESSION_MODELS_REFRESH=0`, bash 5.2.37, `LANG=C.UTF-8`, `LC_ALL` unset, 28 cores.
Other sessions were running on this machine (load average per run is in the raw files under `.dev/issues/607/`).

## Scale store (a throwaway HOME: 477 names in the repo list, 585 in 19 lists, 439 transcripts of about 1.25 MB, built from real transcript heads and tails)

| View | Before (three runs, s) | After Task 1 only (s) | After Stage 1 (three runs, s) |
|---|---|---|---|
| `--here` | 22.244, 22.070, 22.016 (load 2.7-3.0) | 16.057, 16.238 | 8.291, 7.622, 7.906 (load 5.6) |
| `--list` | 10.675, 11.052, 11.524 (load 2.3-2.8) | not run | 5.075, 5.044, 5.047 (load 5.3) |

The issue's measurement on the reporter's store was 22.5 to 27.1 s for `--here` and 14.5 s for `--list`; this scale store gives 22.0 s and 10.7 s before the change.

## This machine's real store (113 names; largest list 27)

| View | Before (s) | After Stage 1 (s) |
|---|---|---|
| `--here` | 1.799, 1.632, 1.623 (load 0.9-1.1) | 0.684, 0.725, 0.697 (load 5.5) |
| `--list` | 1.821, 1.744, 1.664 | 0.941, 0.945, 0.941 |

## Per-function trace (`PS4='+T ${EPOCHREALTIME} ${FUNCNAME[0]:-main} ' bash -x ... --here`, gaps summed per function; scale store)

Before: session_home 11.034, list_sessions 4.508, format_epoch 2.462, session_place 1.458, get_btime 1.175, get_mtime 1.127, session_transcript 0.910.
After: session_home 4.746, session_place 1.512, list_sessions 1.152, epoch_to_var 0.359, stat_times 0.190, transcript index build plus lookups 0.183 in all (the cost the source asked to measure as F3).
Full list: `./stage1-trace-after.txt`.

## What was measured about the index lookup (F3)

A first version searched one long string for each session with `${var%%pattern*}`: `--here` took 26.1 s (slower than before) and `--list` 25.0 s, because that search costs about as much as the `ls | head` it replaced (user time 19 s). The shipped version reads the index once into one variable per session id: build plus 585 lookups cost 0.18 s (traced).

## Per-session process counts (counting shims, test `test_listing_starts_a_fixed_number_of_processes_per_saved_name`)

`--here`: 2 date, 1 stat, 1 head, 1 grep, 1 awk per saved name; none of basename, dirname, ls. `--here --all` and `--list`: 2 date and 1 stat per name. Before (measured by running the same test on the old script): `--here` 4 date, 3 head, 2 dirname, 2 basename, 2 stat, 1 ls, 1 grep, 1 awk per name; `--list` and `--here --all` 4 date, 2 head, 2 stat, 1 dirname, 1 basename, 1 ls.
