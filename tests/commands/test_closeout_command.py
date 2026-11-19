"""Static tests for the /sc:closeout command file (design sections 3.1, 8.3 and 10.1 row 1).

Enforcement type: STATIC (command file text).
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "src/superclaude/commands/closeout.md"
SKILL = ROOT / "src/superclaude/skills/sc-closeout-protocol/SKILL.md"

OPTION_ROWS = ["<PR>", "--issue", "--dispatch", "--entry-key"]
FORBIDDEN_OPTIONS = ["--repo", "--dry-run", "--close", "--unattended"]


def _text() -> str:
    return COMMAND.read_text(encoding="utf-8")


def _frontmatter() -> dict:
    head = _text().split("\n---\n", 1)[0]
    assert head.startswith("---\n")
    fields = {}
    for line in head[4:].splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def _options_first_cells() -> list[str]:
    section = _text().split("## Options", 1)[1].split("\n## ", 1)[0]
    cells = []
    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        cell = line.strip().strip("|").split("|")[0].strip().strip("`")
        cells.append(cell.split(" ")[0])
    return cells


def _bullets(text: str, start: str, end: str) -> list[str]:
    block = text.split(start, 1)[1].split(end, 1)[0]
    return [ln[2:].strip() for ln in block.splitlines() if ln.startswith("- ")]


def test_frontmatter_fields():
    fields = _frontmatter()
    assert fields["name"] == "closeout"
    assert fields["version"]
    assert fields["description"]
    assert fields["category"] == "workflow"
    assert fields["complexity"]
    assert "mcp-servers" in fields
    assert "personas" in fields
    assert (
        fields["argument-hint"]
        == '"<PR> [--issue <N>] [--dispatch <id>] [--entry-key <key>]"'
    )


def test_options_table_lists_exactly_the_four_arguments():
    assert _options_first_cells() == OPTION_ROWS


def test_no_forbidden_option_is_listed():
    cells = _options_first_cells()
    for flag in FORBIDDEN_OPTIONS:
        assert flag not in cells
    assert "--repo" not in _text()


def test_stop_rules_come_before_activation():
    text = _text()
    stops = text.index("## STOP rules")
    assert stops < text.index("## Activation")
    rules = text[stops : text.index("\n## ", stops + 1)]
    for rule in (
        "no `<PR>`",
        "neither a number nor a URL",
        "an unknown flag",
        "a flag with no value",
        "a repeated flag",
        "an `--entry-key` that holds anything but letters, digits, `_`, `.` and `-`",
    ):
        assert rule in rules
    assert "usage block" in rules and "no write" in rules


def test_command_is_at_most_100_lines():
    assert len(_text().splitlines()) <= 100


def test_activation_names_the_skill():
    activation = _text().split("## Activation", 1)[1]
    assert "> Skill sc:closeout-protocol" in activation
    assert "Do NOT proceed with protocol execution using only this command file" in (
        activation
    )
    assert "~/.claude/skills/sc-closeout-protocol/SKILL.md" in activation
    assert ".claude/skills/sc-closeout-protocol/SKILL.md" in activation


def test_no_unattended_mode_section():
    text = _text()
    assert not re.search(r"^#+\s*Unattended mode", text, re.M | re.I)
    assert "never a worker" in text


def test_no_source_tree_path():
    assert "src/superclaude/" not in _text()


def test_boundaries_match_the_skill_will_do_and_will_not_do():
    command = _text()
    skill = SKILL.read_text(encoding="utf-8")
    will = _bullets(command, "**Will:**", "**Will Not:**")
    will_not = _bullets(command, "**Will Not:**", "## Activation")
    skill_will = _bullets(skill, "## Will Do", "## Will Not Do")
    skill_will_not = _bullets(skill, "## Will Not Do", "\n## ")
    assert will and will_not
    assert will == skill_will
    assert will_not == skill_will_not
