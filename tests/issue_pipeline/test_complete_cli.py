"""Task 14: the coordinator-only ``issue-pipeline complete`` verb."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.issue_pipeline import cli as cli_mod
from superclaude.cli.issue_pipeline import complete
from superclaude.cli.issue_pipeline.cli import issue_pipeline_group
from tests.issue_pipeline.test_complete import (
    CANARY,
    ISSUE,
    PROJECT,
    REPO,
    RUN,
    World,
    node,
)


def invoke(world: World, monkeypatch, *extra: str, **over: str):
    monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
    args = {
        "--repo": REPO,
        "--issue": str(ISSUE),
        "--project-id": PROJECT,
        "--run": str(RUN),
        "--outcome": "succeeded",
    }
    args.update(over)
    argv = ["complete", *(x for kv in args.items() for x in kv), *extra]
    return CliRunner().invoke(issue_pipeline_group, argv)


def test_a_succeeded_call_prints_the_closed_success_word(monkeypatch) -> None:
    world = World(node(status="Plan"))
    result = invoke(world, monkeypatch)
    assert result.exit_code == 0 and result.output == "completed\n"
    assert len(world.posts) == 1 and len(world.mutations) == 1


def test_a_failed_outcome_prints_commented_and_moves_nothing(monkeypatch) -> None:
    world = World(node(status="Plan"))
    result = invoke(world, monkeypatch, **{"--outcome": "failed"})
    assert result.exit_code == 0 and result.output == "commented\n"
    assert world.mutations == []


def test_a_person_moved_status_exits_zero_with_its_word(monkeypatch) -> None:
    result = invoke(World(node(status="Done")), monkeypatch)
    assert result.exit_code == 0 and result.output == "status_moved_by_person\n"


@pytest.mark.parametrize(
    "over,word",
    [
        ({"--outcome": "done"}, "refused:bad_outcome"),
        ({"--issue": "0"}, "refused:bad_issue"),
        ({"--project-id": "PVT_x y"}, "refused:bad_project_id"),
        ({"--repo": "SuperClaude-Org"}, "refused:bad_repo"),
        ({"--run": "0"}, "refused:bad_run"),
    ],
)
def test_a_refused_call_prints_a_refused_word_and_exits_one(
    monkeypatch, over: dict, word: str
) -> None:
    world = World()
    result = invoke(world, monkeypatch, **over)
    assert result.exit_code == 1 and result.output == f"{word}\n"
    assert world.argvs == []


def test_a_project_the_issue_is_not_on_is_refused_with_exit_one(monkeypatch) -> None:
    world = World(node("PVTI_other", "PVT_other", "Plan"))
    result = invoke(world, monkeypatch)
    assert result.exit_code == 1 and result.output == "refused:project_missing\n"
    assert world.posts == [] and world.mutations == []


def test_a_failed_move_prints_a_failed_word_and_exits_one(monkeypatch) -> None:
    world = World(node(status="Plan"))
    world.fail_move = True
    result = invoke(world, monkeypatch)
    assert result.exit_code == 1 and result.output == "failed:status_move\n"
    assert len(world.posts) == 1  # the comment stays


def test_the_project_id_and_run_id_are_passed_through(monkeypatch) -> None:
    world = World(node("PVTI_a", "PVT_other", "Plan"), node("PVTI_b", PROJECT, "Plan"))
    result = invoke(world, monkeypatch, **{"--run": "777"})
    assert result.exit_code == 0
    assert f"projectId={PROJECT}" in world.mutations[0]
    assert "itemId=PVTI_b" in world.mutations[0]
    assert complete.result_marker(ISSUE, 777) in world.posts[0]
    assert f"issues/{ISSUE}/comments" in " ".join(
        a for argv in world.argvs for a in argv if "POST" in argv
    )


def test_the_summary_file_is_read_and_no_issue_text_reaches_the_output(
    monkeypatch, tmp_path: Path
) -> None:
    summary = tmp_path / "result.md"
    summary.write_text("outcome: succeeded\nartifacts: a.md\npull_request: none\n")
    world = World(node(status="Plan"))
    world.other_comment("someone", f"{CANARY} a hostile comment")
    result = invoke(world, monkeypatch, "--summary", str(summary))
    assert result.exit_code == 0 and CANARY not in result.output
    assert "Artifacts: a.md" in world.posts[0]
    bad = tmp_path / "bad.md"
    bad.write_text(f"outcome: failed\nartifacts: {CANARY} x\npull_request: none\n")
    result = invoke(World(), monkeypatch, "--summary", str(bad))
    assert result.output == "refused:bad_summary\n" and CANARY not in result.output


def test_every_printed_word_is_a_closed_word(monkeypatch) -> None:
    for status in ("Plan", "Done"):
        out = invoke(World(node(status=status)), monkeypatch).output.strip()
        assert out in complete.RESULT_WORDS
    assert (
        invoke(World(), monkeypatch, **{"--outcome": "x"}).output.strip()
        in complete.RESULT_WORDS
    )


def test_the_verb_is_listed_in_the_group_help() -> None:
    result = CliRunner().invoke(issue_pipeline_group, ["--help"])
    assert "complete" in result.output
    help_text = CliRunner().invoke(issue_pipeline_group, ["complete", "--help"]).output
    assert "coordinator only" in help_text
