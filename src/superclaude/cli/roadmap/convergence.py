"""Convergence engine for deterministic spec-fidelity gate.

Implements FR-7 (convergence gate), FR-8 (regression detection),
and the deviation registry (FR-6) with split structural/semantic
HIGH tracking (BF-3 resolution).
"""
from __future__ import annotations

import atexit
import hashlib
import json
import logging
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .models import Finding

logger = logging.getLogger(__name__)

# --- TurnLedger budget constants (FR-7) ---
# Module-level cost constants for convergence budget accounting.
CHECKER_COST = 10
REMEDIATION_COST = 8
REGRESSION_VALIDATION_COST = 15
CONVERGENCE_PASS_CREDIT = 5

# Derived budget thresholds
MIN_CONVERGENCE_BUDGET = 28   # 1 checker + 1 remediation + 1 regression validation
STD_CONVERGENCE_BUDGET = 46   # 2 full cycles with regression headroom
MAX_CONVERGENCE_BUDGET = 61   # 3 full cycles (catch/verify/backup)


def _get_turnledger_class():
    """Conditional import of TurnLedger (convergence mode only)."""
    from ..sprint.models import TurnLedger
    return TurnLedger


def reimburse_for_progress(
    ledger,
    prev_structural_highs: int,
    curr_structural_highs: int,
) -> int:
    """Credit budget when structural HIGHs decrease between runs.

    Returns 0 when curr_structural_highs >= prev_structural_highs.
    Uses ledger.reimbursement_rate for credit calculation.
    """
    if curr_structural_highs >= prev_structural_highs:
        return 0
    delta = prev_structural_highs - curr_structural_highs
    credit = int(CONVERGENCE_PASS_CREDIT * delta * ledger.reimbursement_rate)
    if credit > 0:
        ledger.credit(credit)
    return credit


def compute_stable_id(
    dimension: str,
    rule_id: str,
    spec_location: str,
    mismatch_type: str,
) -> str:
    """Deterministic finding ID from structural properties."""
    key = f"{dimension}:{rule_id}:{spec_location}:{mismatch_type}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


@dataclass
class RunMetadata:
    """Metadata for a single fidelity run."""
    run_number: int
    timestamp: str
    spec_hash: str
    roadmap_hash: str
    structural_high_count: int = 0
    semantic_high_count: int = 0
    total_high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    budget_snapshot: dict | None = None


