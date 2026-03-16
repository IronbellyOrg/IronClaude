"""CLI Portify Click command group — v2.24.1 interface.

Replaces WORKFLOW_PATH positional with TARGET positional.
Adds --commands-dir, --skills-dir, --agents-dir, --include-agent, --save-manifest.
Backward-compatible: skill-directory invocations continue to work.
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
        superclaude cli-portify run sc-roadmap-protocol --output ./out
        superclaude cli-portify run /path/to/skill/dir --max-turns 100
    """
    pass


@cli_portify_group.command()
@click.argument("target", metavar="TARGET")
@click.option(
    "--cli-name", "--name",
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
    "--start",
    "start_step",
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
def run(
    target: str,
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
    start_step: str,
    max_convergence: int,
    debug: bool,
) -> None:
    """Portify TARGET into a programmatic CLI pipeline.

    TARGET is the name or path of a skill/command to portify.
    Accepted forms: command name, path to .md, path to skill dir,
    skill directory name, sc: prefixed name.

    Examples:
        superclaude cli-portify run roadmap
        superclaude cli-portify run sc:roadmap
        superclaude cli-portify run /path/to/sc-roadmap-protocol
        superclaude cli-portify run sc-roadmap-protocol
    """
    from pathlib import Path

    from superclaude.cli.cli_portify.config import load_portify_config
    from superclaude.cli.cli_portify.models import PortifyValidationError

    # Filter empty include-agent values
    filtered_agents = [a for a in include_agents if a.strip()]

    if dry_run:
        click.echo(f"cli-portify dry-run: {target}")

    try:
        config = load_portify_config(
            workflow_path=target,
            output_dir=output_dir or None,
            cli_name=cli_name or None,
            dry_run=dry_run,
            debug=debug,
            max_turns=max_turns,
            model=model,
        )

        # Apply v2.24.1 options
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

        if dry_run:
            # Emit derived CLI name for dry-run confirmation
            try:
                derived = config.derive_cli_name()
                click.echo(f"Derived CLI name: {derived}")
            except Exception:
                pass
            return

        from superclaude.cli.cli_portify.executor import run_portify
        run_portify(config)

    except PortifyValidationError as exc:
        click.echo(str(exc), err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nEXIT_RECOMMENDATION: INTERRUPTED", err=True)
        sys.exit(0)
