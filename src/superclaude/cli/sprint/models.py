"""Sprint data models — enums, dataclasses, and pure-data types.

All other sprint modules depend on these types. Pipeline base types
(PipelineConfig, Step, StepResult, StepStatus) are imported from
superclaude.cli.pipeline for inheritance.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Optional

from superclaude.cli.pipeline.models import (
    PipelineConfig,
    Step,
    StepResult,
)

if TYPE_CHECKING:
    # Forward-ref only — recovery.py imports from models.py, so a runtime
    # import here would create a cycle. TYPE_CHECKING resolves at static
    # type-check time only; at runtime the annotation is a string.
    from .recovery import RecoveryBundleRef


@dataclass
class TaskEntry:
    """A single task parsed from a phase tasklist markdown file.

    Represents one ``### T<PP>.<TT> -- Title`` block with its metadata.
    """

    task_id: str
    title: str
    description: str = ""
    dependencies: list[str] = field(default_factory=list)
    command: str = ""
    classifier: str = ""


class TaskStatus(Enum):
    """Outcome status for a single task within a phase."""

    PASS = "pass"
    PASS_RECOVERED = "pass_recovered"  # non-zero exit but evidence of success
    FAIL_TERMINAL = "fail"
    FAIL_RECOVERABLE = "fail_recoverable"
    FAIL_PROVIDER_EXHAUSTED = "fail_provider_exhausted"  # infra: 429/account-exhaustion (re-route, not product-bug)
    INCOMPLETE = "incomplete"
    SKIPPED = "skipped"

    @property
    def is_success(self) -> bool:
        return self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)

    @property
    def is_failure(self) -> bool:
        return self in (
            TaskStatus.FAIL_TERMINAL,
            TaskStatus.FAIL_RECOVERABLE,
            TaskStatus.FAIL_PROVIDER_EXHAUSTED,
            TaskStatus.INCOMPLETE,
        )


class GateOutcome(Enum):
    """Outcome of a quality gate check for a task."""

    PASS = "pass"
    FAIL = "fail"
    DEFERRED = "deferred"
    PENDING = "pending"

    @property
    def is_success(self) -> bool:
        return self == GateOutcome.PASS


class GateDisplayState(Enum):
    """Visual state for gate status in the TUI phase table.

    Maps gate lifecycle stages to distinct display properties (color, icon, label)
    for at-a-glance feedback on trailing gate progress.

    Valid transitions:
        NONE → CHECKING → PASS
        NONE → CHECKING → FAIL_DEFERRED → REMEDIATING → REMEDIATED
        NONE → CHECKING → FAIL_DEFERRED → REMEDIATING → HALT
    """

    NONE = "none"
    CHECKING = "checking"
    PASS = "pass"
    FAIL_DEFERRED = "fail_deferred"
    REMEDIATING = "remediating"
    REMEDIATED = "remediated"
    HALT = "halt"

    @property
    def color(self) -> str:
        """Rich style string for TUI rendering."""
        return _GATE_DISPLAY_COLORS[self]

    @property
    def icon(self) -> str:
        """Short icon/label for TUI column rendering."""
        return _GATE_DISPLAY_ICONS[self]

    @property
    def label(self) -> str:
        """Human-readable label for reports."""
        return _GATE_DISPLAY_LABELS[self]


# Valid transitions: frozenset of (from_state, to_state) pairs
GATE_DISPLAY_TRANSITIONS: frozenset[tuple[GateDisplayState, GateDisplayState]] = (
    frozenset(
        {
            (GateDisplayState.NONE, GateDisplayState.CHECKING),
            (GateDisplayState.CHECKING, GateDisplayState.PASS),
            (GateDisplayState.CHECKING, GateDisplayState.FAIL_DEFERRED),
            (GateDisplayState.FAIL_DEFERRED, GateDisplayState.REMEDIATING),
            (GateDisplayState.REMEDIATING, GateDisplayState.REMEDIATED),
            (GateDisplayState.REMEDIATING, GateDisplayState.HALT),
        }
    )
)


def is_valid_gate_transition(
    from_state: GateDisplayState, to_state: GateDisplayState
) -> bool:
    """Check whether a gate display state transition is valid."""
    return (from_state, to_state) in GATE_DISPLAY_TRANSITIONS


_GATE_DISPLAY_COLORS: dict[GateDisplayState, str] = {
    GateDisplayState.NONE: "dim",
    GateDisplayState.CHECKING: "bold cyan",
    GateDisplayState.PASS: "bold green",
    GateDisplayState.FAIL_DEFERRED: "bold yellow",
    GateDisplayState.REMEDIATING: "bold magenta",
    GateDisplayState.REMEDIATED: "green",
    GateDisplayState.HALT: "bold red",
}

_GATE_DISPLAY_ICONS: dict[GateDisplayState, str] = {
    GateDisplayState.NONE: "[dim]—[/]",
    GateDisplayState.CHECKING: "[cyan]⏳[/]",
    GateDisplayState.PASS: "[green]✓[/]",
    GateDisplayState.FAIL_DEFERRED: "[yellow]⚠[/]",
    GateDisplayState.REMEDIATING: "[magenta]🔧[/]",
    GateDisplayState.REMEDIATED: "[green]✓✓[/]",
    GateDisplayState.HALT: "[red]✗[/]",
}

_GATE_DISPLAY_LABELS: dict[GateDisplayState, str] = {
    GateDisplayState.NONE: "No gate",
    GateDisplayState.CHECKING: "Checking",
    GateDisplayState.PASS: "Passed",
    GateDisplayState.FAIL_DEFERRED: "Deferred",
    GateDisplayState.REMEDIATING: "Remediating",
    GateDisplayState.REMEDIATED: "Remediated",
    GateDisplayState.HALT: "Halted",
}


@dataclass
class TaskResult:
    """Outcome of executing a single task subprocess.

    Constructed by the runner from subprocess output — not agent self-reported.
    Includes execution data, gate outcome, and reimbursement tracking.
    """

    task: TaskEntry
    status: TaskStatus = TaskStatus.SKIPPED
    turns_consumed: int = 0
    exit_code: int = 0
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    output_bytes: int = 0
    gate_outcome: GateOutcome = GateOutcome.PENDING
    reimbursement_amount: int = 0
    output_path: str = ""
    # Provider/account-exhaustion (429) recovery evidence (spec §4 Layer 2).
    failure_class: str = ""
    session_resets: int = 0
    exhausted_model: str = ""

    def to_dict(self) -> dict:
        """Serialize to a JSON-safe dict (v4.3.0 phase-N-result.json payload).

        Enum fields use ``.value`` (lowercase string). Datetimes use
        ``.isoformat()`` for UTC ISO 8601. Nested ``task`` is serialized as
        a dict literal of TaskEntry fields per checkpoints.py:write_manifest
        convention. Round-trips via from_dict().
        """
        return {
            "task": {
                "task_id": self.task.task_id,
                "title": self.task.title,
                "description": self.task.description,
                "dependencies": list(self.task.dependencies),
                "command": self.task.command,
                "classifier": self.task.classifier,
            },
            "status": self.status.value,
            "turns_consumed": self.turns_consumed,
            "exit_code": self.exit_code,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat(),
            "output_bytes": self.output_bytes,
            "gate_outcome": self.gate_outcome.value,
            "reimbursement_amount": self.reimbursement_amount,
            "output_path": str(self.output_path),
            "failure_class": self.failure_class,
            "session_resets": self.session_resets,
            "exhausted_model": self.exhausted_model,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TaskResult":
        """Reverse of to_dict(); reconstructs a TaskResult from a JSON-loaded dict."""
        task_data = data["task"]
        return cls(
            task=TaskEntry(
                task_id=task_data["task_id"],
                title=task_data["title"],
                description=task_data.get("description", ""),
                dependencies=list(task_data.get("dependencies", [])),
                command=task_data.get("command", ""),
                classifier=task_data.get("classifier", ""),
            ),
            status=TaskStatus(data["status"]),
            turns_consumed=data["turns_consumed"],
            exit_code=data["exit_code"],
            started_at=datetime.fromisoformat(data["started_at"]),
            finished_at=datetime.fromisoformat(data["finished_at"]),
            output_bytes=data["output_bytes"],
            gate_outcome=GateOutcome(data["gate_outcome"]),
            reimbursement_amount=data["reimbursement_amount"],
            output_path=data["output_path"],
            # New v4.3.0 fields — .get() defaults so OLD payloads round-trip
            # (mirrors HandoffRecord.from_dict; NOT the hard-keyed style above).
            failure_class=data.get("failure_class", ""),
            session_resets=data.get("session_resets", 0),
            exhausted_model=data.get("exhausted_model", ""),
        )

    @property
    def duration_seconds(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()

    def to_context_summary(self, *, verbose: bool = True) -> str:
        """Serialize to structured markdown for context injection.

        Args:
            verbose: If True, include full detail. If False, produce a
                compressed one-line summary for progressive summarization.

        Returns:
            Deterministic markdown string suitable for context injection.
        """
        if not verbose:
            return (
                f"- **{self.task.task_id}**: {self.status.value} "
                f"| gate: {self.gate_outcome.value}"
            )
        lines = [
            f"### {self.task.task_id} — {self.task.title}",
            f"- **Status**: {self.status.value}",
            f"- **Gate**: {self.gate_outcome.value}",
            f"- **Turns consumed**: {self.turns_consumed}",
            f"- **Duration**: {self.duration_seconds:.1f}s",
            f"- **Exit code**: {self.exit_code}",
        ]
        if self.reimbursement_amount > 0:
            lines.append(f"- **Reimbursement**: {self.reimbursement_amount} turns")
        if self.output_path:
            lines.append(f"- **Output**: {self.output_path}")
        return "\n".join(lines)


@dataclass
class HandoffRecord:
    """Runner-constructed per-task handoff record (frozen v1, schema-versioned).

    Derived from ``TaskResult.to_dict()`` plus exactly two delta fields
    (``produced_artifacts``, ``consumed_upstreams``) and a ``schema_version``.
    The RUNNER constructs this from the finalized ``TaskResult`` — it is NOT an
    agent self-report. Forward-compatible: ``from_dict`` tolerates unknown keys
    so an old reader can consume a record written by a newer ``schema_version``
    (SYNTHESIS H4 / M7). Field NAMES + ORDER match SYNTHESIS H4 verbatim. Plain
    dataclass (not ``frozen``), matching its ``TaskResult`` sibling.

    ``gate_outcome`` is the ``GateOutcome`` enum's ``.value`` string
    ("pass"/"fail"/"deferred"/"pending") — never ``dict`` or ``None`` — because
    the source ``TaskResult.gate_outcome`` is a ``GateOutcome`` enum. The H5
    resume skip predicate reads it back via ``GateOutcome(gate_outcome)``.
    """

    schema_version: int = 1
    task_id: str = ""
    phase: int = 0
    status: str = ""  # TaskStatus.value: pass/fail/fail_recoverable/incomplete/skipped
    gate_outcome: str = ""  # GateOutcome.value: pass/fail/deferred/pending
    turns_consumed: int = 0
    exit_code: int = 0
    output_path: str = ""
    started_at: str = ""
    finished_at: str = ""
    produced_artifacts: list[str] = field(default_factory=list)
    consumed_upstreams: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Hand-written JSON-safe dict (mirrors TaskResult.to_dict; NOT asdict).

        List fields are ``list(...)``-copied so the returned dict cannot alias
        the record's internal lists.
        """
        return {
            "schema_version": self.schema_version,
            "task_id": self.task_id,
            "phase": self.phase,
            "status": self.status,
            "gate_outcome": self.gate_outcome,
            "turns_consumed": self.turns_consumed,
            "exit_code": self.exit_code,
            "output_path": str(self.output_path),
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "produced_artifacts": list(self.produced_artifacts),
            "consumed_upstreams": list(self.consumed_upstreams),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "HandoffRecord":
        """Reverse of to_dict; forward-compatible (M7 migration-safe).

        Uses ``data.get(key, default)`` for every field so a dict carrying an
        UNKNOWN extra key round-trips without raising (the unknown key is simply
        ignored) and a missing optional field degrades to its default. This lets
        an old reader consume a record written by a newer ``schema_version``.
        """
        return cls(
            schema_version=data.get("schema_version", 1),
            task_id=data.get("task_id", ""),
            phase=data.get("phase", 0),
            status=data.get("status", ""),
            gate_outcome=data.get("gate_outcome", ""),
            turns_consumed=data.get("turns_consumed", 0),
            exit_code=data.get("exit_code", 0),
            output_path=data.get("output_path", ""),
            started_at=data.get("started_at", ""),
            finished_at=data.get("finished_at", ""),
            produced_artifacts=list(data.get("produced_artifacts", [])),
            consumed_upstreams=list(data.get("consumed_upstreams", [])),
        )

    @classmethod
    def from_task_result(
        cls,
        result: "TaskResult",
        *,
        phase: int,
        produced_artifacts: list[str],
        consumed_upstreams: list[str],
    ) -> "HandoffRecord":
        """Construct from a finalized TaskResult plus the two delta fields.

        Derives the shared fields from ``result`` exactly as
        ``TaskResult.to_dict`` does: ``status`` via ``result.status.value``,
        ``gate_outcome`` via ``result.gate_outcome.value`` (the GateOutcome
        enum's string value, e.g. "pass" — NEVER a dict or None), and timestamps
        via ``.isoformat()``. Reads only real ``TaskResult`` fields.
        """
        return cls(
            schema_version=1,
            task_id=result.task.task_id,
            phase=phase,
            status=result.status.value,
            gate_outcome=result.gate_outcome.value,
            turns_consumed=result.turns_consumed,
            exit_code=result.exit_code,
            output_path=str(result.output_path),
            started_at=result.started_at.isoformat(),
            finished_at=result.finished_at.isoformat(),
            produced_artifacts=list(produced_artifacts),
            consumed_upstreams=list(consumed_upstreams),
        )


class PhaseStatus(Enum):
    """Lifecycle of a single phase."""

    PENDING = "pending"
    RUNNING = "running"
    PASS = "pass"
    PASS_NO_SIGNAL = "pass_no_signal"
    PASS_NO_REPORT = "pass_no_report"
    PASS_RECOVERED = "pass_recovered"  # non-zero exit but evidence of success
    PREFLIGHT_PASS = (
        "preflight_pass"  # completed by preflight execution (python/skip mode)
    )
    # Wave 2 (v3.7): phase passed but one or more `### Checkpoint:` reports
    # declared in the tasklist were not written. Surfaced only when
    # `checkpoint_gate_mode == "full"`. Treated as success for control flow so
    # the sprint continues; the distinct value lets downstream consumers
    # (logs, retros, dashboards) flag the anomaly.
    PASS_MISSING_CHECKPOINT = "pass_missing_checkpoint"
    INCOMPLETE = "incomplete"
    HALT = "halt"
    PROVIDER_EXHAUSTED = "provider_exhausted"
    TIMEOUT = "timeout"
    ERROR = "error"
    SKIPPED = "skipped"

    @property
    def is_terminal(self) -> bool:
        return self in (
            PhaseStatus.PASS,
            PhaseStatus.PASS_NO_SIGNAL,
            PhaseStatus.PASS_NO_REPORT,
            PhaseStatus.PASS_RECOVERED,
            PhaseStatus.PREFLIGHT_PASS,
            PhaseStatus.PASS_MISSING_CHECKPOINT,
            PhaseStatus.INCOMPLETE,
            PhaseStatus.HALT,
            PhaseStatus.PROVIDER_EXHAUSTED,
            PhaseStatus.TIMEOUT,
            PhaseStatus.ERROR,
            PhaseStatus.SKIPPED,
        )

    @property
    def is_success(self) -> bool:
        return self in (
            PhaseStatus.PASS,
            PhaseStatus.PASS_NO_SIGNAL,
            PhaseStatus.PASS_NO_REPORT,
            PhaseStatus.PASS_RECOVERED,
            PhaseStatus.PREFLIGHT_PASS,
            PhaseStatus.PASS_MISSING_CHECKPOINT,
        )

    @property
    def is_failure(self) -> bool:
        return self in (
            PhaseStatus.INCOMPLETE,
            PhaseStatus.HALT,
            PhaseStatus.TIMEOUT,
            PhaseStatus.ERROR,
        )


class SprintOutcome(Enum):
    """Final sprint result."""

    SUCCESS = "success"
    HALTED = "halted"
    INTERRUPTED = "interrupted"
    ERROR = "error"


@dataclass
class Phase:
    """A single phase discovered from the tasklist index."""

    number: int
    file: Path
    name: str = ""  # extracted from phase file heading, or auto-generated
    execution_mode: str = "claude"  # claude, python, or skip
    # TUI v2 Wave 2 (v3.7): short ~60-char description of the phase scope.
    # Drives the "Prompt:" line in the active panel (F5). Populated by
    # ``load_sprint_config`` from the first intent/scope line of the phase
    # tasklist; falls back to ``display_name`` when no body is present.
    # TUI-Q1 resolution: stored on ``Phase`` (not ``SprintConfig``) because
    # the preview is phase-specific and materially different per phase.
    prompt_preview: str = ""

    @property
    def basename(self) -> str:
        return self.file.name

    @property
    def display_name(self) -> str:
        return self.name or f"Phase {self.number}"

    @property
    def prompt_display(self) -> str:
        """Return prompt_preview, falling back to display_name when empty."""
        return self.prompt_preview or self.display_name


@dataclass
class CheckpointEntry:
    """One row in a sprint's checkpoint manifest (v3.7, Wave 3).

    Built by :func:`superclaude.cli.sprint.checkpoints.build_manifest` and
    serialised by :func:`write_manifest`. Recovery metadata is populated by
    :func:`recover_missing_checkpoints` when a missing report is regenerated
    from evidence artifacts.

    Attributes:
        phase: Phase number that declared this checkpoint.
        name: Human-readable label from the ``### Checkpoint:`` heading,
            or the basename of ``expected_path`` when no heading precedes
            the path declaration.
        expected_path: Absolute path where the checkpoint report should
            exist (resolved against the sprint's release dir).
        exists: True when ``expected_path`` is a file on disk.
        recovered: True when this entry was synthesised post-hoc by
            ``recover_missing_checkpoints``.
        recovery_source: Description of the artifact(s) used to recover the
            checkpoint (e.g. ``"artifacts/D-0013, artifacts/D-0014"``).
            ``None`` when ``recovered`` is False.
    """

    phase: int
    name: str
    expected_path: Path
    exists: bool
    recovered: bool = False
    recovery_source: Optional[str] = None


# Sentinel value: grace_period >= this means "shadow forever" (T09/R5)
SHADOW_GRACE_INFINITE: int = 999_999


@dataclass
class SprintConfig(PipelineConfig):
    """Complete configuration for a sprint execution.

    Inherits shared fields from PipelineConfig (work_dir, dry_run,
    max_turns, model, permission_flag, debug). Sprint-specific fields
    are defined here. The ``release_dir`` field maps to ``work_dir``
    via __post_init__ for backward compatibility.
    """

    index_path: Path = field(default_factory=lambda: Path("."))
    release_dir: Path = field(default_factory=lambda: Path("."))
    phases: list[Phase] = field(default_factory=list)
    start_phase: int = 1
    end_phase: int = 0  # 0 = auto-detect (last phase)
    max_turns: int = 100
    model: str = ""  # empty = claude default
    dry_run: bool = False
    permission_flag: str = "--dangerously-skip-permissions"
    tmux_session_name: str = ""
    # Diagnostic fields (all default to pre-change behavior)
    debug: bool = False
    stall_timeout: int = 0  # 0 = disabled
    startup_stall_timeout: int = 300  # 0 = disabled; fires when no events received yet (process never began streaming)
    stall_action: str = "warn"  # "warn" or "kill"
    phase_timeout: int = 0  # 0 = disabled
    # Shadow mode: trailing gates run in parallel, results are metrics-only
    shadow_gates: bool = False
    # Wiring gate mode: controls post-task wiring analysis behavior
    # off=disabled, shadow=log only, soft=warn on critical, full=block on critical+major
    wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "soft"
    # Anti-instinct gate rollout mode: controls anti-instinct gate behavior in sprint
    # off=evaluate+ignore, shadow=evaluate+record, soft=evaluate+record+credit/remediate,
    # full=evaluate+record+credit/remediate+fail
    gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"
    # Wiring gate budget fields (OQ-2 resolution: conservative defaults)
    wiring_gate_scope: str = "task"  # scope for resolve_gate_mode() (Goal-5d)
    wiring_analysis_turns: int = 1  # turns allocated per wiring analysis
    remediation_cost: int = 2  # turns debited per remediation attempt
    # Scope-based wiring gate fields (T09/R5: replaces direct wiring_gate_mode setting)
    wiring_gate_enabled: bool = True
    wiring_gate_grace_period: int = 0
    # Checkpoint enforcement gate mode (v3.7, Wave 2)
    # off=disabled, shadow=log JSONL only, soft=log + stdout warning,
    # full=log + downgrade PASS to PASS_MISSING_CHECKPOINT on missing files
    checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
    # TUI v2 Wave 1 (v3.7): pre-scanned total task count across all active
    # phase files, populated by load_sprint_config. Drives the Tasks portion
    # of the dual progress bar (F3). 0 is a valid fallback when the scan
    # fails or the config is constructed directly (e.g. in unit tests).
    total_tasks: int = 0
    # Transient runtime state directory (e.g. .sprint-exitcode sentinel). Default resolved in __post_init__; override via SPRINT_STATE_DIR env var or --state-dir CLI flag.
    state_dir: Path = field(default_factory=lambda: Path(""))
    # Stage 1 (M4): per-task handoff records. handoff_enabled toggles writing the
    # typed HandoffRecord + the task_complete journal event (--handoff/--no-handoff;
    # default on). handoff_store selects the backend: "file" (the only backend
    # today) → FileHandoffStore; "mail" is reserved for the out-of-scope Stage 4
    # pilot (the Stage-4 data-rollback depends on this selector).
    handoff_enabled: bool = True
    handoff_store: str = "file"
    # Stage 2 (H5): --resume <task_id>. When non-empty, per-task resume is active:
    # tasks with a validated-success handoff record are skipped (not re-run, no
    # budget debit). Composes with the phase-granular --start/--end (which bound
    # the phase range; the validated-success skip suppresses already-done tasks
    # within it). "" = resume inactive (no per-task skipping).
    resume_task_id: str = ""
    # Stage 3 (M4): number of tasks to execute concurrently per phase. 1 =
    # sequential (the safe default — preserves byte-identical legacy behavior);
    # K>1 enables dependency-respecting bounded parallelism via the DAG scheduler.
    task_parallelism: int = 1
    # 429 recovery (spec §7 P5): max account-rotation re-spawns per task before a
    # provider-exhaustion halt for a model switch. Read by the per-phase
    # SessionResetPolicy(max_session_resets=config.max_session_resets) (P3); this
    # closes the 4-hop CLI chain so the operator flag overrides the hardcoded 8.
    max_session_resets: int = 8

    def _derive_tasklist_id(self) -> str:
        """Derive a stable tasklist identifier for the default state_dir path.

        Preference order: release_dir.name (when meaningful) -> index_path.parent.name
        (when meaningful) -> index_path.stem -> "default".
        """
        release_name = self.release_dir.name
        if self.release_dir != Path(".") and release_name not in ("", "."):
            return release_name
        parent_name = self.index_path.parent.name
        if parent_name not in ("", "."):
            return parent_name
        return self.index_path.stem or "default"

    def __post_init__(self):
        import warnings

        # Sync release_dir to PipelineConfig.work_dir so both access paths
        # return the same value.
        object.__setattr__(self, "work_dir", self.release_dir)

        # Migration shim (NFR-007: remove after 1 release)
        # Migrates deprecated field names to new canonical names.
        #
        # T16/R12 Documentation:
        # Current shim migrates internal renames from early v3.0 development:
        #   wiring_budget_turns    -> wiring_analysis_turns  (renamed for clarity)
        #   wiring_remediation_cost -> remediation_cost       (shortened)
        #   wiring_scope           -> wiring_gate_scope       (disambiguated)
        #
        # Spec-intended migration (not yet implemented):
        #   wiring_gate_mode="off"    -> wiring_gate_enabled=False
        #   wiring_gate_mode="shadow" -> wiring_gate_grace_period=SHADOW_GRACE_INFINITE
        #   This full deprecation path requires T09 scope-based fields and is deferred
        #   because wiring_gate_mode remains actively used as the resolved output.
        #   When adopted, callers using old wiring_gate_mode strings will get
        #   DeprecationWarning and automatic mapping to the new scope-based fields.
        _old_to_new = {
            "wiring_budget_turns": "wiring_analysis_turns",
            "wiring_remediation_cost": "remediation_cost",
            "wiring_scope": "wiring_gate_scope",
        }
        for old_name, new_name in _old_to_new.items():
            old_val = getattr(self, old_name, None)
            if old_val is not None:
                warnings.warn(
                    f"SprintConfig field '{old_name}' is deprecated, "
                    f"use '{new_name}' instead. "
                    f"This shim will be removed in the next release.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                object.__setattr__(self, new_name, old_val)

        # Derive wiring_gate_mode from scope-based fields (T09/R5).
        # Only derive if wiring_gate_mode was not explicitly overridden
        # (i.e., still at the default "soft" value from the field definition).
        if not self.wiring_gate_enabled:
            object.__setattr__(self, "wiring_gate_mode", "off")
        elif self.wiring_gate_grace_period >= SHADOW_GRACE_INFINITE:
            object.__setattr__(self, "wiring_gate_mode", "shadow")

        # Derive default state_dir from a tasklist-id when the field is the
        # empty-Path sentinel. The sentinel is Path("") (NOT Path(".")) so we
        # don't collide with release_dir's default and break test isolation.
        if self.state_dir == Path(""):
            object.__setattr__(
                self,
                "state_dir",
                Path(".dev/sprint-state") / self._derive_tasklist_id(),
            )

    @property
    def debug_log_path(self) -> Path:
        """Path to the debug log file within the results directory."""
        return self.results_dir / "debug.log"

    @property
    def results_dir(self) -> Path:
        return self.release_dir / "results"

    @property
    def execution_log_jsonl(self) -> Path:
        return self.release_dir / "execution-log.jsonl"

    @property
    def execution_log_md(self) -> Path:
        return self.release_dir / "execution-log.md"

    @property
    def active_phases(self) -> list[Phase]:
        """Phases within the [start, end] range."""
        end = self.end_phase or max(p.number for p in self.phases)
        return [p for p in self.phases if self.start_phase <= p.number <= end]

    def output_file(self, phase: Phase) -> Path:
        return self.results_dir / f"phase-{phase.number}-output.txt"

    def error_file(self, phase: Phase) -> Path:
        return self.results_dir / f"phase-{phase.number}-errors.txt"

    def task_output_file(self, phase: Phase, task: "TaskEntry") -> Path:
        return self.results_dir / f"phase-{phase.number}-task-{task.task_id}-output.txt"

    def task_error_file(self, phase: Phase, task: "TaskEntry") -> Path:
        return self.results_dir / f"phase-{phase.number}-task-{task.task_id}-errors.txt"

    def handoff_file(self, phase: "Phase", task: "TaskEntry") -> Path:
        """Phase-qualified per-task handoff record path (H5 on-disk key).

        Mirrors ``task_output_file``. The key is phase-qualified because the bare
        ``T<PP>.<TT>`` id is not sprint-unique and collides across phases.
        """
        return (
            self.results_dir
            / "handoff"
            / f"phase-{phase.number}-task-{task.task_id}.json"
        )

    def result_file(self, phase: Phase) -> Path:
        return self.results_dir / f"phase-{phase.number}-result.md"

    def phase_result_json(self, phase: Phase) -> Path:
        return self.results_dir / f"phase-{phase.number}-result.json"


@dataclass
class SprintStep(Step):
    """A pipeline step specialised for sprint phase execution.

    Extends pipeline.Step with sprint-specific fields.
    """

    phase_number: int = 0


@dataclass
class PhaseResult(StepResult):
    """Outcome of executing a single phase.

    Inherits from pipeline.StepResult for shared timing fields.
    Sprint-specific fields (phase, exit_code, etc.) are defined here.
    """

    phase: Phase = field(default_factory=lambda: Phase(number=0, file=Path(".")))
    status: PhaseStatus = PhaseStatus.PENDING
    exit_code: int = 0
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    output_bytes: int = 0
    error_bytes: int = 0
    last_task_id: str = ""
    files_changed: int = 0
    # TUI v2 Wave 1 (v3.7): phase-level totals captured when the phase ends.
    # Populated from the final MonitorState; default to 0 for python/skip-mode
    # phases that never ran a claude subprocess.
    turns: int = 0
    tokens_in: int = 0
    tokens_out: int = 0
    # v4.3.0: granular task evidence for rerun-tasks (TDD §T6)
    task_results: list["TaskResult"] = field(default_factory=list)
    recovery_history: list["RecoveryBundleRef"] = field(default_factory=list)
    # 429 recovery: phase-level account-exhaustion halt signal (spec §4). Set by
    # the single-session path (PROVIDER_EXHAUSTED) and derived from per-task
    # `failure_class` on the per-task path; persisted via _write_phase_result_json.
    halt_reason: str = ""
    exhausted_model: str = ""

    @property
    def duration_seconds(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()

    @property
    def duration_display(self) -> str:
        s = int(self.duration_seconds)
        if s < 60:
            return f"{s}s"
        return f"{s // 60}m {s % 60}s"


@dataclass
class SprintResult:
    """Aggregate result for the entire sprint."""

    config: SprintConfig
    phase_results: list[PhaseResult] = field(default_factory=list)
    outcome: SprintOutcome = SprintOutcome.SUCCESS
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: Optional[datetime] = None
    halt_phase: Optional[int] = None

    @property
    def duration_seconds(self) -> float:
        end = self.finished_at or datetime.now(timezone.utc)
        return (end - self.started_at).total_seconds()

    @property
    def duration_display(self) -> str:
        s = int(self.duration_seconds)
        if s < 3600:
            return f"{s // 60}m {s % 60}s"
        return f"{s // 3600}h {(s % 3600) // 60}m"

    @property
    def phases_passed(self) -> int:
        return sum(1 for r in self.phase_results if r.status.is_success)

    @property
    def phases_failed(self) -> int:
        return sum(1 for r in self.phase_results if r.status.is_failure)

    # TUI v2 Wave 1 (v3.7): cross-phase aggregates used by the enhanced
    # terminal panels (F6) and the release retrospective (F10). Each
    # property sums the matching per-phase field across ``phase_results``.
    @property
    def total_turns(self) -> int:
        return sum(r.turns for r in self.phase_results)

    @property
    def total_tokens_in(self) -> int:
        return sum(r.tokens_in for r in self.phase_results)

    @property
    def total_tokens_out(self) -> int:
        return sum(r.tokens_out for r in self.phase_results)

    @property
    def total_output_bytes(self) -> int:
        return sum(r.output_bytes for r in self.phase_results)

    @property
    def total_files_changed(self) -> int:
        return sum(r.files_changed for r in self.phase_results)

    def _exhaustion_halt(self) -> tuple[str, str] | None:
        """Return ``(halt_task_id, exhausted_model)`` for a provider-exhaustion halt.

        A 429 account-exhaustion halt is recovered by a MODEL SWITCH, not by
        re-running the same model at the same phase (``--start``) — that model's
        account pool is exhausted. This inspects the halted phase's persisted
        ``halt_reason`` (set by the single-session ``PROVIDER_EXHAUSTED`` path and
        derived from per-task ``failure_class`` on the per-task path) and returns
        the specific exhausted task id + resolved model so the resume UX can
        suggest an alternate alias. Returns ``None`` for any non-exhaustion halt.
        """
        if self.halt_phase is None:
            return None
        halted = next(
            (r for r in self.phase_results if r.phase.number == self.halt_phase),
            None,
        )
        if halted is None or halted.halt_reason != "provider_exhaustion":
            return None
        halt_task_id = next(
            (
                tr.task.task_id
                for tr in halted.task_results
                if tr.failure_class == "provider_exhaustion"
            ),
            halted.last_task_id,
        )
        return halt_task_id, halted.exhausted_model

    def resume_command(self) -> str:
        if self.halt_phase is None:
            return ""
        exhaustion = self._exhaustion_halt()
        if exhaustion is not None:
            # Provider/account exhaustion → re-route via a model switch. Import
            # locally to avoid a module-load dependency on the aienv reader.
            from .aienv import suggest_alternate_model

            halt_task_id, exhausted_model = exhaustion
            suggested = (
                suggest_alternate_model(exhausted_model) if exhausted_model else None
            )
            if suggested:
                end = self.config.end_phase or max(p.number for p in self.config.phases)
                if halt_task_id:
                    return (
                        f"superclaude sprint run {self.config.index_path} "
                        f"--resume {halt_task_id} --model {suggested}"
                    )
                # R2-H6: single-session halt has no per-task id → emit a phase-level
                # resume that STILL carries the model switch (the re-route lever),
                # rather than dropping ``--model`` and silently re-running the
                # exhausted model.
                return (
                    f"superclaude sprint run {self.config.index_path} "
                    f"--start {self.halt_phase} --end {end} --model {suggested}"
                )
            # None-safe: no distinct alternate alias found — fall through to the
            # phase-level resume so the operator still has a paste-ready command
            # (they switch the model manually); never fabricate a ``--model``.
        end = self.config.end_phase or max(p.number for p in self.config.phases)
        return (
            f"superclaude sprint run {self.config.index_path} "
            f"--start {self.halt_phase} --end {end}"
        )

    def account_exhaustion_output(self) -> str:
        """Render the full account-exhaustion halt block, or ``""`` if N/A.

        Wraps :func:`build_account_exhaustion_halt` for the single place a
        multi-section block fits (the markdown execution-log summary). Returns
        ``""`` for any non-exhaustion halt so callers can unconditionally append
        the result. ``remaining_tasks`` is left empty here — the per-phase
        outcomes already recorded in the summary cover progress; the block's
        load-bearing content is the rationale + the single-line resume command.
        """
        exhaustion = self._exhaustion_halt()
        if exhaustion is None:
            return ""
        from .aienv import suggest_alternate_model

        halt_task_id, exhausted_model = exhaustion
        suggested = (
            suggest_alternate_model(exhausted_model) if exhausted_model else None
        )
        return build_account_exhaustion_halt(
            self.config,
            halt_task_id,
            exhausted_model,
            suggested,
            remaining_tasks=[],
        )


@dataclass
class MonitorState:
    """Real-time state extracted by the sidecar monitor thread.

    With stream-json output, liveness is tracked via ``last_event_time``
    (updated on each parsed NDJSON line) rather than raw byte growth.

    TUI v2 (v3.7, Wave 1) fields feed the redesigned live display:
    ``turns``/``tokens_*`` for the phase table, ``activity_log`` for the
    3-line tool stream, ``errors`` for the conditional error panel,
    ``last_assistant_text`` for the Agent context line, and
    ``total_tasks_in_phase``/``completed_task_estimate`` for the dual
    progress bar. All defaults preserve existing v3.6 behaviour when the
    TUI v2 renderer is absent.
    """

    output_bytes: int = 0
    output_bytes_prev: int = 0
    last_growth_time: float = field(default_factory=time.monotonic)
    last_event_time: float = field(default_factory=time.monotonic)
    phase_started_at: float = field(default_factory=time.monotonic)
    events_received: int = 0
    last_task_id: str = ""
    last_tool_used: str = ""
    files_changed: int = 0
    lines_total: int = 0
    growth_rate_bps: float = 0.0  # bytes per second
    stall_seconds: float = 0.0
    # TUI v2 Wave 1 (v3.7): richer telemetry extracted from stream-json.
    # F1: ring buffer of the last 3 tool calls — (timestamp, tool_name, description)
    activity_log: list[tuple[float, str, str]] = field(default_factory=list)
    # F2: count of assistant message events for the current phase
    turns: int = 0
    # F4: ring buffer of the last 10 errors — (task_id, tool_name, message)
    errors: list[tuple[str, str, str]] = field(default_factory=list)
    # F5: last ~80 chars of assistant text output (live "Agent:" line)
    last_assistant_text: str = ""
    # F3: task count in the current phase file (set by Monitor.reset)
    total_tasks_in_phase: int = 0
    # F3: estimated completed tasks within the current phase
    completed_task_estimate: int = 0
    # F6: accumulated input/output tokens for the current phase
    tokens_in: int = 0
    tokens_out: int = 0

    @property
    def stall_status(self) -> str:
        now = time.monotonic()
        if self.events_received == 0:
            # No events yet — subprocess is starting up
            if now - self.phase_started_at > 120:
                return "STALLED"
            return "waiting..."
        # Events have been flowing — check time since last event
        since_last = now - self.last_event_time
        if since_last > 120:
            return "STALLED"
        if since_last > 30:
            return "thinking..."
        return "active"

    @property
    def output_size_display(self) -> str:
        if self.output_bytes < 1024:
            return f"{self.output_bytes} B"
        if self.output_bytes < 1024 * 1024:
            return f"{self.output_bytes / 1024:.1f} KB"
        return f"{self.output_bytes / (1024 * 1024):.1f} MB"


@dataclass
class TurnLedger:
    """Economic model for subprocess turn budget tracking.

    Tracks budget allocation, consumption, and reimbursement for sprint
    subprocesses. Enforces monotonicity: consumed can only increase.

    Wiring analysis budget fields (NFR-004: all default to 0):
    - wiring_turns_used: cumulative turns consumed by wiring analysis
    - wiring_turns_credited: cumulative turns credited back from wiring analysis
    - wiring_budget_exhausted: 1 if wiring budget is exhausted, 0 otherwise
    """

    initial_budget: int
    consumed: int = 0
    reimbursed: int = 0
    reimbursement_rate: float = 0.8
    minimum_allocation: int = 5
    minimum_remediation_budget: int = 3
    # Wiring analysis budget tracking (NFR-004: default to zero)
    wiring_turns_used: int = 0
    wiring_turns_credited: int = 0
    wiring_budget_exhausted: int = 0
    wiring_analyses_count: int = 0  # T10/A5: count of wiring analyses executed

    def __post_init__(self) -> None:
        # Stage 3: lock for thread-safe budget mutation under K>1 task parallelism.
        # Created as a NON-FIELD instance attribute so it is excluded from the
        # dataclass __eq__/__repr__ and any field-based serialization (asdict).
        # RLock (reentrant) so try_launch can call the already-guarded debit while
        # holding the lock. Single-threaded behavior (K=1) is unchanged.
        self._lock = threading.RLock()

    def available(self) -> int:
        """Return available turns: initial_budget - consumed + reimbursed."""
        return self.initial_budget - self.consumed + self.reimbursed

    def debit(self, turns: int) -> None:
        """Consume turns from the budget. Enforces monotonicity."""
        if turns < 0:
            raise ValueError("debit amount must be non-negative")
        with self._lock:
            self.consumed += turns

    def credit(self, turns: int) -> None:
        """Reimburse turns to the budget."""
        if turns < 0:
            raise ValueError("credit amount must be non-negative")
        with self._lock:
            self.reimbursed += turns

    def can_launch(self) -> bool:
        """Return True if enough budget remains for a subprocess launch."""
        return self.available() >= self.minimum_allocation

    def try_launch(self, allocation: int | None = None) -> bool:
        """Atomically check-and-debit a launch allocation (Stage 3 TOCTOU fix).

        Under the lock: if ``can_launch()`` holds, debit ``minimum_allocation``
        (the default) and return True; otherwise return False WITHOUT debiting.
        This collapses the check-then-act ``can_launch()`` → ``debit(...)`` pair
        into one atomic operation so two concurrent workers cannot both pass the
        check and both debit, over-committing the budget. Guarding the individual
        methods is insufficient because the TOCTOU spans two calls.
        """
        debit_amount = self.minimum_allocation if allocation is None else allocation
        with self._lock:
            if not self.can_launch():
                return False
            self.debit(debit_amount)
            return True

    def can_remediate(self) -> bool:
        """Return True if enough budget remains for remediation."""
        return self.available() >= self.minimum_remediation_budget

    def debit_wiring(self, turns: int = 1) -> None:
        """Debit turns for wiring analysis before analysis runs.

        Decrements available budget and tracks wiring-specific consumption.
        Sets wiring_budget_exhausted if budget drops below minimum.
        """
        if turns < 0:
            raise ValueError("debit_wiring amount must be non-negative")
        with self._lock:
            self.debit(turns)
            self.wiring_turns_used += turns
            self.wiring_analyses_count += 1
            if self.available() < self.minimum_remediation_budget:
                self.wiring_budget_exhausted = 1

    def credit_wiring(self, turns: int, rate: float | None = None) -> int:
        """Credit turns back after wiring analysis with floor-to-zero arithmetic.

        Uses ``int(turns * rate)`` which floors to zero for fractional results.
        By design: ``credit_wiring(1, 0.8)`` returns 0 credits (R7).

        Returns the number of turns actually credited.
        """
        if turns < 0:
            raise ValueError("credit_wiring turns must be non-negative")
        effective_rate = rate if rate is not None else self.reimbursement_rate
        credit_amount = int(turns * effective_rate)
        with self._lock:
            if credit_amount > 0:
                self.credit(credit_amount)
            self.wiring_turns_credited += credit_amount
        return credit_amount

    def can_run_wiring_gate(self) -> bool:
        """Return True if budget allows running wiring analysis."""
        if self.wiring_budget_exhausted:
            return False
        return self.available() >= self.minimum_remediation_budget


def build_resume_output(
    config: SprintConfig,
    halt_task_id: str,
    remaining_tasks: list[TaskEntry],
    diagnostic_path: str | None = None,
    ledger: TurnLedger | None = None,
) -> str:
    """Build actionable HALT output with resume command and context.

    Produces an actionable resume block containing:
    - Resume command with exact task ID
    - Remaining tasks in execution order
    - Diagnostic output reference (if available)
    - Budget suggestion based on remaining work

    Args:
        config: Sprint configuration.
        halt_task_id: The first uncompleted task ID.
        remaining_tasks: Tasks not yet attempted, in execution order.
        diagnostic_path: Path to diagnostic output (if chain produced results).
        ledger: TurnLedger for budget suggestion.

    Returns:
        Formatted HALT output string.
    """
    remaining_count = len(remaining_tasks)
    budget_suggestion = max(remaining_count * 10, 50) if remaining_count > 0 else 0

    lines = [
        "## HALT — Sprint Paused",
        "",
        "### Resume Command",
        "```",
        f"superclaude sprint run {config.index_path} --resume {halt_task_id} --max-turns {budget_suggestion}",
        "```",
        "",
        f"### Remaining Tasks ({remaining_count})",
    ]

    for task in remaining_tasks:
        lines.append(f"- {task.task_id}: {task.title}")

    if diagnostic_path:
        lines.append("")
        lines.append("### Diagnostic Output")
        lines.append(f"See: {diagnostic_path}")

    if ledger:
        lines.append("")
        lines.append("### Budget Status")
        lines.append(f"- Consumed: {ledger.consumed} turns")
        lines.append(f"- Available: {ledger.available()} turns")
        lines.append(f"- Suggested budget for resume: {budget_suggestion} turns")

    return "\n".join(lines)


def build_account_exhaustion_halt(
    config: SprintConfig,
    halt_task_id: str,
    exhausted_model: str,
    suggested_model: str | None,
    remaining_tasks: list[TaskEntry],
    ledger: TurnLedger | None = None,
) -> str:
    """Build the HALT output for an account/provider-exhaustion stop.

    Distinct from :func:`build_resume_output`: a 429 account-exhaustion halt is
    NOT recovered by re-running with more turns — every routed CLIProxyAPI
    account for ``exhausted_model`` is cooling down via the provider, so the only
    re-route that helps is a *model switch*. When the P5 suggester found a
    distinct alternate (``suggested_model``), the resume command carries
    ``--model {suggested_model}`` on a SINGLE line (the operator's terminal
    cannot paste a multi-line command). When no alternate exists
    (``suggested_model is None``), the message names the exhausted model and
    gives generic recovery guidance WITHOUT fabricating an alias (edge case #7).

    Args:
        config: Sprint configuration (for ``index_path`` in the resume command).
        halt_task_id: The task ID to resume from.
        exhausted_model: The resolved model whose account pool is exhausted.
        suggested_model: A distinct alternate alias to switch to, or ``None``.
        remaining_tasks: Tasks not yet attempted, in execution order.
        ledger: Optional TurnLedger for an informational budget block.

    Returns:
        Formatted HALT output string (single-line resume command).
    """
    remaining_count = len(remaining_tasks)

    lines = [
        "## HALT — Account / Provider Exhaustion",
        "",
        (
            f"The model `{exhausted_model}` is exhausted: all routed CLIProxyAPI "
            "accounts for it are cooling down via the provider, so re-spawning a "
            "fresh session cannot reach a non-exhausted account — only a model "
            "switch re-routes to a different account pool."
        ),
        "",
    ]

    if suggested_model:
        lines += [
            "### Resume Command (switch model)",
            "```",
            f"superclaude sprint run {config.index_path} --resume {halt_task_id} --model {suggested_model}",
            "```",
        ]
    else:
        lines += [
            "### Recovery",
            (
                "- No alternate model alias was found in your environment. "
                "Configure an alternate model alias (e.g. in `~/.aienv`) whose "
                "account pool is not exhausted, or wait for the provider "
                "rate-limit window to clear, then resume."
            ),
            "",
            "### Resume Command",
            "```",
            f"superclaude sprint run {config.index_path} --resume {halt_task_id}",
            "```",
        ]

    lines += ["", f"### Remaining Tasks ({remaining_count})"]
    for task in remaining_tasks:
        lines.append(f"- {task.task_id}: {task.title}")

    if ledger:
        lines += [
            "",
            "### Budget Status",
            f"- Consumed: {ledger.consumed} turns",
            f"- Available: {ledger.available()} turns",
        ]

    return "\n".join(lines)


@dataclass
class ShadowGateMetrics:
    """Aggregated metrics from shadow gate evaluation.

    Collected when ``--shadow-gates`` is enabled. Shadow metrics are
    informational only and do not affect sprint behavior.
    """

    total_evaluated: int = 0
    passed: int = 0
    failed: int = 0
    latency_ms: list[float] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        """Fraction of gates that passed (0.0–1.0)."""
        if self.total_evaluated == 0:
            return 0.0
        return self.passed / self.total_evaluated

    @property
    def p50_latency_ms(self) -> float:
        """Median gate evaluation latency in milliseconds."""
        if not self.latency_ms:
            return 0.0
        s = sorted(self.latency_ms)
        mid = len(s) // 2
        if len(s) % 2 == 0:
            return (s[mid - 1] + s[mid]) / 2
        return s[mid]

    @property
    def p95_latency_ms(self) -> float:
        """95th percentile gate evaluation latency in milliseconds."""
        if not self.latency_ms:
            return 0.0
        s = sorted(self.latency_ms)
        idx = int(len(s) * 0.95)
        return s[min(idx, len(s) - 1)]

    def record(self, passed: bool, evaluation_ms: float) -> None:
        """Record a single shadow gate result."""
        self.total_evaluated += 1
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        self.latency_ms.append(evaluation_ms)
