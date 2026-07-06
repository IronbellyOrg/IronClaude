"""FX5 regression backstop: negative + differential (mutation-must-fail) pairs.

Locks the F4 correctness-bug class and its neighbours. For every gate-load-bearing
helper in the enforced registry (see
``.dev/tasks/.../phase-outputs/discovery/fx5-gate-helper-registry.md``) this module
authors BOTH:

* a NEGATIVE test — degenerate/all-None/absent-key input asserts the safe
  "not resolved / blocker / missing / gate fails" outcome; and
* a DIFFERENTIAL test — a naive/mutated implementation is installed (monkeypatch of
  the helper or its dependency) and a downstream observation is shown to FLIP to the
  buggy value, proving the mutation is DETECTED. A mere "negative test exists"
  checkmark is insufficient (research/02 §5): the differential proves a real
  regression cannot pass silently.

``HELPER_TEST_MAP`` (module level) records, per dotted helper name, the ``negative``
and ``differential`` test function names in THIS file. It IS the enforced registry —
the FX5 collector in ``conftest.py`` imports it and asserts
``GATE_LOAD_BEARING_HELPERS == HELPER_TEST_MAP.keys()``. Every enforced helper carries
both kinds; no helper is omitted and none is left with only one kind.

All tests are authored to PASS green against the current (already-F4-fixed) tree and
reference only real symbols. Marker-free (``--strict-markers`` active).
"""

from __future__ import annotations

from pathlib import Path

from superclaude.pr_submit.classifier import STATE_POLLING
from superclaude.pr_submit.contract_setup import candidate as candidate_mod
from superclaude.pr_submit.contract_setup import diagnosis as diagnosis_mod
from superclaude.pr_submit.contract_setup import lockgate as lockgate_mod
from superclaude.pr_submit.contract_setup import validation as validation_mod
from superclaude.pr_submit.contract_setup.candidate import (
    PROVENANCE_OBSERVED,
    FieldProvenance,
    derive_candidate,
)
from superclaude.pr_submit.contract_setup.evidence import EvidenceBundle
from superclaude.pr_submit.contract_setup.questions import SetupAnswers

# ---------------------------------------------------------------------------
# HELPER_TEST_MAP — the enforced registry (dotted helper -> negative/differential
# test names). Steps 2.5 (this block) + 2.6 (freshness/anti-gaming) together cover
# all 11 enforced helpers. conftest.GATE_LOAD_BEARING_HELPERS must equal its keys.
# ---------------------------------------------------------------------------
HELPER_TEST_MAP: dict[str, dict[str, str]] = {
    "candidate._path_resolves": {
        "negative": "test_path_resolves_all_none_list_is_not_resolved",
        "differential": "test_path_resolves_differential_naive_all_none_flips_findings_observed",
    },
    "candidate._findings_locus": {
        "negative": "test_findings_locus_all_none_not_observed",
        "differential": "test_findings_locus_differential_always_observed_flips_required_unobserved",
    },
    "candidate._review_completeness_signal": {
        "negative": "test_review_completeness_signal_all_none_not_observed",
        "differential": "test_review_completeness_signal_differential_always_observed_flips_required_unobserved",
    },
    "candidate._selected_identity": {
        "negative": "test_selected_identity_no_augment_not_observed",
        "differential": "test_selected_identity_differential_always_observed_flips_required_unobserved",
    },
    "candidate._selected_app_slug": {
        "negative": "test_selected_app_slug_no_augment_not_observed",
        "differential": "test_selected_app_slug_differential_always_observed_flips_required_unobserved",
    },
    "lockgate._paths_resolve": {
        "negative": "test_paths_resolve_unobserved_locus_fails_gate",
        "differential": "test_paths_resolve_differential_presence_not_observation_flips_gate",
    },
    "lockgate._emission_shape_observed": {
        "negative": "test_emission_shape_observed_unobserved_fails_gate",
        "differential": "test_emission_shape_observed_differential_presence_not_observation_flips_gate",
    },
    "diagnosis._resolve_optional_path": {
        "negative": "test_resolve_optional_path_none_and_empty_return_none",
        "differential": "test_resolve_optional_path_differential_dropping_guard_flips_empty",
    },
    "candidate.CandidateContract.required_unobserved": {
        "negative": "test_required_unobserved_lists_unobserved_findings_locus",
        "differential": "test_required_unobserved_differential_skipping_field_flips_membership",
    },
    # --- Step 2.6: freshness gate + anti-gaming controls -----------------------
    "diagnosis._stale_blockers": {
        "negative": "test_stale_blockers_empty_report_no_blockers",
        "differential": "test_stale_blockers_differential_dropping_hash_check_flips_mismatch",
    },
    "validation._negative_control_checks": {
        "negative": "test_negative_control_checks_flags_permissive_empty_classification",
        "differential": "test_negative_control_checks_differential_constant_true_flips",
    },
}


