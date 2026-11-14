# Round 1 advocate statement: Variant 1 (reviewer 1 card plus calibration)

- Protocol: sc-adversarial-protocol, Round 1
- Advocate persona: analyzer (evidence quality, logical consistency)
- Model: sonnet
- Focus: correctness, coverage, deviation-classification
- Evidence re-read for this round: tasklist lines 1140-1142 and 1259-1270 (items 7.15 preamble, 7.16, 7.17), plus the diff-analysis orchestrator evidence for X-001 to X-006.

## Position summary

Variant 1 is the only card that audited the primary matrix layer: all 26 FR rows, all 15 NFR rows and all 35 design steps (76 rows, calibrator coverage score 0.90). Its three MEDIUM findings are the ones that sit on the live critical path of the plan: step 1.0a and the HALT gates around it. After calibration one finding is confirmed at MEDIUM (R1-G1), one is weakened on a sub-point (R1-G2 loses impact, R1-G3 loses the HALT half), and one LOW is refuted (R1-G7). The card makes no HIGH claim and none was needed. I do not claim V1 is the best card on every axis. V2 has the cleaner citations and the only surviving HIGH (R2-G1), and V3 has the best catch on the design text itself (R3-G5, R3-G6). My claim is narrower: on step 1.0a routing, the HALT procedure and the 7.16 and 7.18 check lines, V1 is right and the others are silent or less exact.

## Steelman

### Steelman for V2

V2's strongest argument is precision of evidence plus a recall pass beyond the parsed matrix. Every V2 finding carries a ref and quote pair with an absolute path, 29 citations were checked and none failed, and its calibrator gave a per-finding calibrated_severity. R2-G1 is the best single finding of the run: item 8.3 at tasklist line 1436 requires each class and constant name to appear once by `grep -c`, while the design's own field annotations (`orca_rows: tuple[OrcaObservation, ...]`, `rows: tuple[ClassifiedRow, ...]`) repeat those names. A correct models.py cannot pass. That is a true "correct delivery cannot satisfy the check" defect, and the orchestrator re-read confirmed it. V2 also looked outside the matrix and found real obligations nobody else traced: the design line 80 builder rule, the "proposed" marking on byte limits, the import boundary for probes.py, B5, the renderer bans, and the set-union wording at design 636. V2 is also right on one point where V1 is vague: R2-G5 correctly notes that for the uncaptured case item 7.17 does hand open item 3 to the design's "behaviour until closed" rule.

### Steelman for V3

V3's strongest argument is that it read the design text as a document that the tasklist edits, not only as a source of rows. R3-G5 notes that design line 221 says a new template is allowed "only after a capture", and item 6.3 adds two templates with no capture. R3-G6 notes that the 6.3 Verification (no hit forbids the flag) and the 6.4 pass rule cannot both pass as written, because the D10 row quotes the old forbidding text. R3-G2 finds that design lines 181 and 196 keep the old count of 8 and escape the 6.3 grep. V3 used codegraph, checked the reflect `_git` seam against config.py:64-78 (R3-G9), and its calibrator found 36 citations checked with none failing. V3 also asks the question V1 and V2 skip: whether an owner decision can authorize a change that leaves the design contradicting its own extension rule. It is the only card that treats the R5 edit as a design-consistency problem and not only as a scope question.

## Strengths claimed

