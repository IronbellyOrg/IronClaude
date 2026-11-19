# Base Selection

## Quantitative Scoring (50% weight)

The cards are review documents, so the metrics are applied as follows: RC = share of the 9 content diff points (C-001 to C-009) the card raises; IC = 1 - (intra-card contradictions / claims, as found by the advocates); SR = concrete indicators / (concrete + vague) counted by `grep` over the card; DC = internal references that resolve (plan lines, F-ids, files) / all internal references; SC = H2 sections / the maximum.

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|---|
| RC | 0.30 | 5/9 = 0.556 | 2/9 = 0.222 | 7/9 = 0.778 |
| IC | 0.25 | 0.90 (claims "no under-covered requirement" while F2 shows a gap) | 0.83 (claims "all 16 covered" while F1 shows a verification gap) | 1.00 (its Coverage section matches its findings, apart from the header remark scored below) |
| SR | 0.15 | 1.00 (113 concrete, 0 vague) | 1.00 (29 concrete, 0 vague) | 1.00 (132 concrete, 0 vague) |
| DC | 0.15 | 1.00 | 1.00 | 1.00 (all cited plan lines exist; the plan has 132 lines) |
| SC | 0.15 | 1.00 | 1.00 | 1.00 |
| quant_score | | 0.842 | 0.725 | 0.933 |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Two independent passes scored all 90 criterion-card pairs (pass 1 in order V1, V2, V3; pass 2 in order V3, V2, V1), written to `scoring-pass-1.yaml` and `scoring-pass-2.yaml`. Each MET needs a cited piece of evidence. Limit: both passes were run by agents of the same class (sonnet), and the orchestrator settled the disagreements below, so position-bias control is partial.

### Position-Bias Mitigation

Pass totals: pass 1 gave 26, 20, 28; pass 2 gave 24, 19, 25. The passes disagree on 8 of 90 pairs. Final verdict per disagreement (decided by the orchestrator from both pieces of evidence):

| Criterion | Variant | Pass 1 | Pass 2 | Final | Reason |
|---|---|---|---|---|---|
| completeness.5 | V1 | MET | NOT_MET | NOT_MET | "Not read" is a statement of limits, not an out-of-scope statement |
| correctness.4 | V1 | MET | NOT_MET | MET | Advocate 1 verified the stale clause is in three places (issue.md:44, :48 and commands.md:371), so F1 is consistent |
| completeness.1 | V2 | NOT_MET | MET | NOT_MET | Its advocate conceded the "all 16" claim needs qualifying |
| completeness.5 | V2 | MET | NOT_MET | NOT_MET | same as V1 |
| clarity.4 | V2 | MET | NOT_MET | MET | "Tier 1 card" and task numbers are the plan's own vocabulary, named in the checked list |
| correctness.4 | V3 | MET | NOT_MET | NOT_MET | The header says every other unit is covered while Coverage lists two partial ones |
| clarity.4 | V3 | MET | NOT_MET | NOT_MET | "st7" and "st9" are used without a definition |
| risk_coverage.4 | V3 | MET | NOT_MET | MET | F4 covers the failed worktree and failed launch paths, which depend on Orca |

Verdicts changed by re-evaluation: 3 of 8 (V1 completeness.5, V2 completeness.5, V3 correctness.4 and clarity.4 move away from pass 1; the rest stay).

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|
| Completeness | 4 | 2 | 5 |
| Correctness | 5 | 5 | 4 |
| Structure | 5 | 5 | 5 |
| Clarity | 4 | 5 | 4 |
| Risk Coverage | 3 | 2 | 4 |
| Invariant & Edge Case Coverage | 4 | 0 | 4 |
| Total (of 30) | 25 | 19 | 26 |
| qual_score | 0.833 | 0.633 | 0.867 |

(The per-dimension counts are the pass 1 counts adjusted by the final verdicts above.)

### Edge Case Floor Check

Variant 2 scores 0 of 5 on invariant and edge-case coverage, below the 1 of 5 floor, so it is ineligible as base. Variants 1 and 3 score 4 of 5 and are eligible.

## Combined Scoring

| | Quant (50%) | Qual (50%) | Combined |
|---|---|---|---|
| Variant 3 | 0.933 | 0.867 | **0.900** |
| Variant 1 | 0.842 | 0.833 | 0.838 |
| Variant 2 | 0.725 | 0.633 | 0.679 (ineligible) |

Margin between the top two: 6.3%, above the 5% tiebreaker trigger, so no tiebreaker was applied. Debate performance agrees: variant 3 won 9 of the 17 points outright or by majority (S-001, S-002, C-002, C-003, C-005, C-008, C-009, X-002, X-003).

## Selected Base: Variant 3 (opus, refactorer)

- Selection rationale: highest combined score (0.900), the widest coverage of the content differences (7 of 9), and the only card whose findings the debate confirmed against live files on every contested point.
- Strengths to preserve: the seven findings with explicit fixes; the Coverage section that names the two partly covered spec units; the Checked section on step renumbering and pinned tests.
- Strengths to incorporate from non-base cards:
  - Variant 2: the test gap that nothing asserts the final output repeats the `Level:` line, with an assertion and a mutation check (C-004, U-002).
  - Variant 1: the `-k` filter that selects nothing for `worker_contract` (C-007, U-005).
  - Variant 1: the narrower fix for the stored-level case: print the `Level:` line for `launched` only and pin one phrase (C-003).
  - Variant 1: the explicit note that line 92 of `SKILL.md` stays true (C-006), already present in the base as F5.
