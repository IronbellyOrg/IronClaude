"""Tests for the pure renderer of ``superclaude sweep`` (DESIGN section 11, ``test_report.py`` row).

Covers FR-011, FR-016, NFR-005, NFR-008, NFR-015, SP-23, SP-24, the FR-020 header line,
FR-006 (rule 6 wording), SP-16, WC-13, SPEC section 11 remote coverage, the D9 note, the two
builder decisions (the ten dimensions are Sessions-table columns and never JSON keys;
dimension 9 prints ``frozen`` or ``unknown``, never ``not frozen``, OQ-11), and the two
DESIGN 7.5 cases added by reflect run 2 (the set-union session count and the three renderer
bans).

``SweepResult`` objects are built directly from ``models`` (a ``ClassifiedRow`` per row), or
through ``classify`` and ``classify_all`` where the case is about a classifier outcome. No
test here starts a process (the autouse guard in ``conftest.py`` enforces that). Fixed strings
are written out as literals taken from DESIGN, so a changed constant in ``report.py`` or
``classify.py`` fails here instead of passing silently.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from superclaude.cli.sweep import report
from superclaude.cli.sweep.classify import (
    RULES,
    classify,
    classify_all,
    policy_of,
    safe_to_close,
)
from superclaude.cli.sweep.models import (
    CLASSES,
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
    TranscriptTail,
    WorktreeState,
)

# --- Class names (models.CLASSES) and fixed strings, byte-exact from DESIGN 7.5 and 7.2 ----
WAITING = "waiting on a person"
STALLED = "stalled (proved)"
FENCED = "fenced"
WORKING = "working"
FINISHED = "finished"
IDLE = "idle"
PERSON_ACTIVE = "person session (active)"
UNKNOWN = "could not determine"

NO_RECORDS = "No matching records. This is not an all-clear."
BOUND_LINE = "[Show cap or time budget reached; row total is a lower bound]"
PAGE_LINE = "[Orca rows: 100 shown; total is a lower bound (paging not yet captured)]"
WORKTREES_BANNER = "[child worktrees not discovered: Orca unavailable; worktree count is a lower bound]"
# DESIGN 7.5, second form: Orca answered but the ``orca worktree ps`` source is unscanned.
# ``full_result`` carries that source row with the reason "orca call failed (exit 1)".
WORKTREES_PS_BANNER = (
    "[child worktrees not discovered: orca worktree ps unscanned "
    "(orca call failed (exit 1)); worktree count is a lower bound]"
)
SP24 = "Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred."
SP16 = "could not join Orca workers to transcripts (tab map empty or stale)"
WC13 = "WC-13 violation, review"
ORIGIN_NOT_PROVED = (
    "origin not proved: no tab-map entry; may be a worker of a Run outside the scope"
)
SCOPE_LOWER_BOUND = "(lower bound: remote hosts not scanned)"
UNSCANNED_CONTRACT = "unscanned: contract not readable"

# The headings of DESIGN 7.5 in order; the Sessions heading carries (shown/total).
HEADINGS = [
    "## Source coverage",
    "## Waiting on a person (a)",
    "## Waiting on a person (b)",
    "### Ready Tasks needing ownership review (creator not observable in Phase 1)",
    "## Could not determine",
    "## Retained problems",
    "## Sessions",
    "## Worktrees",
    "## Historical sessions",
    "## Shift Brief",
    "## What I could not determine",
]

SESSION_COLUMNS = [
    "ID",
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
    "Class",
    "Rule",
    "Evidence",
    "Safe to close (terminal / worktree)",
    "Notes",
    "Next inspection",
]

UTC = timezone.utc
HOUR = timedelta(hours=1)
MINUTE = timedelta(minutes=1)
HTML_PAYLOAD = '<button>b</button> <form> <input> <a href="http://x">l</a>'


def distinct(n: int) -> str:
    return f"Distinct affected sessions: {n} (set union, not a sum)"


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


@pytest.fixture
def ctx(fixed_now) -> SweepContext:
    assert fixed_now == datetime(2026, 11, 8, 12, 0, 0, tzinfo=UTC)
    return make_ctx(fixed_now)


def obs(dispatch: str = "D1", **kw) -> OrcaObservation:
    kw.setdefault("run", "R1")
    return OrcaObservation(dispatch=dispatch, **kw)


def srow(row_id: str = "orca:D1", **kw) -> SessionRow:
    base = dict(
        id=row_id.split(":", 1)[-1],
        person_started=None,
        orca=None,
        contract=None,
        transcript_path=None,
        transcript_readable=None,
        last_activity=None,
        gate_policy=None,
        row_id=row_id,
    )
    base.update(kw)
    return SessionRow(**base)


def crow(
    row_id: str,
    class_name: str,
    rule: str,
    *,
    kind: str | None = None,
    evidence: str = "evidence",
    notes: tuple[str, ...] = (),
    orca: OrcaObservation | None = None,
    contract: ContractRecord | None = None,
    person: bool | None = None,
    policy: str | None = None,
    last: datetime | None = None,
    **dims,
) -> ClassifiedRow:
    """A ``ClassifiedRow`` written out by hand (the renderer is a pure function of it)."""
    row = srow(
        row_id,
        person_started=person,
        orca=orca,
        contract=contract,
        last_activity=last,
        **dims,
    )
    return ClassifiedRow(
        row=row,
        classification=Classification(class_name, kind, rule, evidence, tuple(notes)),
        policy=policy,
        safe=SafeToClose(
            "could not determine",
            "could not determine",
            "terminal: not observed; worktree: not observed",
        ),
    )


def real(row: SessionRow, ctx: SweepContext) -> ClassifiedRow:
    """A ``ClassifiedRow`` produced by the real classifier, for the classifier-driven cases."""
    return ClassifiedRow(
        row=row,
        classification=classify(row, ctx),
        policy=policy_of(row),
        safe=safe_to_close(row, None),
    )


def wtree(path: str, **kw) -> WorktreeState:
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


def base_sources() -> tuple[SourceCoverage, ...]:
    return (
        SourceCoverage("orca worker-list R1", "read", 5, None),
        SourceCoverage("remote hosts", "unknown", None, None),
    )


def result_of(
    ctx: SweepContext,
    rows=(),
    *,
    worktrees=(),
    sources=None,
    orca_available: bool = True,
    orca_binary: str = "orca-ide",
    orca_version: str | None = None,
    truncated: bool = False,
    bound_reached: int = 0,
) -> SweepResult:
    rows = tuple(rows)
    counts = {name: 0 for name in CLASSES}
    for r in rows:
        counts[r.classification.class_name] += 1
    summary: dict[str, object] = {
        "counts": counts,
        "bound_reached": bound_reached,
        "visible": len(rows) - counts[IDLE],
        "historical": counts[IDLE],
        "total": len(rows),
        "total_is_lower_bound": True,
    }
    return SweepResult(
        rows=rows,
        worktrees=tuple(worktrees),
        waiting_a=tuple(
            r.row.row_id for r in rows if r.classification.waiting_kind == "a"
        ),
        waiting_b=tuple(
            r.row.row_id for r in rows if r.classification.waiting_kind == "b"
        ),
        summary=summary,
        context=ctx,
        sources=base_sources() if sources is None else tuple(sources),
        orca_available=orca_available,
        orca_binary=orca_binary,
        orca_version=orca_version,
        truncated=truncated,
        collected_start=ctx.now - MINUTE,
        collected_end=ctx.now,
    )


def full_result(ctx: SweepContext) -> SweepResult:
    """Every section populated, with rows and paths under ``.dev/tasks/`` and HTML payloads."""
    n = ctx.now
    contract_path = Path("/wt/.dev/tasks/to-do/pkg-a/return-contract.yaml")
    rows = [
        crow(
            "orca:A1",
            WAITING,
            "blocked_contract",
            kind="a",
            evidence=f"blocked contract {contract_path} {HTML_PAYLOAD}",
            orca=obs("A1", worktree_path="/wt/.dev/tasks/odd"),
            contract=ContractRecord(
                path=contract_path,
                worker_status="blocked",
                blocked_question=f"Which branch? {HTML_PAYLOAD}",
                mtime=n - 5 * HOUR,
            ),
        ),
        crow(
            "orca:A2",
            WAITING,
            "waiting_signal",
            kind="a",
            evidence="agent_wait is non-null (worker-show agentWait)",
            orca=obs("A2", agent_wait={"w": 1}, agent_wait_since=n - HOUR),
        ),
        crow(
            "orca:B1",
            WAITING,
            "waiting_signal",
            kind="b",
            evidence="frozen plan: contract worker_status failed with STOP code E-HALT-QA",
            orca=obs("B1", status="in_progress"),
            policy="frozen",
        ),
        crow(
            "orca:B2",
            WAITING,
            "waiting_signal",
            kind="b",
            evidence="ready Task: creator not observable; needs ownership review",
            orca=obs("B2", status="ready"),
        ),
        crow(
            "orca:U1",
            UNKNOWN,
            "fallback",
            evidence="no rule 1 to 8 matched",
            notes=(SP16,),
        ),
        crow(
            "orca:U2",
            UNKNOWN,
            "fallback",
            evidence=f"no rule 1 to 8 matched {HTML_PAYLOAD}",
            notes=(WC13,),
            orca=obs("U2", parent="D0"),
        ),
        crow("orca:W1", WORKING, "working", evidence="liveness_verdict live"),
        crow(
            "orca:F1",
            FINISHED,
            "finished",
            evidence=(
                f"Orca outcome succeeded; parsed contract {contract_path} "
                "worker_status succeeded"
            ),
        ),
        crow("orca:S1", STALLED, "orca_exit_proof", evidence="exited, no worker_done"),
        crow("orca:X1", FENCED, "fenced", evidence="fenced_evidence present"),
        crow(
            "transcript:P1",
            PERSON_ACTIVE,
            "person_active",
            evidence="active inside the window",
            person=True,
            notes=(ORIGIN_NOT_PROVED,),
            last=n - 5 * MINUTE,
        ),
        crow(
            "transcript:H1",
            IDLE,
            "idle",
            evidence="no activity inside the window",
            person=True,
            last=n - 30 * HOUR,
        ),
        crow(
            "[x] orca:C1",
            WORKING,
            "working",
            notes=(WC13,),
            orca=obs("C1", parent="D0"),
        ),
    ]
    worktrees = [
        wtree(
            "/wt/one",
            uncommitted=True,
            dev_tasks_unsaved=True,
            changed_paths=(".dev/tasks/to-do/pkg-a/progress.md",),
            packages=(
                PackageRecord(
                    "pkg-b", "to-do", None, True, True, "interrupted-archive"
                ),
            ),
            shared_package_ids=("pkg-c",),
            frozen=True,
            removable="no",
            removable_reason="unsaved path under .dev/tasks/",
        ),
        wtree(
            "/wt/.dev/tasks/odd",
            packages=(PackageRecord("pkg-a", "both", None, False, True, "conflict"),),
            shared_package_ids=("pkg-c",),
            removable="could not determine",
            removable_reason="worktree not observed",
        ),
    ]
    sources = [
        SourceCoverage("orca worker-list R1", "read", 5, None),
        SourceCoverage(
            "orca worktree ps", "unscanned", None, "orca call failed (exit 1)"
        ),
        SourceCoverage("ccsession orca-tabs", "read", None, None),
        SourceCoverage("remote hosts", "unknown", None, None),
    ]
    return result_of(
        ctx,
        rows,
        worktrees=worktrees,
        sources=sources,
        orca_version="1.4.246",
        truncated=True,
        bound_reached=1,
    )


def empty_result(ctx: SweepContext) -> SweepResult:
    return result_of(ctx, sources=())


def sweep_input(
    now: datetime,
    *,
    orca_rows=(),
    contracts=(),
    sources=None,
    truncated: bool = False,
) -> SweepInput:
    return SweepInput(
        orca_rows=tuple(orca_rows),
        contracts=tuple(contracts),
        transcripts=(),
        tab_map=(),
        worktrees=(),
        sources=(
            (
                SourceCoverage("orca worker-list R1", "read", None, None),
                SourceCoverage("ccsession orca-tabs", "read", None, None),
            )
            if sources is None
            else tuple(sources)
        ),
        orca_available=True,
        orca_binary="orca-ide",
        orca_version=None,
        truncated=truncated,
        collected_start=now,
        collected_end=now,
    )


def settled_input(now: datetime, *, sources=None) -> SweepInput:
    """One settled Orca row with its contract (finished) and one guard-refused row."""
    settled = obs("D1", outcome="succeeded", status="completed", worktree_path="/wt/a")
    guard = obs(
        "D2", body_text="guard refused: no admitted contract\naccepted by no one"
    )
    return sweep_input(
        now,
        orca_rows=(settled, guard),
        contracts=(
            ContractRecord(
                path=Path("/wt/a/return-contract.yaml"), worker_status="succeeded"
            ),
        ),
        sources=sources,
    )


# --- Text helpers -------------------------------------------------------------------------

_PIPE = re.compile(r"(?<!\\)\|")


def block(text: str, heading: str) -> str:
    """Lines from the line starting with ``heading`` up to the next ``## `` heading or footer."""
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(heading))
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## ") or lines[i] == "Inspection only.":
            end = i
            break
    return "\n".join(lines[start:end])


