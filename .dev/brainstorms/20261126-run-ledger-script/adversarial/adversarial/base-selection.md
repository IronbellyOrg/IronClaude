# Base Selection

## Quantitative Scoring (50% weight)
Computed by reading each variant against the seed brief (7 open questions, 4 success criteria, 6 test cases named in the issue).

| Metric | Weight | V1 (architect) | V2 (refactorer) |
|---|---|---|---|
| Requirement coverage | 0.30 | 1.00 (all 7 questions; hook branch tested-or-dropped) | 1.00 (all 7; hook via the allowed "dropped with reason" branch) |
| Internal consistency | 0.25 | 0.95 (two hook-entry retention windows, 24 h and build-start, never reconciled) | 1.00 |
| Specificity ratio | 0.15 | 0.93 | 0.93 |
| Dependency completeness | 0.15 | 1.00 | 1.00 |
| Section coverage | 0.15 | 1.00 (10 sections) | 0.90 (9 sections, no separate test-plan or risk-per-section heading style) |
| **quant_score** | | **0.9795** | **0.9795** |

Note: scores are estimated by reading, not by a grep script; this is a quick-depth run.

## Qualitative Scoring (50% weight): additive binary rubric (30 criteria, 6 dimensions)
Dual-pass position-bias check run by reading in both orders: no criterion verdict changed between passes.

| Dimension (5 each) | V1 | V2 | Deciding evidence |
|---|---|---|---|
| Completeness | 5 | 4 | V2 does not deliver or test the hook; V1 does |
| Correctness | 5 | 5 | Both verified Orca shapes against the real CLI (worktree id equals worker `worktreeId`; statuses counted) |
| Structure | 3 | 5 | V1 package of 4 modules and 4 subcommands for ~150 lines of logic |
| Clarity | 4 | 5 | V2 states what it deletes and why |
| Risk coverage | 5 | 4 | V1 has lock, stale-hook expiry, shape-drift error; V2 has no overlap guard |
| Invariant and edge-case coverage | 5 | 4 | V1: lost-append race, bad id in `add`, unknown-Run trap; V2: `generated_at` race, repeated cursor. Floor (at least 1 of 5): both pass |
| **qual_score (of 30)** | **27 / 30 = 0.90** | **27 / 30 = 0.90** | |

## Position-Bias Mitigation
Pass 1 (V1 then V2) and pass 2 (V2 then V1) gave identical verdicts on all 60 criterion-variant pairs. Disagreements: 0.

## Combined Scoring
| Variant | 0.5 quant + 0.5 qual |
|---|---|
| V1 | 0.9398 |
| V2 | 0.9398 |
Margin 0.0%: inside the 5% tiebreaker band.

Tiebreaker level 1 (debate points won in the scoring matrix): V2 wins S-001, S-002, C-003, C-004, C-009, C-011, U-003 (7 clear wins); V1 wins C-001, C-005, U-001 (3, two by orchestrator ruling). V2 leads. Level 1 decides.

## Selected Base: Variant 2 (sonnet:refactorer)
- Rationale: tie on both score layers; V2 wins more debate points, and both advocates, including V1's, said the final spec should be V2's shape (one file, one command, XDG path, no new sweep flag).
- Strengths to preserve: one module and one command; `generated_at` before the first Orca call; XDG state path; no new sweep flag; short-circuit call order; 10 named tests.
- Strengths to incorporate from V1: deliver the hook (with lock and merge) and the fixture test; 24 h fallback for the `new` rule; activity clause on the empty-result guard; run-list as the universe; blocked-only count; extra test cases; `flock -n` in the cron line.
