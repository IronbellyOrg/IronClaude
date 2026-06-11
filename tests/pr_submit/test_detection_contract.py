"""Detection-contract tests (spec FR-2.1/FR-2.2, §7).

Covers the three-state classifier (T-201 polling / T-202 clean / T-203 findings),
the T-210 lock gate (``locked:false``/absent → HALT "probe first"), T-211 (a
different bot login → review not detected), and T-212 (interleaved Augment+human
reviews → only the Augment author parsed).

The payloads here are PROVISIONAL inline dicts so the module collects and runs
standalone at the Phase-2 contract gate. Phase 10 lands the durable
``tests/pr_submit/fixtures/*.json`` set (``review-clean.json``,
``review-with-findings.json``, ``review-non-augment.json``,
``review-interleaved.json``) which SUPERSEDES these inline dicts — when Phase 10
lands, swap the inline dicts for ``load_fixture(...)`` rather than keeping both.
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit import (
    DetectionContract,
    DetectionContractLocked,
    classify,
    poll_augment_review,
)

AUGMENT = "augment-code[bot]"


@pytest.fixture
def contract() -> DetectionContract:
    """A synthetic, locked contract for pure classifier tests (bypasses load())."""
    return DetectionContract(
        augment_bot_login=AUGMENT,
        augment_author_association=["NONE", "CONTRIBUTOR"],
        augment_app_slug="augment-code",
        emission_shape="review",
        findings_locus="comments[]",
        locked=True,
    )


def test_t201_empty_reviews_polling(contract):
    """T-201: empty reviews → state = polling."""
    # Phase 10: swap for load_fixture("review-clean.json") with reviews=[].
    payload = {"reviews": [], "comments": []}
    assert classify(payload, contract) == "polling"
    assert poll_augment_review(42, payload=payload, contract=contract) == "polling"


def test_t202_augment_clean(contract):
    """T-202: Augment review, empty findings → state = clean."""
    # Phase 10: swap for load_fixture("review-clean.json").
    payload = {
        "reviews": [
            {"author": {"login": AUGMENT}, "state": "COMMENTED", "has_findings": False}
        ],
        "comments": [],
    }
    assert classify(payload, contract) == "clean"


def test_t203_augment_findings(contract):
    """T-203: Augment review with findings → state = findings."""
    # Phase 10: swap for load_fixture("review-with-findings.json").
    payload = {
        "reviews": [
            {"author": {"login": AUGMENT}, "state": "COMMENTED", "has_findings": True}
        ],
        "comments": [],
    }
    assert classify(payload, contract) == "findings"


def test_t210_locked_false_halts(tmp_path):
    """T-210: contract locked:false (or absent) → skill HALTs with "probe first"."""
    # The shipped contract ships locked:false — loading it for arming HALTs.
    with pytest.raises(DetectionContractLocked):
        DetectionContract.load()

    # An explicit unlocked contract file also HALTs.
    unlocked = tmp_path / "detection-contract.md"
    unlocked.write_text(
        '# c\n\n```yaml\naugment_bot_login: "<PROBE-LOCKED>"\nlocked: false\n```\n',
        encoding="utf-8",
    )
    with pytest.raises(DetectionContractLocked):
        DetectionContract.load(unlocked)

    # An absent contract HALTs too.
    with pytest.raises(DetectionContractLocked):
        DetectionContract.load(tmp_path / "does-not-exist.md")

    # require_locked=False allows inspection without HALTing (locked is False).
    inspected = DetectionContract.load(unlocked, require_locked=False)
    assert inspected.locked is False


def test_local_override_arms_without_touching_shipped_source(tmp_path, monkeypatch):
    """The operator-local locked override arms (for_arming/prefer_local_override) while the
    shipped source stays locked:false — so T-210's default-load HALT is unaffected by the override."""
    from superclaude.pr_submit import detection

    override = tmp_path / "detection-contract.locked.md"
    override.write_text(
        '# local\n\n```yaml\naugment_bot_login: "augmentcode[bot]"\nlocked: true\n```\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(detection, "_LOCAL_OVERRIDE_PATH", override)

    # Default load() ignores the override → shipped source (locked:false) → HALT (T-210 unaffected).
    with pytest.raises(DetectionContractLocked):
        DetectionContract.load()

    # The arm path prefers the override → loads locked:true with the real bot login (ARMED).
    armed = DetectionContract.for_arming()
    assert armed.locked is True
    assert armed.augment_bot_login == "augmentcode[bot]"
    assert DetectionContract.load(prefer_local_override=True).locked is True

    # With no override present, the arm path falls back to the shipped source → HALT.
    monkeypatch.setattr(detection, "_LOCAL_OVERRIDE_PATH", tmp_path / "absent.md")
    with pytest.raises(DetectionContractLocked):
        DetectionContract.for_arming()


def test_t211_different_bot_not_detected(contract):
    """T-211: a comment/review from a different bot login → review not detected."""
    # Phase 10: swap for load_fixture("review-non-augment.json").
    payload = {
        "reviews": [{"author": {"login": "github-actions[bot]"}, "has_findings": True}],
        "comments": [
            {"user": {"login": "github-actions[bot]"}, "path": "a.py", "line": 1}
        ],
    }
    assert classify(payload, contract) == "polling"


def test_tn31_known_non_augment_bot_polling():
    """T-N31 (NFR-4 fail-safe): a known non-Augment bot review stays "polling".

    The complement to T-N30: a `github-actions[bot]` review (a real, common CI bot,
    NOT the Augment reviewer) must NOT be detected as a findings/clean review — the
    fail-safe default is to keep polling (the review is "not detected"). This pins
    the unresolvable T-N31 ID from spec §6.2 (NFR-4) to a concrete assertion;
    behavior is adjacent to FM-4 / EC-10 but the named bot is the explicit subject.
    """
    locked_contract = DetectionContract(augment_bot_login=AUGMENT, locked=True)
    payload = {
        "reviews": [{"author": {"login": "github-actions[bot]"}, "has_findings": True}],
        "comments": [],
    }
    assert classify(payload, locked_contract) == "polling"


def test_t212_interleaved_only_augment_parsed(contract):
    """T-212: two reviews, one Augment one human → only the Augment author parsed."""
    # Phase 10: swap for load_fixture("review-interleaved.json").
    payload = {
        "reviews": [
            {
                "author": {"login": "octocat"},
                "has_findings": False,
                "state": "APPROVED",
            },
            {"author": {"login": AUGMENT}, "has_findings": True, "state": "COMMENTED"},
        ],
        "comments": [],
    }
    # The Augment review carries findings; the human "APPROVED" is ignored.
    assert classify(payload, contract) == "findings"

    # And when only the human reviews (no Augment), it is "polling" — proving the
    # human review never drives the state.
    human_only = {
        "reviews": [
            {"author": {"login": "octocat"}, "has_findings": True, "state": "COMMENTED"}
        ],
        "comments": [],
    }
    assert classify(human_only, contract) == "polling"
