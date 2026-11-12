# Base Selection Report

- Protocol: sc-adversarial-protocol, Mode A, Step 3 (Hybrid Scoring and Base Selection, T04.01 to T04.06; algorithm in refs/scoring-protocol.md A.1 to A.5)
- Written by: debate orchestrator (neutral; took no part in the debate)
- Date: 2026-11-08
- Variants: V1 = `variant-1-original.md` (reviewer 1, analyzer, sonnet slot); V2 = `variant-2-original.md` (reviewer 2, qa, haiku slot); V3 = `variant-3-original.md` (reviewer 3, refactorer, opus slot). Input order V1, V2, V3.
- Inputs: the three variants with their embedded blind calibrations, `diff-analysis.md`, `debate/consensus.md`, `invariant-probe.md`, and `../coverage-matrix.yaml` as the source requirements for RC.
- Debate status carried in: BLOCKED_BY_INVARIANTS (INV-006, INV-021). Base selection proceeds; the block is a merge obligation, not a scoring input. See `debate-transcript.md`.
- Correctness evidence: the calibrations embedded in each variant (per_finding_check verdicts, calibrated_severity, citations_checked and citations_failed) and the consensus positions after Round 2.

## Quantitative Scoring (50% weight)

Computed by a read-only script over the variant text (each metric uses the reviewer card section, above `## Blind calibration`, unless stated). Running it twice gives the same numbers.

| Metric | Weight | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|--------|--------|---------------|---------|-----------------|
| requirement_coverage (RC) | 0.30 | 0.500 (76 of 152) | 0.289 (44 of 152) | 0.211 (32 of 152) |
| internal_consistency (IC) | 0.25 | 1.000 (0 of 85) | 0.906 (5 of 53) | 1.000 (0 of 43) |
| specificity_ratio (SR) | 0.15 | 1.000 (297 concrete, 0 vague) | 0.996 (240 concrete, 1 vague) | 1.000 (275 concrete, 0 vague) |
| dependency_completeness (DC) | 0.15 | 1.000 (11 of 11) | 1.000 (1 of 1) | 1.000 (8 of 8) |
| section_coverage (SC) | 0.15 | 1.000 (2 of 2) | 1.000 (2 of 2) | 1.000 (2 of 2) |
| **quant_score** | | **0.850** | **0.763** | **0.763** |

Unrounded: V1 0.85000, V2 0.76264, V3 0.76316.

### Computation details

