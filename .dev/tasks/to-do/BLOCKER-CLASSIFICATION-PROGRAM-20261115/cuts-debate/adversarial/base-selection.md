# Base Selection: cuts debate (Step 3, hybrid scoring, 2026-11-16)

Judge: scoring judge for /sc:adversarial, depth quick (one debate round). Read-only on all other files. Variants: V1 = opus architect, V2 = sonnet analyzer, V3 = haiku qa. Inputs: `../source.md`, the three variants, `diff-analysis.md`, `debate-transcript.md`, `debate/round1-advocate-*.md`. Spot-checked on disk: `tests/skills/test_review_severity_rule.py:178-205`, `refs/qa.md:198-227`, `ledger.py:104-115`, `card_convert.py:84-87`, `OPEN-QUESTIONS.md:60-115`, stage 2 plan Task 3 (line 72-78), stage 4 plan lines 40-45. All resolved as the variants cite them.

## 1. Quantitative Scoring

Formula: quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC. Counts are my estimates; the method is stated so it can be redone.

| Metric | V1 | V2 | V3 |
|---|---|---|---|
| RC: items addressed with verdict and evidence, out of 19 (C1 to C14 plus X-001 to X-005). Half credit when the verdict has no concrete target or the evidence does not bear on it | 18.5 (X-005: quorum kept as listed, halt risk not examined) = 0.974 | 19 = 1.000 | 18 (C6 and C10 targets vague, half each) = 0.947 |
| IC: 1 minus falsified claims over substantive claims (14 verdict rows + missed items + facts) | 5 falsified of 26: C6 "regrade plus scan protects" (A-002 rejected by all three), C9 "T9 not needed" (stage 0 T9 reconciles rollout, E4), C10 "cut all summaries" (stage 4 entry reads the stage 3 summary, stage 4 plan:42-44), C11 merge (conceded), C13 quorum without halt caveat = 0.808 | 4 of 27: C3 "cut, flag reversal" (withdrawn), C5 and C12 "edit the tuple" (conceded, weakens the pin), C2 plain file and missed-1 tuple edit (half each) = 0.852 | 1.5 of 27: C10 hash binding (conceded, 1), C9 stage 0 discovery check (conceded, 0.5) = 0.944 |
| SR: concrete (file:line, task id, number) over concrete plus vague | 70 of 75 = 0.933 | 72 of 80 = 0.900 (about 7 self-marked UNVERIFIED hedges) | 40 of 65 = 0.615 ("most of", "reduced", "no justified saving yet", generic conditions) |
| DC: references that resolve | 29 of 30 = 0.96 (results.md:60 and OPEN-QUESTIONS:5/14/15 not opened) | 22 of 24 = 0.92 (spec lines 673, 1018 and stage 3 lines 138/154/175/251 not opened; V2 marks them UNVERIFIED) | 19 of 20 = 0.95 (E1, E2, E3, E6, E8 opened; E4, E5, E7 not) |
| SC: sections over the maximum of 5 (evidence, verdict table, missed items, final list, outcome summary) | 5 = 1.00 | 4.5 (facts only a one-line preface) = 0.90 | 4.5 (no outcome total) = 0.90 |
| **quant** | **0.928** | **0.921** | **0.891** |

Arithmetic. V1: 0.2921 + 0.2019 + 0.1400 + 0.1440 + 0.1500. V2: 0.3000 + 0.2130 + 0.1350 + 0.1380 + 0.1350. V3: 0.2842 + 0.2360 + 0.0923 + 0.1425 + 0.1350.

## 2. Qualitative Scoring

30 criteria, 6 dimensions of 5. M = MET, N = NOT MET. Edge-case floor (criteria 26 to 30): every variant meets at least 2, so the floor of 1 holds.

