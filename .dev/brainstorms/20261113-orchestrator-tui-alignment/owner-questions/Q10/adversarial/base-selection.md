# Base Selection: Q10 owner-answer proposals

Scored by the orchestrating session (not an advocate). Variant 1 = A, 2 = B, 3 = C.

## Quantitative Scoring (50% weight)

Requirement set (question.md): R1 the sweep's allow-list position stated; R2 the overstated sentence corrected to what is established (ADJ:813); R3 SW-07 can proceed in W3; R4 the OB-03 consumption outcome handled; R5 no new reader of the coordinator's live mailbox without evidence; R6 interaction with the observer's switched-off read (Q6).

| Metric | Weight | A | B | C | Computation note |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.83 | 0.67 | 0.83 | A misses R5 (adds a reader later); B misses R2 and R3 (waits on OB-03); C misses R4 (no reopen trigger) |
| Internal consistency (IC) | 0.25 | 0.92 | 0.92 | 1.00 | A: claims the sweep would give the coordinator its questions, which its own loop already does (WORKER-CONTRACT.md:100-103); B: proposed final sentence names the observer as reader while its read is off |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.90 | 0.90 | Estimated |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | All references resolve |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | Five of five |
| **quant_score** | | **0.914** | **0.866** | **0.934** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric (condensed CEV)

| Dimension | A | B | C | Evidence (short) |
|---|---|---|---|---|
| Completeness | 5 | 4 | 4 | A covers both the now and the conditional later; B and C lack a reopen trigger |
| Correctness | 3 | 3 | 4 | A overstates its benefit; B keeps an unsupported sentence; none notices line 199 is a header (all lose one) |
| Structure | 4 | 4 | 4 | Same template |
| Clarity | 5 | 4 | 5 | B's two-branch wording is conditional on an undated test |
| Risk | 4 | 4 | 4 | All name the live-Run limit or the stale-sentence cost |
| Invariant and edge cases | 3 | 3 | 2 | A and B handle the consumption branch; C does not |
| **Total of 30** | **24** | **22** | **23** | |
| **qual_score** | **0.800** | **0.733** | **0.767** | |

Edge-case floor: all eligible.

## Position-Bias Mitigation

Pass 1 order A, B, C; pass 2 order C, B, A. One disagreement: A, Completeness "dependencies" (pass 1: 1, names OB-03, OB-04, OB-05; pass 2: 0, misses the coordinator's existing wait). Re-evaluated: 1 (dependencies are named; the missed wait is scored under Correctness). Verdicts changed: 0.

## Combined Scoring

| Variant | quant x 0.5 | qual x 0.5 | Score |
|---|---|---|---|
| A | 0.457 | 0.400 | 0.857 |
| B | 0.433 | 0.367 | 0.800 |
| C | 0.467 | 0.383 | 0.850 |

Margin C to A: 0.007 (within 5%): tiebreaker applied. Level 1, debate performance: C won 8 of 10 points, A won none outright (shared two). Winner: C.

## Selected Base: Variant 3 (proposal C)

- Selection rationale: tiebreaker level 1 (debate points), and chosen by all three advocates.
- Strengths to preserve: `check` stays out of the sweep's allow-list now; the unproven claim is corrected now in SW-07.
- Strengths to incorporate: from A, a reopen trigger tied to OB-03, OB-04 and OB-05, turning into "neither" if OB-03 shows consumption; from B, the firm statement that any sweep read needs a new owner-signed allow-list; from all three advocates, applying the replacement text to the bullet only and keeping the true header value; from A's advocate, the fact that the coordinator already receives questions through its own wait.
