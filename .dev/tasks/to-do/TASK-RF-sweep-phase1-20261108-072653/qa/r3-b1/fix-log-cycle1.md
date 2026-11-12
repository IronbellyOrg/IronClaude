# R3-B1 gate, fix log cycle 1

Fix agent: single fix agent, `fix_authorization: true`. Input: `qa/r3-b1/consolidated-findings-cycle0.md` (F_0 = R3B1-F1 to R3B1-F7, |F_0| = 7). Only `docs/designs/orchestrator-mode.md` was edited (plus this log). DESIGN is now 1025 lines (it was 1023). Line numbers below are after the change.

## Fixes

| Finding | Change (anchor text) | DESIGN line after the change |
|---|---|---|
| R3B1-F1 | 15.1 item 4: replaced "present with the shapes the static bundle read gives (SQLite `YYYY-MM-DD HH:MM:SS` UTC)" with text that gives the SQLite form for `dispatchedAt` only, marks the `completedAt` form UNVERIFIED (either SQLite or ISO 8601 possible, 7.2 accepts both) and lists `status` as one of `pending`, `dispatched`, `completed`, `failed`, `circuit_broken` | 889 |
| R3B1-F2 | `OrcaObservation` row: "confirmed by step 1.0a item 4, open item 23" became "UNVERIFIED until step 1.0a item 4 (open item 23)" | 457 |
| R3B1-F2 | Worker bullet: "are confirmed by step 1.0a item 4 (open item 23)" became "are UNVERIFIED until step 1.0a item 4 confirms them (open item 23)" | 498 |
| R3B1-F2 | Open item 23 text now starts "UNVERIFIED: that `worker-show` ..." | 995 |
| R3B1-F3 | `test_path_b_window_open_row_joins`: Given now reads "row D1 with `session_join` pane P, `dispatch_started` 10:00, ... `dispatched`, a tab-map entry from P to session S, transcript S with `first_record_ts` 10:05, ..." | 743 |
| R3B1-F4 | 7.1 `probes.py`: added `parse_time(value: object) -> datetime \| None` and `parse_worker_show(run: str, list_row: object, show: object \| None) -> OrcaObservation` before `collect`; both never raise; `read_transcript_tail` and `parse_worker_show` share `parse_time` | 390, 391 |
| R3B1-F4 | 7.1 `read_transcript_tail` comment now ends "sets first_record_ts, last_record_ts and tail_complete (times via parse_time)" | 400 |
| R3B1-F4 | Boundaries table: `probes.py` may-import row now lists `datetime` | 211 |
| R3B1-F4 | 7.2 Time parsing paragraph: states `probes.parse_time` applies the rule and that `read_transcript_tail` and `parse_worker_show` call it | 470 |
| R3B1-F4 | Section 11 `test_probes_allowlist.py` cell: the path-B lead-in now names `probes.read_transcript_tail` (first three fixtures), `probes.parse_worker_show` (last three) and `probes.parse_time` | 742 |
| R3B1-F5 | 7.2 Time parsing paragraph: `now`, `collected_start`, `collected_end` and `TranscriptTail.mtime` are aware UTC `datetime` values; `collected_start` is read once at the top of `collect` before the first Orca call; `collected_end` once when `collect` returns; a naive value never reaches `classify` | 470 |
| R3B1-F5 | `SweepInput` row: `collected_start: datetime`, `collected_end: datetime` (aware UTC) | 456 |
| R3B1-F5 | Section 11 `test_classify.py` cell: the R3-B1 window fixtures lead-in says every time in them is aware UTC | 743 |
| R3B1-F6 | `TranscriptTail` row: added `tail_complete: bool` (True when the read began at byte 0; False when it began later and the first partial line was dropped, every file over 256 KiB) | 459 |
| R3B1-F6 | GQ-103(3) row: "`TranscriptTail.first_record_ts` and `tail_complete` (the path-B window)" | 60 |
| R3B1-F6 | Worker bullet: when the window is observable and `tail_complete` is False the session start is not observable; no join; row is could not determine with note `session start not observable: transcript tail only`; the transcript is None with the same note | 498 |
| R3B1-F6 | Section 11: the first reader fixture gains `tail_complete` True, the over-256 KiB fixture gains `tail_complete` False, and a new classify fixture `test_path_b_incomplete_tail_has_no_session_start` | 742, 743 |
| R3B1-F6 | Section 12 FR-010 row: path-B join also needs "a transcript whose tail is complete" | 768 |
| R3B1-F6, R3B1-F4, R3B1-F5, R3B1-F2 | Section 18 `### Fix cycle 3` R3-B1 row: now also names `tail_complete`, the aware-UTC statement, the incomplete-tail case, the two signatures, the `datetime` import, the UNVERIFIED capture item and open item, the new fixture and test-file count, and the section 12 FR-010 row | 1025 |
| R3B1-F7 | Section 11 intro: "edits to four existing test files" became "edits to three existing test files (`tests/commands/test_routing_plugin_parity.py` must also still pass, unchanged)" | 730 |

