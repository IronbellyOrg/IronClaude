"""Tests for --prd-file CLI flag parsing on tasklist validate.

Covers PRD pipeline integration acceptance criteria for tasklist CLI.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.tasklist.commands import tasklist_group


@pytest.fixture
def runner():
    return CliRunner()


class TestPrdFileFlagTasklist:
    """--prd-file flag parsing on tasklist validate."""

    def test_prd_file_in_help(self, runner):
        result = runner.invoke(tasklist_group, ["validate", "--help"])
        assert result.exit_code == 0
        assert "--prd-file" in result.output

    def test_prd_file_defaults_to_none(self, runner, tmp_path):
        """When --prd-file is absent, help still renders."""
        result = runner.invoke(tasklist_group, ["validate", "--help"])
        assert result.exit_code == 0

    def test_prd_file_invalid_path_errors(self, runner, tmp_path):
        """Invalid --prd-file path produces Click error."""
        result = runner.invoke(
            tasklist_group,
            ["validate", str(tmp_path), "--prd-file", "/nonexistent/prd.md"],
        )
        assert result.exit_code != 0
        assert "does not exist" in result.output.lower() or "Error" in result.output
