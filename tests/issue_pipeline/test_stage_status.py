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

pytestmark = pytest.mark.skipif(
    shutil.which("jq") is None, reason="jq is needed to run the projections"
)

RECORDED = Path(__file__).parent / "fixtures" / "recorded"
HOST = "host-login"
OWNER = "owner-login"
LABEL = "plan-approved"
ISSUE = 9
REPO = "IronbellyOrg/IronClaude"
OTHER = "Other/Repo"
CANARY = "CANARY-6e1b-NO-LEAK"
T0 = "2026-11-16T10:00:00Z"
T1 = "2026-11-16T10:05:00Z"
T2 = "2026-11-16T10:10:00Z"

EXPECTED_KEYS = {
    "issue",
    "state",
    "plan_reason",
    "plan_reply_id",
    "plan_hash",
    "record_id",
    "plan_files_checked",
    "approvals",
    "approved",
    "label_revoked",
    "status_seen",
    "assignee_is_host_login",
    "adoption_state",
    "row_state",
    "row_evidence_count",
}
CHANNEL_KEYS = {"accepted", "reason", "evidence_id", "actor_id", "actor_is_host_login"}
VOCAB = {
    "no-plan-reply",
    "plan-reply-invalid",
    "plan-changed",
    "awaiting-approval",
    "approved",
    "revoked",
    "ok",
    "plan-reply-edited",
    "plan-reply-edit-unknown",
    "no-label",
    "label-before-plan",
    "label-removed",
    "actor-not-user",
    "actor-not-allowed",
    "no-comment",
    "author-not-allowed",
    "comment-before-plan",
    "edit-unknown",
    "comment-edited",
    "hash-mismatch",
    "reserved",
    "started",
    "uncertain",
    "recorded",
    "instructed",
    "acked",
    "revoked",
}


def jq(program: str, document: object) -> str:
    done = subprocess.run(
        ["jq", "-c", program],
        input=json.dumps(document),
        capture_output=True,
        text=True,
        check=True,
    )
    return done.stdout


def ok(stdout: str) -> CommandResult:
    return CommandResult(("gh",), 0, stdout, "", False, None, 0.0)


