"""Kept and overwritten installed files that differ from the shipped copy (#346 P3).

``install`` keeps an existing file and must name any kept file that differs from
this version's copy. ``install --force`` / ``update`` overwrite, so a differing
file is saved as ``<name>.bak.<UTC time>`` first, and a file whose save fails is
left untouched. A file that matches the shipped copy is never backed up.

A stale (older shipped) file and a user-edited file are the same case to the
installer, because only the current shipped bytes are known; both are covered.
"""

from __future__ import annotations

import errno
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, NamedTuple

import pytest

from superclaude.cli import install_keep
from superclaude.cli import install_templates as templates_mod
from superclaude.cli import install_user_setup as setup
from superclaude.cli.install_agents import install_agents, list_installed_agents
from superclaude.cli.install_commands import install_commands
from superclaude.cli.install_core import (
    KNOWN_CORE_FILES,
    install_core_files,
    list_installed_core_files,
)
from superclaude.cli.install_keep import backup_if_differs, same_content

STYLE = "pragmatic.md"


def _style(home: Path) -> Path:
    return home / ".claude" / "output-styles" / STYLE


def _baks(directory: Path) -> list[Path]:
    return sorted(directory.glob("*.bak.*"))


# --- helpers -----------------------------------------------------------------


def _rewrite_keeping_stat(path: Path, text: str) -> None:
    """Rewrite ``path`` and restore its old times, so its size and mtime match
    what ``filecmp`` cached, as when a rewrite lands in the same timestamp tick."""
    before = path.stat()
    path.write_text(text)
    os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
    assert path.stat().st_mtime == before.st_mtime


