"""The Wave 4R reviser reads an untrusted review report, so its tools are pinned."""

from __future__ import annotations

import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_AGENT = _ROOT / "src/superclaude/agents/workflow-reviser.md"
_REF = _ROOT / "src/superclaude/skills/sc-workflow-protocol/refs/remediation.md"
_EXPECTED = ["Read", "Edit", "Grep", "Glob"]


def _tools(text: str) -> list[str]:
    fm = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    assert fm, "no frontmatter"
    line = re.search(r"^tools:[ \t]*(.*)$", fm.group(1), re.M)
    assert line and line.group(1).strip(), "no tools: allowlist"
    return [t.strip() for t in line.group(1).split(",") if t.strip()]


def test_agent_tools_are_exactly_read_edit_grep_glob():
    assert _AGENT.is_file()
    assert _tools(_AGENT.read_text(encoding="utf-8")) == _EXPECTED


def test_tools_check_fails_when_bash_is_added():
    text = _AGENT.read_text(encoding="utf-8").replace(
        "tools: Read, Edit, Grep, Glob", "tools: Read, Edit, Grep, Glob, Bash"
    )
    assert _tools(text) != _EXPECTED


def test_remediation_pins_reviser_fail_closed_and_untrusted():
    text = " ".join(_REF.read_text(encoding="utf-8").split())
    assert "`workflow-reviser`" in text
    assert "Fail closed" in text
    assert "never falls back to `general-purpose`" in text
    assert "untrusted data" in text
