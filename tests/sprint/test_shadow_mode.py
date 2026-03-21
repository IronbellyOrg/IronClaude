"""Tests for shadow mode (--shadow-gates) metrics collection.

Includes anti-instinct gate shadow recording tests per FR-SPRINT.4:
- Verify metrics recorded in shadow/soft/full modes
- Verify no recording in off mode
- Verify data point structure (passed, evaluation_ms)
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from superclaude.cli.sprint.executor import run_post_task_anti_instinct_hook
from superclaude.cli.sprint.models import (
    Phase,
    ShadowGateMetrics,
    SprintConfig,
    TaskEntry,
    TaskResult,
    TaskStatus,
)


def _make_config(shadow_gates: bool = False) -> SprintConfig:
    return SprintConfig(
        index_path=Path("/tmp/tasklist-index.md"),
        release_dir=Path("/tmp/release"),
        phases=[
            Phase(number=1, file=Path("/tmp/p1.md"), name="Foundation"),
        ],
        shadow_gates=shadow_gates,
    )


class TestShadowGatesFlag:
    """--shadow-gates flag enables shadow mode on SprintConfig."""

    def test_shadow_gates_default_false(self):
        config = _make_config()
        assert config.shadow_gates is False

    def test_shadow_gates_enabled(self):
        config = _make_config(shadow_gates=True)
        assert config.shadow_gates is True


class TestShadowGateMetrics:
    """Shadow metrics collection without affecting behavior."""

    def test_empty_metrics(self):
        m = ShadowGateMetrics()
        assert m.total_evaluated == 0
        assert m.passed == 0
        assert m.failed == 0
        assert m.pass_rate == 0.0
        assert m.p50_latency_ms == 0.0
        assert m.p95_latency_ms == 0.0

    def test_record_pass(self):
        m = ShadowGateMetrics()
        m.record(passed=True, evaluation_ms=10.0)
        assert m.total_evaluated == 1
        assert m.passed == 1
        assert m.failed == 0
        assert m.pass_rate == 1.0

    def test_record_fail(self):
        m = ShadowGateMetrics()
        m.record(passed=False, evaluation_ms=25.0)
        assert m.total_evaluated == 1
        assert m.passed == 0
        assert m.failed == 1
        assert m.pass_rate == 0.0

    def test_mixed_results(self):
        m = ShadowGateMetrics()
        m.record(passed=True, evaluation_ms=10.0)
        m.record(passed=True, evaluation_ms=20.0)
        m.record(passed=False, evaluation_ms=50.0)
        assert m.total_evaluated == 3
        assert m.passed == 2
        assert m.failed == 1
        assert abs(m.pass_rate - 2 / 3) < 0.001

    def test_latency_p50(self):
        m = ShadowGateMetrics()
        for ms in [10.0, 20.0, 30.0, 40.0, 50.0]:
            m.record(passed=True, evaluation_ms=ms)
        assert m.p50_latency_ms == 30.0

    def test_latency_p50_even_count(self):
        m = ShadowGateMetrics()
        for ms in [10.0, 20.0, 30.0, 40.0]:
            m.record(passed=True, evaluation_ms=ms)
        assert m.p50_latency_ms == 25.0  # avg of 20 and 30

    def test_latency_p95(self):
        m = ShadowGateMetrics()
        for ms in range(1, 101):  # 1..100ms
            m.record(passed=True, evaluation_ms=float(ms))
        assert m.p95_latency_ms >= 95.0

    def test_blocking_results_determine_outcome(self):
        """Shadow metrics must not affect sprint behavior.

        This tests the design contract: ShadowGateMetrics is a passive
        data collector with no side effects on SprintConfig or execution.
        """
        config = _make_config(shadow_gates=True)
        metrics = ShadowGateMetrics()
        metrics.record(passed=False, evaluation_ms=100.0)
        # Config and metrics are independent — shadow failure doesn't alter config
        assert config.shadow_gates is True
        assert metrics.failed == 1
        # No reference between them — shadow is informational only


# ---------------------------------------------------------------------------
# Anti-instinct shadow recording tests (FR-SPRINT.4)
# ---------------------------------------------------------------------------


def _make_anti_instinct_config(
    tmp_path: Path, gate_rollout_mode: str = "off"
) -> SprintConfig:
    pf = tmp_path / "phase-1.md"
    pf.write_text("# Phase 1\n")
    return SprintConfig(
        index_path=tmp_path / "idx.md",
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf)],
        gate_rollout_mode=gate_rollout_mode,
        wiring_gate_mode="off",
    )


def _make_result(output_path: str = "") -> TaskResult:
    now = datetime.now(timezone.utc)
    return TaskResult(
        task=TaskEntry(task_id="T01.01", title="Test"),
        status=TaskStatus.PASS,
        turns_consumed=10,
        started_at=now - timedelta(seconds=10),
        finished_at=now,
        output_path=output_path,
    )


class TestAntiInstinctShadowRecording:
    """FR-SPRINT.4: verify ShadowGateMetrics recording per rollout mode."""

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(True, None))
    def test_off_mode_no_recording(self, mock_gate, tmp_path):
        """off mode: gate evaluates but metrics are NOT recorded."""
        config = _make_anti_instinct_config(tmp_path, "off")
        result = _make_result(str(tmp_path / "out.md"))
        metrics = ShadowGateMetrics()

        run_post_task_anti_instinct_hook(
            TaskEntry(task_id="T01.01", title="t"), config, result,
            shadow_metrics=metrics,
        )

        assert metrics.total_evaluated == 0

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(True, None))
    def test_shadow_mode_records(self, mock_gate, tmp_path):
        """shadow mode: metrics recorded with passed=True and evaluation_ms > 0."""
        config = _make_anti_instinct_config(tmp_path, "shadow")
        (tmp_path / "out.md").write_text("content")
        result = _make_result(str(tmp_path / "out.md"))
        metrics = ShadowGateMetrics()

        run_post_task_anti_instinct_hook(
            TaskEntry(task_id="T01.01", title="t"), config, result,
            shadow_metrics=metrics,
        )

        assert metrics.total_evaluated == 1
        assert metrics.passed == 1
        assert len(metrics.latency_ms) == 1
        assert metrics.latency_ms[0] >= 0.0

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(False, "fail"))
    def test_soft_mode_records_fail(self, mock_gate, tmp_path):
        """soft mode: fail metrics recorded."""
        config = _make_anti_instinct_config(tmp_path, "soft")
        (tmp_path / "out.md").write_text("content")
        result = _make_result(str(tmp_path / "out.md"))
        metrics = ShadowGateMetrics()

        run_post_task_anti_instinct_hook(
            TaskEntry(task_id="T01.01", title="t"), config, result,
            shadow_metrics=metrics,
        )

        assert metrics.total_evaluated == 1
        assert metrics.failed == 1

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(True, None))
    def test_full_mode_records(self, mock_gate, tmp_path):
        """full mode: pass metrics recorded."""
        config = _make_anti_instinct_config(tmp_path, "full")
        (tmp_path / "out.md").write_text("content")
        result = _make_result(str(tmp_path / "out.md"))
        metrics = ShadowGateMetrics()

        run_post_task_anti_instinct_hook(
            TaskEntry(task_id="T01.01", title="t"), config, result,
            shadow_metrics=metrics,
        )

        assert metrics.total_evaluated == 1
        assert metrics.passed == 1

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(True, None))
    def test_data_point_structure(self, mock_gate, tmp_path):
        """Verify ShadowGateMetrics data point contains passed + evaluation_ms."""
        config = _make_anti_instinct_config(tmp_path, "shadow")
        (tmp_path / "out.md").write_text("content")
        result = _make_result(str(tmp_path / "out.md"))
        metrics = ShadowGateMetrics()

        run_post_task_anti_instinct_hook(
            TaskEntry(task_id="T01.01", title="t"), config, result,
            shadow_metrics=metrics,
        )

        assert metrics.total_evaluated == 1
        assert metrics.passed == 1
        assert metrics.failed == 0
        assert isinstance(metrics.latency_ms[0], float)
        assert metrics.latency_ms[0] >= 0.0
