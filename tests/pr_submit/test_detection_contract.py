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

from types import SimpleNamespace

import pytest

from superclaude.cli.reflect.commands import _contract_status_next_command
from superclaude.pr_submit import (
    DetectionContract,
    DetectionContractLocked,
    classify,
    is_decline,
    poll_augment_review,
)
from superclaude.pr_submit.contract_setup import ContractState
from superclaude.pr_submit.contract_setup.diagnosis import _next_command

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


def test_contract_setup_next_commands_are_current_and_actionable():
    """Contract readiness next steps use the Phase-3 CLI surface and PR context."""
    missing = _next_command(ContractState.MISSING, None, None)
    validation = _next_command(
        ContractState.VALIDATION_MISSING, "IronbellyOrg/IronClaude", 42
    )
    ready = _next_command(ContractState.READY, "IronbellyOrg/IronClaude", 42)
    ready_placeholder = _next_command(ContractState.READY, None, None)

    assert (
        missing
        == "superclaude reflect contract-status --repo <owner/repo> --pr <number>"
    )
    assert (
        validation
        == "superclaude reflect contract-status --validate --repo IronbellyOrg/IronClaude --pr 42"
    )
    assert ready == "/sc:pr-submit --monitor 1 --pr 42"
    assert ready_placeholder == "/sc:pr-submit --monitor 1 --pr <number>"
    assert (
        _contract_status_next_command(
            SimpleNamespace(
                state=ContractState.READY, repo="IronbellyOrg/IronClaude", pr_number=42
            )
        )
        == "/sc:pr-submit --monitor 1 --pr 42"
    )
    assert "not yet implemented" not in missing
    assert "not yet implemented" not in validation


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


# --- V1.1 decline classification (FR-9.1, addendum §6.2) ---------------------
# A decline is an Augment-authored comment whose body matches BOTH the
# decline-phrase regex AND the decline-retrigger regex. It is classified FIRST so
# it is never miscounted as "findings". A stale pre-watermark decline is ignored
# (EC-23). The `contract` fixture carries the baked-default decline regexes.


@pytest.mark.inv
def test_t1110_decline_both_regexes_match(contract, load_fixture):
    """T-1110: an Augment "abnormally large" + re-trigger comment → "declined"."""
    payload = load_fixture("decline-comment.json")
    assert payload["expected"]["state"] == "declined"
    assert classify(payload, contract) == "declined"
    # The decline comment alone is a decline via the pure predicate.
    assert is_decline(payload["comments"][0], contract) is True


@pytest.mark.inv
def test_t1110b_decline_from_initial_poll(contract, load_fixture):
    """T-1110b: a decline surfaced at the INITIAL S2 poll → "declined" (FR-9.1)."""
    payload = load_fixture("decline-initial-poll.json")
    assert classify(payload, contract) == "declined"


@pytest.mark.inv
def test_t1110_decline_backtick_wrapped_trigger(contract, load_fixture):
    """T-1110 (real-shape): the REAL Augment decline renders the trigger with markdown
    backticks — ``Comment `augment review` `` — and must still classify as "declined".

    Guards the Phase-3 QA finding F1: the spec-literal ``["']?`` char class would miss
    the most common real decline shape; the default regex includes the backtick.
    """
    payload = load_fixture("decline-backtick.json")
    assert "`augment review`" in payload["comments"][0]["body"]
    assert is_decline(payload["comments"][0], contract) is True
    assert classify(payload, contract) == "declined"


@pytest.mark.inv
def test_live_markdown_decline_graphql_app_slug_classifies_declined():
    """Live PR #188 shape: GraphQL author.login uses app slug, REST bot login differs."""
    live_contract = DetectionContract(
        augment_bot_login="augmentcode[bot]",
        augment_app_slug="augmentcode",
        locked=True,
    )
    comment = {
        "author": {"login": "augmentcode"},
        "body": 'This PR is abnormally large; comment "**_augment review_**" to continue.',
        "id": 18801,
    }
    assert is_decline(comment, live_contract) is True
    assert classify({"reviews": [], "comments": [comment]}, live_contract) == "declined"


@pytest.mark.inv
def test_live_markdown_decline_rest_bot_login_classifies_declined():
    """Live PR #188 REST issue-comment shape: user.login is augmentcode[bot]."""
    live_contract = DetectionContract(
        augment_bot_login="augmentcode[bot]",
        augment_app_slug="augmentcode",
        locked=True,
    )
    comment = {
        "user": {"login": "augmentcode[bot]"},
        "body": 'This PR is abnormally large; comment "**_augment review_**" to continue.',
        "id": 18802,
    }
    assert is_decline(comment, live_contract) is True
    assert classify({"reviews": [], "comments": [comment]}, live_contract) == "declined"


@pytest.mark.inv
def test_live_markdown_decline_empty_identity_set_fail_safe():
    """Empty contract identities do not accept matching decline text."""
    empty_contract = DetectionContract(locked=True)
    comment = {
        "user": {"login": "augmentcode[bot]"},
        "body": 'This PR is abnormally large; comment "**_augment review_**" to continue.',
        "id": 18803,
    }
    assert is_decline(comment, empty_contract) is False
    assert classify({"reviews": [], "comments": [comment]}, empty_contract) == "polling"


