"""Pure renderer for ``superclaude sweep``: Markdown report and JSON v1 (DESIGN 7.1, 7.4, 7.5).

Every function here is a pure function of a ``SweepResult`` and a ``SweepContext``: it
reads no clock, no file and no environment variable, and it starts no process. Only the
standard library ``re`` and ``unicodedata`` and the ``models`` module are imported. The
publication of the report (the one write) lives in ``commands``, never here.
"""

from __future__ import annotations

import re
import unicodedata

from .models import (
    CLASSES,
    JSON_SCHEMA_VERSION,
    ClassifiedRow,
    SweepContext,
    SweepResult,
    WorktreeState,
)

CHECKED_ORCA_VERSION: str = "1.4.245"
CELL_MAX: int = 200  # SP-23 (D4): a table cell is cut to this many characters

_IDLE = CLASSES[5]  # "idle": the Historical sessions rows
_UNKNOWN = CLASSES[7]  # "could not determine"

NO_RECORDS = "No matching records. This is not an all-clear."
DISTINCT = "Distinct affected sessions: {n} (set union, not a sum)"
BOUND_LINE = "[Show cap or time budget reached; row total is a lower bound]"
PAGE_LINE = "[Orca rows: 100 shown; total is a lower bound (paging not yet captured)]"
WORKTREES_LINE = "[child worktrees not discovered: Orca unavailable; worktree count is a lower bound]"
# Orca answered, but the ``orca worktree ps`` source is unscanned (DESIGN 7.5): the reason is
# that source row's ``unscanned`` text, passed through ``sanitize``.
WORKTREES_PS_LINE = (
    "[child worktrees not discovered: orca worktree ps unscanned ({reason}); "
    "worktree count is a lower bound]"
)
COULD_NOT_JOIN = "could not join Orca workers to transcripts (tab map empty or stale)"
WC13_NOTE = "WC-13 violation, review"
SP24_LINE = (
    "Stalled and fenced are not observed in Phase 1; a zero count does not mean "
    "none occurred."
)
SAFE_TO_CLOSE_LINE = (
    "Safe to close never prints yes in Phase 1: each cell gives the terminal value, "
    "the worktree value and, in parentheses, the reason for both."
)

# The ``next inspection`` value per rule name: what to read or check, nothing more.
# One rule can match rows with different evidence, so ``waiting_signal`` and ``fallback``
# name what the row's own Evidence cell names and stay true for every outcome of the rule.
NEXT_INSPECTION: dict[str, str] = {
    "blocked_contract": "read the contract's blocked question and the worker's last "
    "transcript lines",
    "orca_exit_proof": "read the worker's last transcript lines and its Orca worker-show "
    "result",
    "fenced": "read the fencing evidence named in the row",
    "waiting_signal": "read what the Evidence cell names: the Orca agent-wait entry and the "
    "worker's last transcript lines, the contract, or the ready Task in Orca task-list",
    "working": "read the worker's last transcript lines to confirm it is active",
    "finished": "read the worker's report file and its contract",
    "idle": "read the session's last transcript lines",
    "person_active": "read the session's last transcript lines",
    "fallback": "read the row's Evidence and Notes cells, then the sources marked "
    "unscanned in Source coverage (if none, the session's last transcript lines)",
}
_NEXT_DEFAULT = "read the row's evidence and the source it names"

_SESSION_DIMENSIONS = (
    "Lifecycle",
    "Phase",
    "Health",
    "Approval",
    "Freshness",
    "Result",
    "Admission",
    "Evidence packet",
    "Policy",
    "Tests/review",
)


# --- Small helpers ----------------------------------------------------------------------


def _iso(value: object) -> str | None:
    """UTC ISO 8601 with a ``Z`` suffix for an aware UTC datetime; None for anything else."""
    if value is None or not hasattr(value, "isoformat"):
        return None
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")  # type: ignore[attr-defined]


