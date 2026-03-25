"""Sequential pipeline executor for CLI Portify.

Implements:
- Sequential step execution loop with step dispatch registry
- --dry-run phase type filtering to PREREQUISITES/ANALYSIS/USER_REVIEW/SPECIFICATION
- --resume <step-id> skip logic with prior results preserved
- Signal handling integration points
- Timeout classification: exit 124 → TIMEOUT
- _determine_status() classification
- Retry mechanism with retry_limit=1
- TurnLedger budget exhaustion → HALTED
- Return contract emission on all outcome paths (PortifyContract builders)
- Gate consultation via GATE_REGISTRY after each step
- ExecutionLog, OutputMonitor, DiagnosticsCollector, PortifyTUI integration
"""

from __future__ import annotations

import concurrent.futures
import signal
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

_T = TypeVar("_T")

import yaml

from superclaude.cli.cli_portify.contract import (
    StepTiming,
    build_dry_run_contract,
    build_failed_contract,
    build_partial_contract,
    build_success_contract,
)
from superclaude.cli.cli_portify.diagnostics import DiagnosticsCollector
from superclaude.cli.cli_portify.gates import (
    GATE_MIN_ENFORCE,
    GateFailure,
    get_gate_criteria,
)
from superclaude.cli.cli_portify.logging_ import ExecutionLog
from superclaude.cli.cli_portify.failures import FAILURE_HANDLERS, has_handler
from superclaude.cli.cli_portify.models import (
    INVALID_PATH,
    GateEvaluation,
    PortifyConfig,
    PortifyGateMode,
    PortifyOutcome,
    PortifyPhaseType,
    PortifyStatus,
    PortifyStep,
    PortifyStepResult,
    PortifyValidationError,
    TurnLedger,
)
from superclaude.cli.pipeline.gates import gate_passed
from superclaude.cli.cli_portify.monitor import OutputMonitor, TimingCapture
from superclaude.cli.cli_portify.steps import get_step_dispatch
from superclaude.cli.cli_portify.tui import PortifyTUI

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Phase types allowed during --dry-run (SC-012)
DRY_RUN_PHASE_TYPES: frozenset[PortifyPhaseType] = frozenset(
    {
        PortifyPhaseType.PREREQUISITES,
        PortifyPhaseType.ANALYSIS,
        PortifyPhaseType.USER_REVIEW,
        PortifyPhaseType.SPECIFICATION,
    }
)

# Exit code constants
EXIT_CODE_TIMEOUT: int = 124
EXIT_RECOMMENDATION_MARKER: str = "EXIT_RECOMMENDATION:"


# ---------------------------------------------------------------------------
# T10.02: _is_dry_run_eligible() — dry-run phase type filter (FR-037, SC-012)
# ---------------------------------------------------------------------------


def _is_dry_run_eligible(step: "PortifyStep") -> bool:
    """Return True if *step* should execute during --dry-run mode.

    Only steps with phase_type in {PREREQUISITES, ANALYSIS, USER_REVIEW,
    SPECIFICATION} are eligible.  SYNTHESIS, REVIEW, OBSERVABILITY,
    INTEGRATION, CONVERGENCE, and VERIFICATION steps are skipped.

    Args:
        step: PortifyStep to evaluate.

    Returns:
        True if the step's phase_type is in DRY_RUN_PHASE_TYPES.
    """
    return step.phase_type in DRY_RUN_PHASE_TYPES


# ---------------------------------------------------------------------------
# Phase 5: STEP_REGISTRY — step definitions with timeout_s (T05.03, NFR-001)
# ---------------------------------------------------------------------------

