"""``superclaude review lint``: deterministic requirements lint (informational).

Exit 0 always for a readable file, with or without findings. Exit 2 for an
unreadable file, one over 2 MB, or an unknown check name.
"""

from __future__ import annotations

import sys
from pathlib import Path

import click

from superclaude.cli.review.lint import parse_checks, render_json, render_md, run_lint

MAX_BYTES = 2 * 1024 * 1024


@click.command(name="lint")
@click.argument("doc", type=click.Path(dir_okay=False))
@click.option("--format", "fmt", type=click.Choice(["json", "md"]), default="json", show_default=True)
@click.option("--out", "out_path", type=click.Path(dir_okay=False), default=None, help="Write the report here instead of stdout.")
@click.option("--checks", "checks_spec", default=None, help="Comma list of checks: REF,COUNT,KV,PHASE,PATH,RFC (default all).")
def command(doc: str, fmt: str, out_path: str | None, checks_spec: str | None) -> None:
    """Report mechanical inconsistencies in a markdown spec as reviewer evidence."""
    try:
        checks = parse_checks(checks_spec)
    except ValueError as exc:
        click.echo(f"error: {exc}", err=True)
        sys.exit(2)
    path = Path(doc)
    try:
        size = path.stat().st_size
        if size > MAX_BYTES:
            click.echo(f"error: {doc} is {size} bytes, over the 2 MB limit", err=True)
            sys.exit(2)
        data = path.read_bytes()
    except OSError as exc:
        click.echo(f"error: cannot read {doc}: {exc.strerror or exc}", err=True)
        sys.exit(2)
    if len(data) > MAX_BYTES:
        click.echo(f"error: {doc} is over the 2 MB limit", err=True)
        sys.exit(2)
    result = run_lint(data, checks)
    text = render_json(result) if fmt == "json" else render_md(result)
    if out_path:
        target = Path(out_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        click.echo(f"wrote {out_path} ({len(result['findings'])} findings)", err=True)
    else:
        click.echo(text, nl=False)
