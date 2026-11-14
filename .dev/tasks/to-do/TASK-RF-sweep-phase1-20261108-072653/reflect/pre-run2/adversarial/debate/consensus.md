# Consensus: per-point convergence and scoring matrix (after Round 2)

- Protocol: sc-adversarial-protocol, Mode A, Step 2 (Convergence Detection T03.05, Per-Point Scoring Matrix T03.06)
- Written by: debate orchestrator (neutral; takes no position on the audited plan)
- Date: 2026-11-08
- Inputs: `../diff-analysis.md`; `round1-v1.md`, `round1-v2.md`, `round1-v3.md`; `round2-v1.md`, `round2-v2.md`, `round2-v3.md`
- Variants: V1 = reviewer 1 (analyzer, sonnet slot); V2 = reviewer 2 (qa, haiku slot); V3 = reviewer 3 (refactorer, opus slot)
- Threshold: 0.80 (default; no `--convergence` override given)
- Denominator: count(S) + count(C) + count(X) + count(A) = 10 + 25 + 6 + 9 = 50. The A count uses the nine agreement points A-001 to A-009 from diff-analysis. The eight promoted [SHARED-ASSUMPTION] sub-points (A-001c, A-001d, A-002a, A-004b, A-004c, A-006a, A-007b, A-008a / A-009a) are tracked below as sub-points and reported as an alternative denominator of 58. U-NNN points are outside the denominator by rule.

## Reading rules applied

1. Point ids keep their meanings from `diff-analysis.md`. The Round 2 table in `round2-v1.md` reuses some ids with other meanings (V2 and V3 both flagged this). For those rows the V1 Round 2 position is taken from V1's Round 2 response text, not from the table cell. Rows affected are marked with a dagger (†). Where the response text says nothing on the original meaning, the V1 Round 1 position is carried forward.
2. V3's Round 1 statement gives ACCEPT, QUALIFY or REJECT responses for the A ids but no superior-variant column. Those V3 Round 1 positions are derived from the response text and marked (d).
3. "none" is a position: the advocate holds that no variant is superior, or that the claim is refuted or the premise is unsettled. Two or three advocates holding "none" counts as agreement on "none".
4. A qualifier such as "qualified", "narrowed" or "calibrated" does not change the winner; it is carried into the evidence summary.
5. Confidence: unanimous 90 to 99; majority 2 of 3 base 70, plus 10 when the dissenting or losing advocate made an explicit concession on the point; split 50. No point is set to 100.

## Part 1: Per-point tracking

R1 and R2 cells list the V1 / V2 / V3 positions in that order. "agreed" gives the count of advocates on the winning position in Round 2.

