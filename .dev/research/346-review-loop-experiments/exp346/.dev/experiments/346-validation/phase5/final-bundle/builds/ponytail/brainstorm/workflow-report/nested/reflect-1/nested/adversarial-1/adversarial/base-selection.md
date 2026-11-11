# Base Selection Report

Scoring by the orchestrator. The "requirements" for these review cards are the 9 confirmed merged finding clusters (C-001..C-007, C-009, C-010; C-008 is recorded only and C-011 is dropped, per the debate), so requirement coverage measures how many of them each card found.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|--------|--------|---------------|---------|-----------------|
| requirement_coverage | 0.30 | 0.89 (8/9: C-001..C-007, C-009) | 0.22 (2/9: C-003, C-010) | 0.56 (5/9: C-002..C-006) |
| internal_consistency | 0.25 | 0.90 (1 of 10 claims not confirmed: R1-F8) | 0.67 (1 of 3 claims contradicted: `actively_checked` dismissal of the FR-8 test, conceded in Round 2) | 0.71 (2 of 7: R3-F6 not confirmed; "K6 cannot refuse" conceded) |
| specificity_ratio | 0.15 | 0.89 (8/9 findings cite file:line; R1-F8 cites only "plan Constraints") | 1.00 (2/2) | 1.00 (6/6) |
| dependency_completeness | 0.15 | 1.00 (all cited lines exist) | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 (7 top-level keys) | 1.00 (7) | 1.00 (7) |
| **quant_score** | | **0.926** | **0.684** | **0.796** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV in short form: MET needs a cited card item; NOT MET cites the gap.

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| Reviews every in-scope plan task | NOT MET | missed Task 4 (C-010) | NOT MET | 2 tasks only | NOT MET | missed Task 4 and the C-001 pin pair |
| Edge cases / failure scenarios | MET | R1-F4 CHECK_FAIL path | MET | QA-002 post-replace failure | MET | R3-F4 |
| Dependencies / prerequisites | MET | R1-F5 archive-path dependency | NOT MET | none | MET | R3-F5 staging (src.md:174) |
| Success criteria (actionable fix per finding) | MET | every finding has a recommendation | MET | both | MET | all |
| Out of scope stated | MET | `checked_sound` A1-A3, orchestrator notes | MET | `actively_checked` | MET | clears T1 S2 |
| **Subtotal** | **4/5** | | **3/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| No factual errors | MET | R1-F8 is tagged INFERRED, not asserted (re-evaluated, see bias table) | NOT MET | dismissal of the T1 Q1 gap (conceded) | NOT MET | "K6 cannot refuse" (conceded) |
| Feasible fixes | MET | all | MET | both | MET | all |
| Consistent terminology | MET | | MET | | MET | |
| No internal contradictions | MET | | MET | | MET | |
| Claims supported by evidence | MET | spec_ref on every item | MET | quoted lines | MET | spec_ref on every item |
| **Subtotal** | **5/5** | | **4/5** | | **4/5** | |

