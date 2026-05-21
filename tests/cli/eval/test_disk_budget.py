"""Tests for the NFR-PERF4 disk-budget poller (T03.19 / D-0060 / R-060).

The poller is exercised both in isolation (as a standalone
:class:`DiskBudgetPoller`) and through the
:class:`RunOrchestrator` integration that the task acceptance criteria
pin:

* Default budget 1024 MB and default 5-second tick cadence.
* ``--max-disk-mb 0`` disables the poller entirely (no thread, no
  breach).
* When measured usage exceeds ``max_disk_mb`` the poller writes
  ``disk_budget_exceeded.json`` into the run directory and flips
  :meth:`DiskBudgetPoller.is_breached` to ``True`` permanently.
* The orchestrator stops scheduling new specs after the breach but lets
  in-flight workers complete; unsubmitted specs receive a synthesised
  ``SKIPPED`` outcome with ``skip_reason == "disk_budget_exceeded"``.
* Constructor validation rejects negative budgets, non-int budgets, and
  non-positive tick cadences.

A small ``tick_sec`` (e.g. 0.05) and a kilobyte-scale budget are used to
keep the suite under a second — the production cadence/budget are
exercised separately via the constants the poller publishes.
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import pytest

from superclaude.cli.eval.disk_budget import (
    DEFAULT_DISK_BUDGET_MB,
    DEFAULT_DISK_POLL_TICK_SEC,
    DISK_BUDGET_EXCEEDED_ARTIFACT_NAME,
    DISK_BUDGET_EXCEEDED_EXIT_CODE,
    DISK_BUDGET_EXCEEDED_REASON,
    BreachDetail,
    DiskBudgetPoller,
)
from superclaude.cli.eval.models import EvalOutcome, EvalSpec
from superclaude.cli.eval.orchestrator import RunOrchestrator

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _spec(eval_id: str, title: str = "") -> EvalSpec:
    return EvalSpec(id=eval_id, title=title or eval_id)


def _passing_outcome(spec: EvalSpec) -> EvalOutcome:
    return EvalOutcome(
        eval_id=spec.id,
        title=spec.title,
        status="PASS",
        duration_sec=0.0,
        expects=(),
        skip_reason=None,
        skip_flag_triggered=None,
        artifacts={},
        error_class=None,
    )


def _write_bytes(path: Path, size_bytes: int) -> None:
    """Create ``path`` with exactly ``size_bytes`` bytes of payload."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # ``b"\0"`` keeps the file dense and predictable — sparse files
    # would understate the budget under ``stat().st_size``, which is
    # what the poller measures.
    with open(path, "wb") as handle:
        handle.write(b"\0" * size_bytes)


