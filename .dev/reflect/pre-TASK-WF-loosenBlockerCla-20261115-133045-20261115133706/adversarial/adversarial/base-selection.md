# Base Selection Report

Scorer: the orchestrator (neutral judge). Variant A = Variant 1 (reviewer-1 card, haiku-class, analyzer). Variant B = Variant 2 (reviewer-2 card, opus-class, qa). The two advocates ran as opus (for A) and haiku (for B).

## Quantitative Scoring (50% weight)

Source requirement set for RC: the 13 content topics C-001 to C-013 of diff-analysis.md, all of which were confirmed as real plan defects or real wording slips by the end of Round 2 (no formal requirement IDs exist, so section-level topic matching per the scoring protocol). A topic counts for a variant when it appears as a finding or as the same claim.

| Metric | Weight | Variant A (haiku) | Variant B (opus) |
|--------|--------|-------------------|------------------|
| requirement_coverage | 0.30 | 0.385 (5 of 13: C-001, C-002, C-003, C-004, C-005) | 0.692 (9 of 13: C-001, C-006, C-007, C-008, C-009, C-010, C-011, C-012, C-013) |
| internal_consistency | 0.25 | 0.818 (1 - 2/11 claims contradicted by debate evidence: Checked bullets 3 and 4, X-002 and X-001) | 0.882 (1 - 2/17 claims contradicted by verified facts: F3 "7 pairs" and F3 M12 consequence, spec:974 and Grep of 8 pairs) |
| specificity_ratio | 0.15 | 0.818 (9 of 11 statements concrete; Checked bullets 1 and 5 are generic) | 1.000 (17 of 17) |
| dependency_completeness | 0.15 | 1.000 (every plan:N and spec:N reference resolves; A-002 verified) | 1.000 (every reference resolves, including 09-plan-input.md:15 and hooks.json:173) |
| section_coverage | 0.15 | 1.000 (4 H2 sections) | 1.000 (4 H2 sections) |
| **quant_score** | | **0.743** | **0.878** |

Arithmetic. A: 0.30x0.385 + 0.25x0.818 + 0.15x0.818 + 0.15 + 0.15 = 0.1155 + 0.2045 + 0.1227 + 0.30 = 0.743. B: 0.30x0.692 + 0.25x0.882 + 0.15x1.000 + 0.30 = 0.2076 + 0.2205 + 0.15 + 0.30 = 0.878.

## Qualitative Scoring (50% weight) - Additive Binary Rubric (final verdicts after position-bias mitigation)

Applied to the cards as review documents. Evidence is given in the CEV form (claim, evidence, verdict) in compressed table form; MET requires a cited line.

### Completeness (5 criteria)

| Criterion | A | Evidence | B | Evidence |
|-----------|---|----------|---|----------|
| Covers all explicit requirements | NOT MET | misses 8 verified defects (C-006 to C-013) | NOT MET | misses 4 verified defects (C-002 to C-005) | 
| Addresses edge cases/failures | MET | F2 "plan:419 expressly allows the pointer plus the ledger sentence" | MET | F7 line pins that the task's own edit moves |
| Includes dependencies/prerequisites | MET | F3 "Task 11 creates no such row" | MET | F2 "Task 30 updates a task-skill row that Task 11 never creates" |
| Defines success/completion criteria | MET | Verdict line names the four defect classes | MET | Verdict line names the defect classes |
| Specifies out-of-scope items | NOT MET | none stated | NOT MET | none stated |
| **Subtotal** | **3/5** | criteria 2, 3, 4 | **3/5** | criteria 2, 3, 4 |

### Correctness (5 criteria)

| Criterion | A | Evidence | B | Evidence |
|-----------|---|----------|---|----------|
| No factual errors or hallucinated claims | MET | every citation in F1-F6 re-read and true (A-002) | NOT MET | F3 says 7 pairs (Grep: 8 at rf-qa-qualitative.md:240, 291, 362, 429, 500, 567, 746, 784) and ties it to M12, which spec:974 defines on rf-qa only |
| Technical approaches feasible | MET | fixes implied are feasible | MET | same |
| Terminology consistent | MET | | MET | |
| No internal contradictions | MET | F5 and Checked bullet 2 agree | MET | |
| Claims supported by evidence | MET | each finding has file:line and quote | MET | each finding has file:line and quote |
| **Subtotal** | **5/5** | | **4/5** | |

### Structure (5 criteria)

| Criterion | A | B |
|-----------|---|---|
| Logical ordering | MET (Verdict, Findings, Checked, Self-report) | MET |
| Consistent hierarchy | MET | MET |
| Separation of concerns | MET | MET |
| Navigation aids | MET (legend at top defines plan, spec, plan-input) | MET (path note at the bottom, line 42) |
| Follows conventions of the artifact type | MET (F<n> block shape) | MET (uses blocking false for two findings, as the shape allows) |
| **Subtotal** | **5/5** | **5/5** |

### Clarity (5 criteria)

