# R3-B2 gate, fix log, cycle 1

Edited file: `docs/designs/orchestrator-mode.md` only (1026 lines before and after). Every edit was anchored by quoted text. No research file or QA report was edited. Nothing committed, pushed or staged. The item 3.5 commands were not re-run (the orchestrator does that).

Line numbers below are the DESIGN lines after the change; the DESIGN text itself cites sections only.

## Findings fixed

| Id | Change | `file:line` after the change |
|---|---|---|
| R3B2-F1 | Added to the R3-B2 paragraph of the Joins bullet: if the transcript has `tail_complete` False the several-rows rule does not apply and no window is tested. Rows with an observable window get `session start not observable: transcript tail only`, other rows get `Dispatch time window not observable`, and the transcript is None with the tail-only note (or the window note when no row has an observable window). "The rest of this paragraph applies only when `tail_complete` is True." Added fixture `test_path_b_two_rows_incomplete_tail` (both row orders, plus a variant with `dispatch_started` None). The last sentence of the paragraph now says "joins no row because of the tail, window or several-rows rules". | `docs/designs/orchestrator-mode.md:498`; fixture at `:743`; FR-010 row `:768` |
| R3B2-F2 | Residual risk stated, no new behaviour: the Joins bullet gets "First, an open window has no upper bound ..." (a person's later session in the pane joins as False). D9, SP-29 and open item 22 state it as a new residual case, and say D9 as first written covers only True becoming None and that the owner sign-off is still pending (corrected in the re-review of item 3.16; the first wording said "the owner's earlier decision", which no record supports). Fixture `test_path_b_window_open_row_joins` now says its join is the first D9 limit and needs the owner's sign-off at step 1.0b. | `:498`, D9 `:819`, SP-29 `:857`, item 22 `:994`, fixture `:743` |
| R3B2-F3 | New note literal `session started before this Dispatch window` for a matching row whose `dispatch_started` is later than `first_record_ts`; `pane moved to a later session` is kept only for `first_record_ts` after the window end (single-row sentence and several-rows sentences both changed). For the none-holds case the transcript takes the first of the three notes any row received. Recorded the same-session-two-Dispatches limit ("Second, a second Dispatch sent to an agent still running in the pane ...") in the Joins bullet, D9, SP-29 and item 22. Added fixture `test_path_b_live_session_spans_two_dispatches`. | `:498`, `:819`, `:857`, `:994`; fixture `:743` |
| R3B2-F4 | "(a reused pane, a retry, or two rows on one terminal handle)" changed to "(a reused pane or two rows on one terminal handle)". | `:498` |
| R3B2-F5 | Duplicate Dispatch rows are merged first; the merged identity counts as one matching row, has no observable window and keeps its `conflict: duplicate Dispatch rows disagree` reason. Stated in the Joins bullet and in the Duplicate Dispatch bullet (`dispatch_started`, `dispatch_ended`, `dispatch_status` are None for the merged row). Added fixture `test_path_b_duplicate_dispatch_rows_count_once`. FR-010 row mentions the merge-first order. | `:498`, `:509`, fixture `:743`, `:768` |
| R3B2-F6 | Guard case 2 now says a transcript that matched a tab-map entry of a scoped Dispatch row and was left unjoined by the tail, window or several-rows rules carries its pane or tail note only, and the SP-16 line is not printed when every affected transcript is such a one. Fixtures `test_path_b_two_windows_hold_session_is_conflict`, `test_path_b_no_matching_window_holds`, `test_path_b_entry_failing_window_note_order` and the three new ones now assert no SP-16 line. | `:501`, fixtures `:743` |
| R3B2-F7 | The R3-B2 lead-in now states the setup: date 2026-11-08, `now` and `collected_start` 12:00, `window` 6 h, `tail_complete` True unless a fixture says otherwise, S `last_record_ts` 11:30, every row in Run R1 (in `ctx.runs`). | `:743` |
| R3B2-F8 | The Then of `test_path_b_two_windows_hold_session_is_conflict` is restated in defined terms: S is None (`person_started` None) with the `conflict:` note, no `orca:` row carries S, no SP-16 line. The "not True, not idle, not Historical" wording is removed. | `:743` |
| R3B2-F9 | Added to the Joins bullet: a join outcome that makes a row could not determine is applied after rules 1 to 8, replaces their class with rule `fallback` and keeps the rule's own evidence in `evidence`. D1 of `test_path_b_pane_reused_joins_later_row_only` now has a settled contract that rule 6 would class `finished` if the join had succeeded, and the Then says D1 is could not determine with rule `fallback`, not `finished`. | `:498`, fixture `:743` |

## Consistency places updated

| Place | What changed | Line |
|---|---|---|
| 7.2 worker bullet | All of the above | 498 |
| 7.2 guard bullet (case 2 and the printed line) | F6 | 501 |
| 7.2 Duplicate Dispatch bullet | F5 | 509 |
| 11 `test_classify.py` row | lead-in setup, edits to fixtures 1, 2, 4, 6, three new fixtures, R3-B1 open-row fixture sign-off note | 743 |
| 12 FR-010 row | merge-first and tail-first order added | 768 |
| D9 row (13) | tail-complete condition added; owner-decision wording and two residual cases | 819 |
| SP-29 row (14) | same | 857 |
| Open item 22 (17) | owner sign-off now names the two residual cases | 994 |
| `### Fix cycle 3` R3-B2 row (18) | "Gate fixes" sentence added | 1026 |

## Fixture counts

- R3-B1 path-B window fixtures in `test_classify.py`: 5, unchanged.
- R3-B2 several-rows fixtures: 7 before, 10 after (new: `test_path_b_two_rows_incomplete_tail`, `test_path_b_live_session_spans_two_dispatches`, `test_path_b_duplicate_dispatch_rows_count_once`). Four existing R3-B2 fixtures were edited (1, 2, 4, 6); fixtures 3, 5 and 7 are unchanged.
- Path-B fixtures in `test_classify.py` for R3-B1 plus R3-B2: 12 before, 15 after.
- R3-B3 fixtures: not touched (item 4.x).

## Owner attention

- R3B2-F2: Confirm that a path-B window with no end (a row still `pending` or `dispatched`) may join a person's later session in that pane as False (shown as `orca:<dispatch>`), because the DESIGN states this risk instead of bounding the window; the alternative is to count an open window only while `liveness_verdict` is `live`.
- R3B2-F3: Confirm that a live session serving two Dispatches may join the older row only while the newer row is could not determine with `session started before this Dispatch window`, because the sweep cannot tell which Dispatch the session is serving.

## Other notes

- R3B2-F9 follows the reading in the actionability report (the join outcome replaces rules 1 to 8). Under it, a row that rule 2 would have called `stalled (proved)` becomes could not determine when its path-B join fails; this is the same behaviour the single-row R3-B1 text already had, now written down.
- F3 adds one note literal, `session started before this Dispatch window`. It appears in the Joins bullet (`:498`) and in the fixtures (`:743`) only. Research/04 section 3.6 UNVERIFIED items and the DA suggestion of a 15.1 capture line for "does a second Dispatch keep the same session" were not added (not in the smallest fix); the limit is stated in D9.
- MINOR findings R3B2-F10 to R3B2-F24 were left as notes, unchanged. The "R3-B2 rule below" wording in the Joins bullet is left as it was (F10).
- No em-dash and no `TODO` or `TBD` was written; the orchestrator re-runs the item 3.5 commands.

## Orchestrator re-check (item 3.5 commands, run after the fix agent returned)

### Command 1
```
$ grep -n '^## \|^### ' docs/designs/orchestrator-mode.md
3:## 1. Status, scope and inputs
37:## 2. GQ resolutions
39:### 2.1 GQ-103(1) first: lock-free git in the seam
51:### 2.2 GQ-101 to GQ-110
74:### 2.3 GQ-111 to GQ-113 (stale REPORT citations)
82:## 3. G-1 with SP-20: report publication
86:### 3.1 Where the write lives
99:### 3.2 The one write mechanism
131:### 3.3 What a crash can leave, and why it is never reused
149:### 3.4 Final exit-1 rule
157:## 4. Component diagram
223:## 5. Sequence diagram
290:## 6. Data flow with counts
351:## 7. Interfaces
353:### 7.1 Module signatures
449:### 7.2 Data model
518:### 7.3 Allowlist constants
558:### 7.4 JSON schema v1
596:### 7.5 Report layout
613:## Source coverage
614:## Waiting on a person (a)
618:## Waiting on a person (b)
619:### Ready Tasks needing ownership review (creator not observable in Phase 1)
621:## Could not determine
622:## Retained problems
623:## Sessions (<shown>/<total>)
625:## Worktrees
626:## Historical sessions
627:## Shift Brief
628:## What I could not determine
644:### 7.6 Command and skill surface
663:## 8. WC-14 and the never-as-worker list
672:### WC-14. Coordinator loop
692:## 9. Routing and documentation changes
714:## 10. `.gitignore`
728:## 11. Test plan mapped to files
753:## 12. Traceability
805:## 13. Deviations from SPEC
841:## 14. Panel notes carried into the design
868:## 15. REPORT step mapping for `/task-builder`
870:### 15.1 What step 1.0a captures
904:### 15.2 Step table
948:## 16. Rollback
967:## 17. Open items
999:## 18. Revision log: fix cycle 1
1009:### Fix cycle 2
1019:### Fix cycle 3
```
Check 1: PASS (section map listed; 18 numbered ## headings, same 18 sections as before)

### Command 2
```
$ grep -n 'conflict: one pane session\|pane moved to a later session\|joined by pane: latest session' docs/designs/orchestrator-mode.md
498:- A worker, for FR-010, is a transcript that joins a Dispatch row 
743:| `tests/sweep/test_classify.py` | FR-006 to FR-010, FR-012 to FR-
1015:| R2-B1 | Under path B, a scoped worker's pane can move to a late
1026:| R3-B2 | Two Dispatch rows on one pane give conflicting results 
```
Check 2: PASS (4 lines carry the note literals)

### Command 3
```
$ grep -n 'exactly one window holding it\|several rows matching one pane session' docs/designs/orchestrator-mode.md
768:| FR-010 | `person_started` tri-stat
819:| D9 | FR-010 and SP-29 (line 104): 
857:| SP-29 | Applied with the D9 narrow
```
Check 3: PASS (3 lines carry the several-rows wording)

### Command 4
```
$ grep -c '—' docs/designs/orchestrator-mode.md
0
```
Check 4: PASS (expected 0)

### Command 5
```
$ grep -nw 'TODO\|TBD' docs/designs/orchestrator-mode.md
(no output; grep exit status 1 means no match)
```
Check 5: PASS (expected no output)

### Command 6
```
$ grep -n '^Total: 9 deviations.' docs/designs/orchestrator-mode.md
821:Total: 9 deviations.
```
Check 6: PASS (one hit)

### Command 7
```
$ grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md
997:Total: 23 open items.
```
Check 7: PASS (one hit)
