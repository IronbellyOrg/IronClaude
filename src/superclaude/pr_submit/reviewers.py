"""Reviewer adapters for the ``sc:pr-submit`` core: Augment and Codex.

One reviewer-agnostic path with a small per-reviewer adapter: who the author is,
how completion is proven, how severity is read, and which comment asks for a
re-review. Everything after a normalized ``Finding`` is shared. Values come from
the detection contract, so a local override can change or blank them; an empty
identity set disables that reviewer.

Core purity (NFR-6): pure functions over an already-fetched snapshot; no shell or
version-control command tokens.
"""

from __future__ import annotations

import json
import re
from typing import Any

from .classifier import (
    _COMPLETENESS,
    STATE_CLEAN,
    STATE_DECLINED,
    STATE_FINDINGS,
    STATE_POLLING,
    _augment_entries,
    _augment_identities,
    _is_newer,
    _json_object,
    _login_of,
    _review_commits,
    _sha,
    _submission_ts,
    _thread_findings,
    _timestamp,
    has_augment_activity,
    has_reviewer_activity,
)
from .models import EventType
from .severity_router import finding_from_comment, remap_severity

REVIEWERS = ("augment", "codex")

_CODEX_HINTS = {"P0": "critical", "P1": "high", "P2": "medium", "P3": "low"}
_BADGE = re.compile(r"!\[P(\d) Badge\]\(https://img\.shields\.io/badge/P(\d)-[^)\s]*\)")


def reviewer_identities(contract: Any, reviewer: str) -> set[str]:
    """The non-empty author identities of ``reviewer`` (empty set = disabled)."""
    if reviewer == "augment":
        return _augment_identities(contract)
    if reviewer == "codex":
        return {
            identity
            for identity in (
                getattr(contract, "codex_bot_login", None),
                getattr(contract, "codex_app_slug", None),
            )
            if isinstance(identity, str) and identity
        }
    raise ValueError(f"unknown reviewer: {reviewer!r}")


def retrigger_phrase(contract: Any, reviewer: str) -> str:
    """The comment body that asks ``reviewer`` for a re-review."""
    if reviewer == "augment":
        phrases = getattr(contract, "accepted_trigger_phrases", None) or []
        return phrases[0] if phrases else "auggie review"
    if reviewer == "codex":
        return getattr(contract, "codex_retrigger_phrase", None) or "@codex review"
    raise ValueError(f"unknown reviewer: {reviewer!r}")


def reviewer_activity(payload: dict, contract: Any) -> dict[str, bool]:
    """Presence per reviewer. Augment keeps its silence predicate unchanged."""
    return {
        "augment": has_augment_activity(payload, contract),
        "codex": has_reviewer_activity(payload, reviewer_identities(contract, "codex")),
    }


def parse_codex_priority(body: Any) -> str | None:
    """``"P0".."P3"`` from the one Codex badge on the first non-blank line, else None.

    The body must hold exactly one ``![P<n> Badge](https://img.shields.io/badge/P<m>-...)``
    image with ``n == m`` in 0-3, on the first non-blank line. Colour is ignored.
    """
    if not isinstance(body, str):
        return None
    badges = _BADGE.findall(body)
    if len(badges) != 1:
        return None
    alt, url = badges[0]
    if alt != url or alt not in "0123":
        return None
    first = next((line for line in body.splitlines() if line.strip()), "")
    if not _BADGE.search(first):
        return None
    return f"P{alt}"


def codex_severity_hint(priority: str | None) -> str | None:
    """Map a Codex priority onto the existing severity hints (P0 critical .. P3 low)."""
    return _CODEX_HINTS.get(priority) if isinstance(priority, str) else None


_CODEX_TOKEN = "codex-review-state:v1"
_CODEX_MARKER = re.compile(
    r"<!--\s*codex-review-state:v1\s+(.{1,8192}?)\s*-->", re.DOTALL
)
_COMPLETED_REVIEW_STATES = ("COMMENTED", "APPROVED", "CHANGES_REQUESTED")


