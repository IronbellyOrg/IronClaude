"""Frozen data model for the read-only ``superclaude sweep`` (DESIGN section 7.2).

Every type is a frozen dataclass; collections are tuples. Class and state names
are plain ``str`` constants collected in tuples and printed as they are. Times
are aware UTC ``datetime`` values (parsed by ``probes.parse_time``). Only the
standard library is imported, and no type from ``superclaude.contracts`` is
redeclared here (DESIGN line 219).
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

JSON_SCHEMA_VERSION = 1

# Shared by ``probes`` (which reads a contract through a row's report folder) and
# ``classify`` (which attaches that contract to the row), so the two cannot drift.
CONTRACT_FILE = "return-contract.yaml"
REPORT_DIR_RE = re.compile(
    r"--(?:report-dir|output-dir|output)[ =]+"
    r"(?:\"([^\"]+)\"|'([^']+)'|([^\s'\"`]+))"  # a quoted value is taken whole
)


def report_folders(text: str, worktree: str | None) -> tuple[str, ...]:
    """Report folders a brief's text names, absolute and without a trailing slash.

    A relative folder (the WC-16 example ``--report-dir .dev/tdd/auth-1/``) resolves
    against the worker's worktree; with no worktree path it names nothing.
    """
    folders: list[str] = []
    for match in REPORT_DIR_RE.finditer(text):
        raw = match.group(1) or match.group(2) or match.group(3)
        if raw.startswith("/"):
            folders.append(raw.rstrip("/"))
        elif worktree:
            folders.append(os.path.normpath(os.path.join(worktree, raw)))
    return tuple(folders)


# Reason texts ``probes`` writes into an unscanned ``worker-show`` source row and
# ``classify`` reads back to count ``bound_reached`` (FR-020).
SHOW_CAP_REASON = "show cap reached"
TIME_BUDGET_REASON = "time budget reached"

CLASSES: tuple[str, ...] = (
    "waiting on a person",
    "stalled (proved)",
    "fenced",
    "working",
    "finished",
    "idle",
    "person session (active)",
    "could not determine",
)

# Precedence order, first match wins (read by ``classify.package_state``).
PACKAGE_STATES: tuple[str, ...] = (
    "conflict",
    "interrupted-archive",
    "archive-blocked",
    "unfinished",
    "archived",
    "unknown",
)

SAFE_VALUES: tuple[str, ...] = ("yes", "no", "could not determine")


@dataclass(frozen=True)
class SweepContext:
    now: datetime
    window: timedelta
    window_start: datetime  # now - window
    root: Path
    runs: tuple[str, ...]


@dataclass(frozen=True)
class OrcaObservation:
    dispatch: str
    run: str
    # Orca-side join value (DESIGN 2.2 path A or B); None until it is observed.
    session_join: str | None = None
    # Parsed from worker-show dispatch.dispatchedAt, dispatch.completedAt and
    # dispatch.status; all three are None for a row with no worker-show result.
    dispatch_started: datetime | None = None
    dispatch_ended: datetime | None = None
    dispatch_status: str | None = None
    liveness_verdict: str | None = None  # live, unverifiable, exited or None
    status: str | None = None
    outcome: str | None = None
    # Reserved: no code sets these two while the agentWait lookup is off (DESIGN open item 6).
    agent_wait: object | None = None
    agent_wait_present: bool = False  # null versus absent (GQ-58)
    parent: str | None = None
    worktree_path: str | None = None
    body_text: str | None = None
    unsupervised: bool | None = None
    terminal_state: str | None = None
    next_action: str | None = None
    worker_done_seen: bool | None = None
    fenced_evidence: str = "unreadable"  # present, absent or unreadable
    task_spec_text: str | None = None
    # Reserved: the agentWait time. No code sets it while the lookup is off (DESIGN open item 6).
    agent_wait_since: datetime | None = None


@dataclass(frozen=True)
class ContractRecord:
    path: Path
    worker_status: str | None = None
    blocked_question: str | None = None
    reason: str | None = None
    report_path: Path | None = None
    artifacts: tuple[Path, ...] = ()
    command: str | None = None
    # The contract file's st_mtime (aware UTC); the Waiting (a) age uses it (SP-15).
    mtime: datetime | None = None


@dataclass(frozen=True)
class TranscriptTail:
    path: Path
    session_id: str | None
    readable: bool
    last_record_ts: datetime | None
    # Earliest timestamp among the complete records in the tail; for a file over
    # 256 KiB this is not the session start.
    first_record_ts: datetime | None
    # True when the read began at byte 0, so the first complete record is the file's first.
    tail_complete: bool
    mtime: datetime
    project_key: str


@dataclass(frozen=True)
class TabMapEntry:
    file_name: str  # pane key with ":" written as "+"
    session_id: str
    launch_dir: str
    terminal_handle: str


@dataclass(frozen=True)
class SessionRow:
    id: str
    person_started: bool | None
    orca: OrcaObservation | None
    contract: ContractRecord | None
    transcript_path: Path | None
    transcript_readable: bool | None
    last_activity: datetime | None
    gate_policy: str | None
    row_id: str
    # The #409 dimensions, nine fields (OQ-11): dimension 9 "policy" is not a field here,
    # it is printed from ClassifiedRow.policy; they are report-only, never JSON keys.
    lifecycle: str = "unknown"
    phase: str = "unknown"
    health: str = "unknown"
    approval: str = "unknown"
    freshness: str = "unknown"
    freshness_age_s: int | None = None
    result: str = "unknown"
    admission: str = "unknown"
    evidence_packet: str = "unknown"
    tests_review: str | None = None


@dataclass(frozen=True)
class StatusParse:
    entries: tuple[tuple[str, str], ...]  # (XY code, path)
    branch_header: str
    ahead: int | None
    has_upstream: bool | None
    header_note: str | None


@dataclass(frozen=True)
class PackageRecord:
    id: str
    location: str  # to-do, done or both
    has_final_line: bool | None
    archiving_marker: bool
    active: bool | None
    state: str  # set by classify.package_state


@dataclass(frozen=True)
class WorktreeState:
    path: str
    status_read: bool
    uncommitted: bool | None
    unpushed: bool | None
    dev_tasks_unsaved: bool | None
    changed_paths: tuple[str, ...]
    packages: tuple[PackageRecord, ...]
    shared_package_ids: tuple[str, ...]
    frozen: bool | None
    upstream_note: str | None = None
    # Set after mark_shared_packages / classify.removable (DESIGN 7.2 SweepResult, 7.4 JSON).
    removable: str = "could not determine"
    removable_reason: str | None = None


@dataclass(frozen=True)
class Classification:
    class_name: str  # JSON key "class"
    waiting_kind: str | None  # "a", "b" or None
    rule: str
    evidence: str
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class SafeToClose:
    terminal: str
    worktree: str
    reason: str | None = None


@dataclass(frozen=True)
class SourceCoverage:
    name: str
    coverage: str
    age_seconds: int | None
    unscanned: str | None


@dataclass(frozen=True)
class SweepInput:
    orca_rows: tuple[OrcaObservation, ...]
    contracts: tuple[ContractRecord, ...]
    transcripts: tuple[TranscriptTail, ...]
    tab_map: tuple[TabMapEntry, ...]
    worktrees: tuple[WorktreeState, ...]
    sources: tuple[SourceCoverage, ...]
    orca_available: bool
    orca_binary: str
    orca_version: str | None
    truncated: bool
    collected_start: datetime
    collected_end: datetime


# OQ-14: builder decision, the row plus Classification, policy and SafeToClose (DESIGN line 468).
@dataclass(frozen=True)
class ClassifiedRow:
    row: SessionRow
    classification: Classification
    policy: str | None  # classify.policy_of value: "frozen" or None
    safe: SafeToClose


@dataclass(frozen=True)
class SweepResult:
    rows: tuple[ClassifiedRow, ...]
    worktrees: tuple[WorktreeState, ...]  # after mark_shared_packages
    waiting_a: tuple[str, ...]  # row ids
    waiting_b: tuple[str, ...]  # row ids
    # counts per class (zeros included), bound_reached, visible, historical, total,
    # total_is_lower_bound
    summary: dict[str, object]
    # Header data carried from SweepContext and SweepInput.
    context: SweepContext
    sources: tuple[SourceCoverage, ...]
    orca_available: bool
    orca_binary: str
    orca_version: str | None
    truncated: bool
    collected_start: datetime
    collected_end: datetime
