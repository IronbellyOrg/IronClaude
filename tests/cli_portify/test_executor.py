"""Tests for the CLI Portify executor.

Covers T03.04 (executor), T03.06 (_determine_status), T03.07 (retry),
T03.08 (TurnLedger / HALTED), T03.09 (signal handlers), T03.10 (return contract).
"""

from __future__ import annotations

import signal
from pathlib import Path

import pytest
import yaml

from superclaude.cli.cli_portify.executor import (
    PortifyExecutor,
    _build_resume_command,
    _calculate_suggested_resume_budget,
    _determine_status,
    run_with_timeout,
)
from superclaude.cli.cli_portify.models import (
    PortifyOutcome,
    PortifyPhaseType,
    PortifyStatus,
    PortifyStep,
    TurnLedger,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_step(
    step_id: str,
    phase_type: PortifyPhaseType = PortifyPhaseType.PREREQUISITES,
    retry_limit: int = 1,
    output_file: Path | None = None,
) -> PortifyStep:
    return PortifyStep(
        step_id=step_id,
        phase_type=phase_type,
        retry_limit=retry_limit,
        output_file=output_file,
    )


def _runner_success(step: PortifyStep):
    """Always returns exit 0 with EXIT_RECOMMENDATION marker."""
    stdout = "EXIT_RECOMMENDATION: CONTINUE"
    if step.output_file:
        step.output_file.parent.mkdir(parents=True, exist_ok=True)
        step.output_file.write_text("---\nstatus: pass\n---\noutput")
    return 0, stdout, False


def _runner_failure(step: PortifyStep):
    return 1, "", False


def _runner_timeout(step: PortifyStep):
    return 124, "", True


def _runner_no_signal(step: PortifyStep):
    """Exit 0, no EXIT_RECOMMENDATION marker, artifact present."""
    if step.output_file:
        step.output_file.parent.mkdir(parents=True, exist_ok=True)
        step.output_file.write_text("content")
    return 0, "", False


# ---------------------------------------------------------------------------
# T03.04: test_executor — Sequential execution
# ---------------------------------------------------------------------------


class TestExecutorSequentialExecution:
    """T03.04 — Executor runs steps in sequential order."""

    def test_executor_runs_all_steps_sequentially(self, tmp_path):
        executed = []
        steps = [_make_step(sid) for sid in ["s1", "s2", "s3"]]

        def runner(step: PortifyStep):
            executed.append(step.step_id)
            return 0, "EXIT_RECOMMENDATION: CONTINUE", False

        ex = PortifyExecutor(steps, tmp_path, step_runner=runner)
        outcome = ex.run()
        assert outcome == PortifyOutcome.SUCCESS
        assert executed == ["s1", "s2", "s3"]

    def test_executor_stops_on_failure(self, tmp_path):
        executed = []
        steps = [_make_step(sid) for sid in ["s1", "s2", "s3"]]

        call_count = [0]

        def runner(step: PortifyStep):
            executed.append(step.step_id)
            call_count[0] += 1
            if step.step_id == "s2":
                return 1, "", False
            return 0, "EXIT_RECOMMENDATION: CONTINUE", False

        ex = PortifyExecutor(steps, tmp_path, step_runner=runner)
        outcome = ex.run()
        assert outcome == PortifyOutcome.FAILURE
        assert "s3" not in executed

    def test_executor_emits_return_contract(self, tmp_path):
        steps = [_make_step("s1")]
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_success)
        ex.run()
        contract_path = tmp_path / "return-contract.yaml"
        assert contract_path.exists()

    def test_executor_dry_run_filters_phase_types(self, tmp_path):
        """SC-012: dry-run execution filters steps to PREREQUISITES, ANALYSIS,
        USER_REVIEW, SPECIFICATION phase types only. SYNTHESIS, CONVERGENCE,
        and any other non-allowed phase types must not execute."""
        executed = []
        steps = [
            _make_step("s1", PortifyPhaseType.PREREQUISITES),
            _make_step("s2", PortifyPhaseType.SYNTHESIS),
            _make_step("s3", PortifyPhaseType.ANALYSIS),
            _make_step("s4", PortifyPhaseType.CONVERGENCE),
            _make_step("s5", PortifyPhaseType.USER_REVIEW),
            _make_step("s6", PortifyPhaseType.SPECIFICATION),
        ]

        def runner(step: PortifyStep):
            executed.append(step.step_id)
            return 0, "EXIT_RECOMMENDATION: CONTINUE", False

        ex = PortifyExecutor(steps, tmp_path, dry_run=True, step_runner=runner)
        ex.run()
        # SC-012: Only PREREQUISITES, ANALYSIS, USER_REVIEW, SPECIFICATION run
        assert "s1" in executed  # PREREQUISITES — allowed
        assert "s2" not in executed  # SYNTHESIS — excluded
        assert "s3" in executed  # ANALYSIS — allowed
        assert "s4" not in executed  # CONVERGENCE — excluded
        assert "s5" in executed  # USER_REVIEW — allowed
        assert "s6" in executed  # SPECIFICATION — allowed

    def test_executor_resume_skips_prior_steps(self, tmp_path):
        executed = []
        steps = [_make_step(sid) for sid in ["s1", "s2", "s3"]]

        def runner(step: PortifyStep):
            executed.append(step.step_id)
            return 0, "EXIT_RECOMMENDATION: CONTINUE", False

        ex = PortifyExecutor(steps, tmp_path, resume_from="s2", step_runner=runner)
        ex.run()
        assert "s1" not in executed
        assert "s2" in executed
        assert "s3" in executed

    def test_executor_dry_run_contract_has_dry_run_outcome(self, tmp_path):
        steps = [_make_step("s1", PortifyPhaseType.PREREQUISITES)]
        ex = PortifyExecutor(steps, tmp_path, dry_run=True, step_runner=_runner_success)
        ex.run()
        contract = yaml.safe_load((tmp_path / "return-contract.yaml").read_text())
        assert contract["outcome"] == "DRY_RUN"


