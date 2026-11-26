"""dry_run_report and apply_repo, against a fake GitHub (no live call)."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

NOW = datetime(2026, 11, 26, 17, 0, tzinfo=timezone.utc)
REPO = "repos/acme/acme-one"
LIST = f"{REPO}/rulesets?per_page=100"
SERVER = {"source": "acme-one", "source_type": "Repository", "created_at": "2026"}
TAG_RULESET = "protect-release-tags"
PUSH = {"activity_type": "push", "timestamp": "2026-10-01T10:00:00Z"}


def activity(branch):
    return f"{REPO}/activity?ref=refs/heads/{branch}&time_period=quarter&per_page=100"


def digest_of(orr):
    return orr.payload_digest(orr.plan_bodies(["master", "integration"]))


def posts(runner, fake_runner_cls):
    return [c for c in runner.commands if fake_runner_cls.method_of(c.argv) == "POST"]


def apply(orr, runner, tmp_path, confirm=None):
    confirm = confirm or digest_of(orr)
    return orr.apply_repo(runner, "acme", "acme-one", tmp_path / "out", confirm, NOW)


# --- the dry run -------------------------------------------------------------------


def test_dry_run_prints_every_item_and_writes_nothing(world, orr, fake_runner_cls):
    runner = world()
    text = "\n".join(orr.dry_run_report(runner, "acme", "acme-one", NOW))
    assert posts(runner, fake_runner_cls) == []
    assert "acme/acme-one" in text and "default branch: master" in text
    assert "push check" in text and ": pass" in text
    assert "integration: pass (source activity, direct pushes 0" in text
    assert "classic protection: integration none, master none" in text
    assert "existing rulesets: none" in text
    assert "v* tags: 2" in text
    assert "blocks moving and deleting v* tags" in text and "by hand" in text
    names = (TAG_RULESET, "protect-integration", "protect-master")
    order = [text.index(n) for n in names]
    assert order == sorted(order)
    digest = digest_of(orr)
    assert f"digest: {digest}" in text
    assert f"--apply --confirm {digest}" in text
    assert "--org acme --repo acme-one" in text
    assert "would refuse" not in text


def test_dry_run_with_a_read_only_runner_never_posts(world, orr, fake_runner_cls):
    runner = world()
    runner.read_only = True
    assert orr.dry_run_report(runner, "acme", "acme-one", NOW)
    assert posts(runner, fake_runner_cls) == []


def test_dry_run_lists_a_same_name_ruleset_as_skipped_with_the_same_digest(
    world, orr, fake_runner_cls
):
    summary = fake_runner_cls.ok([{"id": 7, "name": "protect-master"}])
    runner = world(gets={LIST: summary})
    text = "\n".join(orr.dry_run_report(runner, "acme", "acme-one", NOW))
    assert "protect-master (branch) - skipped" in text
    assert f"digest: {digest_of(orr)}" in text


def test_dry_run_names_what_would_refuse(world, orr, fake_runner_cls):
    pushed = fake_runner_cls.ok([PUSH])
    runner = world(gets={activity("master"): pushed}, archived=True)
    text = "\n".join(orr.dry_run_report(runner, "acme", "acme-one", NOW))
    assert "would refuse --apply: repo is archived" in text
    assert "would refuse --apply: push check is blocked" in text


def test_dry_run_of_an_unreadable_repo(world, orr, fake_runner_cls):
    runner = world(gets={REPO: fake_runner_cls.http(404)})
    text = "\n".join(orr.dry_run_report(runner, "acme", "acme-one", NOW))
    assert "repo cannot be read (HTTP 404)" in text and "no plan" in text


# --- apply: refusals ---------------------------------------------------------------

COMMITS = f"{REPO}/commits?sha=master&since=2026-08-28T17:00:00Z&per_page=100"

# name -> (what to change in the fake GitHub, text the refusal must hold)
REFUSALS = {
    "wrong-confirm": ({}, "confirm digest does not match"),
    "no-out": ({}, "no --out folder"),
    "push-blocked": (
        {"gets": {activity("integration"): ("ok", [PUSH])}},
        "push check is blocked",
    ),
    "push-incomplete": (
        {"gets": {activity("master"): ("http", 403), COMMITS: ("http", 403)}},
        "push check is incomplete",
    ),
    "classic": (
        {"gets": {f"{REPO}/branches/master/protection": ("ok", {})}},
        "classic branch protection on master",
    ),
    "archived": ({"archived": True}, "repo is archived"),
    "no-admin": ({"permissions": {"admin": False}}, "no admin permission"),
    "protected-id": (
        {"gets": {LIST: ("ok", [{"id": 28081842, "name": "x"}])}},
        "ruleset id this script never touches",
    ),
    "rulesets-unreadable": (
        {"gets": {LIST: ("http", 403)}},
        "ruleset list cannot be read (HTTP 403)",
    ),
}


@pytest.mark.parametrize("name", sorted(REFUSALS))
def test_a_refusal_writes_nothing_and_names_the_check(
    world, orr, fake_runner_cls, tmp_path, name
):
    changes, text = REFUSALS[name]
    gets = {
        path: getattr(fake_runner_cls, kind)(value)
        for path, (kind, value) in changes.get("gets", {}).items()
    }
    options = {k: v for k, v in changes.items() if k != "gets"}
    runner = world(gets=gets, **options)
    confirm = "0" * 64 if name == "wrong-confirm" else digest_of(orr)
    out_dir = None if name == "no-out" else tmp_path / "out"
    got = orr.apply_repo(runner, "acme", "acme-one", out_dir, confirm, NOW)
    assert got["ok"] is False and text in got["error"]
    assert posts(runner, fake_runner_cls) == []
    assert list(tmp_path.iterdir()) == []
    assert got["ids"] == {} and got["comment"] is None and got["before_file"] is None
    # nothing was read by id either: no call names a ruleset id
    assert not any("/rulesets/" in c.argv[-1] for c in runner.commands)


# --- apply: the write loop -----------------------------------------------------------


def test_the_write_order_and_the_read_back_after_each_write(
    world, orr, fake_runner_cls, tmp_path
):
    runner = world()
    got = apply(orr, runner, tmp_path)
    assert got["ok"] is True and got["error"] is None
    assert got["ids"] == {
        TAG_RULESET: 101,
        "protect-integration": 102,
        "protect-master": 103,
    }
    steps = []
    for record in runner.commands:
        if fake_runner_cls.method_of(record.argv) == "POST":
            steps.append(f"POST {record.stdin_name}")
        elif "/rulesets/" in record.argv[-1]:
            steps.append("GET " + record.argv[-1].rsplit("/", 1)[1])
    assert steps == [
        f"POST {TAG_RULESET}",
        "GET 101",
        "POST protect-integration",
        "GET 102",
        "POST protect-master",
        "GET 103",
    ]


def test_the_comment_and_the_rollback_commands_hold_the_ids(world, orr, tmp_path):
    got = apply(orr, world(), tmp_path)
    for name, number in got["ids"].items():
        assert f"{name}={number}" in got["comment"]
    assert "acme/acme-one" in got["comment"] and "2026-11-26" in got["comment"]
    assert got["rollback"] == [
        f"gh api --method DELETE {REPO}/rulesets/{n}" for n in (103, 102, 101)
    ]


def test_the_before_file_holds_complete_bodies_and_is_written_once(
    world, orr, fake_runner_cls, tmp_path
):
    ok = fake_runner_cls.ok
    full = {
        "id": 7,
        "name": "other",
        "target": "branch",
        "rules": [{"type": "deletion"}],
        "bypass_actors": [],
    }
    gets = {LIST: ok([{"id": 7, "name": "other"}]), f"{REPO}/rulesets/7": ok(full)}
    runner = world(gets=gets)
    got = apply(orr, runner, tmp_path)
    assert got["ok"] is True
    path = tmp_path / "out" / "acme-one-before.json"
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["rulesets"] == {"7": full}
    assert saved["protection"] == {"integration": "none", "master": "none"}
    assert saved["digest"] == digest_of(orr) and saved["repo"] == "acme-one"
    assert got["before_file"] == str(path)
    # a second run for the same repo and folder refuses before any write
    count = len(posts(runner, fake_runner_cls))
    again = apply(orr, runner, tmp_path)
    assert again["ok"] is False and "already exists" in again["error"]
    assert len(posts(runner, fake_runner_cls)) == count
    assert json.loads(path.read_text(encoding="utf-8")) == saved


def test_a_failed_before_state_read_writes_nothing(
    world, orr, fake_runner_cls, tmp_path
):
    f = fake_runner_cls
    gets = {LIST: f.ok([{"id": 7, "name": "other"}]), f"{REPO}/rulesets/7": f.http(403)}
    runner = world(gets=gets)
    got = apply(orr, runner, tmp_path)
    assert got["ok"] is False
    assert "before-state read failed for ruleset 7" in got["error"]
    assert posts(runner, f) == [] and list(tmp_path.iterdir()) == []


def test_a_read_back_mismatch_stops_after_the_first_ruleset(
    world, orr, fake_runner_cls, tmp_path
):
    def changed(argv, stdin):
        posted = json.loads(runner.executed[-2][1])
        return fake_runner_cls.ok({**posted, "enforcement": "disabled"})

    runner = world(gets={f"{REPO}/rulesets/101": changed})
    got = apply(orr, runner, tmp_path)
    assert got["ok"] is False and "differs" in got["error"]
    assert "enforcement" in got["error"]
    assert got["ids"] == {TAG_RULESET: 101}
    assert len(posts(runner, fake_runner_cls)) == 1
    assert got["rollback"] == [f"gh api --method DELETE {REPO}/rulesets/101"]
    assert got["comment"] is None


def test_a_failed_read_back_stops_the_run(world, orr, fake_runner_cls, tmp_path):
    runner = world(gets={f"{REPO}/rulesets/101": fake_runner_cls.http(500)})
    got = apply(orr, runner, tmp_path)
    assert got["ok"] is False and "read-back" in got["error"]
    assert got["ids"] == {TAG_RULESET: 101}
    assert len(posts(runner, fake_runner_cls)) == 1


def test_a_failed_post_stops_the_run(world, orr, fake_runner_cls, tmp_path):
    runner = world(post=fake_runner_cls.http(422))
    got = apply(orr, runner, tmp_path)
    assert got["ok"] is False
    assert "POST of protect-release-tags failed" in got["error"]
    assert got["ids"] == {} and got["rollback"] == []
    assert len(posts(runner, fake_runner_cls)) == 1
    assert (tmp_path / "out" / "acme-one-before.json").exists()


def test_a_post_without_an_id_stops_the_run(world, orr, fake_runner_cls, tmp_path):
    runner = world(post=fake_runner_cls.ok({"message": "no id"}))
    got = apply(orr, runner, tmp_path)
    assert got["ok"] is False and got["ids"] == {}


def timed_out_world(world, orr, fake_runner_cls, listed):
    """The first POST times out; the list that follows answers ``listed``."""
    ok = fake_runner_cls.ok
    tag_body = {**orr.render_tags(), "id": 55, **SERVER}
    runner = world(gets={LIST: [ok([]), listed], f"{REPO}/rulesets/55": ok(tag_body)})
    store = runner.store

    def post(argv, stdin):
        number = 101 + len(store)
        store[number] = json.loads(stdin)
        return ok({"id": number})

    runner.replies[("POST", f"{REPO}/rulesets")] = [orr.TIMED_OUT, post, post]
    return runner


def test_a_timed_out_post_is_followed_by_a_list_and_adopts_the_ruleset(
    world, orr, fake_runner_cls, tmp_path
):
    listed = fake_runner_cls.ok([{"id": 55, "name": TAG_RULESET}])
    runner = timed_out_world(world, orr, fake_runner_cls, listed)
    got = apply(orr, runner, tmp_path)
    assert got["ok"] is True
    assert got["ids"][TAG_RULESET] == 55
    kinds = [fake_runner_cls.method_of(c.argv) for c in runner.commands]
    after = runner.commands[kinds.index("POST") + 1]
    assert after.argv[-1] == LIST and "--paginate" in after.argv
    # the timed-out POST is never repeated: one POST per ruleset
    assert [c.stdin_name for c in posts(runner, fake_runner_cls)] == [
        TAG_RULESET,
        "protect-integration",
        "protect-master",
    ]
    assert f"gh api --method DELETE {REPO}/rulesets/55" in got["rollback"]


def test_a_timed_out_post_with_nothing_found_stops(
    world, orr, fake_runner_cls, tmp_path
):
    listed = fake_runner_cls.ok([])
    runner = timed_out_world(world, orr, fake_runner_cls, listed)
    got = apply(orr, runner, tmp_path)
    assert got["ok"] is False and "timed out" in got["error"]
    assert len(posts(runner, fake_runner_cls)) == 1 and got["ids"] == {}


def test_a_same_name_ruleset_gets_no_write_of_any_kind(
    world, orr, fake_runner_cls, tmp_path
):
    ok = fake_runner_cls.ok
    full = {"id": 7, "name": "protect-master", "target": "branch", "rules": []}
    summary = ok([{"id": 7, "name": "protect-master"}])
    runner = world(gets={LIST: summary, f"{REPO}/rulesets/7": ok(full)})
    got = apply(orr, runner, tmp_path)
    assert got["ok"] is True and got["skipped"] == ["protect-master"]
    assert "protect-master" not in got["ids"]
    assert [c.stdin_name for c in posts(runner, fake_runner_cls)] == [
        TAG_RULESET,
        "protect-integration",
    ]
    methods = {fake_runner_cls.method_of(c.argv) for c in runner.commands}
    assert methods == {"GET", "POST"}
    saved = json.loads((tmp_path / "out" / "acme-one-before.json").read_text())
    assert saved["rulesets"] == {"7": full}


def test_no_call_names_a_protected_ruleset_id(world, orr, tmp_path):
    runner = world()
    apply(orr, runner, tmp_path)
    assert orr.PROTECTED_RULESET_IDS == {28081842, 28081844, 28081845}
    for record in runner.commands:
        text = " ".join(record.argv)
        assert not any(str(i) in text for i in orr.PROTECTED_RULESET_IDS)
