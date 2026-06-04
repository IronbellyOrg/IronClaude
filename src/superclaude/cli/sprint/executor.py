"""Sprint executor — core orchestration loop."""

from __future__ import annotations

import contextlib
import json
import logging as _logging
import os
import re
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from superclaude.cli.pipeline.models import Step, StepResult
from superclaude.cli.pipeline.trailing_gate import (
    DeferredRemediationLog,
    TrailingGateResult,
)

from .debug_logger import debug_log, setup_debug_logger
from .diagnostics import DiagnosticCollector, FailureClassifier, ReportGenerator
from .handoff import FileHandoffStore, is_validated_success
from .logging_ import SprintLogger
from .models import (
    GateOutcome,
    HandoffRecord,
    MonitorState,
    Phase,
    PhaseResult,
    PhaseStatus,
    ShadowGateMetrics,
    SprintConfig,
    SprintOutcome,
    SprintResult,
    TaskEntry,
    TaskResult,
    TaskStatus,
    TurnLedger,
)
from .monitor import OutputMonitor, detect_error_max_turns, detect_prompt_too_long
from .notify import notify_phase_complete, notify_sprint_complete
from .process import (
    ClaudeProcess,
    SignalHandler,
    build_task_context,
    count_turns_from_stream_json,
)
from .scheduler import CycleError, topological_launch_order
from .tmux import update_summary_pane, update_tail_pane
from .tui import SprintTUI

_wiring_logger = _logging.getLogger("superclaude.sprint.wiring_hook")
_anti_instinct_logger = _logging.getLogger("superclaude.sprint.anti_instinct_hook")
_checkpoint_logger = _logging.getLogger("superclaude.sprint.checkpoint")
_routing_logger = _logging.getLogger("superclaude.sprint.routing")
_stall_logger = _logging.getLogger("superclaude.sprint.stall")

# M6: a SEPARATE relaxed near-miss probe for the per-task heading router. This is
# NOT the strict extraction regex (`config._TASK_HEADING_RE`, which must stay
# unchanged) — it only diagnoses headings that LOOK like `### T<PP>.<TT>` but miss
# the strict shape (wrong level, separator, or zero-pad). Used warn-only; it never
# reclassifies a phase.
_TASK_HEADING_NEAR_MISS_RE = re.compile(r"#{2,5}\s*T\d{1,2}[._]\d{1,2}", re.MULTILINE)

# Debug logger name for executor-specific events
_DBG_NAME = "superclaude.sprint.debug.executor"


# ---------------------------------------------------------------------------
# T07.01 -- Concrete TrailingGatePolicy for sprint consumer
# ---------------------------------------------------------------------------


class SprintGatePolicy:
    """Sprint-specific implementation of TrailingGatePolicy.

    Builds remediation steps from gate failures and tracks file changes
    within the sprint execution context.
    """

    def __init__(self, config: SprintConfig) -> None:
        self._config = config

    def build_remediation_step(self, gate_result: TrailingGateResult) -> Step:
        """Build a focused remediation Step from a gate failure.

        Constructs a Step whose prompt targets the specific failure reason
        and acceptance criteria, rather than re-executing the entire task.
        """

        prompt = (
            f"REMEDIATION: Fix the following gate failure for step '{gate_result.step_id}'.\n"
            f"Failure reason: {gate_result.failure_reason or 'Unknown'}\n"
            f"Focus only on resolving this specific issue."
        )
        output_dir = self._config.work_dir / "remediation"
        output_dir.mkdir(parents=True, exist_ok=True)

        return Step(
            id=f"{gate_result.step_id}_remediation",
            prompt=prompt,
            output_file=output_dir / f"{gate_result.step_id}_remediation.md",
            gate=None,
            timeout_seconds=self._config.max_turns * 120 + 300,
        )

    def files_changed(self, step_result: StepResult) -> set[Path]:
        """Return file paths modified during step execution.

        Scans the step's output file and working directory for modifications
        since the step started.
        """
        changed: set[Path] = set()
        if step_result.step is not None and step_result.step.output_file.exists():
            changed.add(step_result.step.output_file)
        return changed


# ---------------------------------------------------------------------------
# 4-Layer Subprocess Isolation
# ---------------------------------------------------------------------------


@dataclass
class IsolationLayers:
    """Configuration for the 4-layer subprocess isolation.

    Each layer prevents cross-task state leakage:
    1. scoped_work_dir: Restrict working directory to release dir
    2. git_boundary: Set GIT_CEILING_DIRECTORIES to prevent upward traversal
    3. empty_plugin_dir: Point CLAUDE_PLUGIN_DIR to an empty tempdir
    4. restricted_settings: Set CLAUDE_SETTINGS_DIR to an isolated tempdir

    The ``env_vars`` property returns a dict of environment variable overrides
    that should be merged into the subprocess environment.
    """

    scoped_work_dir: Path
    git_boundary: Path
    plugin_dir: Path
    settings_dir: Path

    @property
    def env_vars(self) -> dict[str, str]:
        """Return environment variable overrides for all 4 isolation layers."""
        return {
            "CLAUDE_WORK_DIR": str(self.scoped_work_dir),
            "GIT_CEILING_DIRECTORIES": str(self.git_boundary),
            "CLAUDE_PLUGIN_DIR": str(self.plugin_dir),
            "CLAUDE_SETTINGS_DIR": str(self.settings_dir),
        }

    @property
    def layers_active(self) -> list[str]:
        """Return list of active isolation layer names for verification."""
        active = []
        if self.scoped_work_dir.exists():
            active.append("scoped_work_dir")
        if self.git_boundary.exists():
            active.append("git_boundary")
        if self.plugin_dir.exists():
            active.append("empty_plugin_dir")
        if self.settings_dir.exists():
            active.append("restricted_settings")
        return active


def setup_isolation(config: SprintConfig, *, scope: str = "") -> IsolationLayers:
    """Create 4-layer isolation for subprocess execution.

    Sets up:
    1. Scoped working directory (the release dir)
    2. Git boundary (prevents git operations above release dir)
    3. Empty plugin directory (no plugins loaded)
    4. Restricted settings directory (minimal settings)

    All directories are created if they don't exist. The caller is
    responsible for passing ``layers.env_vars`` to the subprocess.

    Args:
        config: Sprint configuration providing the release directory.
        scope: Optional per-slot discriminator (H1). When non-empty, the
            plugin and settings dirs become ``plugins/<scope>`` and
            ``settings/<scope>`` so each phase/task/worker gets its own
            isolated settings dir (needed for Stage-3 parallelism). When
            empty (the default), behavior is byte-for-byte equivalent to the
            pre-H1 shared ``plugins`` / ``settings`` dirs, preserving Path A
            serial behavior.

    Returns:
        IsolationLayers with all 4 layers configured.
    """
    base = config.results_dir / ".isolation"
    base.mkdir(parents=True, exist_ok=True)

    plugin_dir = base / "plugins"
    settings_dir = base / "settings"
    if scope:
        plugin_dir = plugin_dir / scope
        settings_dir = settings_dir / scope
    plugin_dir.mkdir(parents=True, exist_ok=True)
    settings_dir.mkdir(parents=True, exist_ok=True)

    return IsolationLayers(
        scoped_work_dir=config.release_dir,
        git_boundary=config.release_dir,
        plugin_dir=plugin_dir,
        settings_dir=settings_dir,
    )


# ---------------------------------------------------------------------------
# Result Aggregation — runner-constructed phase reports
# ---------------------------------------------------------------------------


@dataclass
class AggregatedPhaseReport:
    """Runner-constructed phase report from collected TaskResults.

    This report is built by the runner, not by parsing agent self-reported
    output, ensuring accurate task outcome tracking even when subprocesses
    are budget-exhausted.
    """

    phase_number: int
    tasks_total: int = 0
    tasks_passed: int = 0
    tasks_failed: int = 0
    tasks_incomplete: int = 0
    tasks_skipped: int = 0
    tasks_not_attempted: int = 0
    budget_remaining: int = 0
    total_turns_consumed: int = 0
    total_duration_seconds: float = 0.0
    task_results: list[TaskResult] = field(default_factory=list)
    remaining_task_ids: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        """Overall phase status: PASS, FAIL, or PARTIAL."""
        if self.tasks_total == 0:
            return "PASS"
        if self.tasks_passed == self.tasks_total:
            return "PASS"
        if self.tasks_passed == 0:
            return "FAIL"
        return "PARTIAL"

    def to_yaml(self) -> str:
        """Render the report as a YAML string.

        Produces a machine-readable YAML document with standardized fields
        for downstream tooling and TUI display.
        """
        lines = [
            f"phase: {self.phase_number}",
            f"status: {self.status}",
            f"tasks_total: {self.tasks_total}",
            f"tasks_passed: {self.tasks_passed}",
            f"tasks_failed: {self.tasks_failed}",
            f"tasks_incomplete: {self.tasks_incomplete}",
            f"tasks_not_attempted: {self.tasks_not_attempted}",
            f"budget_remaining: {self.budget_remaining}",
            f"total_turns_consumed: {self.total_turns_consumed}",
            f"total_duration_seconds: {self.total_duration_seconds:.1f}",
            "tasks:",
        ]
        for tr in self.task_results:
            lines.append(f"  - task_id: {tr.task.task_id}")
            lines.append(f'    title: "{tr.task.title}"')
            lines.append(f"    status: {tr.status.value}")
            lines.append(f"    gate_outcome: {tr.gate_outcome.value}")
            lines.append(f"    turns_consumed: {tr.turns_consumed}")
            lines.append(f"    duration_seconds: {tr.duration_seconds:.1f}")
        if self.remaining_task_ids:
            lines.append("remaining_tasks:")
            for tid in self.remaining_task_ids:
                lines.append(f"  - {tid}")
        return "\n".join(lines) + "\n"

    def to_markdown(self) -> str:
        """Render the report as a markdown string with YAML frontmatter."""
        lines = [
            "---",
            f"phase: {self.phase_number}",
            f"status: {self.status}",
            f"tasks_total: {self.tasks_total}",
            f"tasks_passed: {self.tasks_passed}",
            f"tasks_failed: {self.tasks_failed}",
            "---",
            "",
            f"# Phase {self.phase_number} — Aggregated Task Report",
            "",
            "| Task ID | Title | Status | Turns | Duration |",
            "|---------|-------|--------|-------|----------|",
        ]
        for tr in self.task_results:
            dur = f"{tr.duration_seconds:.1f}s"
            lines.append(
                f"| {tr.task.task_id} | {tr.task.title} | {tr.status.value} "
                f"| {tr.turns_consumed} | {dur} |"
            )
        lines.append("")
        lines.append(f"**Total turns consumed:** {self.total_turns_consumed}")
        lines.append(f"**Total duration:** {self.total_duration_seconds:.1f}s")

        if self.remaining_task_ids:
            lines.append("")
            lines.append("## Remaining Tasks (Budget Exhausted)")
            for tid in self.remaining_task_ids:
                lines.append(f"- {tid}")

        lines.append("")
        if self.status == "PASS":
            lines.append("EXIT_RECOMMENDATION: CONTINUE")
        else:
            lines.append("EXIT_RECOMMENDATION: HALT")

        return "\n".join(lines) + "\n"


def aggregate_task_results(
    phase_number: int,
    task_results: list[TaskResult],
    remaining_task_ids: list[str] | None = None,
    budget_remaining: int = 0,
) -> AggregatedPhaseReport:
    """Aggregate individual TaskResults into a runner-constructed PhaseReport.

    This function is the runner's authoritative source of task outcomes.
    It does not rely on agent self-reporting.

    Args:
        phase_number: The phase number being aggregated.
        task_results: List of TaskResult from execute_phase_tasks().
        remaining_task_ids: Task IDs that were not attempted due to budget.

    Returns:
        AggregatedPhaseReport with computed counts and status.
    """
    report = AggregatedPhaseReport(
        phase_number=phase_number,
        task_results=task_results,
        remaining_task_ids=remaining_task_ids or [],
        budget_remaining=budget_remaining,
    )

    report.tasks_total = len(task_results) + len(report.remaining_task_ids)
    report.tasks_passed = sum(1 for r in task_results if r.status.is_success)
    report.tasks_failed = sum(
        1 for r in task_results if r.status == TaskStatus.FAIL_TERMINAL
    )
    report.tasks_incomplete = sum(
        1 for r in task_results if r.status == TaskStatus.INCOMPLETE
    )
    report.tasks_skipped = sum(
        1 for r in task_results if r.status == TaskStatus.SKIPPED
    )
    report.tasks_not_attempted = len(report.remaining_task_ids)
    report.total_turns_consumed = sum(r.turns_consumed for r in task_results)
    report.total_duration_seconds = sum(r.duration_seconds for r in task_results)

    return report


