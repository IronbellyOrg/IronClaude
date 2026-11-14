# Round 1 advocate statement, Variant 1 (analyzer card, reviewer 1)

Notation: TL = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`. DESIGN = `docs/designs/orchestrator-mode.md`. Calibrated verdicts (CAL) outrank card self-scores.

## Position Summary

V1 is the only card that audits the requirement spine (FR-001 to FR-026, NFR-001 to NFR-015, step-1.0a to step-1.29; 76 rows, `rows_audited: 76`, V1 card line 198). It is the right base for coverage and ordering claims. It is the weakest card on depth: it found no HIGH defect, and the calibrator scored it 0.68 (V1 CAL line 223).

Where V1 is right it is checkably right (R1-G3, verified at TL:2509). Where it is wrong, the CAL already says so (R1-G1 item number, R1-G6 "installs nothing"). I do not defend those. I argue that a merge should keep V1's 76-row coverage ledger and R1-G3, and take the HIGH findings (R2-G3, R2-G5, R2-G7) from V2.

## Steelman

### Variant 2 (qa, haiku slot)

V2 audited the text an executor will actually obey, and it found the only defects that stop a correct run. I re-read three of them:

- R2-G3: TL:1258 step (6) orders `echo "${XDG_STATE_HOME...}"` and `ls -la <printed path>`. TL:1260 then says "every command in the file is one of the eight templates or a file read", and the grep "finds only the forbidden-list sentence" that the Action never asks anyone to write. A correct run cannot satisfy the Verification. CAL: HIGH, holds.
- R2-G7: TL:989 Branch 1 fires "if `status` is PENDING or `Chosen:` is empty". 6.1 writes PENDING, and only Branch 2 sets RESOLVED. So Branch 2 is unreachable. CAL: HIGH, holds. The analyst found the same text at TL:1165 and TL:2481.
- R2-G5: TL:1431 makes `ClassifiedRow` carry `row: SessionRow`, while TL:1434 wants each name to appear once. CAL: HIGH, holds.

V2 also has the best calibrated confidence (0.85) and the only confirmation of Tier-1 F3. It also lists `not_checked` and `recommended_action`, which V1 lacks.

### Variant 3 (refactorer, opus slot)

V3 audited the Phase 2 to 6 design-fix edits, which rewrite the spec that the later phases build from. It has the cleanest citations (`citations_failed: 0`, 40 checked) and the smallest self-to-calibrated gap (0.82 to 0.80). Its holding findings are real:

- R3-G4 (MEDIUM, holds): 7.3 and 7.4 ask the owner only for the rule id, not for the revised WC-16 text. This is a real approval-scope gap.
- R3-G6 (holds): 13.6 adds a CHANGELOG bullet beyond R8.
- R3-G3 (holds): the 5.5 greps for `:545` and similar patterns cannot match DESIGN's "(line 545)" form.
- R3-G8 and R3-G9 are the only reuse checks of any card.

## Strengths Claimed

1. **Only full-spine audit (S-001).** V2 audits GQ, D, SP and INF rows (51). V3 audits 24 rows. Neither maps FR-001 to FR-026 or NFR-001 to NFR-015. A merged verdict on "is every requirement delivered" has no other source than V1. All 76 rows carry a verdict and evidence (V1 card lines 14 to 89).
2. **Delivery-versus-lens discipline.** V1 notices when a matrix hit is not a delivery item and re-maps it. FR-002 matched only QA lens 9.10, FR-025 only decision record 7.1, NFR-014 only lens 14.35 (V1 card lines 15, 38, 53). It then names the real delivery items (8.10, 9.1, 10.7; 8.6, 8.9, 13.7; 8.10, 10.3). The analyst accepted this method as shared assumption A-005 (STATED).
3. **R1-G3 is verified and unique (C-006, U-004).** TL:2509 reads: "find the test function in tests/sweep/ or tests/commands/test_sweep_command.py ... A missing or hollow test is BLOCKING." Section 12 sends FR-023 to `tests/skills/test_worker_contract.py` and FR-024 to `tests/recommend/`, `tests/core/` and `tests/commands/test_routing_plugin_parity.py` (DESIGN:777, 778). A literal lens either raises a false BLOCKING (which opens a fix cycle) or skips rows. CAL: MEDIUM, holds yes. It is the only MEDIUM in V1 that holds, and the only one of any card that is not an owner-gate or process-gate point.
4. **Row verdicts match findings.** V1 marks step-1.0a `partial` (card line 55) and files R1-G1 for it. V2's INF-013 `covered` against its own HIGH R2-G8 is a contradiction the CAL names (X-007). V1 has no such mismatch.
5. **Ordering evidence (C-011).** R1-G5 checked both SPEC tables and found that 8.1, 8.4, 8.12, 9.1 and 9.3 add gates, each with a stated reason. CAL: holds, LOW. V3's matching ordering claim (R3-G10) rests on a belief about 6.2 that X-001 refutes. V1's ordering claim does not.
6. **Severity restraint (X-008).** V1 self-rated 0 HIGH and 2 MEDIUM, and calibration moved one finding down. V2 self-rated 7 HIGH and calibration cut 4 of them. A merge that trusts V1's severities needs less correction.

## Weaknesses Identified (in the other variants)

**V2**
- **Severity inflation.** `findings_high: 7` against 3 calibrated HIGH. G2 is typed `gate-bypass`, yet the CAL says "an executor following the text still waits for the person, so the gate is not bypassed" (V2 CAL lines 236 to 239). G1 and G8 are the same kind of overstatement.
- **R2-G1 rests on an absence claim.** The CAL caveat says absence "was not verified"; the analyst's greps (0 hits) removed the caveat but not the MEDIUM cap.
- **R2-G4 is weak.** CAL LOW: the insertion counts match the specified edits on a clean file, and no earlier item edits `.gitignore` or `main.py`. A citation is off by two lines (TL:1635-1636).
- **R2-G9 contradicts the design.** CAL LOW: DESIGN:216 says the NFR-004 import test enforces B2.
- **Internal inconsistency.** INF-013 `covered` and GQ-106 `covered-in-substance` against R2-G8 and R2-G4 (X-007). Grade 2 with a 0.96 self-confidence (card lines 148, 163) is a calibration miss.
- **It never audits the FR, NFR or step spine**, so it cannot say whether the plan delivers each requirement.

**V3**
- **Two of ten findings are not findings.** R3-G9 and R3-G10 are positive confirmations (S-007). The CAL says G9 "should not count as a finding" and G10 is "informational only".
- **R3-G10 is wrong on the owner gate.** It praises "The R5 owner decision HALTs rather than defaulting". TL:989 shows that the HALT never resumes (X-001).
- **R3-G1 is overrated.** The card says MEDIUM; the CAL says "wording ambiguity, not a lost rule" (LOW).
- **False matches left unexplored.** INF-005 and INF-014 are `false-match` with no finding; the CAL criticises this.
- **Narrow base.** 24 rows. Disjoint item lists with V1 on eight row IDs (S-002) mean V3's `covered` for those rows (FR-023 to 5.3, step-1.0a to 2.4) judge design text, not delivery.

## Concessions

1. **I missed the three HIGH defects** (C-001, C-002, C-007). V1 read TL:1258 and noted "worker-list runs before the before-reads, which the item discloses" (card line 55) without testing the Verification at TL:1260 against the Action. That is a depth failure, and no HIGH finding exists in V1.
2. **R1-G1 is overstated.** TL:1265 (7.17) states that for STILL UNVERIFIED items "the DESIGN 'behaviour until closed' applies". DESIGN:971 is open item 3, not item 2, so my recommended condition names the wrong item. The CAL (LOW, partly) is right. What survives: the word `M2` has 0 hits in TL, so no named owner-note step exists.
3. **R1-G6 contains a false clause.** "Installs nothing" is wrong; TL:2488 says `pipx run --spec` builds a wheel and installs runtime dependencies (X-006). The 168-count weakness in 14.5 stands at LOW.
4. **R1-G2 and R1-G4 rest on unproven or already-documented claims.** The registry counts are not demonstrated, and the Phase 13 intro already says R1, R2 and R3 belong together (CAL citations_failed).
5. **X-003: I misdescribed item 2.16** as a "phase 2 edit". TL:347 names it a QA SPEC-fidelity lens. My conclusion (2.16 is not delivery) survives.
6. **S-008: no deviation category.** I used `gap_class` only and the calibrator scored `deviation_classification_clarity` at 0.25. All three cards share the omission, but the penalty is real and V1 carries it.
7. **S-006: four citations failed** in the CAL (G1, G2, G4, G6), against 1 for V2 and 0 for V3. V1's citation grounding is the weakest of the three (0.80).
8. **About 32 of 76 verdicts are `covered-in-substance`** (17 FR, 10 NFR, 5 step). They depend on delegation to DESIGN rows (see A-001). If the delegated row is weak, those verdicts are weak.
9. **X-009: grade 4 is too generous** given three HIGH unsatisfiable or deadlocking checks found by V2.

## Shared Assumption Responses

**A-001 (delegation counts as coverage): QUALIFY.** V1 relies on it for about 32 of 76 verdicts. It is sound only when the delegated DESIGN row survives the Phase 2 to 6 edits unchanged in substance. A-004 is STATED (8.3 Context says "as revised by Phases 2 to 6"), so items read the revised DESIGN. V3's R3-G1 shows the wording risk for FR-010, but its CAL downgrades that to ambiguity. Accept delegation per row, on the condition that the executor reads the revised row, not the original.

**A-002 (judge checks as written, literal execution): QUALIFY.** Literal reading is correct for pass or fail of a Verification (R2-G3 and R2-G5 cannot pass literally, and that is the defect). It is wrong for severity when the text supplies a fallback: the CAL downgraded R2-G2 (executor still waits), R2-G8 (false assurance only), R3-G2 ("an executor can avoid the error") and R1-G1 (inherited behaviour). So: literal for "can this check pass", recovery-aware for "how bad is it". The three HIGH findings survive both readings, because no recovery exists inside the text.

**A-007 (master anchors stay stable until execution): QUALIFY.** No card states it, but the tasklist partly guards it. TL:2508 reads `artifacts/base-commit.txt` and `artifacts/design-base.md`, so drift against the base is detectable, and V3 verified the pins (test_worker_contract.py:25, 155-173, 382-391; WORKER-CONTRACT.md:110). R3-G3 shows grep patterns can be wrong, but that is a pattern error, not anchor drift. Treat the assumption as low risk with a cheap guard, and accept it as long as the executor re-checks the base commit before Phase 13.

## Per-Point Positions

| ID | Superior | Reason |
|---|---|---|
| S-001 | V1 | Only card on the FR, NFR and step spine (76 rows); V2 and V3 cover GQ, D, SP, INF and the R rows. |
| S-002 | tie | Disjoint item lists reflect different scopes (execution items versus design-fix items); neither is wrong, and the V3 rows judge DESIGN text, not delivery. |
| S-003 | V2 | Line ranges (`:1784-1788`) are the most checkable; V1 full paths are next, V3's `TL:` shorthand is least portable. |
| S-004 | V3 | Smallest self-to-calibrated gap and one downgrade; V1 close behind; V2 had 4 HIGH cuts. |
| S-005 | V2 | Only card with `recommended_action` and `not_checked`; V1 has rationale only. |
| S-006 | V3 | 40 citations, 0 failed; V1 had 4 failed. |
| S-007 | V2 | No confirmation filed as a finding; V1 has one (G5), V3 has two (G9, G10). |
| S-008 | tie | All three omit the four-way deviation category; only one calibrator penalised it, so the scores are not comparable. |
| S-009 | V2 | Touches F1, F2, F3 and F7 by name; V1 touches F4, F6, F8. |
| C-001 | V2 | R2-G3 verified at TL:1258 and TL:1260 (echo and ls against "eight templates or a file read"). V1 and V3 missed it. |
| C-002 | V2 | R2-G7 (unreachable Branch 2) beats V1's missing branch (CAL LOW) and V3's wrong question (MEDIUM). TL:989 confirms the deadlock. |
| C-003 | tie | V1 `covered` and V3 G1 (ambiguity, LOW) are both defensible; the CAL reading sits between them. |
| C-004 | tie | V1 G2 (ID labels, LOW partly) and V2 G9 (matrix row, LOW partly) address different things, and neither is demonstrated in full. |
| C-005 | V2 | Only card to find the missing GQ-111 to GQ-113 rule; analyst greps verified absence (0 hits); MEDIUM. |
| C-006 | V1 | R1-G3 verified at TL:2509; CAL MEDIUM yes; V2 and V3 did not find it. |
| C-007 | V2 | R2-G5 (8.3 `grep -c` against `row: SessionRow`) is HIGH and holds. V3's G3 is LOW. |
| C-008 | V2 | G8 (MEDIUM) finds an unproven guard; V1 says `covered`, V3 G7 is only a design preference. |
| C-009 | V2 | G10 (missing SP-28 deliverable, MEDIUM) outranks V1 G6 (LOW, contains a false clause). |
| C-010 | tie | All three agree no commits are made; CAL for G4 says the plan already documents the grouping. |
| C-011 | V1 | R1-G5 is an accurate ordering check with stated reasons; V3's G10 includes a refuted owner-gate claim. |
| C-012 | tie | V1 describes the current SPEC row; V3 describes the planned phase 5 edit; consistent at pre-execution (analyst). |
| C-013 | V3 | R3-G6 holds (TL:2293 versus R8 scope). |
| C-014 | V3 | Only card with reuse checks (G8, G9); both LOW. |
| C-015 | tie | V1 re-maps four false matches, V2 turns one into a finding; V3 records and stops (weakest). V1 and V2 are comparable. |
| X-001 | V2 | TL:989 confirms Branch 1 fires on PENDING; V3's "HALTs rather than defaulting" praises a gate that never resumes. |
| X-002 | tie | Calibrated reading is wording ambiguity (LOW): neither "fully covered" nor "rule lost". |
| X-003 | V3 | TL:347 names 2.16 a SPEC-fidelity lens; V1 misdescribed it (conclusion survives). |
| X-004 | V1 | CAL on R2-G9: the design itself says the NFR-004 import test enforces B2 (DESIGN:216), so V1's `covered` stands. The B2 matrix omission is V2's valid residue. |
| X-005 | tie | CAL is right on the item number (3 not 2); V1 is right that `M2` has 0 hits in TL and no explicit HALT exists. |
| X-006 | none (internal to V1; the CAL side wins) | TL:2488 shows `pipx run --spec` installs runtime dependencies, so V1's card text is wrong. |
| X-007 | V1 | V2's own CAL names the INF-013 and GQ-106 mismatches; V1's verdicts and findings agree. |
| X-008 | tie (V1 and V3) | Both stayed near their calibrated severities; V2's `gate-bypass` HIGH is contradicted by its own CAL. |
| X-009 | V2 | Three calibrated HIGH defects make grade 4 (V1, V3) too generous. |
| X-010 | V2 | V2 follows false matches to real delivery items; V3 stops at the false match. |
| X-011 | V1 | The executable subject is the 1.0a capture (7.16 to 7.18); V3 judged the design-text fix (2.4). Neither refutes the other, but V1 chose the item that runs. |
| X-012 | none (internal to V3; the CAL side wins) | The reflect precedent also replaces the whole `_git`, so G7 is a design preference. |
| A-001 | tie | All three share it; qualified as above (delegation holds if the revised DESIGN row is used). |
| A-002 | tie | All three share it; literal for pass or fail, recovery-aware for severity. |
| A-007 | tie | All three share it; partly guarded by `base-commit.txt` and `design-base.md` (TL:2508). |