def _window_text(window: object) -> str:
    seconds = int(window.total_seconds())  # type: ignore[attr-defined]
    if seconds > 0 and seconds % 3600 == 0:
        return f"{seconds // 3600}h"
    if seconds > 0 and seconds % 60 == 0:
        return f"{seconds // 60}m"
    return f"{seconds}s"


def _yn(value: bool | None) -> str:
    return "unknown" if value is None else ("yes" if value else "no")


def _age_text(seconds: int | None) -> str:
    if seconds is None:
        return "unknown"
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m"
    if seconds < 86400:
        return f"{seconds // 3600}h {seconds % 3600 // 60}m"
    return f"{seconds // 86400}d {seconds % 86400 // 3600}h"


def _wait_age_s(row: ClassifiedRow, ctx: SweepContext) -> int | None:
    """Seconds since a wait began (SP-15): the earlier of a blocked contract's file time and
    the agentWait time; None when neither is known or the earlier one is in the future."""
    orca, contract = row.row.orca, row.row.contract
    times = []
    if contract is not None and contract.worker_status == "blocked":
        times.append(contract.mtime)
    if orca is not None and orca.agent_wait is not None:
        times.append(orca.agent_wait_since)
    known = [t for t in times if t is not None]
    if not known:
        return None
    seconds = int((ctx.now - min(known)).total_seconds())
    return seconds if seconds >= 0 else None


def _table(headers: tuple[str, ...], rows: list[tuple[str, ...]]) -> str:
    """A Markdown table; every cell goes through ``cell`` and an empty cell is ``none``."""
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(c) or "none" for c in row) + " |")
    return "\n".join(lines)


def _is_ready(row: ClassifiedRow) -> bool:
    return row.row.orca is not None and row.row.orca.status == "ready"


def _rows(result: SweepResult, class_name: str) -> list[ClassifiedRow]:
    return [r for r in result.rows if r.classification.class_name == class_name]


def _distinct(ids: object) -> str:
    return DISTINCT.format(n=len(set(ids)))  # type: ignore[call-overload]


def _version_line(observed: str | None) -> str:
    if observed is not None and observed.split("-", 1)[0] == CHECKED_ORCA_VERSION:
        return f"Orca lock risk: unlikely (checked for Orca {CHECKED_ORCA_VERSION})"
    seen = sanitize(observed) if observed else "unknown"
    return (
        f"Orca lock risk: UNVERIFIED (checked for Orca {CHECKED_ORCA_VERSION}; "
        f"observed {seen})"
    )


def _worktrees_line(result: SweepResult) -> str | None:
    """The header banner for incomplete worktree discovery, or None when it is complete."""
    if not result.orca_available:
        return WORKTREES_LINE
    for s in result.sources:
        if s.name == "orca worktree ps" and s.unscanned:
            return WORKTREES_PS_LINE.format(reason=sanitize(s.unscanned))
    return None


# --- Sections (DESIGN 7.5, in order) ----------------------------------------------------


def _header(result: SweepResult, ctx: SweepContext) -> str:
    summary = result.summary
    shown, total = summary["visible"], summary["total"]
    sources = " . ".join(
        sanitize(f"{s.name} {s.coverage}")
        + (f" (age {s.age_seconds}s)" if s.age_seconds is not None else "")
        for s in result.sources
    )
    lines = [
        f"READ ONLY . observed {_iso(ctx.now)} . collected "
        f"{_iso(result.collected_start)} to {_iso(result.collected_end)} "
        "(not an atomic runtime snapshot)",
        f"Scope: Runs {sanitize(', '.join(ctx.runs)) or 'none'} . worktrees "
        f"{len(result.worktrees)} . sessions {shown}/{total} "
        f"(lower bound: remote hosts not scanned) . window {_window_text(ctx.window)}",
        f"Orca binary: {sanitize(result.orca_binary)}",
        f"Sources: {sources or 'none'}",
        "Messages coverage: partial",
        _version_line(result.orca_version),
        "Untracked paths: listed per file (--untracked-files=all); not observed in a "
        "worktree whose status was unread",
    ]
    worktrees_line = _worktrees_line(result)
    if worktrees_line is not None:
        lines.append(worktrees_line)
    if int(summary["bound_reached"]) >= 1:  # type: ignore[call-overload]
        lines.append(BOUND_LINE)
    if result.truncated:
        lines.append(PAGE_LINE)
    return "\n".join(lines)


