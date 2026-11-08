"""Tests for the audit log: reason table pin, line builders, writer, rotation.

The 59 reason names and the (kind, exit) table below are literal copies of the
closed reason table (spec lines 330-358 plus the five proposals DF-02, DF-03,
DF-22 and DF-57, and the two Gate C proposals ``cycle_complete`` (exit 0) and
``cycle_crashed`` (exit 1), fix findings C-2 and C-3). They are never imported
from the module under test and never read from the design or spec (decision
DF-31), so adding or removing a name in ``audit.py`` fails the pin test.
"""

from __future__ import annotations

import json
import os
import stat
from datetime import datetime, timezone

import pytest

from superclaude.cli.issue_watch import audit
from superclaude.cli.issue_watch.audit import (
    REASON_TABLE,
    REASONS,
    AuditLog,
    cycle_line,
    decision_line,
    line,
    stderr_fallback,
    warning_line,
)
from superclaude.cli.issue_watch.predicates import MAX_ISSUE_NUMBER

from .conftest import FakeClock

MIB = 1024 * 1024
ROTATE_AT = 5 * MIB

# The 59 reason names, in the order of the reason table.
EXPECTED_NAMES = [
    "config_invalid",
    "approvers_invalid",
    "platform_unsupported",
    "worktree_invalid",
    "origin_mismatch",
    "orca_not_found",
    "account_id_mismatch",
    "store_invalid",
    "store_missing",
    "lock_missing",
    "lock_invalid",
    "state_dir_unwritable",
    "login_invalid",
    "gh_auth_failed",
    "gh_timeout",
    "gh_non_json",
    "project_read_failed",
    "truncated",
    "discovery_duplicate",
    "rate_limited",
    "rate_limit_clamped",
    "lock_held",
    "cycle_crashed",
    "disabled",
    "disabled_mid_cycle",
    "not_enabled",
    "cycle_complete",
    "not_approved",
    "approval_before_trigger",
    "approval_before_init",
    "events_incomplete",
    "events_unreadable",
    "edited_after_approval",
    "project_mismatch",
    "project_unreadable",
    "unassigned",
    "assigned_other",
    "already_dispatched",
    "in_backoff",
    "day_cap",
    "budget_exhausted",
    "revalidation_failed",
    "marker_unreadable",
    "edits_unreadable",
    "prompt_invalid",
    "revalidation_transient",
    "attempts_exhausted",
    "spawn_error",
    "launch_unknown",
    "pending_orphan",
    "claim_not_observed",
    "launched",
    "claimed",
    "re-approved",
    "discovery_count",
    "clock_skew",
    "dry_run_shadow_reset",
    "reset_refused",
    "operator_reset",
]

