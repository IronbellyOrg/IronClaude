# QA Report: R3-B1 cross-reference chain lens (task-qualitative, report-only)

**Topic:** R3-B1 path-B window names (`first_record_ts`, `dispatch_started`, `dispatch_ended`, `dispatch_status`) in `docs/designs/orchestrator-mode.md` (1023 lines on disk)
**Date:** 2026-11-09
**Phase:** task-qualitative (cross-reference lens), `fix_authorization: false`
**Fix cycle:** N/A (first review of this gate)
**Inputs read:** DESIGN lines 1-36, 37-82, 351-446, 447-515, 726-802, 803-865, 866-945, 946-1023; research/04 lines 30-140 and 215-232; research/09 lines 139-226; `phase-outputs/test-results/r3-b1-mechanical.md`; `artifacts/design-base.md` (pre-edit copy, used for `diff`); task item 2.6 and 2.7 text.

Scope note honoured: the R3-B2 several-rows rule, the forward reference "Several matching rows follow the R3-B2 rule below." and the transcript outcome for a path-B match that does not join are Phase 3 work and are not counted below. They are listed once under "Deferred, not counted".

---

## Findings

No BLOCKING and no MAJOR finding. Every section, step and open-item number cited in the new text exists and says what the citation claims. The five findings below are MINOR (they never fail the gate).

### M1 (MINOR): no 7.1 signature owns the time-parsing rule or the `worker-show` parser that section 11 and 12 test

- Evidence: DESIGN 7.1 (lines 353-446) names one parser, `parse_status` (line 394), and one transcript reader, `read_transcript_tail` (line 398). The "Time parsing (design)" rule is only in 7.2 (line 468). Section 11 line 740 has three `test_worker_show_dispatch_times_*` fixtures and section 12 line 766 calls them "reader and parser fixtures", but no 7.1 name builds `OrcaObservation.dispatch_started`, `dispatch_ended` or `dispatch_status` from `worker-show`. The only possible entry point is `collect` (line 390) with `patch_orca`.
- What is wrong: the parser fixtures cite an entry point the design never names, and the module that holds the parse (probes, because `classify.py` and `report.py` are pure) is implied, not stated. A builder at step 1.4 must guess.
- Smallest fix: add one line to 7.1 `probes.py`, for example `def parse_time(text: object) -> datetime | None   # section 7.2 time parsing; used by collect (worker-show times) and read_transcript_tail`, and say in the three fixture rows that they go through `collect` with `patch_orca` or through `parse_time`.

### M2 (MINOR): section 12 FR-010 row traces the six parser fixtures but not the four `test_classify.py` window fixtures

- Evidence: line 766 test column reads `sweep/test_classify.py` (the D9 join fixtures and the SPEC line 236 fixture), then `sweep/test_probes_allowlist.py` (the six reader and parser fixtures of the path-B time fields). The four `test_path_b_*` window fixtures are in line 741 and are not named in 766. `diff` against `design-base.md` shows line 766 changed only by the `test_probes_allowlist.py` clause.
- Smallest fix: in line 766 extend the `test_classify.py` parenthesis to "(the D9 join fixtures, the four path-B window fixtures and the SPEC line 236 fixture)".

### M3 (MINOR): older section 11 wording was not aligned with the new names

- Evidence: line 741 still says "the later session, whose earliest timestamp is outside the Dispatch row's window" (should name `first_record_ts`) and "a row with no observable start time never joins by path B" (the rule at line 496 now speaks of "no observable window" and the note `Dispatch time window not observable`; a terminal row with a start time but no end time also has no window). The same case is covered again by the new `test_path_b_row_without_start_has_no_window` in the same cell.
- Smallest fix: reword to "whose `first_record_ts` is outside the Dispatch row's window" and "a row with no observable window never joins by path B (see the two last window fixtures)".

### M4 (MINOR): Fix cycle 3 R3-B1 row does not name every changed section

