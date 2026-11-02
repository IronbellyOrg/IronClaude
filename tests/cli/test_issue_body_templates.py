"""The Handoff and Backlog issue body files ship as core files, and one rule
line in the distributed CLAUDE.md tells the agent to use them.

KNOWN_CORE_FILES versus the shipped set is already pinned by
test_how_we_work_install.py::test_known_core_set_matches_shipped.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli import install_core

_REPO = Path(__file__).resolve().parents[2]
_CORE = _REPO / "src/superclaude/core"
_CLAUDE = _CORE / "CLAUDE.md"

_COMMON = ["What was tried", "Relevant files and links", "Done when"]
_HEADINGS = {
    "ISSUE-HANDOFF.md": [*_COMMON, "Who it is for"],
    "ISSUE-BACKLOG.md": [*_COMMON, "Pick-up note"],
}


def test_body_files_shipped_and_installed_flat(tmp_path):
    shipped = install_core.list_core_files()
    for name in _HEADINGS:
        assert name in shipped, name
    target = tmp_path / ".claude"
    ok, message = install_core.install_core_files(target_path=target, force=False)
    assert ok, message
    for name in _HEADINGS:
        assert (target / name).read_bytes() == (_CORE / name).read_bytes(), name


@pytest.mark.parametrize("name", sorted(_HEADINGS))
def test_body_file_has_exactly_its_four_headings(name):
    lines = (_CORE / name).read_text(encoding="utf-8").splitlines()
    headings = [line for line in lines if line.startswith("#")]
    assert headings == [f"## {title}" for title in _HEADINGS[name]]
    for index, line in enumerate(lines):
        if line.startswith("#"):
            below = lines[index + 1] if index + 1 < len(lines) else ""
            assert below.strip() and not below.startswith("#"), line


@pytest.mark.parametrize("name", sorted(_HEADINGS))
def test_body_file_names_no_execution_key_or_clickup(name):
    """Tripwire for AC 3 and AC 4, not proof of them."""
    text = (_CORE / name).read_text(encoding="utf-8").lower()
    assert "execution key" not in text
    assert "clickup" not in text


def test_claude_md_has_exactly_one_issue_rule_line():
    all_lines = _CLAUDE.read_text(encoding="utf-8").splitlines()
    hits = [i for i, line in enumerate(all_lines) if "gh issue create" in line]
    assert len(hits) == 1, hits
    rule = all_lines[hits[0]]
    assert rule.startswith("10. **Issues**")
    assert all_lines[hits[0] - 1].startswith("9. **Temporal**")
    assert '--title "<title>" --body-file <the copy>' in rule
    assert "never edit the installed template" in rule
    assert "fill every section" in rule
    handoff, backlog = "~/.claude/ISSUE-HANDOFF.md", "~/.claude/ISSUE-BACKLOG.md"
    assert f"`{handoff}` for work handed to" in rule
    assert f"`{backlog}` for parked work" in rule
    assert (
        rule.index(handoff)
        < rule.index("handed")
        < rule.index(backlog)
        < rule.index("parked")
    )


def test_no_issue_skill_or_command_added():
    for root in ("src/superclaude", "plugins/superclaude"):
        skills = _REPO / root / "skills"
        if skills.is_dir():
            assert not list(skills.glob("sc-issue*")), root
        commands = _REPO / root / "commands"
        if commands.is_dir():
            assert not list(commands.rglob("issue.md")), root
