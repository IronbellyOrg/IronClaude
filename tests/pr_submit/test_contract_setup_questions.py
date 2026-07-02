"""Setup-question-table and candidate-lockability tests for detection-contract setup.

Covers acceptance area 2 of the research plan
(``TASK-RF-detection-contract-20260701-164700/research/03-validation-tests.md``,
"Candidate derivation and 16 setup questions") and the question sequence in
``merged-requirements.md`` §4 "Proposed Question Sequence With Defaults".

These tests exercise the REAL package surface only:

- ``SETUP_QUESTIONS`` / ``SetupQuestion`` / ``SetupAnswers`` from
  ``superclaude.pr_submit.contract_setup.questions``
- ``derive_candidate`` / ``FieldProvenance`` / ``CandidateContract`` from
  ``superclaude.pr_submit.contract_setup.candidate``
- ``validate_candidate`` from ``superclaude.pr_submit.contract_setup.validation``
- ``EvidenceBundle`` from ``superclaude.pr_submit.contract_setup.evidence``

Evidence is constructed as an in-memory ``EvidenceBundle`` (a frozen dataclass)
so no real ``.dev/pr-monitor/`` artifacts are touched. ``derive_candidate`` only
reads ``evidence.probe_dir`` to compute a probe-evidence path string; we point it
at a pytest ``tmp_path`` so nothing under the repo is written.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from superclaude.pr_submit.contract_setup.candidate import (
    FieldProvenance,
    derive_candidate,
)
from superclaude.pr_submit.contract_setup.evidence import EvidenceBundle
from superclaude.pr_submit.contract_setup.questions import (
    SETUP_QUESTIONS,
    SetupAnswers,
)
from superclaude.pr_submit.contract_setup.validation import validate_candidate

AUGMENT = "augmentcode[bot]"
OTHER_AUGMENT = "augment-code[bot]"

EXPECTED_QUESTION_IDS = [
    "repo",
    "probe_pr",
    "operation",
    "evidence_source",
    "surfaces_to_inspect",
    "detected_augment_identity",
    "author_association_values",
    "emission_shape",
    "findings_locus",
    "severity_field_path",
    "review_completeness_signal",
    "decline_detection_fields",
    "expected_classifier_result",
    "run_validation",
    "write_local_locked_contract",
    "next_step",
]


def _bundle(
    probe_dir: Path,
    *,
    reviews: list[dict[str, Any]] | None = None,
    comments: list[dict[str, Any]] | None = None,
    check_runs: list[dict[str, Any]] | None = None,
    repo: str | None = "IronbellyOrg/IronClaude",
    pr_number: int | None = 42,
) -> EvidenceBundle:
    """Build an in-memory EvidenceBundle mirroring ``load_evidence`` output shape."""
    reviews = reviews or []
    comments = comments or []
    check_runs = check_runs or []
    combined = {
        "reviews": reviews,
        "comments": comments,
        "check_runs": check_runs,
        "metadata": {"repo": repo, "pr_number": pr_number},
    }
    surfaces = [
        name
        for name, payload in (
            ("reviews", reviews),
            ("comments", comments),
            ("check_runs", check_runs),
        )
        if payload
    ]
    return EvidenceBundle(
        probe_dir=probe_dir,
        repo=repo,
        pr_number=pr_number,
        captured_at="2026-07-01T00:00:00+00:00",
        surfaces=sorted(surfaces),
        omitted_surfaces=sorted(
            set(("reviews", "comments", "check_runs")) - set(surfaces)
        ),
        reviews=reviews,
        comments=comments,
        check_runs=check_runs,
        combined_payload=combined,
        sha256="deadbeef" * 8,
        pagination_complete=True,
        cross_pr_shape_only=False,
    )


def _augment_review(*, findings: bool, login: str = AUGMENT) -> dict[str, Any]:
    return {
        "author": {"login": login},
        "state": "COMMENTED",
        "submitted_at": "2026-07-01T00:00:00Z",
        "has_findings": findings,
        "body": "finding: something needs fixing" if findings else "",
    }


# --- 1. The 16-question table -------------------------------------------------


def test_setup_question_sequence_contains_all_16_questions_in_order():
    """SETUP_QUESTIONS has exactly the 16 acceptance IDs, in the acceptance order.

    The stable question ID lives on ``SetupQuestion.id`` (questions.py:40).
    """
    assert [question.id for question in SETUP_QUESTIONS] == EXPECTED_QUESTION_IDS
    assert len(SETUP_QUESTIONS) == 16
    # IDs are unique — no accidental duplicate collapsing two questions into one.
    assert len({question.id for question in SETUP_QUESTIONS}) == 16


# --- 2. Defaults are suggestions only, never lock values ----------------------


def test_setup_defaults_are_suggestions_not_lock_values_without_evidence(tmp_path):
    """A bare default (no observed evidence) can NEVER mark a required field observed.

    With an empty payload, every must-never-guess field derives from a *default
    suggestion* whose ``FieldProvenance.observed`` is False, so
    ``required_unobserved()`` reports them and the candidate cannot lock.
    """
    evidence = _bundle(tmp_path, repo="IronbellyOrg/IronClaude")
    # Defaults supplied as answers are still only *suggestions* — they must not
    # promote an unobserved field to observed.
    answers = SetupAnswers(
        repo="IronbellyOrg/IronClaude",
        emission_shape="review",
        findings_locus="reviews[].body",
        review_completeness_signal="reviews[].state",
    )
    candidate = derive_candidate(evidence, answers=answers)

    missing = candidate.required_unobserved()
    # Identity, emission_shape, findings_locus, review_completeness_signal are all
    # required-to-observe and, with an empty payload, none are observed.
    for required_field in (
        "augment_identity",
        "emission_shape",
        "findings_locus",
        "review_completeness_signal",
    ):
        assert required_field in missing, (missing, required_field)

    # Each of those provenance entries is a suggestion, not observed.
    for prov_key in ("emission_shape", "findings_locus", "review_completeness_signal"):
        prov = candidate.provenance[prov_key]
        assert isinstance(prov, FieldProvenance)
        assert prov.observed is False, (prov_key, prov)

    # The validation report therefore fails (cannot lock from suggestions).
    report = validate_candidate(candidate, evidence, expected_result="findings")
    assert report.result == "failed"
    assert report.blockers  # non-empty blocker list


# --- 3. Multiple observed identities require explicit selection ---------------


def test_multiple_augment_identity_candidates_require_explicit_selection(tmp_path):
    """>1 observed Augment identity + no explicit answer → identity left unselected.

    ``_selected_identity`` only auto-selects when exactly one login is observed;
    with two it emits a default-suggested (unobserved) provenance and no value.
    """
    evidence = _bundle(
        tmp_path,
        reviews=[
            _augment_review(findings=True, login=AUGMENT),
            _augment_review(findings=True, login=OTHER_AUGMENT),
        ],
    )
    candidate = derive_candidate(evidence, answers=SetupAnswers())

    bot_prov = candidate.provenance["augment_bot_login"]
    assert bot_prov.value is None
    assert bot_prov.observed is False
    # Identity counts as unobserved for lockability.
    assert "augment_identity" in candidate.required_unobserved()

    # An explicit selection of an observed login resolves it (observed=True).
    chosen = derive_candidate(
        evidence, answers=SetupAnswers(detected_augment_identity=AUGMENT)
    )
    chosen_prov = chosen.provenance["augment_bot_login"]
    assert chosen_prov.value == AUGMENT
    assert chosen_prov.observed is True
    assert "augment_identity" not in chosen.required_unobserved()


# --- 4. Unobserved emission shape / polling result cannot lock ----------------


def test_unobserved_emission_shape_cannot_be_locked(tmp_path):
    """Selecting an emission shape absent from the payload cannot lock.

    Evidence has only reviews; answering ``check_run`` yields an unobserved
    emission-shape provenance and a failing validation report (surface_present
    and required_observed_provenance both fail).
    """
    evidence = _bundle(
        tmp_path,
        reviews=[_augment_review(findings=True)],
    )
    candidate = derive_candidate(
        evidence,
        answers=SetupAnswers(
            detected_augment_identity=AUGMENT,
            emission_shape="check_run",  # not present in the payload
        ),
    )
    shape_prov = candidate.provenance["emission_shape"]
    assert shape_prov.value == "check_run"
    assert shape_prov.observed is False
    assert "emission_shape" in candidate.required_unobserved()

    report = validate_candidate(candidate, evidence, expected_result="findings")
    assert report.result == "failed"
    # The unobserved surface is a blocker.
    assert any(
        "surface" in blocker or "unobserved" in blocker for blocker in report.blockers
    )


def test_polling_expected_result_is_never_lockable(tmp_path):
    """``expected_classifier_result == "polling"`` can never lock.

    A payload with no Augment activity derives ``expected == "polling"``; the
    ``expected_not_polling`` check fails, so the report result is "failed".
    """
    evidence = _bundle(tmp_path)  # empty payload → derived expected == polling
    candidate = derive_candidate(evidence, answers=SetupAnswers())
    assert candidate.expected_classifier_result == "polling"
    assert "expected_classifier_result" in candidate.required_unobserved()

    report = validate_candidate(
        candidate, evidence, expected_result=candidate.expected_classifier_result
    )
    assert report.result == "failed"
    assert any(
        "polling" in blocker or "clean, findings, or declined" in blocker
        for blocker in report.blockers
    )


# --- 5. Missing decline evidence records decline_validation: not_exercised ----


def test_missing_decline_evidence_records_not_exercised(tmp_path):
    """No decline sample → ``decline_validation == "not_exercised"`` (a warning, not failed).

    Findings-only evidence classifies as "findings"; since neither expected nor
    classifier result is "declined", ``_decline_validation`` returns
    ``not_exercised`` — recorded on the report, and the decline check does not
    fail (only "failed" fails).
    """
    evidence = _bundle(
        tmp_path,
        reviews=[_augment_review(findings=True, login=AUGMENT)],
    )
    candidate = derive_candidate(
        evidence, answers=SetupAnswers(detected_augment_identity=AUGMENT)
    )
    report = validate_candidate(candidate, evidence, expected_result="findings")

    assert report.decline_validation == "not_exercised"
    # not_exercised is not a lock blocker on the decline axis.
    decline_checks = [c for c in report.checks if c.name == "decline_validation"]
    assert decline_checks and decline_checks[0].passed is True
    assert "not_exercised" in report.summary()
