"""Shared fixtures for the Run ledger tests: no test starts a process unless it is marked
``integration`` (same idea as ``tests/sweep/conftest.py``)."""

from __future__ import annotations

import os
import subprocess

import pytest


@pytest.fixture(autouse=True)
def no_subprocess(request, monkeypatch):
    """Raise on any process start, except for a test whose own decorator marks ``integration``."""
    marks = getattr(request.function, "pytestmark", [])  # own decorator marks only
    if any(m.name == "integration" for m in marks):
        return

    def _blocked(*args, **kwargs):
        raise AssertionError(
            "run_ledger tests must not start a process; use a fake runner"
        )

    monkeypatch.setattr(subprocess, "run", _blocked)
    monkeypatch.setattr(subprocess, "Popen", _blocked)
    monkeypatch.setattr(os, "system", _blocked)
