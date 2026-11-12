# QA Report: impl-core, edge-case lens (T183)

**Topic:** `superclaude sweep` Phase 1 core (`probes.py`, `classify.py`, `models.py`, `report.py`, tests, `.gitignore`)
**Date:** 2026-11-12
**Phase:** doc-qualitative adapted to code (edge-case lens), `fix_authorization: false`
**Fix cycle:** N/A (first review of this gate)

## How this was checked

All source files were read in chunks of at most 150 lines: `probes.py` (1-1294), `classify.py` (1-996), `models.py` (1-239), `report.py` (1-692), `tests/sweep/conftest.py`, `tests/sweep/test_readonly.py`, DESIGN `docs/designs/orchestrator-mode.md` sections 2.1, 2.2, 5, 6, 7.1-7.5, 10 and 11, the 1.0a facts file, the gitignore check, both pytest outputs and `phase8-validation.md`.

Beyond reading, the edge cases were executed against the real module (`probes` imported from `src/`, `PYTHONDONTWRITEBYTECODE=1`, temp files in a private `/tmp/ironclaude-batch.*` directory that was removed afterwards; `subprocess.run` and the two seams were faked, so no Orca or git process was started). Every result quoted below was produced by those runs unless it says "by reading".

Real-data cross-check for finding E2: of the 60 most recent transcripts under `/home/coder/.claude/projects`, 36 end with a record that has a `sessionId` and no `timestamp` (`atis-latch`, `cost-state`).

Not verified: Python 3.10 behaviour of `datetime.fromisoformat` (only 3.11 is installed); a year-9999-plus file mtime.

## Findings

### E1: MAJOR: unused worker-show share only flows forward, so `min(D, 50)` is missed and the report says the cap was reached

- Evidence: `src/superclaude/cli/sweep/probes.py:134-150` (`take_show`, the carry at 139-144 compares running totals up to the current Run only). DESIGN `docs/designs/orchestrator-mode.md:341` pins `worker-show` at `min(D, 50)` "when time allows", and 7.1 line 369 says "even split, remainder to the first Run".
- Run result: Run A has 40 rows, Run B has 10 rows (D = 50). Shows taken: A 25, B 10, total 35 of 50. Fifteen rows get no `worker-show` and are counted in `bound_reached`, and the report then prints "Show cap or time budget reached" although only 35 of 50 calls were used. Reverse order (A 10 rows, B 60) gives A 10, B 40, which is correct. Two Runs of 40 give 25 each (correct). Even split with 3 Runs gives 18/16/16 (correct).
- What is wrong: the carry is not in the DESIGN, and it works in one direction only. The pinned count `min(D, 50)` and the "cap reached" message are both untrue when an earlier Run is larger than its share and a later Run is smaller.
- Smallest fix: read every Run's `worker-list` first, then split the 50 shows by the real row counts (each Run gets `min(rows, fair share)` and the leftover goes to Runs that still have rows). If the owner prefers the strict even split, delete the carry at 139-144 and change DESIGN line 341 and the bound-line text to say "per-Run share reached".

### E2: MAJOR: `last_record_ts` is overwritten by records that carry no timestamp, so the activity time falls back to file mtime for most real transcripts

- Evidence: `src/superclaude/cli/sweep/probes.py:709-715` (`last_ts = ts` runs for every JSON object, including one whose `timestamp` is missing, and with no check for `sessionId`), and `probes.py:720` (`last_record_ts=last_ts if readable`). DESIGN 7.1 line 400 and 7.2 line 459 define the value from the complete records (the comment at `probes.py:713` itself says a complete record has both fields). The fallback is `classify.py:795-798` (`_last_activity` returns `tail.mtime`).
- Run result: a transcript whose records are `07:00`, `08:00`, then `{"type":"last-prompt","sessionId":"S1"}` gives `readable True`, `last_record_ts None`. A trailing record with no `sessionId` and no `timestamp` gives the same. In the real data above, 36 of 60 recent transcripts end this way.
- What is wrong: for those transcripts the row reports "last_activity from transcript st_mtime". mtime can be later than the last real message (any later write, copy or restore), so a stale person session can print as active. The DESIGN test plan (line 759, "record timestamp older than mtime") expects the record time to win.
- Smallest fix: in `_tail_from_bytes`, move `last_ts = ts` inside the block at line 713 (`if ts is not None and isinstance(sid, str) and sid:`), so only a complete record sets it.