def header_block(text: str) -> str:
    return text.split("## Source coverage", 1)[0]


def split_cells(line: str) -> list[str]:
    return [c.strip() for c in _PIPE.split(line)[1:-1]]


def tables(text: str) -> list[tuple[list[str], list[dict[str, str]]]]:
    """Each Markdown table in ``text`` as (headers, rows as dicts)."""
    groups: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.startswith("|"):
            current.append(line)
        elif current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)
    out = []
    for group in groups:
        headers = split_cells(group[0])
        body = [dict(zip(headers, split_cells(line))) for line in group[2:]]
        out.append((headers, body))
    return out


def headings_of(text: str) -> list[str]:
    heads = [line for line in text.splitlines() if line.startswith("#")]
    return [re.sub(r" \(\d+/\d+\)$", "", h) for h in heads]


def sessions_table(text: str) -> list[dict[str, str]]:
    return tables(block(text, "## Sessions"))[0][1]


def json_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {k for v in value.values() for k in json_keys(v)}
    if isinstance(value, list):
        return {k for v in value for k in json_keys(v)}
    return set()


# ===========================================================================================
# Layout: heading order (FR-011), SECTIONS, last line
# ===========================================================================================


@pytest.mark.parametrize("build", [full_result, empty_result], ids=["full", "empty"])
def test_heading_order_equals_section_7_5(ctx, build):
    text = report.render(build(ctx), ctx)
    assert headings_of(text) == HEADINGS
    assert re.search(r"(?m)^## Sessions \(\d+/\d+\)$", text)