def _codex_marker(comment: dict) -> dict | None:
    """Parse the one bounded ``codex-review-state:v1`` marker; None when invalid."""
    body = comment.get("body")
    if not isinstance(body, str) or body.count(_CODEX_TOKEN) != 1:
        return None
    match = _CODEX_MARKER.search(body)
    if not match:
        return None
    try:
        marker = json.loads(match[1], object_pairs_hook=_json_object)
    except (ValueError, RecursionError):
        return None
    review = marker.get("code_review") if isinstance(marker, dict) else None
    if (
        not isinstance(review, dict)
        or not isinstance(review.get("status"), str)
        or _sha(review.get("commit_sha")) is None
        or type(review.get("has_any_findings")) is not bool
    ):
        return None
    return review


def _comment_updated_at(comment: dict) -> Any:
    """The summary comment's update time (REST or GraphQL shape); missing -> None."""
    return comment.get("updated_at", comment.get("updatedAt"))


def codex_review_state(
    payload: dict,
    contract: Any,
    *,
    watermark: Any = None,
    current_head_sha: str | None = None,
) -> dict | None:
    """The completed Codex code review of the expected head, or None (keep polling).

    Evidence is the Codex summary comment's ``codex-review-state:v1`` marker. The
    newest valid marker wins; two markers with the same latest time are ambiguous.
    Completion time is the later of that comment's ``updated_at`` and the newest
    Codex formal review submitted for the head (design section 18, A1/A3). It must
    be no later than ``observed_at`` and, with a watermark, strictly newer than it.
    """
    if not isinstance(payload, dict):
        return None
    identities = reviewer_identities(contract, "codex")
    head = _sha(
        current_head_sha if current_head_sha is not None else payload.get("head_sha")
    )
    observed = _timestamp(payload.get("observed_at"))
    if not identities or head is None or observed is None:
        return None
    candidates = []
    for comment in _augment_entries(payload.get("comments"), identities):
        body = comment.get("body")
        if not isinstance(body, str) or _CODEX_TOKEN not in body:
            continue
        updated = _timestamp(_comment_updated_at(comment))
        if updated is None:
            return None  # an unordered candidate could be the newest: keep polling
        candidates.append((updated, _codex_marker(comment)))
    if not candidates:
        return None
    # The newest marker decides (A3). An older malformed marker is superseded;
    # a newest marker that is malformed, or a tie at the newest time, polls.
    latest = max(updated for updated, _ in candidates)
    newest = [marker for updated, marker in candidates if updated == latest]
    if len(newest) != 1 or newest[0] is None:
        return None
    marker = newest[0]
    if marker["status"] != "completed" or _sha(marker["commit_sha"]) != head:
        return None
    review_times, head_reviews = [], []
    for review in _augment_entries(payload.get("reviews"), identities):
        if review.get("state") not in _COMPLETED_REVIEW_STATES:
            continue
        if not any(_sha(commit) == head for commit in _review_commits(review)):
            continue
        submitted = _timestamp(_submission_ts(review))
        if submitted is None:
            return None
        review_times.append(submitted)
        head_reviews.append(review)
    completed_at = max([latest, *review_times])
    if completed_at > observed:
        return None
    if watermark is not None and not _is_newer(completed_at, watermark):
        return None
    return {
        "completed_at": completed_at,
        "has_any_findings": marker["has_any_findings"],
        "head_review": bool(review_times),
        "head_reviews": head_reviews,
        "head_sha": head,
    }