- **RC.** Source requirements are the 152 row ids in `coverage-matrix.yaml` (`rows:`; 126 parsed and 26 inferred, all unique). For each variant, RC = distinct matrix ids that appear as a `row_coverage` id in the card, divided by 152. Every row_coverage id in every card is a matrix id (none outside the matrix). Verdict mix: V1 covered 65, covered-in-substance 10, partial 1; V2 covered 18, covered-in-substance 15, partial 8, missing 3; V3 covered 26, covered-in-substance 6. Caveat that matters for reading the result: the slices were assigned disjointly by the reviewer briefs (union 152, pairwise overlap 0, 0, 0, reproduced by this script), so RC here measures the width of each brief, not the quality of each reviewer (consensus S-001, 90%). A sensitivity check without this effect is given under Combined Scoring.
- **IC.** Scorable claims = findings plus row_coverage rows (V1 9 + 76 = 85; V2 9 + 44 = 53; V3 11 + 32 = 43). A contradiction is a claim inside the same card that conflicts with another claim or with a constraint the card itself states. V2: 5. R2-G1 states the card's HIGH bar ("HIGH under the brief's scale because correct delivery cannot satisfy the check"), and five other findings are rated HIGH while their own text says correct delivery is not blocked (R2-G2 "No present stale-count use or REPORT edit was found"; R2-G3 "the before-release deadline is not itself already breached"; R2-G4 missing checks; R2-G5 a conditional branch; R2-G7 a count that "can conceal"). The calibrator names the same conflict ("conflicts with the card's own HIGH standard ... which only R2-G1 meets"). V1: 0 found (summary counts match findings: 0 HIGH, 3 MEDIUM, 6 LOW; rows_audited 76 matches the list). V3: 0 found (3 MEDIUM, 8 LOW, 32 rows all match; R3-G5 and the best-practice line "No unauthorized scope creep was found" are about different things, as all three advocates agreed on X-006; R3-G7 duplicates part of R3-G1 but does not oppose it). Errors against outside files (refuted R1-G7, the 41 failed V1 second refs, R3-G8's conflict with item 5.4) are correctness defects, not internal contradictions; they are scored in the qualitative layer.
- **SR.** Prose fields only (claim, remediation, note, quote, and best-practice reasons). Concrete tokens: numbers, backticked names, ID tokens such as FR-011 or R3-G5, and file names ending in .py, .md or .yaml. Vague tokens: exactly the protocol list ("appropriate", "as needed", "properly", "adequate", "should consider", "might", "various", "etc.", "best practice(s)", "industry standard"). All three cards are near the ceiling, so SR barely separates them. V2's one vague token is "adequate" in R2-G4 ("is not an adequate B5 check"), counted because the rule is lexical.
- **DC.** Internal references are mentions of the card's own finding ids (R1-G*, R2-G*, R3-G*) outside their defining line, for example V1 row notes "see R1-G1" and V3 R3-G7 "include 4 if R3-G2 is applied". All resolve. References to the tasklist, design, SPEC, Tier-1 card (F-numbers) or coverage matrix are external documents and are excluded by rule, so V1's 41 failed second refs do not enter DC; they enter the qualitative Correctness dimension.
- **SC.** Each variant has two H2 sections (`## Reviewer card`, `## Blind calibration`), so SC is 1.000 for all three and does not discriminate.

## Qualitative Scoring (50% weight): Additive Binary Rubric

