"""superclaude review: deterministic helpers for document review loops.

Subcommand modules are optional, so branches that add different subcommands
merge without touching this file.
"""

from __future__ import annotations

import importlib

import click


@click.group(name="review")
def review_group() -> None:
    """Deterministic helpers for document review loops."""


for _name in ("panel_cmd", "merge_cmd", "ledger_cmd", "telemetry_cmd", "lint_cmd", "estimate_cmd"):
    try:
        _module = importlib.import_module(f"{__name__}.{_name}")
    except ModuleNotFoundError as _exc:
        if _exc.name != f"{__name__}.{_name}":
            raise
        continue
    review_group.add_command(_module.command)
