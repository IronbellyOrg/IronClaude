"""The allowlisted Runner, check_org and the fake runner of conftest."""

from __future__ import annotations

import json
import re
import subprocess

import pytest

REPO = "repos/acme/acme-one"
BODY = json.dumps({"name": "protect-master"})

ACCEPTED = [
    ["gh", "api", REPO],
    ["gh", "api", f"{REPO}/branches/master"],
    ["gh", "api", f"{REPO}/branches/release/1.0"],
    ["gh", "api", f"{REPO}/branches/master/protection"],
    ["gh", "api", f"{REPO}/rulesets"],
    ["gh", "api", "--paginate", f"{REPO}/rulesets?per_page=100"],
    ["gh", "api", f"{REPO}/rulesets/12"],
    [
        "gh",
        "api",
        "--paginate",
        f"{REPO}/activity?ref=refs/heads/master&time_period=quarter&per_page=100",
    ],
    ["gh", "api", f"{REPO}/commits?sha=master&since=2026-08-28T17:25:08Z"],
    ["gh", "api", f"{REPO}/commits/abc1234def/pulls"],
    ["gh", "api", f"{REPO}/git/matching-refs/tags/v"],
    ["gh", "api", "--paginate", f"{REPO}/git/matching-refs/tags/v"],
]
POST = ["gh", "api", "--method", "POST", f"{REPO}/rulesets", "--input", "-"]

REFUSED = [
    [],
    [""],
    ["git", "status"],
    ["gh"],
    ["gh", "pr", "list"],
    ["gh", "api"],
    ["gh", "api", "user"],
    ["gh", "api", f"{REPO}/hooks"],
    ["gh", "api", f"{REPO}/keys"],
    ["gh", "api", f"{REPO}/installations"],
    ["gh", "api", f"{REPO}/branches"],
    ["gh", "api", f"{REPO}/rulesets/abc"],
    ["gh", "api", f"{REPO}/commits/xyz/pulls"],
    ["gh", "api", f"{REPO}/git/matching-refs/heads/v"],
    ["gh", "api", "repos/-x/acme-one"],
    ["gh", "api", "repos/acme/-one"],
    ["gh", "api", f"{REPO}/branches/-x"],
    ["gh", "api", f"{REPO}/branches/../rulesets"],
    ["gh", "api", f"{REPO}/branches/a~b"],
    ["gh", "api", f"{REPO}/branches/master/protection/"],
    ["gh", "api", "repos/acme/.."],
    ["gh", "api", "repos/acme/acme-one/../other"],
    ["gh", "api", "repos/SuperClaude-Org/acme-one"],
    ["gh", "api", "repos/superclaude-org/acme-one"],
    ["gh", "api", REPO, "--jq", ".name"],
    ["gh", "api", REPO, "-X", "DELETE"],
    ["gh", "api", "--method", "DELETE", f"{REPO}/rulesets/12"],
    ["gh", "api", "--method", "PUT", f"{REPO}/rulesets/12", "--input", "-"],
    ["gh", "api", "--method", "GET", REPO],
    ["gh", "api", REPO, "--input", "-"],
    ["gh", "api", "--paginate", REPO],
    ["gh", "api", f"{REPO}/rulesets?evil=1"],
    ["gh", "api", f"{REPO}/rulesets?per_page"],
    ["gh", "api", REPO, f"{REPO}/rulesets"],
    ["gh", "api", REPO, "--paginate", "--paginate"],
]


def test_refused_calls_never_reach_execute(fake_runner_cls, orr):
    runner = fake_runner_cls()
    for argv in REFUSED:
        with pytest.raises(orr.RefusedCommand):
            runner.run(argv)
    assert runner.executed == []
    assert runner.commands == []


@pytest.mark.parametrize(
    "bad_post",
    [
        POST[:-2],
        POST[:-1] + ["x"],
        ["gh", "api", "--method", "POST", REPO, "--input", "-"],
        ["gh", "api", "--method", "POST", f"{REPO}/rulesets/12", "--input", "-"],
        ["gh", "api", "--method", "POST", f"{REPO}/rulesets?x=1", "--input", "-"],
        ["gh", "api", "--method", "POST", "--paginate", f"{REPO}/rulesets"]
        + ["--input", "-"],
    ],
)
def test_bad_posts_are_refused(fake_runner_cls, orr, bad_post):
    runner = fake_runner_cls()
    with pytest.raises(orr.RefusedCommand):
        runner.run(bad_post, BODY)
    assert runner.executed == []


@pytest.mark.parametrize("stdin", [None, "", "not json", "[]", "{}", '{"name": 3}'])
def test_a_post_needs_a_body_with_a_name(fake_runner_cls, orr, stdin):
    runner = fake_runner_cls()
    with pytest.raises(orr.RefusedCommand):
        runner.run(POST, stdin)
    assert runner.executed == []