Method. Two independent judge agents ran the 30-criterion rubric with the Claim-Evidence-Verdict rule (MET needs a cited piece of evidence; no evidence means NOT MET; no partial credit). Pass 1 evaluated V1, V2, V3 in that order; Pass 2 evaluated V3, V2, V1. Both used the embedded calibrations and `debate/consensus.md` Parts 2 and 5 as correctness evidence, with two shared rules: a finding the calibrator refuted or all three advocates withdrew counts as a factual error (K1), and a stated severity bar contradicted by the card's own ratings counts as an internal contradiction (K4). "Source input" for C1 is the slice and duties set by each card's reviewer brief. The tables give the final verdict after disagreement resolution; the five criteria where the passes disagreed are marked (R) and logged under Position-Bias Mitigation.

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| C1 Covers all explicit requirements from source input | MET | 76 of 76 slice rows audited (summary); owner gates (R1-G2), step 1.0a (R1-G1, R1-G3); T1 F1, F3, F5, F12, F13 related | MET | 44 of 44 slice rows; recall pass (R2-G6); soundness, test-plan and gate-sizing duties in the best-practice reasons; T1 F2, F6, F9, F10 | NOT MET | 21 of 32 rows "per T1 matrix" with delivering items not re-read, against brief duty 5 (card line 375 admits it) |
| C2 Edge cases and failure scenarios | MET | R1-G1 two unrouted capture outcomes; R1-G3 live state change between reads | MET | R2-G1 conforming models.py fails; R2-G5 captured-cursor branch missing | MET | R3-G6 checks fail on historical quotes; R3-G2 no zero-argv pin for templates 9 and 10 |
| C3 Dependencies and prerequisites | MET | FR-002 row ties the fourth test to the 7.14 to 7.17 capture; step rows check gate order against SPEC 15.2 | MET | R2-G5 ties the 7.17 outcome to the 8.10 and 10.3 pins; D9 row gates 8.4 on sign-off | MET | R3-G5 names the missing "only after a capture" prerequisite for templates 9 and 10 |
| C4 Success or completion criteria | MET | Every remediation ends with "Check by reading" | MET | Every remediation ends with "Success:" | NOT MET | Calibrator: "few remediations state how to verify the fix" |
| C5 Explicit out-of-scope statement | NOT MET | No exclusion stated; line 226 is a limitation note, not a scope boundary | MET | Best-practice reason: the I19 sizing authority was outside the permitted file set, so only the stated rule was checked | NOT MET (R) | Line 375 is a limitation note of the same kind as V1's line 226; no scope boundary stated |
| **Subtotal** | **4/5** | | **5/5** | | **2/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| K1 No factual errors | NOT MET | R1-G7 refuted by calibration and withdrawn (C-009); R1-G8 withdrawn (C-010) | NOT MET | R2-G5 and row INF-019 said run-current was covered by delegation; V2 conceded the CLOSED path is unrouted (X-001, X-005) | NOT MET | R3-G3 withdrawn (C-010); R3-G8 superseded by item 5.4 and conceded (C-022) |
| K2 Approaches feasible | MET | 7.17 third Branch, count from the facts file, anchored greps; R1-G1 fix kept (consensus rank 2) | MET | Anchored or AST definition count (R2-G1); one Key Constraints bullet (R2-G2) | NOT MET | R3-G8 remedy edits the D6 row that item 5.4 forbids; second R3-G5 remedy withdrawn |
| K3 Terminology consistent and accurate | NOT MET | `gate-bypass` on R1-G1 dropped by consensus; R1-G3 and R1-G9 classes arguable (calibrator); SPEC line numbers under the design path | MET | gap_class values used consistently; no V2 class label rejected by consensus | MET | gap_class set separates design fix, check defect and reuse (S-007, clarity 0.85) |
| K4 No internal contradictions | MET | Summary counts match findings; no stated bar broken (IC 1.000) | NOT MET | Six HIGH against its own bar; only R2-G1 meets it (calibrator; X-004; IC 0.906) | MET | Summary counts match; no stated bar broken (IC 1.000) |
| K5 Claims supported by evidence | NOT MET | 41 of 78 citations failed; four findings with empty evidence lists (S-003, S-004) | MET | 29 checked, 0 failed; ref and quote pairs on every finding | NOT MET (R) | 21 of 32 rows cite only "T1 matrix row"; R3-G7 quote field is a reviewer note (S-003, S-004) |
| **Subtotal** | **2/5** | | **3/5** | | **2/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| S1 Logical ordering | MET | header, findings, row_coverage, best_practice_compliance, confidence, summary, then calibration | MET | same schema order | MET | same schema order |
| S2 Consistent hierarchy | MET | each finding and row uses one field set | MET | uniform field sets | MET | uniform depth across 11 findings and 32 rows |
| S3 Separation of concerns | MET | row notes defer to findings ("see R1-G1 and R1-G3") | MET | GQ-103 defers the model-check defect to R2-G1 | MET | findings, rows, grade and summary in separate blocks |
| S4 Navigation aids | MET | rows FR-026, NFR-003, step-1.0a, step-1.28 point at findings | MET | GQ-103 to R2-G1; INF-017 to F12; R2-G9 to T1 card lines | MET | INV-005 note cites R3-G1 and R3-G6; reasons cite R3-G2, R3-G6, R3-G9 |
| S5 Follows artifact conventions | NOT MET | four `evidence: []`; two refs read "Section 8 gate" | NOT MET (R) | absolute /home/coder paths and "scale: 5", while its brief (reviewer-2.md lines 65 and 121) asks for repo-relative paths and "scale: 0-5" | NOT MET | evidence as one mapping, not a list; R3-G7 quote is a note; row evidence without a path |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| L1 Unambiguous language | NOT MET | hedges: "may legitimately end" (R1-G1), "could compare differently" (R1-G3) | MET (R) | no hedge words in the card (the four "could" hits are in the calibration section) | NOT MET (R) | hedges: "may leave 15.1 with no hit" (R3-G6), "the executor may copy" (R3-G9), "may be called" (R3-G2) |
| L2 Concrete | MET | item numbers and lines (7.17, 8.10, 10.3; tasklist 1265, 1485) | MET | grep -c clause at tasklist 1436 against design 454 and 466 | MET | R3-G2 widened grep; R3-G10 names the four helpers |
| L3 Clear section purpose | MET | one job per schema block; plus or minus reasons | MET | one job per block; plus or minus reasons | MET | one job per block |
| L4 Terms defined on first use | NOT MET | FR, NFR, OQ, HALT, R5, T1, SPEC undefined | NOT MET | GQ, SP, INF, OQ, T1 undefined | NOT MET | D10, INV-005, NFR, OQ, R5, T1 undefined |
| L5 Actionable next steps | MET | each remediation names the item and the check | MET | each remediation names the item and a success test | MET | each finding gives a concrete edit to a named item |
| **Subtotal** | **3/5** | | **4/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| R1 At least 3 risks with probability and impact | NOT MET | only R1-G1 states likelihood ("a likely case and not a remote one") | NOT MET | severity only; no probability | NOT MET | severity only; calibrator: no blast-radius reasoning |
| R2 Mitigation per risk | MET | all nine findings carry a remediation | MET | all nine carry a remediation | MET | all eleven carry a remediation |
| R3 Failure modes and recovery | MET | R1-G1 recovery: PENDING owner note, then HALT; R1-G3 branch to a person ruling | MET | R2-G5: record authorization or halt for a design revision | NOT MET | calibrator: "no execution-order or rollback risks" |
| R4 External dependencies | MET | R1-G1 and R1-G3 cover live Orca capture outcomes and live worker fields | MET | R2-G5 live capture outcome; R2-G8 live capture actor | MET | R3-G5 no evidence that template 10 parses; R3-G9 reflect helper differences |
| R5 Monitoring or validation | MET | each "Check by reading" is a validation step | MET | "Success:" tests, for example R2-G7 | MET | R3-G2 widened grep and zero-argv assertions |
| **Subtotal** | **4/5** | | **4/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| E1 Collection boundaries | MET | allowlist fixed at exactly ten while the capture can need an eleventh (R1-G1) | MET | exactly ten templates (R2-G5); "appears once" over names (R2-G1) | MET | 15.1 left with no hit (R3-G6); zero-argv for templates 9 and 10 (R3-G2) |
| E2 State interactions across components | MET | captured cursor field against the 8.10 count and 10.3 tests (R1-G1) | MET | 7.17 recorded cursor against the 8.10 and 10.3 pins (R2-G5) | MET | 6.3 allowlist edit against the design 221 rule (R3-G5, X-006) |
| E3 Guard condition gaps | MET | unanchored `coder` grep (R1-G5); Branch 2 sets RESOLVED with no condition (R1-G2) | MET | no checks for the probes.py boundary, B5, renderer bans (R2-G4) | MET | grep misses "(8)" and "8 read" (R3-G2); no historical-text exemption (R3-G6) |
| E4 Count divergence | MET | fixed count of ten against a captured eleventh (R1-G1, C-001) | MET | occurrence count used as a definition count (R2-G1, C-012) | MET | "five helpers" against four (R3-G10, C-024); stale count of 8 (R3-G2) |
| E5 Interaction effects | MET | R5 allow, capture outcome and exact-count pins combine (R1-G1, X-005) | MET | conditional cursor template against the R5 ten-template pins (R2-G5) | MET | D10 text written by 6.3 against the 6.3 and 6.4 greps (R3-G6) |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 4/5 | 5/5 | 2/5 |
| Correctness | 2/5 | 3/5 | 2/5 |
| Structure | 4/5 | 4/5 | 4/5 |
| Clarity | 3/5 | 4/5 | 3/5 |
| Risk Coverage | 4/5 | 4/5 | 3/5 |
| Invariant & Edge Case | 5/5 | 5/5 | 5/5 |
| **qual_score** | **22/30 = 0.733** | **25/30 = 0.833** | **19/30 = 0.633** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Floor (at least 1/5) | Eligible as base |
|---------|-----------------------------|----------------------|------------------|
| V1 | 5/5 | met | yes |
| V2 | 5/5 | met | yes |
| V3 | 5/5 | met | yes |