class World:
    """Raw GitHub evidence for one issue, served through the injected runner."""

    def __init__(
        self,
        *,
        host: str = HOST,
        assignees: tuple[str, ...] = (OWNER,),
        repo: str = REPO,
    ) -> None:
        self.host, self.assignees, self.repo = host, assignees, repo
        self.comments: list[dict] = []
        self.events: list[dict] = []
        self.field_nodes: list[dict] = []  # G8 nodes: the Approved field events (R35)
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

    def comment(
        self, body: str, at: str, login: str = OWNER, uid: int = 111, kind: str = "User"
    ) -> int:
        cid = self._id()
        self.comments.append(self._comment(cid, login, uid, kind, at, body))
        return cid

    @staticmethod
    def _comment(cid: int, login: str, uid: int, kind: str, at: str, body: str) -> dict:
        return {
            "id": cid,
            "user": {"login": login, "id": uid, "type": kind},
            "created_at": at,
            "updated_at": at,
            "body": body,
        }

    def label(
        self,
        event: str,
        at: str,
        login: str = OWNER,
        uid: int = 111,
        kind: str = "User",
    ) -> None:
        self.events.append(
            {
                "id": self._id(),
                "event": event,
                "label": {"name": LABEL},
                "actor": {"id": uid, "login": login, "type": kind},
                "created_at": at,
            }
        )

    def field_set(
        self, at: str, login: str = OWNER, uid: int = 111, kind: str = "User"
    ) -> None:
        """The Approved issue field set to Yes (R35), as GraphQL gives it."""
        self.field_nodes.append(
            {
                "__typename": "IssueFieldAddedEvent",
                "createdAt": at,
                "actor": {"__typename": kind, "login": login, "databaseId": uid},
                "issueField": {"name": "Approved"},
                "value": "Yes",
            }
        )

    def status_move(self, at: str) -> None:
        self.events.append(
            {
                "id": self._id(),
                "event": "project_v2_item_status_changed",
                "actor": {"id": 5, "login": "bot[bot]", "type": "Bot"},
                "created_at": at,
            }
        )

    # the injected runner
    @staticmethod
    def named_repo(argv) -> str | None:
        """The repository an argv names: a REST path, a GraphQL owner and name, or none."""
        for a in argv:
            if a.startswith("repos/"):
                return "/".join(a.split("/")[1:3])
        owner = next((a[6:] for a in argv if a.startswith("owner=")), None)
        name = next((a[5:] for a in argv if a.startswith("name=")), None)
        return f"{owner}/{name}" if owner and name else None

    def run(self, argv, timeout, *, cwd=None) -> CommandResult:
        self.argvs.append(list(argv))
        named = self.named_repo(argv)
        assert named in (None, self.repo), (
            f"{named} was read from the {self.repo} world"
        )
        if argv[:3] == ["gh", "api", "graphql"] and "timelineItems" in argv[4]:
            # The Approved field events (R35): none in these tests.
            return ok(
                json.dumps(
                    {
                        "data": {
                            "repository": {
                                "issue": {
                                    "timelineItems": {
                                        "nodes": self.field_nodes,
                                        "pageInfo": {
                                            "hasNextPage": False,
                                            "endCursor": None,
                                        },
                                    }
                                }
                            }
                        }
                    }
                )
            )
        if argv == ["gh", "api", "user", "--include"]:
            return ok(
                "HTTP/2.0 200 OK\ndate: Mon, 16 Nov 2026 10:00:00 GMT\n\n"
                + json.dumps({"login": self.host, "id": 1})
            )
        if argv[:3] == ["gh", "api", "graphql"]:
            nodes = [
                {
                    "databaseId": c["id"],
                    "author": {"login": c["user"]["login"]},
                    "createdAt": c["created_at"],
                    "lastEditedAt": self.edited.get(c["id"]),
                }
                for c in self.comments
            ]
            data = {
                "data": {
                    "repository": {
                        "issue": {
                            "createdAt": "2026-11-15T00:00:00Z",
                            "lastEditedAt": None,
                            "comments": {
                                "nodes": nodes,
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                            },
                        }
                    }
                }
            }
            return ok(json.dumps(data))
        path = next(a for a in argv if a.startswith("repos/"))
        if path.endswith("/events"):
            return ok(jq(gh.EVENTS_JQ, self.events))
        if path.endswith("/comments"):
            return ok(jq(reads.COMMENTS_JQ, self.comments))
        assert path.endswith(f"/issues/{ISSUE}") or re.search(r"/issues/\d+$", path), (
            path
        )
        return ok(
            json.dumps(
                {
                    "number": int(path.rsplit("/", 1)[1]),
                    "state": "open",
                    "labels": [],
                    "assignees": list(self.assignees),
                }
            )
        )


@pytest.fixture
def plan_dir(tmp_path: Path) -> Path:
    d = tmp_path / "report"
    d.mkdir()
    (d / "plan.md").write_text("the plan")
    return d


def plan_sha(plan_dir: Path) -> str:
    return plan_hash.compute(plan_dir, ["plan.md"])[1]


def invoke(
    world: World,
    monkeypatch,
    *args: str,
    issue: int = ISSUE,
    approvers=frozenset({222}),
    label: str = LABEL,
    repo: str = REPO,
    config_repo: str | None = None,
):
    monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
    monkeypatch.setattr(
        cli_mod,
        "_load_stage_inputs",
        lambda path: (label, approvers, config_repo or repo),
    )
    return CliRunner().invoke(
        issue_pipeline_group,
        ["stage-status", str(issue), "--repo", repo, "--json", *args],
    )


