"""Sprint recovery — RecoveryBundle abstraction and merge engine.

Consumed by `rerun_tasks.py` (v4.3.0) and the future v4.4.0 `sprint repair`
umbrella verb. Centralises merge-back logic so multiple recovery verbs share
one engine and one audit log. Mirrors the canonical conventions established
in `checkpoints.py` (module docstring, import grouping, section banners,
atomic file writes via temp-file + replace).

The `Nominator` Protocol decouples failed-task selection from merge: the
v4.3.0 `ManualNominator` reads `--tasks T01.01,T01.02` from CLI flags; the
v4.4.0 `ReflectReportNominator` resolves `--from-reflect-report` against
the sc:reflect deviation taxonomy.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import signal
import socket
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional, Protocol

from .debug_logger import debug_log
from .models import PhaseResult, TaskResult, TaskStatus

__all__ = [
    "RecoveryStatus",
    "RecoveryBundle",
    "RecoveryBundleRef",
    "Nominator",
    "ManualNominator",
    "ReflectReportNominator",
    "compute_tasklist_sha256",
    "write_recovery_audit_log",
    "acquire_recovery_lock",
    "release_recovery_lock",
    "acquire_run_lock",
    "release_run_lock",
    "retry_count_for_task",
    "merge_recovery_bundle",
    # Re-exports for downstream consumers (rerun_tasks.py, sprint repair v4.4.0):
    "PhaseResult",
    "TaskResult",
    "TaskStatus",
]

_recovery_logger = logging.getLogger("superclaude.sprint.recovery")


# ---------------------------------------------------------------------------
# Section A — Status enums
# ---------------------------------------------------------------------------


class RecoveryStatus(Enum):
    """Outcome status for a recovery merge operation."""

    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    DRYRUN = "dryrun"

    @property
    def is_terminal(self) -> bool:
        return self in (RecoveryStatus.SUCCESS, RecoveryStatus.FAILED)


# ---------------------------------------------------------------------------
# Section B — Recovery bundle dataclass
# ---------------------------------------------------------------------------


@dataclass
class RecoveryBundle:
    """Record of a single recovery merge operation against a phase.

    Authored by the rerun-tasks verb (v4.3.0) and any future recovery verb
    sharing the merge engine. Persisted as JSON inside the bundle directory
    and appended-by-reference to ``PhaseResult.recovery_history`` so the
    audit chain across multiple retries is preserved.

    Attributes:
        bundle_id: Stable identifier (`rerun-<isots>` for rerun-tasks).
        affected_phase: Phase number whose results were merged back.
        verb: Recovery verb that produced this bundle (default `rerun-tasks`).
        affected_tasks: Task IDs that were re-executed in this bundle.
        artifacts_produced: Files written by the rerun (per-task outputs,
            phase-N-result.{md,json}, audit log).
        artifacts_replaced: Mapping ``canonical_path -> preserved_path`` where
            the preserved path is the ``.failed-<ts>`` forensic rename of
            the prior canonical artifact (TDD line 79).
        source_tasklist_sha256: SHA256 of the tasklist BEFORE the rerun.
            Compared against the tasklist on disk at merge time to detect
            mid-flight edits (TDD T8.1).
        end_tasklist_sha256: SHA256 of the tasklist AFTER the merge. Null
            until the merge completes.
        status: Outcome status; defaults to ``DRYRUN`` until the engine
            commits a real merge.
        rerun_attempt: Attempt counter, 1..3. Capped at 3 per TDD T8.2.
    """

    bundle_id: str
    affected_phase: int
    verb: str = "rerun-tasks"
    affected_tasks: list[str] = field(default_factory=list)
    artifacts_produced: list[Path] = field(default_factory=list)
    artifacts_replaced: dict[Path, Path] = field(default_factory=dict)
    source_tasklist_sha256: str = ""
    end_tasklist_sha256: Optional[str] = None
    status: RecoveryStatus = RecoveryStatus.DRYRUN
    rerun_attempt: int = 1


@dataclass
class RecoveryBundleRef:
    """Compact reference appended to ``PhaseResult.recovery_history``.

    Holds the minimal pointer needed to locate the full RecoveryBundle on
    disk without forcing models.py to import recovery.py (circular-import
    avoidance, per Phase 1 Step 1.6).

    Attributes:
        bundle_id: Matches ``RecoveryBundle.bundle_id``.
        path: Filesystem path to the persisted bundle JSON.
        status: Final ``RecoveryStatus`` at merge completion.
        timestamp: UTC timezone-aware moment the reference was created.
    """

    bundle_id: str
    path: Path
    status: RecoveryStatus
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Section C — Nomination protocol (manual + reflect-report)
# ---------------------------------------------------------------------------


class Nominator(Protocol):
    """Strategy interface that selects which task IDs to re-execute."""

    def nominate(self, context: dict) -> list[str]: ...


class ManualNominator:
    """Wraps the explicit ``--tasks T01.01,T01.02`` CLI flag list (v4.3.0).

    Default nominator for `sprint rerun-tasks --phase N --tasks ...`.
    Returns the operator-provided task IDs verbatim, no filtering.
    """

    def __init__(self, phase: int, tasks: list[str]):
        self.phase = phase
        self.tasks = tasks

    def nominate(self, context: dict) -> list[str]:
        return list(self.tasks)


class ReflectReportNominator:
    """Resolves ``--from-reflect-report`` against a sc:reflect deviation register.

    v4.3.0 STUB — the canonical reflect-report schema ships in v4.4.0
    alongside SprintRunReflect (TDD line 149 co-dependency note). This
    v4.3.0 implementation documents the expected schema and returns an
    empty list with a `reflect_report_nominator_v43_stub` debug-log event
    so operators can wire the flag now and have it activate cleanly when
    v4.4.0 lands the schema.

    Expected v4.4.0 schema (JSON-by-default, YAML optional):
        {
          "task_id": "T07.11",
          "classification": "regression" | "drift" | "necessary" | "authorized",
          "phase": 7,
          ...
        }

    Only entries with ``classification == "regression"`` or
    ``classification == "drift"`` are nominated (TDD line 143).
    """

    def __init__(self, report_path: Path):
        self.report_path = report_path

    def nominate(self, context: dict) -> list[str]:
        try:
            raw = self.report_path.read_text(encoding="utf-8")
        except OSError:
            return []

        entries: list[dict] = []
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                entries = [e for e in data if isinstance(e, dict)]
            elif isinstance(data, dict) and "deviations" in data:
                entries = [e for e in data["deviations"] if isinstance(e, dict)]
        except json.JSONDecodeError:
            try:
                import yaml  # type: ignore[import-not-found]

                data = yaml.safe_load(raw)
                if isinstance(data, list):
                    entries = [e for e in data if isinstance(e, dict)]
                elif isinstance(data, dict) and "deviations" in data:
                    entries = [e for e in data["deviations"] if isinstance(e, dict)]
            except ImportError:
                entries = []
            except Exception:
                entries = []

        debug_log(
            _recovery_logger,
            "reflect_report_nominator_v43_stub",
            report_path=str(self.report_path),
            entries_seen=len(entries),
        )

        nominated: list[str] = []
        for entry in entries:
            cls = entry.get("classification", "")
            if cls in ("regression", "drift"):
                tid = entry.get("task_id", "")
                if tid:
                    nominated.append(tid)
        return nominated


# ---------------------------------------------------------------------------
# Section D — SHA256 hashing + audit log
# ---------------------------------------------------------------------------


def compute_tasklist_sha256(path: Path) -> str:
    """Return the SHA256 hex digest of the file at ``path``."""
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return ""


def write_recovery_audit_log(audit_log_path: Path, event: dict) -> None:
    """Append a JSONL event entry to the shared recovery audit log.

    The audit log lives at ``<results_dir>/recovery-audit.log`` (TDD T4
    line 66) and is shared across all recovery verbs (rerun-tasks today,
    sprint repair in v4.4.0). Append-mode write so concurrent recovery
    operations contribute entries without race-clobbering.
    """
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    try:
        audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        with audit_log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except OSError:
        return


# ---------------------------------------------------------------------------
# Section E — Lock file helpers (concurrent-recovery protection)
# ---------------------------------------------------------------------------


def _read_proc_starttime(pid: int) -> Optional[str]:
    """Return field 22 (``starttime``) from ``/proc/<pid>/stat`` as a string.

    The starttime (process start time in clock ticks since boot) uniquely
    identifies a process across PID reuse. Returns ``None`` when ``/proc`` is
    absent (non-Linux / minimal container), the file cannot be read, or the
    field cannot be parsed — callers then degrade to PID-only liveness.

    The second field (``comm``) is wrapped in parentheses and may itself
    contain spaces and parentheses, so we split on the substring AFTER the
    LAST ``)`` and index field 22 (1-based) = index 19 of the post-comm tokens
    (fields 3..N map to post-comm indices 0..N-3; field 22 → index 19).
    """
    try:
        with open(f"/proc/{pid}/stat", encoding="utf-8") as f:
            data = f.read()
        after_comm = data[data.rindex(")") + 1 :]
        fields = after_comm.split()
        return fields[19]
    except (OSError, ValueError, IndexError):
        return None


def _pid_is_alive(pid: int, recorded_starttime: Optional[str]) -> bool:
    """Return whether ``pid`` is a live process, mitigating PID-reuse.

    ``pid <= 0`` is never alive. Otherwise ``os.kill(pid, 0)`` probes the
    process: ``ProcessLookupError`` ⇒ dead, ``PermissionError`` ⇒ alive (PID
    exists, owned by another user). When the probe says alive AND
    ``recorded_starttime`` is not ``None``, the current
    ``/proc/<pid>/stat`` starttime is compared against the recorded value;
    a mismatch means the PID was recycled into a different process, so the
    original holder is treated as dead (its stale lock is reclaimable).
    """
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        # PID exists, owned by another user — treat as alive.
        return True
    if recorded_starttime is not None:
        current = _read_proc_starttime(pid)
        if current is not None and current != recorded_starttime:
            # Recycled PID — the recorded holder is gone.
            return False
    return True


def _register_lock_release(lock_path: Path) -> None:
    """Register atexit + SIGINT/SIGTERM release for ``lock_path``.

    The ``atexit`` handler covers normal-return and unhandled-exception
    paths. Signal handlers for BOTH SIGINT and SIGTERM release the lock and
    then CHAIN to the previous handler (release-and-return semantics) so the
    sprint's own ``SignalHandler`` is not clobbered and the test process is
    not killed. Registration is guarded so it degrades silently in non-main
    threads / restricted test contexts where signal handling is unavailable.
    """
    import atexit

    atexit.register(lambda: release_recovery_lock(lock_path))

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            prev = signal.getsignal(sig)

            def _handler(signum, frame, _prev=prev, _lp=lock_path):
                release_recovery_lock(_lp)
                if callable(_prev):
                    _prev(signum, frame)

            signal.signal(sig, _handler)
        except (ValueError, OSError):
            # signal.signal()/getsignal() may fail in non-main threads or in
            # test contexts where signal handling is restricted. atexit still
            # covers normal exit.
            pass


def _acquire_pid_lock(
    lock_path: Path,
    *,
    force: bool = False,
    payload_extra: Optional[dict] = None,
    held_message=None,
) -> Path:
    """Atomically acquire an exclusive PID lock at ``lock_path``.

    Shared hardened core for both the phase recovery lock and the
    release-scoped run lock. Behavior:

    - **Atomic acquisition (R1.1):** ``os.open(O_CREAT|O_EXCL|O_WRONLY)``
      eliminates the exists-then-write TOCTOU window. On ``FileExistsError``
      the prior holder is read (corrupt/partial JSON ⇒ treated as dead),
      liveness is tested via ``_pid_is_alive`` (PID-reuse aware, R3), a LIVE
      holder raises ``click.ClickException`` unless ``force=True``, and an
      otherwise dead/forced lock is unlinked (tolerating a concurrent
      reclaimer's ``FileNotFoundError``) and the exclusive create is RETRIED,
      bounded to 3 attempts to prevent reclaimer livelock.
    - **Payload:** ``{"pid", "starttime", "timestamp"}`` merged with
      ``payload_extra``. ``starttime`` mitigates PID reuse (R3).
    - **Release registration (R1.2):** atexit + SIGINT/SIGTERM (see
      ``_register_lock_release``).

    ``held_message`` is an optional ``callable(prior_pid, prior_ts) -> str``
    producing the live-holder ``ClickException`` message; when ``None`` the
    byte-exact phase-lock message is used.
    """
    # Local import: click is a CLI dependency; lazy-import keeps recovery.py
    # importable by tests that don't need the CLI shim.
    import click

    payload = {
        "pid": os.getpid(),
        "starttime": _read_proc_starttime(os.getpid()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if payload_extra:
        payload.update(payload_extra)
    encoded = json.dumps(payload).encode("utf-8")

    max_attempts = 3
    for _attempt in range(max_attempts):
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            # A lock already exists — inspect the prior holder.
            try:
                prior = json.loads(lock_path.read_text(encoding="utf-8"))
                prior_pid = int(prior.get("pid", 0))
                prior_ts = prior.get("timestamp", "")
                prior_starttime = prior.get("starttime")
            except (OSError, ValueError, json.JSONDecodeError):
                # Corrupt/partial/torn lockfile — treat holder as dead.
                prior_pid = 0
                prior_ts = ""
                prior_starttime = None

            if not force and _pid_is_alive(prior_pid, prior_starttime):
                if held_message is not None:
                    msg = held_message(prior_pid, prior_ts)
                else:
                    msg = (
                        f"Recovery lock held by PID {prior_pid} since {prior_ts}. "
                        f"Remove `{lock_path}` if the prior process crashed."
                    )
                raise click.ClickException(msg)

            # Stale (or force-reclaimed) lock — unlink and retry the
            # exclusive create. Tolerate a concurrent reclaimer winning the
            # unlink race (FileNotFoundError).
            try:
                lock_path.unlink()
            except FileNotFoundError:
                pass
            except OSError:
                pass
            continue
        else:
            os.write(fd, encoded)
            os.close(fd)
            _register_lock_release(lock_path)
            return lock_path

    # Exhausted bounded retries — a live holder almost certainly exists.
    raise click.ClickException(
        f"Could not acquire lock `{lock_path}` after {max_attempts} attempts; "
        f"a live run may exist."
    )


def acquire_recovery_lock(results_dir: Path, phase: int) -> Path:
    """Create an exclusive recovery lock for ``phase`` under ``results_dir``.

    Lock file: ``<results_dir>/.recovery-locks/phase-{phase}.lock``. Contents
    are JSON ``{"pid": <os.getpid()>, "timestamp": <utc isoformat>}``. If a
    lock exists for a live PID, raises ``click.ClickException``. If the
    holding PID is dead (``os.kill(pid, 0)`` → ProcessLookupError), the
    stale lock is reclaimed. atexit + SIGTERM handlers auto-release the
    lock on normal exit and signal-driven termination (TDD T8.5).
    """
    locks_dir = results_dir / ".recovery-locks"
    locks_dir.mkdir(parents=True, exist_ok=True)
    lock_path = locks_dir / f"phase-{phase}.lock"
    return _acquire_pid_lock(lock_path)


def release_recovery_lock(lock_path: Path) -> None:
    """Idempotently unlink ``lock_path``; safe to call from atexit or signals."""
    try:
        lock_path.unlink()
    except OSError:
        pass


def acquire_run_lock(results_dir: Path, *, force: bool = False) -> Path:
    """Acquire the release-scoped run lock under ``results_dir``.

    Lock file: ``<results_dir>/.recovery-locks/run.lock`` (same directory as
    the phase locks, distinct filename so the two lock families never
    collide). JSON payload ``{"pid", "starttime", "timestamp", "hostname"}``.

    A LIVE holder with ``force=False`` raises ``click.ClickException`` naming
    the holder PID + timestamp + the ``--ignore-run-lock`` remediation hint
    (R2.2). A dead-PID stale lock — the SIGKILL/SIGSEGV safety net, since
    atexit/signal handlers do not run on those — is reclaimed (R2.3).
    ``force=True`` reclaims even a live holder.
    """
    locks_dir = results_dir / ".recovery-locks"
    locks_dir.mkdir(parents=True, exist_ok=True)
    lock_path = locks_dir / "run.lock"

    def _held_message(prior_pid, prior_ts):
        return (
            f"Sprint run-lock held by PID {prior_pid} since {prior_ts}. "
            f"Re-run with --ignore-run-lock if that process crashed."
        )

    return _acquire_pid_lock(
        lock_path,
        force=force,
        payload_extra={"hostname": socket.gethostname()},
        held_message=_held_message,
    )


def release_run_lock(path: Path) -> None:
    """Idempotently unlink the run lock at ``path``.

    Best-effort: safe to call from atexit, signal handlers, or directly, and
    safe to call twice (double-release is a no-op).
    """
    try:
        path.unlink()
    except OSError:
        pass


def retry_count_for_task(phase_result: PhaseResult, task_id: str) -> int:
    """Return the number of prior recovery bundles that re-ran ``task_id``.

    Tolerates both dataclass (RecoveryBundleRef) and dict entries in the
    bare-typed ``recovery_history`` field. Per TDD T8.2 the rerun engine
    caps retries at 3 — callers compare this count to that threshold.
    """
    count = 0
    history = getattr(phase_result, "recovery_history", []) or []
    for entry in history:
        affected: list = []
        if hasattr(entry, "affected_tasks"):
            affected = list(getattr(entry, "affected_tasks", []) or [])
        elif isinstance(entry, dict):
            affected = list(entry.get("affected_tasks", []) or [])
        if task_id in affected:
            count += 1
    return count


# ---------------------------------------------------------------------------
# Section F — Generic merge engine (verb-agnostic recovery vehicle)
# ---------------------------------------------------------------------------


def merge_recovery_bundle(
    bundle: RecoveryBundle,
    source_index: Path,
    *,
    release_dir: Optional[Path] = None,
    expected_deliverables: Optional[dict[str, list[Path]]] = None,
) -> None:
    """Apply a RecoveryBundle's rerun artifacts back into the canonical results.

    Canonical merge sequence (TDD §T5, lines 86-99): Steps 1-7 reconcile the
    ``results/phase-N-*`` file families, plus an inserted Step 3.5 that
    relocates the rerun's TASKLIST_ROOT deliverable trees (``artifacts/``,
    ``evidence/``, ``checkpoints/``) from the bundle root back to the canonical
    TASKLIST_ROOT and fails loudly when a declared deliverable does not land.
    Each step emits a ``debug_log`` trace event tagged with ``bundle_id`` for
    audit traceability. All file writes use the atomic tmp + replace pattern
    (researcher 2 §1.6) so partial writes cannot corrupt prior state.

    Called by ``rerun_tasks.run_rerun_tasks`` today; v4.4.0 will add
    ``sprint repair from-reflect`` as a second consumer. The function is
    verb-agnostic — any caller that builds a RecoveryBundle can merge.

    Args:
        bundle: RecoveryBundle authored by the rerun verb. Mutated in place:
            ``status`` is set to SUCCESS or PARTIAL, ``end_tasklist_sha256``
            is populated.
        source_index: Path to the canonical tasklist-index.md. Used to resolve
            the release directory (and from it the canonical ``results/`` dir
            and ``execution-log.jsonl``) when ``release_dir`` is not supplied.
        release_dir: Canonical release directory (``SprintConfig.release_dir``).
            When provided by the caller (Phase 3 ``run_rerun_tasks`` holds the
            resolved ``SprintConfig``), it is authoritative. When omitted, it is
            resolved from ``source_index`` via the same
            ``config._resolve_release_dir`` logic the loader uses — NOT a naive
            ``source_index.parent``, which is wrong when the index lives under a
            ``tasklist/`` subdirectory.
        expected_deliverables: Optional map of ``task_id`` -> declared
            deliverable Paths for the affected tasks (computed by the caller via
            ``rerun_tasks._declared_deliverables``; default ``None`` preserves
            the verb-agnostic behavior). When supplied, Step 3.5 verifies each
            declared deliverable landed at its mirrored canonical destination and
            appends a ``deliverable-not-landed:<task>:<rel>`` entry to the
            failure list (downgrading status to PARTIAL) for any that did not —
            so a stranded deliverable can never be silently reported as SUCCESS.
    """
    import shutil

    if release_dir is None:
        # Local import: config imports models/recovery indirectly; keep at
        # function scope to avoid module-import cycles.
        from .config import _resolve_release_dir

        release_dir = _resolve_release_dir(source_index)

    # Canonical layout (SprintConfig): results live in <release_dir>/results,
    # the execution log lives in <release_dir>/execution-log.jsonl (a SIBLING
    # of results/, not a child).
    results_dir = release_dir / "results"
    execlog_path = release_dir / "execution-log.jsonl"
    audit_log = results_dir / "recovery-audit.log"
    phase = bundle.affected_phase
    bundle_id = bundle.bundle_id

    failures: list[str] = []

    # Step 1 — Rename original task transcripts; copy rerun transcripts to canonical paths.
    debug_log(
        _recovery_logger,
        "merge_step_1_rename_transcripts",
        bundle_id=bundle_id,
        affected_tasks=len(bundle.affected_tasks),
    )
    for task_id in bundle.affected_tasks:
        canonical = results_dir / f"phase-{phase}-task-{task_id}-output.txt"
        if canonical.exists():
            try:
                orig_ts = int(canonical.stat().st_mtime)
                preserved = results_dir / (
                    f"phase-{phase}-task-{task_id}-output.failed-{orig_ts}.txt"
                )
                canonical.rename(preserved)
                bundle.artifacts_replaced[canonical] = preserved
            except OSError as exc:
                failures.append(f"rename-output:{task_id}:{exc}")
        for produced in bundle.artifacts_produced:
            if produced.name == canonical.name:
                try:
                    shutil.copy2(produced, canonical)
                except OSError as exc:
                    failures.append(f"copy-output:{task_id}:{exc}")

    # Step 2 — Same rename-and-replace for checkpoint reports (phase-N-cp*.md).
    debug_log(_recovery_logger, "merge_step_2_rename_checkpoints", bundle_id=bundle_id)
    for cp_canonical in results_dir.glob(f"phase-{phase}-cp*.md"):
        # Only replace checkpoints whose task ID is in affected_tasks.
        if not any(tid in cp_canonical.name for tid in bundle.affected_tasks):
            continue
        try:
            orig_ts = int(cp_canonical.stat().st_mtime)
            preserved = cp_canonical.with_name(
                cp_canonical.stem + f".failed-{orig_ts}" + cp_canonical.suffix
            )
            cp_canonical.rename(preserved)
            bundle.artifacts_replaced[cp_canonical] = preserved
        except OSError as exc:
            failures.append(f"rename-checkpoint:{cp_canonical.name}:{exc}")
        for produced in bundle.artifacts_produced:
            if produced.name == cp_canonical.name:
                try:
                    shutil.copy2(produced, cp_canonical)
                except OSError as exc:
                    failures.append(f"copy-checkpoint:{cp_canonical.name}:{exc}")

    # Step 3 — Same for -errors.txt siblings.
    debug_log(_recovery_logger, "merge_step_3_rename_errors", bundle_id=bundle_id)
    for task_id in bundle.affected_tasks:
        err_canonical = results_dir / f"phase-{phase}-task-{task_id}-errors.txt"
        if err_canonical.exists():
            try:
                orig_ts = int(err_canonical.stat().st_mtime)
                preserved = results_dir / (
                    f"phase-{phase}-task-{task_id}-errors.failed-{orig_ts}.txt"
                )
                err_canonical.rename(preserved)
                bundle.artifacts_replaced[err_canonical] = preserved
            except OSError as exc:
                failures.append(f"rename-errors:{task_id}:{exc}")
        for produced in bundle.artifacts_produced:
            if produced.name == err_canonical.name:
                try:
                    shutil.copy2(produced, err_canonical)
                except OSError as exc:
                    failures.append(f"copy-errors:{task_id}:{exc}")

    # Step 3.5 — relocate + verify TASKLIST_ROOT deliverable trees.
    # Rerun agents write declared deliverable trees (artifacts/, evidence/,
    # checkpoints/) into the bundle ROOT because the rerun sub-index pins
    # TASKLIST_ROOT to the bundle. Steps 1-3 only reconcile the
    # results/phase-N-* file families, so without this step those trees stay
    # stranded inside the bundle while the merge still reports SUCCESS (silent
    # data loss — the Defect-1 root cause). This step copies each tree back to
    # the canonical TASKLIST_ROOT (source_index.parent) and, when the caller
    # declares expected deliverables, fails loudly (appends to ``failures``,
    # downgrading status to PARTIAL via the flip below) for any declared tree
    # that does not land. It NEVER auto-PASSes a stranded deliverable.
    debug_log(
        _recovery_logger,
        "merge_step_3_5_relocate_deliverables",
        bundle_id=bundle_id,
    )
    canonical_root = source_index.parent
    bundle_root = (
        bundle.artifacts_produced[0].parent.parent
        if bundle.artifacts_produced
        else None
    )
    if bundle_root is not None:
        for subtree in ("artifacts", "evidence", "checkpoints"):
            src_tree = bundle_root / subtree
            if not src_tree.is_dir():
                continue
            for produced_file in src_tree.rglob("*"):
                if not produced_file.is_file():
                    continue
                rel = produced_file.relative_to(bundle_root)
                dest = canonical_root / rel
                try:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    # Preserve any clobbered canonical file as .failed-<mtime>
                    # (mirrors the Step 1/2/3 clobber-preserve idiom).
                    if dest.exists():
                        orig_ts = int(dest.stat().st_mtime)
                        preserved = dest.with_name(
                            dest.stem + f".failed-{orig_ts}" + dest.suffix
                        )
                        dest.rename(preserved)
                        bundle.artifacts_replaced[dest] = preserved
                    # Per-file atomic copy (mirrors the tmp + replace idiom).
                    tmp = dest.with_suffix(dest.suffix + ".tmp")
                    shutil.copy2(produced_file, tmp)
                    tmp.replace(dest)
                except OSError as exc:
                    failures.append(f"relocate-deliverable:{subtree}:{rel}:{exc}")

    # Verify each declared deliverable landed at its mirrored canonical
    # destination; a missing/empty tree appends a deliverable-not-landed
    # failure so the status flip downgrades to PARTIAL (never silent SUCCESS).
    if expected_deliverables is not None:
        for task_id, declared_paths in expected_deliverables.items():
            for declared in declared_paths:
                # Map the declared path onto its mirrored canonical destination
                # by its subtree segment; declared paths resolve against cwd,
                # which need not equal canonical_root, so check the mirror.
                parts = declared.parts
                rel_dest: Path = Path(declared.name)
                for idx, part in enumerate(parts):
                    if part in ("artifacts", "evidence", "checkpoints"):
                        rel_dest = Path(*parts[idx:])
                        break
                canonical_dest = canonical_root / rel_dest
                # Verify the CANONICAL mirror ONLY. A cwd-resolved declared path
                # that is NOT the canonical destination must never count as
                # landed — otherwise a stale/pre-existing non-canonical file
                # masks a deliverable that relocation never landed in canonical
                # (the DEV-3 silent-SUCCESS hole).
                landed = canonical_dest.is_file() and canonical_dest.stat().st_size > 0
                if not landed:
                    failures.append(f"deliverable-not-landed:{task_id}:{rel_dest}")

    # Step 4 — Write phase-N-rerun-manifest.json atomically.
    debug_log(_recovery_logger, "merge_step_4_write_manifest", bundle_id=bundle_id)
    manifest_path = results_dir / f"phase-{phase}-rerun-manifest.json"
    manifest = {
        "bundle_id": bundle_id,
        "verb": bundle.verb,
        "affected_phase": phase,
        "affected_tasks": list(bundle.affected_tasks),
        "rerun_attempt": bundle.rerun_attempt,
        "source_tasklist_sha256": bundle.source_tasklist_sha256,
        "artifacts_produced": [str(p) for p in bundle.artifacts_produced],
        "artifacts_replaced": {
            str(k): str(v) for k, v in bundle.artifacts_replaced.items()
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        tmp = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
        tmp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        tmp.replace(manifest_path)
    except OSError as exc:
        failures.append(f"write-manifest:{exc}")

    # Step 5 — Append phase_rerun_start, task_rerun_complete×N, phase_rerun_complete to execution-log.jsonl.
    debug_log(_recovery_logger, "merge_step_5_emit_events", bundle_id=bundle_id)
    try:
        # Local import: logging_ may indirectly import from recovery's consumers (rerun_tasks)
        # → keep this at function scope to avoid module-import cycles.
        from .logging_ import SprintLogger  # noqa: F401

        execlog = execlog_path
        execlog.parent.mkdir(parents=True, exist_ok=True)
        with execlog.open("a", encoding="utf-8") as f:
            ts = datetime.now(timezone.utc).isoformat()
            f.write(
                json.dumps(
                    {
                        "event": "phase_rerun_start",
                        "timestamp": ts,
                        "phase": phase,
                        "bundle_id": bundle_id,
                        "affected_tasks": list(bundle.affected_tasks),
                    }
                )
                + "\n"
            )
            for task_id in bundle.affected_tasks:
                f.write(
                    json.dumps(
                        {
                            "event": "task_rerun_complete",
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "phase": phase,
                            "task_id": task_id,
                            "bundle_id": bundle_id,
                        }
                    )
                    + "\n"
                )
            f.write(
                json.dumps(
                    {
                        "event": "phase_rerun_complete",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "phase": phase,
                        "bundle_id": bundle_id,
                        "failures": failures,
                    }
                )
                + "\n"
            )
    except OSError as exc:
        failures.append(f"emit-events:{exc}")

    # Step 6 — Append phase_complete_superseded_by event (append-only, never rewrites prior phase_complete).
    debug_log(_recovery_logger, "merge_step_6_supersede_link", bundle_id=bundle_id)
    try:
        execlog = execlog_path
        bundle_dir = (
            bundle.artifacts_produced[0].parent
            if bundle.artifacts_produced
            else results_dir
        )
        with execlog.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "event": "phase_complete_superseded_by",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "phase": phase,
                        "bundle": str(bundle_dir),
                        "bundle_id": bundle_id,
                    }
                )
                + "\n"
            )
    except OSError as exc:
        failures.append(f"supersede-link:{exc}")

    # Step 7 — Rewrite phase-N-result.json atomically with updated task_results + recovery_history.
    debug_log(_recovery_logger, "merge_step_7_rewrite_result_json", bundle_id=bundle_id)
    result_json_path = results_dir / f"phase-{phase}-result.json"
    try:
        if result_json_path.exists():
            existing = json.loads(result_json_path.read_text(encoding="utf-8"))
        else:
            existing = {"phase": phase, "task_results": [], "recovery_history": []}

        # Splice new TaskResult dicts over prior entries for the affected task IDs.
        # The replacement results come from a `task-results.json` sidecar that
        # Phase 3's run_rerun_tasks writes into the bundle dir alongside the
        # rerun transcripts. The sidecar is the bundle's serialized rerun
        # PhaseResult.task_results.
        #
        # R-F3 (sc:reflect): when the sidecar is absent or unreadable, we MUST
        # NOT drop the affected tasks' prior result entries — silent removal is
        # data loss. Instead we PRESERVE the prior entries unchanged and record
        # a failure so the bundle status downgrades to PARTIAL and the operator
        # is alerted that result-json was not refreshed for the affected tasks.
        prior_results: list[dict] = existing.get("task_results", []) or []
        bundle_dir = (
            bundle.artifacts_produced[0].parent if bundle.artifacts_produced else None
        )
        new_results: list[dict] = []
        sidecar_ok = False
        if bundle_dir is not None:
            sidecar = bundle_dir / "task-results.json"
            if sidecar.exists():
                try:
                    new_results = json.loads(sidecar.read_text(encoding="utf-8"))
                    sidecar_ok = True
                except (OSError, json.JSONDecodeError) as exc:
                    failures.append(f"result-json-sidecar-unreadable:{exc}")

        if sidecar_ok:
            # Replace affected tasks' entries with the refreshed rerun results.
            keep: list[dict] = [
                r
                for r in prior_results
                if r.get("task", {}).get("task_id") not in bundle.affected_tasks
            ]
            existing["task_results"] = keep + new_results
        else:
            # No usable replacement — preserve ALL prior entries (including the
            # affected tasks) and flag the gap. Never silently drop.
            if bundle.affected_tasks:
                failures.append(
                    "result-json-not-refreshed:no task-results.json sidecar in bundle; "
                    f"prior entries preserved for {','.join(bundle.affected_tasks)}"
                )
            existing["task_results"] = prior_results

        # Append a RecoveryBundleRef for this merge.
        ref = {
            "bundle_id": bundle_id,
            "path": str(result_json_path.parent / f"recovery-bundle-{bundle_id}.json"),
            "status": (
                RecoveryStatus.PARTIAL.value
                if failures
                else RecoveryStatus.SUCCESS.value
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        existing.setdefault("recovery_history", []).append(ref)

        tmp = result_json_path.with_suffix(result_json_path.suffix + ".tmp")
        tmp.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
        tmp.replace(result_json_path)
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"rewrite-result-json:{exc}")

    # Finalize bundle status + audit log.
    bundle.status = RecoveryStatus.PARTIAL if failures else RecoveryStatus.SUCCESS
    bundle.end_tasklist_sha256 = compute_tasklist_sha256(source_index)
    write_recovery_audit_log(
        audit_log,
        {
            "event": "merge_recovery_bundle",
            "bundle_id": bundle_id,
            "affected_phase": phase,
            "affected_tasks": list(bundle.affected_tasks),
            "status": bundle.status.value,
            "failures": failures,
            "rerun_attempt": bundle.rerun_attempt,
        },
    )
