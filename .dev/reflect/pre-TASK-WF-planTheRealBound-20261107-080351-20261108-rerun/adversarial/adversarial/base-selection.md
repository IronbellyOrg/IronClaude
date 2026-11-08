# Base Selection

Scorer: the orchestrator (sonnet class), a different class from both debaters (haiku and opus). Timestamp 2026-11-08T02:16Z.

## Quantitative Scoring (50% weight)

Computed from the variant text; no advocate input. Requirements = INF-001..INF-010 (the spec's ten inferred requirements).

| Metric | Weight | Variant 1 | Variant 2 | Basis |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.00 | 1.00 | both give an explicit verdict for INF-001..INF-010 |
| Internal consistency (IC) | 0.25 | 0.95 | 0.95 | no contradicting claims inside either card; variant 1 applies a "Drift" category its own brief forbids (counted in the qualitative layer, not here) |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.92 | both are dense in plan, helper and design line citations; variant 2 has a few more hedges ("Low-Medium") |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | internal references resolve; variant 2's N-ids point at the Tier 1 card (external, excluded) |
| Section coverage (SC) | 0.15 | 0.714 | 1.000 | variant 1 has 5 top-level sections, variant 2 has 7 (max 7) |
| **quant_score** | | **0.930** | **0.976** | 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC |

## Qualitative Scoring (50% weight): additive binary rubric, 30 criteria

Each criterion is MET (1) only with a cited piece of evidence in the variant; otherwise NOT MET (0).

| Dimension | Variant 1 | Variant 2 | Deciding evidence (NOT MET items) |
|---|---|---|---|
| Completeness (5) | 3 | 4 | V1 NOT MET: prerequisites (no nested-launch precondition) and out-of-scope statement; V2 NOT MET: out-of-scope statement |
| Correctness (5) | 3 | 4 | V1 NOT MET: A-02 says the plan "requires" a pty session while the plan says "attempt" with an unavailable fallback (calibrator note), and the "Drift" label contradicts the brief; V2 NOT MET: N-4 budget claim only [INFERRED] |
| Structure (5) | 4 | 4 | V1 NOT MET: follows the artifact convention (forbidden category); V2 NOT MET: severities off the HIGH/MEDIUM/LOW scale |
| Clarity (5) | 4 | 4 | V1 NOT MET: "Drift" used for every finding carries no information; V2 NOT MET: N-ids not defined in the card |
| Risk coverage (5) | 4 | 5 | V1 NOT MET: failure modes and recovery are thin (calibrator risk dimension 0.78) |
| Invariant and edge-case coverage (5) | 4 | 5 | V1 NOT MET: no boundary-of-collection or maximum-count (run cap) reasoning |
| **Total** | **22 / 30** | **26 / 30** | |
| **qual_score** | **0.733** | **0.867** | |

Edge-case floor check: both variants score at least 1/5 on invariant and edge-case coverage, so both are eligible as base.

## Position-Bias Mitigation

The reverse-order second evaluation pass was NOT run. The qualitative scores above are a single pass in input order. This is recorded as a degraded component (`position-bias-pass: not-run`) and it lowers confidence in the margin below, although the margin is well outside the 5% tiebreaker band.

## Combined Scoring

| Variant | quant (x0.5) | qual (x0.5) | Combined |
|---|---|---|---|
| 1 | 0.465 | 0.367 | **0.831** |
| 2 | 0.488 | 0.433 | **0.921** |

Margin: 0.090 (9.0%), outside the 5% tiebreaker band, so no tiebreaker is applied. For reference, debate performance: variant 2 won S-003, C-003, C-005 outright, variant 1 won C-002 outright, the rest were ties or contested (see the scoring matrix).

## Selected Base: Variant 2 (reviewer 2, qa persona, opus class)

**Selection rationale.** Variant 2 scores higher on both layers: broader section coverage, a disposition of every Tier 1 defect, and more execution blockers found. Its main weakness (off-scale severity labels) is cheaper to repair than variant 1's weaknesses (a forbidden category on every row, thinner Tier 1 coverage).

**Strengths to preserve from the base.** The per-defect disposition table (N-1..N-14), Q-1 (ordered pty calls with expected statuses), Q-2 (a "not observed (reason)" row category), Q-3 (no task produces wrapper or auto-mode evidence), Q-4 (observe release with the real surviving child), Q-5 (one real governed Git push), Q-6 (stop recorded pids, not only the cwd sweep), Q-7 (expected fork status), Q-8 (identify the Claude pid for the hop count), the run-budget arithmetic and the PASS-reachability analysis.

**Strengths to incorporate from variant 1.** A-02's documentary basis for the budget finding (the archived help file lines 131-132, verified), A-01's testable self-check, A-03's different-controller observation (narrowed), A-04's redacted process-tree snapshot fields, A-05's reparenting assertion, and its correct refutation that the plan does not force a thirteenth Claude start.