def assert_closed(out: dict) -> None:
    assert set(out) == EXPECTED_KEYS
    assert set(out["approvals"]) == {"label", "comment"}
    for channel in out["approvals"].values():
        assert set(channel) == CHANNEL_KEYS
    strings = [
        out["state"],
        out["plan_reason"],
        out["adoption_state"],
        out["row_state"],
    ]
    strings += [c["reason"] for c in out["approvals"].values()]
    assert all(s is None or s in VOCAB for s in strings), strings
    for key in ("plan_hash",):
        assert out[key] is None or re.fullmatch(r"[0-9a-f]{64}", out[key])
    assert out["record_id"] is None or re.fullmatch(
        r"ap-[1-9][0-9]*-plan-[0-9a-f]{12}", out["record_id"]
    )
    assert CANARY not in json.dumps(out)


def status(
    world: World, monkeypatch, plan_dir: Path, *extra: str, approvers=frozenset({222})
) -> dict:
    result = invoke(
        world,
        monkeypatch,
        "--plan-dir",
        str(plan_dir),
        "--plan-file",
        "plan.md",
        *extra,
        approvers=approvers,
    )
    assert result.exit_code == 0, result.output
    out = json.loads(result.output)
    assert_closed(out)
    return out


# --- recorded files -------------------------------------------------------------


def test_recorded_files_through_the_injected_runner_print_only_closed_keys(
    monkeypatch,
) -> None:
    world = World(host="ironbelly", assignees=("ironbelly",))
    world.comments = json.loads((RECORDED / "comments-page1.json").read_text())
    world.events = json.loads((RECORDED / "events-page1.json").read_text())
    raw_edits = json.loads((RECORDED / "edits-page1.json").read_text())
    real_run = world.run

    def run(argv, timeout, *, cwd=None):
        if argv[:3] == ["gh", "api", "graphql"] and "timelineItems" not in argv[4]:
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
    assert (
        out["state"] == "no-plan-reply"
        and out["approved"] is False
        and out["plan_hash"] is None
    )


def test_plan_reply_and_no_approval(monkeypatch, plan_dir: Path) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    out = status(world, monkeypatch, plan_dir)
    assert out["state"] == "awaiting-approval" and out["plan_files_checked"] is True
    assert (
        out["approvals"]["label"]["reason"] == "no-label"
        and out["approvals"]["comment"]["reason"] == "no-comment"
    )


def test_label_only(monkeypatch, plan_dir: Path) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    world.label("labeled", T1)
    out = status(world, monkeypatch, plan_dir)
    assert (
        out["approved"]
        and out["approvals"]["label"]["accepted"]
        and not out["approvals"]["comment"]["accepted"]
    )
    assert out["status_seen"] is False


def test_the_approved_field_is_seen_as_the_label_approval__r35(
    monkeypatch, plan_dir: Path
) -> None:
    from superclaude.cli.issue_watch.predicates import APPROVAL_FIELD_LABEL

    world = World()
    world.plan_reply(plan_sha(plan_dir))
    world.field_set(T1, uid=222)
    result = invoke(
        world,
        monkeypatch,
        "--plan-dir",
        str(plan_dir),
        "--plan-file",
        "plan.md",
        label=APPROVAL_FIELD_LABEL,
    )
    assert result.exit_code == 0, result.output
    out = json.loads(result.output)
    assert out["approved"] and out["approvals"]["label"]["accepted"]
    assert out["approvals"]["label"]["actor_id"] == 222


def test_comment_only(monkeypatch, plan_dir: Path) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    world.comment("approved", T1)
    out = status(world, monkeypatch, plan_dir)
    assert (
        out["approved"]
        and out["approvals"]["comment"]["accepted"]
        and not out["approvals"]["label"]["accepted"]
    )


def test_label_and_comment_make_one_key_and_one_row(
    monkeypatch, plan_dir: Path, tmp_path: Path
) -> None:
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
    approval_record.record_create(
        adir, ISSUE, "plan", sha, "comment", f"c{cid}", "u_1", T1
    )
    out = status(world, monkeypatch, plan_dir, "--approvals-dir", str(adir))
    assert (
        out["approved"]
        and out["approvals"]["label"]["accepted"]
        and out["approvals"]["comment"]["accepted"]
    )
    assert (out["adoption_state"], out["row_state"], out["row_evidence_count"]) == (
        "started",
        "recorded",
        2,
    )
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


