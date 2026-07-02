"""Declarative setup question table for detection-contract setup."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

if False:  # pragma: no cover - typing-only import without runtime dependency cycle.
    from .evidence import EvidenceBundle

DefaultDeriver = Callable[["EvidenceBundle | None", "SetupAnswers"], object | None]


@dataclass(frozen=True)
class SetupAnswers:
    """Resolved operator answers for the setup sequence."""

    repo: str | None = None
    probe_pr: int | None = None
    operation: str | None = None
    evidence_source: str | None = None
    surfaces_to_inspect: tuple[str, ...] = ()
    detected_augment_identity: str | None = None
    # Optional operator override for the Augment app slug, selected alongside the
    # bot identity (part of the `detected_augment_identity` question, not a 17th
    # question). A dedicated field so the app slug is not tunnelled through the
    # unrelated `decline_detection_fields` bucket.
    augment_app_slug: str | None = None
    author_association_values: tuple[str, ...] = ()
    emission_shape: str | None = None
    findings_locus: str | None = None
    severity_field_path: str | None = None
    review_completeness_signal: str | None = None
    decline_detection_fields: dict[str, Any] = field(default_factory=dict)
    expected_classifier_result: str | None = None
    run_validation: bool | None = None
    write_local_locked_contract: bool | None = None
    next_step: bool | None = None


@dataclass(frozen=True)
class SetupQuestion:
    """One declarative setup question and its lockability metadata."""

    id: str
    prompt: str
    derive_default: DefaultDeriver
    required_for_lock: bool = False
    lockable_only_if_observed: bool = False


def _answer_default(attr: str) -> DefaultDeriver:
    def derive(
        _evidence: EvidenceBundle | None, answers: SetupAnswers
    ) -> object | None:
        value = getattr(answers, attr)
        if value in ((), {}, None):
            return None
        return value

    return derive


def _evidence_attr(attr: str, answer_attr: str | None = None) -> DefaultDeriver:
    # The operator answer and the evidence field may have different names (e.g. the
    # `probe_pr` answer vs the `pr_number` evidence field). Read the answer under
    # `answer_attr` (defaults to `attr`), else fall back to the evidence field.
    answer_key = answer_attr or attr

    def derive(evidence: EvidenceBundle | None, answers: SetupAnswers) -> object | None:
        answered = getattr(answers, answer_key, None)
        if answered not in ((), {}, None):
            return answered
        return getattr(evidence, attr, None) if evidence is not None else None

    return derive


def _surfaces_default(
    evidence: EvidenceBundle | None, answers: SetupAnswers
) -> object | None:
    if answers.surfaces_to_inspect:
        return answers.surfaces_to_inspect
    if evidence is not None and evidence.surfaces:
        return tuple(evidence.surfaces)
    return ("reviews", "comments", "check_runs")


def _operation_default(
    _evidence: EvidenceBundle | None, answers: SetupAnswers
) -> object | None:
    return answers.operation or "diagnose"


def _evidence_source_default(
    _evidence: EvidenceBundle | None, answers: SetupAnswers
) -> object | None:
    return answers.evidence_source or "existing-captured-json"


def _run_validation_default(
    _evidence: EvidenceBundle | None, answers: SetupAnswers
) -> object | None:
    return True if answers.run_validation is None else answers.run_validation


def _write_lock_default(
    _evidence: EvidenceBundle | None, answers: SetupAnswers
) -> object | None:
    return (
        False
        if answers.write_local_locked_contract is None
        else answers.write_local_locked_contract
    )


def _next_step_default(
    _evidence: EvidenceBundle | None, answers: SetupAnswers
) -> object | None:
    return True if answers.next_step is None else answers.next_step


def _none_default(
    _evidence: EvidenceBundle | None, _answers: SetupAnswers
) -> object | None:
    return None


SETUP_QUESTIONS: list[SetupQuestion] = [
    SetupQuestion(
        "repo", "Use resolved repo `<owner/repo>`?", _evidence_attr("repo"), True, True
    ),
    SetupQuestion(
        "probe_pr",
        "Which PR contains a recent Augment-authored payload?",
        _evidence_attr("pr_number", answer_attr="probe_pr"),
        True,
        True,
    ),
    SetupQuestion(
        "operation",
        "Diagnose only, validate existing evidence, or capture/validate/offer write?",
        _operation_default,
    ),
    SetupQuestion(
        "evidence_source",
        "Fetch current GitHub payloads or use existing captured JSON?",
        _evidence_source_default,
    ),
    SetupQuestion(
        "surfaces_to_inspect",
        "PR reviews, issue comments, check runs, or all?",
        _surfaces_default,
    ),
    SetupQuestion(
        "detected_augment_identity",
        "Lock this observed bot/app identity?",
        _answer_default("detected_augment_identity"),
        True,
        True,
    ),
    SetupQuestion(
        "author_association_values",
        "Use these observed author associations?",
        _answer_default("author_association_values"),
    ),
    SetupQuestion(
        "emission_shape",
        "Which observed surface is primary?",
        _answer_default("emission_shape"),
        True,
        True,
    ),
    SetupQuestion(
        "findings_locus",
        "Use this observed field path?",
        _answer_default("findings_locus"),
        True,
        True,
    ),
    SetupQuestion(
        "severity_field_path",
        "Use this observed severity path or `null`?",
        _answer_default("severity_field_path"),
    ),
    SetupQuestion(
        "review_completeness_signal",
        "What observed signal means review is complete?",
        _answer_default("review_completeness_signal"),
        True,
        True,
    ),
    SetupQuestion(
        "decline_detection_fields",
        "Use existing decline defaults and validate if evidence exists?",
        _answer_default("decline_detection_fields"),
    ),
    SetupQuestion(
        "expected_classifier_result",
        "What should the captured payload classify as?",
        _answer_default("expected_classifier_result"),
        True,
    ),
    SetupQuestion(
        "run_validation",
        "Dry-run existing classifier against captured payload and candidate?",
        _run_validation_default,
        True,
    ),
    SetupQuestion(
        "write_local_locked_contract",
        "Write `.dev/pr-monitor/detection-contract.locked.md`?",
        _write_lock_default,
    ),
    SetupQuestion("next_step", "Print rerun command?", _next_step_default),
]
