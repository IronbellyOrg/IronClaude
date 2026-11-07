# Base Selection

Orchestrator scoring, 2026-11-06T22:14:00Z. "Source requirements" for RC are the 15 inferred requirement rows in `../artifacts/coverage-matrix.yaml` (the spec has no formal IDs, so topic matching is used: a row counts when the variant's findings or clean list check it).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 | Computation |
|--------|--------|-----------|-----------|-----------|-------------|
| Requirement coverage (RC) | 0.30 | 0.87 (13/15) | 0.60 (9/15) | 0.63 (9.5/15; INF-004 partial) | V1 misses INF-014, INF-015; V2 misses INF-001, -002, -003, -007, -012, -015; V3 misses INF-009..INF-014 except partial INF-004 |
| Internal consistency (IC) | 0.25 | 1.00 | 1.00 | 1.00 | No intra-card contradiction found (cross-card contradictions are X-001..X-003) |
| Specificity ratio (SR) | 0.15 | 0.95 | 0.90 | 0.93 | Concrete file:line claims vs hedged ones; V2 tags QA-1 [INFERRED] |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | Named helpers verified: `test_every_repo_setup_line_is_gated` :573, `_patched_copy` :580 |
| Section coverage (SC) | 0.15 | 0.60 (3/5) | 0.80 (4/5) | 1.00 (5/5) | Top-level blocks: V1 findings, checked, calibration; V2 + limitations; V3 findings, advisory, checked, not_checked, calibration |
| **quant_score** | | **0.894** | **0.835** | **0.879** | (RC×0.30)+(IC×0.25)+(SR×0.15)+(DC×0.15)+(SC×0.15) |

## Qualitative Scoring (50% weight): Additive Binary Rubric

CEV summary per dimension (MET counts; evidence is the card text plus the debate rounds).

### Completeness (5)
- V1: 4. Covers requirements (13/15), edge cases (R1-5 dry-run/partial/audit failure), dependencies (init_lite.py), success criteria (verifiers on every finding). NOT MET: out-of-scope statement (none).
- V2: 2. MET: success criteria (verifiers), edge case (QA-1 witness). NOT MET: requirement coverage (9/15), dependencies, out of scope (limitations section is about method, not scope).
- V3: 4. MET: dependencies (spec copy), out of scope (R3-A2 marked out of brief), success criteria, edge cases (R3-A3). NOT MET: covers all requirements (missed Task 5).

### Correctness (5)
- V1: 4. NOT MET: "no factual errors" (clean claim "No other test or mirror pins" narrower than the brief, conceded Round 2).
- V2: 3. NOT MET: no factual errors (Task 5 clean claim wrong in premise, withdrawn); claims supported (QA-2 grade overstated, conceded).
- V3: 4. NOT MET: terminology/grades consistent (R3-A1 calibrated P2 but filed advisory, conceded).

### Structure (5)
- V1: 4; V2: 4; V3: 5 (separate gating vs advisory blocks, not_checked declared). NOT MET for V1/V2: navigation aid (no gating/advisory split).

### Clarity (5)
- V1: 4; V2: 4; V3: 4. Each NOT MET: acronyms (AC, WC-n) not defined on first use.

### Risk Coverage (5)
- V1: 3 (risks R1-1, R1-2, R1-5 with mitigations; no monitoring; no external-dependency failure).
- V2: 2 (QA-1, QA-2 with mitigations; fewer than 3 risks).
- V3: 4 (R3-1, R3-3, R3-A1, R3-A2, R3-A3 with mitigations; external dependency = spec/history; NOT MET: monitoring).

### Invariant & Edge Case Coverage (5)
- V1: 4 (collection boundary `[]`/dry-run, state across line layout (R1-6), guard gaps (R1-1), interaction (R1-2)); NOT MET: count divergence.
- V2: 3 (guard gap QA-1, collection `[]`, guard on scan roots QA-2).
- V3: 3 (state: spec copy drift, guard: slice, interaction: R3-A1).

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 4 | 2 | 4 |
| Correctness | 4 | 3 | 4 |
| Structure | 4 | 4 | 5 |
| Clarity | 4 | 4 | 4 |
| Risk Coverage | 3 | 2 | 4 |
| Invariant & Edge Case | 4 | 3 | 3 |
| **Total / 30** | **23 (0.767)** | **18 (0.600)** | **24 (0.800)** |

### Edge Case Floor Check
All variants score at least 1/5 on Invariant & Edge Case Coverage: all eligible.

## Position-Bias Mitigation

| Pass | Order | Disagreements | Verdicts changed |
|------|-------|---------------|------------------|
| 1 | V1, V2, V3 | | |
| 2 | V3, V2, V1 | 2 (V3 Completeness criterion 1; V1 Structure criterion 4) | 1 |

Re-evaluation: V3 Completeness c1 stays NOT MET (Task 5 not checked, its own `not_checked`); V1 Structure c4 stays NOT MET. Pass 2 first scored V3 Structure 4; re-evaluated MET (the separate advisory block is a navigation aid) -> 5. Final verdicts as tabled.

## Combined Scoring

| Variant | Quant ×0.5 | Qual ×0.5 | Final |
|---------|-----------|-----------|-------|
| V1 (sonnet:analyzer) | 0.447 | 0.383 | 0.830 |
| V2 (haiku:qa) | 0.418 | 0.300 | 0.718 |
| V3 (opus:refactorer) | 0.440 | 0.400 | 0.840 |

Margin V3 over V1: 0.010 (1.2%), within 5%: tiebreaker applied.
- Level 1 (debate points won, shared = 0.5): V3 5.5, V1 5.0. V3 wins by 10%, so Level 1 decides.

## Selected Base: Variant 3 (opus:refactorer)

- **Selection rationale:** highest combined score after tiebreaker; its card shape (gating findings, a separate non-gating block, explicit not_checked) is the right container for a merged verdict, and it holds the scope findings (R3-1, R3-A1) the others missed.
- **Strengths to preserve:** R3-1 (spec copy, recorded-decision fix), R3-3 (WC-4 slice), R3-4 and R3-5 (single-source notes), advisory block (R3-A2).
- **Strengths to incorporate:** from V1: R1-1 (P1, status assertion), R1-2 (narrowed workflow conflict, merged with R3-A1), R1-3 (better AC3 replacement, qualified by INV-009), R1-5 (exit-path verification); from V2: QA-1 (P1, narrowed to "left out"); from the probe: INV-001, INV-003, INV-005, INV-006, INV-007 (MEDIUM), INV-002, INV-004, INV-010, INV-011, INV-016 (LOW).
