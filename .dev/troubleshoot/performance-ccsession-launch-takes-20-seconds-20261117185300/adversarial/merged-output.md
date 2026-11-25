<!-- Provenance: produced by /sc:adversarial; Base: Variant 3 (staged); Merge date: 2026-11-17 -->

# Fix proposal 3: staged: ship the bash quick win first (it becomes the fallback), then the python3 batch helper (system-architect card)

## Problem statement

<!-- Source: Base (original, modified) - I:<n> notation defined on first use, per Change #7(a) -->

`ccsession --ask` (run by ccsession-orca for every new plain Claude tab) builds the saved-session list with `list_sessions` (`/home/coder/.claude/skills/ccsession-tag/ccsession:1554-1663`; in this document `I:<n>` means line n of that installed file, which is byte-identical to origin/master 10f6ec670). With 477 saved names it takes 22.5-27.1 s on a 28-core machine (27.069 s at load 11.9; 22.5-24.7 s at lower load), user 5.8 s, sys 13.6 s, with nothing printed until the whole list is built (I:1718 captures it inside `$(...)`), then the 30 s question starts inside Orca's 60 s readiness window (I:1733-1735). Captured costs: session_home 12.16 s (pipeline `head | tail | grep -oE | awk` per session, I:1396-1397), list_sessions loop body 5.12 s, format_epoch 2.68 s (878 failing `date -r` first, then `date -d`), get_btime + get_mtime 2.42 s, session_transcript 2.03 s, session_place 1.95 s. Locale defect: `local ... LC_ALL=C` (I:1383, 1403) is not exported, so grep runs in UTF-8; `LC_ALL=C ccsession --here` ran 16.2-16.7 s against 22.5-24.7 s plain (median gap 6.99 s).

## Proposed change

The change ships in three stages. Stage 1 can ship alone and stays in place afterwards as the fallback of Stage 2. Stage 3 is optional.

### Stage 1: ccsession only (becomes the fallback of Stage 2)

<!-- Source: Base (original) -->

