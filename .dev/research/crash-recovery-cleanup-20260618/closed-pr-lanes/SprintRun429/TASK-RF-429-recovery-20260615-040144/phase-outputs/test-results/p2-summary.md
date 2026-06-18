# P2 Test Summary (Step 3.5)

**Targeted:** `uv run pytest tests/sprint/test_models.py tests/sprint/test_rerun_tasks.py tests/sprint/test_resume.py -v` → **193 passed, 0 failed** (0.37s).
**Marker:** `uv run pytest -m backward_compat -v` → **20 passed, 1 skipped, 0 failed** (7.04s).

All 7 new P2 tests pass:
- `TestProviderExhaustedStatus::test_provider_exhausted_value_and_membership` — value `fail_provider_exhausted`, is_failure True, is_success False, value-lookup round-trip.
- `TestTaskResultExhaustionBackCompat::test_taskresult_from_dict_old_payload_round_trips` (@backward_compat) — OLD dict without the 3 keys loads without KeyError, fields default to ""/0/"".
- `TestTaskResultExhaustionBackCompat::test_taskresult_new_fields_round_trip` (@backward_compat) — new fields survive to_dict→from_dict.
- `TestClassifyTranscriptProviderExhaustion` (3 cases) — `_classify_transcript` returns FAIL_PROVIDER_EXHAUSTED for single_account_429 + all_account_cooldown (RED→GREEN), FAIL_TERMINAL for task_failure_real (no over-capture).
- `TestResumePlanner::test_resume_reruns_provider_exhausted_task` — planner ZERO-EDIT auto-routing re-runs the exhausted task at TASK granularity.

**Note:** an initial run surfaced 1 failure caused by the append Edit splitting the pre-existing `test_base_argv_without_positional_is_rejected` control test (its second assertion `assert "Missing argument 'INDEX_PATH'" in result.output` was orphaned). Fixed by restoring that assertion to the control test and removing the orphan from the new test class; both verified against `git show HEAD:`. No regressions remain.
