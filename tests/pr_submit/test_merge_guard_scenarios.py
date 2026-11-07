"""Scenario tests for the merge guard (issue #375) over a real run log and a fake ``gh``.

A small driver plays the part of the protocol (``refs/merge-guard.md``): it reads the
PR with ``scripts/set-draft-state.sh`` against a fake ``gh`` on ``PATH``, decides with
the pure functions of ``superclaude.pr_submit.merge_guard``, appends the guard events
to a real ``RunLog`` in a temporary directory, mutates with the script and settles.
The fake ``gh`` is the only PR: its draft flag, timeline count, head and state are
files, and the driver moves them the way a real push or a person would.

Only ``FakeGh``, its constants and the ``fake_gh`` fixture are imported from
``test_set_draft_state.py``, never a ``test_*`` function (pytest would collect it
twice). No test calls GitHub.
"""

from __future__ import annotations

import re
import shutil

import pytest

from superclaude.pr_submit import merge_guard as mg
from superclaude.pr_submit.fsm import push_idempotency_key
from superclaude.pr_submit.recovery import detect_crash_window, resolve_crash_window
from superclaude.pr_submit.run_log import RunLog
from tests.pr_submit.test_set_draft_state import HEAD, REPO, FakeGh


@pytest.fixture
def fake_gh(tmp_path):
    for tool in ("bash", "jq"):
        if shutil.which(tool) is None:
            pytest.skip(f"{tool} is not on PATH")
    return FakeGh(tmp_path)


PR = 7
TARGET = "b" * 40
BRANCH = "feature"
A = mg.GuardAction