def _codex_selection(
    payload: dict, contract: Any, watermark: Any, current_head_sha: str | None
) -> tuple[str, list[dict]]:
    if not isinstance(payload, dict) or not all(
        payload.get(key) is True for key in _COMPLETENESS
    ):
        return STATE_POLLING, []
    state = codex_review_state(
        payload, contract, watermark=watermark, current_head_sha=current_head_sha
    )
    if state is None:
        return STATE_POLLING, []
    roots = _thread_findings(
        payload.get("threads"),
        contract,
        None,
        reviewer_identities(contract, "codex"),
        completed_at=state["completed_at"],
        reviews=state["head_reviews"],
    )
    if roots is None:
        return STATE_POLLING, []
    if roots:
        selected = []
        for root in roots:
            priority = parse_codex_priority(root.get("body"))
            selected.append(
                {
                    **root,
                    "reviewer": "codex",
                    "codex_priority": priority,
                    "severity_hint": codex_severity_hint(priority),
                }
            )
        return STATE_FINDINGS, selected
    if not state["has_any_findings"] or state["head_review"]:
        return STATE_CLEAN, []
    return STATE_POLLING, []  # findings promised but not yet visible


def classify_codex(
    payload: dict,
    contract: Any,
    *,
    watermark: Any = None,
    current_head_sha: str | None = None,
) -> str:
    """Codex gate state: ``polling`` / ``clean`` / ``findings`` (never ``declined``)."""
    return _codex_selection(payload, contract, watermark, current_head_sha)[0]


def codex_finding_comments(
    payload: dict,
    contract: Any,
    *,
    watermark: Any = None,
    current_head_sha: str | None = None,
) -> list[dict]:
    """Unresolved Codex-rooted roots for a ``findings`` state, same selection rules
    as Augment, each with ``reviewer``, ``codex_priority`` and ``severity_hint``."""
    return _codex_selection(payload, contract, watermark, current_head_sha)[1]


def list_review_threads(payload: dict, contract: Any) -> list[dict]:
    """Every Augment- or Codex-rooted review thread, resolved or not, for reports."""
    threads = payload.get("threads") if isinstance(payload, dict) else None
    owners = {name: reviewer_identities(contract, name) for name in REVIEWERS}
    rows = []
    for thread in threads if isinstance(threads, list) else []:
        connection = thread.get("comments") if isinstance(thread, dict) else None
        nodes = connection.get("nodes") if isinstance(connection, dict) else None
        if not isinstance(nodes, list) or not nodes or not isinstance(nodes[0], dict):
            continue
        root = nodes[0]
        reviewer = next(
            (n for n, ids in owners.items() if _login_of(root) in ids), None
        )
        if reviewer is None:
            continue
        priority = (
            parse_codex_priority(root.get("body")) if reviewer == "codex" else None
        )
        raw = {
            "path": root.get("path", thread.get("path")),
            "line": root.get("line", thread.get("line")),
            "original_line": root.get("originalLine", thread.get("originalLine")),
            "body": root.get("body"),
            "reviewer": reviewer,
            "severity_hint": codex_severity_hint(priority),
        }
        try:
            severity = remap_severity(finding_from_comment(raw)).remapped_severity.value
        except ValueError:
            severity = None
        rows.append(
            {
                "reviewer": reviewer,
                "path": raw["path"],
                "line": raw["line"],
                "original_line": raw["original_line"],
                "is_resolved": thread.get("isResolved"),
                "priority": priority,
                "severity": severity,
                "thread_id": thread.get("id"),
                "comment_id": root.get("databaseId"),
            }
        )
    return rows


# --- per-reviewer wait outcomes and the merge (design section 6 + section 18 A2) ---

WAIT_PENDING = "pending"
WAIT_DONE = "done"
WAIT_ABSENT = "absent"
WAIT_INCOMPLETE = "incomplete"
_DONE_STATES = (STATE_CLEAN, STATE_FINDINGS, STATE_DECLINED)


def _state_name(value: Any) -> str:
    return str(getattr(value, "value", value))