# ---------------------------------------------------------------------------
# T03.06: test_determine_status — Status classification
# ---------------------------------------------------------------------------


class TestDetermineStatus:
    """T03.06 — _determine_status() classifies all exit code paths correctly."""

    def test_determine_status_timeout_exit_124(self):
        status = _determine_status(124, timed_out=True, stdout="")
        assert status == PortifyStatus.TIMEOUT

    def test_determine_status_timeout_flag(self):
        status = _determine_status(0, timed_out=True, stdout="")
        assert status == PortifyStatus.TIMEOUT

    def test_determine_status_error_nonzero(self):
        status = _determine_status(1, timed_out=False, stdout="")
        assert status == PortifyStatus.ERROR

    def test_determine_status_error_exit_2(self):
        status = _determine_status(2, timed_out=False, stdout="")
        assert status == PortifyStatus.ERROR

    def test_determine_status_pass_with_marker_and_artifact(self, tmp_path):
        artifact = tmp_path / "out.md"
        artifact.write_text("content")
        status = _determine_status(
            0,
            timed_out=False,
            stdout="EXIT_RECOMMENDATION: CONTINUE",
            artifact_path=artifact,
        )
        assert status == PortifyStatus.PASS

    def test_determine_status_pass_no_signal_no_marker(self, tmp_path):
        artifact = tmp_path / "out.md"
        artifact.write_text("content")
        status = _determine_status(
            0,
            timed_out=False,
            stdout="",
            artifact_path=artifact,
        )
        assert status == PortifyStatus.PASS_NO_SIGNAL

    def test_determine_status_pass_no_report_no_artifact(self, tmp_path):
        status = _determine_status(
            0,
            timed_out=False,
            stdout="",
            artifact_path=tmp_path / "nonexistent.md",
        )
        assert status == PortifyStatus.PASS_NO_REPORT

    def test_determine_status_pass_no_report_no_artifact_path(self):
        status = _determine_status(0, timed_out=False, stdout="", artifact_path=None)
        assert status == PortifyStatus.PASS_NO_REPORT

    def test_determine_status_pass_no_signal_triggers_retry(self, tmp_path):
        """PASS_NO_SIGNAL triggers retry (not PASS_NO_REPORT)."""
        artifact = tmp_path / "out.md"
        artifact.write_text("content")
        status = _determine_status(
            0, timed_out=False, stdout="", artifact_path=artifact
        )
        assert status == PortifyStatus.PASS_NO_SIGNAL
        # Verify it's distinct from PASS_NO_REPORT
        assert status != PortifyStatus.PASS_NO_REPORT


# ---------------------------------------------------------------------------
# T03.07: test_retry — Retry mechanism
# ---------------------------------------------------------------------------


class TestRetry:
    """T03.07 — Retry mechanism with retry_limit=1."""

    def test_retry_triggered_on_pass_no_signal(self, tmp_path):
        """PASS_NO_SIGNAL triggers exactly one retry."""
        artifact = tmp_path / "out.md"
        call_count = [0]
        step = _make_step("s1", output_file=artifact)

        def runner(s: PortifyStep):
            call_count[0] += 1
            artifact.write_text("content")
            return 0, "", False  # no marker → PASS_NO_SIGNAL

        ex = PortifyExecutor([step], tmp_path, step_runner=runner)
        ex.run()
        # 1 initial + 1 retry = 2 calls
        assert call_count[0] == 2

    def test_retry_not_triggered_on_pass_no_report(self, tmp_path):
        """PASS_NO_REPORT does not trigger retry (no artifact)."""
        call_count = [0]
        step = _make_step("s1", output_file=tmp_path / "nonexistent.md")

        def runner(s: PortifyStep):
            call_count[0] += 1
            return 0, "", False  # no marker, no artifact → PASS_NO_REPORT

        ex = PortifyExecutor([step], tmp_path, step_runner=runner)
        ex.run()
        assert call_count[0] == 1  # no retry

    def test_retry_max_one_attempt(self, tmp_path):
        """Retry fires at most once regardless of repeated PASS_NO_SIGNAL."""
        artifact = tmp_path / "out.md"
        call_count = [0]
        step = _make_step("s1", output_file=artifact)

        def runner(s: PortifyStep):
            call_count[0] += 1
            artifact.write_text("still no marker")
            return 0, "", False

        ex = PortifyExecutor([step], tmp_path, step_runner=runner)
        ex.run()
        # Max 2 calls (1 initial + 1 retry) — never more
        assert call_count[0] == 2

    def test_retry_consumes_budget(self, tmp_path):
        """Each retry invocation consumes one turn from the ledger."""
        artifact = tmp_path / "out.md"
        step = _make_step("s1", output_file=artifact)

        def runner(s: PortifyStep):
            artifact.write_text("content")
            return 0, "", False  # PASS_NO_SIGNAL → retry

        ex = PortifyExecutor([step], tmp_path, turn_budget=10, step_runner=runner)
        ex.run()
        # 2 turns consumed (initial + retry)
        assert ex._ledger.consumed == 2


# ---------------------------------------------------------------------------
# T03.08: test_turn_ledger — TurnLedger and HALTED
# ---------------------------------------------------------------------------


