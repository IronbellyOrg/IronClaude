# Phase 12 validation (item 12.5)

Run 2026-11-12 after items 12.1 to 12.4. Each block: the command, its exit code, the last 30 lines of output and one PASS or FAIL line.

## Check 1 ruff check

Command: `uv run ruff check tests/skills/test_worker_contract.py`
```text
All checks passed!
(exit 0)
```
Check 1 ruff check: PASS (exit 0, expected 0)

## Check 2 ruff format --check

Command: `uv run ruff format --check tests/skills/test_worker_contract.py`
```text
1 file already formatted
(exit 0)
```
Check 2 ruff format --check: PASS (exit 0, expected 0)

## Check 3 pytest tests/skills tests/core

Command: `uv run pytest tests/skills tests/core -v`
```text
tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S15-sprint-tasklist-bundle-targets14-inputs14-boundaries14] PASSED [ 98%]
tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S16-roadmap-fidelity-targets15-inputs15-boundaries15] PASSED [ 98%]
tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S17-tier-validation-targets16-inputs16-boundaries16] PASSED [ 98%]
tests/core/test_how_we_work_routing_table.py::test_specialist_matching_and_unavailable_contract_are_shared_not_keyword_first PASSED [ 98%]
tests/core/test_how_we_work_routing_table.py::test_reports_keep_specialist_objective_instead_of_generic_competitor PASSED [ 98%]
tests/core/test_how_we_work_routing_table.py::test_requested_analysis_research_explain_modes_are_not_forced_defaults PASSED [ 98%]
tests/core/test_how_we_work_routing_table.py::test_adversarial_generation_comparison_and_pipeline_remain_exclusive PASSED [ 98%]
tests/core/test_how_we_work_routing_table.py::test_cleanup_audit_and_improvement_have_separate_authority_boundaries PASSED [ 99%]
tests/core/test_how_we_work_routing_table.py::test_previews_documentation_and_suite_runs_disclose_actual_writes PASSED [ 99%]
tests/core/test_how_we_work_routing_table.py::test_diagnosis_reflection_and_review_preserve_remediation_coupling PASSED [ 99%]
tests/core/test_how_we_work_routing_table.py::test_reflect_optional_inputs_and_report_only_post_flags PASSED [ 99%]
tests/core/test_how_we_work_routing_table.py::test_pr_monitor_ceiling_is_conditional_and_each_branch_has_one_exact_value PASSED [ 99%]
tests/core/test_how_we_work_routing_table.py::test_pr_attachment_monitor_log_resume_and_silence_are_not_new_shipping PASSED [ 99%]
tests/core/test_how_we_work_routing_table.py::test_other_operations_preserve_requested_authority_and_owned_state PASSED [ 99%]
tests/core/test_how_we_work_routing_table.py::test_lifecycle_and_contract_gaps_do_not_certify_stale_or_mixed_interfaces PASSED [ 99%]
tests/core/test_how_we_work_routing_table.py::test_swarm_settings_help_retains_inputs_without_inferred_real_launch PASSED [ 99%]
tests/core/test_how_we_work_routing_table.py::test_explicit_cleanup_controls_and_pr_attachment_do_not_gain_default_actions PASSED [ 99%]
tests/core/test_how_we_work_routing_table.py::test_grouped_required_flags_still_use_exact_flag_tokens PASSED [ 99%]
tests/core/test_how_we_work_routing_table.py::test_task_and_implement_verification_claims_are_not_universal_test_guarantees PASSED [ 99%]
tests/core/test_orca_session_launch_guidance.py::test_orca_session_launch_guidance[core/CLAUDE.md] PASSED [ 99%]
tests/core/test_orca_session_launch_guidance.py::test_orca_session_launch_guidance[skills/ccsession-tag/README.md] PASSED [ 99%]
tests/core/test_orca_session_launch_guidance.py::test_appended_paragraph_names_the_owner_roles_and_no_source_path[core/CLAUDE.md] PASSED [ 99%]
tests/core/test_orca_session_launch_guidance.py::test_appended_paragraph_names_the_owner_roles_and_no_source_path[skills/ccsession-tag/README.md] PASSED [ 99%]
tests/core/test_orca_session_launch_guidance.py::test_appended_paragraph_is_identical_in_both_copies PASSED [ 99%]
tests/core/test_research_config.py::test_each_depth_profile_names_concrete_params_and_tools PASSED [ 99%]
tests/core/test_research_config.py::test_advanced_only_with_gating_language PASSED [ 99%]
tests/core/test_research_config.py::test_discovery_caps_and_crawl_truncation_present PASSED [ 99%]
tests/core/test_research_config.py::test_map_and_crawl_tool_ids_present PASSED [100%]

============================ 2008 passed in 53.62s =============================
(exit 0)
```
Check 3 pytest tests/skills tests/core: PASS (exit 0, expected 0)

## Check 4 src/superclaude paths in the contract

Command: `grep -n 'src/superclaude' src/superclaude/core/WORKER-CONTRACT.md` compared with `git show HEAD:src/superclaude/core/WORKER-CONTRACT.md | grep -c 'src/superclaude'`
```text
now=0 head=0
```
Check 4 src/superclaude hit count: PASS (now 0 equals HEAD 0; the edits add none)
