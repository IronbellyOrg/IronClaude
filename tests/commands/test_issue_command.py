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


def test_st1_options_table_lists_exactly_the_eight_flags():
    assert sorted(_options_rows()) == sorted(
        [
            "--claim",
            "--create",
            "--depth",
            "--mode",
            "--type",
            "--pipeline",
            "--submit",
            "--stage",
        ]
    )


STAGES = ["research", "spec", "plan", "debug"]


def test_r23_stage_option_is_claim_only_with_the_four_stages():
    row = _options_rows()["--stage"]
    assert row[1] == "claim"
    assert re.findall(r"`([a-z]+)`", row[3]) == STAGES
    assert "--stage research|spec|plan|debug" in _frontmatter()["argument-hint"]


def test_r23_stage_stop_rules_follow_the_submit_rule():
    text = _text()
    stops = text.index("## STOP rules")
    rules = text[stops : text.index("\n## ", stops + 1)]
    submit = rules.index("E-SUBMIT-NEEDS-FULL")
    stage_create = rules.index('"--stage applies to --claim only"')
    stage_value = rules.index("A `--stage` value that is not")
    assert submit < stage_create < stage_value
    assert "`--stage` together with `--create`: STOP `E-CLAIM-ONLY-FLAG`" in rules
    assert "with no value" in rules[stage_value:]


@pytest.mark.parametrize("stage", STAGES)
@pytest.mark.parametrize(
    "level", ["none", "worktree", "full", "full --submit"], ids=str
)
def test_r23_every_prompt_form_the_watcher_sends_is_a_documented_form(stage, level):
    """Each form the watcher can send (Task 7) parses under the documented rules:
    one of the three --pipeline values, --submit only after full, one stage."""
    from superclaude.cli.issue_watch import launch

    prompt = f"/sc:issue --claim 12 --pipeline {level} --stage {stage}"
    assert launch.PROMPT_PATTERN.fullmatch(prompt)
    tokens = prompt.split()
    assert tokens[tokens.index("--pipeline") + 1] in ("worktree", "full", "none")
    assert ("--submit" in tokens) <= (tokens[tokens.index("--pipeline") + 1] == "full")
    assert tokens[tokens.index("--stage") + 1] in STAGES


@pytest.mark.parametrize(
    "prompt",
    [
        "/sc:issue --claim 12 --pipeline none --stage research extra",
        "/sc:issue --claim 12 --pipeline turbo --stage research",
        "/sc:issue --claim 12 --pipeline worktree --submit --stage plan",
        "/sc:issue --claim 12 --pipeline none --submit --stage plan",
        "/sc:issue --claim 12 --pipeline full --stage ready",
        "/sc:issue --claim 12 --stage plan",
    ],
)
def test_r23_extra_text_an_unknown_level_and_submit_without_full_are_refused(prompt):
    from superclaude.cli.issue_watch import launch

    assert launch.PROMPT_PATTERN.fullmatch(prompt) is None


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
    assert "launch-result.json" in claim_row
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


# --- command and skill agree on the create question (issue 834) --------------------

# The old broad trigger is built from fragments, so no whole copy of it sits in tests/.
OLD_TRIGGER = "new" + " material" + " or a" + " contradiction"
CREATE_FILES = [
    "description.md",
    "scout.md",
    "flags.md",
    "issue-body.md",
    "draft-notes.md",
    "create-review.md",
]


def agreement_problems(command: str, skill: str) -> list[str]:
    """Problems with how the command file and SKILL.md describe the create question."""
    problems = []
    if "nothing is shown for approval first" not in command:
        problems.append("the command lost the direct-posting promise")
    if "never shown for approval" not in skill:
        problems.append("SKILL.md lost the no-approval promise")
    if "contradicts your own description, instruction or flag" not in command:
        problems.append("the command lacks the contradiction exception")
    if (
        "supported contradiction of the user's own description, instruction or flag"
        not in skill
    ):
        problems.append("SKILL.md lacks the contradiction-only prompt rule")
    for where, text in (("the command", command), ("SKILL.md", skill)):
        if OLD_TRIGGER in text:
            problems.append(f"{where} still carries the old broad trigger")
    row = next((ln for ln in command.splitlines() if ln.startswith("| create |")), "")
    problems += [
        f"the create Outputs row lacks {name}"
        for name in CREATE_FILES
        if name not in row
    ]
    if "printed in the final output" not in row:
        problems.append("the create Outputs row does not mention retained additions")
    return problems


def test_command_and_skill_agree_on_the_create_question():
    assert agreement_problems(_text(), SKILL.read_text(encoding="utf-8")) == []


def test_agreement_check_fails_when_the_contradiction_exception_is_removed(tmp_path):
    copy = tmp_path / "issue.md"
    copy.write_text(re.sub(r" The one exception is `--create`:[^\n]*", "", _text()))
    problems = agreement_problems(
        copy.read_text(encoding="utf-8"), SKILL.read_text(encoding="utf-8")
    )
    assert problems == ["the command lacks the contradiction exception"]


def test_agreement_check_fails_when_the_old_trigger_returns(tmp_path):
    copy = tmp_path / "SKILL.md"
    copy.write_text(
        SKILL.read_text(encoding="utf-8") + f"\nAsk when notes list {OLD_TRIGGER}.\n"
    )
    problems = agreement_problems(_text(), copy.read_text(encoding="utf-8"))
    assert problems == ["SKILL.md still carries the old broad trigger"]


def test_agreement_check_fails_when_the_create_row_loses_a_file(tmp_path):
    copy = tmp_path / "issue.md"
    copy.write_text(_text().replace("`create-review.md`", "`review.md`"))
    problems = agreement_problems(
        copy.read_text(encoding="utf-8"), SKILL.read_text(encoding="utf-8")
    )
    assert problems == ["the create Outputs row lacks create-review.md"]
