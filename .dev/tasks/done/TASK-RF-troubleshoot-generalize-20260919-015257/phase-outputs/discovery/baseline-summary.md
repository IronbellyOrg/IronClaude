# Baseline pytest (item 0.4) — recorded BEFORE any edit

Worktree: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize`
HEAD: `5d35643eae43131965a6e5e029ccfc3e589faf12` (`origin/master`)
Date: 2026-09-19

## tests/troubleshoot/

- Capture: `baseline-pytest-troubleshoot.txt`
- Summary: **1 failed, 70 passed** in 15.04s (71 collected)
- Known-red (do NOT fix): `tests/troubleshoot/backtest/test_backtest_e4.py::test_backtest_e4_new_gate_catches_via_contract_enumeration_ref`
  - Assertion: H2 ref must require BOTH `gate_passed` AND `_evaluate_gate` consumers be classified
  - File: `tests/troubleshoot/backtest/test_backtest_e4.py:105`

## Full suite

- Capture: `baseline-pytest-full.txt`
- Summary: **25 failed, 11361 passed, 139 skipped, 2 xpassed, 37 warnings, 1 error** in 412.66s (0:06:52)
- Pre-existing reds (verbatim node ids; later runs MUST not add to this set):

1. `tests/audit/test_invariant_preservation_NFR_6_through_10.py::TestInvariant3_PersistentArtifact::test_task_id_naming_pattern_preserved`
2. `tests/cli/eval/test_eval_run.py::test_d0072_spec_documents_flag_wiring`
3. `tests/cli/eval/test_validation_commands.py::test_evidence_root_directory_exists`
4. `tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[01-targeted-pytest]`
5. `tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[02-make-verify-sync]`
6. `tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[03-eval-doctor]`
7. `tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[04-eval-run-E1]`
8. `tests/cli/test_cli_registration.py::test_top_level_command_roster_unchanged`
9. `tests/pr_submit/test_hook_update.py::test_hook_points_at_src_source`
10. `tests/pr_submit/test_hook_update.py::test_t701_offer_mentions_both_commands`
11. `tests/pr_submit/test_hook_update.py::test_t702_non_matching_command_exits_zero`
12. `tests/pr_submit/test_hook_update.py::test_t703_failed_pr_create_exits_zero`
13. `tests/pr_submit/test_static_grep.py::test_t104_every_gh_call_is_repo_scoped`
14. `tests/pr_submit/test_static_grep.py::test_tn40_no_depth_quick_fix_anywhere`
15. `tests/sprint/e2e_real/test_e2e_resume.py::TestE2EResume::test_e2e_run_autodetect_task_level`
16. `tests/sprint/e2e_real/test_e2e_resume.py::TestE2EResume::test_e2e_hard_crash_phase_level`
17. `tests/sprint/e2e_real/test_e2e_resume_drift_stop.py::TestE2EResumeDriftStop::test_e2e_run_stops_on_material_tasklist_drift`
18. `tests/sprint/e2e_real/test_e2e_resume_fresh.py::TestE2EResumeFresh::test_e2e_run_fresh_disables_autoresume`
19. `tests/sprint/e2e_real/test_e2e_resume_fresh.py::TestE2EResumeFresh::test_e2e_run_autoresume_without_fresh_reexecutes_only_failed_task`
20. `tests/sprint/e2e_real/test_e2e_resume_multiphase.py::test_e2e_run_autodetect_task_level_across_phase_boundary`
21. `tests/sprint/test_rerun_tasks_e2e.py::TestRerunTasksRoundTrip::test_rerun_renames_originals_flips_checkboxes_emits_event_runs_verify_checkpoints`
22. `tests/sprint/test_rerun_tasks_e2e.py::TestRerunTasksMergeBackNoForce::test_merge_back_succeeds_without_force_merge`
23. `tests/sprint/test_resume.py::TestCliWiring::test_explicit_start_bypasses_autodetect`
24. `tests/sprint/test_resume.py::TestCliWiring::test_nothing_to_resume_cli`
25. `tests/troubleshoot/backtest/test_backtest_e4.py::test_backtest_e4_new_gate_catches_via_contract_enumeration_ref` (known-red)
26. ERROR `tests/v3.3/test_zero_files_analyzed.py::TestZeroFilesAnalyzedFail::test_zero_files_analyzed_returns_fail`
