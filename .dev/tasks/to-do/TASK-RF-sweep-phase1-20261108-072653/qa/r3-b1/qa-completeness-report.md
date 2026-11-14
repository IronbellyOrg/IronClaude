# QA Report: R3-B1 completeness lens (research/04 section 2.2 edits and 10 fixtures)

**Date:** 2026-11-09
**Phase:** fix-cycle gate review (design fix R3-B1), completeness lens
**fix_authorization:** false (report only)
**DESIGN:** `docs/designs/orchestrator-mode.md`, 1023 lines (wc -l, this run). The file is untracked (`git status` shows `??`), so no earlier version exists in git to diff against.
**Reference:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/04-design-fixes-r3.md` lines 75-140, `research/09-gap-fill.md` Gap 4 (lines 139-175), `phase-outputs/test-results/r3-b1-mechanical.md`.
**Scope note applied:** the R3-B2 several-rows rule, the forward reference "Several matching rows follow the R3-B2 rule below." and the transcript outcome for a path-B non-join belong to Phase 3 item 3.1. They are not findings here.

## Edit-by-edit result (research/04 lines 87-95)

| # | Edit | DESIGN location | Result | Evidence |
|---|---|---|---|---|
| 1 | `OrcaObservation` row, three new fields plus bundle-name parenthesis | line 455 | PRESENT | Contains verbatim `dispatch_started: datetime \| None`, `dispatch_ended: datetime \| None`, `dispatch_status: str \| None` (design: from `worker-show` `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status`, names read statically from the Orca 1.4.245 bundle and confirmed by step 1.0a item 4, open item 23; all three are None for a row with no `worker-show` result, such as a row past the 50-call cap or a `call_failed` show). Same wording as research/04:87. |
| 2 | `TranscriptTail` row, `first_record_ts` after `last_record_ts` | line 457 | PRESENT | "`last_record_ts: datetime \| None`, `first_record_ts: datetime \| None` (the earliest `timestamp` among the complete records in the tail; for a file over 256 KiB this is not the session start)". Matches research/04:88. |
| 3 | Time-parsing paragraph after the 7.2 table, before "Constants in `models.py`" | line 468 | PRESENT | Starts "Time parsing (design): every Orca and transcript time is parsed to an aware UTC `datetime`", lists the SQLite and ISO `Z`/offset forms, the `Z` to `+00:00` rewrite for Python 3.10, and "An unparseable or missing value is None and raises nothing". Sits between the last table row (466) and "Constants in `models.py`" (470). One deliberate deviation: the closing reference "(unknown row schema rule, line 504)" became `(the "Unknown row schema" bullet below)`. That bullet exists at line 506, so the target is valid and the change removes a line-number reference that would go stale. |
| 4 | Worker bullet: window rule replacement | line 496 | PRESENT | Contains each required sentence: "`first_record_ts`, cut to whole seconds, must fall inside the row's window, from `dispatch_started` to `dispatch_ended`, both ends included, or to `collected_start` when `dispatch_ended` is None and `dispatch_status` is `pending` or `dispatched`"; "Times are compared as UTC instants"; "has no observable window"; the step 1.0a item 4 / open item 23 sentence; "Clock skew or the seconds cut can only move a session to could not determine or False, never to True"; the two non-join sentences with `pane moved to a later session` and `Dispatch time window not observable`; and the forward reference to the R3-B2 rule (out of scope here). The old "UNVERIFIED and come from the step 1.0a item 4 capture" sentence is gone (grep: no match). |
| 5 | 7.1 `read_transcript_tail` comment | line 398 | PRESENT | `# last 256 KiB, first partial line dropped; sets first_record_ts and last_record_ts`. |
| 6 | 2.2 GQ-103(3) field list | line 60 | PRESENT | "... `OrcaObservation.dispatch_started`, `dispatch_ended`, `dispatch_status` and `TranscriptTail.first_record_ts` (the path-B window)". |
| 7 | 15.1 item 4 capture text | line 887 | PRESENT | "and whether `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` are present with the shapes the static bundle read gives (SQLite `YYYY-MM-DD HH:MM:SS` UTC); also record, for one worker, whether `dispatchedAt` is earlier than the first transcript record of its session, and whether `completedAt` is set for `failed` and `circuit_broken` rows". The "Feeds" cell also names "the path-B time window". |
| 8 | 17 open item 23 | line 993 | PRESENT | Item text matches research/04:94 word for word. Behaviour cell: "No path-B join is made: every path-B match is could not determine with note `Dispatch time window not observable`, and its transcript is None". The note change (m5) is applied. The "unchanged otherwise" half cannot be checked against a prior version because the file is untracked; the sentence is coherent with line 496. |
| 9 | 18 `### Fix cycle 3` with R3-B1 row; cycle 2 row wording fix (m2) | lines 1017-1023; row 1013 | PRESENT | `### Fix cycle 3` exists at 1017 with an R3-B1 row whose Change cell matches research/04:95 ("... `read_transcript_tail` comment (7.1); GQ-103(3) list (2.2); capture item 4 and open item 23 name the bundle fields (15.1, 17); reader, parser and window fixtures (11)"). The cycle 2 R2-B1 row at 1013 now says "the earliest `timestamp` in the transcript tail must fall inside the Dispatch row's time window" (m2 applied; the phrase "transcript's earliest timestamp" no longer appears). Cycle 2 row not rewritten otherwise, as research/04 asks. |

