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
    "--pipeline": ["worktree", "full", "none"],
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
    assert fields["mcp-servers"] == "[litellm, auggie, codegraph]"
    assert fields["personas"] == "[analyzer]"
    assert fields["argument-hint"]
    assert "--pipeline worktree|full|none" in fields["argument-hint"]
    assert "--submit" in fields["argument-hint"]


def test_st3_version_is_1_1_0():
    assert _frontmatter()["version"] == '"1.1.0"'


def test_st1_options_table_lists_exactly_the_seven_flags():
    assert sorted(_options_rows()) == sorted(
        [
            "--claim",
            "--create",
            "--depth",
            "--mode",
            "--type",
            "--pipeline",
            "--submit",
        ]
    )


@pytest.mark.parametrize("flag", sorted(ALLOWED))
def test_options_table_allowed_values(flag):
    values_cell = _options_rows()[flag][3]
    assert re.findall(r"`([a-z]+)`", values_cell) == ALLOWED[flag]


def test_option_defaults():
    rows = _options_rows()
    assert rows["--depth"][2] == "`quick`"
    assert rows["--mode"][2] == rows["--type"][2] == "chosen by a worker when omitted"
    assert rows["--claim"][1] == "claim"
    assert all(
        rows[f][1] == "create" for f in ("--create", "--depth", "--mode", "--type")
    )
    assert rows["--pipeline"][1] == rows["--submit"][1] == "claim"
    assert rows["--pipeline"][2] == "`worktree`"
    assert rows["--submit"][2] == "off"
    assert rows["--submit"][3] == "no value"
    assert "`--pipeline full`" in rows["--submit"][4]


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


def test_st2_pipeline_and_submit_stop_rules_come_after_the_old_ones():
    text = _text()
    stops = text.index("## STOP rules")
    rules = text[stops : text.index("\n## ", stops + 1)]
    old = rules.index("E-CREATE-ONLY-FLAG")
    claim_only = rules.index("E-CLAIM-ONLY-FLAG")
    values = rules.index("`--pipeline` value that is not `worktree`, `full` or `none`")
    submit = rules.index("E-SUBMIT-NEEDS-FULL")
    assert old < claim_only < values < submit
    assert stops < text.index("## Activation")
    assert '"--pipeline and --submit apply to --claim only"' in rules
    assert '"--submit needs --pipeline full"' in rules
    assert "with no value" in rules[values:submit]


def test_st3_will_not_names_what_the_command_never_runs_itself():
    text = _text()
    will_not = text.split("**Will Not:**", 1)[1].split("## Activation", 1)[0]
    assert "Run any next-step command" not in text
    for token in (
        "`/sc:implement`",
        "`/task`",
        "a commit",
        "a push",
        "`/sc:pr-submit`",
    ):
        assert token in will_not
    assert "Pass an Orca link flag" in will_not
    assert "Merge anything" in will_not
    assert "the launched agent may" in will_not


def test_claim_outputs_and_examples_cover_the_new_flags():
    text = _text()
    claim_row = next(ln for ln in text.splitlines() if ln.startswith("| claim |"))
    assert "launch-prompt.md" in claim_row and "worktree.json" in claim_row
    for example in (
        "/sc:issue --claim 302 --pipeline none",
        "/sc:issue --claim 302 --pipeline full",
        "/sc:issue --claim 302 --pipeline full --submit",
    ):
        assert example in text.splitlines()
    assert "E-ORCA-REQUIRED" in text


def test_activation_names_the_skill():
    activation = _text().split("## Activation", 1)[1]
    assert "> Skill sc:issue-protocol" in activation
    assert "~/.claude/skills/sc-issue-protocol/SKILL.md" in activation


def test_no_source_tree_path():
    assert "src/superclaude/" not in _text()


@pytest.mark.parametrize("path", [COMMAND, SKILL], ids=["command", "skill"])
def test_rule_10_line_is_carried_verbatim(path):
    assert RULE_10_LINE in path.read_text(encoding="utf-8").splitlines()
