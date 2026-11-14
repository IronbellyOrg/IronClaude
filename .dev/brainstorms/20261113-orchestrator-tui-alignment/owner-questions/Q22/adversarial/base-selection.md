# Base Selection (Q22)

Scored by the orchestrating worker (debate-orchestrator role). Requirement set for RC, from question.md: (r1) observer snapshot threshold, (r2) Coder workspace record threshold, (r3) Coder#477 placeholder (CO-02), (r4) contract note text (XC-05), (r5) TUIBBS channel (CO-04), (r6) consistency with the mapping-table rule for "stale".

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (proposal-A) | V2 (proposal-B) | V3 (proposal-C) | Basis |
|---|---|---|---|---|---|
| RC | 0.30 | 1.00 (6/6) | 0.83 (r5 deferred only) | 1.00 (6/6) | topic match |
| IC | 0.25 | 0.90 ("same 45 s everywhere" conflates file age and data age, conceded) | 0.90 (calls its rule "safe" yet concedes it flickers) | 0.90 (rationale says 60 s; real worst gap about 75 s, conceded) | round 1 concessions |
| SR | 0.15 | 0.90 | 0.85 | 0.90 | cited constants and lines |
| DC | 0.15 | 1.00 | 0.95 | 0.95 | references resolved |
| SC | 0.15 | 1.00 | 1.00 | 1.00 | five sections each |
| **quant_score** | | **0.955** | **0.896** | **0.948** | |

## Qualitative Scoring (50% weight), 30-criterion binary rubric

| Dimension | V1 | V2 | V3 | Deciding evidence |
|---|---|---|---|---|
| Completeness (5) | 5 | 3 | 4 | V2 leaves number and CO-04 open; V3 silent on `--once` files |
| Correctness (5) | 4 | 3 | 4 | V1: 45 s marks a live, backing-off writer stale (`commands.py:294-297`); V2: one-cycle rule flickers; V3: Coder 2 minutes is a guess |
| Structure (5) | 5 | 5 | 5 | identical |
| Clarity (5) | 4 | 5 | 5 | V1 is a formula, not a plain number |
| Risk coverage (5) | 5 | 4 | 4 | V1 names backoff, `--once`, borrowed multiplier, unknown Coder interval |
| Invariant and edge case (5) | 4 | 3 | 3 | V1: backoff, `--once`, copy delay; none handle clock skew |
| **Total (30)** | **27** | **23** | **25** | |
| **qual_score** | 0.900 | 0.767 | 0.833 | |

Edge-case floor: all eligible.

## Position-Bias Mitigation
Two reading orders by the same orchestrating worker; not independent agents. No criterion changed.

## Combined Scoring

| Variant | Score |
|---|---|
| V1 (proposal-A) | 0.928 |
| V2 (proposal-B) | 0.832 |
| V3 (proposal-C) | 0.891 |

Margin V1 over V3: 0.037 (under 5 percent): tiebreaker level 1, debate points won: V1 6 (C-001, C-003, C-004, C-005, X-001, X-002), V3 3 (C-002, X-003, A-001). V1 selected.

## Selected Base: Variant 1 (proposal-A)

- Strengths to preserve: per-producer rule, interval kept in the note (no new snapshot key), copy delay as an input, `--once` statement.
- Strengths to incorporate: from V3, the observer's file threshold must clear the worst live write gap (about 75 s, inference), and file age (writer liveness, `generatedAt`) is a different axis from data age (`source.status`, `source.observedAt`); from all three advocates (A-001), a same-host assumption and an "age unknown" rule for negative or implausible ages; from V2, the reader must show both ages.
