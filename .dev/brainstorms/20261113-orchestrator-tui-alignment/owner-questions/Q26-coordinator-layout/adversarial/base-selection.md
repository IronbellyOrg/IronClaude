# Base Selection

Scored in-context by the worker that ran the skill (no separate scoring agent). Pass 1 read the variants in order 1, 2, 3; pass 2 in order 3, 2, 1, in the same context, so the position-bias mitigation is weaker than two independent evaluators. The single disagreement between passes is logged below.

## Quantitative Scoring (50% weight)

Requirements (RC) are the owner's answer of 2026-11-14, split into ten: R1 a coordinator branch per project; R2 a coordinator worktree; R3 a `.dev/coordinators/` directory; R4 may stay unmerged; R5 several developers with several coordinators on one project; R6 a naming convention for folders and files that avoids conflicts; R7 developers share the same space; R8 per-developer sub-directories explored; R9 per-epic sub-directories explored; R10 per-release sub-directories explored.

| Metric | Weight | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Basis |
|---|---|---|---|---|---|
| RC | 0.30 | 0.90 | 1.00 | 0.80 | A misses R8 (developer only a field); C misses R1 (branch per developer) and R7 (separate branches) |
| IC | 0.25 | 0.975 | 0.975 | 1.00 | about 40 claims each; A: X-002 (repeatable `g0001`); B: repeatable `<dev>-g<NNNN>` across one developer's coordinators (V2 advocate concession 3); C: none found |
| SR | 0.15 | 0.92 | 0.92 | 0.90 | concrete names, grammars and limits in all three; C slightly more prose |
| DC | 0.15 | 1.00 | 1.00 | 1.00 | every internal reference resolves |
| SC | 0.15 | 1.00 | 1.00 | 1.00 | 8 of 8 sections each |
| quant_score | | 0.952 | 0.982 | 0.925 | |

## Qualitative Scoring (50% weight)

MET = 1, NOT MET = 0. Evidence is a section of the variant.

| Dimension | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| Completeness | all source requirements | 0 | 1 | 0 | RC above |
| | edge cases and failures | 1 | 1 | 1 | Concurrency and Cost and risk sections |
| | dependencies | 1 | 1 | 1 | Relation to existing rules (Orca base, grants) |
| | success criteria | 0 | 0 | 0 | none states an acceptance check |
| | out of scope stated | 0 | 0 | 0 | none |
| Correctness | no factual errors | 0 | 0 | 0 | all three call `<orca-prefix>/<name>` "observed"; `brainstorm-reflect-panel` is on `ironbelly/shadow-runs` and `issue-409-mvp` on `409-Phase2` |
| | feasible | 1 | 1 | 1 | git conflict behaviour as described |
| | terminology consistent | 1 | 1 | 1 | |
| | no internal contradiction | 0 | 0 | 1 | IC above |
| | claims supported | 1 | 1 | 1 | Facts blocks |
| Structure | 5 criteria | 5 | 5 | 5 | identical structure, tables, cross-references |
| Clarity | 5 criteria | 5 | 5 | 5 | terms defined, grammar tables, unresolved items listed |
| Risk coverage | 3 risks with probability and impact | 0 | 0 | 0 | no probabilities |
| | mitigation for each | 0 | 0 | 0 | several risks left unresolved |
| | failure and recovery | 1 | 1 | 1 | forced takeover; lost claim; branch deletion |
| | external dependency failure | 0 | 0 | 0 | no GitHub or Orca outage handling |
| | monitoring | 1 | 1 | 1 | revision recorded per read |
| Invariants and edge cases | empty and boundary collections | 1 | 1 | 0 | A: empty `holder.md` = free; B: scope closed when every coordinator closed; C: none |
| | cross-component state | 1 | 1 | 1 | lease or claim versus dispatch; C names its race |
| | guard gaps named | 1 | 1 | 1 | |
| | count divergence | 1 | 1 | 1 | `-2` suffix rules |
| | interaction effects | 1 | 1 | 0 | release versus epic rule in A and B; none in C |
| Total | of 30 | 22 | 23 | 21 | |
| qual_score | | 0.733 | 0.767 | 0.700 | |

### Edge Case Floor Check
All three score at least 3 of 5 on invariants and edge cases; all eligible.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Final |
|---|---|---|---|---|
| no internal contradiction | V3 | NOT MET (scan stopped at "advisory" race) | MET (the race is stated, not contradicted) | MET: stating a weakness is not a contradiction |

Disagreements found: 1; verdicts changed: 1.

## Combined Scoring

| Variant | quant x 0.5 | qual x 0.5 | Score |
|---|---|---|---|
| Variant 2 (B) | 0.491 | 0.383 | 0.874 |
| Variant 1 (A) | 0.476 | 0.367 | 0.843 |
| Variant 3 (C) | 0.463 | 0.350 | 0.813 |

Margin Variant 2 over Variant 1: 0.031, inside the 5 percent band, so the tiebreaker applies. Level 1 (debate points won): Variant 2 won 8 points outright against Variant 1's 1. Tiebreaker applied: yes (level 1).

## Selected Base: Variant 2 (proposal B)

Selection rationale: it is the only variant that meets every part of the owner's answer (one branch, shared space, developer and scope sub-directories, several developers per epic) and the only one with a git-enforced, project-wide lock on the thing that collides (issue, PR, item). All three advocates' overall positions named it as the base.

Strengths to preserve: scope-first folders with developer sub-folders; project-wide create-once `claims/` keyed `issue-<N>`, `pr-<N>`, `item-<scope>-<id>`; "no pushed claim, no dispatch"; release claims only release-only items; archive as a state row; one readable ledger per coordinator.

Strengths to incorporate:
- From Variant 1: immutable one-file-per-entry for grants (S-003); a same-second suffix rule; an explicit statement that an unpushed claim or folder is not real.
- From Variant 3: the `adhoc` kind (C-009); a push grant narrowed by path (C-008, adapted to one branch); no host or contact details in pushed files (A-006); a coordinator may stay unpushed only if it dispatches nothing (A-006 reconciled with C-003).
- From the advocates' concessions: a written conflict rule for `claims/` (abort, never resolve in one's own favour); claim bodies always unique; grant and row ids qualified by the coordinator; the handle in the worktree name (A-002); identity read from `gh` and frozen (A-001); a stale-base reading rule (A-004); a never-force-push rule (A-003).
