# AC-C3 compare (tests/skills/)

- Baseline: 1109 passed in 14.13s (rc=0)
- Current: 1255 passed in 12.66s (rc=0)
- Baseline-passing tests that now fail: 0
- Verdict: PASS

## New test functions in this plan (all changed test files; parametrized cases add more ids)
- tests/commands/test_graph_command.py::test_graph_skill_documents_worker_flags_and_contract
- tests/commands/test_graph_command.py::test_graph_unattended_section_follows_init_section
- tests/commands/test_impact_command.py::test_impact_skill_documents_worker_flags_fields_and_cap
- tests/commands/test_impact_command.py::test_impact_unattended_section_between_outputs_and_boundaries
- tests/commands/test_workflow_command.py::test_worker_flags_and_worker_contract_are_documented_in_refs
- tests/skills/test_brainstorm_protocol.py::test_brainstorm_unattended_nested_directories_are_named
- tests/skills/test_worker_contract.py::test_ac_1_4_assertion_holds
- tests/skills/test_worker_contract.py::test_ac_1_4_check_fails_when_phrase_removed
- tests/skills/test_worker_contract.py::test_business_panel_frontmatter_is_not_inside_a_code_fence
- tests/skills/test_worker_contract.py::test_cleanup_audit_names_final_report_and_contract_write_exception
- tests/skills/test_worker_contract.py::test_explain_declares_write_under_tool_coordination
- tests/skills/test_worker_contract.py::test_index_repo_output_format_states_where_the_files_land
- tests/skills/test_worker_contract.py::test_init_lite_contract_exception_and_pass_through_are_documented
- tests/skills/test_worker_contract.py::test_load_usage_line_declares_checkpoint_and_load_is_not_converted
- tests/skills/test_worker_contract.py::test_nested_check_fails_on_nested_text_without_a_nested_list
- tests/skills/test_worker_contract.py::test_nested_propagation_text_matches_the_nested_list
- tests/skills/test_worker_contract.py::test_no_section_check_fails_when_an_unconverted_command_has_one
- tests/skills/test_worker_contract.py::test_only_brainstorm_lists_nested_commands
- tests/skills/test_worker_contract.py::test_p1_command_set_is_complete
- tests/skills/test_worker_contract.py::test_p1_set_check_fails_on_a_missing_extra_or_repeated_command
- tests/skills/test_worker_contract.py::test_unattended_section_check_fails_on_synthetic_defects
- tests/skills/test_worker_contract.py::test_unattended_section_check_fails_when_token_removed
- tests/skills/test_worker_contract.py::test_unattended_section_check_forbids_nested_text_without_a_nested_list
- tests/skills/test_worker_contract.py::test_unattended_section_content
- tests/skills/test_worker_contract.py::test_unattended_section_helper_reads_only_its_own_section
- tests/skills/test_worker_contract.py::test_unattended_sections_match_the_listed_commands
- tests/skills/test_worker_contract.py::test_unconverted_command_has_no_unattended_section
- !! REMOVED in tests/skills/test_worker_contract.py: ['test_no_command_has_unattended_mode_section_after_p0']