def test_same_content_is_true_only_for_identical_readable_files(tmp_path: Path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.write_text("x")
    b.write_text("x")
    assert same_content(a, b)
    _rewrite_keeping_stat(b, "y")
    assert not same_content(a, b)
    assert not same_content(a, tmp_path / "missing")


def test_same_content_sees_a_rewrite_that_keeps_size_and_mtime(tmp_path: Path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.write_text("x")
    b.write_text("x")
    assert same_content(a, b)
    _rewrite_keeping_stat(b, "y")
    assert not same_content(a, b)
    _rewrite_keeping_stat(b, "x")
    assert same_content(a, b)


def test_core_install_reports_a_kept_file_rewritten_with_the_same_size_and_mtime(
    tmp_path: Path,
):
    assert install_core_files(target_path=tmp_path)[0]
    ok, message = install_core_files(target_path=tmp_path)  # compares every file
    assert ok and "differ" not in message
    victim = next(tmp_path.glob("*.md"))
    _rewrite_keeping_stat(victim, "z" * victim.stat().st_size)
    ok, message = install_core_files(target_path=tmp_path)
    assert ok and "differ from this version" in message and victim.name in message


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


# --- core files, agents and templates (one table, one row per installer) ---------


class _Row(NamedTuple):
    id: str
    install: Callable  # (target, force) -> (ok, message)
    target: Callable  # (tmp_path) -> installer target folder
    victims: (
        Callable  # (target) -> sorted shipped files in the target, first is the victim
    )
    noun: str  # as in "Saved N changed <noun>(s)"
    key: Callable  # (victim, target) -> name the failure line starts with
    kept_note: bool  # a plain install names a kept file that differs


_ROWS = {
    row.id: row
    for row in (
        _Row(
            id="core",
            install=lambda t, f: install_core_files(target_path=t, force=f),
            target=lambda tmp: tmp / ".claude",
            victims=lambda t: sorted(t.glob("*.md")),
            noun="core file",
            key=lambda v, t: v.name,
            kept_note=True,
        ),
        _Row(
            id="agents",
            install=lambda t, f: install_agents(target_path=t, force=f),
            target=lambda tmp: tmp / "agents",
            victims=lambda t: sorted(t.glob("*.md")),
            noun="agent",
            key=lambda v, t: v.stem,
            kept_note=False,
        ),
        _Row(
            id="templates",
            install=lambda t, f: templates_mod.install_templates(
                target_path=t, force=f
            ),
            target=lambda tmp: tmp / "templates",
            victims=lambda t: sorted(
                p for p in (t / "workflow").rglob("*") if p.is_file()
            ),
            noun="template",
            key=lambda v, t: str(v.relative_to(t)),
            kept_note=False,
        ),
    )
}


@pytest.fixture(params=list(_ROWS), ids=list(_ROWS))
def row(request) -> _Row:
    return _ROWS[request.param]


def _victim_baks(victim: Path) -> list[Path]:
    """Backups of this one file; a stray file in the folder cannot change the count."""
    return sorted(victim.parent.glob(victim.name + ".bak.*"))


def _edit(victim: Path) -> bytes:
    shipped = victim.read_bytes()
    victim.write_bytes(b"my own edit\n")
    return shipped


def _wrap_copy(monkeypatch, fail_on: Callable, error: Exception) -> list[Path]:
    """Wrap the copy every installer and the helper call; record each destination and
    raise ``error`` when ``fail_on(dst)``. Failing only the victim's copy keeps the
    other files processable."""
    real = install_keep.shutil.copy2
    seen: list[Path] = []

    def wrapper(src, dst, *args, **kwargs):
        seen.append(Path(dst))
        if fail_on(Path(dst)):
            raise error
        return real(src, dst, *args, **kwargs)

    monkeypatch.setattr(install_keep.shutil, "copy2", wrapper)
    return seen


def _backup_only(victim: Path) -> Callable:
    return lambda dst: dst.name.startswith(victim.name + ".bak.")


def _replacement_only(victim: Path) -> Callable:
    return lambda dst: dst == victim


def _freeze_clock(monkeypatch) -> None:
    class _Frozen:
        @staticmethod
        def now(tz=None):
            return datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)

    monkeypatch.setattr(install_keep, "datetime", _Frozen)


def _installed_target(row: _Row, tmp_path: Path) -> tuple[Path, Path]:
    target = row.target(tmp_path)
    ok, message = row.install(target, False)
    assert ok, message
    return target, row.victims(target)[0]


def test_forced_install_saves_a_differing_file_then_replaces_it(row, tmp_path):
    target, victim = _installed_target(row, tmp_path)
    shipped = _edit(victim)
    ok, message = row.install(target, True)
    assert ok, message
    assert victim.read_bytes() == shipped
    baks = _victim_baks(victim)
    assert [b.read_bytes() for b in baks] == [b"my own edit\n"]
    assert f"Saved 1 changed {row.noun}" in message and str(baks[0]) in message
    # a saved file still counts as installed (FR-042)
    assert f"   - {row.key(victim, target)}" in message.split("💾")[0]


def test_forced_install_of_a_matching_or_missing_file_makes_no_backup(row, tmp_path):
    target = row.target(tmp_path)
    ok, message = row.install(target, True)  # empty target: nothing to save
    assert ok, message
    assert "Saved" not in message
    ok, message = row.install(target, True)  # every file matches
    assert ok, message
    assert "Saved" not in message
    assert not list(target.rglob("*.bak.*"))


def test_a_second_forced_run_makes_no_further_backup(row, tmp_path):
    target, victim = _installed_target(row, tmp_path)
    _edit(victim)
    assert row.install(target, True)[0]
    ok, message = row.install(target, True)
    assert ok, message
    assert "Saved" not in message
    assert len(_victim_baks(victim)) == 1


def test_plain_install_keeps_the_edit_and_makes_no_backup(row, tmp_path):
    target, victim = _installed_target(row, tmp_path)
    _edit(victim)
    ok, message = row.install(target, False)
    assert ok, message
    assert victim.read_bytes() == b"my own edit\n"
    assert not _victim_baks(victim)
    assert ("differ from this version" in message) == row.kept_note
    if not row.kept_note:
        assert "differ" not in message


def test_core_kept_note_names_the_bak_naming(tmp_path):
    row = _ROWS["core"]
    target, victim = _installed_target(row, tmp_path)
    _edit(victim)
    ok, message = row.install(target, False)
    assert ok, message
    assert "saved as <name>.bak.<time> first" in message


@pytest.mark.parametrize(
    "error",
    [PermissionError("denied"), OSError(errno.ENOSPC, "No space left on device")],
    ids=["permission", "enospc"],
)
def test_failed_save_leaves_the_file_untouched(row, tmp_path, monkeypatch, error):
    target, victim = _installed_target(row, tmp_path)
    second = row.victims(target)[1]
    second_shipped = _edit(second)
    _edit(victim)
    seen = _wrap_copy(monkeypatch, _backup_only(victim), error)
    ok, message = row.install(target, True)
    assert not ok
    assert (
        f"{row.key(victim, target)}: could not save a copy first, left untouched"
        in message
    )
    assert str(error) in message
    assert victim.read_bytes() == b"my own edit\n"
    assert [d for d in seen if d == victim] == []  # the replacement was never attempted
    assert not _victim_baks(victim)
    # another file in the same run is saved and replaced
    assert second.read_bytes() == second_shipped
    assert [b.read_bytes() for b in _victim_baks(second)] == [b"my own edit\n"]


def test_save_then_failed_replacement_keeps_the_backup(row, tmp_path, monkeypatch):
    target, victim = _installed_target(row, tmp_path)
    _edit(victim)
    _wrap_copy(monkeypatch, _replacement_only(victim), OSError("boom"))
    ok, message = row.install(target, True)
    assert not ok
    baks = _victim_baks(victim)
    assert [b.read_bytes() for b in baks] == [b"my own edit\n"]
    before_failed, failed_block = message.split("❌ Failed", 1)
    assert "💾 Saved" in before_failed  # the saved block comes before the failed block
    assert str(baks[0]) in before_failed.split("💾 Saved", 1)[1]
    assert f"{row.key(victim, target)}: boom" in failed_block


def test_backup_names_do_not_collide_on_one_instant(row, tmp_path, monkeypatch):
    target, victim = _installed_target(row, tmp_path)
    _freeze_clock(monkeypatch)
    victim.write_bytes(b"first edit\n")
    assert row.install(target, True)[0]
    victim.write_bytes(b"second edit\n")
    assert row.install(target, True)[0]
    first, second = _victim_baks(victim)
    assert second.name == first.name + "-2"
    assert first.read_bytes() == b"first edit\n"
    assert second.read_bytes() == b"second edit\n"


def test_same_size_same_mtime_edit_is_saved_when_forced(row, tmp_path):
    target, victim = _installed_target(row, tmp_path)
    shipped = victim.read_bytes()
    assert shipped
    _rewrite_keeping_stat(victim, "z" * len(shipped))
    ok, message = row.install(target, True)
    assert ok, message
    assert victim.read_bytes() == shipped
    assert [b.read_bytes() for b in _victim_baks(victim)] == [b"z" * len(shipped)]


def test_directory_at_the_victim_path_fails_closed(row, tmp_path):
    target, victim = _installed_target(row, tmp_path)
    victim.unlink()
    victim.mkdir()
    ok, message = row.install(target, True)
    assert not ok
    assert (
        f"{row.key(victim, target)}: could not save a copy first, left untouched"
        in message
    )
    assert victim.is_dir()
    assert not _victim_baks(victim)


# --- templates only: content, nesting, excluded folder, listings --------------------


def test_empty_and_binary_content_is_saved_exactly(tmp_path):
    row = _ROWS["templates"]
    target, victim = _installed_target(row, tmp_path)
    victim.write_bytes(b"")
    assert row.install(target, True)[0]
    binary = b"head\x00middle\xfftail"
    victim.write_bytes(binary)
    assert row.install(target, True)[0]
    assert sorted(b.read_bytes() for b in _victim_baks(victim)) == [b"", binary]


def test_nested_template_backup_and_excluded_folder(tmp_path, monkeypatch):
    row = _ROWS["templates"]
    target, victim = _installed_target(row, tmp_path)
    _edit(victim)
    assert row.install(target, True)[0]
    baks = _victim_baks(victim)
    assert len(baks) == 1 and baks[0].parent == victim.parent  # its own subfolder

    # The installer visits source files only, so the protected folder is tested with a
    # temporary source that holds one: a target-only file would pass without the guard.
    source = tmp_path / "source"
    (source / "agent-memory").mkdir(parents=True)
    (source / "agent-memory" / "x.md").write_text("shipped memory\n")
    (source / "workflow").mkdir()
    (source / "workflow" / "y.md").write_text("shipped y\n")
    other = tmp_path / "other"
    (other / "agent-memory").mkdir(parents=True)
    (other / "agent-memory" / "x.md").write_text("USER MEMORY\n")
    (other / "workflow").mkdir()
    (other / "workflow" / "y.md").write_text("edited y\n")
    monkeypatch.setattr(templates_mod, "_get_templates_source", lambda: source)
    ok, message = templates_mod.install_templates(target_path=other, force=True)
    assert ok, message
    assert (other / "agent-memory" / "x.md").read_text() == "USER MEMORY\n"
    assert not list((other / "agent-memory").glob("x.md.bak.*"))
    assert [b.read_text() for b in sorted((other / "workflow").glob("y.md.bak.*"))] == [
        "edited y\n"
    ]


def test_listings_ignore_backups(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    claude = tmp_path / ".claude"
    assert install_core_files(force=True)[0]
    assert install_agents(force=True)[0]
    assert templates_mod.install_templates(force=True)[0]
    template = sorted((claude / "templates" / "workflow").glob("*"))[0]
    agent = sorted((claude / "agents").glob("*.md"))[0]
    core = next(p for p in sorted(claude.glob("*.md")) if p.name in KNOWN_CORE_FILES)
    for f in (template, agent, core):
        (f.parent / (f.name + ".bak.20261126T000000Z")).write_text("old")
        (f.parent / (f.name + ".bak.20261126T000000Z-2")).write_text("older")
    installed = templates_mod.list_installed_templates()
    assert not any(".bak." in n for n in installed)
    assert len(installed) == len(templates_mod.list_available_templates())
    assert not any(".bak." in n for n in list_installed_agents())
    assert not any(".bak." in n for n in list_installed_core_files())


def test_no_shipped_template_name_contains_bak():
    assert not [n for n in templates_mod.list_available_templates() if ".bak." in n]
