# Base Selection (Q25)

Scored by the orchestrating worker (debate-orchestrator role). Requirement set for RC, from question.md: (r1) who starts the PR session, (r2) who builds the change, (r3) never a worker and never the coordinator running pr-submit, (r4) one live agent per worktree, (r5) person sees unseen changes before push, (r6) grant row per PR, (r7) fork-only target and URL check, (r8) behaviour if the route fails.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (worker + launched PR session) | V2 (owner-opened) | V3 (agent per item) | Basis |
|---|---|---|---|---|---|
| RC | 0.30 | 1.00 (8/8) | 0.88 (r8 implicit) | 0.88 (r8 stall case open) | topic match |
| IC | 0.25 | 0.95 | 0.90 ("strongest reading" of SKILL.md:47 overstated, conceded) | 0.90 (diff stop claimed yet binds only by prompt) | concessions |
| SR | 0.15 | 0.90 | 0.85 | 0.90 | concrete commands |
| DC | 0.15 | 1.00 | 1.00 | 0.90 ("Orca idle notices" unsourced) | references |
| SC | 0.15 | 1.00 | 1.00 | 1.00 | five sections |
| **quant_score** | | **0.973** | **0.926** | **0.914** | |

## Qualitative Scoring (50% weight), 30-criterion binary rubric

| Dimension | V1 | V2 | V3 | Deciding evidence |
|---|---|---|---|---|
| Completeness (5) | 5 | 4 | 4 | V1 names check plus fallback; V3 lacks stall rule; V2 lacks delegation path |
| Correctness (5) | 4 | 4 | 4 | V1 rests on UNVERIFIED launch (stated); V2 overstates skill rule; V3 relies on prompt-only stop |
| Structure (5) | 5 | 5 | 5 | identical |
| Clarity (5) | 5 | 5 | 5 | all concrete |
| Risk coverage (5) | 4 | 4 | 4 | each names its main risk |
| Invariant and edge case (5) | 4 | 3 | 3 | V1: one-agent rule, admitted result, fallback; V2: plain-terminal agent question unstated; V3: pre-PR stall unhandled |
| **Total (30)** | **27** | **25** | **25** | |
| **qual_score** | 0.900 | 0.833 | 0.833 | |

Edge-case floor: all eligible.

## Position-Bias Mitigation
Two reading orders by the same orchestrating worker; not independent agents. No criterion changed.

## Combined Scoring

| Variant | Score |
|---|---|
| V1 | 0.937 |
| V2 | 0.880 |
| V3 | 0.874 |

Margin V1 over V2: 0.057 (above 5 percent; no tiebreaker). Debate points won: V1 4, V3 3, V2 2.

## Selected Base: Variant 1 (proposal-A)

- Strengths to preserve: supervised worker for the build, coordinator review before publishing, no per-PR owner time, no spec rows to change, one-time Orca check.
- Strengths to incorporate: from V3, named fallback route with a stall rule; from V2, the owner's "go" for the first push given in the PR session's own conversation where practical, and the commit named in the grant row plus a D3 sentence (A-001); from V1's own concessions, the review-fix pushes at `--monitor 3` are listed in the grant row, and the PR session reads the worker's contract and handoff files first.
