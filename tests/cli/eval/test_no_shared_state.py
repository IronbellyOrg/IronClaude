"""NFR-ISO1 integration test: no shared mutable state across N×15 trials.

Task T03.20 / Deliverable D-0061 / Roadmap row R-061.

This file owns the *cross-trial* NFR-ISO1 acceptance the design-spec pins:

    "No shared HOMEs, no shared file handles (e.g. ``auggie-first.jsonl``),
    and no port collisions at ``--parallel 15``. Tests run N×15 trials."

Where ``test_parallel_15.py`` (T03.16 / D-0058) exercises **one** parallel
run of 15 evals and confirms intra-run isolation, this file iterates the
same composition **3 trials in a row** against a shared scratch root and
confirms inter-run isolation. That arrangement is the only one that can
expose low-probability race conditions on long-lived state — e.g. a
worker that accidentally caches a HOME path in a module-level dict, a
shared JSONL file handle held across runs, or a session_id allocator
that resets to a deterministic seed at run boundaries. A single trial
cannot catch those bugs; 3 × 15 == 45 evals against the same scratch
root can.

What the test asserts pairwise across **all 45 evals**:

1. **HOME path uniqueness.** Every eval's :attr:`HomeIsolation.home_path`
   is distinct from every other eval's, regardless of trial. The
   ``tempfile.mkdtemp`` randomness inside :meth:`HomeIsolation.setup`
   is what guarantees this even across trials — the assertion fails
   immediately if a regression starts re-using a HOME root.
2. **session_id uniqueness.** Each eval's ``CLAUDE_SESSION_ID`` is
   distinct across all trials. The worker allocates the id from a
   ``(trial, spec.id)`` tuple so a regression that re-uses a previous
   trial's id (e.g. a UUID generator seeded once per process) would
   surface as a collision.
3. **Per-eval JSONL path uniqueness.** The per-eval
   ``home_path/.eval-logs/telemetry.jsonl`` path is distinct across all
   45 evals. This is the proxy for the AC's "no shared file handles
   (e.g. ``auggie-first.jsonl``)" — once two evals diverge on JSONL
   path, no shared write handle can fan out into the wrong namespace.
4. **No port collisions.** :meth:`HomeIsolation.env` is inspected for
   any ``*_PORT`` / ``*PORT*`` keys; the harness's contract is that
   no port-bound state leaks into the per-eval env. A regression that
   added a port variable to the isolation layer would be caught here
   even before the harness binds the port — the variable's mere
   presence is the smell.
5. **No telemetry cross-talk.** Each per-eval JSONL is parsed and the
   embedded ``eval_id`` / ``session_id`` / ``trial`` fields match the
   eval that owns the file. Two evals that ended up writing to the
   same file would surface here as "eval ``E007`` reads ``E003`` in
   its own JSONL," which is a stronger assertion than path
   uniqueness alone (path uniqueness rules out shared *paths*; this
   rules out shared *content* even when the paths happen to differ).

The worker stub deliberately mirrors the shape used by
``test_parallel_15.py``: a real :class:`HomeIsolation`, a real
:meth:`setup`/``env``/``teardown`` cycle, a real JSONL write under the
eval-private namespace, and a synthetic PASS outcome. The Phase 4 PTY
adapter is out of scope; NFR-ISO1 is a statement about the
orchestrator+isolation composition, not about the subprocess that runs
under the per-eval HOME.

The number of trials is sized to be high enough to catch low-probability
races (3 trials × 15 evals × ~8 simultaneous workers gives many
distinct interleavings under the GIL) while staying cheap enough to run
in well under a second on the dev host.
"""

from __future__ import annotations

import json
import threading
from collections import Counter
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.eval.config import EvalConfig
from superclaude.cli.eval.isolation import HomeIsolation
from superclaude.cli.eval.models import EvalOutcome, EvalSpec
from superclaude.cli.eval.orchestrator import RunOrchestrator

# Number of trial repetitions. NFR-ISO1's "N×15 trials" leaves N to
# implementations; 3 is the smallest value that meaningfully separates
# "happened to work once" from "the contract holds run-over-run" while
# keeping the wall-clock cost trivial.
N_TRIALS = 3
EVALS_PER_TRIAL = 15
PARALLEL = 8


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    """A *single* scratch root shared across every trial.

    Sharing the root is the entire point: if two trials independently
    materialize HOMEs under the same directory and the runner caches
    state at module scope, the second trial's evals will collide with
    the first's. A per-trial scratch root would mask that bug.
    """

    root = tmp_path / "eval-runs"
    root.mkdir()
    return root


