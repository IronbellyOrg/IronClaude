"""Pure three-state review classifier for the ``sc:pr-submit`` core (spec §7 / FR-2.2).

:func:`classify` is a pure function of ``(payload, contract)`` that returns one of
``"polling"`` / ``"clean"`` / ``"findings"``. It keys ONLY on
``contract.augment_bot_login`` (never a literal string), so a different bot login
is treated as "review not detected" (T-211) and interleaved Augment+human reviews
parse only the Augment author (T-212).

NFR-6 core purity: no review-fetch command tokens; the payload is already fetched.
"""

from __future__ import annotations

from typing import Any

# The three review states this classifier can emit.
STATE_POLLING = "polling"
STATE_CLEAN = "clean"
STATE_FINDINGS = "findings"


def _login_of(entry: dict) -> str | None:
    """Extract the author login from either payload shape.

    ``gh pr view --json reviews`` yields ``{"author": {"login": ...}}`` while the
    REST ``/pulls/<N>/reviews`` (and ``/comments``) yields ``{"user": {"login": ...}}``.
    Both are supported so synthetic fixtures may use either shape.
    """
    author = entry.get("author")
    if isinstance(author, dict) and author.get("login"):
        return author["login"]
    user = entry.get("user")
    if isinstance(user, dict) and user.get("login"):
        return user["login"]
    # Some flattened fixtures put the login directly on the entry.
    return entry.get("login")


def _augment_entries(entries: Any, bot_login: str | None) -> list[dict]:
    """Filter ``entries`` to those authored by the contract's Augment bot login."""
    if not isinstance(entries, list) or not bot_login:
        return []
    return [e for e in entries if isinstance(e, dict) and _login_of(e) == bot_login]


def _entry_has_findings(review: dict) -> bool:
    """True when a single Augment review object self-signals findings.

    Synthetic fixtures may carry an explicit ``has_findings`` flag or a
    ``findings_count`` integer; either being truthy marks the review as carrying
    findings. (The real ``findings_locus`` JSON path is probe-locked; the
    synthetic shape mirrors it.)
    """
    if review.get("has_findings"):
        return True
    count = review.get("findings_count")
    return isinstance(count, int) and count > 0


def classify(payload: dict, contract: Any) -> str:
    """Return the review state for ``payload`` against ``contract`` (pure).

    - No Augment review present (empty reviews, or only a non-Augment/different
      bot author) → ``"polling"`` (T-201, T-211).
    - Augment review present, no findings → ``"clean"`` (T-202).
    - Augment review present, findings present (in the review object's
      self-signal or in Augment-authored inline comments) → ``"findings"``
      (T-203). Interleaved reviews parse only the Augment author (T-212).
    """
    bot_login = getattr(contract, "augment_bot_login", None)
    reviews = payload.get("reviews") if isinstance(payload, dict) else None
    comments = payload.get("comments") if isinstance(payload, dict) else None

    augment_reviews = _augment_entries(reviews, bot_login)
    if not augment_reviews:
        # No review detected from the Augment bot (T-201 empty / T-211 other bot).
        return STATE_POLLING

    # An Augment review exists — determine clean vs findings. Findings live either
    # in the review object's self-signal or in Augment-authored inline comments
    # (findings_locus == comments[]). Only the Augment author is parsed (T-212).
    if any(_entry_has_findings(r) for r in augment_reviews):
        return STATE_FINDINGS
    if _augment_entries(comments, bot_login):
        return STATE_FINDINGS
    return STATE_CLEAN
