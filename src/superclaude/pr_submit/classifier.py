"""Pure four-state review classifier for the ``sc:pr-submit`` core (spec §7 / FR-2.2,
addendum FR-9.1).

:func:`classify` is a pure function of ``(payload, contract)`` that returns one of
``"polling"`` / ``"clean"`` / ``"findings"`` / ``"declined"``. It keys on the Augment
IDENTITY SET ``{contract.augment_bot_login, contract.augment_app_slug}`` (never a literal
string), so the same author rendered as ``augmentcode[bot]`` (REST) or ``augmentcode``
(GraphQL app-slug) is recognized either way, while a different bot login is treated as
"review not detected" (T-211) and interleaved Augment+human reviews parse only the Augment
author (T-212). The V1.1 ``"declined"`` state (FR-9.1) is checked FIRST so an Augment
"abnormally large" decline is never miscounted as ``"findings"``; the decline predicate
lives in the sibling pure fn :func:`is_decline`.

NFR-6 core purity: no review-fetch command tokens; the payload is already fetched.
"""

from __future__ import annotations

import re
from typing import Any

# The four review states this classifier can emit.
STATE_POLLING = "polling"
STATE_CLEAN = "clean"
STATE_FINDINGS = "findings"
STATE_DECLINED = "declined"


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


def _augment_identities(contract: Any) -> set[str]:
    """Return non-empty Augment identities accepted for this detection contract."""
    identities = {
        getattr(contract, "augment_bot_login", None),
        getattr(contract, "augment_app_slug", None),
    }
    return {str(identity) for identity in identities if identity}


def _augment_entries(entries: Any, augment_identities: set[str]) -> list[dict]:
    """Filter ``entries`` to those authored by any configured Augment identity."""
    if not isinstance(entries, list) or not augment_identities:
        return []
    return [
        e for e in entries if isinstance(e, dict) and _login_of(e) in augment_identities
    ]


def _entry_ts(entry: dict) -> Any:
    """Best-effort timestamp for a comment OR review entry.

    Comments carry ``createdAt`` / ``created_at``; review objects carry ``submittedAt``
    (and sometimes ``createdAt``). Checking all three keeps the watermark/staleness
    logic consistent whether a decline arrives as a comment or as a review — without
    this, a decline-as-review (only ``submittedAt``) would bypass staleness (FR-9.5).
    """
    return entry.get("createdAt") or entry.get("created_at") or entry.get("submittedAt")


def _is_newer(ts: Any, watermark: Any) -> bool:
    """True iff ``ts`` is strictly newer than ``watermark``, compared fail-safe.

    GitHub timestamps are ISO-8601 strings (lexicographically orderable). If either
    side is absent, or the two are not order-comparable (e.g. a ``datetime`` vs a
    string), return False — a non-comparable/absent timestamp is treated as NOT newer
    rather than raising ``TypeError`` (fail-safe staleness; FR-9.5).
    """
    if ts is None or watermark is None:
        return False
    try:
        return ts > watermark
    except TypeError:
        return False


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


def is_decline(comment: dict, contract: Any, *, watermark: Any = None) -> bool:
    """True iff ``comment`` is an Augment "abnormally large" decline (FR-9.1 / FR-9.5).

    A decline is an Augment-authored comment (authored by any identity in the contract's
    ``{augment_bot_login, augment_app_slug}`` set) whose body matches BOTH
    ``contract.decline_phrase_regex`` (default ``abnormally\\s+large``) AND
    ``contract.decline_retrigger_regex`` (default
    ``comment ["'`*_]*(augment|auggie|augmentcode) review["'`*_]*`` — the ``*_`` wrappers
    accept the Markdown-emphasized real shape ``comment "**_augment review_**"``),
    case-insensitively, AND that is newer than ``watermark``. A ``None`` watermark accepts
    any decline; when a watermark is given, a comment whose ``createdAt``/``created_at`` is
    not strictly newer is treated as a stale pre-watermark decline and ignored (EC-23).

    Pure: no I/O, no ``gh``/``git`` tokens. A body matching only ``abnormally large``
    (no re-trigger instruction) is NOT a decline — both regexes must match.
    """
    if not isinstance(comment, dict):
        return False
    augment_identities = _augment_identities(contract)
    if not augment_identities or _login_of(comment) not in augment_identities:
        return False
    phrase_re = getattr(contract, "decline_phrase_regex", None)
    retrigger_re = getattr(contract, "decline_retrigger_regex", None)
    if not phrase_re or not retrigger_re:
        return False
    body = comment.get("body") or ""
    if not re.search(phrase_re, body, re.IGNORECASE):
        return False
    if not re.search(retrigger_re, body, re.IGNORECASE):
        return False
    if watermark is not None:
        # Use _entry_ts (incl. submittedAt) so a decline arriving as a review object —
        # not just a comment — is still staleness-checked (FR-9.5). Fail-safe compare.
        if not _is_newer(_entry_ts(comment), watermark):
            return False
    return True


