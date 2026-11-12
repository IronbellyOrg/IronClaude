# Round 1 debate: Variant 3 advocate (reviewer 3 card plus calibration)

- Protocol: sc-adversarial-protocol, Round 1
- Variant: 3 (reviewer 3, refactorer persona, opus slot, calibrated by sonnet)
- Advocate model: opus
- Focus: correctness, coverage, deviation-classification
- Inputs read: `variant-1-original.md`, `variant-2-original.md`, `variant-3-original.md`, `diff-analysis.md`
- Evidence re-read by this advocate on 2026-11-08: tasklist lines 996 to 1005 (items 6.3 and 6.4); design lines 181, 196 and 221 (grep); design `agent-wait` hits (lines 66, 532, 738, 873); `reflect/pre-run2/coverage-matrix.yaml` header and row count (152 rows)
- Paths: "tasklist" is `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`; "design" is `docs/designs/orchestrator-mode.md`

## Position summary

Variant 3 is the only card that audits the R5 change itself instead of treating it as a finished strength. Its central claim (R3-G5, C-020, X-006) is that the owner authorized templates 9 and 10, but item 6.3 adds them while leaving design line 221 unchanged ("a new template in `ALLOWED_ORCA` (only after a capture, and never a write verb)"). After Phase 6 the design therefore contradicts itself. That is a design-text inconsistency inside an authorized expansion, not unauthorized scope, and the card says both halves: it raises the gap, and its best-practice line says "No unauthorized scope creep was found". The rest of the card follows the same R5 thread through the record surfaces that Variants 1 and 2 did not open: the D10 row cells (R3-G1), the R5 history line (R3-G7), the stale counts at design lines 181 and 196 that the step (8) grep misses (R3-G2), and the 6.4 pass rule that needs a 15.1 hit which step (4) never writes (R3-G6).

On the calibrator's numbers, Variant 3 has 11 findings with none refuted, 36 citations checked with 0 failed, the best classification clarity of the three cards (0.85), and the only calibrated confidence that rose above its self-report (0.75 to 0.79). Its weakness is depth of risk: no HIGH, no blast-radius reasoning on INV-005, 21 of 32 rows tagged [INFERRED], and it missed the one real HIGH of the run (R2-G1). The merge should take Variant 3 as the authority on the R5 and record-integrity thread, take Variant 2's R2-G1 as the top finding, and take Variant 1's executability findings on Phase 7.

## Steelman

### Variant 1 (analyzer, sonnet slot)

Strongest argument: Variant 1 is the only card that read the plan as a literal executor would and asked, item by item, whether a correct executor can pass each check. That method produced confirmed findings no other card has: R1-G2 (the Phase 7 preamble sends HALT items to item 6.2, which has no HALT), R1-G5 and R1-G6 (the unanchored "coder" grep, the forbidden-list sentence the Action never writes, and echo and ls not allowed by the 7.16 Verification). Its R1-G1 is also the most precise statement of the step 1.0a branch problem: both the cursor-template outcome and the run-current --json outcome lack an owner route, and 8.10 and 10.3 pin exactly ten templates, so a likely capture result breaks two pins. Its 76-row slice (FR, NFR and every design step) is the widest of the three, with calibrator coverage of 0.90.

What it gets right: blast-radius framing on FR-002, FR-026 and NFR-003; no HIGH label where the evidence did not support one; and on X-001 its "no route" reading is correct for the CLOSED path, which is the path a successful capture takes.

### Variant 2 (qa, haiku slot)

Strongest argument: Variant 2 found the only defect in the run that blocks a correct delivery. R2-G1 shows that the 8.3 Verification counts name occurrences with `grep -c` (tasklist line 1436), so a correct models.py fails the check. The calibrator confirmed it at HIGH, and the fix is one line. Variant 2 is also the only card that states a HIGH bar in words ("correct delivery cannot satisfy the check"), and the only card whose calibration supplies `calibrated_severity` for every finding, which is what makes a cross-card severity merge possible. It has the cleanest citations (0.95; 29 checked, 0 failed), and it audits the coverage matrix itself (R2-G6 set-union wording at design 636, R2-G9 INF-017 pointing at F11 instead of F12).

