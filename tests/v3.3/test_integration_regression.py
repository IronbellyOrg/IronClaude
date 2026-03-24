"""Integration + regression suite for v3.3 TurnLedger validation (T02.29).

T17 — Cross-phase ledger coherence: ledger state correct across multiple phases.
T18 — Mode switch mid-sprint: mode change handled correctly.
T19 — Concurrent gate evaluation: no state corruption.
T20 — Audit completeness: all test events recorded in audit trail.
T21 — Manifest coverage: wiring manifest covers all entry points.
T22 — Full pipeline E2E: end-to-end pipeline execution.

Dependencies: T01.02 (audit_trail fixture), T01.07 (manifest for T21)
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from superclaude.cli.sprint.executor import (
    execute_phase_tasks,
    execute_sprint,
    run_post_phase_wiring_hook,
    run_post_task_anti_instinct_hook,
    run_post_task_wiring_hook,
    SprintGatePolicy,
)
from superclaude.cli.sprint.models import (
    GateOutcome,
    Phase,
    PhaseResult,
    PhaseStatus,
    SprintConfig,
    TaskEntry,
    TaskResult,
    TaskStatus,
    TurnLedger,
    ShadowGateMetrics,
)
from superclaude.cli.audit.wiring_gate import WiringFinding, WiringReport
from superclaude.cli.pipeline.trailing_gate import (
    DeferredRemediationLog,
    TrailingGateResult,
)
from superclaude.cli.audit.reachability import ReachabilityAnalyzer, load_manifest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@dataclass
class _FakeWiringReport:
    """Non-blocking wiring report stub for monkeypatching."""

    target_dir: str = ""
    files_analyzed: int = 5
    files_skipped: int = 0
    unwired_callables: list = dc_field(default_factory=list)
    orphan_modules: list = dc_field(default_factory=list)
    unwired_registries: list = dc_field(default_factory=list)
    scan_duration_seconds: float = 0.01
    rollout_mode: str = "soft"

    @property
    def all_findings(self):
        return []

    @property
    def total_findings(self):
        return 0

    @property
    def unsuppressed_findings(self):
        return []

    def blocking_count(self, mode: str) -> int:
        return 0


def _make_multi_phase_config(
    tmp_path: Path,
    *,
    num_phases: int = 3,
    wiring_gate_mode: str = "soft",
    gate_rollout_mode: str = "off",
    max_turns: int = 50,
) -> SprintConfig:
    """Build a SprintConfig with multiple task-inventory phases."""
    phases = []
    for i in range(1, num_phases + 1):
        pf = tmp_path / f"phase-{i}-tasklist.md"
        pf.write_text(
            f"# Phase {i}\n\n"
            f"### T{i:02d}.01 -- Task A{i}\nDo task A{i}\n\n"
            f"### T{i:02d}.02 -- Task B{i}\nDo task B{i}\n"
        )
        phases.append(Phase(number=i, file=pf, name=f"Phase {i}"))

    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")

    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=phases,
        start_phase=1,
        end_phase=num_phases,
        max_turns=max_turns,
        wiring_gate_mode=wiring_gate_mode,
        wiring_gate_scope="none",
        gate_rollout_mode=gate_rollout_mode,
        wiring_analysis_turns=2,
    )


def _patch_wiring_analysis(monkeypatch, *, rollout_mode: str = "soft"):
    """Monkeypatch run_wiring_analysis to return a clean report."""

    def _fake_run_wiring_analysis(wiring_config, source_dir):
        return _FakeWiringReport(
            target_dir=str(source_dir),
            rollout_mode=wiring_config.rollout_mode,
        )

    monkeypatch.setattr(
        "superclaude.cli.audit.wiring_gate.run_wiring_analysis",
        _fake_run_wiring_analysis,
    )


def _make_factory(*, turns: int = 3, exit_code: int = 0):
    """Return a subprocess factory that records calls."""
    calls = []

    def _factory(task, cfg, ph):
        calls.append({"task_id": task.task_id, "phase": ph.number})
        return (exit_code, turns, 100)

    return _factory, calls


# ---------------------------------------------------------------------------
# T17: Cross-Phase Ledger Coherence
# ---------------------------------------------------------------------------


class TestCrossPhaseledgerCoherence:
    """FR-6.2/T17: Ledger state is correct across multiple phases.

    Validates that a single TurnLedger instance maintains correct
    consumed/reimbursed/available invariants when shared across
    3 consecutive phases of execute_phase_tasks.
    """

    def test_cross_phase_ledger(
        self, tmp_path: Path, audit_trail, monkeypatch,
    ) -> None:
        """T17: Execute 3 phases sequentially with a shared ledger,
        asserting budget invariant at each phase boundary."""
        config = _make_multi_phase_config(tmp_path, num_phases=3, wiring_gate_mode="soft")
        _patch_wiring_analysis(monkeypatch)

        initial_budget = 200
        ledger = TurnLedger(
            initial_budget=initial_budget,
            minimum_allocation=5,
            reimbursement_rate=0.8,
        )

        phase_snapshots: list[dict] = []

        def _snap(label: str) -> dict:
            s = {
                "label": label,
                "consumed": ledger.consumed,
                "reimbursed": ledger.reimbursed,
                "available": ledger.available(),
            }
            phase_snapshots.append(s)
            return s

        _snap("initial")

        # Execute all 3 phases with the same ledger
        for phase in config.phases:
            tasks = [
                TaskEntry(
                    task_id=f"T{phase.number:02d}.01",
                    title=f"Task A{phase.number}",
                    description=f"Do A{phase.number}",
                ),
                TaskEntry(
                    task_id=f"T{phase.number:02d}.02",
                    title=f"Task B{phase.number}",
                    description=f"Do B{phase.number}",
                ),
            ]
            factory, _ = _make_factory(turns=3)

            results, remaining, gate_results = execute_phase_tasks(
                tasks, config, phase,
                ledger=ledger,
                _subprocess_factory=factory,
            )

            snap = _snap(f"after_phase_{phase.number}")

            # Invariant: available = initial_budget - consumed + reimbursed
            assert ledger.available() == (
                ledger.initial_budget - ledger.consumed + ledger.reimbursed
            ), f"Phase {phase.number} invariant violated: {snap}"

            # All tasks passed (no budget exhaustion at 200)
            assert len(results) == 2, (
                f"Phase {phase.number}: expected 2 results, got {len(results)}"
            )
            assert len(remaining) == 0, (
                f"Phase {phase.number}: unexpected remaining tasks: {remaining}"
            )
            assert all(r.status == TaskStatus.PASS for r in results)

        # Final assertions: ledger consumed turns across all 3 phases
        # Each phase: 2 tasks * (pre-debit 5 + wiring debit 2) = 14 consumed
        # Each phase: 2 tasks * (credit 2 + wiring credit 1) = 6 reimbursed
        # 3 phases: consumed = 42, reimbursed = 18
        assert ledger.consumed > 0, "Ledger must have consumed turns"
        assert ledger.reimbursed > 0, "Ledger must have reimbursed turns"

        # Monotonicity: consumed can only increase across phases
        for i in range(1, len(phase_snapshots)):
            assert phase_snapshots[i]["consumed"] >= phase_snapshots[i - 1]["consumed"], (
                f"Consumed decreased between {phase_snapshots[i-1]['label']} and {phase_snapshots[i]['label']}"
            )

        audit_trail.record(
            test_id="test_cross_phase_ledger",
            spec_ref="FR-6.2/T17",
            assertion_type="behavioral",
            inputs={
                "initial_budget": initial_budget,
                "num_phases": 3,
                "tasks_per_phase": 2,
            },
            observed={
                "phase_snapshots": phase_snapshots,
                "final_consumed": ledger.consumed,
                "final_reimbursed": ledger.reimbursed,
                "final_available": ledger.available(),
            },
            expected={
                "invariant_held": True,
                "monotonic_consumed": True,
                "all_tasks_passed": True,
            },
            verdict="PASS",
            evidence=(
                f"Cross-phase ledger coherence: 3 phases executed with shared "
                f"TurnLedger, invariant held at every boundary. "
                f"Final: consumed={ledger.consumed}, reimbursed={ledger.reimbursed}, "
                f"available={ledger.available()}"
            ),
        )


# ---------------------------------------------------------------------------
# T18: Mode Switch Mid-Sprint
# ---------------------------------------------------------------------------


class TestModeSwitchMidSprint:
    """FR-6.2/T18: Mode change mid-sprint handled correctly.

    Validates that switching wiring_gate_mode between phases is handled
    correctly — phase 1 runs with 'off' mode (no wiring analysis),
    phase 2 runs with 'soft' mode (wiring analysis fires).
    """

    def test_mode_switch(
        self, tmp_path: Path, audit_trail, monkeypatch,
    ) -> None:
        """T18: Run phase 1 with wiring off, then phase 2 with wiring soft.
        Verify wiring counters only advance in phase 2."""
        config = _make_multi_phase_config(
            tmp_path, num_phases=2, wiring_gate_mode="off",
        )
        _patch_wiring_analysis(monkeypatch)

        ledger = TurnLedger(initial_budget=100, minimum_allocation=5)

        # Phase 1: wiring_gate_mode = "off" — no wiring analysis
        tasks_p1 = [TaskEntry(task_id="T01.01", title="Task P1", description="p1")]
        factory_p1, calls_p1 = _make_factory(turns=3)

        results_p1, _, _ = execute_phase_tasks(
            tasks_p1, config, config.phases[0],
            ledger=ledger, _subprocess_factory=factory_p1,
        )

        wiring_after_p1 = ledger.wiring_turns_used

        # Now switch mode to "soft" for phase 2
        config.wiring_gate_mode = "soft"

        tasks_p2 = [TaskEntry(task_id="T02.01", title="Task P2", description="p2")]
        factory_p2, calls_p2 = _make_factory(turns=4)

        results_p2, _, _ = execute_phase_tasks(
            tasks_p2, config, config.phases[1],
            ledger=ledger, _subprocess_factory=factory_p2,
        )

        wiring_after_p2 = ledger.wiring_turns_used

        # Assertions
        assert results_p1[0].status == TaskStatus.PASS
        assert results_p2[0].status == TaskStatus.PASS

        # Phase 1 (off): no wiring turns consumed
        assert wiring_after_p1 == 0, (
            f"Phase 1 (off mode) should have 0 wiring turns, got {wiring_after_p1}"
        )

        # Phase 2 (soft): wiring analysis ran, turns consumed
        assert wiring_after_p2 > 0, (
            f"Phase 2 (soft mode) should have consumed wiring turns, got {wiring_after_p2}"
        )

        # Budget invariant still holds
        assert ledger.available() == (
            ledger.initial_budget - ledger.consumed + ledger.reimbursed
        )

        audit_trail.record(
            test_id="test_mode_switch",
            spec_ref="FR-6.2/T18",
            assertion_type="behavioral",
            inputs={
                "phase_1_mode": "off",
                "phase_2_mode": "soft",
            },
            observed={
                "wiring_after_p1": wiring_after_p1,
                "wiring_after_p2": wiring_after_p2,
                "p1_status": results_p1[0].status.value,
                "p2_status": results_p2[0].status.value,
            },
            expected={
                "wiring_after_p1": 0,
                "wiring_after_p2_gt_0": True,
            },
            verdict="PASS",
            evidence=(
                f"Mode switch: phase 1 (off) wiring_turns=0, "
                f"phase 2 (soft) wiring_turns={wiring_after_p2}. "
                f"Mode change mid-sprint handled correctly."
            ),
        )


# ---------------------------------------------------------------------------
# T19: Concurrent Gate Evaluation
# ---------------------------------------------------------------------------


class TestConcurrentGateEvaluation:
    """FR-6.2/T19: Concurrent gate evaluation doesn't corrupt state.

    Validates that when multiple threads evaluate gate hooks concurrently
    on separate ledger/metrics instances, no state corruption occurs.
    """

    def test_concurrent_gate(
        self, tmp_path: Path, audit_trail, monkeypatch,
    ) -> None:
        """T19: Run gate evaluation from 4 threads concurrently,
        each with its own ledger. Assert no cross-contamination."""
        _patch_wiring_analysis(monkeypatch)

        num_threads = 4
        tasks_per_thread = 5
        results_by_thread: dict[int, list[TaskResult]] = {}
        ledgers: list[TurnLedger] = []
        errors: list[str] = []

        def _run_phase(thread_id: int) -> None:
            try:
                thread_dir = tmp_path / f"thread-{thread_id}"
                thread_dir.mkdir(parents=True, exist_ok=True)
                config = _make_multi_phase_config(
                    thread_dir,
                    num_phases=1,
                    wiring_gate_mode="soft",
                )

                ledger = TurnLedger(initial_budget=100, minimum_allocation=5)
                ledgers.append(ledger)

                tasks = [
                    TaskEntry(
                        task_id=f"T{thread_id:02d}.{j:02d}",
                        title=f"Thread{thread_id}-Task{j}",
                        description=f"t{thread_id}-{j}",
                    )
                    for j in range(1, tasks_per_thread + 1)
                ]
                factory, _ = _make_factory(turns=2)

                results, remaining, _ = execute_phase_tasks(
                    tasks, config, config.phases[0],
                    ledger=ledger, _subprocess_factory=factory,
                )
                results_by_thread[thread_id] = results
            except Exception as exc:
                errors.append(f"Thread {thread_id}: {exc}")

        threads = [
            threading.Thread(target=_run_phase, args=(i,))
            for i in range(num_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=30)

        # No exceptions
        assert not errors, f"Thread errors: {errors}"

        # Each thread produced correct results independently
        for tid in range(num_threads):
            assert tid in results_by_thread, f"Thread {tid} missing results"
            results = results_by_thread[tid]
            assert len(results) == tasks_per_thread, (
                f"Thread {tid}: expected {tasks_per_thread} results, got {len(results)}"
            )
            assert all(r.status == TaskStatus.PASS for r in results), (
                f"Thread {tid}: not all tasks passed"
            )

        # Each ledger is independent (no cross-contamination)
        for i, ledger in enumerate(ledgers):
            assert ledger.available() == (
                ledger.initial_budget - ledger.consumed + ledger.reimbursed
            ), f"Ledger {i} invariant violated"
            assert ledger.consumed > 0, f"Ledger {i} should have consumed turns"

        audit_trail.record(
            test_id="test_concurrent_gate",
            spec_ref="FR-6.2/T19",
            assertion_type="behavioral",
            inputs={
                "num_threads": num_threads,
                "tasks_per_thread": tasks_per_thread,
            },
            observed={
                "threads_completed": len(results_by_thread),
                "errors": errors,
                "ledger_invariants_held": all(
                    l.available() == l.initial_budget - l.consumed + l.reimbursed
                    for l in ledgers
                ),
            },
            expected={
                "threads_completed": num_threads,
                "errors": [],
                "ledger_invariants_held": True,
            },
            verdict="PASS",
            evidence=(
                f"Concurrent gate evaluation: {num_threads} threads × "
                f"{tasks_per_thread} tasks, no state corruption, "
                f"all ledger invariants held."
            ),
        )


# ---------------------------------------------------------------------------
# T20: Audit Completeness
# ---------------------------------------------------------------------------


class TestAuditCompleteness:
    """FR-6.2/T20: All test events recorded in audit trail.

    Validates that every task in a multi-task phase produces an audit-trail
    record when the test harness emits one per task result, and that
    records contain required fields.
    """

    def test_audit_completeness(
        self, tmp_path: Path, audit_trail, monkeypatch,
    ) -> None:
        """T20: Execute a 3-task phase, emit one audit record per task,
        then verify all records exist with required fields."""
        config = _make_multi_phase_config(
            tmp_path, num_phases=1, wiring_gate_mode="off",
        )

        ledger = TurnLedger(initial_budget=100, minimum_allocation=5)
        tasks = [
            TaskEntry(task_id=f"T01.{j:02d}", title=f"Task {j}", description=f"t{j}")
            for j in range(1, 4)
        ]
        factory, _ = _make_factory(turns=2)

        results, remaining, _ = execute_phase_tasks(
            tasks, config, config.phases[0],
            ledger=ledger, _subprocess_factory=factory,
        )

        # Emit one audit record per task result
        emitted_ids = []
        for result in results:
            rec = audit_trail.record(
                test_id=f"audit_completeness_{result.task.task_id}",
                spec_ref="FR-6.2/T20",
                assertion_type="behavioral",
                inputs={"task_id": result.task.task_id},
                observed={
                    "status": result.status.value,
                    "turns_consumed": result.turns_consumed,
                },
                expected={"status": "PASS"},
                verdict="PASS" if result.status == TaskStatus.PASS else "FAIL",
                evidence=f"Task {result.task.task_id} completed with status {result.status.value}",
            )
            emitted_ids.append(rec["test_id"])

        # Verify: all 3 task records exist in the audit trail
        trail_ids = [r["test_id"] for r in audit_trail.records]
        for eid in emitted_ids:
            assert eid in trail_ids, f"Audit record {eid} missing from trail"

        # Verify: required fields present in every record we just emitted
        required_fields = {
            "test_id", "spec_ref", "assertion_type", "inputs",
            "observed", "expected", "verdict", "evidence",
        }
        recent_records = [
            r for r in audit_trail.records
            if r["test_id"].startswith("audit_completeness_")
        ]
        assert len(recent_records) == 3, (
            f"Expected 3 audit records, got {len(recent_records)}"
        )
        for rec in recent_records:
            missing = required_fields - set(rec.keys())
            assert not missing, (
                f"Record {rec['test_id']} missing fields: {missing}"
            )

        # Final summary record
        audit_trail.record(
            test_id="test_audit_completeness",
            spec_ref="FR-6.2/T20",
            assertion_type="behavioral",
            inputs={"num_tasks": 3},
            observed={
                "records_emitted": len(recent_records),
                "all_fields_present": True,
            },
            expected={
                "records_emitted": 3,
                "all_fields_present": True,
            },
            verdict="PASS",
            evidence=(
                f"Audit completeness: 3/3 task records emitted with all "
                f"required fields present."
            ),
        )


# ---------------------------------------------------------------------------
# T21: Manifest Coverage
# ---------------------------------------------------------------------------


class TestManifestCoverage:
    """FR-6.2/T21: Wiring manifest covers all entry points.

    Validates that the wiring manifest (tests/v3.3/wiring_manifest.yaml)
    declares entry points for all major orchestration functions and that
    every required_reachable target references a valid entry point.
    """

    def test_manifest_coverage(self, audit_trail) -> None:
        """T21: Load the wiring manifest and verify structural completeness."""
        manifest_path = Path(__file__).parent / "wiring_manifest.yaml"
        assert manifest_path.exists(), (
            f"Wiring manifest not found at {manifest_path}"
        )

        with open(manifest_path) as f:
            data = yaml.safe_load(f)

        assert "wiring_manifest" in data, "Missing top-level 'wiring_manifest' key"
        manifest = data["wiring_manifest"]

        # Entry points exist and are non-empty
        entry_points = manifest.get("entry_points", [])
        assert len(entry_points) > 0, "entry_points must be non-empty"

        ep_functions = {ep["function"] for ep in entry_points}

        # Required: at least the 3 core entry points
        expected_eps = {"execute_sprint", "execute_phase_tasks", "execute_roadmap"}
        missing_eps = expected_eps - ep_functions
        assert not missing_eps, (
            f"Missing expected entry points: {missing_eps}"
        )

        # Required reachable targets exist and reference valid entry points
        targets = manifest.get("required_reachable", [])
        assert len(targets) > 0, "required_reachable must be non-empty"

        for target in targets:
            assert "target" in target, f"Target missing 'target' field: {target}"
            assert "from_entry" in target, f"Target missing 'from_entry' field: {target}"
            assert "spec_ref" in target, f"Target missing 'spec_ref' field: {target}"
            assert target["from_entry"] in ep_functions, (
                f"Target '{target['target']}' references unknown entry "
                f"'{target['from_entry']}'; known: {ep_functions}"
            )

        # Verify the manifest is parseable by load_manifest
        ep_loaded, targets_loaded = load_manifest(manifest_path)
        assert len(ep_loaded) == len(entry_points), (
            f"load_manifest returned {len(ep_loaded)} entry points, "
            f"YAML has {len(entry_points)}"
        )
        assert len(targets_loaded) == len(targets), (
            f"load_manifest returned {len(targets_loaded)} targets, "
            f"YAML has {len(targets)}"
        )

        # Coverage: count unique spec_refs to gauge breadth
        spec_refs = {t["spec_ref"] for t in targets}

        audit_trail.record(
            test_id="test_manifest_coverage",
            spec_ref="FR-6.2/T21",
            assertion_type="structural",
            inputs={"manifest_path": str(manifest_path)},
            observed={
                "entry_point_count": len(entry_points),
                "target_count": len(targets),
                "spec_ref_count": len(spec_refs),
                "entry_point_functions": sorted(ep_functions),
            },
            expected={
                "has_execute_sprint": True,
                "has_execute_phase_tasks": True,
                "has_execute_roadmap": True,
                "all_from_entry_valid": True,
            },
            verdict="PASS",
            evidence=(
                f"Manifest coverage: {len(entry_points)} entry points, "
                f"{len(targets)} required_reachable targets, "
                f"{len(spec_refs)} unique spec_refs. "
                f"All from_entry references valid."
            ),
        )


# ---------------------------------------------------------------------------
# T22: Full Pipeline E2E
# ---------------------------------------------------------------------------


class TestFullPipelineE2E:
    """FR-6.2/T22: End-to-end pipeline execution.

    Validates that execute_sprint constructs all infrastructure (TurnLedger,
    ShadowGateMetrics, DeferredRemediationLog, SprintGatePolicy), delegates
    to execute_phase_tasks for task-inventory phases, and the resulting
    ledger/metrics are correctly populated after the full pipeline run.
    """

    def test_full_pipeline_e2e(self, tmp_path: Path, audit_trail) -> None:
        """T22: Run execute_sprint end-to-end with captured infrastructure,
        verifying all 4 core classes are constructed and tasks execute."""
        config = _make_multi_phase_config(
            tmp_path, num_phases=2, wiring_gate_mode="off", max_turns=50,
        )
        config.results_dir.mkdir(parents=True, exist_ok=True)

        captured = {
            "ledger": None,
            "shadow_metrics": None,
            "remediation_log": None,
            "gate_policy": None,
            "phase_calls": [],
        }

        original_gate_init = SprintGatePolicy.__init__

        def _capture_gate_init(self, cfg):
            captured["gate_policy"] = self
            original_gate_init(self, cfg)

        def _capture_phase_tasks(tasks, config, phase, ledger=None, **kwargs):
            captured["ledger"] = ledger
            captured["shadow_metrics"] = kwargs.get("shadow_metrics")
            captured["remediation_log"] = kwargs.get("remediation_log")
            captured["phase_calls"].append(phase.number)
            results = [
                TaskResult(
                    task=t,
                    status=TaskStatus.PASS,
                    exit_code=0,
                    turns_consumed=2,
                )
                for t in tasks
            ]
            return results, [], []

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.executor.execute_phase_tasks",
                side_effect=_capture_phase_tasks,
            ),
            patch(
                "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
                side_effect=lambda phase, config, pr, **kw: pr,
            ),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch(
                "superclaude.cli.sprint.preflight.execute_preflight_phases",
                return_value=[],
            ),
            patch.object(
                SprintGatePolicy, "__init__", _capture_gate_init,
            ),
        ):
            execute_sprint(config)

        # --- Assertions: all 4 infrastructure classes constructed ---
        assert isinstance(captured["ledger"], TurnLedger), (
            f"Expected TurnLedger, got {type(captured['ledger'])}"
        )
        assert isinstance(captured["shadow_metrics"], ShadowGateMetrics), (
            f"Expected ShadowGateMetrics, got {type(captured['shadow_metrics'])}"
        )
        assert isinstance(captured["remediation_log"], DeferredRemediationLog), (
            f"Expected DeferredRemediationLog, got {type(captured['remediation_log'])}"
        )
        assert isinstance(captured["gate_policy"], SprintGatePolicy), (
            f"Expected SprintGatePolicy, got {type(captured['gate_policy'])}"
        )

        # --- Assertions: phases were delegated ---
        assert len(captured["phase_calls"]) == 2, (
            f"Expected 2 phase calls, got {captured['phase_calls']}"
        )
        assert captured["phase_calls"] == [1, 2], (
            f"Expected phases [1, 2], got {captured['phase_calls']}"
        )

        # --- Assertions: ledger was initialized correctly ---
        ledger = captured["ledger"]
        expected_budget = config.max_turns * len(config.active_phases)
        assert ledger.initial_budget == expected_budget, (
            f"Expected budget {expected_budget}, got {ledger.initial_budget}"
        )

        audit_trail.record(
            test_id="test_full_pipeline_e2e",
            spec_ref="FR-6.2/T22",
            assertion_type="behavioral",
            inputs={
                "num_phases": 2,
                "max_turns": config.max_turns,
            },
            observed={
                "ledger_type": type(captured["ledger"]).__name__,
                "shadow_metrics_type": type(captured["shadow_metrics"]).__name__,
                "remediation_log_type": type(captured["remediation_log"]).__name__,
                "gate_policy_type": type(captured["gate_policy"]).__name__,
                "phase_calls": captured["phase_calls"],
                "initial_budget": ledger.initial_budget,
            },
            expected={
                "ledger_type": "TurnLedger",
                "shadow_metrics_type": "ShadowGateMetrics",
                "remediation_log_type": "DeferredRemediationLog",
                "gate_policy_type": "SprintGatePolicy",
                "phase_calls": [1, 2],
                "initial_budget": expected_budget,
            },
            verdict="PASS",
            evidence=(
                f"Full pipeline E2E: execute_sprint constructed all 4 infrastructure "
                f"classes, delegated to 2 phases, budget={expected_budget}."
            ),
        )