#: Registry of pipeline steps with per-step timeout budgets.
#: protocol-mapping and analysis-synthesis steps use 600s per NFR-001.
STEP_REGISTRY: dict[str, dict] = {
    "validate-config": {
        "step_id": "validate-config",
        "phase_type": PortifyPhaseType.PREREQUISITES,
        "timeout_s": 30,
        "retry_limit": 0,
    },
    "discover-components": {
        "step_id": "discover-components",
        "phase_type": PortifyPhaseType.PREREQUISITES,
        "timeout_s": 60,
        "retry_limit": 0,
    },
    "protocol-mapping": {
        "step_id": "protocol-mapping",
        "phase_type": PortifyPhaseType.ANALYSIS,
        "timeout_s": 600,
        "retry_limit": 1,
    },
    "analysis-synthesis": {
        "step_id": "analysis-synthesis",
        "phase_type": PortifyPhaseType.ANALYSIS,
        "timeout_s": 600,
        "retry_limit": 1,
    },
    "user-review-p1": {
        "step_id": "user-review-p1",
        "phase_type": PortifyPhaseType.USER_REVIEW,
        "timeout_s": 0,
        "retry_limit": 0,
    },
    # Phase 6: Specification pipeline steps (T06.01–T06.04, FR-020–FR-023, NFR-001)
    "step-graph-design": {
        "step_id": "step-graph-design",
        "phase_type": PortifyPhaseType.SPECIFICATION,
        "timeout_s": 600,
        "retry_limit": 1,
    },
    "models-gates-design": {
        "step_id": "models-gates-design",
        "phase_type": PortifyPhaseType.SPECIFICATION,
        "timeout_s": 600,
        "retry_limit": 1,
    },
    "prompts-executor-design": {
        "step_id": "prompts-executor-design",
        "phase_type": PortifyPhaseType.SPECIFICATION,
        "timeout_s": 600,
        "retry_limit": 1,
    },
    "pipeline-spec-assembly": {
        "step_id": "pipeline-spec-assembly",
        "phase_type": PortifyPhaseType.SPECIFICATION,
        "timeout_s": 600,
        "retry_limit": 1,
    },
    "user-review-p2": {
        "step_id": "user-review-p2",
        "phase_type": PortifyPhaseType.USER_REVIEW,
        "timeout_s": 0,
        "retry_limit": 0,
    },
    # Phase 7: Release spec synthesis step (T07.04, R-051, NFR-001)
    "release-spec-synthesis": {
        "step_id": "release-spec-synthesis",
        "phase_type": PortifyPhaseType.SYNTHESIS,
        "timeout_s": 900,
        "retry_limit": 1,
    },
    # Phase 8: Panel review step — internal convergence loop, no outer retry (T08.06, AC-011, NFR-001)
    "panel-review": {
        "step_id": "panel-review",
        "phase_type": PortifyPhaseType.CONVERGENCE,
        "timeout_s": 1200,
        "retry_limit": 0,
    },
}


# ---------------------------------------------------------------------------
# T02.09: run_with_timeout() — enforce step-level time budgets (NFR-001)
# ---------------------------------------------------------------------------