def _wait_for_breach(
    poller: DiskBudgetPoller, *, timeout: float = 2.0
) -> bool:
    """Block until ``poller.is_breached()`` flips or ``timeout`` elapses."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if poller.is_breached():
            return True
        time.sleep(0.01)
    return False


# ---------------------------------------------------------------------------
# Public constants — pinned by the design-spec / tasklist
# ---------------------------------------------------------------------------


class TestPublicConstants:
    def test_default_budget_is_1024_mb(self) -> None:
        """Design-spec §4: ``--max-disk-mb`` defaults to 1024."""
        assert DEFAULT_DISK_BUDGET_MB == 1024

    def test_default_tick_is_5_seconds(self) -> None:
        """Design-spec §13 NFR-PERF4: poll cadence is 5 s."""
        assert DEFAULT_DISK_POLL_TICK_SEC == 5.0

    def test_breach_exit_code_is_2(self) -> None:
        """Design-spec §4: disk-budget breach exits with code 2."""
        assert DISK_BUDGET_EXCEEDED_EXIT_CODE == 2

    def test_artifact_name_is_pinned(self) -> None:
        """Reporter consumers must not have to discover the filename."""
        assert DISK_BUDGET_EXCEEDED_ARTIFACT_NAME == "disk_budget_exceeded.json"

    def test_reason_token_is_pinned(self) -> None:
        """SKIPPED outcomes carry a stable skip_reason token."""
        assert DISK_BUDGET_EXCEEDED_REASON == "disk_budget_exceeded"


# ---------------------------------------------------------------------------
# Constructor validation
# ---------------------------------------------------------------------------


class TestConstructorGuards:
    def test_negative_budget_rejected(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            DiskBudgetPoller(tmp_path, max_disk_mb=-1)

    def test_non_int_budget_rejected(self, tmp_path: Path) -> None:
        with pytest.raises(TypeError):
            DiskBudgetPoller(tmp_path, max_disk_mb=1.5)  # type: ignore[arg-type]

    def test_boolean_budget_rejected(self, tmp_path: Path) -> None:
        """``True`` is an ``int`` in Python; the poller refuses it."""
        with pytest.raises(TypeError):
            DiskBudgetPoller(tmp_path, max_disk_mb=True)  # type: ignore[arg-type]

    def test_zero_tick_rejected(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            DiskBudgetPoller(tmp_path, tick_sec=0)

    def test_negative_tick_rejected(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            DiskBudgetPoller(tmp_path, tick_sec=-0.1)

    def test_empty_artifact_name_rejected(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            DiskBudgetPoller(tmp_path, artifact_name="")


# ---------------------------------------------------------------------------
# Default budget / lifecycle
# ---------------------------------------------------------------------------


class TestDefaults:
    def test_default_budget_uses_module_constant(self, tmp_path: Path) -> None:
        poller = DiskBudgetPoller(tmp_path)
        assert poller.max_disk_mb == DEFAULT_DISK_BUDGET_MB
        assert poller.budget_bytes == DEFAULT_DISK_BUDGET_MB * 1024 * 1024

    def test_default_tick_uses_module_constant(self, tmp_path: Path) -> None:
        poller = DiskBudgetPoller(tmp_path)
        assert poller.tick_sec == DEFAULT_DISK_POLL_TICK_SEC

    def test_enabled_when_budget_positive(self, tmp_path: Path) -> None:
        poller = DiskBudgetPoller(tmp_path, max_disk_mb=1)
        assert poller.enabled is True

    def test_disabled_when_budget_zero(self, tmp_path: Path) -> None:
        poller = DiskBudgetPoller(tmp_path, max_disk_mb=0)
        assert poller.enabled is False


# ---------------------------------------------------------------------------
# ``max_disk_mb=0`` disables the poller entirely
# ---------------------------------------------------------------------------


class TestDisabledPoller:
    def test_start_is_noop_when_disabled(self, tmp_path: Path) -> None:
        poller = DiskBudgetPoller(tmp_path, max_disk_mb=0, tick_sec=0.01)
        poller.start()
        # No thread should have been spawned; start() is idempotent in
        # the disabled state.
        assert poller._thread is None  # noqa: SLF001 — white-box check
        poller.stop()
        assert poller.is_breached() is False

    def test_breach_does_not_fire_when_disabled(self, tmp_path: Path) -> None:
        """Writing past the would-be budget never triggers a breach."""
        poller = DiskBudgetPoller(tmp_path, max_disk_mb=0, tick_sec=0.01)
        with poller:
            # Write 200 KB — would have breached a 1-byte budget if the
            # poller were enabled. The disabled poller never inspects.
            _write_bytes(tmp_path / "big.bin", 200 * 1024)
            time.sleep(0.05)
            assert poller.is_breached() is False
            assert poller.breach_detail() is None
            assert poller.artifact_path() is None


# ---------------------------------------------------------------------------
# Breach detection + side-car payload
# ---------------------------------------------------------------------------


class TestBreachDetection:
    def test_breach_triggers_when_usage_exceeds_budget(
        self, tmp_path: Path
    ) -> None:
        """The poller flips ``is_breached`` after a tick observes the breach."""
        poller = DiskBudgetPoller(
            tmp_path,
            max_disk_mb=1,
            tick_sec=0.05,
            clock=lambda: "2026-05-20T00:00:00Z",
        )
        # Write 1.5 MB — comfortably past the 1 MB budget.
        _write_bytes(tmp_path / "payload.bin", int(1.5 * 1024 * 1024))
        with poller:
            assert _wait_for_breach(poller), (
                "poller did not detect breach within timeout"
            )

    def test_breach_writes_side_car_with_payload(self, tmp_path: Path) -> None:
        poller = DiskBudgetPoller(
            tmp_path,
            max_disk_mb=1,
            tick_sec=0.05,
            clock=lambda: "2026-05-20T12:34:56Z",
        )
        _write_bytes(tmp_path / "payload.bin", int(1.5 * 1024 * 1024))
        with poller:
            assert _wait_for_breach(poller)
            poller.stop()
        side_car = tmp_path / DISK_BUDGET_EXCEEDED_ARTIFACT_NAME
        assert side_car.exists()
        payload = json.loads(side_car.read_text(encoding="utf-8"))
        assert payload["reason"] == DISK_BUDGET_EXCEEDED_REASON
        assert payload["max_disk_mb"] == 1
        assert payload["budget_bytes"] == 1024 * 1024
        assert payload["usage_bytes"] > payload["budget_bytes"]
        assert payload["output_dir"] == str(tmp_path)
        assert payload["ticked_at"] == "2026-05-20T12:34:56Z"

    def test_breach_detail_matches_side_car(self, tmp_path: Path) -> None:
        poller = DiskBudgetPoller(
            tmp_path,
            max_disk_mb=1,
            tick_sec=0.05,
            clock=lambda: "2026-05-20T00:00:00Z",
        )
        _write_bytes(tmp_path / "payload.bin", int(1.5 * 1024 * 1024))
        with poller:
            assert _wait_for_breach(poller)
            poller.stop()
        side_car_data = json.loads(
            (tmp_path / DISK_BUDGET_EXCEEDED_ARTIFACT_NAME).read_text()
        )
        assert dict(poller.breach_detail()) == side_car_data

    def test_breach_is_one_shot(self, tmp_path: Path) -> None:
        """Once breached the flag stays set; further ticks do not reset it."""
        poller = DiskBudgetPoller(
            tmp_path,
            max_disk_mb=1,
            tick_sec=0.05,
            clock=lambda: "2026-05-20T00:00:00Z",
        )
        _write_bytes(tmp_path / "payload.bin", int(1.5 * 1024 * 1024))
        with poller:
            assert _wait_for_breach(poller)
            # Even if the directory is cleaned up after the breach the
            # flag must remain set so the orchestrator's downstream
            # logic sees a stable signal.
            (tmp_path / "payload.bin").unlink()
            time.sleep(0.1)
            assert poller.is_breached() is True

    def test_no_breach_when_usage_under_budget(self, tmp_path: Path) -> None:
        poller = DiskBudgetPoller(
            tmp_path, max_disk_mb=1, tick_sec=0.05
        )
        _write_bytes(tmp_path / "small.bin", 4096)
        with poller:
            time.sleep(0.2)
            assert poller.is_breached() is False
            assert poller.breach_detail() is None
            assert poller.artifact_path() is None

    def test_artifact_path_returns_none_before_breach(
        self, tmp_path: Path
    ) -> None:
        poller = DiskBudgetPoller(tmp_path, max_disk_mb=1, tick_sec=0.05)
        with poller:
            assert poller.artifact_path() is None


# ---------------------------------------------------------------------------
# Symlinks must not double-count
# ---------------------------------------------------------------------------


class TestSymlinkHandling:
    def test_symlinks_are_skipped(self, tmp_path: Path) -> None:
        """A symlink that points outside the tree must not inflate usage."""
        outside = tmp_path.parent / "outside"
        outside.mkdir(exist_ok=True)
        target = outside / "huge.bin"
        try:
            _write_bytes(target, 2 * 1024 * 1024)
            link = tmp_path / "evil-link"
            link.symlink_to(target)
            poller = DiskBudgetPoller(
                tmp_path, max_disk_mb=1, tick_sec=0.05
            )
            with poller:
                time.sleep(0.2)
                # The link target is 2 MB > 1 MB budget. If the poller
                # followed the symlink the breach would fire; the
                # contract is that symlinks are skipped.
                assert poller.is_breached() is False
        finally:
            target.unlink(missing_ok=True)
            outside.rmdir()


# ---------------------------------------------------------------------------
# BreachDetail dataclass
# ---------------------------------------------------------------------------


class TestBreachDetail:
    def test_to_dict_preserves_declared_order(self) -> None:
        detail = BreachDetail(
            reason="disk_budget_exceeded",
            output_dir="/tmp/run",
            usage_bytes=2_000_000,
            budget_bytes=1_048_576,
            max_disk_mb=1,
            ticked_at="2026-05-20T00:00:00Z",
        )
        assert list(detail.to_dict().keys()) == [
            "reason",
            "output_dir",
            "usage_bytes",
            "budget_bytes",
            "max_disk_mb",
            "ticked_at",
        ]


# ---------------------------------------------------------------------------
# RunOrchestrator integration
# ---------------------------------------------------------------------------


class _GatedWorker:
    """Worker that blocks until a release event is set.

    Used to keep an "in-flight" eval pending while a disk-budget breach
    propagates. The worker records its own spec id so tests can assert
    submission ordering.
    """

    def __init__(self) -> None:
        self.release = threading.Event()
        self.submitted: list[str] = []
        self.completed: list[str] = []
        self._lock = threading.Lock()

    def __call__(self, spec: EvalSpec) -> EvalOutcome:
        with self._lock:
            self.submitted.append(spec.id)
        # Wait up to 2 s; tests release within ms.
        self.release.wait(timeout=2.0)
        with self._lock:
            self.completed.append(spec.id)
        return _passing_outcome(spec)


class TestOrchestratorIntegration:
    def test_orchestrator_accepts_optional_poller(
        self, tmp_path: Path
    ) -> None:
        """The constructor accepts ``disk_budget_poller=None`` unchanged."""

        def worker(spec: EvalSpec) -> EvalOutcome:
            return _passing_outcome(spec)

        orch = RunOrchestrator(run_one=worker, disk_budget_poller=None)
        outcomes = orch.run([_spec("E1"), _spec("E2")])
        assert [o.status for o in outcomes] == ["PASS", "PASS"]

    def test_disabled_poller_does_not_change_behavior(
        self, tmp_path: Path
    ) -> None:
        """``max_disk_mb=0`` is a no-op even when wired through the orchestrator."""

        def worker(spec: EvalSpec) -> EvalOutcome:
            return _passing_outcome(spec)

        poller = DiskBudgetPoller(tmp_path, max_disk_mb=0, tick_sec=0.05)
        orch = RunOrchestrator(run_one=worker, disk_budget_poller=poller)
        outcomes = orch.run([_spec("E1"), _spec("E2"), _spec("E3")])
        assert [o.status for o in outcomes] == ["PASS", "PASS", "PASS"]

    def test_breach_stops_scheduling_but_preserves_outcome_per_spec(
        self, tmp_path: Path
    ) -> None:
        """Unsubmitted specs receive SKIPPED outcomes with the pinned reason.

        Pre-breach the poller before calling ``run()`` so the
        submission loop observes a stable ``is_breached() == True``
        from its first iteration. The orchestrator must still emit
        one outcome per spec (the per-spec contract) and the
        synthesised rows must carry the pinned ``skip_reason`` /
        ``skip_flag_triggered``.
        """

        _write_bytes(tmp_path / "payload.bin", int(1.5 * 1024 * 1024))
        poller = DiskBudgetPoller(
            tmp_path,
            max_disk_mb=1,
            tick_sec=0.05,
        )
        poller.start()
        try:
            assert _wait_for_breach(poller, timeout=2.0), (
                "poller failed to flag the pre-populated breach"
            )
        finally:
            # Stop the background thread but keep the breach flag set
            # — ``is_breached`` is one-shot, so the orchestrator still
            # sees it as breached after ``stop()``.
            poller.stop()
        assert poller.is_breached() is True

        worker_calls: list[str] = []

        def worker(spec: EvalSpec) -> EvalOutcome:
            # The worker must never run when the budget is already
            # breached; if it does, the assertion below catches it.
            worker_calls.append(spec.id)
            return _passing_outcome(spec)

        orch = RunOrchestrator(run_one=worker, disk_budget_poller=poller)
        outcomes = orch.run(
            [_spec("E1"), _spec("E2"), _spec("E3")], parallel=1
        )
        assert len(outcomes) == 3
        assert worker_calls == [], (
            "worker invoked despite pre-existing budget breach"
        )
        for outcome in outcomes:
            assert outcome.status == "SKIPPED"
            assert outcome.skip_reason == DISK_BUDGET_EXCEEDED_REASON
            assert outcome.skip_flag_triggered == "--max-disk-mb"
        # Side-car was written during the pre-breach phase.
        assert (tmp_path / DISK_BUDGET_EXCEEDED_ARTIFACT_NAME).exists()

    def test_inflight_workers_complete_after_breach(
        self, tmp_path: Path
    ) -> None:
        """In-flight workers are not interrupted by a mid-run breach.

        Submit a batch of slow workers; once the pool is saturated,
        write a payload that exceeds the budget. The poller detects
        the breach on its next tick. Every already-submitted future
        runs to completion (returning ``PASS``); the orchestrator
        never kills a worker thread on disk-budget exit.
        """

        poller = DiskBudgetPoller(
            tmp_path,
            max_disk_mb=1,
            tick_sec=0.05,
        )

        started = threading.Event()
        release = threading.Event()
        start_count = 0
        start_lock = threading.Lock()

        def worker(spec: EvalSpec) -> EvalOutcome:
            nonlocal start_count
            with start_lock:
                start_count += 1
                if start_count == 2:
                    started.set()
            release.wait(timeout=3.0)
            return _passing_outcome(spec)

        orch = RunOrchestrator(run_one=worker, disk_budget_poller=poller)

        # Drive ``run`` on a background thread so we can trip the
        # breach mid-execution from the test thread.
        outcomes_holder: dict[str, list[EvalOutcome]] = {}

        def runner() -> None:
            outcomes_holder["result"] = orch.run(
                [_spec("E1"), _spec("E2")], parallel=2
            )

        run_thread = threading.Thread(target=runner)
        run_thread.start()
        try:
            assert started.wait(timeout=2.0), "workers never started"
            # Trip the breach while both workers are pending.
            _write_bytes(tmp_path / "payload.bin", int(1.5 * 1024 * 1024))
            assert _wait_for_breach(poller, timeout=2.0)
        finally:
            release.set()
            run_thread.join(timeout=5.0)

        assert "result" in outcomes_holder, "orchestrator did not return"
        outcomes = outcomes_holder["result"]
        # Both specs were submitted before the breach, so both run to
        # completion — the orchestrator does not interrupt in-flight
        # work on a disk-budget breach.
        assert [o.status for o in outcomes] == ["PASS", "PASS"]

    def test_breach_outcome_order_matches_input_order(
        self, tmp_path: Path
    ) -> None:
        """Even with SKIPPED backfills, the outcome order must mirror specs.

        Pre-breach the poller so every spec is routed to the SKIPPED
        backfill path; verify the synthesised outcomes still appear in
        input order.
        """
        _write_bytes(tmp_path / "payload.bin", int(1.5 * 1024 * 1024))
        poller = DiskBudgetPoller(tmp_path, max_disk_mb=1, tick_sec=0.05)
        poller.start()
        try:
            assert _wait_for_breach(poller, timeout=2.0)
        finally:
            poller.stop()

        def worker(spec: EvalSpec) -> EvalOutcome:
            return _passing_outcome(spec)

        orch = RunOrchestrator(run_one=worker, disk_budget_poller=poller)
        spec_ids = ["A", "B", "C", "D"]
        outcomes = orch.run([_spec(i) for i in spec_ids], parallel=1)
        assert [o.eval_id for o in outcomes] == spec_ids

    def test_no_breach_means_all_pass(self, tmp_path: Path) -> None:
        """A healthy poller does not synthesise SKIPPED outcomes."""

        def worker(spec: EvalSpec) -> EvalOutcome:
            return _passing_outcome(spec)

        poller = DiskBudgetPoller(tmp_path, max_disk_mb=64, tick_sec=0.05)
        orch = RunOrchestrator(run_one=worker, disk_budget_poller=poller)
        outcomes = orch.run([_spec("E1"), _spec("E2")])
        assert all(o.status == "PASS" for o in outcomes)

    def test_breach_stops_poller_on_orchestrator_exit(
        self, tmp_path: Path
    ) -> None:
        """The poller thread is joined when ``run()`` returns."""
        _write_bytes(tmp_path / "payload.bin", int(1.5 * 1024 * 1024))
        poller = DiskBudgetPoller(tmp_path, max_disk_mb=1, tick_sec=0.05)

        def worker(spec: EvalSpec) -> EvalOutcome:
            return _passing_outcome(spec)

        orch = RunOrchestrator(run_one=worker, disk_budget_poller=poller)
        orch.run([_spec("E1")], parallel=1)
        # After run() returns the thread must be dead. ``_thread`` is
        # the daemon spawned by ``start``; ``is_alive() is False``
        # confirms the ``finally`` block joined it.
        thread = poller._thread  # noqa: SLF001
        if thread is not None:
            assert thread.is_alive() is False

    def test_cancellation_takes_priority_over_disk_breach(
        self, tmp_path: Path
    ) -> None:
        """A cancelled token routes unsubmitted specs to INTERRUPTED, not SKIPPED."""
        from superclaude.cli.eval.signal_handler import CancellationToken

        _write_bytes(tmp_path / "payload.bin", int(1.5 * 1024 * 1024))
        token = CancellationToken()
        token.cancel()
        poller = DiskBudgetPoller(tmp_path, max_disk_mb=1, tick_sec=0.05)

        def worker(spec: EvalSpec) -> EvalOutcome:
            return _passing_outcome(spec)

        orch = RunOrchestrator(
            run_one=worker,
            cancellation_token=token,
            disk_budget_poller=poller,
        )
        outcomes = orch.run(
            [_spec("E1"), _spec("E2")], parallel=1
        )
        # Token was already cancelled before submission, so every spec
        # is INTERRUPTED (operator intent dominates the resource limit).
        assert all(o.status == "INTERRUPTED" for o in outcomes)
