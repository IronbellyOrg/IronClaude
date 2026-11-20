"""Tasks 7 and 11: the worker brief is built from fixed templates, one row per Status."""

from __future__ import annotations

import random
import re
from pathlib import Path

import pytest

from superclaude.cli.issue_pipeline import brief

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "src/superclaude/core/WORKER-CONTRACT.md"
TEMPLATE = ROOT / "src/superclaude/cli/issue_pipeline/templates/worker-brief.txt"
SUMMARY_TEMPLATE = (
    ROOT / "src/superclaude/skills/sc-issue-protocol/templates/issue-summary.md"
)
CLAIM_REF = ROOT / "src/superclaude/skills/sc-issue-protocol/refs/claim.md"

HEAD = """Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
On a blocked gate: report blocked
Plan approval: after writing the plan, follow rule WC-17 in ~/.claude/WORKER-CONTRACT.md before any further step.
Local commit: not authorized
Report directory: .dev/issues/452/worker-{stage}
Worktree: path:<existing worktree>
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Relaunch: In review fails the project check, so after the coordinator's move to In review a relaunch needs the owner to move the Status back to an allowed value.
"""
S = '"issue 452 @.dev/issues/452/issue-summary.md"'
D = ".dev/issues/452"
# one row per allowed Status: (stage, route) -> the Command line
ROWS = {
    (
        "research",
        None,
    ): f"Command: /sc:research {S} --unattended --report-dir {D}/worker-research\n",
    (
        "spec",
        "design",
    ): f"Command: /sc:design {D}/issue-summary.md --type architecture --format spec --unattended --report-dir {D}/worker-spec\n",
    (
        "spec",
        "brainstorm",
    ): f"Command: /sc:brainstorm {S} --blind --handoff design --unattended --output {D}/worker-spec\n",
    (
        "plan",
        None,
    ): f"Command: /sc:workflow {D}/issue-summary.md --depth standard --handoff none --unattended --report-dir {D}/worker-plan\n",
    (
        "debug",
        None,
    ): f"Command: /sc:troubleshoot {S} --unattended --report-dir {D}/worker-debug\n",
}


def golden(stage: str, route: str | None) -> str:
    return HEAD.format(stage=stage) + ROWS[(stage, route)]


@pytest.mark.parametrize("stage,route", list(ROWS))
def test_golden_brief_per_allowed_status(stage: str, route: str | None) -> None:
    assert brief.build(452, stage, route) == golden(stage, route)


def test_there_is_one_row_per_allowed_status() -> None:
    assert (
        {stage for stage, _ in ROWS}
        == set(brief.STAGES)
        == {
            "research",
            "spec",
            "plan",
            "debug",
        }
    )
    assert {route for stage, route in ROWS if stage == "spec"} == set(brief.ROUTES)


def test_the_debug_row_at_level_none_runs_troubleshoot_without_fix() -> None:
    text = brief.build(452, "debug")
    commands = [line for line in text.splitlines() if line.startswith("Command:")]
    assert len(commands) == 1 and commands[0].startswith("Command: /sc:troubleshoot ")
    assert "--fix" not in text


def test_the_spec_row_follows_the_route_of_the_judgment() -> None:
    well_defined = brief.build(452, "spec", "design")
    not_defined = brief.build(452, "spec", "brainstorm")
    assert "/sc:design " in well_defined and "/sc:brainstorm" not in well_defined
    assert "/sc:brainstorm " in not_defined
    # the brainstorm row hands off to /sc:design (high complexity or scope)
    assert "--handoff design" in not_defined


def test_the_spec_judgment_is_recorded_in_issue_summary_not_decided_by_code() -> None:
    """The claim worker writes `spec-route: design|brainstorm — <reason>`; the brief only reads it."""
    summary = SUMMARY_TEMPLATE.read_text()
    assert "- spec-route: <design | brainstorm> — <one-line reason>" in summary
    claim = CLAIM_REF.read_text()
    assert "`spec-route: design|brainstorm — <reason>`" in claim
    # Simple or Medium with a stated acceptance criterion is well defined; the rest, and Complex, is not
    assert "only when the complexity is Simple or Medium" in claim
    assert "every Complex issue, is `brainstorm`" in claim
    assert "`/sc:design`" in claim


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
        for stage, route in ROWS:
            text = brief.build(n, stage, route)
            assert set(text) <= allowed
            assert text == _expected_from_template(n, stage, route)
            assert text.count(str(n)) >= 3


def _expected_from_template(n: int, stage: str, route: str | None) -> str:
    sections: dict[str, list[str]] = {}
    current: list[str] | None = None
    for line in TEMPLATE.read_text().splitlines():
        if line.startswith("#") or not line:
            continue
        if line.startswith("["):
            current = sections.setdefault(line[1:-1], [])
        elif current is not None:
            current.append(line)
    row = f"spec-{route}" if stage == "spec" else stage
    return (
        "\n".join([*sections["head"], *sections[row]])
        .replace("{N}", str(n))
        .replace("{STAGE}", stage)
        + "\n"
    )


HOSTILE = [
    "<script>x</script>",
    "$(rm -rf /)",
    "plan; /sc:implement x",
    "plan\n/sc:implement x",
    "PLAN",
    "",
    " plan",
    "plan ",
    "ready",
    "implement",
    None,
    5,
    ["plan"],
    "‮plan",
]


