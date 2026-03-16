"""CLI Portify Click command group and subcommands.

Defines the ``superclaude cli-portify`` command group with the ``run`` subcommand
and all 7 user-facing options (FR-049).
"""

from __future__ import annotations

import sys

import click


@click.group("cli-portify")
def cli_portify_group():
    """Port inference-based SuperClaude workflows into programmatic CLI pipelines.

    Converts slash commands, skills, and agents into deterministic Python-controlled
    pipeline runners with supervised, sprint-style execution.

    Examples:
        superclaude cli-portify run sc:roadmap
        superclaude cli-portify run sc:roadmap --dry-run
        superclaude cli-portify run sc:roadmap --output ./out --max-turns 100
        superclaude cli-portify run sc:roadmap --resume step-graph-design
    """
    pass


@cli_portify_group.command()
@click.argument("workflow", metavar="WORKFLOW")
@click.option(
    "--name",
    default="",
    help="Override derived CLI name for the portified pipeline",
)
@click.option(
    "--output",
    "output_dir",
    default="",
    help="Output directory for generated pipeline (default: alongside workflow)",
)
@click.option(
    "--max-turns",
    type=int,
    default=200,
    help="Maximum Claude agent turns (default: 200)",
)
@click.option(
    "--model",
    default="",
    help="Claude model to use (default: env CLAUDE_MODEL or claude default)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Execute only PREREQUISITES/ANALYSIS/USER_REVIEW/SPECIFICATION steps (SC-012)",
)
@click.option(
    "--resume",
    "resume_step",
    default="",
    metavar="STEP_ID",
    help="Resume pipeline from a specific step ID",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug logging",
)
def run(
    workflow: str,
    name: str,
    output_dir: str,
    max_turns: int,
    model: str,
    dry_run: bool,
    resume_step: str,
    debug: bool,
) -> None:
    """Portify WORKFLOW into a programmatic CLI pipeline.

    WORKFLOW is the path to a skill directory or the name of a skill/command/agent
    to portify (e.g., ``sc:roadmap``, ``~/.claude/skills/sc-roadmap``).

    Runs the full portification pipeline: analysis, specification synthesis,
    release spec generation, and panel review.
    """
    from superclaude.cli.cli_portify.config import load_portify_config
    from superclaude.cli.cli_portify.executor import run_portify
    from superclaude.cli.cli_portify.models import PortifyValidationError

    try:
        config = load_portify_config(
            workflow_path=workflow,
            output_dir=output_dir or None,
            cli_name=name or None,
            dry_run=dry_run,
            debug=debug,
            max_turns=max_turns,
            model=model,
        )
        # Thread resume step into config if provided
        if resume_step:
            config.resume_from = resume_step  # type: ignore[attr-defined]

        run_portify(config)

    except PortifyValidationError as exc:
        click.echo(str(exc), err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nEXIT_RECOMMENDATION: INTERRUPTED", err=True)
        sys.exit(0)
