"""Tests for the pure classifier of ``superclaude sweep`` (DESIGN section 11, ``test_classify.py`` row).

Covers FR-006 to FR-010, FR-012 to FR-015, NFR-004, NFR-010, D9, WC-13, M6 and M9, the
R3-B1 window fixtures, the R3-B2 several-rows fixtures, the R3-B3 FR-010 fixtures, and the
import boundaries of DESIGN section 4 (lines 210, 211, 212 and 219).

``SweepInput`` and ``SweepContext`` objects are built directly from ``models``; no test here
starts a process (the autouse guard in ``conftest.py`` enforces that). Class names and note
strings are written out as literals taken from DESIGN, so a changed constant in
``classify.py`` fails here instead of passing silently.
"""

from __future__ import annotations

import ast
import builtins
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from superclaude.cli.sweep import classify as classify_module
from superclaude.cli.sweep import probes
from superclaude.cli.sweep import report as report_module
from superclaude.cli.sweep.classify import (
    RULES,
    classify,
    classify_all,
    mark_shared_packages,
    package_state,
    policy_of,
    removable,
    safe_to_close,
)
from superclaude.cli.sweep.models import (
    CLASSES,
    PACKAGE_STATES,
    SAFE_VALUES,
    ContractRecord,
    OrcaObservation,
    PackageRecord,
    SessionRow,
    SourceCoverage,
    SweepContext,
    SweepInput,
    TabMapEntry,
    TranscriptTail,
    WorktreeState,
)

REPO = Path(__file__).resolve().parents[2]
SWEEP_DIR = REPO / "src" / "superclaude" / "cli" / "sweep"
SWEEP_PKG = "superclaude.cli.sweep"

# --- Class names (DESIGN section 7.2, models.CLASSES) -------------------------------------
WAITING = "waiting on a person"
STALLED = "stalled (proved)"
FENCED = "fenced"
WORKING = "working"
FINISHED = "finished"
IDLE = "idle"
PERSON_ACTIVE = "person session (active)"
UNKNOWN = "could not determine"

# --- Notes, byte-exact from DESIGN sections 7.2 and 12 ------------------------------------
N_WINDOW = "Dispatch time window not observable"
N_SEVERAL = "conflict: one pane session matches several Dispatch rows"
N_MOVED = "pane moved to a later session"
N_BEFORE = "session started before this Dispatch window"
N_TAIL = "session start not observable: transcript tail only"
N_JOINED = "joined by pane: latest session of the pane"
N_JOIN_NOT_OBSERVABLE = "tab map join not observable"
N_NOT_SCOPED = "Orca pane session, not in scoped Runs"
N_EARLIER = "earlier pane session not joinable (tab map keeps only the latest session)"
N_ORIGIN_NOT_PROVED = (
    "origin not proved: no tab-map entry; may be a worker of a Run outside the scope"
)
N_SP16 = "could not join Orca workers to transcripts (tab map empty or stale)"
N_O_UNAVAILABLE = "origin unknown: Orca unavailable"
N_O_TRUNCATED = "origin unknown: worker list truncated"
N_O_CALL_FAILED = "origin unknown: worker list call failed"
N_O_RUN = "origin unknown: Run not confirmed"
N_O_TABS = "origin unknown: tab map unreadable"
N_DUPLICATE = "conflict: duplicate Dispatch rows disagree"
N_WC13 = "WC-13 violation, review"
N_ASK = "blocked contract under ask the coordinator; may be re-running"
N_NOT_OBSERVED = "blocked contract; Orca state not observed"
N_EXITED = "Orca: exited; fenced evidence not readable"
N_FUTURE = "timestamp in the future"
N_TRANSCRIPT = "unscanned: transcript not readable"
N_CONTRACT = "unscanned: contract not readable"
N_PARTIAL = "partial: usable not yet judged"
N_NO_CONTRACT = "no contract read for this row; finished needs a parsed contract"

UTC = timezone.utc
HOUR = timedelta(hours=1)
MINUTE = timedelta(minutes=1)
PANE = "tab1+leaf1"  # a tab-map file name (pane key with ":" written as "+")
HANDLE = "term-1"  # the third line of the same tab-map file


def at(hour: int, minute: int = 0, second: int = 0, micro: int = 0) -> datetime:
    """A clock time on 2026-11-08, aware UTC (the day of ``fixed_now``)."""
    return datetime(2026, 11, 8, hour, minute, second, micro, tzinfo=UTC)


@pytest.fixture
def now(fixed_now) -> datetime:
    assert fixed_now == at(
        12
    )  # the R3 fixtures are written as clock times around 12:00
    return fixed_now


@pytest.fixture
def path_a(monkeypatch):
    """The join path of the shared FR-010 Given: ``session_join`` is the Claude session id."""
    monkeypatch.setattr(classify_module, "JOIN_PATH", "A")


@pytest.fixture
def path_b(monkeypatch):
    """The join path in force (step 1.0a items 1 and 22): the tab-map pane or handle."""
    monkeypatch.setattr(classify_module, "JOIN_PATH", "B")


# --- Builders -----------------------------------------------------------------------------


def make_ctx(
    now: datetime, window: timedelta = 6 * HOUR, runs: tuple[str, ...] = ("R1",)
) -> SweepContext:
    return SweepContext(
        now=now,
        window=window,
        window_start=now - window,
        root=Path("/sweep-root"),
        runs=runs,
    )


def orca(dispatch: str = "D1", **kw) -> OrcaObservation:
    kw.setdefault("run", "R1")
    return OrcaObservation(dispatch=dispatch, **kw)


def contract(
    worker_status: str | None,
    path: str = "/sweep-root/.dev/reports/run/return-contract.yaml",
    **kw,
) -> ContractRecord:
    return ContractRecord(path=Path(path), worker_status=worker_status, **kw)


def row(**kw) -> SessionRow:
    base = dict(
        id="x",
        person_started=None,
        orca=None,
        contract=None,
        transcript_path=None,
        transcript_readable=None,
        last_activity=None,
        gate_policy=None,
        row_id="orca:D1",
    )
    base.update(kw)
    return SessionRow(**base)


def tail(
    sid: str | None,
    last: datetime | None,
    first: datetime | None = None,
    *,
    complete: bool = True,
    readable: bool = True,
    mtime: datetime | None = None,
) -> TranscriptTail:
    name = sid or "unnamed"
    return TranscriptTail(
        path=Path(f"/home/u/.claude/projects/key/{name}.jsonl"),
        session_id=sid,
        readable=readable,
        last_record_ts=last,
        first_record_ts=first if first is not None else last,
        tail_complete=complete,
        mtime=mtime if mtime is not None else (last or at(12)),
        project_key="key",
    )


def entry(sid: str, pane: str = PANE, handle: str = HANDLE) -> TabMapEntry:
    return TabMapEntry(
        file_name=pane, session_id=sid, launch_dir="/sweep-root", terminal_handle=handle
    )


def src(name: str, unscanned: str | None = None) -> SourceCoverage:
    return SourceCoverage(name, "unscanned" if unscanned else "read", None, unscanned)


def ok_sources(*runs: str) -> tuple[SourceCoverage, ...]:
    return tuple(src(f"orca worker-list {r}") for r in runs) + (
        src("ccsession orca-tabs"),
    )


def sweep_input(
    now: datetime,
    *,
    orca_rows=(),
    transcripts=(),
    tab_map=(),
    contracts=(),
    worktrees=(),
    sources=None,
    available: bool = True,
    truncated: bool = False,
) -> SweepInput:
    return SweepInput(
        orca_rows=tuple(orca_rows),
        contracts=tuple(contracts),
        transcripts=tuple(transcripts),
        tab_map=tuple(tab_map),
        worktrees=tuple(worktrees),
        sources=ok_sources("R1") if sources is None else tuple(sources),
        orca_available=available,
        orca_binary="orca-ide",
        orca_version=None,
        truncated=truncated,
        collected_start=now,
        collected_end=now,
    )


def run(inp: SweepInput, ctx: SweepContext):
    """``classify_all`` plus the invariants every fixture must keep (FR-012, FR-006)."""
    result = classify_all(inp, ctx)
    ids = [c.row.row_id for c in result.rows]
    assert len(ids) == len(set(ids))
    for c in result.rows:
        assert c.classification.class_name in CLASSES
        assert c.safe.terminal in SAFE_VALUES
        assert c.safe.worktree != "yes"  # FR-012 over every fixture in this file
    for w in result.worktrees:
        assert w.removable != "yes"
    return result


def by_id(result) -> dict:
    return {c.row.row_id: c for c in result.rows}


def notes_of(result, row_id: str) -> tuple[str, ...]:
    return by_id(result)[row_id].classification.notes


def assert_unknown(c, *notes: str) -> None:
    """The row is could not determine through the fallback rule and carries ``notes``."""
    assert c.classification.class_name == UNKNOWN
    assert c.classification.rule == "fallback"
    for note in notes:
        assert note in c.classification.notes


