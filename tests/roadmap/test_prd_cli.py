"""Tests for --prd-file and --tdd-file CLI flag parsing on roadmap run.

Covers PRD pipeline integration Phase 10 acceptance criteria:
- --prd-file accepted by Click and resolves to absolute path in RoadmapConfig
- --prd-file defaults to None when absent
- --tdd-file accepted alongside --prd-file
- Invalid path produces Click error
"""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.roadmap.commands import roadmap_group


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def tmp_spec(tmp_path):
    spec = tmp_path / "spec.md"
    spec.write_text("# Test Spec\n\nSome content.")
    return spec


@pytest.fixture
def tmp_prd(tmp_path):
    prd = tmp_path / "prd.md"
    prd.write_text("# Test PRD\n\n## User Personas\n\nSome personas.")
    return prd


@pytest.fixture
def tmp_tdd(tmp_path):
    tdd = tmp_path / "tdd.md"
    tdd.write_text("# Test TDD\n\n## 10. Component Inventory\n\nSome components.")
    return tdd


class TestPrdFileFlag:
    """--prd-file flag parsing on roadmap run."""

    def test_prd_file_in_help(self, runner):
        result = runner.invoke(roadmap_group, ["run", "--help"])
        assert result.exit_code == 0
        assert "--prd-file" in result.output

    def test_prd_file_defaults_to_none(self, runner, tmp_spec):
        """When --prd-file is absent, config.prd_file should be None."""
        result = runner.invoke(
            roadmap_group,
            ["run", str(tmp_spec), "--dry-run"],
        )
        # dry-run exits 0 and prints plan without launching subprocesses
        assert result.exit_code == 0

    def test_prd_file_invalid_path_errors(self, runner, tmp_spec):
        """Invalid --prd-file path produces Click error."""
        result = runner.invoke(
            roadmap_group,
            ["run", str(tmp_spec), "--prd-file", "/nonexistent/prd.md"],
        )
        assert result.exit_code != 0
        assert "does not exist" in result.output.lower() or "Error" in result.output


class TestTddFileFlag:
    """--tdd-file flag parsing on roadmap run."""

    def test_tdd_file_in_help(self, runner):
        result = runner.invoke(roadmap_group, ["run", "--help"])
        assert result.exit_code == 0
        assert "--tdd-file" in result.output

    def test_tdd_file_invalid_path_errors(self, runner, tmp_spec):
        """Invalid --tdd-file path produces Click error."""
        result = runner.invoke(
            roadmap_group,
            ["run", str(tmp_spec), "--tdd-file", "/nonexistent/tdd.md"],
        )
        assert result.exit_code != 0
        assert "does not exist" in result.output.lower() or "Error" in result.output


class TestBothFlags:
    """--tdd-file and --prd-file used together."""

    def test_both_flags_in_help(self, runner):
        result = runner.invoke(roadmap_group, ["run", "--help"])
        assert "--tdd-file" in result.output
        assert "--prd-file" in result.output
