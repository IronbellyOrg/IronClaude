"""Task 1: the plan hash and the ``issue-pipeline plan-hash`` verb."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.issue_pipeline import plan_hash
from superclaude.cli.issue_pipeline.cli import issue_pipeline_group


@pytest.fixture
def report(tmp_path: Path) -> Path:
    (tmp_path / "a.md").write_bytes(b"alpha")
    (tmp_path / "b.md").write_bytes(b"beta")
    return tmp_path


def _hash(report: Path, *names: str) -> str:
    return plan_hash.compute(report, list(names))[1]


def test_cli_prints_ordered_list_and_a_64_hex_hash(report: Path) -> None:
    result = CliRunner().invoke(issue_pipeline_group, ["plan-hash", str(report), "b.md", "a.md"])
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert lines[:2] == ["file: a.md", "file: b.md"]
    assert re.fullmatch(r"plan-sha256: [0-9a-f]{64}", lines[2])


def test_argument_order_does_not_change_the_hash(report: Path) -> None:
    assert _hash(report, "a.md", "b.md") == _hash(report, "b.md", "a.md")


def test_one_byte_changes_the_hash(report: Path) -> None:
    before = _hash(report, "a.md", "b.md")
    (report / "a.md").write_bytes(b"alphb")
    assert _hash(report, "a.md", "b.md") != before


def test_rename_changes_the_hash(report: Path) -> None:
    before = _hash(report, "a.md", "b.md")
    (report / "a.md").rename(report / "c.md")
    assert _hash(report, "c.md", "b.md") != before


def test_swapping_bytes_between_two_files_changes_the_hash(report: Path) -> None:
    before = _hash(report, "a.md", "b.md")
    (report / "a.md").write_bytes(b"alphabeta"[:6])  # "alphab"
    (report / "b.md").write_bytes(b"eta")
    assert _hash(report, "a.md", "b.md") != before


def test_adding_a_file_changes_the_hash(report: Path) -> None:
    before = _hash(report, "a.md", "b.md")
    (report / "c.md").write_bytes(b"")
    assert _hash(report, "a.md", "b.md", "c.md") != before


@pytest.mark.parametrize(
    ("make", "name", "reason"),
    [
        ("symlink", "link.md", "symlink"),
        ("none", "/etc/hostname", "absolute-name"),
        ("none", "../a.md", "dotdot-name"),
        ("none", "sub/../a.md", "dotdot-name"),
        ("none", "missing.md", "missing"),
        ("none", "a.md", "duplicate-name"),
    ],
)
def test_refusals_exit_non_zero_with_a_closed_reason(report: Path, make: str, name: str, reason: str) -> None:
    secret = report.parent / "outside-secret.txt"
    secret.write_text("CANARY-FILE-TEXT")
    if make == "symlink":
        (report / "link.md").symlink_to(secret)
    names = ["a.md", name] if reason == "duplicate-name" else [name]
    result = CliRunner().invoke(issue_pipeline_group, ["plan-hash", str(report), *names])
    assert result.exit_code != 0
    assert result.output.strip() == f"refused:{reason}"
    assert "CANARY" not in result.output


def test_a_symlinked_directory_component_is_refused(report: Path, tmp_path_factory: pytest.TempPathFactory) -> None:
    other = tmp_path_factory.mktemp("other")
    (other / "x.md").write_text("x")
    (report / "sub").symlink_to(other)
    with pytest.raises(plan_hash.PlanHashError) as err:
        plan_hash.compute(report, ["sub/x.md"])
    assert err.value.reason == "symlink"


def test_no_names_and_a_bad_directory_are_refused(report: Path) -> None:
    with pytest.raises(plan_hash.PlanHashError) as err:
        plan_hash.compute(report, [])
    assert err.value.reason == "no-names"
    with pytest.raises(plan_hash.PlanHashError) as err:
        plan_hash.compute(report / "nope", ["a.md"])
    assert err.value.reason == "bad-dir"


def test_a_directory_is_not_a_plan_file(report: Path) -> None:
    (report / "d").mkdir()
    with pytest.raises(plan_hash.PlanHashError) as err:
        plan_hash.compute(report, ["d"])
    assert err.value.reason == "not-a-file"
