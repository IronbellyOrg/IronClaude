# Round 2 rebuttal, Variant 3 advocate (refactorer persona, opus slot)

Notation: A = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/adversarial/`. V3 = `A/variant-3-original.md`. TL = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`. R04 = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/04-design-fixes-r3.md`. DA = `A/diff-analysis.md`. Calibrated verdicts (CAL) outrank card self-scores.

V3 is a complement to V2, not a rival. V2 owns the execution blockers. V3 owns the review of the Phase 2 to 6 design edits and the scope of owner approval. This round I widen V2's deadlock finding with new evidence and shrink my own R3-G1 to a one-word fix.

## Response to Criticisms

**From V1, Round 1**

1. *"Two of ten findings are not findings (R3-G9, R3-G10)."* Concede. CAL says G9 "should not count as a finding" (V3:194) and G10 is "informational only" (V3:198). The merge should list them as confirmations. That leaves V3 with 8 findings: 1 MEDIUM (R3-G4) and 7 LOW.
2. *"R3-G10 is wrong on the owner gate."* Concede in full. The error is larger than V1 said. My card wrote "R5 is held for the owner: 6.2 requires the owner's words, and option (a) HALTs" (V3:117) and praised "The R5 owner decision HALTs rather than defaulting" (V3:125). That praise covers half of a gate that never resumes. The same Branch 1 text sits in eight HALT items, not three (New Evidence 1).
3. *"R3-G1 is overrated."* Concede, MEDIUM to LOW. New Evidence 2 finds the one sentence that causes the ambiguity, so the fix shrinks to one word.
4. *"False matches left unexplored (INF-005, INF-014)."* Concede. V3:37-38 records each false match and stops. V2 found the real delivery items (X-010).
5. *"Narrow base (24 rows), and V3's `covered` verdicts for shared row IDs judge design text, not delivery."* Concede both the scope and the subject. My step-1.0a row maps to 2.4 (V3:32, TL:263), which is a DESIGN text edit. It says nothing about whether the 7.16 capture can pass, and R2-G3 sits there. I hold one point only: the design-fix slice needs a reviewer, and V3 is the only card that reviews it.

**From V2, Round 1**

6. *"R3-G10 treats stopping as a complete approval mechanism."* Concede (see point 2).
7. *"V3 sometimes stops at a false matrix match."* Concede (see point 4).
8. *"R3-G7 seam extraction is a preference, and the cited precedent also replaces the whole `_git`."* Concede. CAL (V3:186) is right that `tests/cli/reflect/conftest.py:59-74` replaces the whole function too. The `missing-reuse` class is wrong. This is a test-design preference at LOW and does not justify adding a helper.

**From V1, Round 2**

9. *"V3 marks D6 `covered` with only a pointer. That is the same row-against-finding gap V3 blames on V2, only smaller."* Concede. V3:28 says "the owner never approves it. See R3-G4" under a `covered` verdict. The honest label is `partial`: the 5.3 and 5.4 records build the text, but nothing gets the text approved. The same fix applies the other way to FR-010 (V3:23). Its note says the rule "is lost", which goes beyond what CAL sustains (V3:162). It should read "ambiguous after edit 4, see R3-G1".
10. *"R2-G7 has two missing links."* Agree, and I add a third. First, no step writes the owner's answer into the record. Second, Branch 1 shadows Branch 2. Third, the HALT rule at TL:192 has no resume clause: it sets "Blocked", STOPs and does not tick the item, with no instruction for re-entry. New Evidence 1 shows the scope.
11. *"R2-G5 is wider than one name."* Accept V1's reading. I did not re-read DESIGN:466 this round, so I take the point on V1's citation. It raises my confidence that C-007 belongs to V2.
12. *"R2-G3 is the softest HIGH."* I side with V2's Round 2 answer, not V1. The 7.16 Action requires `echo` and `ls` at TL:1258 step (6). The Verification accepts only "one of the eight templates or a file read" (DA C-001, citing TL:1260). An executor who follows the Action fails the Verification. That conflict is direct and needs no inference.
13. *"The A-007 guard is TL:224, not TL:2508."* Accept. TL:224 is the base-commit check (item 1.3). It records the HEAD sha and, on a mismatch, only adds a note telling the executor to re-check research anchors. It is not a HALT. My A-007 answer below uses it.
14. *"With the concessions, V3 is a complement to V2, not a rival."* Accept. That is my position.

**From V2, Round 2**

15. *"V3's reuse conclusions are not independently re-audited."* Fair. They rest on V3's reads and on CAL, which checked each file (V3:194: `recovery.py:424-433`, `atomic.py:31-32`, `config.py:64-78`). I did not reopen them this round. They are confirmations, so they change no defect count either way.
16. *"The D6 label also needs qualification (X-007)."* Concede (see point 9). I still claim the comparison on X-007. V3's rows name the finding that qualifies them, so a merge can fix them by relabelling. V2's INF-013 row says `covered` and never points to G8.

**Calibration points nobody pressed but the merge should carry**

17. R3-G3 is weaker than my card's wording suggests. CAL (V3:170) says item 5.10 and the 5.5 read-each-line step give partial cover. The four `:545`-style patterns are still dead, so the finding holds at LOW.
18. R3-G8 holds but has "little value" (V3:190), because sweep models do not redefine contracts constants. Keep it as an optional LOW.

## Updated Assessment

**V1 (analyzer).** V1 is still the only card that covers the FR and NFR rows and the step rows across the delivery phases. V1 also found the one real MEDIUM that no other card has: R1-G3, the 14.11 lens's narrow search path (C-006). Its weak points stand. CAL confidence is 0.68. Four citations failed. The "installs nothing" clause in R1-G6 is wrong (X-006), and R1-G1 names open item 2 instead of 3 (X-005). In Round 2, V1 made the best rebuttal of my card (the D6 label). It also made the best addition to V2's gate finding: the HALT rule at TL:192 has no resume clause. V1 is wrong to call R2-G3 soft (point 12). Net: V1 is the coverage backbone of the merge but should not set severity.

**V2 (qa).** V2 owns all three calibrated HIGH findings, and each is a check that cannot pass or a gate that cannot resume (U-001 to U-003). After this round I count the deadlock as the most important finding across all three cards. It is also wider than V2 stated. V2's weak points stand. Four of its seven self-rated HIGHs fall to MEDIUM under CAL (X-008). The INF-013 row contradicts G8 (X-007). Its grade of 2 is not calibrated (X-009). V2's Round 2 concessions on D6 and A-007 were fair. Net: V2 should set the merge's severity and blocker list.

**V3 (refactorer), after concessions.** 8 real findings: R3-G4 MEDIUM, plus R3-G1, G2, G3, G5, G6, G7 and G8 at LOW. G9 and G10 become confirmations. G10's owner-gate clause is withdrawn. V3 is the only card to review the Phase 2 to 6 design edits (S-002) and the only one to catch that the owner approves an id rather than the rule text (R3-G4, U-006). Every V3 citation CAL checked held (40 of 40, V3:156-157). Net: V3 supplies the design-fix and approval-scope slice. Its two row labels need relabelling (D6 to `partial`, and the FR-010 note to "ambiguous").

## New Evidence

**1. The owner-gate deadlock covers eight HALT items plus the shared procedure, not three.**

A grep of TL for "PENDING or" returns 9 lines: 989 (6.2), 1140 (the shared Phase 7 procedure), 1151 (7.2), 1165 (7.4), 1179 (7.6), 1193 (7.8), 1207 (7.10), 1221 (7.12) and 2481 (14.7). Each Branch 1 fires "if `status` is PENDING or `Chosen:` is empty", and only Branch 2 sets `status: RESOLVED`. TL:2481 shows the pattern in full: Branch 1 "if `status` is PENDING or `Chosen:` is empty, apply the HALT rule ... and STOP", and Branch 2 "if `Chosen:` is (A) or (B) with `Decided by:` and `Decision source:` filled, set `status: RESOLVED`". A record created as PENDING can only leave PENDING through Branch 2, and Branch 1 is tested first. So the owner's answer can never be applied as written.

The analysis named 6.2, 7.4 and 14.7 (DA:45, DA:130), and V2 named 6.2, TL:1140 and 14.7. The other five Phase 7 items (7.2, 7.6, 7.8, 7.10, 7.12) were not named by any card or round. TL:988 makes the owner's own words in the session the decision, with "no separate grant file". No step tells the executor to copy those words into `Chosen:`, `Decided by:` and `Decision source:` before the branch test. The HALT rule at TL:192 STOPs without a re-entry instruction. All three combine: the owner answers, nobody writes the answer down, and Branch 1 fires again.

Not affected: 7.15 tests only an empty Run id (DA C-002, citing TL:1242), so it does not deadlock. Its weakness is V2's R2-G2.

Fix, applied once: in the 6.2 text and in the shared procedure at TL:1140, (a) add a step before the branch test that copies the owner's words from the session into the four fields, and (b) change Branch 1 to fire only when `Chosen:` is empty. 7.2 to 7.12 point at the shared procedure. 14.7 needs the same edit plus the "quotes the owner's words" clause it lacks (R2-G2). This stays separate from R3-G4. R3-G4 is about what the 7.3 and 7.4 decision asks: the id only, not the text (7.4 completion gate at TL:1168: "GQ-11 is RESOLVED as WC-16"). Fixing the deadlock lets 7.4 resume, but it still resumes on an id choice alone.

**2. The R3-B1/B2 clause question comes from one scoping word at R04:90.**

Edit 4 at R04:90 drops the transcript clause from the single-row sentence. The replacement text ends with a pointer sentence: "Several matching rows follow the R3-B2 rule below." R3-B2 at R04:148 opens with "Several scoped Dispatch rows can match one tab-map entry". Its no-window branch says the transcript is None with `pane moved to a later session` or `Dispatch time window not observable`. It closes with "A transcript with a tab-map entry that fails the window takes these notes", which is general enough to cover one row. The fixtures at R04:115-117 pin S None for the single-row cases (summary of prior reads; CAL V3:162 confirms).

CAL's reading holds: the rule survives in R3-B2's last sentence, but the R04:90 pointer scopes R3-B2 to "Several". A reader of the single-row sentence is sent nowhere for the transcript. That is wording ambiguity at LOW, not a lost rule. The fix is one word in item 2.2's replacement text: "Several matching rows" becomes "One or more matching rows". This replaces both alternatives in my card's recommendation (V3:47) and answers CAL's actionability note that G1 offered two options (V3:152).

**3. The A-007 guard is real but narrow.**

TL:224 (item 1.3) records `git rev-parse HEAD` and copies DESIGN to `artifacts/design-base.md`. If the sha "does not start with `5dc29d23`", it records the sha and adds a note that "every research anchor must be re-checked against the new base before it is used". It is a note, not a HALT. It covers research anchors, not the master pins in the test files or WORKER-CONTRACT.md:110. HEAD is 5dc29d23 today (session git status), so the pins hold now.

## Per-Point Positions (Round 2)

| Point | Winner | Conf. | One-line reason |
|---|---|---|---|
| S-001 | V1 | 90 | 76 rows across FR, NFR and step IDs is the widest base. V3's 24 is the narrowest (conceded). |
| S-002 | tie | 80 | Changed from V3. Disjoint item lists show the cards judge different subjects. V3 owns the design-fix slice and V1 and V2 own delivery. |
| S-003 | V2 | 75 | Line ranges let a reader verify a span. V3's `TL:` shorthand is compact but points at item headings (V3:148). |
| S-004 | V3 | 85 | Smallest gap between self and calibrated severity (one MEDIUM to LOW) and confidence delta of -0.02. |
| S-005 | V2 | 90 | Only V2 carries `recommended_action` and `not_checked`. V3 has neither. |
| S-006 | V3 | 90 | 40 citations checked and 0 failed, against 4 failed for V1 and 1 for V2. |
| S-007 | V2 | 85 | V2 files no confirmations as findings. V3 filed two (conceded). |
| S-008 | tie | 95 | All three omit the deviation category, and only one calibrator penalised it. |
| S-009 | V2 | 70 | V2 links four distinct T1 findings including F1 and F3. V3 touches F9 twice and gets one of those wrong. |
| C-001 | V2 | 88 | R2-G3 is a direct conflict between the Action (`echo`, `ls`) and the Verification. V1 and V3 miss it. |
| C-002 | V2 | 95 | R2-G7 is the root defect, and New Evidence 1 widens it to eight items. R3-G4 is a separate, smaller MEDIUM. |
| C-003 | V3 | 75 | Only V3 found the dropped clause. CAL rightly cuts it to LOW, and New Evidence 2 gives a one-word fix. |
| C-004 | V1 | 60 | R1-G2 is the clearer traceability gap. V2 G9 is about one matrix row, and V3 has none. |
| C-005 | V2 | 90 | Only V2 caught GQ-111 to GQ-113, and DA verified the 0-hit greps. |
| C-006 | V1 | 95 | Only V1 caught the 14.11 search path, verified at TL:2509 per DA. |
| C-007 | V2 | 95 | R2-G5 makes a correct file fail. R3-G3 is a vacuous pass at LOW. |
| C-008 | V2 | 85 | A missing negative guard test is a real gap. R3-G7 is a preference (conceded). |
| C-009 | V2 | 65 | R2-G10 holds partly at MEDIUM. R1-G6 is LOW and has a wrong clause (X-006). |
| C-010 | V1 | 60 | Only V1 asks for the handoff line. All three agree no commits are made. |
| C-011 | tie | 80 | V1 and V3 both confirm ordering, and neither finds a defect. |
| C-012 | V3 | 80 | R3-G5 is the only concrete defect on the R4 bound. V1 and V3 are consistent at pre-execution (DA:55). |
| C-013 | V3 | 85 | R3-G6 holds (CAL LOW). V1 marks R8 covered without checking scope. |
| C-014 | V3 | 80 | Only V3 audited the reuse precedents. V2's caveat that they were not re-audited lowers this from 90. |
| C-015 | V2 | 85 | V2 turns a false match into a finding. V3 records it and stops (conceded). |
| X-001 | V2 | 98 | TL:989 and the 9-line grep refute R3-G10's owner-gate clause. Conceded in full. |
| X-002 | V3 | 75 | As calibrated: wording ambiguity at LOW, located by New Evidence 2 at R04:90. V1's plain `covered` misses it. |
| X-003 | V3 | 95 | TL:347 shows 2.16 is a QA lens, not an edit (DA:66). |
| X-004 | V1 | 85 | DESIGN:216 asserts the NFR-004 test enforces B2, so V2's claim is a design critique (DA:67). |
| X-005 | V1 | 70 | As calibrated: V1 is right that `M2` has 0 hits, and CAL is right on the item number. |
| X-006 | V1 | 95 | As calibrated: CAL wins inside V1's card, since TL:2488 installs runtime dependencies. |
| X-007 | V3 | 65 | V3's rows point at their qualifying finding, so relabelling fixes them. V2's INF-013 row does not point at G8. D6 still needs relabelling. |
| X-008 | tie | 85 | Internal to V2. CAL outranks, so G1, G2, G6 and G8 drop to MEDIUM. No cross-card winner. |
| X-009 | V2 | 70 | With eight deadlocking HALT items, grade 4 is too generous. V2's grade 2 is closer, though no CAL scores it. |
| X-010 | V2 | 85 | V2 finds the real delivery items, and V3 stops at the false match. |
| X-011 | V1 | 60 | Changed from tie. V1's `partial` judges the capture run that matters. V3's `covered` judges a text edit (conceded). |
| X-012 | V3 | 85 | As calibrated: CAL inside V3's card wins, since the precedent replaces the whole `_git`. |
| A-001 | V3 | 75 | V3 is the only card to test a delegated row against a Phase 2 to 6 edit. The test found real, if LOW, drift. |
| A-002 | V2 | 80 | All three HIGHs rest on literal execution, and V2 argues it best. I move to QUALIFY on severity only. |
| A-007 | V3 | 60 | V3 found a stale anchor pattern (R3-G3). The TL:224 guard is note-only and limited to research anchors. |

## Final positions on shared assumptions

**A-001: QUALIFY.** A row can count as covered by delegation only when the delegated row's text survives the Phase 2 to 6 DESIGN edits unchanged. The edits do change meaning in at least one place: edit 4 removes the single-row transcript clause, and the pointer at R04:90 scopes the rescue rule to "Several" rows (New Evidence 2). The drift is LOW and has a one-word fix, so the assumption mostly holds. The merge should add a rule: any row delegated to text that a Phase 2 to 6 edit touches is `covered-in-substance` until the edited text is re-read, and the FR-010 note is relabelled "ambiguous".

**A-002: QUALIFY (moved from ACCEPT).** Literal reading decides pass or fail. A check that cannot pass as written is a defect, which keeps U-001 to U-003 as findings. Recovery awareness decides severity. A defect the executor will predictably detect and route around (CAL on R3-G2: "an executor can avoid the error", V3:166) is LOW. A defect that stops the run or lets broken work pass silently is HIGH. The owner-gate deadlock fails both tests: it stops the run, and the only way out is for the executor to edit the gate it is meant to obey. It stays HIGH.

**A-007: QUALIFY.** The master pins hold today because HEAD is 5dc29d23. The plan has a guard at TL:224, but it is a note, not a HALT, and covers research anchors only, not the `test_worker_contract.py` pins or WORKER-CONTRACT.md:110. R3-G3 shows a line-anchor pattern can already be dead. The merge should recommend extending the TL:224 note to the master pins and making a sha mismatch a HALT before any phase that greps a line anchor.
