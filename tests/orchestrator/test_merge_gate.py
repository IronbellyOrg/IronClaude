"""``merge-gate`` (5.3 waves 6 and 7): the thirteen closed reasons, the hard refusals, the merge-safety hold.

The gate never merges: every case runs the real click verb against a fake ``gh`` that answers
the one read the gate makes (``gh pr view``) and records every argv. The review snapshots are
built from the live-poll fixtures of ``tests/pr_submit/fixtures`` (an Augment review that is
clean, an Augment review with an open thread, a Codex summary that is clean), so the core
classifiers decide on real shapes.
"""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import stat
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.issue_watch.predicates import format_utc
from superclaude.cli.orchestrator import actions, answer_check, ext, merge_gate
from superclaude.cli.orchestrator.group import orchestrator_group
from superclaude.cli.orchestrator.state import StateError
from superclaude.pr_submit import ci as core_ci
from superclaude.pr_submit import reviewers as core_reviewers

from .fake_world import ENTRY, REPO, _result, asked, call

FIXTURES = Path(__file__).parents[1] / "pr_submit" / "fixtures"
HEAD = "029a45179d78667bb50ec53185d47cde85451bf8"
OLD_HEAD = "7c3f4304a52cdb351ef93f1ab2d6f13922bec6a6"
PR = 77
NOW = datetime.now(timezone.utc)
CODEX = "chatgpt-codex-connector[bot]"
AUGMENT = "augmentcode[bot]"
SKILL = Path(__file__).parents[2] / "src" / "superclaude" / "skills"
SNAPSHOT_SH = SKILL / "sc-orchestrator-protocol" / "scripts" / "pr-snapshot.sh"


def fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


# --- the fake gh ----------------------------------------------------------------------------


class Gh:
    """Answers ``gh pr view`` and records every argv; anything else is an unexpected call."""

    def __init__(self, **view: Any) -> None:
        self.view: dict[str, Any] | None = {
            "state": "OPEN",
            "isDraft": False,
            "headRefOid": HEAD,
            "mergeable": "MERGEABLE",
            "mergeStateStatus": "CLEAN",
            **view,
        }
        self.fail = False
        self.raw: str | None = None
        self.calls: list[tuple[str, ...]] = []

    def run(self, argv: list[str], timeout: float, *, cwd: str | None = None):
        key = tuple(argv)
        self.calls.append(key)
        if key[:3] == ("gh", "pr", "view") and not self.fail:
            return _result(self.raw if self.raw is not None else json.dumps(self.view))
        return _result(returncode=1, stderr="fake: no")


# --- snapshots --------------------------------------------------------------------------------


def ci_snapshot(bucket: str = "pass", head: str = HEAD, checks: list | None = None):
    rows = (
        checks
        if checks is not None
        else [
            {
                "name": "test",
                "state": "SUCCESS" if bucket == "pass" else bucket.upper(),
                "bucket": bucket,
                "link": "https://github.com/o/r/actions/runs/5/job/1",
                "workflow": "CI",
            }
        ]
    )
    return {
        "pr": PR,
        "head_sha": head,
        "source": "ci",
        "state": "clean",
        "checks": rows,
        "merge_state": {"mergeable": "MERGEABLE", "status": "CLEAN"},
    }


def snap(reviews=(), comments=(), threads=(), head: str = HEAD) -> dict:
    return {
        "pr": PR,
        "head_sha": head,
        "observed_at": "2026-11-08T18:31:00Z",
        "state": "review_present",
        "comments_ok": True,
        "reviews_ok": True,
        "threads_ok": True,
        "reviews": list(reviews),
        "comments": list(comments),
        "threads": list(threads),
    }


def _augment_clean() -> dict:
    return fixture("cosmos-pr455-malformed-then-good.json")


def _codex_comments() -> list[dict]:
    cdx = fixture("codex-clean-pr334.json")
    cdx = json.loads(json.dumps(cdx).replace(cdx["head_sha"], HEAD))
    return [c for c in cdx["comments"] if c["user"]["login"] == CODEX]


def augment_clean() -> dict:
    return snap(reviews=_augment_clean()["reviews"])


def codex_clean() -> dict:
    return snap(comments=_codex_comments())


def both_clean() -> dict:
    return snap(reviews=_augment_clean()["reviews"], comments=_codex_comments())


def augment_findings() -> dict:
    """An Augment review of the head with one open Augment thread (``findings``)."""
    doc = fixture("cosmos-pr337.json")
    doc["head_sha"] = doc["head_sha"]
    return doc


def human_thread(resolved: bool = False) -> dict:
    return {
        "id": "PRRT_h1",
        "path": "a.py",
        "line": 3,
        "originalLine": 3,
        "isResolved": resolved,
        "isOutdated": False,
        "comments": {"nodes": [{"databaseId": 5, "author": {"login": "clayphi"}}]},
    }


def working_comment(login: str = AUGMENT) -> dict:
    """A comment by a review agent that is not a finished review (activity, no completion)."""
    return {
        "id": 9,
        "user": {"login": login},
        "body": "Looking at this now.",
        "created_at": "2026-11-08T18:20:00Z",
    }


def decline_comment() -> dict:
    return {
        "id": 10,
        "user": {"login": AUGMENT},
        "body": "This pull request is abnormally large. Comment `augment review` to ask again.",
        "created_at": "2026-11-08T18:20:00Z",
    }


def review(login: str | None, state: str, rid: int, at: str, head: str = HEAD) -> dict:
    return {
        "id": rid,
        "user": {"login": login} if login is not None else None,
        "state": state,
        "submitted_at": at,
        "commit_id": head,
        "body": "x",
    }


# --- running the verb ---------------------------------------------------------------------------

DEFAULT_FILES: Any = object()


@dataclass
class Out:
    code: int
    out: dict
    gh: Gh
    root: Path


def minutes_ago(n: float) -> str:
    return format_utc(NOW - timedelta(minutes=n))


def run_gate(
    tmp_path: Path,
    monkeypatch,
    *,
    view: dict | None = None,
    ci: Any = None,
    reviews: Any = None,
    files: Any = DEFAULT_FILES,
    count: str | None = "1",
    merge_safety: str | None = None,
    reviewers: str = "augment,codex",
    worker_done: str = "yes",
    answer_ref: str | None = None,
    finished: str | None = None,
    head: str = HEAD,
    gh: Gh | None = None,
    extra: tuple[str, ...] = (),
    root: Path | None = None,
) -> Out:
    root = root or (tmp_path / "orch")
    root.mkdir(exist_ok=True)
    snaps = tmp_path / "snap"
    snaps.mkdir(exist_ok=True)
    gh = gh or Gh(**(view or {}))
    monkeypatch.setattr(ext, "inner_runner", lambda: gh)

    def put(name: str, value: Any) -> Path:
        path = snaps / name
        if value is not None:
            path.write_text(value if isinstance(value, str) else json.dumps(value))
        return path

    ci_value = ci_snapshot() if ci is None else ci
    reviews_value = both_clean() if reviews is None else reviews
    args = [
        "merge-gate",
        "--repo",
        REPO,
        "--pr",
        str(PR),
        "--ci",
        str(put("ci.json", None if ci is False else ci_value)),
        "--reviews",
        str(put("reviews.json", None if reviews is False else reviews_value)),
        "--expected-head",
        head,
        "--worker-done",
        worker_done,
        "--reviewers",
        reviewers,
    ]
    if files is DEFAULT_FILES:
        files = [{"filename": "src/a.py", "status": "modified"}]
    if files is not None:
        args += ["--files-json", str(put("files.json", files))]
    if count is not None:
        args += ["--changed-count", count]
    if merge_safety is not None:
        args += ["--merge-safety", merge_safety]
    if answer_ref is not None:
        args += ["--answer-ref", answer_ref]
    if finished is not None:
        args += ["--checks-finished-at", finished]
    code, out = call(root, *args, *extra)
    return Out(code, out, gh, root)