def test_without_plan_files_the_markers_own_hash_is_used_and_flagged(
    monkeypatch, plan_dir: Path
) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    out = json.loads(invoke(world, monkeypatch).output)
    assert out["plan_files_checked"] is False and out["state"] == "awaiting-approval"


def test_a_failed_read_prints_a_closed_refusal_and_nothing_else(monkeypatch) -> None:
    class Down:
        def run(self, argv, timeout, *, cwd=None):
            return CommandResult(
                tuple(argv), 1, "", f"HTTP 502 {CANARY}", False, None, 0.0
            )

    result = invoke(Down(), monkeypatch)
    assert (
        result.exit_code == 1
        and result.output.startswith("refused:")
        and CANARY not in result.output
    )


# --- read-only proof -------------------------------------------------------------


def test_the_command_only_reads_and_never_calls_orca(
    monkeypatch, plan_dir: Path, tmp_path: Path
) -> None:
    world = World()
    world.plan_reply(plan_sha(plan_dir))
    world.comment("approved", T1)
    world.label("labeled", T1)
    before = sorted(p.name for p in tmp_path.rglob("*"))
    status(world, monkeypatch, plan_dir)
    assert sorted(p.name for p in tmp_path.rglob("*")) == before  # nothing was written
    assert world.argvs
    graphql = [a for a in world.argvs if a[:3] == ["gh", "api", "graphql"]]
    # the watcher's fixed queries, untouched: the Approved field events, then edits
    assert graphql == [gh.argv_approval_events(ISSUE), gh.argv_edits(ISSUE)]
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


# --- claim-time approval (plan Task 11, R29, R35) ----------------------------------


def _claim_entry(tmp_path: Path, approved_at: str) -> dict:
    """The watcher store's claimed entry for the issue (a dispatch.json fixture)."""
    path = tmp_path / "dispatch.json"
    path.write_text(
        json.dumps(
            {
                str(ISSUE): {
                    "state": "claimed",
                    "approver_id": 222,
                    "approval_event_id": 4242,
                    "approved_at": approved_at,
                }
            }
        )
    )
    return json.loads(path.read_text())[str(ISSUE)]


def _field_status(world: World, monkeypatch, plan_dir: Path) -> dict:
    from superclaude.cli.issue_watch.predicates import APPROVAL_FIELD_LABEL

    result = invoke(
        world,
        monkeypatch,
        "--plan-dir",
        str(plan_dir),
        "--plan-file",
        "plan.md",
        label=APPROVAL_FIELD_LABEL,
    )
    assert result.exit_code == 0, result.output
    out = json.loads(result.output)
    assert_closed(out)
    return out


def test_a_claim_time_approval_dated_before_the_plan_reply_is_not_plan_approval(
    monkeypatch, plan_dir: Path, tmp_path: Path
) -> None:
    entry = _claim_entry(tmp_path, T0)
    world = World()
    world.field_set(entry["approved_at"], uid=entry["approver_id"])
    world.plan_reply(plan_sha(plan_dir), at=T1)
    out = _field_status(world, monkeypatch, plan_dir)
    assert out["approved"] is False and out["state"] == "awaiting-approval"
    assert out["approvals"]["label"]["accepted"] is False
    assert out["approvals"]["label"]["reason"] == "label-before-plan"


def test_an_approval_dated_after_the_plan_reply_is_accepted(
    monkeypatch, plan_dir: Path, tmp_path: Path
) -> None:
    entry = _claim_entry(tmp_path, T0)
    world = World()
    world.field_set(entry["approved_at"], uid=entry["approver_id"])
    world.plan_reply(plan_sha(plan_dir), at=T1)
    world.field_set(T2, uid=entry["approver_id"])  # a fresh approval after the reply
    out = _field_status(world, monkeypatch, plan_dir)
    assert out["approved"] is True and out["state"] == "approved"
    assert out["approvals"]["label"]["reason"] == "ok"
    assert out["approvals"]["label"]["actor_id"] == entry["approver_id"]


