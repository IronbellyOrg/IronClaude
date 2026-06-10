"""AC-1: SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE recursion-breaker self-suppression.

The group-level guard must exit 0 BEFORE any launch when the marker == "1"
(contract Section 3), even for a since-moved tasklist (pre-empting Click's
`exists=True` validation). Negative controls prove ONLY the exact string "1"
suppresses -- "0"/absent/"2" run normally (the F2 too-loose-truthiness defense).
"""

from __future__ import annotations

from unittest.mock import patch

from superclaude.cli.reflect.commands import reflect_group

_MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"
_SUPPRESS_MSG = "recursion breaker"


def test_marker_one_suppresses_before_launch(
    cli_runner, temp_tasklist, monkeypatch
) -> None:
    """marker == "1" -> exit 0 and ClaudeProcess is NEVER constructed (AC-1)."""
    monkeypatch.setenv(_MARKER, "1")
    with patch("superclaude.cli.reflect.runner.ClaudeProcess") as mock_cls:
        result = cli_runner.invoke(reflect_group, ["run", str(temp_tasklist)])
    assert result.exit_code == 0
    mock_cls.assert_not_called()
    assert _SUPPRESS_MSG in result.output


def test_marker_one_suppresses_since_moved_file(cli_runner, monkeypatch) -> None:
    """marker == "1" pre-empts Click exists=True: a since-moved path still exits 0."""
    monkeypatch.setenv(_MARKER, "1")
    with patch("superclaude.cli.reflect.runner.ClaudeProcess") as mock_cls:
        result = cli_runner.invoke(
            reflect_group, ["run", "/no/such/since-moved-tasklist.md"]
        )
    assert result.exit_code == 0
    mock_cls.assert_not_called()
    assert _SUPPRESS_MSG in result.output


def _assert_not_suppressed(cli_runner, temp_tasklist, make_stub):
    """Helper: a non-suppressing marker proceeds to a real (stubbed) launch."""
    factory = make_stub("pass.yaml", rc=0)
    with patch(
        "superclaude.cli.reflect.runner.ClaudeProcess", side_effect=factory
    ) as mock_cls:
        result = cli_runner.invoke(reflect_group, ["run", str(temp_tasklist)])
    # NOT suppressed: the guard message is absent and a launch occurred.
    assert _SUPPRESS_MSG not in result.output
    assert mock_cls.call_count >= 1
    return result


def test_marker_zero_does_not_suppress(
    cli_runner,
    temp_tasklist,
    patch_git,
    patch_runner_env,
    make_claude_process_stub,
    monkeypatch,
) -> None:
    """marker == "0" must NOT suppress (only the string "1" does)."""
    monkeypatch.setenv(_MARKER, "0")
    _assert_not_suppressed(cli_runner, temp_tasklist, make_claude_process_stub)


def test_marker_absent_does_not_suppress(
    cli_runner,
    temp_tasklist,
    patch_git,
    patch_runner_env,
    make_claude_process_stub,
    monkeypatch,
) -> None:
    """marker absent (unset) must NOT suppress."""
    monkeypatch.delenv(_MARKER, raising=False)
    _assert_not_suppressed(cli_runner, temp_tasklist, make_claude_process_stub)


def test_marker_two_does_not_suppress(
    cli_runner,
    temp_tasklist,
    patch_git,
    patch_runner_env,
    make_claude_process_stub,
    monkeypatch,
) -> None:
    """marker == "2" must NOT suppress (guards against a too-loose truthiness check)."""
    monkeypatch.setenv(_MARKER, "2")
    _assert_not_suppressed(cli_runner, temp_tasklist, make_claude_process_stub)
