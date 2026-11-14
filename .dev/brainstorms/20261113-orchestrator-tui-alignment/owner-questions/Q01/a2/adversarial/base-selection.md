# Base Selection: Q1 (a2) and (b)

Scoring was done inline by the orchestrating worker; both rubric passes were run by the same evaluator, so they are not independent. Requirements for the coverage metric: R1 the ruling names a shape (SW-01 (1)); R2 the six channels are in scope; R3 the ruling names any channel it leaves out (SW-01 (4)); R4 the premise; R5 the allow-list authority for this purpose only; R6 the two host facts are handled; R7 a regression test reproducing the probe; R8 the git-status scope is kept separate from the other reads (SW-02 (2), INV-039).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 | Note |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.750 (misses R3, R8) | 0.750 (misses R1, R8) | 0.750 (misses R3, R8) | |
| Internal consistency (IC) | 0.25 | 0.933 (X-001) | 1.000 | 1.000 | |
| Specificity ratio (SR) | 0.15 | 0.87 | 0.87 | 0.87 | manual estimate |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | |
| **quant_score** | | **0.889** | **0.906** | **0.906** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric

| Dimension | V1 | V2 | V3 | Deciding evidence (CEV, condensed) |
|---|---|---|---|---|
| Completeness | 4 | 4 | 4 | Criterion 1 NOT MET for all (R8 absent everywhere; R1 absent in V2; R3 absent in V1, V3). |
| Correctness | 4 | 3 | 4 | V1 criterion 4 NOT MET (X-001). V2 criterion 1 NOT MET (cites only half of ADJ line 206; fails SW-01 (1), conceded) and criterion 5 NOT MET. V3 criterion 1 NOT MET ("avoids F2's failure on this host" argues against a literal F2 rule that Variant 1 does not use). |
| Structure | 4 | 4 | 4 | Criterion 4 (navigation aids): NOT MET for all. |
| Clarity | 5 | 4 | 5 | V2 criterion 5 NOT MET: the owner's decision point is deferred, not identified. |
| Risk coverage | 4 | 3 | 4 | Criterion 1 NOT MET for all. V2 criterion 5 NOT MET (no detection mechanism tied to a named shape). |
| Invariant and edge-case coverage | 4 | 3 | 5 | V3 MET on all five (two-sided test; host facts as constraints; interaction of two behaviours). V1 NOT MET on criterion 4. V2 NOT MET on criteria 2 and 4. |
| **Total** | **25/30 = 0.833** | **21/30 = 0.700** | **26/30 = 0.867** | |

Edge-case floor: all eligible.

## Position-Bias Mitigation

| Pass | Order | Result |
|---|---|---|
| 1 | V1, V2, V3 | 25, 21, 26 |
| 2 | V3, V2, V1 | 26, 21, 25 |

Disagreements: 0. Same evaluator for both passes.

## Combined Scoring

| Variant | 0.5 x quant | 0.5 x qual | Combined |
|---|---|---|---|
| Variant 1 | 0.444 | 0.417 | 0.861 |
| Variant 2 | 0.453 | 0.350 | 0.803 |
| Variant 3 | 0.453 | 0.433 | **0.886** |

Margin Variant 3 over Variant 1: 2.5 points (under 5), so the tiebreaker applies. Level 1 (debate points won): Variant 1 won 7, Variant 3 won 1 (plus two ties). Winner: Variant 1.

## Selected Base: Variant 1 (proposal-A, F2 refuse and report with the "could run for this worktree" rule)

- Selection rationale: tiebreaker on debate points; all three advocates' neutral recommendation.
- Strengths to preserve: one behaviour; results never altered, only withheld; the counting rule that keeps the system git-lfs filter from refusing every worktree.
- Strengths to incorporate:
  1. From Variant 2 (won C-003, X-001): drop the unlisted-channel claim; the ruling names the channels left out; anything the check cannot classify is refused and reported.
  2. From Variant 3 (won C-005): the two-sided regression test.
  3. From all advocates: the environment counting rule (a setting counts only when it names a program `git status` could run).
  4. From all advocates (A-002): the git-status scope is kept separate from the contract allow-list and transcript scans.
  5. From Variant 2 (U-002): the author records the rule's reasoning in the PR and the owner reviews it before merge.
  6. From Variant 3: name the combination as the runner-up if a later count shows many fsmonitor-only worktrees.