def run_with_timeout(
    fn: Callable[..., _T], timeout_s: float, *args: Any, **kwargs: Any
) -> _T:
    """Run *fn* in a thread and raise TimeoutError if it exceeds *timeout_s* seconds.

    Used to enforce:
      - SC-001: validate_and_configure() ≤ 30 s
      - SC-002: discover_components()     ≤ 60 s

    Args:
        fn: Callable to execute.
        timeout_s: Maximum allowed wall-clock seconds.
        *args / **kwargs: Forwarded to *fn*.

    Returns:
        The return value of *fn*.

    Raises:
        TimeoutError: If *fn* does not complete within *timeout_s* seconds.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(fn, *args, **kwargs)
        try:
            return future.result(timeout=timeout_s)
        except concurrent.futures.TimeoutError:
            raise TimeoutError(f"Operation timed out after {timeout_s}s")


# ---------------------------------------------------------------------------
# _determine_status()
# ---------------------------------------------------------------------------


def _determine_status(
    exit_code: int,
    timed_out: bool,
    stdout: str = "",
    artifact_path: Optional[Path] = None,
) -> PortifyStatus:
    """Classify a step outcome from exit code, EXIT_RECOMMENDATION, and artifact.

    Classification rules (priority order):
      1. exit 124 (or timed_out=True)  → TIMEOUT
      2. exit non-zero                 → ERROR
      3. exit 0 + marker + artifact    → PASS
      4. exit 0 + no marker + artifact → PASS_NO_SIGNAL  (triggers retry)
      5. exit 0 + artifact, no result  → PASS_NO_REPORT  (no retry)
      6. exit 0 + no artifact          → PASS_NO_REPORT
    """
    if timed_out or exit_code == EXIT_CODE_TIMEOUT:
        return PortifyStatus.TIMEOUT

    if exit_code != 0:
        return PortifyStatus.ERROR

    # exit 0 paths
    has_marker = EXIT_RECOMMENDATION_MARKER in stdout
    artifact_exists = artifact_path is not None and Path(artifact_path).exists()

    if has_marker and artifact_exists:
        return PortifyStatus.PASS

    if not has_marker and artifact_exists:
        return PortifyStatus.PASS_NO_SIGNAL  # triggers retry

    # No artifact (or no result file) → no retry
    return PortifyStatus.PASS_NO_REPORT


# ---------------------------------------------------------------------------
# Return contract helpers (T03.10)
# ---------------------------------------------------------------------------


def _build_resume_command(step_id: str, cli_name: str = "portify") -> str:
    """Build the exact CLI command string for resuming from a step."""
    return f"superclaude cli-portify run --resume {step_id}"


def _calculate_suggested_resume_budget(steps: list[PortifyStep]) -> int:
    """Calculate suggested_resume_budget = remaining_steps_count * 25.

    remaining = steps with PENDING or INCOMPLETE status.
    """
    remaining = sum(
        1
        for s in steps
        if s.status in (PortifyStatus.PENDING, PortifyStatus.INCOMPLETE)
    )
    return remaining * 25


def _emit_return_contract(
    workdir: Path,
    outcome: PortifyOutcome,
    steps: list[PortifyStep],
    completed_steps: list[str],
    resume_from_step_id: str = "",
) -> Path:
    """Emit return-contract.yaml to the workdir on ALL outcome paths (SC-011).

    Returns the path to the emitted file.
    """
    remaining_steps = [
        s.step_id
        for s in steps
        if s.status in (PortifyStatus.PENDING, PortifyStatus.INCOMPLETE)
    ]
    resume_command = (
        _build_resume_command(resume_from_step_id) if resume_from_step_id else ""
    )
    suggested_budget = _calculate_suggested_resume_budget(steps)

    artifacts = [str(s.output_file) for s in steps if s.output_file and Path(s.output_file).exists()]
    step_timings = [
        StepTiming(step_name=s.step_id, duration_seconds=0.0)
        for s in steps
        if s.status not in (PortifyStatus.PENDING, PortifyStatus.SKIPPED)
    ]
    gate_results = {
        s.step_id: s.status.value
        for s in steps
        if s.status not in (PortifyStatus.PENDING, PortifyStatus.SKIPPED)
    }
    total_duration = sum(t.duration_seconds for t in step_timings)

    if outcome == PortifyOutcome.SUCCESS:
        contract_obj = build_success_contract(
            artifacts=artifacts,
            step_timings=step_timings,
            gate_results=gate_results,
            total_duration=total_duration,
        )
    elif outcome == PortifyOutcome.DRY_RUN:
        contract_obj = build_dry_run_contract(
            step_results=[],
            artifacts=artifacts,
            step_timings=step_timings,
            total_duration=total_duration,
        )
    elif outcome in (PortifyOutcome.HALTED, PortifyOutcome.INTERRUPTED):
        contract_obj = build_partial_contract(
            step_results=[],
            artifacts=artifacts,
            step_timings=step_timings,
            gate_results=gate_results,
            total_duration=total_duration,
            resume_step=resume_from_step_id,
        )
    else:
        contract_obj = build_failed_contract(
            step_results=[],
            artifacts=artifacts,
            step_timings=step_timings,
            gate_results=gate_results,
            total_duration=total_duration,
            error_message="pipeline failed",
            resume_step=resume_from_step_id,
        )

    contract = contract_obj.to_dict()
    # Backward-compatible fields still consumed by executor tests
    contract.update(
        {
            "outcome": outcome.value,
            "completed_steps": completed_steps,
            "remaining_steps": remaining_steps,
            "suggested_resume_budget": suggested_budget,
        }
    )
    if resume_command:
        contract["resume_command"] = resume_command

    workdir.mkdir(parents=True, exist_ok=True)
    contract_path = workdir / "return-contract.yaml"
    with open(contract_path, "w") as fh:
        yaml.safe_dump(contract, fh, default_flow_style=False)
    return contract_path


# ---------------------------------------------------------------------------
# PortifyGatePolicy — two-layer gate enforcement
# ---------------------------------------------------------------------------


class PortifyGatePolicy:
    """Two-layer gate enforcement for the portify pipeline.

    Layer 1 (global mode): shadow/soft/full baseline for all gates.
    Layer 2 (per-gate promotion): individual gates can override upward.
    """

    def __init__(
        self, global_mode: PortifyGateMode = PortifyGateMode.SHADOW
    ) -> None:
        self._global_mode = global_mode

    def evaluate(
        self,
        step_id: str,
        output_file: Path | None,
        min_enforce_mode: PortifyGateMode = PortifyGateMode.SHADOW,
    ) -> GateEvaluation:
        effective = max(self._global_mode, min_enforce_mode)

        try:
            criteria = get_gate_criteria(step_id)
        except KeyError:
            return GateEvaluation(
                step_id=step_id,
                gate_id=step_id,
                tier="NONE",
                passed=True,
                reason=None,
                effective_mode=effective,
                blocked=False,
            )

        tier = getattr(criteria, "enforcement_tier", "STANDARD")
        gate_id = getattr(criteria, "gate_id", step_id)

        if output_file is None or not output_file.exists():
            passed, reason = True, None
        else:
            passed, reason = gate_passed(output_file, criteria)

        blocked = (not passed) and (effective == PortifyGateMode.FULL)

        failure = None
        if not passed:
            failure = GateFailure(
                gate_id=gate_id,
                check_name="gate_passed",
                diagnostic=reason or "",
                artifact_path=str(output_file) if output_file else "",
                tier=tier,
            )

        return GateEvaluation(
            step_id=step_id,
            gate_id=gate_id,
            tier=tier,
            passed=passed,
            reason=reason,
            effective_mode=effective,
            blocked=blocked,
            failure=failure,
        )


# ---------------------------------------------------------------------------
# PortifyExecutor
# ---------------------------------------------------------------------------


class PortifyExecutor:
    """Sequential pipeline executor for CLI Portify.

    Usage:
        executor = PortifyExecutor(steps, workdir, dry_run=False)
        outcome = executor.run()
    """

    def __init__(
        self,
        steps: list[PortifyStep],
        workdir: Path,
        *,
        config: Optional[PortifyConfig] = None,
        dry_run: bool = False,
        resume_from: str = "",
        turn_budget: int = 200,
        step_runner: Optional[Callable[[PortifyStep], tuple[int, str, bool]]] = None,
        gate_mode: PortifyGateMode = PortifyGateMode.SHADOW,
    ) -> None:
        """
        Args:
            steps: Ordered list of steps in registered order.
            workdir: Working directory for artifacts and return contract.
            config: The PortifyConfig for this run (passed to step dispatch functions).
            dry_run: If True, filter execution to DRY_RUN_PHASE_TYPES only.
            resume_from: Step ID to resume from (skip all prior steps).
            turn_budget: Total Claude-invocation budget (TurnLedger).
            step_runner: Optional callable (step) -> (exit_code, stdout, timed_out).
                         Used for testing; real runs use step dispatch.
            gate_mode: Gate enforcement mode (shadow/soft/full).
        """
        self.steps = steps
        self.workdir = workdir
        self._config = config
        self.dry_run = dry_run
        self.resume_from = resume_from
        self._ledger = TurnLedger(total_budget=turn_budget)
        self._step_runner = step_runner
        self._interrupted: bool = False
        self._completed_steps: list[str] = []
        self._step_results: dict[str, PortifyStepResult] = {}
        self._execution_log = ExecutionLog(workdir)
        self._timing = TimingCapture()
        self._diagnostics = DiagnosticsCollector()
        self._monitor = OutputMonitor(stall_timeout_seconds=float(config.stall_timeout) if config else 60.0)
        self._tui = PortifyTUI()
        self._gate_policy = PortifyGatePolicy(global_mode=gate_mode)

        # Signal handler integration points (T03.04 / T03.09)
        self._prev_sigint: Optional[Callable] = None
        self._prev_sigterm: Optional[Callable] = None

    # ------------------------------------------------------------------
    # Signal handling (T03.09)
    # ------------------------------------------------------------------

    def _install_signal_handlers(self) -> None:
        """Register SIGINT / SIGTERM handlers for graceful shutdown."""

        def _handle(signum: int, frame) -> None:
            self._interrupted = True
            signal_name = signal.Signals(signum).name if signum in signal.Signals.__members__.values() else str(signum)
            self._execution_log.signal_received(signal_name)

        try:
            self._prev_sigint = signal.signal(signal.SIGINT, _handle)
            self._prev_sigterm = signal.signal(signal.SIGTERM, _handle)
        except (OSError, ValueError):
            # Non-main thread or OS doesn't support — skip gracefully
            pass

    def _restore_signal_handlers(self) -> None:
        """Restore prior signal handlers after execution."""
        try:
            if self._prev_sigint is not None:
                signal.signal(signal.SIGINT, self._prev_sigint)
            if self._prev_sigterm is not None:
                signal.signal(signal.SIGTERM, self._prev_sigterm)
        except (OSError, ValueError):
            pass

    # ------------------------------------------------------------------
    # Step filtering
    # ------------------------------------------------------------------

    def _should_execute(self, step: PortifyStep) -> bool:
        """Return True if this step should be executed given current mode."""
        if self.dry_run:
            return _is_dry_run_eligible(step)
        return True

    def _should_skip_for_resume(self, step: PortifyStep, resume_started: bool) -> bool:
        """Return True if this step should be skipped because --resume hasn't reached it."""
        return not resume_started

    # ------------------------------------------------------------------
    # Step execution
    # ------------------------------------------------------------------

    def _execute_step(self, step: PortifyStep) -> PortifyStatus:
        """Execute a single step via the dispatch registry or test runner.

        If a step_runner was provided (testing), uses that. Otherwise dispatches
        to the step module's run_*() function via get_step_dispatch().
        """
        if self._step_runner is not None:
            # Testing path: use injected runner
            exit_code, stdout, timed_out = self._step_runner(step)
            artifact_path = step.output_file
            status = _determine_status(exit_code, timed_out, stdout, artifact_path)
            self._ledger.consume(1)

            # Retry once on PASS_NO_SIGNAL (retry_limit=1 per NFR-002)
            if status == PortifyStatus.PASS_NO_SIGNAL and step.retry_limit >= 1:
                if self._ledger.can_launch():
                    exit_code, stdout, timed_out = self._step_runner(step)
                    self._ledger.consume(1)
                    status = _determine_status(exit_code, timed_out, stdout, artifact_path)
            return status

        # Production path: dispatch to step module
        dispatch = get_step_dispatch()
        step_fn = dispatch.get(step.step_id)
        if step_fn is None:
            return PortifyStatus.ERROR

        self._ledger.consume(1)
        self._execution_log.step_start(step.step_id)
        self._timing.start_step(step.step_id)
        self._tui.step_start(step.step_id)
        result = step_fn(self._config)
        self._timing.end_step(step.step_id)

        # Two-layer gate enforcement: global mode + per-gate promotion
        gate_min = GATE_MIN_ENFORCE.get(step.step_id, PortifyGateMode.SHADOW)
        gate_eval = self._gate_policy.evaluate(step.step_id, step.output_file, gate_min)

        self._execution_log.gate_eval(
            step.step_id,
            gate_id=gate_eval.gate_id,
            tier=gate_eval.tier,
        )

        if not gate_eval.passed:
            if gate_eval.effective_mode == PortifyGateMode.SOFT:
                self._tui.gate_warning(step.step_id, gate_eval.reason)
            elif gate_eval.effective_mode == PortifyGateMode.FULL:
                if gate_eval.failure is not None:
                    self._diagnostics.record_gate_failure(gate_eval.failure)
                return PortifyStatus.HALT
        # Shadow mode: result logged above, no further action

        gate_result = "pass" if gate_eval.passed else gate_eval.effective_mode.name.lower()

        timing = self._timing.get_step_timing(step.step_id)
        duration = timing.duration_seconds if timing is not None else 0.0
        self._execution_log.step_end(step.step_id, status=result.portify_status.value, duration_s=duration)
        self._tui.step_complete(step.step_id, result.portify_status.value, duration, gate_result)

        if result.portify_status in (PortifyStatus.ERROR, PortifyStatus.FAIL, PortifyStatus.TIMEOUT):
            if result.error_message:
                self._diagnostics.record_exit_code(1)
            if result.artifact_path and not Path(result.artifact_path).exists():
                self._diagnostics.record_missing_artifact(result.artifact_path)
            if result.resume_context.resume_command:
                self._diagnostics.set_resume_guidance(result.resume_context.resume_command)

            # Dispatch to registered failure handler if classification is available
            if result.failure_classification and has_handler(result.failure_classification):
                handler = FAILURE_HANDLERS[result.failure_classification]
                if handler is not None:
                    self._execution_log.failure_handler(
                        step.step_id,
                        handler_name=handler.__name__,
                        classification=result.failure_classification.value,
                    )

        # Store the step result for contract emission
        self._step_results[step.step_id] = result
        return result.portify_status

    # ------------------------------------------------------------------
    # Main execution loop
    # ------------------------------------------------------------------

    def run(self) -> PortifyOutcome:
        """Execute all steps sequentially. Returns pipeline outcome."""
        self._install_signal_handlers()
        self._timing.start_pipeline()
        self._tui.start()
        outcome = PortifyOutcome.SUCCESS
        resume_started = self.resume_from == ""  # True if no resume target

        try:
            for step in self.steps:
                # Check for interrupt before each step
                if self._interrupted:
                    outcome = PortifyOutcome.INTERRUPTED
                    break

                # Resume skip logic
                if not resume_started:
                    if step.step_id == self.resume_from:
                        resume_started = True
                    else:
                        step.status = PortifyStatus.SKIPPED
                        continue

                # Dry-run filtering
                if not self._should_execute(step):
                    step.status = PortifyStatus.SKIPPED
                    continue

                # Budget check before launch (FR-040)
                if not self._ledger.can_launch():
                    outcome = PortifyOutcome.HALTED
                    break

                step.status = PortifyStatus.RUNNING
                status = self._execute_step(step)
                step.status = status

                if status in (
                    PortifyStatus.PASS,
                    PortifyStatus.PASS_NO_SIGNAL,
                    PortifyStatus.PASS_NO_REPORT,
                ):
                    self._completed_steps.append(step.step_id)
                elif status == PortifyStatus.TIMEOUT:
                    outcome = PortifyOutcome.TIMEOUT
                    break
                elif status == PortifyStatus.ERROR:
                    outcome = PortifyOutcome.FAILURE
                    break

                # Check interrupt after step completes
                if self._interrupted:
                    outcome = PortifyOutcome.INTERRUPTED
                    break

        finally:
            self._timing.end_pipeline()
            self._restore_signal_handlers()
            self._tui.stop()
            # Determine resume step (first non-completed step)
            resume_step = ""
            for s in self.steps:
                if s.status in (PortifyStatus.PENDING, PortifyStatus.INCOMPLETE):
                    resume_step = s.step_id
                    break

            final_outcome = outcome if not self.dry_run else PortifyOutcome.DRY_RUN
            self._execution_log.pipeline_outcome(final_outcome.value)
            self._execution_log.flush(status=final_outcome.value, elapsed=self._timing.total_duration)

            if final_outcome in (PortifyOutcome.FAILURE, PortifyOutcome.TIMEOUT, PortifyOutcome.HALTED):
                self._diagnostics.emit_diagnostics(self.workdir, step_id=resume_step)

            _emit_return_contract(
                workdir=self.workdir,
                outcome=final_outcome,
                steps=self.steps,
                completed_steps=self._completed_steps,
                resume_from_step_id=resume_step,
            )

        return outcome