1. Breadth of coverage. 76 rows audited against 44 and 32, and the step-1.0a row is marked partial with `agrees_with_t1: false`, a disagreement that the orchestrator evidence for X-005 supports (tasklist line 1267 has only one Branch, for a changed field name).
2. R1-G1 is confirmed by the calibrator and by orchestrator evidence (X-002). Design line 552 wants a cursor template as one extra template, tasklist line 1485 requires `ALLOWED_ORCA` count 10, line 1793 pins ten. The card also traced the spread of the effect to 8.10, 10.3, FR-002, FR-026 and NFR-003, which the calibrator names as the only strong risk-spread reasoning on any card.
3. R1-G1 is also right on the run-current `--json` half (X-001). Line 1259 forbids running `run-current --json` in the capture, so a CLOSED answer of "plain output does not parse" reaches 7.17 with no owner route. V2's delegation argument only works while item 3 is STILL UNVERIFIED.
4. R1-G2, R1-G5 and R1-G6 are unique to V1 and confirmed. Item 6.2 (line 989) is "Log the OQ-1 decision (L3, no HALT)", so the pointer at line 1142 resolves to the wrong item. The 7.18 grep at line 1276 searches bare `coder`. The 7.16 Verification at line 1262 demands that every command be a template or a file read while Action step 6 at line 1260 runs `echo` and `ls -la`. A literal executor fails these checks, and a lax executor learns to skip them. That is a correctness harm to the gate, not a style point.
5. Severity discipline. Zero HIGH, no inflation. The calibrator cut V2 from six HIGH to one; V1 needed no cut at the top end.
6. Every remediation names an item and ends with a "Check by reading" test (calibrator actionability 0.85).

## Weaknesses identified in the others

V2:
- Severity inflation. Six HIGH, and by V2's own stated bar ("correct delivery cannot satisfy the check") only R2-G1 qualifies. The calibrator cut five to MEDIUM or LOW. A merged register that takes V2 at face value would put five false HIGH items ahead of real work.
- R2-G5 grades the cursor outcome HIGH, but its own claim describes a stall at the 8.10 and 10.3 pins, which the calibrator cut to MEDIUM (X-002). It then narrows F1 on run-current by relying on the delegation clause. The delegation is real only on the unverified path (X-001 evidence).
- R2-G7 claims equal counts can hide a swap. Tasklist line 2471 recounts at the recorded base, and the zero-hit grep is scoped to named files (line 2469). The concealment case needs an edit outside the scoped list that the plan never makes.
- V2 never examines the 7.15 to 7.17 HALT branches or the 7.16 and 7.18 check text, so the gate-quality layer of Phase 7 is unaudited by V2.
- Slice is only 44 rows, built from GQ, D, SP and INF families, so FR and NFR rows are not seen by V2 at all.

V3:
- 21 of 32 rows cite only "T1 matrix row" and are tagged [INFERRED]. For those rows V3 gives no independent evidence, so its coverage claim is thin.
- R3-G5 and V3's own best-practice line pull in two directions ("No unauthorized scope creep was found"), flagged in X-006. The finding is a design-text inconsistency, not a plan gap. Of its two remedies, the second (add the agent-wait forms to the capture) conflicts with tasklist line 1259, which keeps the flag out of step 1.0a; the first (reword design line 221) is sound.
- Eight of eleven findings are LOW wording or traceability fixes (R3-G4, G8, G10, G11 and similar). Calibration weakened R3-G6, R3-G8 and R3-G11. R3-G8's remedy conflicts with item 5.4.
- No finding touches step 1.0a routing, the HALT branches or the allowlist-count pin, the part of the plan with the largest blast radius.
- Slice of 32 rows does not include any FR, NFR or step row, so V3 offers no view on delivery of the build phases.

## Concessions