def log_rows(root: Path) -> list[dict]:
    path = actions.actions_path(root)
    return [json.loads(line) for line in path.read_text().splitlines()]


# --- the clean case and the exit code -------------------------------------------------------------


def test_the_clean_case_passes_and_the_gate_only_reads(tmp_path, monkeypatch):
    r = run_gate(tmp_path, monkeypatch)
    assert r.code == 0, r.out
    assert r.out["merge_ok"] is True and r.out["reasons"] == []
    assert r.out["state"] == "open" and r.out["head"] == HEAD
    assert r.out["checks"] == "clean"
    assert r.out["reviews"]["outcome"] == "clean"
    # the only call is one read of the pull request, pinned to the repo
    assert r.gh.calls == [
        (
            "gh",
            "pr",
            "view",
            str(PR),
            "--repo",
            REPO,
            "--json",
            "state,isDraft,headRefOid,mergeable,mergeStateStatus",
        )
    ]


def test_the_closed_set_holds_thirteen_names():
    assert merge_gate.REASONS == (
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
    assert len(set(merge_gate.REASONS)) == 13


def test_a_hold_exits_3_so_a_chained_merge_never_runs(tmp_path, monkeypatch):
    r = run_gate(tmp_path, monkeypatch, worker_done="no")
    assert r.code == 3 and r.out["merge_ok"] is False
    assert r.out["ok"] is True  # the verb judged; the verdict is merge_ok


# --- one failing case for each of the thirteen reasons ------------------------------------------------

STALLED = minutes_ago(61)

FAILING: dict[str, tuple[dict, list[str]]] = {
    "checks_failing": ({"ci": ci_snapshot("fail")}, ["checks_failing"]),
    "checks_pending": ({"ci": ci_snapshot("pending")}, ["checks_pending"]),
    "review_pending": (
        {"reviews": snap(comments=[working_comment()]), "reviewers": "augment"},
        ["review_pending"],
    ),
    "review_stalled": (
        {
            "reviews": snap(comments=[working_comment()]),
            "reviewers": "augment",
            "finished": STALLED,
        },
        ["review_stalled"],
    ),
    "review_none_present": ({"reviews": snap()}, ["review_none_present"]),
    "threads_open": (
        {"reviews": snap(threads=[human_thread()] ).copy() | {
            "reviews": _augment_clean()["reviews"],
            "comments": _codex_comments(),
        }},
        ["threads_open"],
    ),
    "worker_not_done": ({"worker_done": "no"}, ["worker_not_done"]),
    "head_moved": ({"view": {"headRefOid": OLD_HEAD}}, ["head_moved"]),
    "draft": (
        {"view": {"isDraft": True, "mergeStateStatus": "DRAFT"}},
        ["draft"],
    ),
    "not_mergeable": (
        {"view": {"mergeable": "CONFLICTING", "mergeStateStatus": "DIRTY"}},
        ["not_mergeable"],
    ),
    "snapshot_incomplete": ({"ci": False}, ["snapshot_incomplete"]),
    "changes_requested": (
        {
            "reviews": snap(
                reviews=[
                    *_augment_clean()["reviews"],
                    review("clayphi", "CHANGES_REQUESTED", 9001, "2026-11-08T19:00:00Z"),
                ],
                comments=_codex_comments(),
            )
        },
        ["changes_requested"],
    ),
    "merge_safety": (
        {"files": [{"filename": ".github/workflows/ci.yml"}]},
        ["merge_safety"],
    ),
}


def test_every_reason_of_the_closed_set_has_a_failing_case():
    assert set(FAILING) == set(merge_gate.REASONS)


@pytest.mark.parametrize("reason", sorted(FAILING))
def test_a_failing_case_for_each_reason(tmp_path, monkeypatch, reason):
    kwargs, expected = FAILING[reason]
    r = run_gate(tmp_path, monkeypatch, **copy.deepcopy(kwargs))
    assert r.out["reasons"] == expected, r.out
    assert r.out["merge_ok"] is False and r.code == 3
    assert reason in r.out["reasons"]


# --- merge_wait outcomes: every one has a reason or a pass (finding F11) ------------------------


@pytest.mark.parametrize(
    ("case", "kwargs", "outcome", "expected"),
    [
        (
            "polling, a reviewer is working",
            {"reviews": snap(comments=[working_comment()]), "reviewers": "augment"},
            "polling",
            ["review_pending"],
        ),
        (
            "polling, nobody has shown up",
            {"reviews": snap()},
            "polling",
            ["review_none_present"],
        ),
        ("clean", {}, "clean", []),
        (
            "findings",
            {"reviews": augment_findings(), "reviewers": "augment", "ci": ci_snapshot(head="da6557a13b3a542cbda62957e19e8de95f40a35d"),
             "head": "da6557a13b3a542cbda62957e19e8de95f40a35d", "view": {"headRefOid": "da6557a13b3a542cbda62957e19e8de95f40a35d"}},
            "findings",
            ["threads_open"],
        ),
        (
            "declined",
            {"reviews": snap(comments=[decline_comment()]), "reviewers": "augment"},
            "declined",
            ["review_stalled"],
        ),
        (
            "no_response, both listed reviewers silent for an hour",
            {"reviews": snap(), "finished": STALLED},
            "no_response",
            ["review_stalled", "review_none_present"],
        ),
        (
            "timeout, one started and never finished, one silent",
            {"reviews": snap(comments=[working_comment()]), "finished": STALLED},
            "timeout",
            ["review_stalled"],
        ),
    ],
    ids=lambda v: v if isinstance(v, str) and " " in v else None,
)
def test_each_merge_wait_outcome_maps_to_a_reason_or_a_pass(
    tmp_path, monkeypatch, case, kwargs, outcome, expected
):
    r = run_gate(tmp_path, monkeypatch, **copy.deepcopy(kwargs))
    assert r.out["reviews"]["outcome"] == outcome, r.out
    assert sorted(r.out["reasons"]) == sorted(expected), (case, r.out)
    assert r.out["merge_ok"] is (not expected)


def test_a_listed_reviewer_that_is_silent_is_never_skipped(tmp_path, monkeypatch):
    # Augment finished clean, Codex (listed) never showed up: /sc:pr-submit would skip it,
    # the gate holds (ADD4: the detect value is dropped).
    r = run_gate(tmp_path, monkeypatch, reviews=augment_clean())
    assert r.out["merge_ok"] is False and r.out["reasons"] == ["review_pending"]
    r = run_gate(tmp_path, monkeypatch, reviews=augment_clean(), finished=STALLED)
    assert r.out["reasons"] == ["review_stalled"]
    assert r.out["reviews"]["absent"] == ["codex"]


def test_an_unlisted_reviewer_is_not_waited_for(tmp_path, monkeypatch):
    assert run_gate(tmp_path, monkeypatch, reviews=augment_clean(), reviewers="augment").out["merge_ok"]
    assert run_gate(tmp_path, monkeypatch, reviews=codex_clean(), reviewers="codex").out["merge_ok"]


def test_reviewers_none_waits_for_no_review_agent(tmp_path, monkeypatch):
    r = run_gate(tmp_path, monkeypatch, reviews=snap(), reviewers="none")
    assert r.out["merge_ok"] is True and "reviews" not in r.out
    # but an open thread and a change request still hold
    r = run_gate(tmp_path, monkeypatch, reviews=snap(threads=[human_thread()]), reviewers="none")
    assert r.out["reasons"] == ["threads_open"]


@pytest.mark.parametrize("value", ["", "augment,augment", "claude", "augment,", "none,codex", "Augment"])
def test_a_bad_reviewers_value_is_refused(tmp_path, monkeypatch, value):
    r = run_gate(tmp_path, monkeypatch, reviewers=value)
    assert r.code == 2 and r.out["ok"] is False and r.out["reason"] == "invalid_input"


def test_the_sixty_minute_clock(tmp_path, monkeypatch):
    work = {"reviews": snap(comments=[working_comment()]), "reviewers": "augment"}
    # no time given: held as pending, the clock is said to be missing
    r = run_gate(tmp_path, monkeypatch, **work)
    assert r.out["reasons"] == ["review_pending"] and r.out["stall_clock"] == "not_given"
    # 59 minutes: still pending; 61: stalled
    r = run_gate(tmp_path, monkeypatch, finished=minutes_ago(59), **work)
    assert r.out["reasons"] == ["review_pending"] and r.out["stall_clock"] == "running"
    r = run_gate(tmp_path, monkeypatch, finished=minutes_ago(61), **work)
    assert r.out["reasons"] == ["review_stalled"]
    # the clock does not run while a check is still pending
    r = run_gate(tmp_path, monkeypatch, finished=STALLED, ci=ci_snapshot("pending"), **work)
    assert r.out["stall_clock"] == "not_started"
    assert "review_stalled" not in r.out["reasons"]


def test_a_review_with_an_unreadable_marker_is_stalled_not_clean(tmp_path, monkeypatch):
    doc = fixture("cosmos-pr455-malformed-marker.json")
    head = doc["head_sha"]
    r = run_gate(
        tmp_path,
        monkeypatch,
        reviews=doc,
        reviewers="augment",
        ci=ci_snapshot(head=head),
        head=head,
        view={"headRefOid": head},
    )
    assert r.out["reasons"] == ["review_stalled"]
    assert r.out["reviews"]["incomplete"] == ["augment"]


# --- changes_requested: a hard refusal --------------------------------------------------------------


def with_reviews(*extra: dict) -> dict:
    return snap(
        reviews=[*_augment_clean()["reviews"], *extra], comments=_codex_comments()
    )


T1, T2, T3 = "2026-11-08T19:00:00Z", "2026-11-08T19:10:00Z", "2026-11-08T19:20:00Z"


@pytest.mark.parametrize(
    ("label", "extra", "held"),
    [
        ("a human", [review("clayphi", "CHANGES_REQUESTED", 1, T1)], ["clayphi"]),
        ("a review agent", [review(CODEX, "CHANGES_REQUESTED", 1, T1)], [CODEX]),
        (
            "two reviewers, one still requesting",
            [
                review("clayphi", "CHANGES_REQUESTED", 1, T1),
                review("ana", "CHANGES_REQUESTED", 2, T1),
                review("clayphi", "APPROVED", 3, T2),
            ],
            ["ana"],
        ),
        (
            "a later comment does not clear it",
            [
                review("clayphi", "CHANGES_REQUESTED", 1, T1),
                review("clayphi", "COMMENTED", 2, T2),
            ],
            ["clayphi"],
        ),
        (
            "an account that no longer exists never clears",
            [review(None, "CHANGES_REQUESTED", 1, T1), review(None, "APPROVED", 2, T2)],
            ["(unknown account 1)"],
        ),
        (
            "a later request by the same author",
            [
                review("clayphi", "CHANGES_REQUESTED", 1, T1),
                review("clayphi", "APPROVED", 2, T2),
                review("clayphi", "CHANGES_REQUESTED", 3, T3),
            ],
            ["clayphi"],
        ),
        (
            "the later time wins over the higher id",
            [
                review("clayphi", "APPROVED", 5, T1),
                review("clayphi", "CHANGES_REQUESTED", 4, T2),
            ],
            ["clayphi"],
        ),
    ],
)
def test_an_open_change_request_holds(tmp_path, monkeypatch, label, extra, held):
    r = run_gate(tmp_path, monkeypatch, reviews=with_reviews(*extra))
    assert r.out["reasons"] == ["changes_requested"], (label, r.out)
    assert r.out["changes_requested_by"] == held
    assert r.out["merge_ok"] is False


@pytest.mark.parametrize(
    "extra",
    [
        [review("clayphi", "CHANGES_REQUESTED", 1, T1), review("clayphi", "APPROVED", 2, T2)],
        [review("clayphi", "CHANGES_REQUESTED", 1, T1), review("clayphi", "DISMISSED", 2, T2)],
        [review("clayphi", "DISMISSED", 1, T1)],
        [review("clayphi", "COMMENTED", 1, T1)],
        [review("clayphi", "PENDING", 1, T1)],
    ],
    ids=["approved after", "dismissed", "dismissed alone", "comment only", "pending"],
)
def test_a_request_the_author_withdrew_or_a_dismissal_does_not_hold(tmp_path, monkeypatch, extra):
    r = run_gate(tmp_path, monkeypatch, reviews=with_reviews(*extra))
    assert r.out["merge_ok"] is True and r.out["reasons"] == []


def test_a_decisive_review_with_no_readable_time_is_an_incomplete_snapshot(tmp_path, monkeypatch):
    bad = review("clayphi", "CHANGES_REQUESTED", 1, "yesterday")
    r = run_gate(tmp_path, monkeypatch, reviews=with_reviews(bad))
    assert "snapshot_incomplete" in r.out["reasons"] and r.out["merge_ok"] is False


# --- a recorded OK for a failing check overrides neither hard refusal --------------------------------


def failing_check_ok(root: Path) -> str:
    """Clay's recorded OK to merge over a failing check: an accepted answer for its own question key."""
    key = f"ci_failing:{PR}:{HEAD}"
    asked(root, entry="ironclaude-655.3.1", key=key, row=9)
    return answer_check.check(
        root,
        entry="ironclaude-655.3.1",
        source="session",
        answered_at="2026-11-19T10:30:00Z",
        question_key=key,
        reply_to="ironclaude-655.3.1",
    )["ref"]


def test_the_ok_for_a_failing_check_is_only_for_a_failing_check(tmp_path, monkeypatch):
    root = tmp_path / "orch"
    root.mkdir()
    ref = failing_check_ok(root)
    r = run_gate(tmp_path, monkeypatch, ci=ci_snapshot("fail"), answer_ref=ref)
    assert r.out["reasons"] == ["checks_failing"] and r.out["waivable"] is True
    # with changes_requested: still not mergeable, and not waivable
    r = run_gate(
        tmp_path,
        monkeypatch,
        ci=ci_snapshot("fail"),
        reviews=with_reviews(review("clayphi", "CHANGES_REQUESTED", 1, T1)),
        answer_ref=ref,
    )
    assert r.out["reasons"] == ["checks_failing", "changes_requested"]
    assert r.out["merge_ok"] is False and r.out["waivable"] is False
    # with a merge-safety file: the same ref is for another question and does not clear it
    r = run_gate(
        tmp_path,
        monkeypatch,
        ci=ci_snapshot("fail"),
        files=[{"filename": ".github/workflows/ci.yml"}],
        answer_ref=ref,
    )
    assert r.out["reasons"] == ["checks_failing", "merge_safety"]
    assert r.out["merge_safety"]["answer_ref"] == "answer_ref_key_mismatch"
    assert r.out["waivable"] is False


def test_no_answer_clears_changes_requested(tmp_path, monkeypatch):
    root = tmp_path / "orch"
    root.mkdir()
    key = f"merge_safety:{PR}:{HEAD}"
    asked(root, entry="ironclaude-655.7.1", key=key, row=8)
    ref = answer_check.check(
        root,
        entry="ironclaude-655.7.1",
        source="session",
        answered_at="2026-11-19T10:30:00Z",
        question_key=key,
        reply_to="ironclaude-655.7.1",
    )["ref"]
    r = run_gate(
        tmp_path,
        monkeypatch,
        reviews=with_reviews(review("clayphi", "CHANGES_REQUESTED", 1, T1)),
        files=[{"filename": ".github/workflows/ci.yml"}],
        answer_ref=ref,
    )
    assert r.out["reasons"] == ["changes_requested"]  # merge_safety cleared, the request is not
    assert r.out["merge_ok"] is False


# --- the merge-safety hold --------------------------------------------------------------------------


def ms_asked(root: Path, pr: int = PR, head: str = HEAD, entry: str = "ironclaude-655.7.1") -> str:
    """Clay's accepted answer to the merge-safety question of ``pr`` at ``head``; returns the ref."""
    key = f"merge_safety:{pr}:{head}"
    asked(root, entry=entry, key=key, row=8)
    return answer_check.check(
        root,
        entry=entry,
        source="session",
        answered_at="2026-11-19T10:30:00Z",
        question_key=key,
        reply_to=entry,
    )["ref"]


CLAUDE_LIST = (
    ".github/workflows/**,.github/rulesets/**,.github/settings.yml,CODEOWNERS,"
    ".github/CODEOWNERS,docs/CODEOWNERS,.claude/settings.json,"
    "src/superclaude/hooks/**,plugins/superclaude/hooks/**"
)


@pytest.mark.parametrize(
    ("files", "matched"),
    [
        ([{"filename": ".github/workflows/ci.yml"}], [".github/workflows/ci.yml"]),
        ([{"filename": ".github/workflows/deep/x/y.yml"}], [".github/workflows/deep/x/y.yml"]),
        ([{"filename": "CODEOWNERS"}], ["CODEOWNERS"]),
        ([{"filename": ".github/CODEOWNERS"}], [".github/CODEOWNERS"]),
        ([{"filename": ".claude/settings.json"}], [".claude/settings.json"]),
        ([{"filename": "src/superclaude/hooks/guard.sh"}], ["src/superclaude/hooks/guard.sh"]),
        (
            [
                {
                    "filename": "scripts/ci.yml",
                    "status": "renamed",
                    "previous_filename": ".github/workflows/ci.yml",
                }
            ],
            [".github/workflows/ci.yml"],
        ),
        (
            [
                {
                    "filename": ".github/workflows/new.yml",
                    "status": "renamed",
                    "previous_filename": "tools/old.yml",
                }
            ],
            [".github/workflows/new.yml"],
        ),
    ],
    ids=[
        "workflow",
        "nested workflow",
        "CODEOWNERS",
        "github CODEOWNERS",
        "claude settings",
        "hooks",
        "rename out of workflows",
        "rename into workflows",
    ],
)
def test_a_listed_file_holds_a_green_reviewed_pull_request(tmp_path, monkeypatch, files, matched):
    r = run_gate(tmp_path, monkeypatch, files=files, merge_safety=CLAUDE_LIST)
    assert r.out["reasons"] == ["merge_safety"] and r.out["merge_ok"] is False
    safety = r.out["merge_safety"]
    assert safety["result"] == "matched" and safety["files"] == matched
    assert safety["escalate"] is True
    assert safety["question_key"] == f"merge_safety:{PR}:{HEAD}"
    assert r.out["checks"] == "clean" and r.out["reviews"]["outcome"] == "clean"


@pytest.mark.parametrize(
    "files",
    [
        [{"filename": "docs/workflows.md"}],
        [{"filename": "github/workflows/ci.yml"}],
        [{"filename": "src/CODEOWNERS.md"}],
        [{"filename": "x/CODEOWNERS"}],
        [{"filename": "src/a.py"}],
        [{"filename": "src/a.py", "status": "renamed", "previous_filename": "src/b.py"}],
    ],
)
def test_other_files_do_not_hold(tmp_path, monkeypatch, files):
    r = run_gate(tmp_path, monkeypatch, files=files, merge_safety=CLAUDE_LIST)
    assert r.out["merge_ok"] is True and r.out["merge_safety"]["result"] == "clear"


def test_the_default_list_applies_when_the_key_is_absent_and_none_switches_the_hold_off(
    tmp_path, monkeypatch
):
    workflow = [{"filename": ".github/workflows/ci.yml"}]
    assert run_gate(tmp_path, monkeypatch, files=workflow).out["reasons"] == ["merge_safety"]
    # the default list holds what every repo shares, not IronClaude's own files
    assert run_gate(tmp_path, monkeypatch, files=[{"filename": ".claude/settings.json"}]).out["merge_ok"]
    r = run_gate(tmp_path, monkeypatch, files=workflow, merge_safety="none", count=None)
    assert r.out["merge_ok"] is True and r.out["merge_safety"]["result"] == "none"
    assert merge_gate.DEFAULT_MERGE_SAFETY == merge_gate.parse_globs(None)


def test_a_custom_list_replaces_the_default(tmp_path, monkeypatch):
    files = [{"filename": ".github/workflows/ci.yml"}]
    assert run_gate(tmp_path, monkeypatch, files=files, merge_safety="infra/**").out["merge_ok"]
    r = run_gate(tmp_path, monkeypatch, files=[{"filename": "infra/db/x.tf"}], merge_safety="infra/**")
    assert r.out["reasons"] == ["merge_safety"]


@pytest.mark.parametrize("value", ["", ",", "a,,b", " a", "a ,b", "[ab]", "a{b,c}", "../x", "a\nb", "!a"])
def test_a_list_the_gate_cannot_read_is_refused_never_guessed(tmp_path, monkeypatch, value):
    r = run_gate(tmp_path, monkeypatch, merge_safety=value)
    if value in ("../x",):
        return  # dots and slashes are plain characters of a path glob
    assert r.code == 2 and r.out["reason"] == "merge_safety_globs_invalid"
    assert r.gh.calls == []  # refused before anything is read


def LIST(rows: int, name: str = "src/f{}.py"):
    return [{"filename": name.format(i), "status": "modified"} for i in range(rows)]


# a list that cannot be trusted: every one holds with the one line, never "no match"
UNREADABLE: dict[str, dict] = {
    "missing, no flag": {"files": None, "count": "1"},
    "missing, no file": {"files": "__absent__", "count": "1"},
    "failed, an error reply": {"files": {"message": "Server Error"}, "count": "1"},
    "failed, a page that is an error": {"files": '[{"filename":"a"}]{"message":"x"}', "count": "2"},
    "not JSON": {"files": "<html>502</html>", "count": "1"},
    "empty file": {"files": "", "count": "1"},
    "a row with no filename": {"files": [{"status": "added"}], "count": "1"},
    "a row that is not an object": {"files": ["a.py"], "count": "1"},
    "short": {"files": LIST(2), "count": "5"},
    "more rows than the count": {"files": LIST(3), "count": "2"},
    "count unknown": {"files": LIST(1), "count": None},
    "count not a number": {"files": LIST(1), "count": "many"},
    "truncated at 3000": {"files": LIST(3000), "count": "3000"},
    "truncated at more than 3000": {"files": LIST(3001), "count": "3001"},
}


@pytest.mark.parametrize("case", sorted(UNREADABLE))
def test_a_file_list_that_cannot_be_read_holds_and_says_so(tmp_path, monkeypatch, case):
    spec = copy.deepcopy(UNREADABLE[case])
    if spec["files"] == "__absent__":
        spec["files"] = None
        extra = ("--files-json", str(tmp_path / "nowhere.json"))
    else:
        extra = ()
    if case == "count not a number":
        r = run_gate(tmp_path, monkeypatch, **spec)
        assert r.code == 2 and r.out["reason"] == "invalid_input"
        return
    r = run_gate(tmp_path, monkeypatch, extra=extra, **spec)
    assert r.out["reasons"] == ["merge_safety"] and r.out["merge_ok"] is False, r.out
    safety = r.out["merge_safety"]
    assert safety["result"] == "unreadable"
    assert safety["line"] == "the file list of this pull request could not be read"
    assert safety["files"] == []


def test_the_problem_of_each_unreadable_list_is_named():
    def problem(files, count):
        return merge_gate.read_file_list(files, count)[1]

    assert problem(None, 1) == "missing"
    assert problem(Path("/nope/none.json"), 1) == "missing"


def test_a_list_read_whole_in_pages_or_slurped_is_the_same_list(tmp_path):
    rows = LIST(5)
    pages = tmp_path / "pages.json"
    pages.write_text(json.dumps(rows[:2]) + json.dumps(rows[2:4]) + "\n" + json.dumps(rows[4:]))
    slurped = tmp_path / "slurped.json"
    slurped.write_text(json.dumps([rows[:3], rows[3:]]))
    one = tmp_path / "one.json"
    one.write_text(json.dumps(rows))
    for path in (pages, slurped, one):
        got, problem = merge_gate.read_file_list(path, 5)
        assert problem is None and [r["filename"] for r in got] == [r["filename"] for r in rows]
    # 2999 rows is the largest list that is trusted
    big = tmp_path / "big.json"
    big.write_text(json.dumps(LIST(2999)))
    assert merge_gate.read_file_list(big, 2999)[1] is None
    big.write_text(json.dumps(LIST(3000)))
    assert merge_gate.read_file_list(big, 3000)[1] == "truncated"
    empty = tmp_path / "empty.json"
    empty.write_text("[]")
    assert merge_gate.read_file_list(empty, 0) == ([], None)
    assert merge_gate.read_file_list(empty, 1)[1] == "short"


def test_a_pull_request_that_changes_nothing_listed_is_not_held_by_an_empty_list(tmp_path, monkeypatch):
    r = run_gate(tmp_path, monkeypatch, files=[], count="0")
    assert r.out["merge_ok"] is True


# the OK of Clay's that clears the hold, and the ones that do not

def test_an_accepted_answer_for_this_pull_request_and_head_clears_the_hold(tmp_path, monkeypatch):
    root = tmp_path / "orch"
    root.mkdir()
    ref = ms_asked(root)
    files = [{"filename": ".github/workflows/ci.yml"}]
    r = run_gate(tmp_path, monkeypatch, files=files, answer_ref=ref)
    assert r.code == 0 and r.out["merge_ok"] is True and r.out["reasons"] == []
    safety = r.out["merge_safety"]
    assert safety["result"] == "cleared_by_answer" and safety["was"] == "matched"
    assert safety["answer_ref"] == "accepted" and safety["held"] is False


def test_an_accepted_answer_also_clears_a_list_that_could_not_be_read(tmp_path, monkeypatch):
    root = tmp_path / "orch"
    root.mkdir()
    ref = ms_asked(root)
    r = run_gate(tmp_path, monkeypatch, files=None, answer_ref=ref)
    assert r.out["merge_ok"] is True
    assert r.out["merge_safety"]["was"] == "unreadable"


def test_answers_that_do_not_clear_the_hold(tmp_path, monkeypatch):
    root = tmp_path / "orch"
    root.mkdir()
    other_pr = ms_asked(root, pr=PR + 1, entry="ironclaude-655.7.2")
    older_head = ms_asked(root, head=OLD_HEAD, entry="ironclaude-655.7.3")
    failing = failing_check_ok(root)
    asked(root, entry="ironclaude-655.7.4", key=f"merge_safety:{PR}:{HEAD}", row=8)
    refused = answer_check.check(
        root,
        entry="ironclaude-655.7.4",
        source="session",
        answered_at="2026-11-19T09:00:00Z",  # older than the question: refused
        question_key=f"merge_safety:{PR}:{HEAD}",
        reply_to="ironclaude-655.7.4",
    )
    assert refused["accepted"] is False
    files = [{"filename": ".github/workflows/ci.yml"}]
    cases = {
        "another pull request": (other_pr, "answer_ref_key_mismatch"),
        "an older head": (older_head, "answer_ref_key_mismatch"),
        "the failing-check question": (failing, "answer_ref_key_mismatch"),
        "an unaccepted answer": (refused["ref"], "answer_ref_rejected"),
        "a ref that was never made": ("a-20261119T000000Z-deadbeef", "answer_ref_unknown"),
        "text that is no ref": ("yes, merge it", "answer_ref_unknown"),
    }
    for label, (ref, why) in cases.items():
        r = run_gate(tmp_path, monkeypatch, files=files, answer_ref=ref)
        assert r.out["reasons"] == ["merge_safety"], label
        assert r.out["merge_safety"]["answer_ref"] == why, label
        assert r.out["merge_ok"] is False, label


def test_a_new_push_is_a_new_question(tmp_path, monkeypatch):
    root = tmp_path / "orch"
    root.mkdir()
    ref = ms_asked(root, head=OLD_HEAD)
    files = [{"filename": ".github/workflows/ci.yml"}]
    r = run_gate(tmp_path, monkeypatch, files=files, answer_ref=ref)
    assert r.out["reasons"] == ["merge_safety"]
    assert r.out["merge_safety"]["question_key"] == f"merge_safety:{PR}:{HEAD}"


def test_one_ref_cannot_carry_two_oks(tmp_path, monkeypatch):
    # An answer is recorded for exactly one question key, so the ref of the failing-check
    # OK is refused by the hold and the ref of the hold is not the failing-check OK (F46).
    root = tmp_path / "orch"
    root.mkdir()
    hold = ms_asked(root)
    failing = failing_check_ok(root)
    rows = {r["id"]: r for r in log_rows_of(root)}
    assert rows[hold]["question_key"] == f"merge_safety:{PR}:{HEAD}"
    assert rows[failing]["question_key"] == f"ci_failing:{PR}:{HEAD}"
    assert rows[hold]["question_key"] != rows[failing]["question_key"]


def log_rows_of(root: Path) -> list[dict]:
    return log_rows(root)


def test_a_ref_given_for_a_clear_list_changes_nothing(tmp_path, monkeypatch):
    root = tmp_path / "orch"
    root.mkdir()
    ref = ms_asked(root)
    r = run_gate(tmp_path, monkeypatch, answer_ref=ref)
    assert r.out["merge_ok"] is True and r.out["merge_safety"]["result"] == "clear"
    assert "answer_ref" not in r.out["merge_safety"]


# one failed read is re-read at the next run before it escalates (finding F44)

def test_one_unreadable_list_does_not_escalate_but_the_second_in_a_row_does(tmp_path, monkeypatch):
    first = run_gate(tmp_path, monkeypatch, files=None)
    assert first.out["merge_safety"]["unreadable_runs"] == 1
    assert first.out["merge_safety"]["escalate"] is False
    assert first.out["reasons"] == ["merge_safety"]
    second = run_gate(tmp_path, monkeypatch, files=None)
    assert second.out["merge_safety"]["unreadable_runs"] == 2
    assert second.out["merge_safety"]["escalate"] is True
    # a readable run starts the count again
    ok = run_gate(tmp_path, monkeypatch)
    assert ok.out["merge_ok"] is True
    again = run_gate(tmp_path, monkeypatch, files=None)
    assert again.out["merge_safety"]["unreadable_runs"] == 1
    assert again.out["merge_safety"]["escalate"] is False


def test_the_unreadable_count_is_for_one_pull_request_and_head(tmp_path, monkeypatch):
    run_gate(tmp_path, monkeypatch, files=None)
    other = run_gate(
        tmp_path,
        monkeypatch,
        files=None,
        head=OLD_HEAD,
        view={"headRefOid": OLD_HEAD},
        ci=ci_snapshot(head=OLD_HEAD),
        reviews=snap(head=OLD_HEAD),
    )
    assert other.out["merge_safety"]["unreadable_runs"] == 1


def test_a_match_escalates_at_once(tmp_path, monkeypatch):
    r = run_gate(tmp_path, monkeypatch, files=[{"filename": "CODEOWNERS"}])
    assert r.out["merge_safety"]["escalate"] is True


# --- the other facts of the pull request ------------------------------------------------------------


def test_a_merged_pull_request_prints_merged_and_no_reasons(tmp_path, monkeypatch):
    r = run_gate(tmp_path, monkeypatch, view={"state": "MERGED"}, ci=False, reviews=False, files=None)
    assert r.code == 0
    assert r.out["state"] == "merged" and r.out["reasons"] == []
    assert r.out["merge_ok"] is False  # nothing to merge: never a second gh pr merge


def test_a_pull_request_closed_without_a_merge_is_not_mergeable(tmp_path, monkeypatch):
    r = run_gate(tmp_path, monkeypatch, view={"state": "CLOSED"}, ci=False, reviews=False, files=None)
    assert r.code == 3 and r.out["state"] == "closed" and r.out["reasons"] == ["not_mergeable"]


def test_a_failed_read_of_the_pull_request_is_an_incomplete_snapshot(tmp_path, monkeypatch):
    gh = Gh()
    gh.fail = True
    r = run_gate(tmp_path, monkeypatch, gh=gh)
    assert r.out["state"] == "unknown" and r.out["merge_ok"] is False
    assert "snapshot_incomplete" in r.out["reasons"]


@pytest.mark.parametrize(
    "raw",
    [
        "not json",
        "[]",
        json.dumps({"state": "WEIRD", "isDraft": False}),
        json.dumps({"state": "OPEN", "isDraft": "no", "headRefOid": HEAD}),
        json.dumps({"state": "OPEN", "isDraft": False, "headRefOid": "abc", "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN"}),
        json.dumps({"state": "OPEN", "isDraft": False, "headRefOid": HEAD}),
    ],
)
def test_a_read_of_the_pull_request_that_cannot_be_understood_holds(tmp_path, monkeypatch, raw):
    gh = Gh()
    gh.raw = raw
    r = run_gate(tmp_path, monkeypatch, gh=gh)
    assert r.out["merge_ok"] is False and "snapshot_incomplete" in r.out["reasons"]


@pytest.mark.parametrize(
    ("view", "reasons"),
    [
        ({"mergeable": "CONFLICTING", "mergeStateStatus": "DIRTY"}, ["not_mergeable"]),
        ({"mergeable": "MERGEABLE", "mergeStateStatus": "BEHIND"}, ["not_mergeable"]),
        ({"mergeable": "CONFLICTING", "mergeStateStatus": "CLEAN"}, ["not_mergeable"]),
        ({"mergeStateStatus": "BLOCKED"}, ["not_mergeable"]),
        ({"mergeable": "UNKNOWN", "mergeStateStatus": "UNKNOWN"}, ["snapshot_incomplete"]),
        ({"mergeable": "", "mergeStateStatus": ""}, ["snapshot_incomplete"]),
        ({"mergeStateStatus": "SOMETHING_NEW"}, ["snapshot_incomplete"]),
        ({"mergeStateStatus": "UNSTABLE"}, []),
        ({"mergeStateStatus": "HAS_HOOKS"}, []),
    ],
)
def test_mergeability(tmp_path, monkeypatch, view, reasons):
    r = run_gate(tmp_path, monkeypatch, view=view)
    assert r.out["reasons"] == reasons


def test_blocked_is_not_a_reason_of_its_own_when_something_explains_it(tmp_path, monkeypatch):
    r = run_gate(tmp_path, monkeypatch, view={"mergeStateStatus": "BLOCKED"}, ci=ci_snapshot("fail"))
    assert r.out["reasons"] == ["checks_failing"]


@pytest.mark.parametrize("where", ["ci", "reviews", "live"])
def test_a_head_that_moved_is_head_moved_and_nothing_judged_on_the_old_head(tmp_path, monkeypatch, where):
    kwargs: dict[str, Any] = {
        "files": [{"filename": ".github/workflows/ci.yml"}],
        "ci": ci_snapshot("fail"),
    }
    if where == "ci":
        kwargs["ci"] = ci_snapshot("fail", head=OLD_HEAD)
    elif where == "reviews":
        kwargs["reviews"] = snap(head=OLD_HEAD)
    else:
        kwargs["view"] = {"headRefOid": OLD_HEAD}
    r = run_gate(tmp_path, monkeypatch, **kwargs)
    assert r.out["reasons"] == ["head_moved"]
    assert "merge_safety" not in r.out and "reviews" not in r.out
    # the head given is itself checked: the snapshots belong to another head
    r = run_gate(tmp_path, monkeypatch, head=OLD_HEAD)
    assert r.out["reasons"] == ["head_moved"]


@pytest.mark.parametrize(
    "case",
    [
        "no ci file",
        "no reviews file",
        "ci is not json",
        "ci is a list",
        "ci head empty (a failed poll)",
        "ci head is not a sha",
        "ci checks missing",
        "reviews head null",
        "comments_ok false",
        "reviews_ok false",
        "threads_ok false",
        "threads missing",
    ],
)
def test_an_incomplete_snapshot_holds_and_judges_nothing_it_cannot_see(tmp_path, monkeypatch, case):
    ci, rv = ci_snapshot(), both_clean()
    if case == "no ci file":
        ci = False
    elif case == "no reviews file":
        rv = False
    elif case == "ci is not json":
        ci = "{oops"
    elif case == "ci is a list":
        ci = "[]"
    elif case == "ci head empty (a failed poll)":
        ci = {**ci, "head_sha": "", "checks": [], "state": "polling"}
    elif case == "ci head is not a sha":
        ci = {**ci, "head_sha": "main"}
    elif case == "ci checks missing":
        ci = {k: v for k, v in ci.items() if k != "checks"}
    elif case == "reviews head null":
        rv = {**rv, "head_sha": None}
    elif case.endswith("false"):
        rv = {**rv, case.split()[0]: False}
    else:
        rv = {k: v for k, v in rv.items() if k != "threads"}
    r = run_gate(tmp_path, monkeypatch, ci=ci, reviews=rv)
    assert r.out["reasons"] == ["snapshot_incomplete"] or (
        "snapshot_incomplete" in r.out["reasons"]
    )
    assert r.out["merge_ok"] is False and "review_pending" not in r.out["reasons"]
    assert "head_moved" not in r.out["reasons"]


def test_an_empty_check_list_is_never_clean(tmp_path, monkeypatch):
    r = run_gate(tmp_path, monkeypatch, ci=ci_snapshot(checks=[]))
    assert r.out["reasons"] == ["checks_pending"]


@pytest.mark.parametrize("bucket", ["cancel"])
def test_a_cancelled_check_is_failing(tmp_path, monkeypatch, bucket):
    assert run_gate(tmp_path, monkeypatch, ci=ci_snapshot(bucket)).out["reasons"] == ["checks_failing"]


def test_a_resolved_thread_does_not_hold_and_an_unresolved_one_does(tmp_path, monkeypatch):
    clean = both_clean()
    resolved = {**clean, "threads": [human_thread(resolved=True)]}
    assert run_gate(tmp_path, monkeypatch, reviews=resolved).out["merge_ok"] is True
    open_ = {**clean, "threads": [human_thread(resolved=True), human_thread()]}
    assert run_gate(tmp_path, monkeypatch, reviews=open_).out["reasons"] == ["threads_open"]
    junk = {**clean, "threads": ["x"]}
    assert run_gate(tmp_path, monkeypatch, reviews=junk).out["reasons"] == ["threads_open"]


def test_worker_done_must_be_yes_or_no(tmp_path, monkeypatch):
    r = run_gate(tmp_path, monkeypatch, extra=())
    assert r.out["merge_ok"] is True
    code, out = call(tmp_path / "orch", "merge-gate", "--repo", REPO)  # missing options
    assert code != 0


@pytest.mark.parametrize(
    "args",
    [
        {"repo": "not a repo"},
        {"pr": "0"},
        {"pr": "-4"},
        {"pr": "x"},
        {"head": "abc123"},
        {"head": "G" * 40},
        {"finished": "yesterday"},
        {"count": "-1"},
    ],
)
def test_bad_input_is_refused_with_exit_2_and_no_read(tmp_path, monkeypatch, args):
    gh = Gh()
    monkeypatch.setattr(ext, "inner_runner", lambda: gh)
    root = tmp_path / "orch"
    root.mkdir()
    snaps = tmp_path / "s"
    snaps.mkdir()
    (snaps / "c.json").write_text(json.dumps(ci_snapshot()))
    (snaps / "r.json").write_text(json.dumps(both_clean()))
    argv = [
        "merge-gate",
        "--repo", args.get("repo", REPO),
        "--pr", args.get("pr", str(PR)),
        "--ci", str(snaps / "c.json"),
        "--reviews", str(snaps / "r.json"),
        "--expected-head", args.get("head", HEAD),
        "--worker-done", "yes",
        "--reviewers", "none",
    ]
    if "finished" in args:
        argv += ["--checks-finished-at", args["finished"]]
    if "count" in args:
        argv += ["--changed-count", args["count"]]
    code, out = call(root, *argv)
    assert code == 2 and out["ok"] is False and out["reason"] == "invalid_input"
    assert gh.calls == []


def test_the_expected_head_may_be_given_in_capitals(tmp_path, monkeypatch):
    assert run_gate(tmp_path, monkeypatch, head=HEAD.upper()).out["merge_ok"] is True


# --- the record ----------------------------------------------------------------------------------------


def test_every_run_writes_one_row_to_the_action_log_and_prints_its_id(tmp_path, monkeypatch):
    r = run_gate(tmp_path, monkeypatch, files=[{"filename": "CODEOWNERS"}])
    rows = [x for x in log_rows(r.root) if x["kind"] == "merge-gate"]
    assert len(rows) == 1 and rows[0]["id"] == r.out["ref"]
    row = rows[0]
    assert (row["repo"], row["pr"], row["head"]) == (REPO, PR, HEAD)
    assert row["merge_ok"] is False and row["reasons"] == ["merge_safety"]
    assert row["file_list"] == "matched" and row["state"] == "open"
    assert stat.S_IMODE(actions.actions_path(r.root).stat().st_mode) == 0o600
    run_gate(tmp_path, monkeypatch)
    assert len([x for x in log_rows(r.root) if x["kind"] == "merge-gate"]) == 2


def test_the_row_names_a_ref_that_was_passed_and_no_answer_text(tmp_path, monkeypatch):
    root = tmp_path / "orch"
    root.mkdir()
    ref = ms_asked(root)
    run_gate(tmp_path, monkeypatch, files=[{"filename": "CODEOWNERS"}], answer_ref=ref)
    row = [x for x in log_rows(root) if x["kind"] == "merge-gate"][-1]
    assert row["answer_ref"] == ref and row["file_list"] == "cleared_by_answer"


# --- the gate never merges and holds no copy of the core --------------------------------------------------


def test_the_gate_makes_no_call_except_the_one_read_of_the_pull_request(tmp_path, monkeypatch):
    for kwargs in (
        {},
        {"worker_done": "no"},
        {"files": [{"filename": "CODEOWNERS"}]},
        {"view": {"state": "MERGED"}},
        {"view": {"state": "CLOSED"}},
        {"ci": ci_snapshot("fail")},
    ):
        r = run_gate(tmp_path, monkeypatch, **kwargs)
        assert all(c[:3] == ("gh", "pr", "view") for c in r.gh.calls), r.gh.calls
        assert len(r.gh.calls) == 1


def test_the_gate_text_holds_no_merge_command():
    text = Path(merge_gate.__file__).read_text(encoding="utf-8")
    code = re.sub(r'""".*?"""', "", text, flags=re.DOTALL)
    for forbidden in ("pr merge", '"merge"', "--admin", "--auto", "--delete-branch", "subprocess"):
        assert forbidden not in code, forbidden


def test_the_gate_imports_the_core_and_holds_no_copy_of_its_classification():
    assert merge_gate.classify_checks is core_ci.classify_checks
    assert merge_gate.merge_wait is core_reviewers.merge_wait
    assert merge_gate.augment_wait_outcome is core_reviewers.augment_wait_outcome
    assert merge_gate.codex_wait_outcome is core_reviewers.codex_wait_outcome
    assert merge_gate.classify_codex is core_reviewers.classify_codex
    from superclaude.pr_submit import classifier

    assert merge_gate.classify is classifier.classify
    text = Path(merge_gate.__file__).read_text(encoding="utf-8")
    code = re.sub(r'""".*?"""', "", text, flags=re.DOTALL)
    assert re.search(r"from superclaude\.pr_submit\.ci import classify_checks", code)
    # no check bucket, no review marker, no Augment or Codex identity is read here
    for forbidden in ("bucket", "action_required", "cosmos", "codex-review-state", "augmentcode", "chatgpt"):
        assert forbidden not in code, forbidden
    assert not re.search(r"^def (classify|poll|decline|completion)", code, re.MULTILINE)


def test_the_verb_is_in_the_group():
    assert orchestrator_group.commands["merge-gate"] is merge_gate.merge_gate_cmd


# --- the matcher that B3b shares ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("glob", "path", "hit"),
    [
        (".github/workflows/**", ".github/workflows/ci.yml", True),
        (".github/workflows/**", ".github/workflows/a/b/c.yml", True),
        (".github/workflows/**", ".github/workflows", False),
        (".github/workflows/**", ".github/workflow/ci.yml", False),
        (".github/workflows/**", "x/.github/workflows/ci.yml", False),
        ("**/CODEOWNERS", "CODEOWNERS", True),
        ("**/CODEOWNERS", "a/b/CODEOWNERS", True),
        ("**/CODEOWNERS", "a/CODEOWNERS.md", False),
        ("*.yml", "ci.yml", True),
        ("*.yml", "a/ci.yml", False),
        ("a/*/c", "a/b/c", True),
        ("a/*/c", "a/b/d/c", False),
        ("a?c", "abc", True),
        ("a?c", "a/c", False),
        ("a.b", "aXb", False),
        ("CODEOWNERS", "codeowners", False),
        ("docs/**/x.md", "docs/x.md", True),
        ("docs/**/x.md", "docs/a/b/x.md", True),
    ],
)
def test_the_glob_matcher(glob, path, hit):
    assert bool(merge_gate.merge_safety_files([glob], [{"filename": path}])) is hit


