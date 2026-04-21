# TDD Comparison: Adversarial Artifacts (Test 1 vs Test 3)

**Generated**: 2026-04-02
**Purpose**: Compare adversarial pipeline artifacts (diff-analysis, debate-transcript, base-selection) between TDD and spec runs

---

## 1. diff-analysis.md Comparison

### Frontmatter

| Field | Test 1 (TDD) | Test 3 (Spec) |
|---|---|---|
| total_diff_points | 12 | 14 |
| shared_assumptions_count | 14 | 12 |

Both have exactly 2 frontmatter fields with the same field names. Values differ as expected due to different input content.

### Structural Comparison

| Section | Test 1 (TDD) | Test 3 (Spec) |
|---|---|---|
| Section 1: Shared Assumptions | 14 items | 12 items |
| Section 2: Divergence Points | D-01 through D-12 (12 points) | D-1 through D-14 (14 points) |
| Section 3: Areas Where One Variant Is Stronger | Opus strengths + Haiku strengths | Opus strengths + Haiku strengths |
| Section 4: Areas Requiring Debate | 6 items | 5 items |

Both follow the same 4-section structure. Content differs because TDD vs spec source documents produce different roadmap variants with different divergence points.

---

## 2. debate-transcript.md Comparison

### Frontmatter

| Field | Test 1 (TDD) | Test 3 (Spec) |
|---|---|---|
| convergence_score | 0.72 | 0.62 |
| rounds_completed | 2 | 2 |

Both have exactly 2 frontmatter fields with the same field names.

### Structural Comparison

| Section | Test 1 (TDD) | Test 3 (Spec) |
|---|---|---|
| Round 1: Initial Positions | Present (6 debate topics) | Present (8 debate topics) |
| Round 2: Rebuttals | Present (Variant A rebuts, Variant B rebuts) | Present (Variant A rebuts, Variant B rebuts) |
| Convergence Assessment | Present (6 agreement areas, 5 remaining disputes) | Present (4 agreement areas, 4 disagreement areas, merge strategy) |

Both follow the same 3-part structure (Round 1, Round 2, Convergence Assessment). Test 1 achieves higher convergence (0.72 vs 0.62), suggesting the TDD roadmap variants had more common ground due to richer shared extraction content.

---

## 3. base-selection.md Comparison

### Frontmatter

| Field | Test 1 (TDD) | Test 3 (Spec) |
|---|---|---|
| base_variant | B | roadmap-opus-architect |
| variant_scores | A:71 B:78 | A:79 B:71 |

Both have exactly 2 frontmatter fields with the same field names. Different base selections are expected -- the adversarial pipeline evaluates different roadmap content and may select different winners.

### Structural Comparison

| Section | Test 1 (TDD) | Test 3 (Spec) |
|---|---|---|
| Scoring Criteria table | Present (6 criteria) | Present (10 criteria) |
| Per-Criterion Scores | Present (C1-C6 with per-variant justification) | Present (C1-C10 with per-variant justification) |
| Overall Scores table | Present (6-row weighted table) | Present (10-row weighted table) |
| Base Variant Selection Rationale | Present (3 reasons for Variant B) | Present (5 reasons for Variant A) |
| Specific Improvements to Incorporate | Present (6 ordered items) | Present (10+ items in Must/Should/Should-NOT tiers) |

Both follow the same structural pattern: criteria definition, per-criterion scoring with justification, aggregate score table, selection rationale, improvement list. The number of criteria differs (6 vs 10), which is expected LLM non-determinism in evaluation framework granularity.

---

## Side-by-Side Metrics Summary

| Metric | Test 1 (TDD) | Test 3 (Spec) | Format Match? |
|---|---|---|---|
| diff-analysis FM fields | 2 | 2 | YES |
| diff-analysis sections | 4 | 4 | YES |
| diff total_diff_points | 12 | 14 | n/a (value) |
| diff shared_assumptions | 14 | 12 | n/a (value) |
| debate FM fields | 2 | 2 | YES |
| debate sections | 3 | 3 | YES |
| debate convergence_score | 0.72 | 0.62 | n/a (value) |
| debate rounds_completed | 2 | 2 | YES |
| base-selection FM fields | 2 | 2 | YES |
| base-selection sections | 5 | 5 | YES |
| base-selection base_variant | B (Haiku) | A (Opus) | n/a (value) |
| base-selection variant A score | 71 | 79 | n/a (value) |
| base-selection variant B score | 78 | 71 | n/a (value) |

---

## Verdict: **STRUCTURAL_FORMAT_MATCH_CONFIRMED**

All three adversarial artifacts (diff-analysis.md, debate-transcript.md, base-selection.md) share the same structural format between Test 1 and Test 3:
- Same frontmatter field names and counts
- Same section hierarchy (4/3/5 sections respectively)
- Same analytical framework (divergence points, debate rounds, scoring criteria)

Values differ as expected due to different input content. The adversarial pipeline produces structurally consistent outputs regardless of TDD vs spec input.