# --- the repository is named by the caller (plan Task 15) ----------------------------


class Router:
    """A runner that serves each repository from its own ``World``."""

    def __init__(self, **worlds: World) -> None:
        self.worlds = worlds  # keyed by "owner/name" through ``by_repo``
        self.by_repo = {w.repo: w for w in worlds.values()}
        self.argvs: list[list[str]] = []

    def run(self, argv, timeout, *, cwd=None) -> CommandResult:
        self.argvs.append(list(argv))
        repo = World.named_repo(argv)
        world = self.by_repo[repo] if repo else next(iter(self.by_repo.values()))
        return world.run(argv, timeout, cwd=cwd)


def test_stage_status_without_repo_and_without_a_config_reads_nothing(
    monkeypatch, tmp_path: Path
) -> None:
    world = World()
    monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
    missing = tmp_path / "absent.json"
    result = CliRunner().invoke(
        issue_pipeline_group,
        ["stage-status", str(ISSUE), "--config", str(missing)],
    )
    assert result.exit_code == 2 and result.output == "refused:config_invalid\n"
    assert world.argvs == []


@pytest.mark.parametrize(
    "bad", ["a/b/c", "", "a b/c", "-a/b", "a/-b", "justone", "a/b\n", "{owner}/{repo}"]
)
def test_a_repo_that_is_not_owner_slash_name_is_refused_before_any_call(
    monkeypatch, bad: str
) -> None:
    world = World()
    result = invoke(world, monkeypatch, repo=bad)
    assert result.exit_code == 1 and result.output == "refused:bad-repo\n"
    assert world.argvs == []


def test_with_another_repo_every_read_carries_it_and_none_names_the_default(
    monkeypatch, plan_dir: Path
) -> None:
    world = World(repo=OTHER)
    world.plan_reply(plan_sha(plan_dir))
    result = invoke(world, monkeypatch, repo=OTHER)
    assert result.exit_code == 0, result.output
    reads_ = [a for a in world.argvs if a != ["gh", "api", "user", "--include"]]
    kinds = {
        "reread": lambda a: (
            a[:4] == ["gh", "api", "--method", "GET"]
            and a[4].endswith(f"/issues/{ISSUE}")
        ),
        "events": lambda a: len(a) > 4 and a[4].endswith("/events"),
        "comments": lambda a: len(a) > 4 and a[4].endswith("/comments"),
        "edits": lambda a: (
            a[:3] == ["gh", "api", "graphql"] and "comments(first" in " ".join(a)
        ),
        "approval_events": lambda a: (
            a[:3] == ["gh", "api", "graphql"] and "timelineItems" in " ".join(a)
        ),
    }
    for kind, test in kinds.items():
        matched = [a for a in reads_ if test(a)]
        assert matched, kind
        for argv in matched:
            text = "\n".join(argv)
            assert "Other/Repo" in text or (
                "owner=Other" in argv and "name=Repo" in argv
            ), kind
            assert "IronClaude" not in text and "IronbellyOrg" not in text, kind


def test_an_approval_on_the_default_repos_issue_never_approves_the_other_repo(
    monkeypatch, plan_dir: Path
) -> None:
    sha = plan_sha(plan_dir)
    fork = World(repo=REPO)
    fork.plan_reply(sha)
    fork.label("labeled", T1)  # approved on IronClaude's issue of the same number
    other = World(repo=OTHER)
    other.plan_reply(sha)  # the same plan, no approval on the other repo
    router = Router(fork=fork, other=other)
    result = invoke(
        router,
        monkeypatch,
        "--plan-dir",
        str(plan_dir),
        "--plan-file",
        "plan.md",
        repo=OTHER,
    )
    out = json.loads(result.output)
    assert result.exit_code == 0 and out["approved"] is False
    assert out["approvals"]["label"]["reason"] == "no-label"
    assert not any("IronClaude" in " ".join(a) for a in router.argvs)
    # and the same call for the default repo does see its own approval
    again = invoke(
        router,
        monkeypatch,
        "--plan-dir",
        str(plan_dir),
        "--plan-file",
        "plan.md",
        repo=REPO,
    )
    assert json.loads(again.output)["approved"] is True