No variant scores 0/5, so the floor is not suspended. Note that this dimension does not separate the cards: each one found count, guard and boundary gaps, which is what a check-soundness review of this tasklist produces. It also says nothing about the two invariants none of them found (INV-006, INV-021).

## Position-Bias Mitigation

Pass 1 (order V1, V2, V3) totals: V1 22, V2 24, V3 20. Pass 2 (order V3, V2, V1) totals: V1 22, V2 26, V3 21. The passes agreed on 85 of 90 criterion-variant pairs (V1 30 of 30, V2 28 of 30, V3 27 of 30). The five disagreements were re-evaluated by the orchestrator against both passes' evidence, with the bar each pass had already applied to the other variants; the re-evaluation verdict is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Reason for the final verdict |
|-----------|---------|--------|--------|-----------|-------|------------------------------|
| S5 conventions | V2 | NOT MET | MET | DISAGREE | NOT MET | Re-read reviewer-2.md: line 65 "Cite paths relative to the repository root", line 121 "scale: 0-5". V2 uses absolute paths and "scale: 5". Complete ref and quote pairs do not cure a deviation from the brief's card shape. |
| L1 unambiguous language | V2 | NOT MET | MET | DISAGREE | MET | Both passes judged V1 and V3 by lexical hedges ("may", "could"). A grep of V2 finds "could" only in the calibration section (lines 545 to 582), none in the card. Pass 1's reason (R2-G4 offers two methods) is an open option, not hedged language. |
| C5 out of scope | V3 | NOT MET | MET | DISAGREE | NOT MET | V3 line 375 ("not re-read item by item") is the same kind of limitation note as V1 line 226, which both passes scored NOT MET. The INF-014 "a constraint, not an action" note classifies a row, like V1's FR-010 note that Pass 1 rejected. |
| K5 evidence support | V3 | NOT MET | MET | DISAGREE | NOT MET | 0 of 36 checked citations failed, but 21 of 32 row verdicts rest only on "T1 matrix row" with no own evidence or rationale. Both passes scored V1 NOT MET for unsupported row refs of similar weight. |
| L1 unambiguous language | V3 | MET | NOT MET | DISAGREE | NOT MET | The hedges Pass 2 cites are in the card: "may leave 15.1 with no hit at all" (R3-G6), "the executor may copy" (R3-G9), "or state that they may be called" (R3-G2). The calibrator's "no hedging" referred to classification, not wording. Same bar as V1. |