def assert_no_sp16(result) -> None:
    assert all(N_SP16 not in c.classification.notes for c in result.rows)


# ===========================================================================================
# Rules 1 to 9 (FR-006, NFR-010)
# ===========================================================================================


def _rule_cases(now: datetime) -> dict[str, tuple[SessionRow, str, str | None]]:
    # Rule 5 (working) cannot match while the live agentWait, `live` and `in_progress`
    # names are uncaptured (DESIGN open item 6): its case holds all four conditions and
    # is expected to fall to the fallback rule.
    live_unwaiting = orca(
        liveness_verdict="live",
        status="in_progress",
        agent_wait_present=True,
        agent_wait=None,
    )
    return {
        "blocked_contract": (
            row(
                orca=orca(outcome="failed"),
                contract=contract("blocked", reason="needs a person"),
            ),
            WAITING,
            "a",
        ),
        "orca_exit_proof": (
            row(
                orca=orca(
                    liveness_verdict="exited",
                    worker_done_seen=False,
                    fenced_evidence="absent",
                ),
                transcript_readable=True,
            ),
            STALLED,
            None,
        ),
        "fenced": (row(orca=orca(fenced_evidence="present")), FENCED, None),
        "waiting_signal": (
            row(
                orca=orca(
                    agent_wait={"since": "2026-11-08T10:00:00Z"},
                    agent_wait_present=True,
                    agent_wait_since=at(10),
                )
            ),
            WAITING,
            "a",
        ),
        "working": (row(orca=live_unwaiting), UNKNOWN, None),
        "finished": (
            row(
                orca=orca(outcome="succeeded"),
                contract=contract("succeeded"),
            ),
            FINISHED,
            None,
        ),
        "idle": (
            row(
                person_started=True,
                transcript_readable=True,
                last_activity=now - 7 * HOUR,
            ),
            IDLE,
            None,
        ),
        "person_active": (
            row(
                person_started=True,
                transcript_readable=True,
                last_activity=now - HOUR,
            ),
            PERSON_ACTIVE,
            None,
        ),
        "fallback": (row(), UNKNOWN, None),
    }


RULE_NAMES = [
    "blocked_contract",
    "orca_exit_proof",
    "fenced",
    "waiting_signal",
    "working",
    "finished",
    "idle",
    "person_active",
    "fallback",
]


@pytest.mark.parametrize("rule", RULE_NAMES)
def test_rule_case_per_rule_1_to_9(now, rule):
    case_row, class_name, kind = _rule_cases(now)[rule]
    cls = classify(case_row, make_ctx(now))
    matched = "fallback" if rule == "working" else rule  # rule 5 cannot match (item 6)
    assert (cls.rule, cls.class_name, cls.waiting_kind) == (matched, class_name, kind)


def test_every_class_name_but_working_is_reached(now):
    reached = {
        classify(r, make_ctx(now)).class_name for r, _, _ in _rule_cases(now).values()
    }
    assert reached == set(CLASSES) - {WORKING}  # no row is working in Phase 1


def test_rules_order_pin():
    assert [r.name for r in RULES] == RULE_NAMES  # NFR-010


def test_rule_4_waiting_age_and_future_timestamp(now):
    waiting = orca(agent_wait={"since": "x"}, agent_wait_since=at(10))
    cls = classify(row(orca=waiting), make_ctx(now))
    assert "waiting since 2026-11-08T10:00:00+00:00" in cls.evidence
    future = orca(agent_wait={"since": "x"}, agent_wait_since=now + HOUR)
    cls = classify(row(orca=future), make_ctx(now))
    assert (cls.class_name, cls.waiting_kind, cls.notes) == (WAITING, "a", (N_FUTURE,))
    assert "waiting since" not in cls.evidence  # unknown age


@pytest.mark.parametrize(
    "case_row",
    [
        pytest.param(
            row(
                orca=orca(status="in_progress"),
                contract=contract("failed", reason="E-QA-FAIL stop"),
            ),
            id="frozen-plan",
        ),
        pytest.param(row(orca=orca(status="ready")), id="ready-task"),
    ],
)
def test_rule_4_waiting_b(now, case_row):
    cls = classify(case_row, make_ctx(now))
    assert (cls.rule, cls.class_name, cls.waiting_kind) == (
        "waiting_signal",
        WAITING,
        "b",
    )


def test_resume_needed_alone_is_not_a_frozen_plan(now):
    failed = row(contract=contract("failed", reason="E-RESUME-NEEDED"))
    assert classify(failed, make_ctx(now)).class_name == UNKNOWN
    assert policy_of(failed) is None


@pytest.mark.parametrize(
    "case_row, expected",
    [
        (row(contract=contract("failed", reason="E-QA-FAIL")), "frozen"),
        (row(contract=contract("blocked", reason="E-QA-FAIL")), "frozen"),
        (row(contract=contract("blocked", command="/sc:implement x")), "frozen"),
        (row(contract=contract("blocked", reason="a question")), None),
        (row(contract=contract("succeeded")), None),
        (row(), None),
    ],
)
def test_policy_of_is_independent_of_the_class(case_row, expected):
    assert policy_of(case_row) == expected


def test_rule_5_never_matches_while_the_agent_wait_names_are_uncaptured(now):
    full = dict(
        liveness_verdict="live",
        status="in_progress",
        agent_wait_present=True,
        agent_wait=None,
    )
    ctx = make_ctx(now)
    # All four conditions of DESIGN 7.2 hold, and the row still falls to the fallback.
    cls = classify(row(orca=orca(**full)), ctx)
    assert (cls.rule, cls.class_name) == ("fallback", UNKNOWN)  # open item 6
    for broken in (
        {"liveness_verdict": "unverifiable"},
        {"status": "pending"},
        {"agent_wait_present": False},
        {"agent_wait": {"since": "x"}},  # a non-null wait is rule 4, not working
    ):
        cls = classify(row(orca=orca(**{**full, **broken})), ctx)
        assert cls.class_name != WORKING, broken


# ===========================================================================================
# Window, last_activity source, future timestamps, FR-007 and SP-26
# ===========================================================================================


@pytest.mark.parametrize(
    "window_hours, rule",
    [(4, "idle"), (5, "person_active"), (6, "person_active")],
)
def test_5h_old_row_is_idle_only_when_window_is_under_5h(now, window_hours, rule):
    five_hours = row(
        person_started=True, transcript_readable=True, last_activity=now - 5 * HOUR
    )
    ctx = make_ctx(now, timedelta(hours=window_hours))
    assert classify(five_hours, ctx).rule == rule


def test_record_timestamp_older_than_mtime_is_used_and_named(now):
    inp = sweep_input(
        now, transcripts=(tail("sess-T", now - 5 * HOUR, mtime=now - HOUR),)
    )
    result = run(inp, make_ctx(now, 4 * HOUR))
    c = by_id(result)["transcript:sess-T"]
    assert c.classification.class_name == IDLE
    assert "last_activity from last_record_ts of the last complete record" in (
        c.classification.evidence
    )
    assert c.row.last_activity == now - 5 * HOUR


def test_mtime_is_the_source_when_no_record_carries_a_time(now):
    inp = sweep_input(now, transcripts=(tail("sess-T", None, mtime=now - 5 * HOUR),))
    c = by_id(run(inp, make_ctx(now, 4 * HOUR)))["transcript:sess-T"]
    assert c.classification.class_name == IDLE
    assert "last_activity from transcript st_mtime" in c.classification.evidence


def test_future_timestamp_is_unknown_age_and_never_idle(now):
    future = row(
        person_started=True, transcript_readable=True, last_activity=now + 2 * HOUR
    )
    cls = classify(future, make_ctx(now, MINUTE))  # a window so short idle would fit
    assert cls.class_name != IDLE
    assert N_FUTURE in cls.notes


def test_future_transcript_gets_no_age(now):
    inp = sweep_input(now, transcripts=(tail("sess-T", now + 2 * HOUR),))
    c = by_id(run(inp, make_ctx(now)))["transcript:sess-T"]
    assert c.row.freshness == "unknown"
    assert c.row.freshness_age_s is None
    assert c.classification.class_name != IDLE
    assert N_FUTURE in c.classification.notes


# ===========================================================================================
# FR-008, FR-009, rule 1 notes (M6)
# ===========================================================================================


@pytest.mark.parametrize(
    "observed",
    [
        pytest.param(
            orca(
                liveness_verdict="unverifiable",
                status="in_progress",
                agent_wait_present=True,
            ),
            id="unverifiable",
        ),
        pytest.param(
            orca(
                liveness_verdict="live",
                status="in_progress",
                agent_wait_present=False,
            ),
            id="late-heartbeat",
        ),
        pytest.param(
            orca(liveness_verdict=None, status="in_progress", agent_wait_present=True),
            id="stale-liveStatus",
        ),
        pytest.param(orca(), id="missing-worker-show-row"),
    ],
)
def test_fr008_four_inputs_are_could_not_determine_never_stalled(now, observed):
    cls = classify(row(orca=observed, transcript_readable=True), make_ctx(now))
    assert (cls.class_name, cls.rule) == (UNKNOWN, "fallback")
    assert cls.class_name != STALLED


