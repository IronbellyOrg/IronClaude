# Base Selection (Q21)

Scored by the orchestrating worker (debate-orchestrator role, not a separate agent), by reading the three variants against `question.md`. Requirement set for RC: the 6 items question.md says the answer must address: (r1) signal source, (r2) timing relative to FU-1, (r3) effect on SW-10, (r4) effect on WA-07, (r5) allow-list (NFR-014), (r6) behaviour when the signal is unusable.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (proposal-A) | V2 (proposal-B) | V3 (proposal-C) | Basis |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.00 (6/6) | 1.00 (6/6) | 0.83 (5/6; r6 not applicable, no signal handling) | topic match to r1-r6 |
| Internal consistency (IC) | 0.25 | 0.90 (one contradiction: "false label unlikely" vs coarse fallback that labels any person session in the worktree) | 1.00 | 0.95 (says WA-07 "loses one route" while WA-07's row still lists SW-10 as a blocker) | contradiction scan, round 1 concessions |
| Specificity (SR) | 0.15 | 0.85 | 0.90 | 0.85 | cited lines, named items vs vague words |
| Dependency completeness (DC) | 0.15 | 0.85 (does not state FU-1 waits on Q2, Q20) | 1.00 | 0.90 (WA-07 table edit unstated) | internal references resolved |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | five sections each |
| **quant_score** | | **0.925** | **0.985** | **0.900** | |

## Qualitative Scoring (50% weight), 30-criterion binary rubric, summary of CEV verdicts

| Dimension | V1 | V2 | V3 | Deciding evidence |
|---|---|---|---|---|
| Completeness (5) | 4 | 5 | 4 | V1 omits FU-1's wait on Q2/Q20; V3 has no unusable-signal rule (not needed) and no WA-07 table edit |
| Correctness (5) | 3 | 5 | 4 | V1 lists `status --json` first, which lacks launched sessions' op ids (`cycle.py:1308-1323`, conceded); V1 fallback contradicts its safety claim; V3 understates the WA-07 edit |
| Structure (5) | 5 | 5 | 5 | identical layout |
| Clarity (5) | 4 | 5 | 5 | V1 leaves input choice open ("which one ... is UNVERIFIED") |
| Risk coverage (5) | 4 | 5 | 4 | V2 names drift, n=1, wait on Q2/Q20, error direction; V3 names misleading report but no mitigation beyond a doc sentence |
| Invariant and edge case (5) | 3 | 4 | 3 | V2: empty-signal stop, error direction, D-A case; misses build-drift tripwire (V3 critique). V1: positive match but unsafe fallback. V3: safe default but no handling after reopen |
| **Total (30)** | **23** | **29** | **25** | |
| **qual_score** | 0.767 | 0.967 | 0.833 | |

Edge-case floor (at least 1 of 5): all eligible.

## Position-Bias Mitigation
Two reading orders by the same orchestrating worker (V1, V2, V3 then V3, V2, V1); not independent agents. No criterion changed between orders.

## Combined Scoring

| Variant | quant x 0.5 | qual x 0.5 | Score |
|---|---|---|---|
| V1 (proposal-A) | 0.463 | 0.383 | 0.846 |
| V2 (proposal-B) | 0.493 | 0.483 | 0.976 |
| V3 (proposal-C) | 0.450 | 0.417 | 0.867 |

Margin V2 over V3: 0.109 (no tiebreaker). Debate points won: V2 6, V1 1, V3 0, unresolved 2.

## Selected Base: Variant 2 (proposal-B)

- Rationale: no new input and no allow-list change (`probes.py:55`), evidence-gated with a fixture test, and the only explicit "no reliable signal, stop" rule; won 6 of 10 points, 3 unanimously.
- Strengths to preserve: stop rule; FU-1 gate; error direction toward "never messaged".
- Strengths to incorporate: from V1, the fact that the watcher's `dispatch.json` is a versioned record holding `operation_id` and `launch_cwd` (`record.py:69-95`), as the named alternative if FU-1 shows Orca rows carry no signal (not a new input now); from V3, the documentation sentence naming the blind spot now, the n=1 and build-drift concern, and the WA-07 dependency note.
