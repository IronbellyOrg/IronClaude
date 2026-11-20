"""``lease`` (DQ3): the lowest active lease keeps the claim, the loser and the stopping winner release theirs."""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.orchestrator import limits

from .fake_world import REPO, World, call, install, make_root, repos_text

ISSUE = ("--repo", REPO, "--number", "655")


def lease_body(host: str, run: str, released: bool = False) -> str:
    tail = " state=released" if released else ""
    return f"<!-- sc:orchestrator:lease host={host} run={run}{tail} -->"


@pytest.fixture
def world(monkeypatch) -> World:
    w = install(monkeypatch, World())
    yield w
    assert not w.unexpected, w.unexpected
    # every call a verb made passes the refusal list: the guard stayed in the path
    assert [c for c in w.calls if limits.refuse(list(c)) is not None] == []


def orchestrator(tmp_path: Path, name: str, **kw) -> Path:
    path = tmp_path / name
    path.mkdir()
    return make_root(path, run_id=f"run_{name}", host=f"host-{name}", **kw)


def post(root: Path) -> tuple[int, dict]:
    return call(root, "lease", "post", *ISSUE)


def check(root: Path) -> tuple[int, dict]:
    return call(root, "lease", "check", *ISSUE)


def release(root: Path) -> tuple[int, dict]:
    return call(root, "lease", "release", *ISSUE)


# --- post ---------------------------------------------------------------------------------------


def test_post_writes_the_marker_comment_and_prints_its_id_and_grant(
    tmp_path: Path, world: World
) -> None:
    a = orchestrator(tmp_path, "a")
    code, out = post(a)
    assert code == 0 and out == {
        "ok": True,
        "comment_id": 1001,
        "reused": False,
        "grant": "issue.comment",
    }
    assert world.body_of(1001) == "<!-- sc:orchestrator:lease host=host-a run=run_a -->"
    assert world.argvs("gh", "api", "-X", "POST") == [
        (
            "gh", "api", "-X", "POST", f"repos/{REPO}/issues/655/comments",
            "-f", "body=<!-- sc:orchestrator:lease host=host-a run=run_a -->", "--jq", ".id",
        )
    ]  # fmt: skip


def test_post_twice_after_a_restart_finds_its_lease_and_posts_nothing_more(
    tmp_path: Path, world: World
) -> None:
    a = orchestrator(tmp_path, "a")
    post(a)
    code, out = post(a)
    assert code == 0 and out["reused"] is True and out["comment_id"] == 1001
    assert len(world.argvs("gh", "api", "-X", "POST")) == 1


def test_a_released_lease_is_not_reused(tmp_path: Path, world: World) -> None:
    a = orchestrator(tmp_path, "a")
    post(a)
    release(a)
    code, out = post(a)
    assert code == 0 and out["reused"] is False and out["comment_id"] == 1002


# --- two orchestrators ----------------------------------------------------------------------------


def test_two_orchestrators_the_lowest_id_keeps_the_claim_and_the_loser_releases_its_lease(
    tmp_path: Path, world: World
) -> None:
    a, b = orchestrator(tmp_path, "a"), orchestrator(tmp_path, "b")
    assert post(a)[1]["comment_id"] == 1001
    assert post(b)[1]["comment_id"] == 1002

    code, out = check(a)
    assert code == 0 and out["keep"] is True
    assert (out["comment_id"], out["lowest_comment_id"], out["active_leases"]) == (
        1001,
        1001,
        2,
    )

    code, out = check(b)
    assert (code, out["ok"], out["reason"]) == (3, False, "lease_lost")
    assert out["winner_comment_id"] == 1001 and out["released"] is True
    assert world.body_of(1002) == lease_body(
        "host-b", "run_b", released=True
    )  # the loser's lease
    assert world.body_of(1001) == lease_body(
        "host-a", "run_a"
    )  # the winner's is untouched
    assert world.argvs("gh", "api", "-X", "PATCH") == [
        (
            "gh", "api", "-X", "PATCH", f"repos/{REPO}/issues/comments/1002",
            "-f", "body=" + lease_body("host-b", "run_b", released=True),
        )
    ]  # fmt: skip


def test_the_winner_releases_its_lease_at_its_stop_so_a_later_run_can_win(
    tmp_path: Path, world: World
) -> None:
    a, c = orchestrator(tmp_path, "a"), orchestrator(tmp_path, "c")
    post(a)
    assert check(a)[0] == 0

    code, out = release(a)  # the winner stops (wave 9)
    assert code == 0 and out["released"] == [1001]
    assert world.body_of(1001) == lease_body("host-a", "run_a", released=True)

    post(c)
    code, out = check(
        c
    )  # the released lease is not counted: c is the lowest active one
    assert code == 0 and out["keep"] is True and out["lowest_comment_id"] == 1002
    assert out["active_leases"] == 1


def test_without_the_release_a_stopped_winner_would_keep_the_lowest_id_for_ever(
    tmp_path: Path, world: World
) -> None:
    a, c = orchestrator(tmp_path, "a"), orchestrator(tmp_path, "c")
    post(a)
    post(c)
    code, out = check(c)
    assert (code, out["reason"], out["winner_comment_id"]) == (3, "lease_lost", 1001)


