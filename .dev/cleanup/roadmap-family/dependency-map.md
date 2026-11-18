# Dependency map: remove the roadmap, tasklist and sprint family (PR 11, 6.0.0)

Generated read-only from the tracked tree at `956f49642` (head of the `integration` line). Inputs: `git ls-files`, a line search for the removed names, and codegraph/search checks recorded in section 1.

## 1. Import check (the stop rule)

Rule from the prompt: if a kept module imports from `cli/roadmap`, `cli/tasklist`, `cli/sprint` or `compression.py`, stop and report.

- **Kept source modules: none import them.** The only kept source that imports the three packages is `src/superclaude/cli/main.py` (the three registrations). `src/superclaude/cli/eval/isolation.py` and `eval/reporter.py` only mention `cli/sprint/executor.py` in a docstring.
- `compression.py` is imported only by `cli/roadmap/executor.py` and `scripts/compress.py`; both go.
- `cli/sprint/aienv.py` imports `swarm.config`; it goes with sprint. Swarm does not import sprint (checked: no `from superclaude.cli.sprint` under `cli/swarm/`).
- **Kept TEST files that import the removed packages** (the tests cover removed code; each is removed or trimmed, listed in section 4): `tests/pipeline/test_full_flow.py`, `tests/pipeline/test_trailing_gate.py`, `tests/pipeline/test_process.py`, `tests/cli/eval/test_home_isolation_extend.py` (two cases), `tests/unit/test_cli_install.py`, `tests/swarm/test_module_shape.py` (reads `cli/sprint/` on disk).

## 2. Files to delete

Total tracked files deleted: **447**.

| Path (grouped) | Files |
|---|---|
| `docs/analysis-sc-tasklist.md` | 1 |
| `docs/developer-guide/sprint-tui-reference.md` | 1 |
| `docs/generated/sprint-cli/00-overview.md` | 1 |
| `docs/generated/sprint-cli/01-entry-points.md` | 1 |
| `docs/generated/sprint-cli/02-data-models.md` | 1 |
| `docs/generated/sprint-cli/03-execution-engine.md` | 1 |
| `docs/generated/sprint-cli/04-gates-validation.md` | 1 |
| `docs/generated/sprint-cli/05-pm-agent.md` | 1 |
| `docs/generated/sprint-cli/06-artifacts-output.md` | 1 |
| `docs/generated/sprint-cli/07-skills-commands.md` | 1 |
| `docs/generated/sprint-cli/08-test-coverage.md` | 1 |
| `docs/generated/sprint-cli/09-wiring-validation.md` | 1 |
| `docs/generated/sprint-cli/10-critique-validation.md` | 1 |
| `docs/guides/roadmap-cli-tools-release-guide.md` | 1 |
| `docs/guides/sprint-cli-tools-release-guide.md` | 1 |
| `docs/sprint-budget-architecture.md` | 1 |
| `docs/sprint-cli-deep-dive.md` | 1 |
| `plugins/superclaude/templates/roadmaps` | 6 |
| `scripts/compress.py` | 1 |
| `scripts/eval_1.py` | 1 |
| `scripts/eval_2.py` | 1 |
| `scripts/eval_3.py` | 1 |
| `scripts/eval_runner.py` | 1 |
| `scripts/fidelity-check-setup.sh` | 1 |
| `scripts/rerun-incomplete-phases.sh` | 1 |
| `scripts/run-fidelity-batch-refactored.sh` | 1 |
| `scripts/run-fidelity-batch.sh` | 1 |
| `scripts/smoke-test-v2.sh` | 1 |
| `src/superclaude/cli/eval` | 1 |
| `src/superclaude/cli/roadmap` | 53 |
| `src/superclaude/cli/sprint` | 30 |
| `src/superclaude/cli/tasklist` | 6 |
| `src/superclaude/commands/roadmap.md` | 1 |
| `src/superclaude/commands/tasklist.md` | 1 |
| `src/superclaude/commands/validate-roadmap.md` | 1 |
| `src/superclaude/compression.py` | 1 |
| `src/superclaude/examples/roadmap_template.compressed.md` | 1 |
| `src/superclaude/examples/roadmap_template.md` | 1 |
| `src/superclaude/examples/tasklist_index_template.md` | 1 |
| `src/superclaude/examples/tasklist_phase_template.md` | 1 |
| `src/superclaude/skills/sc-roadmap-protocol` | 7 |
| `src/superclaude/skills/sc-tasklist-protocol` | 6 |
| `src/superclaude/skills/sc-validate-roadmap-protocol` | 1 |
| `tests/cli/eval/test_isolation_layers_probe.py` | 1 |
| `tests/cli/eval/test_phase_report_probe.py` | 1 |
| `tests/cli/test_tdd_extract_prompt.py` | 1 |
| `tests/integration/test_sprint_wiring.py` | 1 |
| `tests/integration/test_wiring_e2e_shadow.py` | 1 |
| `tests/roadmap/__init__.py` | 1 |
| `tests/roadmap/conftest.py` | 1 |
| `tests/roadmap/fixtures/recurrence` | 47 |
| `tests/roadmap/test_accept_spec_change.py` | 1 |
| `tests/roadmap/test_anti_instinct_integration.py` | 1 |
| `tests/roadmap/test_anti_instinct_recurrence.py` | 1 |
| `tests/roadmap/test_backward_compat.py` | 1 |
| `tests/roadmap/test_certify_gate_eval.py` | 1 |
| `tests/roadmap/test_certify_gates.py` | 1 |
| `tests/roadmap/test_certify_prompts.py` | 1 |
| `tests/roadmap/test_cli_contract.py` | 1 |
| `tests/roadmap/test_compression_integration.py` | 1 |
| `tests/roadmap/test_convergence.py` | 1 |
| `tests/roadmap/test_convergence_e2e.py` | 1 |
| `tests/roadmap/test_convergence_smoke.py` | 1 |
| `tests/roadmap/test_convergence_wiring.py` | 1 |
| `tests/roadmap/test_cosmetic_remediator.py` | 1 |
| `tests/roadmap/test_dispatch_reachability.py` | 1 |
| `tests/roadmap/test_dry_run.py` | 1 |
| `tests/roadmap/test_embed_inputs.py` | 1 |
| `tests/roadmap/test_eval_convergence_multirun.py` | 1 |
| `tests/roadmap/test_eval_finding_lifecycle.py` | 1 |
| `tests/roadmap/test_eval_gate_ordering.py` | 1 |
| `tests/roadmap/test_eval_gate_rejection.py` | 1 |
| `tests/roadmap/test_executor.py` | 1 |
| `tests/roadmap/test_file_passing.py` | 1 |
| `tests/roadmap/test_fingerprint.py` | 1 |
| `tests/roadmap/test_gate_empty_target.py` | 1 |
| `tests/roadmap/test_gates_data.py` | 1 |
| `tests/roadmap/test_generation_phantom_id_prevention.py` | 1 |
| `tests/roadmap/test_halt.py` | 1 |
| `tests/roadmap/test_inline_fallback.py` | 1 |
| `tests/roadmap/test_integration_contracts.py` | 1 |
| `tests/roadmap/test_integration_v5_pipeline.py` | 1 |
| `tests/roadmap/test_merge_completeness.py` | 1 |
| `tests/roadmap/test_models.py` | 1 |
| `tests/roadmap/test_nfr_compliance.py` | 1 |
| `tests/roadmap/test_no_fragility_stubs.py` | 1 |
| `tests/roadmap/test_obligation_scanner.py` | 1 |
| `tests/roadmap/test_obligation_scanner_extract_component_context.py` | 1 |
| `tests/roadmap/test_obligation_scanner_meta_context.py` | 1 |
| `tests/roadmap/test_parallel.py` | 1 |
| `tests/roadmap/test_parser_consistency.py` | 1 |
| `tests/roadmap/test_phase7_hardening.py` | 1 |
| `tests/roadmap/test_pipeline_envelope.py` | 1 |
| `tests/roadmap/test_pipeline_integration.py` | 1 |
| `tests/roadmap/test_prd_cli.py` | 1 |
| `tests/roadmap/test_prd_prompts.py` | 1 |
| `tests/roadmap/test_progress.py` | 1 |
| `tests/roadmap/test_prompts.py` | 1 |
| `tests/roadmap/test_recurrence_regression.py` | 1 |
| `tests/roadmap/test_remediate.py` | 1 |
| `tests/roadmap/test_remediate_executor.py` | 1 |
| `tests/roadmap/test_remediate_parser.py` | 1 |
| `tests/roadmap/test_remediate_prompts.py` | 1 |
| `tests/roadmap/test_remediation.py` | 1 |
| `tests/roadmap/test_resume.py` | 1 |
| `tests/roadmap/test_resume_pipeline_states.py` | 1 |
| `tests/roadmap/test_resume_restore.py` | 1 |
| `tests/roadmap/test_retrospective.py` | 1 |
| `tests/roadmap/test_retry_contract.py` | 1 |
| `tests/roadmap/test_semantic_layer.py` | 1 |
| `tests/roadmap/test_spec_fidelity.py` | 1 |
| `tests/roadmap/test_spec_parser.py` | 1 |
| `tests/roadmap/test_spec_patch_cycle.py` | 1 |
| `tests/roadmap/test_spec_roadmap_id_containment.py` | 1 |
| `tests/roadmap/test_spec_structural_audit.py` | 1 |
| `tests/roadmap/test_state.py` | 1 |
| `tests/roadmap/test_structural_checkers.py` | 1 |
| `tests/roadmap/test_structural_checkers_properties.py` | 1 |
| `tests/roadmap/test_threshold_registry.py` | 1 |
| `tests/roadmap/test_tool_write_step_certify.py` | 1 |
| `tests/roadmap/test_tool_write_step_debate.py` | 1 |
| `tests/roadmap/test_tool_write_step_diff.py` | 1 |
| `tests/roadmap/test_tool_write_step_extract.py` | 1 |
| `tests/roadmap/test_tool_write_step_extract_tdd.py` | 1 |
| `tests/roadmap/test_tool_write_step_generate.py` | 1 |
| `tests/roadmap/test_tool_write_step_merge.py` | 1 |
| `tests/roadmap/test_tool_write_step_remediation.py` | 1 |
| `tests/roadmap/test_tool_write_step_score.py` | 1 |
| `tests/roadmap/test_tool_write_step_spec_fidelity.py` | 1 |
| `tests/roadmap/test_tool_write_step_test_strategy.py` | 1 |
| `tests/roadmap/test_tool_write_step_validate_reflect.py` | 1 |
| `tests/roadmap/test_validate_cli.py` | 1 |
| `tests/roadmap/test_validate_defects.py` | 1 |
| `tests/roadmap/test_validate_executor.py` | 1 |
| `tests/roadmap/test_validate_gates.py` | 1 |
| `tests/roadmap/test_validate_resume_failure.py` | 1 |
| `tests/roadmap/test_validate_sc001_sc003.py` | 1 |
| `tests/roadmap/test_validate_unit.py` | 1 |
| `tests/roadmap/test_verify_implementation.py` | 1 |
| `tests/roadmap/test_vocabulary.py` | 1 |
| `tests/sc-roadmap/__init__.py` | 1 |
| `tests/sc-roadmap/compliance/__init__.py` | 1 |
| `tests/sc-roadmap/compliance/test_critical_corrections.py` | 1 |
| `tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py` | 1 |
| `tests/sc-roadmap/compliance/test_path_conventions.py` | 1 |
| `tests/sc-roadmap/compliance/test_task_tool_pattern.py` | 1 |
| `tests/sc-roadmap/compliance/test_todowrite_states.py` | 1 |
| `tests/sc-roadmap/conftest.py` | 1 |
| `tests/sc-roadmap/fixtures/invalid_spec.md` | 1 |
| `tests/sc-roadmap/fixtures/minimal_spec.md` | 1 |
| `tests/sc-roadmap/fixtures/sample_spec.md` | 1 |
| `tests/sc-roadmap/integration/__init__.py` | 1 |
| `tests/sc-roadmap/integration/test_adversarial_pipeline.py` | 1 |
| `tests/sc-roadmap/integration/test_full_pipeline.py` | 1 |
| `tests/sc-roadmap/integration/test_return_contract_routing.py` | 1 |
| `tests/sc-roadmap/integration/test_wave1_pipeline.py` | 1 |
| `tests/sc-roadmap/integration/test_wave2_pipeline.py` | 1 |
| `tests/sc-roadmap/integration/test_wave3_pipeline.py` | 1 |
| `tests/sc-roadmap/integration/test_wave4_validation.py` | 1 |
| `tests/sc-roadmap/integration/test_wave5_completion.py` | 1 |
| `tests/sc-roadmap/unit/__init__.py` | 1 |
| `tests/sc-roadmap/unit/test_artifact_generation.py` | 1 |
| `tests/sc-roadmap/unit/test_complexity_scoring.py` | 1 |
| `tests/sc-roadmap/unit/test_domain_analysis.py` | 1 |
| `tests/sc-roadmap/unit/test_extraction.py` | 1 |
| `tests/sc-roadmap/unit/test_milestone_generation.py` | 1 |
| `tests/sc-roadmap/unit/test_persona_activation.py` | 1 |
| `tests/sc-roadmap/unit/test_spec_validation.py` | 1 |
| `tests/sc-roadmap/unit/test_template_discovery.py` | 1 |
| `tests/sprint/__init__.py` | 1 |
| `tests/sprint/conftest.py` | 1 |
| `tests/sprint/diagnostic/__init__.py` | 1 |
| `tests/sprint/diagnostic/conftest.py` | 1 |
| `tests/sprint/diagnostic/test_debug_logger.py` | 1 |
| `tests/sprint/diagnostic/test_diagnostics.py` | 1 |
| `tests/sprint/diagnostic/test_instrumentation.py` | 1 |
| `tests/sprint/diagnostic/test_level_0.py` | 1 |
| `tests/sprint/diagnostic/test_level_1.py` | 1 |
| `tests/sprint/diagnostic/test_level_2.py` | 1 |
| `tests/sprint/diagnostic/test_level_3.py` | 1 |
| `tests/sprint/diagnostic/test_negative.py` | 1 |
| `tests/sprint/e2e_real/__init__.py` | 1 |
| `tests/sprint/e2e_real/conftest.py` | 1 |
| `tests/sprint/e2e_real/fake_claude.py` | 1 |
| `tests/sprint/e2e_real/fake_claude_sourceedit.py` | 1 |
| `tests/sprint/e2e_real/test_e2e_abort_restore.py` | 1 |
| `tests/sprint/e2e_real/test_e2e_isolation_smoke.py` | 1 |
| `tests/sprint/e2e_real/test_e2e_lock_and_retry_cap.py` | 1 |
| `tests/sprint/e2e_real/test_e2e_rerun_happy_path.py` | 1 |
| `tests/sprint/e2e_real/test_e2e_resume.py` | 1 |
| `tests/sprint/e2e_real/test_e2e_resume_drift_stop.py` | 1 |
| `tests/sprint/e2e_real/test_e2e_resume_fresh.py` | 1 |
| `tests/sprint/e2e_real/test_e2e_resume_multiphase.py` | 1 |
| `tests/sprint/e2e_real/test_e2e_sha_guard_real_edit.py` | 1 |
| `tests/sprint/e2e_real/test_e2e_turn_count.py` | 1 |
| `tests/sprint/fixtures/exhaustion` | 9 |
| `tests/sprint/test_aienv.py` | 1 |
| `tests/sprint/test_anti_instinct_sprint.py` | 1 |
| `tests/sprint/test_backward_compat_regression.py` | 1 |
| `tests/sprint/test_checkpoints.py` | 1 |
| `tests/sprint/test_cli_contract.py` | 1 |
| `tests/sprint/test_config.py` | 1 |
| `tests/sprint/test_context_injection.py` | 1 |
| `tests/sprint/test_diagnostics.py` | 1 |
| `tests/sprint/test_e2e_halt.py` | 1 |
| `tests/sprint/test_e2e_success.py` | 1 |
| `tests/sprint/test_e2e_trailing.py` | 1 |
| `tests/sprint/test_execute_sprint_integration.py` | 1 |
| `tests/sprint/test_executor.py` | 1 |
| `tests/sprint/test_gate_display_state.py` | 1 |
| `tests/sprint/test_handoff_backward_compat.py` | 1 |
| `tests/sprint/test_handoff_concurrency.py` | 1 |
| `tests/sprint/test_handoff_crash_consistency.py` | 1 |
| `tests/sprint/test_handoff_performance.py` | 1 |
| `tests/sprint/test_handoff_record.py` | 1 |
| `tests/sprint/test_handoff_store.py` | 1 |
| `tests/sprint/test_integration_halt.py` | 1 |
| `tests/sprint/test_integration_lifecycle.py` | 1 |
| `tests/sprint/test_integration_signal.py` | 1 |
| `tests/sprint/test_kpi_contract.py` | 1 |
| `tests/sprint/test_kpi_report.py` | 1 |
| `tests/sprint/test_logging_events.py` | 1 |
| `tests/sprint/test_models.py` | 1 |
| `tests/sprint/test_monitor.py` | 1 |
| `tests/sprint/test_multi_phase.py` | 1 |
| `tests/sprint/test_nfr_benchmarks.py` | 1 |
| `tests/sprint/test_per_phase_budget.py` | 1 |
| `tests/sprint/test_per_task_env_isolation.py` | 1 |
| `tests/sprint/test_phase5_negative_validation.py` | 1 |
| `tests/sprint/test_phase8_halt_fix.py` | 1 |
| `tests/sprint/test_poll_watchdog_ceiling.py` | 1 |
| `tests/sprint/test_preflight.py` | 1 |
| `tests/sprint/test_process.py` | 1 |
| `tests/sprint/test_property_based.py` | 1 |
| `tests/sprint/test_recovery.py` | 1 |
| `tests/sprint/test_recovery_policy.py` | 1 |
| `tests/sprint/test_regression_gaps.py` | 1 |
| `tests/sprint/test_rerun_tasks.py` | 1 |
| `tests/sprint/test_rerun_tasks_e2e.py` | 1 |
| `tests/sprint/test_rerun_tasks_failure_modes.py` | 1 |
| `tests/sprint/test_resolve_release_dir.py` | 1 |
| `tests/sprint/test_resume.py` | 1 |
| `tests/sprint/test_resume_backward_compat.py` | 1 |
| `tests/sprint/test_resume_contract.py` | 1 |
| `tests/sprint/test_resume_semantics.py` | 1 |
| `tests/sprint/test_retrospective.py` | 1 |
| `tests/sprint/test_scheduler.py` | 1 |
| `tests/sprint/test_shadow_mode.py` | 1 |
| `tests/sprint/test_sprint_docs_cli_parity.py` | 1 |
| `tests/sprint/test_stage1_wiring.py` | 1 |
| `tests/sprint/test_state_dir_isolation.py` | 1 |
| `tests/sprint/test_summarizer.py` | 1 |
| `tests/sprint/test_tmux.py` | 1 |
| `tests/sprint/test_tui.py` | 1 |
| `tests/sprint/test_tui_gate_column.py` | 1 |
| `tests/sprint/test_tui_monitor.py` | 1 |
| `tests/sprint/test_tui_redirect_gate.py` | 1 |
| `tests/sprint/test_tui_task_updates.py` | 1 |
| `tests/sprint/test_tui_v2_wave1.py` | 1 |
| `tests/sprint/test_tui_v2_wave2.py` | 1 |
| `tests/sprint/test_turn_ledger_concurrency.py` | 1 |
| `tests/sprint/test_watchdog.py` | 1 |
| `tests/sprint/test_wiring_budget_scenarios.py` | 1 |
| `tests/sprint/test_wiring_integration.py` | 1 |
| `tests/sprint/test_wiring_mode_resolution.py` | 1 |
| `tests/sprint/test_wiring_performance.py` | 1 |
| `tests/tasklist/__init__.py` | 1 |
| `tests/tasklist/test_autowire.py` | 1 |
| `tests/tasklist/test_bash_policy_contract.py` | 1 |
| `tests/tasklist/test_prd_cli.py` | 1 |
| `tests/tasklist/test_prd_prompts.py` | 1 |
| `tests/tasklist/test_tasklist_cli.py` | 1 |
| `tests/tasklist/test_tasklist_fidelity.py` | 1 |
| `tests/test_sc_roadmap_refactor.sh` | 1 |
| `tests/troubleshoot/fixtures/procedures` | 4 |
| `tests/unit/test_eval_runner_master_checkout.py` | 1 |
| `tests/v3.3/__init__.py` | 1 |
| `tests/v3.3/conftest.py` | 1 |
| `tests/v3.3/test_broken_wiring_detection.py` | 1 |
| `tests/v3.3/test_fidelity_checker.py` | 1 |
| `tests/v3.3/test_gate_rollout_modes.py` | 1 |
| `tests/v3.3/test_integration_regression.py` | 1 |
| `tests/v3.3/test_reachability_eval.py` | 1 |
| `tests/v3.3/test_session_summary.py` | 1 |
| `tests/v3.3/test_turnledger_lifecycle.py` | 1 |
| `tests/v3.3/test_wiring_points_e2e.py` | 1 |
| `tests/v3.3/wiring_manifest.yaml` | 1 |
| `tests/v3.3/wiring_manifest_schema.yaml` | 1 |

