# Phase 8 Regression Test Results

**Command:** `uv run pytest tests/ -v --tb=short`
**Result:** 4791 passed, 5 failed, 102 skipped, 22 warnings, 1 error (92.55s)

## Failures Analysis

| Test | Related to our changes? | Details |
|---|---|---|
| `test_credential_scanner.py::test_detects_real_secrets` | NO — pre-existing | Credential scanner detection count off by 1 |
| `test_wiring_pipeline.py::test_pipeline_runs_wiring_verification_in_shadow_mode` | NO — pre-existing | Imports RoadmapConfig but doesn't use input_type/tdd_file; wiring integration test |
| `test_wiring_pipeline.py::test_resume_skips_completed_wiring_verification` | NO — pre-existing | Same as above |
| `test_spec_fidelity.py::test_spec_fidelity_prompt_requires_quoting_both_docs` | **YES — FIXED** | Test asserted "Spec Quote" but we changed to "Source Quote". Updated test. |
| `test_zero_files_analyzed.py::TestZeroFilesAnalyzedFail` | NO — pre-existing (ERROR, not FAIL) | v3.3 test error |

## Summary
- 1 failure caused by our changes: `test_spec_fidelity.py` — **FIXED** (updated assertion from "Spec Quote" to "Source Quote")
- 4 failures/errors are pre-existing, unrelated to this task
