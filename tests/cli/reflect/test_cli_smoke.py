"""CLI smoke tests for ``superclaude reflect`` -- help/flags/dry-run/print-command.

Mirrors ``tests/cli/prd/test_cli_smoke.py``. The dry-run and print-command paths
must never construct ``ClaudeProcess`` (FR-12), asserted via ``assert_not_called``.
"""

from __future__ import annotations

import subprocess
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
import yaml

import superclaude.cli.reflect.config as config_mod
from superclaude.cli.reflect.commands import _build_inner_command, reflect_group
from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.runner import ReflectRunner

from .conftest import _FAKE_BASE, _FAKE_HEAD

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
    )

    cmd = _build_inner_command(config)

    assert "--isolate-reviewers" in cmd
    assert "--no-isolate-reviewers" not in cmd


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
    )

    cmd = _build_inner_command(config)

    assert "--no-isolate-reviewers" in cmd
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


def test_config_error_sidecar_carries_error_detail(
    cli_runner, temp_tasklist, tmp_path
) -> None:
    """B2: a config STOP records the real cause in the sidecar ``error_detail``
    while ``reason`` stays byte-stable ``config-error`` and ``error_detail`` never
    leaks into the committable tasklist frontmatter.

    Patches ``resolve_config`` to raise the post-C2 actionable message; the
    config-STOP handler must surface that cause (truncated) via the sidecar-only
    ``error_detail`` field. Pre-fix the field did not exist.
    """
    out_dir = tmp_path / "out"
    with patch(
        "superclaude.cli.reflect.config.resolve_config",
        side_effect=ValueError(
            "base-unresolved: 'master' did not resolve; "
            "pass --base <ref> or set frontmatter start_commit"
        ),
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
    # The real cause is carried in the sidecar-only error_detail field...
    assert "base-unresolved" in data["error_detail"]
    # ...while reason stays byte-stable.
    assert data["reason"] == "config-error"
    # error_detail must NEVER reach the committable tasklist frontmatter.
    tasklist_after = temp_tasklist.read_text(encoding="utf-8")
    assert "error_detail" not in tasklist_after
    # Explicitly pin that no frontmatter writeback ran on the config-STOP path:
    # the config STOP exits (sys.exit(2)) before write_reflect_post, so the
    # reflect_post block stays the empty stub — a leak is structurally impossible
    # here because _build_reflect_post_value never executes on this path.
    assert 'reflect_post: ""' in tasklist_after


def test_base_unresolved_message_is_actionable(temp_tasklist, monkeypatch) -> None:
    """C2: the master-only resolve path is byte-identical (exactly ONE merge-base
    call, no extra git call), and the main-only STOP raises an ACTIONABLE
    ``base-unresolved`` naming the ``--base`` / ``start_commit`` remediation.
    """
    # Strip frontmatter start_commit so both blocks exercise the merge-base branch.
    text = temp_tasklist.read_text(encoding="utf-8").replace(
        f'start_commit: "{_FAKE_BASE}"', 'start_commit: ""'
    )
    temp_tasklist.write_text(text, encoding="utf-8")

    # ---- master-only path: resolution unchanged, exactly ONE merge-base call ----
    def _fake_git_master(cwd, *args):
        if args and args[0] == "rev-parse":
            return _FAKE_HEAD
        if args and args[0] == "merge-base":
            return _FAKE_BASE
        return ""

    mock = MagicMock(side_effect=_fake_git_master)
    monkeypatch.setattr(config_mod, "_git", mock)
    config = resolve_config(str(temp_tasklist), depth="standard", model="test-model")
    assert config.base == _FAKE_BASE
    # Count merge-base SPECIFICALLY (the same mock also records rev-parse HEAD, so
    # total call_count == 2). Proves no EXTRA merge-base git call was added vs
    # pre-fix. The fake is invoked as _git(cwd, *args) so "merge-base" is in c.args.
    merge_base_calls = [c for c in mock.call_args_list if "merge-base" in c.args]
    assert len(merge_base_calls) == 1
    # And exactly TWO total git calls (the single merge-base + the single
    # rev-parse HEAD) — proves NO extra git call of any kind was added on the
    # byte-identical master-resolve path, not merely that merge-base ran once.
    assert mock.call_count == 2

    # ---- main-only path: master doesn't exist -> actionable base-unresolved ----
    def _fake_git_main_only(cwd, *args):
        if args and args[0] == "rev-parse":
            return _FAKE_HEAD
        if args and args[0] == "merge-base":
            raise subprocess.CalledProcessError(128, ["git", "merge-base"])
        return ""

    monkeypatch.setattr(config_mod, "_git", MagicMock(side_effect=_fake_git_main_only))
    with pytest.raises(ValueError, match="base-unresolved") as excinfo:
        resolve_config(str(temp_tasklist), depth="standard", model="test-model")
    # The C2 actionable guidance names the remediation path.
    assert "pass --base" in str(excinfo.value)
    assert "start_commit" in str(excinfo.value)


def test_runner_crash_writes_blocked_runner_error_sidecar(
    cli_runner, temp_tasklist, tmp_path, patch_git
) -> None:
    """D2: a non-ValueError raised inside ``ReflectRunner.run()`` writes a BLOCKED
    ``reason="runner-error"`` sidecar carrying ``error_detail`` then re-raises, so
    the crash still yields a non-zero exit (no bare traceback swallow).

    ``patch_git`` is REQUIRED: without it ``resolve_config`` calls the real
    ``config._git`` in a non-git tmp dir and STOPs with a ``config-error`` sidecar
    BEFORE ``run`` is reached — which would make ``reason == "runner-error"`` fail.
    Stubbing git lets ``resolve_config`` resolve cleanly so control reaches the
    patched ``run`` and the D2 wrap produces the ``runner-error`` sidecar.
    """
    out_dir = tmp_path / "out"
    with patch.object(ReflectRunner, "run", side_effect=RuntimeError("boom")):
        result = cli_runner.invoke(
            reflect_group,
            ["run", str(temp_tasklist), "--output", str(out_dir)],
        )
    assert result.exit_code != 0
    sidecar = out_dir / "wrapper-result.yaml"
    assert sidecar.exists()
    data = yaml.safe_load(sidecar.read_text(encoding="utf-8"))
    assert data["verdict"] == "blocked"
    assert "error_detail" in data
    assert "boom" in data["error_detail"]
    # runner-error distinguishes a crash sidecar from a config-STOP (config-error).
    assert data["reason"] == "runner-error"
    # D2 re-raises the original crash (bare ``raise``); under the default
    # catch_exceptions=True the CliRunner CAPTURES it into result.exception, proving
    # the wrapper wrote the sidecar AND re-raised rather than swallowing via sys.exit.
    assert isinstance(result.exception, RuntimeError)
