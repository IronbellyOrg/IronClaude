"""CR-1 / IM-1 coverage: the ``--isolate-reviewers`` CLI passthrough and the
COR-1 base-resolves STOP in ``create_review_snapshot``.

1. CLI passthrough — invoking ``reflect run --isolate-reviewers`` threads
   ``isolate_reviewers=True`` into ``resolve_config`` (captured kwarg); the
   default (no flag) yields ``isolate_reviewers=False``.
2. base-STOP — ``create_review_snapshot`` returns ``(None, "no-committable-ref")``
   when ``<base>`` does NOT resolve (the base ``rev-parse --verify`` raises),
   BEFORE any ``git worktree add``.

Falsifier discipline: fails-before (no flag wired / no base check) and
passes-after (CR-1 + IM-1 landed).
"""

from __future__ import annotations

import subprocess
from unittest.mock import patch

from superclaude.cli.reflect.commands import reflect_group
from superclaude.cli.reflect.config import _audit_tree_dirty, create_review_snapshot


def _capture_resolve_config(monkeypatch):
    """Patch ``config.resolve_config`` to record the kwargs it was called with.

    Returns the capture dict. The stub raises ``ValueError`` so the command
    short-circuits at the config-STOP handler (exit 2) without launching a
    runner -- we only care that the kwarg reached ``resolve_config``.
    """
    import superclaude.cli.reflect.config as config_mod

    captured: dict = {}

    def _fake_resolve(*args, **kwargs):
        captured.update(kwargs)
        raise ValueError("captured")

    monkeypatch.setattr(config_mod, "resolve_config", _fake_resolve)
    return captured


def test_isolate_reviewers_flag_threads_true(
    cli_runner, temp_tasklist, monkeypatch
) -> None:
    """CR-1: ``--isolate-reviewers`` reaches ``resolve_config`` as True."""
    captured = _capture_resolve_config(monkeypatch)
    result = cli_runner.invoke(
        reflect_group, ["run", str(temp_tasklist), "--isolate-reviewers"]
    )
    # Config-STOP -> exit 2 (the ValueError handler), but the kwarg was captured.
    assert result.exit_code == 2
    assert captured.get("isolate_reviewers") is True


def test_isolate_reviewers_default_is_false(
    cli_runner, temp_tasklist, monkeypatch
) -> None:
    """CR-1: the DEFAULT (no flag) yields ``isolate_reviewers=False``."""
    captured = _capture_resolve_config(monkeypatch)
    result = cli_runner.invoke(reflect_group, ["run", str(temp_tasklist)])
    assert result.exit_code == 2
    assert captured.get("isolate_reviewers") is False


def test_no_isolate_reviewers_flag_is_false(
    cli_runner, temp_tasklist, monkeypatch
) -> None:
    """CR-1: the explicit ``--no-isolate-reviewers`` negation yields False."""
    captured = _capture_resolve_config(monkeypatch)
    result = cli_runner.invoke(
        reflect_group, ["run", str(temp_tasklist), "--no-isolate-reviewers"]
    )
    assert result.exit_code == 2
    assert captured.get("isolate_reviewers") is False


def test_audit_tree_dirty_checks_repo_root_scope(tmp_path) -> None:
    """COR-5: task-dir tasklists still check the repo-wide audit diff."""
    repo_root = tmp_path / "repo"
    task_dir = repo_root / ".dev" / "tasks" / "to-do" / "TASK-RF-demo"
    task_dir.mkdir(parents=True)
    calls: list[tuple[str, tuple[str, ...]]] = []

    def _fake_git(cwd, *args):
        calls.append((str(cwd), args))
        if args == ("rev-parse", "--show-toplevel"):
            return str(repo_root)
        if args[:2] == ("diff", "--name-only"):
            assert cwd == repo_root
            return "src/superclaude/cli/reflect/config.py"
        if args == ("status", "--porcelain=v1"):
            assert cwd == repo_root
            return " M src/superclaude/cli/reflect/config.py"
        raise AssertionError(args)

    with patch("superclaude.cli.reflect.config._git", side_effect=_fake_git):
        assert _audit_tree_dirty(task_dir, "base-ref") is True

    assert (str(task_dir), ("rev-parse", "--show-toplevel")) in calls


def test_isolate_reviewers_flag_in_help(cli_runner) -> None:
    """CR-1: the flag is documented in ``run --help``."""
    result = cli_runner.invoke(reflect_group, ["run", "--help"])
    assert result.exit_code == 0
    assert "--isolate-reviewers" in result.output
    assert "--no-isolate-reviewers" in result.output


class _SnapshotConfig:
    """Minimal duck-typed config for ``create_review_snapshot`` unit tests."""

    def __init__(self, tmp_path, base="deadbeef", head="cafef00d"):
        self.tasklist_path = tmp_path / "TASK.md"
        self.tasklist_path.write_text("x", encoding="utf-8")
        self.output_dir = tmp_path / "out"
        self.base = base
        self.head = head


def test_base_does_not_resolve_stops_no_committable_ref(tmp_path) -> None:
    """IM-1 / COR-1: an unresolvable ``<base>`` STOPs ``no-committable-ref``
    BEFORE any ``git worktree add``.

    The patched ``_git`` raises on the base ``rev-parse --verify`` probe; a
    ``worktree add`` reaching git would be a contract violation, asserted via
    the recorded call args.
    """
    config = _SnapshotConfig(tmp_path)
    calls: list[tuple[str, ...]] = []

    def _fake_git(cwd, *args):
        calls.append(args)
        # The base committability probe: rev-parse --verify <base>^{commit}.
        if args[:2] == ("rev-parse", "--verify"):
            raise subprocess.SubprocessError("bad ref")
        return ""

    with patch("superclaude.cli.reflect.config._git", side_effect=_fake_git):
        snapshot, reason = create_review_snapshot(config)

    assert snapshot is None
    assert reason == "no-committable-ref"
    # The base probe must have fired, and no worktree add may have been attempted.
    assert any(a[:2] == ("rev-parse", "--verify") for a in calls)
    assert not any(a[:2] == ("worktree", "add") for a in calls)


def test_base_resolves_proceeds_past_base_check(tmp_path) -> None:
    """IM-1 negative-witness: when ``<base>`` resolves AND HEAD matches, the
    base check does NOT STOP and the helper proceeds to ``worktree add``.
    """
    config = _SnapshotConfig(tmp_path)

    def _fake_git(cwd, *args):
        if args[:2] == ("rev-parse", "--verify"):
            return config.base  # base resolves
        if args[0] == "rev-parse":  # rev-parse HEAD
            return config.head  # HEAD unchanged -> no head-moved STOP
        return ""  # worktree add succeeds

    with patch("superclaude.cli.reflect.config._git", side_effect=_fake_git):
        snapshot, reason = create_review_snapshot(config)

    # Proceeded past the base + HEAD checks to a successful snapshot.
    assert reason is None
    assert snapshot == config.output_dir / "_review-snapshot"