def test_read_only_runner_refuses_post_but_reads(fake_runner_cls, orr):
    runner = fake_runner_cls(read_only=True)
    with pytest.raises(orr.RefusedCommand):
        runner.run(POST, BODY)
    assert runner.executed == [] and runner.commands == []
    runner.run(["gh", "api", REPO])
    assert len(runner.executed) == 1


def test_normal_runner_accepts_a_post_and_records_its_name(fake_runner_cls):
    runner = fake_runner_cls(
        {("POST", f"{REPO}/rulesets"): fake_runner_cls.ok({"id": 5})}
    )
    result = runner.run(POST, BODY)
    assert result.returncode == 0
    assert runner.commands[0].stdin_name == "protect-master"
    assert runner.executed == [(POST, BODY)]


def test_check_org(orr):
    for bad in (
        "SuperClaude-Org",
        "superclaude-org",
        "SUPERCLAUDE-ORG",
        "",
        "-x",
        "a/b",
    ):
        with pytest.raises(ValueError):
            orr.check_org(bad)
    assert orr.check_org("acme") == "acme"


def test_every_accepted_call_is_an_allowed_shape(fake_runner_cls):
    runner = fake_runner_cls()
    for argv in ACCEPTED:
        runner.run(argv)
    runner.run(POST, BODY)
    assert len(runner.commands) == len(ACCEPTED) + 1
    shape = re.compile(
        r"^repos/acme/acme-one(/(branches/[\w./-]+|rulesets(/\d+)?|activity|commits"
        r"|commits/[0-9a-f]+/pulls|git/matching-refs/tags/v))?(\?[\w=&:./-]+)?$"
    )
    for record in runner.commands:
        assert record.argv[:2] == ["gh", "api"]
        assert shape.match(runner.path_of(record.argv)), record.argv
    assert len(runner.executed) == len(runner.commands)


def test_replies_are_keyed_by_method_and_path(fake_runner_cls, orr):
    ok = fake_runner_cls.ok
    seen = []

    def echo(argv, stdin):
        seen.append(stdin)
        return ok({"echo": True})

    runner = fake_runner_cls(
        {
            ("GET", f"{REPO}/rulesets"): ok([]),
            ("GET", f"{REPO}/rulesets?per_page=100"): ok(["paged"]),
            ("POST", f"{REPO}/rulesets"): [ok({"id": 1}), ok({"id": 2}), echo],
        }
    )
    assert json.loads(runner.run(["gh", "api", f"{REPO}/rulesets"]).stdout) == []
    paged = runner.run(["gh", "api", f"{REPO}/rulesets?per_page=100"])
    assert json.loads(paged.stdout) == ["paged"]
    ids = [json.loads(runner.run(POST, BODY).stdout) for _ in range(2)]
    assert ids == [{"id": 1}, {"id": 2}]
    assert runner.run(POST, BODY).returncode == 0 and seen == [BODY]
    # the list is used up, and a path with no reply gets 127
    assert runner.run(POST, BODY).returncode == 127
    assert runner.run(["gh", "api", REPO]).returncode == 127


def test_timeout_becomes_the_named_result(orr, monkeypatch):
    seen = {}

    def stub(argv, **kwargs):
        seen.update(kwargs)
        raise subprocess.TimeoutExpired(argv, kwargs["timeout"])

    monkeypatch.setattr(subprocess, "run", stub)
    result = orr.Runner().run(["gh", "api", REPO])
    assert result == orr.TIMED_OUT
    assert result.returncode == 124
    assert seen["timeout"] == orr.TIMEOUT_SECONDS


def test_a_missing_program_is_a_127_result(orr, monkeypatch):
    def stub(argv, **kwargs):
        raise FileNotFoundError("gh")

    monkeypatch.setattr(subprocess, "run", stub)
    assert orr.Runner().run(["gh", "api", REPO]).returncode == 127


def test_a_refused_call_starts_no_process(orr, monkeypatch):
    def stub(argv, **kwargs):
        raise AssertionError("a process was started")

    monkeypatch.setattr(subprocess, "run", stub)
    with pytest.raises(orr.RefusedCommand):
        orr.Runner().run(["git", "status"])
    with pytest.raises(orr.RefusedCommand):
        orr.Runner(read_only=True).run(POST, BODY)


def test_the_real_runner_passes_stdin_and_returns_output(orr, monkeypatch):
    seen = {}

    def stub(argv, **kwargs):
        seen.update(kwargs)
        return subprocess.CompletedProcess(argv, 0, stdout="out", stderr="err")

    monkeypatch.setattr(subprocess, "run", stub)
    result = orr.Runner().run(POST, BODY)
    assert (result.returncode, result.stdout, result.stderr) == (0, "out", "err")
    assert seen["input"] == BODY