def test_fr009_exited_row_without_proof_is_not_stalled(now):
    exited = orca(
        liveness_verdict="exited", worker_done_seen=None, fenced_evidence="absent"
    )
    cls = classify(row(orca=exited, transcript_readable=True), make_ctx(now))
    assert cls.class_name == UNKNOWN


def test_rule_2_stalled_holds_when_no_transcript_was_joined(now):
    # TST-F6: an Orca row with no joined transcript has ``transcript_readable=None``
    # (``classify_all`` sets it so). Only an unreadable transcript (False) blocks rule 2.
    proof = orca(
        liveness_verdict="exited", worker_done_seen=False, fenced_evidence="absent"
    )

    cls = classify(row(orca=proof, transcript_readable=None), make_ctx(now))

    assert (cls.rule, cls.class_name) == ("orca_exit_proof", STALLED)
    unreadable = classify(row(orca=proof, transcript_readable=False), make_ctx(now))
    assert (unreadable.rule, unreadable.class_name) == ("fallback", UNKNOWN)


def test_rule_2_stalled_through_classify_all_for_an_orca_row_with_no_transcript(now):
    proof = orca(
        "D1",
        liveness_verdict="exited",
        worker_done_seen=False,
        fenced_evidence="absent",
    )

    result = run(sweep_input(now, orca_rows=(proof,)), make_ctx(now))

    only = by_id(result)["orca:D1"]
    assert only.row.transcript_readable is None  # no transcript joined to this row
    assert (only.classification.rule, only.classification.class_name) == (
        "orca_exit_proof",
        STALLED,
    )


def test_fr009_case_1_guard_refused_body_is_finished_with_the_note(now):
    exited = orca(
        liveness_verdict="exited",
        fenced_evidence="unreadable",
        body_text="guard refused: no admitted contract\nmore text",
    )
    cls = classify(row(orca=exited, transcript_readable=True), make_ctx(now))
    assert (cls.class_name, cls.rule) == (FINISHED, "finished")
    assert cls.notes == (N_EXITED,)


def test_fr009_case_2_exited_unreadable_and_nothing_else_is_fallback(now):
    exited = orca(liveness_verdict="exited", fenced_evidence="unreadable")
    cls = classify(row(orca=exited, transcript_readable=True), make_ctx(now))
    assert (cls.class_name, cls.rule) == (UNKNOWN, "fallback")
    assert cls.notes == (N_EXITED,)


def test_settled_orca_row_without_a_contract_names_the_missing_contract(now):
    # FIN-F4: the five live Orca rows were exited, succeeded and completed, yet could not
    # be `finished` because no contract was read; the row now says so.
    settled = orca(liveness_verdict="exited", status="completed", outcome="succeeded")
    cls = classify(row(orca=settled), make_ctx(now))
    assert (cls.class_name, cls.rule) == (UNKNOWN, "fallback")
    assert N_NO_CONTRACT in cls.notes
    for outcome in ("partial", "failed"):
        again = classify(row(orca=orca(outcome=outcome)), make_ctx(now))
        assert N_NO_CONTRACT in again.notes, outcome


@pytest.mark.parametrize(
    "case_row",
    [
        pytest.param(row(orca=orca(outcome=None)), id="not-settled"),
        pytest.param(row(), id="no-orca-row"),
        pytest.param(
            row(orca=orca(outcome="succeeded"), contract=contract("running")),
            id="contract-not-settled",
        ),
        pytest.param(
            row(orca=orca(outcome="succeeded"), contract=contract("succeeded")),
            id="finished",
        ),
    ],
)
def test_no_contract_note_is_only_for_a_settled_row_with_no_contract(now, case_row):
    assert N_NO_CONTRACT not in classify(case_row, make_ctx(now)).notes


def _live(**kw) -> OrcaObservation:
    base = dict(
        liveness_verdict="live",
        status="in_progress",
        agent_wait_present=True,
        agent_wait=None,
    )
    return orca(**{**base, **kw})


def test_rule1_ask_the_coordinator_declines_with_the_note(now):
    blocked = row(
        orca=_live(),
        contract=contract("blocked", reason="a question"),
        gate_policy="ask the coordinator",
    )
    cls = classify(blocked, make_ctx(now))
    assert cls.class_name != WAITING
    assert N_ASK in cls.notes


def test_rule1_gate_policy_none_declines_and_a_wait_reaches_rule_4(now):
    waiting_orca = _live(agent_wait={"since": "x"}, agent_wait_since=at(10))
    blocked = row(
        orca=waiting_orca, contract=contract("blocked", reason="q"), gate_policy=None
    )
    cls = classify(blocked, make_ctx(now))
    assert (cls.rule, cls.class_name, cls.waiting_kind) == (
        "waiting_signal",
        WAITING,
        "a",
    )
    assert N_ASK in cls.notes
    declined = classify(row(orca=_live(), contract=blocked.contract), make_ctx(now))
    assert declined.class_name != WAITING and N_ASK in declined.notes


def test_rule1_without_orca_row_declines_unless_ruling_halt(now):
    plain = classify(row(contract=contract("blocked", reason="q")), make_ctx(now))
    assert (plain.class_name, plain.notes) == (UNKNOWN, (N_NOT_OBSERVED,))
    halted = classify(
        row(contract=contract("blocked", reason="E-HALT-QA raised")), make_ctx(now)
    )
    assert (halted.rule, halted.class_name, halted.waiting_kind) == (
        "blocked_contract",
        WAITING,
        "a",
    )
    assert "Ruling halt E-HALT-QA; no Orca row" in halted.evidence


@pytest.mark.parametrize(
    "observed, policy, reason, why",
    [
        pytest.param(
            orca(outcome="succeeded"), None, "q", "Orca row settled", id="settled"
        ),
        pytest.param(
            _live(),
            "report blocked",
            "q",
            "gate_policy is report blocked",
            id="report-blocked",
        ),
        pytest.param(
            _live(),
            "ask the coordinator",
            "E-NO-RULING",
            "Ruling halt E-NO-RULING",
            id="ruling-halt",
        ),
    ],
)
def test_rule1_matches(now, observed, policy, reason, why):
    blocked = row(
        orca=observed, contract=contract("blocked", reason=reason), gate_policy=policy
    )
    cls = classify(blocked, make_ctx(now))
    assert (cls.rule, cls.class_name, cls.waiting_kind) == (
        "blocked_contract",
        WAITING,
        "a",
    )
    assert why in cls.evidence


def test_rule1_and_2_decline_when_the_transcript_is_unreadable(now):
    exited = orca(
        liveness_verdict="exited",
        worker_done_seen=False,
        fenced_evidence="absent",
        outcome="failed",
    )
    case = row(
        orca=exited,
        contract=contract("blocked", reason="q"),
        transcript_readable=False,
    )
    cls = classify(case, make_ctx(now))
    assert (cls.class_name, cls.rule) == (UNKNOWN, "fallback")
    assert N_TRANSCRIPT in cls.notes


# ===========================================================================================
# Rule 6 wording and SP-07, FINAL: reading, WC-13, unreadable inputs (SPEC section 11)
# ===========================================================================================


def test_sp07_guard_refused_on_a_later_line_is_not_finished(now):
    later = orca(body_text="working on it\nguard refused: quoted from a log")
    cls = classify(row(orca=later), make_ctx(now))
    assert cls.class_name != FINISHED


def test_rule6_finished_never_says_admitted_or_accepted(now):
    for outcome, worker in (("succeeded", "succeeded"), ("failed", "failed")):
        case = row(orca=orca(outcome=outcome), contract=contract(worker))
        cls = classify(case, make_ctx(now))
        if cls.class_name == FINISHED:
            text = " ".join((cls.evidence, *cls.notes, cls.class_name, cls.rule))
            assert "admitted" not in text and "accepted" not in text
    guard = classify(row(orca=orca(body_text="guard refused: x")), make_ctx(now))
    assert guard.class_name == FINISHED
    assert "admitted" not in guard.evidence and "accepted" not in guard.evidence


def test_rule6_partial_carries_its_note(now):
    case = row(orca=orca(outcome="partial"), contract=contract("partial"))
    cls = classify(case, make_ctx(now))
    assert (cls.class_name, cls.notes) == (FINISHED, (N_PARTIAL,))


def test_wc13_parent_adds_the_note_and_keeps_the_class(now):
    with_parent = row(
        orca=orca(parent="D0", agent_wait={"since": "x"}), transcript_readable=True
    )
    without = row(orca=orca(agent_wait={"since": "x"}), transcript_readable=True)
    cls, plain = classify(with_parent, make_ctx(now)), classify(without, make_ctx(now))
    assert N_WC13 in cls.notes and N_WC13 not in plain.notes
    assert cls.class_name == plain.class_name == WAITING


