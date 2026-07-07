"""CLI smoke tests for ``superclaude reflect`` -- help/flags/dry-run/print-command.

Mirrors ``tests/cli/prd/test_cli_smoke.py``. The dry-run and print-command paths
must never construct ``ClaudeProcess`` (FR-12), asserted via ``assert_not_called``.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

import yaml

from superclaude.cli.reflect.commands import _build_inner_command, reflect_group

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
    # FR-RH1 reachability gate flag-pair.
    "--reachability",
    "--no-reachability",
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
    """F6: the --print-command argv preview byte-matches the RESTRICTED
    ``build_command()`` for the Tier-1 review child (L1b, reviewer_profile=True),
    and still never constructs ClaudeProcess (FR-12).

    Post-Phase-3 the restricted preview DROPS ``--tools default`` and
    ``--dangerously-skip-permissions`` (the write/permission tokens) and keeps
    ``--no-session-persistence``, mirroring the restricted ``build_command()``.
    ``--max-turns`` precedes ``--output-format stream-json``.
    """
    with patch("superclaude.cli.reflect.runner.ClaudeProcess") as mock_cls:
        result = cli_runner.invoke(
            reflect_group, ["run", str(temp_tasklist), "--print-command"]
        )
    assert result.exit_code == 0
    out = result.output
    # --no-session-persistence is still emitted in the restricted preview.
    assert "--no-session-persistence" in out
    # The restricted preview OMITS the write/permission tokens.
    assert "--tools default" not in out
    assert "--dangerously-skip-permissions" not in out
    # --output-format stream-json follows --max-turns (real builder order).
    assert "--max-turns" in out
    assert "--output-format stream-json" in out
    assert out.index("--max-turns") < out.index("--output-format stream-json")
    # FR-12: the preview must NOT construct ClaudeProcess.
    mock_cls.assert_not_called()


def test_tmux_inner_command_forwards_isolate_reviewers(tmp_path) -> None:
    """--tmux inner reinvocation preserves explicit reviewer isolation."""
    config = SimpleNamespace(
        tasklist_path=tmp_path / "TASK.md",
        output_dir=tmp_path / "reflect-out",
        depth="deep",
        timeout_seconds=600,
        transport="stub",
        reviewers=3,
        promote=True,
        allow_single_vendor=False,
        isolate_reviewers=True,
        reachability=True,
        resume=False,
        base_override=None,
        tier2_fallback_enabled=True,
    )

    cmd = _build_inner_command(config)

    assert "--isolate-reviewers" in cmd
    assert "--no-isolate-reviewers" not in cmd
    # The Tier-2 fallback state is forwarded explicitly so the inner foreground
    # reinvocation does not silently reset it ON.
    assert "--tier2-fallback" in cmd
    assert "--no-tier2-fallback" not in cmd


def test_tmux_inner_command_forwards_no_isolate_reviewers(tmp_path) -> None:
    """--tmux inner reinvocation preserves explicit reviewer-isolation opt-out."""
    config = SimpleNamespace(
        tasklist_path=tmp_path / "TASK.md",
        output_dir=tmp_path / "reflect-out",
        depth="deep",
        timeout_seconds=600,
        transport="stub",
        reviewers=3,
        promote=True,
        allow_single_vendor=False,
        isolate_reviewers=False,
        reachability=True,
        resume=False,
        base_override=None,
        tier2_fallback_enabled=False,
    )

    cmd = _build_inner_command(config)

    assert "--no-isolate-reviewers" in cmd
    # A disabled fallback state forwards --no-tier2-fallback explicitly.
    assert "--no-tier2-fallback" in cmd
    assert "--tier2-fallback" not in cmd
    assert "--isolate-reviewers" not in cmd


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