def test_the_matcher_reads_both_names_and_lists_each_path_once():
    rows = [
        {"filename": "a/x.yml", "previous_filename": ".github/workflows/x.yml"},
        {"filename": ".github/workflows/x.yml", "previous_filename": ".github/workflows/x.yml"},
        {"filename": "b.py", "previous_filename": 5},
    ]
    assert merge_gate.merge_safety_files([".github/workflows/**"], rows) == [
        ".github/workflows/x.yml"
    ]
    assert merge_gate.merge_safety_files([], rows) == []


def test_parse_globs():
    assert merge_gate.parse_globs("a/**,b") == ("a/**", "b")
    assert merge_gate.parse_globs("none") == ()
    with pytest.raises(StateError) as exc:
        merge_gate.parse_globs("")
    assert exc.value.reason == "merge_safety_globs_invalid"


# --- pr-snapshot.sh -------------------------------------------------------------------------------------------

POLL_OK = """#!/usr/bin/env bash
printf '{"stub":"%s","args":"%s"}\\n' "$(basename "$0")" "$*"
"""


def stub_home(tmp_path: Path, ci: str = POLL_OK, review: str = POLL_OK) -> Path:
    scripts = tmp_path / "home" / ".claude" / "skills" / "sc-pr-submit-protocol" / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "poll-ci-checks.sh").write_text(ci)
    (scripts / "poll-augment-review.sh").write_text(review)
    return tmp_path / "home"