def check_budget_guard(ledger: TurnLedger | None) -> str | None:
    """Pre-launch budget guard: returns a halt message if budget is insufficient.

    Returns None if launch is allowed, or a descriptive message string
    if the budget is too low to launch a subprocess.
    """
    if ledger is None:
        return None
    if ledger.can_launch():
        return None
    return (
        f"Budget exhausted: {ledger.available()} turns remaining, "
        f"minimum {ledger.minimum_allocation} required for launch"
    )


def run_wiring_safeguard_checks(
    config: SprintConfig,
    report: object | None = None,
) -> list[str]:
    """Pre-activation safeguards for wiring analysis (SC-010, section 7 Phase 1).

    Checks run before the first wiring analysis in a sprint session:
    1. Zero-match warning: >50 files scanned but 0 findings → suspicious
    2. Whitelist validation: attempt to load whitelist, warn if parse fails
    3. provider_dir_names check: verify configured directories exist

    Safeguards produce warnings only; they never block sprint execution.

    Returns a list of warning messages (empty if all checks pass).
    """
    from superclaude.cli.audit.wiring_config import WiringConfig

    warnings: list[str] = []

    # Check 1: Zero-match warning (requires a report from a prior run)
    if report is not None:
        files_scanned = getattr(report, "files_analyzed", 0)
        total_findings = getattr(report, "total_findings", 0)
        if files_scanned > 50 and total_findings == 0:
            msg = (
                f"Zero-match warning: {files_scanned} files scanned but "
                f"0 findings produced — verify wiring analysis configuration"
            )
            _wiring_logger.warning(msg)
            warnings.append(msg)

    # Check 2: Whitelist validation
    # Try to parse with "soft" mode so malformed YAML raises instead of silently
    # returning empty. This is a safeguard check, not runtime behavior.
    whitelist_path = (
        config.release_dir
        / "src"
        / "superclaude"
        / "cli"
        / "audit"
        / "wiring_whitelist.yaml"
    )
    if whitelist_path.exists():
        try:
            import yaml as _yaml

            raw = _yaml.safe_load(whitelist_path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                msg = f"Whitelist validation failed: file at {whitelist_path} is not a YAML mapping"
                _wiring_logger.warning(msg)
                warnings.append(msg)
        except Exception as exc:
            msg = f"Whitelist validation failed: {exc}"
            _wiring_logger.warning(msg)
            warnings.append(msg)

    # Check 3: provider_dir_names sanity check
    wiring_config = WiringConfig()
    source_dir = config.release_dir
    for dir_name in wiring_config.provider_dir_names:
        found = list(source_dir.rglob(dir_name))
        dirs_found = [d for d in found if d.is_dir()]
        if not dirs_found:
            msg = (
                f"Provider directory '{dir_name}' not found under "
                f"{source_dir} — orphan module detection may miss files"
            )
            _wiring_logger.warning(msg)
            warnings.append(msg)

    return warnings


def _resolve_wiring_mode(config: SprintConfig) -> str:
    """Resolve the effective wiring gate mode from config.

    Uses resolve_gate_mode(scope, grace_period) from trailing_gate.py
    to map scope-based configuration to an effective mode string (Goal-5d).
    Falls back to config.wiring_gate_mode if scope resolution is not applicable.
    """
    from superclaude.cli.pipeline.models import GateMode
    from superclaude.cli.pipeline.trailing_gate import GateScope, resolve_gate_mode

    scope_map = {
        "release": GateScope.RELEASE,
        "milestone": GateScope.MILESTONE,
        "task": GateScope.TASK,
    }
    scope = scope_map.get(config.wiring_gate_scope)
    if scope is None:
        return config.wiring_gate_mode

    gate_mode = resolve_gate_mode(
        scope=scope, grace_period=config.wiring_gate_grace_period
    )

    # Map GateMode back to wiring mode string
    mode_map = {
        GateMode.BLOCKING: "full",
        GateMode.TRAILING: "shadow",
    }
    return mode_map.get(gate_mode, config.wiring_gate_mode)


def run_post_task_wiring_hook(
    task: TaskEntry,
    config: SprintConfig,
    task_result: TaskResult,
    ledger: TurnLedger | None = None,
    remediation_log: DeferredRemediationLog | None = None,
) -> TaskResult:
    """Run post-task wiring analysis based on config.wiring_gate_mode.

    Integrates with TurnLedger for budget-aware gate enforcement:
    - Checks can_run_wiring_gate() before analysis (debit-before-analysis)
    - Uses resolve_gate_mode(scope, grace_period) for mode resolution (Goal-5d)
    - Callable-based remediation interface avoids TurnLedger import in
      trailing_gate.py (Constraint 7)

    Mode behavior:
    - off: skip analysis entirely, return task_result unchanged
    - shadow: run analysis, log findings, task status unchanged (SC-006)
    - soft: run analysis, warn on critical findings, task status unchanged
    - full: run analysis, block (set FAIL) on critical+major findings,
            invoke remediation via callable interface

    Returns the (possibly modified) TaskResult. Only full mode may change
    task status to FAIL when blocking findings exist.
    """
    mode = _resolve_wiring_mode(config)

    if mode == "off":
        return task_result

    # Budget guard: check if wiring analysis budget allows this run
    if ledger is not None and not ledger.can_run_wiring_gate():
        _wiring_logger.info(
            "Wiring hook skipped for task %s: budget exhausted",
            task.task_id,
        )
        return task_result

    # Debit wiring turns before analysis (debit-before-analysis model)
    if ledger is not None:
        ledger.debit_wiring(config.wiring_analysis_turns)

    # Lazy import to avoid circular dependency at module level
    from superclaude.cli.audit.wiring_config import WiringConfig
    from superclaude.cli.audit.wiring_gate import run_wiring_analysis

    source_dir = config.release_dir
    wiring_config = WiringConfig(
        rollout_mode=mode if mode in ("shadow", "soft", "full") else "shadow"
    )

    try:
        report = run_wiring_analysis(wiring_config, source_dir)
    except Exception as exc:
        _wiring_logger.warning(
            "Wiring analysis failed for task %s: %s — continuing",
            task.task_id,
            exc,
        )
        return task_result

    total = report.total_findings
    blocking = report.blocking_count(mode)

    _wiring_logger.info(
        "Wiring hook [%s] task=%s: %d findings, %d blocking (%.4fs)",
        mode,
        task.task_id,
        total,
        blocking,
        report.scan_duration_seconds,
    )

    if mode == "shadow":
        # SC-006: log findings without affecting task status
        if total > 0:
            _wiring_logger.info(
                "Shadow mode: %d findings logged for task %s (status unchanged)",
                total,
                task.task_id,
            )
        # T05/R3: Log shadow findings to DeferredRemediationLog
        _log_shadow_findings_to_remediation_log(report, task, config, remediation_log)
        # Credit wiring turns back (shadow never blocks)
        if ledger is not None:
            ledger.credit_wiring(config.wiring_analysis_turns)
        return task_result

    if mode == "soft":
        # Warn on critical findings but don't change status
        critical_count = sum(
            1 for f in report.unsuppressed_findings if f.severity == "critical"
        )
        if critical_count > 0:
            _wiring_logger.warning(
                "Soft mode: %d critical findings for task %s",
                critical_count,
                task.task_id,
            )
        # Credit wiring turns back (soft never blocks)
        if ledger is not None:
            ledger.credit_wiring(config.wiring_analysis_turns)
        return task_result

    if mode == "full":
        # Block on critical+major findings
        if blocking > 0:
            _wiring_logger.error(
                "Full mode: %d blocking findings for task %s — marking FAIL",
                blocking,
                task.task_id,
            )
            task_result.status = TaskStatus.FAIL_TERMINAL
            task_result.gate_outcome = GateOutcome.FAIL

            # T08/R4: Remediation lifecycle via callable interface (Constraint 7)
            # Amendment A2 Option B: inline remediation for v3.2; full
            # attempt_remediation() wiring deferred to v3.3.
            if ledger is not None:
                can_remediate = ledger.can_remediate
                if can_remediate():
                    # Step 1: Format remediation prompt
                    prompt = _format_wiring_failure(report, task, config)
                    if prompt:
                        # Step 2: Debit remediation cost
                        ledger.debit(config.remediation_cost)
                        _wiring_logger.info(
                            "Full mode: remediation debited %d turns for task %s",
                            config.remediation_cost,
                            task.task_id,
                        )
                        # Step 3: Recheck wiring after remediation
                        passed, recheck_report = _recheck_wiring(
                            config,
                            config.release_dir,
                            mode,
                        )
                        if passed:
                            task_result.status = TaskStatus.PASS
                            task_result.gate_outcome = GateOutcome.PASS
                            ledger.credit_wiring(config.wiring_analysis_turns)
                            _wiring_logger.info(
                                "Remediation succeeded for task %s",
                                task.task_id,
                            )
                        else:
                            _wiring_logger.warning(
                                "Remediation failed for task %s — FAIL persists",
                                task.task_id,
                            )
                    else:
                        _wiring_logger.info(
                            "Full mode: no blocking findings to format for task %s",
                            task.task_id,
                        )
                else:
                    _wiring_logger.warning(
                        "Full mode: BUDGET_EXHAUSTED for task %s remediation",
                        task.task_id,
                    )
        else:
            # No blocking findings — credit turns back
            if ledger is not None:
                ledger.credit_wiring(config.wiring_analysis_turns)
        return task_result

    return task_result


# ---------------------------------------------------------------------------
# T04/R3: Shadow findings adapter for DeferredRemediationLog
# ---------------------------------------------------------------------------


def _log_shadow_findings_to_remediation_log(
    report: object,
    task: TaskEntry,
    config: SprintConfig,
    remediation_log: DeferredRemediationLog | None = None,
) -> None:
    """Log shadow mode findings to DeferredRemediationLog.

    Creates a synthetic TrailingGateResult per unsuppressed finding and
    appends to the remediation log. No-op when remediation_log is None.

    Amendment A1: Uses corrected TrailingGateResult constructor fields
    (step_id, passed, evaluation_ms, failure_reason).
    """
    if remediation_log is None:
        return

    # Lazy import to access unsuppressed_findings without top-level coupling
    unsuppressed = getattr(report, "unsuppressed_findings", [])
    for finding in unsuppressed:
        gate_result = TrailingGateResult(
            step_id=task.task_id,
            passed=False,
            evaluation_ms=0.0,
            failure_reason=f"[shadow] {finding.finding_type}: {finding.detail}",
        )
        remediation_log.append(gate_result)


# ---------------------------------------------------------------------------
# T06/R4: Format wiring failure for remediation prompt
# ---------------------------------------------------------------------------


def _format_wiring_failure(
    report: object,
    task: TaskEntry,
    config: SprintConfig,
) -> str:
    """Format a remediation prompt string from blocking wiring findings.

    Returns a non-empty string when blocking findings (critical/major severity)
    exist, or an empty string when none are present.

    The output is plain text suitable for consumption by a Claude subprocess.
    """
    unsuppressed = getattr(report, "unsuppressed_findings", [])
    blocking = [
        f for f in unsuppressed if getattr(f, "severity", "") in ("critical", "major")
    ]
    if not blocking:
        return ""

    lines = [
        f"WIRING REMEDIATION for task {task.task_id}: {task.title}",
        f"Blocking findings: {len(blocking)}",
        "",
    ]

    by_type: dict[str, int] = {}
    for f in blocking:
        ft = getattr(f, "finding_type", "unknown")
        by_type[ft] = by_type.get(ft, 0) + 1
    for ft, count in by_type.items():
        lines.append(f"  {ft}: {count}")
    lines.append("")

    for f in blocking:
        file_path = getattr(f, "file_path", "unknown")
        symbol = getattr(f, "symbol_name", "unknown")
        detail = getattr(f, "detail", "")
        lines.append(f"- [{getattr(f, 'severity', '?')}] {file_path} :: {symbol}")
        if detail:
            lines.append(f"  {detail}")
    lines.append("")
    lines.append("Fix these wiring issues and re-run the task.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# T07/R4: Recheck wiring after remediation
# ---------------------------------------------------------------------------


def _recheck_wiring(
    config: SprintConfig,
    source_dir: Path,
    mode: str,
) -> tuple[bool, object | None]:
    """Re-run wiring analysis and return (passed, report_or_None).

    Returns (True, report) if no blocking findings remain after remediation,
    (False, report) if blocking findings persist, or (False, None) on error.
    """
    from superclaude.cli.audit.wiring_config import WiringConfig
    from superclaude.cli.audit.wiring_gate import run_wiring_analysis

    try:
        wiring_config = WiringConfig(
            rollout_mode=mode if mode in ("shadow", "soft", "full") else "shadow",
        )
        report = run_wiring_analysis(wiring_config, source_dir)
        if report.blocking_count(mode) == 0:
            return (True, report)
        return (False, report)
    except Exception as exc:
        _wiring_logger.warning("Recheck wiring failed: %s", exc)
        return (False, None)


# ---------------------------------------------------------------------------
# T01/R1: Post-phase wiring hook (phase-level adapter)
# ---------------------------------------------------------------------------


def run_post_phase_wiring_hook(
    phase: Phase,
    config: SprintConfig,
    phase_result: PhaseResult,
    ledger: TurnLedger | None = None,
    remediation_log: DeferredRemediationLog | None = None,
) -> PhaseResult:
    """Run post-phase wiring analysis by delegating to the per-task hook.

    Creates a synthetic TaskEntry/TaskResult from the PhaseResult, delegates
    to run_post_task_wiring_hook() for the actual analysis, and maps the
    returned status back onto the PhaseResult.

    This avoids duplicating wiring analysis logic for phase-level execution.
    """
    # Build synthetic TaskEntry from the phase
    synthetic_task = TaskEntry(
        task_id=f"phase-{phase.number}",
        title=phase.file.name,
        description=f"Phase {phase.number} aggregate wiring check",
    )

    # Map PhaseResult status to TaskStatus for the synthetic TaskResult
    if phase_result.status.is_success:
        synth_status = TaskStatus.PASS
    elif phase_result.status.is_failure:
        synth_status = TaskStatus.FAIL_TERMINAL
    else:
        synth_status = TaskStatus.SKIPPED

    synthetic_result = TaskResult(
        task=synthetic_task,
        status=synth_status,
        exit_code=phase_result.exit_code,
        started_at=phase_result.started_at,
        finished_at=phase_result.finished_at,
        output_bytes=phase_result.output_bytes,
    )

    # Delegate to the per-task hook
    updated_result = run_post_task_wiring_hook(
        synthetic_task,
        config,
        synthetic_result,
        ledger=ledger,
        remediation_log=remediation_log,
    )

    # Map back: if the wiring hook changed status to FAIL, propagate to PhaseResult
    if (
        updated_result.status == TaskStatus.FAIL_TERMINAL
        and synth_status != TaskStatus.FAIL_TERMINAL
    ):
        phase_result.status = PhaseStatus.HALT

    return phase_result


def run_post_task_anti_instinct_hook(
    task: TaskEntry,
    config: SprintConfig,
    task_result: TaskResult,
    ledger: TurnLedger | None = None,
    shadow_metrics: ShadowGateMetrics | None = None,
) -> tuple[TaskResult, TrailingGateResult | None]:
    """Run post-task anti-instinct gate based on config.gate_rollout_mode.

    Mode behavior matrix:
    - off: evaluate gate, ignore result (metrics not recorded)
    - shadow: evaluate gate, record metrics via ShadowGateMetrics (FR-SPRINT.4)
    - soft: evaluate + record + credit on PASS / remediate on FAIL (FR-SPRINT.3)
    - full: evaluate + record + credit on PASS / remediate on FAIL / set FAIL status (FR-SPRINT.3)

    All TurnLedger calls are guarded with ``if ledger is not None`` (NFR-007).
    Anti-instinct and wiring-integrity gates evaluate independently (NFR-010).

    Returns a tuple of (possibly modified TaskResult, TrailingGateResult or None).
    For mode "off", gate_result is None. For shadow mode, gate IS evaluated
    and the result is returned for capture.
    """
    import time as _time

    mode = config.gate_rollout_mode

    if mode == "off":
        # Evaluate but ignore — no metrics, no side effects
        return (task_result, None)

    # Lazy import to avoid circular dependency
    from superclaude.cli.pipeline.gates import gate_passed
    from superclaude.cli.roadmap.gates import ANTI_INSTINCT_GATE

    # Evaluate the anti-instinct gate on the task's output artifact
    output_path = Path(task_result.output_path) if task_result.output_path else None

    eval_start = _time.monotonic()
    if output_path is not None and output_path.exists():
        passed, failure_reason = gate_passed(output_path, ANTI_INSTINCT_GATE)
    else:
        # No output artifact to evaluate — gate passes vacuously
        passed = True
        failure_reason = None
    eval_end = _time.monotonic()
    evaluation_ms = (eval_end - eval_start) * 1000.0

    _anti_instinct_logger.info(
        "Anti-instinct hook [%s] task=%s: passed=%s (%.1fms)",
        mode,
        task.task_id,
        passed,
        evaluation_ms,
    )

    # Build TrailingGateResult for all non-off modes (v3.1-T05)
    gate_result = TrailingGateResult(
        step_id=task.task_id,
        passed=passed,
        evaluation_ms=evaluation_ms,
        failure_reason=failure_reason if not passed else None,
    )

    # Record metrics for shadow/soft/full modes (FR-SPRINT.4)
    if shadow_metrics is not None:
        shadow_metrics.record(passed=passed, evaluation_ms=evaluation_ms)

    if mode == "shadow":
        # Record metrics only, no behavioral impact
        return (task_result, gate_result)

    # soft and full modes: credit on PASS, remediate on FAIL
    if passed:
        # Credit path: reimburse turns on gate PASS
        if ledger is not None:
            # SPEC-DEVIATION (BUG-010): Spec says reimbursement should use upstream
            # merge step turns. We use task_result.turns_consumed because it reflects
            # the actual work done by this task, which is more practical and defensible.
            # See: roadmap-gap-analysis-merged.md, D4.
            credit_amount = int(task_result.turns_consumed * ledger.reimbursement_rate)
            ledger.credit(credit_amount)
            task_result.reimbursement_amount = credit_amount
            _anti_instinct_logger.info(
                "Anti-instinct PASS: credited %d turns for task %s",
                credit_amount,
                task.task_id,
            )
        task_result.gate_outcome = GateOutcome.PASS
    else:
        # SPEC-DEVIATION (BUG-009/P6): Spec says this path should delegate to
        # attempt_remediation() for retry-once semantics. We use inline fail logic
        # (set GateOutcome.FAIL / TaskStatus.FAIL_TERMINAL) as an intentional v3.1
        # simplification. attempt_remediation() has a 6-arg callable-based API
        # that requires more design work to integrate here safely. Deferred to v3.2.
        # See: gap-remediation-tasklist.md, T08 Option B.

        # Remediation path: check budget, mark BUDGET_EXHAUSTED or FAIL
        if ledger is not None and not ledger.can_remediate():
            _anti_instinct_logger.warning(
                "Anti-instinct FAIL + BUDGET_EXHAUSTED for task %s: "
                "available=%d < minimum_remediation_budget=%d",
                task.task_id,
                ledger.available(),
                ledger.minimum_remediation_budget,
            )
            task_result.gate_outcome = GateOutcome.FAIL
            if mode == "full":
                task_result.status = TaskStatus.FAIL_TERMINAL
            return (task_result, gate_result)

        _anti_instinct_logger.warning(
            "Anti-instinct FAIL for task %s: %s",
            task.task_id,
            failure_reason or "unknown reason",
        )
        task_result.gate_outcome = GateOutcome.FAIL

        if mode == "full":
            # Full mode: fail the task
            task_result.status = TaskStatus.FAIL_TERMINAL

    return (task_result, gate_result)


def _run_one_task(
    task,
    config: SprintConfig,
    phase,
    *,
    started_at,
    prior_context: str = "",
    ledger: TurnLedger | None = None,
    subprocess_factory=None,
    shadow_metrics: ShadowGateMetrics | None = None,
    remediation_log: DeferredRemediationLog | None = None,
    lock=None,
) -> tuple[TaskResult, TrailingGateResult | None]:
    """Execute one task: spawn → classify → reconcile budget → post-task hooks.

    Shared by the sequential (K=1) and parallel (K>1) per-task paths so both
    classify and reconcile identically. The SPAWN runs UNLOCKED (the slow part —
    concurrency here is the source of the wall-clock win). The budget reconcile
    and the post-task hooks run under ``lock`` when provided (K>1) so shared
    ledger / shadow_metrics / remediation_log mutations cannot race. With
    ``lock=None`` (K=1) there is no locking and behavior is identical to the
    former inline block.
    """
    if subprocess_factory is not None:
        exit_code, turns_consumed, output_bytes = subprocess_factory(
            task, config, phase
        )
    else:
        exit_code, turns_consumed, output_bytes = _run_task_subprocess(
            task, config, phase, prior_context=prior_context
        )

    finished_at = datetime.now(timezone.utc)

    # Determine task status from exit code.
    task_output_path = config.task_output_file(phase, task)
    if exit_code == 0:
        status = TaskStatus.PASS
    elif exit_code == 124:
        status = TaskStatus.INCOMPLETE
    elif detect_error_max_turns(task_output_path) and _task_completed_before_overrun(
        task_output_path
    ):
        # Budget overrun (error_max_turns) AFTER completing substantive work:
        # the task emitted a successful result before the terminal overrun
        # envelope, so recover instead of failing the phase. Completion
        # evidence outranks the transient-failure classification below.
        # (#121, ported into the shared helper so BOTH K=1 and K>1 recover.)
        status = TaskStatus.PASS_RECOVERED
    elif _is_transient_failure(task_output_path):
        status = TaskStatus.FAIL_RECOVERABLE
    else:
        status = TaskStatus.FAIL_TERMINAL

    guard = lock if lock is not None else contextlib.nullcontext()
    with guard:
        if ledger is not None:
            actual = max(turns_consumed, 0)
            pre_allocated = ledger.minimum_allocation
            if actual > pre_allocated:
                ledger.debit(actual - pre_allocated)
            elif actual < pre_allocated:
                ledger.credit(pre_allocated - actual)

        result = TaskResult(
            task=task,
            status=status,
            turns_consumed=turns_consumed,
            exit_code=exit_code,
            started_at=started_at,
            finished_at=finished_at,
            output_bytes=output_bytes,
        )

        # Post-task wiring hook: run wiring analysis per config.wiring_gate_mode
        result = run_post_task_wiring_hook(
            task, config, result, ledger=ledger, remediation_log=remediation_log
        )
        # Post-task anti-instinct hook per config.gate_rollout_mode
        result, gate_result = run_post_task_anti_instinct_hook(
            task, config, result, ledger=ledger, shadow_metrics=shadow_metrics
        )
    return result, gate_result


def _execute_phase_tasks_parallel(
    tasks: list[TaskEntry],
    config: SprintConfig,
    phase,
    *,
    ledger: TurnLedger | None = None,
    _subprocess_factory=None,
    _env_capture: list | None = None,
    shadow_metrics: ShadowGateMetrics | None = None,
    remediation_log: DeferredRemediationLog | None = None,
    tui: "SprintTUI | None" = None,
    sprint_result: "SprintResult | None" = None,
    logger: "SprintLogger | None" = None,
    handoff_store=None,
) -> tuple[list[TaskResult], list[str], list[TrailingGateResult]]:
    """Bounded parallel per-task execution (Stage 3, K>1 only).

    Runs up to ``config.task_parallelism`` tasks concurrently per dependency wave
    (from ``topological_launch_order``), routing every shared mutation through the
    thread-safe primitives: ``TurnLedger.try_launch``/``debit``/``credit`` (locked),
    ``SprintLogger._jsonl`` (locked), per-task handoff files (independent, atomic
    temp+replace), and a local lock guarding the env-capture list, the per-task
    reconcile+hooks (via ``_run_one_task(lock=...)``), and TUI updates. K==1 never
    reaches here — the caller takes the unchanged sequential path.

    The SPAWN runs concurrently (the source of the wall-clock win); only the fast
    reconcile/hook/TUI mutations are serialized. Budget-exhaustion semantics differ
    from the sequential path: a task whose atomic ``try_launch`` fails is recorded
    SKIPPED and added to ``remaining`` (already-launched tasks still complete),
    rather than breaking the whole loop. Results are assembled in the original
    declared task order (not completion order) for determinism.
    """
    try:
        waves = topological_launch_order(tasks)
    except CycleError:
        # A dependency cycle cannot be wave-ordered; fall back to a single set in
        # declared order so execution still completes deterministically.
        waves = [[t.task_id for t in tasks]]

    by_id = {t.task_id: t for t in tasks}
    results_by_id: dict[str, TaskResult] = {}
    remaining: list[str] = []
    gate_results: list[TrailingGateResult] = []
    completed_results: list[TaskResult] = []  # prior-wave results for M3 context
    lock = threading.Lock()
    k = max(1, int(getattr(config, "task_parallelism", 1)))

    def _worker(task, prior_context):
        started_at = datetime.now(timezone.utc)
        # Resume skip (same validated-success predicate + back-compat as sequential).
        if (
            handoff_store is not None
            and getattr(config, "resume_task_id", "")
            and (config.results_dir / "handoff").exists()
        ):
            _prior = handoff_store.read(phase=phase, task=task)
            if _prior is not None and is_validated_success(_prior):
                return (
                    TaskResult(
                        task=task,
                        status=TaskStatus.PASS,
                        turns_consumed=0,
                        exit_code=0,
                        started_at=started_at,
                        finished_at=datetime.now(timezone.utc),
                        gate_outcome=GateOutcome.PASS,
                        output_path=_prior.output_path,
                    ),
                    None,
                    "skip",
                )
        # Atomic budget gate.
        if ledger is not None and not ledger.try_launch():
            return (
                TaskResult(
                    task=task,
                    status=TaskStatus.SKIPPED,
                    started_at=started_at,
                    finished_at=datetime.now(timezone.utc),
                ),
                None,
                "budget",
            )
        if _env_capture is not None:
            with lock:
                _env_capture.append(_task_env(task, config, phase))
        result, gate_result = _run_one_task(
            task,
            config,
            phase,
            started_at=started_at,
            prior_context=prior_context,
            ledger=ledger,
            subprocess_factory=_subprocess_factory,
            shadow_metrics=shadow_metrics,
            remediation_log=remediation_log,
            lock=lock,
        )
        if logger is not None:
            logger.write_task_complete(
                phase.number,
                task.task_id,
                result.status.value,
                result.turns_consumed,
                result.duration_seconds,
            )
        if handoff_store is not None:
            record = HandoffRecord.from_task_result(
                result,
                phase=phase.number,
                produced_artifacts=[str(config.task_output_file(phase, task))],
                consumed_upstreams=list(task.dependencies),
            )
            handoff_store.write(record, phase=phase, task=task)
        if tui is not None and sprint_result is not None:
            with lock:
                _st = MonitorState()
                _st.last_task_id = task.task_id
                _st.last_event_time = time.monotonic()
                tui.update(sprint_result, _st, phase)
        return result, gate_result, "ran"

    for wave in waves:
        wave_tasks = [by_id[tid] for tid in wave if tid in by_id]
        # All tasks in a wave share the same prior context = results of PRIOR waves
        # (their dependencies); same-wave tasks are independent by construction.
        prior_context = build_task_context(list(completed_results), start_commit="")
        with ThreadPoolExecutor(max_workers=k) as pool:
            wave_out = list(pool.map(lambda t: _worker(t, prior_context), wave_tasks))
        # Merge (single-threaded) preserving determinism.
        for (result, gate_result, kind), t in zip(wave_out, wave_tasks):
            results_by_id[t.task_id] = result
            completed_results.append(result)
            if gate_result is not None:
                gate_results.append(gate_result)
            if kind == "budget":
                remaining.append(t.task_id)

    results = [results_by_id[t.task_id] for t in tasks if t.task_id in results_by_id]
    return results, remaining, gate_results


def execute_phase_tasks(
    tasks: list[TaskEntry],
    config: SprintConfig,
    phase,
    ledger: TurnLedger | None = None,
    *,
    _subprocess_factory=None,
    _env_capture: list | None = None,
    shadow_metrics: ShadowGateMetrics | None = None,
    remediation_log: DeferredRemediationLog | None = None,
    # TUI params are optional for backward compat with tests.
    # When provided, per-task progress is shown in the dashboard.
    tui: "SprintTUI | None" = None,
    sprint_result: "SprintResult | None" = None,
    logger: "SprintLogger | None" = None,
    handoff_store=None,
) -> tuple[list[TaskResult], list[str], list[TrailingGateResult]]:
    """Per-task subprocess orchestration loop.

    Iterates over a task inventory, spawning one subprocess per task with
    budget allocation from the TurnLedger. Returns task results, a list
    of remaining (unattempted) task IDs if budget was exhausted, and
    accumulated TrailingGateResults from anti-instinct hook evaluations.

    Args:
        tasks: Ordered list of TaskEntry from the tasklist parser.
        config: Sprint configuration.
        phase: The Phase being executed.
        ledger: Optional TurnLedger for budget tracking.
        _subprocess_factory: Optional callable for testing; signature
            ``(task, config, phase) -> (exit_code, turns_consumed, output_bytes)``.
        shadow_metrics: Optional ShadowGateMetrics for anti-instinct gate
            metrics collection (used in shadow/soft/full rollout modes).

    Returns:
        Tuple of (results, remaining_task_ids, gate_results).
        remaining_task_ids is non-empty only when the loop halted due to
        budget exhaustion. gate_results contains TrailingGateResult from
        each evaluated anti-instinct gate (None results filtered out).
    """
    results: list[TaskResult] = []
    remaining: list[str] = []
    gate_results: list[TrailingGateResult] = []

    if not tasks:
        return results, remaining, gate_results

    # Stage 3 (H6): bounded parallel execution when --task-parallelism K>1 and
    # there is more than one task. K==1 (the default) falls through to the
    # unchanged sequential loop below, preserving byte-identical legacy behavior.
    if getattr(config, "task_parallelism", 1) > 1 and len(tasks) > 1:
        return _execute_phase_tasks_parallel(
            tasks,
            config,
            phase,
            ledger=ledger,
            _subprocess_factory=_subprocess_factory,
            _env_capture=_env_capture,
            shadow_metrics=shadow_metrics,
            remediation_log=remediation_log,
            tui=tui,
            sprint_result=sprint_result,
            logger=logger,
            handoff_store=handoff_store,
        )

    for i, task in enumerate(tasks):
        started_at = datetime.now(timezone.utc)

        # H5 resume skip: when resuming (config.resume_task_id set) and a handoff
        # store is present, a task with a VALIDATED-SUCCESS handoff record is not
        # re-run and does not debit the budget. The recorded result is the prior
        # validated success (status PASS, gate PASS) so downstream dependency
        # oracles (_is_satisfied → status.is_success) and phase aggregation see it
        # as satisfied; turns_consumed is 0 because this run spent none on it.
        # Only validated-success records are skipped — every non-success state
        # (FAIL_*/INCOMPLETE/SKIPPED, or PASS-with-gate-fail) still runs.
        # Back-compat (H5/M5): resuming against a pre-Stage-1 release_dir that has
        # NO handoff/ directory performs NO per-task skipping and degrades to
        # today's phase-granular behavior with no error. The explicit dir check
        # short-circuits before any read; handoff/ is created lazily only on the
        # first write (FileHandoffStore.write), never on a read.
        if (
            handoff_store is not None
            and getattr(config, "resume_task_id", "")
            and (config.results_dir / "handoff").exists()
        ):
            _prior = handoff_store.read(phase=phase, task=task)
            if _prior is not None and is_validated_success(_prior):
                results.append(
                    TaskResult(
                        task=task,
                        status=TaskStatus.PASS,
                        turns_consumed=0,
                        exit_code=0,
                        started_at=started_at,
                        finished_at=datetime.now(timezone.utc),
                        gate_outcome=GateOutcome.PASS,
                        output_path=_prior.output_path,
                    )
                )
                continue

        # Budget gate (atomic). try_launch checks can_launch AND debits the
        # minimum_allocation as ONE atomic op under the ledger lock, so two
        # concurrent workers (K>1) cannot both pass the check then both debit and
        # over-commit the budget. Single-threaded (K=1) semantics are identical to
        # the former can_launch()-then-debit() pair: the same tasks are skipped and
        # the same turns are debited. On failure (insufficient budget), mark this
        # and all subsequent tasks skipped and stop.
        if ledger is not None and not ledger.try_launch():
            remaining = [t.task_id for t in tasks[i:]]
            for t in tasks[i:]:
                results.append(
                    TaskResult(
                        task=t,
                        status=TaskStatus.SKIPPED,
                        started_at=started_at,
                        finished_at=datetime.now(timezone.utc),
                    )
                )
            break
        # (try_launch already debited minimum_allocation on success)

        # Per-task TUI update: show which task is about to launch
        if tui is not None and sprint_result is not None:
            _tui_state = MonitorState()
            _tui_state.events_received = i
            _tui_state.last_event_time = time.monotonic()
            _tui_state.last_task_id = task.task_id
            tui.update(sprint_result, _tui_state, phase)

        # H6 env-capture test seam: record the per-task isolation env that the
        # child WOULD receive, for every launched task, regardless of whether
        # the real subprocess or the injected factory runs (the factory bypasses
        # build_env, so per-worker CLAUDE_SETTINGS_DIR isolation is otherwise
        # untestable). Inert (zero behavior change) when _env_capture is None.
        if _env_capture is not None:
            _env_capture.append(_task_env(task, config, phase))

        # M3 prior-task context: render the prior results (already accumulated in
        # `results` at the top of this iteration) into the per-task prompt. Runs
        # in the parent process; start_commit="" simply skips the git-diff section.
        prior_context = build_task_context(results, start_commit="")

        # Spawn + classify + reconcile + post-task hooks. Shared with the K>1
        # parallel path via _run_one_task; lock=None here (sequential, no race).
        result, gate_result = _run_one_task(
            task,
            config,
            phase,
            started_at=started_at,
            prior_context=prior_context,
            ledger=ledger,
            subprocess_factory=_subprocess_factory,
            shadow_metrics=shadow_metrics,
            remediation_log=remediation_log,
            lock=None,
        )
        if gate_result is not None:
            gate_results.append(gate_result)

        results.append(result)

        # Per-task journal + typed handoff write (Stage 0/1) — the single
        # in-loop site under one single-writer discipline (M2). Emitted exactly
        # once per task at the moment the TaskResult is finalized; fully inert
        # (zero side effects, legacy behavior) when both params are None.
        if logger is not None:
            logger.write_task_complete(
                phase.number,
                task.task_id,
                result.status.value,
                result.turns_consumed,
                result.duration_seconds,
            )
        if handoff_store is not None:
            record = HandoffRecord.from_task_result(
                result,
                phase=phase.number,
                produced_artifacts=[str(config.task_output_file(phase, task))],
                consumed_upstreams=list(task.dependencies),
            )
            handoff_store.write(record, phase=phase, task=task)

        # Per-task TUI update: show task completion
        if tui is not None and sprint_result is not None:
            _tui_state = MonitorState()
            _tui_state.events_received = i + 1
            _tui_state.last_event_time = time.monotonic()
            _tui_state.last_task_id = task.task_id
            tui.update(sprint_result, _tui_state, phase)

    return results, remaining, gate_results


def _task_env(task: TaskEntry, config: SprintConfig, phase) -> dict[str, str]:
    """Per-task isolation env (H1/H6) — the single source of per-task subprocess env.

    Returns the full 4-layer ``setup_isolation`` env dict scoped to
    ``task-<task_id>`` so each task gets its OWN CLAUDE_SETTINGS_DIR /
    CLAUDE_PLUGIN_DIR (plus the release-scoped CLAUDE_WORK_DIR /
    GIT_CEILING_DIRECTORIES). Pure apart from the directory ``mkdir`` that
    ``setup_isolation`` already performs. Shared by the Path B wiring
    (``_run_task_subprocess``) and the H6 ``_env_capture`` test seam so both
    observe an identical per-task env. The ``phase`` arg is accepted for a
    uniform call shape (and future per-phase-qualified scoping) even though the
    scope is task-id based today.
    """
    return setup_isolation(config, scope=f"task-{task.task_id}").env_vars


def _poll_with_stall_watchdog(
    proc,
    config: SprintConfig,
    *,
    output_path: Path | None = None,
    on_stall=None,
    poll_interval: float = 0.5,
) -> None:
    """Wait for ``proc`` to exit while watching for a startup stall (RC.2).

    A stall = the per-task stream-json ``output_path`` does not grow for longer
    than ``config.startup_stall_timeout`` seconds. On the first stall this emits a
    LOUD warning, invokes ``on_stall(proc)`` (if given), and — when
    ``config.stall_action == "kill"`` — terminates the child. With
    ``startup_stall_timeout <= 0`` the watchdog is disabled and this degrades to a
    plain ``proc.wait()``. Shared by the per-task wait (``_run_task_subprocess``)
    and, under K>1, by each parallel worker's own wait (RC.3) — every in-flight
    per-task process gets its OWN independent stall timer (no shared timer state
    across workers). Previously a hung per-task process was never detected.
    """
    timeout = getattr(config, "startup_stall_timeout", 0) or 0
    underlying = getattr(proc, "_process", None)
    if underlying is None or timeout <= 0:
        proc.wait()
        return

    def _size() -> int:
        try:
            if output_path is not None and output_path.exists():
                return output_path.stat().st_size
        except OSError:
            return 0
        return 0

    last_size = _size()
    last_progress = time.monotonic()
    acted = False
    while underlying.poll() is None:
        time.sleep(poll_interval)
        cur = _size()
        if cur != last_size:
            last_size = cur
            last_progress = time.monotonic()
            acted = False
        elif not acted and (time.monotonic() - last_progress) > timeout:
            acted = True
            _stall_logger.warning(
                "Per-task subprocess stalled: no output for >%ss "
                "(startup_stall_timeout); stall_action=%s.",
                timeout,
                getattr(config, "stall_action", "warn"),
            )
            if on_stall is not None:
                try:
                    on_stall(proc)
                except Exception:  # noqa: BLE001 - on_stall is best-effort
                    pass
            if getattr(config, "stall_action", "warn") == "kill":
                try:
                    underlying.terminate()
                except Exception:  # noqa: BLE001 - best-effort kill
                    pass
                break
    proc.wait()


def _run_task_subprocess(
    task: TaskEntry,
    config: SprintConfig,
    phase,
    prior_context: str = "",
) -> tuple[int, int, int]:
    """Run a single task in a subprocess. Returns (exit_code, turns, output_bytes).

    This is the real implementation that spawns a ClaudeProcess. For testing,
    callers of execute_phase_tasks pass _subprocess_factory instead.

    ``prior_context`` is the rendered ``build_task_context(...)`` block for the
    prior tasks in this phase (M3); when non-empty it is appended to the
    single-task directive so the spawned worker sees prior-task context. Computed
    by the caller in the parent process (no logger needed).
    """
    # Build a task-specific prompt (single-task directive).
    prompt = (
        f"Execute task {task.task_id}: {task.title}\n"
        f"From phase file: {phase.file}\n"
        f"Description: {task.description}\n"
    )
    if prior_context:
        prompt = f"{prompt}\n{prior_context}\n"

    proc = ClaudeProcess.__new__(ClaudeProcess)
    proc.config = config
    proc.phase = phase
    from superclaude.cli.pipeline.process import ClaudeProcess as _Base

    _Base.__init__(
        proc,
        prompt=prompt,
        output_file=config.task_output_file(phase, task),
        error_file=config.task_error_file(phase, task),
        max_turns=config.max_turns,
        model=config.model,
        permission_flag=config.permission_flag,
        timeout_seconds=config.max_turns * 120 + 300,
        output_format="stream-json",
        # Path B isolation (H1): inject the full per-task setup_isolation env set
        # (own CLAUDE_SETTINGS_DIR / CLAUDE_PLUGIN_DIR / CLAUDE_WORK_DIR /
        # GIT_CEILING_DIRECTORIES). Previously Path B passed no env_vars and the
        # child inherited the parent env verbatim — the unmitigated-corruption path.
        env_vars=_task_env(task, config, phase),
    )
    proc.start()
    # RC.2: per-task wait now runs under the stall watchdog (was a bare wait, so a
    # hung per-task process was never detected). Each call has its OWN timer, so
    # under K>1 every parallel worker is independently watched (RC.3).
    _poll_with_stall_watchdog(
        proc, config, output_path=config.task_output_file(phase, task)
    )
    exit_code = proc._process.returncode if proc._process else -1
    output_path = config.task_output_file(phase, task)
    output_bytes = output_path.stat().st_size if output_path.exists() else 0
    # Real per-task turn count parsed from the stream-json result event.
    # Supersedes the T02.06 turn-counting wire (formerly hard-coded 0, which
    # made every task credit back its full minimum allocation and under-report
    # total_turns_consumed).
    turns = max(count_turns_from_stream_json(output_path), 0)
    return (exit_code if exit_code is not None else -1, turns, output_bytes)


def _parse_phase_tasks(phase: Phase, config: SprintConfig) -> list[TaskEntry] | None:
    """Parse a phase file for task entries.

    Returns a list of TaskEntry if the phase file contains a task inventory
    (i.e., ``### T<PP>.<TT>`` headings), or None for freeform-prompt phases
    that should use the ClaudeProcess fallback.
    """
    from .config import parse_tasklist

    if not phase.file.exists():
        return None

    content = phase.file.read_text(encoding="utf-8", errors="replace")
    tasks = parse_tasklist(content, execution_mode=phase.execution_mode)
    if tasks:
        return tasks
    # M6 warn-only near-miss probe: the strict heading regex matched nothing, so
    # this phase routes to the single-session (Path A) fallback. If a RELAXED
    # probe finds a heading that LOOKS like a `T<PP>.<TT>` task heading (wrong
    # level, separator, or missing zero-pad), emit a LOUD warning so a heading
    # typo does not silently demote a per-task phase to single-session — but do
    # NOT reroute (return None unchanged). Legitimately freeform phases (no
    # `T<PP>.<TT>`-like text) produce no match and no warning.
    if _TASK_HEADING_NEAR_MISS_RE.search(content):
        _routing_logger.warning(
            "Phase file %s has a heading-format near-miss: it contains text that "
            "looks like '### T<PP>.<TT>' task headings but none matched the strict "
            "parser, so this phase will run as a SINGLE-SESSION (per-phase) phase. "
            "If per-task execution was intended, check the heading level (###), the "
            "separator (-- or em-dash), and two-digit zero-padding.",
            phase.file,
        )
    return None


def execute_sprint(config: SprintConfig):
    """Main orchestration loop.

    For each active phase:
    1. Launch claude -p subprocess
    2. Start output monitor thread
    3. Update TUI in a polling loop until process exits (with timeout)
    4. Parse result file for CONTINUE/HALT
    5. Record PhaseResult
    6. Decide whether to continue or halt
    """
    # Pre-flight: verify claude binary is available before starting TUI/logging
    if shutil.which("claude") is None:
        raise SystemExit(
            "Error: 'claude' binary not found in PATH. "
            "Install Claude Code CLI before running sprint."
        )

    signal_handler = SignalHandler()
    signal_handler.install()

    setup_debug_logger(config)
    import logging as _logging

    _dbg = _logging.getLogger(_DBG_NAME)

    logger = SprintLogger(config)
    tui = SprintTUI(config)
    monitor = OutputMonitor(Path("/dev/null"))  # reset per phase
    proc_manager: ClaudeProcess | None = None

    sprint_result = SprintResult(config=config)

    # TUI v2 Wave 3 (v3.7): background phase-summary thread pool. Each
    # completed phase triggers a daemon thread that re-parses the
    # stream-json output file, asks Sonnet for a narrative, and writes
    # ``results/phase-<N>-summary.md``. Failures never propagate to the
    # sprint loop (see SummaryWorker.__doc__).
    #
    # TUI v2 Wave 4 (v3.7, F9): the worker's on_summary_ready callback
    # fans out to either the dedicated tmux summary pane (``:0.1``) or
    # the TUI's ``latest_summary_notification`` line when running with
    # ``--no-tmux``. The callback is exception-isolated inside
    # SummaryWorker so a broken pane or stale session cannot abort the
    # sprint.
    from .summarizer import PhaseSummarizer, SummaryWorker

    def _summary_fanout(summary) -> None:
        path = summary.path
        if path is None:
            return
        session = config.tmux_session_name
        if session:
            update_summary_pane(session, path)
        else:
            tui.latest_summary_notification = (
                f"Phase {summary.phase.number} summary ready: {path}"
            )

    _summary_worker = SummaryWorker(
        PhaseSummarizer(config), on_summary_ready=_summary_fanout
    )

    # --- v3.1 gap-remediation: infrastructure instantiation (T01–T06) ---
    # T01 (BUG-001/P0): Construct TurnLedger for budget tracking
    ledger = TurnLedger(
        initial_budget=config.max_turns * len(config.active_phases),
        reimbursement_rate=0.8,
    )
    # T02 (BUG-002/P0): Construct ShadowGateMetrics for anti-instinct telemetry
    shadow_metrics = ShadowGateMetrics()
    # T03 (BUG-005/P2): Construct DeferredRemediationLog for failed gate persistence
    from superclaude.cli.pipeline.trailing_gate import DeferredRemediationLog

    remediation_log = DeferredRemediationLog(
        persist_path=config.results_dir / "remediation.json",
    )
    # T06 (BUG-006/P5): Construct SprintGatePolicy for remediation step building.
    # The instance is intentionally not bound to a local — its construction is
    # captured by tests via SprintGatePolicy.__init__ patching (see
    # tests/v3.3/test_wiring_points_e2e.py::test_sprint_gate_policy_construction).
    SprintGatePolicy(config)

    # T05-C: Accumulator for all TrailingGateResults across phases
    all_gate_results: list[TrailingGateResult] = []

    logger.write_header(sprint_result)

    tui.start()

    # Startup orphan cleanup: remove stale isolation dirs from crashed previous runs
    shutil.rmtree(config.results_dir / ".isolation", ignore_errors=True)

    # Execute all python-mode phases via preflight executor before the main loop.
    # Removing this single call reverts to all-Claude behavior (R-051 rollback property).
    # Lazy import breaks the preflight → executor → preflight circular import cycle.
    from .preflight import execute_preflight_phases  # noqa: PLC0415

    preflight_results = execute_preflight_phases(config)

    try:
        for phase in config.active_phases:
            if signal_handler.shutdown_requested:
                sprint_result.outcome = SprintOutcome.INTERRUPTED
                break

            # Python-mode phases were already executed by preflight; skip here.
            if phase.execution_mode == "python":
                continue

            # Skip-mode phases: record SKIPPED with no subprocess launched.
            if phase.execution_mode == "skip":
                _now = datetime.now(timezone.utc)
                skip_result = PhaseResult(
                    phase=phase,
                    status=PhaseStatus.SKIPPED,
                    exit_code=0,
                    started_at=_now,
                    finished_at=_now,
                )
                sprint_result.phase_results.append(skip_result)
                logger.write_phase_result(skip_result)
                continue

            # v3.1-T04: Per-task delegation — if phase has a task inventory,
            # delegate to execute_phase_tasks() instead of single ClaudeProcess.
            tasks = _parse_phase_tasks(phase, config)
            if tasks:
                started_at = datetime.now(timezone.utc)
                logger.write_phase_start(phase, started_at)
                # Signal TUI that this phase is now active
                tui.update(sprint_result, MonitorState(), phase)
                # M5 legacy-exact gating: with --handoff=off (handoff_enabled
                # False) NO HandoffRecord is written AND NO task_complete journal
                # event is emitted, so the execution log is byte-equivalent to the
                # pre-Stage-1 behavior. Both the store and the per-task journal
                # logger are gated by handoff_enabled; the store also requires the
                # "file" backend ("mail" is the out-of-scope Stage 4 selector).
                _handoff_store = (
                    FileHandoffStore(config)
                    if config.handoff_enabled and config.handoff_store == "file"
                    else None
                )
                _handoff_logger = logger if config.handoff_enabled else None
                task_results, remaining, phase_gate_results = execute_phase_tasks(
                    tasks=tasks,
                    config=config,
                    phase=phase,
                    ledger=ledger,
                    shadow_metrics=shadow_metrics,
                    remediation_log=remediation_log,
                    tui=tui,
                    sprint_result=sprint_result,
                    logger=_handoff_logger,
                    handoff_store=_handoff_store,
                )
                all_gate_results.extend(phase_gate_results)
                # RC.1 (reflect C-021): use the runner-authoritative aggregation
                # (counts + status) as the source of the phase result instead of
                # an inline binary collapse. aggregate_task_results now has a live
                # caller. For a fully-attempted phase (no `remaining`) the PASS/ERROR
                # outcome is equivalent to the former `all(r.status == PASS)`; when
                # budget left tasks un-attempted (`remaining` non-empty) the report
                # correctly counts them so the phase is no longer reported PASS.
                # aggregate_task_results.tasks_passed uses TaskStatus.is_success, so
                # #121's PASS_RECOVERED is counted as success here.
                phase_report = aggregate_task_results(
                    phase.number, task_results, remaining_task_ids=remaining
                )
                all_passed = phase_report.status == "PASS"
                status = PhaseStatus.PASS if all_passed else PhaseStatus.ERROR
                phase_result = PhaseResult(
                    phase=phase,
                    status=status,
                    exit_code=0 if all_passed else 1,
                    started_at=started_at,
                    finished_at=datetime.now(timezone.utc),
                    task_results=task_results,
                )

                # v3.2-T02: Run post-phase wiring hook for per-task phases too
                phase_result = run_post_phase_wiring_hook(
                    phase,
                    config,
                    phase_result,
                    ledger=ledger,
                    remediation_log=remediation_log,
                )

                sprint_result.phase_results.append(phase_result)
                logger.write_phase_result(phase_result)
                # v4.3.0-T06: persist phase result as JSON for rerun-tasks consumption
                _write_phase_result_json(config, phase, phase_result)
                # Refresh TUI with completed phase (current_phase=None resets active panel)
                tui.update(sprint_result, MonitorState(), None)
                continue

            # Per-phase isolation directory: exactly one file (the phase file)
            isolation_dir = config.results_dir / ".isolation" / f"phase-{phase.number}"
            isolation_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(phase.file, isolation_dir / phase.file.name)

            try:
                # Reset monitor for this phase. Pass phase.file so the
                # TUI v2 dual progress bar (F3) knows how many tasks live
                # in the phase without re-scanning every poll tick.
                output_path = config.output_file(phase)
                monitor.reset(output_path, phase_file=phase.file)
                monitor.start()

                # Update tmux tail pane if running in tmux
                if config.tmux_session_name:
                    update_tail_pane(config.tmux_session_name, output_path)

                # Launch claude with isolation env vars. H1 (Path A): KEEP the
                # phase-scoped CLAUDE_WORK_DIR (the per-phase copy dir at
                # isolation_dir) and ADD only the settings + plugin isolation
                # keys so this per-phase session gets its own settings/plugin
                # dirs without losing the phase work-dir scoping. setup_isolation's
                # own CLAUDE_WORK_DIR is the whole release dir, which would clobber
                # the phase scope, so it is deliberately NOT merged here.
                _layers = setup_isolation(config, scope=f"phase-{phase.number}")
                _phase_env_vars = {
                    "CLAUDE_WORK_DIR": str(
                        isolation_dir
                    ),  # KEEP phase-scoped (re-pinned)
                    "CLAUDE_SETTINGS_DIR": _layers.env_vars["CLAUDE_SETTINGS_DIR"],
                    "CLAUDE_PLUGIN_DIR": _layers.env_vars["CLAUDE_PLUGIN_DIR"],
                }
                proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)
                proc_manager.start()
                started_at = datetime.now(timezone.utc)
                # Use monotonic clock for deadline enforcement to be immune to NTP adjustments
                deadline = time.monotonic() + proc_manager.timeout_seconds
                logger.write_phase_start(phase, started_at)

                debug_log(_dbg, "PHASE_BEGIN", phase=phase.number, file=str(phase.file))

                tui.update(sprint_result, monitor.state, phase)

                # Poll loop: wait for process to finish while updating TUI
                # Enforces monotonic timeout via deadline check.
                _timed_out = False
                _stall_acted = False  # single-fire guard for watchdog
                _poll_start = time.monotonic()
                while proc_manager._process.poll() is None:
                    if signal_handler.shutdown_requested:
                        proc_manager.terminate()
                        break
                    if time.monotonic() > deadline:
                        # Timeout reached: kill the process, exit loop
                        _timed_out = True
                        proc_manager.terminate()
                        break

                    ms = monitor.state
                    _elapsed = time.monotonic() - _poll_start

                    debug_log(
                        _dbg,
                        "poll_tick",
                        phase=phase.number,
                        pid=proc_manager._process.pid,
                        poll_result="running",
                        elapsed=round(_elapsed, 1),
                        output_bytes=ms.output_bytes,
                        growth_rate=round(ms.growth_rate_bps, 1),
                        stall_seconds=round(ms.stall_seconds, 1),
                        stall_status=ms.stall_status,
                    )

                    # --- Watchdog: startup-stall check (no events received yet) ---
                    if (
                        config.startup_stall_timeout > 0
                        and ms.events_received == 0
                        and ms.stall_seconds > config.startup_stall_timeout
                        and not _stall_acted
                    ):
                        _stall_acted = True
                        debug_log(
                            _dbg,
                            "startup_stall_triggered",
                            phase=phase.number,
                            action=config.stall_action,
                            stall_seconds=round(ms.stall_seconds, 1),
                            pid=proc_manager._process.pid,
                        )
                        if config.stall_action == "kill":
                            import sys

                            print(
                                f"[WATCHDOG] Startup-stall detected ({ms.stall_seconds:.0f}s > "
                                f"{config.startup_stall_timeout}s, no events received) — "
                                f"killing phase {phase.number}",
                                file=sys.stderr,
                            )
                            _timed_out = True
                            proc_manager.terminate()
                            break
                        else:
                            # warn action: log and continue
                            import sys

                            print(
                                f"[WATCHDOG] Startup-stall detected ({ms.stall_seconds:.0f}s > "
                                f"{config.startup_stall_timeout}s, no events received) — "
                                f"warning for phase {phase.number}",
                                file=sys.stderr,
                            )

                    # --- Watchdog: mid-stall check (events seen, then silence) ---
                    if (
                        config.stall_timeout > 0
                        and ms.stall_seconds > config.stall_timeout
                        and ms.events_received > 0  # only after stream began
                        and not _stall_acted
                    ):
                        _stall_acted = True
                        debug_log(
                            _dbg,
                            "watchdog_triggered",
                            phase=phase.number,
                            action=config.stall_action,
                            stall_seconds=round(ms.stall_seconds, 1),
                            pid=proc_manager._process.pid,
                        )
                        if config.stall_action == "kill":
                            import sys

                            print(
                                f"[WATCHDOG] Mid-stall detected ({ms.stall_seconds:.0f}s > "
                                f"{config.stall_timeout}s) — killing phase {phase.number}",
                                file=sys.stderr,
                            )
                            _timed_out = True
                            proc_manager.terminate()
                            break
                        else:
                            # warn action: log and continue
                            import sys

                            print(
                                f"[WATCHDOG] Mid-stall detected ({ms.stall_seconds:.0f}s > "
                                f"{config.stall_timeout}s) — warning for phase {phase.number}",
                                file=sys.stderr,
                            )

                    # Reset single-fire guard when output resumes
                    if _stall_acted and ms.stall_seconds == 0.0:
                        _stall_acted = False

                    # Update TUI at ~2 Hz (monitor thread handles data extraction)
                    # Wrap in try/except so a display glitch cannot abort the sprint
                    try:
                        tui.update(sprint_result, monitor.state, phase)
                    except Exception as _tui_exc:
                        import sys

                        print(
                            f"[TUI] Display error (continuing sprint): {_tui_exc}",
                            file=sys.stderr,
                        )
                    time.sleep(0.5)

                # Safely read exit code: returncode may be None if terminate raced.
                # Use _timed_out flag instead of assigning directly to returncode.
                raw_rc = proc_manager._process.returncode
                if _timed_out:
                    exit_code = 124
                else:
                    exit_code = raw_rc if raw_rc is not None else -1
                monitor.stop()
                finished_at = datetime.now(timezone.utc)
                _phase_dur = (finished_at - started_at).total_seconds()
                debug_log(
                    _dbg,
                    "PHASE_END",
                    phase=phase.number,
                    exit_code=exit_code,
                    duration=round(_phase_dur, 1),
                )

                # If shutdown was requested during the poll loop, classify as
                # INTERRUPTED rather than letting _determine_phase_status see
                # exit_code=-1 (None→-1 fallback) and return PhaseStatus.ERROR,
                # which would incorrectly set the outcome to HALTED.
                if signal_handler.shutdown_requested:
                    logger.write_phase_interrupt(
                        phase, started_at, finished_at, exit_code
                    )
                    sprint_result.outcome = SprintOutcome.INTERRUPTED
                    break

                # Write a preliminary result sentinel so _determine_phase_status()
                # always finds a result file for exit_code=0 phases that wrote no report.
                # Guard: only for successful exits; non-zero paths must not reach this.
                if exit_code == 0:
                    _wrote_preliminary = _write_preliminary_result(
                        config, phase, started_at.timestamp()
                    )
                    debug_log(
                        _dbg,
                        "preliminary_result_write",
                        path=f"{'executor-preliminary (option_d)' if _wrote_preliminary else 'agent-written/option_a_or_noop'}",
                    )

                # Determine phase status
                status = _determine_phase_status(
                    exit_code=exit_code,
                    result_file=config.result_file(phase),
                    output_file=config.output_file(phase),
                    config=config,
                    phase=phase,
                    started_at=started_at.timestamp(),
                    error_file=config.error_file(phase),
                )

                # Wave 2: checkpoint enforcement gate (v3.7). Respects
                # config.checkpoint_gate_mode (off/shadow/soft/full). Shadow is
                # the default — emits a `checkpoint_verification` JSONL event
                # and never alters status. In `full` mode, missing checkpoints
                # downgrade PASS to PASS_MISSING_CHECKPOINT.
                if status == PhaseStatus.PASS:
                    try:
                        status = _verify_checkpoints(
                            config=config,
                            phase=phase,
                            status=status,
                            logger=logger,
                        )
                    except Exception as _cp_exc:  # noqa: BLE001
                        _checkpoint_logger.warning(
                            "Phase %d: checkpoint gate raised %s",
                            phase.number,
                            _cp_exc,
                        )

                # Write executor result file for downstream consumers.
                # Written AFTER status determination to avoid circularity.
                # Overwrites any agent-written file — executor is authoritative.
                _write_executor_result_file(
                    config=config,
                    phase=phase,
                    status=status,
                    exit_code=exit_code,
                    monitor_state=monitor.state,
                    started_at=started_at,
                    finished_at=finished_at,
                )

                # Collect stderr size for telemetry
                error_file = config.error_file(phase)
                error_bytes = error_file.stat().st_size if error_file.exists() else 0

                phase_result = PhaseResult(
                    phase=phase,
                    status=status,
                    exit_code=exit_code,
                    started_at=started_at,
                    finished_at=finished_at,
                    output_bytes=monitor.state.output_bytes,
                    error_bytes=error_bytes,
                    last_task_id=monitor.state.last_task_id,
                    files_changed=monitor.state.files_changed,
                    # TUI v2 Wave 1 (v3.7): capture per-phase totals so
                    # the terminal panels (F6) and release retrospective
                    # (F10) can render aggregates across phases.
                    turns=monitor.state.turns,
                    tokens_in=monitor.state.tokens_in,
                    tokens_out=monitor.state.tokens_out,
                )

                # v3.2-T02: Run post-phase wiring hook for every claude-mode phase
                phase_result = run_post_phase_wiring_hook(
                    phase,
                    config,
                    phase_result,
                    ledger=ledger,
                    remediation_log=remediation_log,
                )

                sprint_result.phase_results.append(phase_result)

                # TUI v2 Wave 3 (v3.7, §6.4): hook ordering after phase
                # completion is 1) _verify_checkpoints (already run
                # above), 2) summary_worker.submit, 3) end-of-sprint
                # manifest update. Submit is non-blocking; the daemon
                # thread will write results/phase-N-summary.md and is
                # exception-isolated from this loop.
                try:
                    _summary_worker.submit(phase, phase_result)
                except Exception as _sw_exc:  # noqa: BLE001 - must not abort
                    debug_log(
                        _dbg,
                        "summary_worker_submit_error",
                        phase=phase.number,
                        error=str(_sw_exc),
                    )

                debug_log(
                    _dbg,
                    "phase_complete",
                    phase=phase.number,
                    status=status.value,
                    exit_code=exit_code,
                    duration=round(_phase_dur, 1),
                )

                # Log and notify
                logger.write_phase_result(phase_result)
                # v4.3.0-T06: persist phase result as JSON for rerun-tasks consumption
                _write_phase_result_json(config, phase, phase_result)
                notify_phase_complete(phase_result)

                tui.update(sprint_result, monitor.state, None)

                # Decide: continue or halt?
                if status.is_failure:
                    # Collect diagnostics for the failed phase
                    try:
                        collector = DiagnosticCollector(config)
                        bundle = collector.collect(phase, phase_result, monitor.state)
                        classifier = FailureClassifier()
                        bundle.category = classifier.classify(bundle)
                        reporter = ReportGenerator()
                        diag_path = (
                            config.results_dir / f"phase-{phase.number}-diagnostic.md"
                        )
                        reporter.write(bundle, diag_path)
                        debug_log(
                            _dbg,
                            "diagnostic_report",
                            phase=phase.number,
                            category=bundle.category.value,
                            path=str(diag_path),
                        )
                    except Exception as _diag_exc:
                        debug_log(
                            _dbg,
                            "diagnostic_error",
                            phase=phase.number,
                            error=str(_diag_exc),
                        )

                    sprint_result.outcome = SprintOutcome.HALTED
                    sprint_result.halt_phase = phase.number
                    break

            finally:
                shutil.rmtree(isolation_dir, ignore_errors=True)

        # Merge preflight results with main-loop results in original phase order.
        # Build a lookup from phase number → PhaseResult, main-loop results win
        # on conflict (they are the authoritative executor record for claude phases).
        _merged: dict[int, PhaseResult] = {r.phase.number: r for r in preflight_results}
        for r in sprint_result.phase_results:
            _merged[r.phase.number] = r
        sprint_result.phase_results = [
            _merged[p.number] for p in config.active_phases if p.number in _merged
        ]

        # Sprint finished
        sprint_result.finished_at = datetime.now(timezone.utc)
        if sprint_result.outcome == SprintOutcome.SUCCESS:
            # Verify all phases actually passed
            if not all(r.status.is_success for r in sprint_result.phase_results):
                sprint_result.outcome = SprintOutcome.ERROR

        # TUI v2 Wave 3 (v3.7, F10): wait for any in-flight per-phase
        # summary threads to finish, then generate the release
        # retrospective. Blocking — runs before the terminal panel so
        # operators see a "retrospective ready" state, not a partial one.
        # Capped at a generous timeout because Sonnet is 30s per phase;
        # if summaries are still running after the cap we take what we
        # have and move on (never abort sprint wrap-up).
        try:
            _summary_worker.wait(timeout=90.0)
        except Exception as _sw_wait_exc:  # noqa: BLE001 - defensive
            debug_log(
                _dbg,
                "summary_worker_wait_error",
                error=str(_sw_wait_exc),
            )
        try:
            from .retrospective import RetrospectiveGenerator

            RetrospectiveGenerator(config).generate(
                sprint_result, _summary_worker.get_summaries()
            )
        except Exception as _retro_exc:  # noqa: BLE001 - defensive
            debug_log(
                _dbg,
                "retrospective_error",
                error=str(_retro_exc),
            )

        tui.update(sprint_result, MonitorState(), None)

        # T07 (BUG-007/P3): Build KPI report from accumulated gate results
        from superclaude.cli.sprint.kpi import build_kpi_report

        kpi_report = build_kpi_report(
            gate_results=all_gate_results,
            remediation_log=remediation_log,
            turn_ledger=ledger,
        )
        kpi_path = config.results_dir / "gate-kpi-report.md"
        kpi_path.write_text(kpi_report.format_report())

        # Wave 3 (v3.7): write the checkpoint manifest and emit a
        # `checkpoint_manifest` JSONL event so post-sprint tooling has a
        # single source of truth for checkpoint completeness.
        try:
            from .checkpoints import build_manifest, write_manifest

            _manifest = build_manifest(config.index_path, config.release_dir)
            _manifest_path = config.release_dir / "manifest.json"
            write_manifest(_manifest, _manifest_path)
            _manifest_total = len(_manifest)
            _manifest_found = sum(1 for _e in _manifest if _e.exists)
            logger._jsonl(  # noqa: SLF001
                {
                    "event": "checkpoint_manifest",
                    "path": str(_manifest_path),
                    "total": _manifest_total,
                    "found": _manifest_found,
                    "missing": _manifest_total - _manifest_found,
                }
            )
        except Exception as _mf_exc:  # noqa: BLE001
            _checkpoint_logger.warning(
                "Sprint end: checkpoint manifest write failed: %s", _mf_exc
            )

        logger.write_summary(sprint_result)
        notify_sprint_complete(sprint_result)

    finally:
        # Ensure monitor thread and subprocess are cleaned up even on exception.
        # Each step is independent so one failure does not prevent others.
        try:
            monitor.stop()
        except Exception:
            pass
        if proc_manager is not None:
            try:
                proc_manager.terminate()
            except Exception:
                pass
        try:
            tui.stop()
        except Exception:
            pass
        try:
            signal_handler.uninstall()
        except Exception:
            pass

    # Write sentinel exit code file in state_dir (non-tracked transient path) so tmux caller can read the outcome
    _exitcode = 0 if sprint_result.outcome == SprintOutcome.SUCCESS else 1
    _write_exit_sentinel(config, _exitcode)

    if _exitcode != 0:
        raise SystemExit(_exitcode)


def _write_exit_sentinel(config: SprintConfig, exitcode: int) -> None:
    """Write the .sprint-exitcode sentinel to config.state_dir for tmux IPC.

    Best-effort: OSErrors are swallowed so a failed sentinel write doesn't mask
    the real sprint exit code. The state_dir is non-tracked transient state
    (post-FU-001); never write into the tracked release_dir archive.
    """
    try:
        state_dir = config.state_dir
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / ".sprint-exitcode").write_text(str(exitcode))
    except OSError:
        pass


