"""Pure, finite review classification and shared actionable-root selection.

Only the configured Augment identities supply evidence. Cosmos completion is an
observed wire format, not a prose heuristic; ambiguous/incomplete evidence polls.
Legacy injected payloads without attribution context remain supported.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

STATE_POLLING = "polling"
STATE_CLEAN = "clean"
STATE_FINDINGS = "findings"
STATE_DECLINED = "declined"

_COMPLETENESS = ("comments_ok", "reviews_ok", "threads_ok")
_MISSING = object()
_COSMOS_TOKEN = re.compile(r"cosmos[\s_-]*review[\s_-]*status", re.IGNORECASE)
_COSMOS_MARKER = re.compile(
    r"<!--\s*cosmos-review-status:v1\s+(.{1,8192}?)\s*-->", re.DOTALL
)


def _login_of(entry: dict) -> str | None:
    """Accept REST, GraphQL and legacy flattened author shapes."""
    for key in ("author", "user"):
        author = entry.get(key)
        if isinstance(author, dict) and isinstance(author.get("login"), str):
            return author["login"]
    login = entry.get("login")
    return login if isinstance(login, str) else None


def _augment_identities(contract: Any) -> set[str]:
    return {
        identity
        for identity in (
            getattr(contract, "augment_bot_login", None),
            getattr(contract, "augment_app_slug", None),
        )
        if isinstance(identity, str) and identity
    }


def _augment_entries(entries: Any, identities: set[str]) -> list[dict]:
    if not isinstance(entries, list):
        return []
    return [e for e in entries if isinstance(e, dict) and _login_of(e) in identities]


def has_augment_activity(payload: dict, contract: Any) -> bool:
    """Raw review/comment activity for silence handling, independent of completion."""
    if not isinstance(payload, dict):
        return False
    identities = _augment_identities(contract)
    return bool(
        _augment_entries(payload.get("reviews"), identities)
        or _augment_entries(payload.get("comments"), identities)
    )


def poll_succeeded(payload: dict) -> bool:
    """Missing additive flags are compatible with old injected payloads only."""
    if not isinstance(payload, dict) or not payload.get("head_sha"):
        return False
    reviews = payload.get("reviews")
    cosmos = isinstance(reviews, list) and any(
        _cosmos_shaped(r) for r in reviews if isinstance(r, dict)
    )
    return all(payload.get(key, not cosmos) is True for key in _COMPLETENESS) and (
        not cosmos or _timestamp(payload.get("observed_at")) is not None
    )


def _submission_ts(review: dict) -> Any:
    """Formal completion uses submission, never creation of a draft review."""
    return review.get("submitted_at", review.get("submittedAt"))


def _entry_ts(entry: dict) -> Any:
    # A present-but-null submission time (pending review) must not use creation.
    for key in ("submitted_at", "submittedAt", "createdAt", "created_at"):
        if key in entry:
            return entry[key]
    return None


def _timestamp(value: Any) -> datetime | None:
    """Parse aware instants; naive, malformed and arbitrary Any values fail closed."""
    try:
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if isinstance(value, datetime) and value.utcoffset() is not None:
            return value.astimezone(timezone.utc)
    except (ValueError, TypeError, OverflowError):
        pass
    return None


def _is_newer(ts: Any, watermark: Any) -> bool:
    time, boundary = _timestamp(ts), _timestamp(watermark)
    return time is not None and boundary is not None and time > boundary


def _sha(value: Any) -> str | None:
    if isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{40}", value):
        return value.lower()
    return None


def _review_commits(review: dict) -> list[Any]:
    commits = [review["commit_id"]] if "commit_id" in review else []
    if "commit" in review:
        commit = review["commit"]
        commits.append(commit.get("oid") if isinstance(commit, dict) else None)
    return commits


def _cosmos_shaped(review: dict) -> bool:
    body = review.get("body")
    if not isinstance(body, str):
        return False
    return bool(
        _COSMOS_TOKEN.search(body)
        or (
            "Deep Code Review Agent" in body
            and "https://cosmos.augmentcode.com/session" in body
        )
        or re.search(r"^#{1,6}\s+Cosmos\b", body, re.IGNORECASE | re.MULTILINE)
    )


def _json_object(pairs: list[tuple[str, Any]]) -> dict:
    """Reject duplicate keys rather than let a later head/count overwrite evidence."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate marker key")
        result[key] = value
    return result


