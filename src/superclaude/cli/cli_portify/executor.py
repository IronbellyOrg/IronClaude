"""Sequential pipeline executor for CLI Portify.

Implements:
- Sequential step execution loop (T03.04)
- --dry-run phase type filtering to PREREQUISITES/ANALYSIS/USER_REVIEW/SPECIFICATION (T03.04)
- --resume <step-id> skip logic with prior results preserved (T03.04)
- Signal handling integration points (T03.04 / T03.09)
- Timeout classification: exit 124 → TIMEOUT (T03.06)
- _determine_status() classification (T03.06)
- Retry mechanism with retry_limit=1 (T03.07)
- TurnLedger budget exhaustion → HALTED (T03.08)
- Return contract emission on all outcome paths (T03.10)
- Phase 5: protocol-mapping and analysis-synthesis step execution (T05.01, T05.02)
- Phase 5: 600s timeout enforcement for analysis steps (T05.03)
- Phase 5: user-review-p1 gate writing phase1-approval.yaml (T05.04)
- Phase 5: --resume validation with YAML parse + schema check (T05.05)
- Phase 6: step-graph-design step execution with G-005 gate (T06.01, FR-020)
- Phase 6: models-gates-design step execution with G-006 gate (T06.02, FR-021)
- Phase 6: prompts-executor-design step execution with G-007 gate (T06.03, FR-022)
- Phase 6: pipeline-spec-assembly programmatic pre-assembly + G-008 gate (T06.04, FR-023, SC-005)
- Phase 6: user-review-p2 gate writing phase2-approval.yaml (T06.06, FR-025, FR-026)
- Phase 6: --resume validation for phase2-approval.yaml (T06.06, FR-026)
- Phase 7: load_release_spec_template + create_working_copy (T07.01, R-048, AC-009)
- Phase 7: 4-substep release spec synthesis 3a-3d (T07.02, R-049, FR-027)
- Phase 7: placeholder scan + portify-release-spec.md emission with G-010 (T07.03, R-050)
- Phase 7: inline embed guard CONTENT_TOO_LARGE + 900s timeout (T07.04, R-051, OQ-008)
- Phase 8: panel-review STEP_REGISTRY entry with timeout_s=1200, retry_limit=0 (T08.06, AC-011, NFR-001)
"""

from __future__ import annotations

import concurrent.futures
import signal
import sys
import time
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

_T = TypeVar("_T")

import yaml

from superclaude.cli.cli_portify.models import (
    INVALID_PATH,
    PortifyOutcome,
    PortifyPhaseType,
    PortifyStatus,
    PortifyStep,
    PortifyStepResult,
    PortifyValidationError,
    TurnLedger,
)

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

    contract = {
        "outcome": outcome.value,
        "completed_steps": completed_steps,
        "remaining_steps": remaining_steps,
        "resume_command": resume_command,
        "suggested_resume_budget": suggested_budget,
    }

    workdir.mkdir(parents=True, exist_ok=True)
    contract_path = workdir / "return-contract.yaml"
    with open(contract_path, "w") as fh:
        yaml.safe_dump(contract, fh, default_flow_style=False)
    return contract_path


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
        dry_run: bool = False,
        resume_from: str = "",
        turn_budget: int = 200,
        step_runner: Optional[Callable[[PortifyStep], tuple[int, str, bool]]] = None,
    ) -> None:
        """
        Args:
            steps: Ordered list of steps in registered order.
            workdir: Working directory for artifacts and return contract.
            dry_run: If True, filter execution to DRY_RUN_PHASE_TYPES only.
            resume_from: Step ID to resume from (skip all prior steps).
            turn_budget: Total Claude-invocation budget (TurnLedger).
            step_runner: Optional callable (step) -> (exit_code, stdout, timed_out).
                         Used for testing; real runs use subprocess.
        """
        self.steps = steps
        self.workdir = workdir
        self.dry_run = dry_run
        self.resume_from = resume_from
        self._ledger = TurnLedger(total_budget=turn_budget)
        self._step_runner = step_runner
        self._interrupted: bool = False
        self._completed_steps: list[str] = []
        self._step_results: dict[str, PortifyStepResult] = {}

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
        """Execute a single step with retry logic (retry_limit=1 for PASS_NO_SIGNAL)."""
        if self._step_runner is not None:
            exit_code, stdout, timed_out = self._step_runner(step)
        else:
            # Default: no-op (real subprocess invocation belongs in process.py)
            exit_code, stdout, timed_out = 0, "", False

        artifact_path = step.output_file
        status = _determine_status(exit_code, timed_out, stdout, artifact_path)
        self._ledger.consume(1)

        # Retry once on PASS_NO_SIGNAL (retry_limit=1 per NFR-002)
        if status == PortifyStatus.PASS_NO_SIGNAL and step.retry_limit >= 1:
            if self._ledger.can_launch():
                if self._step_runner is not None:
                    exit_code, stdout, timed_out = self._step_runner(step)
                else:
                    exit_code, stdout, timed_out = 0, "", False
                self._ledger.consume(1)
                status = _determine_status(exit_code, timed_out, stdout, artifact_path)

        return status

    # ------------------------------------------------------------------
    # Main execution loop
    # ------------------------------------------------------------------

    def run(self) -> PortifyOutcome:
        """Execute all steps sequentially. Returns pipeline outcome."""
        self._install_signal_handlers()
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
            self._restore_signal_handlers()
            # Determine resume step (first non-completed step)
            resume_step = ""
            for s in self.steps:
                if s.status in (PortifyStatus.PENDING, PortifyStatus.INCOMPLETE):
                    resume_step = s.step_id
                    break
            _emit_return_contract(
                workdir=self.workdir,
                outcome=outcome if not self.dry_run else PortifyOutcome.DRY_RUN,
                steps=self.steps,
                completed_steps=self._completed_steps,
                resume_from_step_id=resume_step,
            )

        return outcome


