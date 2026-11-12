"""`superclaude review panel`: resolve and validate reviewer panel templates."""

from __future__ import annotations

import json
import sys

import click

from superclaude.cli.review import panel as pnl


@click.group(name="panel")
def command() -> None:
    """Resolve and validate the reviewer panel template."""


@command.command("resolve")
@click.option(
    "--template",
    "template",
    default=None,
    type=click.Path(dir_okay=False),
    help="Panel template file (whole-file replacement), or @NAME for a packaged template such as @live7.",
)
@click.option(
    "--tiers",
    "tiers_path",
    default=None,
    type=click.Path(dir_okay=False),
    help="Tier file (whole-file replacement).",
)
@click.option(
    "--env",
    "env",
    default=None,
    help="Environment name (default: $SUPERCLAUDE_REVIEW_ENV, gateway when T3Model01 is set, else anthropic-only).",
)
@click.option("--run-id", required=True, help="Review loop id; seeds the random slots.")
@click.option(
    "--kind",
    "kind",
    type=click.Choice(["first", "re-review"]),
    default="first",
    show_default=True,
)
@click.option(
    "--seed", type=int, default=None, help="Base seed instead of the run-id hash."
)
@click.option(
    "--sequence", type=int, default=None, help="Sequence number for round_robin slots."
)
@click.option(
    "--hard-exclude-class",
    "hard_classes",
    multiple=True,
    help="Model class (e.g. sonnet) that can never be picked; repeatable. Expands through the tier file's classes; case-insensitive.",
)
@click.option(
    "--strict-distinct",
    is_flag=True,
    help="Never pick a model already chosen for an earlier reviewer (no repeat, no re-admission).",
)
def resolve_cmd(
    template,
    tiers_path,
    env,
    run_id,
    kind,
    seed,
    sequence,
    hard_classes,
    strict_distinct,
) -> None:
    """Print the reviewers of a panel as JSON (schema review-panel-resolution/1)."""
    try:
        panel = pnl.load_panel(template)
        tiers = pnl.load_tiers(tiers_path)
        errors = pnl.validate_panel(panel, tiers, sequence=sequence)
        if errors:
            raise ValueError("invalid panel template: " + "; ".join(errors))
        class_map = tiers.get("classes", {})
        known = sorted(set(class_map.values()))
        hard: list[str] = []
        for name in hard_classes:
            ids = [m for m, c in class_map.items() if c.lower() == name.lower()]
            if not ids:
                raise click.UsageError(
                    f"unknown class '{name}' for --hard-exclude-class "
                    f"(known classes: {', '.join(known) or 'none'})"
                )
            hard.extend(ids)
        out = pnl.resolve(
            panel,
            tiers,
            pnl.select_env(env),
            run_id,
            kind,
            seed,
            sequence,
            hard_exclude=hard,
            strict_distinct=strict_distinct,
        )
    except pnl.ExclusionExhausted as exc:
        raise click.ClickException(f"{type(exc).__name__}: {exc}") from exc
    except (ValueError, pnl.NoModelAvailable, OSError, json.JSONDecodeError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(json.dumps(out, indent=2, sort_keys=True))


@command.command("validate")
@click.argument("path", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--kind", type=click.Choice(["panel", "tiers"]), default="panel", show_default=True
)
def validate_cmd(path, kind) -> None:
    """Validate a panel template or tier file; exit 0 when valid, 1 when not."""
    try:
        with open(path, encoding="utf-8") as fh:
            obj = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        click.echo(f"{path}: cannot read: {exc}")
        sys.exit(1)
    errors = pnl.validate_tiers(obj) if kind == "tiers" else pnl.validate_panel(obj)
    for err in errors:
        click.echo(f"{path}: {err}")
    if errors:
        sys.exit(1)
    click.echo(f"{path}: valid {kind} file")