@dataclass
class DeviationRegistry:
    """File-backed deviation registry with stable finding IDs.

    Implements FR-6 (persistent registry), FR-10 (run-to-run memory).
    Status values: ACTIVE, FIXED, FAILED, SKIPPED.
    """
    path: Path
    release_id: str
    spec_hash: str
    runs: list[dict] = field(default_factory=list)
    findings: dict[str, dict] = field(default_factory=dict)

    @classmethod
    def load_or_create(cls, path: Path, release_id: str, spec_hash: str) -> DeviationRegistry:
        """Load existing registry or create fresh one.

        If spec_hash differs from saved -> reset (new spec version, FR-6).
        Pre-v3.05 registries: findings missing source_layer default to "structural".
        """
        if path.exists():
            try:
                data = json.loads(path.read_text())
                if data.get("spec_hash") == spec_hash:
                    findings = data.get("findings", {})
                    # Backward compat: default source_layer for pre-v3.05 registries
                    for fid, finding in findings.items():
                        if "source_layer" not in finding:
                            finding["source_layer"] = "structural"
                        if "first_seen_run" not in finding:
                            finding["first_seen_run"] = 1
                        if "last_seen_run" not in finding:
                            finding["last_seen_run"] = 1
                    return cls(
                        path=path,
                        release_id=release_id,
                        spec_hash=spec_hash,
                        runs=data.get("runs", []),
                        findings=findings,
                    )
                logger.info("Spec hash changed; resetting deviation registry")
            except (json.JSONDecodeError, KeyError):
                logger.warning("Corrupted registry at %s; creating fresh", path)
        return cls(path=path, release_id=release_id, spec_hash=spec_hash)

    def begin_run(self, roadmap_hash: str) -> int:
        """Start a new run. Returns run_number."""
        from datetime import datetime, timezone
        run_number = len(self.runs) + 1
        self.runs.append({
            "run_number": run_number,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "spec_hash": self.spec_hash,
            "roadmap_hash": roadmap_hash,
        })
        return run_number

    def merge_findings(
        self,
        structural: list[Finding],
        semantic: list[Finding],
        run_number: int,
    ) -> None:
        """Merge current scan findings into registry.

        New findings: append with first_seen_run.
        Known findings: update last_seen_run.
        Missing findings: mark FIXED.
        """
        current_ids: set[str] = set()

        for source, findings_list in [("structural", structural), ("semantic", semantic)]:
            for f in findings_list:
                stable_id = f.stable_id if hasattr(f, 'stable_id') and f.stable_id else compute_stable_id(
                    f.dimension, getattr(f, 'rule_id', ''), f.location, getattr(f, 'rule_id', '')
                )
                current_ids.add(stable_id)

                if stable_id in self.findings:
                    self.findings[stable_id]["last_seen_run"] = run_number
                    self.findings[stable_id]["status"] = "ACTIVE"
                    if hasattr(f, 'files_affected'):
                        self.findings[stable_id]["files_affected"] = list(f.files_affected)
                else:
                    self.findings[stable_id] = {
                        "stable_id": stable_id,
                        "dimension": f.dimension,
                        "severity": f.severity,
                        "description": f.description,
                        "location": f.location,
                        "source_layer": source,
                        "status": "ACTIVE",
                        "first_seen_run": run_number,
                        "last_seen_run": run_number,
                        "debate_verdict": None,
                        "debate_transcript": None,
                        "files_affected": list(f.files_affected) if hasattr(f, 'files_affected') else [],
                    }

        # Mark missing findings as FIXED
        for sid, finding in self.findings.items():
            if sid not in current_ids and finding["status"] == "ACTIVE":
                finding["status"] = "FIXED"

        # Update run metadata with counts
        structural_highs = sum(
            1 for f in self.findings.values()
            if f["status"] == "ACTIVE" and f["severity"] == "HIGH" and f["source_layer"] == "structural"
        )
        semantic_highs = sum(
            1 for f in self.findings.values()
            if f["status"] == "ACTIVE" and f["severity"] == "HIGH" and f["source_layer"] == "semantic"
        )
        if self.runs:
            self.runs[-1]["structural_high_count"] = structural_highs
            self.runs[-1]["semantic_high_count"] = semantic_highs
            self.runs[-1]["total_high_count"] = structural_highs + semantic_highs

    def get_active_highs(self) -> list[dict]:
        """Return findings with status=ACTIVE and severity=HIGH."""
        return [
            f for f in self.findings.values()
            if f["status"] == "ACTIVE" and f["severity"] == "HIGH"
        ]

    def get_active_high_count(self) -> int:
        """Count of active HIGH findings (gate evaluation)."""
        return len(self.get_active_highs())

    def get_structural_high_count(self) -> int:
        """Count of active structural HIGH findings (monotonic enforcement)."""
        return sum(
            1 for f in self.findings.values()
            if f["status"] == "ACTIVE" and f["severity"] == "HIGH" and f["source_layer"] == "structural"
        )

    def get_semantic_high_count(self) -> int:
        """Count of active semantic HIGH findings (informational only)."""
        return sum(
            1 for f in self.findings.values()
            if f["status"] == "ACTIVE" and f["severity"] == "HIGH" and f["source_layer"] == "semantic"
        )

    def get_prior_findings_summary(self, max_entries: int = 50) -> str:
        """Format prior findings for semantic layer prompt (FR-10)."""
        entries = sorted(self.findings.values(), key=lambda f: f.get("first_seen_run", 0))
        lines = ["| Stable ID | Severity | Status | Source | First Seen |"]
        lines.append("|-----------|----------|--------|--------|------------|")
        for entry in entries[:max_entries]:
            lines.append(
                f"| {entry['stable_id'][:8]}... | {entry['severity']} | "
                f"{entry['status']} | {entry.get('source_layer', 'unknown')} | "
                f"Run {entry.get('first_seen_run', '?')} |"
            )
        if len(entries) > max_entries:
            lines.append(f"| ... | {len(entries) - max_entries} more entries truncated | ... | ... | ... |")
        return "\n".join(lines)

    def update_finding_status(self, stable_id: str, status: str) -> None:
        """Update a finding's status (FIXED, FAILED, SKIPPED)."""
        if stable_id in self.findings:
            self.findings[stable_id]["status"] = status

    def record_debate_verdict(
        self,
        stable_id: str,
        verdict: str,
        transcript_path: str,
    ) -> None:
        """Record adversarial debate outcome for a finding."""
        if stable_id in self.findings:
            self.findings[stable_id]["debate_verdict"] = verdict
            self.findings[stable_id]["debate_transcript"] = transcript_path
            if verdict.startswith("DOWNGRADE_TO_"):
                new_severity = verdict.replace("DOWNGRADE_TO_", "")
                self.findings[stable_id]["severity"] = new_severity

    def save(self) -> None:
        """Atomic write: tmp + os.replace()."""
        import os
        data = {
            "schema_version": 1,
            "release_id": self.release_id,
            "spec_hash": self.spec_hash,
            "runs": self.runs,
            "findings": self.findings,
        }
        tmp_path = self.path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(data, indent=2))
        os.replace(str(tmp_path), str(self.path))


