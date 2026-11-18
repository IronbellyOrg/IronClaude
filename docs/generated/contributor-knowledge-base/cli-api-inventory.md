# CLI API Inventory

## Scope and source of truth

This inventory documents the current Python code under `src/superclaude/cli/` as it exists in this repository on 2026-03-09.

When older hand-written docs and current code differ, prefer the code. In particular, command wiring and exported symbols below are derived from the current package source, not from older README-style summaries.

## Package overview

`src/superclaude/cli/` is the implementation package behind the `superclaude` console script.

| Item | Current code evidence | Notes for contributors |
| --- | --- | --- |
| Console entry point | `pyproject.toml` → `superclaude = "superclaude.cli.main:main"` | The Click root group lives in `src/superclaude/cli/main.py`. |
| Root package export | `src/superclaude/cli/__init__.py` exports `main` | Importing `superclaude.cli` exposes the top-level Click entry point. |
| CLI style | Click command groups and subcommands | Top-level commands are defined in `main.py`; larger workflow CLIs live in subpackages. |
| Major subsystems | install/update flows, MCP installation, health checks, shared pipeline helpers, audit helpers | `pipeline/` and `audit/` are support libraries. |

## Directory map

```text
src/superclaude/cli/
├── __init__.py
├── main.py
├── doctor.py
├── install_agents.py
├── install_commands.py
├── install_core.py
├── install_mcp.py
├── install_skill.py
├── install_skills.py
├── audit/
└── pipeline/
```

## Top-level entry points

### Root Click group

| Symbol | File | Kind | Role |
| --- | --- | --- | --- |
| `main` | `src/superclaude/cli/main.py` | Click group | Root `superclaude` CLI group with version support. |

### Top-level commands registered in `main.py`

| CLI command | Python function | Primary dependencies | Purpose |
| --- | --- | --- | --- |
| `superclaude install` | `install` | `install_core`, `install_commands`, `install_agents`, `install_skill`, `install_skills` | Install core framework files, slash commands, agents, and skills. |
| `superclaude mcp` | `mcp` | `install_mcp` | List or install MCP servers. |
| `superclaude update` | `update` | `install_core`, `install_commands`, `install_agents`, `install_skills` | Force-refresh installed framework assets. |
| `superclaude install-skill <name>` | `install_skill` | `install_skill` | Install one skill into the Claude Code skills directory. |
| `superclaude doctor` | `doctor` | `doctor.run_doctor` | Run installation/configuration checks and return non-zero on failure. |
| `superclaude version` | `version` | package `__version__` | Print framework version. |

## Top-level module inventory

| Module | Key symbols observed | Contributor notes |
| --- | --- | --- |
| `src/superclaude/cli/__init__.py` | `main` | Minimal re-export of the root CLI entry point. |
| `src/superclaude/cli/main.py` | `main`, `install`, `mcp`, `update`, `install_skill`, `doctor`, `version` | First file to read when tracing command registration. Also manually registers the later subcommand groups. |
| `src/superclaude/cli/doctor.py` | `run_doctor`, `_check_pytest_plugin`, `_check_agents_installed`, `_check_skills_installed`, `_check_configuration` | Health-check implementation used by the `doctor` command. |
| `src/superclaude/cli/install_core.py` | `install_core_files`, `list_core_files`, `list_installed_core_files` | Handles installation/listing of core framework files. |
| `src/superclaude/cli/install_commands.py` | `install_commands`, `list_available_commands`, `list_installed_commands` | Handles slash command asset installation. |
| `src/superclaude/cli/install_agents.py` | `install_agents`, `list_available_agents`, `list_installed_agents` | Handles agent asset installation; includes `_EXCLUDE_FILES` filter constant. |
| `src/superclaude/cli/install_skill.py` | `install_skill_command`, `list_available_skills`, `_get_skill_source`, `_is_valid_skill_dir` | Single-skill installer and skill discovery helpers. |
| `src/superclaude/cli/install_skills.py` | `install_all_skills`, `list_installed_skills`, `_has_corresponding_command` | Bulk skill installer. |
| `src/superclaude/cli/install_mcp.py` | `AIRIS_GATEWAY`, `MCP_SERVERS`, `install_mcp_servers`, `list_available_servers`, `install_mcp_server` | MCP server catalog and install orchestration. |

## Subpackage inventory

## `pipeline/` subpackage

### Purpose

Shared pipeline foundation used by workflow-oriented CLIs. The package docstring explicitly describes it as the shared base for CLI pipeline runners, and its `__all__` exposes a broad reusable API.

### Exported/public surface from `pipeline/__init__.py`

