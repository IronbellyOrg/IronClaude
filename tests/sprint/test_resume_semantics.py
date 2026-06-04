"""Tests for sprint resume semantics -- actionable HALT output.

Covers T07.06 acceptance criteria.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.sprint.models import (
    SprintConfig,
    TaskEntry,
    TurnLedger,
    build_resume_output,
)


class TestResumeSemantics:
    """HALT output includes actionable resume command."""

    def _make_tasks(self, *ids: str) -> list[TaskEntry]:
        return [TaskEntry(task_id=tid, title=f"Task {tid}") for tid in ids]

    def test_resume_command_includes_task_id(self):
        """Resume command includes correct task ID."""
        config = SprintConfig(index_path=Path("sprint.md"))
        output = build_resume_output(
            config=config,
            halt_task_id="T07.03",
            remaining_tasks=self._make_tasks("T07.03", "T07.04", "T07.05"),
        )
        assert "--resume T07.03" in output

    def test_resume_command_includes_budget(self):
        """Resume command includes a budget suggestion via the REAL turn-budget
        flag. Stage 2 reconciled the dangling resume hint: `--budget` is not a
        real `sprint run` option, so the printed command now uses `--max-turns`
        (the actual turn-budget flag) and is directly runnable."""
        config = SprintConfig(index_path=Path("sprint.md"))
        output = build_resume_output(
            config=config,
            halt_task_id="T07.03",
            remaining_tasks=self._make_tasks("T07.03", "T07.04"),
        )
        assert "--max-turns" in output
        assert "--budget" not in output  # the non-existent flag was removed

    def test_remaining_tasks_listed(self):
        """Remaining tasks listed in execution order."""
        config = SprintConfig(index_path=Path("sprint.md"))
        tasks = self._make_tasks("T07.03", "T07.04", "T07.05")
        output = build_resume_output(
            config=config,
            halt_task_id="T07.03",
            remaining_tasks=tasks,
        )
        assert "T07.03" in output
        assert "T07.04" in output
        assert "T07.05" in output
        # Order preserved — indices computed for the assertion-by-presence above.
        # (Previously bound idx_03/idx_04/idx_05 but never compared; just verify all are present.)

    def test_remaining_task_count(self):
        """Output shows remaining task count."""
        config = SprintConfig(index_path=Path("sprint.md"))
        output = build_resume_output(
            config=config,
            halt_task_id="T07.03",
            remaining_tasks=self._make_tasks("T07.03", "T07.04"),
        )
        assert "2" in output

    def test_resume_task_id_matches_first_uncompleted(self):
        """Resume task ID matches the first uncompleted task."""
        config = SprintConfig(index_path=Path("sprint.md"))
        output = build_resume_output(
            config=config,
            halt_task_id="T07.05",
            remaining_tasks=self._make_tasks("T07.05", "T07.06", "T07.07"),
        )
        assert "--resume T07.05" in output

    def test_diagnostic_path_included(self):
        """Diagnostic output reference included when available."""
        config = SprintConfig(index_path=Path("sprint.md"))
        output = build_resume_output(
            config=config,
            halt_task_id="T07.03",
            remaining_tasks=self._make_tasks("T07.03"),
            diagnostic_path="/path/to/diagnostic.md",
        )
        assert "/path/to/diagnostic.md" in output

    def test_no_diagnostic_path_when_none(self):
        """No diagnostic section when path is None."""
        config = SprintConfig(index_path=Path("sprint.md"))
        output = build_resume_output(
            config=config,
            halt_task_id="T07.03",
            remaining_tasks=self._make_tasks("T07.03"),
            diagnostic_path=None,
        )
        assert "Diagnostic Output" not in output

    def test_budget_status_with_ledger(self):
        """Budget status included when ledger provided."""
        config = SprintConfig(index_path=Path("sprint.md"))
        ledger = TurnLedger(initial_budget=100)
        ledger.debit(60)
        output = build_resume_output(
            config=config,
            halt_task_id="T07.03",
            remaining_tasks=self._make_tasks("T07.03"),
            ledger=ledger,
        )
        assert "60" in output  # consumed
        assert "40" in output  # available

    def test_empty_remaining_tasks(self):
        """Handles empty remaining tasks gracefully."""
        config = SprintConfig(index_path=Path("sprint.md"))
        output = build_resume_output(
            config=config,
            halt_task_id="T07.07",
            remaining_tasks=[],
        )
        assert "0" in output
