# Base Selection

Requirement set for RC: spec AC1-AC8 + RF1-RF12 = 20 items. Every score below was checked against the CURRENT tasklist (954add6c). Both cards reviewed the superseded 9d4d00ed revision.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (sonnet:analyzer) | V2 (haiku:qa) | Computation notes |
|--------|--------|------------------|---------------|-------------------|
| Requirement coverage (RC) | 0.30 | 0.35 | 0.25 | V1 evidences RF2, RF3, RF6, RF8, RF9, RF11, AC7 = 7/20. V2 evidences RF11, RF12, AC3, AC5, AC6 = 5/20. |
| Internal consistency (IC) | 0.25 | 1.00 | 1.00 | Neither card contradicts itself. Each verdict matches the severity of its own findings. |
| Specificity ratio (SR) | 0.15 | 1.00 | 1.00 | Every claim cites a line or a literal. |
| Dependency completeness (DC) | 0.15 | 1.00 | 0.67 | V1's T:50/T:56 citations resolve in the current file. V2's :62 citation now points at the TARGET-header AC, not at step 5, so 2/3 resolve. |
| Section coverage (SC) | 0.15 | 1.00 | 0.80 | Top-level keys: 10 in V1, 8 in V2. |
| **quant_score** | | **0.805** | **0.695** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric

The table gives MET counts per dimension. The CEV evidence summary records the deciding citation for each criterion.

| Dimension | V1 | V2 | Key CEV evidence |
|-----------|----|----|------------------|
| Completeness | 3/5 | 2/5 | V1 met: explicit reqs partly (prior-findings ledger), dependencies (baseline_checks), completion criteria (verdict + resolved flags). V2 met: edge cases (wrong-implementation lens), completion criteria. Neither card covers out-of-scope. |
| Correctness | 3/5 | 3/5 | Neither card hallucinates against the revision it saw, and both use terminology consistently. Neither card is consistent with the current file: A1 and QA-1..3 are all stale no-ops. V1 also failed to notice the gaps that V2 found. V2's citations no longer resolve. |
| Structure | 3/5 | 3/5 | Both follow the reviewer-card schema, with logical ordering and clear separation. Neither has navigation aids. |
| Clarity | 4/5 | 3/5 | Both are unambiguous and concrete. V1's actions are explicit through recommended_change and resolved flags. V2's coverage_gaps uses "not proven", which is abstract. |
| Risk coverage | 1/5 | 2/5 | V1 met: validation mechanism (baseline_checks). V2 met: failure modes (unconditional WARN, non-deep step 5) and a detection mechanism (proposed tests). Neither card scores probability or impact. |
| Invariant & edge case | 1/5 | 1/5 | V1 met: guard-condition gap (Wave 0 slicing for ordering, the predicate). V2 met: guard-condition gap (depth condition, deep-only guard). |
| **qual_score** | **15/30 = 0.500** | **14/30 = 0.467** | |

### Edge Case Floor Check
Both variants scored 1/5, so both are eligible.

## Position-Bias Mitigation
The orchestrator ran two passes: input order (V1→V2) and reverse order (V2→V1). The passes had 0 disagreements and changed 0 verdicts.

## Combined Scoring

| Variant | Quant ×0.5 | Qual ×0.5 | Final |
|---------|-----------|-----------|-------|
| V1 | 0.403 | 0.250 | **0.653** |
| V2 | 0.348 | 0.233 | **0.581** |

The margin is 7.2%, above the 5% tiebreaker threshold, so no tiebreaker was applied. In the debate V1 won 3 points (C-001, X-001, X-002) and V2 won 3 points (C-002, C-003, C-004).

## Selected Base: Variant 1 (sonnet:analyzer)

**Selection rationale.**
- V1's verdict (`approve`) and `coverage_gaps: []` are correct for the current tasklist, and both advocates agreed on this (X-001, X-002).
- V1's 9-item prior-findings ledger and its baseline checks are the only audit trail showing that the earlier review rounds stayed closed.

**Strengths to preserve.** V1's verdict, its prior_findings_resolved ledger and its baseline_checks.

**Strengths to incorporate from V2.**
- Record QA-1, QA-2 and QA-3 as valid findings that the tasklist has already applied, with the current line evidence.
- Record V2's three coverage gaps as closed.

**Base weaknesses to fix.**
- target_tasklist_sha256 is stale.
- A1 should be marked as applied.
- The card should carry a note that the review was done against a superseded revision.
