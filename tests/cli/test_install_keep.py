"""Kept and overwritten installed files that differ from the shipped copy (#346 P3).

``install`` keeps an existing file and must name any kept file that differs from
this version's copy. ``install --force`` / ``update`` overwrite, so a differing
file is saved as ``<name>.bak.<UTC time>`` first, and a file whose save fails is
left untouched. A file that matches the shipped copy is never backed up.

A stale (older shipped) file and a user-edited file are the same case to the
installer, because only the current shipped bytes are known; both are covered.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli import install_keep
from superclaude.cli import install_user_setup as setup
from superclaude.cli.install_commands import install_commands
from superclaude.cli.install_keep import backup_if_differs, same_content

STYLE = "pragmatic.md"


def _style(home: Path) -> Path:
    return home / ".claude" / "output-styles" / STYLE


def _baks(directory: Path) -> list[Path]:
    return sorted(directory.glob("*.bak.*"))


# --- helpers -----------------------------------------------------------------


def test_same_content_is_true_only_for_identical_readable_files(tmp_path: Path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.write_text("x")
    b.write_text("x")
    assert same_content(a, b)
    b.write_text("y")
    assert not same_content(a, b)
    assert not same_content(a, tmp_path / "missing")


def test_backup_if_differs_returns_none_for_a_matching_file(tmp_path: Path):
    shipped, target = tmp_path / "s", tmp_path / "t"
    shipped.write_text("same")
    target.write_text("same")
    assert backup_if_differs(shipped, target) is None
    assert not _baks(tmp_path)


def test_backup_names_are_unique_within_one_second(tmp_path: Path):
    shipped, target = tmp_path / "s.md", tmp_path / "t.md"
    shipped.write_text("new")
    target.write_text("mine")
    first = backup_if_differs(shipped, target)
    second = backup_if_differs(shipped, target)
    assert first and second and first != second
    assert first.read_text() == second.read_text() == "mine"


# --- output styles ------------------------------------------------------------


def test_clean_home_installs_without_warning_or_backup(tmp_path: Path):
    ok, message = setup.install_output_styles(home=tmp_path)
    assert ok, message
    assert "differ" not in message and "Saved" not in message
    assert not _baks(_style(tmp_path).parent)


@pytest.mark.parametrize("content", ["an older shipped version\n", "my own edit\n"])
def test_install_keeps_a_differing_style_and_names_it(tmp_path: Path, content: str):
    assert setup.install_output_styles(home=tmp_path)[0]
    _style(tmp_path).write_text(content)
    ok, message = setup.install_output_styles(home=tmp_path)
    assert ok, message
    assert _style(tmp_path).read_text() == content  # kept
    assert "differ from this version" in message
    assert STYLE in message
    assert not _baks(_style(tmp_path).parent)  # nothing overwritten, nothing saved


@pytest.mark.parametrize("content", ["an older shipped version\n", "my own edit\n"])
def test_forced_install_saves_the_differing_style_then_replaces_it(
    tmp_path: Path, content: str
):
    assert setup.install_output_styles(home=tmp_path)[0]
    shipped = _style(tmp_path).read_text()
    _style(tmp_path).write_text(content)
    ok, message = setup.install_output_styles(home=tmp_path, force=True)
    assert ok, message
    assert _style(tmp_path).read_text() == shipped
    baks = _baks(_style(tmp_path).parent)
    assert len(baks) == 1 and baks[0].read_text() == content
    assert "Saved 1 changed output style" in message


def test_forced_install_of_a_matching_style_makes_no_backup(tmp_path: Path):
    assert setup.install_output_styles(home=tmp_path)[0]
    ok, message = setup.install_output_styles(home=tmp_path, force=True)
    assert ok, message
    assert "Saved" not in message
    assert not _baks(_style(tmp_path).parent)


def test_failed_save_leaves_the_file_untouched_and_reports_it(
    tmp_path: Path, monkeypatch
):
    assert setup.install_output_styles(home=tmp_path)[0]
    _style(tmp_path).write_text("my own edit\n")

    def boom(*_a, **_k):
        raise OSError("disk full")

    monkeypatch.setattr(install_keep.shutil, "copy2", boom)
    ok, message = setup.install_output_styles(home=tmp_path, force=True)
    assert not ok
    assert "left untouched" in message and "disk full" in message
    assert _style(tmp_path).read_text() == "my own edit\n"


# --- rules ---------------------------------------------------------------------


def test_rules_report_kept_differing_files_and_back_up_when_forced(tmp_path: Path):
    assert setup.install_rules(home=tmp_path)[0]
    rule = next((tmp_path / ".claude" / "rules").rglob("*.md"))
    rule.write_text("my own edit\n")
    ok, message = setup.install_rules(home=tmp_path)
    assert ok and "differ from this version" in message
    assert rule.read_text() == "my own edit\n"
    ok, message = setup.install_rules(home=tmp_path, force=True)
    assert ok and "Saved 1 changed rule file" in message
    assert [b.read_text() for b in _baks(rule.parent)] == ["my own edit\n"]


# --- commands ------------------------------------------------------------------


def test_commands_report_kept_differing_files_and_back_up_when_forced(tmp_path: Path):
    target = tmp_path / "sc"
    assert install_commands(target_path=target)[0]
    victim = sorted(target.glob("*.md"))[0]
    victim.write_text("my own edit\n")

    ok, message = install_commands(target_path=target)
    assert ok
    assert "differ from this version" in message and f"/{victim.stem}" in message
    assert victim.read_text() == "my own edit\n"
    assert not _baks(target)

    ok, message = install_commands(target_path=target, force=True)
    assert ok and "Saved 1 changed command" in message
    assert victim.read_text() != "my own edit\n"
    assert [b.read_text() for b in _baks(target)] == ["my own edit\n"]


def test_commands_clean_install_has_no_warning(tmp_path: Path):
    ok, message = install_commands(target_path=tmp_path / "sc")
    assert ok
    assert "differ" not in message and "Saved" not in message


def test_commands_failed_save_leaves_the_file_untouched(tmp_path: Path, monkeypatch):
    target = tmp_path / "sc"
    assert install_commands(target_path=target)[0]
    victim = sorted(target.glob("*.md"))[0]
    victim.write_text("my own edit\n")

    def boom(*_a, **_k):
        raise OSError("read-only")

    monkeypatch.setattr(install_keep.shutil, "copy2", boom)
    ok, message = install_commands(target_path=target, force=True)
    assert not ok and "left untouched" in message
    assert victim.read_text() == "my own edit\n"