def snapshot(tmp_path: Path, home: Path, *args: str, cwd: Path | None = None):
    env = {"PATH": os.environ["PATH"], "HOME": str(home)}
    return subprocess.run(
        ["bash", str(SNAPSHOT_SH), *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd or tmp_path),
        check=False,
    )


def test_the_snapshot_script_exists_and_is_executable():
    assert SNAPSHOT_SH.is_file() and os.access(SNAPSHOT_SH, os.X_OK)
    assert SNAPSHOT_SH.read_text().startswith("#!/usr/bin/env bash\n")


def test_the_snapshot_script_runs_the_two_poll_scripts_and_saves_their_json(tmp_path):
    home = stub_home(tmp_path)
    out = tmp_path / "out"
    done = snapshot(tmp_path, home, "--pr", "12", "--repo", "o/r", "--out", str(out))
    assert done.returncode == 0, done.stderr
    ci = json.loads((out / "ci.json").read_text())
    reviews = json.loads((out / "reviews.json").read_text())
    assert ci == {"stub": "poll-ci-checks.sh", "args": "--pr 12 --repo o/r"}
    assert reviews == {"stub": "poll-augment-review.sh", "args": "--pr 12 --repo o/r"}
    assert stat.S_IMODE((out / "ci.json").stat().st_mode) == 0o600
    assert stat.S_IMODE(out.stat().st_mode) == 0o700
    assert done.stdout.splitlines() == [f"ci={out}/ci.json", f"reviews={out}/reviews.json"]
    assert sorted(p.name for p in out.iterdir()) == ["ci.json", "reviews.json"]  # no temporary file left


