# Fix proposal 1: one python3 batch helper for the listing, with the bash path kept as fallback (Tier 1 card and root-cause-analyst card)

## Problem statement (shared by all three proposals)

`ccsession --ask` (run by ccsession-orca for every new plain Claude tab) builds the saved-session list with `list_sessions` (`/home/coder/.claude/skills/ccsession-tag/ccsession:1554-1663`, byte-identical to origin/master 10f6ec670). With 477 saved names it takes 22.5-27.1 s on a 28-core machine (27.069 s at load 11.9; 22.5-24.7 s at lower load), user 5.8 s, sys 13.6 s, with nothing printed until the whole list is built (I:1718 captures it inside `$(...)`), then the 30 s question starts inside Orca's 60 s readiness window (I:1733-1735). Captured costs: session_home 12.16 s (pipeline `head | tail | grep -oE | awk` per session, I:1396-1397), list_sessions loop body 5.12 s, format_epoch 2.68 s (878 failing `date -r` first, then `date -d`), get_btime + get_mtime 2.42 s, session_transcript 2.03 s, session_place 1.95 s. Locale defect: `local ... LC_ALL=C` (I:1383, 1403) is not exported, so grep runs in UTF-8; `LC_ALL=C ccsession --here` ran 16.2-16.7 s against 22.5-24.7 s plain (median gap 6.99 s).

## Proposed change

Add a python3 helper `scan_sessions.py` beside `retention.py` in `src/superclaude/skills/ccsession-tag/` (precedent: I:1674-1675 calls a python3 helper in `$CCSESSION_DIR`), called once per list_sessions run. Input: bash passes the topic files' uuids in its own glob order, so row order stays identical. The helper does one directory scan mapping uuid to the newest transcript (rule of I:1481-1482), then the same head 256 KiB + tail 1 MiB scan with the same rule "first cwd whose sanitised name equals the store folder, else the first cwd" including the JSON unescaping at I:1386-1389, and prints one tab-separated record per uuid. It writes no file and still reads only the two ends of each transcript. Bash keeps one `stat -c '%W %Y'` per row (GNU first, BSD fallback), session_place per row, row formatting and colours. Fallback: when python3 or the helper fails or gives short output, the existing per-row code runs unchanged, with the locale fixed there (`LC_ALL=C` prefix on grep and awk in session_home and session_branch) and `date -d "@$e"` tried before `date -r` on GNU.

## Evidence

Tier 1 and root-cause-analyst cards (tier1-hypothesis.md, tier2-root-cause-analyst-hypothesis.md); prototype of the index plus scan: 0.75 s total for 439 sessions, 554 MB read (tier1-observation.md); Arms 1-3 and the end-to-end locale probe. Expected saving (derived): session_home 12.16 s and session_transcript 2.03 s replaced by about 0.75 s, so about 13.4 s of 27.07 s; the remaining about 13.6 s is loop 5.12 + format_epoch 2.68 + stat 2.42 + place 1.95 + duration 0.14 + unattributed 0.57 + helper 0.75.

## Risks

Behaviour drift of the helper against the pinned cwd rule (tests 4474-4594: here/gone/other); one-record-per-line pairing with odd file names; birth time stays in bash because Python has no portable Linux birth time; the fallback stays slow where python3 is missing; more than 3 files (script, new helper, test file, possibly README).

## Test plan

Existing `_listed` tests and the pinned-format tests must pass unchanged; new parity test (helper vs python3 hidden from PATH, byte-identical stdout/stderr/exit code on all three views); spawn-count shim test N=10 vs N=60; locale shim asserting `LC_ALL=C` reaches grep; no file written under HOME or TMPDIR.

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
