# Base Variant Selection

Abbreviations: TL is the tasklist `TASK-RF-sweep-phase1-20261108-072653.md`. DESIGN is `docs/designs/orchestrator-mode.md`. CAL is a card's Part 2 blind calibration. DA is `diff-analysis.md`. V1 is the analyzer card (`variant-1-original.md`), V2 the qa card (`variant-2-original.md`), V3 the refactorer card (`variant-3-original.md`).

## Quantitative Scoring (50% weight)

Metric definitions used for these reflect cards:

- RC (requirement coverage): rows covered over the 151-row union of all three ledgers.
- IC (internal consistency): 1 minus contradictions over (rows plus findings). A contradiction is a card claim refuted by its own CAL or by the debate (DA X points).
- SR (specificity ratio): findings with one checkable recommendation that targets the right site, over all findings.
- DC (dependency completeness): cited references that resolve under CAL, over references checked.
- SC (section coverage): top-level YAML keys over 15 (the V2 key set, the widest).

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| Requirement Coverage (RC) | 0.30 | 0.503 (76/151) | 0.338 (51/151) | 0.159 (24/151) |
| Internal Consistency (IC) | 0.25 | 0.951 (1 - 4/82) | 0.984 (1 - 1/61) | 0.971 (1 - 1/34) |
| Specificity Ratio (SR) | 0.15 | 0.667 (4/6) | 0.800 (8/10) | 0.800 (8/10) |
| Dependency Completeness (DC) | 0.15 | 0.969 (124/128) | 0.958 (23/24) | 1.000 (40/40) |
| Section Coverage (SC) | 0.15 | 0.933 (14/15) | 1.000 (15/15) | 0.933 (14/15) |
| **Quantitative Score** | | **0.774** | **0.761** | **0.700** |

Notes on the counts:

- V1 IC contradictions: X-003 (2.16 called an edit, TL:347), X-006 ("installs nothing", TL:2488), X-005 (open item 2 instead of 3, DESIGN:971), and the R1-G1 "no owner route" clause. V1 SR misses: R1-G1 (wrong target, open item 2) and R1-G5 (no change). V1 DC failures: R1-G1, R1-G2, R1-G4, R1-G6.
- V2 IC contradiction: R2-G2 `gate-bypass` class against its own CAL (X-008). V2 SR misses: R2-G9 and R2-G10 (either-or recommendations). V2 DC failure: R2-G4 (9.2 is TL:1634, not TL:1635-1636). V2 has the extra `grounding_root` key.
- V3 IC contradiction: R3-G10 calls the owner gate sound, refuted by TL:989 (X-001). V3 SR misses: R3-G1 (two alternatives) and R3-G7 (no item target for the helper).

## Qualitative Scoring (50% weight), Additive Binary Rubric

### Per-Criterion Scores

#### Completeness (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1. Covers all explicit requirements | MET | MET | MET |
| 2. Addresses edge cases and failure scenarios | NOT MET | MET | MET |
| 3. Includes dependencies and prerequisites | MET | MET | MET |
| 4. Defines success or completion criteria | MET | MET | MET |
| 5. Specifies what is out of scope | MET | MET | NOT MET |
| **Subtotal** | **4/5** | **5/5** | **4/5** |

CEV:

