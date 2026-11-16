"""Task 6: the read-only ``stage-status`` verb."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.issue_pipeline import approval_record, plan_hash, reads
from superclaude.cli.issue_pipeline import cli as cli_mod
from superclaude.cli.issue_pipeline.cli import issue_pipeline_group
from superclaude.cli.issue_watch import github as gh
from superclaude.cli.issue_watch.runner import CommandResult

pytestmark = pytest.mark.skipif(shutil.which("jq") is None, reason="jq is needed to run the projections")

RECORDED = Path(__file__).parent / "fixtures" / "recorded"
HOST = "host-login"
OWNER = "owner-login"
LABEL = "plan-approved"
ISSUE = 9
CANARY = "CANARY-6e1b-NO-LEAK"
T0 = "2026-11-16T10:00:00Z"
T1 = "2026-11-16T10:05:00Z"
T2 = "2026-11-16T10:10:00Z"

EXPECTED_KEYS = {
    "issue", "state", "plan_reason", "plan_reply_id", "plan_hash", "record_id", "plan_files_checked", "approvals",
    "approved", "label_revoked", "status_seen", "assignee_is_host_login", "adoption_state", "row_state", "row_evidence_count",
}
CHANNEL_KEYS = {"accepted", "reason", "evidence_id", "actor_id", "actor_is_host_login"}
VOCAB = {
    "no-plan-reply", "plan-reply-invalid", "plan-changed", "awaiting-approval", "approved", "revoked", "ok",
    "plan-reply-edited", "plan-reply-edit-unknown", "no-label", "label-before-plan", "label-removed", "actor-not-user",
    "actor-not-allowed", "no-comment", "author-not-allowed", "comment-before-plan", "edit-unknown", "comment-edited",
    "hash-mismatch", "reserved", "started", "uncertain", "recorded", "instructed", "acked", "revoked",
}


def jq(program: str, document: object) -> str:
    done = subprocess.run(["jq", "-c", program], input=json.dumps(document), capture_output=True, text=True, check=True)
    return done.stdout


def ok(stdout: str) -> CommandResult:
    return CommandResult(("gh",), 0, stdout, "", False, None, 0.0)


class World:
    """Raw GitHub evidence for one issue, served through the injected runner."""

    def __init__(self, *, host: str = HOST, assignees: tuple[str, ...] = (OWNER,)) -> None:
        self.host, self.assignees = host, assignees
        self.comments: list[dict] = []
        self.events: list[dict] = []
        self.edited: dict[int, str] = {}
        self.argvs: list[list[str]] = []
        self._next = 100

    def _id(self) -> int:
        self._next += 1
        return self._next

    def plan_reply(self, plan: str, at: str = T0) -> int:
        cid = self._id()
        body = f"Plan ready. {CANARY}\n<!-- sc:stage:plan id=ap-{ISSUE}-plan-{plan[:12]} plan={plan} -->"
        self.comments.append(self._comment(cid, self.host, 1, "User", at, body))
        return cid

    def comment(self, body: str, at: str, login: str = OWNER, uid: int = 111, kind: str = "User") -> int:
        cid = self._id()
        self.comments.append(self._comment(cid, login, uid, kind, at, body))
        return cid

    @staticmethod
    def _comment(cid: int, login: str, uid: int, kind: str, at: str, body: str) -> dict:
        return {"id": cid, "user": {"login": login, "id": uid, "type": kind}, "created_at": at, "updated_at": at, "body": body}

    def label(self, event: str, at: str, login: str = OWNER, uid: int = 111, kind: str = "User") -> None:
        self.events.append(
            {"id": self._id(), "event": event, "label": {"name": LABEL}, "actor": {"id": uid, "login": login, "type": kind}, "created_at": at}
        )

    def status_move(self, at: str) -> None:
        self.events.append({"id": self._id(), "event": "project_v2_item_status_changed", "actor": {"id": 5, "login": "bot[bot]", "type": "Bot"}, "created_at": at})

    # the injected runner
    def run(self, argv, timeout, *, cwd=None) -> CommandResult:
        self.argvs.append(list(argv))
        if argv == ["gh", "api", "user", "--include"]:
            return ok("HTTP/2.0 200 OK\ndate: Mon, 16 Nov 2026 10:00:00 GMT\n\n" + json.dumps({"login": self.host, "id": 1}))
        if argv[:3] == ["gh", "api", "graphql"]:
            nodes = [
                {"databaseId": c["id"], "author": {"login": c["user"]["login"]}, "createdAt": c["created_at"], "lastEditedAt": self.edited.get(c["id"])}
                for c in self.comments
            ]
            data = {"data": {"repository": {"issue": {"createdAt": "2026-11-15T00:00:00Z", "lastEditedAt": None,
                    "comments": {"nodes": nodes, "pageInfo": {"hasNextPage": False, "endCursor": None}}}}}}
            return ok(json.dumps(data))
        path = next(a for a in argv if a.startswith("repos/"))
        if path.endswith("/events"):
            return ok(jq(gh.EVENTS_JQ, self.events))
        if path.endswith("/comments"):
            return ok(jq(reads.COMMENTS_JQ, self.comments))
        assert path.endswith(f"/issues/{ISSUE}") or re.search(r"/issues/\d+$", path), path
        return ok(json.dumps({"number": int(path.rsplit("/", 1)[1]), "state": "open", "labels": [], "assignees": list(self.assignees)}))


@pytest.fixture
def plan_dir(tmp_path: Path) -> Path:
    d = tmp_path / "report"
    d.mkdir()
    (d / "plan.md").write_text("the plan")
    return d


def plan_sha(plan_dir: Path) -> str:
    return plan_hash.compute(plan_dir, ["plan.md"])[1]


def invoke(world: World, monkeypatch, *args: str, issue: int = ISSUE, approvers=frozenset({222})):
    monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
    monkeypatch.setattr(cli_mod, "_load_stage_inputs", lambda path: (LABEL, approvers))
    return CliRunner().invoke(issue_pipeline_group, ["stage-status", str(issue), "--json", *args])


def assert_closed(out: dict) -> None:
    assert set(out) == EXPECTED_KEYS
    assert set(out["approvals"]) == {"label", "comment"}
    for channel in out["approvals"].values():
        assert set(channel) == CHANNEL_KEYS
    strings = [out["state"], out["plan_reason"], out["adoption_state"], out["row_state"]]
    strings += [c["reason"] for c in out["approvals"].values()]
    assert all(s is None or s in VOCAB for s in strings), strings
    for key in ("plan_hash",):
        assert out[key] is None or re.fullmatch(r"[0-9a-f]{64}", out[key])
    assert out["record_id"] is None or re.fullmatch(r"ap-[1-9][0-9]*-plan-[0-9a-f]{12}", out["record_id"])
    assert CANARY not in json.dumps(out)


def status(world: World, monkeypatch, plan_dir: Path, *extra: str, approvers=frozenset({222})) -> dict:
    result = invoke(world, monkeypatch, "--plan-dir", str(plan_dir), "--plan-file", "plan.md", *extra, approvers=approvers)
    assert result.exit_code == 0, result.output
    out = json.loads(result.output)
    assert_closed(out)
    return out


# --- recorded files -------------------------------------------------------------


def test_recorded_files_through_the_injected_runner_print_only_closed_keys(monkeypatch) -> None:
    world = World(host="ironbelly", assignees=("ironbelly",))
    world.comments = json.loads((RECORDED / "comments-page1.json").read_text())
    world.events = json.loads((RECORDED / "events-page1.json").read_text())
    raw_edits = json.loads((RECORDED / "edits-page1.json").read_text())
    real_run = world.run

    def run(argv, timeout, *, cwd=None):
        if argv[:3] == ["gh", "api", "graphql"]:
            world.argvs.append(list(argv))
            return ok(json.dumps(raw_edits))
        return real_run(argv, timeout, cwd=cwd)

    world.run = run  # type: ignore[method-assign]
    result = invoke(world, monkeypatch, issue=452)
    assert result.exit_code == 0, result.output
    out = json.loads(result.output)
    assert_closed(out)
    assert out["state"] == "no-plan-reply" and out["issue"] == 452


# --- the case table --------------------------------------------------------------


def test_no_plan_reply_yet(monkeypatch, plan_dir: Path) -> None:
    world = World()
    world.comment("hello", T1)
    out = status(world, monkeypatch, plan_dir)
    assert out["state"] == "no-plan-reply" and out["approved"] is False and out["plan_hash"] is None


def test_plan_reply_and_no_approval(monkeypatch, plan_dir: Path) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    out = status(world, monkeypatch, plan_dir)
    assert out["state"] == "awaiting-approval" and out["plan_files_checked"] is True
    assert out["approvals"]["label"]["reason"] == "no-label" and out["approvals"]["comment"]["reason"] == "no-comment"


def test_label_only(monkeypatch, plan_dir: Path) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    world.label("labeled", T1)
    out = status(world, monkeypatch, plan_dir)
    assert out["approved"] and out["approvals"]["label"]["accepted"] and not out["approvals"]["comment"]["accepted"]
    assert out["status_seen"] is False


def test_comment_only(monkeypatch, plan_dir: Path) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    world.comment("approved", T1)
    out = status(world, monkeypatch, plan_dir)
    assert out["approved"] and out["approvals"]["comment"]["accepted"] and not out["approvals"]["label"]["accepted"]


def test_label_and_comment_make_one_key_and_one_row(monkeypatch, plan_dir: Path, tmp_path: Path) -> None:
    sha = plan_sha(plan_dir)
    world = World()
    world.plan_reply(sha)
    cid = world.comment("approved", T1)
    world.label("labeled", T1)
    world.status_move(T2)
    adir = tmp_path / "approvals"
    approval_record.init_dir(adir)
    approval_record.adopt_create(adir, ISSUE, "plan", T0)
    approval_record.adopt_mark(adir, ISSUE, "plan", "started", "ctx_1", T0)
    approval_record.record_create(adir, ISSUE, "plan", sha, "label", "evt-1", "u_1", T1)
    approval_record.record_create(adir, ISSUE, "plan", sha, "comment", f"c{cid}", "u_1", T1)
    out = status(world, monkeypatch, plan_dir, "--approvals-dir", str(adir))
    assert out["approved"] and out["approvals"]["label"]["accepted"] and out["approvals"]["comment"]["accepted"]
    assert (out["adoption_state"], out["row_state"], out["row_evidence_count"]) == ("started", "recorded", 2)
    assert out["status_seen"] is True
    assert len(list(adir.glob("approval-*.json"))) == 1


def test_plan_changed_after_approval(monkeypatch, plan_dir: Path) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    world.comment("approved", T1)
    (plan_dir / "plan.md").write_text("the plan, edited")
    out = status(world, monkeypatch, plan_dir)
    assert out["state"] == "plan-changed" and out["approved"] is False


def test_approval_label_removed(monkeypatch, plan_dir: Path) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    world.label("labeled", T1)
    world.label("unlabeled", T2)
    out = status(world, monkeypatch, plan_dir)
    assert out["state"] == "revoked" and out["label_revoked"] is True


def test_approver_not_listed(monkeypatch, plan_dir: Path) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    world.comment("approved", T1, login="stranger", uid=999)
    world.label("labeled", T1, login="stranger", uid=999)
    out = status(world, monkeypatch, plan_dir)
    assert out["approved"] is False
    assert out["approvals"]["comment"]["reason"] == "author-not-allowed"
    assert out["approvals"]["label"]["reason"] == "actor-not-allowed"
    listed = status(world, monkeypatch, plan_dir, approvers=frozenset({999}))
    assert listed["approved"] is True


def test_without_plan_files_the_markers_own_hash_is_used_and_flagged(monkeypatch, plan_dir: Path) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    out = json.loads(invoke(world, monkeypatch).output)
    assert out["plan_files_checked"] is False and out["state"] == "awaiting-approval"


def test_a_failed_read_prints_a_closed_refusal_and_nothing_else(monkeypatch) -> None:
    class Down:
        def run(self, argv, timeout, *, cwd=None):
            return CommandResult(tuple(argv), 1, "", f"HTTP 502 {CANARY}", False, None, 0.0)

    result = invoke(Down(), monkeypatch)
    assert result.exit_code == 1 and result.output.startswith("refused:") and CANARY not in result.output


# --- read-only proof -------------------------------------------------------------


def test_the_command_only_reads_and_never_calls_orca(monkeypatch, plan_dir: Path, tmp_path: Path) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    world.comment("approved", T1)
    world.label("labeled", T1)
    before = sorted(p.name for p in tmp_path.rglob("*"))
    status(world, monkeypatch, plan_dir)
    assert sorted(p.name for p in tmp_path.rglob("*")) == before  # nothing was written
    assert world.argvs
    graphql = [a for a in world.argvs if a[:3] == ["gh", "api", "graphql"]]
    assert graphql == [gh.argv_edits(ISSUE)]  # the watcher's fixed query, untouched
    for argv in world.argvs:
        assert argv[0] == "gh" and "orca" not in " ".join(argv).lower().split()
        if "--method" in argv:
            assert argv[argv.index("--method") + 1] == "GET"
        elif argv[:3] != ["gh", "api", "graphql"]:
            assert argv == ["gh", "api", "user", "--include"] or "--method" in argv
        text = " ".join(argv)
        assert not re.search(r"mutation|--method (POST|PUT|PATCH|DELETE)|-X ", text)


def test_stage_status_help_exits_zero() -> None:
    result = CliRunner().invoke(issue_pipeline_group, ["stage-status", "--help"])
    assert result.exit_code == 0 and "stage-status" in result.output