def _is_attributed_review(review: dict, watermark: Any) -> bool:
    """True when ``review`` is a genuine re-review attributed to our re-trigger (FR-9.5).

    At the S5 re-trigger poll a watermark (our re-trigger comment's timestamp) is set; a
    review is "attributed" only when it is NEWER than the watermark (a real post-re-trigger
    re-review). A ``None`` watermark (the initial poll) treats any review as attributed. A
    review carrying no timestamp cannot be attributed once a watermark is set.
    """
    if not isinstance(review, dict):
        return False
    if watermark is None:
        return True
    return _is_newer(_entry_ts(review), watermark)


def classify(payload: dict, contract: Any, *, watermark: Any = None) -> str:
    """Return the review state for ``payload`` against ``contract`` (pure).

    - Augment "abnormally large" decline present (an Augment-authored comment/review
      whose body matches BOTH decline regexes, newer than ``watermark``) →
      ``"declined"`` (FR-9.1). Checked FIRST so a decline is never miscounted as
      ``"findings"`` — EXCEPT FR-9.5: at the S5 re-trigger poll (a watermark is set), a
      genuine attributed re-review (a real review newer than the watermark) WINS over a
      co-occurring decline (the App actually reviewed), so it is classified as the review.
    - No Augment review present (empty reviews, or only a non-Augment/different
      bot author) → ``"polling"`` (T-201, T-211).
    - Augment review present, no findings → ``"clean"`` (T-202).
    - Augment review present, findings present (in the review object's
      self-signal or in Augment-authored inline comments) → ``"findings"``
      (T-203). Interleaved reviews parse only the Augment author (T-212).

    ``watermark`` (keyword-only, default ``None``) is threaded into :func:`is_decline`
    so a stale pre-watermark decline is ignored (EC-23); ``None`` accepts any decline.
    """
    augment_identities = _augment_identities(contract)
    reviews = payload.get("reviews") if isinstance(payload, dict) else None
    comments = payload.get("comments") if isinstance(payload, dict) else None

    augment_reviews = _augment_entries(reviews, augment_identities)
    augment_comments = _augment_entries(comments, augment_identities)

    # V1.1 decline check (FR-9.1) — runs BEFORE clean/findings/polling so an Augment
    # decline (which may arrive as a bare comment with no formal review) is never
    # miscounted. Scans Augment-authored comments AND reviews for a decline marker.
    decline_present = any(
        is_decline(entry, contract, watermark=watermark)
        for entry in (*augment_comments, *augment_reviews)
    )
    if decline_present:
        # FR-9.5 (review > decline): at the S5 re-trigger poll (a watermark is set) a
        # GENUINE attributed re-review — a real review newer than our re-trigger watermark
        # — WINS over a co-occurring decline (the App actually reviewed). Otherwise (the
        # initial poll where watermark is None, or no attributed review present) the
        # decline-first rule (FR-9.1) holds.
        attributed_rereview = watermark is not None and any(
            _is_attributed_review(r, watermark)
            and not is_decline(r, contract, watermark=watermark)
            for r in augment_reviews
        )
        if not attributed_rereview:
            return STATE_DECLINED
        # else: fall through — the attributed re-review wins; classify clean/findings below.

    if not augment_reviews:
        # No review detected from the Augment bot (T-201 empty / T-211 other bot).
        return STATE_POLLING

    # An Augment review exists — determine clean vs findings. Findings live either
    # in the review object's self-signal or in Augment-authored inline comments
    # (findings_locus == comments[]). Only the Augment author is parsed (T-212). A
    # decline-shaped comment is NEVER a finding (it is a decline, handled above / by
    # FR-9.5), so it is excluded from the findings-comment count.
    if any(_entry_has_findings(r) for r in augment_reviews):
        return STATE_FINDINGS
    # A finding-comment must carry inline context (path + integer line + body) — a
    # bare/summary Augment comment with no locus is NOT a finding (restores the V1.0
    # guard the V1.1 refactor dropped). This also keeps conversation/issue comments
    # (which have no path/line — e.g. the App's "Review completed" summary) from
    # being miscounted once the poller surfaces them alongside inline comments.
    finding_comments = [
        c
        for c in augment_comments
        if not is_decline(c, contract, watermark=None)
        and c.get("path")
        and isinstance(c.get("line"), int)
        and c.get("body")
    ]
    if finding_comments:
        return STATE_FINDINGS
    return STATE_CLEAN