def test_unreadable_transcript_row_is_could_not_determine(now):
    case = row(
        person_started=True,
        transcript_readable=False,
        last_activity=now - 7 * HOUR,
    )
    cls = classify(case, make_ctx(now))
    assert (cls.class_name, cls.rule) == (UNKNOWN, "fallback")
    assert N_TRANSCRIPT in cls.notes


def _write_transcript(sweep_root, now, raw: bytes, name: str = "session-0001"):
    return sweep_root.transcript(name, raw=raw, mtime=now - HOUR)


def test_truncated_jsonl_transcript_is_could_not_determine(now, sweep_root):
    # no complete record carries both timestamp and sessionId (SPEC line 442)
    cut = b'{"type": "user", "timestamp": "2026-11-08T11:00:00.000Z", "sess'
    path = _write_transcript(sweep_root, now, cut)
    unreadable = probes.read_transcript_tail(path)
    assert unreadable.readable is False
    result = run(sweep_input(now, transcripts=(unreadable,)), make_ctx(now))
    c = by_id(result)["transcript:session-0001"]
    assert_unknown(c, N_TRANSCRIPT)


def test_transcript_cut_only_in_its_last_line_is_classified_normally(now, sweep_root):
    good = json.dumps(
        {"type": "user", "timestamp": "2026-11-08T11:00:00.000Z", "sessionId": "sess-X"}
    ).encode()
    path = _write_transcript(
        sweep_root, now, good + b'\n{"type": "user", "timestamp": "2026-11-08T11:3'
    )
    readable = probes.read_transcript_tail(path)
    assert readable.readable is True
    assert readable.last_record_ts == at(11)
    c = by_id(run(sweep_input(now, transcripts=(readable,)), make_ctx(now)))[
        "transcript:sess-X"
    ]
    assert c.row.person_started is True
    assert c.classification.class_name == PERSON_ACTIVE


def test_transcript_whose_open_raises_oserror_is_could_not_determine(
    now, sweep_root, monkeypatch
):
    path = _write_transcript(sweep_root, now, b"{}\n")
    real_open = builtins.open

    def refuse(file, *args, **kwargs):
        if str(file) == str(path):
            raise PermissionError(13, "denied")
        return real_open(file, *args, **kwargs)

    with monkeypatch.context() as m:
        m.setattr(builtins, "open", refuse)
        unreadable = probes.read_transcript_tail(path)
    assert unreadable.readable is False
    sources = ok_sources("R1") + (src(f"transcript {path}", "transcript not readable"),)
    result = run(
        sweep_input(now, transcripts=(unreadable,), sources=sources), make_ctx(now)
    )
    assert_unknown(by_id(result)[f"transcript:{path.stem}"], N_TRANSCRIPT)


def test_contract_whose_open_raises_oserror_is_could_not_determine(
    now, sweep_root, monkeypatch
):
    path = sweep_root.contract("reports/run", worker_status="blocked")
    real_read = Path.read_bytes

    def refuse(self):
        if self == path:
            raise PermissionError(13, "denied")
        return real_read(self)

    with monkeypatch.context() as m:
        m.setattr(Path, "read_bytes", refuse)
        assert probes.read_contract(path) is None
    sources = ok_sources("R1") + (src("contract D1", "contract not readable"),)
    inp = sweep_input(now, orca_rows=(orca("D1", outcome="failed"),), sources=sources)
    c = by_id(run(inp, make_ctx(now)))["orca:D1"]
    assert_unknown(c, N_CONTRACT)


def test_inconsistent_contract_observation_is_named(now):
    sources = ok_sources("R1") + (
        src("contract D1", "conflict: inconsistent observation"),
    )
    inp = sweep_input(now, orca_rows=(orca("D1"),), sources=sources)
    assert_unknown(
        by_id(run(inp, make_ctx(now)))["orca:D1"], "conflict: inconsistent observation"
    )


# ===========================================================================================
# FR-010: complete-negative join, the control and the seven test_fr010_* fixtures
# (shared Given, path A; each fixture changes only the list-completeness inputs it names)
# ===========================================================================================


def fr010(
    now: datetime,
    *,
    runs: tuple[str, ...] = ("R1",),
    orca_rows=None,
    sources=None,
    available: bool = True,
    truncated: bool = False,
    tab_map=(),
):
    t = tail("sess-T", now - 8 * HOUR)  # unjoined, no tab-map entry
    u = tail("sess-U", now - 30 * MINUTE)  # active; joined to D1
    rows = (orca("D1", session_join="sess-U"),) if orca_rows is None else orca_rows
    inp = sweep_input(
        now,
        orca_rows=rows,
        transcripts=(t, u),
        tab_map=tab_map,
        sources=ok_sources(*runs) if sources is None else sources,
        available=available,
        truncated=truncated,
    )
    return inp, make_ctx(now, runs=runs)


def assert_origin_unknown(result, *notes: str) -> None:
    t = by_id(result)["transcript:sess-T"]
    assert t.row.person_started is None
    assert t.classification.class_name == UNKNOWN
    assert t.classification.notes == notes  # exactly these, in this order
    assert t.classification.class_name not in (IDLE, PERSON_ACTIVE)
    assert result.summary["historical"] == 0
    assert t in result.rows  # visible
    assert N_SP16 not in t.classification.notes
    assert N_JOIN_NOT_OBSERVABLE not in t.classification.notes


def test_fr010_control_complete_list_older_transcript_is_true_and_historical(
    now, path_a
):
    result = run(*fr010(now))
    t = by_id(result)["transcript:sess-T"]
    assert t.row.person_started is True
    assert t.classification.class_name == IDLE
    assert t.classification.notes == (N_ORIGIN_NOT_PROVED,)
    assert result.summary["historical"] == 1
    u_row = by_id(result)["orca:D1"]
    assert u_row.row.person_started is False  # U joined D1 by path A
    assert "transcript:sess-U" not in by_id(result)


def test_fr010_outage_older_transcript_unknown_not_historical(now, path_a):
    sources = (
        src("orca worker-list R1", "orca unavailable"),
        src("ccsession orca-tabs"),
    )
    inp, ctx = fr010(now, orca_rows=(), sources=sources, available=False)
    assert_origin_unknown(run(inp, ctx), N_O_UNAVAILABLE)


def test_fr010_full_page_uncaptured_continuation(now, path_a):
    page = [
        orca(f"D{i:03d}", session_join=f"pane-{i}")
        for i in range(1, probes.WORKER_LIST_PAGE)
    ] + [orca("D100", session_join="sess-U")]
    assert len(page) == probes.WORKER_LIST_PAGE == 100
    inp, ctx = fr010(now, orca_rows=tuple(page), truncated=True)
    result = run(inp, ctx)
    assert_origin_unknown(result, N_O_TRUNCATED)
    assert result.summary["total_is_lower_bound"] is True


def test_fr010_call_failed_incomplete_list(now, path_a):
    sources = (
        src("orca worker-list R1"),
        src("orca worker-list R2", "orca call failed (exit 1)"),
        src("ccsession orca-tabs"),
    )
    inp, ctx = fr010(now, runs=("R1", "R2"), sources=sources)
    assert_origin_unknown(run(inp, ctx), N_O_CALL_FAILED)


def test_fr010_unknown_run_empty_list_unknown(now, path_a):
    sources = ok_sources("R1", "BAD") + (
        src("orca task-list BAD", "orca call failed (exit 1)"),
    )
    inp, ctx = fr010(now, runs=("R1", "BAD"), sources=sources)
    assert_origin_unknown(run(inp, ctx), N_O_RUN)
    # the same input with task-list BAD not unscanned is a real Run with no rows: control result
    sources = ok_sources("R1", "BAD") + (src("orca task-list BAD"),)
    inp, ctx = fr010(now, runs=("R1", "BAD"), sources=sources)
    t = by_id(run(inp, ctx))["transcript:sess-T"]
    assert t.row.person_started is True and t.classification.class_name == IDLE


def test_fr010_run_not_reached_budget_unknown(now, path_a):
    sources = (
        src("orca worker-list R1"),
        src("orca worker-list R2", "time budget reached (90 s)"),
        src("ccsession orca-tabs"),
    )
    inp, ctx = fr010(now, runs=("R1", "R2"), sources=sources)
    assert_origin_unknown(run(inp, ctx), N_O_CALL_FAILED)


def test_fr010_tab_map_unreadable_older_transcript_unknown(now, path_a):
    sources = (
        src("orca worker-list R1"),
        src("ccsession orca-tabs", "tab map not readable"),
    )
    inp, ctx = fr010(now, sources=sources)
    assert_origin_unknown(run(inp, ctx), N_O_TABS)
    # the same input with an empty readable folder gives the control result
    t = by_id(run(*fr010(now)))["transcript:sess-T"]
    assert t.row.person_started is True and t.classification.class_name == IDLE


