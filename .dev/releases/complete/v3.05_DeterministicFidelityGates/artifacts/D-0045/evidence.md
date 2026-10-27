# D-0045: SC-4, SC-6, NFR-4, NFR-7 End-to-End Evidence

## SC-4: >=70% Structural Findings Ratio

### Tests Passed
- `test_sc4_ratio` — verifies structural findings >= 70% of total
- `test_all_structural_findings_tagged` — all structural findings have source_layer="structural"
- `test_structural_vs_semantic_dimensions_disjoint` — dimensions are non-overlapping
- `test_finding_counts_by_source_layer` — count breakdown by source layer

### Implementation
- 5 structural dimensions: signatures, data_models, gates, cli, nfrs
- 4 semantic dimensions: prose_sufficiency, contradiction_detection, completeness_coverage, architectural_alignment
- Structural checkers produce deterministic findings without LLM calls

## SC-6: No Semantic Prompt Exceeds 30,720 Bytes

### Tests Passed
- `test_truncate_within_budget` — prompts within budget pass through
- `test_truncate_oversized` — oversized content truncated to budget
- `test_truncate_on_line_boundary` — truncation happens on line boundaries
- `test_truncation_marker_includes_heading` — truncation marker visible in output
- `test_truncation_priority_prior_first` — prior summary truncated first, then structural context

### Implementation
- `MAX_PROMPT_BYTES = 30_720` in semantic_layer.py
- Budget allocation: spec+roadmap 60%, structural context 20%, prior summary 15%, template 5%
- `_truncate_to_budget()` enforces byte limit before every LLM call

## NFR-4: Checkers Share No Mutable State

### Tests Passed
- `test_no_shared_mutable_state` — each checker has independent Finding counter
- `test_parallel_execution_determinism` — parallel execution matches sequential
- `test_parallel_execution_both_sides` — debate runs both sides in parallel safely

## NFR-7: Steps 1-7 Unchanged

### Tests Passed
- `test_full_pipeline_sc1_through_sc6` — complete pipeline flow verified
- Steps 1-7 use identical step definitions regardless of `convergence_enabled`
- Only step 8 (spec-fidelity) gate changes: `None` when convergence enabled

## Combined Test Results
```
27 tests passed covering SC-4, SC-6, NFR-4, NFR-7
```
