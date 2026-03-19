"""Integration tests for sprint post-task wiring hook with all 4 mode tests.

Tests:
1. off mode skips analysis entirely
2. shadow mode logs findings without changing task status (SC-006)
3. soft mode warns on critical findings
4. full mode blocks on critical+major findings
5. Pre-activation safeguards emit warnings for misconfigured provider_dir_names (SC-010)
"""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from superclaude.cli.sprint.executor import (
    run_post_task_wiring_hook,
    run_wiring_safeguard_checks,
)
from superclaude.cli.sprint.models import (
    GateOutcome,
    SprintConfig,
    TaskEntry,
    TaskResult,
    TaskStatus,
)


def _make_task() -> TaskEntry:
    return TaskEntry(task_id="T05.01", title="Test task for wiring hook")


def _make_result(task: TaskEntry, status: TaskStatus = TaskStatus.PASS) -> TaskResult:
    return TaskResult(task=task, status=status)


def _make_config(tmp_path: Path, mode: str) -> SprintConfig:
    """Create a SprintConfig with a source dir containing scannable Python files."""
    release_dir = tmp_path / "release"
    release_dir.mkdir(exist_ok=True)
    # Write a Python file with an unwired Optional[Callable] to produce findings
    (release_dir / "sample.py").write_text(
        "from typing import Optional, Callable\n"
        "\n"
        "class Foo:\n"
        "    def __init__(self, hook: Optional[Callable] = None):\n"
        "        self.hook = hook\n"
    )
    return SprintConfig(
        wiring_gate_mode=mode,
        release_dir=release_dir,
    )


def _make_clean_config(tmp_path: Path, mode: str) -> SprintConfig:
    """Create a SprintConfig with no findings (clean codebase)."""
    release_dir = tmp_path / "clean_release"
    release_dir.mkdir(exist_ok=True)
    (release_dir / "clean.py").write_text("x = 1\n")
    return SprintConfig(
        wiring_gate_mode=mode,
        release_dir=release_dir,
    )


class TestOffMode:
    """off mode skips analysis entirely."""

    def test_off_mode_returns_unchanged_result(self, tmp_path):
        task = _make_task()
        config = _make_config(tmp_path, "off")
        result = _make_result(task)

        returned = run_post_task_wiring_hook(task, config, result)

        assert returned.status == TaskStatus.PASS
        assert returned is result  # same object, not modified

    def test_off_mode_no_analysis_executed(self, tmp_path, caplog):
        """off mode should not run any wiring analysis (no log messages)."""
        task = _make_task()
        config = _make_config(tmp_path, "off")
        result = _make_result(task)

        with caplog.at_level(logging.DEBUG, logger="superclaude.sprint.wiring_hook"):
            run_post_task_wiring_hook(task, config, result)

        # No wiring hook log messages should appear
        wiring_messages = [r for r in caplog.records if "Wiring hook" in r.message]
        assert len(wiring_messages) == 0


class TestShadowMode:
    """shadow mode logs findings without changing task status (SC-006)."""

    def test_shadow_mode_status_unchanged_with_findings(self, tmp_path):
        """SC-006: Task status MUST remain unchanged in shadow mode even with findings."""
        task = _make_task()
        config = _make_config(tmp_path, "shadow")
        result = _make_result(task)

        returned = run_post_task_wiring_hook(task, config, result)

        assert returned.status == TaskStatus.PASS

    def test_shadow_mode_logs_findings(self, tmp_path, caplog):
        task = _make_task()
        config = _make_config(tmp_path, "shadow")
        result = _make_result(task)

        with caplog.at_level(logging.INFO, logger="superclaude.sprint.wiring_hook"):
            run_post_task_wiring_hook(task, config, result)

        info_msgs = [r for r in caplog.records if "Wiring hook" in r.message]
        assert len(info_msgs) >= 1

    def test_shadow_mode_clean_codebase_no_change(self, tmp_path):
        task = _make_task()
        config = _make_clean_config(tmp_path, "shadow")
        result = _make_result(task)

        returned = run_post_task_wiring_hook(task, config, result)

        assert returned.status == TaskStatus.PASS


