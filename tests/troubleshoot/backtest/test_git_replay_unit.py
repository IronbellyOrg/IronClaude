"""Unit tests for the git-replay helper -- subprocess-mocked, zero real git side effects.

Patches the MODULE-ALIASED ``git_replay._subprocess.run`` (mirroring
``tests/sprint/test_process.py``'s ``patch("...process._subprocess.run")`` convention) so the
checkout -> yield -> guaranteed-teardown control flow runs in milliseconds. Function names are
prefixed ``test_backtest_*`` to stay distinct from the impl suite's ``test_hardening_*`` nodeids.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from tests.troubleshoot.backtest import git_replay

_PATCH_TARGET = "tests.troubleshoot.backtest.git_replay._subprocess.run"


def _argvs(mock_run: MagicMock) -> list[list[str]]:
    """Return the argv list (first positional arg) of every recorded _subprocess.run call."""
    return [call.args[0] for call in mock_run.call_args_list]


def test_backtest_checkout_worktree_issues_detached_add_with_commitish_unchanged() -> (
    None
):
    with patch(_PATCH_TARGET) as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        with git_replay.checkout_worktree("94d5baa0") as wt:
            assert wt is not None

    argvs = _argvs(mock_run)
    add_calls = [a for a in argvs if a[:4] == ["git", "worktree", "add", "--detach"]]
    assert len(add_calls) == 1, f"expected exactly one detached add, got {argvs}"
    add = add_calls[0]
    # Argument order: ... add --detach <path> <commitish>  (path BEFORE commitish).
    assert add[-1] == "94d5baa0", (
        f"commitish must pass through unchanged, got {add[-1]!r}"
    )
    assert "^" not in add[-1], "commitish must carry NO caret (G1 no double-decrement)"
    # The path arg precedes the commitish and is the minted worktree dir.
    assert add[-2].endswith("wt"), (
        f"worktree path should precede commitish, got {add!r}"
    )


def test_backtest_checkout_worktree_teardown_fires_even_when_body_raises() -> None:
    sentinel = RuntimeError("boom inside replay body")
    with patch(_PATCH_TARGET) as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        with pytest.raises(RuntimeError) as excinfo:
            with git_replay.checkout_worktree("94d5baa0"):
                raise sentinel
        assert excinfo.value is sentinel  # original exception is NOT masked by teardown

    argvs = _argvs(mock_run)
    assert any(a[:4] == ["git", "worktree", "remove", "--force"] for a in argvs), (
        f"teardown must force-remove the worktree even on body exception, got {argvs}"
    )
    assert any(a[:3] == ["git", "worktree", "prune"] for a in argvs), (
        f"teardown must prune the admin record even on body exception, got {argvs}"
    )


def test_backtest_replay_escapes_has_exactly_five_bare_parent_shas() -> None:
    assert len(git_replay.REPLAY_ESCAPES) == 5
    by_id = {e.escape_id: e.prefix_parent_sha for e in git_replay.REPLAY_ESCAPES}
    assert by_id == {
        "E1": "94d5baa0",
        "E2": "10723863",
        "E3": "e97aa4fd",
        "E4": "1b0264f1",
        "E5": "d878bc6d",
    }
    for esc in git_replay.REPLAY_ESCAPES:
        assert "^" not in esc.prefix_parent_sha, (
            f"{esc.escape_id} prefix_parent_sha {esc.prefix_parent_sha!r} must be the BARE "
            "parent sha with NO caret (applying ^ double-decrements -> meaningless backtest)"
        )


def test_backtest_escape_by_id_round_trips_and_rejects_unknown() -> None:
    assert git_replay.escape_by_id("E4").prefix_parent_sha == "1b0264f1"
    assert git_replay.escape_by_id("E4").wave == "H2"
    with pytest.raises(KeyError):
        git_replay.escape_by_id("E99")