Full list:

- `docs/analysis-sc-tasklist.md`
- `docs/developer-guide/sprint-tui-reference.md`
- `docs/generated/sprint-cli/00-overview.md`
- `docs/generated/sprint-cli/01-entry-points.md`
- `docs/generated/sprint-cli/02-data-models.md`
- `docs/generated/sprint-cli/03-execution-engine.md`
- `docs/generated/sprint-cli/04-gates-validation.md`
- `docs/generated/sprint-cli/05-pm-agent.md`
- `docs/generated/sprint-cli/06-artifacts-output.md`
- `docs/generated/sprint-cli/07-skills-commands.md`
- `docs/generated/sprint-cli/08-test-coverage.md`
- `docs/generated/sprint-cli/09-wiring-validation.md`
- `docs/generated/sprint-cli/10-critique-validation.md`
- `docs/guides/roadmap-cli-tools-release-guide.md`
- `docs/guides/sprint-cli-tools-release-guide.md`
- `docs/sprint-budget-architecture.md`
- `docs/sprint-cli-deep-dive.md`
- `plugins/superclaude/templates/roadmaps/documentation-release.md`
- `plugins/superclaude/templates/roadmaps/feature-release.md`
- `plugins/superclaude/templates/roadmaps/migration-release.md`
- `plugins/superclaude/templates/roadmaps/performance-release.md`
- `plugins/superclaude/templates/roadmaps/quality-release.md`
- `plugins/superclaude/templates/roadmaps/security-release.md`
- `scripts/compress.py`
- `scripts/eval_1.py`
- `scripts/eval_2.py`
- `scripts/eval_3.py`
- `scripts/eval_runner.py`
- `scripts/fidelity-check-setup.sh`
- `scripts/rerun-incomplete-phases.sh`
- `scripts/run-fidelity-batch-refactored.sh`
- `scripts/run-fidelity-batch.sh`
- `scripts/smoke-test-v2.sh`
- `src/superclaude/cli/eval/suites/tasklist_deterministic_shape.yaml`
- `src/superclaude/cli/roadmap/__init__.py`
- `src/superclaude/cli/roadmap/certify_prompts.py`
- `src/superclaude/cli/roadmap/code_assertions.py`
- `src/superclaude/cli/roadmap/commands.py`
- `src/superclaude/cli/roadmap/convergence.py`
- `src/superclaude/cli/roadmap/cosmetic_remediator.py`
- `src/superclaude/cli/roadmap/envelope.py`
- `src/superclaude/cli/roadmap/executor.py`
- `src/superclaude/cli/roadmap/fidelity_checker.py`
- `src/superclaude/cli/roadmap/fingerprint.py`
- `src/superclaude/cli/roadmap/gates.py`
- `src/superclaude/cli/roadmap/id_registry.py`
- `src/superclaude/cli/roadmap/integration_contracts.py`
- `src/superclaude/cli/roadmap/models.py`
- `src/superclaude/cli/roadmap/obligation_scanner.py`
- `src/superclaude/cli/roadmap/prompts.py`
- `src/superclaude/cli/roadmap/remediate.py`
- `src/superclaude/cli/roadmap/remediate_executor.py`
- `src/superclaude/cli/roadmap/remediate_parser.py`
- `src/superclaude/cli/roadmap/remediate_prompts.py`
- `src/superclaude/cli/roadmap/semantic_layer.py`
- `src/superclaude/cli/roadmap/spec_parser.py`
- `src/superclaude/cli/roadmap/spec_patch.py`
- `src/superclaude/cli/roadmap/spec_structural_audit.py`
- `src/superclaude/cli/roadmap/structural_checkers.py`
- `src/superclaude/cli/roadmap/templates.py`
- `src/superclaude/cli/roadmap/templates/certify.md.j2`
- `src/superclaude/cli/roadmap/templates/debate.md.j2`
- `src/superclaude/cli/roadmap/templates/diff.md.j2`
- `src/superclaude/cli/roadmap/templates/extract.md.j2`
- `src/superclaude/cli/roadmap/templates/extract_tdd.md.j2`
- `src/superclaude/cli/roadmap/templates/generate.md.j2`
- `src/superclaude/cli/roadmap/templates/merge.md.j2`
- `src/superclaude/cli/roadmap/templates/reflect.md.j2`
- `src/superclaude/cli/roadmap/templates/score.md.j2`
- `src/superclaude/cli/roadmap/templates/spec_fidelity.md.j2`
- `src/superclaude/cli/roadmap/templates/test_strategy.md.j2`
- `src/superclaude/cli/roadmap/templates/tool_schemas/certify.schema.json`
- `src/superclaude/cli/roadmap/templates/tool_schemas/debate.schema.json`
- `src/superclaude/cli/roadmap/templates/tool_schemas/diff.schema.json`
- `src/superclaude/cli/roadmap/templates/tool_schemas/extract.schema.json`
- `src/superclaude/cli/roadmap/templates/tool_schemas/extract_tdd.schema.json`
- `src/superclaude/cli/roadmap/templates/tool_schemas/generate.schema.json`
- `src/superclaude/cli/roadmap/templates/tool_schemas/merge.schema.json`
- `src/superclaude/cli/roadmap/templates/tool_schemas/reflect.schema.json`
- `src/superclaude/cli/roadmap/templates/tool_schemas/score.schema.json`
- `src/superclaude/cli/roadmap/templates/tool_schemas/spec_fidelity.schema.json`
- `src/superclaude/cli/roadmap/templates/tool_schemas/test_strategy.schema.json`
- `src/superclaude/cli/roadmap/tool_writer.py`
- `src/superclaude/cli/roadmap/validate_executor.py`
- `src/superclaude/cli/roadmap/validate_gates.py`
- `src/superclaude/cli/roadmap/validate_prompts.py`
- `src/superclaude/cli/roadmap/verify_implementation.py`
- `src/superclaude/cli/sprint/__init__.py`
- `src/superclaude/cli/sprint/aienv.py`
- `src/superclaude/cli/sprint/checkpoints.py`
- `src/superclaude/cli/sprint/classifiers.py`
- `src/superclaude/cli/sprint/commands.py`
- `src/superclaude/cli/sprint/config.py`
- `src/superclaude/cli/sprint/debug_logger.py`
- `src/superclaude/cli/sprint/diagnostics.py`
- `src/superclaude/cli/sprint/executor.py`
- `src/superclaude/cli/sprint/handoff.py`
- `src/superclaude/cli/sprint/kpi.py`
- `src/superclaude/cli/sprint/logging_.py`
- `src/superclaude/cli/sprint/models.py`
- `src/superclaude/cli/sprint/monitor.py`
- `src/superclaude/cli/sprint/notify.py`
- `src/superclaude/cli/sprint/preflight.py`
- `src/superclaude/cli/sprint/process.py`
- `src/superclaude/cli/sprint/recovery.py`
- `src/superclaude/cli/sprint/recovery_policy.py`
- `src/superclaude/cli/sprint/rerun_tasks.py`
- `src/superclaude/cli/sprint/resume/__init__.py`
- `src/superclaude/cli/sprint/resume/drift.py`
- `src/superclaude/cli/sprint/resume/integrity.py`
- `src/superclaude/cli/sprint/resume/models.py`
- `src/superclaude/cli/sprint/resume/planner.py`
- `src/superclaude/cli/sprint/retrospective.py`
- `src/superclaude/cli/sprint/scheduler.py`
- `src/superclaude/cli/sprint/summarizer.py`
- `src/superclaude/cli/sprint/tmux.py`
- `src/superclaude/cli/sprint/tui.py`
- `src/superclaude/cli/tasklist/__init__.py`
- `src/superclaude/cli/tasklist/commands.py`
- `src/superclaude/cli/tasklist/executor.py`
- `src/superclaude/cli/tasklist/gates.py`
- `src/superclaude/cli/tasklist/models.py`
- `src/superclaude/cli/tasklist/prompts.py`
- `src/superclaude/commands/roadmap.md`
- `src/superclaude/commands/tasklist.md`
- `src/superclaude/commands/validate-roadmap.md`
- `src/superclaude/compression.py`
- `src/superclaude/examples/roadmap_template.compressed.md`
- `src/superclaude/examples/roadmap_template.md`
- `src/superclaude/examples/tasklist_index_template.md`
- `src/superclaude/examples/tasklist_phase_template.md`
- `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`
- `src/superclaude/skills/sc-roadmap-protocol/__init__.py`
- `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md`
- `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`
- `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md`
- `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md`
- `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md`
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`
- `src/superclaude/skills/sc-tasklist-protocol/__init__.py`
- `src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md`
- `src/superclaude/skills/sc-tasklist-protocol/rules/tier-classification.md`
- `src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md`
- `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md`
- `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`
- `tests/cli/eval/test_isolation_layers_probe.py`
- `tests/cli/eval/test_phase_report_probe.py`
- `tests/cli/test_tdd_extract_prompt.py`
- `tests/integration/test_sprint_wiring.py`
- `tests/integration/test_wiring_e2e_shadow.py`
- `tests/roadmap/__init__.py`
- `tests/roadmap/conftest.py`
- `tests/roadmap/fixtures/recurrence/README.md`
- `tests/roadmap/fixtures/recurrence/anti_instinct/imperative_verb_with_allowlist_phrase_case.expected.json`
- `tests/roadmap/fixtures/recurrence/anti_instinct/imperative_verb_with_allowlist_phrase_case.md`
- `tests/roadmap/fixtures/recurrence/anti_instinct/module_path_fp_case.expected.json`
- `tests/roadmap/fixtures/recurrence/anti_instinct/module_path_fp_case.md`
- `tests/roadmap/fixtures/recurrence/anti_instinct/multimodelswarm_fp_case.expected.json`
- `tests/roadmap/fixtures/recurrence/anti_instinct/multimodelswarm_fp_case.md`
- `tests/roadmap/fixtures/recurrence/anti_instinct/stub_worker_parallelism_fp_case.expected.json`
- `tests/roadmap/fixtures/recurrence/anti_instinct/stub_worker_parallelism_fp_case.md`
- `tests/roadmap/fixtures/recurrence/anti_instinct/valid_obligation_case.expected.json`
- `tests/roadmap/fixtures/recurrence/anti_instinct/valid_obligation_case.md`
- `tests/roadmap/fixtures/recurrence/deferred/context_window_oom_case.expected.json`
- `tests/roadmap/fixtures/recurrence/deferred/context_window_oom_case.md`
- `tests/roadmap/fixtures/recurrence/deferred/generator_validator_asymmetry_case.expected.json`
- `tests/roadmap/fixtures/recurrence/deferred/generator_validator_asymmetry_case.md`
- `tests/roadmap/fixtures/recurrence/deferred/sprint_executor_vacuous_gate_case.expected.json`
- `tests/roadmap/fixtures/recurrence/deferred/sprint_executor_vacuous_gate_case.md`
- `tests/roadmap/fixtures/recurrence/deferred/telemetry_text_regex_case.expected.json`
- `tests/roadmap/fixtures/recurrence/deferred/telemetry_text_regex_case.md`
- `tests/roadmap/fixtures/recurrence/deferred/truncation_no_detection_case.expected.json`
- `tests/roadmap/fixtures/recurrence/deferred/truncation_no_detection_case.md`
- `tests/roadmap/fixtures/recurrence/dispatch_reachability/skipped_verification_step_case.expected.json`
- `tests/roadmap/fixtures/recurrence/dispatch_reachability/skipped_verification_step_case.md`
- `tests/roadmap/fixtures/recurrence/dispatch_reachability/unwired_certify_step_case.expected.json`
- `tests/roadmap/fixtures/recurrence/dispatch_reachability/unwired_certify_step_case.md`
- `tests/roadmap/fixtures/recurrence/fragility_stub/cross_refs_resolve_stub_case.expected.json`
- `tests/roadmap/fixtures/recurrence/fragility_stub/cross_refs_resolve_stub_case.md`
- `tests/roadmap/fixtures/recurrence/fragility_stub/fail_open_ambiguous_found_case.expected.json`
- `tests/roadmap/fixtures/recurrence/fragility_stub/fail_open_ambiguous_found_case.md`
- `tests/roadmap/fixtures/recurrence/id_containment/milestone_id_case.expected.json`
- `tests/roadmap/fixtures/recurrence/id_containment/milestone_id_case.md`
- `tests/roadmap/fixtures/recurrence/id_containment/spec_roadmap_drift_case.expected.json`
- `tests/roadmap/fixtures/recurrence/id_containment/spec_roadmap_drift_case.md`
- `tests/roadmap/fixtures/recurrence/merge_completeness/merge_dropped_findings_case.expected.json`
- `tests/roadmap/fixtures/recurrence/merge_completeness/merge_dropped_findings_case.md`
- `tests/roadmap/fixtures/recurrence/retry_contract/retry_loop_no_terminal_case.expected.json`
- `tests/roadmap/fixtures/recurrence/retry_contract/retry_loop_no_terminal_case.md`
- `tests/roadmap/fixtures/recurrence/spec_fidelity/deviation_unclassified_case.expected.json`
- `tests/roadmap/fixtures/recurrence/spec_fidelity/deviation_unclassified_case.md`
- `tests/roadmap/fixtures/recurrence/spec_fidelity/phantom_id_high_severity_case.expected.json`
- `tests/roadmap/fixtures/recurrence/spec_fidelity/phantom_id_high_severity_case.md`
- `tests/roadmap/fixtures/recurrence/spec_fidelity/phase_restructure_deviation_case.expected.json`
- `tests/roadmap/fixtures/recurrence/spec_fidelity/phase_restructure_deviation_case.md`
- `tests/roadmap/fixtures/recurrence/threshold_registry/convergence_threshold_drift_case.expected.json`
- `tests/roadmap/fixtures/recurrence/threshold_registry/convergence_threshold_drift_case.md`
- `tests/roadmap/fixtures/recurrence/verification/validation_complete_false_ships_case.expected.json`
- `tests/roadmap/fixtures/recurrence/verification/validation_complete_false_ships_case.md`
- `tests/roadmap/test_accept_spec_change.py`
- `tests/roadmap/test_anti_instinct_integration.py`
- `tests/roadmap/test_anti_instinct_recurrence.py`
- `tests/roadmap/test_backward_compat.py`
- `tests/roadmap/test_certify_gate_eval.py`
- `tests/roadmap/test_certify_gates.py`
- `tests/roadmap/test_certify_prompts.py`
- `tests/roadmap/test_cli_contract.py`
- `tests/roadmap/test_compression_integration.py`
- `tests/roadmap/test_convergence.py`
- `tests/roadmap/test_convergence_e2e.py`
- `tests/roadmap/test_convergence_smoke.py`
- `tests/roadmap/test_convergence_wiring.py`
- `tests/roadmap/test_cosmetic_remediator.py`
- `tests/roadmap/test_dispatch_reachability.py`
- `tests/roadmap/test_dry_run.py`
- `tests/roadmap/test_embed_inputs.py`
- `tests/roadmap/test_eval_convergence_multirun.py`
- `tests/roadmap/test_eval_finding_lifecycle.py`
- `tests/roadmap/test_eval_gate_ordering.py`
- `tests/roadmap/test_eval_gate_rejection.py`
- `tests/roadmap/test_executor.py`
- `tests/roadmap/test_file_passing.py`
- `tests/roadmap/test_fingerprint.py`
- `tests/roadmap/test_gate_empty_target.py`
- `tests/roadmap/test_gates_data.py`
- `tests/roadmap/test_generation_phantom_id_prevention.py`
- `tests/roadmap/test_halt.py`
- `tests/roadmap/test_inline_fallback.py`
- `tests/roadmap/test_integration_contracts.py`
- `tests/roadmap/test_integration_v5_pipeline.py`
- `tests/roadmap/test_merge_completeness.py`
- `tests/roadmap/test_models.py`
- `tests/roadmap/test_nfr_compliance.py`
- `tests/roadmap/test_no_fragility_stubs.py`
- `tests/roadmap/test_obligation_scanner.py`
- `tests/roadmap/test_obligation_scanner_extract_component_context.py`
- `tests/roadmap/test_obligation_scanner_meta_context.py`
- `tests/roadmap/test_parallel.py`
- `tests/roadmap/test_parser_consistency.py`
- `tests/roadmap/test_phase7_hardening.py`
- `tests/roadmap/test_pipeline_envelope.py`
- `tests/roadmap/test_pipeline_integration.py`
- `tests/roadmap/test_prd_cli.py`
- `tests/roadmap/test_prd_prompts.py`
- `tests/roadmap/test_progress.py`
- `tests/roadmap/test_prompts.py`
- `tests/roadmap/test_recurrence_regression.py`
- `tests/roadmap/test_remediate.py`
- `tests/roadmap/test_remediate_executor.py`
- `tests/roadmap/test_remediate_parser.py`
- `tests/roadmap/test_remediate_prompts.py`
- `tests/roadmap/test_remediation.py`
- `tests/roadmap/test_resume.py`
- `tests/roadmap/test_resume_pipeline_states.py`
- `tests/roadmap/test_resume_restore.py`
- `tests/roadmap/test_retrospective.py`
- `tests/roadmap/test_retry_contract.py`
- `tests/roadmap/test_semantic_layer.py`
- `tests/roadmap/test_spec_fidelity.py`
- `tests/roadmap/test_spec_parser.py`
- `tests/roadmap/test_spec_patch_cycle.py`
- `tests/roadmap/test_spec_roadmap_id_containment.py`
- `tests/roadmap/test_spec_structural_audit.py`
- `tests/roadmap/test_state.py`
- `tests/roadmap/test_structural_checkers.py`
- `tests/roadmap/test_structural_checkers_properties.py`
- `tests/roadmap/test_threshold_registry.py`
- `tests/roadmap/test_tool_write_step_certify.py`
- `tests/roadmap/test_tool_write_step_debate.py`
- `tests/roadmap/test_tool_write_step_diff.py`
- `tests/roadmap/test_tool_write_step_extract.py`
- `tests/roadmap/test_tool_write_step_extract_tdd.py`
- `tests/roadmap/test_tool_write_step_generate.py`
- `tests/roadmap/test_tool_write_step_merge.py`
- `tests/roadmap/test_tool_write_step_remediation.py`
- `tests/roadmap/test_tool_write_step_score.py`
- `tests/roadmap/test_tool_write_step_spec_fidelity.py`
- `tests/roadmap/test_tool_write_step_test_strategy.py`
- `tests/roadmap/test_tool_write_step_validate_reflect.py`
- `tests/roadmap/test_validate_cli.py`
- `tests/roadmap/test_validate_defects.py`
- `tests/roadmap/test_validate_executor.py`
- `tests/roadmap/test_validate_gates.py`
- `tests/roadmap/test_validate_resume_failure.py`
- `tests/roadmap/test_validate_sc001_sc003.py`
- `tests/roadmap/test_validate_unit.py`
- `tests/roadmap/test_verify_implementation.py`
- `tests/roadmap/test_vocabulary.py`
- `tests/sc-roadmap/__init__.py`
- `tests/sc-roadmap/compliance/__init__.py`
- `tests/sc-roadmap/compliance/test_critical_corrections.py`
- `tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py`
- `tests/sc-roadmap/compliance/test_path_conventions.py`
- `tests/sc-roadmap/compliance/test_task_tool_pattern.py`
- `tests/sc-roadmap/compliance/test_todowrite_states.py`
- `tests/sc-roadmap/conftest.py`
- `tests/sc-roadmap/fixtures/invalid_spec.md`
- `tests/sc-roadmap/fixtures/minimal_spec.md`
- `tests/sc-roadmap/fixtures/sample_spec.md`
- `tests/sc-roadmap/integration/__init__.py`
- `tests/sc-roadmap/integration/test_adversarial_pipeline.py`
- `tests/sc-roadmap/integration/test_full_pipeline.py`
- `tests/sc-roadmap/integration/test_return_contract_routing.py`
- `tests/sc-roadmap/integration/test_wave1_pipeline.py`
- `tests/sc-roadmap/integration/test_wave2_pipeline.py`
- `tests/sc-roadmap/integration/test_wave3_pipeline.py`
- `tests/sc-roadmap/integration/test_wave4_validation.py`
- `tests/sc-roadmap/integration/test_wave5_completion.py`
- `tests/sc-roadmap/unit/__init__.py`
- `tests/sc-roadmap/unit/test_artifact_generation.py`
- `tests/sc-roadmap/unit/test_complexity_scoring.py`
- `tests/sc-roadmap/unit/test_domain_analysis.py`
- `tests/sc-roadmap/unit/test_extraction.py`
- `tests/sc-roadmap/unit/test_milestone_generation.py`
- `tests/sc-roadmap/unit/test_persona_activation.py`
- `tests/sc-roadmap/unit/test_spec_validation.py`
- `tests/sc-roadmap/unit/test_template_discovery.py`
- `tests/sprint/__init__.py`
- `tests/sprint/conftest.py`
- `tests/sprint/diagnostic/__init__.py`
- `tests/sprint/diagnostic/conftest.py`
- `tests/sprint/diagnostic/test_debug_logger.py`
- `tests/sprint/diagnostic/test_diagnostics.py`
- `tests/sprint/diagnostic/test_instrumentation.py`
- `tests/sprint/diagnostic/test_level_0.py`
- `tests/sprint/diagnostic/test_level_1.py`
- `tests/sprint/diagnostic/test_level_2.py`
- `tests/sprint/diagnostic/test_level_3.py`
- `tests/sprint/diagnostic/test_negative.py`
- `tests/sprint/e2e_real/__init__.py`
- `tests/sprint/e2e_real/conftest.py`
- `tests/sprint/e2e_real/fake_claude.py`
- `tests/sprint/e2e_real/fake_claude_sourceedit.py`
- `tests/sprint/e2e_real/test_e2e_abort_restore.py`
- `tests/sprint/e2e_real/test_e2e_isolation_smoke.py`
- `tests/sprint/e2e_real/test_e2e_lock_and_retry_cap.py`
- `tests/sprint/e2e_real/test_e2e_rerun_happy_path.py`
- `tests/sprint/e2e_real/test_e2e_resume.py`
- `tests/sprint/e2e_real/test_e2e_resume_drift_stop.py`
- `tests/sprint/e2e_real/test_e2e_resume_fresh.py`
- `tests/sprint/e2e_real/test_e2e_resume_multiphase.py`
- `tests/sprint/e2e_real/test_e2e_sha_guard_real_edit.py`
- `tests/sprint/e2e_real/test_e2e_turn_count.py`
- `tests/sprint/fixtures/exhaustion/all_account_cooldown.jsonl`
- `tests/sprint/fixtures/exhaustion/all_account_cooldown_apierror429.jsonl`
- `tests/sprint/fixtures/exhaustion/api_retry_maxed.jsonl`
- `tests/sprint/fixtures/exhaustion/clean_pass.jsonl`
- `tests/sprint/fixtures/exhaustion/operation_timeout.jsonl`
- `tests/sprint/fixtures/exhaustion/provider_429_incidental_ratelimit_text.jsonl`
- `tests/sprint/fixtures/exhaustion/single_account_429.jsonl`
- `tests/sprint/fixtures/exhaustion/single_account_apierror429_SYNTHESIZED.jsonl`
- `tests/sprint/fixtures/exhaustion/task_failure_real.jsonl`
- `tests/sprint/test_aienv.py`
- `tests/sprint/test_anti_instinct_sprint.py`
- `tests/sprint/test_backward_compat_regression.py`
- `tests/sprint/test_checkpoints.py`
- `tests/sprint/test_cli_contract.py`
- `tests/sprint/test_config.py`
- `tests/sprint/test_context_injection.py`
- `tests/sprint/test_diagnostics.py`
- `tests/sprint/test_e2e_halt.py`
- `tests/sprint/test_e2e_success.py`
- `tests/sprint/test_e2e_trailing.py`
- `tests/sprint/test_execute_sprint_integration.py`
- `tests/sprint/test_executor.py`
- `tests/sprint/test_gate_display_state.py`
- `tests/sprint/test_handoff_backward_compat.py`
- `tests/sprint/test_handoff_concurrency.py`
- `tests/sprint/test_handoff_crash_consistency.py`
- `tests/sprint/test_handoff_performance.py`
- `tests/sprint/test_handoff_record.py`
- `tests/sprint/test_handoff_store.py`
- `tests/sprint/test_integration_halt.py`
- `tests/sprint/test_integration_lifecycle.py`
- `tests/sprint/test_integration_signal.py`
- `tests/sprint/test_kpi_contract.py`
- `tests/sprint/test_kpi_report.py`
- `tests/sprint/test_logging_events.py`
- `tests/sprint/test_models.py`
- `tests/sprint/test_monitor.py`
- `tests/sprint/test_multi_phase.py`
- `tests/sprint/test_nfr_benchmarks.py`
- `tests/sprint/test_per_phase_budget.py`
- `tests/sprint/test_per_task_env_isolation.py`
- `tests/sprint/test_phase5_negative_validation.py`
- `tests/sprint/test_phase8_halt_fix.py`
- `tests/sprint/test_poll_watchdog_ceiling.py`
- `tests/sprint/test_preflight.py`
- `tests/sprint/test_process.py`
- `tests/sprint/test_property_based.py`
- `tests/sprint/test_recovery.py`
- `tests/sprint/test_recovery_policy.py`
- `tests/sprint/test_regression_gaps.py`
- `tests/sprint/test_rerun_tasks.py`
- `tests/sprint/test_rerun_tasks_e2e.py`
- `tests/sprint/test_rerun_tasks_failure_modes.py`
- `tests/sprint/test_resolve_release_dir.py`
- `tests/sprint/test_resume.py`
- `tests/sprint/test_resume_backward_compat.py`
- `tests/sprint/test_resume_contract.py`
- `tests/sprint/test_resume_semantics.py`
- `tests/sprint/test_retrospective.py`
- `tests/sprint/test_scheduler.py`
- `tests/sprint/test_shadow_mode.py`
- `tests/sprint/test_sprint_docs_cli_parity.py`
- `tests/sprint/test_stage1_wiring.py`
- `tests/sprint/test_state_dir_isolation.py`
- `tests/sprint/test_summarizer.py`
- `tests/sprint/test_tmux.py`
- `tests/sprint/test_tui.py`
- `tests/sprint/test_tui_gate_column.py`
- `tests/sprint/test_tui_monitor.py`
- `tests/sprint/test_tui_redirect_gate.py`
- `tests/sprint/test_tui_task_updates.py`
- `tests/sprint/test_tui_v2_wave1.py`
- `tests/sprint/test_tui_v2_wave2.py`
- `tests/sprint/test_turn_ledger_concurrency.py`
- `tests/sprint/test_watchdog.py`
- `tests/sprint/test_wiring_budget_scenarios.py`
- `tests/sprint/test_wiring_integration.py`
- `tests/sprint/test_wiring_mode_resolution.py`
- `tests/sprint/test_wiring_performance.py`
- `tests/tasklist/__init__.py`
- `tests/tasklist/test_autowire.py`
- `tests/tasklist/test_bash_policy_contract.py`
- `tests/tasklist/test_prd_cli.py`
- `tests/tasklist/test_prd_prompts.py`
- `tests/tasklist/test_tasklist_cli.py`
- `tests/tasklist/test_tasklist_fidelity.py`
- `tests/test_sc_roadmap_refactor.sh`
- `tests/troubleshoot/fixtures/procedures/tasklist/authorized.md`
- `tests/troubleshoot/fixtures/procedures/tasklist/no-emitter-no-file.md`
- `tests/troubleshoot/fixtures/procedures/tasklist/refused.md`
- `tests/troubleshoot/fixtures/procedures/tasklist/source-only-read.md`
- `tests/unit/test_eval_runner_master_checkout.py`
- `tests/v3.3/__init__.py`
- `tests/v3.3/conftest.py`
- `tests/v3.3/test_broken_wiring_detection.py`
- `tests/v3.3/test_fidelity_checker.py`
- `tests/v3.3/test_gate_rollout_modes.py`
- `tests/v3.3/test_integration_regression.py`
- `tests/v3.3/test_reachability_eval.py`
- `tests/v3.3/test_session_summary.py`
- `tests/v3.3/test_turnledger_lifecycle.py`
- `tests/v3.3/test_wiring_points_e2e.py`
- `tests/v3.3/wiring_manifest.yaml`
- `tests/v3.3/wiring_manifest_schema.yaml`

## 3. Historical records left untouched

`.dev/` (work records), `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, `docs/memory/`, `CHANGELOG.md`, `KNOWLEDGE.md` (accumulated insights, past entries), `docs/v5.0.0.md`. 31427 tracked files fall in this group; none is edited.