class Guarded:
    """One run of the guard protocol over the fake PR."""

    def __init__(
        self,
        tmp_path,
        gh,
        *,
        mode=mg.GuardMode.DRAFT,
        ordinal=3,
        name="run",
        is_draft=False,
        state="OPEN",
    ):
        self.gh = gh
        self.mode = mode
        self.ordinal = ordinal
        self.log = RunLog(PR, tmp_path / name)
        self.run_id = "run-1"
        self.state = state
        self.head = HEAD
        self.transitions = 0
        self.sync(is_draft=is_draft)  # every run starts from its own fake PR
        self.mark = len(gh.calls())

    # --- the fake PR ---------------------------------------------------------
    def sync(self, is_draft=None):
        self.gh.configure(
            state=self.state,
            is_draft=self.gh.is_draft() if is_draft is None else is_draft,
            head=self.head,
            transitions=self.transitions,
        )

    def calls(self):
        """The fake-``gh`` calls made since this run started."""
        return self.gh.calls()[self.mark :]

    def ready_calls(self):
        """The calls that mark the PR ready: ``pr ready`` without ``--undo``."""
        return [
            c for c in self.calls() if c.startswith("pr ready") and "--undo" not in c
        ]

    def person_toggles(self, to_draft: bool):
        """Someone else flips the draft state: the timeline gains an event."""
        self.transitions += 1
        self.sync(is_draft=to_draft)

    # --- reading -------------------------------------------------------------
    def script(self, *args):
        return self.gh.run("--pr", str(PR), "--repo", REPO, *args)

    @property
    def active(self):
        return self.mode == mg.GuardMode.DRAFT and self.ordinal >= 3

    def read(self):
        run = self.script("--read")
        if run.returncode != 0:
            return mg.GuardRead(ok=False)
        j = run.json
        return mg.GuardRead(
            ok=j["ok"],
            state=j["state"],
            is_draft=j["isDraft"],
            head_sha=j["headRefOid"],
            auto_merge_armed=j["autoMergeRequest"],
            transitions=j["transitions"],
            complete=j["complete"],
        )

    def live_read(self):
        """A read for the decision: inert settings never read the PR."""
        return self.read() if self.active else mg.GuardRead(ok=False)

    def events(self):
        return self.log.read_events()

    def types(self):
        return [e["event_type"] for e in self.events()]

    def guard(self):
        return mg.fold_draft_guard(self.events())

    def of_type(self, event_type):
        return [e for e in self.events() if e["event_type"] == event_type]

    # --- the run log ---------------------------------------------------------
    def append(self, event_type, **fields):
        return self.log.append(
            {"event_type": event_type, "run_id": self.run_id, **fields}
        )

    def key(self, cycle, to):
        earlier = [
            e
            for e in self.of_type("draft_guard_requested")
            if e["cycle_id"] == cycle and e["to"] == to
        ]
        return f"guard:{self.run_id}:{cycle}:{to}:a{len(earlier) + 1}"

    def request(self, cycle, to, first_read=None):
        key = self.key(cycle, to)
        first = {}
        if first_read is not None:
            first = {
                "timeline_baseline": first_read.transitions,
                "original_is_draft": first_read.is_draft,
            }
        self.append(
            "draft_guard_requested",
            cycle_id=cycle,
            to=to,
            idempotency_key=key,
            **first,
        )
        return key

    def settle(self, cycle, to, key, outcome, **fields):
        self.append(
            "draft_guard_settled",
            cycle_id=cycle,
            to=to,
            idempotency_key=key,
            outcome=outcome,
            **fields,
        )

    def mutate(
        self, cycle, to, *, attempts, first_read=None, between=None, settle=True
    ):
        """request -> script -> settle, retried up to ``attempts`` times."""
        for attempt in range(1, attempts + 1):
            key = self.request(cycle, to, first_read if attempt == 1 else None)
            run = self.script("--to", to)
            ok = run.returncode == 0 and run.json["ok"]
            if ok:
                changed = run.json["changed"]
                if changed:
                    self.transitions += 1
                    self.sync()
                if settle:
                    self.settle(cycle, to, key, "confirmed", changed=changed)
                return True
            self.settle(cycle, to, key, "failed", changed=False)
            if between is not None and attempt == 1:
                between()
        return False

    # --- the protocol steps --------------------------------------------------
    def engage(self, cycle):
        guard = self.guard()
        read = self.live_read()
        d = mg.engage_decision(
            mode=self.mode, ordinal=self.ordinal, cycle_id=cycle, guard=guard, read=read
        )
        if d.action == A.ENGAGE:
            first = read if guard is None else None
            if not self.mutate(cycle, "draft", attempts=1, first_read=first):
                self.append("terminal_halted", reason="draft_guard_unavailable")
        elif d.action == A.HALT_UNAVAILABLE:
            self.append("terminal_halted", reason="draft_guard_unavailable")
        elif d.action == A.HALT_PR_NOT_OPEN:
            self.append("terminal_halted", reason="pr_not_open")
        elif d.action in (A.SKIP_ALREADY_DRAFT, A.SKIP_USER_OVERRIDE):
            self.settle(
                cycle,
                "draft",
                None,
                "skipped",
                cause=d.cause,
                original_is_draft=read.is_draft,
                timeline_baseline=read.transitions,
            )
        return d

    def edit(self, cycle):
        if "terminal_halted" not in self.types():
            self.append("fix_applied", cycle_id=cycle)

    def pre_push(self):
        """The Pre-push step: the PR must be OPEN before ``push_decision``."""
        if not self.active:
            return True
        read = self.read()
        if not read.ok or read.state != "OPEN":
            self.append("terminal_halted", reason="pr_not_open")
            return False
        return True

    def push_start(self, cycle):
        self.append("push_decision", cycle_id=cycle)
        key = push_idempotency_key(self.run_id, cycle, HEAD, BRANCH)
        self.append(
            "push_initiated",
            cycle_id=cycle,
            idempotency_key=key,
            pre_push_sha=HEAD,
            target_sha=TARGET,
            target_branch=BRANCH,
            kind="fix",
        )
        return key

    def push_land(self, cycle, key):
        self.head = TARGET
        self.sync()
        self.append(
            "push_completed",
            cycle_id=cycle,
            idempotency_key=key,
            pre_push_sha=HEAD,
            target_sha=TARGET,
            target_branch=BRANCH,
            kind="fix",
        )

    def push(self, cycle):
        self.push_land(cycle, self.push_start(cycle))

    def release(self, cycle, *, applied_edits=1, push_completed=True, between=None):
        guard = self.guard()
        read = self.live_read()
        d = mg.release_decision(
            mode=self.mode,
            ordinal=self.ordinal,
            cycle_id=cycle,
            guard=guard,
            read=read,
            applied_edits=applied_edits,
            target_sha=TARGET,
            push_completed=push_completed,
        )
        if d.action == A.RELEASE:
            self.mutate(cycle, "ready", attempts=2, between=between)
        elif d.action == A.SKIP_USER_OVERRIDE:
            self.settle(cycle, "ready", None, "skipped", cause=d.cause)
        elif d.action == A.HALT_PR_NOT_OPEN:
            self.append("terminal_halted", reason="pr_not_open")
        return d

    def rereview(self, cycle):
        self.append("rereview_requested", cycle_id=cycle, reviewer="augment")

    def status(self):
        halts = [
            e
            for e in self.of_type("terminal_halted")
            if e.get("reason") == "draft_guard_unavailable"
        ]
        if halts:
            return "unavailable"
        return mg.guard_status(self.guard(), self.mode, self.ordinal)

    # --- resume --------------------------------------------------------------
    def resume_inputs(self):
        events = self.events()
        guard = mg.fold_draft_guard(events)
        return {
            "guard": guard,
            "pending": mg.pending_requests(events),
            "published": mg.held_cycle_published(events, guard),
        }

    def decide_resume(self, *, branch=None, applied_edits=1, target_sha=TARGET):
        inputs = self.resume_inputs()
        return mg.resume_decision(
            mode=self.mode,
            ordinal=self.ordinal,
            guard=inputs["guard"],
            read=self.read(),
            pending=inputs["pending"],
            dangling_branch=branch,
            published=inputs["published"],
            applied_edits=applied_edits,
            target_sha=target_sha,
        )

    def reconcile(self, decision):
        request = self.resume_inputs()["pending"][-1]
        cycle, to, key = request["cycle_id"], request["to"], request["idempotency_key"]
        if decision.reason == "resume_reconciled":
            self.settle(cycle, to, key, "confirmed", changed=True, cause=decision.cause)
        elif decision.reason == "not_applied":
            self.settle(cycle, to, key, "skipped", cause=decision.cause)

    def resume_dangling_push(self, remote_reachable, observed=None):
        """Crash recovery over the real run log: detect, resolve, return the branch."""
        dangling = detect_crash_window(self.log)
        assert dangling is not None
        branch, _state = resolve_crash_window(
            self.log,
            dangling,
            remote_reachable=remote_reachable,
            observed_remote_sha=observed,
        )
        return branch, dangling