| id | level | R1 v1 / v2 / v3 | R2 v1 / v2 / v3 | agreed | winner |
|----|-------|-----------------|-----------------|--------|--------|
| S-001 | L2 | V1 / none / none | none / none / none | yes (3/3) | none |
| S-002 | L2 | V1+V3 / V2 / V3 | none† / V2 / none | yes (2/3) | none |
| S-003 | L1 | V2 / V2 / V2 | V2 / V2 / V2 | yes (3/3) | V2 |
| S-004 | L2 | V2 / V2 / V2 | V2 / V2 / V2 | yes (3/3) | V2 |
| S-005 | L2 | V2 / V2 / V2 | V2 / V2 / V2 | yes (3/3) | V2 |
| S-006 | L1 | none / V2 / V2 | none / V2 / V2 | yes (2/3) | V2 |
| S-007 | L2 | none / none / V3 | V3 / V3 / V3 | yes (3/3) | V3 |
| S-008 | L1 | none / V3 / V3 | none / V3 / V3 | yes (2/3) | V3 |
| S-009 | L2 | none / none / V3 | none / none / none | yes (3/3) | none |
| S-010 | L2 | none / V2 / V3 | none† / none / none | yes (3/3) | none |
| C-001 | L3 | V1 / V2 / V1 | V1 / V1 / V1 | yes (3/3) | V1 |
| C-002 | L3 | V1 / V1 / V1 | V1 / V1 / V1 | yes (3/3) | V1 |
| C-003 | L3 | V1 / V1 / V1 | V1 / V1 / V1 | yes (3/3) | V1 |
| C-004 | L3 | V1 / V1 / V1 | V1 / none / none | yes (2/3) | none |
| C-005 | L2 | none / V2 / V2 | none / V2 / V2 | yes (2/3) | V2 |
| C-006 | L1 | V2 / V2 / V2 | V2 / V2 / V2 | yes (3/3) | V2 |
| C-007 | L3 | V1 / V1 / V1 | V1 / V1 / V1 | yes (3/3) | V1 |
| C-008 | L3 | V1 / V1 / V1 | V1 / V1 / V1 | yes (3/3) | V1 |
| C-009 | L3 | none (claim withdrawn) / none / none | none† / none / none | yes (3/3) | none |
| C-010 | L1 | V3 / none / none | none / none / none | yes (3/3) | none |
| C-011 | L3 | V1 / V2 / V1 | none / none / none | yes (3/3) | none |
| C-012 | L3 | V2 / V2 / V2 | V2 / V2 / V2 | yes (3/3) | V2 |
| C-013 | L2 | V2 / V2 / V2 | V2 / V2 / V2 | yes (3/3) | V2 |
| C-014 | L2 | V2 / V2 / V2 | V2 / V2 / V2 | yes (3/3) | V2 |
| C-015 | L3 | V2 / V2 / V2 | V2 / V2 / V2 | yes (3/3) | V2 |
| C-016 | L2 | V2 / V2 / V2 | V2 / V2 / V2 | yes (3/3) | V2 |
| C-017 | L2 | V3 / V3 / V3 | V3 / V3 / V3 | yes (3/3) | V3 |
| C-018 | L3 | V3 / V3 / V3 | V3 / V3 / V3 | yes (3/3) | V3 |
| C-019 | L1 | V3 / V3 / V3 | V3 / V3 / V3 | yes (3/3) | V3 |
| C-020 | L3 | V3 / V3 / V3 | V3 / V3 / V3 | yes (3/3) | V3 |
| C-021 | L3 | V3 / V3 / V3 | V3 / V3 / V3 | yes (3/3) | V3 |
| C-022 | L2 | none / V3 / V3 | none / none / none | yes (3/3) | none |
| C-023 | L2 | V3 / V3 / V3 | V3† / V3 / V3 | yes (3/3) | V3 |
| C-024 | L1 | V3 / V3 / V3 | V3 / V3 / V3 | yes (3/3) | V3 |
| C-025 | L1 | V3 / V3 / V3 | V3 / V3 / V3 | yes (3/3) | V3 |
| X-001 | L3 | V1 / V1 / V1 | V1 / V1 / V1 | yes (3/3) | V1 |
| X-002 | L3 | V1 / V1 / V1 | V1 / V1 / V1 | yes (3/3) | V1 |
| X-003 | L3 | V1 / none / V1 | none / none / none | yes (3/3) | none |
| X-004 | L2 | V1+V3 / V2 / none | none / V2 / none | yes (2/3) | none |
| X-005 | L3 | V1 / V1 / V1 | V1 / V1 / V1 | yes (3/3) | V1 |
| X-006 | L3 | V3 / V3 / V3 | V3 / V3 / V3 | yes (3/3) | V3 |
| A-001 | L3 | none / V2 / none (d) | none / V1 / V1 | yes (2/3) | V1 |
| A-002 | L2 | none / V2 / none (d) | none / V2 / none | yes (2/3) | none |
| A-003 | L1 | V3 / none / none (d) | none / none / none | yes (3/3) | none |
| A-004 | L3 | V1 / none / none (d) | none / none / none | yes (3/3) | none |
| A-005 | L3 | V3 / V3 / V3 (d) | V3 / V3 / V3 | yes (3/3) | V3 |
| A-006 | L2 | none / none / none (d) | none / none / V1 | yes (2/3) | none |
| A-007 | L3 | none / none / none (d) | none / none / none | yes (3/3) | none |
| A-008 | L2 | none / none / none (d) | none / none / none | yes (3/3) | none |
| A-009 | L2 | V2 / V2 / V2 (d) | V2 / V2 / none | yes (2/3) | V2 |

Promoted sub-points (outside the primary denominator of 50; included in the alternative denominator of 58):

