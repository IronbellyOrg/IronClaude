"""CLI smoke tests for ``superclaude reflect`` -- help/flags/dry-run/print-command.

Mirrors ``tests/cli/prd/test_cli_smoke.py``. The dry-run and print-command paths
must never construct ``ClaudeProcess`` (FR-12), asserted via ``assert_not_called``.
"""

from __future__ import annotations

from unittest.mock import patch

import yaml

from superclaude.cli.reflect.commands import reflect_group

_SPEC9_FLAGS = [
    "--tmux",
    "--print-command",
    "--no-promote",
    "--promote",
    "--timeout",
    "--depth",
    "--output",
    "--allow-single-vendor",
    "--dry-run",
    "--resume",
    # Auto-fix evolution flags (D1/D3/D6).
    "--fix",
    "--no-fix",
    "--max-fix-iterations",
    "--base",
]


def test_group_help_shows_run(cli_runner) -> None:
    result = cli_runner.invoke(reflect_group, ["--help"])
    assert result.exit_code == 0
    assert "run" in result.output


def test_run_help_shows_all_spec9_flags(cli_runner) -> None:
    result = cli_runner.invoke(reflect_group, ["run", "--help"])
    assert result.exit_code == 0
    for flag in _SPEC9_FLAGS:
        assert flag in result.output, f"missing option in help: {flag}"


def test_dry_run_never_launches(cli_runner, temp_tasklist, patch_git) -> None:
    """--dry-run derives + previews but never constructs ClaudeProcess (case 9)."""
    with patch("superclaude.cli.reflect.runner.ClaudeProcess") as mock_cls:
        result = cli_runner.invoke(
            reflect_group, ["run", str(temp_tasklist), "--dry-run"]
        )
    assert result.exit_code == 0
    mock_cls.assert_not_called()


def test_print_command_prints_and_never_launches(
    cli_runner, temp_tasklist, patch_git
) -> None:
    """--print-command prints the composed command and never launches (case 13)."""
    with patch("superclaude.cli.reflect.runner.ClaudeProcess") as mock_cls:
        result = cli_runner.invoke(
            reflect_group, ["run", str(temp_tasklist), "--print-command"]
        )
    assert result.exit_code == 0
    assert "/sc:reflect --mode post" in result.output
    assert "claude --print" in result.output
    mock_cls.assert_not_called()


def test_nonexistent_tasklist_is_nonzero(cli_runner) -> None:
    """A nonexistent tasklist path exits non-zero (Click exists=True guard)."""
    result = cli_runner.invoke(reflect_group, ["run", "/no/such/tasklist-xyz.md"])
    assert result.exit_code != 0


def test_print_command_argv_preview_matches_build_command(
    cli_runner, temp_tasklist, patch_git
) -> None:
    """F6: the --print-command argv preview byte-matches build_command()'s flag
    set + order, and still never constructs ClaudeProcess (FR-12).

    Pre-fix the preview omitted ``--no-session-persistence`` and
    ``--tools default`` and reordered ``--output-format``. Post-fix it mirrors
    ``ClaudeProcess.build_command()`` (pipeline/process.py): ``--max-turns``
    precedes ``--output-format stream-json``.
    """
    with patch("superclaude.cli.reflect.runner.ClaudeProcess") as mock_cls:
        result = cli_runner.invoke(
            reflect_group, ["run", str(temp_tasklist), "--print-command"]
        )
    assert result.exit_code == 0
    out = result.output
    # Previously-missing flags are now present.
    assert "--no-session-persistence" in out
    assert "--tools default" in out
    # --output-format stream-json follows --max-turns (real builder order).
    assert "--max-turns" in out
    assert "--output-format stream-json" in out
    assert out.index("--max-turns") < out.index("--output-format stream-json")
    # FR-12: the preview must NOT construct ClaudeProcess.
    mock_cls.assert_not_called()


def test_config_stop_writes_blocked_sidecar(
    cli_runner, temp_tasklist, tmp_path
) -> None:
    """F4: a config/preflight STOP writes a BLOCKED wrapper-result.yaml sidecar
    when an output dir is resolvable (FR-7).

    The tasklist exists (so Click's exists=True guard passes and an output dir
    IS resolvable), and ``resolve_config`` is patched to raise ``ValueError``
    for a non-tasklist reason, exercising the config-STOP handler path. Pre-fix
    no sidecar was written; post-fix one exists with ``verdict: blocked``.
    """
    out_dir = tmp_path / "out"
    with patch(
        "superclaude.cli.reflect.config.resolve_config",
        side_effect=ValueError("config-error"),
    ):
        result = cli_runner.invoke(
            reflect_group,
            ["run", str(temp_tasklist), "--output", str(out_dir)],
        )
    assert result.exit_code == 2
    sidecar = out_dir / "wrapper-result.yaml"
    assert sidecar.exists()
    data = yaml.safe_load(sidecar.read_text(encoding="utf-8"))
    assert data["verdict"] == "blocked"