| # | Criterion |
|---|---|
| 1 | Verdict (CUT, KEEP, SHRINK) for every cut C1 to C14 |
| 2 | Risk of each verdict with file evidence |
| 3 | Reward per cut in tasks or files |
| 4 | A "do not cut when" condition for every cut |
| 5 | Final list of cuts, plus cuts or keeps the source missed |
| 6 | States `qa.md:225` scope correctly (not every run) |
| 7 | Treats the ten-file copy test as binding on the MDTM templates and prompts |
| 8 | C3 matches the converged print-only carrier (no sweep, no promote) |
| 9 | C11 and C12 survive the stage 4 entry contract and the pin test |
| 10 | C13 consistent with `ledger.py:107-113` and the owner's no-salvage ruling |
| 11 | Uniform per-cut table |
| 12 | Itemized evidence section apart from verdicts |
| 13 | Final list ordered by reward over risk |
| 14 | Missed cuts and keeps in their own section |
| 15 | Outcome summary with a task or package total |
| 16 | Verdict names a concrete target for all 14 |
| 17 | Rewards quantified with task ids |
| 18 | Unverified items marked |
| 19 | Conditions name checkable evidence, not a behaviour |
| 20 | Table, final list and totals do not contradict each other |
| 21 | Flags or handles the owner-approval reversal on C3 |
| 22 | Safety path kept (scan, consequence rule) |
| 23 | A check against under-blocking survives the cuts |
| 24 | Lists dependency rewiring for cut tasks |
| 25 | Names the existing tests that break (test_c, test_h, other `pragmatic.md` readers) |
| 26 | Atomic S1 to S3 copy into the ten files with `pragmatic.md` |
| 27 | `S5_FILES = S1_S3_FILES[:6]` slice edge |
| 28 | Reverse scan must keep the S1 opening sentence |
| 29 | Plugin twin byte equality (`test_h`) forces the twin edit |
| 30 | Capture failure or silent loss (fail-closed notes, empty list is not "no findings") |

### Pass 1 (order V1, V2, V3), with evidence cites

| # | V1 | V2 | V3 |
|---|---|---|---|
| 1 | M 14 rows with verdicts | M 14 rows | M 14 rows |
| 2 | M F1 to F7 per row | M line refs per risk cell | M E1 to E8 per row |
| 3 | M task ids in reward column | M ids and counts | N "most of", "reduced", no ids |
| 4 | M condition column filled | M filled | M filled |
| 5 | M M1 to M5 plus list | M five missed items | M five consistency checks |
| 6 | M F2 cites qa.md:225, :301 | M C3 row corrects it | M E2 scoped to no-FINAL runs |
| 7 | M F1, C5, C12 | M C4, C5 cite :181-203 | M E1, C5 |
| 8 | M shrink, cut S3 T10 | N cut, flag reversal | M keep carrier, cut sweep |
| 9 | N C11 merge breaks stage 4 entry | N C12 tuple edit weakens pin | M stages kept, pins kept strong |
| 10 | N quorum built, halt risk unexamined | M ledger.py:107-113 halt risk | M integrity kept, no salvage |
| 11 | M | M | M |
| 12 | M F1 to F7 itemized | M "eight facts" preface | M E1 to E8 key |
| 13 | M ordered | M ordered | M ordered |
| 14 | M section 2 | M section 2 | M own section |
| 15 | M 15 tasks, 3 packages | M about 33 of 54 | N "no exact total yet" |
| 16 | M | M | N C6, C10 targets vague |
| 17 | M | M | N no ids |
| 18 | M "Not verified" list | M UNVERIFIED inline | M plans-not-passes caveat |
| 19 | M RT1, OD4, 82 blockers named | M stage 0 T4, RT1 wording | M "pointer names deleted folder" |
| 20 | N rewards sum to 48, 39 removed | M 33 of 54 adds up | M overlap stated |
| 21 | M F3, keeps approval | M flag to owner | M E3:111 kept |
| 22 | M scan kept, S1 consequence | M scan outlives classifier | M no grade lowering |
| 23 | M T4 plus RT1 plus lists | M missed 5, two mechanisms | M discovery checks kept |
| 24 | N no rewiring list | M missed 2 names T6, T7, T8, T9, T14 | M missed 4 |
| 25 | M M3 two other readers | M missed 1, G10 | M missed 2 |
| 26 | M M2 atomic copy | N tuple edit instead | N pins kept, not atomic |
| 27 | N | M line 193 slice | N |
| 28 | M M5 opening must stay | N | N |
| 29 | M F7, M4 | M C5 test_h | M twins kept |
| 30 | N | N | M missed 1 capture failure |
| **Met** | **24** | **25** | **23** |

### Pass 2 (order V3, V2, V1), independent re-read

Verdicts only. Cells that differ from pass 1 are marked with *.