# ---------------------------------------------------------------------------
# T10.01: run_portify() — top-level entry point called by commands.py (FR-049)
# ---------------------------------------------------------------------------


# Known artifact names per step ID for output_file assignment
_STEP_ARTIFACT_NAMES: dict[str, str] = {
    "validate-config": "validate-config-result.json",
    "discover-components": "component-inventory.md",
    "protocol-mapping": "portify-analysis.md",
    "analysis-synthesis": "portify-analysis.md",
    "step-graph-design": "portify-spec.md",
    "models-gates-design": "portify-spec.md",
    "prompts-executor-design": "portify-spec.md",
    "pipeline-spec-assembly": "portify-spec.md",
    "release-spec-synthesis": "synthesized-spec.md",
    "brainstorm-gaps": "brainstorm-gaps.md",
    "panel-review": "panel-reviewed-spec.md",
}


def run_portify(config: PortifyConfig) -> PortifyOutcome:
    """Execute the full portify pipeline from a resolved PortifyConfig.

    Builds steps from STEP_REGISTRY, constructs a PortifyExecutor, and runs it.
    Returns the outcome for use by the CLI command.

    Args:
        config: Fully resolved PortifyConfig (from load_portify_config).

    Returns:
        PortifyOutcome indicating pipeline result.
    """
    from superclaude.cli.cli_portify.resume import validate_resume_entry
    from superclaude.cli.cli_portify.workdir import (
        create_workdir,
        emit_portify_config_yaml,
    )

    # Create workdir if not already set
    if config.workdir_path is None:
        workdir = create_workdir(config)
        config.workdir_path = workdir
    workdir = Path(config.workdir_path)

    # Emit workdir config artifact
    emit_portify_config_yaml(config, workdir)

    # Validate resume prerequisites before execution
    if config.resume_from:
        valid, missing, _preserved = validate_resume_entry(config.resume_from, workdir)
        if not valid:
            raise PortifyValidationError(
                INVALID_PATH,
                f"Cannot resume from {config.resume_from}",
                ", ".join(missing),
            )

    # Ensure results dir exists
    results_dir = workdir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # Also set output_dir if not set (steps use config.output_dir / "results")
    if config.output_dir is None:
        config.output_dir = workdir

    steps = []
    for entry in STEP_REGISTRY.values():
        step_id = entry["step_id"]
        artifact_name = _STEP_ARTIFACT_NAMES.get(step_id, "")
        output_file = results_dir / artifact_name if artifact_name else None
        error_file = results_dir / f"{step_id}.err" if artifact_name else None

        steps.append(
            PortifyStep(
                step_id=step_id,
                phase_type=entry["phase_type"],
                timeout_seconds=entry.get("timeout_s", 300),
                retry_limit=entry.get("retry_limit", 0),
                output_file=output_file,
                error_file=error_file,
            )
        )

    gate_mode_enum = PortifyGateMode[config.gate_mode.upper()]
    executor = PortifyExecutor(
        steps=steps,
        workdir=workdir,
        config=config,
        dry_run=config.dry_run,
        resume_from=config.resume_from,
        turn_budget=config.max_turns,
        gate_mode=gate_mode_enum,
    )
    return executor.run()