- Evidence: line 1023 lists 7.2, 7.1, 2.2, 15.1, 17 and 11. `diff` against `design-base.md` also changes line 740 (Covers cell gains `FR-010`) and line 766 (FR-010 row, section 12). research/04 edit 9 says the new table "still names every change". Section 12 is missing from the row.
- Smallest fix: append "; FR-010 test column and the `test_probes_allowlist.py` Covers cell (12, 11)" to the R3-B1 change text.

### M5 (MINOR): no stated outcome when `first_record_ts` is None for a path-B candidate

- Evidence: line 457 defines `first_record_ts` as the earliest `timestamp` among complete records; line 468 says an unparseable value is None; line 511 makes a transcript readable when it holds one record with both `timestamp` and `sessionId`, not a parseable one. Line 496 says `first_record_ts` "must fall inside" the window. For a readable transcript with only unparseable timestamps the test fails and the row would get `pane moved to a later session`, which is the wrong reason. The "never to True" claim still holds, so this is safe but mislabeled.
- Smallest fix: add one sentence at line 496: "A transcript whose `first_record_ts` is None does not join and is treated as a row with no observable window (note `Dispatch time window not observable`)", plus a fifth fixture or a case in the `missing_or_bad` fixture.

### Notes (no severity, not findings)

- N1: Section 1 lines 7-9 still describe R3-B1 as "three time fields" and as open. That is correct until the gate closes; whoever closes the gate must reword it (there are now four fields, including `dispatch_status`).
- N2: research/04:221 says to grep the four model names in 7.1, 7.2, 2.2, 11, 15.1, 17 and 18. Read literally, 7.1 holds only `first_record_ts`, and 15.1 and 17 hold only the Orca source names (`dispatch.dispatchedAt` and the rest), as research/04 edits 5, 7 and 8 prescribe. Task item 2.7 states the per-section reading it used, and the mechanical report's matrix shows the zeros openly, so the report is honest. A gate reader who applies the literal wording will see "failures"; the edits, not the gate sentence, are the authority.
- Deferred, not counted (Phase 3, per the scope note): (a) line 496 "Several matching rows follow the R3-B2 rule below." has no target yet; (b) the sentence "and that transcript is None with the same note" was removed from line 496 as research/04 edit 4 prescribes, while line 741 (fixtures) and line 993 (open item 23) still state the transcript is None. Item 3.1 must restore one rule.

---

## Checks

Method: each check was run against the file text on disk. FAIL marks a check that carries a finding; the severity is in the last column.