# name -> (kind, exit), written out in full.
EXPECTED_TABLE = {
    "config_invalid": ("cycle", 2),
    "approvers_invalid": ("cycle", 2),
    "platform_unsupported": ("cycle", 2),
    "worktree_invalid": ("cycle", 2),
    "origin_mismatch": ("cycle", 2),
    "orca_not_found": ("cycle", 2),
    "account_id_mismatch": ("cycle", 2),
    "store_invalid": ("cycle", 6),
    "store_missing": ("cycle", 6),
    "lock_missing": ("cycle", 6),
    "lock_invalid": ("cycle", 6),
    "state_dir_unwritable": ("cycle", 6),
    "login_invalid": ("cycle", 3),
    "gh_auth_failed": ("cycle", 3),
    "gh_timeout": ("cycle", 3),
    "gh_non_json": ("cycle", 3),
    "project_read_failed": ("cycle", 3),
    "truncated": ("cycle", 4),
    "discovery_duplicate": ("cycle", 4),
    "rate_limited": ("cycle", 5),
    "rate_limit_clamped": ("cycle", 5),
    "lock_held": ("cycle", 75),
    "cycle_crashed": ("cycle", 1),
    "disabled": ("cycle", 0),
    "disabled_mid_cycle": ("cycle", 0),
    "not_enabled": ("cycle", 0),
    "cycle_complete": ("cycle", 0),
    "not_approved": ("skip", 0),
    "approval_before_trigger": ("skip", 0),
    "approval_before_init": ("skip", 0),
    "events_incomplete": ("skip", 0),
    "events_unreadable": ("skip", 0),
    "edited_after_approval": ("skip", 0),
    "project_mismatch": ("skip", 0),
    "project_unreadable": ("skip", 0),
    "unassigned": ("skip", 0),
    "assigned_other": ("skip", 0),
    "already_dispatched": ("skip", 0),
    "in_backoff": ("skip", 0),
    "day_cap": ("skip", 0),
    "budget_exhausted": ("skip", 0),
    "revalidation_failed": ("skip", 0),
    "marker_unreadable": ("skip", 0),
    "edits_unreadable": ("skip", 0),
    "prompt_invalid": ("entry", 7),
    "revalidation_transient": ("entry", 7),
    "attempts_exhausted": ("entry", 0),
    "spawn_error": ("entry", 7),
    "launch_unknown": ("entry", 7),
    "pending_orphan": ("entry", 0),
    "claim_not_observed": ("entry", 0),
    "launched": ("entry", 0),
    "claimed": ("entry", 0),
    "re-approved": ("note", 0),
    "discovery_count": ("warning", 0),
    "clock_skew": ("warning", 0),
    "dry_run_shadow_reset": ("warning", 0),
    "reset_refused": ("warning", 2),
    "operator_reset": ("skip/warning", 0),
}

# Reasons that are only ever the value of a ``note`` key, never a line reason.
NOTE_ONLY = {"re-approved"}
LINE_REASONS = [name for name in EXPECTED_NAMES if name not in NOTE_ONLY]

# Keys that must never appear on any line (design line 718).
FORBIDDEN_KEYS = ["rate_remaining", "title", "body", "label", "label_name", "stderr"]


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock(datetime(2026, 11, 7, 12, 0, 0, tzinfo=timezone.utc))


@pytest.fixture
def ts(clock: FakeClock) -> str:
    return clock.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def common(ts: str, **over: object) -> dict:
    """The keyword arguments every builder takes."""
    base = {
        "ts": ts,
        "host": "box1",
        "login": "octo",
        "cycle_id": "c" * 32,
        "dry_run": False,
    }
    base.update(over)
    return base


def big_file(path, marker: bytes, size: int = ROTATE_AT) -> None:
    """Create ``path`` holding ``marker`` and extended to ``size`` bytes."""
    with open(path, "wb") as handle:
        handle.write(marker)
        handle.truncate(size)


def head(path, count: int = 5) -> bytes:
    with open(path, "rb") as handle:
        return handle.read(count)


def names_in(directory) -> list[str]:
    return sorted(p.name for p in directory.iterdir())


# ---------------------------------------------------------------- reason table


def test_reasons_pin_59_names__ac14_fr020_nfr006():
    assert len(EXPECTED_NAMES) == 59
    assert len(set(EXPECTED_NAMES)) == 59
    assert isinstance(REASONS, frozenset)
    assert REASONS == frozenset(EXPECTED_NAMES)
    assert len(REASON_TABLE) == 59
    assert list(REASON_TABLE) == EXPECTED_NAMES


def test_reason_table_kind_and_exit__ac14_fr020_nfr006():
    assert set(EXPECTED_TABLE) == set(EXPECTED_NAMES)
    assert REASON_TABLE == EXPECTED_TABLE
    for name, (kind, code) in EXPECTED_TABLE.items():
        assert REASON_TABLE[name] == (kind, code), name


# ----------------------------------------------------------------- line checks