def _source_coverage(result: SweepResult, ctx: SweepContext) -> str:
    out = ["## Source coverage", ""]
    if not result.sources:
        out.append(NO_RECORDS)
        return "\n".join(out)
    rows = [
        (
            s.name,
            s.coverage,
            "unknown" if s.age_seconds is None else str(s.age_seconds),
            f"unscanned: {s.unscanned}" if s.unscanned else "",
        )
        for s in result.sources
    ]
    out.append(_table(("Source", "Coverage", "Age (s)", "Unscanned"), rows))
    return "\n".join(out)


def _waiting_a(result: SweepResult, ctx: SweepContext) -> str:
    rows = [r for r in result.rows if r.classification.waiting_kind == "a"]
    aged = [(_wait_age_s(r, ctx), r) for r in rows]
    # Oldest first, tie-break by ID; rows of unknown age follow as their own group.
    known = sorted(
        ((a, r) for a, r in aged if a is not None),
        key=lambda p: (-p[0], p[1].row.row_id),
    )
    unknown = sorted(
        ((a, r) for a, r in aged if a is None), key=lambda p: p[1].row.row_id
    )
    table_rows = []
    for age, r in known + unknown:
        row, orca = r.row, r.row.orca
        affected = ", ".join(
            part
            for part in (
                f"Run {orca.run}" if orca is not None else "",
                f"worktree {orca.worktree_path}" if orca and orca.worktree_path else "",
            )
            if part
        )
        table_rows.append(
            (
                row.row_id,
                _age_text(age),
                (row.contract.blocked_question if row.contract else None) or "unknown",
                "unknown",
                "unknown",
                affected or "unknown",
                r.classification.evidence,
            )
        )
    out = ["## Waiting on a person (a)", ""]
    if table_rows:
        headers = (
            "ID",
            "Age",
            "Question",
            "Requested by",
            "Decision owner",
            "Affected",
        )
        out.append(_table((*headers, "Evidence"), table_rows))
        out += ["", _distinct(r.row.row_id for r in rows)]
    else:
        out.append(NO_RECORDS)
    out += ["", "Seen is not resolved", "Answered: could not determine"]
    return "\n".join(out)


def _waiting_b(result: SweepResult, ctx: SweepContext) -> str:
    rows = [r for r in result.rows if r.classification.waiting_kind == "b"]
    frozen = sorted((r for r in rows if not _is_ready(r)), key=lambda r: r.row.row_id)
    ready = sorted((r for r in rows if _is_ready(r)), key=lambda r: r.row.row_id)
    out = ["## Waiting on a person (b)", ""]
    if frozen:
        out.append(
            _table(
                ("ID", "Policy reason", "Evidence"),
                [
                    (r.row.row_id, r.classification.rule, r.classification.evidence)
                    for r in frozen
                ],
            )
        )
    else:
        out.append(NO_RECORDS)
    out += [
        "",
        "### Ready Tasks needing ownership review (creator not observable in Phase 1)",
        "",
    ]
    if ready:
        out.append(
            _table(
                ("ID", "Run", "Evidence"),
                [
                    (
                        r.row.row_id,
                        r.row.orca.run if r.row.orca else "",
                        r.classification.evidence,
                    )
                    for r in ready
                ],
            )
        )
    else:
        out.append(NO_RECORDS)
    out += ["", f"Ready Tasks: {len(ready)}"]
    if rows:
        out += ["", _distinct(r.row.row_id for r in rows)]
    return "\n".join(out)