# --- helpers shared by the assertions ---------------------------------------


def ready_calls(gh):
    """The calls that mark the PR ready: ``pr ready`` without ``--undo``."""
    return [c for c in gh.calls() if c.startswith("pr ready") and "--undo" not in c]


def assert_never_readied(gh):
    """No ``pr ready`` without ``--undo``: the PR is never made ready."""
    assert [c for c in ready_calls(gh) if "--undo" not in c] == []


def assert_scoped(calls):
    """Every fake-``gh`` call names the resolved repo: ``--repo`` or a ``repos/`` path."""
    assert calls
    for call in calls:
        assert f"--repo {REPO}" in call or f"repos/{REPO}/" in call, call


def engaged(tmp_path, gh, cycle="fix-1", name="run", **kw):
    run = Guarded(tmp_path, gh, name=name, **kw)
    assert run.engage(cycle).action == A.ENGAGE
    assert gh.is_draft() is True
    return run


def full_cycle(run, cycle="fix-1"):
    """Engage -> edit -> push -> release -> re-trigger of one fix cycle."""
    run.engage(cycle)
    run.edit(cycle)
    run.push(cycle)
    run.release(cycle)
    run.rereview(cycle)


# --- the twelve tests ---------------------------------------------------------


def test_guard_modes_ordinals_and_resume_authority(fake_gh, tmp_path):
    inert = [
        (mg.GuardMode.DRAFT, 0),
        (mg.GuardMode.DRAFT, 1),
        (mg.GuardMode.DRAFT, 2),
        (mg.GuardMode.OFF, 3),
    ]
    for index, (mode, ordinal) in enumerate(inert):
        run = Guarded(tmp_path, fake_gh, mode=mode, ordinal=ordinal, name=f"i{index}")
        d = run.engage("fix-1")
        assert d.action == A.NOOP and d.reason in ("mode_off", "ordinal")
        assert run.pre_push() is True
        assert run.events() == []
        assert mg.guard_status(run.guard(), mode, ordinal) == "off"
    assert fake_gh.calls() == []  # no call at all, so no `pr ready`
    assert ready_calls(fake_gh) == []

    # A guard held by an earlier run is reported, not touched, below 3 and with off.
    held = engaged(tmp_path, fake_gh, name="held")
    before = len(fake_gh.calls())
    for mode, ordinal in inert:
        held.mode, held.ordinal = mode, ordinal
        d = held.decide_resume()
        assert d.action == A.REPORT_HELD and d.reason == "held_report"
        assert mg.guard_status(held.guard(), mode, ordinal) == "held"
    held.mode, held.ordinal = mg.GuardMode.DRAFT, 3
    assert held.decide_resume().action == A.NOOP
    assert fake_gh.is_draft() is True
    assert [c for c in fake_gh.calls()[before:] if c.startswith("pr ready")] == []

    # A settled guard is not reported as held.
    held.push("fix-1")
    held.release("fix-1")
    held.mode = mg.GuardMode.OFF
    assert held.decide_resume().action == A.NOOP
    assert held.status() == "released"