class TestTurnLedger:
    """T03.08 — TurnLedger tracks budget and produces HALTED on exhaustion."""

    def test_turn_ledger_tracks_consumed(self):
        ledger = TurnLedger(total_budget=5)
        ledger.consume(2)
        assert ledger.consumed == 2
        assert ledger.remaining == 3

    def test_turn_ledger_can_launch_true(self):
        ledger = TurnLedger(total_budget=5)
        assert ledger.can_launch() is True

    def test_turn_ledger_can_launch_false_when_exhausted(self):
        ledger = TurnLedger(total_budget=2)
        ledger.consume(2)
        assert ledger.can_launch() is False

    def test_turn_ledger_remaining_never_negative(self):
        ledger = TurnLedger(total_budget=1)
        ledger.consume(10)
        assert ledger.remaining == 0

    def test_turn_ledger_budget_exhaustion_produces_halted(self, tmp_path):
        """When budget=0, first step triggers HALTED before any execution."""
        steps = [_make_step(sid) for sid in ["s1", "s2"]]
        executed = []

        def runner(s: PortifyStep):
            executed.append(s.step_id)
            return 0, "EXIT_RECOMMENDATION: CONTINUE", False

        ex = PortifyExecutor(steps, tmp_path, turn_budget=0, step_runner=runner)
        outcome = ex.run()
        assert outcome == PortifyOutcome.HALTED
        assert executed == []

    def test_turn_ledger_halted_emits_return_contract(self, tmp_path):
        steps = [_make_step("s1")]
        ex = PortifyExecutor(
            steps, tmp_path, turn_budget=0, step_runner=_runner_success
        )
        ex.run()
        assert (tmp_path / "return-contract.yaml").exists()


# ---------------------------------------------------------------------------
# T03.09: test_signal_handler — Signal handling
# ---------------------------------------------------------------------------


class TestSignalHandler:
    """T03.09 — SIGINT/SIGTERM set INTERRUPTED outcome after step completes."""

    def test_signal_handler_interrupted_flag_set(self, tmp_path):
        steps = [_make_step(sid) for sid in ["s1", "s2"]]
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_success)

        # Simulate interrupt mid-run by setting the flag directly
        call_count = [0]

        def runner_with_interrupt(step: PortifyStep):
            call_count[0] += 1
            if call_count[0] == 1:
                ex._interrupted = True  # simulate signal after first step
            return 0, "EXIT_RECOMMENDATION: CONTINUE", False

        ex._step_runner = runner_with_interrupt
        outcome = ex.run()
        assert outcome == PortifyOutcome.INTERRUPTED

    def test_signal_handler_interrupted_emits_contract(self, tmp_path):
        steps = [_make_step("s1")]
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_success)
        ex._interrupted = True  # interrupt before any step
        ex.run()
        assert (tmp_path / "return-contract.yaml").exists()

    def test_signal_handler_sigint_registered(self, tmp_path):
        """_install_signal_handlers registers SIGINT handler."""
        steps = [_make_step("s1")]
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_success)
        ex._install_signal_handlers()
        # Verify handler is installed (not SIG_DFL or SIG_IGN)
        handler = signal.getsignal(signal.SIGINT)
        assert callable(handler)
        ex._restore_signal_handlers()

    def test_signal_handler_sigterm_registered(self, tmp_path):
        """_install_signal_handlers registers SIGTERM handler."""
        steps = [_make_step("s1")]
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_success)
        ex._install_signal_handlers()
        handler = signal.getsignal(signal.SIGTERM)
        assert callable(handler)
        ex._restore_signal_handlers()

    def test_signal_handler_handlers_restored_after_run(self, tmp_path):
        """Original signal handlers are restored after executor finishes."""
        original_sigint = signal.getsignal(signal.SIGINT)
        steps = [_make_step("s1")]
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_success)
        ex.run()
        assert signal.getsignal(signal.SIGINT) == original_sigint


# ---------------------------------------------------------------------------
# T03.10: test_return_contract — Return contract emission
# ---------------------------------------------------------------------------


class TestReturnContract:
    """T03.10 — Return contract emitted on all outcome paths (SC-011)."""

    def test_return_contract_emitted_on_success(self, tmp_path):
        steps = [_make_step("s1")]
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_success)
        ex.run()
        assert (tmp_path / "return-contract.yaml").exists()

    def test_return_contract_emitted_on_failure(self, tmp_path):
        steps = [_make_step("s1")]
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_failure)
        ex.run()
        assert (tmp_path / "return-contract.yaml").exists()

    def test_return_contract_emitted_on_timeout(self, tmp_path):
        steps = [_make_step("s1")]
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_timeout)
        ex.run()
        assert (tmp_path / "return-contract.yaml").exists()

    def test_return_contract_emitted_on_dry_run(self, tmp_path):
        steps = [_make_step("s1", PortifyPhaseType.PREREQUISITES)]
        ex = PortifyExecutor(steps, tmp_path, dry_run=True, step_runner=_runner_success)
        ex.run()
        assert (tmp_path / "return-contract.yaml").exists()

    def test_return_contract_emitted_on_halted(self, tmp_path):
        steps = [_make_step("s1")]
        ex = PortifyExecutor(
            steps, tmp_path, turn_budget=0, step_runner=_runner_success
        )
        ex.run()
        assert (tmp_path / "return-contract.yaml").exists()

    def test_return_contract_resume_command_format(self, tmp_path):
        steps = [_make_step("s1"), _make_step("s2")]
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_failure)
        ex.run()
        contract = yaml.safe_load((tmp_path / "return-contract.yaml").read_text())
        # resume_command should contain step id
        rc = contract.get("resume_command", "")
        assert "superclaude cli-portify run --resume" in rc

    def test_return_contract_suggested_budget_dynamic(self, tmp_path):
        """suggested_resume_budget = remaining_pending_steps * 25."""
        steps = [_make_step(sid) for sid in ["s1", "s2", "s3"]]
        # s1 fails, s2 and s3 remain
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_failure)
        ex.run()
        contract = yaml.safe_load((tmp_path / "return-contract.yaml").read_text())
        # After s1 fails: s2 + s3 are PENDING → 2 * 25 = 50
        assert contract["suggested_resume_budget"] == 50

    def test_return_contract_success_completed_steps(self, tmp_path):
        steps = [_make_step(sid) for sid in ["s1", "s2"]]
        ex = PortifyExecutor(steps, tmp_path, step_runner=_runner_success)
        ex.run()
        contract = yaml.safe_load((tmp_path / "return-contract.yaml").read_text())
        assert "s1" in contract["completed_steps"]
        assert "s2" in contract["completed_steps"]

    def test_resume_command_helper(self):
        cmd = _build_resume_command("step-5")
        assert "step-5" in cmd
        assert "superclaude cli-portify run --resume" in cmd

    def test_suggested_budget_calculation(self, tmp_path):
        steps = [_make_step(sid) for sid in ["s1", "s2", "s3"]]
        # All PENDING → 3 * 25 = 75
        budget = _calculate_suggested_resume_budget(steps)
        assert budget == 75


