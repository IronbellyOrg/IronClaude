"""Pure decision core for the ``sc:pr-submit`` merge guard (issue #375).

The guard turns a pull request into a draft when a verified Medium-or-higher
review finding is routed to a fix, and marks it ready again only once that
cycle's fix push is confirmed on the PR head (or a zero-edit cycle is proven).

This module only DECIDES. It does no I/O: the protocol (``SKILL.md`` and
``refs/merge-guard.md``) reads the PR through ``scripts/set-draft-state.sh``,
calls these functions, appends the run-log events and performs the mutation.
That is the same split as the push triad and the re-trigger (NFR-6).

Core-purity (NFR-6 / AC-9): this module imports only ``enum``, ``dataclasses``,
``re`` and ``is_conflict_cycle`` from ``.conflicts``, and contains no
version-control or hosting command word on any line.

Guard state is the plain dict returned by :func:`fold_draft_guard` (or ``None``
when the run log holds no guard record); decisions read it with ``.get`` so a
hand-built dict works the same way.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from .conflicts import is_conflict_cycle

# Event names of the two guard events (the members of ``EventType`` carry the
# same values; a test pins the equality because this module cannot import them).
REQUESTED = "draft_guard_requested"
SETTLED = "draft_guard_settled"

# The strings crash recovery returns for a dangling push (see ``recovery.py``).
# ``recovery`` imports ``run_log``, which imports this module, so the values are
# repeated here and a test asserts they equal the ``recovery`` constants.
BRANCH_LANDED = "landed"
BRANCH_NOT_LANDED = "not_landed"
BRANCH_AMBIGUOUS = "ambiguous"

_CYCLE_KINDS = ("fix", "ci")
_MIN_ORDINAL = 3  # the guard acts only at --monitor 3


class GuardMode(str, Enum):
    """The ``--merge-guard`` flag values. ``off`` makes the guard inert."""

    DRAFT = "draft"
    OFF = "off"


class Direction(str, Enum):
    """The target state of one draft/ready mutation."""

    DRAFT = "draft"
    READY = "ready"


class Phase(str, Enum):
    """Folded guard phases. These are fold values, not ``MonitorState`` members."""

    ENGAGE_PENDING = "engage_pending"
    HELD = "held"
    RELEASE_PENDING = "release_pending"
    RELEASED = "released"
    DISABLED = "disabled"


class GuardAction(str, Enum):
    """What the protocol must do next."""

    NOOP = "noop"
    ENGAGE = "engage"
    RELEASE = "release"
    RETRY_RELEASE = "retry_release"
    REBIND = "rebind"
    HOLD = "hold"
    REPORT_HELD = "report_held"
    SKIP_ALREADY_DRAFT = "skip_already_draft"
    SKIP_USER_OVERRIDE = "skip_user_override"
    RECONCILE = "reconcile"
    HALT_PR_NOT_OPEN = "halt_pr_not_open"
    HALT_UNAVAILABLE = "halt_unavailable"


@dataclass(frozen=True)
class GuardRead:
    """Parsed output of the read mode of ``scripts/set-draft-state.sh``."""

    ok: bool
    state: str | None = None
    is_draft: bool | None = None
    head_sha: str | None = None
    auto_merge_armed: bool = False
    transitions: int | None = None
    complete: bool = False


@dataclass(frozen=True)
class GuardDecision:
    """One decision: the action, why, the settle cause it implies, and notes."""

    action: GuardAction
    reason: str
    cause: str | None = None
    notes: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Cycle identity
# ---------------------------------------------------------------------------


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def fix_cycle_id(kind: str, n: int) -> str:
    """``"fix-<n>"`` for kind ``fix``, ``"ci-<n>"`` for kind ``ci``.

    Raises ``ValueError`` for any other kind or when ``n < 1``. The two prefixes
    never collide with the reserved conflict-cycle prefixes.
    """
    if kind not in _CYCLE_KINDS:
        raise ValueError("cycle kind must be 'fix' or 'ci'")
    if not (_is_int(n) and n >= 1):
        raise ValueError("cycle number must be an int >= 1")
    return f"{kind}-{n}"


def next_cycle_number(events: object, kind: str) -> int:
    """1 + the highest ``<kind>-<n>`` seen in any event's ``cycle_id``; 1 when none."""
    if kind not in _CYCLE_KINDS:
        raise ValueError("cycle kind must be 'fix' or 'ci'")
    pattern = re.compile(rf"^{kind}-([0-9]+)$")
    highest = 0
    for event in _iter_events(events):
        cycle_id = event.get("cycle_id")
        if isinstance(cycle_id, str):
            match = pattern.match(cycle_id)
            if match:
                highest = max(highest, int(match.group(1)))
    return highest + 1