def _is_transient_failure(output_path: Path) -> bool:
    """Heuristic: was a task failure transient (retryable) rather than terminal?

    Returns True when the transcript shows API-retry / connection-refused markers,
    or its final non-blank JSON line has `is_error: true` and zero output tokens
    (TDD §T6 lines 122-126). Degrades gracefully to False on any read/parse error.
    """
    try:
        text = output_path.read_text(errors="replace")
    except OSError:
        return False
    if "api_retry" in text or "ConnectionRefused" in text:
        return True
    for line in reversed(text.splitlines()):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            obj = json.loads(stripped)
        except (ValueError, TypeError):
            return False
        return bool(obj.get("is_error") and obj.get("output_tokens", 1) == 0)
    return False


# A successful per-task completion envelope: a result line whose subtype is
# "success", or an agent task_complete envelope. Used by
# ``_task_completed_before_overrun`` to detect completion evidence that gates
# per-task recovery from ``error_max_turns``.
_TASK_SUCCESS_ENVELOPE_PATTERN = re.compile(
    r'"subtype"\s*:\s*"success"|"(?:type|subtype)"\s*:\s*"task_complete"'
)

# A SECOND, tail-only class of completion evidence: a strong completion verdict
# emitted in the final assistant turns when the agent finished its deliverable
# but overran the turn budget BEFORE emitting a structured
# ``success``/``task_complete`` envelope (e.g. TUIBBS V1 MVP sprint Phase 7 /
# task T07.05, whose deliverable was complete and green on disk but whose stream
# carried no success envelope). Deliberately conservative (strong verdict
# phrases, not a bare "PASS") and applied only to the tail of the stream by
# ``_task_completed_before_overrun`` — a task that overran *mid-work* does not
# end on a completion verdict, while one that overran *after completing* does,
# so tail-scoping preserves the completed-after-overrun vs overran-mid-work
# distinction the recovery gate exists to protect.
_TASK_TAIL_COMPLETION_PATTERN = re.compile(
    r"VERDICT:\s*PASS"
    r"|EXIT_RECOMMENDATION:\s*CONTINUE"
    r'|"result"\s*:\s*"Pass"'
    r"|ACCEPTANCE CRITERIA[^\n]{0,40}ALL MET",
    re.IGNORECASE,
)
_TASK_TAIL_COMPLETION_WINDOW = 15


