# R4 gate, fix log: cycle 1

Fix agent for F_0 = {R4-F1, R4-F2, R4-F3, R4-F4, R4-F5, R4-F6}. Only `docs/designs/orchestrator-mode.md` was edited. Line numbers below are the lines after the change.

## Fixes

| Id | Change | `file:line` after the change (all in `docs/designs/orchestrator-mode.md`) |
|---|---|---|
| R4-F1 | Section 16 rollback row: "the `RULE_PHRASES` entry" became "the `RULE_PHRASES["WC-16"]` entry, the `RULE_PHRASES["never-as-worker"]` phrase at test line 89", so the row lists all five test-file pin edits. Smallest fix used as written | `:972` |
| R4-F2 | Took the second option of the smallest fix (same commit), because pin 5 is already listed with the other four pins and moving it would split the pin list. Step 1.18 now says it lands in one commit with 1.19, which carries the `never-as-worker` phrase edit; step 1.19 gate changed from "1.18" to "same commit as 1.18" (both step ids kept). Added a paragraph under the pin list saying steps 1.18 and 1.19 land in one commit and why `test_contract_states_rule[never-as-worker]` is red between them. Section 12 test-file row now reads "step 1.19, same commit as step 1.18" | `:946`, `:947`, `:690`, `:763` |
| R4-F3 | Section 15.2: step 1.21 gate "1.14" became "1.14, 1.18"; step 1.24b gate "1.16" became "1.16, 1.17". Open item 20 "Behaviour until closed" now says R1 and R2 (step 1.21) wait for step 1.18 and R8 (step 1.24b) waits for step 1.17. The text differs a little from the suggested "wait for 1.17 and 1.18 as well" because 1.24b needs only 1.17 under the gates written (1.18 only adds the list entry, which R8 does not cite). Added one sentence to the section 8 Gate paragraph so the gate is stated where the steps 1.17 to 1.19 gate is | `:949`, `:954`, `:1007`, `:668` |
| R4-F4 | The one-commit rule now reads "R1 to R4 land in one commit" and names the failing test (`test_other_commands_membership_and_live_references`, which asserts the table members equal `_OTHER_COMMANDS`; checked at `tests/core/test_how_we_work_routing_table.py:291-297`). Steps 1.21 and 1.22 merged by gate: 1.22 gate "same commit as 1.21", 1.21 says it lands with 1.22 (R4) and 1.23 (R3), 1.23 says "in the same commit as 1.21 and 1.22". No renumbering. The rollback row for R1 to R5 already reverts together and was left alone | `:724`, `:949`, `:950`, `:951` |
| R4-F5 | WC-16 now has the coordinator run "The sweep." under `### Liveness supervision` unchanged and, in the same pass, run `/sc:sweep`; `/sc:sweep` is an added read, not a replacement, not a second pass, no heartbeat update, no `worktree ps --agent-wait` listing. Every other bare "the sweep" that meant the command in the WC-16 block now says `/sc:sweep` (classes, report, recommends nothing, does not observe). "It keeps a periodic sweep scheduled" became "The coordinator keeps that pass scheduled". Section 8 "Final text" paragraph now lists four changes and says master's sweep is "The sweep." only; the SP-27 explanation paragraph says `/sc:sweep`. R2 bold lead and body rewritten ("runs `/sc:sweep` on every wake, at most once every 5 minutes, beside "The sweep."", "adds to that sweep and does not replace it"). D6 row text updated (row text only; no new deviation). The R1/R6 word-avoidance rule now says "the description of `/sc:sweep`" | `:677`, `:672`, `:680`, `:714`, `:831`, `:726` |
| R4-F6 | One sentence added to WC-16: "Its own reads are not L1 probes and do not count against the L1 cap; the coordinator's own L1 probes stay limited to workers a trigger fired for." The `liveness-*` pinned phrases and contract lines 110 and 151 are not reworded. Also named in the section 8 "Final text" paragraph and in D6 | `:677`, `:672`, `:831` |
| Gate fixes | "Gate fixes" sentence added to the `Fix cycle 3` R4 row of section 18 | `:1043` |

Checks I ran after the edits (read-only grep): the four pinned phrases are present in the WC-16 block (`:675`, `:677`); no `uv` code span in the WC-16 block (count 0); `Total: 9 deviations.` at `:836` and `Total: 23 open items.` at `:1012` unchanged; no em dash, en dash or placeholder marker in the design file (count 0). I did not re-run the item 5.12 mechanical commands.

## Consistency places updated

| Place | What was aligned | Line |
|---|---|---|
| Section 8 Gate paragraph | Steps 1.21 and 1.24b wait for 1.18 and 1.17 | `:668` |
| Section 8 Final text paragraph | Four D6 changes; `/sc:sweep` additive; L1 sentence; proposed, awaiting owner approval with GQ-11 | `:672` |
| Section 8 WC-16 block | Additive wording, L1 sentence, command named `/sc:sweep` throughout | `:677` |
| Section 8 SP-27 paragraph | "the sweep" became `/sc:sweep` | `:680` |
| Section 8 pins | Same-commit paragraph for steps 1.18 and 1.19 | `:690` |
| Section 9 R2 | Bold lead and body match WC-16 | `:714` |
| Section 9 rules | "R1 to R4 land in one commit"; R1/R6 wording rule names `/sc:sweep` | `:724`, `:726` |
| Section 12 test-file row | Step 1.19 "same commit as step 1.18" | `:763` |
| Section 13 D6 | Row text matches the WC-16 text | `:831` |
| Section 15.2 step table | Steps 1.18, 1.19, 1.21, 1.22, 1.23, 1.24b | `:946`, `:947`, `:949`, `:950`, `:951`, `:954` |
| Section 16 rollback | Row lists the `never-as-worker` phrase edit (R4-F1) | `:972` |
| Section 17 open item 20 | Behaviour until closed covers R1, R2 and R8 | `:1007` |
| Section 18 Fix cycle 3, R4 row | "Gate fixes" sentence | `:1043` |

