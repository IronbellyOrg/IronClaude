"""The verb ``superclaude orchestrator merge-gate``: may this pull request be merged now (design 5.3 waves 6 and 7, DQ8, ADD4, ADD5).

    merge-gate --repo <R> --pr <N> --ci <file> --reviews <file> --expected-head <sha>
               --worker-done <yes|no> --reviewers <augment,codex | augment | codex | none>
               [--files-json <file> --changed-count <n> --merge-safety <globs | none>]
               [--answer-ref <id>] [--checks-finished-at <UTC time>]

THE GATE NEVER MERGES. It judges and records. It runs one read, ``gh pr view`` (state, draft,
head, mergeability), through the guarded runner, reads the two snapshots that
``scripts/pr-snapshot.sh`` wrote and the file list of the pull request, prints ``merge_ok``
and a ``reasons`` list, and appends one ``merge-gate`` row to the action log. Wave 7 runs
``gh pr merge`` only after this verb prints ``merge_ok: true`` for the head it is about to
merge, and never for a hold.

Nothing here classifies a check or a review. The CI state is ``superclaude.pr_submit.ci.classify_checks``;
the Augment and Codex states are ``classify`` and ``classify_codex``; the wait outcomes are
``augment_wait_outcome``, ``codex_wait_outcome`` and ``merge_wait`` of ``superclaude.pr_submit``
(a test asserts these names are the core's own). The gate adds only what the core does not
decide: the thirteen closed reasons, the 60 minute stall rule (ADD4), the latest-review rule
of ``changes_requested`` and the merge-safety hold (ruling 35).

The ``reasons`` are a closed set of thirteen (``REASONS``). The exit code is 0 when
``merge_ok`` is true or the pull request is already merged, 3 for a hold (so ``gate && merge``
can never merge a hold), 2 for a bad input and 6 or 4 when the gate cannot read what it needs
to judge at all. The verdict, not the exit code, is the record.

Choices the spec leaves open (each is tested):

* A reviewer is "listed" by ``--reviewers`` (the repo's ``reviewers`` of ``repos.yaml``). One
  that shows no activity is never skipped as ``/sc:pr-submit`` skips it (ADD4 drops ``detect``):
  it is pending, and 60 minutes after the head's checks finished it is stalled.
* ``merge_wait`` outcomes: ``polling`` is ``review_pending`` (or ``review_none_present`` when no
  listed reviewer has shown any activity), ``clean`` passes, ``findings`` is ``threads_open``,
  ``declined`` is ``review_stalled`` at once (the agent said it will not review this head, so
  waiting is pointless and the orchestrator escalates), ``no_response`` is ``review_none_present``
  and ``review_stalled``, ``timeout`` is ``review_stalled`` (finding F11 of issue 665). A listed
  reviewer that is absent or incomplete never lets a ``clean`` or ``findings`` outcome pass.
* The 60 minute clock needs the time the head's checks finished. The snapshots do not hold it,
  so the orchestrator passes ``--checks-finished-at`` (the first time the gate showed no
  ``checks_pending`` for this head, kept in the state file). Without it nothing is ever stalled:
  the pull request is held as pending and the output says ``stall_clock: not_given``.
* ``changes_requested`` follows GitHub: the latest ``APPROVED``, ``CHANGES_REQUESTED`` or
  ``DISMISSED`` review of each author counts, and a later ``COMMENTED`` review does not clear a
  request (GitHub keeps it open). A review with no readable account never clears.
* A merged pull request prints ``state: merged``, ``merge_ok: false`` and no reasons (there is
  nothing to merge; never a second ``gh pr merge``). One closed without a merge prints
  ``state: closed`` and ``not_mergeable``.
* ``mergeStateStatus`` ``DIRTY`` or ``BEHIND``, or ``mergeable`` ``CONFLICTING``, is
  ``not_mergeable``. ``BLOCKED`` is ``not_mergeable`` only when no other reason explains it.
  ``UNKNOWN`` (GitHub is still computing) is ``snapshot_incomplete``: run the gate again.
* An empty check list never reads clean (``expect_checks``): a repo with no check at all stays
  ``checks_pending``.
* The merge-safety hold fails closed on a file list that is missing, not JSON, not a list of
  rows with a ``filename``, whose count is unknown, whose rows are not exactly ``--changed-count``,
  or that holds 3000 or more rows (finding F47 of issue 675). One unreadable read is re-read at
  the next gate run before it escalates (finding F44): ``merge_safety.escalate`` is true for a
  match at once and for an unreadable list only from the second run in a row for the same pull
  request and head (counted in the action log). ``--merge-safety`` absent means the default
  list; ``none`` means the list was emptied on Clay's word; an empty value is refused (an unset
  shell variable must never switch the hold off). Only a glob of ``*``, ``**`` and ``?`` is
  read; any other glob syntax is refused (exit 2) and never guessed at (finding F45).
* ``--answer-ref`` clears ONLY the merge-safety hold, and only when it is an accepted
  ``answer-check`` for the question key ``merge_safety:<PR>:<head sha>`` of this run. A ref
  checked for another key (the failing-check question included) cannot clear it, so one ref
  can never carry two OKs (finding F46). ``changes_requested`` is never cleared by any answer.
* When the head moved (the snapshot, the live head and ``--expected-head`` differ) only
  ``head_moved`` and the reasons that do not depend on a head are printed.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

import click

from superclaude.cli.issue_watch.predicates import (
    parse_utc,
    valid_issue_number,
    valid_repo,
)
from superclaude.pr_submit.ci import classify_checks
from superclaude.pr_submit.classifier import (
    STATE_CLEAN,
    STATE_DECLINED,
    STATE_FINDINGS,
    STATE_POLLING,
    augment_marker_defect,
    classify,
)
from superclaude.pr_submit.detection import DetectionContract, DetectionContractLocked
from superclaude.pr_submit.reviewers import (
    WAIT_ABSENT,
    augment_wait_outcome,
    classify_codex,
    codex_wait_outcome,
    merge_wait,
    reviewer_activity,
)

from . import actions, answer_check, common, ext
from .state import EXIT_CONFLICT, EXIT_INVALID, EXIT_UNREADABLE, StateError

REASONS: Final = (
    "checks_failing",
    "checks_pending",
    "review_pending",
    "review_stalled",
    "review_none_present",
    "threads_open",
    "worker_not_done",
    "head_moved",
    "draft",
    "not_mergeable",
    "snapshot_incomplete",
    "changes_requested",
    "merge_safety",
)
"""The closed set of thirteen reasons (5.3 wave 6)."""

EXIT_HOLD: Final = EXIT_CONFLICT
STALL_SECONDS: Final = 3600
"""A listed review agent with no activity, or not finished, this long after the checks finished is stalled."""
TRUNCATED_ROWS: Final = 3000
"""``gh api pulls/<N>/files`` stops at 3000 files, so 3000 rows or more is a cut list (F47)."""
MAX_FILE_BYTES: Final = 32 * 1024 * 1024
UNREADABLE_LINE: Final = "the file list of this pull request could not be read"
DEFAULT_MERGE_SAFETY: Final = (
    ".github/workflows/**",
    ".github/rulesets/**",
    ".github/settings.yml",
    "CODEOWNERS",
    ".github/CODEOWNERS",
    "docs/CODEOWNERS",
)
"""The list used when ``merge_safety_files`` is absent (AD-E5). Each repo adds the files its
own gate reads (for IronClaude ``.claude/settings.json`` and the hook folders) in its
``repos.yaml`` entry; the default holds only what every repo shares."""

_SHA = re.compile(r"[0-9a-f]{40}")
_GLOB_OK = re.compile(r"[A-Za-z0-9_./*?@+ ~-]{1,200}")
_DECISIVE: Final = ("APPROVED", "CHANGES_REQUESTED", "DISMISSED")
_KNOWN_REVIEWERS: Final = ("augment", "codex")
_MERGE_STATUS_OK: Final = ("CLEAN", "UNSTABLE", "HAS_HOOKS")
_MERGE_STATUS_HELD: Final = ("DIRTY", "BEHIND")


# --- the merge-safety matcher (B3b's AU7 uses these two functions) ------------------------


def parse_globs(value: str | None) -> tuple[str, ...]:
    """The list of ``--merge-safety``: absent is the default, ``none`` is empty, else comma separated.

    An empty value, an empty part, or a glob with any character outside letters, digits and
    ``_ . / * ? @ + ~ -`` and a space is ``merge_safety_globs_invalid`` (exit 2): the gate
    reads only ``*``, ``**`` and ``?`` and never guesses at brackets or braces.
    """
    if value is None:
        return DEFAULT_MERGE_SAFETY
    if value == "none":
        return ()
    parts = value.split(",")
    if not all(_GLOB_OK.fullmatch(p) and p == p.strip() for p in parts):
        raise StateError("merge_safety_globs_invalid", EXIT_INVALID)
    return tuple(parts)


def _glob_regex(pattern: str) -> re.Pattern[str]:
    out: list[str] = []
    i = 0
    while i < len(pattern):
        if pattern.startswith("**", i):
            if pattern[i + 2 : i + 3] == "/":  # "**/" is zero or more folders
                out.append("(?:.*/)?")
                i += 3
            else:
                out.append(".*")
                i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("".join(out), re.DOTALL)


def merge_safety_files(
    globs: Sequence[str], rows: Sequence[Mapping[str, Any]]
) -> list[str]:
    """The paths of ``rows`` that a glob matches: ``filename`` and ``previous_filename`` of each row.

    A rename OUT of a protected path is a match through ``previous_filename``. The result
    is sorted and holds each matched path once.
    """
    regexes = [_glob_regex(g) for g in globs]
    found: set[str] = set()
    for row in rows:
        for key in ("filename", "previous_filename"):
            path = row.get(key)
            if isinstance(path, str) and any(rx.fullmatch(path) for rx in regexes):
                found.add(path)
    return sorted(found)


def read_file_list(
    path: Path | None, changed_count: int | None
) -> tuple[list[dict[str, Any]] | None, str | None]:
    """``(rows, None)`` for a list read whole, or ``(None, problem)`` for one that cannot be trusted.

    ``problem`` is a closed token: ``missing``, ``unreadable``, ``too_large``, ``not_json``,
    ``not_a_list``, ``bad_row``, ``count_unknown``, ``short``, ``count_mismatch``,
    ``truncated``. The file is the output of ``gh api --paginate repos/<R>/pulls/<N>/files``:
    one JSON array per page, one after the other (or one array of arrays).
    """
    if path is None:
        return None, "missing"
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_FILE_BYTES + 1)
    except OSError:
        return None, "missing" if not Path(path).exists() else "unreadable"
    if len(data) > MAX_FILE_BYTES:
        return None, "too_large"
    try:
        values = ext.json_values(data.decode("utf-8"))
    except (StateError, UnicodeDecodeError):
        return None, "not_json"
    rows: list[dict[str, Any]] = []
    for value in values:
        if not isinstance(value, list):
            return None, "not_a_list"  # an error reply is an object, never a list
        for item in value:
            for row in item if isinstance(item, list) else [item]:
                if not isinstance(row, dict) or not isinstance(
                    row.get("filename"), str
                ):
                    return None, "bad_row"
                if "previous_filename" in row and not isinstance(
                    row["previous_filename"], str
                ):
                    return None, "bad_row"
                rows.append(row)
    if not values:
        return None, "not_json"
    if len(rows) >= TRUNCATED_ROWS:
        return None, "truncated"
    if changed_count is None:
        return None, "count_unknown"
    if len(rows) < changed_count:
        return None, "short"
    if len(rows) != changed_count:
        return None, "count_mismatch"
    return rows, None


# --- the snapshots ------------------------------------------------------------------------


def _read_object(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES:
            return None
        doc = json.loads(data.decode("utf-8"))
    except (OSError, ValueError, RecursionError):
        return None
    return doc if isinstance(doc, dict) else None


def _head_of(doc: Mapping[str, Any] | None) -> str | None:
    head = doc.get("head_sha") if doc is not None else None
    if isinstance(head, str) and _SHA.fullmatch(head.lower()):
        return head.lower()
    return None


def _ci_ok(doc: dict[str, Any] | None) -> bool:
    return (
        doc is not None
        and _head_of(doc) is not None
        and isinstance(doc.get("checks"), list)
    )


def _reviews_ok(doc: dict[str, Any] | None) -> bool:
    return (
        doc is not None
        and _head_of(doc) is not None
        and all(doc.get(k) is True for k in ("comments_ok", "reviews_ok", "threads_ok"))
        and all(isinstance(doc.get(k), list) for k in ("reviews", "comments", "threads"))
    )


def _open_changes(reviews: Sequence[Any]) -> list[str] | None:
    """The accounts whose latest decisive review is ``CHANGES_REQUESTED``; None when it cannot be read.

    Decisive means ``APPROVED``, ``CHANGES_REQUESTED`` or ``DISMISSED``. ``COMMENTED`` and a
    pending review never change it. Order is the submission time, then the review id.
    """
    latest: dict[str, tuple[datetime, int, str]] = {}
    for review in reviews:
        if not isinstance(review, dict):
            return None
        state = review.get("state")
        if state not in _DECISIVE:
            continue
        rid = review.get("id")
        user = review.get("user")
        login = user.get("login") if isinstance(user, dict) else None
        try:
            when = parse_utc(review.get("submitted_at"))
        except ValueError:
            return None
        if type(rid) is not int:
            return None
        # No readable account: the review stands alone, nothing by "the same author" can clear it.
        who = login if isinstance(login, str) and login else f"(unknown account {rid})"
        mark = (when, rid, state)
        if who not in latest or mark[:2] > latest[who][:2]:
            latest[who] = mark
    return sorted(who for who, mark in latest.items() if mark[2] == "CHANGES_REQUESTED")


def _outcome_reasons(
    decision: Mapping[str, Any],
    listed: Sequence[str],
    active: Mapping[str, bool],
) -> set[str]:
    """Map a ``merge_wait`` result to the review reasons (every outcome has a row, F11)."""
    outcome = decision["outcome"]
    reasons: set[str] = set()
    if outcome == STATE_POLLING:
        any_active = any(active.get(name) for name in listed)
        reasons.add("review_pending" if any_active else "review_none_present")
    elif outcome == STATE_FINDINGS:
        reasons.add("threads_open")
    elif outcome == STATE_CLEAN:
        pass
    elif outcome in (STATE_DECLINED, "timeout"):
        reasons.add("review_stalled")
    elif outcome == "no_response":
        reasons.update(("review_none_present", "review_stalled"))
    else:  # an outcome this gate does not know: hold
        reasons.add("review_pending")
    if any(name in decision["absent"] or name in decision["incomplete"] for name in listed):
        reasons.add("review_stalled")
    return reasons


def _review_reasons(
    payload: dict[str, Any], listed: Sequence[str], elapsed: float
) -> tuple[set[str], dict[str, Any]]:
    try:
        contract = DetectionContract.load()
    except DetectionContractLocked:
        raise StateError("detection_contract_unreadable", EXIT_UNREADABLE) from None
    head = _head_of(payload)
    active = reviewer_activity(payload, contract)
    stalled = elapsed >= STALL_SECONDS
    augment = (WAIT_ABSENT, STATE_POLLING)  # a reviewer that is not listed is ignored
    codex = (WAIT_ABSENT, STATE_POLLING)
    augment_state = classify(payload, contract, current_head_sha=head)
    codex_state = classify_codex(payload, contract, current_head_sha=head)
    if "augment" in listed:
        nxt = None
        if stalled:
            nxt = "TERMINAL_TIMEOUT" if active["augment"] else "TERMINAL_AUGMENT_NO_RESPONSE"
        defect = augment_marker_defect(payload, contract, current_head_sha=head)
        augment = (
            augment_wait_outcome(augment_state, nxt, marker_defect=defect),
            augment_state,
        )
    if "codex" in listed:
        codex = (
            codex_wait_outcome(
                codex_state,
                active=active["codex"],
                elapsed=int(elapsed),
                timeout=STALL_SECONDS,
                silence_timeout=STALL_SECONDS,
                other_settled=False,  # never skipped because the other reviewer finished (ADD4)
            ),
            codex_state,
        )
    decision = merge_wait(augment, codex)
    detail = {
        "augment": augment_state if "augment" in listed else None,
        "codex": codex_state if "codex" in listed else None,
        "outcome": decision["outcome"],
        "absent": [n for n in listed if n in decision["absent"]],
        "incomplete": [n for n in listed if n in decision["incomplete"]],
    }
    return _outcome_reasons(decision, listed, active), detail


# --- the merge-safety hold ----------------------------------------------------------------


def _prior_unreadable(root: Path, repo: str, pr: int, head: str) -> int:
    """How many gate runs in a row for this pull request and head found the list unreadable."""
    count = 0
    try:
        with open(actions.actions_path(root), "rb") as handle:
            for raw in handle:
                try:
                    row = json.loads(raw.decode("utf-8"))
                except (ValueError, RecursionError):
                    continue
                if (
                    isinstance(row, dict)
                    and row.get("kind") == "merge-gate"
                    and row.get("repo") == repo
                    and row.get("pr") == pr
                    and row.get("head") == head
                    and isinstance(row.get("file_list"), str)
                ):
                    count = count + 1 if row["file_list"] == "unreadable" else 0
    except OSError:
        return 0
    return count


def question_key(pr: int, head: str) -> str:
    """The question key of the merge-safety hold (5.3 wave 7): ``merge_safety:<PR>:<head sha>``."""
    return f"merge_safety:{pr}:{head}"


def _safety(
    root: Path,
    *,
    repo: str,
    pr: int,
    head: str,
    globs: Sequence[str],
    files_path: Path | None,
    changed_count: int | None,
    answer_ref: str | None,
) -> dict[str, Any]:
    """The state of the merge-safety hold: ``none``, ``clear``, ``matched``, ``unreadable`` or ``cleared_by_answer``."""
    out: dict[str, Any] = {"result": "none", "files": [], "held": False}
    if not globs:
        return out  # the list was emptied on Clay's word: no hold
    rows, problem = read_file_list(files_path, changed_count)
    if rows is None:
        out.update(result="unreadable", list_problem=problem, line=UNREADABLE_LINE)
    else:
        matched = merge_safety_files(globs, rows)
        if not matched:
            out["result"] = "clear"
            return out
        out.update(result="matched", files=matched)
    out["held"] = True
    key = question_key(pr, head)
    out["question_key"] = key
    if answer_ref is not None:
        try:
            answer_check.require_accepted(root, answer_ref, question_key=key)
        except StateError as exc:
            out["answer_ref"] = exc.reason  # the hold stays; the caller reads why
        else:
            out.update(answer_ref="accepted", held=False, was=out["result"])
            out["result"] = "cleared_by_answer"
            return out
    if out["result"] == "unreadable":
        runs = _prior_unreadable(root, repo, pr, head) + 1
        out.update(unreadable_runs=runs, escalate=runs >= 2)
    else:
        out["escalate"] = True
    return out


# --- the judgement ------------------------------------------------------------------------


def _live_view(runner: Any, repo: str, pr: int) -> dict[str, Any] | None:
    """The one read of the pull request itself; None when it cannot be read or understood."""
    argv = [
        "gh",
        "pr",
        "view",
        str(pr),
        "--repo",
        repo,
        "--json",
        "state,isDraft,headRefOid,mergeable,mergeStateStatus",
    ]
    try:
        doc = json.loads(ext.run_checked(runner, argv))
    except (StateError, ValueError, RecursionError):
        return None
    if (
        not isinstance(doc, dict)
        or doc.get("state") not in ("OPEN", "CLOSED", "MERGED")
        or type(doc.get("isDraft")) is not bool
    ):
        return None
    if doc["state"] == "OPEN" and not (
        isinstance(doc.get("headRefOid"), str)
        and _SHA.fullmatch(doc["headRefOid"].lower())
        and isinstance(doc.get("mergeable"), str)
        and isinstance(doc.get("mergeStateStatus"), str)
    ):
        return None
    return doc


def gate(
    root: Path,
    *,
    repo: str,
    pr: int,
    ci_path: Path | None,
    reviews_path: Path | None,
    expected_head: str,
    worker_done: bool,
    reviewers: Sequence[str],
    files_path: Path | None = None,
    changed_count: int | None = None,
    globs: Sequence[str] = DEFAULT_MERGE_SAFETY,
    answer_ref: str | None = None,
    checks_finished_at: datetime | None = None,
    now: datetime | None = None,
    runner: Any = None,
) -> dict[str, Any]:
    """Judge one pull request and record the verdict; the result holds ``merge_ok`` and ``reasons``."""
    now = now if now is not None else datetime.now(timezone.utc)
    runner = runner if runner is not None else ext.make_runner("merge-gate")
    view = _live_view(runner, repo, pr)
    result: dict[str, Any] = {
        "repo": repo,
        "pr": pr,
        "head": expected_head,
        "state": "unknown",
        "merge_ok": False,
        "reasons": [],
    }
    reasons: set[str] = set()
    safety: dict[str, Any] | None = None

    if view is not None and view["state"] == "MERGED":
        result["state"] = "merged"
    elif view is not None and view["state"] == "CLOSED":
        result.update(state="closed")
        reasons.add("not_mergeable")
    else:
        result["state"] = "open" if view is not None else "unknown"
        ci = _read_object(ci_path)
        snap = _read_object(reviews_path)
        ci_ok, snap_ok = _ci_ok(ci), _reviews_ok(snap)
        heads = {
            h
            for h in (
                _head_of(ci) if ci_ok else None,
                _head_of(snap) if snap_ok else None,
                view["headRefOid"].lower() if view is not None else None,
            )
            if h is not None
        }
        if view is None or not ci_ok or not snap_ok:
            reasons.add("snapshot_incomplete")
        moved = bool(heads - {expected_head})
        if moved:
            reasons.add("head_moved")
        if not worker_done:
            reasons.add("worker_not_done")
        if view is not None:
            if view["isDraft"] or view["mergeStateStatus"] == "DRAFT":
                reasons.add("draft")
            if view["mergeable"] == "CONFLICTING" or (
                view["mergeStateStatus"] in _MERGE_STATUS_HELD
            ):
                reasons.add("not_mergeable")
            elif view["mergeable"] != "MERGEABLE" or (
                view["mergeStateStatus"] not in (*_MERGE_STATUS_OK, "BLOCKED", "DRAFT")
            ):
                # UNKNOWN (GitHub is still computing), an empty read or a value this
                # gate has never seen: run the gate again, never merge on a guess.
                reasons.add("snapshot_incomplete")
        if snap_ok:
            assert snap is not None
            held = _open_changes(snap["reviews"])
            if held is None:
                reasons.add("snapshot_incomplete")
            elif held:
                reasons.add("changes_requested")
                result["changes_requested_by"] = held
        checks_done = False
        if not moved:
            if ci_ok:
                assert ci is not None
                state = classify_checks(ci, wait_sha=expected_head, expect_checks=True)
                result["checks"] = state
                checks_done = state != STATE_POLLING
                if state == STATE_FINDINGS:
                    reasons.add("checks_failing")
                elif state == STATE_POLLING:
                    reasons.add("checks_pending")
            if snap_ok:
                assert snap is not None
                if any(
                    not isinstance(t, dict) or t.get("isResolved") is not True
                    for t in snap["threads"]
                ):
                    reasons.add("threads_open")
                if reviewers:
                    elapsed = 0.0
                    if checks_done and checks_finished_at is not None:
                        elapsed = max(0.0, (now - checks_finished_at).total_seconds())
                    result["stall_clock"] = (
                        "not_given"
                        if checks_done and checks_finished_at is None
                        else ("running" if checks_done else "not_started")
                    )
                    found, detail = _review_reasons(snap, reviewers, elapsed)
                    reasons |= found
                    result["reviews"] = detail
            safety = _safety(
                root,
                repo=repo,
                pr=pr,
                head=expected_head,
                globs=globs,
                files_path=files_path,
                changed_count=changed_count,
                answer_ref=answer_ref,
            )
            result["merge_safety"] = safety
            if safety["held"]:
                reasons.add("merge_safety")
        if view is not None and view["mergeStateStatus"] == "BLOCKED" and not reasons:
            reasons.add("not_mergeable")  # blocked and nothing above explains it

    result["reasons"] = [r for r in REASONS if r in reasons]
    result["merge_ok"] = result["state"] == "open" and not reasons
    # The one reason an OK of Clay's can cover is a failing check, and only when it is the only one.
    result["waivable"] = result["reasons"] == ["checks_failing"]
    result["ref"] = actions.append(
        root,
        "merge-gate",
        now=now,
        repo=repo,
        pr=pr,
        head=expected_head,
        state=result["state"],
        merge_ok=result["merge_ok"],
        reasons=result["reasons"],
        **({"file_list": safety["result"]} if safety is not None else {}),
        **({"answer_ref": answer_ref} if safety and "answer_ref" in safety else {}),
    )
    return result


# --- the verb -----------------------------------------------------------------------------


def _int(value: str | None, field: str, *, minimum: int = 0) -> int | None:
    if value is None:
        return None
    if re.fullmatch(r"[0-9]{1,9}", value) is None or int(value) < minimum:
        raise StateError("invalid_input", EXIT_INVALID, field=field)
    return int(value)


def _reviewers(value: str) -> tuple[str, ...]:
    if value == "none":
        return ()
    names = value.split(",")
    if (
        not names
        or len(set(names)) != len(names)
        or any(n not in _KNOWN_REVIEWERS for n in names)
    ):
        raise StateError("invalid_input", EXIT_INVALID, field="reviewers")
    return tuple(names)


@click.command("merge-gate")
@click.option("--repo", required=True, help="owner/name of the pull request's repo.")
@click.option("--pr", required=True, help="The pull request number.")
@click.option(
    "--ci",
    "ci_path",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="The CI snapshot that pr-snapshot.sh wrote (ci.json).",
)
@click.option(
    "--reviews",
    "reviews_path",
    required=True,
    type=click.Path(dir_okay=False, path_type=Path),
    help="The review snapshot that pr-snapshot.sh wrote (reviews.json).",
)
@click.option("--expected-head", required=True, help="The full head sha to be merged.")
@click.option(
    "--worker-done",
    required=True,
    type=click.Choice(["yes", "no"]),
    help="Whether a valid worker_done for the active Task and Dispatch is in.",
)
@click.option(
    "--reviewers",
    required=True,
    help="The repo's reviewers from repos.yaml: augment, codex, augment,codex or none.",
)
@click.option(
    "--files-json",
    "files_path",
    type=click.Path(dir_okay=False, path_type=Path),
    default=None,
    help="gh api --paginate repos/<R>/pulls/<N>/files, saved to a file.",
)
@click.option("--changed-count", default=None, help="changedFiles of the pull request.")
@click.option(
    "--merge-safety",
    default=None,
    help="Comma separated globs of merge_safety_files, or none; absent means the default list.",
)
@click.option(
    "--answer-ref",
    default=None,
    help="The id of an answer-check for the question key merge_safety:<PR>:<head sha>.",
)
@click.option(
    "--checks-finished-at",
    default=None,
    help="UTC time the head's checks finished (starts the 60 minute review clock).",
)
def merge_gate_cmd(
    repo,
    pr,
    ci_path,
    reviews_path,
    expected_head,
    worker_done,
    reviewers,
    files_path,
    changed_count,
    merge_safety,
    answer_ref,
    checks_finished_at,
) -> None:
    """Say whether this pull request may be merged now; it never merges."""
    verdict: dict[str, Any] = {}

    def action() -> dict[str, Any]:
        number = _int(pr, "pr", minimum=1)
        if not valid_repo(repo) or number is None or not valid_issue_number(number):
            raise StateError("invalid_input", EXIT_INVALID)
        head = expected_head.lower()
        if _SHA.fullmatch(head) is None:
            raise StateError("invalid_input", EXIT_INVALID, field="expected_head")
        try:
            finished = (
                parse_utc(checks_finished_at) if checks_finished_at is not None else None
            )
        except ValueError:
            raise StateError("invalid_input", EXIT_INVALID, field="checks_finished_at") from None
        result = gate(
            common.root(),
            repo=repo,
            pr=number,
            ci_path=ci_path,
            reviews_path=reviews_path,
            expected_head=head,
            worker_done=worker_done == "yes",
            reviewers=_reviewers(reviewers),
            files_path=files_path,
            changed_count=_int(changed_count, "changed_count"),
            globs=parse_globs(merge_safety),
            answer_ref=answer_ref,
            checks_finished_at=finished,
        )
        verdict.update(result)
        return result

    common.run(action)
    if not verdict["merge_ok"] and verdict["state"] != "merged":
        click.get_current_context().exit(EXIT_HOLD)


__all__ = [
    "DEFAULT_MERGE_SAFETY",
    "REASONS",
    "gate",
    "merge_gate_cmd",
    "merge_safety_files",
    "parse_globs",
    "question_key",
    "read_file_list",
]
