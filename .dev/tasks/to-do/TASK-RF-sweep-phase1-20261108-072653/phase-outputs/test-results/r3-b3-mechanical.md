# R3-B3 mechanical gate checks (item 4.6)

Design file: `docs/designs/orchestrator-mode.md` (1030 lines). Section 7.2 is lines 449-518, section 7.4 is lines 559-598, section 11 is lines 731-755. Run on 2026-11-08T22:07:38Z.

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

## Command 2: outage and uncaptured continuation
```
$ grep -n 'outage\|uncaptured continuation' docs/designs/orchestrator-mode.md
11:- R3-B3: three SPEC FR-010 fixtures (outage, full page, `call_faile
746:| `tests/sweep/test_classify.py` | FR-006 to FR-010, FR-012 to FR-
771:| FR-010 | `person_started` tri-state, completeness guard with its
1030:| R3-B3 | Three SPEC FR-010 fixtures (outage, full page, `call_fa
```

## Command 3: the origin unknown literals
```
$ grep -n 'origin unknown:' docs/designs/orchestrator-mode.md
501:- List-incomplete cases (SPEC FR-010): no transcript can be proved
746:| `tests/sweep/test_classify.py` | FR-006 to FR-010, FR-012 to FR-
1030:| R3-B3 | Three SPEC FR-010 fixtures (outage, full page, `call_fa
```

## Command 4: "four incomplete cases" count
```
$ grep -c 'four incomplete cases' docs/designs/orchestrator-mode.md
1
```

## Command 5: the per-Run source row name
```
$ grep -n 'orca worker-list <run>' docs/designs/orchestrator-mode.md
501:- List-incomplete cases (SPEC FR-010): no transcript can be proved
595:Each scoped Run's `worker-list` call has its own source row named 
1030:| R3-B3 | Three SPEC FR-010 fixtures (outage, full page, `call_fa
```

## Command 6: em-dash count
```
$ grep -c '—' docs/designs/orchestrator-mode.md
0
```

## Command 7: TODO or TBD
```
$ grep -nw 'TODO\|TBD' docs/designs/orchestrator-mode.md
(no output expected; grep exit status 1 means no match)
```

## Command 8: deviation total
```
$ grep -n '^Total: 9 deviations.' docs/designs/orchestrator-mode.md
824:Total: 9 deviations.
```

## Command 9: open-item total
```
$ grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md
1000:Total: 23 open items.
```

## Pass-rule counts (lines per section range)

| Text | 7.2 | 7.4 | 11 |
|---|---|---|---|
| `origin unknown: Orca unavailable` | 1 | 0 | 1 |
| `origin unknown: worker list truncated` | 1 | 0 | 1 |
| `origin unknown: worker list call failed` | 1 | 0 | 1 |
| `orca worker-list <run>` | 1 | 1 | 0 |
| `outage` | 0 | 0 | 1 |
| `uncaptured continuation` | 0 | 0 | 1 |
| `four incomplete cases` | 0 | 0 | 0 |

## Checks

- Check 1: PASS - "outage" and "uncaptured continuation" appear in section 11
- Check 2: PASS - the three origin unknown literals are in 7.2
- Check 3: PASS - the three origin unknown literals are in section 11
- Check 4: PASS - "four incomplete cases" is absent from section 11 and from every section before 18; the 1 remaining hit(s) are in section 18 (the Fix cycle 3 R3-B3 row quotes cycle 2's wording to correct it)
- Check 5: PASS - the source row name appears in 7.2 and in 7.4
- Check 6: PASS - em-dash count is 0
- Check 7: PASS - no TODO or TBD
- Check 8: PASS - one 'Total: 9 deviations.' hit
- Check 9: PASS - one 'Total: 23 open items.' hit

Result: 9 of 9 checks PASS.
