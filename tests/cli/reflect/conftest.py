"""Shared fixtures for the ``superclaude reflect run`` test suite.

Provides the fixtures directory constant, a ``CliRunner`` factory, and the
Idiom-B ``ClaudeProcess`` stub factory: a callable ``**kwargs`` -> MagicMock
whose ``.start()`` is a no-op and whose ``.wait()`` writes a chosen fixture
contract into ``<output_dir>/return-contract.yaml`` then returns a given rc.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


_FAKE_BASE = "1111111111111111111111111111111111111111"
_FAKE_HEAD = "2222222222222222222222222222222222222222"

_TASKLIST_TEMPLATE = """\
---
id: "TASK-TEST-0001"
title: "Test tasklist"
status: "🟠 Doing"
start_commit: "{base}"
spec_path: ""
reflect_post: ""
---

# Test tasklist

Body line one.
Body line two.
"""


@pytest.fixture
def cli_runner() -> CliRunner:
    """A fresh Click ``CliRunner``."""
    return CliRunner()


@pytest.fixture
def temp_tasklist(tmp_path) -> Path:
    """Write a minimal MDTM tasklist (frontmatter + body) and return its path.

    Carries ``start_commit`` (so ``<BASE>`` resolves without git) and a
    ``reflect_post: ""`` stub block for write-back tests.
    """
    path = tmp_path / "TASK-TEST-0001.md"
    path.write_text(_TASKLIST_TEMPLATE.format(base=_FAKE_BASE), encoding="utf-8")
    return path


@pytest.fixture
def patch_git(monkeypatch):
    """Stub ``config._git`` so resolve_config works without a real repo.

    Returns ``_FAKE_HEAD`` for ``rev-parse HEAD`` and ``_FAKE_BASE`` for any
    ``merge-base`` call. Exposes the two SHAs as attributes for assertions.
    """
    import superclaude.cli.reflect.config as config_mod

    def _fake_git(cwd, *args):
        if args and args[0] == "rev-parse":
            return _FAKE_HEAD
        if args and args[0] == "merge-base":
            return _FAKE_BASE
        return ""

    monkeypatch.setattr(config_mod, "_git", _fake_git)

    class _Git:
        base = _FAKE_BASE
        head = _FAKE_HEAD

    return _Git


@pytest.fixture
def patch_runner_env(monkeypatch):
    """Let the launch path proceed under test isolation.

    Stubs ``runner._child_env`` to a plain dict (so the throwaway
    ``ClaudeProcess`` is NOT constructed during the alias count -- keeping the
    patched ``ClaudeProcess`` call count equal to the real launches) and
    ``runner.shutil.which`` so the ``claude``-binary preflight passes.
    """
    import superclaude.cli.reflect.runner as runner_mod

    monkeypatch.setattr(runner_mod, "_child_env", lambda: {})
    monkeypatch.setattr(runner_mod.shutil, "which", lambda name: "/usr/bin/claude")


@pytest.fixture
def make_claude_process_stub():
    """Return an Idiom-B factory builder for stubbing ``ClaudeProcess``.

    Usage::

        factory = make_claude_process_stub("pass.yaml", rc=0)
        with patch("superclaude.cli.reflect.runner.ClaudeProcess", side_effect=factory):
            ...

    ``fixture_name=None`` (or ``write_contract=False``) simulates a run that
    writes NO contract (so the verdict routes ``blocked``). The factory writes
    the fixture from inside ``.wait()`` so the contract appears only after the
    "subprocess" completes, matching the real launch ordering.
    """

    def _builder(
        fixture_name: str | None = None, rc: int = 0, write_contract: bool = True
    ):
        fixture_bytes = b""
        if fixture_name is not None:
            fixture_bytes = (FIXTURES_DIR / fixture_name).read_bytes()

        def factory(**kwargs):
            output_file = Path(kwargs["output_file"])
            output_dir = output_file.parent
            mock = MagicMock()
            mock.start.return_value = None

            def _wait() -> int:
                if write_contract and fixture_name is not None:
                    output_dir.mkdir(parents=True, exist_ok=True)
                    (output_dir / "return-contract.yaml").write_bytes(fixture_bytes)
                return rc

            mock.wait.side_effect = _wait
            return mock

        return factory

    return _builder
