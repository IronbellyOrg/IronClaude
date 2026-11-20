"""The audit log: the 62-reason table pin, the line builders, the writer and rotation (design 4.7)."""

from __future__ import annotations

import json
import os

import pytest

from superclaude.cli.issue_watch import audit, launch, predicates, route

# The reasons the table lost, changed and gained (design 4.7). The table below is a
# literal copy: a change to the table has to change this test too.
REMOVED_14 = {
    "approvers_invalid", "worktree_invalid", "project_read_failed", "not_approved",
    "approval_before_trigger", "approval_before_init", "events_incomplete",
    "events_unreadable", "edited_after_approval", "project_mismatch",
    "project_unreadable", "edits_unreadable", "marker_unreadable", "re-approved",
}  # fmt: skip
RENAMED_5 = {
    "launched": "woken",
    "claimed": "acked",
    "claim_not_observed": "ack_not_observed",
    "launch_unknown": "wake_unknown",
    "prompt_invalid": "wake_line_invalid",
}
ADDED_17 = {
    "repos_invalid", "orchestrator_repo_invalid", "repo_not_listed", "repo_disabled",
    "checkout_missing", "no_session", "wake_write_failed", "mailbox_unavailable",
    "registry_invalid", "held_incomplete", "held_backlog", "hold_removed_by_hand",
    "hold_applied", "hold_released", "plan_requested", "hold_write_failed", "plan_stuck",
}  # fmt: skip

TABLE = {
    # cycle, exit 2
    "config_invalid": ("cycle", 2), "platform_unsupported": ("cycle", 2),
    "origin_mismatch": ("cycle", 2), "orca_not_found": ("cycle", 2),
    "account_id_mismatch": ("cycle", 2), "repos_invalid": ("cycle", 2),
    "orchestrator_repo_invalid": ("cycle", 2), "registry_invalid": ("cycle", 2),
    # cycle, exit 6 and 7
    "store_invalid": ("cycle", 6), "store_missing": ("cycle", 6), "lock_missing": ("cycle", 6),
    "lock_invalid": ("cycle", 6), "state_dir_unwritable": ("cycle", 6),
    "wake_write_failed": ("cycle", 6), "plan_stuck": ("cycle", 7),
    # cycle, the rest
    "login_invalid": ("cycle", 3), "gh_auth_failed": ("cycle", 3), "gh_timeout": ("cycle", 3),
    "gh_non_json": ("cycle", 3), "truncated": ("cycle", 4), "discovery_duplicate": ("cycle", 4),
    "rate_limited": ("cycle", 5), "rate_limit_clamped": ("cycle", 5), "lock_held": ("cycle", 75),
    "cycle_crashed": ("cycle", 1), "disabled": ("cycle", 0), "disabled_mid_cycle": ("cycle", 0),
    "not_enabled": ("cycle", 0), "cycle_complete": ("cycle", 0),
    # skip
    "unassigned": ("skip", 0), "assigned_other": ("skip", 0), "already_dispatched": ("skip", 0),
    "in_backoff": ("skip", 0), "day_cap": ("skip", 0), "budget_exhausted": ("skip", 0),
    "revalidation_failed": ("skip", 0), "repo_not_listed": ("skip", 0),
    "repo_disabled": ("skip", 0), "checkout_missing": ("skip", 0), "held_incomplete": ("skip", 0),
    "held_backlog": ("skip", 0), "hold_removed_by_hand": ("skip", 0),
    # entry
    "wake_line_invalid": ("entry", 7), "revalidation_transient": ("entry", 7),
    "attempts_exhausted": ("entry", 7), "spawn_error": ("entry", 7), "wake_unknown": ("entry", 7),
    "no_session": ("entry", 7), "ack_not_observed": ("entry", 7), "pending_orphan": ("entry", 0),
    "woken": ("entry", 0), "acked": ("entry", 0),
    # notes, warnings, reset
    "hold_applied": ("note", 0), "hold_released": ("note", 0), "plan_requested": ("note", 0),
    "discovery_count": ("warning", 0), "clock_skew": ("warning", 0),
    "dry_run_shadow_reset": ("warning", 0), "reset_refused": ("warning", 2),
    "mailbox_unavailable": ("warning", 0), "hold_write_failed": ("warning", 0),
    "operator_reset": ("skip/warning", 0),
}  # fmt: skip

