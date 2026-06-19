"""Per-phase turn-budget model tests (R-1..R-10, TM-0..TM-14).

These tests pin the per-phase ``TurnLedger`` model for the sprint runner. Under
the model, ``execute_sprint`` constructs a FRESH ledger for every phase sized
``max_turns × len(tasks)`` (R-1/R-2/R-3) at the tasks-resolution point, so a
heavy early phase can no longer drain the turns a later phase needs (the global
pool starvation regression TM-0 guards against). The gate (R-5) becomes a pure
within-phase safety net. The R-10 sprint-level wiring accumulator keeps the
persisted ``gate-kpi-report.md`` wiring totals sprint-cumulative after the
per-phase reset.

Harness notes
-------------
* A phase whose tasklist file carries ``### T<PP>.<TT>`` headings routes through
  the per-task executor path (``_parse_phase_tasks`` → ``execute_phase_tasks``).
* Per-task turn consumption is controlled by patching the module-level
  ``executor._run_task_subprocess`` (full sprint) or via the
  ``_subprocess_factory`` parameter (direct ``execute_phase_tasks`` call); both
  return ``(exit_code, turns_consumed, output_bytes)``.
* Per-phase ledger instances are captured by patching ``executor.TurnLedger``
  with an instance-recording factory (the real class is still constructed, so
  budget arithmetic is exercised for real).
* The final ``SprintResult`` is captured via the patched ``SprintLogger``'s
  ``write_summary`` call, mirroring ``test_multi_phase``.
"""

from __future__ import annotations

import contextlib
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from superclaude.cli.sprint.executor import (
    aggregate_task_results,
    execute_phase_tasks,
    execute_sprint,
)
from superclaude.cli.sprint.handoff import FileHandoffStore
from superclaude.cli.sprint.models import (
    GateOutcome,
    HandoffRecord,
    Phase,
    PhaseStatus,
    SprintConfig,
    SprintOutcome,
    TaskEntry,
    TaskStatus,
    TurnLedger,
)

# ---------------------------------------------------------------------------
# Shared harness helpers
# ---------------------------------------------------------------------------


def _write_task_phase_file(path: Path, phase_num: int, num_tasks: int) -> None:
    """Write a phase tasklist file with ``num_tasks`` ``### T<PP>.<TT>`` blocks."""
    lines = [f"# Phase {phase_num}\n", "\n## Tasks\n"]
    for t in range(1, num_tasks + 1):
        lines.append(
            f"\n### T{phase_num:02d}.{t:02d} -- task {t}\n\n"
            f"**Dependencies:** none\n\nBody for T{phase_num:02d}.{t:02d}.\n"
        )
    path.write_text("".join(lines), encoding="utf-8")


def _make_task_config(
    tmp_path: Path,
    *,
    phase_task_counts: list[int],
    max_turns: int = 100,
    **overrides,
) -> SprintConfig:
    """Build a SprintConfig with one task phase per entry in ``phase_task_counts``.

    Each phase file gets ``### T<PP>.<TT>`` headings so ``_parse_phase_tasks``
    routes the phase through the per-task executor. Wiring/anti-instinct gates
    default to ``off`` so PASS tasks stay clean unless a test overrides them.
    """
    phases: list[Phase] = []
    for i, n in enumerate(phase_task_counts, start=1):
        pf = tmp_path / f"phase-{i}-tasklist.md"
        _write_task_phase_file(pf, i, n)
        phases.append(Phase(number=i, file=pf, name=f"Phase {i}"))
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n", encoding="utf-8")
    kwargs = dict(
        index_path=index,
        release_dir=tmp_path,
        phases=phases,
        start_phase=1,
        end_phase=len(phases),
        max_turns=max_turns,
        wiring_gate_mode="off",
        wiring_gate_scope="none",
        gate_rollout_mode="off",
    )
    kwargs.update(overrides)
    return SprintConfig(**kwargs)


