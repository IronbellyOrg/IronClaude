# Adversarial Debate Transcript

- Protocol: sc-adversarial-protocol, Mode A, Step 2 (debate-transcript.md Artifact Assembly, T03.07)
- Written by: debate orchestrator (neutral; took no part in the debate)
- Date: 2026-11-08
- Variants: V1 = reviewer 1 card plus blind calibration (analyzer, sonnet slot); V2 = reviewer 2 card plus blind calibration (qa, haiku slot); V3 = reviewer 3 card plus blind calibration (refactorer, opus slot)
- Round files are summarized here, not pasted. Each summary points at its file in `debate/`.

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 and Round 2), plus Round 2.5 invariant probe. No Round 3 at standard depth.
- Convergence achieved: 100% (50 of 50 diff points agreed after Round 2)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3
- Diff points in denominator: 50 (S 10, C 25, X 6, A 9), from `diff-analysis.md` (67 differences in total; the 17 U-NNN unique contributions sit outside the denominator by rule). Alternative denominator with the 8 promoted sub-points: 58.

## Round 1: Advocate Statements

All three advocates wrote in parallel, with a steelman of each other variant, claimed strengths, weaknesses found in the others, concessions, a position on every diff point and a response to every shared assumption.

### Variant 1 Advocate (analyzer, sonnet)
File: `debate/round1-v1.md`

**Position**: V1 is the only card that audited the primary matrix layer (26 FR, 15 NFR and 35 design-step rows, 76 in all) and its MEDIUM findings sit on the live critical path: step 1.0a routing, the HALT gates and the 7.16 and 7.18 check lines. It does not claim to be best on every axis.

**Steelman of V2**: cleanest evidence (29 citations checked, none failed), the best single finding of the run (R2-G1, the 8.3 `grep -c` check that rejects a correct models.py), and a recall pass beyond the matrix.

**Steelman of V3**: the only card that read the design as a document the tasklist edits (R3-G5 design line 221, R3-G6 the 6.3 and 6.4 checks, R3-G2 the stale count of 8).

**Key strengths claimed**:
1. Breadth: 76 rows, with step-1.0a marked partial against Tier 1.
2. R1-G1 confirmed on both halves: the cursor outcome conflicts with the ten-template pins (tasklist 1485, 1793) and a CLOSED run-current --json need has no owner route.
3. Unique confirmed findings R1-G2 (HALT pointer to item 6.2), R1-G5 (bare `coder` grep) and R1-G6 (echo and ls against the 7.16 Verification).
4. No HIGH inflation; every remediation ends with a "Check by reading" test.

**Weaknesses identified in V2 and V3**: V2 rated six HIGH and its own bar supports one; R2-G5 and R2-G7 overstate. V3 has 21 of 32 rows tagged [INFERRED] from Tier 1, eight of eleven findings are LOW, and nothing touches step 1.0a.

**Concessions**: R1-G7 refuted and withdrawn; R1-G3 weakened to the strip-rule gap; R1-G2 lower impact; R1-G8 and R1-G9 weakened; 41 of 78 citations failed (second refs on FR and NFR rows); classification clarity 0.60; R2-G1 and V3's R5 findings are better than anything V1 found on those points.

### Variant 2 Advocate (qa, haiku)
File: `debate/round1-v2.md`

**Position**: V2 is strongest where QA must tell a bad product from a bad test. R2-G1 is a deterministic false rejection (tasklist 1436 against 1433, design 454 and 466). The calibrated profile is one HIGH, five MEDIUM and three LOW, not six HIGH.

**Steelman of V1**: execution-path completeness; V1 is stronger than V2 on the CLOSED capture path, and its capture-check findings survive calibration.

**Steelman of V3**: authorized changes still need consistent design text and records; V3's D10 and count findings catch incomplete propagation.