| id | level | R1 v1 / v2 / v3 | R2 v1 / v2 / v3 | agreed | winner |
|----|-------|-----------------|-----------------|--------|--------|
| A-001c | L3 | none / V2 / none (d) | none / V2 / none | yes (2/3) | none |
| A-001d | L3 | none / none / none (d) | V3 / none / none | yes (2/3) | none |
| A-002a | L2 | none / V2 / none (d) | none / V2 / none | yes (2/3) | none |
| A-004b | L3 | none / none / none (d) | none / none / V1 | yes (2/3) | none |
| A-004c | L3 | none / none / none (d) | none / none / none | yes (3/3) | none |
| A-006a | L2 | none / none / none (d) | none / none / V1 | yes (2/3) | none |
| A-007b | L3 | none / none / none (d) | none / none / none | yes (3/3) | none |
| A-008a / A-009a | L2 | none / none / none (d) | none / none / none | yes (3/3) | none |

Notes on marked cells:

- † S-002: V1's Round 2 table cell says V3 with a reason about classification (that is S-007's topic). V1's response text (section 4 and its X-004 row) withdraws "severity discipline" as a V1 strength because V1 missed the only HIGH, which leaves no variant superior on severity profile. Taken literally, the cell would make S-002 a split (V3 / V2 / none) and drop Round 2 convergence to 49/50 = 0.98.
- † S-010: V1's cell says V3 with a reason about honest [INFERRED] tagging (S-004's topic). V1's response text says nothing on Tier-1 relation coverage, so its Round 1 "none" is carried. A literal reading (V3 / none / none) gives the same winner.
- † C-009: V1's cell reason talks about line 163 (C-010's topic). V1 withdrew R1-G7 in both rounds, so "none" holds either way.
- † C-023: V1's cell reason talks about R3-G8 and item 5.4 (C-022's topic). The winner V3 matches V1's Round 1 position on the `_git` seam.
- C-001 and C-003 in V1's Round 2 table carry reasons about row coverage; the winner (V1) matches V1's response text on the original meaning, so no remapping was needed.

## Part 2: Scoring matrix

Tasklist line numbers (T) and design line numbers (D) are as quoted by the advocates and the diff-analysis orchestrator evidence; this file did not re-read them.