@pytest.mark.inv
def test_t1110c_decline_wins_over_cooccurring_findings(contract):
    """Decline-FIRST ordering (FR-9.1): when a findings-bearing Augment review AND a
    decline comment co-occur, the state is "declined" — a decline is NEVER miscounted
    as "findings". Guards QA finding F2 (decline-first ordering was previously untested
    against co-occurrence; every other decline fixture has reviews=[]).
    """
    payload = {
        "reviews": [
            {
                "author": {"login": AUGMENT},
                "state": "COMMENTED",
                "has_findings": True,
            }
        ],
        "comments": [
            {
                "user": {"login": AUGMENT},
                "body": 'This PR is abnormally large; comment "augment review" to proceed.',
                "id": 4104,
            }
        ],
    }
    # Sanity: the review alone WOULD be "findings" — proving the decline must win.
    findings_only = {"reviews": payload["reviews"], "comments": []}
    assert classify(findings_only, contract) == "findings"
    # With the co-occurring decline, decline-first ordering yields "declined".
    assert classify(payload, contract) == "declined"


@pytest.mark.inv
def test_t1111_abnormally_large_without_retrigger_is_not_decline(contract):
    """T-1111: a body mentioning ONLY "abnormally large" (no re-trigger) is NOT a decline.

    Both regexes must match. With no formal review present, the state stays
    "polling" — the phrase alone never flips to "declined".
    """
    payload = {
        "reviews": [],
        "comments": [
            {
                "user": {"login": AUGMENT},
                "body": "Heads up: this diff is abnormally large.",
                "id": 4101,
            }
        ],
    }
    assert is_decline(payload["comments"][0], contract) is False
    assert classify(payload, contract) == "polling"


@pytest.mark.inv
def test_t1112_retrigger_instruction_without_phrase_is_not_decline(contract):
    """T-1112: a re-trigger instruction WITHOUT the "abnormally large" phrase is NOT a decline.

    Guards the AND requirement from the other side — a benign comment that merely
    says 'comment "augment review"' (e.g. an operator echo) must not be a decline.
    """
    payload = {
        "reviews": [],
        "comments": [
            {
                "user": {"login": AUGMENT},
                "body": 'To re-run, comment "augment review" on the PR.',
                "id": 4102,
            }
        ],
    }
    assert is_decline(payload["comments"][0], contract) is False
    assert classify(payload, contract) == "polling"


@pytest.mark.inv
def test_t1112b_decline_from_non_augment_author_ignored(contract):
    """T-1112b: a decline-shaped comment from a NON-Augment author is NOT a decline (T-211 sibling)."""
    payload = {
        "reviews": [],
        "comments": [
            {
                "user": {"login": "octocat"},
                "body": 'This PR is abnormally large; comment "augment review".',
                "id": 4103,
            }
        ],
    }
    assert is_decline(payload["comments"][0], contract) is False
    assert classify(payload, contract) == "polling"


@pytest.mark.inv
def test_ec23_t1118_stale_pre_watermark_decline_ignored(contract, load_fixture):
    """EC-23 / T-1118: a decline OLDER than the watermark is ignored; the same decline
    with no watermark (None) is accepted."""
    payload = load_fixture("stale-decline-pre-watermark.json")
    comment = payload["comments"][0]
    watermark = payload["watermark"]
    # With the watermark, the stale decline is ignored.
    assert is_decline(comment, contract, watermark=watermark) is False
    assert classify(payload, contract, watermark=watermark) != "declined"
    # With no watermark (None), the same decline IS accepted.
    assert is_decline(comment, contract, watermark=None) is True
    assert classify(payload, contract) == "declined"


@pytest.mark.inv
def test_t1117_ec22_attributed_rereview_wins_over_decline(contract):
    """T-1117 / EC-22 / FR-9.5: at the S5 re-trigger poll, a GENUINE attributed re-review
    (a real review newer than the watermark) WINS over a co-occurring decline (review >
    decline — the App actually reviewed). The decline-first rule (FR-9.1) is overridden
    ONLY here (a watermark is set); the initial poll keeps decline-first.
    """
    watermark = "2026-06-12T09:30:00Z"
    decline = {
        "user": {"login": AUGMENT},
        "createdAt": "2026-06-12T10:00:00Z",
        "body": 'abnormally large; comment "augment review"',
        "id": 4201,
    }
    # A genuine attributed re-review (newer than the watermark) carrying findings.
    rereview_findings = {
        "author": {"login": AUGMENT},
        "createdAt": "2026-06-12T10:05:00Z",
        "state": "COMMENTED",
        "has_findings": True,
    }
    payload = {"reviews": [rereview_findings], "comments": [decline]}
    # Review wins → "findings" (NOT "declined"), proceed as an attributed re-review.
    assert classify(payload, contract, watermark=watermark) == "findings"
    # A clean attributed re-review + the same decline → "clean" (review still wins).
    clean_rereview = {**rereview_findings, "has_findings": False}
    assert (
        classify(
            {"reviews": [clean_rereview], "comments": [decline]},
            contract,
            watermark=watermark,
        )
        == "clean"
    )
    # Contrast — at the INITIAL poll (watermark=None), decline-first (FR-9.1) holds.
    assert classify(payload, contract, watermark=None) == "declined"
    # Contrast — a decline with NO attributed re-review at S5 stays "declined".
    assert (
        classify({"reviews": [], "comments": [decline]}, contract, watermark=watermark)
        == "declined"
    )