@pytest.mark.parametrize("kind", ["cycle", "decision", "warning"])
def test_line_unknown_reason_raises__ac14_fr020_nfr006(kind, ts):
    fields = common(ts, reason="typo_reason")
    if kind == "cycle":
        fields.update(exit=0, gh_calls=1, duration_ms=2)
    if kind == "decision":
        fields.update(
            issue=1, approver_id=None, approval_event_id=None, approved_at=None
        )
    with pytest.raises(ValueError):
        line(kind, **fields)


def test_line_note_name_is_not_a_reason__ac14_fr020_nfr006(ts):
    with pytest.raises(ValueError):
        warning_line(**common(ts, reason="re-approved"))


def test_line_unknown_kind_raises__ac14_fr020_nfr006(ts):
    with pytest.raises(ValueError):
        line("skip", **common(ts, reason="not_approved"))


def test_line_key_outside_kind_set_raises__ac14_fr020_nfr006(ts):
    cycle = common(ts, reason="disabled", exit=0, gh_calls=0, duration_ms=1)
    # ``issue`` belongs to decision and warning lines only.
    with pytest.raises(ValueError):
        line("cycle", issue=3, **cycle)
    warn = common(ts, reason="clock_skew")
    # ``exit`` and ``state`` are not warning keys.
    with pytest.raises(ValueError):
        line("warning", exit=0, **warn)
    with pytest.raises(ValueError):
        line("warning", state="pending", **warn)


def test_line_missing_required_key_raises__ac14_fr020_nfr006(ts):
    with pytest.raises(ValueError):
        line("cycle", **common(ts, reason="disabled", exit=0))
    with pytest.raises(ValueError):
        line("decision", **common(ts, reason="not_approved", issue=1))


@pytest.mark.parametrize("key", FORBIDDEN_KEYS)
def test_line_rejects_forbidden_keys__ac14_fr020_nfr006(key, ts):
    cycle = common(ts, reason="disabled", exit=0, gh_calls=0, duration_ms=1)
    warn = common(ts, reason="clock_skew")
    decision = common(
        ts,
        reason="not_approved",
        issue=1,
        approver_id=None,
        approval_event_id=None,
        approved_at=None,
    )
    for kind, fields in (("cycle", cycle), ("warning", warn), ("decision", decision)):
        with pytest.raises(ValueError):
            line(kind, **{**fields, key: "free text from an issue"})


@pytest.mark.parametrize("key", FORBIDDEN_KEYS)
def test_builders_never_emit_forbidden_keys__ac14_fr020_nfr006(key, ts):
    extra = {key: "free text from an issue"}
    with pytest.raises(TypeError):
        cycle_line(
            **common(ts, reason="disabled"),
            exit_code=0,
            gh_calls=0,
            duration_ms=1,
            **extra,
        )
    with pytest.raises(TypeError):
        decision_line(**common(ts, reason="not_approved"), issue=1, **extra)
    with pytest.raises(TypeError):
        warning_line(**common(ts, reason="clock_skew"), **extra)


def test_builders_output_holds_no_forbidden_key__ac14_fr020_nfr006(ts):
    built = [
        cycle_line(
            **common(ts, reason="gh_timeout"),
            exit_code=3,
            gh_calls=4,
            duration_ms=900,
            discovery_count=7,
            clock_skew_s=2,
        ),
        decision_line(
            **common(ts, reason="launched"),
            issue=5,
            state="launched",
            approver_id=1,
            approval_event_id=2,
            approved_at=ts,
            note="re-approved",
        ),
        warning_line(
            **common(ts, reason="discovery_count"), issue=5, discovery_count=99
        ),
    ]
    for item in built:
        assert not set(FORBIDDEN_KEYS) & set(item)


@pytest.mark.parametrize("reason", LINE_REASONS)
def test_every_reason_is_accepted_by_line__ac14_fr020_nfr006(reason, ts):
    built = warning_line(**common(ts, reason=reason))
    assert built["reason"] == reason