# ---------------------------------------------------------------------------
# Builders — construct real EvidenceBundle / CandidateContract without touching disk.
# ---------------------------------------------------------------------------
def _evidence(
    *,
    reviews: list[dict] | None = None,
    comments: list[dict] | None = None,
    check_runs: list[dict] | None = None,
    combined_payload: dict | None = None,
    repo: str = "IronbellyOrg/IronClaude",
    pr_number: int = 42,
    sha256: str = "deadbeefdeadbeef",
) -> EvidenceBundle:
    reviews = reviews or []
    comments = comments or []
    check_runs = check_runs or []
    if combined_payload is None:
        combined_payload = {
            "reviews": reviews,
            "comments": comments,
            "check_runs": check_runs,
        }
    return EvidenceBundle(
        probe_dir=Path("/nonexistent/probe"),
        repo=repo,
        pr_number=pr_number,
        captured_at="2026-07-01T12:00:00+00:00",
        surfaces=["comments", "reviews"],
        omitted_surfaces=[],
        reviews=reviews,
        comments=comments,
        check_runs=check_runs,
        combined_payload=combined_payload,
        sha256=sha256,
        pagination_complete=True,
    )


def _all_none_reviews_evidence() -> EvidenceBundle:
    """Reviews present but every body is None — the F4 degenerate payload."""
    payload = {"reviews": [{"body": None}, {"body": None}], "comments": []}
    return _evidence(reviews=[{"body": None}, {"body": None}], combined_payload=payload)


def _human_only_evidence() -> EvidenceBundle:
    """A human-authored payload with no Augment identity observable."""
    payload = {
        "reviews": [{"user": {"login": "human-user"}, "body": "hi"}],
        "comments": [],
    }
    return _evidence(
        reviews=[{"user": {"login": "human-user"}, "body": "hi"}],
        combined_payload=payload,
    )


def _no_surface_evidence() -> EvidenceBundle:
    return _evidence(
        reviews=[],
        comments=[],
        check_runs=[],
        combined_payload={"reviews": [], "comments": [], "check_runs": []},
    )


# --- Naive mutants (installed via monkeypatch in the differential tests) -------
def _naive_path_resolves(payload: dict, path: str | None) -> bool:
    """Pre-F4-fix: an all-None list stays truthy → path falsely resolves."""
    if not path:
        return False
    normalized = path.replace("[]", "")
    current = payload
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


def _naive_always_observed_findings_locus(evidence, answers, provenance):
    provenance["findings_locus"] = FieldProvenance(
        "reviews[].body", PROVENANCE_OBSERVED, True, "reviews[].body"
    )
    return "reviews[].body"


def _naive_always_observed_review_signal(evidence, answers, provenance):
    provenance["review_completeness_signal"] = FieldProvenance(
        "reviews[].state", PROVENANCE_OBSERVED, True, "reviews[].state"
    )
    return "reviews[].state"


def _naive_always_observed_identity(evidence, answers, provenance):
    provenance["augment_bot_login"] = FieldProvenance(
        "augmentcode[bot]", PROVENANCE_OBSERVED, True, "payload.user.login"
    )
    return "augmentcode[bot]"


def _naive_always_observed_app_slug(evidence, answers, provenance):
    provenance["augment_app_slug"] = FieldProvenance(
        "augment", PROVENANCE_OBSERVED, True, "payload.app.slug"
    )
    return "augment"


def _naive_paths_resolve_presence_only(candidate):
    """Drop the .observed checks (presence != observation) — the classic F4 sink regression."""
    findings = candidate.provenance.get("findings_locus")
    signal = candidate.provenance.get("review_completeness_signal")
    return lockgate_mod._check(
        "paths_resolve", bool(findings and signal), "presence-only (mutant)"
    )


def _naive_emission_shape_presence_only(candidate):
    provenance = candidate.provenance.get("emission_shape")
    return lockgate_mod._check(
        "emission_shape_observed", bool(provenance), "presence-only (mutant)"
    )


def _naive_resolve_optional_path(value: str | None, base: Path) -> Path | None:
    """Drop the `if not value` guard — empty string resolves to base instead of None."""
    path = Path(value)
    if path.is_absolute():
        return path
    return base / path