| Check | What was checked | Result | Severity if FAIL |
|---|---|---|---|
| C1 | Sections 2.2, 7.1, 7.2, 11, 12, 15.1, 17, 18 exist and hold the text the edits target (`grep` section map and chunked Reads) | PASS | |
| C2 | `first_record_ts` in 7.1 (398), 7.2 (455-457, 496), 2.2 (60), 11 (740, 741), 18 (1023); `dispatch_*` model names in 7.2 (455, 496), 2.2 (60), 11 (740, 741), 18 (1023); Orca source names in 7.2 (455), 11 (740), 15.1 (887), 17 (993) | PASS | |
| C3 | GQ-103(3) row (line 60) lists the four names, points to `models.py` (section 7.2), and the fields exist in the 7.2 table (455, 457) | PASS | |
| C4 | Line 455 citations: "section 2.2 path A or B" (GQ-108, line 65), "step 1.0a item 4" (15.1 row 4, line 887, holds the fields), "open item 23" (line 993, same fields) | PASS | |
| C5 | Line 496 citations: step 1.0a item 4, open item 23, `collected_start` (SweepInput, line 454), `pending` / `dispatched` values (research/04 line 50), 50-call cap (Budget `shows=50`, line 367) | PASS | |
| C6 | Line 468 citation "the 'Unknown row schema' bullet below" resolves to line 506; section 11 line 740 "per the unknown row schema rule" resolves to the same bullet | PASS | |
| C7 | Line 398 `read_transcript_tail` comment matches 457 and the reader fixtures in 740 (uncut value, minimum not first line, tail only over 256 KiB) | PASS | |
| C8 | Fixture arithmetic in 741: 10:00:00.700 and 11:00:00.400 cut to 10:00:00 and 11:00:00 are inside 10:00:00 to 11:00:00 inclusive; 11:00:01.000 is outside; open row D1 with `dispatched` and S at 10:05 joins up to `collected_start` 12:00; terminal row without end has no window; counts are 6 plus 4 (names counted with `grep -o`) | PASS | |
| C9 | Section 12 FR-010 row (line 766) cites the right file and the right count (six) for the parser fixtures | PASS | |
| C10 | Section 12 traces all ten R3-B1 fixtures | FAIL | MINOR (M2) |
| C11 | 15.1 row 4 (line 887) matches research/04 edit 7 and its Feeds column cites the window and open item 23; row 13 and open item 22 still agree | PASS | |
| C12 | Open item 23 (line 993) text matches research/04 edit 8; "Closed by" step 1.0a item 4 exists; behaviour until closed agrees with line 496 (`Dispatch time window not observable`); row count is 23 | PASS | |
| C13 | 7.2 edits 1 to 4 (lines 455, 457, 468, 496) are verbatim to research/04 section 2.2; edits 5 to 8 (lines 398, 60, 887, 993) match | PASS | |
| C14 | Fix cycle 3 table (lines 1017-1023): intro cites master `5dc29d23`, which is an ancestor of `origin/master` (`git merge-base --is-ancestor`), row text cites existing sections | PASS | |
| C15 | Fix cycle 3 R3-B1 row names every changed section | FAIL | MINOR (M4) |
| C16 | Cycle 2 R2-B1 row (line 1013) now reads "the earliest `timestamp` in the transcript tail"; the old phrase is gone (`diff` against base) | PASS | |
| C17 | 7.1 names an owner for the time-parsing rule and the `worker-show` parser that the section 11 and 12 fixtures call | FAIL | MINOR (M1) |
| C18 | Stale-term sweep for "earliest", "start time", "end time", "time window" across the file (grep with line numbers) | FAIL | MINOR (M3) |
| C19 | Outcome of `first_record_ts` None is specified against 457, 468, 496, 511 | FAIL | MINOR (M5) |
| C20 | Totals: `Total: 9 deviations.` (line 819), `Total: 23 open items.` (line 995, 23 numbered rows), em-dash count 0, no `TODO` or `TBD` (own greps) | PASS | |
| C21 | `r3-b1-mechanical.md`: recounted the matrix lines against the file, confirmed the seven PASS lines, and checked that its per-section rule is the one stated in task item 2.7 | PASS | |
| C22 | External facts in the new text: Python 3.10 `fromisoformat` rejects `Z` and `requires-python = ">=3.10"` (pyproject line 16); Dispatch status set `pending`, `dispatched`, `completed`, `failed`, `circuit_broken` and `datetime('now')` form (research/04 lines 50-51) | PASS | |
| C23 | Section 1 status text (lines 7-9) and D9 / SP-29 rows (817, 855) agree with the new window wording | PASS | |

## Summary

- Checks passed: 18 / 23
- Checks failed: 5 (all MINOR)
- Critical or blocking issues: 0

## Self-Audit

**(a) Reliance list:** none. No inherited structural verdict was supplied; every check above was run from the files on disk.

**(b) Independent semantic checks:**
- Window arithmetic and inclusive bounds re-derived by hand for the three bound fixtures and the open-row fixture (C8); read lines 741 and 496 in full.
- `diff` of `design-base.md` against the edited design to find every changed hunk (60, 398, 455, 457, 468, 496, 740-741, 766, 887, 993, 1013, 1016-1023) and compare to research/04 edits 1 to 9 (C13, C15, C16).
- Followed every new name into section 12 and found the missing `test_classify.py` trace (C10) and the missing owner in 7.1 (C17), which the mechanical report's grep matrix cannot show.
- Checked `5dc29d23` against `origin/master` (C14) and `requires-python` (C22).

**Confidence:** Verified: 23/23 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 14 | Grep: 8 | Glob: 0 | Bash: 7 (inspection only, no file written except this report)

Note on process: an instruction in my agent preamble says not to write report files; the task prompt names this exact path as the one required output, so I wrote it and nothing else.

Verdict: PASS
Blocking count: 0