def _iter_events(events: object):
    if not isinstance(events, (list, tuple)):
        return
    for event in events:
        if isinstance(event, dict):
            yield event


# ---------------------------------------------------------------------------
# Fold of the two guard events
# ---------------------------------------------------------------------------


def _new_record(cycle_id: object, baseline: object, original_is_draft: object) -> dict:
    return {
        "phase": Phase.ENGAGE_PENDING.value,
        "phase_before_request": None,
        "cycle_id": cycle_id,
        "original_is_draft": original_is_draft,
        "baseline": baseline,
        "run_toggles": 0,
        "unsettled": 0,
        "failed_mutations": 0,
        "owned_draft": False,
        "disabled_cause": None,
    }


def fold_draft_guard(events: object) -> dict | None:
    """Fold the guard events into the ``draft_guard`` state, or ``None`` when absent.

    Fields: ``phase``, ``phase_before_request``, ``cycle_id``,
    ``original_is_draft``, ``baseline``, ``run_toggles``, ``unsettled``,
    ``failed_mutations``, ``owned_draft``, ``disabled_cause``.

    ``original_is_draft`` and ``baseline`` come only from the first guard record
    (a first request, or a first skip), never from a later read. A settled
    ``not_applied`` request of either direction clears its key and returns the
    phase to the one before the request; when that request was the first guard
    record the whole record is erased, so the next request is a first request
    again. Every other ``skipped`` settle copies the event's ``cause`` into
    ``disabled_cause``.
    """
    record: dict | None = None
    pending: dict[str, str | None] = {}  # key -> phase before that request
    failed_open: dict[tuple, int] = {}  # (cycle, direction) -> failed, not yet resolved
    for event in _iter_events(events):
        event_type = event.get("event_type")
        if event_type == REQUESTED:
            record = _fold_requested(record, pending, event)
        elif event_type == SETTLED:
            record = _fold_settled(record, pending, event, failed_open)
    if record is not None:
        record["unsettled"] = len(pending)
    return record


def _fold_requested(record: dict | None, pending: dict, event: dict) -> dict:
    to = event.get("to")
    key = event.get("idempotency_key")
    if record is None:
        record = _new_record(
            event.get("cycle_id"),
            event.get("timeline_baseline"),
            event.get("original_is_draft"),
        )
        before = None
    else:
        before = record["phase"]
        record["phase_before_request"] = before
        record["cycle_id"] = event.get("cycle_id", record["cycle_id"])
    record["phase"] = (
        Phase.ENGAGE_PENDING.value
        if to == Direction.DRAFT.value
        else Phase.RELEASE_PENDING.value
    )
    if before is None:
        record["phase_before_request"] = None
    if isinstance(key, str):
        pending[key] = before
    return record


def _fold_settled(
    record: dict | None, pending: dict, event: dict, failed_open: dict
) -> dict | None:
    key = event.get("idempotency_key")
    had_request = isinstance(key, str) and key in pending
    before = pending.pop(key, None) if had_request else None
    outcome = event.get("outcome")
    cause = event.get("cause")
    to = event.get("to")
    changed = bool(event.get("changed"))

    if outcome == "skipped":
        if cause == "not_applied":
            if record is None or not had_request:
                return record  # nothing pending to undo
            if before is None:
                return None  # the first guard record never took effect
            record["phase"] = before
            return record
        if record is None:
            record = _new_record(
                event.get("cycle_id"),
                event.get("timeline_baseline"),
                event.get("original_is_draft"),
            )
        record["phase"] = Phase.DISABLED.value
        record["owned_draft"] = False
        record["disabled_cause"] = cause
        return record

    if record is None:
        return None
    scope = (event.get("cycle_id"), to)
    if outcome == "failed":
        record["phase"] = Phase.RELEASE_PENDING.value
        record["failed_mutations"] += 1
        failed_open[scope] = failed_open.get(scope, 0) + 1
        return record
    if outcome == "confirmed":
        if to == Direction.DRAFT.value:
            record["phase"] = Phase.HELD.value
            record["owned_draft"] = True
        else:
            record["phase"] = Phase.RELEASED.value
            record["owned_draft"] = False
        if isinstance(event.get("cycle_id"), str):
            record["cycle_id"] = event["cycle_id"]  # a re-bound held guard follows it
        if changed:
            record["run_toggles"] += 1
        # A later confirmed settle of the same cycle and direction resolves the earlier
        # failed attempts: `changed` true means they changed nothing; `changed` false
        # means the PR was already in the target state, so one of them landed.
        resolved = failed_open.pop(scope, 0)
        if resolved:
            record["failed_mutations"] -= resolved
            if not changed:
                record["run_toggles"] += 1
    return record


