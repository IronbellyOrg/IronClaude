# Tier 1 observation (captured by the parent, same-shell, 2026-11-17)

Version measured: installed /home/coder/.claude/skills/ccsession-tag/ccsession, 2072 lines, byte-identical to origin/master 10f6ec670bf55f0fe768be8e0ef2067d5c5d879e (cmp). Run site: this machine (28 cores, load average 11.9 at start of measuring), `HOME=/home/coder`.

## Store size

| Item | Value | Source command |
|---|---|---|
| topic lists (`~/.claude/projects/*/topics`) | 19 | `ls -d ~/.claude/projects/*/topics \| wc -l` |
| topic (name) files in all lists | 589 | `ls ~/.claude/projects/*/topics/*.txt \| wc -l` |
| topic files in the IronClaude repo list (`github.com-IronbellyOrg-IronClaude`) | 477 | per-list count |
| workspace folders under `~/.claude/projects` | 437 | `ls ~/.claude/projects \| wc -l` |
| transcripts (`*/*.jsonl`) | 1741 | `ls ~/.claude/projects/*/*.jsonl \| wc -l` |
| size of `~/.claude/projects` | 23G | `du -sh` |

## Wall-clock (the reported symptom, reproduced)

| Command | real | user | sys | Output lines |
|---|---|---|---|---|
| `ccsession --here` (this is what `ccsession --ask` runs through `show_saved worktree`) | 27.069s | 5.823s | 13.566s | 405 |
| `ccsession --list` | 14.473s | 4.241s | 11.563s | 609 |

CPU: user+sys = 19.4s over 27.1s wall for `--here`, i.e. about 0.7 of one core, in 28 cores. sys time (process creation, glob/stat) is 70% of the CPU time.
Contrast: `python3 models.py refresh --wait 2` (the other launch step) takes 0.17s, so the model refresh is not the cause. `retention_warning` (ccsession:1665-1678) is one python3 call after the list.

## bash -x trace of `ccsession --here` (trace overhead included, trace wall 27.08s)

Self time per function, from consecutive trace timestamps (file: /tmp/ccs-xtrace.log, 54,295 lines, not kept in the repo):

| Function | Self time | Calls observed |
|---|---|---|
| session_home (ccsession:1377-1399) | 12.16s | 439 (one per session with a transcript) |
| list_sessions loop body (ccsession:1554-1663) | 5.12s | 477 topic files |
| format_epoch (ccsession:1533-1537) | 2.68s | 878 `date` processes (two per row) |
| session_transcript (ccsession:1480-1483) | 2.03s | 477 `ls -t */<uuid>.jsonl` + `head` |
| session_place (ccsession:1430-1478) | 1.95s | 439 |
| get_btime (ccsession:1488-1512) + get_mtime (ccsession:1514-1531) | 1.22s + 1.20s | 439 + 439 `stat` |
| format_duration | 0.14s | 439 |

Largest single commands: `awk` inside the session_home head/tail/grep/awk pipeline 9.89s (the cost of the whole pipeline is booked to its last process), `date` 2.66s, `head` in session_transcript 1.12s, `ls` in session_transcript 0.92s, `git` in session_place 0.91s, `stat` 0.88s + 0.86s.

Process counts in the trace: 1756 `date`, 972 `head`, 936 `dirname`, 936 `basename`, 878 `stat`, 477 `ls`, 457 `pwd`, 448 `grep`.

## Where the sessions live

Transcripts of the 477 sessions are not in the repo-keyed folder (`$PROJECTS_DIR/<repo key>/`), they live in one folder per working directory (437 folders). So the first lookup `$(dirname "$ws_dir")/$uuid.jsonl` (ccsession:1595) misses for them and `session_transcript` (ccsession:1480-1483) globs `"$PROJECTS_DIR"/*/<uuid>.jsonl` across 437 folders for each of 477 sessions (about 208,000 path checks, one `ls` and one `head` process each).

## Prototype (throwaway, /tmp/ccs-proto/proto.py, not a patch)

One Python process doing the same index (one directory scan builds uuid -> newest transcript for all 1741 transcripts) and the same head 256 KiB + tail 1 MiB working-directory scan for the 439 sessions: 0.01s index + 0.73s scan = 0.75s total (second run 0.78s); 554 MB read, no process spawned per session. It omits session_place's git calls, so the real total is a bit higher; the per-session process-creation cost is what disappears (the trace lists about 6,900 command words for 477 rows, of which at least 6,403 are external processes (date 1756 + head 972 + dirname 936 + basename 936 + stat 878 + ls 477 + grep 448; `pwd`, `cd`, `printf`, `echo` and `read` are builtins and not counted), roughly 13 or more per row, and the whole run is about 57 ms per row).

