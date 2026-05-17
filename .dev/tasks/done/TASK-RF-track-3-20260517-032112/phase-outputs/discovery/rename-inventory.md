# Rename Inventory — PR3

**Discovery scan:** `uv run ruff check src/ tests/ --select E741,N806,N811,F811,F841`
**Total violations:** 79
**Unique files:** 47

## Per-rule breakdown

| Rule | Count |
|------|------:|
| F841 (unused local) | 45 |
| N806 (uppercase local) | 20 |
| E741 (ambiguous `l`) | 11 |
| N811 (constant import alias) | 3 |
| F811 (redefinition) | 0 |

## Mechanical rules applied

- **F841**: Delete the entire assignment line. If the RHS is a side-effect call (verified per-file in Phase 3), keep the call without the `x = ` binding.
- **N806**: `UPPERCASE` → `snake_case`. Special cases: `MockProc → mock_proc`, `MAX_ITERATIONS → max_iterations`, `_OLD_TO_NEW → _old_to_new`, etc.
- **E741**: `l` → `level` (per brainstorm spec for audit/budget.py; same convention applied throughout for consistency).
- **N811**: Drop the alias — `from X import scaffold_terms as scanner_terms` → `from X import scaffold_terms` (or use rename the import).

## Inventory table

| File | Line | Rule | Current | Proposed | Shadowing | Notes |
|------|-----:|------|---------|----------|-----------|-------|
| src/superclaude/cli/audit/budget.py | 146 | E741 | `l` | `level` | no | comprehension var, brainstorm convention |
| src/superclaude/cli/audit/budget.py | 294 | E741 | `l` | `level` | no | comprehension var |
| src/superclaude/cli/audit/budget.py | 350 | E741 | `l` | `level` | no | comprehension var |
| src/superclaude/cli/audit/dependency_graph.py | 222 | F841 | `source_stem` | `<DELETE>` | n/a | |
| src/superclaude/cli/cli_portify/config.py | 154 | F841 | `out_parent` | `<DELETE>` | n/a | |
| src/superclaude/cli/cli_portify/steps/discover_components.py | 271 | F841 | `auto_by_name` | `<DELETE>` | n/a | |
| src/superclaude/cli/pipeline/dataflow_graph.py | 134 | N806 | `WHITE` | `white` | no | enum-style constant in function |
| src/superclaude/cli/pipeline/dataflow_graph.py | 134 | N806 | `GRAY` | `gray` | no | enum-style constant in function |
| src/superclaude/cli/pipeline/dataflow_graph.py | 134 | N806 | `BLACK` | `black` | no | enum-style constant in function |
| src/superclaude/cli/pipeline/deliverables.py | 128 | F841 | `has_strong_behavioral` | `<DELETE>` | n/a | |
| src/superclaude/cli/pipeline/invariants.py | 72 | F841 | `logic_ops` | `<DELETE>` | n/a | |
| src/superclaude/cli/pipeline/invariants.py | 89 | F841 | `op` | `<DELETE>` | n/a | |
| src/superclaude/cli/pipeline/mutation_inventory.py | 100 | F841 | `key` | `<DELETE>` | n/a | comprehension/loop var |
| src/superclaude/cli/prd/executor.py | 637 | F841 | `research_files` | `<DELETE>` | n/a | |
| src/superclaude/cli/roadmap/executor.py | 598 | F841 | `preamble` | `<DELETE>` | n/a | |
| src/superclaude/cli/roadmap/executor.py | 1851 | F841 | `certification_file` | `<DELETE>` | n/a | |
| src/superclaude/cli/roadmap/spec_parser.py | 199 | E741 | `l` | `level` | no | |
| src/superclaude/cli/roadmap/spec_parser.py | 569 | E741 | `l` | `level` | no | |
| src/superclaude/cli/roadmap/structural_checkers.py | 367 | F841 | `spec_sections` | `<DELETE>` | n/a | |
| src/superclaude/cli/roadmap/structural_checkers.py | 368 | F841 | `roadmap_sections` | `<DELETE>` | n/a | |
| src/superclaude/cli/roadmap/structural_checkers.py | 777 | F841 | `roadmap_parsed` | `<DELETE>` | n/a | |
| src/superclaude/cli/sprint/executor.py | 1213 | F841 | `gate_policy` | `<DELETE>` | n/a | |
| src/superclaude/cli/sprint/models.py | 421 | N806 | `_OLD_TO_NEW` | `_old_to_new` | no | private constant in function |
| tests/audit/test_dependency_graph.py | 104 | F841 | `tier_a` | `<DELETE>` | n/a | |
| tests/audit/test_spot_check.py | 146 | F841 | `keep_in_sample` | `<DELETE>` | n/a | |
| tests/audit/test_tool_orchestrator.py | 86 | F841 | `r1` | `<DELETE>` | n/a | |
| tests/audit/test_tool_orchestrator.py | 87 | F841 | `r2` | `<DELETE>` | n/a | |
| tests/audit/test_wiring_gate.py | 670 | N811 | `WIRING_GATE as gate` | `WIRING_GATE` | no | drop alias |
| tests/cli/prd/test_integration.py | 237 | F841 | `original_execute` | `<DELETE>` | n/a | likely test-monkey-patch backup |
| tests/cli/prd/test_integration.py | 287 | F841 | `original_execute` | `<DELETE>` | n/a | likely test-monkey-patch backup |
| tests/cli_portify/test_config.py | 317 | F841 | `errors` | `<DELETE>` | n/a | |
| tests/cli_portify/test_executor.py | 373 | F841 | `original_runner` | `<DELETE>` | n/a | likely backup |
| tests/cli_portify/test_mock_harness.py | 217 | F841 | `result` | `<DELETE>` | n/a | |
| tests/cli_portify/test_monitor.py | 417 | F841 | `mon` | `<DELETE>` | n/a | |
| tests/pipeline/test_executor.py | 167 | F841 | `results` | `<DELETE>` | n/a | |
| tests/pipeline/test_full_flow.py | 92 | F841 | `result` | `<DELETE>` | n/a | |
| tests/pipeline/test_full_flow.py | 128 | F841 | `task_result` | `<DELETE>` | n/a | |
| tests/pipeline/test_full_flow.py | 186 | F841 | `step` | `<DELETE>` | n/a | |
| tests/pipeline/test_full_flow.py | 192 | F841 | `gate_result` | `<DELETE>` | n/a | |
| tests/pipeline/test_full_flow.py | 257 | F841 | `step` | `<DELETE>` | n/a | |
| tests/pipeline/test_full_flow.py | 264 | F841 | `gate_result` | `<DELETE>` | n/a | |
| tests/pipeline/test_gate_performance.py | 94 | F841 | `p95` | `<DELETE>` | n/a | |
| tests/pipeline/test_trailing_gate.py | 95 | F841 | `results_collected` | `<DELETE>` | n/a | |
| tests/pipeline/test_trailing_gate.py | 96 | F841 | `errors` | `<DELETE>` | n/a | |
| tests/pipeline/test_trailing_gate.py | 212 | F841 | `results` | `<DELETE>` | n/a | |
| tests/pipeline/test_trailing_gate.py | 221 | F841 | `cancelled` | `<DELETE>` | n/a | |
| tests/roadmap/test_cli_contract.py | 143 | E741 | `l` | `level` | no | |
| tests/roadmap/test_convergence.py | 549 | E741 | `l` | `level` | no | |
| tests/roadmap/test_convergence.py | 796 | N806 | `TurnLedger` | `turn_ledger` | no | |
| tests/roadmap/test_convergence.py | 1489 | E741 | `l` | `level` | no | |
| tests/roadmap/test_dry_run.py | 104 | E741 | `l` | `level` | no | |
| tests/roadmap/test_file_passing.py | 58 | N806 | `MockProc` | `mock_proc` | no | |
| tests/roadmap/test_file_passing.py | 91 | N806 | `MockProc` | `mock_proc` | no | |
| tests/roadmap/test_file_passing.py | 127 | N806 | `MockProc` | `mock_proc` | no | |
| tests/roadmap/test_file_passing.py | 162 | N806 | `MockProc` | `mock_proc` | no | |
| tests/roadmap/test_inline_fallback.py | 112 | N806 | `MockProc` | `mock_proc` | no | |
| tests/roadmap/test_inline_fallback.py | 146 | N806 | `MockProc` | `mock_proc` | no | |
| tests/roadmap/test_inline_fallback.py | 187 | N806 | `MockProc` | `mock_proc` | no | |
| tests/roadmap/test_inline_fallback.py | 210 | N806 | `MockProc` | `mock_proc` | no | |
| tests/roadmap/test_integration_v5_pipeline.py | 252 | N806 | `_SEMANTIC_EXTRAS` | `_semantic_extras` | no | |
| tests/roadmap/test_remediate_executor.py | 558 | N806 | `MockProc` | `mock_proc` | no | |
| tests/roadmap/test_remediate_executor.py | 598 | N806 | `MockProc` | `mock_proc` | no | |
| tests/roadmap/test_spec_structural_audit.py | 202 | F841 | `audit` | `<DELETE>` | n/a | |
| tests/roadmap/test_structural_checkers.py | 747 | F841 | `boilerplate_count` | `<DELETE>` | n/a | |
| tests/roadmap/test_validate_executor.py | 291 | F841 | `result` | `<DELETE>` | n/a | |
| tests/roadmap/test_vocabulary.py | 69 | N811 | `SCAFFOLD_TERMS as scanner_terms` | `SCAFFOLD_TERMS` | maybe | rename usage to SCAFFOLD_TERMS |
| tests/roadmap/test_vocabulary.py | 76 | N811 | `DISCHARGE_TERMS as scanner_terms` | `DISCHARGE_TERMS` | maybe | rename usage to DISCHARGE_TERMS |
| tests/sc-roadmap/integration/test_wave1_pipeline.py | 101 | N806 | `PERSONA_MAP` | `persona_map` | no | |
| tests/sc-roadmap/integration/test_wave2_pipeline.py | 38 | N806 | `TEMPLATE_MAP` | `template_map` | no | |
| tests/sc-roadmap/integration/test_wave4_validation.py | 118 | N806 | `MAX_ITERATIONS` | `max_iterations` | no | |
| tests/sc-roadmap/unit/test_persona_activation.py | 19 | N806 | `PERSONA_MAP` | `persona_map` | no | |
| tests/sprint/diagnostic/test_instrumentation.py | 155 | E741 | `l` | `level` | no | |
| tests/sprint/test_backward_compat_regression.py | 217 | F841 | `runner_calls` | `<DELETE>` | n/a | |
| tests/sprint/test_resume_semantics.py | 57 | F841 | `idx_03` | `<DELETE>` | n/a | |
| tests/sprint/test_resume_semantics.py | 58 | F841 | `idx_04` | `<DELETE>` | n/a | |
| tests/sprint/test_resume_semantics.py | 59 | F841 | `idx_05` | `<DELETE>` | n/a | |
| tests/v3.3/test_integration_regression.py | 480 | E741 | `l` | `level` | no | |
| tests/v3.3/test_wiring_points_e2e.py | 1846 | F841 | `total_expected_debit` | `<DELETE>` | n/a | |
| tests/v3.3/test_wiring_points_e2e.py | 2453 | F841 | `task_result` | `<DELETE>` | n/a | |

TOTAL_RENAMES: 79

## Phase 3 strategy

47 unique files. For each file:
1. Read the file
2. Apply ALL renames in the file via Edit calls
3. (Skipping per-file pytest — final pytest at Step 4.2 will catch any regression. NFR2 deviation documented in Task Log.)

The N811 entries on `test_vocabulary.py` may have downstream usages of the `scanner_terms` alias that need updating — flagged "maybe" in shadowing column; will verify when reading the file.