def test_sections_tuple_has_twelve_functions_and_render_joins_them(ctx):
    result = full_result(ctx)
    assert len(report.SECTIONS) == 12
    assert report.render(result, ctx) == (
        "\n\n".join(section(result, ctx) for section in report.SECTIONS) + "\n"
    )


@pytest.mark.parametrize("build", [full_result, empty_result], ids=["full", "empty"])
def test_last_line_is_report_complete(ctx, build):
    text = report.render(build(ctx), ctx)
    assert text.endswith("Report complete\n")
    assert text.splitlines()[-1] == "Report complete"
    assert "Inspection only." in text.splitlines()


def test_header_first_line_and_scope_line_are_exact(ctx):
    lines = report.render(result_of(ctx, sources=base_sources()), ctx).splitlines()
    assert lines[0] == (
        "READ ONLY . observed 2026-11-08T12:00:00Z . collected 2026-11-08T11:59:00Z "
        "to 2026-11-08T12:00:00Z (not an atomic runtime snapshot)"
    )
    assert lines[1] == (
        "Scope: Runs R1 . worktrees 0 . sessions 0/0 "
        "(lower bound: remote hosts not scanned) . window 6h"
    )


def test_header_has_the_seven_exact_lines_of_design_7_5(ctx):
    # TST-F2: the four lines after the scope line were unpinned. The resolved binary name is
    # printed (never a bare ``orca``, NFR-003), the messages coverage is ``partial``, each
    # source carries its age, and the version line is the UNVERIFIED form for no version file.
    text = report.render(result_of(ctx, sources=base_sources()), ctx)

    assert header_block(text).rstrip("\n").splitlines() == [
        "READ ONLY . observed 2026-11-08T12:00:00Z . collected 2026-11-08T11:59:00Z "
        "to 2026-11-08T12:00:00Z (not an atomic runtime snapshot)",
        "Scope: Runs R1 . worktrees 0 . sessions 0/0 "
        "(lower bound: remote hosts not scanned) . window 6h",
        "Orca binary: orca-ide",
        "Sources: orca worker-list R1 read (age 5s) . remote hosts unknown",
        "Messages coverage: partial",
        "Orca lock risk: UNVERIFIED (checked for Orca 1.4.245; observed unknown)",
        "Untracked paths: listed per file (--untracked-files=all); not observed in a "
        "worktree whose status was unread",
    ]


def test_header_sources_line_says_none_when_there_are_no_sources(ctx):
    lines = header_block(report.render(empty_result(ctx), ctx)).splitlines()

    assert "Sources: none" in lines
    assert "Orca binary: orca-ide" in lines


@pytest.mark.parametrize(
    ("build", "banner_shown", "ps_banner"),
    [
        # Orca answered and ``orca worktree ps`` is an unscanned source: since the FIN-F5 fix
        # the header prints the second DESIGN 7.5 form (WORKTREES_PS_BANNER), not the
        # "Orca unavailable" text, so the old banner is not shown here.
        (full_result, False, WORKTREES_PS_BANNER),
        (empty_result, False, None),
        (lambda c: result_of(c, orca_available=False), True, None),  # Orca unavailable
    ],
    ids=["ps-unscanned", "complete", "orca-unavailable"],
)
def test_discovery_incomplete_banner_is_in_the_header_only_when_discovery_is_incomplete(
    ctx, build, banner_shown, ps_banner
):
    text = report.render(build(ctx), ctx)
    header_lines = header_block(text).splitlines()

    assert (WORKTREES_BANNER in header_lines) is banner_shown
    assert text.count(WORKTREES_BANNER) == int(banner_shown)
    assert (WORKTREES_PS_BANNER in header_lines) is (ps_banner is not None)
    assert text.count(WORKTREES_PS_BANNER) == int(ps_banner is not None)
    # Once, on one line, in the header block only: no other banner line appears anywhere.
    assert text.count("[child worktrees not discovered") == int(
        banner_shown or ps_banner is not None
    )


def ps_unscanned_result(
    ctx: SweepContext, reason: str | None, coverage: str = "unscanned", **kw
) -> SweepResult:
    sources = (
        SourceCoverage("orca worker-list R1", "read", 5, None),
        SourceCoverage("orca worktree ps", coverage, None, reason),
    )
    return result_of(ctx, sources=sources, **kw)


def test_banner_names_the_worktree_list_truncated_reason_in_the_ps_unscanned_form(ctx):
    # Orca answered; only the ``orca worktree ps`` list was cut short (the probe records that
    # source as coverage ``read`` with the reason "worktree list truncated").
    text = report.render(
        ps_unscanned_result(ctx, "worktree list truncated", coverage="read"), ctx
    )

    expected = (
        "[child worktrees not discovered: orca worktree ps unscanned "
        "(worktree list truncated); worktree count is a lower bound]"
    )
    assert expected in header_block(text).splitlines()
    assert text.count("[child worktrees not discovered") == 1
    assert WORKTREES_BANNER not in text  # Orca did answer: never "Orca unavailable"