@contextlib.contextmanager
def _capture_ledgers():
    """Patch ``executor.TurnLedger`` to record each constructed instance.

    Yields a list of ``(instance, available_at_construction)`` tuples in
    construction order. ``available_at_construction`` equals ``initial_budget``
    because a fresh ledger has ``consumed == 0`` — i.e. it is the budget the
    phase sees AT ENTRY, before any task runs.
    """
    captured: list[tuple[TurnLedger, int]] = []
    real_cls = TurnLedger

    def _factory(*args, **kwargs):
        inst = real_cls(*args, **kwargs)
        captured.append((inst, inst.available()))
        return inst

    with patch("superclaude.cli.sprint.executor.TurnLedger", side_effect=_factory):
        yield captured


@contextlib.contextmanager
def _drive_sprint(
    *,
    subprocess_side_effect,
    phase_wiring_hook=None,
):
    """Drive ``execute_sprint`` with the full subprocess machinery patched out.

    ``subprocess_side_effect`` is installed as ``executor._run_task_subprocess``
    (signature ``(task, config, phase, prior_context="") -> (exit, turns, bytes)``).
    Optionally replace ``executor.run_post_phase_wiring_hook`` with
    ``phase_wiring_hook``. Yields a one-element list that will hold the captured
    ``SprintResult`` after the ``with`` block runs ``execute_sprint`` itself.
    """
    captured_result: list = []

    logger = MagicMock()
    logger.write_summary = MagicMock(side_effect=lambda sr: captured_result.append(sr))

    stack = [
        patch(
            "superclaude.cli.sprint.executor.shutil.which",
            return_value="/usr/bin/claude",
        ),
        patch(
            "superclaude.cli.sprint.executor._run_task_subprocess",
            side_effect=subprocess_side_effect,
        ),
        patch("superclaude.cli.sprint.notify._notify"),
        patch("superclaude.cli.sprint.executor.SprintLogger", return_value=logger),
    ]
    if phase_wiring_hook is not None:
        stack.append(
            patch(
                "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
                side_effect=phase_wiring_hook,
            )
        )

    with contextlib.ExitStack() as es:
        for p in stack:
            es.enter_context(p)
        yield captured_result


# ---------------------------------------------------------------------------
# TM-0 (MANDATORY regression) — global-pool starvation no longer occurs
# ---------------------------------------------------------------------------


@pytest.mark.regression
def test_regression_3x5_no_global_pool_starvation(tmp_path):
    """TM-0 (R-3): 3 phases × 5 tasks at --max-turns 100, each task consuming 25 turns.

    Under the OLD global pool (max_turns × len(active_phases) = 100 × 3 = 300),
    3 × 5 × 25 = 375 turns OVERFLOW the single 300-turn pool: once cumulative
    consumption passes 300 the per-task budget gate denies later launches, tasks
    are recorded SKIPPED, and the phase maps to ERROR. Under the per-phase model
    each phase gets its OWN fresh 500-turn pool (100 × 5) and 5 × 25 = 125 ≤ 500,
    so NOTHING is starved.

    NOTE (regression strength): 25 > 20 is deliberate. A 20-turn workload totals
    exactly 15 × 20 = 300 and merely *fills* the old pool without overflowing it —
    every task still launches (each launch needs only available >= minimum_allocation),
    so the old code would NOT skip/ERROR and the starvation assertions below would
    pass under it. 25/task (375 total) genuinely reproduces the starvation this
    regression guards, so the 0-SKIPPED / SUCCESS assertions — not just the
    structural per-phase-ledger assertions — distinguish old from new. (Spec TM-0
    requires >= 20 turns/task; 25 satisfies it.)

    Asserts EXACTLY: 0 SKIPPED tasks; all 3 phases PASS; sprint SUCCESS; and
    ledger.available() == 500 at entry to EACH of the 3 phases.
    """
    config = _make_task_config(tmp_path, phase_task_counts=[5, 5, 5], max_turns=100)

    def _subprocess(task, config, phase, prior_context=""):
        # Each task consumes 25 turns → 15 × 25 = 375 total, which OVERFLOWS the old
        # global pool (300) and would starve later phases under it, while staying
        # within each phase's own 500-turn budget (5 × 25 = 125) under the per-phase
        # model.
        return (0, 25, 100)

    with (
        _capture_ledgers() as ledgers,
        _drive_sprint(subprocess_side_effect=_subprocess) as captured,
    ):
        execute_sprint(config)

    result = captured[0]

    # Sprint succeeded and all three phases passed.
    assert result.outcome == SprintOutcome.SUCCESS
    assert len(result.phase_results) == 3
    for pr in result.phase_results:
        assert pr.status == PhaseStatus.PASS

    # Zero SKIPPED tasks across the whole sprint.
    skipped = [
        tr
        for pr in result.phase_results
        for tr in pr.task_results
        if tr.status == TaskStatus.SKIPPED
    ]
    assert skipped == [], f"expected 0 SKIPPED tasks, got {len(skipped)}"

    # A fresh ledger per phase, each sized 100 × 5 == 500, and available()==500
    # at entry to every phase (independent of any earlier phase's consumption).
    assert len(ledgers) == 3, f"expected one ledger per phase, got {len(ledgers)}"
    for inst, available_at_entry in ledgers:
        assert inst.initial_budget == 500
        assert available_at_entry == 500


