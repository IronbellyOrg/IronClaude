---
gate: wiring-verification
target_dir: src/superclaude
files_analyzed: 166
files_skipped: 31
rollout_mode: soft
analysis_complete: true
audit_artifacts_used: 0
unwired_callable_count: 0
orphan_module_count: 7
unwired_registry_count: 0
critical_count: 0
major_count: 7
info_count: 0
total_findings: 7
blocking_findings: 0
whitelist_entries_applied: 0
---

## Summary

- **Target**: src/superclaude
- **Files analyzed**: 166
- **Files skipped**: 31
- **Rollout mode**: soft
- **Total findings**: 7
- **Blocking findings**: 0
- **Scan duration**: 0.7012s

## Unwired Optional Callable Injections

No unsuppressed unwired callable findings.

## Orphan Modules / Symbols

- **cli.cli_portify.steps.analyze_workflow** (src/superclaude/cli/cli_portify/steps/analyze_workflow.py:1) [major]: Module 'cli.cli_portify.steps.analyze_workflow' in provider directory 'steps' has zero inbound imports (import-graph only; AST plugin not loaded)

- **cli.cli_portify.steps.brainstorm_gaps** (src/superclaude/cli/cli_portify/steps/brainstorm_gaps.py:1) [major]: Module 'cli.cli_portify.steps.brainstorm_gaps' in provider directory 'steps' has zero inbound imports (import-graph only; AST plugin not loaded)

- **cli.cli_portify.steps.design_pipeline** (src/superclaude/cli/cli_portify/steps/design_pipeline.py:1) [major]: Module 'cli.cli_portify.steps.design_pipeline' in provider directory 'steps' has zero inbound imports (import-graph only; AST plugin not loaded)

- **cli.cli_portify.steps.discover_components** (src/superclaude/cli/cli_portify/steps/discover_components.py:1) [major]: Module 'cli.cli_portify.steps.discover_components' in provider directory 'steps' has zero inbound imports (import-graph only; AST plugin not loaded)

- **cli.cli_portify.steps.panel_review** (src/superclaude/cli/cli_portify/steps/panel_review.py:1) [major]: Module 'cli.cli_portify.steps.panel_review' in provider directory 'steps' has zero inbound imports (import-graph only; AST plugin not loaded)

- **cli.cli_portify.steps.synthesize_spec** (src/superclaude/cli/cli_portify/steps/synthesize_spec.py:1) [major]: Module 'cli.cli_portify.steps.synthesize_spec' in provider directory 'steps' has zero inbound imports (import-graph only; AST plugin not loaded)

- **cli.cli_portify.steps.validate_config** (src/superclaude/cli/cli_portify/steps/validate_config.py:1) [major]: Module 'cli.cli_portify.steps.validate_config' in provider directory 'steps' has zero inbound imports (import-graph only; AST plugin not loaded)

## Unregistered Dispatch Entries

No unsuppressed registry findings.

## Suppressions and Dynamic Retention

No suppressions applied.

- Audit artifacts used: 0

## Recommended Remediation

- **Orphan modules**: Import orphan modules from consumer code or remove if no longer needed.

## Evidence and Limitations

- Analysis uses AST-based static analysis; dynamic imports and runtime wiring are not detected.
- Alias resolution is limited to direct name references.
- Registry detection uses pattern matching on variable names; non-conventional naming may be missed.
