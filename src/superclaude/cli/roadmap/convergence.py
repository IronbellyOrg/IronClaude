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
        """
        if path.exists():
            try:
                data = json.loads(path.read_text())
                if data.get("spec_hash") == spec_hash:
                    return cls(
                        path=path,
                        release_id=release_id,
                        spec_hash=spec_hash,
                        runs=data.get("runs", []),
                        findings=data.get("findings", {}),
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
