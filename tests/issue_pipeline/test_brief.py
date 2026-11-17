"""Task 7: the worker brief is built from fixed templates."""

from __future__ import annotations

import random
import re
from pathlib import Path

import pytest

from superclaude.cli.issue_pipeline import brief

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "src/superclaude/core/WORKER-CONTRACT.md"
TEMPLATE = ROOT / "src/superclaude/cli/issue_pipeline/templates/worker-brief.txt"

HEAD = """Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
On a blocked gate: report blocked
Plan approval: after writing the plan, follow rule WC-17 in ~/.claude/WORKER-CONTRACT.md before any further step.
Local commit: not authorized
Report directory: .dev/issues/452/worker-plan
Worktree: path:<existing worktree>
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
"""
D = ".dev/issues/452/worker-plan"
BRAIN = '/sc:brainstorm "issue 452 @.dev/issues/452/issue-summary.md"'
GOLDEN = {
    "simple": HEAD
    + f"Command: {BRAIN} --depth quick --unattended --output {D}/brainstorm\n"
    + f"Command: /sc:workflow {D}/brainstorm/merged-requirements.md --depth quick --handoff none --unattended --report-dir {D}/workflow\n",
    "medium": HEAD
    + f"Command: {BRAIN} --blind --unattended --output {D}/brainstorm\n"
    + f"Command: /sc:design {D}/brainstorm/merged-requirements.md --type architecture --format spec --unattended --report-dir {D}/design\n"
    + f"Command: /sc:workflow {D}/design/design-report.md --depth standard --handoff none --unattended --report-dir {D}/workflow\n",
    "complex": HEAD
    + f"Command: {BRAIN} --depth deep --research deep --codebase --blind --unattended --output {D}/brainstorm\n"
    + f"Command: /sc:design {D}/brainstorm/merged-requirements.md --type architecture --format spec --unattended --report-dir {D}/design\n"
    + f"Command: /sc:workflow {D}/design/design-report.md --depth deep --handoff none --unattended --report-dir {D}/workflow\n",
}


@pytest.mark.parametrize("complexity", ["simple", "medium", "complex"])
def test_golden_brief_per_feature_row(complexity: str) -> None:
    assert brief.build(452, "feature", complexity) == GOLDEN[complexity]


@pytest.mark.parametrize("complexity", ["medium", "complex"])
def test_design_rows_use_a_fixed_architecture_type(complexity: str) -> None:
    text = brief.build(7, "feature", complexity)
    design = [line for line in text.splitlines() if "/sc:design" in line]
    assert len(design) == 1 and "--type architecture --format spec" in design[0]
    assert "/sc:design" not in brief.build(7, "feature", "simple")


def _template_characters() -> set[str]:
    body = "".join(
        line
        for line in TEMPLATE.read_text().splitlines(keepends=True)
        if not line.startswith("#")
    )
    return set(body) | set("0123456789")


def test_output_holds_only_template_characters_plus_the_issue_number() -> None:
    allowed = _template_characters()
    rng = random.Random(7)
    numbers = [1, 9, 452, 99999, *(rng.randrange(1, 10**9) for _ in range(30))]
    for n in numbers:
        for complexity in ("simple", "medium", "complex"):
            text = brief.build(n, "feature", complexity)
            assert set(text) <= allowed
            # the output is the template section with {N} replaced by the validated number, nothing else
            assert text == _expected_from_template(n, complexity)
            assert text.count(str(n)) >= 3


def _expected_from_template(n: int, complexity: str) -> str:
    sections: dict[str, list[str]] = {}
    current: list[str] | None = None
    for line in TEMPLATE.read_text().splitlines():
        if line.startswith("#") or not line:
            continue
        if line.startswith("["):
            current = sections.setdefault(line[1:-1], [])
        elif current is not None:
            current.append(line)
    return (
        "\n".join([*sections["head"], *sections[complexity]]).replace("{N}", str(n))
        + "\n"
    )


HOSTILE = [
    "<script>x</script>",
    "$(rm -rf /)",
    "simple; /sc:implement x",
    "simple\n/sc:implement x",
    "SIMPLE",
    "",
    " simple",
    "simple ",
    None,
    5,
    ["simple"],
    "‮simple",
]


@pytest.mark.parametrize("value", HOSTILE)
def test_values_outside_the_enums_refuse_with_a_closed_reason(value: object) -> None:
    with pytest.raises(brief.BriefRefused) as err:
        brief.build(452, "feature", value)
    assert err.value.reason == "bad-complexity"
    with pytest.raises(brief.BriefRefused) as err:
        brief.build(452, value, "simple")
    assert err.value.reason == "bad-type"


