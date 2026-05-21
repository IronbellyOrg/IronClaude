"""Tests for the ``claude.min_version`` HARD check (T02.20 / D-0039 / R-039).

R1-mit pins the supported ``claude`` CLI version range and enforces it
inside ``eval doctor`` via :func:`_check_claude_version`. The floor is
sourced from :class:`EvalConfig.min_claude_version` (default
:data:`DEFAULT_MIN_CLAUDE_VERSION` = ``(0, 5, 0)``) so the policy lives
in one place — the doctor module does not embed a duplicate copy.

These tests cover the four acceptance criteria from the phase tasklist:

1. ``_check_claude_version()`` rejects claude installations below the
   floor; doctor exits 2 when invoked against such a stub.
2. A reference fixture stubbing ``claude --version`` at ``0.4.0`` fails
   the doctor check (the canonical "below floor" boundary value).
3. The version floor is sourced from :class:`EvalConfig` — the doctor
   module never reads a hard-coded constant.
4. The minimum is recorded as ``0.5.0`` (matches D-0039 spec).
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.eval import commands as doctor_module
from superclaude.cli.eval.commands import (
    HARD_FAIL_EXIT_CODE,
    _check_claude_version,
    build_doctor_report,
    eval_group,
)
from superclaude.cli.eval.config import DEFAULT_MIN_CLAUDE_VERSION, EvalConfig

# ---------------------------------------------------------------------------
# EvalConfig policy: the floor is single-sourced from config.
# ---------------------------------------------------------------------------


def test_default_min_claude_version_is_0_5_0() -> None:
    """T02.20 AC: ``min_version 0.5.0 recorded`` (D-0039 policy)."""
    assert DEFAULT_MIN_CLAUDE_VERSION == (0, 5, 0)


def test_eval_config_exposes_min_claude_version_field() -> None:
    cfg = EvalConfig()
    assert cfg.min_claude_version == DEFAULT_MIN_CLAUDE_VERSION


def test_eval_config_min_claude_version_is_overridable() -> None:
    """The floor must be reconfigurable from EvalConfig (not patched in doctor)."""
    cfg = EvalConfig(min_claude_version=(1, 2, 3))
    assert cfg.min_claude_version == (1, 2, 3)


# ---------------------------------------------------------------------------
# Floor enforcement: 0.4.0 stub fails; >= 0.5.0 passes.
# ---------------------------------------------------------------------------


def test_check_claude_version_rejects_0_4_0_stub() -> None:
    """Reference fixture: ``claude --version`` -> ``claude 0.4.0`` fails."""
    status = _check_claude_version(probe=lambda: "claude 0.4.0")
    assert status.passed is False
    assert status.failure_mode == "hard"
    assert "< required 0.5.0" in status.detail


def test_check_claude_version_passes_at_floor() -> None:
    status = _check_claude_version(probe=lambda: "claude 0.5.0")
    assert status.passed is True
    assert status.failure_mode == "hard"


def test_check_claude_version_passes_above_floor() -> None:
    status = _check_claude_version(probe=lambda: "claude 0.5.7")
    assert status.passed is True


# ---------------------------------------------------------------------------
# Floor source-of-truth: must come from EvalConfig, not doctor module.
# ---------------------------------------------------------------------------


def test_check_claude_version_floor_sourced_from_eval_config() -> None:
    """Raising the EvalConfig floor changes the check without touching doctor."""
    strict_cfg = EvalConfig(min_claude_version=(0, 9, 0))
    status = _check_claude_version(
        probe=lambda: "claude 0.5.0",
        config=strict_cfg,
    )
    assert status.passed is False
    assert "< required 0.9.0" in status.detail
    assert "Claude CLI >= 0.9.0" == status.description


def test_check_claude_version_lowered_floor_lets_old_release_pass() -> None:
    """Lowering the EvalConfig floor lets a previously-rejected build pass."""
    permissive_cfg = EvalConfig(min_claude_version=(0, 3, 0))
    status = _check_claude_version(
        probe=lambda: "claude 0.4.0",
        config=permissive_cfg,
    )
    assert status.passed is True


def test_check_claude_version_explicit_min_version_kw_still_wins() -> None:
    """Tests retain the legacy explicit ``min_version=`` kwarg override."""
    status = _check_claude_version(
        probe=lambda: "claude 0.5.0",
        min_version=(0, 6, 0),
    )
    assert status.passed is False
    assert "< required 0.6.0" in status.detail


def test_doctor_module_does_not_define_hardcoded_floor_constant() -> None:
    """Guard: the doctor module must not embed a duplicate version constant."""
    assert not hasattr(doctor_module, "_MIN_CLAUDE_VERSION")


# ---------------------------------------------------------------------------
# build_doctor_report wires the EvalConfig floor through to the report.
# ---------------------------------------------------------------------------


def test_build_doctor_report_uses_config_floor(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    (tmp_path / ".claude").mkdir()
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: "claude 0.5.5",
    )
    strict_cfg = EvalConfig(min_claude_version=(0, 9, 0))
    report = build_doctor_report(config=strict_cfg)
    assert "claude.min_version" in report.hard_failures
    by_name = {row.name: row for row in report.report}
    assert by_name["claude.min_version"].description == "Claude CLI >= 0.9.0"


def test_build_doctor_report_default_config_uses_0_5_0(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    (tmp_path / ".claude").mkdir()
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: "claude 0.5.0",
    )
    report = build_doctor_report()
    assert "claude.min_version" not in report.hard_failures
    by_name = {row.name: row for row in report.report}
    assert by_name["claude.min_version"].description == "Claude CLI >= 0.5.0"


# ---------------------------------------------------------------------------
# CLI surface: doctor exits 2 when stubbed claude --version reports 0.4.0.
# ---------------------------------------------------------------------------


def test_cli_doctor_exits_two_when_stub_reports_0_4_0(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """T02.20 validation: stub claude binary at 0.4.0; doctor exits 2."""
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    (tmp_path / ".claude").mkdir()
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: "claude 0.4.0",
    )
    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor"])
    assert result.exit_code == HARD_FAIL_EXIT_CODE
    assert "claude.min_version" in result.stderr
    assert "< required 0.5.0" in result.stderr