def test_attach_and_create_preserve_preexisting_draft(fake_gh, tmp_path):
    run = Guarded(tmp_path, fake_gh, is_draft=True)
    d = run.engage("fix-1")
    assert d.action == A.SKIP_ALREADY_DRAFT and d.cause == "already_draft"
    settled = run.of_type("draft_guard_settled")
    assert [(e["outcome"], e["cause"], e["original_is_draft"]) for e in settled] == [
        ("skipped", "already_draft", True)
    ]
    assert run.guard()["phase"] == "disabled"
    assert run.guard()["original_is_draft"] is True
    # Every later step is inert: the PR is never made ready, in this cycle or the next.
    run.edit("fix-1")
    run.push("fix-1")
    assert run.release("fix-1").reason == "not_held"
    assert run.engage("fix-2").reason == "disabled"
    assert run.ready_calls() == []
    assert_never_readied(fake_gh)
    assert fake_gh.is_draft() is True
    assert run.status() == "off"


def test_guard_engages_at_routed_finding_once_per_cycle(fake_gh, tmp_path):
    run = Guarded(tmp_path, fake_gh)
    cycle = mg.fix_cycle_id("fix", mg.next_cycle_number(run.events(), "fix"))
    assert cycle == "fix-1"
    assert run.engage(cycle).action == A.ENGAGE
    requests = run.of_type("draft_guard_requested")
    assert [(e["cycle_id"], e["to"]) for e in requests] == [("fix-1", "draft")]
    assert requests[0]["timeline_baseline"] == 0
    assert requests[0]["original_is_draft"] is False
    # Once per cycle id: the same cycle reaching the end of Wave 3 again does nothing.
    again = run.engage(cycle)
    assert again.action == A.NOOP and again.reason == "already_held"
    assert len(run.of_type("draft_guard_requested")) == 1
    # A conflict cycle never engages, whatever the phase.
    for conflict in ("conflict-1", "sync-1"):
        d = run.engage(conflict)
        assert d.action == A.NOOP and d.reason == "conflict_cycle"

    # After the cycle is released, the next routed finding is the next cycle id; a
    # CI-fix cycle engages with kind ci and its own counter.
    run.edit(cycle)
    run.push(cycle)
    run.release(cycle)
    second = mg.fix_cycle_id("fix", mg.next_cycle_number(run.events(), "fix"))
    assert second == "fix-2"
    assert run.engage(second).action == A.ENGAGE
    run.push(second)
    run.release(second)
    ci = mg.fix_cycle_id("ci", mg.next_cycle_number(run.events(), "ci"))
    assert ci == "ci-1"
    assert run.engage(ci).action == A.ENGAGE
    assert [e["cycle_id"] for e in run.of_type("draft_guard_requested")] == [
        "fix-1",
        "fix-1",
        "fix-2",
        "fix-2",
        "ci-1",
    ]
    # A conflict cycle on a fresh run never engages and logs nothing.
    fresh = Guarded(tmp_path, fake_gh, name="fresh")
    assert fresh.engage("conflict-1").reason == "conflict_cycle"
    assert fresh.events() == []


def test_acceptance_trace_event_order(fake_gh, tmp_path):
    run = Guarded(tmp_path, fake_gh)
    full_cycle(run)
    wanted = {
        "draft_guard_requested",
        "draft_guard_settled",
        "fix_applied",
        "push_completed",
        "rereview_requested",
    }
    trace = [
        (
            e["event_type"],
            e["to"] if e["event_type"] == "draft_guard_requested" else e.get("outcome"),
        )
        for e in RunLog(PR, tmp_path / "run").read_events()
        if e["event_type"] in wanted
    ]
    assert trace == [
        ("draft_guard_requested", "draft"),
        ("draft_guard_settled", "confirmed"),
        ("fix_applied", None),
        ("push_completed", None),
        ("draft_guard_requested", "ready"),
        ("draft_guard_settled", "confirmed"),
        ("rereview_requested", None),
    ]
    types = run.types()
    release_settle = len(types) - 1 - types[::-1].index("draft_guard_settled")
    assert types.index("rereview_requested") > release_settle
    assert "rereview_requested" not in types[:release_settle]
    assert fake_gh.is_draft() is False
    assert run.status() == "released"