What it gets right: the design-invariant findings (R2-G2 builder rule at design 80, R2-G3 byte limits not marked "proposed", R2-G4 three unchecked invariants) survive at MEDIUM and are real gaps no other card raised. Its calibrated confidence of 0.81, the highest of the three, is earned.

## Strengths claimed

1. **The only card that audits the authorized change instead of accepting it (R3-G5, C-020, X-006).** Design line 221 still reads "a new template in `ALLOWED_ORCA` (only after a capture, and never a write verb)". Item 6.3 (tasklist line 998) adds templates 9 and 10 with no capture and no edit to line 221. Variant 1 calls R5 a strength; Variant 2 rates GQ-109 "covered: authorized change". Neither notices that the design, after Phase 6, breaks its own extension rule. The calibrator confirmed the finding.
2. **Correct deviation classification on that thread.** The card holds both truths at once: the expansion is authorized ("No unauthorized scope creep was found"), and the record is inconsistent (R3-G5). Under the reflect-reviewer taxonomy this is an Authorized expansion with an incomplete record, not Drift. The diff-analysis lists X-006 as a contradiction, but the orchestrator's own reading is that both statements are true; the conflict is between Variant 3 and the design text, not inside Variant 3.
3. **Record-integrity findings grounded in re-read text (R3-G1, R3-G2, R3-G4, R3-G7).** Re-checked for this round: the 6.3 D10 row Section cell reads "7.3, 11, 15.1" and the R5 history list reads "(7.3, 11, 13, 15.1)" (tasklist line 998), while the 6.3 Output names 7.3, 11, 12, 13 and 15.1 (line 999). Design line 181 reads "ALLOWED_ORCA (8)" and line 196 reads "8 read templates", and neither matches the step (8) grep `'eight\|8 templates'`. Design line 873 still says "the eight `ALLOWED_ORCA` templates". These are concrete, cheap fixes that keep the D10 record honest.
4. **A real gate defect in 6.4 (R3-G6, C-021).** The 6.4 pass rule (tasklist line 1005) needs hits in "7.3 (the two `ALLOWED_ORCA` templates), 11, 13 (D10) and 15.1" that allow the flag. Step (4) of 6.3 only deletes text from 15.1, so a literal executor can fail 6.4 after a correct edit. The calibrator kept this half of the finding.
5. **A codegraph-grounded reuse finding (R3-G9).** Only Variant 3 used codegraph, and it found that item 8.5 does not cite the reflect `_git` seam at `src/superclaude/cli/reflect/config.py:64-78` (`-C`, `check=True`, `timeout=10`) or say how the new seam differs. Copying `check=True` without saying so changes error behaviour.
6. **The clearest classification and the best calibration direction.** Classification clarity 0.85 (V1 0.60, V2 0.70); actionability 0.90; 36 citations checked, 0 failed; the only card whose calibrated confidence rose (0.75 to 0.79), meaning it under-claimed rather than over-claimed.
7. **The most new findings against Tier 1.** Seven of eleven findings are new relative to T1 (S-010), against four for V1 and three for V2.

## Weaknesses identified in the others

### Variant 1

- **Citation reliability.** 41 of 78 citations failed (S-004, S-005): the second refs at design lines 444 to 484 look like SPEC line numbers written under the design path. Citation score 0.50. Every row is tagged Grounded, so the tag carries no signal.
- **The R5 record was not tested.** V1 treats R5 as "a recorded owner decision with a pre-flight check" and stops there, so it misses C-017 to C-021, the whole record thread.
- **One refuted and three weakened findings.** R1-G7 is refuted (9.3 reads OQ-8 at 1640 with a HALT at 1643). R1-G3 shrank to the strip rule. R1-G8 and R1-G9 rest on contradicted preconditions (A-003a, A-004a).
- **Classification clarity 0.60.** Its gap_class set does not separate design fixes from check defects.
- **It missed R2-G1**, as Variant 3 did.