# ---------------------------------------------------------------------------
# TM-1 (Integration) — fresh ledger per phase with distinct identities
# ---------------------------------------------------------------------------


def test_per_phase_ledger_is_fresh_each_phase(tmp_path):
    """TM-1 (R-2): 3 task phases with varied counts.

    Asserts EXACTLY: a fresh ledger is constructed per phase (object identities
    differ across phases) AND initial_budget == max_turns × len(tasks) for each
    phase.
    """
    counts = [2, 4, 3]
    config = _make_task_config(tmp_path, phase_task_counts=counts, max_turns=100)

    def _subprocess(task, config, phase, prior_context=""):
        return (0, 5, 100)

    with (
        _capture_ledgers() as ledgers,
        _drive_sprint(subprocess_side_effect=_subprocess),
    ):
        execute_sprint(config)

    instances = [inst for inst, _ in ledgers]
    # One fresh ledger per phase.
    assert len(instances) == len(counts)
    # Distinct object identities — no in-place reset/reuse across phases.
    assert len({id(inst) for inst in instances}) == len(counts)
    for a_idx in range(len(instances)):
        for b_idx in range(a_idx + 1, len(instances)):
            assert instances[a_idx] is not instances[b_idx]
    # Each ledger is sized max_turns × len(tasks) for its own phase.
    for inst, n in zip(instances, counts):
        assert inst.initial_budget == 100 * n


# ---------------------------------------------------------------------------
# TM-5 (Integration) — phase-1 reimbursement does not affect phase 2
# ---------------------------------------------------------------------------


def test_phase1_reimbursement_does_not_affect_phase2(tmp_path):
    """TM-5 (R-4): a reimbursement in phase 1 leaves phase 2's fresh ledger full.

    Phase-1 tasks consume FEWER turns (2) than minimum_allocation (5), so the
    per-task reconciliation credits (5 - 2) back to phase 1's ledger
    (reimbursed > 0) — a genuine phase-1 reimbursement. Phase 2 then constructs a
    brand-new ledger, so its available() at entry is the FULL max_turns ×
    len(tasks_phase2), unaffected by phase 1.

    Asserts EXACTLY: phase 2's fresh ledger is unaffected — its available() is
    full (== max_turns × len(tasks) for phase 2).
    """
    counts = [3, 2]  # phase 2 has 2 tasks → its budget is 100 × 2 == 200
    config = _make_task_config(tmp_path, phase_task_counts=counts, max_turns=100)

    def _subprocess(task, config, phase, prior_context=""):
        # Phase 1 tasks underspend (2 < minimum_allocation=5) → reimbursement.
        # Phase 2 tasks spend exactly minimum_allocation → no credit of their own.
        return (0, 2 if phase.number == 1 else 5, 100)

    with (
        _capture_ledgers() as ledgers,
        _drive_sprint(subprocess_side_effect=_subprocess),
    ):
        execute_sprint(config)

    phase1_ledger, _ = ledgers[0]
    phase2_ledger, phase2_available_at_entry = ledgers[1]

    # A reimbursement actually occurred in phase 1.
    assert phase1_ledger.reimbursed > 0

    # Phase 2's fresh ledger is unaffected: full budget at entry, no carryover.
    assert phase2_ledger is not phase1_ledger
    assert phase2_available_at_entry == 100 * counts[1]  # == 200
    assert phase2_ledger.initial_budget == 100 * counts[1]