def test_line_rejects_wrong_value_types__ac14_fr020_nfr006(ts):
    with pytest.raises(ValueError):
        warning_line(**common(ts, reason="clock_skew", dry_run="no"))
    with pytest.raises(ValueError):
        cycle_line(
            **common(ts, reason="disabled"),
            exit_code=True,
            gh_calls=0,
            duration_ms=1,
        )
    with pytest.raises(ValueError):
        warning_line(**common(ts, reason="clock_skew", cycle_id=None))


def build_with(key: str, value: object, ts: str) -> dict:
    """Build the smallest valid line that carries ``key`` set to ``value``."""
    if key in {"ts", "host", "login", "cycle_id"}:
        fields = common(ts, reason="clock_skew")
        fields[key] = value
        return warning_line(**fields)
    if key in {"exit", "gh_calls", "duration_ms"}:
        args: dict = {"exit_code": 0, "gh_calls": 0, "duration_ms": 1}
        args["exit_code" if key == "exit" else key] = value
        return cycle_line(**common(ts, reason="disabled"), **args)
    if key == "discovery_count":
        return warning_line(
            **common(ts, reason="discovery_count"), discovery_count=value
        )
    fields = {"issue": 1}
    fields[key] = value
    return decision_line(**common(ts, reason="launched"), **fields)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("state", "Fix the login bug in prod"),
        ("state", ""),
        ("state", "Pending"),
        ("state", "done"),
        ("cycle_id", "short"),
        ("cycle_id", "C" * 32),
        ("cycle_id", "c" * 33),
        ("cycle_id", "c" * 31 + "\n"),
        ("cycle_id", "Fix the login bug in prod!!!!"),
        ("ts", "yesterday"),
        ("ts", "2026-13-45T25:61:61Z"),
        ("ts", "2026-11-07T12:00:00Z\n"),
        ("ts", "2026-11-07T12:00:00+00:00"),
        ("ts", ""),
        ("approved_at", "soon"),
        ("approved_at", "Title of an issue"),
        ("approved_at", "2026-11-07 12:00:00Z"),
        ("host", ""),
        ("host", "bo\nx"),
        ("host", "h" * 256),
        ("login", ""),
        ("login", "two words"),
        ("login", "a\tb"),
        ("login", "a\nb"),
        ("login", "x" * 101),
        ("issue", 0),
        ("issue", -5),
        ("issue", 10**9),
        ("approver_id", 0),
        ("approver_id", -1),
        ("approval_event_id", -7),
        ("exit", -1),
        ("exit", 256),
        ("gh_calls", -1),
        ("duration_ms", -5),
        ("discovery_count", -1),
    ],
)
def test_line_rejects_values_outside_the_key_shape__ac14_fr020_nfr006(key, value, ts):
    """Design 223, 701-718: a typed string is not enough; issue text must not fit."""
    with pytest.raises(ValueError, match="allowed shape"):
        build_with(key, value, ts)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        *[("state", s) for s in sorted(audit._ENTRY_STATES)],
        ("cycle_id", "0123456789abcdef" * 2),
        ("host", "hôst-☃"),
        ("login", "owner-login"),
        ("login", "bad_login!"),
        ("login", None),
        ("approved_at", None),
        ("approver_id", None),
        ("approval_event_id", None),
        ("issue", 1),
        ("issue", MAX_ISSUE_NUMBER),
        ("exit", 0),
        ("exit", 75),
        ("exit", 255),
        ("gh_calls", 0),
        ("duration_ms", 0),
        ("discovery_count", 0),
    ],
)
def test_line_accepts_values_inside_the_key_shape__ac14_fr020_nfr006(key, value, ts):
    assert build_with(key, value, ts)[key] == value