def test_fr010_incomplete_notes_order(now, path_a):
    # part (a): a partial outage; guard cases 1 and 2 hold too
    inp = sweep_input(
        now,
        orca_rows=(orca("D1", session_join=None),),
        transcripts=(tail("sess-T", now - 8 * HOUR),),
        available=False,
    )
    t = by_id(run(inp, make_ctx(now)))["transcript:sess-T"]
    assert t.row.person_started is None
    assert t.classification.class_name == UNKNOWN
    assert t.classification.notes == (N_O_UNAVAILABLE, N_SP16, N_JOIN_NOT_OBSERVABLE)
    # part (b): several list-incomplete cases together, with no join-guard note
    rows = [orca(f"D{i:03d}", session_join=f"pane-{i}") for i in range(1, 100)]
    rows.append(orca("D100", session_join="sess-U"))
    sources = (
        src("orca worker-list R1"),
        src("orca worker-list R2", "orca call failed (exit 1)"),
        src("orca worker-list R3"),
        src("orca task-list R3", "orca call failed (exit 1)"),
        src("ccsession orca-tabs", "tab map not readable"),
    )
    inp, ctx = fr010(
        now,
        runs=("R1", "R2", "R3"),
        orca_rows=tuple(rows),
        sources=sources,
        truncated=True,
    )
    assert_origin_unknown(
        run(inp, ctx), N_O_TRUNCATED, N_O_CALL_FAILED, N_O_RUN, N_O_TABS
    )


# ===========================================================================================
# FR-010 exemptions (Change 33), SP-29, person_started tri-state, D9 join fixtures
# ===========================================================================================


@pytest.mark.parametrize(
    ("case_row", "expected"),
    [
        pytest.param(
            row(person_started=True, transcript_readable=False, last_activity=at(1)),
            ("fallback", UNKNOWN),
            id="unreadable-transcript",
        ),
        pytest.param(
            row(person_started=True, transcript_readable=True, last_activity=None),
            ("fallback", UNKNOWN),
            id="unknown-timestamp",
        ),
        pytest.param(
            row(
                person_started=True,
                transcript_readable=True,
                last_activity=at(1),
                orca=orca(status="in_progress"),
            ),
            ("fallback", UNKNOWN),
            id="open-task",
        ),
        pytest.param(
            row(
                person_started=True,
                transcript_readable=True,
                last_activity=at(1),
                orca=orca(agent_wait={"since": "x"}),
            ),
            ("waiting_signal", WAITING),
            id="explicit-wait",
        ),
        pytest.param(
            row(
                person_started=True,
                transcript_readable=True,
                last_activity=at(1),
                orca=orca(outcome="succeeded"),
            ),
            ("fallback", UNKNOWN),
            id="unread-report-candidate",
        ),
    ],
)
def test_fr010_exemptions_never_become_idle(now, case_row, expected):
    # TST-F6: ``last_activity`` is at(1), 11 h before ``now`` and outside the 6 h window, so a
    # missing window test in rule 8 would turn these rows into ``person session (active)``.
    cls = classify(case_row, make_ctx(now))
    assert (cls.rule, cls.class_name) == expected


def test_fr010_exemption_orca_rows_never_go_to_historical(now, path_a):
    stale = tail(
        "sess-W", now - 9 * HOUR
    )  # an open Task whose worker transcript is old
    open_task = orca("D1", session_join="sess-W", status="in_progress")
    result = run(
        sweep_input(now, orca_rows=(open_task,), transcripts=(stale,)), make_ctx(now)
    )
    assert result.summary["historical"] == 0
    assert by_id(result)["orca:D1"].classification.class_name != IDLE


def test_sp29_other_run_transcripts_are_never_true_or_historical(now, path_b):
    # R1 has 2 workers, R2 has 3 in the same worktree tree; the tab map lists all 5
    sids = [f"sess-{i}" for i in range(1, 6)]
    entries = [
        entry(s, pane=f"tab{i}+leaf{i}", handle=f"term-{i}")
        for i, s in enumerate(sids, 1)
    ]
    rows = [
        orca(
            f"D{i}",
            session_join=f"term-{i}",
            dispatch_started=at(9),
            dispatch_status="dispatched",
        )
        for i in (1, 2)
    ]
    tails = [tail(s, now - 2 * HOUR, at(9, 5)) for s in sids]
    result = run(
        sweep_input(now, orca_rows=rows, transcripts=tails, tab_map=entries),
        make_ctx(now),
    )
    assert {"orca:D1", "orca:D2"} <= set(by_id(result))
    for sid in sids[2:]:
        c = by_id(result)[f"transcript:{sid}"]
        assert c.row.person_started is None
        assert c.classification.class_name == UNKNOWN
        assert N_NOT_SCOPED in c.classification.notes
    assert result.summary["historical"] == 0


def test_person_started_is_none_for_every_unjoined_transcript_while_join_is_none(
    now, path_a
):
    inp = sweep_input(
        now,
        orca_rows=(orca("D1", session_join=None),),
        transcripts=(tail("sess-A", now - 8 * HOUR), tail("sess-B", now - 1 * HOUR)),
    )
    result = run(inp, make_ctx(now))
    for sid in ("sess-A", "sess-B"):
        c = by_id(result)[f"transcript:{sid}"]
        assert c.row.person_started is None
        assert N_JOIN_NOT_OBSERVABLE in c.classification.notes
    assert result.summary["historical"] == 0


def test_d9_path_b_tab_map_join_is_false_and_shown_as_the_dispatch_row(now, path_b):
    d1 = pane_row("D1", at(10), None, "dispatched")
    s = tail("S", at(11, 30), at(10, 5))
    result = run(
        sweep_input(now, orca_rows=(d1,), transcripts=(s,), tab_map=(entry("S"),)),
        make_ctx(now),
    )
    assert set(by_id(result)) == {"orca:D1"}  # no transcript:S row
    c = by_id(result)["orca:D1"]
    assert c.row.person_started is False
    assert c.row.transcript_path == s.path
    assert N_JOINED in c.classification.notes


def test_d9_tab_map_entry_that_joins_no_scoped_row_is_none_even_when_guard_holds(
    now, path_a
):
    inp, ctx = fr010(now, tab_map=(entry("sess-T", pane="x+1", handle="term-x"),))
    result = run(inp, ctx)
    t = by_id(result)["transcript:sess-T"]
    assert t.row.person_started is None
    assert t.classification.class_name == UNKNOWN
    assert t.classification.notes == (N_NOT_SCOPED,)
    assert result.summary["historical"] == 0


def test_d9_path_a_no_entry_true_carries_the_origin_not_proved_note(now, path_a):
    # a worker of an unscoped Run in the same worktree has no entry either: still noted
    inp = sweep_input(
        now,
        orca_rows=(orca("D1", session_join="sess-U"),),
        transcripts=(
            tail("sess-U", now - 30 * MINUTE),
            tail("sess-T", now - 8 * HOUR),
            tail("sess-W", now - 2 * HOUR),
        ),
    )
    result = run(inp, make_ctx(now))
    trues = [c for c in result.rows if c.row.person_started is True]
    assert {c.row.row_id for c in trues} == {"transcript:sess-T", "transcript:sess-W"}
    for c in trues:
        assert N_ORIGIN_NOT_PROVED in c.classification.notes


def test_d9_path_b_unmatched_session_join_makes_every_unjoined_transcript_none(
    now, path_b
):
    ghost = pane_row("D1", at(9), None, "dispatched", join="no-such-pane")
    inp = sweep_input(
        now,
        orca_rows=(ghost,),
        transcripts=(
            tail("sess-T", now - 8 * HOUR),
            tail("sess-V", now - 8 * HOUR),
        ),
        tab_map=(entry("sess-V", pane="tab9+leaf9", handle="term-9"),),
    )
    result = run(inp, make_ctx(now))
    for sid in ("sess-T", "sess-V"):
        c = by_id(result)[f"transcript:{sid}"]
        assert c.row.person_started is None
        assert N_SP16 in c.classification.notes
    assert N_EARLIER in notes_of(result, "transcript:sess-T")
    assert N_NOT_SCOPED in notes_of(result, "transcript:sess-V")


def test_guard_cases_1_and_2_together_put_sp16_first_then_join_not_observable(
    now, path_a
):
    inp = sweep_input(
        now,
        orca_rows=(orca("D1", session_join=None),),
        transcripts=(tail("sess-T", now - 8 * HOUR),),
    )
    t = by_id(run(inp, make_ctx(now)))["transcript:sess-T"]
    assert t.classification.notes == (N_SP16, N_JOIN_NOT_OBSERVABLE)


def test_spec_line_236_worker_rows_present_no_transcript_joined(now, path_a):
    inp = sweep_input(
        now,
        orca_rows=(orca("D1", session_join="sess-elsewhere"),),
        transcripts=(tail("sess-T", now - 8 * HOUR),),
    )
    t = by_id(run(inp, make_ctx(now)))["transcript:sess-T"]
    assert t.row.person_started is None
    assert t.classification.class_name == UNKNOWN
    assert t.classification.notes == (N_SP16,)