STAMP = {
    "ts": "2026-11-19T12:00:00Z",
    "host": "h",
    "login": "me",
    "cycle_id": "a" * 32,
    "dry_run": False,
}


def test_the_reason_table_is_pinned_to_exactly_62_entries_with_a_kind_and_an_exit():
    assert len(TABLE) == 62
    assert dict(audit.REASON_TABLE) == TABLE
    assert audit.REASONS == frozenset(TABLE)
    for kind, code in audit.REASON_TABLE.values():
        assert isinstance(kind, str) and 0 <= code <= 255


def test_the_table_names_the_14_removed_the_5_renamed_and_the_17_added_reasons():
    old = {
        "approvers_invalid", "worktree_invalid", "project_read_failed", "not_approved",
        "approval_before_trigger", "approval_before_init", "events_incomplete",
        "events_unreadable", "edited_after_approval", "project_mismatch",
        "project_unreadable", "edits_unreadable", "marker_unreadable", *RENAMED_5,
    }  # fmt: skip
    assert len(REMOVED_14) == 14 and len(RENAMED_5) == 5 and len(ADDED_17) == 17
    assert not (REMOVED_14 & audit.REASONS)  # none of the 14 survives
    assert not (set(RENAMED_5) & audit.REASONS)  # the five old names are gone ...
    assert set(RENAMED_5.values()) <= audit.REASONS  # ... and the new names are in
    assert ADDED_17 <= audit.REASONS
    assert len(old) == 18 and 59 - 14 - 5 + 5 + 17 == 62


def test_the_changed_exit_codes_and_the_resend_meaning():
    assert audit.REASON_TABLE["ack_not_observed"] == (
        "entry",
        7,
    )  # was 0: the owner must see it
    assert audit.REASON_TABLE["attempts_exhausted"] == ("entry", 7)  # was 0
    assert audit.REASON_TABLE["pending_orphan"] == (
        "entry",
        0,
    )  # now "resend", never "abandon"
    assert audit.REASON_TABLE["plan_stuck"] == ("cycle", 7)
    assert audit.REASON_TABLE["origin_mismatch"] == (
        "cycle",
        2,
    )  # one meaning, one kind (F4)


def test_the_module_docstring_states_the_origin_mismatch_choice_and_the_ack_reason_rule():
    text = audit.__doc__ or ""
    assert "origin_mismatch" in text and "ONE meaning" in text
    assert "ack_reason" in text and "claimed_elsewhere" in text


def test_the_pattern_copies_equal_the_package_patterns():
    assert audit._REPO_SHAPE.pattern == predicates.REPO_PATTERN.pattern
    assert audit._WAKE_ID_SHAPE.pattern == predicates.WAKE_ID_PATTERN.pattern
    assert audit._WAKE_ID_SHAPE.pattern == launch.WAKE_ID_PATTERN.pattern
    assert (
        audit._ORCHESTRATOR_SHAPE.pattern == predicates.ORCHESTRATOR_ID_PATTERN.pattern
    )
    assert route.ORCHESTRATOR_ID_PATTERN is predicates.ORCHESTRATOR_ID_PATTERN
    assert predicates.OPERATION_ID_PATTERN.pattern == launch.HANDLE_PATTERN.pattern


# --- the builders ------------------------------------------------------------------------------


def test_a_cycle_line_has_the_closed_key_set():
    line = audit.cycle_line(
        **STAMP,
        exit_code=0,
        reason="cycle_complete",
        gh_calls=3,
        duration_ms=5,
        discovery_count=2,
    )
    assert set(line) == {
        "kind", "ts", "host", "login", "cycle_id", "dry_run", "reason", "exit",
        "gh_calls", "duration_ms", "discovery_count",
    }  # fmt: skip


def test_a_decision_line_names_the_repo_and_carries_no_approval_field():
    line = audit.decision_line(
        **STAMP, reason="woken", repo="IronbellyOrg/IronClaude", issue=5, state="woken",
        orchestrator="ironclaude-1", wake_id="20261119T120000Z-0000000a", stages="input_accepted,turn_started",
    )  # fmt: skip
    assert line["repo"] == "IronbellyOrg/IronClaude" and line["issue"] == 5
    assert not {"approver_id", "approval_event_id", "approved_at"} & set(line)
    with pytest.raises(TypeError):
        audit.decision_line(**STAMP, reason="woken", repo="o/r", issue=5, approver_id=1)  # type: ignore[call-arg]