| Diff point | Winner | Confidence | Evidence summary |
|------------|--------|------------|------------------|
| S-001 | none | 90% | The three slices are disjoint by assignment, so slice width measures the brief, not reviewer quality. V1 reports the union is 152 of 152 ids. |
| S-002 | none | 70% | V2's six HIGH lost five to calibration, while V1 and V3 with zero HIGH missed the one real HIGH (C-012): opposite errors. V2 dissents for its calibrated profile; V1's position is read from its response text (see note †). |
| S-003 | V2 | 95% | Every V2 finding has ref and quote pairs. V1 conceded four empty evidence lists and V3 conceded R3-G7's note used as a quote. |
| S-004 | V2 | 95% | V2 has zero failed citations; V1 conceded 41 failed second refs and V3 conceded 21 rows tagged [INFERRED] from T1 mapping. |
| S-005 | V2 | 90% | Highest calibrated confidence (0.81) with 0 of 29 citations failed; V2 itself notes this is sampled grounding, not full verification. |
| S-006 | V2 | 80% | Only V2's calibration gives per-finding calibrated_severity, which the merge needs; V1 holds it is a calibrator output, not card merit, but asked the merge to apply that style to all cards. |
| S-007 | V3 | 95% | V3's gap_class set separates design fixes, check defects and reuse (clarity 0.85); V1 and V2 both moved to V3 in Round 2. No card follows the four-category taxonomy. |
| S-008 | V3 | 70% | V3 states its grade scale in words; V1 holds the point is cosmetic. Low stakes. |
| S-009 | none | 90% | Model labels and tooling do not decide finding truth; V3 withdrew its codegraph credit after C-023 narrowed. |
| S-010 | none | 80% | V3's count of new findings and V2's audit of the matrix itself are complementary, not a ranking. |
| C-001 | V1 | 95% | 8.10 Context (T 1482) uses the captured cursor field while T 1485 and T 1793 pin ten templates, and the 7.17 Branch (T 1267) cannot fire for a cursor; D 552 wants an extra template. V2 conceded its HIGH to V1's MEDIUM. |
| C-002 | V1 | 95% | On the CLOSED path a run-current --json need has no 7.17 owner route, and T 1259 forbids the --json probe; V2 conceded its delegation reading covers only STILL UNVERIFIED. |
| C-003 | V1 | 90% | T 1142 sends HALT items to item 6.2, which is titled "no HALT" (T 989). All three agree impact is lower because T 1142 spells out both Branches itself. |
| C-004 | none | 80% | T 1260 and T 1262 already strip timestamps; V1 conceded. Only a LOW clarification of which fields count as timestamps survives. |
| C-005 | V2 | 80% | V1 and V2 both raised the 7.16 actor gap at LOW; V2's framing as unclear role identity, not an unauthorized capture, is preferred. V1 called the framings equal. |
| C-006 | V2 | 95% | Unique and confirmed: matrix row INF-017 points at T1 F11; the actor finding is F12. |
| C-007 | V1 | 90% | Unique and confirmed: the 7.18 grep at T 1276 searches bare `coder`, and 7.16 expects a forbidden-list sentence the Action never writes. V1's SOURCES.md extension is [INFERRED] and unverified. |
| C-008 | V1 | 90% | Action step 6 runs echo and ls (T 1260) while the Verification allows only templates or file reads (T 1262); V1 withdrew the agent-wait second sentence. |
| C-009 | none | 95% | R1-G7 is refuted: 9.3 reads OQ-8 at T 1640 and halts at T 1643. V1 withdrew it in both rounds. |
| C-010 | none | 95% | T 163 says step 1.0a uses only templates 1 to 8 and "eight called in Phase 1" is accurate or at worst ambiguous; both claimants (V1, V3) withdrew. |
| C-011 | none | 90% | T 2471 recounts at the recorded base and orders replacement of each hit; T 2256 leaves core CLAUDE.md untouched, so neither the drift nor the concealment mechanism holds. A LOW fidelity question on design 939 scope remains (A-004c). |
| C-012 | V2 | 98% | T 1436 counts each name with `grep -c` while T 1433 requires ClassifiedRow fields that repeat SessionRow, Classification and SafeToClose, so a correct models.py fails. Orchestrator-verified; V1 and V3 both conceded they missed it and rank it first. |
| C-013 | V2 | 90% | Unique: the design 80 builder rule is not copied into the task; calibrated MEDIUM, and V2 conceded its HIGH. |
| C-014 | V2 | 90% | Unique: byte limits are not marked "proposed" (design 987, open item 19); calibrated MEDIUM. |
| C-015 | V2 | 90% | Unique: no check for the probes.py import boundary (D 211), B5 no redeclared types (D 219) or renderer bans (D 638); an import-absence grep cannot prove B5. MEDIUM, missing checks rather than proven breaches. |
| C-016 | V2 | 90% | Unique spec-body recall: the set-union session-count wording (D 636) has no row or test; V2 concedes broad delegation may still deliver it. MEDIUM traceability. |
| C-017 | V3 | 90% | Unique: the D10 row cells and R5 history line in 6.3 (T 998, T 999) omit sections 2.2 and 12 and the SPEC lines; R3-G7 merges into R3-G1. |
| C-018 | V3 | 95% | D 181 "ALLOWED_ORCA (8)" and D 196 "8 read templates" escape the 6.3 grep `eight\|8 templates`, and T 1793 has no zero-argv case for templates 9 and 10. Re-verified by V1 and V3. |
| C-019 | V3 | 90% | The 5.11 row puts both draft-name hits in sections 13 and 14; both are in 13 (section 14 starts at D 837). Verified by V3 only; V1 accepted it without re-reading. |
| C-020 | V3 | 90% | D 221 still requires a capture before a new template, and no 6.3 step or grep reaches it (re-verified by V1 and V3). Authorized expansion with an incomplete record, not scope creep; V3 withdrew its second remedy. |
| C-021 | V3 | 90% | The 6.4 pass rule (T 1005) needs a 15.1 hit that allows the flag, and 6.3 step (4) only removes the D 873 text. D10 half conceded; V1 says "cannot pass", V3 says "ambiguous, costs a fix loop via T 1007". |
| C-022 | none | 95% | Item 5.4 already cites SPEC 415 and 583 and forbids other D6 edits; V3 conceded the remedy conflicts, so the point is superseded. |
| C-023 | V3 | 90% | Unique, but V3's own new evidence narrows it: T 1448 already states check=False and GitCallFailed, so only a citation of config.py:64-78 is missing. LOW. |
| C-024 | V3 | 90% | Unique: 9.1 says "five helpers"; design 7.1 lists four plus `_publish`. |
| C-025 | V3 | 90% | Unique, weakened: OQ-16 says no fixture covers templates 9 and 10, but 10.3 has a positive unit case (T 1793). One-line wording fix. |
| X-001 | V1 | 95% | V2 conceded: its delegation to the D 971 rule covers only the STILL UNVERIFIED path; the CLOSED path has no branch. |
| X-002 | V1 | 95% | MEDIUM fits a stall or conflicted build rather than shipped wrong code; V2 conceded its HIGH. |
| X-003 | none | 90% | V1's "fails after any unrelated change" is defeated by the T 2471 base recount and V2's concealment case by T 2256 and the T 2469 scope; both conceded. |
| X-004 | none | 70% | V2's stated HIGH bar is the right test, but V2 applied it to one of six HIGH; V1 withdrew its "severity discipline" claim. V2 dissents for its calibrated profile. |
| X-005 | V1 | 95% | The step-1.0a row is partial (plan weaker than T1 said) because the CLOSED path is unrouted; V2 conceded. |
| X-006 | V3 | 95% | R5 authorizes templates 9 and 10 (V1, V2 right) and D 221 still contradicts them (V3 right); V1 and V2 conceded the design-text defect. |
| A-001 | V1 | 80% | The captured-cursor conflict is a real MEDIUM gap and V1 named the fix (a 7.17 branch). V1 itself recorded "none"; V2 conceded to V1. |
| A-002 | none | 70% | The 7.16 actor point is a LOW clarification; whether the executor is the D 868 coordinator is not settled. V2 holds V2 for its framing. |
| A-003 | none | 95% | The premise that "Phase 1" excludes the capture is contradicted by T 1257 and T 1258; both count complaints are withdrawn. |
| A-004 | none | 90% | Precondition a is contradicted (T 2471 recount); b is settled by T 2256 and T 2469 per V1 and V3; c stays an open design reading. |
| A-005 | V3 | 95% | Owner authorization (OQ-1 RESOLVED) does not edit D 221; only V3 tested this, and V1 and V2 conceded. |
| A-006 | none | 80% | V1 reports a 152 of 152 disjoint union with no missing or extra ids (script deleted, not re-run by V2 or V3); V3 credits V1, V2 accepts with attribution. Per-row reliability still differs. |
| A-007 | none | 90% | Grades 4, 3 and 4 rest on owner decisions before their gates and on live Orca access; V2 conceded its grade 3 is not defensible on an unstated scale. |
| A-008 | none | 90% | Each card uses its own gap_class set; a UC-1 card is not shown to be bound to the four-category UC-2 taxonomy, nor shown exempt. |
| A-009 | V2 | 80% | Original severity labels are not comparable; the merge should use V2-style calibrated severity and V2's stated bar. V3 says "none" but in Round 1 asked for calibrated severity. |
| A-001c (sub) | none | 70% | All three accept that the D 973 no-cursor fallback ends once item 5 is CLOSED with a cursor field, which makes C-001 a real gap; V2 claims the credit. |
| A-001d (sub) | none | 70% | A QA path exists (T 1524, T 1525, T 1588) but T 1485 has no stop clause; neither safe stop nor silent omission is guaranteed. V1 dissents, holding silent omission likely. All agree a named branch is needed. |
| A-002a (sub) | none | 70% | Coordinator equivalence is unknown, not shown false; one sentence naming the actor closes it. |
| A-004b (sub) | none | 70% | V1 and V3 hold T 2256 and T 2469 settle that no unscoped primitive is edited; V2 says this weakens the scenario without proving every file. No swap is demonstrated. |
| A-004c (sub) | none | 90% | Whether D 939 "every hit justified" covers the 168 pre-existing hits is not settled by the task; LOW either way. |
| A-006a (sub) | none | 70% | The missing-row worry is answered by V1's reported union check; it is not independently reproduced. |
| A-007b (sub) | none | 90% | Live Orca access and permission for 7.16 are unestablished; without them 7.17, 8.10, 9.1 and 10.3 stall. |
| A-008a / A-009a (sub) | none | 90% | No card states the classification or severity rubric it was graded against; the uncertainty stays explicit. |

