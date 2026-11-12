# Base Selection Report

Variant 1 = reviewer 1 card (sonnet:analyzer). Variant 2 = reviewer 2 card (haiku:qa). Scored by the orchestrator (opus, debate-orchestrator role, not a debater).

## Quantitative Scoring (50% weight)

RC, SR, DC and SC computed by `/tmp/reflect-containment/quant.py` (deterministic: 34 inferred source requirements from `artifacts/inferred-requirements.yaml`, content-word containment ≥ 0.6 over the whole card; concrete/vague indicator regex; `R1-n`/`R2-n` references resolved against finding-table rows; H2 count). IC counted by hand from the diff analysis (no intra-variant contradiction found in either card; X-001..X-004 are all cross-variant).

| Metric | Weight | Variant 1 (sonnet:analyzer) | Variant 2 (haiku:qa) |
|--------|--------|-----------------------------|----------------------|
| requirement_coverage | 0.30 | 0.941 (32/34; misses INF-004, INF-020) | 0.882 (30/34; misses INF-004, INF-008, INF-024, INF-026) |
| internal_consistency | 0.25 | 1.000 (0 contradictions) | 1.000 (0 contradictions) |
| specificity_ratio | 0.15 | 1.000 (306 concrete, 0 vague) | 1.000 (191 concrete, 0 vague) |
| dependency_completeness | 0.15 | 1.000 (13/13 refs) | 1.000 (9/9 refs) |
| section_coverage | 0.15 | 0.833 (5/6 H2) | 1.000 (6/6 H2) |
| **quant_score** | | **0.957** | **0.965** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV evidence is abbreviated to the decisive citation in each card.

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Covers all explicit requirements | MET | §2 table traces scope items (1)-(3), out-of-scope, respect list | NOT MET | No source-item trace; `--help` allowance (INF-008) and out-of-scope list not addressed |
| Addresses edge cases/failures | MET | R1-3 count 0, R1-8 failed launch | MET | R2-5 unknown reply, R2-6 identity |
| Includes dependencies/prerequisites | MET | R1-12 `superclaude update`, R1-13 hook ordering | MET | R2-3 ordering, F9 verify-sync concurrency |
| Defines success/completion criteria | MET | R1-1 test list, R1-6 acceptance greps | MET | Per-task "would fail on wrong work?" table |
| Specifies out-of-scope items | MET | §2 rows for WC-13, worker-start, Orca, existing tabs | NOT MET | Searched all sections; none |
| **Subtotal** | **5/5** | | **3/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| No factual errors | NOT MET | R1-6 lists SKILL.md :89, :92 (already conditioned); R1-11 attributes an enforcement claim to Constraints :19 that the plan does not make | NOT MET | "Drift" label contradicts §10.3 (withdrawn in R2); F3 refutation only partly right (C-012) |
| Feasible approaches | MET | Remedies keep existing guards (close after :513) | NOT MET | "Restore agent-on-create" omits failed-copy = no agent (conceded R2 item 5) |
| Consistent terminology | MET | | MET | |
| No internal contradictions | MET | IC 1.000 | MET | IC 1.000 |
| Claims supported by evidence | MET | Calibrator: 13 held, 0 failed | MET | Calibrator: 22 held, 0 failed |
| **Subtotal** | **4/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Logical section ordering | MET | grade → coverage → findings → deviations → confidence | MET | grade → per-task → findings → T1 checks → deviations → limits |
| Consistent hierarchy | MET | | MET | |
| Separation of concerns | MET | | MET | |
| Navigation aids | MET | "vs T1" column | MET | "vs T1" column, path labels |
| Artifact-type conventions | MET | | MET | |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Unambiguous language | NOT MET | "Covered, borderline", "Covered, with gaps" | MET | |
| Concrete | MET | | MET | |
| Each section has a clear purpose | MET | | MET | |
| Terms defined on first use | NOT MET | FO-18, D2, WC-13 undefined | NOT MET | FO-11, ST-9, ST-10 undefined |
| Actionable next steps | NOT MET | No go/no-go (S-007) | MET | "Return the plan for revision; resolve R2-4 first" |
| **Subtotal** | **2/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| ≥3 risks with probability and impact | MET | R1-3 timing likelihood, R1-2 matcher likelihood, severities | NOT MET | Severity only; likelihood not weighed (calibrator note on R2-5/R2-6) |
| Mitigation per risk | MET | Recommended-change column | MET | Recommended-change column |
| Failure modes and recovery | MET | R1-8 recovery via claim.md:123 | NOT MET | Launch-failure recovery not covered (conceded R1) |
| External dependencies | MET | Installed Orca vs checkout; hook install | MET | Installed Orca schemas; live ordering |
| Monitoring/validation mechanism | MET | Task 8 live check as ship gate | MET | Tests per finding |
| **Subtotal** | **5/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Collection boundaries | MET | R1-3 count 0 | MET | Zero-terminal tests (R2-5) |
| State interactions across components | MET | R1-13, R1-10 | MET | R2-3 |
| Guard condition gaps | MET | R1-4 | MET | R2-5, R2-6 |
| Count divergence | MET | R1-1 "all 12 listed tests"; exactly-one-terminal gate | NOT MET | No count analysis beyond "five-call assertion" |
| Interaction effects | MET | R1-1 cross-command flag | MET | Both command orders, nested substitution (R2-1) |
| **Subtotal** | **5/5** | | **4/5** | |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Completeness | 5/5 | 3/5 |
| Correctness | 4/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 2/5 | 4/5 |
| Risk Coverage | 5/5 | 3/5 |
| Invariant & Edge Case | 5/5 | 4/5 |
| **qual_score** | **26/30 = 0.867** | **22/30 = 0.733** |

