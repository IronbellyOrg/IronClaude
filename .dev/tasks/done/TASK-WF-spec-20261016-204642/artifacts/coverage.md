# Cosmos acceptance coverage

All paths and commands below are relative to the isolated worktree root. Each `file::function` is a
runnable pytest selector: `uv run pytest <selector> -q`. Parametrized functions run every listed case.

## A1–A16 mapping

| Case | Executable regressions | Boundary checked |
|---|---|---|
| A1 | `tests/pr_submit/test_cosmos_review.py::test_a1_a5_resolved_old_thread_never_poisons_clean` | Current-head zero marker remains clean with resolved old root, null or integer line. |
| A2 | `tests/pr_submit/test_cosmos_review.py::test_a2_old_head_only_polls` | Old-head evidence cannot complete current-head wait. |
| A3 | `tests/pr_submit/test_cosmos_review.py::test_a3_a14_positive_count_requires_enough_detail_no_partial_dispatch` | Positive count without enough usable detail polls, no partial dispatch. |
| A4 | `tests/pr_submit/test_cosmos_review.py::test_a4_a14_older_open_root_survives_zero_count_and_watermark` | Old unresolved outdated root survives zero marker and re-trigger watermark. |
| A5 | `tests/pr_submit/test_cosmos_review.py::test_a1_a5_resolved_old_thread_never_poisons_clean`; `tests/pr_submit/test_cosmos_poll.py::test_reply_later_page_and_already_resolved` | Resolved root excluded; already-resolved lookup skips before reply/resolve. |
| A6 | `tests/pr_submit/test_cosmos_review.py::test_a6_marker_field_validation`; `tests/pr_submit/test_cosmos_review.py::test_a6_bad_marker_never_falls_back_to_legacy_clean`; `tests/pr_submit/test_cosmos_review.py::test_duplicate_marker_even_unsupported_duplicate_blocks_completion` | JSON/envelope/version/status/count/SHA/duplicate validation, no legacy-clean fallback. |
| A7 | `tests/pr_submit/test_cosmos_review.py::test_a7_review_commit_and_marker_must_agree`; `tests/pr_submit/test_cosmos_review.py::test_a7_explicit_head_is_not_ignored` | Review commit, marker head and explicit expected head attribution. |
| A8 | `tests/pr_submit/test_cosmos_review.py::test_a8_completion_must_be_strictly_newer`; `tests/pr_submit/test_cosmos_review.py::test_actual_instants_not_lexical_timestamp_order`; `tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_requires_strict_time_attribution` | Strictly newer aware timestamps; equal/invalid/missing watermark blocked in S5. |
| A9 | `tests/pr_submit/test_cosmos_review.py::test_a9_unordered_reviews_human_and_other_bot_are_ignored`; `tests/pr_submit/test_cosmos_review.py::test_newer_or_unorderable_same_head_evidence_cannot_be_bypassed`; `tests/pr_submit/test_cosmos_review.py::test_graphql_review_shape_and_case_insensitive_full_sha` | Latest relevant review, identity variants and bad newer evidence. |
| A10 | `tests/pr_submit/test_cosmos_poll.py::test_poll_all_pages_and_raw_provenance`; `tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root` | Real shell retrieves later REST reviews/thread pages; later root reaches normalization. |
| A11 | `tests/pr_submit/test_cosmos_poll.py::test_rest_malformed_and_failures`; `tests/pr_submit/test_cosmos_poll.py::test_rest_later_page_failure_and_repeated_page`; `tests/pr_submit/test_cosmos_poll.py::test_poll_invalid_threads`; `tests/pr_submit/test_cosmos_poll.py::test_poll_later_thread_failure_or_invalid_completion`; `tests/pr_submit/test_cosmos_poll.py::test_thread_connection_shape`; `tests/pr_submit/test_cosmos_review.py::test_a11_incomplete_flags_block_both_public_seams` | API/GraphQL failures, null/malformed collections, cursor termination and completeness flags fail closed. |
| A12 | `tests/pr_submit/test_cosmos_review.py::test_a12_root_only_selection_and_human_root_with_bot_reply`; `tests/pr_submit/test_cosmos_poll.py::test_poll_all_pages_and_raw_provenance` | Root-only query; one finding despite replies; bot reply cannot adopt human root. Stub enforces repo/query pins. |
| A13 | `tests/pr_submit/test_severity_router.py::test_raw_severity_normalization`; `tests/pr_submit/test_severity_router.py::test_raw_low_hint_still_obeys_category_floor_and_verification` | Production Markdown LF/CRLF/normalized hints, precedence, Medium fallback and category floor; remote verification not trusted. |
| A14 | `tests/pr_submit/test_cosmos_review.py::test_a3_a14_positive_count_requires_enough_detail_no_partial_dispatch`; `tests/pr_submit/test_cosmos_review.py::test_a4_a14_older_open_root_survives_zero_count_and_watermark`; `tests/pr_submit/test_cosmos_review.py::test_count_is_lower_bound_not_equality_with_historical_threads` | Counts cannot erase old open roots or license clean without detail; no historical count equality assumption. |
| A15 | `tests/pr_submit/test_cosmos_review.py::test_a15_legacy_synthetic_and_explicit_attribution`; `tests/pr_submit/test_cosmos_review.py::test_a15_decline_precedence_only_valid_completion_overrides`; `tests/pr_submit/test_skill_parse.py::test_t101_monitor_choices_valid`; `tests/pr_submit/test_loop_guard.py::test_t620_629_fence_post_matrix`; `tests/pr_submit/test_severity_router.py::test_tn30_router_remap_coverage` | Legacy/decline compatibility, ordinals, capped rounds and existing severity routes; full suite retains other gates. |
| A16 | `tests/pr_submit/test_cosmos_protocol.py::test_real_poll_to_documented_gate_preserves_later_root`; `tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_binds_actual_exports_and_same_context`; `tests/pr_submit/test_severity_router.py::test_selected_cosmos_root_normalizes_same_identity_and_nullable_locus` | Real shell JSON to documented gate to shared selector to exported adapter, stable IDs, null current line, unverified provenance and Low report-only route. |