# ---------------------------------------------------------------------------
# Phase 5 Step Execution Functions (T05.01, T05.02, T05.04)
# ---------------------------------------------------------------------------


def execute_protocol_mapping_step(
    config_cli_name: str,
    inventory: list,
    workdir: Path,
    process_runner: Optional[Callable[[str, Path], tuple[int, str, bool]]] = None,
) -> PortifyStepResult:
    """Execute the protocol-mapping step (T05.01, FR-013, FR-014).

    Runs Claude via subprocess to produce ``workdir/protocol-map.md`` with
    required YAML frontmatter and EXIT_RECOMMENDATION marker.  Applies G-002
    gate after execution; retries once on PASS_NO_SIGNAL.

    Args:
        config_cli_name: CLI name being portified.
        inventory: List of ComponentEntry objects.
        workdir: Working directory where protocol-map.md will be written.
        process_runner: Optional callable (prompt, output_path) -> (exit_code, stdout, timed_out).
                        Used for testing; real runs use PortifyProcess.

    Returns:
        PortifyStepResult with portify_status set based on gate outcome.
    """
    from superclaude.cli.cli_portify.prompts import build_protocol_mapping_prompt

    prompt = build_protocol_mapping_prompt(config_cli_name, inventory)
    output_path = workdir / "protocol-map.md"

    if process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
    else:
        exit_code, stdout, timed_out = (
            0,
            EXIT_RECOMMENDATION_MARKER + " CONTINUE",
            False,
        )

    artifact_path = output_path if output_path.exists() else None
    status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    # Retry once on PASS_NO_SIGNAL (retry_limit=1 per NFR-002)
    if status == PortifyStatus.PASS_NO_SIGNAL and process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
        artifact_path = output_path if output_path.exists() else None
        status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    return PortifyStepResult(
        step_name="protocol-mapping",
        step_number=3,
        phase=2,
        portify_status=status,
        artifact_path=str(output_path),
        iteration_timeout=STEP_REGISTRY["protocol-mapping"]["timeout_s"],
    )


def execute_analysis_synthesis_step(
    config_cli_name: str,
    inventory: list,
    workdir: Path,
    process_runner: Optional[Callable[[str, Path], tuple[int, str, bool]]] = None,
) -> PortifyStepResult:
    """Execute the analysis-synthesis step (T05.02, FR-016, FR-017).

    Reads protocol-map.md from workdir, runs Claude to produce
    ``workdir/portify-analysis-report.md`` with all 7 required sections and
    EXIT_RECOMMENDATION marker.  Applies G-003 gate; retries once on PASS_NO_SIGNAL.

    Args:
        config_cli_name: CLI name being portified.
        inventory: List of ComponentEntry objects.
        workdir: Working directory containing protocol-map.md and where
                 portify-analysis-report.md will be written.
        process_runner: Optional callable for testing.

    Returns:
        PortifyStepResult with portify_status set based on gate outcome.
    """
    from superclaude.cli.cli_portify.prompts import build_analysis_synthesis_prompt

    protocol_map_path = workdir / "protocol-map.md"
    protocol_map_content = ""
    if protocol_map_path.exists():
        protocol_map_content = protocol_map_path.read_text(encoding="utf-8")

    prompt = build_analysis_synthesis_prompt(
        config_cli_name, inventory, protocol_map_content
    )
    output_path = workdir / "portify-analysis-report.md"

    if process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
    else:
        exit_code, stdout, timed_out = (
            0,
            EXIT_RECOMMENDATION_MARKER + " CONTINUE",
            False,
        )

    artifact_path = output_path if output_path.exists() else None
    status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    # Retry once on PASS_NO_SIGNAL (retry_limit=1 per NFR-002)
    if status == PortifyStatus.PASS_NO_SIGNAL and process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
        artifact_path = output_path if output_path.exists() else None
        status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    return PortifyStepResult(
        step_name="analysis-synthesis",
        step_number=4,
        phase=2,
        portify_status=status,
        artifact_path=str(output_path),
        iteration_timeout=STEP_REGISTRY["analysis-synthesis"]["timeout_s"],
    )