def test_release_with_no_active_lease_releases_nothing_and_is_not_an_error(
    tmp_path: Path, world: World
) -> None:
    a = orchestrator(tmp_path, "a")
    assert release(a) == (0, {"ok": True, "released": [], "grant": "issue.comment"})
    post(a)
    release(a)
    assert release(a)[1]["released"] == []
    assert world.argvs("gh", "api", "-X", "PATCH").__len__() == 1


def test_only_leases_of_the_users_own_login_count(tmp_path: Path, world: World) -> None:
    a = orchestrator(tmp_path, "a")
    world.add_comment(
        REPO, 655, lease_body("host-x", "run_x"), login="someone-else"
    )  # id 1001
    world.add_comment(REPO, 655, "a plain comment")
    post(a)
    code, out = check(a)
    assert code == 0 and out["keep"] is True and out["active_leases"] == 1
    assert out["lowest_comment_id"] == out["comment_id"] == 1003


def test_a_comment_that_only_looks_like_a_lease_is_not_one(
    tmp_path: Path, world: World
) -> None:
    a = orchestrator(tmp_path, "a")
    world.add_comment(REPO, 655, "see <!-- sc:orchestrator:lease host=h run=r --> here")
    world.add_comment(REPO, 655, "<!-- sc:orchestrator:lease host=h run=r --> extra")
    world.add_comment(REPO, 655, "<!-- sc:orchestrator:lease host=h r=r -->")
    post(a)
    code, out = check(a)
    assert code == 0 and out["active_leases"] == 1


def test_a_missing_own_lease_is_lease_missing(tmp_path: Path, world: World) -> None:
    a = orchestrator(tmp_path, "a")
    code, out = check(a)
    assert (code, out["reason"]) == (3, "lease_missing")


# --- the write is a grant, and a read that fails is no answer ---------------------------------------


def test_no_grant_no_comment(tmp_path: Path, world: World) -> None:
    a = make_root(tmp_path, text=repos_text(grants=["issue.assign"]))
    code, out = post(a)
    assert (code, out["reason"], out["grant"]) == (2, "no_grant", "issue.comment")
    assert world.argvs("gh", "api", "-X") == [] and world.comments == {}


@pytest.mark.parametrize(
    ("repos", "reason"),
    [
        ([], "repo_not_listed"),
        ([{"repo": REPO, "enabled": False, "checkout": None}], "repo_disabled"),
    ],
)
def test_an_unlisted_or_disabled_repo_gets_no_lease(
    tmp_path: Path, world: World, repos: list, reason: str
) -> None:
    a = make_root(tmp_path, text=repos_text(repos=repos))
    assert post(a)[1]["reason"] == reason
    assert world.comments == {}


def test_the_loser_without_the_grant_cannot_release_and_says_so(
    tmp_path: Path, world: World
) -> None:
    a = orchestrator(tmp_path, "a")
    b = orchestrator(tmp_path, "b", text=repos_text(grants=[]))
    post(a)
    world.add_comment(
        REPO, 655, lease_body("host-b", "run_b")
    )  # b's lease, posted before it lost the grant
    code, out = check(b)
    assert (code, out["reason"]) == (2, "no_grant")
    assert world.body_of(1002) == lease_body("host-b", "run_b")  # nothing edited


def test_a_comment_list_that_cannot_be_read_is_never_read_as_a_shorter_list(
    tmp_path: Path, world: World
) -> None:
    a = orchestrator(tmp_path, "a")
    post(a)
    world.fail_when.append(lambda argv: "--paginate" in argv)
    code, out = check(a)
    assert (code, out["reason"]) == (6, "external_failed")
    world.fail_when.clear()
    world.comments[(REPO, 655)].append(
        {"id": "not-a-number", "login": "clayphi", "body": "x"}
    )
    code, out = check(a)
    assert (code, out["reason"]) == (6, "external_unreadable")


def test_a_failed_post_is_reported_and_nothing_is_recorded(
    tmp_path: Path, world: World
) -> None:
    a = orchestrator(tmp_path, "a")
    world.fail_when.append(lambda argv: argv[:4] == ("gh", "api", "-X", "POST"))
    code, out = post(a)
    assert (code, out["reason"]) == (6, "external_failed") and "stderr" not in out


def test_a_missing_run_file_stops_the_lease(tmp_path: Path, world: World) -> None:
    a = make_root(tmp_path, run=False)
    code, out = post(a)
    assert (code, out["reason"]) == (5, "run_not_found")
    assert world.calls == []


def test_a_host_that_cannot_go_into_the_marker_is_refused(
    tmp_path: Path, world: World
) -> None:
    a = make_root(tmp_path, host="host with spaces")
    code, out = post(a)
    assert (code, out["reason"]) == (2, "invalid_host")
    assert world.comments == {}


@pytest.mark.parametrize(
    "args", [("--repo", "bad repo", "--number", "1"), ("--repo", REPO, "--number", "0")]
)
def test_a_bad_repo_or_number_is_refused(
    tmp_path: Path, world: World, args: tuple
) -> None:
    a = orchestrator(tmp_path, "a")
    code, out = call(a, "lease", "post", *args)
    assert (code, out["reason"]) == (2, "invalid_input")
