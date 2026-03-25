"""CLI Portify Click command group and subcommands.

Defines the ``superclaude cli-portify`` command group with the ``run`` subcommand
and all user-facing options (FR-049). Merges options from the former cli.py module.
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
@click.argument("workflow", metavar="TARGET")
@click.option(
    "--cli-name",
    "--name",
    "cli_name",
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
    "--commands-dir",
    default="",
    help="Override directory to search for command .md files",
)
@click.option(
    "--skills-dir",
    default="",
    help="Override directory to search for skill directories",
)
@click.option(
    "--agents-dir",
    default="",
    help="Override directory to search for agent .md files",
)
@click.option(
    "--include-agent",
    "include_agents",
    multiple=True,
    help="Include specific agent by name (may be repeated; empty values filtered)",
)
@click.option(
    "--save-manifest",
    "save_manifest",
    default="",
    help="Write component manifest Markdown to this path",
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
    "--start",
    "resume_step",
    default="",
    metavar="STEP_ID",
    help="Resume pipeline from a specific step ID",
)
@click.option(
    "--max-convergence",
    type=int,
    default=3,
    help="Maximum convergence iterations for panel-review (default: 3)",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug logging",
)
@click.option(
    "--gate-mode",
    type=click.Choice(["shadow", "soft", "full"], case_sensitive=False),
    default="shadow",
    help="Gate enforcement mode: shadow (log only), soft (warn), full (block).",
)
def run(
    workflow: str,
    cli_name: str,
    output_dir: str,
    commands_dir: str,
    skills_dir: str,
    agents_dir: str,
    include_agents: tuple,
    save_manifest: str,
    max_turns: int,
    model: str,
    dry_run: bool,
    resume_step: str,
    max_convergence: int,
    debug: bool,
    gate_mode: str,
) -> None:
    """Portify WORKFLOW into a programmatic CLI pipeline.

    WORKFLOW is the path to a skill directory or the name of a skill/command/agent
    to portify (e.g., ``sc:roadmap``, ``~/.claude/skills/sc-roadmap``).

    Runs the full portification pipeline: analysis, specification synthesis,
    release spec generation, and panel review.
    """
    from pathlib import Path

    from superclaude.cli.cli_portify.config import (
        load_portify_config,
        validate_portify_config,
    )
    from superclaude.cli.cli_portify.executor import run_portify
    from superclaude.cli.cli_portify.models import PortifyValidationError

    # Filter empty include-agent values
    filtered_agents = [a for a in include_agents if a.strip()]

    try:
        config = load_portify_config(
            workflow_path=workflow,
            output_dir=output_dir or None,
            cli_name=cli_name or None,
            dry_run=dry_run,
            debug=debug,
            max_turns=max_turns,
            model=model,
            max_convergence=max_convergence,
        )

        # Apply optional directory overrides
        if commands_dir:
            config.commands_dir = Path(commands_dir)
        if skills_dir:
            config.skills_dir = Path(skills_dir)
        if agents_dir:
            config.agents_dir = Path(agents_dir)
        if save_manifest:
            config.save_manifest_path = Path(save_manifest)
        if filtered_agents:
            config._include_agents_list = list(filtered_agents)
            config.include_agents = True

        # Set resume_from directly (now a proper field on PortifyConfig)
        if resume_step:
            config.resume_from = resume_step

        # Set gate enforcement mode
        config.gate_mode = gate_mode

        # Validate config before proceeding
        validation_errors = validate_portify_config(config)
        if validation_errors:
            for err in validation_errors:
                click.echo(f"Error: {err}", err=True)
            sys.exit(1)

        if dry_run:
            click.echo(f"cli-portify dry-run: {workflow}")
            try:
                click.echo(f"Derived CLI name: {config.derive_cli_name()}")
            except Exception:
                pass
            return

        run_portify(config)

    except PortifyValidationError as exc:
        click.echo(str(exc), err=True)
        sys.exit(1)
    except FileNotFoundError as exc:
        click.echo(f"File not found: {exc}", err=True)
        sys.exit(1)
    except PermissionError as exc:
        click.echo(f"Permission denied: {exc}", err=True)
        sys.exit(1)
    except OSError as exc:
        click.echo(f"OS error: {exc}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nEXIT_RECOMMENDATION: INTERRUPTED", err=True)
        sys.exit(0)
    except Exception as exc:
        import traceback

        if debug:
            traceback.print_exc()
        click.echo(f"Unexpected error: {exc}", err=True)
        sys.exit(1)
