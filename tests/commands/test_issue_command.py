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
    assert "--plan <number|url>" in fields["argument-hint"]
    assert "--remaining <file>" in fields["argument-hint"]


def test_st3_version_is_1_1_0():
    assert _frontmatter()["version"] == '"1.1.0"'


def test_st1_options_table_lists_exactly_the_nine_flags():
    assert sorted(_options_rows()) == sorted(
        [
            "--claim",
            "--create",
            "--plan",
            "--remaining",
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
    assert all(rows[f][1] == "create" for f in ("--create", "--mode", "--type"))
    assert rows["--depth"][1] == "create, plan"
    assert rows["--plan"][1] == rows["--remaining"][1] == "plan"
    assert rows["--pipeline"][1] == rows["--submit"][1] == "claim"
    assert rows["--pipeline"][2] == "`full` or `worktree`, picked from the issue"
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
    assert "Exactly one of `--claim`, `--create` and `--plan`" in rules
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


def test_default_level_is_for_a_person_and_the_watcher_stays_explicit():
    text = _text()
    assert "always passes `--pipeline none`" in text
    assert "/sc:issue --claim 302 --pipeline worktree" in text.splitlines()
    assert "an explicit `--pipeline` always wins" in text
    assert "`refs/claim.md`" in text
    assert "even though `full` is the default" not in text


def test_submit_rule_stops_a_bare_submit_and_keeps_its_message():
    text = _text()
    stops = text.index("## STOP rules")
    rules = text[stops : text.index("\n## ", stops + 1)]
    rule = next(ln for ln in rules.splitlines() if "E-SUBMIT-NEEDS-FULL" in ln)
    assert "no `--pipeline`" in rule
    assert '"--submit needs --pipeline full"' in rule


def test_activation_names_the_skill():
    activation = _text().split("## Activation", 1)[1]
    assert "> Skill sc:issue-protocol" in activation
    assert "~/.claude/skills/sc-issue-protocol/SKILL.md" in activation


def test_no_source_tree_path():
    assert "src/superclaude/" not in _text()


@pytest.mark.parametrize("path", [COMMAND, SKILL], ids=["command", "skill"])
def test_rule_10_line_is_carried_verbatim(path):
    assert RULE_10_LINE in path.read_text(encoding="utf-8").splitlines()


# --- plan mode (issue 655, PR P): `--plan` and `--remaining` -----------------------


def _stop_rules() -> str:
    text = _text()
    stops = text.index("## STOP rules")
    return text[stops : text.index("\n## ", stops + 1)]


def _rule_line(*needles: str) -> str:
    """The one bullet of the STOP rules that holds every needle."""
    hits = [
        ln
        for ln in _stop_rules().splitlines()
        if ln.startswith("- ") and all(n in ln for n in needles)
    ]
    assert len(hits) == 1, (needles, hits)
    return hits[0]


def _section(heading: str) -> str:
    text = _text()
    start = text.index(heading)
    return text[start : text.index("\n## ", start + 1)]


def test_plan_mode_is_named_in_every_part_of_the_command_file():
    text = _text()
    assert "--plan <number|url>" in _frontmatter()["argument-hint"]
    usage = _section("## Usage")
    assert "/sc:issue --plan <number|url> [--depth quick|standard|deep]" in usage
    assert "--remaining <file>" in usage
    top = text.split("## Triggers", 1)[0]
    assert top.count("`--plan`") >= 1 and "Three modes" in top
    assert "All three modes post directly to GitHub" in top
    assert "`--plan`" in _section("## Boundaries")
    assert "`--plan`" in _section("## Outputs") or "| plan |" in _section("## Outputs")


def test_plan_options_rows_name_the_issue_and_the_remaining_file_rules():
    rows = _options_rows()
    assert "issue number (`302`, `#302`) or issue URL" in rows["--plan"][3]
    remaining = " ".join(rows["--remaining"])
    for needle in (
        "round: <n>",
        "1 to 20 lines",
        "300 characters",
        "Only with `--plan`",
    ):
        assert needle in remaining, needle
    assert rows["--depth"][2] == "`quick`"
    assert "plan" in rows["--depth"][1]


@pytest.mark.parametrize(
    ("needles", "message"),
    [
        (
            ("Exactly one of `--claim`, `--create` and `--plan`", "None, or more than"),
            None,
        ),
        (
            (
                "E-CREATE-ONLY-FLAG",
                "`--mode` or `--type` together with `--claim` or `--plan`",
            ),
            '"--mode and --type apply to --create only; --depth applies to --create and --plan"',
        ),
        (("E-CREATE-ONLY-FLAG", "`--depth` together with `--claim`"), None),
        (
            ("E-CLAIM-ONLY-FLAG", "`--create` or `--plan`"),
            '"--pipeline and --submit apply to --claim only"',
        ),
        (("An empty `--plan` argument", "Usage block"), None),
        (
            ("E-PLAN-ONLY-FLAG", "`--remaining` without `--plan`"),
            '"--remaining applies to --plan only"',
        ),
    ],
    ids=[
        "none-or-more-than-one-mode",
        "mode-or-type-with-plan",
        "depth-with-claim-still-refused",
        "pipeline-or-submit-with-plan",
        "empty-plan-argument",
        "remaining-without-plan",
    ],
)
def test_each_plan_stop_rule_has_its_code_and_message(needles, message):
    line = _rule_line(*needles)
    if message:
        assert message in line
    if "Exactly one" in needles[0] or "empty `--plan`" in needles[0]:
        assert "Usage block" in line


def test_depth_is_refused_with_claim_and_passes_with_plan():
    line = _rule_line("E-CREATE-ONLY-FLAG", "`--depth` together with `--claim`")
    assert "`--plan`" not in line.split("`--mode`")[0]
    assert "--depth applies to --create and --plan" in _stop_rules()
    assert "create, plan" in _options_rows()["--depth"][1]


def test_remaining_rule_names_both_other_modes():
    line = _rule_line("E-PLAN-ONLY-FLAG")
    assert "`--claim`" in line and "`--create`" in line


def test_the_stops_that_need_the_issue_are_named_in_the_command_file():
    rules = _stop_rules()
    for code in (
        "E-ISSUE-NOT-FOUND",
        "E-PLAN-NOT-AN-ISSUE",
        "E-PLAN-ISSUE-CLOSED",
        "E-PLAN-REPEATED-HEADING",
        "E-REMAINING-FILE",
        "E-REMAINING-NEEDS-PLAN",
    ):
        assert code in rules, code
    assert "`already_planned`" in rules and "not a stop" in rules


def test_plan_examples_are_listed_as_whole_lines():
    lines = _text().splitlines()
    for example in (
        "/sc:issue --plan 302",
        "/sc:issue --plan 302 --depth standard",
    ):
        assert example in lines
    assert any(ln.startswith("/sc:issue --plan 302 --remaining ") for ln in lines), (
        "a --remaining example"
    )


def test_plan_outputs_row_names_the_files_and_the_one_post():
    row = next(ln for ln in _text().splitlines() if ln.startswith("| plan |"))
    for name in ("plan-input.md", "plan-sections.md", "draft-notes.md", "plan-body.md"):
        assert name in row, name
    assert "plan-before-round-<n>.md" in row and "--remaining" in row


def test_plan_boundaries_say_what_plan_mode_writes_and_never_touches():
    boundaries = _section("## Boundaries")
    will, will_not = boundaries.split("**Will Not:**")
    assert "On plan (`--plan`):" in will and "one body edit" in will
    assert "On plan (`--plan`):" in will_not
    for token in (
        "post a comment",
        "label",
        "assign anyone",
        "touch ClickUp",
        "create a worktree",
        "launch an agent",
        "ask a question",
        "outside the sections it fills",
    ):
        assert token in will_not, token


def test_the_command_says_other_sessions_call_it_and_not_the_protocol_alone():
    text = _text()
    assert "calls this command" in text
    assert "never loads `sc:issue-protocol` alone" in text
    assert "a direct protocol call would skip them" in text


def test_the_old_two_mode_wording_is_gone():
    text = _text()
    assert "Exactly one of `--claim` / `--create`" not in text
    assert "Both modes post directly" not in text
    assert "Two modes on the repository" not in text


def test_every_row_of_the_related_commands_table_is_one_row_of_two_cells():
    section = _text().split("## Related Commands", 1)[1]
    rows = [ln for ln in section.splitlines() if ln.startswith("|")]
    assert len(rows) >= 4  # header, separator, and the rows that follow
    for row in rows:
        assert "||" not in row, row
        # a Markdown row of two cells has exactly three unescaped pipes
        assert row.replace("\\|", "").count("|") == 3, row