# --- the repo defaults to the config's (plan Task 16) --------------------------------


def _write_config(tmp_path: Path, **extra: object) -> Path:
    """A real watcher config file, so the verb's own loader reads it."""
    approvers = tmp_path / "approvers"
    approvers.write_text("222\n")
    approvers.chmod(0o600)
    raw = {
        "schema_version": 1,
        "project_id": "PVT_abc",
        "worktree": str(tmp_path),
        "approvers_file": str(approvers),
        "state_dir": str(tmp_path / "state"),
        **extra,
    }
    path = tmp_path / "issue-watch.json"
    path.write_text(json.dumps(raw))
    return path


def _stage_cli(world, monkeypatch, config: Path, *extra: str):
    monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
    return CliRunner().invoke(
        issue_pipeline_group,
        ["stage-status", str(ISSUE), "--config", str(config), "--json", *extra],
    )


def test_without_repo_the_config_repo_is_read(monkeypatch, tmp_path: Path) -> None:
    world = World(repo=OTHER)
    result = _stage_cli(world, monkeypatch, _write_config(tmp_path, repo=OTHER))
    assert result.exit_code == 0, result.output
    assert world.argvs  # it read, and the World asserts every argv names Other/Repo
    assert not any("IronClaude" in " ".join(a) for a in world.argvs)


def test_without_config_the_per_repo_config_of_a_zero_setup_host_is_used(
    monkeypatch, tmp_path: Path
) -> None:
    """Only issue-watch.d/<name>.json exists (the generator's output); --repo picks it."""
    home = tmp_path / "home"
    folder = home / ".config" / "superclaude" / "issue-watch.d"
    folder.mkdir(parents=True)
    generated = _write_config(tmp_path, repo=OTHER)
    (folder / "Other.json").write_text(generated.read_text())
    monkeypatch.setenv("HOME", str(home))
    world = World(repo=OTHER)
    monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
    result = CliRunner().invoke(
        issue_pipeline_group, ["stage-status", str(ISSUE), "--repo", OTHER, "--json"]
    )
    assert result.exit_code == 0, result.output
    assert world.argvs  # it read; there is no ~/.config/superclaude/issue-watch.json


def test_a_hand_written_config_without_a_repo_key_reads_the_fork(
    monkeypatch, tmp_path: Path
) -> None:
    world = World(repo=REPO)
    result = _stage_cli(world, monkeypatch, _write_config(tmp_path))
    assert result.exit_code == 0, result.output
    assert any(f"repos/{REPO}/issues/{ISSUE}" in " ".join(a) for a in world.argvs)


def test_a_repo_that_differs_from_the_configs_is_refused_before_any_call(
    monkeypatch, tmp_path: Path
) -> None:
    world = World(repo=OTHER)
    config = _write_config(tmp_path, repo=OTHER)
    result = _stage_cli(world, monkeypatch, config, "--repo", REPO)
    assert result.exit_code == 1 and result.output == "refused:repo-mismatch\n"
    assert world.argvs == []
    # a default config (no repo key) against --repo Other/Repo is a mismatch too
    (tmp_path / "plain").mkdir()
    plain = _write_config(tmp_path / "plain")
    result = _stage_cli(world, monkeypatch, plain, "--repo", OTHER)
    assert result.output == "refused:repo-mismatch\n" and world.argvs == []


def test_a_repo_that_matches_the_configs_is_accepted(
    monkeypatch, tmp_path: Path
) -> None:
    # the compare is case-insensitive; the repo the caller typed is the one that is read
    world = World(repo=OTHER.lower())
    config = _write_config(tmp_path, repo=OTHER)
    result = _stage_cli(world, monkeypatch, config, "--repo", OTHER.lower())
    assert result.exit_code == 0, result.output
    assert world.argvs