- Locale: prefix `LC_ALL=C` on grep and awk in session_home and session_branch (keep the `local LC_ALL=C` for bash's own matching).
- Date flavour: probe the `date` flavour once with `date --version` and use `date -d` only on GNU (keep BSD-first order on non-GNU).
- Stat: one `stat -c '%W %Y'` per row, GNU first.
- Spawns to builtins: basename, dirname and `head -n 1` become `${x##*/}`, `${x%/*}` and `IFS= read -r uuid < file || true` (the `|| true` because of `set -e`, I:132).
- Transcript lookup: build one `ls -t "$PROJECTS_DIR"/*/*.jsonl` index in memory on the first miss and pick the first line ending in `/<uuid>.jsonl` (newest copy, no file written).
- Bash 3.2: keep every construct bash 3.2 safe (no associative arrays, `mapfile` or `printf '%(...)T'`).

<!-- Source: Variant 3 (base), Stage 1 date item - modified per Change #9 -->

- Why `printf '%(...)T'` is not used for dates: bash 3.2 (macOS) lacks it (I:1690, 1823 state the bash 3.2 floor); the `date --version` probe on GNU and the BSD-first order elsewhere keep format_epoch's text and both platforms (I:1533-1537).

<!-- Source: Variant 2, Section "Proposed change" and Test plan (U-003) - merged per Change #4 -->

- Optional, measure first: rows classified `other` are built and discarded after get_btime, get_mtime and format_epoch ran (I:1610-1627, 1636); classifying first would skip that work (about 0.9 s on assumptions about the count of `other` rows, not derived exactly); keep only if the trace shows it and the output stays byte-identical.

<!-- Source: Variant 2, Section "Proposed change" (C-011) - merged per Change #5 -->

File count: Stage 1 touches 2 files (`ccsession`, `tests/unit/test_ccsession_tag.py`) and can ship as its own change.

### Stage 2: one python3 helper per list

<!-- Source: Base (original, modified) - helper named and placed per Change #1 -->

Add `scan_sessions.py` beside `retention.py` in `src/superclaude/skills/ccsession-tag/` (precedent: I:1674-1675 calls a python3 helper in `$CCSESSION_DIR`; install route: `install.sh:40` and `src/superclaude/cli/install_skill.py:52` copy the whole skill folder, so no manifest edit). It is called once per list (inside the `first` block so the lazy heading holds) and prints one `\x1f`-separated record per input uuid in input order (path, then the session's start folder). It does:

- an index of the newest copy of each transcript;
- head 256 KiB then tail 1 MiB scanned as bytes;
- the two unescape replacements in the order of I:1388-1389 (not `json.loads`);
- per-byte folder match against the store folder;
- first-cwd fallback and dedup as in I:1390-1398;
- head read first and the tail skipped when a store-matching folder is found.

Bash captures the output inside `if out=$(...); then` and any failure runs Stage 1 unchanged. Nothing is written. Birth time stays in `stat -c '%W'`.

<!-- Source: Variant 2, Section "Proposed change" (C-011) - merged per Change #5 -->

File count: Stage 2 touches 3 to 4 files (`ccsession`, `scan_sessions.py`, the test file, README only if it should mention the helper).

### Stage 3: optional

<!-- Source: Base (original) -->

Only if Stage 2 still shows more than about 2 s in stat and date: move stat and date strings into the helper with their own parity test.

## Evidence

<!-- Source: Base (original, modified) - measured locale probe leads, derived estimates relabelled per Change #8; A-core/A-full defined per Change #7(a) -->

Measured (tier1-observation.md, parent-captured, same shell, same store, alternated, read-only):

| Run | plain `ccsession --here` | `env LC_ALL=C ccsession --here` | gap |
|---|---|---|---|
| 1 | 23.586 s | 16.657 s | 6.93 s |
| 2 | 24.663 s | 16.244 s | 8.42 s |
| 3 | 22.471 s | 16.597 s | 5.87 s |
| median | 23.586 s | 16.597 s | 6.99 s |

Machine load fell from 9.76 to 4.19 during the probe. This is the measured part of Stage 1: the unexported `LC_ALL=C` costs about 7 s of a 23.6 s listing. Caveat from the source: the probe exports `LC_ALL=C` for the whole script (also bash glob collation and `date`), not only for grep; only the grep stage is the intended cause.

<!-- Source: Variant 1, Section "Evidence" - merged per Change #6 (reference for gate A-002) -->

Measured: a throwaway prototype of the index plus the head 256 KiB and tail 1 MiB scan ran in 0.75 s total for 439 sessions, 554 MB read, with no process spawned per session (tier1-observation.md; it omits session_place's git calls and ran warm).

Derived, not executed, split unresolved in the debate (C-010): the remaining time of the 27.07 s run is about 13.6 s for the Variant 1 helper design, 11.6-14.1 s for the Variant 2 bash-only design, and about 14.6 s for Stage 1 of this proposal (system-architect card, tier2-system-architect-hypothesis.md: itemised additive savings 12.47 s using a 1.2 ms per-fork proxy for dirname/basename/head, not measured). For Stage 2, two derived variants remain, neither executed: A-core (the helper does the index and the scan, bash keeps one `stat` and one `date -d` per timestamp) leaves 4.62 s, and A-full (the helper does the stat and date strings as well) leaves 2.70 s.

<!-- Source: Base (original) -->

The stage order is argued by the timing window: the `--ask` budget is 60 - 30 = 30 s, the list at 27.07 s leaves 2.93 s, so a store about 11% larger makes an unanswered question outlast Orca's 60 s window (I:1733-1735).

## Risks

<!-- Source: Base (original, modified) - risks restated as a table per Change #7(b); rows added per Changes #2, #3 and #4 -->

Probability and impact are qualitative labels, not measurements.

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Helper drift against the pinned cwd rule (unescape order, bytes vs characters, first-cwd fallback, `ls -t` ties, symlinked or directory-named `*.jsonl`, a file deleted between index and stat) | Medium | Wrong start folder, so the here/gone/other class changes | Parity test of the helper against the python3-hidden bash path on all three views; byte-identical stdout, stderr and exit code; the fixtures listed in the Test plan |
| One-record-per-input-uuid pairing breaks if an input line is missing or odd (file names with spaces; labels reject control characters, `validate_label` at `ccsession:315`) | Low | Rows paired with the wrong record | Fixture with topic names with spaces and with `%2F` escapes, and one topic file whose uuid has no transcript; any short or odd output runs Stage 1 unchanged |
| Locale output change: the C locale restores the intended byte-wise match, so a UTF-8 grep may drop working folders with invalid UTF-8 bytes while a C-locale grep keeps them (worker knowledge of GNU grep, unverified) | Low | Output differs for folders with invalid UTF-8 bytes only | Pin it with a fixture whose cwd holds invalid UTF-8 bytes |
| python3 missing, or python startup where `python3` is the macOS stub (unverified) | Low to Medium | Helper path fails or is slow | Any helper failure runs Stage 1 unchanged inside `if out=$(...); then`; test with python3 hidden from PATH |
| The `date --version` probe breaks BSD | Low | Wrong date text on macOS | Probe once; use `date -d` only on GNU; keep BSD-first order elsewhere (I:1533-1537) |
| Timing window on larger stores: Stage 1 alone leaves about 14.6 s (derived) | Medium | A store about 11% larger at the unfixed 27.07 s makes an unanswered question outlast Orca's 60 s window | Ship Stage 2; gates A-002 and A-004 below |
| Stage 1 savings rest on an unmeasured per-fork proxy | Medium | The 2.8 s saving may be smaller | Gate A-004 below |
| Classifying `other` rows before get_btime, get_mtime and format_epoch (optional Stage 1 item) reorders computation | Medium | Output could change | Keep only if the trace shows the saving and the output stays byte-identical; otherwise do not adopt |
| More than 3 files at Stage 2 (script, helper, test file, README maybe) | Certain | A written plan is required | Stage 1 ships as its own 2-file change; Stage 2 is planned separately |

## Open assumptions and measurement gates

<!-- Source: Base (original, modified) - new section per Change #6; from debate points A-001, A-002, A-004, A-006 -->

| ID | Assumption | Gate |
|---|---|---|
| A-001 | The reporter's locale and store size are unverified | Capture `locale` and the number of topic files from the reporter, or reproduce with `LANG=en_US.UTF-8` |
| A-002 | Every timing and the 0.75 s prototype ran warm | Measure the Stage 2 helper once on a cold page cache before claiming its saving |
| A-004 | The 1.53 ms and 1.2 ms per-spawn proxies for `dirname`, `basename` and `head` are not measurements | Measure them (200 iterations) before relying on the 2.8 s saving |
| A-006 | `session_place` (1.95 s) and the held-back output (nothing prints until the whole list is built, I:1718) are left as they are | Printing rows as they are built changes the `show_saved` contract and is a separate follow-up |

## Out of scope

<!-- Source: Base (original, modified) - new section per Change #7(c) -->

- Bounding the list to the N newest rows.
- A cache file.
- Printing rows as they are built (see gate A-006).
- The hook that records the start folder.
- Stage 3, unless the trace shows more than about 2 s in stat and date.

## Test plan

<!-- Source: Base (original, modified) - fixtures appended per Changes #2 and #3 -->

Existing `_listed` tests unchanged; parity A/B/C (helper vs python3 hidden from PATH, all three views, byte-identical stdout, stderr and exit code; fixtures: transcript missing, only elsewhere, two copies, store folder only in the tail, first cwd not matching, escaped quote and backslash in a cwd, non-ASCII cwd, file under 256 KiB and over 1.25 MiB, deleted folder, `%W` printing 0); spawn-count shim test N=10 vs N=60; locale shim asserting `LC_ALL=C` in grep's environment; no file under HOME or TMPDIR; a static test rejecting bash 4 constructs in the changed region.

<!-- Source: Variant 1, Section "Risks" (U-004) - merged per Change #2 -->

Added fixture for the pairing risk: topic names with spaces and with `%2F` escapes, and one topic file whose uuid has no transcript.

<!-- Source: Variant 2, C-005 - merged per Change #3 -->

Added fixture for the locale risk: a cwd that holds invalid UTF-8 bytes.

## Success measure

<!-- Source: Base (original, modified) - split out of the Test plan paragraph; Task 1 trace defined and Stage 1 target stated per Changes #7(a) and #8 -->

Run the Task 1 trace (the `bash -x` PS4 timestamp trace of `ccsession --here` in diagnosability-tasklist.md Task 1) and `time ccsession --here` / `--list` three times each on the same store, with `uptime` recorded, and compare to 27.069 s and 14.473 s. The Stage 1 target is at or below the derived 14.6 s on the same store, to be confirmed by the same trace.

## Documented constraints to honor

<!-- Source: Base (original) - kept verbatim -->

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
