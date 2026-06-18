"""Tests for the SUPERCLAUDE_SPRINT_RENDER_DIAG env-gate on the Live redirect.

The TUI's Rich ``Live`` is built with ``redirect_stdout``/``redirect_stderr``
controlled by ``SUPERCLAUDE_SPRINT_RENDER_DIAG``: the default keeps Rich's
redirect enabled (so cross-thread output cannot corrupt the Live UI), and
``SUPERCLAUDE_SPRINT_RENDER_DIAG=1`` disables it for a crash-diagnosis run (the
H-C probe). These tests pin that behavior so it cannot silently regress
(PR #182 review).
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

from rich.console import Console

from superclaude.cli.sprint.models import Phase, SprintConfig
from superclaude.cli.sprint.tui import SprintTUI


def _make_config() -> SprintConfig:
    return SprintConfig(
        index_path=Path("/tmp/tasklist-index.md"),
        release_dir=Path("/tmp/release"),
        phases=[Phase(number=1, file=Path("/tmp/p1.md"), name="Foundation")],
    )


def _captured_redirect_kwargs() -> tuple[bool, bool]:
    """Build a TUI, start it with ``Live`` mocked, return the redirect kwargs."""
    tui = SprintTUI(_make_config(), console=Console(file=StringIO(), width=100))
    with patch("superclaude.cli.sprint.tui.Live") as mock_live:
        mock_live.return_value = MagicMock()
        tui.start()
    _, kwargs = mock_live.call_args
    return kwargs["redirect_stdout"], kwargs["redirect_stderr"]


def test_redirect_enabled_by_default(monkeypatch):
    """Default (env unset): Rich's redirect stays on — no UI corruption."""
    monkeypatch.delenv("SUPERCLAUDE_SPRINT_RENDER_DIAG", raising=False)
    redirect_stdout, redirect_stderr = _captured_redirect_kwargs()
    assert redirect_stdout is True
    assert redirect_stderr is True


def test_redirect_disabled_in_diag_mode(monkeypatch):
    """SUPERCLAUDE_SPRINT_RENDER_DIAG=1: redirect disabled (the H-C probe)."""
    monkeypatch.setenv("SUPERCLAUDE_SPRINT_RENDER_DIAG", "1")
    redirect_stdout, redirect_stderr = _captured_redirect_kwargs()
    assert redirect_stdout is False
    assert redirect_stderr is False


def test_redirect_enabled_for_non_one_values(monkeypatch):
    """Only the exact value '1' enables the probe; other values keep redirect."""
    monkeypatch.setenv("SUPERCLAUDE_SPRINT_RENDER_DIAG", "true")
    redirect_stdout, redirect_stderr = _captured_redirect_kwargs()
    assert redirect_stdout is True
    assert redirect_stderr is True
