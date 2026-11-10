"""`superclaude review estimate`: capture-recapture estimate of unseen defects."""

from __future__ import annotations

import json
import sys

import click

from superclaude.cli.review.estimate import CaptureError, estimate_capture


@click.command(name="estimate")
@click.argument("capture", metavar="CAPTURE.json")
@click.option(
    "--blocking-only", is_flag=True, help="Only count defects marked blocking."
)
@click.option(
    "--open-blocking",
    type=click.IntRange(min=0),
    default=0,
    show_default=True,
    help="Number of blocking findings still open (the stop rule requires 0).",
)
def command(capture: str, blocking_only: bool, open_blocking: int) -> None:
    """Estimate how many defects the occasions in a review-capture/1 file have not found."""
    try:
        with open(capture, encoding="utf-8") as fh:
            obj = json.load(fh)
        result = estimate_capture(
            obj, blocking_only=blocking_only, open_blocking=open_blocking
        )
    except (
        OSError,
        ValueError,
        CaptureError,
    ) as exc:  # json.JSONDecodeError is a ValueError
        click.echo(f"error: {exc}", err=True)
        sys.exit(2)
    click.echo(json.dumps(result, indent=2, sort_keys=True))
