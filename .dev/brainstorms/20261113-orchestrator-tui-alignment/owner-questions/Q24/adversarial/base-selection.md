# Base Selection (Q24)

Scored by the orchestrating worker (debate-orchestrator role). Requirement set for RC, from question.md: (r1) runner of XC-03, (r2) runner of XC-04, (r3) runner of OB-03 and its separate write row, (r4) terminal that holds no Run, (r5) XC-04 master code and report location, (r6) protection of the `issue-409-mvp` evidence, (r7) behaviour if the runner is unavailable.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (fresh session) | V2 (owner) | V3 (409 session) | Basis |
|---|---|---|---|---|---|
| RC | 0.30 | 0.86 (6/7; r7 implicit) | 0.86 (r5 unspecified) | 1.00 (7/7) | topic match |
| IC | 0.25 | 0.90 (step 5 removal deletes the report it must keep, conceded) | 1.00 | 0.95 ("one runner" yet three rows) | concessions |
| SR | 0.15 | 0.95 (exact create command) | 0.80 | 0.90 | concrete commands, lines |
| DC | 0.15 | 1.00 | 0.90 | 1.00 | references resolve |
| SC | 0.15 | 1.00 | 1.00 | 1.00 | five sections |
| **quant_score** | | **0.920** | **0.913** | **0.973** | |

## Qualitative Scoring (50% weight), 30-criterion binary rubric

| Dimension | V1 | V2 | V3 | Deciding evidence |
|---|---|---|---|---|
| Completeness (5) | 4 | 3 | 4 | V2 lacks XC-04 environment; V1 and V3 each lack one fallback detail |
| Correctness (5) | 4 | 4 | 3 | V3 depends on an UNVERIFIED session and an unmerged worktree for "master code"; V1 step 5 flaw |
| Structure (5) | 5 | 5 | 5 | identical |
| Clarity (5) | 5 | 4 | 5 | V2 procedures unspecified |
| Risk coverage (5) | 5 | 3 | 4 | V1 names D-A, cold start, report location; V2 thin on its own risks of hand typing beyond one line |
| Invariant and edge case (5) | 4 | 3 | 3 | V1: terminal read-back, master revision; V3: binding risk named only by its advocate |
| **Total (30)** | **27** | **22** | **24** | |
| **qual_score** | 0.900 | 0.733 | 0.800 | |

Edge-case floor: all eligible.

## Position-Bias Mitigation
Two reading orders by the same orchestrating worker; not independent agents. No criterion changed.

## Combined Scoring

| Variant | Score |
|---|---|
| V1 (fresh session) | 0.910 |
| V2 (owner) | 0.823 |
| V3 (409 session) | 0.887 |

Margin V1 over V3: 0.023 (under 5 percent): tiebreaker level 1, debate points won: V1 3 outright (C-001, C-003, X-002) plus shared wins on C-004 and C-005; V3 0 outright plus a shared win on C-005. V1 selected.

## Selected Base: Variant 1 (proposal-A)

- Strengths to preserve: master-based runner, no dependence on the 409 session's survival, no risk to the 409 evidence, read-back that the terminal holds no Run.
- Strengths to incorporate: from V3, the 409 session as an adviser (not runner) and the record-first step for A-001; from V2, OB-03 stays with the owner, who also authors the pass record (INV-014); from V1's own advocate, copy the sweep report into the ledger package before the worktree is removed, and hand the runner the observer's verified field list.