# ===========================================================================================
# R2-B1 pane reuse (path B): /clear, a resume and a person rerun leave the same data
# ===========================================================================================


def pane_row(
    dispatch: str,
    start: datetime | None,
    end: datetime | None = None,
    status: str = "dispatched",
    join: str = PANE,
    **kw,
) -> OrcaObservation:
    return orca(
        dispatch,
        session_join=join,
        dispatch_started=start,
        dispatch_ended=end,
        dispatch_status=status,
        **kw,
    )


S_TAIL = dict(last=at(11, 30))  # S last_record_ts is 11:30 in every R3-B2 fixture


def b_result(rows, tails, entries=None, now=at(12)):
    """A path-B sweep at 12:00, window 6 h, every row in Run R1."""
    entries = (entry("S"),) if entries is None else entries
    inp = sweep_input(now, orca_rows=rows, transcripts=tails, tab_map=entries)
    return run(inp, make_ctx(now))


@pytest.mark.parametrize("cause", ["clear", "resume", "person-rerun"])
def test_r2_b1_pane_reuse_outside_window_does_not_join(path_b, cause):
    # the tab map keeps one session per pane, so the three causes give identical input
    d1 = pane_row("D1", at(9), at(10), "completed")
    early = tail(
        "sess-early", at(9, 50), at(9, 1)
    )  # the worker's own session: no entry
    late = tail("sess-late", **S_TAIL, first=at(10, 30))
    result = b_result([d1], [early, late], (entry("sess-late"),))
    assert_unknown(by_id(result)["orca:D1"], N_MOVED)
    e = by_id(result)["transcript:sess-early"]
    assert e.row.person_started is None
    assert N_EARLIER in e.classification.notes
    assert e.classification.class_name == UNKNOWN
    lt = by_id(result)["transcript:sess-late"]
    assert lt.row.person_started is None
    assert N_MOVED in lt.classification.notes
    assert not [c for c in result.rows if c.row.person_started is True]
    assert result.summary["historical"] == 0


def test_r2_b1_later_session_inside_the_window_is_false_and_noted(path_b):
    d1 = pane_row("D1", at(9), at(10), "completed")
    early = tail("sess-early", at(9, 50), at(9, 1))
    late = tail("sess-late", **S_TAIL, first=at(9, 30))
    result = b_result([d1], [early, late], (entry("sess-late"),))
    c = by_id(result)["orca:D1"]
    assert c.row.person_started is False
    assert N_JOINED in c.classification.notes
    assert notes_of(result, "transcript:sess-early") == (N_EARLIER,)


def test_r2_b1_row_with_no_observable_start_never_joins_by_path_b(path_b):
    d1 = pane_row("D1", None, None, "dispatched")
    result = b_result([d1], [tail("S", **S_TAIL, first=at(10, 5))])
    assert_unknown(by_id(result)["orca:D1"], N_WINDOW)
    assert by_id(result)["transcript:S"].row.person_started is None


# ===========================================================================================
# R3-B1 path-B window fixtures
# ===========================================================================================


def test_path_b_window_open_row_joins(path_b):
    d1 = pane_row("D1", at(10), None, "dispatched")
    s = tail("S", **S_TAIL, first=at(10, 5))
    result = b_result([d1], [s])
    assert set(by_id(result)) == {"orca:D1"}
    c = by_id(result)["orca:D1"]
    assert c.row.person_started is False
    assert c.row.transcript_path == s.path
    assert N_JOINED in c.classification.notes  # the first D9 limit: no upper bound


@pytest.mark.parametrize(
    "first, joins",
    [
        pytest.param(at(10, 0, 0, 700_000), True, id="start-second-cut"),
        pytest.param(at(11, 0, 0, 400_000), True, id="end-second-cut"),
        pytest.param(at(11, 0, 1), False, id="one-second-after-end"),
    ],
)
def test_path_b_window_inclusive_bounds(path_b, first, joins):
    d1 = pane_row("D1", at(10), at(11), "completed")
    result = b_result([d1], [tail("S", **S_TAIL, first=first)])
    if joins:
        assert by_id(result)["orca:D1"].row.person_started is False
        assert "transcript:S" not in by_id(result)
    else:
        assert_unknown(by_id(result)["orca:D1"], N_MOVED)
        s = by_id(result)["transcript:S"]
        assert s.row.person_started is None
        assert N_MOVED in s.classification.notes


def test_path_b_terminal_row_without_end_has_no_window(path_b):
    d1 = pane_row("D1", at(10), None, "completed")
    result = b_result([d1], [tail("S", **S_TAIL, first=at(10, 30))])
    assert_unknown(by_id(result)["orca:D1"], N_WINDOW)
    s = by_id(result)["transcript:S"]
    assert s.row.person_started is None
    assert N_WINDOW in s.classification.notes


def test_path_b_row_without_start_has_no_window(path_b):
    d1 = pane_row(
        "D1", None, None, "dispatched"
    )  # for example past the 50-call show cap
    result = b_result([d1], [tail("S", **S_TAIL, first=at(10, 30))])
    assert_unknown(by_id(result)["orca:D1"], N_WINDOW)
    s = by_id(result)["transcript:S"]
    assert s.row.person_started is None  # never True
    assert N_WINDOW in s.classification.notes


def test_path_b_incomplete_tail_has_no_session_start(path_b):
    d1 = pane_row("D1", at(10), at(11), "completed")
    s = tail("S", **S_TAIL, first=at(10, 30), complete=False)
    result = b_result([d1], [s])
    assert_unknown(by_id(result)["orca:D1"], N_TAIL)
    c = by_id(result)["transcript:S"]
    assert c.row.person_started is None  # never False or True
    assert N_TAIL in c.classification.notes


# ===========================================================================================
# R3-B2 several-rows fixtures (path B, 12:00 now and collected_start, window 6 h)
# ===========================================================================================


def _reused_pane(join: str = PANE):
    d1 = pane_row(
        "D1",
        at(9),
        at(10),
        "completed",
        join=join,
        outcome="succeeded",
        task_spec_text="--report-dir /sweep-root/.dev/reports/d1",
    )
    d2 = pane_row("D2", at(10, 30), None, "dispatched", join=join)
    return d1, d2


def _reused_pane_result(rows_order=(0, 1), join: str = PANE, entries=None):
    d1, d2 = _reused_pane(join)
    rows = [(d1, d2)[i] for i in rows_order]
    done = contract(
        "succeeded", path="/sweep-root/.dev/reports/d1/return-contract.yaml"
    )
    inp = sweep_input(
        at(12),
        orca_rows=rows,
        transcripts=(tail("S", **S_TAIL, first=at(10, 40)),),
        tab_map=(entry("S"),) if entries is None else entries,
        contracts=(done,),
    )
    return run(inp, make_ctx(at(12)))


def _assert_reused_pane(result):
    d2 = by_id(result)["orca:D2"]
    assert d2.row.person_started is False
    assert N_JOINED in d2.classification.notes
    assert N_MOVED not in d2.classification.notes  # S's notes do not hold the D1 note
    assert "transcript:S" not in by_id(result)
    d1 = by_id(result)["orca:D1"]
    assert_unknown(d1, N_MOVED)
    assert d1.classification.rule != "finished"
    assert (
        "Orca outcome succeeded" in d1.classification.evidence
    )  # rule 6 evidence kept


def test_path_b_pane_reused_joins_later_row_only(path_b):
    _assert_reused_pane(_reused_pane_result())


def test_path_b_rows_share_terminal_handle(path_b):
    # D1 and D2 match by terminal_handle (tab-map line 3), not by file name
    _assert_reused_pane(_reused_pane_result(join=HANDLE))


def _two_windows_result(order=(0, 1)):
    d1 = pane_row("D1", at(9), None, "dispatched")
    d2 = pane_row("D2", at(10), None, "pending")
    rows = [(d1, d2)[i] for i in order]
    return b_result(rows, [tail("S", **S_TAIL, first=at(10, 5))])


def test_path_b_two_windows_hold_session_is_conflict(path_b):
    result = _two_windows_result()
    for dispatch in ("D1", "D2"):
        c = by_id(result)[f"orca:{dispatch}"]
        assert_unknown(c, N_SEVERAL)
        assert c.row.transcript_path is None  # no orca row carries S
    s = by_id(result)["transcript:S"]
    assert s.row.person_started is None
    assert N_SEVERAL in s.classification.notes
    assert_no_sp16(result)


def test_path_b_shared_boundary_second_is_conflict(path_b):
    d1 = pane_row("D1", at(9), at(10), "completed")
    d2 = pane_row("D2", at(10), None, "dispatched")
    result = b_result([d1, d2], [tail("S", **S_TAIL, first=at(10, 0, 0, 400_000))])
    assert_unknown(by_id(result)["orca:D1"], N_SEVERAL)
    assert_unknown(by_id(result)["orca:D2"], N_SEVERAL)
    assert by_id(result)["transcript:S"].row.person_started is None