def augment_wait_outcome(state: str, next_state: Any, *, absent: bool = False) -> str:
    """Augment's wait outcome from the existing gate state and ``poll_outcome`` result.

    ``absent`` (already recorded absent, or no Augment identity) is ``absent`` at
    once and is never ``pending`` (A2).
    """
    if absent:
        return WAIT_ABSENT
    if state in _DONE_STATES:
        return WAIT_DONE
    nxt = _state_name(next_state)
    if nxt == "TERMINAL_AUGMENT_NO_RESPONSE":
        return WAIT_ABSENT
    if nxt == "TERMINAL_TIMEOUT":
        return WAIT_INCOMPLETE
    return WAIT_PENDING


def codex_wait_outcome(
    state: str,
    *,
    active: bool,
    elapsed: int,
    timeout: int,
    silence_timeout: int,
    other_settled: bool,
    absent: bool = False,
) -> str:
    """Codex's wait outcome.

    ``absent`` (already recorded absent, or no Codex identity) is ``absent`` at once
    (A2). A Codex with no activity is absent as soon as Augment is settled or at the
    silence deadline; an active Codex with no completion is ``incomplete`` at
    ``--timeout``.
    """
    if absent:
        return WAIT_ABSENT
    if state in (STATE_CLEAN, STATE_FINDINGS):
        return WAIT_DONE
    if active:
        return WAIT_INCOMPLETE if elapsed >= timeout else WAIT_PENDING
    if other_settled or elapsed >= min(silence_timeout, timeout):
        return WAIT_ABSENT
    return WAIT_PENDING


def merge_wait(augment: tuple[str, str], codex: tuple[str, str]) -> dict:
    """Merge per-reviewer ``(wait_outcome, gate_state)`` pairs into one round outcome.

    ``outcome`` is ``polling`` / ``clean`` / ``findings`` / ``declined`` /
    ``no_response`` / ``timeout``; ``used`` names the reviewers whose results the
    outcome uses, ``absent`` / ``incomplete`` the others (design section 6 table).
    """
    pairs = {"augment": augment, "codex": codex}
    absent = [name for name, (out, _) in pairs.items() if out == WAIT_ABSENT]
    incomplete = [name for name, (out, _) in pairs.items() if out == WAIT_INCOMPLETE]
    done = [(name, st) for name, (out, st) in pairs.items() if out == WAIT_DONE]
    result = {
        "outcome": STATE_POLLING,
        "used": [],
        "absent": absent,
        "incomplete": incomplete,
    }
    if any(out == WAIT_PENDING for out, _ in pairs.values()):
        return result
    result["used"] = [name for name, _ in done]
    if augment == (WAIT_DONE, STATE_DECLINED):
        result["outcome"] = STATE_DECLINED
    elif done:
        findings = any(st == STATE_FINDINGS for _, st in done)
        result["outcome"] = STATE_FINDINGS if findings else STATE_CLEAN
    elif len(absent) == len(pairs):
        result["outcome"] = "no_response"
    else:
        result["outcome"] = "timeout"
    return result


# --- cross-reviewer dedup and re-trigger bookkeeping (design sections 9 and 12) ---


def dedup_groups(findings: list) -> list[list]:
    """Group findings by ``(path, line)``, using ``original_line`` when ``line`` is None.

    Input order is kept and every finding is kept: a group of two means Augment and
    Codex (or two findings) flagged the same place; each keeps its own verdict.
    """
    groups: dict[tuple, list] = {}
    for finding in findings:
        line = finding.line if finding.line is not None else finding.original_line
        groups.setdefault((finding.path, line), []).append(finding)
    return list(groups.values())


def pending_retriggers(
    events: list[dict], cycle_id: Any, present: list[str]
) -> list[str]:
    """Present reviewers with no ``rereview_requested`` for ``cycle_id`` yet.

    An event without ``reviewer`` counts as augment (logs written before Codex).
    """
    posted = {
        ev.get("reviewer") or "augment"
        for ev in events
        if isinstance(ev, dict)
        and ev.get("event_type") == EventType.REREVIEW_REQUESTED.value
        and ev.get("cycle_id") == cycle_id
    }
    return [name for name in present if name not in posted]
