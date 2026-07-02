# QA Report — Task Integrity (acceptance-traceability lens)

**Topic:** Phase 4 test coverage of the 16 setup-question IDs + 12 safe-lock predicates (detection-contract setup flow)
**Date:** 2026-07-02
**Phase:** task-integrity / synthesis-gate-equivalent
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## VERDICT: PASS

Every one of the 16 setup-question IDs and every one of the 12 safe-lock preconditions has at least one dedicated test in the assigned Phase-4 suites. The six behavior-bearing question IDs called out in checklist item 1 each have a dedicated *behavioral* test (not just an entry in the 16-ID ordered-list assertion). Two non-blocking observations are recorded under Findings; neither is an uncovered ID or predicate, so neither triggers the FAIL rule.

---

## Confidence

**Confidence:** Verified: 28/28 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

(28 = 16 question IDs + 12 predicates; each verified by reading the actual test body and, for the source-of-truth predicate list, the `LockGate.CHECK_IDS` tuple in `lockgate.py:27-40` and §6 of `merged-requirements.md`.)

**Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 4

All 7 assigned test files + `lockgate.py` + `merged-requirements.md` were read in full. Bash calls were `grep`/`mkdir` used to cross-check specific ID/predicate strings against test bodies. Tool-call count (13) exceeds the 28-item checklist only because each Read covers many checklist items at once; every ID/predicate below cites the specific test function that verifies it.

---

## Coverage Matrix A — 16 Setup-Question IDs

Source of truth for the ID set + order: `EXPECTED_QUESTION_IDS` in `test_contract_setup_questions.py:42-59`, asserted equal to `[q.id for q in SETUP_QUESTIONS]` by `test_setup_question_sequence_contains_all_16_questions_in_order` (existence + order + uniqueness for the full set).

| # | Question ID | Dedicated test | Kind |
|---|-------------|----------------|------|
| 1 | `repo` | `test_setup_question_sequence...` (list assertion) + used as observed provenance in `test_repo_mismatch_blocks_lock` (validation) | existence + behavioral |
| 2 | `probe_pr` | list assertion + PR-identity behavior in `test_cross_pr_shape_only_blocks_readiness` (evidence) / `test_write_lock_refused_when_gate_predicate_fails_cross_pr_shape_only` (writer) | existence + behavioral |
| 3 | `operation` | list assertion | existence |
| 4 | `evidence_source` | list assertion; evidence-source loading behavior in `test_load_evidence_records_deterministic_sha256` + `test_metadata_propagates_from_combined_payload` (evidence) | existence + behavioral |
| 5 | `surfaces_to_inspect` | list assertion; surface present/omitted behavior in `test_present_and_omitted_surfaces_are_distinct` (evidence) | existence + behavioral |
| 6 | `detected_augment_identity` | **behavioral:** `test_multiple_augment_identity_candidates_require_explicit_selection` (questions), `test_human_prose_does_not_produce_observed_augment_identity` + `test_user_supplied_identity_absent_from_payload_is_not_observed` + `test_real_augment_review_is_observed_identity` (evidence) | existence + behavioral ✓ |
| 7 | `author_association_values` | list assertion; association values carried on payloads (`author_association`) exercised through `_augment_clean_combined` in evidence/validation flows | existence |
| 8 | `emission_shape` | **behavioral:** `test_unobserved_emission_shape_cannot_be_locked` (questions) | existence + behavioral ✓ |
| 9 | `findings_locus` | **behavioral:** `test_findings_locus_resolves_against_evidence_when_findings_exist` (validation, asserts `findings_locus_recorded` check + `observed is True`) | existence + behavioral ✓ |
| 10 | `severity_field_path` | `test_severity_path_null_is_allowed_but_recorded_not_field_backed` + `test_severity_path_present_is_field_backed_and_distinct_from_null` (validation) | existence + behavioral |
| 11 | `review_completeness_signal` | list assertion + required-unobserved behavior in `test_setup_defaults_are_suggestions_not_lock_values_without_evidence` (questions) | existence + behavioral (see Finding 1) |
| 12 | `decline_detection_fields` | **behavioral:** `test_missing_decline_evidence_records_not_exercised` (questions AND validation) | existence + behavioral ✓ |
| 13 | `expected_classifier_result` | **behavioral:** `test_polling_expected_result_is_never_lockable` (questions), `test_polling_expected_result_rejected_as_non_lockable` (validation) | existence + behavioral ✓ |
| 14 | `run_validation` | **behavioral:** `test_validation_reuses_classify_seam_dry_run_only` (validation) — the dry-run classifier invocation is the behavioral realization of the "run validation" question | existence + behavioral ✓ |
| 15 | `write_local_locked_contract` | list assertion; write behavior in `test_write_lock_requires_explicit_confirmation` + `test_write_lock_writes_when_confirmed_and_gate_passes` (writer) | existence + behavioral |
| 16 | `next_step` | list assertion; next-command behavior in `test_ready_when_locked_evidence_and_passed_report` / `test_missing_when_no_local_override` (diagnosis) + `test_contract_status_runs_without_tasklist` (CLI) | existence + behavioral |

**All six behavior-bearing IDs required by checklist item 1** (`detected_augment_identity`, `emission_shape`, `findings_locus`, `expected_classifier_result`, `run_validation`, `decline_detection_fields`) have dedicated behavioral tests — marked ✓ above.

---

## Coverage Matrix B — 12 Safe-Lock Preconditions

Source of truth: `LockGate.CHECK_IDS` in `lockgate.py:27-40` (12 ordered check names) cross-referenced to `merged-requirements.md` §6 "Safe Locking Policy" (12 numbered preconditions). Mapping below is 1:1.

