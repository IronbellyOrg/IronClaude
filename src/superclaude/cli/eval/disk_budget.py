"""NFR-PERF4 disk-budget poller (T03.19 / D-0060 / R-060).

Design-spec §4 (``--max-disk-mb``) and §13 (NFR-PERF4) require the
orchestrator to bound the cumulative artifact size under
``--output-dir`` during a run. The motivation is the R4 risk row in
design-spec §10: a fan-out of 15 concurrent HOMEs with PTY transcripts
can grow past several hundred megabytes on a slow eval; left unchecked,
that fills the developer host (or a CI runner with a tight disk quota)
and corrupts every neighbouring run. The orchestrator addresses this
by polling the run-directory size every five seconds and signalling a
"stop scheduling, drain in-flight, exit 2" breach when the configured
budget is exceeded.

This module implements the polling primitive. The integration with
:class:`RunOrchestrator` lives in ``orchestrator.py``; the CLI flag
(``--max-disk-mb``) is wired by the Phase 4 dispatcher per design-spec
§4. The poller is deliberately decoupled from both so it can be exercised
in isolation by the T03.19 fixture suite (``test_disk_budget.py``) and
re-used by any future component (eg. the doctor pre-flight) that needs
a cheap, side-effect-free disk gauge.

Public surface
==============

:class:`DiskBudgetPoller`
    Background-thread poller. Constructed with an output directory and a
    ``max_disk_mb`` budget; ``start()`` / ``stop()`` (or the context-
    manager form) drive the background thread. Exposes :meth:`is_breached`
    so the orchestrator can short-circuit its submission loop and
    :meth:`breach_detail` for the partial-summary payload.

:data:`DISK_BUDGET_EXCEEDED_EXIT_CODE`
    Process exit code emitted by the Phase 4 dispatcher when the poller
    has flagged a breach. ``2`` per design-spec §4 (harness error).

:data:`DISK_BUDGET_EXCEEDED_ARTIFACT_NAME`
    Filename of the side-car the poller writes inside the run directory
    on breach. The Reporter (COMP-008 / T03.13) surfaces this path under
    ``RunSummary.artifacts['disk_budget_exceeded']``; the filename is
    pinned here so consumers do not have to discover it by scan.

Breach semantics
================

When ``max_disk_mb > 0``:

* The poller measures cumulative size of the output directory tree every
  ``tick_sec`` seconds (default ``5.0``). The first tick fires *after*
  the initial sleep so an empty run directory does not get flagged on
  start-up.
* When measured usage exceeds ``max_disk_mb * 1024 * 1024`` bytes, the
  poller writes ``DISK_BUDGET_EXCEEDED_ARTIFACT_NAME`` into the output
  directory, sets its internal ``is_breached()`` flag, and exits the
  loop. The flag is one-shot — once set, the poller stays in the
  breached state for the rest of its lifetime.
* The orchestrator polls ``is_breached()`` between submissions; on a
  breach it stops scheduling new specs and synthesises a
  ``SKIPPED`` outcome (skip_reason ``"disk_budget_exceeded"``) for every
  unsubmitted spec. In-flight workers continue to completion — the
  poller never kills a thread or sends a signal.

When ``max_disk_mb == 0``:

* The poller is *disabled*. ``start()`` is a no-op, the background
  thread is never spawned, and :meth:`is_breached` always returns
  ``False``. The orchestrator behaves as if no poller were wired.
  Design-spec §4 documents ``--max-disk-mb 0`` as the "disable"
  invocation.

Thread safety
=============

The breach state is stored as a :class:`threading.Event`. Reading the
detail mapping after :meth:`is_breached` returns ``True`` is safe because
the detail is published *before* the event is set (release-then-set
ordering). The poller thread is the only writer of the detail; the
orchestrator (main) thread is the only reader. Both ends communicate
through the event without explicit locking.
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional

__all__ = [
    "DISK_BUDGET_EXCEEDED_ARTIFACT_NAME",
    "DISK_BUDGET_EXCEEDED_EXIT_CODE",
    "DISK_BUDGET_EXCEEDED_REASON",
    "DISK_BUDGET_RETENTION_ADVICE",
    "DEFAULT_DISK_BUDGET_MB",
    "DEFAULT_DISK_POLL_TICK_SEC",
    "DiskBudgetPoller",
]


# Process exit code returned by the Phase 4 CLI dispatcher when the
# poller has signalled a breach. Matches the design-spec §4 exit-code
# table: ``2`` = harness error. The disk-budget breach is a harness-
# enforced abort, not a per-eval failure, so it uses the same code as
# the loader / scratch-root / reporter-contract violations.
DISK_BUDGET_EXCEEDED_EXIT_CODE: int = 2

# Filename the poller writes when a breach is detected. Pinned here so
# the orchestrator, Reporter, and integration tests all reference one
# constant. ``.json`` because the payload is a structured
# :class:`BreachDetail` projection.
DISK_BUDGET_EXCEEDED_ARTIFACT_NAME: str = "disk_budget_exceeded.json"

# ``skip_reason`` token written into every synthesised SKIPPED outcome
# the orchestrator emits for unsubmitted specs after a breach. Stable
# value so the Reporter / CLI consumers can match on it.
DISK_BUDGET_EXCEEDED_REASON: str = "disk_budget_exceeded"

# Design-spec §4 default budget. The CLI flag default mirrors this so a
# bare ``superclaude eval run`` is bounded out of the box.
DEFAULT_DISK_BUDGET_MB: int = 1024

# Design-spec §13 polling cadence. Five seconds is a coarse-enough tick
# that the recursive ``stat()`` walk does not become a measurable share
# of runtime even for a 15-eval suite emitting transcripts at a few MB/s.
DEFAULT_DISK_POLL_TICK_SEC: float = 5.0

# OPS-003 retention-policy advice rendered to stderr by the Phase 4 CLI
# dispatcher immediately before the disk-budget breach exit. Pinned as a
# module constant so ``docs/eval/retention.md`` and the CLI stderr text
# agree by construction: the policy doc quotes this string verbatim, and
# ``tests/cli/eval/test_retention_policy.py`` asserts both surfaces carry
# the same bytes. Drift between the doc and CLI surface is therefore a
# test failure rather than a silent operator confusion.
#
# Three sentences, each load-bearing:
#   1. Name the breach explicitly so operators reading the stderr tail in
#      CI logs can pivot to the policy doc.
#   2. Tell the operator what was preserved (the run dir + summaries +
#      per-eval artifacts for finished evals + the
#      ``disk_budget_exceeded.json`` side-car) so they do not assume the
#      run was wiped.
#   3. Tell the operator the two retention knobs (``--keep-home`` and
#      ``--max-disk-mb``) and where the full policy lives, so the next
#      run can be configured without re-reading the source.
DISK_BUDGET_RETENTION_ADVICE: str = (
    "disk-budget exceeded: the run was aborted to protect the host filesystem. "
    "The run directory, summary.{md,json}, junit.xml, per-eval artifacts for "
    "finished evals, and disk_budget_exceeded.json side-car are retained for "
    "forensic inspection. "
    "Raise --max-disk-mb (or set to 0 to disable the budget) and/or pass "
    "--keep-home False on the next invocation; see docs/eval/retention.md "
    "for the full OPS-003 retention policy."
)


_BYTES_PER_MB: int = 1024 * 1024


@dataclass(frozen=True)
class BreachDetail:
    """Side-car payload describing a disk-budget breach.

    Serialised verbatim into :data:`DISK_BUDGET_EXCEEDED_ARTIFACT_NAME`
    by the poller. The Reporter surfaces this dict back through
    ``RunSummary.artifacts['disk_budget_exceeded']`` so reviewers can
    diagnose "why did the run exit 2" without re-running the poller.

    Attributes
    ----------
    reason:
        Always :data:`DISK_BUDGET_EXCEEDED_REASON`. Pinned so consumers
        can match on the constant token without parsing structure.
    output_dir:
        Absolute path of the directory the poller was watching, as a
        string (paths do not JSON-serialise without a converter).
    usage_bytes:
        Measured cumulative size of the directory tree at the breach
        tick. ``int`` so the value round-trips through JSON losslessly.
    budget_bytes:
        Effective budget in bytes (``max_disk_mb * 1024 * 1024``).
    max_disk_mb:
        Original budget the operator configured, in megabytes. Stored
        alongside ``budget_bytes`` so the side-car is readable without a
        mental conversion.
    ticked_at:
        ISO-8601 timestamp of the breach tick. Stamped via
        :func:`time.gmtime` + :func:`time.strftime` so the value is
        timezone-stable (UTC ``Z``).
    """

    reason: str
    output_dir: str
    usage_bytes: int
    budget_bytes: int
    max_disk_mb: int
    ticked_at: str

    def to_dict(self) -> dict:
        """Return a JSON-serialisable dict in field-declared order."""
        return {
            "reason": self.reason,
            "output_dir": self.output_dir,
            "usage_bytes": self.usage_bytes,
            "budget_bytes": self.budget_bytes,
            "max_disk_mb": self.max_disk_mb,
            "ticked_at": self.ticked_at,
        }


class DiskBudgetPoller:
    """Background-thread poller enforcing the NFR-PERF4 disk budget.

    Parameters
    ----------
    output_dir:
        Directory whose recursive size is summed every tick. Created if
        missing only when ``ensure_output_dir=True``; otherwise the
        first tick on a non-existent directory measures ``0`` bytes.
    max_disk_mb:
        Budget in megabytes. ``0`` disables the poller entirely (see
        module docstring). Negative values raise :class:`ValueError`.
    tick_sec:
        Seconds between size measurements. Defaults to
        :data:`DEFAULT_DISK_POLL_TICK_SEC` (5 s). Tests pass a small
        value (eg. 0.05) to keep the suite fast.
    artifact_name:
        Filename of the breach side-car. Defaults to
        :data:`DISK_BUDGET_EXCEEDED_ARTIFACT_NAME`. Tests substitute a
        unique name when several pollers share a directory.
    clock:
        Optional ``() -> str`` returning the ``ticked_at`` ISO-8601
        timestamp. Tests inject a deterministic clock; the default
        formatter uses :func:`time.gmtime` so production output is
        timezone-stable.

    Notes
    -----
    The recursive size walk uses :meth:`pathlib.Path.rglob` and
    :meth:`pathlib.Path.stat` with ``follow_symlinks=False`` so the
    poller cannot be tricked into double-counting via a symlink into a
    sibling tree. Files that disappear between the directory walk and
    the ``stat()`` call (eg. an in-flight runner cleaning up its scratch
    HOME) are silently ignored — a transient OS error must not crash the
    poller thread.
    """

    DEFAULT_TICK_SEC = DEFAULT_DISK_POLL_TICK_SEC
    DEFAULT_MAX_DISK_MB = DEFAULT_DISK_BUDGET_MB
    ARTIFACT_NAME = DISK_BUDGET_EXCEEDED_ARTIFACT_NAME
    BREACH_REASON = DISK_BUDGET_EXCEEDED_REASON

    def __init__(
        self,
        output_dir: Path,
        *,
        max_disk_mb: int = DEFAULT_DISK_BUDGET_MB,
        tick_sec: float = DEFAULT_DISK_POLL_TICK_SEC,
        artifact_name: str = DISK_BUDGET_EXCEEDED_ARTIFACT_NAME,
        ensure_output_dir: bool = False,
        clock: Optional["callable[[], str]"] = None,
    ) -> None:
        if not isinstance(max_disk_mb, int) or isinstance(max_disk_mb, bool):
            raise TypeError(
                f"max_disk_mb must be int; got {type(max_disk_mb).__name__}"
            )
        if max_disk_mb < 0:
            raise ValueError(
                f"max_disk_mb must be >= 0; got {max_disk_mb} "
                "(use 0 to disable the budget)"
            )
        if tick_sec <= 0:
            raise ValueError(f"tick_sec must be > 0; got {tick_sec}")
        if not artifact_name:
            raise ValueError("artifact_name must be non-empty")

        self._output_dir = Path(output_dir)
        if ensure_output_dir:
            self._output_dir.mkdir(parents=True, exist_ok=True)

        self._max_disk_mb = int(max_disk_mb)
        self._budget_bytes = int(max_disk_mb) * _BYTES_PER_MB
        self._tick_sec = float(tick_sec)
        self._artifact_name = artifact_name
        self._clock = clock or _default_iso_clock

        self._stop_event = threading.Event()
        self._breach_event = threading.Event()
        self._detail: Optional[BreachDetail] = None
        self._artifact_path: Optional[Path] = None
        self._thread: Optional[threading.Thread] = None
        self._lifecycle_lock = threading.Lock()

    # ------------------------------------------------------------------
    # Read-only inspection surface
    # ------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """``True`` when the poller will actually spawn a thread."""
        return self._max_disk_mb > 0

    @property
    def max_disk_mb(self) -> int:
        return self._max_disk_mb

    @property
    def budget_bytes(self) -> int:
        return self._budget_bytes

    @property
    def tick_sec(self) -> float:
        return self._tick_sec

    @property
    def output_dir(self) -> Path:
        return self._output_dir

    @property
    def artifact_name(self) -> str:
        return self._artifact_name

    def is_breached(self) -> bool:
        """``True`` once a breach has been recorded.

        One-shot — once the flag flips it never resets for the lifetime
        of the poller. The orchestrator polls this between submissions
        to decide whether to keep scheduling.
        """
        return self._breach_event.is_set()

    def breach_detail(self) -> Optional[Mapping[str, object]]:
        """Return the breach payload as a plain dict, or ``None``.

        The mapping mirrors :class:`BreachDetail.to_dict`. Returns
        ``None`` until :meth:`is_breached` reports ``True``.
        """
        detail = self._detail
        if detail is None:
            return None
        return detail.to_dict()

    def artifact_path(self) -> Optional[Path]:
        """Path of the side-car file the poller wrote, or ``None``.

        Equal to ``output_dir / artifact_name`` once a breach has been
        recorded; ``None`` while the poller is healthy.
        """
        return self._artifact_path

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Spawn the background polling thread.

        No-op when :attr:`enabled` is ``False`` (``max_disk_mb=0``) or
        when the thread is already running. Idempotent so the
        orchestrator can call :meth:`start` unconditionally without
        guarding the disabled case.
        """
        with self._lifecycle_lock:
            if not self.enabled:
                return
            if self._thread is not None and self._thread.is_alive():
                return
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._poll_loop,
                name=f"cliEval-disk-budget-{self._max_disk_mb}MB",
                daemon=True,
            )
            self._thread.start()

    def stop(self, *, timeout: Optional[float] = None) -> None:
        """Signal the background thread to exit and join it.

        ``timeout`` is forwarded to :meth:`threading.Thread.join`. The
        method is idempotent and safe to call from any thread; signal-
        handler installers MAY call it from the main thread without
        knowing whether the poller was ever started.
        """
        with self._lifecycle_lock:
            thread = self._thread
            self._stop_event.set()
        if thread is not None:
            thread.join(timeout=timeout)

    def __enter__(self) -> "DiskBudgetPoller":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()

    # ------------------------------------------------------------------
    # Polling internals
    # ------------------------------------------------------------------

    def _poll_loop(self) -> None:
        """Tick-driven measurement loop.

        Uses :meth:`threading.Event.wait` rather than :func:`time.sleep`
        so :meth:`stop` can shortcut the next tick immediately — the
        orchestrator does not want to wait up to ``tick_sec`` seconds
        for the poller to notice it is being shut down.
        """
        while not self._stop_event.wait(self._tick_sec):
            usage_bytes = self._compute_usage()
            if usage_bytes > self._budget_bytes:
                self._record_breach(usage_bytes)
                return

    def _compute_usage(self) -> int:
        """Sum every regular file under ``output_dir`` non-recursively-of-symlinks.

        Returns ``0`` when the directory does not exist yet; lets the
        poller run before the orchestrator has created its run
        directory without raising. Per-file ``OSError`` is swallowed so
        a vanishing in-flight scratch file does not crash the poller.
        """
        root = self._output_dir
        if not root.is_dir():
            return 0
        total = 0
        # ``rglob('*')`` returns every entry including directories and
        # symlinks. We only count regular files (``is_file()`` returns
        # ``False`` for symlinks to files thanks to ``follow_symlinks``
        # behaviour of the underlying ``stat`` — but we also guard with
        # ``is_symlink()`` to be explicit about the policy).
        for entry in root.rglob("*"):
            if entry.is_symlink():
                continue
            try:
                if not entry.is_file():
                    continue
                total += entry.stat().st_size
            except (OSError, FileNotFoundError):
                # Transient: file was reaped between ``rglob`` and
                # ``stat``. Skip — the next tick will catch any
                # persistent growth.
                continue
        return total

    def _record_breach(self, usage_bytes: int) -> None:
        """Persist the side-car and flip the breach flag.

        The detail is built *before* the side-car is written so a
        partial-write failure (eg. directory was deleted out from under
        us) still leaves a valid in-memory payload for the Reporter.
        The breach flag is set *after* the detail is published so any
        consumer that reads :meth:`breach_detail` after observing
        :meth:`is_breached` ``True`` is guaranteed a non-``None``
        return.
        """
        detail = BreachDetail(
            reason=self.BREACH_REASON,
            output_dir=str(self._output_dir),
            usage_bytes=int(usage_bytes),
            budget_bytes=self._budget_bytes,
            max_disk_mb=self._max_disk_mb,
            ticked_at=self._clock(),
        )
        artifact_path = self._output_dir / self._artifact_name
        try:
            self._output_dir.mkdir(parents=True, exist_ok=True)
            artifact_path.write_text(
                json.dumps(detail.to_dict(), indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        except OSError:
            # Filesystem unavailable — record the breach in memory only
            # so the orchestrator still observes the flag. The side-car
            # absence is a known degraded mode documented in the spec.
            artifact_path = None

        # Publish detail before flipping the flag (release-then-set
        # ordering — see module docstring).
        self._detail = detail
        self._artifact_path = artifact_path
        self._breach_event.set()


def _default_iso_clock() -> str:
    """Return the current UTC time as an ISO-8601 ``Z`` string.

    Centralised so :class:`DiskBudgetPoller` and the side-car payload
    use a single timestamp format. Tests inject a deterministic clock
    via the constructor so we never have to mock ``time``.
    """
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