- C1. V1: Claim, covers its assigned spine. Evidence, 76 rows over FR-001 to FR-026, NFR-001 to NFR-015 and the step rows (S-001). Verdict MET. V2: Claim, covers the QA and gate rows. Evidence, 51 rows with `recommended_action` per row (S-005). Verdict MET. V3: Claim, covers the design-fix slice. Evidence, 24 rows on phases 2 to 6 (S-002). Verdict MET. Each card's scope was assigned, so coverage is judged within scope; breadth is scored by RC.
- C2. V1: Claim, failure paths reviewed. Evidence, misses all three calibrated HIGHs (R2-G7 deadlock, R2-G5 `grep -c`, R2-G3 echo), each a failure path. Verdict NOT MET. V2: Evidence, R2-G7 (TL:989 Branch 1 shadows Branch 2) and R2-G5 (TL:1431 against TL:1434). Verdict MET. V3: Evidence, R3-G1 single-row case (research/04:90) and R3-G4 id-only approval (TL:1156-1168). Verdict MET.
- C3. V1: Evidence, R1-G4 commit grouping and R1-G5 gate order (DESIGN:907-912). MET. V2: Evidence, R2-G6 gate files before 8.1 (TL:1417-1421). MET. V3: Evidence, R3-G9 precedent survey (recovery.py:424-434, atomic.py:22-38). MET.
- C4. All three give a `holds`-style verdict per row and a check per recommendation (V1 "Check:" lines; V2 named PASS results; V3 "expect one hit each"). MET for all.
- C5. V1: Claim, states what it did not inspect. Evidence, its summary admits the QA items were not fully inspected. Verdict MET (set in the reverse pass, see Position-Bias). V2: Evidence, the `not_checked` list (S-005). MET. V3: Evidence, INF-005 and INF-014 are marked false-match with no gap entry and no out-of-scope note (X-010). NOT MET.

#### Correctness (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1. No factual errors | NOT MET | MET | NOT MET |
| 2. Approaches are feasible | MET | MET | MET |
| 3. Terminology consistent | MET | MET | MET |
| 4. No internal contradictions | MET | MET | MET |
| 5. Claims supported by evidence | NOT MET | MET | MET |
| **Subtotal** | **3/5** | **5/5** | **4/5** |

CEV:

- C1. V1: Evidence, X-003 (TL:347: 2.16 is a QA lens), X-006 (TL:2488: `pipx run --spec` installs runtime dependencies), X-005 (DESIGN:971 is open item 3). NOT MET. V2: Evidence, the one cite drift (R2-G4, two lines) is a citation slip, not a false claim; severity inflation is a calibration matter scored under X-008. MET. V3: Evidence, R3-G10 "owner gate sound" refuted by TL:989 (X-001). NOT MET.
- C2. Every recommendation in all three cards names an edit an executor can make. MET for all.
- C3. All three use the reflect gap classes and row ids consistently. MET for all.
- C4. No card contradicts itself between its rows and its findings, except V2 INF-013 `covered` against R2-G8 (X-007). Judged as a row-label slip that V2 conceded, not a contradiction of substance. MET for all.
- C5. V1: Evidence, CAL failed 4 citations (R1-G1, R1-G2, R1-G4, R1-G6), dcc 0.25. NOT MET. V2: Evidence, 24 ranges checked, 1 failed, cc 0.90. MET. V3: Evidence, 40 checked, 0 failed. MET.

#### Structure (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1. Logical section ordering | MET | MET | MET |
| 2. Consistent hierarchy depth | MET | MET | MET |
| 3. Clear separation of concerns | NOT MET | MET | NOT MET |
| 4. Navigation aids present | MET | MET | MET |
| 5. Follows artifact conventions | NOT MET | NOT MET | NOT MET |
| **Subtotal** | **3/5** | **4/5** | **3/5** |

CEV:

- C1, C2, C4. All three follow the card schema (metadata, row_verdicts, findings, compliance, self_scores, summary) with ids usable as anchors. MET for all.
- C3. V1: Evidence, R1-G5 is a confirmation filed as a finding ("No plan change needed"). NOT MET. V2: Evidence, no confirmation in findings (S-007). MET. V3: Evidence, R3-G9 and R3-G10 are confirmations ("No change needed"). NOT MET.
- C5. All three omit the Aligned, Refinement, Drift, Regression deviation category (S-008). NOT MET for all.

#### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1. Unambiguous language | MET | NOT MET | NOT MET |
| 2. Concrete rather than abstract | MET | MET | MET |
| 3. Each section has a clear purpose | MET | MET | MET |
| 4. Terms defined | MET | MET | MET |
| 5. Actionable next steps | MET | MET | MET |
| **Subtotal** | **5/5** | **4/5** | **4/5** |

CEV:

- C1. V1: Evidence, each recommendation is a single edit plus a "Check:" line (R1-G3, R1-G4). MET. V2: Evidence, R2-G9 ("Add a B2 matrix row or explicitly expand NFR-004") and R2-G10 ("Add a rationale deliverable to 14.9, or ...") leave the choice open. NOT MET. V3: Evidence, R3-G1 ("keep a transcript clause ... or word the item 3.1 rule ..."). NOT MET.
- C2 to C5. All three quote exact text and name items. MET for all.

#### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1. At least 3 risks with probability and impact | NOT MET | MET | NOT MET |
| 2. Mitigation per risk | MET | MET | MET |
| 3. Failure modes and recovery | MET | MET | MET |
| 4. External dependencies | MET | MET | MET |
| 5. Monitoring or validation mechanism | MET | MET | MET |
| **Subtotal** | **4/5** | **5/5** | **4/5** |

CEV:

- C1. V1: Evidence, findings state impact (R1-G3 "false BLOCKING") but give no blast radius or likelihood per finding. NOT MET. V2: Evidence, three findings state the literal outcome (R2-G7 STOP before RESOLVED; R2-G5 a correct module fails; R2-G3 the probe fails), with CAL rsc 0.85. MET. V3: Evidence, CAL notes little blast radius per finding (rsc 0.72). NOT MET.
- C2. Every finding in all three carries a recommendation. MET.
- C3. V1 R1-G1 (unparseable plain output), V2 R2-G7 (resume path), V3 R3-G4 (approval on id alone). MET for all.
- C4. V1 run-current and pipx (DESIGN:874, TL:2474); V2 Orca templates (TL:1258); V3 WORKER-CONTRACT.md:110. MET for all.
- C5. Each recommendation has a check (grep, named PASS, exit code). MET for all.

#### Invariant and Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1. Boundary conditions for collections | NOT MET | MET | NOT MET |
| 2. State variable interactions | NOT MET | MET | MET |
| 3. Guard condition gaps | MET | MET | MET |
| 4. Count divergence | MET | MET | NOT MET |
| 5. Interaction effects when features combine | NOT MET | MET | MET |
| **Subtotal** | **2/5** | **5/5** | **3/5** |

CEV:

- C1. V1: Claim, collection bounds reviewed. Evidence, R1-G6 checks a whole-tree count (168) but not the scoped set boundary of the five folders; no empty or one-element case is raised. NOT MET. V2: Evidence, R2-G3 grep scope (captured output inside the probe file, TL:1260) and R2-G6 per-file outcome set (TL:1417-1421). MET. V3: Evidence, R3-G3 is a pattern mismatch (`:545` against "(line 545)"), not a collection boundary. NOT MET (confirmed on re-evaluation, see Position-Bias).
- C2. V1: Evidence, no finding traces a status field across items; the 6.2 PENDING to RESOLVED transition is missed. NOT MET. V2: Evidence, R2-G7 traces `status` PENDING through Branch 1 and Branch 2 (TL:982-992). MET. V3: Evidence, R3-G4 traces the approval state from 7.3 to 7.4 (TL:1156-1168, DESIGN:988). MET.
- C3. V1: Evidence, R1-G1 (no HALT branch for unparseable output; partly holds). MET. V2: R2-G7, R2-G2. MET. V3: R3-G4 (the 7.4 gate passes on an id). MET.
- C4. V1: Evidence, R1-G6 (one hit removed plus one added leaves the count of 168 unchanged). MET. V2: Evidence, R2-G5 (TL:1434 "appears once" against two required occurrences). MET. V3: Evidence, no count-divergence finding. NOT MET.
- C5. V1: Evidence, no finding on two features combining. NOT MET. V2: Evidence, R2-G2 (7.15 record used by 7.16 without recheck, TL:1242-1248). MET. V3: Evidence, R3-G1 (R3-B1 edit 4 combined with the R3-B2 insert drops the single-row clause). MET.

### Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4/5 | 5/5 | 4/5 |
| Correctness | 3/5 | 5/5 | 4/5 |
| Structure | 3/5 | 4/5 | 3/5 |
| Clarity | 5/5 | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 5/5 | 4/5 |
| Invariant and Edge Case | 2/5 | 5/5 | 3/5 |
| **Total** | **21/30** | **28/30** | **22/30** |
| **Qualitative Score** | **0.700** | **0.933** | **0.733** |

