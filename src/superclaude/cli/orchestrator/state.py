"""What survives a restart: the per-issue state file, plan records and run files (design 5.5).

Everything lives under ``<orchestrator-repo>/.orchestrator/``, the folder that the
poll reads (``issue_watch.route``) and that this module shares with it:

* ``issues/<owner>__<repo>__<N>.json``: the state file of one issue. Fields:
  ``schema``, ``repo``, ``number``, ``orchestrator``, ``tiers``, ``status``
  (``in_progress``, ``done``, ``escalated``, ``skipped``, ``failed``), ``wave``,
  ``step``, ``wake_id``, ``ids`` (the ids found so far), ``round``, ``remaining``,
  ``rounds``, ``body_sha`` and the append-only ``log`` of
  ``{ts, wave, step, phase, detail}`` where ``phase`` is ``intent`` or ``done``;
* ``issues/plan-<key>.<requested_at>.json``: the plan record of one plan request
  (``kind: plan``; status ``in_progress``, ``done`` or ``failed``), never reused by a
  later request of the same key;
* ``runs/<orchestrator id>.json``: the Run of one orchestrator (5.7).

The rules (5.5): write the ``intent`` line before an outward act and the ``done``
line after it; on a restart an ``intent`` with no ``done`` is settled by reading the
outside state, never by repeating the act (``pending_intent`` finds it). A state
file is created exclusively (a second file for one key is refused), every write
holds ``flock`` on ``.orchestrator/state.lock`` (the lock the poll's routing also
takes), and a file is replaced whole through a temporary file and ``rename``, so a
reader never sees half a file. A file that cannot be read is reported and never
overwritten.

Exclusive create here is a temporary file plus ``os.link``: it fails with
``EEXIST`` exactly as ``O_EXCL`` does, and the new file appears already complete,
so a kill cannot leave an empty state file behind.
"""

from __future__ import annotations

import json
import os
import re
import threading
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

from superclaude.cli.issue_watch.predicates import (
    ORCHESTRATOR_ID_PATTERN,
    WAKE_ID_PATTERN,
    file_key,
    format_utc,
    parse_utc,
    valid_issue_number,
    valid_operation_id,
    valid_repo,
)
from superclaude.cli.issue_watch.route import (
    ISSUES_DIR,
    PLAN_STATUSES,
    RUN_STATUSES,
    RUNS_DIR,
    STATE_DIR,
    STATE_STATUSES,
    StateLockBusy,
    state_lock,
)
from superclaude.cli.swarm.atomic import write_prepared_bytes

STATE_SCHEMA: Final = "orchestrator-state/1"
PLAN_SCHEMA: Final = "orchestrator-plan/1"
RUN_SCHEMA: Final = "orchestrator-run/1"

MAX_READ_BYTES: Final = 1024 * 1024
"""The poll reads a state file only up to this size; a bigger one counts as unreadable."""
MAX_WRITE_BYTES: Final = 900 * 1024
"""A write that would make a file bigger than this is refused (it stays readable by the poll)."""

PHASES: Final = ("intent", "done")
FINAL_STATUSES: Final = ("done", "skipped", "failed")
RETAKE_STEPS: Final = ("closeout_unclear", "closeout_failed", "handback_stopped")
"""The last steps of an ``escalated`` file that a hand-run ``--take`` may move aside (5.7)."""
RETAKEN_DIR: Final = "retaken"

_TRANSITIONS: Final = {
    "in_progress": frozenset({"done", "escalated", "skipped", "failed"}),
    # Never straight to ``done`` (finding F36 of issue 675): wave 9 must not turn an
    # escalated ending (landed_open, closeout_unclear, closeout_failed,
    # handback_stopped) into closed work. A person's answer first reopens the file.
    "escalated": frozenset({"in_progress", "skipped", "failed"}),
}
_RUN_TRANSITIONS: Final = {
    "active": frozenset({"ending"}),
    "ending": frozenset({"active", "ended"}),
}
PLAN_STEPS: Final = ("plan_call_started", "plan_written", "plan_done", "plan_failed")