**Key strengths claimed**:
1. R2-G1, the only HIGH that survives calibration.
2. Checks matched to real prohibitions (R2-G4: design 211, 219 B5, 638).
3. Coverage beyond the matrix (R2-G6, design 636 set-union wording).
4. Documentary obligations kept separate from behaviour (R2-G2, R2-G3 at MEDIUM).
5. Auditable evidence: 29 citations checked, 0 failed.

**Weaknesses identified in V1 and V3**: V1's 41 failed second refs and four empty evidence lists; R1-G7 must be dropped. V3's inherited mappings are not an independent audit; parts of R3-G6 and R3-G8 overstate.

**Concessions**: all five HIGH downgrades accepted (R2-G2 to R2-G5 to MEDIUM, R2-G7 to LOW); the unconditional INF-019 covered-in-substance verdict withdrawn for the CLOSED path; R2-G6 and R2-G8 prove traceability gaps, not delivery failures.

### Variant 3 Advocate (refactorer, opus)
File: `debate/round1-v3.md`

**Position**: V3 is the only card that audited the R5 change itself rather than treating it as a finished strength. Design line 221 still says "only after a capture" after item 6.3 adds templates 9 and 10: an authorized expansion with an incomplete record, not scope creep.

**Steelman of V1**: read the plan as a literal executor would and asked whether each check can pass; R1-G1 is the most precise statement of the step 1.0a branch problem.

**Steelman of V2**: found the only defect that blocks correct delivery (R2-G1), states a HIGH bar in words, and its calibration gives calibrated_severity per finding.

**Key strengths claimed**:
1. R3-G5 (C-020, X-006) confirmed, with correct classification as authorized expansion.
2. Record-integrity findings re-read this round (R3-G1, R3-G2, R3-G4, R3-G7).
3. A real gate defect in 6.4 (R3-G6, the 15.1 half).
4. Codegraph-grounded reuse finding R3-G9 (`_git` seam, config.py:64-78).
5. Best classification clarity (0.85), 36 citations checked with 0 failed, and the only calibrated confidence that rose (0.75 to 0.79).

**Weaknesses identified in V1 and V2**: V1 citation reliability (41 of 78 failed) and the R5 record untested; V2 HIGH inflation, over-confidence (0.90 to 0.81), and R5 accepted without audit.

**Concessions**: missed R2-G1; 21 of 32 rows [INFERRED]; R3-G3, R3-G6 (D10 half), R3-G8 and R3-G11 weakened; R3-G7 duplicates R3-G1; R3-G5 at MEDIUM is arguable; no blast-radius reasoning and no HIGH tested against a stated bar.

## Round 2: Rebuttals

Sequential rebuttals in the order V1, V2, V3. Each advocate answered every criticism, updated its view of the others, added re-read evidence and restated a position on every diff point.

### Variant 1 Rebuttal
File: `debate/round2-v1.md`

- Conceded the citation defect but narrowed its reach: all 41 failures are the second ref on FR and NFR rows; each row also names its delivering items, so verdicts stand as "item-checked, second ref unreliable".
- Withdrew R1-G7 fully; withdrew R1-G3 to a LOW wording gap (tasklist 1260 and 1262 already strip timestamps); withdrew R1-G8 (line 163 is accurate); kept R1-G9 only as a LOW fidelity note.
- Conceded it missed R2-G1 and the R5 record thread, and withdrew its "severity discipline" strength.
- New evidence on R1-G1: 8.10 Context (1482) uses the captured cursor field while 8.10 Verification (1485) pins ten; 8.10 has no stop clause; 10.3 (1796) routes a failing test to code; the 7.17 Branch (1267) cannot fire for a cursor. Held MEDIUM, argued silent loss of the cursor template is the likely route.
- Reported a union check of the three row_coverage lists: 152 of 152 matrix ids, no overlap. Note: the Round 2 positions table in this file reuses some point ids with other meanings; `debate/consensus.md` Part 1 reads those rows from the response text (marked with a dagger there).

### Variant 2 Rebuttal
File: `debate/round2-v2.md`

