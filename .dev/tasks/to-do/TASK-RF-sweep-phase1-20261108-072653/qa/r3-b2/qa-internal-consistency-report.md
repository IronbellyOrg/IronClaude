# QA Report: R3-B2 internal-consistency lens

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` after items 3.1 to 3.4 (R3-B2, several Dispatch rows on one pane session)
**Date:** 2026-11-09
**Phase:** fix-gate review, domain lens (internal consistency; research/09 Gap 5 sizing row 500-1500 lines; the DESIGN is 1026 lines on disk, not the 1013 of build time, same row)
**fix_authorization:** false (no file edited except this report)

## What I read (all in chunks of at most 150 lines)

- DESIGN 396-401, 449-518 (all of 7.2), 728-753 (section 11), 764-769 (FR-010 row), 805-860 (D9 and section 14 incl. SP-29), 1019-1026 (fix cycle 3).
- research/04 lines 40-119 (R3-B1 edits 1-9 and fixtures) and 120-176 (section 3, R3-B2).
- research/09 lines 139-208 (Gap 4, Gap 5).
- `phase-outputs/test-results/r3-b2-mechanical.md` (117 lines). I reproduced its checks 4 to 7 myself (no em dash, no TODO or TBD, one `Total: 9 deviations.` at 821, one `Total: 23 open items.` at 997). I did not rely on it for the rule analysis.
- I did not read the other lens report as evidence.

## The rule under test (DESIGN:498, worker bullet)

Window: `first_record_ts` cut to whole seconds, inside `dispatch_started` to `dispatch_ended`, both ends included, or to `collected_start` when `dispatch_ended` is None and status is `pending` or `dispatched`; no window when `dispatch_started` is None, or status is anything else with no end. Then the several-rows rule: exactly one row's window holds -> join that row only; two or more hold -> join none, `conflict:` on those rows and on the transcript; none holds -> every row CND with its note, transcript None.

For transcripts with a complete tail the three-way split (0, 1, 2 or more holders) is exhaustive and set-based, so it cannot depend on row order. The defects are where other 7.2 rules reach the same input.

## Findings

### F1 (MAJOR) Incomplete tail x several rows: the DESIGN gives two or three outcomes

Both sides, both at `docs/designs/orchestrator-mode.md:498`:

- Side A: "When the window is observable but the transcript has `tail_complete` False, the session start is not observable ... That match does not join: the row is could not determine with note `session start not observable: transcript tail only`, and that transcript is None with the same note."
- Side B: "If exactly one matching row's window holds the transcript, the transcript joins that row only and is False with note `joined by pane: latest session of the pane`; each other matching row is could not determine with note `pane moved to a later session`".

Input that gets two outcomes: D1 on P, 10:00:00 to 11:00:00, `completed`; D2 on P from 11:30, `dispatched`; tab-map P to S; S `tail_complete` False with `first_record_ts` 11:40 (any worker transcript over 256 KiB, `TranscriptTail` row at line 459 says this is "every file over 256 KiB", so this is the normal long-worker case).

- Reading A (tail rule first): D1 and D2 are both CND `session start not observable: transcript tail only`; S is None, same note.
- Reading B (several-rows rule, "window holds" computed from `first_record_ts` alone): S joins D2, False; D1 is CND `pane moved to a later session`.

Nothing says which applies. Third outcome with a mixed input: D1 has an observable window, D2 has `dispatch_started` None, S `tail_complete` False. Side A gives D1 `session start not observable` and S None with that note; Side B (no row holds) gives D2 `Dispatch time window not observable` and S None with `pane moved to a later session` (a matching row has an observable window). The seven R3-B2 fixtures (line 743) do not set `tail_complete` False, and the one R3-B1 incomplete-tail fixture (`test_path_b_incomplete_tail_has_no_session_start`) has a single row.

Smallest fix: add to 7.2 after the none-holds sentence: "A transcript with `tail_complete` False is not tested against the windows of several rows: each matching row with an observable window is could not determine with `session start not observable: transcript tail only`, each other matching row with `Dispatch time window not observable`, and the transcript is None with the first of those notes that applies." Add one fixture (two rows, incomplete tail, same result in both row orders).

### F2 (MAJOR) Duplicate Dispatch rows x several-rows count: the DESIGN gives two or three outcomes

Both sides:

- `docs/designs/orchestrator-mode.md:498`: "no row wins by position (as for duplicate Dispatch rows, in the Duplicate Dispatch bullet of this section)" and "If two or more matching rows' windows hold it, it joins none of them: each of those rows is could not determine with note `conflict: one pane session matches several Dispatch rows`".
- `docs/designs/orchestrator-mode.md:509`: "rows that share one Dispatch id but differ in state are merged into one `orca:<dispatch>` identity. That row is could not determine with reason `conflict: duplicate Dispatch rows disagree`."

Neither bullet says whether the merge happens before the matching rows are counted, and nothing says what `dispatch_started`, `dispatch_ended` and `dispatch_status` the merged identity carries (the `OrcaObservation` row at line 457 defines no merge of them).

Input: `orca_rows` holds D1a (`dispatched`, start 09:00, no end) and D1b (same Dispatch id D1, `completed`, 09:00 to 10:00), both with `session_join` P; S `first_record_ts` 09:30, complete tail.

- Count before merge: both windows hold -> "two or more", S is None with `conflict: one pane session ...`, and the one identity `orca:D1` carries two different `conflict:` strings.
- Merge first, window not merged: D1 has no observable window -> CND `Dispatch time window not observable`, S None with that note.
- Merge first, one of the two windows kept: S joins D1 (False) on a row that 509 says is CND.

Smallest fix: in the 509 bullet add "A merged identity counts as one matching row in the several-rows rule, and has no observable window", and add a fixture with a duplicate pair on a pane.

### F3 (MAJOR) Guard case 2 (SP-16) x the R3-B2 None outcomes: two notes, and a false printed reason

Both sides:

- `docs/designs/orchestrator-mode.md:501`: "Second, Orca returned at least one worker row and no transcript joined any Orca row (SPEC line 236, SP-16)." ... "In the second and third cases, Could not determine also prints the line `could not join Orca workers to transcripts (tab map empty or stale)`, and each affected transcript carries it as its note."
- `docs/designs/orchestrator-mode.md:498`: "the transcript is None with the `conflict:` note", "the transcript is None with `pane moved to a later session`".
- Fixtures, line 743: `test_path_b_no_matching_window_holds` ("S is None with `pane moved to a later session`"), `test_path_b_two_windows_hold_session_is_conflict` ("S is None with the same note"), `test_path_b_entry_failing_window_note_order` ("S's note is `pane moved to a later session`").

In each of these fixtures the Orca rows exist and no transcript joined any Orca row, so guard case 2 holds. Then S must also carry the SP-16 literal (501), and the report prints "(tab map empty or stale)" although the tab map was read and matched the rows; the fixtures say S's note is only the pane note. Order and precedence of the two notes are given nowhere (501 gives an order only for cases 1 and 2 together). This is largely inherited from R3-B1 (single row, `pane moved`), but R3-B2 adds two new None outcomes that reach it and three fixtures that assert a single note.

Smallest fix: in 501 case 2 add "unless a scoped Dispatch row matched a tab-map entry and was not joined by the window or several-rows rule; that transcript carries the pane note only". Add to the three fixtures "and `Could not determine` does not print the SP-16 line".

### F4 (MINOR) Summary rows disagree with 498 and with each other

- D9 (`:819`) and SP-29 (`:857`) say "a path-B join also needs the Dispatch row's time window and, when several rows match ..., exactly one window holding it" but omit the complete-tail condition that FR-010 (`:768`) has: "a path-B join also needing the Dispatch row's time window and a transcript whose tail is complete". Same rule, three different statements; the gate sentence is "D9, SP-29 and FR-010 rows agree" (research/09 line 167).
- `:499`, D9 (`:819`) and `:743` state without condition "a tab-map entry that joins no scoped row gives None with note `Orca pane session, not in scoped Runs`". Only the last sentence of 498 overrides this, and it names "a tab-map entry that fails the window". The conflict case (both windows hold) and the incomplete-tail case do not "fail the window" but also take other notes.
- Fix: add the tail clause to D9 and SP-29; change "fails the window" to "joins no row because of the window rules or the several-rows rule".

### F5 (MINOR) `pane moved to a later session` is wrong when the transcript is earlier than the row

`:498`: "each other matching row is could not determine with note `pane moved to a later session`". If D1 is 09:00 to 10:00, D2 is a worker-start row `pending` from 10:30 (inserted before its pane runs, research/04 line 51), and S (first record 09:20) is D1's session, S joins D1 and D2 is told the pane moved to a later session although S is earlier. Wording only; one clause fix ("moved to another session").

### F6 (MINOR) Fixtures 1 to 3 do not fix `collected_start`

Fixture 1 (D2 "from 10:30, `dispatched`", S 10:40), fixture 2 (open rows, S 10:05) and fixture 3 (D2 open from 10:00:00) depend on the open window ending at `collected_start`, but only the R3-B1 fixture `test_path_b_window_open_row_joins` names `collected_start` (12:00). A fixed `now` earlier than the S time would make the rows not hold. Add "`collected_start` 12:00" to the three.

### F7 (MINOR) Branch coverage of the rule is thinner than the rule

The order fixture (`test_path_b_multi_row_result_ignores_row_order`) reverses only the first two fixtures. No fixture exercises "other matching row has no observable window" inside the several-rows rule, "no matching row has an observable window", or three rows. The mechanical report's check 2 counts only the three headline outcomes.

### F8 (MINOR) Fractional bounds: only `first_record_ts` is cut

`:498` "`first_record_ts`, cut to whole seconds, must fall inside the row's window ... both ends included", while 7.2 `Time parsing` (`:470`) and `test_worker_show_dispatch_times_iso_z_form` (`:742`) accept `dispatchedAt: "...07:00:00.123Z"`. With start 07:00:00.123 and S first 07:00:00.400, the cut gives 07:00:00.000 < start, so the start bound fails; "both ends included" holds only for whole-second bounds. Direction is safe (toward CND or False) as the "never True" sentence says, but the rule can split a shared boundary one way (end holds, next start fails). Fix: cut all compared values to whole seconds.

### F9 (MINOR) Path A with several rows is unaddressed

The several-rows rule is introduced as path B ("by path B"). Two scoped rows with the same `session_join` equal to one `sessionId` (path A, line 497, for example a retry that resumes the session) join one transcript to two rows; 498 says a joined transcript "is shown as the Orca row `orca:<dispatch>`", singular. No rule, no fixture. State that the rule applies to either path or that path A cannot repeat a `sessionId`.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Read all inputs in chunks of at most 150 lines (7.2 whole, section 11 rows, FR-010, D9, SP-29, fix cycle 3, research/04 section 2 and 3, research/09 Gap 4 and 5, mechanical report) | PASS |
| C2 | Hold-count split (0, 1, 2 or more) is exhaustive and mutually exclusive for rows with a complete tail | PASS |
| C3 | The several-rows rule itself has no positional wording; its sentences are set-based (order independence) | PASS |
| C4 | Agrees with R3-B1 window: inclusive whole seconds (fixture 3 arithmetic: 10:00:00.400 cut to 10:00:00, held by 09:00:00 to 10:00:00 and by the start of D2), no window for a terminal row with no end, open window ends at `collected_start` | PASS (MINOR F8) |
| C5 | Agrees with the incomplete-tail rule (`tail_complete` False) | FAIL (F1) |
| C6 | Agrees with the duplicate-Dispatch-row rule (509) | FAIL (F2) |
| C7 | Agrees with the FR-010 guard cases 1 to 4 and the SP-16 literal (501) | FAIL (F3) |
| C8 | Agrees with 499 and D9 note rule (`Orca pane session, not in scoped Runs`) and with the m11 note order | PASS (MINOR F4) |
| C9 | FR-010 (768), D9 (819) and SP-29 (857) rows each carry the several-rows clause and agree with each other | PASS (MINOR F4: tail clause missing in D9 and SP-29) |
| C10 | Each of the seven R3-B2 fixtures matches the rule it names (Given/Then worked by hand: fixtures 1, 2, 3, 4, 5, 6, 7) | PASS (MINOR F6) |
| C11 | Fixtures cover the rule's branches | PASS (MINOR F7) |
| C12 | research/04 section 3.3 edits 1 to 5 appear in the DESIGN (edit 1 at 498; edit 2 at 743 after "a row with no observable start time never joins by path B;"; edit 3 at 768; edit 4 at 819 and 857; edit 5 at 1026). The only text differences from the plan are the line-number pointers turned into section pointers | PASS |
| C13 | Counts and style: no em dash, no TODO or TBD, `Total: 9 deviations.` at 821, `Total: 23 open items.` at 997 (my own grep) | PASS |
| C14 | Path A / other note literals: `conflict:` is used only for rules at 498, 509, 510 (no consumer keys off the prefix); path-A repetition | PASS (MINOR F9) |

## Summary

- Checks passed: 11 / 14 (C5, C6, C7 fail).
- BLOCKING: 0. MAJOR: 3 (F1, F2, F3). MINOR: 6 (F4 to F9).
- The three MAJOR findings each have one concrete input on which the DESIGN as written gives two or more different outcomes. None of the three is covered by a fixture, so the test plan would not catch them.

## Confidence

Verified: 14/14 checks run | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% of checks run; the defects above are reasoning over the text, not execution (there is no code yet, the DESIGN is the artifact).
Tool engagement: Read: 11 | Grep: 7 | Glob: 0 | Bash: 1

Verdict: FAIL
Blocking count: 3
