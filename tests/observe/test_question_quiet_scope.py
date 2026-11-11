"""T51: the quiet-scope non-consumption test for the message read (INV-022).

A stateful fake Orca backend keeps a mailbox of ``question`` rows, a ``delivered_at`` marker per
row and an acknowledgement set. It answers only the one R2 template. It fails the test if an
argv could consume (plain ``check`` without ``--all``, or an acknowledgement or wait option) or
could narrow the read in a way the observer must not use (``--peek`` hides acknowledged rows).
The shapes follow REPORT 2.2, steps 1 to 9 (``research/evidence`` files 03 to 12 of the gate
research): rows with ``id`` (``msg_``), ``run_id``, ``created_at`` and ``delivered_at``.

A pass covers ONLY the visible effects tested here, which are the effects the gate research saw
as the owner of a probe Run: repeated reads through the observer return the same ids in the
same order and leave the fake mailbox state unchanged. It does NOT show non-consumption by a
reader that is not the Run's owner (Q-1, UNVERIFIED); that needs a plain terminal and is
plan Task 16.
"""

from __future__ import annotations

import copy
import itertools
import json

import pytest

from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector
from tests.observe.conftest import (
    QRUN,
    QUESTION_BASE,
    FakeClock,
    FakeDiscover,
    FakeRunner,
    make_envelope,
    make_question_rows,
    make_rows,
)

PASS_SCOPE = (
    "a pass covers only the visible effects tested, as the owner of a probe Run; "
    "it does not show non-consumption by a non-owner reader (Q-1)"
)
CONSUMING_TOKENS = ("--ack", "--wait", "--peek")  # none may ever reach the backend


class FakeOrcaMailbox:
    """The Run mailbox of one probe Run, answering only the R2 message template."""

    consuming = False  # a consuming fake changes the mailbox on every read

    def __init__(self, rows):
        self.rows = [dict(r) for r in rows]  # newest first, as check --all returns them
        self.delivery = None  # a pending delivery id, set only by a consuming read
        self.acknowledged = []
        self._envelope_ids = itertools.count(1)
        self.reads = 0

    def fingerprint(self):
        """Every piece of state a read could change: rows, markers, delivery and acks."""
        return json.dumps(
            {
                "rows": self.rows,
                "delivery": self.delivery,
                "acknowledged": self.acknowledged,
            },
            sort_keys=True,
        )

    def __call__(self, argv, timeout):
        tail = list(argv[1:])
        for token in CONSUMING_TOKENS:
            assert token not in tail, f"{token} reached the backend: {tail}"
        if tail[:5] != QUESTION_BASE:
            assert tail[:3] == ["orchestration", "worker-list", "--json"], tail
            assert "check" not in tail  # plain check would consume a delivery
            return 0, json.dumps(make_envelope(make_rows(2, 1), total=2))
        assert tail[5:] == ["--run", QRUN, "--json"], tail
        self.reads += 1
        if self.consuming:  # the behaviour the test must be able to detect
            self.delivery = f"delivery_{self.reads}"
            for row in self.rows:
                row["delivered_at"] = "2026-11-11T20:01:30Z"
        envelope = {
            "id": f"env-{next(self._envelope_ids)}",  # differs per call, like the real one
            "ok": True,
            "result": {
                "acknowledged": None,
                "count": len(self.rows),
                "messages": copy.deepcopy(self.rows),
                "runId": QRUN,
            },
            "_meta": {"runtimeId": "redacted"},
        }
        return 0, json.dumps(envelope)

    def send(self, rows):
        """A sender writes new questions (the scope stops being quiet)."""
        self.rows = [*rows, *self.rows]


def observer_over(backend, clock):
    runner = FakeRunner([], [backend])
    return Collector(
        LiveSource(runner, FakeDiscover([])), clock, run_id=QRUN, questions=True
    )