## Primitive behaviour observed in this run (2026-11-17T19:00:52Z, same shell, bash 5.2.37, GNU coreutils date)

- `date -r 1794941650 '+%Y-%m-%d %H:%M'` prints `date: 1794941650: No such file or directory`, exit 1 (GNU `date -r` takes a FILE). `date -d @1794941650 '+%Y-%m-%d %H:%M'` prints `2026-11-17 18:54`, exit 0. So format_epoch (ccsession:1533-1537) always runs a failing process first on Linux, then the working one.
- 200 iterations of "date -r (fails) then date -d" take 0.511 s (2.6 ms each); 200 iterations of date -d alone take 0.241 s (1.2 ms each). Over 878 timestamps: about 2.2 s with the failing attempt, about 1.1 s without.
- One `ls -t ~/.claude/projects/*/<uuid>.jsonl | head -n 1` (session_transcript's body, one uuid) takes 0.005 s; times 477 sessions = about 2.4 s, matching the traced 2.03 s.
## Falsification probe run by the parent (2026-11-17T19:02:52Z, same shell, read-only; 439 transcripts, 3,848 MB total, median 2.6 MB, p90 17.7 MB, max 174.6 MB; file list built with the same `ls -t */<uuid>.jsonl` rule)

| Arm | What it runs per file | real | user | sys |
|---|---|---|---|---|
| 1 | `{ head -c 262144 f; echo; tail -c 1048576 f; } >/dev/null` (no grep, no awk) | 1.442 s (1.517 s second run) | 0.363 s | 1.130 s |
| 2 | same, piped through `LC_ALL=C grep -oE '"cwd":"([^"\\]|\\.)*"' \| awk '!seen[$0]++'` (LC_ALL=C given to grep on the command line) | 6.460 s | 3.475 s | 4.488 s |
| 3 | identical pipeline with the shell's own locale (LANG=C.UTF-8, LC_ALL unset), as session_home really runs it | 13.227 s | 9.992 s | 4.493 s |

Reading: reading the two file ends is cheap (Arm 1, 1.4 s). The `grep -oE` stage is the cost, and it doubles in the UTF-8 locale (Arm 3 vs Arm 2). The traced session_home self time was 12.16 s (tier1 trace), close to Arm 3.

Locale finding (2026-11-17T19:03:28Z): ccsession:1383 declares `local store want cwd first="" LC_ALL=C` and ccsession:1403 (session_branch) declares `local b LC_ALL=C`, intending the byte-wise "C" locale for the grep. In bash a `local` variable that was not already exported is not passed to child processes: `bash -c 'f() { local x LC_ALL=C; env | grep -c "^LC_ALL="; }; f'` prints 0, and `LC_ALL` is unset in this shell (LANG=C.UTF-8); `grep -n 'export LC_ALL\|export LANG'` on the script finds no export. So the grep in session_home runs in the user's UTF-8 locale and pays the roughly 2x regex cost seen between Arm 3 and Arm 2. (Only the command-prefix forms `LC_ALL=C tr ...` at ccsession:686, 689, 694 do reach their processes.)

## End-to-end locale probe (2026-11-17T19:07:38Z to 19:09:38Z; locale-probe.txt; same shell, same store, alternated, read-only; load average at start 9.76, at end 4.19)

| Run | plain `ccsession --here` | `env LC_ALL=C ccsession --here` | gap |
|---|---|---|---|
| 1 | 23.586 s | 16.657 s | 6.93 s |
| 2 | 24.663 s | 16.244 s | 8.42 s |
| 3 | 22.471 s | 16.597 s | 5.87 s |
| median | 23.586 s | 16.597 s | 6.99 s (29.6% of the plain run) |

Reading: the unexported `LC_ALL=C` (ccsession:1383) costs about 7 s of a 23.6 s listing end to end on this machine (LANG=C.UTF-8). Each pair gap exceeds the 3.38 s threshold preregistered by the performance-engineer card and the 4.0 s threshold of the root-cause-analyst card. Caveats: this exports LC_ALL=C for the whole script (also bash glob collation and `date`), not only for grep; only the grep stage is the intended cause; the plain times here (22.5-24.7 s) are lower than the first run (27.07 s) because the machine load was lower, so the 20 s the reporter sees is within the range of this store on a quieter machine.

- `bash --version` is 5.2.37 here; bash 3.2 (macOS) is the compatibility floor stated in ccsession comments (I:1690, I:1823) and has no `printf '%(...)T'` builtin time formatting.