def test_path_b_no_matching_window_holds(path_b):
    d1 = pane_row("D1", at(9), at(9, 30), "completed")
    d2 = pane_row("D2", at(10), at(10, 30), "completed")
    result = b_result([d1, d2], [tail("S", **S_TAIL, first=at(11))])
    assert_unknown(by_id(result)["orca:D1"], N_MOVED)
    assert_unknown(by_id(result)["orca:D2"], N_MOVED)
    s = by_id(result)["transcript:S"]
    assert s.row.person_started is None
    assert N_MOVED in s.classification.notes
    assert_no_sp16(result)


def _snapshot(result):
    return [
        (c.row.row_id, c.classification.class_name, c.classification.notes)
        for c in result.rows
    ]


@pytest.mark.parametrize(
    "build",
    [
        pytest.param(_reused_pane_result, id="reused-pane"),
        pytest.param(_two_windows_result, id="two-windows"),
    ],
)
def test_path_b_multi_row_result_ignores_row_order(path_b, build):
    assert _snapshot(build((0, 1))) == _snapshot(build((1, 0)))


def test_path_b_entry_failing_window_note_order(path_b):
    d1 = pane_row("D1", at(9), at(10), "completed")
    result = b_result([d1], [tail("S", **S_TAIL, first=at(10, 30))])
    notes = notes_of(result, "transcript:S")
    assert N_MOVED in notes
    assert N_NOT_SCOPED not in notes
    assert_no_sp16(result)


@pytest.mark.parametrize("order", [(0, 1), (1, 0)])
def test_path_b_two_rows_incomplete_tail(path_b, order):
    d1 = pane_row("D1", at(9), at(10), "completed")
    d2 = pane_row("D2", at(10, 30), None, "dispatched")
    s = tail("S", **S_TAIL, first=at(10, 40), complete=False)
    result = b_result([(d1, d2)[i] for i in order], [s])
    for dispatch in ("D1", "D2"):
        assert_unknown(by_id(result)[f"orca:{dispatch}"], N_TAIL)
    c = by_id(result)["transcript:S"]
    assert c.row.person_started is None  # never False
    assert N_TAIL in c.classification.notes
    assert_no_sp16(result)
    # with D2's start None instead, D1 and S keep the tail-only note and D2 is not observable
    d2_blind = pane_row("D2", None, None, "dispatched")
    result = b_result([(d1, d2_blind)[i] for i in order], [s])
    assert_unknown(by_id(result)["orca:D1"], N_TAIL)
    assert_unknown(by_id(result)["orca:D2"], N_WINDOW)
    assert N_TAIL in notes_of(result, "transcript:S")


def test_path_b_live_session_spans_two_dispatches(path_b):
    d1 = pane_row("D1", at(9), at(10), "completed")
    d2 = pane_row("D2", at(10, 30), None, "dispatched")
    result = b_result([d1, d2], [tail("S", **S_TAIL, first=at(9, 5))])
    one = by_id(result)["orca:D1"]
    assert one.row.person_started is False and N_JOINED in one.classification.notes
    two = by_id(result)["orca:D2"]
    assert_unknown(two, N_BEFORE)
    assert N_MOVED not in two.classification.notes  # pins the second D9 limit
    assert "transcript:S" not in by_id(result)


def test_path_b_duplicate_dispatch_rows_count_once(path_b):
    d1a = pane_row("D1", at(9), None, "dispatched")
    d1b = pane_row("D1", at(9), at(10), "completed")
    result = b_result([d1a, d1b], [tail("S", **S_TAIL, first=at(9, 30))])
    assert [i for i in by_id(result) if i.startswith("orca:")] == ["orca:D1"]
    merged = by_id(result)["orca:D1"]
    assert_unknown(merged, N_DUPLICATE, N_WINDOW)
    assert merged.row.transcript_path is None
    s = by_id(result)["transcript:S"]
    assert s.row.person_started is None
    assert N_WINDOW in s.classification.notes
    for c in (merged, s):
        assert N_SEVERAL not in c.classification.notes
    assert_no_sp16(result)


# ===========================================================================================
# FR-012, FR-013 (one fixture per condition), FR-005 (M9)
# ===========================================================================================


def wtree(path: str = "/w1", **kw) -> WorktreeState:
    base = dict(
        path=path,
        status_read=True,
        uncommitted=False,
        unpushed=False,
        dev_tasks_unsaved=False,
        changed_paths=(),
        packages=(),
        shared_package_ids=(),
        frozen=None,
    )
    base.update(kw)
    return WorktreeState(**base)


def pkgrec(pid, location="to-do", final=False, marker=False, active=False):
    return PackageRecord(pid, location, final, marker, active, "unknown")


@pytest.mark.parametrize(
    "terminal_state, next_action, terminal",
    [
        ("retained", "release", "no"),
        ("retained", None, "no"),
        (None, "release", "could not determine"),
        ("reclaimable", None, "could not determine"),
        ("reclaimable", "release", "could not determine"),
        ("reclaimable", "keep", "no"),
        ("other", "release", "no"),
    ],
)
def test_fr012_terminal_values_and_worktree_is_never_yes(
    terminal_state, next_action, terminal
):
    observed = orca(terminal_state=terminal_state, next_action=next_action)
    for worktree in (None, wtree(), wtree(status_read=False), wtree(uncommitted=True)):
        safe = safe_to_close(row(orca=observed), worktree)
        assert safe.terminal == terminal
        assert safe.worktree in ("no", "could not determine")
    assert safe_to_close(row(), None).terminal == "could not determine"


@pytest.mark.parametrize(
    "state, reason_part",
    [
        pytest.param(dict(uncommitted=True), "uncommitted", id="uncommitted"),
        pytest.param(
            dict(unpushed=True, upstream_note="ahead 3"), "ahead 3", id="unpushed-ahead"
        ),
        pytest.param(
            dict(unpushed=None, upstream_note="no upstream"),
            "no upstream",
            id="unpushed-no-upstream",
        ),
        pytest.param(
            dict(dev_tasks_unsaved=True), ".dev/tasks/", id="unsaved-dev-tasks"
        ),
        pytest.param(dict(frozen=True), "frozen plan", id="frozen-plan"),
        pytest.param(
            dict(packages=(pkgrec("p1", "to-do", final=False),)),
            "package p1 is unfinished",
            id="package-unfinished",
        ),
        pytest.param(
            dict(packages=(pkgrec("p1", "to-do", final=True),)),
            "package p1 is archive-blocked",
            id="package-archive-blocked",
        ),
        pytest.param(
            dict(packages=(pkgrec("p1", "to-do", final=True, marker=True),)),
            "package p1 is interrupted-archive",
            id="package-interrupted-archive",
        ),
        pytest.param(
            dict(packages=(pkgrec("p1", "both"),)),
            "package p1 is conflict",
            id="package-conflict",
        ),
        pytest.param(
            dict(shared_package_ids=("p9",)),
            "active package p9 shared with another worktree",
            id="shared-active-package",
        ),
    ],
)
def test_fr013_one_fixture_per_condition_names_the_condition(state, reason_part):
    value, reason = removable(wtree(**state))
    assert value == "no"
    assert reason_part in reason


def test_fr013_first_condition_wins_and_archived_does_not_block():
    value, reason = removable(wtree(uncommitted=True, frozen=True))
    assert (value, reason) == ("no", "uncommitted changes")
    value, reason = removable(wtree(packages=(pkgrec("p1", "done"),)))
    assert value == "could not determine"
    assert reason == "report read, open PR and unmerged commits not observable"
    value, reason = removable(wtree(status_read=False))
    assert (value, reason) == (
        "could not determine",
        "unscanned: worktree not readable",
    )


def test_fr013_frozen_row_makes_its_worktree_a_frozen_plan(now):
    host = orca(
        "D1",
        worktree_path="/w1",
        task_spec_text="--report-dir /w1/.dev/reports/run",
    )
    frozen = contract(
        "failed", path="/w1/.dev/reports/run/return-contract.yaml", reason="E-QA-FAIL"
    )
    result = run(
        sweep_input(
            now,
            orca_rows=(host,),
            contracts=(frozen,),
            worktrees=(wtree("/w1"), wtree("/w2")),
        ),
        make_ctx(now),
    )
    first, second = result.worktrees
    assert first.frozen is True
    assert (first.removable, first.removable_reason) == ("no", "frozen plan")
    assert second.frozen is None
    assert by_id(result)["orca:D1"].policy == "frozen"
    assert by_id(result)["orca:D1"].safe.worktree == "no"


