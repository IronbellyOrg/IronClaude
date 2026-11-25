# Hypothesis (Tier 2, root-cause-analyst): list_sessions forks about 14 processes per saved name, and its largest per-row step runs grep in UTF-8 because `local LC_ALL=C` is never exported

(Persisted by the parent from the troubleshoot-analyst return, lens root-cause-analyst (independent second opinion); condensed, no claim changed. I = /home/coder/.claude/skills/ccsession-tag/ccsession; numbers come from tier1-observation.md.)

**Tier**: 2   **Timestamp**: unobserved (worker has no clock; the parent's stamp is the persist time of this file)
**Cause class**: Performance/resource (N+1 process spawning) plus a latent wrong-environment bug (locale not exported)
**Claim class**: `mixed` (runtime_behavior for spawn cost, environment_dependent for the locale penalty)
**Evidence class**: `runtime_trace` (parent-captured trace and arms; I:1383 read as source)
**Verdict direction**: AFFIRM Tier 1's per-session-process claim with a different ranking and a narrower fix
**Consistency with docs**: no_docs_found for speed; aligned for the output contract
runs-in=coder workspace, one bash process

## Claim

Two defects plus small members of the first. D1 (design): list_sessions (I:1554-1663) runs a fresh set of external processes per topic file with no batching: 477 rows at 56.7 ms each (27.07 s wall, about 6,900 processes). D2 (bug): the cwd scan (I:1396-1397) was meant to run in the C locale but `local ... LC_ALL=C` (I:1383) is not exported, so `grep -oE` runs in the user's UTF-8 locale: 13.2 s on the 439 transcripts against 6.5 s in the C locale on the same files.

Root cause for an issue (worker): "`ccsession --ask` runs about 14 external processes per saved session (6,900 for 477 rows, 56.7 ms per row, 27.1 s wall). Its biggest step, the per-transcript cwd scan, takes 12.2 s, about 6.8 s of it because `local LC_ALL=C` is not exported and `grep` runs in UTF-8."

## Ranking by captured numbers (shares of 27.07 s wall; self times overlap, 0.57 s unattributed)

| # | Cause | Captured cost | Share | Standalone fix size |
|---|---|---|---|---|
| 1 | D2 locale: Arm 3 minus Arm 2 (13.227 s vs 6.460 s) | 6.77 s | 25% | one line |
| 2 | `grep -oE`/`awk` per session even in C locale: Arm 2 minus Arm 1 (6.460 s vs 1.442 s) | 5.02 s | 18.5% | needs the helper |
| 3 | Per-row spawns outside session_home: loop body 5.12, format_epoch 2.68, get_btime+get_mtime 2.42, session_transcript 2.03, session_place 1.95, format_duration 0.14 | 14.34 s | 53% | needs the helper |
| 4 | Reading the file ends (Arm 1) | 1.44 s | 5% | cannot go below this |
| 5 | Failing `date -r` first (878 times) | about 1.1 s | 4% | swap the order |
| 6 | Glob across 437 folders | 2.03 s (inside row 3) | 7.5% | one-pass index |

Cross-check (worker): `--list` (no session_home, no session_place) costs 14.473 s / 609 rows = 23.8 ms per row; `--here` costs 56.7 ms per row; the 33 ms per-row difference matches session_home plus session_place (12.16 + 1.95 s over 439 calls = 32 ms). The reported 5-10% CPU is not explained: measured 19.4 s CPU in 27.1 s wall, about 0.7 core of 28 (about 2.5% of this machine); it would match a machine with 7-14 cores or fewer (worker arithmetic, unverified).

## Evidence

- E1 I:1383 `local store want cwd first="" LC_ALL=C`; parent probe `bash -c 'f() { local x LC_ALL=C; env | grep -c "^LC_ALL="; }; f'` printed 0; LC_ALL is unset here (LANG=C.UTF-8); only I:686, 689, 694 reach a child with `LC_ALL=C` (grep of I for LC_ALL: lines 686, 689, 694, 1383, 1403).
- E2 Arms 1-3 (tier1-observation.md): 1.442 s (1.517 s second run), 6.460 s, 13.227 s over 439 files, 3,848 MB; Arms 2 and 3 differ only in locale but each ran once under load average 11.9 (noise unknown).
- E3 I:1480-1483 and I:1595-1600: transcripts live in per-cwd folders, so every row misses `$(dirname "$ws_dir")/$uuid.jsonl` and pays `ls -t "$PROJECTS_DIR"/*/<uuid>.jsonl | head` (0.005 s per call, 2.4 s for 477); test fixtures write transcripts the same way (`_transcript`, tests/unit/test_ccsession_tag.py:3820-3835).
- E4 /tmp/ccs-proto/proto.py:29,52: the prototype returns in 0.73 s for 554 MB but does not apply the "first cwd whose sanitised name equals the store" rule and prints no rows; 0.75 s is a bound for the scan, not for the finished list.

## Triggers beyond list size (worker answers)

- The list runs only when ccsession-orca decides to ask (ccsession-orca:141-155 and 197-204): terminal on stdin and stdout, autostart on, no resume, no valid CCSESSION_NAME, no prompt or prefill. A plain tab relaunch with ORCA_PANE_KEY reopens the saved session without asking (ccsession-orca:164-191). `ask_session_name` returns before listing only if keys are already waiting (I:1698-1701). Every new plain Claude tab pays the list whatever the answer. The Coder New Terminal hook was not read (unverified).
- It scales with the rows in this repo's list (the scope_slug skip at I:1573 leaves the other 18 lists alone) and, through the glob, with the 437 workspace folders. session_home runs for all rows to sort them into here/gone/other (I:1606-1608) while only here and gone rows print.
- Output is held back: `sessions=$(... list_sessions ...)` (I:1718) captures everything first, so the terminal shows nothing for the whole listing and then the 30 s question starts: about 57 s of Orca's 60 s readiness window (I:1733-1735).
- The `*` answer runs list_sessions again with filter "" (I:1771): about 11 s for 477 rows (derived from 23.8 ms per row, not measured).
- If the user already exports LC_ALL, or runs a plain C/POSIX locale, D2 costs little (how bash's `local` treats an already-exported variable is unverified); the 20 s reported against 27 s here may partly be this difference.

## Proposed Fix (one fix, differs from Tier 1 in shape)

A python3 helper `scan_sessions.py` beside the script, called once per list_sessions run; it does everything that needs a process per row today and prints row fields as tab-separated text; bash keeps only printing and session_place.

- Input: bash passes the topic files in its own glob order on stdin through the `printf` builtin, so row order stays identical (Python's sort and bash's locale-collated glob can differ).
- It takes each file's first line as the uuid, looks it up in one scan of `$PROJECTS_DIR/*/*.jsonl` (newest wins, rule at I:1481-1482), applies the head 256 KiB + tail 1 MiB scan with the same "first cwd whose sanitised name equals the store, else the first" rule including the JSON unescaping at I:1386-1389.
- Times: one `stat` call for all files (GNU `-c '%W %Y %n'` first, BSD `-f '%B %m %N'` only on failure) because Python has no portable Linux birth time; times formatted with `time.strftime('%Y-%m-%d %H:%M')` and the duration as format_duration does.
- Fallback: if python3 or the helper fails or gives short output, the existing per-row code runs unchanged; fix D2 there with `export LC_ALL=C` inside the subshell or `LC_ALL=C grep`, and try `date -d "@$e"` before `date -r`, in the same diff, so the fallback does not keep the bug.
- Difference from Tier 1: Tier 1's plan keeps stat and date per row in bash (about 5 s of fork cost left) and leaves the bug in the fallback; the one-line export alone removes about 6.8 s but the captured numbers leave about 20 s, so it does not meet the symptom.

Install route (read by the worker): `install.sh:40` runs `cp -R "$SKILL_DIR"/. "$TARGET_SKILL_DIR"/` and `src/superclaude/cli/install_skill.py:52` calls `shutil.copytree(skill_source, skill_target)`, so a new `.py` is installed with no manifest edit; only named scripts get chmod +x (install.sh:48-52), and a `.py` called as `python3 "$CCSESSION_DIR/scan_sessions.py"` needs none; the existing call at I:1674-1675 is the precedent. The checkout copy has no retention.py (older than origin/master); how `_self` resolves a symlink (I:150-158) and the plugins/superclaude/ mirror are unverified.

Files: 3 (`src/superclaude/skills/ccsession-tag/ccsession`, new `scan_sessions.py`, `tests/unit/test_ccsession_tag.py`), a fourth (`README.md`) only if it should mention the helper; `.claude/` copies come from `make sync-dev` and are never staged. A written-plan change, not a direct edit.

Tests: (1) spawn count: counting wrappers for date, stat, head, ls, basename, dirname, grep and awk first on PATH (each appends its name to a log and execs the real binary resolved with `command -v`; precedent `_slow_probe` tests/unit/test_ccsession_tag.py:1967-1977 and `_fake_orca` :3912-3939); N=10 and N=60 topic files built with `_transcript` (:3820) and topics as at :4567-4569; run `_ccs(main, env, "--here")` (:3838); assert the count grows by at most a small constant, not about 14 per row. (2) fallback and output identity: a python3 shim that exits 1 only when `"$*"` contains `scan_sessions` and otherwise execs the real python3; stdout of `--here` must be byte-identical to the helper run; use fixtures `_three_worktrees` (:4474-4504, 4585-4594) and the copied-from-another-machine case (:4551-4573); the `_listed` regex (:3897-3909) pins the row format. Tests 4522 and 3465 and others not read in full (unverified). Re-run `time ccsession --here` against 27.07 s and 14.47 s; no prediction.

## Confidence

Self-reported: 0.8 for the diagnosis, 0.65 for how much the fix will save. Evidence grounding 1.0; runtime check 1.0 (parent-run reproduction and arms; the worker's reading of I:1383 matches the parent's env probe); symptom coverage 0.5 (5-10% CPU not covered; 2.5% here); reproducibility fit 1.0; fix directness 0.5 (helper unwritten; the prototype omits the matching rule and session_place); domain coherence 1.0.

## Risks

Row order (a helper that sorts itself can reorder rows; pass bash's ordered list in; a missing or odd file name (spaces, newlines) would break one-record-per-line pairing; quote and test the pairing); cwd rule (first matching cwd, else first, and JSON unescaping, or here/gone/other drifts: tests 4474-4594); birth time (stat stays a subprocess, one call; failure yields "(times unavailable)" as before); missing python3 (fallback stays slow as today).

## If I'm wrong, it's probably because

The Arm 3 vs Arm 2 gap is load or cache noise (single run each, load average 11.9), so the locale is worth much less than 6.8 s and the helper must carry nearly all the saving.

## Falsification standard (worker)

# Discriminator: does the unexported locale cost seconds end to end?
Hypothesis A: `grep` in session_home runs in the shell's UTF-8 locale and that adds seconds to a real `ccsession --here`.
Hypothesis B: the Arm 3 vs Arm 2 gap was run-order, cache or load noise, so a real run with `LC_ALL=C` exported is not meaningfully faster.
Observable that differs: (median of 3 plain `ccsession --here` wall times) minus (median of 3 `LC_ALL=C ccsession --here` wall times) >= 4.0 s, runs alternated plain/C, same shell, same store, 3 each.
Exact probe: parent-run, read-only: alternate plain and `LC_ALL=C` `ccsession --here`, six runs; any failed or missing run makes it unobserved, never false.
Primitive under dispute: I:1383 `local store want cwd first="" LC_ALL=C` and I:1396-1397 `done < <({ head -c 262144 "$1"; echo; tail -c 1048576 "$1"; } 2>/dev/null | grep -oE '"cwd":"([^"\\]|\\.)*"' | awk '!seen[$0]++')`.
Reference-context value: n/a (first instrumented run of this probe; the six-run capture is the reference).
Pre-registered outcomes: true -> A consistent (gap of 4 s or more with LC_ALL=C), B refuted; false -> A refuted for a gap of 4 s or more (a smaller gap is not excluded), B consistent (not proof, since the arms measure only the scan).
Falsifier: "If the median gap is below 4.0 s in complete alternated captures, A is false at that size and the locale is a minor item; the helper's saving must then be justified by D1 alone." Exporting LC_ALL=C for the whole script also changes bash glob collation, so compare row order separately.

## Alternatives considered

Locale as the single root cause (rejected: 6.77 s of 27.07 s; the non-session_home rows are 14.3 s without any grep); glob across 437 folders (rejected as dominant, 2.03 s, 7.5%); failing `date -r` (about 1.1 s); model refresh (0.17 s); cache file (rejected: README:190).

## Grounding gaps (worker)

Not read: list_heading, ensure_names_migrated, I lines 1-1369 except grep hits (so how `_self` resolves and where LANG comes from), retention.py, the Coder hook, tests 3465 and the `_three_worktrees` body. Arm 2 vs Arm 3 is a single run each under load 11.9 (the probe above is meant to settle it). Cold-cache cost of reading 554 MB not measured. Why `grep -oE` is slow even in the C locale and which locale the reporter had are unverified. Whether a Python `re` scan reproduces the matching rule at the same speed is not measured. Diagnosability verdict partial (not read by the worker).
