"""`superclaude review telemetry`: task variables, append-only records and the SQLite loader."""

from __future__ import annotations

import json
import os

import click

from superclaude.cli.review import telemetry as tel

DEFAULT_DIR = ".dev/benchmarks/review-telemetry"


@click.group(name="telemetry")
def command() -> None:
    """Review telemetry: task variables, append-only records, SQLite loader."""


@command.command("taskvars")
@click.argument("doc", type=click.Path(exists=True, dir_okay=False))
@click.option("--specialization", default="unspecified", show_default=True)
@click.option(
    "--kind",
    "kind",
    type=click.Choice(list(tel.KINDS)),
    default="first",
    show_default=True,
)
def taskvars_cmd(doc, specialization, kind) -> None:
    """Print the task variables of a document as JSON."""
    with open(doc, encoding="utf-8", newline="") as fh:
        text = fh.read()
    click.echo(
        json.dumps(
            tel.task_variables(text, specialization, kind), indent=2, sort_keys=True
        )
    )


@command.command("append")
@click.option(
    "--dir",
    "directory",
    default=None,
    envvar="SUPERCLAUDE_REVIEW_TELEMETRY_DIR",
    help=f"Telemetry directory (default {DEFAULT_DIR}).",
)
@click.option(
    "--record",
    "record",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="JSON file with one record (or a list of records).",
)
def append_cmd(directory, record) -> None:
    """Validate record(s) and append them to the run file."""
    try:
        with open(record, encoding="utf-8") as fh:
            obj = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise click.ClickException(f"cannot read {record}: {exc}") from exc
    records = obj if isinstance(obj, list) else [obj]
    directory = directory or DEFAULT_DIR
    for rec in records:
        try:
            path = tel.append_record(directory, rec)
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        click.echo(os.fspath(path))


@command.command("load")
@click.option(
    "--dir", "directory", default=None, envvar="SUPERCLAUDE_REVIEW_TELEMETRY_DIR"
)
@click.option(
    "--db",
    "db",
    required=True,
    type=click.Path(dir_okay=False),
    help="SQLite file to create or update.",
)
def load_cmd(directory, db) -> None:
    """Load all records into SQLite (idempotent); invalid lines are listed and skipped."""
    counts = tel.load(directory or DEFAULT_DIR, db)
    for item in counts["invalid"]:
        click.echo(f"invalid: {item}", err=True)
    click.echo(
        json.dumps(
            {
                "reviewer_runs": counts["reviewer_runs"],
                "outcomes": counts["outcomes"],
                "invalid": len(counts["invalid"]),
            }
        )
    )
