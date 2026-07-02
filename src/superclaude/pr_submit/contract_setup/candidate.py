"""Candidate detection-contract derivation with field provenance."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from superclaude.pr_submit.detection import DetectionContract

from .evidence import EvidenceBundle
from .questions import SetupAnswers

PROVENANCE_OBSERVED = "observed"
PROVENANCE_DEFAULT_SUGGESTED = "default_suggested"
PROVENANCE_USER = "user"

MUST_OBSERVE_FIELDS = {
    "augment_identity",
    "emission_shape",
    "findings_locus",
    "review_completeness_signal",
    "probe_evidence",
    "repo",
}
LOCKABLE_RESULTS = {"clean", "findings", "declined"}


@dataclass(frozen=True)
class FieldProvenance:
    """Value provenance for a candidate contract field."""

    value: object
    source: str
    observed: bool
    evidence_ref: str | None = None


@dataclass(frozen=True)
class CandidateContract:
    """Candidate detection contract plus evidence provenance."""

    contract: DetectionContract
    provenance: dict[str, FieldProvenance]
    expected_classifier_result: str

    def required_unobserved(self) -> list[str]:
        """Return must-never-guess fields without observed provenance."""
        missing: list[str] = []
        for field in sorted(MUST_OBSERVE_FIELDS - {"augment_identity"}):
            provenance = self.provenance.get(field)
            if provenance is None or not provenance.observed:
                missing.append(field)
        bot = self.provenance.get("augment_bot_login")
        app = self.provenance.get("augment_app_slug")
        if not ((bot and bot.observed) or (app and app.observed)):
            missing.append("augment_identity")
        if self.expected_classifier_result not in LOCKABLE_RESULTS:
            missing.append("expected_classifier_result")
        return missing


def derive_candidate(
    evidence: EvidenceBundle, *, answers: SetupAnswers | None = None
) -> CandidateContract:
    """Derive a candidate contract from captured evidence and optional answers."""
    answers = answers or SetupAnswers()
    provenance: dict[str, FieldProvenance] = {}

    identity = _selected_identity(evidence, answers, provenance)
    app_slug = _selected_app_slug(evidence, answers, provenance)
    author_association = tuple(
        answers.author_association_values
    ) or _observed_associations(evidence)
    provenance["augment_author_association"] = FieldProvenance(
        list(author_association),
        PROVENANCE_OBSERVED if author_association else PROVENANCE_DEFAULT_SUGGESTED,
        bool(author_association),
        "payload.author_association" if author_association else None,
    )

    emission_shape = _emission_shape(evidence, answers, provenance)
    findings_locus = _findings_locus(evidence, answers, provenance)
    severity_field_path = answers.severity_field_path or _observed_severity_path(
        evidence
    )
    provenance["severity_field_path"] = FieldProvenance(
        severity_field_path,
        PROVENANCE_OBSERVED if severity_field_path else PROVENANCE_DEFAULT_SUGGESTED,
        bool(severity_field_path),
        "payload.severity" if severity_field_path else None,
    )
    review_signal = _review_completeness_signal(evidence, answers, provenance)

    evidence_path = _evidence_path(evidence)
    provenance["probe_evidence"] = FieldProvenance(
        str(evidence_path), PROVENANCE_OBSERVED, True, str(evidence_path)
    )
    provenance["repo"] = FieldProvenance(
        evidence.repo,
        PROVENANCE_OBSERVED if evidence.repo else PROVENANCE_DEFAULT_SUGGESTED,
        bool(evidence.repo),
        "metadata.repo" if evidence.repo else None,
    )

    expected = answers.expected_classifier_result or _expected_result(evidence)
    provenance["expected_classifier_result"] = FieldProvenance(
        expected,
        PROVENANCE_OBSERVED
        if expected in LOCKABLE_RESULTS
        else PROVENANCE_DEFAULT_SUGGESTED,
        expected in LOCKABLE_RESULTS,
        "payload.classifier-shape" if expected in LOCKABLE_RESULTS else None,
    )

    contract = DetectionContract(
        augment_bot_login=identity,
        augment_author_association=list(author_association),
        augment_app_slug=app_slug,
        emission_shape=emission_shape,
        findings_locus=findings_locus,
        severity_field_path=severity_field_path,
        review_completeness_signal=review_signal,
        probe_evidence=str(evidence_path),
        locked=True,
    )
    return CandidateContract(
        contract=contract,
        provenance=provenance,
        expected_classifier_result=expected,
    )


def _selected_identity(
    evidence: EvidenceBundle,
    answers: SetupAnswers,
    provenance: dict[str, FieldProvenance],
) -> str | None:
    observed = sorted(_observed_logins(evidence))
    if answers.detected_augment_identity:
        selected = answers.detected_augment_identity
        provenance["augment_bot_login"] = FieldProvenance(
            selected,
            PROVENANCE_USER,
            selected in observed,
            "payload.user.login" if selected in observed else None,
        )
        return selected
    if len(observed) == 1:
        selected = observed[0]
        provenance["augment_bot_login"] = FieldProvenance(
            selected, PROVENANCE_OBSERVED, True, "payload.user.login"
        )
        return selected
    provenance["augment_bot_login"] = FieldProvenance(
        None, PROVENANCE_DEFAULT_SUGGESTED, False, None
    )
    return None


def _selected_app_slug(
    evidence: EvidenceBundle,
    answers: SetupAnswers,
    provenance: dict[str, FieldProvenance],
) -> str | None:
    observed = sorted(_observed_app_slugs(evidence))
    answer = answers.decline_detection_fields.get("augment_app_slug")
    if isinstance(answer, str) and answer:
        provenance["augment_app_slug"] = FieldProvenance(
            answer,
            PROVENANCE_USER,
            answer in observed,
            "payload.app.slug" if answer in observed else None,
        )
        return answer
    if len(observed) == 1:
        selected = observed[0]
        provenance["augment_app_slug"] = FieldProvenance(
            selected, PROVENANCE_OBSERVED, True, "payload.app.slug"
        )
        return selected
    provenance["augment_app_slug"] = FieldProvenance(
        None, PROVENANCE_DEFAULT_SUGGESTED, False, None
    )
    return None


def _observed_logins(evidence: EvidenceBundle) -> set[str]:
    logins: set[str] = set()
    for entry in [*evidence.reviews, *evidence.comments]:
        login = _nested_str(entry, "user", "login") or _nested_str(
            entry, "author", "login"
        )
        if login and _looks_like_augment(login):
            logins.add(login)
    return logins


def _observed_app_slugs(evidence: EvidenceBundle) -> set[str]:
    slugs: set[str] = set()
    for entry in [*evidence.reviews, *evidence.comments, *evidence.check_runs]:
        slug = _nested_str(entry, "app", "slug") or _nested_str(
            entry, "author", "app", "slug"
        )
        if slug and _looks_like_augment(slug):
            slugs.add(slug)
    return slugs


def _observed_associations(evidence: EvidenceBundle) -> tuple[str, ...]:
    values = set()
    for entry in [*evidence.reviews, *evidence.comments]:
        value = entry.get("author_association")
        if isinstance(value, str) and value:
            values.add(value)
    return tuple(sorted(values))


def _emission_shape(
    evidence: EvidenceBundle,
    answers: SetupAnswers,
    provenance: dict[str, FieldProvenance],
) -> str | None:
    if answers.emission_shape:
        observed = _shape_observed(evidence, answers.emission_shape)
        provenance["emission_shape"] = FieldProvenance(
            answers.emission_shape,
            PROVENANCE_USER,
            observed,
            f"payload.{answers.emission_shape}" if observed else None,
        )
        return answers.emission_shape
    for shape, present in (
        ("review", bool(evidence.reviews)),
        ("issue_comment", bool(evidence.comments)),
        ("check_run", bool(evidence.check_runs)),
    ):
        if present:
            provenance["emission_shape"] = FieldProvenance(
                shape, PROVENANCE_OBSERVED, True, f"payload.{shape}"
            )
            return shape
    provenance["emission_shape"] = FieldProvenance(
        None, PROVENANCE_DEFAULT_SUGGESTED, False, None
    )
    return None


def _findings_locus(
    evidence: EvidenceBundle,
    answers: SetupAnswers,
    provenance: dict[str, FieldProvenance],
) -> str | None:
    if answers.findings_locus:
        observed = _path_resolves(evidence.combined_payload, answers.findings_locus)
        provenance["findings_locus"] = FieldProvenance(
            answers.findings_locus,
            PROVENANCE_USER,
            observed,
            answers.findings_locus if observed else None,
        )
        return answers.findings_locus
    for path in ("reviews[].body", "comments[].body", "check_runs[].output"):
        if _path_resolves(evidence.combined_payload, path):
            provenance["findings_locus"] = FieldProvenance(
                path, PROVENANCE_OBSERVED, True, path
            )
            return path
    provenance["findings_locus"] = FieldProvenance(
        None, PROVENANCE_DEFAULT_SUGGESTED, False, None
    )
    return None


def _observed_severity_path(evidence: EvidenceBundle) -> str | None:
    for path in (
        "reviews[].severity",
        "comments[].severity",
        "check_runs[].conclusion",
    ):
        if _path_resolves(evidence.combined_payload, path):
            return path
    return None


def _review_completeness_signal(
    evidence: EvidenceBundle,
    answers: SetupAnswers,
    provenance: dict[str, FieldProvenance],
) -> str | None:
    if answers.review_completeness_signal:
        provenance["review_completeness_signal"] = FieldProvenance(
            answers.review_completeness_signal,
            PROVENANCE_USER,
            _path_resolves(
                evidence.combined_payload, answers.review_completeness_signal
            ),
            answers.review_completeness_signal,
        )
        return answers.review_completeness_signal
    for path in (
        "reviews[].state",
        "reviews[].submitted_at",
        "comments[].created_at",
        "check_runs[].conclusion",
    ):
        if _path_resolves(evidence.combined_payload, path):
            provenance["review_completeness_signal"] = FieldProvenance(
                path, PROVENANCE_OBSERVED, True, path
            )
            return path
    provenance["review_completeness_signal"] = FieldProvenance(
        None, PROVENANCE_DEFAULT_SUGGESTED, False, None
    )
    return None


def _expected_result(evidence: EvidenceBundle) -> str:
    if _has_augmented_body(evidence, "abnormally large"):
        return "declined"
    if _has_augmented_body(evidence, "finding") or _has_augmented_body(
        evidence, "issue"
    ):
        return "findings"
    if _observed_logins(evidence) or _observed_app_slugs(evidence):
        return "clean"
    return "polling"


def _evidence_path(evidence: EvidenceBundle) -> Path:
    combined = evidence.probe_dir / "combined-payload.json"
    return combined if combined.exists() else evidence.probe_dir


def _has_augmented_body(evidence: EvidenceBundle, needle: str) -> bool:
    lowered = needle.lower()
    for entry in [*evidence.reviews, *evidence.comments]:
        body = entry.get("body")
        if isinstance(body, str) and lowered in body.lower():
            login = _nested_str(entry, "user", "login") or _nested_str(
                entry, "author", "login"
            )
            if login is None or _looks_like_augment(login):
                return True
    return False


def _shape_observed(evidence: EvidenceBundle, shape: str) -> bool:
    return (
        (shape == "review" and bool(evidence.reviews))
        or (shape == "issue_comment" and bool(evidence.comments))
        or (shape == "check_run" and bool(evidence.check_runs))
    )


def _path_resolves(payload: dict[str, Any], path: str | None) -> bool:
    if not path:
        return False
    normalized = path.replace("[]", "")
    current: Any = payload
    for part in normalized.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list):
            current = [item.get(part) for item in current if isinstance(item, dict)]
        else:
            return False
        if current in (None, []):
            return False
    return True


def _nested_str(data: dict[str, Any], *keys: str) -> str | None:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current if isinstance(current, str) and current else None


def _looks_like_augment(value: str) -> bool:
    lowered = value.lower()
    return "augment" in lowered or "auggie" in lowered
