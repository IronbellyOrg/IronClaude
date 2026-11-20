"""Task 18: ``orca repo list`` and the origin filter, over the fake runner."""

from __future__ import annotations

import pytest

from superclaude.cli.issue_watch import repos
from superclaude.cli.issue_watch.repos import RepoListError, list_repos

from .conftest import result

ORCA = "/home/u/.local/bin/orca-ide"
LIST_ARGV = (ORCA, "repo", "list")
OWNERS = ("IronbellyOrg",)


def _git(path: str) -> tuple[str, ...]:
    return ("git", "-C", path, "remote", "get-url", "origin")


def _line(n: int, name: str, path: str) -> str:
    return f"00000000-0000-4000-8000-{n:012d}  {name}  {path}"


def _script(lines: list[str], origins: dict[str, object]) -> dict:
    script: dict = {LIST_ARGV: result(stdout="\n".join(lines) + "\n")}
    for path, url in origins.items():
        script[_git(path)] = url if not isinstance(url, str) else result(stdout=url)
    return script


SIX = [
    _line(1, "IronClaude", "/home/u/workspaces/IronClaude"),
    _line(2, "Coder", "/home/u/workspaces/Coder"),
    _line(3, "scratch", "/tmp/scratch-checkout"),
    _line(4, "gitlab-thing", "/home/u/workspaces/gitlab-thing"),
    _line(5, "forkofsomeone", "/home/u/workspaces/forkofsomeone"),
    _line(6, "Ironeye", "/home/u/workspaces/Ironeye"),
]
SIX_ORIGINS = {
    "/home/u/workspaces/IronClaude": "https://github.com/IronbellyOrg/IronClaude.git\n",
    "/home/u/workspaces/Coder": "git@github.com:IronbellyOrg/Coder.git\n",
    "/home/u/workspaces/gitlab-thing": "https://gitlab.com/IronbellyOrg/x.git\n",
    "/home/u/workspaces/forkofsomeone": "https://github.com/SomeoneElse/IronClaude.git\n",
    "/home/u/workspaces/Ironeye": "https://github.com/ironbellyorg/Ironeye\n",
}


def test_six_repos_with_one_in_tmp_skipped_and_the_other_skips_reported(
    fake_runner,
) -> None:
    runner = fake_runner(_script(SIX, SIX_ORIGINS))
    got = list_repos(runner, ORCA, OWNERS)
    assert [(r.name, r.slug) for r in got.repos] == [
        ("IronClaude", "IronbellyOrg/IronClaude"),
        ("Coder", "IronbellyOrg/Coder"),
        ("Ironeye", "ironbellyorg/Ironeye"),
    ]
    assert [(s.name, s.reason) for s in got.skipped] == [
        ("scratch", "path_in_tmp"),
        ("gitlab-thing", "origin_not_github"),
        ("forkofsomeone", "foreign_owner"),
    ]
    first = got.repos[0]
    assert first.orca_id == "00000000-0000-4000-8000-000000000001"
    assert first.path == "/home/u/workspaces/IronClaude"
    # the /tmp repo's origin was never read
    assert _git("/tmp/scratch-checkout") not in [argv for argv, _ in runner.calls]


def test_a_non_github_origin_is_skipped(fake_runner) -> None:
    path = "/home/u/workspaces/x"
    runner = fake_runner(
        _script([_line(1, "x", path)], {path: "https://gitlab.com/IronbellyOrg/x.git"})
    )
    got = list_repos(runner, ORCA, OWNERS)
    assert got.repos == () and [s.reason for s in got.skipped] == ["origin_not_github"]


def test_a_foreign_owner_is_skipped_and_an_allowed_one_matches_any_case(
    fake_runner,
) -> None:
    a, b = "/home/u/workspaces/a", "/home/u/workspaces/b"
    runner = fake_runner(
        _script(
            [_line(1, "a", a), _line(2, "b", b)],
            {
                a: "https://github.com/Other/a.git",
                b: "https://github.com/IRONBELLYORG/b",
            },
        )
    )
    got = list_repos(runner, ORCA, ["ironbellyorg"])
    assert [r.name for r in got.repos] == ["b"]
    assert [(s.name, s.reason) for s in got.skipped] == [("a", "foreign_owner")]


@pytest.mark.parametrize(
    ("reply", "reason"),
    [
        (result(stderr="boom", returncode=1), "list_failed"),
        (result(returncode=127), "list_failed"),
        (result(spawn_error="FileNotFoundError"), "list_failed"),
        (result(timed_out=True), "list_timeout"),
    ],
)
def test_a_failed_or_timed_out_list_raises_never_an_empty_list(
    fake_runner, reply, reason
) -> None:
    runner = fake_runner({LIST_ARGV: reply})
    with pytest.raises(RepoListError) as err:
        list_repos(runner, ORCA, OWNERS)
    assert err.value.reason == reason


