72dd6956e9a4db06db3781c2455ef0c42f178083
Review one task for spec compliance.

Task brief: Depends on: Task 13

Run the full suite and checks the source names (section 16 last line, section 20 item 9): `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py`, then the full suite `uv run pytest` (`make test` runs the same command), then `make lint`, then `make verify-sync`. Fix every failure caused by this feature in the file that causes it (re-running `make sync-dev` after any `src/superclaude/` fix). A failure that also occurs on master without this feature's changes is not fixed here: show that by running the same failing test on master in a temporary Orca worktree (`orca worktree create --name issue302-master-check --base-branch origin/master`; never a raw `git worktree add`), record it as pre-existing with the test ID and error line, then remove the worktree with `orca worktree rm --worktree name:issue302-master-check`.

Acceptance criteria:
- `./artifacts/t14-targeted.log`, `./artifacts/t14-full-pytest.log`, `./artifacts/t14-lint.log` and `./artifacts/t14-verify-sync.log` exist and hold the command outputs with their exit codes.
- `uv run pytest` reports no failure caused by this feature; `make lint` and `make verify-sync` exit 0.
- Every remaining failure is listed in `./artifacts/t14-failures.md` with the test ID, the error line and the evidence that it also fails on master; if there are none, the file says so.
- `orca worktree list` shows no `issue302-master-check` worktree.
- `git add .dev/tasks` has been run so this package and its `artifacts/` are staged; nothing is committed or pushed.

