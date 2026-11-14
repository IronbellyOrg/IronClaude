# Base Selection Report (Q29)

Scored by the orchestrating worker in-context. Requirements used for coverage (7): (1) the coordinator's CLI on this host gains the sweep; (2) follows the owner's update rule; (3) installs a pinned, reviewed commit; (4) keeps workspaces consistent; (5) handles the shadowing user-level install; (6) ends no running session; (7) checks the gate in the coordinator's own environment.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (proposal-A) | V2 (proposal-B) | V3 (proposal-C) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.714 (5/7; misses 2, 4) | 0.571 (4/7; misses 1 as written, 5, 6) | 0.571 (4/7; misses 1, 3, 5) |
| internal_consistency | 0.25 | 1.00 | 1.00 | 0.90 (step 3 expects the gate to pass on its own; its own risk section says it may never) |
| specificity_ratio | 0.15 | 0.85 | 0.85 | 0.85 |
| dependency_completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **0.892** | **0.849** | **0.824** |

## Qualitative Scoring (50% weight)

| Dimension | V1 | V2 | V3 | Decisive evidence |
|---|---|---|---|---|
| Completeness | 4/5 | 3/5 | 3/5 | V2 leaves the shadow removal unresolved; V3 delivers nothing |
| Correctness | 5/5 | 5/5 | 4/5 | V3 step 3 is wrong on this host (`main.tf:594-597`) |
| Structure | 5/5 | 5/5 | 5/5 | identical |
| Clarity | 4/5 | 4/5 | 4/5 | ids unglossed |
| Risk coverage | 3/5 | 3/5 | 2/5 | V1 and V2 name drift and restart risks |
| Invariants and edge cases | 2/5 | 3/5 | 2/5 | V2 names the persistence question |
| **qual_score** | **23/30 = 0.767** | **23/30 = 0.767** | **20/30 = 0.667** | |

## Position-Bias Mitigation
Pass 1 (V1, V2, V3) and pass 2 (V3, V2, V1) by the same in-context scorer, not independent. Re-checked V3 correctness and V2 completeness; no verdict changed.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final** | Debate points |
|---|---|---|---|---|
| V1 | 0.446 | 0.383 | **0.829** | 4 |
| V2 | 0.424 | 0.383 | **0.808** | 4 |
| V3 | 0.412 | 0.333 | **0.745** | 0 |

Margin V1 over V2: 2.6% (below 5%). Tiebreaker level 1 (debate points): 4 to 4, tied. Level 2 (correctness count): 5 to 5, tied. Level 3 (input order): V1. Base: V1.

## Selected Base: Variant 1 (proposal-A)

### Selection Rationale
V1 and V2 tie on every tiebreaker level; input order picks V1. The base is the starting text only: the debate gave V2 the route points (C-001, X-001, X-003, C-003), and two of three advocates picked V2 amended, so the merge replaces V1's route with V2's and keeps V1's discipline (pinned commit, a dated removal rule).

### Strengths to Preserve from Base
1. A concrete action that changes what the coordinator runs on this host.
2. A pinned commit, never a branch.

### Strengths to Incorporate
1. From V2: the Coder template as the route (`workflow_dispatch` to start the bump at once), then one owner-approved removal of the shadowing user-level install after the workspace update.
2. From V2 advocate: check `which -a superclaude` and `superclaude sweep --help` in the coordinator's own environment (a worktree `.venv` can come first).
3. From V3: "not runnable, XC-04 held" as the interim ledger record until both steps have run.