def test_banner_reason_is_the_sanitized_unscanned_text(ctx):
    # ``sanitize`` escapes ``|``, ``<``, ``>``, ``[`` and ``]`` and folds a newline to a space;
    # the banner must carry that sanitized text, on one line.
    reason = "cut | see <log>\nnext [3]"
    text = report.render(ps_unscanned_result(ctx, reason), ctx)

    expected = (
        "[child worktrees not discovered: orca worktree ps unscanned "
        "(cut \\| see &lt;log&gt; next \\[3\\]); worktree count is a lower bound]"
    )
    assert report.sanitize(reason) == "cut \\| see &lt;log&gt; next \\[3\\]"
    assert expected in header_block(text).splitlines()
    assert text.count("[child worktrees not discovered") == 1
    assert reason not in text


def test_orca_unavailable_keeps_the_old_banner_even_when_the_ps_row_has_a_reason(ctx):
    # Orca really was unavailable: the first DESIGN 7.5 form, unchanged, whatever the
    # ``orca worktree ps`` row says.
    result = ps_unscanned_result(ctx, "orca unavailable", orca_available=False)
    text = report.render(result, ctx)

    assert WORKTREES_BANNER in header_block(text).splitlines()
    assert text.count("[child worktrees not discovered") == 1
    assert (
        "worktree ps unscanned (orca unavailable)" not in text
    )  # no second-form banner


@pytest.mark.parametrize(
    "sources",
    [
        (SourceCoverage("orca worktree ps", "read", 3, None),),
        (SourceCoverage("orca task-list R1", "unscanned", None, "orca call failed"),),
    ],
    ids=["ps-read", "other-source-unscanned"],
)
def test_no_banner_when_only_a_source_other_than_ps_is_unscanned_or_ps_was_read(
    ctx, sources
):
    text = report.render(result_of(ctx, sources=sources), ctx)

    assert "[child worktrees not discovered" not in text


# ===========================================================================================
# Waiting (a) sort and Waiting (b) content (FR-011)
# ===========================================================================================


def test_waiting_a_sorts_oldest_first_then_unknown_age_with_ties_by_id(ctx):
    n = ctx.now
    d7 = crow(
        "orca:D7",
        WAITING,
        "waiting_signal",
        kind="a",
        orca=obs("D7", agent_wait={"w": 1}, agent_wait_since=n - 3 * HOUR),
    )
    d2 = crow(
        "orca:D2",
        WAITING,
        "waiting_signal",
        kind="a",
        orca=obs("D2", agent_wait={"w": 1}, agent_wait_since=n - 2 * HOUR),
    )
    # The earlier of the contract time (2h) and the agentWait time (1m) is the age: 2h.
    d3 = crow(
        "orca:D3",
        WAITING,
        "blocked_contract",
        kind="a",
        orca=obs("D3", agent_wait={"w": 1}, agent_wait_since=n - MINUTE),
        contract=ContractRecord(
            path=Path("/c3.yaml"),
            worker_status="blocked",
            blocked_question="Q-D3",
            mtime=n - 2 * HOUR,
        ),
    )
    d9 = crow(
        "orca:D9",
        WAITING,
        "blocked_contract",
        kind="a",
        orca=obs("D9", outcome="failed"),
        contract=ContractRecord(
            path=Path("/c9.yaml"),
            worker_status="blocked",
            blocked_question="Q-D9",
            mtime=n - 10 * MINUTE,
        ),
    )
    d1 = crow(
        "orca:D1",
        WAITING,
        "waiting_signal",
        kind="a",
        orca=obs("D1", agent_wait={"w": 1}),  # no agentWait time: unknown age
    )
    result = result_of(ctx, [d9, d3, d1, d7, d2])  # shuffled on purpose
    section = block(report.render(result, ctx), "## Waiting on a person (a)")
    rows = tables(section)[0][1]
    assert [(r["ID"], r["Age"]) for r in rows] == [
        ("orca:D7", "3h 0m"),
        ("orca:D2", "2h 0m"),
        ("orca:D3", "2h 0m"),
        ("orca:D9", "10m"),
        ("orca:D1", "unknown"),
    ]
    assert {r["ID"]: r["Question"] for r in rows}["orca:D9"] == "Q-D9"
    assert distinct(5) in section.splitlines()
    assert "Seen is not resolved" in section
    assert "Answered: could not determine" in section


def test_waiting_b_lists_frozen_then_ready_tasks_and_never_prints_question_text(ctx):
    secret = "SECRET-QUESTION-TEXT"
    frozen = real(
        srow(
            "orca:F1",
            orca=obs("F1"),
            contract=ContractRecord(
                path=Path("/c1.yaml"),
                worker_status="failed",
                reason="E-HALT-QA stop",
                blocked_question=secret,
            ),
        ),
        ctx,
    )
    ready = real(srow("orca:T1", orca=obs("T1", status="ready")), ctx)
    asking = real(
        srow(
            "orca:A1",
            orca=obs("A1", outcome="failed"),
            contract=ContractRecord(
                path=Path("/c2.yaml"),
                worker_status="blocked",
                blocked_question="VISIBLE-QUESTION",
                mtime=ctx.now - HOUR,
            ),
        ),
        ctx,
    )
    assert (frozen.classification.class_name, frozen.classification.waiting_kind) == (
        WAITING,
        "b",
    )
    assert ready.classification.waiting_kind == "b"
    assert asking.classification.waiting_kind == "a"
    text = report.render(result_of(ctx, [asking, ready, frozen]), ctx)
    b = block(text, "## Waiting on a person (b)")
    assert secret not in b
    assert secret not in text
    assert all("Question" not in headers for headers, _ in tables(b))
    assert "VISIBLE-QUESTION" in block(text, "## Waiting on a person (a)")  # (a) has it
    order = [
        b.index("orca:F1"),
        b.index("### Ready Tasks needing ownership review"),
        b.index("orca:T1"),
        b.index("Ready Tasks: 1"),
    ]
    assert order == sorted(order)


# ===========================================================================================
# Sanitize and cell (FR-016, SP-23)
# ===========================================================================================