| Criterion | A | Evidence | B | Evidence |
|-----------|---|----------|---|----------|
| Unambiguous language | MET | each claim names "The executor ..." and the wrong result | MET | same |
| Concrete rather than abstract | MET | | MET | |
| Each section has a clear purpose | MET | | MET | |
| Acronyms and terms defined on first use | NOT MET (after Pass 2) | uses "digest", "owner go", "offline scaffold", "T2 reverse scan" with no definition | NOT MET | uses M12, OD4, T1, M, C, E, REQ-06 with no definition |
| Actionable next steps | NOT MET | no finding says what to change | MET | F8 "goes red at Task 26 unless it checks the registry row for `legacy`" |
| **Subtotal** | **3/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | A | B |
|-----------|---|---|
| Identifies at least 3 risks with probability and impact | NOT MET (impact only; no probability) | NOT MET (impact only) |
| Mitigation for each risk | NOT MET | NOT MET |
| Failure modes and recovery | NOT MET (failure modes, no recovery) | NOT MET |
| External dependencies and their failure scenarios | NOT MET (plan and spec only) | MET (hooks/hooks.json absent at root; code files hold the phrases) |
| Monitoring or validation mechanism | NOT MET ("Static review only; no commands") | MET (Checked lists the Greps run) |
| **Subtotal** | **0/5** | **2/5** |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | A | B |
|-----------|---|---|
| Collection boundaries (scan sets, enumerations) | MET (F1 canonical source inside the scan set) | MET (F1 scan set includes code files) |
| State variable interactions across components | MET (F2, F3 registry state vs file state) | MET (F2 same) |
| Guard condition gaps | MET (F5 owner gate) | MET (F4 input guard) |
| Count divergence | NOT MET | MET (F3 pair count, F9 "exactly the 11 carriers" vs 18 rows) |
| Interaction effects | MET (F4 built-but-not-wired sweep) | MET (F7 edit shifts its own pins) |
| **Subtotal** | **4/5** | **5/5** |

**Edge case floor check**: A 4/5 and B 5/5, both at or above the 1/5 floor; both eligible.

### Qualitative Summary

| Dimension | A | B |
|-----------|---|---|
| Completeness | 3/5 | 3/5 |
| Correctness | 5/5 | 4/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 3/5 | 4/5 |
| Risk Coverage | 0/5 | 2/5 |
| Invariant & Edge Case | 4/5 | 5/5 |
| **qual_score** | **20/30 = 0.667** | **23/30 = 0.767** |

## Position-Bias Mitigation

Pass 1 evaluated A then B; Pass 2 evaluated B then A, each from a fresh reading of the two cards and the debate evidence. Only criteria where the passes differed are listed.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness 1 (all explicit requirements) | B | NOT MET | MET (broadest set of verified defects) | DISAGREE | NOT MET (re-evaluation: B misses C-002 to C-005, four verified defects) |
| Correctness 1 (no factual errors) | A | MET | NOT MET (Checked bullet 4 "sound") | DISAGREE | MET (re-evaluation: plan:299 literally says "before Task 26", so the sentence is true; the debate showed it incomplete, not false) |
| Clarity 4 (terms defined) | A | MET | NOT MET (no definitions of digest, T2, owner go) | DISAGREE | NOT MET (re-evaluation: the legend defines only paths) |

Disagreements re-evaluated: 3. Final verdicts changed: 1 (A on Clarity 4, from MET to NOT MET).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (haiku:analyzer) | 0.372 | 0.333 | **0.705** | not needed |
| B (opus:qa) | 0.439 | 0.383 | **0.822** | not needed |

**Margin**: 11.7 percentage points (above the 5% threshold)
**Tiebreaker applied**: No

For information only: debate performance (points on which the advocates give the variant as winner in the scoring matrix, excluding "both", "neither" and QUALIFY rows): A wins C-002, C-003, C-004, C-005; B wins S-002, S-003, S-004, S-005, C-006, C-007, C-009, C-010, C-011, C-012, C-013, X-001, X-002.

## Selected Base: Variant 2 (opus:qa, reviewer-2 card)

### Selection Rationale
Variant 2 leads on both layers: broader coverage of the verified defects (9 of 13 against 5 of 13), every Checked bullet tied to a file or Grep, and live-repository evidence that Variant 1 never reached (five code-file hits, root hooks path, eight FAIL bullets). Its weaknesses are factual and local: the F3 count and M12 consequence, and over-grading F4 and F6 in full.

### Strengths to Preserve from Base
1. Calibrated severity shape (two non-blocking findings) and repository-grounded citations.
2. F1, F3, F5 and the missing-path limb of F7 with their evidence.
3. The Checked section with the verified facts.

### Strengths to Incorporate from Non-Base Variants
1. From Variant 1: F1 (canonical rule.md versus the T2 reverse scan), F4 (sweep not wired into the task skill), F5 (no owner go between stage 0 and stage 1), F6 (no fresh-findings evaluation), and F2/F3 as the clearer statement of the registry mechanism.
2. From the fault-finder (origin: fault-finder, carried only with verified citations): INV-001, INV-002, INV-003 (non-blocking), INV-008 (non-blocking).
EOF
echo ok