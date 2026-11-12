# R3-B2 mechanical gate checks (item 3.5)

Design file: `docs/designs/orchestrator-mode.md` (1026 lines). Section 7.2 is lines 449-517, the worker bullet is line 498, section 11 is lines 728-752. Run on 2026-11-08T21:10:08Z.

## Command 1: section map
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

## Command 2: note literals
```
$ grep -n 'conflict: one pane session\|pane moved to a later session\|joined by pane: latest session' docs/designs/orchestrator-mode.md
498:- A worker, for FR-010, is a transcript that joins a Dis
743:| `tests/sweep/test_classify.py` | FR-006 to FR-010, FR-
1015:| R2-B1 | Under path B, a scoped worker's pane can move
1026:| R3-B2 | Two Dispatch rows on one pane give conflictin
```

## Command 3: rule wording in rows
```
$ grep -n 'exactly one window holding it\|several rows matching one pane session' docs/designs/orchestrator-mode.md
768:| FR-010 | `person_started
819:| D9 | FR-010 and SP-29 (l
857:| SP-29 | Applied with the
```

## Command 4: em-dash count
```
$ grep -c '—' docs/designs/orchestrator-mode.md
0
```

## Command 5: TODO or TBD
```
$ grep -nw 'TODO\|TBD' docs/designs/orchestrator-mode.md
(no output expected; grep exit status 1 means no match)
```

## Command 6: deviation total
```
$ grep -n '^Total: 9 deviations.' docs/designs/orchestrator-mode.md
821:Total: 9 deviations.
```

## Command 7: open-item total
```
$ grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md
997:Total: 23 open items.
```

## Outcome-to-fixture table (check 2 reads it)

| Outcome | 7.2 sentence (worker bullet, line 498) | Fixture in section 11 | Hits in 7.2 | Hits in 11 |
|---|---|---|---|---|
| One matching row's window holds the transcript | "If exactly one matching row's window holds the transcript, the transcript joins that row only and is False with note `joined by pane: latest session of the pane`" | `test_path_b_pane_reused_joins_later_row_only` | 1 | 1 |
| Two or more matching rows' windows hold it | "If two or more matching rows' windows hold it, it joins none of them" (note `conflict: one pane session matches several Dispatch rows`) | `test_path_b_two_windows_hold_session_is_conflict` and `test_path_b_shared_boundary_second_is_conflict` | 1 | 1 and 1 |
| No matching row's window holds it | "If no matching row's window holds it, every matching row is could not determine with its note" | `test_path_b_no_matching_window_holds` | 1 | 1 |

## Checks

- Check 1: PASS - 7.2 gives exactly one sentence for each of the three outcomes (one holds, two or more hold, none holds)
- Check 2: PASS - each outcome has a fixture in section 11 (table above)
- Check 3: PASS - D9, SP-29 and the FR-010 row carry the several-rows wording (1 1 1)
- Check 4: PASS - em-dash count is 0
- Check 5: PASS - no TODO or TBD
- Check 6: PASS - one 'Total: 9 deviations.' hit
- Check 7: PASS - one 'Total: 23 open items.' hit

Result: 7 of 7 checks PASS.