INJECTIONS = {
    "pipe": ("a|b", "a\\|b"),
    "ansi": ("Q\x1b[31mredQ\x1b[0m", "QredQ"),
    "bidi": ("Qa" + chr(0x202E) + "bQ", "QabQ"),  # U+202E, right-to-left override
    "script": ("<script>alert(1)</script>", "&lt;script&gt;alert(1)&lt;/script&gt;"),
    "link": ("[click](http://evil.example)", "\\[click\\](http://evil.example)"),
}


def injected_result(ctx: SweepContext, payload: str) -> SweepResult:
    n = ctx.now
    rows = [
        crow(
            "orca:A1",
            WAITING,
            "blocked_contract",
            kind="a",
            evidence=payload,
            notes=(payload,),
            orca=obs("A1", worktree_path=payload),
            contract=ContractRecord(
                path=Path("/c.yaml"),
                worker_status="blocked",
                blocked_question=payload,
                mtime=n - HOUR,
            ),
        ),
        crow("orca:U1", UNKNOWN, "fallback", evidence=payload, notes=(payload,)),
        crow("orca:B1", WAITING, "waiting_signal", kind="b", evidence=payload),
    ]
    worktrees = [
        wtree(
            payload,
            packages=(PackageRecord(payload, "both", None, False, True, "conflict"),),
            removable_reason=payload,
        )
    ]
    sources = [SourceCoverage(payload, payload, None, payload)]
    return result_of(
        ctx,
        rows,
        worktrees=worktrees,
        sources=sources,
        orca_binary=payload,
        orca_version=payload,
    )


@pytest.mark.parametrize("name", list(INJECTIONS))
def test_injection_keeps_the_column_count_and_leaves_no_active_tag_or_link(
    fixed_now, name
):
    payload, expected = INJECTIONS[name]
    ctx = make_ctx(fixed_now, runs=(payload,))
    text = report.render(injected_result(ctx, payload), ctx)
    assert (
        expected in text
    )  # the payload is neutralised, not dropped (except ESC and bidi)
    assert "\x1b" not in text
    assert not any(
        unicodedata.category(ch) in ("Cc", "Cf") for ch in text if ch != "\n"
    )
    assert "<" not in text  # no active tag
    assert re.search(r"(?<!\\)\]\(", text) is None  # no live Markdown link
    assert headings_of(text) == HEADINGS  # a payload cannot add or move a heading
    # Every line of a table has as many unescaped pipes as the table's header line.
    width = None
    checked = 0
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            count = len(_PIPE.findall(line))
            width = count if width is None else width
            assert count == width, line
            checked += 1
        else:
            width = None
    assert checked >= 10  # not vacuous: the fixture has several tables


@pytest.mark.parametrize("length", [199, 200])
def test_cell_keeps_text_up_to_200_characters(length):
    assert report.cell("x" * length) == "x" * length


@pytest.mark.parametrize("length", [201, 300])
def test_cell_cuts_longer_text_to_200_characters_ending_in_dots(length):
    out = report.cell("x" * length)
    assert len(out) == 200
    assert out == "x" * 197 + "..."


def test_300_character_cell_prints_200_characters_while_the_json_value_is_whole(ctx):
    long = "y" * 300
    result = result_of(
        ctx,
        [crow("orca:U1", UNKNOWN, "fallback", evidence=long)],
        sources=base_sources(),
    )
    text = report.render(result, ctx)
    assert {r["Evidence"] for r in sessions_table(text)} == {"y" * 197 + "..."}
    assert all(len(r["Evidence"]) == 200 for r in sessions_table(text))
    assert report.to_json(result, ctx, "/r.md")["rows"][0]["evidence"] == long


# ===========================================================================================
# Determinism (NFR-005)
# ===========================================================================================


def test_render_twice_gives_equal_bytes_and_equal_json_apart_from_report_path(ctx):
    result = full_result(ctx)
    first, second = report.render(result, ctx), report.render(result, ctx)
    assert first.encode("utf-8") == second.encode("utf-8")
    one = report.to_json(result, ctx, "/reports/one.md")
    two = report.to_json(result, ctx, "/reports/two.md")
    assert one["report_path"] != two["report_path"]
    two["report_path"] = one["report_path"]
    assert json.dumps(one, sort_keys=True) == json.dumps(two, sort_keys=True)
    # The time printed comes from ctx.now alone.
    later = make_ctx(ctx.now + HOUR)
    assert "observed 2026-11-08T13:00:00Z" in report.render(result, later)


@pytest.mark.parametrize("path", ["/tmp/project[1]/a|b.md", "/tmp/<x>/a&b\\c.md"])
def test_json_report_path_is_the_real_path_not_the_markdown_escaped_one(ctx, path):
    # The skill Reads report_path as given, so it must not carry Markdown escapes.
    result = full_result(ctx)
    payload = json.loads(json.dumps(report.to_json(result, ctx, path)))
    assert payload["report_path"] == path


# ===========================================================================================
# Source loss (NFR-008), version line (NFR-015), header lines (FR-020, SPEC 321, 454)
# ===========================================================================================


def test_source_loss_gives_could_not_determine_with_the_unscanned_reason(ctx):
    control = classify_all(settled_input(ctx.now), ctx)
    assert {c.row.row_id: c.classification.class_name for c in control.rows} == {
        "orca:D1": FINISHED,
        "orca:D2": FINISHED,
    }
    lost = settled_input(
        ctx.now,
        sources=(
            SourceCoverage("orca worker-list R1", "read", None, None),
            SourceCoverage("ccsession orca-tabs", "read", None, None),
            SourceCoverage("contract D1", "unscanned", None, "contract unreadable"),
        ),
    )
    result = classify_all(lost, ctx)
    text = report.render(result, ctx)
    cls = {c.row.row_id: c.classification for c in result.rows}["orca:D1"]
    assert (cls.class_name, cls.rule) == (UNKNOWN, "fallback")
    assert UNSCANNED_CONTRACT in cls.notes

    cant = {r["ID"]: r for r in tables(block(text, "## Could not determine"))[0][1]}
    assert UNSCANNED_CONTRACT in cant["orca:D1"]["Notes"]
    session = {r["ID"]: r for r in sessions_table(text)}["orca:D1"]
    assert session["Class"] == UNKNOWN
    assert session["Next inspection"] == report.NEXT_INSPECTION["fallback"]
    d1_lines = [ln.lower() for ln in text.splitlines() if ln.startswith("| orca:D1 ")]
    assert len(d1_lines) == 2  # its Could not determine row and its Sessions row
    for low in d1_lines:
        assert "| finished |" not in low  # the Class cell is never finished
        assert "failed" not in low
    assert "- contract D1: unscanned: contract unreadable" in text.splitlines()
    assert report.to_json(result, ctx, "/r.md")["rows"][0]["class"] == UNKNOWN
    assert "not frozen" not in text.lower()


