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


# --- review findings of PR 584: stable evidence identity, revoke, row shape -----


def test_the_same_evidence_at_a_later_time_is_not_appended_again(adir: Path) -> None:
    _adopt_started(adir)
    ar.record_create(
        adir, 9, "plan", H1, "label", "evt-1", "u_1", "2026-11-16T10:00:01Z"
    )
    again = ar.record_create(
        adir, 9, "plan", H1, "label", "evt-1", "u_1", "2026-11-16T10:09:59Z"
    )
    row = ar.record_show(adir, 9, "plan", H1)
    assert again["result"] == "exists" and len(row["evidence"]) == 1
    assert (
        row["evidence"][0]["time"] == "2026-11-16T10:00:01Z"
    )  # the first recording stands


def test_replaying_old_evidence_does_not_reopen_a_revoked_row(adir: Path) -> None:
    _adopt_started(adir)
    _create(adir, "label", "evt-1")
    ar.record_mark(adir, 9, "plan", H1, "revoked", T)
    replay = ar.record_create(
        adir, 9, "plan", H1, "label", "evt-1", "u_1", "2026-11-16T11:00:00Z"
    )
    assert replay["row"]["state"] == "revoked"
    with pytest.raises(ar.ApprovalError) as err:
        ar.record_mark(
            adir, 9, "plan", H1, "instructed", T
        )  # still no continuation without fresh evidence
    assert err.value.reason == "bad-move"
    fresh = ar.record_create(adir, 9, "plan", H1, "comment", "c-new", "u_1", T)
    assert fresh["row"]["state"] == "recorded"  # genuinely new evidence reopens it


def _row_path(adir: Path, kind: str) -> Path:
    return next(adir.glob(f"{kind}-*.json"))


@pytest.mark.parametrize(
    "damage",
    [
        lambda r: r.pop("evidence"),
        lambda r: r.update(junk="x"),
        lambda r: r.update(evidence=[]),
        lambda r: r.update(evidence="nope"),
        lambda r: r.update(evidence=[{"channel": "label", "id": "e1"}]),
        lambda r: r.update(kind="adoption"),
        lambda r: r.update(issue=10),
        lambda r: r.update(plan_hash="b" * 64),
        lambda r: r.update(record_id="ap-9-plan-ffffffffffff"),
        lambda r: r.update(state="bogus"),
        lambda r: r.update(updated_at="yesterday"),
        lambda r: r.update(evidence=r["evidence"] * 2),  # the same evidence twice
    ],
)
def test_a_structurally_damaged_approval_row_is_a_closed_refusal(
    adir: Path, damage
) -> None:
    _adopt_started(adir)
    _create(adir, "label", "e1")
    path = _row_path(adir, "approval")
    row = json.loads(path.read_text())
    damage(row)
    path.write_text(json.dumps(row))
    for call in (
        lambda: ar.record_show(adir, 9, "plan", H1),
        lambda: _create(adir, "comment", "c1"),
        lambda: ar.record_mark(adir, 9, "plan", H1, "instructed", T),
    ):
        with pytest.raises(ar.ApprovalError) as err:
            call()
        assert err.value.reason == "row-invalid"
    shown = CliRunner().invoke(
        issue_pipeline_group,
        ["record-show", str(adir), "--issue", "9", "--plan-hash", H1],
    )
    assert (shown.exit_code, shown.output.strip()) == (1, "refused:row-invalid")


@pytest.mark.parametrize(
    "damage",
    [
        lambda r: r.pop("dispatch_id"),
        lambda r: r.update(extra=1),
        lambda r: r.update(state="started", dispatch_id=None),
        lambda r: r.update(state="reserved", dispatch_id="ctx_1"),
        lambda r: r.update(stage="other"),
        lambda r: r.update(kind="approval"),
    ],
)
def test_a_structurally_damaged_adoption_row_is_a_closed_refusal(
    adir: Path, damage
) -> None:
    ar.adopt_create(adir, 9, "plan", T)
    path = _row_path(adir, "adoption")
    row = json.loads(path.read_text())
    damage(row)
    path.write_text(json.dumps(row))
    for call in (
        lambda: ar.adopt_show(adir, 9, "plan"),
        lambda: ar.adopt_create(adir, 9, "plan", T),
        lambda: ar.adopt_mark(adir, 9, "plan", "started", "ctx_2", T),
    ):
        with pytest.raises(ar.ApprovalError) as err:
            call()
        assert err.value.reason == "row-invalid"
