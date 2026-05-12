"""Tests for _resolve_release_dir — tasklist subdirectory detection."""

from __future__ import annotations

from superclaude.cli.sprint.config import _resolve_release_dir


class TestResolveReleaseDir:
    """Test release directory resolution heuristic."""

    def test_index_in_release_dir_directly(self, tmp_path):
        """When index is directly in release dir, return parent as-is."""
        index = tmp_path / "tasklist-index.md"
        index.write_text("index")
        assert _resolve_release_dir(index) == tmp_path

    def test_tasklist_subdir_with_roadmap_state(self, tmp_path):
        """When index is in tasklist/ and grandparent has .roadmap-state.json."""
        tasklist_dir = tmp_path / "tasklist"
        tasklist_dir.mkdir()
        index = tasklist_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / ".roadmap-state.json").write_text("{}")

        assert _resolve_release_dir(index) == tmp_path

    def test_tasklist_subdir_with_spec_file(self, tmp_path):
        """When index is in tasklist/ and grandparent has *spec*.md."""
        tasklist_dir = tmp_path / "tasklist"
        tasklist_dir.mkdir()
        index = tasklist_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / "v3.3-requirements-spec.md").write_text("spec")

        assert _resolve_release_dir(index) == tmp_path

    def test_tasklist_subdir_no_indicators(self, tmp_path):
        """When index is in tasklist/ but grandparent has no indicators, fall back."""
        tasklist_dir = tmp_path / "tasklist"
        tasklist_dir.mkdir()
        index = tasklist_dir / "tasklist-index.md"
        index.write_text("index")
        # No .roadmap-state.json, no spec files

        assert _resolve_release_dir(index) == tasklist_dir

    def test_tasks_subdir_variant(self, tmp_path):
        """'tasks' directory name is also recognized."""
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        index = tasks_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / ".roadmap-state.json").write_text("{}")

        assert _resolve_release_dir(index) == tmp_path

    def test_tasklists_subdir_variant(self, tmp_path):
        """'tasklists' directory name is also recognized."""
        tl_dir = tmp_path / "tasklists"
        tl_dir.mkdir()
        index = tl_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / "my-spec.md").write_text("spec")

        assert _resolve_release_dir(index) == tmp_path

    def test_unrelated_subdir_name(self, tmp_path):
        """Arbitrary subdir name is not resolved to grandparent."""
        other_dir = tmp_path / "sprints"
        other_dir.mkdir()
        index = other_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / ".roadmap-state.json").write_text("{}")

        # "sprints" is not in the known set, so returns parent (= other_dir)
        assert _resolve_release_dir(index) == other_dir

    def test_case_insensitive(self, tmp_path):
        """Directory name matching is case-insensitive."""
        tl_dir = tmp_path / "Tasklist"
        tl_dir.mkdir()
        index = tl_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / ".roadmap-state.json").write_text("{}")

        assert _resolve_release_dir(index) == tmp_path
