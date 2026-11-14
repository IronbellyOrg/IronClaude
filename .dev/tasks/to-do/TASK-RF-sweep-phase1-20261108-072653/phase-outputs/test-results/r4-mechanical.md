# R4 mechanical gate checks (item 5.12)

Design file: `docs/designs/orchestrator-mode.md` (1043 lines). Run on 2026-11-08T23:53:47Z.

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
666:## 8. WC-16 and the never-as-worker list
675:### WC-16. Coordinator loop
707:## 9. Routing and documentation changes
729:## 10. `.gitignore`
743:## 11. Test plan mapped to files
768:## 12. Traceability
820:## 13. Deviations from SPEC
856:## 14. Panel notes carried into the design
883:## 15. REPORT step mapping for `/task-builder`
885:### 15.1 What step 1.0a captures
919:### 15.2 Step table
963:## 16. Rollback
982:## 17. Open items
1014:## 18. Revision log: fix cycle 1
1024:### Fix cycle 2
1034:### Fix cycle 3
```

## Command 2: WC-14 hits
```
$ grep -n 'WC-14' docs/designs/orchestrator-mode.md
668:**Gate.** Steps 1.17 to 1.19 are written only after the owner answers GQ-11 (step 1.0b) and step 1.16a has
831:| D6 | WC-14 (WC-16 in this design) text of SPEC section 10 (lines 404-408) | The same text renumbered WC-
854:| 1.17 | The REPORT's WC-14 (WC-16 in this design) draft | The SPEC section 10 text plus D6 (section 8) |
1043:| R4 | DESIGN was written against base `e8db2fe6`; master `5dc29d23` already has WC-14 and WC-15, a coord
```

## Command 3: WC-16 hits
```
$ grep -n 'WC-16' docs/designs/orchestrator-mode.md
5:Status: design for review, issue #339 Phase 1, written 2026-11-08 by `/sc:design --type architecture --forma
13:Phase 1 adds one read-only command, `superclaude sweep run`, a thin `/sc:sweep` command and `sc-sweep-proto
666:## 8. WC-16 and the never-as-worker list
668:**Gate.** Steps 1.17 to 1.19 are written only after the owner answers GQ-11 (step 1.0b) and step 1.16a has
672:**Final text.** The SPEC section 10 text (lines 404-408) with four changes, all deviation D6: the heading 
675:### WC-16. Coordinator loop
684:- Add to `RULE_PHRASES` (the dict at line 25), after the `"WC-15"` entry (lines 165-172) and before the `"
699:- `_check_rule` (lines 755-762) needs the rule ident on the heading line, so the WC-16 heading carries `WC
714:| R2 | Same file, `## Orca coordination` (line 396) | One bullet after the never-workers bullet (line 403)
720:| R8 | `CHANGELOG.md`, `## [Unreleased]` (line 5) | A `### sweep: read-only supervision snapshot (Phase 1)
734:# superclaude sweep reports: dated, operator-local, never posted (WC-16). Never tracked.
796:| FR-023 | WC-16 and the never-as-worker addition (8) | `tests/skills/test_worker_contract.py` |
831:| D6 | WC-14 (WC-16 in this design) text of SPEC section 10 (lines 404-408) | The same text renumbered WC-
854:| 1.17 | The REPORT's WC-14 (WC-16 in this design) draft | The SPEC section 10 text plus D6 (section 8) |
945:| 1.17 | | WC-16 in `src/superclaude/core/WORKER-CONTRACT.md` | 8 | 1.0b (GQ-11 answered), 1.16a |
972:| WC-16 with the D6 sentence, the line 23 never-as-worker entry, the `RULE_PHRASES["WC-16"]` entry, the `R
1007:| 20 | Owner decisions GQ-10, GQ-11 (WC-16 approval), GQ-35, GQ-61 and GQ-63 | Step 1.0b | Steps 1.17 to 
1008:| 21 | PR #422 overlap with WC-16, the never-as-worker list and the #409 dimensions | Step 1.16a | Steps 
1043:| R4 | DESIGN was written against base `e8db2fe6`; master `5dc29d23` already has WC-14 and WC-15, a coord
```

## Command 4: old insertion text
```
$ grep -n 'after line 561\|519-561' docs/designs/orchestrator-mode.md
(no output expected; grep exit status 1)
```

## Command 5: cadence phrase
```
$ grep -n 'at most once every 5 minutes' docs/designs/orchestrator-mode.md
672:**Final text.** The SPEC section 10 text (lines 404-408) with four changes, all deviation D6: the heading 
677:The coordinator keeps watching its Run until every Task it created is settled and every result has been in
714:| R2 | Same file, `## Orca coordination` (line 396) | One bullet after the never-workers bullet (line 403)
831:| D6 | WC-14 (WC-16 in this design) text of SPEC section 10 (lines 404-408) | The same text renumbered WC-
1043:| R4 | DESIGN was written against base `e8db2fe6`; master `5dc29d23` already has WC-14 and WC-15, a coord
```

## Command 6: step 1.16a hits
```
$ grep -n '1.16a' docs/designs/orchestrator-mode.md
668:**Gate.** Steps 1.17 to 1.19 are written only after the owner answers GQ-11 (step 1.0b) and step 1.16a has
917:Pre-implementation steps: 1.0a (this capture), 1.0b (owner decisions) and 1.16a (the record-only PR #422 c
944:| 1.16a | Pre | Record-only: write `.dev/tasks/<pkg>/artifacts/pr422-409-check.md` with four points: (1) t
945:| 1.17 | | WC-16 in `src/superclaude/core/WORKER-CONTRACT.md` | 8 | 1.0b (GQ-11 answered), 1.16a |
977:| Step artifacts under `.dev/tasks/<pkg>/artifacts/` (design: `readonly-probe.md`, `owner-decisions.md`, t
1008:| 21 | PR #422 overlap with WC-16, the never-as-worker list and the #409 dimensions | Step 1.16a | Steps 
1043:| R4 | DESIGN was written against base `e8db2fe6`; master `5dc29d23` already has WC-14 and WC-15, a coord
```

## Command 7: em-dash count
```
$ grep -c '—' docs/designs/orchestrator-mode.md
0
```

## Command 8: TODO or TBD
```
$ grep -nw 'TODO\|TBD' docs/designs/orchestrator-mode.md
(no output expected; grep exit status 1)
```

## Command 9: deviation total
```
$ grep -n '^Total: 9 deviations.' docs/designs/orchestrator-mode.md
836:Total: 9 deviations.
```

## Command 10: open-item total
```
$ grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md
1012:Total: 23 open items.
```

## Checks

- Check 1: PASS - every WC-14 hit is a worker rule (keep) hit (the section 8 on-master sentence, 1, and the section 18 R4 row that names master WC-14, 1) or one of the two section 13 historical names (2), each followed by (WC-16 in this design)
- Check 2: PASS - WC-16 appears in sections 1, 8, 9, 10, 12, 13, 15, 16 and 17
- Check 3: PASS - no 'after line 561' or '519-561' text; 'after line 565' appears 2 times
- Check 4: PASS - the cadence phrase is in section 8 (2 lines) and in the WC-16 block (1)
- Check 5: PASS - no 'wait for', 'follow-up PR', 'rebase' or 'if #422 is open' wording on any 1.16a line
- Check 6: PASS - em-dash count is 0
- Check 7: PASS - no TODO or TBD
- Check 8: PASS - one 'Total: 9 deviations.' hit
- Check 9: PASS - one 'Total: 23 open items.' hit
- Check 10: PASS - 18 numbered ## sections, as before

Result: 10 of 10 checks PASS.
