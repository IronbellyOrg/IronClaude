"""Task 3: the approval record helper, rows and verbs."""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.issue_pipeline import approval_record as ar
from superclaude.cli.issue_pipeline.cli import issue_pipeline_group

H1 = "0123456789abcdef" * 4
H2 = "fedcba9876543210" * 4
T = "2026-11-16T10:00:00Z"


@pytest.fixture
def adir(tmp_path: Path) -> Path:
    d = tmp_path / "approvals"
    ar.init_dir(d)
    return d


def _adopt_started(d: Path, issue: int = 9) -> None:
    ar.adopt_create(d, issue, "plan", T)
    ar.adopt_mark(d, issue, "plan", "started", "ctx_abc123", T)


def _create(d: Path, channel: str, ev: str, h: str = H1, issue: int = 9) -> dict:
    return ar.record_create(d, issue, "plan", h, channel, ev, "u_1", T)


def test_init_makes_a_private_directory_and_lock(tmp_path: Path) -> None:
    d = tmp_path / "x"
    ar.init_dir(d)
    ar.init_dir(d)  # safe to repeat
    assert stat.S_IMODE(d.stat().st_mode) == 0o700
    assert stat.S_IMODE((d / "lock").stat().st_mode) == 0o600


def test_record_create_before_init_fails_with_a_closed_reason(tmp_path: Path) -> None:
    d = tmp_path / "no-init"
    d.mkdir()
    result = CliRunner().invoke(
        issue_pipeline_group,
        [
            "record-create",
            str(d),
            "--issue",
            "9",
            "--plan-hash",
            H1,
            "--channel",
            "label",
            "--evidence-id",
            "e1",
            "--actor",
            "u1",
        ],
    )
    assert result.exit_code == 1 and result.output.strip() == "refused:not-initialized"
    assert "Traceback" not in result.output
    missing = CliRunner().invoke(
        issue_pipeline_group,
        ["record-show", str(tmp_path / "absent"), "--issue", "9", "--plan-hash", H1],
    )
    assert missing.output.strip() == "refused:no-row"


def test_after_init_the_first_call_succeeds(adir: Path) -> None:
    _adopt_started(adir)
    assert _create(adir, "label", "e1")["result"] == "created"


def test_label_then_comment_leave_one_row_with_two_evidence_entries(adir: Path) -> None:
    _adopt_started(adir)
    first = _create(adir, "label", "evt-1")
    second = _create(adir, "comment", "cmt-2")
    assert (first["result"], second["result"]) == ("created", "exists")
    row = ar.record_show(adir, 9, "plan", H1)
    assert [e["channel"] for e in row["evidence"]] == ["label", "comment"]
    assert len(list(adir.glob("approval-*.json"))) == 1
    assert row["record_id"] == "ap-9-plan-" + H1[:12]


def test_the_same_evidence_twice_is_not_appended_twice(adir: Path) -> None:
    _adopt_started(adir)
    _create(adir, "label", "evt-1")
    _create(adir, "label", "evt-1")
    assert len(ar.record_show(adir, 9, "plan", H1)["evidence"]) == 1


def test_a_different_plan_hash_makes_a_different_row(adir: Path) -> None:
    _adopt_started(adir)
    _create(adir, "label", "evt-1", H1)
    _create(adir, "label", "evt-1", H2)
    assert len(list(adir.glob("approval-*.json"))) == 2


def test_record_create_needs_an_adoption_row(adir: Path) -> None:
    with pytest.raises(ar.ApprovalError) as err:
        _create(adir, "label", "e1")
    assert err.value.reason == "no-adoption"


def test_record_mark_allows_only_forward_moves_and_revoke(adir: Path) -> None:
    _adopt_started(adir)
    _create(adir, "label", "e1")

    def mark(state: str) -> str:
        return ar.record_mark(adir, 9, "plan", H1, state, T)["row"]["state"]

    for bad in ("acked", "recorded", "bogus"):
        with pytest.raises(ar.ApprovalError) as err:
            mark(bad)
        assert err.value.reason == "bad-move"
    assert mark("instructed") == "instructed"
    with pytest.raises(ar.ApprovalError):
        mark("instructed")  # a second continuation instruction is refused
    assert mark("acked") == "acked"
    with pytest.raises(ar.ApprovalError):
        mark("instructed")  # no way back
    assert mark("revoked") == "revoked"
    with pytest.raises(ar.ApprovalError):
        mark("revoked")


@pytest.mark.parametrize("prefix", [[], ["instructed"], ["instructed", "acked"]])
def test_revoke_from_every_state_and_re_approval_reopens_the_same_row(
    adir: Path, prefix: list[str]
) -> None:
    _adopt_started(adir)
    _create(adir, "label", "e1")
    for state in prefix:
        ar.record_mark(adir, 9, "plan", H1, state, T)
    assert (
        ar.record_mark(adir, 9, "plan", H1, "revoked", T)["row"]["state"] == "revoked"
    )
    again = _create(adir, "comment", "c9")
    assert again["result"] == "exists" and again["row"]["state"] == "recorded"
    assert len(list(adir.glob("approval-*.json"))) == 1


