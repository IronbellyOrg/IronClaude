# Base Selection (D01)

Honesty note: the scores below are the orchestrator's single-evaluator estimates, not machine-computed; the position-bias check was a reverse-order re-read by the same evaluator, not an independent run.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (OURS) | Variant B (CLAY) | Basis |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.00 | 1.00 | Brief asks for claim, mechanism, 5 to 10 cited facts, costs, risks, gets-right, recommended rule: all present (A 8 facts, B 9) |
| Internal consistency (IC) | 0.25 | 0.95 | 0.93 | A: "no equal" / "silent" on edits overstated (corrected by `orchestrator.md:488`). B: "owner trend toward fewer gates" contradicted by REQ line 62 (R36 withdraws only R31); fact 8 symbol count corrected from 13 to 14 |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.88 | Both cite file:line; B has more inferential claims |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | Internal references resolve |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 7 H2 sections each |
| **quant_score** | | **0.9725** | **0.9645** | |

## Qualitative Scoring (50% weight)

| Dimension (5 criteria each) | A | B | Evidence |
|---|---|---|---|
| Completeness | 5 | 4 | B has no explicit statement of what is out of scope (A names D09 for label writes; B also names D09 but not the owner-record conflict as scope) |
| Correctness | 4 | 3 | A overstated C-006; B's R36 trend and "assignment widens nothing so removal narrows nothing" ignore what the approval adds (content binding, deliberate act) |
| Structure | 5 | 5 | Same template |
| Clarity | 4 | 4 | Both clear; both long |
| Risk coverage | 4 | 3 | A lists costs, risks and concessions with mitigations (ship gate); B lists risks without mitigations for stale content |
| Invariant and edge-case coverage | 3 | 2 | A: edit-after-approval, same login, claim assigns, two assignees; B: same login, OQ6 gaps, bots. Both miss manual-claim double start (INV-002) and wave-1 re-check gap (INV-001) |
| **Total / 30** | **25** | **21** | |
| qual_score | 0.833 | 0.700 | |

Edge-case floor (1/5): both eligible (3 and 2).

## Position-Bias Mitigation

Pass 1 order A, B; pass 2 order B, A. No criterion verdict changed between passes (0 disagreements). Limitation as stated above.

## Combined Scoring

| Variant | 0.5 x quant | 0.5 x qual | Final |
|---|---|---|---|
| A (OURS) | 0.486 | 0.417 | 0.903 |
| B (CLAY) | 0.482 | 0.350 | 0.832 |

Margin 7.1 points, above the 5-point tiebreak band; no tiebreaker applied (debate points won: A on C-001, C-003, C-006, C-007, C-008, X-001, X-002; B on C-004, C-005, C-010).

## Selected Base: Variant A (OURS)

**Rationale.** A wins the high-severity points C-001, C-006, C-007 and the owner-record points C-008 and X-001 in both advocates' final positions; B's advocate conceded them and called the owner records decisive. B wins readiness (C-005), the same-login weakness (C-004) and code surface (C-010).

**Strengths to preserve (from A).** Assignment never sufficient; approval by an allowed approver (field `Approved`, R35); `unchanged_since` content binding; Status allow-list (R22); the claim-marker guard and `_revalidate`; closed ship gate.

**Strengths to incorporate (from B).**
1. `plan_check(body)` as a read-only skip reason, evaluated before the approval counts (`hold.py:122-143`).
2. `hold:backlog` read as a person's veto from labels already fetched, no watcher label write.
3. Honest limits: L-1 stays an accepted risk; reopen the approval question after D05 and D06 deliver a guarded, claim-only flow.
4. Mandatory requirements from the invariant probe (MR-1 re-check at start, MR-2 keep claim-marker guard).