@pytest.mark.parametrize(
    ("observed", "line"),
    [
        (
            "1.4.245-aidev02.780594c521aa",
            "Orca lock risk: unlikely (checked for Orca 1.4.245)",
        ),
        (
            "1.4.246",
            "Orca lock risk: UNVERIFIED (checked for Orca 1.4.245; observed 1.4.246)",
        ),
        (
            None,  # a missing, unreadable or unparseable version file
            "Orca lock risk: UNVERIFIED (checked for Orca 1.4.245; observed unknown)",
        ),
    ],
    ids=["checked-build", "other-version", "missing-file"],
)
def test_orca_lock_risk_line_by_observed_version(ctx, observed, line):
    assert report.CHECKED_ORCA_VERSION == "1.4.245"
    text = report.render(result_of(ctx, orca_version=observed), ctx)
    assert line in header_block(text).splitlines()
    assert sum(1 for ln in text.splitlines() if ln.startswith("Orca lock risk:")) == 1


def test_bound_reached_line_is_in_the_header_only_when_the_count_is_at_least_one(ctx):
    reached = report.render(result_of(ctx, bound_reached=2), ctx)
    assert BOUND_LINE in header_block(reached).splitlines()
    assert "Show cap or time budget reached" in block(reached, "## Retained problems")
    none = report.render(result_of(ctx, bound_reached=0), ctx)
    assert BOUND_LINE not in none
    assert "Show cap or time budget reached" not in none


def test_full_worker_list_page_prints_the_lower_bound_line_and_json_true(ctx):
    result = classify_all(sweep_input(ctx.now, truncated=True), ctx)
    text = report.render(result, ctx)
    assert PAGE_LINE in header_block(text).splitlines()
    assert (
        report.to_json(result, ctx, "/r.md")["summary"]["total_is_lower_bound"] is True
    )
    # total_is_lower_bound is always True in Phase 1: remote hosts are never scanned.
    plain = classify_all(sweep_input(ctx.now), ctx)
    assert PAGE_LINE not in report.render(plain, ctx)
    assert (
        report.to_json(plain, ctx, "/r.md")["summary"]["total_is_lower_bound"] is True
    )


def test_remote_coverage_row_and_scope_line_never_say_there_are_no_sessions(ctx):
    text = report.render(result_of(ctx, sources=base_sources()), ctx)
    headers, rows = tables(block(text, "## Source coverage"))[0]
    remote = [r for r in rows if r[headers[0]] == "remote hosts"]
    assert [r["Coverage"] for r in remote] == ["unknown"]
    scope = next(ln for ln in text.splitlines() if ln.startswith("Scope:"))
    assert SCOPE_LOWER_BOUND in scope
    assert "no sessions" not in text.lower()


# ===========================================================================================
# Fixed strings: SP-24, empty section, SP-16, WC-13, D9 note, rule 6 wording
# ===========================================================================================


@pytest.mark.parametrize("build", [full_result, empty_result], ids=["full", "empty"])
def test_sp24_footnote_is_in_the_sessions_section(ctx, build):
    text = report.render(build(ctx), ctx)
    assert SP24 in block(text, "## Sessions").splitlines()
    assert text.count(SP24) == 1


def test_empty_sections_print_the_exact_no_records_string(ctx):
    text = report.render(empty_result(ctx), ctx)
    for heading in (
        "## Source coverage",
        "## Waiting on a person (a)",
        "## Could not determine",
        "## Retained problems",
        "## Sessions",
        "## Worktrees",
        "## Historical sessions",
    ):
        assert NO_RECORDS in block(text, heading).splitlines(), heading
    # Waiting (b) is empty twice: the frozen-plan list and the Ready Tasks list.
    assert block(text, "## Waiting on a person (b)").splitlines().count(NO_RECORDS) == 2
    for heading in ("## Shift Brief", "## What I could not determine"):
        assert NO_RECORDS not in block(text, heading)
    assert NO_RECORDS not in header_block(text)
    # A populated report prints it nowhere.
    assert NO_RECORDS not in report.render(full_result(ctx), ctx)


RULE_CLASS = {
    "blocked_contract": (WAITING, "a"),
    "orca_exit_proof": (STALLED, None),
    "fenced": (FENCED, None),
    "waiting_signal": (WAITING, "b"),
    "working": (WORKING, None),
    "finished": (FINISHED, None),
    "idle": (IDLE, None),
    "person_active": (PERSON_ACTIVE, None),
    "fallback": (UNKNOWN, None),
}
BANNED_WORD = re.compile(r"\b(stop|retry|release|merge|remov\w*)\b", re.IGNORECASE)


def test_next_inspection_map_has_an_entry_per_rule_and_only_names_a_read(ctx):
    names = {rule.name for rule in RULES}
    assert set(RULE_CLASS) == names  # a new rule needs a row here
    assert set(report.NEXT_INSPECTION) == names
    for name, value in report.NEXT_INSPECTION.items():
        assert value.strip(), name
        assert BANNED_WORD.search(value) is None, (name, value)


def test_every_sessions_row_has_a_next_inspection_cell_from_the_map(ctx):
    rows = [
        crow(f"orca:{name}", cls, name, kind=kind)
        for name, (cls, kind) in RULE_CLASS.items()
    ]
    rows.append(crow("orca:ZZ", UNKNOWN, "no_such_rule"))  # a rule with no map entry
    text = report.render(result_of(ctx, rows), ctx)
    cells = {r["ID"]: r["Next inspection"] for r in sessions_table(text)}
    assert set(cells) == {r.row.row_id for r in rows if r.classification.rule != "idle"}
    for name in RULE_CLASS:
        if name != "idle":  # idle rows are Historical sessions, not Sessions rows
            assert cells[f"orca:{name}"] == report.NEXT_INSPECTION[name]
    assert cells["orca:ZZ"].strip()
    assert all(v.strip() and BANNED_WORD.search(v) is None for v in cells.values())


def test_next_inspection_waiting_signal_and_fallback_fit_every_outcome():
    # FIN-F3: one rule name matches rows with different evidence, so the map entry names
    # what the row's own Evidence cell names and never a list that can be empty.
    waiting = report.NEXT_INSPECTION["waiting_signal"]
    for named in ("agent-wait entry", "contract", "Task in Orca task-list"):
        assert named in waiting
    fallback = report.NEXT_INSPECTION["fallback"]
    assert "Evidence and Notes cells" in fallback
    assert "(if none, the session's last transcript lines)" in fallback