Disagreements re-evaluated: 5
Final verdicts changed: 5 of 5 resolutions differ from one of the two passes by construction; against Pass 1, 2 changed (V2 L1 to MET, V3 L1 to NOT MET); against Pass 2, 3 changed (V2 S5, V3 C5, V3 K5 to NOT MET).
Effect: V2 25 (Pass 1 24, Pass 2 26), V3 19 (Pass 1 20, Pass 2 21), V1 22 (both passes).

## Combined Scoring

variant_score = 0.50 × quant_score + 0.50 × qual_score

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker (diff points won of 50) |
|---------|---------------|--------------|-----------------|-------------------------------------------|
| V2 (qa) | 0.381 (0.763) | 0.417 (0.833) | **0.798** | 12 (24%) |
| V1 (analyzer) | 0.425 (0.850) | 0.367 (0.733) | **0.792** | 9 (18%) |
| V3 (refactorer) | 0.382 (0.763) | 0.317 (0.633) | **0.698** | 12 (24%) |

Unrounded: V2 0.79798, V1 0.79167, V3 0.69825.

**Margin**: V2 over V1 is 0.0063 (0.63 percentage points), below the 0.05 threshold. V1 over V3 is 0.093.
**Tiebreaker applied**: Yes, level 1 (debate performance).

