# Phase 9.2 -- 4-Way Pipeline Completion Comparison

Generated: 2026-04-03
Source: .roadmap-state.json from all 4 result directories

## Pipeline Step Status Comparison

| Step | TDD-only (prior) | TDD+PRD (new) | Spec-only (prior) | Spec+PRD (new) |
|------|-------------------|----------------|---------------------|-----------------|
| **extract** | PASS (att 1) | PASS (att 1) | PASS (att 1) | PASS (att 1) |
| **generate-opus-architect** | PASS (att 1) | PASS (att 1) | PASS (att 1) | PASS (att 1) |
| **generate-haiku-architect** | PASS (att 1) | PASS (att 2) | PASS (att 1) | PASS (att 1) |
| **diff** | PASS (att 1) | PASS (att 1) | PASS (att 1) | PASS (att 1) |
| **debate** | PASS (att 1) | PASS (att 1) | PASS (att 1) | PASS (att 1) |
| **score** | PASS (att 1) | PASS (att 1) | PASS (att 1) | PASS (att 1) |
| **merge** | PASS (att 1) | PASS (att 1) | PASS (att 1) | PASS (att 1) |
| **anti-instinct** | FAIL (att 1) | FAIL (att 1) | FAIL (att 1) | FAIL (att 1) |
| **wiring-verification** | PASS (att 1) | PASS (att 1) | PASS (att 1) | PASS (att 1) |
| **spec-fidelity** | NOT PRESENT | NOT PRESENT | NOT PRESENT | NOT PRESENT |

## Extraction Gate Analysis

### TDD Pipeline: EXTRACT_TDD_GATE (19 fields)

The TDD+PRD run uses the `requirements-design-extraction-agent` generator (vs `requirements-extraction-agent` in TDD-only). Both produce 19 frontmatter fields in the extraction output:

| Frontmatter Field | TDD-only | TDD+PRD | Delta |
|--------------------|----------|---------|-------|
| functional_requirements | 5 | 5 | 0 |
| nonfunctional_requirements | 4 | 9 | +5 |
| total_requirements | 9 | 14 | +5 |
| complexity_score | 0.65 | 0.55 | -0.10 |
| risks_identified | 3 | 7 | +4 |
| dependencies_identified | 6 | 8 | +2 |
| success_criteria_count | 7 | 10 | +3 |
| data_models_identified | 2 | 2 | 0 |
| api_surfaces_identified | 4 | 4 | 0 |
| components_identified | 4 | 9 | +5 |
| test_artifacts_identified | 6 | 6 | 0 |
| migration_items_identified | 3 | 15 | +12 |
| operational_items_identified | 2 | 9 | +7 |

PRD enrichment significantly increased extraction yield: +5 NFRs, +4 risks, +5 components, +12 migration items, +7 operational items. The PRD adds product-level context that surfaces additional non-functional, migration, and operational concerns.

### Spec Pipeline: EXTRACT_GATE (13 fields)

Both spec runs produce 13 frontmatter fields:

| Frontmatter Field | Spec-only | Spec+PRD | Delta |
|--------------------|-----------|----------|-------|
| functional_requirements | 5 | 5 | 0 |
| nonfunctional_requirements | 3 | 7 | +4 |
| total_requirements | 8 | 12 | +4 |
| complexity_score | 0.62 | 0.60 | -0.02 |
| risks_identified | 3 | 7 | +4 |
| dependencies_identified | 7 | 9 | +2 |
| success_criteria_count | 8 | 6 | -2 |

PRD enrichment increased NFRs and risks similarly to the TDD pipeline but slightly reduced success_criteria_count.

## Step-by-Step Differences

### 1. Extract Step
- All 4 runs PASS on first attempt.
- TDD+PRD extraction took ~327s (vs ~159s for TDD-only) -- roughly 2x longer, likely due to processing additional PRD input.
- Spec+PRD extraction took ~94s (vs ~121s for Spec-only) -- slightly faster.

### 2. Generate Steps (opus + haiku)
- TDD+PRD haiku-architect required 2 attempts (vs 1 for all other runs). This is the only retry across all 4 runs.
- Spec+PRD opus-architect took ~8 minutes (vs ~2 minutes for Spec-only opus-architect) -- significantly longer with PRD enrichment.

### 3. Diff, Debate, Score Steps
- All 4 runs PASS on first attempt with comparable durations.

### 4. Merge Step
- All 4 runs PASS on first attempt. TDD+PRD merge took ~6.5 minutes, comparable to TDD-only (~4 minutes). Spec+PRD merge took ~6 minutes vs ~3.5 minutes for Spec-only.

### 5. Anti-Instinct Step
- All 4 runs FAIL. This step executes in <1 second in all cases (pure analysis, no generation).

### 6. Wiring Verification
- All 4 runs PASS. Executes in <1 second.

### 7. Spec-Fidelity
- NOT PRESENT in any of the 4 roadmap state files. The pipeline halted after anti-instinct FAIL in all cases, and spec-fidelity was not recorded as a step.

## State File Structural Differences

| Field | TDD-only | TDD+PRD | Spec-only | Spec+PRD |
|-------|----------|---------|-----------|----------|
| prd_file | absent | present | absent | present |
| tdd_file | absent | null | absent | null |
| input_type | absent | "tdd" | absent | "spec" |
| schema_version | 1 | 1 | 1 | 1 |
| spec_hash | 43c9e660... | 43c9e660... | 2db9d8c5... | 2db9d8c5... |

The PRD-enriched runs include `prd_file`, `tdd_file`, and `input_type` fields in the state file, confirming the new multi-input pipeline schema is active.

## Total Pipeline Duration

| Run | Start | End | Duration |
|-----|-------|-----|----------|
| TDD-only | 15:15:14 | 15:28:57 | ~13.7 min |
| TDD+PRD | 02:33:31 | 02:58:32 | ~25.0 min |
| Spec-only | 15:39:59 | 15:53:49 | ~13.8 min |
| Spec+PRD | 03:07:23 | 03:28:14 | ~20.8 min |

PRD enrichment increased total pipeline duration by ~82% for TDD and ~51% for Spec pipelines.