All nine edits: PRESENT. No PARTIAL or MISSING edit.

## Fixture-by-fixture result (research/04 lines 99-117; research/09 Gap 4 lines 145-157)

Fixtures 1 to 6 sit in the `tests/sweep/test_probes_allowlist.py` row (DESIGN line 740), fixtures 7 to 10 in the `tests/sweep/test_classify.py` row (DESIGN line 741). The DESIGN writes them as prose inside the "Main cases" cell instead of Given/When/Then tables; the When step is implicit.

| # | Fixture | Result | Evidence |
|---|---|---|---|
| 1 | `test_read_transcript_tail_sets_first_and_last_record_ts` | PRESENT | 740: 3 complete records at 07:00:01Z, 07:00:05Z, 07:00:09Z, one `sessionId`; `first_record_ts` 07:00:01 UTC, `last_record_ts` 07:00:09 UTC, both aware. |
| 2 | `test_read_transcript_tail_first_record_ts_is_minimum` | PRESENT | 740: records 07:00:05Z, 07:00:01Z, 07:00:09Z give 07:00:01, "the earliest value and not the first line". |
| 3 | `test_read_transcript_tail_first_record_ts_over_256k` | PRESENT | 740: file over 256 KiB, first record 07:00:00Z before the tail, first complete tail record 08:00:00Z, result 08:00:00 "because only the tail is read". |
| 4 | `test_worker_show_dispatch_times_sqlite_form` | PRESENT | 740: `dispatchedAt: "2026-11-08 07:00:00"`, `completedAt: null`, `status: "dispatched"` gives `dispatch_started` 2026-11-08 07:00:00 UTC aware, `dispatch_ended` None, `dispatch_status` `"dispatched"`. |
| 5 | `test_worker_show_dispatch_times_iso_z_form` | PRESENT | 740: `dispatchedAt: "2026-11-08T07:00:00.123Z"` and `completedAt: "2026-11-08T08:00:00Z"` both parse as aware UTC. |
| 6 | `test_worker_show_dispatch_times_missing_or_bad` | PRESENT | 740: one fixture with no `dispatch` times, one with `dispatchedAt: "yesterday"`, field None, nothing raised, "per the unknown row schema rule". |
| 7 | `test_path_b_window_open_row_joins` | PARTIAL | 741: "row D1 with `dispatch_started` 10:00, `dispatch_ended` None and `dispatch_status` `dispatched`, transcript S with `first_record_ts` 10:05, `collected_start` 12:00: S joins D1, `person_started` is False, S is shown as `orca:D1` with note `joined by pane: latest session of the pane`". The Then half is complete. The Given drops two items research/04:114 requires: "`session_join` pane P" and "tab-map entry P to session S". See finding F1. |
| 8 | `test_path_b_window_inclusive_bounds` | PRESENT | 741: D1 10:00:00 to 11:00:00 `completed`; S `first_record_ts` 10:00:00.700, 11:00:00.400, 11:00:01.000; first two join (seconds cut, both ends included); third does not join, D1 could not determine with `pane moved to a later session`, S None. Research/04:115 itself has no tab-map items for this row, so nothing is dropped. |
| 9 | `test_path_b_terminal_row_without_end_has_no_window` | PRESENT | 741: D1 started 10:00, `dispatch_ended` None, `dispatch_status` `completed`, S first record 10:30: no join, D1 could not determine with `Dispatch time window not observable`, S None "with the same note" (m4). |
| 10 | `test_path_b_row_without_start_has_no_window` | PRESENT | 741: D1 `dispatch_started` None "for example past the 50-call show cap": no join, D1 could not determine with `Dispatch time window not observable`, S None, never True. |

Counts: 10 of 10 fixture names found; 9 PRESENT, 1 PARTIAL.

## Findings

