"""Unit tests for superclaude.cli.prd.inventory.

Section 8.1 test plan: 5 tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.prd.inventory import (
    check_existing_work,
    create_task_dirs,
    discover_research_files,
    discover_synth_files,
    select_template,
)
from superclaude.cli.prd.models import ExistingWorkState, PrdConfig


class TestCheckExistingWork:
    """Existing work detection with 4-state results."""

    def test_check_existing_work_no_existing(self, tmp_path: Path) -> None:
        """Returns NO_EXISTING when no task dirs exist."""
        config = PrdConfig(
            work_dir=tmp_path,
            product_name="TestProduct",
            product_slug="test-product",
        )
        result = check_existing_work(config)
        assert result == ExistingWorkState.NO_EXISTING

    def test_check_existing_work_resume_stage_b(
        self, tmp_path: Path
    ) -> None:
        """Detects existing task file with research but no results."""
        # Create task dir structure with slug in name
        tasks_root = tmp_path / ".dev" / "tasks" / "to-do"
        task_dir = tasks_root / "TASK-PRD-test-product-001"
        research_dir = task_dir / "research"
        research_dir.mkdir(parents=True)

        # Create a completed research file
        (research_dir / "research-01.md").write_text(
            "# Product Capabilities\nContent here."
        )

        # Create a task file for content matching
        (task_dir / "task.md").write_text(
            "---\ntitle: TestProduct PRD\n---\nTask content"
        )

        config = PrdConfig(
            work_dir=tmp_path,
            product_name="TestProduct",
            product_slug="test-product",
        )
        result = check_existing_work(config)
        assert result == ExistingWorkState.RESUME_STAGE_B


class TestSelectTemplate:
    """Template selection based on PRD scope."""

    def test_select_template(self) -> None:
        assert select_template("product") == 2
        assert select_template("Product") == 2
        assert select_template("feature") == 1
        assert select_template("update") == 1
        assert select_template("") == 1


class TestDiscoverResearchFiles:
    """Research file discovery with completion filtering."""

    def test_discover_research_files(self, tmp_path: Path) -> None:
        """Finds completed research files, skips incomplete."""
        research_dir = tmp_path / "research"
        research_dir.mkdir()

        # Completed file
        (research_dir / "research-01.md").write_text(
            "# Product Capabilities\nFull content here."
        )
        # Incomplete file
        (research_dir / "research-02.md").write_text(
            "# Technical Architecture\n[INCOMPLETE] - needs more work"
        )
        # Empty file (should be skipped)
        (research_dir / "research-03.md").write_text("")

        files = discover_research_files(tmp_path)
        assert len(files) == 1
        assert files[0].name == "research-01.md"

    def test_discover_research_files_no_dir(self, tmp_path: Path) -> None:
        """Returns empty list when research dir doesn't exist."""
        assert discover_research_files(tmp_path) == []


class TestDiscoverSynthFiles:
    """Synthesis file discovery with pattern matching."""

    def test_discover_synth_files(self, tmp_path: Path) -> None:
        """Finds synth files matching synth-*.md pattern."""
        synth_dir = tmp_path / "synthesis"
        synth_dir.mkdir()

        (synth_dir / "synth-01-exec.md").write_text("content")
        (synth_dir / "synth-02-business.md").write_text("content")
        (synth_dir / "other-file.md").write_text("content")  # should not match

        files = discover_synth_files(tmp_path)
        assert len(files) == 2
        assert files[0].name == "synth-01-exec.md"
        assert files[1].name == "synth-02-business.md"


class TestCreateTaskDirs:
    """Task directory creation."""

    def test_create_task_dirs(self, tmp_path: Path) -> None:
        task_dir = tmp_path / "my-task"
        task_dir.mkdir()
        create_task_dirs(task_dir)

        for subdir in ("research", "synthesis", "qa", "reviews", "results"):
            assert (task_dir / subdir).is_dir(), f"{subdir} not created"
