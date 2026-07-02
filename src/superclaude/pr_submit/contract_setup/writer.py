"""Safe report and local-lock writers for detection-contract setup."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

import yaml

from superclaude.pr_submit.detection import _LOCAL_OVERRIDE_REL

from .candidate import CandidateContract
from .evidence import EvidenceBundle
from .lockgate import LockGate
from .validation import ValidationReport


class ContractSetupError(RuntimeError):
    """Base error for detection-contract setup helpers."""


class ContractSetupRefused(ContractSetupError):
    """Raised when a requested lock write fails the safe-lock gate."""


class EvidenceUnreadable(ContractSetupError):
    """Raised when evidence cannot be rendered or written safely."""


def write_report(
    report: ValidationReport, evidence: EvidenceBundle, dest_dir: Path
) -> Path:
    """Write validation report artifacts under a probe directory."""
    root = Path(dest_dir)
    _ensure_report_destination(root)
    root.mkdir(parents=True, exist_ok=True)
    report_path = root / "validation-report.yaml"
    summary_path = root / "validation-summary.md"
    data = {
        "result": report.result,
        "classifier_result": report.classifier_result,
        "expected_result": report.expected_result,
        "evidence_sha256": report.evidence_sha256,
        "repo": evidence.repo,
        "pr_number": evidence.pr_number,
        "captured_at": evidence.captured_at,
        "validated_surfaces": list(report.validated_surfaces),
        "omitted_surfaces": list(evidence.omitted_surfaces),
        "decline_validation": report.decline_validation,
        "cross_pr_shape_only": evidence.cross_pr_shape_only,
        "blockers": list(report.blockers),
        "negative_controls": [
            {
                "name": check.name,
                "passed": check.passed,
                "detail": check.detail,
            }
            for check in report.negative_controls
        ],
        "checks": [
            {
                "name": check.name,
                "passed": check.passed,
                "detail": check.detail,
            }
            for check in report.checks
        ],
    }
    _atomic_write_text(report_path, yaml.safe_dump(data, sort_keys=False))
    _atomic_write_text(summary_path, report.summary() + "\n")
    return report_path


def write_lock(
    candidate: CandidateContract,
    evidence: EvidenceBundle,
    report: ValidationReport,
    *,
    confirmed: bool,
    dest: Path = Path(".dev/pr-monitor/detection-contract.locked.md"),
) -> Path:
    """Write the local locked contract only after confirmation and a passing gate."""
    destination = Path(dest)
    _ensure_lock_destination(destination)
    validation_report_path = evidence.probe_dir / "validation-report.yaml"
    gate = LockGate.evaluate(
        candidate,
        evidence,
        report,
        confirmed=confirmed,
        dest=destination,
        validation_report_path=validation_report_path,
    )
    if not gate.passed:
        failed = ", ".join(failure.name for failure in gate.failures)
        raise ContractSetupRefused(f"safe lock gate failed: {failed}")
    resolved_destination = _active_root_lock_path(destination)
    resolved_destination.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(
        resolved_destination,
        _render_locked_contract(candidate, evidence, report, validation_report_path),
    )
    return resolved_destination


def _ensure_report_destination(dest_dir: Path) -> None:
    resolved = (
        dest_dir.resolve()
        if dest_dir.is_absolute()
        else (Path.cwd() / dest_dir).resolve()
    )
    parts = resolved.parts
    if ".claude" in parts:
        raise ContractSetupRefused(
            "validation reports must not be written under .claude"
        )
    if ".dev" not in parts or "pr-monitor" not in parts or "probes" not in parts:
        raise ContractSetupRefused(
            "validation reports must be written under .dev/pr-monitor/probes"
        )


def _active_root_lock_path(dest: Path) -> Path:
    repo_root = Path.cwd().resolve()
    resolved = dest.resolve() if dest.is_absolute() else (repo_root / dest).resolve()
    expected = (repo_root / _LOCAL_OVERRIDE_REL).resolve()
    if resolved != expected:
        raise ContractSetupRefused(
            "lock destination must be exactly .dev/pr-monitor/detection-contract.locked.md under the active repository root"
        )
    return resolved


def _ensure_lock_destination(dest: Path) -> None:
    resolved = _active_root_lock_path(dest)
    if ".claude" in resolved.parts or "src" in resolved.parts:
        raise ContractSetupRefused(
            "lock destination must not target shipped refs or .claude mirrors"
        )


def _render_locked_contract(
    candidate: CandidateContract,
    evidence: EvidenceBundle,
    report: ValidationReport,
    validation_report: Path,
) -> str:
    contract = candidate.contract
    data: dict[str, Any] = {
        "augment_bot_login": contract.augment_bot_login,
        "augment_author_association": list(contract.augment_author_association),
        "augment_app_slug": contract.augment_app_slug,
        "emission_shape": contract.emission_shape,
        "findings_locus": contract.findings_locus,
        "severity_field_path": contract.severity_field_path,
        "review_completeness_signal": contract.review_completeness_signal,
        "probe_evidence": contract.probe_evidence,
        "decline_phrase_regex": contract.decline_phrase_regex,
        "decline_retrigger_regex": contract.decline_retrigger_regex,
        "accepted_trigger_phrases": list(contract.accepted_trigger_phrases),
        "locked": True,
        "metadata": {
            "schema_version": "1.0",
            "generated_by": "superclaude.pr_submit.contract_setup",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "repo": evidence.repo,
            "pr_number": evidence.pr_number,
            "evidence_sha256": evidence.sha256,
            "validation_report": str(validation_report)
            if validation_report is not None
            else None,
            "validation_result": report.result,
            "validation_classifier_result": report.classifier_result,
            "validated_surfaces": list(report.validated_surfaces),
            "decline_validation": report.decline_validation,
        },
    }
    yaml_block = yaml.safe_dump(data, sort_keys=False)
    return "# Locked detection contract\n\n```yaml\n" + yaml_block + "```\n"


def _atomic_write_text(path: Path, content: str) -> None:
    with NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    temp_path.replace(path)
