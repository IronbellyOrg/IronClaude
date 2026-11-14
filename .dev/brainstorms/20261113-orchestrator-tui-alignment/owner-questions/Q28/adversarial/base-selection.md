# Base Selection Report (Q28)

Scored by the orchestrating worker in-context. Requirements used for coverage (8): (1) no tool before the ruling; (2) gate on the Codex thread being resolved; (3) no tool designs an INV-008 fix (`merged-requirements.md:191`); (4) stop before acting on a finding that needs an owner ruling (`:194`); (5) every tool write listed in a grant row (`:1050`); (6) PR-open check before each push (owner memory); (7) uses the project's review loop; (8) no merge by the tool.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (proposal-A) | V2 (proposal-B) | V3 (proposal-C) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.500 (4/8: misses 1 via level-1 option, 2, 3, 6) | 0.375 (3/8: misses 2, 3, 5 auggie comment, 6, 7) | 0.750 (6/8: misses 6, 7) |
| internal_consistency | 0.25 | 1.00 | 1.00 | 1.00 |
| specificity_ratio | 0.15 | 0.85 | 0.85 | 0.85 |
| dependency_completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **0.828** | **0.790** | **0.903** |

## Qualitative Scoring (50% weight)

| Dimension | V1 | V2 | V3 | Decisive evidence |
|---|---|---|---|---|
| Completeness | 4/5 | 3/5 | 3/5 | V1 lists every write; V2 misses the decline-fallback comment; V3 has no exit or PR-open check |
| Correctness | 4/5 | 4/5 | 5/5 | V1 and V2 gate on "closed by reply", which leaves the thread selectable (`detection-contract.md:132-136`) |
| Structure | 5/5 | 5/5 | 5/5 | identical |
| Clarity | 4/5 | 4/5 | 4/5 | ids unglossed |
| Risk coverage | 3/5 | 3/5 | 3/5 | each names its main risk; none quantifies |
| Invariants and edge cases | 3/5 | 3/5 | 3/5 | late Codex review, mid-cycle merge, two sessions |
| **qual_score** | **23/30 = 0.767** | **22/30 = 0.733** | **23/30 = 0.767** | |

## Position-Bias Mitigation
Pass 1 (V1, V2, V3) and pass 2 (V3, V2, V1) by the same in-context scorer, not independent. Re-checked: V3 completeness (kept 3/5), V1 correctness (kept 4/5). Disagreements: 0.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final** | Debate points |
|---|---|---|---|---|
| V1 | 0.414 | 0.383 | **0.797** | 4 |
| V2 | 0.395 | 0.367 | **0.762** | 4 |
| V3 | 0.451 | 0.383 | **0.834** | 1 |

Margin V3 over V1: 3.7% (below 5%). Tiebreaker level 1 (debate points): V1 4, V3 1. Base: V1.

## Selected Base: Variant 1 (proposal-A)

### Selection Rationale
V3 and V1 are within the tie band; V1 wins on debate points (standard loop, tool push checks, one session). V3's strongest point (a new git-configuration finding is likely right after SW-02's push, and level 3 would fix it alone) is merged in as an extra gate, not discarded.

### Strengths to Preserve from Base
1. Level 3 after the ruling, under a grant row that lists every write; never merge.
2. One session (the #539 author) runs it.

### Strengths to Incorporate
1. From all three: no level 1 before the ruling; gate on "resolved".
2. From V3: wait until Codex's review of SW-02's push has come back with no new git-configuration finding before attaching the tool.
3. From V2 and V3: a written stop rule for any git-configuration finding; PR-open and head check before each push (the `--merge-guard off` path may skip it, `SKILL.md:309` versus `refs/merge-guard.md:94-97`).
4. From V2: list the decline-fallback `/sc:auggie-review` PR comment in the grant row or hold on a decline.