# ---------------------------------------------------------------------------
# T02.09: run_with_timeout() — NFR-001 enforcement tests
# ---------------------------------------------------------------------------


class TestRunWithTimeout:
    """T02.09 acceptance criteria:
    - Input-validation step with mocked 31s execution raises TimeoutError (SC-001).
    - Component-discovery step with mocked 61s execution raises TimeoutError (SC-002).
    - Fast functions complete normally within timeout.
    """

    def test_fast_function_completes_normally(self):
        """A function completing instantly is returned without error."""
        result = run_with_timeout(lambda: 42, timeout_s=5.0)
        assert result == 42

    def test_fast_function_with_args(self):
        """Arguments are forwarded to the function correctly."""
        result = run_with_timeout(lambda x, y: x + y, 5.0, 3, 4)
        assert result == 7

    def test_slow_function_raises_timeout_error(self):
        """A function exceeding the timeout raises TimeoutError (not hanging)."""
        import threading

        def _slow():
            threading.Event().wait(timeout=10)  # simulate blocking

        with pytest.raises(TimeoutError):
            run_with_timeout(_slow, timeout_s=0.1)

    def test_step0_validate_config_timeout_boundary(self):
        """Mocked slow validate-config execution raises TimeoutError (SC-001: ≤30s boundary)."""
        import threading

        # Use 0.05s timeout to test boundary behavior without waiting 30s in CI
        def _mock_slow_validate():
            threading.Event().wait(timeout=10)

        with pytest.raises(TimeoutError):
            run_with_timeout(_mock_slow_validate, timeout_s=0.05)

    def test_step1_discover_components_timeout_boundary(self):
        """Mocked slow discover-components execution raises TimeoutError (SC-002: ≤60s boundary)."""
        import threading

        # Use 0.05s timeout to test boundary behavior without waiting 60s in CI
        def _mock_slow_discover():
            threading.Event().wait(timeout=10)

        with pytest.raises(TimeoutError):
            run_with_timeout(_mock_slow_discover, timeout_s=0.05)

    def test_timeout_error_message_contains_limit(self):
        """TimeoutError message includes the timeout limit."""
        import threading

        def _slow():
            threading.Event().wait(timeout=10)

        with pytest.raises(TimeoutError, match="5.0"):
            run_with_timeout(_slow, timeout_s=5.0)

    def test_return_value_passed_through(self):
        """Return value from a successful call is passed through unchanged."""
        result = run_with_timeout(lambda: {"key": "value"}, 5.0)
        assert result == {"key": "value"}

    def test_exception_propagated_from_function(self):
        """Exceptions raised inside the function are re-raised to the caller."""

        def _raises():
            raise ValueError("inner error")

        with pytest.raises(ValueError, match="inner error"):
            run_with_timeout(_raises, timeout_s=5.0)


# ---------------------------------------------------------------------------
# Item 2.3 (cleanup-debt-reduction): production-dispatch live-owner assertions
#
# Every test below constructs PortifyExecutor WITHOUT step_runner, so run()
# and _execute_step() take the real production branch (executor.py:577-650).
# Only the step functions selected by the real get_step_dispatch() registry
# are replaced (monkeypatch.setitem on the cached registry dict); gates,
# ExecutionLog, TimingCapture, DiagnosticsCollector, FAILURE_HANDLERS and the
# run loop are the real implementations. Expected values pin CURRENT behavior
# (characterization), including behavior that differs from what a reader
# might expect (FAIL and gate HALT do not stop the run loop).
# ---------------------------------------------------------------------------

import dataclasses  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import stat  # noqa: E402
import time  # noqa: E402

from click.testing import CliRunner  # noqa: E402

from superclaude.cli.cli_portify import executor as executor_mod  # noqa: E402
from superclaude.cli.cli_portify.failures import FAILURE_HANDLERS  # noqa: E402
from superclaude.cli.cli_portify.models import (  # noqa: E402
    FailureClassification,
    MonitorState,
    PortifyConfig,
    PortifyGateMode,
    PortifyStepResult,
    ResumeContext,
)
from superclaude.cli.cli_portify.monitor import OutputMonitor  # noqa: E402
from superclaude.cli.cli_portify.steps import get_step_dispatch  # noqa: E402


def _live_step(
    step_id: str,
    phase_type: PortifyPhaseType = PortifyPhaseType.ANALYSIS,
    output_file: Path | None = None,
) -> PortifyStep:
    return PortifyStep(step_id=step_id, phase_type=phase_type, output_file=output_file)