## 4. References in kept files (path:line, change needed)

**121 kept files** hold **436** matching lines.

### `CLAUDE.md`
Change: Remove or reword the mention.

- `CLAUDE.md:168`  superclaude sprint run <tasklist-index.md>   # Execute sprint pipeline
- `CLAUDE.md:169`  superclaude roadmap run <spec.md>            # Generate roadmap pipeline
- `CLAUDE.md:170`  superclaude roadmap validate <output-dir>    # Validate roadmap artifacts

### `README.md`
Change: Remove or reword the mention.

- `README.md:114`  superclaude sprint run <tasklist-index.md>
- `README.md:115`  superclaude roadmap run <spec.md>
- `README.md:116`  superclaude roadmap validate <output-dir>
- `README.md:117`  superclaude tasklist validate <output-dir> --roadmap-file <roadmap.md>

### `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`
Change: Doc: remove or reword the mention.

- `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:196`  **Key numbers:** 2 session roles (coordinator, worker) plus the person; 5 owner decisions D1-D5 (historical record `.dev/orca-command-refactor/decisions/APPROVED.md:8-12`...
- `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1321`  9. **Five command files with no `## Unattended mode` section and no bar.** Of the 41 command files, 28 carry the section and 8 names are barred (`WORKER-CONTRACT.md:23`);...
- `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:2203`  \| P0 to P4 \| Phases of the worker-contract rollout plan (`source.md` section 6). P1 and P2 converted 31 commands; 28 remain after the 6.0.0 command removals. The plan p...

### `docs/developer-guide/review-severity-rule.md`
Change: Doc: remove or reword the mention.

- `docs/developer-guide/review-severity-rule.md:68`  \| `/sc:tasklist` patch loop \| Capped at pass `k=2`; open High or Medium (blocking) findings HALT and escalate instead of shipping "logged for human review"; Low finding...
- `docs/developer-guide/review-severity-rule.md:102`  - **Roadmap convergence `max_runs=3`.** The roadmap fidelity gate runs up to 3 checker runs by default (`src/superclaude/cli/roadmap/convergence.py:440`) and remediates o...

### `docs/developer-guide/session-memory.md`
Change: Doc: remove or reword the mention.

- `docs/developer-guide/session-memory.md:26`  \| Other skills that use the store \| `sc-task-protocol`, `sc-reflect-protocol`, `sc-validate-roadmap-protocol`, `sc-crash-recovery` (see [Who reads and writes the store]...
- `docs/developer-guide/session-memory.md:33`  - **Kept out of git.** On the first write, if `<project>/.superclaude/.gitignore` is absent, the writer creates it with the single line `*` (`pm-agent.md:21`). The whole ...
- `docs/developer-guide/session-memory.md:47`  └── validate-roadmap/<key>.md       # /sc:validate-roadmap subfolder
- `docs/developer-guide/session-memory.md:60`  Subfolder keys follow the same split. For example, `/sc:reflect` overwrites `reflect/last-pass-{slug}.md` whole and writes `reflect/handoff-{slug}-{timestamp}.md` once (`...
- `docs/developer-guide/session-memory.md:81`  \| `sc-validate-roadmap-protocol` \| Reads and writes ledger, terminology and pattern files under `validate-roadmap/`; every read and write is fail-open \| `sc-validate-r...

### `docs/generated/contributor-knowledge-base/architecture-guide.md`
Change: Doc: remove or reword the mention.

- `docs/generated/contributor-knowledge-base/architecture-guide.md:256`  - `sc-roadmap-protocol/`

### `docs/generated/contributor-knowledge-base/cli-api-inventory.md`
Change: Doc: remove or reword the mention.

- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:57`  \| `superclaude sprint ...` \| `sprint_group` added via `main.add_command(...)` \| `src/superclaude/cli/sprint/` \| Multi-phase sprint execution workflow. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:58`  \| `superclaude roadmap ...` \| `roadmap_group` added via `main.add_command(...)` \| `src/superclaude/cli/roadmap/` \| Roadmap generation and validation workflow. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:80`  Implements the `superclaude sprint` command group for orchestrating multi-phase Claude Code sprint execution.
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:86`  \| `sprint_group` \| `src/superclaude/cli/sprint/commands.py` \| Click subcommand group, re-exported by `src/superclaude/cli/sprint/__init__.py`. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:92`  \| `superclaude sprint run` \| `run` \| Loads sprint config, discovers phases, and either dry-runs, launches in tmux, or executes directly. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:93`  \| `superclaude sprint attach` \| `attach` \| Reattaches to a running sprint tmux session. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:94`  \| `superclaude sprint status` \| `status` \| Reads sprint execution status from logs. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:95`  \| `superclaude sprint logs` \| `logs` \| Tails the sprint execution log, optionally following output. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:96`  \| `superclaude sprint kill` \| `kill` \| Stops a running sprint, with optional force mode. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:102`  \| `commands.py` \| `sprint_group`, `run`, `attach`, `status`, `logs`, `kill`, `_print_dry_run` \| User-facing CLI layer. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:116`  Implements the `superclaude roadmap` command group. Current code describes this as an 8-step roadmap generation pipeline built on the shared `pipeline/` foundation, with ...
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:122`  \| `roadmap_group` \| `src/superclaude/cli/roadmap/commands.py` \| Click subcommand group, re-exported by `src/superclaude/cli/roadmap/__init__.py`. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:128`  \| `superclaude roadmap run` \| `run` \| Parses agent specs, builds `RoadmapConfig`, and executes the roadmap pipeline. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:129`  \| `superclaude roadmap validate` \| `validate` \| Builds `ValidateConfig`, runs validation, and prints blocking/warning/info counts. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:135`  \| `commands.py` \| `roadmap_group`, `run`, `validate` \| CLI entry layer for roadmap flows. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:141`  \| `__init__.py` \| `roadmap_group` \| Public export surface. \|
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:250`  - `src/superclaude/cli/sprint/commands.py`, or
- `docs/generated/contributor-knowledge-base/cli-api-inventory.md:251`  - `src/superclaude/cli/roadmap/commands.py`

### `docs/generated/contributor-knowledge-base/components-guide.md`
Change: Doc: remove or reword the mention.

- `docs/generated/contributor-knowledge-base/components-guide.md:36`  #### `src/superclaude/cli/sprint/`
- `docs/generated/contributor-knowledge-base/components-guide.md:50`  #### `src/superclaude/cli/roadmap/`

### `docs/generated/contributor-knowledge-base/visual-architecture-summary.md`
Change: Doc: remove or reword the mention.

- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:24`  - [Release pipeline (`/sc:roadmap`)](#release-pipeline-scroadmap)
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:274`  I --> I1[src/superclaude/cli/sprint/]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:279`  J --> J1[src/superclaude/cli/roadmap/]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:302`  C1[/sc:roadmap]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:303`  C2[/sc:tasklist]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:313`  S1[sc:roadmap-protocol]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:314`  S2[sc:tasklist-protocol]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:337`  ## Release pipeline (`/sc:roadmap`)
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:339`  The default planning route is not this pipeline: for a full specification it is `/prd`, then `/tdd`, then `/roadmap`, then `/task` on each phase task file; see [How We Wo...
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:343`  A["Specification file(s)"] --> B["/sc:roadmap"]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:344`  B --> C[sc:roadmap-protocol]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:355`  D --> E["/sc:tasklist"]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:356`  E --> F[sc:tasklist-protocol]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:357`  F --> G[tasklist-index.md + phase-N-tasklist.md bundle]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:359`  G --> H["superclaude sprint run tasklist-index.md"]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:367`  `sc:roadmap-protocol` can call `sc:adversarial-protocol` in two different places: for multi-spec consolidation and for multi-roadmap generation.
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:371`  A[/sc:roadmap] --> B[sc:roadmap-protocol]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:421`  `/sc:tasklist` and `/sc:task` should be understood as adjacent but distinct compliance surfaces. If contributors change task tier logic, they should think about both the ...
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:425`  A[roadmap.md] --> B[/sc:tasklist]
- `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:426`  B --> C[sc:tasklist-protocol]

### `docs/getting-started/upgrading.md`
Change: Doc: remove or reword the mention.

- `docs/getting-started/upgrading.md:263`  \| `superclaude sprint run <index>` in CI \| With no `--start`/`--end` it auto-resumes and asks for confirmation. Add `--yes` (or set `CI=1`), or pass `--start 1` for the...

### `docs/guides/RELEASE-GUIDE-INSTRUCTIONS.md`
Change: Doc: remove or reword the mention.

- `docs/guides/RELEASE-GUIDE-INSTRUCTIONS.md:11`  - A new CLI subcommand group ships (e.g., `superclaude roadmap`, `superclaude sprint`)

### `docs/guides/prd-skill-release-guide.md`
Change: Doc: remove or reword the mention.

- `docs/guides/prd-skill-release-guide.md:519`  Run the phase task files one at a time, in the order the roadmap run printed. Before starting the next phase, open the task file and read its `reflect_post` entry (the fi...
- `docs/guides/prd-skill-release-guide.md:540`  The CLI pipeline (`superclaude roadmap run` -> `/sc:tasklist` -> `superclaude sprint run`) is a separate release pipeline; see [roadmap-cli-tools-release-guide.md](roadma...

### `docs/guides/reflect-cli-tools-guide.md`
Change: Doc: remove or reword the mention.

- `docs/guides/reflect-cli-tools-guide.md:444`  ### O2 — per-phase (sc:tasklist end-of-phase gate)

### `docs/guides/suites-guide.md`
Change: Doc: remove or reword the mention.

- `docs/guides/suites-guide.md:48`  \| 7 \| `tasklist_deterministic_shape` \| 1 \| One-off baseline \| `/sc:tasklist` shape contract + renumbering \|
- `docs/guides/suites-guide.md:262`  ### 7. `tasklist_deterministic_shape.yaml` — `/sc:tasklist` shape contract
- `docs/guides/suites-guide.md:265`  gap) produces a canonical Sprint-compatible bundle: `tasklist-index.md` +
- `docs/guides/suites-guide.md:269`  **1 eval (E1):** invokes `/sc:tasklist @<seeded>/roadmap.md` and asserts
- `docs/guides/suites-guide.md:279`  `.claude/skills/sc-tasklist-protocol/**`. `timeout_sec: 600` (LLM-heavy).

### `docs/guides/tdd-skill-release-guide.md`
Change: Doc: remove or reword the mention.

- `docs/guides/tdd-skill-release-guide.md:541`  Run the phase task files one at a time, in the order the roadmap run printed. Before starting the next phase, open the task file and read its `reflect_post` entry (the fi...
- `docs/guides/tdd-skill-release-guide.md:562`  The CLI pipeline (`superclaude roadmap run` -> `/sc:tasklist` -> `superclaude sprint run`) is a separate release pipeline; see [roadmap-cli-tools-release-guide.md](roadma...

### `docs/onboarding/ironclaude-onboarding.html`
Change: Doc: remove or reword the mention.

- `docs/onboarding/ironclaude-onboarding.html:564`  <tr><td><code>/roadmap</code></td><td><code>/sc:roadmap</code></td></tr>

### `docs/reference/deviation-report-format.md`
Change: Doc: remove or reword the mention.

- `docs/reference/deviation-report-format.md:105`  \| Defined by \| Prompt builders `build_spec_fidelity_prompt` in `src/superclaude/cli/roadmap/prompts.py` and `build_tasklist_fidelity_prompt` in `src/superclaude/cli/tas...
- `docs/reference/deviation-report-format.md:106`  \| Checked by \| `_high_severity_count_zero` and `_tasklist_ready_consistent` in `src/superclaude/cli/roadmap/gates.py` (reused by `src/superclaude/cli/tasklist/gates.py`...

### `docs/reference/diagnostic-reference.md`
Change: Doc: remove or reword the mention.

- `docs/reference/diagnostic-reference.md:314`  - **CLI pipelines**: `superclaude sprint`, `superclaude roadmap` and the other pipeline commands start `claude` subprocesses, which call the model API over the network

### `docs/reference/model-aliases.md`
Change: Doc: remove or reword the mention.

- `docs/reference/model-aliases.md:61`  - **Sprint alternate-model suggestion.** Given the alias `opus`, `suggest_alternate_model` returns `sonnet` when the two slots hold different ids (`src/superclaude/cli/sp...
- `docs/reference/model-aliases.md:62`  - **Roadmap names.** Step ids such as `generate-opus-architect` (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md` line 114) and the `/sc:recommend` eval model lists ...

### `docs/user-guide/brainstorm.md`
Change: Doc: remove or reword the mention.

- `docs/user-guide/brainstorm.md:16`  \| Handoff \| Text suggestion only \| Flag-gated invocation of `/sc:design`, `/sc:tasklist`, or `/task-builder` \|
- `docs/user-guide/brainstorm.md:67`  - `--handoff task` requires `task-builder` skill; `--handoff tasklist` requires `sc-tasklist-protocol`. Brainstorm STOPs rather than silently downgrading.
- `docs/user-guide/brainstorm.md:76`  6. **Wave 4 — Handoff (flag-gated)**: invoke `/sc:tasklist` or `/task-builder`, or print text recommendation for `/sc:design`.
- `docs/user-guide/brainstorm.md:132`  Codebase + research enrichment; 5 proposals × 3 models; deep debate; merged requirements feed `sc:tasklist` invocation.
- `docs/user-guide/brainstorm.md:173`  \| `tasklist` \| Invoke `Skill sc-tasklist-protocol` with `merged-requirements.md` \| `sc-tasklist-protocol` \|
- `docs/user-guide/brainstorm.md:187`  \| `/sc:tasklist` \| Wave 4 invoked handoff \|
- `docs/user-guide/brainstorm.md:226`  ├── tasklist  → invoke /sc:tasklist

### `docs/user-guide/codegraph.md`
Change: Doc: remove or reword the mention.

- `docs/user-guide/codegraph.md:120`  - **Ask codegraph first, Grep/Read as fallback:** `/sc:troubleshoot`, `/sc:reflect`, `/sc:validate-roadmap`, `/sc:brainstorm`, `/sc:cleanup-audit`, `/sc:auggie-review`, `...

### `docs/user-guide/commands.md`
Change: Doc: remove or reword the mention.

- `docs/user-guide/commands.md:42`  \| `/sc:roadmap` \| Roadmap artifacts from spec, TDD, PRD \| `roadmap.md` \| Report only \|
- `docs/user-guide/commands.md:43`  \| `/sc:tasklist` \| Sprint-ready tasklist bundles from roadmaps \| `tasklist.md` \| Report only \|
- `docs/user-guide/commands.md:73`  \| `/sc:validate-roadmap` \| Validate roadmap pipeline outputs \| `validate-roadmap.md` \| Report only \|
- `docs/user-guide/commands.md:548`  ### `/sc:roadmap` - Roadmap Generator
- `docs/user-guide/commands.md:550`  **When to use:** Generate roadmap pipeline artifacts from one to three markdown inputs (spec, TDD and/or PRD), mirroring the `superclaude roadmap run` CLI. It does not ge...
- `docs/user-guide/commands.md:555`  /sc:roadmap [OPTIONS] INPUT_FILES...
- `docs/user-guide/commands.md:576`  /sc:roadmap spec.md tdd.md prd.md --output .dev/releases/current/example-release/
- `docs/user-guide/commands.md:577`  /sc:roadmap spec.md --dry-run
- `docs/user-guide/commands.md:667`  ### `/sc:tasklist` - Tasklist Generator
- `docs/user-guide/commands.md:669`  **When to use:** Turn a roadmap into a deterministic, Sprint CLI-compatible tasklist bundle and validate it against the source roadmap. It does not modify the roadmap or ...
- `docs/user-guide/commands.md:674`  /sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]
- `docs/user-guide/commands.md:714`  ### `/sc:validate-roadmap` - Roadmap Pipeline Output Validator
- `docs/user-guide/commands.md:716`  **When to use:** Validate the `roadmap.md`, `test-strategy.md` and `extraction.md` produced by a prior `superclaude roadmap run`, with single-agent reflection or, for two...
- `docs/user-guide/commands.md:721`  /sc:validate-roadmap <roadmap-path> --specs <spec1.md,spec2.md,...> [options]
- `docs/user-guide/commands.md:724`  The command hands its arguments to the `sc-validate-roadmap-protocol` skill, which needs the roadmap file and the spec files it was built from. It is a read-only audit an...
- `docs/user-guide/commands.md:743`  /sc:validate-roadmap .dev/releases/current/v2/roadmap.md --specs docs/specs/billing-tdd.md
- `docs/user-guide/commands.md:744`  /sc:validate-roadmap ./roadmap.md --specs spec-a.md,spec-b.md --depth deep
- `docs/user-guide/commands.md:828`  - Optionally hands off to `/sc:design`, `/sc:tasklist`, or `/task-builder`

### `docs/user-guide/flags.md`
Change: Doc: remove or reword the mention.

- `docs/user-guide/flags.md:239`  \| `--dry-run` \| `superclaude mcp --dry-run`, `superclaude sprint run ... --dry-run` \| Show what would happen without doing it \|
- `docs/user-guide/flags.md:242`  \| `--resume <task_id>` \| `superclaude sprint run ... --resume <task_id>` \| Resume from a task id, skipping tasks that already passed \|
- `docs/user-guide/flags.md:243`  \| `--task-parallelism K` \| `superclaude sprint run ... --task-parallelism K` \| Run K tasks of a phase at once (default `1`, sequential) \|
- `docs/user-guide/flags.md:244`  \| `--handoff` / `--no-handoff` \| `superclaude sprint run ...` \| Turn per-task handoff records on (default) or off \|
- `docs/user-guide/flags.md:245`  \| `--yes` / `-y` \| `superclaude sprint run ... --yes`, `superclaude sprint rerun-tasks ... --yes` \| Answer yes to the sprint confirmation prompts; on `sprint run` it a...

### `docs/user-guide/session-management.md`
Change: Doc: remove or reword the mention.

- `docs/user-guide/session-management.md:12`  - Some skills (`/sc:task`, `/sc:reflect`, `/sc:validate-roadmap`) keep their own subfolders in the same store. The developer note [File-Based Session Memory](../developer...

### `plugins/superclaude/commands/brainstorm.md`
Change: Command text: remove the removed-command handoff or row.

- `plugins/superclaude/commands/brainstorm.md:71`  - `--handoff task` requires the task-builder skill installed; `--handoff tasklist` requires sc-tasklist-protocol
- `plugins/superclaude/commands/brainstorm.md:106`  Codebase + research enrichment; 5 proposals × 3 models; deep debate; merged requirements feed sc:tasklist invocation.
- `plugins/superclaude/commands/brainstorm.md:134`  6. Wave 4: flag-gated handoff to `/sc:design`, `/sc:tasklist`, or `/task-builder`
- `plugins/superclaude/commands/brainstorm.md:153`  - Hand off merged requirements to `/sc:design`, `/sc:tasklist`, or `/task-builder` (flag-gated)
- `plugins/superclaude/commands/brainstorm.md:174`  \| `/sc:tasklist` \| Handoff (invoked) \| `--handoff tasklist` invokes `Skill sc-tasklist-protocol` \|
- `plugins/superclaude/commands/brainstorm.md:200`  - `/sc:tasklist` for sprint planning

### `plugins/superclaude/commands/spec-panel.md`
Change: Command text: remove the removed-command handoff or row.

- `plugins/superclaude/commands/spec-panel.md:36`  6b. **Downstream Roadmap Frontmatter** (conditional — output intended for sc:roadmap): If the user's intent is to feed the output into sc:roadmap (indicated by user instr...
- `plugins/superclaude/commands/spec-panel.md:38`  6d. **Downstream Roadmap Frontmatter for PRD** (conditional — PRD output intended for sc:roadmap): Ensure the output document contains: `spec_type: "product-requirements"...
- `plugins/superclaude/commands/spec-panel.md:403`  \| SP-4 (Quantity Flow Diagram) \| `sc:roadmap` RM-3 \| Risk input \| Dimensional mismatches inform risk-weighted roadmap prioritization \|
- `plugins/superclaude/commands/spec-panel.md:404`  \| SP-2 (Whittaker Assumptions) \| `sc:roadmap` RM-2 \| Assumption input \| Identified assumptions feed roadmap assumption tracking \|

### `plugins/superclaude/commands/workflow.md`
Change: Command text: remove the removed-command handoff or row.

- `plugins/superclaude/commands/workflow.md:96`  **Will Not:** mutate product code; edit the plan from reflect findings; emit `tasklist-index.md`; run `superclaude roadmap`.
- `plugins/superclaude/commands/workflow.md:103`  \| `/sc:tasklist` \| Sprint bundle from a **roadmap** \|
- `plugins/superclaude/commands/workflow.md:104`  \| `/sc:roadmap` \| CLI spec → roadmap.md \|
- `plugins/superclaude/commands/workflow.md:109`  Plan only. Next: `/sc:implement .dev/tasks/to-do/<id>/<id>.md` (not MDTM `/task`) or `/sc:tasklist` on a roadmap.

### `plugins/superclaude/core/RULES.md`
Change: Remove or reword the mention.

- `plugins/superclaude/core/RULES.md:64`  ✅ **Right**: `superclaude sprint run --help` → confirm `--start` exists → recommend `--start 2`

### `plugins/superclaude/skills/sc-implement-protocol/SKILL.md`
Change: Remove or reword the mention.

- `plugins/superclaude/skills/sc-implement-protocol/SKILL.md:210`  - Generating the spec (`/sc:brainstorm`, `/sc:workflow`, `/sc:tasklist`)

### `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`
Change: Routing guide: remove rows/mentions. Both copies must stay byte-identical; core/CLAUDE.md level table re-copied.

- `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:256`  \| Release-pipeline roadmap artifacts \| Explicit `/sc:roadmap` intent retains supplied spec/TDD/PRD and output preferences. \| Contract gap: command's 1-3 positional Mar...
- `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:257`  \| Sprint-compatible tasklist bundle \| `/sc:tasklist <roadmap>` with optional spec/output. Input must be a readable non-empty roadmap; verify supplied spec and writable ...
- `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:258`  \| Roadmap fidelity audit \| Preserve roadmap and requirement sources, or the supplied pipeline output directory, according to the requested surface. \| Contract gap: `/s...
- `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:296`  \| `/roadmap` and `/sc:roadmap` \| `/roadmap` is the expressly selected or exceptionally justified MDTM composer: it uses task-builder/task internally and can produce pha...
- `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:381`  \| roadmap-artifacts \| explicitly requested release-pipeline sc:roadmap artifacts from supplied spec/TDD/PRD \| - \| 1. preserve explicit `/sc:roadmap` target, supplied ...
- `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:382`  \| sprint-tasklist-bundle \| existing roadmap to Sprint-compatible index and phase tasklist files \| - \| 1. `/sc:tasklist <roadmap-path>` with supplied spec/output<br>2....
- `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:383`  \| roadmap-fidelity \| investigative roadmap-versus-requirements fidelity audit or explicit pipeline-directory validation \| - \| 1. preserve roadmap/spec sources or supp...

### `plugins/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md`
Change: Remove or reword the mention.

- `plugins/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md:53`  Skills with large protocol bodies (`/sc:adversarial`, `/sc:roadmap`, `/sc:cleanup-audit`) cost real tokens just to load. For a small task, the loading cost dwarfs the wor...

### `plugins/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md`
Change: Remove or reword the mention.

- `plugins/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md:8`  \| `/sc:tasklist` \| print `/sc:tasklist <roadmap-path>` (positional roadmap file; only when a roadmap exists) \| pass `<id>.md` or any workflow plan as its input; print ...
- `plugins/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md:9`  \| `/sc:roadmap` \| INFO if source already looks like a roadmap \| run `superclaude roadmap` \|

### `scripts/dependency_baseline.txt`
Change: Script: remove the mention.

- `scripts/dependency_baseline.txt:71`  # tool-write JSON in src/superclaude/cli/roadmap/tool_writer.py (render_tool_output).

### `scripts/reflect_consumer_inventory.py`
Change: Script: remove the mention.

- `scripts/reflect_consumer_inventory.py:37`  sc-task-protocol, sc-tasklist-protocol and sc-workflow-protocol SKILL.md, task-builder SKILL.md with
- `scripts/reflect_consumer_inventory.py:39`  .dev/eval-workspaces/sc-reflect/grader.py, the sprint executor src/superclaude/cli/sprint/executor.py),
- `scripts/reflect_consumer_inventory.py:43`  src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md (the sc:tasklist row).
- `scripts/reflect_consumer_inventory.py:62`  repository (the meta-eval runs.jsonl aggregator and the sc:roadmap validation gate) are listed as UNVERIFIED;
- `scripts/reflect_consumer_inventory.py:148`  "src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md": (
- `scripts/reflect_consumer_inventory.py:150`  "section 9.3 sc:tasklist row (review fix): opens return-contract.yaml, "
- `scripts/reflect_consumer_inventory.py:170`  "src/superclaude/skills/sc-tasklist-protocol/SKILL.md": (
- `scripts/reflect_consumer_inventory.py:172`  "section 9.3 sc:tasklist gate",
- `scripts/reflect_consumer_inventory.py:178`  "src/superclaude/cli/sprint/executor.py": (
- `scripts/reflect_consumer_inventory.py:193`  "sc:roadmap validation gate (section 9.3)",

### `src/superclaude/agents/rf-qa.md`
Change: Remove or reword the mention.

- `src/superclaude/agents/rf-qa.md:337`  #### Structural Gate Additions (TB-Add-1, TB-Add-3 through TB-Add-8, imported from sc:tasklist 17-point gate per CB-3 per-check classification)
- `src/superclaude/agents/rf-qa.md:339`  These additions close specific structural gaps that sc:tasklist's pre-write gate catches but task-builder's task-integrity historically did not. Each cites its source che...
- `src/superclaude/agents/rf-qa.md:341`  21. **TB-Add-1: Placeholder scan (sc:tasklist check 11).** No checklist item contains the literal
- `src/superclaude/agents/rf-qa.md:347`  22. **TB-Add-3: Clarification adjacency (sc:tasklist check 14).** If the task has Open Questions, each blocked checklist item that depends on a question MUST reference th...
- `src/superclaude/agents/rf-qa.md:348`  23. **TB-Add-4: Circular dependency detection (sc:tasklist check 15).** Item-to-item dependencies form a DAG. No item depends (via Context/Action references) on a later i...
- `src/superclaude/agents/rf-qa.md:349`  24. **TB-Add-5: Granularity check / XL splitting (sc:tasklist check 16).** If an item is flagged as `complex`, `multi-file`, or otherwise XL (per item 10 atomicity), it m...
- `src/superclaude/agents/rf-qa.md:350`  25. **TB-Add-6: Confidence/Verification format consistency (sc:tasklist check 17).** All Verification fields use the same `Verify: ...` prefix; all Acceptance Criteria en...

### `src/superclaude/cli/eval/isolation.py`
Change: Remove or reword the mention.

- `src/superclaude/cli/eval/isolation.py:6`  ``superclaude.cli.sprint.executor``:
- `src/superclaude/cli/eval/isolation.py:19`  ``cli/sprint/executor.py`` is touched.

### `src/superclaude/cli/eval/reporter.py`
Change: Remove or reword the mention.

- `src/superclaude/cli/eval/reporter.py:29`  Pattern reference: ``src/superclaude/cli/sprint/executor.py:190-335``

### `src/superclaude/cli/install_skills.py`
Change: Remove or reword the mention.

- `src/superclaude/cli/install_skills.py:14`  named "sc-<command>-protocol" (e.g. sc-roadmap-protocol, backing commands/roadmap.md).

### `src/superclaude/cli/main.py`
Change: Remove the three deferred imports and `add_command` lines (sprint, roadmap, tasklist).

- `src/superclaude/cli/main.py:525`  from superclaude.cli.sprint import sprint_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
- `src/superclaude/cli/main.py:527`  main.add_command(sprint_group, name="sprint")
- `src/superclaude/cli/main.py:529`  from superclaude.cli.roadmap import roadmap_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
- `src/superclaude/cli/main.py:531`  main.add_command(roadmap_group, name="roadmap")
- `src/superclaude/cli/main.py:533`  from superclaude.cli.tasklist import tasklist_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
- `src/superclaude/cli/main.py:535`  main.add_command(tasklist_group, name="tasklist")

### `src/superclaude/cli/pipeline/combined_m2_pass.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/combined_m2_pass.py:11`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/conflict_detector.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/conflict_detector.py:12`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/conflict_review.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/conflict_review.py:6`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/contract_extractor.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/contract_extractor.py:13`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/dataflow_graph.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/dataflow_graph.py:14`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/dataflow_pass.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/dataflow_pass.py:14`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/diagnostic_chain.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/diagnostic_chain.py:16`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/executor.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/executor.py:7`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.
- `src/superclaude/cli/pipeline/executor.py:281`  # cli/roadmap/cosmetic_remediator.py). Activated when the consumer

### `src/superclaude/cli/pipeline/fmea_classifier.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/fmea_classifier.py:13`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/fmea_domains.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/fmea_domains.py:9`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/fmea_promotion.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/fmea_promotion.py:9`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/gates.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/gates.py:39`  ``cli/roadmap/*`` (NFR-007). When either is ``None`` and the criteria

### `src/superclaude/cli/pipeline/guard_analyzer.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/guard_analyzer.py:14`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/guard_pass.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/guard_pass.py:12`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/guard_resolution.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/guard_resolution.py:12`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/invariant_pass.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/invariant_pass.py:9`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/invariants.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/invariants.py:16`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/models.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/models.py:3`  This module has zero imports from superclaude.cli.sprint or
- `src/superclaude/cli/pipeline/models.py:4`  superclaude.cli.roadmap (NFR-007). All types here are generic pipeline
- `src/superclaude/cli/pipeline/models.py:18`  """Pluggable cosmetic-failure remediator (see cli/roadmap/cosmetic_remediator.py).
- `src/superclaude/cli/pipeline/models.py:111`  ``PipelineEnvelope`` (defined in ``cli/roadmap/envelope.py``) and a
- `src/superclaude/cli/pipeline/models.py:113`  ``Finding`` (defined in ``cli/roadmap/findings.py``) on FAIL with
- `src/superclaude/cli/pipeline/models.py:185`  auto-remediation lane (see ``cli/roadmap/cosmetic_remediator.py``) rewrote
- `src/superclaude/cli/pipeline/models.py:274`  etc. -- see ``cli/roadmap/cosmetic_remediator.py``), the output is

### `src/superclaude/cli/pipeline/mutation_inventory.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/mutation_inventory.py:9`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/process.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/process.py:9`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/state_detector.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/state_detector.py:15`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/pipeline/trailing_gate.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/trailing_gate.py:8`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.
- `src/superclaude/cli/pipeline/trailing_gate.py:245`  The sprint runner implements this protocol to build remediation steps

### `src/superclaude/cli/pipeline/verification_emitter.py`
Change: Comment only: the NFR-007 note names removed packages; reword to the generic rule.

- `src/superclaude/cli/pipeline/verification_emitter.py:11`  NFR-007: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.

### `src/superclaude/cli/recommend/commands.py`
Change: Remove or reword the mention.

- `src/superclaude/cli/recommend/commands.py:7`  ``superclaude --help`` fast, mirroring the ``cli/tasklist`` precedent

### `src/superclaude/cli/reflect/config.py`
Change: Comment only: 'No imports from cli.sprint/cli.roadmap' note; reword.

- `src/superclaude/cli/reflect/config.py:8`  - No imports from ``superclaude.cli.sprint`` or ``superclaude.cli.roadmap``.

### `src/superclaude/cli/reflect/models.py`
Change: Comment only: 'No imports from cli.sprint/cli.roadmap' note; reword.

- `src/superclaude/cli/reflect/models.py:9`  - No imports from ``superclaude.cli.sprint`` or ``superclaude.cli.roadmap``.

### `src/superclaude/cli/reflect/runner.py`
Change: Comment only: 'No imports from cli.sprint/cli.roadmap' note; reword.

- `src/superclaude/cli/reflect/runner.py:9`  - No imports from ``superclaude.cli.sprint`` or ``superclaude.cli.roadmap``.

### `src/superclaude/cli/swarm/__init__.py`
Change: Comment only: swarm docstring says it mirrors cli/sprint; reword (swarm stays).

- `src/superclaude/cli/swarm/__init__.py:9`  Module shape mirrors ``cli/sprint/`` (AC-003 / NFR-015) so operators
- `src/superclaude/cli/swarm/__init__.py:13`  cli/sprint/commands.py    -> cli/swarm/commands.py
- `src/superclaude/cli/swarm/__init__.py:14`  cli/sprint/config.py      -> cli/swarm/config.py
- `src/superclaude/cli/swarm/__init__.py:15`  cli/sprint/models.py      -> cli/swarm/models.py
- `src/superclaude/cli/swarm/__init__.py:16`  cli/sprint/logging_.py    -> cli/swarm/logging_.py
- `src/superclaude/cli/swarm/__init__.py:17`  cli/sprint/tmux.py        -> cli/swarm/tmux.py
- `src/superclaude/cli/swarm/__init__.py:18`  cli/sprint/tui.py         -> cli/swarm/tui.py
- `src/superclaude/cli/swarm/__init__.py:19`  cli/sprint/preflight.py   -> cli/swarm/preflight.py

### `src/superclaude/cli/swarm/config.py`
Change: Comment only: swarm docstring says it mirrors cli/sprint; reword (swarm stays).

- `src/superclaude/cli/swarm/config.py:5`  ``cli/sprint/config.py::SprintConfig`` but enforces ``frozen=True``

### `src/superclaude/cli/swarm/models.py`
Change: Comment only: swarm docstring says it mirrors cli/sprint; reword (swarm stays).

- `src/superclaude/cli/swarm/models.py:4`  swarm pipeline serializes. It mirrors ``cli/sprint/models.py`` in role.

### `src/superclaude/cli/swarm/tmux.py`
Change: Comment only: swarm docstring says it mirrors cli/sprint; reword (swarm stays).

- `src/superclaude/cli/swarm/tmux.py:3`  Mirrors ``cli/sprint/tmux.py`` in role: provide tmux session lifecycle

### `src/superclaude/cli/swarm/transports/__init__.py`
Change: Comment only: swarm docstring says it mirrors cli/sprint; reword (swarm stays).

- `src/superclaude/cli/swarm/transports/__init__.py:3`  Swarm-specific divergence from ``cli/sprint/`` (which shells out via

### `src/superclaude/commands/adversarial.md`
Change: Command text: remove the removed-command handoff or row.

- `src/superclaude/commands/adversarial.md:192`  \| `/sc:roadmap` \| Multi-spec/multi-roadmap modes \| `/sc:roadmap --specs spec1.md,spec2.md` \|
- `src/superclaude/commands/adversarial.md:195`  \| `/sc:tasklist` \| Pipeline output as sprint input \| Generate tasklist from pipeline merged output \|

### `src/superclaude/commands/brainstorm.md`
Change: Command text: remove the removed-command handoff or row.

- `src/superclaude/commands/brainstorm.md:74`  - `--handoff task` requires the task-builder skill installed; `--handoff tasklist` requires sc-tasklist-protocol
- `src/superclaude/commands/brainstorm.md:109`  Codebase + research enrichment; 5 proposals × 3 models; deep debate; merged requirements feed sc:tasklist invocation.
- `src/superclaude/commands/brainstorm.md:137`  6. Wave 4: flag-gated handoff to `/sc:design`, `/sc:tasklist`, or `/task-builder`
- `src/superclaude/commands/brainstorm.md:169`  - Hand off merged requirements to `/sc:design`, `/sc:tasklist`, or `/task-builder` (flag-gated)
- `src/superclaude/commands/brainstorm.md:190`  \| `/sc:tasklist` \| Handoff (invoked) \| `--handoff tasklist` invokes `Skill sc-tasklist-protocol` \|
- `src/superclaude/commands/brainstorm.md:216`  - `/sc:tasklist` for sprint planning

### `src/superclaude/commands/release-split.md`
Change: Command text: remove the removed-command handoff or row.

- `src/superclaude/commands/release-split.md:150`  \| `/sc:tasklist` \| Part 3 execution (tasklists) \| Produce tasklist bundles if appropriate \|

### `src/superclaude/commands/spec-panel.md`
Change: Command text: remove the removed-command handoff or row.

- `src/superclaude/commands/spec-panel.md:38`  6b. **Downstream Roadmap Frontmatter** (conditional — output intended for sc:roadmap): If the user's intent is to feed the output into sc:roadmap (indicated by user instr...
- `src/superclaude/commands/spec-panel.md:40`  6d. **Downstream Roadmap Frontmatter for PRD** (conditional — PRD output intended for sc:roadmap): Ensure the output document contains: `spec_type: "product-requirements"...
- `src/superclaude/commands/spec-panel.md:405`  \| SP-4 (Quantity Flow Diagram) \| `sc:roadmap` RM-3 \| Risk input \| Dimensional mismatches inform risk-weighted roadmap prioritization \|
- `src/superclaude/commands/spec-panel.md:406`  \| SP-2 (Whittaker Assumptions) \| `sc:roadmap` RM-2 \| Assumption input \| Identified assumptions feed roadmap assumption tracking \|

### `src/superclaude/commands/workflow.md`
Change: Command text: remove the removed-command handoff or row.

- `src/superclaude/commands/workflow.md:96`  **Will Not:** mutate product code; edit the plan from reflect findings; emit `tasklist-index.md`; run `superclaude roadmap`.
- `src/superclaude/commands/workflow.md:103`  \| `/sc:tasklist` \| Sprint bundle from a **roadmap** \|
- `src/superclaude/commands/workflow.md:104`  \| `/sc:roadmap` \| CLI spec → roadmap.md \|
- `src/superclaude/commands/workflow.md:109`  Plan only. Next: `/sc:implement .dev/tasks/to-do/<id>/<id>.md` (not MDTM `/task`) or `/sc:tasklist` on a roadmap.

### `src/superclaude/contracts/__init__.py`
Change: Remove or reword the mention.

- `src/superclaude/contracts/__init__.py:30`  ``cli/roadmap/fingerprint.py``, ``cli/roadmap/spec_structural_audit.py``,
- `src/superclaude/contracts/__init__.py:31`  and ``cli/roadmap/gates.py``.
- `src/superclaude/contracts/__init__.py:50`  #     extractor at `cli/roadmap/spec_parser.py:328` (Phase 2 D1 informational
- `src/superclaude/contracts/__init__.py:85`  # `cli/roadmap/fingerprint.py` / `spec_structural_audit.py`). R1.1 reconciles
- `src/superclaude/contracts/__init__.py:94`  "sc:roadmap": (0.7, 0.5),
- `src/superclaude/contracts/__init__.py:102`  # documented at `cli/roadmap/gates.py:18` (B-1).
- `src/superclaude/contracts/__init__.py:119`  #     `cli/roadmap/fingerprint.py:171,205` and `>= 0.7` literal at
- `src/superclaude/contracts/__init__.py:120`  #     `cli/roadmap/gates.py:375` (Phase 6 D3 finding — missed by Phase 4
- `src/superclaude/contracts/__init__.py:123`  #     `cli/roadmap/spec_structural_audit.py:91`.
- `src/superclaude/contracts/__init__.py:239`  # (``cli/roadmap/templates/tool_schemas/{extract,extract_tdd,generate,merge}``

### `src/superclaude/core/HOW-WE-WORK.md`
Change: Routing guide: remove rows/mentions. Both copies must stay byte-identical; core/CLAUDE.md level table re-copied.

- `src/superclaude/core/HOW-WE-WORK.md:256`  \| Release-pipeline roadmap artifacts \| Explicit `/sc:roadmap` intent retains supplied spec/TDD/PRD and output preferences. \| Contract gap: command's 1-3 positional Mar...
- `src/superclaude/core/HOW-WE-WORK.md:257`  \| Sprint-compatible tasklist bundle \| `/sc:tasklist <roadmap>` with optional spec/output. Input must be a readable non-empty roadmap; verify supplied spec and writable ...
- `src/superclaude/core/HOW-WE-WORK.md:258`  \| Roadmap fidelity audit \| Preserve roadmap and requirement sources, or the supplied pipeline output directory, according to the requested surface. \| Contract gap: `/s...
- `src/superclaude/core/HOW-WE-WORK.md:296`  \| `/roadmap` and `/sc:roadmap` \| `/roadmap` is the expressly selected or exceptionally justified MDTM composer: it uses task-builder/task internally and can produce pha...
- `src/superclaude/core/HOW-WE-WORK.md:381`  \| roadmap-artifacts \| explicitly requested release-pipeline sc:roadmap artifacts from supplied spec/TDD/PRD \| - \| 1. preserve explicit `/sc:roadmap` target, supplied ...
- `src/superclaude/core/HOW-WE-WORK.md:382`  \| sprint-tasklist-bundle \| existing roadmap to Sprint-compatible index and phase tasklist files \| - \| 1. `/sc:tasklist <roadmap-path>` with supplied spec/output<br>2....
- `src/superclaude/core/HOW-WE-WORK.md:383`  \| roadmap-fidelity \| investigative roadmap-versus-requirements fidelity audit or explicit pipeline-directory validation \| - \| 1. preserve roadmap/spec sources or supp...

### `src/superclaude/core/RULES.md`
Change: Routing guide: remove rows/mentions. Both copies must stay byte-identical; core/CLAUDE.md level table re-copied.

- `src/superclaude/core/RULES.md:64`  ✅ **Right**: `superclaude sprint run --help` → confirm `--start` exists → recommend `--start 2`

### `src/superclaude/examples/release-spec-template.md`
Change: Remove or reword the mention.

- `src/superclaude/examples/release-spec-template.md:228`  > What this spec feeds into. How downstream consumers (sc:roadmap, sc:tasklist, etc.) use the output.
- `src/superclaude/examples/release-spec-template.md:230`  ### For sc:roadmap
- `src/superclaude/examples/release-spec-template.md:234`  ### For sc:tasklist

### `src/superclaude/examples/tdd_template.md`
Change: Remove or reword the mention.

- `src/superclaude/examples/tdd_template.md:17`  complexity_score: ""      # 0.0-1.0 -- computed by sc:roadmap; provide estimated value if known
- `src/superclaude/examples/tdd_template.md:18`  complexity_class: ""      # LOW \| MEDIUM \| HIGH -- computed by sc:roadmap; provide estimated value if known
- `src/superclaude/examples/tdd_template.md:65`  - complexity_score and complexity_class: computed by sc:roadmap during extraction. Provide estimated values if known; the extraction step will compute authoritative value...
- `src/superclaude/examples/tdd_template.md:69`  - `complexity_score`, `complexity_class`: Computed by sc:roadmap during extraction (not read from frontmatter). Pre-populated values are advisory only.
- `src/superclaude/examples/tdd_template.md:71`  - `quality_scores`: Populated by sc:spec-panel review output. Not consumed by sc:roadmap.

### `src/superclaude/skills/roadmap/SKILL.md`
Change: Remove or reword the mention.

- `src/superclaude/skills/roadmap/SKILL.md:143`  \| State file \| `${TASK_DIR}.roadmap-state.json` \|
- `src/superclaude/skills/roadmap/SKILL.md:203`  a. Read `${TASK_DIR}.roadmap-state.json` (if it exists) and extract the stored `input_hash`
- `src/superclaude/skills/roadmap/SKILL.md:212`  6. Update `.roadmap-state.json` with the new input_hash and last_run timestamp
- `src/superclaude/skills/roadmap/SKILL.md:213`  e. If no `.roadmap-state.json` exists → treat as a fresh re-run (inform user, offer to re-generate from scratch or build on existing roadmap)
- `src/superclaude/skills/roadmap/SKILL.md:578`  - Compute SHA-256 hash of user input. Store in roadmap metadata and in `${TASK_DIR}.roadmap-state.json`.
- `src/superclaude/skills/roadmap/SKILL.md:579`  - Create/update `.roadmap-state.json` with: schema_version, input_hash, input_paths, created, last_run, roadmap_status, sections_populated, validation_status (obligation_...
- `src/superclaude/skills/roadmap/SKILL.md:590`  - After all BUILD_REQUESTs pass Stage 3, update `.roadmap-state.json` with `build_requests_generated: true`.
- `src/superclaude/skills/roadmap/SKILL.md:660`  - Each item: (1) invoke /task-builder with BUILD_REQUEST path, (2) receive created task file path, (3) update the roadmap's Task File Tracker (Section 6) with the task fi...
- `src/superclaude/skills/roadmap/SKILL.md:2484`  - [ ] Input hash computed and stored in metadata and `.roadmap-state.json`

### `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`
Change: Remove or reword the mention.

- `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:51`  - Integration: Called by `/sc:roadmap` in multi-spec/multi-roadmap modes
- `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:2090`  purpose: "Enable programmatic integration with other commands (sc:roadmap, sc:design)"

### `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
Change: Remove or reword the mention.

- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:40`  5. Optional handoff to `/sc:design`, `/sc:tasklist`, or `/task-builder`
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:108`  - If `--handoff task` AND `task-builder` skill missing → STOP: `"task-builder skill missing. Re-run with --handoff tasklist (if sc-tasklist-protocol installed) or --hando...
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:109`  - If `--handoff tasklist` AND `sc-tasklist-protocol` missing → STOP similarly
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:302`  2. **Invoke**: `Skill sc-adversarial-protocol` with above arguments. Direct skill invocation, not command — per sc:roadmap pattern.
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:315`  5. **Fallback protocol** (F1-F3 per sc:roadmap pattern):
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:332`  - **`none`** (default): Print summary table of artifacts. Suggest text-only next steps: `"Next: /sc:design @<output>/merged-requirements.md, or /sc:tasklist for sprint pl...
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:338`  2. Invoke `Skill sc-tasklist-protocol` with `--source <output>/merged-requirements.md`

### `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`
Change: Remove or reword the mention.

- `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:163`  - `/sc:tasklist @<output>/merged-requirements.md` — sprint planning
- `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:187`  **Invoke**: `Skill sc-tasklist-protocol` with arguments:

### `src/superclaude/skills/sc-crash-recovery/SKILL.md`
Change: Replace the removed-pipeline resume commands (kept skill).

- `src/superclaude/skills/sc-crash-recovery/SKILL.md:3`  description: Post-crash work-state recovery. Fans parallel subagents across pipeline artifacts (.dev/releases, manifest.json, execution-log.jsonl, .roadmap-state.json), r...
- `src/superclaude/skills/sc-crash-recovery/SKILL.md:65`  - recent `.roadmap-state.json` / `manifest.json` / `execution-log.jsonl` / `.sprint-exitcode` files
- `src/superclaude/skills/sc-crash-recovery/SKILL.md:116`  - **Roadmap** — `superclaude roadmap run` → `docs/generated/<...>/.roadmap-state.json` or `.dev/research/roadmap-*/`
- `src/superclaude/skills/sc-crash-recovery/SKILL.md:117`  - **Tasklist** — `superclaude tasklist` → multi-file bundle per release in `.dev/releases/current/<release>/phase-N-tasklist.md` + `tasklist-index.md`
- `src/superclaude/skills/sc-crash-recovery/SKILL.md:118`  - **Sprint (task execution)** — `superclaude sprint run` → `.dev/releases/current/<release>/manifest.json` + `execution-log.jsonl` + `.sprint-exitcode`

### `src/superclaude/skills/sc-crash-recovery/refs/investigators.md`
Change: Replace the removed-pipeline resume commands (kept skill).

- `src/superclaude/skills/sc-crash-recovery/refs/investigators.md:19`  - .dev/releases/current/*/ — sprint runs (look for manifest.json, execution-log.jsonl, .sprint-exitcode, tasklist-index.md, phase-*.md)
- `src/superclaude/skills/sc-crash-recovery/refs/investigators.md:24`  - docs/generated/*/ and any *.roadmap-state.json found in tree — roadmap runs
- `src/superclaude/skills/sc-crash-recovery/refs/investigators.md:35`  For roadmaps: read .roadmap-state.json and report per-step status.

### `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md`
Change: Replace the removed-pipeline resume commands (kept skill).

- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:52`  ## Roadmap pipeline (`superclaude roadmap run`)
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:54`  **Created by:** `superclaude roadmap run <spec.md>` CLI.
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:59`  ├── .roadmap-state.json           # AUTHORITATIVE state — step-by-step progress
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:68`  **Status signal:** `.roadmap-state.json` is the ground truth. Each step has a `status: pass \| fail \| pending` and an `attempts` counter. The CLI retries failed steps up...
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:73`  superclaude roadmap run <original-spec.md> --output <same-output-dir> --resume
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:81`  superclaude roadmap validate <output-dir>
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:84`  ## Tasklist pipeline (`superclaude tasklist`)
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:86`  **Created by:** `superclaude tasklist` from a roadmap.
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:91`  ├── tasklist-index.md             # entry point — lists all phase files
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:99`  **Status signal:** existence of phase files and checkpoint files. The presence of `tasklist-index.md` means generation succeeded; missing checkpoint files mean the sprint...
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:102`  ## Sprint pipeline (`superclaude sprint run`)
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:104`  **Created by:** `superclaude sprint run <tasklist-index.md>` CLI — executes the multi-phase tasklist.
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:122`  superclaude sprint run <release>/tasklist-index.md
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:125`  superclaude sprint run <release>/tasklist-index.md --yes
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:128`  superclaude sprint run <release>/tasklist-index.md --start 6 --end 6
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:131`  superclaude sprint run <release>/tasklist-index.md --fresh
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:144`  superclaude sprint rerun-tasks <release>/tasklist-index.md
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:147`  superclaude sprint rerun-tasks <release>/tasklist-index.md --phase 7 --tasks T07.11,T07.12
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:150`  superclaude sprint rerun-tasks <release>/tasklist-index.md --phase 7 --tasks T07.11,T07.12 --dry-run
- `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:156`  must be redone, use the bare `sprint run` auto-resume command or pass an explicit

### `src/superclaude/skills/sc-crash-recovery/refs/report-template.md`
Change: Replace the removed-pipeline resume commands (kept skill).

- `src/superclaude/skills/sc-crash-recovery/refs/report-template.md:84`  superclaude sprint run .dev/releases/current/<release>/tasklist-index.md
- `src/superclaude/skills/sc-crash-recovery/refs/report-template.md:90`  superclaude sprint run .dev/releases/current/<release>/tasklist-index.md --yes
- `src/superclaude/skills/sc-crash-recovery/refs/report-template.md:96`  superclaude sprint rerun-tasks .dev/releases/current/<release>/tasklist-index.md
- `src/superclaude/skills/sc-crash-recovery/refs/report-template.md:97`  superclaude sprint rerun-tasks .dev/releases/current/<release>/tasklist-index.md --phase <N> --tasks <task-ids>
- `src/superclaude/skills/sc-crash-recovery/refs/report-template.md:103`  superclaude sprint run .dev/releases/current/<release>/tasklist-index.md --fresh
- `src/superclaude/skills/sc-crash-recovery/refs/report-template.md:109`  superclaude roadmap validate docs/generated/<run-slug>

### `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh`
Change: Replace the removed-pipeline resume commands (kept skill).

- `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:137`  ROADMAP_STATES=$(recent_files ".roadmap-state.json" \| awk 'BEGIN{printf "["} {printf "%s\"%s\"", sep, $0; sep=","} END{printf "]"}')

### `src/superclaude/skills/sc-implement-protocol/SKILL.md`
Change: Remove or reword the mention.

- `src/superclaude/skills/sc-implement-protocol/SKILL.md:210`  - Generating the spec (`/sc:brainstorm`, `/sc:workflow`, `/sc:tasklist`)

### `src/superclaude/skills/sc-issue-protocol/refs/chains.md`
Change: Remove or reword the mention.

- `src/superclaude/skills/sc-issue-protocol/refs/chains.md:24`  No brainstorm step carries a handoff flag: the tasklist handoff feeds `/sc:tasklist`, not `/sc:workflow`, and the design handoff only prints a suggestion (B11), so `/sc:w...

### `src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md`
Change: Remove or reword the mention.

- `src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md:53`  Skills with large protocol bodies (`/sc:adversarial`, `/sc:roadmap`, `/sc:cleanup-audit`) cost real tokens just to load. For a small task, the loading cost dwarfs the wor...

### `src/superclaude/skills/sc-reflect-protocol/SKILL.md`
Change: Remove sprint/roadmap/tasklist consumer rows and mentions.

- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:998`  \| **`superclaude sprint run` (executor.py TurnLedger)** \| CLI consumer of return-contract.yaml \| `status`, `per_task_verdicts[].status`, `per_task_verdicts[].per_task_...
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1000`  \| **`sc:roadmap` validation gate** \| Roadmap pipeline post-step \| `status`, `coverage_pct`, `unmapped_requirements`, `best_practice_grade` \| `coverage_pct < 0.90 OR u...
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1001`  \| **`sc:tasklist` generator gate** \| Tasklist pipeline post-step \| `status`, `coverage_pct`, `unmapped_requirements`, `coverage_undefined` \| `coverage_undefined: true...
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1430`  1. **Eval-driven nature of the skill.** Reflection quality is judged by graders running on representative inputs; this is precisely what skill-creator 2.0 ships out of th...
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1443`  \| Production execution \| `superclaude sprint run` against tasklists that *use* sc-reflect \| Only after skill ships and is stable \|
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1446`  `superclaude sprint` is *not* the build path; it is the *execution* path for skills already built. Conflating the two is the trap.
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1520`  Reflect is the **final QA gate** between the executor and the archive. When UC-2 verification passes strictly, the validated work-unit folder moves from its in-progress l...

### `src/superclaude/skills/sc-release-split-protocol/SKILL.md`
Change: Remove or reword the mention.

- `src/superclaude/skills/sc-release-split-protocol/SKILL.md:35`  **Pipeline Position**: `release artifact → sc:release-split → split specs/tasklists + fidelity audit → (user decides) → sc:roadmap / sc:tasklist`
- `src/superclaude/skills/sc-release-split-protocol/SKILL.md:106`  Part 3: Execution                        → /sc:design \| /sc:workflow \| /sc:tasklist
- `src/superclaude/skills/sc-release-split-protocol/SKILL.md:226`  7. Apply convergence routing (aligned with sc:roadmap thresholds):
- `src/superclaude/skills/sc-release-split-protocol/SKILL.md:276`  \| Split approved, need tasklists \| Sprint planning \| `/sc:tasklist` \|
- `src/superclaude/skills/sc-release-split-protocol/SKILL.md:279`  **Do NOT** use `/sc:roadmap` or `/sc:tasklist` unless the approved proposal explicitly says they are appropriate at this stage. Default to `/sc:design` for producing rele...

### `src/superclaude/skills/sc-release-split-protocol/refs/adversarial-integration.md`
Change: Remove or reword the mention.

- `src/superclaude/skills/sc-release-split-protocol/refs/adversarial-integration.md:112`  Thresholds aligned with sc:roadmap for cross-skill consistency:

### `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
Change: Remove the `sprint rerun-tasks` hint.

- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:525`  **Sprint-failure recovery hint.** When the diagnosed target is a `superclaude sprint run` phase that failed on a *subset* of its tasks from a transient cause (API outage,...

### `src/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md`
Change: Remove or reword the mention.

- `src/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md:8`  \| `/sc:tasklist` \| print `/sc:tasklist <roadmap-path>` (positional roadmap file; only when a roadmap exists) \| pass `<id>.md` or any workflow plan as its input; print ...
- `src/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md:9`  \| `/sc:roadmap` \| INFO if source already looks like a roadmap \| run `superclaude roadmap` \|

### `src/superclaude/skills/task-builder/SKILL.md`
Change: Remove or reword the mention.

- `src/superclaude/skills/task-builder/SKILL.md:1395`  Structural Gate Additions (TB-Add-1, TB-Add-3 through TB-Add-8, imported from sc:tasklist 17-point pre-write gate per CB-3 per-check classification, see rf-qa agent defin...
- `src/superclaude/skills/task-builder/SKILL.md:1670`  **Invoke reflect directly.** Invoke the `sc:reflect-protocol` skill DIRECTLY from this task-builder context (this is task-builder's OWN pre-execution advisory gate, run b...

### `src/superclaude/templates/documents/release-spec-template.md`
Change: Remove or reword the mention.

- `src/superclaude/templates/documents/release-spec-template.md:226`  > What this spec feeds into. How downstream consumers (sc:roadmap, sc:tasklist, etc.) use the output.
- `src/superclaude/templates/documents/release-spec-template.md:228`  ### For sc:roadmap
- `src/superclaude/templates/documents/release-spec-template.md:231`  ### For sc:tasklist

### `tests/cli/eval/test_home_isolation_extend.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/cli/eval/test_home_isolation_extend.py:520`  ``cli/sprint/executor.IsolationLayers`` shape. Re-import the probe
- `tests/cli/eval/test_home_isolation_extend.py:542`  from superclaude.cli.sprint.executor import IsolationLayers

### `tests/cli/eval/test_single_command.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/cli/eval/test_single_command.py:35`  ``pytest.skip`` with the missing-dependency reason so a sprint runner

### `tests/cli/reflect/test_no_nesting_guard.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/cli/reflect/test_no_nesting_guard.py:39`  # ("No imports from ``superclaude.cli.sprint``") never false-positives.
- `tests/cli/reflect/test_no_nesting_guard.py:128`  """AC-8: NO cli.sprint / cli.roadmap import in any cli/reflect/*.py (NFR-1)."""

### `tests/commands/test_workflow_command.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/commands/test_workflow_command.py:231`  assert "/sc:tasklist <roadmap-path>" in usage and "--source" not in usage
- `tests/commands/test_workflow_command.py:235`  if line.startswith("\| `/sc:tasklist`")
- `tests/commands/test_workflow_command.py:238`  assert "`/sc:tasklist <roadmap-path>`" in do

### `tests/core/test_how_we_work_routing_table.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/core/test_how_we_work_routing_table.py:301`  "sc:validate-roadmap",
- `tests/core/test_how_we_work_routing_table.py:706`  {"sc:roadmap"},
- `tests/core/test_how_we_work_routing_table.py:713`  {"sc:tasklist"},
- `tests/core/test_how_we_work_routing_table.py:725`  {"sc:validate-roadmap"},

### `tests/hooks/test_launch_level_guard.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/hooks/test_launch_level_guard.py:937`  "name", ["sc:cleanup-audit-protocol", "task-builder", "sc:tasklist-protocol"]

### `tests/pipeline/test_full_flow.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/pipeline/test_full_flow.py:39`  from superclaude.cli.sprint.models import (
- `tests/pipeline/test_full_flow.py:345`  from superclaude.cli.sprint.executor import (  # noqa: E402  # late import for test section grouping
- `tests/pipeline/test_full_flow.py:349`  from superclaude.cli.sprint.models import (  # noqa: E402  # late import for test section grouping
- `tests/pipeline/test_full_flow.py:354`  from superclaude.cli.sprint.models import (  # noqa: E402  # late import for test section grouping
- `tests/pipeline/test_full_flow.py:357`  from superclaude.cli.sprint.models import (  # noqa: E402  # late import for test section grouping
- `tests/pipeline/test_full_flow.py:360`  from superclaude.cli.sprint.models import (  # noqa: E402  # late import for test section grouping
- `tests/pipeline/test_full_flow.py:472`  from superclaude.cli.sprint.executor import run_post_task_wiring_hook  # noqa: E402,I001  # late import for wiring section grouping

### `tests/pipeline/test_process.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/pipeline/test_process.py:243`  from superclaude.cli.sprint.models import Phase, SprintConfig, TaskEntry
- `tests/pipeline/test_process.py:247`  index = tmp_path / "tasklist-index.md"

### `tests/pipeline/test_trailing_gate.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/pipeline/test_trailing_gate.py:558`  from superclaude.cli.sprint.executor import SprintGatePolicy
- `tests/pipeline/test_trailing_gate.py:559`  from superclaude.cli.sprint.models import SprintConfig
- `tests/pipeline/test_trailing_gate.py:567`  from superclaude.cli.sprint.executor import SprintGatePolicy
- `tests/pipeline/test_trailing_gate.py:568`  from superclaude.cli.sprint.models import SprintConfig
- `tests/pipeline/test_trailing_gate.py:585`  from superclaude.cli.sprint.executor import SprintGatePolicy
- `tests/pipeline/test_trailing_gate.py:586`  from superclaude.cli.sprint.models import SprintConfig
- `tests/pipeline/test_trailing_gate.py:606`  from superclaude.cli.sprint.executor import SprintGatePolicy
- `tests/pipeline/test_trailing_gate.py:607`  from superclaude.cli.sprint.models import SprintConfig

### `tests/recommend/fixtures/routing_refresh_cases.json`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/recommend/fixtures/routing_refresh_cases.json:233`  "negative": {"competitors": ["sc:roadmap", "roadmap", "sc:implement"], "must_not": "automatic roadmap/product execution or a forced split"},
- `tests/recommend/fixtures/routing_refresh_cases.json:268`  "request": "Use /sc:roadmap to produce release-pipeline roadmap artifacts from {fixture:spec} and {fixture:tdd}.",
- `tests/recommend/fixtures/routing_refresh_cases.json:271`  "targets": ["sc:roadmap"],
- `tests/recommend/fixtures/routing_refresh_cases.json:280`  "activation": {"sc:roadmap": "sc:roadmap-protocol"},
- `tests/recommend/fixtures/routing_refresh_cases.json:283`  "unavailable_plugin": {"environment": "plugin-only", "missing": "sc:roadmap", "expected": "not installed: sc:roadmap; no substitution by /roadmap"},
- `tests/recommend/fixtures/routing_refresh_cases.json:292`  "targets": ["sc:tasklist"],
- `tests/recommend/fixtures/routing_refresh_cases.json:301`  "activation": {"sc:tasklist": "sc:tasklist-protocol"},
- `tests/recommend/fixtures/routing_refresh_cases.json:304`  "unavailable_plugin": {"environment": "plugin-only", "missing": "sc:tasklist", "expected": "not installed: sc:tasklist; no substitution by task-builder"},
- `tests/recommend/fixtures/routing_refresh_cases.json:313`  "targets": ["sc:validate-roadmap"],
- `tests/recommend/fixtures/routing_refresh_cases.json:322`  "activation": {"sc:validate-roadmap": "sc-validate-roadmap-protocol"},
- `tests/recommend/fixtures/routing_refresh_cases.json:325`  "unavailable_plugin": {"environment": "plugin-only", "missing": "sc:validate-roadmap", "expected": "not installed: sc:validate-roadmap; no substitution by sc:reflect"},
- `tests/recommend/fixtures/routing_refresh_cases.json:690`  {"name": "validate-roadmap", "history": "Active; M+D+F", "disposition": "CHANGE", "requirements_tests": "FR-04/05; S16/T45/T74", "report": "analyses/validate-roadmap.md"}...

### `tests/recommend/test_routing_refresh.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/recommend/test_routing_refresh.py:620`  assert "/sc:tasklist --source" not in _GUIDE.read_text(encoding="utf-8")

### `tests/review/test_reflect_consumer_inventory.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/review/test_reflect_consumer_inventory.py:44`  root, "src/superclaude/skills/sc-roadmap-protocol/SKILL.md", "merge_method\n"
- `tests/review/test_reflect_consumer_inventory.py:89`  assert inv.classify("src/superclaude/cli/sprint/executor.py")[0] == "consumer"
- `tests/review/test_reflect_consumer_inventory.py:102`  "src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md"
- `tests/review/test_reflect_consumer_inventory.py:117`  inv.classify("src/superclaude/skills/sc-roadmap-protocol/SKILL.md")[0]
- `tests/review/test_reflect_consumer_inventory.py:139`  rows["src/superclaude/skills/sc-roadmap-protocol/SKILL.md"][0] == "not in scope"
- `tests/review/test_reflect_consumer_inventory.py:307`  assert "\| `src/superclaude/cli/sprint/executor.py` \| consumer \|" in text

### `tests/skills/fixtures/review_severity_sweep_edits.yaml`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/skills/fixtures/review_severity_sweep_edits.yaml:29`  #   tasklist       sc-tasklist-protocol Stages 8-10: Low findings are notes; open High/Medium findings HALT at the cap (B3-10)
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:961`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:969`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:977`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:985`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:993`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:1001`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:1009`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:1017`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:1025`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:1033`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:1041`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md
- `tests/skills/fixtures/review_severity_sweep_edits.yaml:1049`  file: src/superclaude/skills/sc-tasklist-protocol/SKILL.md

### `tests/skills/test_codegraph_adoption.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/skills/test_codegraph_adoption.py:3`  Pins the codegraph tier placed above each Phase 1 Grep/Read floor in validate-roadmap,
- `tests/skills/test_codegraph_adoption.py:18`  _VR_SKILL = _SRC / "skills" / "sc-validate-roadmap-protocol" / "SKILL.md"
- `tests/skills/test_codegraph_adoption.py:19`  _VR_CMD = _SRC / "commands" / "validate-roadmap.md"
- `tests/skills/test_codegraph_adoption.py:27`  _TASKLIST_SKILL = _SRC / "skills" / "sc-tasklist-protocol" / "SKILL.md"

### `tests/skills/test_primitive_dual_surface_lookup.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/skills/test_primitive_dual_surface_lookup.py:19`  "sc-roadmap-protocol/SKILL.md",
- `tests/skills/test_primitive_dual_surface_lookup.py:20`  "sc-roadmap-protocol/refs/adversarial-integration.md",

### `tests/skills/test_task_builder_merge.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/skills/test_task_builder_merge.py:28`  # RFMerger P3: the sc-tasklist-protocol generator reuses (mirrors) the DM-003
- `tests/skills/test_task_builder_merge.py:31`  REPO_ROOT / "src" / "superclaude" / "skills" / "sc-tasklist-protocol" / "SKILL.md"
- `tests/skills/test_task_builder_merge.py:131`  # Every TB-Add cites the originating sc:tasklist check ID for traceability.
- `tests/skills/test_task_builder_merge.py:134`  # "check 13" (TB-Add-2's sc:tasklist source) dropped with the
- `tests/skills/test_task_builder_merge.py:142`  f"rf-qa.md missing source-check traceability for sc:tasklist {source_check}"
- `tests/skills/test_task_builder_merge.py:548`  """RFMerger P3: the sc-tasklist-protocol generator's Stage-7 synthetic-dnsp
- `tests/skills/test_task_builder_merge.py:570`  (the source contract at :1066,:1231) AND sc-tasklist-protocol/SKILL.md (the P1
- `tests/skills/test_task_builder_merge.py:588`  f"sc-tasklist-protocol/SKILL.md missing Execution Context sub-field "

### `tests/skills/test_worker_contract.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/skills/test_worker_contract.py:760`  "tasklist-index.md",

### `tests/swarm/test_module_shape.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/swarm/test_module_shape.py:1`  """T01.07 — Structural mapping: ``cli/swarm/`` mirrors ``cli/sprint/``.
- `tests/swarm/test_module_shape.py:11`  cli/sprint/__init__.py    -> cli/swarm/__init__.py
- `tests/swarm/test_module_shape.py:12`  cli/sprint/commands.py    -> cli/swarm/commands.py
- `tests/swarm/test_module_shape.py:13`  cli/sprint/config.py      -> cli/swarm/config.py
- `tests/swarm/test_module_shape.py:14`  cli/sprint/models.py      -> cli/swarm/models.py
- `tests/swarm/test_module_shape.py:15`  cli/sprint/logging_.py    -> cli/swarm/logging_.py
- `tests/swarm/test_module_shape.py:16`  cli/sprint/tmux.py        -> cli/swarm/tmux.py
- `tests/swarm/test_module_shape.py:17`  cli/sprint/tui.py         -> cli/swarm/tui.py
- `tests/swarm/test_module_shape.py:18`  cli/sprint/preflight.py   -> cli/swarm/preflight.py
- `tests/swarm/test_module_shape.py:160`  f"  Missing in cli/sprint/: {missing_in_sprint or 'none'}\n"

### `tests/troubleshoot/backtest/git_replay.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/troubleshoot/backtest/git_replay.py:3`  Mirrors the ``src/superclaude/cli/sprint/process.py`` subprocess seam: ``subprocess`` is

### `tests/unit/test_cli_doctor.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/unit/test_cli_doctor.py:50`  _write_command(commands_dir, "roadmap", "sc:roadmap-protocol")
- `tests/unit/test_cli_doctor.py:52`  _write_skill(skills_dir, "sc-roadmap-protocol")

### `tests/unit/test_cli_install.py`
Change: Test: remove the cases or fixtures that name the removed item (kept file).

- `tests/unit/test_cli_install.py:35`  from superclaude.cli.roadmap.templates import get_template_path
- `tests/unit/test_cli_install.py:119`  task.md tasklist.md tdd.md test.md troubleshoot.md validate-roadmap.md
- `tests/unit/test_cli_install.py:284`  sc-roadmap-protocol/SKILL.md
- `tests/unit/test_cli_install.py:285`  sc-roadmap-protocol/__init__.py sc-roadmap-protocol/refs/adversarial-integration.md
- `tests/unit/test_cli_install.py:286`  sc-roadmap-protocol/refs/extraction-pipeline.md sc-roadmap-protocol/refs/scoring.md
- `tests/unit/test_cli_install.py:287`  sc-roadmap-protocol/refs/templates.md sc-roadmap-protocol/refs/validation.md
- `tests/unit/test_cli_install.py:292`  sc-task-protocol/__init__.py sc-tasklist-protocol/SKILL.md
- `tests/unit/test_cli_install.py:293`  sc-tasklist-protocol/__init__.py sc-tasklist-protocol/rules/file-emission-rules.md
- `tests/unit/test_cli_install.py:294`  sc-tasklist-protocol/rules/tier-classification.md
- `tests/unit/test_cli_install.py:295`  sc-tasklist-protocol/templates/index-template.md
- `tests/unit/test_cli_install.py:296`  sc-tasklist-protocol/templates/phase-template.md sc-troubleshoot-protocol/SKILL.md
- `tests/unit/test_cli_install.py:315`  sc-validate-roadmap-protocol/SKILL.md sc-validate-tests-protocol/SKILL.md
- `tests/unit/test_cli_install.py:688`  Protocol skills are named ``sc-<command>-protocol`` (e.g. sc-roadmap-protocol
- `tests/unit/test_cli_install.py:706`  for name in ("sc-roadmap-protocol", "sc-reflect-protocol", "sc-task-protocol"):
- `tests/unit/test_cli_install.py:766`  for name in ("sc-init-lite-protocol", "sc-roadmap-protocol"):


## 5. Secondary scan: references the name search above does not catch

Found with a bare-word search (`sprint`, `tasklist`, `roadmap`) over kept files. Each needs a human read.

| Path:line | What it says | Change |
|---|---|---|
| `PROJECT_INDEX.json:46` | CLI groups list has `sprint`, `roadmap`, `tasklist` | Remove the three names |
| `PROJECT_INDEX.json:94` | subpackages list has `sprint`, `roadmap`, `tasklist` | Remove the three names |
| `PROJECT_INDEX.md:36` | CLI groups list | Remove the three names |
| `PROJECT_INDEX.md:68` | subpackages `sprint/`, `roadmap/`, `tasklist/` | Remove the three |
| `PROJECT_INDEX.md:97` | feature suites `sprint/`, `roadmap/`, `tasklist/` | Remove the three |
| `docs/developer-guide/technical-architecture.md:315` | CLI list names `sprint`, `roadmap`, `tasklist` | Remove the three names |
| `docs/developer-guide/testing-debugging.md:348` | example `uv run pytest tests/sprint/ -v` | Use a kept test folder |
| `docs/guides/suites-guide.md:48,262-279` | suite 7 `tasklist_deterministic_shape` | Remove the row and section (suite file is deleted) |
| `docs/user-guide/flags.md:239-245` | sprint flag rows | Remove the sprint rows and sprint mentions |
| `docs/user-guide/flags.md:89,121` | `--handoff tasklist`, `--tasklist` | `--handoff` lists `tasklist` (brainstorm); `--tasklist` is a reflect flag: check and keep the reflect one |
| `.gitignore:243-262` | `/.sprint-exitcode`, `.dev/sprint-state/`, sprint per-task dump rules | Remove the sprint-runner rules (the e2e-reflect harness rule stays) |
| `pyproject.toml:127` | pytest marker `diagnostic: Sprint diagnostic framework tests` | Check whether any kept test uses the marker; reword or remove |
| `src/superclaude/cli/recommend/prompts.py:31-78,201` | artifact-type words `roadmap-generation`, "Sprint bundles" | Routing: check against `tests/recommend` before touching |
| `src/superclaude/cli/recommend/commands.py:7`, `recommend/models.py:4`, `recommend/cache.py:3` | comments citing `cli/tasklist`, `roadmap/convergence.py` | Reword the comments |
| `src/superclaude/core/CLAUDE.md:38` | "`docs/generated/` is a roadmap pipeline artifact directory" | Reword |
| `src/superclaude/core/WORKER-CONTRACT.md:330` | `tasklist` in the list of 12 commands that accept `--unattended` | Remove the name; check the guard test pins |
| `scripts/README.md` | lists scripts being deleted | Remove those rows |
| `CLAUDE.md` (repo) | `superclaude sprint/roadmap` commands in "Pipelines"; the five-case list of internal temporary checkouts names `scripts/eval_runner.py` | Remove the pipeline lines; list four cases |
| `README.md:114-117` | pipeline usage lines | Remove the four lines |

## 6. Judgement calls (flagged in the PR body)

1. `scripts/eval_runner.py` (and `tests/unit/test_eval_runner_master_checkout.py`) are removed with the family: the runner only runs `tests/roadmap/test_eval_*.py` (removed) and `scripts/eval_1.py`, `eval_2.py`, `eval_3.py` (they drive `superclaude roadmap run`; removed). Without them it would point at missing files. The repo `CLAUDE.md` exception list loses the `eval_runner.py` case.
2. `scripts/fidelity-check-setup.sh`, `run-fidelity-batch*.sh`, `rerun-incomplete-phases.sh`, `smoke-test-v2.sh` drive `superclaude roadmap run` and `superclaude sprint run`; removed.
3. Kept test files that import removed packages are trimmed to the cases that use them (section 1). `tests/swarm/test_module_shape.py` pins swarm's file layout against `cli/sprint/` on disk; the sprint half goes, the swarm-only half stays.
4. `tests/cli/eval/test_isolation_layers_probe.py` and `test_phase_report_probe.py` pin the shape of `cli/sprint/executor.py` classes; they test removed code and are removed. Two cases in `test_home_isolation_extend.py` use `IsolationLayers`; they are trimmed.
5. `docs/memory/*`, `KNOWLEDGE.md` past entries and `.dev/` are historical records and are not edited.
6. `cli/eval/suites/tasklist_deterministic_shape.yaml` targets `/sc:tasklist`; removed with its docs row.