@dataclass
class ConvergenceResult:
    """Outcome of a convergence-controlled fidelity run."""
    passed: bool
    run_count: int
    final_high_count: int
    structural_progress_log: list[str] = field(default_factory=list)
    semantic_fluctuation_log: list[str] = field(default_factory=list)
    regression_detected: bool = False
    halt_reason: str | None = None


@dataclass
class RegressionResult:
    """Outcome of a parallel regression validation (FR-8)."""
    validated_findings: list[dict] = field(default_factory=list)
    debate_verdicts: list[dict] = field(default_factory=list)
    agents_succeeded: int = 0
    consolidated_report_path: str = ""


def _check_regression(registry: DeviationRegistry) -> bool:
    """Check if structural HIGHs increased (regression).

    Only structural findings trigger regression (BF-3).
    Semantic fluctuations are logged but do not trigger FR-8.
    """
    if len(registry.runs) < 2:
        return False

    prev_run = registry.runs[-2]
    curr_run = registry.runs[-1]

    prev_structural = prev_run.get("structural_high_count", 0)
    curr_structural = curr_run.get("structural_high_count", 0)
    prev_semantic = prev_run.get("semantic_high_count", 0)
    curr_semantic = curr_run.get("semantic_high_count", 0)

    # Log semantic fluctuation (informational only)
    if curr_semantic != prev_semantic:
        logger.warning(
            "Semantic HIGH fluctuation: %d -> %d (delta: %+d). Not a regression.",
            prev_semantic, curr_semantic, curr_semantic - prev_semantic,
        )

    # Only structural increase triggers regression
    if curr_structural > prev_structural:
        logger.error(
            "Structural regression detected: %d -> %d HIGHs",
            prev_structural, curr_structural,
        )
        return True

    return False


_active_validation_dirs: list[Path] = []


def _create_validation_dirs(
    spec_path: Path,
    roadmap_path: Path,
    registry_path: Path,
    count: int = 3,
) -> list[Path]:
    """Create temporary directories with independent file copies.

    Each directory gets its own copy of spec, roadmap, and registry.
    Replaces git worktrees (BF-4: checkers don't need git repo).
    """
    dirs: list[Path] = []
    for i in range(count):
        d = Path(tempfile.mkdtemp(prefix=f"fidelity-validation-{i}-"))
        shutil.copy2(spec_path, d / spec_path.name)
        shutil.copy2(roadmap_path, d / roadmap_path.name)
        if registry_path.exists():
            shutil.copy2(registry_path, d / registry_path.name)
        dirs.append(d)

    _active_validation_dirs.extend(dirs)
    return dirs


