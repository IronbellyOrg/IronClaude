# Base Selection Report (Q26)

Scored by the orchestrating worker in-context (not a separate agent). Requirement list used for requirement coverage (8, from `question.md` and spec rules): (1) names a home; (2) names the ledger branch; (3) coordinator certainly person-opened (`WORKER-CONTRACT.md:69`, `merged-requirements.md:457` part 1); (4) not in the #539 checkout; (5) no session creates a worktree for its own use; (6) coordinator never switches a branch itself; (7) grant table on disk (`merged-requirements.md:449` part 5); (8) Orca gate acknowledged.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (proposal-A) | V2 (proposal-B) | V3 (proposal-C) |
|--------|--------|-----------------|-----------------|-----------------|
| requirement_coverage | 0.30 | 0.875 (7/8; (3) unverified) | 1.000 (8/8) | 0.500 (4/8; (1), (2), (3), (7) not met) |
| internal_consistency | 0.25 | 1.00 (0 contradictions) | 0.90 (cites "Session A ... (current branch)" yet switches branch) | 1.00 |
| specificity_ratio | 0.15 | 0.85 | 0.90 (measured facts) | 0.75 |
| dependency_completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 (5/5) | 1.00 | 1.00 |
| **quant_score** | | **0.940** | **0.960** | **0.813** |

Specificity was estimated by counting concrete statements (commands, paths, counts, dates) against vague ones per file; it is an estimate, not a mechanical count.

## Qualitative Scoring (50% weight), additive binary rubric

| Dimension | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| Completeness | all requirements | NOT MET (person-opened unverified, variant-1 "costs" bullet 1) | MET | NOT MET (no home, no branch) |
| | edge cases | MET (Orca down; first-screen check) | MET (refused switch; `git add .dev` risk) | MET (grants off disk) |
| | dependencies | MET (Orca) | MET (owner switch; Orca) | MET (Orca; rulings) |
| | success criteria | MET (XC-10 (3) records path) | MET (XC-10 (3)) | MET (XC-10 (3) "held") |
| | out of scope stated | NOT MET | NOT MET | NOT MET |
| Correctness | no factual errors | MET | NOT MET (step 1: untracked entries "stay in the folder across a branch switch"; the switch aborts, verified 2026-11-14) | MET |
| | feasible | MET | MET (after a clean-up step) | MET |
| | terminology consistent | MET | MET | MET |
| | no internal contradictions | MET | MET | MET |
| | claims supported | MET | MET | MET |
| Structure | logical order; hierarchy; separation; cross-references; conventions | 5 MET | 5 MET | 5 MET |
| Clarity | unambiguous; concrete; section purpose; actionable | 4 MET | 4 MET | 4 MET |
| | ids glossed on first use | NOT MET (XC-10, XC-09 unglossed) | NOT MET | NOT MET |
| Risk | 3+ risks with probability and impact | NOT MET | NOT MET | NOT MET |
| | mitigation per risk | NOT MET | NOT MET | NOT MET |
| | failure modes and recovery | MET | MET | MET |
| | external dependencies | MET (Orca) | MET | MET |
| | monitoring | MET (first-screen check) | NOT MET | MET (re-ask trigger) |
| Invariants | empty collections | NOT MET | NOT MET | NOT MET |
| | state across boundaries | MET (only program files on branch) | MET (untracked entries beside ledger) | MET (agents cannot read grants) |
| | guard gaps | MET (person-opened) | MET (refused switch) | MET |
| | count divergence | NOT MET | NOT MET | NOT MET |
| | interaction effects | MET (host worktree load) | MET (shared branch with other work) | MET (conflict with always-staged practice) |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3/5 | 4/5 | 3/5 |
| Correctness | 5/5 | 4/5 | 5/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk coverage | 3/5 | 2/5 | 3/5 |
| Invariants and edge cases | 3/5 | 3/5 | 3/5 |
| **qual_score** | **23/30 = 0.767** | **22/30 = 0.733** | **23/30 = 0.767** |

Edge case floor (at least 1/5): all eligible.

## Position-Bias Mitigation

Pass 1 in input order (V1, V2, V3) and pass 2 in reverse order (V3, V2, V1), both by the orchestrating worker in this context, so they are not independent. Criteria re-checked in pass 2 against evidence: V2 "no factual errors" (kept NOT MET: reproduced git abort), V1 "all requirements" (kept NOT MET: no source says an `--agent` session is person-opened), V3 "monitoring" (kept MET). Disagreements re-evaluated: 0. Final verdicts changed: 0.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final** | Debate points won |
|---|---|---|---|---|
| V1 (proposal-A) | 0.470 | 0.383 | **0.853** | 5 |
| V2 (proposal-B) | 0.480 | 0.367 | **0.847** | 4 |
| V3 (proposal-C) | 0.406 | 0.383 | **0.790** | 0 |

**Margin**: V1 over V2 0.6% (below the 5% threshold). **Tiebreaker applied**: yes, level 1 (debate points: V1 5, V2 4).

## Selected Base: Variant 1 (proposal-A)

### Selection Rationale
V1 and V2 are statistically tied; V1 wins the tiebreaker on debate points because the git-state points (A-001 staged files travel with a switch, A-002 one live session per checkout, C-002, C-004) all went to V1 unanimously, and the orchestrator's verification added a fact against V2 (the switch to an origin/master branch aborts until 34 identical untracked copies are cleared). V2 keeps the single most important point, X-001: only V2 is certainly person-opened. The merged answer therefore keeps V1's home on the condition that the owner settles X-001, and falls back to V2 with mitigations if the owner does not.

### Strengths to Preserve from Base
1. A dedicated checkout whose index never changes branch (A-001).
2. One live session in the coordinator home by construction (A-002).
3. Main checkout untouched (C-004).

### Strengths to Incorporate from Non-Base Variants
1. From V2: the person-opened requirement (X-001) as an explicit owner condition, and V2 itself as the fallback home.
2. From V2 advocate: the no-switch, no-other-commit rule for the main checkout while the ledger is staged uncommitted (fallback only).
3. From V3 and the orchestrator check: the clean-up precondition for the main-checkout switch (fallback only).
4. From V3: if Orca is still unreachable when the owner answers, the answer is recorded and the home is created at the first successful Orca read; meanwhile the owner holds the ledger, with the grant rows the W0 items need written out in full.