class TestSoftMode:
    """soft mode warns on critical findings."""

    def test_soft_mode_warns_on_critical(self, tmp_path, caplog):
        task = _make_task()
        config = _make_config(tmp_path, "soft")
        result = _make_result(task)

        with caplog.at_level(logging.WARNING, logger="superclaude.sprint.wiring_hook"):
            returned = run_post_task_wiring_hook(task, config, result)

        # Status should NOT change in soft mode
        assert returned.status == TaskStatus.PASS

        # Should have warning about critical findings
        warning_msgs = [
            r for r in caplog.records
            if r.levelno >= logging.WARNING and "critical" in r.message.lower()
        ]
        assert len(warning_msgs) >= 1

    def test_soft_mode_clean_no_warning(self, tmp_path, caplog):
        task = _make_task()
        config = _make_clean_config(tmp_path, "soft")
        result = _make_result(task)

        with caplog.at_level(logging.WARNING, logger="superclaude.sprint.wiring_hook"):
            returned = run_post_task_wiring_hook(task, config, result)

        assert returned.status == TaskStatus.PASS
        critical_warnings = [
            r for r in caplog.records
            if r.levelno >= logging.WARNING and "critical" in r.message.lower()
        ]
        assert len(critical_warnings) == 0


class TestFullMode:
    """full mode blocks on critical+major findings."""

    def test_full_mode_blocks_with_findings(self, tmp_path):
        task = _make_task()
        config = _make_config(tmp_path, "full")
        result = _make_result(task)

        returned = run_post_task_wiring_hook(task, config, result)

        # Full mode with critical findings should mark FAIL
        assert returned.status == TaskStatus.FAIL
        assert returned.gate_outcome == GateOutcome.FAIL

    def test_full_mode_passes_clean_codebase(self, tmp_path):
        task = _make_task()
        config = _make_clean_config(tmp_path, "full")
        result = _make_result(task)

        returned = run_post_task_wiring_hook(task, config, result)

        assert returned.status == TaskStatus.PASS

    def test_full_mode_logs_error(self, tmp_path, caplog):
        task = _make_task()
        config = _make_config(tmp_path, "full")
        result = _make_result(task)

        with caplog.at_level(logging.ERROR, logger="superclaude.sprint.wiring_hook"):
            run_post_task_wiring_hook(task, config, result)

        error_msgs = [
            r for r in caplog.records
            if r.levelno >= logging.ERROR and "blocking" in r.message.lower()
        ]
        assert len(error_msgs) >= 1


class TestSafeguards:
    """Pre-activation safeguards emit warnings (SC-010)."""

    def test_missing_provider_dirs_produce_warnings(self, tmp_path):
        """SC-010: misconfigured provider_dir_names should produce warnings."""
        config = SprintConfig(release_dir=tmp_path)
        warnings = run_wiring_safeguard_checks(config)

        provider_warnings = [w for w in warnings if "Provider directory" in w]
        assert len(provider_warnings) >= 1

    def test_zero_match_warning(self, tmp_path):
        config = SprintConfig(release_dir=tmp_path)

        class MockReport:
            files_analyzed = 100
            total_findings = 0

        warnings = run_wiring_safeguard_checks(config, report=MockReport())
        zero_match = [w for w in warnings if "Zero-match" in w]
        assert len(zero_match) == 1

    def test_invalid_whitelist_produces_warning(self, tmp_path):
        wl_dir = tmp_path / "src" / "superclaude" / "cli" / "audit"
        wl_dir.mkdir(parents=True)
        (wl_dir / "wiring_whitelist.yaml").write_text(": invalid {{}")

        config = SprintConfig(release_dir=tmp_path)
        warnings = run_wiring_safeguard_checks(config)

        wl_warnings = [w for w in warnings if "Whitelist" in w]
        assert len(wl_warnings) == 1

    def test_safeguards_do_not_block_execution(self, tmp_path):
        """Safeguard warnings should never raise or block."""
        config = SprintConfig(release_dir=tmp_path)
        # This should complete without exception even with invalid state
        warnings = run_wiring_safeguard_checks(config)
        assert isinstance(warnings, list)