def test_host_and_login_take_any_printable_bounded_token__ac14_fr020_nfr006(ts):
    """Pins the documented limit: host and login are not closed to free text."""
    sentence = "Fix the login bug in prod, urgent"
    assert build_with("host", sentence, ts)["host"] == sentence
    assert build_with("host", "h" * 255, ts)["host"] == "h" * 255
    token = "Fix-the-login-bug-in-prod,urgent"
    assert build_with("login", token, ts)["login"] == token
    assert build_with("login", "x" * 100, ts)["login"] == "x" * 100
    # The docstring says so and does not claim a closed shape for every key.
    doc = " ".join(audit.__doc__.split())
    assert "``host`` and ``login``" in doc
    assert "any printable token" in doc
    assert "free text cannot be written" not in doc


def test_no_free_text_key_exists_on_any_line_kind__ac14_fr020_nfr006():
    """No key on any line kind can hold a title, body, label or stderr text."""
    allowed = set().union(*(req | opt for req, opt in audit._KEYS.values()))
    assert not set(FORBIDDEN_KEYS) & allowed
    assert allowed <= set(audit._TYPES)


def test_state_enum_is_the_design_state_set__fr020():
    """Design 422: the entry ``state`` values."""
    assert audit._ENTRY_STATES == {
        "pending",
        "launched",
        "unknown",
        "failed",
        "abandoned",
        "claimed",
    }


def test_issue_bound_matches_the_predicates_bound__fr020():
    assert audit._MAX_ISSUE == MAX_ISSUE_NUMBER


# ---------------------------------------------------------------------- writer


def test_append_sorted_keys_and_ascii__ac14_fr020_nfr006(tmp_path, ts):
    log = AuditLog(tmp_path)
    built = warning_line(**common(ts, host="hôst-☃", reason="clock_skew"))
    log.append(built)
    raw = (tmp_path / "audit.jsonl").read_bytes()
    text = raw.decode("ascii")  # raises if any byte is outside ASCII
    assert text.endswith("\n")
    assert text.count("\n") == 1
    assert "\\u00f4" in text
    parsed = json.loads(text)
    assert parsed == built
    assert list(json.loads(text, object_pairs_hook=lambda p: [k for k, _ in p])) == (
        sorted(built)
    )


def test_append_adds_one_line_per_call__ac14_fr020_nfr006(tmp_path, ts):
    log = AuditLog(tmp_path)
    for reason in ("clock_skew", "discovery_count"):
        log.append(warning_line(**common(ts, reason=reason)))
    lines = (tmp_path / "audit.jsonl").read_text().splitlines()
    assert [json.loads(item)["reason"] for item in lines] == [
        "clock_skew",
        "discovery_count",
    ]


def test_append_file_mode_is_0600__ac14_fr020_nfr006(tmp_path, ts):
    log = AuditLog(tmp_path)
    log.append(warning_line(**common(ts, reason="clock_skew")))
    mode = stat.S_IMODE(os.stat(tmp_path / "audit.jsonl").st_mode)
    assert mode == 0o600


def test_append_makes_one_os_write__ac14_fr020_nfr006(tmp_path, ts, monkeypatch):
    log = AuditLog(tmp_path)
    calls: list[tuple[int, bytes]] = []
    real_write = os.write

    def counting_write(fd, data):
        calls.append((fd, bytes(data)))
        return real_write(fd, data)

    built = cycle_line(
        **common(ts, reason="gh_timeout"), exit_code=3, gh_calls=1, duration_ms=5
    )
    monkeypatch.setattr(os, "write", counting_write)
    log.append(built)
    monkeypatch.undo()
    assert len(calls) == 1
    assert calls[0][1] == (tmp_path / "audit.jsonl").read_bytes()


# -------------------------------------------------------------------- rotation


def test_rotation_below_threshold_does_nothing__ac14_fr020_nfr006(tmp_path):
    current = tmp_path / "audit.jsonl"
    big_file(current, b"cur--", size=ROTATE_AT - 1)
    AuditLog(tmp_path).rotate_if_needed()
    assert names_in(tmp_path) == ["audit.jsonl"]
    assert current.stat().st_size == ROTATE_AT - 1


