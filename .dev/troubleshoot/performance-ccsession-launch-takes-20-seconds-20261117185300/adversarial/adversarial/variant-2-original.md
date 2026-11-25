# Fix proposal 2: bash-only: fix the grep locale and replace the per-row spawns with builtins, in ccsession alone (performance-engineer card)

## Problem statement (shared by all three proposals)

`ccsession --ask` (run by ccsession-orca for every new plain Claude tab) builds the saved-session list with `list_sessions` (`/home/coder/.claude/skills/ccsession-tag/ccsession:1554-1663`, byte-identical to origin/master 10f6ec670). With 477 saved names it takes 22.5-27.1 s on a 28-core machine (27.069 s at load 11.9; 22.5-24.7 s at lower load), user 5.8 s, sys 13.6 s, with nothing printed until the whole list is built (I:1718 captures it inside `$(...)`), then the 30 s question starts inside Orca's 60 s readiness window (I:1733-1735). Captured costs: session_home 12.16 s (pipeline `head | tail | grep -oE | awk` per session, I:1396-1397), list_sessions loop body 5.12 s, format_epoch 2.68 s (878 failing `date -r` first, then `date -d`), get_btime + get_mtime 2.42 s, session_transcript 2.03 s, session_place 1.95 s. Locale defect: `local ... LC_ALL=C` (I:1383, 1403) is not exported, so grep runs in UTF-8; `LC_ALL=C ccsession --here` ran 16.2-16.7 s against 22.5-24.7 s plain (median gap 6.99 s).

## Proposed change

Edit `ccsession` only (plus its test file): (a) prefix `LC_ALL=C` on the grep and awk in session_home and on the grep in session_branch, in the same command-prefix form as I:686, 689, 694; (b) replace per-row spawns: `date` via bash `printf -v ... '%(%Y-%m-%d %H:%M)T'` when `BASH_VERSINFO` >= 4.2 (else the current path, so bash 3.2 is untouched) or at least stop trying `date -r` first on GNU; one `stat -c '%W %Y'` per file; dirname, basename and `head -n 1` become parameter expansion and `read -r` with `dirname "$ws_dir"` hoisted out of the row loop; session_transcript uses a builtin glob plus `-nt` instead of `ls -t | head -n 1`. No python3 helper.

## Evidence

performance-engineer card (tier2-performance-engineer-hypothesis.md): derived savings (a) 6.2-6.8 s, b1+ up to 2.68 s, b2 0.87-1.20 s, b3 about 2.8 s (assumes these coreutils cost as much as `date`, 1.53 ms: unverified), b4 1.12-2.03 s; a+b 13.0-15.5 s saved, remaining 11.6-14.1 s of 27.07 s. Measured: the locale change alone shortened `ccsession --here` by a median 6.99 s end to end (LC_ALL=C exported for the whole script).

## Risks

The locale change alters output only for working folders with invalid UTF-8 bytes; `printf '%(...)T'` local-time and DST edges unverified; the `-nt` glob may break ties differently from `ls -t`; the savings of b3 and b4 borrow per-spawn costs and are not measured; the per-session scan (Arm 2: 6.46 s with C locale) stays, so the result stays above the 0.75 s helper bound; user-time inconsistency noted by the worker (whole-run user 5.8 s vs Arm 3 user 10.0 s) is unresolved.

## Test plan

A shim `grep` on PATH that records `$LC_ALL` and must see `C`; spawn-count shims for date, dirname, basename, head, stat, ls at N=10 vs N=60 requiring no growth; existing pinned-format tests byte-identical; a static check that the changed region uses no bash 4 construct unguarded.

## Documented constraints to honor

(Verbatim copy of the Restrictions and Re-frame signals sections of doc-context.md.)

- `I:1380` (session_home) — "# Only the start and the end of the file are read (transcripts can be" gigabytes: a fix must not read whole transcripts and must keep both ends.
- `I:1378` (session_home) — "# <transcript> -> the folder the session was started in: the first recorded folder whose name matches the transcript's folder, else the first one."
- `I:1481` (session_transcript) — "# <session id> -> its transcript (the newest copy), or nothing."
- `I:1490` and `I:1516` (get_btime, get_mtime) — GNU `stat -c` first; BSD `stat -f` must never run first on Linux.
- `I:1533` (format_epoch) — BSD `date -r` first, GNU `date -d @` fallback; format `%Y-%m-%d %H:%M`.
- `I:1690` and `I:1823` (ask_session_name, ask_drain_waiting) — bash 3.2 (macOS) compatibility: no `read -t 0`, no fractional `read -t`.
- `I:1733` (ask_session_name) — "Every question gives up after CCSESSION_ASK_TIMEOUT seconds (default 30; 0 waits for ever): Orca fails a supervised worker whose Claude is not ready within 60 seconds"; listing time runs before the question.
- `/home/coder/.claude/skills/ccsession-tag/README.md:190` — "Listing never writes any file."
- README:275 — `last` in the list is each transcript's change time; nothing touches transcript files.
- Output formats pinned by tests (row format, "(transcript missing)", "(times unavailable)", "(was <folder>)", "N more sessions in other worktrees of this repo", first two lines dropped by show_saved): tests/unit/test_ccsession_tag.py `_listed` helper (line 3897) and tests at 4474, 4522, 4551, 4585, 3465, 2740.
- Re-frame: no document sets a speed or CPU target; the `--ask` list runs before the 30 s question and counts against Orca's 60 s readiness window; any fix must keep output text, exit codes (0, 1, 3, 130), the stdout/stderr split, the here/gone/other classification and "Listing never writes any file".