_STEP = re.compile(r"[a-z][a-z0-9_]{0,59}")
_SHA = re.compile(r"[0-9a-f]{7,64}")
_REF = re.compile(r"[A-Za-z0-9._/-]{1,200}")
_TAG = re.compile(r"[A-Za-z0-9._-]{1,32}")
_RUN_ID = re.compile(r"[A-Za-z0-9._:-]{1,128}")
_HOST = re.compile(r"[ -~]{1,255}")
_UTC_STAMP = "%Y%m%dT%H%M%SZ"
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")

EXIT_INVALID: Final = 2
EXIT_CONFLICT: Final = 3
EXIT_UNREADABLE: Final = 4
EXIT_NOT_FOUND: Final = 5
EXIT_LOCK_BUSY: Final = 75


class StateError(Exception):
    """A state operation that cannot be done; ``reason`` is a fixed code, ``code`` the exit code."""

    def __init__(self, reason: str, code: int = EXIT_INVALID, **info: object) -> None:
        super().__init__(reason)
        self.reason = reason
        self.code = code
        self.info = info


# --- field checks ----------------------------------------------------------------------


def _text(value: object, limit: int) -> bool:
    return isinstance(value, str) and len(value) <= limit and not _CONTROL.search(value)


def _pos_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and 0 < value < 2**53


def _is_abs_path(value: object) -> bool:
    return isinstance(value, str) and _text(value, 1024) and os.path.isabs(value)


def _match(pattern: re.Pattern[str]) -> Callable[[object], bool]:
    return lambda v: isinstance(v, str) and pattern.fullmatch(v) is not None


IDS_CHECKS: Final[dict[str, Callable[[object], bool]]] = {
    "lease_comment_id": _pos_int,
    "claim_comment_id": _pos_int,
    "plan_marker": lambda v: _text(v, 200) and bool(v),
    "task_id": valid_operation_id,
    "dispatch_id": valid_operation_id,
    "terminal_handle": valid_operation_id,
    "worktree_path": _is_abs_path,
    "branch": _match(_REF),
    "pr_number": _pos_int,
    "pr_head_sha": _match(_SHA),
    "merge_commit": _match(_SHA),
}
"""The ids a wave finds and records: name -> check. A restart reads them back."""

ROUND_KEYS: Final = frozenset(
    {
        "round",
        "pr",
        "head_sha",
        "merge_commit",
        "dispatch",
        "branch",
        "remaining",
        "closeout_result",
        "audit_result",
    }
)
TIER_AGENTS: Final = ("plan", "worker")
TIER_KEYS: Final = ("requested", "effective", "fallback_from")
REMAINING_MAX_LINES: Final = 20
REMAINING_MAX_CHARS: Final = 300


def _check_tiers(tiers: object) -> bool:
    if not isinstance(tiers, dict) or not set(tiers) <= set(TIER_AGENTS):
        return False
    return all(
        isinstance(t, dict)
        and set(t) <= set(TIER_KEYS)
        and all(v is None or _text(v, 200) for v in t.values())
        for t in tiers.values()
    )


def _check_log(log: object) -> bool:
    if not isinstance(log, list):
        return False
    for e in log:
        if not (
            isinstance(e, dict)
            and set(e) == {"ts", "wave", "step", "phase", "detail"}
            and isinstance(e["ts"], str)
            and isinstance(e["wave"], int)
            and _match(_STEP)(e["step"])
            and e["phase"] in PHASES
            and (e["detail"] is None or _text(e["detail"], 2000))
        ):
            return False
        try:
            parse_utc(e["ts"])
        except ValueError:
            return False
    return True


