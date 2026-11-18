# Base Selection

## Quantitative Scoring (50% weight)

Source requirements (RC denominator = 20 checks a complete card must cover): the nine first-review statuses F1-F9 plus the eleven plan findings the debate confirmed as real (C-001 to C-010 and C-012). Metrics SR, DC and SC were computed by script `/tmp/reflect2s1_quant.py` (concrete-indicator and vague-word counts; resolved finding-id references; H2 section counts); RC and IC were counted by the orchestrator.

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| RC requirement coverage (V1 16 of 20: F1-F9, C-001 to C-006, C-009; V2 13 of 20: F1-F9, C-001, C-006, C-007, C-008; V3 17 of 20: F1-F9, C-001 to C-006, C-010, C-012) | 0.30 | 0.8000 | 0.6500 | 0.8500 |
| IC internal consistency (1 minus contradictions over claims: V1 1 of 15 (X-003); V2 1 of 14 (X-004, charged by the Pass 1 scorer, cleared on re-evaluation but counted here conservatively); V3 0 of 15) | 0.25 | 0.9333 | 0.9286 | 1.0000 |
| SR specificity ratio (script: 70, 32, 65 concrete lines; 0 vague lines each) | 0.15 | 1.0000 | 1.0000 | 1.0000 |
| DC dependency completeness (finding-id references resolved: 14/14, 10/10, 16/16) | 0.15 | 1.0000 | 1.0000 | 1.0000 |
| SC section coverage (6 H2 sections each) | 0.15 | 1.0000 | 1.0000 | 1.0000 |
| **quant_score** | | **0.9233** | **0.8771** | **0.9550** |

## Qualitative Scoring (50% weight): additive binary rubric (30 criteria)

Two independent scorer agents (general-purpose, sonnet class): Pass 1 evaluated V1, V2, V3; Pass 2 evaluated V3, V2, V1. Each used the debate outcome as ground truth for correctness. Per-criterion verdicts below, order C1-C5 / R1-R5 / S1-S5 / L1-L5 / K1-K5 / E1-E5 (M = MET, N = NOT MET); evidence of at most 12 words per verdict was returned by the scorers with the CEV rule (no evidence, no MET).

| Variant | Pass | C | R | S | L | K | E | Total |
|---|---|---|---|---|---|---|---|---|
| V1 | 1 | MMMMM | MMMNM | MMMMM | MMMNM | MMMMM | MMMMM | 28 |
| V1 | 2 | MMMMM | MMMNM | MMMMM | MMMNM | MMMMM | MMMMM | 28 |
| V2 | 1 | MMMMM | NMMNN | MMMMM | MMMNM | MMMMM | MMMMN | 25 |
| V2 | 2 | MMMMM | MMMMN | MMMMM | MMMNM | MMMMM | MMMMN | 27 |
| V3 | 1 | MMMNM | MMMMM | MMMMM | MMMNM | MMMMM | MMMMM | 28 |
| V3 | 2 | MMMMM | MMMMM | MMMMM | MMMNM | MMMMM | MMMMM | 29 |

Not-met items that both passes agree on: V1.R4 (header "All nine first-review fixes are in the live plan" contradicts its own F1 and F5 lines), V1.L4, V2.R5 (grades of R2-F2 and R2-F3 BLOCKING, which the debate settled as NON-BLOCKING), V2.L4, V2.E5, V3.L4 (PLAN, SPEC, T-numbers used without definition).

### Qualitative Summary: position-bias resolution
Disagreements found: 3 criterion-variant pairs (V2.R1, V2.R4, V3.C4). Each was re-evaluated with both pieces of evidence and the debate outcome:
- V2.R1 ("no factual errors"): MET on re-evaluation. R2-F2 and R2-F3 state facts about PLAN:159/164 versus SPEC:512/516 that the debate confirmed as real gaps; the "independently confirmed" bytecode claim is true (A1 and A3 re-ran the grep). The over-grade is charged to R5, not R1.
- V2.R4 ("no internal contradictions"): MET on re-evaluation. X-004 was settled as not a defect by all three advocates (file inspection is not a command).
- V3.C4 ("defines completion criteria"): MET on re-evaluation, consistent with V1.C4 (a verdict plus the exact fix for the blocking item).
Verdicts changed from Pass 1 by re-evaluation: 3. Final: V1 28/30, V2 27/30, V3 29/30.

### Edge Case Floor Check (dimension E, floor 1 of 5)
V1 5, V2 4, V3 5: all eligible.

## Position-Bias Mitigation
Dual-pass done (forward and reverse); results above.

## Combined Scoring

| Variant | quant (x0.50) | qual (x0.50) | combined |
|---|---|---|---|
| V1 | 0.9233 | 0.9333 (28/30) | 0.9283 |
| V2 | 0.8771 | 0.9000 (27/30) | 0.8886 |
| V3 | 0.9550 | 0.9667 (29/30) | **0.9608** |

Margin V3 over V1: 3.25 percent, under the 5 percent tiebreaker trigger. Tiebreaker level 1 (debate points won in the Scoring Matrix of `debate-transcript.md`, exclusive wins): V3 6 (C-002, C-003, C-010, C-012, X-001, X-003), V1 3 (C-004, C-009, X-002), V2 2 (C-007, C-008). V3 wins at level 1 (consistent with the combined score). Judge class note: the scorers are sonnet class and Variant 1's reviewer is sonnet class (the same collision as the first run; haiku and opus classes are also advocate classes, so no disjoint class exists): `judge_class_collision: true`.

## Selected Base: Variant 3 (reviewer 3, refactorer persona, opus class)

### Selection rationale
Highest combined score (0.9608), the widest coverage of confirmed plan findings (17 of 20), no internal contradiction, the correct single blocking grade, evidence for the blocking defect on disk, and a "Not checked" disclosure.

### Strengths to preserve
Its first-review table with plan lines, the R3-F1 blocking finding with consequence and exact fix, R3-F2 to R3-F6 (non-blocking), the "Checked and found sound" list, the "Not checked" paragraph.

### Strengths to incorporate from non-base variants
- V1: R1-F4 (the `classifier` column target; update call); the multi-path `defining file` cell separator inside R1-F2; the load-by-path resolver fix for R1-F5 (replaces V3's subprocess fix, conceded by A3); the label "F5 partly fixed".
- V2: R2-F2 (M presence-by-name precheck) and R2-F3 (D decision-basis input), re-graded NON-BLOCKING after Round 2 (A1 and A3 agreed; A2 withdrew BLOCKING); R2-F5 (`verify-citations`) already in V3's R3-F6.
- Debate outputs: A-002 qualification ("fails under default settings"); INV-001 (the PLAN:125 fix must say "lists no file other than `follow_ups.py`" and cover both sentences); INV-004 (Tasks 4 and 5 lack a `src/superclaude` check although the copied spec text holds two such paths); INV-006 (tasklist count 9 lines, not 7), INV-010 (the importer list has no end point beyond stage 1), INV-013 (lint check 11 and a `THRESHOLDS` constant).
- Drop: V2's R2-F4 (concerns the review's own matrix, not the plan), V1's X-003 header wording.