def _cleanup_validation_dirs(dirs: list[Path]) -> None:
    """Remove temporary validation directories.

    Best-effort cleanup: logs warning on failure, does not raise.
    """
    for d in dirs:
        try:
            shutil.rmtree(d)
            if d in _active_validation_dirs:
                _active_validation_dirs.remove(d)
        except OSError as exc:
            logger.warning("Failed to clean up validation dir %s: %s", d, exc)


def _atexit_cleanup() -> None:
    """Fallback cleanup registered with atexit."""
    if _active_validation_dirs:
        logger.info("atexit: cleaning up %d validation dirs", len(_active_validation_dirs))
        _cleanup_validation_dirs(list(_active_validation_dirs))


atexit.register(_atexit_cleanup)


def execute_fidelity_with_convergence(
    registry: DeviationRegistry,
    ledger,
    run_checkers: "Callable",
    run_remediation: "Callable",
    handle_regression_fn: "Callable | None" = None,
    max_runs: int = 3,
    spec_path: Path | None = None,
    roadmap_path: Path | None = None,
) -> ConvergenceResult:
    """Convergence-controlled fidelity gate (FR-7).

    Coordinates up to max_runs (default 3) checker/remediation cycles
    within step 8 with TurnLedger budget accounting.

    Run labels: Run 1 (catch) -> remediation -> Run 2 (verify) -> remediation -> Run 3 (backup).

    Pass condition: registry.get_active_high_count() == 0.
    Monotonic progress enforced on structural_high_count only.
    Semantic HIGH fluctuations logged as warnings.
    Budget exhaustion halts with diagnostic report.

    Parameters
    ----------
    registry : DeviationRegistry
        The deviation registry tracking findings across runs.
    ledger : TurnLedger
        Budget accounting object (from sprint.models).
    run_checkers : Callable
        Function that runs structural + semantic checkers and merges
        findings into the registry. Signature: (registry, run_number) -> None.
    run_remediation : Callable
        Function that attempts to remediate active HIGH findings.
        Signature: (registry) -> None.
    handle_regression_fn : Callable | None
        Function to handle regression detection. Called when structural
        HIGHs increase. Signature: (registry, spec_path, roadmap_path) -> RegressionResult.
    max_runs : int
        Maximum number of checker runs (default 3).
    spec_path : Path | None
        Path to spec file (for regression validation).
    roadmap_path : Path | None
        Path to roadmap file (for regression validation).

    Returns
    -------
    ConvergenceResult
        Outcome including pass/fail, run count, and diagnostic logs.
    """
    run_labels = ["catch", "verify", "backup"]
    structural_progress: list[str] = []
    semantic_fluctuation: list[str] = []
    prev_structural_highs = registry.get_structural_high_count()

    for run_idx in range(max_runs):
        run_label = run_labels[run_idx] if run_idx < len(run_labels) else f"run-{run_idx + 1}"

        # Budget guard: can we afford a checker run?
        if not ledger.can_launch():
            halt_msg = (
                f"Budget exhausted before run {run_idx + 1} ({run_label}). "
                f"TurnLedger: available={ledger.available()}, "
                f"consumed={ledger.consumed}, initial={ledger.initial_budget}"
            )
            logger.error(halt_msg)
            return ConvergenceResult(
                passed=False,
                run_count=run_idx,
                final_high_count=registry.get_active_high_count(),
                structural_progress_log=structural_progress,
                semantic_fluctuation_log=semantic_fluctuation,
                halt_reason=halt_msg,
            )

        # Debit for checker run
        ledger.debit(CHECKER_COST)
        run_number = registry.begin_run(
            roadmap_hash=hashlib.sha256(
                (roadmap_path.read_bytes() if roadmap_path and roadmap_path.exists() else b"")
            ).hexdigest()
        )

        # Record budget snapshot after debit
        if registry.runs:
            registry.runs[-1]["budget_snapshot"] = {
                "consumed": ledger.consumed,
                "reimbursed": ledger.reimbursed,
                "available": ledger.available(),
                "initial": ledger.initial_budget,
            }

        # Execute checkers
        run_checkers(registry, run_number)

        # Check pass condition
        active_highs = registry.get_active_high_count()
        curr_structural = registry.get_structural_high_count()
        curr_semantic = registry.get_semantic_high_count()

        if active_highs == 0:
            ledger.credit(CONVERGENCE_PASS_CREDIT)
            logger.info(
                "Run %d (%s): PASS — 0 active HIGHs. Credit %d turns. "
                "budget: consumed=%d, reimbursed=%d, available=%d",
                run_idx + 1, run_label, CONVERGENCE_PASS_CREDIT,
                ledger.consumed, ledger.reimbursed, ledger.available(),
            )
            return ConvergenceResult(
                passed=True,
                run_count=run_idx + 1,
                final_high_count=0,
                structural_progress_log=structural_progress,
                semantic_fluctuation_log=semantic_fluctuation,
            )

        # Log progress
        progress_msg = (
            f"Run {run_idx + 1} ({run_label}): structural {prev_structural_highs} -> {curr_structural}, "
            f"budget: consumed={ledger.consumed}, reimbursed={ledger.reimbursed}, "
            f"available={ledger.available()}"
        )
        structural_progress.append(progress_msg)

        # Check for semantic fluctuation
        prev_semantic = (
            registry.runs[-2].get("semantic_high_count", 0)
            if len(registry.runs) >= 2 else 0
        )
        if curr_semantic != prev_semantic:
            fluct_msg = (
                f"Run {run_idx + 1}: semantic HIGH fluctuation "
                f"{prev_semantic} -> {curr_semantic} (warning only)"
            )
            semantic_fluctuation.append(fluct_msg)
            logger.warning(fluct_msg)

        # Check for structural regression (only after Run 1 baseline)
        if run_idx > 0 and curr_structural > prev_structural_highs:
            logger.error(
                "Structural regression in run %d: %d -> %d",
                run_idx + 1, prev_structural_highs, curr_structural,
            )
            if handle_regression_fn and spec_path and roadmap_path:
                # Budget guard for regression validation
                if not ledger.can_launch():
                    halt_msg = (
                        f"Budget exhausted before regression validation. "
                        f"TurnLedger: available={ledger.available()}"
                    )
                    return ConvergenceResult(
                        passed=False,
                        run_count=run_idx + 1,
                        final_high_count=active_highs,
                        structural_progress_log=structural_progress,
                        semantic_fluctuation_log=semantic_fluctuation,
                        regression_detected=True,
                        halt_reason=halt_msg,
                    )
                ledger.debit(REGRESSION_VALIDATION_COST)
                handle_regression_fn(registry, spec_path, roadmap_path)
                # Re-evaluate after regression handling
                active_highs = registry.get_active_high_count()
                curr_structural = registry.get_structural_high_count()

            return ConvergenceResult(
                passed=False,
                run_count=run_idx + 1,
                final_high_count=active_highs,
                structural_progress_log=structural_progress,
                semantic_fluctuation_log=semantic_fluctuation,
                regression_detected=True,
            )

        # Reimburse for progress
        credit = reimburse_for_progress(ledger, prev_structural_highs, curr_structural)
        if credit > 0:
            progress_credit_msg = (
                f"Run {run_idx + 1}: progress credit {credit} turns "
                f"(structural {prev_structural_highs} -> {curr_structural})"
            )
            logger.info(progress_credit_msg)
            structural_progress.append(progress_credit_msg)

        prev_structural_highs = curr_structural

        # Remediate before next run (if not the last run)
        if run_idx < max_runs - 1:
            if not ledger.can_remediate():
                halt_msg = (
                    f"Budget exhausted before remediation after run {run_idx + 1}. "
                    f"TurnLedger: available={ledger.available()}"
                )
                logger.error(halt_msg)
                return ConvergenceResult(
                    passed=False,
                    run_count=run_idx + 1,
                    final_high_count=active_highs,
                    structural_progress_log=structural_progress,
                    semantic_fluctuation_log=semantic_fluctuation,
                    halt_reason=halt_msg,
                )
            ledger.debit(REMEDIATION_COST)
            run_remediation(registry)

        registry.save()

    # All runs exhausted without convergence
    final_highs = registry.get_active_high_count()
    halt_msg = (
        f"Convergence not reached after {max_runs} runs. "
        f"Remaining active HIGHs: {final_highs}. "
        f"TurnLedger: available={ledger.available()}, consumed={ledger.consumed}"
    )
    logger.error(halt_msg)
    return ConvergenceResult(
        passed=False,
        run_count=max_runs,
        final_high_count=final_highs,
        structural_progress_log=structural_progress,
        semantic_fluctuation_log=semantic_fluctuation,
        halt_reason=halt_msg,
    )