### E3: MAJOR: `collect` can raise when a contract file disappears or cannot be stat-ed, against the "never raises past collect" rule

- Evidence: `src/superclaude/cli/sweep/probes.py:1242` (`candidate.exists()` is not wrapped), `probes.py:1254-1257` (`os.stat(candidate).st_mtime` and `datetime.fromtimestamp` run after `_contract` succeeded, with no `try`). DESIGN 7.1 line 394: readers "never raise past collect"; 7.2 lines 511 and 513 say a changed or removed input degrades one row.
- Run result: a contract read successfully and then removed before the age `os.stat` raised `FileNotFoundError` out of `_read_contracts`; nothing caught it. A contract inside a directory without search permission raises `PermissionError` from `exists()` on Python 3.11 in the same way (by reading, not run).
- What is wrong: a worker that rewrites or deletes its `return-contract.yaml` while the sweep runs turns the whole sweep into an exit-1 failure instead of one `unscanned` row.
- Smallest fix: wrap the per-candidate body of `_read_contracts` in `try/except (OSError, ValueError, OverflowError)` and record `SourceCoverage(name, "unscanned", None, "contract not readable")`; take the age from the same `os.stat` that `_contract` already does, or catch the error from the age call.

### E4: MAJOR: `bound_reached` is inferred from "all four show fields are None", so duplicate Dispatch rows and empty shows are reported as "Show cap or time budget reached"

- Evidence: `src/superclaude/cli/sweep/classify.py:871-874` (`_not_enriched`) and `classify.py:966` (`bound_reached`), printed by `report.py:207-208` (header line) and `report.py:376-380` (Retained problems).
- Run result: one Run with a duplicate Dispatch id whose two rows disagree (`completed` vs `dispatched`), one `worker-show` that returned `{}`, and a 50-show cap that was nowhere near reached (3 shows used) gave `bound_reached = 2`. The merged duplicate has every field None by design (`classify.py:544-545`), and the empty show has no keys, so both look "not enriched".
- What is wrong: neither row was cut by the cap or the time budget, yet the report says it was. The duplicate row is one of the cases this lens names. The number is still a safe lower bound, but the stated cause is false.
- Smallest fix: count only rows whose own `orca worker-show <dispatch>` source row carries the `show cap reached` or `time budget reached` reason, or set an explicit `show_skipped` flag in `probes._show` and have `_not_enriched` read that flag.

## Minor findings (notes only, never fail the gate)

