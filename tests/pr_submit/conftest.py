"""Shared fixtures for the ``tests/pr_submit`` suite (spec §6.3).

Provides ``load_fixture`` (the JSON fixture loader), ``mock_gh`` (in-process
monkeypatch of the ``pr_submit`` gh-wrapper seam, recording argv to assert the
``--repo`` pin), ``mock_monitor`` (stubs Monitor arming), ``fixture_findings``
(loads a finding set), and ``tmp_skill_dir`` (a ``tmp_path``-based skill dir). The
in-process monkeypatch is preferred over a PATH-shim for unit speed (research/04 §D).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def load_fixture():
    """Return a loader: ``load_fixture("name.json")`` → parsed JSON from ``fixtures/``."""

    def _load(name: str):
        return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))

    return _load


@pytest.fixture
def mock_gh(monkeypatch):
    """Monkeypatch the ``detection`` poll seam to a fixture-returning fake; record calls.

    Returns a recorder object: set ``recorder.payload`` to control the returned poll
    payload; read ``recorder.calls`` (a list of pr_num args) to assert invocations.
    Keeps tests in-process (no subprocess) per the repo's unit-speed precedent.
    """
    from superclaude.pr_submit import detection

    class _MockGh:
        def __init__(self) -> None:
            self.calls: list = []
            self.payload: dict = {"reviews": [], "comments": []}

        def fetch(self, pr_num):
            self.calls.append(pr_num)
            return dict(self.payload)

    recorder = _MockGh()
    monkeypatch.setattr(detection, "_fetch_payload", recorder.fetch)
    return recorder


@pytest.fixture
def mock_monitor():
    """A stand-in for the Monitor arming seam — records each arm call."""

    class _MockMonitor:
        def __init__(self) -> None:
            self.calls = 0

        def __call__(self, *_args, **_kwargs) -> None:
            self.calls += 1

    return _MockMonitor()


@pytest.fixture
def fixture_findings():
    """Load the default finding set (the medium+high AC-2 fixture)."""
    return json.loads(
        (FIXTURES_DIR / "finding-medium-high.json").read_text(encoding="utf-8")
    )


@pytest.fixture
def tmp_skill_dir(tmp_path, monkeypatch):
    """A tmp_path-based skill/output dir for run-log and artifact writes."""
    d = tmp_path / "pr-monitor"
    d.mkdir(parents=True, exist_ok=True)
    return d