Additional guard regressions:
- `tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_blocks_advanced_snapshot_before_head_override`
  proves an explicit public override alone can accept the pushed review after the actual snapshot head
  advances, then executes the documented caller guard and verifies classification is not called.
- `tests/pr_submit/test_cosmos_protocol.py::test_attended_gate_empty_legacy_signal_is_not_empty_driver_clean`
  and `test_attended_gate_normalization_valueerror_discards_entire_batch` execute the documented gate:
  empty legacy signals or invalid roots become polling, never an empty findings driver input.
- `tests/pr_submit/test_cosmos_poll.py::test_poll_changed_head_invalidates_entire_snapshot` checks the
  adapter's separate within-collection race guard; reply tests cover conflicting IDs, incomplete later
  lookup pages, path/line lookalikes and invalid mutation responses without real writes.
- `tests/pr_submit/test_cosmos_review.py::test_future_submission_cannot_establish_completion_or_bypass_newer_evidence`
  and `test_cosmos_requires_trustworthy_snapshot_observation` validate the pure snapshot-time boundary.
- `tests/pr_submit/test_cosmos_protocol.py::test_protocol_refs_pin_live_boundaries_and_existing_gates`
  checks canonical doc wiring and unchanged shipped identities/default trigger.

## Runnable validation

```bash
uv run pytest tests/pr_submit/test_cosmos_protocol.py -q
uv run pytest tests/pr_submit/test_cosmos_review.py tests/pr_submit/test_cosmos_poll.py tests/pr_submit/test_severity_router.py tests/pr_submit/test_cosmos_protocol.py -q
uv run pytest tests/pr_submit -q
uv run ruff check src/superclaude/pr_submit/{__init__,classifier,detection,models,severity_router}.py tests/pr_submit/{test_cosmos_protocol,test_cosmos_review,test_cosmos_poll,test_detection_contract,test_severity_router,test_static_grep}.py
uv run ruff format --check src/superclaude/pr_submit/{__init__,classifier,detection,models,severity_router}.py tests/pr_submit/{test_cosmos_protocol,test_cosmos_review,test_cosmos_poll,test_detection_contract,test_severity_router,test_static_grep}.py
for script in src/superclaude/skills/sc-pr-submit-protocol/scripts/*.sh; do bash -n "$script" || exit; done
make sync-dev
make verify-sync
git diff --check
```

Task4 results: focused protocol **15 passed**; combined focused Cosmos regressions **237 passed**;
full `tests/pr_submit` **593 passed**. Changed Python
lint/format checks passed (11 files; focused test rechecked after its final edit); all PR-submit shell
syntax checks passed; sync-dev, verify-sync and whitespace checks passed. All shell integration tests
use an executable isolated stub, not real external mutations. No core/script/model edits belong to
Task4; no commits, pushes, GitHub writes, ledger/source changes or archiving were performed.

## Synthetic versus live evidence

`tests/pr_submit/fixtures/cosmos-pr266.json` is a **sanitized synthetic PR266-shaped fixture**, not a
verbatim live recording: representative timestamps, path, prose and opaque GraphQL IDs. The new
poll-to-normalize test also uses stubbed APIs and synthetic data; it is not a live PR regression run.

The parent-owned, already-passed read-only live check is separately recorded in
[artifacts/live-pr266-check.md](live-pr266-check.md): observed `2026-10-16T21:08:57Z`, complete snapshot,
`clean`, three reviews, one thread, zero actionable roots. It exercised the actual poll/API/classifier
boundary, not normalization of an open finding. Task4 did not repeat it or perform remote writes.

Independent Task4 QA and the final whole-plan FINAL review remain parent-owned; this coverage map is
not either verdict and does not authorize archiving.