def _events(workdir: Path) -> list[dict]:
    lines = (workdir / "execution-log.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines]


class _FakeStepFn:
    """Stand-in for a dispatch-selected run_*() step function.

    Records the config it receives, optionally sleeps (so the real
    TimingCapture measures a nonzero duration) and writes its artifact,
    then returns a realistic PortifyStepResult.
    """

    def __init__(
        self,
        result: PortifyStepResult,
        *,
        sleep_s: float = 0.0,
        artifact: Path | None = None,
        artifact_text: str = "",
    ) -> None:
        self.result = result
        self.sleep_s = sleep_s
        self.artifact = artifact
        self.artifact_text = artifact_text
        self.configs: list = []

    def __call__(self, config):
        self.configs.append(config)
        if self.sleep_s:
            time.sleep(self.sleep_s)
        if self.artifact is not None:
            self.artifact.parent.mkdir(parents=True, exist_ok=True)
            self.artifact.write_text(self.artifact_text, encoding="utf-8")
        return self.result


@pytest.fixture
def live_dispatch(monkeypatch):
    """Install fakes into the REAL cached dispatch registry used by _execute_step."""
    registry = get_step_dispatch()
    # The executor resolves the same callable/registry object at dispatch time.
    assert executor_mod.get_step_dispatch is get_step_dispatch
    assert executor_mod.get_step_dispatch() is registry

    def install(step_id: str, fn) -> None:
        assert step_id in registry  # only replace real dispatch-selected entries
        monkeypatch.setitem(registry, step_id, fn)

    return install


def _pass_result(step_name: str) -> PortifyStepResult:
    return PortifyStepResult(
        step_name=step_name,
        step_number=3,
        phase=2,
        portify_status=PortifyStatus.PASS,
        artifact_path="",
        resume_context=ResumeContext(),
    )


def _failed_result(
    step_name: str,
    status: PortifyStatus,
    classification: FailureClassification | None,
    missing_artifact: Path,
) -> PortifyStepResult:
    return PortifyStepResult(
        step_name=step_name,
        step_number=3,
        phase=2,
        portify_status=status,
        failure_classification=classification,
        artifact_path=str(missing_artifact),
        resume_context=ResumeContext(
            resume_command=f"superclaude cli-portify run --resume {step_name}",
            resume_step=step_name,
            resume_phase=2,
        ),
        error_message=f"{step_name} failed",
    )


class TestProductionDispatchLiveOwners:
    """Item 2.3: real run()/_execute_step dispatch with step_runner UNSET."""

    def test_step_fn_receives_real_config_and_result_identity_stored(
        self, tmp_path, live_dispatch
    ):
        config = PortifyConfig(stall_timeout=17)
        r1 = _pass_result("protocol-mapping")
        r2 = _pass_result("analysis-synthesis")
        f1, f2 = _FakeStepFn(r1), _FakeStepFn(r2)
        live_dispatch("protocol-mapping", f1)
        live_dispatch("analysis-synthesis", f2)
        steps = [_live_step("protocol-mapping"), _live_step("analysis-synthesis")]

        ex = PortifyExecutor(steps, tmp_path, config=config, turn_budget=10)
        assert ex._step_runner is None
        outcome = ex.run()

        assert outcome == PortifyOutcome.SUCCESS
        assert len(f1.configs) == 1 and f1.configs[0] is config
        assert len(f2.configs) == 1 and f2.configs[0] is config
        assert ex._step_results["protocol-mapping"] is r1
        assert ex._step_results["analysis-synthesis"] is r2
        assert ex._completed_steps == ["protocol-mapping", "analysis-synthesis"]
        assert [s.status for s in steps] == [PortifyStatus.PASS, PortifyStatus.PASS]
        # Ledger: one turn per dispatched step, no retry on the production path
        assert ex._ledger.consumed == 2
        # A-18: diagnostics.md is NOT emitted on SUCCESS
        assert not (tmp_path / "diagnostics.md").exists()
        contract = yaml.safe_load((tmp_path / "return-contract.yaml").read_text())
        assert contract["outcome"] == "SUCCESS"

    def test_execution_log_records_and_real_measured_duration(
        self, tmp_path, live_dispatch
    ):
        """P-1 / A-19: step_start, gate_eval, step_end (status + real duration),
        pipeline_outcome in execution-log.jsonl."""
        fn = _FakeStepFn(_pass_result("protocol-mapping"), sleep_s=0.03)
        live_dispatch("protocol-mapping", fn)
        ex = PortifyExecutor(
            [_live_step("protocol-mapping")], tmp_path, config=PortifyConfig()
        )
        ex.run()

        events = _events(tmp_path)
        assert [e["event_type"] for e in events] == [
            "step_start",
            "gate_eval",
            "step_end",
            "pipeline_outcome",
        ]
        for e in events:
            assert set(["timestamp", "event_type", "step_id"]) <= set(e)
        assert events[0]["step_id"] == "protocol-mapping"
        # protocol-mapping has no GATE_REGISTRY entry -> tier NONE, gate_id = step id
        gate = events[1]
        assert (gate["step_id"], gate["gate_id"], gate["tier"]) == (
            "protocol-mapping",
            "protocol-mapping",
            "NONE",
        )
        step_end = events[2]
        assert step_end["step_id"] == "protocol-mapping"
        assert step_end["status"] == "pass"
        timing = ex._timing.get_step_timing("protocol-mapping")
        assert timing is not None
        assert step_end["duration_s"] == timing.duration_seconds
        assert step_end["duration_s"] >= 0.03
        assert events[3]["step_id"] == ""
        assert events[3]["outcome"] == "SUCCESS"

    def test_pipeline_elapsed_reaches_execution_log_md(self, tmp_path, live_dispatch):
        """A-21: real TimingCapture.total_duration is the md row elapsed value."""
        live_dispatch(
            "protocol-mapping",
            _FakeStepFn(_pass_result("protocol-mapping"), sleep_s=0.03),
        )
        ex = PortifyExecutor(
            [_live_step("protocol-mapping")], tmp_path, config=PortifyConfig()
        )
        ex.run()

        assert ex._timing.total_duration >= 0.03
        md = (tmp_path / "execution-log.md").read_text(encoding="utf-8").splitlines()
        assert md[0] == "# CLI Portify Execution Log"
        assert md[-1] == f"|  | SUCCESS | {ex._timing.total_duration:.3f}s | 4 |"

    def test_error_result_records_diagnostics_and_failure_handler(
        self, tmp_path, live_dispatch
    ):
        """P-2 / P-3 / A-18: ERROR records exit code, missing artifact, resume
        guidance and a failure_handler log entry; diagnostics.md is emitted;
        the failed result is stored; the loop stops."""
        missing = tmp_path / "results" / "portify-analysis.md"
        bad = _failed_result(
            "protocol-mapping",
            PortifyStatus.ERROR,
            FailureClassification.MISSING_ARTIFACT,
            missing,
        )
        f_next = _FakeStepFn(_pass_result("analysis-synthesis"))
        live_dispatch("protocol-mapping", _FakeStepFn(bad))
        live_dispatch("analysis-synthesis", f_next)
        steps = [_live_step("protocol-mapping"), _live_step("analysis-synthesis")]
        ex = PortifyExecutor(steps, tmp_path, config=PortifyConfig())

        outcome = ex.run()

        assert outcome == PortifyOutcome.FAILURE
        assert f_next.configs == []  # loop broke after ERROR
        assert ex._step_results["protocol-mapping"] is bad
        assert "analysis-synthesis" not in ex._step_results
        bundle = ex._diagnostics.build_bundle()
        assert bundle.exit_code == 1
        assert bundle.missing_artifacts == [str(missing)]
        assert (
            bundle.resume_guidance
            == "superclaude cli-portify run --resume protocol-mapping"
        )
        assert bundle.gate_failures == []

        events = _events(tmp_path)
        types = [e["event_type"] for e in events]
        assert types == [
            "step_start",
            "gate_eval",
            "step_end",
            "failure_handler",
            "pipeline_outcome",
        ]
        assert events[2]["status"] == "error"
        assert events[3]["handler_name"] == "handle_missing_template"
        assert events[3]["classification"] == "missing_artifact"
        assert events[4]["outcome"] == "FAILURE"

        diag = (tmp_path / "diagnostics.md").read_text(encoding="utf-8")
        assert diag.startswith("# CLI Portify — Pipeline Failure Diagnostics")
        # emit_diagnostics step_id is the FIRST PENDING step (resume target),
        # not the failed step itself
        assert "**Failed Step:** `analysis-synthesis`" in diag
        assert "**Exit Code:** 1" in diag
        assert f"- `{missing}`" in diag
        assert "superclaude cli-portify run --resume protocol-mapping" in diag
        assert "## Gate Failures\n\n_None recorded._" in diag

    def test_failure_handler_log_is_name_only_not_invocation(
        self, tmp_path, live_dispatch, monkeypatch
    ):
        """The failure_handler record logs handler.__name__; the handler itself
        is never called by the executor (handler-name logging != invocation)."""
        calls: list = []

        def spy_handler(*args, **kwargs):  # pragma: no cover - must not run
            calls.append((args, kwargs))

        monkeypatch.setitem(
            FAILURE_HANDLERS, FailureClassification.MISSING_ARTIFACT, spy_handler
        )
        bad = _failed_result(
            "protocol-mapping",
            PortifyStatus.ERROR,
            FailureClassification.MISSING_ARTIFACT,
            tmp_path / "absent.md",
        )
        live_dispatch("protocol-mapping", _FakeStepFn(bad))
        ex = PortifyExecutor(
            [_live_step("protocol-mapping")], tmp_path, config=PortifyConfig()
        )
        ex.run()

        handler_events = [
            e for e in _events(tmp_path) if e["event_type"] == "failure_handler"
        ]
        assert [e["handler_name"] for e in handler_events] == ["spy_handler"]
        assert calls == []

    @pytest.mark.parametrize(
        "classification",
        [FailureClassification.GATE_FAILURE, FailureClassification.USER_REJECTION],
        ids=["gate_failure", "user_rejection"],
    )
    def test_fail_without_registered_handler_logs_no_failure_handler(
        self, tmp_path, live_dispatch, classification
    ):
        """A-11 (+ review rejection): GATE_FAILURE / USER_REJECTION have no
        callable handler, so no failure_handler entry is logged. FAIL status
        does NOT stop the run loop and outcome stays SUCCESS (executor.py
        693-704), so diagnostics are collected but diagnostics.md is absent."""
        missing = tmp_path / "results" / "portify-analysis.md"
        bad = _failed_result(
            "protocol-mapping", PortifyStatus.FAIL, classification, missing
        )
        f_next = _FakeStepFn(_pass_result("analysis-synthesis"))
        live_dispatch("protocol-mapping", _FakeStepFn(bad))
        live_dispatch("analysis-synthesis", f_next)
        steps = [_live_step("protocol-mapping"), _live_step("analysis-synthesis")]
        ex = PortifyExecutor(steps, tmp_path, config=PortifyConfig())

        outcome = ex.run()

        events = _events(tmp_path)
        assert "failure_handler" not in [e["event_type"] for e in events]
        assert outcome == PortifyOutcome.SUCCESS
        assert len(f_next.configs) == 1  # next step still dispatched
        assert steps[0].status == PortifyStatus.FAIL
        assert ex._step_results["protocol-mapping"] is bad
        assert ex._completed_steps == ["analysis-synthesis"]
        bundle = ex._diagnostics.build_bundle()
        assert bundle.exit_code == 1
        assert bundle.missing_artifacts == [str(missing)]
        assert (
            bundle.resume_guidance
            == "superclaude cli-portify run --resume protocol-mapping"
        )
        assert not (tmp_path / "diagnostics.md").exists()
        step_ends = [e for e in events if e["event_type"] == "step_end"]
        assert [e["status"] for e in step_ends] == ["fail", "pass"]

    def test_timeout_result_outcome_timeout_and_diagnostics(
        self, tmp_path, live_dispatch
    ):
        """TIMEOUT result: handle_timeout name logged, loop stops, outcome
        TIMEOUT, diagnostics.md emitted."""
        bad = _failed_result(
            "protocol-mapping",
            PortifyStatus.TIMEOUT,
            FailureClassification.TIMEOUT,
            tmp_path / "absent.md",
        )
        f_next = _FakeStepFn(_pass_result("analysis-synthesis"))
        live_dispatch("protocol-mapping", _FakeStepFn(bad))
        live_dispatch("analysis-synthesis", f_next)
        steps = [_live_step("protocol-mapping"), _live_step("analysis-synthesis")]
        ex = PortifyExecutor(steps, tmp_path, config=PortifyConfig())

        assert ex.run() == PortifyOutcome.TIMEOUT
        assert f_next.configs == []
        assert ex._step_results["protocol-mapping"] is bad
        events = _events(tmp_path)
        fh = [e for e in events if e["event_type"] == "failure_handler"]
        assert [(e["handler_name"], e["classification"]) for e in fh] == [
            ("handle_timeout", "timeout")
        ]
        assert events[-1]["outcome"] == "TIMEOUT"
        diag = (tmp_path / "diagnostics.md").read_text(encoding="utf-8")
        assert "**Exit Code:** 1" in diag
        assert "superclaude cli-portify run --resume protocol-mapping" in diag

    def test_budget_exhaustion_halted_emits_diagnostics(self, tmp_path, live_dispatch):
        """A-18 HALTED: ledger consumed by the production dispatch; second step
        cannot launch, outcome HALTED and diagnostics.md is emitted."""
        f1 = _FakeStepFn(_pass_result("protocol-mapping"))
        f2 = _FakeStepFn(_pass_result("analysis-synthesis"))
        live_dispatch("protocol-mapping", f1)
        live_dispatch("analysis-synthesis", f2)
        steps = [_live_step("protocol-mapping"), _live_step("analysis-synthesis")]
        ex = PortifyExecutor(steps, tmp_path, config=PortifyConfig(), turn_budget=1)

        assert ex.run() == PortifyOutcome.HALTED
        assert len(f1.configs) == 1 and f2.configs == []
        assert ex._ledger.consumed == 1
        diag = (tmp_path / "diagnostics.md").read_text(encoding="utf-8")
        assert "**Failed Step:** `analysis-synthesis`" in diag
        assert "_No resume command available for this step._" in diag

    def test_unknown_step_id_returns_error_without_logging_or_budget(self, tmp_path):
        """A step id absent from the dispatch registry returns ERROR before any
        ledger consumption or step_start record."""
        ex = PortifyExecutor(
            [_live_step("not-a-registered-step")], tmp_path, config=PortifyConfig()
        )
        assert ex.run() == PortifyOutcome.FAILURE
        assert ex._ledger.consumed == 0
        assert ex._step_results == {}
        assert [e["event_type"] for e in _events(tmp_path)] == ["pipeline_outcome"]
        assert (tmp_path / "diagnostics.md").exists()

    def test_validate_config_fail_does_not_halt_executor(self, tmp_path, live_dispatch):
        """C04 characterization: a validate-config FAIL result (live shape:
        classification None, EXEMPT tier) neither halts the executor loop nor
        logs a failure handler; outcome SUCCESS, no diagnostics.md."""
        vc = PortifyStepResult(
            step_name="validate-config",
            step_number=1,
            phase=1,
            portify_status=PortifyStatus.FAIL,
            failure_classification=None,
            gate_tier="EXEMPT",
            error_message=f"Output path is not writable: {tmp_path / 'out'}",
        )
        f_next = _FakeStepFn(_pass_result("discover-components"))
        live_dispatch("validate-config", _FakeStepFn(vc))
        live_dispatch("discover-components", f_next)
        steps = [
            _live_step("validate-config", PortifyPhaseType.PREREQUISITES),
            _live_step("discover-components", PortifyPhaseType.PREREQUISITES),
        ]
        ex = PortifyExecutor(steps, tmp_path, config=PortifyConfig())

        assert ex.run() == PortifyOutcome.SUCCESS
        assert len(f_next.configs) == 1
        assert steps[0].status == PortifyStatus.FAIL
        assert ex._step_results["validate-config"] is vc
        events = _events(tmp_path)
        assert "failure_handler" not in [e["event_type"] for e in events]
        assert ex._diagnostics.build_bundle().exit_code == 1
        assert not (tmp_path / "diagnostics.md").exists()
        contract = yaml.safe_load((tmp_path / "return-contract.yaml").read_text())
        assert contract["outcome"] == "SUCCESS"

    def test_output_monitor_constructed_but_not_fed_by_dispatch(
        self, tmp_path, live_dispatch
    ):
        """Eight-metric owner (OutputMonitor) is constructed from config but the
        production dispatch never updates it; metrics stay at defaults."""
        live_dispatch(
            "protocol-mapping",
            _FakeStepFn(_pass_result("protocol-mapping"), sleep_s=0.01),
        )
        ex = PortifyExecutor(
            [_live_step("protocol-mapping")],
            tmp_path,
            config=PortifyConfig(stall_timeout=42),
        )
        assert isinstance(ex._monitor, OutputMonitor)
        assert ex._monitor._stall_timeout_seconds == 42.0
        ex.run()
        assert dataclasses.asdict(ex._monitor.state) == dataclasses.asdict(
            MonitorState()
        )
        assert len(dataclasses.fields(MonitorState)) == 8


class TestProductionDispatchGateModes:
    """Item 2.3: source-accurate shadow / soft / full gate behavior on the
    production dispatch path (real PortifyGatePolicy + pipeline gate_passed)."""

    def test_shadow_gate_failure_continues_without_warning(
        self, tmp_path, live_dispatch, capsys
    ):
        out = tmp_path / "results" / "portify-spec.md"
        result = _pass_result("step-graph-design")
        live_dispatch(
            "step-graph-design",
            _FakeStepFn(result, artifact=out, artifact_text="one line\n"),
        )
        steps = [_live_step("step-graph-design", output_file=out)]
        ex = PortifyExecutor(steps, tmp_path, config=PortifyConfig())

        assert ex.run() == PortifyOutcome.SUCCESS
        assert "GATE WARNING" not in capsys.readouterr().err
        assert ex._diagnostics.build_bundle().gate_failures == []
        assert ex._step_results["step-graph-design"] is result
        events = _events(tmp_path)
        assert [e["event_type"] for e in events] == [
            "step_start",
            "gate_eval",
            "step_end",
            "pipeline_outcome",
        ]
        assert events[1]["tier"] == "STRICT"
        assert events[2]["status"] == "pass"

    def test_soft_gate_failure_warns_and_continues(
        self, tmp_path, live_dispatch, capsys
    ):
        """discover-components is promoted to SOFT by GATE_MIN_ENFORCE."""
        out = tmp_path / "results" / "component-inventory.md"
        result = _pass_result("discover-components")
        live_dispatch(
            "discover-components",
            _FakeStepFn(result, artifact=out, artifact_text="one line\n"),
        )
        steps = [_live_step("discover-components", PortifyPhaseType.PREREQUISITES, out)]
        ex = PortifyExecutor(steps, tmp_path, config=PortifyConfig())

        assert ex.run() == PortifyOutcome.SUCCESS
        err = capsys.readouterr().err
        assert "GATE WARNING" in err and "discover-components" in err
        assert "Below minimum line count: 1 < 5" in err
        assert ex._diagnostics.build_bundle().gate_failures == []
        assert ex._step_results["discover-components"] is result
        types = [e["event_type"] for e in _events(tmp_path)]
        assert types == ["step_start", "gate_eval", "step_end", "pipeline_outcome"]

    def test_full_gate_failure_records_gate_failure_then_halts_step(
        self, tmp_path, live_dispatch
    ):
        """FULL: GateFailure recorded, step returns HALT BEFORE step_end and
        before result storage. The run loop does NOT treat HALT as terminal:
        the next step runs, outcome stays SUCCESS and diagnostics.md is absent."""
        out = tmp_path / "results" / "component-inventory.md"
        f_gate = _FakeStepFn(
            _pass_result("discover-components"), artifact=out, artifact_text="x\n"
        )
        f_next = _FakeStepFn(_pass_result("protocol-mapping"))
        live_dispatch("discover-components", f_gate)
        live_dispatch("protocol-mapping", f_next)
        steps = [
            _live_step("discover-components", PortifyPhaseType.PREREQUISITES, out),
            _live_step("protocol-mapping"),
        ]
        ex = PortifyExecutor(
            steps, tmp_path, config=PortifyConfig(), gate_mode=PortifyGateMode.FULL
        )

        outcome = ex.run()

        assert len(f_gate.configs) == 1  # step function executed before the gate
        assert steps[0].status == PortifyStatus.HALT
        assert "discover-components" not in ex._step_results
        assert ex._ledger.consumed == 2
        failures = ex._diagnostics.build_bundle().gate_failures
        assert len(failures) == 1
        gf = failures[0]
        assert (gf.gate_id, gf.check_name, gf.tier, gf.artifact_path) == (
            "discover-components",
            "gate_passed",
            "STANDARD",
            str(out),
        )
        assert gf.diagnostic.startswith("Below minimum line count: 1 < 5")
        events = _events(tmp_path)
        assert [(e["event_type"], e["step_id"]) for e in events] == [
            ("step_start", "discover-components"),
            ("gate_eval", "discover-components"),
            ("step_start", "protocol-mapping"),
            ("gate_eval", "protocol-mapping"),
            ("step_end", "protocol-mapping"),
            ("pipeline_outcome", ""),
        ]
        # Characterized current behavior: HALT is not handled by the run loop
        assert outcome == PortifyOutcome.SUCCESS
        assert ex._completed_steps == ["protocol-mapping"]
        assert len(f_next.configs) == 1
        assert not (tmp_path / "diagnostics.md").exists()

    def test_exempt_gate_promoted_to_full_always_passes(self, tmp_path, live_dispatch):
        """validate-config is promoted to FULL but its gate tier is EXEMPT, so
        any artifact content passes."""
        out = tmp_path / "results" / "validate-config-result.json"
        result = _pass_result("validate-config")
        live_dispatch(
            "validate-config", _FakeStepFn(result, artifact=out, artifact_text="")
        )
        ex = PortifyExecutor(
            [_live_step("validate-config", PortifyPhaseType.PREREQUISITES, out)],
            tmp_path,
            config=PortifyConfig(),
        )
        assert ex.run() == PortifyOutcome.SUCCESS
        assert ex._step_results["validate-config"] is result
        assert ex._diagnostics.build_bundle().gate_failures == []
        gate = [e for e in _events(tmp_path) if e["event_type"] == "gate_eval"][0]
        assert gate["tier"] == "EXEMPT"

    def test_full_gate_with_absent_artifact_passes(self, tmp_path, live_dispatch):
        """PortifyGatePolicy treats a missing output file as a gate pass."""
        out = tmp_path / "results" / "component-inventory.md"  # never written
        result = _pass_result("discover-components")
        live_dispatch("discover-components", _FakeStepFn(result))
        ex = PortifyExecutor(
            [_live_step("discover-components", PortifyPhaseType.PREREQUISITES, out)],
            tmp_path,
            config=PortifyConfig(),
            gate_mode=PortifyGateMode.FULL,
        )
        assert ex.run() == PortifyOutcome.SUCCESS
        assert ex._step_results["discover-components"] is result
        assert ex._diagnostics.build_bundle().gate_failures == []


class TestCliNonWritableOutputTerminal:
    """C04 characterization: the live terminal guard for a non-writable output
    is the CLI validation gate (commands.py sys.exit(1)), before run_portify."""

    def test_cli_exits_1_before_run_portify(self, tmp_path, monkeypatch):
        from superclaude.cli.cli_portify.commands import cli_portify_group

        skill = tmp_path / "sc-test-protocol"
        skill.mkdir()
        (skill / "SKILL.md").write_text("# Test Skill\n")
        out = tmp_path / "locked-output"
        out.mkdir()
        out.chmod(stat.S_IRUSR | stat.S_IXUSR)
        called: list = []
        monkeypatch.setattr(
            executor_mod, "run_portify", lambda config: called.append(config)
        )
        try:
            assert not os.access(out, os.W_OK)
            result = CliRunner().invoke(
                cli_portify_group, ["run", str(skill), "--output", str(out)]
            )
        finally:
            out.chmod(stat.S_IRWXU)

        assert result.exit_code == 1
        assert f"Error: Output path is not writable: {out}" in result.output
        assert called == []