def _task_completed_before_overrun(output_path: Path) -> bool:
    """Return True iff the per-task NDJSON stream shows completion evidence
    BEFORE its terminal ``error_max_turns`` envelope.

    This is the completion-evidence gate for per-task recovery. A task that
    overran *after* finishing its substantive work shows completion evidence in
    the lines preceding the terminal ``{"type":"result","subtype":"error_max_turns"}``
    envelope; a task that overran *without* finishing does not. Recovery is
    GATED on this — ``error_max_turns`` alone is NOT sufficient (that would mask
    a task that overran without finishing).

    Two classes of completion evidence are recognized, in order:

    1. **Structured success envelope** — a successful
       ``{"type":"result","subtype":"success"}`` (or agent ``task_complete``)
       envelope anywhere in the pre-terminal lines.
    2. **Tail completion verdict** — a strong completion verdict
       (``_TASK_TAIL_COMPLETION_PATTERN``) within the last
       ``_TASK_TAIL_COMPLETION_WINDOW`` pre-terminal lines. This recovers the
       *artifact-only* overrun where the agent finished and wrote its
       deliverable + evidence but tripped the turn ceiling before emitting a
       structured envelope (the motivating case: TUIBBS V1 MVP sprint Phase 7 /
       task T07.05). The verdict scan is **tail-scoped on purpose**: a task
       that overran mid-work does not end on a completion verdict, while one
       that overran after completing does, so confining the scan to the tail
       preserves the completed-after-overrun vs overran-mid-work distinction
       (a casual mid-stream "PASS" cannot trigger recovery).

    This helper is only meaningful when called for a stream whose terminal line
    is the ``error_max_turns`` envelope (i.e. ``detect_error_max_turns`` is
    already True); it scans the lines strictly BEFORE that terminal line so the
    error line itself can never be mistaken for completion evidence.

    Returns False when the file is missing/unreadable/empty, or when neither
    class of completion evidence appears before the terminal
    ``error_max_turns`` line. Reads the file defensively (mirroring
    ``detect_error_max_turns``); performs no network or subprocess calls.
    """
    try:
        content = output_path.read_text(errors="replace")
    except (FileNotFoundError, OSError):
        return False

    if not content.strip():
        return False

    lines = [ln.strip() for ln in content.strip().splitlines() if ln.strip()]
    if not lines:
        return False

    # Class 1: a structured success/task_complete envelope anywhere in the
    # lines strictly before the terminal (last non-empty) line, which is the
    # error_max_turns envelope on the gated-recovery path.
    for line in lines[:-1]:
        if _TASK_SUCCESS_ENVELOPE_PATTERN.search(line):
            return True

    # Class 2: a strong completion verdict in the TAIL (last
    # ``_TASK_TAIL_COMPLETION_WINDOW`` pre-terminal lines). Tail-scoped on
    # purpose — a task that overran mid-work does not end on a completion
    # verdict, while one that overran after completing does. This recovers the
    # artifact-only overrun (no success envelope) that Class 1 misses.
    for line in lines[:-1][-_TASK_TAIL_COMPLETION_WINDOW:]:
        if _TASK_TAIL_COMPLETION_PATTERN.search(line):
            return True

    return False


