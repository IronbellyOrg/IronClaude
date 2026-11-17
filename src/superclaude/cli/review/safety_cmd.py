"""`superclaude review safety-scan <file>`: print rows that hold destructive or secret words.

A hit is information, not a failure, so the command exits 0 on any readable input.
Unreadable or missing input exits 2 and never prints a hit count.
"""

from __future__ import annotations

import click

from superclaude.cli.review import safety_route as route

PERSON_PROMPT = "Show these rows to the person before they are treated as follow-ups."


@click.command(name="safety-scan")
@click.argument("file", type=str)
@click.option(
    "--unattended",
    is_flag=True,
    default=False,
    help="Worker mode: end with a signal line instead of asking a person.",
)
def command(file: str, unattended: bool) -> None:
    """Scan FILE (one row per line) for destructive or secret vocabulary."""
    result = route.scan_file(file)
    if isinstance(result, route.Unreadable):
        click.echo(f"safety-scan: cannot read {result.path}: {result.reason}")
        raise SystemExit(2)
    for hit in result.hits:
        click.echo(
            f"SAFETY HIT line {hit.line} ({hit.word}), graded blocking: {hit.row}"
        )
    if result.empty:
        click.echo("safety-scan: file is empty, 0 rows read")
    else:
        click.echo(
            f"safety-scan: {result.rows_read} rows read, "
            f"{result.rows_skipped} skipped, {len(result.hits)} hits"
        )
    if unattended:
        click.echo(f"safety-scan signal: {'partial' if result.hits else 'none'}")
    elif result.hits:
        click.echo(PERSON_PROMPT)
