# Phase 6 TDD Wire Verification

**Date:** 2026-03-27

All 9 prompt builders accept both `tdd_file` and `prd_file` kwargs:

| Builder | Result | Output Size |
|---------|--------|-------------|
| `build_extract_prompt` | OK | 4038 chars |
| `build_generate_prompt` | OK | 3638 chars |
| `build_extract_prompt_tdd` | OK | 7223 chars |
| `build_score_prompt` | OK | 1665 chars |
| `build_spec_fidelity_prompt` | OK | 5804 chars |
| `build_test_strategy_prompt` | OK | 3078 chars |
| `build_diff_prompt` | OK | 1096 chars |
| `build_debate_prompt` | OK | 1289 chars |
| `build_merge_prompt` | OK | 1379 chars |

ALL PASS. Both `tdd_file` and `prd_file` kwargs accepted without errors.
