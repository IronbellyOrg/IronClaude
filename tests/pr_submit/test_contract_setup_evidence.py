"""Evidence-loading + candidate-derivation tests for detection-contract setup.

Exercises the REAL loader/derivation/validation surface in
``superclaude.pr_submit.contract_setup`` — never live GitHub, never a real
``.dev/pr-monitor/`` directory. Every probe dir is built under ``tmp_path`` with
the exact filenames the loader reads (``gh-reviews.json`` / ``gh-comments.json``
/ ``gh-check-runs.json`` / ``combined-payload.json`` / optional ``manifest.json``).

Covers:
1. Deterministic SHA-256 of the combined payload for the same probe dir.
2. repo / PR / captured-at metadata propagation.
3. Present vs OMITTED surfaces recorded distinctly (``surfaces`` vs
   ``omitted_surfaces``).
4. Raw payload body redaction: ``EvidenceBundle.summary()`` and
   ``ValidationReport.summary()`` never echo raw review/comment/check-run bodies.
5. Cross-PR evidence recorded as shape-only readiness
   (``cross_pr_shape_only`` and its readiness-blocking freshness check).
6. Stale evidence policy: repo mismatch blocks candidate readiness via the
   freshness checks (the implemented mismatch-based policy).
7. Copied human prose cannot mint an observed Augment identity
   (``derive_candidate`` marks bot-login provenance unobserved for non-Augment
   authors).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.pr_submit.contract_setup.candidate import (
    PROVENANCE_OBSERVED,
    derive_candidate,
)
from superclaude.pr_submit.contract_setup.evidence import (
    EvidenceBundle,
    load_evidence,
)
from superclaude.pr_submit.contract_setup.questions import SetupAnswers
from superclaude.pr_submit.contract_setup.validation import validate_candidate

AUGMENT = "augmentcode[bot]"
AUGMENT_SLUG = "augmentcode"
# A unique string planted in every raw body/output; must NEVER appear in summaries.
SENTINEL = "RAW_BODY_SENTINEL_DO_NOT_PRINT_ff00ff"


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def _build_probe(
    root: Path,
    *,
    reviews: list[dict] | None = None,
    comments: list[dict] | None = None,
    check_runs: list[dict] | None = None,
    combined: dict | None = None,
    manifest: dict | None = None,
    write_surface_files: bool = True,
) -> Path:
    """Create a probe dir with the exact filenames ``load_evidence`` reads."""
    root.mkdir(parents=True, exist_ok=True)
    if write_surface_files:
        if reviews is not None:
            _write_json(root / "gh-reviews.json", reviews)
        if comments is not None:
            _write_json(root / "gh-comments.json", comments)
        if check_runs is not None:
            _write_json(root / "gh-check-runs.json", check_runs)
    if combined is not None:
        _write_json(root / "combined-payload.json", combined)
    if manifest is not None:
        _write_json(root / "manifest.json", manifest)
    return root


def _augment_clean_combined(
    *, repo: str = "IronbellyOrg/IronClaude", pr: int = 42, **extra
) -> dict:
    """A combined payload with a clean Augment review carrying a sentinel body."""
    payload = {
        "metadata": {
            "repo": repo,
            "pr_number": pr,
            "captured_at": "2026-07-01T12:00:00Z",
        },
        "reviews": [
            {
                "author": {"login": AUGMENT, "app": {"slug": AUGMENT_SLUG}},
                "app": {"slug": AUGMENT_SLUG},
                "state": "COMMENTED",
                "submitted_at": "2026-07-01T11:59:00Z",
                "author_association": "NONE",
                "has_findings": False,
                "severity": "info",
                "body": f"Looks good. {SENTINEL}",
            }
        ],
        "comments": [
            {
                "user": {"login": AUGMENT},
                "created_at": "2026-07-01T11:59:30Z",
                "author_association": "NONE",
                "severity": "info",
                "body": f"nit comment {SENTINEL}",
            }
        ],
        "check_runs": [
            {
                "app": {"slug": AUGMENT_SLUG},
                "conclusion": "success",
                "output": {"text": f"check output {SENTINEL}"},
            }
        ],
    }
    payload.update(extra)
    return payload


# ---------------------------------------------------------------------------
# 1. Deterministic SHA-256 of the combined payload.
# ---------------------------------------------------------------------------


def test_load_evidence_records_deterministic_sha256(tmp_path):
    """Same probe dir → identical canonical SHA-256 across two loads."""
    combined = _augment_clean_combined()
    probe = _build_probe(tmp_path / "probe", combined=combined)

    first = load_evidence(probe)
    second = load_evidence(probe)

    assert first.sha256
    assert len(first.sha256) == 64  # hex sha256
    assert first.sha256 == second.sha256

    # A different payload → different hash (the hash actually covers content).
    other = _build_probe(
        tmp_path / "probe2",
        combined=_augment_clean_combined(pr=99),
    )
    assert load_evidence(other).sha256 != first.sha256


def test_sha256_is_key_order_independent(tmp_path):
    """Canonical (sort_keys) hashing → key order in the JSON does not change the hash."""
    base = _augment_clean_combined()
    reordered = {k: base[k] for k in reversed(list(base.keys()))}

    a = _build_probe(tmp_path / "a", combined=base)
    b = _build_probe(tmp_path / "b", combined=reordered)

    assert load_evidence(a).sha256 == load_evidence(b).sha256


# ---------------------------------------------------------------------------
# 2. repo / PR / captured-at metadata propagation.
# ---------------------------------------------------------------------------


def test_metadata_propagates_from_combined_payload(tmp_path):
    combined = _augment_clean_combined(repo="acme/widgets", pr=7)
    probe = _build_probe(tmp_path / "probe", combined=combined)

    bundle = load_evidence(probe)

    assert bundle.repo == "acme/widgets"
    assert bundle.pr_number == 7
    assert bundle.captured_at == "2026-07-01T12:00:00Z"


def test_metadata_propagates_from_manifest(tmp_path):
    """Manifest is a first-class metadata source (takes precedence)."""
    combined = {"reviews": [], "comments": [], "check_runs": []}
    manifest = {
        "repo": "manifest-org/repo",
        "pr_number": 314,
        "captured_at": "2026-06-30T08:00:00Z",
    }
    probe = _build_probe(tmp_path / "probe", combined=combined, manifest=manifest)

    bundle = load_evidence(probe)

    assert bundle.repo == "manifest-org/repo"
    assert bundle.pr_number == 314
    assert bundle.captured_at == "2026-06-30T08:00:00Z"


def test_captured_at_falls_back_to_file_mtime_when_absent(tmp_path):
    """No captured_at metadata → loader derives a timestamp from file mtimes."""
    combined = {"reviews": [], "comments": [], "check_runs": []}
    probe = _build_probe(tmp_path / "probe", combined=combined)

    bundle = load_evidence(probe)

    # No metadata timestamp, but a JSON file exists → mtime-derived ISO string.
    assert bundle.captured_at is not None
    assert "T" in bundle.captured_at


# ---------------------------------------------------------------------------
# 3. Present vs OMITTED surfaces recorded distinctly.
# ---------------------------------------------------------------------------


def test_present_and_omitted_surfaces_are_distinct(tmp_path):
    """Surface files present via gh-*.json are 'surfaces'; absent ones are 'omitted'."""
    probe = _build_probe(
        tmp_path / "probe",
        reviews=[{"author": {"login": AUGMENT}, "has_findings": False}],
        comments=[{"user": {"login": AUGMENT}, "body": "hi"}],
        # No gh-check-runs.json written → check_runs omitted.
        combined=None,
    )

    bundle = load_evidence(probe)

    assert set(bundle.surfaces) == {"reviews", "comments"}
    assert bundle.omitted_surfaces == ["check_runs"]
    # A surface is never in both lists at once.
    assert not (set(bundle.surfaces) & set(bundle.omitted_surfaces))


def test_all_surfaces_present_leaves_omitted_empty(tmp_path):
    probe = _build_probe(
        tmp_path / "probe",
        reviews=[{"author": {"login": AUGMENT}, "has_findings": False}],
        comments=[],
        check_runs=[],
    )

    bundle = load_evidence(probe)

    assert set(bundle.surfaces) == {"reviews", "comments", "check_runs"}
    assert bundle.omitted_surfaces == []


def test_omitted_surface_not_conflated_with_empty_present_surface(tmp_path):
    """An empty-but-present surface (file exists, list is []) is PRESENT, not omitted."""
    probe = _build_probe(
        tmp_path / "probe",
        reviews=[],  # gh-reviews.json exists but is empty → present
        comments=[{"user": {"login": AUGMENT}, "body": "x"}],
        # check_runs file absent → omitted
    )

    bundle = load_evidence(probe)

    assert "reviews" in bundle.surfaces  # present despite being empty
    assert "check_runs" in bundle.omitted_surfaces
    assert "reviews" not in bundle.omitted_surfaces


# ---------------------------------------------------------------------------
# 4. Raw payload body redaction.
# ---------------------------------------------------------------------------


def test_evidence_summary_omits_raw_payload_bodies(tmp_path):
    combined = _augment_clean_combined()
    probe = _build_probe(tmp_path / "probe", combined=combined)

    bundle = load_evidence(probe)
    summary = bundle.summary()

    # The raw bodies live in the bundle...
    assert bundle.reviews[0]["body"].endswith(SENTINEL)
    # ...but the summary never echoes them.
    assert SENTINEL not in summary
    # Redaction stays useful: safe metadata + hash + counts remain.
    assert bundle.sha256 in summary
    assert "counts=reviews:1" in summary


def test_validation_summary_omits_raw_payload_bodies(tmp_path):
    combined = _augment_clean_combined()
    probe = _build_probe(tmp_path / "probe", combined=combined)
    bundle = load_evidence(probe)

    candidate = derive_candidate(bundle)
    report = validate_candidate(
        candidate, bundle, expected_result=candidate.expected_classifier_result
    )
    summary = report.summary()

    assert SENTINEL not in summary
    # Diagnostics still carry the evidence hash so redaction is not lossy.
    assert bundle.sha256 in summary


def test_raw_sentinel_still_present_in_on_disk_json(tmp_path):
    """Redaction is a rendering concern: the raw evidence JSON still holds the body."""
    combined = _augment_clean_combined()
    probe = _build_probe(tmp_path / "probe", combined=combined)

    raw = (probe / "combined-payload.json").read_text(encoding="utf-8")
    assert SENTINEL in raw  # source of truth keeps the body
    assert SENTINEL not in load_evidence(probe).summary()  # rendering redacts it


# ---------------------------------------------------------------------------
# 5. Cross-PR evidence recorded as shape-only readiness.
# ---------------------------------------------------------------------------


def test_cross_pr_evidence_flagged_shape_only(tmp_path):
    combined = _augment_clean_combined(cross_pr_shape_only=True)
    probe = _build_probe(tmp_path / "probe", combined=combined)

    bundle = load_evidence(probe)

    assert bundle.cross_pr_shape_only is True
    assert "cross_pr_shape_only=True" in bundle.summary()


def test_cross_pr_shape_only_blocks_readiness(tmp_path):
    """Shape-only cross-PR evidence cannot establish current-PR readiness."""
    combined = _augment_clean_combined(cross_pr_shape_only=True)
    probe = _build_probe(tmp_path / "probe", combined=combined)
    bundle = load_evidence(probe)

    candidate = derive_candidate(bundle)
    report = validate_candidate(
        candidate, bundle, expected_result=candidate.expected_classifier_result
    )

    assert report.passed is False
    assert any("shape-only" in b for b in report.blockers)


def test_default_evidence_is_not_cross_pr_shape_only(tmp_path):
    """Absent the flag, evidence is treated as current-PR (not shape-only)."""
    probe = _build_probe(tmp_path / "probe", combined=_augment_clean_combined())
    assert load_evidence(probe).cross_pr_shape_only is False


# ---------------------------------------------------------------------------
# 6. Stale evidence policy (repo mismatch blocks readiness).
# ---------------------------------------------------------------------------


def test_repo_mismatch_blocks_candidate_readiness(tmp_path):
    """Candidate repo (from evidence) that does not match evidence.repo blocks lock.

    The implemented freshness policy is mismatch-based: the validation
    ``repo_match`` check compares the candidate's recorded repo against the
    evidence repo. Forcing a divergence surfaces the stale/blocked path.
    """
    combined = _augment_clean_combined(repo="real-org/real-repo")
    probe = _build_probe(tmp_path / "probe", combined=combined)
    bundle = load_evidence(probe)

    # The candidate records repo provenance from the ORIGINAL evidence
    # ("real-org/real-repo"). We then validate it against a divergent bundle
    # whose repo differs, exercising the freshness ``repo_match`` = False path.
    candidate = derive_candidate(bundle)
    divergent = EvidenceBundle(
        probe_dir=bundle.probe_dir,
        repo="other-org/other-repo",
        pr_number=bundle.pr_number,
        captured_at=bundle.captured_at,
        surfaces=bundle.surfaces,
        omitted_surfaces=bundle.omitted_surfaces,
        reviews=bundle.reviews,
        comments=bundle.comments,
        check_runs=bundle.check_runs,
        combined_payload=bundle.combined_payload,
        sha256=bundle.sha256,
        pagination_complete=bundle.pagination_complete,
        cross_pr_shape_only=bundle.cross_pr_shape_only,
    )
    report = validate_candidate(
        candidate, divergent, expected_result=candidate.expected_classifier_result
    )

    assert report.passed is False
    assert any("repo" in b.lower() for b in report.blockers)


def test_matching_repo_passes_freshness(tmp_path):
    """The clean, self-consistent evidence bundle passes the freshness gate."""
    combined = _augment_clean_combined()
    probe = _build_probe(tmp_path / "probe", combined=combined)
    bundle = load_evidence(probe)

    candidate = derive_candidate(bundle)
    report = validate_candidate(
        candidate, bundle, expected_result=candidate.expected_classifier_result
    )

    # No repo/shape-only blockers on the consistent bundle.
    assert not any("repo" in b.lower() for b in report.blockers)
    assert not any("shape-only" in b for b in report.blockers)


# ---------------------------------------------------------------------------
# 7. Copied human prose cannot mint an observed Augment identity.
# ---------------------------------------------------------------------------


def test_human_prose_does_not_produce_observed_augment_identity(tmp_path):
    """A human-authored review that merely QUOTES Augment text never marks the
    bot-login provenance as observed."""
    combined = {
        "metadata": {"repo": "acme/repo", "pr_number": 5},
        "reviews": [
            {
                "author": {"login": "octocat"},
                "state": "COMMENTED",
                "has_findings": False,
                "body": "I pasted what augment-code said: 'looks fine to me'.",
            }
        ],
        "comments": [],
        "check_runs": [],
    }
    probe = _build_probe(tmp_path / "probe", combined=combined)
    bundle = load_evidence(probe)

    candidate = derive_candidate(bundle)
    bot = candidate.provenance.get("augment_bot_login")

    assert bot is not None
    assert bot.observed is False
    assert bot.source != PROVENANCE_OBSERVED
    # The must-observe identity gate flags the unobserved augment_identity.
    assert "augment_identity" in candidate.required_unobserved()


def test_user_supplied_identity_absent_from_payload_is_not_observed(tmp_path):
    """An operator-typed identity that does NOT appear in the payload is recorded
    as user-sourced but NOT observed (cannot be laundered into 'observed')."""
    combined = {
        "metadata": {"repo": "acme/repo", "pr_number": 5},
        "reviews": [
            {"author": {"login": "octocat"}, "has_findings": False, "body": "ok"}
        ],
        "comments": [],
        "check_runs": [],
    }
    probe = _build_probe(tmp_path / "probe", combined=combined)
    bundle = load_evidence(probe)

    answers = SetupAnswers(detected_augment_identity="augmentcode[bot]")
    candidate = derive_candidate(bundle, answers=answers)
    bot = candidate.provenance["augment_bot_login"]

    assert bot.value == "augmentcode[bot]"
    assert bot.observed is False  # not present in the captured payload
    assert "augment_identity" in candidate.required_unobserved()


def test_real_augment_review_is_observed_identity(tmp_path):
    """Contrast: a genuine Augment-authored review DOES mark identity observed."""
    combined = _augment_clean_combined()
    probe = _build_probe(tmp_path / "probe", combined=combined)
    bundle = load_evidence(probe)

    candidate = derive_candidate(bundle)
    bot = candidate.provenance["augment_bot_login"]

    assert bot.value == AUGMENT
    assert bot.observed is True
    assert bot.source == PROVENANCE_OBSERVED
    assert "augment_identity" not in candidate.required_unobserved()


# ---------------------------------------------------------------------------
# Loader guardrails.
# ---------------------------------------------------------------------------


def test_missing_probe_dir_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_evidence(tmp_path / "does-not-exist")


def test_empty_probe_dir_with_no_json_raises(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(FileNotFoundError):
        load_evidence(empty)
