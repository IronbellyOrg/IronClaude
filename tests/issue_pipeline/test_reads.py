"""Task 5: the GitHub reads that turn comment text into booleans."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from superclaude.cli.issue_pipeline import reads
from superclaude.cli.issue_watch import github as gh
from superclaude.cli.issue_watch.runner import CommandResult

RECORDED = Path(__file__).parent / "fixtures" / "recorded"
CANARY = "CANARY-9f3a-DO-NOT-LEAK"
H = "a" * 64
RID = "ap-9-plan-" + H[:12]
LONG = f"approved {RID} plan-sha256={H}"

pytestmark = pytest.mark.skipif(shutil.which("jq") is None, reason="jq is needed to run the projection")


def jq(program: str, document: object) -> str:
    done = subprocess.run(["jq", "-c", program], input=json.dumps(document), capture_output=True, text=True, check=True)
    return done.stdout


def project(bodies: list[str | None]) -> list[dict]:
    raw = [
        {"id": i + 1, "user": {"login": "u", "id": 5, "type": "User"}, "created_at": "2026-11-16T10:00:00Z", "body": b}
        for i, b in enumerate(bodies)
    ]
    return json.loads(jq(reads.COMMENTS_JQ, raw))


def ok(stdout: str) -> CommandResult:
    return CommandResult(("gh",), 0, stdout, "", False, None, 0.0)


def failed(stderr: str = "HTTP 502: Bad Gateway") -> CommandResult:
    return CommandResult(("gh",), 1, "", stderr, False, None, 0.0)


class Served:
    """A runner that answers each call from ``answer(argv)`` and keeps every argv and reply."""

    def __init__(self, answer) -> None:
        self.answer = answer
        self.argvs: list[list[str]] = []
        self.replies: list[CommandResult] = []

    def run(self, argv, timeout, *, cwd=None) -> CommandResult:
        self.argvs.append(list(argv))
        reply = self.answer(list(argv))
        self.replies.append(reply)
        return reply


def never_expires() -> float:
    return 30.0


# --- the projection over the recorded file -------------------------------------


def test_projection_over_the_recorded_comments_has_every_field_with_its_type() -> None:
    raw = json.loads((RECORDED / "comments-page1.json").read_text())
    rows = json.loads(jq(reads.COMMENTS_JQ, raw))
    assert len(rows) == len(raw) > 0
    for row in rows:
        assert isinstance(row["id"], int) and isinstance(row["user_id"], int)
        assert isinstance(row["login"], str) and isinstance(row["user_type"], str)
        assert isinstance(row["created_at"], str) and isinstance(row["matches_approval_line"], bool)
        assert row["approval_form"] is None and row["approval_record_id"] is None and row["approval_hash"] is None
        assert row["plan_marker_record_id"] is None and row["plan_marker_hash"] is None
    facts = [reads._comment_fact(row) for row in rows]  # Python re-validates every row
    assert [f.id for f in facts] == [c["id"] for c in raw]


# --- the exact forms -----------------------------------------------------------


def test_matches_approval_line_only_for_the_two_exact_forms() -> None:
    bodies = ["approved", LONG, "approved\n", "approved ", " approved", "> approved", f"> {LONG}", "I approved this", LONG + "\n", LONG + " x", "Approved", None]
    rows = project(bodies)
    assert [r["matches_approval_line"] for r in rows] == [True, True] + [False] * 10
    assert rows[0]["approval_form"] == "short" and rows[1]["approval_form"] == "long"
    assert rows[1]["approval_record_id"] == RID and rows[1]["approval_hash"] == H
    assert all(r["approval_record_id"] is None for i, r in enumerate(rows) if i != 1)


def test_the_plan_marker_is_read_with_its_hash() -> None:
    rows = project([f"intro\n<!-- sc:stage:plan id={RID} plan={H} -->\nmore", "<!-- sc:stage:plan id=bad plan=x -->"])
    assert (rows[0]["plan_marker_record_id"], rows[0]["plan_marker_hash"]) == (RID, H)
    assert rows[1]["plan_marker_record_id"] is None


# --- no text ------------------------------------------------------------------


def test_the_new_argv_asks_for_no_body_field() -> None:
    argv = reads.argv_comments_projected(452, 1)
    assert argv[:5] == ["gh", "api", "--method", "GET", "repos/IronbellyOrg/IronClaude/issues/452/comments"]
    for banned in ("--json", "--template", "-t", "bodyText", "bodyHTML"):
        assert banned not in argv
    assert "body:" not in reads.COMMENTS_JQ.replace(" ", "")  # no output key named body
    keys = set(project(["x"])[0])
    assert not keys & {"body", "title", "text", "message"}


def test_a_hostile_body_never_reaches_output_argv_result_or_a_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    hostile = [
        f"{CANARY} <script>alert(1)</script> [x](javascript:y)",
        CANARY * 5000 + "\n" + LONG,
        f"<!-- sc:stage:plan id={RID} plan={H} -->{CANARY}",
        "‮" + CANARY,
    ]
    raw = [
        {"id": i + 1, "user": {"login": "u", "id": 5, "type": "User"}, "created_at": "2026-11-16T10:00:00Z", "body": b}
        for i, b in enumerate(hostile)
    ]
    projected = jq(reads.COMMENTS_JQ, raw)
    assert CANARY not in projected
    runner = Served(lambda argv: ok(projected))
    out = reads.comments(runner, gh.CallBudget(), 452, never_expires)
    assert out.reason is None and len(out.value) == 4
    assert CANARY not in repr(out) and CANARY not in " ".join(" ".join(a) for a in runner.argvs)
    assert all(CANARY not in r.stdout + r.stderr for r in runner.replies)
    assert list(tmp_path.iterdir()) == []  # nothing was written


@pytest.mark.parametrize("field", ["approval_hash", "approval_record_id", "plan_marker_hash", "login", "user_type"])
def test_python_rejects_a_captured_value_that_breaks_its_pattern(field: str) -> None:
    row = project([LONG])[0]
    row[field] = "not valid\n" if field in ("login", "user_type") else "ZZ" + CANARY
    if field == "plan_marker_hash":
        row["plan_marker_record_id"] = RID
    with pytest.raises(gh._Malformed):
        reads._comment_fact(row)
    served = Served(lambda argv: ok(json.dumps([row])))
    result = reads.comments(served, gh.CallBudget(), 9, never_expires)
    assert result.value is None and result.reason == "comments_unreadable"


# --- budget, page cap, failure --------------------------------------------------


def _page(n_items: int, offset: int = 0) -> str:
    return json.dumps([{"id": offset + i + 1, "login": "u", "user_id": 5, "user_type": "User", "created_at": "2026-11-16T10:00:00Z",
                        "matches_approval_line": False, "approval_form": None, "approval_record_id": None, "approval_hash": None,
                        "plan_marker_record_id": None, "plan_marker_hash": None} for i in range(n_items)])


def test_page_cap_stops_a_comment_read_that_never_ends() -> None:
    # every page is full with fresh ids, so only the page cap ends the read: incomplete, never partial
    def answer(argv: list[str]) -> CommandResult:
        page = int(next(a for a in argv if a.startswith("page=")).split("=")[1])
        return ok(_page(gh.PAGE_SIZE, offset=page * 1000))

    runner = Served(answer)
    result = reads.comments(runner, gh.CallBudget(), 9, never_expires)
    assert result.value is None and result.reason == "comments_unreadable"
    assert len(runner.argvs) == gh.PAGE_CAP


def test_call_cap_is_shared_across_events_comments_and_edits() -> None:
    budget = gh.CallBudget()
    budget.calls = gh.CALL_CAP - gh.RESERVED_CALLS - 2  # room for two per-issue calls only
    recorded = {"events": _recorded_events(), "comments": _page(1)}

    def answer(argv: list[str]) -> CommandResult:
        return ok(recorded["events"] if argv[4].endswith("/events") else recorded["comments"])

    runner = Served(answer)
    out = reads.read_stage_evidence(runner, 452, never_expires, budget)
    assert out.value is None and out.reason == "budget_exhausted"
    assert budget.calls <= gh.CALL_CAP - gh.RESERVED_CALLS
    assert len(runner.argvs) == 2  # the third read never ran


def _recorded_events() -> str:
    return jq(gh.EVENTS_JQ, json.loads((RECORDED / "events-page1.json").read_text()))


def test_a_transient_gh_failure_returns_a_closed_reason_not_a_partial_approval() -> None:
    def answer(argv: list[str]) -> CommandResult:
        if argv[4].endswith("/events"):
            return ok(_recorded_events())
        return failed()

    out = reads.read_stage_evidence(Served(answer), 452, never_expires)
    assert out.value is None and out.reason == "comments_unreadable"
    first = reads.read_stage_evidence(Served(lambda argv: failed()), 452, never_expires)
    assert first.value is None and first.reason == "events_unreadable"


def test_the_whole_read_over_the_recorded_files_succeeds() -> None:
    raw_comments = json.loads((RECORDED / "comments-page1.json").read_text())
    edits = (RECORDED / "edits-page1.json").read_text()

    def answer(argv: list[str]) -> CommandResult:
        if argv[:3] == ["gh", "api", "graphql"]:
            return ok(edits)
        if argv[4].endswith("/events"):
            return ok(_recorded_events())
        assert argv[4].endswith("/comments")
        return ok(jq(reads.COMMENTS_JQ, raw_comments))

    out = reads.read_stage_evidence(Served(answer), 452, never_expires)
    assert out.reason is None
    evidence = out.value
    assert len(evidence.comments) == len(raw_comments) and evidence.events and evidence.edits.comments
