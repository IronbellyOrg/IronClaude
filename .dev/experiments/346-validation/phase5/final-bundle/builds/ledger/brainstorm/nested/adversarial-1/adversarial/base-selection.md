# Base Selection Report

Sources: `scoring-pass1.md` (quantitative layer and qualitative pass 1, order A, B, C), `scoring-pass2.md` (qualitative pass 2, order C, B, A), `scoring-reeval.md` (final verdicts on the 14 criteria the passes disagreed on). Disagreements were found by `/tmp/bs346-tools/passdiff.py` from the two pass files.

Variants: A = `variant-1-opus-architect.md` (opus:architect), B = `variant-2-sonnet-analyzer.md` (sonnet:analyzer), C = `variant-3-haiku-backend.md` (haiku:backend).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A | Variant B | Variant C |
|--------|--------|-----------|-----------|-----------|
| requirement_coverage | 0.30 | 0.958 (11.5/12) | 0.958 (11.5/12) | 0.958 (11.5/12) |
| internal_consistency | 0.25 | 0.957 (1 - 2/46) | 0.940 (1 - 3/50) | 0.935 (1 - 3/46) |
| specificity_ratio | 0.15 | 0.915 (107/117) | 0.970 (195/201) | 0.841 (37/44) |
| dependency_completeness | 0.15 | 1.000 (32/32) | 0.974 (38/39) | 0.938 (15/16) |
| section_coverage | 0.15 | 1.000 (12/12) | 1.000 (12/12) | 1.000 (12/12) |
| **quant_score** | | **0.964** | **0.964** | **0.938** |

Counting details are in `scoring-pass1.md` `## Quantitative`.

## Qualitative Scoring (50% weight), Additive Binary Rubric

Per-criterion Claim-Evidence-Verdict tables: `scoring-pass1.md` and `scoring-pass2.md` `## Qualitative`. Final verdicts = verdicts both passes agreed on (A 21 met, B 24 met, C 19 met) plus the 14 re-evaluated cells in `scoring-reeval.md`.

### Qualitative Summary

| Dimension | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Pass 1 total | 24/30 | 25/30 | 22/30 |
| Pass 2 total | 22/30 | 26/30 | 23/30 |
| Agreed MET | 21 | 24 | 19 |
| Re-evaluated MET (of disputed cells) | 3 of 4 | 1 of 3 | 2 of 7 |
| **qual_score (final)** | **24/30 = 0.800** | **25/30 = 0.833** | **21/30 = 0.700** |

### Edge Case Floor Check

All three variants score at least 3/5 on Invariant and Edge Case Coverage in both passes: all eligible as base.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Dependencies and prerequisites | A | NOT MET | MET | DISAGREE | NOT MET (A keeps `## Unattended mode`, fails `tests/skills/test_worker_contract.py:837`, no fix listed) |
| Feasible with stated constraints | A | MET | NOT MET | DISAGREE | MET (S1 run fits the seed-brief constraints) |
| Feasible with stated constraints | B | NOT MET | MET | DISAGREE | NOT MET (sixth session breaks "same briefs") |
| Consistent terminology | B | NOT MET | MET | DISAGREE | NOT MET (`disputed` as status and as flag; `late` rows with status `open`) |
| Consistent terminology | C | NOT MET | MET | DISAGREE | NOT MET ("deferred" has two meanings) |
| Claims supported by evidence | C | MET | NOT MET | DISAGREE | NOT MET (headline forecast has no basis) |
| Separation of concerns | C | MET | NOT MET | DISAGREE | MET |
| Navigation aids or cross-references | C | NOT MET | MET | DISAGREE | NOT MET |
| Unambiguous language | A | MET | NOT MET | DISAGREE | MET |
| Unambiguous language | B | MET | NOT MET | DISAGREE | MET |
| Each section one clear purpose | C | NOT MET | MET | DISAGREE | MET |
| Terms defined on first use | C | NOT MET | MET | DISAGREE | NOT MET |
| Mitigation per risk | C | MET | NOT MET | DISAGREE | NOT MET |
| Collection boundaries | A | MET | NOT MET | DISAGREE | MET |

Disagreements re-evaluated: 14. Final verdicts changed from pass 1: 3 (all C: evidence MET to NOT MET, mitigation MET to NOT MET, one clear purpose NOT MET to MET); reasons per cell in `scoring-reeval.md`.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (opus:architect) | 0.482 | 0.400 | **0.882** | 12 points won outright |
| B (sonnet:analyzer) | 0.482 | 0.417 | **0.899** | 22 points won outright |
| C (haiku:backend) | 0.469 | 0.350 | **0.819** | 10 points won outright |

**Margin**: B over A 0.017 (1.9%), below the 5% threshold.
**Tiebreaker applied**: Yes, level 1 (debate performance). Points won outright in the final scoring matrix of `debate-transcript.md`: B 22, A 12, C 10 (shared wins: B+C 15, A+C 11, A+B 11; none 4). B wins.

## Selected Base: Variant B (sonnet:analyzer)

### Selection Rationale

B has the highest combined score and wins the debate tiebreaker. It is the only variant that traces the failure in the real review files (minor F22 applied under the brief "apply confirmed findings", which created blocking N5, whose fix created N12), checks that hunk-anchored verification would have caught every review-3 blocker in two traces, gives the convergence bound B1 x r x r, and states plainly that its conservative forecast probably misses the review-3 bar. Its weaknesses (intra-variant X-016 and X-017, the extra sweep session, no FR-8/FR-9 field, a role flag `--as` that proves nothing) are all fixable from A and C, as the Round 2 consensus records.

### Strengths to Preserve from Base

1. Root-cause trace and trace-grounded predictions (B sections 1, 9, 10).
2. Minor rows mechanically unanswerable; `revise-check` and `revert-unclaimed` (B sections 2, 6).
3. Sweep in a fresh session that has not read the ledger; sweep rows classified by location and a hidden-defect share H; baseline sweeps on the six existing final specs (B sections 4, 9).
4. Install naming trap and the copy-plus-drift test with `## Unattended mode` omitted (B section 6).
5. Honest causes table: fix-induced defects LEFT, minor edits REMOVED, mechanisms LEFT (B section 10).
6. No second computed stop for spec-panel, with data (B section 4).

### Strengths to Incorporate from Non-Base Variants

1. From A: kernel, contract and adapter split with a `PROFILES` table, profile-computed `blocking` (fixes X-016), derivable default ledger path, script-written verify plan `plan-r<k>.md`, `E-REPORT-EDITED`, `E-NOT-CHANGED`, V1-ledger validity check, `dup_of` matching, actor inferred from the subcommand (A sections 2, 3, 6, 9).
2. From C: split of `loop_decision` and `delivery_outcome`; `cannot-verify` result; inputs bound to round, document hash and ledger sequence; nonblocking lock plus `--op` and request-digest idempotency; old-side ranges and deletion tombstones; anchor relocation with `anchor_state=missing|ambiguous`; reuse-storage-not-grading adoption rule (C sections 3, 4, 6, 7).
3. From the invariant probe (`invariant-probe.md`): the 27 UNADDRESSED items, of which 9 HIGH, as mandatory fixes in the refactor plan, because the debate convergence gate was blocked by them and depth standard has no Round 3.
