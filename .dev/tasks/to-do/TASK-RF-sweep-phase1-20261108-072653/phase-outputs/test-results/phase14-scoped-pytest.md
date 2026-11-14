# Phase 14 scoped test run (item 14.3)

Run 2026-11-12.

Command: `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -v`

Exit code: 0

Counts (last summary line): ============================ 3220 passed in 56.99s =============================
FAILED lines: 0  ERROR lines: 0  SKIPPED lines: 0

Last 40 lines of output:
```text
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S10] PASSED [ 98%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S11] PASSED [ 98%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S12] PASSED [ 98%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S13] PASSED [ 98%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S14] PASSED [ 98%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S15] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S16] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S17] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S18] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S19] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S20] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S21] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S22] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S23] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S24] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S25] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S26] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S27] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S28] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S29] PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_unmatched_cache_expectation_rejects_unconditional_wording PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_conditional_step_guard_rejects_incidental_only PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_cache_expectation_follows_the_guide_block PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_matched_routes_bypass_cache_so_seeded_rows_cannot_win PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_unmatched_cache_hints_are_consulted_then_rejected PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_example_only_flags_are_not_declared_or_routed PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_retired_identities_have_no_shipped_command PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_command_dispositions_trace_appendix_c_and_inventory PASSED [ 99%]
tests/recommend/test_routing_refresh.py::test_analyst_reports_and_disposition_appendix_are_retained PASSED [ 99%]
tests/recommend/test_telemetry.py::TestTelemetryAppend::test_append_event_writes_exactly_five_fields PASSED [ 99%]
tests/recommend/test_telemetry.py::TestTelemetryAppend::test_append_event_is_line_oriented PASSED [ 99%]
tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[miss] PASSED [ 99%]
tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[HIT] PASSED [ 99%]
tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[cold] PASSED [ 99%]
tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[success] PASSED [ 99%]
tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[] PASSED [ 99%]
tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[miss_unknown] PASSED [ 99%]
tests/recommend/test_telemetry.py::TestTelemetryAppend::test_all_six_valid_cache_results_accepted PASSED [100%]

============================ 3220 passed in 56.99s =============================
```

Scoped run: PASS (exit 0, 0 failed)
