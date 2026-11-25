# Base Selection Report

Variant A = OURS (`variant-1-original.md`). Variant B = CLAY (`variant-2-original.md`). Source input has no formal requirement IDs, so requirement coverage uses topic matching on eight topics taken from the D06 question (merge, coordinator start, `/sc:pr-submit` as worker, reviewer hold, WORKER-CONTRACT lines, skip rule, approvals in chat, typed answers). Quantitative numbers were computed by a read-only script (`uv run python -I`) over the two files.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (OURS) | Variant B (CLAY) |
|--------|--------|------------------|------------------|
| requirement_coverage | 0.30 | 1.000 (8 of 8 topics matched) | 1.000 (8 of 8 topics matched) |
| internal_consistency | 0.25 | 0.952 (1 contradiction X-005 in 21 claims) | 0.955 (1 contradiction X-004 in 22 claims) |
| specificity_ratio | 0.15 | 1.000 (19 concrete, 0 vague indicators) | 1.000 (19 concrete, 0 vague indicators) |
| dependency_completeness | 0.15 | 1.000 (the one internal reference, "memory note above", resolves) | 1.000 (no unresolved internal references) |
| section_coverage | 0.15 | 1.000 (6 of 6 H2) | 1.000 (6 of 6 H2) |
| **quant_score** | | **0.988** | **0.989** |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Two independent evaluator agents scored all 30 criteria with Claim-Evidence-Verdict. Pass 1 (order A then B): agent add4b9e20e05dff77. Pass 2 (order B then A): agent ad7d424a67342d05e. Where the passes agreed the verdict stands; where they disagreed the verdict below is the orchestrator's re-evaluation citing both passes. IDs: C completeness, K correctness, T structure, L clarity, R risk coverage, E invariant and edge case coverage.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| C1 covers all explicit requirements | MET | merge, coordinator start, worker pr-submit, reviewer hold, and a safe subset (R25, R9/R17) | NOT MET | covers the four authority points, but carves out no safe subset (re-evaluated, see log) |
| C2 edge cases and failure scenarios | MET | PR 368 merged mid-cycle; late Codex security review | MET | restart never merges twice; short file list holds; 60 minute bound |
| C3 dependencies and prerequisites | MET | D5 depth precondition; AC-4.3 never run; R25 unpushed | MET | merge-gate and answer-check unbuilt; waker.py pattern; ccsession |
| C4 success or completion criteria | NOT MET | no explicit completion criteria | MET | merge condition: every listed reviewer finished on the final head |
| C5 out of scope | NOT MET | no scope section (re-evaluated; "deferred, not rejected" is a D3 fact, not a scope statement) | NOT MET | only prohibitions on flags, no scope section |
| **Subtotal** | **3/5** | | **3/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| K1 no factual errors | MET | contract lines :23, :70, :241, :244, :245 verified by both evaluators | MET | D:112, :118, :135, :138, :694 verified |
| K2 feasible with stated constraints | MET | uses R25 and R9 routes | MET | waker.py pattern runs; but unbuilt and reverses D3/D4/D5 |
| K3 terminology consistent | MET | coordinator, person, go used consistently | NOT MET | "orchestrator" and "coordinator" interchanged, undefined |
| K4 no internal contradictions | NOT MET | "three owner decisions (D3, D4, GIT)" in "gets right" against four listed in fact 1; R25 against :245 (X-005) (re-evaluated) | MET | spoofable source is admitted as a risk, not contradicted |
| K5 claims supported | MET | nine facts with file:line | MET | D:nnn cites throughout |
| **Subtotal** | **4/5** | | **4/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| T1 logical ordering | MET | claim, mechanism, facts, costs, risks, strengths | MET | same |
| T2 consistent hierarchy | MET | uniform H2 and numbered lists | MET | same |
| T3 separation of concerns | MET | costs, risks, strengths separate | MET | same |
| T4 navigation aids | MET | numbered facts; path legend | MET | numbered facts; "D:nnn" legend |
| T5 type conventions | MET | position-paper form | MET | opens with "strongest honest case" |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| L1 unambiguous language | MET | "never merges on its own initiative" | NOT MET | "row 9", "ruling 5", "AU4a" unexplained (re-evaluated) |
| L2 concrete | MET | quotes contract lines, rows R25, R9 | MET | exact `gh pr merge` flags, 13 reasons |
| L3 clear purpose per section | MET | one purpose per heading | MET | same |
| L4 terms defined on first use | MET | D3, D4, D5, GIT glossed in fact 1 | NOT MET | DQ2, ADD1, G1, FR-17, AU4a undefined |
| L5 actionable next steps | MET | facts 7-8: Full Submit and script start as adoptable subset | NOT MET | no next steps |
| **Subtotal** | **5/5** | | **2/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| R1 at least 3 risks with probability and impact | NOT MET | risks listed, no probability or impact | NOT MET | same |
| R2 mitigation for each risk | NOT MET | "no separate merge-time check", no mitigation | NOT MET | no mitigation for the unprotected-master risk |
| R3 failure modes and recovery | NOT MET | PR 368 branch re-created; no recovery given | MET | fails closed; PR state read first after restart |
| R4 external dependencies and failure | MET | late reviewer; unprotected master | MET | absent reviewer holds; 60 minute bound |
| R5 monitoring or validation mechanism | NOT MET | none proposed for its own model (re-evaluated; AC-4.3 belongs to the deferred D3 option) | MET | action log; answer-check results; AU4a audit |
| **Subtotal** | **1/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| E1 collection boundaries | NOT MET | no empty, single or maximum reviewer cases | MET | reviewers: both, one or `none`; missing file list |
| E2 state interactions across boundaries | MET | owner merge then round-2 push re-created the branch | MET | OK bound to question key and head sha |
| E3 guard condition gaps | MET | "nothing mechanical binds the coordinator" | MET | source cannot tell person from script |
| E4 count divergence | NOT MET | none | NOT MET | none |
| E5 interaction effects | MET | R25 auto-submit plus reviewer skip gives a false "clean" | MET | late reviewer plus unprotected master plus moved head |
| **Subtotal** | **3/5** | | **4/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 3/5 | 3/5 |
| Correctness | 4/5 | 4/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 2/5 |
| Risk Coverage | 1/5 | 3/5 |
| Invariant & Edge Case | 3/5 | 4/5 |
| **qual_score** | **21/30 = 0.700** | **21/30 = 0.700** |