def test_fr005_three_workers_two_worktrees_one_active_person_session(now, path_a):
    workers = [
        orca(f"D{i}", session_join=f"sess-w{i}", worktree_path=f"/w{1 + i % 2}")
        for i in (1, 2, 3)
    ]
    tails = [tail(f"sess-w{i}", now - 20 * MINUTE) for i in (1, 2, 3)]
    tails.append(tail("sess-person", now - 10 * MINUTE))  # M9: an active session
    result = run(
        sweep_input(
            now,
            orca_rows=workers,
            transcripts=tails,
            worktrees=(wtree("/w1"), wtree("/w2")),
        ),
        make_ctx(now),
    )
    assert len(result.rows) == 4
    assert len(result.worktrees) == 2
    person = by_id(result)["transcript:sess-person"]
    assert person.row.person_started is True
    assert person.classification.class_name == PERSON_ACTIVE
    assert result.summary["total"] == result.summary["visible"] == 4
    assert result.summary["historical"] == 0


# ===========================================================================================
# FR-014 package states, FR-015 shared packages
# ===========================================================================================


def _unreadable_ledger(root):
    folder = root.package("p", ledger=None)
    (folder / "progress.md").mkdir()  # open raises OSError: the ledger is unreadable


PACKAGE_FIXTURES = {
    "unfinished": lambda r: r.package("p", ledger="step 1 done\n"),
    "archive-blocked": lambda r: r.package("p", ledger="step 1 done\n", final=True),
    "interrupted-archive": lambda r: r.package("p", ledger="x\n", archiving=True),
    "conflict": lambda r: (
        r.package("p", location="to-do", ledger="x\n"),
        r.package("p", location="done", ledger=None),
    ),
    "archived": lambda r: r.package("p", location="done", ledger=None),
    "unknown": _unreadable_ledger,
}


def test_package_fixtures_cover_every_package_state():
    assert set(PACKAGE_FIXTURES) == set(PACKAGE_STATES)


@pytest.mark.parametrize("state", list(PACKAGE_FIXTURES))
def test_fr014_one_fixture_per_package_state(sweep_root, state):
    PACKAGE_FIXTURES[state](sweep_root)
    (record,) = probes.read_packages(sweep_root.root)
    assert package_state(record) == state


@pytest.mark.parametrize(
    "ledger, state",
    [
        ("note: FINAL: is quoted here, not a line start\nmore\n", "unfinished"),
        ("step 1\n   FINAL: all tasks complete\n", "archive-blocked"),
    ],
)
def test_sp07_final_counts_only_at_the_start_of_a_line(sweep_root, ledger, state):
    sweep_root.package("p", ledger=ledger)
    (record,) = probes.read_packages(sweep_root.root)
    assert package_state(record) == state


@pytest.mark.parametrize(
    "record, state",
    [
        (pkgrec("p", "both", final=True, marker=True), "conflict"),
        (pkgrec("p", "to-do", final=True, marker=True), "interrupted-archive"),
        (pkgrec("p", "done", marker=True), "interrupted-archive"),
        (pkgrec("p", "to-do", final=True), "archive-blocked"),
        (pkgrec("p", "to-do", final=None), "unknown"),
    ],
)
def test_fr014_precedence_is_the_order_of_package_states(record, state):
    assert package_state(record) == state


def _three_worktrees(active_in: tuple[bool, bool, bool]):
    folders = [f"pkg-{i:02d}" for i in range(44)]
    return tuple(
        wtree(
            f"/w{n}",
            packages=tuple(
                pkgrec(p, "done", active=(active and p == "pkg-07")) for p in folders
            ),
        )
        for n, active in enumerate(active_in, 1)
    )


def test_fr015_44_committed_folders_in_3_worktrees_give_no_shared_flag():
    marked = mark_shared_packages(_three_worktrees((False, False, False)))
    assert all(w.shared_package_ids == () for w in marked)


def test_fr015_one_modified_folder_in_3_worktrees_is_shared_by_all_3(now):
    ctx = make_ctx(now)
    result = run(sweep_input(now, worktrees=_three_worktrees((True, True, True))), ctx)
    assert [w.shared_package_ids for w in result.worktrees] == [("pkg-07",)] * 3
    # One printed line names all 3 worktrees (report.py builds it from shared_package_ids).
    printed = [
        line
        for line in report_module.render(result, ctx).splitlines()
        if "is in several worktrees" in line
    ]
    assert printed == ["- Active package pkg-07 is in several worktrees: /w1, /w2, /w3"]
    for w in result.worktrees:
        assert w.removable == "no"
        assert (
            w.removable_reason == "active package pkg-07 shared with another worktree"
        )


def test_fr015_active_in_only_one_worktree_is_not_shared():
    marked = mark_shared_packages(_three_worktrees((True, False, False)))
    assert all(w.shared_package_ids == () for w in marked)


def test_fr015_untracked_path_in_a_package_folder_marks_it_active(
    sweep_root, patch_git
):
    sweep_root.package("pkg-1", ledger="x\n")
    sweep_root.package("pkg-2", ledger="x\n")
    patch_git.respond(
        sweep_root.root,
        "## main...origin/main\0?? .dev/tasks/to-do/pkg-1/progress.md\0",
    )
    state, _ = probes.read_worktree(sweep_root.root, probes.Budget())
    assert {p.id: p.active for p in state.packages} == {"pkg-1": True, "pkg-2": False}


# ===========================================================================================
# NFR-004 import boundaries (DESIGN lines 210, 211, 212) and B5 (line 219)
# ===========================================================================================


def imported_names(source: str) -> set[str]:
    """Every dotted name ``source`` imports, relative imports resolved inside the package."""
    names: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                parts = SWEEP_PKG.split(".")[
                    : len(SWEEP_PKG.split(".")) - (node.level - 1)
                ]
                prefix = ".".join([*parts, *([node.module] if node.module else [])])
            else:
                prefix = node.module or ""
            names.add(prefix)
            names.update(f"{prefix}.{a.name}" for a in node.names)
    return names


def banned_hits(source: str, banned: set[str]) -> list[str]:
    return sorted(
        n
        for n in imported_names(source)
        for b in banned
        if n == b or n.startswith(b + ".")
    )


def sweep_modules(*names: str) -> set[str]:
    return {f"{SWEEP_PKG}.{n}" for n in names}


STDLIB_BANNED = {"subprocess", "click", "os", "shutil"}
CLASSIFY_BANNED = STDLIB_BANNED | sweep_modules("probes", "report", "commands")
REPORT_BANNED = STDLIB_BANNED | sweep_modules("probes", "classify", "commands")
PROBES_BANNED = {"click"} | sweep_modules("classify", "report")


@pytest.mark.parametrize(
    "source, banned",
    [
        ("import os", STDLIB_BANNED),
        ("import os.path", STDLIB_BANNED),
        ("from os import path", STDLIB_BANNED),
        ("from os.path import join", STDLIB_BANNED),
        ("import subprocess as sp", STDLIB_BANNED),
        ("import shutil", STDLIB_BANNED),
        ("import click", PROBES_BANNED),
        ("from click import command", PROBES_BANNED),
        ("from . import classify", PROBES_BANNED),
        ("from . import report as r", PROBES_BANNED),
        ("from .classify import classify_all", PROBES_BANNED),
        ("from .report import render", PROBES_BANNED),
        ("from superclaude.cli.sweep import classify", PROBES_BANNED),
        ("from superclaude.cli.sweep.report import render", PROBES_BANNED),
        ("import superclaude.cli.sweep.classify", PROBES_BANNED),
    ],
)
def test_import_scanner_catches_every_import_form(source, banned):
    assert banned_hits(source, banned), source


def test_import_scanner_ignores_allowed_imports():
    allowed = "import re\nfrom .models import SweepInput\nfrom pathlib import Path\n"
    assert banned_hits(allowed, CLASSIFY_BANNED | REPORT_BANNED | PROBES_BANNED) == []


@pytest.mark.parametrize(
    "module, banned",
    [
        ("classify.py", CLASSIFY_BANNED),
        ("report.py", REPORT_BANNED),
        ("probes.py", PROBES_BANNED),
    ],
)
def test_nfr004_module_imports_nothing_it_must_not(module, banned):
    source = (SWEEP_DIR / module).read_text(encoding="utf-8")
    assert banned_hits(source, banned) == []


@pytest.mark.parametrize("module", ["classify.py", "report.py"])
def test_classify_and_report_import_only_models_inside_the_package(module):
    names = imported_names((SWEEP_DIR / module).read_text(encoding="utf-8"))
    inside = {n.split(".")[3] for n in names if n.startswith(SWEEP_PKG + ".")}
    assert inside <= {"models"}


def _class_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}


def test_b5_no_type_is_redeclared_from_superclaude_contracts():
    root = Path(__file__).resolve().parents[2]
    models = _class_names(root / "src/superclaude/cli/sweep/models.py")
    contracts = _class_names(root / "src/superclaude/contracts/__init__.py")
    assert (
        models and contracts
    )  # both sides found, so an empty intersection means something
    assert models & contracts == set()
