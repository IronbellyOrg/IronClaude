# Base Selection Report

## Quantitative Scoring (50% weight)

The cards have no FR-style requirement IDs. Requirement coverage therefore uses the edge-case rule: the "requirements" are the 15 distinct real defects that either reviewer found and that the debate kept. Those are the merged findings M-01 to M-06 and M-08 to M-16; M-07 (found by a calibrator), M-17 (not a defect) and M-18/M-19 (found by the probe) are excluded. A finding counts as covering a defect only if it identifies it as a defect (P2R2-7's "benign" plan:48 does not count).

| Metric | Weight | Variant A (sonnet:analyzer) | Variant B (haiku/glm-5.3:qa) |
|--------|--------|-------------------|-------------------|
| requirement_coverage | 0.30 | 0.867 (13/15: M-01..M-06, M-08..M-14) | 0.400 (6/15: M-02, M-03, M-04, M-06, M-15, M-16) |
| internal_consistency | 0.25 | 0.909 (1 contradiction in 11 claims: same origin given two classes, R1-02 vs R1-05/09) | 0.857 (1 in 7: P2R2-7 calls the t14/t16 files benign while P2R2-4 says their paths are wrong) |
| specificity_ratio | 0.15 | 0.909 (10/11; vague: "likely" in R1-08) | 0.857 (6/7; vague: P2R2-6's three-way "or" fix) |
| dependency_completeness | 0.15 | 0.975 (1 broken of about 40 line references: plan:84 in R1-07) | 0.920 (2 broken of about 25: source.md:465 in P2R2-4, the U25 label in P2R2-5) |
| section_coverage | 0.15 | 1.000 (8/8 top-level fields incl. self_audit) | 0.875 (7/8, no self_audit) |
| **quant_score** | | **0.920** | **0.732** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Claim-Evidence-Verdict (CEV): a criterion is MET only when specific evidence can be cited.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Covers all explicit requirements | MET | self_audit: "Checked T0-T12 mapping and order, U1-U25 assignment" | MET | P2R2-6: "reviewer verified each span is carried by a plan task" |
| Addresses edge cases/failures | MET | R1-01 success-case exit; R1-09 "Disconnected" | MET | P2R2-1 workspace with a local-scope entry; P2R2-2 `set -u` abort |
| Includes dependencies/prerequisites | MET | R1-05 U11 needs Task 5; R1-06 Ready line needs Task 7 | NOT MET | no task-ordering finding; searched P2R2-1..7 |
| Defines success/completion criteria | MET | each fix states the passing command (R1-01, R1-09) | MET | P2R2-3 "closing equality test" |
| Specifies out-of-scope items | MET | self_audit UNVERIFIED: directory-level pytest vs baseline | NOT MET | no scope or UNVERIFIED statement |
| **Subtotal** | **5/5** | | **3/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| No factual errors | NOT MET | plan:84 wrongly cited (calibrator) | NOT MET | plan:48 "benign" (wrong); U25 mislabel; source.md:465 |
| Feasible fixes | NOT MET | `$ART` unbound under `-u`; `test -z "$(…)"` vacuous (Round 2) | NOT MET | P2R2-1 fix writes to the t16 file source.md:706 forbids |
| Terminology consistent | NOT MET | drift vs necessary for the same origin | MET | drift used uniformly for every plan finding |
| No internal contradictions | NOT MET | see IC | NOT MET | see IC |
| Claims supported by evidence | MET | every finding cites plan and spec lines | MET | every finding cites plan or artifact lines |
| **Subtotal** | **1/5** | | **2/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Logical ordering | NOT MET | importance mixed (important, important, minor, important, ...) | MET | the one important finding first, minors after |
| Consistent hierarchy | MET | uniform finding schema | MET | uniform finding schema |
| Separation of concerns | NOT MET | R1-04 bundles three defects | MET | one defect per finding |
| Navigation aids | MET | ids plus plan_ref/spec_ref on every finding | MET | same |
| Artifact-type conventions | MET | reviewer-card fields plus self_audit | MET | reviewer-card fields present |
| **Subtotal** | **3/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Unambiguous language | NOT MET | R1-08 "likely fails" | MET | no hedged claim |
| Concrete | MET | exact commands in fixes | MET | exact commands in fixes |
| Each finding summarizable | MET | one-sentence claims | MET | one-sentence claims |
| Terms defined on first use | NOT MET | D-1, D-2, X-11 unglossed | NOT MET | INF-037, INF-056 unglossed |
| Actionable next steps | MET | every finding has a fix | MET | every defect finding has a fix |
| **Subtotal** | **3/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| ≥3 risks with probability and impact | NOT MET | severity only, no probability | NOT MET | severity only, no probability |
| Mitigation per risk | MET | fix per finding | MET | fix per defect finding |
| Failure modes and recovery | MET | R1-02 block abort; R1-07 silent pass | MET | P2R2-1 block abort; P2R2-2 unbound abort |
| External dependency failures | MET | R1-08 uv/yaml; R1-11 `claude mcp get` in sandbox | NOT MET | none |
| Monitoring/validation mechanism | MET | R1-09 negative check; R1-04 equality test | MET | P2R2-3 closing equality test |
| **Subtotal** | **4/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Collection boundaries | MET | R1-01 empty `rg` input on a clean commit | NOT MET | none |
| State variables across boundaries | MET | R1-03 `$E` across the task boundary; R1-04 working directory | MET | P2R2-2 `$E` under `set -u` |
| Guard condition gaps | MET | R1-07, R1-09 | MET | P2R2-1 |
| Count divergence / range bounds | MET | R1-05 U1-U11 range boundary misassigns U11 | NOT MET | none |
| Interaction effects | MET | R1-06 Task 6 / Task 7 interaction | NOT MET | none |
| **Subtotal** | **5/5** | | **2/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 3/5 |
| Correctness | 1/5 | 2/5 |
| Structure | 3/5 | 5/5 |
| Clarity | 3/5 | 4/5 |
| Risk Coverage | 4/5 | 3/5 |
| Invariant & Edge Case | 5/5 | 2/5 |
| **qual_score** | **21/30 = 0.700** | **19/30 = 0.633** |

### Edge Case Floor Check
- Variant A: 5/5, eligible.
- Variant B: 2/5, eligible.

## Position-Bias Mitigation

Pass 1 ran in input order (A, B). Pass 2 ran in reverse order (B, A), with the same rubric applied independently.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness: covers all explicit requirements | B | MET | NOT MET | DISAGREE | MET (re-evaluated: P2R2-6 records a span-by-span check of the spec, which is evidence of checking coverage even though it is overstated) |
| All other 59 criterion-variant pairs | A, B | as above | same | AGREE | as above |

- Disagreements re-evaluated: 1
- Final verdicts changed: 0

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (sonnet:analyzer) | 0.460 | 0.350 | **0.810** | 7 points won (not needed) |
| B (haiku/glm-5.3:qa) | 0.366 | 0.317 | **0.683** | 6 points won |

**Margin**: 12.7 points (above the 5% threshold)
**Tiebreaker applied**: No

## Selected Base: Variant A (reviewer 1, sonnet:analyzer)

### Selection Rationale
- A wins on requirement coverage: 13 of 15 kept defects, against 6.
- A wins every invariant criterion.
- A wins the high-impact debate points X-001, X-003, X-004 and C-001.
- B wins structure and classification (S-002, C-002, C-004, X-002). These are merge-able improvements, not reasons to change the base.
- The calibrators agree: C 0.80 for A against 0.74 for B.

### Strengths to Preserve from Base
1. Defect content of R1-01, R1-02, R1-05, R1-07, R1-09, R1-10 and the Task 14 copy gap.
2. Spec-line citations on every finding.
3. Self-audit with its UNVERIFIED item.

### Strengths to Incorporate from Non-Base Variants
1. From Variant B: one defect per finding. Split R1-04 into path, Task 3 hash and Task 14 copy (S-002; P2R2-3, P2R2-4).
2. From Variant B: literal package paths instead of `$ART` (C-004, P2R2-4 fix).
3. From Variant B: `$E` classified as drift and the `set -u` mechanism named (X-002, P2R2-2).
4. From Variant B: the T1 coverage-matrix findings (C-003; P2R2-5 with the U23 correction, P2R2-6 at minor).
5. From Variant B: a record of authorized expansions (S-003; P2R2-7's Task 2 "commit only if changed" and plan:48's intent).
6. From the debate and the probe:
   - the classification rule (A-002 rejected by both advocates);
   - the plan:48 file-first or if-form fix;
   - the t16 conflict (A-003);
   - INV-001 to INV-018 corrections, including the new findings for plan:134-135 (INV-006) and the vacuous checks (INV-011, INV-017).