| Category | Exported symbols |
| --- | --- |
| Core models | `PipelineConfig`, `Step`, `StepResult`, `StepStatus`, `GateCriteria`, `SemanticCheck`, `Deliverable`, `DeliverableKind` |
| Execution/process | `execute_pipeline`, `ClaudeProcess`, `gate_passed` |
| Deliverable analysis | `decompose_deliverables`, `is_behavioral` |
| Guard analysis | `GuardDetection`, `GuardKind`, `TypeTransitionKind`, `GuardAnalysisOutput`, `run_guard_analysis_pass`, `GuardResolutionOutput`, `ReleaseGateWarning`, `AcceptedRisk` |
| Invariants/FMEA | `InvariantRegistryOutput`, `run_invariant_registry_pass`, `DetectionDifficulty`, `Severity`, `FMEAFailureMode`, `classify_failure_modes`, `FMEAPromotionOutput`, `ReleaseGateViolation`, `promote_failure_modes`, `CombinedM2Output`, `run_combined_m2_pass` |
| Dataflow/conflict analysis | `DataFlowGraph`, `DataFlowNode`, `DataFlowEdge`, `NodeOperation`, `build_dataflow_graph`, `ImplicitContract`, `extract_implicit_contracts`, `ConflictKind`, `ConflictDetection`, `detect_conflicts`, `DataFlowTracingOutput`, `run_dataflow_tracing_pass` |
| Trailing gate/remediation | `TrailingGatePolicy`, `TrailingGateResult`, `TrailingGateRunner`, `GateResultQueue`, `GateScope`, `DeferredRemediationLog`, `RemediationEntry`, `RemediationStatus`, `build_remediation_prompt`, `resolve_gate_mode` |
| Conflict review helpers | `ConflictAction`, `ConflictReviewResult`, `detect_file_overlap`, `review_conflicts` |
| Diagnostics | `DiagnosticReport`, `DiagnosticStage`, `StageResult`, `run_diagnostic_chain` |

### Important modules

| Module | Key API surface observed | Why it matters |
| --- | --- | --- |
| `__init__.py` | Broad `__all__` export list | Best starting point for shared workflow primitives. |
| `models.py` | `StepStatus`, `GateMode`, `SemanticCheck`, `GateCriteria`, `Step`, `StepResult`, `DeliverableKind`, `Deliverable`, `PipelineConfig` | Common typed model layer. |
| `executor.py` | `execute_pipeline`, `_execute_single_step`, `_run_parallel_steps`, `_build_state`, `StepRunner` | Generic pipeline runner. |
| `process.py` | `ClaudeProcess` with `build_command`, `build_env`, `start`, `wait`, `terminate` | Shared subprocess wrapper for Claude execution. |
| `gates.py`, `deliverables.py`, `trailing_gate.py` | files present | Gate enforcement, deliverable handling, remediation/trailing gate logic. |
| `guard_*`, `invariant_pass.py`, `fmea_*`, `combined_m2_pass.py` | files present | Analysis passes layered on top of the generic pipeline model. |
| `dataflow_*`, `contract_extractor.py`, `conflict_*` | files present | Cross-step structural analysis and conflict handling. |
| `diagnostic_chain.py`, `verification_emitter.py`, `mutation_inventory.py`, `state_detector.py` | files present | Diagnostics and verification support. |

## `audit/` subpackage

### Purpose

Support library for cleanup/audit-oriented analysis. The package docstring calls it a cleanup-audit v2 module covering classification, coverage, checkpointing, validation, and profiling.

### Important modules

| Module | Key API surface observed | Why it matters |
| --- | --- | --- |
| `tool_orchestrator.py` | `ToolOrchestrator`, `ResultCache`, `FileAnalysis`, `CacheStats`, `compute_content_hash` | Central orchestration/cache layer for per-file and batch analysis. |
| `validation.py` | `ValidationResult`, `stratified_sample`, `validate_consistency` | Validation utilities. |
| `classification.py`, `duplication.py`, `dead_code.py`, `dynamic_imports.py`, `dependency_graph.py`, `coverage.py` | files present | Domain-specific audit analyses. |
| `checkpoint.py`, `resume.py`, `batch_decomposer.py`, `batch_retry.py`, `budget.py` | files present | Audit execution control and resilience helpers. |
| `artifact_emitter.py`, `report_completeness.py`, `report_depth.py`, `report_limitations.py`, `validation_output.py` | files present | Reporting and artifact shaping. |
| `credential_scanner.py`, `gitignore_checker.py`, `manifest_gate.py`, `evidence_gate.py`, `anti_lazy.py`, `known_issues.py` | files present | Safety, policy, and evidence-oriented checks. |
| `docs_audit.py`, `filetype_rules.py`, `dir_assessment.py`, `profile_generator.py`, `profiler.py`, `env_matrix.py` | files present | Supporting audit heuristics and profiling. |

## Command group structure at a glance

| Level | Registered names |
| --- | --- |
| Root group | `superclaude` |
| Root commands | `install`, `mcp`, `update`, `install-skill`, `doctor`, `version` |

## Contributor navigation tips

### If you need to change command registration

Start with `src/superclaude/cli/main.py`.

That file owns:

- the root Click group
- top-level commands

### If you need to change installation behavior

Read these in order:

1. `src/superclaude/cli/main.py`
2. `src/superclaude/cli/install_core.py`
3. `src/superclaude/cli/install_commands.py`
4. `src/superclaude/cli/install_agents.py`
5. `src/superclaude/cli/install_skill.py` and `install_skills.py`
6. `src/superclaude/cli/install_mcp.py`

### If you need to change workflow orchestration

Use this split:

- `pipeline/` for shared execution, gate, process, and analysis primitives
- `audit/` for lower-level audit analysis and reporting support

### If older docs disagree with current code

Prefer the current package code.

Examples from the current tree:

- the active console-script target is `superclaude.cli.main:main`
- `pipeline/__init__.py` exports a larger shared API surface than older high-level docs usually summarize

## Fast start reading order for contributors

1. `pyproject.toml` — console-script wiring
2. `src/superclaude/cli/main.py` — root command graph
3. One workflow package, for example `src/superclaude/cli/reflect/commands.py`
4. Its matching `models.py` and runner module
5. `src/superclaude/cli/pipeline/__init__.py` and `pipeline/models.py`
6. `src/superclaude/cli/audit/` if the change touches cleanup/audit internals