### Variant 2

- **HIGH inflation.** Six HIGHs, five cut by calibration (R2-G2, R2-G3, R2-G4 and R2-G5 to MEDIUM; R2-G7 to LOW). By its own stated bar only R2-G1 qualifies (X-004). The card applied its bar to one finding in six.
- **Over-confidence.** Self 0.90, calibrated 0.81, the largest drop of the three cards.
- **R5 accepted without audit.** GQ-109 is rated covered as an authorized change; the design line 221 inconsistency and the D10 record gaps go unseen.
- **The X-001 narrowing is only half right.** R2-G5 says the run-current concern is "covered in substance" by the 7.17 delegation to the behaviour-until-closed rule. That holds only on the STILL UNVERIFIED path. On the CLOSED path there is no route, so the narrowing understates the gap.
- **Grade 3 is harsher than its own calibrated evidence.** After calibration its findings are one HIGH, five MEDIUM and three LOW, close to the profiles that the other two cards graded 4.

## Concessions

1. **Variant 3 missed the only real HIGH (R2-G1, C-012).** A refactorer reading the plan should have caught a `grep -c` check that fails a correct models.py. That is the most important miss on this card.
2. **21 of 32 rows are [INFERRED].** They cite only "T1 matrix row" and were not re-read against the tasklist (S-004, A-006b). Coverage 0.70 is a fair score.
3. **Weakened findings, accepted as weakened.**
   - R3-G3 (line 163): imprecise wording, not false. A-003a is contradicted by tasklist 1257 and 1258, and line 163 itself says step 1.0a uses templates 1 to 8.
   - R3-G6: the D10 half was overstated. Only the 15.1 half stands.
   - R3-G8: the remedy conflicts with item 5.4, which already cites SPEC 415 and 583 and says "change nothing else". The finding should be closed as superseded by 5.4, not fixed.
   - R3-G11: the OQ-16 contradiction is loose, because 10.3 has a positive unit case.
4. **R3-G7 duplicates R3-G1**, and its quote field is a reviewer note, not file text (S-003). It should merge into R3-G1.
5. **R3-G5 at MEDIUM is arguable.** The calibrator says LOW would fit, because Phase 1 never calls templates 9 and 10 (A-005c). I hold MEDIUM only for as long as nothing calls them; see A-005c below.
6. **No blast-radius reasoning on INV-005 lock safety, no execution-order or rollback risks, and few remediations say how to verify them.** These are the calibrator's risk-coverage criticisms (risk 0.70), and they are correct.
7. **No HIGH at all.** On X-004, Variant 3 avoided inflation but did not test any finding against a stated HIGH bar.

## Per-point positions

