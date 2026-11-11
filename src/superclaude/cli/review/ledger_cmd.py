"""`superclaude review ledger`: revise, defer, verdict and capture over a finding ledger."""

from __future__ import annotations

import json
import sys

import click

from superclaude.cli.review import findings as fnd
from superclaude.cli.review import ledger as led

EXIT_BY_DECISION = {"PASS": 0, "REVISE": 10, "ESCALATE": 11}


def _read(path: str) -> str:
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            return fh.read()
    except OSError as exc:
        raise click.ClickException(f"cannot read {path}: {exc}") from exc


def _load(path: str) -> dict:
    try:
        return led.load(path)
    except led.LedgerError as exc:
        raise click.ClickException(str(exc)) from exc


@click.group(name="ledger")
def command() -> None:
    """Typed finding ledger: only these commands change a finding's status."""


@command.command("revise")
@click.option(
    "--ledger",
    "ledger_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "--old",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="The candidate before the revision.",
)
@click.option(
    "--new",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="The candidate after the revision.",
)
@click.option(
    "--fixmap",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="The reviser's output (fixmap-v1 block, or a table with applied rows).",
)
def revise_cmd(ledger_path, old, new, fixmap) -> None:
    """Apply a revision: rows the fix map names as applied and a hunk touches become resolved_check."""
    ledger = _load(ledger_path)
    fm = fnd.parse_fixmap(_read(fixmap))
    try:
        res = led.apply_revision(ledger, _read(old), _read(new), fm["items"])
    except led.LedgerError as exc:
        raise click.ClickException(str(exc)) from exc
    led.save(ledger, ledger_path)
    res["fixmap_ok"] = fm["ok"]
    click.echo(json.dumps(res, indent=1, sort_keys=True))


@command.command("defer")
@click.option(
    "--ledger",
    "ledger_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
)
@click.option("--lid", required=True)
@click.option("--reason", required=True)
def defer_cmd(ledger_path, lid, reason) -> None:
    """Human command: mark a finding deferred."""
    ledger = _load(ledger_path)
    try:
        led.defer(ledger, lid, reason)
    except led.LedgerError as exc:
        raise click.ClickException(str(exc)) from exc
    led.save(ledger, ledger_path)
    click.echo(json.dumps(led.verdict(ledger), sort_keys=True))


@command.command("verdict")
@click.option(
    "--ledger",
    "ledger_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
)
def verdict_cmd(ledger_path) -> None:
    """Print the stored verdict of the last round; exit 0 PASS, 10 REVISE, 11 ESCALATE."""
    ledger = _load(ledger_path)
    try:
        v = led.verdict(ledger)
    except led.LedgerError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(json.dumps(v, sort_keys=True))
    sys.exit(EXIT_BY_DECISION[v["decision"]])


@command.command("capture")
@click.option(
    "--ledger",
    "ledger_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
)
@click.option("--round", "round_n", required=True, type=click.IntRange(min=1))
@click.option(
    "--out",
    default=None,
    type=click.Path(dir_okay=False),
    help="Write the capture matrix here as well.",
)
def capture_cmd(ledger_path, round_n, out) -> None:
    """Export the capture matrix (review-capture/1) of one whole-document round."""
    ledger = _load(ledger_path)
    try:
        cap = led.capture(ledger, round_n, source=ledger_path)
    except led.LedgerError as exc:
        raise click.ClickException(str(exc)) from exc
    text = json.dumps(cap, indent=1, sort_keys=True)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    click.echo(text)
