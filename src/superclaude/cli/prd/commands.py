"""PRD CLI commands -- Click command group and subcommands.

Defines the ``superclaude prd`` command group with two subcommands:
run, resume.
"""

from __future__ import annotations

import sys

import click


@click.group("prd")
def prd_group():
    """Generate Product Requirements Documents via multi-step pipeline.

    Orchestrates a 15-step PRD generation pipeline that produces
    comprehensive product requirements from a natural-language request.
    Supports tiered execution (lightweight, standard, heavyweight)
    and resumable pipelines.

    Examples:
        superclaude prd run "Build a user auth system" --product my-app
        superclaude prd run "Add search" --tier heavyweight --where src/api
        superclaude prd run "MVP spec" --dry-run
        superclaude prd resume parse-request
    """
    pass


@prd_group.command()
@click.argument("request")
@click.option(
    "--product",
    "-p",
    default=None,
    help="Product name or scope override.",
)
@click.option(
    "--where",
    "-w",
    multiple=True,
    help="Source directories to focus on (repeatable).",
)
@click.option(
    "--output",
    "-o",
    default=None,
    help="Output path for final PRD (default: current directory).",
)
@click.option(
    "--tier",
    type=click.Choice(["lightweight", "standard", "heavyweight"], case_sensitive=False),
    default="standard",
    help="Pipeline tier (default: standard).",
)
@click.option(
    "--max-turns",
    type=int,
    default=300,
    help="Turn budget for subprocesses (default: 300).",
)
@click.option(
    "--model",
    default="",
    help="Claude model to use (default: env CLAUDE_MODEL or claude default).",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Validate config without launching the pipeline.",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging.",
)
def run(
    request: str,
    product: str | None,
    where: tuple[str, ...],
    output: str | None,
    tier: str,
    max_turns: int,
    model: str,
    dry_run: bool,
    debug: bool,
) -> None:
    """Execute the PRD generation pipeline.

    REQUEST is a natural-language description of the product or feature
    you want to generate requirements for.

    Examples:
        superclaude prd run "Build a user auth system"
        superclaude prd run "Add search" --tier heavyweight
        superclaude prd run "MVP spec" --dry-run
    """
    from .config import resolve_config
    from .executor import PrdExecutor

    try:
        config = resolve_config(
            request,
            product=product,
            where=where if where else None,
            output=output,
            tier=tier,
            max_turns=max_turns,
            model=model,
            dry_run=dry_run,
            debug=debug,
        )
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    if dry_run:
        click.echo(f"Dry run: config validated successfully.")
        click.echo(f"  Request: {config.user_message}")
        click.echo(f"  Tier:    {config.tier}")
        click.echo(f"  Output:  {config.output_path}")
        click.echo(f"  Turns:   {config.max_turns}")
        return

    executor = PrdExecutor(config)
    result = executor.run()

    if result.outcome != "success":
        click.echo(f"Pipeline finished with outcome: {result.outcome}", err=True)
        sys.exit(1)


@prd_group.command()
@click.argument("step_id")
@click.option(
    "--max-turns",
    type=int,
    default=300,
    help="Turn budget for subprocesses (default: 300).",
)
@click.option(
    "--model",
    default="",
    help="Claude model to use (default: env CLAUDE_MODEL or claude default).",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging.",
)
def resume(
    step_id: str,
    max_turns: int,
    model: str,
    debug: bool,
) -> None:
    """Resume a previously interrupted PRD pipeline from a specific step.

    STEP_ID is the pipeline step to resume from (e.g. parse-request,
    investigation-3, qa-synthesis-gate).

    The command reads saved state from the task directory to reconstruct
    pipeline context, then continues execution from the specified step.

    Examples:
        superclaude prd resume parse-request
        superclaude prd resume investigation-3 --max-turns 500
    """
    from .config import resolve_config
    from .executor import PrdExecutor

    try:
        config = resolve_config(
            request="",
            max_turns=max_turns,
            model=model,
            debug=debug,
            resume_from=step_id,
        )
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    executor = PrdExecutor(config)
    result = executor.run()

    if result.outcome != "success":
        click.echo(f"Pipeline finished with outcome: {result.outcome}", err=True)
        sys.exit(1)