## Part 3: Convergence and taxonomy coverage

### Convergence

| Measure | Round 1 | Round 2 |
|---------|---------|---------|
| Agreed points (primary denominator 50) | 47 | 50 |
| Convergence (primary) | 0.94 | 1.00 |
| Unresolved in that round | S-002, S-010, X-004 (V1 named two winners on S-002 and X-004; S-010 had three different positions) | none |
| Agreed points (alternative denominator 58, with sub-points) | 55 | 58 |
| Convergence (alternative) | 0.95 | 1.00 |

- Threshold 0.80: met in both rounds, under both denominators.
- Sensitivity: if V1's remapped Round 2 S-002 cell is read literally (V3), S-002 becomes a split and Round 2 convergence is 49/50 = 0.98. Still above threshold.
- Winner changes between Round 1 and Round 2 majorities: C-004 (V1 to none), C-011 (V1 to none), C-022 (V3 to none), X-003 (V1 to none), A-001 (none to V1), S-007 (none to V3), and S-002, S-010, X-004 (split to none). Each change follows a concession or new evidence recorded in Round 2. No point flipped back, so no oscillation.
- Early termination condition met: stable majority at or above threshold for two consecutive rounds (0.94, then 1.00), with all taxonomy levels covered. Round 3 is not needed on the diff-point measure.
- Caution on the 1.00 figure: 17 of the 50 agreed points are agreed on "none", 5 of them (S-002, C-004, X-004, A-002, A-006) by a 2 of 3 majority, and several winners carry a narrowed finding. Positional agreement is complete; several premises inside agreed points remain open in substance (listed in Part 4).