- **M1** `probes.py:530-532`: when the 512 KiB tail window starts exactly at a line start, the first full line is dropped as if it were partial. Run result: a `FINAL:` line at that position in an oversize ledger gave `False`. Fix: also read the byte before the window and drop the first line only if that byte is not `\n`.
- **M2** `probes.py:536`: `str.splitlines()` splits on `\x0b`, `\x0c`, `\x1c`, `\x85` and U+2028, so `note<FF>FINAL: inside text` counted as `FINAL:` (all five separators returned True). DESIGN 7.2 line 516 says `FINAL:` counts only at the start of a line. Direction is safe (it blocks removal). Fix: `text.split("\n")` and strip `\r`.
- **M3** `probes.py:527-533`: for a ledger over 1 MiB only the tail is read; the head is never read. DESIGN GQ-105 and test line 759 say "head 512 KiB and the tail 512 KiB are read and the tail is searched". There is no behavioural difference (a `FINAL:` only in the head gives `False` in both readings). Fix: reword DESIGN and the constant comment, or drop `head` from the test wording.
- **M4** `probes.py:514-521`: `_stable` takes no budget, so the one re-read of a changed input happens even when the time budget is spent. NFR-007 (DESIGN line 808) says "only while the budget allows". Cost is one extra local file read. Fix: pass a `Budget` or a callable into the readers and raise `ReadFailed("conflict: inconsistent observation")` when `call_timeout()` is None.
- **M5** `probes.py:680-682`: the size check and `read_bytes` are separate; a contract that grows past 1 MiB between them is read whole before `_stable` sees the change. Fix: read with a `CONTRACT_LIMIT + 1` cap, as `read_orca_version` does at line 814.
- **M6** `probes.py:1003`: the full-page test uses `len(workers)` after non-dict rows were dropped, so a page of 100 with one non-object row reads as 99 when `hasMore` is false. Fix: test `len(raw)` when `raw` is a list.
- **M7** `probes.py:1050-1063`: a `worker-list` row with no `dispatchId` gets only an `unscanned` source row and no session row, so `total` does not count it. The row total is flagged as a lower bound by the unscanned source, so this is safe. Fix: emit a could-not-determine row, or document it.
- **M8** `classify.py:337-350` and `classify.py:402-403`: a future `last_activity` is classed "person session (active)" with note `timestamp in the future` (run result), and `ctx.now` is read before `collect`, which can take 90 s, so any session written during the sweep gets that note. DESIGN 7.2 line 492 only says rule 7 is never satisfied. Fix: use `collected_end` as the future cut-off, or state the rule 8 reading in DESIGN.
- **M9** `classify.py:657-660` and `classify.py:684-686`: if two transcripts join one Dispatch row, `joined.setdefault` keeps the first but `taken.add(idx)` hides both. Run result: two transcripts in, one row out, no note. It needs two tab-map files with one terminal handle, so it is unlikely. Fix: call `j.taken.add(idx)` only when `setdefault` stored this transcript, and send the other to `j.left` with the several-rows note.
- **M10** `classify.py:476-497` with `probes.py:890-896`: a worktree whose `git status` failed but whose directory exists still reports `removable: no` from its packages (run result: `('no', 'package pk is unfinished')`). DESIGN 7.2 line 513 says the worktree is could not determine. Fail-safe direction. Fix: check `status_read` first, or state in DESIGN that disk evidence still gives `no`.
- **M11** `probes.py:593-602` with `classify.py:429-435`: a `to-do/` package with no `progress.md` gets `has_final_line None`, state `unknown` (run result) and an `unscanned` row. GQ-105 says a `to-do/` package without a `FINAL:` line is `unfinished`. Effect: such a package does not print `package X is unfinished` as a removal reason (it still never reaches "yes"). Fix: treat `FileNotFoundError` as `False`, not as unreadable.
- **M12** `classify.py:825-844`: an over-1-MiB or outside-root contract is noted as `unscanned: contract not readable`. The cause is lost. Fix: map the source reason text to the note, as is done for `inconsistent`.
- **M13** `probes.py:800-801`: a tab-map file with fewer than three non-empty lines is skipped with no `unscanned` mark, so a half-written entry looks like "no entry".
- **M14** `probes.py:466-474`: the older git header `Initial commit on <branch>` is read as "no upstream". Modern git prints `No commits yet`, so this only matters on old git.
- **M15** `probes.py:741` and `probes.py:921-922`: `datetime.fromtimestamp` is not guarded against an absurd mtime (ValueError or OverflowError), and `_age` clamps a future mtime to 0. Not run for a year-33000 mtime.
- **M16** `probes.py:75-77` and `probes.py:349`: Python 3.10 `fromisoformat` accepts only 3 or 6 fractional digits; other forms fall to `None` (handled, no crash), which can make a transcript unreadable. Not run on 3.10.
- **M17** Single-record size: one JSONL record over 256 KiB (a large tool result) leaves no complete record in the tail, so the transcript prints unreadable (run result: `readable False`). This matches DESIGN 7.2 line 514 exactly, but the owner should know it is reachable in normal use.
- **M18** Test coverage: only four tests exist (`tests/sweep/test_readonly.py`, 4 passed in `step-1.4-pytest.txt` and `phase8-validation.md`). None of the edge cases in this report has a test yet; DESIGN 11 assigns them to later files (`test_probes_allowlist.py`, `test_classify.py`, `test_report.py`). Not a defect of this gate.

## Self-audit

- Independent verifications: 33 checks (13 executed probes over boundaries and fixtures, the rest by reading with line numbers). Files read: the four source modules, `models.py`, two test files, DESIGN sections listed above, `1.0a-facts.md`, `readonly-probe.md` sections 3 and 4, the raw `worker-show` capture (keys `worktreePath`, `taskId`, `parent`, `terminalState`, `outcome` exist), `gitignore-check.md`, `step-1.4a-pytest.txt`, `step-1.4-pytest.txt`, `phase8-validation.md`.
- Tool engagement (approximate): Read 34, Grep 4, Bash 12, Glob 0. No web research was done, so no Tavily or fallback call applies.
- The 4 MAJOR findings were each reproduced by running the code (E1, E2, E3, E4), not only inferred from reading. E2 was also checked against 60 real transcripts.
- Where the code matches DESIGN the check says PASS with the boundary values that were run, not a general statement.