### Edge Case Floor Check

| Variant | Invariant and Edge Case Score | Floor (1/5) | Status |
|---|---|---|---|
| V1 | 2/5 | 1/5 | Eligible |
| V2 | 5/5 | 1/5 | Eligible |
| V3 | 3/5 | 1/5 | Eligible |

## Position-Bias Mitigation

| Dimension | Variant | Pass 1 (V1, V2, V3) | Pass 2 (V3, V2, V1) | Agreement | Final |
|---|---|---|---|---|---|
| Completeness C5 | V1 | NOT MET | MET | Disagree | MET |
| Invariant C1 | V3 | NOT MET | MET | Disagree | NOT MET |
| All other 88 criterion cells | all | as tabled | as tabled | Agree | as tabled |

Disagreements found: 2. Verdicts changed through re-evaluation: 1.

- V1 Completeness C5: re-read V1's summary. It states that the QA items were not fully inspected, which is an explicit scope statement. Final MET.
- V3 Invariant C1: re-read R3-G3. The defect is a literal pattern that cannot match DESIGN's "(line 545)" form; no collection size, empty case or set boundary is involved. Final NOT MET.

## Combined Scoring

| Variant | Quantitative (x0.50) | Qualitative (x0.50) | Combined Score |
|---|---|---|---|
| V1 | 0.774 x 0.50 = 0.387 | 0.700 x 0.50 = 0.350 | **0.737** |
| V2 | 0.761 x 0.50 = 0.381 | 0.933 x 0.50 = 0.467 | **0.847** |
| V3 | 0.700 x 0.50 = 0.350 | 0.733 x 0.50 = 0.367 | **0.717** |

Margin: 11.0% (V2 0.847 over V1 0.737). Tiebreaker applied: No (margin above 5%).

## Selected Base: V2 (qa card, `variant-2-original.md`)

### Selection Rationale

V2 leads on the qualitative layer by 7 criteria over V1 and 6 over V3, and is within 0.013 of V1 on the quantitative layer, where V1's lead comes almost entirely from RC (ledger breadth by assignment, not by quality). V2 holds every calibrated HIGH (R2-G7, R2-G5, R2-G3), has the highest calibrated confidence (0.85), and is the only card at 5/5 on Invariant and Edge Case coverage. The debate agrees: V2 won 15 of 39 points, the most of any variant, and all three advocates named V2's HIGHs as the merge core in Round 2.

### Strengths to Preserve from Base

- The three calibrated HIGH findings and their literal-execution evidence: R2-G7 (TL:982-992, TL:1140, TL:2481-2484), R2-G5 (TL:1431-1435), R2-G3 (TL:1258-1261).
- The `recommended_action` and `not_checked` fields (S-005).
- Line-range citation notation (S-003).
- No confirmations in the findings list (S-007).
- Tier-1 engagement, including the only Tier-2 confirmation of T1 F3 (S-009).
- The INF-005 and INF-014 delivery verdicts (X-010) and the INF-001 to R2-G1 conversion (C-015).

### Strengths to Incorporate from Non-Base Variants

- From V1: the 76-row FR, NFR and step ledger (S-001); R1-G3, the 14.11 lens folder fix (C-006, CAL MEDIUM); R1-G4, the 14.46 commit-grouping line (C-010); the count part of R1-G6; the R1-G1 M2 naming (X-005, partly); the R1-G2 ID labels (C-004).
- From V3: the 24 design-fix rows for phases 2 to 6 (S-002); R3-G4, owner approval of the WC-16 text (CAL MEDIUM, kept separate per INV-021); R3-G3 dead `:545` greps; R3-G5 cadence wording; R3-G6 CHANGELOG bullet; R3-G8 `make lint-architecture`; R3-G1 FR-010 wording; R3-G2 fallback pointer; R3-G7 fake-seam preference; the zero-failure citation corrections (TL:425 for R3-G2, TL:796 for R3-G3).
- From the debate and Round 2.5: the fix-sufficiency items INV-001 to INV-017 folded into the merged findings (see `refactor-plan.md`).