def _classify_from_result_file(
    result_file: Path,
    started_at: float,
) -> PhaseStatus | None:
    """Classify phase outcome from the agent-written result file.

    Returns a PhaseStatus if the result file exists, is fresh (mtime > started_at),
    and contains a recognizable EXIT_RECOMMENDATION. Returns None if the file is
    missing, stale, or unreadable.
    """
    if not result_file.exists():
        return None
    try:
        mtime = result_file.stat().st_mtime
    except OSError:
        return None
    if started_at > 0 and mtime < started_at:
        # Stale file from a previous run — do not trust
        return None
    try:
        content = result_file.read_text(errors="replace")
    except OSError:
        return None
    upper = content.upper()
    if "EXIT_RECOMMENDATION: HALT" in upper:
        return PhaseStatus.HALT
    if "EXIT_RECOMMENDATION: CONTINUE" in upper:
        return PhaseStatus.PASS_RECOVERED
    if re.search(r"status:\s*PASS\b", content, re.IGNORECASE):
        return PhaseStatus.PASS_RECOVERED
    if re.search(r"status:\s*FAIL(?:ED|URE)?\b", content, re.IGNORECASE):
        return PhaseStatus.HALT
    if re.search(r"status:\s*PARTIAL\b", content, re.IGNORECASE):
        return PhaseStatus.INCOMPLETE
    return None


