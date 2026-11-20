"""``plan-check`` (4.11 point 1): the verb and the poll's ``plan_check`` are one function."""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.issue_watch import hold
from superclaude.cli.orchestrator import ext, plan_check

from .fake_world import call

GOOD = "## Priority\nP2\n\n## Fix approach\nChange the poll.\n\n## Test plan\nRun the tests.\n"


def check(tmp_path: Path, body: str | bytes) -> tuple[int, dict]:
    path = tmp_path / "body.md"
    path.write_bytes(body if isinstance(body, bytes) else body.encode())
    return call(tmp_path, "plan-check", "--body-file", str(path), tag=None)


def test_the_verb_and_the_polls_check_are_one_function() -> None:
    assert plan_check.plan_check is hold.plan_check


def test_a_body_with_all_three_sections_passes(tmp_path: Path) -> None:
    assert check(tmp_path, GOOD) == (0, {"ok": True, "missing": []})


def without(heading: str) -> str:
    return GOOD.replace(heading + "\n", "")


CASES = [
    # (what is wrong, body, the tokens that are missing)
    ("priority removed", GOOD.replace("## Priority\nP2\n\n", ""), ["priority"]),
    (
        "fix approach removed",
        GOOD.replace("## Fix approach\nChange the poll.\n\n", ""),
        ["fix_approach"],
    ),
    (
        "test plan removed",
        GOOD.replace("\n## Test plan\nRun the tests.\n", ""),
        ["test_plan"],
    ),
    ("priority emptied", GOOD.replace("P2\n", ""), ["priority"]),
    (
        "fix approach emptied",
        GOOD.replace("Change the poll.\n", "\n"),
        ["fix_approach"],
    ),
    ("test plan emptied", GOOD.replace("Run the tests.\n", ""), ["test_plan"]),
    ("priority not known yet", GOOD.replace("P2", "Not known yet"), ["priority"]),
    (
        "fix approach NOT KNOWN YET",
        GOOD.replace("Change the poll.", "NOT KNOWN YET"),
        ["fix_approach"],
    ),
    (
        "test plan not Known Yet",
        GOOD.replace("Run the tests.", "not Known Yet"),
        ["test_plan"],
    ),
    ("priority written twice", GOOD + "\n## Priority\nP1\n", ["priority"]),
    ("test plan written twice", GOOD + "\n## Test plan\nMore.\n", ["test_plan"]),
    ("priority only a comment", GOOD.replace("P2", "<!-- unknown -->"), ["priority"]),
    (
        "fix approach only a comment",
        GOOD.replace("Change the poll.", "<!--\nlater\n-->"),
        ["fix_approach"],
    ),
    (
        "everything missing",
        "Something is wrong.\n",
        ["priority", "fix_approach", "test_plan"],
    ),
    ("an empty body", "", ["priority", "fix_approach", "test_plan"]),
]


@pytest.mark.parametrize(("why", "body", "missing"), CASES, ids=[c[0] for c in CASES])
def test_each_failure_gives_its_closed_token_and_exit_3(
    tmp_path: Path, why: str, body: str, missing: list
) -> None:
    code, out = check(tmp_path, body)
    assert (code, out["ok"], out["reason"], out["missing"]) == (
        3,
        False,
        "plan_incomplete",
        missing,
    )
    assert (
        tuple(out["missing"]) == hold.plan_check(body).missing
    )  # the same answer as the poll's


def test_a_mutation_the_check_stays_red_when_a_heading_is_removed_from_a_passing_copy(
    tmp_path: Path,
) -> None:
    assert check(tmp_path, GOOD)[0] == 0
    for heading in ("## Priority", "## Fix approach", "## Test plan"):
        assert check(tmp_path, GOOD.replace(heading, "## Something else"))[0] == 3


def test_a_section_ends_at_the_create_marker(tmp_path: Path) -> None:
    body = "## Priority\nP2\n\n## Fix approach\nDo it.\n\n## Test plan\n<!-- sc:issue:create id=1 -->\nRun the tests.\n"
    code, out = check(tmp_path, body)
    assert (code, out["missing"]) == (
        3,
        ["test_plan"],
    )  # text after the marker is not part of the section


def test_the_verb_makes_no_external_call(tmp_path: Path, monkeypatch) -> None:
    def boom() -> None:
        raise AssertionError("plan-check must not run any command")

    monkeypatch.setattr(ext, "inner_runner", boom)
    assert check(tmp_path, GOOD)[0] == 0
    assert check(tmp_path, "")[0] == 3


def test_a_body_that_cannot_be_read_is_refused_not_read_as_empty(
    tmp_path: Path,
) -> None:
    code, out = call(
        tmp_path, "plan-check", "--body-file", str(tmp_path / "missing.md"), tag=None
    )
    assert (code, out["reason"]) == (2, "body_unreadable")
    code, out = check(tmp_path, b"\xff\xfe not utf-8")
    assert (code, out["reason"]) == (2, "invalid_input")
    code, out = check(tmp_path, b"x" * (plan_check.MAX_BODY_BYTES + 1))
    assert (code, out["reason"]) == (2, "body_too_large")