### Taxonomy coverage gate

| Level | Points in denominator | Points addressed by all three advocates in Round 2 | Covered |
|-------|-----------------------|----------------------------------------------------|---------|
| L1 surface | 9 (S-003, S-006, S-008, C-006, C-010, C-019, C-024, C-025, A-003) | 9 | yes |
| L2 structural | 19 (S-001, S-002, S-004, S-005, S-007, S-009, S-010, C-005, C-013, C-014, C-016, C-017, C-022, C-023, X-004, A-002, A-006, A-008, A-009) | 19 | yes |
| L3 state mechanics | 22 (C-001, C-002, C-003, C-004, C-007, C-008, C-009, C-011, C-012, C-015, C-018, C-020, C-021, X-001, X-002, X-003, X-005, X-006, A-001, A-004, A-005, A-007) | 22 | yes |

Sub-points add 3 at L2 (A-002a, A-006a, A-008a / A-009a) and 5 at L3 (A-001c, A-001d, A-004b, A-004c, A-007b), all addressed. Gate result: PASS. No forced round is needed.

### Gate status

- Diff-point agreement gate: PASS (1.00 against 0.80).
- Taxonomy coverage gate: PASS (L1, L2 and L3 all covered).
- Invariant-probe gate (AD-1): PENDING. Round 2.5 has not run, so `invariant-probe.md` does not exist yet.
- Status: CONVERGED on the diff-point and taxonomy gates, conditional on Round 2.5 reporting no HIGH-severity UNADDRESSED invariant. If it reports one, the status becomes BLOCKED_BY_INVARIANTS.

## Part 4: Unresolved points

Formally unresolved (agreed = false after Round 2): none.

Agreed by position but still open in substance. These do not lower the convergence score, but the merge must not present them as settled:

1. A-001d: whether a failed ten-template check at 8.10 is caught by QA (V2, V3: a QA path exists at T 1524, T 1525, T 1588) or leads to silent loss of the cursor template (V1: T 1485 has no stop clause, T 1796 routes test failures to code). V1 dissents. All three agree a named 7.17 branch is the fix.
2. A-004c and C-011: whether design 939 "every hit justified" covers the 168 pre-existing hits. No advocate claims to know; LOW either way.
3. A-002a and C-005: whether the executing agent counts as the coordinator named at design 868.
4. A-007b: live Orca access and permission for the 7.16 capture are assumed by every grade and never established.
5. A-008a / A-009a: no card states the classification or severity rubric it was graded against.
6. A-006a: the 152 of 152 union rests on one advocate's report from a script that was deleted; no other advocate re-ran it.
7. Severity within agreed winners: C-020 (MEDIUM per card and calibrator "arguable"; V3 accepts LOW by runtime effect), C-021 (V1 "cannot pass" against V3 "ambiguous, costs a fix loop"), C-003 (calibrated MEDIUM; all three say impact is lower).
8. Single-source verification: C-019 was verified by V3 only; V1's SOURCES.md extension of C-007 is [INFERRED] and unchecked.
9. S-002: agreement depends on reading V1's remapped Round 2 cell from its response text (see note † in Part 1).

## Part 5: Emerging consensus

What the merged verdict should say, finding by finding, as the three advocates left it after Round 2. Severity is the calibrated severity where one exists; a weakened finding without one keeps its card severity unless all three advocates narrowed it. This is the summary the Round 2.5 fault-finder should probe.

### Keep

