"""Regression tests for _resolve_step_content in the PRD executor.

Guards the fix for the build-task-file gate HALT bug, where the gate
was measuring ~18 lines of NDJSON commentary against min_lines=400
instead of the 409-line task file on disk. Root cause: build-task-file
writes to a DYNAMIC filename (TASK-PRD-{product_slug}.md) so it
cannot live in the static _STEP_ARTIFACT_FILES dict. The fix adds a
special-case glob branch in _resolve_step_content.
"""

from __future__ import annotations

import os
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


# ---------------------------------------------------------------------------
# Layer 2 hotfix acceptance tests (AC3-AC6)
# ---------------------------------------------------------------------------


def test_variant_filename_recovered_from_where_subdir(tmp_path: Path) -> None:
    """[AC3] A variant-named scope-discovery doc in a WHERE subdir is recovered.

    The agent dropped the canonical ``-raw`` suffix and wrote
    ``scope-discovery.md`` into a WHERE source/spec directory. The
    pattern-aware backstop must recover that real document instead of the
    short NDJSON commentary.
    """
    task_dir = tmp_path / "prd-variant"
    task_dir.mkdir()
    (task_dir / "parsed-request.json").write_text(
        '{"GOAL": "g", "WHERE": [".dev/specs"]}', encoding="utf-8"
    )
    where_dir = task_dir / ".dev" / "specs"
    where_dir.mkdir(parents=True)
    # Canonical name is scope-discovery-raw.md; this is the dropped-suffix variant.
    on_disk = _write_lines(where_dir / "scope-discovery.md", 60, prefix="scope")

    ndjson_text = "\n".join(f"commentary line {i}" for i in range(24)) + "\n"

    result = _resolve_step_content("scope-discovery", task_dir, ndjson_text)

    assert result == on_disk
    assert result != ndjson_text
    assert len(result.splitlines()) >= 50


def test_freshness_outranks_size_inv006(tmp_path: Path) -> None:
    """[AC4] A fresher SHORTER file beats a stale LONGER file (INV-006).

    Both candidates sit inside task_dir (equal preferred-root rank), so the
    mtime tiebreak decides. The deterministic picker must rank freshness above
    raw content length, else a stale longer artifact from a prior failed run
    would silently win.
    """
    task_dir = tmp_path / "prd-fresh"
    task_dir.mkdir()
    (task_dir / "parsed-request.json").write_text(
        '{"GOAL": "g", "WHERE": [".dev/specs"]}', encoding="utf-8"
    )
    stale_dir = task_dir / ".dev" / "specs"
    stale_dir.mkdir(parents=True)
    stale_long = stale_dir / "scope-discovery.md"
    _write_lines(stale_long, 120, prefix="stale")
    os.utime(stale_long, (1_000_000, 1_000_000))  # OLD mtime

    fresh_short = task_dir / "scope-discovery-raw.md"
    fresh_content = _write_lines(fresh_short, 55, prefix="fresh")
    os.utime(fresh_short, (2_000_000, 2_000_000))  # NEWER mtime

    result = _resolve_step_content("scope-discovery", task_dir, "ndjson fallback")

    assert result == fresh_content
    assert len(result.splitlines()) < 120


def test_where_traversal_escape_excluded_inv005(tmp_path: Path) -> None:
    """[AC5] A WHERE entry escaping the repo root via '..' is not searched (INV-005).

    A candidate document reachable only via a ``..``-traversal WHERE entry
    (outside the repo_root = task_dir.parent) must be rejected by the realpath
    containment guard, so its content is never returned.
    """
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    task_dir = repo_root / "prd-task"
    task_dir.mkdir()

    outside = tmp_path / "outside"
    outside.mkdir()
    # Longer than anything in-bounds — would win on size if not excluded.
    escaped_content = _write_lines(
        outside / "scope-discovery.md", 200, prefix="escaped"
    )

    (task_dir / "parsed-request.json").write_text(
        '{"GOAL": "g", "WHERE": ["../outside"]}', encoding="utf-8"
    )

    ndjson_text = "ndjson commentary fallback\nsecond line"
    result = _resolve_step_content("scope-discovery", task_dir, ndjson_text)

    assert result != escaped_content
    assert result == ndjson_text


def test_zero_match_returns_ndjson_fallback(tmp_path: Path) -> None:
    """[AC6] No matching artifact and no WHERE dirs -> NDJSON fallback, no crash.

    Regression guard over the existing zero-match behavior preserved by the
    hotfix: the function returns ndjson_text exactly as today.
    """
    task_dir = tmp_path / "prd-empty-scope"
    task_dir.mkdir()

    ndjson_text = "only commentary — no scope-discovery file was written"
    result = _resolve_step_content("scope-discovery", task_dir, ndjson_text)

    assert result == ndjson_text


# ---------------------------------------------------------------------------
# Assembly gate content resolution (TASK-PRD-*.md exclusion)
# ---------------------------------------------------------------------------


def test_assembly_excludes_task_file_and_picks_real_prd(tmp_path: Path) -> None:
    """The assembly gate must read the assembled PRD, not the TASK-PRD task file.

    The build-task-file MDTM task (``TASK-PRD-{slug}.md``) lives in task_dir and
    also contains "prd", so the ``"prd" in name`` filter matches it. Because the
    assembly search visits task_dir before task_dir.parent and breaks on the
    first dir with a candidate, the task file was being selected and the real
    assembled PRD (written to the output dir = task_dir.parent) was never seen —
    failing the min_lines gate on the wrong document. The TASK- exclusion fixes
    this.
    """
    parent = tmp_path / "out"
    parent.mkdir()
    task_dir = parent / "prd-myproduct"
    task_dir.mkdir()
    # build-task-file artifact in task_dir — contains "prd", must be excluded.
    _write_lines(task_dir / "TASK-PRD-myproduct.md", 450, prefix="task")
    # The real assembled PRD lives in the output dir (task_dir.parent).
    real = _write_lines(parent / "myproduct-prd.md", 900, prefix="prd")

    result = _resolve_step_content("assembly", task_dir, "ndjson commentary")

    assert result == real, "assembly must select the assembled PRD, not the task file"
    assert len(result.splitlines()) >= 800
    assert "task" not in result


def test_assembly_falls_back_to_ndjson_when_only_task_file_present(
    tmp_path: Path,
) -> None:
    """If the only "prd" file is the excluded TASK-PRD task file, fall through.

    Guards that the TASK- exclusion does not accidentally return the task file;
    with no real PRD on disk the assembly branch yields no candidate and the
    resolver falls back to the NDJSON text.
    """
    parent = tmp_path / "out2"
    parent.mkdir()
    task_dir = parent / "prd-only-task"
    task_dir.mkdir()
    _write_lines(task_dir / "TASK-PRD-only.md", 450, prefix="task")

    ndjson_text = "assembly commentary — no assembled PRD written yet"
    result = _resolve_step_content("assembly", task_dir, ndjson_text)

    assert result == ndjson_text
    assert "task" not in result