## Decisions and notes

- F4: the `parse_worker_show` signature takes the `worker-list` row and the `worker-show` result because 7.2 already says the `worker-show` value wins where both return a field. The exact argument list is a design choice; research/04 only says the parser builds `OrcaObservation`.
- F6: the incomplete-tail check runs only after the window is found observable, so `Dispatch time window not observable` keeps priority. The note text `session start not observable: transcript tail only` is new and distinct from the two existing path-B notes.
- Scope: no several-rows rule and no transcript outcome for a path-B match that does not join were written (item 3.1). The forward reference "Several matching rows follow the R3-B2 rule below." was left as it was.
- No line-number pointers into the DESIGN, em-dashes, `TODO` or `TBD` were written. Not run by the fix agent: the item 2.7 commands (the orchestrator re-runs them).
- MINOR findings R3B1-F8 to R3B1-F24 are left as notes. F17 and F18 are partly overlapped by the F1 and F2 edits (the `completedAt` form is now stated UNVERIFIED), but not closed.
- Nothing under `.claude/` was touched, staged or committed.

## Orchestrator appendix (item 2.7 re-run results)

The results are in the next section, "Orchestrator re-check".

## Orchestrator re-check (item 2.7 commands, run after the fix agent returned)

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
Check 1: PASS (headings and section numbering listed; 18 numbered sections and Fix cycle 3 present: 18 numbered ## headings)

### Command 2
```
$ grep -n 'first_record_ts\|dispatch_started\|dispatch_ended\|dispatch_status' docs/designs/orchestrator-mode.md
60:| GQ-103(3) | The model carries every field a rule reads: `SessionRow.gate_policy` (from the Task
391:def parse_worker_show(run: str, list_row: object, show: object | None) -> OrcaObservation   # ne
400:def read_transcript_tail(path: Path) -> TranscriptTail       # last 256 KiB, first partial line 
457:| `OrcaObservation` | SPEC list (line 231) plus `dispatch: str`, `run: str`, `session_join: str 
459:| `TranscriptTail` (design) | `path`, `session_id: str \| None`, `readable: bool`, `last_record_
498:- A worker, for FR-010, is a transcript that joins a Dispatch row of a scoped Run by path A or p
742:| `tests/sweep/test_probes_allowlist.py` | NFR-003, NFR-014, FR-021, FR-026, FR-020, NFR-007, GQ
743:| `tests/sweep/test_classify.py` | FR-006 to FR-010, FR-012 to FR-015, NFR-010, NFR-004, GQ-101,
1025:| R3-B1 | The path-B window compares the earliest transcript timestamp with the Dispatch row's 
```
Check 2: PASS (9 lines carry the model names)

### Command 3
```
$ grep -c '—' docs/designs/orchestrator-mode.md
0
```
Check 3: PASS (expected 0)

### Command 4
```
$ grep -nw 'TODO\|TBD' docs/designs/orchestrator-mode.md
(no output)
```
Check 4: PASS (expected no output)

### Command 5
```
$ grep -n '^Total: 9 deviations.' docs/designs/orchestrator-mode.md
821:Total: 9 deviations.
```
Check 5: PASS (one hit)

### Command 6
```
$ grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md
997:Total: 23 open items.
```
Check 6: PASS (one hit)