def pending_requests(events: object) -> list[dict]:
    """Guard requests with no matching settle, matched by ``idempotency_key``.

    The guard keeps its own crash window: ``recovery.py`` pairs only the push
    events. A retry carries a different ``:a<k>`` key suffix, so it is its own
    request.
    """
    requests: dict[str, dict] = {}
    for event in _iter_events(events):
        event_type = event.get("event_type")
        key = event.get("idempotency_key")
        if not isinstance(key, str):
            continue
        if event_type == REQUESTED:
            requests[key] = event
        elif event_type == SETTLED:
            requests.pop(key, None)
    return list(requests.values())


def held_cycle_published(events: object, guard: dict | None) -> bool:
    """True when the held cycle's push completed, normally or by recovery."""
    if not guard:
        return False
    cycle_id = guard.get("cycle_id")
    if not isinstance(cycle_id, str):
        return False
    return any(
        event.get("event_type") == "push_completed"
        and event.get("cycle_id") == cycle_id
        for event in _iter_events(events)
    )


# ---------------------------------------------------------------------------
# Status mapping
# ---------------------------------------------------------------------------


def _phase(guard: dict | None) -> str | None:
    if not guard:
        return None
    phase = guard.get("phase")
    return phase.value if isinstance(phase, Phase) else phase


def _is_off(mode: object, ordinal: object) -> bool:
    return mode == GuardMode.OFF or not (_is_int(ordinal) and ordinal >= _MIN_ORDINAL)


def guard_status(guard: dict | None, mode: object, ordinal: object) -> str:
    """The ``merge_guard`` output field: first match wins.

    ``off``, ``released``, ``held``, ``user_override`` or ``unavailable``.
    """
    if guard is None and _is_off(mode, ordinal):
        return "off"
    if guard is None:
        return "released"
    phase = _phase(guard)
    if phase == Phase.HELD.value:
        return "held"
    if phase in (Phase.ENGAGE_PENDING.value, Phase.RELEASE_PENDING.value):
        return "held" if guard.get("owned_draft") else "unavailable"
    if phase == Phase.DISABLED.value:
        cause = guard.get("disabled_cause")
        if cause == "user_override":
            return "user_override"
        if cause == "already_draft":
            return "off"
        return "unavailable"
    if phase == Phase.RELEASED.value:
        return "released"
    return "unavailable"


# ---------------------------------------------------------------------------
# Toggle classification
# ---------------------------------------------------------------------------


def classify_toggles(guard: dict | None, read: GuardRead) -> str:
    """``"ok"``, ``"foreign"`` or ``"unreadable"``: the only foreign-toggle test.

    No actor identity is used (one login serves the human and the agent): the
    count of draft/ready transitions on the timeline is compared with the count
    the guard itself made, with slack for calls that failed or were never settled.
    """
    if (
        not read.ok
        or not read.complete
        or read.transitions is None
        or read.is_draft is None
        or not guard
        or not _is_int(guard.get("baseline"))
    ):
        return "unreadable"
    observed = read.transitions - guard["baseline"]
    run_toggles = guard.get("run_toggles", 0)
    slack = guard.get("unsettled", 0) + guard.get("failed_mutations", 0)
    if observed < run_toggles:
        return "unreadable"  # events are missing from the timeline
    if observed > run_toggles + slack:
        return "foreign"
    expected = {Phase.HELD.value: True, Phase.RELEASED.value: False}.get(_phase(guard))
    if expected is not None and read.is_draft != expected:
        return "foreign"
    return "ok"


# ---------------------------------------------------------------------------
# Decisions
# ---------------------------------------------------------------------------


