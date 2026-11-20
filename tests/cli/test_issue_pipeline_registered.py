"""Task 1: the ``issue-pipeline`` group is registered on the main CLI."""

from __future__ import annotations

from click.testing import CliRunner

from superclaude.cli.main import main


def test_issue_pipeline_group_is_registered() -> None:
    assert "issue-pipeline" in main.commands
    assert "issue-watch" in main.commands  # the neighbouring registration is untouched
    result = CliRunner().invoke(main, ["issue-pipeline", "--help"])
    assert result.exit_code == 0
    assert "plan-hash" in result.output