def test_the_snapshot_script_leaves_no_file_for_a_poll_that_failed(tmp_path):
    home = stub_home(tmp_path, ci="#!/usr/bin/env bash\necho half\nexit 2\n")
    out = tmp_path / "out"
    out.mkdir()
    (out / "ci.json").write_text("{}")  # an older snapshot must not survive a failed one
    done = snapshot(tmp_path, home, "--pr", "12", "--repo", "o/r", "--out", str(out))
    assert done.returncode == 2
    assert list(out.iterdir()) == []


def test_the_snapshot_script_falls_back_to_the_project_copy(tmp_path):
    repo = tmp_path / "checkout"
    scripts = repo / ".claude" / "skills" / "sc-pr-submit-protocol" / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "poll-ci-checks.sh").write_text(POLL_OK)
    (scripts / "poll-augment-review.sh").write_text(POLL_OK)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    empty_home = tmp_path / "nohome"
    empty_home.mkdir()
    done = snapshot(tmp_path, empty_home, "--pr", "3", "--repo", "o/r", "--out", str(tmp_path / "o"), cwd=repo)
    assert done.returncode == 0, done.stderr


def test_the_snapshot_script_stops_when_the_poll_scripts_are_not_installed(tmp_path):
    empty_home = tmp_path / "nohome"
    empty_home.mkdir()
    done = snapshot(tmp_path, empty_home, "--pr", "3", "--repo", "o/r", "--out", str(tmp_path / "o"))
    assert done.returncode == 2 and "not installed" in done.stderr
    assert not (tmp_path / "o").exists()


