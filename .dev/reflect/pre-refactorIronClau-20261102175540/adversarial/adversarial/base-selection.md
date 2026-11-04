# Base Selection

## Quantitative Scoring (50% weight)

Computed deterministically by script over variant-N-original.md (concrete-indicator and vague-word regexes; section count = top-level YAML keys; requirement coverage = plan tasks addressed by findings, section-level topic matching because the spec has no requirement IDs; internal consistency from contradictions noted in blind calibration).

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|--------|--------|-----------|-----------|-----------|
| Requirement coverage (RC): tasks addressed / 7 | 0.30 | 0.571 (Tasks 1, 3, 4, 7) | 0.571 (Tasks 1, 3, 6, 7) | 0.571 (Tasks 1, 2, 3, 6) |
| Internal consistency (IC) | 0.25 | 0.900 (1 of 10: R1-3 labelled necessary while describing a labelling defect) | 1.000 (0 of 8) | 0.875 (1 of 8: R3-F4 labelled drift while saying it will most likely pass) |
| Specificity ratio (SR) | 0.15 | 1.000 (66 concrete, 0 vague) | 1.000 (41 concrete, 0 vague) | 0.966 (112 concrete, 4 vague) |
| Dependency completeness (DC) | 0.15 | 1.000 (no internal refs) | 1.000 (no internal refs) | 1.000 (2 of 2 resolved) |
| Section coverage (SC) | 0.15 | 0.750 (6 of 8) | 1.000 (8 of 8) | 0.750 (6 of 8) |
| **quant_score** | | **0.809** | **0.871** | **0.798** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Two independent read-only passes: `qualitative-pass1.md` (order 1, 2, 3) and `qualitative-pass2.md` (order 3, 2, 1). Every MET verdict carries a citation in the pass files.

### Qualitative Summary (final, after disagreement resolution)
| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant | Total/30 | qual_score |
|---|---|---|---|---|---|---|---|---|
| 1 | 4 | 5 | 5 | 4 | 5 | 4 | 27 | 0.900 |
| 2 | 3 | 3 | 5 | 4 | 3 | 3 | 21 | 0.700 |
| 3 | 4 | 4 | 5 | 4 | 5 | 4 | 26 | 0.867 |

### Edge Case Floor Check
All three variants score 4/5 or 3/5 on Invariant & Edge Case Coverage (>= 1/5): all eligible as base.

## Position-Bias Mitigation

Pass 1 arithmetic note: pass 1 reported Variant 3 = 27, but its own dimension subtotals (4+4+5+4+5+4) sum to 26; the corrected figure is used.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation basis |
|-----------|---------|--------|--------|-----------|-------|---------------------|
| C1 | 2 | NOT MET | MET | No | NOT MET | `missing_requirements: []` is wrong (eval_runner.py:143) and C-001 was missed; same standard applied to Variants 1 and 3 (both NOT MET) |
| T1 | 2 | MET | NOT MET | No | MET | Card order is findings, missing requirements, disputes, inferred claims; the criterion concerns section order, which is logical |
| E1 | 2 | NOT MET | MET | No | NOT MET | An empty `missing_requirements` list is not collection-boundary analysis of the subject; Variants 1 and 3 both NOT MET on the same basis |
| K3 | 3 | NOT MET | MET | No | NOT MET | All six labelled drift; its own advocate conceded R3-F1 is a spec gap and R3-F4 a coverage gap (round2-v3.md) |
| L4 | 3 | NOT MET | MET | No | MET | R3-F1 glosses INF-003 inline as "every tracked file" (variant-3-original.md, R3-F1 rationale) |
| L1 | 3 | MET | NOT MET | No | NOT MET | R3-F1 ("likely a fifth internal-checkout case or a project-worktree rewrite"), R3-F5 and R3-F6 end in either/or recommendations |
| R3 | 3 | MET | NOT MET | No | MET | R3-F5 gives a recovery ("removed after the scan" or reclassify) and R3-F2 gives a fallback check; weak but present |

- disagreements_found: 7
- verdicts_changed relative to pass 1: 2 (Variant 3 L4 NOT MET -> MET; Variant 3 L1 MET -> NOT MET); relative to pass 2: 5 (Variant 2 C1, T1, E1; Variant 3 K3, R3)
- Final totals: Variant 1 = 27 (both passes agree), Variant 2 = 21 (pass 1), Variant 3 = 26 (corrected pass 1 and pass 2 agree on the total, differ on which criteria)

## Combined Scoring

| Variant | quant x 0.50 | qual x 0.50 | Combined |
|---------|--------------|-------------|----------|
| 1 | 0.4045 | 0.4500 | **0.8545** |
| 2 | 0.4355 | 0.3500 | 0.7855 |
| 3 | 0.3990 | 0.4335 | 0.8325 |

- Margin between top two (Variant 1 vs Variant 3): 0.022 (< 0.05), so the tiebreaker applies.
- Tiebreaker level 1 (debate points won, debate-transcript.md scoring matrix): Variant 1 wins 4 (S-002, S-003, C-001, C-003); Variant 2 wins 3 (S-001, C-005, X-001); Variant 3 wins 2 (X-002, A-003); ties: C-002, C-004, A-001, A-002. Variant 1 > Variant 3. Decided at level 1.

## Selected Base: Variant 1 (reviewer-1, sonnet, analyzer)

### Selection rationale
Highest combined score (0.8545) and the most debate points won. Its classifications use the 4-category taxonomy correctly, it has no factual errors (K1 MET in both passes), and it alone covers both pre-PR checks (CLAUDE.md:64 and :66), the consensus winner of C-001 at 97% confidence.

### Strengths to preserve
- R1-1 (both pre-PR checks, stop-and-report rewrite, grep acceptance check).
- R1-2 necessary-deviation class with the Blocked status of POST-REFLECT-TASK.md.
- R1-3 label fix; R1-5 decision on CLAUDE.md:251.

### Strengths to incorporate
- From Variant 3: R3-F1 (scripts/eval_runner.py, X-002 winner, 97%); R3-F3, R3-F4, R3-F5 (unique, real); the A-003 zero-skip qualification (A-003 winner, 92%).
- From Variant 2: explicit coverage/missing-requirements section (S-001 winner); C-005 reading that the fetch/pull ban is not a deviation (C-005 winner, 95%); X-001 majority reading (62%, contested) plus the fixture citation test_implement_retry_revert.py:613 for R1-4.
- From the invariant probe (not a variant, but blocking/warning items that the merged verdict must carry): INV-005 (HIGH), INV-001, INV-003, INV-004, INV-006, INV-008, INV-009, INV-010, INV-011 (MEDIUM), INV-002, INV-014 (LOW).