def test_adoption_reserve_start_and_uncertain_paths(adir: Path) -> None:
    assert ar.adopt_create(adir, 5, "plan", T)["row"]["state"] == "reserved"
    with pytest.raises(ar.ApprovalError) as err:
        ar.adopt_create(adir, 5, "plan", T)
    assert err.value.reason == "uncertain-launch"
    ar.adopt_mark(adir, 5, "plan", "uncertain", None, T)
    with pytest.raises(ar.ApprovalError) as err:
        ar.adopt_create(adir, 5, "plan", T)
    assert err.value.reason == "uncertain-launch"
    # a person settles an uncertain row after reading worker-list
    assert (
        ar.adopt_mark(adir, 5, "plan", "started", "ctx_1", T)["row"]["dispatch_id"]
        == "ctx_1"
    )
    with pytest.raises(ar.ApprovalError) as err:
        ar.adopt_create(adir, 5, "plan", T)
    assert err.value.reason == "already-started"
    with pytest.raises(ar.ApprovalError):
        ar.adopt_mark(adir, 5, "plan", "uncertain", None, T)


def test_started_needs_a_valid_dispatch_id(adir: Path) -> None:
    ar.adopt_create(adir, 5, "plan", T)
    for bad in (None, "", "has space", "x" * 81):
        with pytest.raises(ar.ApprovalError) as err:
            ar.adopt_mark(adir, 5, "plan", "started", bad, T)
        assert err.value.reason == "bad-dispatch-id"


@pytest.mark.parametrize(
    "kwargs",
    [
        {"channel": "email"},
        {"evidence_id": "has space"},
        {"evidence_id": "x" * 81},
        {"actor": "<b>"},
        {"plan_hash": "ABC"},
        {"stage": "Plan"},
        {"issue": 0},
    ],
)
def test_stored_values_must_match_fixed_patterns(adir: Path, kwargs: dict) -> None:
    _adopt_started(adir)
    args = {
        "issue": 9,
        "stage": "plan",
        "plan_hash": H1,
        "channel": "label",
        "evidence_id": "e1",
        "actor": "u1",
        "now": T,
    }
    args.update(kwargs)
    with pytest.raises(ar.ApprovalError):
        ar.record_create(adir, **args)


def test_a_corrupt_row_is_a_closed_refusal_and_files_are_private(adir: Path) -> None:
    _adopt_started(adir)
    _create(adir, "label", "e1")
    row_file = next(adir.glob("approval-*.json"))
    assert stat.S_IMODE(row_file.stat().st_mode) == 0o600
    row_file.write_text("{not json")
    with pytest.raises(ar.ApprovalError) as err:
        ar.record_show(adir, 9, "plan", H1)
    assert err.value.reason == "row-invalid"


def test_a_symlinked_row_is_refused(adir: Path, tmp_path: Path) -> None:
    target = tmp_path / "elsewhere.json"
    target.write_text(json.dumps({"state": "recorded"}))
    (adir / "adoption-9-plan.json").symlink_to(target)
    with pytest.raises(ar.ApprovalError) as err:
        ar.adopt_create(adir, 9, "plan", T)
    assert err.value.reason == "row-invalid"


def test_cli_round_trip_prints_closed_json(adir: Path) -> None:
    run = CliRunner()
    base = [str(adir), "--issue", "9"]
    assert (
        json.loads(run.invoke(issue_pipeline_group, ["adopt-create", *base]).output)[
            "result"
        ]
        == "created"
    )
    run.invoke(
        issue_pipeline_group,
        ["adopt-mark", *base, "--state", "started", "--dispatch-id", "ctx_1"],
    )
    made = run.invoke(
        issue_pipeline_group,
        [
            "record-create",
            *base,
            "--plan-hash",
            H1,
            "--channel",
            "label",
            "--evidence-id",
            "e1",
            "--actor",
            "u1",
        ],
    )
    assert json.loads(made.output)["row"]["state"] == "recorded"
    marked = run.invoke(
        issue_pipeline_group,
        ["record-mark", *base, "--plan-hash", H1, "--state", "instructed"],
    )
    assert json.loads(marked.output)["row"]["state"] == "instructed"
    shown = run.invoke(issue_pipeline_group, ["record-show", *base, "--plan-hash", H1])
    assert json.loads(shown.output)["row"]["state"] == "instructed"
    again = run.invoke(
        issue_pipeline_group,
        ["record-mark", *base, "--plan-hash", H1, "--state", "instructed"],
    )
    assert (again.exit_code, again.output.strip()) == (1, "refused:bad-move")


def test_lock_held_reports_retry_with_exit_75(adir: Path) -> None:
    import fcntl

    _adopt_started(adir)
    fd = os.open(adir / "lock", os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        result = CliRunner().invoke(
            issue_pipeline_group,
            [
                "record-create",
                str(adir),
                "--issue",
                "9",
                "--plan-hash",
                H1,
                "--channel",
                "label",
                "--evidence-id",
                "e1",
                "--actor",
                "u1",
            ],
        )
    finally:
        os.close(fd)
    assert (result.exit_code, result.output.strip()) == (75, "lock-held, retry")
    # the retry appends the evidence
    assert _create(adir, "label", "e1")["result"] == "created"


def test_the_watcher_record_module_is_not_edited() -> None:
    import subprocess

    out = subprocess.run(
        [
            "git",
            "diff",
            "--stat",
            "HEAD",
            "--",
            "src/superclaude/cli/issue_watch/record.py",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert out.strip() == ""