1. R1-G7 is refuted. Item 9.3 reads the OQ-8 record at line 1640 and its HALT at line 1643 handles a Run that cannot be read; item 8.4 re-checks OQ-7; 14.8 depends on the 14.7 gate. I withdraw it. It carries no weight.
2. R1-G3 is weakened. Item 7.16 at line 1262 already halts on a before and after difference, which is what design 875 requires. Only the missing timestamp-strip rule stands, and the claim that live state fields cause false halts stays [INFERRED] and unproven. No calibrated severity was given, so I ask the merge to treat it as LOW.
3. R1-G2 is confirmed but with lower impact. The preamble at line 1142 writes out Branch 1 and Branch 2 itself, and Branch 2 there says "the source quoting the owner's words". So the wrong pointer to 6.2 is real but harmless in practice, and the true residual weakness is only in 7.15 Branch 2 and 14.7 Branch 2 wording. I should have said this in the card.
4. R1-G8 is weakened. Step 1.0a is part of Phase 1 and does call templates 7 and 8 (lines 1257, 1258, 1260 step 3). "Eight called in Phase 1" is true of the capture and false only of the code. Ambiguous wording, not a misstatement (A-003a is contradicted).
5. R1-G9 is weakened. My sentence "fails after any unrelated change on the base" is overstated because line 2471 recounts at the recorded base. Line 2471 also demands replacement of every hit with the installed path, which is stricter than justification. This is closer to a Refinement.
6. Citation hygiene is the card's real defect. 41 of 78 checked citations failed, all the second refs on FR and NFR rows in the design range 444 to 484 (likely SPEC line numbers under the design file path). Two refs read "Section 8 gate", which is not a line. Four findings (R1-G5, R1-G6, R1-G7, R1-G9) have empty evidence lists. The finding-level quotes (14 of 14) all matched. The row verdicts and items stand; the second citations must be discarded or re-pointed before the merge relies on them.
7. Classification vocabulary. I did not use Aligned, Refinement, Drift or Regression, and the calibrator scored deviation clarity 0.60. R1-G3 and R1-G9 are arguably misclassified in gap_class. I also now think `gate-bypass` on R1-G1 is a little strong: a failed count check at 8.10 stops the executor, so the harm is a dead end and wasted code, not a silent bypass. The severity MEDIUM still holds because the dead end has no owner route.
8. R1-G6's second sentence (agent-wait forms in the check) is unsupported, since line 1259 says the flag is not run in 1.0a.
9. V2's R2-G1 is better than anything on my card. The merge should rank it first.
10. V3's R3-G5 and R3-G6 find real design-text inconsistencies introduced by item 6.3 that I treated as a strength ("R5 decision flows through 6.1 to 6.4"). I missed them.

## Per-point positions

