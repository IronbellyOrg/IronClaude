# Base Selection (Q23)

Scored by the orchestrating worker (debate-orchestrator role). Requirement set for RC, from question.md: (r1) mapping-table meaning for XC-05, (r2) OB-06 prerequisite (e), (r3) observer default-view effect, (r4) sweep effect, (r5) handling of the unconfirmed Orca meaning, (r6) related states `release_pending`, `release_unknown`.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (historical) | V2 (live side) | V3 (own state) | Basis |
|---|---|---|---|---|---|
| RC | 0.30 | 1.00 (6/6) | 0.83 (r6 missing) | 0.83 (r6 missing) | topic match |
| IC | 0.25 | 0.90 (calls rows "finished" while A-001 is unconfirmed) | 0.85 ("live" contradicts finished task; conceded) | 1.00 | concessions |
| SR | 0.15 | 0.90 | 0.85 | 0.90 | cited lines and counts |
| DC | 0.15 | 1.00 | 1.00 | 1.00 | references resolve |
| SC | 0.15 | 1.00 | 1.00 | 1.00 | five sections |
| **quant_score** | | **0.960** | **0.889** | **0.949** | |

## Qualitative Scoring (50% weight), 30-criterion binary rubric

| Dimension | V1 | V2 | V3 | Deciding evidence |
|---|---|---|---|---|
| Completeness (5) | 5 | 4 | 4 | V1 raises related states; V2 and V3 do not |
| Correctness (5) | 3 | 3 | 5 | V1 hides possibly-running rows (`view.py:363-366` ignores liveness); V2's "live" is wrong for a succeeded task (fixture) |
| Structure (5) | 5 | 5 | 5 | identical |
| Clarity (5) | 5 | 4 | 4 | V3 "its own state" leaves "is it running?" to another field |
| Risk coverage (5) | 4 | 4 | 5 | V3 names provisional-forever risk and a settling step |
| Invariant and edge case (5) | 3 | 3 | 4 | V3 is correct whether or not the session exited (A-001) |
| **Total (30)** | **25** | **23** | **27** | |
| **qual_score** | 0.833 | 0.767 | 0.900 | |

Edge-case floor: all eligible.

## Position-Bias Mitigation
Two reading orders by the same orchestrating worker; not independent agents. No criterion changed.

## Combined Scoring

| Variant | Score |
|---|---|
| V1 (historical) | 0.897 |
| V2 (live side) | 0.828 |
| V3 (own state) | 0.925 |

Margin V3 over V1: 0.028 (under 5 percent): tiebreaker level 1, debate points won: V3 5 (C-001, C-004, X-002, X-003, A-001) plus a shared win on C-002; V1 1 (C-003). V3 selected.

## Selected Base: Variant 3 (proposal-C)

- Strengths to preserve: no meaning claimed beyond evidence; no code change; reopen step through the shared capture XC-03.
- Strengths to incorporate: from V2, the observed fixture facts (task finished, resources still held, release not requested, liveness unverifiable) written into the row as observations; from V2 and V1, the conditional outcome once the meaning is confirmed (automatic release: historical as in V1; release by a person: visible as "awaiting release" as in V2); from V1, the related states and the U-001 note that the sweep's "historical" and "settled" differ from the observer's.