# ---------------------------------------------------------------------------
# TM-8 (Integration, D-3 guard) — legacy phase after a task phase gets a fresh
# max_turns × 1 ledger
# ---------------------------------------------------------------------------


def test_legacy_phase_after_task_phase_has_fresh_ledger(tmp_path):
    """TM-8 (R-6, D-3): a legacy (freeform) phase following a task phase.

    The R-2 construction binds ``ledger`` for BOTH branches, so reaching the
    legacy fall-through after a task branch must NOT raise NameError and the
    legacy phase must get a fresh ``max_turns × 1`` ledger whose wiring hook runs.

    Asserts EXACTLY: no NameError is raised; the legacy phase gets a fresh
    max_turns × 1 ledger; and the wiring hook runs.
    """
    max_turns = 7  # max_turns × 1 == 7 is distinct from the task phase's 14
    # Phase 1: task phase (2 tasks). Phase 2: legacy freeform phase.
    p1 = tmp_path / "phase-1-tasklist.md"
    _write_task_phase_file(p1, 1, 2)
    p2 = tmp_path / "phase-2-tasklist.md"
    p2.write_text("# Phase 2: freeform legacy phase\n", encoding="utf-8")
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n", encoding="utf-8")
    config = SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[
            Phase(number=1, file=p1, name="Phase 1"),
            Phase(number=2, file=p2, name="Phase 2"),
        ],
        start_phase=1,
        end_phase=2,
        max_turns=max_turns,
        wiring_gate_mode="off",
        gate_rollout_mode="off",
    )

    def _task_subprocess(task, config, phase, prior_context=""):
        return (0, 3, 100)

    class _LegacyPopen:
        def __init__(self):
            self.returncode = 0
            self.pid = 7100
            self.stdin = None
            self._poll = 0

        def poll(self):
            self._poll += 1
            return None if self._poll <= 1 else 0

        def wait(self, timeout=None):
            self.returncode = 0
            return 0

    def _popen_factory(*args, **kwargs):
        legacy_phase = config.phases[1]
        config.results_dir.mkdir(parents=True, exist_ok=True)
        config.result_file(legacy_phase).write_text("EXIT_RECOMMENDATION: CONTINUE\n")
        config.output_file(legacy_phase).write_text("output phase 2\n")
        return _LegacyPopen()

    wiring_hook_phases: list[int] = []

    def _spy_wiring_hook(
        phase, config, phase_result, ledger=None, remediation_log=None
    ):
        # wiring_gate_mode="off" → the real hook is a passthrough; recording the
        # call here faithfully proves the executor invoked the wiring hook for
        # this phase (the legacy branch), and returns the result unchanged.
        wiring_hook_phases.append(phase.number)
        return phase_result

    captured = []
    logger = MagicMock()
    logger.write_summary = MagicMock(side_effect=lambda sr: captured.append(sr))

    with (
        _capture_ledgers() as ledgers,
        (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            )
        ),
        patch(
            "superclaude.cli.sprint.executor._run_task_subprocess",
            side_effect=_task_subprocess,
        ),
        patch(
            "superclaude.cli.pipeline.process.subprocess.Popen",
            side_effect=_popen_factory,
        ),
        patch("superclaude.cli.pipeline.process.os.setpgrp"),
        patch("superclaude.cli.sprint.notify._notify"),
        patch(
            "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
            side_effect=_spy_wiring_hook,
        ),
        patch("superclaude.cli.sprint.executor.SprintLogger", return_value=logger),
    ):
        # No NameError is raised reaching the legacy branch after a task branch.
        execute_sprint(config)

    # Two ledgers: phase 1 (task, 2×7=14) and phase 2 (legacy, 1×7=7).
    assert len(ledgers) == 2
    legacy_ledger, _ = ledgers[1]
    assert legacy_ledger.initial_budget == max_turns * 1  # fresh max_turns × 1

    # The wiring hook ran for the legacy phase (phase 2).
    assert 2 in wiring_hook_phases