| # | V3 | V2 | V1 |
|---|---|---|---|
| 1 to 11 | M M N M M M M M M M M | M M M M M M M N M M M | M M M M M M M M N N M |
| 12 | M | N* | M |
| 13 to 18 | M M N N N M | M M M M M M | M M M M M M |
| 19 | N* | M | M |
| 20 | M | M | N |
| 21 to 25 | M M M M M | M M M M M | M M M N M |
| 26 to 30 | N N N M M | N M N M N | M N M M N |

Pass 2 totals: V3 22, V2 24, V1 24.

### Final per dimension (after re-evaluating disagreements)

| Dimension | V1 pass 1 | V1 pass 2 | V1 final | V2 pass 1 | V2 pass 2 | V2 final | V3 pass 1 | V3 pass 2 | V3 final |
|---|---|---|---|---|---|---|---|---|---|
| Completeness (1 to 5) | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 4 |
| Correctness (6 to 10) | 3 | 3 | 3 | 3 | 3 | 3 | 5 | 5 | 5 |
| Structure (11 to 15) | 5 | 5 | 5 | 5 | 4 | 4 | 4 | 4 | 4 |
| Clarity (16 to 20) | 4 | 4 | 4 | 5 | 5 | 5 | 3 | 2 | 2 |
| Risk coverage (21 to 25) | 4 | 4 | 4 | 5 | 5 | 5 | 5 | 5 | 5 |
| Invariants and edge cases (26 to 30) | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 2 | 2 |
| **Total of 30** | 24 | 24 | **24** | 25 | 24 | **24** | 23 | 22 | **22** |
| **qual** | | | **0.800** | | | **0.800** | | | **0.733** |

## 3. Position-Bias Mitigation

- Order: pass 1 read V1, V2, V3; pass 2 read V3, V2, V1, scored without looking at pass 1 cells.
- Disagreements found: 2 of 90 cells.
  - V2 criterion 12 (itemized evidence section): pass 1 MET, pass 2 NOT MET. Re-evaluated: V2 gives one preface sentence naming files, not an itemized evidence section. Final NOT MET (verdict changed from pass 1).
  - V3 criterion 19 (conditions name checkable evidence): pass 1 MET, pass 2 NOT MET. Re-evaluated: the source asks for "a named piece of evidence"; V3's conditions for C1, C2, C3, C6 and C7 describe behaviours, not a named file, test or number. Final NOT MET (verdict changed from pass 1).
- No disagreement for V1. First-read order did not move V1 (24 and 24); the two changes both moved a variant down in the pass that read it second.
- Sensitivity: if V2 criterion 12 were MET, V2 qual would be 0.833 and its combined score 0.877, ahead of V1 by 1.3 points. That is still inside the 5 percent band, so the tiebreaker in section 4 would still decide, and it gives V1. The selection does not depend on that one cell.

## 4. Combined Scoring

Combined = 0.5 quant + 0.5 qual.

| Variant | quant | qual | Combined |
|---|---|---|---|
| V1 opus architect | 0.928 | 0.800 | **0.864** |
| V2 sonnet analyzer | 0.921 | 0.800 | **0.861** |
| V3 haiku qa | 0.891 | 0.733 | **0.812** |

- Margin V1 over V2: 0.0035 (0.35 points). Within 5 percent, so the tiebreaker applies. V3 is 5.2 points behind V1 and outside the band.
- Tiebreaker step 1, points won in debate. Scoring matrix of `debate-transcript.md`; a point goes to the variant that first held the final position (shared points split; unanimous points C-001, C-014, X-001, A-002 give no differential):

