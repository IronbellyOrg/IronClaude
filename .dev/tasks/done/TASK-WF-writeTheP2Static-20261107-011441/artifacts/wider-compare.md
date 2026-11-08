# Wider run comparison

| Run | File | Result |
|---|---|---|
| Baseline (HEAD 576b6659, before this plan) | `t1-baseline-wider.txt` | 9164 passed, 30 skipped, 1 xpassed, 5 warnings in 434.43s (0:07:14), rc=0 |
| Final (after the debates and the reflect change) | `wider-run.txt` | 9165 passed, 30 skipped, 1 xpassed, 5 warnings in 433.27s (0:07:13), rc=0 |

Command (both runs): `uv run pytest tests/core tests/commands tests/recommend tests/cli tests/cli_portify tests/unit tests/roadmap tests/tasklist tests/troubleshoot tests/pr_submit tests/docs tests/agents -q -rf -p no:cacheprovider --ignore=tests/cli/eval/test_perf_home_setup.py` (the ignored test rewrites a tracked evidence file).

Failures after the plan: 0. Baseline-passing tests that now fail: none. Passed count rose by 1 (9164 to 9165): the one test this plan added outside tests/skills is in `tests/commands/test_workflow_command.py` (Task 17); the other new tests are in `tests/skills/` (see `ac-c3-compare.md`). The skipped, xpassed and warning counts are unchanged.

## Pre-existing test files named in the plan Constraints

The plan names 33 entries (32 files and the `tests/troubleshoot/` folder). They were run together after Task 20 (`uv run pytest <files> -q -p no:cacheprovider`: 75 test files, all passing, 2329 tests). Per-file results are in `named-files-results.txt`.

```text
PASS tests/agents/test_tavily_tool_parity.py: 4 tests, 0 failed, 0 skipped
PASS tests/cli/eval/test_workflow_vs_task_builder_companion.py: 125 tests, 0 failed, 0 skipped
PASS tests/cli/reflect/test_remediation_route_table.py: 4 tests, 0 failed, 0 skipped
PASS tests/cli/test_tdd_extract_prompt.py: 68 tests, 0 failed, 0 skipped
PASS tests/cli_portify/test_brainstorm_gaps.py: 16 tests, 0 failed, 0 skipped
PASS tests/commands/test_auggie_review_remediation_chain.py: 12 tests, 0 failed, 0 skipped
PASS tests/commands/test_auggie_review_revagent.py: 12 tests, 0 failed, 0 skipped
PASS tests/commands/test_impact_command.py: 81 tests, 0 failed, 0 skipped
PASS tests/commands/test_research_command.py: 2 tests, 0 failed, 0 skipped
PASS tests/commands/test_routing_plugin_parity.py: 5 tests, 0 failed, 0 skipped
PASS tests/commands/test_workflow_command.py: 19 tests, 0 failed, 0 skipped
PASS tests/core/test_how_we_work_routing_table.py: 79 tests, 0 failed, 0 skipped
PASS tests/docs/test_onboarding_deck.py: 3 tests, 0 failed, 0 skipped
PASS tests/pr_submit/test_static_grep.py: 21 tests, 0 failed, 0 skipped
PASS tests/recommend/test_dispatch.py: 16 tests, 0 failed, 0 skipped
PASS tests/recommend/test_routing_refresh.py: 248 tests, 0 failed, 0 skipped
PASS tests/skills/test_brainstorm_protocol.py: 4 tests, 0 failed, 0 skipped
PASS tests/skills/test_codegraph_adoption.py: 50 tests, 0 failed, 0 skipped
PASS tests/skills/test_issue_protocol.py: 78 tests, 0 failed, 0 skipped
PASS tests/skills/test_model_alias_policy.py: 13 tests, 0 failed, 0 skipped
PASS tests/skills/test_primitive_dual_surface_lookup.py: 3 tests, 0 failed, 0 skipped
PASS tests/skills/test_reflect_input_snapshot.py: 15 tests, 0 failed, 0 skipped
PASS tests/skills/test_review_severity_rule.py: 62 tests, 0 failed, 0 skipped
PASS tests/skills/test_sc_recommend_routing_contract.py: 28 tests, 0 failed, 0 skipped
PASS tests/skills/test_task_builder_merge.py: 68 tests, 0 failed, 0 skipped
PASS tests/skills/test_task_workspace_smoke.py: 4 tests, 0 failed, 0 skipped
PASS tests/skills/test_tier2_tavily_consistency.py: 5 tests, 0 failed, 0 skipped
PASS tests/skills/test_worker_contract.py: 684 tests, 0 failed, 0 skipped
PASS tests/tasklist/test_bash_policy_contract.py: 2 tests, 0 failed, 0 skipped
PASS tests/tasklist/test_tasklist_cli.py: 70 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_backtest_e1.py: 2 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_backtest_e2.py: 2 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_backtest_e3.py: 2 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_backtest_e4.py: 2 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_backtest_e5.py: 2 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_backtest_status_separation.py: 3 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_catch_rate_aggregation.py: 7 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_catch_rate_schema.py: 19 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_git_replay_integration.py: 2 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_git_replay_unit.py: 4 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_path_resolution.py: 1 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_replay_executor.py: 6 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/backtest/test_waiver_regreen.py: 1 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_behaviour_definition_row.py: 3 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_calibrator_assertions.py: 46 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_calibrator_eval_cases.py: 35 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_codegraph_grounding.py: 5 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_cosmetic_counter.py: 1 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_counter_key.py: 1 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_diagnostic_worker_contract.py: 50 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_discriminator_form.py: 2 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_discriminator_rows.py: 5 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_hardening_h0.py: 2 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_hardening_h1.py: 1 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_hardening_h2.py: 2 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_hardening_h3.py: 3 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_hardening_h4.py: 2 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_hardening_output_contract.py: 3 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_hardening_verdict.py: 6 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_hardstop_verdicts.py: 4 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_hc_rename_guard.py: 1 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_headline_threshold.py: 2 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_inline_fallback_parity.py: 3 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_locus_card.py: 16 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_menu_equality.py: 14 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_primitive_differential.py: 3 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_primitivegrep_targeting.py: 1 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_producers_enumeration.py: 7 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_regression_sysbox.py: 3 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_threshold_bracket.py: 3 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_timestamp_tolerance.py: 3 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_validator_assertions.py: 122 tests, 0 failed, 0 skipped
PASS tests/troubleshoot/test_verdict_source.py: 3 tests, 0 failed, 0 skipped
PASS tests/unit/test_cli_doctor.py: 30 tests, 0 failed, 0 skipped
PASS tests/unit/test_cli_install.py: 96 tests, 0 failed, 0 skipped
```