def validate_state(
    doc: object, repo: str | None = None, number: int | None = None
) -> None:
    """Raise ``StateError('state_unreadable')`` unless ``doc`` is a well-formed state file."""
    ok = (
        isinstance(doc, dict)
        and doc.get("schema") == STATE_SCHEMA
        and valid_repo(doc.get("repo"))
        and valid_issue_number(doc.get("number"))
        and (repo is None or doc["repo"] == repo)
        and (number is None or doc["number"] == number)
        and _match(ORCHESTRATOR_ID_PATTERN)(doc.get("orchestrator"))
        and doc.get("status") in STATE_STATUSES
        and isinstance(doc.get("wave"), int)
        and 0 <= doc["wave"] <= 9
        and _match(_STEP)(doc.get("step"))
        and (doc.get("wake_id") is None or _match(WAKE_ID_PATTERN)(doc["wake_id"]))
        and isinstance(doc.get("ids"), dict)
        and all(k in IDS_CHECKS and IDS_CHECKS[k](v) for k, v in doc["ids"].items())
        and _check_tiers(doc.get("tiers"))
        and _pos_int(doc.get("round"))
        and isinstance(doc.get("remaining"), list)
        and len(doc["remaining"]) <= REMAINING_MAX_LINES
        and all(_text(r, REMAINING_MAX_CHARS) for r in doc["remaining"])
        and isinstance(doc.get("rounds"), list)
        and all(isinstance(r, dict) and set(r) <= ROUND_KEYS for r in doc["rounds"])
        and (doc.get("body_sha") is None or _match(_SHA)(doc["body_sha"]))
        and _check_log(doc.get("log"))
    )
    if not ok:
        raise StateError("state_unreadable", EXIT_UNREADABLE)


def _validate_plan(doc: object) -> None:
    ok = (
        isinstance(doc, dict)
        and doc.get("schema") == PLAN_SCHEMA
        and doc.get("kind") == "plan"
        and valid_repo(doc.get("repo"))
        and valid_issue_number(doc.get("number"))
        and _match(ORCHESTRATOR_ID_PATTERN)(doc.get("orchestrator"))
        and doc.get("status") in PLAN_STATUSES
        and doc.get("step") in PLAN_STEPS
        and isinstance(doc.get("requested_at"), str)
        and _check_log(doc.get("log"))
    )
    if ok:
        try:
            parse_utc(doc["requested_at"])  # type: ignore[index]
        except ValueError:
            ok = False
    if not ok:
        raise StateError("state_unreadable", EXIT_UNREADABLE)


def _validate_run(doc: object) -> None:
    ok = (
        isinstance(doc, dict)
        and doc.get("schema") == RUN_SCHEMA
        and _match(_RUN_ID)(doc.get("run_id"))
        and _match(_TAG)(doc.get("tag"))
        and valid_repo(doc.get("repo"))
        and _match(_HOST)(doc.get("host"))
        and isinstance(doc.get("created_at"), str)
        and doc.get("status") in RUN_STATUSES
    )
    if ok:
        try:
            parse_utc(doc["created_at"])  # type: ignore[index]
        except ValueError:
            ok = False
    if not ok:
        raise StateError("state_unreadable", EXIT_UNREADABLE)


# --- files ------------------------------------------------------------------------------


def _folder(root: Path | str, sub: str) -> Path:
    return Path(root) / STATE_DIR / sub


def state_path(root: Path | str, repo: str, number: int) -> Path:
    """``<root>/.orchestrator/issues/<owner>__<repo>__<N>.json`` (``ValueError`` for a bad key)."""
    return _folder(root, ISSUES_DIR) / f"{file_key(repo, number)}.json"


def _stamp(requested_at: str) -> str:
    return parse_utc(requested_at).strftime(_UTC_STAMP)


def plan_path(root: Path | str, repo: str, number: int, requested_at: str) -> Path:
    """``issues/plan-<key>.<requested_at>.json`` for the ``requested_at`` of a plan request."""
    name = f"plan-{file_key(repo, number)}.{_stamp(requested_at)}.json"
    return _folder(root, ISSUES_DIR) / name


def run_path(root: Path | str, ident: str) -> Path:
    """``runs/<orchestrator id>.json``."""
    if ORCHESTRATOR_ID_PATTERN.fullmatch(ident) is None:
        raise StateError("invalid_orchestrator_id")
    return _folder(root, RUNS_DIR) / f"{ident}.json"


_held = threading.local()


