# QA Report: R3-B2 completeness lens

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` after items 3.1 to 3.4 (R3-B2, several Dispatch rows on one pane session)
**Date:** 2026-11-09
**Phase:** fix-cycle gate review (completeness lens)
**Fix authorization:** false (report only)
**DESIGN size read:** 1026 lines (the gate sizing note says 1013 at build time; the file grew with R3-B1 and R3-B2; the 500-1500 row still applies)

Sources read from disk: research/04 lines 120-176; research/09 Gap 4 (lines 139-175); `r3-b2-mechanical.md` (lines 1-116); DESIGN lines 449-518, 728-753, 768, 819, 857, 1015-1026. The mechanical report was used only as a pointer; every verdict below comes from the DESIGN text itself.

## Section 3.3: the five edits

| Edit | Where (DESIGN) | Quoted text found | Verdict |
|---|---|---|---|
| E1 7.2 worker bullet, after "...because a person rerun inside the window cannot be told apart." | line 498 | "Several scoped Dispatch rows can match one tab-map entry by path B (a reused pane, a retry, or two rows on one terminal handle). The result does not depend on row order, and no row wins by position ..." through "If exactly one matching row's window holds the transcript, the transcript joins that row only and is False with note `joined by pane: latest session of the pane`; each other matching row is could not determine with note `pane moved to a later session` (or `Dispatch time window not observable` ...)", "If two or more matching rows' windows hold it, it joins none of them: each of those rows is could not determine with note `conflict: one pane session matches several Dispatch rows` ... the transcript is None with the `conflict:` note", "If no matching row's window holds it, every matching row is could not determine with its note, and the transcript is None with `pane moved to a later session`, or with `Dispatch time window not observable` when no matching row has an observable window." All three outcomes and the "those notes are not added to the transcript" clause are present. | PRESENT |
| E2 11, `test_classify.py` row, after "a row with no observable start time never joins by path B;" | line 743 | "a row with no observable start time never joins by path B; the R3-B2 several-rows fixtures, all under path B and all with aware UTC times: `test_path_b_pane_reused_joins_later_row_only` (...)" | PRESENT |
| E3 12, FR-010 row | line 768 | "..., and one rule for several rows matching one pane session (join only the one row whose window holds it; `conflict:` when two or more do)" | PRESENT |
| E4a 13 D9 | line 819 | "a path-B join also needs the Dispatch row's time window and, when several rows match one pane session, exactly one window holding it" | PRESENT |
| E4b 14 SP-29 | line 857 | "a path-B join needs the Dispatch row's time window and, when several rows match one pane session, exactly one window holding it" | PRESENT |
| E5 18 Fix cycle 3, R3-B2 row | line 1026 | "Added the several-rows rule with the `conflict: one pane session matches several Dispatch rows` note, and the note order for a tab-map entry that fails the window (m11) (7.2); fixtures (11); FR-010, D9 and SP-29 rows (12, 13, 14)" (word for word the 04 text) | PRESENT |

## m11 note-order sentence

Present at DESIGN line 498, final sentence: "A transcript with a tab-map entry that fails the window takes these notes instead of `Orca pane session, not in scoped Runs` (in the bullet that follows this one)." The bullet that follows (line 499) is the one that holds `Orca pane session, not in scoped Runs`, so the reference is correct. Verdict: PRESENT.

## Section 3.4: the seven fixtures (all on line 743, in the `test_classify.py` row, once each)

| Fixture | Given, When and Then checked against 04:158-164 | Verdict |
|---|---|---|
| `test_path_b_pane_reused_joins_later_row_only` | D1 09:00-10:00 `completed`, D2 from 10:30 `dispatched`, S first 10:40; S joins D2 only, False, `orca:D2`, `joined by pane: latest session of the pane`; D1 `pane moved to a later session`; S notes lack `pane moved` | PRESENT |
| `test_path_b_two_windows_hold_session_is_conflict` | D1 from 09:00 `dispatched`, D2 from 10:00 `pending`, S 10:05; no join; both rows and S carry the `conflict:` note; S not True, not idle, not Historical; no `orca:` row carries S | PRESENT |
| `test_path_b_shared_boundary_second_is_conflict` | D1 09:00:00-10:00:00 `completed`, D2 from 10:00:00 `dispatched`, S 10:00:00.400; both windows hold S (seconds cut, both ends inclusive); both rows `conflict:`, S None | PRESENT |
| `test_path_b_no_matching_window_holds` | D1 09:00-09:30, D2 10:00-10:30, both `completed`, S 11:00; both rows and S carry `pane moved to a later session` | PRESENT |
| `test_path_b_multi_row_result_ignores_row_order` | first two fixtures with `orca_rows` reversed; same classes, notes and `row_id` values | PRESENT |
| `test_path_b_entry_failing_window_note_order` | tab-map P to S, D1 ended before S's first record; S note is `pane moved to a later session`, not `Orca pane session, not in scoped Runs` | PRESENT |
| `test_path_b_rows_share_terminal_handle` | as fixture one but matched by `terminal_handle` (tab-map line 3); same result | PRESENT |

Outcome coverage (research/09 Gap 4, gate at 04:222): one window holds is covered by fixture 1; two or more hold by fixtures 2 and 3; none holds by fixture 4. Each of the three 7.2 outcome sentences has a fixture.

## Checks

| Check | What was checked | Result |
|---|---|---|
| C1 | E1: the several-rows text is in 7.2 after the "person rerun" sentence, with all three outcomes (one, two or more, none) and the not-added-to-transcript clause | PASS |
| C2 | E2: fixture names are inserted in the `test_classify.py` row at the required anchor | PASS |
| C3 | E3: FR-010 row carries the several-rows clause | PASS |
| C4 | E4: D9 and SP-29 each carry "exactly one window holding it" | PASS |
| C5 | E5: Fix cycle 3 R3-B2 row matches 04:152 | PASS |
| C6 | m11 note-order sentence present in 7.2 | PASS |
| C7 | Fixture 1 `pane_reused_joins_later_row_only` | PASS |
| C8 | Fixture 2 `two_windows_hold_session_is_conflict` | PASS |
| C9 | Fixture 3 `shared_boundary_second_is_conflict` | PASS |
| C10 | Fixture 4 `no_matching_window_holds` | PASS |
| C11 | Fixture 5 `multi_row_result_ignores_row_order` | PASS |
| C12 | Fixture 6 `entry_failing_window_note_order` | PASS |
| C13 | Fixture 7 `rows_share_terminal_handle` | PASS |
| C14 | Each 7.2 outcome has a fixture in section 11 (research/09 Gap 4 gate) | PASS |
| C15 | Independent re-run of the em-dash, `TODO`/`TBD` scan (0 matches, Grep count) and the two totals (`Total: 9 deviations.` at 821, `Total: 23 open items.` at 997) | PASS |

## Findings

No BLOCKING or MAJOR findings.

| id | Severity | Evidence | What is wrong | Smallest fix |
|---|---|---|---|---|
| F1 | MINOR | DESIGN:498 against 04:148 | 04 says "as for duplicate Dispatch rows, line 505". DESIGN says "in the Duplicate Dispatch bullet of this section". This is a deliberate change that avoids a line number that goes stale (the bullet is at line 509 now), and the meaning is the same. | None needed. |
| F2 | MINOR | DESIGN:768 against 04:150 | The FR-010 insertion follows "and a transcript whose tail is complete" (text added by R3-B1), not directly the 04 anchor "Dispatch row's time window". The 04 clause is present word for word. | None needed. |
| F3 | MINOR | DESIGN:743 fixture 6 against 04:163 | The `(m11)` label is not repeated in the fixture's Then column. The behaviour (note order) is fully stated, and `(m11)` appears in the line 1026 revision row. | None needed. |

## Summary

- Edits PRESENT: 5 of 5 (E4 counted as one edit covering two rows, both present). Fixtures PRESENT: 7 of 7. PARTIAL: 0. MISSING: 0. m11 sentence: PRESENT.
- Checks passed: 15 / 15.
- Tool engagement: Read: 9 | Grep: 4 | Glob: 0 | Bash: 1 (line count and folder listing). Every verdict cites DESIGN text read directly in this run.
- Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Scope note: this lens covers completeness against 04 section 3 only. It does not judge whether the rule is logically consistent or whether the R3-B1 and R3-B3 edits are right; the sibling reports cover those.

Verdict: PASS
Blocking count: 0