### Edge Case Floor Check

V1 5/5 eligible; V2 4/5 eligible.

## Position-Bias Mitigation

Pass 1 evaluated V1 then V2; pass 2 evaluated V2 then V1. Both passes were run by the same judge (the orchestrator), which is a stated limitation: the reversal guards against order effects, not against one judge's view.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Correctness: feasible approaches | V2 | NOT MET | MET ("adjust ordering/tests" read as covering the guard) | DISAGREE | NOT MET: V2's R2 item 5 concedes the remedy omitted the failed-copy guarantee |

Disagreements re-evaluated: 1. Final verdicts changed: 0.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (sonnet:analyzer) | 0.479 | 0.433 | **0.912** | not needed |
| V2 (haiku:qa) | 0.482 | 0.367 | **0.849** | not needed |

**Margin**: 6.3 points (above the 5% threshold). **Tiebreaker applied**: No.

## Selected Base: Variant 1 (sonnet:analyzer)

### Selection Rationale

V1 traces every source item and out-of-scope item, covers failure and recovery paths (failed launch, timing), and its load-bearing citations all held under calibration (C = 0.83 vs V2 0.89, but V2's higher calibration rests on fewer, narrower claims). V2 wins Clarity and contributes the two most consequential test-level findings, which are merged in.

### Strengths to Preserve from Base

1. Source-item coverage table (§2) and the classification of the plan's own additions.
2. Task 1 scanner mechanics (R1-1) and matching rule (R1-2).
3. Reply-envelope analysis and `--tab` choice (R1-4, R1-5); failed-launch consequence (R1-8); timing race (R1-3).
4. Residual-scope notes: docstring (R1-9), WC-13 qualifier (R1-10), not-covered actors (R1-12).

### Strengths to Incorporate from Non-Base Variants

1. V2 R2-5: unknown/malformed/timed-out reply → no close; `created_scene()`/FO-11 fixture conflict; valid-reply fixture (raise R1-4 to HIGH).
2. V2 R2-6 (at MEDIUM): repository identity before any close, foreign-repo fixture.
3. V2 R2-2 fail-open and full-message tests; R2-3 executable interaction test (replaces R1-13 remedy).
4. V2 R2-7 null worktree fields and ten-key pin; R2-8 user guide and HOW-WE-WORK.md:329; R2-9 ownership assertions.
5. V2 per-task acceptance table, F2/F8/F9 rulings, actionable verdict.
6. Invariant probe INV-001 (HIGH) and the MEDIUM UNADDRESSED items.