def test_rotation_without_current_file_does_nothing__ac14_fr020_nfr006(tmp_path):
    AuditLog(tmp_path).rotate_if_needed()
    assert names_in(tmp_path) == []


def test_rotation_shifts_every_file_at_5_mib__ac14_fr020_nfr006(tmp_path):
    base = tmp_path / "audit.jsonl"
    big_file(base, b"cur--")
    (tmp_path / "audit.jsonl.1").write_bytes(b"one--")
    (tmp_path / "audit.jsonl.2").write_bytes(b"two--")
    (tmp_path / "audit.jsonl.3").write_bytes(b"three")
    (tmp_path / "audit.jsonl.4").write_bytes(b"four-")
    AuditLog(tmp_path).rotate_if_needed()
    assert names_in(tmp_path) == [
        "audit.jsonl.1",
        "audit.jsonl.2",
        "audit.jsonl.3",
        "audit.jsonl.4",
    ]
    assert head(tmp_path / "audit.jsonl.1") == b"cur--"
    assert (tmp_path / "audit.jsonl.1").stat().st_size == ROTATE_AT
    assert head(tmp_path / "audit.jsonl.2") == b"one--"
    assert head(tmp_path / "audit.jsonl.3") == b"two--"
    assert head(tmp_path / "audit.jsonl.4") == b"three"


def test_rotation_keeps_exactly_four_rotated_files__ac14_fr020_nfr006(tmp_path):
    log = AuditLog(tmp_path)
    for generation in range(6):
        big_file(tmp_path / "audit.jsonl", f"gen{generation}".encode())
        log.rotate_if_needed()
    assert names_in(tmp_path) == [
        "audit.jsonl.1",
        "audit.jsonl.2",
        "audit.jsonl.3",
        "audit.jsonl.4",
    ]
    assert head(tmp_path / "audit.jsonl.1", 4) == b"gen5"
    assert head(tmp_path / "audit.jsonl.4", 4) == b"gen2"


def test_rotation_partial_state_only_current__ac14_fr020_nfr006(tmp_path):
    big_file(tmp_path / "audit.jsonl", b"cur--")
    AuditLog(tmp_path).rotate_if_needed()
    assert names_in(tmp_path) == ["audit.jsonl.1"]
    assert head(tmp_path / "audit.jsonl.1") == b"cur--"


def test_rotation_partial_state_current_and_dot_1__ac14_fr020_nfr006(tmp_path):
    big_file(tmp_path / "audit.jsonl", b"cur--")
    (tmp_path / "audit.jsonl.1").write_bytes(b"one--")
    AuditLog(tmp_path).rotate_if_needed()
    assert names_in(tmp_path) == ["audit.jsonl.1", "audit.jsonl.2"]
    assert not (tmp_path / "audit.jsonl.3").exists()
    assert head(tmp_path / "audit.jsonl.1") == b"cur--"
    assert head(tmp_path / "audit.jsonl.2") == b"one--"


def record_os_calls(monkeypatch, state_dir) -> list[tuple]:
    """Wrap ``os.replace`` and ``os.fsync``; each fsync notes if its fd is the dir."""
    events: list[tuple] = []
    real_replace = os.replace
    real_fsync = os.fsync

    def replace(src, dst):
        real_replace(src, dst)  # a missing source raises before it is recorded
        events.append(("replace", os.path.basename(src), os.path.basename(dst)))

    def fsync(fd):
        info = os.fstat(fd)
        is_state_dir = stat.S_ISDIR(info.st_mode) and os.path.samestat(
            info, os.stat(state_dir)
        )
        events.append(("fsync", is_state_dir))
        return real_fsync(fd)

    monkeypatch.setattr(os, "replace", replace)
    monkeypatch.setattr(os, "fsync", fsync)
    return events