@contextmanager
def locked(root: Path | str, wait_s: float = 10.0) -> Iterator[None]:
    """Hold ``.orchestrator/state.lock``; ``StateError('lock_busy')`` when it stays held.

    The lock can be taken again by the thread that already holds it (it is then
    only counted): a verb that needs the lock for a whole sequence, such as
    ``idle-end``, can call the functions below that take it themselves. A
    ``flock`` taken through a second file descriptor would otherwise wait for
    the first one until ``lock_busy``.
    """
    key = os.path.realpath(Path(root) / STATE_DIR)
    counts: dict[str, int] = _held.__dict__.setdefault("counts", {})
    if counts.get(key, 0) > 0:
        counts[key] += 1
        try:
            yield
        finally:
            counts[key] -= 1
        return
    try:
        with state_lock(Path(root), wait_s):
            counts[key] = 1
            try:
                yield
            finally:
                counts.pop(key, None)
    except StateLockBusy:
        raise StateError("lock_busy", EXIT_LOCK_BUSY) from None


def _read(path: Path) -> dict[str, Any]:
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_READ_BYTES + 1)
    except FileNotFoundError:
        raise StateError("not_found", EXIT_NOT_FOUND) from None
    except OSError:
        raise StateError("state_unreadable", EXIT_UNREADABLE) from None
    try:
        doc = json.loads(data.decode("utf-8")) if len(data) <= MAX_READ_BYTES else None
    except (ValueError, RecursionError):
        doc = None
    if not isinstance(doc, dict):
        raise StateError("state_unreadable", EXIT_UNREADABLE)
    return doc


def _encode(doc: dict[str, Any]) -> bytes:
    data = (json.dumps(doc, indent=2) + "\n").encode("ascii")
    if len(data) > MAX_WRITE_BYTES:
        raise StateError("state_too_large", EXIT_UNREADABLE)
    return data


def _replace(path: Path, doc: dict[str, Any]) -> None:
    """Replace ``path`` whole by a temporary file and ``rename``."""
    write_prepared_bytes(path, _encode(doc))


def _create_exclusive(path: Path, doc: dict[str, Any]) -> None:
    """Create ``path`` with its whole content, or raise ``already_exists``."""
    data = _encode(doc)
    os.makedirs(path.parent, mode=0o700, exist_ok=True)
    tmp = path.with_name(f".{path.name}.new-{os.getpid()}")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        try:
            os.write(fd, data)
            os.fsync(fd)
        finally:
            os.close(fd)
        try:
            os.link(tmp, path)
        except FileExistsError:
            raise StateError("already_exists", EXIT_CONFLICT) from None
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def _now(now: datetime | None) -> datetime:
    return now if now is not None else datetime.now(timezone.utc)


def _line(now: datetime, wave: int, step: str, phase: str, detail: str | None) -> dict:
    return {
        "ts": format_utc(now),
        "wave": wave,
        "step": step,
        "phase": phase,
        "detail": detail,
    }


def _check_position(wave: object, step: object, detail: object) -> None:
    if not (isinstance(wave, int) and 0 <= wave <= 9 and _match(_STEP)(step)):
        raise StateError("invalid_wave_or_step")
    if detail is not None and not _text(detail, 2000):
        raise StateError("invalid_detail")


# --- the state file of an issue ---------------------------------------------------------


def load_state(root: Path | str, repo: str, number: int) -> dict[str, Any]:
    """Read and check the state file of an issue (``not_found`` or ``state_unreadable``)."""
    doc = _read(state_path(root, repo, number))
    validate_state(doc, repo, number)
    return doc


def pending_intent(doc: dict[str, Any]) -> dict[str, Any] | None:
    """The ``intent`` line that no ``done`` line has settled, or ``None`` (rule 2 of 5.5)."""
    open_line: dict[str, Any] | None = None
    for entry in doc["log"]:
        if entry["phase"] == "intent":
            open_line = entry
        elif open_line is not None and (entry["wave"], entry["step"]) == (
            open_line["wave"],
            open_line["step"],
        ):
            open_line = None
    return open_line


