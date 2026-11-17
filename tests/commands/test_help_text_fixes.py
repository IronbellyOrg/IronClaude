"""Regression checks for small help-text and message fixes (issues 505, 506, 536)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_COMMANDS = _REPO / "src/superclaude/commands"

# The tracked copies carry the same header text as the source file.
_BUSINESS_PANEL_FILES = (
    "src/superclaude/commands/business-panel.md",
    "plugins/superclaude/commands/business-panel.md",
    "commands/sc-business-panel.md",
)


def _help_description(path: Path) -> str:
    """The value `/sc:help` shows: the first `description:` line, as `grep -m1` finds it."""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("description:"):
            return line[len("description:") :].strip().strip('"')
    return ""


@pytest.mark.parametrize("relative", _BUSINESS_PANEL_FILES)
def test_business_panel_supplies_a_description_the_help_listing_reads(relative):
    path = _REPO / relative
    assert _help_description(path), f"{relative}: /sc:help finds no description"
    assert not re.search(r"^purpose:", path.read_text("utf-8"), re.M), (
        f"{relative}: use description:, not purpose:"
    )


_CLEANUP_FILES = (
    "src/superclaude/commands/cleanup.md",
    "plugins/superclaude/commands/cleanup.md",
    "commands/sc-cleanup.md",
)


def _section(text: str, heading: str) -> str:
    """Body of one `## heading` section, up to the next `## ` heading."""
    match = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert match, f"no '## {heading}' section"
    return match.group(1)


def _fenced_command_lines(section: str) -> list[str]:
    blocks = re.findall(r"```[a-z]*\n(.*?)```", section, re.S)
    return [
        line
        for block in blocks
        for line in block.splitlines()
        if line.startswith("/sc:")
    ]


@pytest.mark.parametrize("relative", _CLEANUP_FILES)
def test_cleanup_usage_lists_every_option_its_examples_use(relative):
    text = (_REPO / relative).read_text(encoding="utf-8")
    usage_lines = _fenced_command_lines(_section(text, "Usage"))
    example_lines = _fenced_command_lines(_section(text, "Examples"))
    assert usage_lines and example_lines
    usage_flags = {f for line in usage_lines for f in re.findall(r"--[a-z-]+", line)}
    for line in example_lines:
        for flag in re.findall(r"--[a-z-]+", line):
            assert flag in usage_flags, (
                f"{relative}: '{line}' uses {flag}, not in usage"
            )


@pytest.mark.parametrize("relative", _CLEANUP_FILES)
def test_cleanup_says_plainly_that_preview_edits_nothing(relative):
    usage = _section((_REPO / relative).read_text(encoding="utf-8"), "Usage")
    sentences = [s for s in re.split(r"(?<=\.)\s+", usage) if "`--preview`" in s]
    assert sentences, f"{relative}: no sentence explains --preview"
    assert any("what would change" in s and "edits nothing" in s for s in sentences), (
        sentences
    )


_PM_FILES = (
    "src/superclaude/commands/pm.md",
    "src/superclaude/agents/pm-agent.md",
    "src/superclaude/skills/sc-pm-protocol/SKILL.md",
    "plugins/superclaude/commands/pm.md",
    "plugins/superclaude/agents/pm-agent.md",
    "commands/sc-pm.md",
    "agents/sc-pm-agent.md",
)

# Wording that told users PM starts by itself or restores memory by itself.
_PM_FALSE_PROMISES = (
    "runs automatically at every session start",
    "Auto-Executes Every Time",
    "EVERY Claude Code session start",
    "auto-activates at session start",
    "Session Start (MANDATORY)",
    "ALWAYS activates to restore",
    "no command needed",
    "never need to manually invoke",
    "(Always Active)",
)


@pytest.mark.parametrize("relative", _PM_FILES)
def test_pm_text_does_not_promise_to_start_or_restore_memory_by_itself(relative):
    text = (_REPO / relative).read_text(encoding="utf-8")
    found = [phrase for phrase in _PM_FALSE_PROMISES if phrase.lower() in text.lower()]
    assert not found, f"{relative} still promises: {found}"


def test_pm_has_no_startup_hook():
    hooks = (_REPO / "src/superclaude/hooks/hooks.json").read_text(encoding="utf-8")
    assert not re.search(r"\bpm\b|pm-agent|sc:pm", hooks, re.I)