def _cosmos_marker(review: dict) -> dict | None:
    body = review.get("body")
    if not isinstance(body, str) or len(_COSMOS_TOKEN.findall(body)) != 1:
        return None
    match = _COSMOS_MARKER.search(body)
    if not match:
        return None
    try:
        marker = json.loads(match[1], object_pairs_hook=_json_object)
    except (ValueError, RecursionError):
        return None
    if not isinstance(marker, dict):
        return None
    count, specialist = marker.get("unresolved_count"), marker.get("specialist")
    if (
        not isinstance(specialist, str)
        or not specialist.strip()
        or marker.get("status") != "reviewed"
        or not _sha(marker.get("head"))
        or not _sha(marker.get("baseline"))
        or type(count) is not int
        or count < 0
    ):
        return None
    return marker


def _entry_has_findings(review: dict) -> bool:
    count = review.get("findings_count")
    return bool(review.get("has_findings")) or (type(count) is int and count > 0)


def is_decline(comment: dict, contract: Any, *, watermark: Any = None) -> bool:
    """Legacy decline predicate; both phrases and a configured author are required."""
    if not isinstance(comment, dict) or _login_of(comment) not in _augment_identities(
        contract
    ):
        return False
    phrase = getattr(contract, "decline_phrase_regex", None)
    trigger = getattr(contract, "decline_retrigger_regex", None)
    body = comment.get("body")
    return bool(
        isinstance(body, str)
        and phrase
        and trigger
        and re.search(phrase, body, re.IGNORECASE)
        and re.search(trigger, body, re.IGNORECASE)
        and (watermark is None or _is_newer(_entry_ts(comment), watermark))
    )


def _completion_reviews(
    reviews: list[dict], expected: Any, watermark: Any, cosmos: bool, observed_at: Any
) -> tuple[list[dict], dict | None]:
    """Select latest relevant completion before validating it; never skip bad newer evidence."""
    contextual = (
        cosmos
        or expected is not _MISSING
        or watermark is not None
        or observed_at is not _MISSING
    )
    if not contextual:
        return [
            r for r in reviews if r.get("state") not in ("PENDING", "DISMISSED")
        ], None
    head = _sha(expected)
    observed = _timestamp(observed_at)
    if head is None or ((cosmos or observed_at is not _MISSING) and observed is None):
        return [], None
    candidates = []
    for review in reviews:
        marker = _cosmos_marker(review)
        commits = _review_commits(review)
        # Only unambiguously unrelated evidence can be excluded before ordering.
        if head and commits and all(_sha(c) and _sha(c) != head for c in commits):
            if not _cosmos_shaped(review) or (marker and _sha(marker["head"]) != head):
                continue
        time = _timestamp(_submission_ts(review))
        if time is None:
            return [], None
        candidates.append((time, review, marker))
    if not candidates:
        return [], None
    latest_time = max(time for time, _, _ in candidates)
    latest = [(r, m) for time, r, m in candidates if time == latest_time]
    if len(latest) != 1:
        return [], None  # Cannot order two distinct reviews at the same instant.
    review, marker = latest[0]
    if (observed is not None and latest_time > observed) or (
        watermark is not None and not _is_newer(latest_time, watermark)
    ):
        return [], None
    if review.get("state") not in ("COMMENTED", "APPROVED", "CHANGES_REQUESTED"):
        return [], None
    commits = _review_commits(review)
    if head and (any(_sha(c) != head for c in commits) or (not cosmos and not commits)):
        return [], None
    if cosmos and (marker is None or _sha(marker["head"]) != head):
        return [], None
    return [review], marker


def _stable_id(entry: dict) -> str | int | None:
    for key in ("databaseId", "id"):
        value = entry.get(key)
        if (type(value) is int and value > 0) or (
            isinstance(value, str) and value.strip()
        ):
            return value
    return None