def create_state(
    root: Path | str,
    repo: str,
    number: int,
    orchestrator: str,
    *,
    wake_id: str | None = None,
    wave: int = 1,
    step: str = "claim",
    retake: bool = False,
) -> dict[str, Any]:
    """Create the state file of an issue (``status: in_progress``); a second one is refused.

    With ``retake`` (a hand-run ``--take``) an ``escalated`` file whose last step is
    one of ``RETAKE_STEPS`` is first moved to
    ``issues/retaken/<key>-<UTC time>.json``; any other existing file still refuses.
    """
    doc: dict[str, Any] = {
        "schema": STATE_SCHEMA,
        "repo": repo,
        "number": number,
        "orchestrator": orchestrator,
        "tiers": {},
        "status": "in_progress",
        "wave": wave,
        "step": step,
        "wake_id": wake_id,
        "ids": {},
        "round": 1,
        "remaining": [],
        "rounds": [],
        "body_sha": None,
        "log": [],
    }
    validate_state(doc)
    path = state_path(root, repo, number)
    with locked(root):
        if retake and path.exists():
            old = _read(path)
            if old.get("status") == "escalated" and old.get("step") in RETAKE_STEPS:
                aside = _folder(root, ISSUES_DIR) / RETAKEN_DIR
                os.makedirs(aside, mode=0o700, exist_ok=True)
                stamp = datetime.now(timezone.utc).strftime(_UTC_STAMP)
                os.rename(path, aside / f"{file_key(repo, number)}-{stamp}.json")
        try:
            _create_exclusive(path, doc)
        except StateError as exc:
            if exc.reason != "already_exists":
                raise
            existing = _read(path)
            validate_state(
                existing, repo, number
            )  # a file that is not one is reported as such
            raise StateError(
                "already_exists",
                EXIT_CONFLICT,
                status=existing.get("status"),
                step=existing.get("step"),
            ) from None
    return doc