# ---------------------------------------------------------------------------
# TM-9 (Integration, safety net) — single-phase overspend trips the gate
# ---------------------------------------------------------------------------


def test_single_task_overspend_trips_safety_net(tmp_path):
    """TM-9 (R-5): 1 phase × 3 tasks at max_turns=10, task 1 consumes 28.

    The per-phase pool is 10 × 3 = 30. Task 1 genuinely overspends WITHIN the
    phase (28 turns), draining the pool to 2 (< minimum_allocation), so the
    safety-net gate trips for tasks 2–3 — a real within-phase overspend, not a
    cross-phase ordering artifact.

    Asserts EXACTLY: task 1 PASS; tasks 2–3 SKIPPED; ``remaining`` is populated;
    and the phase result is ERROR.
    """
    config = _make_task_config(tmp_path, phase_task_counts=[3], max_turns=10)
    phase = config.phases[0]
    tasks = [TaskEntry(f"T01.0{i}", f"task {i}") for i in (1, 2, 3)]
    # Fresh per-phase ledger sized exactly as the executor sizes it (R-2).
    ledger = TurnLedger(initial_budget=config.max_turns * len(tasks))  # 30

    def _factory(task, config, phase):
        # Task 1 overspends this phase's OWN budget; the others would be cheap,
        # but the gate trips before they launch.
        return (0, 28 if task.task_id == "T01.01" else 5, 100)

    results, remaining, _ = execute_phase_tasks(
        tasks, config, phase, ledger=ledger, _subprocess_factory=_factory
    )

    by_id = {r.task.task_id: r.status for r in results}
    assert by_id["T01.01"] == TaskStatus.PASS
    assert by_id["T01.02"] == TaskStatus.SKIPPED
    assert by_id["T01.03"] == TaskStatus.SKIPPED

    # The gate populated `remaining` with the un-attempted tasks.
    assert remaining, "expected `remaining` to be populated on overspend"
    assert set(remaining) == {"T01.02", "T01.03"}

    # The phase result is ERROR: the executor maps a non-PASS aggregate to
    # PhaseStatus.ERROR (executor.py: status = PASS if aggregate=="PASS" else ERROR).
    report = aggregate_task_results(phase.number, results, remaining_task_ids=remaining)
    phase_status = PhaseStatus.PASS if report.status == "PASS" else PhaseStatus.ERROR
    assert phase_status == PhaseStatus.ERROR


# ---------------------------------------------------------------------------
# TM-10 (Integration, starvation impossibility) — heavy phase 1 cannot starve
# phase 2
# ---------------------------------------------------------------------------