- Level 1: diff points won in the Step 2 scoring matrix (`debate-transcript.md`, winner tally): V2 12, V1 9. The gap is 3 points of 50 (6 percentage points; V1 has 25% fewer wins than V2), which is not within 5%, so level 1 decides. Winner: V2. Levels 2 (correctness count: V2 3, V1 2) and 3 (input order) were not needed; level 2 would also have chosen V2.
- Sensitivity checks, all giving the same base:
  - RC normalized to each card's assigned slice (every card audited its whole slice, so RC = 1.000 for all, removing the brief-width effect of S-001): V2 0.905, V1 0.867, V3 0.817. Margin 0.038, under 0.05; level 1 again chooses V2.
  - Pass 1 qualitative verdicts only: V1 0.792, V2 0.781. Margin 0.010; level 1 chooses V2.
  - Pass 2 qualitative verdicts only: V2 0.815, V1 0.792. Margin 0.023; level 1 chooses V2.
- Reading the margin: V1 leads the quantitative layer only through RC, which measures brief width (76 rows against 44), and V2 leads the qualitative layer on correctness, completeness and clarity. The combined scores are close enough that the base choice rests on the debate record, and that record favours V2 under every variant of the calculation above.

## Selected Base: Variant 2 (reviewer 2, qa, haiku slot)

### Selection Rationale

V2 has the highest combined score (0.798), but by less than the 0.05 tiebreak threshold over V1 (0.792), so the protocol's level-1 tiebreaker decides: V2 won 12 diff points in the debate against V1's 9. The choice holds under all three sensitivity checks. The evidence behind it:

- It holds the only finding of the three cards that survived calibration at HIGH: R2-G1, the 8.3 `grep -c` check that rejects a correct models.py (calibrator confirmed, C-012 at 98%, conceded by V1 and V3). The probe found the R2-G1 fix alone is enough (INV-020).
- It has the strongest grounding: 29 citations checked, 0 failed, ref and quote pairs on every finding (S-003, S-004 and S-005 at 90 to 95%), against V1's 41 of 78 failed and V3's 21 inferred rows.
- Its calibration is the only one that gives calibrated_severity per finding, and it is the only card that states a HIGH bar in words. The consensus adopts both as the merge's severity standard (S-006, A-009).
- It is the only card with a recall pass beyond the matrix (R2-G6) and an audit of the matrix itself (R2-G9).
- Its weaknesses are known and bounded: five HIGH ratings that must be replaced by calibrated severity (IC 0.906, K4 NOT MET), the INF-019 delegation reading that is wrong on the CLOSED path (K1 NOT MET), and repo-relative paths and the 0-5 scale not followed (S5 NOT MET). All three are mechanical corrections already agreed in the debate.

### Strengths to Preserve from Base

1. R2-G1 as the first-ranked finding at HIGH, with its one-line fix (count definitions, not references), plus the probe's residual: count constants by their definitions too (INV-020).
2. The evidence format: ref and quote pairs on every finding and a "Success:" criterion on every remediation.
3. The calibrated severity profile, one HIGH, five MEDIUM and three LOW, and the stated HIGH bar ("correct delivery cannot satisfy the check") as the rule for every merged finding.
4. R2-G2, R2-G3, R2-G4 and R2-G6 at calibrated MEDIUM, worded as missing checks or traceability gaps, not observed breaches; R2-G4's note that an import-absence grep cannot prove B5.
5. R2-G9 (INF-017 cites F11, should be F12) and R2-G8 (capture actor), both LOW.
6. The 44 GQ, D, SP and INF row verdicts, with INF-019 changed to partial and INF-024 kept as missing.

Corrections the merge applies to the base (all agreed in Round 2): replace the five original HIGH labels with calibrated severity; change INF-019 from covered-in-substance to partial; fold R2-G5's cursor half into V1's R1-G1 and drop its run-current narrowing; reduce R2-G7 to a LOW fidelity note merged with R1-G9; convert absolute paths to repo-relative and the scale to 0-5.

### Strengths to Incorporate from Non-Base Variants