@pytest.mark.parametrize(
    "issue", [0, -3, "452", "4 5", 4.0, True, None, 2**63, [1], "452\n/sc:implement"]
)
def test_a_non_integer_issue_number_is_refused(issue: object) -> None:
    with pytest.raises(brief.BriefRefused) as err:
        brief.build(issue, "feature", "simple")
    assert err.value.reason == "bad-issue"


@pytest.mark.parametrize("complexity", ["simple", "medium", "complex", "bogus"])
def test_type_bug_is_refused_and_builds_no_brief(complexity: str) -> None:
    with pytest.raises(brief.BriefRefused) as err:
        brief.build(452, "bug", complexity)
    assert err.value.reason == "type-not-supported"


def test_no_row_runs_implement_commit_push_or_submit_and_every_command_is_unattended() -> (
    None
):
    forbidden = ("/sc:implement", "/task", "git commit", "git push", "/sc:pr-submit")
    for complexity in ("simple", "medium", "complex"):
        text = brief.build(452, "feature", complexity)
        commands = [line for line in text.splitlines() if line.startswith("Command:")]
        assert len(commands) >= 2
        for token in forbidden:
            assert token not in text, (complexity, token)
        for line in commands:
            assert "--unattended" in line
            assert (
                len(re.findall(r"--(?:output|report-dir) ", line)) == 1
            )  # exactly one report directory
            if line.startswith("Command: /sc:workflow"):
                assert "--handoff none" in line


def test_fixed_lines_equal_the_contract_template_word_for_word() -> None:
    contract = CONTRACT.read_text()
    block = (
        re.search(
            r"## 5\. Coordinator brief template.*?```text\n(.*?)```", contract, re.S
        )
        .group(1)
        .splitlines()
    )
    ours = brief.build(452, "feature", "simple").splitlines()
    for prefix in (
        "Guard:",
        "Chain:",
        "On a blocked gate:",
        "Local commit:",
        "Outward actions:",
    ):
        theirs = [line for line in block if line.startswith(prefix)]
        mine = [line for line in ours if line.startswith(prefix)]
        assert len(theirs) == len(mine) == 1 and theirs == mine, prefix
    # the one deliberate difference: the Worktree slot
    assert next(line for line in block if line.startswith("Worktree:")).startswith(
        "Worktree: <shared feature worktree"
    )
    assert "Worktree: path:<existing worktree>" in ours


def test_brief_points_at_the_plan_approval_rule_of_the_contract() -> None:
    contract = CONTRACT.read_text()
    assert "**WC-17. Plan approval is the reply to the worker's own ask.**" in contract
    for complexity in ("simple", "medium", "complex"):
        lines = brief.build(452, "feature", complexity).splitlines()
        pointer = [line for line in lines if line.startswith("Plan approval:")]
        assert len(pointer) == 1 and "WC-17" in pointer[0]
        assert lines.index(pointer[0]) < next(
            i for i, line in enumerate(lines) if line.startswith("Command:")
        )


NONCE = "0123456789abcdef0123456789abcdef"
MARKER_RE = re.compile(r"\[sc-launch:v1:[0-9a-f]{32}\]")


@pytest.mark.parametrize("complexity", ["simple", "medium", "complex"])
def test_a_governed_brief_carries_exactly_one_marker_line(complexity: str) -> None:
    text = brief.build(452, "feature", complexity, NONCE)
    lines = text.splitlines()
    marked = [line for line in lines if MARKER_RE.search(line)]
    assert marked == [f"Launch marker: [sc-launch:v1:{NONCE}]"]
    assert len(MARKER_RE.findall(text)) == 1
    # it sits in the head, before the first command, and the rest is the plain brief
    assert lines.index(marked[0]) < next(
        i for i, line in enumerate(lines) if line.startswith("Command:")
    )
    assert text.replace(marked[0] + "\n", "") == brief.build(452, "feature", complexity)


@pytest.mark.parametrize("complexity", ["simple", "medium", "complex"])
def test_the_g1_test_issue_brief_carries_no_marker(complexity: str) -> None:
    assert "sc-launch" not in brief.build(452, "feature", complexity)


@pytest.mark.parametrize(
    "nonce",
    ["", "abc", "A" * 32, "0" * 31, "0" * 33, "g" * 32, 5, [NONCE], NONCE + "\n"],
)
def test_a_nonce_outside_the_guard_form_is_refused(nonce: object) -> None:
    with pytest.raises(brief.BriefRefused) as err:
        brief.build(452, "feature", "simple", nonce)
    assert err.value.reason == "bad-nonce"