| Rank | Finding(s) | Diff points | Final severity | Wording basis |
|------|-----------|-------------|----------------|---------------|
| 1 | R2-G1 | C-012, U-001 | HIGH | V2. 8.3 Verification counts name occurrences with `grep -c` (T 1436) while T 1433 requires fields that repeat class names, so a correct models.py fails. Fix: count definitions, not references. The only HIGH of the run; list first. |
| 2 | R1-G1 (absorbs R2-G5's cursor half) | C-001, C-002, X-001, X-002, X-005, A-001, A-001c | MEDIUM | V1, narrowed by V2. Two unrouted step 1.0a outcomes: (a) a captured cursor field conflicts with the ten-template pins (T 1482 against T 1485, T 1793; D 552), and the 7.17 Branch cannot fire for it; (b) a CLOSED run-current --json need has no owner route, while the STILL UNVERIFIED path is covered by delegation to D 971. Fix: a named 7.17 branch sending both to the owner. Do not claim either "safe stop" or "silent omission" is guaranteed (A-001d). Drop the `gate-bypass` label in favour of an unrouted-outcome description. |
| 3 | R2-G2 | C-013, U-004 | MEDIUM | V2. Design 80 builder rule not copied into Key Constraints. |
| 4 | R2-G3 | C-014, U-005 | MEDIUM | V2. Byte limits not marked "proposed"; open item 19 has no closing disposition. |
| 5 | R2-G4 | C-015, U-002 | MEDIUM | V2. Missing checks for D 211, D 219 (B5) and D 638; state them as missing checks, not observed breaches, and note an import-absence grep cannot prove B5. |
| 6 | R2-G6 | C-016, U-003 | MEDIUM | V2. Set-union session-count wording (D 636) is untraced; a traceability gap, since broad delegation may still deliver it. |
| 7 | R3-G1 (R3-G7 merged in) | C-017, U-011 | MEDIUM | V3. D10 row cells and R5 history line under-report the SPEC departure and sections 2.2 and 12. One finding, not two. |
| 8 | R3-G5 | C-020, X-006, A-005, U-012 | MEDIUM, open (LOW defensible) | V3. Classify as an authorized expansion with an incomplete record, not scope creep: R5 authorizes templates 9 and 10, but D 221 still says "only after a capture" and no 6.3 step reaches it. Remedy: reword D 221 to allow a recorded owner decision. V3's second remedy (add agent-wait to the capture) is withdrawn. Severity is open: MEDIUM as a record-integrity point, LOW by runtime effect while nothing calls the templates. |
| 9 | R3-G6 (15.1 half only) | C-021, U-013 | MEDIUM (weakened, scope narrowed) | V3. The 6.4 pass rule (T 1005) needs a 15.1 hit allowing the flag; 6.3 step (4) only removes the D 873 text. Use V3's wording ("ambiguous; costs a fix loop via T 1007"), not V1's "cannot pass". Fix: write the T 1259 sentence into 15.1 in step (4). Drop the D10 half. |
| 10 | R1-G2 | C-003, U-007 | MEDIUM as calibrated, with an impact note | V1. The T 1142 pointer to item 6.2 (T 989, "no HALT") is wrong; impact is lower because T 1142 spells out both Branches. The residual weakness is 7.15 and 14.7 Branch 2 not requiring the owner's quoted words. |
| 11 | R1-G5 | C-007, U-008 | LOW | V1. Bare `coder` grep at T 1276; forbidden-list sentence expected but never written. Leave out the SOURCES.md extension unless a grep confirms it. |
| 12 | R1-G6 (first sentence only) | C-008, U-008 | LOW | V1. echo and ls in Action step 6 (T 1260) against the T 1262 Verification. Drop the agent-wait sentence. |
| 13 | R1-G4 and R2-G8 merged | C-005, A-002, A-002a | LOW | V2 framing. Name the capture actor in 7.16; an actor-identity clarification, not a claim of unauthorized capture. |
| 14 | R2-G9 | C-006, U-006 | LOW | V2. Matrix row INF-017 cites F11; should be F12. |
| 15 | R3-G2 | C-018, U-014 | LOW | V3. D 181 and D 196 keep the count of 8 and escape the 6.3 grep; no zero-argv pin for templates 9 and 10. |
| 16 | R3-G4 | C-019 | LOW | V3. Both 5.11 hits are in section 13. Verified by V3 only. |
| 17 | R3-G9 | C-023, U-015 | LOW | V3, narrowed by V3. Only the citation of config.py:64-78 is missing; T 1448 already states check=False and GitCallFailed. Close to a Refinement. |
| 18 | R3-G10 | C-024, U-016 | LOW | V3. "five helpers" in 9.1 against four plus `_publish` in design 7.1. |
| 19 | R3-G11 | C-025 | LOW | V3. One-line OQ-16 wording fix: 10.3 has a positive unit case. |
| 20 | R1-G3 | C-004, U-009 | LOW clarification only | All three. The strip rule exists (T 1260, T 1262); only the definition of which fields count as timestamps is missing. Do not say "no strip rule". |
| 21 | R1-G9 and R2-G7 merged | C-011, X-003, A-004 | LOW fidelity note, not a defect | Two of three keep a note, V3 would close it. State only that design 939 "every hit justified" may or may not cover the 168 pre-existing hits (A-004c). Drop both mechanisms: base drift (T 2471 recounts) and same-count concealment (T 2256, T 2469). |

### Drop

| Finding(s) | Diff points | Reason |
|-----------|-------------|--------|
| R1-G7 | C-009, U-010 | Refuted by calibration; withdrawn by V1 (9.3 reads OQ-8 at T 1640 and halts at T 1643). |
| R1-G8 and R3-G3 | C-010, A-003 | T 163 is accurate or at worst ambiguous; both claimants withdrew. |
| R3-G8 | C-022 | Superseded by item 5.4, which already cites SPEC 415 and 583 and forbids other D6 edits. |

### Statements about the cards and the review itself

- Coverage: the merge may say the three slices cover 152 of 152 matrix ids with no overlap, attributed to V1's reported union check (not re-run by others). Row verdicts carry different weight: V1 rows are item-checked with unreliable second refs (41 failed); V3's 21 [INFERRED] rows are not independently confirmed.
- Severity: use calibrated severity and V2's stated bar (HIGH means correct delivery cannot satisfy the check). Original labels are not comparable across cards; do not sum or compare raw HIGH counts.
- Classification: no card uses the four-category taxonomy, and no advocate showed a UC-1 card is bound to it or exempt from it. Use descriptive gap classes and map R3-G5 to Authorized expansion where the label fits.
- Grades 4, 3 and 4 should not be ranked against each other; the scales differ and V2 conceded grade 3 is not defensible on an unstated scale.
- Preconditions to state plainly: owner decisions must be resolved before their gates (T 1142), and live Orca access for 7.16 is assumed, not established (A-007b).

### Suggested Round 2.5 probe targets

A-001d (QA catch against silent loss), C-020 and C-021 severity, the unreproduced 152 of 152 union check, C-019 and the SOURCES.md extension of C-007 (single-source or unchecked), and the S-002 reading of V1's remapped cell.