AC ids: T14.AC1..T14.AC5 = the five acceptance bullets in order.
Artifacts in .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/: t14-targeted.log, t14-full-pytest.log, t14-lint.log, t14-verify-sync.log, t14-failures.md, t14-make-install.log, t14-worktree-and-staging.txt. The full-suite log has 15073 lines and is NOT inlined in the diff below; read it at .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-full-pytest.log (its outcome line is near the end, followed by `rc=`).
Environment actions taken in this task, both disclosed in t14-failures.md: `make install` (the project's setup target) installed the dev extras so ruff exists for `make lint`; the full suite rewrote the tracked file .dev/releases/current/cliEval/evidence/T02.15/perf.json (an existing perf test writes it) and the executor restored it with `git restore` so no unrelated change remains. No source file was changed by this task.

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 72dd6956e9a4db06db3781c2455ef0c42f178083
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-targeted.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-targeted.log
new file mode 100644
index 00000000..089a2022
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-targeted.log
@@ -0,0 +1,1424 @@
+$ uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/.venv/bin/python
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collecting ... collected 1411 items
+
+tests/commands/test_auggie_review_remediation_chain.py::test_chain_order[command option row] PASSED [  0%]
+tests/commands/test_auggie_review_remediation_chain.py::test_chain_order[command example] PASSED [  0%]
+tests/commands/test_auggie_review_remediation_chain.py::test_chain_order[skill step 4] PASSED [  0%]
+tests/commands/test_auggie_review_remediation_chain.py::test_chain_order[ref offer prompt] PASSED [  0%]
+tests/commands/test_auggie_review_remediation_chain.py::test_dispatch_never_branches_on_depth[command option row] PASSED [  0%]
+tests/commands/test_auggie_review_remediation_chain.py::test_dispatch_never_branches_on_depth[command example] PASSED [  0%]
+tests/commands/test_auggie_review_remediation_chain.py::test_dispatch_never_branches_on_depth[skill step 4] PASSED [  0%]
+tests/commands/test_auggie_review_remediation_chain.py::test_dispatch_never_branches_on_depth[ref offer prompt] PASSED [  0%]
+tests/commands/test_auggie_review_remediation_chain.py::test_dispatch_literals PASSED [  0%]
+tests/commands/test_auggie_review_remediation_chain.py::test_removed_deep_route_is_gone_from_the_primitive PASSED [  0%]
+tests/commands/test_auggie_review_remediation_chain.py::test_resume_without_spec_or_plan_restarts_at_phase_a PASSED [  0%]
+tests/commands/test_auggie_review_remediation_chain.py::test_resume_without_plan_reruns_phase_b_not_an_unconditional_fallback PASSED [  0%]
+tests/commands/test_auggie_review_revagent.py::test_accepted_set_is_exactly_the_agent_tool_enum PASSED [  0%]
+tests/commands/test_auggie_review_revagent.py::test_command_surface PASSED [  0%]
+tests/commands/test_auggie_review_revagent.py::test_unsupported_value_stop_and_examples_in_same_bullet PASSED [  1%]
+tests/commands/test_auggie_review_revagent.py::test_missing_value_stop_and_full_predicate PASSED [  1%]
+tests/commands/test_auggie_review_revagent.py::test_validation_precedes_env_check_and_is_depth_independent PASSED [  1%]
+tests/commands/test_auggie_review_revagent.py::test_error_handling_rows PASSED [  1%]
+tests/commands/test_auggie_review_revagent.py::test_warn_is_in_wave0_conditioned_and_audited PASSED [  1%]
+tests/commands/test_auggie_review_revagent.py::test_step5_passes_model_and_stays_deep_only PASSED [  1%]
+tests/commands/test_auggie_review_revagent.py::test_revagent_never_reaches_auggie PASSED [  1%]
+tests/commands/test_auggie_review_revagent.py::test_tool_coordination_names_only_the_reviewer_spawn PASSED [  1%]
+tests/commands/test_auggie_review_revagent.py::test_frontmatter_default_unchanged PASSED [  1%]
+tests/commands/test_auggie_review_revagent.py::test_audit_literals PASSED [  1%]
+tests/commands/test_graph_command.py::test_graph_command_frontmatter PASSED [  1%]
+tests/commands/test_graph_command.py::test_graph_command_invokes_protocol_skill PASSED [  1%]
+tests/commands/test_graph_command.py::test_graph_command_allowed_tools_exact PASSED [  1%]
+tests/commands/test_graph_command.py::test_graph_skill_allowed_tools_exact PASSED [  1%]
+tests/commands/test_graph_command.py::test_graph_init_only_in_command PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_init_user_typed_guard PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_nested_worktree_refusal PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_init_preflight_refuses_running_init PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_no_sync_or_explore PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_index_state_enum PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_next_action_enum[none] PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_next_action_enum[run_graph_init] PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_next_action_enum[run_graph_init_worktree_local] PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_next_action_enum[install_codegraph] PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_next_action_enum[enable_codegraph] PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_next_action_enum[status_only_branch] PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_next_action_enum[align_version] PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_next_action_enum[wait_for_sync] PASSED [  2%]
+tests/commands/test_graph_command.py::test_graph_next_action_enum[check_codegraph_error] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[schema_version] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[command] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[subcommand] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[status] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[contract_path] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[output_dir] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[checked_at] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[access] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[index_state] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[worktree_root] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[worktree_relation] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[cli_version] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[pin] PASSED [  3%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[pin_match] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[mcp_tools_listed] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[counts] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[pending] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[telemetry] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[telemetry_opt_out] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[kill_switch] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[next_action] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[degraded] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[init.requested] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[init.form] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[init.ran] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[init.exit_code] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_contract_fields_documented[init.refused_reason] PASSED [  4%]
+tests/commands/test_graph_command.py::test_graph_telemetry_opt_out_and_switch PASSED [  5%]
+tests/commands/test_graph_command.py::test_graph_guide_lookup_line[graph.md] PASSED [  5%]
+tests/commands/test_graph_command.py::test_graph_guide_lookup_line[SKILL.md] PASSED [  5%]
+tests/commands/test_graph_command.py::test_graph_no_skill_callers PASSED [  5%]
+tests/commands/test_help_command.py::test_help_has_no_static_command_table PASSED [  5%]
+tests/commands/test_help_command.py::test_help_lists_live_locations PASSED [  5%]
+tests/commands/test_help_command.py::test_help_prints_level_table_by_marker_and_points_to_recommend PASSED [  5%]
+tests/commands/test_help_command.py::test_help_points_to_guide_as_plain_path PASSED [  5%]
+tests/commands/test_help_command.py::test_help_size_and_shape PASSED     [  5%]
+tests/commands/test_help_command.py::test_help_names_builtins PASSED     [  5%]
+tests/commands/test_impact_command.py::test_impact_command_frontmatter PASSED [  5%]
+tests/commands/test_impact_command.py::test_impact_command_invokes_protocol_skill PASSED [  5%]
+tests/commands/test_impact_command.py::test_impact_skill_name PASSED     [  5%]
+tests/commands/test_impact_command.py::test_impact_allowed_tools_exact PASSED [  5%]
+tests/commands/test_impact_command.py::test_impact_no_wildcards PASSED   [  6%]
+tests/commands/test_impact_command.py::test_impact_no_mutating_verbs PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_no_explore PASSED     [  6%]
+tests/commands/test_impact_command.py::test_impact_node_file_mode_has_symbols_only PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_guide_lookup_line[impact.md] PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_guide_lookup_line[SKILL.md] PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_runtime_surface_dual_surface PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[schema_version] PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[command] PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[status] PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[caller] PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[output_dir] PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[report_path] PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[contract_path] PASSED [  6%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[input.mode] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[input.symbols] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[input.diff_base] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[input.changed_files] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[input.depth] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[input.limit] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[input.tests] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[input.test_depth] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[readiness] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[advisory] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[degraded] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[symbols[]] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[ambiguous[]] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[unmapped_files[]] PASSED [  7%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[dependents[]] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[dependents_omitted] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[call_sites] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[tests[]] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[selection_source] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_contract_fields_documented[errors[]] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_status_enum PASSED    [  8%]
+tests/commands/test_impact_command.py::test_impact_tokens_closed_vocabulary PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[codegraph absent-graph:absent] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[lookup tools unlisted-graph:unlisted] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[switched off-graph:disabled] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[not initialized-graph:not_initialized] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[foreign index-graph:foreign_index] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[stale-graph:stale] PASSED [  8%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[version mismatch-graph:version_mismatch] PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[truncated-graph:truncated] PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[parse failure-graph:parse_failed] PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[ambiguous name-graph:ambiguous] PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[empty result-graph:empty] PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[budget-limited rows-graph:unresolved] PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[bad flags-blocked] PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_failure_table_rows[output dir unwritable-failed] PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_md_sections_in_order PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_call_site_budget PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_advisory_rule PASSED  [  9%]
+tests/commands/test_impact_command.py::test_impact_status_only_cli_transport_before_grep_fallback PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_diff_default_compares_against_head PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_diff_mode_grep_fallback_lists_files_as_unmapped PASSED [  9%]
+tests/commands/test_impact_command.py::test_impact_call_site_confirmation_is_direct_callers_only PASSED [  9%]
+tests/commands/test_impact_command.py::test_name_patterns_are_dollar_safe[path0] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_name_patterns_are_dollar_safe[path1] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_name_patterns_are_dollar_safe[path2] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_example_uses_placeholders_only PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_callers_wired[sc-reflect-protocol/SKILL.md-sc-reflect-protocol] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_callers_wired[sc-implement-protocol/SKILL.md-sc-implement-protocol] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_callers_wired[sc-pr-submit-protocol/SKILL.md-sc-pr-submit-protocol] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_callers_wired[sc-pr-submit-protocol/refs/troubleshoot-dispatch.md-sc-pr-submit-protocol] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_callers_wired[sc-troubleshoot-protocol/SKILL.md-sc-troubleshoot-protocol] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_callers_wired[sc-auggie-review-protocol/SKILL.md-sc-auggie-review-protocol] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_callers_wired[sc-task-protocol/SKILL.md-sc-task-protocol] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_troubleshoot_wave1_does_not_call_impact PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill[sc-task-protocol/SKILL.md] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill[sc-pr-submit-protocol/SKILL.md] PASSED [ 10%]
+tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill[sc-troubleshoot-protocol/SKILL.md] PASSED [ 11%]
+tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill[sc-auggie-review-protocol/SKILL.md] PASSED [ 11%]
+tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill[sc-implement-protocol/SKILL.md] PASSED [ 11%]
+tests/commands/test_impact_command.py::test_impact_callers_may_invoke_skill[sc-reflect-protocol/SKILL.md] PASSED [ 11%]
+tests/commands/test_issue_command.py::test_frontmatter_fields PASSED     [ 11%]
+tests/commands/test_issue_command.py::test_options_table_lists_exactly_the_five_flags PASSED [ 11%]
+tests/commands/test_issue_command.py::test_options_table_allowed_values[--depth] PASSED [ 11%]
+tests/commands/test_issue_command.py::test_options_table_allowed_values[--mode] PASSED [ 11%]
+tests/commands/test_issue_command.py::test_options_table_allowed_values[--type] PASSED [ 11%]
+tests/commands/test_issue_command.py::test_option_defaults PASSED        [ 11%]
+tests/commands/test_issue_command.py::test_no_repo_dry_run_or_preview_flag PASSED [ 11%]
+tests/commands/test_issue_command.py::test_stop_rules_come_before_activation PASSED [ 11%]
+tests/commands/test_issue_command.py::test_activation_names_the_skill PASSED [ 11%]
+tests/commands/test_issue_command.py::test_no_source_tree_path PASSED    [ 11%]
+tests/commands/test_issue_command.py::test_rule_10_line_is_carried_verbatim[command] PASSED [ 12%]
+tests/commands/test_issue_command.py::test_rule_10_line_is_carried_verbatim[skill] PASSED [ 12%]
+tests/commands/test_research_command.py::test_research_command_no_param_duplication PASSED [ 12%]
+tests/commands/test_research_command.py::test_research_tiers_match_config PASSED [ 12%]
+tests/commands/test_routing_plugin_parity.py::test_sc_recommend_plugin_tree_mirrors_src_plus_guide PASSED [ 12%]
+tests/commands/test_routing_plugin_parity.py::test_readme_listed_command_mirrors_match_src[help] PASSED [ 12%]
+tests/commands/test_routing_plugin_parity.py::test_readme_listed_command_mirrors_match_src[recommend] PASSED [ 12%]
+tests/commands/test_routing_plugin_parity.py::test_readme_listed_command_mirrors_match_src[workflow] PASSED [ 12%]
+tests/commands/test_routing_plugin_parity.py::test_readme_listed_command_mirrors_match_src[implement] PASSED [ 12%]
+tests/commands/test_workflow_command.py::test_activation_handoff PASSED  [ 12%]
+tests/commands/test_workflow_command.py::test_command_has_no_execute_step PASSED [ 12%]
+tests/commands/test_workflow_command.py::test_skill_and_five_refs_exist PASSED [ 12%]
+tests/commands/test_workflow_command.py::test_mcp_servers_empty PASSED   [ 12%]
+tests/commands/test_workflow_command.py::test_plan_uses_template_00 PASSED [ 12%]
+tests/commands/test_workflow_command.py::test_workflow_template_is_bundled_and_installed PASSED [ 13%]
+tests/commands/test_workflow_command.py::test_plugin_mirror_matches_src PASSED [ 13%]
+tests/commands/test_workflow_command.py::test_all_creation_paths_target_to_do_not_workflow_root PASSED [ 13%]
+tests/commands/test_workflow_command.py::test_output_flag_is_retired_everywhere PASSED [ 13%]
+tests/commands/test_workflow_command.py::test_naming_and_collision_policy_is_specified PASSED [ 13%]
+tests/commands/test_workflow_command.py::test_early_stop_creates_no_package_and_failures_are_separated PASSED [ 13%]
+tests/commands/test_workflow_command.py::test_contract_and_plan_use_stable_portable_identity PASSED [ 13%]
+tests/commands/test_workflow_command.py::test_template_00_authoring_contract PASSED [ 13%]
+tests/commands/test_workflow_command.py::test_plugin_ships_managed_implement_protocol_and_helper PASSED [ 13%]
+tests/commands/test_workflow_command.py::test_digit_prefix_precedes_final_subject_truncation PASSED [ 13%]
+tests/commands/test_workflow_command.py::test_tasklist_referral_uses_positional_roadmap PASSED [ 13%]
+tests/commands/test_workflow_command.py::test_final_reflect_pre_precedes_contract_and_handoff PASSED [ 13%]
+tests/core/test_claude_md_routing_block.py::test_level_table_copy_matches_guide PASSED [ 13%]
+tests/core/test_claude_md_routing_block.py::test_routing_block_rule_and_pointer PASSED [ 13%]
+tests/core/test_claude_md_routing_block.py::test_imports_resolve_to_shipped_core_files PASSED [ 14%]
+tests/core/test_claude_md_routing_block.py::test_removed_sections_stay_removed PASSED [ 14%]
+tests/core/test_claude_md_routing_block.py::test_mcp_flag_column_is_advisory PASSED [ 14%]
+tests/core/test_claude_md_routing_block.py::test_always_loaded_policy_keeps_workflow_default_and_mdtm_boundary PASSED [ 14%]
+tests/core/test_codegraph_guide.py::test_guide_exists_and_is_short PASSED [ 14%]
+tests/core/test_codegraph_guide.py::test_guide_has_seven_sections PASSED [ 14%]
+tests/core/test_codegraph_guide.py::test_guide_names_seven_tools_and_closed_token_list PASSED [ 14%]
+tests/core/test_codegraph_guide.py::test_guide_fixed_lines_and_pin_parity PASSED [ 14%]
+tests/core/test_codegraph_guide.py::test_banned_names_only_in_never_section PASSED [ 14%]
+tests/core/test_codegraph_guide.py::test_guide_names_switches_and_status_guard PASSED [ 14%]
+tests/core/test_codegraph_guide.py::test_guide_holds_sentinel_and_no_source_path PASSED [ 14%]
+tests/core/test_codegraph_guide.py::test_not_initialized_message_names_graph_status PASSED [ 14%]
+tests/core/test_codegraph_guide.py::test_plugin_copy_is_byte_identical PASSED [ 14%]
+tests/core/test_codegraph_guide.py::test_core_claude_single_codegraph_row_names_guide PASSED [ 14%]
+tests/core/test_codegraph_guide.py::test_core_claude_marked_block_names_guide_once PASSED [ 15%]
+tests/core/test_codegraph_guide.py::test_refresh_tool_row_puts_codegraph_above_grep PASSED [ 15%]
+tests/core/test_codegraph_guide.py::test_core_and_modes_have_no_serena_or_explore PASSED [ 15%]
+tests/core/test_codegraph_guide.py::test_orchestration_matrix_has_codegraph_row PASSED [ 15%]
+tests/core/test_codegraph_guide.py::test_sentinel_only_in_the_guide PASSED [ 15%]
+tests/core/test_how_we_work_routing_table.py::test_each_marker_appears_exactly_once[<!-- level-table:v1 -->] PASSED [ 15%]
+tests/core/test_how_we_work_routing_table.py::test_each_marker_appears_exactly_once[<!-- /level-table -->] PASSED [ 15%]
+tests/core/test_how_we_work_routing_table.py::test_each_marker_appears_exactly_once[<!-- routing-table:v1 -->] PASSED [ 15%]
+tests/core/test_how_we_work_routing_table.py::test_each_marker_appears_exactly_once[<!-- /routing-table -->] PASSED [ 15%]
+tests/core/test_how_we_work_routing_table.py::test_markers_are_ordered PASSED [ 15%]
+tests/core/test_how_we_work_routing_table.py::test_level_table_block PASSED [ 15%]
+tests/core/test_how_we_work_routing_table.py::test_routing_header_and_separator PASSED [ 15%]
+tests/core/test_how_we_work_routing_table.py::test_every_row_has_eight_cells_and_no_pipe_in_a_cell PASSED [ 15%]
+tests/core/test_how_we_work_routing_table.py::test_ids_unique_kebab_and_stable PASSED [ 15%]
+tests/core/test_how_we_work_routing_table.py::test_level_and_changes_files_vocabulary PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_every_command_and_skill_token_exists PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_every_notes_flag_exists_in_its_command PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_notes_flag_check_still_rejects_unknown_slash_command_flags PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_notes_flag_check_ignores_flags_of_non_slash_commands PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_other_commands_membership_and_live_references PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_mandatory_flags_name_real_steps_and_real_flags PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_every_section_reference_is_a_heading PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_guide_is_ascii_except_the_ruling_example PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_guide_is_not_an_at_import_anywhere PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_named_mandatory_flags_are_on_their_steps[/sc:auggie-review---no-post-pr] PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_named_mandatory_flags_are_on_their_steps[/sc:reflect --mode post---no-promote] PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_direct_change_threshold_and_written_plan_requirement PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_ordinary_routes_plan_with_workflow_then_implement[simple-plan] PASSED [ 16%]
+tests/core/test_how_we_work_routing_table.py::test_ordinary_routes_plan_with_workflow_then_implement[feature-existing] PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_ordinary_routes_plan_with_workflow_then_implement[research-first] PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_mdtm_cannot_be_selected_by_a_proxy_alone[File count] PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_mdtm_cannot_be_selected_by_a_proxy_alone[multiple sessions] PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_mdtm_cannot_be_selected_by_a_proxy_alone[existing spec/PRD/TDD] PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_mdtm_cannot_be_selected_by_a_proxy_alone[risk] PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_mdtm_cannot_be_selected_by_a_proxy_alone[auditability] PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_mdtm_cannot_be_selected_by_a_proxy_alone[drift concerns] PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_mdtm_cannot_be_selected_by_a_proxy_alone[resume] PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_explicit_mdtm_creation_or_existing_task_execution_is_preserved PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_existing_approved_plan_and_explicit_executor_keep_their_identity PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_inspection_breadth_does_not_require_an_implementation_plan PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_contained_cleanup_exception_retains_safeguards_not_structural_migration PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_full_spec_ordinary_post_document_planning_is_workflow_first PASSED [ 17%]
+tests/core/test_how_we_work_routing_table.py::test_document_only_full_spec_stops_without_downstream_planning PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_explicit_roadmap_preserves_its_composer_and_phase_task_outputs PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_standard_planning_default_and_conditional_quick_are_consistent PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_bug_planning_and_brainstorm_follow_on_do_not_use_size_to_choose_mdtm PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_old_size_based_mdtm_policy_is_not_retained[fits in one or two sessions] PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_old_size_based_mdtm_policy_is_not_retained[level 4 for anything larger, longer, or riskier] PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_old_size_based_mdtm_policy_is_not_retained[Use the second pair for many files, multi-session work] PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_old_size_based_mdtm_policy_is_not_retained[Add `--handoff task` to go straight to a task file] PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_old_size_based_mdtm_policy_is_not_retained[For work that changes code, prefer `/task-builder`] PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S01-installed-inventory-targets0-inputs0-boundaries0] PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S02-focused-design-targets1-inputs1-boundaries1] PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S03-technical-design-document-targets2-inputs2-boundaries2] PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S04-cleanup-audit-only-targets3-inputs3-boundaries3] PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S05-contained-improve-targets4-inputs4-boundaries4] PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S06-auggie-review-only-targets5-inputs5-boundaries5] PASSED [ 18%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S07-localization-review-targets6-inputs6-boundaries6] PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S08-context-audit-targets7-inputs7-boundaries7] PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S09-cli-eval-create-targets8-inputs8-boundaries8] PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S10-cli-eval-run-targets9-inputs9-boundaries9] PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S11-cli-portification-spec-targets10-inputs10-boundaries10] PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S12-release-boundary-targets11-inputs11-boundaries11] PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S13-post-release-targets12-inputs12-boundaries12] PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S14-roadmap-artifacts-targets13-inputs13-boundaries13] PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S15-sprint-tasklist-bundle-targets14-inputs14-boundaries14] PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S16-roadmap-fidelity-targets15-inputs15-boundaries15] PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_static_targets_inputs_and_stops[S17-tier-validation-targets16-inputs16-boundaries16] PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_specialist_matching_and_unavailable_contract_are_shared_not_keyword_first PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_reports_keep_specialist_objective_instead_of_generic_competitor PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_requested_analysis_research_explain_modes_are_not_forced_defaults PASSED [ 19%]
+tests/core/test_how_we_work_routing_table.py::test_adversarial_generation_comparison_and_pipeline_remain_exclusive PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_cleanup_audit_and_improvement_have_separate_authority_boundaries PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_previews_documentation_and_suite_runs_disclose_actual_writes PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_diagnosis_reflection_and_review_preserve_remediation_coupling PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_reflect_optional_inputs_and_report_only_post_flags PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_pr_monitor_ceiling_is_conditional_and_each_branch_has_one_exact_value PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_pr_attachment_monitor_log_resume_and_silence_are_not_new_shipping PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_other_operations_preserve_requested_authority_and_owned_state PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_lifecycle_and_contract_gaps_do_not_certify_stale_or_mixed_interfaces PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_swarm_settings_help_retains_inputs_without_inferred_real_launch PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_explicit_cleanup_controls_and_pr_attachment_do_not_gain_default_actions PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_grouped_required_flags_still_use_exact_flag_tokens PASSED [ 20%]
+tests/core/test_how_we_work_routing_table.py::test_task_and_implement_verification_claims_are_not_universal_test_guarantees PASSED [ 20%]
+tests/core/test_research_config.py::test_each_depth_profile_names_concrete_params_and_tools PASSED [ 20%]
+tests/core/test_research_config.py::test_advanced_only_with_gating_language PASSED [ 21%]
+tests/core/test_research_config.py::test_discovery_caps_and_crawl_truncation_present PASSED [ 21%]
+tests/core/test_research_config.py::test_map_and_crawl_tool_ids_present PASSED [ 21%]
+tests/skills/test_brainstorm_protocol.py::test_brainstorm_no_tavily_param_duplication PASSED [ 21%]
+tests/skills/test_clickup_claim.py::test_skipped_without_token PASSED    [ 21%]
+tests/skills/test_clickup_claim.py::test_skipped_without_workspace PASSED [ 21%]
+tests/skills/test_clickup_claim.py::test_github_link_match_beats_title_match PASSED [ 21%]
+tests/skills/test_clickup_claim.py::test_github_link_in_custom_field_value_matches PASSED [ 21%]
+tests/skills/test_clickup_claim.py::test_github_link_with_longer_number_does_not_match PASSED [ 21%]
+tests/skills/test_clickup_claim.py::test_title_match_only_as_whole_token PASSED [ 21%]
+tests/skills/test_clickup_claim.py::test_title_match_assigns_with_title_rule PASSED [ 21%]
+tests/skills/test_clickup_claim.py::test_ambiguous_returns_candidates_and_makes_no_put PASSED [ 21%]
+tests/skills/test_clickup_claim.py::test_not_found PASSED                [ 21%]
+tests/skills/test_clickup_claim.py::test_already_assigned_makes_no_put PASSED [ 21%]
+tests/skills/test_clickup_claim.py::test_assign_sends_assignees_add_body PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_list_ids_narrow_the_search PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_auth_failure_gives_auth[401] PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_auth_failure_gives_auth[403] PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_429_is_retried_exactly_once_then_continues PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_429_twice_gives_rate_limited PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_other_http_error_gives_short_reason PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_page_cap_is_honoured_and_first_page_is_zero PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_empty_page_ends_the_search PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_invalid_max_pages_falls_back_to_default[0] PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_invalid_max_pages_falls_back_to_default[-1] PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_invalid_max_pages_falls_back_to_default[abc] PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_invalid_max_pages_falls_back_to_default[] PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_invalid_max_pages_falls_back_to_default[2.5] PASSED [ 22%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args0] PASSED [ 23%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args1] PASSED [ 23%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args2] PASSED [ 23%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args3] PASSED [ 23%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args4] PASSED [ 23%]
+tests/skills/test_clickup_claim.py::test_bad_arguments_exit_2[args5] PASSED [ 23%]
+tests/skills/test_clickup_claim.py::test_token_never_printed_on_any_outcome PASSED [ 23%]
+tests/skills/test_clickup_claim.py::test_script_imports_only_standard_library PASSED [ 23%]
+tests/skills/test_codegraph_adoption.py::test_validate_roadmap_step05_puts_codegraph_above_grep_and_never_skips PASSED [ 23%]
+tests/skills/test_codegraph_adoption.py::test_brainstorm_tier2_names_codegraph_files_and_search PASSED [ 23%]
+tests/skills/test_codegraph_adoption.py::test_task_protocol_standard_step2_names_codegraph_callers PASSED [ 23%]
+tests/skills/test_codegraph_adoption.py::test_tasklist_strict_row PASSED [ 23%]
+tests/skills/test_codegraph_adoption.py::test_cleanup_audit_and_auggie_review_name_codegraph[src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md] PASSED [ 23%]
+tests/skills/test_codegraph_adoption.py::test_cleanup_audit_and_auggie_review_name_codegraph[src/superclaude/skills/sc-auggie-review-protocol/SKILL.md] PASSED [ 23%]
+tests/skills/test_codegraph_adoption.py::test_cleanup_audit_and_auggie_review_name_codegraph[src/superclaude/commands/auggie-review.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_auggie_review_deep_pass_brief_passes_run_state PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_mcp_servers_gain_codegraph[src/superclaude/commands/validate-roadmap.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_mcp_servers_gain_codegraph[src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_mcp_servers_gain_codegraph[src/superclaude/commands/brainstorm.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_mcp_servers_gain_codegraph[plugins/superclaude/commands/brainstorm.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_mcp_servers_gain_codegraph[src/superclaude/skills/sc-brainstorm-protocol/SKILL.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_mcp_servers_gain_codegraph[src/superclaude/commands/cleanup-audit.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_mcp_servers_gain_codegraph[src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_mcp_servers_gain_codegraph[src/superclaude/commands/auggie-review.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_mcp_servers_gain_codegraph[src/superclaude/skills/sc-auggie-review-protocol/SKILL.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_task_command_mcp_servers_unchanged[src/superclaude/commands/task.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_task_command_mcp_servers_unchanged[plugins/superclaude/commands/task.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md] PASSED [ 24%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/commands/validate-roadmap.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/skills/sc-brainstorm-protocol/SKILL.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/commands/brainstorm.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[plugins/superclaude/commands/brainstorm.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/skills/sc-task-protocol/SKILL.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/commands/task.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[plugins/superclaude/commands/task.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/skills/sc-tasklist-protocol/SKILL.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/commands/cleanup-audit.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/skills/sc-auggie-review-protocol/SKILL.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_no_serena_tool_names[src/superclaude/commands/auggie-review.md] PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_reflect_calls_impact_protocol_with_its_caller PASSED [ 25%]
+tests/skills/test_codegraph_adoption.py::test_reflect_briefs_pass_codegraph_run_state PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_section6_heading PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_allowed_tools_hold_six_codegraph_names PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_step_1b3_logs_prod_and_test_counts_separately PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_files_have_no_removed_tool_names[src/superclaude/skills/sc-reflect-protocol/SKILL.md] PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_files_have_no_removed_tool_names[src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md] PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_files_have_no_removed_tool_names[src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md] PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_files_have_no_removed_tool_names[src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md] PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_files_have_no_removed_tool_names[src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md] PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_files_have_no_removed_tool_names[src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md] PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_files_have_no_removed_tool_names[src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml] PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_files_have_no_removed_tool_names[src/superclaude/commands/reflect.md] PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_files_have_no_removed_tool_names[plugins/superclaude/commands/reflect.md] PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_envelope_names_bash PASSED [ 26%]
+tests/skills/test_codegraph_adoption.py::test_reflect_commands_mcp_servers_gain_codegraph[src/superclaude/commands/reflect.md] PASSED [ 27%]
+tests/skills/test_codegraph_adoption.py::test_reflect_commands_mcp_servers_gain_codegraph[plugins/superclaude/commands/reflect.md] PASSED [ 27%]
+tests/skills/test_implement_adviser_family.py::test_ac18_two_families_and_gpt_is_t1 PASSED [ 27%]
+tests/skills/test_implement_adviser_family.py::test_ac19_spawn_path_pinned PASSED [ 27%]
+tests/skills/test_implement_adviser_family.py::test_ac19_no_gpt_reachable_gives_fallback_header_and_no_stop PASSED [ 27%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[x.log-1-3-0-OK x.log:1-3] PASSED [ 27%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[x.log-3-3-0-OK x.log:3-3] PASSED [ 27%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[x.log-1-4-0-CLAMPED x.log:1-4 -> 1-3] PASSED [ 27%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[x.log-4-4-1-FAIL x.log:4-4 (file has 3 lines)] PASSED [ 27%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[x.log-1-5-1-FAIL x.log:1-5 (file has 3 lines)] PASSED [ 27%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[x.log-0-3-1-FAIL x.log:0-3 (file has 3 lines)] PASSED [ 27%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[y.log-1-3-0-OK y.log:1-3] PASSED [ 27%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[y.log-1-4-1-FAIL y.log:1-4 (file has 3 lines)] PASSED [ 27%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[z.log-1-3-0-OK z.log:1-3] PASSED [ 27%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[z.log-1-4-0-CLAMPED z.log:1-4 -> 1-3] PASSED [ 27%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[z.log-1-5-1-FAIL z.log:1-5 (file has 3 lines)] PASSED [ 28%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[nope.log-1-1-1-FAIL nope.log (missing)] PASSED [ 28%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[a=b-1-3-0-OK a=b:1-3] PASSED [ 28%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[x.log-01-03-0-OK x.log:01-03] PASSED [ 28%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[x.log-1-18446744073709551619-1-FAIL x.log:1-18446744073709551619 (file has 3 lines)] PASSED [ 28%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[-x-1-4-1-FAIL -x:1-4 (file has 3 lines)] PASSED [ 28%]
+tests/skills/test_implement_retry_citation.py::test_cite_check[nul.log-1-3-1-FAIL nul.log:1-3 (file has 2 lines)] PASSED [ 28%]
+tests/skills/test_implement_retry_citation.py::test_mutant_without_the_clamp_branch PASSED [ 28%]
+tests/skills/test_implement_retry_citation.py::test_mutant_counting_with_wc PASSED [ 28%]
+tests/skills/test_implement_retry_citation.py::test_step_4_text_names_the_count_and_the_clamp PASSED [ 28%]
+tests/skills/test_implement_retry_citation.py::test_adviser_carries_the_phantom_line_rule PASSED [ 28%]
+tests/skills/test_implement_retry_revert.py::test_harness_env_holds_only_the_git_keys_it_sets PASSED [ 28%]
+tests/skills/test_implement_retry_revert.py::test_revert_refused_without_evidence[False] PASSED [ 28%]
+tests/skills/test_implement_retry_revert.py::test_revert_refused_without_evidence[empty] PASSED [ 28%]
+tests/skills/test_implement_retry_revert.py::test_revert_refuses_non_tree_start[commit] PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_revert_refuses_non_tree_start[nogit] PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_revert_refuses_non_tree_start[zero] PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_rid_encoding_for_dotted_ids[1.lock] PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_rid_encoding_for_dotted_ids[1..2] PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_checkpoint_ref_holds_tree_without_identity PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_restore_from_bare_tree PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_restore_symlink_and_type_swaps PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_post_revert_verify_reports_residue[keep.txt] PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_post_revert_verify_reports_residue[.dev/x] PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_post_revert_verify_reports_residue_for_failed_restore PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_foreign_dev_files_untouched_across_two_reverts PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_ledger_outside_run_dir_survives_revert PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_retries_and_troubleshoot_untouched PASSED [ 29%]
+tests/skills/test_implement_retry_revert.py::test_revert_from_subdirectory_covers_top_level PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_glob_and_colon_paths_reverted_literally PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_source_outside_repo_needs_no_exclude PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_rename_lists_both_sides PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_submodule_paths_excluded_and_listed PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_revert_idempotent_after_partial_attempt PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_sweep_ref_create_only_and_kept_after_complete PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_revert_binds_target_from_ledger PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_revert_targets_ledger_worktree_only PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_head_moved_halts_before_revert PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_failed_attempt_artifacts_moved PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_resumed_guard_refusal_moves_artifacts_back PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_finished_revert_refusal_keeps_artifacts PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_rerun_after_finished_revert_skips_artifact_move PASSED [ 30%]
+tests/skills/test_implement_retry_revert.py::test_real_dup_named_artifact_moves_back_under_its_own_name PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_collision_copy_keeps_its_name_in_a_collision_folder PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_symlink_artifact_moves_back_as_a_symlink PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_failed_moveback_is_named_on_stdout PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_symlinked_parent_never_moves_a_file_across_the_package PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_forward_move_never_writes_through_a_symlinked_save_folder PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_only_numeric_collision_folders_are_read_and_path_is_literal PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_done_file_keeps_every_saved_folder PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_nothing_is_lost_or_overwritten_on_moveback PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_repo_path_with_glob_chars_and_failglob PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_restored_parent_symlink_never_deletes_outside_file[-link] PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_restored_parent_symlink_never_deletes_outside_file[-a/link] PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_restored_parent_symlink_never_deletes_outside_file[deep/-link] PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_restored_parent_symlink_never_deletes_outside_file[deep/-a/link] PASSED [ 31%]
+tests/skills/test_implement_retry_revert.py::test_restored_dangling_or_file_symlink_parent_not_deleted_through[dangling] PASSED [ 32%]
+tests/skills/test_implement_retry_revert.py::test_restored_dangling_or_file_symlink_parent_not_deleted_through[file] PASSED [ 32%]
+tests/skills/test_implement_retry_revert.py::test_attempt_only_symlink_leaf_still_unlinked_in_worktree[-file] PASSED [ 32%]
+tests/skills/test_implement_retry_revert.py::test_attempt_only_symlink_leaf_still_unlinked_in_worktree[-dir] PASSED [ 32%]
+tests/skills/test_implement_retry_revert.py::test_attempt_only_symlink_leaf_still_unlinked_in_worktree[newdir/-file] PASSED [ 32%]
+tests/skills/test_implement_retry_revert.py::test_attempt_only_symlink_leaf_still_unlinked_in_worktree[newdir/-dir] PASSED [ 32%]
+tests/skills/test_implement_retry_revert.py::test_restored_parent_symlink_contained_in_linked_worktree PASSED [ 32%]
+tests/skills/test_implement_retry_revert.py::test_symlink_to_tracked_dir_does_not_destroy_the_target PASSED [ 32%]
+tests/skills/test_implement_retry_revert.py::test_restored_file_ancestor_reports_no_false_delete PASSED [ 32%]
+tests/skills/test_implement_severity_replay.py::test_r_a1_blocks_with_readback_dependent_constraint PASSED [ 32%]
+tests/skills/test_implement_severity_replay.py::test_r_a2_low_label_ignored_blocks_and_probe_before_locality_repairs PASSED [ 32%]
+tests/skills/test_implement_severity_replay.py::test_r_a3_late_blockers_after_a2_repair_take_adviser_route PASSED [ 32%]
+tests/skills/test_implement_severity_replay.py::test_r_a4_passes_with_notes PASSED [ 32%]
+tests/skills/test_implement_severity_replay.py::test_r_a5_parent_caps_inherited_harm_and_computes_compliant PASSED [ 32%]
+tests/skills/test_implement_severity_replay.py::test_t1_end_state_and_notes_chain PASSED [ 33%]
+tests/skills/test_implement_severity_replay.py::test_pv_r1_counts_blocking_families_only PASSED [ 33%]
+tests/skills/test_implement_severity_replay.py::test_pv_r1_all_severity_flip_changes_outcome PASSED [ 33%]
+tests/skills/test_implement_severity_replay.py::test_v3_f01_unmet_behind_non_blocking_completes PASSED [ 33%]
+tests/skills/test_implement_severity_replay.py::test_v3_f03_scope_blocker_never_compliant PASSED [ 33%]
+tests/skills/test_implement_severity_replay.py::test_v3_f02_inline_after_failing_review_reruns_as_subagent PASSED [ 33%]
+tests/skills/test_implement_severity_replay.py::test_ac09_addendum1_origin_fixture PASSED [ 33%]
+tests/skills/test_implement_severity_static.py::test_ac01_checklist_readback_and_vocabulary_mapping PASSED [ 33%]
+tests/skills/test_implement_severity_static.py::test_ac02_one_closed_reviewer_template_with_seven_slots PASSED [ 33%]
+tests/skills/test_implement_severity_static.py::test_ac02_no_finding_quota_phrase PASSED [ 33%]
+tests/skills/test_implement_severity_static.py::test_ac03_verdict_order_fed_by_blocking_findings_only PASSED [ 33%]
+tests/skills/test_implement_severity_static.py::test_ac03_retired_spec_sentences_absent PASSED [ 33%]
+tests/skills/test_implement_severity_static.py::test_ac03_label_rules PASSED [ 33%]
+tests/skills/test_implement_severity_static.py::test_ac03_scope_attachment_and_non_blocking_unmet_rules PASSED [ 33%]
+tests/skills/test_implement_severity_static.py::test_v1f05_reviewer_limits_and_parent_keys PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_v2f12_notes_append_on_failing_review_and_superseded_prefix PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_ac04_ledger_regexes_unchanged PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_ac04_archive_helper_regexes_unchanged PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_ac07_fixture_ledgers_parse PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_ac07_archive_suite_fixture_ledger_parses_and_archives PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_ac10_per_attempt_table_rows PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_ac11_allow_list_classes_are_closed PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_ac11_every_halt_stop_ruling_site_is_classified PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_ac11_minors_only_replay_writes_no_halt_and_no_ruling PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_family_probe_section_in_qa PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_skill_q5_names_family_probe PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_retry_repair_round_rules PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_p1_output_style_exempts_implement_severity_model PASSED [ 34%]
+tests/skills/test_implement_severity_static.py::test_p2_minors_never_drive_a_fix_pass_repair_or_review PASSED [ 35%]
+tests/skills/test_implement_severity_static.py::test_p3_severity_model_precedence_over_output_style PASSED [ 35%]
+tests/skills/test_implement_severity_static.py::test_p4_precedence_line_inside_closed_reviewer_template PASSED [ 35%]
+tests/skills/test_implement_severity_static.py::test_rec2a_verified_minor_rule_stops_late_promotion PASSED [ 35%]
+tests/skills/test_implement_severity_static.py::test_rec2_notes_line_carries_ac_and_set_aside_answers PASSED [ 35%]
+tests/skills/test_implement_severity_static.py::test_rec2b_line_drift_boundary_is_minor_not_false_claim PASSED [ 35%]
+tests/skills/test_implement_severity_static.py::test_rec2_closed_reviewer_template_unchanged PASSED [ 35%]
+tests/skills/test_issue_protocol.py::test_skill_frontmatter_and_size PASSED [ 35%]
+tests/skills/test_issue_protocol.py::test_every_named_path_exists_and_every_file_is_named PASSED [ 35%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[SKILL.md] PASSED [ 35%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[chains.md] PASSED [ 35%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[claim.md] PASSED [ 35%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[create.md] PASSED [ 35%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[labels.md] PASSED [ 35%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[tiers.md] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_all_five_refs_exist PASSED     [ 36%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[accuracy-check-comment-<!-- sc:issue:accuracy-check -->] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[claim-comment-<!-- sc:issue:claim -->] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[create-review-comment-<!-- sc:issue:create-review -->] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[issue-bug-complex-<!-- sc:issue:create template=issue-bug-complex -->] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[issue-bug-simple-<!-- sc:issue:create template=issue-bug-simple -->] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[issue-feature-complex-<!-- sc:issue:create template=issue-feature-complex -->] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[issue-feature-simple-<!-- sc:issue:create template=issue-feature-simple -->] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_marker_check_fails_when_marker_is_removed PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_issue_template_headings_in_order[issue-bug-complex-expected0] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_issue_template_headings_in_order[issue-bug-simple-expected1] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_issue_template_headings_in_order[issue-feature-complex-expected2] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_issue_template_headings_in_order[issue-feature-simple-expected3] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_issue_template_has_no_clickup_text[issue-bug-complex] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_issue_template_has_no_clickup_text[issue-bug-simple] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_issue_template_has_no_clickup_text[issue-feature-complex] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_issue_template_has_no_clickup_text[issue-feature-simple] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_every_chain_flag_exists_in_its_command PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_brainstorm_steps_have_no_handoff_and_pin_models PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[SKILL.md] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[chains.md] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[claim.md] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[create.md] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[labels.md] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[tiers.md] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t3.md] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t2.md] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t1.md] PASSED [ 37%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[SKILL.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[chains.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[claim.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[create.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[labels.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[tiers.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[clickup_claim.py] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[origin_repo.py] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[accuracy-check-comment.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[claim-comment.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[create-review-comment.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[description.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[draft-notes.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[flags-decision.md] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-bug-complex.md] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-bug-simple.md] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-feature-complex.md] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-feature-simple.md] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[next-steps.md] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[recommend-record.md] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[scout-report.md] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[summary.md] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-worker-t3.md] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-worker-t2.md] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-worker-t1.md] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_fork_safety_scan_fails_on_a_ref_without_repo PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_no_source_tree_path_in_skill_files PASSED [ 39%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude] PASSED [ 39%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude.git] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude/] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude.git/] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude.git] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude/] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude\n] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[https://gitlab.com/IronbellyOrg/IronClaude.git] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[git@bitbucket.org:IronbellyOrg/IronClaude.git] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[https://github.com/IronbellyOrg] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[/srv/git/IronClaude.git] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_exits_nonzero_with_e_no_origin PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_missing_origin_exits_nonzero_with_e_no_origin PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_missing_origin_with_other_remote_still_e_no_origin PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_only_origin_is_read_when_another_remote_exists PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_mode_prints_repo_and_number PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_mode_foreign_url_exits_with_distinct_code PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_mode_without_origin_reports_e_no_origin_first PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_bad_arguments_exit_2 PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[302-302] PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[#302-302] PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/ironbellyorg/ironclaude/issues/302-302] PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302/-302] PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302#issuecomment-9-302] PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302?x=1-302] PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[http://github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 41%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[www.github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://www.github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[git@github.com:IronbellyOrg/IronClaude/issues/302-302] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/octocat/IronClaude/issues/1] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/OtherRepo/issues/1] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/IronClaudeX/issues/1] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/IronClaud/issues/1] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrgX/IronClaude/issues/1] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://gitlab.com/IronbellyOrg/IronClaude/issues/1] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[github.com/octocat/Hello-World/issues/1] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[www.github.com/IronbellyOrg/IronClaudeX/issues/1] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[git@github.com:octocat/Hello-World.git] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[git@bitbucket.org:IronbellyOrg/IronClaude.git] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302/] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302#discussion_r1] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_foreign_repo_is_e_foreign_repo PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[Org302/Repo456-https://github.com/Org302/Repo456] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[Org302/Repo456-https://github.com/Org302/Repo456/] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[Org302/Repo456-https://github.com/Org302/Repo456/issues] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[IronbellyOrg/IronClaude302-https://github.com/IronbellyOrg/IronClaude302/tree/main] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_and_repo_do_not_replace_the_issue_segment PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[abc] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[0] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[-3] PASSED [ 44%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[302abc] PASSED [ 44%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[https://github.com/IronbellyOrg/IronClaude/issues/abc] PASSED [ 44%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[https://github.com/IronbellyOrg/IronClaude/issues/302/comments] PASSED [ 44%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[github.com/IronbellyOrg/IronClaude] PASSED [ 44%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[git@github.com:IronbellyOrg/IronClaude.git] PASSED [ 44%]
+tests/skills/test_issue_repo_resolution.py::test_script_imports_only_standard_library PASSED [ 44%]
+tests/skills/test_issue_worker_agents.py::test_worker_file_exists_with_pinned_picker_id[issue-worker-t1] PASSED [ 44%]
+tests/skills/test_issue_worker_agents.py::test_worker_file_exists_with_pinned_picker_id[issue-worker-t2] PASSED [ 44%]
+tests/skills/test_issue_worker_agents.py::test_worker_file_exists_with_pinned_picker_id[issue-worker-t3] PASSED [ 44%]
+tests/skills/test_issue_worker_agents.py::test_picker_tier_exists_in_ccsession_models[issue-worker-t1] PASSED [ 44%]
+tests/skills/test_issue_worker_agents.py::test_picker_tier_exists_in_ccsession_models[issue-worker-t2] PASSED [ 44%]
+tests/skills/test_issue_worker_agents.py::test_picker_tier_exists_in_ccsession_models[issue-worker-t3] PASSED [ 44%]
+tests/skills/test_issue_worker_agents.py::test_tools_exclude_edit[issue-worker-t1] PASSED [ 44%]
+tests/skills/test_issue_worker_agents.py::test_tools_exclude_edit[issue-worker-t2] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_tools_exclude_edit[issue-worker-t3] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_no_permission_mode[issue-worker-t1] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_no_permission_mode[issue-worker-t2] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_no_permission_mode[issue-worker-t3] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_body_states_github_git_and_write_rules[issue-worker-t1] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_body_states_github_git_and_write_rules[issue-worker-t2] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_body_states_github_git_and_write_rules[issue-worker-t3] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t1] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t2] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t3] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_no_source_tree_path_or_brace_placeholder[issue-worker-t1] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_no_source_tree_path_or_brace_placeholder[issue-worker-t2] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_no_source_tree_path_or_brace_placeholder[issue-worker-t3] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_scan_helper_flags_mentions_without_repo[Run `gh issue view 3 --repo <R> --json body`.-missing0] PASSED [ 45%]
+tests/skills/test_issue_worker_agents.py::test_scan_helper_flags_mentions_without_repo[Run `gh issue view 3 --json body`.-missing1] PASSED [ 46%]
+tests/skills/test_issue_worker_agents.py::test_scan_helper_flags_mentions_without_repo[never gh label create x-missing2] PASSED [ 46%]
+tests/skills/test_issue_worker_agents.py::test_scan_helper_flags_mentions_without_repo[```\ngh pr list --state merged\n```-missing3] PASSED [ 46%]
+tests/skills/test_issue_worker_agents.py::test_scan_helper_flags_mentions_without_repo[`gh api user -q .login`-missing4] PASSED [ 46%]
+tests/skills/test_primitive_dual_surface_lookup.py::test_adversarial_prerequisite_checks_accept_both_surfaces PASSED [ 46%]
+tests/skills/test_primitive_dual_surface_lookup.py::test_persona_check_accepts_both_surfaces PASSED [ 46%]
+tests/skills/test_primitive_dual_surface_lookup.py::test_rf_qa_lookup_is_project_first PASSED [ 46%]
+tests/skills/test_reflect_input_snapshot.py::test_skill_defines_pinned_exact_output_root_policy PASSED [ 46%]
+tests/skills/test_reflect_input_snapshot.py::test_input_resolution_carries_output_guard PASSED [ 46%]
+tests/skills/test_reflect_input_snapshot.py::test_managed_delegate_ref_points_at_reflect_policy_and_mirror_matches PASSED [ 46%]
+tests/skills/test_reflect_input_snapshot.py::test_own_writes_stable_initially_and_on_recompute PASSED [ 46%]
+tests/skills/test_reflect_input_snapshot.py::test_real_edits_still_detected[tasklist] PASSED [ 46%]
+tests/skills/test_reflect_input_snapshot.py::test_real_edits_still_detected[source] PASSED [ 46%]
+tests/skills/test_reflect_input_snapshot.py::test_real_edits_still_detected[log] PASSED [ 46%]
+tests/skills/test_reflect_input_snapshot.py::test_real_edits_still_detected[qa] PASSED [ 47%]
+tests/skills/test_reflect_input_snapshot.py::test_real_edits_still_detected[sibling] PASSED [ 47%]
+tests/skills/test_reflect_input_snapshot.py::test_real_edits_still_detected[delivery] PASSED [ 47%]
+tests/skills/test_reflect_input_snapshot.py::test_prefix_collision_sibling_not_excluded PASSED [ 47%]
+tests/skills/test_reflect_input_snapshot.py::test_overlap_and_escape_fail_closed PASSED [ 47%]
+tests/skills/test_reflect_input_snapshot.py::test_external_output_parent_traversal_is_rejected PASSED [ 47%]
+tests/skills/test_reflect_input_snapshot.py::test_recorded_move_maps_pinned_root_without_retargeting PASSED [ 47%]
+tests/skills/test_reflect_input_snapshot.py::test_external_explicit_input_changes_remain_visible PASSED [ 47%]
+tests/skills/test_repo_inventory_nongit.py::test_nongit_target_dot_counts_files PASSED [ 47%]
+tests/skills/test_repo_inventory_nongit.py::test_nongit_target_dot_still_excludes_hidden PASSED [ 47%]
+tests/skills/test_repo_inventory_nongit.py::test_nongit_target_absolute_unchanged PASSED [ 47%]
+tests/skills/test_repo_inventory_nongit.py::test_no_illegal_number_noise PASSED [ 47%]
+tests/skills/test_repo_inventory_nongit.py::test_empty_target_no_noise PASSED [ 47%]
+tests/skills/test_review_severity_rule.py::test_b_canonical_bullets_follow_binary_verdict_bullet PASSED [ 47%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[Report issues of any severity.] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[List gaps of any severity in the table.] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[A finding at any severity blocks the gate.] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[ALL findings regardless of severity must be resolved.] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[No severity level is exempt from fixing.] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[A 'minor issues still pass' allowance is PROHIBITED.] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[Minor issues must still be fixed before PASS.] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[Cosmetic gaps still must be fixed.] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[Zero tolerance: The batch must be perfect to pass] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[All findings must be resolved before the next phase.] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_fires_on_any_severity_wording[Send CRITICAL, IMPORTANT, and MINOR issues to gap-fill.] PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_matcher_ignores_the_new_rule_text PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_a_no_any_severity_wording_in_tracked_primitives PASSED [ 48%]
+tests/skills/test_review_severity_rule.py::test_c_s1_s3_copied_verbatim[src/superclaude/agents/rf-qa.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_s1_s3_copied_verbatim[src/superclaude/agents/rf-qa-qualitative.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_s1_s3_copied_verbatim[src/superclaude/templates/documents/agent_template_qa.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_s1_s3_copied_verbatim[src/superclaude/templates/documents/skill_template.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_s1_s3_copied_verbatim[src/superclaude/templates/workflow/01_mdtm_template_generic_task.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_s1_s3_copied_verbatim[src/superclaude/templates/workflow/02_mdtm_template_complex_task.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_s1_s3_copied_verbatim[src/superclaude/rules/prompts/automated_qa_workflow_qa_prompt.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_s1_s3_copied_verbatim[src/superclaude/rules/prompts/doc_code_analyst_qa_prompt.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_s1_s3_copied_verbatim[src/superclaude/rules/prompts/documentation_expert_qa_prompt.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_s1_s3_copied_verbatim[src/superclaude/rules/prompts/recruiting_expert_qa_prompt.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_no_inventory_labels_or_annotation[src/superclaude/agents/rf-qa.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_no_inventory_labels_or_annotation[src/superclaude/agents/rf-qa-qualitative.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_no_inventory_labels_or_annotation[src/superclaude/templates/documents/agent_template_qa.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_no_inventory_labels_or_annotation[src/superclaude/templates/documents/skill_template.md] PASSED [ 49%]
+tests/skills/test_review_severity_rule.py::test_c_no_inventory_labels_or_annotation[src/superclaude/templates/workflow/01_mdtm_template_generic_task.md] PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_c_no_inventory_labels_or_annotation[src/superclaude/templates/workflow/02_mdtm_template_complex_task.md] PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_c_no_inventory_labels_or_annotation[src/superclaude/rules/prompts/automated_qa_workflow_qa_prompt.md] PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_c_no_inventory_labels_or_annotation[src/superclaude/rules/prompts/doc_code_analyst_qa_prompt.md] PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_c_no_inventory_labels_or_annotation[src/superclaude/rules/prompts/documentation_expert_qa_prompt.md] PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_c_no_inventory_labels_or_annotation[src/superclaude/rules/prompts/recruiting_expert_qa_prompt.md] PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_d_canonical_cap_text_in_style PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_d_at_cap_clause_present_where_cap_rows_add_it PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_e_every_cap_edits_row_holds PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_j_every_sweep_edits_row_holds PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_ej_fixtures_are_byte_copies_of_the_plan_tables PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_f_regression_matcher_fires[Max 3 fix cycles] PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_f_regression_matcher_fires[phase-gate QA failing 3 fix cycles] PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_f_regression_matcher_fires[after 3 failed cycles] PASSED [ 50%]
+tests/skills/test_review_severity_rule.py::test_f_regression_matcher_fires[max-3-cycles] PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_f_no_old_cap_numbers_outside_implement_protocol PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_g_no_conditional_pass_kept[src/superclaude/templates/documents/skill_template.md] PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_g_no_conditional_pass_kept[src/superclaude/skills/prd/refs/agent-prompts.md] PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_g_no_conditional_pass_kept[src/superclaude/skills/tdd/refs/agent-prompts.md] PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_g_no_conditional_pass_kept[src/superclaude/skills/tech-reference/SKILL.md] PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_g_no_conditional_pass_kept[src/superclaude/skills/tech-research/SKILL.md] PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_g_no_conditional_pass_kept[src/superclaude/skills/operational-guide/SKILL.md] PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_g_readme_remediation_suffix_kept PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_h_implement_protocol_plugin_twins_byte_equal PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_i_sweep_matcher_fires[If findings exist, spawn ONE rf-qa agent] PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_i_sweep_matcher_fires[If verification finds new issues, repeat] PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_i_sweep_matcher_fires[FAIL: Issues found (list with specific fixes)] PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_i_sweep_matcher_fires[logged for human review] PASSED [ 51%]
+tests/skills/test_review_severity_rule.py::test_i_blocking_line_is_in_scope PASSED [ 52%]
+tests/skills/test_review_severity_rule.py::test_i_no_swept_wording_in_tracked_primitives PASSED [ 52%]
+tests/skills/test_review_severity_rule.py::test_k_unqualified_zero_tolerance_fires[Zero tolerance: The batch must be perfect to pass] PASSED [ 52%]
+tests/skills/test_review_severity_rule.py::test_k_unqualified_zero_tolerance_fires[You enforce a zero-tolerance policy for errors.] PASSED [ 52%]
+tests/skills/test_review_severity_rule.py::test_k_zero_tolerance_only_with_a_qualifier PASSED [ 52%]
+tests/skills/test_sc_recommend_routing_contract.py::test_step_0_comes_before_the_hot_path PASSED [ 52%]
+tests/skills/test_sc_recommend_routing_contract.py::test_guide_locations_are_listed_in_order PASSED [ 52%]
+tests/skills/test_sc_recommend_routing_contract.py::test_guide_not_found_line_is_shared_with_help PASSED [ 52%]
+tests/skills/test_sc_recommend_routing_contract.py::test_hard_limit_overrides_native_first PASSED [ 52%]
+tests/skills/test_sc_recommend_routing_contract.py::test_mandatory_flags_rule_is_present PASSED [ 52%]
+tests/skills/test_sc_recommend_routing_contract.py::test_builtins_allowed_in_r2_and_r4 PASSED [ 52%]
+tests/skills/test_sc_recommend_routing_contract.py::test_uv_cache_step_is_gated PASSED [ 52%]
+tests/skills/test_sc_recommend_routing_contract.py::test_match_uses_the_whole_objective_and_preserves_explicit_selection PASSED [ 52%]
+tests/skills/test_sc_recommend_routing_contract.py::test_ordered_output_resolves_branches_before_emitting_steps PASSED [ 52%]
+tests/skills/test_sc_recommend_routing_contract.py::test_interface_evidence_accepts_declarations_not_conflicting_examples PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_verification_follows_actual_activation_and_relevant_dependencies PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_retirement_checks_provenance_without_excluding_custom_commands PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_missing_requested_targets_stay_visible_while_irrelevant_ghosts_drop PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_live_and_no_guide_fallbacks_keep_workflow_first_policy PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_cache_hit_is_a_reverified_request_specific_hint PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_cold_worker_preserves_verification_and_implementation_boundaries PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_classifier_keys_do_not_force_ordinary_planning_into_mdtm PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_optional_cache_insertion_never_bypasses_parent_validation PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_tdd_followup_offers_workflow_and_task_only_for_existing_mdtm PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_recommend_command_summary_is_accurate_and_flags_unchanged PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_hook_reminder_matches_branches_and_stays_advisory PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_hook_is_fail_open_and_matches_only_recommend[payload0-True] PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_hook_is_fail_open_and_matches_only_recommend[payload1-True] PASSED [ 53%]
+tests/skills/test_sc_recommend_routing_contract.py::test_hook_is_fail_open_and_matches_only_recommend[payload2-True] PASSED [ 54%]
+tests/skills/test_sc_recommend_routing_contract.py::test_hook_is_fail_open_and_matches_only_recommend[payload3-False] PASSED [ 54%]
+tests/skills/test_sc_recommend_routing_contract.py::test_hook_is_fail_open_and_matches_only_recommend[payload4-False] PASSED [ 54%]
+tests/skills/test_sc_recommend_routing_contract.py::test_hook_is_fail_open_and_matches_only_recommend[not json sc-recommend-False] PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_rf_qa_checklist_count_extended PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_rf_qa_contains_tb_add_tag[TB-Add-1] PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_rf_qa_contains_tb_add_tag[TB-Add-3] PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_rf_qa_contains_tb_add_tag[TB-Add-4] PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_rf_qa_contains_tb_add_tag[TB-Add-5] PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_rf_qa_contains_tb_add_tag[TB-Add-6] PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_rf_qa_contains_tb_add_tag[TB-Add-7] PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_skill_mirrors_tb_add_tag[TB-Add-1] PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_skill_mirrors_tb_add_tag[TB-Add-3] PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_skill_mirrors_tb_add_tag[TB-Add-4] PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_skill_mirrors_tb_add_tag[TB-Add-5] PASSED [ 54%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_skill_mirrors_tb_add_tag[TB-Add-6] PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_skill_mirrors_tb_add_tag[TB-Add-7] PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_tb_add_2_removed_deliberately PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_tb_add_7_inactive_path_documented PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_source_check_traceability PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR06StructuralGateAdditions::test_skill_15item_validation_checklist_extended PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR01ExecutionContextHeader::test_skill_documents_execution_context_block PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR01ExecutionContextHeader::test_execution_context_uses_source_areas_not_paths PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR01ExecutionContextHeader::test_execution_context_required_and_degrades_gracefully PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR01ExecutionContextHeader::test_execution_context_scope_confinement_rule PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR01ExecutionContextHeader::test_output_schema_shows_execution_context_block PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR01ExecutionContextHeader::test_rf_qa_adds_tb_add_8 PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR01ExecutionContextHeader::test_tb_add_8_specifies_evidence_or_absence PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR01ExecutionContextHeader::test_skill_mirrors_tb_add_8 PASSED [ 55%]
+tests/skills/test_task_builder_merge.py::TestPR04GateResultsPassthrough::test_skill_documents_inherited_structural_verdict PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR04GateResultsPassthrough::test_skill_inv_002_reinjection_on_fix_cycles PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR04GateResultsPassthrough::test_skill_inv_010_dynamic_tb_add_enumeration PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR04GateResultsPassthrough::test_skill_anti_inflation_inv_019 PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR04GateResultsPassthrough::test_skill_passthrough_fallback_documented PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR04GateResultsPassthrough::test_rf_qa_qualitative_rule_11_references_passthrough PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR04GateResultsPassthrough::test_rf_qa_qualitative_anti_inflation_in_rule_11 PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR04GateResultsPassthrough::test_rf_qa_qualitative_output_has_reliance_audit_section PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Drift] PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Contradictions] PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Omissions] PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Weakened criteria] PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Invented content] PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_axes_are_overlay_not_replacement PASSED [ 56%]
+tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_drift_baseline_requirement PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_axis_annotation_required_in_items_reviewed PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_skill_references_5_axis_lens PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_invented_content_axis_is_evidence_bound PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_weakened_axis_anti_inflation PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_skill_documents_retry_monotonicity_protocol PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_skill_monotonicity_guard_strict_shrink PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_skill_regression_detection_precedence PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_skill_independent_counters_preserved PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_skill_inv_012_dnsp_composition PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_rf_task_builder_has_protocol PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_rf_qa_has_protocol_in_fix_cycle PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_skill_rule_7_references_protocol PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_skill_documents_dnsp_protocol PASSED [ 57%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_skill_dnsp_emission_contract_fields[severity: HIGH] PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_skill_dnsp_emission_contract_fields[source: "synthetic-dnsp"] PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_skill_dnsp_emission_contract_fields[affected_range] PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_skill_dnsp_emission_contract_fields[evidence] PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_skill_dnsp_emission_contract_fields[recommendation] PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_skill_all_agents_fail_guard PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_skill_dedup_key_specified PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_skill_applies_to_a8_a10_a105 PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_rf_analyst_partition_protocol_has_dnsp PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_rf_analyst_has_output_format_example PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_rf_qa_partition_protocol_has_dnsp PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_rf_qa_qualitative_partition_protocol_has_dnsp PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestPR03DnspSyntheticFinding::test_inv_012_composition_documented_across_agents PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestTasklistDnspMapsDM003::test_tasklist_p3_reuses_dm003_contract PASSED [ 58%]
+tests/skills/test_task_builder_merge.py::TestP1ExecutionContextNoSemanticCollision::test_p1_execution_context_contract_identical_across_surfaces PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_documented_subject_examples_follow_the_stated_algorithm[docs/PRD_User Auth.md-prdUserAuth] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_documented_subject_examples_follow_the_stated_algorithm[Add logout to the header and wire it to /logout-addLogoutToTheHe] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_documented_subject_examples_follow_the_stated_algorithm[!!!.md-plan] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_documented_subject_examples_follow_the_stated_algorithm[\xdcn\xefcode Caf\xe9.md-nCodeCaf] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_documented_subject_examples_follow_the_stated_algorithm[authLogin.md-authLogin] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_documented_subject_examples_follow_the_stated_algorithm[XMLParser.md-xmlParser] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_documented_subject_examples_follow_the_stated_algorithm[2fa login.md-plan2FaLogin] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_doc_examples_cover_cap_and_fallback PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_subject_edge_cases[authLogin-authLogin] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_subject_edge_cases[XMLParser-xmlParser] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_subject_edge_cases[snake_case_name-snakeCaseName] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_subject_edge_cases[kebab-case-name-kebabCaseName] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_subject_edge_cases[two words here-twoWordsHere] PASSED [ 59%]
+tests/skills/test_task_workspace_lifecycle.py::test_subject_edge_cases[!!!-plan] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_subject_edge_cases[-plan] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_subject_edge_cases[2fa login-plan2FaLogin] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_subject_edge_cases[123-plan123] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_subject_edge_cases[\xdcn\xefcode Caf\xe9-nCodeCaf] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_subject_truncates_to_16_and_always_matches_helper_regex PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_tasklist_filename_is_full_id_basename_including_suffix PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_generated_ids_are_accepted_by_the_archive_helper[] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_generated_ids_are_accepted_by_the_archive_helper[-2] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_generated_ids_are_accepted_by_the_archive_helper[-9] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_helper_rejects_non_workflow_or_unbounded_suffix_ids[TASK-WF-x-20261001-063000-1] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_helper_rejects_non_workflow_or_unbounded_suffix_ids[TASK-WF-x-20261001-063000-10] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_helper_rejects_non_workflow_or_unbounded_suffix_ids[TASK-WF-X-20261001-063000] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_helper_rejects_non_workflow_or_unbounded_suffix_ids[TASK-WF-auth-login-20261001-063000] PASSED [ 60%]
+tests/skills/test_task_workspace_lifecycle.py::test_helper_rejects_non_workflow_or_unbounded_suffix_ids[TASK-WF-1abc-20261001-063000] PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_helper_rejects_non_workflow_or_unbounded_suffix_ids[TASK-WF-abcdefghijklmnopq-20261001-063000] PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_helper_rejects_non_workflow_or_unbounded_suffix_ids[TASK-WF--20261001-063000] PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_helper_rejects_non_workflow_or_unbounded_suffix_ids[task-wf-x-20261001-063000] PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_helper_rejects_non_workflow_or_unbounded_suffix_ids[TASK-PRD-x-20261001-063000] PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_workflow_and_helper_agree_on_contract_and_schema PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_workflow_handoff_relocation_rule PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_managed_detection_requires_schema_slug_contract_and_checkout_location PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_legacy_behavior_is_preserved PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_managed_ledger_artifacts_and_pins_are_stable PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_managed_final_and_archive_gate_rules PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_managed_final_judges_end_state_not_ledger_line_numbers PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_protocol_prose_has_no_cross_file_line_pointers PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_stale_to_do_path_is_resolved_before_missing_file_check PASSED [ 61%]
+tests/skills/test_task_workspace_lifecycle.py::test_managed_location_resolution_order PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_helper_invocation_uses_skill_base_directory_and_uv_not_repo_path PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_enforcement_map_separates_protocol_from_executable PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_command_surface_documents_managed_packages PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_session_confirmation_contract_and_documented_ruling PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_managed_ledger_extension_examples_parse_with_the_shipped_helper PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_machine_schema_has_no_inline_comments_and_is_helper_readable PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_ownerless_marker_recovery_is_documented_narrowly PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_ledger_retry_halt_examples_parse_with_helper PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_corrupt_check_lists_retry_and_halt PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_resume_table_row_order_and_text PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_row_x_runs_block_as_recheck PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_retry_ref_rules_text PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_retry_ref_and_reason_lists PASSED [ 62%]
+tests/skills/test_task_workspace_lifecycle.py::test_halt_span_negative_fixtures_fail[`halt reason=budget`] PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_halt_span_negative_fixtures_fail[`halt review=2 reason=budget|batch`] PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_halt_span_negative_fixtures_fail[`halt review=5 reason=batch`] PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_halt_span_negative_fixtures_fail[`halt review=6 reason=budget`] PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_halt_span_negative_fixtures_fail[```\nT1: halt review=2 reason=Bad Reason\n```] PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_halt_span_negative_fixtures_fail[`halt review=<k> reason=<r>` with r = `bogus`] PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_halt_span_positive_fixtures_pass[`halt review=2 reason=budget`] PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_halt_span_positive_fixtures_pass[`halt review=<k> reason=<r>` with r = `dispute`] PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_halt_span_positive_fixtures_pass[`halt review=<k> reason=<r>`, where r is `no-snapshot` or `head-moved` and k] PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_halt_span_positive_fixtures_pass[```\nT1: halt review=4 reason=no-runner-up\n```] PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_retry_ref_revert_block_present PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_stop_table_lists_e_resume_needed PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_parallel_rules_identical_in_skill_and_retry_ref PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_touched_file_rule_unchanged PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_skill_retry_wiring_text PASSED [ 63%]
+tests/skills/test_task_workspace_lifecycle.py::test_reviewer_rules_text PASSED [ 64%]
+tests/skills/test_task_workspace_lifecycle.py::test_revert_delete_is_guarded_against_symlinked_ancestors PASSED [ 64%]
+tests/skills/test_task_workspace_lifecycle.py::test_adviser_is_bundled_with_the_plugin_and_selected_by_available_type PASSED [ 64%]
+tests/skills/test_task_workspace_smoke.py::test_plugin_commands_match_canonical PASSED [ 64%]
+tests/skills/test_task_workspace_smoke.py::test_installer_ships_scripts_and_documented_invocation_runs PASSED [ 64%]
+tests/skills/test_task_workspace_smoke.py::test_positive_lifecycle_archives_with_valid_links PASSED [ 64%]
+tests/skills/test_task_workspace_smoke.py::test_negative_failed_final_stays_in_to_do PASSED [ 64%]
+tests/skills/test_tier2_tavily_consistency.py::test_tier2_tool_id_parity PASSED [ 64%]
+tests/skills/test_tier2_tavily_consistency.py::test_brainstorm_no_map_crawl PASSED [ 64%]
+tests/skills/test_tier2_tavily_consistency.py::test_rate_cap_intact PASSED [ 64%]
+tests/skills/test_tier2_tavily_consistency.py::test_fail_open_intact PASSED [ 64%]
+tests/skills/test_tier2_tavily_consistency.py::test_troubleshoot_search_depth_advanced PASSED [ 64%]
+tests/skills/test_workflow_archive.py::test_valid_package_moves_intact_without_marker PASSED [ 64%]
+tests/skills/test_workflow_archive.py::test_existing_destination_is_never_overwritten[file] PASSED [ 64%]
+tests/skills/test_workflow_archive.py::test_existing_destination_is_never_overwritten[empty] PASSED [ 65%]
+tests/skills/test_workflow_archive.py::test_existing_destination_is_never_overwritten[nonempty] PASSED [ 65%]
+tests/skills/test_workflow_archive.py::test_existing_destination_is_never_overwritten[dangling] PASSED [ 65%]
+tests/skills/test_workflow_archive.py::test_destination_created_just_before_syscall_is_preserved PASSED [ 65%]
+tests/skills/test_workflow_archive.py::test_kernel_noreplace_rejects_empty_dir_and_symlink PASSED [ 65%]
+tests/skills/test_workflow_archive.py::test_stale_plan_pin PASSED        [ 65%]
+tests/skills/test_workflow_archive.py::test_mismatched_or_legacy_plan_filename_is_rejected PASSED [ 65%]
+tests/skills/test_workflow_archive.py::test_stale_source_pin PASSED      [ 65%]
+tests/skills/test_workflow_archive.py::test_pin_after_first_start_rejected PASSED [ 65%]
+tests/skills/test_workflow_archive.py::test_missing_final PASSED         [ 65%]
+tests/skills/test_workflow_archive.py::test_skipped_issues_or_unbound_final[FINAL: skipped evidence=none] PASSED [ 65%]
+tests/skills/test_workflow_archive.py::test_skipped_issues_or_unbound_final[FINAL: issues evidence=a.py:1 state={s}] PASSED [ 65%]
+tests/skills/test_workflow_archive.py::test_skipped_issues_or_unbound_final[FINAL: pass evidence=src/a.py:1] PASSED [ 65%]
+tests/skills/test_workflow_archive.py::test_final_before_later_record_is_stale PASSED [ 65%]
+tests/skills/test_workflow_archive.py::test_delivery_change_after_final_invalidates_but_unrelated_does_not PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_unrelated_change_keeps_final_valid PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_each_attempt_needs_fresh_final PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_pending_task PASSED          [ 66%]
+tests/skills/test_workflow_archive.py::test_blocked_task PASSED          [ 66%]
+tests/skills/test_workflow_archive.py::test_noncompliant_without_task_ruling PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_legacy_task_ruling_needs_no_duplicate_archive_approval[None] PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_legacy_task_ruling_needs_no_duplicate_archive_approval[waive T2] PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_legacy_task_ruling_needs_no_duplicate_archive_approval[waive T20 and T1] PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_named_operator_archive_ruling_waives_task_not_final PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_session_acceptance_archives_without_rewriting_history_or_second_approval PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_confirmation_for_another_task_does_not_authorize_completion PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_reopened_task_requires_new_scoped_acceptance[False] PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_reopened_task_requires_new_scoped_acceptance[True] PASSED [ 66%]
+tests/skills/test_workflow_archive.py::test_new_start_requires_new_completion_and_acceptance[none] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_new_start_requires_new_completion_and_acceptance[ruling] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_new_start_requires_new_completion_and_acceptance[complete] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_new_start_requires_new_completion_and_acceptance[renewed] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_new_start_cannot_reuse_compliant_completion PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_acceptance_cannot_cover_changed_verdict_fields[verdict=missing-verdict=extra] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_acceptance_cannot_cover_changed_verdict_fields[ac=T2.AC1-ac=T2.AC2] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_acceptance_cannot_cover_changed_verdict_fields[evidence=src/a.py:1-evidence=src/a.py:2] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_acceptance_cannot_cover_changed_verdict_fields[test:skip-test:fail] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_acceptance_cannot_cover_changed_verdict_fields[files=src/a.py-files=./artifacts/evidence.txt] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_scoped_acceptance_does_not_waive_final_or_immutable_inputs[missing-final] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_scoped_acceptance_does_not_waive_final_or_immutable_inputs[issues] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_scoped_acceptance_does_not_waive_final_or_immutable_inputs[stale-final] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_scoped_acceptance_does_not_waive_final_or_immutable_inputs[delivery] PASSED [ 67%]
+tests/skills/test_workflow_archive.py::test_scoped_acceptance_does_not_waive_final_or_immutable_inputs[plan] PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_scoped_acceptance_does_not_waive_final_or_immutable_inputs[source] PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_malformed_ledger[<lambda>0] PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_malformed_ledger[<lambda>1] PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_malformed_ledger[<lambda>2] PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_malformed_ledger[<lambda>3] PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_invalid_package_contract[<lambda>0] PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_invalid_package_contract[<lambda>1] PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_invalid_package_contract[<lambda>2] PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_existing_marker_is_never_reclaimed PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_source_symlink_escape PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_parent_symlink_escape PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_not_under_checkout_or_wrong_name PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_unsupported_primitive_fails_closed_without_fallback[None] PASSED [ 68%]
+tests/skills/test_workflow_archive.py::test_unsupported_primitive_fails_closed_without_fallback[38] PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_unsupported_primitive_fails_closed_without_fallback[22] PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_unsupported_primitive_fails_closed_without_fallback[18] PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_non_linux_platform_fails_closed PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_interrupt_after_move_keeps_marker_until_operator_clears PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_clear_marker_never_touches_conflicting_locations PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_empty_or_unproven_done_dir_is_not_already_archived PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_archived_dir_with_tampered_plan_or_no_final_is_rejected PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_already_archived_survives_later_delivery_edits PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_oserror_before_move_is_reported_and_cleaned PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_oserror_creating_marker_is_reported PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_cli_reports_oserror_without_traceback PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_cli_real_process_archive_and_error_exit PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_main_empty_clear_marker_errors_and_never_archives[] PASSED [ 69%]
+tests/skills/test_workflow_archive.py::test_main_empty_clear_marker_errors_and_never_archives[  ] PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_cli_process_empty_clear_marker_leaves_valid_package PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_direct_empty_token_cannot_remove_ownerless_or_owned_marker PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_recovery_rejects_symlink_marker_or_owner[False] PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_recovery_rejects_symlink_marker_or_owner[True] PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_ambiguous_relative_delivery_is_rejected[./src/a.py] PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_ambiguous_relative_delivery_is_rejected[./artifacts/../src/a.py] PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_directory_digest_tracks_nested_symlink_targets[file] PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_directory_digest_tracks_nested_symlink_targets[directory] PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_directory_digest_tracks_nested_symlink_targets[dangling] PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_delivery_executable_mode_change_invalidates_final[False] PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_delivery_executable_mode_change_invalidates_final[True] PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_directory_traversal_error_cannot_produce_final_state PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex[open-3] PASSED [ 70%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex[open-4] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex[open-5] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex[revert-3] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex[revert-4] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex[revert-5] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex[review-3] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex[review-4] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex[review-5] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_accepts_every_rung_name[T3_Model01] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_accepts_every_rung_name[T2_Model02] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_accepts_every_rung_name[T1_Model02] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_accepts_every_rung_name[T1_Model01] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_accepts_every_rung_name[haiku] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_accepts_every_rung_name[sonnet] PASSED [ 71%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_accepts_every_rung_name[opus] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_accepts_every_rung_name[unknown] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_rejects[T1: retry n=2 step=review] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_rejects[T1: retry n=6 step=review] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_rejects[T1: retry n=3 step=open checkpoint=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa tier=opus] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_rejects[T1: retry n=3 step=open checkpoint=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa tier=] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_rejects[T1: retry n=3 step=open checkpoint=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa tier=bad-tier] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_rejects[T1: retry n=3 step=open checkpoint=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa tier=T2.Model] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_rejects[T1: retry n=3 step=revert supersedes=none] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_rejects[T1: retry n=3 step=revert brief=./artifacts/retries/T1_brief-3.md] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_rejects[T1: retry n=3 step=revert brief=./b.md supersedes=T1_brief-5.md] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_rejects[T1: retry n=3 step=revert brief=./b.md supersedes=T1_brief-2.md] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_record_regex_rejects[T1: retry n=3 step=other] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence[T1: retry n=3 step=revert brief=./artifacts/retries/T1_brief-3.md supersedes=none-T1_brief-3.md] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence[T1: retry n=4 step=revert brief=./artifacts/retries/T1_brief-4.md supersedes=T1_brief-3.md-T1_brief-4.md] PASSED [ 72%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence[T1: retry n=5 step=revert brief=./artifacts/retries/T1_brief-5.md supersedes=T1_brief-4.md-T1_brief-5.md] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence_legacy_root PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence_rejected[T1: retry n=4 step=revert brief=./artifacts/retries/T1_brief-4.md supersedes=none-T1_brief-4.md] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence_rejected[T1: retry n=5 step=revert brief=./artifacts/retries/T1_brief-5.md supersedes=T1_brief-3.md-T1_brief-5.md] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence_rejected[T1: retry n=3 step=revert brief=./artifacts/retries/T1_brief-3.md supersedes=T1_brief-4.md-T1_brief-3.md] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence_rejected[T1: retry n=3 step=revert brief=./artifacts/retries/T1_brief-4.md supersedes=none-T1_brief-4.md] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence_rejected[T1: retry n=3 step=revert brief=./artifacts/retries/T2_brief-3.md supersedes=none-T2_brief-3.md] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence_rejected[T1: retry n=3 step=revert brief=./artifacts/../artifacts/retries/T1_brief-3.md supersedes=none-T1_brief-3.md] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence_rejected[T1: retry n=3 step=revert brief=.dev/implement/../retries/T1_brief-3.md supersedes=none-None] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence_rejected[T1: retry n=3 step=revert brief=artifacts/retries/T1_brief-3.md supersedes=none-T1_brief-3.md] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_retry_brief_chain_and_existence_rejected[T1: retry n=3 step=revert brief=./artifacts/retries/T1_brief-3.md supersedes=none-None] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex_review_range[2] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex_review_range[3] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex_review_range[4] PASSED [ 73%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex_review_range[5] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex_rejects_review_out_of_range[1] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex_rejects_review_out_of_range[6] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex_rejects_review_out_of_range[10] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex[T1: halt review=6 reason=batch] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex[T1: halt reason=no-evidence] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex[T1: halt review=2 reason=Bad Reason] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex[T1: halt review=2 reason=Bad] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex[T1: halt review=2 reason=] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_halt_record_regex[T1: halt review=2 reason=-x] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_retry_or_halt_for_unknown_task_rejected[T9: retry n=3 step=review] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_retry_or_halt_for_unknown_task_rejected[T9: halt review=2 reason=budget] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_retry_or_halt_for_unknown_task_rejected[T9: retry n=3 step=open checkpoint=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa tier=unknown] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_retry_or_halt_for_unknown_task_rejected[T9: retry n=3 step=revert brief=./artifacts/retries/T9_brief-3.md supersedes=none] PASSED [ 74%]
+tests/skills/test_workflow_archive.py::test_full_ladder_managed_ledger_archives PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_plugin_helper_copy_is_byte_identical PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_halt_examples_block_equals_reason_table PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=5 reason=ladder-end] PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=no-snapshot] PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=3 reason=no-snapshot] PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=no-snapshot] PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=batch] PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=head-moved] PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=3 reason=head-moved] PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=head-moved] PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=budget] PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=advice-rejected] PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=3 reason=advice-rejected] PASSED [ 75%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=dispute] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=3 reason=dispute] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=no-runner-up] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=brief-invalid] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=no-evidence] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=3 reason=no-evidence] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=no-evidence] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=operator-review] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=3 reason=operator-review] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=operator-review] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=5 reason=operator-review] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_malformed_halt_reason_lines_are_rejected[T1: halt reason=no-evidence] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_malformed_halt_reason_lines_are_rejected[T1: halt review=6 reason=batch] PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_issues_then_shifted_final_archives_then_already_archived PASSED [ 76%]
+tests/skills/test_workflow_archive.py::test_symlinked_retries_directory_is_rejected_before_any_move[True] PASSED [ 77%]
+tests/skills/test_workflow_archive.py::test_symlinked_retries_directory_is_rejected_before_any_move[False] PASSED [ 77%]
+tests/skills/test_workflow_archive.py::test_symlinked_brief_file_is_rejected PASSED [ 77%]
+tests/skills/test_workflow_archive.py::test_verdict_regex_matches_notes_example_line_with_exact_files PASSED [ 77%]
+tests/skills/test_workflow_archive.py::test_field_after_files_is_swallowed_into_files PASSED [ 77%]
+tests/skills/test_workflow_archive.py::test_compliant_complete_with_notes_token_keeps_print_state_files PASSED [ 77%]
+tests/recommend/test_best_model.py::TestBestModelTiers::test_quality_picks_highest_pass_rate_tiebreak_tokens PASSED [ 77%]
+tests/recommend/test_best_model.py::TestBestModelTiers::test_speed_respects_70pct_floor PASSED [ 77%]
+tests/recommend/test_best_model.py::TestBestModelTiers::test_cost_respects_70pct_floor PASSED [ 77%]
+tests/recommend/test_best_model.py::TestBestModelTiers::test_speed_cost_floor_none_qualify_suppresses PASSED [ 77%]
+tests/recommend/test_best_model.py::TestBestModelTiers::test_balanced_weighted_sum_picks_expected PASSED [ 77%]
+tests/recommend/test_best_model.py::TestBestModelTiers::test_balanced_is_default_tier PASSED [ 77%]
+tests/recommend/test_best_model.py::TestBestModelTiers::test_confidence_below_half_suppresses_hint PASSED [ 77%]
+tests/recommend/test_best_model.py::TestBestModelTiers::test_based_on_recorded PASSED [ 77%]
+tests/recommend/test_cache.py::TestLookupCachePersistence::test_save_and_reload PASSED [ 78%]
+tests/recommend/test_cache.py::TestLookupCachePersistence::test_surface_hash_invalidation_resets_rows PASSED [ 78%]
+tests/recommend/test_cache.py::TestLookupCachePersistence::test_source_hash_full_digest PASSED [ 78%]
+tests/recommend/test_cache.py::TestLookupCachePersistence::test_surface_hash_is_full_digest PASSED [ 78%]
+tests/recommend/test_cache.py::TestLookupCacheRowOps::test_get_row_returns_match_or_none PASSED [ 78%]
+tests/recommend/test_cache.py::TestLookupCacheRowOps::test_upsert_replaces_existing_key PASSED [ 78%]
+tests/recommend/test_cache.py::TestLookupCacheRowOps::test_upsert_appends_new_key PASSED [ 78%]
+tests/recommend/test_cache.py::TestLookupCacheAtomicWrite::test_atomic_write_no_partial_on_crash PASSED [ 78%]
+tests/recommend/test_cache.py::test_surface_hash_changes_when_guide_changes PASSED [ 78%]
+tests/recommend/test_cache.py::test_surface_hash_stable_when_guide_unchanged PASSED [ 78%]
+tests/recommend/test_cache.py::test_surface_hash_guide_path_overrides_default PASSED [ 78%]
+tests/recommend/test_cache.py::test_surface_hash_without_guide_is_full_digest PASSED [ 78%]
+tests/recommend/test_cache.py::test_surface_hash_changes_when_an_installed_command_is_added PASSED [ 78%]
+tests/recommend/test_cache.py::test_surface_hash_ignores_installed_roots_when_given_none_to_scan PASSED [ 78%]
+tests/recommend/test_cache.py::test_surface_hash_changes_when_a_nested_project_command_is_added PASSED [ 79%]
+tests/recommend/test_cli_registration.py::test_recommend_group_registered PASSED [ 79%]
+tests/recommend/test_cli_registration.py::test_recommend_help_lists_subcommands PASSED [ 79%]
+tests/recommend/test_cli_registration.py::test_recommend_eval_run_exposes_mode_choice PASSED [ 79%]
+tests/recommend/test_dispatch.py::TestDispatchOutcomes::test_hit PASSED  [ 79%]
+tests/recommend/test_dispatch.py::TestDispatchOutcomes::test_native_likely PASSED [ 79%]
+tests/recommend/test_dispatch.py::TestDispatchOutcomes::test_miss_no_key_unknown PASSED [ 79%]
+tests/recommend/test_dispatch.py::TestDispatchOutcomes::test_miss_low_confidence PASSED [ 79%]
+tests/recommend/test_dispatch.py::TestDispatchOutcomes::test_miss_validation_stale_on_hash_drift PASSED [ 79%]
+tests/recommend/test_dispatch.py::TestDispatchOutcomes::test_miss_budget_exceeded PASSED [ 79%]
+tests/recommend/test_dispatch.py::TestColdInsertWarmsToHit::test_cache_put_recomputes_source_hash_then_dispatch_hits PASSED [ 79%]
+tests/recommend/test_dispatch.py::test_semantic_cache_collisions_require_consumer_guards[T56-reference-only-change] PASSED [ 79%]
+tests/recommend/test_dispatch.py::test_semantic_cache_collisions_require_consumer_guards[T55-same-key-new-input-path] PASSED [ 79%]
+tests/recommend/test_dispatch.py::test_semantic_cache_collisions_require_consumer_guards[T52-comparison-is-not-adherence-audit] PASSED [ 79%]
+tests/recommend/test_dispatch.py::test_semantic_cache_collisions_require_consumer_guards[T52-comparison-is-not-local-PR-review] PASSED [ 80%]
+tests/recommend/test_dispatch.py::test_semantic_cache_collisions_require_consumer_guards[T53-PRD-authoring-is-not-TDD] PASSED [ 80%]
+tests/recommend/test_dispatch.py::test_semantic_cache_collisions_require_consumer_guards[T53-PRD-authoring-is-not-existing-spec-critique] PASSED [ 80%]
+tests/recommend/test_dispatch.py::test_semantic_cache_collisions_require_consumer_guards[T54-MDTM-is-not-Sprint-artifacts] PASSED [ 80%]
+tests/recommend/test_dispatch.py::test_semantic_cache_collisions_require_consumer_guards[T48-hash-valid-retired-candidate] PASSED [ 80%]
+tests/recommend/test_dispatch.py::test_collision_case_clauses_map_one_to_one PASSED [ 80%]
+tests/recommend/test_eval_pipeline.py::TestGrader::test_five_assertion_types PASSED [ 80%]
+tests/recommend/test_eval_pipeline.py::TestGrader::test_grade_text_pass_rate PASSED [ 80%]
+tests/recommend/test_eval_pipeline.py::TestAggregate::test_mode_matrix_panels PASSED [ 80%]
+tests/recommend/test_eval_pipeline.py::TestAggregate::test_aggregate_by_model PASSED [ 80%]
+tests/recommend/test_eval_pipeline.py::TestFinalizeRoundTrip::test_finalize_writes_results_and_patches_row PASSED [ 80%]
+tests/recommend/test_plugin_eval.py::TestRunPreconditions::test_hard_block_raises PASSED [ 80%]
+tests/recommend/test_plugin_eval.py::TestRunPreconditions::test_warn_and_skip_do_not_raise[warn] PASSED [ 80%]
+tests/recommend/test_plugin_eval.py::TestRunPreconditions::test_warn_and_skip_do_not_raise[skip] PASSED [ 80%]
+tests/recommend/test_plugin_eval.py::TestRunPreconditions::test_satisfied_precondition_returns_empty PASSED [ 81%]
+tests/recommend/test_plugin_eval.py::TestEvaluateAdoption::test_pass_rate_gain_is_positive PASSED [ 81%]
+tests/recommend/test_plugin_eval.py::TestEvaluateAdoption::test_token_drop_is_positive PASSED [ 81%]
+tests/recommend/test_plugin_eval.py::TestEvaluateAdoption::test_pass_rate_regression_is_negative_even_with_token_drop PASSED [ 81%]
+tests/recommend/test_plugin_eval.py::TestPatchPluginRow::test_patch_round_trip PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_fixture_schema_and_completeness PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_every_mapped_test_function_exists PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S01] PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S02] PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S03] PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S04] PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S05] PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S06] PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S07] PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S08] PASSED [ 81%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S09] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S10] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S11] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S12] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S13] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S14] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S15] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S16] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S17] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S18] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S19] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S20] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S21] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S22] PASSED [ 82%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S23] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S24] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S25] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S26] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S27] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S28] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_targets_and_competitors_are_current_primitives[S29] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S01] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S02] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S03] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S04] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S05] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S06] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S07] PASSED [ 83%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S08] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S09] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S10] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S11] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S12] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S13] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S14] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S15] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S16] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S17] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S18] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S19] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S20] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S21] PASSED [ 84%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S22] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S23] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S24] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S25] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S26] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S27] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S28] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_guide_route_supports_expected_target[S29] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S01] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S02] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S03] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S04] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S05] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S06] PASSED [ 85%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S07] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S08] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S09] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S10] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S11] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S12] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S13] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S14] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S15] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S16] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S17] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S18] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S19] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S20] PASSED [ 86%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S21] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S22] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S23] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S24] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S25] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S26] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S27] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S28] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_case_mode_flags_are_declared_by_their_target[S29] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_flag_value_check_rejects_undeclared_enumerated_value PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S01] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S02] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S03] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S04] PASSED [ 87%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S05] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S06] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S07] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S08] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S09] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S10] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S11] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S12] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S13] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S14] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S15] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S16] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S17] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S18] PASSED [ 88%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S19] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S20] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S21] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S22] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S23] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S24] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S25] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S26] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S27] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S28] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_other_command_routes_are_not_named_by_a_routing_row[S29] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_route_check_rejects_other_route_for_a_routed_command PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S01] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S02] PASSED [ 89%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S03] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S04] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S05] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S06] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S07] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S08] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S09] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S10] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S11] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S12] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S13] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S14] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S15] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S16] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S17] PASSED [ 90%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S18] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S19] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S20] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S21] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S22] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S23] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S24] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S25] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S26] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S27] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S28] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_required_positionals_are_retained_or_clarified[S29] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_positional_check_rejects_a_dropped_required_spec_path PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S01] PASSED [ 91%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S02] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S03] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S04] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S05] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S06] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S07] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S08] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S09] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S10] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S11] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S12] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S13] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S14] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S15] PASSED [ 92%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S16] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S17] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S18] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S19] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S20] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S21] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S22] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S23] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S24] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S25] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S26] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S27] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S28] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_case_mandatory_flags_match_the_guide_row[S29] PASSED [ 93%]
+tests/recommend/test_routing_refresh.py::test_mandatory_flag_check_rejects_omitted_or_altered_entries PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S01] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S02] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S03] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S04] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S05] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S06] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S07] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S08] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S09] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S10] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S11] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S12] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S13] PASSED [ 94%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S14] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S15] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S16] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S17] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S18] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S19] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S20] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S21] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S22] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S23] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S24] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S25] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S26] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S27] PASSED [ 95%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S28] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_case_activation_matches_command_source[S29] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_tdd_activation_uses_the_tdd_skill_not_a_guessed_protocol PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S01] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S02] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S03] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S04] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S05] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S06] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S07] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S08] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S09] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S10] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S11] PASSED [ 96%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S12] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S13] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S14] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S15] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S16] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S17] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S18] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S19] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S20] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S21] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S22] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S23] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S24] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S25] PASSED [ 97%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S26] PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S27] PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S28] PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_variants_name_real_primitives_and_wrong_cache_rows[S29] PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_unmatched_cache_expectation_rejects_unconditional_wording PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_conditional_step_guard_rejects_incidental_only PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_cache_expectation_follows_the_guide_block PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_matched_routes_bypass_cache_so_seeded_rows_cannot_win PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_unmatched_cache_hints_are_consulted_then_rejected PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_example_only_flags_are_not_declared_or_routed PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_retired_identities_have_no_shipped_command PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_command_dispositions_trace_appendix_c_and_inventory PASSED [ 98%]
+tests/recommend/test_routing_refresh.py::test_analyst_reports_and_disposition_appendix_are_retained PASSED [ 98%]
+tests/recommend/test_telemetry.py::TestTelemetryAppend::test_append_event_writes_exactly_five_fields PASSED [ 98%]
+tests/recommend/test_telemetry.py::TestTelemetryAppend::test_append_event_is_line_oriented PASSED [ 99%]
+tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[miss] PASSED [ 99%]
+tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[HIT] PASSED [ 99%]
+tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[cold] PASSED [ 99%]
+tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[success] PASSED [ 99%]
+tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[] PASSED [ 99%]
+tests/recommend/test_telemetry.py::TestTelemetryAppend::test_invalid_cache_result_rejected[miss_unknown] PASSED [ 99%]
+tests/recommend/test_telemetry.py::TestTelemetryAppend::test_all_six_valid_cache_results_accepted PASSED [ 99%]
+tests/cli/test_issue_body_templates.py::test_body_files_shipped_and_installed_flat PASSED [ 99%]
+tests/cli/test_issue_body_templates.py::test_body_file_has_exactly_its_four_headings[ISSUE-BACKLOG.md] PASSED [ 99%]
+tests/cli/test_issue_body_templates.py::test_body_file_has_exactly_its_four_headings[ISSUE-HANDOFF.md] PASSED [ 99%]
+tests/cli/test_issue_body_templates.py::test_body_file_names_no_execution_key_or_clickup[ISSUE-BACKLOG.md] PASSED [ 99%]
+tests/cli/test_issue_body_templates.py::test_body_file_names_no_execution_key_or_clickup[ISSUE-HANDOFF.md] PASSED [ 99%]
+tests/cli/test_issue_body_templates.py::test_claude_md_has_exactly_one_issue_rule_line PASSED [ 99%]
+tests/cli/test_issue_body_templates.py::test_issue_command_and_skill_are_the_only_issue_primitives PASSED [100%]
+
+============================ 1411 passed in 19.57s =============================
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-lint.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-lint.log
new file mode 100644
index 00000000..bc4371d9
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-lint.log
@@ -0,0 +1,162 @@
+$ make lint
+🔍 Checking architecture policy compliance...
+
+=== Check 1/2: Bidirectional Command ↔ Skill Links ===
+  ✅ [Check 1]: adversarial → sc-adversarial-protocol
+  ✅ [Check 1]: auggie-review → sc-auggie-review-protocol
+  ✅ [Check 1]: brainstorm → sc-brainstorm-protocol
+  ✅ [Check 1]: cleanup-audit → sc-cleanup-audit-protocol
+  ✅ [Check 1]: cli-eval → sc-cli-eval-protocol
+  ✅ [Check 1]: cli-portify → sc-cli-portify-protocol
+  ✅ [Check 1]: graph → sc-graph-protocol
+  ✅ [Check 1]: impact → sc-impact-protocol
+  ✅ [Check 1]: implement → sc-implement-protocol
+  ✅ [Check 1]: init-lite → sc-init-lite-protocol
+  ✅ [Check 1]: issue → sc-issue-protocol
+  ✅ [Check 1]: pm → sc-pm-protocol
+  ✅ [Check 1]: post-release → sc-post-release-protocol
+  ✅ [Check 1]: pr-submit → sc-pr-submit-protocol
+  ✅ [Check 1]: recommend → sc-recommend (utility skill; no -protocol suffix)
+  ✅ [Check 1]: reflect → sc-reflect-protocol
+  ✅ [Check 1]: release-split → sc-release-split-protocol
+  ✅ [Check 1]: review-translation → sc-review-translation-protocol
+  ✅ [Check 1]: roadmap → sc-roadmap-protocol
+  ✅ [Check 1]: swarm-wizard → sc-swarm-wizard-protocol
+  ✅ [Check 1]: task → sc-task-protocol
+  ✅ [Check 1]: tasklist → sc-tasklist-protocol
+  ✅ [Check 1]: troubleshoot → sc-troubleshoot-protocol
+  ✅ [Check 1]: validate-roadmap → sc-validate-roadmap-protocol
+  ✅ [Check 1]: validate-tests → sc-validate-tests-protocol
+  ✅ [Check 1]: workflow → sc-workflow-protocol
+  ✅ [Check 2]: sc-adversarial-protocol ← adversarial.md
+  ✅ [Check 2]: sc-auggie-review-protocol ← auggie-review.md
+  ✅ [Check 2]: sc-brainstorm-protocol ← brainstorm.md
+  ✅ [Check 2]: sc-cleanup-audit-protocol ← cleanup-audit.md
+  ✅ [Check 2]: sc-cli-eval-protocol ← cli-eval.md
+  ✅ [Check 2]: sc-cli-portify-protocol ← cli-portify.md
+  ✅ [Check 2]: sc-graph-protocol ← graph.md
+  ✅ [Check 2]: sc-impact-protocol ← impact.md
+  ✅ [Check 2]: sc-implement-protocol ← implement.md
+  ✅ [Check 2]: sc-init-lite-protocol ← init-lite.md
+  ✅ [Check 2]: sc-issue-protocol ← issue.md
+  ✅ [Check 2]: sc-pm-protocol ← pm.md
+  ✅ [Check 2]: sc-post-release-protocol ← post-release.md
+  ✅ [Check 2]: sc-pr-submit-protocol ← pr-submit.md
+  ✅ [Check 2]: sc-reflect-protocol ← reflect.md
+  ✅ [Check 2]: sc-release-split-protocol ← release-split.md
+  ✅ [Check 2]: sc-review-translation-protocol ← review-translation.md
+  ✅ [Check 2]: sc-roadmap-protocol ← roadmap.md
+  ✅ [Check 2]: sc-swarm-wizard-protocol ← swarm-wizard.md
+  ✅ [Check 2]: sc-task-protocol ← task.md
+  ✅ [Check 2]: sc-tasklist-protocol ← tasklist.md
+  ✅ [Check 2]: sc-troubleshoot-protocol ← troubleshoot.md
+  ✅ [Check 2]: sc-validate-roadmap-protocol ← validate-roadmap.md
+  ✅ [Check 2]: sc-validate-tests-protocol ← validate-tests.md
+  ✅ [Check 2]: sc-workflow-protocol ← workflow.md
+
+=== Check 3/4: Command Size Limits ===
+  ⚠️  WARN [Check 3]: brainstorm.md (201 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: reflect.md (305 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: spawn.md (210 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: spec-panel.md (462 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: troubleshoot.md (215 lines, warn threshold 200)
+
+=== Check 6: Activation Section Present (for paired commands) ===
+  ✅ [Check 6]: adversarial.md has ## Activation
+  ✅ [Check 6]: auggie-review.md has ## Activation
+  ✅ [Check 6]: brainstorm.md has ## Activation
+  ✅ [Check 6]: cleanup-audit.md has ## Activation
+  ✅ [Check 6]: cli-eval.md has ## Activation
+  ✅ [Check 6]: cli-portify.md has ## Activation
+  ✅ [Check 6]: graph.md has ## Activation
+  ✅ [Check 6]: impact.md has ## Activation
+  ✅ [Check 6]: implement.md has ## Activation
+  ✅ [Check 6]: init-lite.md has ## Activation
+  ✅ [Check 6]: issue.md has ## Activation
+  ✅ [Check 6]: pm.md has ## Activation
+  ✅ [Check 6]: post-release.md has ## Activation
+  ✅ [Check 6]: pr-submit.md has ## Activation
+  ✅ [Check 6]: reflect.md has ## Activation
+  ✅ [Check 6]: release-split.md has ## Activation
+  ✅ [Check 6]: review-translation.md has ## Activation
+  ✅ [Check 6]: roadmap.md has ## Activation
+  ✅ [Check 6]: swarm-wizard.md has ## Activation
+  ✅ [Check 6]: task.md has ## Activation
+  ✅ [Check 6]: tasklist.md has ## Activation
+  ✅ [Check 6]: troubleshoot.md has ## Activation
+  ✅ [Check 6]: validate-roadmap.md has ## Activation
+  ✅ [Check 6]: validate-tests.md has ## Activation
+  ✅ [Check 6]: workflow.md has ## Activation
+
+=== Check 8: Skill Frontmatter Completeness ===
+  ✅ [Check 8]: sc-adversarial-protocol frontmatter complete
+  ✅ [Check 8]: sc-auggie-review-protocol frontmatter complete
+  ✅ [Check 8]: sc-brainstorm-protocol frontmatter complete
+  ✅ [Check 8]: sc-cleanup-audit-protocol frontmatter complete
+  ✅ [Check 8]: sc-cli-eval-protocol frontmatter complete
+  ✅ [Check 8]: sc-cli-portify-protocol frontmatter complete
+  ✅ [Check 8]: sc-graph-protocol frontmatter complete
+  ✅ [Check 8]: sc-impact-protocol frontmatter complete
+  ✅ [Check 8]: sc-implement-protocol frontmatter complete
+  ✅ [Check 8]: sc-init-lite-protocol frontmatter complete
+  ✅ [Check 8]: sc-issue-protocol frontmatter complete
+  ✅ [Check 8]: sc-pm-protocol frontmatter complete
+  ✅ [Check 8]: sc-post-release-protocol frontmatter complete
+  ✅ [Check 8]: sc-pr-submit-protocol frontmatter complete
+  ✅ [Check 8]: sc-reflect-protocol frontmatter complete
+  ✅ [Check 8]: sc-release-split-protocol frontmatter complete
+  ✅ [Check 8]: sc-review-translation-protocol frontmatter complete
+  ✅ [Check 8]: sc-roadmap-protocol frontmatter complete
+  ✅ [Check 8]: sc-swarm-wizard-protocol frontmatter complete
+  ✅ [Check 8]: sc-task-protocol frontmatter complete
+  ✅ [Check 8]: sc-tasklist-protocol frontmatter complete
+  ✅ [Check 8]: sc-troubleshoot-protocol frontmatter complete
+  ✅ [Check 8]: sc-validate-roadmap-protocol frontmatter complete
+  ✅ [Check 8]: sc-validate-tests-protocol frontmatter complete
+  ✅ [Check 8]: sc-workflow-protocol frontmatter complete
+
+=== Check 9: Protocol Naming Consistency ===
+  ✅ [Check 9]: sc:adversarial-protocol ends in -protocol
+  ✅ [Check 9]: sc:auggie-review-protocol ends in -protocol
+  ✅ [Check 9]: sc:brainstorm-protocol ends in -protocol
+  ✅ [Check 9]: sc:cleanup-audit-protocol ends in -protocol
+  ✅ [Check 9]: sc:cli-eval-protocol ends in -protocol
+  ✅ [Check 9]: sc-cli-portify-protocol ends in -protocol
+  ✅ [Check 9]: sc:graph-protocol ends in -protocol
+  ✅ [Check 9]: sc:impact-protocol ends in -protocol
+  ✅ [Check 9]: sc:implement-protocol ends in -protocol
+  ✅ [Check 9]: sc:init-lite-protocol ends in -protocol
+  ✅ [Check 9]: sc:issue-protocol ends in -protocol
+  ✅ [Check 9]: sc:pm-protocol ends in -protocol
+  ✅ [Check 9]: sc:post-release-protocol ends in -protocol
+  ✅ [Check 9]: sc:pr-submit-protocol ends in -protocol
+  ✅ [Check 9]: sc:reflect-protocol ends in -protocol
+  ✅ [Check 9]: sc:release-split-protocol ends in -protocol
+  ✅ [Check 9]: sc:review-translation-protocol ends in -protocol
+  ✅ [Check 9]: sc:roadmap-protocol ends in -protocol
+  ✅ [Check 9]: sc:swarm-wizard-protocol ends in -protocol
+  ✅ [Check 9]: sc:task-protocol ends in -protocol
+  ✅ [Check 9]: sc:tasklist-protocol ends in -protocol
+  ✅ [Check 9]: sc:troubleshoot-protocol ends in -protocol
+  ✅ [Check 9]: sc-validate-roadmap-protocol ends in -protocol
+  ✅ [Check 9]: sc:validate-tests-protocol ends in -protocol
+  ✅ [Check 9]: sc:workflow-protocol ends in -protocol
+
+=== Check 10: Workspace Suffix Blocklist ===
+  ✅ [Check 10]: no *-workspace directories under .claude/skills/
+
+=== Check 11: Contract Constant Anti-Duplication (Contract #5 + #8) ===
+  ✅ [Check 11]: no contract-constant duplications
+
+=== Checks 5/7: NEEDS DESIGN (skipped) ===
+  ℹ️  Check 5 (inline protocol detection) — pending design
+  ℹ️  Check 7 (activation references correct skill) — pending design
+
+=== Summary ===
+  Errors:   0
+  Warnings: 5
+  ✅ PASS — architecture policy compliant (5 warning(s))
+Running linter...
+uv run ruff check .
+All checks passed!
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-verify-sync.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-verify-sync.log
new file mode 100644
index 00000000..cb6ce040
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-verify-sync.log
@@ -0,0 +1,219 @@
+$ make verify-sync
+🔍 Verifying src/superclaude/ ↔ .claude/ sync...
+
+=== Skills ===
+  ✅ ccsession-tag
+  ✅ confidence-check
+  ✅ operational-guide
+  ✅ prd
+  ✅ readme
+  ✅ roadmap
+  ✅ sc-adversarial-protocol
+  ✅ sc-auggie-review-protocol
+  ✅ sc-bare-review
+  ✅ sc-brainstorm-protocol
+  ✅ sc-cleanup-audit-protocol
+  ✅ sc-cli-eval-protocol
+  ✅ sc-cli-portify-protocol
+  ✅ sc-crash-recovery
+  ✅ sc-graph-protocol
+  ✅ sc-impact-protocol
+  ✅ sc-implement-protocol
+  ✅ sc-init-lite-protocol
+  ✅ sc-issue-protocol
+  ✅ sc-pm-protocol
+  ✅ sc-post-release-protocol
+  ✅ sc-pr-submit-protocol
+  ✅ sc-recommend
+  ✅ sc-reflect-protocol
+  ✅ sc-release-split-protocol
+  ✅ sc-review-translation-protocol
+  ✅ sc-roadmap-protocol
+  ✅ sc-swarm-wizard-protocol
+  ✅ sc-task-protocol
+  ✅ sc-tasklist-protocol
+  ✅ sc-troubleshoot-protocol
+  ✅ sc-validate-roadmap-protocol
+  ✅ sc-validate-tests-protocol
+  ✅ sc-workflow-protocol
+  ✅ task-builder
+  ✅ task
+  ✅ tdd
+  ✅ tech-reference
+  ✅ tech-research
+
+=== Agents ===
+  ✅ audit-analyzer.md
+  ✅ audit-comparator.md
+  ✅ audit-consolidator.md
+  ✅ audit-scanner.md
+  ✅ audit-validator.md
+  ✅ auggie-reviewer.md
+  ✅ backend-architect.md
+  ✅ business-panel-experts.md
+  ✅ confidence-calibrator.md
+  ✅ debate-orchestrator.md
+  ✅ deep-research-agent.md
+  ✅ deep-research.md
+  ✅ devops-architect.md
+  ✅ eval-docs-loader.md
+  ✅ eval-run-reporter.md
+  ✅ eval-suite-author.md
+  ✅ evidence-validator.md
+  ✅ frontend-architect.md
+  ✅ implement-retry-adviser.md
+  ✅ issue-worker-t1.md
+  ✅ issue-worker-t2.md
+  ✅ issue-worker-t3.md
+  ✅ learning-guide.md
+  ✅ merge-executor.md
+  ✅ performance-engineer.md
+  ✅ pm-agent.md
+  ✅ python-expert.md
+  ✅ quality-engineer.md
+  ✅ refactoring-expert.md
+  ✅ reflect-reviewer.md
+  ✅ repo-index.md
+  ✅ requirements-analyst.md
+  ✅ reuse-auditor.md
+  ✅ rf-analyst.md
+  ✅ rf-assembler.md
+  ✅ rf-qa-qualitative.md
+  ✅ rf-qa.md
+  ✅ rf-task-builder.md
+  ✅ rf-task-executor.md
+  ✅ rf-task-researcher.md
+  ✅ rf-team-lead.md
+  ✅ root-cause-analyst.md
+  ✅ security-engineer.md
+  ✅ self-review.md
+  ✅ socratic-mentor.md
+  ✅ system-architect.md
+  ✅ technical-writer.md
+  ✅ troubleshoot-analyst.md
+
+=== Commands ===
+  ✅ adversarial.md
+  ✅ agent.md
+  ✅ analyze.md
+  ✅ auggie-review.md
+  ✅ brainstorm.md
+  ✅ build.md
+  ✅ business-panel.md
+  ✅ cleanup-audit.md
+  ✅ cleanup.md
+  ✅ cli-eval.md
+  ✅ cli-portify.md
+  ✅ design.md
+  ✅ document.md
+  ✅ explain.md
+  ✅ git.md
+  ✅ graph.md
+  ✅ help.md
+  ✅ impact.md
+  ✅ implement.md
+  ✅ improve.md
+  ✅ index-repo.md
+  ✅ index.md
+  ✅ init-lite.md
+  ✅ issue.md
+  ✅ load.md
+  ✅ pm.md
+  ✅ post-release.md
+  ✅ pr-submit.md
+  ✅ recommend.md
+  ✅ reflect.md
+  ✅ release-split.md
+  ✅ research.md
+  ✅ review-translation.md
+  ✅ roadmap.md
+  ✅ save.md
+  ✅ spawn.md
+  ✅ spec-panel.md
+  ✅ swarm-wizard.md
+  ✅ task.md
+  ✅ tasklist.md
+  ✅ tdd.md
+  ✅ test.md
+  ✅ troubleshoot.md
+  ✅ validate-roadmap.md
+  ✅ validate-tests.md
+  ✅ workflow.md
+
+=== Hooks ===
+  ✅ auggie-flag-clear.sh
+  ✅ codegraph-session-start.sh
+  ✅ freshness-file-changed.sh
+  ✅ freshness-post-read.sh
+  ✅ freshness-pre-edit.sh
+  ✅ freshness-session-start.sh
+  ✅ freshness-subagent-start.sh
+  ✅ freshness-subagent-stop.sh
+  ✅ freshness-user-prompt.sh
+  ✅ reject-workspace-writes.sh
+  ✅ sc-recommend-phase0.sh
+  ✅ pragmatic-subagent.js
+
+=== Templates ===
+  ✅ workflow/05_prd_template.md
+  ✅ workflow/03_project_plan_template.md
+  ✅ workflow/03_component_authoring_template.md
+  ✅ workflow/00_mdtm_template_simple_task.md
+  ✅ workflow/01_mdtm_template_generic_task__gfdoc.md
+  ✅ workflow/06_architecture_proposal_template.md
+  ✅ workflow/02_mdtm_template_complex_task.md
+  ✅ workflow/04_feature_brief_template.md
+  ✅ workflow/changelog_template.md
+  ✅ workflow/01_mdtm_template_generic_task.md
+  ✅ workflow/99_mdtm_template_generic_task_old.md
+  ✅ documents/prd_template.md
+  ✅ documents/operational_guide_template.md
+  ✅ documents/GFxAI_Master_Documentation_Template.md
+  ✅ documents/tdd_template.md
+  ✅ documents/agent_template_analysis.md
+  ✅ documents/supplemental-doc-creation-checklist.md
+  ✅ documents/agent_template_qa.md
+  ✅ documents/skill_template.md
+  ✅ documents/roadmap_template.md
+  ✅ documents/agent_template_worker.md
+  ✅ documents/release-spec-template.md
+  ✅ documents/supplemental_doc_template.md
+  ✅ documents/technical_reference_template.md
+  ✅ documents/readme_template.md
+  ✅ modularization-template-review/qa-fix-summary_template.md
+  ✅ modularization-template-review/qa-task-research-alignment_report_template.md
+  ✅ modularization-template-review/analyst-synthesis-review_report_template.md
+  ✅ modularization-template-review/research-notes_template.md
+  ✅ modularization-template-review/synthetic-dnsp-finding.contract
+  ✅ modularization-template-review/INDEX.md
+  ✅ modularization-template-review/qa-task-validation-structure_report_template.md
+  ✅ modularization-template-review/qa-cross-source-contradictions_template.md
+  ✅ modularization-template-review/track-scope-map_template.md
+  ✅ modularization-template-review/claim-evidence-matrix_template.md
+  ✅ modularization-template-review/qa-inventory_report_template.md
+  ✅ modularization-template-review/analyst-coverage-matrix_template.md
+  ✅ modularization-template-review/codebase-research_template.md
+  ✅ modularization-template-review/analyst-completeness_report_template.md
+  ✅ modularization-template-review/analyst-gap-analysis_template.md
+  ✅ modularization-template-review/qa-lens_report_template.md
+  ✅ modularization-template-review/qa-consolidated-findings_template.md
+  ✅ modularization-template-review/qa-task-validation-b2_report_template.md
+  ✅ modularization-template-review/qa-research-gap_report_template.md
+  ✅ modularization-template-review/qa-research-evidence_report_template.md
+  ✅ modularization-template-review/qa-qualitative-operational_report_template.md
+  ✅ modularization-template-review/qa-qualitative-sufficiency_report_template.md
+  ✅ modularization-template-review/analyst-cross-validation_report_template.md
+  ✅ modularization-template-review/qa-acceptance-methodology-audit_template.md
+  ✅ modularization-template-review/pipeline-complete_report_template.md
+  ✅ modularization-template-review/qa-source-fidelity_template.md
+  ✅ modularization-template-review/qa-research-depth_report_template.md
+  ✅ modularization-template-review/web-research_template.md
+
+=== Installer Registration ===
+  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js
+
+=== Hooks Cross-Consistency ===
+  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
+
+✅ All components in sync.
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-failures.md b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-failures.md
new file mode 100644
index 00000000..bb76fff0
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-failures.md
@@ -0,0 +1,15 @@
+# Task 14: remaining failures
+
+None. No test failed, so no master comparison was needed and no `issue302-master-check` worktree was created.
+
+| Check | Command | Outcome | Log (outcome line) |
+|---|---|---|---|
+| Targeted suite | `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py` | 1411 passed, rc=0 | `./t14-targeted.log` |
+| Full suite | `uv run pytest` | 14830 passed, 136 skipped, 2 xpassed, 0 failed, 0 errors, rc=0 | `./t14-full-pytest.log` |
+| Lint | `make lint` | `All checks passed!`, rc=0 | `./t14-lint.log` |
+| Sync | `make verify-sync` | `All components in sync.`, rc=0 | `./t14-verify-sync.log` |
+
+Environment notes (not failures):
+
+- `ruff` was not installed in this worktree's `.venv`, so `make lint` could not start it. `make install` (the project's own setup target, `uv pip install -e ".[dev]"`, which pins `ruff==0.15.20`) was run first; its output is in `./t14-make-install.log`. No project file changed.
+- The full suite rewrites the tracked file `.dev/releases/current/cliEval/evidence/T02.15/perf.json` with new timing numbers (`tests/cli/eval/test_perf_home_setup.py` writes it; existing behaviour, not part of this feature). The file was unmodified before the run; it was restored with `git restore -- .dev/releases/current/cliEval/evidence/T02.15/perf.json` so the branch carries no unrelated change.
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-make-install.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-make-install.log
new file mode 100644
index 00000000..cab76d3d
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-make-install.log
@@ -0,0 +1,17 @@
+$ make install (dev extras: ruff was missing from this worktree .venv, so make lint could not spawn ruff)
+ + coverage==7.17.1
+ + librt==0.16.0
+ + mypy==2.4.1
+ + mypy-extensions==1.2.0
+ + numpy==2.4.6
+ + pathspec==1.1.1
+ + py-cpuinfo2==10.1.1
+ + pytest-benchmark==5.3.1
+ + pytest-cov==7.1.0
+ + ruff==0.15.20
+ + scipy==1.17.1
+ ~ superclaude==5.0.0 (from file:///home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command)
+
+✅ Installation complete!
+   Run 'make verify' to check installation
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-worktree-and-staging.txt b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-worktree-and-staging.txt
new file mode 100644
index 00000000..9ddd0218
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t14-worktree-and-staging.txt
@@ -0,0 +1,5 @@
+$ orca worktree list | grep -c issue302-master-check
+0
+(0 = no issue302-master-check worktree)
+$ git status --short .dev/tasks, run after git add .dev/tasks (lines not staged; this file itself excluded)
+(nothing above = everything under .dev/tasks is staged)

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