### Structure (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|----|
| Logical ordering | MET | MET | MET |
| Consistent hierarchy | MET | MET | MET |
| Separation of concerns | NOT MET (R1-F9 bundles C-006 and C-007) | MET | MET |
| Navigation aids (ids, task refs) | MET | MET | MET |
| Card conventions (claim_tag, calibration block) | MET | MET | MET |
| **Subtotal** | **4/5** | **5/5** | **5/5** |

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|----|
| Unambiguous language | MET | MET | MET |
| Concrete | MET | MET | MET |
| One purpose per item | NOT MET (R1-F9) | MET | MET |
| Terms defined on first use (K6, FR-8, 427) | NOT MET | NOT MET | NOT MET |
| Actionable next steps | MET | MET | MET |
| **Subtotal** | **3/5** | **4/5** | **4/5** |

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|----|
| ≥3 risks with impact | MET (9) | NOT MET (2) | MET (6) |
| Mitigation per risk | MET | MET | MET |
| Failure modes and recovery | MET (R1-F4) | MET (QA-002) | MET (R3-F4) |
| External dependencies | MET (R1-F5) | NOT MET | MET (R3-F5) |
| Validation mechanism (tests named) | MET | MET | MET |
| **Subtotal** | **5/5** | **3/5** | **5/5** |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|----|
| Collection boundaries (empty, single) | NOT MET | NOT MET | NOT MET |
| State interactions across components | MET (check.log → verdict) | MET (state.json vs S) | MET (state.json → K6) |
| Guard-condition gaps | MET (R1-F7) | MET (QA-001) | MET (R3-F2) |
| Count divergence | MET (R1-F4 count equality) | NOT MET | MET (R3-F4) |
| Interaction effects | MET (R1-F1 two pins) | NOT MET | MET (R3-F1 removal × Usage line) |
| **Subtotal** | **4/5** | **2/5** | **4/5** |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 4/5 | 3/5 | 4/5 |
| Correctness | 5/5 | 4/5 | 4/5 |
| Structure | 4/5 | 5/5 | 5/5 |
| Clarity | 3/5 | 4/5 | 4/5 |
| Risk Coverage | 5/5 | 3/5 | 5/5 |
| Invariant & Edge Case | 4/5 | 2/5 | 4/5 |
| **qual_score** | **25/30 = 0.833** | **21/30 = 0.700** | **26/30 = 0.867** |

### Edge Case Floor Check

All three score at least 1/5 (V1 4, V2 2, V3 4): all eligible.

## Position-Bias Mitigation

Pass 1 in input order (V1, V2, V3); pass 2 in reverse (V3, V2, V1).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Correctness: no factual errors | V1 | MET | NOT MET | DISAGREE | MET (R1-F8 is tagged INFERRED, not asserted as fact) |
| Completeness: dependencies | V3 | MET | NOT MET | DISAGREE | MET (R3-F5 cites the src.md:174 prerequisite) |

Disagreements re-evaluated: 2
Final verdicts changed: 0

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (analyzer) | 0.463 | 0.417 | **0.880** | 8.0 points won |
| V2 (qa) | 0.342 | 0.350 | **0.692** | 1.5 points won |
| V3 (refactorer) | 0.398 | 0.434 | **0.832** | 10.0 points won |

**Margin**: V1 over V3 = 4.8% (below the 5% threshold)
**Tiebreaker applied**: Yes, level 1 (debate performance). Points won in the scoring matrix (split wins count 0.5): V3 10.0 vs V1 8.0, a 20% gap, so level 1 decides.

## Selected Base: Variant 3 (reviewer-3-card.yaml, refactorer, opus, calibrated C 0.81)

### Selection Rationale
V1 has the higher combined score because it found more clusters, but the top two are within 5%, so the debate decides. V3 won more points: the FR-8 data-model finding (C-005), the fuller staging scope (C-006), the T10 classification (C-008, X-005), the one-finding-per-cluster structure (S-003) and the C-005 contradiction (X-003). V3 also has the highest calibrated C (0.81) and no bundled items, which makes it the cleanest skeleton for one deduplicated list.

### Strengths to Preserve from Base
1. Flat schema with spec_ref and grounded evidence on every finding.
2. R3-F2 (C-005) as blocking, with the data-model framing, narrowed per Round 2.
3. R3-F5 (C-006) scope: docs/ and .dev/tasks.
4. `actively_checked` with line ranges.

### Strengths to Incorporate from Non-Base Variants
1. From V1: R1-F1 (C-001, blocking), R1-F9 part a (C-007), R1-F5 (C-009), R1-F6 and R1-F7 as corroboration of C-005 and C-003, R1-F2 severity for C-002, `checked_sound`.
2. From V2: QA-002 (C-010, minor, fix required), QA-001 as corroboration of C-003, the `category` field and quoted-line evidence.
3. From the debate: V1's owner-count evidence on C-010 (plan:101 vs plan:21); V2's src.md:140 support for C-005.
4. From the invariant probe: INV-005, INV-007, INV-008 and INV-011 notes on fixes; INV-001 and INV-003 as probe-raised blocking candidates.