| id | superior variant or none | one-line reason |
|----|--------------------------|-----------------|
| S-001 | none | The slices are disjoint by assignment, so slice width measures the brief, not the reviewer. |
| S-002 | V3 | Eleven findings with none refuted is the best surviving yield; V2's six HIGHs collapsed to one. |
| S-003 | V2 | Ref and quote lists on every finding with absolute paths; V3's single map and R3-G7 note-as-quote are weaker. |
| S-004 | V2 | Tasklist ranges on every row with one [INFERRED]; V1 has 41 failed refs and V3 has 21 inferred rows. |
| S-005 | V2 | Highest calibrated confidence (0.81, 0 failed), though V3 is the only card that under-claimed. |
| S-006 | V2 | Only V2's calibration gives calibrated_severity, which the merge needs. |
| S-007 | V3 | Its gap_class set separates design fixes, check defects and reuse, and scored 0.85 clarity. |
| S-008 | V3 | A scale written in words is checkable; "0-5" and "5" are not. |
| S-009 | V3 | Only card that used codegraph, which grounds R3-G9. |
| S-010 | V3 | Seven new findings against T1, the most; V2 adds a matrix audit worth keeping. |
| C-001 | V1 | Confirmed at MEDIUM and stated precisely: the ten-template pins break on a likely capture result. |
| C-002 | V1 | Correct on the CLOSED path, where no owner route exists; V2's "covered" holds only on STILL UNVERIFIED. |
| C-003 | V1 | Confirmed and unique; the preamble at 1142 lowers impact but does not repair the pointer to 6.2. |
| C-004 | V1 | The strip-rule half stands, and only V1 raised it. |
| C-005 | V2 | Both raise it at LOW; V2 adds the INF-017 trace and a calibrated severity. |
| C-006 | V2 | Unique matrix-audit finding, confirmed. |
| C-007 | V1 | Confirmed and unique; a literal executor cannot pass the check as written. |
| C-008 | V1 | Confirmed for echo and ls; its second sentence on agent-wait forms is unsupported. |
| C-009 | none | Refuted (9.3 reads OQ-8 at 1640 and HALTs at 1643); carries no weight. |
| C-010 | none | Both V1 and V3 were weakened; the wording is imprecise, not false. |
| C-011 | V1 | LOW is the right severity; V2's HIGH was cut to LOW and A-004a is contradicted. |
| C-012 | V2 | The only HIGH that survived calibration and the most important finding of the run. |
| C-013 | V2 | Unique, real at MEDIUM after calibration. |
| C-014 | V2 | Unique, real at MEDIUM after calibration. |
| C-015 | V2 | Unique, real at MEDIUM; it also shows the T1 F10 fix would not prove B5. |
| C-016 | V2 | Unique spec-body recall finding at MEDIUM. |
| C-017 | V3 | Confirmed: the D10 cells omit NFR-003, NFR-014, SPEC 323 and 510, the eight-to-ten count and sections 2.2 and 12. |
| C-018 | V3 | Confirmed against design 181 and 196, re-read this round. |
| C-019 | V3 | Confirmed: section 14 starts at design 837, so both hits are in 13. |
| C-020 | V3 | Confirmed: design 221 is unchanged while two uncaptured templates are added. |
| C-021 | V3 | The 15.1 half of the 6.4 pass rule defect is confirmed (tasklist 1005). |
| C-022 | V3 (qualified) | Unique, but the remedy conflicts with item 5.4, so close it as superseded. |
| C-023 | V3 | Confirmed, codegraph-grounded reuse gap with a real check=True risk. |
| C-024 | V3 | Confirmed count mismatch against design 7.1. |
| C-025 | V3 (qualified) | Weakened; worth a one-line OQ-16 rewording only. |
| X-001 | V1 (qualified) | No route on the CLOSED path; V2 is right only on the STILL UNVERIFIED path. |
| X-002 | V1 | MEDIUM is supported; V2's HIGH was cut to MEDIUM by its own calibrator. |
| X-003 | V1 | LOW is right; both overstate the mechanism, but V2 overstates the severity too. |
| X-004 | none | V2's stated bar is the right one, but only V2 states it, and it applied it to one HIGH in six. |
| X-005 | V1 (qualified) | The plan is weaker than T1 said on the CLOSED path; V2's narrowing fits only the fallback path. |
| X-006 | V3 | Authorization and the textual breach are both true, and only V3 records both. |
| U-001 | V2 | R2-G1, the top finding of the run. |
| U-002 | V2 | Unique invariant gaps at MEDIUM. |
| U-003 | V2 | Unique recall finding at MEDIUM. |
| U-004 | V2 | Unique builder-rule gap at MEDIUM. |
| U-005 | V2 | Unique byte-limit marking gap at MEDIUM. |
| U-006 | V2 | Unique matrix trace fix at LOW. |
| U-007 | V1 | Unique HALT-pointer defect at MEDIUM. |
| U-008 | V1 | Unique literal-executor check defects. |
| U-009 | V1 | Unique strip-rule gap, kept after weakening. |
| U-010 | none | Refuted; no weight. |
| U-011 | V3 | The D10 and R5 history under-reporting, merged as one finding. |
| U-012 | V3 | The design 221 inconsistency, the core of X-006. |
| U-013 | V3 | The 15.1 half of the 6.4 gate defect. |
| U-014 | V3 | Stale counts at design 181 and 196 plus the missing zero-argv pin for templates 9 and 10. |
| U-015 | V3 | The unstated `_git` seam differences. |
| U-016 | V3 | The 9.1 helper count. |
| U-017 | V3 (qualified) | Keep R3-G4 and R3-G11 as wording fixes; close R3-G8 as superseded by 5.4. |

