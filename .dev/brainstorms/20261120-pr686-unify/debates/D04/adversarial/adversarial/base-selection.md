# Base Selection Report (D04 claim level and grants)

## Quantitative Scoring (50% weight)

Computed by the orchestrator from the variant text. Source requirements: the 7 required items of the brief and topic (claim, mechanism, 5 to 10 cited facts, costs, risks, gets-right, `/sc:issue --claim` flag semantics).

| Metric | Weight | Variant A (OURS) | Variant B (CLAY) |
|--------|--------|------------------|------------------|
| requirement_coverage | 0.30 | 1.000 (7/7) | 0.857 (6/7: only `--pipeline none` is described; no `worktree`, `full` or `--submit` semantics) |
| internal_consistency | 0.25 | 0.90 (2 contradicted claims of about 20: X-002, X-003) | 0.90 (2 of about 20: X-003, X-004) |
| specificity_ratio | 0.15 | 1.00 (131 concrete indicators, 0 vague, by grep) | 1.00 (136 concrete, 0 vague) |
| dependency_completeness | 0.15 | 1.00 (no unresolved internal reference) | 1.00 |
| section_coverage | 0.15 | 1.00 (6 H2) | 1.00 (6 H2) |
| **quant_score** | | **0.975** | **0.932** |

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Two independent evaluator agents scored all 30 criteria for both variants (pass 1 order A then B, agent a79d508e460698910; pass 2 order B then A, agent a51a7caa6eca8b139). Verdicts below are the agreed or re-evaluated final ones. Evidence is the shortened Claim-Evidence-Verdict citation.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| C1 covers all explicit requirements | MET | Mechanism 1 maps None/Worktree/Full/Full Submit to `--pipeline` and `--submit` | NOT MET | Only `--pipeline none`; no `worktree`, `full` or `--submit` semantics |
| C2 edge cases and failures | MET | `W-ENFORCEMENT-ABSENT` refusal; empty Pipeline means None | MET | `E-NO-GRANT` refusal; `answer-check` rejects relayed or stale answers |
| C3 dependencies and prerequisites | MET | Guard (issue 394), 12 observations, issue 442, `Approved` field | MET | `repos.yaml`, `answer-check`, PR B contract rewrite (ADD1) |
| C4 success or completion criteria | MET | Governed claim forbidden until the 12 observations pass and a reviewed commit flips the gate | NOT MET | No completion criteria for the none-only route |
| C5 out-of-scope stated | NOT MET | None stated | NOT MET | None stated |
| **Subtotal** | **4/5** | | **2/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| K1 no factual errors | NOT MET | "the control that exists today" overstated; Q36 misread in costs | NOT MET | Fact 5 misreads Q36; `E-NO-GRANT` covers at most 2 of 6 entries (D:696) |
| K2 feasible approach | MET | Guard, level state outside worktree, closed gate | MET | Fixed built command, standing list, verbs |
| K3 consistent terminology | MET | "Pipeline", "level", "grant row" used steadily | MET | "grants", "worker-start", "orchestrator" steady |
| K4 no internal contradictions | NOT MET | Fact 3 vs cost 1 (X-002) | MET | Costs and risks do not contradict the claim |
| K5 claims supported | NOT MET | "Only per-issue throttle" rests on an UNVERIFIED fact (fact 4) and was refuted in Round 2 | NOT MET | "Refuses a write outside the list" and fact 5 lack support (INV-006, X-003) |
| **Subtotal** | **2/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| S1 logical order | MET | Claim, Mechanism, Facts, Costs, Risks, Gets right | MET | Same order |
| S2 consistent hierarchy | MET | Uniform H2 and lists | MET | Same |
| S3 separation of concerns | MET | Cost (today) and risk (future) are distinct; re-evaluated after a pass disagreement | MET | Costs and risks distinct |
| S4 navigation aids | MET | "same doc, lines 19-26"; R and D references | MET | R and D references |
| S5 conventions of the artifact | MET | All required sections, 8 facts | MET | All required sections, 8 facts |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| L1 unambiguous language | MET | Explicit flag mapping | MET | "always at `--pipeline none`"; code names are covered by L4; re-evaluated after a pass disagreement |
| L2 concrete | MET | Paths, lines, constant | MET | Regex, six entries, error code |
| L3 clear section purpose | MET | One purpose per section | MET | Same |
| L4 acronyms defined | NOT MET | R23, D:, DQ7, K12, OB-H1 undefined | NOT MET | D:, DQ6, DQ7, K12, ADD1, N1 undefined |
| L5 actionable next step | MET | Gate flip after observations and a reviewed commit | NOT MET | No next step named |
| **Subtotal** | **4/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| R1 at least 3 risks with probability and impact | NOT MET | 3 risks, no probability or impact | NOT MET | 2 risks, no probability or impact |
| R2 mitigation per risk | NOT MET | None | NOT MET | None ("verb and a test" only describes) |
| R3 failure modes and recovery | NOT MET | Refusal stated, no recovery | NOT MET | Refuse-and-log stated, no recovery |
| R4 external dependencies | MET | Guard absent means the claim refuses | MET | Removing Project reads drops the GraphQL failure class |
| R5 monitoring or validation | MET | 12 observation tests and a guard the agent cannot edit | MET | `E-NO-GRANT` log, test rows, mailbox heartbeats |
| **Subtotal** | **2/5** | | **2/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| E1 collection boundaries | MET | "an empty Pipeline means None" | NOT MET | No empty, single or max handling |
| E2 state interactions across components | MET | Level in `~/.claude/state/launch-level/pending/<nonce>` | MET | Orchestrator edits `repos.yaml`; mailbox |
| E3 guard-condition gaps | MET | Guard does not see `worker-start`; standing list self-edit gap | MET | Orchestrator edits its own grants; no L1 or L2 |
| E4 count divergence | MET | 12 = 9 + 3; four board values vs three flags plus `--submit` | MET | Six grants; 12 observations |
| E5 interaction effects | MET | Status x Pipeline matrix; Pipeline plus `Approved` | MET | Standing `pr.merge` plus unguarded workers plus unprotected master |
| **Subtotal** | **5/5** | | **4/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 2/5 |
| Correctness | 2/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 3/5 |
| Risk Coverage | 2/5 | 2/5 |
| Invariant & Edge Case | 5/5 | 4/5 |
| **qual_score** | **22/30 = 0.733** | **19/30 = 0.633** |