def test_rotation_fsyncs_the_state_dir_once_after_the_last_replace__df30(
    tmp_path, monkeypatch
):
    big_file(tmp_path / "audit.jsonl", b"cur--")
    (tmp_path / "audit.jsonl.1").write_bytes(b"one--")
    log = AuditLog(tmp_path)
    events = record_os_calls(monkeypatch, tmp_path)
    log.rotate_if_needed()
    monkeypatch.undo()
    assert events == [
        ("replace", "audit.jsonl.1", "audit.jsonl.2"),
        ("replace", "audit.jsonl", "audit.jsonl.1"),
        ("fsync", True),
    ]


@pytest.mark.parametrize("size", [None, ROTATE_AT - 1], ids=["no-file", "below"])
def test_no_rotation_means_no_fsync__df30(tmp_path, monkeypatch, size):
    if size is not None:
        big_file(tmp_path / "audit.jsonl", b"cur--", size=size)
    log = AuditLog(tmp_path)
    events = record_os_calls(monkeypatch, tmp_path)
    log.rotate_if_needed()
    monkeypatch.undo()
    assert events == []


def test_exit_75_path_appends_without_rotating__ac14_fr020_nfr006(tmp_path, ts):
    current = tmp_path / "audit.jsonl"
    big_file(current, b"cur--", size=ROTATE_AT + 10)
    log = AuditLog(tmp_path)
    log.append(warning_line(**common(ts, reason="lock_held")))
    assert names_in(tmp_path) == ["audit.jsonl"]
    assert current.stat().st_size > ROTATE_AT + 10


# --------------------------------------------------------------- stderr fallback


def test_stderr_fallback_emits_only_five_keys__ac14_fr020_nfr006(capsys, ts):
    stderr_fallback("state_dir_unwritable", 6, ts=ts, host="box1")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.count("\n") == 1
    assert json.loads(captured.err) == {
        "kind": "cycle",
        "ts": ts,
        "host": "box1",
        "exit": 6,
        "reason": "state_dir_unwritable",
    }


def test_stderr_fallback_defaults_keep_the_key_set__ac14_fr020_nfr006(
    capsys, monkeypatch
):
    monkeypatch.setattr(audit.socket, "gethostname", lambda: "defaulthost")
    stderr_fallback("config_invalid", 2)
    parsed = json.loads(capsys.readouterr().err)
    assert sorted(parsed) == ["exit", "host", "kind", "reason", "ts"]
    assert parsed["host"] == "defaulthost"
    assert parsed["exit"] == 2
    assert parsed["reason"] == "config_invalid"
    assert isinstance(parsed["ts"], str)


@pytest.mark.parametrize(
    "bad",
    [
        {"ts": "yesterday"},
        {"ts": "2026-11-07T12:00:00Z\n"},
        {"host": ""},
        {"host": "a\nb"},
        {"exit_code": 256},
        {"exit_code": -1},
        {"exit_code": "3"},
        {"exit_code": True},
        {"exit_code": None},
    ],
    ids=lambda b: next(iter(b)) + "=" + repr(next(iter(b.values()))),
)
def test_stderr_fallback_rejects_bad_values_and_writes_nothing__nfr006(capsys, ts, bad):
    args = {"exit_code": 6, "ts": ts, "host": "box1", **bad}
    exit_code = args.pop("exit_code")
    with pytest.raises(ValueError):
        stderr_fallback("state_dir_unwritable", exit_code, **args)
    assert capsys.readouterr().err == ""


def test_stderr_fallback_unknown_reason_raises__ac14_fr020_nfr006(capsys, ts):
    with pytest.raises(ValueError):
        stderr_fallback("typo_reason", 2, ts=ts, host="box1")
    assert capsys.readouterr().err == ""


# ---------------------------------------------------------------- line examples