- Restated all five HIGH downgrades; argued the largest confidence drop shows the largest self-correction, not the weakest card (V2 still has the highest calibrated confidence, 0.81).
- Conceded V1's HALT-pointer and capture-check defects, the R5 consistency audit to V3, and C-002, X-001 and X-005 to V1 (INF-019 becomes partial).
- On the cursor branch, conceded V1's MEDIUM over its own HIGH but countered "silent omission": the safety gate (tasklist 1524, 1525, 1588) reads DESIGN and the capture facts and can HALT, though it also pins ten. Neither safe stop nor silent loss is guaranteed.
- Narrowed R2-G7 to at most a LOW fidelity question (tasklist 2471 recounts and orders replacement; 2256 leaves core CLAUDE.md untouched).
- Conceded grade 3 against grade 4 is not defensible on an unstated scale, and that V3 has the clearest descriptive classification.
- Accepted V1's 152 of 152 union as attributed evidence, not independently run.

### Variant 3 Rebuttal
File: `debate/round2-v3.md`

- Conceded the 21 [INFERRED] rows carry less weight, and that V3 missed R2-G1.
- Withdrew the second R3-G5 remedy (adding agent-wait to the capture contradicts tasklist 1259); kept the first (reword design 221 to allow a recorded owner decision); accepted MEDIUM as a record-integrity point with LOW defensible by runtime effect.
- Conceded the D10 half of R3-G6; held the 15.1 half (step (4) deletes the only 15.1 hit at design 873); rejected V1's "cannot pass" as too strong; the fix is one clause written into 15.1.
- Closed R3-G8 as superseded by item 5.4, R3-G3 as accurate wording, and merged R3-G7 into R3-G1.
- Deferred to V1 on C-001, C-002, C-003, C-007, C-008, X-001, X-002 and X-005; judged both "silent omission" (V1) and "safe stop" (V2) as not guaranteed on A-001d.
- Accepted V1's union check with attribution.

## Round 2.5: Invariant Probe

File: `invariant-probe.md` (fault-finder agent, neutral). It probed the emerging consensus in `debate/consensus.md` Part 5 against the tasklist and design text, re-read for the probe, with a sixth category `sufficiency_challenge` that tests whether a recommended fix alone leaves the plan working.

- Total findings: 22. ADDRESSED 13 (HIGH 1, MEDIUM 1, LOW 11). UNADDRESSED 9 (HIGH 2, MEDIUM 4, LOW 3).
- By category: state_variables 5, guard_conditions 5, count_divergence 4, collection_boundaries 3, interaction_effects 2, sufficiency_challenge 3.
- HIGH UNADDRESSED:
  - INV-006 (guard_conditions): item 6.2's Verification expects `grep -n 'OQ-1 (R5) RESOLVED'` to return one hit, but the pattern already matches 3 lines before 6.2 runs (tasklist 991, 993, 2802) and 4 after a correct append. Correct delivery cannot meet the check, the same class as C-012. No card or advocate raised it, so the consensus statement "R2-G1 is the only HIGH of the run" is wrong.
  - INV-021 (sufficiency_challenge): the R1-G1 fix alone (a 7.17 branch to the owner) leaves the plan executable only if the owner declines. If the owner approves an 11th cursor template or `run-current --json`, items 7.3, 11, 12, 15.1, 7.16, 8.10 and 10.3 still hard-code the pre-change state and nothing re-gates a second allowlist edit. The branch must also name the follow-up (a design edit with its own gate, a re-capture, re-pinned counts) or say that approval means re-planning before step 1.2.
- MEDIUM UNADDRESSED: INV-005 (a resumed HALT on T 1142 Branch 2 does not carry the design fix the 7.17 HALT asks for), INV-008 (the 7.16 forbidden-token grep scans the whole notes file, so an honest capture can fail it), INV-015 (a Run with zero Dispatch rows leaves capture items and open items unverified), INV-018 (the R3-G5 and R3-G2 remedies edit section 4, which no 6.3 Output, 6.4 check or R5 gate input covers).
- LOW UNADDRESSED: INV-003, INV-007, INV-010.
- On the two other fixes it traced fully: the R2-G1 fix alone is enough (INV-020, ADDRESSED) and the R3-G6 fix alone is enough (INV-022, ADDRESSED).