def test_heavy_phase1_cannot_starve_phase2(tmp_path):
    """TM-10 (R-3/R-4): a heavy phase 1 that fully consumes its own pool.

    Phase 1 (3 tasks at max_turns=10 → pool 30) is driven so each task consumes
    exactly its full max_turns share, draining phase 1's pool to 0. Phase 2 then
    constructs a brand-new ledger, so it enters with the FULL max_turns × N₂
    budget — starvation is impossible by construction.

    Asserts EXACTLY: phase 2 enters with a full max_turns × N₂ budget (N₂ is
    phase 2's task count).
    """
    max_turns = 10
    counts = [3, 4]  # phase 1 pool 30; phase 2 pool 40
    config = _make_task_config(tmp_path, phase_task_counts=counts, max_turns=max_turns)

    def _subprocess(task, config, phase, prior_context=""):
        # Phase 1 tasks each consume the full per-task share → drains phase 1's
        # pool exactly to 0 across its 3 tasks (no skip; the gate never trips).
        return (0, max_turns if phase.number == 1 else 1, 100)

    with (
        _capture_ledgers() as ledgers,
        _drive_sprint(subprocess_side_effect=_subprocess),
    ):
        execute_sprint(config)

    phase1_ledger, _ = ledgers[0]
    phase2_ledger, phase2_available_at_entry = ledgers[1]

    # Precondition: phase 1 fully consumed its own pool.
    assert phase1_ledger.available() == 0, (
        f"phase 1 should be fully drained, available={phase1_ledger.available()}"
    )

    # Starvation impossibility: phase 2 enters with the FULL max_turns × N₂.
    assert phase2_available_at_entry == max_turns * counts[1]  # == 40
    assert phase2_ledger.initial_budget == max_turns * counts[1]


# ---------------------------------------------------------------------------
# TM-11 (Integration) — skip + python phases construct no ledger
# ---------------------------------------------------------------------------


def test_skip_and_python_phases_construct_no_ledger(tmp_path):
    """TM-11 (R-8): a sprint mixing a skip phase + a python phase + one task phase.

    python and skip phases ``continue`` BEFORE the R-2 construction site, so they
    allocate no ledger; only the task phase constructs one.

    Asserts EXACTLY: exactly one ``TurnLedger.__init__`` construction occurs (only
    the task phase) AND the skip phase records PhaseStatus.SKIPPED with
    exit_code=0. The pre-loop accumulator is a ``_SprintWiringTotals`` (NOT a
    TurnLedger), so the spy — which targets ``TurnLedger.__init__`` only — does
    not count it.
    """
    p1 = tmp_path / "phase-1-tasklist.md"
    p1.write_text("# Phase 1 (python, no tasks)\n", encoding="utf-8")
    p2 = tmp_path / "phase-2-tasklist.md"
    p2.write_text("# Phase 2 (skip)\n", encoding="utf-8")
    p3 = tmp_path / "phase-3-tasklist.md"
    _write_task_phase_file(p3, 3, 2)
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n", encoding="utf-8")
    config = SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[
            Phase(number=1, file=p1, name="Phase 1", execution_mode="python"),
            Phase(number=2, file=p2, name="Phase 2", execution_mode="skip"),
            Phase(number=3, file=p3, name="Phase 3", execution_mode="claude"),
        ],
        start_phase=1,
        end_phase=3,
        max_turns=10,
        wiring_gate_mode="off",
        gate_rollout_mode="off",
    )

    construct_count = [0]
    orig_init = TurnLedger.__init__

    def _counting_init(self, *args, **kwargs):
        construct_count[0] += 1
        orig_init(self, *args, **kwargs)

    def _task_subprocess(task, config, phase, prior_context=""):
        return (0, 3, 100)

    captured = []
    logger = MagicMock()
    logger.write_summary = MagicMock(side_effect=lambda sr: captured.append(sr))

    with (
        patch.object(TurnLedger, "__init__", _counting_init),
        patch(
            "superclaude.cli.sprint.executor.shutil.which",
            return_value="/usr/bin/claude",
        ),
        patch(
            "superclaude.cli.sprint.executor._run_task_subprocess",
            side_effect=_task_subprocess,
        ),
        patch("superclaude.cli.sprint.notify._notify"),
        patch("superclaude.cli.sprint.executor.SprintLogger", return_value=logger),
    ):
        # A sprint containing a SKIP phase exits non-zero: PhaseStatus.SKIPPED is
        # not in PhaseStatus.is_success, so the outcome is ERROR → SystemExit(1)
        # (executor.py outcome/exit logic). This is pre-existing skip-phase
        # behavior, orthogonal to TM-11's assertions; the TurnLedger.__init__ spy
        # and the captured SprintResult are both populated before the exit.
        with pytest.raises(SystemExit):
            execute_sprint(config)

    # Exactly one TurnLedger construction — only the task phase (phase 3).
    assert construct_count[0] == 1, (
        f"expected exactly 1 TurnLedger construction, got {construct_count[0]}"
    )

    # The skip phase recorded SKIPPED with exit_code 0.
    result = captured[0]
    skip_results = [pr for pr in result.phase_results if pr.phase.number == 2]
    assert len(skip_results) == 1
    assert skip_results[0].status == PhaseStatus.SKIPPED
    assert skip_results[0].exit_code == 0