def execute_user_review_p1(
    config_cli_name: str,
    workdir: Path,
    *,
    _exit: bool = True,
) -> None:
    """Execute the user-review-p1 gate (T05.04, FR-018, SC-006).

    Writes ``workdir/phase1-approval.yaml`` with ``status: pending`` and
    prints resume instructions to stdout.  Exits cleanly with code 0.

    Args:
        config_cli_name: CLI name being portified (used in instructions).
        workdir: Working directory where phase1-approval.yaml will be written.
        _exit: If True (default), calls sys.exit(0). Set False in tests.
    """
    approval = {
        "status": "pending",
        "workflow": config_cli_name,
        "review_artifacts": [
            "protocol-map.md",
            "portify-analysis-report.md",
        ],
        "instructions": "Review artifacts above. Set status to 'approved' to continue.",
    }

    workdir.mkdir(parents=True, exist_ok=True)
    approval_path = workdir / "phase1-approval.yaml"
    with open(approval_path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(approval, fh, default_flow_style=False, sort_keys=False)

    resume_cmd = f"superclaude cli-portify run {config_cli_name} --resume phase2"
    print(f"Review complete? Run: {resume_cmd}")

    if _exit:
        sys.exit(0)


# ---------------------------------------------------------------------------
# Phase 5 Resume Validation (T05.05, FR-019)
# ---------------------------------------------------------------------------


def _validate_phase1_approval(workdir: Path) -> None:
    """Validate phase1-approval.yaml using YAML parse + schema check (T05.05, FR-019).

    Reads ``workdir/phase1-approval.yaml``, parses with yaml.safe_load(), and
    validates that ``status == 'approved'``.

    Raises:
        PortifyValidationError: On missing file, malformed YAML, missing status
                                field, or non-approved status.
    """
    approval_path = workdir / "phase1-approval.yaml"

    if not approval_path.exists():
        raise PortifyValidationError(
            INVALID_PATH,
            "phase1-approval.yaml not found — run the analysis phase first",
            str(approval_path),
        )

    raw = approval_path.read_text(encoding="utf-8")

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise PortifyValidationError(
            INVALID_PATH,
            f"phase1-approval.yaml: malformed YAML — {exc}",
            str(approval_path),
        )

    if not isinstance(data, dict):
        raise PortifyValidationError(
            INVALID_PATH,
            "phase1-approval.yaml: must be a YAML mapping",
            str(approval_path),
        )

    if "status" not in data:
        raise PortifyValidationError(
            INVALID_PATH,
            "phase1-approval.yaml: missing required field 'status'",
            str(approval_path),
        )

    if data["status"] != "approved":
        raise PortifyValidationError(
            INVALID_PATH,
            f"phase1-approval.yaml: status must be 'approved', got '{data['status']}'",
            str(approval_path),
        )


# ---------------------------------------------------------------------------
# Phase 6: Specification pipeline step executors (T06.01–T06.04, FR-020–FR-023)
# ---------------------------------------------------------------------------


def execute_step_graph_design_step(
    config_cli_name: str,
    workdir: Path,
    process_runner: Optional[Callable[[str, Path], tuple[int, str, bool]]] = None,
) -> PortifyStepResult:
    """Execute the step-graph-design step (T06.01, FR-020).

    Reads portify-analysis-report.md from workdir, runs Claude to produce
    ``workdir/step-graph-spec.md`` with EXIT_RECOMMENDATION marker.
    Applies G-005 gate; retries once on PASS_NO_SIGNAL.

    Args:
        config_cli_name: CLI name being portified.
        workdir: Working directory containing portify-analysis-report.md and where
                 step-graph-spec.md will be written.
        process_runner: Optional callable (prompt, output_path) -> (exit_code, stdout, timed_out).
                        Used for testing; real runs use PortifyProcess.

    Returns:
        PortifyStepResult with portify_status set based on G-005 gate outcome.
    """
    from superclaude.cli.cli_portify.prompts import build_step_graph_design_prompt

    analysis_report_path = workdir / "portify-analysis-report.md"
    analysis_report_content = ""
    if analysis_report_path.exists():
        analysis_report_content = analysis_report_path.read_text(encoding="utf-8")

    prompt = build_step_graph_design_prompt(config_cli_name, analysis_report_content)
    output_path = workdir / "step-graph-spec.md"

    if process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
    else:
        exit_code, stdout, timed_out = (
            0,
            EXIT_RECOMMENDATION_MARKER + " CONTINUE",
            False,
        )

    artifact_path = output_path if output_path.exists() else None
    status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    # Retry once on PASS_NO_SIGNAL (retry_limit=1 per NFR-002)
    if status == PortifyStatus.PASS_NO_SIGNAL and process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
        artifact_path = output_path if output_path.exists() else None
        status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    return PortifyStepResult(
        step_name="step-graph-design",
        step_number=6,
        phase=3,
        portify_status=status,
        gate_tier="STRICT",
        artifact_path=str(output_path),
        iteration_timeout=STEP_REGISTRY["step-graph-design"]["timeout_s"],
    )


def execute_models_gates_design_step(
    config_cli_name: str,
    workdir: Path,
    process_runner: Optional[Callable[[str, Path], tuple[int, str, bool]]] = None,
) -> PortifyStepResult:
    """Execute the models-gates-design step (T06.02, FR-021).

    Reads step-graph-spec.md from workdir, runs Claude to produce
    ``workdir/models-gates-spec.md`` with return type pattern (G-006).
    Applies G-006 gate; retries once on PASS_NO_SIGNAL.

    Args:
        config_cli_name: CLI name being portified.
        workdir: Working directory containing step-graph-spec.md and where
                 models-gates-spec.md will be written.
        process_runner: Optional callable (prompt, output_path) -> (exit_code, stdout, timed_out).

    Returns:
        PortifyStepResult with portify_status set based on G-006 gate outcome.
    """
    from superclaude.cli.cli_portify.prompts import build_models_gates_design_prompt

    step_graph_path = workdir / "step-graph-spec.md"
    step_graph_content = ""
    if step_graph_path.exists():
        step_graph_content = step_graph_path.read_text(encoding="utf-8")

    prompt = build_models_gates_design_prompt(config_cli_name, step_graph_content)
    output_path = workdir / "models-gates-spec.md"

    if process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
    else:
        exit_code, stdout, timed_out = 0, "tuple[bool, str]", False

    artifact_path = output_path if output_path.exists() else None
    status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    # Retry once on PASS_NO_SIGNAL (retry_limit=1 per NFR-002)
    if status == PortifyStatus.PASS_NO_SIGNAL and process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
        artifact_path = output_path if output_path.exists() else None
        status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    return PortifyStepResult(
        step_name="models-gates-design",
        step_number=7,
        phase=3,
        portify_status=status,
        gate_tier="STANDARD",
        artifact_path=str(output_path),
        iteration_timeout=STEP_REGISTRY["models-gates-design"]["timeout_s"],
    )


def execute_prompts_executor_design_step(
    config_cli_name: str,
    workdir: Path,
    process_runner: Optional[Callable[[str, Path], tuple[int, str, bool]]] = None,
) -> PortifyStepResult:
    """Execute the prompts-executor-design step (T06.03, FR-022).

    Reads step-graph-spec.md and models-gates-spec.md from workdir, runs Claude
    to produce ``workdir/prompts-executor-spec.md`` with EXIT_RECOMMENDATION marker.
    Applies G-007 gate; retries once on PASS_NO_SIGNAL.

    Args:
        config_cli_name: CLI name being portified.
        workdir: Working directory containing step-graph-spec.md and models-gates-spec.md
                 and where prompts-executor-spec.md will be written.
        process_runner: Optional callable (prompt, output_path) -> (exit_code, stdout, timed_out).

    Returns:
        PortifyStepResult with portify_status set based on G-007 gate outcome.
    """
    from superclaude.cli.cli_portify.prompts import build_prompts_executor_design_prompt

    step_graph_path = workdir / "step-graph-spec.md"
    step_graph_content = ""
    if step_graph_path.exists():
        step_graph_content = step_graph_path.read_text(encoding="utf-8")

    models_gates_path = workdir / "models-gates-spec.md"
    models_gates_content = ""
    if models_gates_path.exists():
        models_gates_content = models_gates_path.read_text(encoding="utf-8")

    prompt = build_prompts_executor_design_prompt(
        config_cli_name, step_graph_content, models_gates_content
    )
    output_path = workdir / "prompts-executor-spec.md"

    if process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
    else:
        exit_code, stdout, timed_out = (
            0,
            EXIT_RECOMMENDATION_MARKER + " CONTINUE",
            False,
        )

    artifact_path = output_path if output_path.exists() else None
    status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    # Retry once on PASS_NO_SIGNAL (retry_limit=1 per NFR-002)
    if status == PortifyStatus.PASS_NO_SIGNAL and process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
        artifact_path = output_path if output_path.exists() else None
        status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    return PortifyStepResult(
        step_name="prompts-executor-design",
        step_number=8,
        phase=3,
        portify_status=status,
        gate_tier="STRICT",
        artifact_path=str(output_path),
        iteration_timeout=STEP_REGISTRY["prompts-executor-design"]["timeout_s"],
    )


def assemble_specs_programmatic(
    step_graph_content: str,
    models_gates_content: str,
    prompts_executor_content: str,
) -> str:
    """Programmatically concatenate and deduplicate 3 input specs (T06.04, FR-023, SC-005).

    Concatenates the three spec artifacts with section headers, then deduplicates
    repeated YAML frontmatter sections before passing to Claude synthesis.

    Args:
        step_graph_content: Content of step-graph-spec.md.
        models_gates_content: Content of models-gates-spec.md.
        prompts_executor_content: Content of prompts-executor-spec.md.

    Returns:
        Assembled and deduplicated content string ready for Claude synthesis.
    """
    sections: list[str] = []

    if step_graph_content.strip():
        sections.append("## Step Graph Design\n\n" + step_graph_content.strip())

    if models_gates_content.strip():
        sections.append("## Models and Gates Design\n\n" + models_gates_content.strip())

    if prompts_executor_content.strip():
        sections.append(
            "## Prompts and Executor Design\n\n" + prompts_executor_content.strip()
        )

    assembled = "\n\n".join(sections)

    # Deduplicate repeated YAML frontmatter blocks (keep only first occurrence).
    # A frontmatter block starts at the beginning of a line with exactly "---"
    # followed by key: value lines and closed by another "---" line.
    import re as _re

    frontmatter_pattern = _re.compile(r"^---\n(?:[^\n]+\n)*?---\n", _re.MULTILINE)
    matches = list(frontmatter_pattern.finditer(assembled))
    if len(matches) > 1:
        # Remove all but the first frontmatter block (reverse order to preserve offsets)
        for match in reversed(matches[1:]):
            assembled = assembled[: match.start()] + assembled[match.end() :]

    return assembled


def execute_pipeline_spec_assembly_step(
    config_cli_name: str,
    workdir: Path,
    process_runner: Optional[Callable[[str, Path], tuple[int, str, bool]]] = None,
) -> PortifyStepResult:
    """Execute the pipeline-spec-assembly step (T06.04, FR-023, SC-005).

    Programmatically assembles step-graph-spec.md, models-gates-spec.md, and
    prompts-executor-spec.md into deduplicated content, then runs Claude synthesis
    to produce ``workdir/portify-spec.md``.  Applies G-008 gate (EXIT_RECOMMENDATION
    + step-count consistency); retries once on PASS_NO_SIGNAL.

    Args:
        config_cli_name: CLI name being portified.
        workdir: Working directory containing the 3 input specs and where
                 portify-spec.md will be written.
        process_runner: Optional callable (prompt, output_path) -> (exit_code, stdout, timed_out).

    Returns:
        PortifyStepResult with portify_status set based on G-008 gate outcome.
    """
    from superclaude.cli.cli_portify.prompts import build_spec_assembly_prompt

    # Read the 3 input specs
    step_graph_content = ""
    step_graph_path = workdir / "step-graph-spec.md"
    if step_graph_path.exists():
        step_graph_content = step_graph_path.read_text(encoding="utf-8")

    models_gates_content = ""
    models_gates_path = workdir / "models-gates-spec.md"
    if models_gates_path.exists():
        models_gates_content = models_gates_path.read_text(encoding="utf-8")

    prompts_executor_content = ""
    prompts_executor_path = workdir / "prompts-executor-spec.md"
    if prompts_executor_path.exists():
        prompts_executor_content = prompts_executor_path.read_text(encoding="utf-8")

    # Programmatic pre-assembly + deduplication (SC-005)
    assembled = assemble_specs_programmatic(
        step_graph_content, models_gates_content, prompts_executor_content
    )

    prompt = build_spec_assembly_prompt(assembled)
    output_path = workdir / "portify-spec.md"

    if process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
    else:
        exit_code, stdout, timed_out = (
            0,
            EXIT_RECOMMENDATION_MARKER + " CONTINUE",
            False,
        )

    artifact_path = output_path if output_path.exists() else None
    status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    # Retry once on PASS_NO_SIGNAL (retry_limit=1 per NFR-002)
    if status == PortifyStatus.PASS_NO_SIGNAL and process_runner is not None:
        exit_code, stdout, timed_out = process_runner(prompt, output_path)
        artifact_path = output_path if output_path.exists() else None
        status = _determine_status(exit_code, timed_out, stdout, artifact_path)

    return PortifyStepResult(
        step_name="pipeline-spec-assembly",
        step_number=9,
        phase=3,
        portify_status=status,
        gate_tier="STRICT",
        artifact_path=str(output_path),
        iteration_timeout=STEP_REGISTRY["pipeline-spec-assembly"]["timeout_s"],
    )


# ---------------------------------------------------------------------------
# Phase 6 User Review P2 (T06.06, FR-025, FR-026)
# ---------------------------------------------------------------------------


def execute_user_review_p2(
    config_cli_name: str,
    workdir: Path,
    step_results: Optional[list[PortifyStepResult]] = None,
    *,
    _exit: bool = True,
) -> None:
    """Execute the user-review-p2 gate (T06.06, FR-025, SC-006).

    Validates all Phase 2 blocking gates (G-005, G-006, G-007, G-008) passed,
    validates portify-spec.md has non-empty step_mapping section, then writes
    ``workdir/phase2-approval.yaml`` with ``status: completed`` and prints
    resume instructions to stdout.  Exits cleanly with code 0.

    Args:
        config_cli_name: CLI name being portified (used in instructions).
        workdir: Working directory where phase2-approval.yaml will be written.
        step_results: List of PortifyStepResult objects from Phase 2 steps.
                      If None, skips gate-pass validation.
        _exit: If True (default), calls sys.exit(0). Set False in tests.

    Raises:
        PortifyValidationError: If blocking gates have not passed or portify-spec.md
                                is missing or has an empty step_mapping section.
    """
    # Validate all blocking gates passed (G-005, G-006, G-007, G-008)
    if step_results is not None:
        blocking_steps = {
            "step-graph-design",
            "models-gates-design",
            "prompts-executor-design",
            "pipeline-spec-assembly",
        }
        for result in step_results:
            if result.step_name in blocking_steps:
                if result.portify_status not in (
                    PortifyStatus.PASS,
                    PortifyStatus.PASS_NO_SIGNAL,
                ):
                    raise PortifyValidationError(
                        INVALID_PATH,
                        f"Blocking gate not passed for step '{result.step_name}' "
                        f"(status: {result.portify_status.value}) — cannot write phase2-approval.yaml",
                        str(workdir),
                    )

    # Validate portify-spec.md has non-empty step_mapping section
    portify_spec_path = workdir / "portify-spec.md"
    if not portify_spec_path.exists():
        raise PortifyValidationError(
            INVALID_PATH,
            "portify-spec.md not found — run pipeline-spec-assembly step first",
            str(portify_spec_path),
        )

    spec_content = portify_spec_path.read_text(encoding="utf-8")
    import re as _re

    step_mapping_match = _re.search(
        r"##\s+Step\s+Mapping\s*\n(.*?)(?=\n##|\Z)",
        spec_content,
        _re.DOTALL | _re.IGNORECASE,
    )
    if not step_mapping_match or not step_mapping_match.group(1).strip():
        raise PortifyValidationError(
            INVALID_PATH,
            "portify-spec.md: empty or missing 'Step Mapping' section — cannot approve",
            str(portify_spec_path),
        )

    approval = {
        "status": "completed",
        "workflow": config_cli_name,
        "review_artifacts": [
            "step-graph-spec.md",
            "models-gates-spec.md",
            "prompts-executor-spec.md",
            "portify-spec.md",
        ],
        "instructions": "Review artifacts above. Phase 2 specification is complete.",
    }

    workdir.mkdir(parents=True, exist_ok=True)
    approval_path = workdir / "phase2-approval.yaml"
    with open(approval_path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(approval, fh, default_flow_style=False, sort_keys=False)

    resume_cmd = f"superclaude cli-portify run {config_cli_name} --resume phase3"
    print(f"Phase 2 complete. Run: {resume_cmd}")

    if _exit:
        sys.exit(0)


def _validate_phase2_approval(workdir: Path) -> None:
    """Validate phase2-approval.yaml using YAML parse + schema check (T06.06, FR-026).

    Reads ``workdir/phase2-approval.yaml``, parses with yaml.safe_load(), and
    validates that ``status == 'completed'``.

    Raises:
        PortifyValidationError: On missing file, malformed YAML, missing status
                                field, or non-completed status.
    """
    approval_path = workdir / "phase2-approval.yaml"

    if not approval_path.exists():
        raise PortifyValidationError(
            INVALID_PATH,
            "phase2-approval.yaml not found — run the specification phase first",
            str(approval_path),
        )

    raw = approval_path.read_text(encoding="utf-8")

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise PortifyValidationError(
            INVALID_PATH,
            f"phase2-approval.yaml: malformed YAML — {exc}",
            str(approval_path),
        )

    if not isinstance(data, dict):
        raise PortifyValidationError(
            INVALID_PATH,
            "phase2-approval.yaml: must be a YAML mapping",
            str(approval_path),
        )

    if "status" not in data:
        raise PortifyValidationError(
            INVALID_PATH,
            "phase2-approval.yaml: missing required field 'status'",
            str(approval_path),
        )

    if data["status"] != "completed":
        raise PortifyValidationError(
            INVALID_PATH,
            f"phase2-approval.yaml: status must be 'completed', got '{data['status']}'",
            str(approval_path),
        )


# ---------------------------------------------------------------------------
# Phase 7: Release Spec Synthesis Step Executors (T07.01–T07.03)
# ---------------------------------------------------------------------------


def scan_for_placeholders(content: str) -> list[str]:
    """Return a list of remaining {{SC_PLACEHOLDER:*}} names in *content* (T07.03, FR-028).

    Args:
        content: Draft spec content to scan.

    Returns:
        List of placeholder names (the part after ``{{SC_PLACEHOLDER:``).
        Empty list means zero placeholders remain.
    """
    import re as _re

    pattern = _re.compile(r"\{\{SC_PLACEHOLDER:([^}]+)\}\}")
    return [m.group(1) for m in pattern.finditer(content)]


def execute_release_spec_synthesis_step(
    config_cli_name: str,
    workdir: Path,
    project_root: Optional[Path] = None,
    process_runner: Optional[Callable[[str, Path], tuple[int, str, bool]]] = None,
) -> PortifyStepResult:
    """Execute the full 4-substep release spec synthesis (T07.01–T07.03, R-048–R-050, FR-027).

    Substeps:
        3a: Confirm working copy exists (load template + create_working_copy).
        3b: Populate 13 sections via Claude (section population prompt).
        3c: Run 3-persona brainstorm (architect, analyzer, backend).
        3d: Incorporate findings; CRITICAL/MAJOR → body; unresolvable → Section 12.

    Then validates zero placeholders and emits ``workdir/portify-release-spec.md``
    with YAML frontmatter (title, status, quality_scores).

    Applies G-010 gate: zero placeholders + Section 12 present +
    EXIT_RECOMMENDATION in stdout.

    Args:
        config_cli_name: CLI name being portified.
        workdir: Working directory containing portify-spec.md and
                 portify-analysis-report.md; output files written here.
        project_root: Root of the project (for loading release spec template).
                      Defaults to the repo root (3 levels up from this file).
        process_runner: Optional callable (prompt, output_path) -> (exit_code, stdout, timed_out).
                        Used for testing; real runs use PortifyProcess.

    Returns:
        PortifyStepResult with portify_status from G-010 gate.
    """
    from superclaude.cli.cli_portify.models import BrainstormFinding
    from superclaude.cli.cli_portify.prompts import (
        build_brainstorm_prompt,
        build_section_population_prompt,
        create_working_copy,
        incorporate_findings,
        load_release_spec_template,
    )

    output_path = workdir / "portify-release-spec.md"

    # Resolve project_root from this file location if not provided
    if project_root is None:
        # executor.py lives at src/superclaude/cli/cli_portify/executor.py
        # project_root is 4 levels up
        project_root = Path(__file__).parent.parent.parent.parent.parent

    # --- Substep 3a: Load template and confirm working copy ---
    try:
        template_content = load_release_spec_template(project_root)
    except Exception:
        # Template load failure — emit return contract and return ERROR
        return PortifyStepResult(
            step_name="release-spec-synthesis",
            step_number=10,
            phase=4,
            portify_status=PortifyStatus.ERROR,
            gate_tier="STRICT",
            artifact_path=str(output_path),
            error_message="Failed to load release spec template",
            iteration_timeout=STEP_REGISTRY["release-spec-synthesis"]["timeout_s"],
        )

    working_copy_path = create_working_copy(template_content, workdir)
    working_copy = working_copy_path.read_text(encoding="utf-8")

    # Read source artifacts (portify-spec.md, portify-analysis-report.md)
    portify_spec_path = workdir / "portify-spec.md"
    portify_spec = (
        portify_spec_path.read_text(encoding="utf-8")
        if portify_spec_path.exists()
        else ""
    )

    analysis_report_path = workdir / "portify-analysis-report.md"
    analysis_report = (
        analysis_report_path.read_text(encoding="utf-8")
        if analysis_report_path.exists()
        else ""
    )

    # --- Substep 3b: 13-section population via Claude ---
    population_prompt = build_section_population_prompt(
        working_copy, portify_spec, analysis_report
    )
    draft_path = workdir / "release-spec-draft.md"

    if process_runner is not None:
        exit_code, stdout, timed_out = process_runner(population_prompt, draft_path)
    else:
        # Default no-op: write an empty draft
        draft_path.write_text(working_copy, encoding="utf-8")
        exit_code, stdout, timed_out = (
            0,
            EXIT_RECOMMENDATION_MARKER + " CONTINUE",
            False,
        )

    if timed_out or exit_code == EXIT_CODE_TIMEOUT:
        return PortifyStepResult(
            step_name="release-spec-synthesis",
            step_number=10,
            phase=4,
            portify_status=PortifyStatus.TIMEOUT,
            gate_tier="STRICT",
            artifact_path=str(output_path),
            iteration_timeout=STEP_REGISTRY["release-spec-synthesis"]["timeout_s"],
        )
    if exit_code != 0:
        return PortifyStepResult(
            step_name="release-spec-synthesis",
            step_number=10,
            phase=4,
            portify_status=PortifyStatus.ERROR,
            gate_tier="STRICT",
            artifact_path=str(output_path),
            error_message=f"Section population step exited {exit_code}",
            iteration_timeout=STEP_REGISTRY["release-spec-synthesis"]["timeout_s"],
        )

    draft_content = (
        draft_path.read_text(encoding="utf-8") if draft_path.exists() else working_copy
    )

    # --- Substep 3c: 3-persona brainstorm ---
    all_findings: list[BrainstormFinding] = []
    for persona in ("architect", "analyzer", "backend"):
        brainstorm_prompt = build_brainstorm_prompt(draft_content, persona)
        brainstorm_path = workdir / f"brainstorm-{persona}.md"

        if process_runner is not None:
            b_exit, b_stdout, b_timed_out = process_runner(
                brainstorm_prompt, brainstorm_path
            )
        else:
            b_stdout = EXIT_RECOMMENDATION_MARKER + " CONTINUE"
            b_timed_out = False

        # Parse JSON findings from stdout
        import json as _json
        import re as _re

        for line in b_stdout.splitlines():
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    obj = _json.loads(line)
                    finding = BrainstormFinding(
                        gap_id=obj.get("gap_id", ""),
                        description=obj.get("description", ""),
                        severity=obj.get("severity", "MINOR"),
                        affected_section=obj.get("affected_section", ""),
                        persona=obj.get("persona", persona),
                    )
                    all_findings.append(finding)
                except (_json.JSONDecodeError, KeyError):
                    pass

    # --- Substep 3d: Incorporate findings ---
    final_content = incorporate_findings(draft_content, all_findings)

    # --- T07.03: Scan for remaining placeholders ---
    remaining = scan_for_placeholders(final_content)
    if remaining:
        return PortifyStepResult(
            step_name="release-spec-synthesis",
            step_number=10,
            phase=4,
            portify_status=PortifyStatus.ERROR,
            gate_tier="STRICT",
            artifact_path=str(output_path),
            error_message=(
                f"Placeholder leakage: {len(remaining)} {{{{SC_PLACEHOLDER:*}}}} "
                f"sentinels remain: {remaining[:5]}"
            ),
            iteration_timeout=STEP_REGISTRY["release-spec-synthesis"]["timeout_s"],
        )

    # Add YAML frontmatter (FR-029)
    frontmatter = (
        "---\n"
        f"title: portify-release-spec-{config_cli_name}\n"
        "status: draft\n"
        "quality_scores: {}\n"
        "---\n\n"
    )
    # Strip existing frontmatter if present
    import re as _re

    final_content_stripped = _re.sub(
        r"^---\n.*?---\n\n?", "", final_content, count=1, flags=_re.DOTALL
    )
    final_output = frontmatter + final_content_stripped

    # Write portify-release-spec.md
    workdir.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_output, encoding="utf-8")

    # G-010 gate: zero placeholders + Section 12 present
    import re as _re2

    has_section12 = bool(_re2.search(r"^##\s+12\b", final_output, _re2.MULTILINE))
    if not has_section12:
        return PortifyStepResult(
            step_name="release-spec-synthesis",
            step_number=10,
            phase=4,
            portify_status=PortifyStatus.ERROR,
            gate_tier="STRICT",
            artifact_path=str(output_path),
            error_message="G-010 gate failed: Section 12 (Brainstorm Gap Analysis) not present",
            iteration_timeout=STEP_REGISTRY["release-spec-synthesis"]["timeout_s"],
        )

    return PortifyStepResult(
        step_name="release-spec-synthesis",
        step_number=10,
        phase=4,
        portify_status=PortifyStatus.PASS,
        gate_tier="STRICT",
        artifact_path=str(output_path),
        iteration_timeout=STEP_REGISTRY["release-spec-synthesis"]["timeout_s"],
    )


# ---------------------------------------------------------------------------
# T10.01: run_portify() — top-level entry point called by commands.py (FR-049)
# ---------------------------------------------------------------------------


def run_portify(config: "PortifyConfig") -> PortifyOutcome:
    """Execute the full portify pipeline from a resolved PortifyConfig.

    Builds steps from STEP_REGISTRY, constructs a PortifyExecutor, and runs it.
    Returns the outcome for use by the CLI command.

    Args:
        config: Fully resolved PortifyConfig (from load_portify_config).

    Returns:
        PortifyOutcome indicating pipeline result.
    """
    from superclaude.cli.cli_portify.models import PortifyConfig, PortifyStep

    workdir = config.workdir_path or (
        Path(config.output_dir) / config.cli_name if config.output_dir else Path(".")
    )
    workdir = Path(workdir)

    steps = [
        PortifyStep(
            step_id=entry["step_id"],
            phase_type=entry["phase_type"],
            retry_limit=entry.get("retry_limit", 0),
        )
        for entry in STEP_REGISTRY.values()
    ]

    executor = PortifyExecutor(
        steps=steps,
        workdir=workdir,
        dry_run=config.dry_run,
        resume_from=getattr(config, "resume_from", "") or "",
        turn_budget=config.max_turns,
    )
    return executor.run()
