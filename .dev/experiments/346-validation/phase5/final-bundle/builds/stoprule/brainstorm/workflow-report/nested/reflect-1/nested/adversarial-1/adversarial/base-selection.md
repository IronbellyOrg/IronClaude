# Base Selection: reflect reviewer cards

Scored inline by the orchestrator (debate-orchestrator role) from the three variants, the debate transcript and the invariant probe. "Requirements" for RC are the 19 points the debate settled as real defects (minor or blocking): C-001 to C-006, C-008 to C-016, C-018, C-020, C-021.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 | V2 | V3 | Computation |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.58 | 0.11 | 0.53 | real defects raised / 19 (V1 11, V2 2, V3 10) |
| Internal consistency (IC) | 0.25 | 1.00 | 0.90 | 0.95 | V2 counts drift 2 while not classifying the declared deviations; V3 verdict FAIL on two findings it later conceded to minor |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.85 | 0.90 | concrete file:line findings / substantive statements |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | every finding id referenced is defined |
| Section coverage (SC) | 0.15 | 1.00 | 0.90 | 1.00 | card sections / max |
| **quant_score** | | **0.859** | **0.670** | **0.830** | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

| Dimension | V1 | V2 | V3 | Evidence (CEV, condensed) |
|---|---|---|---|---|
| Completeness (5) | 4 | 1 | 4 | V1 covers ordering, fixture, spec-inherited gaps; V3 covers test-harness layer; V2 two items only; none states out-of-scope explicitly except V3 (R3-10) |
| Correctness (5) | 4 | 3 | 3 | V1 severities closest to the final consensus (only F1/F2/F7 over-graded); V2 QA-001 over-graded; V3 R3-1/R3-2 over-graded and unmapped counts |
| Structure (5) | 4 | 3 | 4 | id/severity/evidence/recommendation per finding (V1, V3); V2 mixes table and YAML |
| Clarity (5) | 4 | 3 | 4 | one-line claims with fix text; V2 clear but sparse |
| Risk coverage (5) | 3 | 1 | 3 | V1 F3/F10 fixture risks; V3 R3-4/R3-5 test-run risks; V2 none beyond its two |
| Invariant & edge-case coverage (5) | 3 | 2 | 2 | V1 F1 state ordering, F9 unclaimed-hunk guard, F5 count; V2 QA-002 withdrawn-prior boundary; V3 R3-2 count |
| **Total / 30** | **22** | **13** | **20** | |
| **qual_score** | **0.733** | **0.433** | **0.667** | |

### Edge Case Floor Check
All three variants score at least 1/5 on invariant and edge-case coverage: all eligible.

## Position-Bias Mitigation
Two orderings (V1, V2, V3 and V3, V2, V1) were scored by the same orchestrator, not by two independent evaluators; no criterion verdict changed between orderings. Recorded as a weaker-than-specified mitigation.

## Combined Scoring

| Variant | quant x 0.5 | qual x 0.5 | Combined |
|---|---|---|---|
| V1 (reviewer-1, analyzer) | 0.430 | 0.367 | **0.796** |
| V3 (reviewer-3, refactorer) | 0.415 | 0.333 | 0.748 |
| V2 (reviewer-2, qa) | 0.335 | 0.217 | 0.552 |

Margin V1 over V3: 4.8 points (within 5%), so the tiebreaker applies. Level 1 (debate points won, scoring matrix): V1 14, V3 9, V2 3. V1 wins.

## Selected Base: Variant 1 (reviewer-1 card, analyzer)

- Selection rationale: highest combined score, best-calibrated severities, and the only card that found the single consensus blocking defect (C-003, Task 7 replay).
- Strengths to preserve: F3 (C-003), F1/F2 ordering findings at corrected severity, F4, F5, F6, F8 to F11, the confirmed declared-deviation classification (authorized and necessary).
- Strengths to incorporate: V2 QA-002 (C-009); V3 R3-3 (C-014), R3-4 (C-015), R3-5 (C-016), R3-6 part (C-013), R3-10 (C-018), R3-12 (C-020), R3-A1 (C-021), R3-1 analysis of the equality-test lock-in (C-004); invariant probe INV-001, INV-002, INV-003, INV-004 (folded into C-003 and C-004) and INV-005 to INV-009 as new MEDIUM items.