def _could_not_determine(result: SweepResult, ctx: SweepContext) -> str:
    rows = sorted(_rows(result, _UNKNOWN), key=lambda r: r.row.row_id)
    out = ["## Could not determine", ""]
    if not rows:
        out.append(NO_RECORDS)
        return "\n".join(out)
    out.append(
        _table(
            ("ID", "Rule", "Evidence", "Notes"),
            [
                (
                    r.row.row_id,
                    r.classification.rule,
                    r.classification.evidence,
                    "; ".join(r.classification.notes),
                )
                for r in rows
            ],
        )
    )
    if any(COULD_NOT_JOIN in r.classification.notes for r in rows):
        out += ["", COULD_NOT_JOIN]
    out += ["", _distinct(r.row.row_id for r in rows)]
    return "\n".join(out)


def _retained_problems(result: SweepResult, ctx: SweepContext) -> str:
    lines: list[str] = []
    shared: dict[str, list[str]] = {}
    for w in result.worktrees:
        for pkg in w.packages:
            if pkg.state == "interrupted-archive":
                lines.append(
                    f"Worktree {sanitize(w.path)}: package {sanitize(pkg.id)} has an "
                    "interrupted archive (.archiving marker present)"
                )
            elif pkg.state == "conflict":
                lines.append(
                    f"Worktree {sanitize(w.path)}: package {sanitize(pkg.id)} is in both "
                    "to-do/ and done/ (conflict)"
                )
        for pid in w.shared_package_ids:
            shared.setdefault(pid, []).append(w.path)
    for pid in sorted(shared):
        where = ", ".join(sanitize(p) for p in shared[pid])
        lines.append(f"Active package {sanitize(pid)} is in several worktrees: {where}")
    for r in sorted(result.rows, key=lambda r: r.row.row_id):
        if WC13_NOTE in r.classification.notes:
            lines.append(f"{sanitize(r.row.row_id)}: {WC13_NOTE}")
    bound = int(result.summary["bound_reached"])  # type: ignore[call-overload]
    if bound >= 1:
        lines.append(
            f"Show cap or time budget reached: {bound} Orca rows have no worker-show result"
        )
    out = ["## Retained problems", ""]
    out += [f"- {line}" for line in lines] if lines else [NO_RECORDS]
    return "\n".join(out)


def _dimension_cells(r: ClassifiedRow) -> tuple[str, ...]:
    row = r.row
    freshness = row.freshness
    if row.freshness_age_s is not None:
        freshness = f"{row.freshness} ({row.freshness_age_s}s)"
    return (
        row.lifecycle,
        row.phase,
        row.health,
        row.approval,
        freshness,
        row.result,
        row.admission,
        row.evidence_packet,
        "frozen" if r.policy == "frozen" else "unknown",  # never "not frozen" (OQ-11)
        row.tests_review if row.tests_review is not None else "unavailable",
    )


def _sessions(result: SweepResult, ctx: SweepContext) -> str:
    rows = sorted(
        (r for r in result.rows if r.classification.class_name != _IDLE),
        key=lambda r: r.row.row_id,
    )
    total = result.summary["total"]
    out = [f"## Sessions ({len(rows)}/{total})", "", SP24_LINE, SAFE_TO_CLOSE_LINE, ""]
    if not rows:
        out.append(NO_RECORDS)
        return "\n".join(out)
    headers = (
        "ID",
        *_SESSION_DIMENSIONS,
        "Class",
        "Rule",
        "Evidence",
        "Safe to close (terminal / worktree)",
        "Notes",
        "Next inspection",
    )
    body = []
    for r in rows:
        c = r.classification
        label = c.class_name + (f" ({c.waiting_kind})" if c.waiting_kind else "")
        body.append(
            (
                r.row.row_id,
                *_dimension_cells(r),
                label,
                c.rule,
                c.evidence,
                f"{r.safe.terminal} / {r.safe.worktree}"
                + (f" ({r.safe.reason})" if r.safe.reason else ""),
                "; ".join(c.notes),
                NEXT_INSPECTION.get(c.rule, _NEXT_DEFAULT),
            )
        )
    out.append(_table(headers, body))
    return "\n".join(out)


