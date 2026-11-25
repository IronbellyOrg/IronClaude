# Fix proposal 3: staged: ship the bash quick win first (it becomes the fallback), then the python3 batch helper (system-architect card)

## Problem statement (shared by all three proposals)

`ccsession --ask` (run by ccsession-orca for every new plain Claude tab) builds the saved-session list with `list_sessions` (`/home/coder/.claude/skills/ccsession-tag/ccsession:1554-1663`, byte-identical to origin/master 10f6ec670). With 477 saved names it takes 22.5-27.1 s on a 28-core machine (27.069 s at load 11.9; 22.5-24.7 s at lower load), user 5.8 s, sys 13.6 s, with nothing printed until the whole list is built (I:1718 captures it inside `$(...)`), then the 30 s question starts inside Orca's 60 s readiness window (I:1733-1735). Captured costs: session_home 12.16 s (pipeline `head | tail | grep -oE | awk` per session, I:1396-1397), list_sessions loop body 5.12 s, format_epoch 2.68 s (878 failing `date -r` first, then `date -d`), get_btime + get_mtime 2.42 s, session_transcript 2.03 s, session_place 1.95 s. Locale defect: `local ... LC_ALL=C` (I:1383, 1403) is not exported, so grep runs in UTF-8; `LC_ALL=C ccsession --here` ran 16.2-16.7 s against 22.5-24.7 s plain (median gap 6.99 s).

## Proposed change

Stage 1 (ccsession only; becomes the fallback of stage 2): prefix `LC_ALL=C` on grep and awk in session_home and session_branch (keep the `local LC_ALL=C` for bash's own matching); probe the `date` flavour once with `date --version` and use `date -d` only on GNU (keep BSD-first order on non-GNU); one `stat -c '%W %Y'` per row, GNU first; basename/dirname/`head -n 1` become `${x##*/}`, `${x%/*}` and `IFS= read -r uuid < file || true` (the `|| true` because of `set -e`, I:132); build one `ls -t "$PROJECTS_DIR"/*/*.jsonl` index in memory on the first miss and pick the first line ending in `/<uuid>.jsonl` (newest copy, no file written); keep every construct bash 3.2 safe (no associative arrays, `mapfile` or `printf '%(...)T'`). Stage 2: a python3 helper called once per list (inside the `first` block so the lazy heading holds) that prints one `\x1f`-separated record per input uuid in input order (path, then the session's start folder): index of the newest copy, head 256 KiB then tail 1 MiB scanned as bytes, the two unescape replacements in the order of I:1388-1389 (not `json.loads`), per-byte folder match against the store folder, first-cwd fallback and dedup as in I:1390-1398, head read first and the tail skipped when a store-matching folder is found; bash captures it inside `if out=$(...); then` and any failure runs stage 1 unchanged; nothing is written; birth time stays in `stat -c '%W'`. Stage 3 (optional, only if stage 2 still shows more than about 2 s in stat and date): move stat and date strings into the helper with their own parity test.

## Evidence

system-architect card (tier2-system-architect-hypothesis.md): stage 1 lower bound about 14.6 s remaining of 27.07 s (itemised additive savings 12.47 s using a 1.2 ms per-fork proxy for dirname/basename/head, not measured); stage 2 A-core 4.62 s and A-full 2.70 s remaining (derived, not executed); end-to-end locale probe (median gap 6.99 s). The stage order is argued by the timing window: the `--ask` budget is 60 - 30 = 30 s, the list at 27.07 s leaves 2.93 s, so a store about 11% larger makes an unanswered question outlast Orca's 60 s window (I:1733-1735).

## Risks

Helper drift (unescape order, bytes vs characters, first-cwd fallback, `ls -t` ties, symlinked or directory-named `*.jsonl`, a file deleted between index and stat); the `date --version` probe must not break BSD; python startup where `python3` is the macOS stub (unverified); more than 3 files at stage 2 (script, helper, test file, README maybe); the stage 1 savings use an unmeasured per-fork proxy.

## Test plan

Existing `_listed` tests unchanged; parity A/B/C (helper vs python3 hidden from PATH, all three views, byte-identical stdout, stderr and exit code; fixtures: transcript missing, only elsewhere, two copies, store folder only in the tail, first cwd not matching, escaped quote and backslash in a cwd, non-ASCII cwd, file under 256 KiB and over 1.25 MiB, deleted folder, `%W` printing 0); spawn-count shim test N=10 vs N=60; locale shim asserting `LC_ALL=C` in grep's environment; no file under HOME or TMPDIR; a static test rejecting bash 4 constructs in the changed region. Success measure: the same Task 1 trace and `time ccsession --here` / `--list` three times each on the same store, with `uptime` recorded, compared to 27.069 s and 14.473 s.

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