## Checks

| Check | What was checked | Result |
|---|---|---|
| C1 | Budget even split, remainder to the first Run (3 Runs gave 18/16/16) | PASS |
| C2 | Show cap boundary: 50th take True, 51st False, reason `show cap reached (50)` | PASS |
| C3 | `call_timeout` at 10.0, 9.999, 1.0 and 0.999 s left, and `cut()` | PASS |
| C4 | Unused share reaches every Run so `worker-show` is `min(D, 50)` (DESIGN line 341) | FAIL (E1) |
| C5 | 8 MiB output limit at limit minus 1, at, plus 1, for orca and git, stdout plus stderr | PASS |
| C6 | 1 MiB contract limit at limit minus 1, at, plus 1 (`over 1 MiB` only at plus 1) | PASS |
| C7 | 1 MiB ledger limit at limit minus 1, at, plus 1 | PASS |
| C8 | 256 KiB transcript tail at limit minus 1, at, plus 1, and `tail_complete` | PASS |
| C9 | Ledger head-and-tail read (GQ-105): window alignment and head read | FAIL (M1, M3, minor) |
| C10 | `FINAL:` counts only at the start of a line (DESIGN line 516) | FAIL (M2, minor) |
| C11 | Truncated JSONL tail: last line cut is skipped, earlier complete record keeps it readable, a lone cut record is unreadable | PASS |
| C12 | `last_record_ts` is the time of the last complete record | FAIL (E2) |
| C13 | Unreadable transcript causes (OSError, no complete record) and the row note path | PASS |
| C14 | Future timestamp: rule 7 never idle, waiting time in the future adds the note | PASS |
| C15 | Future timestamp under rule 8 and the note on sessions written after `now` | FAIL (M8, minor) |
| C16 | Worktree removed between reads: stat failure and git failure give `unscanned: worktree not readable`, other worktrees continue | PASS |
| C17 | An unreadable worktree stays could not determine even when its packages are unfinished | FAIL (M10, minor) |
| C18 | Readers never raise past `collect` | FAIL (E3) |
| C19 | Duplicate Dispatch row: identical rows collapse, differing rows merge into one `orca:` row with the conflict note, window fields None, no show used | PASS |
| C20 | `bound_reached` counts only rows cut by the cap or the time budget | FAIL (E4) |
| C21 | Changed contract: one re-read, then `conflict: inconsistent observation` on the row | PASS |
| C22 | Re-read only while the budget allows (NFR-007) | FAIL (M4, minor) |
| C23 | Missing or extra `worker-show` key leaves the field None and raises nothing | PASS |
| C24 | Page-full test and a `worker-list` row without a Dispatch id | FAIL (M6, M7, minor) |
| C25 | `parse_status` M7: ahead N, ahead plus behind, behind only, synced, no upstream, gone, detached, no commits yet, rename pair, path with a space | PASS |
| C26 | `parse_time` rule of DESIGN 7.2 (SQLite form, ISO with Z or offset, junk, non-string, overflow, leap second) | PASS |
| C27 | DESIGN 7.3 constants and the 10 `ALLOWED_ORCA` templates, `ALLOWED_GIT`, `FORBIDDEN_TOKENS` | PASS |
| C28 | `.gitignore` item 8.6: two added lines after `.dev/sprint-state/`, `.dev/sweeps/` ignored (rc 0), `.dev/tasks/` not ignored (rc 1) | PASS |
| C29 | Two transcripts joined to one Dispatch row are both kept | FAIL (M9, minor) |
| C30 | `to-do/` package without `progress.md` is `unfinished` (GQ-105) | FAIL (M11, minor) |
| C31 | Source-reason notes name the real cause (over 1 MiB, outside root, tab-map entry) | FAIL (M12, M13, minor) |
| C32 | Test evidence files agree with the code (4 tests pass; no edge-case tests yet) | PASS |
| C33 | Field names used by `parse_worker_show` and `_run_rows` exist in the live capture | PASS |

Passed 20 of 33. Failed 13: 4 carry a MAJOR finding (C4, C12, C18, C20) and 9 carry only MINOR findings (C9, C10, C15, C17, C22, C24, C29, C30, C31).

Verdict: FAIL
Blocking count: 4