def _package_states(w: WorktreeState) -> str:
    return "; ".join(f"{p.id}: {p.state}" for p in w.packages) or "none"


def _worktrees(result: SweepResult, ctx: SweepContext) -> str:
    out = ["## Worktrees", ""]
    if not result.worktrees:
        out.append(NO_RECORDS)
        return "\n".join(out)
    rows = [
        (
            w.path,
            _yn(w.uncommitted),
            _yn(w.unpushed) + (f" ({w.upstream_note})" if w.upstream_note else ""),
            _yn(w.dev_tasks_unsaved),
            _package_states(w),
            w.removable,
            w.removable_reason or "",
        )
        for w in sorted(result.worktrees, key=lambda w: w.path)
    ]
    headers = (
        "Path",
        "Uncommitted",
        "Unpushed",
        ".dev/tasks/ unsaved",
        "Package state",
    )
    out.append(_table((*headers, "Removable", "Reason"), rows))
    return "\n".join(out)


def _historical(result: SweepResult, ctx: SweepContext) -> str:
    rows = sorted(_rows(result, _IDLE), key=lambda r: r.row.row_id)
    out = ["## Historical sessions", ""]
    if not rows:
        out.append(NO_RECORDS)
        return "\n".join(out)
    out.append(
        _table(
            ("ID", "Last activity", "Evidence"),
            [
                (
                    r.row.row_id,
                    _iso(r.row.last_activity) or "unknown",
                    r.classification.evidence,
                )
                for r in rows
            ],
        )
    )
    return "\n".join(out)


def _shift_brief(result: SweepResult, ctx: SweepContext) -> str:
    needing = {
        r.row.row_id
        for r in result.rows
        if r.classification.waiting_kind in ("a", "b")
        or r.classification.class_name == _UNKNOWN
    }
    return "\n".join(
        [
            "## Shift Brief",
            "",
            "Sessions waiting on a person (a or b) or could not determine:",
            _distinct(needing),
            "Raw logs are omitted. This brief is not an assurance of completeness.",
        ]
    )


def _not_determined(result: SweepResult, ctx: SweepContext) -> str:
    lines = [
        f"- {sanitize(s.name)}: unscanned: {sanitize(s.unscanned)}"
        for s in result.sources
        if s.unscanned
    ]
    if not result.orca_available:
        lines.append(
            "- Orca became unavailable; the Orca sources marked unscanned above were not read"
        )
    if result.truncated:
        lines.append(
            "- A worker list filled its page; the Orca row total is a lower bound"
        )
    lines.append("- Remote hosts were not scanned; the session count is a lower bound")
    lines.append(
        "- Messages coverage is partial: pending questions cannot be read without "
        "consuming them"
    )
    return "\n".join(["## What I could not determine", "", *lines])


def _footer(result: SweepResult, ctx: SweepContext) -> str:
    listing = [f"- {sanitize(s.name)}: {sanitize(s.coverage)}" for s in result.sources]
    return "\n".join(["Inspection only.", *listing, "Report complete"])


SECTIONS = (
    _header,
    _source_coverage,
    _waiting_a,
    _waiting_b,
    _could_not_determine,
    _retained_problems,
    _sessions,
    _worktrees,
    _historical,
    _shift_brief,
    _not_determined,
    _footer,
)

# --- sanitize, cell, render, to_json ----------------------------------------------------

_ESCAPES = re.compile(
    r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)?"  # OSC
    r"|[\x1b\x9b]\[[0-?]*[ -/]*[@-~]?"  # CSI
    r"|\x1b[@-Z\\-_]?"  # other two-character escapes
)