| # | §6 precondition / `CHECK_IDS` name | Dedicated test | File |
|---|-----------------------------------|----------------|------|
| 1 | evidence-exists-readable / `evidence_readable` | `test_load_evidence_records_deterministic_sha256`, `test_missing_probe_dir_raises`, `test_empty_probe_dir_with_no_json_raises` | evidence |
| 2 | evidence-tied-to-repo / `evidence_repo_bound` | `test_repo_mismatch_blocks_candidate_readiness` (evidence), `test_repo_mismatch_blocks_lock` (validation) — assert `repo_match` fails / `repo` blocker | evidence + validation |
| 3 | PR-identity / cross-PR-shape-only / `pr_identity_recorded` | `test_cross_pr_evidence_flagged_shape_only` + `test_cross_pr_shape_only_blocks_readiness` (evidence); `test_write_lock_refused_when_gate_predicate_fails_cross_pr_shape_only` (writer, names the `pr_identity_recorded` predicate) | evidence + writer |
| 4 | Augment-identity-observed-in-metadata / `identity_observed` | `test_real_augment_review_is_observed_identity` (observed=True) vs `test_human_prose_does_not_produce_observed_augment_identity` + `test_user_supplied_identity_absent_from_payload_is_not_observed` (observed=False) | evidence |
| 5 | emission-shape-observed / `emission_shape_observed` | `test_unobserved_emission_shape_cannot_be_locked` (questions) — unobserved shape blocks lock | questions |
| 6 | findings/completion-paths-resolve / `paths_resolve` | `test_findings_locus_resolves_against_evidence_when_findings_exist` (`findings_locus_recorded` passes) + required-unobserved completion-signal coverage in `test_setup_defaults_are_suggestions...` | validation + questions (see Finding 1) |
| 7 | expected-result-not-polling / `expected_not_polling` | `test_polling_expected_result_rejected_as_non_lockable` (asserts `expected_not_polling` check fails), `test_polling_expected_result_is_never_lockable` | validation + questions |
| 8 | classifier-returns-expected / `classifier_matches` | `test_findings_locus_resolves...` (`classifier_result == "findings"`, report passes) + `test_validation_reuses_classify_seam_dry_run_only` (classifier drives result) + `test_write_lock_refused_when_expected_result_polling` (writer) | validation + writer |
| 9 | negative-controls-not-false-positive / `negative_controls_pass` | `test_negative_controls_empty_and_non_augment_do_not_classify_reviewed` (asserts both controls PASS + classify to POLLING) | validation |
| 10 | validation-report-written-with-hash / `report_written` | `test_lock_metadata_includes_evidence_hash_and_validation_report` + `test_write_lock_refused_when_report_not_written` (writer, `report_written` predicate fails when report absent) + `test_missing_evidence_hash_blocks_lock` (validation) | writer + validation |
| 11 | explicit-user-confirmation / `user_confirmed` | `test_write_lock_requires_explicit_confirmation` (refusal names `user_confirmed`) + `test_write_lock_writes_when_confirmed_and_gate_passes` | writer |
| 12 | target-path-is-dev-pr-monitor-only / `dest_under_pr_monitor` | `test_lock_destination_is_exactly_dev_pr_monitor_under_cwd`, `test_lock_destination_off_target_is_refused`, `test_no_write_under_claude_mirror`, `test_no_write_under_src_shipped_ref` | writer |

**All 12 preconditions have at least one dedicated test.** No uncovered predicate.

---

## Summary

- Question IDs covered: 16 / 16
- Behavior-bearing question IDs with dedicated behavioral tests: 6 / 6
- Safe-lock predicates covered: 12 / 12
- Uncovered questions: 0
- Uncovered predicates: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

---

## Findings (non-blocking — no uncovered ID or predicate)

| # | Severity | Location | Observation | Note |
|---|----------|----------|-------------|------|
| 1 | MINOR | `paths_resolve` predicate / `review_completeness_signal` (Q11) | The `findings_locus` half of the composite `paths_resolve` predicate has a **positive resolving** assertion (`findings_locus_recorded` passes against real findings evidence). The `review_completeness_signal` / completion-signal half is covered only via the **negative** path (asserted as required-unobserved with an empty payload in `test_setup_defaults_are_suggestions...`). There is no positive test asserting a completion signal *resolves* against clean/no-findings evidence and drives `paths_resolve` to pass. Coverage of the ID and predicate exists (both halves have provenance assertions), so this is not an uncovered item — but the completion-signal resolution path is asymmetrically weaker than the findings-locus path. | Not a FAIL. Recommend a follow-up positive test for completion-signal resolution on clean evidence if this suite is extended. |
| 2 | INFO | Q7 `author_association_values` | Covered by the 16-ID list assertion; `author_association` values are present on the payload fixtures (`_augment_clean_combined`) and thus flow through evidence/validation, but there is no test that *specifically* asserts author-association handling behavior. Per §4 Q7 the field is only conditionally required ("empty is allowed unless classifier validation requires it"), so a dedicated behavioral test is not mandated by the checklist (Q7 is not in the behavior-bearing subset). | Not a FAIL. Existence coverage satisfies the checklist. |

---

## Recommendations

- PASS — Phase 4 acceptance-traceability is satisfied; the suite may proceed.
- Optional (non-blocking): add one positive test asserting `review_completeness_signal` resolves against clean/no-findings evidence, to bring the completion-signal half of `paths_resolve` to parity with the findings-locus half (Finding 1).

## QA Complete
