"""Pure safe-locking gate for detection-contract setup."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from superclaude.pr_submit.classifier import STATE_POLLING
from superclaude.pr_submit.detection import _LOCAL_OVERRIDE_REL

from .candidate import CandidateContract
from .evidence import EvidenceBundle
from .validation import CheckResult, ValidationReport


@dataclass(frozen=True)
class GateResult:
    """Result of evaluating all safe-lock predicates."""

    passed: bool
    failures: list[CheckResult]


class LockGate:
    """Evaluate the 12 ordered safe-locking predicates without side effects."""

    CHECK_IDS = (
        "evidence_readable",
        "evidence_repo_bound",
        "pr_identity_recorded",
        "identity_observed",
        "emission_shape_observed",
        "paths_resolve",
        "expected_not_polling",
        "classifier_matches",
        "negative_controls_pass",
        "report_written",
        "user_confirmed",
        "dest_under_pr_monitor",
    )

    @staticmethod
    def evaluate(
        candidate: CandidateContract,
        evidence: EvidenceBundle,
        report: ValidationReport,
        *,
        confirmed: bool,
        dest: Path,
        validation_report_path: Path | None = None,
    ) -> GateResult:
        """Return pass/fail plus every failed safe-lock predicate."""
        checks = (
            _evidence_readable(evidence),
            _evidence_repo_bound(candidate, evidence),
            _pr_identity_recorded(evidence),
            _identity_observed(candidate),
            _emission_shape_observed(candidate),
            _paths_resolve(candidate),
            _expected_not_polling(candidate),
            _classifier_matches(report),
            _negative_controls_pass(report),
            _report_written(report, validation_report_path),
            _user_confirmed(confirmed),
            _dest_under_pr_monitor(Path(dest)),
        )
        failures = [check for check in checks if not check.passed]
        return GateResult(passed=not failures, failures=failures)


def _check(name: str, passed: bool, detail: str) -> CheckResult:
    return CheckResult(name=name, passed=passed, detail=detail)


def _evidence_readable(evidence: EvidenceBundle) -> CheckResult:
    return _check(
        "evidence_readable", bool(evidence.combined_payload), "Evidence payload loaded."
    )


def _evidence_repo_bound(
    candidate: CandidateContract, evidence: EvidenceBundle
) -> CheckResult:
    repo = candidate.provenance.get("repo")
    return _check(
        "evidence_repo_bound",
        bool(repo and repo.value and repo.value == evidence.repo),
        "Evidence repo matches candidate repo.",
    )


def _pr_identity_recorded(evidence: EvidenceBundle) -> CheckResult:
    return _check(
        "pr_identity_recorded",
        evidence.pr_number is not None and not evidence.cross_pr_shape_only,
        "Evidence PR identity is recorded for the current PR; cross-PR evidence is shape-only.",
    )


def _identity_observed(candidate: CandidateContract) -> CheckResult:
    bot = candidate.provenance.get("augment_bot_login")
    app = candidate.provenance.get("augment_app_slug")
    return _check(
        "identity_observed",
        bool((bot and bot.observed) or (app and app.observed)),
        "Augment bot/app identity is observed in payload metadata.",
    )


def _emission_shape_observed(candidate: CandidateContract) -> CheckResult:
    provenance = candidate.provenance.get("emission_shape")
    return _check(
        "emission_shape_observed",
        bool(provenance and provenance.observed),
        "Emission shape is observed in payload.",
    )


def _paths_resolve(candidate: CandidateContract) -> CheckResult:
    findings = candidate.provenance.get("findings_locus")
    signal = candidate.provenance.get("review_completeness_signal")
    return _check(
        "paths_resolve",
        bool(findings and findings.observed and signal and signal.observed),
        "Findings locus and completion signal resolve against evidence.",
    )


def _expected_not_polling(candidate: CandidateContract) -> CheckResult:
    return _check(
        "expected_not_polling",
        candidate.expected_classifier_result in {"clean", "findings", "declined"},
        "Expected classifier result is lockable and not polling.",
    )


def _classifier_matches(report: ValidationReport) -> CheckResult:
    return _check(
        "classifier_matches",
        report.classifier_result == report.expected_result
        and report.classifier_result != STATE_POLLING,
        "Validation classifier result matches expected non-polling result.",
    )


def _negative_controls_pass(report: ValidationReport) -> CheckResult:
    controls = {
        check.name: check.passed
        for check in report.negative_controls
        if check.name in {"empty_negative_control", "non_augment_negative_control"}
    }
    return _check(
        "negative_controls_pass",
        controls.get("empty_negative_control") is True
        and controls.get("non_augment_negative_control") is True,
        "Empty and non-Augment negative controls stay polling.",
    )


def _report_written(
    report: ValidationReport, validation_report_path: Path | None
) -> CheckResult:
    passed = False
    if (
        validation_report_path is not None
        and validation_report_path.exists()
        and validation_report_path.is_file()
        and report.evidence_sha256
    ):
        try:
            text = validation_report_path.read_text(encoding="utf-8")
        except OSError:
            text = ""
        passed = report.evidence_sha256 in text and report.result == "passed"
    return _check(
        "report_written",
        passed,
        "Validation report file exists and references the matching evidence hash.",
    )


def _user_confirmed(confirmed: bool) -> CheckResult:
    return _check(
        "user_confirmed", confirmed is True, "User explicitly confirmed lock write."
    )


def _dest_under_pr_monitor(dest: Path) -> CheckResult:
    repo_root = Path.cwd().resolve()
    resolved = dest.resolve() if dest.is_absolute() else (repo_root / dest).resolve()
    expected = (repo_root / _LOCAL_OVERRIDE_REL).resolve()
    forbidden = ".claude" in resolved.parts or "src" in resolved.parts
    return _check(
        "dest_under_pr_monitor",
        resolved == expected and not forbidden,
        "Destination is exactly .dev/pr-monitor/detection-contract.locked.md under the active repository root.",
    )