### Edge Case Floor Check

Threshold 1/5. Variant A: 3/5, eligible. Variant B: 4/5, eligible.

## Position-Bias Mitigation

Raw totals: Pass 1 A 22, B 22; Pass 2 A 23, B 22.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| C5 | A | NOT MET | MET | DISAGREE | NOT MET (the cited "deferred, not rejected" is a D3 fact, not a scope statement) |
| K4 | A | MET | NOT MET | DISAGREE | NOT MET (the "three owner decisions" count omits D5; R25 against :245) |
| R5 | A | NOT MET | MET | DISAGREE | NOT MET (AC-4.3 validates the deferred D3 option, not A's own model) |
| C1 | B | NOT MET | MET | DISAGREE | NOT MET (no safe subset carved out, which the question asks for) |
| L1 | B | MET | NOT MET | DISAGREE | NOT MET (undefined codes make the sentences ambiguous to an outside reader) |

All other 55 criterion-variant pairs agree. Disagreements re-evaluated: 5. Final verdicts changed from one of the passes: 5 (each re-evaluation sided with the NOT MET pass; this is the stricter reading the CEV rule asks for. Final A is 21 (passes gave 22 and 23) and final B is 21 (passes gave 22 and 22), so the re-evaluation costs each side points and favours neither).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (OURS) | 0.4940 | 0.3500 | **0.8440** | 8 points won (S-002, C-001, C-003, C-006, C-007, C-008, C-010, X-002) |
| B (CLAY) | 0.4943 | 0.3500 | **0.8443** | 4 points won (C-004, X-001, X-003, X-005) |

**Margin**: 0.03% (far below the 5% threshold)
**Tiebreaker applied**: Yes, level 1 (debate performance): A won 8 points, B won 4. A is the base.

## Selected Base: Variant A (OURS)

### Selection Rationale
The two papers score the same (0.844 against 0.844); the 0.0003 numeric edge to B is inside the tie band and is decided by the Step 2 scoring matrix, where A's position won eight points and B's four (and A's position carried the agreed hybrid on the four contested authority questions C-001, C-003, C-006, C-007). The owner's weighting rule (OURS wins unless CLAY shows a clear, evidenced benefit; a tie goes to OURS) points the same way and is not needed to decide it. The base choice only decides which paper the merge starts from.

### Strengths to Preserve from Base
1. The authority rule: the person's named go for each merge; `/sc:pr-submit` never an Orca worker; coordinator rules tied to owner decisions D3, D4, D5 and GIT (APPROVED.md:10-13).
2. The owner-recorded route to automation (R25 Full Submit as a per-issue go, R9/R17 launch-prompt authorization) with the explicit note that these need a contract amendment first.
3. Clear defined terms and plain statements (clarity 5/5).

### Strengths to Incorporate from Non-Base Variants
1. From Variant B: the merge-gate verb as a read-only check before the go (13 closed reasons, head-pinned `gh pr merge`, fail-closed file list, restart reads PR state first), Section "The mechanism" items 1 to 3 and facts 1 and 9.
2. From Variant B: the merge-time reviewer hold on the final head with an owner-set per-repo `reviewers` list (fact 2, fact 3, fact 4).
3. From Variant B: `answer-check` as a validator of stale or mismatched chat answers, with the source limit stated (mechanism item 4, fact 5).
4. From Variant B: `E-NO-GRANT` (the verb refuses any GitHub write not on an owner-recorded list, with no `pr.merge`), fact 5 and rebuttal item 4.
5. From Variant B: the depth-0 script start by terminal and ccsession (fact 7), with A's launch-prompt authorization condition.
6. From Variant B: the nine-row list as a reasons list for non-outward decisions (fact 6), adopted only after an owner chat decision.
7. From Variant B: the "risks written down with mitigations" habit (K12) and the post-merge audit idea (AU4a, AU7).
8. From the invariant probe: the closures for INV-001 to INV-013 become required spec items (see `refactor-plan.md`).