def _thread_findings(threads: Any, contract: Any, completed: dict) -> list[dict] | None:
    """Return roots only, or None if an unresolved source cannot be safely selected.

    Current-null/original-only locations stay hints. Resolution is authoritative;
    neither outdated state nor the re-trigger watermark discards an open root.
    """
    if not isinstance(threads, list):
        return None
    identities = _augment_identities(contract)
    selected, seen_threads, seen_roots = [], set(), set()
    completed_at = _timestamp(_submission_ts(completed))
    for thread in threads:
        if not isinstance(thread, dict) or type(thread.get("isResolved")) is not bool:
            return None
        if thread["isResolved"]:
            continue
        connection = thread.get("comments")
        nodes = connection.get("nodes") if isinstance(connection, dict) else None
        if not isinstance(nodes, list) or not nodes or not isinstance(nodes[0], dict):
            return None
        root = nodes[0]
        login = _login_of(root)
        if not login:
            return None
        if login not in identities:
            continue  # A bot reply never turns a human-rooted thread into a finding.
        if root.get("replyTo") is not None or root.get("in_reply_to_id") is not None:
            return None
        if is_decline(root, contract):
            continue
        origin = root.get("pullRequestReview")
        if not isinstance(origin, dict):
            return None
        comment_id, thread_id, review_id = (
            _stable_id(root),
            _stable_id(thread),
            _stable_id(origin),
        )
        path = root.get("path", thread.get("path"))
        line = root.get("line", thread.get("line"))
        original = root.get("originalLine", thread.get("originalLine"))
        body = root.get("body")
        created = _timestamp(_entry_ts(root))
        if (
            comment_id is None
            or thread_id is None
            or review_id is None
            or type(thread.get("isOutdated")) is not bool
            or not isinstance(path, str)
            or not path.strip()
            or not isinstance(body, str)
            or not body.strip()
            or not any(type(n) is int and n > 0 for n in (line, original))
            or (line is not None and (type(line) is not int or line <= 0))
            or (original is not None and (type(original) is not int or original <= 0))
            or not _review_commits(origin)
            or any(_sha(c) is None for c in _review_commits(origin))
            or created is None
            or completed_at is None
            or created > completed_at
        ):
            return None
        if thread_id in seen_threads or comment_id in seen_roots:
            return None  # Duplicate/conflicting identities are not extra findings.
        seen_threads.add(thread_id)
        seen_roots.add(comment_id)
        selected.append(
            {
                **root,
                "body": body,
                "path": path,
                "line": line,
                "original_line": original,
                "comment_id": comment_id,
                "thread_id": thread_id,
                "review_id": review_id,
                "is_outdated": thread["isOutdated"],
                "is_resolved": False,
            }
        )
    return selected


def _selection(
    payload: dict, contract: Any, watermark: Any, current_head_sha: str | None
) -> tuple[str, list[dict]]:
    if not isinstance(payload, dict) or any(
        payload.get(key, True) is not True for key in _COMPLETENESS
    ):
        return STATE_POLLING, []
    identities = _augment_identities(contract)
    reviews = _augment_entries(payload.get("reviews"), identities)
    comments = _augment_entries(payload.get("comments"), identities)
    cosmos = any(_cosmos_shaped(r) for r in reviews)
    expected = (
        current_head_sha
        if current_head_sha is not None
        else payload.get("head_sha", _MISSING)
    )
    decline = any(
        is_decline(e, contract, watermark=watermark) for e in (*comments, *reviews)
    )
    review_candidates = [r for r in reviews if not is_decline(r, contract)]
    completed, marker = _completion_reviews(
        review_candidates,
        expected,
        watermark,
        cosmos,
        payload.get("observed_at", _MISSING),
    )
    # Initial decline-first behavior is unchanged. Only validated re-review overrides.
    if decline and not (watermark is not None and completed):
        return STATE_DECLINED, []
    if not completed:
        return STATE_POLLING, []
    if cosmos and not (
        all(payload.get(key) is True for key in _COMPLETENESS)
        and isinstance(payload.get("reviews"), list)
        and isinstance(payload.get("comments"), list)
    ):
        return STATE_POLLING, []
    if cosmos or "threads" in payload:
        findings = _thread_findings(payload.get("threads"), contract, completed[0])
        if findings is None or (marker and len(findings) < marker["unresolved_count"]):
            return STATE_POLLING, []
    else:
        findings = [
            {**c, "comment_id": _stable_id(c), "original_line": c.get("original_line")}
            for c in comments
            if not is_decline(c, contract)
            and c.get("isResolved") is not True
            and c.get("in_reply_to_id") is None
            and c.get("replyTo") is None
            and isinstance(c.get("path"), str)
            and c["path"]
            and type(c.get("line")) is int
            and c["line"] > 0
            and isinstance(c.get("body"), str)
            and c["body"]
        ]
    if findings or (not cosmos and any(_entry_has_findings(r) for r in completed)):
        return STATE_FINDINGS, findings
    return STATE_CLEAN, []


def classify(
    payload: dict,
    contract: Any,
    *,
    watermark: Any = None,
    current_head_sha: str | None = None,
) -> str:
    """Return polling/declined/clean/findings from one shared selection decision."""
    return _selection(payload, contract, watermark, current_head_sha)[0]


def actionable_finding_comments(
    payload: dict,
    contract: Any,
    *,
    watermark: Any = None,
    current_head_sha: str | None = None,
) -> list[dict]:
    """Return additive raw root dictionaries only for a validated findings outcome.

    Raw id/databaseId/pullRequestReview remain intact. Stable comment_id/thread_id/
    review_id and original_line/is_outdated feed the existing normalization seam.
    The watermark attributes completion, never historical unresolved roots.
    """
    return _selection(payload, contract, watermark, current_head_sha)[1]
