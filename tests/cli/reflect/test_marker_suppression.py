"""AC-1: SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE recursion-breaker self-suppression.

The group-level guard must exit 0 BEFORE any launch when the marker == "1"
(contract Section 3), even for a since-moved tasklist (pre-empting Click's
`exists=True` validation). Negative controls prove ONLY the exact string "1"
suppresses -- "0"/absent/"2" run normally (the F2 too-loose-truthiness defense).
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from superclaude.cli.reflect.commands import reflect_group

_MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"
_SUPPRESS_MSG = "recursion breaker"

# Source-of-truth skill file (NOT the .claude/ mirror): parents[3] of
# tests/cli/reflect/test_marker_suppression.py is the repo/worktree root.
_REPO_ROOT = Path(__file__).resolve().parents[3]
_REFLECT_SKILL_SRC = _REPO_ROOT / "src/superclaude/skills/sc-reflect-protocol/SKILL.md"


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


def _extract_execute_shell_command_envelope(text: str) -> str:
    """Extract the §6.1.1 execute_shell_command safety-envelope section.

    Uses stable heading anchors: the section starts at the §6.1.1 heading and
    ends at the next §6.2 heading.
    """
    start = text.index("### 6.1.1 `execute_shell_command` safety envelope")
    end = text.index("### 6.2", start)
    return text[start:end]


def test_verification_envelope_strips_reflect_wrapper_marker() -> None:
    """Regression guard (marker-leak bug): the §6.1.1 verification envelope MUST
    strip SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE from step-5.5 verification subprocesses.

    Without the env-strip control, a verification command that itself invokes
    ``superclaude reflect run`` (the reflect CLI's own tests) inherits the wrapper
    marker, trips the commands.py recursion-breaker guard, and produces a false
    degraded/null-convergence outcome on a clean audit.

    This is a source-contract test: the fix lives in the skill body
    (src/superclaude/skills/sc-reflect-protocol/SKILL.md §6.1.1 control (i)), so the
    assertion reads the source-of-truth skill text, NOT the .claude/ mirror. If the
    verification-command construction is ever moved into Python, this contract test
    MUST be superseded by a direct unit test proving that a marker-present input
    environment yields a marker-stripped verification invocation (env -u prefix or
    an env dict that omits the marker).
    """
    text = _REFLECT_SKILL_SRC.read_text(encoding="utf-8")
    envelope = _extract_execute_shell_command_envelope(text)
    # The envelope must explicitly account for the recursion-breaker marker...
    assert _MARKER in envelope
    # ...as a concrete env-strip command prefix, not vague prose.
    assert f"env -u {_MARKER}" in envelope
    # Hardening (reflect POST finding R2-1): the two assertions above ALSO pass if
    # control (i) is surgically deleted, because control (b)'s cross-reference
    # duplicates the `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` sentinel. Bind the
    # guard to control (i)'s own distinctive text (absent from control (b)) so the
    # test FAILS if the marker-strip control is removed, not merely if the string
    # appears somewhere in §6.1.1.
    assert "**(i) Wrapper-marker strip" in envelope
    assert "MUST be executed as the fixed protocol-authored wrapper" in envelope
