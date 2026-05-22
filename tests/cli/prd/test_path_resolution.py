"""Regression tests: PRD CLI path resolution is anchored to ``.claude/``.

These tests guard against the bug where ``superclaude prd run`` crashed
with ``FileNotFoundError: 'src/superclaude/skills/prd/refs/build-request-template.md'``
whenever invoked from any CWD outside the IronClaude repo (PR
fix/prd-path-resolution-and-templates).

The architectural invariant under test: ``_default_skill_refs_dir`` and
``_default_template_path`` MUST resolve to absolute ``.claude/``-anchored
paths (project-local first, user-home second), with a dev-tree fallback
for editable installs. They MUST NEVER return a relative path that
would silently resolve against the user's CWD.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.prd.config import _discover_skill_refs_dir
from superclaude.cli.prd.models import (
    _default_skill_refs_dir,
    _default_template_path,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _isolate_paths(
    monkeypatch: pytest.MonkeyPatch,
    *,
    cwd: Path,
    home: Path,
) -> None:
    """Pin ``Path.cwd`` and ``Path.home`` to specific tmp paths.

    Hides the real user CWD/home from the resolution helpers so the test
    can deterministically control which candidate "exists."
    """
    monkeypatch.setattr(Path, "cwd", classmethod(lambda cls: cwd))
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))


def _make_refs(parent: Path) -> Path:
    refs = parent / ".claude" / "skills" / "prd" / "refs"
    refs.mkdir(parents=True)
    # Drop a marker file so a downstream consumer's exists()-check works
    (refs / "build-request-template.md").write_text("# stub\n", encoding="utf-8")
    return refs


def _make_template(parent: Path) -> Path:
    template = parent / ".claude" / "templates" / "workflow" / "05_prd_template.md"
    template.parent.mkdir(parents=True)
    template.write_text("# stub\n", encoding="utf-8")
    return template


# ---------------------------------------------------------------------------
# _default_skill_refs_dir
# ---------------------------------------------------------------------------


def test_skill_refs_prefers_cwd_project_claude(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """``<cwd>/.claude/skills/prd/refs`` wins over ``~/.claude/skills/prd/refs``."""
    cwd = tmp_path / "proj"
    home = tmp_path / "home"
    cwd.mkdir()
    home.mkdir()
    cwd_refs = _make_refs(cwd)
    _make_refs(home)  # home also has it, but cwd should win
    _isolate_paths(monkeypatch, cwd=cwd, home=home)

    assert _default_skill_refs_dir() == cwd_refs
    assert _discover_skill_refs_dir() == cwd_refs  # delegate parity


def test_skill_refs_falls_back_to_home_claude(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """When cwd has no ``.claude/skills/prd/refs``, ``~/.claude/...`` wins."""
    cwd = tmp_path / "proj"
    home = tmp_path / "home"
    cwd.mkdir()
    home.mkdir()
    # cwd intentionally has NO .claude/
    home_refs = _make_refs(home)
    _isolate_paths(monkeypatch, cwd=cwd, home=home)

    assert _default_skill_refs_dir() == home_refs


def test_skill_refs_falls_back_to_dev_tree(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """When neither .claude/ exists but ``<cwd>/src/.../refs`` does, use it."""
    cwd = tmp_path / "proj"
    home = tmp_path / "home"
    cwd.mkdir()
    home.mkdir()
    dev_refs = cwd / "src" / "superclaude" / "skills" / "prd" / "refs"
    dev_refs.mkdir(parents=True)
    _isolate_paths(monkeypatch, cwd=cwd, home=home)

    assert _default_skill_refs_dir() == dev_refs


def test_skill_refs_returns_absolute_home_path_on_total_miss(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """When NOTHING resolves, return the home candidate (absolute, not relative).

    Critical invariant: even on a total miss, the result must be an
    absolute path so any subsequent ``FileNotFoundError`` cites an
    absolute path the user can paste into ``ls``. Returning a relative
    path here is the original bug.
    """
    cwd = tmp_path / "proj"
    home = tmp_path / "home"
    cwd.mkdir()
    home.mkdir()
    _isolate_paths(monkeypatch, cwd=cwd, home=home)

    result = _default_skill_refs_dir()
    assert result.is_absolute(), (
        f"refs path must be absolute; got relative path {result!r} — "
        f"this is the regression the PR fixes."
    )
    assert result == home / ".claude" / "skills" / "prd" / "refs"
    assert not result.exists()  # documents the miss


# ---------------------------------------------------------------------------
# _default_template_path
# ---------------------------------------------------------------------------


def test_template_path_prefers_cwd_project_claude(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """``<cwd>/.claude/templates/workflow/05_prd_template.md`` wins."""
    cwd = tmp_path / "proj"
    home = tmp_path / "home"
    cwd.mkdir()
    home.mkdir()
    cwd_tpl = _make_template(cwd)
    _make_template(home)
    _isolate_paths(monkeypatch, cwd=cwd, home=home)

    assert _default_template_path() == cwd_tpl


def test_template_path_falls_back_to_home_claude(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """When cwd has no template, ``~/.claude/templates/...`` wins."""
    cwd = tmp_path / "proj"
    home = tmp_path / "home"
    cwd.mkdir()
    home.mkdir()
    home_tpl = _make_template(home)
    _isolate_paths(monkeypatch, cwd=cwd, home=home)

    assert _default_template_path() == home_tpl


def test_template_path_falls_back_to_dev_tree(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Dev fallback for editable installs run from the IronClaude repo root."""
    cwd = tmp_path / "proj"
    home = tmp_path / "home"
    cwd.mkdir()
    home.mkdir()
    dev_tpl = cwd / "src" / "superclaude" / "templates" / "workflow" / "05_prd_template.md"
    dev_tpl.parent.mkdir(parents=True)
    dev_tpl.write_text("# stub\n", encoding="utf-8")
    _isolate_paths(monkeypatch, cwd=cwd, home=home)

    assert _default_template_path() == dev_tpl


def test_template_path_returns_absolute_home_path_on_total_miss(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Even on total miss the result is an absolute path."""
    cwd = tmp_path / "proj"
    home = tmp_path / "home"
    cwd.mkdir()
    home.mkdir()
    _isolate_paths(monkeypatch, cwd=cwd, home=home)

    result = _default_template_path()
    assert result.is_absolute()
    assert (
        result
        == home / ".claude" / "templates" / "workflow" / "05_prd_template.md"
    )
    assert not result.exists()