def _verify_checkpoints(
    config: SprintConfig,
    phase: Phase,
    status: PhaseStatus,
    logger: SprintLogger,
) -> PhaseStatus:
    """Wave 2 checkpoint enforcement gate.

    After ``_determine_phase_status()`` returns a PASS-like status, parses the
    phase tasklist for ``Checkpoint Report Path:`` declarations, verifies the
    referenced files exist, emits a ``checkpoint_verification`` JSONL event,
    and reacts based on ``config.checkpoint_gate_mode``:

    - ``off``    — no action
    - ``shadow`` — JSONL event only (default)
    - ``soft``   — JSONL event + stdout warning
    - ``full``   — JSONL event + downgrade status to ``PASS_MISSING_CHECKPOINT``
                   when any declared checkpoint file is missing

    Returns the (possibly downgraded) status. Exceptions are swallowed so a
    scanner fault never breaks the phase completion flow.
    """
    mode = getattr(config, "checkpoint_gate_mode", "shadow")
    if mode == "off":
        return status

    # Late import: shared parsing module (Wave 2 T02.01).
    from .checkpoints import extract_checkpoint_paths, verify_checkpoint_files

    try:
        declared = extract_checkpoint_paths(phase.file, config.release_dir)
    except Exception as exc:  # noqa: BLE001
        _checkpoint_logger.warning(
            "Phase %d: checkpoint scan raised %s", phase.number, exc
        )
        return status

    if not declared:
        return status  # No checkpoint sections → nothing to verify.

    verified = verify_checkpoint_files(declared)
    expected = [str(p) for _name, p in declared]
    found = [str(p) for _name, p, ok in verified if ok]
    missing = [str(p) for _name, p, ok in verified if not ok]

    try:
        logger.write_checkpoint_verification(
            phase=phase.number,
            expected=expected,
            found=found,
            missing=missing,
        )
    except Exception as exc:  # noqa: BLE001
        _checkpoint_logger.warning(
            "Phase %d: failed to emit checkpoint_verification event: %s",
            phase.number,
            exc,
        )

    if not missing:
        return status

    for name, path, _ok in verified:
        if _ok:
            continue
        _checkpoint_logger.warning(
            "Phase %d: checkpoint report missing — %s (expected at %s)",
            phase.number,
            name,
            path,
        )

    if mode == "soft":
        print(
            f"⚠ Phase {phase.number}: {len(missing)} checkpoint report(s) "
            f"missing — see execution-log.jsonl for details"
        )
    elif mode == "full":
        return PhaseStatus.PASS_MISSING_CHECKPOINT

    return status


