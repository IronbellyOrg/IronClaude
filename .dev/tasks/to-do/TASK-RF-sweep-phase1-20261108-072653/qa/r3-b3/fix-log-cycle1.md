# R3-B3 gate, cycle 1: fix log

Fix agent: single fix agent, `fix_authorization: true`. Only file edited: `docs/designs/orchestrator-mode.md` (still 1030 lines; no line was added or removed, long lines were edited in place). Line numbers below are the lines after the change. Totals unchanged: `Total: 9 deviations.` (line 824) and `Total: 23 open items.` (line 1000). No `orca` command, no network call, no commit, no staging.

## Findings fixed

| Id | Change | Location after change |
|---|---|---|
| R3B3-F1 (BLOCKING) | The list-incomplete bullet now has a Run-not-confirmed case: a scoped Run whose `orca worker-list <run>` row has no `unscanned` and has no `OrcaObservation`, while its `orca task-list <run>` row has `unscanned`, only while `orca_available` is True; note `origin unknown: Run not confirmed`. The bullet states that an unknown Run id gives a complete empty `worker-list` (exit 0, `ok` true; live read 2026-11-08, UNVERIFIED until step 1.0a item 8) and that a real Run with zero rows and a `task-list` that did not fail is complete. Sequence diagram line reworded to `unknown Run id: ok, zero rows; task-list --run R fails (7.2)`. Capture item 8 reworded (what `worker-list` returns for an unknown id; error shape of `task-list`). Open item 4 reworded (the "Behaviour until closed" cell keeps the nonzero-exit-on-call-one rule and adds the empty-list rule). New fixture `test_fr010_unknown_run_empty_list_unknown`. No new open item, no new deviation. | 245, 501, 896, 979, 746 |
| R3B3-F2 | Deleted "in the window" from the join-guard bullet: now `every unjoined transcript is None, in four cases`. | 502 |
| R3B3-F3 | Added a shared Given with a second transcript U joined by `sessionId` to D1 (so guard case 2 does not hold), named the control (T is True with the `origin not proved` note and Historical), replaced "differ by one input" with "each fixture changes only the list-completeness inputs it names", and stated that T's notes are exactly the one `origin unknown:` note the fixture names (no SP-16 literal, no `tab map join not observable`). | 746 |
| R3B3-F4 | `test_fr010_incomplete_notes_order` now has an exact Given and note list. Part (a): R1 ok with D1 whose `session_join` is None, then `orca_available` False, no U; notes exactly `origin unknown: Orca unavailable`, the SP-16 literal, `tab map join not observable`. Part (b): R1 100 rows `truncated`, R2 `call_failed`, R3 zero rows with `orca task-list R3` unscanned, `ccsession orca-tabs` unscanned; notes exactly truncated, call failed, Run not confirmed, tab map unreadable, no join-guard note. The 7.2 bullet now says every note that holds is attached, in a stated order, before any join-guard note. | 501, 746 |
| R3B3-F5 | `call_failed` trigger rewritten: the `orca worker-list <run>` row has `unscanned` set while `orca_available` is True; the outage note alone covers the unavailable case (the rows left unread after an outage carry `unscanned: orca unavailable` and do not also count); a budget cut counts. Fixture 1 now says `sources` holds `orca worker-list R1` with `unscanned` `orca unavailable` and T carries exactly one `origin unknown:` note; fixture 3 says `orca_available` True is what the trigger needs. The bullet states that `classify_all` evaluates all five cases from `orca_available`, `truncated`, `orca_rows` and `sources` only. | 501, 746 |
| R3B3-F6 | Fifth list-incomplete case (the SPEC's fourth reason) added: `collect` set `unscanned` on the source row `ccsession orca-tabs` (the folder exists but cannot be listed or read; a missing folder and an empty readable folder are not this case); note `origin unknown: tab map unreadable`, placed last in the note order. New non-SPEC fixture `test_fr010_tab_map_unreadable_older_transcript_unknown`; the FR-010 row names it. No deviation recorded. | 501, 595, 746, 771 |
| R3B3-F7 | Section 7.2 and 7.4 now say every Run in `ctx.runs` has the rows `orca worker-list <run>` and `orca task-list <run>`; a Run whose `worker-list` was never started because the budget ran out carries `unscanned: time budget reached (90 s)` and counts as `call_failed` for this rule. New fixture `test_fr010_run_not_reached_budget_unknown`. | 501, 595, 746 |
| R3B3-F8 | Fixture 2 is a hand-built `SweepInput` (100 `OrcaObservation` rows, distinct Dispatch ids, `session_join` values different from T's, one matching U, `truncated` True); `page.nextCursor` is no longer a Given input and is tagged UNVERIFIED with a pointer to step 1.0a item 3 and open item 5; the page-to-flag rule moved to the `collect` test (F9). | 746 |
| R3B3-F9 | `test_probes_allowlist.py` row gains `test_collect_worker_list_source_rows_and_truncated` (row names exactly `orca worker-list R1` and `orca worker-list R2`, literal `orca` prefix, R2 `unscanned` non-null and R1 None, `task-list` failure on `orca task-list R2`, budget-spent R2, unreadable and missing `orca-tabs/` folder, `truncated` True at 100 rows and False at 99). `test_report.py` row gains the lower-bound line `[Orca rows: 100 shown; total is a lower bound (paging not yet captured)]` and `summary.total_is_lower_bound` True. Section 7.4 states the row names and that `collect` sets `truncated` at `WORKER_LIST_PAGE` rows. | 745, 747, 595 |
| Section 18 | Gate fixes sentence added to the R3-B3 row of the `Fix cycle 3` table. The phrase "four incomplete cases" still appears once, in that row's correction of cycle 2. | 1030 |
| FR-010 row | Now says five list-incomplete cases (three SPEC cases, the SPEC tab-map reason, and the design's Run not confirmed), the notes attached in one order, four join-incomplete cases unchanged, and names the new fixtures, the `collect` test and the lower-bound line test. | 771 |

## Deviations from the "Smallest fix" lines

1. Counting. R3B3-F1 and R3B3-F6 both call their trigger "the fourth". Both are added, so the rule has five cases: the SPEC's four reasons (Orca unavailable, truncated, `call_failed`, tab map unreadable) plus the design's Run not confirmed. "Three SPEC list-incomplete cases" and "three SPEC incomplete-case fixtures" are kept as the SPEC count; "four join-incomplete cases" is untouched.
2. Note literal for F1. The consolidated file says "a fourth note"; the DA report names it `origin unknown: Run not confirmed`. I used that literal.
3. F7 smallest fix says "state in `:501` and `:595`". Done. I also named the sibling row `orca task-list <run>` in section 7.4, because the Run-not-confirmed rule needs a row `classify_all` can read.
4. F3 smallest fix adds U "as in the control". The control in section 11 had no stated Given, so I wrote one (T True with `origin not proved`, Historical).

## Not changed (outside the nine ids)

- `test_cli_contract.py` row still lists "unknown-Run then R2" as a Run id case (line 749). It tests the nonzero-exit unknown-Run shape, which stays pending step 1.0a item 8; with the live read it may need a later reword (MINOR R3B3-F15).
- research/04 4.3 fixture 3 still says "a nonzero exit on call one is `unavailable`"; it is a research file and out of scope.
- MINOR findings F10 to F25 untouched.

## Owner attention

- R3B3-F1: an empty `worker-list` for a scoped Run counts as complete only while `task-list --run <run>` did not fail; the owner could instead choose to treat any zero-row Run as incomplete (safer, but a real Run with no workers would then hide every older unjoined transcript behind `origin unknown:`).
- R3B3-F6: the SPEC's "tab map unreadable" is enforced as a rule (no deviation recorded). The owner could instead rule the SPEC sentence illustrative and record a deviation, which would change `Total: 9 deviations.`.
- R3B3-F6: a missing `orca-tabs/` folder is treated as readable and empty, not as unreadable. The owner could reverse this so a missing folder also gives `origin unknown: tab map unreadable`.
- R3B3-F5: after an outage only the outage note is attached; the owner could prefer to also show `worker list call failed` for the unscanned rows.
- R3B3-F7: a Run the budget never reached is `call_failed` (note `origin unknown: worker list call failed`), not a separate note.

## Fixture counts

`test_fr010_*` fixtures in the section 11 `test_classify.py` cell: before 4 (`test_fr010_outage_older_transcript_unknown_not_historical`, `test_fr010_full_page_uncaptured_continuation`, `test_fr010_call_failed_incomplete_list`, `test_fr010_incomplete_notes_order`); after 7 (added `test_fr010_unknown_run_empty_list_unknown`, `test_fr010_run_not_reached_budget_unknown`, `test_fr010_tab_map_unreadable_older_transcript_unknown`). Plus the control (not a `test_fr010_*` name) and one new `collect` test in `test_probes_allowlist.py`, `test_collect_worker_list_source_rows_and_truncated`.

Read-only checks run by this agent after editing (the orchestrator re-runs the mechanical commands): em dash 0, en dash 0, placeholder tokens 0, "four incomplete cases" 1 (section 18 correction row only), `Total: 9 deviations.` and `Total: 23 open items.` present, file length 1030 lines.

## Orchestrator re-check (item 4.6 commands, run after the fix agent returned)

Design file: `docs/designs/orchestrator-mode.md` (1030 lines). Section 7.2 is lines 449-518, 7.4 is lines 559-598, section 11 is lines 731-755, section 18 starts at line 1002.

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
519:### 7.3 Allowlist constants
559:### 7.4 JSON schema v1
599:### 7.5 Report layout
616:## Source coverage
617:## Waiting on a person (a)
621:## Waiting on a person (b)
622:### Ready Tasks needing ownership review (creator not observable in Phase 1)
624:## Could not determine
625:## Retained problems
626:## Sessions (<shown>/<total>)
628:## Worktrees
629:## Historical sessions
630:## Shift Brief
631:## What I could not determine
647:### 7.6 Command and skill surface
666:## 8. WC-14 and the never-as-worker list
675:### WC-14. Coordinator loop
695:## 9. Routing and documentation changes
717:## 10. `.gitignore`
731:## 11. Test plan mapped to files
756:## 12. Traceability
808:## 13. Deviations from SPEC
844:## 14. Panel notes carried into the design
871:## 15. REPORT step mapping for `/task-builder`
873:### 15.1 What step 1.0a captures
907:### 15.2 Step table
951:## 16. Rollback
970:## 17. Open items
1002:## 18. Revision log: fix cycle 1
1012:### Fix cycle 2
1022:### Fix cycle 3
```
Check 1: PASS (section map listed; 18 numbered ## headings, same 18 sections as before)

### Command 2
```
$ grep -n 'outage\|uncaptured continuation' docs/designs/orchestrator-mode.md
11:- R3-B3: three SPEC FR-010 fixtures (outage, full page, `call_faile
501:- List-incomplete cases (SPEC FR-010): no transcript can be proved
746:| `tests/sweep/test_classify.py` | FR-006 to FR-010, FR-012 to FR-
771:| FR-010 | `person_started` tri-state, completeness guard with its
1030:| R3-B3 | Three SPEC FR-010 fixtures (outage, full page, `call_fa
```
Check 2: PASS (both words appear in section 11)

### Command 3
```
$ grep -n 'origin unknown:' docs/designs/orchestrator-mode.md
501:- List-incomplete cases (SPEC FR-010): no transcript can be proved
746:| `tests/sweep/test_classify.py` | FR-006 to FR-010, FR-012 to FR-
1030:| R3-B3 | Three SPEC FR-010 fixtures (outage, full page, `call_fa
```
Check 3: PASS (the five origin unknown literals (the three SPEC FR-010 literals, the tab map unreadable literal and the Run not confirmed literal) are in 7.2 and in section 11)

### Command 4
```
$ grep -c 'four incomplete cases' docs/designs/orchestrator-mode.md
1
```
Check 4: PASS (absent from section 11 and from every section before 18; the 1 remaining hit(s) are in section 18 (the Fix cycle 3 R3-B3 row quotes cycle 2's wording to correct it))

### Command 5
```
$ grep -n 'orca worker-list <run>' docs/designs/orchestrator-mode.md
501:- List-incomplete cases (SPEC FR-010): no transcript can be proved
595:Every Run in `ctx.runs` has its own source row named `orca worker-
1030:| R3-B3 | Three SPEC FR-010 fixtures (outage, full page, `call_fa
```
Check 5: PASS (the source row name appears in 7.2 and in 7.4)

### Command 6
```
$ grep -c '—' docs/designs/orchestrator-mode.md
0
```
Check 6: PASS (expected 0)

### Command 7
```
$ grep -nw 'TODO\|TBD' docs/designs/orchestrator-mode.md
(no output; grep exit status 1; 1 means no match)
```
Check 7: PASS (expected no output)

### Command 8
```
$ grep -n '^Total: 9 deviations.' docs/designs/orchestrator-mode.md
824:Total: 9 deviations.
```
Check 8: PASS (one hit)

### Command 9
```
$ grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md
1000:Total: 23 open items.
```
Check 9: PASS (one hit)

Result: 9 of 9 checks PASS.
