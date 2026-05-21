"""Regression tests for _resolve_step_content in the PRD executor.

Guards the fix for the build-task-file gate HALT bug, where the gate
was measuring ~18 lines of NDJSON commentary against min_lines=400
instead of the 409-line task file on disk. Root cause: build-task-file
writes to a DYNAMIC filename (TASK-PRD-{product_slug}.md) so it
cannot live in the static _STEP_ARTIFACT_FILES dict. The fix adds a
special-case glob branch in _resolve_step_content.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.prd.executor import _resolve_step_content


def _write_lines(path: Path, n_lines: int, prefix: str = "line") -> str:
    """Write a file with n_lines lines and return the content."""
    content = "\n".join(f"{prefix} {i}" for i in range(n_lines)) + "\n"
    path.write_text(content, encoding="utf-8")
    return content


def test_build_task_file_returns_disk_content_not_ndjson(tmp_path: Path) -> None:
    """The build-task-file special-case returns the on-disk TASK-PRD-*.md content."""
    task_dir = tmp_path / "prd-fake"
    task_dir.mkdir()
    task_file = task_dir / "TASK-PRD-fake.md"
    on_disk = _write_lines(task_file, 450)

    ndjson_text = "short assistant commentary\nfewer than 20 lines"

    result = _resolve_step_content("build-task-file", task_dir, ndjson_text)

    assert result == on_disk, "expected on-disk task file content, got NDJSON or other"
    assert result != ndjson_text
    assert len(result.splitlines()) >= 400


def test_build_task_file_picks_largest_when_multiple_match(tmp_path: Path) -> None:
    """When multiple TASK-PRD-*.md files exist in task_dir, pick the largest."""
    task_dir = tmp_path / "prd-multi"
    task_dir.mkdir()
    _write_lines(task_dir / "TASK-PRD-small.md", 50, prefix="small")
    large_content = _write_lines(task_dir / "TASK-PRD-large.md", 420, prefix="large")
    _write_lines(task_dir / "TASK-PRD-medium.md", 200, prefix="medium")

    result = _resolve_step_content("build-task-file", task_dir, "ndjson")

    assert result == large_content


def test_build_task_file_does_not_search_parent_dir(tmp_path: Path) -> None:
    """The build-task-file glob is scoped to task_dir only, NOT task_dir.parent.

    A stray TASK-PRD-*.md in the parent directory must NOT be picked up,
    even if it is larger than anything in task_dir. This guards against
    multi-match ambiguity from prior failed runs in sibling directories.
    """
    parent = tmp_path / "parent"
    parent.mkdir()
    # Stray file in parent — must be ignored.
    _write_lines(parent / "TASK-PRD-stray.md", 500, prefix="stray")

    task_dir = parent / "prd-isolated"
    task_dir.mkdir()
    inside = _write_lines(task_dir / "TASK-PRD-real.md", 410, prefix="real")

    result = _resolve_step_content("build-task-file", task_dir, "ndjson")

    assert result == inside
    assert "stray" not in result


def test_build_task_file_falls_back_to_ndjson_when_no_match(tmp_path: Path) -> None:
    """When no TASK-PRD-*.md exists in task_dir, fall back to NDJSON text."""
    task_dir = tmp_path / "prd-empty"
    task_dir.mkdir()

    ndjson_text = "commentary only — no task file was written"

    result = _resolve_step_content("build-task-file", task_dir, ndjson_text)

    assert result == ndjson_text


def test_unknown_step_id_still_returns_ndjson(tmp_path: Path) -> None:
    """Regression guard: unknown step_id with no dict entry falls back to NDJSON.

    Ensures the build-task-file special-case did not break the existing
    fallback path for step IDs not in _STEP_ARTIFACT_FILES.
    """
    task_dir = tmp_path / "prd-unknown"
    task_dir.mkdir()

    ndjson_text = "ndjson for an unknown step"
    result = _resolve_step_content("some-unregistered-step", task_dir, ndjson_text)

    assert result == ndjson_text


def test_known_static_step_id_still_resolves_from_disk(tmp_path: Path) -> None:
    """Regression guard: existing static-name resolution (e.g. research-notes) is unaffected."""
    task_dir = tmp_path / "prd-research"
    task_dir.mkdir()
    notes = task_dir / "research-notes.md"
    on_disk = _write_lines(notes, 60, prefix="note")

    result = _resolve_step_content("research-notes", task_dir, "short ndjson")

    assert result == on_disk
