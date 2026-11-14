# Convergence Summary

Scoring clerk tally for the 3-advocate debate on the unified alignment spec. Sources: the per-point tables in `round1-advocate-V1.md`, `-V2.md`, `-V3.md` (Round 1) and the FINAL per-point tables in `round2-rebuttal-V1.md`, `-V2.md`, `-V3.md` (Round 2, section 5); levels from `diff-analysis.md`. Full matrix: `debate-transcript.md`, section "Scoring Matrix".

Rule: a point is AGREED when at least 2 of 3 advocates name the same winner (V1, V2, V3, MERGE or NEITHER each count as a position; a cell is read by its first word, so "MERGE (V1 base)" is MERGE). UNANIMOUS when 3 of 3. Otherwise UNRESOLVED (confidence 50). Convergence = agreed points / 44. Threshold 75%. The invariant gate is applied separately by the orchestrator after the Round 2.5 probe; `invariant-probe.md` was still a stub (TODO markers, no findings) at the time of this tally.

## Per-round convergence

| Round | Agreed (of 44) | Unanimous | Two of three | Unresolved | Convergence | Status vs 75% |
|---|---|---|---|---|---|---|
| Round 1 | 41 | 15 | 26 | 3 (S-001, C-005, C-010) | 93.2% | above threshold |
| Round 2 (final) | 44 | 39 | 5 (S-002, C-001, C-011, X-003, X-014) | 0 | 100.0% | CONVERGED (agreement only; invariant gate pending) |

Round 2 winners: MERGE 17, V2 11, V1 9, V3 4, NEITHER 3 (total 44).

## Per-level coverage (taxonomy coverage gate)

| Level | Points | Round 1 agreed | Round 2 agreed | Round 2 unresolved |
|---|---|---|---|---|
| L1 surface | 3 (S-001, S-006, C-011) | 2 | 3 | none |
| L2 structural | 20 | 18 | 20 | none |
| L3 state-mechanics | 16 | 16 | 16 | none |
| U (promoted unique points; `diff-analysis.md` gives them no level) | 5 (U-004, U-005, U-010, U-011, U-012) | 5 | 5 | none |
| Total | 44 | 41 | 44 | none |

Gate result: every level L1, L2 and L3 has points, and every point at every level is agreed in Round 2. Covered.

## UNRESOLVED points

Round 2: none.

Round 1 had three, each resolved in Round 2:

| Point | Level | Round 1 stances (V1 / V2 / V3) | Round 2 final stances (V1 / V2 / V3) | Round 2 winner |
|---|---|---|---|---|
| S-001 | L1 | MERGE 65 / V2 60 / V3 92 | MERGE 65 / MERGE 60 / MERGE 80 | MERGE, 68.3 |
| C-005 | L2 | MERGE 60 / V1 60 / V3 92 | MERGE 65 / MERGE 65 / MERGE 90 | MERGE, 73.3 |
| C-010 | L2 | V1 65 / V2 65 / MERGE 97 | V1 70 / V1 65 / V1 90 | V1, 75.0 |

Points still split 2 to 1 after Round 2 (agreed, not unanimous):

| Point | V1 | V2 | V3 | Winner, confidence |
|---|---|---|---|---|
| S-002 | V1 60 | MERGE 60 | V1 75 | V1, 67.5 |
| C-001 | MERGE 85 | V2 80 | V2 96 | V2, 88.0 |
| C-011 | V2 80 | V2 82 | MERGE 90 | V2, 81.0 |
| X-003 | V1 85 | MERGE 85 | MERGE 98 | MERGE, 91.5 |
| X-014 | V1 72 | MERGE 78 | V1 96 | V1, 84.0 |

## Final preferred base (end of each Round 2 rebuttal, section 6)

| Advocate | Final preferred base | Confidence | Change from Round 1 |
|---|---|---|---|
| V1 (opus:architect) | V1 | 70 | not stated in the section |
| V2 (opus:analyzer) | V2 | 60 | down from 70 (stated: C-003 and C-010 concessions); V2 says it would accept V1 if a fresh reviewer's row count goes against V2 |
| V3 (haiku:backend) | V1 | 75/100 | changed from V3 at 90 |

Two of three advocates name V1 as the final base.

## Flips between rounds

- Advocate-point flips (an advocate's own winner differs between Round 1 and Round 2): 40 in total. V1 7, V2 11, V3 22.
- Points on which at least one advocate flipped: 29 of 44.
- Points on which the majority winner changed: 12 (S-001, S-002, S-003, C-001, C-003, C-005, C-010, X-003, X-012, X-013, X-014, A-005).
- Per-advocate flip lists are in `debate-transcript.md`, section "Convergence Assessment".