def test_guard_releases_only_after_publication_or_zero_edit_proof(fake_gh, tmp_path):
    run = engaged(tmp_path, fake_gh)
    run.edit("fix-1")
    # No completed push: hold. A push whose head is not the target: hold.
    d = run.release("fix-1", push_completed=False)
    assert (d.action, d.reason) == (A.HOLD, "push_not_completed")
    key = run.push_start("fix-1")
    run.push_land("fix-1", key)
    run.head = "c" * 40  # someone pushed on top: the head is no longer the target
    run.sync()
    d = run.release("fix-1")
    assert (d.action, d.reason) == (A.HOLD, "head_mismatch")
    assert fake_gh.is_draft() is True
    assert_never_readied(fake_gh)
    # The head equals the target: released, before any re-trigger.
    run.head = TARGET
    run.sync()
    d = run.release("fix-1")
    assert (d.action, d.reason) == (A.RELEASE, "pushed")
    assert fake_gh.is_draft() is False
    assert "rereview_requested" not in run.types()

    # A zero-edit cycle after a fixing cycle releases with no_edits and no push.
    assert run.engage("fix-2").action == A.ENGAGE
    d = run.release("fix-2", applied_edits=0, push_completed=False)
    assert (d.action, d.reason, d.cause) == (A.RELEASE, "no_edits", "no_edits")
    assert fake_gh.is_draft() is False
    assert run.guard()["phase"] == "released"
    assert run.types().count("push_completed") == 1  # only the first cycle pushed


def test_guard_holds_on_unpublished_or_uncertain_exits(fake_gh, tmp_path):
    def check(name, run):
        # The exit leaves the PR a draft the run owns, and the report says held.
        assert fake_gh.is_draft() is True, name
        assert run.status() == "held", name
        assert run.guard()["owned_draft"] is True, name
        assert run.guard()["phase"] in ("held", "release_pending"), name

    # Validation fails after engage, or the run halts before the push.
    run = engaged(tmp_path, fake_gh, name="validation")
    run.edit("fix-1")
    run.append("terminal_halted", reason="validation_failed")
    check("validation", run)
    assert run.ready_calls() == []

    # The push was rejected: push_initiated with no landing, then a halt.
    rejected = engaged(tmp_path, fake_gh, name="rejected")
    rejected.edit("fix-1")
    rejected.push_start("fix-1")
    rejected.append("terminal_halted", reason="push_rejected")
    check("rejected", rejected)
    assert rejected.ready_calls() == []

    # The push's landing is uncertain: the remote tip is unknown.
    ambiguous = engaged(tmp_path, fake_gh, name="ambiguous")
    ambiguous.edit("fix-1")
    ambiguous.push_start("fix-1")
    branch, _ = ambiguous.resume_dangling_push(None, observed="d" * 40)
    assert branch == "ambiguous"
    check("ambiguous", ambiguous)
    assert ambiguous.ready_calls() == []

    # The release could not be confirmed.
    unconfirmed = engaged(tmp_path, fake_gh, name="unconfirmed")
    unconfirmed.edit("fix-1")
    unconfirmed.push("fix-1")
    fake_gh.flag("fail_ready")
    unconfirmed.release("fix-1")
    fake_gh.flag("fail_ready", False)
    check("unconfirmed", unconfirmed)
    assert len(unconfirmed.ready_calls()) == 2  # the attempt and its one retry failed


def test_guard_engage_failure_blocks_edits(fake_gh, tmp_path):
    # The mutation fails: request, settled(failed), halt, no edit.
    fake_gh.flag("fail_ready")
    run = Guarded(tmp_path, fake_gh)
    run.engage("fix-1")
    run.edit("fix-1")
    types = run.types()
    assert types == [
        "draft_guard_requested",
        "draft_guard_settled",
        "terminal_halted",
    ]
    assert run.of_type("draft_guard_settled")[0]["outcome"] == "failed"
    assert run.of_type("terminal_halted")[0]["reason"] == "draft_guard_unavailable"
    assert "fix_applied" not in types
    assert fake_gh.is_draft() is False
    assert run.status() == "unavailable"

    # The read fails: no request exists, the halt reason still reports unavailable.
    fake_gh.flag("fail_ready", False)
    fake_gh.flag("fail_view")
    unread = Guarded(tmp_path, fake_gh, name="unread")
    d = unread.engage("fix-1")
    assert (d.action, d.reason) == (A.HALT_UNAVAILABLE, "read_failed")
    unread.edit("fix-1")
    assert unread.types() == ["terminal_halted"]
    assert unread.guard() is None
    assert mg.guard_status(unread.guard(), unread.mode, unread.ordinal) == "released"
    assert unread.status() == "unavailable"
    fake_gh.flag("fail_view", False)

    # The timeline is unreadable at engage: halt before any edit as well.
    fake_gh.flag("fail_timeline")
    blind = Guarded(tmp_path, fake_gh, name="blind")
    d = blind.engage("fix-1")
    assert (d.action, d.reason) == (A.HALT_UNAVAILABLE, "timeline_unreadable")
    blind.edit("fix-1")
    assert "fix_applied" not in blind.types()
    assert blind.status() == "unavailable"
    assert fake_gh.is_draft() is False