@pytest.mark.parametrize("value", HOSTILE)
def test_a_status_outside_the_closed_set_is_refused_with_a_closed_reason(
    value: object,
) -> None:
    with pytest.raises(brief.BriefRefused) as err:
        brief.build(452, value)
    assert err.value.reason == "bad-stage"


@pytest.mark.parametrize("value", HOSTILE)
def test_a_route_outside_the_closed_set_is_refused(value: object) -> None:
    if value is None:
        value = "missing"  # a spec row with no route is refused too
    with pytest.raises(brief.BriefRefused) as err:
        brief.build(452, "spec", value)
    assert err.value.reason == "bad-route"
    with pytest.raises(brief.BriefRefused) as err:
        brief.build(452, "spec")
    assert err.value.reason == "bad-route"


@pytest.mark.parametrize("stage", ["research", "plan", "debug"])
def test_a_route_is_refused_for_every_stage_but_spec(stage: str) -> None:
    with pytest.raises(brief.BriefRefused) as err:
        brief.build(452, stage, "design")
    assert err.value.reason == "bad-route"


@pytest.mark.parametrize(
    "issue", [0, -3, "452", "4 5", 4.0, True, None, 2**63, [1], "452\n/sc:implement"]
)
def test_a_non_integer_issue_number_is_refused(issue: object) -> None:
    with pytest.raises(brief.BriefRefused) as err:
        brief.build(issue, "plan")
    assert err.value.reason == "bad-issue"


def test_no_row_runs_implement_commit_push_or_submit_and_every_command_is_unattended() -> (
    None
):
    forbidden = ("/sc:implement", "/task", "git commit", "git push", "/sc:pr-submit")
    for stage, route in ROWS:
        text = brief.build(452, stage, route)
        commands = [line for line in text.splitlines() if line.startswith("Command:")]
        assert len(commands) == 1
        for token in forbidden:
            assert token not in text, (stage, token)
        for line in commands:
            assert "--unattended" in line
            assert (
                len(re.findall(r"--(?:output|report-dir) ", line)) == 1
            )  # exactly one report directory
            if line.startswith("Command: /sc:workflow"):
                assert "--handoff none" in line


def test_the_brief_has_no_level_slot() -> None:
    """The brief is used only at level none: it names no level and offers no level argument."""
    import inspect

    assert list(inspect.signature(brief.build).parameters) == [
        "issue",
        "stage",
        "route",
        "nonce",
    ]
    assert "{LEVEL}" not in TEMPLATE.read_text()
    assert "--pipeline" not in brief.build(452, "plan")


def test_the_brief_says_a_relaunch_needs_the_status_moved_back() -> None:
    lines = brief.build(452, "plan").splitlines()
    relaunch = [line for line in lines if line.startswith("Relaunch:")]
    assert len(relaunch) == 1
    assert "In review" in relaunch[0] and "move the Status back" in relaunch[0]
    assert lines.index(relaunch[0]) < next(
        i for i, line in enumerate(lines) if line.startswith("Command:")
    )


def test_fixed_lines_equal_the_contract_template_word_for_word() -> None:
    contract = CONTRACT.read_text()
    block = (
        re.search(
            r"## 5\. Coordinator brief template.*?```text\n(.*?)```", contract, re.S
        )
        .group(1)
        .splitlines()
    )
    ours = brief.build(452, "plan").splitlines()
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
    for stage, route in ROWS:
        lines = brief.build(452, stage, route).splitlines()
        pointer = [line for line in lines if line.startswith("Plan approval:")]
        assert len(pointer) == 1 and "WC-17" in pointer[0]
        assert lines.index(pointer[0]) < next(
            i for i, line in enumerate(lines) if line.startswith("Command:")
        )


NONCE = "0123456789abcdef0123456789abcdef"
MARKER_RE = re.compile(r"\[sc-launch:v1:[0-9a-f]{32}\]")


@pytest.mark.parametrize("stage,route", list(ROWS))
def test_a_governed_brief_carries_exactly_one_marker_line(
    stage: str, route: str | None
) -> None:
    text = brief.build(452, stage, route, NONCE)
    lines = text.splitlines()
    marked = [line for line in lines if MARKER_RE.search(line)]
    assert marked == [f"Launch marker: [sc-launch:v1:{NONCE}]"]
    assert len(MARKER_RE.findall(text)) == 1
    # it sits in the head, before the first command, and the rest is the plain brief
    assert lines.index(marked[0]) < next(
        i for i, line in enumerate(lines) if line.startswith("Command:")
    )
    assert text.replace(marked[0] + "\n", "") == brief.build(452, stage, route)


@pytest.mark.parametrize("stage,route", list(ROWS))
def test_the_g1_test_issue_brief_carries_no_marker(
    stage: str, route: str | None
) -> None:
    assert "sc-launch" not in brief.build(452, stage, route)


@pytest.mark.parametrize(
    "nonce",
    ["", "abc", "A" * 32, "0" * 31, "0" * 33, "g" * 32, 5, [NONCE], NONCE + "\n"],
)
def test_a_nonce_outside_the_guard_form_is_refused(nonce: object) -> None:
    with pytest.raises(brief.BriefRefused) as err:
        brief.build(452, "plan", None, nonce)
    assert err.value.reason == "bad-nonce"