## Scoring Matrix

Copied from `debate/consensus.md` Part 2 (per-point scoring after Round 2). Confidence rule there: unanimous 90 to 99, majority 2 of 3 base 70 plus 10 for an explicit concession, split 50; no point at 100. "none" means the advocates agreed no variant is superior, or that the claim is refuted or the premise unsettled. Tasklist (T) and design (D) line numbers are as quoted by the advocates and the diff-analysis evidence.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | none | 90% | The three slices are disjoint by assignment, so slice width measures the brief, not reviewer quality. V1 reports the union is 152 of 152 ids. |
| S-002 | none | 70% | V2's six HIGH lost five to calibration, while V1 and V3 with zero HIGH missed the one real HIGH (C-012): opposite errors. V2 dissents for its calibrated profile. |
| S-003 | V2 | 95% | Every V2 finding has ref and quote pairs. V1 conceded four empty evidence lists and V3 conceded R3-G7's note used as a quote. |
| S-004 | V2 | 95% | V2 has zero failed citations; V1 conceded 41 failed second refs and V3 conceded 21 rows tagged [INFERRED] from T1 mapping. |
| S-005 | V2 | 90% | Highest calibrated confidence (0.81) with 0 of 29 citations failed; sampled grounding, not full verification. |
| S-006 | V2 | 80% | Only V2's calibration gives per-finding calibrated_severity, which the merge needs. |
| S-007 | V3 | 95% | V3's gap_class set separates design fixes, check defects and reuse (clarity 0.85); V1 and V2 moved to V3 in Round 2. |
| S-008 | V3 | 70% | V3 states its grade scale in words; V1 holds the point is cosmetic. |
| S-009 | none | 90% | Model labels and tooling do not decide finding truth. |
| S-010 | none | 80% | V3's count of new findings and V2's audit of the matrix itself are complementary, not a ranking. |
| C-001 | V1 | 95% | 8.10 Context (T 1482) uses the captured cursor field while T 1485 and T 1793 pin ten templates, and the 7.17 Branch (T 1267) cannot fire for a cursor. V2 conceded its HIGH to V1's MEDIUM. |
| C-002 | V1 | 95% | On the CLOSED path a run-current --json need has no 7.17 owner route, and T 1259 forbids the --json probe. |
| C-003 | V1 | 90% | T 1142 sends HALT items to item 6.2, titled "no HALT" (T 989). Impact is lower because T 1142 spells out both Branches. |
| C-004 | none | 80% | T 1260 and T 1262 already strip timestamps; V1 conceded. Only a LOW clarification survives. |
| C-005 | V2 | 80% | Both raised the 7.16 actor gap at LOW; V2's framing as unclear role identity is preferred. |
| C-006 | V2 | 95% | Unique and confirmed: matrix row INF-017 points at T1 F11; the actor finding is F12. |
| C-007 | V1 | 90% | Unique and confirmed: the 7.18 grep at T 1276 searches bare `coder`, and 7.16 expects a forbidden-list sentence the Action never writes. |
| C-008 | V1 | 90% | Action step 6 runs echo and ls (T 1260) while the Verification allows only templates or file reads (T 1262). |
| C-009 | none | 95% | R1-G7 is refuted: 9.3 reads OQ-8 at T 1640 and halts at T 1643. Withdrawn by V1. |
| C-010 | none | 95% | T 163 is accurate or at worst ambiguous; both claimants withdrew. |
| C-011 | none | 90% | T 2471 recounts at the recorded base; T 2256 leaves core CLAUDE.md untouched. A LOW fidelity question on design 939 remains. |
| C-012 | V2 | 98% | T 1436 counts each name with `grep -c` while T 1433 requires fields that repeat class names, so a correct models.py fails. V1 and V3 conceded. |
| C-013 | V2 | 90% | Unique: the design 80 builder rule is not copied into the task; calibrated MEDIUM. |
| C-014 | V2 | 90% | Unique: byte limits not marked "proposed" (design 987, open item 19); calibrated MEDIUM. |
| C-015 | V2 | 90% | Unique: no check for D 211, B5 (D 219) or D 638; missing checks, not proven breaches. |
| C-016 | V2 | 90% | Unique spec-body recall: set-union wording (D 636) has no row or test. MEDIUM traceability. |
| C-017 | V3 | 90% | Unique: D10 row cells and R5 history line in 6.3 omit sections 2.2 and 12 and the SPEC lines; R3-G7 merges into R3-G1. |
| C-018 | V3 | 95% | D 181 and D 196 escape the 6.3 grep, and T 1793 has no zero-argv case for templates 9 and 10. |
| C-019 | V3 | 90% | Both 5.11 draft-name hits are in section 13, not 13 and 14. Verified by V3 only. |
| C-020 | V3 | 90% | D 221 still requires a capture before a new template, and no 6.3 step reaches it. Authorized expansion with an incomplete record. |
| C-021 | V3 | 90% | The 6.4 pass rule (T 1005) needs a 15.1 hit that allows the flag; 6.3 step (4) only removes the D 873 text. |
| C-022 | none | 95% | Item 5.4 already cites SPEC 415 and 583 and forbids other D6 edits; superseded. |
| C-023 | V3 | 90% | Unique but narrowed: only a citation of config.py:64-78 is missing. LOW. |
| C-024 | V3 | 90% | Unique: 9.1 says "five helpers"; design 7.1 lists four plus `_publish`. |
| C-025 | V3 | 90% | Unique, weakened: OQ-16 wording against the 10.3 positive unit case (T 1793). |
| X-001 | V1 | 95% | V2 conceded: its delegation covers only the STILL UNVERIFIED path. |
| X-002 | V1 | 95% | MEDIUM fits a stall or conflicted build rather than shipped wrong code; V2 conceded its HIGH. |
| X-003 | none | 90% | Both mechanisms defeated (T 2471 recount; T 2256 and T 2469 scope); both conceded. |
| X-004 | none | 70% | V2's stated HIGH bar is the right test, but V2 applied it to one of six HIGH; V1 withdrew "severity discipline". |
| X-005 | V1 | 95% | The step-1.0a row is partial because the CLOSED path is unrouted; V2 conceded. |
| X-006 | V3 | 95% | R5 authorizes templates 9 and 10 and D 221 still contradicts them; V1 and V2 conceded the design-text defect. |
| A-001 | V1 | 80% | The captured-cursor conflict is a real MEDIUM gap and V1 named the fix (a 7.17 branch). |
| A-002 | none | 70% | The 7.16 actor point is a LOW clarification; coordinator equivalence unsettled. |
| A-003 | none | 95% | The premise that "Phase 1" excludes the capture is contradicted by T 1257 and T 1258. |
| A-004 | none | 90% | Precondition a contradicted (T 2471); b settled by T 2256 and T 2469; c open. |
| A-005 | V3 | 95% | Owner authorization (OQ-1 RESOLVED) does not edit D 221; only V3 tested this. |
| A-006 | none | 80% | V1 reports a 152 of 152 disjoint union; not re-run by V2 or V3 during the debate. |
| A-007 | none | 90% | Grades 4, 3 and 4 rest on owner decisions and live Orca access; scales differ. |
| A-008 | none | 90% | Each card uses its own gap_class set; binding to the four-category UC-2 taxonomy not shown. |
| A-009 | V2 | 80% | Original severity labels are not comparable; use V2-style calibrated severity and V2's stated bar. |
| A-001c (sub) | none | 70% | The D 973 no-cursor fallback ends once item 5 is CLOSED with a cursor field. |
| A-001d (sub) | none | 70% | A QA path exists (T 1524, T 1525, T 1588) but T 1485 has no stop clause; neither safe stop nor silent omission is guaranteed. |
| A-002a (sub) | none | 70% | Coordinator equivalence is unknown, not shown false. |
| A-004b (sub) | none | 70% | No unscoped primitive edit is demonstrated; not proven for every file. |
| A-004c (sub) | none | 90% | Whether D 939 "every hit justified" covers the 168 pre-existing hits is not settled; LOW either way. |
| A-006a (sub) | none | 70% | The missing-row worry is answered by V1's reported union check. |
| A-007b (sub) | none | 90% | Live Orca access and permission for 7.16 are unestablished. |
| A-008a / A-009a (sub) | none | 90% | No card states the classification or severity rubric it was graded against. |