| ID | Severity | Evidence | What is wrong | Smallest fix |
|---|---|---|---|---|
| F1 | MAJOR | `docs/designs/orchestrator-mode.md:741` (fixture `test_path_b_window_open_row_joins`) against `research/04-design-fixes-r3.md:114` | The fixture's Given omits `session_join` pane P and the tab-map entry from P to session S. Without a tab-map entry the Then ("S joins D1") has no cause, so the fixture does not exercise path B at all. Fixtures 8 to 10 inherit path B from the `path_b` name; fixture 7 is the only one where research/04 spells the join setup out, and the DESIGN dropped it. This is the one fixture that proves the positive join. | In the line 741 text for `test_path_b_window_open_row_joins`, change "(row D1 with `dispatch_started` 10:00, `dispatch_ended` None and `dispatch_status` `dispatched`, transcript S" to "(row D1 with `session_join` pane P, `dispatch_started` 10:00, `dispatch_ended` None and `dispatch_status` `dispatched`; a tab-map entry from P to session S; transcript S". |
| F2 | MINOR | `docs/designs/orchestrator-mode.md:382-400` (7.1 signatures) and 740 (fixtures 4 to 6) | Fixtures 4 to 6 test "the `worker-show` parser" (research/04:106), but 7.1 names no function that turns `worker-show` JSON into `OrcaObservation` or parses times; `collect` is the nearest. The DESIGN fixture text does not name the entry point either. research/04 prescribes no 7.1 edit for it, so this is not an omitted edit. | Optional: name the function (or `collect`) in the fixture cell so the tests have a target. |
| F3 | MINOR (out of scope, recorded) | `docs/designs/orchestrator-mode.md:741` ("and that later transcript is None with the same note") against 496 | The test_classify cell still says the later transcript is None for the moved-pane case, while edit 4 removed that clause from the worker bullet. The scope note assigns the transcript outcome for a non-join to Phase 3 item 3.1. | None here; confirm item 3.1 closes it. |

## Other checks

- Mechanical recheck (this run): `wc -l` 1023; em-dash count 0; `TODO`/`TBD` count 0; `^Total: 9 deviations.` 1 hit; `^Total: 23 open items.` 1 hit; `first_record_ts` 7 lines. These agree with `r3-b1-mechanical.md` (7 of 7 PASS).
- Stale-text sweep: grep for `earliest|UNVERIFIED and come|fields that carry|observable start` finds only the new line 457, the status bullet at line 9 (describes the defect, correct), and rows 740, 741, 1013, 1023. No old "fields that carry the Dispatch start and end times" text remains in 15.1.
- research/09 Gap 4 recommendation (not from 04): the FR-010 traceability row at DESIGN:766 already lists `sweep/test_probes_allowlist.py` "(the six reader and parser fixtures of the path-B time fields)", and the probes file's Covers cell (740) already lists FR-010. Present.
- Gate sizing used by the lead: DESIGN is 1023 lines now, still the 500-1500 row. No change.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Edit 1: `OrcaObservation` row (line 455) | PASS |
| C2 | Edit 2: `TranscriptTail.first_record_ts` (line 457) | PASS |
| C3 | Edit 3: time-parsing paragraph (line 468) | PASS |
| C4 | Edit 4: worker bullet window rule (line 496) | PASS |
| C5 | Edit 5: 7.1 `read_transcript_tail` comment (line 398) | PASS |
| C6 | Edit 6: GQ-103(3) list (line 60) | PASS |
| C7 | Edit 7: 15.1 item 4 (line 887) | PASS |
| C8 | Edit 8: open item 23 (line 993) | PASS |
| C9 | Edit 9: Fix cycle 3 R3-B1 row plus cycle 2 m2 wording (lines 1013, 1017-1023) | PASS |
| C10 | Fixture 1 `..._sets_first_and_last_record_ts` | PASS |
| C11 | Fixture 2 `..._first_record_ts_is_minimum` | PASS |
| C12 | Fixture 3 `..._first_record_ts_over_256k` | PASS |
| C13 | Fixture 4 `test_worker_show_dispatch_times_sqlite_form` | PASS |
| C14 | Fixture 5 `test_worker_show_dispatch_times_iso_z_form` | PASS |
| C15 | Fixture 6 `test_worker_show_dispatch_times_missing_or_bad` | PASS |
| C16 | Fixture 7 `test_path_b_window_open_row_joins` | FAIL |
| C17 | Fixture 8 `test_path_b_window_inclusive_bounds` | PASS |
| C18 | Fixture 9 `test_path_b_terminal_row_without_end_has_no_window` | PASS |
| C19 | Fixture 10 `test_path_b_row_without_start_has_no_window` | PASS |
| C20 | Mechanical counts recheck (em-dash, TODO/TBD, 9 deviations, 23 open items) | PASS |
| C21 | Stale-text sweep for pre-fix wording | PASS |
| C22 | research/09 Gap 4 recommended FR-010 traceability addition | PASS |

## Self-audit

Tool calls that back this report: Read of research/04 lines 70-144, research/09 lines 139-208, the mechanical report in full, and DESIGN lines 51-74, 394-401, 447-516, 726-751, 868-901 and 965-1023; Grep for stale wording, row anchors, parser signatures and `^def|^class`; Bash for `wc -l`, `git status`, `git log`, the totals recheck and the FR-010, D9 and SP-29 rows. I did not find an edit that is missing. I found one fixture that lost its join setup in transcription.

Confidence: Verified 22/22 | Unverifiable 1 (the "unchanged otherwise" half of edit 8, no prior version in git; the check still passes on the text that is present) | Unchecked 0.

Verdict: FAIL
Blocking count: 1
