"""Suite-local fixtures for the differential backtest harness.

Mirrors the ``tests/cli/eval/conftest.py`` convention (unique scratch dir minted per test, best-effort
``shutil.rmtree`` teardown in ``finally``). Every report-output fixture here is ``tmp_path``-rooted and
never writes under ``docs/`` (where the root ``tests/conftest.py`` ``_pollution_snapshot`` autouse guard
watches for pollution).
"""

from __future__ import annotations

import shutil
import tempfile
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture
def replay_scratch_root() -> Iterator[Path]:
    """Yield a unique throwaway directory for git-worktree replay checkouts.

    Minted with a uuid suffix so concurrent/repeated tests never collide, and removed best-effort in
    ``finally`` (``ignore_errors=True`` so a still-open fd never crashes the suite).

    NOTE: this only reaps the checkout DIRECTORY. ``git_replay.checkout_worktree`` STILL must run
    ``git worktree remove --force`` + ``git worktree prune`` itself, because the
    ``.git/worktrees/<name>/`` admin record lives in the shared common-dir and is NOT removed by
    deleting the checkout dir (G3).
    """
    root = Path(tempfile.gettempdir()) / f"backtest-replay-{uuid.uuid4().hex[:12]}"
    root.mkdir(parents=True, exist_ok=True)
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


@pytest.fixture
def catch_rate_output_dir(tmp_path: Path) -> Path:
    """Return a ``tmp_path``-rooted directory for writing catch-rate artifacts.

    Explicitly NOT under ``docs/`` (where the ``_pollution_snapshot`` autouse guard watches for
    pollution). ``tmp_path`` is per-test and auto-cleaned by pytest, so the catch-rate.json /
    catch-rate.md the writer emits never pollute the tree.
    """
    out = tmp_path / "catch-rate-out"
    out.mkdir(parents=True, exist_ok=True)
    return out