def _inert(mode: object, ordinal: object, cycle_id: object) -> str | None:
    if mode == GuardMode.OFF:
        return "mode_off"
    if not (_is_int(ordinal) and ordinal >= _MIN_ORDINAL):
        return "ordinal"
    if is_conflict_cycle(cycle_id):
        return "conflict_cycle"
    return None


def engage_decision(
    *,
    mode: object,
    ordinal: object,
    cycle_id: object,
    guard: dict | None,
    read: GuardRead,
) -> GuardDecision:
    """Decide whether to make the PR a draft: first matching row wins."""
    inert = _inert(mode, ordinal, cycle_id)
    if inert:  # row 1
        return GuardDecision(GuardAction.NOOP, inert)
    phase = _phase(guard)
    if phase == Phase.DISABLED.value:  # row 2
        return GuardDecision(GuardAction.NOOP, "disabled")
    if not read.ok:  # row 3
        return GuardDecision(GuardAction.HALT_UNAVAILABLE, "read_failed")
    if read.state != "OPEN":  # row 4
        return GuardDecision(GuardAction.HALT_PR_NOT_OPEN, "pr_not_open")
    if phase == Phase.RELEASE_PENDING.value:
        if guard.get("owned_draft"):  # row 5
            return GuardDecision(GuardAction.RETRY_RELEASE, "release_pending")
        return GuardDecision(GuardAction.HOLD, "ownership_unproven")  # row 6
    if phase == Phase.HELD.value:  # row 7
        held_cycle = guard.get("cycle_id")
        if held_cycle not in (None, cycle_id):
            # A later cycle reuses the held draft: the guard must follow it, or resume
            # would judge the release against the earlier cycle's push.
            return GuardDecision(GuardAction.REBIND, "cycle_rebound")
        return GuardDecision(GuardAction.NOOP, "already_held")
    if not read.complete or read.transitions is None:  # row 8
        return GuardDecision(GuardAction.HALT_UNAVAILABLE, "timeline_unreadable")
    if guard and classify_toggles(guard, read) == "foreign":  # row 9
        return GuardDecision(
            GuardAction.SKIP_USER_OVERRIDE, "user_override", cause="user_override"
        )
    if guard is None and read.is_draft:  # row 10
        return GuardDecision(
            GuardAction.SKIP_ALREADY_DRAFT, "already_draft", cause="already_draft"
        )
    notes = ("auto_merge_armed",) if read.auto_merge_armed else ()  # row 11
    return GuardDecision(GuardAction.ENGAGE, "engage", notes=notes)


def release_decision(
    *,
    mode: object,
    ordinal: object,
    cycle_id: object,
    guard: dict | None,
    read: GuardRead,
    applied_edits: int,
    target_sha: str | None,
    push_completed: bool,
) -> GuardDecision:
    """Decide whether to mark the PR ready again: first matching row wins.

    ``applied_edits`` is THIS cycle's count of applied edits, not the run-wide
    output field, so a zero-edit cycle after a fixing cycle still releases with
    cause ``no_edits``.
    """
    inert = _inert(mode, ordinal, cycle_id)
    if inert:  # row 1
        return GuardDecision(GuardAction.NOOP, inert)
    phase = _phase(guard)
    if phase not in (Phase.HELD.value, Phase.RELEASE_PENDING.value):  # row 2
        return GuardDecision(GuardAction.NOOP, "not_held")
    if not read.ok:  # row 3
        return GuardDecision(GuardAction.HOLD, "read_failed")
    if read.state != "OPEN":  # row 4
        return GuardDecision(GuardAction.HALT_PR_NOT_OPEN, "pr_not_open")
    verdict = classify_toggles(guard, read)
    if verdict == "unreadable":  # row 5
        return GuardDecision(GuardAction.HOLD, "timeline_unreadable")
    if verdict == "foreign":  # row 6
        return GuardDecision(
            GuardAction.SKIP_USER_OVERRIDE, "user_override", cause="user_override"
        )
    if applied_edits == 0:  # row 7
        return GuardDecision(GuardAction.RELEASE, "no_edits", cause="no_edits")
    if push_completed and target_sha is not None and read.head_sha == target_sha:
        return GuardDecision(GuardAction.RELEASE, "pushed", cause="pushed")  # row 8
    reason = "head_mismatch" if push_completed else "push_not_completed"
    return GuardDecision(GuardAction.HOLD, reason)  # row 9


