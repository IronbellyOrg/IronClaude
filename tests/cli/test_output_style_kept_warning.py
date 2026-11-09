"""Output-style install warnings never replace a kept user's files."""

import os
from pathlib import Path

import pytest

from superclaude.cli import install_user_setup as setup
from superclaude.cli.install_core import filecmp


@pytest.fixture
def style_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    source = tmp_path / "package" / "output-styles"
    source.mkdir(parents=True)
    packaged = source / "pragmatic.md"
    packaged.write_bytes(b"current packaged style\n")
    home = tmp_path / "home"
    dest = home / ".claude" / "output-styles"
    dest.mkdir(parents=True)
    settings = home / ".claude" / "settings.json"
    settings.write_bytes(b'{"outputStyle": "My custom style"}\n')
    unknown = dest / "personal.md"
    unknown.write_bytes(b"My independent style\n")
    monkeypatch.setattr(setup, "_package_dir", lambda name: source)
    yield home, packaged, dest / packaged.name
    assert settings.read_bytes() == b'{"outputStyle": "My custom style"}\n'
    assert unknown.read_bytes() == b"My independent style\n"


@pytest.mark.parametrize("existing", [None, "identical", "older", "customized"])
def test_warn_only_for_differing_kept_styles(style_paths, existing):
    home, packaged, installed = style_paths
    content = {
        "identical": packaged.read_bytes(),
        "older": b"previous packaged style\n",
        "customized": b"My customized style\n",
    }
    if existing is not None:
        installed.write_bytes(content[existing])
    ok, message = setup.install_output_styles(home=home)
    assert ok, message
    assert installed.read_bytes() == (
        packaged.read_bytes() if existing is None else content[existing]
    )
    if existing in ("older", "customized"):
        assert "1 kept output style(s) differ" in message
        assert "NOT updated" in message
        assert f"Packaged: {packaged}" in message
        assert f"Kept: {installed}" in message
        assert "merge desired changes manually" in message
        assert "preserving your customizations" in message
    else:
        assert "⚠️" not in message
    assert "--force" not in message
    assert "superclaude update" not in message
    assert "personal.md" not in message


def test_same_size_and_mtime_do_not_hide_changed_style(style_paths):
    home, packaged, installed = style_paths
    installed.write_bytes(b"X" * packaged.stat().st_size)
    stat = packaged.stat()
    os.utime(installed, ns=(stat.st_atime_ns, stat.st_mtime_ns))
    ok, message = setup.install_output_styles(home=home)
    assert ok, message
    assert "1 kept output style(s) differ" in message
    assert installed.read_bytes() == b"X" * stat.st_size


def test_unreadable_comparison_warns_without_claiming_known_difference(
    style_paths, monkeypatch: pytest.MonkeyPatch
):
    home, packaged, installed = style_paths
    installed.write_bytes(packaged.read_bytes())
    before = installed.read_bytes()

    def unreadable_comparison(a, b, shallow):
        assert (a, b) == (packaged, installed)
        assert shallow is False
        raise PermissionError("comparison denied")

    monkeypatch.setattr(filecmp, "cmp", unreadable_comparison)
    ok, message = setup.install_output_styles(home=home)
    assert ok, message
    assert "differ from this version or could not be compared" in message
    assert "NOT updated" in message
    assert f"Packaged: {packaged}" in message
    assert f"Kept: {installed}" in message
    assert installed.read_bytes() == before
    assert "--force" not in message


def test_explicit_force_still_copies_without_kept_warning(style_paths):
    home, packaged, installed = style_paths
    installed.write_bytes(b"Customized style\n")
    ok, message = setup.install_output_styles(home=home, force=True)
    assert ok, message
    assert installed.read_bytes() == packaged.read_bytes()
    assert "1 installed, 0 kept" in message
    assert "⚠️" not in message


def test_nested_styles_report_exact_paths_and_ignore_copy_exclusions(style_paths):
    home, packaged, installed = style_paths
    for relative in ("nested/other.md", "__pycache__/cached.pyc", ".DS_Store"):
        src = packaged.parent / relative
        target = installed.parent / relative
        src.parent.mkdir(parents=True, exist_ok=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        src.write_bytes(b"Packaged\n")
        target.write_bytes(b"Customized\n")
    ok, message = setup.install_output_styles(home=home)
    assert ok, message
    assert "1 kept output style(s) differ" in message
    assert f"Packaged: {packaged.parent / 'nested/other.md'}" in message
    assert f"Kept: {installed.parent / 'nested/other.md'}" in message
    assert "__pycache__" not in message
    assert ".DS_Store" not in message
    for relative in ("nested/other.md", "__pycache__/cached.pyc", ".DS_Store"):
        assert (installed.parent / relative).read_bytes() == b"Customized\n"