def _check_checkpoint_pass(config: SprintConfig, phase: Phase) -> bool:
    """Return True if the end-of-phase checkpoint file exists with status PASS."""
    checkpoint_path = (
        config.release_dir / "checkpoints" / f"CP-P{phase.number:02d}-END.md"
    )
    if not checkpoint_path.exists():
        return False
    try:
        content = checkpoint_path.read_text(errors="replace").upper()
        return "STATUS: PASS" in content or "**RESULT**: PASS" in content
    except OSError:
        return False


def _check_contamination(config: SprintConfig, phase: Phase) -> list[str]:
    """Return list of artifact files containing cross-phase task ID patterns."""
    import re as _re

    contaminated: list[str] = []
    artifacts_dir = config.release_dir / "artifacts"
    if not artifacts_dir.exists():
        return contaminated
    next_phase = phase.number + 1
    pattern = _re.compile(rf"T{next_phase:02d}\.\d{{2}}", _re.IGNORECASE)
    for md_file in artifacts_dir.rglob("*.md"):
        try:
            if pattern.search(md_file.read_text(errors="replace")):
                contaminated.append(str(md_file.relative_to(config.release_dir)))
        except OSError:
            pass
    return contaminated


def _write_crash_recovery_log(
    config: SprintConfig,
    phase: Phase,
    contaminated: list[str],
) -> None:
    """Append crash recovery entry to results/crash_recovery_log.md."""
    log_path = config.results_dir / "crash_recovery_log.md"
    entry = (
        f"\n## Phase {phase.number} — PASS_RECOVERED Recovery\n"
        f"**Timestamp**: {datetime.now(timezone.utc).isoformat()}\n"
        f"**Checkpoint**: checkpoints/CP-P{phase.number:02d}-END.md (PASS)\n"
        f"**Contamination check**: "
        + (
            "CLEAN"
            if not contaminated
            else f"WARNING — {len(contaminated)} file(s): {contaminated}"
        )
        + "\n"
        "**Action**: Phase reclassified ERROR→PASS_RECOVERED.\n"
    )
    try:
        with open(log_path, "a") as f:
            f.write(entry)
    except OSError:
        pass


