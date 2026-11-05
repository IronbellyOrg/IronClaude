# Base Selection

Evaluator: orchestrator (single evaluator; Pass 1 input order V1, V2; Pass 2 reverse order V2, V1; verdicts agreed on every criterion, no re-evaluation needed). Inputs: variants, diff-analysis.md, debate-transcript.md, invariant-probe.md, independent calibrations (V1 C 0.85, V2 C 0.78).

## Quantitative Scoring (50% weight)

Source topics for RC (section-level, no formal IDs): Tasks 1-5, AC1-AC6, HC1, HC5 = 13 topics.

| Metric | Weight | V1 | V2 | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.92 (12/13: all but AC4) | 0.85 (11/13: misses Task 2, Task 3) | topics addressed by at least one finding or verified statement |
| Internal consistency (IC) | 0.25 | 1.00 | 1.00 | no self-contradiction found in either card |
| Specificity ratio (SR) | 0.15 | 0.95 | 0.95 | nearly every statement carries file:line or a concrete value |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | internal references (F-ids, rows, INF ids) resolve |
| Section coverage (SC) | 0.15 | 0.67 (2 blocks) | 1.00 (3 blocks) | findings table + checked list vs table + adherence + answers |
| **quant_score** | | **0.919** | **0.948** | (RC×0.30)+(IC×0.25)+(SR×0.15)+(DC×0.15)+(SC×0.15) |

## Qualitative Scoring (50% weight) — Additive Binary Rubric (CEV, condensed)

| Dimension | V1 met | V2 met | Decisive evidence |
|---|---|---|---|
| Completeness (5) | 4 | 3 | V1: whole-plan scope, deps (F10 install tests), success criteria (F4 order), out-of-scope (F7 "do not add a new test"); misses spec-to-plan completeness. V2: completeness check (variant-2 "every requirement-bearing span"), declared residual; misses Tasks 2-3, edge cases. |
| Correctness (5) | 4 | 4 | V1: 12/12 confirmed; hedged F3 label costs one. V2: 5/6 confirmed, row 1 overstated. |
| Structure (5) | 4 | 4 | both tabular and ordered; V2 lacks a recommendation column (V1 lacks counts) |
| Clarity (5) | 4 | 3 | V1 actionable recommendations per finding; V2 names gaps without next steps |
| Risk Coverage (5) | 3 | 1 | V1: F1, F3, F5 risks with mitigation (3 risks + mitigation + monitoring via pid check); V2: no mitigations |
| Invariant & Edge Case (5) | 3 | 2 | V1: guard gaps (F7), state interaction (F3), cleanup boundaries (F6); V2: phase-ordering state, contingent grep equivalence |
| **Total** | **22/30 = 0.733** | **17/30 = 0.567** | |

Edge-case floor (≥1/5): both eligible.

## Position-Bias Mitigation

| Pass | Order | Result |
|---|---|---|
| 1 | V1, V2 | V1 22, V2 17 |
| 2 | V2, V1 | V2 17, V1 22 |
Disagreements found: 0. Verdicts changed: 0.

## Combined Scoring

| Variant | Quant ×0.5 | Qual ×0.5 | Score |
|---|---|---|---|
| V1 | 0.460 | 0.367 | **0.826** |
| V2 | 0.474 | 0.283 | **0.757** |

Margin 6.9 percentage points (> 5%): no tiebreaker. Debate tally agrees (V1 won 13 of 20 points unanimously, V2 4, TIE 3).

## Selected Base: Variant 1 (reviewer-1-card, analyzer)

- Selection rationale: wider risk coverage with concrete mitigations (F1, F3, F4, F5), every finding actionable, calibrated 0.85 with 12/12 findings confirmed.
- Strengths to preserve: F1, F3, F4, F5, F7, F8, F10, the "checked and aligned" list.
- Strengths to incorporate from Variant 2: after.txt redirect (C-006, as LOW), spec-to-plan completeness check (C-014), HC5 as Drift (X-002), contingent grep equivalence (C-003), adherence counts (U-010).
- Weaknesses to fix (from debate concessions and the invariant probe): F2 severity -> LOW; F5 recommendation (fixture runs SKILL_DIR's proxy; check /proc/<pid>/stat state or the port rather than `kill -0`, INV-004); F3 category hedge; add INV-001 and INV-002 (MEDIUM) and the LOW residuals INV-003, INV-010, INV-011, INV-013 and the inherited-descriptor note.