def mutate(
    root: Path | str,
    repo: str,
    number: int,
    change: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    """Read, change and write one state file under the lock; the result is checked first.

    ``change`` edits the document in place. A document that fails ``validate_state``
    after the change is not written. This is how a wave records ids and how
    ``handback`` writes the next round.
    """
    path = state_path(root, repo, number)
    with locked(root):
        doc = _read(path)
        validate_state(doc, repo, number)
        change(doc)
        try:
            validate_state(doc, repo, number)
        except StateError:  # the file was fine; the change is what is wrong
            raise StateError("invalid_value") from None
        _replace(path, doc)
    return doc


def _not_final(doc: dict[str, Any]) -> None:
    if doc["status"] in FINAL_STATUSES:
        raise StateError("final_status", EXIT_CONFLICT, status=doc["status"])


def record_intent(
    root: Path | str,
    repo: str,
    number: int,
    wave: int,
    step: str,
    detail: str | None = None,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Write the ``intent`` line before an outward act (rule 1).

    Refused with ``intent_open`` while an earlier ``intent`` has no ``done``: that
    act is settled from the outside state first, and not repeated.
    """
    _check_position(wave, step, detail)
    stamp = _now(now)

    def change(doc: dict[str, Any]) -> None:
        _not_final(doc)
        open_line = pending_intent(doc)
        if open_line is not None:
            raise StateError(
                "intent_open",
                EXIT_CONFLICT,
                wave=open_line["wave"],
                step=open_line["step"],
            )
        doc["wave"], doc["step"] = wave, step
        doc["log"].append(_line(stamp, wave, step, "intent", detail))

    return mutate(root, repo, number, change)


def record_done(
    root: Path | str,
    repo: str,
    number: int,
    wave: int,
    step: str,
    detail: str | None = None,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Write the ``done`` line after an outward act.

    It settles the open ``intent`` of the same wave and step. With no open
    ``intent`` it records an act whose effect was already visible outside (rule 3).
    An open ``intent`` for another step is ``intent_mismatch``.
    """
    _check_position(wave, step, detail)
    stamp = _now(now)

    def change(doc: dict[str, Any]) -> None:
        _not_final(doc)
        open_line = pending_intent(doc)
        if open_line is not None and (open_line["wave"], open_line["step"]) != (
            wave,
            step,
        ):
            raise StateError(
                "intent_mismatch",
                EXIT_CONFLICT,
                wave=open_line["wave"],
                step=open_line["step"],
            )
        doc["wave"], doc["step"] = wave, step
        doc["log"].append(_line(stamp, wave, step, "done", detail))

    return mutate(root, repo, number, change)


def set_fields(
    root: Path | str,
    repo: str,
    number: int,
    *,
    ids: dict[str, object] | None = None,
    body_sha: str | None = None,
    tiers: dict[str, dict[str, object]] | None = None,
) -> dict[str, Any]:
    """Record what a wave found: ids (a ``None`` value removes one), the body hash and the tiers.

    ``tiers`` is merged one agent (``plan`` or ``worker``) at a time. Unknown names
    and bad values are refused, because the result is checked before it is written.
    """
    if not ids and body_sha is None and not tiers:
        raise StateError("nothing_to_set")
    if ids and not set(ids) <= set(IDS_CHECKS):
        raise StateError("unknown_id_name")

    def change(doc: dict[str, Any]) -> None:
        _not_final(doc)
        for name, value in (ids or {}).items():
            if value is None:
                doc["ids"].pop(name, None)
            else:
                doc["ids"][name] = value
        if body_sha is not None:
            doc["body_sha"] = body_sha
        for agent, values in (tiers or {}).items():
            doc["tiers"].setdefault(agent, {}).update(values)

    return mutate(root, repo, number, change)


def set_status(
    root: Path | str,
    repo: str,
    number: int,
    status: str,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Move the file to ``status``: ``in_progress`` to any end; ``escalated`` back to
    ``in_progress`` (after the answer) or on to ``skipped`` or ``failed``, never to ``done``.

    ``done``, ``skipped`` and ``failed`` are final. The move is logged as a ``done``
    line with the step ``status_<status>``; it does not settle an open ``intent``.
    """
    if status not in STATE_STATUSES:
        raise StateError("invalid_status")
    stamp = _now(now)

    def change(doc: dict[str, Any]) -> None:
        if doc["status"] == status:
            return
        if status not in _TRANSITIONS.get(doc["status"], frozenset()):
            raise StateError("bad_transition", EXIT_CONFLICT, status=doc["status"])
        doc["status"] = status
        doc["log"].append(_line(stamp, doc["wave"], f"status_{status}", "done", None))

    return mutate(root, repo, number, change)


# --- plan records -----------------------------------------------------------------------


def create_plan(
    root: Path | str,
    repo: str,
    number: int,
    requested_at: str,
    orchestrator: str,
    *,
    now: datetime | None = None,
) -> tuple[dict[str, Any], bool]:
    """Create the plan record of one request, or return the one a kill left (``created=False``).

    Wave 0 writes the record first and the acknowledgment ``taken`` second, so a
    record that already exists is the record of this same request.
    """
    stamp = _now(now)
    doc: dict[str, Any] = {
        "schema": PLAN_SCHEMA,
        "kind": "plan",
        "repo": repo,
        "number": number,
        "requested_at": format_utc(parse_utc(requested_at)),
        "orchestrator": orchestrator,
        "status": "in_progress",
        "step": "plan_call_started",
        "log": [_line(stamp, 0, "plan_call_started", "done", None)],
    }
    _validate_plan(doc)
    path = plan_path(root, repo, number, requested_at)
    with locked(root):
        try:
            _create_exclusive(path, doc)
        except StateError as exc:
            if exc.reason != "already_exists":
                raise
            existing = _read(path)
            _validate_plan(existing)
            return existing, False
    return doc, True


def load_plan(
    root: Path | str, repo: str, number: int, requested_at: str
) -> dict[str, Any]:
    """Read and check one plan record."""
    doc = _read(plan_path(root, repo, number, requested_at))
    _validate_plan(doc)
    return doc


def record_plan_step(
    root: Path | str,
    repo: str,
    number: int,
    requested_at: str,
    step: str,
    detail: str | None = None,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Add a step to a plan record: ``plan_written`` (detail: the body hash), ``plan_done`` or ``plan_failed``.

    ``plan_done`` ends the record ``done`` and ``plan_failed`` (with its reason as
    detail) ends it ``failed``. A final record takes no more steps.
    """
    if step not in PLAN_STEPS[1:]:
        raise StateError("invalid_plan_step")
    if step == "plan_written" and not _match(_SHA)(detail):
        raise StateError("invalid_detail")
    if step == "plan_failed" and not (detail and _text(detail, 300)):
        raise StateError("invalid_detail")
    stamp = _now(now)
    path = plan_path(root, repo, number, requested_at)
    with locked(root):
        doc = _read(path)
        _validate_plan(doc)
        if doc["status"] != "in_progress":
            raise StateError("plan_final", EXIT_CONFLICT, status=doc["status"])
        doc["step"] = step
        doc["log"].append(_line(stamp, 0, step, "done", detail))
        if step == "plan_done":
            doc["status"] = "done"
        elif step == "plan_failed":
            doc["status"] = "failed"
        _validate_plan(doc)
        _replace(path, doc)
    return doc


# --- run files --------------------------------------------------------------------------


def create_run(
    root: Path | str,
    ident: str,
    run_id: str,
    tag: str,
    repo: str,
    host: str,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Write ``runs/<id>.json`` at once, before anything else (wave 0); a second one is refused."""
    doc: dict[str, Any] = {
        "schema": RUN_SCHEMA,
        "run_id": run_id,
        "tag": tag,
        "repo": repo,
        "host": host,
        "created_at": format_utc(_now(now)),
        "status": "active",
    }
    _validate_run(doc)
    with locked(root):
        _create_exclusive(run_path(root, ident), doc)
    return doc


def load_run(root: Path | str, ident: str) -> dict[str, Any]:
    """Read and check ``runs/<id>.json``."""
    doc = _read(run_path(root, ident))
    _validate_run(doc)
    return doc


def set_run_status(root: Path | str, ident: str, status: str) -> dict[str, Any]:
    """Move a run file: ``active`` to ``ending``; ``ending`` back to ``active`` or on to ``ended``.

    ``ended`` is final: an ended id is never reused.
    """
    if status not in RUN_STATUSES:
        raise StateError("invalid_status")
    path = run_path(root, ident)
    with locked(root):
        doc = _read(path)
        _validate_run(doc)
        if doc["status"] == status:
            return doc
        if status not in _RUN_TRANSITIONS.get(doc["status"], frozenset()):
            raise StateError("bad_transition", EXIT_CONFLICT, status=doc["status"])
        doc["status"] = status
        _replace(path, doc)
    return doc


# --- what is open (the restart rule) -----------------------------------------------------


def list_open(
    root: Path | str, orchestrator: str | None = None, status: str = "in_progress"
) -> list[dict[str, Any]]:
    """Summaries of the state files and plan records with ``status`` (the restart rule of 5.5).

    A state file carries ``pending_intent`` (the line to settle, or ``None``). A file
    that cannot be read is listed with ``reason: state_unreadable`` and never skipped.
    ``orchestrator`` keeps only the files of that orchestrator.
    """
    found: list[dict[str, Any]] = []
    directory = _folder(root, ISSUES_DIR)
    try:
        names = sorted(n for n in os.listdir(directory) if n.endswith(".json"))
    except OSError:
        return found
    for name in names:
        path = directory / name
        if not path.is_file():
            continue
        is_plan = name.startswith("plan-")
        try:
            doc = _read(path)
            if is_plan:
                _validate_plan(doc)
            else:
                validate_state(doc)
                if f"{file_key(doc['repo'], doc['number'])}.json" != name:
                    raise StateError("state_unreadable", EXIT_UNREADABLE)
        except StateError as exc:
            found.append({"file": name, "reason": exc.reason})
            continue
        if doc["status"] != status or (
            orchestrator is not None and doc["orchestrator"] != orchestrator
        ):
            continue
        item = {
            "kind": "plan" if is_plan else "issue",
            "repo": doc["repo"],
            "number": doc["number"],
            "orchestrator": doc["orchestrator"],
            "status": doc["status"],
            "step": doc["step"],
        }
        if is_plan:
            item["requested_at"] = doc["requested_at"]
        else:
            item["wave"] = doc["wave"]
            item["pending_intent"] = pending_intent(doc)
        found.append(item)
    return found
