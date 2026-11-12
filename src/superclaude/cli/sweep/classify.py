"""Pure classifier for the read-only ``superclaude sweep`` (DESIGN sections 7.1, 7.2).

Every function here is pure over ``models`` types. The module reads no file, starts
no process and never reads a clock: every time comes from ``SweepContext.now`` or
the data passed in (NFR-004). Only the standard library and ``.models`` are imported.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import MISSING, dataclass, field, fields, replace
from datetime import datetime
from pathlib import Path

from .models import (
    CLASSES,
    PACKAGE_STATES,
    SHOW_CAP_REASON,
    TIME_BUDGET_REASON,
    Classification,
    ClassifiedRow,
    ContractRecord,
    OrcaObservation,
    PackageRecord,
    SafeToClose,
    SessionRow,
    SourceCoverage,
    SweepContext,
    SweepInput,
    SweepResult,
    TabMapEntry,
    TranscriptTail,
    WorktreeState,
    report_folders,
)

# Join path in force. Step 1.0a items 1 and 22 (CLOSED): ``session_join`` is
# ``dispatch.assigneeHandle``, compared with ``TabMapEntry.terminal_handle`` (path B).
JOIN_PATH = "B"

(
    C_WAITING,
    C_STALLED,
    C_FENCED,
    C_WORKING,
    C_FINISHED,
    C_IDLE,
    C_PERSON_ACTIVE,
    C_UNKNOWN,
) = CLASSES

# Notes and reasons, byte-exact from DESIGN section 7.2 and the R3 fixes.
NOTE_WINDOW_NOT_OBSERVABLE = "Dispatch time window not observable"
NOTE_SEVERAL_ROWS = "conflict: one pane session matches several Dispatch rows"
NOTE_PANE_MOVED = "pane moved to a later session"
NOTE_BEFORE_WINDOW = "session started before this Dispatch window"
NOTE_TAIL_ONLY = "session start not observable: transcript tail only"
NOTE_JOINED_BY_PANE = "joined by pane: latest session of the pane"
NOTE_JOIN_NOT_OBSERVABLE = "tab map join not observable"
NOTE_PANE_NOT_SCOPED = "Orca pane session, not in scoped Runs"
NOTE_EARLIER_PANE = (
    "earlier pane session not joinable (tab map keeps only the latest session)"
)
NOTE_ORIGIN_NOT_PROVED = (
    "origin not proved: no tab-map entry; may be a worker of a Run outside the scope"
)
NOTE_COULD_NOT_JOIN = (
    "could not join Orca workers to transcripts (tab map empty or stale)"
)
NOTE_ORIGIN_UNAVAILABLE = "origin unknown: Orca unavailable"
NOTE_ORIGIN_TRUNCATED = "origin unknown: worker list truncated"
NOTE_ORIGIN_CALL_FAILED = "origin unknown: worker list call failed"
NOTE_ORIGIN_RUN_NOT_CONFIRMED = "origin unknown: Run not confirmed"
NOTE_ORIGIN_TAB_MAP = "origin unknown: tab map unreadable"
NOTE_DUPLICATE_DISPATCH = "conflict: duplicate Dispatch rows disagree"
NOTE_INCONSISTENT = "conflict: inconsistent observation"
NOTE_WC13 = "WC-13 violation, review"
NOTE_ASK_COORDINATOR = "blocked contract under ask the coordinator; may be re-running"
NOTE_ORCA_NOT_OBSERVED = "blocked contract; Orca state not observed"
NOTE_EXITED_UNREADABLE = "Orca: exited; fenced evidence not readable"
NOTE_FUTURE = "timestamp in the future"
NOTE_TRANSCRIPT_UNREADABLE = "unscanned: transcript not readable"
NOTE_CONTRACT_UNREADABLE = "unscanned: contract not readable"
NOTE_PARTIAL = "partial: usable not yet judged"
NOTE_NO_CONTRACT = "no contract read for this row; finished needs a parsed contract"
REASON_WORKTREE_UNREADABLE = "unscanned: worktree not readable"
REASON_NOT_OBSERVABLE = (
    "report read, open PR and unmerged commits not observable"  # SPEC section 7
)

POLICY_REPORT_BLOCKED = "report blocked"
POLICY_ASK_COORDINATOR = "ask the coordinator"
POLICY_FROZEN = "frozen"

_RESUME_CODE = "E-RESUME-NEEDED"
_RULING_HALT_CODES = ("E-HALT-QA", "E-NO-RULING")
_SETTLED_OUTCOMES = ("succeeded", "partial", "failed")
_GUARD_REFUSED = "guard refused:"

_STOP_CODE = re.compile(r"\bE-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
_GATE_LINE = re.compile(
    r"^\s*On a blocked gate:\s*(report blocked|ask the coordinator)\s*\.?\s*$",
    re.MULTILINE,
)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def _settled(orca: OrcaObservation | None) -> bool:
    return orca is not None and orca.outcome in _SETTLED_OUTCOMES


def _stop_codes(contract: ContractRecord) -> tuple[str, ...]:
    text = " ".join(t for t in (contract.reason, contract.blocked_question) if t)
    return tuple(dict.fromkeys(_STOP_CODE.findall(text)))


def _freeze_codes(contract: ContractRecord) -> tuple[str, ...]:
    return tuple(c for c in _stop_codes(contract) if c != _RESUME_CODE)


def _ruling_halt(contract: ContractRecord) -> tuple[str, ...]:
    return tuple(c for c in _stop_codes(contract) if c in _RULING_HALT_CODES)


def _classification(
    class_name: str,
    rule: str,
    evidence: str,
    waiting_kind: str | None = None,
    notes: tuple[str, ...] = (),
) -> Classification:
    return Classification(
        class_name=class_name,
        waiting_kind=waiting_kind,
        rule=rule,
        evidence=evidence,
        notes=notes,
    )


def _unique(notes: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(notes))


# ---------------------------------------------------------------------------
# Rules (DESIGN 7.2 table; SPEC section 7)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Rule:
    name: str
    match: Callable[[SessionRow, SweepContext], Classification | None]


def _blocked_contract(
    row: SessionRow,
) -> tuple[Classification | None, tuple[str, ...]]:
    """Rule 1. Returns the match (or None) and the notes a decline attaches."""
    contract, orca = row.contract, row.orca
    if (
        contract is None
        or contract.worker_status != "blocked"
        or row.transcript_readable is False
    ):
        return None, ()
    halt = _ruling_halt(contract)
    if orca is None:
        if not halt:
            return None, (NOTE_ORCA_NOT_OBSERVED,)
        why = "Ruling halt " + ", ".join(halt) + "; no Orca row"
    elif _settled(orca):
        why = f"Orca row settled (outcome {orca.outcome})"
    elif row.gate_policy == POLICY_REPORT_BLOCKED:
        why = "gate_policy is report blocked"
    elif halt:
        why = "Ruling halt " + ", ".join(halt)
    else:
        live = orca.liveness_verdict == "live"
        ask = row.gate_policy in (POLICY_ASK_COORDINATOR, None)
        return None, (NOTE_ASK_COORDINATOR,) if live and ask else ()
    evidence = f"contract {contract.path} worker_status blocked; {why}"
    return _classification(C_WAITING, "blocked_contract", evidence, "a"), ()


def _exit_proof(row: SessionRow) -> tuple[Classification | None, tuple[str, ...]]:
    """Rule 2. Returns the match (or None) and the notes a decline attaches."""
    orca = row.orca
    if orca is None or orca.liveness_verdict != "exited":
        return None, ()
    if (
        row.transcript_readable is not False
        and orca.worker_done_seen is False
        and orca.fenced_evidence == "absent"
    ):
        evidence = (
            "liveness_verdict exited, worker_done_seen False, fenced_evidence absent"
        )
        return _classification(C_STALLED, "orca_exit_proof", evidence), ()
    unreadable = (
        orca.fenced_evidence == "unreadable" or row.transcript_readable is False
    )
    return None, (NOTE_EXITED_UNREADABLE,) if unreadable else ()


def _rule_blocked_contract(row: SessionRow, ctx: SweepContext) -> Classification | None:
    return _blocked_contract(row)[0]


def _rule_orca_exit_proof(row: SessionRow, ctx: SweepContext) -> Classification | None:
    return _exit_proof(row)[0]


def _rule_fenced(row: SessionRow, ctx: SweepContext) -> Classification | None:
    orca = row.orca
    if orca is not None and orca.fenced_evidence == "present":
        return _classification(C_FENCED, "fenced", "fenced_evidence present")
    return None


def _rule_waiting_signal(row: SessionRow, ctx: SweepContext) -> Classification | None:
    orca, contract = row.orca, row.contract
    if orca is not None and orca.agent_wait is not None:
        since = orca.agent_wait_since  # reserved: set by nothing yet (open item 6)
        notes: tuple[str, ...] = ()
        evidence = "agent_wait is non-null (worker-show agentWait)"
        if since is not None and since > ctx.now:
            notes = (NOTE_FUTURE,)
        elif since is not None:
            evidence += f"; waiting since {since.isoformat()}"
        return _classification(C_WAITING, "waiting_signal", evidence, "a", notes)
    if contract is not None and contract.worker_status == "failed":
        codes = _freeze_codes(contract)
        if codes:
            evidence = (
                "frozen plan: contract worker_status failed with STOP code "
                + ", ".join(codes)
            )
            return _classification(C_WAITING, "waiting_signal", evidence, "b")
    if orca is not None and orca.status == "ready":
        evidence = "ready Task: creator not observable; needs ownership review"
        return _classification(C_WAITING, "waiting_signal", evidence, "b")
    return None


def _rule_working(row: SessionRow, ctx: SweepContext) -> Classification | None:
    # Rule 5 cannot match in Phase 1 (DESIGN open item 6): the live names of the
    # ``agentWait`` field and of the ``live`` and ``in_progress`` values were never
    # captured, so a row that would reach it falls to the fallback. Once a read-only
    # capture records them, restore the four conditions of DESIGN 7.2 (SP-24):
    # liveness_verdict "live", status "in_progress", agent_wait_present True, agent_wait None.
    return None


def _rule_finished(row: SessionRow, ctx: SweepContext) -> Classification | None:
    orca, contract = row.orca, row.contract
    if orca is not None and orca.body_text is not None:
        lines = orca.body_text.splitlines()
        if lines and lines[0].startswith(_GUARD_REFUSED):
            evidence = f"Orca body_text first line starts with {_GUARD_REFUSED}"
            return _classification(C_FINISHED, "finished", evidence)
    if (
        _settled(orca)
        and orca is not None
        and contract is not None
        and contract.worker_status in _SETTLED_OUTCOMES
    ):
        evidence = (
            f"Orca outcome {orca.outcome}; parsed contract {contract.path} "
            f"worker_status {contract.worker_status}"
        )
        partial = "partial" in (orca.outcome, contract.worker_status)
        notes = (NOTE_PARTIAL,) if partial else ()
        return _classification(C_FINISHED, "finished", evidence, None, notes)
    return None


def _rule_idle(row: SessionRow, ctx: SweepContext) -> Classification | None:
    last = row.last_activity
    if (
        row.person_started is True
        and row.orca is None
        and row.transcript_readable is True
        and last is not None
        and last <= ctx.now
        and last < ctx.window_start
    ):
        age = int((ctx.now - last).total_seconds())
        evidence = (
            f"person_started True; last_activity {last.isoformat()} ({age} s old) "
            f"is before window_start {ctx.window_start.isoformat()}"
        )
        return _classification(C_IDLE, "idle", evidence)
    return None


def _rule_person_active(row: SessionRow, ctx: SweepContext) -> Classification | None:
    last = row.last_activity
    if (
        row.person_started is True
        and row.transcript_readable is True
        and last is not None
        and last >= ctx.window_start
    ):
        evidence = (
            f"person_started True; last_activity {last.isoformat()} is inside the "
            f"window from {ctx.window_start.isoformat()}"
        )
        return _classification(C_PERSON_ACTIVE, "person_active", evidence)
    return None


def _rule_fallback(row: SessionRow, ctx: SweepContext) -> Classification:
    orca = row.orca
    if orca is None:
        seen = "no Orca row"
    else:
        seen = (
            f"liveness_verdict {orca.liveness_verdict}, outcome {orca.outcome}, "
            f"status {orca.status}"
        )
    evidence = f"no rule 1 to 8 matched ({seen}; person_started {row.person_started})"
    # An Orca row that is settled but not finished lacks a contract (rule 6 needs one).
    notes = (NOTE_NO_CONTRACT,) if _settled(orca) and row.contract is None else ()
    return _classification(C_UNKNOWN, "fallback", evidence, notes=notes)


RULES: tuple[Rule, ...] = (
    Rule("blocked_contract", _rule_blocked_contract),
    Rule("orca_exit_proof", _rule_orca_exit_proof),
    Rule("fenced", _rule_fenced),
    Rule("waiting_signal", _rule_waiting_signal),
    Rule("working", _rule_working),
    Rule("finished", _rule_finished),
    Rule("idle", _rule_idle),
    Rule("person_active", _rule_person_active),
    Rule("fallback", _rule_fallback),
)


def _force_unknown(cls: Classification, notes: tuple[str, ...]) -> Classification:
    """Apply a could-not-determine outcome after rules 1 to 8, keeping the evidence."""
    return replace(
        cls,
        class_name=C_UNKNOWN,
        waiting_kind=None,
        rule="fallback",
        notes=_unique(cls.notes + notes),
    )


def classify(row: SessionRow, ctx: SweepContext) -> Classification:
    """Walk ``RULES`` in order; the first rule that returns a value wins."""
    result = None
    for rule in RULES:
        result = rule.match(row, ctx)
        if result is not None:
            break
    if result is None:  # RULES ends with the fallback, which always matches
        result = _rule_fallback(row, ctx)
    notes = list(_blocked_contract(row)[1] + _exit_proof(row)[1] + result.notes)
    if row.orca is not None and row.orca.parent is not None:
        notes.append(NOTE_WC13)
    if row.last_activity is not None and row.last_activity > ctx.now:
        notes.append(NOTE_FUTURE)
    result = replace(result, notes=_unique(notes))
    if row.transcript_readable is False:
        result = _force_unknown(result, (NOTE_TRANSCRIPT_UNREADABLE,))
    return result


def policy_of(row: SessionRow) -> str | None:
    """``"frozen"`` or None, independent of the class (GQ-96)."""
    contract = row.contract
    if contract is None:
        return None
    other_codes = bool(_freeze_codes(contract))
    if contract.worker_status == "failed" and other_codes:
        return POLICY_FROZEN
    if contract.worker_status == "blocked":
        implement = contract.command is not None and "sc:implement" in contract.command
        if other_codes or implement:
            return POLICY_FROZEN
    return None


# ---------------------------------------------------------------------------
# Packages and worktrees (SPEC package states, FR-013 to FR-015)
# ---------------------------------------------------------------------------

_PACKAGE_TESTS: dict[str, Callable[[PackageRecord], bool]] = {
    "conflict": lambda p: p.location == "both",
    "interrupted-archive": lambda p: p.archiving_marker,
    "archive-blocked": lambda p: p.location == "to-do" and p.has_final_line is True,
    "unfinished": lambda p: p.location == "to-do" and p.has_final_line is False,
    "archived": lambda p: p.location == "done",
}
_REMOVAL_BLOCKING_STATES = (
    "unfinished",
    "archive-blocked",
    "interrupted-archive",
    "conflict",
)


def package_state(pkg: PackageRecord) -> str:
    """First match in ``PACKAGE_STATES`` order; ``unknown`` when none matches."""
    for state in PACKAGE_STATES:
        test = _PACKAGE_TESTS.get(state)
        if test is not None and test(pkg):
            return state
    return "unknown"


def mark_shared_packages(
    worktrees: tuple[WorktreeState, ...],
) -> tuple[WorktreeState, ...]:
    """Flag a package id that is active in two or more worktrees (FR-015)."""
    where: dict[str, set[str]] = {}
    for w in worktrees:
        for p in w.packages:
            if p.active is True:
                where.setdefault(p.id, set()).add(w.path)
    shared = {pid for pid, paths in where.items() if len(paths) >= 2}
    return tuple(
        replace(
            w,
            shared_package_ids=tuple(
                sorted(
                    {p.id for p in w.packages if p.active is True and p.id in shared}
                )
            ),
        )
        for w in worktrees
    )


def removable(worktree: WorktreeState) -> tuple[str, str]:
    """``("no", <first FR-013 condition>)`` or ``("could not determine", <reason>)``."""
    if worktree.uncommitted is True:
        return "no", "uncommitted changes"
    if worktree.unpushed is True:
        return "no", f"unpushed branch: {worktree.upstream_note or 'ahead'}"
    if worktree.upstream_note == "no upstream":
        return "no", "unpushed branch: no upstream"
    if worktree.dev_tasks_unsaved is True:
        return "no", "unsaved path under .dev/tasks/"
    if worktree.frozen is True:
        return "no", "frozen plan"
    for pkg in sorted(worktree.packages, key=lambda p: (p.id, p.location)):
        state = package_state(pkg)
        if state in _REMOVAL_BLOCKING_STATES:
            return "no", f"package {pkg.id} is {state}"
    if worktree.shared_package_ids:
        pid = sorted(worktree.shared_package_ids)[0]
        return "no", f"active package {pid} shared with another worktree"
    if not worktree.status_read:
        return "could not determine", REASON_WORKTREE_UNREADABLE
    return "could not determine", REASON_NOT_OBSERVABLE


def safe_to_close(row: SessionRow, worktree: WorktreeState | None) -> SafeToClose:
    """Two review values; ``worktree`` is never ``yes`` in Phase 1 (FR-012)."""
    orca = row.orca
    if orca is None:
        terminal, t_reason = "could not determine", "no Orca row; terminal not observed"
    else:
        state, action = orca.terminal_state, orca.next_action
        seen = f"terminal_state={state}, next_action={action}"
        if state == "retained":
            terminal, t_reason = "no", f"terminal retained ({seen})"
        elif state is None or action is None:
            terminal, t_reason = "could not determine", f"not observed ({seen})"
        elif state == "reclaimable" and action == "release":
            terminal = "could not determine"
            t_reason = f"result read not observable ({seen})"
        else:
            terminal, t_reason = "no", f"not releasable ({seen})"
    if worktree is None:
        wt, w_reason = "could not determine", "worktree not observed"
    else:
        wt, w_reason = removable(worktree)
    return SafeToClose(
        terminal=terminal,
        worktree=wt,
        reason=f"terminal: {t_reason}; worktree: {w_reason}",
    )


# ---------------------------------------------------------------------------
# Orca rows, contracts and the transcript joins (DESIGN 7.2 Joins, D9)
# ---------------------------------------------------------------------------


def _merge_group(group: list[OrcaObservation]) -> OrcaObservation:
    """One identity for rows that share a Dispatch id but differ; no row wins."""
    values: dict[str, object] = {}
    for f in fields(OrcaObservation):
        seen = [getattr(g, f.name) for g in group]
        if all(v == seen[0] for v in seen):
            values[f.name] = seen[0]
        elif f.name == "run":
            values[f.name] = min(seen)
        elif f.default is not MISSING:
            values[f.name] = f.default
    for name in ("dispatch_started", "dispatch_ended", "dispatch_status"):
        values[name] = None
    return OrcaObservation(**values)  # type: ignore[arg-type]


def _merge_dispatches(
    orca_rows: tuple[OrcaObservation, ...],
) -> tuple[list[OrcaObservation], set[str]]:
    groups: dict[str, list[OrcaObservation]] = {}
    for o in orca_rows:
        bucket = groups.setdefault(o.dispatch, [])
        if o not in bucket:
            bucket.append(o)
    merged: list[OrcaObservation] = []
    conflicts: set[str] = set()
    for dispatch in sorted(groups):
        group = groups[dispatch]
        if len(group) == 1:
            merged.append(group[0])
        else:
            conflicts.add(dispatch)
            merged.append(_merge_group(group))
    return merged, conflicts


def _window(
    orca: OrcaObservation, collected_start: datetime, conflicts: set[str]
) -> tuple[datetime, datetime] | None:
    """The observable Dispatch window, or None (R3-B1)."""
    if orca.dispatch in conflicts or orca.dispatch_started is None:
        return None
    if orca.dispatch_ended is not None:
        return orca.dispatch_started, orca.dispatch_ended
    if orca.dispatch_status in ("pending", "dispatched"):
        return orca.dispatch_started, collected_start
    return None


def _gate_policy(spec_text: str | None) -> str | None:
    if spec_text is None:
        return None
    found = set(_GATE_LINE.findall(spec_text))
    if not found:
        return POLICY_REPORT_BLOCKED  # WC-3 default when the brief says nothing
    return next(iter(found)) if len(found) == 1 else None


def _contract_for(
    orca: OrcaObservation,
    contracts: tuple[ContractRecord, ...],
    all_rows: list[OrcaObservation],
) -> ContractRecord | None:
    """DESIGN names no key between a contract and its row; see the final report."""
    texts = [t for t in (orca.task_spec_text, orca.body_text) if t]
    # A report folder named in the text (``--report-dir <folder>``) names its contract.
    folders = {f for t in texts for f in report_folders(t, orca.worktree_path)}
    named = {
        c.path: c
        for c in contracts
        if str(c.path.parent) in folders or any(str(c.path) in t for t in texts)
    }
    if named:
        return next(iter(named.values())) if len(named) == 1 else None
    if orca.worktree_path is None:
        return None
    if sum(1 for r in all_rows if r.worktree_path == orca.worktree_path) != 1:
        return None
    under = [c for c in contracts if c.path.is_relative_to(Path(orca.worktree_path))]
    return under[0] if len(under) == 1 else None


@dataclass
class _Joins:
    joined: dict[str, TranscriptTail] = field(default_factory=dict)
    taken: set[int] = field(default_factory=set)  # indexes of joined transcripts
    row_notes: dict[str, list[str]] = field(default_factory=dict)
    forced: dict[str, list[str]] = field(default_factory=dict)
    left: dict[int, str] = field(default_factory=dict)  # transcript index -> note


def _add(book: dict[str, list[str]], key: str, note: str) -> None:
    notes = book.setdefault(key, [])
    if note not in notes:
        notes.append(note)


def _join_path_b(
    j: _Joins,
    idx: int,
    tail: TranscriptTail,
    rows: list[OrcaObservation],
    collected_start: datetime,
    conflicts: set[str],
) -> None:
    windows = {r.dispatch: _window(r, collected_start, conflicts) for r in rows}
    first = tail.first_record_ts
    if not tail.tail_complete or first is None:
        observable = False
        for r in rows:
            if windows[r.dispatch] is not None:
                observable = True
                _add(j.forced, r.dispatch, NOTE_TAIL_ONLY)
            else:
                _add(j.forced, r.dispatch, NOTE_WINDOW_NOT_OBSERVABLE)
        j.left[idx] = NOTE_TAIL_ONLY if observable else NOTE_WINDOW_NOT_OBSERVABLE
        return
    cut = first.replace(microsecond=0)
    miss: dict[str, str] = {}
    for r in rows:
        window = windows[r.dispatch]
        if window is None:
            miss[r.dispatch] = NOTE_WINDOW_NOT_OBSERVABLE
        elif cut > window[1]:
            miss[r.dispatch] = NOTE_PANE_MOVED
        elif cut < window[0]:
            miss[r.dispatch] = NOTE_BEFORE_WINDOW
    holders = [r for r in rows if r.dispatch not in miss]
    for dispatch, note in miss.items():
        _add(j.forced, dispatch, note)
    if len(holders) == 1:
        j.joined.setdefault(holders[0].dispatch, tail)
        j.taken.add(idx)
        _add(j.row_notes, holders[0].dispatch, NOTE_JOINED_BY_PANE)
    elif holders:
        for r in holders:
            _add(j.forced, r.dispatch, NOTE_SEVERAL_ROWS)
        j.left[idx] = NOTE_SEVERAL_ROWS
    else:
        order = (NOTE_PANE_MOVED, NOTE_BEFORE_WINDOW, NOTE_WINDOW_NOT_OBSERVABLE)
        j.left[idx] = next(n for n in order if n in miss.values())


def _join_transcripts(
    ordered: list[TranscriptTail],
    tab_map: tuple[TabMapEntry, ...],
    rows: list[OrcaObservation],
    collected_start: datetime,
    conflicts: set[str],
) -> _Joins:
    j = _Joins()
    for idx, tail in enumerate(ordered):
        sid = tail.session_id
        if sid is None:
            continue
        a_rows = [r for r in rows if r.session_join == sid]
        if a_rows:  # path A: the Orca field holds the Claude session id
            if len(a_rows) == 1:
                j.joined.setdefault(a_rows[0].dispatch, tail)
                j.taken.add(idx)
            else:
                for r in a_rows:
                    _add(j.forced, r.dispatch, NOTE_SEVERAL_ROWS)
                j.left[idx] = NOTE_SEVERAL_ROWS
            continue
        keys = {k for e in tab_map if e.session_id == sid for k in _entry_keys(e)}
        b_rows = [
            r for r in rows if r.session_join is not None and r.session_join in keys
        ]
        if b_rows:
            _join_path_b(j, idx, tail, b_rows, collected_start, conflicts)
    return j


def _entry_keys(entry: TabMapEntry) -> tuple[str, str]:
    return entry.file_name, entry.terminal_handle


def _origin_unknown(inp: SweepInput, ctx: SweepContext) -> tuple[str, ...]:
    """The five list-incomplete cases (SPEC FR-010 and R3-B3), in note order.

    Known gap: a worker-list row with a missing or empty Dispatch id is dropped in ``probes`` and
    leaves only an unscanned ``orca worker-list <run> row <i>`` source row, which none of the five
    cases reads (a Run whose rows are all dropped would look complete); unverified for real Orca.
    """
    source = {s.name: s for s in inp.sources}
    notes: list[str] = []
    if not inp.orca_available:
        notes.append(NOTE_ORIGIN_UNAVAILABLE)
    if inp.truncated:
        notes.append(NOTE_ORIGIN_TRUNCATED)
    if inp.orca_available:
        runs_seen = {o.run for o in inp.orca_rows}
        failed = unconfirmed = False
        for run in ctx.runs:
            listing = source.get(f"orca worker-list {run}")
            if listing is not None and listing.unscanned is not None:
                failed = True
                continue
            tasks = source.get(f"orca task-list {run}")
            if (
                run not in runs_seen
                and tasks is not None
                and tasks.unscanned is not None
            ):
                unconfirmed = True
        if failed:
            notes.append(NOTE_ORIGIN_CALL_FAILED)
        if unconfirmed:
            notes.append(NOTE_ORIGIN_RUN_NOT_CONFIRMED)
    tabs = source.get("ccsession orca-tabs")
    if tabs is not None and tabs.unscanned is not None:
        notes.append(NOTE_ORIGIN_TAB_MAP)
    return tuple(notes)


@dataclass(frozen=True)
class _Guard:
    origin: tuple[str, ...]
    unobservable: bool  # first case: a scoped Dispatch row has no session_join
    no_join: bool  # second case: workers returned, no transcript joined
    unmatched: bool  # third case (path B): a session_join matches no tab-map entry
    earlier_pane: bool  # fourth case (path B): a scoped Dispatch row exists

    @property
    def failed(self) -> bool:
        return self.unobservable or self.no_join or self.unmatched or self.earlier_pane


def _guard(
    inp: SweepInput, ctx: SweepContext, rows: list[OrcaObservation], j: _Joins
) -> _Guard:
    keys = {k for e in inp.tab_map for k in _entry_keys(e)}
    path_b = JOIN_PATH == "B"
    # A ready Task has no Dispatch, so it is not a scoped Dispatch row (FR-010 cases).
    rows = [r for r in rows if r.status != "ready"]
    return _Guard(
        origin=_origin_unknown(inp, ctx),
        unobservable=any(r.session_join is None for r in rows),
        no_join=bool(rows) and not j.joined,
        unmatched=path_b
        and any(
            r.session_join is not None and r.session_join not in keys for r in rows
        ),
        earlier_pane=path_b and bool(rows),
    )


def _person_origin(
    idx: int, has_entry: bool, j: _Joins, g: _Guard
) -> tuple[bool | None, tuple[str, ...]]:
    """``person_started`` and the notes of a transcript that joined no Orca row."""
    notes = list(g.origin)
    if idx in j.left:  # left unjoined by the tail, window or several-rows rule
        notes.append(j.left[idx])
        return None, tuple(notes)
    if g.no_join or g.unmatched:
        notes.append(NOTE_COULD_NOT_JOIN)
    if g.unobservable:
        notes.append(NOTE_JOIN_NOT_OBSERVABLE)
    if g.earlier_pane and not has_entry:
        notes.append(NOTE_EARLIER_PANE)
    if has_entry:
        notes.append(NOTE_PANE_NOT_SCOPED)
    if g.origin or g.failed or has_entry:
        return None, tuple(notes)
    notes.append(NOTE_ORIGIN_NOT_PROVED)
    return True, tuple(notes)


# ---------------------------------------------------------------------------
# Row building and classify_all
# ---------------------------------------------------------------------------


def _last_activity(tail: TranscriptTail) -> tuple[datetime, str]:
    if tail.last_record_ts is not None:
        return tail.last_record_ts, "last_record_ts of the last complete record"
    return tail.mtime, "transcript st_mtime"


def _lifecycle(orca: OrcaObservation | None) -> str:
    # REPORT:1248: source is the Orca outcome; settled -> settled, else running;
    # no outcome observed -> unknown.
    if orca is None or orca.outcome is None:
        return "unknown"
    return "settled" if _settled(orca) else "running"


def _health(contract: ContractRecord | None) -> str:
    # REPORT:1248: a failed contract gives "failed result"; liveness "unverifiable" and
    # everything else give "unknown" ("no issue observed" has no Phase 1 source).
    if contract is not None and contract.worker_status == "failed":
        return "failed result"
    return "unknown"


def _result(contract: ContractRecord | None) -> str:
    if contract is None or contract.worker_status is None:
        return "unknown"
    if contract.worker_status == "blocked":
        return "null"  # REPORT:1248, blocked prints null
    return contract.worker_status


def _source_flags(
    sources: tuple[SourceCoverage, ...], dispatch: str | None, transcript: Path | None
) -> tuple[str, ...]:
    """Notes from per-input source rows named ``contract <dispatch>``/``transcript <path>``.

    DESIGN 7.2 gives the notes but no model field carries them, so this reads an
    ``unscanned`` source row under those two names (see the final report).
    """
    wanted: dict[str, str] = {}
    if dispatch is not None:
        wanted[f"contract {dispatch}"] = NOTE_CONTRACT_UNREADABLE
    if transcript is not None:
        wanted[f"transcript {transcript}"] = NOTE_TRANSCRIPT_UNREADABLE
    notes: set[str] = set()
    for s in sources:
        if s.name in wanted and s.unscanned is not None:
            notes.add(
                NOTE_INCONSISTENT if "inconsistent" in s.unscanned else wanted[s.name]
            )
    return tuple(sorted(notes))


def _norm(path: str) -> str:
    return path.rstrip("/") or "/"


def _prepare_worktrees(
    worktrees: tuple[WorktreeState, ...],
    frozen_paths: frozenset[str] = frozenset(),
) -> tuple[WorktreeState, ...]:
    """Order, mark package states and shared ids, and set ``removable``.

    ``frozen_paths`` holds the normalised paths of worktrees that host a frozen row;
    those get ``frozen=True`` (FR-013), the others keep what they had (never False).
    """
    staged = tuple(
        replace(
            w,
            packages=tuple(
                replace(p, state=package_state(p))
                for p in sorted(w.packages, key=lambda p: (p.id, p.location))
            ),
            frozen=True if _norm(w.path) in frozen_paths else w.frozen,
        )
        for w in sorted(worktrees, key=lambda w: w.path)
    )
    out = []
    for w in mark_shared_packages(staged):
        value, reason = removable(w)
        out.append(replace(w, removable=value, removable_reason=reason))
    return tuple(out)


def _show_cut(sources: tuple[SourceCoverage, ...]) -> set[str]:
    """Names of ``worker-show`` source rows that the show cap or time budget cut (FR-020)."""
    return {
        s.name
        for s in sources
        if s.unscanned is not None
        and (SHOW_CAP_REASON in s.unscanned or TIME_BUDGET_REASON in s.unscanned)
    }


def classify_all(inp: SweepInput, ctx: SweepContext) -> SweepResult:
    """Join, classify and summarise every row; the result ignores input order."""
    orca_rows, conflicts = _merge_dispatches(inp.orca_rows)
    ordered = sorted(inp.transcripts, key=lambda t: (t.session_id or "", str(t.path)))
    joins = _join_transcripts(
        ordered, inp.tab_map, orca_rows, inp.collected_start, conflicts
    )
    guard = _guard(inp, ctx, orca_rows, joins)

    built: list[tuple[SessionRow, tuple[str, ...], tuple[str, ...], str]] = []
    for o in orca_rows:
        tail = joins.joined.get(o.dispatch)
        contract = _contract_for(o, inp.contracts, orca_rows)
        last, source = _last_activity(tail) if tail is not None else (None, "")
        row = SessionRow(
            id=o.dispatch,
            person_started=False if tail is not None else None,
            orca=o,
            contract=contract,
            transcript_path=tail.path if tail is not None else None,
            transcript_readable=tail.readable if tail is not None else None,
            last_activity=last,
            gate_policy=_gate_policy(o.task_spec_text),
            row_id=f"orca:{o.dispatch}",
            lifecycle=_lifecycle(o),
            health=_health(contract),
            result=_result(contract),
        )
        forced = list(joins.forced.get(o.dispatch, ()))
        if o.dispatch in conflicts:
            forced.insert(0, NOTE_DUPLICATE_DISPATCH)
        forced += _source_flags(inp.sources, o.dispatch, tail.path if tail else None)
        info = tuple(joins.row_notes.get(o.dispatch, ()))
        built.append((row, info, _unique(forced), source))

    for idx, tail in enumerate(ordered):
        if idx in joins.taken:
            continue
        entries = [e for e in inp.tab_map if e.session_id == tail.session_id]
        person, notes = _person_origin(idx, bool(entries), joins, guard)
        last, source = _last_activity(tail)
        age_ok = person is True and last <= ctx.now
        stale = last < ctx.window_start
        sid = tail.session_id if tail.session_id is not None else tail.path.stem
        row = SessionRow(
            id=sid,
            person_started=person,
            orca=None,
            contract=None,
            transcript_path=tail.path,
            transcript_readable=tail.readable,
            last_activity=last,
            gate_policy=None,
            row_id=f"transcript:{sid}",
            freshness=("stale" if stale else "fresh") if age_ok else "unknown",
            freshness_age_s=int((ctx.now - last).total_seconds()) if age_ok else None,
        )
        flags = _source_flags(inp.sources, None, tail.path)
        built.append((row, notes, flags, source))

    # A worktree that hosts a frozen row is a frozen plan (FR-013); needs the rows first.
    frozen_paths = frozenset(
        _norm(b[0].orca.worktree_path)
        for b in built
        if b[0].orca is not None
        and b[0].orca.worktree_path is not None
        and policy_of(b[0]) == POLICY_FROZEN
    )
    worktrees = _prepare_worktrees(inp.worktrees, frozen_paths)
    by_path = {_norm(w.path): w for w in worktrees}

    classified: list[ClassifiedRow] = []
    for row, info, forced, source in sorted(built, key=lambda b: b[0].row_id):
        cls = classify(row, ctx)
        if row.orca is None:
            cls = replace(cls, notes=_unique(info + cls.notes))
        else:
            cls = replace(cls, notes=_unique(cls.notes + info))
        if cls.rule in ("idle", "person_active"):
            cls = replace(cls, evidence=f"{cls.evidence}; last_activity from {source}")
        if forced:
            cls = _force_unknown(cls, forced)
        wt = None
        if row.orca is not None and row.orca.worktree_path is not None:
            wt = by_path.get(_norm(row.orca.worktree_path))
        classified.append(
            ClassifiedRow(
                row=row,
                classification=cls,
                policy=policy_of(row),
                safe=safe_to_close(row, wt),
            )
        )

    counts = {name: 0 for name in CLASSES}
    for c in classified:
        counts[c.classification.class_name] += 1
    historical = counts[C_IDLE]
    cut = _show_cut(inp.sources)
    bound_reached = sum(1 for o in orca_rows if f"orca worker-show {o.dispatch}" in cut)
    summary: dict[str, object] = {
        "counts": counts,
        "bound_reached": bound_reached,
        "visible": len(classified) - historical,
        "historical": historical,
        "total": len(classified),
        # shortcut: always true in Phase 1, because the report always prints "remote hosts
        # not scanned" (report.py header and "What I could not determine"); make it
        # conditional when remote hosts are scanned.
        "total_is_lower_bound": True,
    }
    return SweepResult(
        rows=tuple(classified),
        worktrees=worktrees,
        waiting_a=tuple(
            c.row.row_id for c in classified if c.classification.waiting_kind == "a"
        ),
        waiting_b=tuple(
            c.row.row_id for c in classified if c.classification.waiting_kind == "b"
        ),
        summary=summary,
        context=ctx,
        sources=inp.sources,
        orca_available=inp.orca_available,
        orca_binary=inp.orca_binary,
        orca_version=inp.orca_version,
        truncated=inp.truncated,
        collected_start=inp.collected_start,
        collected_end=inp.collected_end,
    )