# ---------------------------------------------------------------------------
# TM-13 (Integration, D-4/R-10 guard, OQ-1 Position A PINNED) —
# sprint-cumulative wiring totals in the KPI report
# ---------------------------------------------------------------------------


def _parse_kpi_int(content: str, label: str) -> int:
    """Extract the integer following ``label`` in a gate-kpi-report.md line."""
    for line in content.splitlines():
        if label in line:
            return int(line.rsplit(maxsplit=1)[-1])
    raise AssertionError(f"label {label!r} not found in KPI report:\n{content}")


def test_kpi_wiring_totals_accumulate_across_phases(tmp_path):
    """TM-13 (R-10, D-4, C3 — OQ-1 Position A PINNED): sprint-cumulative wiring KPI.

    A 2-phase sprint where phase 1 runs 3 wiring analyses and phase 2 runs 2. The
    per-phase wiring hook is replaced with a deterministic stub that bumps each
    phase's FRESH ledger (debit_wiring once per analysis, plus a credit), so the
    counts are pinned. The REAL code under test is the R-10 chain: the two
    add-sites sum each phase's wiring fields into the sprint accumulator, and the
    accumulator (NOT the last-phase ledger) is passed to build_kpi_report and
    persisted to gate-kpi-report.md.

    Asserts EXACTLY: the persisted gate-kpi-report.md reports
    ``wiring_analyses_run == 5`` (sprint-cumulative, 3+2 — a SINGLE pinned value,
    no Position B branch) AND ``wiring_turns_used`` / ``wiring_turns_credited``
    are the sprint-cumulative sums, NOT last-phase-only.
    """
    config = _make_task_config(tmp_path, phase_task_counts=[2, 2], max_turns=100)

    analyses_by_phase = {1: 3, 2: 2}

    def _subprocess(task, config, phase, prior_context=""):
        return (0, 3, 100)

    def _phase_wiring_hook(
        phase, config, phase_result, ledger=None, remediation_log=None
    ):
        # Deterministically register this phase's wiring analyses on its OWN fresh
        # per-phase ledger. debit_wiring bumps wiring_turns_used + wiring_analyses_count;
        # credit_wiring(5) credits int(5*0.8)=4 into wiring_turns_credited.
        for _ in range(analyses_by_phase.get(phase.number, 0)):
            ledger.debit_wiring(1)
            ledger.credit_wiring(5)
        return phase_result

    with _drive_sprint(
        subprocess_side_effect=_subprocess, phase_wiring_hook=_phase_wiring_hook
    ):
        execute_sprint(config)

    kpi_path = config.results_dir / "gate-kpi-report.md"
    assert kpi_path.exists(), f"expected gate-kpi-report.md at {kpi_path}"
    content = kpi_path.read_text()

    # Sprint-cumulative analyses run == 3 + 2 == 5 (the single pinned value).
    assert _parse_kpi_int(content, "Analyses run:") == 5

    # Turns used/credited are the sprint-cumulative sums, NOT last-phase-only.
    # used: 3 + 2 == 5 (last-phase-only would be 2); credited: 12 + 8 == 20
    # (per analysis credit_wiring(5) == int(5*0.8) == 4; last-phase-only would be 8).
    used = _parse_kpi_int(content, "Turns used:")
    credited = _parse_kpi_int(content, "Turns credited:")
    assert used == 5, f"expected sprint-cumulative turns used 5, got {used}"
    assert used != 2, "regression: KPI reported last-phase-only wiring turns used"
    assert credited == 20, (
        f"expected sprint-cumulative turns credited 20, got {credited}"
    )
    assert credited != 8, "regression: KPI reported last-phase-only turns credited"


