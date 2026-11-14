# Base Selection Report (Q27)

Scored by the orchestrating worker in-context. Requirements used for coverage (7): (1) gives a direct answer on #539; (2) the plan can be executed by its executor as written; (3) no dependency on Q26; (4) level-3 routing (`~/.claude/CLAUDE.md`); (5) stays inside A-004 and rule 15 (`merged-requirements.md:978`, `:988`); (6) satisfies the always-staged rule; (7) named-path commits in #539.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (proposal-A) | V2 (proposal-B) | V3 (proposal-C) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.714 (5/7; (2) fails at `managed-workspace.md:11`, (3) fails) | 0.714 (5/7; (1) sidesteps, (4) level 4) | 1.000 (7/7) |
| internal_consistency | 0.25 | 1.00 | 1.00 | 1.00 |
| specificity_ratio | 0.15 | 0.85 | 0.85 | 0.85 |
| dependency_completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **0.892** | **0.892** | **0.978** |

## Qualitative Scoring (50% weight)

| Dimension | V1 | V2 | V3 | Decisive evidence |
|---|---|---|---|---|
| Completeness | 3/5 | 3/5 | 4/5 | V1 misses the executability requirement; V2 misses the literal question; none states out-of-scope (V3 does: "covers SW-02's own plan only") |
| Correctness | 3/5 | 5/5 | 4/5 | V1 step 2 is false (cross-checkout plan is refused) and its "archive location UNVERIFIED" is now settled against it; V3's "nothing material unresolved" misses reflect files outside the package |
| Structure | 5/5 | 5/5 | 5/5 | identical |
| Clarity | 4/5 | 4/5 | 4/5 | ids unglossed in all |
| Risk coverage | 3/5 | 3/5 | 4/5 | V3 names the narrow-exception guard and growth of review artifacts |
| Invariants and edge cases | 2/5 | 2/5 | 3/5 | V3 alone handles the cross-session and package-state interactions |
| **qual_score** | **20/30 = 0.667** | **22/30 = 0.733** | **24/30 = 0.800** | |

Edge case floor: all eligible.

## Position-Bias Mitigation
Pass 1 (V1, V2, V3) and pass 2 (V3, V2, V1) by the same in-context scorer, so not independent. Re-checked in pass 2: V1 correctness (kept 3/5, verified rule), V3 correctness (kept 4/5, verified reflect paths). Disagreements: 0. Verdicts changed: 0.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final** | Debate points |
|---|---|---|---|---|
| V1 | 0.446 | 0.333 | **0.779** | 1 |
| V2 | 0.446 | 0.367 | **0.813** | 0 |
| V3 | 0.489 | 0.400 | **0.889** | 8 |

Margin V3 over V2: 7.6% (above 5%). Tiebreaker: no.

## Selected Base: Variant 3 (proposal-C)

### Selection Rationale
Only V3 runs as written (plan and code in one checkout, `managed-workspace.md:11`), needs no Q26 answer and stays at level 3; all three advocates picked it.

### Strengths to Preserve from Base
1. Plan, ledger and fix in the #539 checkout and PR.
2. The exception is narrow: SW-02's own plan only.

### Strengths to Incorporate from Non-Base Variants
1. From V2: record first that the Done sweep task package does not cover SW-02.
2. From V1: the guard that nothing else from the alignment program enters #539.
3. From V3's own concessions: reflect's out-of-package reports stay untracked; the commit includes `progress.md`, `artifacts/` and the `to-do/` to `done/` move by named paths.