def test_sessions_safe_to_close_cell_carries_its_reason(ctx):
    # FIN-F2: the report prints the reason behind each Safe to close value, not only the value.
    hand = crow("orca:S1", UNKNOWN, "fallback")
    released = real(
        srow(
            "orca:S2",
            orca=obs(
                "S2",
                liveness_verdict="exited",
                status="completed",
                outcome="succeeded",
                terminal_state="released",
                next_action="none",
            ),
        ),
        ctx,
    )

    text = report.render(result_of(ctx, [hand, released]), ctx)

    column = "Safe to close (terminal / worktree)"
    cells = {r["ID"]: r[column] for r in sessions_table(text)}
    assert cells["orca:S1"] == (
        "could not determine / could not determine "
        "(terminal: not observed; worktree: not observed)"
    )
    assert cells["orca:S2"] == (
        "no / could not determine (terminal: not releasable "
        "(terminal_state=released, next_action=none); worktree: worktree not observed)"
    )
    assert block(text, "## Sessions").splitlines().count(report.SAFE_TO_CLOSE_LINE) == 1
    assert "never prints yes in Phase 1" in report.SAFE_TO_CLOSE_LINE


def test_orca_dropping_mid_run_is_not_reported_as_nothing_read(ctx):
    # FIN-F6: Orca sources read before the drop are real, so the line names only the
    # sources marked unscanned.
    text = report.render(result_of(ctx, orca_available=False), ctx)

    lines = block(text, "## What I could not determine").splitlines()

    assert (
        "- Orca became unavailable; the Orca sources marked unscanned above were not read"
        in lines
    )
    assert not any("Orca sources were not read" in line for line in lines)


def test_sp16_literal_is_printed_under_could_not_determine(ctx):
    with_note = result_of(ctx, [crow("orca:U1", UNKNOWN, "fallback", notes=(SP16,))])
    section = block(report.render(with_note, ctx), "## Could not determine")
    assert SP16 in section.splitlines()  # the standalone line
    assert SP16 in tables(section)[0][1][0]["Notes"]  # and the row's note
    without = result_of(ctx, [crow("orca:U1", UNKNOWN, "fallback")])
    assert SP16 not in report.render(without, ctx)


def test_wc13_row_is_listed_under_retained_problems(ctx):
    flagged = crow(
        "orca:D9", WORKING, "working", notes=(WC13,), orca=obs("D9", parent="D0")
    )
    plain = crow("orca:D8", WORKING, "working")
    text = report.render(result_of(ctx, [plain, flagged]), ctx)
    retained = block(text, "## Retained problems").splitlines()
    assert "- orca:D9: WC-13 violation, review" in retained
    assert not any("orca:D8" in line for line in retained)
    assert NO_RECORDS not in retained


def test_d9_origin_not_proved_note_is_in_the_row_and_in_the_json_notes(ctx):
    row = crow(
        "transcript:P1",
        PERSON_ACTIVE,
        "person_active",
        person=True,
        notes=(ORIGIN_NOT_PROVED,),
        last=ctx.now - MINUTE,
    )
    result = result_of(ctx, [row])
    printed = sessions_table(report.render(result, ctx))[0]
    assert ORIGIN_NOT_PROVED in printed["Notes"]
    entry = report.to_json(result, ctx, "/r.md")["rows"][0]
    assert entry["person_started"] is True
    assert ORIGIN_NOT_PROVED in entry["notes"]


def test_rule6_finished_rows_never_say_admitted_or_accepted(ctx):
    result = classify_all(settled_input(ctx.now), ctx)
    classes = {c.row.row_id: c.classification.class_name for c in result.rows}
    assert classes == {"orca:D1": FINISHED, "orca:D2": FINISHED}
    # The guard-refused body quotes both words; the report must not repeat them.
    text = report.render(result, ctx)
    dumped = json.dumps(report.to_json(result, ctx, "/r.md"), ensure_ascii=False)
    for word in ("admitted", "accepted"):
        assert word not in text.lower()
        assert word not in dumped.lower()


# ===========================================================================================
# Builder decisions: ten dimensions as columns (OQ-11), dimension 9
# ===========================================================================================

DIMENSION_KEYS = {
    "lifecycle",
    "phase",
    "health",
    "approval",
    "freshness",
    "freshness_age_s",
    "result",
    "admission",
    "evidence_packet",
    "tests_review",
}
ROW_KEYS = {
    "row_id",
    "class",
    "waiting_kind",
    "rule",
    "evidence",
    "notes",
    "policy",
    "person_started",
    "safe_to_close",
}


def dimension_result(ctx: SweepContext) -> SweepResult:
    return result_of(
        ctx,
        [
            crow(
                "orca:P1",
                WORKING,
                "working",
                policy="frozen",
                lifecycle="running",
                phase="build",
                health="failed result",
                approval="granted",
                freshness="fresh",
                freshness_age_s=30,
                result="succeeded",
                admission="unknown",
                evidence_packet="present",
                tests_review=None,
            ),
            crow("orca:P2", WORKING, "working", policy=None, tests_review="passed"),
        ],
    )


def test_ten_dimensions_are_sessions_columns_and_not_json_keys(ctx):
    result = dimension_result(ctx)
    text = report.render(result, ctx)
    headers, rows = tables(block(text, "## Sessions"))[0]
    assert headers == SESSION_COLUMNS
    first = {r["ID"]: r for r in rows}["orca:P1"]
    assert (first["Lifecycle"], first["Phase"], first["Health"]) == (
        "running",
        "build",
        "failed result",
    )
    assert (first["Approval"], first["Freshness"], first["Result"]) == (
        "granted",
        "fresh (30s)",
        "succeeded",
    )
    assert (first["Admission"], first["Evidence packet"]) == ("unknown", "present")
    assert first["Tests/review"] == "unavailable"  # None prints unavailable
    payload = report.to_json(result, ctx, "/r.md")
    assert json_keys(payload).isdisjoint(DIMENSION_KEYS)
    assert all(set(r) == ROW_KEYS for r in payload["rows"])


def dimension_cells(text: str) -> dict[str, tuple[str, str, str, str]]:
    """``ID -> (Lifecycle, Health, Result, Freshness)`` as printed in the Sessions table."""
    return {
        r["ID"]: (r["Lifecycle"], r["Health"], r["Result"], r["Freshness"])
        for r in sessions_table(text)
    }