def _reconcile(guard: dict, read: GuardRead | None, pending: list) -> GuardDecision:
    """Resume row 3: settle the last unsettled request from the live state."""
    request = pending[-1]
    if (
        read is None
        or classify_toggles(guard, read) in ("unreadable", "foreign")
        or read.transitions is None
    ):
        return GuardDecision(GuardAction.RECONCILE, "ambiguous")
    observed = read.transitions - guard["baseline"]
    run_toggles = guard.get("run_toggles", 0)
    # `failed_mutations` counts only failed attempts that no later settle of the same cycle
    # and direction resolved (the fold folds a landed one into `run_toggles`), so up to that
    # many transitions may have happened without being counted. The live state decides; the
    # count only has to fit that allowance. A person's single toggle in the request's own
    # direction cannot be told from the request, so it reconciles as applied.
    uncertain = guard.get("failed_mutations", 0)
    wants_draft = request.get("to") == Direction.DRAFT.value
    matches = read.is_draft is wants_draft
    if matches and run_toggles + 1 <= observed <= run_toggles + 1 + uncertain:
        return GuardDecision(
            GuardAction.RECONCILE, "resume_reconciled", cause="resume_reconciled"
        )
    if not matches and run_toggles <= observed <= run_toggles + uncertain:
        return GuardDecision(GuardAction.RECONCILE, "not_applied", cause="not_applied")
    return GuardDecision(GuardAction.RECONCILE, "ambiguous")


def resume_decision(
    *,
    mode: object,
    ordinal: object,
    guard: dict | None,
    read: GuardRead | None,
    pending: list,
    dangling_branch: str | None,
    published: bool,
    applied_edits: int = 1,
    target_sha: str | None = None,
    cycle_id: object = None,
) -> GuardDecision:
    """Decide what ``--resume`` does about the guard: first matching row wins.

    ``dangling_branch`` is ``None`` or a ``BRANCH_*`` constant; ``published`` is
    :func:`held_cycle_published` (a push that completed normally before the
    crash leaves no dangling window). Row 4 re-enters :func:`release_decision`
    with ``push_completed=True``; the held cycle has pushed, so at least one edit
    counts, and with no ``target_sha`` the head proof cannot succeed and the
    guard holds.
    """
    if not guard:  # row 1
        return GuardDecision(GuardAction.NOOP, "no_guard")
    phase = _phase(guard)
    settled_phases = (Phase.RELEASED.value, Phase.DISABLED.value)
    if (not _is_int(ordinal) or ordinal < _MIN_ORDINAL or mode == GuardMode.OFF) and (
        phase not in settled_phases
    ):  # row 2
        return GuardDecision(GuardAction.REPORT_HELD, "held_report")
    if pending:  # row 3
        return _reconcile(guard, read, pending)
    if phase == Phase.HELD.value and (dangling_branch == BRANCH_LANDED or published):
        if read is None:  # row 4
            return GuardDecision(GuardAction.HOLD, "read_failed")
        return release_decision(
            mode=mode,
            ordinal=ordinal,
            cycle_id=cycle_id if cycle_id is not None else guard.get("cycle_id"),
            guard=guard,
            read=read,
            applied_edits=max(1, applied_edits),
            target_sha=target_sha,
            push_completed=True,
        )
    if dangling_branch == BRANCH_NOT_LANDED and phase == Phase.HELD.value:  # row 5
        return GuardDecision(GuardAction.NOOP, "held_through_redrive")
    if dangling_branch == BRANCH_AMBIGUOUS:  # row 6
        return GuardDecision(GuardAction.HOLD, "ambiguous_remote_tip")
    if phase == Phase.RELEASE_PENDING.value:
        if guard.get("owned_draft"):  # row 7
            return GuardDecision(GuardAction.RETRY_RELEASE, "release_pending")
        if read is not None and read.is_draft:  # row 8
            return GuardDecision(GuardAction.HOLD, "ownership_unproven")
    return GuardDecision(GuardAction.NOOP, "nothing_to_do")  # row 9


__all__ = [
    "BRANCH_AMBIGUOUS",
    "BRANCH_LANDED",
    "BRANCH_NOT_LANDED",
    "Direction",
    "GuardAction",
    "GuardDecision",
    "GuardMode",
    "GuardRead",
    "Phase",
    "classify_toggles",
    "engage_decision",
    "fix_cycle_id",
    "fold_draft_guard",
    "guard_status",
    "held_cycle_published",
    "next_cycle_number",
    "pending_requests",
    "release_decision",
    "resume_decision",
]
