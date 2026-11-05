# Base Selection

Method note (disclosed limits): the quantitative metrics were counted by two scorer agents (sonnet class) using the stated counting methods, not by a script, so the two passes differ; the position-bias mitigation below averages them. The 30-criterion qualitative rubric was run twice, in input order (1, 2, 3) and reverse order (3, 2, 1), each with Claim-Evidence-Verdict. Per-criterion disagreement re-evaluation was NOT run (cost); the averaged totals are used and this is reported as a limitation.

## Quantitative Scoring (50% weight)

| Metric (weight) | V1 fwd / rev | V2 fwd / rev | V3 fwd / rev |
|---|---|---|---|
| RC requirement_coverage (0.30) | 0.833 / 0.889 | 0.333 / 0.444 | 0.722 / 0.889 |
| IC internal_consistency (0.25) | 0.857 / 0.857 | 0.800 / 0.800 | 0.750 / 0.750 |
| SR specificity_ratio (0.15) | 0.429 / 0.429 | 0.800 / 0.800 | 0.500 / 0.500 |
| DC dependency_completeness (0.15) | 0.833 / 0.833 | 0.833 / 0.833 | 1.000 / 1.000 |
| SC section_coverage (0.15, normalised) | 0.667 / 0.714 | 1.000 / 0.857 | 0.778 / 1.000 |
| quant_score | 0.754 / 0.777 | 0.695 / 0.707 | 0.746 / 0.829 |
| **quant (mean of passes)** | **0.7655** | **0.7010** | **0.7875** |

## Qualitative Scoring (50% weight): 30-criterion additive binary rubric

| Dimension (5 each) | V1 fwd / rev | V2 fwd / rev | V3 fwd / rev |
|---|---|---|---|
| Completeness | 3 / 3 | 3 / 4 | 4 / 4 |
| Correctness | 2 / 3 | 2 / 2 | 2 / 2 |
| Structure | 4 / 5 | 4 / 4 | 4 / 4 |
| Clarity | 2 / 4 | 4 / 4 | 4 / 3 |
| Risk coverage | 5 / 5 | 3 / 4 | 5 / 5 |
| Invariant and edge cases | 5 / 5 | 2 / 5 | 5 / 5 |
| Total /30 | 21 / 25 | 18 / 23 | 24 / 23 |
| **qual (mean of passes) / 30** | **0.7667** (23.0) | **0.6833** (20.5) | **0.7833** (23.5) |

Edge-case floor (minimum 1/5 on Invariant and edge cases): all three variants clear it; none is ineligible.

## Position-Bias Mitigation
- Passes disagree on 13 of 18 dimension cells by at least one criterion; largest swings: V1 Clarity (2 vs 4) and V1 Correctness (2 vs 3), V2 Invariant (2 vs 5). Quantitative RC for V2 differs by 0.11 and SC for V3 by 0.22.
- Resolution used: mean of the two passes. Limitation: no per-criterion re-evaluation; the totals are therefore indicative, and the winner is decided by the tiebreaker below, not by the score margin.

## Combined Scoring
| Variant | quant (0.5) | qual (0.5) | combined |
|---|---|---|---|
| V1 (analyzer/sonnet) | 0.7655 | 0.7667 | **0.7661** |
| V2 (qa/haiku) | 0.7010 | 0.6833 | 0.6922 |
| V3 (refactorer/opus) | 0.7875 | 0.7833 | **0.7854** |

Margin V3 over V1: 0.0193 (1.9%), inside the 5% tiebreaker band.

Tiebreaker protocol:
- Level 1, debate performance (diff points won in the scoring matrix of debate-transcript.md): V1 wins S-002, C-003, C-004, C-006, X-001, X-003 (6) and shares C-001 and X-002; V3 wins C-002, C-005, C-007, C-008 (4) and shares C-001, C-009, X-002; V2 shares C-009. V1 has more points won, so the winner is V1. Tiebreaker applied: yes (level 1).

## Selected Base: Variant 1 (reviewer-1 analyzer card, sonnet)

Selection rationale: V1 holds the only finding that all three advocates converged on as blocking-until-criterion (X-001), plus the shell-mechanics findings (C-006) that decide whether the exit-3 safety net works. Its combined score is within 2% of V3.

Strengths to preserve from the base: F1 (invalid name or failing --auto-name must still start Claude), F2/F5 (IFS= and `--` handling, required plan notes), F6/F7 (invalid-name test, CCSESSION_NAME test-env exclusion), F10/F11/F12.

Strengths to incorporate from non-base variants (detail in refactor-plan.md):
- From V3: Task 5 contradiction (two Enter reopen tests), scope-additions list with keep/ask-owner opinions, C-005 (executor writes launch-paths.md), C-007 (keep old default hint; report the new 30 s default for the Coder hook), the Task 4 CCSESSION_ASK_TIMEOUT contradiction and the saved-name test (test:1494-1509), the 80-character cut order.
- From V2: timer-default criterion gap (plan:46), README `--session-id` row (README:266), negative matrix result (no spec requirement is taskless), same-minute test.
- From the invariant probe: INV-002, INV-003, INV-005 as required notes; INV-004, INV-006, INV-009, INV-010 as executor notes.