# ===========================================================================
# 1. candidate._path_resolves — F4 ROOT PRIMITIVE
# ===========================================================================
def test_path_resolves_all_none_list_is_not_resolved() -> None:
    pr = candidate_mod._path_resolves
    assert pr({"reviews": [{"body": None}, {"body": None}]}, "reviews[].body") is False
    assert pr({}, "reviews[].body") is False
    assert pr({"reviews": []}, "reviews[].body") is False
    assert pr({"reviews": [{"body": "x"}]}, None) is False


def test_path_resolves_differential_naive_all_none_flips_findings_observed(
    monkeypatch,
) -> None:
    ev = _all_none_reviews_evidence()
    prov_real: dict = {}
    assert candidate_mod._findings_locus(ev, SetupAnswers(), prov_real) is None
    assert prov_real["findings_locus"].observed is False

    # Install the pre-F4 naive primitive; _findings_locus reads it as a module global.
    monkeypatch.setattr(candidate_mod, "_path_resolves", _naive_path_resolves)
    prov_mut: dict = {}
    result = candidate_mod._findings_locus(ev, SetupAnswers(), prov_mut)
    assert result == "reviews[].body"
    assert (
        prov_mut["findings_locus"].observed is True
    )  # bug reappears → mutation detected


# ===========================================================================
# 2. candidate._findings_locus — F4 CALLER
# ===========================================================================
def test_findings_locus_all_none_not_observed() -> None:
    ev = _all_none_reviews_evidence()
    prov: dict = {}
    assert candidate_mod._findings_locus(ev, SetupAnswers(), prov) is None
    assert prov["findings_locus"].observed is False


def test_findings_locus_differential_always_observed_flips_required_unobserved(
    monkeypatch,
) -> None:
    ev = _all_none_reviews_evidence()
    assert "findings_locus" in derive_candidate(ev).required_unobserved()

    monkeypatch.setattr(
        candidate_mod, "_findings_locus", _naive_always_observed_findings_locus
    )
    assert "findings_locus" not in derive_candidate(ev).required_unobserved()


# ===========================================================================
# 3. candidate._review_completeness_signal
# ===========================================================================
def test_review_completeness_signal_all_none_not_observed() -> None:
    ev = _all_none_reviews_evidence()
    prov: dict = {}
    assert candidate_mod._review_completeness_signal(ev, SetupAnswers(), prov) is None
    assert prov["review_completeness_signal"].observed is False


def test_review_completeness_signal_differential_always_observed_flips_required_unobserved(
    monkeypatch,
) -> None:
    ev = _all_none_reviews_evidence()
    assert "review_completeness_signal" in derive_candidate(ev).required_unobserved()

    monkeypatch.setattr(
        candidate_mod,
        "_review_completeness_signal",
        _naive_always_observed_review_signal,
    )
    assert (
        "review_completeness_signal" not in derive_candidate(ev).required_unobserved()
    )


# ===========================================================================
# 4. candidate._selected_identity
# ===========================================================================
def test_selected_identity_no_augment_not_observed() -> None:
    ev = _human_only_evidence()
    prov: dict = {}
    assert candidate_mod._selected_identity(ev, SetupAnswers(), prov) is None
    assert prov["augment_bot_login"].observed is False


def test_selected_identity_differential_always_observed_flips_required_unobserved(
    monkeypatch,
) -> None:
    ev = _human_only_evidence()
    assert "augment_identity" in derive_candidate(ev).required_unobserved()

    monkeypatch.setattr(
        candidate_mod, "_selected_identity", _naive_always_observed_identity
    )
    assert "augment_identity" not in derive_candidate(ev).required_unobserved()


# ===========================================================================
# 5. candidate._selected_app_slug
# ===========================================================================
def test_selected_app_slug_no_augment_not_observed() -> None:
    ev = _human_only_evidence()
    prov: dict = {}
    assert candidate_mod._selected_app_slug(ev, SetupAnswers(), prov) is None
    assert prov["augment_app_slug"].observed is False


def test_selected_app_slug_differential_always_observed_flips_required_unobserved(
    monkeypatch,
) -> None:
    ev = _human_only_evidence()
    # No bot and no app observed → augment_identity is unobserved.
    assert "augment_identity" in derive_candidate(ev).required_unobserved()

    # Mutating only the app-slug selection to always-observed satisfies the
    # (bot OR app) identity clause → augment_identity wrongly drops out.
    monkeypatch.setattr(
        candidate_mod, "_selected_app_slug", _naive_always_observed_app_slug
    )
    assert "augment_identity" not in derive_candidate(ev).required_unobserved()


