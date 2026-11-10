"""`superclaude review merge`: merge reviewer reports into the ledger and write the merged report."""

from __future__ import annotations

import json
import os

import click

from superclaude.cli.review import ledger as led


def _read(path: str) -> str:
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            return fh.read()
    except OSError as exc:
        raise click.ClickException(f"cannot read {path}: {exc}") from exc


@click.command(name="merge")
@click.option(
    "--ledger",
    "ledger_path",
    required=True,
    type=click.Path(dir_okay=False),
    help="Ledger file; created by round 1.",
)
@click.option(
    "--doc",
    "doc",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="The candidate reviewed in this round.",
)
@click.option(
    "--round",
    "round_n",
    required=True,
    type=click.IntRange(min=1),
    help="Review number (1, 2 or 3).",
)
@click.option(
    "--report",
    "reports",
    multiple=True,
    required=True,
    help="REVIEWER_ID=PATH of a reviewer report; repeat for each reviewer.",
)
@click.option(
    "--resolution",
    "resolution",
    default=None,
    type=click.Path(exists=True, dir_okay=False),
    help="Panel resolution JSON (model per reviewer).",
)
@click.option(
    "--out",
    "out",
    required=True,
    type=click.Path(dir_okay=False),
    help="Where to write the merged report.",
)
@click.option(
    "--cap",
    type=click.IntRange(min=1),
    default=3,
    show_default=True,
    help="Review cap used when round 1 creates the ledger.",
)
def command(ledger_path, doc, round_n, reports, resolution, out, cap) -> None:
    """Merge the reviewer reports of one round; print the verdict, decision and Reviser brief ids as JSON."""
    models: dict[str, str] = {}
    if resolution:
        try:
            models = {
                r["reviewer_id"]: r["model"]
                for r in json.loads(_read(resolution))["reviewers"]
            }
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise click.ClickException(
                f"{resolution} is not a panel resolution: {exc}"
            ) from exc
    reviewers = []
    for item in reports:
        rid, sep, path = item.partition("=")
        if not sep or not rid or not path:
            raise click.ClickException(
                f"--report must be REVIEWER_ID=PATH, got {item!r}"
            )
        reviewers.append(
            {
                "reviewer_id": rid,
                "model": models.get(rid),
                "report_path": path,
                "text": _read(path),
            }
        )
    doc_text = _read(doc)
    try:
        if os.path.exists(ledger_path):
            ledger = led.load(ledger_path)
        elif round_n == 1:
            ledger = led.new_ledger(doc, cap)
        else:
            raise click.ClickException(
                f"ledger {ledger_path} does not exist; round {round_n} needs the earlier rounds"
            )
        result = led.merge_round(ledger, doc_text, round_n, reviewers)
        merged = led.render_merged_report(ledger, result, doc, doc_text, round_n)
    except led.LedgerError as exc:
        raise click.ClickException(str(exc)) from exc
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(merged)
    led.save(ledger, ledger_path)
    printable = {k: v for k, v in result.items() if not k.startswith("_")}
    click.echo(json.dumps(printable, indent=1, sort_keys=True))