Winner tally over the 50 primary points (counted from `debate/consensus.md` Part 1):

| Winner | Count | Points |
|--------|-------|--------|
| V1 | 9 | C-001, C-002, C-003, C-007, C-008, X-001, X-002, X-005, A-001 |
| V2 | 12 | S-003, S-004, S-005, S-006, C-005, C-006, C-012, C-013, C-014, C-015, C-016, A-009 |
| V3 | 12 | S-007, S-008, C-017, C-018, C-019, C-020, C-021, C-023, C-024, C-025, X-006, A-005 |
| none | 17 | S-001, S-002, S-009, S-010, C-004, C-009, C-010, C-011, C-022, X-003, X-004, A-002, A-003, A-004, A-006, A-007, A-008 |

Total: 50.

## Convergence Assessment
- Points resolved: 50 of 50 (primary denominator); 58 of 58 with the promoted sub-points
- Alignment: 100% after Round 2 (Round 1: 94%, 47 of 50)
- Threshold: 80%
- Unresolved points: none formally. Agreed by position but still open in substance (they do not lower the score, and the merge must not present them as settled): A-001d, A-004c with C-011, A-002a with C-005, A-007b, A-008a / A-009a, A-006a, the severity of C-020, C-021 and C-003, single-source verification of C-019 and of V1's SOURCES.md extension of C-007, and the S-002 reading of V1's remapped Round 2 cell (`debate/consensus.md` Part 4).
- Sensitivity: read literally, V1's Round 2 S-002 cell makes S-002 a split and alignment 49 of 50 = 98%. Still above threshold.
- Early termination: stable majority at or above threshold for two consecutive rounds (94%, then 100%). No point flipped back, so no oscillation.