@pytest.mark.parametrize(
    "text",
    [
        "just-one-field\n",
        "only  two\n",
        "id-1  name  relative/path\n",
        "bad id!  name  /home/u/x\n",
        "<html>not a list</html>\n",
    ],
)
def test_output_that_cannot_be_read_raises(fake_runner, text) -> None:
    runner = fake_runner({LIST_ARGV: result(stdout=text)})
    with pytest.raises(RepoListError) as err:
        list_repos(runner, ORCA, OWNERS)
    assert err.value.reason == "unreadable_list"


@pytest.mark.parametrize("text", ["", "\n", "\n\n  \n"])
def test_an_empty_but_successful_list_returns_no_repos(fake_runner, text) -> None:
    runner = fake_runner({LIST_ARGV: result(stdout=text)})
    got = list_repos(runner, ORCA, OWNERS)
    assert got.repos == () and got.skipped == ()


def test_an_unreadable_origin_is_skipped_not_fatal(fake_runner) -> None:
    ok_path, bad, silent = "/home/u/a", "/home/u/b", "/home/u/c"
    runner = fake_runner(
        _script(
            [_line(1, "a", ok_path), _line(2, "b", bad), _line(3, "c", silent)],
            {
                ok_path: "https://github.com/IronbellyOrg/a.git",
                bad: result(returncode=128, stderr="fatal: not a git repository"),
                silent: result(stdout="\n"),
            },
        )
    )
    got = list_repos(runner, ORCA, OWNERS)
    assert [r.name for r in got.repos] == ["a"]
    assert [(s.name, s.reason) for s in got.skipped] == [
        ("b", "origin_unreadable"),
        ("c", "origin_unreadable"),
    ]


def test_a_timed_out_git_call_is_an_unreadable_origin(fake_runner) -> None:
    path = "/home/u/a"
    runner = fake_runner(_script([_line(1, "a", path)], {path: result(timed_out=True)}))
    got = list_repos(runner, ORCA, OWNERS)
    assert [s.reason for s in got.skipped] == ["origin_unreadable"]


def test_a_path_with_spaces_and_a_name_with_dots_are_read(fake_runner) -> None:
    path = "/home/u/my work/repo"
    runner = fake_runner(
        _script(
            [_line(1, "coder-bmad.live", path)],
            {path: "https://github.com/IronbellyOrg/repo.git"},
        )
    )
    got = list_repos(runner, ORCA, OWNERS)
    assert [(r.name, r.path) for r in got.repos] == [("coder-bmad.live", path)]


@pytest.mark.parametrize("path", ["/tmp", "/tmp/x", "/tmp/a/b/c"])
def test_every_path_at_or_under_tmp_is_skipped(fake_runner, path) -> None:
    runner = fake_runner({LIST_ARGV: result(stdout=_line(1, "t", path) + "\n")})
    got = list_repos(runner, ORCA, OWNERS)
    assert [s.reason for s in got.skipped] == ["path_in_tmp"] and got.repos == ()


@pytest.mark.parametrize("path", ["/tmpfoo/x", "/home/u/tmp/x", "/var/tmp/x"])
def test_a_path_that_only_looks_like_tmp_is_not_skipped_for_it(
    fake_runner, path
) -> None:
    runner = fake_runner(
        _script([_line(1, "t", path)], {path: "https://github.com/IronbellyOrg/t.git"})
    )
    got = list_repos(runner, ORCA, OWNERS)
    assert [r.name for r in got.repos] == ["t"]


def test_the_commands_are_argv_lists_with_the_given_timeouts(fake_runner) -> None:
    path = "/home/u/a"
    runner = fake_runner(
        _script([_line(1, "a", path)], {path: "https://github.com/IronbellyOrg/a.git"})
    )
    list_repos(runner, ORCA, OWNERS, list_timeout=7.0, git_timeout=3.0)
    assert [argv for argv, _ in runner.calls] == [LIST_ARGV, _git(path)]
    assert runner.timeouts == [7.0, 3.0]
    assert all(cwd is None for _, cwd in runner.calls)


def test_the_module_has_no_shell_and_no_process_import() -> None:
    source = open(repos.__file__, encoding="utf-8").read()
    for banned in ("subprocess", "os.system", "shell=True", "os.popen"):
        assert banned not in source