| id | superior variant or none | one-line reason |
|----|--------------------------|-----------------|
| S-001 | V1 (breadth only) | V1 alone covers FR, NFR and design-step rows (calibrator coverage 0.90); the slices are disjoint, so this is breadth, not quality (see A-006). |
| S-002 | V1 and V3 | A profile with no inflated HIGH matches the calibrator; V2's six HIGH lost five on calibration. |
| S-003 | V2 | Every V2 finding carries evidence; four V1 findings have empty lists (conceded). |
| S-004 | V2 | V2 has 0 failed citations; V1 has 41 failed second refs on rows (conceded), though its verdicts stand. |
| S-005 | V2 | Highest calibrated confidence (0.81) with 0 failed citations; V1 0.71, V3 0.79. |
| S-006 | none | calibrated_severity is a calibrator output format, not a property of the card; the merge should apply the V2 style to all three. |
| S-007 | none | Three vocabularies, none maps to the four-category rubric; normalize in the merge. |
| S-008 | none | Scale notation is cosmetic. |
| S-009 | none | Model labels and codegraph use do not change finding truth. |
| S-010 | none | Different Tier-1 findings were touched; V1 confirmed F1, F3, F5, F12, F13, V2 and V3 cover the others. |
| C-001 | V1 | Cursor outcome with ten-template pins at 1485 and 1793; calibrator confirmed MEDIUM, V2's HIGH was cut to MEDIUM. |
| C-002 | V1 | Orchestrator evidence: on the CLOSED path no 7.17 Branch reaches the owner; V2's delegation covers only STILL UNVERIFIED. |
| C-003 | V1 | Only V1 raised it; confirmed, with lower impact because the preamble at 1142 spells out both branches. |
| C-004 | V1 | Only V1 raised it; the strip-rule gap stands, the HALT half was weakened (treat as LOW). |
| C-005 | none | V1 and V2 agree, both LOW; V2's [INFERRED] framing is as accurate as V1's. |
| C-006 | V2 | Only V2 audited the matrix itself; a valid LOW. |
| C-007 | V1 | Only V1 raised it; calibrator confirmed the bare `coder` grep and the unwritten forbidden-list sentence. |
| C-008 | V1 | Only V1 raised it; confirmed (`echo` and `ls -la` at line 1260 against the line 1262 check). |
| C-009 | V2 and V3 (by silence) | R1-G7 is refuted; V1 concedes, no weight. |
| C-010 | V3 | Both weakened; V3's six-called breakdown is the more exact remedy, though A-003a limits the premise. |
| C-011 | V1 (severity) | LOW is right given the base recount at 2471; V2's per-hit record is a good remedy but its HIGH was cut to LOW. |
| C-012 | V2 | Orchestrator-verified; the only HIGH to survive calibration. |
| C-013 | V2 | Only V2; weakened to MEDIUM, valid. |
| C-014 | V2 | Only V2; weakened to MEDIUM, valid. |
| C-015 | V2 | Only V2; MEDIUM after calibration; its note that F10's absence-of-import grep cannot prove B5 is correct. |
| C-016 | V2 | Only V2, from a spec-body recall pass. |
| C-017 | V3 | Only V3; D10 and R5 history cells under-report the departure. |
| C-018 | V3 | Only V3; lines 181 and 196 escape the 6.3 grep. |
| C-019 | V3 | Only V3; a valid LOW wording fix. |
| C-020 | V3 | Only V3; the design 221 rule is literally breached, though authorization by R5 stays true (X-006). |
| C-021 | V3 | Only V3; the 15.1 half holds, the D10 half was overstated. |
| C-022 | none | Weakened because 5.4 already cites 415 and 583; R3-G8's remedy conflicts with 5.4. |
| C-023 | V3 | Only V3; a real caution about `check=True`. |
| C-024 | V3 | Only V3; "five helpers" against four in design 7.1. |
| C-025 | V3 | Only V3; weakened LOW, valid as a record fix. |
| X-001 | V1 (on the CLOSED path) | V2 is right for STILL UNVERIFIED; once capture settles item 3 no Branch routes to the owner, and line 1259 forbids the `--json` probe. |
| X-002 | V1 | MEDIUM is supported by the orchestrator reading: a stall at the pins, not wrong code shipped. |
| X-003 | V1 (severity) | Both mechanisms are overstated; LOW stands, and V1's "any unrelated change" is conceded as overstated. |
| X-004 | V1 and V3 | HIGH should be kept for checks that correct delivery cannot satisfy; V2 applied its own bar to 1 of 6. |
| X-005 | V1 | Line 1267 has one Branch only; step-1.0a is partial, so the plan is weaker than T1 said. |
| X-006 | V3 | The design 221 breach is real and V1 missed it; V1 and V2 are right that R5 authorizes the templates, so it is a design-text fix, not unauthorized scope. |
| A-001 | none | Stated parts hold; c and d are UNSTATED, see responses below. |
| A-002 | none | Precondition a is open; V1 and V2 both tag it [INFERRED]. |
| A-003 | V3 | A-003a is contradicted (capture calls templates 7 and 8); V1 concedes, V3 gave the more precise breakdown. |
| A-004 | V1 (partly) | The scoped zero-hit check and the base recount weaken both V1's and V2's claims; V1 overstated less on severity. |
| A-005 | V3 | A-005b is contradicted by design 221 as it stands; V3 saw it. |
| A-006 | none | Row slices are disjoint by assignment; the merge needs a union check. |
| A-007 | none | Grades 3 and 4 are within normal spread; b is unstated. |
| A-008 | none | No card used the four categories; a UC-1 card has no completed deviation to classify. |
| A-009 | V2 (partly) | Only V2 stated a HIGH bar; the merge should normalize severities on that bar. |
| A-001c | none | Decides whether C-001 is a gap or non-event; see responses. |
| A-001d | none | Decides whether C-001 needs its own branch; see responses. |
| A-002a | none | Decides whether C-005 is a gap at all; see responses. |
| A-004b | none | Decides whether X-003's concealment case can happen; see responses. |
| A-004c | none | Decides Refinement versus gap on 14.5; see responses. |
| A-006a | none | Needs a union check across slices; see responses. |
| A-007b | none | Live Orca access is assumed; see responses. |
| A-008a / A-009a | none | Common rubric is unchecked; see responses. |

