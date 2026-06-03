"""Shared fixtures for the tests/recommend/ suite.

Mirrors the ``tests/roadmap/`` CLI-submodule precedent (own ``__init__.py`` +
``conftest.py``) but stays minimal: the recommend tests only need a tmp_path-based
cache-path fixture so they never write to the real ``.claude/cache/``.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def cache_path(tmp_path: Path) -> Path:
    """A throwaway lookup-cache YAML path under the test's tmp_path."""
    return tmp_path / "sc-recommend-lookup.yaml"


@pytest.fixture
def events_path(tmp_path: Path) -> Path:
    """A throwaway telemetry JSONL path under the test's tmp_path."""
    return tmp_path / "sc-recommend-events.jsonl"