def test_cycle_line_example__ac14_fr020_nfr006(ts):
    built = cycle_line(
        **common(ts, reason="rate_limited"),
        exit_code=5,
        gh_calls=3,
        duration_ms=1200,
    )
    assert built == {
        "kind": "cycle",
        "ts": ts,
        "host": "box1",
        "login": "octo",
        "cycle_id": "c" * 32,
        "dry_run": False,
        "exit": 5,
        "reason": "rate_limited",
        "gh_calls": 3,
        "duration_ms": 1200,
    }


def test_cycle_line_optional_keys_and_null_login__ac14_fr020_nfr006(ts):
    built = cycle_line(
        **common(ts, reason="clock_skew", login=None),
        exit_code=0,
        gh_calls=1,
        duration_ms=10,
        discovery_count=12,
        clock_skew_s=90,
    )
    assert built["login"] is None
    assert built["discovery_count"] == 12
    assert built["clock_skew_s"] == 90


def test_decision_line_skip_example_has_null_approval__ac14_fr020_nfr006(ts):
    built = decision_line(**common(ts, reason="not_approved"), issue=41)
    assert built["issue"] == 41
    assert "state" not in built
    assert "note" not in built
    for key in ("approver_id", "approval_event_id", "approved_at"):
        assert built[key] is None


def test_decision_line_entry_example_has_state__ac14_fr020_nfr006(ts):
    built = decision_line(
        **common(ts, reason="launched"),
        issue=42,
        state="launched",
        approver_id=1001,
        approval_event_id=2002,
        approved_at=ts,
    )
    assert built["state"] == "launched"
    assert built["approver_id"] == 1001
    assert built["approval_event_id"] == 2002
    assert built["approved_at"] == ts
    assert "note" not in built


def test_decision_line_re_approved_note__ac14_fr020_nfr006(ts):
    built = decision_line(
        **common(ts, reason="already_dispatched"),
        issue=43,
        approver_id=1,
        approval_event_id=2,
        approved_at=ts,
        note="re-approved",
    )
    assert built["note"] == "re-approved"
    with pytest.raises(ValueError):
        decision_line(**common(ts, reason="already_dispatched"), issue=43, note="other")


def test_decision_line_operator_reset__ac17_fr026(ts):
    built = decision_line(**common(ts, reason="operator_reset", login=None), issue=7)
    assert built["kind"] == "decision"
    assert built["reason"] == "operator_reset"
    assert built["issue"] == 7
    assert built["login"] is None
    assert "state" not in built
    assert "note" not in built
    assert built["approver_id"] is None
    assert built["approval_event_id"] is None
    assert built["approved_at"] is None


def test_warning_line_discovery_count_example__ac14_fr020_nfr006(ts):
    built = warning_line(**common(ts, reason="discovery_count"), discovery_count=95)
    assert built["kind"] == "warning"
    assert built["discovery_count"] == 95
    assert "issue" not in built


def test_warning_line_clock_skew_example__ac14_fr020_nfr006(ts):
    built = warning_line(**common(ts, reason="clock_skew"), clock_skew_s=120)
    assert built["clock_skew_s"] == 120


def test_warning_line_operator_reset_without_issue__ac17_fr026(ts):
    built = warning_line(**common(ts, reason="operator_reset", login=None))
    assert built["kind"] == "warning"
    assert built["reason"] == "operator_reset"
    assert "issue" not in built


def test_warning_line_reset_refused__ac17_fr026(ts):
    built = warning_line(**common(ts, reason="reset_refused"), issue=9)
    assert built["reason"] == "reset_refused"
    assert built["issue"] == 9
    assert REASON_TABLE["reset_refused"] == ("warning", 2)


def test_warning_line_dry_run_shadow_reset__ac13_fr019(ts):
    built = warning_line(**common(ts, reason="dry_run_shadow_reset", dry_run=True))
    assert built["reason"] == "dry_run_shadow_reset"
    assert built["dry_run"] is True