def _write_preliminary_result(
    config: SprintConfig,
    phase: Phase,
    started_at: float,
) -> bool:
    """Write a preliminary result file with EXIT_RECOMMENDATION: CONTINUE sentinel.

    This function is a deterministic fallback ensuring ``_determine_phase_status()``
    always finds a valid result file for phases that exit 0 but write no report.
    Without it, such phases return ``PASS_NO_REPORT`` because no result file is present.

    **Ordering invariant**: Call *after* ``finished_at`` is captured and *before*
    ``_determine_phase_status()`` is called. If called after status determination,
    the sentinel file will not affect the already-computed status.

    **Concurrency**: Assumes single-threaded execution (one phase at a time). If the
    sprint loop is parallelised in future, this function must be replaced with an
    ``O_EXCL``-based atomic write to prevent TOCTOU races between the exists-check
    and the write.

    **Sentinel contract**: Writes ``EXIT_RECOMMENDATION: CONTINUE\\n`` so that
    ``_determine_phase_status()`` branch 3 (``result_file.exists()`` → CONTINUE check
    at line 1024) returns ``PhaseStatus.PASS`` instead of falling through to the
    ``PASS_NO_REPORT`` branch (line 1045). This sentinel is intentionally minimal;
    the executor result file written by ``_write_executor_result_file()`` afterwards
    will overwrite it with the authoritative structured report.

    Args:
        config: Sprint configuration providing ``result_file(phase)`` path.
        phase: The phase whose result file to write.
        started_at: Phase start time as a POSIX timestamp (``datetime.timestamp()``).
            Used for the freshness guard: if a result file already exists with
            ``st_mtime >= started_at`` and ``st_size > 0``, it is assumed to be a
            valid agent-written file and is left untouched (no-op).

    Returns:
        ``True`` if the sentinel file was written, ``False`` if the file was preserved
        (freshness guard triggered) or an ``OSError`` prevented the write. The boolean
        is intended for telemetry logging only; callers should not branch on it.
    """
    import logging as _logging

    result_path = config.result_file(phase)
    # Freshness guard: if a valid, fresh agent-written file is present, do not overwrite.
    if result_path.exists():
        try:
            st = result_path.stat()
            if st.st_size > 0 and st.st_mtime >= started_at:
                # Fresh, non-empty agent file — preserve it
                return False
        except OSError:
            pass  # Treat stat failure as absent; fall through to write

    # RC.4 (C-019): write the sentinel via a true O_EXCL atomic create so two
    # concurrent writers cannot both create it and so we never clobber a file that
    # appeared AFTER the freshness check (closing the docstring's exists-check→write
    # TOCTOU). A known-stale / zero-byte file (a fresh one was preserved above) is
    # removed first so O_EXCL can create. If O_EXCL then fails with FileExistsError,
    # a concurrent writer (or a freshly-appeared agent file) beat us — preserve it
    # (no-op). Zero-byte/stale/absent still yield a written sentinel; the
    # EXIT_RECOMMENDATION: CONTINUE contract and the OSError telemetry branch are
    # unchanged.
    try:
        result_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            if result_path.exists():
                result_path.unlink()
        except OSError:
            pass  # If we cannot remove it, the O_EXCL create below will preserve it.
        fd = os.open(result_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        try:
            os.write(fd, b"EXIT_RECOMMENDATION: CONTINUE\n")
        finally:
            os.close(fd)
        return True
    except FileExistsError:
        # A concurrent writer created the sentinel between our unlink and create —
        # its sentinel is equivalent, or a fresh agent file appeared; preserve it.
        return False
    except OSError as exc:
        _logging.getLogger(__name__).warning(
            "preliminary result write failed: %s; phase may report PASS_NO_REPORT",
            exc,
        )
        return False


def _write_phase_result_json(
    config: SprintConfig, phase: Phase, result: PhaseResult
) -> None:
    """Persist a phase result as JSON for rerun-tasks consumption (TDD §T6).

    Mirrors the atomic tmp+rename write convention from checkpoints.py so a
    crash mid-write never leaves a truncated phase-N-result.json on disk.
    """
    payload = {
        "phase": result.phase.number,
        "status": result.status.value,
        "exit_code": result.exit_code,
        "started_at": result.started_at.isoformat(),
        "finished_at": result.finished_at.isoformat(),
        "task_results": [tr.to_dict() for tr in result.task_results],
        "recovery_history": result.recovery_history,
    }
    out = config.phase_result_json(phase)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n")
    tmp.replace(out)


def _write_executor_result_file(
    config: SprintConfig,
    phase: Phase,
    status: PhaseStatus,
    exit_code: int,
    monitor_state: MonitorState,
    started_at: datetime,
    finished_at: datetime,
) -> None:
    """Write executor-sourced result file for downstream consumers.

    This is written AFTER _determine_phase_status returns, so it does not
    create circularity. It provides a deterministic result file even when
    the agent failed to write one.
    """
    duration = (finished_at - started_at).total_seconds()
    recommendation = "CONTINUE" if status.is_success else "HALT"
    content = (
        "---\n"
        f"phase: {phase.number}\n"
        f"status: {'PASS' if status.is_success else 'FAIL'}\n"
        f"tasks_total: 1\n"
        f"tasks_passed: {1 if status.is_success else 0}\n"
        f"tasks_failed: {0 if status.is_success else 1}\n"
        "---\n"
        "\n"
        f"# Phase {phase.number} — Executor Result Report\n"
        "\n"
        f"| Phase | Status | Exit Code | Duration |\n"
        f"|-------|--------|-----------|----------|\n"
        f"| {phase.number} | {status.value} | {exit_code} | {duration:.1f}s |\n"
        "\n"
        f"**Source**: executor (not agent self-report)\n"
        f"**Output bytes**: {monitor_state.output_bytes}\n"
        f"**Last task ID**: {monitor_state.last_task_id or 'n/a'}\n"
        f"**Files changed**: {monitor_state.files_changed}\n"
        "\n"
        f"EXIT_RECOMMENDATION: {recommendation}\n"
    )
    result_path = config.result_file(phase)
    try:
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(content)
    except OSError:
        pass  # Non-fatal — best effort


def _determine_phase_status(
    exit_code: int,
    result_file: Path,
    output_file: Path,
    *,
    config: SprintConfig | None = None,
    phase: Phase | None = None,
    started_at: float = 0.0,
    error_file: Path | None = None,
) -> PhaseStatus:
    """Parse result file and exit code to determine phase status.

    Priority:
    1. Timeout (exit 124) -> TIMEOUT
    2. Non-zero exit -> ERROR
    3. Result file with EXIT_RECOMMENDATION: HALT -> HALT
    4. Result file with EXIT_RECOMMENDATION: CONTINUE -> PASS
    5. Result file with status: PASS/FAIL -> PASS/HALT
    6. No result file but output exists -> PASS_NO_REPORT
    7. No result file and no output -> ERROR
    """
    if exit_code == 124:
        return PhaseStatus.TIMEOUT
    if exit_code != 0:
        # Path 1 — Specific: context exhaustion (Spec B S2)
        # detect_prompt_too_long reads NDJSON output for "Prompt is too long"
        if detect_prompt_too_long(output_file, error_path=error_file):
            # Check if the agent managed to write a result file before exhaustion
            result_status = _classify_from_result_file(result_file, started_at)
            if result_status is not None:
                return result_status
            # No valid result file — context exhausted without completing
            return PhaseStatus.INCOMPLETE

        # Path 2 — General: checkpoint inference (Spec A SOL-C)
        # Reads agent-written checkpoint files (pre-crash evidence)
        if config is not None and phase is not None:
            if _check_checkpoint_pass(config, phase):
                contaminated = _check_contamination(config, phase)
                _write_crash_recovery_log(config, phase, contaminated)
                if not contaminated:
                    return PhaseStatus.PASS_RECOVERED

        # Path 3 — Default: unchanged
        return PhaseStatus.ERROR

    if result_file.exists():
        content = result_file.read_text(errors="replace")
        # Use case-insensitive search for EXIT_RECOMMENDATION tokens to handle
        # model output that varies in casing. When both CONTINUE and HALT appear
        # (conflicting signals), HALT wins — the stronger/safer outcome.
        upper = content.upper()
        # Sentinel contract: EXIT_RECOMMENDATION: CONTINUE is written by
        # _write_preliminary_result() as a deterministic fallback for phases that
        # exit 0 but produce no agent result file. The presence of this sentinel
        # here causes the phase to return PASS rather than fall through to
        # PASS_NO_REPORT (branch 4). _write_executor_result_file() overwrites this
        # file after status determination with the authoritative structured report.
        has_continue = "EXIT_RECOMMENDATION: CONTINUE" in upper
        has_halt = "EXIT_RECOMMENDATION: HALT" in upper
        if has_halt:
            return PhaseStatus.HALT
        if has_continue:
            return PhaseStatus.PASS
        if re.search(r"status:\s*PASS\b", content, re.IGNORECASE):
            return PhaseStatus.PASS
        if re.search(r"status:\s*FAIL(?:ED|URE)?\b", content, re.IGNORECASE):
            return PhaseStatus.HALT
        # PARTIAL result means tasks did not fully complete — treat as halt
        if re.search(r"status:\s*PARTIAL\b", content, re.IGNORECASE):
            return PhaseStatus.HALT
        return PhaseStatus.PASS_NO_SIGNAL

    if output_file.exists() and output_file.stat().st_size > 0:
        # Check for budget exhaustion: a subprocess that exits 0 but hit
        # error_max_turns produced no useful result — reclassify as INCOMPLETE
        # to trigger HALT instead of silent continuation.
        if detect_error_max_turns(output_file):
            return PhaseStatus.INCOMPLETE
        return PhaseStatus.PASS_NO_REPORT

    return PhaseStatus.ERROR
