"""parse_args and main: usage errors, exit codes, what is printed, the full fake run."""

from __future__ import annotations

import re
import subprocess
from datetime import datetime, timezone

import pytest

NOW = datetime(2026, 11, 26, 17, 0, tzinfo=timezone.utc)
REPO = "repos/acme/acme-one"
BASE = ["--org", "acme", "--repo", "acme-one"]
SHAPE = re.compile(
    r"^repos/acme/acme-one(/(branches/[\w./-]+|rulesets(/\d+)?|activity|commits"
    r"|commits/[0-9a-f]+/pulls|git/matching-refs/tags/v))?(\?[\w=&:./-]+)?$"
)


def digest_of(orr):
    return orr.payload_digest(orr.plan_bodies(["master", "integration"]))


def run_main(orr, argv, runner, **kwargs):
    return orr.main(argv, runner=runner, now=NOW, **kwargs)


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["--repo", "acme-one"],
        ["--org", "acme"],
        ["--org", "SuperClaude-Org", "--repo", "acme-one"],
        ["--org", "superclaude-org", "--repo", "acme-one"],
        ["--org", "SUPERCLAUDE-ORG", "--repo", "acme-one"],
        ["--org", "", "--repo", "acme-one"],
        ["--org", "acme", "--repo", "a", "--repo", "b"],
        ["--org", "acme", "--repo", "a,b"],
        ["--org", "acme", "--repo", "a b"],
        ["--org", "acme", "--repo", "acme/acme-one"],
        [*BASE, "--apply"],
        [*BASE, "--confirm", "abc"],
        [*BASE, "--apply", "--confirm", ""],
        [*BASE, "--surprise"],
        [*BASE, "--app"],
    ],
)
def test_usage_errors_exit_64_and_call_nothing(orr, world, capsys, argv):
    runner = world()
    assert run_main(orr, argv, runner) == orr.EXIT_USAGE == 64
    assert "usage error" in capsys.readouterr().err
    assert runner.executed == []


def test_a_refusal_in_apply_exits_69_and_names_the_check(orr, world, capsys, tmp_path):
    argv = [*BASE, "--out", str(tmp_path / "out"), "--apply", "--confirm", "0" * 64]
    runner = world()
    assert run_main(orr, argv, runner) == orr.EXIT_FAILED == 69
    captured = capsys.readouterr()
    assert "refused: confirm digest does not match" in captured.err
    assert captured.out == ""
    assert not any(c.stdin_name for c in runner.commands)


def test_apply_without_out_is_a_refusal_not_a_usage_error(orr, world, capsys):
    argv = [*BASE, "--apply", "--confirm", digest_of(orr)]
    assert run_main(orr, argv, world()) == orr.EXIT_FAILED
    assert "no --out folder" in capsys.readouterr().err


def test_an_out_folder_that_cannot_be_created_exits_69_without_a_traceback(
    orr, world, capsys, tmp_path
):
    blocker = tmp_path / "a-file"
    blocker.write_text("x", encoding="utf-8")
    argv = [
        *BASE,
        "--out",
        str(blocker / "out"),
        "--apply",
        "--confirm",
        digest_of(orr),
    ]
    runner = world()
    assert run_main(orr, argv, runner) == orr.EXIT_FAILED
    captured = capsys.readouterr()
    assert captured.err.startswith("failed: ") and "a-file" in captured.err
    assert not any(c.stdin_name for c in runner.commands)


def test_an_unreadable_rule_file_exits_69_without_a_traceback(
    orr, world, capsys, monkeypatch, tmp_path
):
    monkeypatch.setattr(orr, "RULES_DIR", tmp_path / "missing")
    assert run_main(orr, BASE, world()) == orr.EXIT_FAILED
    assert capsys.readouterr().err.startswith("failed: ")


