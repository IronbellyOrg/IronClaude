"""Step implementations for the cli-portify pipeline.

Provides the STEP_DISPATCH registry mapping step IDs to their run_*() functions.
Each dispatch function accepts (config) and returns a PortifyStepResult.
Some step modules return tuples — the dispatch wrappers normalize these.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from superclaude.cli.cli_portify.models import PortifyConfig, PortifyStepResult


def _get_dispatch_registry() -> dict[str, Callable[["PortifyConfig"], "PortifyStepResult"]]:
    """Build the step dispatch registry lazily to avoid circular imports.

    Maps step IDs from STEP_REGISTRY to their run_*() entry points in step modules.
    Wraps functions that return tuples to extract just the PortifyStepResult.
    """
    from superclaude.cli.cli_portify.steps.analyze_workflow import run_analyze_workflow
    from superclaude.cli.cli_portify.steps.brainstorm_gaps import run_brainstorm_gaps
    from superclaude.cli.cli_portify.steps.design_pipeline import run_design_pipeline
    from superclaude.cli.cli_portify.steps.discover_components import (
        run_discover_components,
    )
    from superclaude.cli.cli_portify.steps.panel_review import run_panel_review
    from superclaude.cli.cli_portify.steps.synthesize_spec import run_synthesize_spec
    from superclaude.cli.cli_portify.steps.validate_config import run_validate_config

    # Wrappers for functions that return tuples (result, PortifyStepResult)
    def _wrap_validate_config(config: "PortifyConfig") -> "PortifyStepResult":
        _, step_result = run_validate_config(config)
        return step_result

    def _wrap_discover_components(config: "PortifyConfig") -> "PortifyStepResult":
        _, step_result = run_discover_components(config)
        return step_result

    return {
        "validate-config": _wrap_validate_config,
        "discover-components": _wrap_discover_components,
        "protocol-mapping": run_analyze_workflow,
        "analysis-synthesis": run_analyze_workflow,
        "step-graph-design": run_design_pipeline,
        "models-gates-design": run_design_pipeline,
        "prompts-executor-design": run_design_pipeline,
        "pipeline-spec-assembly": run_design_pipeline,
        "release-spec-synthesis": run_synthesize_spec,
        "brainstorm-gaps": run_brainstorm_gaps,
        "panel-review": run_panel_review,
    }


# Cached registry instance
_DISPATCH_REGISTRY: dict[str, Callable] | None = None


def get_step_dispatch() -> dict[str, Callable[["PortifyConfig"], "PortifyStepResult"]]:
    """Return the step dispatch registry, building it on first call."""
    global _DISPATCH_REGISTRY
    if _DISPATCH_REGISTRY is None:
        _DISPATCH_REGISTRY = _get_dispatch_registry()
    return _DISPATCH_REGISTRY
