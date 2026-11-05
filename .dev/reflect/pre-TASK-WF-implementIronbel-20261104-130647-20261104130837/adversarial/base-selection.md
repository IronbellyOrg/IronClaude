# Base Selection

Evaluator: orchestrator (debate-orchestrator role), two passes (input order V1, V2, V3; reverse order V3, V2, V1). Variants are reviewer cards, so "requirements" are the 18 content topics C-001..C-018 from diff-analysis.md.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 | V2 | V3 | Computation |
|--------|--------|----|----|----|-------------|
| Requirement coverage (RC) | 0.30 | 0.72 | 0.33 | 0.61 | topics covered / 18 (V1 13, V2 6, V3 11) |
| Internal consistency (IC) | 0.25 | 1.00 | 1.00 | 0.91 | 1 - contradictions/claims (V3: F3 vs F10 grading, 1/11) |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.85 | 0.90 | concrete fix/evidence statements / substantive statements |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | internal finding refs resolve (R2-F5 verified in Round 2) |
| Section coverage (SC) | 0.15 | 1.00 | 0.55 | 1.00 | finding count / max (11) |
| **quant_score** | | **0.901** | **0.709** | **0.846** | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

| Dimension | V1 | V2 | V3 | CEV notes |
|-----------|----|----|----|-----------|
| Completeness (5) | 4 | 2 | 3 | V1 covers plan-integrity and tokenizer; V2 misses tokenizer; V3 misses C-002, C-013, C-014 |
| Correctness (5) | 4 | 4 | 3 | V1 under-graded R1-F5 (conceded); V3 F3/F10 inconsistency, X-001 overstated (conceded); V2 accurate but narrow |
| Structure (5) | 4 | 3 | 4 | all one finding per row; V2 lacks fixes on F5, F6 |
| Clarity (5) | 4 | 3 | 4 | concrete fixes in V1, V3 |
| Risk Coverage (5) | 3 | 2 | 5 | V3 uniquely covers Task 7 permission scope, quote desync, fail-open by construction |
| Invariant & Edge Case (5) | 3 | 1 | 4 | V3: heredoc, comments, continuation, nested substitution; V1: continuation, wrappers; V2: jq-missing only |
| **Total (30)** | **22** | **15** | **23** | |
| **qual_score** | **0.733** | **0.500** | **0.767** | |

### Edge Case Floor Check
All variants score >= 1/5 on Invariant & Edge Case Coverage; all eligible.

## Position-Bias Mitigation
Pass 1 (V1, V2, V3) and pass 2 (V3, V2, V1) agreed on every dimension total except V1 Risk Coverage (pass 1: 3, pass 2: 2). Re-evaluation with both evidence sets: 3 (V1 names the fail-open tokenizer leak R1-F6 and the jq/flaky risks). Disagreements found: 1; verdicts changed: 0.

## Combined Scoring

| Variant | quant x 0.5 | qual x 0.5 | Score |
|---------|-------------|------------|-------|
| V1 (sonnet:analyzer) | 0.451 | 0.367 | 0.817 |
| V3 (opus:refactorer) | 0.423 | 0.383 | 0.806 |
| V2 (haiku:qa) | 0.355 | 0.250 | 0.605 |

Margin V1 vs V3: 1.1% (< 5%) -> tiebreaker applied.
- Level 1 (debate points won): V1 wins C-001, C-002, C-005, C-009, C-012, C-013, C-014, C-018, X-001 (9); V3 wins C-003, C-004, C-006, C-007, C-008, C-011, C-015, C-016, X-002 (9); X-003 split. Tie.
- Level 2 (correctness criteria MET): V1 4, V3 3 -> V1.

## Selected Base: Variant 1 (sonnet:analyzer)

- Selection rationale: highest combined score; wins the correctness tiebreaker; severity discipline matched the plan's own documented decisions (calibrated deviation-classification 0.70 vs V3 0.55).
- Strengths to preserve: R1-F1 diagnosis; R1-F2 allowed `;` cases; R1-F7 dependency order; R1-F10 default-HOME install test; R1-F3 refinement note; R1-F8 Goal wording and template line 965.
- Strengths to incorporate: V3's tokenizer findings as one scanner amendment (R3-F2 desync half, R3-F3 desync half, R3-F5, R3-F7, R3-F9, R3-F10, R3-F11, Round 2 commit-form evidence); V2's jq-missing PATH-shim test (R2-F3) and coverage-matrix note (R2-F5); the invariant-probe findings INV-001..INV-017 and INV-019, INV-021, INV-022, INV-026 as implement-time amendments or documented ceilings.