| Point | V1 | V2 | V3 | Basis |
|---|---|---|---|---|
| C-002/X-003 no new list file | 1.0 | | | V1 M1 |
| C-003 print-only carrier, cut T10 | 1.0 | | 0.5 | V1 shrink with T10 cut; V3 keep carrier, cut sweep |
| C-004 existing copy test, reverse scan, install-path checks | 0.5 | | 0.5 | V1 test and scan (M5); V3 install-path |
| C-005 copy into MDTM templates | 1.0 | | 0.5 | V1 copy; V3 no blanket exemption |
| C-006 cut, keep small planted check | 0.5 | 0.5 | 0.5 | V1 and V2 cut; V3 small check |
| C-007 cut stage 2, keep print, writer, smoke | 0.5 | 0.5 | 0.5 | V1 T3; V2 T4; V3 smoke |
| C-008 RT1 plus five lists | 0.5 | 0.5 | | V2 wording; V1 five lists |
| C-009 stage 0 keep T1, T4, fold T10, T9 errata | 0.7 | 0.3 | | V1 cut set and fold; V2 errata |
| C-010 keep only summaries an entry check reads | | 1.0 | | V2 |
| C-011 keep two packages, atomic copy into stage 3 | 0.5 | 0.25 | 0.25 | V1 atomic copy; V2, V3 keep |
| C-012/X-004 copy all ten files, do not weaken | 0.7 | | 0.3 | V1 M2; V3 pin strength |
| C-013/X-005 quorum only when 2+ launched | | 0.7 | 0.3 | V2; V3 launcher check |
| A-001 mechanical check plus one review | 0.3 | 0.7 | | V2 |
| A-004 notes.md also a writer, keep smoke | 0.5 | | 0.5 | V1; V3 |
| A-005 scan is a backstop | 0.5 | 0.5 | | V1; V2 |
| **Total** | **8.2** | **4.95** | **3.85** | |

- Step 1 decides: V1 8.2 against V2 4.95. Steps 2 (correctness criteria: V1 3, V2 3, V3 5) and 3 (input order) are not reached. Tiebreaker status: APPLIED, resolved at step 1.

## 5. Selected Base

**Base: Variant 1 (opus architect).** Combined 0.864 against 0.861 and 0.812; the score gap is inside the noise, and the debate-points tiebreaker (8.2 against 4.95) decides it. V1's own final positions on C2, C3, C5 and C12 are the converged debate outcomes, and V1 is the only variant that found the atomic-copy invariant (M2) that resolves X-002 and X-004.

**Strengths to preserve from V1**
- Verified facts F1 to F7, including the "Not verified" list.
- M2: copy S1 to S3 into `pragmatic.md` and all ten tuple files in one change, checked by `uv run pytest tests/skills/test_review_severity_rule.py`.
- M3: re-pin `tests/skills/test_review_severity_mapping.py:23` and `test_review_prompt_overrides.py:24`.
- M4: plugin twin of `/sc:implement` forced by `test_h`.
- M5: reverse scan targets the old sentence after the opening; the opening must stay (`test_review_severity_rule.py:70`).
- C3 as print-only shrink (print `notes.md` minors, no sweep, no promote, cut stage 3 T10), so no reversal flag is needed.
- C1, C4, C7, C8 verdicts and the M1 "no new list file" position (with V1's own exception: keep one plain file if the owner wants one cross-reviewer list).

**Corrections the merge must apply to V1** (each was falsified in the debate)
- C11: keep two packages; move the atomic copy into stage 3 (V2, V3; V1 conceded).
- C13: require two valid reports only when two or more reviewers launched; keep parsable-finding behaviour and the Q68 run log (V2, `ledger.py:107-113`).
- C6: do not claim regrade plus scan protects planted-defect recall (A-002); pair with RT1 and a small post-switch planted check.
- C9: keep T9 as a short errata note; C10: keep any summary an entry check reads (stage 4 plan:42-44), cut hash and ruling fields.
- Recompute the 15-task, 3-package outcome without double-counting rewards (V1's reward column sums to 48 against 39 removed).

**Strengths of the non-base variants to incorporate**
- From V2: the dependency-rewiring list (stage 3 T6 to the stage 0 T4 ruling; T7, T8, stage 0 T9, stage 3 T14); RT1 worded "any real blocker found in a Medium list", not a rate; keep two under-blocking mechanisms (stage 0 T4 as a lower bound, RT1 plus the owner reading the first five lists); the `S5_FILES = S1_S3_FILES[:6]` slice edge; one mechanical dependency and G10 check plus one reviewer pass on the trimmed plans.
- From V3: capture-failure handling (notes stay fail-closed, a missing list is not "no findings"); installed-path checks kept because source equality does not detect stale installed copies; do not auto-cut the post-fix helper (stage 3 T5) with the ledger tooling; replace changed literals with consequence checks, never delete tests; verify launcher suitability; state that rewards overlap; do not turn proposals into owner answers (C14 stays recommendations pending the owner).