## Shared assumption responses

| id | response | reason |
|----|----------|--------|
| A-001 (a, b) | ACCEPT | Both are STATED and cited (design 552, tasklist 1267, 1485, 1793); the cursor outcome is real and the pins are unconditional. |
| A-001c | ACCEPT | The design 973 fallback is written for the no-cursor case, so once item 5 is CLOSED with a cursor field it no longer applies, which makes C-001 a real gap. |
| A-001d | QUALIFY | A generic QA rule would stop on a failed count, but a QA fix cycle could "fix" the count by dropping a template instead of routing to the owner, so a named branch is still needed. |
| A-002 (a) / A-002a | QUALIFY | The executor may well be the coordinator, but the plan does not say so; one sentence naming the actor closes C-005 cheaply either way. |
| A-002b | ACCEPT | Tasklist 163 already says the capture is never run by a test. |
| A-003a | REJECT | Contradicted by tasklist 1257 and 1258 and by line 163 itself; this is why R3-G3 was rightly weakened. |
| A-004a | REJECT | Contradicted: tasklist 2471 recounts at the recorded base, so unrelated drift on the base cannot fail 14.5. |
| A-004b | QUALIFY | Unchecked: no card confirmed the task leaves `src/superclaude/core/CLAUDE.md` and other unscoped primitives untouched, so X-003's concealment case is possible but unproven. |
| A-004c | QUALIFY | Design 939 reads most naturally as covering new hits; if it also covers the 168 pre-existing hits, 14.5 is a gap, otherwise a Refinement. The owner or the design text must say which. |
| A-005a | ACCEPT | The OQ-1 record is RESOLVED with the owner's words "Allow it, no conditions needed." |
| A-005b | REJECT | An owner decision authorizes the scope but does not edit design 221; the text still requires a capture first, which is the core of R3-G5 and X-006. |
| A-005c | QUALIFY | True only while nothing calls templates 9 and 10; the moment a later phase calls them, the missing parse evidence becomes a live risk, so 10.3 should pin them now. |
| A-006a | QUALIFY | The matrix has exactly 152 row ids and 76 + 44 + 32 = 152, so the union is complete by count, but no card checked the ids against each other, so the merge should run a union check before claiming full coverage. |
| A-006b | QUALIFY | Conceded for Variant 3: the 21 [INFERRED] rows trust the T1 mapping without a re-read, and the merge should spot-check them. |
| A-007a | ACCEPT | Tasklist 1142 requires PENDING decisions to be resolved before the gates that need them. |
| A-007b | QUALIFY | Live Orca access is assumed and never stated; without it 7.16 stalls and so do 7.17, 8.10, 9.1 and 10.3, so the plan needs a stated precondition or a HALT. |
| A-008a | QUALIFY | A UC-1 card audits a plan, not delivered work, so the UC-2 four-category taxonomy is not binding; but R3-G5 maps cleanly to Authorized expansion with an incomplete record, so the merge can still use the taxonomy where it fits. |
| A-009a | REJECT | Severity labels are not comparable across cards (V2's six HIGHs against zero for V1 and V3), so the merge should use calibrated severity, which only V2's calibration gives, and re-grade V1 and V3 weakened findings before merging. |
