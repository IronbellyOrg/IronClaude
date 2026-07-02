"""Classifier-backed candidate validation for detection-contract setup."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from superclaude.pr_submit.classifier import STATE_POLLING, classify
from superclaude.pr_submit.detection import DetectionContract

from .candidate import LOCKABLE_RESULTS, CandidateContract
from .evidence import EvidenceBundle

DECLINE_VALIDATION_VALUES = {"passed", "not_exercised", "failed"}


@dataclass(frozen=True)
class CheckResult:
    """One validation check result matching the approved public design."""

    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class ValidationReport:
    """Validation results for a candidate contract and evidence bundle."""

    result: str
    classifier_result: str | None
    expected_result: str
    checks: list[CheckResult]
    negative_controls: list[CheckResult]
    decline_validation: str
    evidence_sha256: str
    validated_surfaces: list[str]
    blockers: list[str]

    def summary(self) -> str:
        """Render safe status and counts only; never include raw payload bodies."""
        failed_checks = [check for check in self.checks if not check.passed]
        failed_controls = [
            check for check in self.negative_controls if not check.passed
        ]
        return "\n".join(
            [
                f"result={self.result}",
                f"classifier_result={self.classifier_result}",
                f"expected_result={self.expected_result}",
                f"checks={len(self.checks)}",
                f"failed_checks={len(failed_checks)}",
                f"negative_controls={len(self.negative_controls)}",
                f"failed_negative_controls={len(failed_controls)}",
                f"evidence_sha256={self.evidence_sha256}",
                f"validated_surfaces={','.join(self.validated_surfaces) or '<none>'}",
                f"decline_validation={self.decline_validation}",
                f"blockers={len(self.blockers)}",
            ]
        )

    @property
    def passed(self) -> bool:
        """Backward-compatible convenience derived from the design result field."""
        return self.result == "passed"


def validate_candidate(
    candidate: CandidateContract,
    evidence: EvidenceBundle,
    *,
    expected_result: str,
) -> ValidationReport:
    """Run structure/evidence/classifier checks without writing artifacts."""
    checks: list[CheckResult] = []
    expected = expected_result or candidate.expected_classifier_result
    checks.append(
        CheckResult(
            "expected_not_polling",
            expected in LOCKABLE_RESULTS,
            "expected classifier result must be clean, findings, or declined",
        )
    )
    checks.extend(_structure_checks(candidate))
    checks.extend(_evidence_checks(evidence))
    checks.extend(_identity_checks(candidate))
    checks.extend(_surface_checks(candidate, evidence))

    classifier_result = classify(evidence.combined_payload, candidate.contract)
    checks.append(
        CheckResult(
            "classifier_matches",
            classifier_result == expected and classifier_result != STATE_POLLING,
            f"classifier returned {classifier_result!r}; expected {expected!r}",
        )
    )
    negative_controls = _negative_control_checks(candidate)

    decline_validation = _decline_validation(expected, classifier_result)
    checks.append(
        CheckResult(
            "decline_validation",
            decline_validation != "failed",
            f"decline_validation: {decline_validation}",
        )
    )
    checks.extend(_freshness_checks(candidate, evidence))

    all_checks = [*checks, *negative_controls]
    blockers = [check.detail for check in all_checks if not check.passed]
    result = "passed" if not blockers else "failed"
    return ValidationReport(
        result=result,
        checks=checks,
        negative_controls=negative_controls,
        classifier_result=classifier_result,
        expected_result=expected,
        evidence_sha256=evidence.sha256,
        validated_surfaces=sorted(evidence.surfaces),
        decline_validation=decline_validation,
        blockers=blockers,
    )


def _decline_validation(expected: str, classifier_result: str) -> str:
    if expected == "declined":
        return "passed" if classifier_result == "declined" else "failed"
    if classifier_result == "declined":
        return "failed"
    return "not_exercised"


def _structure_checks(candidate: CandidateContract) -> list[CheckResult]:
    contract = candidate.contract
    required = {
        "augment_identity": contract.augment_bot_login or contract.augment_app_slug,
        "emission_shape": contract.emission_shape,
        "findings_locus": contract.findings_locus,
        "review_completeness_signal": contract.review_completeness_signal,
        "probe_evidence": contract.probe_evidence,
    }
    checks = [
        CheckResult(
            f"required_{field}",
            value not in (None, "", "<PROBE-LOCKED>"),
            f"required field {field} must be populated",
        )
        for field, value in required.items()
    ]
    checks.append(
        CheckResult(
            "candidate_loads",
            isinstance(
                DetectionContract.from_yaml(_contract_to_yaml_dict(contract)),
                DetectionContract,
            ),
            "candidate loads through DetectionContract.from_yaml",
        )
    )
    return checks


def _evidence_checks(evidence: EvidenceBundle) -> list[CheckResult]:
    return [
        CheckResult(
            "evidence_readable",
            bool(evidence.combined_payload),
            "combined payload exists",
        ),
        CheckResult("evidence_hash", bool(evidence.sha256), "evidence hash recorded"),
        CheckResult("evidence_repo", bool(evidence.repo), "repo recorded"),
        CheckResult(
            "evidence_pr", evidence.pr_number is not None, "PR number recorded"
        ),
        CheckResult(
            "evidence_surfaces", bool(evidence.surfaces), "surfaces inspected recorded"
        ),
        CheckResult(
            "pagination_recorded",
            True,
            f"pagination_complete={evidence.pagination_complete}",
        ),
    ]


def _identity_checks(candidate: CandidateContract) -> list[CheckResult]:
    missing = candidate.required_unobserved()
    return [
        CheckResult(
            "required_observed_provenance",
            not missing,
            f"required unobserved fields: {', '.join(missing) if missing else '<none>'}",
        )
    ]


def _surface_checks(
    candidate: CandidateContract, evidence: EvidenceBundle
) -> list[CheckResult]:
    contract = candidate.contract
    shape_present = (
        (contract.emission_shape == "review" and bool(evidence.reviews))
        or (contract.emission_shape == "issue_comment" and bool(evidence.comments))
        or (contract.emission_shape == "check_run" and bool(evidence.check_runs))
    )
    return [
        CheckResult(
            "surface_present", shape_present, "selected surface exists in payload"
        ),
        CheckResult(
            "findings_locus_recorded",
            bool(contract.findings_locus),
            "findings locus recorded",
        ),
        CheckResult(
            "completion_signal_recorded",
            bool(contract.review_completeness_signal),
            "review completeness signal recorded",
        ),
        CheckResult(
            "severity_path_recorded",
            True,
            "severity path may be null; absence is recorded",
        ),
    ]


def _negative_control_checks(candidate: CandidateContract) -> list[CheckResult]:
    empty = classify({"reviews": [], "comments": []}, candidate.contract)
    non_augment_payload = {
        "reviews": [{"user": {"login": "human-user"}, "body": "finding"}],
        "comments": [{"user": {"login": "human-user"}, "body": "finding"}],
    }
    non_augment = classify(non_augment_payload, candidate.contract)
    return [
        CheckResult(
            "empty_negative_control",
            empty == STATE_POLLING,
            f"empty payload => {empty}",
        ),
        CheckResult(
            "non_augment_negative_control",
            non_augment == STATE_POLLING,
            f"non-Augment payload => {non_augment}",
        ),
    ]


def _freshness_checks(
    candidate: CandidateContract, evidence: EvidenceBundle
) -> list[CheckResult]:
    candidate_repo = candidate.provenance.get("repo")
    repo_matches = bool(candidate_repo and candidate_repo.value == evidence.repo)
    return [
        CheckResult("repo_match", repo_matches, "candidate repo matches evidence repo"),
        CheckResult(
            "evidence_hash_present", bool(evidence.sha256), "evidence hash present"
        ),
        CheckResult(
            "cross_pr_shape_only_blocks_readiness",
            not evidence.cross_pr_shape_only,
            "cross-PR evidence is shape-only and cannot establish current-PR readiness or lockability",
        ),
    ]


def _contract_to_yaml_dict(contract: DetectionContract) -> dict[str, Any]:
    return {
        "augment_bot_login": contract.augment_bot_login,
        "augment_author_association": contract.augment_author_association,
        "augment_app_slug": contract.augment_app_slug,
        "emission_shape": contract.emission_shape,
        "findings_locus": contract.findings_locus,
        "severity_field_path": contract.severity_field_path,
        "review_completeness_signal": contract.review_completeness_signal,
        "probe_evidence": contract.probe_evidence,
        "locked": contract.locked,
    }