From V1 (`variant-1-original.md`):
1. R1-G1 (C-001, C-002, X-001, X-002, X-005, A-001), MEDIUM: both unrouted step 1.0a outcomes (a captured cursor field against the ten-template pins at T 1482, 1485, 1793; a CLOSED run-current --json need with no owner route). Drop the `gate-bypass` label and do not claim either "safe stop" or "silent omission" is guaranteed (A-001d).
2. R1-G2 (C-003), MEDIUM with the impact note: the T 1142 pointer to item 6.2 is wrong, but T 1142 spells out both Branches; the residual is Branch 2 in 7.15 and 14.7 not requiring the owner's quoted words.
3. R1-G5 (C-007) and the first sentence of R1-G6 (C-008), LOW: the bare `coder` grep, the unwritten forbidden-list sentence, and echo and ls against the 7.16 Verification.
4. R1-G3 as a LOW clarification only (which fields count as timestamps), and R1-G4 merged with R2-G8 under V2's actor-identity framing.
5. R1-G9 merged with R2-G7 as one LOW fidelity note on design 939 (A-004c).
6. The 76 FR, NFR and design-step row verdicts, marked "item-checked, second ref unreliable": discard the 41 second refs in the design 444 to 484 range and the two "Section 8 gate" refs; keep the step-1.0a partial verdict.
Do not carry: R1-G7 (refuted), R1-G8 (withdrawn), the second sentence of R1-G6.

From V3 (`variant-3-original.md`):
1. R3-G1 with R3-G7 merged in (C-017), MEDIUM: the D10 row cells and the R5 history line omit sections 2.2 and 12 and the SPEC lines.
2. R3-G5 (C-020, X-006, A-005), classified as an authorized expansion with an incomplete record, not scope creep; first remedy only (reword design 221 to allow a recorded owner decision). Severity open: MEDIUM as record integrity, LOW defensible by runtime effect.
3. R3-G6, the 15.1 half only (C-021), MEDIUM, with V3's "ambiguous; costs a fix loop via T 1007" wording and the one-clause fix (write the T 1259 sentence into 15.1). The probe found this fix alone is enough (INV-022).
4. R3-G2 (C-018), R3-G4 (C-019, single-source), R3-G9 narrowed to a missing citation of config.py:64-78 (C-023), R3-G10 (C-024) and R3-G11 (C-025), all LOW.
5. The 32 row verdicts, with the 21 rows that cite only "T1 matrix row" kept tagged [INFERRED] and not counted as independently confirmed.
6. V3's descriptive gap_class vocabulary (design fix, unsound check, traceability, missing reuse, test plan) as the merge's classification labels (S-007), and its written grade scale (S-008).
Do not carry: R3-G3 (withdrawn), R3-G8 (superseded by item 5.4), the second R3-G5 remedy.

Carried from Step 2 as merge obligations, not variant strengths: the debate is BLOCKED_BY_INVARIANTS. The merge must add INV-006 (the item 6.2 `grep -n 'OQ-1 (R5) RESOLVED'` check already matches 3 lines, so correct delivery cannot give "one hit") as a new HIGH and drop the claim that R2-G1 is the only HIGH; must extend the R1-G1 remedy per INV-021 (name the follow-up for an owner approval of an 11th template or `run-current --json`, or state that approval means re-planning before step 1.2); and should review the MEDIUM warnings INV-005, INV-008, INV-015 and INV-018. INV-018 bears directly on items 2 and 4 above: the R3-G5 and R3-G2 remedies edit section 4, so section 4 must be added to the 6.3 Output, the 6.4 checks, the 6.5 to 6.13 inputs, and the R5 and D10 section lists.

Coverage statement the merge may make: the three slices cover 152 of 152 matrix ids with no overlap. The orchestrator re-ran this union check at Step 3 against `coverage-matrix.yaml` (union 152, pairwise overlap 0, no id outside the matrix), so it is no longer a single-advocate report (A-006a, INV-014). The verdicts inside the rows still carry the different weights noted above.