Note: B's pass 1 total was 20 and its pass 2 total 18. Final: K5 re-evaluated to NOT MET (the same strictness applied to A's K5) and L1 kept MET, so B = 2+3+5+3+2+4 = 19. A's pass 1 total was 21 and its pass 2 total 22; after re-evaluating S3 to MET, A = 22.

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Eligible as base |
|---------|-----------------------------|------------------|
| A | 5/5 | Yes |
| B | 4/5 | Yes |

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| S3 | A | NOT MET | MET | DISAGREE | MET (cost and risk are separate sections; the overlap is thematic) |
| K5 | B | MET | NOT MET | DISAGREE | NOT MET (same strictness applied to A's K5) |
| L1 | B | MET | NOT MET | DISAGREE | MET (the undefined codes are scored once, under L4) |

Disagreements re-evaluated: 3 of 60 criterion-variant pairs
Final verdicts changed from one of the passes: 3 (two overturned pass 1, one overturned pass 2)

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (OURS) | 0.4875 | 0.3667 | **0.854** | not needed |
| B (CLAY) | 0.4660 | 0.3167 | **0.783** | not needed |

**Margin**: 7.1 points (above the 5% threshold)
**Tiebreaker applied**: No

## Selected Base: Variant A (OURS, position-OURS.md)

### Selection Rationale
Variant A scores higher on requirement coverage (it explains the `--pipeline` and `--submit` flag semantics the topic asked for), on edge cases (empty Pipeline, level state outside the worktree) and on actionable next step (the gate flip). Both papers share the same correctness defects (the Q36 misread and an overstated claim); no paper has risk probabilities or mitigations. The base score concerns the paper, not the answer: the debate result is a hybrid, and the refactoring plan moves the live rule and four controls from Variant B into the base.

### Strengths to Preserve from Base
1. The `/sc:issue --claim` flag semantics and board-value mapping (Mechanism 1), including `--submit` only with `--pipeline full`.
2. Level state outside the worktree and the fail-closed refusal `W-ENFORCEMENT-ABSENT`.
3. The Full Submit push rule: Pipeline value plus `Approved` field is the person's go for that issue's push only (U-001).
4. The ship gate and the 12 pending observations as the condition for any governed level.

### Strengths to Incorporate from Non-Base Variants
1. From Variant B, Mechanism 1 and Cited fact 1: the live rule is a claim at `--pipeline none`; one supervised `worker-start` route (C-001, C-002, C-004).
2. From Variant B, Mechanism 3 and 4: `E-NO-GRANT`, `answer-check`, closed `refuse(argv)` list, scoped to what they really cover (U-003, U-004, C-008, INV-004, INV-006).
3. From Variant B, Mechanism 2: mailbox supervision, one message handled once per id (U-005).
4. From Variant B, Cited fact 8: no Project read while the gate is closed (U-006, C-009).
5. From Variant B, Cited fact 5, with the Q36 misread removed: the standing grant for low-stakes writes (C-006).