### Gate results

| Gate | Rule | Result |
|------|------|--------|
| Diff-point agreement | score at or above threshold | PASS (1.00 against 0.80) |
| Taxonomy coverage (AD-5) | every level L1, L2, L3 has more than 0 points addressed | PASS (L1 9, L2 19, L3 22; sub-points add 3 at L2 and 5 at L3; no forced round) |
| Invariant probe (AD-1) | count(HIGH and UNADDRESSED) == 0 | FAIL (2) |

- Status: BLOCKED_BY_INVARIANTS (agreement at or above threshold and taxonomy covered, but HIGH-severity UNADDRESSED invariants exist)

```
CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-006, INV-021
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

```
WARNING: 4 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-005, INV-008, INV-015, INV-018
These items do not block convergence but should be reviewed.
```

- LOW UNADDRESSED (no action by rule): INV-003, INV-007, INV-010.
- What clears the block, as the probe states it: the merge carries INV-006 as a new HIGH (and drops the claim that R2-G1 is the only HIGH), and the R1-G1 remedy is extended per INV-021 (name the follow-up for an owner approval, or state that approval means re-planning before step 1.2). Either can also be recorded as an accepted risk by the owner. Depth is standard, so no Round 3 is available inside this run; the decision belongs to the caller.
- Note added at Step 3: the orchestrator re-ran the union check of the three row_coverage lists against `coverage-matrix.yaml` (152 matrix ids; union 152; pairwise overlap 0, 0, 0; no id outside the matrix). This independently reproduces the figure behind A-006, A-006a and INV-014. See `base-selection.md`.