def test_a_successful_apply_prints_the_comment_and_one_delete_per_id(
    orr, world, capsys, tmp_path
):
    out = tmp_path / "out"
    argv = [*BASE, "--out", str(out), "--apply", "--confirm", digest_of(orr)]
    assert run_main(orr, argv, world()) == orr.EXIT_OK
    text = capsys.readouterr().out
    assert "comment for issue 838: Applied rulesets to acme/acme-one" in text
    assert "protect-release-tags=101" in text and "protect-master=103" in text
    deletes = [ln.strip() for ln in text.splitlines() if "--method DELETE" in ln]
    assert sorted(deletes) == sorted(
        f"gh api --method DELETE {REPO}/rulesets/{n}" for n in (101, 102, 103)
    )
    assert (out / "acme-one-before.json").exists()


def test_a_read_back_failure_prints_the_one_written_id_and_exits_69(
    orr, world, fake_runner_cls, capsys, tmp_path
):
    gets = {f"{REPO}/rulesets/101": fake_runner_cls.http(500)}
    argv = [
        *BASE,
        "--out",
        str(tmp_path / "out"),
        "--apply",
        "--confirm",
        digest_of(orr),
    ]
    assert run_main(orr, argv, world(gets=gets)) == orr.EXIT_FAILED
    captured = capsys.readouterr()
    assert "created: protect-release-tags (id 101)" in captured.out
    assert captured.out.count("--method DELETE") == 1
    assert f"{REPO}/rulesets/101" in captured.out
    assert "comment for issue 838" not in captured.out
    assert "failed: read-back of protect-release-tags" in captured.err


def test_a_dry_run_exits_0_prints_the_digest_and_never_posts(
    orr, world, fake_runner_cls, capsys
):
    runner = world()
    runner.read_only = True
    assert run_main(orr, BASE, runner) == orr.EXIT_OK
    assert f"digest: {digest_of(orr)}" in capsys.readouterr().out
    assert all(fake_runner_cls.method_of(c.argv) == "GET" for c in runner.commands)


def test_a_dry_run_of_an_unreadable_repo_exits_69(orr, world, fake_runner_cls, capsys):
    runner = world(gets={REPO: fake_runner_cls.http(404)})
    assert run_main(orr, BASE, runner) == orr.EXIT_FAILED
    assert "no plan" in capsys.readouterr().out


def test_the_full_fake_run_uses_only_allowed_shapes(
    orr, world, fake_runner_cls, capsys, tmp_path
):
    runner = world()
    assert run_main(orr, BASE, runner) == orr.EXIT_OK
    printed = re.search(r"^digest: (\w+)$", capsys.readouterr().out, re.M).group(1)
    argv = [*BASE, "--out", str(tmp_path / "out"), "--apply", "--confirm", printed]
    assert run_main(orr, argv, runner) == orr.EXIT_OK
    assert len(runner.commands) > 10
    for record in runner.commands:
        path = fake_runner_cls.path_of(record.argv)
        assert record.argv[:2] == ["gh", "api"]
        assert SHAPE.match(path), record.argv
        text = " ".join(record.argv)
        assert "superclaude-org" not in text.lower()
        assert not any(str(i) in text for i in orr.PROTECTED_RULESET_IDS)
        if fake_runner_cls.method_of(record.argv) != "GET":
            assert path == f"{REPO}/rulesets" and record.stdin_name


def test_main_finds_the_rule_files_from_any_working_folder(
    orr, world, capsys, tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    assert run_main(orr, BASE, world()) == orr.EXIT_OK
    assert f"digest: {digest_of(orr)}" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []


def test_main_builds_a_read_only_runner_for_a_dry_run_and_passes_env(
    orr, monkeypatch, capsys
):
    seen = []

    def stub(argv, **kwargs):
        seen.append((argv, kwargs["env"]))
        return subprocess.CompletedProcess(argv, 1, "", "gh: Not Found (HTTP 404)")

    monkeypatch.setattr(subprocess, "run", stub)
    code = orr.main(BASE, env={"GH_TOKEN": "t"}, now=NOW)
    assert code == orr.EXIT_FAILED
    assert seen[0][0] == ["gh", "api", REPO]
    assert seen[0][1] == {"GH_TOKEN": "t", "GH_PROMPT_DISABLED": "1"}
    assert "cannot be read" in capsys.readouterr().out
