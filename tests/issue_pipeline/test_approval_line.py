"""Task 2: the approval line and the ``check-approval`` verb."""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.issue_pipeline import approval_line, plan_hash
from superclaude.cli.issue_pipeline.cli import issue_pipeline_group

H = "0123456789abcdef" * 4  # 64 hex
RID = f"ap-9-plan-{H[:12]}"


def _long(rid: str = RID, h: str = H) -> str:
    return f"approved {rid} plan-sha256={h}"


@pytest.mark.parametrize("text", ["approved", _long()])
def test_the_two_accepted_texts(text: str) -> None:
    assert approval_line.parse(text)[0] in ("short", "long")


@pytest.mark.parametrize(
    "text",
    [
        " approved",
        "approved ",
        "approved\n",
        "Approved",
        "APPROVED",
        "approved\napproved",
        " " + _long(),
        _long() + " ",
        _long() + "\n",
        _long() + " extra",
        _long() + "\nsecond line",
        _long(rid="ap-x-plan-0123456789ab"),  # wrong id shape
        _long(rid="ap-9-plan-0123456789a"),  # short id hex
        _long(rid="ap-0-plan-0123456789ab"),  # issue starts with zero
        _long(h=H[:63]),  # 63-character hash
        _long(h=H + "0"),  # 65-character hash
        _long(h=H.upper()),
        "approved plan-sha256=" + H,
        "",
    ],
)
def test_every_variant_is_rejected(text: str) -> None:
    assert approval_line.parse(text) == ("none", None, None)


@pytest.fixture
def plan_dir(tmp_path: Path) -> Path:
    (tmp_path / "plan.md").write_text("the plan")
    (tmp_path / "design.md").write_text("the design")
    return tmp_path


def _good_line(plan_dir: Path, issue: int = 9) -> str:
    digest = plan_hash.compute(plan_dir, ["plan.md", "design.md"])[1]
    return _long(approval_line.record_id(issue, digest), digest)


def test_check_ok_for_the_matching_long_form(plan_dir: Path) -> None:
    line = _good_line(plan_dir)
    assert approval_line.check(plan_dir, ["plan.md", "design.md"], line) == "ok"
    assert approval_line.check(plan_dir, ["plan.md", "design.md"], line, issue=9) == "ok"


def test_check_refuses_after_one_byte_changes(plan_dir: Path) -> None:
    line = _good_line(plan_dir)
    (plan_dir / "plan.md").write_text("the plaN")
    assert approval_line.check(plan_dir, ["plan.md", "design.md"], line) == "refused:mismatch"


def test_check_refuses_a_bare_approved_from_the_worker(plan_dir: Path) -> None:
    assert approval_line.check(plan_dir, ["plan.md", "design.md"], "approved") == "refused:bare"


def test_check_refuses_a_wrong_issue_and_a_foreign_prefix(plan_dir: Path) -> None:
    digest = plan_hash.compute(plan_dir, ["plan.md", "design.md"])[1]
    assert approval_line.check(plan_dir, ["plan.md", "design.md"], _good_line(plan_dir), issue=10) == "refused:mismatch"
    bad_prefix = _long(rid="ap-9-plan-ffffffffffff", h=digest)
    assert approval_line.check(plan_dir, ["plan.md", "design.md"], bad_prefix) == "refused:mismatch"


def test_check_closed_words_for_malformed_and_plan_errors(plan_dir: Path) -> None:
    assert approval_line.check(plan_dir, ["plan.md"], "approve") == "refused:malformed"
    assert approval_line.check(plan_dir, ["missing.md"], _long()) == "refused:missing"


def test_cli_exit_codes_and_closed_output(plan_dir: Path) -> None:
    runner = CliRunner()
    ok = runner.invoke(issue_pipeline_group, ["check-approval", str(plan_dir), "plan.md", "design.md", "--line", _good_line(plan_dir)])
    assert (ok.exit_code, ok.output.strip()) == (0, "ok")
    bare = runner.invoke(issue_pipeline_group, ["check-approval", str(plan_dir), "plan.md", "design.md", "--line", "approved"])
    assert (bare.exit_code, bare.output.strip()) == (1, "refused:bare")


def test_the_module_prints_and_reads_nothing_itself() -> None:
    source = inspect.getsource(approval_line)
    for banned in ("print(", "open(", "read_text", "read_bytes", "stdout", "stderr"):
        assert banned not in source, banned