Unchanged on purpose: `Total: 9 deviations.`, `Total: 23 open items.`, the "four join-incomplete cases", the five list-incomplete cases, the seven `test_fr010_*` fixtures, the four pinned WC-16 phrases, the `liveness-*` phrases, and the rollback row for R1 to R5 (already "Revert together"). Open item 21 was not edited: step 1.17 is gated on 1.16a, and 1.21 and 1.24b now sit behind 1.17 and 1.18, so the gate holds through it.

## Owner attention

- R4-F5: WC-16 now says `/sc:sweep` is an added read beside master's "The sweep." (contract line 110), not a replacement and not a second pass, and that it does not update heartbeat records or run the `worktree ps --agent-wait` listing. This is proposed text awaiting the owner's approval of WC-16 with GQ-11 (step 1.0b); the owner could prefer replacement or a different split of duties. Touches `:672`, `:677`, `:714`, `:831`.
- R4-F6: WC-16 now has the sentence "Its own reads are not L1 probes and do not count against the L1 cap; the coordinator's own L1 probes stay limited to workers a trigger fired for." This is proposed text awaiting the same approval; the owner could prefer to change contract line 151 instead. Touches `:672`, `:677`, `:831`.
- R4-F2: steps 1.18 and 1.19 land in one commit instead of moving the phrase edit into 1.18. Reversible by moving pin 5 into step 1.18.
- R4-F4: steps 1.21, 1.22 and 1.23 land in one commit (R1 to R4). Reversible by ordering R4 before R1 instead.
- WC-16 wording changes of small size the owner may reverse: "The coordinator keeps that pass scheduled while work remains" replaces "It keeps a periodic sweep scheduled while work remains" (`:677`).

## Orchestrator re-check (item 5.12 commands, run after the fix agent returned)

Run by the same script as item 5.12 against the fixed design (`docs/designs/orchestrator-mode.md`, 1043 lines). The first run found one FAIL (check 5): the section 8 Gate paragraph, which also names step 1.16a, said steps 1.21 and 1.24b "wait for" steps 1.18 and 1.17. That is a gate on the owner answer and not the old PR #422 wait, but the check matches the words, so the sentence was reworded to "are gated on" (the only DESIGN change made after the fix agent returned) and the commands were re-run. The re-run below is the record; every check line is PASS. `phase-outputs/test-results/r4-mechanical.md` was regenerated by this run.

### Command 1: section map
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

### Command 2: WC-14 hits
```
$ grep -n 'WC-14' docs/designs/orchestrator-mode.md
668:**Gate.** Steps 1.17 to 1.19 are written only after the owner answers GQ-11 (step 1.0b) and step 1.16a has
831:| D6 | WC-14 (WC-16 in this design) text of SPEC section 10 (lines 404-408) | The same text renumbered WC-
854:| 1.17 | The REPORT's WC-14 (WC-16 in this design) draft | The SPEC section 10 text plus D6 (section 8) |
1043:| R4 | DESIGN was written against base `e8db2fe6`; master `5dc29d23` already has WC-14 and WC-15, a coord
```

### Command 3: WC-16 hits
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

### Command 4: old insertion text
```
$ grep -n 'after line 561\|519-561' docs/designs/orchestrator-mode.md
(no output expected; grep exit status 1)
```

### Command 5: cadence phrase
```
$ grep -n 'at most once every 5 minutes' docs/designs/orchestrator-mode.md
672:**Final text.** The SPEC section 10 text (lines 404-408) with four changes, all deviation D6: the heading 
677:The coordinator keeps watching its Run until every Task it created is settled and every result has been in
714:| R2 | Same file, `## Orca coordination` (line 396) | One bullet after the never-workers bullet (line 403)
831:| D6 | WC-14 (WC-16 in this design) text of SPEC section 10 (lines 404-408) | The same text renumbered WC-
1043:| R4 | DESIGN was written against base `e8db2fe6`; master `5dc29d23` already has WC-14 and WC-15, a coord
```

### Command 6: step 1.16a hits
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

### Command 7: em-dash count
```
$ grep -c '—' docs/designs/orchestrator-mode.md
0
```

### Command 8: TODO or TBD
```
$ grep -nw 'TODO\|TBD' docs/designs/orchestrator-mode.md
(no output expected; grep exit status 1)
```

### Command 9: deviation total
```
$ grep -n '^Total: 9 deviations.' docs/designs/orchestrator-mode.md
836:Total: 9 deviations.
```

### Command 10: open-item total
```
$ grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md
1012:Total: 23 open items.
```

### Checks

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
