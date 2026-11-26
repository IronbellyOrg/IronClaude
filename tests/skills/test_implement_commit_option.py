"""Static pins for the `--commit-tasks` wiring in the implement command and skill (Task 26).

Enforcement type: STATIC (text of `commands/implement.md` and `sc-implement-protocol/SKILL.md`).
The commit rules themselves live in `refs/commit-step.md` (Tasks 27 to 29); the full rule
tests are `tests/skills/test_implement_commit_rules.py` (Task 34).
FR-050, FR-053, FR-054, FR-057, FR-070, FR-071, FR-072, NFR-012.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "src/superclaude/commands/implement.md"
SKILL = ROOT / "src/superclaude/skills/sc-implement-protocol/SKILL.md"
PLUGIN_COMMAND = ROOT / "plugins/superclaude/commands/implement.md"
PLUGIN_SKILL = ROOT / "plugins/superclaude/skills/sc-implement-protocol/SKILL.md"

# SKILL.md had 215 lines before this work; NFR-012 allows 15 more (Tasks 26 and 30 share them).
SKILL_LINE_CAP = 215 + 15

PRECONDITION_REASONS = (
    "not-person",
    "unattended",
    "helper-missing",
    "not-a-repo",
    "detached-head",
    "protected-branch",
    "operation-in-progress",
    "index-locked",
    "git-too-old",
)


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def _command() -> str:
    return COMMAND.read_text(encoding="utf-8")


def test_command_option_row_hint_and_will_not():
    text = _command()
    hint = re.search(r'^argument-hint: "(.*)"$', text, re.M).group(1)
    assert "[--commit-tasks]" in hint
    rows = [x for x in text.splitlines() if x.startswith("| `--commit-tasks`")]
    assert len(rows) == 1 and "| off |" in rows[0]
    assert (
        "- Commit without `--commit-tasks` on the invocation line, push, open PRs, or "
        "release (a managed archive is not any of these)"
    ) in text.splitlines()
    assert "- Auto-commit, open PRs, or release" not in text


def test_skill_known_options_and_wave0_steps_in_order():
    lines = _skill().splitlines()
    known = next(x for x in lines if "Known options:" in x)
    assert "`--commit-tasks`" in known and "refs/commit-step.md" in known
    idx = {
        name: next(i for i, x in enumerate(lines) if x.startswith(prefix))
        for name, prefix in {
            "5": "5. Resolve ledger path.",
            "5b": "5b. ",
            "6": "6. Open or create ledger",
            "6b": "6b. ",
            "7": "7. If N",
        }.items()
    }
    assert idx["5"] < idx["5b"] < idx["6"] < idx["6b"] < idx["7"]
    step5b = lines[idx["5b"]]
    assert (
        "vcs preflight" in step5b and "E-COMMIT-PRECONDITION reason=<token>" in step5b
    )
    for reason in PRECONDITION_REASONS:
        assert f"`{reason}`" in step5b, reason
    step6b = lines[idx["6b"]]
    assert "vcs reconcile" in step6b and "`run` line" in step6b
    assert "commits.md" in step6b


def test_q0_records_branch_and_q8a_sits_between_q7_and_q8():
    skill = _skill()
    assert "<retries>/T<id>/q0-branch" in skill
    lines = skill.splitlines()
    q7 = next(i for i, x in enumerate(lines) if x.startswith("Q7 GATE"))
    q8a = next(i for i, x in enumerate(lines) if x.startswith("Q8a "))
    q8 = next(i for i, x in enumerate(lines) if x.startswith("Q8 NEXT"))
    assert q7 < q8a < q8 and q8a == q7 + 1 and q8 == q8a + 1
    assert "refs/commit-step.md" in lines[q8a]


def test_load_rule_line_names_the_ref_and_both_triggers():
    rule = next(
        x
        for x in _skill().splitlines()
        if x.startswith("Also load `refs/commit-step.md`")
    )
    assert "`--commit-tasks`" in rule and "`commits.md`" in rule


def test_stop_rows_and_closed_list_sentence():
    skill = _skill()
    rows = {
        m.group(1): m.group(0)
        for m in re.finditer(r"^\| `(E-[A-Z-]+)` \|.*\|$", skill, re.M)
    }
    assert "E-COMMIT-PRECONDITION" in rows and "E-COMMIT-REFUSED" in rows
    assert rows["E-COMMIT-PRECONDITION"].count("|") == rows["E-HALT-QA"].count("|")
    assert rows["E-COMMIT-REFUSED"].count("|") == rows["E-HALT-QA"].count("|")
    # the existing transient row is untouched: the two new reasons live in the commit ref only
    assert rows["E-RESUME-NEEDED"].rstrip().endswith("| Nothing written |")
    assert "refs/retry.md" in rows["E-RESUME-NEEDED"]
    sentence = next(
        x for x in skill.splitlines() if x.startswith("No other `E-*` codes")
    )
    for code in ("`E-RESUME-NEEDED`", "`E-COMMIT-PRECONDITION`", "`E-COMMIT-REFUSED`"):
        assert code in sentence, code
    assert "commit step's transient stops" in sentence


def test_done_summary_prints_one_line_per_commit_or_recovered_line():
    done = next(
        x for x in _skill().splitlines() if x.startswith("Every enumerable task has")
    )
    assert "`commit sha=`" in done and "`recovered`" in done
    assert "<short sha> <tasks> <subject>" in done


def test_skill_growth_stays_inside_the_budget_and_names_no_src_path():
    skill = _skill()
    assert len(skill.splitlines()) <= SKILL_LINE_CAP
    for text in (skill, _command()):
        assert "src/superclaude/" not in text


def test_plugin_twins_are_byte_identical():
    assert PLUGIN_COMMAND.read_bytes() == COMMAND.read_bytes()
    assert PLUGIN_SKILL.read_bytes() == SKILL.read_bytes()
