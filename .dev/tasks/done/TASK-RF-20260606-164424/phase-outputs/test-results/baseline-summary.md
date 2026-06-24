# Pytest Baseline Summary — `tests/cli/prd/`

**Captured:** 2026-06-07 03:14 (Step 1.4, pre-change zero-regression anchor)
**Command:** `uv run pytest tests/cli/prd/ -q`
**Branch:** `fix/prd-document-capture-hotfix` (cut from master `54d4b4f5`)
**Raw output:** `pytest-baseline.txt` (same directory)

## Summary line (verbatim)

```
============================= 106 passed in 0.46s ==============================
```

## Counts

| Result  | Count |
|---------|-------|
| passed  | 106   |
| failed  | 0     |
| skipped | 0     |
| error   | 0     |
| **collected** | **106** |

Pytest exit code: `0`

## Currently-failing test node IDs

None. The baseline is fully green — every one of the 106 collected tests passes.

## Per-file breakdown (verbatim from output)

```
tests/cli/prd/test_cli_smoke.py ......                                   [  5%]
tests/cli/prd/test_config.py .                                           [  6%]
tests/cli/prd/test_e2e.py .....                                          [ 11%]
tests/cli/prd/test_executor.py .....                                     [ 16%]
tests/cli/prd/test_filtering.py ..........                               [ 25%]
tests/cli/prd/test_gates.py ....................                         [ 44%]
tests/cli/prd/test_integration.py .........                              [ 52%]
tests/cli/prd/test_inventory.py .......                                  [ 59%]
tests/cli/prd/test_models.py ......                                      [ 65%]
tests/cli/prd/test_path_resolution.py ........                           [ 72%]
tests/cli/prd/test_prompt_builders_dual_mode.py ..........               [ 82%]
tests/cli/prd/test_prompts.py ....                                       [ 85%]
tests/cli/prd/test_research_notes_roundtrip.py ..                        [ 87%]
tests/cli/prd/test_resolve_step_content.py ......                        [ 93%]
tests/cli/prd/test_resume_skip.py .......                                [100%]
```

## Zero-regression contract

Phase 6, Step 6.1 must demonstrate: post-change run has **0 NEW failing node IDs** versus this baseline (baseline failing set is empty, so post-change must also be 0 failures among these 106 pre-existing tests) **AND** all 10 newly-authored AC tests (AC1–AC10) present and passing. Expected post-change green total: 106 + (number of new AC test functions).
