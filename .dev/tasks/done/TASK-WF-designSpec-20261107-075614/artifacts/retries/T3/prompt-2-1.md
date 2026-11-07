bb05a78128b0ec419876a148437ce898b8960c30
Review one task for spec compliance.

Task brief: ## Task 3: Create `merge_guard.py` types, cycle ids, fold, pending matcher, published check and status mapping

Depends on: Task 2

Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6: `GuardMode`, `Direction`, `Phase`, `GuardAction`, `GuardRead`, `GuardDecision`; the string constants `BRANCH_LANDED = "landed"`, `BRANCH_NOT_LANDED = "not_landed"`, `BRANCH_AMBIGUOUS = "ambiguous"`; `fix_cycle_id(kind, n)` and `next_cycle_number(events, kind)` (never colliding with `CONFLICT_CYCLE_PREFIXES` from `src/superclaude/pr_submit/conflicts.py`); `fold_draft_guard(events)` implementing every row of the section 4.2 effect table (fields `phase, phase_before_request, cycle_id, original_is_draft, baseline, run_toggles, unsettled, failed_mutations, owned_draft, disabled_cause`; `None` when no guard record exists; `original_is_draft` taken only from the first guard record or a first skip, never from a later read); `pending_requests(events)` matching requests to settles by `idempotency_key`; `held_cycle_published(events, guard)` (true when a `push_completed` event, normal or recovered, carries the guard's `cycle_id`); `guard_status(guard, mode, ordinal)` implementing the first-match mapping of section 4.1 (`off`, `released`, `held`, `user_override`, `unavailable`). The module imports only `enum`, `dataclasses`, `re` and `is_conflict_cycle` from `.conflicts`, and contains no `gh` or `git` word on any line. Create `tests/pr_submit/test_merge_guard.py` with table tests for these functions.

Acceptance criteria:
- T3.AC1: `fix_cycle_id("fix", 2) == "fix-2"`, `fix_cycle_id("ci", 1) == "ci-1"`, `ValueError` for kind `sync` and for `n == 0`, `is_conflict_cycle(...)` is false for both kinds; `next_cycle_number` returns 1 on an empty log and 3 after `fix-1` and `fix-2` appear in event `cycle_id` fields.
- T3.AC2: A parametrized fold test covers every row of the section 4.2 effect table, and each of these cases fails if the row is implemented wrongly: `settled(any direction, skipped, not_applied)` clears the pending key and restores `phase_before_request` without touching `owned_draft` or the toggle counters; a draft request that was the first record followed by `not_applied` makes the fold return `None`, and a second request then sets a fresh `baseline` and `original_is_draft` (test: request, `not_applied`, request); a ready request followed by `not_applied` gives phase `HELD` with `unsettled == 0`; `settled(draft, confirmed, not changed)` gives `HELD` with `owned_draft` true and no toggle; `settled(ready, confirmed, not changed)` adds no toggle; `settled(draft, failed)` gives `RELEASE_PENDING`, increments `failed_mutations` and leaves `owned_draft` unchanged; `settled(draft, skipped, already_draft)` gives `DISABLED` with `disabled_cause == "already_draft"`; a log with no guard events returns `None`.
- T3.AC3: A `guard_status` test covers every phase and cause of the first-match mapping, including `ENGAGE_PENDING` and `RELEASE_PENDING` with `owned_draft` true (`held`) and false (`unavailable`), `DISABLED` with `user_override` (`user_override`) and with `already_draft` (`off`), mode `OFF` and ordinal below 3 with no record (`off`), and no record at ordinal 3 (`released`).
- T3.AC4: `pending_requests` returns exactly the requests whose key has no settle, with retries distinguished by the `:a<k>` suffix; `held_cycle_published` is true for a normal and for a recovered (`recovered: true`) `push_completed` of the guard's `cycle_id`, false for another cycle's `push_completed` and for `guard is None`; a static test asserts `merge_guard.py` has no whole word `gh` or `git`.
- T3.AC5: A test imports `superclaude.pr_submit.recovery` and asserts `BRANCH_LANDED`, `BRANCH_NOT_LANDED` and `BRANCH_AMBIGUOUS` equal `BRANCH_A_LANDED`, `BRANCH_B_NOT_LANDED` and `BRANCH_C_AMBIGUOUS` of that module.
- T3.AC6: `uv run pytest tests/pr_submit/test_merge_guard.py -q` passes and `uv run ruff check` and `uv run ruff format --check` are clean for both new files.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: bb05a78128b0ec419876a148437ce898b8960c30
Diff against the start snapshot: NEW FILE src/superclaude/pr_submit/merge_guard.py (full contents, 11616 bytes):
"""Pure decision core for the ``sc:pr-submit`` merge guard (issue #375).

The guard turns a pull request into a draft when a verified Medium-or-higher
review finding is routed to a fix, and marks it ready again only once that
cycle's fix push is confirmed on the PR head (or a zero-edit cycle is proven).

This module only DECIDES. It does no I/O: the protocol (``SKILL.md`` and
``refs/merge-guard.md``) reads the PR through ``scripts/set-draft-state.sh``,
calls these functions, appends the run-log events and performs the mutation.
That is the same split as the push triad and the re-trigger (NFR-6).

Core-purity (NFR-6 / AC-9): this module imports only the standard library and
contains no version-control or hosting command word on any line.

Guard state is the plain dict returned by :func:`fold_draft_guard` (or ``None``
when the run log holds no guard record); decisions read it with ``.get`` so a
hand-built dict works the same way.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

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
    for event in _iter_events(events):
        event_type = event.get("event_type")
        if event_type == REQUESTED:
            record = _fold_requested(record, pending, event)
        elif event_type == SETTLED:
            record = _fold_settled(record, pending, event)
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


def _fold_settled(record: dict | None, pending: dict, event: dict) -> dict | None:
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
    if outcome == "failed":
        record["phase"] = Phase.RELEASE_PENDING.value
        record["failed_mutations"] += 1
        return record
    if outcome == "confirmed":
        if to == Direction.DRAFT.value:
            record["phase"] = Phase.HELD.value
            record["owned_draft"] = True
        else:
            record["phase"] = Phase.RELEASED.value
            record["owned_draft"] = False
        if changed:
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

NEW FILE tests/pr_submit/test_merge_guard.py (full contents, 14783 bytes):
"""Tests for the pure merge-guard core (issue #375): ids, fold, status, matchers."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from superclaude.pr_submit import conflicts, recovery
from superclaude.pr_submit import merge_guard as mg
from superclaude.pr_submit.models import EventType

MODULE = Path(mg.__file__)


# --- event builders -------------------------------------------------------------


def _key(cycle: str, to: str, attempt: int = 1) -> str:
    return f"guard:r1:{cycle}:{to}:a{attempt}"


def req(to, *, cycle="fix-1", attempt=1, baseline=None, original=None):
    event = {
        "event_type": "draft_guard_requested",
        "run_id": "r1",
        "cycle_id": cycle,
        "to": to,
        "idempotency_key": _key(cycle, to, attempt),
    }
    if baseline is not None:
        event["timeline_baseline"] = baseline
    if original is not None:
        event["original_is_draft"] = original
    return event


def settled(
    to,
    outcome,
    *,
    changed=False,
    cause=None,
    cycle="fix-1",
    attempt=1,
    original=None,
    with_key=True,
):
    event = {
        "event_type": "draft_guard_settled",
        "run_id": "r1",
        "cycle_id": cycle,
        "to": to,
        "outcome": outcome,
        "changed": changed,
        "cause": cause,
    }
    if with_key:
        event["idempotency_key"] = _key(cycle, to, attempt)
    if original is not None:
        event["original_is_draft"] = original
    return event


def push_completed(cycle, **extra):
    return {"event_type": "push_completed", "cycle_id": cycle, **extra}


ENGAGED = [
    req("draft", baseline=2, original=False),
    settled("draft", "confirmed", changed=True),
]


# --- cycle ids ------------------------------------------------------------------


def test_fix_cycle_id_values_and_errors():
    assert mg.fix_cycle_id("fix", 2) == "fix-2"
    assert mg.fix_cycle_id("ci", 1) == "ci-1"
    for kind, n in (
        ("sync", 1),
        ("conflict", 1),
        ("fix", 0),
        ("ci", -1),
        ("fix", True),
    ):
        with pytest.raises(ValueError):
            mg.fix_cycle_id(kind, n)


@pytest.mark.parametrize("kind", ["fix", "ci"])
def test_fix_cycle_ids_never_look_like_conflict_cycles(kind):
    assert not conflicts.is_conflict_cycle(mg.fix_cycle_id(kind, 1))
    assert not mg.fix_cycle_id(kind, 7).startswith(conflicts.CONFLICT_CYCLE_PREFIXES)


def test_next_cycle_number():
    assert mg.next_cycle_number([], "fix") == 1
    events = [
        {"cycle_id": "fix-1"},
        {"cycle_id": "fix-2"},
        {"cycle_id": "ci-4"},
        {"cycle_id": "sync-9"},
        {},
    ]
    assert mg.next_cycle_number(events, "fix") == 3
    assert mg.next_cycle_number(events, "ci") == 5
    assert mg.next_cycle_number("not a list", "fix") == 1
    with pytest.raises(ValueError):
        mg.next_cycle_number([], "sync")


# --- fold -----------------------------------------------------------------------

FOLD_CASES = {
    "engage_confirmed_changed": (
        ENGAGED,
        {
            "phase": "held",
            "owned_draft": True,
            "run_toggles": 1,
            "unsettled": 0,
            "baseline": 2,
            "original_is_draft": False,
            "failed_mutations": 0,
        },
    ),
    "request_only": (
        [req("draft", baseline=4, original=False)],
        {
            "phase": "engage_pending",
            "unsettled": 1,
            "owned_draft": False,
            "baseline": 4,
        },
    ),
    "draft_failed": (
        [req("draft", baseline=1, original=False), settled("draft", "failed")],
        {
            "phase": "release_pending",
            "failed_mutations": 1,
            "owned_draft": False,
            "run_toggles": 0,
            "unsettled": 0,
        },
    ),
    "draft_confirmed_not_changed": (
        [
            req("draft", baseline=1, original=False),
            settled("draft", "confirmed", changed=False),
        ],
        {"phase": "held", "owned_draft": True, "run_toggles": 0},
    ),
    "ready_confirmed_changed": (
        ENGAGED + [req("ready"), settled("ready", "confirmed", changed=True)],
        {"phase": "released", "owned_draft": False, "run_toggles": 2, "unsettled": 0},
    ),
    "ready_confirmed_not_changed": (
        ENGAGED + [req("ready"), settled("ready", "confirmed", changed=False)],
        {"phase": "released", "owned_draft": False, "run_toggles": 1},
    ),
    "ready_request_only": (
        ENGAGED + [req("ready")],
        {
            "phase": "release_pending",
            "phase_before_request": "held",
            "unsettled": 1,
            "owned_draft": True,
        },
    ),
    "ready_failed": (
        ENGAGED + [req("ready"), settled("ready", "failed")],
        {
            "phase": "release_pending",
            "failed_mutations": 1,
            "owned_draft": True,
            "run_toggles": 1,
        },
    ),
    "skip_already_draft_without_request": (
        [
            settled(
                "draft", "skipped", cause="already_draft", with_key=False, original=True
            )
        ],
        {
            "phase": "disabled",
            "disabled_cause": "already_draft",
            "original_is_draft": True,
            "owned_draft": False,
            "unsettled": 0,
        },
    ),
    "skip_user_override_after_hold": (
        ENGAGED + [settled("ready", "skipped", cause="user_override", with_key=False)],
        {
            "phase": "disabled",
            "disabled_cause": "user_override",
            "owned_draft": False,
            "run_toggles": 1,
        },
    ),
    "retry_after_failed_engage": (
        [
            req("draft", baseline=1, original=False),
            settled("draft", "failed"),
            req("draft", attempt=2),
            settled("draft", "confirmed", changed=True, attempt=2),
        ],
        {
            "phase": "held",
            "failed_mutations": 1,
            "run_toggles": 1,
            "owned_draft": True,
            "baseline": 1,
            "unsettled": 0,
        },
    ),
    "ready_not_applied_returns_to_held": (
        ENGAGED + [req("ready"), settled("ready", "skipped", cause="not_applied")],
        {
            "phase": "held",
            "unsettled": 0,
            "owned_draft": True,
            "run_toggles": 1,
            "disabled_cause": None,
        },
    ),
    "draft_not_applied_after_failed_engage_returns_to_release_pending": (
        [
            req("draft", baseline=1, original=False),
            settled("draft", "failed"),
            req("draft", attempt=2),
            settled("draft", "skipped", cause="not_applied", attempt=2),
        ],
        {
            "phase": "release_pending",
            "unsettled": 0,
            "failed_mutations": 1,
            "owned_draft": False,
            "run_toggles": 0,
            "disabled_cause": None,
        },
    ),
    # A draft-direction not_applied must leave ownership and the toggle counters
    # alone whatever the earlier state was (owned, released or disabled).
    "draft_not_applied_keeps_a_held_state": (
        ENGAGED
        + [
            req("draft", cycle="fix-2"),
            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
        ],
        {
            "phase": "held",
            "unsettled": 0,
            "owned_draft": True,
            "run_toggles": 1,
            "failed_mutations": 0,
            "disabled_cause": None,
        },
    ),
    "draft_not_applied_keeps_a_released_state": (
        ENGAGED
        + [
            req("ready"),
            settled("ready", "confirmed", changed=True),
            req("draft", cycle="fix-2"),
            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
        ],
        {
            "phase": "released",
            "unsettled": 0,
            "owned_draft": False,
            "run_toggles": 2,
            "failed_mutations": 0,
            "disabled_cause": None,
        },
    ),
    "draft_not_applied_keeps_a_disabled_state": (
        [
            settled(
                "draft",
                "skipped",
                cause="already_draft",
                with_key=False,
                original=True,
            ),
            req("draft", cycle="fix-2"),
            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
        ],
        {
            "phase": "disabled",
            "unsettled": 0,
            "owned_draft": False,
            "run_toggles": 0,
            "original_is_draft": True,
            "disabled_cause": "already_draft",
        },
    ),
}


@pytest.mark.parametrize("name", sorted(FOLD_CASES))
def test_fold_effect_table(name):
    events, expected = FOLD_CASES[name]
    state = mg.fold_draft_guard(events)
    assert state is not None
    for key, value in expected.items():
        assert state[key] == value, (name, key, state)


def test_fold_returns_none_without_guard_events():
    assert mg.fold_draft_guard([]) is None
    assert (
        mg.fold_draft_guard([{"event_type": "push_completed", "cycle_id": "fix-1"}])
        is None
    )
    assert mg.fold_draft_guard("not a list") is None


def test_fold_first_request_not_applied_erases_the_record():
    events = [
        req("draft", baseline=1, original=False),
        settled("draft", "skipped", cause="not_applied"),
    ]
    assert mg.fold_draft_guard(events) is None


def test_fold_request_not_applied_request_takes_a_fresh_baseline():
    events = [
        req("draft", baseline=1, original=False),
        settled("draft", "skipped", cause="not_applied"),
        req("draft", cycle="fix-2", baseline=5, original=True),
    ]
    state = mg.fold_draft_guard(events)
    assert state["baseline"] == 5
    assert state["original_is_draft"] is True
    assert state["phase"] == "engage_pending"
    assert state["cycle_id"] == "fix-2"


def test_fold_user_override_sets_disabled_cause_and_feeds_guard_status():
    state = mg.fold_draft_guard(
        ENGAGED + [settled("ready", "skipped", cause="user_override", with_key=False)]
    )
    assert (state["phase"], state["owned_draft"], state["disabled_cause"]) == (
        "disabled",
        False,
        "user_override",
    )
    assert mg.guard_status(state, "draft", 3) == "user_override"


def test_fold_original_is_draft_comes_only_from_the_first_record():
    events = ENGAGED + [
        req("ready", original=True),
        settled("ready", "confirmed", changed=True, original=True),
    ]
    assert mg.fold_draft_guard(events)["original_is_draft"] is False


def test_fold_state_is_plain_data():
    state = mg.fold_draft_guard(ENGAGED)
    assert type(state["phase"]) is str
    assert set(state) == {
        "phase",
        "phase_before_request",
        "cycle_id",
        "original_is_draft",
        "baseline",
        "run_toggles",
        "unsettled",
        "failed_mutations",
        "owned_draft",
        "disabled_cause",
    }


# --- guard_status ---------------------------------------------------------------


def _guard(phase, owned=False, cause=None):
    return {"phase": phase, "owned_draft": owned, "disabled_cause": cause}


STATUS_CASES = [
    (None, "off", 3, "off"),
    (None, "draft", 2, "off"),
    (None, "draft", 3, "released"),
    (_guard("held", True), "draft", 3, "held"),
    (_guard("held", True), "off", 3, "held"),
    (_guard("engage_pending", True), "draft", 3, "held"),
    (_guard("engage_pending", False), "draft", 3, "unavailable"),
    (_guard("release_pending", True), "draft", 3, "held"),
    (_guard("release_pending", False), "draft", 3, "unavailable"),
    (_guard("disabled", False, "user_override"), "draft", 3, "user_override"),
    (_guard("disabled", False, "already_draft"), "draft", 3, "off"),
    (_guard("disabled", False, None), "draft", 3, "unavailable"),
    (_guard("released", False), "draft", 3, "released"),
]


@pytest.mark.parametrize(("guard", "mode", "ordinal", "expected"), STATUS_CASES)
def test_guard_status_mapping(guard, mode, ordinal, expected):
    assert mg.guard_status(guard, mode, ordinal) == expected


def test_failed_engage_reports_unavailable():
    state = mg.fold_draft_guard(
        [req("draft", baseline=1, original=False), settled("draft", "failed")]
    )
    assert mg.guard_status(state, "draft", 3) == "unavailable"


# --- pending_requests and held_cycle_published ----------------------------------


def test_pending_requests_pairs_by_idempotency_key():
    events = [
        req("draft", baseline=1, original=False),
        settled("draft", "failed"),
        req("draft", attempt=2),
        req("ready", cycle="fix-2"),
    ]
    pending = mg.pending_requests(events)
    assert [event["idempotency_key"] for event in pending] == [
        "guard:r1:fix-1:draft:a2",
        "guard:r1:fix-2:ready:a1",
    ]
    assert mg.pending_requests(ENGAGED) == []
    assert mg.pending_requests([]) == []


def test_held_cycle_published_normal_recovered_and_other_cycle():
    guard = mg.fold_draft_guard(ENGAGED)
    assert mg.held_cycle_published(ENGAGED + [push_completed("fix-1")], guard) is True
    assert (
        mg.held_cycle_published(
            ENGAGED + [push_completed("fix-1", recovered=True)], guard
        )
        is True
    )
    assert mg.held_cycle_published(ENGAGED + [push_completed("fix-2")], guard) is False
    assert mg.held_cycle_published(ENGAGED, guard) is False
    assert mg.held_cycle_published(ENGAGED + [push_completed("fix-1")], None) is False


# --- constants that must equal other modules ------------------------------------


def test_branch_constants_equal_recovery_constants():
    assert mg.BRANCH_LANDED == recovery.BRANCH_A_LANDED
    assert mg.BRANCH_NOT_LANDED == recovery.BRANCH_B_NOT_LANDED
    assert mg.BRANCH_AMBIGUOUS == recovery.BRANCH_C_AMBIGUOUS


def test_event_names_equal_event_type_values():
    assert mg.REQUESTED == EventType.DRAFT_GUARD_REQUESTED.value
    assert mg.SETTLED == EventType.DRAFT_GUARD_SETTLED.value


# --- purity ---------------------------------------------------------------------


def test_module_has_no_version_control_or_hosting_command_word():
    token = re.compile(r"\bgh\b|\bgit\b")
    offenders = [
        f"{number}: {line.strip()}"
        for number, line in enumerate(
            MODULE.read_text(encoding="utf-8").splitlines(), 1
        )
        if token.search(line)
    ]
    assert not offenders, offenders


def test_module_imports_only_the_allowed_modules():
    imports = re.findall(
        r"^(?:from|import)\s+(\S+)", MODULE.read_text(encoding="utf-8"), re.M
    )
    assert set(imports) <= {"__future__", "re", "dataclasses", "enum", ".conflicts"}, (
        imports
    )

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/tests/pr_submit/test_merge_guard.py b/tests/pr_submit/test_merge_guard.py
index 69ea4816..79898493 100644
--- a/tests/pr_submit/test_merge_guard.py
+++ b/tests/pr_submit/test_merge_guard.py
@@ -239,9 +239,66 @@ FOLD_CASES = {
             "phase": "release_pending",
             "unsettled": 0,
             "failed_mutations": 1,
+            "owned_draft": False,
+            "run_toggles": 0,
+            "disabled_cause": None,
+        },
+    ),
+    # A draft-direction not_applied must leave ownership and the toggle counters
+    # alone whatever the earlier state was (owned, released or disabled).
+    "draft_not_applied_keeps_a_held_state": (
+        ENGAGED
+        + [
+            req("draft", cycle="fix-2"),
+            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
+        ],
+        {
+            "phase": "held",
+            "unsettled": 0,
+            "owned_draft": True,
+            "run_toggles": 1,
+            "failed_mutations": 0,
+            "disabled_cause": None,
+        },
+    ),
+    "draft_not_applied_keeps_a_released_state": (
+        ENGAGED
+        + [
+            req("ready"),
+            settled("ready", "confirmed", changed=True),
+            req("draft", cycle="fix-2"),
+            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
+        ],
+        {
+            "phase": "released",
+            "unsettled": 0,
+            "owned_draft": False,
+            "run_toggles": 2,
+            "failed_mutations": 0,
             "disabled_cause": None,
         },
     ),
+    "draft_not_applied_keeps_a_disabled_state": (
+        [
+            settled(
+                "draft",
+                "skipped",
+                cause="already_draft",
+                with_key=False,
+                original=True,
+            ),
+            req("draft", cycle="fix-2"),
+            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
+        ],
+        {
+            "phase": "disabled",
+            "unsettled": 0,
+            "owned_draft": False,
+            "run_toggles": 0,
+            "original_is_draft": True,
+            "disabled_cause": "already_draft",
+        },
+    ),
 }
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T3.AC2 at=tests/pr_submit/test_merge_guard.py:602 anchor="without touching `owned_draft` or the toggle counters" chk=y,n,n,n family=fold-notapplied-draft-direction fix=in draft_not_applied_after_failed_engage_returns_to_release_pending, assert owned_draft, run_toggles == 0 and phase_before_request; add a case with a held, released or disabled earlier cycle so owned_draft is not already False covers="settled(any direction, skipped, not_applied) clears the pending key and restores phase_before_request without touching owned_draft or the toggle counters" first=start origin=new: The only draft-direction not_applied case asserts just phase, unsettled, failed_mutations and disabled_cause; owned_draft is False and run_toggles is 0 by default, so a wrong implementation that touched either for a draft request would pass every test.
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