# ===========================================================================
# 6. lockgate._paths_resolve — F4 SINK (gate #6)
# ===========================================================================
def test_paths_resolve_unobserved_locus_fails_gate() -> None:
    candidate = derive_candidate(_all_none_reviews_evidence())
    # findings_locus + review_completeness_signal provenance are present but unobserved.
    assert candidate.provenance["findings_locus"].observed is False
    assert lockgate_mod._paths_resolve(candidate).passed is False


def test_paths_resolve_differential_presence_not_observation_flips_gate(
    monkeypatch,
) -> None:
    candidate = derive_candidate(_all_none_reviews_evidence())
    assert (
        lockgate_mod._paths_resolve(candidate).passed is False
    )  # real: unobserved fails

    monkeypatch.setattr(
        lockgate_mod, "_paths_resolve", _naive_paths_resolve_presence_only
    )
    # The mutant treats present-but-unobserved provenance as resolved → gate wrongly passes.
    assert lockgate_mod._paths_resolve(candidate).passed is True


# ===========================================================================
# 7. lockgate._emission_shape_observed — gate #5
# ===========================================================================
def test_emission_shape_observed_unobserved_fails_gate() -> None:
    candidate = derive_candidate(_no_surface_evidence())
    assert candidate.provenance["emission_shape"].observed is False
    assert lockgate_mod._emission_shape_observed(candidate).passed is False


def test_emission_shape_observed_differential_presence_not_observation_flips_gate(
    monkeypatch,
) -> None:
    candidate = derive_candidate(_no_surface_evidence())
    assert lockgate_mod._emission_shape_observed(candidate).passed is False

    monkeypatch.setattr(
        lockgate_mod, "_emission_shape_observed", _naive_emission_shape_presence_only
    )
    # The mutant treats a present-but-unobserved provenance entry as observed → wrongly passes.
    assert lockgate_mod._emission_shape_observed(candidate).passed is True


# ===========================================================================
# 8. diagnosis._resolve_optional_path
# ===========================================================================
def test_resolve_optional_path_none_and_empty_return_none() -> None:
    base = Path("/tmp/base")
    assert diagnosis_mod._resolve_optional_path(None, base) is None
    assert diagnosis_mod._resolve_optional_path("", base) is None
    # A relative value resolves under base; an absolute value passes through.
    assert diagnosis_mod._resolve_optional_path("x.yaml", base) == base / "x.yaml"


def test_resolve_optional_path_differential_dropping_guard_flips_empty(
    monkeypatch,
) -> None:
    base = Path("/tmp/base")
    assert diagnosis_mod._resolve_optional_path("", base) is None  # real: empty → None

    monkeypatch.setattr(
        diagnosis_mod, "_resolve_optional_path", _naive_resolve_optional_path
    )
    # Dropping the `if not value` guard makes an empty value resolve to `base`
    # (a real path) instead of None — a silent mis-resolve the guard prevents.
    assert diagnosis_mod._resolve_optional_path("", base) == base


# ===========================================================================
# 9. candidate.CandidateContract.required_unobserved
# ===========================================================================
def test_required_unobserved_lists_unobserved_findings_locus() -> None:
    candidate = derive_candidate(_all_none_reviews_evidence())
    missing = candidate.required_unobserved()
    assert "findings_locus" in missing
    assert "review_completeness_signal" in missing


def test_required_unobserved_differential_skipping_field_flips_membership(
    monkeypatch,
) -> None:
    candidate = derive_candidate(_all_none_reviews_evidence())
    assert "findings_locus" in candidate.required_unobserved()  # real: enforced

    # required_unobserved reads MUST_OBSERVE_FIELDS as a module global at call time.
    # Skipping findings_locus from the enforced set (the §5.3 mutation) drops it from
    # the missing list even though it is unobserved → a must-observe field goes unchecked.
    monkeypatch.setattr(
        candidate_mod,
        "MUST_OBSERVE_FIELDS",
        candidate_mod.MUST_OBSERVE_FIELDS - {"findings_locus"},
    )
    assert "findings_locus" not in candidate.required_unobserved()


