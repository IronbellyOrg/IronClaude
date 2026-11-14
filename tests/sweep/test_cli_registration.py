"""Tests for the ``superclaude sweep`` registration (DESIGN section 11, ``test_cli_registration.py`` row).

Covers FR-001 (the group is registered on ``main`` and both help screens exit 0) and NFR-006
(importing ``superclaude.cli.sweep`` runs no seam and loads ``commands`` only when
``sweep_group`` is read).

A plain ``import superclaude.cli.sweep`` in a real interpreter already loads ``commands``,
because ``superclaude/cli/__init__.py`` imports ``main`` and ``main`` reads ``sweep_group`` at
import time. The lazy-import test therefore removes the package and ``commands`` from
``sys.modules`` first and reads the module state itself. ``monkeypatch`` puts both entries
(and the ``superclaude.cli.sweep`` attribute of the parent package) back afterwards, so no
half-imported package leaks into a later test. The other sweep submodules stay loaded: the
seam fakes are patched onto the loaded ``probes`` module, and a fresh ``probes`` would hide a
seam call from them.
"""

from __future__ import annotations

import importlib
import sys

import click
from click.testing import CliRunner

import superclaude.cli as cli_package
from superclaude.cli.main import main

PACKAGE = "superclaude.cli.sweep"
COMMANDS = "superclaude.cli.sweep.commands"


def test_sweep_help_exits_zero():
    result = CliRunner().invoke(main, ["sweep", "--help"])

    assert result.exit_code == 0, result.output
    assert "Usage:" in result.output
    assert "run" in result.output


def test_sweep_run_help_exits_zero():
    result = CliRunner().invoke(main, ["sweep", "run", "--help"])

    assert result.exit_code == 0, result.output
    assert "Usage:" in result.output
    assert "--window" in result.output


def test_import_is_lazy_and_runs_no_seam(monkeypatch, patch_orca, patch_git):
    # Register restores for everything the re-import touches, then drop the loaded entries.
    monkeypatch.setattr(cli_package, "sweep", cli_package.sweep)
    monkeypatch.delitem(sys.modules, PACKAGE, raising=False)
    monkeypatch.delitem(sys.modules, COMMANDS, raising=False)
    assert PACKAGE not in sys.modules
    assert COMMANDS not in sys.modules

    package = importlib.import_module(PACKAGE)

    assert sys.modules[PACKAGE] is package
    assert COMMANDS not in sys.modules  # not imported until sweep_group is read
    assert patch_orca.calls == []
    assert patch_git.calls == []

    group = package.sweep_group  # the lazy __getattr__ imports commands now

    assert COMMANDS in sys.modules
    assert isinstance(group, click.Group)
    assert group.name == "sweep"
    assert patch_orca.calls == []
    assert patch_git.calls == []