def test_guard_release_failure_retries_once_and_reports(fake_gh, tmp_path):
    # Attempt 1 fails; before attempt 2 a person marks the PR ready: the script answers
    # changed false, which counts as confirmed.
    run = engaged(tmp_path, fake_gh)
    run.edit("fix-1")
    run.push("fix-1")
    fake_gh.flag("fail_ready")

    def person_readies():
        fake_gh.flag("fail_ready", False)
        run.person_toggles(False)

    run.release("fix-1", between=person_readies)
    keys = [e["idempotency_key"] for e in run.of_type("draft_guard_requested")]
    assert [k.rsplit(":", 1)[1] for k in keys if ":ready:" in k] == ["a1", "a2"]
    settles = run.of_type("draft_guard_settled")
    assert [(e["to"], e["outcome"]) for e in settles][1:] == [
        ("ready", "failed"),
        ("ready", "confirmed"),
    ]
    assert settles[-1]["changed"] is False
    assert run.guard()["phase"] == "released"
    assert run.status() == "released"

    # Both attempts fail: one retry only, the draft is still owned and reported held.
    fake_gh.flag("fail_ready", False)
    stuck = engaged(tmp_path, fake_gh, name="stuck")
    stuck.edit("fix-1")
    stuck.push("fix-1")
    fake_gh.flag("fail_ready")
    stuck.release("fix-1")
    ready_requests = [
        e for e in stuck.of_type("draft_guard_requested") if e["to"] == "ready"
    ]
    assert len(ready_requests) == 2
    guard = stuck.guard()
    assert guard["phase"] == "release_pending" and guard["owned_draft"] is True
    assert guard["failed_mutations"] == 2
    assert stuck.status() == "held"
    assert fake_gh.is_draft() is True
    # The next checkpoint retries the release instead of engaging again.
    fake_gh.flag("fail_ready", False)
    d = stuck.engage("fix-2")
    assert d.action == A.RETRY_RELEASE


def test_guard_external_toggle_and_roundtrip_disable(fake_gh, tmp_path):
    # A person marks the PR ready and then a draft again while it is held: the draft
    # flag looks as expected, but the timeline shows more transitions than the run made.
    run = engaged(tmp_path, fake_gh)
    run.edit("fix-1")
    run.person_toggles(False)
    run.person_toggles(True)
    assert fake_gh.is_draft() is True
    run.push("fix-1")
    d = run.release("fix-1")
    assert (d.action, d.reason, d.cause) == (
        A.SKIP_USER_OVERRIDE,
        "user_override",
        "user_override",
    )
    assert run.guard()["phase"] == "disabled"
    assert run.guard()["disabled_cause"] == "user_override"
    assert run.status() == "user_override"
    # The run continues: the push stayed, and the guard makes no more draft calls.
    run.rereview("fix-1")
    assert run.types()[-2:] == ["draft_guard_settled", "rereview_requested"]
    assert run.engage("fix-2").reason == "disabled"
    assert run.release("fix-2").reason == "not_held"
    assert run.ready_calls() == []
    assert fake_gh.is_draft() is True  # the person's state is left alone

    # A person readies the held PR once: the flag no longer matches the held phase.
    ready = engaged(tmp_path, fake_gh, name="ready")
    ready.person_toggles(False)
    d = ready.release("fix-1")
    assert d.action == A.SKIP_USER_OVERRIDE

    # Slack: a failed mutation of the run itself is not foreign.
    slack = engaged(tmp_path, fake_gh, name="slack")
    guard = dict(slack.guard(), failed_mutations=1)
    read = mg.GuardRead(
        ok=True,
        state="OPEN",
        is_draft=True,
        head_sha=HEAD,
        transitions=2,
        complete=True,
    )
    assert mg.classify_toggles(guard, read) == "ok"
    far = mg.GuardRead(
        ok=True,
        state="OPEN",
        is_draft=True,
        head_sha=HEAD,
        transitions=3,
        complete=True,
    )
    assert mg.classify_toggles(guard, far) == "foreign"


def test_guard_missing_timeline_or_ambiguous_intent_never_readies(fake_gh, tmp_path):
    run = engaged(tmp_path, fake_gh)
    run.edit("fix-1")
    run.push("fix-1")
    # The timeline call fails: the read is incomplete, the guard holds.
    fake_gh.flag("fail_timeline")
    d = run.release("fix-1")
    assert (d.action, d.reason) == (A.HOLD, "timeline_unreadable")
    fake_gh.flag("fail_timeline", False)
    # The timeline is shorter than the run's own transitions: events are missing.
    run.transitions = 0
    run.sync()
    d = run.release("fix-1")
    assert (d.action, d.reason) == (A.HOLD, "timeline_unreadable")
    assert fake_gh.is_draft() is True
    assert run.ready_calls() == []

    # Resume with an unsettled ready request whose live state fits neither outcome.
    pending = engaged(tmp_path, fake_gh, name="pending")
    pending.push("fix-1")
    pending.request("fix-1", "ready")
    pending.person_toggles(True)  # an extra transition: observed is run_toggles + 1
    d = pending.decide_resume()
    assert (d.action, d.reason) == (A.RECONCILE, "ambiguous")
    pending.reconcile(d)  # ambiguous: no settle and no mutation
    assert len(pending.of_type("draft_guard_settled")) == 1
    assert pending.guard()["phase"] == "release_pending"
    assert pending.ready_calls() == []
    assert fake_gh.is_draft() is True