@pytest.mark.parametrize(
    "bad",
    [
        {"repo": "no-slash"},
        {"repo": "o/r\n"},
        {"issue": 0},
        {"issue": True},
        {"orchestrator": "Iron-1"},
        {"orchestrator": "ironclaude-0"},
        {"wake_id": "20261119T120000Z-ZZZZZZZZ"},
        {"stages": "input_accepted; rm -rf"},
        {"state": "launched"},
        {"reason": "approvers_invalid"},
        {"reason": "no_such_reason"},
    ],
)
def test_a_decision_value_outside_its_closed_shape_is_refused(bad):
    fields = {"reason": "woken", "repo": "o/r", "issue": 5, **bad}
    with pytest.raises(ValueError):
        audit.decision_line(**STAMP, **fields)


def test_a_hold_note_is_a_note_or_the_reason_of_a_decision_line_only():
    for note in ("hold_applied", "hold_released", "plan_requested"):
        line = audit.decision_line(**STAMP, reason=note, repo="o/r", issue=5)
        assert line["reason"] == note
        audit.decision_line(
            **STAMP, reason="held_incomplete", repo="o/r", issue=5, note=note
        )
        with pytest.raises(ValueError):  # not a cycle reason, not a warning reason
            audit.cycle_line(
                **STAMP, exit_code=0, reason=note, gh_calls=0, duration_ms=0
            )
        with pytest.raises(ValueError):
            audit.warning_line(**STAMP, reason=note)
    with pytest.raises(ValueError):  # a note value must be a note
        audit.decision_line(**STAMP, reason="woken", repo="o/r", issue=5, note="woken")


def test_a_warning_line_may_name_a_repo_and_an_issue():
    line = audit.warning_line(**STAMP, reason="hold_write_failed", repo="o/r", issue=7)
    assert (line["repo"], line["issue"]) == ("o/r", 7)
    with pytest.raises(ValueError):
        audit.warning_line(**STAMP, reason="hold_write_failed", repo="bad repo")


def test_host_and_login_stay_bounded_tokens():
    with pytest.raises(ValueError):
        audit.cycle_line(
            **{**STAMP, "login": "has space"},
            exit_code=0,
            reason="cycle_complete",
            gh_calls=0,
            duration_ms=0,
        )
    with pytest.raises(ValueError):
        audit.cycle_line(
            **{**STAMP, "host": "x" * 256},
            exit_code=0,
            reason="cycle_complete",
            gh_calls=0,
            duration_ms=0,
        )


# --- the writer ----------------------------------------------------------------------------------


def test_append_writes_one_json_line_at_mode_0600(tmp_path):
    log = audit.AuditLog(tmp_path)
    log.append(audit.warning_line(**STAMP, reason="clock_skew", clock_skew_s=70))
    log.append(audit.warning_line(**STAMP, reason="clock_skew", clock_skew_s=71))
    lines = (tmp_path / "audit.jsonl").read_text().splitlines()
    assert [json.loads(x)["clock_skew_s"] for x in lines] == [70, 71]
    assert oct(os.stat(tmp_path / "audit.jsonl").st_mode & 0o777) == "0o600"


def test_rotation_keeps_four_files_and_is_a_no_op_below_the_limit(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(audit, "ROTATE_BYTES", 100)
    log = audit.AuditLog(tmp_path)
    log.rotate_if_needed()  # no file yet
    for n in range(6):
        (tmp_path / "audit.jsonl").write_text("#" + "x" * 200 + f"{n}\n")
        log.rotate_if_needed()
    names = sorted(p.name for p in tmp_path.iterdir())
    assert names == ["audit.jsonl.1", "audit.jsonl.2", "audit.jsonl.3", "audit.jsonl.4"]
    (tmp_path / "audit.jsonl").write_text("small\n")
    log.rotate_if_needed()
    assert (tmp_path / "audit.jsonl").exists()


def test_stderr_fallback_writes_only_the_closed_keys(capsys):
    audit.stderr_fallback("repos_invalid", 2, ts="2026-11-19T12:00:00Z", host="h")
    out = json.loads(capsys.readouterr().err)
    assert out == {
        "kind": "cycle",
        "ts": "2026-11-19T12:00:00Z",
        "host": "h",
        "exit": 2,
        "reason": "repos_invalid",
    }
    with pytest.raises(ValueError):
        audit.stderr_fallback("approvers_invalid", 2)