## Shared assumption responses

| id | response | reason |
|----|----------|--------|
| A-001a | ACCEPT | Design 552 and tasklist 1267 ("page.nextCursor or other") make a captured cursor field a real possibility. |
| A-001b | ACCEPT | Lines 1485 and 1793 pin ten with no condition. |
| A-001c | QUALIFY | Design 973's no-cursor fallback covers only the uncaptured case; when item 5 is CLOSED with a cursor field the fallback stops applying, which is why 7.17 needs a Branch. This precondition is what makes C-001 a gap. |
| A-001d | QUALIFY | A failing 8.10 or 10.3 Verification would stop the executor, so the failure is loud, not silent. But no instruction says whether to add an eleventh template or go to the owner. I now call it a dead end with no route, and I accept that `gate-bypass` was too strong a label. |
| A-002a | QUALIFY | The plan does not say who runs 7.16. It names the coordinator only in design 868. The gap is real as an actor traceability point but low impact, since no test runs it (calibrator: LOW). |
| A-002b | ACCEPT | "Never by a test" is already met. |
| A-003 / A-003a | REJECT | Capture reads in 1.0a are Phase 1 and call templates 7 and 8, so line 163 is ambiguous wording, not a misstatement. V1 concedes (R1-G8 weakened). |
| A-004a | REJECT | Line 2471 recounts at the recorded base, so drift alone does not fail the check. V1's "any unrelated change" wording is withdrawn. |
| A-004b | QUALIFY | The scoped list at 2469 limits what can hide a swap. Whether the task edits anything outside it is unverified by V1 and V2 (including `src/superclaude/core/CLAUDE.md`). |
| A-004c | QUALIFY | Line 2471 requires replacing each hit with the installed path, which is stricter than justifying it. So 14.5 is closer to a Refinement than a gap, as the calibrator reads it. |
| A-005a | ACCEPT | The OQ-1 record is RESOLVED with the owner's words. |
| A-005b | REJECT | An owner decision authorizes the templates but does not by itself edit design 221; 6.3 should reword it (V3's first remedy). |
| A-005c | QUALIFY | Phase 1 never calls templates 9 and 10 (tasklist 998, 1259), so no parse evidence is needed now; it will be needed before any later phase calls them. |
| A-006a | QUALIFY | 76 + 44 + 32 = 152 is the assigned set, but no card cross-checks another slice. The merge should run a union check on row ids, and should not claim full coverage from the cards alone. |
| A-006b | ACCEPT | V3's 21 rows rest on T1 mapping; treat them as lower weight. |
| A-007a | ACCEPT | Tasklist 1142 states that PENDING decisions block the gates that need them. |
| A-007b | QUALIFY | Live Orca access for 7.16 is assumed. Without it 7.17, 8.10, 9.1 and 10.3 stall; R1-G4's hand-off branch (as in 14.8 Branch B) would cover it. |
| A-008a | QUALIFY | A UC-1 pre-execution card has no completed work to classify as Drift or Regression, so absence of those labels is not a defect by itself. The calibrator still scores clarity against the rubric (0.60); I accept that for V1. |
| A-009a | REJECT | Severities are not comparable as written. Normalize on calibrated severity and on V2's stated bar (a check that correct delivery cannot satisfy is HIGH); under that bar V1's three MEDIUMs stand and V2's R2-G1 is the only HIGH. |
