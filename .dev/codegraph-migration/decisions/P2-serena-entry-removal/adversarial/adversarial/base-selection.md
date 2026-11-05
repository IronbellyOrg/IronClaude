# Base Selection

Scored by the orchestrator. The hard requirement from `context.md` is treated as requirement R1.

## Quantitative Scoring (50% weight)

Source requirements (context.md "Requirement"): R1 the current-pin `serena` user entry is removed on existing workspaces after `./update.sh`; R2 who removes it is named; R3 when is named; R4 an acceptance check exists; R5 codebase-memory is also absent. Coverage counts a requirement as met only when the variant's mechanism satisfies it, not when it merely mentions it.

| Metric | Weight | V1 (A) | V2 (B) | V3 (C) | Computation notes |
|---|---|---|---|---|---|
| Requirement Coverage (RC) | 0.30 | 0.80 | 1.00 | 0.80 | A misses R1 everywhere; C misses R1 on Coder (X-003); B meets R1 (defect X-001 counted under IC) |
| Internal Consistency (IC) | 0.25 | 1.00 | 0.917 | 1.00 | B: 1 intra-variant contradiction (X-001) in 12 scorable claims |
| Specificity Ratio (SR) | 0.15 | 0.90 | 0.92 | 0.80 | concrete/(concrete+vague) by statement: A 9/10, B 11/12, C 8/10 (C's "unit tests for both branches", "two code paths to test" unspecific) |
| Dependency Completeness (DC) | 0.15 | 1.00 | 0.75 | 0.67 | B cites "the Coder 'Done means' check above", which is defined only in A (1 of 4 unresolved); C says "exact match, as in Option B" (1 of 3 unresolved) |
| Section Coverage (SC) | 0.15 | 0.857 | 1.00 | 0.857 | bullet sections 6 / 7 / 6 |
| **Quant score** | | **0.904** | **0.930** | **0.839** | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV per criterion; MET needs a cited line. Dual pass: input order (A, B, C), then reverse (C, B, A).

| Dimension | Criterion | A | B | C | Evidence (short) |
|---|---|---|---|---|---|
| Completeness | 1 all explicit requirements | 0 | 1 | 0 | A "never automatically"; C keeps entry on Coder; B names who/when/check everywhere |
| | 2 edge/failure scenarios | 0 | 1 | 1 | B "If the codegraph phase failed, nothing changes"; C "codegraph success/failure" tests |
| | 3 dependencies | 1 | 1 | 1 | all cite Coder step 5 / pin bump |
| | 4 success criteria | 1 | 1 | 1 | acceptance bullets |
| | 5 explicit out-of-scope | 1 | 1 | 0 | A "never automatically" on non-Coder; B "Other Tier K shapes ... stay kept"; C none |
| Correctness | 1 no factual errors | 1 | 0 | 1 | B X-001 |
| | 2 feasible | 1 | 1 | 1 | |
| | 3 consistent terms | 1 | 1 | 1 | |
| | 4 no internal contradiction | 1 | 0 | 1 | B X-001 |
| | 5 claims supported | 1 | 1 | 1 | each gives a rationale |
| Structure | 1-5 | 5 | 5 | 5 | same short option layout; all link `context.md` |
| Clarity | 1-5 | 5 | 5 | 5 | concrete commands and conditions in all three |
| Risk Coverage | 1 ≥3 risks with probability/impact | 0 | 0 | 0 | none rates probability |
| | 2 mitigation per risk | 0 | 1 | 1 | A lists weaknesses without mitigation |
| | 3 failure modes and recovery | 0 | 1 | 1 | B failure branch; C both branches |
| | 4 external dependency failure | 1 | 1 | 1 | all name the Coder dependency |
| | 5 detection mechanism | 1 | 1 | 1 | contract test / install output / unit tests |
| Invariant & Edge | 1 boundaries (absent, exact match) | 1 | 1 | 1 | "only when the entry equals", "exact command + args" |
| | 2 cross-component state | 1 | 1 | 1 | bundle re-add discussed by all |
| | 3 guard gaps | 0 | 1 | 1 | B/C codegraph guard; A none |
| | 4 count divergence | 0 | 0 | 0 | n/a |
| | 5 interaction effects | 1 | 1 | 1 | bundle vs installer interaction |

| Dimension subtotal | A | B | C |
|---|---|---|---|
| Completeness | 3 | 5 | 3 |
| Correctness | 5 | 3 | 5 |
| Structure | 5 | 5 | 5 |
| Clarity | 5 | 5 | 5 |
| Risk Coverage | 2 | 4 | 4 |
| Invariant & Edge | 3 | 4 | 4 |
| **Total / 30** | **23 (0.767)** | **26 (0.867)** | **26 (0.867)** |

Edge-case floor (≥1/5): A 3, B 4, C 4. All eligible.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Completeness 1 | B | MET | NOT MET (X-001 seen first in reverse pass) | disagree | MET: B names who, when and a check on every machine type; X-001 is scored under Correctness 1 and 4, not double-counted |

Disagreements: 1. Verdicts changed: 0.

## Combined Scoring

| Variant | Quant ×0.5 | Qual ×0.5 | Final |
|---|---|---|---|
| V2 (B) | 0.465 | 0.433 | **0.898** |
| V3 (C) | 0.419 | 0.433 | 0.853 |
| V1 (A) | 0.452 | 0.383 | 0.835 |

Margin B over C: 0.045 (< 0.05), so the tiebreaker applies. Level 1 (debate points won, Step 2 matrix): B 8 (S-001, C-001, C-002, C-003, C-005, C-006, C-007, C-008), C 1 (S-002), A/C joint 1 (C-004); the 3 contradictions are resolutions, not wins; B wins. Tiebreaker applied: yes (level 1).

## Selected Base: Variant 2 (Option B, original)

- Rationale: the only variant that removes the current-pin entry where `./update.sh` runs, on and off Coder; won 8 of the 10 structural and content points; both other advocates conceded to a corrected B.
- Strengths to preserve: one exact-match replacement rule guarded by codegraph readiness; never leaves the user with neither; no environment probe; early bundle stop (U-001).
- Strengths to incorporate: A's single `jq -e` check over both names and `command -v` checks (U-005); A/C's exact-argv Coder migration, guarded (U-003); C's two-branch test matrix (S-002); Round 2 refinements (state predicate reusing the phase pass check; `serena-local` hint; amend Phase 1 texts in the same merge); invariant-probe resolutions (INV-003, -004, -006 to -009, -011, -013).