def ttail(sid: str, last: datetime, *, readable: bool = True) -> TranscriptTail:
    return TranscriptTail(
        path=Path(f"/home/u/.claude/projects/key/{sid}.jsonl"),
        session_id=sid,
        readable=readable,
        last_record_ts=last,
        first_record_ts=last,
        tail_complete=True,
        mtime=last,
        project_key="key",
    )


def test_lifecycle_health_and_result_cells_come_from_the_classifier(ctx):
    # TST-F4: the cells are filled by ``classify_all`` (not by hand) and printed by ``render``.
    # D1 settled with a succeeded contract; D2 settled with a failed contract; D3 running with
    # no contract; D4 has no outcome and a blocked contract (the Result prints ``null``).
    inp = sweep_input(
        ctx.now,
        orca_rows=(
            obs("D1", outcome="succeeded", status="completed", worktree_path="/wt/ok"),
            obs("D2", outcome="failed", status="completed", worktree_path="/wt/bad"),
            obs("D3", outcome="pending", status="in_progress", worktree_path="/wt/run"),
            obs("D4", status="in_progress", worktree_path="/wt/blocked"),
        ),
        contracts=(
            ContractRecord(Path("/wt/ok/return-contract.yaml"), "succeeded"),
            ContractRecord(Path("/wt/bad/return-contract.yaml"), "failed"),
            ContractRecord(
                Path("/wt/blocked/return-contract.yaml"),
                "blocked",
                blocked_question="Which branch?",
            ),
        ),
    )

    text = report.render(classify_all(inp, ctx), ctx)

    assert dimension_cells(text) == {
        "orca:D1": ("settled", "unknown", "succeeded", "unknown"),
        "orca:D2": ("settled", "failed result", "failed", "unknown"),
        "orca:D3": ("running", "unknown", "unknown", "unknown"),
        "orca:D4": ("unknown", "unknown", "null", "unknown"),
    }


def test_freshness_cell_comes_from_the_classifier_for_a_fresh_and_a_stale_transcript(
    ctx,
):
    # TST-F4: no Orca row is in scope, so the join guard holds and each transcript is a person
    # session. The fresh one is 5 min old; the stale ones are 7 h old (the window is 6 h).
    # A readable stale transcript is historical (idle) and not a Sessions row; an unreadable
    # one is could not determine, so its stale freshness is printed.
    fresh = ttail("fresh-one", ctx.now - 5 * MINUTE)
    stale_readable = ttail("stale-readable", ctx.now - 7 * HOUR)
    stale_unreadable = ttail("stale-unreadable", ctx.now - 7 * HOUR, readable=False)
    inp = replace(
        sweep_input(ctx.now),
        transcripts=(fresh, stale_readable, stale_unreadable),
    )

    result = classify_all(inp, ctx)
    text = report.render(result, ctx)

    assert dimension_cells(text) == {
        "transcript:fresh-one": ("unknown", "unknown", "unknown", "fresh (300s)"),
        "transcript:stale-unreadable": (
            "unknown",
            "unknown",
            "unknown",
            "stale (25200s)",
        ),
    }
    by_id = {r.row.row_id: r for r in result.rows}
    assert by_id["transcript:stale-readable"].classification.class_name == IDLE
    assert by_id["transcript:stale-readable"].row.freshness == "stale"
    assert by_id["transcript:stale-readable"].row.freshness_age_s == 25200
    assert "transcript:stale-readable" in block(text, "## Historical sessions")


def test_dimension_9_prints_frozen_or_unknown_never_not_frozen(ctx):
    result = dimension_result(ctx)
    text = report.render(result, ctx)
    policy = {r["ID"]: r["Policy"] for r in sessions_table(text)}
    assert policy == {"orca:P1": "frozen", "orca:P2": "unknown"}
    assert "not frozen" not in text.lower()
    payload = report.to_json(result, ctx, "/r.md")
    assert [r["policy"] for r in payload["rows"]] == ["frozen", None]
    assert "not frozen" not in json.dumps(payload).lower()


# ===========================================================================================
# DESIGN 7.5 cases added by reflect run 2: set-union count and the three renderer bans
# ===========================================================================================


def test_every_session_count_line_is_a_set_union_not_a_sum(ctx):
    # S is listed twice: in Waiting (b) by its kind and in Could not determine by its class.
    rows = [
        crow("orca:A1", WAITING, "waiting_signal", kind="a"),
        crow("orca:A2", WAITING, "waiting_signal", kind="a"),
        crow("orca:B1", WAITING, "waiting_signal", kind="b"),
        crow("orca:S", UNKNOWN, "fallback", kind="b"),
        crow("orca:U1", UNKNOWN, "fallback"),
    ]
    text = report.render(result_of(ctx, rows), ctx)
    count_lines = [ln for ln in text.splitlines() if "Distinct affected sessions" in ln]
    pattern = re.compile(r"^Distinct affected sessions: \d+ \(set union, not a sum\)$")
    assert all(pattern.match(ln) for ln in count_lines)
    # Waiting (a), Waiting (b), Could not determine: two each; the Shift Brief union is 5.
    assert count_lines == [distinct(2), distinct(2), distinct(2), distinct(5)]
    assert distinct(6) not in text  # the sum of the section counts
    assert distinct(5) in block(text, "## Shift Brief").splitlines()


def test_report_holds_no_action_control(ctx):
    text = report.render(full_result(ctx), ctx)
    # The payloads are present, so the checks below are not vacuous.
    assert "&lt;button&gt;" in text
    assert "\\[x\\] orca:C1" in text
    assert re.search(r"(?m)^\s*[-*+]\s+\[[ xX]\]", text) is None
    assert re.search(r"(?<!\\)\[[ xX]\]", text) is None
    low = text.lower()
    for tag in ("<button", "<form", "<input", "<a "):
        assert tag not in low, tag


def test_report_holds_no_command_to_paste(ctx):
    text = report.render(full_result(ctx), ctx)
    assert "```" not in text
    assert "~~~" not in text
    assert not any(line.lstrip().startswith("$ ") for line in text.splitlines())
    assert len(text.splitlines()) > 40  # the fixture fills every section


def test_report_gives_no_advice_to_delete_anything_under_dev_tasks(ctx):
    text = report.render(full_result(ctx), ctx)
    mentions = [ln for ln in text.splitlines() if ".dev/tasks/" in ln.lower()]
    assert len(mentions) >= 4  # Waiting (a), Retained problems, Sessions, Worktrees
    banned = re.compile(r"delete|remove|rm |clean", re.IGNORECASE)
    for line in mentions:
        assert banned.search(line) is None, line