@pytest.fixture
def eval_config(scratch_root: Path) -> EvalConfig:
    """:class:`EvalConfig` whose allowlist contains the shared scratch root."""

    return EvalConfig(allowed_scratch_roots=(scratch_root,))


def _build_specs(count: int) -> list[EvalSpec]:
    """Build ``count`` deterministically-named eval specs.

    Ids use ``E000``..``E0NN`` zero-padded so the FR-SCH2 regex
    (``^[A-Za-z][A-Za-z0-9._-]*$``) is satisfied. The spec list is
    identical across trials *on purpose* — re-using the same ids
    across trials is what proves the runner does not key any cached
    state off eval_id (a regression that did so would surface as
    cross-trial collisions on either HOME or telemetry paths).
    """

    return [EvalSpec(id=f"E{i:03d}", title=f"eval-{i}") for i in range(count)]


# ---------------------------------------------------------------------------
# Real-isolation worker (mirrors test_parallel_15.py but stamps a trial id)
# ---------------------------------------------------------------------------


def _make_isolation_worker(
    *,
    trial: int,
    scratch_root: Path,
    config: EvalConfig,
    records: list[dict[str, Any]],
    records_lock: threading.Lock,
):
    """Build a worker that captures per-eval state into a thread-safe list.

    Each captured record contains everything the test needs to assert
    cross-trial uniqueness: the trial id, the eval id, the materialized
    ``home_path``, the allocated ``session_id``, the env dict the
    worker would have handed to the subprocess, and the JSONL path the
    worker wrote into. Records survive the trial boundary because the
    worker uses ``teardown(keep=True)`` — the HOMEs stay on disk so the
    final assertions can re-read them.
    """

    def worker(spec: EvalSpec) -> EvalOutcome:
        # Allocate a session_id that bakes in both the trial number and
        # the eval id. If a future regression introduced a UUID
        # generator that reset its seed at run boundaries, the test
        # would still pass on session_id uniqueness (because the worker
        # holds the canonical mapping) — but the env() / JSONL views
        # would diverge, which Test 5 catches.
        session_id = f"sess-t{trial}-{spec.id}"
        isolation = HomeIsolation(
            eval_id=spec.id,
            home_root=scratch_root,
            session_id=session_id,
        )
        home_path = isolation.setup(config=config)
        env = dict(isolation.env())

        # Write a per-eval JSONL log under the eval-private namespace.
        # The path is identical in shape to the one ``test_parallel_15``
        # writes, so a cross-trial regression that shared a file
        # handle would manifest as either a path collision (Test 3)
        # or duplicated content across files (Test 5).
        telemetry_dir = home_path / ".eval-logs"
        telemetry_dir.mkdir(parents=True, exist_ok=True)
        telemetry_path = telemetry_dir / "telemetry.jsonl"
        event = {
            "event": "eval_started",
            "trial": trial,
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

        with records_lock:
            records.append(
                {
                    "trial": trial,
                    "eval_id": spec.id,
                    "home_path": str(home_path),
                    "session_id": session_id,
                    "env": env,
                    "telemetry_path": str(telemetry_path),
                }
            )

        # Keep the HOME on disk so the final assertions can re-read the
        # JSONL after every trial has finished.
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

    return worker


def _run_trials(
    scratch_root: Path,
    config: EvalConfig,
    *,
    n_trials: int = N_TRIALS,
    evals_per_trial: int = EVALS_PER_TRIAL,
    parallel: int = PARALLEL,
) -> list[dict[str, Any]]:
    """Execute ``n_trials`` of ``evals_per_trial``-eval parallel runs.

    Returns the consolidated record list, ordered by trial then by
    completion (the per-trial order is non-deterministic under
    ``as_completed``, which is exactly what cross-trial uniqueness
    assertions want to ride on top of).
    """

    records: list[dict[str, Any]] = []
    records_lock = threading.Lock()

    for trial in range(n_trials):
        worker = _make_isolation_worker(
            trial=trial,
            scratch_root=scratch_root,
            config=config,
            records=records,
            records_lock=records_lock,
        )
        specs = _build_specs(evals_per_trial)
        orch = RunOrchestrator(run_one=worker)
        outcomes = orch.run(specs, parallel=parallel)
        # Sanity: the trial itself must succeed before cross-trial
        # assertions can be meaningful. A failure here means the
        # orchestrator/isolation composition broke before NFR-ISO1
        # could be evaluated.
        assert len(outcomes) == evals_per_trial, (
            f"trial {trial}: expected {evals_per_trial} outcomes, got {len(outcomes)}"
        )
        assert all(o.status == "PASS" for o in outcomes), (
            f"trial {trial}: non-PASS outcomes: "
            f"{[(o.eval_id, o.status) for o in outcomes if o.status != 'PASS']}"
        )

    return records


# ---------------------------------------------------------------------------
# NFR-ISO1 cross-trial assertions
# ---------------------------------------------------------------------------


class TestNoSharedStateAcrossTrials:
    """The NFR-ISO1 cross-trial acceptance bundle.

    Every test re-runs the 3×15 trial composition and asserts a distinct
    slice of the no-shared-state contract. Splitting the assertions
    keeps a failure pinpointed to the broken guarantee rather than
    bundling everything into one opaque assert.
    """

    def test_three_trials_each_with_fifteen_evals_all_pass(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """Pre-condition: the trials themselves succeed."""

        records = _run_trials(scratch_root, eval_config)
        assert len(records) == N_TRIALS * EVALS_PER_TRIAL

    def test_home_paths_pairwise_distinct_across_all_trials(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """No two evals — across any trial — see the same HOME."""

        records = _run_trials(scratch_root, eval_config)
        home_paths = [r["home_path"] for r in records]
        duplicates = [path for path, count in Counter(home_paths).items() if count > 1]
        assert not duplicates, (
            f"shared HOME paths detected across trials: {duplicates!r}"
        )
        assert len(set(home_paths)) == len(records)

    def test_home_paths_all_under_shared_scratch_root(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """Every materialized HOME is rooted under the declared scratch root.

        Uniqueness alone is not enough — a regression that ``mkdtemp``-ed
        outside the scratch root would *also* yield unique paths but
        violate FR-ISO2. Re-asserting containment here closes that gap
        for the cross-trial case.
        """

        records = _run_trials(scratch_root, eval_config)
        scratch_resolved = scratch_root.resolve()
        for record in records:
            home_path = Path(record["home_path"]).resolve()
            assert home_path.is_relative_to(scratch_resolved), (
                f"trial {record['trial']} eval {record['eval_id']}: "
                f"home {home_path} escapes scratch root {scratch_resolved}"
            )

    def test_session_ids_pairwise_distinct_across_all_trials(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """``CLAUDE_SESSION_ID`` is distinct across every eval, every trial.

        The session id is the linchpin for any downstream telemetry
        join — if two evals share a session id, their hook logs collide
        in the eyes of the consumer even if their HOMEs are different.
        Verified in two views simultaneously: the worker's canonical
        record AND the env dict the subprocess would have observed.
        """

        records = _run_trials(scratch_root, eval_config)
        session_ids = [r["session_id"] for r in records]
        env_session_ids = [r["env"]["CLAUDE_SESSION_ID"] for r in records]

        assert len(set(session_ids)) == len(records), (
            f"shared session_ids in canonical record: "
            f"{[sid for sid, c in Counter(session_ids).items() if c > 1]!r}"
        )
        assert len(set(env_session_ids)) == len(records), (
            f"shared session_ids in env dict: "
            f"{[sid for sid, c in Counter(env_session_ids).items() if c > 1]!r}"
        )
        # The two views agree pairwise: a regression that allocated a
        # unique session_id but then exported a stale value via env()
        # would not be caught by either uniqueness check alone.
        assert session_ids == env_session_ids

    def test_telemetry_paths_pairwise_distinct_across_all_trials(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """JSONL paths are pairwise distinct across all 45 evals.

        Proxy for "no shared file handles (e.g. ``auggie-first.jsonl``)":
        once the paths diverge, no shared write handle can fan out into
        the wrong namespace by accident.
        """

        records = _run_trials(scratch_root, eval_config)
        telemetry_paths = [r["telemetry_path"] for r in records]
        duplicates = [
            path for path, count in Counter(telemetry_paths).items() if count > 1
        ]
        assert not duplicates, (
            f"shared telemetry paths detected across trials: {duplicates!r}"
        )
        assert len(set(telemetry_paths)) == len(records)

    def test_telemetry_contents_belong_to_owning_eval(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """Each JSONL file's contents match the eval that owns the path.

        Stronger than path uniqueness: even if two workers happened to
        produce distinct paths, a shared file handle could write the
        wrong record into one of them. Reading the file back and
        matching ``eval_id`` / ``session_id`` / ``trial`` rules that
        regression out.
        """

        records = _run_trials(scratch_root, eval_config)
        for record in records:
            telemetry_path = Path(record["telemetry_path"])
            assert telemetry_path.exists(), (
                f"trial {record['trial']} eval {record['eval_id']}: "
                f"telemetry missing at {telemetry_path}"
            )
            with telemetry_path.open(encoding="utf-8") as fh:
                event = json.loads(fh.readline())
            assert event["trial"] == record["trial"], (
                f"cross-talk: telemetry at {telemetry_path} carries "
                f"trial {event['trial']!r}; record says {record['trial']!r}"
            )
            assert event["eval_id"] == record["eval_id"], (
                f"cross-talk: telemetry at {telemetry_path} carries "
                f"eval_id {event['eval_id']!r}; record says "
                f"{record['eval_id']!r}"
            )
            assert event["session_id"] == record["session_id"]
            assert event["env_session_id"] == record["env"]["CLAUDE_SESSION_ID"]
            assert event["env_home"] == record["env"]["HOME"]
            assert event["telemetry_namespace"] == record["telemetry_path"]

    def test_no_port_state_leaks_into_per_eval_env(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """No port-bound variable appears in any per-eval env.

        NFR-ISO1 names "no port collisions" alongside HOME and JSONL.
        :class:`HomeIsolation` does not bind any port today, so the
        cleanest assertion is the structural one: no variable in the
        per-eval env dict carries a ``PORT`` suffix or ``_PORT_``
        infix. A regression that added one would have to opt in
        explicitly, and would surface here before any actual port
        could be claimed.
        """

        records = _run_trials(scratch_root, eval_config)
        for record in records:
            offending = [key for key in record["env"] if "PORT" in key.upper()]
            assert not offending, (
                f"trial {record['trial']} eval {record['eval_id']}: "
                f"unexpected port-bearing env keys {offending!r}"
            )

    def test_env_home_matches_recorded_home_path_for_every_eval(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """``env()['HOME']`` is the same string the worker recorded.

        Catches a regression where :meth:`HomeIsolation.env` returns a
        stale HOME from a previous trial — e.g. because the env-dict
        was memoized at module scope. The assertion is per-eval, so a
        single drift surfaces with the offending eval id rather than
        as a generic count mismatch.
        """

        records = _run_trials(scratch_root, eval_config)
        for record in records:
            assert record["env"]["HOME"] == record["home_path"], (
                f"trial {record['trial']} eval {record['eval_id']}: "
                f"env HOME ({record['env']['HOME']!r}) does not match "
                f"recorded home_path ({record['home_path']!r}); a stale "
                f"env dict has leaked across the trial boundary"
            )


# ---------------------------------------------------------------------------
# NFR-ISO1 intra-trial sanity (cheap regression guard)
# ---------------------------------------------------------------------------


class TestNoSharedStateWithinEachTrial:
    """A single-trial slice of NFR-ISO1, kept separate so a failure here
    pinpoints "broken intra-trial" vs "broken cross-trial" without
    requiring the reader to diff the two suites.
    """

    def test_each_trial_yields_fifteen_unique_homes(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """Within any one trial, all 15 HOMEs are pairwise distinct."""

        records = _run_trials(scratch_root, eval_config)
        for trial in range(N_TRIALS):
            trial_records = [r for r in records if r["trial"] == trial]
            assert len(trial_records) == EVALS_PER_TRIAL
            homes = {r["home_path"] for r in trial_records}
            assert len(homes) == EVALS_PER_TRIAL, (
                f"trial {trial}: only {len(homes)} unique HOMEs from "
                f"{EVALS_PER_TRIAL} evals"
            )

    def test_each_trial_yields_fifteen_unique_session_ids(
        self, scratch_root: Path, eval_config: EvalConfig
    ) -> None:
        """Within any one trial, all 15 session_ids are pairwise distinct."""

        records = _run_trials(scratch_root, eval_config)
        for trial in range(N_TRIALS):
            trial_records = [r for r in records if r["trial"] == trial]
            session_ids = {r["session_id"] for r in trial_records}
            assert len(session_ids) == EVALS_PER_TRIAL