def test_guard_crash_boundaries_and_push_recovery_abc(fake_gh, tmp_path):
    # (a) Crash after request(draft), before the mutation: the live PR is not a draft.
    a = Guarded(tmp_path, fake_gh, name="a")
    a.request("fix-1", "draft", first_read=a.read())
    d = a.decide_resume()
    assert (d.action, d.reason, d.cause) == (A.RECONCILE, "not_applied", "not_applied")
    a.reconcile(d)
    assert a.guard() is None  # the first record never took effect
    assert a.engage("fix-1").action == A.ENGAGE  # the next cycle engages normally
    assert a.guard()["phase"] == "held"
    assert len(a.of_type("draft_guard_requested")) == 2

    # (b) Crash after the mutation, before the settle: the live PR is a draft.
    fake_gh.configure()
    b = Guarded(tmp_path, fake_gh, name="b")
    b.request("fix-1", "draft", first_read=b.read())
    assert b.script("--to", "draft").json["changed"] is True
    b.transitions += 1
    b.sync()
    d = b.decide_resume()
    assert (d.action, d.reason) == (A.RECONCILE, "resume_reconciled")
    b.reconcile(d)
    assert b.guard()["phase"] == "held" and b.guard()["run_toggles"] == 1
    assert b.engage("fix-1").reason == "already_held"

    # (c) A ready request settled not_applied stays HELD and is released after the
    # publication check (the push completed normally before the crash).
    fake_gh.configure()
    c = engaged(tmp_path, fake_gh, name="c")
    c.edit("fix-1")
    c.push("fix-1")
    c.request("fix-1", "ready")  # crash before the mutation
    d = c.decide_resume()
    assert (d.action, d.reason) == (A.RECONCILE, "not_applied")
    c.reconcile(d)
    assert c.guard()["phase"] == "held"
    d = c.decide_resume()
    assert (d.action, d.reason) == (A.RELEASE, "pushed")
    c.release("fix-1")
    assert c.guard()["phase"] == "released" and fake_gh.is_draft() is False

    # (d) A dangling push_initiated resolved by the real crash recovery, never by a
    # hand-written branch string.
    expected = {
        True: ("landed", A.RELEASE, "pushed"),
        False: ("not_landed", A.NOOP, "held_through_redrive"),
        None: ("ambiguous", A.HOLD, "ambiguous_remote_tip"),
    }
    for index, (reachable, (branch, action, reason)) in enumerate(expected.items()):
        fake_gh.configure()
        run = engaged(tmp_path, fake_gh, name=f"d{index}")
        run.edit("fix-1")
        run.push_start("fix-1")
        if reachable is True:
            run.head = TARGET  # the push landed on the remote and the PR head
            run.sync()
        dangling = detect_crash_window(run.log)
        assert dangling and dangling["target_sha"] == TARGET
        got, _ = run.resume_dangling_push(reachable, observed="e" * 40)
        assert got == branch
        d = run.decide_resume(branch=got, target_sha=dangling["target_sha"])
        assert (d.action, d.reason) == (action, reason), branch
        if d.action == A.RELEASE:
            # Recovery synthesized push_completed, so a later resume also sees published.
            assert run.resume_inputs()["published"] is True
            run.release("fix-1")
            assert fake_gh.is_draft() is False
            assert len(run.ready_calls()) == 1
        else:
            assert fake_gh.is_draft() is True
            assert run.ready_calls() == []

    # (e) Crash after a normal push_completed, before the release: no dangling window.
    fake_gh.configure()
    e = engaged(tmp_path, fake_gh, name="e")
    e.edit("fix-1")
    e.push("fix-1")
    assert detect_crash_window(e.log) is None
    inputs = e.resume_inputs()
    assert inputs["published"] is True
    d = e.decide_resume(branch=None)
    assert (d.action, d.reason) == (A.RELEASE, "pushed")
    e.release("fix-1")
    e.rereview("fix-1")  # the S5a logic runs only after the release
    types = e.types()
    assert types.index("rereview_requested") > max(
        i for i, t in enumerate(types) if t == "draft_guard_settled"
    )
    assert fake_gh.is_draft() is False

    # (f) Engage, crash, resume with the live draft true: held, never disabled.
    fake_gh.configure()
    f = engaged(tmp_path, fake_gh, name="f")
    assert f.read().is_draft is True
    assert f.engage("fix-1").reason == "already_held"  # not SKIP_ALREADY_DRAFT
    assert f.guard()["phase"] == "held"
    assert f.decide_resume().action == A.NOOP
    f.edit("fix-1")
    f.push("fix-1")
    f.release("fix-1")
    assert f.guard()["phase"] == "released" and fake_gh.is_draft() is False


