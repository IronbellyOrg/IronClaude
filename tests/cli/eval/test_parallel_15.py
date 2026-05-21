"""FR-G2 integration test: 15 evals in parallel with strict per-eval isolation.

Task T03.16 / Deliverable D-0058 / Roadmap row R-058.

This file owns the *end-to-end* FR-G2 acceptance the design-spec pins:

    "Run all 15 evals in parallel (default concurrency=8, max=15) with
    strict isolation: each eval owns its own ``HOME`` directory, its own
    ``session_id``, and its own state/telemetry namespace."

Where ``test_orchestrator.py`` (T03.15) owns the *scheduling primitive*
in isolation from runner internals — its worker is a stub that returns a
canned outcome — this file does the opposite: it composes the real
:class:`HomeIsolation` (T02.11 / D-0032) with the real
:class:`RunOrchestrator` (T03.15 / D-0057) and asserts the resulting
suite-level guarantees:

1. **Parallelism**: all 15 specs run concurrently when scheduled at
   ``--parallel 8``, with the runtime observing ``max_workers`` workers
   simultaneously bounded by the clamp.
2. **HOME isolation**: every eval receives its own
   ``HomeIsolation.home_path`` directory. No two workers see the same
   ``HOME`` value, and each directory lives under the scratch root the
   orchestrator declared.
3. **session_id isolation**: every eval receives a unique
   ``CLAUDE_SESSION_ID`` value. The worker stamps the id into a per-
   eval JSONL log so the assertion reads it back from disk — verifying
   that the value actually reached the subprocess view, not just the
   Python record.
4. **Telemetry namespace isolation**: each eval writes its
   ``telemetry.jsonl`` under its own ``home_path/.eval-logs/`` namespace.
   No two evals share a path, no two evals share a JSONL contents, and
   the namespace lives under ``home_path`` (so a sibling eval cannot
   accidentally read it through the orchestrator's run directory).
5. **Clamp at ``MAX_PARALLEL``**: requesting ``parallel=16`` saturates
   to ``RunOrchestrator.MAX_PARALLEL == 15`` without raising — the same
   contract ``test_orchestrator.py`` pins at the unit level, re-asserted
   here against the real orchestrator + real worker composition.

The worker stub deliberately substitutes for the
``EvalRunner.spawn / inject / observe`` trio because spawning a real
Claude subprocess would require a working ``claude`` binary and a hooks
deploy, neither of which is in scope for this integration test. What is
in scope — and what the FR-G2 acceptance criteria actually call out —
is the orchestrator + isolation composition: each spec gets its own
``HomeIsolation`` instance, ``setup()`` materializes a unique
``mkdtemp``-ed HOME, ``env()`` exports a unique ``CLAUDE_SESSION_ID``,
and the per-eval JSONL log lands under the per-eval HOME. The real
PtyDriver / ClaudeProcessAdapter integration is exercised in Phase 4.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.eval.config import EvalConfig
from superclaude.cli.eval.isolation import HomeIsolation
from superclaude.cli.eval.models import EvalOutcome, EvalSpec
from superclaude.cli.eval.orchestrator import RunOrchestrator


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    """Per-test scratch root (mirrors the orchestrator's ``--scratch-root``)."""

    root = tmp_path / "eval-runs"
    root.mkdir()
    return root


@pytest.fixture
def eval_config(scratch_root: Path) -> EvalConfig:
    """An :class:`EvalConfig` whose allowlist contains the test scratch root."""

    return EvalConfig(allowed_scratch_roots=(scratch_root,))


def _build_specs(count: int) -> list[EvalSpec]:
    """Build ``count`` deterministically-named eval specs.

    Ids use ``E000``..``E0NN`` zero-padded so the FR-SCH2 regex
    (``^[A-Za-z][A-Za-z0-9._-]*$``) is satisfied and lexicographic order
    matches numeric order for the input-order assertion.
    """

    return [EvalSpec(id=f"E{i:03d}", title=f"eval-{i}") for i in range(count)]


# ---------------------------------------------------------------------------
# Real-isolation worker
# ---------------------------------------------------------------------------


def _make_isolation_worker(
    *,
    scratch_root: Path,
    config: EvalConfig,
    observed_concurrency: list[int],
    concurrency_lock: threading.Lock,
    isolations_seen: dict[str, HomeIsolation],
    isolations_lock: threading.Lock,
    hold_event: threading.Event | None = None,
):
    """Build a worker that composes :class:`HomeIsolation` with telemetry.

    The worker:

    * Allocates a unique ``session_id`` derived from the eval id.
    * Constructs a real :class:`HomeIsolation`, calls ``setup`` so a
      unique ``mkdtemp``-ed HOME is materialized, and writes a
      ``telemetry.jsonl`` log under the eval-private ``.eval-logs/``
      namespace.
    * Snapshots the running-worker count so the caller can verify the
      :class:`RunOrchestrator` clamp at runtime.
    * Stashes the :class:`HomeIsolation` instance keyed by eval id so
      the caller can assert HOME / session_id / telemetry uniqueness
      *after* the orchestrator returns (the home directories survive
      because ``teardown(keep=True)`` is used).
    * Returns a PASS :class:`EvalOutcome` whose ``artifacts`` carry the
      telemetry path so the orchestrator's outcome list also encodes
      the per-eval namespace.
    """

    running = [0]  # box so we can mutate from inside the closure

    def worker(spec: EvalSpec) -> EvalOutcome:
        # ---- Concurrency snapshot ------------------------------------
        with concurrency_lock:
            running[0] += 1
            observed_concurrency.append(running[0])
        try:
            # ---- Build real isolation -------------------------------
            session_id = f"sess-{spec.id}"
            isolation = HomeIsolation(
                eval_id=spec.id,
                home_root=scratch_root,
                session_id=session_id,
            )
            home_path = isolation.setup(config=config)

            # ---- Write per-eval telemetry --------------------------
            # FR-G2 calls out a per-eval "telemetry namespace"; we model
            # it as a JSONL file under the eval-private ``.eval-logs/``
            # directory. The directory lives under ``home_path`` so a
            # sibling eval physically cannot read or write here.
            telemetry_dir = home_path / ".eval-logs"
            telemetry_dir.mkdir(parents=True, exist_ok=True)
            telemetry_path = telemetry_dir / "telemetry.jsonl"

            env = isolation.env()
            event = {
                "event": "eval_started",
                "eval_id": spec.id,
                "home_path": str(home_path),
                "session_id": session_id,
                "env_home": env["HOME"],
                "env_session_id": env["CLAUDE_SESSION_ID"],
                "telemetry_namespace": str(telemetry_path),
            }
            telemetry_path.write_text(
                json.dumps(event, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            # ---- Hold barrier for the concurrency test --------------
            if hold_event is not None:
                hold_event.wait(timeout=5.0)

            # ---- Stash the isolation so the test can inspect it ----
            with isolations_lock:
                isolations_seen[spec.id] = isolation

            # ---- Tear down without removing so the test can read JSONL
            isolation.teardown(keep=True)

            return EvalOutcome(
                eval_id=spec.id,
                title=spec.title,
                status="PASS",
                duration_sec=0.0,
                expects=(),
                skip_reason=None,
                skip_flag_triggered=None,
                artifacts={"telemetry": str(telemetry_path)},
                error_class=None,
            )
        finally:
            with concurrency_lock:
                running[0] -= 1

    return worker


# ---------------------------------------------------------------------------
# AC: 15-eval parallel run with full isolation
# ---------------------------------------------------------------------------


class TestParallel15:
    """The FR-G2 end-to-end acceptance bundle.

    Each test exercises the same composition (RunOrchestrator over a
    real HomeIsolation worker on 15 specs) but asserts a distinct slice
    of the isolation contract so a failure pinpoints the broken
    guarantee instead of dumping a single mega-assertion.
    """

    def test_runs_fifteen_evals_at_parallel_eight_exits_clean(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """All 15 specs return PASS in input order at ``--parallel 8``."""

        observed_concurrency: list[int] = []
        concurrency_lock = threading.Lock()
        isolations_seen: dict[str, HomeIsolation] = {}
        isolations_lock = threading.Lock()

        worker = _make_isolation_worker(
            scratch_root=scratch_root,
            config=eval_config,
            observed_concurrency=observed_concurrency,
            concurrency_lock=concurrency_lock,
            isolations_seen=isolations_seen,
            isolations_lock=isolations_lock,
        )

        specs = _build_specs(15)
        orch = RunOrchestrator(run_one=worker)
        outcomes = orch.run(specs, parallel=8)

        # AC: one outcome per spec, all PASS, in input order.
        assert len(outcomes) == 15
        assert [o.eval_id for o in outcomes] == [s.id for s in specs]
        assert all(o.status == "PASS" for o in outcomes), [
            (o.eval_id, o.status) for o in outcomes
        ]

    def test_each_eval_receives_unique_home_path(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """``HomeIsolation.home_path`` is unique per eval and under the scratch root."""

        observed_concurrency: list[int] = []
        concurrency_lock = threading.Lock()
        isolations_seen: dict[str, HomeIsolation] = {}
        isolations_lock = threading.Lock()

        worker = _make_isolation_worker(
            scratch_root=scratch_root,
            config=eval_config,
            observed_concurrency=observed_concurrency,
            concurrency_lock=concurrency_lock,
            isolations_seen=isolations_seen,
            isolations_lock=isolations_lock,
        )

        specs = _build_specs(15)
        orch = RunOrchestrator(run_one=worker)
        orch.run(specs, parallel=8)

        assert len(isolations_seen) == 15
        home_paths = {
            iso.eval_id: _read_telemetry_home(iso) for iso in isolations_seen.values()
        }
        # No collisions across the 15 evals.
        assert len(set(home_paths.values())) == 15, home_paths
        # Every home_path is rooted under the declared scratch root.
        scratch_resolved = scratch_root.resolve()
        for eval_id, path in home_paths.items():
            assert Path(path).resolve().is_relative_to(scratch_resolved), (
                f"{eval_id}: {path} escapes scratch_root {scratch_resolved}"
            )

    def test_each_eval_receives_unique_session_id(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """``CLAUDE_SESSION_ID`` is unique per eval (verified via per-eval JSONL)."""

        observed_concurrency: list[int] = []
        concurrency_lock = threading.Lock()
        isolations_seen: dict[str, HomeIsolation] = {}
        isolations_lock = threading.Lock()

        worker = _make_isolation_worker(
            scratch_root=scratch_root,
            config=eval_config,
            observed_concurrency=observed_concurrency,
            concurrency_lock=concurrency_lock,
            isolations_seen=isolations_seen,
            isolations_lock=isolations_lock,
        )

        specs = _build_specs(15)
        orch = RunOrchestrator(run_one=worker)
        orch.run(specs, parallel=8)

        session_ids_from_record = {iso.session_id for iso in isolations_seen.values()}
        session_ids_from_jsonl = {
            _read_telemetry_event(iso)["session_id"]
            for iso in isolations_seen.values()
        }
        env_session_ids_from_jsonl = {
            _read_telemetry_event(iso)["env_session_id"]
            for iso in isolations_seen.values()
        }
        # All three views agree: the record holds 15 unique ids, the
        # JSONL log (the assertion site documented in the AC) holds 15
        # unique ids, and the ``env()`` view the subprocess would see
        # holds the same 15 ids.
        assert len(session_ids_from_record) == 15
        assert len(session_ids_from_jsonl) == 15
        assert session_ids_from_record == session_ids_from_jsonl
        assert env_session_ids_from_jsonl == session_ids_from_jsonl

    def test_each_eval_has_isolated_telemetry_namespace(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """Telemetry JSONL paths are unique and contained under per-eval HOME."""

        observed_concurrency: list[int] = []
        concurrency_lock = threading.Lock()
        isolations_seen: dict[str, HomeIsolation] = {}
        isolations_lock = threading.Lock()

        worker = _make_isolation_worker(
            scratch_root=scratch_root,
            config=eval_config,
            observed_concurrency=observed_concurrency,
            concurrency_lock=concurrency_lock,
            isolations_seen=isolations_seen,
            isolations_lock=isolations_lock,
        )

        specs = _build_specs(15)
        orch = RunOrchestrator(run_one=worker)
        outcomes = orch.run(specs, parallel=8)

        # Each outcome carries the telemetry path on its artifacts map.
        telemetry_paths = [Path(o.artifacts["telemetry"]) for o in outcomes]
        # 15 unique paths.
        assert len({str(p) for p in telemetry_paths}) == 15

        for outcome, path in zip(outcomes, telemetry_paths, strict=True):
            assert path.exists(), f"{outcome.eval_id}: telemetry missing at {path}"
            # The telemetry file lives under THIS eval's home_path, not
            # under any sibling's.
            isolation = isolations_seen[outcome.eval_id]
            # ``teardown(keep=True)`` cleared the private slot; re-derive
            # the HOME by reading the JSONL we just wrote.
            event = _read_telemetry_event(isolation)
            recorded_home = Path(event["home_path"])
            assert path.is_relative_to(recorded_home), (
                f"{outcome.eval_id}: telemetry {path} escapes home {recorded_home}"
            )
            # The telemetry namespace recorded inside the JSONL agrees
            # with the path the orchestrator returned — defends against
            # a bug where the worker stamped one path and wrote another.
            assert event["telemetry_namespace"] == str(path)

    def test_per_eval_jsonl_contents_are_self_consistent(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """Each JSONL row's ``eval_id`` matches the directory it lives in."""

        observed_concurrency: list[int] = []
        concurrency_lock = threading.Lock()
        isolations_seen: dict[str, HomeIsolation] = {}
        isolations_lock = threading.Lock()

        worker = _make_isolation_worker(
            scratch_root=scratch_root,
            config=eval_config,
            observed_concurrency=observed_concurrency,
            concurrency_lock=concurrency_lock,
            isolations_seen=isolations_seen,
            isolations_lock=isolations_lock,
        )

        specs = _build_specs(15)
        orch = RunOrchestrator(run_one=worker)
        outcomes = orch.run(specs, parallel=8)

        for outcome in outcomes:
            isolation = isolations_seen[outcome.eval_id]
            event = _read_telemetry_event(isolation)
            assert event["eval_id"] == outcome.eval_id, (
                f"Cross-talk: telemetry for {outcome.eval_id} reads "
                f"{event['eval_id']!r}"
            )
            assert event["session_id"] == isolation.session_id
            # The env() snapshot baked into the JSONL agrees with the
            # canonical record values — closes the bug where ``env()``
            # would silently drop CLAUDE_SESSION_ID under concurrency.
            assert event["env_session_id"] == isolation.session_id
            assert event["env_home"] == event["home_path"]


# ---------------------------------------------------------------------------
# AC: parallel=16 clamps to MAX_PARALLEL=15
# ---------------------------------------------------------------------------


class TestParallelClampAtFifteen:
    def test_parallel_sixteen_clamps_to_fifteen(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """``parallel=16`` saturates to 15; no worker observes a 16th peer."""

        observed_concurrency: list[int] = []
        concurrency_lock = threading.Lock()
        isolations_seen: dict[str, HomeIsolation] = {}
        isolations_lock = threading.Lock()

        # Use a hold-event to keep every worker alive until the test
        # releases them, so the concurrency snapshot has a chance to
        # observe the upper-bound peer count. Without the barrier the
        # workers complete fast enough that the snapshot under-counts.
        hold_event = threading.Event()
        worker = _make_isolation_worker(
            scratch_root=scratch_root,
            config=eval_config,
            observed_concurrency=observed_concurrency,
            concurrency_lock=concurrency_lock,
            isolations_seen=isolations_seen,
            isolations_lock=isolations_lock,
            hold_event=hold_event,
        )

        # Submit 20 specs at parallel=16; if the clamp leaks we'll
        # observe more than 15 workers running concurrently. Once the
        # peak is observed we release the barrier so the pool drains.
        specs = _build_specs(20)
        orch = RunOrchestrator(run_one=worker)

        # Release the barrier on a delay so workers actually pile up
        # before any of them finish. The delay is generous (1s) but
        # bounded so a hung worker cannot block the test indefinitely.
        releaser = threading.Timer(1.0, hold_event.set)
        releaser.start()
        try:
            outcomes = orch.run(specs, parallel=16)
        finally:
            hold_event.set()  # unconditionally release in case of failure
            releaser.cancel()

        assert len(outcomes) == 20
        # The clamp is the *only* thing that can keep observed_concurrency
        # bounded at 15: ``ThreadPoolExecutor(max_workers=16)`` would
        # have admitted a 16th worker before any of them finished.
        assert max(observed_concurrency) <= RunOrchestrator.MAX_PARALLEL, (
            f"observed concurrency peaked at {max(observed_concurrency)} "
            f"workers; clamp at {RunOrchestrator.MAX_PARALLEL} leaked"
        )
        # Sanity check that the test actually achieved parallelism — if
        # the snapshot peaks at 1 the assertion above is vacuous.
        assert max(observed_concurrency) > 1, (
            "concurrency snapshot is degenerate; clamp assertion is vacuous"
        )

    def test_parallel_at_max_admits_fifteen_concurrent_workers(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """``parallel=15`` actually admits all 15 workers simultaneously."""

        observed_concurrency: list[int] = []
        concurrency_lock = threading.Lock()
        isolations_seen: dict[str, HomeIsolation] = {}
        isolations_lock = threading.Lock()

        hold_event = threading.Event()
        worker = _make_isolation_worker(
            scratch_root=scratch_root,
            config=eval_config,
            observed_concurrency=observed_concurrency,
            concurrency_lock=concurrency_lock,
            isolations_seen=isolations_seen,
            isolations_lock=isolations_lock,
            hold_event=hold_event,
        )

        specs = _build_specs(15)
        orch = RunOrchestrator(run_one=worker)
        releaser = threading.Timer(1.0, hold_event.set)
        releaser.start()
        try:
            outcomes = orch.run(specs, parallel=15)
        finally:
            hold_event.set()
            releaser.cancel()

        assert len(outcomes) == 15
        # Confirms the clamp does not under-admit either: when the
        # request equals MAX_PARALLEL, all 15 workers should run
        # concurrently. Without the barrier the snapshot could
        # under-count by chance; with the 1s hold every spawned worker
        # is parked in ``hold_event.wait`` long enough to be counted.
        assert max(observed_concurrency) == RunOrchestrator.MAX_PARALLEL, (
            f"parallel=15 admitted only {max(observed_concurrency)} "
            f"concurrent workers; expected {RunOrchestrator.MAX_PARALLEL}"
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_telemetry_home(iso: HomeIsolation) -> str:
    """Return the ``home_path`` stamp the worker baked into the JSONL log.

    ``HomeIsolation.teardown(keep=True)`` clears the private ``_home_path``
    slot so :attr:`HomeIsolation.home_path` raises ``RuntimeError`` after
    the worker returns. Reading the value from disk closes that gap
    *and* doubles as a verification that the JSONL was actually written
    by the worker we expected.
    """

    return _read_telemetry_event(iso)["home_path"]


def _read_telemetry_event(iso: HomeIsolation) -> dict[str, Any]:
    """Parse the eval's ``telemetry.jsonl`` and return the first event.

    The file is written exactly once per eval, so the first JSON object
    is the canonical record of what the worker observed when ``setup``
    returned.
    """

    # The worker's JSONL lives at ``home_path/.eval-logs/telemetry.jsonl``;
    # we cannot ask ``iso.home_path`` because teardown(keep=True) cleared
    # the slot. Instead re-derive the path by scanning ``home_root`` for
    # the subdir whose name starts with the eval id (``mkdtemp`` prefix
    # convention in HomeIsolation.setup).
    home_root = iso.home_root
    candidates = [
        p
        for p in home_root.iterdir()
        if p.is_dir() and p.name.startswith(f"{iso.eval_id}-")
    ]
    assert len(candidates) == 1, (
        f"expected exactly one preserved HOME for {iso.eval_id} under "
        f"{home_root}; found {[str(c) for c in candidates]}"
    )
    telemetry_path = candidates[0] / ".eval-logs" / "telemetry.jsonl"
    assert telemetry_path.exists(), (
        f"telemetry log missing for {iso.eval_id} at {telemetry_path}"
    )
    with telemetry_path.open(encoding="utf-8") as fh:
        return json.loads(fh.readline())