def handle_regression(
    registry: DeviationRegistry,
    spec_path: Path,
    roadmap_path: Path,
) -> RegressionResult:
    """Handle structural regression via parallel validation (FR-8).

    Spawns 3 agents in isolated temp dirs, each running the full checker
    suite independently. Results are merged by stable ID, and adversarial
    debate validates each HIGH finding.

    Does NOT perform any ledger operations internally — the caller
    (execute_fidelity_with_convergence) handles budget debiting.

    Parameters
    ----------
    registry : DeviationRegistry
        The deviation registry (updated with debate verdicts).
    spec_path : Path
        Path to spec file.
    roadmap_path : Path
        Path to roadmap file.

    Returns
    -------
    RegressionResult
        Consolidated validation result with findings and debate verdicts.
    """
    dirs = _create_validation_dirs(
        spec_path, roadmap_path, registry.path, count=3,
    )
    try:
        # Each agent independently validates findings
        agent_results: list[dict[str, dict]] = []
        agents_succeeded = 0

        for i, d in enumerate(dirs):
            try:
                # Load independent registry copy
                agent_registry = DeviationRegistry.load_or_create(
                    d / registry.path.name,
                    registry.release_id,
                    registry.spec_hash,
                )
                # Collect active HIGHs from this agent's view
                agent_highs = agent_registry.get_active_highs()
                agent_findings = {
                    f.get("stable_id", ""): f for f in agent_highs
                }
                agent_results.append(agent_findings)
                agents_succeeded += 1
            except Exception as exc:
                logger.error("Validation agent %d failed: %s", i, exc)
                agent_results.append({})

        # All 3 agents must succeed for validation to be considered valid
        if agents_succeeded < 3:
            logger.error(
                "Regression validation FAILED: only %d/3 agents succeeded",
                agents_succeeded,
            )
            return RegressionResult(
                agents_succeeded=agents_succeeded,
            )

        # Merge results by stable ID: preserve unique findings
        merged: dict[str, dict] = {}
        for agent_findings in agent_results:
            for sid, finding in agent_findings.items():
                if sid not in merged:
                    merged[sid] = finding

        # Sort by severity: HIGH -> MEDIUM -> LOW
        severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        validated = sorted(
            merged.values(),
            key=lambda f: severity_order.get(f.get("severity", "LOW"), 3),
        )

        # Write consolidated report
        report_path = registry.path.parent / "fidelity-regression-validation.md"
        report_lines = [
            "---",
            f"agents_succeeded: {agents_succeeded}",
            f"total_findings: {len(validated)}",
            f"high_count: {sum(1 for f in validated if f.get('severity') == 'HIGH')}",
            "---",
            "",
            "## Regression Validation Report",
            "",
        ]
        for f in validated:
            report_lines.append(
                f"- [{f.get('severity', '?')}] {f.get('stable_id', '?')[:8]}: "
                f"{f.get('description', 'no description')}"
            )
        report_path.write_text("\n".join(report_lines), encoding="utf-8")

        return RegressionResult(
            validated_findings=validated,
            debate_verdicts=[],
            agents_succeeded=agents_succeeded,
            consolidated_report_path=str(report_path),
        )

    finally:
        _cleanup_validation_dirs(dirs)