# ---------------------------------------------------------------------------
# TM-14 (Integration, OQ-2 resume-parity) — resume window sizes the phase
# identically
# ---------------------------------------------------------------------------


def test_resume_window_sizes_phase_identically(tmp_path):
    """TM-14 (OQ-2 hybrid): the same phase reached via a full run and a resume window.

    The per-phase pool is sized ``max_turns × len(tasks)`` from
    ``_parse_phase_tasks`` — independent of ``len(active_phases)`` AND of resume
    state. Run (a) is a full run; run (b) is a ``--resume`` partial window where
    the first task is a validated-success skip (``turns_consumed=0``, no debit).

    Asserts EXACTLY: the phase's ``initial_budget == max_turns × len(tasks)`` is
    IDENTICAL in both runs AND the over-provisioned pool never starves and never
    trips the gate spuriously.
    """
    max_turns = 100
    num_tasks = 3

    def _build(subdir: str, resume_task_id: str = "") -> SprintConfig:
        d = tmp_path / subdir
        d.mkdir()
        pf = d / "phase-1-tasklist.md"
        _write_task_phase_file(pf, 1, num_tasks)
        index = d / "tasklist-index.md"
        index.write_text("index\n", encoding="utf-8")
        return SprintConfig(
            index_path=index,
            release_dir=d,
            phases=[Phase(number=1, file=pf, name="Phase 1")],
            start_phase=1,
            end_phase=1,
            max_turns=max_turns,
            wiring_gate_mode="off",
            gate_rollout_mode="off",
            resume_task_id=resume_task_id,
        )

    def _subprocess(task, config, phase, prior_context=""):
        return (0, 3, 100)

    # (a) Full run — all three tasks execute.
    full_cfg = _build("full")
    with (
        _capture_ledgers() as full_ledgers,
        _drive_sprint(subprocess_side_effect=_subprocess),
    ):
        execute_sprint(full_cfg)
    full_budget = full_ledgers[0][0].initial_budget

    # (b) Resume window — T01.01 is a validated-success skip (no debit).
    resume_cfg = _build("resume", resume_task_id="T01.01")
    store = FileHandoffStore(resume_cfg)
    store.write(
        HandoffRecord(
            task_id="T01.01",
            phase=1,
            status=TaskStatus.PASS.value,
            gate_outcome=GateOutcome.PASS.value,
            turns_consumed=4,
            exit_code=0,
            output_path="/r/T01.01.txt",
        ),
        phase=resume_cfg.phases[0],
        task=TaskEntry("T01.01", "First"),
    )

    with (
        _capture_ledgers() as resume_ledgers,
        _drive_sprint(subprocess_side_effect=_subprocess) as captured,
    ):
        execute_sprint(resume_cfg)
    resume_budget = resume_ledgers[0][0].initial_budget
    result = captured[0]

    # Identical sizing in both runs: max_turns × len(tasks), independent of resume
    # and of len(active_phases).
    assert full_budget == max_turns * num_tasks  # == 300
    assert resume_budget == max_turns * num_tasks  # == 300
    assert full_budget == resume_budget

    # The over-provisioned resume pool never starves / never trips the gate
    # spuriously: no task is SKIPPED due to budget.
    budget_skipped = [
        tr
        for pr in result.phase_results
        for tr in pr.task_results
        if tr.status == TaskStatus.SKIPPED
    ]
    assert budget_skipped == [], "resume pool spuriously tripped the budget gate"