# ===========================================================================
# Step 2.6 builders + naive mutants (freshness gate + anti-gaming controls)
# ===========================================================================
def _naive_stale_blockers(data, repo, pr_number, evidence_sha256):
    """Drop the evidence-hash comparison — a stale-hash report no longer blocks."""
    blockers: list[str] = []
    report_repo = diagnosis_mod._first_str(data, "repo", "repository")
    report_pr = data.get("pr_number", data.get("pr"))
    if repo and report_repo and report_repo != repo:
        blockers.append("repo mismatch")
    if (
        pr_number is not None
        and report_pr is not None
        and str(report_pr) != str(pr_number)
    ):
        blockers.append("pr mismatch")
    # (hash comparison removed — this is the mutation)
    return blockers


def _augment_candidate():
    """A real candidate derived from an Augment-authored review (identity observed)."""
    ev = _evidence(
        reviews=[
            {
                "author": {"login": "augmentcode[bot]"},
                "state": "COMMENTED",
                "submitted_at": "2026-07-01T12:00:00Z",
                "body": "finding",
            }
        ],
        comments=[],
    )
    return derive_candidate(ev)


def _non_polling_classify(payload, contract, **kwargs):
    """Simulate a permissive contract: the control payloads classify as non-polling."""
    return "findings"


def _naive_negative_control_checks(candidate):
    """Mutate `empty == STATE_POLLING` (and the sibling) to a constant True."""
    empty = validation_mod.classify({"reviews": [], "comments": []}, candidate.contract)
    non_augment_payload = {
        "reviews": [{"user": {"login": "human-user"}, "body": "finding"}],
        "comments": [{"user": {"login": "human-user"}, "body": "finding"}],
    }
    non_augment = validation_mod.classify(non_augment_payload, candidate.contract)
    return [
        validation_mod.CheckResult("empty_negative_control", True, f"empty => {empty}"),
        validation_mod.CheckResult(
            "non_augment_negative_control", True, f"non-augment => {non_augment}"
        ),
    ]


# ===========================================================================
# 10. diagnosis._stale_blockers — freshness gate (STALE-state driver)
# ===========================================================================
def test_stale_blockers_empty_report_no_blockers() -> None:
    sb = diagnosis_mod._stale_blockers
    # Empty report + no context → no false stale.
    assert sb({}, None, None, "") == []
    # Present report hash that differs from current evidence → a stale blocker.
    mismatch = sb({"evidence_sha256": "aaa"}, None, None, "bbb")
    assert mismatch and any("hash" in b.lower() for b in mismatch)


def test_stale_blockers_differential_dropping_hash_check_flips_mismatch(
    monkeypatch,
) -> None:
    data = {"evidence_sha256": "aaa"}
    assert diagnosis_mod._stale_blockers(
        data, None, None, "bbb"
    )  # real: hash mismatch blocks

    monkeypatch.setattr(diagnosis_mod, "_stale_blockers", _naive_stale_blockers)
    # Dropping the hash comparison loses the blocker → a stale report wrongly passes.
    assert diagnosis_mod._stale_blockers(data, None, None, "bbb") == []


# ===========================================================================
# 11. validation._negative_control_checks — anti-gaming controls (lockgate #9)
# ===========================================================================
def test_negative_control_checks_flags_permissive_empty_classification(
    monkeypatch,
) -> None:
    candidate = _augment_candidate()
    # Healthy contract: the real classifier keeps the empty control at POLLING → passes.
    healthy = {c.name: c for c in validation_mod._negative_control_checks(candidate)}
    assert healthy["empty_negative_control"].passed is True
    assert (
        healthy["empty_negative_control"].detail == f"empty payload => {STATE_POLLING}"
    )

    # Permissive contract simulated: classify() returns a non-polling label for controls.
    monkeypatch.setattr(validation_mod, "classify", _non_polling_classify)
    flagged = {c.name: c for c in validation_mod._negative_control_checks(candidate)}
    assert flagged["empty_negative_control"].passed is False


def test_negative_control_checks_differential_constant_true_flips(monkeypatch) -> None:
    candidate = _augment_candidate()
    monkeypatch.setattr(validation_mod, "classify", _non_polling_classify)
    real = {c.name: c for c in validation_mod._negative_control_checks(candidate)}
    assert (
        real["empty_negative_control"].passed is False
    )  # real control catches the permissive contract

    monkeypatch.setattr(
        validation_mod, "_negative_control_checks", _naive_negative_control_checks
    )
    mutated = {c.name: c for c in validation_mod._negative_control_checks(candidate)}
    # The constant-True mutant reports a pass even though the empty payload mis-classified.
    assert mutated["empty_negative_control"].passed is True
