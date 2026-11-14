# Round 1 advocate: Variant 3 (refactorer, opus slot)

Abbreviations: A = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/adversarial/`; V3 = `A/variant-3-original.md`; TL = the tasklist `TASK-RF-sweep-phase1-20261108-072653.md`; R04 = `research/04` of that task; DESIGN = the orchestrator-mode design doc. TL:347, TL:982, TL:989, TL:1156-1168, TL:1952, R04:86-149 and `src/superclaude/core/WORKER-CONTRACT.md:108-111` were read directly by this advocate. Citations marked "per CAL" come from the blind calibration lines in the variant files.

## Position Summary

V3 is the only card that audits the design-fix phases 2 to 6 and the reuse claims against real code, and it is the best-calibrated card: calibrated confidence 0.80 against 0.82 self (delta -0.02), 40 citations checked and 0 failed (V3:153-157). Its unique findings (R3-G1, R3-G3, R3-G4, R3-G5, R3-G6, R3-G8) cover ground the other two cards do not touch, and every one holds at least partly.

V3 is not the strongest card on execution risk. V2 owns all three calibrated HIGH findings (R2-G3, R2-G5, R2-G7), and V3's R3-G10 claim that the R5 owner gate "HALTs" correctly is refuted by TL:989. The merged result should take V2's verification findings as its core, add V3's design-fix and reuse slice as a complement no other card supplies, and keep V1's breadth of FR, NFR and step row verdicts.

## Steelman

### Variant 1 (analyzer)

V1 audits the widest row set, 76 rows covering every FR, NFR and step. It is the only card that checks phase 7 to 14 delivery for every functional requirement, and it refuses to accept coverage-matrix hits that land on QA lenses or decision records, re-mapping each to a real delivery item (its FR-002, FR-025 and NFR-014 rows). Its R1-G3 is a genuine, calibrated MEDIUM defect (holds, per CAL): the 14.11 lens searches only `tests/sweep/` and `tests/commands/test_sweep_command.py` (the same pair named at TL:87 and TL:132), while section 12 routes some FR-023 and FR-024 tests elsewhere, so the lens can raise a false BLOCKING or skip rows. It also gives the most explicit ordering analysis (R1-G5), and each of its recommendations names an item and a text check.

### Variant 2 (qa)

V2 is the strongest card on what matters most before execution: whether the tasklist can be executed as written. Its three calibrated HIGH findings each describe a check or gate that a correct executor cannot pass.

- R2-G7: 6.1 writes `status: PENDING` (TL:982), 6.2 Branch 1 stops on PENDING, and only Branch 2 sets RESOLVED (TL:989), so the gate halts and never resumes. The same Branch 1 text sits in 7.4 (TL:1165).
- R2-G5: 8.3 requires each model name to appear once by `grep -c`, but `ClassifiedRow.row: SessionRow` guarantees a second hit.
- R2-G3: 7.16 requires `echo` and `ls` in the Action and then its Verification accepts only the eight templates or a file read.

V2 also has the highest calibrated confidence (0.85, per CAL), and it is the only card that turns a false matrix match into a real gap (INF-001 into R2-G1, the missing GQ-111 to GQ-113 rule). Its `recommended_action` and `not_checked` fields are the most useful summary block of the three cards.

## Strengths Claimed

1. **Unique coverage of the design-fix phases 2 to 6.** V3 is the only card that maps rows to phase 2 to 6 edits (S-002). Every later phase reads DESIGN "as revised by Phases 2 to 6" (A-004), so without V3 that revised text has no reviewer. R3-G1 is the only finding in any card that tests whether a delegated rule survives those edits (see A-001).
2. **R3-G1 is a real, if LOW, ambiguity.** R04:90 (edit 4) replaces the clause "and that transcript is None with the same note" with a pointer to the R3-B2 rule. R04:148 opens with several scoped Dispatch rows matching one tab-map entry, and only its last sentence ("a transcript with a tab-map entry that fails the window takes these notes") reaches the one-row case. CAL's downgrade to "wording ambiguity, not a lost rule" (V3:162) is fair. V1 marks FR-010 plain `covered` without examining the edit wording at all.
3. **R3-G4 is the only finding on what the owner is asked.** 7.3 offers only "a new rule WC-16" or "amend the unused WC-1", and 7.4's gate is that GQ-11 is RESOLVED as WC-16 (TL:1156-1168). No item puts the revised rule text to the owner, though DESIGN line 5 and open item 20 require owner approval of the text (V3:174, per CAL). CAL holds it at MEDIUM. It is a different mechanism from V2's R2-G7 (wrong question against an unreachable branch), so the two stack rather than overlap (C-002).
4. **R3-G3 is the only check that passes broken work.** The 5.5 grep uses `:545`, `:865`, `:470` and `:398`, which cannot match DESIGN's "(line 545)" form (V3:170, per CAL). V2's HIGH findings are checks that fail correct work; R3-G3 is the opposite failure mode, a vacuous pass, and no other card found it.
5. **R3-G5 is verified.** TL:1952 reads "the coordinator on every wake" with no bound, while master already carries "at most once every 5 minutes" at `src/superclaude/core/WORKER-CONTRACT.md:110`, and items 5.2 and 13.1 carry the bound too (V3:178, per CAL). The planned command doc would contradict WC-16.
6. **Reuse claims checked against source.** R3-G9 reads `src/superclaude/cli/sprint/recovery.py:424-434`, `src/superclaude/cli/swarm/atomic.py:22-38` and `src/superclaude/cli/reflect/config.py:64-78` (V3:110) and confirms that the fresh `_publish` and `_git` seams are justified; CAL confirms each citation (V3:194). R3-G8 checks the contracts exports and `lint-architecture` (V3:190). No other card checks reuse against code (C-014).
7. **Best calibration and grounding.** Smallest self-to-calibrated delta (-0.02, against V1 -0.12 and V2 -0.11), one severity downgrade (R3-G1), and 0 citation failures against V1's 4 and V2's 1 (S-004, S-006). No V3 finding carries a class label that its CAL says is false, unlike V2's `gate-bypass` on R2-G2 (X-008).
8. **Row notes link defects to findings.** Where V3 marks a row covered but has a finding against it, the note says so: D6 "See R3-G4", FR-010 "See R3-G1", R8 "See R3-G6". That avoids the row-against-finding contradiction CAL flags in V2 (INF-013 `covered` against R2-G8 rated HIGH; X-007).

## Weaknesses Identified

**V1.**

- It misses all three execution-blocking defects (R2-G3, R2-G5, R2-G7). Its step-1.0a row reviews 7.16 without testing the 7.16 Verification against its Action, which is where R2-G3 sits.
- It has factual errors. Item 2.16 is "QA r3-b1, agent 9 of 9: rf-qa, SPEC-fidelity domain lens" (TL:347), not "a phase 2 edit" (X-003). Its claim in R1-G6 that pipx "installs nothing" is wrong per its own CAL (X-006). R1-G1 names open item 2 where the design's item is 3 (X-005, per CAL).
- It is the weakest-calibrated card: calibrated confidence 0.68, 4 citation failures, and `deviation_classification_clarity` 0.25 (per CAL).
- FR-010 is marked `covered` from the R3-B1 and R3-B2 fixtures without reading the edit wording (X-002).
- R8 is marked covered (FR-024 and step-1.24b rows) without noticing that 13.6 exceeds the row (C-013).

**V2.**

- Severity inflation: 7 self-rated HIGH, only 3 survive calibration. R2-G2 is labelled `gate-bypass` though CAL says the gate is not bypassed (per CAL).
- Row verdicts contradict findings: INF-013 `covered` against R2-G8 HIGH, and GQ-106 against R2-G4 (X-007).
- R2-G9's claim that the import-only check cannot establish B2 departs from DESIGN:216, which says the NFR-004 import test enforces B2 (X-004, per CAL).
- The D6 row is `covered` on a byte-for-byte copy without asking whether the owner approved the text being copied, which is R3-G4's point.
- Its self-scores (citation grounding 1.00, overall 0.96) are the least honest self-assessment of the three.

## Concessions

1. **R3-G10 is wrong on the R5 gate.** I claimed "R5 is held for the owner: 6.2 requires the owner's words, and option (a) HALTs" (V3:117) and listed "The R5 owner decision HALTs rather than defaulting" as a strength (V3:125). TL:989 shows Branch 1 fires on `status` PENDING and 6.1 writes PENDING (TL:982), so Branch 2 is unreachable. V2's R2-G7 is right: the gate halts but never resumes. The same text in 7.4 (TL:1165) means my R3-G4 sits on top of a gate that deadlocks before the question I criticised is ever answered.
2. **Grade 4 was too generous** (V3:121). With three calibrated HIGH execution blockers, V2's grade 2 is better supported (X-009).
3. **R3-G9 and R3-G10 should not count as findings.** CAL is right that they are confirmations with "no change needed" (V3:194, V3:198); they inflate my finding count.
4. **R3-G1 is LOW, not MEDIUM.** R04:148's last sentence reaches the one-row case; this is ambiguity, not a lost rule.
5. **R3-G7 misdescribed the precedent.** The reflect conftest also replaces the whole `_git` (V3:186); the point is a test-design preference, and its `missing-reuse` class is wrong.
6. **R3-G4's substance risk is small.** The 5-minute bound is already on master at `WORKER-CONTRACT.md:110`, so the gap is in the gate, not in the rule text.
7. **False matches were recorded but not followed.** INF-005 and INF-014 stop at `false-match` with no finding (V3:149), while V2 found the real delivery (X-010).
8. **V3 misses** V1's R1-G3 (14.11 lens folders), V2's R2-G1 (GQ-111 to GQ-113) and all three V2 HIGH findings.
9. **No deviation category.** V3, like the others, gives only `gap_class` and never applies Aligned, Refinement, Drift or Regression (S-008).
10. **No rationale, `recommended_action` or `not_checked` fields.** V2's summary block is better (S-005).

## Shared Assumption Responses

- **A-001 (delegated rows count as covered): QUALIFY.** Delegation to a complete DESIGN row is real coverage only when that row's text survives the phase 2 to 6 edits. That precondition has to be tested per row, not assumed. R3-G1 shows it can weaken: R04:90 removes a clause from the very row FR-010 delegates to. The merge should accept delegation only for rows that phases 2 to 6 do not edit, or where the edited text was read.
- **A-002 (checks judged as written, literal execution): ACCEPT.** A pre-execution review must judge the text an executor will follow; a reviewer cannot assume the executor repairs broken checks. All three HIGH findings and V3's R3-G3 depend on this standard. The CAL note on R3-G2 that "an executor can avoid the error" (V3:166) is a severity argument, not a rejection of the standard, and it fits a LOW rating.
- **A-007 (master anchors stable until execution): QUALIFY.** V3 verified the anchors on master (`tests/skills/test_worker_contract.py:25` and `155-173`, confirmed at V3:198; `WORKER-CONTRACT.md:110`, re-read this round). The tasklist mitigates drift by re-anchoring phases 2 to 6 by heading (CAL confirms 5.2, 5.5 and 6.4). The assumption holds at the current master but is not guaranteed later, and R3-G3 shows that line-number pins are the weak form. The merge should prefer heading anchors plus a pre-flight re-check of the master SHA.

## Per-Point Positions

| ID | Superior | Reason |
|---|---|---|
| S-001 | V1 | Widest audit (76 rows); V3's 24 rows are the narrowest, even if complementary. |
| S-002 | V3 | Only card mapping rows to the phase 2 to 6 design-fix items; without it those phases are unaudited. |
| S-003 | V2 | Full paths with line ranges are the most precise; CAL notes two V3 cites point at item headings (V3:148). |
| S-004 | V3 | Smallest self-to-calibrated drift (delta -0.02, one downgrade). |
| S-005 | V2 | Only card with `recommended_action` and `not_checked`. |
| S-006 | V3 | 40 citations checked, 0 failed; V1 failed 4, V2 failed 1. |
| S-007 | V2 | Every V2 finding asks for a change; V3 filed two confirmations as findings. |
| S-008 | tie | All three omit the four deviation categories. |
| S-009 | V2 | Confirms or refines more Tier-1 findings, including the execution defects; V3 touches only F5 and F9. |
| C-001 | V2 | R2-G3 holds at HIGH; V1 and V3 missed it. |
| C-002 | V2 | R2-G7 deadlock is the root defect; V3's R3-G4 is a valid second mechanism to merge alongside it. |
| C-003 | V3 | Only card that read the edit wording; the LOW ambiguity is real and V1's plain `covered` did not check it. |
| C-004 | V1 | R1-G2 raises an ID-label gap V3 does not; both it and V2's G9 are LOW. |
| C-005 | V2 | R2-G1 holds (LOW to MEDIUM); unique to V2. |
| C-006 | V1 | R1-G3 holds at MEDIUM; unique to V1. |
| C-007 | V2 | R2-G5 holds at HIGH; V3's R3-G3 adds the vacuous-pass case and should be merged too. |
| C-008 | V2 | R2-G8 calibrated MEDIUM against V3's LOW, partly-holding R3-G7. |
| C-009 | V2 | R2-G10 rated MEDIUM; V1's R1-G6 carries a factual error (X-006). |
| C-010 | V1 | Only card asking for the handoff line; LOW. |
| C-011 | tie | V1 and V3 both confirm the ordering with no defect. |
| C-012 | V3 | R3-G5 holds: TL:1952 lacks the bound that `WORKER-CONTRACT.md:110` carries. |
| C-013 | V3 | R3-G6 holds; V1 marked R8 covered without noticing the extra bullet. |
| C-014 | V3 | Only card that checked reuse against source files (R3-G9, R3-G8). |
| C-015 | V2 | Turns the INF-001 false match into a finding; V3 records false matches and stops. |
| X-001 | V2 | TL:982 and TL:989 confirm the deadlock; V3 concedes R3-G10 on this point. |
| X-002 | V3 | The calibrated V3 reading (LOW ambiguity, R04:148) beats V1's unexamined `covered`. |
| X-003 | V3 | TL:347 names 2.16 a SPEC-fidelity QA lens, as V3 said. |
| X-004 | V1 | DESIGN:216 says the NFR-004 import test enforces B2; V2's insufficiency claim departs from the design. |
| X-005 | V1 | The calibrated V1 position stands: no explicit HALT exists, though the open item is 3, not 2. |
| X-006 | V1 | V1's own CAL corrects its card on what pipx run installs. |
| X-007 | V3 | V3's covered-with-defect rows link their finding ids; V2's INF-013 and GQ-106 do not reconcile. |
| X-008 | V3 | No V3 class or severity is contradicted beyond one downgrade; V2 has four HIGH downgrades and a false `gate-bypass`. |
| X-009 | V2 | Grade 2 fits three calibrated HIGH execution blockers; V3 concedes its grade 4 was generous. |
| X-010 | V2 | Finds the real delivery for the false-match rows; V3 stopped at the false match. |
| X-011 | tie | The cards address different subjects (design edit against capture run); neither refutes the other. |
| X-012 | tie | Internal to V3; the CAL correction of R3-G7 stands and no rival card addresses it. |
| A-001 | V3 | Only card that tested whether a delegated row survives the design edits (R3-G1). |
| A-002 | V2 | Applies literal execution most consistently, and all HIGH findings rest on it. |
| A-007 | V3 | Only card that verified the master anchors and noted heading-based re-anchoring. |
