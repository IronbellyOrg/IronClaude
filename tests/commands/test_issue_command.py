"""Static tests for the /sc:issue command file (design sections 4 and 16).

Enforcement type: STATIC (command file text).
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "src/superclaude/commands/issue.md"
SKILL = ROOT / "src/superclaude/skills/sc-issue-protocol/SKILL.md"

# Default D26, one fixed wording shared by the command file and SKILL.md (F-17).
RULE_10_LINE = (
    "For issues filed through `/sc:issue --create`, its four templates replace the "
    "`ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed "
    "`CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`."
)

ALLOWED = {
    "--depth": ["quick", "standard", "deep"],
    "--mode": ["feature", "bug"],
    "--type": [
        "cicd",
        "command",
        "skill",
        "agent",
        "hook",
        "cli",
        "core",
        "docs",
        "tests",
        "install",
        "other",
    ],
}


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


def _options_rows() -> dict[str, list[str]]:
    section = _text().split("## Options", 1)[1].split("\n## ", 1)[0]
    rows = {}
    for line in section.splitlines():
        if not line.startswith("| `--"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows[cells[0].strip("`")] = cells
    return rows


def test_frontmatter_fields():
    fields = _frontmatter()
    assert fields["name"] == "issue"
    assert fields["description"]
    assert fields["category"] == "workflow"
    assert fields["complexity"] == "advanced"
    assert fields["mcp-servers"] == "[auggie, codegraph]"
    assert fields["personas"] == "[analyzer]"
    assert fields["argument-hint"]


def test_options_table_lists_exactly_the_five_flags():
    assert sorted(_options_rows()) == sorted(["--claim", "--create", "--depth", "--mode", "--type"])


@pytest.mark.parametrize("flag", sorted(ALLOWED))
def test_options_table_allowed_values(flag):
    values_cell = _options_rows()[flag][3]
    assert re.findall(r"`([a-z]+)`", values_cell) == ALLOWED[flag]


def test_option_defaults():
    rows = _options_rows()
    assert rows["--depth"][2] == "`quick`"
    assert rows["--mode"][2] == rows["--type"][2] == "chosen by a worker when omitted"
    assert rows["--claim"][1] == "claim"
    assert all(rows[f][1] == "create" for f in ("--create", "--depth", "--mode", "--type"))


def test_no_repo_dry_run_or_preview_flag():
    text = _text()
    assert "--repo" not in _options_rows()
    assert "--repo" not in text
    assert "--dry-run" not in text and "--preview" not in text


def test_stop_rules_come_before_activation():
    text = _text()
    stops = text.index("## STOP rules")
    assert stops < text.index("## Activation")
    rules = text[stops : text.index("\n## ", stops + 1)]
    assert "Exactly one of `--claim` / `--create`" in rules
    assert "E-CREATE-ONLY-FLAG" in rules
    assert "allowed values" in rules
    assert "empty `--create` description" in rules.lower()


def test_activation_names_the_skill():
    activation = _text().split("## Activation", 1)[1]
    assert "> Skill sc:issue-protocol" in activation
    assert "~/.claude/skills/sc-issue-protocol/SKILL.md" in activation


def test_no_source_tree_path():
    assert "src/superclaude/" not in _text()


@pytest.mark.parametrize("path", [COMMAND, SKILL], ids=["command", "skill"])
def test_rule_10_line_is_carried_verbatim(path):
    assert RULE_10_LINE in path.read_text(encoding="utf-8").splitlines()
