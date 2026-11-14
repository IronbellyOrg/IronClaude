# QA Report: R3-B2 actionability lens (rf-qa-qualitative, doc-qualitative)

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` after items 3.1 to 3.4 (R3-B2, several Dispatch rows on one pane)
**Date:** 2026-11-09
**Fix cycle:** 1 (first review of this gate)
**Lens:** Act as the developer who writes the path-B part of `classify_all` and the seven fixtures from DESIGN alone.
**Fix authorization:** false. Only this report was written.

## Inputs read (all in chunks of 150 lines or fewer)

- DESIGN 7.2: lines 449-517 (worker bullet is line 498). Section 11: lines 728-751 (the `test_classify.py` cell is the single line 743). Rows FR-010 (768), D9 (819), SP-29 (857), GQ-108 (65), GQ-103(3) (60), section 6 counts (320-351), JSON schema and report layout (558-643).
- research/04 section 3, lines 120-176. research/09 Gap 4 (139-175) and Gap 5 (176-195).
- `r3-b2-mechanical.md`, lines 1-117. I did not rely on its PASS lines. I re-read the DESIGN lines myself. `wc -l` gives 1026 lines, which matches its header.

## Fixture-by-fixture walk (Given / When / Then without guessing)

Common to all seven: section 11 has no "When" column. The When is `classify_all(SweepInput, SweepContext)` and is inferable. The research table had it explicitly; the DESIGN cell dropped it.

| # | Fixture | Given complete? | Then checkable? | Guesses I would have to make |
|---|---|---|---|---|
| 1 | `test_path_b_pane_reused_joins_later_row_only` | No | Mostly | `collected_start` (D2 is open, so its window ends at `collected_start`; S at 10:40 only joins if `collected_start` >= 10:40); date, `now`, `window`; `tail_complete`; Run id and `ctx.runs`; D1/D2 `status` fields beyond `completed`/`dispatched`; "S's notes" is the notes of row `orca:D2`, since S has no row of its own |
| 2 | `..._two_windows_hold_session_is_conflict` | No | No | Same `collected_start` problem (both rows open); S `last_record_ts`/`mtime`, `now`, `window` (needed for "not idle, not Historical"); S row class; how "Historical" is asserted |
| 3 | `..._shared_boundary_second_is_conflict` | No | Mostly | `collected_start` >= 10:00:00 for D2; `tail_complete`; whether "cut" is floor or round (fixture cannot tell) |
| 4 | `..._no_matching_window_holds` | Yes, apart from the common items | Yes | Only `tail_complete`, S activity time, Run id |
| 5 | `..._multi_row_result_ignores_row_order` | Yes if 1 and 2 are fixed | Mostly | "The first two fixtures" is one test over two scenarios (parametrize?); compare by `row_id` mapping or by sequence? `SweepResult.rows` order is not defined (DESIGN:468) |
| 6 | `..._entry_failing_window_note_order` | Thin | Yes | D1 start, end and status are unstated (only "ended before"); the name says "note order" but the Then checks which note, not an order |
| 7 | `..._rows_share_terminal_handle` | Thin | Yes | Concrete handle value; the tab-map `file_name` must differ from `session_join` so a file-name match does not also fire; D1 and D2 both use the handle (no mixed file-name/handle match is tested) |

## Checks

| Id | Check | Result |
|---|---|---|
| C1 | Read DESIGN 7.2 worker bullet (line 498) in full and list every note and every place it lands | PASS |
| C2 | Each of the three outcomes (one window holds, two or more hold, none holds) has one 7.2 sentence and at least one section 11 fixture | PASS |
| C3 | Fixture 1 Given is complete enough to write without guessing | FAIL |
| C4 | Fixture 2 Given and Then are complete enough to write without guessing | FAIL |
| C5 | Fixture 3 Given is complete enough to write without guessing | FAIL |
| C6 | Fixture 4 Given and Then are complete enough (apart from the common items) | PASS |
| C7 | Fixture 5 (reversed row order) is unambiguous | PASS (MINOR m1) |
| C8 | Fixture 6 (entry failing window) is unambiguous | PASS (MINOR m4) |
| C9 | Fixture 7 (terminal handle) is unambiguous | PASS (MINOR m4) |
| C10 | For the three R3-B2 outcomes it is clear which notes go on the transcript and which on each Dispatch row | PASS (MINOR m2) |
| C11 | The multi-row rule is complete for a transcript with `tail_complete` False | FAIL |
| C12 | The precedence of a join-derived "could not determine" over rules 1 to 8 is stated, and the fixtures can detect it | FAIL |
| C13 | The Then for S in the conflict fixture (class, "not idle", "not Historical") can be asserted from DESIGN alone | FAIL |
| C14 | 7.2 text, section 11 fixtures, research/04 3.4 and research/09 Gap 4 agree on names, Givens and outcomes | PASS |
| C15 | FR-010 (768), D9 (819) and SP-29 (857) carry the same several-rows wording and agree with 7.2 | PASS |
| C16 | Sizing: DESIGN is 1026 lines now (1013 at build time), still the 500-1500 row, so 4 rf-qa + 4 rf-qa-qualitative + 1 domain lens = 9 (research/09 lines 182 and 193) | PASS |
| C17 | Single-row sentences earlier in the worker bullet do not contradict the multi-row sentences | PASS |

## Findings

### A1 (MAJOR): fixtures 1, 2 and 3 leave out `collected_start`, which decides their outcome

- Evidence: DESIGN:498 says a row whose `dispatch_ended` is None and whose status is `pending` or `dispatched` has a window that runs "to `collected_start`". DESIGN:743 fixture 1 has D2 "from 10:30, `dispatched`" with no end and S at 10:40. Fixture 2 has D1 and D2 both open, S at 10:05. Fixture 3 has D2 open from 10:00:00. Not one of the three names `collected_start`. The only fixture in that cell that does is the R3-B1 `test_path_b_window_open_row_joins` ("`collected_start` 12:00"), at the end of the cell.
- What is wrong: with `collected_start` 10:35, fixture 1 gives no join and the Then fails; with 09:00, fixture 2 has no window holding S and gives the "none holds" result instead of `conflict:`. The expected result holds only for a value the fixture never states. The default "`tail_complete` is True unless a fixture says otherwise" sits inside the R3-B1 sentence that follows the R3-B2 fixtures, so it does not clearly reach them. Date, `now`, `window` and Run id are missing too.
- Smallest fix: in the lead-in "the R3-B2 several-rows fixtures, all under path B and all with aware UTC times", add: "on one date, with `collected_start` 12:00, `tail_complete` True, S `last_record_ts` 11:30, `now` 12:00, `window` 6h, and every row in Run R1 (in `ctx.runs`)".

### A2 (MAJOR): the several-rows rule says nothing about a transcript with `tail_complete` False

- Evidence: DESIGN:498 has two separate pieces. One says that when the window is observable and `tail_complete` is False, "That match does not join: the row is could not determine with note `session start not observable: transcript tail only`, and that transcript is None with the same note". The other is the multi-row rule, which counts "rows' windows" that "hold" the transcript. With an incomplete tail, `first_record_ts` is not trustworthy, so no window can be said to hold or not hold it. No sentence joins the two. No fixture covers it: `grep -o tail_complete` on line 743 finds only the R3-B1 default sentence and `test_path_b_incomplete_tail_has_no_session_start`, which has one row.
- Why it matters: DESIGN:459 says `tail_complete` is False for every file over 256 KiB, which is the usual case for a long worker session. For two matching rows with an incomplete tail I would have to guess which note each row gets, and which of three notes (`session start not observable`, `Dispatch time window not observable`, `pane moved`) the transcript gets when the rows differ (one row without a window, one with).
- Smallest fix: add one sentence before "Several scoped Dispatch rows...": "If the transcript has `tail_complete` False, no window is tested: every matching row with an observable window is could not determine with `session start not observable: transcript tail only`, every other matching row gets `Dispatch time window not observable`, and the transcript is None with the tail-only note when at least one matching row has an observable window, else with `Dispatch time window not observable`." Add one fixture, `test_path_b_two_rows_incomplete_tail`.

### A3 (MAJOR): the Then of the conflict fixture cannot be asserted from DESIGN alone

- Evidence: DESIGN:743 fixture 2 ends "S is None with the same note and is not True, not idle and not Historical; no `orca:` row carries S". The DESIGN gives no class for such a transcript row and no row-level "Historical" marker. `Classification` (DESIGN:465) holds `class_name`, `waiting_kind`, `rule`, `evidence`, `notes`. "Historical" appears only as a report heading (DESIGN:626), a `summary.historical` count (DESIGN:468, 587, 345) and in M9 (DESIGN:865). Nothing says whether a Historical row is dropped from `SweepResult.rows`, flagged, or only counted. "Not idle" depends on S's `last_record_ts` and `now`, which the Given omits (see A1).
- Why it matters: the negative assertions are the point of the fixture (a pane session in conflict must never look like a person's finished session). I would have to pick a class (most likely `could not determine`, which DESIGN does not say), a way to test "not Historical" (`summary.historical == 0`? row present in `rows`?) and S's activity time.
- Smallest fix: state the expected class and the check in the Then, for example "S's row `transcript:S` has `person_started` None, class `could not determine` and rule `fallback`; `summary.historical` is 0 and `summary.total` is 3 (D1, D2, S)", and give S's activity time (see A1).

### A4 (MAJOR): the join-derived "could not determine" has no stated precedence over rules 1 to 8, and the fixtures cannot detect it

- Evidence: the rule table is DESIGN:476-486; rule 9 `fallback` is the only could-not-determine rule. DESIGN:498 says "the row is could not determine with note ..." for D1/D2, but no sentence says whether this forces the class over `finished` (rule 6), `working` (rule 5) or `blocked_contract` (rule 1), or only adds a note. In fixtures 1, 2, 3, 4 and 6 the Dispatch rows are bare (only start, end, status). A bare synthetic row falls to rule 9 anyway, so an implementation that adds the note but leaves rules 1 to 8 untouched passes every fixture.
- Why it matters: a completed worker with a `worker_done` contract and a path-B `pane moved` outcome would show `finished` under one reading and `could not determine` under the other. DESIGN:498 reads like the second; the fixtures cannot prove it.
- Smallest fix: add to 7.2: "A join outcome that makes a row could not determine is applied after rules 1 to 8 and replaces their class (rule `fallback`); the rule's own evidence stays in `evidence`." Give D1 in fixture 1 a contract with `worker_done` (a row that would otherwise be `finished`) so the Then proves it.

### Minor findings (never fail the gate)

- m1: Fixture 5 says "the first two fixtures with `orca_rows` reversed" under one test name. State "parametrized over fixtures 1 and 2" and "compare a `row_id` to (class, notes) mapping, not the `rows` sequence"; `SweepResult.rows` order is not defined (DESIGN:468).
- m2: In fixture 1 "S's notes do not contain `pane moved`" refers to a row that does not exist: S is shown as `orca:D2`. Say "the notes of row `orca:D2`". The same applies to the 7.2 sentence "those notes are not added to the transcript".
- m3: The DESIGN never says that the note literals live in `Classification.notes` and JSON `notes` (DESIGN:574 shows the JSON key) as opposed to the word "reason" (DESIGN:509 uses "reason" for the duplicate case), nor whether the test checks exact list membership or substring. Say "`notes` contains the exact string".
- m4: Fixture 6 gives no D1 start, end or status; its name says "note order" but it checks which note is used, not an order. Fixture 7 does not say the tab-map `file_name` must differ from the handle, and no fixture matches D1 by `file_name` and D2 by `terminal_handle` of the same entry, which 7.2 allows.
- m5: DESIGN:498 refers to "the R3-B2 rule below". R3-B2 is a review label defined only in section 18; a 7.2 reader sees no such name. Also "cut to whole seconds" does not say floor or round; the fixtures (.400 and .700) give the same result either way. Say "truncated to whole seconds".
- m6: Section 11 dropped the explicit When column that research/04 3.4 had, and the seven fixtures sit inside a single table cell (line 743) with about 40 other cases. Readable only by search. Not wrong.
- m7: Out of this gate's scope (R3-B3): `the four incomplete cases` is still in DESIGN:743 (`grep -c` gives 1).

## Self-audit (reliance list and independent checks)

- Relied on: the mechanical report's line numbers (498, 743, 768, 819, 857), which I confirmed by Read. I did not rely on any of its PASS lines.
- Independent checks: C3 to C5 and C11 to C13 come from my own reading of DESIGN:498 against DESIGN:743. The mechanical gate only greps wording and cannot find a missing Given. `grep -o collected_start` on line 743 returned one hit (the R3-B1 fixture); `grep -o tail_complete` on line 498 returned one; `wc -l` returned 1026.
- Confidence: Verified 17/17 | Unverifiable 0 | Unchecked 0 | Confidence 100%.
- Tool engagement: Read 9 | Grep 6 | Glob 0 | Bash 1.

## Recommendations

1. Fix A1 to A4 in DESIGN 7.2 (line 498) and section 11 (line 743) with the four smallest fixes above. These are text edits plus one new fixture.
2. Re-run the mechanical gate afterwards. Its checks should still hold (the new fixture adds one name; deviation and open-item totals are untouched).

Verdict: FAIL
Blocking count: 4