def sanitize(text: object) -> str:
    """Make untrusted text safe for one table cell or line (FR-016, GQ-107).

    Strips ESC, CSI and OSC sequences, control and bidi characters and carriage returns,
    folds newlines to a space, and neutralises backslashes, ``|``, HTML tags and Markdown
    links.
    """
    s = _ESCAPES.sub("", "" if text is None else str(text))
    kept = []
    for ch in s:
        category = unicodedata.category(ch)
        if ch == "\r":
            continue
        if ch in "\n\t\v\f\x85" or category in ("Zl", "Zp"):
            kept.append(" ")
        elif category in ("Cc", "Cf", "Cs", "Co"):
            continue
        else:
            kept.append(ch)
    s = "".join(kept)
    # The backslash goes first, so a backslash in the text cannot pair with one added below.
    for old, new in (
        ("\\", "\\\\"),
        ("|", "\\|"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ("[", "\\["),
        ("]", "\\]"),
    ):
        s = s.replace(old, new)
    return s


def cell(text: object) -> str:
    """``sanitize``, then cut to ``CELL_MAX`` characters ending in ``...``."""
    s = sanitize(text)
    return s if len(s) <= CELL_MAX else s[: CELL_MAX - 3] + "..."


def render(result: SweepResult, ctx: SweepContext) -> str:
    """The whole report: every ``SECTIONS`` block in order, ending ``Report complete``."""
    return "\n\n".join(section(result, ctx) for section in SECTIONS) + "\n"


def to_json(
    result: SweepResult, ctx: SweepContext, report_path: str
) -> dict[str, object]:
    """The JSON v1 object (DESIGN 7.4): every key present, values sanitized but never cut."""
    summary = result.summary
    counts = summary["counts"]
    return {
        "schema_version": JSON_SCHEMA_VERSION,
        "observed_at": _iso(ctx.now),
        "collected": {
            "start": _iso(result.collected_start),
            "end": _iso(result.collected_end),
        },
        "scope": {
            "runs": [sanitize(r) for r in ctx.runs],
            "root": sanitize(ctx.root),
            "worktrees": len(result.worktrees),
        },
        "window": _window_text(ctx.window),
        "orca_available": result.orca_available,
        "sources": [
            {
                "name": sanitize(s.name),
                "coverage": sanitize(s.coverage),
                "age_seconds": s.age_seconds,
                "unscanned": None if s.unscanned is None else sanitize(s.unscanned),
            }
            for s in result.sources
        ],
        "rows": [
            {
                "row_id": sanitize(r.row.row_id),
                "class": r.classification.class_name,
                "waiting_kind": r.classification.waiting_kind,
                "rule": r.classification.rule,
                "evidence": sanitize(r.classification.evidence),
                "notes": [sanitize(n) for n in r.classification.notes],
                "policy": r.policy,
                "person_started": r.row.person_started,
                "safe_to_close": {
                    "terminal": r.safe.terminal,
                    "worktree": r.safe.worktree,
                    "reason": None
                    if r.safe.reason is None
                    else sanitize(r.safe.reason),
                },
            }
            for r in result.rows
        ],
        "worktrees": [
            {
                "path": sanitize(w.path),
                "status_read": w.status_read,
                "uncommitted": w.uncommitted,
                "unpushed": w.unpushed,
                "dev_tasks_unsaved": w.dev_tasks_unsaved,
                "frozen": w.frozen,
                "packages": [
                    {"id": sanitize(p.id), "location": p.location, "state": p.state}
                    for p in w.packages
                ],
                "shared_package_ids": [sanitize(i) for i in w.shared_package_ids],
                "removable": w.removable,
                "removable_reason": (
                    None if w.removable_reason is None else sanitize(w.removable_reason)
                ),
            }
            for w in result.worktrees
        ],
        "waiting": {
            "a": [sanitize(i) for i in result.waiting_a],
            "b": [sanitize(i) for i in result.waiting_b],
        },
        "summary": {
            "counts": {name: counts[name] for name in CLASSES},  # type: ignore[index]
            "bound_reached": summary["bound_reached"],
            "visible": summary["visible"],
            "historical": summary["historical"],
            "total": summary["total"],
            "total_is_lower_bound": summary["total_is_lower_bound"],
        },
        "report_path": report_path,  # the real path: json.dumps escapes it, and Read needs it as is
    }
