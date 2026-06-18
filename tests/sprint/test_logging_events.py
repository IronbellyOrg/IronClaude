"""Non-mock SprintLogger regression tests for the 429-recovery events.

Why non-mock (reflect D1): every executor test uses ``logger = MagicMock()``, which
auto-fabricates ANY attribute — so a call to ``logger.write_session_reset(...)``
succeeds (and even ``.call_count`` asserts) EVEN IF the real ``SprintLogger`` lacks
the method. That masked a HIGH regression where the methods were absent. These tests
instantiate a REAL ``SprintLogger`` so a missing/renamed method fails loudly and
MagicMock can never hide it again.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.sprint.logging_ import SprintLogger
from superclaude.cli.sprint.models import Phase, SprintConfig


def _logger(tmp_path: Path) -> SprintLogger:
    pf = tmp_path / "phase-1-tasklist.md"
    pf.write_text("# Phase 1\n")
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")
    config = SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf, name="Phase 1")],
    )
    return SprintLogger(config)


@pytest.mark.unit
def test_sprint_logger_defines_429_event_methods():
    # D1 guard: the REAL class must DEFINE both methods (not a MagicMock auto-attr).
    # `executor.py` calls them on a real SprintLogger; a missing method would
    # AttributeError on the recovery path at runtime.
    assert callable(getattr(SprintLogger, "write_session_reset", None))
    assert callable(getattr(SprintLogger, "write_account_exhaustion_halt", None))


@pytest.mark.unit
def test_write_session_reset_emits_event(tmp_path):
    logger = _logger(tmp_path)
    logger.write_session_reset(2, "T02.05", 3, "claude-opus-4-8")
    ev = json.loads(logger.config.execution_log_jsonl.read_text().splitlines()[-1])
    assert ev["event"] == "session_reset"
    assert ev["phase"] == 2
    assert ev["task_id"] == "T02.05"
    assert ev["attempt"] == 3
    assert ev["exhausted_model"] == "claude-opus-4-8"
    assert "timestamp" in ev


@pytest.mark.unit
def test_write_account_exhaustion_halt_emits_event(tmp_path):
    logger = _logger(tmp_path)
    logger.write_account_exhaustion_halt(2, "T02.05", "claude-opus-4-8", 8)
    ev = json.loads(logger.config.execution_log_jsonl.read_text().splitlines()[-1])
    assert ev["event"] == "account_exhaustion_halt"
    assert ev["phase"] == 2
    assert ev["task_id"] == "T02.05"
    assert ev["exhausted_model"] == "claude-opus-4-8"
    assert ev["session_resets"] == 8
    assert "timestamp" in ev