def observe_quiet_scope(backend, cycles=5):
    """Step one establishes identity; then repeated reads on a quiet scope are compared."""
    clock = FakeClock()
    collector = observer_over(backend, clock)
    first = collector.run_once()
    # Step one: readable identity fields exist before any comparison is made.
    assert first.question_state == "OK" and first.questions.retained > 0
    for row in backend.rows:
        assert row["id"].startswith("msg_") and row["run_id"] == QRUN
        assert isinstance(row["created_at"], str) and row["created_at"]
    for record in first.questions.records:
        assert record.question.qid.startswith("msg_") and record.key[0] == QRUN
        assert isinstance(record.question.created_epoch, float)  # a created time
    baseline = [r.question.qid for r in first.questions.records]
    before = backend.fingerprint()
    seen = []
    for _ in range(cycles):
        clock.advance(15.0)
        result = collector.run_once()
        assert result.question_state == "OK"
        seen.append([r.question.qid for r in result.questions.records])
        assert backend.fingerprint() == before, "the read changed the mailbox state"
    assert all(ids == baseline for ids in seen), "ids or order changed on a quiet scope"
    return baseline


def probe_rows(n=6):
    return make_question_rows(n)  # synthetic rows with the recorded key names


def test_t51_repeated_reads_on_a_quiet_scope_leave_ids_order_and_mailbox_unchanged():
    backend = FakeOrcaMailbox(probe_rows(6))
    ids = observe_quiet_scope(backend, cycles=5)
    assert len(ids) == 6 and ids == sorted(ids)  # oldest created first, stable
    assert (
        backend.reads == 6 and backend.delivery is None and backend.acknowledged == []
    )
    assert PASS_SCOPE.startswith("a pass covers only the visible effects tested")
    assert all(row["delivered_at"] is None for row in backend.rows), PASS_SCOPE


def test_t51_the_observer_never_sends_a_consuming_or_narrowing_argv():
    backend = FakeOrcaMailbox(probe_rows(3))
    log = []

    def spy(argv, timeout):
        log.append(list(argv))
        return backend(argv, timeout)

    clock = FakeClock()
    collector = Collector(
        LiveSource(FakeRunner([], [spy]), FakeDiscover([])),
        clock,
        run_id=QRUN,
        questions=True,
    )
    for _ in range(3):
        collector.run_once()
        clock.advance(15.0)
    messages = [a for a in log if "check" in a]
    assert len(messages) == 3 and all(a[1:6] == QUESTION_BASE for a in messages)
    for argv in log:
        for token in CONSUMING_TOKENS:
            assert token not in argv
    assert all(a.count("check") == 1 and "--all" in a for a in messages)


def test_t51_a_consuming_fake_makes_the_same_check_fail_so_the_test_can_detect_it():
    backend = FakeOrcaMailbox(probe_rows(4))
    backend.consuming = True
    with pytest.raises(AssertionError, match="changed the mailbox state"):
        observe_quiet_scope(backend, cycles=3)
    assert backend.delivery is not None  # the fake really did consume


def test_t51_the_check_is_sensitive_to_a_new_question_so_quiet_means_no_sender_write():
    backend = FakeOrcaMailbox(probe_rows(3))
    clock = FakeClock()
    collector = observer_over(backend, clock)
    before = [r.question.qid for r in collector.run_once().questions.records]
    backend.send(make_question_rows(1, start=10))  # a sender writes: not a quiet scope
    after = [r.question.qid for r in collector.run_once().questions.records]
    assert after != before and set(before) < set(after)


def test_t51_the_backend_refuses_every_consuming_argv_it_could_be_given():
    backend = FakeOrcaMailbox(probe_rows(1))
    bad = [
        ["/o", "orchestration", "check", "--json"],
        ["/o", "orchestration", "check", "--all", "--ack", "d1"],
        ["/o", "orchestration", "check", "--all", "--wait"],
        ["/o", "orchestration", "check", "--peek", "--types", "question"],
    ]
    for argv in bad:
        with pytest.raises(AssertionError):
            backend(argv, 1.0)
    assert backend.reads == 0 and backend.delivery is None
