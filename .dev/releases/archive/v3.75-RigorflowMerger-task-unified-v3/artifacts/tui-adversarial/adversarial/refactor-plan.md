# Refactoring Plan

## Overview

- **Base variant**: Variant B (combined score 0.944)
- **Incorporated variants**: A (architecture critique + sequencing rationale + INV mitigation), C (per-day ROI + Flagged-L + day-numbered sequencing)
- **Total planned changes**: 8
- **Overall risk**: Low (additive merges; B's structure preserved)

## Planned Changes

### Change #1 — Adopt converged Round-3 final ranking

- Source: All three R3 final positions
- Target: Final shortlist section
- Approach: Replace B's R1 ranking (P-01, P-05, P-02, P-03, P-10) with the R3 converged ranking (P-01, P-05, P-02, P-03, P-07). Move P-10 to "Held back, ship as #6 immediately after P-01 with sentinel mitigation".
- Risk: Low (matches B's own R3 final position)

### Change #2 — Incorporate A's layering critique into P-07 rationale

- Source: Variant A slot #4 / U-003 layering insight
- Target: P-07 rationale section in merged top-5
- Approach: Append a paragraph noting that P-07 is not merely a width fix — it relocates the assistant-text trim from monitor.py:121 to render-time. Architect-lens-specific structural value.
- Rationale: Independent unique contribution from A; B and C both agreed in R2 that the layering critique is valid.
- Risk: Low (additive)

### Change #3 — Incorporate C's per-day ROI summary

- Source: Variant C / U-002
- Target: Methodology section of merged shortlist
- Approach: Add a one-paragraph summary of per-day ROI methodology (P-05 ~0.30/day, P-01 ~0.32/day — within noise) as supporting evidence for the sequencing decision. Do not reproduce the full ratio calculations.
- Rationale: Quantification supports the qualitative reasoning; C's R2 concession that the ratios are "within noise" must be captured.
- Risk: Low (additive)

### Change #4 — Adopt C's day-numbered sequencing labels

- Source: Variant C / S-005 winner
- Target: Sequencing section
- Approach: Replace B's week-numbered sequencing (Week 1, Week 1-2, Week 2-4) with C's day-numbered scheme (Day 1, Day 1-2, Days 3-5). Day-numbered is more actionable for engineering scheduling.
- Risk: Low (label change, semantics preserved)

### Change #5 — Adopt A's "fireworks landing" sequencing rationale

- Source: Variant A sequencing section
- Target: Sequencing section
- Approach: Append A's rationale that P-01 lands *last* so that on the day P-01 ships, every other widget is already correct and the keystone unblocks all of them simultaneously. This is independently derived by A and C and supported by B.
- Rationale: Unanimous sequencing rationale; high-confidence merge.
- Risk: Low

### Change #6 — Add Flagged-Large-Effort section from C

- Source: Variant C / Flagged-L section
- Target: New section after "Held Back"
- Approach: Add a dedicated section explicitly addressing P-09 (the only L-effort proposal) with rationale for exclusion + "next wave's anchor proposal" recommendation. Methodologically rigorous.
- Rationale: C's distinctive methodological contribution; A also implicitly supports.
- Risk: Low (additive)

### Change #7 — Add INV-001/005 mitigation contract from R3

- Source: Round 3 A's mitigation proposal
- Target: P-01 acceptance criteria section
- Approach: Add a mandatory unit-test contract: `tests/sprint/test_monitor_reset_between_tasks.py` with 3-task event-count invariant. Promote reset to public `OutputMonitor.reset_for_next_task()` method.
- Rationale: Required to absorb HIGH UNADDRESSED INV items from Round 2.5. Unanimously accepted in R3.
- Risk: Low (clarifies acceptance criteria; does not change implementation scope)

### Change #8 — Add INV-004 mitigation (prompt_preview audit)

- Source: Round 3 B/C resolution
- Target: P-03 acceptance criteria section
- Approach: 15-minute grep audit of `Phase.prompt_preview` downstream consumers required before P-03 PR merge.
- Risk: Low

## Changes NOT Being Made

### NOT incorporating: B's R1 P-10 inclusion at slot #5

- Variant B's R1 proposed P-10 at slot #5. By R2 B conceded (matching A and C). Final outcome: P-07 at slot #5; P-10 → held-back, ship as #6 post-P-01 with sentinel mitigation. Honour the converged outcome.

### NOT incorporating: A's R1 #1 ranking certainty

- Variant A's R1 framed P-01 at #1 as "structurally obvious." By R2 A conceded the per-day ROI tie with P-05 is "within noise." Final outcome documents the rank #1 dispute as a methodological tiebreak, not a structural certainty. Preserves the steelmanned reasoning rather than re-asserting confidence.

### NOT incorporating: C's R1 placement of P-05 above P-01

- Variant C's R1 ranked P-05 at #1. By R3 C conceded P-01 at #1 (with sequencing preserved). The merged outcome adopts the R3 concession; C's R1 portfolio-risk argument is captured in the methodology section as one valid perspective but not as the ranking driver.

### NOT incorporating: Variant A's lower viability scores

- A's viability scores were systematically lower than B's and C's. Variant B's higher scores reflect the dual-pass position-bias re-evaluation. Honour B's calibrated scores.

## Risk Summary

All 8 planned changes are Low-risk. No High or Medium risks. No structural rewrites. All merges are additive or label-swap operations preserving B's base structure.

## Review Status

- Default: Auto-approved
- Status: Auto-approved (non-interactive mode)
