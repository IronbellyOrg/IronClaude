# Regression Diff — Baseline vs Post-Change (`tests/cli/prd/`)

**Compared:** 2026-06-07 03:46 (Step 6.1)
**Baseline:** `baseline-summary.md` / `pytest-baseline.txt` (pre-change, master `54d4b4f5`)
**Post-change:** `pytest-post.txt` (branch `fix/prd-document-capture-hotfix`)
**Command (both):** `uv run pytest tests/cli/prd/ -q`

## Summary-line comparison

| Run        | Summary line (verbatim)                          |
|------------|--------------------------------------------------|
| Baseline   | `============================= 106 passed in 0.46s ==============================` |
| Post-change| `============================= 122 passed in 0.50s ==============================` |

## Counts

| Result  | Baseline | Post-change | Δ   |
|---------|----------|-------------|-----|
| passed  | 106      | 122         | +16 |
| failed  | 0        | 0           | 0   |
| skipped | 0        | 0           | 0   |
| error   | 0        | 0           | 0   |
| collected | 106    | 122         | +16 |

Pytest exit code: baseline `0`, post-change `0`.

## NEW failing node IDs (failing now but not in baseline)

**NONE.** Baseline failing set was empty; post-change failing set is empty. **0 NEW failures — zero regression.**

## Per-file delta (the +16 are all newly-authored AC tests)

| File | Baseline | Post | Δ | New tests |
|------|----------|------|---|-----------|
| test_e2e.py | 5 | 7 | +2 | AC10a (recovery), AC10b (no-contamination) |
| test_executor.py | 5 | 7 | +2 | AC7 (INV-010 NDJSON channel), AC8 (`_persist_step_artifact` canonical write) |
| test_gates.py | 20 | 23 | +3 | AC9 `TestCheckNoTruncationMarker` (3 methods) |
| test_prompts.py | 4 | 9 | +5 | AC1 (4 parametrized builder pins) + AC2 (mapping sync) |
| test_resolve_step_content.py | 6 | 10 | +4 | AC3 (variant recovery), AC4 (freshness INV-006), AC5 (containment INV-005), AC6 (zero-match fallback) |
| (other 10 files) | 66 | 66 | 0 | unchanged |
| **Total** | **106** | **122** | **+16** | |

## All 10 acceptance tests present and PASSING

| AC | Test | File | Status |
|----|------|------|--------|
| AC1 | `TestDocumentBuilderOutputPins::test_builder_pins_canonical_output_path` (×4 params) | test_prompts.py | PASS |
| AC2 | `test_prompt_executor_mapping_sync` | test_prompts.py | PASS |
| AC3 | `test_variant_filename_recovered_from_where_subdir` | test_resolve_step_content.py | PASS |
| AC4 | `test_freshness_outranks_size_inv006` | test_resolve_step_content.py | PASS |
| AC5 | `test_where_traversal_escape_excluded_inv005` | test_resolve_step_content.py | PASS |
| AC6 | `test_zero_match_returns_ndjson_fallback` | test_resolve_step_content.py | PASS |
| AC7 | `test_determine_status_reads_ndjson_channel_inv010` | test_executor.py | PASS |
| AC8 | `test_persist_step_artifact_writes_canonical_name` | test_executor.py | PASS |
| AC9 | `TestCheckNoTruncationMarker` (×3 methods) | test_gates.py | PASS |
| AC10 | `test_e2e_ac10_recovery_variant_filename`, `test_e2e_ac10_no_where_contamination_when_pinned` | test_e2e.py | PASS |

## Verdict

**PASS.** 0 NEW failures versus baseline AND all 10 AC tests present and passing. Numbers copied verbatim from `pytest-baseline.txt` and `pytest-post.txt`; no fabrication.