def test_guard_closed_merged_or_moved_head_forbids_mutation(fake_gh, tmp_path):
    # A PR merged while held: the next checkpoint halts, nothing is pushed.
    run = engaged(tmp_path, fake_gh)
    run.edit("fix-1")
    run.state = "MERGED"
    run.sync()
    assert run.pre_push() is False
    halt = run.of_type("terminal_halted")[0]
    assert halt["reason"] == "pr_not_open"
    index = run.events().index(halt)
    after = [e["event_type"] for e in run.events()[index + 1 :]]
    assert "push_initiated" not in after and "push_completed" not in after
    assert "push_decision" not in run.types()
    d = run.release("fix-1", applied_edits=0, push_completed=False)
    assert (d.action, d.reason) == (A.HALT_PR_NOT_OPEN, "pr_not_open")
    assert run.guard()["phase"] == "held"
    assert fake_gh.is_draft() is True
    assert run.ready_calls() == []

    # The Pre-push check applies whatever the phase is, a disabled guard included.
    disabled = Guarded(tmp_path, fake_gh, name="disabled", is_draft=True)
    disabled.engage("fix-1")
    assert disabled.guard()["phase"] == "disabled"
    disabled.state = "CLOSED"
    disabled.sync()
    assert disabled.pre_push() is False
    assert disabled.of_type("terminal_halted")[0]["reason"] == "pr_not_open"
    assert "push_initiated" not in disabled.types()

    # Engage on a closed PR halts too, and a moved head holds the release.
    closed = Guarded(tmp_path, fake_gh, name="closed", state="CLOSED")
    d = closed.engage("fix-1")
    assert (d.action, d.reason) == (A.HALT_PR_NOT_OPEN, "pr_not_open")
    assert closed.of_type("draft_guard_requested") == []

    fake_gh.configure()
    moved = engaged(tmp_path, fake_gh, name="moved")
    moved.edit("fix-1")
    moved.push("fix-1")
    moved.head = "f" * 40
    moved.sync()
    d = moved.release("fix-1")
    assert (d.action, d.reason) == (A.HOLD, "head_mismatch")
    assert moved.ready_calls() == []
    assert fake_gh.is_draft() is True


def test_guard_script_contract_scoping_and_legacy_fold(fake_gh, tmp_path):
    # Exit codes: 0 read, 1 for a PR that is not open, 2 usage, 127 missing tool.
    run = Guarded(tmp_path, fake_gh)
    assert run.script("--read").returncode == 0
    full_cycle(run)
    assert_scoped(fake_gh.calls())
    fake_gh.configure(state="MERGED")
    merged = run.script("--to", "ready")
    assert merged.returncode == 1 and merged.json["error"] == "not_open"
    assert fake_gh.run().returncode == 2
    assert fake_gh.run("--pr", "7", "--bogus").returncode == 2
    path = fake_gh.restricted_path(tmp_path, with_gh=False, with_jq=True)
    assert (
        fake_gh.run("--pr", "7", "--repo", REPO, "--read", path=path).returncode == 127
    )
    # The calls of the failing runs are scoped as well.
    assert_scoped(fake_gh.calls())

    # An old log, with no guard event, folds to draft_guard None.
    legacy = RunLog(PR, tmp_path / "legacy")
    for event_type in ("poll_result", "review_detected", "push_completed"):
        legacy.append({"event_type": event_type, "run_id": "old", "cycle_id": "c1"})
    assert legacy.rebuild_state()["draft_guard"] is None
    assert mg.fold_draft_guard(legacy.read_events()) is None
    assert mg.guard_status(None, mg.GuardMode.DRAFT, 3) == "released"
    assert mg.guard_status(None, mg.GuardMode.DRAFT, 2) == "off"
    # A new log folds the same way through RunLog and through the pure fold.
    new = Guarded(tmp_path, fake_gh, name="new")
    fake_gh.configure()
    new.engage("fix-1")
    assert new.log.rebuild_state()["draft_guard"] == mg.fold_draft_guard(new.events())
    assert re.fullmatch(r"fix-[0-9]+", new.guard()["cycle_id"])
