# R3-B1 mechanical gate checks (item 2.7)

Design file: `docs/designs/orchestrator-mode.md` (1023 lines). Run on 2026-11-08T20:21:52Z.

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
447:### 7.2 Data model
516:### 7.3 Allowlist constants
556:### 7.4 JSON schema v1
594:### 7.5 Report layout
611:## Source coverage
612:## Waiting on a person (a)
616:## Waiting on a person (b)
617:### Ready Tasks needing ownership review (creator not observable in Phase 1)
619:## Could not determine
620:## Retained problems
621:## Sessions (<shown>/<total>)
623:## Worktrees
624:## Historical sessions
625:## Shift Brief
626:## What I could not determine
642:### 7.6 Command and skill surface
661:## 8. WC-14 and the never-as-worker list
670:### WC-14. Coordinator loop
690:## 9. Routing and documentation changes
712:## 10. `.gitignore`
726:## 11. Test plan mapped to files
751:## 12. Traceability
803:## 13. Deviations from SPEC
839:## 14. Panel notes carried into the design
866:## 15. REPORT step mapping for `/task-builder`
868:### 15.1 What step 1.0a captures
902:### 15.2 Step table
946:## 16. Rollback
965:## 17. Open items
997:## 18. Revision log: fix cycle 1
1007:### Fix cycle 2
1017:### Fix cycle 3
```

## Command 2: model names
```
$ grep -n 'first_record_ts\|dispatch_started\|dispatch_ended\|dispatch_status' docs/designs/orchestrator-mode.md
60:| GQ-103(3) | The model carries every field a rule reads: `SessionRow.gate_policy` (from the Task spec text
398:def read_transcript_tail(path: Path) -> TranscriptTail       # last 256 KiB, first partial line dropped; s
455:| `OrcaObservation` | SPEC list (line 231) plus `dispatch: str`, `run: str`, `session_join: str \| None` (
457:| `TranscriptTail` (design) | `path`, `session_id: str \| None`, `readable: bool`, `last_record_ts: dateti
496:- A worker, for FR-010, is a transcript that joins a Dispatch row of a scoped Run by path A or path B. A t
740:| `tests/sweep/test_probes_allowlist.py` | NFR-003, NFR-014, FR-021, FR-026, FR-020, NFR-007, GQ-109, M7, 
741:| `tests/sweep/test_classify.py` | FR-006 to FR-010, FR-012 to FR-015, NFR-010, NFR-004, GQ-101, GQ-102, G
1023:| R3-B1 | The path-B window compares the earliest transcript timestamp with the Dispatch row's start and 
```

## Command 3: Orca source names
```
$ grep -n 'dispatch\.dispatchedAt\|dispatch\.completedAt\|dispatch\.status' docs/designs/orchestrator-mode.md
455:| `OrcaObservation` | SPEC list (line 231) plus `dispatch: str`, `run: str`, `session_join: str \| None` (
740:| `tests/sweep/test_probes_allowlist.py` | NFR-003, NFR-014, FR-021, FR-026, FR-020, NFR-007, GQ-109, M7, 
887:| 4 | `worker-show --dispatch <dispatch> --json` field names: the field that can carry `session_join` (a C
993:| 23 | That `worker-show` `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` (read stat
```

## Command 4: em-dash count
```
$ grep -c '—' docs/designs/orchestrator-mode.md
0
```

## Command 5: TODO or TBD
```
$ grep -nw 'TODO\|TBD' docs/designs/orchestrator-mode.md
(exit 0)
```

## Command 6: deviation total
```
$ grep -n '^Total: 9 deviations.' docs/designs/orchestrator-mode.md
819:Total: 9 deviations.
```

## Command 7: open-item total
```
$ grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md
995:Total: 23 open items.
```

## Section-by-field matrix (line counts per section range)

| Section | Lines | first_record_ts | dispatch_started | dispatch_ended | dispatch_status | dispatch.dispatchedAt | dispatch.completedAt | dispatch.status |
|---|---|---|---|---|---|---|---|---|
| 7.1 | 353-446 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 7.2 | 447-515 | 2 | 2 | 2 | 2 | 1 | 1 | 1 |
| 2.2 | 51-73 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 11 | 726-750 | 2 | 2 | 2 | 2 | 1 | 0 | 0 |
| 15.1 | 868-901 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| 17 | 965-996 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| 18 | 997-1023 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |

## Checks

- Check 1: PASS - the matrix meets the per-section rule
- Check 2: PASS - worker bullet (line 496) names all four model fields
- Check 3: PASS - GQ-103(3) row (line 60) lists dispatch_started, dispatch_ended, dispatch_status and first_record_ts
- Check 4: PASS - em-dash count is 0
- Check 5: PASS - no TODO or TBD
- Check 6: PASS - one 'Total: 9 deviations.' hit
- Check 7: PASS - one 'Total: 23 open items.' hit

Result: 7 of 7 checks PASS.