@pytest.mark.parametrize(
    "args",
    [
        [],
        ["--repo", "o/r", "--out", "X"],
        ["--pr", "12", "--out", "X"],
        ["--pr", "12", "--repo", "o/r"],
        ["--pr", "0", "--repo", "o/r", "--out", "X"],
        ["--pr", "1; rm -rf /", "--repo", "o/r", "--out", "X"],
        ["--pr", "12", "--repo", "not-a-repo", "--out", "X"],
        ["--pr", "12", "--repo", "o/r;ls", "--out", "X"],
        ["--pr", "12", "--repo", "o/r", "--out", "X", "--extra"],
    ],
)
def test_the_snapshot_script_refuses_bad_arguments(tmp_path, args):
    home = stub_home(tmp_path)
    args = [str(tmp_path / "out") if a == "X" else a for a in args]
    done = snapshot(tmp_path, home, *args)
    assert done.returncode == 2
    assert not (tmp_path / "out").exists()


def test_the_snapshot_script_has_no_decision_logic():
    text = SNAPSHOT_SH.read_text()
    code = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
    for forbidden in ("jq", "gh ", "merge", "classify", "grep", "sed ", "awk"):
        assert forbidden not in code, forbidden


@pytest.mark.skipif(shutil.which("shellcheck") is None, reason="shellcheck is not installed")
def test_the_snapshot_script_passes_shellcheck():
    done = subprocess.run(["shellcheck", str(SNAPSHOT_SH)], capture_output=True, text=True)
    assert done.returncode == 0, done.stdout


def test_the_snapshot_files_are_what_the_gate_reads(tmp_path, monkeypatch):
    """The two files the script writes are the two the gate takes (``ci.json`` and ``reviews.json``)."""
    text = SNAPSHOT_SH.read_text()
    assert "ci.json" in text and "reviews.json" in text
